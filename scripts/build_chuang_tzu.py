#!/usr/bin/env python3
"""
Parse Chuang Tzu: Mystic, Moralist, and Social Reformer (Gutenberg #59709)
into grammar.json.

Herbert A. Giles translation, 1889.

Structure:
- 33 chapters, divided by scholarly tradition into:
  - Inner Chapters (1-7): attributed to Chuang Tzu himself
  - Outer Chapters (8-22): possibly by Chuang Tzu or close followers
  - Miscellaneous Chapters (23-33): later additions
- L1: Individual chapters
- L2: Thematic groupings (Inner Chapters, Nature/Wu Wei, Tao/Cosmos,
       Knowledge/Limits, Sage's Way, Miscellaneous)
- L3: Meta-categories

NOTE: Giles' commentary appears as indented lines in the text.
Per project convention (build-logs), we strip these editorial comments
to keep only the primary text.
"""

import json
import re
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "chuang-tzu.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "chuang-tzu")
OUTPUT = os.path.join(OUTPUT_DIR, "grammar.json")

# Roman numeral to int mapping for chapters I-XXXIII
ROMAN_MAP = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
    "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13,
    "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19,
    "XX": 20, "XXI": 21, "XXII": 22, "XXIII": 23, "XXIV": 24, "XXV": 25,
    "XXVI": 26, "XXVII": 27, "XXVIII": 28, "XXIX": 29, "XXX": 30,
    "XXXI": 31, "XXXII": 32, "XXXIII": 33,
}

# The 33 chapters with their titles and keywords
CHAPTERS = [
    {"num": 1, "title": "Transcendental Bliss",
     "keywords": ["infinity", "relativity", "perspective", "uselessness", "freedom"]},
    {"num": 2, "title": "The Identity of Contraries",
     "keywords": ["contraries", "duality", "identity", "subjectivity", "oneness", "butterfly-dream"]},
    {"num": 3, "title": "Nourishment of the Soul",
     "keywords": ["soul", "nourishment", "cook", "ox", "skill", "nature"]},
    {"num": 4, "title": "Man Among Men",
     "keywords": ["society", "uselessness", "service", "danger", "diplomacy"]},
    {"num": 5, "title": "The Evidence of Virtue Complete",
     "keywords": ["virtue", "wholeness", "deformity", "inner-worth", "character"]},
    {"num": 6, "title": "The Great Supreme",
     "keywords": ["death", "life", "Tao", "supreme", "transformation", "acceptance"]},
    {"num": 7, "title": "How to Govern",
     "keywords": ["governance", "non-action", "wu-wei", "ruler", "sage-king"]},
    {"num": 8, "title": "Joined Toes",
     "keywords": ["nature", "artificiality", "virtue", "spontaneity", "civilization"]},
    {"num": 9, "title": "Horses' Hoofs",
     "keywords": ["horses", "nature", "civilization", "corruption", "simplicity"]},
    {"num": 10, "title": "Opening Trunks",
     "keywords": ["theft", "sagacity", "government", "robbery", "power"]},
    {"num": 11, "title": "On Letting Alone",
     "keywords": ["non-interference", "wu-wei", "government", "nature", "letting-alone"]},
    {"num": 12, "title": "The Universe",
     "keywords": ["universe", "cosmos", "Tao", "creation", "heaven-earth"]},
    {"num": 13, "title": "The Tao of God",
     "keywords": ["Tao", "God", "heaven", "emperor", "sage", "teaching"]},
    {"num": 14, "title": "The Circling Sky",
     "keywords": ["sky", "cosmos", "questions", "knowledge", "seasons"]},
    {"num": 15, "title": "Self-Conceit",
     "keywords": ["humility", "conceit", "stillness", "water", "mirror"]},
    {"num": 16, "title": "Exercise of Faculties",
     "keywords": ["faculties", "senses", "nature", "return", "simplicity"]},
    {"num": 17, "title": "Autumn Floods",
     "keywords": ["relativity", "perspective", "river", "sea", "knowledge", "limits"]},
    {"num": 18, "title": "Perfect Happiness",
     "keywords": ["happiness", "joy", "death", "skull", "contentment"]},
    {"num": 19, "title": "The Secret of Life",
     "keywords": ["life", "skill", "craft", "archery", "swimming", "mastery"]},
    {"num": 20, "title": "Mountain Trees",
     "keywords": ["trees", "uselessness", "survival", "wisdom", "adaptation"]},
    {"num": 21, "title": "T'ien Tz\u016d Fang",
     "keywords": ["teaching", "master", "disciple", "art", "naturalness"]},
    {"num": 22, "title": "Knowledge Travels North",
     "keywords": ["knowledge", "Tao", "north", "seeking", "silence", "unknowing"]},
    {"num": 23, "title": "K\u00eang Sang Ch'u",
     "keywords": ["sage", "disciple", "teaching", "questions", "inner-life"]},
    {"num": 24, "title": "Hs\u00fc Wu Kuei",
     "keywords": ["archery", "skill", "Tao", "ruler", "counsel"]},
    {"num": 25, "title": "Ts\u00ea Yang",
     "keywords": ["cosmology", "creation", "unity", "diversity", "paradox"]},
    {"num": 26, "title": "Contingencies",
     "keywords": ["contingency", "externals", "parable", "fish", "trap"]},
    {"num": 27, "title": "Language",
     "keywords": ["language", "words", "meaning", "communication", "silence"]},
    {"num": 28, "title": "On Declining Power",
     "keywords": ["power", "decline", "renunciation", "abdication", "simplicity"]},
    {"num": 29, "title": "Robber Ch\u00ea",
     "keywords": ["robber", "Confucius", "morality", "hypocrisy", "critique"]},
    {"num": 30, "title": "On Swords",
     "keywords": ["swords", "ruler", "statecraft", "metaphor", "combat"]},
    {"num": 31, "title": "The Old Fisherman",
     "keywords": ["fisherman", "Confucius", "sincerity", "naturalness", "truth"]},
    {"num": 32, "title": "Lieh Tz\u016d",
     "keywords": ["Lieh-Tzu", "wind", "illusion", "fate", "chance"]},
    {"num": 33, "title": "The Empire",
     "keywords": ["empire", "philosophy", "schools", "survey", "synthesis"]},
]

