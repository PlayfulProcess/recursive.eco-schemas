#!/usr/bin/env python3
"""
Parser for The Book of Tea by Kakuzo Okakura (Gutenberg #769).

Parses 7 essay-chapters into a grammar.json with:
  L1: Individual chapters (essays on tea, aesthetics, Zen, art)
  L2: Thematic groupings (Philosophy & Spirit, History & Practice, Art & Beauty)
  L3: Meta-categories (The Way of Tea)
"""

import json
import re
import sys
from pathlib import Path

SEEDS_DIR = Path(__file__).parent.parent / "seeds"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "book-of-tea"

CHAPTER_TITLES = {
    1: "The Cup of Humanity",
    2: "The Schools of Tea",
    3: "Taoism and Zennism",
    4: "The Tea-Room",
    5: "Art Appreciation",
    6: "Flowers",
    7: "Tea-Masters",
}

CHAPTER_KEYWORDS = {
    1: ["tea", "humanity", "aesthetics", "Teaism", "East", "West", "beauty", "imperfection", "civilisation"],
    2: ["history", "tea", "Bodhidharma", "Lu Wu", "whipped tea", "steeped tea", "Sung", "Tang", "Ming"],
    3: ["Taoism", "Zen", "Laotse", "Zhuangzi", "emptiness", "relativity", "non-dual", "vacuum", "spirit"],
    4: ["tea-room", "sukiya", "architecture", "simplicity", "emptiness", "tokonoma", "asymmetry", "wabi"],
    5: ["art", "appreciation", "beauty", "master", "connoisseur", "sympathy", "spirit", "mutual understanding"],
    6: ["flowers", "ikebana", "flower arrangement", "nature", "sacrifice", "beauty", "offering"],
    7: ["tea-masters", "Rikiu", "aesthetics", "refinement", "life", "death", "art of living", "Zen"],
}


def read_seed():
    """Read the seed file and strip Gutenberg header/footer."""
    path = SEEDS_DIR / "book-of-tea.txt"
    text = path.read_text(encoding="utf-8")

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE BOOK OF TEA ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE BOOK OF TEA ***"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def strip_front_matter(text):
    """Remove production note and title before the first chapter."""
    # The first chapter starts with "I. The Cup of Humanity"
    match = re.search(r'\nI\. The Cup of Humanity\s*\n', text)
    if match:
        text = text[match.start():]
    return text


def parse_chapters(text):
    """Parse text into chapters using Roman numeral + title headers."""
    chapters = {}

    # Find chapter boundaries using the pattern "I. Title" through "VII. Title"
    roman_titles = {
        'I': 1, 'II': 2, 'III': 3, 'IV': 4,
        'V': 5, 'VI': 6, 'VII': 7,
    }

    # Find all chapter starts
    chapter_starts = []
    for match in re.finditer(r'^(I{1,3}|IV|VI{0,2}|VII)\.\s+(.+?)\.?\s*$', text, re.MULTILINE):
        roman = match.group(1)
        if roman in roman_titles:
            num = roman_titles[roman]
            chapter_starts.append((num, match.start(), match.group(0).strip()))

    # Deduplicate: keep the one whose title matches expected
    seen_nums = {}
    for num, pos, full in chapter_starts:
        if num not in seen_nums:
            seen_nums[num] = (pos, full)
        # Keep the first occurrence (should be the actual chapter header)

    sorted_chapters = sorted(seen_nums.items())

    for idx, (num, (start_pos, header)) in enumerate(sorted_chapters):
        if idx + 1 < len(sorted_chapters):
            end_pos = sorted_chapters[idx + 1][1][0]
        else:
            end_pos = len(text)

        chapter_text = text[start_pos:end_pos].strip()
        chapters[num] = chapter_text

    return chapters


def clean_chapter_text(text, chapter_num):
    """Remove the chapter header line, leaving only the essay body."""
    lines = text.split('\n')

    # Skip the header line and any following blank lines
    content_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        # Skip the chapter header line (e.g., "I. The Cup of Humanity")
        if re.match(r'^(I{1,3}|IV|VI{0,2}|VII)\.\s+', stripped):
            content_start = i + 1
            continue
        break

    content_lines = lines[content_start:]

    result = '\n'.join(content_lines).strip()

    # Clean up excessive blank lines
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result


