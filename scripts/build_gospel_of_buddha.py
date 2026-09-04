#!/usr/bin/env python3
"""
Parser for The Gospel of Buddha by Paul Carus (Gutenberg #35895).

Parses 100 chapters into a grammar.json with:
  L1: Individual chapters (teachings, stories, sermons)
  L2: Life-phase groups + thematic groups
  L3: Meta-categories (Life of the Buddha, Teachings & Doctrine, Parables & Stories)
"""

import json
import re
import sys
from pathlib import Path

SEEDS_DIR = Path(__file__).parent.parent / "seeds"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "gospel-of-buddha"

# Table of contents structure from the text
# Section -> (start_chapter, end_chapter, section_title)
BOOK_SECTIONS = {
    "introduction": {
        "title": "Introduction",
        "chapters": [1, 2, 3],
    },
    "becomes-buddha": {
        "title": "Prince Siddhattha Becomes Buddha",
        "chapters": list(range(4, 15)),  # IV-XIV
    },
    "foundation": {
        "title": "The Foundation of the Kingdom of Righteousness",
        "chapters": list(range(15, 30)),  # XV-XXIX
    },
    "consolidation": {
        "title": "Consolidation of the Buddha's Religion",
        "chapters": list(range(30, 48)),  # XXX-XLVII
    },
    "teacher": {
        "title": "The Teacher",
        "chapters": list(range(48, 62)),  # XLVIII-LXI
    },
    "parables": {
        "title": "Parables and Stories",
        "chapters": list(range(62, 88)),  # LXII-LXXXVII
    },
    "last-days": {
        "title": "The Last Days",
        "chapters": list(range(88, 98)),  # LXXXVIII-XCVII
    },
    "conclusion": {
        "title": "Conclusion",
        "chapters": [98, 99, 100],  # XCVIII-C
    },
}

# Chapter titles from the table of contents
CHAPTER_TITLES = {
    1: "Rejoice!",
    2: "Samsara and Nirvana",
    3: "Truth the Saviour",
    4: "The Bodhisatta's Birth",
    5: "The Ties of Life",
    6: "The Three Woes",
    7: "The Bodhisatta's Renunciation",
    8: "King Bimbisara",
    9: "The Bodhisatta's Search",
    10: "Uruvela, the Place of Mortification",
    11: "Mara, the Evil One",
    12: "Enlightenment",
    13: "The First Converts",
    14: "Brahma's Request",
    15: "Upaka",
    16: "The Sermon at Benares",
    17: "The Sangha",
    18: "Yasa, the Youth of Benares",
    19: "Kassapa",
    20: "The Sermon at Rajagaha",
    21: "The King's Gift",
    22: "Sariputta and Moggallana",
    23: "Anathapindika",
    24: "The Sermon on Charity",
    25: "Jetavana",
    26: "The Three Characteristics and the Uncreate",
    27: "The Buddha's Father",
    28: "Yasodhara",
    29: "Rahula",
    30: "Jivaka, the Physician",
    31: "The Buddha's Parents Attain Nirvana",
    32: "Women Admitted to the Sangha",
    33: "The Bhikkhus' Conduct Toward Women",
    34: "Visakha",
    35: "The Uposatha and Patimokkha",
    36: "The Schism",
    37: "The Re-establishment of Concord",
    38: "The Bhikkhus Rebuked",
    39: "Devadatta",
    40: "Name and Form",
    41: "The Goal",
    42: "Miracles Forbidden",
    43: "The Vanity of Worldliness",
    44: "Secrecy and Publicity",
    45: "The Annihilation of Suffering",
    46: "Avoiding the Ten Evils",
    47: "The Preacher's Mission",
    48: "The Dhammapada",
    49: "The Two Brahmans",
    50: "Guard the Six Quarters",
    51: "Simha's Question Concerning Annihilation",
    52: "All Existence is Spiritual",
    53: "Identity and Non-Identity",
    54: "The Buddha Omnipresent",
    55: "One Essence, One Law, One Aim",
    56: "The Lesson Given to Rahula",
    57: "The Sermon on Abuse",
    58: "The Buddha Replies to the Deva",
    59: "Words of Instruction",
    60: "Amitabha",
    61: "The Teacher Unknown",
    62: "Parables",
    63: "The Widow's Two Mites and the Parable of the Three Merchants",
    64: "The Man Born Blind",
    65: "The Lost Son",
    66: "The Giddy Fish",
    67: "The Cruel Crane Outwitted",
    68: "Four Kinds of Merit",
    69: "The Light of the World",
    70: "Luxurious Living",
    71: "The Communication of Bliss",
    72: "The Listless Fool",
    73: "Rescue in the Desert",
    74: "The Sower",
    75: "The Outcast",
    76: "The Woman at the Well",
    77: "The Peacemaker",
    78: "The Hungry Dog",
    79: "The Despot",
    80: "Vasavadatta",
    81: "The Marriage-Feast in Jambunada",
    82: "A Party in Search of a Thief",
    83: "In the Realm of Yamaraja",
    84: "The Mustard Seed",
    85: "Following the Master Over the Stream",
    86: "The Sick Bhikkhu",
    87: "The Patient Elephant",
    88: "The Conditions of Welfare",
    89: "Sariputta's Faith",
    90: "Pataliputta",
    91: "The Mirror of Truth",
    92: "Ambapali",
    93: "The Buddha's Farewell Address",
    94: "The Buddha Announces His Death",
    95: "Chunda, the Smith",
    96: "Metteyya",
    97: "The Buddha's Final Entering Into Nirvana",
    98: "The Three Personalities of the Buddha",
    99: "The Purpose of Being",
    100: "The Praise of All the Buddhas",
}

