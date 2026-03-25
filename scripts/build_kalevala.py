#!/usr/bin/env python3
"""
Build grammar.json for The Kalevala from seeds/kalevala.txt
(Project Gutenberg #5186, John Martin Crawford translation, 1888)

Parses 50 Runos (cantos) of the Finnish national epic.
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SEED_FILE = os.path.join(ROOT_DIR, "seeds", "kalevala.txt")
OUTPUT_DIR = os.path.join(ROOT_DIR, "grammars", "kalevala")
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


# Rune titles from the table of contents
RUNE_TITLES = {
    1: "Birth of Wainamoinen",
    2: "Wainamoinen's Sowing",
    3: "Wainamoinen and Youkahainen",
    4: "The Fate of Aino",
    5: "Wainamoinen's Lamentation",
    6: "Wainamoinen's Hapless Journey",
    7: "Wainamoinen's Rescue",
    8: "Maiden of the Rainbow",
    9: "Origin of Iron",
    10: "Ilmarinen Forges the Sampo",
    11: "Lemminkainen's Lament",
    12: "Kyllikki's Broken Vow",
    13: "Lemminkainen's Second Wooing",
    14: "Death of Lemminkainen",
    15: "Lemminkainen's Restoration",
    16: "Wainamoinen's Boat-building",
    17: "Wainamoinen Finds the Lost Word",
    18: "The Rival Suitors",
    19: "Ilmarinen's Wooing",
    20: "The Brewing of Beer",
    21: "Ilmarinen's Wedding-feast",
    22: "The Bride's Farewell",
    23: "Osmotar, the Bride-adviser",
    24: "The Bride's Farewell (continued)",
    25: "Wainamoinen's Wedding-songs",
    26: "Origin of the Serpent",
    27: "The Unwelcome Guest",
    28: "The Mother's Counsel",
    29: "The Isle of Refuge",
    30: "The Frost-fiend",
    31: "Kullerwoinen, Son of Evil",
    32: "Kullervo as a Shepherd",
    33: "Kullervo and the Cheat-cake",
    34: "Kullervo Finds His Tribe-folk",
    35: "Kullervo's Evil Deeds",
    36: "Kullerwoinen's Victory and Death",
    37: "Ilmarinen's Bride of Gold",
    38: "Ilmarinen's Fruitless Wooing",
    39: "Wainamoinen's Sailing",
    40: "Birth of the Harp",
    41: "Wainamoinen's Harp-songs",
    42: "Capture of the Sampo",
    43: "The Sampo Lost in the Sea",
    44: "Birth of the Second Harp",
    45: "Birth of the Nine Diseases",
    46: "Otso the Honey-eater",
    47: "Louhi Steals Sun, Moon, and Fire",
    48: "Capture of the Fire-fish",
    49: "Restoration of the Sun and Moon",
    50: "Mariatta — Wainamoinen's Departure",
}


def extract_runes(text):
    """Extract the 50 runos from the text."""
    lines = text.split("\n")

    # Find rune start lines
    rune_starts = []
    rune_pattern = re.compile(r'^RUNE\s+([IVXLC]+)\.$')
    for i, line in enumerate(lines):
        m = rune_pattern.match(line.strip())
        if m:
            num = roman_to_int(m.group(1))
            rune_starts.append((i, num))

    # Find EPILOGUE or GLOSSARY as end marker
    end_line = len(lines)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in ("EPILOGUE", "GLOSSARY"):
            end_line = i
            break

    runes = []
    for idx, (start_line, num) in enumerate(rune_starts):
        if idx + 1 < len(rune_starts):
            next_start = rune_starts[idx + 1][0]
        else:
            next_start = end_line

        # Skip the RUNE header line and the title line
        content_start = start_line + 1
        # Skip blank lines and the subtitle
        while content_start < next_start and lines[content_start].strip() == "":
            content_start += 1
        # Skip the subtitle line (e.g., "BIRTH OF WAINAMOINEN.")
        subtitle_line = lines[content_start].strip() if content_start < next_start else ""
        if subtitle_line and subtitle_line == subtitle_line.upper() and len(subtitle_line) > 2:
            content_start += 1

        # Skip blank lines after subtitle
        while content_start < next_start and lines[content_start].strip() == "":
            content_start += 1

        rune_text = "\n".join(lines[content_start:next_start]).strip()
        # Clean up excessive blank lines
        rune_text = re.sub(r'\n{3,}', '\n\n', rune_text)

        runes.append({
            "num": num,
            "title": RUNE_TITLES.get(num, f"Rune {num}"),
            "text": rune_text
        })

    return runes


def extract_proem(text):
    """Extract the Proem (introductory poem)."""
    lines = text.split("\n")
    proem_start = None
    proem_end = None
    # Find the PROEM that's followed by actual verse text (not the one in TOC)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "PROEM":
            # Check if this is the actual poem (next non-blank line starts with verse text)
            for j in range(i + 1, min(i + 5, len(lines))):
                if lines[j].strip().startswith("Mastered") or (
                    lines[j].strip() and not lines[j].strip().startswith("RUNE") and
                    not lines[j].strip()[0].isdigit() and
                    len(lines[j].strip()) > 10
                ):
                    proem_start = i + 1
                    break
            if proem_start is not None:
                break
    if proem_start is not None:
        for i in range(proem_start, len(lines)):
            stripped = lines[i].strip()
            if re.match(r'^RUNE\s+I\.$', stripped):
                proem_end = i
                break
    if proem_start and proem_end:
        text = "\n".join(lines[proem_start:proem_end]).strip()
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text
    return None


# Thematic cycles of the Kalevala
CYCLES = {
    "wainamoinen": {
        "name": "The Wainamoinen Cycle",
        "runes": [1, 2, 3, 4, 5, 6, 7, 8, 16, 17, 18, 25, 39, 40, 41, 50],
        "about": "The great sage Wainamoinen, born of the primordial waters after seven hundred years of gestation, is the central hero of the Kalevala. He is the eternal singer, the first shaman, who creates the world through song and incantation. These runos follow his birth, his quest for a bride, his descent to Tuonela (the underworld), his building of the magical boat, and his final departure from the world when a new age dawns.",
        "for_readers": "Wainamoinen is not a warrior-hero but a wisdom figure — an ancient singer whose power lies in words, memory, and the ability to enchant. His story arc moves from cosmic creation to graceful departure, embodying the Finnish ideal of sisu (endurance) and the power of incantation."
    },
    "lemminkainen": {
        "name": "The Lemminkainen Cycle",
        "runes": [11, 12, 13, 14, 15, 26, 27, 28, 29, 30],
        "about": "Lemminkainen is the reckless adventurer, the trickster-hero who courts danger and dies only to be restored by his mother's devotion. His cycle includes his wooing of the Maiden of Pohyola, his death at the hands of the cowherder of Tuonela, and his mother's heroic gathering of his scattered body from the river of death — one of the Kalevala's most powerful passages.",
        "for_readers": "The Lemminkainen cycle contains the Kalevala's most vivid shamanic imagery: the journey to the underworld, the reassembly of a dismembered body, and the restoration of life. His mother's devotion is one of the great maternal archetypes in world mythology."
    },
    "kullervo": {
        "name": "The Kullervo Tragedy",
        "runes": [31, 32, 33, 34, 35, 36],
        "about": "The Kullervo cycle is the Kalevala's tragic core — a dark story of a slave-born hero driven by suffering and fate to commit terrible deeds, including unwitting incest with his sister. Unable to bear his guilt, Kullervo falls upon his own sword. Tolkien called this 'the germ of my attempt to write legends' and it directly inspired his tale of Túrin Turambar.",
        "for_readers": "The Kullervo cycle is the Kalevala's darkest and most psychologically modern passage. It is a tragedy of fate, abuse, and self-destruction that resonates with Greek tragedy and Norse saga. Tolkien's fascination with it shaped The Silmarillion."
    },
    "sampo": {
        "name": "The Quest for the Sampo",
        "runes": [10, 19, 20, 21, 22, 23, 24, 37, 38, 42, 43, 44],
        "about": "The Sampo is the Kalevala's central mystery — a magical artifact forged by the smith Ilmarinen as bride-price for the daughter of Louhi, mistress of Pohyola (the North). What is the Sampo? A world-mill that grinds out grain, salt, and gold? A cosmic axis? The runos of the Sampo cycle follow its forging, the wedding it purchases, and the great sea-battle for its capture, in which it shatters and its fragments bring fertility to the Finnish coast.",
        "for_readers": "The Sampo has been interpreted as a symbol of cosmic creation, economic wealth, and shamanic power. The quest to forge, win, and recover the Sampo is the Kalevala's great adventure narrative — binding together the three main heroes (Wainamoinen, Ilmarinen, Lemminkainen) in a shared quest."
    },
    "cosmic": {
        "name": "Creation, Fire, and the Cosmic Order",
        "runes": [1, 9, 45, 46, 47, 48, 49, 50],
        "about": "The Kalevala's cosmological runos tell of the creation of the world from a waterfowl's egg, the origin of iron and fire, the birth of disease, and the theft and restoration of the sun and moon. These runos anchor the epic in a mythic framework where natural forces have personalities and origins, and where the cosmic order must be continually maintained through ritual and incantation.",
        "for_readers": "These runos reveal the Kalevala's animist worldview: iron has a biography, fire has parents, diseases have a genealogy, and the sun can be stolen. They are the most explicitly mythological sections and connect Finnish belief to the wider Eurasian shamanic tradition."
    }
}


def build_grammar():
    raw_text = read_seed()
    text = strip_gutenberg(raw_text)

    proem_text = extract_proem(text)
    runes = extract_runes(text)

    items = []
    sort_order = 0
    rune_id_map = {}  # num -> id

    # Add Proem as L1 item
    if proem_text:
        item = {
            "id": "proem",
            "name": "Proem: The Singer's Invocation",
            "sort_order": sort_order,
            "category": "proem",
            "level": 1,
            "sections": {
                "Verse": proem_text
            },
            "keywords": ["invocation", "singer", "opening", "kalevala"],
            "metadata": {}
        }
        items.append(item)
        sort_order += 1

    # L1: Individual Runes
    for rune in runes:
        item_id = f"rune-{rune['num']:02d}"
        rune_id_map[rune['num']] = item_id

        keywords = []
        text_lower = rune['text'].lower()
        for kw in ["wainamoinen", "ilmarinen", "lemminkainen", "louhi", "sampo",
                    "kullervo", "tuonela", "pohyola", "aino", "ukko"]:
            if kw in text_lower:
                keywords.append(kw)

        item = {
            "id": item_id,
            "name": f"Rune {rune['num']}: {rune['title']}",
            "sort_order": sort_order,
            "category": f"rune",
            "level": 1,
            "sections": {
                "Verse": rune['text']
            },
            "keywords": keywords,
            "metadata": {
                "rune_number": rune['num']
            }
        }
        items.append(item)
        sort_order += 1

    # L2: Thematic cycles
    cycle_ids = []
    for cycle_key, cycle in CYCLES.items():
        cycle_id = f"cycle-{cycle_key}"
        cycle_ids.append(cycle_id)
        composite = [rune_id_map[n] for n in cycle["runes"] if n in rune_id_map]

        item = {
            "id": cycle_id,
            "name": cycle["name"],
            "sort_order": sort_order,
            "category": "cycle",
            "level": 2,
            "sections": {
                "About": cycle["about"],
                "For Readers": cycle["for_readers"]
            },
            "keywords": [],
            "metadata": {},
            "composite_of": composite,
            "relationship_type": "emergence"
        }
        items.append(item)
        sort_order += 1

    # L3: Meta
    meta_item = {
        "id": "kalevala-meta",
        "name": "The Kalevala: Epic Poem of Finland",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "The Kalevala is the Finnish national epic, compiled by Elias Lonnrot from oral folk poetry collected across Finland and Karelia. First published in 1835 (expanded 1849), it tells of the mythic heroes Wainamoinen (the eternal singer), Ilmarinen (the divine smith), and Lemminkainen (the reckless adventurer) in their struggles with Louhi, mistress of the dark Northland. The epic moves from cosmic creation through heroic quest to a twilight departure, and is the foundational text of Finnish identity.",
            "For Readers": "The Kalevala is best read aloud — its trochaic octameter (the same meter Longfellow borrowed for Hiawatha) creates a rolling, incantatory rhythm. It is not a single story but a tapestry of mythic cycles: creation, courtship, the forging of the Sampo, the tragedy of Kullervo, and the restoration of cosmic order. J.R.R. Tolkien considered it a primary inspiration for his own mythology."
        },
        "keywords": ["kalevala", "finnish", "epic", "mythology", "wainamoinen", "sampo", "creation"],
        "metadata": {},
        "composite_of": cycle_ids,
        "relationship_type": "emergence"
    }
    items.append(meta_item)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Elias Lonnrot", "date": "1849", "note": "Compiler of the Kalevala from Finnish oral poetry"},
                {"name": "John Martin Crawford", "date": "1888", "note": "English translation"}
            ]
        },
        "name": "The Kalevala",
        "description": "The Kalevala, the Finnish national epic compiled by Elias Lonnrot from oral folk poetry (1835/1849), in the English translation by John Martin Crawford (1888). Fifty runos (cantos) of creation myth, shamanic quest, heroic adventure, and cosmic drama — featuring Wainamoinen the eternal singer, Ilmarinen the divine smith, Lemminkainen the reckless hero, and the mysterious Sampo. The foundational text of Finnish identity and a primary inspiration for Tolkien's mythology.\n\nSource: Project Gutenberg eBook #5186 (https://www.gutenberg.org/ebooks/5186)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Akseli Gallen-Kallela's Kalevala paintings (1890s-1900s) — iconic Finnish national romantic art depicting key scenes. Joseph Alanen's Kalevala illustrations (1919). A.W. Finch and other Finnish Golden Age artists' Kalevala works.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["mythology", "finnish", "epic-poetry", "shamanism", "creation-myth", "public-domain", "full-text"],
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
    print(f"  L1 items (runos + proem): {l1}")
    print(f"  L2 items (cycles): {l2}")
    print(f"  L3 items (meta): {l3}")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
