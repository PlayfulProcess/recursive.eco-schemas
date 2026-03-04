#!/usr/bin/env python3
"""
Parse The Upanishads (Swami Paramananda translation, Gutenberg #3283)
into a grammar.json.

Structure:
- L1: Individual verses from Isha (18), Katha (6 parts), and Kena (4 parts)
- L2: Each Upanishad as a group, Katha/Kena parts, thematic groups
- L3: Meta-level connecting all
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "upanishads.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "upanishads")
OUTPUT = os.path.join(OUTPUT_DIR, "grammar.json")

# Roman numeral pattern
ROMAN_RE = re.compile(r'^(X{0,3})(IX|IV|V?I{0,3})$')

def roman_to_int(s):
    """Convert roman numeral string to integer."""
    s = s.strip()
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    total = 0
    prev = 0
    for ch in reversed(s):
        v = vals.get(ch, 0)
        if v < prev:
            total -= v
        else:
            total += v
        prev = v
    return total


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1:
        text = text[text.index("\n", start) + 1:]
    if end != -1:
        text = text[:end]
    return text.strip()


def find_upanishad_sections(text):
    """Split the text into three Upanishad sections.

    Returns dict with keys 'isha', 'katha', 'kena', each containing
    the full text of that Upanishad (including intro and commentary).
    """
    # Find the second occurrence of each heading (the actual text, not the intro)
    # Pattern: the heading appears twice - once for intro, once for the actual verses

    # Isa-Upanishad text starts at the second "Isa-Upanishad" heading
    isha_positions = [m.start() for m in re.finditer(r'^\s*Isa-Upanishad\s*$', text, re.MULTILINE)]
    katha_positions = [m.start() for m in re.finditer(r'^\s*Katha-Upanishad\s*$', text, re.MULTILINE)]
    kena_positions = [m.start() for m in re.finditer(r'^\s*(?:Kena-Upanishad|KENA-UPANISHAD)\s*$', text, re.MULTILINE)]

    # Second occurrence is the actual text with verses
    isha_start = isha_positions[1] if len(isha_positions) >= 2 else isha_positions[0]
    katha_start = katha_positions[1] if len(katha_positions) >= 2 else katha_positions[0]
    kena_start = kena_positions[1] if len(kena_positions) >= 2 else kena_positions[0]

    # Find endings
    isha_end_match = re.search(r'Here ends this Upanishad', text[isha_start:])
    isha_end = isha_start + isha_end_match.end() if isha_end_match else katha_positions[0]

    katha_end_match = re.search(r'Here ends this Upanishad', text[katha_start:])
    katha_end = katha_start + katha_end_match.end() if katha_end_match else kena_positions[0]

    kena_end_match = re.search(r'Here ends this Upanishad', text[kena_start:])
    kena_end = kena_start + kena_end_match.end() if kena_end_match else len(text)

    return {
        'isha': text[isha_start:isha_end],
        'katha': text[katha_start:katha_end],
        'kena': text[kena_start:kena_end],
    }


def parse_verses_from_section(section_text):
    """Parse roman-numeral-headed verses from a section of text.

    Returns list of (verse_number, verse_text, commentary_text) tuples.
    Each verse is separated by roman numeral headings on their own line.
    The verse text is the first paragraph after the numeral; subsequent
    paragraphs are commentary.
    """
    lines = section_text.split('\n')

    # Find all roman numeral positions
    verse_positions = []  # (line_index, verse_num)
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Match a line that is purely a roman numeral (possibly with leading space)
        # But exclude "Part First", "Part Second" etc.
        if ROMAN_RE.match(stripped) and stripped:
            num = roman_to_int(stripped)
            if num > 0:
                verse_positions.append((i, num))

    verses = []
    for idx, (line_idx, verse_num) in enumerate(verse_positions):
        # Get text from after this roman numeral to the next one
        start = line_idx + 1
        if idx + 1 < len(verse_positions):
            end = verse_positions[idx + 1][0]
        else:
            end = len(lines)

        block = '\n'.join(lines[start:end]).strip()

        # Split into verse text and commentary
        # The verse is typically the first paragraph(s) before a blank line
        # followed by commentary paragraphs that are typically longer prose
        verse_text, commentary_text = split_verse_and_commentary(block)

        verses.append((verse_num, verse_text, commentary_text))

    return verses


def split_verse_and_commentary(block):
    """Split a block of text into verse and commentary.

    The verse is the initial paragraph(s) of the block - typically shorter,
    more poetic lines. Commentary follows after a blank line and tends to
    be longer explanatory prose.

    Strategy: Split on double newlines into paragraphs. The first paragraph
    is always verse text. Subsequent paragraphs are commentary.
    """
    paragraphs = re.split(r'\n\s*\n', block.strip())

    if not paragraphs:
        return "", ""

    # First paragraph is always the verse
    verse_text = clean_paragraph(paragraphs[0])

    # Remaining paragraphs are commentary
    commentary_parts = []
    for p in paragraphs[1:]:
        cleaned = clean_paragraph(p)
        if cleaned:
            # Stop at "Here ends this Upanishad" or "PEACE CHANT"
            if 'Here ends this Upanishad' in cleaned or cleaned.startswith('PEACE CHANT'):
                break
            # Skip closing essay markers
            if cleaned.startswith('This Upanishad is called') or cleaned.startswith('This particular Upanishad'):
                break
            commentary_parts.append(cleaned)

    commentary_text = '\n\n'.join(commentary_parts)

    return verse_text, commentary_text


def clean_paragraph(text):
    """Clean up a paragraph: normalize whitespace, strip."""
    # Replace multiple spaces and newlines with single spaces
    text = re.sub(r'\s+', ' ', text.strip())
    return text


def parse_katha_parts(katha_text):
    """Parse the Katha Upanishad which has 6 parts (Vallis).

    Returns dict: part_num -> [(verse_num, verse_text, commentary)]
    """
    # Split into parts
    part_pattern = re.compile(r'^\s*Part\s+(First|Second|Third|Fourth|Fifth|Sixth)\s*$', re.MULTILINE)
    part_names = {'First': 1, 'Second': 2, 'Third': 3, 'Fourth': 4, 'Fifth': 5, 'Sixth': 6}

    parts = {}
    matches = list(part_pattern.finditer(katha_text))

    for idx, match in enumerate(matches):
        part_num = part_names[match.group(1)]
        start = match.end()
        if idx + 1 < len(matches):
            end = matches[idx + 1].start()
        else:
            end = len(katha_text)

        part_text = katha_text[start:end]
        verses = parse_verses_from_section(part_text)
        parts[part_num] = verses

    return parts


def parse_kena_parts(kena_text):
    """Parse the Kena Upanishad which has 4 parts.

    Returns dict: part_num -> [(verse_num, verse_text, commentary)]
    """
    part_pattern = re.compile(r'^\s*Part\s+(First|Second|Third|fourth|Fourth)\s*$', re.MULTILINE | re.IGNORECASE)
    part_names_lower = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4}

    parts = {}
    matches = list(part_pattern.finditer(kena_text))

    for idx, match in enumerate(matches):
        part_num = part_names_lower[match.group(1).lower()]
        start = match.end()
        if idx + 1 < len(matches):
            end = matches[idx + 1].start()
        else:
            end = len(kena_text)

        part_text = kena_text[start:end]
        verses = parse_verses_from_section(part_text)
        parts[part_num] = verses

    return parts


def build_grammar():
    """Build the complete grammar.json."""
    with open(SEED, 'r', encoding='utf-8') as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    sections = find_upanishad_sections(text)

    items = []
    sort_order = 0

    # Track IDs for L2 composites
    isha_ids = []
    katha_part_ids = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    katha_all_ids = []
    kena_part_ids = {1: [], 2: [], 3: [], 4: []}
    kena_all_ids = []

    # === Parse Isha Upanishad (no parts, just verses I-XVIII) ===
    # Skip the Peace Chant - find verses after it
    isha_text = sections['isha']
    isha_verses = parse_verses_from_section(isha_text)

    # Also extract the Peace Chant as a special item
    peace_chant_match = re.search(r'Peace Chant\s*\n\s*\n(.*?)(?=\n\s*\n\s*(?:The indefinite|I\s*$))', isha_text, re.DOTALL)
    if peace_chant_match:
        peace_text = clean_paragraph(peace_chant_match.group(1))
        item_id = "isha-peace-chant"
        items.append({
            "id": item_id,
            "name": "Isha Upanishad: Peace Chant",
            "sort_order": sort_order,
            "category": "isha",
            "level": 1,
            "sections": {
                "Verse": peace_text,
            },
            "keywords": ["peace", "om", "invocation", "whole", "absolute"],
            "metadata": {"upanishad": "isha", "verse_type": "peace-chant"}
        })
        isha_ids.append(item_id)
        sort_order += 1

    for verse_num, verse_text, commentary in isha_verses:
        item_id = f"isha-v{verse_num:02d}"
        name = f"Isha Upanishad, Verse {verse_num}"

        sections_dict = {"Verse": verse_text}
        if commentary:
            sections_dict["Commentary"] = commentary

        keywords = extract_keywords_isha(verse_num, verse_text)

        items.append({
            "id": item_id,
            "name": name,
            "sort_order": sort_order,
            "category": "isha",
            "level": 1,
            "sections": sections_dict,
            "keywords": keywords,
            "metadata": {"upanishad": "isha", "verse": verse_num}
        })
        isha_ids.append(item_id)
        sort_order += 1

    # === Parse Katha Upanishad (6 parts) ===
    katha_parts = parse_katha_parts(sections['katha'])

    # Extract Katha Peace Chant
    katha_text = sections['katha']
    katha_peace_match = re.search(r'Peace Chant\s*\n\s*\n(.*?)(?=\n\s*\n\s*OM)', katha_text, re.DOTALL)
    if katha_peace_match:
        peace_text = clean_paragraph(katha_peace_match.group(1))
        # Include the OM line
        peace_text += " OM! PEACE! PEACE! PEACE!"
        item_id = "katha-peace-chant"
        items.append({
            "id": item_id,
            "name": "Katha Upanishad: Peace Chant",
            "sort_order": sort_order,
            "category": "katha",
            "level": 1,
            "sections": {
                "Verse": peace_text,
            },
            "keywords": ["peace", "om", "invocation", "protection", "illumination"],
            "metadata": {"upanishad": "katha", "verse_type": "peace-chant"}
        })
        katha_all_ids.append(item_id)
        sort_order += 1

    for part_num in sorted(katha_parts.keys()):
        verses = katha_parts[part_num]
        for verse_num, verse_text, commentary in verses:
            item_id = f"katha-{part_num}-{verse_num:02d}"
            name = f"Katha Upanishad, Part {part_num}, Verse {verse_num}"

            sections_dict = {"Verse": verse_text}
            if commentary:
                sections_dict["Commentary"] = commentary

            keywords = extract_keywords_katha(part_num, verse_num, verse_text)

            items.append({
                "id": item_id,
                "name": name,
                "sort_order": sort_order,
                "category": "katha",
                "level": 1,
                "sections": sections_dict,
                "keywords": keywords,
                "metadata": {"upanishad": "katha", "part": part_num, "verse": verse_num}
            })
            katha_part_ids[part_num].append(item_id)
            katha_all_ids.append(item_id)
            sort_order += 1

    # === Parse Kena Upanishad (4 parts) ===
    kena_parts = parse_kena_parts(sections['kena'])

    # Extract Kena Peace Chant
    kena_text = sections['kena']
    kena_peace_match = re.search(r'Peace Chant\s*\n\s*\n(.*?)(?=\n\s*\n\s*OM)', kena_text, re.DOTALL)
    if kena_peace_match:
        peace_text = clean_paragraph(kena_peace_match.group(1))
        peace_text += " OM! PEACE! PEACE! PEACE!"
        item_id = "kena-peace-chant"
        items.append({
            "id": item_id,
            "name": "Kena Upanishad: Peace Chant",
            "sort_order": sort_order,
            "category": "kena",
            "level": 1,
            "sections": {
                "Verse": peace_text,
            },
            "keywords": ["peace", "om", "invocation", "brahman", "atman"],
            "metadata": {"upanishad": "kena", "verse_type": "peace-chant"}
        })
        kena_all_ids.append(item_id)
        sort_order += 1

    for part_num in sorted(kena_parts.keys()):
        verses = kena_parts[part_num]
        for verse_num, verse_text, commentary in verses:
            item_id = f"kena-{part_num}-{verse_num:02d}"
            name = f"Kena Upanishad, Part {part_num}, Verse {verse_num}"

            sections_dict = {"Verse": verse_text}
            if commentary:
                sections_dict["Commentary"] = commentary

            keywords = extract_keywords_kena(part_num, verse_num, verse_text)

            items.append({
                "id": item_id,
                "name": name,
                "sort_order": sort_order,
                "category": "kena",
                "level": 1,
                "sections": sections_dict,
                "keywords": keywords,
                "metadata": {"upanishad": "kena", "part": part_num, "verse": verse_num}
            })
            kena_part_ids[part_num].append(item_id)
            kena_all_ids.append(item_id)
            sort_order += 1

    # === L2: Upanishad groups ===

    # Isha Upanishad group
    items.append({
        "id": "l2-isha-upanishad",
        "name": "Isha Upanishad",
        "sort_order": sort_order,
        "category": "upanishad-group",
        "level": 2,
        "sections": {
            "About": "The Isha Upanishad (18 verses) opens with one of the most radical statements in spiritual literature: 'All this is pervaded by the Lord.' It teaches non-attachment, renunciation through engagement, and the unity of knowledge and action.",
            "For Readers": "The Isha is the shortest and most concentrated of the Upanishads. Read it slowly, one verse at a time. Each verse is a complete teaching. The opening verse alone -- 'All this is pervaded by the Lord; having renounced the unreal, enjoy the Real' -- contains the entire philosophy of Vedanta in a single breath."
        },
        "keywords": ["isha", "lord", "renunciation", "knowledge", "action", "unity"],
        "metadata": {"upanishad": "isha"},
        "composite_of": isha_ids,
        "relationship_type": "emergence"
    })
    sort_order += 1

    # Katha Upanishad group
    items.append({
        "id": "l2-katha-upanishad",
        "name": "Katha Upanishad",
        "sort_order": sort_order,
        "category": "upanishad-group",
        "level": 2,
        "sections": {
            "About": "The Katha Upanishad tells the story of the boy Nachiketas who visits Death (Yama) and receives the teaching of the Atman (Self). It contains the famous chariot metaphor: the body is the chariot, the Self the rider, the intellect the charioteer, the mind the reins, the senses the horses.",
            "For Readers": "The Katha is the most narrative of the Upanishads and the most accessible. Follow Nachiketas as he refuses every temptation Death offers -- wealth, power, pleasure, long life -- insisting on the one question that matters: What happens after death? The answer transforms the question itself."
        },
        "keywords": ["nachiketas", "death", "yama", "atman", "chariot", "self", "immortality"],
        "metadata": {"upanishad": "katha"},
        "composite_of": katha_all_ids,
        "relationship_type": "emergence"
    })
    sort_order += 1

    # Katha part sub-groups
    katha_part_descriptions = {
        1: "Nachiketas visits Death: the story of the sacrifice, the three boons, and Yama's initial reluctance to teach the secret of what lies beyond death.",
        2: "The teaching begins: the good vs. the pleasant, the nature of the Self (Atman), and the famous declaration 'The Self is never born, nor does It die.'",
        3: "The chariot metaphor: body as chariot, Self as rider, intellect as charioteer, mind as reins, senses as horses. 'Arise! Awake! Having reached the Great Ones, gain understanding.'",
        4: "The Self within all beings: the senses are made outward-going, but the wise turn inward. 'What is here, that is there; he who sees difference goes from death to death.'",
        5: "The city of eleven gates: the body as dwelling-place of the unborn Spirit. 'As fire, though one, becomes various according to what it burns, so does the Self within all beings.'",
        6: "The tree of creation, rooted above in Brahman. Yoga as the firm holding back of the senses. 'When all desires dwelling in the heart cease, then the mortal becomes immortal.'"
    }
    for pn in sorted(katha_part_ids.keys()):
        if katha_part_ids[pn]:
            items.append({
                "id": f"l2-katha-part-{pn}",
                "name": f"Katha Upanishad, Part {pn}",
                "sort_order": sort_order,
                "category": "katha-part",
                "level": 2,
                "sections": {
                    "About": katha_part_descriptions.get(pn, f"Part {pn} of the Katha Upanishad."),
                },
                "keywords": ["katha", "nachiketas", "yama"],
                "metadata": {"upanishad": "katha", "part": pn},
                "composite_of": katha_part_ids[pn],
                "relationship_type": "emergence"
            })
            sort_order += 1

    # Kena Upanishad group
    items.append({
        "id": "l2-kena-upanishad",
        "name": "Kena Upanishad",
        "sort_order": sort_order,
        "category": "upanishad-group",
        "level": 2,
        "sections": {
            "About": "The Kena Upanishad asks 'By whose will?' (kena) -- who directs the mind, the breath, the eye? Its answer: Brahman cannot be known as an object of knowledge, for it is the very ground of knowing itself.",
            "For Readers": "The Kena moves from philosophical inquiry (Parts 1-2) to parable (Parts 3-4). The story of the gods who cannot burn a straw or blow it away -- humbled before the mystery of Brahman -- is one of the most vivid illustrations of the limits of power without wisdom."
        },
        "keywords": ["kena", "brahman", "knowledge", "mind", "consciousness", "devas"],
        "metadata": {"upanishad": "kena"},
        "composite_of": kena_all_ids,
        "relationship_type": "emergence"
    })
    sort_order += 1

    # Kena part sub-groups
    kena_part_descriptions = {
        1: "The fundamental question: 'By whom commanded does the mind go towards its objects?' The answer: Brahman is the ear of the ear, the mind of the mind, the eye of the eye.",
        2: "The paradox of knowing Brahman: 'He who thinks he knows It not, knows It. He who thinks he knows It, knows It not.' True knowledge transcends intellectual certainty.",
        3: "The parable of the Devas: Brahman wins a victory, but the gods take credit. Fire cannot burn a straw, Wind cannot blow it away -- only when Uma reveals the truth does Indra understand.",
        4: "The resolution: Brahman appeared like a flash of lightning. The teaching is based on tapas (self-discipline), dama (sense-control), and karma (right action). Truth is its support."
    }
    for pn in sorted(kena_part_ids.keys()):
        if kena_part_ids[pn]:
            items.append({
                "id": f"l2-kena-part-{pn}",
                "name": f"Kena Upanishad, Part {pn}",
                "sort_order": sort_order,
                "category": "kena-part",
                "level": 2,
                "sections": {
                    "About": kena_part_descriptions.get(pn, f"Part {pn} of the Kena Upanishad."),
                },
                "keywords": ["kena", "brahman"],
                "metadata": {"upanishad": "kena", "part": pn},
                "composite_of": kena_part_ids[pn],
                "relationship_type": "emergence"
            })
            sort_order += 1

    # === L2: Thematic groups ===

    # The Nature of Brahman
    brahman_ids = [
        "isha-v01", "isha-v04", "isha-v05", "isha-v08", "isha-v15", "isha-v16",
        "katha-2-14", "katha-2-15", "katha-2-16", "katha-2-17",
        "katha-3-10", "katha-3-11",
        "katha-5-02", "katha-5-08", "katha-5-09", "katha-5-10", "katha-5-15",
        "katha-6-01", "katha-6-02", "katha-6-03",
        "kena-1-02", "kena-1-03", "kena-1-04", "kena-1-05", "kena-1-06", "kena-1-07", "kena-1-08",
        "kena-2-01", "kena-2-02", "kena-2-03", "kena-2-04",
        "kena-3-01", "kena-3-06", "kena-3-10", "kena-3-12",
        "kena-4-01",
    ]
    # Filter to only include IDs that actually exist
    all_item_ids = {item['id'] for item in items}
    brahman_ids = [i for i in brahman_ids if i in all_item_ids]

    items.append({
        "id": "l2-theme-brahman",
        "name": "The Nature of Brahman",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "Brahman is the central concept of the Upanishads: the ultimate reality, the ground of all being, the infinite and unchanging source from which all things arise and to which all return. These verses explore what Brahman is -- not through definition, for Brahman exceeds all categories, but through negation, analogy, and the shock of paradox. 'The sun does not shine there, nor the moon, nor the stars; when He shines, everything shines after Him.'",
            "For Readers": "Read these verses as attempts to point at something that cannot be pointed at. Each one approaches the mystery from a different angle. Notice how often the Upanishads say what Brahman is NOT -- formless, soundless, touchless, undecaying -- because the Infinite cannot be captured in finite terms."
        },
        "keywords": ["brahman", "absolute", "infinite", "reality", "source"],
        "metadata": {"theme": "brahman"},
        "composite_of": brahman_ids,
        "relationship_type": "emergence"
    })
    sort_order += 1

    # The Self (Atman)
    atman_ids = [
        "isha-v06", "isha-v07",
        "katha-2-18", "katha-2-19", "katha-2-20", "katha-2-21", "katha-2-22", "katha-2-23", "katha-2-24",
        "katha-3-03", "katha-3-04", "katha-3-12", "katha-3-13",
        "katha-4-01", "katha-4-03", "katha-4-04", "katha-4-05", "katha-4-12", "katha-4-13",
        "katha-5-01", "katha-5-03", "katha-5-04", "katha-5-11", "katha-5-12", "katha-5-13",
        "katha-6-07", "katha-6-08", "katha-6-09", "katha-6-17",
    ]
    atman_ids = [i for i in atman_ids if i in all_item_ids]

    items.append({
        "id": "l2-theme-atman",
        "name": "The Self (Atman)",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "Atman is the Self -- not the ego or personality, but the deathless, unchanging awareness at the core of every being. The Upanishads' most radical teaching is that Atman and Brahman are one: the individual Self and the cosmic ground of being are identical. 'The Self is never born, nor does It die. It did not spring from anything, nor did anything spring from It.'",
            "For Readers": "The Atman verses move from description to experience. The Self is described as 'subtler than the subtle, greater than the great,' dwelling in the heart of every creature. But description is only a starting point -- the Upanishads insist that the Self must be directly realized, not merely understood intellectually."
        },
        "keywords": ["atman", "self", "soul", "consciousness", "immortality", "heart"],
        "metadata": {"theme": "atman"},
        "composite_of": atman_ids,
        "relationship_type": "emergence"
    })
    sort_order += 1

    # The Path of Knowledge
    path_ids = [
        "isha-v02", "isha-v09", "isha-v10", "isha-v11", "isha-v14",
        "katha-1-20", "katha-1-21", "katha-1-22", "katha-1-23", "katha-1-24", "katha-1-25",
        "katha-1-26", "katha-1-27", "katha-1-28", "katha-1-29",
        "katha-2-01", "katha-2-02", "katha-2-04", "katha-2-05", "katha-2-06", "katha-2-07",
        "katha-2-08", "katha-2-09",
        "katha-3-05", "katha-3-06", "katha-3-07", "katha-3-08", "katha-3-09", "katha-3-14",
        "katha-6-10", "katha-6-11", "katha-6-14", "katha-6-15",
        "kena-2-05",
        "kena-4-08",
    ]
    path_ids = [i for i in path_ids if i in all_item_ids]

    items.append({
        "id": "l2-theme-path",
        "name": "The Path of Knowledge",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "The Upanishads do not merely describe ultimate reality -- they prescribe a path to realize it. This path requires discrimination between the real and the unreal, control of the senses, and the guidance of an illumined teacher. The Katha Upanishad's chariot metaphor captures it perfectly: the body is the chariot, the Self the rider, the intellect the charioteer, the mind the reins, the senses the horses.",
            "For Readers": "These verses are practical instructions wrapped in metaphor. The good versus the pleasant, the sharp razor's edge of the path, the need for a teacher, the discipline of yoga -- these are not abstract philosophy but a lived program of inner transformation. 'Arise! Awake! Having reached the Great Ones, gain understanding.'"
        },
        "keywords": ["path", "knowledge", "discrimination", "yoga", "teacher", "discipline", "awakening"],
        "metadata": {"theme": "path-of-knowledge"},
        "composite_of": path_ids,
        "relationship_type": "emergence"
    })
    sort_order += 1

    # === L3: The Upanishads ===
    all_l2_ids = [item['id'] for item in items if item['level'] == 2]

    items.append({
        "id": "l3-the-upanishads",
        "name": "The Upanishads: End of the Vedas",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "The Upanishads (literally 'sitting near the teacher') are the philosophical conclusion of the Vedas, the oldest scriptures of India. Known as Vedanta -- 'the end of the Vedas' -- they distill millennia of spiritual inquiry into a single insight: Atman is Brahman, the individual Self is the universal Self. This collection presents three principal Upanishads in Swami Paramananda's luminous 1919 translation: the Isha (on non-attachment and divine pervading), the Katha (Nachiketas' dialogue with Death), and the Kena (the inquiry into the ground of consciousness). Together they form one of humanity's most profound explorations of the nature of reality, consciousness, and liberation.",
            "The Great Sayings": "The Upanishads' teachings are summed up in two Maha-Vakyam (great sayings): 'Tat twam asi' (That thou art) and 'Aham Brahmasmi' (I am Brahman). This oneness of Soul and God lies at the very root of all Vedic thought.",
            "Historical Note": "No date for the origin of the Upanishads can be fixed, as the oral teaching long preceded any written text. Scholars place the Vedic period between 4000 BCE and 1400 BCE. Schopenhauer called the Upanishads 'the most rewarding and elevating reading which is possible in the world.' Thoreau wrote: 'What extracts from the Vedas I have read fall on me like the light of a higher and purer luminary.'"
        },
        "keywords": ["upanishads", "vedanta", "brahman", "atman", "vedas", "non-dual", "liberation"],
        "metadata": {"level": "meta"},
        "composite_of": all_l2_ids,
        "relationship_type": "emergence"
    })
    sort_order += 1

    # === Build final grammar ===
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Anonymous (Vedic sages)", "date": "~800-200 BCE", "note": "Original authors"},
                {"name": "Swami Paramananda", "date": "1919", "note": "Translator and commentator"}
            ]
        },
        "name": "The Upanishads",
        "description": "Three principal Upanishads \u2014 Isha, Katha, and Kena \u2014 translated from Sanskrit by Swami Paramananda. The Upanishads ('sitting near the teacher') are the philosophical conclusion of the Vedas, exploring the nature of Brahman (ultimate reality), Atman (the Self), and their identity. These texts are the fountainhead of Vedanta philosophy and the deepest roots of yoga, meditation, and non-dual awareness.\n\nSource: Project Gutenberg eBook #3283 (https://www.gutenberg.org/ebooks/3283)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Rajput miniature paintings of sages and forest ashrams. Illustrations from early 20th century Vedanta Society publications. Traditional Indian manuscript illuminations.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "vedanta", "indian", "sacred-text", "public-domain", "full-text", "wisdom", "non-dual", "sanskrit"],
        "roots": ["eastern-wisdom"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "non-dual",
        "items": items
    }

    return grammar


def extract_keywords_isha(verse_num, text):
    """Extract keywords for Isha verses based on content."""
    keywords = ["isha", "vedanta"]
    text_lower = text.lower()
    keyword_map = {
        "lord": "lord", "renounce": "renunciation", "enjoy": "enjoyment",
        "covet": "non-attachment", "karma": "karma", "death": "death",
        "self": "self", "atman": "atman", "soul": "soul",
        "oneness": "oneness", "ignorance": "ignorance", "wisdom": "wisdom",
        "vidya": "vidya", "avidya": "avidya", "immortal": "immortality",
        "truth": "truth", "pushan": "sun", "agni": "fire",
        "brahman": "brahman", "prana": "prana",
    }
    for trigger, kw in keyword_map.items():
        if trigger in text_lower and kw not in keywords:
            keywords.append(kw)
    return keywords[:8]


def extract_keywords_katha(part, verse, text):
    """Extract keywords for Katha verses based on content."""
    keywords = ["katha", "nachiketas"]
    text_lower = text.lower()
    keyword_map = {
        "yama": "yama", "death": "death", "self": "self", "atman": "atman",
        "soul": "soul", "brahman": "brahman", "chariot": "chariot",
        "senses": "senses", "mind": "mind", "intellect": "intellect",
        "immortal": "immortality", "fire": "fire-sacrifice",
        "yoga": "yoga", "om": "om", "aum": "om", "purusha": "purusha",
        "discrimination": "discrimination", "desire": "desire",
        "born": "birth", "awake": "awakening",
    }
    for trigger, kw in keyword_map.items():
        if trigger in text_lower and kw not in keywords:
            keywords.append(kw)
    return keywords[:8]


def extract_keywords_kena(part, verse, text):
    """Extract keywords for Kena verses based on content."""
    keywords = ["kena", "brahman"]
    text_lower = text.lower()
    keyword_map = {
        "mind": "mind", "speech": "speech", "eye": "eye", "ear": "ear",
        "breath": "breath", "immortal": "immortality", "self": "self",
        "atman": "atman", "agni": "fire", "vayu": "wind", "indra": "indra",
        "uma": "uma", "deva": "devas", "knowledge": "knowledge",
        "tapas": "tapas", "truth": "truth", "worship": "worship",
    }
    for trigger, kw in keyword_map.items():
        if trigger in text_lower and kw not in keywords:
            keywords.append(kw)
    return keywords[:8]


if __name__ == "__main__":
    grammar = build_grammar()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Print stats
    items = grammar['items']
    l1 = [i for i in items if i['level'] == 1]
    l2 = [i for i in items if i['level'] == 2]
    l3 = [i for i in items if i['level'] == 3]

    isha_items = [i for i in l1 if i['category'] == 'isha']
    katha_items = [i for i in l1 if i['category'] == 'katha']
    kena_items = [i for i in l1 if i['category'] == 'kena']

    print(f"Grammar written to {OUTPUT}")
    print(f"Total items: {len(items)}")
    print(f"  L1 (verses): {len(l1)}")
    print(f"    Isha: {len(isha_items)}")
    print(f"    Katha: {len(katha_items)}")
    print(f"    Kena: {len(kena_items)}")
    print(f"  L2 (groups/themes): {len(l2)}")
    print(f"  L3 (meta): {len(l3)}")

    # Validate
    all_ids = [i['id'] for i in items]
    dupes = set([x for x in all_ids if all_ids.count(x) > 1])
    if dupes:
        print(f"\nWARNING: Duplicate IDs: {dupes}")

    # Check composite_of references
    all_id_set = set(all_ids)
    for item in items:
        if 'composite_of' in item:
            missing = [ref for ref in item['composite_of'] if ref not in all_id_set]
            if missing:
                print(f"WARNING: {item['id']} references missing IDs: {missing}")

    # Show a sample verse
    print(f"\nSample verse (isha-v01):")
    for item in items:
        if item['id'] == 'isha-v01':
            print(f"  Name: {item['name']}")
            print(f"  Verse: {item['sections']['Verse'][:120]}...")
            if 'Commentary' in item['sections']:
                print(f"  Commentary: {item['sections']['Commentary'][:120]}...")
            break
