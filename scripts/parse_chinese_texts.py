#!/usr/bin/env python3
"""
Parse two Chinese literature seed files into grammar.json files:
1. The Shih King (Book of Poetry) - Gutenberg #9394
2. Chinese Literature Anthology - Gutenberg #10056
"""
import json, re, os

# ═══════════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════════

def load_body(filepath):
    """Load a Gutenberg text and extract body between markers."""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    start = text.find("\n", start) + 1
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    return text[start:end].strip()

def truncate(text, limit=2800):
    if len(text) > limit:
        bp = text.rfind(".", 0, limit - 200)
        if bp == -1:
            bp = limit - 200
        remaining = len(text[bp:].split())
        return text[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    return text

def clean_text(text):
    """Clean up text: normalize whitespace, strip footnotes."""
    # Remove footnote markers like [1], [2], etc.
    text = re.sub(r'\[(\d+)\]', '', text)
    # Remove footnote blocks: lines starting with [1. or [2. etc
    lines = text.split('\n')
    cleaned = []
    in_footnote = False
    for line in lines:
        if re.match(r'\s*\[\d+\.', line):
            in_footnote = True
            continue
        if in_footnote:
            if line.strip().endswith(']'):
                in_footnote = False
                continue
            if ']' in line:
                in_footnote = False
                continue
            continue
        cleaned.append(line)
    return '\n'.join(cleaned).strip()

def make_id(text):
    """Convert text to a hyphenated ID."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:60]

def write_grammar(grammar, outdir):
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, "grammar.json")
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"Wrote {outpath}: {len(grammar['items'])} items")


# ═══════════════════════════════════════════════════════════════════════════
# GRAMMAR 1: THE SHIH KING (Book of Poetry)
# ═══════════════════════════════════════════════════════════════════════════

def parse_shih_king():
    body = load_body("seeds/shih-king.txt")
    lines = body.split('\n')

    # The Shih King has 4 major parts:
    # I. Odes of the Temple and the Altar (Sung)
    # II. The Minor Odes of the Kingdom (Hsiao Ya)
    # III. The Major Odes of the Kingdom (Ta Ya)
    # IV. Lessons from the States (Kwo Fang)
    # Each part has Books, each Book has Odes

    # Find part boundaries
    part_markers = [
        ("I. ODES OF THE TEMPLE AND THE ALTAR.", "temple-and-altar", "Part I: Odes of the Temple and the Altar (Sung)", "temple-altar"),
        ("II. THE MINOR ODES OF THE KINGDOM.", "minor-odes", "Part II: The Minor Odes of the Kingdom (Hsiao Ya)", "minor-odes"),
        ("III. THE MAJOR ODES OF THE KINGDOM.", "major-odes", "Part III: The Major Odes of the Kingdom (Ta Ya)", "major-odes"),
        ("IV. LESSONS FROM THE STATES.", "lessons-states", "Part IV: Lessons from the States (Kwo Fang)", "lessons-states"),
    ]

    # Find line numbers of part starts
    part_lines = []
    for marker, pid, pname, pcat in part_markers:
        for i, line in enumerate(lines):
            if marker in line.strip():
                part_lines.append((i, pid, pname, pcat, marker))
                break

    # Find all ODE headings
    ode_pattern = re.compile(r'^\s*ODE\s+(\d+)(?:,\s*STANZA[S]?\s+[\dA-Z, AND TO]+)?\.?\s+THE\s+(.+?)\.?\s*$', re.IGNORECASE)
    # Also match simpler ode patterns
    ode_pattern2 = re.compile(r'^\s*ODE\s+(\d+)(?:,\s*STANZA[S]?\s+[^.]+)?\.?\s+THE\s+(.+?)\.?\s*$', re.IGNORECASE)

    # Find all BOOK headings
    book_pattern = re.compile(r'^\s*BOOK\s+([IVXLC]+)\.?\s+THE\s+(.+?)\.?\s*$', re.IGNORECASE)

    # Extract odes with their text
    ode_locations = []
    for i, line in enumerate(lines):
        m = ode_pattern.match(line) or ode_pattern2.match(line)
        if m:
            ode_num = m.group(1)
            ode_name = m.group(2).strip().rstrip('.')
            ode_locations.append((i, ode_num, ode_name))

    # Also find BOOK headers
    book_locations = []
    for i, line in enumerate(lines):
        m = book_pattern.match(line)
        if m:
            book_num = m.group(1)
            book_name = m.group(2).strip().rstrip('.')
            book_locations.append((i, book_num, book_name))

    print(f"Found {len(ode_locations)} odes, {len(book_locations)} books, {len(part_lines)} parts")

    # Determine which part each ode belongs to
    def get_part_for_line(ln):
        current_part = None
        for pl, pid, pname, pcat, _ in part_lines:
            if ln >= pl:
                current_part = (pid, pname, pcat)
        return current_part or ("unknown", "Unknown", "unknown")

    # Determine which book each ode belongs to
    def get_book_for_line(ln):
        current_book = None
        for bl, bnum, bname in book_locations:
            if ln >= bl:
                current_book = (bnum, bname)
        return current_book or ("?", "Unknown Book")

    # Extract ode text
    items = []
    sort_order = 0

    # Create L1 items for each ode
    for idx, (ode_ln, ode_num, ode_name) in enumerate(ode_locations):
        # Find end: next ode or next book or next part
        end_ln = len(lines)
        for next_ln, _, _ in ode_locations:
            if next_ln > ode_ln:
                end_ln = next_ln
                break
        for next_ln, _, _ in book_locations:
            if next_ln > ode_ln and next_ln < end_ln:
                end_ln = next_ln
                break

        # Extract description line (ALL CAPS line after ODE heading)
        desc_lines = []
        text_lines = []
        in_desc = True
        blank_after_heading = 0

        for j in range(ode_ln + 1, end_ln):
            line = lines[j]
            stripped = line.strip()
            if not stripped:
                if in_desc and desc_lines:
                    in_desc = False
                blank_after_heading += 1
                continue
            if in_desc and stripped == stripped.upper() and len(stripped) > 5:
                desc_lines.append(stripped)
            else:
                in_desc = False
                text_lines.append(line.rstrip())

        # Clean text
        raw_text = '\n'.join(text_lines)
        text = clean_text(raw_text)
        text = truncate(text)

        description = ' '.join(desc_lines) if desc_lines else ""

        # Determine part and book
        part_id, part_name, part_cat = get_part_for_line(ode_ln)
        book_num, book_name = get_book_for_line(ode_ln)

        ode_id = f"{part_id}-ode-{ode_num}"
        # Make unique if needed
        existing_ids = [item['id'] for item in items]
        if ode_id in existing_ids:
            suffix = 2
            while f"{ode_id}-{suffix}" in existing_ids:
                suffix += 1
            ode_id = f"{ode_id}-{suffix}"

        sort_order += 1
        display_name = f"Ode {ode_num}: {ode_name.title()}"
        if len(display_name) > 80:
            display_name = f"Ode {ode_num}: {ode_name.title()[:70]}..."

        sections = {}
        if description:
            sections["Description"] = description.capitalize()
        sections["Verse"] = text if text.strip() else "(Text not available)"
        sections["Context"] = f"From {part_name}, Book {book_num}: {book_name}"

        keywords = ["poetry", "ancient-china"]
        if "sacrifice" in description.lower() or "sacrific" in text.lower()[:500]:
            keywords.append("sacrifice")
        if "heaven" in text.lower()[:500]:
            keywords.append("heaven")
        if "virtue" in description.lower() or "virtue" in text.lower()[:500]:
            keywords.append("virtue")
        if "wife" in description.lower() or "marriage" in description.lower():
            keywords.append("marriage")
        if "war" in description.lower() or "soldier" in description.lower():
            keywords.append("war")
        if "king" in description.lower() or "king" in text.lower()[:200]:
            keywords.append("kingship")
        if "lamenting" in description.lower() or "sorrow" in description.lower() or "distress" in description.lower():
            keywords.append("lament")

        items.append({
            "id": ode_id,
            "name": display_name,
            "sort_order": sort_order,
            "category": part_cat,
            "level": 1,
            "sections": sections,
            "keywords": keywords,
            "metadata": {
                "part": part_name,
                "book": f"Book {book_num}: {book_name}",
                "ode_number": int(ode_num)
            }
        })

    # Create L2 items for each Part
    part_descriptions = {
        "temple-altar": "The Sung (Odes of the Temple and the Altar) contains 40 pieces appropriate to sacrificial services: 31 belonging to the royal court of Chou, 4 to the marquises of Lu, and 5 to the kings of Shang. These are the explicitly religious pieces of the Shih King, composed for ancestral worship and state rituals.",
        "minor-odes": "The Hsiao Ya (Minor Odes of the Kingdom) contains 74 pieces in eight Books, sung at gatherings of feudal princes and their appearances at the royal court. They describe the manners and governance in successive reigns, ranging from celebration to sharp political critique.",
        "major-odes": "The Ta Ya (Major Odes of the Kingdom) contains 31 pieces in three Books, sung on grand occasions at the royal court. These longer, more dignified poems celebrate the founding of the Chou dynasty, praise legendary kings, and address cosmic themes of governance and divine mandate.",
        "lessons-states": "The Kwo Fang (Lessons from the States) contains 160 pieces in fifteen Books, descriptive of manners and events in the feudal states of Chou. Nearly all are short folk songs dealing with love, marriage, labor, military service, and political complaint -- the most human and personal section of the Shih King."
    }

    for marker, pid, pname, pcat in part_markers:
        part_odes = [item['id'] for item in items if item['category'] == pcat]
        if not part_odes:
            continue
        sort_order += 1
        items.append({
            "id": f"part-{pid}",
            "name": pname,
            "sort_order": sort_order,
            "category": "parts",
            "level": 2,
            "sections": {
                "About": part_descriptions.get(pcat, f"Collection of odes from {pname}."),
                "For Readers": f"This section contains {len(part_odes)} odes. Browse them to explore the themes and concerns of ancient Chinese poetry in this tradition."
            },
            "keywords": ["collection", "chinese-poetry", "ancient-china"],
            "composite_of": part_odes,
            "relationship_type": "emergence",
            "metadata": {}
        })

    # Create L2 thematic groupings
    themes = {
        "sacrifice-ritual": {
            "name": "Sacrifice and Ritual",
            "desc": "Odes concerned with sacrificial offerings, temple rites, and ancestral worship. These represent the religious heart of the Shih King, showing how the ancient Chinese understood their relationship with Heaven, ancestors, and the spiritual world.",
            "keywords_match": ["sacrifice"]
        },
        "love-marriage": {
            "name": "Love and Marriage",
            "desc": "Odes about courtship, marriage, spousal devotion, separation, and longing. These folk songs capture the emotional life of ancient China with striking freshness and directness.",
            "keywords_match": ["marriage"]
        },
        "governance-kingship": {
            "name": "Governance and Kingship",
            "desc": "Odes celebrating virtuous rulers, lamenting misgovernance, and reflecting on the mandate of Heaven as it applies to political authority. These pieces show the deep connection between ethics and politics in Chinese thought.",
            "keywords_match": ["kingship"]
        },
        "lament-hardship": {
            "name": "Lament and Hardship",
            "desc": "Odes expressing grief, complaint, and endurance in the face of suffering -- whether from war, poverty, political oppression, or personal loss. These reveal the voice of ordinary people speaking truth to power.",
            "keywords_match": ["lament", "war"]
        }
    }

    for theme_id, theme_info in themes.items():
        matching = [item['id'] for item in items if item['level'] == 1
                   and any(kw in item['keywords'] for kw in theme_info['keywords_match'])]
        if len(matching) < 2:
            continue
        sort_order += 1
        items.append({
            "id": f"theme-{theme_id}",
            "name": theme_info['name'],
            "sort_order": sort_order,
            "category": "themes",
            "level": 2,
            "sections": {
                "About": theme_info['desc'],
                "For Readers": f"This thematic grouping contains {len(matching)} odes that share a common concern with {theme_info['name'].lower()}."
            },
            "keywords": ["theme", "chinese-poetry"],
            "composite_of": matching,
            "relationship_type": "emergence",
            "metadata": {}
        })

    # L3 meta-categories
    part_ids = [item['id'] for item in items if item['category'] == 'parts']
    theme_ids = [item['id'] for item in items if item['category'] == 'themes']

    if part_ids:
        sort_order += 1
        items.append({
            "id": "meta-traditional-divisions",
            "name": "The Four Traditional Divisions",
            "sort_order": sort_order,
            "category": "meta",
            "level": 3,
            "sections": {
                "About": "The Shih King is traditionally divided into four parts: the Sung (Temple Odes), Hsiao Ya (Minor Odes), Ta Ya (Major Odes), and Kwo Fang (Lessons from the States). This division dates back to before Confucius and reflects a progression from the most sacred and public poetry to the most personal and local.",
                "For Readers": "Start with the Lessons from the States for the most accessible folk poetry, then explore the Odes for court and ritual perspectives."
            },
            "keywords": ["structure", "tradition"],
            "composite_of": part_ids,
            "relationship_type": "emergence",
            "metadata": {}
        })

    if theme_ids:
        sort_order += 1
        items.append({
            "id": "meta-thematic-landscape",
            "name": "Thematic Landscape",
            "sort_order": sort_order,
            "category": "meta",
            "level": 3,
            "sections": {
                "About": "Cross-cutting themes that run through all four divisions of the Shih King: love, governance, ritual, and hardship. These themes show the continuity of human concerns across sacred and secular registers.",
                "For Readers": "Use these thematic groupings to explore how similar human experiences are expressed differently in folk songs, court odes, and temple hymns."
            },
            "keywords": ["themes", "structure"],
            "composite_of": theme_ids,
            "relationship_type": "emergence",
            "metadata": {}
        })

    # Fix sort_orders to be sequential
    for i, item in enumerate(items):
        item['sort_order'] = i + 1

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "James Legge", "date": "1879", "note": "Translator, from Sacred Books of the East, Vol. 3"},
                {"name": "Project Gutenberg", "date": "2005", "note": "Digital text, eBook #9394"}
            ]
        },
        "name": "The Shih King (Book of Poetry)",
        "description": "The Book of Poetry (Shih King/Shi Jing), one of the Five Classics of Confucianism, translated by James Legge. Contains odes from the 11th to 7th centuries BCE, including folk songs, court hymns, and ritual odes. This edition presents the religious and ceremonial selections from Legge's translation in Sacred Books of the East, Vol. 3 (1879).\n\nSource: Project Gutenberg eBook #9394 (https://www.gutenberg.org/ebooks/9394)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Traditional Chinese painting and calligraphy from the Song and Ming dynasties depicting court scenes, ritual ceremonies, and pastoral life would complement these ancient poems.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["chinese-poetry", "confucianism", "ancient-china", "folk-songs", "ritual"],
        "roots": ["eastern-wisdom", "confucianism"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan"],
        "worldview": "dialectical",
        "items": items
    }

    write_grammar(grammar, "grammars/shih-king")
    return grammar


# ═══════════════════════════════════════════════════════════════════════════
# GRAMMAR 2: CHINESE LITERATURE ANTHOLOGY
# ═══════════════════════════════════════════════════════════════════════════

def parse_chinese_literature():
    body = load_body("seeds/chinese-literature-anthology.txt")
    lines = body.split('\n')

    items = []
    sort_order = 0

    # This anthology has 5 major works:
    # 1. The Analects of Confucius (Books I-XX)
    # 2. The Sayings of Mencius (Books I, V)
    # 3. The Shi-King (Books I-XV with selections)
    # 4. The Travels of Fa-Hien (Chapters I-XL)
    # 5. The Sorrows of Han (Prologue + 4 Acts)

    # Find major section starts
    def find_line(pattern, start=0):
        for i in range(start, len(lines)):
            if re.search(pattern, lines[i].strip()):
                return i
        return -1

    # ── ANALECTS OF CONFUCIUS ──
    # Find the actual text start (after the TOC, the second "THE ANALECTS")
    analects_body_start = -1
    count = 0
    for i, line in enumerate(lines):
        if line.strip() == "THE ANALECTS":
            count += 1
            if count == 2:
                analects_body_start = i
                break

    # Find "THE SAYINGS OF MENICUS" or "THE SAYINGS OF MENCIUS" to mark end of Analects
    analects_end = find_line(r'^THE SAYINGS OF MENI?CIUS$', analects_body_start + 1)

    # Parse Analects books
    analects_books = []
    book_pattern = re.compile(r'^BOOK\s+([IVXLC]+)\s*$')
    for i in range(analects_body_start, analects_end):
        m = book_pattern.match(lines[i].strip())
        if m:
            analects_books.append((i, m.group(1)))

    book_titles = {
        "I": "On Learning -- Miscellaneous Sayings",
        "II": "Good Government -- Filial Piety -- The Superior Man",
        "III": "Abuse of Proprieties in Ceremonial and Music",
        "IV": "Social Virtue -- Superior and Inferior Man",
        "V": "A Disciple and the Golden Rule -- Miscellaneous",
        "VI": "More Characteristics -- Wisdom -- Philanthropy",
        "VII": "Characteristics of Confucius -- An Incident",
        "VIII": "Sayings of Tsang -- Sentences of the Master",
        "IX": "His Favorite Disciple's Opinion of Him",
        "X": "Confucius in Private and Official Life",
        "XI": "Comparative Worth of His Disciples",
        "XII": "The Master's Answers -- Philanthropy -- Friendships",
        "XIII": "Answers on the Art of Governing -- Consistency",
        "XIV": "Good and Bad Government -- Miscellaneous Sayings",
        "XV": "Practical Wisdom -- Reciprocity the Rule of Life",
        "XVI": "Against Intestine Strife -- Good and Bad Friendships",
        "XVII": "The Master Induced to Take Office -- Nature and Habit",
        "XVIII": "Good Men in Seclusion -- Duke of Chow to His Son",
        "XIX": "Teachings of Various Chief Disciples",
        "XX": "Extracts from the Book of History",
    }

    for idx, (bline, bnum) in enumerate(analects_books):
        end = analects_books[idx + 1][0] if idx + 1 < len(analects_books) else analects_end
        text_lines_raw = []
        for j in range(bline + 1, end):
            text_lines_raw.append(lines[j].rstrip())

        text = clean_text('\n'.join(text_lines_raw)).strip()
        text = truncate(text)

        title = book_titles.get(bnum, f"Book {bnum}")
        sort_order += 1
        items.append({
            "id": f"analects-book-{bnum.lower()}",
            "name": f"Analects Book {bnum}: {title}",
            "sort_order": sort_order,
            "category": "analects",
            "level": 1,
            "sections": {
                "Text": text if text.strip() else "(Text not available)",
                "Context": f"Book {bnum} of the Analects of Confucius. Translated by William Jennings."
            },
            "keywords": ["confucius", "analects", "philosophy", "wisdom"],
            "metadata": {"work": "The Analects of Confucius", "translator": "William Jennings", "book": bnum}
        })

    # ── SAYINGS OF MENCIUS ──
    mencius_body_start = find_line(r'^THE SAYINGS OF MENCIUS$', analects_end)
    # Find Shi-King start
    shi_king_start = find_line(r'^THE SHI-KING$', mencius_body_start + 1)

    mencius_books = []
    for i in range(mencius_body_start, shi_king_start):
        m = book_pattern.match(lines[i].strip())
        if m:
            mencius_books.append((i, m.group(1)))

    mencius_titles = {
        "I": "King Hwuy of Leang",
        "V": "Wan Chang",
    }

    for idx, (bline, bnum) in enumerate(mencius_books):
        end = mencius_books[idx + 1][0] if idx + 1 < len(mencius_books) else shi_king_start
        text_lines_raw = []
        for j in range(bline + 1, end):
            text_lines_raw.append(lines[j].rstrip())

        text = clean_text('\n'.join(text_lines_raw)).strip()
        text = truncate(text)

        title = mencius_titles.get(bnum, f"Book {bnum}")
        sort_order += 1
        items.append({
            "id": f"mencius-book-{bnum.lower()}",
            "name": f"Mencius Book {bnum}: {title}",
            "sort_order": sort_order,
            "category": "mencius",
            "level": 1,
            "sections": {
                "Text": text if text.strip() else "(Text not available)",
                "Context": f"Book {bnum} of the Sayings of Mencius. Translated by James Legge."
            },
            "keywords": ["mencius", "confucianism", "philosophy", "ethics"],
            "metadata": {"work": "The Sayings of Mencius", "translator": "James Legge", "book": bnum}
        })

    # ── THE SHI-KING (Selections) ──
    # Find where Travels of Fa-Hien starts
    fahien_start = find_line(r'^THE TRAVELS OF F', shi_king_start + 100)

    # Parse Shi-King: find Part markers and individual poems (marked with ~Title~)
    shi_king_items = []
    poem_pattern = re.compile(r'^~(.+?)~\s*$')
    part_pattern = re.compile(r'^PART\s+([IVXLC]+)\.\s*[-—]?\s*(.+?)$', re.IGNORECASE)

    current_part = "Part I"
    current_part_id = "shi-king-part-i"

    for i in range(shi_king_start, fahien_start):
        pm = part_pattern.match(lines[i].strip())
        if pm:
            current_part = f"Part {pm.group(1)}: {pm.group(2).strip()}"
            current_part_id = f"shi-king-part-{pm.group(1).lower()}"

    # Find poems by ~Title~ pattern
    poem_locations = []
    for i in range(shi_king_start, fahien_start):
        pm = poem_pattern.match(lines[i].strip())
        if pm:
            poem_locations.append((i, pm.group(1)))

    # Also find BOOK markers for context
    shi_book_locs = []
    for i in range(shi_king_start, fahien_start):
        m = book_pattern.match(lines[i].strip())
        if m:
            shi_book_locs.append((i, m.group(1)))

    # Find Part markers
    shi_part_locs = []
    for i in range(shi_king_start, fahien_start):
        pm = part_pattern.match(lines[i].strip())
        if pm:
            shi_part_locs.append((i, pm.group(1), pm.group(2).strip()))

    def get_shi_part(ln):
        current = "Part I: Lessons from the States"
        for pl, pnum, pname in shi_part_locs:
            if ln >= pl:
                current = f"Part {pnum}: {pname}"
        return current

    def get_shi_book(ln):
        current = "Unknown"
        for bl, bnum in shi_book_locs:
            if ln >= bl:
                # Get the full book heading
                current = lines[bl].strip()
        return current

    for idx, (pline, ptitle) in enumerate(poem_locations):
        end = poem_locations[idx + 1][0] if idx + 1 < len(poem_locations) else fahien_start
        # Also check for next BOOK
        for bl, _ in shi_book_locs:
            if bl > pline and bl < end:
                end = bl
                break

        text_lines_raw = []
        for j in range(pline + 1, end):
            text_lines_raw.append(lines[j].rstrip())
        text = clean_text('\n'.join(text_lines_raw)).strip()
        text = truncate(text)

        poem_id = f"shi-king-{make_id(ptitle)}"
        # Ensure uniqueness
        existing = [it['id'] for it in items]
        if poem_id in existing:
            suf = 2
            while f"{poem_id}-{suf}" in existing:
                suf += 1
            poem_id = f"{poem_id}-{suf}"

        part_ctx = get_shi_part(pline)
        sort_order += 1
        items.append({
            "id": poem_id,
            "name": ptitle,
            "sort_order": sort_order,
            "category": "shi-king",
            "level": 1,
            "sections": {
                "Verse": text if text.strip() else "(Text not available)",
                "Context": f"From the Shi-King selections: {part_ctx}. Translated by Sir John Francis Davis."
            },
            "keywords": ["poetry", "shi-king", "ancient-china"],
            "metadata": {"work": "The Shi-King", "translator": "Sir John Francis Davis", "part": part_ctx}
        })
        shi_king_items.append(poem_id)

    # ── TRAVELS OF FA-HIEN ──
    # Find where Sorrows of Han starts
    sorrows_start = find_line(r'^THE SORROWS OF HAN$', fahien_start + 100)
    if sorrows_start == -1:
        sorrows_start = find_line(r'~THE SORROWS OF HAN~', fahien_start + 100)

    # Parse chapters
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC]+)\s*$')
    chapter_locations = []
    for i in range(fahien_start, sorrows_start):
        m = chapter_pattern.match(lines[i].strip())
        if m:
            chapter_locations.append((i, m.group(1)))

    # Chapter titles: find ~Title~ after each CHAPTER heading
    for idx, (cline, cnum) in enumerate(chapter_locations):
        end = chapter_locations[idx + 1][0] if idx + 1 < len(chapter_locations) else sorrows_start

        # Find title: ~Title~ pattern
        title = f"Chapter {cnum}"
        for j in range(cline, min(cline + 5, end)):
            tm = poem_pattern.match(lines[j].strip())
            if tm:
                title = tm.group(1)
                break

        text_lines_raw = []
        started = False
        for j in range(cline + 1, end):
            line = lines[j].rstrip()
            if not started:
                # Skip title line and blanks
                if poem_pattern.match(line.strip()) or not line.strip():
                    continue
                started = True
            text_lines_raw.append(line)
        text = clean_text('\n'.join(text_lines_raw)).strip()
        text = truncate(text)

        sort_order += 1
        items.append({
            "id": f"fahien-ch-{cnum.lower()}",
            "name": f"Fa-Hien Ch. {cnum}: {title}",
            "sort_order": sort_order,
            "category": "fahien",
            "level": 1,
            "sections": {
                "Text": text if text.strip() else "(Text not available)",
                "Context": f"Chapter {cnum} of The Travels of Fa-Hien. Translated by James Legge."
            },
            "keywords": ["travel", "buddhism", "pilgrimage", "india"],
            "metadata": {"work": "The Travels of Fa-Hien", "translator": "James Legge", "chapter": cnum}
        })

    # ── SORROWS OF HAN ──
    # Find the end of Gutenberg content
    gut_end_line = len(lines)
    for i in range(sorrows_start, len(lines)):
        if "*** END OF THE PROJECT GUTENBERG" in lines[i]:
            gut_end_line = i
            break

    # Parse acts: Prologue + Acts 1-4
    act_markers = [
        (r'~PROLOGUE~', "prologue", "Prologue"),
        (r'~ACT FIRST~', "act-1", "Act First"),
        (r'~ACT SECOND~', "act-2", "Act Second"),
        (r'~ACT THIRD~', "act-3", "Act Third"),
        (r'~ACT FOURTH~', "act-4", "Act Fourth"),
    ]

    act_locations = []
    for pattern, aid, aname in act_markers:
        for i in range(sorrows_start, gut_end_line):
            if re.search(pattern, lines[i].strip()):
                act_locations.append((i, aid, aname))
                break

    for idx, (aline, aid, aname) in enumerate(act_locations):
        end = act_locations[idx + 1][0] if idx + 1 < len(act_locations) else gut_end_line
        text_lines_raw = []
        for j in range(aline + 1, end):
            text_lines_raw.append(lines[j].rstrip())
        text = clean_text('\n'.join(text_lines_raw)).strip()
        text = truncate(text)

        sort_order += 1
        items.append({
            "id": f"sorrows-{aid}",
            "name": f"The Sorrows of Han: {aname}",
            "sort_order": sort_order,
            "category": "sorrows-of-han",
            "level": 1,
            "sections": {
                "Text": text if text.strip() else "(Text not available)",
                "Context": f"{aname} of The Sorrows of Han (Han Koong Tsew). Translated by Sir John Francis Davis."
            },
            "keywords": ["drama", "tragedy", "han-dynasty", "poetry"],
            "metadata": {"work": "The Sorrows of Han", "translator": "Sir John Francis Davis", "act": aname}
        })

    # ── L2: Group by work ──
    works = [
        ("work-analects", "The Analects of Confucius", "analects",
         "The Analects (Lun Yu) record the sayings and conversations of Confucius (551-479 BCE) as collected by his disciples. These twenty books cover ethics, governance, education, ritual, and the cultivation of virtue. Confucius's practical wisdom -- emphasizing filial piety, benevolence (ren), propriety (li), and the ideal of the Superior Man (junzi) -- has shaped Chinese civilization for over two millennia.",
         ["confucius", "analects", "philosophy"]),
        ("work-mencius", "The Sayings of Mencius", "mencius",
         "Mencius (Meng-tzu, 372-289 BCE) was the most important Confucian thinker after the Master himself. More aggressive and politically engaged than Confucius, he traveled to courts confronting rulers with moral demands. His central doctrine: that human nature is inherently good, and that good governance must nourish the people's moral potential.",
         ["mencius", "confucianism", "philosophy"]),
        ("work-shi-king", "The Shi-King (Selections)", "shi-king",
         "Selections from the Book of Poetry (Shi Jing), one of the Five Classics. These poems from the 11th-7th centuries BCE include folk songs about love, labor, and longing; court odes celebrating governance; and ritual hymns. Sir John Francis Davis's verse translation captures the lyric beauty of these ancient pieces.",
         ["poetry", "shi-king", "ancient-china"]),
        ("work-fahien", "The Travels of Fa-Hien", "fahien",
         "Fa-Hien (337-422 CE) was a Chinese Buddhist monk who undertook an extraordinary pilgrimage to India and Sri Lanka (399-414 CE) to obtain complete copies of the Buddhist Vinaya. His record of Buddhist kingdoms is one of the earliest Chinese travel narratives and an invaluable source for the history of Buddhism in India and Central Asia.",
         ["travel", "buddhism", "pilgrimage"]),
        ("work-sorrows", "The Sorrows of Han", "sorrows-of-han",
         "The Sorrows of Han (Han Koong Tsew, 'Autumn in the Palace of Han') is a Yuan dynasty tragedy by Ma Chih-yuan (c. 1260-1334). It dramatizes the historical story of Wang Chao-chun (Chaoukeun), a court beauty sent to marry the Tartar khan due to the treachery of the corrupt minister Mao Yen-shou. A masterpiece of Chinese dramatic literature.",
         ["drama", "tragedy", "han-dynasty"]),
    ]

    for wid, wname, wcat, wdesc, wkw in works:
        work_items = [it['id'] for it in items if it['category'] == wcat]
        if not work_items:
            continue
        sort_order += 1
        items.append({
            "id": wid,
            "name": wname,
            "sort_order": sort_order,
            "category": "works",
            "level": 2,
            "sections": {
                "About": wdesc,
                "For Readers": f"This work contains {len(work_items)} sections. Each can be read independently, though reading in sequence reveals the full arc of the text."
            },
            "keywords": wkw + ["chinese-literature"],
            "composite_of": work_items,
            "relationship_type": "emergence",
            "metadata": {}
        })

    # ── L2: Thematic groupings across works ──
    theme_groups = [
        ("theme-governance", "The Art of Governance",
         "Passages from across the anthology concerned with rulership, political ethics, and the relationship between the ruler and the ruled. From Confucius's ideal of governing by moral example, through Mencius's bold challenges to kings, to the Shi-King's praise and critique of rulers, these selections reveal a civilization deeply concerned with just governance.",
         lambda it: any(kw in it.get('keywords', []) for kw in ['governance', 'philosophy', 'confucius', 'mencius'])),
        ("theme-spiritual-journey", "Spiritual Journeys",
         "The Buddhist pilgrimage of Fa-Hien and the ritual odes of the Shi-King both represent journeys toward the sacred -- one physical, crossing deserts and mountains to reach India; the other spiritual, ascending through ceremonial music and sacrifice to commune with ancestors and Heaven.",
         lambda it: it.get('category') in ['fahien'] or any(kw in it.get('keywords', []) for kw in ['buddhism', 'pilgrimage', 'sacrifice'])),
        ("theme-human-emotion", "Human Emotion and Drama",
         "The folk songs of the Shi-King and the tragedy of The Sorrows of Han share a common focus on human feeling -- love, longing, loyalty, betrayal, and grief. These works show that Chinese literature, even in its earliest forms, gave powerful voice to personal emotion.",
         lambda it: it.get('category') in ['sorrows-of-han'] or any(kw in it.get('keywords', []) for kw in ['drama', 'poetry'])),
    ]

    for tid, tname, tdesc, matcher in theme_groups:
        matching = [it['id'] for it in items if it['level'] == 1 and matcher(it)]
        if len(matching) < 2:
            continue
        sort_order += 1
        items.append({
            "id": tid,
            "name": tname,
            "sort_order": sort_order,
            "category": "themes",
            "level": 2,
            "sections": {
                "About": tdesc,
                "For Readers": f"This thematic grouping draws together {len(matching)} pieces from across the anthology."
            },
            "keywords": ["theme", "chinese-literature"],
            "composite_of": matching,
            "relationship_type": "emergence",
            "metadata": {}
        })

    # ── L3: Meta-categories ──
    work_ids = [it['id'] for it in items if it['category'] == 'works']
    theme_ids = [it['id'] for it in items if it['category'] == 'themes']

    if work_ids:
        sort_order += 1
        items.append({
            "id": "meta-five-works",
            "name": "The Five Works",
            "sort_order": sort_order,
            "category": "meta",
            "level": 3,
            "sections": {
                "About": "This anthology brings together five foundational works of Chinese literature spanning over a thousand years: the philosophical dialogues of Confucius and Mencius (5th-3rd century BCE), the ancient poetry of the Shi-King (11th-7th century BCE), the Buddhist travel narrative of Fa-Hien (5th century CE), and the dramatic tragedy of The Sorrows of Han (13th century CE). Together they represent the breadth of Chinese literary achievement.",
                "For Readers": "Each work offers a different window into Chinese civilization. Start with the Analects for philosophical wisdom, the Shi-King for lyric beauty, Fa-Hien for adventure, or The Sorrows of Han for dramatic intensity."
            },
            "keywords": ["chinese-literature", "anthology", "structure"],
            "composite_of": work_ids,
            "relationship_type": "emergence",
            "metadata": {}
        })

    if theme_ids:
        sort_order += 1
        items.append({
            "id": "meta-themes",
            "name": "Cross-Work Themes",
            "sort_order": sort_order,
            "category": "meta",
            "level": 3,
            "sections": {
                "About": "Thematic currents that flow through all five works of this anthology, connecting ancient poetry to philosophical dialogue, travel narrative to tragedy. These groupings reveal the deep continuities in Chinese literary and moral imagination.",
                "For Readers": "These themes cut across the five individual works, showing how governance, spiritual seeking, and human emotion appear in very different literary forms."
            },
            "keywords": ["themes", "structure", "chinese-literature"],
            "composite_of": theme_ids,
            "relationship_type": "emergence",
            "metadata": {}
        })

    # Fix sort_orders
    for i, item in enumerate(items):
        item['sort_order'] = i + 1

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Confucius", "date": "5th century BCE", "note": "Author of the Analects"},
                {"name": "Mencius", "date": "3rd century BCE", "note": "Author of the Sayings"},
                {"name": "William Jennings", "date": "1895", "note": "Translator of the Analects"},
                {"name": "James Legge", "date": "1895", "note": "Translator of Mencius and Fa-Hien"},
                {"name": "Sir John Francis Davis", "date": "1829", "note": "Translator of the Shi-King and Sorrows of Han"},
                {"name": "Epiphanius Wilson", "date": "1900", "note": "Editor of the anthology"},
                {"name": "Project Gutenberg", "date": "2003", "note": "Digital text, eBook #10056"}
            ]
        },
        "name": "Chinese Literature Anthology",
        "description": "A comprehensive anthology of Chinese literature compiled by Epiphanius Wilson (1900), comprising five major works spanning over a thousand years: The Analects of Confucius (translated by William Jennings), The Sayings of Mencius (translated by James Legge), The Shi-King/Book of Poetry (translated by Sir John Francis Davis), The Travels of Fa-Hien (translated by James Legge), and The Sorrows of Han (translated by Sir John Francis Davis).\n\nSource: Project Gutenberg eBook #10056 (https://www.gutenberg.org/ebooks/10056)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Chinese scroll paintings, ink wash landscapes, and court scenes from the Ming and Qing dynasties would complement these texts. Illustrations from early 20th century editions of Chinese classics published by Colonial Press (1900) are also relevant.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["chinese-literature", "anthology", "poetry", "prose", "confucianism", "taoism"],
        "roots": ["eastern-wisdom", "confucianism"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan"],
        "worldview": "dialectical",
        "items": items
    }

    write_grammar(grammar, "grammars/chinese-literature-anthology")
    return grammar


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Parsing The Shih King...")
    print("=" * 60)
    g1 = parse_shih_king()

    print()
    print("=" * 60)
    print("Parsing Chinese Literature Anthology...")
    print("=" * 60)
    g2 = parse_chinese_literature()

    print()
    print("Done!")
