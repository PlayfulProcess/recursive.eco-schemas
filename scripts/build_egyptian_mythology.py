#!/usr/bin/env python3
"""
Build grammar.json for Myths and Legends of Ancient Egypt from seeds/egyptian-mythology.txt
(Project Gutenberg #43662, Lewis Spence, 1915)

The text has 9 chapters identified by "CHAPTER I: TITLE" format:
  I.    INTRODUCTORY
  II.   EXPLORATION, HISTORY, AND CUSTOMS
  III.  THE PRIESTHOOD: MYSTERIES AND TEMPLES
  IV.   THE CULT OF OSIRIS
  V.    THE GREAT GODS
  VI.   EGYPTIAN LITERATURE
  VII.  MAGIC
  VIII. FOREIGN AND ANIMAL GODS: THE LATE PERIOD
  IX.   EGYPTIAN ART

Followed by GLOSSARY AND INDEX (skipped).
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SEED_FILE = os.path.join(ROOT_DIR, "seeds", "egyptian-mythology.txt")
OUTPUT_DIR = os.path.join(ROOT_DIR, "grammars", "egyptian-mythology")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "grammar.json")


def read_seed():
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    lines = text.split("\n")
    start_idx = 0
    end_idx = len(lines)
    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i + 1
            break
    for i, line in enumerate(lines):
        if end_marker in line:
            end_idx = i
            break
    return "\n".join(lines[start_idx:end_idx])


def roman_to_int(s):
    """Convert Roman numeral string to integer."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    for i in range(len(s)):
        if i + 1 < len(s) and values.get(s[i], 0) < values.get(s[i + 1], 0):
            result -= values.get(s[i], 0)
        else:
            result += values.get(s[i], 0)
    return result


def clean_text(text):
    """Clean up text: remove illustration markers, normalize whitespace."""
    # Remove [Illustration: ...] markers (may span multiple lines)
    text = re.sub(r'\[Illustration[^\]]*\]', '', text, flags=re.DOTALL)
    # Collapse excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# Chapter titles mapped by number
CHAPTER_TITLES = {
    1: "Introductory",
    2: "Exploration, History, and Customs",
    3: "The Priesthood: Mysteries and Temples",
    4: "The Cult of Osiris",
    5: "The Great Gods",
    6: "Egyptian Literature",
    7: "Magic",
    8: "Foreign and Animal Gods: The Late Period",
    9: "Egyptian Art",
}

# Keywords per chapter
CHAPTER_KEYWORDS = {
    1: ["egypt", "religion", "mythology", "gods", "creation", "cosmogony", "totemism"],
    2: ["nile", "history", "pharaoh", "dynasty", "customs", "exploration", "archaeology"],
    3: ["priesthood", "temples", "mysteries", "ritual", "karnak", "sacred"],
    4: ["osiris", "isis", "horus", "set", "underworld", "resurrection", "death"],
    5: ["ra", "amen", "ptah", "thoth", "hathor", "anubis", "sekhmet"],
    6: ["literature", "poetry", "papyrus", "stories", "tales", "scribes"],
    7: ["magic", "spells", "amulets", "sorcery", "ritual", "supernatural"],
    8: ["foreign-gods", "animal-gods", "bes", "serapis", "sacred-animals", "cats"],
    9: ["art", "sculpture", "painting", "architecture", "pyramids", "aesthetics"],
}


def find_chapters(lines):
    """Find chapter boundaries using 'CHAPTER N: TITLE' pattern."""
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC]+):\s+(.+)$')
    chapters = []

    for i, line in enumerate(lines):
        m = chapter_pattern.match(line.strip())
        if m:
            num = roman_to_int(m.group(1))
            title = m.group(2).strip()
            chapters.append((i, num, title))

    return chapters


def find_glossary(lines, after_line=0):
    """Find the GLOSSARY AND INDEX section after the chapters."""
    for i, line in enumerate(lines):
        if i > after_line and line.strip() == "GLOSSARY AND INDEX":
            return i
    return len(lines)


def find_content_start(lines):
    """Find where the actual content starts (after PREFACE, CONTENTS, LIST OF ILLUSTRATIONS)."""
    # Content starts at CHAPTER I
    chapter_pattern = re.compile(r'^CHAPTER\s+I:\s+')
    for i, line in enumerate(lines):
        if chapter_pattern.match(line.strip()):
            return i
    return 0


def extract_chapter_text(lines, start_line, end_line):
    """Extract chapter text, skipping the CHAPTER heading line."""
    # Skip the chapter heading line
    content_start = start_line + 1
    # Skip blank lines after heading
    while content_start < end_line and lines[content_start].strip() == "":
        content_start += 1

    text = "\n".join(lines[content_start:end_line]).strip()
    return clean_text(text)


