#!/usr/bin/env python3
"""
Parse Hesiod, the Homeric Hymns, and Homerica (Gutenberg #348).
Major works: Works and Days, Theogony, Shield of Heracles + 33 Homeric Hymns.
"""
import json, re, os

with open("seeds/hesiod-homeric-hymns.txt", encoding="utf-8") as f:
    text = f.read()

gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()
body_lines = body.split("\n")

def find_section(heading):
    """Find a section by its heading line (stripped match)."""
    for i, line in enumerate(body_lines):
        if line.strip() == heading:
            return i
    return -1

def extract_between(start_ln, end_ln):
    """Extract text between line numbers, skip heading."""
    content = []
    started = False
    for j in range(start_ln + 1, min(end_ln, len(body_lines))):
        line = body_lines[j]
        if not started and line.strip() == "":
            continue
        started = True
        content.append(line.rstrip())
    while content and content[-1].strip() == "":
        content.pop()
    return "\n".join(content)

def truncate(text, limit=3000):
    if len(text) > limit:
        bp = text.rfind(".", 0, limit - 200)
        if bp == -1: bp = limit - 200
        remaining = len(text[bp:].split())
        return text[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    return text

# ═══════════════════════════════════════════════════════════════════════════
# FIND ALL SECTIONS
# ═══════════════════════════════════════════════════════════════════════════

# Major Hesiod works
hesiod_works = [
    ("HESIOD\u2019S WORKS AND DAYS", "works-and-days", "Works and Days"),
    ("THE THEOGONY", "theogony", "The Theogony (Birth of the Gods)"),
    ("THE CATALOGUES OF WOMEN AND EOIAE1701", "catalogues-women", "The Catalogues of Women"),
    ("THE SHIELD OF HERACLES", "shield-heracles", "The Shield of Heracles"),
]

# Minor Hesiod
hesiod_minor = [
    ("THE DIVINATION BY BIRDS", "divination-birds", "The Divination by Birds"),
    ("THE ASTRONOMY", "astronomy", "The Astronomy"),
    ("THE PRECEPTS OF CHIRON", "precepts-chiron", "The Precepts of Chiron"),
    ("THE GREAT WORKS", "great-works", "The Great Works"),
    ("THE IDAEAN DACTYLS", "idaean-dactyls", "The Idaean Dactyls"),
    ("THE MARRIAGE OF CEYX", "marriage-ceyx", "The Marriage of Ceyx"),
    ("THE GREAT EOIAE", "great-eoiae", "The Great Eoiae"),
    ("THE MELAMPODIA", "melampodia", "The Melampodia"),
]

# Homeric Hymns (major ones first, then shorter ones)
hymns = [
    ("I. TO DIONYSUS 2501", "hymn-dionysus-1", "Hymn I: To Dionysus"),
    ("II. TO DEMETER", "hymn-demeter", "Hymn II: To Demeter"),
    ("III. TO DELIAN APOLLO", "hymn-apollo", "Hymn III: To Apollo"),
    ("IV. TO HERMES", "hymn-hermes", "Hymn IV: To Hermes"),
    ("V. TO APHRODITE", "hymn-aphrodite-long", "Hymn V: To Aphrodite"),
    ("VI. TO APHRODITE", "hymn-aphrodite-short", "Hymn VI: To Aphrodite (Short)"),
    ("VII. TO DIONYSUS", "hymn-dionysus-2", "Hymn VII: To Dionysus"),
    ("VIII. TO ARES", "hymn-ares", "Hymn VIII: To Ares"),
    ("IX. TO ARTEMIS", "hymn-artemis-1", "Hymn IX: To Artemis"),
    ("X. TO APHRODITE", "hymn-aphrodite-3", "Hymn X: To Aphrodite"),
    ("XI. TO ATHENA", "hymn-athena-1", "Hymn XI: To Athena"),
    ("XII. TO HERA", "hymn-hera", "Hymn XII: To Hera"),
    ("XIII. TO DEMETER", "hymn-demeter-short", "Hymn XIII: To Demeter (Short)"),
    ("XIV. TO THE MOTHER OF THE GODS", "hymn-mother-gods", "Hymn XIV: To the Mother of the Gods"),
    ("XV. TO HERACLES THE LION-HEARTED", "hymn-heracles", "Hymn XV: To Heracles"),
    ("XVI. TO ASCLEPIUS", "hymn-asclepius", "Hymn XVI: To Asclepius"),
    ("XVII. TO THE DIOSCURI", "hymn-dioscuri-1", "Hymn XVII: To the Dioscuri"),
    ("XVIII. TO HERMES", "hymn-hermes-short", "Hymn XVIII: To Hermes (Short)"),
    ("XIX. TO PAN", "hymn-pan", "Hymn XIX: To Pan"),
    ("XX. TO HEPHAESTUS", "hymn-hephaestus", "Hymn XX: To Hephaestus"),
    ("XXI. TO APOLLO", "hymn-apollo-short", "Hymn XXI: To Apollo (Short)"),
    ("XXII. TO POSEIDON", "hymn-poseidon", "Hymn XXII: To Poseidon"),
    ("XXIII. TO THE SON OF CRONOS, MOST HIGH", "hymn-zeus", "Hymn XXIII: To Zeus"),
    ("XXIV. TO HESTIA", "hymn-hestia-1", "Hymn XXIV: To Hestia"),
    ("XXV. TO THE MUSES AND APOLLO", "hymn-muses-apollo", "Hymn XXV: To the Muses and Apollo"),
    ("XXVI. TO DIONYSUS", "hymn-dionysus-3", "Hymn XXVI: To Dionysus"),
    ("XXVII. TO ARTEMIS", "hymn-artemis-2", "Hymn XXVII: To Artemis"),
    ("XXVIII. TO ATHENA", "hymn-athena-2", "Hymn XXVIII: To Athena"),
    ("XXIX. TO HESTIA", "hymn-hestia-2", "Hymn XXIX: To Hestia"),
    ("XXX. TO EARTH THE MOTHER OF ALL", "hymn-earth", "Hymn XXX: To Earth, Mother of All"),
    ("XXXI. TO HELIOS", "hymn-helios", "Hymn XXXI: To Helios"),
    ("XXXII. TO SELENE", "hymn-selene", "Hymn XXXII: To Selene"),
    ("XXXIII. TO THE DIOSCURI", "hymn-dioscuri-2", "Hymn XXXIII: To the Dioscuri"),
]

ALL_SECTIONS = hesiod_works + hesiod_minor + hymns

# Find all section positions
section_positions = []
for heading, sid, name in ALL_SECTIONS:
    ln = find_section(heading)
    if ln < 0:
        # Try without trailing numbers
        clean_heading = re.sub(r'\d+$', '', heading).strip()
        ln = find_section(clean_heading)
    if ln >= 0:
        section_positions.append((ln, heading, sid, name))
    else:
        print(f"WARNING: Could not find '{heading}'")

section_positions.sort(key=lambda x: x[0])
print(f"Found {len(section_positions)} sections")

# Extract items
items = []
sort_order = 1

for idx, (start_ln, heading, sid, name) in enumerate(section_positions):
    end_ln = section_positions[idx+1][0] if idx+1 < len(section_positions) else len(body_lines)
    text_content = extract_between(start_ln, end_ln)
    excerpt = truncate(text_content)

    # Determine category
    if sid.startswith("hymn-"):
        cat = "hymns"
    elif sid in [s[1] for s in hesiod_minor]:
        cat = "fragments"
    else:
        cat = "works"

    # Astrology for key items
    astro = {}
    astro_map = {
        "theogony": {"planets": ["Saturn", "Jupiter", "Pluto"], "signs": ["Capricorn", "Sagittarius"], "themes": ["cosmic-origins", "divine-generations", "titan-war"]},
        "works-and-days": {"planets": ["Saturn", "Mercury"], "signs": ["Virgo", "Capricorn"], "themes": ["labor", "justice", "seasons", "ages-of-man"]},
        "shield-heracles": {"planets": ["Mars", "Sun"], "signs": ["Aries", "Leo"], "themes": ["combat", "divine-weaponry"]},
        "hymn-demeter": {"planets": ["Moon", "Pluto"], "signs": ["Cancer", "Scorpio"], "themes": ["mother-grief", "descent", "seasons"]},
        "hymn-apollo": {"planets": ["Sun"], "signs": ["Leo"], "themes": ["prophecy", "music", "light"]},
        "hymn-hermes": {"planets": ["Mercury"], "signs": ["Gemini"], "themes": ["trickster", "theft", "invention"]},
        "hymn-aphrodite-long": {"planets": ["Venus"], "signs": ["Taurus", "Libra"], "themes": ["love", "desire", "mortal-divine"]},
        "hymn-dionysus-1": {"planets": ["Neptune", "Pluto"], "signs": ["Pisces", "Scorpio"], "themes": ["ecstasy", "transformation"]},
        "hymn-ares": {"planets": ["Mars"], "signs": ["Aries", "Scorpio"], "themes": ["war", "courage", "violence"]},
        "hymn-artemis-1": {"planets": ["Moon"], "signs": ["Sagittarius"], "themes": ["hunt", "wildness", "chastity"]},
        "hymn-pan": {"planets": ["Saturn", "Mercury"], "signs": ["Capricorn"], "themes": ["wild-god", "panic", "nature"]},
        "hymn-earth": {"planets": ["Earth", "Moon"], "signs": ["Taurus", "Virgo"], "themes": ["great-mother", "fertility", "foundation"]},
        "hymn-helios": {"planets": ["Sun"], "signs": ["Leo"], "themes": ["solar-chariot", "all-seeing"]},
        "hymn-selene": {"planets": ["Moon"], "signs": ["Cancer"], "themes": ["lunar-light", "night"]},
        "hymn-hephaestus": {"planets": ["Mars", "Venus"], "signs": ["Virgo"], "themes": ["craft", "forge", "fire"]},
        "hymn-poseidon": {"planets": ["Neptune"], "signs": ["Pisces"], "themes": ["sea", "earthquake", "horses"]},
    }

    metadata = {"origin": "Greek"}
    if sid in astro_map:
        metadata["astrology"] = astro_map[sid]

    items.append({
        "id": sid,
        "name": name,
        "sort_order": sort_order,
        "category": cat,
        "level": 1,
        "sections": {"Text": excerpt},
        "keywords": ["hesiod", "homeric-hymn", "greek"] + ([sid.replace("hymn-", "")] if sid.startswith("hymn-") else []),
        "metadata": metadata
    })
    sort_order += 1

# L2: Groupings
groups = [
    {
        "id": "group-hesiod-major",
        "name": "Hesiod's Major Works",
        "about": "The two pillars of Hesiodic poetry: the Theogony, which tells the birth of the gods from Chaos through the Titan War to the establishment of Zeus's order; and Works and Days, which teaches the farmer's life, the five ages of man, and the rule of justice. Together they form the oldest systematic Greek cosmology and ethics — how the world was made and how to live in it.",
        "refs": ["works-and-days", "theogony", "shield-heracles"]
    },
    {
        "id": "group-major-hymns",
        "name": "The Great Hymns",
        "about": "The five long Homeric Hymns — substantial narrative poems that tell the stories of the gods: Demeter's grief and the origin of the Eleusinian Mysteries, Hermes' infant trickery, Apollo's birth and oracle, Aphrodite's seduction of Anchises, and Dionysus among the pirates. These are not prayers but epic narratives, each a complete myth in verse. The Hymn to Demeter is the primary source for the Persephone myth.",
        "refs": ["hymn-dionysus-1", "hymn-demeter", "hymn-apollo", "hymn-hermes", "hymn-aphrodite-long"]
    },
    {
        "id": "group-short-hymns",
        "name": "The Short Hymns: A Pantheon in Miniature",
        "about": "Twenty-eight shorter hymns, each a concentrated invocation of a single deity — from Ares the war-god to Hestia of the hearth, from Earth the Mother of All to Selene the moon. Read together, they form a complete map of the Greek divine world: every power, every domain, every face of the sacred, addressed directly and praised.",
        "refs": [s[1] for s in hymns[5:]]  # hymns VI through XXXIII
    },
]

for grp in groups:
    valid_refs = [r for r in grp["refs"] if r in [i["id"] for i in items]]
    items.append({
        "id": grp["id"],
        "name": grp["name"],
        "sort_order": sort_order,
        "category": "groups",
        "level": 2,
        "sections": {
            "About": grp["about"],
            "For Readers": "Read these texts aloud if you can — they were composed for oral performance. Listen for the epithets (rosy-fingered, wine-dark, cloud-gathering) that are the signature of the oral tradition. Each epithet is a small theology: it tells you what the Greeks noticed about their gods."
        },
        "keywords": ["hesiod", "homeric-hymn", "greek"],
        "composite_of": valid_refs,
        "relationship_type": "emergence",
        "metadata": {}
    })
    sort_order += 1

# L3 meta
items.append({
    "id": "meta-greek-sacred-poetry",
    "name": "Greek Sacred Poetry: Where the Gods Speak",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "Hesiod and the Homeric Hymns represent the oldest surviving Greek sacred poetry — the texts that told the Greeks who their gods were, how the world was made, and how to live justly in it. The Theogony is a creation myth as ambitious as Genesis. Works and Days is a handbook for the moral life. The Homeric Hymns are the Greek scripture — direct addresses to the divine powers, telling their stories and praising their attributes. Together, these texts are the foundation on which all later Greek mythology, philosophy, and tragedy was built. When Sophocles wrote Oedipus, when Plato wrote the Republic, when Jung read Greek myth — these are the texts they knew.",
        "Contemplation": "These poets addressed the gods directly — 'Sing, Muse,' 'I begin to sing of Demeter' — as if the gods were listening. What if they were? And what if the act of addressing something sacred, whether or not it answers, is itself the point?"
    },
    "keywords": ["hesiod", "homer", "sacred-poetry", "greek", "foundation"],
    "composite_of": [g["id"] for g in groups],
    "relationship_type": "emergence",
    "metadata": {}
})

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Hesiod", "date": "c. 700 BCE", "note": "Works and Days, Theogony, and other poems"},
            {"name": "Homer (attributed)", "date": "c. 700-500 BCE", "note": "The Homeric Hymns"},
            {"name": "Hugh G. Evelyn-White (translator)", "date": "1914", "note": "English translation (Loeb Classical Library)"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, astrology metadata, groupings"}
        ]
    },
    "name": "Hesiod, the Homeric Hymns, and Homerica",
    "description": "The oldest surviving Greek sacred poetry: Hesiod's Theogony (birth of the gods from Chaos), Works and Days (the farmer's ethics and the five ages of man), the Shield of Heracles, and thirty-three Homeric Hymns — invocations of the Olympian gods from Demeter to Dionysus. These are the foundation texts of Greek mythology: the primary sources for Prometheus, Persephone, Pandora, and the entire Olympian pantheon.\n\nSource: Project Gutenberg eBook #348 (https://www.gutenberg.org/ebooks/348). Hugh G. Evelyn-White translation (1914).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: John Flaxman's line illustrations for Hesiod (1817). Greek vase paintings of the Olympian gods. Walter Crane's illustrations of Greek myths.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["greek", "hesiod", "homer", "hymns", "theogony", "olympian", "sacred-poetry", "mythology"],
    "roots": ["western-philosophy", "mysticism"],
    "shelves": ["wisdom"],
    "lineages": ["Shrei"],
    "worldview": "devotional",
    "items": items
}

os.makedirs("grammars/hesiod-homeric-hymns", exist_ok=True)
with open("grammars/hesiod-homeric-hymns/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

ids = [i["id"] for i in items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in items for r in i.get("composite_of", []) if r not in ids]
print(f"Items: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
print(f"Dupes: {dupes}, Bad refs: {bad_refs}")
print(f"Sort OK: {[i['sort_order'] for i in items] == list(range(1, len(items)+1))}")
