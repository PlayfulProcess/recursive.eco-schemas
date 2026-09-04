#!/usr/bin/env python3
"""
Build grammar.json for The Prose Edda from seeds/prose-edda.txt
(Project Gutenberg #18947, Rasmus B. Anderson translation, 1901)

The Prose Edda (Younger Edda / Snorre's Edda) by Snorri Sturluson (c. 1220).
Main sections: Foreword, The Fooling of Gylfe (17 chapters), Brage's Talk (4 chapters),
Afterword, and selections from Skaldskaparmal.
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SEED_FILE = os.path.join(ROOT_DIR, "seeds", "prose-edda.txt")
OUTPUT_DIR = os.path.join(ROOT_DIR, "grammars", "prose-edda")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "grammar.json")


def read_seed():
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    lines = text.split("\n")
    start_idx = 0
    end_idx = len(lines)
    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i + 1
            break
    for i, line in enumerate(lines):
        if end_marker in line:
            end_idx = i
            break
    return "\n".join(lines[start_idx:end_idx])


def roman_to_int(s):
    """Convert Roman numeral string to integer."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    for i in range(len(s)):
        if i + 1 < len(s) and values.get(s[i], 0) < values.get(s[i+1], 0):
            result -= values.get(s[i], 0)
        else:
            result += values.get(s[i], 0)
    return result


def strip_footnotes(text):
    """Remove footnote markers and footnote text blocks."""
    # Remove inline footnote references like [8]
    text = re.sub(r'\[(\d+)\]', '', text)
    # Remove footnote blocks like "    [Footnote 8: ...]"
    text = re.sub(r'\s*\[Footnote \d+:.*?\]', '', text, flags=re.DOTALL)
    return text


