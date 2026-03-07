#!/usr/bin/env python3
"""
Build grammar.json for Creative Evolution by Henri Bergson.

Source: Project Gutenberg eBook #26163
Author: Henri Bergson (1907)
Translator: Arthur Mitchell (1911)

Structure:
- L1: Introduction + 4 chapters
- L2: Thematic groupings (3 themes)
- L3: Meta-categories (The Complete Work)
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "creative-evolution.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "creative-evolution"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Sections of the text in order
SECTIONS = [
    {
        "key": "introduction",
        "name": "Introduction",
        "pattern": r'^INTRODUCTION\s*$',
        "chapter_num": 0,
    },
    {
        "key": "chapter-1",
        "name": "Chapter I: The Evolution of Life — Mechanism and Teleology",
        "pattern": r'^CHAPTER I\s*$',
        "chapter_num": 1,
    },
    {
        "key": "chapter-2",
        "name": "Chapter II: The Divergent Directions of the Evolution of Life — Torpor, Intelligence, Instinct",
        "pattern": r'^CHAPTER II\s*$',
        "chapter_num": 2,
    },
    {
        "key": "chapter-3",
        "name": "Chapter III: On the Meaning of Life — The Order of Nature and the Form of Intelligence",
        "pattern": r'^CHAPTER III\s*$',
        "chapter_num": 3,
    },
    {
        "key": "chapter-4",
        "name": "Chapter IV: The Cinematographical Mechanism of Thought and the Mechanistic Illusion",
        "pattern": r'^CHAPTER IV\s*$',
        "chapter_num": 4,
    },
]

CHAPTER_KEYWORDS = {
    "introduction": ["intellect", "intuition", "evolution", "philosophy", "duration", "elan-vital"],
    "chapter-1": ["evolution", "mechanism", "teleology", "duration", "vital-impetus", "biology", "adaptation"],
    "chapter-2": ["evolution", "intelligence", "instinct", "torpor", "divergence", "consciousness", "animal", "plant"],
    "chapter-3": ["life", "intelligence", "order", "nature", "matter", "disorder", "creation", "knowledge"],
    "chapter-4": ["thought", "mechanism", "becoming", "cinematography", "Plato", "Aristotle", "Spencer", "Kant", "illusion"],
}

THEMES = [
    {
        "id": "theme-vital-impetus",
        "name": "The Vital Impetus (Élan Vital)",
        "chapters": ["introduction", "chapter-1"],
        "about": "Bergson's revolutionary concept of the élan vital — a vital impetus that drives the evolution of life not through mechanical causation or predetermined design, but through creative, unpredictable becoming. The Introduction frames the problem: our intellect, shaped by evolution to manipulate matter, cannot grasp life's inner movement. Chapter I shows why neither mechanism nor teleology can explain the actual evolution of organisms, arriving at the concept of a vital impetus that carries life forward like a current through matter.",
        "for_readers": "Start with the Introduction for Bergson's luminous overview — one of the great openings in philosophy. Then Chapter I builds the scientific case: a patient, brilliant dismantling of both Darwinian mechanism and teleological design, culminating in the concept of élan vital. These chapters changed how the 20th century thought about life.",
    },
    {
        "id": "theme-divergence-consciousness",
        "name": "Divergence and Forms of Consciousness",
        "chapters": ["chapter-2", "chapter-3"],
        "about": "How the original vital impetus splits into diverging tendencies — torpor (vegetation), instinct (arthropods), and intelligence (vertebrates leading to humanity). Bergson argues these are not grades of perfection but complementary solutions to the problem of living. Chapter II traces these diverging paths through the evolutionary record. Chapter III explores how intelligence, by its very nature, creates the geometrical, spatial world we inhabit — and how intuition might recapture what intelligence necessarily misses.",
        "for_readers": "Chapter II contains Bergson's most original biological thinking — the idea that plants, insects, and humans represent different 'solutions' rather than a hierarchy. Chapter III is the epistemological core: how our intellect manufactures the ordered world of science, and why a deeper knowledge requires intuition. Dense but rewarding.",
    },
    {
        "id": "theme-becoming-philosophy",
        "name": "Real Becoming and the History of Philosophy",
        "chapters": ["chapter-4"],
        "about": "Bergson's sweeping critique of Western philosophy as a 'cinematographical mechanism of thought' — we take snapshots of reality and string them together like frames of a film, missing the continuous flow of real becoming. From Plato and Aristotle through Descartes and Spinoza to Kant and Spencer, Bergson traces how philosophy has consistently substituted static concepts for living duration. The chapter culminates in a vision of philosophy as direct contact with creative becoming.",
        "for_readers": "Chapter IV is Bergson at his most ambitious and poetic. The cinematograph metaphor is unforgettable — our intellect works like a movie camera, taking still pictures and projecting them to simulate movement. The history of philosophy section (Plato through Spencer) is one of the most brilliant compressed surveys ever written. This is where Bergson's alternative vision crystallizes.",
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
    """Remove title page, TOC, translator's note — keep from INTRODUCTION onward."""
    match = re.search(r'^INTRODUCTION\s*$', text, re.MULTILINE)
    if match:
        return text[match.start():]
    return text


def strip_back_matter(text):
    """Remove INDEX and everything after."""
    match = re.search(r'^INDEX\s*$', text, re.MULTILINE)
    if match:
        return text[:match.start()]
    return text


