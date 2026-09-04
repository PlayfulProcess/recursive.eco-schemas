#!/usr/bin/env python3
"""
Parse Pistis Sophia (Gnostic text, Gutenberg #76266).
5 documents + introduction sections → L1 items, with L2 groups + L3 meta.
"""
import json, re, os

with open("seeds/pistis-sophia.txt", encoding="utf-8") as f:
    text = f.read()

gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()

body_lines = body.split("\n")

# Find the main sections by centered headings
# Introduction sections and the 5 Documents
SECTIONS = [
    ("INTRODUCTION", "introduction", "Introduction", "framework"),
    ("1. THE MANUSCRIPT AND ITS HISTORY", "intro-manuscript", "The Manuscript and Its History", "framework"),
    ("2. THE DOCUMENTS IN THE MS.", "intro-documents", "The Documents in the MS.", "framework"),
    ("3. PURPOSE AND COMPOSITION OF THE MS.", "intro-purpose", "The Purpose and Composition of the MS.", "framework"),
    ("4. THE AUTHORSHIP AND DATE OF THE DOCUMENTS", "intro-authorship", "The Authorship and Date of the Documents", "framework"),
    ("THE FIRST DOCUMENT", "doc-1", "The First Document", "scripture"),
    ("THE SECOND DOCUMENT", "doc-2", "The Second Document", "scripture"),
    ("THE THIRD DOCUMENT", "doc-3", "The Third Document", "scripture"),
    ("THE FOURTH DOCUMENT", "doc-4", "The Fourth Document", "scripture"),
    ("THE FIFTH DOCUMENT", "doc-5", "The Fifth Document", "scripture"),
]

positions = []
for heading, sid, name, cat in SECTIONS:
    pos = -1
    for i, line in enumerate(body_lines):
        stripped = line.strip()
        if stripped == heading and i > 100:  # Skip TOC
            pos = sum(len(l) + 1 for l in body_lines[:i])
            break
    if pos < 0:
        # Try case-insensitive
        for i, line in enumerate(body_lines):
            if line.strip().upper() == heading.upper() and i > 100:
                pos = sum(len(l) + 1 for l in body_lines[:i])
                break
    if pos < 0:
        # For intro subsections with numbering, try without the number
        clean = re.sub(r'^\d+\.\s*', '', heading)
        for i, line in enumerate(body_lines):
            if clean in line.strip() and i > 100 and i < 2500:
                pos = sum(len(l) + 1 for l in body_lines[:i])
                break
    positions.append((pos, heading, sid, name, cat))

positions.sort(key=lambda x: x[0] if x[0] >= 0 else 999999)

items = []
sort_order = 1

for idx, (pos, heading, sid, name, cat) in enumerate(positions):
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
            if stripped == "" or stripped == heading or stripped.upper() == heading.upper():
                continue
            if stripped.startswith("LITERAL TRANSLATION"):
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

    level = 1
    if cat == "framework" and sid == "introduction":
        level = 2

    items.append({
        "id": sid,
        "name": name,
        "sort_order": sort_order,
        "category": cat,
        "level": level,
        "sections": {"Text": excerpt},
        "keywords": ["gnostic", "pistis-sophia", "coptic", "jesus", "mary-magdalene"] + {
            "intro-manuscript": ["manuscript", "british-museum", "coptic"],
            "intro-documents": ["textual-analysis", "structure"],
            "intro-purpose": ["gnosticism", "purpose", "composition"],
            "intro-authorship": ["valentinian", "authorship", "dating"],
            "doc-1": ["sophia", "fall", "repentance", "archons", "aeons"],
            "doc-2": ["sophia", "rescue", "light", "redemption"],
            "doc-3": ["mysteries", "baptism", "salvation", "light-treasury"],
            "doc-4": ["sin", "punishment", "fate", "reincarnation"],
            "doc-5": ["apostles", "disciples", "final-teaching"],
        }.get(sid, []),
        "metadata": {}
    })
    sort_order += 1

# Astrology metadata for key sections
astrology_map = {
    "doc-1": {"planets": ["Neptune", "Pluto"], "signs": ["Pisces", "Scorpio"], "themes": ["fall", "sophia", "divine-feminine"]},
    "doc-2": {"planets": ["Sun", "Neptune"], "signs": ["Leo", "Pisces"], "themes": ["redemption", "light", "rescue"]},
    "doc-3": {"planets": ["Neptune", "Jupiter"], "signs": ["Pisces", "Sagittarius"], "themes": ["mystery", "initiation", "baptism"]},
    "doc-4": {"planets": ["Saturn", "Pluto"], "signs": ["Capricorn", "Scorpio"], "themes": ["karma", "judgment", "fate"]},
    "doc-5": {"planets": ["Mercury", "Sun"], "signs": ["Gemini", "Leo"], "themes": ["teaching", "revelation", "gnosis"]},
}
for item in items:
    if item["id"] in astrology_map:
        item["metadata"]["astrology"] = astrology_map[item["id"]]

