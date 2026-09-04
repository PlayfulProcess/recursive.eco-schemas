#!/usr/bin/env python3
"""
Parse Tao Te Ching (Legge translation, Gutenberg #216) into a grammar.json.

Structure:
- L1: 81 individual chapters (verses)
- L2: Thematic groupings + Part 1 (Tao) / Part 2 (Te) divisions
- L3: The two books (Tao / Te)
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "tao-te-ching.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "tao-te-ching")
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


def parse_chapters(text):
    """Parse 81 chapters from the Legge translation.

    The format has two patterns:
    - "Ch. 1. 1. The Tao that can be..." (chapter with "Ch." prefix, only ch 1)
    - "2. 1. All in the world know..." (chapter as bare number + subsection)
    - "6.\\n\\n   The valley spirit..." (chapter as bare number on its own line)

    Key insight: chapters appear sequentially 1-81, so we search for
    each expected number in order, distinguishing chapter starts from
    subsection numbers by requiring a preceding blank line.
    """
    lines = text.split('\n')

    # Find the start of the text (after header)
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('Ch. 1.'):
            start_idx = i
            break

    # Build a map of line positions for each potential chapter start
    # A chapter start is: blank line(s) before, then "N." or "Ch. N." at line start
    chapter_starts = {}  # chapter_num -> line_index

    # Search sequentially for chapters 1-81
    next_expected = 1
    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        # Check for "PART 2." header — skip it
        if line.startswith('PART'):
            continue

        # Check if this line starts a chapter
        # Pattern 1: "Ch. N. ..." (only ch 1)
        # Pattern 2: "N. 1. ..." (chapter with first subsection)
        # Pattern 3: "N." alone on a line (chapter with verse following)
        # Pattern 4: "N. text..." (chapter with direct text, no subsection number)
        m = re.match(r'^(?:Ch\. )?(\d+)\.\s*(.*)', line)
        if not m:
            continue

        num = int(m.group(1))
        rest = m.group(2).strip()

        if num != next_expected:
            continue

        # Verify there's a blank line before this (except for ch 1)
        if num > 1:
            has_blank_before = False
            for j in range(i - 1, max(i - 3, -1), -1):
                if not lines[j].strip():
                    has_blank_before = True
                    break
            if not has_blank_before:
                continue

        chapter_starts[num] = i
        next_expected = num + 1
        if next_expected > 81:
            break

    # Extract chapter texts between boundaries
    sorted_chapters = sorted(chapter_starts.items())
    chapters = []

    for idx, (num, line_idx) in enumerate(sorted_chapters):
        # End boundary: next chapter start or end of text
        if idx + 1 < len(sorted_chapters):
            end_idx = sorted_chapters[idx + 1][1]
        else:
            # Find end of Gutenberg text
            end_idx = len(lines)
            for i in range(line_idx, len(lines)):
                if '*** END OF THE PROJECT GUTENBERG' in lines[i]:
                    end_idx = i
                    break

        ch_text = '\n'.join(lines[line_idx:end_idx]).strip()

        # Remove the chapter number prefix "Ch. N." or "N."
        ch_text = re.sub(r'^(?:Ch\. )?\d+\.\s*', '', ch_text)

        # Clean up excessive whitespace
        ch_text = re.sub(r'\n{3,}', '\n\n', ch_text)
        ch_text = ch_text.strip()

        chapters.append({
            "number": num,
            "text": ch_text,
            "part": 1 if num <= 37 else 2,
        })

    return chapters


# Thematic groupings for L2 emergence
THEMES = [
    {
        "id": "theme-nature-of-tao",
        "name": "The Nature of Tao",
        "chapters": [1, 4, 6, 14, 21, 25, 34, 40, 42, 51],
        "about": "What is the Tao? These chapters circle the ineffable source — nameless, formless, prior to heaven and earth. The Tao that can be spoken is not the eternal Tao, yet Lao Tzu speaks anyway, using paradox, metaphor, and negation to point at what cannot be grasped.",
        "for_readers": "Read these when you want to sit with mystery. Don't try to understand them — let them work on you like water on stone."
    },
    {
        "id": "theme-wu-wei",
        "name": "Wu Wei — Non-Action",
        "chapters": [2, 3, 10, 29, 37, 43, 47, 48, 57, 63, 64],
        "about": "Wu wei (non-action, non-forcing) is the Tao's primary teaching on how to live. Not passivity but effortless action — doing by not-doing, leading by following, accomplishing by letting go.",
        "for_readers": "The antidote to burnout, control, and striving. Linehan's radical acceptance and Akomolafe's 'slowing down' both grow from this root."
    },
    {
        "id": "theme-water-and-softness",
        "name": "Water and Softness",
        "chapters": [8, 22, 36, 43, 76, 78],
        "about": "Water is Lao Tzu's central metaphor: soft, yielding, seeking the low places — yet nothing is stronger. The soft overcomes the hard. The weak overcomes the strong. The low becomes full.",
        "for_readers": "For moments when you feel powerless. These verses redefine strength itself."
    },
    {
        "id": "theme-sage-ruler",
        "name": "The Sage as Ruler",
        "chapters": [3, 5, 17, 18, 19, 29, 30, 31, 57, 58, 59, 60, 61, 65, 66, 72, 73, 74, 75, 80],
        "about": "Lao Tzu's political philosophy: the best ruler is barely noticed. Govern by not-governing. Reduce laws, reduce desires, reduce interference. The sage-ruler leads by emptying, not filling.",
        "for_readers": "Radical governance philosophy — relevant to parenting, management, community building. The leader who serves rather than commands."
    },
    {
        "id": "theme-simplicity-return",
        "name": "Simplicity and Return",
        "chapters": [12, 16, 19, 20, 28, 32, 37, 44, 46, 80],
        "about": "Return to the root. Return to simplicity. Return to the uncarved block (pu). Civilization adds, the Tao subtracts. Desire is the trap; contentment is the way home.",
        "for_readers": "For when the world feels too complicated. These chapters are a compass pointing toward enough."
    },
    {
        "id": "theme-paradox-opposition",
        "name": "Paradox and Opposition",
        "chapters": [2, 7, 9, 11, 13, 22, 24, 36, 41, 45, 56, 58, 71, 76, 78, 81],
        "about": "The Tao teaches through reversal: the useful comes from the useless, fullness from emptiness, strength from weakness. Those who know do not speak; those who speak do not know. Every pair of opposites is secretly one.",
        "for_readers": "The dialectical heart of Taoism. Linehan's dialectical behavior therapy inherits this both-and thinking directly."
    },
    {
        "id": "theme-humility-contentment",
        "name": "Humility and Contentment",
        "chapters": [7, 8, 9, 15, 22, 33, 39, 44, 46, 53, 67, 77, 81],
        "about": "The sage puts himself last and so finds himself first. He does not compete and so no one can compete with him. Contentment is the greatest treasure. Know when to stop.",
        "for_readers": "Practical wisdom for daily life. What does it mean to have enough? To stop striving? To find sufficiency in this moment?"
    },
    {
        "id": "theme-mother-feminine",
        "name": "The Mother and the Feminine",
        "chapters": [1, 6, 10, 20, 25, 28, 52, 59, 61],
        "about": "The Tao is the Mother of all things. The valley spirit, the mysterious feminine, the gateway of heaven and earth. Lao Tzu consistently privileges the feminine principle — receptivity, darkness, softness, depth — over the masculine.",
        "for_readers": "A 2,500-year-old feminist metaphysics. The Tao as womb, as source, as the darkness from which light emerges."
    },
]


def build_grammar(chapters):
    items = []
    sort_order = 0

    # L1: Individual chapters
    for ch in chapters:
        sort_order += 1
        # Create a short name from the first line
        first_line = ch["text"].split("\n")[0]
        # Remove subsection number prefix
        first_line = re.sub(r'^1\.\s*', '', first_line)
        # Truncate for display
        if len(first_line) > 80:
            first_line = first_line[:77] + "..."

        items.append({
            "id": f"ch-{ch['number']:02d}",
            "name": f"Chapter {ch['number']}: {first_line}",
            "level": 1,
            "category": "verse",
            "sort_order": sort_order,
            "sections": {
                "Verse": ch["text"]
            },
            "keywords": [],
            "metadata": {
                "chapter_number": ch["number"],
                "part": ch["part"],
                "part_name": "Tao (The Way)" if ch["part"] == 1 else "Te (Virtue/Power)",
            }
        })

    # L2: Thematic groupings
    for theme in THEMES:
        sort_order += 1
        composite = [f"ch-{n:02d}" for n in theme["chapters"]]
        items.append({
            "id": theme["id"],
            "name": theme["name"],
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": composite,
            "sort_order": sort_order,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "chapter_count": len(theme["chapters"]),
                "chapters": theme["chapters"],
            }
        })

    # L2: Part 1 and Part 2
    part1_ids = [f"ch-{n:02d}" for n in range(1, 38)]
    part2_ids = [f"ch-{n:02d}" for n in range(38, 82)]

    sort_order += 1
    items.append({
        "id": "part-1-tao",
        "name": "Part 1: Tao (The Way)",
        "level": 2,
        "category": "part",
        "relationship_type": "emergence",
        "composite_of": part1_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "The first 37 chapters focus on the Tao itself — its nature, its namelessness, its relationship to the ten thousand things. This is the metaphysical foundation: what is the source of reality, and how does it move?",
        },
        "keywords": [],
        "metadata": {"part": 1, "chapter_range": "1-37", "chapter_count": 37}
    })

    sort_order += 1
    items.append({
        "id": "part-2-te",
        "name": "Part 2: Te (Virtue / Power)",
        "level": 2,
        "category": "part",
        "relationship_type": "emergence",
        "composite_of": part2_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "The final 44 chapters shift from metaphysics to application — how the sage lives, governs, and embodies the Tao. Te is often translated as 'virtue' or 'power,' but it means something closer to 'the Tao expressed through a person.' This is praxis.",
        },
        "keywords": [],
        "metadata": {"part": 2, "chapter_range": "38-81", "chapter_count": 44}
    })

    # L3: The Two Books
    sort_order += 1
    items.append({
        "id": "meta-tao-and-te",
        "name": "The Tao and Its Virtue: Source and Expression",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": ["part-1-tao", "part-2-te"],
        "sort_order": sort_order,
        "sections": {
            "About": "The Tao Te Ching is structured as two books: Tao (the nameless source) and Te (its expression through virtue). This mirrors the fundamental movement of reality itself — from the formless to the formed, from silence to speech, from the one to the ten thousand things. The text is a single breath: inhale (Tao) and exhale (Te).",
        },
        "keywords": [],
        "metadata": {}
    })

    sort_order += 1
    items.append({
        "id": "meta-themes",
        "name": "Eight Streams: Thematic Currents in the Tao Te Ching",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": [t["id"] for t in THEMES],
        "sort_order": sort_order,
        "sections": {
            "About": "Eight thematic currents flow through the Tao Te Ching, overlapping and interweaving like streams in a river delta. A single chapter may belong to several currents simultaneously — Chapter 2 is about wu wei AND paradox AND opposition. This multiplicity is not a flaw in the classification but a feature of the text: the Tao does not divide neatly. These groupings are entry points, not enclosures.",
        },
        "keywords": [],
        "metadata": {"theme_count": len(THEMES)}
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    chapters = parse_chapters(text)
    print(f"Parsed {len(chapters)} chapters")

    if len(chapters) != 81:
        print(f"WARNING: Expected 81 chapters, got {len(chapters)}")
        for ch in chapters:
            print(f"  Ch. {ch['number']}: {ch['text'][:60]}...")
        return

    items = build_grammar(chapters)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Lao Tzu", "date": "~6th century BCE", "note": "Traditional author"},
                {"name": "James Legge", "date": "1891", "note": "English translator"},
            ]
        },
        "name": "Tao Te Ching",
        "description": "The Tao Te Ching ('The Classic of the Way and Its Virtue'), attributed to Lao Tzu, is the foundational text of philosophical Taoism. 81 brief chapters on the nameless source of reality, non-action (wu wei), and the paradox of power through yielding. James Legge translation (1891).\n\nSource: Project Gutenberg eBook #216 (https://www.gutenberg.org/ebooks/216)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Traditional Chinese ink wash paintings (sumi-e) of mountains, water, and mist. The Ma Yuan and Xia Gui school of Southern Song landscape painting (12th-13th century) captures the Tao Te Ching's aesthetic perfectly — vast empty space with minimal brushstrokes suggesting mountains emerging from void.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "taoism", "chinese", "sacred-text", "public-domain", "full-text", "wisdom", "non-dual", "wu-wei"],
        "roots": ["eastern-wisdom"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan", "Akomolafe", "Shrei"],
        "worldview": "non-dual",
        "items": items,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"Grammar written to {OUTPUT}")
    print(f"  L1: {l1} chapters, L2: {l2} emergent groups, L3: {l3} meta-categories")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    main()
