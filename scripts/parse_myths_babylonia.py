#!/usr/bin/env python3
"""
Parse Myths of Babylonia and Assyria (Donald A. Mackenzie, Gutenberg #16653).
20 chapters + preface + introduction → L1 items, grouped into L2 thematic clusters + L3 meta.
"""
import json, re, os

with open("seeds/myths-babylonia-assyria.txt", encoding="utf-8") as f:
    text = f.read()

gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()

# Chapter definitions: (heading_pattern, id, name, category, keywords)
CHAPTERS = [
    ("PREFACE", "preface", "Preface", "framework", ["introduction", "mesopotamia", "overview"]),
    ("INTRODUCTION", "introduction", "Introduction", "framework", ["mesopotamia", "sumer", "akkad", "overview"]),
    ("CHAPTER I.", "ch01-races-civilization", "The Races and Early Civilization of Babylonia", "origins", ["sumer", "akkad", "civilization", "prehistoric"]),
    ("CHAPTER II.", "ch02-land-rivers-god-deep", "The Land of Rivers and the God of the Deep", "deities", ["ea", "enki", "tigris", "euphrates", "eridu"]),
    ("CHAPTER III.", "ch03-rival-pantheons", "Rival Pantheons and Representative Deities", "deities", ["enlil", "anu", "ishtar", "shamash", "sin"]),
    ("CHAPTER IV.", "ch04-demons-fairies-ghosts", "Demons, Fairies, and Ghosts", "spirits", ["demons", "lilith", "utukku", "lamassu", "incantation"]),
    ("CHAPTER V.", "ch05-tammuz-ishtar", "Myths of Tammuz and Ishtar", "deities", ["tammuz", "ishtar", "descent", "underworld", "dying-god"]),
    ("CHAPTER VI.", "ch06-wars-city-states", "Wars of the City States of Sumer and Akkad", "history", ["sargon", "ur", "lagash", "warfare"]),
    ("CHAPTER VII.", "ch07-creation-merodach", "Creation Legend: Merodach the Dragon Slayer", "myths", ["marduk", "tiamat", "creation", "dragon", "enuma-elish"]),
    ("CHAPTER VIII.", "ch08-etana-gilgamesh", "Deified Heroes: Etana and Gilgamesh", "myths", ["gilgamesh", "etana", "enkidu", "hero", "immortality"]),
    ("CHAPTER IX.", "ch09-deluge-hades", "Deluge Legend, the Island of the Blessed, and Hades", "myths", ["flood", "utnapishtim", "underworld", "ereshkigal"]),
    ("CHAPTER X.", "ch10-buildings-laws", "Buildings and Laws and Customs of Babylon", "history", ["hammurabi", "law", "ziggurats", "customs"]),
    ("CHAPTER XI.", "ch11-golden-age", "The Golden Age of Babylonia", "history", ["hammurabi", "golden-age", "prosperity"]),
    ("CHAPTER XII.", "ch12-hittites-kassites", "Rise of the Hittites, Mitannians, Kassites, Hyksos, and Assyrians", "history", ["hittites", "mitanni", "kassites", "hyksos", "invasion"]),
    ("CHAPTER XIII.", "ch13-astrology-astronomy", "Astrology and Astronomy", "wisdom", ["astrology", "astronomy", "zodiac", "omens", "planets"]),
    ("CHAPTER XIV.", "ch14-ashur", "Ashur the National God of Assyria", "deities", ["ashur", "assyria", "national-god", "war-god"]),
    ("CHAPTER XV.", "ch15-trade-supremacy", "Conflicts for Trade and Supremacy", "history", ["trade", "warfare", "empire", "conquest"]),
    ("CHAPTER XVI.", "ch16-race-movements", "Race Movements that Shattered Empires", "history", ["migration", "empire", "collapse", "arameans"]),
    ("CHAPTER XVII.", "ch17-hebrews-assyria", "The Hebrews in Assyrian History", "history", ["hebrews", "israel", "judah", "sennacherib", "bible"]),
    ("CHAPTER XVIII.", "ch18-semiramis", "The Age of Semiramis", "history", ["semiramis", "babylon", "queen", "legend"]),
    ("CHAPTER XIX.", "ch19-splendour", "Assyria's Age of Splendour", "history", ["ashurbanipal", "nineveh", "library", "empire"]),
    ("CHAPTER XX.", "ch20-last-days", "The Last Days of Assyria and Babylonia", "history", ["fall", "nebuchadnezzar", "cyrus", "persian-conquest"]),
]

