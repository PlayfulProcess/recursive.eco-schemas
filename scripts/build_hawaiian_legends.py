#!/usr/bin/env python3
"""
Build grammar.json for Legends of Old Honolulu from seeds/hawaiian-legends.txt
(Project Gutenberg #66547, W.D. Westervelt, 1916)

25 chapters of Hawaiian mythology and legends connected to Honolulu and Oahu.
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SEED_FILE = os.path.join(ROOT_DIR, "seeds", "hawaiian-legends.txt")
OUTPUT_DIR = os.path.join(ROOT_DIR, "grammars", "hawaiian-legends")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "grammar.json")

# Chapter definitions from the table of contents
CHAPTERS = [
    {"num": 1, "roman": "I", "title": "The Migration of the Hawaiians",
     "keywords": ["migration", "polynesia", "wakea", "voyage", "origins"]},
    {"num": 2, "roman": "II", "title": "Legendary Places in Honolulu",
     "keywords": ["honolulu", "places", "landmarks", "geography"]},
    {"num": 3, "roman": "III", "title": "The God of Pakaka Temple",
     "keywords": ["temple", "pakaka", "god", "worship"]},
    {"num": 4, "roman": "IV", "title": "Legend of the Bread-fruit Tree",
     "keywords": ["breadfruit", "ulu", "tree", "sacrifice", "magic"]},
    {"num": 5, "roman": "V", "title": "The Gods Who Found Water",
     "keywords": ["water", "gods", "kane", "kanaloa", "springs"]},
    {"num": 6, "roman": "VI", "title": "The Water of Life of Ka-ne",
     "keywords": ["kane", "water-of-life", "immortality", "sacred-water"]},
    {"num": 7, "roman": "VII", "title": "Mamala the Surf-rider",
     "keywords": ["surfing", "mamala", "shark", "ocean"]},
    {"num": 8, "roman": "VIII", "title": "A Shark Punished at Waikiki",
     "keywords": ["shark", "waikiki", "punishment", "ocean"]},
    {"num": 9, "roman": "IX", "title": "The Legendary Origin of Kapa",
     "keywords": ["kapa", "bark-cloth", "wauke", "craft", "origin"]},
    {"num": 10, "roman": "X", "title": "Creation of Man",
     "keywords": ["creation", "man", "kane", "origin", "humanity"]},
    {"num": 11, "roman": "XI", "title": "The Chief with the Wonderful Servants",
     "keywords": ["chief", "servants", "magic", "contest"]},
    {"num": 12, "roman": "XII", "title": "The Great Dog Ku",
     "keywords": ["dog", "ku", "supernatural", "guardian"]},
    {"num": 13, "roman": "XIII", "title": "The Cannibal Dog-man",
     "keywords": ["dog-man", "cannibal", "shapeshifter", "danger"]},
    {"num": 14, "roman": "XIV", "title": "The Canoe of the Dragon",
     "keywords": ["canoe", "dragon", "mo-o", "supernatural", "water"]},
    {"num": 15, "roman": "XV", "title": "The Wonderful Shell",
     "keywords": ["shell", "magic", "ocean", "treasure"]},
    {"num": 16, "roman": "XVI", "title": "The Ghost Dance on Punchbowl",
     "keywords": ["ghost", "dance", "punchbowl", "spirits", "night-marchers"]},
    {"num": 17, "roman": "XVII", "title": "The Bird-man of Nuuanu Valley",
     "keywords": ["bird-man", "nuuanu", "flight", "supernatural"]},
    {"num": 18, "roman": "XVIII", "title": "The Owls of Honolulu",
     "keywords": ["owls", "pueo", "guardian", "battle", "honolulu"]},
    {"num": 19, "roman": "XIX", "title": "The Two Fish from Tahiti",
     "keywords": ["fish", "tahiti", "voyage", "ocean", "supernatural"]},
    {"num": 20, "roman": "XX", "title": "Iwa, the Notable Thief of Oahu",
     "keywords": ["thief", "iwa", "trickster", "cleverness", "oahu"]},
    {"num": 21, "roman": "XXI", "title": "Pikoi the Rat-killer",
     "keywords": ["pikoi", "rat", "archery", "skill", "contest"]},
    {"num": 22, "roman": "XXII", "title": "Kawelo",
     "keywords": ["kawelo", "warrior", "kauai", "strength", "battle"]},
    {"num": 23, "roman": "XXIII", "title": "Chief Man-eater",
     "keywords": ["cannibal", "chief", "man-eater", "horror", "historical"]},
    {"num": 24, "roman": "XXIV", "title": "Lepe-a-moa",
     "keywords": ["lepe-a-moa", "bird-child", "magic", "transformation"]},
    {"num": 25, "roman": "XXV", "title": "Kamapuaa Legends",
     "keywords": ["kamapuaa", "hog-god", "shapeshifter", "pele", "trickster"]},
]


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


def strip_footnotes(text):
    """Remove footnote markers like [1], [2] etc."""
    return re.sub(r'\s*\[\d+\]', '', text)


def extract_chapters(text):
    """Extract 25 chapters from the text."""
    lines = text.split("\n")

    # Build a map of roman numerals to line numbers
    roman_map = {}
    for ch in CHAPTERS:
        roman = ch["roman"]
        # Search for the roman numeral as a standalone line
        for i, line in enumerate(lines):
            if line.strip() == roman:
                # Verify: next non-blank line should be the chapter title (or close to it)
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip():
                        # Check if the title matches (at least partially)
                        title_words = ch["title"].upper().split()[:3]
                        line_upper = lines[j].strip().upper()
                        if any(w in line_upper for w in title_words):
                            roman_map[ch["num"]] = i
                            break
                if ch["num"] in roman_map:
                    break

    # Find APPENDIX as end marker
    appendix_line = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == "APPENDIX":
            appendix_line = i
            break

    chapters = []
    sorted_nums = sorted(roman_map.keys())

    for idx, num in enumerate(sorted_nums):
        start_line = roman_map[num]

        # Find end (next chapter start or appendix)
        if idx + 1 < len(sorted_nums):
            end_line = roman_map[sorted_nums[idx + 1]]
        else:
            end_line = appendix_line

        # Skip the roman numeral line and title lines
        content_start = start_line + 1
        # Skip blank lines
        while content_start < end_line and lines[content_start].strip() == "":
            content_start += 1
        # Skip the title line(s) - they're in ALL CAPS
        while content_start < end_line:
            stripped = lines[content_start].strip()
            if stripped and stripped == stripped.upper() and len(stripped) > 2:
                content_start += 1
            elif stripped == "":
                content_start += 1
            else:
                break

        ch_text = "\n".join(lines[content_start:end_line]).strip()
        ch_text = strip_footnotes(ch_text)
        ch_text = re.sub(r'\n{3,}', '\n\n', ch_text)

        # Find the matching chapter definition
        ch_def = next(c for c in CHAPTERS if c["num"] == num)
        chapters.append({
            "num": num,
            "title": ch_def["title"],
            "keywords": ch_def["keywords"],
            "text": ch_text
        })

    return chapters


# Thematic groupings
THEMES = [
    {
        "id": "theme-gods-creation",
        "name": "Gods, Creation, and Sacred Waters",
        "chapters": [5, 6, 10],
        "about": "The foundational myths of Hawaiian cosmology: how the gods Kane and Kanaloa found water, the sacred Water of Life (Wai-ola) that grants immortality, and the creation of humanity. Water is the central sacred element in these legends — Hawaiian gods are water-finders, and the first humans are shaped from the red earth moistened by the gods' own power.",
        "for_readers": "These legends reveal a worldview where divinity flows like water through the landscape. Every spring and stream in Honolulu carries the memory of the gods who opened the earth. The creation story connects humanity directly to the land (aina) — a relationship that remains central to Hawaiian identity."
    },
    {
        "id": "theme-shapeshifters",
        "name": "Shapeshifters and Supernatural Beings",
        "chapters": [7, 8, 12, 13, 14, 17, 25],
        "about": "Hawaiian legends are populated with beings who shift between human and animal forms: the shark-riders, the great dog Ku, the cannibal dog-man, the dragon of the canoe, the bird-man of Nuuanu Valley, and above all Kamapuaa the hog-god. These shape-shifting figures blur the boundary between human and animal, expressing the Hawaiian understanding that all life shares a common spiritual essence (mana).",
        "for_readers": "In Hawaiian thought, animals are not lesser beings but aumakua (guardian spirits) and ancestors. A shark might be a family protector; a dog might carry divine power. These legends show a world where transformation between forms is natural, and the boundaries between species are permeable."
    },
    {
        "id": "theme-spirits-ghosts",
        "name": "Spirits, Ghosts, and the Otherworld",
        "chapters": [15, 16, 18, 19, 24],
        "about": "The spirit world lies close to the surface in old Honolulu. Ghost dancers perform on Punchbowl Hill, owls battle to protect the innocent, mysterious fish arrive from Tahiti bearing supernatural power, and the bird-child Lepe-a-moa moves between human and spirit forms. These legends map the invisible geography of Oahu — the places where the boundary between the living and the dead grows thin.",
        "for_readers": "The Hawaiian spirit world is not distant but immediately present in the landscape. Punchbowl, Nuuanu Valley, Waikiki — these are not just places but portals. The legends teach that the dead walk among us, that guardian spirits (aumakua) watch over families, and that the night belongs to the spirit marchers."
    },
    {
        "id": "theme-heroes-tricksters",
        "name": "Heroes, Warriors, and Tricksters",
        "chapters": [11, 20, 21, 22, 23],
        "about": "The human heroes of old Honolulu: the chief with wonderful servants who wins impossible contests, Iwa the master thief whose cleverness outstrips all rivals, Pikoi the supernatural archer who kills rats at impossible distances, Kawelo the mighty warrior who conquers Kauai, and the terrifying Chief Man-eater. These are the stories of human excellence pushed to supernatural heights.",
        "for_readers": "Hawaiian hero stories celebrate different kinds of excellence: physical strength (Kawelo), cunning and stealth (Iwa), precision skill (Pikoi), and leadership (the chief with wonderful servants). Notice how even the darkest figure, Chief Man-eater, serves as a boundary marker — showing what happens when power is severed from community."
    },
    {
        "id": "theme-origins-places",
        "name": "Origins, Migrations, and Sacred Places",
        "chapters": [1, 2, 3, 4, 9],
        "about": "How the Hawaiians came to be where they are: the great Polynesian migration across the Pacific, the legendary places of Honolulu and their stories, the god of Pakaka Temple, the magical breadfruit tree that was once a man, and the origin of kapa (bark cloth). These legends root Hawaiian culture in specific places and explain how the arts of civilization came to the islands.",
        "for_readers": "These legends connect the Hawaiian people to a vast Pacific world — ancestors who navigated by stars across thousands of miles of open ocean. Every place in Honolulu carries a story that reaches back to Tahiti, to the homeland Kahiki, and ultimately to the deep past of Polynesian migration."
    }
]


def build_grammar():
    raw_text = read_seed()
    text = strip_gutenberg(raw_text)
    chapters = extract_chapters(text)

    print(f"Extracted {len(chapters)} chapters")

    items = []
    sort_order = 0
    ch_id_map = {}

    # L1: Individual chapters (legends)
    for ch in chapters:
        item_id = f"legend-{ch['num']:02d}"
        ch_id_map[ch['num']] = item_id

        items.append({
            "id": item_id,
            "name": ch["title"],
            "sort_order": sort_order,
            "category": "legend",
            "level": 1,
            "sections": {
                "Legend": ch["text"]
            },
            "keywords": ch["keywords"],
            "metadata": {"chapter_number": ch["num"]}
        })
        sort_order += 1

    # L2: Thematic groupings
    theme_ids = []
    for theme in THEMES:
        composite = [ch_id_map[n] for n in theme["chapters"] if n in ch_id_map]
        items.append({
            "id": theme["id"],
            "name": theme["name"],
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"]
            },
            "keywords": [],
            "metadata": {},
            "composite_of": composite,
            "relationship_type": "emergence"
        })
        theme_ids.append(theme["id"])
        sort_order += 1

    # L3: Meta
    meta_item = {
        "id": "hawaiian-legends-meta",
        "name": "Legends of Old Honolulu",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Legends of Old Honolulu, collected and translated from the Hawaiian by W.D. Westervelt (1916). Twenty-five legends rooted in the places, gods, and heroes of Honolulu and the island of Oahu — from the great Polynesian migration to the exploits of Kamapuaa the hog-god. These are the myths that live in the landscape: every valley, reef, spring, and hill in Honolulu carries a story of gods, shapeshifters, ghost dancers, and ancestral heroes.",
            "For Readers": "Westervelt gathered these legends from Hawaiian-language newspapers and from elders who still remembered the old stories. They reveal a world where the natural and supernatural are inseparable, where animals are ancestors, where water is sacred, and where the spirits of the dead walk the hills at night. Read them with a map of Honolulu beside you — the places are real, and the legends still inhabit them."
        },
        "keywords": ["hawaiian", "polynesian", "honolulu", "oahu", "mythology", "legends"],
        "metadata": {},
        "composite_of": theme_ids,
        "relationship_type": "emergence"
    }
    items.append(meta_item)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "W.D. Westervelt", "date": "1916", "note": "Collector and translator"},
                {"name": "Hawaiian oral tradition", "date": "pre-contact to 19th century", "note": "Original sources"}
            ]
        },
        "name": "Legends of Old Honolulu",
        "description": "Legends of Old Honolulu (Mythology), collected and translated from the Hawaiian by W.D. Westervelt (1916). Twenty-five legends of gods, shapeshifters, ghost dancers, and heroes rooted in the places of Honolulu and Oahu — the Polynesian migration, the sacred Water of Life, Kamapuaa the hog-god, the ghost dance on Punchbowl, the owls of Honolulu, and more. A window into the Hawaiian mythological imagination where landscape and story are inseparable.\n\nSource: Project Gutenberg eBook #66547 (https://www.gutenberg.org/ebooks/66547)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: The original 1916 Ellis Press edition includes photographs of Honolulu landscapes. Charles W. Bartlett's Hawaiian color woodblock prints (1910s-1920s). D. Howard Hitchcock's landscape paintings of Hawaii (early 1900s). Arman Manookian's Hawaiian art (1920s).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["mythology", "hawaiian", "polynesian", "legends", "shapeshifters", "public-domain", "full-text"],
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
    print(f"  L1 items (legends): {l1}")
    print(f"  L2 items (themes): {l2}")
    print(f"  L3 items (meta): {l3}")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
