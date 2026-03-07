#!/usr/bin/env python3
"""
Parser for The Song Celestial / Bhagavad Gita by Sir Edwin Arnold (Gutenberg #2388).

Parses 18 chapters of verse into a grammar.json with:
  L1: Individual chapters (each a discourse between Krishna and Arjuna)
  L2: Thematic groupings (Yoga of Action, Knowledge, Devotion, etc.)
  L3: Meta-categories (The Crisis, The Teaching, The Vision, The Resolution)
"""

import json
import re
import sys
from pathlib import Path

SEEDS_DIR = Path(__file__).parent.parent / "seeds"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "bhagavad-gita"

# Chapter titles from the table of contents
CHAPTER_TITLES = {
    1: "The Distress of Arjuna",
    2: "The Book of Doctrines",
    3: "Virtue in Work",
    4: "The Religion of Knowledge",
    5: "Religion of Renouncing Works",
    6: "Religion by Self-Restraint",
    7: "Religion by Discernment",
    8: "Religion by Service of the Supreme",
    9: "Religion by the Kingly Knowledge and the Kingly Mystery",
    10: "Religion by the Heavenly Perfections",
    11: "The Manifesting of the One and Manifold",
    12: "Religion of Faith",
    13: "Religion by Separation of Matter and Spirit",
    14: "Religion by Separation from the Qualities",
    15: "Religion by Attaining the Supreme",
    16: "The Separateness of the Divine and Undivine",
    17: "Religion by the Threefold Faith",
    18: "Religion by Deliverance and Renunciation",
}

# Sanskrit chapter names (from the "HERE ENDETH" lines)
SANSKRIT_NAMES = {
    1: "Arjun-Vishad",
    2: "Sankhya-Yog",
    3: "Karma-Yog",
    4: "Jnana-Yog",
    5: "Karmasanyas-Yog",
    6: "Atmasanyam-Yog",
    7: "Vijnaana-Yog",
    8: "Aksharaparabrahma-Yog",
    9: "Rajavidya-Rajaguhya-Yog",
    10: "Vibhuti-Yog",
    11: "Vishwarupa-Darshan-Yog",
    12: "Bhakti-Yog",
    13: "Kshetra-Kshetragna-Vibhaga-Yog",
    14: "Gunatraya-Vibhaga-Yog",
    15: "Purushottama-Yog",
    16: "Daivasura-Sampad-Vibhaga-Yog",
    17: "Shraddhatraya-Vibhaga-Yog",
    18: "Mokshasanyasayog",
}

CHAPTER_KEYWORDS = {
    1: ["Arjuna", "distress", "war", "duty", "grief", "family", "battlefield", "Kurukshetra"],
    2: ["soul", "immortality", "duty", "Sankhya", "yoga", "detachment", "wisdom", "equanimity"],
    3: ["karma", "action", "work", "duty", "selfless service", "sacrifice", "desire"],
    4: ["knowledge", "wisdom", "incarnation", "sacrifice", "renunciation", "divine birth"],
    5: ["renunciation", "action", "liberation", "Sankhya", "yoga", "equanimity", "peace"],
    6: ["meditation", "self-restraint", "yoga", "mind", "discipline", "stillness", "Atman"],
    7: ["discernment", "divine nature", "illusion", "maya", "knowledge", "devotion"],
    8: ["supreme", "Brahman", "death", "rebirth", "devotion", "liberation", "Om"],
    9: ["kingly knowledge", "mystery", "devotion", "creation", "faith", "worship"],
    10: ["divine perfections", "manifestation", "glory", "vibhuti", "devotion"],
    11: ["universal form", "cosmic vision", "Vishwarupa", "terror", "awe", "omnipresence"],
    12: ["faith", "devotion", "bhakti", "love", "worship", "qualities of the devoted"],
    13: ["field", "knower", "matter", "spirit", "Prakriti", "Purusha", "discrimination"],
    14: ["three gunas", "sattva", "rajas", "tamas", "qualities", "transcendence"],
    15: ["supreme being", "Ashvattha tree", "Purushottama", "imperishable", "liberation"],
    16: ["divine nature", "demonic nature", "virtue", "vice", "discernment"],
    17: ["threefold faith", "sattva", "rajas", "tamas", "food", "worship", "charity"],
    18: ["renunciation", "liberation", "moksha", "duty", "surrender", "grace", "final teaching"],
}