# Find positions
body_lines = body.split("\n")
positions = []
for heading, sid, name, cat, kw in CHAPTERS:
    pos = -1
    for i, line in enumerate(body_lines):
        if line.strip() == heading:
            pos = sum(len(l) + 1 for l in body_lines[:i])
            break
    if pos < 0:
        # Fallback: case-insensitive
        for i, line in enumerate(body_lines):
            if line.strip().upper() == heading.upper():
                pos = sum(len(l) + 1 for l in body_lines[:i])
                break
    positions.append((pos, heading, sid, name, cat, kw))

# Sort by position
positions.sort(key=lambda x: x[0] if x[0] >= 0 else 999999)

items = []
sort_order = 1

for idx, (pos, heading, sid, name, cat, kw) in enumerate(positions):
    if pos < 0:
        print(f"WARNING: Could not find '{heading}'")
        continue

    # Find end position
    if idx + 1 < len(positions):
        end_pos = positions[idx + 1][0]
    else:
        end_pos = len(body)

    section_text = body[pos:end_pos].strip()
    # Remove heading lines
    lines = section_text.split("\n")
    content = []
    started = False
    for line in lines:
        if not started:
            stripped = line.strip()
            if stripped == "" or stripped == heading or stripped == heading.rstrip("."):
                continue
            # Skip chapter title line (ALL CAPS following chapter number)
            if stripped.isupper() and len(stripped) > 5:
                continue
            # Skip synopsis lines (indented italics-style summaries)
            if line.startswith("  ") and "--" in line:
                continue
            started = True
        content.append(line.rstrip())

    while content and content[-1].strip() == "":
        content.pop()

    full_text = "\n".join(content)

    # Truncate
    if len(full_text) > 3000:
        bp = full_text.rfind(".", 0, 2800)
        if bp == -1:
            bp = 2800
        remaining = len(full_text[bp:].split())
        excerpt = full_text[:bp + 1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    else:
        excerpt = full_text

    level = 1
    if cat == "framework":
        level = 2

    items.append({
        "id": sid,
        "name": name,
        "sort_order": sort_order,
        "category": cat,
        "level": level,
        "sections": {"Text": excerpt},
        "keywords": ["babylonia", "assyria", "mesopotamia", "mackenzie"] + kw,
        "metadata": {}
    })
    sort_order += 1

# Astrology metadata for key chapters
astrology_map = {
    "ch05-tammuz-ishtar": {"planets": ["Venus", "Pluto"], "signs": ["Scorpio", "Taurus"], "themes": ["descent", "dying-god", "fertility"]},
    "ch07-creation-merodach": {"planets": ["Jupiter", "Mars"], "signs": ["Aries", "Sagittarius"], "themes": ["creation", "dragon-slaying", "cosmic-order"]},
    "ch08-etana-gilgamesh": {"planets": ["Sun", "Saturn"], "signs": ["Leo", "Capricorn"], "themes": ["heroic-quest", "mortality", "immortality"]},
    "ch09-deluge-hades": {"planets": ["Neptune", "Pluto"], "signs": ["Pisces", "Scorpio"], "themes": ["flood", "underworld", "death-rebirth"]},
    "ch13-astrology-astronomy": {"planets": ["Mercury", "Saturn"], "signs": ["Gemini", "Aquarius"], "themes": ["divination", "celestial-order", "zodiac"]},
    "ch14-ashur": {"planets": ["Mars", "Sun"], "signs": ["Aries", "Leo"], "themes": ["war-god", "national-deity", "sovereignty"]},
    "ch04-demons-fairies-ghosts": {"planets": ["Pluto", "Neptune"], "signs": ["Scorpio", "Pisces"], "themes": ["spirits", "protection", "shadow"]},
}

for item in items:
    if item["id"] in astrology_map:
        item["metadata"]["astrology"] = astrology_map[item["id"]]

# L2 thematic groups
groups = [
    {
        "id": "group-gods-myths",
        "name": "Gods, Myths, and the Otherworld",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch02-land-rivers-god-deep", "ch03-rival-pantheons", "ch04-demons-fairies-ghosts",
                         "ch05-tammuz-ishtar", "ch07-creation-merodach", "ch08-etana-gilgamesh", "ch09-deluge-hades"],
        "sections": {
            "About": "The mythological core of Mesopotamian civilization: the great gods (Ea, Enlil, Anu, Ishtar, Marduk, Ashur), the spirits and demons that populated the invisible world, and the epic stories — the descent of Ishtar, the creation battle against Tiamat, the wanderings of Gilgamesh, and the great flood. These myths shaped every subsequent Western mythology.",
            "For Readers": "Start with Chapter V (Tammuz and Ishtar) for the archetypal dying-god myth, then Chapter VII (Creation Legend) for the cosmic battle that echoes through Genesis and Greek mythology, then Chapter VIII (Gilgamesh) for the oldest hero's journey in world literature."
        },
        "keywords": ["mythology", "gods", "creation", "underworld"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "group-history-empire",
        "name": "Empire, History, and the Rise and Fall of Powers",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch01-races-civilization", "ch06-wars-city-states", "ch10-buildings-laws", "ch11-golden-age",
                         "ch12-hittites-kassites", "ch15-trade-supremacy", "ch16-race-movements",
                         "ch17-hebrews-assyria", "ch18-semiramis", "ch19-splendour", "ch20-last-days"],
        "sections": {
            "About": "The historical narrative of Mesopotamia from the earliest Sumerian city-states through the rise and fall of Babylon and Assyria — spanning over three thousand years. Mackenzie traces the interplay of warfare, trade, law, and cultural exchange that shaped the ancient world.",
            "For Readers": "Start with Chapter X (Buildings and Laws) for Hammurabi's Babylon, then read Chapters XIX-XX for the dramatic collapse of the greatest empires of antiquity."
        },
        "keywords": ["history", "empire", "warfare", "civilization"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "group-astrology-wisdom",
        "name": "Stars, Wisdom, and Sacred Knowledge",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch13-astrology-astronomy", "ch14-ashur"],
        "sections": {
            "About": "Babylonian astrology and astronomy — the origin of the zodiac, planetary divination, and the relationship between celestial observation and religious authority. Includes the theology of Ashur, Assyria's supreme god who merged stellar and martial symbolism.",
            "For Readers": "Chapter XIII is essential reading for anyone interested in the origins of astrology — the Babylonians created the system that still underlies Western astrology today."
        },
        "keywords": ["astrology", "astronomy", "wisdom", "divination"],
        "relationship_type": "emergence",
        "metadata": {}
    },
]

for g in groups:
    g["sort_order"] = sort_order
    items.append(g)
    sort_order += 1

# L3 Meta card
items.append({
    "id": "meta-mesopotamia",
    "name": "Mesopotamia: Where Civilization Wrote Its Dreams",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "Donald A. Mackenzie's 'Myths of Babylonia and Assyria' (1915) is a comprehensive survey of Mesopotamian mythology and history — from the creation epic Enuma Elish to the fall of Babylon to Cyrus the Great. Mackenzie weaves together the great myths (Tammuz and Ishtar's descent, Gilgamesh's quest for immortality, Marduk's battle against the chaos-dragon Tiamat) with three millennia of political history. This is the civilization that invented writing, the zodiac, the seven-day week, and the flood story that echoes in Genesis. Every Western mythology carries Mesopotamian DNA.",
        "Contemplation": "The Babylonians looked at the same sky we look at and saw the same patterns — but they saw gods where we see physics. Their astrology became our astronomy. Their flood story became Noah. Their Ishtar became Aphrodite became Venus. What does it mean that our most 'modern' ideas are thirty centuries old?"
    },
    "keywords": ["mesopotamia", "civilization", "mythology", "astrology", "creation"],
    "composite_of": [i["id"] for i in items if i["level"] == 1],
    "relationship_type": "emergence",
    "metadata": {}
})
sort_order += 1