# L2 groups
groups = [
    {
        "id": "group-introduction",
        "name": "Introduction: The Manuscript and Its World",
        "category": "introduction",
        "level": 2,
        "composite_of": ["intro-manuscript", "intro-documents", "intro-purpose", "intro-authorship"],
        "sections": {
            "About": "Francis Legge's scholarly introduction to the Pistis Sophia manuscript — its discovery, its structure (five documents of varying date and authorship), its place in Gnostic literature, and the question of who wrote it and when. Essential context for understanding the most complete Gnostic scripture that survives.",
            "For Readers": "Read the Introduction sections before diving into the Documents — they explain the complex cosmology and terminology that the text assumes the reader already knows."
        },
        "keywords": ["introduction", "manuscript", "gnosticism", "scholarship"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "group-sophia-drama",
        "name": "The Drama of Sophia: Fall and Redemption",
        "category": "sophia-drama",
        "level": 2,
        "composite_of": ["doc-1", "doc-2"],
        "sections": {
            "About": "The central narrative of the Pistis Sophia: the divine feminine principle (Sophia/Wisdom) falls from the realm of light, is tormented by the archons (cosmic rulers), and cries out in thirteen repentances — each linked to a Psalm. Jesus descends to rescue her and restore her to her place in the light. This is the Gnostic myth that underlies all later Western mysticism about the exiled soul.",
            "For Readers": "The First Document contains Sophia's thirteen repentances — the emotional heart of the text. Read them as poetry, as the cry of the soul lost in matter yearning for return to the light."
        },
        "keywords": ["sophia", "fall", "repentance", "redemption", "divine-feminine"],
        "relationship_type": "emergence",
        "metadata": {"astrology": {"planets": ["Neptune", "Venus", "Pluto"], "signs": ["Pisces", "Libra", "Scorpio"], "themes": ["sophia", "fall-and-redemption", "divine-feminine"]}}
    },
    {
        "id": "group-mysteries-teaching",
        "name": "The Mysteries: Salvation Through Knowledge",
        "category": "teaching",
        "level": 2,
        "composite_of": ["doc-3", "doc-4", "doc-5"],
        "sections": {
            "About": "The later Documents shift from narrative to instruction: the mysteries of baptism and salvation, the fate of souls after death (including a complex system of reincarnation and punishment), and Jesus's final teachings to the apostles. Mary Magdalene emerges as the most perceptive disciple, asking the deepest questions.",
            "For Readers": "Document 3 describes the mystery of baptism — not the water ceremony but a spiritual transformation through light. Document 4 is the most challenging, with its detailed cosmology of archons and aeons."
        },
        "keywords": ["mysteries", "gnosis", "salvation", "mary-magdalene"],
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
    "id": "meta-pistis-sophia",
    "name": "Pistis Sophia: The Exiled Soul's Cry for Light",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "The Pistis Sophia is the most complete Gnostic scripture to survive — a Coptic text from 3rd-4th century Egypt, now in the British Museum. It records the resurrected Jesus teaching his disciples for eleven years after the resurrection, revealing the mysteries of the cosmos. At its center is the myth of Sophia (Wisdom) — a divine being who falls from the realm of light, is trapped by hostile cosmic powers, and cries out in thirteen repentances until Jesus descends to rescue her. This myth — the exile of the divine feminine, the soul lost in matter, the longing for return to the light — became the template for all subsequent Western mysticism, from Kabbalah to alchemy to Romanticism.",
        "Contemplation": "Sophia fell because she desired to know the Light — and that desire itself became her prison. The Gnostics saw this as the human condition: we are fragments of light trapped in matter, remembering something we cannot name. Is this a pathology to be cured, or a sacred homesickness that drives all creativity, all love, all seeking?"
    },
    "keywords": ["gnostic", "sophia", "divine-feminine", "light", "gnosis", "redemption"],
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
            {"name": "George Horner (translator)", "date": "1924", "note": "Literal translation from Coptic"},
            {"name": "Francis Legge", "date": "1924", "note": "Introduction and scholarly apparatus"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, thematic groupings, astrology metadata, and meta interpretation"}
        ]
    },
    "name": "Pistis Sophia",
    "description": "The most complete Gnostic scripture — a Coptic text recording the resurrected Jesus teaching his disciples the mysteries of the cosmos. At its center: the myth of Sophia (Wisdom), who falls from the light, is trapped by archons, and cries out in thirteen repentances until rescued by Jesus. Five documents covering the drama of the fallen divine feminine, the mysteries of baptism and salvation, and the fate of souls after death.\n\nSource: Project Gutenberg eBook #76266 (https://www.gutenberg.org/ebooks/76266).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Gnostic gems and amulets from the British Museum. William Blake's visionary paintings (particularly 'The Ancient of Days' and 'Satan in his Original Glory'). Byzantine icons of Christ Pantocrator and Sophia/Wisdom.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["gnostic", "sophia", "coptic", "christianity", "esoteric", "divine-feminine", "mystery"],
    "roots": ["mysticism", "western-philosophy"],
    "shelves": ["wisdom"],
    "lineages": ["Shrei"],
    "worldview": "non-dual",
    "items": items
}

os.makedirs("grammars/pistis-sophia", exist_ok=True)
with open("grammars/pistis-sophia/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

ids = [i["id"] for i in items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in items for r in i.get("composite_of", []) if r not in ids]
print(f"Items: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
print(f"Sections: {sum(len(i.get('sections',{})) for i in items)}")
print(f"Dupes: {dupes}, Bad refs: {bad_refs}")
print(f"Sort OK: {[i['sort_order'] for i in items] == list(range(1, len(items)+1))}")
