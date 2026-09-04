#!/usr/bin/env python3
"""
Build grammar.json for Walden by Henry David Thoreau.

Source: Project Gutenberg eBook #205
Author: Henry David Thoreau (1854)

Structure:
- L1: 18 chapters (Economy through Conclusion)
- L2: Thematic groupings (6 themes)
- L3: Meta-categories (The Complete Work, Thematic Arcs)

Note: The Gutenberg #205 file contains both Walden and Civil Disobedience.
We extract only Walden.
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "walden.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "walden"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Walden's 18 chapters in order
CHAPTERS = [
    "Economy",
    "Where I Lived, and What I Lived For",
    "Reading",
    "Sounds",
    "Solitude",
    "Visitors",
    "The Bean-Field",
    "The Village",
    "The Ponds",
    "Baker Farm",
    "Higher Laws",
    "Brute Neighbors",
    "House-Warming",
    "Former Inhabitants and Winter Visitors",
    "Winter Animals",
    "The Pond in Winter",
    "Spring",
    "Conclusion",
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


def extract_walden_only(text):
    """Extract only Walden, excluding Civil Disobedience which follows.

    The Gutenberg #205 file contains both Walden and Civil Disobedience.
    The title 'ON THE DUTY OF CIVIL DISOBEDIENCE' appears twice:
    once in the TOC near the top, and once as the actual section heading.
    We want to cut at the LAST occurrence.
    """
    marker = "ON THE DUTY OF CIVIL DISOBEDIENCE"
    idx = text.rfind(marker)
    if idx > 0:
        text = text[:idx]
    # Also trim "THE END" if present
    end_marker = "THE END"
    idx = text.rfind(end_marker)
    if idx > len(text) - 200:  # only if near the end
        text = text[:idx]
    return text.strip()


def strip_front_matter(text):
    """Remove title page, contents, and epigraph before Economy.

    The TOC has ' Economy' (with leading space), but the actual
    chapter heading is 'Economy' flush left on its own line.
    We need the second occurrence — the actual chapter start.
    """
    # Find lines that are exactly "Economy" (no leading whitespace)
    # Use regex to match the actual chapter heading
    match = re.search(r'(?:^|\n)(Economy)\n', text)
    if match:
        # Skip the TOC occurrence (has leading space in TOC)
        # Find the occurrence that starts at column 0
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line == "Economy":
                # Verify this is the chapter heading (not the TOC entry)
                # TOC entries have leading spaces
                return '\n'.join(lines[i:])
    return text


def parse_chapters(text):
    """Parse Walden into its 18 chapters."""
    chapters = []

    for i, chapter_name in enumerate(CHAPTERS):
        # Find the chapter heading
        # Chapter names appear on their own line
        pattern = re.escape(chapter_name)
        match = re.search(r'^' + pattern + r'\s*$', text, re.MULTILINE)
        if not match:
            print(f"WARNING: Could not find chapter '{chapter_name}'")
            continue

        start = match.end()

        # Find the start of the next chapter (or end of text)
        if i + 1 < len(CHAPTERS):
            next_pattern = re.escape(CHAPTERS[i + 1])
            next_match = re.search(r'^' + next_pattern + r'\s*$', text[start:], re.MULTILINE)
            if next_match:
                end = start + next_match.start()
            else:
                end = len(text)
        else:
            end = len(text)

        chapter_text = text[start:end].strip()

        # Clean up: normalize whitespace
        chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)

        chapters.append({
            'name': chapter_name,
            'text': chapter_text,
            'chapter_num': i + 1,
        })

    return chapters


def make_id(name):
    """Create a hyphenated ID from a chapter name."""
    clean = name.lower()
    clean = re.sub(r'[^a-z0-9\s-]', '', clean)
    clean = re.sub(r'\s+', '-', clean.strip())
    clean = re.sub(r'-+', '-', clean)
    return clean


def extract_first_sentence(text, max_len=120):
    """Extract the first sentence for a summary."""
    clean = ' '.join(text.split())
    # Remove italic markers
    clean = re.sub(r'_([^_]+)_', r'\1', clean)
    m = re.search(r'[.!?]["\u201d]?\s', clean)
    if m and m.end() <= max_len:
        return clean[:m.end()].strip()
    if len(clean) > max_len:
        truncated = clean[:max_len]
        last_space = truncated.rfind(' ')
        if last_space > max_len // 2:
            return truncated[:last_space] + "..."
        return truncated[:max_len - 3] + "..."
    return clean


# Chapter keywords
CHAPTER_KEYWORDS = {
    "economy": ["simplicity", "economy", "shelter", "food", "clothing", "labor", "cost"],
    "where-i-lived-and-what-i-lived-for": ["morning", "awareness", "time", "purpose", "deliberate-living"],
    "reading": ["books", "classics", "education", "language", "wisdom"],
    "sounds": ["nature", "trains", "birds", "listening", "wildness"],
    "solitude": ["solitude", "nature", "companionship", "self-reliance", "visitors"],
    "visitors": ["society", "conversation", "hospitality", "hermit", "poet"],
    "the-bean-field": ["agriculture", "labor", "beans", "farming", "husbandry"],
    "the-village": ["society", "gossip", "news", "walking", "night"],
    "the-ponds": ["water", "purity", "depth", "Walden-Pond", "nature"],
    "baker-farm": ["poverty", "fishing", "Irish", "simplicity", "labor"],
    "higher-laws": ["hunting", "vegetarianism", "purity", "instinct", "wildness"],
    "brute-neighbors": ["animals", "loon", "ants", "observation", "nature"],
    "house-warming": ["fire", "winter", "chimney", "warmth", "shelter"],
    "former-inhabitants-and-winter-visitors": ["history", "hermits", "poverty", "memory", "visitors"],
    "winter-animals": ["animals", "winter", "owls", "foxes", "ice"],
    "the-pond-in-winter": ["ice", "depth", "measurement", "fishing", "winter"],
    "spring": ["thawing", "rebirth", "mud", "birds", "renewal"],
    "conclusion": ["travel", "exploration", "self-discovery", "morning", "awakening"],
}


# Thematic groupings for L2
THEMES = [
    {
        "id": "theme-economy-simplicity",
        "name": "Economy and Simplicity",
        "chapters": ["economy", "the-bean-field", "baker-farm", "house-warming"],
        "about": "Thoreau's radical experiment in economic reduction. What does a human actually need? He strips life to its essentials — shelter, food, fuel, clothing — and finds that the cost of a thing is 'the amount of what I will call life which is required to be exchanged for it.' These chapters are a manual for voluntary simplicity, written with meticulous accounting and fierce wit.",
        "for_readers": "Start with Economy — Thoreau's longest and most famous chapter. It reads like an anti-capitalist manifesto disguised as household accounts. The Bean-Field and Baker Farm apply the same clear-eyed economics to farming and labor. House-Warming shows how little warmth actually costs.",
    },
    {
        "id": "theme-nature-observation",
        "name": "Nature and Close Observation",
        "chapters": ["sounds", "the-ponds", "brute-neighbors", "winter-animals", "the-pond-in-winter"],
        "about": "Thoreau as naturalist — patient, precise, lyrical. He measures the depth of Walden Pond, watches a battle between red and black ants, tracks a loon across the water, listens to owls and foxes in winter darkness. These chapters are ecological writing before ecology existed, attention so deep it becomes a form of prayer.",
        "for_readers": "The Ponds contains Thoreau's most beautiful prose — his description of Walden's water is luminous. Brute Neighbors is surprisingly dramatic (the ant battle is unforgettable). The Pond in Winter shows Thoreau as empirical scientist, plumbing the pond's depths with a line and lead.",
    },
    {
        "id": "theme-solitude-society",
        "name": "Solitude and Society",
        "chapters": ["solitude", "visitors", "the-village", "former-inhabitants-and-winter-visitors"],
        "about": "The tension at Walden's heart: Thoreau went to the woods to be alone, but he was never truly a hermit. He walked to Concord village regularly, entertained visitors in his cabin, and treasured certain companions. These chapters explore the balance between withdrawal and engagement, silence and conversation.",
        "for_readers": "Solitude is Thoreau's most meditative chapter — on being alone without loneliness. Visitors provides the counterpoint: the value of the right kind of company. Former Inhabitants and Winter Visitors haunts — Thoreau finds himself among ghosts of earlier hermits and outcasts who lived in the same woods.",
    },
    {
        "id": "theme-higher-life",
        "name": "Higher Laws and Awakening",
        "chapters": ["where-i-lived-and-what-i-lived-for", "reading", "higher-laws"],
        "about": "Thoreau's spiritual and intellectual vision. 'I went to the woods because I wished to live deliberately, to front only the essential facts of life.' These chapters articulate what the experiment is for — not just simpler living, but deeper living. Reading great books, pursuing purity, waking up to the morning of existence.",
        "for_readers": "Where I Lived contains the most quoted passages in Walden — 'I wanted to live deep and suck out all the marrow of life.' Reading is Thoreau's passionate defense of the classics. Higher Laws is his most controversial chapter, wrestling with vegetarianism, wildness, and the body's animal appetites.",
    },
    {
        "id": "theme-seasons-renewal",
        "name": "Seasons and Renewal",
        "chapters": ["spring", "conclusion"],
        "about": "Walden's magnificent closing arc. After winter's long stillness, spring arrives like resurrection — the ice cracks, the thawing sand flows in organic forms, the birds return. And Thoreau draws his conclusion: 'I learned this, at least, by my experiment: that if one advances confidently in the direction of his dreams, and endeavors to live the life which he has imagined, he will meet with a success unexpected in common hours.'",
        "for_readers": "Spring is Thoreau's ecstatic chapter — the thawing sand-bank passage is one of the most original pieces of nature writing ever composed. The Conclusion is surprisingly tender, urging readers not to imitate Thoreau but to find their own Walden. 'If a man does not keep pace with his companions, perhaps it is because he hears a different drummer.'",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = extract_walden_only(text)
    text = strip_front_matter(text)

    chapters = parse_chapters(text)
    print(f"Parsed {len(chapters)} chapters")

    items = []
    sort_order = 0

    # L1: Individual chapters
    for ch in chapters:
        chapter_id = make_id(ch['name'])
        sort_order += 1
        first_sentence = extract_first_sentence(ch['text'])
        keywords = CHAPTER_KEYWORDS.get(chapter_id, ["walden", "nature", "philosophy"])

        items.append({
            "id": chapter_id,
            "name": ch['name'],
            "sort_order": sort_order,
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": ch['text'],
            },
            "keywords": keywords,
            "metadata": {
                "chapter_number": ch['chapter_num'],
            }
        })
        print(f"  Ch {ch['chapter_num']:2d}: {ch['name']} ({len(ch['text'])} chars)")

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

    # L3: Meta-categories
    sort_order += 1
    chapter_ids = [make_id(ch['name']) for ch in chapters]
    items.append({
        "id": "walden-complete",
        "name": "Walden: Life in the Woods",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "Henry David Thoreau's Walden (1854) is the record of two years, two months, and two days spent living in a self-built cabin on the shore of Walden Pond near Concord, Massachusetts. It is at once an experiment in radical simplicity, a work of natural history, a spiritual autobiography, and a critique of American economic life. Thoreau compresses his two years into the cycle of a single year — from summer through winter to spring — making the book itself a meditation on renewal. The 18 chapters move from the practical (building a house, growing beans, keeping warm) to the transcendent (awakening, morning, the meaning of life), with nature observation threading through everything.",
            "For Readers": "Walden rewards both sequential reading and browsing. Read it straight through to feel Thoreau's seasonal arc — the descent into winter solitude and the ecstatic return of spring. Or dip in: Economy for the philosophy of simplicity, Where I Lived for the famous manifesto, The Ponds for pure nature writing, Conclusion for the parting wisdom. Thoreau is funnier and more practical than his reputation suggests. He is also more radical.",
        },
        "keywords": ["walden", "thoreau", "nature", "simplicity", "transcendentalism"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Henry David Thoreau",
                    "date": "1854",
                    "note": "Author"
                }
            ]
        },
        "name": "Walden",
        "description": "Henry David Thoreau's Walden (1854) — the foundational text of American nature writing and voluntary simplicity. A record of two years spent living in a self-built cabin on the shore of Walden Pond near Concord, Massachusetts. Thoreau distills his experiment into 18 chapters that move from the economics of shelter and food through deep nature observation to spiritual awakening. 'I went to the woods because I wished to live deliberately, to front only the essential facts of life.'\n\nSource: Project Gutenberg eBook #205 (https://www.gutenberg.org/ebooks/205)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Illustrations from the first edition of Walden (Ticknor and Fields, 1854) including Thoreau's own survey map of Walden Pond. Daguerreotypes of Thoreau (1856). Photographs of Walden Pond and Concord landscapes. Herbert Wendell Gleason's photographs of Thoreau country (early 1900s).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["nature", "philosophy", "simplicity", "transcendentalism", "ecology", "public-domain", "full-text"],
        "roots": ["ecology-nature"],
        "shelves": ["earth"],
        "lineages": ["Andreotti"],
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
