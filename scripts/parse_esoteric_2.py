#!/usr/bin/env python3
"""
Parser for three esoteric/alchemy seed texts:
1. The History of Magic by Eliphas Levi (Gutenberg #70033)
2. The Mirror of Alchimy by Roger Bacon et al. (Gutenberg #58393)
3. The Rosicrucian Mysteries by Max Heindel (Gutenberg #29855)

Outputs grammar.json for each into grammars/<name>/
"""

import json
import re
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_body(text):
    """Extract body between Gutenberg START/END markers."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    if start_idx == -1 or end_idx == -1:
        raise ValueError("Could not find Gutenberg markers")
    start_idx = text.index("\n", start_idx) + 1
    return text[start_idx:end_idx].strip()


def truncate_text(text, max_chars=2800):
    """Truncate text at ~2800 chars, at last period."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    bp = text.rfind(".", 0, max_chars)
    if bp == -1:
        bp = max_chars
    remaining_words = len(text[bp+1:].split())
    return text[:bp+1] + f" [Text continues for approximately {remaining_words} more words...]"


def clean_text(text):
    """Clean up formatting artifacts."""
    text = re.sub(r'\[Illustration:.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r"\[Transcriber'?s [Nn]ote:.*?\]", '', text, flags=re.DOTALL)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def make_grammar_commons(attribution):
    return {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": attribution
    }


def make_item(id_, name, sort_order, category, level, sections, keywords, composite_of=None, metadata=None):
    item = {
        "id": id_,
        "name": name,
        "sort_order": sort_order,
        "category": category,
        "level": level,
        "sections": sections,
        "keywords": keywords
    }
    if composite_of:
        item["composite_of"] = composite_of
        item["relationship_type"] = "emergence"
    if metadata:
        item["metadata"] = metadata
    return item


# ============================================================
# HISTORY OF MAGIC PARSER
# ============================================================

