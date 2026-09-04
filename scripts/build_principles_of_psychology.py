#!/usr/bin/env python3
"""
Build grammar.json for The Principles of Psychology (Volume 1) by William James.

Source: Project Gutenberg eBook #57628
Author: William James (1890)

Structure:
- L1: 16 chapters (Volume 1 only)
- L2: Thematic groupings (4 themes)
- L3: Meta-categories (The Complete Work)

Note: This is Volume 1 only (of 2). Volume 1 covers chapters I-XVI.
Chapters use format "CHAPTER IV.[136]" with optional footnote refs.
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "principles-of-psychology.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "principles-of-psychology"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Chapter titles extracted from the TOC
CHAPTERS = [
    ("I", "The Scope of Psychology"),
    ("II", "The Functions of the Brain"),
    ("III", "On Some General Conditions of Brain-Activity"),
    ("IV", "Habit"),
    ("V", "The Automaton-Theory"),
    ("VI", "The Mind-Stuff Theory"),
    ("VII", "The Methods and Snares of Psychology"),
    ("VIII", "The Relations of Minds to Other Things"),
    ("IX", "The Stream of Thought"),
    ("X", "The Consciousness of Self"),
    ("XI", "Attention"),
    ("XII", "Conception"),
    ("XIII", "Discrimination and Comparison"),
    ("XIV", "Association"),
    ("XV", "The Perception of Time"),
    ("XVI", "Memory"),
]

CHAPTER_KEYWORDS = {
    "chapter-1": ["psychology", "science", "mental-life", "consciousness", "brain", "scope"],
    "chapter-2": ["brain", "reflex", "hemispheres", "localization", "motor", "aphasia", "nerve-centres"],
    "chapter-3": ["brain-activity", "stimuli", "reaction-time", "cerebral", "neural"],
    "chapter-4": ["habit", "plasticity", "neural", "practice", "ethics", "character", "behavior"],
    "chapter-5": ["automaton", "consciousness", "epiphenomenalism", "materialism", "free-will"],
    "chapter-6": ["mind-stuff", "evolution", "consciousness", "unconscious", "soul"],
    "chapter-7": ["method", "introspection", "experiment", "error", "psychologists-fallacy"],
    "chapter-8": ["mind-body", "knowledge", "acquaintance", "consciousness", "time", "space"],
    "chapter-9": ["stream-of-consciousness", "thought", "continuity", "fringe", "transitive", "substantive"],
    "chapter-10": ["self", "identity", "ego", "consciousness", "personal-identity", "social-self", "spiritual-self"],
    "chapter-11": ["attention", "voluntary", "passive", "concentration", "discrimination", "neural"],
    "chapter-12": ["conception", "abstraction", "universals", "sameness", "meaning"],
    "chapter-13": ["discrimination", "comparison", "analysis", "abstraction", "Webers-law", "sensation"],
    "chapter-14": ["association", "contiguity", "similarity", "memory", "thought", "habit"],
    "chapter-15": ["time-perception", "duration", "present", "past", "temporal"],
    "chapter-16": ["memory", "recognition", "retention", "recall", "forgetting", "brain"],
}

THEMES = [
    {
        "id": "theme-brain-and-method",
        "name": "Brain, Body, and Method",
        "chapters": ["chapter-1", "chapter-2", "chapter-3", "chapter-7"],
        "about": "James's foundations: what psychology is, how the brain works, and how we should study the mind. Chapter I defines psychology as 'the Science of Mental Life' and insists that consciousness exists for practical purposes — to help organisms navigate their environment. Chapters II and III provide a remarkably clear account of brain function (localization, reflex action, the hemispheres) that remains impressive for 1890. Chapter VII addresses method with characteristic honesty — the difficulties of introspection, the psychologist's fallacy, and the need for experimental rigor.",
        "for_readers": "Start with Chapter I for James's manifesto — psychology as natural science. Chapter II is a tour de force of accessible neuroscience. Chapter VII is essential for understanding James's intellectual honesty about the limits of psychological method. These chapters show why James is considered the founder of American psychology.",
    },
    {
        "id": "theme-consciousness-theories",
        "name": "The Nature of Consciousness",
        "chapters": ["chapter-5", "chapter-6", "chapter-8", "chapter-9"],
        "about": "James's revolutionary account of consciousness. He demolishes the 'automaton theory' (that consciousness is an epiphenomenon) and the 'mind-stuff theory' (that complex consciousness is built from simple mental atoms). Chapter IX — 'The Stream of Thought' — is James's most famous and influential chapter, introducing the metaphor of consciousness as a flowing stream rather than a chain of linked ideas. Thought is personal, constantly changing, sensibly continuous, and always dealing with objects independent of itself.",
        "for_readers": "Chapter IX is the jewel of the entire work — one of the most important chapters in the history of psychology. James's five characteristics of thought changed how we understand consciousness. The metaphor of the 'stream' (vs. the older 'chain' or 'train' of ideas) influenced Bergson, Husserl, and the entire stream-of-consciousness literary movement (Joyce, Woolf, Faulkner). Read Chapter IX even if you read nothing else.",
    },
    {
        "id": "theme-self-and-attention",
        "name": "The Self and Attention",
        "chapters": ["chapter-10", "chapter-11"],
        "about": "James's groundbreaking analysis of selfhood and attention. Chapter X — 'The Consciousness of Self' — distinguishes the empirical self ('Me': material, social, and spiritual selves) from the pure ego ('I': the stream of consciousness itself). James's treatment of the social self ('a man has as many social selves as there are individuals who recognize him') anticipates social psychology by decades. Chapter XI gives attention its due as the mechanism by which consciousness selects from the blooming, buzzing confusion of experience.",
        "for_readers": "Chapter X is extraordinary — James invents the psychology of identity. His analysis of the material self, social self, and spiritual self feels contemporary (think social media's multiplication of social selves). The section on disorders of the self (alternating personalities, mediumship) reads like case studies from a modern clinical textbook. Chapter XI on attention is equally prescient — James's distinction between voluntary and involuntary attention remains fundamental.",
    },
    {
        "id": "theme-habit-and-cognition",
        "name": "Habit, Association, and the Cognitive Faculties",
        "chapters": ["chapter-4", "chapter-12", "chapter-13", "chapter-14", "chapter-15", "chapter-16"],
        "about": "James on the practical mechanisms of mental life. Chapter IV on Habit is one of his most famous — 'habit is the enormous fly-wheel of society' — showing how neural plasticity creates behavioral grooves, with powerful ethical implications. The cognitive chapters (Conception, Discrimination, Association, Time, Memory) build a comprehensive account of how the mind organizes, distinguishes, connects, and retains its experience. Throughout, James insists on the brain basis of mental operations while refusing to reduce consciousness to mechanism.",
        "for_readers": "Chapter IV on Habit is perhaps the most practically useful chapter in the entire work — James's maxims for habit formation ('Never suffer an exception,' 'Seize the first possible opportunity to act') still appear in self-help books. Chapter XIV on Association is the historical heart of empirical psychology — James's critical survey of associationism is masterly. Chapter XVI on Memory completes the cognitive picture with James's important distinction between primary (short-term) and secondary memory.",
    },
]


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        start_idx = text.index("\n", start_idx) + 1
    else:
        start_idx = 0
    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = len(text)
    return text[start_idx:end_idx]


def strip_front_matter(text):
    """Remove everything before the first actual chapter (after TOC)."""
    # The TOC has chapters listed, then after INDEX. the actual text begins
    # with "PSYCHOLOGY." followed by "CHAPTER I."
    # Find the PSYCHOLOGY. marker that precedes the actual text
    match = re.search(r'^PSYCHOLOGY\.\s*$', text, re.MULTILINE)
    if match:
        return text[match.start():]
    return text


def clean_text(text):
    """Clean up footnotes and normalize whitespace."""
    # Remove inline footnote references like [136], [215]
    text = re.sub(r'\[\d+\]', '', text)
    # Remove [Illustration] markers
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_chapters(text):
    """Parse text into 16 chapters."""
    chapters = []

    for i, (roman, title) in enumerate(CHAPTERS):
        # Match CHAPTER X. or CHAPTER X.[footnote]
        # Need to be careful: the TOC also has CHAPTER entries
        # We use the body text (after strip_front_matter removed the TOC)
        pattern = r'^CHAPTER ' + re.escape(roman) + r'\.(\[\d+\])?\s*$'

        matches = list(re.finditer(pattern, text, re.MULTILINE))
        if not matches:
            print(f"WARNING: Could not find Chapter {roman}: {title}")
            continue

        # Use the first match (should be in the body now)
        match = matches[0]
        start = match.start()

        # Find start of next chapter
        if i + 1 < len(CHAPTERS):
            next_roman = CHAPTERS[i + 1][0]
            next_pattern = r'^CHAPTER ' + re.escape(next_roman) + r'\.(\[\d+\])?\s*$'
            next_matches = list(re.finditer(next_pattern, text, re.MULTILINE))
            if next_matches:
                end = next_matches[0].start()
            else:
                end = len(text)
        else:
            # Last chapter - find INDEX or end
            idx_match = re.search(r'^INDEX\.\s*$', text, re.MULTILINE)
            if idx_match:
                end = idx_match.start()
            else:
                end = len(text)

        chapter_text = text[start:end].strip()
        chapter_text = clean_text(chapter_text)

        chapters.append({
            'num': i + 1,
            'roman': roman,
            'title': title,
            'text': chapter_text,
        })

    return chapters


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = strip_front_matter(text)

    chapters = parse_chapters(text)
    print(f"Parsed {len(chapters)} chapters")

    items = []
    sort_order = 0

    # L1: Individual chapters
    for ch in chapters:
        sort_order += 1
        chapter_id = f"chapter-{ch['num']}"
        keywords = CHAPTER_KEYWORDS.get(chapter_id, ["psychology", "consciousness", "mind"])

        items.append({
            "id": chapter_id,
            "name": f"Chapter {ch['roman']}: {ch['title']}",
            "sort_order": sort_order,
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": ch['text'],
            },
            "keywords": keywords,
            "metadata": {
                "chapter_number": ch['num'],
                "roman_numeral": ch['roman'],
            }
        })
        print(f"  Ch {ch['num']:2d} ({ch['roman']:>4s}): {ch['title']} ({len(ch['text'])} chars)")

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

    # L3: Meta-category
    sort_order += 1
    items.append({
        "id": "principles-of-psychology-complete",
        "name": "The Principles of Psychology (Volume 1): The Complete Work",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "William James's The Principles of Psychology (1890) is the founding text of American psychology and one of the great intellectual achievements of the nineteenth century. Written over twelve years, it combines rigorous empirical science with philosophical depth and literary brilliance. Volume 1 covers sixteen chapters, from the scope and methods of psychology through the brain, habit, consciousness, the self, attention, and memory. James's central insight — that consciousness is not a thing but a process, a stream rather than a chain — revolutionized psychology, philosophy, and literature. His analysis of habit, the self, and attention remain startlingly contemporary.",
            "For Readers": "James is one of the great prose stylists of American philosophy — the Principles is a pleasure to read. Start with Chapter IX ('The Stream of Thought') for the most famous and influential chapter. Chapter IV ('Habit') is the most practically useful — its maxims still appear in self-help books. Chapter X ('The Consciousness of Self') is the most philosophically rich. For the neuroscience foundations, Chapters I-III are remarkably clear. James's characteristic move is to start with the physiological facts, then reveal their philosophical implications with dazzling insight.",
        },
        "keywords": ["james", "psychology", "consciousness", "stream-of-thought", "self", "habit", "brain"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "William James",
                    "date": "1890",
                    "note": "Author"
                }
            ]
        },
        "name": "Principles of Psychology (Volume 1)",
        "description": "William James's The Principles of Psychology (1890) — the founding text of American psychology. Volume 1 covers sixteen chapters from the scope and methods of psychology through brain function, habit, the stream of consciousness, the self, attention, and memory. James writes with extraordinary clarity and literary brilliance, combining rigorous empirical observation with philosophical depth. His metaphor of consciousness as a 'stream' rather than a 'chain' revolutionized psychology, philosophy, and literature.\n\nSource: Project Gutenberg eBook #57628 (https://www.gutenberg.org/ebooks/57628)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs of William James (1890s-1900s). Brain diagrams from the original 1890 Henry Holt edition. Illustrations of experimental apparatus from 19th-century psychology laboratories. Portraits of James at Harvard.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["psychology", "consciousness", "philosophy", "neuroscience", "habit", "self", "attention", "memory", "public-domain", "full-text"],
        "roots": ["process-philosophy"],
        "shelves": ["mirror"],
        "lineages": ["Linehan", "Gottman"],
        "worldview": "pragmatist",
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
