#!/usr/bin/env python3
"""
Parse Indian Myth and Legend (Donald A. Mackenzie, Gutenberg #47228).
26 chapters → L1 items, grouped into L2 thematic clusters + L3 meta.
"""
import json, re, os

with open("seeds/indian-myth-legend.txt", encoding="utf-8") as f:
    text = f.read()

gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()

CHAPTERS = [
    ("CHAPTER I", "ch01-indra", "Indra, King of the Gods", "vedic-gods", ["indra", "thunder", "soma", "vedic"]),
    ("CHAPTER II", "ch02-vedic-deities", "The Great Vedic Deities", "vedic-gods", ["agni", "varuna", "surya", "vayu", "vedic"]),
    ("CHAPTER III", "ch03-yama", "Yama, the First Man, and King of the Dead", "vedic-gods", ["yama", "death", "underworld", "first-man"]),
    ("CHAPTER IV", "ch04-demons-giants", "Demons and Giants and Fairies", "spirits", ["asuras", "rakshasas", "gandharvas", "apsaras"]),
    ("CHAPTER V", "ch05-vedic-age", "Social and Religious Developments of the Vedic Age", "framework", ["vedic", "caste", "sacrifice", "brahman"]),
    ("CHAPTER VI", "ch06-creation-ages", "Mysteries of Creation, the World's Ages, and Soul Wandering", "cosmology", ["creation", "yugas", "samsara", "brahma"]),
    ("CHAPTER VII", "ch07-vishnu-buddhism", "New Faiths: Vishnu Religion, Buddhism, and Jainism", "philosophy", ["vishnu", "buddha", "jain", "avatar"]),
    ("CHAPTER VIII", "ch08-epic-deities", "Divinities of the Epic Period", "deities", ["shiva", "vishnu", "devi", "ganesh", "hanuman"]),
    ("CHAPTER IX", "ch09-bharata-prelude", "Prelude to the Great Bharata War", "mahabharata", ["vyasa", "bharata", "kurukshetra"]),
    ("CHAPTER X", "ch10-pandavas-kauravas", "Royal Rivals: the Pandavas and Kauravas", "mahabharata", ["arjuna", "yudhishthira", "duryodhana"]),
    ("CHAPTER XI", "ch11-tournament", "The Tournament", "mahabharata", ["karna", "arjuna", "drona"]),
    ("CHAPTER XII", "ch12-first-exile", "First Exile of the Pandavas", "mahabharata", ["exile", "forest", "pandavas"]),
    ("CHAPTER XIII", "ch13-draupadi", "The Choice of Draupadi", "mahabharata", ["draupadi", "swayamvara", "bow-contest"]),
    ("CHAPTER XIV", "ch14-pandava-triumph", "Triumph of the Pandavas", "mahabharata", ["indraprastha", "kingdom", "triumph"]),
    ("CHAPTER XV", "ch15-gambling", "The Great Gambling Match", "mahabharata", ["dice", "gambling", "shakuni", "humiliation"]),
    ("CHAPTER XVI", "ch16-second-exile", "Second Exile of the Pandavas", "mahabharata", ["exile", "forest", "dharma"]),
    ("CHAPTER XVII", "ch17-defiance", "Defiance of Duryodhana", "mahabharata", ["duryodhana", "krishna", "diplomacy", "war"]),
    ("CHAPTER XVIII", "ch18-battle", "The Battle of Eighteen Days", "mahabharata", ["kurukshetra", "bhagavad-gita", "krishna", "arjuna"]),
    ("CHAPTER XIX", "ch19-atonement", "Atonement and the Ascent to Heaven", "mahabharata", ["atonement", "heaven", "dharma", "death"]),
    ("CHAPTER XX", "ch20-nala-damayanti", "Nala and Damayantí", "romance", ["nala", "damayanti", "love", "gambling", "swans"]),
    ("CHAPTER XXI", "ch21-wanderings-forest", "Wanderings in the Forest", "romance", ["exile", "forest", "adventure"]),
    ("CHAPTER XXII", "ch22-nala-exile", "Nala in Exile", "romance", ["nala", "disguise", "serpent", "transformation"]),
    ("CHAPTER XXIII", "ch23-homecoming", "The Homecoming of the King", "romance", ["reunion", "identity", "restoration"]),
    ("CHAPTER XXIV", "ch24-rama-sita-won", "Story of Rama: How Sita was Won", "ramayana", ["rama", "sita", "bow-of-shiva", "swayamvara"]),
    ("CHAPTER XXV", "ch25-abduction-sita", "The Abduction of Sita", "ramayana", ["ravana", "lanka", "abduction", "hanuman"]),
    ("CHAPTER XXVI", "ch26-rama-fulfilled", "Rama's Mission Fulfilled", "ramayana", ["rama", "ravana", "battle", "dharma", "ayodhya"]),
]

