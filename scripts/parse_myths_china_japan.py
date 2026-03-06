#!/usr/bin/env python3
"""
Parse Myths of China and Japan (Donald A. Mackenzie, Gutenberg #67344).
21 chapters → L1 items, grouped into L2 thematic clusters + L3 meta.
"""
import json, re, os

with open("seeds/myths-china-japan.txt", encoding="utf-8") as f:
    text = f.read()

gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()

CHAPTERS = [
    ("CHAPTER I", "ch01-dawn-civilization", "The Dawn of Civilization", "origins", ["civilization", "culture", "origins"]),
    ("CHAPTER II", "ch02-far-travelled-invention", "A Far-Travelled Invention", "origins", ["invention", "diffusion", "technology"]),
    ("CHAPTER III", "ch03-ancient-mariners", "Ancient Mariners and Explorers", "origins", ["maritime", "exploration", "trade"]),
    ("CHAPTER IV", "ch04-search-wealth", "The World-Wide Search for Wealth", "origins", ["wealth", "trade", "resources"]),
    ("CHAPTER V", "ch05-dragon-lore", "Chinese Dragon Lore", "dragon-myths", ["dragon", "lung", "rain", "emperor"]),
    ("CHAPTER VI", "ch06-bird-serpent", "Bird and Serpent Myths", "dragon-myths", ["phoenix", "serpent", "fenghuang", "garuda"]),
    ("CHAPTER VII", "ch07-dragon-folk-stories", "Dragon Folk-Stories", "dragon-myths", ["dragon", "folk-tale", "transformation"]),
    ("CHAPTER VIII", "ch08-kingdom-under-sea", "The Kingdom Under the Sea", "otherworld", ["sea", "dragon-king", "underwater", "palace"]),
    ("CHAPTER IX", "ch09-islands-blest", "The Islands of the Blest", "otherworld", ["islands", "immortality", "paradise", "penglai"]),
    ("CHAPTER X", "ch10-mother-goddess", "The Mother-Goddess of China and Japan", "deities", ["mother-goddess", "nuwa", "amaterasu", "guanyin"]),
    ("CHAPTER XI", "ch11-tree-herb-stone", "Tree-, Herb-, and Stone-Lore", "nature", ["tree", "herb", "jade", "sacred-plants"]),
    ("CHAPTER XII", "ch12-copper-culture", "How Copper-Culture Reached China", "origins", ["copper", "metallurgy", "bronze"]),
    ("CHAPTER XIII", "ch13-jade-symbolism", "The Symbolism of Jade", "nature", ["jade", "symbolism", "immortality", "virtue"]),
    ("CHAPTER XIV", "ch14-creation-myths", "Creation Myths and the God and Goddess Cults", "cosmology", ["creation", "pangu", "nuwa", "fuxi"]),
    ("CHAPTER XV", "ch15-mythical-kings", "Mythical and Legendary Kings", "history", ["huangdi", "yao", "shun", "yu", "sage-kings"]),
    ("CHAPTER XVI", "ch16-taoism", "Myths and Doctrines of Taoism", "philosophy", ["taoism", "laozi", "immortals", "alchemy"]),
    ("CHAPTER XVII", "ch17-japan-culture", "Culture Mixing in Japan", "japan", ["japan", "shinto", "buddhism", "culture"]),
    ("CHAPTER XVIII", "ch18-japanese-gods", "Japanese Gods and Dragons", "japan", ["kami", "dragon", "susanoo", "shinto"]),
    ("CHAPTER XIX", "ch19-rival-deities", "Rival Deities of Life and Death, Sunshine and Storm", "japan", ["amaterasu", "susanoo", "izanagi", "izanami"]),
    ("CHAPTER XX", "ch20-dragon-slayer", "The Dragon-Slayer and His Rival", "japan", ["yamato-takeru", "dragon", "hero", "sword"]),
    ("CHAPTER XXI", "ch21-ancient-mikados", "Ancient Mikados and Heroes", "japan", ["mikado", "emperor", "heroes", "history"]),
]

body_lines = body.split("\n")
positions = []
for heading, sid, name, cat, kw in CHAPTERS:
    pos = -1
    for i, line in enumerate(body_lines):
        if line.strip() == heading and i > 50:  # Skip TOC
            pos = sum(len(l) + 1 for l in body_lines[:i])
            break
    positions.append((pos, heading, sid, name, cat, kw))

