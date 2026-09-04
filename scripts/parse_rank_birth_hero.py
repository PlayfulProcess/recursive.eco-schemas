#!/usr/bin/env python3
"""
Parse The Myth of the Birth of the Hero (Otto Rank, 1914, Gutenberg #66192).
15 hero myths + introduction + interpretation chapters.
"""
import json, re, os

with open("seeds/myth-birth-hero-rank.txt", encoding="utf-8") as f:
    text = f.read()

gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()

# Hero sections in order (heading text as it appears centered)
SECTIONS = [
    ("INTRODUCTION", "introduction", "Introduction: The Hero Pattern"),
    ("SARGON", "sargon", "Sargon of Akkad"),
    ("MOSES", "moses", "Moses"),
    ("KARNA", "karna", "Karna"),
    ("ŒDIPUS", "oedipus", "Oedipus"),
    ("PARIS", "paris", "Paris"),
    ("TELEPHOS", "telephos", "Telephos"),
    ("PERSEUS", "perseus", "Perseus"),
    ("GILGAMOS", "gilgamos", "Gilgamos (Gilgamesh)"),
    ("KYROS", "kyros", "Kyros (Cyrus the Great)"),
    ("TRISTAN", "tristan", "Tristan"),
    ("ROMULUS.", "romulus", "Romulus"),
    ("HERCULES[60]", "hercules", "Hercules"),
    ("Jesus", "jesus", "Jesus"),
    ("SIEGFRIED", "siegfried", "Siegfried"),
    ("LOHENGRIN", "lohengrin", "Lohengrin"),
]

# Find positions by scanning lines
body_lines = body.split("\n")
positions = []
for heading, sid, name in SECTIONS:
    pos = -1
    for i, line in enumerate(body_lines):
        if line.strip() == heading and len(line) - len(line.lstrip()) > 20:
            # Calculate byte position
            pos = sum(len(l) + 1 for l in body_lines[:i])
            break
    if pos < 0:
        # Try case-insensitive
        for i, line in enumerate(body_lines):
            if line.strip().upper() == heading.upper() and len(line) - len(line.lstrip()) > 20:
                pos = sum(len(l) + 1 for l in body_lines[:i])
                break
    positions.append((pos, heading, sid, name))

# Sort by position
positions.sort(key=lambda x: x[0] if x[0] >= 0 else 999999)

# The interpretation section starts after Lohengrin
# Find it — it's the text after the last hero myth that starts with analysis
interp_start = body.find("On inverting the Lohengrin saga")
if interp_start > 0:
    positions.append((interp_start, "INTERPRETATION", "interpretation", "The Hero Pattern: Rank's Interpretation"))

# Find INDEX
index_pos = body.find("\n" + " " * 20 + "INDEX")
if index_pos < 0:
    index_pos = len(body)

items = []
sort_order = 1