# Thematic groupings (L2)
THEMES = [
    {
        "id": "theme-inner-chapters",
        "name": "The Inner Chapters",
        "chapter_nums": [1, 2, 3, 4, 5, 6, 7],
        "about": "The seven Inner Chapters (Nei P'ien) are universally regarded as the authentic core of Chuang Tzu's philosophy, most likely written by Chuang Tzu himself in the 4th century BCE. They contain his most celebrated passages: the butterfly dream, the cook cutting up an ox, the useless tree, and the identity of contraries. Together they lay out a complete philosophical vision — the relativity of all distinctions, the futility of argument, the nourishment of life through skill and spontaneity, the paradox of useful uselessness, and the ultimate unity of life and death in the Tao.",
        "for_readers": "Start here. These seven chapters are the beating heart of Taoist philosophy. Read them slowly, let the paradoxes work on you. Chuang Tzu does not argue — he tells stories, and the stories dissolve the categories your mind insists on maintaining.",
    },
    {
        "id": "theme-nature-wu-wei",
        "name": "Nature and Non-Action (Wu Wei)",
        "chapter_nums": [8, 9, 10, 11],
        "about": "Chapters 8 through 11 form a sustained critique of civilization and its discontents. Joined toes and extra fingers are natural — but charity and duty are artificial additions to human nature. Horses run free until the horse-trainer breaks them. Trunks are locked against thieves, but the greatest thief steals the whole trunk. The solution is wu wei: letting alone, non-interference, allowing things to follow their own nature without the meddling of sages and rulers.",
        "for_readers": "A Taoist manifesto against the over-managed life. These chapters challenge every assumption about improvement, education, and moral cultivation. What if the best thing a ruler — or a parent, or a teacher — could do is simply get out of the way?",
    },
    {
        "id": "theme-tao-cosmos",
        "name": "The Tao and the Cosmos",
        "chapter_nums": [12, 13, 14],
        "about": "Three cosmological meditations on the Tao as the source and substance of all things. Chapter 12 (The Universe) explores how the Tao pervades heaven and earth. Chapter 13 (The Tao of God) traces the transmission of the Way from the cosmic to the human. Chapter 14 (The Circling Sky) poses the great questions about the nature of the cosmos that cannot be answered but must be lived.",
        "for_readers": "For those drawn to the big questions: What is the universe? Where does it come from? How does the Tao manifest in the daily life of a sage? These chapters move between cosmic scale and intimate encounter.",
    },
    {
        "id": "theme-knowledge-limits",
        "name": "Knowledge and Its Limits",
        "chapter_nums": [15, 16, 17, 18],
        "about": "An epistemological sequence exploring the limits and illusions of knowledge. Self-Conceit warns against the arrogance of learning. Exercise of Faculties counsels a return to simplicity. Autumn Floods — one of Chuang Tzu's most celebrated chapters — uses the dialogue between the River God and the Sea to demolish all claims to absolute knowledge. Perfect Happiness asks whether happiness can be pursued or only received.",
        "for_readers": "Essential reading for anyone who suspects that knowing more does not always mean understanding more. The Autumn Floods chapter alone is worth the entire book — a masterpiece of philosophical dialogue on the relativity of all perspective.",
    },
    {
        "id": "theme-sages-way",
        "name": "The Sage's Way",
        "chapter_nums": [19, 20, 21, 22],
        "about": "Four chapters on the practical wisdom of the sage in the world. The Secret of Life reveals mastery through stories of craftsmen, swimmers, and archers who embody effortless skill. Mountain Trees explores how the sage navigates between usefulness and uselessness. T'ien Tzu Fang offers portraits of true teachers and their methods. Knowledge Travels North is the profound culmination: the Tao cannot be spoken, cannot be taught, cannot be known — and yet it is everywhere.",
        "for_readers": "The most practical section of the book. How does one actually live the Tao? Through skill acquired by forgetting technique, through adaptation that is neither submission nor resistance, through teaching that is silence, and through knowledge that knows it cannot know.",
    },
    {
        "id": "theme-miscellaneous-chapters",
        "name": "The Miscellaneous Chapters",
        "chapter_nums": [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33],
        "about": "The eleven Miscellaneous Chapters (Tsa P'ien) are generally considered later additions by followers and editors of the Chuang Tzu school. They include some of the text's most provocative material: the famous passage about the fish-trap and the word-trap (Chapter 26), the satirical encounter between Confucius and Robber Che (Chapter 29), and the remarkable final chapter surveying all the philosophical schools of ancient China. While their authorship is debated, they extend and develop the core themes of the Inner Chapters into new territory.",
        "for_readers": "Do not skip these on account of disputed authorship. Chapter 26 on Contingencies contains the immortal line about forgetting the trap once the fish is caught — a perfect metaphor for Chuang Tzu's entire philosophy of language. Chapter 33 on The Empire is the oldest surviving history of Chinese philosophy.",
    },
]

