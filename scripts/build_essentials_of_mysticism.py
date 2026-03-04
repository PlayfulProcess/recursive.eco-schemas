#!/usr/bin/env python3
"""
Parse The Essentials of Mysticism (Evelyn Underhill, Gutenberg #74203) into grammar.json.

Structure:
- L1: Individual essays (6 standalone + 3 medieval mystics + 3 modern French mystics = 12 total)
- L2: Groupings (Theory & Practice, Historical Mystics, Three Medieval, Modern French)
- L3: Meta-categories
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "essentials-of-mysticism.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "essentials-of-mysticism")
OUTPUT = os.path.join(OUTPUT_DIR, "grammar.json")


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1:
        text = text[text.index("\n", start) + 1:]
    if end != -1:
        text = text[:end]
    return text.strip()


# Essay definitions with their centered title patterns (as they appear in the text)
ESSAYS = [
    {
        "id": "essentials-of-mysticism",
        "name": "The Essentials of Mysticism",
        "title_pattern": "THE ESSENTIALS OF MYSTICISM",
        "keywords": ["mysticism", "definition", "experience", "God", "consciousness"],
    },
    {
        "id": "mystic-and-corporate-life",
        "name": "The Mystic and the Corporate Life",
        "title_pattern": "THE MYSTIC AND THE CORPORATE LIFE",
        "keywords": ["community", "church", "individual", "corporate", "religion"],
    },
    {
        "id": "mysticism-doctrine-atonement",
        "name": "Mysticism and the Doctrine of Atonement",
        "title_pattern": "MYSTICISM AND THE DOCTRINE OF ATONEMENT",
        "keywords": ["atonement", "theology", "redemption", "sacrifice", "Christ"],
    },
    {
        "id": "mystic-as-creative-artist",
        "name": "The Mystic as Creative Artist",
        "title_pattern": "THE MYSTIC AS CREATIVE ARTIST",
        "keywords": ["art", "creativity", "vision", "expression", "beauty"],
    },
    {
        "id": "education-of-spirit",
        "name": "The Education of the Spirit",
        "title_pattern": "THE EDUCATION OF THE SPIRIT",
        "keywords": ["education", "spiritual-growth", "training", "development"],
    },
    {
        "id": "will-intellect-feeling-prayer",
        "name": "The Place of Will, Intellect, and Feeling in Prayer",
        "title_pattern": "THE PLACE OF WILL, INTELLECT AND FEELING IN PRAYER",
        "keywords": ["prayer", "will", "intellect", "feeling", "contemplation"],
    },
    {
        "id": "mysticism-of-plotinus",
        "name": "The Mysticism of Plotinus",
        "title_pattern": "THE MYSTICISM OF PLOTINUS",
        "keywords": ["Plotinus", "Neoplatonism", "philosophy", "the-One", "emanation"],
    },
    {
        "id": "mirror-of-simple-souls",
        "name": "The Mirror of Simple Souls",
        "title_pattern": "MIRROR OF SIMPLE SOULS",
        "keywords": ["Marguerite-Porete", "annihilation", "soul", "love", "medieval"],
    },
    {
        "id": "blessed-angela-of-foligno",
        "name": "The Blessed Angela of Foligno",
        "title_pattern": "THE BLESSED ANGELA OF FOLIGNO",
        "keywords": ["Angela", "Franciscan", "vision", "suffering", "divine-love"],
    },
    {
        "id": "julian-of-norwich",
        "name": "Julian of Norwich",
        "title_pattern": "JULIAN OF NORWICH",
        "keywords": ["Julian", "anchoress", "revelations", "divine-love", "English-mysticism"],
    },
    {
        "id": "soeur-therese",
        "name": "Soeur Thérèse de l'Enfant-Jésus",
        "title_pattern": "ENFANT-J",
        "keywords": ["Therese", "Lisieux", "little-way", "Carmelite", "simplicity"],
    },
    {
        "id": "lucie-christine",
        "name": "Lucie-Christine",
        "title_pattern": "LUCIE-CHRISTINE",
        "keywords": ["Lucie-Christine", "lay-mystic", "married", "contemplation", "French"],
    },
    {
        "id": "charles-peguy",
        "name": "Charles Péguy",
        "title_pattern": "CHARLES PÉGUY",
        "keywords": ["Peguy", "poet", "patriot", "social-mysticism", "French"],
    },
]


def find_essay_boundaries(text):
    """Find the line numbers where each essay begins."""
    lines = text.split('\n')
    boundaries = []

    # Skip the table of contents and preface — find the first essay title
    # Each essay title appears as centered ALL CAPS text
    # We'll match against our known patterns

    for essay in ESSAYS:
        pattern = essay["title_pattern"]
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == pattern:
                # For sub-essays within "Three Medieval Mystics" and "Mysticism in Modern France",
                # we need to be careful not to match the TOC entries
                # Check that this isn't in the first 100 lines (TOC area)
                if i > 100:
                    boundaries.append((essay["id"], i))
                    break

    # Sort by line number
    boundaries.sort(key=lambda x: x[1])
    return boundaries, lines


def parse_essays(text):
    """Parse all essays from the text."""
    boundaries, lines = find_essay_boundaries(text)
    parsed = []

    for idx, (essay_id, start_line) in enumerate(boundaries):
        # End boundary
        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][1]
        else:
            end_line = len(lines)

        raw_content = '\n'.join(lines[start_line:end_line])

        # Clean: remove the centered title lines at the top
        # Remove lines that are purely decorative (all caps centered headers, roman numerals)
        content_lines = raw_content.split('\n')
        cleaned = []
        skip_header = True
        for cl in content_lines:
            stripped = cl.strip()
            if skip_header:
                # Skip centered title lines, blank lines, and sub-headers at the top
                if not stripped:
                    continue
                # Skip ALL CAPS title lines
                if stripped.upper() == stripped and len(stripped) > 3 and not stripped.startswith('_'):
                    continue
                # Skip roman numeral section headers like "I" or "II"
                if re.match(r'^[IVX]+\.?$', stripped):
                    continue
                # Skip quoted title lines
                if stripped.startswith('"') and stripped.endswith('"') and stripped.upper() == stripped:
                    continue
                skip_header = False
            cleaned.append(cl)

        content = '\n'.join(cleaned)
        # Normalize whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()

        # Find the essay definition
        essay_def = next(e for e in ESSAYS if e["id"] == essay_id)

        parsed.append({
            "id": essay_def["id"],
            "name": essay_def["name"],
            "content": content,
            "keywords": essay_def["keywords"],
        })

    return parsed


# Thematic groupings
THEMES = [
    {
        "id": "theme-theory-practice",
        "name": "Theory and Practice of Mysticism",
        "essays": ["essentials-of-mysticism", "mystic-and-corporate-life", "mysticism-doctrine-atonement",
                    "mystic-as-creative-artist", "education-of-spirit", "will-intellect-feeling-prayer"],
        "about": "The first six essays lay out Underhill's framework: what mysticism is (direct consciousness of God), how it relates to communal religion, what it means theologically, how it connects to artistic creation, how the spirit is trained, and how prayer engages will, intellect, and feeling. These are not abstract theories but practical maps of the interior landscape.",
        "for_readers": "Start here for Underhill's definitive answer to the question 'What is mysticism?' She cuts through centuries of confusion to identify the essential experience beneath all traditions: an overwhelming consciousness of God and of one's own soul."
    },
    {
        "id": "theme-historical-mystics",
        "name": "The Historical Mystics",
        "essays": ["mysticism-of-plotinus", "mirror-of-simple-souls", "blessed-angela-of-foligno",
                    "julian-of-norwich", "soeur-therese", "lucie-christine", "charles-peguy"],
        "about": "Seven portraits of mystics across seventeen centuries: from the pagan philosopher Plotinus to the modern French poet Péguy. Underhill shows how the same essential experience manifests in radically different lives — a Neoplatonist, a condemned heretic, a Franciscan visionary, an English anchoress, a Carmelite nun, a married laywoman, and a poet killed in the Great War.",
        "for_readers": "These essays demonstrate that mysticism is not one personality type or one tradition. The variety is the point: the path to God has been walked by philosophers and peasants, monks and mothers, artists and soldiers."
    },
    {
        "id": "theme-medieval-mystics",
        "name": "Three Medieval Mystics",
        "essays": ["mirror-of-simple-souls", "blessed-angela-of-foligno", "julian-of-norwich"],
        "about": "Three women mystics of the medieval church: the anonymous author of The Mirror of Simple Souls (now identified as Marguerite Porete, burned as a heretic in 1310), Angela of Foligno (a Franciscan visionary of extreme spiritual intensity), and Julian of Norwich (the English anchoress whose Revelations of Divine Love is among the most luminous texts in the language). Each represents a different mode of mystical experience: intellectual annihilation, passionate suffering, and serene love.",
        "for_readers": "For those interested in women's spiritual voices from the Middle Ages. These three women — one executed, one living in ecstatic extremity, one dwelling in quiet certainty — show the range and power of female mysticism."
    },
    {
        "id": "theme-modern-france",
        "name": "Mysticism in Modern France",
        "essays": ["soeur-therese", "lucie-christine", "charles-peguy"],
        "about": "Three French mystics of the modern era: Thérèse of Lisieux (the 'Little Flower'), who found God in the most ordinary acts of convent life; Lucie-Christine, a married woman whose interior life was as intense as any cloistered contemplative; and Charles Péguy, poet and patriot, whose mysticism fused social justice with Catholic devotion. Together they prove that mysticism did not end with the Middle Ages.",
        "for_readers": "These essays demolish the myth that mysticism requires special conditions. A nun, a wife and mother, and a poet-soldier — all found the same divine reality through utterly different paths."
    },
]


def build_grammar(essays):
    items = []
    sort_order = 0

    # L1: Individual essays
    for essay in essays:
        sort_order += 1
        items.append({
            "id": essay["id"],
            "name": essay["name"],
            "level": 1,
            "category": "essay",
            "sort_order": sort_order,
            "sections": {
                "Essay": essay["content"]
            },
            "keywords": essay["keywords"],
            "metadata": {}
        })

    # L2: Thematic groupings
    for theme in THEMES:
        sort_order += 1
        items.append({
            "id": theme["id"],
            "name": theme["name"],
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": theme["essays"],
            "sort_order": sort_order,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {"essay_count": len(theme["essays"])}
        })

    # L3: Meta-categories
    sort_order += 1
    items.append({
        "id": "meta-complete-work",
        "name": "The Essentials of Mysticism: Theory and Lives",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": ["theme-theory-practice", "theme-historical-mystics"],
        "sort_order": sort_order,
        "sections": {
            "About": "Underhill's collection moves from theory to biography, from the question 'What is mysticism?' to the question 'Who are the mystics?' The structure is itself an argument: mysticism cannot be understood through abstract definition alone. It must be seen in lives. The first half lays down principles; the second half tests them against the irreducible particularity of seven human beings who touched the Real. The whole is greater than either half — a complete introduction to the mystical life as both science and art.",
        },
        "keywords": [],
        "metadata": {}
    })

    sort_order += 1
    items.append({
        "id": "meta-women-mystics",
        "name": "Women's Voices in the Mystical Tradition",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": ["theme-medieval-mystics", "theme-modern-france"],
        "sort_order": sort_order,
        "sections": {
            "About": "Of the seven mystics Underhill profiles, five are women — and this is no accident. Underhill herself was the foremost woman scholar of mysticism in the English-speaking world, and she consistently championed female voices that the academic establishment overlooked. From Marguerite Porete (executed for her radical theology) to Lucie-Christine (a wife and mother living the contemplative life in secret), these women demonstrate that the mystical vocation has always belonged as much to women as to men, often against institutional resistance.",
        },
        "keywords": [],
        "metadata": {}
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    essays = parse_essays(text)
    print(f"Parsed {len(essays)} essays")

    for essay in essays:
        preview = essay["content"][:60].replace('\n', ' ')
        print(f"  {essay['name']}: {preview}...")

    items = build_grammar(essays)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Evelyn Underhill", "date": "1920", "note": "Author"},
            ]
        },
        "name": "The Essentials of Mysticism",
        "description": "The Essentials of Mysticism and Other Essays by Evelyn Underhill (1920). Thirteen essays on the theory and practice of mysticism, from its essential nature to its expression in the lives of mystics from Plotinus to Charles Péguy. Underhill — the premier English-language scholar of mysticism in the early twentieth century — offers both rigorous analysis and sympathetic portraiture.\n\nSource: Project Gutenberg eBook #74203 (https://www.gutenberg.org/ebooks/74203)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Pre-Raphaelite and Arts and Crafts movement imagery complements Underhill's sensibility. Also: medieval manuscript illuminations, particularly those depicting contemplative figures and visionary experiences. The photographs and engravings of the mystics discussed (Julian's cell at Norwich, Assisi, Lisieux) would provide visual context.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["mysticism", "contemplative", "theology", "spiritual-practice", "public-domain", "full-text", "essays", "women-writers"],
        "roots": ["mysticism", "christian-mysticism"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan", "Shrei"],
        "worldview": "contemplative",
        "items": items,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT}")
    print(f"  L1: {l1} essays, L2: {l2} emergent groups, L3: {l3} meta-categories")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    main()
