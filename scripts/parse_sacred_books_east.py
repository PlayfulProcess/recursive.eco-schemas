#!/usr/bin/env python3
"""
Parse Sacred Books of the East — anthology edited by Epiphanius Wilson (1900).
Includes Vedic Hymns, Zend-Avesta, Dhammapada, Upanishads, Koran selections, and Life of Buddha.
"""
import json, re, os

with open("seeds/sacred-books-east.txt", encoding="utf-8") as f:
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

# Find major section headings (the traditions)
# These are typically ALL CAPS multi-word headings on their own lines
major_sections = []
section_patterns = [
    "VEDIC HYMNS",
    "THE ZEND-AVESTA",
    "DHAMMAPADA",
    "UPANISHADS",
    "THE KORAN",
    "LIFE OF BUDDHA",
]

# Find these headings in the body (after TOC)
toc_end = 0
for i, line in enumerate(lines):
    if "VEDIC HYMNS" in line.strip() and i > 10:
        toc_end = i
        break

# Find all section headings and sub-headings after TOC
headings = []
for i, line in enumerate(lines):
    if i < toc_end:
        continue
    stripped = line.strip()
    if not stripped:
        continue

    # Check for major section headings
    for sp in section_patterns:
        if stripped == sp or stripped == "THE " + sp:
            headings.append((i, stripped, "major"))
            break
    else:
        # Check for sub-headings: relatively short ALL CAPS or Title Case lines
        # that aren't just random text
        if (stripped.isupper() and 3 < len(stripped) < 80 and
            not stripped.startswith("I ") and not stripped.startswith("II ") and
            stripped not in ["CONTENTS", "SACRED BOOKS OF THE EAST"] and
            not stripped.startswith("INCLUDING") and
            not re.match(r'^\d', stripped)):
            headings.append((i, stripped, "sub"))

# Manual approach: find major sections, then split by sub-headings within each
items = []
sort_order = 1

# Find major section boundaries
major_bounds = []
for i, line in enumerate(lines):
    stripped = line.strip()
    for sp in section_patterns:
        if stripped == sp and i > toc_end:
            major_bounds.append((i, sp))
            break

# Process each major section
tradition_items = {}
for sec_idx, (sec_start, sec_name) in enumerate(major_bounds):
    if sec_idx + 1 < len(major_bounds):
        sec_end = major_bounds[sec_idx + 1][0]
    else:
        sec_end = len(lines)

    # Find sub-section headings within this major section
    sub_headings = []
    for i in range(sec_start + 1, sec_end):
        stripped = lines[i].strip()
        if not stripped:
            continue
        # Look for Introduction or titled subsections
        if (stripped == "Introduction" or
            (stripped.istitle() and len(stripped) > 3 and len(stripped) < 80 and
             not stripped.startswith("(") and
             not re.match(r'^\d', stripped) and
             stripped not in ["Contents", "Sacred Books Of The East"])):
            # Check it's a heading (followed by blank or text, not continuing)
            if i + 1 < len(lines) and (lines[i+1].strip() == "" or len(lines[i+1].strip()) > len(stripped)):
                sub_headings.append((i, stripped))

    if not sub_headings:
        # Take the whole section as one item
        section_text = "\n".join(lines[sec_start+1:sec_end]).strip()
        clean_name = sec_name.title()
        item_id = re.sub(r'[^a-z0-9\s]', '', sec_name.lower())
        item_id = re.sub(r'\s+', '-', item_id.strip())

        items.append({
            "id": item_id,
            "name": clean_name,
            "sort_order": sort_order,
            "category": item_id,
            "level": 1,
            "sections": {"Text": truncate(section_text)},
            "keywords": ["sacred-texts", item_id]
        })
        tradition_items[sec_name] = [item_id]
        sort_order += 1
    else:
        tradition_items[sec_name] = []
        # Split into sub-sections
        for sub_idx, (sub_start, sub_name) in enumerate(sub_headings):
            if sub_idx + 1 < len(sub_headings):
                sub_end = sub_headings[sub_idx + 1][0]
            else:
                sub_end = sec_end

            sub_text = "\n".join(lines[sub_start+1:sub_end]).strip()
            if len(sub_text) < 50:
                continue

            parent_id = re.sub(r'[^a-z0-9\s]', '', sec_name.lower())
            parent_id = re.sub(r'\s+', '-', parent_id.strip())
            sub_id_part = re.sub(r'[^a-z0-9\s]', '', sub_name.lower())
            sub_id_part = re.sub(r'\s+', '-', sub_id_part.strip())[:40]
            item_id = f"{parent_id}-{sub_id_part}"

            items.append({
                "id": item_id,
                "name": sub_name,
                "sort_order": sort_order,
                "category": parent_id,
                "level": 1,
                "sections": {
                    "Text": truncate(sub_text),
                    "Tradition": sec_name.title()
                },
                "keywords": ["sacred-texts", parent_id, sub_id_part.split("-")[0] if sub_id_part else "text"]
            })
            tradition_items[sec_name].append(item_id)
            sort_order += 1

