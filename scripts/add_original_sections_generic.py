#!/usr/bin/env python3
"""
Generic script to add "Original" sections to kids grammars by extracting
relevant passages from seed texts using keyword search.

Works by:
1. Reading the grammar's L1 items and their source metadata
2. Reading the corresponding seed text(s)
3. Finding the best matching passage using keywords from the story
4. Adding it as an "Original" section

Usage: python3 scripts/add_original_sections_generic.py <grammar-name> <seed-file> [seed-file2...]
"""

import json
import re
import sys


def read_text(filepath):
    """Read a text file, stripping Gutenberg header/footer."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Strip Gutenberg header
    start_markers = ["*** START OF THE PROJECT GUTENBERG", "*** START OF THIS PROJECT GUTENBERG"]
    for marker in start_markers:
        idx = text.find(marker)
        if idx >= 0:
            text = text[text.find("\n", idx) + 1:]
            break

    # Strip Gutenberg footer
    end_markers = ["*** END OF THE PROJECT GUTENBERG", "*** END OF THIS PROJECT GUTENBERG",
                   "End of the Project Gutenberg", "End of Project Gutenberg"]
    for marker in end_markers:
        idx = text.find(marker)
        if idx >= 0:
            text = text[:idx]
            break

    return text


def split_into_chunks(text, chunk_size=500):
    """Split text into overlapping chunks of roughly chunk_size words."""
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk = []
    current_len = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        words = len(para.split())
        if current_len + words > chunk_size and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            # Keep last paragraph for overlap
            current_chunk = [current_chunk[-1]] if current_chunk else []
            current_len = len(current_chunk[0].split()) if current_chunk else 0
        current_chunk.append(para)
        current_len += words

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def extract_keywords(item):
    """Extract search keywords from a grammar item."""
    keywords = set()

    # From item keywords
    for kw in item.get("keywords", []):
        keywords.add(kw.lower())

    # From item name (split on spaces)
    for word in item.get("name", "").split():
        w = word.lower().strip("'\",.!?")
        if len(w) > 3:
            keywords.add(w)

    # From source metadata
    meta = item.get("metadata", {})
    for key in meta:
        if "source" in key.lower() or key == "tradition":
            val = str(meta[key])
            # Extract significant words from source reference
            for word in val.split():
                w = word.lower().strip("'\",.!?()—")
                if len(w) > 3 and not w.isdigit() and w not in (
                    "from", "also", "that", "this", "with", "they", "their", "them",
                    "have", "been", "were", "was", "and", "the", "for", "not",
                    "book", "part", "chapter", "section", "page", "kanda",
                    "translation", "variant", "version", "tradition",
                    "found", "across", "many"):
                    keywords.add(w)

    # From the story text itself, extract proper nouns (capitalized words)
    story = item.get("sections", {}).get("Story", "")
    for word in story.split():
        w = word.strip("'\",.!?—\n")
        if w and w[0].isupper() and len(w) > 3 and w.upper() != w:
            keywords.add(w.lower())

    return list(keywords)


def score_chunk(chunk, keywords):
    """Score a chunk based on keyword matches."""
    chunk_lower = chunk.lower()
    score = 0
    matched = set()
    for kw in keywords:
        if kw in chunk_lower:
            score += 1
            matched.add(kw)
    return score, matched


def find_best_passage(chunks, keywords, max_chars=1200):
    """Find the best matching passage from chunks."""
    if not chunks:
        return None

    scored = []
    for i, chunk in enumerate(chunks):
        score, matched = score_chunk(chunk, keywords)
        if score > 0:
            scored.append((score, len(matched), i, chunk))

    if not scored:
        return None

    # Sort by score descending, then by number of unique matches
    scored.sort(key=lambda x: (-x[0], -x[1], x[2]))

    best_chunk = scored[0][3]

    # Clean up: normalize whitespace within paragraphs
    paragraphs = best_chunk.split("\n\n")
    cleaned = []
    for para in paragraphs:
        para = re.sub(r'\s+', ' ', para.strip())
        if para:
            cleaned.append(para)

    result = "\n\n".join(cleaned)

    # Truncate if too long
    if len(result) > max_chars:
        # Find a sentence boundary near the limit
        truncated = result[:max_chars]
        last_period = truncated.rfind(". ")
        if last_period > max_chars // 2:
            truncated = truncated[:last_period + 1]
        result = truncated

    return result


def get_source_label(grammar_name, seed_files):
    """Generate a source attribution label."""
    labels = {
        "norse-kids": "Snorri Sturluson, The Prose Edda (Rasmus Anderson, trans.)",
        "king-arthur-kids": "Sir Thomas Malory, Le Morte d'Arthur (Caxton, 1485)",
        "egyptian-kids": "Lewis Spence, Myths and Legends of Ancient Egypt (1915)",
        "ramayana-kids": "The Ramayana (Ralph Griffith, verse translation)",
        "polynesian-kids": "W. D. Westervelt, Legends of Gods and Ghosts (1915)",
        "west-african-kids": "W. H. Barker & Cecilia Sinclair, West African Folk-Tales (1917)",
        "maya-kids": "Lewis Spence, Popol Vuh: Mythic and Heroic Sagas of the Kichés",
        "dreamtime-kids": "K. Langloh Parker, Australian Legendary Tales (1896)",
        "tibetan-dream-kids": "A. L. Shelton, Tibetan Folk Tales (1925)",
    }
    return labels.get(grammar_name, "Source text")


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 add_original_sections_generic.py <grammar-name> <seed-file> [seed-file2...]",
              file=sys.stderr)
        sys.exit(1)

    grammar_name = sys.argv[1]
    seed_files = sys.argv[2:]

    grammar_path = f"grammars/{grammar_name}/grammar.json"

    print(f"Processing {grammar_name}...", file=sys.stderr)

    # Read and combine seed texts
    all_text = ""
    for sf in seed_files:
        print(f"  Reading {sf}...", file=sys.stderr)
        text = read_text(sf)
        all_text += "\n\n" + text
        print(f"    {len(text)} chars", file=sys.stderr)

    chunks = split_into_chunks(all_text, chunk_size=300)
    print(f"  Split into {len(chunks)} chunks", file=sys.stderr)

    with open(grammar_path, "r", encoding="utf-8") as f:
        grammar = json.load(f)

    source_label = get_source_label(grammar_name, seed_files)
    updated = 0
    skipped = 0
    failed = 0

    for item in grammar["items"]:
        if item.get("level", 1) != 1:
            continue

        if "Original" in item.get("sections", {}):
            skipped += 1
            continue

        keywords = extract_keywords(item)
        if not keywords:
            print(f"  SKIP {item['id']}: no keywords", file=sys.stderr)
            skipped += 1
            continue

        passage = find_best_passage(chunks, keywords)
        if passage:
            header = f"— {source_label} —"
            item["sections"]["Original"] = f"{header}\n\n{passage}"
            updated += 1
            print(f"  ✓ {item['id']} ({len(passage)} chars, keywords: {keywords[:5]}...)", file=sys.stderr)
        else:
            print(f"  ✗ {item['id']}: no matching passage (keywords: {keywords[:5]})", file=sys.stderr)
            failed += 1

    print(f"\nResults: {updated} updated, {skipped} skipped, {failed} failed", file=sys.stderr)

    with open(grammar_path, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"Wrote {grammar_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