body_lines = body.split("\n")
positions = []
for heading, sid, name, cat, kw in CHAPTERS:
    pos = -1
    for i, line in enumerate(body_lines):
        if line.strip() == heading:
            pos = sum(len(l) + 1 for l in body_lines[:i])
            break
    if pos < 0:
        for i, line in enumerate(body_lines):
            if line.strip().startswith(heading) and i > 100:
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
    skip_count = 0
    for line in lines:
        if not started:
            stripped = line.strip()
            if stripped == "" or stripped == heading:
                continue
            # Skip chapter title and synopsis
            if skip_count < 3 and (stripped.isupper() or stripped.startswith("[Illustration") or (line.startswith(" ") and "—" in line)):
                skip_count += 1
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
        "keywords": ["india", "hindu", "mackenzie", "mythology"] + kw,
        "metadata": {}
    })
    sort_order += 1

# Astrology metadata
astrology_map = {
    "ch01-indra": {"planets": ["Jupiter", "Mars"], "signs": ["Sagittarius", "Aries"], "themes": ["thunder-god", "soma", "cosmic-battle"]},
    "ch03-yama": {"planets": ["Saturn", "Pluto"], "signs": ["Capricorn", "Scorpio"], "themes": ["death", "judgment", "underworld"]},
    "ch06-creation-ages": {"planets": ["Saturn", "Neptune"], "signs": ["Capricorn", "Pisces"], "themes": ["yugas", "creation", "cosmic-cycles"]},
    "ch08-epic-deities": {"planets": ["Sun", "Moon", "Mars"], "signs": ["Leo", "Cancer", "Aries"], "themes": ["shiva", "vishnu", "devi"]},
    "ch18-battle": {"planets": ["Mars", "Sun"], "signs": ["Aries", "Leo"], "themes": ["dharma", "duty", "cosmic-war"]},
    "ch20-nala-damayanti": {"planets": ["Venus", "Neptune"], "signs": ["Libra", "Pisces"], "themes": ["love", "fate", "devotion"]},
    "ch24-rama-sita-won": {"planets": ["Sun", "Venus"], "signs": ["Leo", "Libra"], "themes": ["dharma", "devotion", "divine-love"]},
}
for item in items:
    if item["id"] in astrology_map:
        item["metadata"]["astrology"] = astrology_map[item["id"]]

