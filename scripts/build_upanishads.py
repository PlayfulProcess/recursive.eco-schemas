#!/usr/bin/env python3
"""
Parser for The Upanishads (Swami Paramananda translation, Gutenberg #3283).

Parses three Upanishads — Isha, Katha, Kena — into a grammar.json with:
  L1: Individual verses (with verse text and commentary separated)
  L2: Per-Upanishad groups + per-part groups (for Katha/Kena) + thematic cross-groups
  L3: Meta-categories connecting L2 groups
"""

import json
import re
import sys
from pathlib import Path

SEEDS_DIR = Path(__file__).parent.parent / "seeds"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "upanishads"

ROMAN_MAP = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7,
    'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12, 'XIII': 13,
    'XIV': 14, 'XV': 15, 'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19,
    'XX': 20, 'XXI': 21, 'XXII': 22, 'XXIII': 23, 'XXIV': 24, 'XXV': 25,
    'XXVI': 26, 'XXVII': 27, 'XXVIII': 28, 'XXIX': 29
}


def read_seed():
    """Read the seed file and strip Gutenberg header/footer."""
    path = SEEDS_DIR / "upanishads.txt"
    text = path.read_text(encoding="utf-8")

    # Strip Gutenberg header
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE UPANISHADS ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE UPANISHADS ***"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def find_upanishad_sections(text):
    """Split text into the three Upanishads plus their introductions."""
    # The Upanishad names appear in the table of contents first, then as actual
    # section headers later. We need to skip the TOC (which is near the top).
    # Strategy: skip past "Introduction" section, then find the Upanishad names.
    # The Introduction section ends before the first actual Isa-Upanishad section.

    import re

    # Find ALL occurrences and use the ones after the TOC
    # The TOC lists them on consecutive lines near position ~2600
    # The actual sections start much later (after the Introduction text)
    # Skip past "Paramananda" signature which ends the Introduction
    intro_end = text.find("Paramananda\n")
    if intro_end == -1:
        intro_end = 5000  # fallback: skip first 5000 chars to get past TOC+intro
    else:
        intro_end += len("Paramananda\n")

    # Find first occurrence of each after the introduction
    isa_start = text.find("Isa-Upanishad", intro_end)
    # Find first occurrence of Katha after Isa section
    katha_start = text.find("Katha-Upanishad", isa_start + 100)
    # Find first occurrence of Kena after Katha section
    kena_start = text.find("Kena-Upanishad", katha_start + 100)

    # Isa section: from Isa to Katha
    isa_text = text[isa_start:katha_start].strip()
    # Katha section: from Katha to Kena
    katha_text = text[katha_start:kena_start].strip()
    # Kena section: from Kena to end
    kena_text = text[kena_start:].strip()

    return {
        'isha': isa_text,
        'katha': katha_text,
        'kena': kena_text,
    }


def parse_verses_from_section(section_text, has_parts=False):
    """
    Parse roman-numeral verses from a section of text.
    Returns list of dicts with verse_num, part (if applicable), verse_text, commentary.
    """
    if has_parts:
        parts = split_into_parts(section_text)
        verses = []
        for part_num, part_text in parts.items():
            part_verses = extract_verses(part_text, part_num)
            verses.extend(part_verses)
        return verses
    else:
        return extract_verses(section_text, part_num=None)


def split_into_parts(text):
    """Split Katha/Kena text into parts."""
    parts = {}
    part_names = {
        'First': 1, 'Second': 2, 'Third': 3, 'Fourth': 4,
        'Fifth': 5, 'Sixth': 6, 'fourth': 4,
    }

    # Only match Part headers that appear as standalone centered lines
    # (preceded by newline + whitespace, not embedded in commentary text)
    part_pattern = re.compile(r'^\s{10,}Part\s+(First|Second|Third|Fourth|Fifth|Sixth|fourth)\s*$', re.IGNORECASE | re.MULTILINE)
    matches = list(part_pattern.finditer(text))

    for i, match in enumerate(matches):
        part_name = match.group(1)
        part_num = part_names.get(part_name, part_names.get(part_name.capitalize(), 0))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        parts[part_num] = text[start:end]

    return parts