# L3 meta-categories
META_CATEGORIES = [
    {
        "id": "meta-way-of-chuang-tzu",
        "name": "The Way of Chuang Tzu",
        "composite_of": [t["id"] for t in THEMES],
        "about": "The Chuang Tzu is not a treatise but a living thing — a collection of parables, dialogues, meditations, and cosmic jokes that dissolve the reader's certainties one by one. Its method is not argument but transformation: by the time you finish, you are no longer sure what is real and what is dream, what is useful and what is useless, what is life and what is death. This is precisely the point. The Way of Chuang Tzu is the way of radical freedom — freedom from fixed perspectives, from the tyranny of conventional knowledge, from the prison of the ego. It is the oldest and most eloquent expression of the insight that the Tao which can be named is not the eternal Tao.",
    },
    {
        "id": "meta-complete-chuang-tzu",
        "name": "Chuang Tzu and the Tao",
        "composite_of": ["chapter-{:02d}".format(i) for i in range(1, 34)],
        "about": "The complete Chuang Tzu in Herbert Giles' 1889 translation — all thirty-three chapters, from the soaring Leviathan of Chapter 1 to the philosophical survey of Chapter 33. This is one of the foundational texts of world philosophy, standing alongside the Tao Te Ching as the twin pillar of Taoist thought. Where Lao Tzu is terse and enigmatic, Chuang Tzu is expansive and playful. Where Lao Tzu speaks in the voice of the sage, Chuang Tzu gives voice to butchers, wheelwrights, cicadas, butterflies, and the skull by the roadside. Together they constitute one of humanity's deepest investigations into the nature of reality, knowledge, and the good life.",
    },
]


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    if start == -1:
        start = text.find("*** START OF THIS PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if end == -1:
        end = text.find("*** END OF THIS PROJECT GUTENBERG EBOOK")
    if start != -1:
        text = text[text.index("\n", start) + 1:]
    if end != -1:
        text = text[:end]
    return text.strip()


def strip_commentary(text):
    """Remove Giles' editorial commentary (indented lines).

    Commentary lines in the Giles translation are indented with leading spaces.
    We remove these to keep only the primary text. We also remove the
    _Argument_ summary at the start of each chapter (captured separately).
    """
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        # Skip lines that are indented (Giles' commentary)
        # But keep blank lines for paragraph structure
        if line == '' or line == '\n':
            cleaned.append('')
            continue
        # Commentary lines start with spaces (typically 1-2 spaces)
        # Primary text lines start at column 0
        if line and line[0] == ' ':
            continue
        cleaned.append(line)
    result = '\n'.join(cleaned)
    # Collapse multiple blank lines
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()


def extract_argument(text):
    """Extract the _Argument_ section from the start of a chapter."""
    match = re.search(r'_Argument_:?--(.+?)(?:\n\n|\n[A-Z])', text, re.DOTALL)
    if match:
        arg_text = match.group(1).strip()
        # Clean up: remove extra whitespace from line wrapping
        arg_text = re.sub(r'\s+', ' ', arg_text)
        return arg_text
    return ""


def parse_chapters(text):
    """Parse all 33 chapters from the stripped Gutenberg text."""
    lines = text.split('\n')

    # Find chapter boundaries using "CHAPTER I." pattern
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXL]+)\.\s*$')
    boundaries = []

    for i, line in enumerate(lines):
        m = chapter_pattern.match(line.strip())
        if m:
            roman = m.group(1)
            if roman in ROMAN_MAP:
                boundaries.append((ROMAN_MAP[roman], i))

    if len(boundaries) != 33:
        print(f"WARNING: Found {len(boundaries)} chapters, expected 33")
        for num, line_num in boundaries:
            print(f"  Chapter {num} at line {line_num}")

    # Find end of text (before INDEX)
    text_end = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == '_INDEX_' or line.strip() == 'INDEX':
            text_end = i
            break

    parsed = []
    for idx, (ch_num, start_line) in enumerate(boundaries):
        # End boundary: next chapter or end of text
        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][1]
        else:
            end_line = text_end

        # Get the raw chapter text (everything between chapter heading and next chapter)
        raw_lines = lines[start_line:end_line]
        raw_text = '\n'.join(raw_lines)

        # Extract title (first non-blank line after "CHAPTER X.")
        title = ""
        content_start = 0
        for j, cl in enumerate(raw_lines):
            stripped = cl.strip()
            if j == 0:
                continue  # Skip the "CHAPTER X." line
            if stripped and not title:
                title = stripped.rstrip('.')
                content_start = j + 1
                break

        # Extract the Argument
        argument = extract_argument(raw_text)

        # Get content after the title line
        content_lines = raw_lines[content_start:]
        content_text = '\n'.join(content_lines)

        # Remove the _Argument_ block from content
        # The argument block starts with " _Argument_" (indented) and ends at the
        # first non-indented, non-blank line
        content_text = re.sub(
            r'\s*_Argument_:?--.*?(?=\n[A-Z]|\n\n[A-Z])',
            '',
            content_text,
            count=1,
            flags=re.DOTALL
        )

        # Strip Giles' commentary (indented lines)
        content_text = strip_commentary(content_text)

        # Clean up
        content_text = content_text.strip()

        # Find the matching chapter definition
        ch_def = next((c for c in CHAPTERS if c["num"] == ch_num), None)
        if ch_def is None:
            print(f"WARNING: No definition for chapter {ch_num}")
            continue

        parsed.append({
            "num": ch_num,
            "title": ch_def["title"],  # Use our clean title, not the ALL-CAPS one
            "argument": argument,
            "content": content_text,
            "keywords": ch_def["keywords"],
        })

    return parsed