# Handle duplicate IDs
seen = {}
for item in items:
    if item["id"] in seen:
        seen[item["id"]] += 1
        item["id"] = f"{item['id']}-{seen[item['id']]}"
    else:
        seen[item["id"]] = 1

# L2: One per tradition
l2_ids = []
tradition_names = {
    "VEDIC HYMNS": ("Vedic Hymns", "Ancient hymns from the Rig Veda — prayers to Indra, Agni, Rudra, Soma, and other deities of the Vedic pantheon."),
    "THE ZEND-AVESTA": ("The Zend-Avesta", "Sacred texts of Zoroastrianism — creation myths, purity laws, and the cosmic struggle between Ahura Mazda and Angra Mainyu."),
    "DHAMMAPADA": ("The Dhammapada", "Sayings of the Buddha on the path to enlightenment — verses on mindfulness, suffering, and liberation."),
    "UPANISHADS": ("The Upanishads", "Philosophical dialogues on the nature of Brahman, Atman, and the ultimate reality underlying all existence."),
    "THE KORAN": ("Selections from the Koran", "Selected suras from the Quran — the revelation received by Muhammad, covering creation, judgment, and divine law."),
    "LIFE OF BUDDHA": ("The Life of Buddha", "Narrative of Siddhartha Gautama's journey from prince to enlightened teacher."),
}

for trad, trad_ids in tradition_items.items():
    if not trad_ids:
        continue
    tname, tdesc = tradition_names.get(trad, (trad.title(), ""))
    l2_id = f"tradition-{re.sub(r'[^a-z0-9]', '-', trad.lower()).strip('-')}"
    items.append({
        "id": l2_id,
        "name": tname,
        "sort_order": sort_order,
        "category": "tradition",
        "level": 2,
        "sections": {
            "About": tdesc,
            "Texts": f"{len(trad_ids)} selections"
        },
        "keywords": ["sacred-texts", tname.lower().replace(" ", "-")],
        "composite_of": trad_ids,
        "relationship_type": "emergence"
    })
    l2_ids.append(l2_id)
    sort_order += 1

# L3 meta
items.append({
    "id": "sacred-books-complete",
    "name": "Sacred Books of the East: Complete Anthology",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "An anthology of sacred literature from the world's major Eastern religious traditions, edited by Epiphanius Wilson (1900). Includes selections from the Vedic Hymns, Zend-Avesta (Zoroastrianism), Dhammapada (Buddhism), Upanishads (Hindu philosophy), the Koran (Islam), and the Life of Buddha.",
        "For Readers": "This anthology provides a gateway to the spiritual literature of Asia and the Middle East. Each tradition is represented by its most essential and accessible texts, making it an ideal starting point for comparative religion."
    },
    "keywords": ["sacred-texts", "anthology", "comparative-religion", "eastern-wisdom"],
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
            {"name": "Epiphanius Wilson", "date": "1900", "note": "Editor"},
            {"name": "Project Gutenberg", "note": "Source"}
        ]
    },
    "name": "Sacred Books of the East",
    "description": "An anthology of sacred literature from the world's Eastern religious traditions, edited by Epiphanius Wilson (1900). Includes Vedic Hymns, Zend-Avesta, Dhammapada, Upanishads, selections from the Koran, and the Life of Buddha.\n\nSource: Project Gutenberg\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Ancient Indian miniatures, Persian manuscript illuminations, Buddhist art from Gandhara and Ajanta, Islamic geometric patterns and calligraphy.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["sacred-texts", "comparative-religion", "vedas", "zoroastrianism", "buddhism", "upanishads", "quran", "eastern-wisdom"],
    "roots": ["eastern-wisdom", "mysticism"],
    "shelves": ["wisdom"],
    "lineages": ["Shrei", "Akomolafe"],
    "worldview": "non-dual",
    "items": items
}

os.makedirs("grammars/sacred-books-east", exist_ok=True)
with open("grammars/sacred-books-east/grammar.json", "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

print(f"Generated {len(items)} items")
print(f"L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
