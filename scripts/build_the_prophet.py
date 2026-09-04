#!/usr/bin/env python3
"""
Parse The Prophet (Kahlil Gibran, Gutenberg #58585) into grammar.json.

Structure:
- L1: 28 individual sections (The Coming of the Ship, 26 essays, The Farewell)
- L2: Thematic groupings
- L3: Meta-categories
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "the-prophet.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "the-prophet")
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


# The sections of The Prophet in order, with their trigger patterns
SECTIONS = [
    ("the-coming-of-the-ship", "The Coming of the Ship", None),  # Opening narrative
    ("on-love", "On Love", "_Love_"),
    ("on-marriage", "On Marriage", "_Marriage_"),
    ("on-children", "On Children", "_Children_"),
    ("on-giving", "On Giving", "_Giving_"),
    ("on-eating-and-drinking", "On Eating and Drinking", "_Eating and Drinking_"),
    ("on-work", "On Work", "_Work_"),
    ("on-joy-and-sorrow", "On Joy and Sorrow", "_Joy and Sorrow_"),
    ("on-houses", "On Houses", "_Houses_"),
    ("on-clothes", "On Clothes", "_Clothes_"),
    ("on-buying-and-selling", "On Buying and Selling", "_Buying and Selling_"),
    ("on-crime-and-punishment", "On Crime and Punishment", "_Crime and Punishment_"),
    ("on-laws", "On Laws", "_Laws_"),
    ("on-freedom", "On Freedom", "_Freedom_"),
    ("on-reason-and-passion", "On Reason and Passion", "_Reason and Passion_"),
    ("on-pain", "On Pain", "_Pain_"),
    ("on-self-knowledge", "On Self-Knowledge", "_Self-Knowledge_"),
    ("on-teaching", "On Teaching", "_Teaching_"),
    ("on-friendship", "On Friendship", "_Friendship_"),
    ("on-talking", "On Talking", "_Talking_"),
    ("on-time", "On Time", "_Time_"),
    ("on-good-and-evil", "On Good and Evil", "_Good and Evil_"),
    ("on-prayer", "On Prayer", "_Prayer_"),
    ("on-pleasure", "On Pleasure", "_Pleasure_"),
    ("on-beauty", "On Beauty", "_Beauty_"),
    ("on-religion", "On Religion", "_Religion_"),
    ("on-death", "On Death", "_Death_"),
    ("the-farewell", "The Farewell", None),  # Closing narrative
]


def parse_sections(text):
    """Parse the 28 sections of The Prophet."""
    lines = text.split('\n')

    # Find where the actual text begins (after front matter)
    # Look for "THE PROPHET" followed by "Almustafa"
    text_start = 0
    for i, line in enumerate(lines):
        if 'Almustafa, the chosen and the' in line:
            text_start = i
            break

    # Find the section boundaries by looking for the topic markers
    # Each topic is introduced with "Speak to us of _Topic_" or similar
    section_starts = []

    # The Coming of the Ship starts at text_start
    section_starts.append((0, text_start))  # index into SECTIONS, line number

    # Find each topic section
    # Join consecutive lines for trigger matching (some triggers span two lines)
    for i in range(text_start, len(lines)):
        line = lines[i]
        # Also check the combined current+next line for multi-line triggers
        combined = line
        if i + 1 < len(lines):
            combined = line + ' ' + lines[i + 1]
        for sec_idx, (sec_id, sec_name, trigger) in enumerate(SECTIONS):
            if trigger and (trigger in line or trigger in combined):
                # Avoid duplicate matches
                if not any(s[0] == sec_idx for s in section_starts):
                    section_starts.append((sec_idx, i))
                break

    # Find The Farewell - starts with "And now it was evening."
    for i in range(text_start, len(lines)):
        if 'And now it was evening.' in lines[i]:
            section_starts.append((27, i))  # The Farewell
            break

    # Sort by line number
    section_starts.sort(key=lambda x: x[1])

    # Extract content for each section
    parsed = []
    for idx, (sec_idx, start_line) in enumerate(section_starts):
        # End boundary
        if idx + 1 < len(section_starts):
            end_line = section_starts[idx + 1][1]
        else:
            end_line = len(lines)

        raw_content = '\n'.join(lines[start_line:end_line])

        # Clean up
        # Remove illustration markers
        raw_content = re.sub(r'\[Illustration:.*?\]', '', raw_content)
        # Remove ***** dividers
        raw_content = re.sub(r'\*{3,}\s*\*{0,}', '', raw_content)
        # Remove the "Speak to us of _Topic_" prompt lines for essay sections
        # but keep the actual teaching
        # Normalize whitespace
        raw_content = re.sub(r'\n{3,}', '\n\n', raw_content)
        raw_content = raw_content.strip()

        sec_id, sec_name, trigger = SECTIONS[sec_idx]
        parsed.append({
            "id": sec_id,
            "name": sec_name,
            "content": raw_content,
            "section_index": sec_idx,
        })

    return parsed


# Thematic groupings
THEMES = [
    {
        "id": "theme-love-relationships",
        "name": "Love and Human Bonds",
        "sections": ["on-love", "on-marriage", "on-children", "on-friendship"],
        "about": "Gibran's teaching on love is paradoxical: love binds by setting free. Marriage requires spaces in togetherness. Children belong not to their parents but to Life itself. Friendship is found in shared silence, not shared words. These four essays form the emotional core of the book.",
        "for_readers": "For anyone navigating relationships. Gibran's counsel on marriage — 'let there be spaces in your togetherness' — remains among the most quoted passages in wedding ceremonies worldwide. His words on children have consoled and challenged parents for a century."
    },
    {
        "id": "theme-inner-life",
        "name": "The Inner Landscape",
        "sections": ["on-joy-and-sorrow", "on-pain", "on-self-knowledge", "on-reason-and-passion", "on-good-and-evil"],
        "about": "The territory of the soul: joy and sorrow as inseparable, pain as the breaking of understanding's shell, self-knowledge as infinite depth. Gibran dissolves the boundary between good and evil, reason and passion — not into moral relativism but into a vision of wholeness.",
        "for_readers": "For moments of inner conflict. Gibran teaches that your joy and your sorrow are not enemies but the same cup, measured by the same depth. Deeply resonant with Linehan's dialectical thinking."
    },
    {
        "id": "theme-daily-life",
        "name": "The Sacred in Daily Life",
        "sections": ["on-eating-and-drinking", "on-work", "on-houses", "on-clothes", "on-buying-and-selling"],
        "about": "Gibran sacralizes the mundane: eating is communion, work is love made visible, houses should not become anchors, clothes should not hide the beauty of the body. The marketplace itself can be a temple if approached with reverence.",
        "for_readers": "For finding meaning in ordinary activities. These essays transform cooking, working, shopping, and homemaking into spiritual practices."
    },
    {
        "id": "theme-society-freedom",
        "name": "Society, Law, and Freedom",
        "sections": ["on-crime-and-punishment", "on-laws", "on-freedom", "on-talking", "on-giving"],
        "about": "Gibran's social philosophy: the criminal is not separate from the righteous, law should be a garment willingly worn not a chain, freedom is found not in overthrowing but in transcending. Even giving must be given freely — not from duty but from the joy of giving itself.",
        "for_readers": "A vision of justice rooted in compassion rather than punishment. These essays challenge retributive thinking and reimagine what it means to live together."
    },
    {
        "id": "theme-transcendence",
        "name": "The Eternal and the Beyond",
        "sections": ["on-time", "on-prayer", "on-religion", "on-death", "on-beauty", "on-pleasure"],
        "about": "The mystical summit of Gibran's vision: time as a river, prayer as expanding into the living ether, religion as all acts and all reflections, death as standing naked in the wind. Beauty is eternity gazing at itself in a mirror. Pleasure is a freedom song — not a bondage.",
        "for_readers": "For questions about mortality, meaning, and the sacred. Gibran offers a non-dogmatic mysticism that honors all paths while pointing beyond all of them."
    },
    {
        "id": "theme-narrative-frame",
        "name": "The Story of Almustafa",
        "sections": ["the-coming-of-the-ship", "the-farewell"],
        "about": "The narrative frame: Almustafa has lived twelve years in the city of Orphalese. His ship returns to take him home. In the hours before departure, the people ask him to speak. After his teachings, he boards the ship and sails into the mist. The frame is itself a teaching — all wisdom is spoken in the hour of parting.",
        "for_readers": "The opening and closing are often overlooked but they hold the key: every teaching Almustafa gives is colored by departure. Wisdom arrives at the threshold of loss."
    },
]


def build_grammar(sections):
    items = []
    sort_order = 0

    # L1: Individual sections
    for sec in sections:
        sort_order += 1
        section_key = "Poem" if sec["id"] in ("the-coming-of-the-ship", "the-farewell") else "Verse"
        items.append({
            "id": sec["id"],
            "name": sec["name"],
            "level": 1,
            "category": "essay",
            "sort_order": sort_order,
            "sections": {
                section_key: sec["content"]
            },
            "keywords": [],
            "metadata": {
                "section_number": sec["section_index"] + 1,
            }
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
            "composite_of": theme["sections"],
            "sort_order": sort_order,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {"essay_count": len(theme["sections"])}
        })

    # L3: Meta-categories
    sort_order += 1
    items.append({
        "id": "meta-teachings",
        "name": "The Teachings of Almustafa: Five Dimensions of Wisdom",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": [t["id"] for t in THEMES if t["id"] != "theme-narrative-frame"],
        "sort_order": sort_order,
        "sections": {
            "About": "The Prophet's twenty-six essays weave together into five dimensions: the bonds of love, the depths of the inner life, the holiness of daily existence, the question of how to live together, and the mystery of the eternal. These dimensions do not compete but interpenetrate — work is love, love is freedom, freedom is prayer, prayer is death, death is life. The book is a single vision refracted through twenty-six facets.",
        },
        "keywords": [],
        "metadata": {}
    })

    sort_order += 1
    items.append({
        "id": "meta-complete-work",
        "name": "The Prophet: Departure as Revelation",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": ["theme-narrative-frame", "meta-teachings"],
        "sort_order": sort_order,
        "sections": {
            "About": "The Prophet is a single gesture: a man leaving a city he has loved for twelve years, pouring out his wisdom in the hour of departure. The narrative frame is not decoration — it is the deepest teaching. All of Almustafa's words are spoken on the threshold, between presence and absence, between the known and the unknown. This is why the book resonates: we are all always departing, always on the edge of the ship, always speaking our truest words in the moment before silence.",
        },
        "keywords": [],
        "metadata": {}
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    sections = parse_sections(text)
    print(f"Parsed {len(sections)} sections")

    for sec in sections:
        preview = sec["content"][:60].replace('\n', ' ')
        print(f"  {sec['name']}: {preview}...")

    items = build_grammar(sections)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Kahlil Gibran", "date": "1923", "note": "Author"},
            ]
        },
        "name": "The Prophet",
        "description": "The Prophet by Kahlil Gibran (1923) is a collection of 26 poetic essays spoken by the sage Almustafa to the people of Orphalese on the day of his departure. Topics range from Love and Marriage to Death and Freedom. One of the most translated books in history, it offers a non-sectarian mystical vision of human life in all its dimensions.\n\nSource: Project Gutenberg eBook #58585 (https://www.gutenberg.org/ebooks/58585)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Gibran's own twelve original drawings accompany the text — ethereal charcoal and wash figures in his distinctive symbolist style, influenced by William Blake and Auguste Rodin. These drawings are integral to the work and are in the public domain.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["poetry", "mysticism", "philosophy", "sacred-text", "public-domain", "full-text", "contemplative", "non-dual", "Lebanese"],
        "roots": ["mysticism", "eastern-wisdom"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan", "Shrei"],
        "worldview": "non-dual",
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