def clean_text(text):
    """Clean up footnotes and normalize whitespace."""
    # Remove footnote references like [1], [48]
    text = re.sub(r'\[(\d+)\]', '', text)
    # Remove footnote blocks
    text = re.sub(r'\[Footnote \d+:.*?\]', '', text, flags=re.DOTALL)
    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_first_sentences(text, max_len=200):
    """Extract first couple sentences for a summary."""
    clean = ' '.join(text.split())
    clean = re.sub(r'_([^_]+)_', r'\1', clean)
    sentences = re.split(r'(?<=[.!?])\s+', clean)
    result = ""
    for s in sentences:
        if len(result) + len(s) + 1 > max_len:
            break
        result = (result + " " + s).strip()
    if not result and clean:
        result = clean[:max_len] + "..."
    return result


def parse_sections(text):
    """Parse text into introduction + 4 chapters."""
    sections = []

    for i, sec in enumerate(SECTIONS):
        match = re.search(sec["pattern"], text, re.MULTILINE)
        if not match:
            print(f"WARNING: Could not find section '{sec['name']}'")
            continue

        start = match.start()

        # Find start of next section
        if i + 1 < len(SECTIONS):
            next_match = re.search(SECTIONS[i + 1]["pattern"], text, re.MULTILINE)
            if next_match:
                end = next_match.start()
            else:
                end = len(text)
        else:
            end = len(text)

        section_text = text[start:end].strip()
        # Remove the heading lines (first few lines up to double newline)
        heading_end = section_text.find('\n\n')
        if heading_end != -1:
            # For chapters, skip the subtitle too
            remaining = section_text[heading_end:].strip()
            # Check if next block is a subtitle (all caps or short line)
            lines = remaining.split('\n\n', 1)
            if lines and len(lines[0]) < 200 and lines[0].isupper():
                if len(lines) > 1:
                    remaining = lines[1].strip()
            section_text = remaining

        section_text = clean_text(section_text)

        sections.append({
            'key': sec['key'],
            'name': sec['name'],
            'text': section_text,
            'chapter_num': sec['chapter_num'],
        })

    return sections


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = strip_back_matter(text)
    text = strip_front_matter(text)

    sections = parse_sections(text)
    print(f"Parsed {len(sections)} sections")

    items = []
    sort_order = 0

    # L1: Individual sections
    for sec in sections:
        sort_order += 1
        keywords = CHAPTER_KEYWORDS.get(sec['key'], ["bergson", "evolution", "philosophy"])

        items.append({
            "id": sec['key'],
            "name": sec['name'],
            "sort_order": sort_order,
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": sec['text'],
            },
            "keywords": keywords,
            "metadata": {
                "chapter_number": sec['chapter_num'],
            }
        })
        print(f"  {sec['key']}: {sec['name']} ({len(sec['text'])} chars)")

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
        "id": "creative-evolution-complete",
        "name": "Creative Evolution: The Complete Work",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "Henri Bergson's Creative Evolution (L'Évolution créatrice, 1907) is one of the most influential philosophical works of the twentieth century, winning Bergson the Nobel Prize in Literature in 1927. Against both mechanistic science and teleological design, Bergson argues that life is driven by a vital impetus (élan vital) — a creative force that flows through matter like a current, splitting into divergent tendencies (plant, insect, human) as it encounters obstacles. The book's central insight is that our intellect, having evolved to manipulate solid matter, systematically distorts reality by spatializing time and freezing becoming into static snapshots — what Bergson brilliantly calls 'the cinematographical mechanism of thought.' Only intuition — a philosophical method that enters into the flow of duration — can grasp life's creative movement from within.",
            "For Readers": "Creative Evolution rewards patient reading. The Introduction is one of the great openings in philosophy — read it first for the vision. Chapters I and II build the biological argument with remarkable erudition. Chapter III is the most difficult but philosophically richest — Bergson's theory of knowledge. Chapter IV is the most dazzling — a compressed history of Western philosophy as a series of failed attempts to think real becoming. Bergson writes with extraordinary clarity for a philosopher; the prose itself demonstrates the fluid thinking he advocates.",
        },
        "keywords": ["bergson", "elan-vital", "evolution", "duration", "intuition", "philosophy"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Henri Bergson",
                    "date": "1907",
                    "note": "Author"
                },
                {
                    "name": "Arthur Mitchell",
                    "date": "1911",
                    "note": "Translator"
                }
            ]
        },
        "name": "Creative Evolution",
        "description": "Henri Bergson's Creative Evolution (L'Évolution créatrice, 1907) — the work that introduced élan vital into modern thought and won Bergson the Nobel Prize in Literature. Against both mechanism and teleology, Bergson argues that life is driven by a vital impetus that creates unpredictably as it flows through matter. Four chapters trace this impetus through the divergence of plant, insect, and human evolution, culminating in a brilliant critique of Western philosophy's inability to think real becoming. Translated by Arthur Mitchell (1911).\n\nSource: Project Gutenberg eBook #26163 (https://www.gutenberg.org/ebooks/26163)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs of Henri Bergson (early 1900s). Diagrams of evolutionary divergence from early 20th century biology texts. Ernst Haeckel's tree of life illustrations from Generelle Morphologie (1866). Early cinema apparatus illustrations showing the cinematograph mechanism Bergson uses as his central metaphor.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "evolution", "vitalism", "duration", "intuition", "process-philosophy", "public-domain", "full-text"],
        "roots": ["process-philosophy"],
        "shelves": ["mirror"],
        "lineages": ["Akomolafe"],
        "worldview": "process",
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
