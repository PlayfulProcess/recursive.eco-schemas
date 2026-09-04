#!/usr/bin/env python3
"""
Build grammar.json for The Golden Bough by James George Frazer.

Source: Project Gutenberg eBook #3623 (Abridged edition, 1922)
Author: Sir James George Frazer

Structure:
- L1: 69 chapters (+ Preface)
- L2: Thematic groupings
- L3: Meta-categories
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "golden-bough.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "golden-bough"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Chapter titles from the TOC (used for matching and display)
CHAPTER_TITLES = {
    0: "Preface",
    1: "The King of the Wood",
    2: "Priestly Kings",
    3: "Sympathetic Magic",
    4: "Magic and Religion",
    5: "The Magical Control of the Weather",
    6: "Magicians as Kings",
    7: "Incarnate Human Gods",
    8: "Departmental Kings of Nature",
    9: "The Worship of Trees",
    10: "Relics of Tree Worship in Modern Europe",
    11: "The Influence of the Sexes on Vegetation",
    12: "The Sacred Marriage",
    13: "The Kings of Rome and Alba",
    14: "Succession to the Kingdom in Ancient Latium",
    15: "The Worship of the Oak",
    16: "Dianus and Diana",
    17: "The Burden of Royalty",
    18: "The Perils of the Soul",
    19: "Tabooed Acts",
    20: "Tabooed Persons",
    21: "Tabooed Things",
    22: "Tabooed Words",
    23: "Our Debt to the Savage",
    24: "The Killing of the Divine King",
    25: "Temporary Kings",
    26: "Sacrifice of the King's Son",
    27: "Succession to the Soul",
    28: "The Killing of the Tree-Spirit",
    29: "The Myth of Adonis",
    30: "Adonis in Syria",
    31: "Adonis in Cyprus",
    32: "The Ritual of Adonis",
    33: "The Gardens of Adonis",
    34: "The Myth and Ritual of Attis",
    35: "Attis as a God of Vegetation",
    36: "Human Representatives of Attis",
    37: "Oriental Religions in the West",
    38: "The Myth of Osiris",
    39: "The Ritual of Osiris",
    40: "The Nature of Osiris",
    41: "Isis",
    42: "Osiris and the Sun",
    43: "Dionysus",
    44: "Demeter and Persephone",
    45: "Corn-Mother and Corn-Maiden in Northern Europe",
    46: "Corn-Mother in Many Lands",
    47: "Lityerses",
    48: "The Corn-Spirit as an Animal",
    49: "Ancient Deities of Vegetation as Animals",
    50: "Eating the God",
    51: "Homeopathic Magic of a Flesh Diet",
    52: "Killing the Divine Animal",
    53: "The Propitiation of Wild Animals by Hunters",
    54: "Types of Animal Sacrament",
    55: "The Transference of Evil",
    56: "The Public Expulsion of Evils",
    57: "Public Scapegoats",
    58: "Human Scapegoats in Classical Antiquity",
    59: "Killing the God in Mexico",
    60: "Between Heaven and Earth",
    61: "The Myth of Balder",
    62: "The Fire-Festivals of Europe",
    63: "The Interpretation of the Fire-Festivals",
    64: "The Burning of Human Beings in the Fires",
    65: "Balder and the Mistletoe",
    66: "The External Soul in Folk-Tales",
    67: "The External Soul in Folk-Custom",
    68: "The Golden Bough",
    69: "Farewell to Nemi",
}

# Roman numeral to int mapping
def roman_to_int(s):
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    for i in range(len(s)):
        if i + 1 < len(s) and vals.get(s[i], 0) < vals.get(s[i+1], 0):
            result -= vals.get(s[i], 0)
        else:
            result += vals.get(s[i], 0)
    return result


def int_to_roman(n):
    """Convert integer to roman numeral string."""
    vals = [(50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    result = ''
    for val, numeral in vals:
        while n >= val:
            result += numeral
            n -= val
    return result


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


def make_id(chapter_num):
    """Create an ID from chapter number."""
    if chapter_num == 0:
        return "preface"
    title = CHAPTER_TITLES[chapter_num]
    # Convert to lowercase, replace non-alphanum with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    return f"ch{chapter_num:02d}-{slug}"


def make_keywords(chapter_num, text):
    """Generate keywords based on chapter content."""
    title = CHAPTER_TITLES[chapter_num].lower()
    keywords = []

    keyword_map = {
        "magic": "magic", "taboo": "taboo", "king": "kingship",
        "tree": "trees", "oak": "oak", "vegetation": "vegetation",
        "corn": "corn-spirit", "adonis": "adonis", "attis": "attis",
        "osiris": "osiris", "isis": "isis", "dionysus": "dionysus",
        "demeter": "demeter", "persephone": "persephone",
        "fire": "fire-festivals", "balder": "balder", "soul": "soul",
        "evil": "evil", "scapegoat": "scapegoat", "sacrifice": "sacrifice",
        "priest": "priesthood", "diana": "diana", "worship": "worship",
        "ritual": "ritual", "myth": "mythology", "animal": "animals",
        "death": "death", "golden bough": "golden-bough", "nemi": "nemi",
    }

    for term, kw in keyword_map.items():
        if term in title:
            keywords.append(kw)

    if not keywords:
        # Fallback: use first few significant words from title
        words = re.findall(r'[a-z]+', title)
        keywords = [w for w in words if len(w) > 3][:3]

    return keywords


# Thematic groupings for L2
THEMES = [
    {
        "id": "theme-sacred-kingship",
        "name": "Sacred Kingship and the Priesthood of Nemi",
        "chapters": list(range(1, 9)),  # 1-8
        "about": "The heart of Frazer's inquiry: the strange rule of succession at the sacred grove of Nemi, where the priest-king could only be replaced by the man who killed him. From this starting point, Frazer traces the institution of sacred kingship across cultures — kings who were also magicians, priests, and incarnate gods, wielding power over nature itself.",
        "for_readers": "Begin here. Chapter 1 sets the scene at the eerie grove of Diana at Nemi, and the remaining chapters trace the logic outward: why would a king be sacred? Because he was first a magician, then a god incarnate. This is Frazer's central argument in miniature.",
    },
    {
        "id": "theme-magic-and-taboo",
        "name": "Magic, Taboo, and the Primitive Mind",
        "chapters": [3, 4, 5, 17, 18, 19, 20, 21, 22, 23],
        "about": "Frazer's elaborate taxonomy of magical thinking: sympathetic magic (like produces like, things once in contact remain connected), the evolution from magic to religion to science, and the vast system of taboos that governed the lives of sacred persons. These chapters document hundreds of customs from around the world, revealing a common logic beneath seemingly irrational practices.",
        "for_readers": "Chapter 3 on Sympathetic Magic is one of the most influential chapters in anthropology. The taboo chapters (19-22) are encyclopedic — browse them for the extraordinary range of human belief about what is dangerous to touch, eat, say, or do.",
    },
    {
        "id": "theme-tree-worship-vegetation",
        "name": "Tree Worship and the Spirit of Vegetation",
        "chapters": [9, 10, 11, 12, 13, 14, 15, 16],
        "about": "The worship of trees and vegetation spirits across European and ancient cultures. Frazer argues that the King of the Wood at Nemi was a personification of the tree-spirit, and traces connections between tree worship, sacred marriages, and the fertility of the land. May-poles, harvest customs, and sacred groves all connect to an ancient veneration of the green world.",
        "for_readers": "These chapters connect the abstract theory of sacred kingship to the concrete world of European folk custom. The May-pole, the harvest sheaf, the sacred oak — all are survivals of an ancient religion of vegetation.",
    },
    {
        "id": "theme-dying-god",
        "name": "The Dying and Reviving God",
        "chapters": list(range(24, 45)),  # 24-44
        "about": "The great central theme of The Golden Bough: the myth of the dying and reviving god, found across the ancient world in the figures of Adonis, Attis, Osiris, and Dionysus. Frazer argues these myths reflect an ancient ritual of killing the divine king when his powers waned, to ensure the renewal of nature. The killing of the tree-spirit, temporary kings, and the sacrifice of the king's son are all variations on this theme.",
        "for_readers": "This is the longest and most famous section. The myths of Adonis, Attis, Osiris, and Dionysus are told in vivid detail. Watch for Frazer's method: he compares myths across cultures to reveal a common pattern of death and resurrection tied to the agricultural cycle.",
    },
    {
        "id": "theme-corn-spirit",
        "name": "The Corn-Spirit and Harvest Customs",
        "chapters": list(range(45, 55)),  # 45-54
        "about": "The spirit of the corn (grain) as it manifests in European harvest customs and worldwide agricultural rites. The Corn-Mother, the Corn-Maiden, the last sheaf, and the various animal forms the corn-spirit takes (wolf, goat, bull, pig) — all are traced through hundreds of examples. Frazer connects these folk customs to the ancient dying gods, arguing they are the same phenomenon in a humbler guise.",
        "for_readers": "These chapters are ethnographic treasure troves. The customs described — the last sheaf treated as a living being, the harvest worker who cuts the last grain identified with the corn-spirit — show how the abstract theology of dying gods played out in the daily life of European peasants.",
    },
    {
        "id": "theme-scapegoat-evil",
        "name": "Scapegoats and the Expulsion of Evil",
        "chapters": list(range(55, 60)),  # 55-59
        "about": "The universal human practice of transferring evil, disease, and misfortune to another being — an animal, an object, or a human scapegoat — and then expelling or destroying it. Frazer traces this from simple folk remedies through elaborate public rituals of purification, culminating in the Roman Saturnalia and the killing of the god in Mexico.",
        "for_readers": "The scapegoat chapters reveal one of humanity's most persistent psychological mechanisms: the belief that suffering can be transferred to another. The connections Frazer draws between ancient Roman festivals and the Aztec sacrifice of god-impersonators are startling.",
    },
    {
        "id": "theme-fire-soul-mistletoe",
        "name": "Fire, the External Soul, and the Golden Bough",
        "chapters": list(range(60, 70)),  # 60-69
        "about": "The grand finale of Frazer's argument. The myth of Balder, the Norse god killed by a mistletoe dart, connects to the great fire-festivals of Europe and the widespread folk-belief in the 'external soul' — the idea that a person's life can be stored outside the body in a plant, animal, or object. The Golden Bough itself, Frazer concludes, was the mistletoe growing on the sacred oak at Nemi, in which the priest-king's soul was believed to reside.",
        "for_readers": "These final chapters bring Frazer's vast comparative journey to its destination. The fire-festivals chapter (62) is magnificent in scope. The external soul chapters (66-67) read like fairy tales. And the final 'Farewell to Nemi' is one of the great passages in English prose.",
    },
]


def parse_golden_bough(text):
    """Parse Golden Bough into preface + 69 chapters."""
    chapters = {}

    # Find the Preface
    preface_match = re.search(r'^Preface\s*$', text, re.MULTILINE)
    if not preface_match:
        print("WARNING: Could not find Preface")
        return chapters

    # Build a list of chapter positions: (chapter_num, start_pos)
    chapter_positions = []

    # Preface
    chapter_positions.append((0, preface_match.start()))

    # Chapters 1-69 use Roman numeral headings in the body
    # Pattern: "^{ROMAN}. {Title}" on its own line
    for ch_num in range(1, 70):
        roman = int_to_roman(ch_num)
        title = CHAPTER_TITLES[ch_num]
        # Build a flexible pattern
        # The title in the body may differ slightly from our list
        pattern = rf'^{roman}\.\s+' + re.escape(title[0:20])
        match = re.search(pattern, text, re.MULTILINE)
        if not match:
            # Try just the Roman numeral with a period and space
            pattern2 = rf'^{roman}\.\s+\S'
            for m in re.finditer(pattern2, text, re.MULTILINE):
                # Verify it's a chapter heading (not a sub-section number)
                line = text[m.start():text.index('\n', m.start())]
                # Chapter headings have title case words after the roman numeral
                after_roman = line[len(roman)+2:].strip()
                if after_roman and after_roman[0].isupper() and len(after_roman) > 5:
                    match = m
                    break
        if match:
            chapter_positions.append((ch_num, match.start()))
        else:
            print(f"WARNING: Could not find Chapter {ch_num}: {CHAPTER_TITLES[ch_num]}")

    # Sort by position
    chapter_positions.sort(key=lambda x: x[1])

    # Extract text for each chapter
    for i, (ch_num, pos) in enumerate(chapter_positions):
        if i + 1 < len(chapter_positions):
            end = chapter_positions[i + 1][1]
        else:
            end = len(text)

        chunk = text[pos:end].strip()

        # Remove the heading line(s)
        lines = chunk.split('\n')
        # Skip heading line and any blank lines after it
        text_start = 1
        while text_start < len(lines) and not lines[text_start].strip():
            text_start += 1

        chapter_text = '\n'.join(lines[text_start:]).strip()
        # Clean up multiple blank lines
        chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)

        chapters[ch_num] = chapter_text

    return chapters


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)

    chapters = parse_golden_bough(text)
    print(f"Parsed {len(chapters)} chapters (expected 70: Preface + 69)")

    items = []
    sort_order = 0

    # L1: Individual chapters
    for ch_num in sorted(chapters.keys()):
        sort_order += 1
        ch_id = make_id(ch_num)
        ch_name = CHAPTER_TITLES[ch_num]
        if ch_num > 0:
            ch_name = f"Chapter {ch_num}: {ch_name}"
        ch_text = chapters[ch_num]
        keywords = make_keywords(ch_num, ch_text)

        item = {
            "id": ch_id,
            "name": ch_name,
            "sort_order": sort_order,
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": ch_text,
            },
            "keywords": keywords,
            "metadata": {
                "chapter_number": ch_num,
            }
        }
        items.append(item)
        print(f"  Ch {ch_num:2d}: {CHAPTER_TITLES[ch_num]} ({len(ch_text)} chars)")

    # L2: Thematic groupings
    all_theme_ids = []
    for theme in THEMES:
        sort_order += 1
        theme_id = theme["id"]
        all_theme_ids.append(theme_id)

        composite = [make_id(ch) for ch in theme["chapters"]]

        items.append({
            "id": theme_id,
            "name": theme["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": composite,
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
        "id": "golden-bough-complete",
        "name": "The Golden Bough: A Study of Magic and Religion",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "Sir James George Frazer's The Golden Bough (1890, abridged 1922) is one of the most influential works of comparative mythology and religion ever written. Starting from a single puzzle — why did the priest of Diana at Nemi have to kill his predecessor to take office? — Frazer spins outward through the world's myths, rituals, and folk customs to construct a vast theory of sacred kingship, dying gods, and the evolution of human thought from magic through religion to science. The book documents hundreds of customs from every inhabited continent: tree worship, harvest rituals, fire festivals, taboos, scapegoats, and the universal pattern of the dying and reviving god. Though many of Frazer's specific theories have been superseded, his method of cross-cultural comparison and his encyclopedic documentation of human ritual life remain invaluable. The Golden Bough influenced a generation of writers and thinkers, from T.S. Eliot and W.B. Yeats to Wittgenstein and Joseph Campbell.",
            "For Readers": "The Golden Bough rewards both sequential reading and browsing. Read Chapter 1 and 69 (Farewell to Nemi) for the frame. The magic chapters (3-5) and the dying god chapters (24-44) are the theoretical core. The harvest customs (45-54) and fire festivals (62) are the most vivid ethnographic material. Frazer writes beautifully — his prose is Victorian in its amplitude but always clear. The book is best approached as a cabinet of wonders: every chapter opens doors onto practices and beliefs that expand one's sense of what it means to be human.",
        },
        "keywords": ["mythology", "religion", "magic", "ritual", "comparative", "frazer", "golden-bough"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Sir James George Frazer",
                    "date": "1922",
                    "note": "Author (Abridged Edition)"
                }
            ]
        },
        "name": "The Golden Bough",
        "description": "Sir James George Frazer's The Golden Bough: A Study of Magic and Religion (Abridged Edition, 1922) — the foundational work of comparative mythology. In 69 chapters, Frazer traces the institution of sacred kingship from the grove of Diana at Nemi through the world's myths, rituals, and folk customs: sympathetic magic, tree worship, the dying gods Adonis, Attis, Osiris, and Dionysus, corn-spirits, scapegoats, fire festivals, and the external soul. A vast cabinet of wonders that shaped modern understanding of myth and ritual.\n\nSource: Project Gutenberg eBook #3623 (https://www.gutenberg.org/ebooks/3623)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: J.M.W. Turner's painting 'The Golden Bough' (1834, Tate Gallery). Illustrations from the 12-volume third edition (Macmillan, 1906-1915). Ancient Roman artifacts depicting Diana of Nemi. Victorian engravings of European harvest customs and fire festivals.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["mythology", "religion", "magic", "ritual", "anthropology", "comparative-religion", "public-domain", "full-text"],
        "roots": ["indigenous-mythology"],
        "shelves": ["mirror"],
        "lineages": ["Shrei"],
        "worldview": "comparative",
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
