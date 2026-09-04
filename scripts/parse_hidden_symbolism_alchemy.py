#!/usr/bin/env python3
"""
Parse Hidden Symbolism of Alchemy and the Occult Arts (Herbert Silberer, Gutenberg #27755).
3 parts × 10 sections → L1 items, with L2 parts + L3 meta.
"""
import json, re, os

with open("seeds/hidden-symbolism-alchemy.txt", encoding="utf-8") as f:
    text = f.read()

gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()

# Sections defined by centered headings in the body
# Format: centered "Part X." then centered "Section X." then title on next line
SECTIONS = [
    ("TRANSLATOR’S PREFACE", "translators-preface", "Translator's Preface", "framework"),
    ("The Parable.", "sec-parable", "The Parable", "parable"),
    ("Dream And Myth Interpretation.", "sec-dream-myth", "Dream and Myth Interpretation", "parable"),
    ("Psychoanalytic Interpretation Of The Parable.", "sec-psychoanalytic", "Psychoanalytic Interpretation of the Parable", "analytic"),
    ("Alchemy.", "sec-alchemy", "Alchemy", "analytic"),
    ("The Hermetic Art.", "sec-hermetic-art", "The Hermetic Art", "analytic"),
    ("Rosicrucianism And Freemasonry.", "sec-rosicrucian", "Rosicrucianism and Freemasonry", "analytic"),
    ("The Problem Of Multiple Interpretation.", "sec-multiple-interp", "The Problem of Multiple Interpretation", "analytic"),
    ("Introversion And Regeneration.", "sec-introversion", "Introversion and Regeneration", "synthetic"),
    ("The Goal Of The Work.", "sec-goal-of-work", "The Goal of the Work", "synthetic"),
    ("The Royal Art.", "sec-royal-art", "The Royal Art", "synthetic"),
    ("NOTES.", "notes", "Notes", "framework"),
    ("BIBLIOGRAPHY.", "bibliography", "Bibliography", "framework"),
]

body_lines = body.split("\n")
positions = []

for heading, sid, name, cat in SECTIONS:
    pos = -1
    for i, line in enumerate(body_lines):
        if line.strip() == heading or line.strip() == heading.rstrip("."):
            # Make sure it's not in TOC (TOC is in first ~100 lines)
            if i < 50:
                continue
            pos = sum(len(l) + 1 for l in body_lines[:i])
            break
    if pos < 0:
        # Try without trailing period
        clean = heading.rstrip(".")
        for i, line in enumerate(body_lines):
            if line.strip() == clean and i >= 50:
                pos = sum(len(l) + 1 for l in body_lines[:i])
                break
    if pos < 0:
        # Try uppercase
        for i, line in enumerate(body_lines):
            if line.strip().upper() == heading.upper() and i >= 50:
                pos = sum(len(l) + 1 for l in body_lines[:i])
                break
    positions.append((pos, heading, sid, name, cat))

# Sort by position
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
            if stripped == "" or stripped == heading or stripped == heading.rstrip(".") or stripped.upper() == heading.upper():
                continue
            if stripped.startswith("Part ") or stripped.startswith("Section "):
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
    if cat == "framework":
        level = 2

    items.append({
        "id": sid,
        "name": name,
        "sort_order": sort_order,
        "category": cat,
        "level": level,
        "sections": {"Text": excerpt},
        "keywords": ["alchemy", "symbolism", "silberer", "psychoanalysis"] + {
            "sec-parable": ["parable", "allegory", "wanderer"],
            "sec-dream-myth": ["dream", "myth", "interpretation", "freud"],
            "sec-psychoanalytic": ["freud", "psychoanalysis", "unconscious"],
            "sec-alchemy": ["alchemy", "prima-materia", "philosopher-stone", "transmutation"],
            "sec-hermetic-art": ["hermes", "thoth", "emerald-tablet", "as-above-so-below"],
            "sec-rosicrucian": ["rosicrucian", "freemasonry", "initiation", "secret-societies"],
            "sec-multiple-interp": ["hermeneutics", "anagogic", "multiple-meaning"],
            "sec-introversion": ["introversion", "regeneration", "meditation", "yoga"],
            "sec-goal-of-work": ["philosopher-stone", "gold", "spiritual-goal", "self"],
            "sec-royal-art": ["royal-art", "great-work", "opus-magnum", "individuation"],
        }.get(sid, []),
        "metadata": {}
    })
    sort_order += 1

# Astrology metadata
astrology_map = {
    "sec-alchemy": {"planets": ["Saturn", "Mercury"], "signs": ["Capricorn", "Virgo"], "themes": ["transmutation", "prima-materia"]},
    "sec-hermetic-art": {"planets": ["Mercury", "Neptune"], "signs": ["Gemini", "Pisces"], "themes": ["as-above-so-below", "hidden-knowledge"]},
    "sec-introversion": {"planets": ["Moon", "Neptune"], "signs": ["Cancer", "Pisces"], "themes": ["inner-journey", "meditation"]},
    "sec-goal-of-work": {"planets": ["Sun", "Pluto"], "signs": ["Leo", "Scorpio"], "themes": ["philosopher-stone", "transformation"]},
    "sec-royal-art": {"planets": ["Sun", "Jupiter"], "signs": ["Leo", "Sagittarius"], "themes": ["great-work", "individuation"]},
}
for item in items:
    if item["id"] in astrology_map:
        item["metadata"]["astrology"] = astrology_map[item["id"]]