def clean_text(text):
    """Clean up text: strip footnotes, normalize whitespace."""
    text = strip_footnotes(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# Chapter titles for Fooling of Gylfe (from TOC)
GYLFE_TITLES = {
    1: "Gefjun's Plowing",
    2: "Gylfe's Journey to Asgard",
    3: "Of the Highest God",
    4: "The Creation of the World",
    5: "The Creation (continued)",
    6: "The First Works of the Asas — The Golden Age",
    7: "On the Wonderful Things in Heaven",
    8: "The Asas",
    9: "Loke and His Offspring",
    10: "The Goddesses (Asynjes)",
    11: "The Giantess Gerd and Skirner's Journey",
    12: "Life in Valhal",
    13: "Odin's Horse and Frey's Ship",
    14: "Thor's Adventures",
    15: "The Death of Balder",
    16: "Ragnarok",
    17: "Regeneration",
}

# Chapter titles for Brage's Talk
BRAGE_TITLES = {
    1: "Aeger's Journey to Asgard",
    2: "Idun and Her Apples",
    3: "How Njord Got Skade to Wife",
    4: "The Origin of Poetry",
}


def find_sections(lines):
    """Find the major sections of the text."""
    sections = {}

    # Find Foreword
    for i, line in enumerate(lines):
        if line.strip() == "FOREWORD.":
            sections['foreword_start'] = i
            break

    # Find Fooling of Gylfe (the actual narrative, not TOC)
    gylfe_starts = []
    for i, line in enumerate(lines):
        if line.strip() == "THE FOOLING OF GYLFE.":
            gylfe_starts.append(i)

    # The first occurrence in the TOC area, the second is the actual narrative
    # We look for CHAPTER I right after THE FOOLING OF GYLFE
    for gs in gylfe_starts:
        # Check if there's a CHAPTER I within 10 lines
        for j in range(gs + 1, min(gs + 10, len(lines))):
            if lines[j].strip() == "CHAPTER I.":
                # Check if this is the narrative (has actual paragraph text nearby)
                for k in range(j + 1, min(j + 10, len(lines))):
                    if len(lines[k].strip()) > 50:
                        sections['gylfe_start'] = gs
                        break
                if 'gylfe_start' in sections:
                    break
        if 'gylfe_start' in sections:
            break

    # Find Afterword to Gylfe
    for i, line in enumerate(lines):
        if line.strip() == "AFTERWORD" and i > sections.get('gylfe_start', 0):
            # Check next line for "TO THE FOOLING OF GYLFE"
            for j in range(i + 1, min(i + 3, len(lines))):
                if "FOOLING OF GYLFE" in lines[j]:
                    sections['gylfe_afterword_start'] = i
                    break
            if 'gylfe_afterword_start' in sections:
                break

    # Find Brage's Talk
    for i, line in enumerate(lines):
        stripped = line.strip().replace('\u2019', "'")
        if stripped == "BRAGE'S TALK.":
            # Make sure it's the narrative one (has CHAPTER I nearby)
            for j in range(i + 1, min(i + 10, len(lines))):
                if lines[j].strip() == "CHAPTER I.":
                    for k in range(j + 1, min(j + 10, len(lines))):
                        if len(lines[k].strip()) > 50:
                            sections['brage_start'] = i
                            break
                    break
            if 'brage_start' in sections:
                break

    # Find Afterword to Brage's Talk
    for i, line in enumerate(lines):
        if line.strip() == "AFTERWORD" and i > sections.get('brage_start', 0):
            for j in range(i + 1, min(i + 3, len(lines))):
                # Handle both ASCII apostrophe and Unicode right single quotation mark
                line_normalized = lines[j].replace('\u2019', "'")
                if "BRAGE'S TALK" in line_normalized.upper():
                    sections['brage_afterword_start'] = i
                    break
            if 'brage_afterword_start' in sections:
                break

    # Find NOTES section
    for i, line in enumerate(lines):
        if line.strip() == "NOTES." and i > sections.get('brage_afterword_start', 0):
            sections['notes_start'] = i
            break

    return sections


def extract_chapters(lines, start_line, end_line, title_map, id_prefix):
    """Extract chapters between start_line and end_line."""
    chapters = []
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC]+)\.$')

    chapter_starts = []
    for i in range(start_line, end_line):
        m = chapter_pattern.match(lines[i].strip())
        if m:
            num = roman_to_int(m.group(1))
            chapter_starts.append((i, num))

    for idx, (ch_start, num) in enumerate(chapter_starts):
        if idx + 1 < len(chapter_starts):
            ch_end = chapter_starts[idx + 1][0]
        else:
            ch_end = end_line

        # Skip the CHAPTER line and subtitle
        content_start = ch_start + 1
        while content_start < ch_end and lines[content_start].strip() == "":
            content_start += 1
        # Skip the subtitle line (all caps)
        if content_start < ch_end:
            subtitle = lines[content_start].strip()
            if subtitle and (subtitle == subtitle.upper() or subtitle.endswith(".")):
                # Check if it looks like a subtitle (short, all caps or similar)
                if len(subtitle) < 80 and subtitle.upper() == subtitle:
                    content_start += 1

        while content_start < ch_end and lines[content_start].strip() == "":
            content_start += 1

        ch_text = "\n".join(lines[content_start:ch_end]).strip()
        ch_text = clean_text(ch_text)

        title = title_map.get(num, f"Chapter {num}")
        item_id = f"{id_prefix}-ch{num:02d}"

        chapters.append({
            "id": item_id,
            "num": num,
            "title": title,
            "text": ch_text
        })

    return chapters


def extract_section_text(lines, start_line, end_line):
    """Extract text of a section, skipping the header."""
    content_start = start_line + 1
    while content_start < end_line and lines[content_start].strip() == "":
        content_start += 1
    # Skip secondary header lines
    while content_start < end_line:
        stripped = lines[content_start].strip()
        if stripped and stripped == stripped.upper() and len(stripped) < 60:
            content_start += 1
            continue
        if stripped == "":
            content_start += 1
            continue
        break

    text = "\n".join(lines[content_start:end_line]).strip()
    return clean_text(text)


