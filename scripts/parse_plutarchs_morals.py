#!/usr/bin/env python3
"""
Parse Plutarch's Morals (Moralia) — Gutenberg #23639.
A collection of moral essays on virtue, anger, contentment, education, etc.
"""
import json, re, os

with open("seeds/plutarchs-morals.txt", encoding="utf-8") as f:
    text = f.read()

gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()
lines = body.split("\n")

def truncate(t, limit=2800):
    if len(t) > limit:
        bp = t.rfind(".", 0, limit - 200)
        if bp == -1: bp = limit - 200
        remaining = len(t[bp:].split())
        return t[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    return t

# Essay definitions - (heading_text, id, name, category, keywords)
ESSAY_DEFS = [
    ("ON EDUCATION.", "on-education", "On Education", "ethics", ["education", "children", "virtue"]),
    ("ON LOVE TO ONE'S OFFSPRING.", "on-love-offspring", "On Love to One's Offspring", "family", ["love", "children", "parenting"]),
    ("ON LOVE.", "on-love", "On Love", "ethics", ["love", "eros", "friendship"]),
    ("CONJUGAL PRECEPTS.", "conjugal-precepts", "Conjugal Precepts", "family", ["marriage", "partnership", "advice"]),
    ("CONSOLATORY LETTER TO HIS WIFE.", "consolatory-letter", "Consolatory Letter to His Wife", "family", ["grief", "consolation", "death"]),
    ("THAT VIRTUE MAY BE TAUGHT.", "virtue-may-be-taught", "That Virtue May Be Taught", "virtue", ["virtue", "education", "character"]),
    ("ON VIRTUE AND VICE.", "virtue-and-vice", "On Virtue and Vice", "virtue", ["virtue", "vice", "ethics"]),
    ("ON MORAL VIRTUE.", "on-moral-virtue", "On Moral Virtue", "virtue", ["virtue", "reason", "passion"]),
]

# Find essays by heading pattern
essay_starts = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if not stripped:
        continue
    # Look for ALL CAPS lines that are essay headings
    if (stripped.startswith("ON ") or stripped.startswith("THAT ") or
        stripped.startswith("HOW ") or stripped.startswith("WHETHER ") or
        stripped.startswith("AGAINST ") or stripped.startswith("CONCERNING ") or
        stripped == "CONJUGAL PRECEPTS." or stripped == "CONSOLATORY LETTER TO HIS WIFE." or
        stripped == "PROGRESS IN VIRTUE." or stripped == "ON EXILE." or
        stripped == "ON FORTUNE."):
        if stripped.isupper() and len(stripped) > 5:
            essay_starts.append((i, stripped))

# Remove duplicate/continuation headings (multi-line titles)
cleaned = []
prev_line = -10
for line_num, heading in essay_starts:
    if line_num - prev_line <= 2:
        # Merge with previous
        if cleaned:
            prev_ln, prev_h = cleaned[-1]
            cleaned[-1] = (prev_ln, prev_h + " " + heading)
    else:
        cleaned.append((line_num, heading))
    prev_line = line_num

essay_starts = cleaned

# Extract text for each essay
items = []
sort_order = 1

for idx, (start_line, heading) in enumerate(essay_starts):
    if idx + 1 < len(essay_starts):
        end_line = essay_starts[idx + 1][0]
    else:
        end_line = len(lines)

    content = []
    started = False
    for j in range(start_line + 1, min(end_line, len(lines))):
        line = lines[j]
        if not started and line.strip() == "":
            continue
        started = True
        content.append(line.rstrip())
    while content and content[-1].strip() == "":
        content.pop()
    essay_text = "\n".join(content)

    # Create clean name
    name = heading.rstrip(".")
    name = re.sub(r'\[\d+\]', '', name).strip()
    # Title case
    name = name.title()
    # Fix common words
    for word in ["A", "An", "The", "Of", "On", "To", "By", "In", "And", "Or", "Is", "Be", "May", "Not", "One'S", "From"]:
        name = name.replace(f" {word} ", f" {word.lower()} ")
    if name.startswith("On "):
        name = "On " + name[3:]
    if name.startswith("That "):
        name = "That " + name[5:]
    if name.startswith("How "):
        name = "How " + name[4:]

    # Create ID
    item_id = re.sub(r'[^a-z0-9\s]', '', heading.lower().rstrip("."))
    item_id = re.sub(r'\[\d+\]', '', item_id).strip()
    item_id = re.sub(r'\s+', '-', item_id)[:60]

    # Determine category
    cat = "ethics"
    heading_lower = heading.lower()
    if any(w in heading_lower for w in ["love", "marriage", "conjugal", "wife", "offspring"]):
        cat = "family"
    elif any(w in heading_lower for w in ["virtue", "vice", "moral"]):
        cat = "virtue"
    elif any(w in heading_lower for w in ["anger", "envy", "hatred", "shyness", "curiosity", "talkativeness"]):
        cat = "passions"
    elif any(w in heading_lower for w in ["fortune", "exile", "punishment", "borrowing"]):
        cat = "fate"
    elif any(w in heading_lower for w in ["flatterer", "friend", "enemies", "praise"]):
        cat = "social"

    items.append({
        "id": item_id,
        "name": name,
        "sort_order": sort_order,
        "category": cat,
        "level": 1,
        "sections": {
            "Essay": truncate(essay_text),
            "Theme": f"Category: {cat.title()}"
        },
        "keywords": ["plutarch", "moralia", cat]
    })
    sort_order += 1

# Handle duplicate IDs
seen_ids = {}
for item in items:
    if item["id"] in seen_ids:
        seen_ids[item["id"]] += 1
        item["id"] = f"{item['id']}-{seen_ids[item['id']]}"
    else:
        seen_ids[item["id"]] = 1

# L2: Group by category
categories = {}
for item in items:
    cat = item["category"]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(item["id"])

cat_names = {
    "ethics": "Ethics and Character",
    "virtue": "On Virtue",
    "family": "Marriage, Love, and Family",
    "passions": "Mastering the Passions",
    "social": "Friends, Flatterers, and Enemies",
    "fate": "Fortune, Exile, and Providence"
}

l2_ids = []
for cat, cat_ids in categories.items():
    l2_id = f"group-{cat}"
    items.append({
        "id": l2_id,
        "name": cat_names.get(cat, cat.title()),
        "sort_order": sort_order,
        "category": "thematic-group",
        "level": 2,
        "sections": {
            "About": f"Essays in Plutarch's Moralia on the theme of {cat_names.get(cat, cat).lower()}.",
            "Essays": f"{len(cat_ids)} essays"
        },
        "keywords": ["plutarch", "moralia", cat],
        "composite_of": cat_ids,
        "relationship_type": "emergence"
    })
    l2_ids.append(l2_id)
    sort_order += 1

# L3 meta
items.append({
    "id": "moralia-complete",
    "name": "Plutarch's Moralia: Complete",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "The Moralia (Moral Essays) of Plutarch — a vast collection of essays, dialogues, and reflections on ethics, education, marriage, anger, fortune, and the good life. Written in the 1st-2nd century CE, these essays complement Plutarch's more famous Parallel Lives and reveal a mind concerned with practical wisdom and the cultivation of character.",
        "For Readers": "Each essay stands alone as a meditation on a specific aspect of human life. Start with 'On Contentedness of Mind' for Stoic-influenced serenity, 'On Restraining Anger' for practical psychology, or 'Conjugal Precepts' for ancient wisdom on partnership."
    },
    "keywords": ["plutarch", "moralia", "complete", "ethics", "wisdom"],
    "composite_of": l2_ids,
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
            {"name": "Plutarch", "date": "46-120 CE", "note": "Author"},
            {"name": "William W. Goodwin", "date": "1874", "note": "Editor/Translator"},
            {"name": "Project Gutenberg", "date": "2007", "note": "Source: eBook #23639"}
        ]
    },
    "name": "Plutarch's Moralia",
    "description": "Plutarch's moral essays — practical wisdom on education, marriage, anger, friendship, fortune, and the cultivation of character. These essays reveal the humane, psychologically astute side of one of antiquity's greatest writers.\n\nSource: Project Gutenberg eBook #23639 (https://www.gutenberg.org/ebooks/23639)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Ancient Roman portraits and busts. Illustrations from 19th century editions of Plutarch's works.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["plutarch", "moralia", "ethics", "virtue", "ancient-greece", "ancient-rome", "practical-wisdom", "marriage", "anger", "friendship"],
    "roots": ["western-philosophy", "classical-antiquity"],
    "shelves": ["wisdom"],
    "lineages": ["Linehan", "Gottman", "Johnson"],
    "worldview": "dialectical",
    "items": items
}

os.makedirs("grammars/plutarchs-morals", exist_ok=True)
with open("grammars/plutarchs-morals/grammar.json", "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

print(f"Generated {len(items)} items")
print(f"L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
