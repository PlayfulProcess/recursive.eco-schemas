#!/usr/bin/env python3
"""
Build grammar.json for My First Summer in the Sierra by John Muir.

Source: Project Gutenberg eBook #32540
Author: John Muir (1911, based on journals from 1869)

Structure:
- L1: 11 chapters (journal entries covering June to September 1869)
- L2: Thematic groupings (4 themes)
- L3: Meta-category
"""

import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "my-first-summer-in-sierra.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "my-first-summer-in-sierra"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

CHAPTER_TITLES = [
    "Through the Foothills with a Flock of Sheep",
    "In Camp on the North Fork of the Merced",
    "A Bread Famine",
    "To the High Mountains",
    "The Yosemite",
    "Mount Hoffman and Lake Tenaya",
    "A Strange Experience",
    "The Mono Trail",
    "Bloody Canyon and Mono Lake",
    "The Tuolumne Camp",
    "Back to the Lowlands",
]

CHAPTER_IDS = [
    "through-the-foothills",
    "in-camp-north-fork-merced",
    "a-bread-famine",
    "to-the-high-mountains",
    "the-yosemite",
    "mount-hoffman-and-lake-tenaya",
    "a-strange-experience",
    "the-mono-trail",
    "bloody-canyon-and-mono-lake",
    "the-tuolumne-camp",
    "back-to-the-lowlands",
]

CHAPTER_KEYWORDS = [
    ["foothills", "sheep", "wildflowers", "central-valley", "june"],
    ["merced", "camp", "forests", "sugar-pine", "sequoia"],
    ["bread", "famine", "provisions", "hunger", "simplicity"],
    ["mountains", "altitude", "meadows", "flowers", "glaciers"],
    ["yosemite", "falls", "valley", "half-dome", "granite"],
    ["hoffman", "tenaya", "lake", "summit", "panorama"],
    ["bears", "wilderness", "fear", "solitude", "night"],
    ["mono", "trail", "pass", "altitude", "crossing"],
    ["canyon", "mono-lake", "volcanic", "desert", "alkaline"],
    ["tuolumne", "meadows", "camp", "autumn", "cathedral-peak"],
    ["descent", "lowlands", "farewell", "autumn", "return"],
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
    """Remove title page, dedication, TOC, and illustration list.

    The actual text begins at CHAPTER I.
    """
    match = re.search(r'^CHAPTER I\s*$', text, re.MULTILINE)
    if match:
        return text[match.start():]
    return text


def strip_back_matter(text):
    """Remove INDEX and anything after the main text."""
    # Look for INDEX section
    idx = text.find("\nINDEX\n")
    if idx >= 0:
        text = text[:idx]
    # Also check for "INDEX" at start of a line
    match = re.search(r'^INDEX\s*$', text, re.MULTILINE)
    if match:
        text = text[:match.start()]
    return text.strip()


def parse_chapters(text):
    """Parse into 11 chapters."""
    chapters = []

    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC]+)\s*$', re.MULTILINE)
    matches = list(chapter_pattern.finditer(text))

    for i, match in enumerate(matches):
        start = match.start()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        chunk = text[start:end].strip()
        lines = chunk.split('\n')

        # Skip "CHAPTER X", blank line, title line, blank line
        text_start = 0
        blank_count = 0
        title_found = False
        for j, line in enumerate(lines):
            if j == 0:
                continue  # "CHAPTER X"
            if not line.strip():
                if title_found:
                    blank_count += 1
                continue
            if not title_found:
                title_found = True
                continue  # title line
            if title_found and blank_count >= 1:
                text_start = j
                break

        chapter_text = '\n'.join(lines[text_start:]).strip()

        # Clean up: remove [Illustration...] markers
        chapter_text = re.sub(r'\[Illustration[^\]]*\]', '', chapter_text)
        # Normalize whitespace
        chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)
        chapter_text = chapter_text.strip()

        chapters.append({
            'index': i,
            'text': chapter_text,
        })

    return chapters


