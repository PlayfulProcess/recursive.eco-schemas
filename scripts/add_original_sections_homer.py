#!/usr/bin/env python3
"""
Add "Original" sections to homer-kids grammar items using exact quotes
from Butler's prose translations of the Iliad and Odyssey.
"""

import json
import re
import sys

ILIAD_PATH = "seeds/iliad-butler.txt"
ODYSSEY_PATH = "seeds/odyssey-butler.txt"
GRAMMAR_PATH = "grammars/homer-kids/grammar.json"

# Map each L1 item to its source and key passage location
# Format: (source, book_num, search_terms) where search_terms help find the right passage
STORY_SOURCES = {
    # === ILIAD STORIES ===
    # Wrath cycle (Iliad)
    "wrath-golden-apple": None,  # Pre-Iliad myth (not in Homer directly)
    "wrath-paris-helen": None,  # Pre-Iliad backstory (referenced but not narrated)
    "wrath-achilles-rage": ("iliad", 1, ["Sing, O goddess, the anger of Achilles"]),
    "wrath-hector-andromache": ("iliad", 6, ["Hector, I shall never hear you"]),
    "wrath-patroclus": ("iliad", 16, ["Patroclus"]),
    "wrath-achilles-hector": ("iliad", 22, ["Hector"]),
    "wrath-priam-achilles": ("iliad", 24, ["Priam"]),

    # Heroes (Iliad)
    "hero-ajax": ("iliad", 7, ["Ajax"]),
    "hero-diomedes": ("iliad", 5, ["Diomed"]),
    "hero-odysseus-spy": ("iliad", 10, ["Ulysses", "Diomed"]),
    "hero-cassandra": None,  # Mentioned but not featured in Homer
    "hero-penelope": ("odyssey", 1, ["Penelope"]),
    "hero-helen": ("iliad", 3, ["Helen"]),
    "hero-wooden-horse": ("odyssey", 8, ["wooden horse", "Demodocus"]),

    # Gods (Iliad)
    "god-zeus-scales": ("iliad", 8, ["scales", "Zeus"]),
    "god-athena-odysseus": ("odyssey", 13, ["Minerva"]),
    "god-poseidon-grudge": ("odyssey", 5, ["Neptune"]),
    "god-aphrodite-wounded": ("iliad", 5, ["Venus", "wounded"]),
    "god-hermes-guide": ("iliad", 24, ["Mercury"]),
    "god-hephaestus-shield": ("iliad", 18, ["shield", "Vulcan"]),
    "god-ares-screams": ("iliad", 5, ["Mars", "scream"]),

    # === ODYSSEY STORIES ===
    # Voyage cycle
    "voyage-cyclops": ("odyssey", 9, ["Cyclops", "Polyphemus", "Nobody"]),
    "voyage-circe": ("odyssey", 10, ["Circe"]),
    "voyage-sirens": ("odyssey", 12, ["Sirens"]),
    "voyage-scylla-charybdis": ("odyssey", 12, ["Scylla", "Charybdis"]),
    "voyage-calypso": ("odyssey", 5, ["Calypso"]),
    "voyage-underworld": ("odyssey", 11, ["dead", "Tiresias"]),
    "voyage-lotus-eaters": ("odyssey", 9, ["Lotus"]),
    "voyage-aeolus-winds": ("odyssey", 10, ["Aeolus", "winds"]),

    # Homecoming cycle (Odyssey)
    "home-disguise": ("odyssey", 13, ["beggar", "disguise"]),
    "home-argos": ("odyssey", 17, ["dog", "Argos"]),
    "home-eurycleia": ("odyssey", 19, ["Euryclea", "scar"]),
    "home-bow": ("odyssey", 21, ["bow"]),
    "home-suitors-fall": ("odyssey", 22, ["suitors"]),
    "home-penelope-test": ("odyssey", 23, ["bed", "Penelope"]),
    "home-peace": ("odyssey", 24, ["peace"]),

    # Echoes
    "echo-troy-burns": None,  # Not in Homer (post-Iliad)
    "echo-aeneas-flees": None,  # Virgil, not Homer
    "echo-telemachus": ("odyssey", 2, ["Telemachus"]),
    "echo-tiresias": ("odyssey", 11, ["Tiresias"]),
    "echo-wine-dark-sea": ("odyssey", 5, ["wine-dark"]),
    "echo-homer-sings": None,  # Meta-narrative
}