def chapter_id(num):
    """Generate a chapter ID from its number."""
    return f"chapter-{num:02d}"


def chapter_section(ch):
    """Determine the scholarly section for a chapter."""
    if ch["num"] <= 7:
        return "inner"
    elif ch["num"] <= 22:
        return "outer"
    else:
        return "miscellaneous"


def build_grammar(chapters):
    """Build the grammar items list from parsed chapters."""
    items = []
    sort_order = 0

    # L1: Individual chapters
    for ch in chapters:
        sort_order += 1
        sections = {}

        if ch["argument"]:
            sections["Argument"] = ch["argument"]
        sections["Text"] = ch["content"]

        section = chapter_section(ch)
        section_label = {
            "inner": "Inner Chapters (1-7)",
            "outer": "Outer Chapters (8-22)",
            "miscellaneous": "Miscellaneous Chapters (23-33)",
        }[section]

        items.append({
            "id": chapter_id(ch["num"]),
            "name": f"Chapter {ch['num']}: {ch['title']}",
            "level": 1,
            "category": section_label,
            "sort_order": sort_order,
            "sections": sections,
            "keywords": ch["keywords"],
            "metadata": {
                "chapter_number": ch["num"],
                "section": section,
            },
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
            "composite_of": [chapter_id(n) for n in theme["chapter_nums"]],
            "sort_order": sort_order,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {"chapter_count": len(theme["chapter_nums"])},
        })

    # L3: Meta-categories
    for meta in META_CATEGORIES:
        sort_order += 1
        items.append({
            "id": meta["id"],
            "name": meta["name"],
            "level": 3,
            "category": "meta",
            "relationship_type": "emergence",
            "composite_of": meta["composite_of"],
            "sort_order": sort_order,
            "sections": {
                "About": meta["about"],
            },
            "keywords": [],
            "metadata": {},
        })

    return items