def build_chapter_sections(chapter_num, text):
    """Build sections for a chapter item."""
    sections = {}

    cleaned = clean_chapter_text(text, chapter_num)
    sections["Essay"] = cleaned

    # Extract a notable passage (the opening paragraph) as a "Key Passage"
    paragraphs = [p.strip() for p in cleaned.split('\n\n') if p.strip()]
    if paragraphs:
        sections["Opening"] = paragraphs[0]

    # Add reflections specific to each chapter
    reflections = {
        1: "Okakura begins with tea as a meeting point between East and West. Where in your own life do you find the 'religion of aestheticism' -- the worship of the beautiful among the sordid facts of everyday existence?",
        2: "Three schools of tea mirror three philosophies of life: the boiled tea of the Classic, the whipped tea of the Romantic, the steeped tea of the Naturalistic. Which school speaks to your temperament?",
        3: "Taoism and Zen share the love of the relative over the absolute, the incomplete over the complete. 'In the art of life the important thing is the beginning,' says Laotse. What does it mean to value emptiness and incompletion?",
        4: "The tea-room is an empty space that the guest fills with imagination. Sukiya means 'the abode of fancy,' 'the abode of vacancy,' 'the abode of the unsymmetrical.' What kind of space invites the most presence?",
        5: "Art appreciation requires a meeting between the giver and receiver. The masterpiece is a symphony played upon our finest feelings. How do you prepare yourself to receive beauty?",
        6: "The flower arrangement is a meditation on sacrifice and transience. 'In joy or sadness, flowers are our constant friends.' What is your relationship with the living beauty around you?",
        7: "The last tea of Rikiu: a ceremony of exquisite refinement even unto death. 'He only who has lived with the beautiful can die beautifully.' What does it mean to make your whole life an aesthetic act?",
    }
    sections["Reflection"] = reflections.get(chapter_num, "Sit with this essay. What speaks to you?")

    return sections


def make_chapter_id(chapter_num):
    """Create a hyphenated ID for a chapter."""
    title = CHAPTER_TITLES.get(chapter_num, f"Chapter {chapter_num}")
    slug = title.lower()
    slug = re.sub(r"[''']s\b", "s", slug)
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return f"ch{chapter_num}-{slug}"


def build_l1_items(chapters):
    """Build L1 items from parsed chapters."""
    items = []

    for chapter_num in sorted(chapters.keys()):
        raw_text = chapters[chapter_num]
        sections = build_chapter_sections(chapter_num, raw_text)

        item = {
            "id": make_chapter_id(chapter_num),
            "name": CHAPTER_TITLES.get(chapter_num, f"Chapter {chapter_num}"),
            "sort_order": chapter_num - 1,
            "category": "chapter",
            "level": 1,
            "sections": sections,
            "keywords": CHAPTER_KEYWORDS.get(chapter_num, []),
            "metadata": {
                "chapter_number": chapter_num,
            },
        }
        items.append(item)

    return items


L2_GROUPS = {
    "philosophy-and-spirit": {
        "name": "Philosophy and Spirit",
        "category": "theme",
        "chapters": [1, 3],
        "about": "The philosophical foundations of Teaism. Chapter 1 introduces tea as a bridge between civilizations and a 'religion of aestheticism' -- the worship of the Imperfect. Chapter 3 traces the Taoist and Zen roots that give the tea ceremony its spiritual depth: the love of emptiness, the embrace of relativity, the art of being in the world without being captured by it.",
        "keywords": ["philosophy", "Taoism", "Zen", "aesthetics", "East-West", "spirituality"],
    },
    "history-and-practice": {
        "name": "History and Practice",
        "category": "theme",
        "chapters": [2, 4, 7],
        "about": "The evolution of tea from medicine to beverage to spiritual practice, the architecture of the tea-room (sukiya), and the lives of the great tea-masters who made their entire existence an art form. From Lu Wu's 'Tea Classic' through the Sung dynasty's whipped tea to the quiet rooms of Rikiu, where simplicity became the highest refinement.",
        "keywords": ["history", "tea-room", "tea-masters", "Rikiu", "practice", "architecture", "sukiya"],
    },
    "art-and-beauty": {
        "name": "Art and Beauty",
        "category": "theme",
        "chapters": [5, 6],
        "about": "Okakura's meditations on the appreciation of art and the art of flower arrangement (ikebana). True appreciation requires sympathy -- a meeting between the giver and receiver. The flower chapter is a tender elegy on beauty, sacrifice, and the relationship between humanity and the natural world.",
        "keywords": ["art", "beauty", "appreciation", "flowers", "ikebana", "nature", "aesthetics"],
    },
}


def build_l2_items(l1_items):
    """Build L2 emergence items."""
    items = []
    l1_ids = {item["metadata"]["chapter_number"]: item["id"] for item in l1_items}

    sort_order = len(l1_items)

    for group_id, info in L2_GROUPS.items():
        composite_ids = [l1_ids[ch] for ch in info["chapters"] if ch in l1_ids]

        item = {
            "id": group_id,
            "name": info["name"],
            "sort_order": sort_order,
            "category": info["category"],
            "level": 2,
            "composite_of": composite_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": info["about"],
                "For Readers": f"These {len(composite_ids)} essays form a natural cluster. Read them together for a deeper immersion in this dimension of Okakura's thought, or let a single chapter draw you in.",
            },
            "keywords": info["keywords"],
            "metadata": {
                "chapter_count": len(composite_ids),
                "chapter_numbers": info["chapters"],
            },
        }
        items.append(item)
        sort_order += 1

    return items