def extract_verses(text, part_num):
    """Extract individual verses from a chunk of text."""
    lines = text.split('\n')
    verses = []

    verse_starts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in ROMAN_MAP:
            verse_starts.append((i, ROMAN_MAP[stripped]))

    for idx, (line_idx, verse_num) in enumerate(verse_starts):
        end_idx = verse_starts[idx + 1][0] if idx + 1 < len(verse_starts) else len(lines)
        verse_lines = lines[line_idx + 1:end_idx]

        full_text = '\n'.join(verse_lines).strip()
        paragraphs = re.split(r'\n\s*\n', full_text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        if not paragraphs:
            continue

        # First paragraph is the verse text, rest is commentary
        verse_text = clean_text(paragraphs[0])
        commentary = ""
        if len(paragraphs) > 1:
            commentary = clean_text('\n\n'.join(paragraphs[1:]))

        verses.append({
            'part': part_num,
            'verse_num': verse_num,
            'verse_text': verse_text,
            'commentary': commentary,
        })

    return verses


def clean_text(text):
    """Clean up text: normalize whitespace, join wrapped lines."""
    paragraphs = re.split(r'\n\s*\n', text)
    cleaned_paragraphs = []
    for p in paragraphs:
        joined = ' '.join(line.strip() for line in p.split('\n') if line.strip())
        joined = re.sub(r'  +', ' ', joined)
        cleaned_paragraphs.append(joined)
    return '\n\n'.join(cleaned_paragraphs)


def extract_peace_chant(text):
    """Extract the Peace Chant from an Upanishad section."""
    pc_start = text.find("Peace Chant")
    if pc_start == -1:
        return None

    lines = text[pc_start:].split('\n')
    chant_lines = []
    started = False
    for line in lines:
        stripped = line.strip()
        if stripped == "Peace Chant":
            started = True
            continue
        if started:
            if stripped in ROMAN_MAP:
                break
            chant_lines.append(line)

    chant_text = '\n'.join(chant_lines).strip()
    paragraphs = re.split(r'\n\s*\n', chant_text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    verse = clean_text(paragraphs[0]) if paragraphs else ""
    commentary = clean_text('\n\n'.join(paragraphs[1:])) if len(paragraphs) > 1 else ""

    return {'verse_text': verse, 'commentary': commentary}


def extract_keywords(text):
    """Extract keywords from verse text."""
    keyword_terms = {
        'Brahman': 'brahman', 'Atman': 'atman', 'Self': 'self',
        'Prana': 'prana', 'Purusha': 'purusha', 'Aum': 'aum',
        'OM': 'om', 'Yoga': 'yoga', 'Karma': 'karma',
        'immortal': 'immortality', 'death': 'death', 'Soul': 'soul',
        'Nachiketas': 'nachiketas', 'Yama': 'yama',
        'Vidya': 'vidya', 'Avidya': 'avidya',
        'meditation': 'meditation', 'knowledge': 'knowledge',
        'ignorance': 'ignorance', 'wisdom': 'wisdom',
        'senses': 'senses', 'mind': 'mind', 'intellect': 'intellect',
        'Devas': 'devas', 'Agni': 'agni', 'Vayu': 'vayu',
        'Indra': 'indra', 'Uma': 'uma',
        'liberation': 'liberation', 'bliss': 'bliss',
        'desire': 'desire', 'renunciation': 'renunciation',
        'oneness': 'oneness', 'unity': 'unity',
    }
    keywords = []
    for term, kw in keyword_terms.items():
        if term in text:
            keywords.append(kw)
    return sorted(set(keywords))


def build_grammar():
    """Build the complete grammar."""
    text = read_seed()
    sections = find_upanishad_sections(text)

    items = []
    sort_order = 1

    # Track all L1 IDs per Upanishad and per part for L2 grouping
    isha_ids = []
    katha_ids = {}  # part_num -> [ids]
    kena_ids = {}   # part_num -> [ids]
    all_l1_ids = []

    # =========================================================================
    # ISHA UPANISHAD
    # =========================================================================
    isha_text = sections['isha']

    # Peace Chant
    pc = extract_peace_chant(isha_text)
    if pc:
        item_id = "isha-peace-chant"
        sections_dict = {"Verse": pc['verse_text']}
        if pc['commentary']:
            sections_dict["Commentary"] = pc['commentary']
        items.append({
            "id": item_id,
            "name": "Isha Upanishad: Peace Chant",
            "sort_order": sort_order,
            "category": "isha",
            "level": 1,
            "sections": sections_dict,
            "keywords": extract_keywords(pc['verse_text']),
            "metadata": {"upanishad": "Isha", "section": "Peace Chant"}
        })
        isha_ids.append(item_id)
        all_l1_ids.append(item_id)
        sort_order += 1

    # Verses
    isha_verses = parse_verses_from_section(isha_text, has_parts=False)
    for v in isha_verses:
        vnum = v['verse_num']
        item_id = f"isha-v{vnum:02d}"
        name = f"Isha Upanishad: Verse {vnum}"

        sections_dict = {"Verse": v['verse_text']}
        if v['commentary']:
            sections_dict["Commentary"] = v['commentary']

        items.append({
            "id": item_id,
            "name": name,
            "sort_order": sort_order,
            "category": "isha",
            "level": 1,
            "sections": sections_dict,
            "keywords": extract_keywords(v['verse_text'] + ' ' + v.get('commentary', '')),
            "metadata": {
                "upanishad": "Isha",
                "verse_number": vnum,
            }
        })
        isha_ids.append(item_id)
        all_l1_ids.append(item_id)
        sort_order += 1

    # =========================================================================
    # KATHA UPANISHAD
    # =========================================================================
    katha_text = sections['katha']

    # Peace Chant
    pc = extract_peace_chant(katha_text)
    if pc:
        item_id = "katha-peace-chant"
        sections_dict = {"Verse": pc['verse_text']}
        if pc['commentary']:
            sections_dict["Commentary"] = pc['commentary']
        items.append({
            "id": item_id,
            "name": "Katha Upanishad: Peace Chant",
            "sort_order": sort_order,
            "category": "katha",
            "level": 1,
            "sections": sections_dict,
            "keywords": extract_keywords(pc['verse_text']),
            "metadata": {"upanishad": "Katha", "section": "Peace Chant"}
        })
        katha_ids.setdefault(0, []).append(item_id)
        all_l1_ids.append(item_id)
        sort_order += 1

    # Verses by part
    katha_verses = parse_verses_from_section(katha_text, has_parts=True)
    for v in katha_verses:
        pnum = v['part']
        vnum = v['verse_num']
        item_id = f"katha-{pnum}-{vnum:02d}"
        name = f"Katha Upanishad Part {pnum}: Verse {vnum}"

        sections_dict = {"Verse": v['verse_text']}
        if v['commentary']:
            sections_dict["Commentary"] = v['commentary']

        items.append({
            "id": item_id,
            "name": name,
            "sort_order": sort_order,
            "category": "katha",
            "level": 1,
            "sections": sections_dict,
            "keywords": extract_keywords(v['verse_text'] + ' ' + v.get('commentary', '')),
            "metadata": {
                "upanishad": "Katha",
                "part": pnum,
                "verse_number": vnum,
            }
        })
        katha_ids.setdefault(pnum, []).append(item_id)
        all_l1_ids.append(item_id)
        sort_order += 1

    # =========================================================================
    # KENA UPANISHAD
    # =========================================================================
    kena_text = sections['kena']

    # Peace Chant
    pc = extract_peace_chant(kena_text)
    if pc:
        item_id = "kena-peace-chant"
        sections_dict = {"Verse": pc['verse_text']}
        if pc['commentary']:
            sections_dict["Commentary"] = pc['commentary']
        items.append({
            "id": item_id,
            "name": "Kena Upanishad: Peace Chant",
            "sort_order": sort_order,
            "category": "kena",
            "level": 1,
            "sections": sections_dict,
            "keywords": extract_keywords(pc['verse_text']),
            "metadata": {"upanishad": "Kena", "section": "Peace Chant"}
        })
        kena_ids.setdefault(0, []).append(item_id)
        all_l1_ids.append(item_id)
        sort_order += 1

    # Verses by part
    kena_verses = parse_verses_from_section(kena_text, has_parts=True)
    for v in kena_verses:
        pnum = v['part']
        vnum = v['verse_num']
        item_id = f"kena-{pnum}-{vnum:02d}"
        name = f"Kena Upanishad Part {pnum}: Verse {vnum}"

        sections_dict = {"Verse": v['verse_text']}
        if v['commentary']:
            sections_dict["Commentary"] = v['commentary']

        items.append({
            "id": item_id,
            "name": name,
            "sort_order": sort_order,
            "category": "kena",
            "level": 1,
            "sections": sections_dict,
            "keywords": extract_keywords(v['verse_text'] + ' ' + v.get('commentary', '')),
            "metadata": {
                "upanishad": "Kena",
                "part": pnum,
                "verse_number": vnum,
            }
        })
        kena_ids.setdefault(pnum, []).append(item_id)
        all_l1_ids.append(item_id)
        sort_order += 1

    # =========================================================================
    # L2 EMERGENCE: Per-Upanishad groups
    # =========================================================================
    l2_upanishad_ids = []

    # Isha Upanishad group
    item_id = "l2-isha"
    items.append({
        "id": item_id,
        "name": "The Isha Upanishad",
        "sort_order": sort_order,
        "category": "upanishad-group",
        "level": 2,
        "composite_of": isha_ids,
        "relationship_type": "emergence",
        "sections": {
            "About": "The Isha Upanishad (also Isha-Vasya, 'God-covered') opens with the radical declaration that everything in the universe should be 'covered by the Lord.' In just 18 verses it presents the complete Vedantic teaching: the identity of Brahman and Atman, the reconciliation of knowledge and action, the transcendence of duality. It forms the closing chapter of the Shukla Yajur-Veda and is considered one of the most concise and powerful expressions of non-dual philosophy.",
            "For Readers": "Begin with verses I and VI-VII for the core teaching of oneness. Read verses IX-XIV for the profound reconciliation of knowledge (Vidya) and ignorance (Avidya) — a teaching that transcends all binary thinking. The final prayer (XVIII) is one of the most beautiful in all sacred literature."
        },
        "keywords": ["brahman", "atman", "oneness", "vidya", "avidya", "renunciation", "non-dual"],
        "metadata": {"upanishad": "Isha", "verse_count": len(isha_ids)}
    })
    l2_upanishad_ids.append(item_id)
    sort_order += 1

    # Katha Upanishad group
    all_katha_l1 = []
    for part_ids in katha_ids.values():
        all_katha_l1.extend(part_ids)

    item_id = "l2-katha"
    items.append({
        "id": item_id,
        "name": "The Katha Upanishad",
        "sort_order": sort_order,
        "category": "upanishad-group",
        "level": 2,
        "composite_of": all_katha_l1,
        "relationship_type": "emergence",
        "sections": {
            "About": "The Katha Upanishad presents a dramatic dialogue between the boy Nachiketas and Yama, the Ruler of Death. After his father rashly gives him to Death, Nachiketas waits three days at Death's door and earns three boons. He uses the third to ask the ultimate question: what happens after death? Yama's answer unfolds across six parts, progressing from the distinction between the pleasant and the good, through the famous chariot metaphor of the Self, to the nature of Brahman, Yoga, and the path to immortality. It is the most widely known and frequently translated of all Upanishads.",
            "For Readers": "Part 1 tells the dramatic story — read it as narrative. Parts 2-3 contain the core philosophical teaching, including the chariot metaphor (Part 3, verses III-IV) and the great exhortation 'Arise! Awake!' (Part 3, verse XIV). Parts 4-6 deepen the meditation on Brahman and culminate in the practical teaching of Yoga and liberation."
        },
        "keywords": ["nachiketas", "yama", "death", "immortality", "self", "yoga", "chariot", "brahman"],
        "metadata": {"upanishad": "Katha", "verse_count": len(all_katha_l1), "parts": 6}
    })
    l2_upanishad_ids.append(item_id)
    sort_order += 1

    # Kena Upanishad group
    all_kena_l1 = []
    for part_ids in kena_ids.values():
        all_kena_l1.extend(part_ids)

    item_id = "l2-kena"
    items.append({
        "id": item_id,
        "name": "The Kena Upanishad",
        "sort_order": sort_order,
        "category": "upanishad-group",
        "level": 2,
        "composite_of": all_kena_l1,
        "relationship_type": "emergence",
        "sections": {
            "About": "The Kena Upanishad ('By whom?') is the most analytical and metaphysical of the three, opening with the fundamental inquiry: By whom directed does the mind go forth? What power enables speech, sight, hearing? The answer leads to the profound teaching that Brahman is 'the ear of the ear, the mind of the mind' — the invisible power behind all faculties. Parts 3-4 present the famous parable of the Devas and Brahman, where even the gods of Fire, Wind, and Lightning discover they have no power independent of the Absolute.",
            "For Readers": "Parts 1-2 are the philosophical core — pure inquiry into the nature of consciousness and knowing. The paradox of Part 2 ('He who thinks he knows It not, knows It') is one of the deepest statements in all philosophy. Parts 3-4 tell the vivid parable of Brahman humbling the gods — a story that makes the abstract teaching concrete."
        },
        "keywords": ["brahman", "consciousness", "knowledge", "devas", "agni", "vayu", "indra", "uma"],
        "metadata": {"upanishad": "Kena", "verse_count": len(all_kena_l1), "parts": 4}
    })
    l2_upanishad_ids.append(item_id)
    sort_order += 1

    # =========================================================================
    # L2 EMERGENCE: Katha Parts
    # =========================================================================
    l2_katha_part_ids = []
    katha_part_descriptions = {
        1: ("The Story of Nachiketas", "The dramatic origin story: Nachiketas questions his father's hollow sacrifice, is sent to Death, waits three days, and earns three boons. His third request — to know what happens after death — sets the stage for the deepest teaching.", "Read this as a story of courage and spiritual aspiration. A boy's innocent questioning leads to the most profound dialogue in Indian philosophy."),
        2: ("The Good and the Pleasant", "Yama begins his teaching with the fundamental distinction between the good (shreyas) and the pleasant (preyas). He praises Nachiketas for choosing wisdom over wealth, then reveals the sacred syllable AUM and the nature of the eternal, unborn Self.", "This part contains the foundational choice every seeker faces. Verses XVIII-XIX ('This Self is never born, nor does It die') are among the most quoted passages in all Vedantic literature."),
        3: ("The Chariot of the Self", "The famous chariot metaphor: the Self is the lord, the body is the chariot, intellect is the driver, mind is the reins, senses are the horses. Yama traces the hierarchy from senses to the Absolute, culminating in the great call: 'Arise! Awake!'", "The chariot metaphor (verses III-IX) is one of the most practical spiritual teachings ever given. Verse XIV ('Arise! Awake!') is the clarion call of the Upanishads."),
        4: ("This Verily Is That", "The teaching deepens: the Self is the perceiver behind all perception, present in waking and dream. Through the refrain 'This verily is That,' Yama shows Brahman as the single reality underlying all experience.", "Notice the repeated refrain 'This verily is That' — each verse reveals another face of the same truth. The image of pure water poured into pure water (verse XV) is unforgettable."),
        5: ("The Cosmic Self", "The body as a city with eleven gates, the Self as fire and air taking many forms, the one Ruler who makes the one form manifold. Culminates in the sublime declaration: 'The sun does not shine there, nor the moon, nor the stars.'", "Verse XV ('The sun does not shine there...') appears in multiple Upanishads and is considered one of the most luminous passages in all sacred literature."),
        6: ("The Tree of Eternity and Liberation", "The final teaching: the inverted tree of creation rooted in Brahman, the practical path of Yoga (firm holding back of the senses), and the culmination — Nachiketas attains Brahman and becomes free from impurity and death.", "This is the practical culmination. Verse XI defines Yoga. Verse XIV ('When all desires dwelling in the heart cease...') gives the condition for liberation. The story ends with Nachiketas achieving what he sought."),
    }

    for pnum in sorted(katha_ids.keys()):
        if pnum == 0:
            continue  # peace chant, not a separate part
        part_l1_ids = list(katha_ids[pnum])
        # Include peace chant in part 1
        if pnum == 1 and 0 in katha_ids:
            part_l1_ids = katha_ids[0] + part_l1_ids

        title, about, for_readers = katha_part_descriptions.get(pnum, (f"Part {pnum}", "", ""))
        item_id = f"l2-katha-part-{pnum}"
        items.append({
            "id": item_id,
            "name": f"Katha Upanishad: {title}",
            "sort_order": sort_order,
            "category": "katha-part",
            "level": 2,
            "composite_of": part_l1_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": about,
                "For Readers": for_readers,
            },
            "keywords": extract_keywords(about),
            "metadata": {"upanishad": "Katha", "part": pnum}
        })
        l2_katha_part_ids.append(item_id)
        sort_order += 1

    # =========================================================================
    # L2 EMERGENCE: Kena Parts
    # =========================================================================
    l2_kena_part_ids = []
    kena_part_descriptions = {
        1: ("The Inquiry: By Whom?", "The disciple asks the fundamental question: By whom directed does the mind think? The teacher answers: Brahman is 'the ear of the ear, the mind of the mind' — the invisible power behind all perception. Yet It cannot be reached by eye, speech, or mind.", "These eight verses are pure philosophical inquiry at its finest. Each verse strips away another layer of assumption about what we think we know."),
        2: ("The Paradox of Knowing", "The teacher warns against thinking one 'knows' Brahman through intellect alone. The disciple, after meditation, arrives at the profound paradox: 'I do not think I know It well, nor do I think that I do not know It.' True knowledge of the Infinite transcends ordinary knowing.", "Part 2 contains one of the deepest paradoxes in all philosophy. Sit with verse III: 'He who thinks he knows It not, knows It. He who thinks he knows It, knows It not.'"),
        3: ("The Parable of the Devas and Brahman", "Brahman wins a victory for the gods, but they claim the glory as their own. To teach them humility, Brahman appears as a mysterious spirit. Fire cannot burn a straw before It; Wind cannot blow it away. Only when Uma (Divine Wisdom) appears does Indra recognize the truth.", "This is one of the great parables of world literature. The image of the all-powerful gods unable to burn or blow away a single straw before Brahman is both humorous and profound."),
        4: ("Recognition and Practice", "Uma reveals to Indra that the mysterious spirit was Brahman. The teaching is summarized: Brahman flashes like lightning, appears and disappears like the winking of an eye. The Upanishad concludes with the practical foundation: tapas (self-discipline), dama (sense-control), karma (right action), and Truth.", "The final part grounds the metaphysical teaching in practice. Verses VII-IX give the concrete path: self-discipline, sense-control, right action, and Truth as the ultimate support."),
    }

    for pnum in sorted(kena_ids.keys()):
        if pnum == 0:
            continue
        part_l1_ids = list(kena_ids[pnum])
        if pnum == 1 and 0 in kena_ids:
            part_l1_ids = kena_ids[0] + part_l1_ids

        title, about, for_readers = kena_part_descriptions.get(pnum, (f"Part {pnum}", "", ""))
        item_id = f"l2-kena-part-{pnum}"
        items.append({
            "id": item_id,
            "name": f"Kena Upanishad: {title}",
            "sort_order": sort_order,
            "category": "kena-part",
            "level": 2,
            "composite_of": part_l1_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": about,
                "For Readers": for_readers,
            },
            "keywords": extract_keywords(about),
            "metadata": {"upanishad": "Kena", "part": pnum}
        })
        l2_kena_part_ids.append(item_id)
        sort_order += 1

    # =========================================================================
    # L2 EMERGENCE: Thematic cross-Upanishad groups
    # =========================================================================
    l2_thematic_ids = []

    # Theme: Nature of Brahman/Atman (identity of Self and God)
    brahman_verses = []
    for item in items:
        if item['level'] == 1 and any(k in item.get('keywords', [])
                                       for k in ['brahman', 'atman', 'self', 'purusha']):
            brahman_verses.append(item['id'])

    item_id = "l2-theme-brahman-atman"
    items.append({
        "id": item_id,
        "name": "Theme: The Nature of Brahman and Atman",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "composite_of": brahman_verses,
        "relationship_type": "emergence",
        "sections": {
            "About": "The central teaching of the Upanishads is the identity of Brahman (the Absolute, ultimate reality) and Atman (the individual Self). 'Tat tvam asi' — That thou art. These verses explore what Brahman is, what the Self is, and how they are one and the same. From the Isha's declaration that all is covered by the Lord, through the Katha's progressive unveiling of the Self beyond senses and mind, to the Kena's inquiry into the power behind all perception — the teaching converges on one truth: there is only One.",
            "For Readers": "Read these verses as a progressive revelation. The Isha states the truth directly. The Katha reveals it through dialogue and metaphor. The Kena approaches it through philosophical inquiry. Together they offer multiple doorways into the same realization."
        },
        "keywords": ["brahman", "atman", "self", "oneness", "non-dual", "identity"],
        "metadata": {"theme": "brahman-atman", "verse_count": len(brahman_verses)}
    })
    l2_thematic_ids.append(item_id)
    sort_order += 1

    # Theme: Death and Immortality
    death_verses = []
    for item in items:
        if item['level'] == 1 and any(k in item.get('keywords', [])
                                       for k in ['death', 'immortality']):
            death_verses.append(item['id'])

    item_id = "l2-theme-death-immortality"
    items.append({
        "id": item_id,
        "name": "Theme: Death and Immortality",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "composite_of": death_verses,
        "relationship_type": "emergence",
        "sections": {
            "About": "The question that drives Nachiketas to the Ruler of Death is humanity's oldest question: what happens when we die? The Upanishads' answer is radical: death is real only for the body; the Self is never born and never dies. Immortality is not a future state but a present realization — the recognition of one's identity with the deathless Brahman. These verses trace the teaching from the Isha's warning about 'killing the Self' through the Katha's complete journey with Death to the Kena's teaching that the wise become immortal by knowing the Self.",
            "For Readers": "The Katha Upanishad is the essential text here — it is literally a conversation with Death. Start with Part 1 for the story, then Part 2, verses XVIII-XIX for the core statement. The Isha (verse III) and Kena (Part 1, verse II) add complementary perspectives."
        },
        "keywords": ["death", "immortality", "nachiketas", "yama", "liberation"],
        "metadata": {"theme": "death-immortality", "verse_count": len(death_verses)}
    })
    l2_thematic_ids.append(item_id)
    sort_order += 1

    # Theme: The Path of Knowledge vs. the Path of Pleasure
    path_verses = []
    for item in items:
        if item['level'] == 1:
            text_combined = ' '.join(item.get('sections', {}).values())
            if any(term in text_combined for term in ['pleasant', 'good', 'Vidya', 'Avidya', 'ignorance', 'desire', 'discrimination']):
                if any(k in item.get('keywords', []) for k in ['wisdom', 'knowledge', 'ignorance', 'desire', 'vidya', 'avidya']):
                    path_verses.append(item['id'])

    item_id = "l2-theme-knowledge-pleasure"
    items.append({
        "id": item_id,
        "name": "Theme: Knowledge vs. Pleasure",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "composite_of": path_verses,
        "relationship_type": "emergence",
        "sections": {
            "About": "A persistent teaching across all three Upanishads: the path of the good (shreyas) and the path of the pleasant (preyas) lead in opposite directions. The Isha reconciles knowledge and works. The Katha's Yama teaches that the wise choose the good over the pleasant. The Kena warns that thinking one 'knows' Brahman through intellect alone is itself a form of ignorance. True discrimination (viveka) is the faculty that distinguishes the real from the unreal.",
            "For Readers": "The Katha's Part 2 (verses I-VI) gives the clearest statement. The Isha's verses IX-XIV offer a subtler teaching about integrating apparent opposites. The Kena's Part 2 adds the paradox that even 'knowing' can become an obstacle."
        },
        "keywords": ["wisdom", "knowledge", "ignorance", "desire", "discrimination", "vidya", "avidya"],
        "metadata": {"theme": "knowledge-pleasure", "verse_count": len(path_verses)}
    })
    l2_thematic_ids.append(item_id)
    sort_order += 1

    # Theme: Yoga and Practice
    yoga_verses = []
    for item in items:
        if item['level'] == 1:
            text_combined = ' '.join(item.get('sections', {}).values())
            if any(term in text_combined for term in ['Yoga', 'senses', 'control', 'meditation', 'chariot', 'reins', 'horses']):
                if any(k in item.get('keywords', []) for k in ['yoga', 'senses', 'mind', 'meditation', 'intellect']):
                    yoga_verses.append(item['id'])

    item_id = "l2-theme-yoga-practice"
    items.append({
        "id": item_id,
        "name": "Theme: Yoga and the Mastery of the Senses",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "composite_of": yoga_verses,
        "relationship_type": "emergence",
        "sections": {
            "About": "The Upanishads do not merely philosophize — they prescribe a path. The Katha Upanishad contains one of the earliest definitions of Yoga ('the firm holding back of the senses') and the famous chariot metaphor: the Self as lord, body as chariot, intellect as driver, mind as reins, senses as horses. The Kena Upanishad adds the practical foundation: tapas (self-discipline), dama (sense-control), and karma (right action). These verses map the inner technology of liberation.",
            "For Readers": "Start with the chariot metaphor (Katha Part 3, verses III-IX) — it is the most vivid and practical image. Then read Katha Part 6, verses X-XI for the definition of Yoga. The Kena's final verses (Part 4, VIII-IX) ground everything in daily practice."
        },
        "keywords": ["yoga", "senses", "mind", "meditation", "intellect", "chariot", "discipline"],
        "metadata": {"theme": "yoga-practice", "verse_count": len(yoga_verses)}
    })
    l2_thematic_ids.append(item_id)
    sort_order += 1

    # Theme: The Limits of Knowledge and Language
    limits_verses = []
    for item in items:
        if item['level'] == 1:
            text_combined = ' '.join(item.get('sections', {}).values())
            if any(term in text_combined for term in ['cannot be known', 'beyond', 'unknow', 'speech does not', 'eye does not', 'not seen', 'not heard']):
                limits_verses.append(item['id'])

    item_id = "l2-theme-beyond-words"
    items.append({
        "id": item_id,
        "name": "Theme: Beyond Words and Mind",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "composite_of": limits_verses,
        "relationship_type": "emergence",
        "sections": {
            "About": "The Upanishads repeatedly insist that ultimate reality cannot be captured by language, thought, or sensory perception. The Kena Upanishad builds its entire first part on this theme: 'There the eye does not go, nor speech, nor mind.' The Katha teaches that the Self is 'subtler than the subtle.' These verses point toward a mode of knowing that transcends the intellect — what the tradition calls prajna or direct spiritual perception.",
            "For Readers": "The Kena's Part 1 (verses III-VIII) is the purest expression of this theme. Pair it with Katha Part 2, verse VIII ('subtler than the subtle') and Part 3, verse XII. Notice how the texts use language to point beyond language — a profound paradox that anticipates Wittgenstein by millennia."
        },
        "keywords": ["knowledge", "mind", "brahman", "ineffable", "beyond"],
        "metadata": {"theme": "beyond-words", "verse_count": len(limits_verses)}
    })
    l2_thematic_ids.append(item_id)
    sort_order += 1

    # =========================================================================
    # L3 META-CATEGORIES
    # =========================================================================

    # L3: The Three Upanishads
    item_id = "l3-three-upanishads"
    items.append({
        "id": item_id,
        "name": "The Three Upanishads",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": l2_upanishad_ids + l2_katha_part_ids + l2_kena_part_ids,
        "relationship_type": "emergence",
        "sections": {
            "About": "Three Upanishads, three approaches to the same truth. The Isha is direct proclamation: 18 verses that state the non-dual truth with the force of revelation. The Katha is dramatic dialogue: a boy confronts Death and receives the complete teaching through story, metaphor, and progressive revelation across six parts. The Kena is philosophical inquiry: questions that strip away every assumption until only Brahman remains. Together they form a complete spiritual education — from declaration to narrative to analysis, from 'All this is covered by the Lord' to 'He who knows this becomes established in the highest abode of Brahman.'",
            "For Readers": "If you are new to the Upanishads, start with the Katha — its story structure makes the philosophy accessible. Move to the Isha for the most concentrated statement of the teaching. Then approach the Kena for the deepest philosophical inquiry. Each reading will illuminate the others."
        },
        "keywords": ["upanishads", "vedanta", "brahman", "atman", "non-dual", "wisdom"],
        "metadata": {"upanishad_count": 3}
    })
    sort_order += 1

    # L3: Thematic Threads
    item_id = "l3-thematic-threads"
    items.append({
        "id": item_id,
        "name": "Thematic Threads Across the Upanishads",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": l2_thematic_ids,
        "relationship_type": "emergence",
        "sections": {
            "About": "Five great themes weave through all three Upanishads like threads in a tapestry: the nature of Brahman and Atman, death and immortality, knowledge versus pleasure, yoga and practice, and the limits of language and thought. Each Upanishad addresses all these themes but emphasizes different facets. Following a single thread across all three texts reveals how the same truth can be approached from multiple angles — and how the Vedantic vision holds together as a unified whole.",
            "For Readers": "Choose the theme that calls to you most strongly and follow it across all three Upanishads. The themes are not separate teachings but different faces of one diamond. If you are drawn to questions of mortality, start with Death and Immortality. If philosophical paradox intrigues you, start with Beyond Words and Mind. Each thread leads to the same center."
        },
        "keywords": ["themes", "vedanta", "brahman", "death", "yoga", "knowledge"],
        "metadata": {"theme_count": len(l2_thematic_ids)}
    })
    sort_order += 1

    # =========================================================================
    # BUILD GRAMMAR
    # =========================================================================
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Anonymous (Vedic sages)",
                    "date": "~800-200 BCE",
                    "note": "Original authors"
                },
                {
                    "name": "Swami Paramananda",
                    "date": "1919",
                    "note": "Translator and commentator"
                }
            ]
        },
        "name": "The Upanishads",
        "description": (
            "Three principal Upanishads — Isha, Katha, and Kena — translated from Sanskrit by "
            "Swami Paramananda (1919). The Upanishads ('sitting near the teacher') are the "
            "philosophical conclusion of the Vedas, exploring the nature of Brahman (ultimate reality), "
            "Atman (the Self), and their identity. These texts are the fountainhead of Vedanta philosophy "
            "and the deepest roots of yoga, meditation, and non-dual awareness. Each verse is presented "
            "with Paramananda's commentary.\n\n"
            "Source: Project Gutenberg eBook #3283 (https://www.gutenberg.org/ebooks/3283)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Rajput miniature paintings of sages and forest "
            "ashrams from the 17th-18th centuries. Illustrations from early 20th century Vedanta Society "
            "publications. Traditional Indian manuscript illuminations depicting scenes of guru-disciple "
            "teaching in forest settings."
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["upanishads", "hindu", "vedanta", "sacred-text", "philosophy"],
        "roots": ["eastern-wisdom", "mysticism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei", "Akomolafe"],
        "worldview": "non-dual",
        "items": items,
    }

    # Fix sort_order to be sequential starting at 1
    for i, item in enumerate(grammar['items']):
        item['sort_order'] = i + 1

    return grammar


def main():
    grammar = build_grammar()

    # Stats
    levels = {}
    for item in grammar['items']:
        lvl = item['level']
        levels[lvl] = levels.get(lvl, 0) + 1

    print(f"Built Upanishads grammar:")
    print(f"  Total items: {len(grammar['items'])}")
    for lvl in sorted(levels):
        print(f"  L{lvl}: {levels[lvl]}")

    # Verify no duplicate IDs
    ids = [item['id'] for item in grammar['items']]
    dupes = [x for x in ids if ids.count(x) > 1]
    if dupes:
        print(f"  WARNING: Duplicate IDs: {set(dupes)}")

    # Verify composite_of references
    id_set = set(ids)
    for item in grammar['items']:
        for ref in item.get('composite_of', []):
            if ref not in id_set:
                print(f"  WARNING: {item['id']} references missing ID: {ref}")

    # Write output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "grammar.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"\nWritten to {output_path}")


if __name__ == '__main__':
    main()
