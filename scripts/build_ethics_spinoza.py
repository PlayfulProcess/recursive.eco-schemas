#!/usr/bin/env python3
"""
Build grammar.json for Ethics by Baruch Spinoza.

Source: Project Gutenberg eBook #3800
Author: Baruch Spinoza (1677)
Translator: R. H. M. Elwes

Structure:
- L1: 5 parts, each containing definitions, axioms, propositions
- L2: Thematic groupings (6 themes)
- L3: Meta-categories (The Complete Work, Thematic Arcs)
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "ethics-spinoza.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "ethics-spinoza"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# The five parts of the Ethics
PARTS = [
    {
        "id": "part-1",
        "name": "Part I: Concerning God",
        "search_pattern": r"PART I\.\s*CONCERNING GOD",
        "subtitle": "Concerning God",
    },
    {
        "id": "part-2",
        "name": "Part II: On the Nature and Origin of the Mind",
        "search_pattern": r"Part II\.",
        "subtitle": "On the Nature and Origin of the Mind",
    },
    {
        "id": "part-3",
        "name": "Part III: On the Origin and Nature of the Emotions",
        "search_pattern": r"PART III\.",
        "subtitle": "On the Origin and Nature of the Emotions",
    },
    {
        "id": "part-4",
        "name": "Part IV: Of Human Bondage, or the Strength of the Emotions",
        "search_pattern": r"PART IV:",
        "subtitle": "Of Human Bondage, or the Strength of the Emotions",
    },
    {
        "id": "part-5",
        "name": "Part V: Of the Power of the Understanding, or of Human Freedom",
        "search_pattern": r"PART V:",
        "subtitle": "Of the Power of the Understanding, or of Human Freedom",
    },
]

PART_KEYWORDS = {
    "part-1": ["God", "substance", "attribute", "nature", "infinity", "existence", "cause", "necessity"],
    "part-2": ["mind", "body", "idea", "thought", "extension", "knowledge", "perception", "intellect"],
    "part-3": ["emotions", "desire", "pleasure", "pain", "love", "hatred", "affects", "passions"],
    "part-4": ["bondage", "good", "evil", "virtue", "reason", "strength", "weakness", "servitude"],
    "part-5": ["freedom", "understanding", "blessedness", "eternity", "love-of-God", "wisdom", "liberation"],
}


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
    """Remove title page and front matter before Part I."""
    match = re.search(r'PART I\.\s*CONCERNING GOD', text)
    if match:
        return text[match.start():]
    return text


def parse_parts(text):
    """Parse the Ethics into its 5 parts."""
    parts = []

    for i, part_info in enumerate(PARTS):
        match = re.search(part_info["search_pattern"], text)
        if not match:
            print(f"WARNING: Could not find '{part_info['name']}'")
            continue

        start = match.start()

        # Find the start of the next part (or end of text)
        if i + 1 < len(PARTS):
            next_match = re.search(PARTS[i + 1]["search_pattern"], text[start + 10:])
            if next_match:
                end = start + 10 + next_match.start()
            else:
                end = len(text)
        else:
            end = len(text)

        part_text = text[start:end].strip()

        # Remove the part heading itself from the text content
        # Find where the actual content begins (after subtitle and blank lines)
        lines = part_text.split('\n')
        content_start = 0
        for j, line in enumerate(lines):
            stripped = line.strip()
            if j > 0 and (stripped.startswith('DEFINITION') or stripped.startswith('PREFACE') or
                          stripped.startswith('Most writers') or stripped.startswith('Human infirmity') or
                          stripped.startswith('At length') or stripped.startswith('I now pass')):
                content_start = j
                break

        content_text = '\n'.join(lines[content_start:]).strip()

        # Clean up: normalize whitespace
        content_text = re.sub(r'\n{3,}', '\n\n', content_text)

        parts.append({
            'id': part_info['id'],
            'name': part_info['name'],
            'subtitle': part_info['subtitle'],
            'text': content_text,
            'part_num': i + 1,
        })

    return parts


def extract_first_paragraph(text, max_len=300):
    """Extract the first meaningful paragraph for a summary."""
    clean = ' '.join(text.split())
    # Remove footnote markers
    clean = re.sub(r'\[\d+\]', '', clean)
    # Get first sentence or two
    sentences = re.split(r'(?<=[.!?])\s+', clean)
    result = ""
    for s in sentences:
        if len(result) + len(s) > max_len:
            break
        result += s + " "
    return result.strip() if result else clean[:max_len] + "..."


# Thematic groupings for L2
THEMES = [
    {
        "id": "theme-metaphysics-substance",
        "name": "Metaphysics of Substance",
        "parts": ["part-1"],
        "about": "The foundation of Spinoza's entire system: the proof that there is only one substance, which is God or Nature (Deus sive Natura). Through rigorous geometric demonstration, Spinoza establishes that substance is self-caused, infinite, and identical with the totality of reality. Every finite thing is a mode or modification of this one substance. This is the bedrock from which everything else in the Ethics follows.",
        "for_readers": "Part I is the most challenging section of the Ethics, written in strict axiomatic form. Read the Definitions first to understand Spinoza's technical vocabulary (substance, attribute, mode). The key insight arrives at Proposition 15: 'Whatever is, is in God, and nothing can exist or be conceived without God.' This is not conventional theism but radical immanence — God is not outside nature but identical with it.",
    },
    {
        "id": "theme-mind-body",
        "name": "Mind and Body",
        "parts": ["part-2"],
        "about": "Spinoza's revolutionary theory of mind-body parallelism. The mind and body are not two separate substances (as Descartes claimed) but one and the same thing expressed under two attributes — thought and extension. 'The order and connection of ideas is the same as the order and connection of things.' This dissolves the mind-body problem entirely: there is no interaction because there is no separation.",
        "for_readers": "Part II contains Spinoza's most original contribution to philosophy of mind. Proposition 7 ('The order and connection of ideas is the same as the order and connection of things') is one of the most consequential sentences in philosophy. Spinoza also develops his theory of knowledge here — the three kinds of knowledge that will become crucial in Part V's account of freedom.",
    },
    {
        "id": "theme-emotions-passions",
        "name": "The Life of the Emotions",
        "parts": ["part-3"],
        "about": "A systematic natural science of the emotions. Spinoza refuses to moralize about human passions — he wants to understand them as natural phenomena, 'as if it were a question of lines, planes, and bodies.' All emotions derive from three primary affects: desire (conatus), pleasure, and pain. Love is pleasure associated with an external cause; hatred is pain so associated. From these simple principles, Spinoza derives the full complexity of emotional life.",
        "for_readers": "Part III reads like a psychology textbook two centuries ahead of its time. Spinoza's account of how emotions work — projection, identification, rivalry, ambivalence — anticipates Freud. The definitions of the emotions at the end of Part III are a remarkable catalog. Pay special attention to the concept of conatus (Proposition 6): 'Each thing, in so far as it is in itself, endeavours to persist in its own being.'",
    },
    {
        "id": "theme-bondage-ethics",
        "name": "Human Bondage and Ethics",
        "parts": ["part-4"],
        "about": "Why we fail to act rationally even when we know what is good. Spinoza analyzes the power of passive emotions over reason, showing how we are 'in bondage' when driven by external causes we do not understand. But he also develops his positive ethics here: virtue is power, the good is what is truly useful to us, and the free person is guided by reason rather than fear. This part bridges the descriptive psychology of Part III with the liberation of Part V.",
        "for_readers": "Part IV is where Spinoza becomes most practical. His analysis of human weakness is unsentimental but compassionate — we are part of nature and cannot simply will ourselves free. The famous Appendix to Part IV contains Spinoza's most accessible ethical teachings: how to live well, the value of friendship, the role of cheerfulness. It reads like a philosophical self-help manual of extraordinary depth.",
    },
    {
        "id": "theme-freedom-blessedness",
        "name": "Freedom and Blessedness",
        "parts": ["part-5"],
        "about": "The culmination of the entire Ethics: how the mind achieves freedom through understanding. Spinoza shows that we can transform passive emotions into active ones by forming clear and distinct ideas of them — a process remarkably similar to modern cognitive therapy. The highest form of knowledge is the 'intellectual love of God' (amor Dei intellectualis), in which the mind understands itself and all things as part of the eternal, infinite substance. 'Blessedness is not the reward of virtue, but virtue itself.'",
        "for_readers": "Part V is the shortest but most exalted section. Spinoza's prescription for freedom — understanding our emotions transforms them — anticipates both Freud and mindfulness practice. The final propositions on the intellectual love of God are among the most beautiful passages in philosophy. The very last proposition ('Blessedness is not the reward of virtue, but virtue itself') is Spinoza's ultimate message.",
    },
    {
        "id": "theme-geometric-method",
        "name": "The Geometric Method",
        "parts": ["part-1", "part-2", "part-3", "part-4", "part-5"],
        "about": "Spinoza wrote the Ethics in the manner of Euclid's Elements: definitions, axioms, propositions, proofs, corollaries, and scholia. This is not mere affectation — the geometric method embodies Spinoza's conviction that reality itself has a logical structure that can be grasped by reason. Each proposition follows necessarily from what precedes it, mirroring the necessary order of nature itself. Understanding WHY Spinoza chose this form is essential to understanding the work.",
        "for_readers": "Do not be intimidated by the geometric form. The definitions set up Spinoza's vocabulary. The axioms state what he takes as self-evident. The propositions are his claims, and the proofs show how they follow. But the richest philosophical content often appears in the Notes (Scholia) and Appendices, where Spinoza writes in his own voice and addresses objections. Read the scholia first if the proofs seem impenetrable.",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = strip_front_matter(text)

    parts = parse_parts(text)
    print(f"Parsed {len(parts)} parts")

    items = []
    sort_order = 0

    # L1: Individual parts
    for part in parts:
        sort_order += 1
        first_para = extract_first_paragraph(part['text'])
        keywords = PART_KEYWORDS.get(part['id'], ["philosophy", "ethics", "spinoza"])

        items.append({
            "id": part['id'],
            "name": part['name'],
            "sort_order": sort_order,
            "level": 1,
            "category": "part",
            "sections": {
                "Text": part['text'],
            },
            "keywords": keywords,
            "metadata": {
                "part_number": part['part_num'],
                "subtitle": part['subtitle'],
            }
        })
        print(f"  Part {part['part_num']}: {part['name']} ({len(part['text'])} chars)")

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
            "composite_of": theme["parts"],
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "part_count": len(theme["parts"]),
            }
        })

    # L3: Meta-categories
    sort_order += 1
    items.append({
        "id": "ethics-complete",
        "name": "Ethics: The Complete System",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "Baruch Spinoza's Ethics (Ethica Ordine Geometrico Demonstrata, published posthumously in 1677) is one of the most ambitious works in the history of philosophy. Written in geometric form — definitions, axioms, propositions, proofs — it attempts to derive the entire nature of reality, mind, emotion, and human freedom from a single starting point: the concept of substance. Spinoza's God is not a personal creator but Nature itself (Deus sive Natura), and his ethics are not commandments but a natural science of human flourishing. The work moves from metaphysics (Part I) through philosophy of mind (Part II), psychology of emotions (Part III), analysis of human bondage (Part IV), to the liberation of the understanding (Part V). Its influence runs through Hegel, Marx, Freud, Einstein, Deleuze, and contemporary neuroscience.",
            "For Readers": "The Ethics rewards patient, sequential reading — each part builds on what precedes it. But if you want to taste the work before committing, try the Appendix to Part I (Spinoza's devastating critique of teleology and superstition), the Scholia in Part III (his psychology of emotions), or the Appendix to Part IV (his practical ethics). Spinoza is often called the 'God-intoxicated philosopher' and the 'prince of philosophers.' Both titles are earned in this single, extraordinary book.",
        },
        "keywords": ["spinoza", "ethics", "substance", "God", "nature", "freedom", "geometric-method", "rationalism", "monism"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Baruch Spinoza",
                    "date": "1677",
                    "note": "Author"
                },
                {
                    "name": "R. H. M. Elwes",
                    "date": "1883",
                    "note": "Translator"
                }
            ]
        },
        "name": "Ethics",
        "description": "Baruch Spinoza's Ethics (Ethica Ordine Geometrico Demonstrata, 1677) — one of the most radical and rigorous works in the history of philosophy. Written in geometric form (definitions, axioms, propositions, proofs), it builds a complete system from the concept of substance through mind-body parallelism, a natural science of the emotions, and an analysis of human bondage, culminating in a vision of intellectual freedom and blessedness. Spinoza's God is not a personal creator but Nature itself: 'Deus sive Natura.' Translated by R. H. M. Elwes (1883).\n\nSource: Project Gutenberg eBook #3800 (https://www.gutenberg.org/ebooks/3800)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Portraits of Spinoza, including the famous painting attributed to Baruch Spinoza (c. 1665). Engravings from early editions of the Opera Posthuma (1677). Images of Spinoza's lens-grinding tools and the Spinoza House in The Hague.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "metaphysics", "ethics", "rationalism", "monism", "emotions", "freedom", "public-domain", "full-text"],
        "roots": ["western-philosophy"],
        "shelves": ["mirror"],
        "lineages": ["Akomolafe", "Shrei"],
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
    print(f"  L1: {l1} parts, L2: {l2} themes, L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