def read_seed():
    """Read the seed file and strip Gutenberg header/footer."""
    path = SEEDS_DIR / "bhagavad-gita.txt"
    text = path.read_text(encoding="utf-8")

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        # Skip to end of that line
        start_idx = text.index('\n', start_idx) + 1
        text = text[start_idx:]

    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def strip_front_matter(text):
    """Remove title page, dedication, preface, and table of contents."""
    # The first chapter starts with "CHAPTER I"
    match = re.search(r'\nCHAPTER I\s*\n', text)
    if match:
        text = text[match.start():]
    return text


def strip_back_matter(text):
    """Remove footnotes after the last chapter."""
    # Footnotes start with [FN#1]
    match = re.search(r'\n\[FN#1\]', text)
    if match:
        text = text[:match.start()]
    return text


def parse_chapters(text):
    """Parse text into 18 chapters using CHAPTER markers."""
    chapters = {}

    # Find chapter start positions
    chapter_starts = []
    for match in re.finditer(r'^\s*CHAPTER\s+([IVXL]+)\s*$', text, re.MULTILINE):
        roman = match.group(1)
        num = roman_to_int(roman)
        chapter_starts.append((num, match.start()))

    lines = text.split('\n')

    # Convert positions to line numbers for easier extraction
    for idx, (num, start_pos) in enumerate(chapter_starts):
        if idx + 1 < len(chapter_starts):
            end_pos = chapter_starts[idx + 1][1]
        else:
            end_pos = len(text)

        chapter_text = text[start_pos:end_pos].strip()
        chapters[num] = chapter_text

    return chapters


def roman_to_int(s):
    """Convert roman numeral string to integer."""
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and roman_map.get(c, 0) < roman_map.get(s[i + 1], 0):
            result -= roman_map[c]
        else:
            result += roman_map.get(c, 0)
    return result


def clean_chapter_text(text, chapter_num):
    """Clean chapter text: remove header, HERE ENDETH footer, and footnote markers."""
    lines = text.split('\n')

    # Remove the "CHAPTER X" header line and blank lines after it
    content_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r'^CHAPTER\s+[IVXL]+$', stripped):
            content_start = i + 1
            continue
        break

    # Remove the "HERE ENDETH/ENDS" footer and everything after it
    content_end = len(lines)
    for i, line in enumerate(lines):
        if re.match(r'^\s*HERE END(ETH|S) CHAPTER', line.strip()):
            content_end = i
            break

    content_lines = lines[content_start:content_end]

    # Remove footnote references like [FN#1]
    cleaned = []
    for line in content_lines:
        line = re.sub(r'\[FN#\d+\]', '', line)
        cleaned.append(line)

    result = '\n'.join(cleaned).strip()

    # Clean up multiple blank lines
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result


def extract_speakers(text):
    """Extract speaker sections from chapter text.
    Returns list of (speaker, text) tuples."""
    # Speakers appear as "  Krishna." or "  Arjuna." or "  Sanjaya." etc.
    # on their own line (indented, with period)
    speakers = []
    current_speaker = None
    current_lines = []

    for line in text.split('\n'):
        stripped = line.strip()
        # Check if this is a speaker attribution line
        speaker_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)[\.:]\s*$', stripped)
        if speaker_match and stripped.rstrip('.:') in [
            'Krishna', 'Arjuna', 'Sanjaya', 'Dhritirashtra'
        ]:
            if current_speaker and current_lines:
                speakers.append((current_speaker, '\n'.join(current_lines).strip()))
            current_speaker = stripped.rstrip('.:')
            current_lines = []
        else:
            current_lines.append(line)

    if current_speaker and current_lines:
        speakers.append((current_speaker, '\n'.join(current_lines).strip()))

    # If no speakers found, treat entire text as narrative
    if not speakers:
        speakers = [("Narrative", text)]

    return speakers