def build_grammar():
    raw_text = read_seed()
    text = strip_gutenberg(raw_text)
    lines = text.split("\n")

    sections = find_sections(lines)

    items = []
    sort_order = 0

    # Extract Foreword
    foreword_end = sections.get('gylfe_start', len(lines))
    if 'foreword_start' in sections:
        fw_text = extract_section_text(lines, sections['foreword_start'], foreword_end)
        items.append({
            "id": "foreword",
            "name": "Foreword: The Euhemeristic Prologue",
            "sort_order": sort_order,
            "category": "foreword",
            "level": 1,
            "sections": {
                "Passage": fw_text
            },
            "keywords": ["foreword", "euhemerism", "troy", "asgard", "odin"],
            "metadata": {}
        })
        sort_order += 1

    # Extract Fooling of Gylfe chapters
    gylfe_end = sections.get('gylfe_afterword_start', sections.get('brage_start', len(lines)))
    gylfe_chapters = extract_chapters(
        lines,
        sections.get('gylfe_start', 0),
        gylfe_end,
        GYLFE_TITLES,
        "gylfe"
    )

    gylfe_ids = []
    for ch in gylfe_chapters:
        keywords = []
        text_lower = ch['text'].lower()
        for kw in ["odin", "thor", "loke", "balder", "frey", "freya", "heimdal",
                    "ymer", "asgard", "midgard", "ragnarok", "valhal", "fenris", "jotun"]:
            if kw in text_lower:
                keywords.append(kw)

        items.append({
            "id": ch['id'],
            "name": f"Gylfe {ch['num']}: {ch['title']}",
            "sort_order": sort_order,
            "category": "gylfe",
            "level": 1,
            "sections": {
                "Passage": ch['text']
            },
            "keywords": keywords,
            "metadata": {"chapter_number": ch['num']}
        })
        gylfe_ids.append(ch['id'])
        sort_order += 1

    # Extract Afterword to Gylfe
    brage_start = sections.get('brage_start', len(lines))
    if 'gylfe_afterword_start' in sections:
        aw_text = extract_section_text(lines, sections['gylfe_afterword_start'], brage_start)
        items.append({
            "id": "gylfe-afterword",
            "name": "Afterword to the Fooling of Gylfe",
            "sort_order": sort_order,
            "category": "gylfe",
            "level": 1,
            "sections": {
                "Passage": aw_text
            },
            "keywords": ["afterword", "euhemerism", "troy"],
            "metadata": {}
        })
        gylfe_ids.append("gylfe-afterword")
        sort_order += 1

    # Extract Brage's Talk chapters
    brage_end = sections.get('brage_afterword_start', sections.get('notes_start', len(lines)))
    brage_chapters = extract_chapters(
        lines,
        sections.get('brage_start', 0),
        brage_end,
        BRAGE_TITLES,
        "brage"
    )

    brage_ids = []
    for ch in brage_chapters:
        keywords = []
        text_lower = ch['text'].lower()
        for kw in ["odin", "thor", "loke", "idun", "skade", "njord", "brage",
                    "asgard", "poetry", "mead"]:
            if kw in text_lower:
                keywords.append(kw)

        items.append({
            "id": ch['id'],
            "name": f"Brage {ch['num']}: {ch['title']}",
            "sort_order": sort_order,
            "category": "brage",
            "level": 1,
            "sections": {
                "Passage": ch['text']
            },
            "keywords": keywords,
            "metadata": {"chapter_number": ch['num']}
        })
        brage_ids.append(ch['id'])
        sort_order += 1

    # Extract Afterword to Brage's Talk
    notes_start = sections.get('notes_start', len(lines))
    if 'brage_afterword_start' in sections:
        baw_text = extract_section_text(lines, sections['brage_afterword_start'], notes_start)
        # This afterword contains the Skaldskaparmal passages too
        items.append({
            "id": "brage-afterword",
            "name": "Afterword to Brage's Talk and Poetical Diction",
            "sort_order": sort_order,
            "category": "brage",
            "level": 1,
            "sections": {
                "Passage": baw_text
            },
            "keywords": ["afterword", "kenning", "skaldic-poetry", "poetic-diction"],
            "metadata": {}
        })
        brage_ids.append("brage-afterword")
        sort_order += 1

    # L2: Section groupings
    # Fooling of Gylfe
    l2_gylfe = {
        "id": "section-gylfe",
        "name": "The Fooling of Gylfe (Gylfaginning)",
        "sort_order": sort_order,
        "category": "section",
        "level": 2,
        "sections": {
            "About": "The Fooling of Gylfe (Gylfaginning) is the core mythological section of the Prose Edda. King Gylfe of Sweden, disguised as Ganglere, travels to Asgard to question the gods. Through dialogue with the mysterious figures High, Just-as-High, and Third, he learns the entire Norse cosmogony: the creation from Ymer's body, the world-tree Ygdrasil, the gods and goddesses, Thor's adventures among the giants, the death of Balder, and the final doom of Ragnarok followed by regeneration.",
            "For Readers": "This is the most complete and systematic account of Norse mythology that survives from the medieval period. Snorri wrote it as a handbook for poets, but it became the primary source for almost everything we know about the Norse gods. Read it as one continuous dialogue — Gylfe asks, the gods answer, and a whole cosmos unfolds."
        },
        "keywords": ["norse", "creation", "ragnarok", "odin", "thor", "balder"],
        "metadata": {},
        "composite_of": gylfe_ids,
        "relationship_type": "emergence"
    }
    items.append(l2_gylfe)
    sort_order += 1

    # Brage's Talk
    l2_brage = {
        "id": "section-brage",
        "name": "Brage's Talk (Bragaraedur)",
        "sort_order": sort_order,
        "category": "section",
        "level": 2,
        "sections": {
            "About": "Brage's Talk is set at a feast in Asgard where the god Brage tells the sea-giant Aeger the stories behind the poetic kennings. It includes the myth of Idun's apples of immortality, the tale of how Njord won Skade for his wife by making her laugh, and the origin of the mead of poetry — the sacred drink made from the blood of the wise Kvaser, stolen by Odin from the giants.",
            "For Readers": "Brage's Talk reveals how Norse myths were embedded in poetic language. Every kenning (poetic circumlocution) carried a story. When a skald called gold 'Sif's hair' or poetry 'Kvaser's blood,' the audience was expected to know the myth. This section restores those connections."
        },
        "keywords": ["brage", "idun", "poetry", "kenning", "mead", "skaldic"],
        "metadata": {},
        "composite_of": brage_ids,
        "relationship_type": "emergence"
    }
    items.append(l2_brage)
    sort_order += 1

    # Thematic L2: Creation and Cosmogony
    creation_ids = [ch['id'] for ch in gylfe_chapters if ch['num'] in [1, 2, 3, 4, 5, 6, 7]]
    l2_creation = {
        "id": "theme-creation",
        "name": "Creation and the Cosmic Order",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "The Norse creation begins in the void of Ginungagap, between the ice of Niflheim and the fire of Muspelheim. From the melting ice, the giant Ymer is born; from his slain body the gods create the world. The world-tree Ygdrasil holds the cosmos together, with its roots reaching into the realms of death, frost-giants, and gods. Asgard gleams above; Midgard shelters humanity; and beneath it all, the Norns weave fate.",
            "For Readers": "The Norse creation myth is one of the most vivid in world mythology — a cosmos built from a murdered giant's flesh, skull, and blood. Notice how violence and beauty are intertwined: destruction creates, and creation contains the seeds of its own destruction at Ragnarok."
        },
        "keywords": ["creation", "ymer", "ginungagap", "ygdrasil", "asgard", "midgard"],
        "metadata": {},
        "composite_of": creation_ids,
        "relationship_type": "emergence"
    }
    items.append(l2_creation)
    sort_order += 1

    # Gods and Goddesses
    gods_ids = [ch['id'] for ch in gylfe_chapters if ch['num'] in [8, 9, 10, 11, 12, 13]]
    l2_gods = {
        "id": "theme-gods",
        "name": "The Gods, Goddesses, and Valhal",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "The Asas (gods) and Asynjes (goddesses) of Norse mythology: Odin the Allfather, Thor the Thunderer, Loke the Trickster, Balder the Beautiful, Frey and Freyja, Heimdal the Watchman, and many others. Also the monstrous offspring of Loke — the Fenris-wolf, the Midgard-serpent, and Hel, goddess of death. And Valhal, where the fallen warriors feast and fight until Ragnarok.",
            "For Readers": "The Norse gods are mortal — they age, they fear, and they will die at Ragnarok. This gives the mythology a tragic dignity found in few other traditions. Loke is especially complex: neither fully god nor fully enemy, he is the catalyst whose actions drive the entire mythic narrative toward its doom."
        },
        "keywords": ["odin", "thor", "loke", "balder", "valhal", "fenris", "hel"],
        "metadata": {},
        "composite_of": gods_ids,
        "relationship_type": "emergence"
    }
    items.append(l2_gods)
    sort_order += 1

    # Doom and Renewal
    doom_ids = [ch['id'] for ch in gylfe_chapters if ch['num'] in [14, 15, 16, 17]]
    l2_doom = {
        "id": "theme-doom",
        "name": "Doom and Renewal: From Balder's Death to Ragnarok",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "The death of Balder — killed by a mistletoe dart guided by Loke's treachery — sets in motion the end of the world. Ragnarok brings the final battle: the Fenris-wolf swallows Odin, Thor slays the Midgard-serpent but falls to its venom, fire consumes the world. Yet from the ashes, a green earth rises, Balder returns, and a new age begins.",
            "For Readers": "Ragnarok is not mere destruction but a cosmic cycle of death and rebirth. The Norse faced the end with courage rather than despair — knowing the gods would fall but fighting anyway. This unflinching acceptance of mortality, paired with hope for renewal, is the heart of Norse wisdom."
        },
        "keywords": ["ragnarok", "balder", "death", "renewal", "doom", "regeneration"],
        "metadata": {},
        "composite_of": doom_ids,
        "relationship_type": "emergence"
    }
    items.append(l2_doom)
    sort_order += 1

    # L3: Meta
    all_l2_ids = ["section-gylfe", "section-brage", "theme-creation", "theme-gods", "theme-doom"]
    meta_item = {
        "id": "prose-edda-meta",
        "name": "The Prose Edda of Snorri Sturluson",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "The Prose Edda (also called the Younger Edda or Snorre's Edda) was written by the Icelandic scholar and chieftain Snorri Sturluson around 1220 CE. It is the most complete and systematic account of Norse mythology that survives from the medieval period. Originally composed as a handbook for poets — explaining the mythological allusions embedded in skaldic verse — it became the primary source for nearly everything we know about Odin, Thor, Loke, Ragnarok, and the Norse cosmos.",
            "For Readers": "Snorri wrote as a Christian looking back at the old faith with a mixture of scholarly distance and genuine admiration. His framing device — a Swedish king questioning disguised gods — gives the myths a quality of remembered wisdom: stories told about gods who were already gone. This makes the Prose Edda both a mythology and an elegy."
        },
        "keywords": ["norse", "edda", "snorri", "mythology", "odin", "thor", "ragnarok", "creation"],
        "metadata": {},
        "composite_of": all_l2_ids,
        "relationship_type": "emergence"
    }
    items.append(meta_item)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Snorri Sturluson", "date": "c. 1220", "note": "Original author"},
                {"name": "Rasmus B. Anderson", "date": "1901", "note": "English translation"}
            ]
        },
        "name": "The Prose Edda",
        "description": "The Prose Edda (Younger Edda) by Snorri Sturluson (c. 1220), the most complete medieval account of Norse mythology, in the English translation by Rasmus B. Anderson (1901). Includes The Fooling of Gylfe (Gylfaginning) — the full Norse cosmogony from creation to Ragnarok — and Brage's Talk (Bragaraedur) — the myths behind the poetic kennings. The foundational source for Odin, Thor, Loke, Balder, Ragnarok, and the Norse cosmos.\n\nSource: Project Gutenberg eBook #18947 (https://www.gutenberg.org/ebooks/18947)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: W.G. Collingwood's illustrations for the 1908 Norroena Society Edda editions — pen and ink drawings of Norse mythological scenes. Lorenz Frolich's Norse mythology illustrations (1895) — romantic depictions of the Aesir. Arthur Rackham's illustrations for Wagner's Ring cycle (1910-1911), which draw directly on Eddaic sources.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["mythology", "norse", "viking", "creation-myth", "ragnarok", "public-domain", "full-text"],
        "roots": ["indigenous-mythology"],
        "shelves": ["earth"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"Generated {OUTPUT_FILE}")
    print(f"  L1 items: {l1}")
    print(f"    Foreword: 1")
    print(f"    Gylfe chapters: {len(gylfe_chapters)}")
    print(f"    Gylfe afterword: {'1' if 'gylfe_afterword_start' in sections else '0'}")
    print(f"    Brage chapters: {len(brage_chapters)}")
    print(f"    Brage afterword: {'1' if 'brage_afterword_start' in sections else '0'}")
    print(f"  L2 items (groups): {l2}")
    print(f"  L3 items (meta): {l3}")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
