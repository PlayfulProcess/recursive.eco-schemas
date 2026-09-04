#!/usr/bin/env python3
"""
Parse Plotinus Enneads (Complete Works) from two volumes.
Gutenberg - Kenneth Sylvan Guthrie translation.
Vol 1: seeds/plotinus-enneads-v1.txt
Vol 2: seeds/plotinus-enneads-v2.txt
"""
import json, re, os

def truncate(text, limit=2800):
    if len(text) > limit:
        bp = text.rfind(".", 0, limit - 200)
        if bp == -1: bp = limit - 200
        remaining = len(text[bp:].split())
        return text[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    return text

def parse_volume(filepath):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    gut_start = text.find("\n", gut_start) + 1
    gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    body = text[gut_start:gut_end].strip()
    lines = body.split("\n")

    # Find all tractate headings
    tractates = []
    pattern = re.compile(r'^(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH) ENNEAD, BOOK (\w+)\.')
    for i, line in enumerate(lines):
        m = pattern.match(line.strip())
        if m:
            ennead_word = m.group(1)
            book_word = m.group(2)

            ennead_map = {"FIRST": 1, "SECOND": 2, "THIRD": 3, "FOURTH": 4, "FIFTH": 5, "SIXTH": 6}
            book_map = {"FIRST": 1, "SECOND": 2, "THIRD": 3, "FOURTH": 4, "FIFTH": 5,
                       "FOURTH": 4, "SIXTH": 6, "SEVEN": 7, "SEVENTH": 7, "EIGHTH": 8,
                       "EIGHT": 8, "NINTH": 9, "NINE": 9, "ONE": 1, "TWO": 2, "THREE": 3,
                       "FOUR": 4, "FIVE": 5, "SIX": 6}
            ennead_num = ennead_map.get(ennead_word, 0)
            book_num = book_map.get(book_word, 0)

            # Get subtitle (usually 2 lines after heading)
            subtitle = ""
            for j in range(i+1, min(i+6, len(lines))):
                if lines[j].strip() and not lines[j].strip().startswith("("):
                    subtitle = lines[j].strip()
                    # Check if subtitle continues on next line
                    if j+1 < len(lines) and lines[j+1].strip() and not lines[j+1].strip().startswith("(") and not lines[j+1].strip().startswith("1."):
                        subtitle += " " + lines[j+1].strip()
                    break

            tractates.append({
                "line": i,
                "ennead": ennead_num,
                "book": book_num,
                "subtitle": subtitle
            })

    # Extract text for each tractate
    for idx, t in enumerate(tractates):
        if idx + 1 < len(tractates):
            end_line = tractates[idx + 1]["line"]
        else:
            end_line = len(lines)

        content = []
        started = False
        for j in range(t["line"] + 1, min(end_line, len(lines))):
            line = lines[j]
            if not started and line.strip() == "":
                continue
            started = True
            content.append(line.rstrip())
        while content and content[-1].strip() == "":
            content.pop()
        t["text"] = "\n".join(content)

    return tractates

# Parse both volumes
v1_tractates = parse_volume("seeds/plotinus-enneads-v1.txt")
v2_tractates = parse_volume("seeds/plotinus-enneads-v2.txt")
all_tractates = v1_tractates + v2_tractates

print(f"Found {len(v1_tractates)} tractates in vol 1, {len(v2_tractates)} in vol 2")

# Sort by ennead then book number for organized output
all_tractates.sort(key=lambda t: (t["ennead"], t["book"]))

# Handle duplicates (same ennead+book from different volumes)
seen = {}
for t in all_tractates:
    key = (t["ennead"], t["book"])
    if key in seen:
        # Append text
        seen[key]["text"] += "\n\n---\n\n" + t["text"]
    else:
        seen[key] = t

unique_tractates = sorted(seen.values(), key=lambda t: (t["ennead"], t["book"]))

# Build items
items = []
sort_order = 1

# Ennead descriptions
ennead_info = {
    1: ("Ethics and the Human Condition", "The soul's relation to the body, beauty, virtue, happiness, and dialectic"),
    2: ("The Physical World", "Matter, potentiality, the heavens, and the elements"),
    3: ("The World-Soul and Nature", "Fate, providence, contemplation, nature, time, and eternity"),
    4: ("The Soul", "The soul's essence, descent, memory, perception, and immortality"),
    5: ("Intelligence (Nous)", "The three hypostases, intelligible beauty, and the origin of intellect"),
    6: ("Being, Number, and the One", "The categories, the Good, and the transcendent One"),
}

ennead_item_ids = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

for t in unique_tractates:
    item_id = f"ennead-{t['ennead']}-{t['book']}"
    subtitle = t["subtitle"]
    name = f"Ennead {t['ennead']}.{t['book']}: {subtitle}" if subtitle else f"Ennead {t['ennead']}.{t['book']}"

    items.append({
        "id": item_id,
        "name": name,
        "sort_order": sort_order,
        "category": f"ennead-{t['ennead']}",
        "level": 1,
        "sections": {
            "Text": truncate(t["text"]),
            "Ennead": f"Ennead {t['ennead']}: {ennead_info.get(t['ennead'], ('',''))[0]}"
        },
        "keywords": ["neoplatonism", "plotinus", f"ennead-{t['ennead']}",
                     subtitle.lower().split()[0] if subtitle else "philosophy"]
    })
    ennead_item_ids[t["ennead"]].append(item_id)
    sort_order += 1

# L2: One item per Ennead
ennead_l2_ids = []
for en in range(1, 7):
    if not ennead_item_ids[en]:
        continue
    en_name, en_desc = ennead_info.get(en, ("", ""))
    l2_id = f"ennead-{en}-complete"
    items.append({
        "id": l2_id,
        "name": f"Ennead {en}: {en_name}",
        "sort_order": sort_order,
        "category": "ennead",
        "level": 2,
        "sections": {
            "About": f"The {['', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth'][en]} Ennead covers {en_desc}.",
            "Tractates": f"{len(ennead_item_ids[en])} tractates"
        },
        "keywords": ["neoplatonism", "plotinus", en_name.lower().replace(" ", "-")],
        "composite_of": ennead_item_ids[en],
        "relationship_type": "emergence"
    })
    ennead_l2_ids.append(l2_id)
    sort_order += 1

# L3: Complete Enneads
items.append({
    "id": "enneads-complete",
    "name": "The Enneads: Complete Works of Plotinus",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "The complete Enneads of Plotinus — the foundational text of Neoplatonism. Plotinus (204-270 CE) developed a philosophical system centered on three hypostases: the One (the transcendent source), Nous (divine intellect), and Soul (the world-soul). His thought profoundly influenced Augustine, medieval mysticism, and the entire Platonic tradition.",
        "The Three Hypostases": "The One: the ineffable, transcendent source beyond being. Nous (Intelligence): the realm of Forms, the first emanation. Soul: the mediator between intellect and matter, source of the physical world."
    },
    "keywords": ["neoplatonism", "plotinus", "complete", "metaphysics", "the-one", "nous", "soul"],
    "composite_of": ennead_l2_ids,
    "relationship_type": "emergence"
})