# Build grammar
grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Donald A. Mackenzie", "date": "1915", "note": "Original text: Myths of Babylonia and Assyria"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, thematic groupings, astrology metadata, and meta interpretation"}
        ]
    },
    "name": "Myths of Babylonia and Assyria",
    "description": "Donald A. Mackenzie's comprehensive survey of Mesopotamian mythology and history (1915) — from the creation epic Enuma Elish and the descent of Ishtar to the fall of Babylon. Covers the gods (Ea, Enlil, Marduk, Ishtar, Tammuz), the epic of Gilgamesh, Babylonian astrology, and three millennia of empire.\n\nSource: Project Gutenberg eBook #16653 (https://www.gutenberg.org/ebooks/16653).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Mesopotamian cylinder seal impressions from the British Museum collections. Austen Henry Layard's drawings of Assyrian palace reliefs (1849). Bas-reliefs from Nineveh showing winged bulls (lamassu) and battle scenes.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["mythology", "mesopotamia", "babylonia", "assyria", "ancient-history", "astrology", "creation-myth"],
    "roots": ["western-philosophy", "mysticism"],
    "shelves": ["wisdom"],
    "lineages": ["Shrei", "Akomolafe"],
    "worldview": "animist",
    "items": items
}

os.makedirs("grammars/myths-babylonia-assyria", exist_ok=True)
with open("grammars/myths-babylonia-assyria/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

# Validate
ids = [i["id"] for i in items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in items for r in i.get("composite_of", []) if r not in ids]
print(f"Items: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
print(f"Sections: {sum(len(i.get('sections',{})) for i in items)}")
print(f"Dupes: {dupes}, Bad refs: {bad_refs}")
print(f"Sort OK: {[i['sort_order'] for i in items] == list(range(1, len(items)+1))}")