positions.sort(key=lambda x: x[0] if x[0] >= 0 else 999999)

items = []
sort_order = 1

for idx, (pos, heading, sid, name, cat, kw) in enumerate(positions):
    if pos < 0:
        print(f"WARNING: Could not find '{heading}'")
        continue

    if idx + 1 < len(positions):
        end_pos = positions[idx + 1][0]
    else:
        end_pos = len(body)

    section_text = body[pos:end_pos].strip()
    lines = section_text.split("\n")
    content = []
    started = False
    for line in lines:
        if not started:
            stripped = line.strip()
            if stripped == "" or stripped == heading:
                continue
            if stripped.isupper() and len(stripped) > 5:
                continue
            if stripped.startswith("[Illustration"):
                continue
            if line.startswith("    ") and "—" in line:
                continue
            started = True
        content.append(line.rstrip())

    while content and content[-1].strip() == "":
        content.pop()

    full_text = "\n".join(content)
    if len(full_text) > 3000:
        bp = full_text.rfind(".", 0, 2800)
        if bp == -1:
            bp = 2800
        remaining = len(full_text[bp:].split())
        excerpt = full_text[:bp + 1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    else:
        excerpt = full_text

    items.append({
        "id": sid,
        "name": name,
        "sort_order": sort_order,
        "category": cat,
        "level": 1,
        "sections": {"Text": excerpt},
        "keywords": ["china", "japan", "east-asia", "mackenzie"] + kw,
        "metadata": {}
    })
    sort_order += 1

# Astrology metadata
astrology_map = {
    "ch05-dragon-lore": {"planets": ["Jupiter", "Neptune"], "signs": ["Sagittarius", "Pisces"], "themes": ["dragon", "rain", "imperial-power"]},
    "ch09-islands-blest": {"planets": ["Neptune", "Venus"], "signs": ["Pisces", "Taurus"], "themes": ["immortality", "paradise", "elixir"]},
    "ch10-mother-goddess": {"planets": ["Moon", "Venus"], "signs": ["Cancer", "Taurus"], "themes": ["mother-goddess", "creation", "compassion"]},
    "ch14-creation-myths": {"planets": ["Saturn", "Neptune"], "signs": ["Capricorn", "Pisces"], "themes": ["creation", "cosmic-egg", "yin-yang"]},
    "ch16-taoism": {"planets": ["Neptune", "Moon"], "signs": ["Pisces", "Cancer"], "themes": ["tao", "wu-wei", "immortality"]},
    "ch19-rival-deities": {"planets": ["Sun", "Mars"], "signs": ["Leo", "Aries"], "themes": ["amaterasu", "storm-god", "cosmic-conflict"]},
}
for item in items:
    if item["id"] in astrology_map:
        item["metadata"]["astrology"] = astrology_map[item["id"]]

# L2 groups
groups = [
    {
        "id": "group-chinese-mythology",
        "name": "Chinese Mythology: Dragons, Jade, and the Tao",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch05-dragon-lore", "ch06-bird-serpent", "ch07-dragon-folk-stories", "ch08-kingdom-under-sea",
                         "ch09-islands-blest", "ch10-mother-goddess", "ch11-tree-herb-stone", "ch13-jade-symbolism",
                         "ch14-creation-myths", "ch15-mythical-kings", "ch16-taoism"],
        "sections": {
            "About": "The mythological heart of China: dragon lore, the creation myth of Pangu, the cosmic mother Nüwa who repairs the sky, the Islands of the Blest where immortals dwell, the sacred symbolism of jade, and the mythical sage-kings (Yao, Shun, Yu) who governed by virtue. Plus the myths and doctrines of Taoism — the way that cannot be named.",
            "For Readers": "Start with Chapter V (Dragon Lore) for the most distinctive Chinese mythology, then Chapter XIV (Creation Myths) for Pangu and Nüwa, then Chapter XVI (Taoism) for the philosophical dimension."
        },
        "keywords": ["china", "dragon", "taoism", "creation"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "group-japanese-mythology",
        "name": "Japanese Mythology: Kami, Sun, and Storm",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch17-japan-culture", "ch18-japanese-gods", "ch19-rival-deities", "ch20-dragon-slayer", "ch21-ancient-mikados"],
        "sections": {
            "About": "Japanese mythology from the Kojiki and Nihon Shoki: the creation by Izanagi and Izanami, the sun goddess Amaterasu's withdrawal into the cave (plunging the world into darkness), the storm god Susanoo's wild deeds, the hero Yamato-takeru, and the divine origins of the imperial line.",
            "For Readers": "Chapter XIX (Rival Deities) tells the central myth — Amaterasu vs Susanoo — that still shapes Japanese culture and Shinto practice today."
        },
        "keywords": ["japan", "shinto", "amaterasu", "kami"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "group-cultural-origins",
        "name": "Cultural Origins: Trade, Technology, and Diffusion",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch01-dawn-civilization", "ch02-far-travelled-invention", "ch03-ancient-mariners", "ch04-search-wealth", "ch12-copper-culture"],
        "sections": {
            "About": "Mackenzie's argument that East Asian civilization was not isolated but connected to wider patterns of cultural diffusion — through trade routes, maritime exploration, and the spread of metallurgy. A product of its era's diffusionist theories, but contains valuable comparative mythology.",
            "For Readers": "These chapters provide historical context but are the most dated part of the book. Skip to the mythology chapters unless you're interested in early 20th-century theories of cultural diffusion."
        },
        "keywords": ["origins", "diffusion", "trade", "technology"],
        "relationship_type": "emergence",
        "metadata": {}
    },
]

for g in groups:
    g["sort_order"] = sort_order
    items.append(g)
    sort_order += 1

# L3 Meta
items.append({
    "id": "meta-china-japan",
    "name": "Myths of China and Japan: Where the Dragon Meets the Sun",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "Donald A. Mackenzie's 'Myths of China and Japan' (1923) surveys the mythologies of East Asia — from Chinese dragon lore and Taoist immortals to Japanese kami and the sun goddess Amaterasu. Mackenzie traces connections between East Asian myths and those of other civilizations, exploring how ideas about dragons, jade, the mother-goddess, and the otherworld traveled along ancient trade routes.",
        "Contemplation": "In China the dragon brings rain and blessing. In Europe the dragon hoards treasure and must be slain. Same creature, opposite meanings. What does this tell us about how cultures dream? And what happens when the myths finally meet — as they have in our globalized world?"
    },
    "keywords": ["china", "japan", "dragon", "amaterasu", "taoism", "mythology"],
    "composite_of": [i["id"] for i in items if i["level"] == 1],
    "relationship_type": "emergence",
    "metadata": {}
})
sort_order += 1

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Donald A. Mackenzie", "date": "1923", "note": "Original text: Myths of China and Japan"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, thematic groupings, astrology metadata, and meta interpretation"}
        ]
    },
    "name": "Myths of China and Japan",
    "description": "Donald A. Mackenzie's survey of East Asian mythology (1923) — Chinese dragon lore, creation myths of Pangu and Nüwa, Taoist immortals, Japanese kami, the sun goddess Amaterasu, and the hero Yamato-takeru. 21 chapters covering the mythological traditions of China and Japan.\n\nSource: Project Gutenberg eBook #67344 (https://www.gutenberg.org/ebooks/67344).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Traditional Chinese dragon paintings from the Ming and Qing dynasties. Ukiyo-e prints by Hokusai and Hiroshige depicting Japanese mythology. Shinto shrine art depicting Amaterasu emerging from the cave.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["mythology", "china", "japan", "dragon", "taoism", "shinto", "east-asia"],
    "roots": ["eastern-wisdom"],
    "shelves": ["wisdom", "wonder"],
    "lineages": ["Shrei"],
    "worldview": "animist",
    "items": items
}

os.makedirs("grammars/myths-china-japan", exist_ok=True)
with open("grammars/myths-china-japan/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

ids = [i["id"] for i in items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in items for r in i.get("composite_of", []) if r not in ids]
print(f"Items: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
print(f"Sections: {sum(len(i.get('sections',{})) for i in items)}")
print(f"Dupes: {dupes}, Bad refs: {bad_refs}")
print(f"Sort OK: {[i['sort_order'] for i in items] == list(range(1, len(items)+1))}")