def main():
    # Read the seed file
    if not os.path.exists(SEED):
        print(f"ERROR: Seed file not found at {SEED}")
        print("To download, run locally:")
        print('  curl -L -o seeds/chuang-tzu.txt '
              '"https://www.gutenberg.org/cache/epub/59709/pg59709.txt" && \\')
        print('  git add seeds/chuang-tzu.txt && \\')
        print('  git commit -m "Add Chuang Tzu source text (Gutenberg #59709)" && \\')
        print('  git push origin $(git branch --show-current)')
        sys.exit(1)

    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    # Quick sanity check
    if "Chuang" not in raw and "Zhuangzi" not in raw:
        print("ERROR: The seed file does not appear to contain Chuang Tzu.")
        print("Expected: Chuang Tzu: Mystic, Moralist, and Social Reformer (Gutenberg #59709)")
        sys.exit(1)

    text = strip_gutenberg(raw)
    chapters = parse_chapters(text)

    if not chapters:
        print("ERROR: No chapters parsed.")
        sys.exit(1)

    print(f"Parsed {len(chapters)} chapters")
    for ch in chapters:
        preview = ch["content"][:60].replace('\n', ' ')
        print(f"  Ch {ch['num']:2d}: {ch['title']}: {preview}...")

    items = build_grammar(chapters)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Zhuangzi (Chuang Tzu)",
                    "date": "4th-3rd century BCE",
                    "note": "Author, Taoist philosopher",
                },
                {
                    "name": "Herbert A. Giles",
                    "date": "1889",
                    "note": "Translator, H.B.M.'s Consul at Tamsui",
                },
            ],
        },
        "name": "Chuang Tzu: Mystic, Moralist, and Social Reformer",
        "description": (
            "The complete Chuang Tzu (Zhuangzi) in Herbert A. Giles' landmark 1889 "
            "translation — all 33 chapters of one of the foundational texts of Taoist "
            "philosophy. Chuang Tzu (c. 369-286 BCE) was the most brilliant and "
            "creative of the ancient Chinese philosophers, whose parables of the "
            "butterfly dream, the cook and the ox, and the useless tree have shaped "
            "world thought for over two millennia. The Inner Chapters (1-7) are "
            "attributed to Chuang Tzu himself; the Outer (8-22) and Miscellaneous "
            "(23-33) chapters were composed by his followers and editors.\n\n"
            "Source: Project Gutenberg eBook #59709 "
            "(https://www.gutenberg.org/ebooks/59709)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Traditional Chinese ink wash "
            "paintings (shuimo hua) depicting Taoist themes — particularly works from "
            "the Song Dynasty (960-1279) such as those by Liang Kai and Mu Qi, whose "
            "spare, spontaneous brushwork embodies the Taoist aesthetic. Also: "
            "illustrations from early printed editions of the Zhuangzi, and the "
            "tradition of literati painting (wenren hua) that drew deeply from "
            "Chuang Tzu's nature philosophy."
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "philosophy", "taoism", "chinese-philosophy", "classic",
            "public-domain", "full-text", "sacred-text", "mysticism",
        ],
        "roots": ["eastern-wisdom", "mysticism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei", "Akomolafe"],
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
    print(f"  L1: {l1} chapters, L2: {l2} emergent groups, L3: {l3} meta-categories")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    main()