L3_GROUPS = {
    "meta-way-of-tea": {
        "name": "The Way of Tea",
        "category": "meta",
        "l2_ids": [
            "philosophy-and-spirit",
            "history-and-practice",
            "art-and-beauty",
        ],
        "about": "Okakura's complete vision of Teaism as a way of life. Not merely a ceremony or a beverage, but a philosophy that integrates spirit (Taoism and Zen), practice (the tea-room and its masters), and beauty (art and flowers) into a single, coherent art of living. 'Teaism is a cult founded on the adoration of the beautiful among the sordid facts of everyday existence.'",
        "keywords": ["Teaism", "way of life", "aesthetics", "philosophy", "practice", "beauty"],
    },
}


def build_l3_items(l1_items, l2_items):
    """Build L3 meta-category items."""
    items = []
    sort_order = len(l1_items) + len(l2_items)

    all_ids = {item["id"] for item in l1_items + l2_items}

    for group_id, info in L3_GROUPS.items():
        composite_ids = [lid for lid in info["l2_ids"] if lid in all_ids]

        item = {
            "id": group_id,
            "name": info["name"],
            "sort_order": sort_order,
            "category": info["category"],
            "level": 3,
            "composite_of": composite_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": info["about"],
                "How to Use": "The Book of Tea is short enough to read in a single sitting, and deep enough to return to for years. Begin with 'The Cup of Humanity' for Okakura's manifesto, move to 'Taoism and Zennism' for the philosophical depth, and end with 'Tea-Masters' for the unforgettable story of Rikiu's last tea ceremony.",
            },
            "keywords": info["keywords"],
            "metadata": {},
        }
        items.append(item)
        sort_order += 1

    return items


def build_grammar(chapters):
    """Build the complete grammar JSON structure."""
    l1_items = build_l1_items(chapters)
    print(f"  Built {len(l1_items)} L1 items (chapters)")

    l2_items = build_l2_items(l1_items)
    print(f"  Built {len(l2_items)} L2 items (thematic groups)")

    l3_items = build_l3_items(l1_items, l2_items)
    print(f"  Built {len(l3_items)} L3 items (meta-categories)")

    all_items = l1_items + l2_items + l3_items

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Kakuzo Okakura",
                    "date": "1906",
                    "note": "Originally published by Fox Duffield & Company, New York. Written in English by the author.",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "1997",
                    "note": "Digitized text, eBook #769. Credits: Matthew, Gabrielle Harbowy, and David Widger.",
                },
            ],
        },
        "name": "The Book of Tea",
        "description": (
            "The Book of Tea by Kakuzo Okakura (1906), a luminous essay on the Japanese tea ceremony "
            "as a pathway to understanding Eastern aesthetics, philosophy, and the art of living. "
            "In seven chapters, Okakura traces the roots of Teaism through Taoism and Zen Buddhism, "
            "explores the architecture of the tea-room, the appreciation of art and flowers, and the "
            "lives of the great tea-masters -- culminating in the unforgettable story of Rikiu's last "
            "tea ceremony. Written in English for a Western audience, it remains one of the most "
            "beautiful bridges between Eastern and Western thought.\n\n"
            "Source: Project Gutenberg eBook #769 (https://www.gutenberg.org/ebooks/769)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Japanese woodblock prints (ukiyo-e) of tea ceremonies "
            "by Kitagawa Utamaro, Suzuki Harunobu, and Utagawa Hiroshige. Also: photographs of traditional "
            "tea-rooms and chashitsu architecture. Illustrations from early 20th century editions of the book."
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["tea", "aesthetics", "Zen", "Taoism", "Japanese-culture", "philosophy", "art-of-living", "essay"],
        "roots": ["eastern-wisdom"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan", "Shrei"],
        "worldview": "non-dual",
        "items": all_items,
    }

    return grammar


def main():
    print("Reading seed text...")
    text = read_seed()

    print("Stripping front matter...")
    text = strip_front_matter(text)

    print("Parsing chapters...")
    chapters = parse_chapters(text)
    print(f"  Found {len(chapters)} chapters")

    if len(chapters) != 7:
        print(f"  WARNING: Expected 7 chapters, found {len(chapters)}", file=sys.stderr)
        missing = [i for i in range(1, 8) if i not in chapters]
        if missing:
            print(f"  Missing chapters: {missing}", file=sys.stderr)

    print("Building grammar...")
    grammar = build_grammar(chapters)

    print(f"Writing grammar to {OUTPUT_DIR / 'grammar.json'}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "grammar.json", "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    total_items = len(grammar["items"])
    print(f"Done! {total_items} total items written.")


if __name__ == "__main__":
    main()