def build_grammar():
    raw_text = read_seed()
    text = strip_gutenberg(raw_text)
    lines = text.split("\n")

    chapter_positions = find_chapters(lines)
    # Find glossary after the last chapter
    last_chapter_line = chapter_positions[-1][0] if chapter_positions else 0
    glossary_line = find_glossary(lines, after_line=last_chapter_line)

    if not chapter_positions:
        print("ERROR: No chapters found!")
        return

    print(f"Found {len(chapter_positions)} chapters")
    for pos, num, title in chapter_positions:
        print(f"  Chapter {num}: {title} (line {pos})")
    print(f"Glossary at line {glossary_line}")

    items = []
    sort_order = 0

    # Build L1 items: chapters
    chapter_ids = []
    for idx, (ch_start, num, title) in enumerate(chapter_positions):
        # Chapter ends at next chapter or glossary
        if idx + 1 < len(chapter_positions):
            ch_end = chapter_positions[idx + 1][0]
        else:
            ch_end = glossary_line

        ch_text = extract_chapter_text(lines, ch_start, ch_end)
        ch_id = f"chapter-{num}"
        ch_name = CHAPTER_TITLES.get(num, title.title())
        keywords = CHAPTER_KEYWORDS.get(num, [])

        items.append({
            "id": ch_id,
            "name": f"Chapter {num}: {ch_name}",
            "sort_order": sort_order,
            "category": "chapter",
            "level": 1,
            "sections": {
                "Text": ch_text
            },
            "keywords": keywords,
            "metadata": {"chapter_number": num}
        })
        chapter_ids.append(ch_id)
        sort_order += 1

    # L2: Thematic groupings
    l2_items = []

    # 1. History and Society (chapters 1-3)
    l2_history = {
        "id": "theme-history-and-society",
        "name": "History and Society",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "The foundations of Egyptian civilization: an introduction to the mythological worldview, the history of exploration and archaeological discovery in the Nile Valley, the customs and daily life of the ancient Egyptians, and the powerful priesthood that maintained the temples and mysteries. These chapters provide the essential context for understanding the gods, magic, and literature that follow.",
            "For Readers": "Start here to understand the world that produced Egyptian mythology. The religion of Egypt was not a static system but evolved over thousands of years, absorbing and transforming beliefs from many sources. The priesthood held enormous power, and the temples were not just places of worship but centers of learning, medicine, and political authority."
        },
        "keywords": ["history", "society", "priesthood", "temples", "customs", "nile"],
        "metadata": {},
        "composite_of": ["chapter-1", "chapter-2", "chapter-3"],
        "relationship_type": "emergence"
    }
    l2_items.append(l2_history)
    sort_order += 1

    # 2. The Gods of Egypt (chapters 4-5)
    l2_gods = {
        "id": "theme-the-gods-of-egypt",
        "name": "The Gods of Egypt",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "The core mythology of ancient Egypt: the cult of Osiris — his murder by Set, the devotion of Isis, the resurrection and judgment of the dead — and the great gods of the Egyptian pantheon: Ra the sun god, Amen-Ra king of the gods, Ptah the creator, Thoth god of wisdom, Hathor goddess of love, and many others. These chapters contain the central mythological narratives that shaped Egyptian civilization for millennia.",
            "For Readers": "The Osiris myth is one of the most powerful stories in world mythology — a tale of betrayal, devotion, death, and resurrection that influenced Greek and Roman religion and echoes through Western culture to this day. The great gods of Egypt were not distant abstractions but living presences woven into every aspect of daily life, from agriculture to medicine to the journey after death."
        },
        "keywords": ["osiris", "isis", "ra", "horus", "set", "thoth", "hathor", "gods"],
        "metadata": {},
        "composite_of": ["chapter-4", "chapter-5"],
        "relationship_type": "emergence"
    }
    l2_items.append(l2_gods)
    sort_order += 1

    # 3. Knowledge and Power (chapters 6-7)
    l2_knowledge = {
        "id": "theme-knowledge-and-power",
        "name": "Knowledge and Power",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "The intellectual and magical traditions of ancient Egypt: the rich literary heritage — from love poetry and adventure tales to wisdom literature and religious hymns — and the practice of magic, which was not separate from religion but deeply intertwined with it. Spells, amulets, and ritual words of power (heka) were used by priests, physicians, and ordinary people alike to navigate the seen and unseen worlds.",
            "For Readers": "Egyptian literature is far richer and more varied than most people realize, including the world's oldest known love poems and adventure stories alongside the famous funerary texts. Magic in Egypt was a technology of the sacred — not superstition but a systematic practice rooted in the belief that words, images, and rituals could shape reality. Understanding Egyptian magic helps explain why the culture was so deeply concerned with names, images, and the written word."
        },
        "keywords": ["literature", "magic", "spells", "poetry", "papyrus", "heka"],
        "metadata": {},
        "composite_of": ["chapter-6", "chapter-7"],
        "relationship_type": "emergence"
    }
    l2_items.append(l2_knowledge)
    sort_order += 1

    # 4. The Late Period (chapters 8-9)
    l2_late = {
        "id": "theme-the-late-period",
        "name": "The Late Period",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "The transformation of Egyptian religion in its later centuries: the foreign gods absorbed from conquered and conquering peoples, the sacred animal cults that became increasingly prominent, and the remarkable artistic tradition that produced some of the most iconic works in human history. These chapters trace how Egyptian civilization adapted, evolved, and ultimately influenced the cultures that succeeded it.",
            "For Readers": "The late period of Egyptian religion is fascinating precisely because it shows a living tradition absorbing new influences while maintaining its core identity. The animal gods — cats, bulls, crocodiles, ibises — were not primitive relics but sophisticated theological expressions. And Egyptian art, with its distinctive conventions and breathtaking craftsmanship, remains one of humanity's greatest aesthetic achievements."
        },
        "keywords": ["foreign-gods", "animal-gods", "art", "sculpture", "late-period"],
        "metadata": {},
        "composite_of": ["chapter-8", "chapter-9"],
        "relationship_type": "emergence"
    }
    l2_items.append(l2_late)
    sort_order += 1

    items.extend(l2_items)

    # L3: Meta
    all_l2_ids = [item["id"] for item in l2_items]
    meta_item = {
        "id": "egyptian-mythology-meta",
        "name": "Myths and Legends of Ancient Egypt",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Myths and Legends of Ancient Egypt by Lewis Spence (1915) is a comprehensive survey of Egyptian mythology, religion, history, and culture. Spence, a Scottish journalist and folklorist, brought the methods of comparative mythology to bear on Egyptian religion, arguing that its animal gods, magical practices, and mythological narratives could be understood through the same frameworks used to study other world mythologies. The book covers the full sweep of Egyptian civilization: from the earliest dynastic period through the great age of the pharaohs to the late period of foreign influence and animal cults.",
            "For Readers": "This is a rich and opinionated guide to Egyptian mythology by a writer who took the gods seriously as mythological beings rather than treating them as mere historical curiosities. Spence's comparative approach — drawing connections between Egyptian myths and those of other cultures — makes this an excellent entry point for anyone interested in how mythological thinking works across civilizations. The illustrations by Evelyn Paul add a distinctive early-20th-century artistic dimension to the text."
        },
        "keywords": ["egypt", "mythology", "gods", "osiris", "ra", "isis", "magic", "art", "civilization"],
        "metadata": {},
        "composite_of": all_l2_ids,
        "relationship_type": "emergence"
    }
    items.append(meta_item)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Lewis Spence", "date": "1915", "note": "Author"},
                {"name": "Evelyn Paul", "date": "1915", "note": "Illustrator"}
            ]
        },
        "name": "Myths and Legends of Ancient Egypt",
        "description": "Myths and Legends of Ancient Egypt by Lewis Spence (1915), a comprehensive survey of Egyptian mythology, religion, history, magic, literature, and art. Covers the great gods (Osiris, Isis, Ra, Horus, Thoth, Set), the priesthood and temple mysteries, Egyptian literature and magical practices, sacred animal cults, and the artistic tradition. Illustrated by Evelyn Paul.\n\nSource: Project Gutenberg eBook #43662 (https://www.gutenberg.org/ebooks/43662)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Evelyn Paul's original colour plates and line drawings for this 1915 edition — richly detailed depictions of Egyptian gods, temples, and mythological scenes in an Arts and Crafts-influenced style. Also: the tomb paintings and papyrus illustrations reproduced in E.A. Wallis Budge's editions of the Book of the Dead (1895-1913), and the Egyptian archaeological illustrations in Description de l'Egypte (1809-1829).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["mythology", "egypt", "ancient", "gods", "magic", "public-domain", "full-text"],
        "roots": ["indigenous-mythology", "mysticism"],
        "shelves": ["wonder", "wisdom"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGenerated {OUTPUT_FILE}")
    print(f"  L1 items (chapters): {l1}")
    print(f"  L2 items (thematic groups): {l2}")
    print(f"  L3 items (meta): {l3}")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