# L2 Part groups
part_groups = [
    {
        "id": "part-parable",
        "name": "Part I: The Parable",
        "category": "part",
        "level": 2,
        "composite_of": ["sec-parable", "sec-dream-myth"],
        "sections": {
            "About": "Part I presents a mysterious alchemical parable — the story of a wanderer who descends into the earth, encounters symbolic trials, and achieves transformation — then shows how dream interpretation and myth analysis can unlock its hidden meanings.",
            "For Readers": "Read the Parable first as a story, letting it work on you before you analyze it. Then read the Dream and Myth Interpretation section to see how Silberer unpacks the symbolic layers."
        },
        "keywords": ["parable", "allegory", "dream"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "part-analytic",
        "name": "Part II: The Analytic Part",
        "category": "part",
        "level": 2,
        "composite_of": ["sec-psychoanalytic", "sec-alchemy", "sec-hermetic-art", "sec-rosicrucian", "sec-multiple-interp"],
        "sections": {
            "About": "Part II analyzes the parable through multiple lenses: Freudian psychoanalysis, the history and practice of alchemy, Hermetic philosophy, Rosicrucianism and Freemasonry, and the problem of multiple valid interpretations of a single symbol.",
            "For Readers": "The Alchemy section (Section II) and Hermetic Art (Section III) are the most relevant for understanding alchemical symbolism. The Multiple Interpretation section is philosophically the most original — Silberer argues that symbols have simultaneous valid meanings at different levels."
        },
        "keywords": ["analysis", "alchemy", "hermeticism", "freemasonry"],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "part-synthetic",
        "name": "Part III: The Synthetic Part",
        "category": "part",
        "level": 2,
        "composite_of": ["sec-introversion", "sec-goal-of-work", "sec-royal-art"],
        "sections": {
            "About": "Part III synthesizes the psychoanalytic and alchemical perspectives into a unified theory of spiritual development: introversion as the mechanism of psychological regeneration, the Philosopher's Stone as the goal of inner work, and the 'Royal Art' as the practice of conscious transformation.",
            "For Readers": "This is where Silberer's work most anticipates Jung's later psychology of individuation. The Royal Art section is the culmination — the union of psychological and spiritual development."
        },
        "keywords": ["synthesis", "individuation", "regeneration", "royal-art"],
        "relationship_type": "emergence",
        "metadata": {}
    },
]

for g in part_groups:
    g["sort_order"] = sort_order
    items.append(g)
    sort_order += 1

# L3 Meta card
items.append({
    "id": "meta-hidden-symbolism",
    "name": "The Hidden Symbolism: Where Psychology Met Alchemy",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "Herbert Silberer's 'Hidden Symbolism of Alchemy and the Occult Arts' (1914) is a forgotten masterpiece — the first systematic attempt to read alchemical texts through the lens of psychoanalysis. Silberer was a member of Freud's circle but went beyond Freud by recognizing that symbols operate at multiple levels simultaneously: a sexual level, a spiritual level, and a cosmic level. His concept of 'anagogic' interpretation (reading upward from matter to spirit) directly influenced Jung's later work on alchemy and individuation. Silberer committed suicide in 1923, and his work was largely forgotten — but it remains the missing link between Freud and Jung.",
        "Contemplation": "The alchemists said: 'Our gold is not common gold.' Silberer showed that the Philosopher's Stone was never about chemistry — it was about the transformation of the psyche. When you read 'dissolve and coagulate,' read: let the old self dissolve so a new self can crystallize. The laboratory is you."
    },
    "keywords": ["alchemy", "psychoanalysis", "symbolism", "individuation", "transformation"],
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
            {"name": "Herbert Silberer", "date": "1914", "note": "Original text: Problems of Mysticism and Its Symbolism"},
            {"name": "Smith Ely Jelliffe (translator)", "date": "1917", "note": "English translation"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, astrology metadata, and meta interpretation"}
        ]
    },
    "name": "Hidden Symbolism of Alchemy and the Occult Arts",
    "description": "Herbert Silberer's groundbreaking 1914 study connecting alchemical symbolism to psychoanalysis — the missing link between Freud and Jung. Through analysis of an alchemical parable, Silberer explores alchemy, Hermeticism, Rosicrucianism, and the psychology of spiritual transformation.\n\nSource: Project Gutenberg eBook #27755 (https://www.gutenberg.org/ebooks/27755).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Alchemical woodcuts from the Rosarium Philosophorum (1550). Emblems from Michael Maier's Atalanta Fugiens (1617). Illustrations from Basil Valentine's The Twelve Keys.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["alchemy", "psychoanalysis", "symbolism", "hermeticism", "occult", "jung", "freud"],
    "roots": ["western-philosophy", "mysticism"],
    "shelves": ["wisdom", "mirror"],
    "lineages": ["Shrei", "Akomolafe"],
    "worldview": "dialectical",
    "items": items
}

os.makedirs("grammars/hidden-symbolism-alchemy", exist_ok=True)
with open("grammars/hidden-symbolism-alchemy/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

ids = [i["id"] for i in items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in items for r in i.get("composite_of", []) if r not in ids]
print(f"Items: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
print(f"Sections: {sum(len(i.get('sections',{})) for i in items)}")
print(f"Dupes: {dupes}, Bad refs: {bad_refs}")
print(f"Sort OK: {[i['sort_order'] for i in items] == list(range(1, len(items)+1))}")