# L2 groups
groups = [
    {
        "id": "group-vedic-gods",
        "name": "The Vedic Gods: Powers of Heaven and Earth",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch01-indra", "ch02-vedic-deities", "ch03-yama", "ch04-demons-giants", "ch05-vedic-age", "ch06-creation-ages"],
        "sections": {
            "About": "The earliest stratum of Indian mythology: the Vedic gods — Indra the thunder-wielder, Agni the fire, Varuna the cosmic law, Yama the first man to die and become king of the dead. Plus the creation myths, the world ages (yugas), and the doctrine of soul-wandering (samsara) that would become central to all Indian thought.",
            "For Readers": "Start with Chapter I (Indra) for the most vivid Vedic mythology, then Chapter VI (Creation) for the profound cosmological vision that underlies Hinduism and Buddhism."
        },
        "keywords": ["vedic", "indra", "creation", "cosmology"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "group-mahabharata",
        "name": "The Mahābhārata: The Great Bharata War",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch09-bharata-prelude", "ch10-pandavas-kauravas", "ch11-tournament", "ch12-first-exile",
                         "ch13-draupadi", "ch14-pandava-triumph", "ch15-gambling", "ch16-second-exile",
                         "ch17-defiance", "ch18-battle", "ch19-atonement"],
        "sections": {
            "About": "The complete arc of the Mahābhārata as retold by Mackenzie: from the rivalry of the Pandava and Kaurava cousins through the great gambling match, the years of exile, the diplomacy of Krishna, the eighteen-day battle of Kurukshetra (which includes the Bhagavad Gita), and the final ascent to heaven.",
            "For Readers": "The Gambling Match (Ch XV) is the dramatic turning point. The Battle of Eighteen Days (Ch XVIII) contains Mackenzie's retelling of the Bhagavad Gita — Krishna's teaching to Arjuna on the battlefield."
        },
        "keywords": ["mahabharata", "pandavas", "krishna", "dharma"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "group-ramayana",
        "name": "The Rāmāyaṇa: The Story of Rama",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch24-rama-sita-won", "ch25-abduction-sita", "ch26-rama-fulfilled"],
        "sections": {
            "About": "India's second great epic: the story of Rama, prince of Ayodhya, who wins the princess Sita by bending the bow of Shiva, loses her to the demon king Ravana, and wages war across the sea to rescue her — aided by the monkey god Hanuman and the bear king Jambavan.",
            "For Readers": "Read all three chapters in sequence for the complete story. This is the most beloved narrative in Indian culture, performed in festivals throughout South and Southeast Asia."
        },
        "keywords": ["ramayana", "rama", "sita", "hanuman", "dharma"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "group-nala",
        "name": "Nala and Damayantí: A Love Story Within the Epic",
        "category": "thematic-group",
        "level": 2,
        "composite_of": ["ch20-nala-damayanti", "ch21-wanderings-forest", "ch22-nala-exile", "ch23-homecoming"],
        "sections": {
            "About": "The story of Nala and Damayantí — one of the most beautiful love stories in world literature, embedded within the Mahābhārata. King Nala, cursed by a demon through a gambling match, loses his kingdom and wanders in exile, separated from his devoted wife, until fate brings them back together.",
            "For Readers": "This tale mirrors the main Mahābhārata story (gambling, exile, reunion) but on a human, domestic scale. It's a complete romance that can be read independently."
        },
        "keywords": ["nala", "damayanti", "love", "fate"],
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
    "id": "meta-indian-myth",
    "name": "Indian Myth: The Longest Story Ever Told",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "Donald A. Mackenzie's 'Indian Myth and Legend' (1913) retells the vast mythology of India — from the thunder-god Indra and the Vedic fire-sacrifice to the cosmic war of the Mahābhārata and the quest of Rama. Mackenzie covers the full arc: Vedic gods and demons, the creation of the world through cosmic ages (yugas), the rise of Vishnu, Shiva, and the Goddess, the complete Mahābhārata including the Bhagavad Gita, and the Rāmāyaṇa. This is mythology on an epic scale — the Mahābhārata alone is seven times longer than the Iliad and Odyssey combined.",
        "Contemplation": "India's mythology is unique in world literature: it contains everything. Comedy and tragedy, philosophy and war, human love and cosmic dissolution. The Bhagavad Gita is embedded in the middle of a battlefield. The most tender love story (Nala and Damayantí) is told to console an exiled king. What does it mean that the deepest wisdom always arrives in the middle of the worst crisis?"
    },
    "keywords": ["india", "hindu", "mythology", "mahabharata", "ramayana", "vedic"],
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
            {"name": "Donald A. Mackenzie", "date": "1913", "note": "Original text: Indian Myth and Legend"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, thematic groupings, astrology metadata, and meta interpretation"}
        ]
    },
    "name": "Indian Myth and Legend",
    "description": "Donald A. Mackenzie's comprehensive retelling of Indian mythology (1913) — from the Vedic gods (Indra, Agni, Varuna, Yama) through the great epics: the complete Mahābhārata (including the Bhagavad Gita) and the Rāmāyaṇa. 26 chapters covering creation myths, cosmic cycles, the philosophy of dharma, and the most beloved stories of Hindu civilization.\n\nSource: Project Gutenberg eBook #47228 (https://www.gutenberg.org/ebooks/47228).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Warwick Goble's watercolour illustrations from the original 1913 edition (ethereal, Pre-Raphaelite style). Raja Ravi Varma's paintings of Hindu deities and epic scenes (1890s). Mughal miniature paintings of Rama, Krishna, and the Pandavas.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["mythology", "india", "hindu", "mahabharata", "ramayana", "vedic", "krishna", "rama"],
    "roots": ["eastern-wisdom", "devotional-practice"],
    "shelves": ["wisdom"],
    "lineages": ["Shrei", "Akomolafe"],
    "worldview": "devotional",
    "items": items
}

os.makedirs("grammars/indian-myth-legend", exist_ok=True)
with open("grammars/indian-myth-legend/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

ids = [i["id"] for i in items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in items for r in i.get("composite_of", []) if r not in ids]
print(f"Items: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
print(f"Sections: {sum(len(i.get('sections',{})) for i in items)}")
print(f"Dupes: {dupes}, Bad refs: {bad_refs}")
print(f"Sort OK: {[i['sort_order'] for i in items] == list(range(1, len(items)+1))}")
