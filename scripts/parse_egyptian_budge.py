#!/usr/bin/env python3
"""
Parse three E.A. Wallis Budge Egyptian texts into grammars:
1. Book of the Dead (Gutenberg #7145)
2. Legends of the Gods (Gutenberg #9411)
3. Egyptian Ideas of the Future Life (Gutenberg #11277)
"""
import json, re, os

def read_gutenberg(path):
    """Read a Gutenberg text and return body between START/END markers."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    start = text.find("\n", start) + 1
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    return text[start:end].strip()

def truncate(text, limit=2800):
    """Truncate text at ~2800 chars, finding last period before cutoff."""
    if len(text) <= limit:
        return text
    bp = text.rfind(".", 0, limit - 100)
    if bp == -1:
        bp = limit - 100
    remaining = len(text[bp:].split())
    return text[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"

def strip_footnotes(text):
    """Remove [FN#N] and [N] footnote markers and footnote blocks."""
    # Remove inline footnote markers
    text = re.sub(r'\[FN#\d+\]', '', text)
    text = re.sub(r'\[Footnote:[^\]]*\]', '', text)
    text = re.sub(r'\[\d+\]', '', text)
    # Remove footnote blocks (lines starting with [FN#)
    lines = text.split('\n')
    cleaned = []
    in_footnote = False
    for line in lines:
        if re.match(r'^\s*\[FN#', line):
            in_footnote = True
            continue
        if in_footnote:
            if line.strip() == '' or (not line.startswith(' ') and not line.startswith('\t')):
                in_footnote = False
                if line.strip() == '':
                    continue
            else:
                continue
        # Also skip footnote text blocks
        if re.match(r'^\s*\[Footnote:', line):
            in_footnote = True
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)

def clean_text(text):
    """Clean extracted text: strip footnotes, normalize whitespace."""
    text = strip_footnotes(text)
    # Remove #### image placeholders
    text = re.sub(r'####', '', text)
    # Normalize multiple blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()

