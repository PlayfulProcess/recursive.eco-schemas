#!/usr/bin/env python3
"""
Build grammar.json for The Popol Vuh from seeds/popol-vuh.txt
(Project Gutenberg #56550, Lewis Spence retelling, 1908)

Parses the four narrative books, skips Spence's commentary sections.
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SEED_FILE = os.path.join(ROOT_DIR, "seeds", "popol-vuh.txt")
OUTPUT_DIR = os.path.join(ROOT_DIR, "grammars", "popol-vuh")
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


def extract_books(text):
    """Extract the four narrative books from the text."""
    lines = text.split("\n")

    # Find the start lines of each book
    book_starts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in ("THE FIRST BOOK", "THE SECOND BOOK", "THE THIRD BOOK", "THE FOURTH BOOK"):
            book_starts.append((i, stripped))

    # Find the end of the narrative section (COSMOGONY or BOOK II. COMMENTED)
    narrative_end = len(lines)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in ('COSMOGONY OF THE "POPOL VUH"', "BOOK II. COMMENTED UPON"):
            narrative_end = i
            break

    books = []
    for idx, (start_line, title) in enumerate(book_starts):
        # End is either the next book's start or narrative_end
        if idx + 1 < len(book_starts):
            end_line = book_starts[idx + 1][0]
        else:
            end_line = narrative_end

        # Skip the title line and any blank lines after it
        content_start = start_line + 1
        book_text = "\n".join(lines[content_start:end_line]).strip()
        books.append((title, book_text))

    return books


def split_paragraphs(text):
    """Split text into paragraphs (separated by blank lines).
    Skips all-caps heading lines that appear as sub-headings within books.
    """
    # Split on one or more blank lines
    raw_paras = re.split(r"\n\s*\n", text)
    paragraphs = []
    for p in raw_paras:
        # Join continuation lines (unwrap)
        cleaned = " ".join(p.split())
        cleaned = cleaned.strip()
        if not cleaned:
            continue
        # Skip all-caps heading lines (sub-headings within books)
        if re.match(r'^[A-Z][A-Z \-]{4,}$', cleaned):
            continue
        paragraphs.append(cleaned)
    return paragraphs


def first_sentence_name(text, max_len=80):
    """Extract first sentence, truncated to max_len characters."""
    # Find first sentence end
    match = re.search(r'[.!?](?:\s|$)', text)
    if match:
        sentence = text[:match.end()].strip()
    else:
        sentence = text

    if len(sentence) <= max_len:
        return sentence

    # Truncate at word boundary
    truncated = sentence[:max_len]
    last_space = truncated.rfind(" ")
    if last_space > 40:
        truncated = truncated[:last_space]
    return truncated + "..."


def strip_footnote_refs(text):
    """Remove footnote reference markers like [1], [2], etc."""
    return re.sub(r'\s*\[\d+\]', '', text)


def build_grammar():
    raw_text = read_seed()
    text = strip_gutenberg(raw_text)
    books = extract_books(text)

    book_labels = [
        ("book-1", "The First Book"),
        ("book-2", "The Second Book"),
        ("book-3", "The Third Book"),
        ("book-4", "The Fourth Book"),
    ]

    book_l2_names = [
        "The First Book: Creation",
        "The Second Book: The Hero Twins",
        "The Third Book: The Creation of Humanity",
        "The Fourth Book: The Kiché Kingdom",
    ]

    book_l2_abouts = [
        "The primeval waters, the Creators (Hurakan, Gucumatz, Tepeu), the failed first humans made of clay and wood, the flood that destroyed them.",
        "The adventures of Hunahpu and Xbalanque, the Hero Twins who descend to Xibalba (the underworld), outwit the Lords of Death, and rise as the sun and moon.",
        "The successful creation of humans from maize, the gift of sight, the migration of the tribes.",
        "The founding of the Kiché nation, the lineages, the coming of the Spaniards.",
    ]

    items = []
    sort_order = 0
    book_item_ids = {i: [] for i in range(4)}  # track L1 ids per book

    # L1: Paragraphs
    for book_idx, (title, book_text) in enumerate(books):
        category = book_labels[book_idx][0]
        paragraphs = split_paragraphs(book_text)

        for para_idx, para_text in enumerate(paragraphs):
            para_text = strip_footnote_refs(para_text)
            item_id = f"{category}-p{para_idx + 1:02d}"
            name = first_sentence_name(para_text)

            item = {
                "id": item_id,
                "name": name,
                "sort_order": sort_order,
                "category": category,
                "level": 1,
                "sections": {
                    "Passage": para_text
                },
                "keywords": [],
                "metadata": {}
            }
            items.append(item)
            book_item_ids[book_idx].append(item_id)
            sort_order += 1

    # L2: Book groups
    for book_idx in range(4):
        category = book_labels[book_idx][0]
        item_id = f"{category}-emergence"
        item = {
            "id": item_id,
            "name": book_l2_names[book_idx],
            "sort_order": sort_order,
            "category": category,
            "level": 2,
            "sections": {
                "About": book_l2_abouts[book_idx],
                "For Readers": "Read these passages as a connected narrative. The Popol Vuh was an oral tradition before it was written — let the rhythm of retelling carry you."
            },
            "keywords": [],
            "metadata": {},
            "composite_of": book_item_ids[book_idx],
            "relationship_type": "emergence"
        }
        items.append(item)
        sort_order += 1

    # L2: Thematic groups
    # We assign paragraphs to thematic groups based on content keywords
    all_l1_ids = []
    for ids in book_item_ids.values():
        all_l1_ids.extend(ids)

    # Creation and Destruction — Book 1 passages about creation/destruction + Book 3 creation
    creation_ids = []
    for item in items:
        if item["level"] != 1:
            continue
        text_lower = item["sections"]["Passage"].lower()
        if item["category"] == "book-1" and any(w in text_lower for w in ["creat", "destroy", "flood", "mannikin", "clay", "wood", "hurakan", "gucumatz"]):
            creation_ids.append(item["id"])
        elif item["category"] == "book-3" and any(w in text_lower for w in ["creat", "maize", "yellow", "white", "former"]):
            creation_ids.append(item["id"])

    # Descent to Xibalba — Book 2 passages about Xibalba
    xibalba_ids = []
    for item in items:
        if item["level"] != 1:
            continue
        text_lower = item["sections"]["Passage"].lower()
        if any(w in text_lower for w in ["xibalba", "underworld", "lords of death", "hun-came", "vukub-came"]):
            xibalba_ids.append(item["id"])

    # Maize and Humanity — passages about maize and human creation
    maize_ids = []
    for item in items:
        if item["level"] != 1:
            continue
        text_lower = item["sections"]["Passage"].lower()
        if any(w in text_lower for w in ["maize", "corn", "yellow and white", "balam-quitz"]):
            maize_ids.append(item["id"])

    thematic_groups = [
        {
            "id": "theme-creation-destruction",
            "name": "Creation and Destruction",
            "about": "The multiple creations and their failures — from the primeval darkness through the clay people and wooden mannikins to the flood that destroyed them. The gods learn through failure what humanity must be.",
            "ids": creation_ids
        },
        {
            "id": "theme-descent-xibalba",
            "name": "The Descent to Xibalba",
            "about": "The hero journey into the underworld: first the father and uncle who fall to the Lords of Death, then the Hero Twins who outwit them. A mythic pattern of descent, trial, and transformation.",
            "ids": xibalba_ids
        },
        {
            "id": "theme-maize-humanity",
            "name": "Maize and Humanity",
            "about": "The creation of true humans from corn — the substance that finally satisfies the gods. Humanity is literally made of maize, binding people and plant in sacred reciprocity.",
            "ids": maize_ids
        }
    ]

    for group in thematic_groups:
        if not group["ids"]:
            continue
        item = {
            "id": group["id"],
            "name": group["name"],
            "sort_order": sort_order,
            "category": "thematic",
            "level": 2,
            "sections": {
                "About": group["about"],
                "For Readers": "These passages are gathered by theme across the four books. Read them together to see how the Popol Vuh weaves its central concerns through the entire narrative."
            },
            "keywords": [],
            "metadata": {},
            "composite_of": group["ids"],
            "relationship_type": "emergence"
        }
        items.append(item)
        sort_order += 1

    # L3: Meta
    all_l2_ids = [item["id"] for item in items if item["level"] == 2]
    meta_item = {
        "id": "popol-vuh-meta",
        "name": "The Popol Vuh",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "The Popol Vuh ('Book of the Community'), the creation myth of the K'iche' Maya. From the primordial waters through the Hero Twins' triumph over death to the founding of nations — the most complete surviving mythology of pre-Columbian Mesoamerica.",
            "For Readers": "The Popol Vuh moves from cosmic creation to human history in four books. It can be read as mythology, as philosophy of repeated creation-through-failure, or as the origin story of a people who understood themselves as literally made of corn."
        },
        "keywords": ["popol-vuh", "maya", "creation-myth", "hero-twins", "xibalba", "maize"],
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
                {"name": "Anonymous (K'iche' Maya)", "date": "~1554-1558", "note": "Original manuscript"},
                {"name": "Lewis Spence", "date": "1908", "note": "English retelling"}
            ]
        },
        "name": "The Popol Vuh",
        "description": "The Popol Vuh ('Book of the Community'), the creation myth of the K'iche' Maya of Central America, retold by Lewis Spence (1908). The most complete surviving mythology of pre-Columbian Mesoamerica: the primordial waters, the failed creations of humanity from mud and wood, the Hero Twins' descent into the underworld of Xibalba, and the final creation of true humans from maize. As Spence notes: it is 'the New World's richest mythological mine.'\n\nSource: Project Gutenberg eBook #56550 (https://www.gutenberg.org/ebooks/56550)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Maya codex illustrations (Dresden, Madrid, Paris codices). Frederick Catherwood's lithographs of Maya ruins from 'Incidents of Travel in Central America' (1841). Maya ceramic paintings of the Hero Twins.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["mythology", "maya", "indigenous", "creation-myth", "public-domain", "full-text", "mesoamerica"],
        "roots": ["indigenous-mythology"],
        "shelves": ["earth"],
        "lineages": ["Andreotti", "Shrei"],
        "worldview": "animist",
        "items": items
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Summary
    l1_count = sum(1 for i in items if i["level"] == 1)
    l2_count = sum(1 for i in items if i["level"] == 2)
    l3_count = sum(1 for i in items if i["level"] == 3)
    print(f"Generated {OUTPUT_FILE}")
    print(f"  L1 items (passages): {l1_count}")
    print(f"  L2 items (emergence): {l2_count}")
    print(f"  L3 items (meta): {l3_count}")
    print(f"  Total items: {len(items)}")

    # Print book breakdown
    for book_idx in range(4):
        cat = book_labels[book_idx][0]
        count = len(book_item_ids[book_idx])
        print(f"  {book_labels[book_idx][1]}: {count} passages")

    # Print thematic group sizes
    for group in thematic_groups:
        print(f"  Theme '{group['name']}': {len(group['ids'])} passages")


if __name__ == "__main__":
    build_grammar()
