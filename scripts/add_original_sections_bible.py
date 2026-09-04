#!/usr/bin/env python3
"""
Add "Original" sections to biblical-stories-kids grammar items
using exact quotes from the KJV Bible (seeds/king-james-bible.txt).
"""

import json
import re
import sys

KJV_PATH = "seeds/king-james-bible.txt"
GRAMMAR_PATH = "grammars/biblical-stories-kids/grammar.json"

# Map book names to their headers in the KJV Gutenberg text
BOOK_HEADERS = {
    "Genesis": "The First Book of Moses: Called Genesis",
    "Exodus": "The Second Book of Moses: Called Exodus",
    "Leviticus": "The Third Book of Moses: Called Leviticus",
    "Numbers": "The Fourth Book of Moses: Called Numbers",
    "Deuteronomy": "The Fifth Book of Moses: Called Deuteronomy",
    "Joshua": "The Book of Joshua",
    "Judges": "The Book of Judges",
    "Ruth": "The Book of Ruth",
    "1 Samuel": "The First Book of Samuel",
    "2 Samuel": "The Second Book of Samuel",
    "1 Kings": "The First Book of the Kings",
    "2 Kings": "The Second Book of the Kings",
    "1 Chronicles": "The First Book of the Chronicles",
    "2 Chronicles": "The Second Book of the Chronicles",
    "Nehemiah": "The Book of Nehemiah",
    "Esther": "The Book of Esther",
    "Job": "The Book of Job",
    "Psalms": "The Book of Psalms",
    "Proverbs": "The Proverbs",
    "Isaiah": "The Book of the Prophet Isaiah",
    "Jeremiah": "The Book of the Prophet Jeremiah",
    "Ezekiel": "The Book of the Prophet Ezekiel",
    "Daniel": "The Book of Daniel",
    "Hosea": "Hosea",
    "Joel": "Joel",
    "Amos": "Amos",
    "Obadiah": "Obadiah",
    "Jonah": "Jonah",
    "Micah": "Micah",
    "Nahum": "Nahum",
    "Habakkuk": "Habakkuk",
    "Zephaniah": "Zephaniah",
    "Haggai": "Haggai",
    "Zechariah": "Zechariah",
    "Malachi": "Malachi",
    "Ezra": "Ezra",
    "Ecclesiastes": "Ecclesiastes",
    "Song of Solomon": "The Song of Solomon",
    "Matthew": "The Gospel According to Saint Matthew",
    "Mark": "The Gospel According to Saint Mark",
    "Luke": "The Gospel According to Saint Luke",
    "John": "The Gospel According to Saint John",
    "Acts": "The Acts of the Apostles",
    "Romans": "The Epistle of Paul the Apostle to the Romans",
    "1 Corinthians": "The First Epistle of Paul the Apostle to the Corinthians",
    "2 Corinthians": "The Second Epistle of Paul the Apostle to the Corinthians",
    "Galatians": "The Epistle of Paul the Apostle to the Galatians",
    "Ephesians": "The Epistle of Paul the Apostle to the Ephesians",
    "Philippians": "The Epistle of Paul the Apostle to the Philippians",
    "Colossians": "The Epistle of Paul the Apostle to the Colossians",
    "1 Thessalonians": "The First Epistle of Paul the Apostle to the Thessalonians",
    "2 Thessalonians": "The Second Epistle of Paul the Apostle to the Thessalonians",
    "1 Timothy": "The First Epistle of Paul the Apostle to Timothy",
    "2 Timothy": "The Second Epistle of Paul the Apostle to Timothy",
    "Titus": "The Epistle of Paul the Apostle to Titus",
    "Philemon": "The Epistle of Paul the Apostle to Philemon",
    "Hebrews": "The Epistle of Paul the Apostle to the Hebrews",
    "James": "The General Epistle of James",
    "1 Peter": "The First Epistle General of Peter",
    "1 John": "The First Epistle General of John",
    "2 John": "The Second Epistle General of John",
    "3 John": "The Third Epistle General of John",
    "Jude": "The General Epistle of Jude",
    "Revelation": "The Revelation of Saint John the Divine",
}


