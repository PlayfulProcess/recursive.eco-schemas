#!/usr/bin/env python3
"""
Parser for Swedenborg's "Heaven and its Wonders and Hell"
Source: Project Gutenberg eBook #17368
Translator: John C. Ager

Structure: 63 chapters (Roman numeral headings), each containing numbered sections.
The text divides into three major parts:
  - Heaven (Chapters I-XLIII, sections 2-420)
  - World of Spirits (Chapters XLIV-LV, sections 421-535)
  - Hell (Chapters LVI-LXIII, sections 536-603)
"""

import json
import re
import os

SEED_FILE = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'swedenborg-heaven-hell.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'swedenborg-heaven-hell')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'grammar.json')

# Chapter definitions: (roman, section_num, title, part)
# part: "heaven", "world-of-spirits", "hell"
CHAPTERS = [
    ("I", 2, "The God of Heaven is the Lord", "heaven"),
    ("II", 7, "It is the Divine of the Lord that Makes Heaven", "heaven"),
    ("III", 13, "In Heaven the Divine of the Lord is Love to Him and Charity Towards the Neighbor", "heaven"),
    ("IV", 20, "Heaven is Divided into Two Kingdoms", "heaven"),
    ("V", 29, "There are Three Heavens", "heaven"),
    ("VI", 41, "The Heavens Consist of Innumerable Societies", "heaven"),
    ("VII", 51, "Each Society is a Heaven in a Smaller Form, and Each Angel in the Smallest Form", "heaven"),
    ("VIII", 59, "All Heaven in the Aggregate Reflects a Single Man", "heaven"),
    ("IX", 68, "Each Society in Heaven Reflects a Single Man", "heaven"),
    ("X", 73, "Therefore Every Angel is in a Complete Human Form", "heaven"),
    ("XI", 78, "It is from the Lord's Divine Human that Heaven as a Whole and in Part Reflects Man", "heaven"),
    ("XII", 87, "There is a Correspondence of All Things of Heaven with All Things of Man", "heaven"),
    ("XIII", 103, "There is a Correspondence of Heaven with All Things of the Earth", "heaven"),
    ("XIV", 116, "The Sun in Heaven", "heaven"),
    ("XV", 126, "Light and Heat in Heaven", "heaven"),
    ("XVI", 141, "The Four Quarters in Heaven", "heaven"),
    ("XVII", 154, "Changes of State of the Angels in Heaven", "heaven"),
    ("XVIII", 162, "Time in Heaven", "heaven"),
    ("XIX", 170, "Representatives and Appearances in Heaven", "heaven"),
    ("XX", 177, "The Garments with which Angels Appear Clothed", "heaven"),
    ("XXI", 183, "The Places of Abode and Dwellings of Angels", "heaven"),
    ("XXII", 191, "Space in Heaven", "heaven"),
    ("XXIII", 200, "The Form of Heaven which Determines Affiliations and Communications There", "heaven"),
    ("XXIV", 213, "Governments in Heaven", "heaven"),
    ("XXV", 221, "Divine Worship in Heaven", "heaven"),
    ("XXVI", 228, "The Power of the Angels of Heaven", "heaven"),
    ("XXVII", 234, "The Speech of Angels", "heaven"),
    ("XXVIII", 246, "The Speech of Angels with Man", "heaven"),
    ("XXIX", 258, "Writings in Heaven", "heaven"),
    ("XXX", 265, "The Wisdom of the Angels of Heaven", "heaven"),
    ("XXXI", 276, "The State of Innocence of Angels in Heaven", "heaven"),
    ("XXXII", 284, "The State of Peace in Heaven", "heaven"),
    ("XXXIII", 291, "The Conjunction of Heaven with the Human Race", "heaven"),
    ("XXXIV", 303, "Conjunction of Heaven with Man by Means of the Word", "heaven"),
    ("XXXV", 311, "Heaven and Hell are from the Human Race", "heaven"),
    ("XXXVI", 318, "The Heathen, or Peoples Outside of the Church, in Heaven", "heaven"),
    ("XXXVII", 329, "Little Children in Heaven", "heaven"),
    ("XXXVIII", 346, "The Wise and the Simple in Heaven", "heaven"),
    ("XXXIX", 357, "The Rich and the Poor in Heaven", "heaven"),
    ("XL", 366, "Marriages in Heaven", "heaven"),
    ("XLI", 387, "The Employments of Angels in Heaven", "heaven"),
    ("XLII", 395, "Heavenly Joy and Happiness", "heaven"),
    ("XLIII", 415, "The Immensity of Heaven", "heaven"),
    ("XLIV", 421, "What the World of Spirits Is", "world-of-spirits"),
    ("XLV", 432, "In Respect to His Interiors Every Man is a Spirit", "world-of-spirits"),
    ("XLVI", 445, "The Resuscitation of Man from the Dead and His Entrance into Eternal Life", "world-of-spirits"),
    ("XLVII", 453, "Man After Death is in a Complete Human Form", "world-of-spirits"),
    ("XLVIII", 461, "After Death Man is Possessed of Every Sense, and of All the Memory, Thought, and Affection, that He Had in the World, Leaving Nothing Behind Except His Earthly Body", "world-of-spirits"),
    ("XLIX", 470, "Man After Death is Such as His Life Had Been in the World", "world-of-spirits"),
    ("L", 485, "The Delights of Every One's Life are Changed After Death into Things that Correspond", "world-of-spirits"),
    ("LI", 491, "The First State of Man After Death", "world-of-spirits"),
    ("LII", 499, "The Second State of Man After Death", "world-of-spirits"),
    ("LIII", 512, "Third State of Man After Death, which is a State of Instruction for Those Who Enter Heaven", "world-of-spirits"),
    ("LIV", 521, "No One Enters Heaven by Mercy Apart from Means", "world-of-spirits"),
    ("LV", 528, "It is Not So Difficult to Live the Life that Leads to Heaven as is Believed", "world-of-spirits"),
    ("LVI", 536, "The Lord Rules the Hells", "hell"),
    ("LVII", 545, "The Lord Casts No One into Hell; the Spirit Casts Himself Down", "hell"),
    ("LVIII", 551, "All Who are in the Hells are in Evils and in Falsities Therefrom Derived from the Loves of Self and of the World", "hell"),
    ("LVIV", 566, "What Hell Fire is and What the Gnashing of Teeth Is", "hell"),
    ("LX", 576, "The Malice and Heinous Artifices of Infernal Spirits", "hell"),
    ("LXI", 582, "The Appearance, Situation, and Number of the Hells", "hell"),
    ("LXII", 589, "The Equilibrium Between Heaven and Hell", "hell"),
    ("LXIII", 597, "By Means of the Equilibrium Between Heaven and Hell Man is in Freedom", "hell"),
]