def parse_history_of_magic():
    seed_path = os.path.join(REPO, "seeds", "history-of-magic-levi.txt")
    with open(seed_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    body = extract_body(raw)
    lines = body.split('\n')

    # Structure: PREFACE, INTRODUCTION, then BOOK I-VII each with CHAPTER I-VII
    # Headings are centered (lots of leading whitespace), ALL CAPS
    # Book subtitles are in _italics_ on next line

    # Define book structure from the TOC we found
    book_defs = [
        ("I", "The Derivations of Magic", [
            ("I", "Fabulous Sources"),
            ("II", "Magic of the Magi"),
            ("III", "Magic in India"),
            ("IV", "Hermetic Magic"),
            ("V", "Magic in Greece"),
            ("VI", "Mathematical Magic of Pythagoras"),
            ("VII", "The Holy Kabalah"),
        ]),
        ("II", "Magical Realisation in the Ancient World", [
            ("I", "Primitive Symbolism of History"),
            ("II", "Mysticism"),
            ("III", "Initiations and Ordeals"),
            ("IV", "The Magic of Public Worship"),
            ("V", "Mysteries of Virginity"),
            ("VI", "Superstitions"),
            ("VII", "Magical Monuments"),
        ]),
        ("III", "The Divine Synthesis and Realisation of Magia", [
            ("I", "Christ Accused of Magic by the Jews"),
            ("II", "The Witness of Magic to Christianity"),
            ("III", "The Devil"),
            ("IV", "The Last Pagans"),
            ("V", "Legends"),
            ("VI", "Some Kabalistic Paintings and Sacred Emblems"),
            ("VII", "Philosophers of the Alexandrian School"),
        ]),
        ("IV", "Magic and Civilisation", [
            ("I", "Magic Among Barbarians"),
            ("II", "Influence of Women"),
            ("III", "The Salic Laws Against Sorcerers"),
            ("IV", "Legends of the Reign of Charlemagne"),
            ("V", "Magicians"),
            ("VI", "Some Famous Prosecutions"),
            ("VII", "Superstitions Relating to the Devil"),
        ]),
        ("V", "The Adepts and the Priesthood", [
            ("I", "Priests and Popes Accused of Magic"),
            ("II", "Appearance of the Bohemian Nomads"),
            ("III", "Legend and History of Raymund Lully"),
            ("IV", "On Certain Alchemists"),
            ("V", "Some Famous Sorcerers and Magicians"),
            ("VI", "Some Magical Prosecutions"),
            ("VII", "The Magical Origin of Freemasonry"),
        ]),
        ("VI", "Magic in the Eighteenth Century", [
            ("I", "Remarkable Authors of the Eighteenth Century"),
            ("II", "Thaumaturgic Personalities of the Eighteenth Century"),
            ("III", "Prophecies of Cazotte"),
            ("IV", "The French Revolution"),
            ("V", "Phenomena of Mediomania"),
            ("VI", "The German Illuminati"),
            ("VII", "Empire and Restoration"),
        ]),
        ("VII", "Magic in the Nineteenth Century", [
            ("I", "Magnetic Mystics and Materialists"),
            ("II", "Hallucinations"),
            ("III", "Mesmerists and Somnambulists"),
            ("IV", "The Fantastic Side of Magical Literature"),
            ("V", "Some Private Recollections of the Writer"),
            ("VI", "The Occult Sciences"),
            ("VII", "Summary and Conclusion"),
        ]),
    ]

    # Find body start - skip TOC.  The body starts with the second "INTRODUCTION"
    # after the TOC section. We look for the pattern: THE HISTORY OF MAGIC
    # followed by INTRODUCTION after the TOC.
    body_start_line = 0
    found_toc_intro = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "INTRODUCTION" and not found_toc_intro:
            # This is the TOC entry for Introduction
            found_toc_intro = True
            continue
        if stripped == "THE HISTORY OF MAGIC" and found_toc_intro:
            body_start_line = i
            break

    # Find the introduction
    intro_start = None
    for i in range(body_start_line, len(lines)):
        if lines[i].strip() == "INTRODUCTION":
            intro_start = i
            break

    # Find BOOK I start to delimit introduction
    book_starts = []
    for i in range(body_start_line, len(lines)):
        stripped = lines[i].strip()
        m = re.match(r'^BOOK ([IVX]+)$', stripped)
        if m:
            book_starts.append((i, m.group(1)))

    # Also find Preface start (body preface, not the Waite preface at top)
    preface_start = None
    for i in range(body_start_line, len(lines)):
        if lines[i].strip() == "PREFACE TO THE ENGLISH TRANSLATION":
            preface_start = i
            break

    items = []
    sort_order = 1

    # Add Preface if found before Introduction
    if preface_start and intro_start and preface_start < intro_start:
        text = '\n'.join(lines[preface_start + 2:intro_start])
        text = clean_text(text)
        text = truncate_text(text)
        items.append(make_item(
            id_="preface", name="Preface to the English Translation",
            sort_order=sort_order, category="preface", level=1,
            sections={"Text": text},
            keywords=["preface", "waite", "eliphas-levi"]
        ))
        sort_order += 1

    # Add Introduction
    if intro_start:
        # Find where intro ends (at BOOK I)
        intro_end = book_starts[0][0] if book_starts else intro_start + 500
        text = '\n'.join(lines[intro_start + 2:intro_end])
        text = clean_text(text)
        text = truncate_text(text)
        items.append(make_item(
            id_="introduction", name="Introduction",
            sort_order=sort_order, category="introduction", level=1,
            sections={"Text": text},
            keywords=["introduction", "magic", "definition"]
        ))
        sort_order += 1

    # Parse each book's chapters
    l1_ids_by_book = {}
    book_roman_to_idx = {bs[1]: idx for idx, bs in enumerate(book_starts)}

    for book_idx, (book_roman, book_title, chapters_def) in enumerate(book_defs):
        book_line = None
        for bs_line, bs_roman in book_starts:
            if bs_roman == book_roman:
                book_line = bs_line
                break

        if book_line is None:
            print(f"  Warning: Could not find BOOK {book_roman}")
            continue

        # Next book start
        next_book_line = len(lines)
        for bs_line, bs_roman in book_starts:
            if bs_line > book_line:
                next_book_line = bs_line
                break

        # Find chapters within this book's range
        book_lines = lines[book_line:next_book_line]
        chapter_positions = []  # (line_offset, chapter_roman, chapter_name)

        for ch_roman, ch_name in chapters_def:
            # Look for centered "CHAPTER I" etc.
            heading = f"CHAPTER {ch_roman}"
            for j, bline in enumerate(book_lines):
                if bline.strip() == heading:
                    chapter_positions.append((j, ch_roman, ch_name))
                    break

        l1_ids_by_book[book_roman] = []

        for ch_idx, (ch_offset, ch_roman, ch_name) in enumerate(chapter_positions):
            # Find end of chapter
            if ch_idx + 1 < len(chapter_positions):
                ch_end = chapter_positions[ch_idx + 1][0]
            else:
                ch_end = len(book_lines)

            # Skip heading lines (CHAPTER X, then title in ALL CAPS)
            content_start = ch_offset + 1
            for j in range(ch_offset + 1, min(ch_offset + 10, ch_end)):
                stripped = book_lines[j].strip()
                if not stripped:
                    content_start = j + 1
                elif stripped == stripped.upper() and len(stripped) > 2:
                    content_start = j + 1
                else:
                    content_start = j
                    break

            text = '\n'.join(book_lines[content_start:ch_end])
            text = clean_text(text)
            text = truncate_text(text)

            book_num = ["I", "II", "III", "IV", "V", "VI", "VII"].index(book_roman) + 1
            ch_num = ["I", "II", "III", "IV", "V", "VI", "VII"].index(ch_roman) + 1
            item_id = f"book-{book_num}-chapter-{ch_num}"

            items.append(make_item(
                id_=item_id,
                name=f"Book {book_roman}, Ch. {ch_roman}: {ch_name}",
                sort_order=sort_order,
                category=f"book-{book_num}",
                level=1,
                sections={"Text": text},
                keywords=["magic", "history", ch_name.lower().replace(" ", "-")]
            ))
            l1_ids_by_book[book_roman].append(item_id)
            sort_order += 1

    # L2: One per book
    l2_ids = []
    for book_roman, book_title, _ in book_defs:
        book_num = ["I", "II", "III", "IV", "V", "VI", "VII"].index(book_roman) + 1
        l2_id = f"book-{book_num}"
        refs = l1_ids_by_book.get(book_roman, [])
        if not refs:
            continue

        items.append(make_item(
            id_=l2_id,
            name=f"Book {book_roman}: {book_title}",
            sort_order=sort_order,
            category="book",
            level=2,
            sections={
                "About": f"Book {book_roman} of The History of Magic: {book_title}. Eliphas Levi traces the history and practice of magic through seven books, each containing seven chapters corresponding to the seven planets of classical astrology.",
                "For Readers": f"Read the chapters of Book {book_roman} in sequence to follow Levi's argument about {book_title.lower()}."
            },
            keywords=["magic", "history", book_title.lower().replace(" ", "-")],
            composite_of=refs
        ))
        l2_ids.append(l2_id)
        sort_order += 1

    # L3: Meta-categories
    early_books = [lid for lid in l2_ids if lid in ["book-1", "book-2", "book-3"]]
    later_books = [lid for lid in l2_ids if lid in ["book-4", "book-5", "book-6", "book-7"]]

    items.append(make_item(
        id_="ancient-magic", name="Ancient Magic: Origins to Early Christianity",
        sort_order=sort_order, category="meta", level=3,
        sections={
            "About": "The first three books trace magic from its mythological origins through the ancient civilizations — the Magi, India, Egypt, Greece, Pythagoras, the Kabalah — through the rise of Christianity and the last pagans. Levi argues that true magic is the science of the ancient magi, not vulgar sorcery.",
            "How to Use": "Read these books to understand Levi's thesis: that magic is the ancient and universal science of Nature, preserved through the Kabalah and Hermeticism, confirmed rather than destroyed by Christianity."
        },
        keywords=["ancient-magic", "origins", "kabbalah", "hermeticism"],
        composite_of=early_books
    ))
    sort_order += 1

    items.append(make_item(
        id_="medieval-modern-magic", name="Medieval to Modern Magic",
        sort_order=sort_order, category="meta", level=3,
        sections={
            "About": "Books IV through VII trace magic from the barbarian invasions through the medieval period (Charlemagne, the alchemists, Raymund Lully, Freemasonry) to the eighteenth-century occultists and finally Levi's own nineteenth-century experiences with mesmerism, somnambulism, and the occult sciences.",
            "How to Use": "Follow the thread from medieval sorcery and alchemy through the Enlightenment to Levi's own era. Note how magic transforms from a persecuted art to an intellectual tradition, and how Levi positions himself as its modern interpreter."
        },
        keywords=["medieval-magic", "alchemy", "freemasonry", "modern-magic"],
        composite_of=later_books
    ))
    sort_order += 1

    grammar = {
        "_grammar_commons": make_grammar_commons([
            {"name": "Eliphas Levi (Alphonse Louis Constant)", "date": "1860", "note": "Original author"},
            {"name": "Arthur Edward Waite", "date": "1922", "note": "English translator"},
            {"name": "Project Gutenberg", "date": "2023", "note": "eBook #70033"}
        ]),
        "name": "The History of Magic",
        "description": "The History of Magic by Eliphas Levi (1860), translated by Arthur Edward Waite (1922) — a comprehensive survey of magic from its mythological origins through ancient civilizations, medieval alchemy and sorcery, to the occultism of the eighteenth and nineteenth centuries. Levi presents magic as the science of the ancient magi, tracing its thread through the Kabalah, Hermeticism, and the Western esoteric tradition.\n\nSource: Project Gutenberg eBook #70033 (https://www.gutenberg.org/ebooks/70033)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: The original 1922 Rider edition includes numerous illustrations. Additional relevant imagery: the Baphomet drawing by Eliphas Levi, engravings from Levi's Dogme et Rituel de la Haute Magie (1856), Kabalistic diagrams from the Sepher Yetzirah tradition, and portraits of Levi from the 19th century.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["magic", "occultism", "history", "kabbalah", "hermeticism", "eliphas-levi"],
        "roots": ["mysticism", "western-esotericism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }

    out_dir = os.path.join(REPO, "grammars", "history-of-magic-levi")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "grammar.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"History of Magic: {len(items)} items written to {out_path}")
    return grammar


# ============================================================
# MIRROR OF ALCHIMY PARSER
# ============================================================

def parse_mirror_of_alchimy():
    seed_path = os.path.join(REPO, "seeds", "mirror-of-alchimy.txt")
    with open(seed_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    body = extract_body(raw)
    lines = body.split('\n')

    # Structure: Multiple treatises bound together
    # 1. Mirror of Alchimy (Roger Bacon) - CHAP. I-VII
    # 2. Smaragdine Table of Hermes (short, standalone)
    # 3. Commentary of Hortulanus on the Smaragdine Table - CHAP. I-XIII
    # 4. Secrets of Alchimie (Calid) - CHAP. I-XVI
    # 5. Discourse on Art and Nature (Roger Bacon) - no chapters

    # Define treatise boundaries by finding key markers
    treatise_markers = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if "The Mirrour of Alchimy" in stripped or "The Mirrour of Alchimy" in line:
            treatise_markers.append(("mirror_title", i))
        if "The Smaragdine Table of Hermes" in stripped:
            treatise_markers.append(("smaragdine", i))
        if "briefe Commentarie of Hortulanus" in stripped or "briefe Commentarie of Hortulanus" in line:
            treatise_markers.append(("hortulanus_title", i))
        if "Booke of the Secrets of Alchimie" in stripped or "Booke of the Secrets of Alchimie" in line:
            treatise_markers.append(("calid_title", i))
        if "admirable force and efficacie of Art and" in stripped or "admirable force and efficacie of Art" in line:
            treatise_markers.append(("art_nature_title", i))
        if "Here endeth the Mirror of Alchimy" in stripped:
            treatise_markers.append(("mirror_end", i))
        if "Here endeth the Table of Hermes" in stripped:
            treatise_markers.append(("smaragdine_end", i))
        if "endeth the Commentarie of" in stripped and "Hortulanus" in stripped:
            treatise_markers.append(("hortulanus_end", i))
        if "Here endeth the secrets Alchimy" in stripped:
            treatise_markers.append(("calid_end", i))
        if stripped == "FINIS.":
            treatise_markers.append(("finis", i))

    marker_dict = {}
    for label, line_num in treatise_markers:
        if label not in marker_dict:
            marker_dict[label] = line_num

    items = []
    sort_order = 1

    # Helper: find all CHAP. X headings in a range
    def find_chapters_in_range(start, end):
        """Find CHAP. lines in range, return list of (line_idx, chap_label)"""
        results = []
        for i in range(start, end):
            stripped = lines[i].strip()
            m = re.match(r'CHAP\.\s+([IVXL]+)\.$', stripped)
            if m:
                results.append((i, m.group(1)))
        return results

    # Helper: get subtitle (italic line after chapter heading)
    def get_subtitle(line_idx):
        """Look for _italic subtitle_ in lines after chapter heading."""
        for j in range(line_idx + 1, min(line_idx + 5, len(lines))):
            stripped = lines[j].strip()
            if stripped.startswith('_') and stripped.endswith('_'):
                return stripped.strip('_').strip('.')
            if stripped and not stripped.startswith('_'):
                break
        return ""

    # ---- 1. MIRROR OF ALCHIMY (Roger Bacon) ----
    mirror_start = marker_dict.get("mirror_title", 0)
    mirror_end = marker_dict.get("mirror_end", marker_dict.get("smaragdine", len(lines)))
    mirror_chapters = find_chapters_in_range(mirror_start, mirror_end)

    mirror_names = [
        "Of the Definitions of Alchimy",
        "Of the Natural Principles and Procreation of Minerals",
        "Out of What Things the Elixir Must Be Made",
        "Of the Quality of the Vessel and Furnace",
        "Of the Accidental and Essential Colours in the Work",
        "Of the Quality of the Vessel and Furnace",
        "How to Make Projection of the Medicine",
    ]

    # Also add the Preface
    preface_line = None
    for i in range(0, mirror_start + 30):
        if lines[i].strip() == "The Preface.":
            preface_line = i
            break

    if preface_line is not None:
        first_ch = mirror_chapters[0][0] if mirror_chapters else mirror_end
        text = '\n'.join(lines[preface_line + 2:first_ch])
        text = clean_text(text)
        text = truncate_text(text)
        items.append(make_item(
            id_="mirror-preface", name="The Mirror of Alchimy: Preface",
            sort_order=sort_order, category="mirror-of-alchimy", level=1,
            sections={"Text": text},
            keywords=["roger-bacon", "alchemy", "preface"]
        ))
        sort_order += 1

    mirror_l1_ids = []
    if preface_line is not None:
        mirror_l1_ids.append("mirror-preface")

    for ch_idx, (ch_line, ch_roman) in enumerate(mirror_chapters):
        subtitle = get_subtitle(ch_line)
        ch_num = ch_idx + 1
        if ch_idx < len(mirror_names):
            name = mirror_names[ch_idx]
        elif subtitle:
            name = subtitle
        else:
            name = f"Chapter {ch_roman}"

        # Find end
        if ch_idx + 1 < len(mirror_chapters):
            ch_end = mirror_chapters[ch_idx + 1][0]
        else:
            ch_end = mirror_end

        # Skip heading + subtitle
        content_start = ch_line + 1
        for j in range(ch_line + 1, min(ch_line + 8, ch_end)):
            stripped = lines[j].strip()
            if not stripped or stripped.startswith('_'):
                content_start = j + 1
            else:
                content_start = j
                break

        text = '\n'.join(lines[content_start:ch_end])
        text = clean_text(text)
        text = truncate_text(text)

        item_id = f"mirror-ch-{ch_num}"
        items.append(make_item(
            id_=item_id,
            name=f"Mirror Ch. {ch_roman}: {name}",
            sort_order=sort_order,
            category="mirror-of-alchimy",
            level=1,
            sections={"Text": text},
            keywords=["roger-bacon", "alchemy", "transmutation"]
        ))
        mirror_l1_ids.append(item_id)
        sort_order += 1

    # ---- 2. SMARAGDINE TABLE ----
    smaragdine_start = marker_dict.get("smaragdine", None)
    smaragdine_end = marker_dict.get("smaragdine_end", None)
    if smaragdine_start and smaragdine_end:
        # The text is between the title and the "endeth" marker
        content_start = smaragdine_start
        for j in range(smaragdine_start, min(smaragdine_start + 8, smaragdine_end)):
            stripped = lines[j].strip()
            if not stripped or "Smaragdine Table" in stripped or "Trismegistus" in stripped:
                content_start = j + 1
            else:
                content_start = j
                break

        text = '\n'.join(lines[content_start:smaragdine_end])
        text = clean_text(text)
        text = truncate_text(text)

        items.append(make_item(
            id_="smaragdine-table", name="The Smaragdine Table of Hermes Trismegistus",
            sort_order=sort_order, category="hermetic", level=1,
            sections={"Text": text},
            keywords=["hermes-trismegistus", "emerald-tablet", "alchemy", "hermetic"]
        ))
        sort_order += 1

    # ---- 3. HORTULANUS COMMENTARY ----
    hortulanus_start = marker_dict.get("hortulanus_title", None)
    hortulanus_end = marker_dict.get("hortulanus_end", None)
    calid_start = marker_dict.get("calid_title", None)
    if not hortulanus_end and calid_start:
        hortulanus_end = calid_start

    hortulanus_l1_ids = []
    if hortulanus_start and hortulanus_end:
        hort_chapters = find_chapters_in_range(hortulanus_start, hortulanus_end)

        for ch_idx, (ch_line, ch_roman) in enumerate(hort_chapters):
            subtitle = get_subtitle(ch_line)
            ch_num = ch_idx + 1
            name = subtitle if subtitle else f"Chapter {ch_roman}"

            if ch_idx + 1 < len(hort_chapters):
                ch_end = hort_chapters[ch_idx + 1][0]
            else:
                ch_end = hortulanus_end

            content_start = ch_line + 1
            for j in range(ch_line + 1, min(ch_line + 8, ch_end)):
                stripped = lines[j].strip()
                if not stripped or stripped.startswith('_'):
                    content_start = j + 1
                else:
                    content_start = j
                    break

            text = '\n'.join(lines[content_start:ch_end])
            text = clean_text(text)
            text = truncate_text(text)

            item_id = f"hortulanus-ch-{ch_num}"
            items.append(make_item(
                id_=item_id,
                name=f"Hortulanus Ch. {ch_roman}: {name}",
                sort_order=sort_order,
                category="hortulanus-commentary",
                level=1,
                sections={"Text": text},
                keywords=["hortulanus", "emerald-tablet", "commentary", "alchemy"]
            ))
            hortulanus_l1_ids.append(item_id)
            sort_order += 1

    # ---- 4. SECRETS OF ALCHIMIE (Calid) ----
    calid_end = marker_dict.get("calid_end", None)
    art_nature_start = marker_dict.get("art_nature_title", None)
    if not calid_end and art_nature_start:
        calid_end = art_nature_start

    calid_l1_ids = []
    if calid_start and calid_end:
        calid_chapters = find_chapters_in_range(calid_start, calid_end)

        for ch_idx, (ch_line, ch_roman) in enumerate(calid_chapters):
            subtitle = get_subtitle(ch_line)
            ch_num = ch_idx + 1
            name = subtitle if subtitle else f"Chapter {ch_roman}"

            if ch_idx + 1 < len(calid_chapters):
                ch_end = calid_chapters[ch_idx + 1][0]
            else:
                ch_end = calid_end

            content_start = ch_line + 1
            for j in range(ch_line + 1, min(ch_line + 8, ch_end)):
                stripped = lines[j].strip()
                if not stripped or stripped.startswith('_'):
                    content_start = j + 1
                else:
                    content_start = j
                    break

            text = '\n'.join(lines[content_start:ch_end])
            text = clean_text(text)
            text = truncate_text(text)

            item_id = f"calid-ch-{ch_num}"
            items.append(make_item(
                id_=item_id,
                name=f"Calid Ch. {ch_roman}: {name}",
                sort_order=sort_order,
                category="secrets-of-alchimie",
                level=1,
                sections={"Text": text},
                keywords=["calid", "alchemy", "secrets"]
            ))
            calid_l1_ids.append(item_id)
            sort_order += 1

    # ---- 5. DISCOURSE ON ART AND NATURE (Roger Bacon) ----
    if art_nature_start:
        finis_line = marker_dict.get("finis", len(lines))
        # Content starts after the title block
        content_start = art_nature_start
        for j in range(art_nature_start, min(art_nature_start + 15, finis_line)):
            stripped = lines[j].strip()
            if not stripped or "admirable force" in stripped or "Roger Bacon" in stripped or "Oxford" in stripped or stripped.startswith("_") or "fellow of" in stripped or "Brasen-nose" in stripped:
                content_start = j + 1
            else:
                content_start = j
                break

        text = '\n'.join(lines[content_start:finis_line])
        text = clean_text(text)
        text = truncate_text(text)

        items.append(make_item(
            id_="art-and-nature", name="Of the Admirable Force and Efficacy of Art and Nature",
            sort_order=sort_order, category="art-and-nature", level=1,
            sections={"Text": text},
            keywords=["roger-bacon", "art", "nature", "philosophy"]
        ))
        sort_order += 1

    # ---- L2: THEMATIC GROUPS ----
    l2_groups = [
        ("mirror-treatise", "The Mirror of Alchimy (Roger Bacon)", "mirror-of-alchimy",
         mirror_l1_ids,
         "Roger Bacon's Mirror of Alchimy in seven chapters, covering the definitions of alchemy, the natural principles and procreation of minerals, the preparation of the Elixir, and the art of projection. A concise, practical guide to the transmutation of metals.",
         ["roger-bacon", "alchemy", "transmutation", "elixir"]),
        ("hermetic-emerald", "The Emerald Tablet and Its Commentary", "hermetic",
         ["smaragdine-table"] + hortulanus_l1_ids,
         "The legendary Smaragdine (Emerald) Table of Hermes Trismegistus — one of the most famous alchemical texts in history — together with the detailed commentary of Hortulanus the Philosopher, who explains each cryptic sentence in terms of practical alchemical operations.",
         ["hermes", "emerald-tablet", "hortulanus", "hermetic"]),
        ("calid-secrets", "The Secrets of Alchimie (Calid)", "secrets-of-alchimie",
         calid_l1_ids,
         "The Book of the Secrets of Alchimie by Calid, translated from Hebrew into Arabic and thence into Latin and English. A systematic treatise covering the four masteries (solution, congelation, albification, rubification), the elements and instruments of the work, and the making of the white and red stones.",
         ["calid", "alchemy", "secrets", "transmutation"]),
    ]

    l2_ids = []
    for id_, name, cat, refs, about, kw in l2_groups:
        if not refs:
            continue
        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category=cat, level=2,
            sections={
                "About": about,
                "For Readers": "Read these chapters in sequence to follow the alchemical argument from principles through practice."
            },
            keywords=kw,
            composite_of=refs
        ))
        l2_ids.append(id_)
        sort_order += 1

    # L3: Meta
    all_l2 = l2_ids + (["art-and-nature"] if art_nature_start else [])
    items.append(make_item(
        id_="mirror-complete", name="The Mirror of Alchimy — Complete Collection",
        sort_order=sort_order, category="meta", level=3,
        sections={
            "About": "A collection of five alchemical treatises bound together in the 1597 London edition: Roger Bacon's Mirror of Alchimy, the Smaragdine Table of Hermes Trismegistus, Hortulanus's Commentary on the Emerald Tablet, Calid's Secrets of Alchimie, and Bacon's Discourse on the Force of Art and Nature. Together they represent the core texts of medieval Western alchemy.",
            "How to Use": "Begin with the Mirror of Alchimy for Bacon's systematic introduction to alchemical principles. Then read the Emerald Tablet — the foundational text of Hermetic alchemy — with Hortulanus's commentary. Follow with Calid's practical Secrets, and conclude with Bacon's philosophical discourse on Art and Nature."
        },
        keywords=["alchemy", "roger-bacon", "hermes", "calid", "medieval", "meta"],
        composite_of=all_l2
    ))

    grammar = {
        "_grammar_commons": make_grammar_commons([
            {"name": "Roger Bacon", "date": "c. 1267", "note": "Attributed author of the Mirror and Art & Nature treatises"},
            {"name": "Hermes Trismegistus", "date": "ancient", "note": "Attributed author of the Smaragdine Table"},
            {"name": "Hortulanus", "date": "c. 14th century", "note": "Commentator on the Emerald Tablet"},
            {"name": "Calid (son of Jazich)", "date": "c. 8th century", "note": "Author of the Secrets of Alchimie"},
            {"name": "Project Gutenberg", "date": "2018", "note": "eBook #58393"}
        ]),
        "name": "The Mirror of Alchimy",
        "description": "The Mirror of Alchimy (1597 London edition) — a collection of five alchemical treatises: Roger Bacon's Mirror of Alchimy on the transmutation of metals, the Smaragdine (Emerald) Table of Hermes Trismegistus, Hortulanus's Commentary on the Emerald Tablet, Calid's Book of the Secrets of Alchimie, and Bacon's Discourse on the Admirable Force and Efficacy of Art and Nature.\n\nSource: Project Gutenberg eBook #58393 (https://www.gutenberg.org/ebooks/58393)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Woodcuts from 16th-century alchemical editions, engravings from the Musaeum Hermeticum (1678), illustrations from Michael Maier's Atalanta Fugiens (1618), and the printer's device from the 1597 Richard Olive edition.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["alchemy", "transmutation", "roger-bacon", "esoteric", "medieval"],
        "roots": ["mysticism", "western-esotericism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }

    out_dir = os.path.join(REPO, "grammars", "mirror-of-alchimy")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "grammar.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"Mirror of Alchimy: {len(items)} items written to {out_path}")
    return grammar


# ============================================================
# ROSICRUCIAN MYSTERIES PARSER
# ============================================================

def parse_rosicrucian_mysteries():
    seed_path = os.path.join(REPO, "seeds", "rosicrucian-mysteries.txt")
    with open(seed_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    body = extract_body(raw)
    lines = body.split('\n')

    # Structure: 5 chapters + Mt. Ecclesia appendix + Index
    # Headings: "CHAPTER I. THE ORDER OF ROSICRUCIANS..."
    chapter_defs = [
        ("CHAPTER I.", "chapter-1", "The Order of Rosicrucians and the Rosicrucian Fellowship",
         "order-and-fellowship", ["rosicrucian", "fellowship", "order"]),
        ("CHAPTER II.", "chapter-2", "The Problem of Life and Its Solution",
         "problem-of-life", ["life", "death", "problem", "solution"]),
        ("CHAPTER III.", "chapter-3", "The Visible and the Invisible World",
         "visible-invisible", ["visible", "invisible", "worlds", "planes"]),
        ("CHAPTER IV.", "chapter-4", "The Constitution of Man",
         "constitution-of-man", ["man", "constitution", "bodies", "spirit"]),
        ("CHAPTER V.", "chapter-5", "Life and Death",
         "life-and-death", ["life", "death", "afterlife", "rebirth"]),
    ]

    # Find chapter positions
    chapter_starts = []
    for heading, id_, name, cat, kw in chapter_defs:
        for i, line in enumerate(lines):
            if line.strip().startswith(heading):
                chapter_starts.append((i, id_, name, cat, kw))
                break

    # Find Mt. Ecclesia section
    mt_ecclesia_start = None
    index_start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "Mt. Ecclesia" or stripped == "MT. ECCLESIA":
            # Check it's the section, not just a mention
            if i > 100:  # Skip TOC mention
                mt_ecclesia_start = i
                break
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "Index" or stripped == "INDEX":
            if i > 100:
                index_start = i
                break

    items = []
    sort_order = 1
    l1_ids = []

    for ch_idx, (start_line, id_, name, cat, kw) in enumerate(chapter_starts):
        # End of chapter
        if ch_idx + 1 < len(chapter_starts):
            end_line = chapter_starts[ch_idx + 1][0]
        elif mt_ecclesia_start:
            end_line = mt_ecclesia_start
        elif index_start:
            end_line = index_start
        else:
            end_line = len(lines)

        # Skip heading line(s)
        content_start = start_line + 1
        for j in range(start_line + 1, min(start_line + 10, end_line)):
            stripped = lines[j].strip()
            if not stripped:
                content_start = j + 1
            else:
                content_start = j
                break

        text = '\n'.join(lines[content_start:end_line])
        text = clean_text(text)
        text = truncate_text(text)

        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category=cat, level=1,
            sections={"Teaching": text},
            keywords=["rosicrucian", "max-heindel"] + kw
        ))
        l1_ids.append(id_)
        sort_order += 1

    # Mt. Ecclesia appendix
    if mt_ecclesia_start:
        end_line = index_start if index_start else len(lines)
        content_start = mt_ecclesia_start + 2
        text = '\n'.join(lines[content_start:end_line])
        text = clean_text(text)
        text = truncate_text(text)

        items.append(make_item(
            id_="mt-ecclesia", name="Mt. Ecclesia",
            sort_order=sort_order, category="appendix", level=1,
            sections={"Text": text},
            keywords=["rosicrucian", "mt-ecclesia", "fellowship", "oceanside"]
        ))
        l1_ids.append("mt-ecclesia")
        sort_order += 1

    # L2: Thematic groups
    l2_groups = [
        ("rosicrucian-foundations", "Rosicrucian Foundations", "foundations",
         ["chapter-1", "chapter-2"],
         "The opening chapters introduce the Rosicrucian Order and Fellowship, their history and mission, and the fundamental problem of life that their teachings address — the mystery of death and the meaning of existence.",
         ["rosicrucian", "foundations", "order"]),
        ("invisible-worlds-and-man", "The Invisible Worlds and the Constitution of Man", "cosmology",
         ["chapter-3", "chapter-4"],
         "Heindel's cosmology: the visible and invisible worlds (Chemical, Etheric, Desire, and Thought regions) and the complex constitution of man as a being of multiple bodies — dense, vital, desire, and mental — animated by a threefold spirit.",
         ["cosmology", "invisible-worlds", "constitution", "bodies"]),
        ("life-death-rebirth", "Life, Death, and Rebirth", "eschatology",
         ["chapter-5"] + (["mt-ecclesia"] if mt_ecclesia_start else []),
         "The final chapter addresses the mysteries of life after death — the panorama of life, purgatory, the heaven worlds, and rebirth — revealing the Rosicrucian understanding of the soul's journey. The appendix on Mt. Ecclesia describes the physical home of the Rosicrucian Fellowship.",
         ["life", "death", "rebirth", "afterlife"]),
    ]

    l2_ids = []
    for id_, name, cat, refs, about, kw in l2_groups:
        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category=cat, level=2,
            sections={
                "About": about,
                "For Readers": "Read these chapters together to build a progressive understanding of the Rosicrucian worldview, from its institutional origins through its metaphysical cosmology to its vision of the afterlife."
            },
            keywords=kw,
            composite_of=refs
        ))
        l2_ids.append(id_)
        sort_order += 1

    # L3: Meta
    items.append(make_item(
        id_="rosicrucian-complete", name="The Rosicrucian Mysteries — Complete",
        sort_order=sort_order, category="meta", level=3,
        sections={
            "About": "Max Heindel's elementary exposition of the secret teachings of the Rosicrucian Order. The book presents a complete metaphysical system: the visible and invisible worlds, the complex constitution of man, the mysteries of life and death, and the soul's journey through purgatory and the heaven worlds toward rebirth. Written as an accessible introduction to the Western Mystery tradition.",
            "How to Use": "Begin with the Foundations to understand the Order and the fundamental problem of life. Then explore the Invisible Worlds and Constitution of Man to grasp the cosmological framework. Finally, study Life, Death, and Rebirth to understand the Rosicrucian vision of the soul's journey."
        },
        keywords=["rosicrucian", "max-heindel", "esoteric", "cosmology", "meta"],
        composite_of=l2_ids
    ))

    grammar = {
        "_grammar_commons": make_grammar_commons([
            {"name": "Max Heindel", "date": "1911", "note": "Author, Third Edition"},
            {"name": "Project Gutenberg", "date": "2009", "note": "eBook #29855"}
        ]),
        "name": "The Rosicrucian Mysteries",
        "description": "The Rosicrucian Mysteries: An Elementary Exposition of Their Secret Teachings by Max Heindel (1911, Third Edition) — an introduction to the Rosicrucian Order's metaphysical teachings covering the invisible worlds, the constitution of man, and the mysteries of life, death, and rebirth.\n\nSource: Project Gutenberg eBook #29855 (https://www.gutenberg.org/ebooks/29855)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Rosicrucian emblems from the Fama Fraternitatis (1614) and Confessio Fraternitatis (1615), engravings from Robert Fludd's Utriusque Cosmi Historia (1617-1621), and the Rose Cross symbol from various 17th-century Rosicrucian publications.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["rosicrucian", "esoteric", "mysticism", "spiritual-development", "occultism"],
        "roots": ["mysticism", "western-esotericism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }

    out_dir = os.path.join(REPO, "grammars", "rosicrucian-mysteries")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "grammar.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"Rosicrucian Mysteries: {len(items)} items written to {out_path}")
    return grammar


if __name__ == "__main__":
    print("Parsing esoteric/alchemy seed texts (batch 2)...")
    print()
    parse_history_of_magic()
    print()
    parse_mirror_of_alchimy()
    print()
    parse_rosicrucian_mysteries()
    print()
    print("Done!")