# Keywords for each chapter
CHAPTER_KEYWORDS = {
    1: ["rejoice", "salvation", "truth", "glad tidings"],
    2: ["samsara", "nirvana", "impermanence", "self", "truth", "immortality"],
    3: ["truth", "consciousness", "evolution", "karma", "dharma"],
    4: ["birth", "Siddhattha", "Lumbini", "Maya", "Suddhodana", "prophecy"],
    5: ["youth", "marriage", "Yasodhara", "princely life"],
    6: ["suffering", "old age", "sickness", "death", "impermanence"],
    7: ["renunciation", "great departure", "asceticism", "Channa"],
    8: ["Bimbisara", "Rajagaha", "kingship"],
    9: ["search", "teachers", "asceticism", "Alara", "Uddaka"],
    10: ["mortification", "fasting", "middle way", "Uruvela"],
    11: ["Mara", "temptation", "evil", "desire", "resolve"],
    12: ["enlightenment", "bodhi tree", "four noble truths", "awakening"],
    13: ["first converts", "Trapusha", "Bhallika", "teaching"],
    14: ["Brahma", "compassion", "preaching", "dharma wheel"],
    15: ["Upaka", "proclamation", "Tathagata"],
    16: ["Benares", "four noble truths", "eightfold path", "first sermon", "dharma"],
    17: ["sangha", "community", "ordination", "bhikkhus"],
    18: ["Yasa", "conversion", "lay disciple", "renunciation"],
    19: ["Kassapa", "fire worship", "conversion", "Jatilas"],
    20: ["Rajagaha", "sermon", "fire sermon"],
    21: ["gift", "Bamboo Grove", "Veluvana", "generosity"],
    22: ["Sariputta", "Moggallana", "chief disciples", "Assaji"],
    23: ["Anathapindika", "generosity", "lay supporter"],
    24: ["charity", "giving", "merit", "compassion"],
    25: ["Jetavana", "monastery", "gift", "dedication"],
    26: ["impermanence", "suffering", "non-self", "uncreate", "nirvana"],
    27: ["father", "Suddhodana", "family", "return home"],
    28: ["Yasodhara", "wife", "devotion", "reunion"],
    29: ["Rahula", "son", "ordination", "inheritance"],
    30: ["Jivaka", "physician", "healing", "medicine"],
    31: ["parents", "death", "nirvana", "grief", "impermanence"],
    32: ["women", "ordination", "Pajapati", "equality"],
    33: ["conduct", "women", "discipline", "mindfulness"],
    34: ["Visakha", "lay supporter", "generosity", "devotion"],
    35: ["observance", "rules", "Uposatha", "Patimokkha", "discipline"],
    36: ["schism", "conflict", "division", "community"],
    37: ["concord", "reconciliation", "peace", "harmony"],
    38: ["rebuke", "mindfulness", "discipline", "quarreling"],
    39: ["Devadatta", "betrayal", "jealousy", "evil"],
    40: ["name", "form", "dependent origination", "consciousness"],
    41: ["goal", "nirvana", "liberation", "purpose"],
    42: ["miracles", "truth", "teaching", "wisdom"],
    43: ["worldliness", "vanity", "attachment", "renunciation"],
    44: ["secrecy", "publicity", "sincerity", "integrity"],
    45: ["suffering", "annihilation", "four noble truths", "liberation"],
    46: ["ten evils", "ethics", "morality", "right action"],
    47: ["preaching", "mission", "compassion", "teaching"],
    48: ["Dhammapada", "verses", "wisdom", "truth", "path"],
    49: ["Brahmans", "caste", "equality", "true brahman"],
    50: ["six quarters", "family", "social duties", "relationships"],
    51: ["annihilation", "nihilism", "middle way", "Simha"],
    52: ["existence", "spiritual", "mind", "consciousness"],
    53: ["identity", "non-identity", "self", "continuity"],
    54: ["omnipresence", "Buddha nature", "dharma body"],
    55: ["unity", "essence", "law", "purpose"],
    56: ["Rahula", "lesson", "truth", "lying"],
    57: ["abuse", "patience", "equanimity", "response"],
    58: ["deva", "questions", "wisdom", "dialogue"],
    59: ["instruction", "practice", "mindfulness", "guidance"],
    60: ["Amitabha", "infinite light", "Pure Land", "devotion"],
    61: ["teacher", "unknown", "dharma", "selflessness"],
    62: ["parables", "allegory", "teaching stories"],
    63: ["generosity", "charity", "widow", "merchants"],
    64: ["blindness", "sight", "wisdom", "ignorance"],
    65: ["lost son", "return", "compassion", "recognition"],
    66: ["fish", "desire", "foolishness", "attachment"],
    67: ["crane", "lobster", "outwitting", "cunning"],
    68: ["merit", "sacrifice", "compassion", "true worth"],
    69: ["light", "world", "darkness", "wisdom"],
    70: ["luxury", "attachment", "simplicity", "renunciation"],
    71: ["bliss", "sharing", "communication", "joy"],
    72: ["fool", "laziness", "mindfulness", "effort"],
    73: ["desert", "rescue", "perseverance", "leadership"],
    74: ["sowing", "harvest", "karma", "effort"],
    75: ["outcast", "caste", "equality", "true nobility"],
    76: ["woman", "well", "equality", "caste", "compassion"],
    77: ["peace", "conflict resolution", "harmony"],
    78: ["hungry dog", "attachment", "desire", "contentment"],
    79: ["despot", "tyranny", "justice", "karma"],
    80: ["Vasavadatta", "courtesan", "conversion", "renunciation"],
    81: ["marriage", "Jambunada", "community", "celebration"],
    82: ["thief", "self", "seeking", "wisdom"],
    83: ["Yamaraja", "death", "judgment", "karma", "afterlife"],
    84: ["mustard seed", "grief", "death", "Kisa Gotami", "universal suffering"],
    85: ["faith", "stream", "following", "trust"],
    86: ["sick bhikkhu", "compassion", "care", "service"],
    87: ["elephant", "patience", "endurance", "solitude"],
    88: ["welfare", "conditions", "prosperity", "community"],
    89: ["Sariputta", "faith", "devotion", "trust"],
    90: ["Pataliputta", "prophecy", "city", "future"],
    91: ["mirror", "truth", "self-reflection", "stream-entry"],
    92: ["Ambapali", "courtesan", "generosity", "conversion"],
    93: ["farewell", "last teaching", "self-reliance", "impermanence"],
    94: ["death", "announcement", "earthquake", "passing"],
    95: ["Chunda", "last meal", "compassion", "merit"],
    96: ["Metteyya", "future Buddha", "prophecy", "hope"],
    97: ["parinibbana", "death", "final nirvana", "passing", "funeral"],
    98: ["three bodies", "Buddha nature", "dharma body", "transformation"],
    99: ["purpose", "being", "meaning", "existence"],
    100: ["praise", "Buddhas", "devotion", "reverence"],
}