# Thematic groupings
THEMES = [
    {
        "id": "theme-ascent-and-landscape",
        "name": "The Ascent: Foothills to High Sierra",
        "chapters": [
            "through-the-foothills",
            "to-the-high-mountains",
            "mount-hoffman-and-lake-tenaya",
        ],
        "about": "Muir's physical and spiritual ascent from the hot Central Valley through the successive forest belts to the high granite peaks of the Sierra. Each chapter rises in elevation and in Muir's ecstatic response to the landscape. The foothills are beautiful but parched; the middle forests are cathedral-like; the high country is pure light and granite and ice.",
        "for_readers": "Follow Muir's elevation gain as a metaphor for deepening attention. The foothills chapter introduces his method — patient daily observation punctuated by rapture. Mount Hoffman is the summit experience, both literally and spiritually.",
    },
    {
        "id": "theme-yosemite-and-wonder",
        "name": "Yosemite and Natural Wonder",
        "chapters": [
            "the-yosemite",
            "bloody-canyon-and-mono-lake",
            "the-tuolumne-camp",
        ],
        "about": "Muir's encounters with the Sierra's most dramatic landscapes: Yosemite Valley with its waterfalls and granite walls, the volcanic desolation of Mono Lake, and the sublime meadows of the Tuolumne. His descriptions blend scientific precision (he is always measuring, classifying, theorizing about glaciation) with mystical celebration.",
        "for_readers": "The Yosemite chapter contains some of Muir's most famous descriptions — the first sight of Yosemite Falls, the granite domes, the sense of entering a temple. Mono Lake provides stark contrast: alkaline, volcanic, otherworldly. The Tuolumne meadows are Muir's paradise found.",
    },
    {
        "id": "theme-wilderness-and-solitude",
        "name": "Wilderness, Solitude, and the Inner Life",
        "chapters": [
            "in-camp-north-fork-merced",
            "a-bread-famine",
            "a-strange-experience",
        ],
        "about": "The personal and spiritual dimension of Muir's summer. In camp, he observes the daily rhythms of forest life. The bread famine reduces him to essentials and deepens his kinship with wild creatures. The strange experience — encounters with bears and the unsettling solitude of the deep wilderness — tests his nerve and transforms his relationship with fear.",
        "for_readers": "These are the most intimate chapters. The bread famine is both comic and revealing — Muir discovers he can live on less than he thought. A Strange Experience shows the wilderness pushing back, reminding Muir that he is a guest in a world not made for human comfort.",
    },
    {
        "id": "theme-journey-and-return",
        "name": "The Journey Out and the Return",
        "chapters": [
            "the-mono-trail",
            "back-to-the-lowlands",
        ],
        "about": "The arc of departure: crossing the Sierra divide via the Mono Trail into the eastern desert, then the bittersweet descent back to the lowlands as autumn arrives. Muir's summer in the mountains ends not with triumph but with longing — he does not want to leave, and the return to civilization feels like exile.",
        "for_readers": "The Mono Trail chapter captures the drama of a Sierra crossing — the high pass, the sudden descent into a different world. Back to the Lowlands is one of the most poignant endings in nature writing. Muir's reluctant farewell to the mountains reveals how deeply the Sierra has entered his soul.",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = strip_front_matter(text)
    text = strip_back_matter(text)

    chapters = parse_chapters(text)
    print(f"Parsed {len(chapters)} chapters (expected 11)")

    items = []
    sort_order = 0

    # L1: Individual chapters
    for i, ch in enumerate(chapters):
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
        print(f"  Ch {i+1:2d}: {chapter_name} ({len(ch['text'])} chars)")

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
        "id": "my-first-summer-complete",
        "name": "My First Summer in the Sierra",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "John Muir's My First Summer in the Sierra (1911, based on journals from 1869) is the ecstatic record of a young Scotsman's first season in the mountains that would define his life. Hired as a sheepherder's assistant, the 31-year-old Muir follows a flock from the hot Central Valley up through the forest belts to the high meadows of Yosemite and the Tuolumne. His journal entries, dated from June through September 1869, combine precise botanical and geological observation with rhapsodic celebration. Every tree, flower, bird, and rock formation is greeted with wonder. The Sierra is not landscape but living temple, and Muir's summer among its peaks and meadows transforms him from wanderer to prophet of wilderness.",
            "For Readers": "Read this book in summer if you can, and outdoors if possible. Muir's prose is so saturated with sunlight and mountain air that it changes the reader's attention to the natural world. The chapters follow the calendar — June through September — and the elevation rises with the summer. Read straight through for the journey, or dip into individual chapters: The Yosemite for awe, A Bread Famine for humor and simplicity, Mount Hoffman for the summit of Muir's ecstasy, Back to the Lowlands for the bittersweet farewell.",
        },
        "keywords": ["sierra", "muir", "mountains", "nature", "wilderness", "yosemite"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "John Muir",
                    "date": "1911",
                    "note": "Author (based on 1869 journals)"
                }
            ]
        },
        "name": "My First Summer in the Sierra",
        "description": "John Muir's My First Summer in the Sierra (1911) — the ecstatic journal of a young naturalist's first season in the mountains of California. Based on Muir's 1869 journals, the book follows his ascent from the Central Valley through the forest belts to the high granite peaks of Yosemite and the Tuolumne. 11 chapters of precise observation and rapturous celebration that helped inspire the American conservation movement.\n\nSource: Project Gutenberg eBook #32540 (https://www.gutenberg.org/ebooks/32540)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Herbert W. Gleason's photographs of the Sierra Nevada (early 1900s), which accompanied the original edition. Charles S. Olcott's Yosemite photographs. William Keith's paintings of the Sierra (Keith was Muir's close friend). Carleton Watkins' and Eadweard Muybridge's photographs of Yosemite (1860s-1870s).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["nature", "mountains", "journal", "wilderness", "ecology", "california", "public-domain", "full-text"],
        "roots": ["ecology-nature"],
        "shelves": ["earth"],
        "lineages": ["Shrei"],
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
