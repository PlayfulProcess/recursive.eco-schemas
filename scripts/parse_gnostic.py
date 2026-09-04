#!/usr/bin/env python3
"""
Parser for two Gnostic texts:
1. The Gnosis of the Light (Codex Brucianus) by F. Lamplugh - Gutenberg #30799
2. The Gnostic Crucifixion by G.R.S. Mead - Gutenberg #35735

Both are short texts with clear section structure.
"""

import json
import re
import os

TRUNCATE_LIMIT = 2800

def truncate_text(text, limit=TRUNCATE_LIMIT):
    """Truncate text at limit, finding last period before cutoff."""
    text = text.strip()
    if len(text) <= limit:
        return text
    bp = text.rfind(".", 0, limit)
    if bp == -1:
        bp = limit
    remaining_words = len(text[bp+1:].split())
    return text[:bp+1] + f" [Text continues for approximately {remaining_words} more words...]"


def extract_body(filepath):
    """Extract body text between Gutenberg markers."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1:
        raise ValueError(f"Could not find Gutenberg markers in {filepath}")
    start = text.find("\n", start) + 1
    return text[start:end].strip()


def clean_text(text):
    """Clean up whitespace in text."""
    # Normalize whitespace but preserve paragraph breaks
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        cleaned.append(line.strip())
    text = '\n'.join(cleaned)
    # Collapse multiple blank lines to double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_gnosis_of_light(seed_path):
    """Parse The Gnosis of the Light into grammar items."""
    body = extract_body(seed_path)
    body = clean_text(body)

    # Find the three major sections
    # 1. Introduction starts at "INTRODUCTION"
    # 2. Main text starts at "The Gnosis of the Light" (after CONTENTS)
    # 3. Notes start at "NOTES"

    # Find Introduction
    intro_match = re.search(r'\nINTRODUCTION\n', body)
    if not intro_match:
        raise ValueError("Could not find INTRODUCTION")

    # Find the main text - it starts with "[1]This is the Father"
    main_match = re.search(r'\nThe Gnosis of the Light\n', body)
    if not main_match:
        # Try alternate
        main_match = re.search(r'\n\[1\]This is the Father', body)
    if not main_match:
        raise ValueError("Could not find main text start")

    # Find Notes section
    notes_match = re.search(r'\nNOTES\n', body)
    if not notes_match:
        raise ValueError("Could not find NOTES section")

    # Find the footnote [1] before NOTES (end of main text)
    footnote1_match = re.search(r'\n\[1\] The title and the opening part', body)

    intro_text = body[intro_match.end():main_match.start()].strip()
    # Main text starts after "The Gnosis of the Light" heading
    main_start = body.find('\n', main_match.start() + 1)
    if footnote1_match:
        main_text = body[main_start:footnote1_match.start()].strip()
    else:
        main_text = body[main_start:notes_match.start()].strip()
    notes_text = body[notes_match.end():].strip()

    # Remove ads/publisher info at the end of notes
    printed_match = re.search(r'\nPRINTED IN GREAT BRITAIN', notes_text)
    if printed_match:
        notes_text = notes_text[:printed_match.start()].strip()

    items = []
    sort_order = 1

    # === INTRODUCTION ===
    # Split into meaningful paragraphs/sections
    # The introduction is one continuous essay. Split into thematic chunks.
    intro_paragraphs = [p.strip() for p in intro_text.split('\n\n') if p.strip()]

    # Group intro paragraphs into ~3-4 sections by theme
    # Section 1: What is Gnosis (first few paragraphs up to "The Gnostic movement began")
    # Section 2: Gnostic teaching method (from "Hence the disciple" to "sacred place")
    # Section 3: The Codex Brucianus and this work (from "The Codex Brucianus" and Schmidt quote)
    # Section 4: The spiritual body and community (from "This awakening" onward)

    # Find split points
    intro_splits = []
    current_pos = 0
    split_markers = [
        "The Gnostic movement began",
        "Hence the disciple was confronted",
        "Now this strange way of teaching",
        "This awakening of the Body of Stars",
        "I believe that the original source",
        "I think also that the original MS.",
        "It is pleasant, in these days",
    ]

    # Build intro sections by combining paragraphs
    intro_sections = []
    current_section = []
    for p in intro_paragraphs:
        started_new = False
        for marker in split_markers:
            if p.startswith(marker):
                if current_section:
                    intro_sections.append('\n\n'.join(current_section))
                current_section = [p]
                started_new = True
                break
        if not started_new:
            current_section.append(p)
    if current_section:
        intro_sections.append('\n\n'.join(current_section))

    # Merge small sections to get ~4-5 items
    merged_intro = []
    temp = []
    for s in intro_sections:
        temp.append(s)
        combined = '\n\n'.join(temp)
        if len(combined) > 1500:
            merged_intro.append(combined)
            temp = []
    if temp:
        if merged_intro:
            # Merge last small chunk with previous
            if len('\n\n'.join(temp)) < 800:
                merged_intro[-1] = merged_intro[-1] + '\n\n' + '\n\n'.join(temp)
            else:
                merged_intro.append('\n\n'.join(temp))
        else:
            merged_intro.append('\n\n'.join(temp))

    intro_titles = [
        ("intro-what-is-gnosis", "What is Gnosis?"),
        ("intro-gnostic-teaching", "The Gnostic Method of Teaching"),
        ("intro-body-of-stars", "The Body of Stars"),
        ("intro-codex-brucianus", "The Codex Brucianus"),
        ("intro-scholarly-appreciation", "Scholarly Appreciation"),
    ]

    intro_ids = []
    for i, section_text in enumerate(merged_intro):
        if i < len(intro_titles):
            item_id, item_name = intro_titles[i]
        else:
            item_id = f"intro-section-{i+1}"
            item_name = f"Introduction Part {i+1}"

        items.append({
            "id": item_id,
            "name": item_name,
            "sort_order": sort_order,
            "category": "introduction",
            "level": 1,
            "sections": {
                "Text": truncate_text(section_text)
            },
            "keywords": ["introduction", "gnosis", "gnosticism"],
            "metadata": {}
        })
        intro_ids.append(item_id)
        sort_order += 1

    # === MAIN TEXT ===
    # The main text uses numbered references [1], [2], etc. but is continuous prose.
    # Split by the paragraph numbering embedded in notes: (1), (2), etc.
    # Actually the main text is continuous - split into thematic sections.

    # Split main text into natural paragraphs
    main_paragraphs = [p.strip() for p in main_text.split('\n\n') if p.strip()]

    # Define section breaks based on content themes
    section_defs = [
        ("father-of-all", "The Father of All Fathers", ["father", "infinite", "abyss"],
         "This is the Father of all Fathers"),
        ("second-space", "The Second Space", ["logos", "cross", "ennead"],
         "The Second Space is that which is called"),
        ("twelve-deeps", "The Twelve Deeps", ["deeps", "wisdom", "mystery"],
         "The First Deep is the Universal Fount"),
        ("temple-of-pleroma", "The Temple of the Pleroma", ["temple", "pleroma", "monad"],
         "In this wise has He created the Temple"),
        ("setheus", "The Deep of Setheus", ["setheus", "paternities", "faces"],
         "Beyond all these Spaces comes the Deep of Setheus"),
        ("alone-begotten", "The Alone-Begotten Word", ["alone-begotten", "word", "dark-ray"],
         "The Alone-begotten holds in His right hand"),
        ("monad-metropolis", "The Monad as Metropolis", ["monad", "city", "crown"],
         "This is He who dwells in the Monad"),
        ("light-spark-descent", "The Descent of the Light-Spark", ["light-spark", "descent", "grace"],
         "The Indivisible Point sent the Light-Spark"),
        ("indivisible-queen", "The Indivisible Queen", ["queen", "crown", "mother"],
         "This is the Indivisible [Queen and Mother]"),
        ("immeasurable-deep", "The Immeasurable Deep", ["deep", "paternities", "powers"],
         "In each of these Enneads there is a Monad"),
        ("five-powers", "The Five Powers of the Deep", ["love", "hope", "faith", "gnosis", "peace"],
         "And in the midst of the Immeasurable Deep there are five Powers"),
        ("triple-power", "The Triple-Power and the Logos Demiourgos", ["triple-power", "logos", "demiourgos"],
         "This is the Abyss which surrounds the Temple"),
        ("robe-of-power", "The Robe of Power", ["robe", "ordering", "matter"],
         "The First Monad sent Him"),
        ("propator", "The Propator", ["propator", "father", "crown"],
         "established the Propator"),
        ("autopator", "The Autopator", ["autopator", "ennead", "initiation"],
         "she established the Autopator"),
        ("protogennetor", "The Protogennetor", ["protogennetor", "son", "matter"],
         "When the Mother established the Protogennetor"),
        ("hymn-to-boundless", "Hymn to the Boundless One", ["hymn", "prayer", "boundless"],
         "Thou alone art Boundless"),
        ("infinite-spark", "The Infinite Spark of Light", ["spark", "light", "manifestation"],
         "From Being Unbounded came forth"),
        ("lord-of-universe", "The Lord of the Universe", ["lord", "right", "left", "life", "death"],
         "The King of Glory was seated"),
        ("prayer-of-births", "The Prayer of the Births of Matter", ["prayer", "matter", "spirit"],
         "They prayed unto the Hidden Mystery"),
        ("hierarchy-established", "The Hierarchy Established", ["hierarchy", "baptism", "sophia"],
         "And He heard them and sent unto them"),
        ("hymn-to-light", "Hymn to the Light", ["hymn", "light", "praise"],
         "O Alone-begotten of Light"),
    ]

    main_text_ids = []
    remaining_text = main_text

    # Use a simpler approach: split by finding each section marker
    sections_found = []
    for item_id, name, kw, marker in section_defs:
        pos = remaining_text.find(marker)
        if pos != -1:
            sections_found.append((pos, item_id, name, kw, marker))

    sections_found.sort(key=lambda x: x[0])

    for i, (pos, item_id, name, kw, marker) in enumerate(sections_found):
        if i + 1 < len(sections_found):
            next_pos = sections_found[i+1][0]
            section_text = remaining_text[pos:next_pos].strip()
        else:
            section_text = remaining_text[pos:].strip()

        items.append({
            "id": item_id,
            "name": name,
            "sort_order": sort_order,
            "category": "gnosis-text",
            "level": 1,
            "sections": {
                "Text": truncate_text(section_text)
            },
            "keywords": kw,
            "metadata": {}
        })
        main_text_ids.append(item_id)
        sort_order += 1

    # If we found nothing, fall back to paragraph-based splitting
    if not sections_found:
        chunk = []
        chunk_num = 0
        for p in main_paragraphs:
            chunk.append(p)
            combined = '\n\n'.join(chunk)
            if len(combined) > 2000:
                chunk_num += 1
                item_id = f"gnosis-passage-{chunk_num}"
                items.append({
                    "id": item_id,
                    "name": f"Passage {chunk_num}",
                    "sort_order": sort_order,
                    "category": "gnosis-text",
                    "level": 1,
                    "sections": {"Text": truncate_text(combined)},
                    "keywords": ["gnosis", "light", "pleroma"],
                    "metadata": {}
                })
                main_text_ids.append(item_id)
                sort_order += 1
                chunk = []
        if chunk:
            chunk_num += 1
            item_id = f"gnosis-passage-{chunk_num}"
            items.append({
                "id": item_id,
                "name": f"Passage {chunk_num}",
                "sort_order": sort_order,
                "category": "gnosis-text",
                "level": 1,
                "sections": {"Text": truncate_text('\n\n'.join(chunk))},
                "keywords": ["gnosis", "light", "pleroma"],
                "metadata": {}
            })
            main_text_ids.append(item_id)
            sort_order += 1

    # === NOTES ===
    # Notes are numbered (1) through (43), each starting on its own line after a blank line
    # Most use "(N)" format but some (34, 43) use "N." format
    # Must match at start of line to avoid matching inline refs like "(1) audibly; (2) inaudibly"
    note_pattern_paren = re.compile(r'(?:^|\n\n)\((\d+)\)\s', re.MULTILINE)
    note_pattern_dot = re.compile(r'\n(\d+)\.\s\s', re.MULTILINE)

    note_positions = []
    for m in note_pattern_paren.finditer(notes_text):
        note_positions.append((m.start(), int(m.group(1))))
    for m in note_pattern_dot.finditer(notes_text):
        num = int(m.group(1))
        if num in [34, 43]:  # Known notes using this format
            note_positions.append((m.start(), num))

    note_positions.sort(key=lambda x: x[0])

    note_ids = []
    for i, (start_pos, note_num) in enumerate(note_positions):
        if i + 1 < len(note_positions):
            end_pos = note_positions[i+1][0]
        else:
            end_pos = len(notes_text)

        note_content = notes_text[start_pos:end_pos].strip()

        # Skip very short notes
        if len(note_content) < 50:
            continue

        item_id = f"note-{note_num}"
        items.append({
            "id": item_id,
            "name": f"Note {note_num}",
            "sort_order": sort_order,
            "category": "notes",
            "level": 1,
            "sections": {
                "Commentary": truncate_text(note_content)
            },
            "keywords": ["commentary", "notes", "interpretation"],
            "metadata": {}
        })
        note_ids.append(item_id)
        sort_order += 1

    # === L2: Thematic Groupings ===
    l2_items = []

    # L2: Introduction group
    l2_items.append({
        "id": "l2-introduction",
        "name": "Introduction: The Nature of Gnosis",
        "sort_order": sort_order,
        "category": "thematic-grouping",
        "level": 2,
        "composite_of": intro_ids,
        "sections": {
            "About": "Lamplugh's introduction to the Codex Brucianus, explaining the nature of Gnosis as direct knowledge of God received through contemplation, the method of symbolic teaching used by Gnostic schools, and the concept of the Body of Stars or spiritual body that is awakened through the mysteries.",
            "Key Themes": "Gnosis as direct knowledge vs. faith (Pistis); the Body of Stars and spiritual transformation; the Codex Brucianus as a second-century Egyptian mystical text; the relationship between Gnostic, Christian, and Platonic traditions."
        },
        "keywords": ["introduction", "gnosis", "pistis", "body-of-stars", "codex-brucianus"],
        "metadata": {}
    })
    sort_order += 1

    # L2: Cosmology - The Divine Hierarchy
    cosmology_ids = [mid for mid in main_text_ids if mid in
        ["father-of-all", "second-space", "twelve-deeps", "temple-of-pleroma", "setheus", "alone-begotten", "monad-metropolis"]]
    if cosmology_ids:
        l2_items.append({
            "id": "l2-divine-hierarchy",
            "name": "The Divine Hierarchy: From Father to Monad",
            "sort_order": sort_order,
            "category": "thematic-grouping",
            "level": 2,
            "composite_of": cosmology_ids,
            "sections": {
                "About": "The emanation of the divine realms from the unknowable Father through the Second Space (Logos), the Twelve Deeps, the Temple of the Pleroma, Setheus (the AEon of AEons), the Alone-Begotten Word, and the Monad. Each level of being contains and reflects all others in an infinite recursion of divine light.",
                "Key Themes": "The Father beyond all names; the Logos as Second Creator; the Twelve Deeps as universal principles (Wisdom, Mystery, Gnosis, Purity, etc.); the Temple of the Pleroma as cosmic architecture; Setheus as the manifested Sun of Eternity; the Dark Ray of the Alone-Begotten."
            },
            "keywords": ["cosmology", "emanation", "pleroma", "hierarchy", "setheus"],
            "metadata": {}
        })
        sort_order += 1

    # L2: The Light-Spark and Descent
    descent_ids = [mid for mid in main_text_ids if mid in
        ["light-spark-descent", "indivisible-queen", "five-powers", "immeasurable-deep"]]
    if descent_ids:
        l2_items.append({
            "id": "l2-light-spark",
            "name": "The Light-Spark: Descent and Crown",
            "sort_order": sort_order,
            "category": "thematic-grouping",
            "level": 2,
            "composite_of": descent_ids,
            "sections": {
                "About": "The descent of the Light-Spark from the Pleroma into the lower regions, bringing form and knowledge to those without. The Indivisible Queen (Mother) who crowns all dominion, and the Five Powers of the Immeasurable Deep: Love, Hope, Faith, Gnosis, and Peace.",
                "Key Themes": "The incarnation of divine light in matter; the captivity of the Light-Spark; the Crown of Life; the Five Powers as stages of spiritual realization; the Gate of God."
            },
            "keywords": ["light-spark", "descent", "incarnation", "five-powers", "crown"],
            "metadata": {}
        })
        sort_order += 1

    # L2: The Re-Ordering
    reorder_ids = [mid for mid in main_text_ids if mid in
        ["triple-power", "robe-of-power", "propator", "autopator", "protogennetor"]]
    if reorder_ids:
        l2_items.append({
            "id": "l2-re-ordering",
            "name": "The Re-Ordering: From Matter to Spirit",
            "sort_order": sort_order,
            "category": "thematic-grouping",
            "level": 2,
            "composite_of": reorder_ids,
            "sections": {
                "About": "The cosmic re-ordering after the descent of the Light-Spark. The Triple-Power and Logos Demiourgos establish order, the Robe of Power separates being from non-being, and three great hierarchs (Propator, Autopator, Protogennetor) are established to guide souls from matter back to spirit.",
                "Key Themes": "Separation of that-which-is from that-which-is-not; the Propator as purification; the Autopator as illumination; the Protogennetor as union; Jerusalem as the incorruptible world; the brooding over matter like a bird over eggs."
            },
            "keywords": ["re-ordering", "propator", "autopator", "protogennetor", "matter", "spirit"],
            "metadata": {}
        })
        sort_order += 1

    # L2: Hymns and Prayers
    hymn_ids = [mid for mid in main_text_ids if mid in
        ["hymn-to-boundless", "prayer-of-births", "hymn-to-light"]]
    if hymn_ids:
        l2_items.append({
            "id": "l2-hymns-prayers",
            "name": "Hymns and Prayers of the Gnosis",
            "sort_order": sort_order,
            "category": "thematic-grouping",
            "level": 2,
            "composite_of": hymn_ids,
            "sections": {
                "About": "The devotional heart of the text: the Mother's hymn to the Boundless One, the prayer of the Births of Matter for spiritual bodies, and the culminating Hymn to the Light praising the Alone-Begotten through twenty-seven invocations.",
                "Key Themes": "Divine prayer as cosmic invocation; the yearning of matter for spirit; the Mother as intercessor; the Hymn to the Light as a litany of divine attributes."
            },
            "keywords": ["hymn", "prayer", "devotion", "invocation", "light"],
            "metadata": {}
        })
        sort_order += 1

    # L2: Notes group
    if note_ids:
        l2_items.append({
            "id": "l2-notes",
            "name": "Commentary Notes by F. Lamplugh",
            "sort_order": sort_order,
            "category": "thematic-grouping",
            "level": 2,
            "composite_of": note_ids,
            "sections": {
                "About": "Lamplugh's explanatory notes illuminating the symbolism of the Gnostic text. These cover the meaning of the City/Monad, the vibratory formula IAO, the Cosmic Cross, the Temple of the Pleroma, the Dark Ray, the Star-Body (Astroeides), and the nature of Gnostic initiation.",
                "Key Themes": "Symbolism of the Cross; the IAO formula; the Body of Stars (Astroeides); the three paths of Purgation, Illumination, and Union; connections to Platonic and Hermetic traditions."
            },
            "keywords": ["commentary", "notes", "symbolism", "interpretation"],
            "metadata": {}
        })
        sort_order += 1

    items.extend(l2_items)

    # === L3: Meta-categories ===
    all_main_ids = [item["id"] for item in l2_items]

    items.append({
        "id": "l3-gnosis-of-light",
        "name": "The Gnosis of the Light: Complete Work",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": all_main_ids,
        "sections": {
            "About": "The complete Gnosis of the Light (Untitled Apocalypse) from the Codex Brucianus, with Lamplugh's introduction and notes. A second-century Gnostic masterwork describing the emanation of divine realms from the unknowable Father, the descent of the Light-Spark into matter, and the cosmic re-ordering that guides souls back to their source in the Pleroma of Light.",
            "Significance": "Schmidt called it 'a magnificently conceived work by an old Gnostic philosopher' dating to the period of Basilides and Valentinus (c. 160-200 AD). Its philosophical basis is Alexandrian Platonism, and it shows marked affinities with the Gospel of Mary. The text was likely used to prepare candidates for the 'Baptism of Light' in an Egyptian school of contemplation."
        },
        "keywords": ["gnosis", "light", "codex-brucianus", "pleroma", "gnosticism"],
        "metadata": {}
    })
    sort_order += 1

    return items


def parse_gnostic_crucifixion(seed_path):
    """Parse The Gnostic Crucifixion into grammar items."""
    body = extract_body(seed_path)
    body = clean_text(body)

    # Find the main sections
    # 1. Preface starts at "PREFACE."
    # 2. Vision of the Cross starts at "THE VISION OF THE CROSS."
    # 3. Comments starts at "COMMENTS."
    # 4. Postscript starts at "POSTCRIPT."

    preface_match = re.search(r'\nPREFACE\.\n', body)
    vision_match = re.search(r'\nTHE VISION OF THE CROSS\.\n', body)
    comments_match = re.search(r'\nCOMMENTS\.\n', body)
    postscript_match = re.search(r'\nPOSTCRIPT\.\n', body)

    if not all([preface_match, vision_match, comments_match, postscript_match]):
        raise ValueError("Could not find all section markers in Gnostic Crucifixion")

    preface_text = body[preface_match.end():vision_match.start()].strip()
    vision_text = body[vision_match.end():comments_match.start()].strip()
    comments_text = body[comments_match.end():postscript_match.start()].strip()

    # End postscript before printer info
    printed_match = re.search(r'\nPRINTED BY PERCY LUND', body)
    if printed_match:
        postscript_text = body[postscript_match.end():printed_match.start()].strip()
    else:
        postscript_text = body[postscript_match.end():].strip()
    # Also remove Transcriber's Notes
    trans_match = re.search(r'\nTranscriber.s Notes:', postscript_text)
    if trans_match:
        postscript_text = postscript_text[:trans_match.start()].strip()

    items = []
    sort_order = 1

    # === PREFACE ===
    items.append({
        "id": "preface",
        "name": "Preface",
        "sort_order": sort_order,
        "category": "preface",
        "level": 1,
        "sections": {
            "Text": truncate_text(preface_text)
        },
        "keywords": ["preface", "acts-of-john", "miracle", "dating"],
        "metadata": {}
    })
    sort_order += 1

    # === VISION OF THE CROSS ===
    # Split into numbered paragraphs (1-25)
    # Pattern: "N. " or "N [digits" at start of paragraph
    vision_paragraphs = re.split(r'\n\n+', vision_text)

    current_para = None
    current_text = []
    vision_items = []
    vision_ids = []

    para_pattern = re.compile(r'^(\d+)\.\s')

    for p in vision_paragraphs:
        p = p.strip()
        if not p:
            continue
        match = para_pattern.match(p)
        if match:
            # Save previous
            if current_para is not None:
                combined = '\n\n'.join(current_text)
                item_id = f"vision-{current_para}"
                vision_items.append((item_id, f"Vision of the Cross, Verse {current_para}", combined))
                vision_ids.append(item_id)
            current_para = int(match.group(1))
            current_text = [p]
        else:
            if current_text:
                current_text.append(p)
            else:
                current_text = [p]

    # Save last
    if current_para is not None:
        combined = '\n\n'.join(current_text)
        item_id = f"vision-{current_para}"
        vision_items.append((item_id, f"Vision of the Cross, Verse {current_para}", combined))
        vision_ids.append(item_id)

    # Group vision verses into larger items (some are very short)
    # Group: 1-3 (narrative setup), 4-8 (revelation begins), 9-13 (nature of the cross),
    # 14-18 (the multitude and mystery), 19-25 (suffering and understanding)
    vision_groups = [
        (1, 3, "vision-1-3", "The Cave and the Cross", ["cave", "crucifixion", "mount-of-olives"]),
        (4, 8, "vision-4-8", "The Names of the Cross", ["cross-of-light", "logos", "names"]),
        (9, 13, "vision-9-13", "The Cross as Wisdom and Boundary", ["wisdom", "harmony", "cross-beaming"]),
        (14, 18, "vision-14-18", "The Multitude and the Mystery", ["race", "upper-nature", "mystery"]),
        (19, 23, "vision-19-23", "The Suffering of the Word", ["suffering", "word", "logos", "paradox"]),
        (24, 25, "vision-24-25", "The Ascension and the Symbolic", ["ascension", "symbol", "dispensation"]),
    ]

    for start_v, end_v, group_id, group_name, kw in vision_groups:
        group_texts = []
        group_verse_ids = []
        for item_id, item_name, text in vision_items:
            verse_num = int(item_id.split('-')[1])
            if start_v <= verse_num <= end_v:
                group_texts.append(text)
                group_verse_ids.append(item_id)

        if group_texts:
            combined = '\n\n'.join(group_texts)
            items.append({
                "id": group_id,
                "name": group_name,
                "sort_order": sort_order,
                "category": "vision",
                "level": 1,
                "sections": {
                    "Text": truncate_text(combined)
                },
                "keywords": kw,
                "metadata": {}
            })
            sort_order += 1

    # === COMMENTS ===
    # Comments are keyed to verse numbers: "1. The disciples flee..."
    # Split by paragraph number references
    comment_paragraphs = re.split(r'\n\n+', comments_text)

    # Group comments by the verse they reference
    comment_sections = []
    current_comment = []
    current_ref = None

    # First, collect the introductory text before numbered comments
    intro_comments = []

    comment_num_pattern = re.compile(r'^(\d+)\.\s')

    for p in comment_paragraphs:
        p = p.strip()
        if not p:
            continue
        match = comment_num_pattern.match(p)
        if match:
            num = int(match.group(1))
            if current_comment:
                if current_ref is not None:
                    comment_sections.append((current_ref, '\n\n'.join(current_comment)))
                else:
                    intro_comments.extend(current_comment)
            current_ref = num
            current_comment = [p]
        else:
            current_comment.append(p)

    if current_comment and current_ref is not None:
        comment_sections.append((current_ref, '\n\n'.join(current_comment)))

    # Add introductory comments if any
    if intro_comments:
        items.append({
            "id": "comments-intro",
            "name": "Introduction to the Comments",
            "sort_order": sort_order,
            "category": "commentary",
            "level": 1,
            "sections": {
                "Commentary": truncate_text('\n\n'.join(intro_comments))
            },
            "keywords": ["commentary", "introduction", "text-criticism"],
            "metadata": {}
        })
        sort_order += 1

    # Group comments similarly to vision groups
    comment_groups = [
        (1, 3, "comments-1-3", "Commentary: The Cave and the Cross", ["cave", "mount-of-olives", "tree-of-life", "batos"]),
        (4, 8, "comments-4-8", "Commentary: The Names of the Cross", ["cross", "names", "bread", "life"]),
        (9, 13, "comments-9-13", "Commentary: Wisdom and the Cross", ["wisdom", "harmony", "cross-beaming", "docetism"]),
        (14, 18, "comments-14-18", "Commentary: The Race and the Mystery", ["race", "limbs", "osiris", "gospel-of-eve"]),
        (19, 23, "comments-19-23", "Commentary: The Word and Suffering", ["word", "suffering", "logos", "reason"]),
        (24, 25, "comments-24-25", "Commentary: Ascension and Contemplation", ["ascension", "contemplation", "symbol"]),
    ]

    comment_ids = []
    for start_c, end_c, group_id, group_name, kw in comment_groups:
        group_texts = []
        for ref, text in comment_sections:
            if start_c <= ref <= end_c:
                group_texts.append(text)

        if group_texts:
            combined = '\n\n'.join(group_texts)
            items.append({
                "id": group_id,
                "name": group_name,
                "sort_order": sort_order,
                "category": "commentary",
                "level": 1,
                "sections": {
                    "Commentary": truncate_text(combined)
                },
                "keywords": kw,
                "metadata": {}
            })
            comment_ids.append(group_id)
            sort_order += 1

    # === POSTSCRIPT ===
    items.append({
        "id": "postscript",
        "name": "Postscript: The Cross of Light",
        "sort_order": sort_order,
        "category": "postscript",
        "level": 1,
        "sections": {
            "Text": truncate_text(postscript_text)
        },
        "keywords": ["postscript", "cross-of-light", "peter", "andrew", "acts-of-philip"],
        "metadata": {}
    })
    sort_order += 1

    # === L2: Thematic Groupings ===
    vision_l1_ids = [f"vision-{s}-{e}" for s, e, _, _, _ in vision_groups]

    items.append({
        "id": "l2-vision",
        "name": "The Vision of the Cross: Complete Text",
        "sort_order": sort_order,
        "category": "thematic-grouping",
        "level": 2,
        "composite_of": [vid for vid in vision_l1_ids if any(i["id"] == vid for i in items)],
        "sections": {
            "About": "The complete Vision of the Cross from the Acts of John, in which the disciple John, having fled the physical crucifixion, receives on the Mount of Olives a vision of the Cross of Light. The Lord reveals that the Cross is called by many names (Word, Mind, Jesus, Christ, Door, Way, Bread, Seed, Resurrection) and that His true suffering is not what the multitude below perceives.",
            "Key Themes": "The Cross of Light as the master-symbol; the many names of the Cross; the paradox of suffering and non-suffering; the distinction between the wood cross and the living Cross; the gathering of the Race."
        },
        "keywords": ["vision", "cross-of-light", "acts-of-john", "revelation"],
        "metadata": {}
    })
    sort_order += 1

    items.append({
        "id": "l2-commentary",
        "name": "Mead's Commentary: Interpreting the Mystery",
        "sort_order": sort_order,
        "category": "thematic-grouping",
        "level": 2,
        "composite_of": [cid for cid in comment_ids] + (["comments-intro"] if intro_comments else []),
        "sections": {
            "About": "G.R.S. Mead's detailed commentary on each verse of the Vision, drawing on Valentinian, Naassene, Docetic, and Hermetic sources. He interprets the Cross as the principle of separation and union, the Batos as the medium of transmission between Light and Darkness, and the Race as the upper nature of humanity awakening to its divine origin.",
            "Key Themes": "The Batos as Tree of Life and medium of passage; the Cross as Boundary (Horos) of the Pleroma; the Race of the Logos; the Limbs of the Ineffable; the mystery of simultaneous joy and sorrow; the Osiric tradition of scattered and gathered limbs."
        },
        "keywords": ["commentary", "mead", "interpretation", "valentinian", "naassene"],
        "metadata": {}
    })
    sort_order += 1

    items.append({
        "id": "l2-postscript-context",
        "name": "The Cross in Gnostic Literature",
        "sort_order": sort_order,
        "category": "thematic-grouping",
        "level": 2,
        "composite_of": ["preface", "postscript"],
        "sections": {
            "About": "The framing material: Mead's preface establishing the early date of the text through the miracle of the loaves, and his postscript tracing the mystery of the Cross through the Acts of Philip, the Acts of Andrew, the Martyrdom of Peter, the Docetic baptism doctrine, and the Valentinian interpretation of Ephesians. The reversed crucifixion of Peter symbolizes the man of generation; the upright crucifixion of Christ symbolizes the regenerate man.",
            "Key Themes": "Dating evidence from the miracle of the loaves; the Address of Andrew to the Cross; Peter crucified head-downwards; the Docetic body of baptism; the Valentinian Cross as Boundary of the Pleroma."
        },
        "keywords": ["postscript", "cross", "peter", "andrew", "philip", "docetism"],
        "metadata": {}
    })
    sort_order += 1

    # === L3: Meta ===
    l2_ids = ["l2-vision", "l2-commentary", "l2-postscript-context"]
    items.append({
        "id": "l3-gnostic-crucifixion",
        "name": "The Gnostic Crucifixion: Complete Work",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": l2_ids,
        "sections": {
            "About": "G.R.S. Mead's complete study of the Gnostic interpretation of the crucifixion, based on the newly-found fragments of the Acts of John. The Vision of the Cross reveals the crucifixion as a cosmic rather than merely historical event: the Cross of Light is the master-symbol uniting all opposites, the means by which the Logos 'cross-beams' all things, simultaneously separating and joining the generable and ingenerable.",
            "Significance": "Published in 1907 as Volume VII of 'Echoes from the Gnosis,' this work is one of the earliest modern studies to take Gnostic Christianity seriously on its own terms. Mead draws on Valentinian, Naassene, Docetic, and Hermetic sources to reconstruct a coherent mystical theology of the Cross that predates and differs radically from orthodox Christianity's emphasis on substitutionary atonement."
        },
        "keywords": ["gnostic-crucifixion", "cross-of-light", "acts-of-john", "mead", "gnosticism"],
        "metadata": {}
    })
    sort_order += 1

    return items


def build_grammar(name, description, tags, items, attribution, gutenberg_num, gutenberg_url):
    """Build the complete grammar JSON structure."""
    return {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": attribution
        },
        "name": name,
        "description": description,
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": tags,
        "roots": ["mysticism", "western-esotericism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "non-dual",
        "items": items
    }


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    seeds_dir = os.path.join(base_dir, "seeds")
    grammars_dir = os.path.join(base_dir, "grammars")

    # === Grammar 1: Gnosis of the Light ===
    print("Parsing The Gnosis of the Light...")
    gnosis_items = parse_gnosis_of_light(os.path.join(seeds_dir, "gnosis-of-light.txt"))

    gnosis_grammar = build_grammar(
        name="The Gnosis of the Light",
        description="Translation and commentary on the Codex Brucianus, an ancient Gnostic text describing the emanation of divine light and the structure of the spiritual universe. Rev. F. Lamplugh's 1918 English rendering of the Untitled Apocalypse, a second-century work from the Codex Brucianus (Bodleian Library, Oxford), with introduction and explanatory notes.\n\nSource: Project Gutenberg eBook #30799 (https://www.gutenberg.org/ebooks/30799)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: The Codex Brucianus Gnostic Cross frontispiece (original MS, Bodleian Library); William Blake's visionary illustrations of cosmic emanation (1790s-1820s); Athanasius Kircher's diagrams of cosmic hierarchies from Oedipus Aegyptiacus (1652-1654).",
        tags=["gnosticism", "esoteric", "light", "cosmology", "early-christianity"],
        items=gnosis_items,
        attribution=[
            {"name": "F. Lamplugh", "date": "1918", "note": "Translator and commentator"},
            {"name": "Unknown Gnostic author", "date": "c. 160-200 AD", "note": "Original Greek text (Untitled Apocalypse, Codex Brucianus)"},
            {"name": "Project Gutenberg", "date": "2009", "note": "Digital text, eBook #30799"}
        ],
        gutenberg_num=30799,
        gutenberg_url="https://www.gutenberg.org/ebooks/30799"
    )

    output_path = os.path.join(grammars_dir, "gnosis-of-light", "grammar.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(gnosis_grammar, f, indent=2, ensure_ascii=False)
    print(f"  Written to {output_path}")
    print(f"  Items: {len(gnosis_items)}, L1: {sum(1 for i in gnosis_items if i['level']==1)}, L2: {sum(1 for i in gnosis_items if i['level']==2)}, L3: {sum(1 for i in gnosis_items if i['level']==3)}")

    # === Grammar 2: Gnostic Crucifixion ===
    print("\nParsing The Gnostic Crucifixion...")
    crucifixion_items = parse_gnostic_crucifixion(os.path.join(seeds_dir, "gnostic-crucifixion.txt"))

    crucifixion_grammar = build_grammar(
        name="The Gnostic Crucifixion",
        description="G.R.S. Mead's study of the Gnostic interpretation of the crucifixion, exploring how early Gnostic Christians understood the cross as a cosmic symbol rather than a historical event. Based on the newly-found fragments of The Acts of John, this 1907 work presents the Vision of the Cross with Mead's detailed commentary drawing on Valentinian, Naassene, Docetic, and Hermetic sources.\n\nSource: Project Gutenberg eBook #35735 (https://www.gutenberg.org/ebooks/35735)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Early Christian cross symbols from the Roman catacombs (2nd-4th century); the Chi-Rho and Christogram from Constantine's era; Coptic cross designs from Egyptian manuscripts; William Blake's crucifixion and resurrection illustrations.",
        tags=["gnosticism", "esoteric", "crucifixion", "mysticism", "early-christianity"],
        items=crucifixion_items,
        attribution=[
            {"name": "G.R.S. Mead", "date": "1907", "note": "Author, translator, and commentator"},
            {"name": "Unknown Gnostic author", "date": "c. 1st-2nd century AD", "note": "Original Vision of the Cross from the Acts of John"},
            {"name": "Project Gutenberg", "date": "2011", "note": "Digital text, eBook #35735"}
        ],
        gutenberg_num=35735,
        gutenberg_url="https://www.gutenberg.org/ebooks/35735"
    )

    output_path = os.path.join(grammars_dir, "gnostic-crucifixion", "grammar.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(crucifixion_grammar, f, indent=2, ensure_ascii=False)
    print(f"  Written to {output_path}")
    print(f"  Items: {len(crucifixion_items)}, L1: {sum(1 for i in crucifixion_items if i['level']==1)}, L2: {sum(1 for i in crucifixion_items if i['level']==2)}, L3: {sum(1 for i in crucifixion_items if i['level']==3)}")


if __name__ == "__main__":
    main()
