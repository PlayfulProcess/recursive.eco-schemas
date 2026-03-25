#!/usr/bin/env python3
"""
Build grammar.json for On the Origin of Species by Charles Darwin.

Source: Project Gutenberg eBook #1228 (First Edition, 1859)
Author: Charles Darwin

Structure:
- L1: Introduction + 14 chapters
- L2: Thematic groupings (5 themes) + structural parts
- L3: Meta-categories
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "origin-of-species.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "origin-of-species"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Chapter definitions: (roman_numeral, title)
# Note: Introduction has no roman numeral
CHAPTER_DEFS = [
    (None, "INTRODUCTION."),
    ("I", "VARIATION UNDER DOMESTICATION."),
    ("II", "VARIATION UNDER NATURE."),
    ("III", "STRUGGLE FOR EXISTENCE."),
    ("IV", "NATURAL SELECTION."),
    ("V", "LAWS OF VARIATION."),
    ("VI", "DIFFICULTIES ON THEORY."),
    ("VII", "INSTINCT."),
    ("VIII", "HYBRIDISM."),
    ("IX", "ON THE IMPERFECTION OF THE GEOLOGICAL RECORD."),
    ("X", "ON THE GEOLOGICAL SUCCESSION OF ORGANIC BEINGS."),
    ("XI", "GEOGRAPHICAL DISTRIBUTION."),
    ("XII", "GEOGRAPHICAL DISTRIBUTION\u2014_continued_."),
    ("XIII", "MUTUAL AFFINITIES OF ORGANIC BEINGS: MORPHOLOGY:\nEMBRYOLOGY:\nRUDIMENTARY ORGANS."),
    ("XIV", "RECAPITULATION AND CONCLUSION."),
]

# Clean titles for display
CLEAN_TITLES = [
    "Introduction",
    "Variation Under Domestication",
    "Variation Under Nature",
    "Struggle for Existence",
    "Natural Selection",
    "Laws of Variation",
    "Difficulties on Theory",
    "Instinct",
    "Hybridism",
    "On the Imperfection of the Geological Record",
    "On the Geological Succession of Organic Beings",
    "Geographical Distribution",
    "Geographical Distribution (continued)",
    "Mutual Affinities of Organic Beings: Morphology, Embryology, Rudimentary Organs",
    "Recapitulation and Conclusion",
]

CHAPTER_IDS = [
    "introduction",
    "variation-under-domestication",
    "variation-under-nature",
    "struggle-for-existence",
    "natural-selection",
    "laws-of-variation",
    "difficulties-on-theory",
    "instinct",
    "hybridism",
    "imperfection-of-geological-record",
    "geological-succession-of-organic-beings",
    "geographical-distribution",
    "geographical-distribution-continued",
    "mutual-affinities-morphology-embryology",
    "recapitulation-and-conclusion",
]

CHAPTER_KEYWORDS = [
    ["introduction", "overview", "natural-selection", "species"],
    ["domestication", "variation", "pigeons", "selection", "breeding"],
    ["variation", "nature", "species", "varieties", "individual-differences"],
    ["struggle", "existence", "competition", "population", "checks"],
    ["natural-selection", "sexual-selection", "divergence", "adaptation", "extinction"],
    ["variation", "laws", "correlation", "use-disuse", "climate"],
    ["difficulties", "transitional-forms", "complex-organs", "instinct"],
    ["instinct", "behavior", "bees", "slave-making", "cuckoo"],
    ["hybridism", "sterility", "fertility", "crosses", "species"],
    ["geology", "fossils", "imperfection", "record", "extinction"],
    ["geology", "succession", "fossils", "extinction", "affinities"],
    ["geography", "distribution", "migration", "barriers", "islands"],
    ["geography", "dispersal", "freshwater", "islands", "alpine"],
    ["classification", "morphology", "embryology", "rudimentary-organs", "unity"],
    ["recapitulation", "conclusion", "grandeur", "entangled-bank", "natural-selection"],
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


def strip_front_matter(text):
    """Remove title page, TOC, and detailed contents.

    The actual text begins at the second INTRODUCTION. heading
    (the first is in the TOC).
    """
    # Find the second occurrence of "INTRODUCTION." on its own line
    matches = list(re.finditer(r'^INTRODUCTION\.\s*$', text, re.MULTILINE))
    if len(matches) >= 2:
        return text[matches[1].start():]
    elif matches:
        return text[matches[0].start():]
    return text


def strip_back_matter(text):
    """Remove INDEX and anything after the main text."""
    idx = text.find("\nINDEX.\n")
    if idx >= 0:
        text = text[:idx]
    return text.strip()


def parse_chapters(text):
    """Parse the Origin into Introduction + 14 chapters."""
    chapters = []

    # Find each chapter start
    chapter_starts = []

    # Introduction
    intro_match = re.search(r'^INTRODUCTION\.\s*$', text, re.MULTILINE)
    if intro_match:
        chapter_starts.append((0, intro_match.start()))

    # Numbered chapters: "CHAPTER I." through "CHAPTER XIV."
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC0-9]+)\.\s*$', re.MULTILINE)
    for m in chapter_pattern.finditer(text):
        chapter_starts.append((None, m.start()))

    # Sort by position
    chapter_starts.sort(key=lambda x: x[1])

    for i, (_, pos) in enumerate(chapter_starts):
        # Find the end of this chapter (start of next, or end of text)
        if i + 1 < len(chapter_starts):
            end = chapter_starts[i + 1][1]
        else:
            end = len(text)

        chunk = text[pos:end].strip()

        # Extract the chapter text (after the heading and sub-heading lines)
        # Skip the chapter heading, title, and topic summary
        lines = chunk.split('\n')

        # Find where the actual prose begins (after empty lines following header)
        text_start = 0
        blank_count = 0
        in_header = True
        for j, line in enumerate(lines):
            if in_header:
                if not line.strip():
                    blank_count += 1
                else:
                    if blank_count >= 2:
                        # We've passed through the header + topic summary
                        text_start = j
                        in_header = False
                    blank_count = 0

        # For the introduction, the structure is simpler
        if i == 0:
            # Skip "INTRODUCTION." and blank lines
            for j, line in enumerate(lines):
                if j == 0:
                    continue
                if line.strip():
                    text_start = j
                    break

        chapter_text = '\n'.join(lines[text_start:]).strip()
        # Clean up multiple blank lines
        chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)

        chapters.append({
            'index': i,
            'text': chapter_text,
        })

    return chapters


# Thematic groupings
THEMES = [
    {
        "id": "theme-variation-and-selection",
        "name": "Variation and Selection",
        "chapters": [
            "variation-under-domestication",
            "variation-under-nature",
            "natural-selection",
            "laws-of-variation",
        ],
        "about": "The foundation of Darwin's argument: variation exists everywhere in nature, as it does under domestication. Natural selection — the survival and reproduction of organisms best suited to their environment — acts on this variation to produce adaptation and divergence. These chapters build the positive case for evolution by natural selection, moving from the familiar (pigeon breeding) to the wild (the tangled bank).",
        "for_readers": "Start here. Darwin deliberately begins with what his readers knew — the breeding of pigeons and dogs — then extends the logic to nature. Chapter IV (Natural Selection) is the theoretical heart of the book. Read Chapter I and IV together for the core argument.",
    },
    {
        "id": "theme-struggle-and-competition",
        "name": "The Struggle for Existence",
        "chapters": [
            "struggle-for-existence",
        ],
        "about": "Darwin's examination of the relentless competition among living things — for food, space, mates, and survival. He shows that far more individuals are born than can possibly survive, creating the pressure that drives natural selection. This is not merely 'red in tooth and claw' — Darwin emphasizes complex interdependencies, where the number of cats in a district can determine which flowers grow there.",
        "for_readers": "Chapter III is Darwin's most ecological chapter, full of remarkable chains of dependency. His famous example of cats, mice, bumblebees, and clover shows systems thinking a century before the term was coined.",
    },
    {
        "id": "theme-difficulties-and-objections",
        "name": "Difficulties and Objections",
        "chapters": [
            "difficulties-on-theory",
            "instinct",
            "hybridism",
        ],
        "about": "Darwin's extraordinary intellectual honesty: he devotes three chapters to the hardest objections to his theory. How could complex organs like the eye evolve gradually? How do we explain instincts like the slave-making ant? Why are species hybrids often sterile? Rather than avoiding these difficulties, Darwin confronts them directly and shows how natural selection can account for each.",
        "for_readers": "These chapters reveal Darwin as a thinker willing to face the strongest arguments against his own theory. Chapter VI on the eye is legendary — Darwin writes 'To suppose that the eye... could have been formed by natural selection, seems, I freely confess, absurd in the highest possible degree' — and then proceeds to show it is not absurd at all.",
    },
    {
        "id": "theme-geological-evidence",
        "name": "The Geological Record",
        "chapters": [
            "imperfection-of-geological-record",
            "geological-succession-of-organic-beings",
        ],
        "about": "Darwin confronts the fossil record — both its evidence for evolution and its gaps. Why don't we find every transitional form? Because the geological record is profoundly incomplete, 'a history of the world imperfectly kept, and written in a changing dialect.' Despite this imperfection, the succession of fossil forms, from simple to complex, from ancient to recent, tells a story consistent with descent with modification.",
        "for_readers": "Chapter IX is Darwin's most defensive chapter, and yet it transforms a weakness into an insight: the imperfection of the geological record is itself explained by the theory. Chapter X then shows what the fossils do tell us — and it is powerful.",
    },
    {
        "id": "theme-geography-and-classification",
        "name": "Geography, Classification, and Unity of Type",
        "chapters": [
            "geographical-distribution",
            "geographical-distribution-continued",
            "mutual-affinities-morphology-embryology",
        ],
        "about": "The convergence of evidence. Why do oceanic islands have unique species related to those on the nearest mainland? Why do embryos of vastly different adult animals look so similar? Why do rudimentary organs exist? Darwin weaves geographical distribution, comparative anatomy, embryology, and classification into a single explanatory tapestry. By the end, the argument from multiple independent lines of evidence is overwhelming.",
        "for_readers": "These chapters are where Darwin's argument achieves its full cumulative force. The Galapagos examples in Chapter XI are famous, but Chapter XIII — on morphology, embryology, and rudimentary organs — is perhaps the most intellectually satisfying chapter in the book.",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = strip_front_matter(text)
    text = strip_back_matter(text)

    chapters = parse_chapters(text)
    print(f"Parsed {len(chapters)} chapters (expected 15: Intro + 14)")

    items = []
    sort_order = 0

    # L1: Individual chapters
    for i, ch in enumerate(chapters):
        sort_order += 1
        chapter_id = CHAPTER_IDS[i]
        chapter_name = CLEAN_TITLES[i]
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
                "chapter_number": i,  # 0 = Introduction
            }
        })
        print(f"  Ch {i:2d}: {chapter_name} ({len(ch['text'])} chars)")

    # L2: Thematic groupings
    all_theme_ids = []
    for theme in THEMES:
        sort_order += 1
        theme_id = theme["id"]
        all_theme_ids.append(theme_id)

        items.append({
            "id": theme_id,
            "name": theme["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": theme["chapters"],
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "chapter_count": len(theme["chapters"]),
            }
        })

    # L2: Structural grouping - Introduction and Conclusion frame
    sort_order += 1
    items.append({
        "id": "frame-introduction-conclusion",
        "name": "The Frame: Introduction and Conclusion",
        "sort_order": sort_order,
        "level": 2,
        "category": "structure",
        "relationship_type": "emergence",
        "composite_of": ["introduction", "recapitulation-and-conclusion"],
        "sections": {
            "About": "Darwin's opening and closing frame the entire argument. The Introduction modestly states the plan and the problem. The Recapitulation and Conclusion restates the argument with the confidence of having made the case, ending with one of the most famous passages in scientific writing: 'There is grandeur in this view of life, with its several powers, having been originally breathed into a few forms or into one; and that, whilst this planet has gone cycling on according to the fixed law of gravity, from so simple a beginning endless forms most beautiful and most wonderful have been, and are being, evolved.'",
            "For Readers": "Read the Introduction first and last. On first reading, it sets the stage. After you have read the full argument, return to it and see how Darwin carefully prepared the ground. The Conclusion is the emotional climax — read it slowly.",
        },
        "keywords": ["frame", "introduction", "conclusion", "grandeur"],
        "metadata": {}
    })

    # L3: Meta-category
    sort_order += 1
    items.append({
        "id": "origin-of-species-complete",
        "name": "On the Origin of Species",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids + ["frame-introduction-conclusion"],
        "sections": {
            "About": "Charles Darwin's On the Origin of Species (1859) is arguably the most important scientific book ever written. In a single volume, Darwin presented the theory of evolution by natural selection — the idea that species are not immutable creations but the products of variation, inheritance, competition, and differential survival over vast stretches of time. The book's power lies not in a single flash of insight but in the patient accumulation of evidence from domestication, biogeography, paleontology, embryology, and comparative anatomy. Darwin knew his argument would be controversial, so he built it like a legal case: premise, evidence, objections confronted, alternative explanations ruled out, convergent proof. The result changed biology, philosophy, and humanity's understanding of its own place in nature.",
            "For Readers": "The Origin rewards careful sequential reading — Darwin designed it as a cumulative argument. But you can also approach it thematically: variation and selection for the mechanism, difficulties and objections for Darwin's intellectual honesty, geology for deep time, geography and classification for convergent evidence. The prose is Victorian but remarkably clear. Darwin writes as a naturalist who has spent decades observing, and his examples (pigeons, barnacles, bees, Galapagos finches) make abstract ideas vivid.",
        },
        "keywords": ["evolution", "natural-selection", "darwin", "biology", "species"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Charles Darwin",
                    "date": "1859",
                    "note": "Author (First Edition)"
                }
            ]
        },
        "name": "On the Origin of Species",
        "description": "Charles Darwin's On the Origin of Species (1859, First Edition) — the foundational text of evolutionary biology. In 15 chapters (Introduction plus 14), Darwin presents the theory of evolution by natural selection, building a cumulative argument from variation under domestication through the struggle for existence, natural selection, the geological record, geographical distribution, and the unity of type revealed by comparative anatomy and embryology. 'There is grandeur in this view of life.'\n\nSource: Project Gutenberg eBook #1228 (https://www.gutenberg.org/ebooks/1228)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: The single diagram from the first edition (the tree of divergence in Chapter IV). Illustrations from later editions. Natural history illustrations by Ernst Haeckel (1834-1919). John Gould's bird illustrations from The Zoology of the Voyage of H.M.S. Beagle (1838-1843).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["science", "biology", "evolution", "natural-selection", "ecology", "public-domain", "full-text"],
        "roots": ["ecology-nature"],
        "shelves": ["earth"],
        "lineages": ["Akomolafe"],
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