def make_grammar(name, description, tags, items, gutenberg_id, gutenberg_title):
    """Build the full grammar JSON structure."""
    return {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "E.A. Wallis Budge",
                    "date": "1904",
                    "note": f"Source: Project Gutenberg eBook #{gutenberg_id} (https://www.gutenberg.org/ebooks/{gutenberg_id})"
                }
            ]
        },
        "name": name,
        "description": description,
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": tags,
        "roots": ["eastern-wisdom", "mysticism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }


# ═══════════════════════════════════════════════════════════════════════════
# GRAMMAR 1: BOOK OF THE DEAD
# ═══════════════════════════════════════════════════════════════════════════

def parse_book_of_dead():
    body = read_gutenberg("seeds/book-of-the-dead-egyptian.txt")
    lines = body.split("\n")

    # Chapter definitions: (heading_pattern, id, name)
    chapters = [
        ("CHAPTER I", "chapter-1", "The Title", "The origins and naming of the Book of the Dead"),
        ("CHAPTER II", "chapter-2", "The Preservation of the Mummified Body", "Mummification, Thoth's protection, and the defense against evil"),
        ("CHAPTER III", "chapter-3", "The Book Per-t em Hru", "The 'Chapters of Coming Forth by Day' and their versions"),
        ("CHAPTER IV", "chapter-4", "Thoth, the Author of the Book of the Dead", "Thoth as divine author and the role of magical words"),
        ("CHAPTER V", "chapter-5", "Thoth and Osiris", "The relationship between Thoth and Osiris in funerary tradition"),
        ("CHAPTER VI", "chapter-6", "Osiris as Judge of the Dead", "Osiris as sovereign of the Underworld and judge of souls"),
        ("CHAPTER VII", "chapter-7", "The Judgment of Osiris", "The Weighing of the Heart and the 42 Negative Confessions"),
        ("CHAPTER VIII", "chapter-8", "The Kingdom of Osiris", "The Sekhet-Aaru (Elysian Fields) and the blessed afterlife"),
        ("CHAPTER IX", "chapter-9", "The Doors of the Book of the Dead", "A description of the principal chapters and their purposes"),
    ]

    # Find chapter positions
    chapter_positions = []
    for heading, cid, cname, cdesc in chapters:
        for i, line in enumerate(lines):
            if line.strip() == heading:
                chapter_positions.append((i, cid, cname, cdesc))
                break

    items = []
    sort_order = 1

    for idx, (start_ln, cid, cname, cdesc) in enumerate(chapter_positions):
        # Find end of chapter
        if idx + 1 < len(chapter_positions):
            end_ln = chapter_positions[idx + 1][0]
        else:
            end_ln = len(lines)

        # Extract text: skip heading, blank lines, subtitle, then find first paragraph
        content_lines = []
        started = False
        found_first_blank_after_subtitle = False
        in_subtitle = False
        for j in range(start_ln + 1, end_ln):
            line = lines[j]
            stripped = line.strip()
            if not started:
                # Skip blank lines at the top
                if stripped == '':
                    if in_subtitle:
                        found_first_blank_after_subtitle = True
                        in_subtitle = False
                    continue
                # The first non-blank line after heading is the subtitle
                if not found_first_blank_after_subtitle:
                    in_subtitle = True
                    continue
                # After subtitle + blank, we're at the body text
                started = True
            content_lines.append(line.rstrip())

        # Remove trailing blanks
        while content_lines and content_lines[-1].strip() == '':
            content_lines.pop()

        text = clean_text('\n'.join(content_lines))
        text = truncate(text)

        items.append({
            "id": cid,
            "name": cname,
            "sort_order": sort_order,
            "category": "chapters",
            "level": 1,
            "sections": {
                "Text": text,
                "About": cdesc
            },
            "keywords": ["egypt", "book-of-the-dead", "funerary"],
            "metadata": {}
        })
        sort_order += 1

    # L2: Thematic groupings
    l2_groups = [
        {
            "id": "theme-origins",
            "name": "Origins and Authorship",
            "category": "themes",
            "composite_of": ["chapter-1", "chapter-3", "chapter-4"],
            "about": "The origins, naming, and divine authorship of the Book of the Dead. These chapters trace the text from its modern title through its ancient Egyptian name 'Per-t em Hru' (Coming Forth by Day) to its attributed author, the god Thoth.",
            "keywords": ["origins", "thoth", "authorship", "history"]
        },
        {
            "id": "theme-preservation",
            "name": "Mummification and Protection",
            "category": "themes",
            "composite_of": ["chapter-2", "chapter-5"],
            "about": "The preservation of the body and the divine partnership of Thoth and Osiris in protecting the dead. Mummification was not merely physical preservation but a magical act, sustained by the words of power that Thoth provided.",
            "keywords": ["mummification", "protection", "thoth", "osiris"]
        },
        {
            "id": "theme-judgment",
            "name": "Judgment and the Afterlife",
            "category": "themes",
            "composite_of": ["chapter-6", "chapter-7", "chapter-8", "chapter-9"],
            "about": "The judgment of the dead before Osiris and the blessed afterlife that awaits those who pass. The Weighing of the Heart, the 42 Negative Confessions, and the paradise of the Sekhet-Aaru (Field of Reeds) form the climactic sequence of the Egyptian funerary journey.",
            "keywords": ["judgment", "afterlife", "osiris", "sekhet-aaru"]
        },
    ]

    for g in l2_groups:
        items.append({
            "id": g["id"],
            "name": g["name"],
            "sort_order": sort_order,
            "category": g["category"],
            "level": 2,
            "composite_of": g["composite_of"],
            "relationship_type": "emergence",
            "sections": {
                "About": g["about"]
            },
            "keywords": g["keywords"],
            "metadata": {}
        })
        sort_order += 1

    # L3: Meta
    items.append({
        "id": "meta-book-of-dead",
        "name": "The Egyptian Book of the Dead",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": ["theme-origins", "theme-preservation", "theme-judgment"],
        "relationship_type": "emergence",
        "sections": {
            "About": "E.A. Wallis Budge's introduction to the Book of the Dead -- the great collection of funerary texts that the ancient Egyptians called 'Per-t em Hru,' the Chapters of Coming Forth by Day. These nine chapters trace the origin and purpose of the spells, the role of Thoth as their divine author, the judgment of the dead before Osiris, and the paradise that awaited the justified soul in the Sekhet-Aaru (Field of Reeds). Together they form a complete guide to the Egyptian understanding of death, judgment, and immortality."
        },
        "keywords": ["egypt", "book-of-the-dead", "overview"],
        "metadata": {}
    })

    desc = ("E.A. Wallis Budge's introduction to the Egyptian Book of the Dead, the great funerary text known "
            "to the ancient Egyptians as 'Per-t em Hru' (Coming Forth by Day). This work explains the origins, "
            "authorship, and contents of the spells, hymns, and magical formulae that guided the dead through "
            "the Underworld to the judgment hall of Osiris and beyond to the blessed fields of the afterlife. "
            "Source: Project Gutenberg eBook #7145 (https://www.gutenberg.org/ebooks/7145)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: The Papyrus of Ani (British Museum), illustrated with "
            "scenes of the Weighing of the Heart, the Fields of the Blessed, and the gods of the Underworld. "
            "Also: the Book of the Dead papyri reproductions by Edouard Naville (1886) and Karl Richard Lepsius "
            "(1842), both featuring hieroglyphic vignettes in the traditional Egyptian style.")

    grammar = make_grammar(
        "The Book of the Dead",
        desc,
        ["egypt", "death", "afterlife", "ritual", "ancient-religion"],
        items,
        7145,
        "The Book of the Dead"
    )
    grammar["_grammar_commons"]["attribution"][0]["date"] = "1901"

    os.makedirs("grammars/book-of-the-dead-egyptian", exist_ok=True)
    with open("grammars/book-of-the-dead-egyptian/grammar.json", "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"Book of the Dead: {len(items)} items written")
    return items


# ═══════════════════════════════════════════════════════════════════════════
# GRAMMAR 2: LEGENDS OF THE GODS
# ═══════════════════════════════════════════════════════════════════════════

def parse_legends_of_gods():
    body = read_gutenberg("seeds/legends-of-gods-egyptian.txt")
    lines = body.split("\n")

    # The book has two main parts:
    # INTRODUCTION sections I-IX (scholarly introductions to each legend)
    # Then the actual TRANSLATED TEXTS of the legends
    #
    # We'll extract the Introduction sections and the legend texts separately.

    # Introduction sections (I-IX) with their titles
    intro_sections = [
        ("I.", "THE LEGEND OF THE GOD NEB-ER-TCHER, AND THE HISTORY OF CREATION.", "intro-creation", "The Legend of Creation"),
        ("II.", "THE LEGEND OF THE DESTRUCTION OF MANKIND.", "intro-destruction", "The Legend of the Destruction of Mankind"),
        ("III.", "THE LEGEND OF RA AND ISIS.", "intro-ra-isis", "The Legend of Ra and Isis"),
        ("IV.", "THE LEGEND OF HERU-BEHUTET AND THE WINGED DISK.", "intro-horus-winged-disk", "The Legend of Horus and the Winged Disk"),
        ("V.", "LEGEND OF THE BIRTH OF HORUS, SON OF ISIS AND OSIRIS.", "intro-birth-horus", "The Legend of the Birth of Horus"),
        ("VI.", "A LEGEND OF KHENSU NEFER-HETEP", "intro-khensu", "The Legend of Khensu and the Princess of Bekhten"),
        ("VII.", "A LEGEND OF KHNEMU AND OF A SEVEN YEARS' FAMINE.", "intro-khnemu", "The Legend of Khnemu and the Seven Years' Famine"),
        ("VIII.", "THE LEGEND OF THE DEATH AND RESURRECTION OF HORUS", "intro-death-horus", "The Legend of the Death and Resurrection of Horus"),
        ("IX.", "THE HISTORY OF ISIS AND OSIRIS.", "intro-isis-osiris", "The History of Isis and Osiris (Plutarch)"),
    ]

    # Find the INTRODUCTION marker
    intro_start = None
    for i, line in enumerate(lines):
        if line.strip() == "INTRODUCTION":
            intro_start = i
            break

    # Find each intro section by looking for Roman numeral at start of line
    # followed by the title on the next non-blank line
    intro_positions = []
    for sec_num, sec_title, sec_id, sec_name in intro_sections:
        for i in range(intro_start if intro_start else 0, len(lines)):
            stripped = lines[i].strip()
            if stripped == sec_num:
                intro_positions.append((i, sec_id, sec_name, sec_title))
                break

    # The translated legend texts start after the introduction
    # Find them by their ALL-CAPS titles
    legend_texts = [
        ("THE LEGEND OF THE DESTRUCTION OF MANKIND.", "text-destruction", "The Destruction of Mankind (Translation)"),
        ("THE LEGEND OF RA AND ISIS.", "text-ra-isis", "Ra and Isis (Translation)"),
        ("THE LEGEND OF HORUS OF BEHUTET AND THE WINGED DISK.", "text-horus-winged-disk", "Horus of Behutet and the Winged Disk (Translation)"),
        ("THE LEGEND OF THE DEATH OF HORUS THROUGH THE STING OF A SCORPION", "text-death-horus", "The Death and Resurrection of Horus (Translation)"),
    ]

    # Find the Plutarch section (ISIS AND OSIRIS ACCORDING TO PLUTARCH)
    # This has numbered sections I-XLVIII+

    items = []
    sort_order = 1

    # Extract Introduction sections
    for idx, (start_ln, sec_id, sec_name, sec_title) in enumerate(intro_positions):
        if idx + 1 < len(intro_positions):
            end_ln = intro_positions[idx + 1][0]
        else:
            # Find the start of the legend texts (the first translated text heading)
            end_ln = len(lines)
            for i in range(start_ln + 10, len(lines)):
                if lines[i].strip() == "THE LEGEND OF THE DESTRUCTION OF MANKIND." and i > 2000:
                    end_ln = i
                    break

        content_lines = []
        started = False
        for j in range(start_ln + 1, end_ln):
            line = lines[j]
            if not started:
                # Skip the title line(s) and blank lines before text
                stripped = line.strip()
                if stripped == '' or stripped == sec_title.rstrip('.') or stripped == sec_title:
                    continue
                if stripped.startswith("THE LEGEND") or stripped.startswith("LEGEND") or stripped.startswith("A LEGEND") or stripped.startswith("THE HISTORY"):
                    continue
                started = True
            content_lines.append(line.rstrip())

        while content_lines and content_lines[-1].strip() == '':
            content_lines.pop()

        text = clean_text('\n'.join(content_lines))
        text = truncate(text)

        items.append({
            "id": sec_id,
            "name": sec_name,
            "sort_order": sort_order,
            "category": "introduction",
            "level": 1,
            "sections": {
                "Introduction": text,
                "About": f"Budge's scholarly introduction to {sec_name.lower()}, discussing the sources, context, and significance of the ancient Egyptian text."
            },
            "keywords": ["egypt", "mythology", "introduction"],
            "metadata": {}
        })
        sort_order += 1

    # Now extract the actual legend translation texts
    # These are the texts after the Introduction section

    # Find the first translated text: "THE LEGEND OF THE DESTRUCTION OF MANKIND" (the one after line 2300)
    # Find where the Introduction ends (after section IX)
    intro_end_line = 0
    for i, line in enumerate(lines):
        if line.strip() == "IX.":
            if i > 1500:  # Make sure it's the intro section IX, not a sub-number
                intro_end_line = i
                break
    # The translated texts start after all intro sections
    # Find the first translated legend title after the introduction
    texts_start = intro_end_line + 100  # Some margin past intro IX

    legend_text_defs = [
        {
            "title": "THE LEGEND OF THE DESTRUCTION OF MANKIND.",
            "id": "text-destruction",
            "name": "The Destruction of Mankind (Translation)",
            "keywords": ["ra", "hathor", "sekhmet", "destruction", "humanity"]
        },
        {
            "title": "THE LEGEND OF RA AND ISIS.",
            "id": "text-ra-isis",
            "name": "Ra and Isis (Translation)",
            "keywords": ["ra", "isis", "secret-name", "magic", "serpent"]
        },
        {
            "title": "THE LEGEND OF HORUS OF BEHUTET AND THE WINGED DISK.",
            "id": "text-horus-winged-disk",
            "name": "Horus of Behutet and the Winged Disk (Translation)",
            "keywords": ["horus", "winged-disk", "battle", "set", "enemies"]
        },
        {
            "title": "THE LEGEND OF THE DEATH OF HORUS THROUGH THE STING OF A SCORPION",
            "id": "text-death-horus",
            "name": "The Death and Resurrection of Horus (Translation)",
            "keywords": ["horus", "scorpion", "isis", "thoth", "resurrection"]
        },
    ]

    # Find positions of legend texts -- only look AFTER the intro ends
    legend_positions = []
    for ldef in legend_text_defs:
        for i in range(texts_start, len(lines)):
            if lines[i].strip().startswith(ldef["title"].rstrip('.')):
                legend_positions.append((i, ldef))
                break

    # Also find the Plutarch section - look for section title after the legend texts
    plutarch_start = None
    # Plutarch's text starts with "I.  Though it be the wise man"
    for i in range(texts_start, len(lines)):
        if "I.  Though it be the wise man" in lines[i]:
            # Back up to find the section title
            for j in range(i - 30, i):
                if "ISIS AND OSIRIS" in lines[j] and "PLUTARCH" in lines[j]:
                    plutarch_start = j
                    break
            if plutarch_start is None:
                # Look for any ISIS AND OSIRIS heading nearby
                for j in range(i - 50, i):
                    if "ISIS AND OSIRIS" in lines[j]:
                        plutarch_start = j
                        break
            if plutarch_start is None:
                plutarch_start = i - 5
            break

    for idx, (start_ln, ldef) in enumerate(legend_positions):
        # Find end
        if idx + 1 < len(legend_positions):
            end_ln = legend_positions[idx + 1][0]
        elif plutarch_start:
            end_ln = plutarch_start
        else:
            end_ln = len(lines)

        content_lines = []
        started = False
        for j in range(start_ln + 1, end_ln):
            line = lines[j]
            stripped = line.strip()
            if not started:
                if stripped == '' or stripped.startswith("THE LEGEND") or stripped.startswith("AND HIS RESURRECTION") or stripped.startswith("HIS RESURRECTION"):
                    continue
                started = True
            # Skip running headers (repeated legend title before each sub-chapter)
            if stripped.startswith("THE LEGEND OF THE DESTRUCTION") or stripped.startswith("THE LEGEND OF HORUS OF BEHUTET") or stripped.startswith("THE LEGEND OF THE DEATH OF HORUS"):
                if stripped == ldef["title"] or stripped == ldef["title"].rstrip('.'):
                    continue
            content_lines.append(line.rstrip())

        while content_lines and content_lines[-1].strip() == '':
            content_lines.pop()

        text = clean_text('\n'.join(content_lines))
        text = truncate(text)

        items.append({
            "id": ldef["id"],
            "name": ldef["name"],
            "sort_order": sort_order,
            "category": "legend-texts",
            "level": 1,
            "sections": {
                "Text": text,
                "About": f"The translated text of {ldef['name'].replace(' (Translation)', '')} from the ancient Egyptian original."
            },
            "keywords": ldef["keywords"],
            "metadata": {}
        })
        sort_order += 1

    # Plutarch's Isis and Osiris
    if plutarch_start:
        end_ln = len(lines)
        # Find the Gutenberg end
        for i in range(plutarch_start, len(lines)):
            if "*** END" in lines[i]:
                end_ln = i
                break

        # Find the actual start of Plutarch's text (section I.)
        plut_text_start = plutarch_start
        for i in range(plutarch_start, end_ln):
            if lines[i].strip().startswith("I.  Though it be"):
                plut_text_start = i
                break

        # Find section title
        plut_title_start = plutarch_start
        for i in range(plutarch_start, plut_text_start):
            stripped = lines[i].strip()
            if "ISIS AND OSIRIS" in stripped:
                plut_title_start = i
                break

        content_lines = []
        for j in range(plut_text_start, end_ln):
            content_lines.append(lines[j].rstrip())

        while content_lines and content_lines[-1].strip() == '':
            content_lines.pop()

        text = clean_text('\n'.join(content_lines))
        text = truncate(text)

        items.append({
            "id": "text-isis-osiris-plutarch",
            "name": "Isis and Osiris According to Plutarch (Translation)",
            "sort_order": sort_order,
            "category": "legend-texts",
            "level": 1,
            "sections": {
                "Text": text,
                "About": "Plutarch's De Iside et Osiride, the most complete classical account of the Isis and Osiris myth, as translated and annotated by Budge."
            },
            "keywords": ["isis", "osiris", "plutarch", "classical"],
            "metadata": {}
        })
        sort_order += 1

    # L2: Thematic groupings
    l2_groups = [
        {
            "id": "theme-creation-cosmos",
            "name": "Creation and Cosmic Order",
            "composite_of": ["intro-creation", "intro-destruction", "text-destruction"],
            "about": "The creation of the world by the self-begotten god Neb-er-tcher (Khepera) and the near-destruction of humanity when Ra grew old and humans rebelled. These legends establish the cosmic order: the world emerged from the primordial waters of Nu through the power of divine speech, and humanity exists only because Ra relented from total annihilation.",
            "keywords": ["creation", "destruction", "neb-er-tcher", "ra", "cosmic-order"]
        },
        {
            "id": "theme-divine-power",
            "name": "Divine Knowledge and Magic",
            "composite_of": ["intro-ra-isis", "text-ra-isis", "intro-khensu", "intro-khnemu"],
            "about": "The secret names of the gods and the magical power of divine knowledge. Isis tricks Ra into revealing his secret name, gaining supreme magical authority. Khensu heals the Princess of Bekhten through his divine presence. Khnemu controls the Nile's flood. These legends reveal how the Egyptians understood divine power as operating through knowledge, names, and ritual.",
            "keywords": ["isis", "ra", "magic", "secret-name", "divine-power"]
        },
        {
            "id": "theme-horus-battles",
            "name": "The Wars of Horus",
            "composite_of": ["intro-horus-winged-disk", "intro-birth-horus", "text-horus-winged-disk", "intro-death-horus", "text-death-horus"],
            "about": "The cycle of Horus -- his miraculous birth to Isis and the dead Osiris, his death by scorpion sting and resurrection through Thoth, and his great battles against Set and the enemies of Ra. The Winged Disk legend is the most martial Egyptian myth, depicting Horus as the champion of cosmic order against chaos.",
            "keywords": ["horus", "set", "battle", "birth", "resurrection"]
        },
        {
            "id": "theme-isis-osiris",
            "name": "The Isis and Osiris Cycle",
            "composite_of": ["intro-isis-osiris", "text-isis-osiris-plutarch"],
            "about": "The central myth of Egyptian religion: Osiris the good king is murdered and dismembered by his brother Set; Isis searches the world for his body, reassembles it, and conceives Horus; Osiris becomes lord of the afterlife. Plutarch's De Iside et Osiride provides the most complete version of this story, here presented alongside Budge's introduction.",
            "keywords": ["isis", "osiris", "set", "death", "resurrection", "plutarch"]
        },
    ]

    for g in l2_groups:
        items.append({
            "id": g["id"],
            "name": g["name"],
            "sort_order": sort_order,
            "category": "themes",
            "level": 2,
            "composite_of": g["composite_of"],
            "relationship_type": "emergence",
            "sections": {
                "About": g["about"]
            },
            "keywords": g["keywords"],
            "metadata": {}
        })
        sort_order += 1

    # L3: Meta
    items.append({
        "id": "meta-legends-gods",
        "name": "Legends of the Egyptian Gods",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": ["theme-creation-cosmos", "theme-divine-power", "theme-horus-battles", "theme-isis-osiris"],
        "relationship_type": "emergence",
        "sections": {
            "About": "E.A. Wallis Budge's collection of the foundational myths of ancient Egypt: the creation of the world from the primordial waters, Ra's near-destruction of humanity, Isis's theft of Ra's secret name, the birth, death, and resurrection of Horus, and the great myth of Isis and Osiris as told by Plutarch. These legends span from the earliest Egyptian religious texts to classical Greek retellings, forming a complete portrait of Egyptian mythological thought."
        },
        "keywords": ["egypt", "mythology", "gods", "overview"],
        "metadata": {}
    })

    desc = ("E.A. Wallis Budge's collection of the major legends of the Egyptian gods, with translations from the "
            "original hieroglyphic and hieratic texts. Includes the Legend of Creation, the Destruction of Mankind, "
            "Ra and Isis, Horus and the Winged Disk, the Birth and Death of Horus, the legends of Khensu and Khnemu, "
            "and Plutarch's complete narrative of Isis and Osiris. "
            "Source: Project Gutenberg eBook #9411 (https://www.gutenberg.org/ebooks/9411)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: The plates from the original 1912 edition by Budge, including "
            "Horus spearing the Hippopotamus-fiend, the Procreation of Horus, the Resurrection of Osiris, and the "
            "Bekhten and Metternich Steles. Also: reliefs from the Temple of Edfu depicting the Horus myths.")

    grammar = make_grammar(
        "Legends of the Gods",
        desc,
        ["egypt", "mythology", "gods", "osiris", "isis", "creation-myth"],
        items,
        9411,
        "Legends of the Gods"
    )
    grammar["_grammar_commons"]["attribution"][0]["date"] = "1912"

    os.makedirs("grammars/legends-of-gods-egyptian", exist_ok=True)
    with open("grammars/legends-of-gods-egyptian/grammar.json", "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"Legends of the Gods: {len(items)} items written")
    return items


# ═══════════════════════════════════════════════════════════════════════════
# GRAMMAR 3: EGYPTIAN IDEAS OF THE FUTURE LIFE
# ═══════════════════════════════════════════════════════════════════════════

def parse_egyptian_ideas():
    body = read_gutenberg("seeds/egyptian-ideas-future-life.txt")
    lines = body.split("\n")

    chapters = [
        ("CHAPTER I.", "THE BELIEF IN GOD ALMIGHTY.", "chapter-1", "The Belief in God Almighty",
         "The Egyptian concept of the One God (Neter) -- self-existent, immortal, invisible, eternal, and almighty"),
        ("CHAPTER II.", "OSIRIS THE GOD OF THE RESURRECTION.", "chapter-2", "Osiris the God of the Resurrection",
         "The myth of Osiris, his death and resurrection, and his role as king of the underworld"),
        ("CHAPTER III.", "THE \"GODS\" OF THE EGYPTIANS.", "chapter-3", "The 'Gods' of the Egyptians",
         "The nature of the Egyptian pantheon: how monotheism and polytheism coexisted in Egyptian thought"),
        ("CHAPTER IV.", "THE JUDGMENT OF THE DEAD.", "chapter-4", "The Judgment of the Dead",
         "The Weighing of the Heart, the Hall of Maati, and the 42 Assessors of the Dead"),
        ("CHAPTER V.", "THE RESURRECTION AND IMMORTALITY.", "chapter-5", "The Resurrection and Immortality",
         "The Egyptian doctrines of bodily resurrection, the ka, the ba, the khu, and eternal life"),
    ]

    # Find chapter positions by matching "CHAPTER N." at start of line
    chapter_positions = []
    for ch_heading, ch_title, ch_id, ch_name, ch_desc in chapters:
        for i, line in enumerate(lines):
            if line.strip() == ch_heading:
                # Verify next non-blank line has the title
                chapter_positions.append((i, ch_id, ch_name, ch_desc))
                break

    items = []
    sort_order = 1

    for idx, (start_ln, ch_id, ch_name, ch_desc) in enumerate(chapter_positions):
        if idx + 1 < len(chapter_positions):
            end_ln = chapter_positions[idx + 1][0]
        else:
            end_ln = len(lines)
            # Find end marker
            for i in range(start_ln, len(lines)):
                if "*** END" in lines[i]:
                    end_ln = i
                    break

        # Skip the heading, title, and initial blanks
        content_lines = []
        started = False
        past_title = False
        for j in range(start_ln + 1, end_ln):
            line = lines[j]
            stripped = line.strip()
            if not past_title:
                if stripped == '' or stripped.startswith("THE ") or stripped.startswith("OSIRIS") or stripped == chapters[idx][1]:
                    continue
                past_title = True
            if not started and stripped == '':
                continue
            started = True
            content_lines.append(line.rstrip())

        while content_lines and content_lines[-1].strip() == '':
            content_lines.pop()

        text = clean_text('\n'.join(content_lines))
        text = truncate(text)

        items.append({
            "id": ch_id,
            "name": ch_name,
            "sort_order": sort_order,
            "category": "chapters",
            "level": 1,
            "sections": {
                "Text": text,
                "About": ch_desc
            },
            "keywords": ["egypt", "afterlife", "theology"],
            "metadata": {}
        })
        sort_order += 1

    # L2: Thematic groupings
    l2_groups = [
        {
            "id": "theme-theology",
            "name": "Egyptian Theology",
            "composite_of": ["chapter-1", "chapter-3"],
            "about": "The theological foundations of Egyptian religion: the belief in one supreme, self-existent God (Neter) alongside the multiplicity of divine forms. Budge argues that the Egyptians held a sophisticated monotheism beneath their apparent polytheism -- the many gods were aspects or manifestations of the One.",
            "keywords": ["theology", "monotheism", "polytheism", "neter"]
        },
        {
            "id": "theme-osiris-judgment",
            "name": "Osiris and the Judgment",
            "composite_of": ["chapter-2", "chapter-4"],
            "about": "The myth of Osiris as the foundation of Egyptian afterlife beliefs, and the great scene of judgment in the Hall of Maati (Truth). Osiris conquered death and thereby guaranteed resurrection to all who followed him; but first the dead must pass the Weighing of the Heart against the feather of Maat.",
            "keywords": ["osiris", "judgment", "maati", "weighing-of-heart"]
        },
        {
            "id": "theme-immortality",
            "name": "The Doctrine of Immortality",
            "composite_of": ["chapter-2", "chapter-5"],
            "about": "The Egyptian understanding of resurrection, the multiple souls (ka, ba, khu, sekhem), and the mechanics of eternal life. The dead were not merely spirits -- they required a preserved body, sustenance in the tomb, and magical texts to navigate the afterlife and achieve union with Osiris.",
            "keywords": ["resurrection", "immortality", "ka", "ba", "khu", "soul"]
        },
    ]

    for g in l2_groups:
        items.append({
            "id": g["id"],
            "name": g["name"],
            "sort_order": sort_order,
            "category": "themes",
            "level": 2,
            "composite_of": g["composite_of"],
            "relationship_type": "emergence",
            "sections": {
                "About": g["about"]
            },
            "keywords": g["keywords"],
            "metadata": {}
        })
        sort_order += 1

    # L3: Meta
    items.append({
        "id": "meta-egyptian-ideas",
        "name": "Egyptian Ideas of the Future Life",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": ["theme-theology", "theme-osiris-judgment", "theme-immortality"],
        "relationship_type": "emergence",
        "sections": {
            "About": "E.A. Wallis Budge's comprehensive account of ancient Egyptian beliefs about God, the gods, death, judgment, and the afterlife. From the sublime monotheism underlying Egyptian polytheism, through the Osiris myth and the Weighing of the Heart, to the doctrines of the ka, ba, and khu -- this work reveals how the Egyptians understood the journey from death to eternal life in the kingdom of Osiris."
        },
        "keywords": ["egypt", "afterlife", "theology", "overview"],
        "metadata": {}
    })

    desc = ("E.A. Wallis Budge's account of the principal ideas and beliefs held by the ancient Egyptians "
            "concerning God, the resurrection, and the future life. Covers the belief in one supreme God (Neter), "
            "the myth of Osiris, the nature of the Egyptian pantheon, the Judgment of the Dead in the Hall of Maati, "
            "and the doctrines of resurrection, the ka, the ba, and immortality. "
            "Source: Project Gutenberg eBook #11277 (https://www.gutenberg.org/ebooks/11277)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: The eight illustrations from the original 1899/1908 edition "
            "by Budge, including The Creation, Isis Suckling Horus, the Judgment Scene from the Papyrus of Ani, "
            "and the Sekhet-Aaru (Elysian Fields) from the papyri of Nebseni, Ani, and Anilai.")

    grammar = make_grammar(
        "Egyptian Ideas of the Future Life",
        desc,
        ["egypt", "afterlife", "soul", "judgment", "ancient-religion"],
        items,
        11277,
        "Egyptian Ideas of the Future Life"
    )
    grammar["_grammar_commons"]["attribution"][0]["date"] = "1899"

    os.makedirs("grammars/egyptian-ideas-future-life", exist_ok=True)
    with open("grammars/egyptian-ideas-future-life/grammar.json", "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"Egyptian Ideas of the Future Life: {len(items)} items written")
    return items


# ═══════════════════════════════════════════════════════════════════════════
# RUN ALL THREE
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Parsing Egyptian Budge texts...")
    print("=" * 60)
    parse_book_of_dead()
    print()
    parse_legends_of_gods()
    print()
    parse_egyptian_ideas()
    print()
    print("Done! All three grammars written.")