for idx, (pos, heading, sid, name) in enumerate(positions):
    if pos < 0:
        print(f"WARNING: Could not find '{heading}'")
        continue

    # Find end position
    if idx + 1 < len(positions):
        end_pos = positions[idx + 1][0]
    else:
        end_pos = index_pos

    section_text = body[pos:end_pos].strip()
    # Remove heading line
    lines = section_text.split("\n")
    content = []
    started = False
    for line in lines:
        if not started:
            if line.strip() == "" or line.strip() in [heading, heading.rstrip(".")]:
                continue
            # Check if this is still heading material
            if line.strip().startswith("[") and line.strip().endswith("]"):
                continue
            started = True
        content.append(line.rstrip())

    while content and content[-1].strip() == "":
        content.pop()

    full_text = "\n".join(content)

    # Truncate long sections
    if len(full_text) > 3000:
        bp = full_text.rfind(".", 0, 2800)
        if bp == -1:
            bp = 2800
        remaining = len(full_text[bp:].split())
        excerpt = full_text[:bp + 1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    else:
        excerpt = full_text

    # Determine category and level
    if sid in ("introduction", "interpretation"):
        cat = "framework"
        level = 2
    else:
        cat = "hero-myths"
        level = 1

    # Keywords based on hero
    hero_keywords = {
        "sargon": ["babylonian", "river", "vestal", "gardener"],
        "moses": ["hebrew", "ark", "river", "pharaoh", "bulrushes"],
        "karna": ["indian", "sun-god", "river", "earrings", "armor"],
        "oedipus": ["greek", "exposed", "ankles", "sphinx", "fate"],
        "paris": ["trojan", "exposed", "shepherd", "apple", "beauty"],
        "telephos": ["greek", "exposed", "deer", "suckled"],
        "perseus": ["greek", "chest", "sea", "danae", "oracle"],
        "gilgamos": ["babylonian", "tower", "eagle", "gardener"],
        "kyros": ["persian", "dream", "exposed", "shepherd", "empire"],
        "tristan": ["celtic", "orphan", "sea", "knight", "love"],
        "romulus": ["roman", "twins", "she-wolf", "river", "founding"],
        "hercules": ["greek", "serpents", "divine-father", "labors"],
        "jesus": ["hebrew", "virgin-birth", "manger", "star", "persecution"],
        "siegfried": ["germanic", "dragon", "invulnerable", "forest"],
        "lohengrin": ["germanic", "swan", "grail", "forbidden-question"],
    }

    # Astrology metadata for each hero
    hero_astrology = {
        "sargon": {"planets": ["Saturn", "Jupiter"], "signs": ["Capricorn"], "themes": ["king-founder", "river-exposure"]},
        "moses": {"planets": ["Saturn", "Neptune"], "signs": ["Pisces"], "themes": ["divine-mission", "water-rescue"]},
        "karna": {"planets": ["Sun", "Mars"], "signs": ["Leo", "Aries"], "themes": ["solar-hero", "abandoned-warrior"]},
        "oedipus": {"planets": ["Sun", "Saturn", "Pluto"], "signs": ["Leo", "Capricorn"], "themes": ["fate", "self-knowledge"]},
        "paris": {"planets": ["Venus", "Mars"], "signs": ["Libra"], "themes": ["beauty-judgment", "doomed-love"]},
        "telephos": {"planets": ["Mars", "Moon"], "signs": ["Aries"], "themes": ["wound", "suckled-by-deer"]},
        "perseus": {"planets": ["Mars", "Jupiter"], "signs": ["Aries", "Sagittarius"], "themes": ["sea-chest", "divine-quest"]},
        "gilgamos": {"planets": ["Saturn", "Mars"], "signs": ["Capricorn"], "themes": ["tower", "mortality"]},
        "kyros": {"planets": ["Jupiter", "Saturn"], "signs": ["Sagittarius", "Capricorn"], "themes": ["empire", "dream-prophecy"]},
        "tristan": {"planets": ["Venus", "Neptune"], "signs": ["Pisces", "Libra"], "themes": ["orphan", "tragic-love"]},
        "romulus": {"planets": ["Mars", "Jupiter"], "signs": ["Aries", "Leo"], "themes": ["twins", "she-wolf", "city-founding"]},
        "hercules": {"planets": ["Sun", "Mars"], "signs": ["Leo", "Aries"], "themes": ["divine-strength", "serpent-slaying"]},
        "jesus": {"planets": ["Sun", "Neptune"], "signs": ["Pisces"], "themes": ["virgin-birth", "divine-child"]},
        "siegfried": {"planets": ["Mars", "Sun"], "signs": ["Aries", "Leo"], "themes": ["dragon-slayer", "invulnerability"]},
        "lohengrin": {"planets": ["Neptune", "Moon"], "signs": ["Pisces", "Cancer"], "themes": ["swan-knight", "forbidden-question"]},
    }

    metadata = {"origin": "comparative"}
    if sid in hero_astrology:
        metadata["astrology"] = hero_astrology[sid]

    items.append({
        "id": sid,
        "name": name,
        "sort_order": sort_order,
        "category": cat,
        "level": level,
        "sections": {
            "Text": excerpt
        },
        "keywords": ["rank", "hero-myth", "birth"] + hero_keywords.get(sid, []),
        "metadata": metadata
    })
    sort_order += 1

# L3 Meta card
items.append({
    "id": "meta-hero-pattern",
    "name": "The Hero Pattern: Why the Same Birth Story?",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "Otto Rank identified a single pattern recurring across fifteen hero myths spanning Babylonian, Hebrew, Indian, Greek, Persian, Celtic, Roman, Germanic, and Christian traditions: the hero is born of distinguished parents (often a king); his birth is preceded by a prophecy warning the father; the infant is exposed (in water, in a chest, on a mountain); he is rescued by humble folk (shepherds, fishermen, animals); he grows up to discover his true identity, takes revenge on the father, and achieves greatness. The pattern is too consistent to be coincidence. Rank's psychoanalytic interpretation: the myth is the child's fantasy — the 'family romance' in which the disappointing real parents are replaced by noble, divine ones, and the child imagines himself abandoned and rescued, secretly royal. The myth is the dream of every child who has ever felt: I don't belong here. I must be from somewhere else.",
        "Contemplation": "Rank's fifteen heroes were all exposed and rescued, all discovered their true parentage, all achieved greatness. What if the pattern is not about kings and gods but about you — about the universal experience of being born into a world that does not recognize who you are, and the long journey to claim your own name?"
    },
    "keywords": ["hero-pattern", "family-romance", "exposure", "rescue", "identity"],
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
            {"name": "Otto Rank", "date": "1914", "note": "Original text: The Myth of the Birth of the Hero"},
            {"name": "Smith Ely Jelliffe & F. Robbins (translators)", "date": "1914", "note": "English translation"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, astrology metadata, and meta interpretation"}
        ]
    },
    "name": "The Myth of the Birth of the Hero",
    "description": "Otto Rank's groundbreaking 1914 study comparing fifteen hero birth myths across world cultures — from Sargon of Akkad to Lohengrin. Each hero follows the same pattern: distinguished parentage, prophecy of danger, exposure as an infant, rescue by humble folk, discovery of true identity, and rise to greatness. Rank's psychoanalytic interpretation sees the myth as the child's universal fantasy of secret royal origins — the 'family romance' that Freud identified.\n\nSource: Project Gutenberg eBook #66192 (https://www.gutenberg.org/ebooks/66192).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Classical depictions of hero myths from Greek vase paintings. Gustave Doré's illustrations of Moses. Medieval manuscript illustrations of Siegfried, Tristan, and Lohengrin. Babylonian cylinder seals depicting Sargon and Gilgamesh.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["psychology", "hero-myth", "rank", "birth", "psychoanalysis", "comparative-mythology", "family-romance"],
    "roots": ["western-philosophy", "scientific-inquiry"],
    "shelves": ["mirror", "wisdom"],
    "lineages": ["Shrei", "Akomolafe"],
    "worldview": "dialectical",
    "items": items
}

os.makedirs("grammars/myth-birth-hero-rank", exist_ok=True)
with open("grammars/myth-birth-hero-rank/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

# Validate
ids = [i["id"] for i in items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in items for r in i.get("composite_of", []) if r not in ids]
print(f"Items: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
print(f"Dupes: {dupes}, Bad refs: {bad_refs}")
print(f"Sort OK: {[i['sort_order'] for i in items] == list(range(1, len(items)+1))}")