def verify_seed(text):
    """Verify this is the correct Gutenberg text."""
    assert "Heaven and its Wonders and Hell" in text[:500], "Wrong seed file!"
    assert "Swedenborg" in text[:1000], "Wrong seed file!"


def extract_body(text):
    """Extract text between Gutenberg markers."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start = text.index(start_marker)
    start = text.index('\n', start) + 1
    end = text.index(end_marker)
    return text[start:end]


def strip_footnotes(text):
    """Remove footnote blocks and footnote markers from text."""
    # Remove footnote blocks: lines starting with {Footnote ...} through next blank line
    lines = text.split('\n')
    cleaned = []
    in_footnote = False
    in_references = False
    footnote_blank_count = 0

    for line in lines:
        stripped = line.strip()

        # Skip REFERENCES/EXTRACTS blocks
        if stripped.startswith('[REFERENCES TO') or stripped.startswith('EXTRACTS FROM THE ARCANA'):
            in_references = True
            continue
        if in_references:
            if stripped == '' :
                footnote_blank_count += 1
                if footnote_blank_count >= 2:
                    in_references = False
                    footnote_blank_count = 0
            else:
                footnote_blank_count = 0
            continue

        # Skip footnote blocks
        if stripped.startswith('{Footnote'):
            in_footnote = True
            continue
        if in_footnote:
            if stripped == '':
                footnote_blank_count += 1
                if footnote_blank_count >= 2:
                    in_footnote = False
                    footnote_blank_count = 0
            else:
                footnote_blank_count = 0
            continue

        cleaned.append(line)

    result = '\n'.join(cleaned)
    # Remove inline footnote markers like {1}, {2}
    result = re.sub(r'\{(\d+)\}', '', result)
    return result


def find_chapter_boundaries(body):
    """Find line positions of each chapter heading."""
    lines = body.split('\n')
    boundaries = []

    for i, ch in enumerate(CHAPTERS):
        roman, sec_num, title, part = ch
        # Pattern: "SEC_NUM. ROMAN. TITLE TEXT"
        pattern = rf'^{sec_num}\.\s+{re.escape(roman)}\.\s+'
        found = False
        for lineno, line in enumerate(lines):
            if re.match(pattern, line.strip()):
                boundaries.append((i, lineno))
                found = True
                break
        if not found:
            print(f"WARNING: Could not find chapter {roman} (section {sec_num})")
            # Try looser match
            for lineno, line in enumerate(lines):
                if line.strip().startswith(f"{sec_num}. {roman}."):
                    boundaries.append((i, lineno))
                    found = True
                    break
        if not found:
            print(f"ERROR: Chapter {roman} not found at all!")

    return boundaries, lines


def extract_chapter_text(boundaries, lines, ch_index):
    """Extract text for a chapter between its heading and the next chapter."""
    ch_idx, start_line = boundaries[ch_index]

    if ch_index + 1 < len(boundaries):
        _, end_line = boundaries[ch_index + 1]
    else:
        end_line = len(lines)

    # Get the heading line(s) - may span multiple lines
    heading_end = start_line + 1
    # Check if title continues on next line (not starting with a number or blank)
    while heading_end < end_line and lines[heading_end].strip() and not re.match(r'^\d+\.', lines[heading_end].strip()):
        # Check if this is part of the title (ALL CAPS continuation)
        if lines[heading_end].strip().isupper() or lines[heading_end].strip().endswith('.'):
            heading_end += 1
        else:
            break

    # Get the body text
    chapter_lines = lines[heading_end:end_line]
    raw_text = '\n'.join(chapter_lines)

    # Strip footnotes
    cleaned = strip_footnotes(raw_text)

    # Clean up extra whitespace
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned).strip()

    return cleaned


def truncate_text(text, max_chars=2800):
    """Truncate text at ~max_chars, finding last period."""
    if len(text) <= max_chars:
        return text
    bp = text.rfind(".", 0, max_chars)
    if bp == -1:
        bp = max_chars
    truncated = text[:bp + 1]
    remaining_words = len(text[bp + 1:].split())
    if remaining_words > 10:
        truncated += f" [Text continues for approximately {remaining_words} more words...]"
    return truncated


def make_id(roman, title):
    """Create a hyphenated ID from chapter info."""
    # Use roman numeral as prefix
    clean = title.lower()
    clean = re.sub(r'[^a-z0-9\s]', '', clean)
    words = clean.split()[:6]
    return f"ch-{roman.lower()}-" + '-'.join(words)


def get_keywords(title, part):
    """Generate keywords from chapter title and part."""
    keywords = [part]
    title_lower = title.lower()
    keyword_map = {
        'angel': 'angels', 'heaven': 'heaven', 'hell': 'hell',
        'spirit': 'spirits', 'love': 'love', 'lord': 'the-lord',
        'divine': 'divine', 'wisdom': 'wisdom', 'peace': 'peace',
        'innocence': 'innocence', 'marriage': 'marriage',
        'death': 'death', 'children': 'children', 'worship': 'worship',
        'speech': 'speech', 'sun': 'sun', 'light': 'light',
        'space': 'space', 'time': 'time', 'fire': 'fire',
        'freedom': 'freedom', 'equilibrium': 'equilibrium',
        'correspondence': 'correspondence', 'human': 'human-form',
        'society': 'societies', 'kingdom': 'kingdoms',
        'heathen': 'heathen', 'rich': 'rich-and-poor',
        'poor': 'rich-and-poor', 'govern': 'government',
        'garment': 'garments', 'dwelling': 'dwellings',
        'writing': 'writings', 'power': 'power',
        'joy': 'joy', 'happiness': 'happiness',
        'resuscitation': 'resuscitation', 'memory': 'memory',
        'instruction': 'instruction', 'mercy': 'mercy',
    }
    for key, val in keyword_map.items():
        if key in title_lower and val not in keywords:
            keywords.append(val)
    return keywords


def build_grammar():
    with open(SEED_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    verify_seed(text)
    body = extract_body(text)
    boundaries, lines = find_chapter_boundaries(body)

    items = []
    sort_order = 1

    # Also extract intro (section 1, before chapter I)
    if boundaries:
        intro_end = boundaries[0][1]
        intro_text = '\n'.join(lines[:intro_end])
        intro_text = strip_footnotes(intro_text).strip()
        # Remove the title/header lines
        intro_text = re.sub(r'^.*?From Things Heard and Seen.*?\n', '', intro_text, flags=re.DOTALL)
        intro_text = re.sub(r'^.*?Translated by.*?\n', '', intro_text, flags=re.DOTALL)
        # Find the actual numbered section start
        intro_match = re.search(r'^1\. ', intro_text, re.MULTILINE)
        if intro_match:
            intro_text = intro_text[intro_match.start():]
        intro_text = truncate_text(intro_text.strip())

        items.append({
            "id": "introduction",
            "name": "Introduction",
            "sort_order": sort_order,
            "category": "heaven",
            "level": 1,
            "sections": {
                "Text": intro_text,
                "About": "Swedenborg's opening statement explaining the purpose of his revelations about heaven and hell, based on thirteen years of spiritual experience."
            },
            "keywords": ["introduction", "revelation", "spiritual-vision"],
            "metadata": {"section_numbers": "1", "part": "introduction"}
        })
        sort_order += 1

    # L1: Individual chapters
    chapter_ids_by_part = {"heaven": [], "world-of-spirits": [], "hell": []}

    for idx, (roman, sec_num, title, part) in enumerate(CHAPTERS):
        ch_text = extract_chapter_text(boundaries, lines, idx)
        ch_text = truncate_text(ch_text)
        ch_id = make_id(roman, title)
        chapter_ids_by_part[part].append(ch_id)

        # Determine ending section number
        if idx + 1 < len(CHAPTERS):
            end_sec = CHAPTERS[idx + 1][1] - 1
        else:
            end_sec = 603  # Last section of the book

        items.append({
            "id": ch_id,
            "name": f"{roman}. {title}",
            "sort_order": sort_order,
            "category": part,
            "level": 1,
            "sections": {
                "Text": ch_text,
                "About": f"Chapter {roman} of Heaven and Hell, sections {sec_num}-{end_sec}. {title}."
            },
            "keywords": get_keywords(title, part),
            "metadata": {
                "chapter_roman": roman,
                "section_numbers": f"{sec_num}-{end_sec}",
                "part": part
            }
        })
        sort_order += 1

    # L2: Part groupings
    part_defs = [
        ("heaven-part", "Part One: Heaven", "heaven",
         "The first and largest section of the work, comprising 43 chapters (I-XLIII). Swedenborg describes the nature of heaven based on his spiritual visions: the Lord as God of heaven, angelic societies, the human form of heaven, correspondences, the sun and light of heaven, angelic speech and wisdom, states of innocence and peace, and the diversity of heavenly life including children, the wise and simple, and marriages.",
         "Chapters I-XLIII covering the structure, governance, inhabitants, and nature of heavenly life as witnessed by Swedenborg."),
        ("world-of-spirits-part", "Part Two: The World of Spirits", "world-of-spirits",
         "The middle section, comprising 12 chapters (XLIV-LV). This covers the intermediate realm between heaven and hell where all people first arrive after death. Swedenborg describes the process of dying, the preservation of memory and senses, the three states of transition, and the path toward either heaven or hell based on one's inner character.",
         "Chapters XLIV-LV covering the intermediate state between heaven and hell, the process of death and transition, and the sorting of souls."),
        ("hell-part", "Part Three: Hell", "hell",
         "The final section, comprising 8 chapters (LVI-LXIII). Swedenborg describes the Lord's governance over hell, the nature of hellfire as burning desire and hatred, the malice of infernal spirits, the appearance and structure of the hells, and the equilibrium between heaven and hell that preserves human freedom.",
         "Chapters LVI-LXIII covering the nature, governance, and structure of hell, and the equilibrium between heaven and hell."),
    ]

    for part_id, part_name, part_key, about, summary in part_defs:
        composite = []
        if part_key == "heaven":
            composite = ["introduction"] + chapter_ids_by_part[part_key]
        else:
            composite = chapter_ids_by_part[part_key]

        items.append({
            "id": part_id,
            "name": part_name,
            "sort_order": sort_order,
            "category": part_key,
            "level": 2,
            "sections": {
                "About": about,
                "Summary": summary,
                "For Readers": f"This section groups all chapters belonging to {part_name}. Read sequentially for Swedenborg's complete vision, or explore individual chapters by topic."
            },
            "keywords": [part_key, "swedenborg", "afterlife"],
            "composite_of": composite,
            "relationship_type": "emergence",
            "metadata": {"part": part_key}
        })
        sort_order += 1

    # L3: The complete work
    items.append({
        "id": "complete-work",
        "name": "Heaven and Hell: The Complete Vision",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Emanuel Swedenborg's 'Heaven and its Wonders and Hell' (De Caelo et ejus Mirabilibus et de Inferno, 1758) is one of the most influential visionary accounts of the afterlife in Western literature. Based on what Swedenborg claimed were thirteen years of direct spiritual experience, the work systematically describes the structure and nature of heaven, the intermediate world of spirits, and hell. Unlike medieval visions of torment, Swedenborg's afterlife is psychological: heaven and hell are states of being determined by one's inner loves and character, not external rewards or punishments.",
            "Summary": "The work is divided into three parts: Heaven (43 chapters on angelic life, correspondences, and the structure of heavenly societies), The World of Spirits (12 chapters on the transition after death), and Hell (8 chapters on infernal states and the equilibrium that preserves human freedom). The text profoundly influenced William Blake, Ralph Waldo Emerson, Helen Keller, Jorge Luis Borges, and the founding of the Swedenborgian Church.",
            "For Readers": "This grammar presents each of Swedenborg's 63 chapters as individual items, grouped into three major parts. The text is rich with specific visionary detail — Swedenborg describes angelic garments, heavenly architecture, the speech of angels, and the psychology of infernal spirits with the precision of a scientist cataloguing a newly discovered world."
        },
        "keywords": ["swedenborg", "afterlife", "heaven", "hell", "complete-work", "mysticism"],
        "composite_of": ["heaven-part", "world-of-spirits-part", "hell-part"],
        "relationship_type": "emergence",
        "metadata": {"part": "meta"}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Emanuel Swedenborg",
                    "date": "1758",
                    "note": "Original Latin: De Caelo et ejus Mirabilibus et de Inferno, ex Auditis et Visis"
                },
                {
                    "name": "John C. Ager",
                    "date": "1900",
                    "note": "English translation"
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2005",
                    "note": "eBook #17368, e-text donated by the Kempton Project"
                }
            ]
        },
        "name": "Heaven and Hell",
        "description": "Emanuel Swedenborg's visionary account of the afterlife, 'Heaven and its Wonders and Hell' (1758), describing the structure of heaven, the world of spirits, and hell based on his claimed thirteen years of direct spiritual experience. Translated by John C. Ager.\n\nSource: Project Gutenberg eBook #17368 (https://www.gutenberg.org/ebooks/17368)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: William Blake's illustrations inspired by Swedenborg's visions (1790s), particularly from 'The Marriage of Heaven and Hell.' John Flaxman's neoclassical spiritual illustrations. Hieronymus Bosch's 'The Garden of Earthly Delights' (1490-1510) for hellscape imagery. Gustave Doré's illustrations for Dante's Divine Comedy provide parallel afterlife imagery.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["swedenborg", "afterlife", "heaven", "hell", "mysticism", "visions", "christianity"],
        "roots": ["mysticism", "western-esotericism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "devotional",
        "items": items
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"Grammar written to {OUTPUT_FILE}")
    print(f"Total items: {len(items)}")
    print(f"  L1: {sum(1 for i in items if i['level'] == 1)}")
    print(f"  L2: {sum(1 for i in items if i['level'] == 2)}")
    print(f"  L3: {sum(1 for i in items if i['level'] == 3)}")


if __name__ == '__main__':
    build_grammar()