# Re-number
for i, item in enumerate(items):
    item["sort_order"] = i + 1

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Plotinus", "date": "204-270 CE", "note": "Author"},
            {"name": "Kenneth Sylvan Guthrie", "date": "1918", "note": "Translator"},
            {"name": "Project Gutenberg", "date": "2021", "note": "Source"}
        ]
    },
    "name": "Plotinus: The Enneads",
    "description": "The complete Enneads of Plotinus, the foundational text of Neoplatonism, translated by Kenneth Sylvan Guthrie. Fifty-four tractates organized in six groups of nine ('enneads'), covering metaphysics, ethics, cosmology, and the nature of reality. Plotinus's vision of the One, Nous, and Soul shaped Western mysticism, theology, and philosophy for nearly two millennia.\n\nSource: Project Gutenberg\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Raphael's 'School of Athens' (1509-1511) includes idealized portraits of ancient philosophers. Ancient Roman busts and mosaics depicting philosophers.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["neoplatonism", "plotinus", "metaphysics", "mysticism", "the-one", "nous", "soul", "emanation", "beauty", "ancient-philosophy"],
    "roots": ["western-philosophy", "mysticism", "classical-antiquity"],
    "shelves": ["wisdom"],
    "lineages": ["Shrei", "Linehan"],
    "worldview": "non-dual",
    "items": items
}

os.makedirs("grammars/plotinus-enneads", exist_ok=True)
with open("grammars/plotinus-enneads/grammar.json", "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

print(f"\nGenerated {len(items)} items")
print(f"L1: {sum(1 for i in items if i['level']==1)}")
print(f"L2: {sum(1 for i in items if i['level']==2)}")
print(f"L3: {sum(1 for i in items if i['level']==3)}")