def parse_homer(filepath, book_header_pattern):
    """Parse Homer text into {book_num: text} structure."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Find book boundaries
    book_pattern = re.compile(book_header_pattern, re.MULTILINE)
    matches = list(book_pattern.finditer(text))

    books = {}
    for i, m in enumerate(matches):
        # Extract roman numeral and convert to int
        roman = m.group(1).strip().rstrip(".")
        book_num = roman_to_int(roman)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        book_text = text[start:end].strip()
        # Clean up: remove extra whitespace but keep paragraph breaks
        book_text = re.sub(r'\n{3,}', '\n\n', book_text)
        books[book_num] = book_text

    return books


def roman_to_int(s):
    """Convert Roman numeral string to integer."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
    result = 0
    for i, c in enumerate(s):
        if c not in values:
            continue
        if i + 1 < len(s) and s[i + 1] in values and values[c] < values[s[i + 1]]:
            result -= values[c]
        else:
            result += values[c]
    return result


def extract_passage(book_text, search_terms, max_chars=1500):
    """Find the most relevant passage from a book using search terms."""
    paragraphs = book_text.split("\n\n")

    # Score each paragraph by how many search terms it contains
    scored = []
    for i, para in enumerate(paragraphs):
        para_clean = para.strip()
        if len(para_clean) < 30:
            continue
        score = 0
        for term in search_terms:
            if term.lower() in para_clean.lower():
                score += 1
        if score > 0:
            scored.append((score, i, para_clean))

    if not scored:
        # Just return the first substantial paragraph
        for para in paragraphs:
            if len(para.strip()) > 50:
                return para.strip()[:max_chars]
        return None

    # Sort by score (descending), then by position (ascending)
    scored.sort(key=lambda x: (-x[0], x[1]))

    # Take the best paragraph and maybe the next one
    best_idx = scored[0][1]
    result_paras = [paragraphs[best_idx].strip()]

    # Add next paragraph if under char limit
    if best_idx + 1 < len(paragraphs):
        next_para = paragraphs[best_idx + 1].strip()
        if len("\n\n".join(result_paras)) + len(next_para) < max_chars and len(next_para) > 30:
            result_paras.append(next_para)

    result = "\n\n".join(result_paras)
    if len(result) > max_chars:
        # Truncate at last sentence boundary
        truncated = result[:max_chars]
        last_period = truncated.rfind(". ")
        if last_period > max_chars // 2:
            truncated = truncated[:last_period + 1]
        result = truncated

    return result


def main():
    print("Parsing Homer texts...", file=sys.stderr)
    # Odyssey uses "BOOK I" through "BOOK XXIV"
    odyssey_books = parse_homer(ODYSSEY_PATH, r'^BOOK\s+([IVXL]+)\s*$')
    print(f"  Odyssey: {len(odyssey_books)} books", file=sys.stderr)

    # Iliad uses "BOOK I." through "BOOK XXIV." (with trailing period)
    iliad_books = parse_homer(ILIAD_PATH, r'^BOOK\s+([IVXL]+)\.?\s*$')
    print(f"  Iliad: {len(iliad_books)} books", file=sys.stderr)

    with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
        grammar = json.load(f)

    updated = 0
    skipped = 0
    failed = 0

    for item in grammar["items"]:
        if item.get("level", 1) != 1:
            continue

        item_id = item["id"]
        if item_id not in STORY_SOURCES:
            print(f"  SKIP {item_id}: not in mapping", file=sys.stderr)
            skipped += 1
            continue

        source_info = STORY_SOURCES[item_id]
        if source_info is None:
            print(f"  SKIP {item_id}: pre-Homeric or non-Homeric story", file=sys.stderr)
            skipped += 1
            continue

        if "Original" in item.get("sections", {}):
            print(f"  SKIP {item_id}: already has Original", file=sys.stderr)
            skipped += 1
            continue

        source, book_num, search_terms = source_info
        source_name = "The Iliad" if source == "iliad" else "The Odyssey"
        books = iliad_books if source == "iliad" else odyssey_books

        if book_num not in books:
            print(f"  FAILED {item_id}: Book {book_num} not found in {source}", file=sys.stderr)
            failed += 1
            continue

        passage = extract_passage(books[book_num], search_terms)
        if passage:
            # Clean up line breaks within paragraphs
            passage = re.sub(r'\n(?!\n)', ' ', passage)
            passage = re.sub(r'  +', ' ', passage)
            header = f"— Homer, {source_name}, Book {book_num} (Samuel Butler, prose) —"
            item["sections"]["Original"] = f"{header}\n\n{passage}"
            updated += 1
            print(f"  ✓ {item_id}: {source_name} Book {book_num} ({len(passage)} chars)", file=sys.stderr)
        else:
            print(f"  ✗ {item_id}: no passage found", file=sys.stderr)
            failed += 1

    print(f"\nResults: {updated} updated, {skipped} skipped, {failed} failed", file=sys.stderr)

    with open(GRAMMAR_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"Wrote {GRAMMAR_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
