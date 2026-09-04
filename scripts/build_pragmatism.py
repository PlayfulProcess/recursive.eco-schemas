#!/usr/bin/env python3
"""
Build grammar.json for Pragmatism by William James.

Source: Project Gutenberg eBook #5116
Author: William James (1907)

Structure:
- L1: 8 lectures
- L2: Thematic groupings (4 themes)
- L3: Meta-categories (The Complete Work)
"""

import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "pragmatism.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "pragmatism"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# The 8 lectures - titles as they appear in text after "Lecture N" heading
LECTURES = [
    {"num": "I", "title": "The Present Dilemma in Philosophy"},
    {"num": "II", "title": "What Pragmatism Means"},
    {"num": "III", "title": "Some Metaphysical Problems Pragmatically Considered"},
    {"num": "IV", "title": "The One and the Many"},
    {"num": "V", "title": "Pragmatism and Common Sense"},
    {"num": "VI", "title": "Pragmatism's Conception of Truth"},
    {"num": "VII", "title": "Pragmatism and Humanism"},
    {"num": "VIII", "title": "Pragmatism and Religion"},
]

LECTURE_KEYWORDS = {
    1: ["temperament", "philosophy", "rationalism", "empiricism", "tender-minded", "tough-minded"],
    2: ["method", "truth", "meaning", "consequences", "squirrel", "humanism"],
    3: ["substance", "materialism", "design", "free-will", "metaphysics"],
    4: ["monism", "pluralism", "unity", "many", "oneness"],
    5: ["common-sense", "categories", "evolution", "knowledge", "concepts"],
    6: ["truth", "verification", "agreement", "expedient", "reality"],
    7: ["humanism", "reality", "rationalism", "human-contribution"],
    8: ["religion", "meliorism", "salvation", "possibility", "Absolute"],
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


def find_content_start(text):
    """Find where the actual lecture content begins (after TOC).

    The text has: Preface, then Contents (with all 8 lectures listed),
    then 'PRAGMATISM' heading, then the actual lectures.
    We need to find the SECOND occurrence of 'Lecture I' —
    the first is in the Contents, the second is the actual lecture.
    """
    # Find the "PRAGMATISM" heading that precedes the actual lectures
    # It appears as a standalone heading after the TOC
    lines = text.split('\n')
    in_content = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "PRAGMATISM" and i > 100:  # After TOC
            return '\n'.join(lines[i:])

    # Fallback: find second occurrence of "Lecture I"
    first = text.find("Lecture I\n")
    if first >= 0:
        second = text.find("Lecture I\n", first + 20)
        if second >= 0:
            return text[second:]
    return text


def parse_lectures(text):
    """Parse the book into its 8 lectures."""
    lectures = []

    for i, lecture in enumerate(LECTURES):
        # Pattern: "Lecture <num>\n\n<title>"
        pattern = rf'Lecture {lecture["num"]}\s*\n\s*\n\s*{re.escape(lecture["title"])}'
        match = re.search(pattern, text)
        if not match:
            # Try simpler pattern
            pattern = rf'Lecture {lecture["num"]}\s*\n'
            matches = list(re.finditer(pattern, text))
            if matches:
                match = matches[-1]  # Take last match (actual content, not TOC)
            else:
                print(f"WARNING: Could not find Lecture {lecture['num']}: {lecture['title']}")
                continue

        # Find the actual text content (skip the heading and title)
        start = match.end()
        # Skip the title line if we matched just "Lecture N\n"
        remaining = text[start:]
        title_match = re.match(r'\s*' + re.escape(lecture["title"]) + r'\s*\n', remaining)
        if title_match:
            start += title_match.end()

        # Find the next lecture or end of text
        if i + 1 < len(LECTURES):
            next_pattern = rf'Lecture {LECTURES[i+1]["num"]}\s*\n'
            next_match = re.search(next_pattern, text[start:])
            if next_match:
                end = start + next_match.start()
            else:
                end = len(text)
        else:
            end = len(text)

        lecture_text = text[start:end].strip()
        # Clean up whitespace
        lecture_text = re.sub(r'\n{3,}', '\n\n', lecture_text)

        lectures.append({
            'num': i + 1,
            'roman': lecture['num'],
            'title': lecture['title'],
            'text': lecture_text,
        })

    return lectures


def make_id(title):
    """Create a hyphenated ID from a lecture title."""
    clean = title.lower()
    clean = re.sub(r"'s", "s", clean)
    clean = re.sub(r'[^a-z0-9\s-]', '', clean)
    clean = re.sub(r'\s+', '-', clean.strip())
    clean = re.sub(r'-+', '-', clean)
    return f"lecture-{clean}"


# Thematic groupings for L2
THEMES = [
    {
        "id": "theme-method-and-meaning",
        "name": "Method and Meaning",
        "lectures": ["lecture-the-present-dilemma-in-philosophy", "lecture-what-pragmatism-means"],
        "about": "The opening movement of James's argument: philosophy is stuck between two temperaments — the 'tender-minded' (rationalist, idealist, optimistic) and the 'tough-minded' (empiricist, materialist, skeptical). Pragmatism offers a way through. It is first presented as a method for settling metaphysical disputes by tracing their practical consequences: if two theories have exactly the same practical effects, they mean the same thing. The famous squirrel example illustrates the approach.",
        "for_readers": "Lecture I is one of the most entertaining pieces of philosophical writing ever produced. James's portrait of philosophical temperaments — the tender-minded rationalist and the tough-minded empiricist — is both funny and penetrating. Lecture II introduces the pragmatic method through the brilliantly simple squirrel story. Together they provide the clearest introduction to pragmatism ever written.",
    },
    {
        "id": "theme-metaphysical-applications",
        "name": "Metaphysical Applications",
        "lectures": ["lecture-some-metaphysical-problems-pragmatically-considered", "lecture-the-one-and-the-many", "lecture-pragmatism-and-common-sense"],
        "about": "James applies the pragmatic method to the great traditional problems of philosophy: substance, materialism vs. spiritualism, design, free will, the one and the many, and the categories of common sense. In each case, he asks: what practical difference does it make? The results are liberating — many 'deep' philosophical disputes turn out to be verbal, while others (like free will) gain new urgency when their practical stakes are made clear.",
        "for_readers": "Lecture III shows pragmatism at work on real philosophical problems — substance, materialism, design, free will. Lecture IV tackles the monism-pluralism debate with characteristic verve. Lecture V is the most original, arguing that our basic concepts (thing, cause, mind, body) were themselves once revolutionary inventions by prehistoric geniuses. These lectures show why pragmatism matters beyond philosophy departments.",
    },
    {
        "id": "theme-truth-theory",
        "name": "The Theory of Truth",
        "lectures": ["lecture-pragmatisms-conception-of-truth", "lecture-pragmatism-and-humanism"],
        "about": "The most controversial and consequential part of James's pragmatism: his theory of truth. Truth is not a static correspondence between ideas and fixed reality but a dynamic process of verification. 'The true is the name of whatever proves itself to be good in the way of belief.' Ideas become true as they are verified in experience. This is not relativism — reality constrains our beliefs — but it means truth is made, not found, and grows over time.",
        "for_readers": "Lecture VI contains James's most famous and most attacked claims. Read it slowly — James is not saying 'anything goes' but that truth is a living, growing thing tied to human practice. Lecture VII deepens this with the concept of 'humanism' (borrowed from F.C.S. Schiller): the human contribution to reality is everywhere. These are the lectures that made pragmatism famous and infamous.",
    },
    {
        "id": "theme-religion-and-hope",
        "name": "Religion and Hope",
        "lectures": ["lecture-pragmatism-and-religion"],
        "about": "James's concluding vision: pragmatism as meliorism — the belief that the world can be made better, though not certainly. Against both optimism (everything is fine) and pessimism (nothing can help), pragmatism offers a world genuinely 'in the making,' where human effort matters. James connects this to religion: if believing in God makes us better able to improve the world, that belief has pragmatic value. The universe is an unfinished story in which we are co-authors.",
        "for_readers": "The final lecture reveals James's deepest motivation: he wants a philosophy that leaves room for genuine hope without certainty. His concept of meliorism — the world is neither saved nor lost but improvable — is perhaps his most enduring contribution. The closing image of a world 'in the making' where human choice matters is both philosophically rigorous and deeply moving.",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = find_content_start(text)

    lectures = parse_lectures(text)
    print(f"Parsed {len(lectures)} lectures")

    items = []
    sort_order = 0

    # L1: Individual lectures
    for lec in lectures:
        lec_id = make_id(lec['title'])
        sort_order += 1
        keywords = LECTURE_KEYWORDS.get(lec['num'], ["pragmatism", "philosophy"])

        items.append({
            "id": lec_id,
            "name": f"Lecture {lec['roman']}: {lec['title']}",
            "sort_order": sort_order,
            "level": 1,
            "category": "lecture",
            "sections": {
                "Text": lec['text'],
            },
            "keywords": keywords,
            "metadata": {
                "lecture_number": lec['num'],
            }
        })
        print(f"  Lecture {lec['roman']}: {lec['title']} ({len(lec['text'])} chars)")

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
            "composite_of": theme["lectures"],
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "lecture_count": len(theme["lectures"]),
            }
        })

    # L3: Meta-category
    sort_order += 1
    items.append({
        "id": "pragmatism-complete",
        "name": "Pragmatism: A New Name for Some Old Ways of Thinking",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "William James's Pragmatism (1907) is the founding text of America's most distinctive contribution to world philosophy. Based on lectures delivered at the Lowell Institute in Boston and Columbia University in New York, it presents pragmatism as both a method for settling philosophical disputes and a theory of truth. James argues that the meaning of any idea lies in its practical consequences, and that truth is not a static property but a dynamic process — ideas become true as they are verified in experience. The book moves from a diagnosis of philosophy's temperamental divide (rationalism vs. empiricism) through applications to metaphysics, epistemology, and religion, arriving at a vision of meliorism: the world is genuinely 'in the making,' and human effort matters. Dedicated to John Stuart Mill, it draws on Charles Sanders Peirce, John Dewey, and F.C.S. Schiller while remaining entirely James's own — warm, witty, concrete, and passionately engaged.",
            "For Readers": "Pragmatism is one of the most readable works of serious philosophy ever written. James writes with humor, energy, and an extraordinary gift for concrete examples (the squirrel, the hotel corridor, the lost in the forest). Read it straight through — it builds an argument across eight lectures. Or start with Lecture II (What Pragmatism Means) for the method, then jump to Lecture VI (Pragmatism's Conception of Truth) for the theory that shook philosophy. James is the rare philosopher who makes you feel the stakes of abstract questions.",
        },
        "keywords": ["pragmatism", "truth", "method", "James", "philosophy", "empiricism", "meliorism"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "William James",
                    "date": "1907",
                    "note": "Author"
                }
            ]
        },
        "name": "Pragmatism",
        "description": "William James's Pragmatism: A New Name for Some Old Ways of Thinking (1907) — the founding text of America's most distinctive philosophical tradition. Eight lectures delivered at the Lowell Institute and Columbia University, presenting pragmatism as both a method for resolving philosophical disputes and a revolutionary theory of truth. James argues that the meaning of any concept lies in its practical consequences, and that truth is not a fixed correspondence but a living, growing process of verification. Warm, witty, and devastatingly concrete.\n\nSource: Project Gutenberg eBook #5116 (https://www.gutenberg.org/ebooks/5116)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs of William James (various, 1890s-1900s). Images of Harvard University and the Lowell Institute in Boston. Portraits by his wife Alice Howe Gibbens James.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "pragmatism", "truth", "empiricism", "American-philosophy", "public-domain", "full-text"],
        "roots": ["process-philosophy"],
        "shelves": ["mirror"],
        "lineages": ["Akomolafe"],
        "worldview": "dialectical",
        "items": items,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1: {l1} lectures, L2: {l2} themes, L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
