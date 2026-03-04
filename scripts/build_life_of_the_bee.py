#!/usr/bin/env python3
"""
Build grammar.json for The Life of the Bee by Maurice Maeterlinck.

Source: Project Gutenberg eBook #4511
Author: Maurice Maeterlinck
Translator: Alfred Sutro (1901)

NOTE: The seed file at seeds/life-of-the-bee.txt was downloaded with
the wrong Gutenberg number (#18852, which is an architectural illustration
magazine). The correct Gutenberg number for The Life of the Bee is #4511.

To fix, run locally:
    curl -L -o seeds/life-of-the-bee.txt "https://www.gutenberg.org/cache/epub/4511/pg4511.txt"

Structure:
- L1: 7 chapters (or 8 depending on edition — some include "Appendix")
- L2: Thematic groupings (3 themes)
- L3: Meta-category
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "life-of-the-bee.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "life-of-the-bee"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Expected chapter structure (Maeterlinck / Sutro translation)
CHAPTER_TITLES = [
    "On the Threshold of the Hive",
    "The Swarm",
    "The Foundation of the City",
    "The Life of the Bee",
    "The Young Queens",
    "The Nuptial Flight",
    "The Massacre of the Males",
    "The Progress of the Race",
]

CHAPTER_IDS = [
    "on-the-threshold-of-the-hive",
    "the-swarm",
    "the-foundation-of-the-city",
    "the-life-of-the-bee",
    "the-young-queens",
    "the-nuptial-flight",
    "the-massacre-of-the-males",
    "the-progress-of-the-race",
]

CHAPTER_KEYWORDS = [
    ["hive", "bees", "observation", "apiculture", "introduction"],
    ["swarm", "departure", "colony", "migration", "queen"],
    ["wax", "comb", "architecture", "construction", "geometry"],
    ["worker-bee", "labor", "pollen", "honey", "division-of-labor"],
    ["queens", "royal-cells", "succession", "rivalry", "birth"],
    ["mating", "flight", "drones", "queen", "reproduction"],
    ["drones", "massacre", "autumn", "expulsion", "sacrifice"],
    ["evolution", "intelligence", "progress", "instinct", "future"],
]


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx >= 0:
        start_idx = text.index("\n", start_idx) + 1
    else:
        start_idx = 0
    end_idx = text.find(end_marker)
    if end_idx < 0:
        end_idx = len(text)
    return text[start_idx:end_idx]


def verify_seed(text):
    """Check that the seed file is actually The Life of the Bee."""
    if "Maeterlinck" in text or "Life of the Bee" in text:
        return True
    if "Brochure Series" in text or "Architectural Illustration" in text:
        print("ERROR: The seed file contains 'The Brochure Series of Architectural")
        print("Illustration' (Gutenberg #18852), NOT 'The Life of the Bee'.")
        print("")
        print("The correct Gutenberg number for The Life of the Bee is #4511.")
        print("To fix, run locally:")
        print("")
        print('  curl -L -o seeds/life-of-the-bee.txt \\')
        print('    "https://www.gutenberg.org/cache/epub/4511/pg4511.txt"')
        print("")
        return False
    return True


def parse_chapters(text):
    """Parse the book into chapters.

    The Life of the Bee uses roman numeral chapter headings,
    sometimes with the title on the next line.
    """
    chapters = []

    # Try multiple heading patterns
    # Pattern 1: "I -- ON THE THRESHOLD OF THE HIVE" (Roman numeral + dash + title)
    chapter_pattern = re.compile(
        r'^([IVXLC]+)\s+--\s+',
        re.MULTILINE
    )
    matches = list(chapter_pattern.finditer(text))

    # Filter to only valid chapter numbers (I through VIII)
    valid_romans = {'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'}
    matches = [m for m in matches if m.group(1) in valid_romans]

    if not matches:
        print("WARNING: Could not find 'I -- TITLE' pattern. Trying 'CHAPTER I' pattern...")
        chapter_pattern = re.compile(
            r'^(?:CHAPTER\s+)?([IVXLC]+)\s*$',
            re.MULTILINE
        )
        matches = list(chapter_pattern.finditer(text))
        matches = [m for m in matches if m.group(1) in valid_romans]

    if not matches:
        print("WARNING: Could not find chapter headings. Trying 'BOOK I' pattern...")
        chapter_pattern = re.compile(r'^BOOK\s+([IVXLC]+)', re.MULTILINE)
        matches = list(chapter_pattern.finditer(text))

    for i, match in enumerate(matches):
        start = match.start()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        chunk = text[start:end].strip()
        lines = chunk.split('\n')

        # Skip heading lines to get to prose
        text_start = 0
        blank_seen = 0
        for j, line in enumerate(lines):
            if j < 3 and not line.strip():
                blank_seen += 1
                continue
            if j < 5 and line.strip().isupper():
                continue  # Skip title lines
            if blank_seen >= 1 and line.strip() and j > 0:
                text_start = j
                break

        chapter_text = '\n'.join(lines[text_start:]).strip()
        chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)

        chapters.append({
            'index': i,
            'text': chapter_text,
        })

    return chapters


# Thematic groupings
THEMES = [
    {
        "id": "theme-society-and-labor",
        "name": "Society and Labor in the Hive",
        "chapters": [
            "on-the-threshold-of-the-hive",
            "the-foundation-of-the-city",
            "the-life-of-the-bee",
        ],
        "about": "Maeterlinck's exploration of the hive as a society: the extraordinary architecture of the comb, the division of labor among worker bees, and the ceaseless industry that sustains the colony. He describes the geometric perfection of wax cells, the ventilation systems, the guard bees, the foragers, and the nurses with a blend of scientific observation and philosophical wonder. The hive becomes a mirror for reflecting on human civilization, cooperation, and the meaning of work.",
        "for_readers": "Begin with On the Threshold of the Hive for Maeterlinck's method — patient observation elevated to philosophy. The Foundation of the City describes the astonishing architecture of the comb. The Life of the Bee gives the daily rhythms of the hive. Together these chapters form a portrait of collective intelligence that anticipates modern complexity science.",
    },
    {
        "id": "theme-queens-and-succession",
        "name": "Queens, Mating, and Succession",
        "chapters": [
            "the-swarm",
            "the-young-queens",
            "the-nuptial-flight",
        ],
        "about": "The dramatic arc of the hive's reproductive cycle: the mysterious decision to swarm, the rearing of young queens in their royal cells, the deadly rivalry among queens, and the extraordinary nuptial flight in which the queen mates in midair and returns to found a new dynasty. Maeterlinck writes these chapters with the tension of a novel — the suspense of the swarm's departure, the violence of queen succession, the ecstasy and tragedy of the mating flight.",
        "for_readers": "The Swarm is one of the great set pieces of nature writing — the hive's deliberate departure into the unknown. The Young Queens reads like court drama. The Nuptial Flight is both scientific and mythic. Read these for the story of the hive as epic.",
    },
    {
        "id": "theme-mortality-and-meaning",
        "name": "Mortality, Sacrifice, and the Spirit of the Hive",
        "chapters": [
            "the-massacre-of-the-males",
            "the-progress-of-the-race",
        ],
        "about": "The philosophical climax of the book. The Massacre of the Males describes the brutal autumn expulsion of the drones — those who have served their reproductive purpose are driven from the hive to die. The Progress of the Race steps back to ask what it all means: what is the 'spirit of the hive' that governs these collective behaviors? Maeterlinck reaches toward questions about consciousness, purpose, and the relationship between individual sacrifice and collective progress.",
        "for_readers": "The Massacre of the Males is shocking and unforgettable — nature red in tooth and claw, within the hive itself. The Progress of the Race is Maeterlinck's philosophical meditation on what the bees teach us about intelligence, purpose, and the arc of evolution. End here for the deepest questions.",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")

    if not verify_seed(raw):
        print("\nCannot build grammar with wrong seed file.")
        sys.exit(1)

    text = strip_gutenberg(raw)

    chapters = parse_chapters(text)
    print(f"Parsed {len(chapters)} chapters (expected 7-8)")

    if len(chapters) == 0:
        print("ERROR: No chapters found. The text may not be parseable.")
        sys.exit(1)

    items = []
    sort_order = 0

    # L1: Individual chapters
    num_chapters = min(len(chapters), len(CHAPTER_IDS))
    for i in range(num_chapters):
        ch = chapters[i]
        sort_order += 1
        chapter_id = CHAPTER_IDS[i]
        chapter_name = CHAPTER_TITLES[i]
        keywords = CHAPTER_KEYWORDS[i]

        items.append({
            "id": chapter_id,
            "name": chapter_name,
            "sort_order": sort_order,
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": ch['text'],
            },
            "keywords": keywords,
            "metadata": {
                "chapter_number": i + 1,
            }
        })
        print(f"  Ch {i+1}: {chapter_name} ({len(ch['text'])} chars)")

    # L2: Thematic groupings
    all_theme_ids = []
    existing_ids = {item["id"] for item in items}
    for theme in THEMES:
        sort_order += 1
        theme_id = theme["id"]
        all_theme_ids.append(theme_id)
        # Only include composite_of references that exist
        valid_refs = [c for c in theme["chapters"] if c in existing_ids]

        items.append({
            "id": theme_id,
            "name": theme["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": valid_refs,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "chapter_count": len(valid_refs),
            }
        })

    # L3: Meta-category
    sort_order += 1
    items.append({
        "id": "life-of-the-bee-complete",
        "name": "The Life of the Bee",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "Maurice Maeterlinck's The Life of the Bee (1901) is a philosophical meditation on the honeybee colony — one of the most extraordinary works of nature writing ever produced. Part natural history, part philosophy, part prose-poem, Maeterlinck describes the architecture of the comb, the drama of the swarm, the deadly succession of queens, the ecstatic nuptial flight, and the autumn massacre of the drones. Throughout, he asks what the 'spirit of the hive' — the mysterious intelligence that governs the colony — can teach us about consciousness, cooperation, sacrifice, and the meaning of life. Translated by Alfred Sutro, the book won Maeterlinck the Nobel Prize in Literature (1911).",
            "For Readers": "Read this book slowly. Maeterlinck writes in long, meditative paragraphs that reward attention. The narrative arc follows the lifecycle of the hive through a single season: from the threshold observation through the swarm, the building of a new city, the daily life of workers, the rearing of queens, the mating flight, and the final expulsion of the drones. Each chapter deepens the philosophical questions. The writing is luminous and strange — a Belgian symbolist poet looking into a beehive and finding the universe.",
        },
        "keywords": ["bees", "nature", "philosophy", "hive", "maeterlinck", "ecology"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Maurice Maeterlinck",
                    "date": "1901",
                    "note": "Author"
                },
                {
                    "name": "Alfred Sutro",
                    "date": "1901",
                    "note": "Translator (English)"
                }
            ]
        },
        "name": "The Life of the Bee",
        "description": "Maurice Maeterlinck's The Life of the Bee (1901) — a philosophical meditation on the honeybee colony that blends natural history, philosophy, and prose poetry. Maeterlinck describes the architecture of the comb, the drama of the swarm, the succession of queens, the nuptial flight, and the massacre of the drones, asking throughout what the 'spirit of the hive' can teach us about consciousness, cooperation, and the meaning of life. Translated by Alfred Sutro.\n\nSource: Project Gutenberg eBook #4511 (https://www.gutenberg.org/ebooks/4511)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: E.A. Butler's illustrations of bee anatomy and behavior. Karl von Frisch's early bee research diagrams. Botanical illustrations of bee-pollinated flowers by Pierre-Joseph Redoute (1759-1840). Natural history plates from 19th-century entomological works.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["nature", "philosophy", "bees", "ecology", "symbolism", "public-domain", "full-text"],
        "roots": ["ecology-nature"],
        "shelves": ["earth"],
        "lineages": ["Kelty"],
        "worldview": "naturalist",
        "items": items,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1: {l1} chapters, L2: {l2} themes, L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