def build_chapter_sections(chapter_num, text):
    """Build sections for a chapter item."""
    sections = {}

    # Clean and get the verse text
    cleaned = clean_chapter_text(text, chapter_num)

    # The main verse content
    sections["Verse"] = cleaned

    # Identify primary speakers
    speakers = extract_speakers(cleaned)
    speaker_names = list(set(s[0] for s in speakers))
    if len(speaker_names) > 1:
        sections["Speakers"] = ", ".join(speaker_names)

    # Add a reflection/meditation prompt
    title = CHAPTER_TITLES.get(chapter_num, "")
    reflections = {
        1: "Arjuna's paralysis before battle mirrors every moment when duty and compassion seem to conflict. When have you stood between two goods, unable to act?",
        2: "The soul is neither born nor dies. What changes when you stop identifying with what passes away?",
        3: "Act without attachment to outcomes. What would your work look like if you sought no reward?",
        4: "Whenever dharma declines, the divine arises. What form does wisdom take when it appears in your life?",
        5: "The wise see action in inaction and inaction in action. What does it mean to be still while the world moves?",
        6: "The mind is restless, turbulent, strong. Like the wind, it resists control. What is your practice of returning?",
        7: "Among thousands, hardly one strives for perfection. Among those who strive, hardly one knows the divine in truth. What draws you onward?",
        8: "Whatever you remember at the moment of death, that you become. What are you practicing remembering?",
        9: "I am the same to all beings. What does it mean to worship through the ordinary acts of offering, eating, and giving?",
        10: "The divine is the best among all categories. Where do you perceive the infinite showing through the finite?",
        11: "Arjuna sees the entire universe in the body of Krishna -- creation and destruction simultaneously. Can you hold both wonder and terror in a single gaze?",
        12: "Those who worship with faith, fixing their minds on the divine -- which path calls to you, the formless or the personal?",
        13: "The field and the knower of the field. Are you the body, the mind, or that which witnesses both?",
        14: "Sattva binds through happiness, rajas through action, tamas through negligence. Which quality dominates your current state?",
        15: "The cosmic tree has its roots above and branches below. What nourishes you from the invisible?",
        16: "Divine qualities lead to liberation, demonic to bondage. This is not about other people -- which tendencies live in you?",
        17: "Even faith has three qualities. What kind of faith sustains you -- is it luminous, passionate, or dark?",
        18: "Give up all dharmas and take refuge in Me alone. This is the ultimate surrender. What would it mean to truly let go?",
    }
    sections["Meditation"] = reflections.get(chapter_num, f"Sit with this teaching on {title.lower()}. What truth speaks to your condition?")

    return sections


def make_chapter_id(chapter_num):
    """Create a hyphenated ID for a chapter."""
    title = CHAPTER_TITLES.get(chapter_num, f"Chapter {chapter_num}")
    slug = title.lower()
    slug = re.sub(r"[''']s\b", "s", slug)
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return f"ch{chapter_num:02d}-{slug}"


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
                "sanskrit_name": SANSKRIT_NAMES.get(chapter_num, ""),
            },
        }
        items.append(item)

    return items


