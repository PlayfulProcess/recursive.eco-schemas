#!/usr/bin/env python3
"""
Build grammar.json for The Critique of Pure Reason by Immanuel Kant.

Source: Project Gutenberg eBook #4280
Author: Immanuel Kant (1781/1787)
Translator: J. M. D. Meiklejohn

Structure:
- L1: Major divisions (Prefaces, Introduction, Transcendental Aesthetic,
      Transcendental Analytic, Transcendental Dialectic, Doctrine of Method chapters)
- L2: Thematic groupings (4 themes)
- L3: Meta-categories (The Complete Work)

This is a very large and dense text. L1 items are at the level of major
divisions/books, not individual sections or paragraphs.
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "critique-pure-reason.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "critique-pure-reason"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Major sections to extract, in order. Each has a start pattern and the next one ends it.
DIVISIONS = [
    {
        "key": "preface-first-edition",
        "name": "Preface to the First Edition (1781)",
        "start_pattern": r'^PREFACE TO THE FIRST EDITION 1781\s*$',
        "sort": 1,
    },
    {
        "key": "preface-second-edition",
        "name": "Preface to the Second Edition (1787)",
        "start_pattern": r'^PREFACE TO THE SECOND EDITION 1787\s*$',
        "sort": 2,
    },
    {
        "key": "introduction",
        "name": "Introduction",
        "start_pattern": r'^Introduction\s*$',
        "sort": 3,
    },
    {
        "key": "transcendental-aesthetic",
        "name": "Transcendental Aesthetic",
        "start_pattern": r'^FIRST PART\. TRANSCENDENTAL ÆSTHETIC\.\s*$',
        "sort": 4,
    },
    {
        "key": "analytic-of-conceptions",
        "name": "Analytic of Conceptions (Book I)",
        "start_pattern": r'^BOOK I\. Analytic of Conceptions',
        "sort": 5,
    },
    {
        "key": "analytic-of-principles",
        "name": "Analytic of Principles (Book II)",
        "start_pattern": r'^BOOK II\. Analytic of Principles\s*$',
        "sort": 6,
    },
    {
        "key": "transcendental-dialectic-intro",
        "name": "Transcendental Dialectic — Introduction and Conceptions of Pure Reason",
        "start_pattern": r'^TRANSCENDENTAL DIALECTIC\.\s*$',
        "sort": 7,
    },
    {
        "key": "dialectic-paralogisms",
        "name": "Dialectic: Paralogisms of Pure Reason",
        "start_pattern": r'^Chapter I\. Of the Paralogisms of Pure Reason\s*$',
        "sort": 8,
    },
    {
        "key": "dialectic-antinomy",
        "name": "Dialectic: The Antinomy of Pure Reason",
        "start_pattern": r'^Chapter II\. The Antinomy of Pure Reason\s*$',
        "sort": 9,
    },
    {
        "key": "dialectic-ideal",
        "name": "Dialectic: The Ideal of Pure Reason",
        "start_pattern": r'^Chapter III\. The Ideal of Pure Reason\s*$',
        "sort": 10,
    },
    {
        "key": "discipline-of-pure-reason",
        "name": "The Discipline of Pure Reason",
        "start_pattern": r'^Chapter I\. The Discipline of Pure Reason\s*$',
        "sort": 11,
    },
    {
        "key": "canon-of-pure-reason",
        "name": "The Canon of Pure Reason",
        "start_pattern": r'^Chapter II\. The Canon of Pure Reason\s*$',
        "sort": 12,
    },
    {
        "key": "architectonic-of-pure-reason",
        "name": "The Architectonic of Pure Reason",
        "start_pattern": r'^Chapter III\. The Architectonic of Pure Reason\s*$',
        "sort": 13,
    },
    {
        "key": "history-of-pure-reason",
        "name": "The History of Pure Reason",
        "start_pattern": r'^Chapter IV\. The History of Pure Reason\s*$',
        "sort": 14,
    },
]

KEYWORDS = {
    "preface-first-edition": ["reason", "metaphysics", "critique", "knowledge", "experience"],
    "preface-second-edition": ["Copernican-revolution", "a-priori", "knowledge", "science", "reason"],
    "introduction": ["a-priori", "synthetic", "analytic", "judgement", "knowledge", "experience"],
    "transcendental-aesthetic": ["space", "time", "intuition", "sensibility", "a-priori", "phenomena"],
    "analytic-of-conceptions": ["categories", "understanding", "concepts", "logic", "deduction", "judgement"],
    "analytic-of-principles": ["schematism", "analogies", "causality", "substance", "phenomena", "noumena"],
    "transcendental-dialectic-intro": ["reason", "ideas", "illusion", "dialectic", "unconditioned"],
    "dialectic-paralogisms": ["soul", "self", "psychology", "paralogism", "substance", "identity"],
    "dialectic-antinomy": ["cosmology", "infinity", "freedom", "causality", "antinomy", "thesis", "antithesis"],
    "dialectic-ideal": ["God", "theology", "existence", "ontological", "cosmological", "proof"],
    "discipline-of-pure-reason": ["discipline", "dogmatism", "polemics", "hypothesis", "proof"],
    "canon-of-pure-reason": ["practical-reason", "morality", "freedom", "God", "immortality", "hope"],
    "architectonic-of-pure-reason": ["system", "science", "architecture", "philosophy", "metaphysics"],
    "history-of-pure-reason": ["history", "dogmatism", "empiricism", "scepticism", "criticism"],
}

THEMES = [
    {
        "id": "theme-foundations",
        "name": "The Foundations of Critical Philosophy",
        "chapters": ["preface-first-edition", "preface-second-edition", "introduction"],
        "about": "Kant's revolutionary framing of the critical project. The First Preface (1781) diagnoses the 'battlefield of endless controversies' that is metaphysics. The Second Preface (1787) introduces the Copernican revolution: instead of knowledge conforming to objects, objects must conform to our faculty of knowledge. The Introduction defines the central question — 'How are synthetic a priori judgements possible?' — and maps the territory the Critique will traverse.",
        "for_readers": "The Second Preface is the best entry point — Kant at his most programmatic and clear. The Introduction is essential: Kant's distinction between analytic and synthetic judgements, and the discovery that our most important knowledge (mathematics, physics, metaphysics) requires synthetic a priori judgements. This framing shapes everything that follows.",
    },
    {
        "id": "theme-sensibility-understanding",
        "name": "Sensibility and Understanding: How Experience Is Possible",
        "chapters": ["transcendental-aesthetic", "analytic-of-conceptions", "analytic-of-principles"],
        "about": "The constructive heart of the Critique. The Transcendental Aesthetic shows that space and time are not properties of things but forms of our sensibility — the framework through which we receive all experience. The Analytic of Conceptions derives the twelve categories (substance, causality, etc.) as the pure concepts the understanding must apply to make experience intelligible. The Analytic of Principles shows how these categories apply to phenomena through schematism, yielding the fundamental principles of natural science. Together, these sections answer: how is objective experience possible?",
        "for_readers": "The Transcendental Aesthetic is the most accessible major section — space and time as forms of intuition. The Analytic gets difficult: the Metaphysical Deduction (deriving categories from logical forms of judgement) and Transcendental Deduction (proving categories apply to experience) are among the hardest passages in philosophy. The Analogies of Experience in the Principles section are remarkably rewarding — Kant's proof that causality is not discovered but imposed by the mind.",
    },
    {
        "id": "theme-dialectic-illusion",
        "name": "The Dialectic of Illusion: Reason's Inevitable Errors",
        "chapters": ["transcendental-dialectic-intro", "dialectic-paralogisms", "dialectic-antinomy", "dialectic-ideal"],
        "about": "Kant's devastating critique of traditional metaphysics. When reason tries to extend knowledge beyond experience, it inevitably generates three kinds of illusion: about the soul (paralogisms — rational psychology's false proofs of immortality), about the world (antinomies — equally compelling proofs that the universe is both finite and infinite, that freedom both exists and doesn't), and about God (the ideal — the failure of ontological, cosmological, and physico-theological proofs). The Antinomy section is the dramatic centre of the entire Critique.",
        "for_readers": "The Antinomies are the most dramatic philosophical writing Kant ever produced — four pairs of thesis and antithesis, each apparently proven, revealing reason's deep self-contradictions. The section on the Ideal dismantles the proofs of God's existence with surgical precision (the ontological argument's conflation of existence with predication remains decisive). The Paralogisms show why Descartes' 'I think therefore I am' doesn't prove what he thought it did.",
    },
    {
        "id": "theme-method-system",
        "name": "Method and System: The Architecture of Reason",
        "chapters": ["discipline-of-pure-reason", "canon-of-pure-reason", "architectonic-of-pure-reason", "history-of-pure-reason"],
        "about": "The Transcendental Doctrine of Method — how reason should proceed after the Critique has established its limits. The Discipline sets boundaries (reason cannot operate like mathematics). The Canon opens the door to practical reason: morality, freedom, God, and immortality re-enter not as objects of knowledge but as postulates of practical faith. The Architectonic envisions philosophy as a systematic whole. The History surveys the three stages of metaphysics: dogmatism, empiricism, and criticism.",
        "for_readers": "The Canon of Pure Reason is surprisingly moving — after 700 pages of demolition, Kant rebuilds. The famous questions appear here: 'What can I know? What ought I to do? What may I hope?' The Architectonic reveals Kant the system-builder, dreaming of philosophy as an organic unity. The History is a compressed but brilliant survey that places the Critique in the story of human thought.",
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
    """Remove title page and TOC — keep from first Preface onward."""
    match = re.search(r'^PREFACE TO THE FIRST EDITION 1781\s*$', text, re.MULTILINE)
    if match:
        return text[match.start():]
    return text


def clean_text(text):
    """Normalize whitespace and clean formatting artifacts."""
    # Remove [Illustration] markers
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_divisions(text):
    """Parse text into major divisions."""
    divisions = []

    for i, div in enumerate(DIVISIONS):
        match = re.search(div["start_pattern"], text, re.MULTILINE)
        if not match:
            print(f"WARNING: Could not find division '{div['name']}' with pattern '{div['start_pattern']}'")
            continue

        start = match.start()

        # Find start of next division
        if i + 1 < len(DIVISIONS):
            next_match = re.search(DIVISIONS[i + 1]["start_pattern"], text, re.MULTILINE)
            if next_match:
                end = next_match.start()
            else:
                end = len(text)
        else:
            end = len(text)

        div_text = text[start:end].strip()
        div_text = clean_text(div_text)

        divisions.append({
            'key': div['key'],
            'name': div['name'],
            'text': div_text,
            'sort': div['sort'],
        })

    return divisions


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = strip_front_matter(text)

    divisions = parse_divisions(text)
    print(f"Parsed {len(divisions)} divisions")

    items = []
    sort_order = 0

    # L1: Major divisions
    for div in divisions:
        sort_order += 1
        keywords = KEYWORDS.get(div['key'], ["kant", "reason", "critique"])

        items.append({
            "id": div['key'],
            "name": div['name'],
            "sort_order": sort_order,
            "level": 1,
            "category": "division",
            "sections": {
                "Text": div['text'],
            },
            "keywords": keywords,
            "metadata": {}
        })
        print(f"  {div['key']}: {div['name']} ({len(div['text'])} chars)")

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
                "division_count": len(theme["chapters"]),
            }
        })

    # L3: Meta-category
    sort_order += 1
    items.append({
        "id": "critique-pure-reason-complete",
        "name": "The Critique of Pure Reason: The Complete Work",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "Immanuel Kant's Critique of Pure Reason (Kritik der reinen Vernunft, 1781; second edition 1787) is the founding text of modern philosophy. Kant's 'Copernican revolution' argues that the mind does not passively receive reality but actively structures experience through forms of sensibility (space and time) and categories of understanding (causality, substance, etc.). This makes objective science possible but also means that reason, when it tries to know things beyond experience — the soul, the cosmos as a whole, God — inevitably falls into illusion. The Critique thus draws the boundaries of human knowledge: we can know phenomena (things as they appear to us) but never noumena (things in themselves). Within these boundaries, science is secure; beyond them, only practical reason (morality) can guide us.",
            "For Readers": "The Critique is one of the most difficult and most rewarding books in the Western canon. Start with the Second Preface for the Copernican revolution. The Introduction defines synthetic a priori knowledge. The Transcendental Aesthetic (space and time) is the most accessible section. The Analytic is the hardest but most important — the categories and their deduction. The Dialectic is the most dramatic — the antinomies are breathtaking philosophical theatre. The Doctrine of Method contains Kant's most humane writing, especially the Canon's three questions: What can I know? What ought I to do? What may I hope?",
        },
        "keywords": ["kant", "critique", "reason", "knowledge", "metaphysics", "a-priori", "categories"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Immanuel Kant",
                    "date": "1781/1787",
                    "note": "Author"
                },
                {
                    "name": "J. M. D. Meiklejohn",
                    "date": "1855",
                    "note": "Translator"
                }
            ]
        },
        "name": "Critique of Pure Reason",
        "description": "Immanuel Kant's Critique of Pure Reason (Kritik der reinen Vernunft, 1781; second edition 1787) — the founding text of critical philosophy and one of the most important works in the history of Western thought. Kant's 'Copernican revolution' argues that the mind actively structures experience through forms of sensibility and categories of understanding, making science possible but setting limits on metaphysical knowledge. Fourteen major divisions cover the Transcendental Aesthetic (space and time), Analytic (categories and principles), Dialectic (illusions about soul, cosmos, and God), and Doctrine of Method. Translated by J. M. D. Meiklejohn.\n\nSource: Project Gutenberg eBook #4280 (https://www.gutenberg.org/ebooks/4280)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Portraits of Immanuel Kant, including the famous engraving after the painting by Döbler (1791). Views of Königsberg (now Kaliningrad). Title pages of the first and second editions (1781, 1787). Diagrams from 19th-century commentaries illustrating the table of categories and the architectonic of pure reason.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "epistemology", "metaphysics", "reason", "knowledge", "Enlightenment", "public-domain", "full-text"],
        "roots": ["process-philosophy"],
        "shelves": ["mirror"],
        "lineages": ["Andreotti"],
        "worldview": "rationalist",
        "items": items,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1: {l1} divisions, L2: {l2} themes, L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