def parse_kjv(filepath):
    """Parse KJV into {book_name: {(chapter, verse): text}} using simple regex."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find each book's text region using LINE-BASED matching (not substring)
    # This avoids matching "Jonah" inside "unto Jonah" etc.
    book_positions = []
    for book_name, header in BOOK_HEADERS.items():
        last_line = -1
        for i, line in enumerate(lines):
            if i < 95:  # Skip TOC
                continue
            if line.strip() == header:
                last_line = i
        if last_line >= 0:
            book_positions.append((last_line, book_name))

    body_text = "".join(lines)  # Keep for verse extraction below

    book_positions.sort()

    books = {}
    for idx, (start_line, book_name) in enumerate(book_positions):
        end_line = book_positions[idx + 1][0] if idx + 1 < len(book_positions) else len(lines)
        book_text = "".join(lines[start_line:end_line])

        # Flatten text and extract verses by regex
        flat = re.sub(r'\n', ' ', book_text)
        verse_matches = list(re.finditer(r'(\d+):(\d+)\s', flat))

        verses = {}
        for i, m in enumerate(verse_matches):
            ch = int(m.group(1))
            v = int(m.group(2))
            start = m.end()
            end = verse_matches[i + 1].start() if i + 1 < len(verse_matches) else len(flat)
            text = flat[start:end].strip()
            # Clean up extra spaces
            text = re.sub(r'\s+', ' ', text)
            verses[(ch, v)] = text

        books[book_name] = verses

    return books


def get_passage(books, book_name, ch_start, v_start, ch_end, v_end):
    """Extract verses from a book between (ch_start, v_start) and (ch_end, v_end)."""
    if book_name not in books:
        print(f"  WARNING: Book '{book_name}' not found in parsed KJV", file=sys.stderr)
        return None

    verses = books[book_name]
    result = []
    for (ch, v), text in sorted(verses.items()):
        if (ch, v) < (ch_start, v_start):
            continue
        if v_end == 999:  # whole chapter(s)
            if ch > ch_end:
                break
        else:
            if (ch, v) > (ch_end, v_end):
                break
        result.append(f"{ch}:{v} {text}")

    return "\n".join(result) if result else None


def extract_passage(books, reference):
    """Parse a bible reference string and extract the passage."""
    # Handle Book of Tobit (not in KJV)
    if "Tobit" in reference:
        return None

    # Handle composite references with parenthetical descriptions
    ref = re.sub(r'\s*\([^)]*\)', '', reference).strip()

    # Handle "composite healing passages" etc
    if "composite" in ref.lower():
        return None

    # Handle multi-part refs: "Daniel 10, Revelation 12" or "Luke 2:1-20, Matthew 2:1-12"
    if ", " in ref:
        parts = []
        for sub_ref in ref.split(", "):
            text = extract_single(books, sub_ref.strip())
            if text:
                parts.append(f"[{sub_ref.strip()}]\n{text}")
        return "\n\n".join(parts) if parts else None

    return extract_single(books, ref)


def extract_single(books, ref):
    """Extract a single reference."""
    # "Book of Ruth" → "Ruth 1-4"
    if ref.startswith("Book of "):
        book_name = ref[8:]
        return get_passage(books, book_name, 1, 1, 99, 999)

    # "Genesis 25:29-34"
    m = re.match(r'^(.+?)\s+(\d+):(\d+)-(\d+)$', ref)
    if m:
        return get_passage(books, m.group(1), int(m.group(2)), int(m.group(3)),
                           int(m.group(2)), int(m.group(4)))

    # "Genesis 32:22-32"  (same pattern, already handled above)

    # "Matthew 17:1-9"  (same)

    # "1 Kings 19:11-13" — note the book name has a number
    # Already handled by the regex above since (.+?) is non-greedy

    # "Exodus 3" (whole chapter)
    m = re.match(r'^(.+?)\s+(\d+)$', ref)
    if m:
        return get_passage(books, m.group(1), int(m.group(2)), 1,
                           int(m.group(2)), 999)

    # "Jonah 1-4" (chapter range)
    m = re.match(r'^(.+?)\s+(\d+)-(\d+)$', ref)
    if m:
        return get_passage(books, m.group(1), int(m.group(2)), 1,
                           int(m.group(3)), 999)

    # "2 Kings 22-23"
    # Already handled

    print(f"  WARNING: Could not parse reference: {ref}", file=sys.stderr)
    return None


def truncate_passage(text, max_verses=25):
    """For very long passages, take key excerpts."""
    lines = text.strip().split("\n")
    if len(lines) <= max_verses:
        return text

    # Take first 10 and last 8 with ellipsis
    result = lines[:10]
    omitted = len(lines) - 18
    result.append(f"\n[... {omitted} verses omitted for length ...]\n")
    result.extend(lines[-8:])
    return "\n".join(result)


def main():
    print("Parsing KJV Bible...", file=sys.stderr)
    books = parse_kjv(KJV_PATH)
    print(f"  Found {len(books)} books", file=sys.stderr)
    for book_name in sorted(books.keys()):
        total = len(books[book_name])
        print(f"  {book_name}: {total} verses", file=sys.stderr)

    with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
        grammar = json.load(f)

    updated = 0
    skipped = 0
    failed = 0

    for item in grammar["items"]:
        if item.get("level", 1) != 1:
            continue

        ref = item.get("metadata", {}).get("bible_reference")
        if not ref:
            skipped += 1
            continue

        if "Original" in item.get("sections", {}):
            skipped += 1
            continue

        print(f"  Extracting {item['id']}: {ref}", file=sys.stderr)
        passage = extract_passage(books, ref)

        if passage:
            passage = truncate_passage(passage)
            item["sections"]["Original"] = f"— King James Version, {ref} —\n\n{passage}"
            updated += 1
            # Print first line as sanity check
            first_line = passage.split("\n")[0][:80]
            print(f"    ✓ {first_line}...", file=sys.stderr)
        else:
            print(f"    ✗ FAILED to extract", file=sys.stderr)
            failed += 1

    print(f"\nResults: {updated} updated, {skipped} skipped, {failed} failed", file=sys.stderr)

    with open(GRAMMAR_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"Wrote {GRAMMAR_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