def int_to_roman(num):
    """Convert integer to roman numeral string."""
    val = [100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ['C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    roman = ''
    for i, v in enumerate(val):
        while num >= v:
            roman += syms[i]
            num -= v
    return roman


def roman_to_int(s):
    """Convert roman numeral string to integer."""
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and roman_map[c] < roman_map[s[i + 1]]:
            result -= roman_map[c]
        else:
            result += roman_map[c]
    return result


def read_seed():
    """Read the seed file and strip Gutenberg header/footer."""
    path = SEEDS_DIR / "gospel-of-buddha.txt"
    text = path.read_text(encoding="utf-8")

    # Strip Gutenberg header
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE GOSPEL OF BUDDHA, COMPILED FROM ANCIENT RECORDS ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE GOSPEL OF BUDDHA, COMPILED FROM ANCIENT RECORDS ***"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def strip_front_matter(text):
    """Remove preface, pronunciation guide, and table of contents."""
    # Find the start of the actual text content — "INTRODUCTION." section header
    # We look for the line "INTRODUCTION." which precedes chapter I
    match = re.search(r'\nINTRODUCTION\.\s*\n', text)
    if match:
        text = text[match.start():]
    return text


def strip_back_matter(text):
    """Remove Table of Reference, Glossary, Index at the end."""
    # The back matter starts with "TABLE OF REFERENCE."
    match = re.search(r'\nTABLE OF REFERENCE\.?\s*\n', text)
    if match:
        text = text[:match.start()]
    return text


def parse_chapters(text):
    """
    Parse text into chapters. Each chapter starts with a roman numeral.
    Returns dict of {chapter_num: chapter_text}.
    """
    chapters = {}

    # Build list of all roman numerals I to C
    all_romans = [int_to_roman(i) for i in range(1, 101)]

    # Find chapter boundaries
    # Chapters can start as:
    # 1) Roman numeral alone on a line: "^VII.$" or "^XX$" (some lack period)
    # 2) Roman numeral with title on same line: "^IV. THE BODHISATTA'S BIRTH$"
    # Pattern: a line that starts with a valid roman numeral, optionally followed by period and title
    chapter_positions = []

    lines = text.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        # Check if line is a roman numeral (with optional period, with optional title)
        # Must match a known roman numeral exactly
        match = re.match(r'^([IVXLC]+)\.?\s*(.*?)$', stripped)
        if match:
            roman_str = match.group(1)
            if roman_str in all_romans:
                num = roman_to_int(roman_str)
                if 1 <= num <= 100:
                    # Make sure this isn't a section header like "INTRODUCTION."
                    # and isn't part of running text
                    # Check: previous line should be blank or this is near start
                    if i > 0 and lines[i - 1].strip() == '':
                        # Also check that following lines aren't blank + uppercase title
                        # (or the title is on the same line)
                        remaining = match.group(2).strip()
                        if remaining:
                            # Title on same line (like "IV. THE BODHISATTA'S BIRTH")
                            chapter_positions.append((num, i))
                        else:
                            # Roman numeral alone — next non-blank line should be the title
                            chapter_positions.append((num, i))

    # Sort by position and deduplicate
    # Some chapter numbers might appear in the TOC too — we only want the actual chapter starts
    # Filter: keep only the ones that are in order (skip TOC references)
    filtered = []
    expected = 1
    for num, pos in chapter_positions:
        if num == expected:
            filtered.append((num, pos))
            expected = num + 1
        elif num > expected and not filtered:
            # We might have missed some, try to recover
            pass

    # If filtering missed chapters, try a more lenient approach
    if len(filtered) < 90:
        # Use all positions but take the last occurrence of each number
        by_num = {}
        for num, pos in chapter_positions:
            if num not in by_num or pos > by_num[num]:
                by_num[num] = pos
        filtered = sorted(by_num.items())

    # Extract chapter texts
    for idx, (num, start_line) in enumerate(filtered):
        if idx + 1 < len(filtered):
            end_line = filtered[idx + 1][1]
        else:
            end_line = len(lines)

        chapter_text = '\n'.join(lines[start_line:end_line]).strip()
        chapters[num] = chapter_text

    return chapters


def clean_chapter_text(text, chapter_num):
    """
    Clean chapter text: remove the roman numeral header and title,
    strip verse numbers, and return clean teaching text.
    """
    lines = text.split('\n')

    # Remove the first few lines (roman numeral, blank lines, title)
    content_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        # Skip lines that are the roman numeral
        if re.match(r'^[IVXLC]+\.?\s*$', stripped):
            content_start = i + 1
            continue
        # Skip lines that are ALL CAPS (title or section header)
        if stripped == stripped.upper() and len(stripped) > 2 and not stripped[0].isdigit():
            content_start = i + 1
            continue
        # Skip [Illustration] lines
        if stripped.startswith('[Illustration'):
            content_start = i + 1
            continue
        break

    content_lines = lines[content_start:]

    # Remove [Illustration] markers throughout
    content_lines = [l for l in content_lines if not l.strip().startswith('[Illustration')]

    # Remove right-aligned verse numbers (numbers at the end of lines after spaces)
    cleaned = []
    for line in content_lines:
        # Verse numbers appear as spaces + number at end of line
        cleaned_line = re.sub(r'\s{2,}\d+\s*$', '', line)
        cleaned.append(cleaned_line)

    # Join and clean up
    result = '\n'.join(cleaned).strip()

    # Remove section header lines that appear between chapters (like "PRINCE SIDDHATTHA BECOMES BUDDHA.")
    section_headers = [
        "PRINCE SIDDHATTHA BECOMES BUDDHA.",
        "PRINCE SIDDHATTHA BECOMES BUDDHA",
        "THE FOUNDATION OF THE KINGDOM OF RIGHTEOUSNESS.",
        "THE FOUNDATION OF THE KINGDOM OF RIGHTEOUSNESS",
        "CONSOLIDATION OF THE BUDDHA'S RELIGION.",
        "CONSOLIDATION OF THE BUDDHA'S RELIGION",
        "THE TEACHER.",
        "PARABLES AND STORIES.",
        "PARABLES AND STORIES",
        "THE LAST DAYS.",
        "THE LAST DAYS",
        "CONCLUSION.",
        "CONCLUSION",
        "INTRODUCTION.",
    ]
    for header in section_headers:
        result = result.replace(header, '').strip()

    # Clean up multiple blank lines
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result


def get_section_for_chapter(chapter_num):
    """Return which book section a chapter belongs to."""
    for section_id, info in BOOK_SECTIONS.items():
        if chapter_num in info["chapters"]:
            return section_id, info["title"]
    return "unknown", "Unknown"


def make_chapter_id(chapter_num):
    """Create a hyphenated ID for a chapter."""
    title = CHAPTER_TITLES.get(chapter_num, f"Chapter {chapter_num}")
    # Create ID from title
    slug = title.lower()
    slug = re.sub(r"[''']s\b", "s", slug)  # possessives
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return f"ch{chapter_num:02d}-{slug}"


def determine_teaching_type(chapter_num, text):
    """Determine what kind of sections to use based on chapter content."""
    if chapter_num in range(62, 88):
        return "parable"
    elif chapter_num in [1, 2, 3, 98, 99, 100]:
        return "philosophical"
    elif chapter_num in range(4, 15):
        return "narrative"
    elif chapter_num in [16, 20, 24, 26, 40, 45, 46, 48]:
        return "sermon"
    else:
        return "teaching"


def build_sections(chapter_num, text, teaching_type):
    """Build the sections dict for a chapter item."""
    sections = {}

    if teaching_type == "parable":
        sections["Story"] = text
        # Add a brief reflection prompt
        title = CHAPTER_TITLES.get(chapter_num, "")
        sections["Reflection"] = f"What does this story of {title.lower()} reveal about the nature of suffering, wisdom, or compassion? How might its lesson apply to your own life?"

    elif teaching_type == "narrative":
        sections["Story"] = text
        sections["Reflection"] = "What does this episode in the Buddha's journey reveal about the path from suffering to awakening?"

    elif teaching_type == "sermon":
        sections["Teaching"] = text
        sections["Reflection"] = "How do these words challenge your understanding? What would it mean to put this teaching into practice today?"

    elif teaching_type == "philosophical":
        sections["Teaching"] = text
        sections["Reflection"] = "Sit with these words. What truth resonates most deeply?"

    else:
        sections["Teaching"] = text
        sections["Reflection"] = "What insight does this passage offer for your own path?"

    return sections


def build_l1_items(chapters):
    """Build L1 items from parsed chapters."""
    items = []

    for chapter_num in sorted(chapters.keys()):
        raw_text = chapters[chapter_num]
        text = clean_chapter_text(raw_text, chapter_num)

        if not text.strip():
            print(f"  Warning: Chapter {chapter_num} has no content after cleaning", file=sys.stderr)
            continue

        section_id, section_title = get_section_for_chapter(chapter_num)
        teaching_type = determine_teaching_type(chapter_num, text)
        sections = build_sections(chapter_num, text, teaching_type)

        item = {
            "id": make_chapter_id(chapter_num),
            "name": CHAPTER_TITLES.get(chapter_num, f"Chapter {chapter_num}"),
            "sort_order": chapter_num - 1,
            "category": section_id,
            "level": 1,
            "sections": sections,
            "keywords": CHAPTER_KEYWORDS.get(chapter_num, []),
            "metadata": {
                "chapter_number": chapter_num,
                "roman_numeral": int_to_roman(chapter_num),
                "book_section": section_title,
            },
        }
        items.append(item)

    return items


# L2 groupings: life phases and thematic groups
L2_GROUPS = {
    # Life phase groups
    "phase-birth-and-youth": {
        "name": "Birth and Youth of the Bodhisatta",
        "category": "life-phase",
        "chapters": [4, 5, 6],
        "about": "The miraculous birth of Prince Siddhattha at Lumbini, his sheltered youth in the palace of King Suddhodana, and his first encounters with the suffering of old age, sickness, and death that would propel him toward renunciation.",
        "keywords": ["birth", "youth", "prince", "palace", "prophecy", "three woes"],
    },
    "phase-renunciation-and-search": {
        "name": "The Great Renunciation and Search",
        "category": "life-phase",
        "chapters": [7, 8, 9, 10, 11],
        "about": "Siddhattha leaves the palace, encounters teachers and ascetics, practices severe mortification at Uruvela, and confronts Mara the tempter. The journey from privilege through suffering toward the middle way.",
        "keywords": ["renunciation", "search", "asceticism", "mortification", "Mara", "temptation"],
    },
    "phase-awakening": {
        "name": "Enlightenment and First Teaching",
        "category": "life-phase",
        "chapters": [12, 13, 14, 15, 16],
        "about": "The Bodhisatta attains supreme enlightenment beneath the Bodhi tree, makes his first converts, and at Brahma's request begins to teach the Dharma. The Sermon at Benares sets the Wheel of the Law in motion with the Four Noble Truths and the Eightfold Path.",
        "keywords": ["enlightenment", "awakening", "Bodhi tree", "first sermon", "four noble truths"],
    },
    "phase-building-sangha": {
        "name": "Building the Sangha",
        "category": "life-phase",
        "chapters": [17, 18, 19, 20, 21, 22, 23, 24, 25],
        "about": "The Buddha establishes the monastic community, converts Kassapa and the fire-worshippers, wins the patronage of kings and wealthy merchants, and establishes the great monasteries at Veluvana and Jetavana.",
        "keywords": ["sangha", "community", "ordination", "conversion", "monastery"],
    },
    "phase-family-reunion": {
        "name": "Return to Family",
        "category": "life-phase",
        "chapters": [27, 28, 29, 30, 31],
        "about": "The Buddha returns to Kapilavatthu to visit his father Suddhodana, reunites with his wife Yasodhara and son Rahula, and witnesses his parents' attainment of Nirvana. The personal and the universal dharma intertwine.",
        "keywords": ["family", "father", "wife", "son", "return", "Kapilavatthu"],
    },
    "phase-sangha-governance": {
        "name": "Governing the Sangha",
        "category": "life-phase",
        "chapters": [32, 33, 34, 35, 36, 37, 38, 39],
        "about": "The Buddha addresses the practical challenges of community life: admitting women to the order, establishing rules of conduct, healing schisms, dealing with Devadatta's treachery, and maintaining harmony among the bhikkhus.",
        "keywords": ["sangha", "rules", "women", "schism", "Devadatta", "discipline"],
    },
    "phase-final-days": {
        "name": "The Final Days and Parinibbana",
        "category": "life-phase",
        "chapters": [88, 89, 90, 91, 92, 93, 94, 95, 96, 97],
        "about": "The Buddha's last journey from Rajagaha to Kusinara. He gives his farewell address, announces his approaching death, takes his final meal from Chunda the smith, prophesies the coming of Metteyya, and enters final Nirvana. His last words: 'Work out your salvation with diligence.'",
        "keywords": ["death", "parinibbana", "farewell", "last days", "Metteyya", "funeral"],
    },
    # Thematic groups
    "theme-core-doctrine": {
        "name": "Core Doctrine and Philosophy",
        "category": "theme",
        "chapters": [1, 2, 3, 26, 40, 41, 45, 51, 52, 53, 54, 55, 98, 99, 100],
        "about": "The foundational philosophical teachings of the Buddha: the nature of Samsara and Nirvana, the Three Characteristics (impermanence, suffering, non-self), dependent origination, the annihilation of suffering, and the ultimate nature of the Buddha as truth itself.",
        "keywords": ["philosophy", "doctrine", "samsara", "nirvana", "non-self", "dependent origination"],
    },
    "theme-ethics-conduct": {
        "name": "Ethics and Right Conduct",
        "category": "theme",
        "chapters": [24, 33, 42, 43, 44, 46, 47, 48, 50, 56, 57, 59],
        "about": "Practical ethical teachings: the ten evils to avoid, the sermon on charity, the six quarters of social duty, instructions on right speech, the vanity of worldliness, and the path of moral conduct in daily life.",
        "keywords": ["ethics", "morality", "conduct", "charity", "duty", "ten evils"],
    },
    "theme-parables-stories": {
        "name": "Parables and Teaching Stories",
        "category": "theme",
        "chapters": list(range(62, 88)),
        "about": "Twenty-six stories and parables used by the Buddha to illuminate the dharma: the mustard seed teaching grief, the cruel crane outwitted, the lost son returning, the sower and his seeds, rescue in the desert, and many more. Each story makes an abstract truth vivid and memorable.",
        "keywords": ["parables", "stories", "allegory", "teaching", "fables"],
    },
    "theme-conversion-devotion": {
        "name": "Conversion and Devotion",
        "category": "theme",
        "chapters": [13, 14, 15, 18, 19, 22, 23, 25, 34, 58, 60, 61, 80, 92],
        "about": "Stories of people encountering the Buddha and being transformed: from the first converts Trapusha and Bhallika, through the great disciples Sariputta and Moggallana, to courtesans like Vasavadatta and Ambapali. Each conversion reveals a different facet of the dharma's power to awaken.",
        "keywords": ["conversion", "devotion", "faith", "discipleship", "transformation"],
    },
    "theme-compassion-service": {
        "name": "Compassion and Service",
        "category": "theme",
        "chapters": [30, 68, 69, 71, 75, 76, 77, 84, 86, 95],
        "about": "The Buddha's teachings on compassion in action: caring for the sick, serving others, breaking down barriers of caste and gender, comforting the grieving Kisa Gotami, and the radical equality at the heart of the dharma.",
        "keywords": ["compassion", "service", "equality", "caste", "kindness", "grief"],
    },
}


def build_l2_items(l1_items):
    """Build L2 emergence items from L1 chapters."""
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
                "For Readers": f"This group of {len(composite_ids)} chapters can be read together as a unified arc. Read them in sequence to follow the thread, or dip into individual chapters that call to you.",
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
    "meta-life-of-buddha": {
        "name": "The Life of the Buddha",
        "category": "meta",
        "l2_ids": [
            "phase-birth-and-youth",
            "phase-renunciation-and-search",
            "phase-awakening",
            "phase-building-sangha",
            "phase-family-reunion",
            "phase-sangha-governance",
            "phase-final-days",
        ],
        "about": "The complete arc of Siddhattha Gotama's life, from miraculous birth to final Nirvana. Seven phases trace the journey from prince to ascetic to awakened teacher to aging sage entering the deathless. This is not merely biography but a map of the spiritual path itself.",
        "keywords": ["biography", "life", "Buddha", "journey", "awakening", "path"],
    },
    "meta-teachings-doctrine": {
        "name": "Teachings and Doctrine",
        "category": "meta",
        "l2_ids": [
            "theme-core-doctrine",
            "theme-ethics-conduct",
            "theme-conversion-devotion",
            "theme-compassion-service",
        ],
        "about": "The Buddha's complete teaching system: foundational philosophy (Four Noble Truths, dependent origination, non-self), practical ethics (the ten evils, social duties, right speech), the transformative power of conversion and devotion, and the radical compassion that breaks all barriers.",
        "keywords": ["teachings", "doctrine", "dharma", "philosophy", "ethics", "compassion"],
    },
    "meta-parables": {
        "name": "The Buddha as Storyteller",
        "category": "meta",
        "l2_ids": [
            "theme-parables-stories",
        ],
        "about": "The Buddha was a master storyteller who used vivid narratives, fables, and parables to make abstract truths tangible. From the mustard seed to the cruel crane, from the lost son to rescue in the desert, these twenty-six stories reveal the dharma through drama, humor, and unforgettable imagery.",
        "keywords": ["stories", "parables", "narrative", "teaching", "allegory"],
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
                "How to Use": "Begin with whichever meta-category draws you. Within each, the L2 groups provide focused pathways. Within those, individual chapters offer daily contemplation.",
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
    print(f"  Built {len(l2_items)} L2 items (groups)")

    l3_items = build_l3_items(l1_items, l2_items)
    print(f"  Built {len(l3_items)} L3 items (meta-categories)")

    all_items = l1_items + l2_items + l3_items

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Paul Carus",
                    "date": "1894 (first edition), 1915 (illustrated edition)",
                    "note": "Compiled from ancient Buddhist records. Published by The Open Court Publishing Company, Chicago.",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2011",
                    "note": "Digitized text, eBook #35895. Credits: Andrea Ball & Marc D'Hooghe.",
                },
            ],
        },
        "name": "The Gospel of Buddha",
        "description": (
            "The Gospel of Buddha, compiled from ancient records by Paul Carus (1894, illustrated edition 1915). "
            "A harmonized retelling of the life and teachings of Siddhattha Gotama drawn from Pali, Sanskrit, and Chinese sources. "
            "One hundred chapters trace the arc from the Bodhisatta's birth through enlightenment, the founding of the Sangha, "
            "decades of teaching through sermons and parables, to the final entering into Nirvana at Kusinara. "
            "Carus sought to present Buddhism's essential spirit on common ground shared by all schools.\n\n"
            "Source: Project Gutenberg eBook #35895 (https://www.gutenberg.org/ebooks/35895)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Olga Kopetzky (1915, Open Court Publishing), pen-and-ink drawings "
            "inspired by Ajanta cave paintings and Gandhara sculpture. Classical Buddhist art style with European draftsmanship. "
            "Also consider: illustrations from Edwin Arnold's 'The Light of Asia' (various editions, 1879+)."
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["buddhism", "sacred-text", "life-of-buddha", "parables", "dharma", "philosophy", "compassion"],
        "roots": ["eastern-wisdom"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan", "Akomolafe", "Shrei"],
        "worldview": "non-dual",
        "items": all_items,
    }

    return grammar


def main():
    print("Reading seed text...")
    text = read_seed()

    print("Stripping front and back matter...")
    text = strip_front_matter(text)
    text = strip_back_matter(text)

    print("Parsing chapters...")
    chapters = parse_chapters(text)
    print(f"  Found {len(chapters)} chapters")

    if len(chapters) < 95:
        print(f"  WARNING: Expected ~100 chapters, only found {len(chapters)}", file=sys.stderr)

    # Report any missing chapters
    missing = [i for i in range(1, 101) if i not in chapters]
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