# L2 thematic groupings
L2_GROUPS = {
    "yoga-of-crisis": {
        "name": "The Yoga of Crisis",
        "category": "theme",
        "chapters": [1],
        "about": "Arjuna's existential crisis on the battlefield of Kurukshetra. Seeing his teachers, elders, and kinsmen arrayed for slaughter, the great warrior collapses in grief and lays down his weapons. This is the necessary shattering that precedes all teaching -- the moment when the old self can no longer sustain itself.",
        "keywords": ["crisis", "grief", "paralysis", "duty", "compassion", "battlefield"],
    },
    "yoga-of-knowledge": {
        "name": "The Yoga of Knowledge (Jnana)",
        "category": "theme",
        "chapters": [2, 4, 7, 13],
        "about": "Krishna's teaching on the nature of the Self, the immortality of the soul, the distinction between matter and spirit, and the path of wisdom. The Sankhya philosophy that forms the intellectual backbone of the Gita: the Self is neither born nor dies, the wise grieve neither for the living nor the dead, and true knowledge is knowing the field from the knower of the field.",
        "keywords": ["knowledge", "jnana", "soul", "immortality", "Sankhya", "discrimination", "wisdom"],
    },
    "yoga-of-action": {
        "name": "The Yoga of Selfless Action (Karma)",
        "category": "theme",
        "chapters": [3, 5],
        "about": "Krishna's revolutionary teaching on action without attachment. You have a right to work but never to its fruits. Perform every action as an offering. The path of karma yoga -- selfless service -- is not withdrawal from the world but engagement without ego. Renunciation is not abandoning action but abandoning the desire for results.",
        "keywords": ["karma", "action", "selfless service", "detachment", "duty", "sacrifice"],
    },
    "yoga-of-meditation": {
        "name": "The Yoga of Meditation and Self-Mastery",
        "category": "theme",
        "chapters": [6, 8],
        "about": "The practice of meditation, the discipline of the restless mind, and the path of concentrating consciousness on the Supreme at the hour of death. Krishna teaches Arjuna that the mind is indeed hard to control -- like the wind -- but through practice and dispassion it can be mastered.",
        "keywords": ["meditation", "mind", "discipline", "concentration", "practice", "Brahman"],
    },
    "yoga-of-devotion": {
        "name": "The Yoga of Devotion (Bhakti)",
        "category": "theme",
        "chapters": [9, 12],
        "about": "The path of love and surrender. Krishna reveals the royal secret and the royal science: whoever offers a leaf, a flower, a fruit, or water with devotion, that the Lord accepts. The devoted are the dearest to the divine. Bhakti is the most accessible path -- requiring not learning or austerity but simply a heart turned toward the infinite.",
        "keywords": ["devotion", "bhakti", "love", "surrender", "worship", "faith", "grace"],
    },
    "yoga-of-divine-glory": {
        "name": "The Yoga of Divine Manifestation",
        "category": "theme",
        "chapters": [10, 11],
        "about": "Krishna reveals his infinite perfections -- he is the best among all categories, the beginning, middle, and end of all beings. Then, at Arjuna's request, he reveals his cosmic form: the entire universe contained in a single divine body, simultaneously creating and destroying. Arjuna trembles in awe and begs to see the gentle form again.",
        "keywords": ["cosmic vision", "Vishwarupa", "divine glory", "manifestation", "awe", "terror"],
    },
    "yoga-of-the-gunas": {
        "name": "The Yoga of the Three Qualities",
        "category": "theme",
        "chapters": [14, 17],
        "about": "Krishna's teaching on the three gunas -- sattva (luminosity), rajas (passion), tamas (darkness) -- that bind the soul to nature. Everything in the created world partakes of these three qualities: food, worship, charity, even faith itself. Liberation comes through transcending all three, resting in the Self beyond qualities.",
        "keywords": ["gunas", "sattva", "rajas", "tamas", "qualities", "transcendence", "nature"],
    },
    "yoga-of-liberation": {
        "name": "The Yoga of Liberation and Surrender",
        "category": "theme",
        "chapters": [15, 16, 18],
        "about": "The culmination of the teaching. The cosmic tree of existence, the distinction between divine and demonic natures, and Krishna's final, most intimate instruction: 'Abandon all dharmas and take refuge in Me alone. I shall deliver you from all sin. Do not grieve.' The Gita ends not with philosophical argument but with an act of love.",
        "keywords": ["liberation", "moksha", "surrender", "grace", "renunciation", "divine nature"],
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
                "For Readers": f"This group of {len(composite_ids)} chapters explores a unified dimension of Krishna's teaching. Read them together to follow the thread of {info['name'].lower()}, or enter through whichever chapter title speaks to you.",
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
    "meta-the-crisis": {
        "name": "The Crisis: Why the Teaching Begins",
        "category": "meta",
        "l2_ids": ["yoga-of-crisis"],
        "about": "Every genuine spiritual teaching begins with a crisis. Arjuna's breakdown on the battlefield is not weakness but the necessary dissolution of his former self-understanding. He cannot fight because his old categories of friend and enemy, right and wrong, have collapsed. Into this void, Krishna speaks.",
        "keywords": ["crisis", "beginning", "shattering", "necessity"],
    },
    "meta-the-teaching": {
        "name": "The Teaching: Six Paths to the One",
        "category": "meta",
        "l2_ids": [
            "yoga-of-knowledge",
            "yoga-of-action",
            "yoga-of-meditation",
            "yoga-of-devotion",
            "yoga-of-the-gunas",
        ],
        "about": "The heart of the Gita: Krishna offers not one path but many -- knowledge for the philosophical, selfless action for the active, meditation for the contemplative, devotion for the loving, and the discipline of the gunas for those who would understand their own nature. All paths converge on the same summit. The genius of the Gita is its radical inclusiveness.",
        "keywords": ["teaching", "paths", "yoga", "inclusiveness", "dharma"],
    },
    "meta-the-vision": {
        "name": "The Vision: Reality Unveiled",
        "category": "meta",
        "l2_ids": ["yoga-of-divine-glory"],
        "about": "At the climactic centre of the poem, Krishna removes the veil. Arjuna sees the cosmic form -- all beings flowing into the mouth of Time, creation and dissolution happening simultaneously. This is the direct encounter with the Real that shatters all concepts, even those Krishna has just taught. After this, only surrender remains.",
        "keywords": ["vision", "cosmic form", "revelation", "Vishwarupa", "direct experience"],
    },
    "meta-the-resolution": {
        "name": "The Resolution: Surrender and Return",
        "category": "meta",
        "l2_ids": ["yoga-of-liberation"],
        "about": "The teaching culminates not in escape from the world but in return to it, transformed. Krishna's final instruction is the most radical: abandon all rules and simply surrender. Arjuna's last words echo across millennia: 'My doubt is fled. According to Thy word, so will I do.' He picks up his bow.",
        "keywords": ["resolution", "surrender", "return", "action", "grace", "freedom"],
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
                "How to Use": "The Bhagavad Gita unfolds as a drama in four acts: crisis, teaching, vision, and resolution. Begin wherever you are drawn. If you are in crisis, start with Chapter 1. If you seek understanding, enter the teaching. If you are ready for direct encounter, read Chapter 11. If you seek peace, go to Chapter 18.",
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
                    "name": "Sir Edwin Arnold",
                    "date": "1885 (translation), 1900 (this edition)",
                    "note": "Translated from the Sanskrit text. Published by Truslove, Hanson & Comba, Ltd., New York.",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2000",
                    "note": "Digitized text, eBook #2388. Credits: J. C. Byers. HTML version by Al Haines.",
                },
            ],
        },
        "name": "The Bhagavad Gita (Song Celestial)",
        "description": (
            "The Bhagavad Gita ('Song of God'), translated as 'The Song Celestial' by Sir Edwin Arnold (1885). "
            "A 700-verse discourse between Prince Arjuna and the god Krishna on the battlefield of Kurukshetra, "
            "embedded within the Mahabharata epic. In 18 chapters, Krishna reveals the paths of knowledge, "
            "action, meditation, and devotion, culminating in the vision of his cosmic form and the teaching "
            "of ultimate surrender. The most widely read and influential text in Hindu philosophy.\n\n"
            "Source: Project Gutenberg eBook #2388 (https://www.gutenberg.org/ebooks/2388)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Indian miniature paintings of the Bhagavad Gita "
            "(Rajasthani and Pahari schools, 17th-19th century), particularly the Kurukshetra battle scenes "
            "and Krishna revealing his Vishwarupa form. Also: illustrations from Edwin Arnold's 'The Light of Asia' "
            "and Victorian-era Orientalist depictions of the Mahabharata."
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["hinduism", "sacred-text", "philosophy", "yoga", "bhakti", "dharma", "verse", "epic"],
        "roots": ["eastern-wisdom"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei", "Linehan", "Akomolafe"],
        "worldview": "non-dual",
        "items": all_items,
    }

    return grammar


def main():
    print("Reading seed text...")
    text = read_seed()

    print("Stripping front matter...")
    text = strip_front_matter(text)

    print("Stripping back matter...")
    text = strip_back_matter(text)

    print("Parsing chapters...")
    chapters = parse_chapters(text)
    print(f"  Found {len(chapters)} chapters")

    if len(chapters) != 18:
        print(f"  WARNING: Expected 18 chapters, found {len(chapters)}", file=sys.stderr)
        missing = [i for i in range(1, 19) if i not in chapters]
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
