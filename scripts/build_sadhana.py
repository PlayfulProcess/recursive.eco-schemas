#!/usr/bin/env python3
"""
Parse Sadhana: The Realisation of Life (Rabindranath Tagore, Gutenberg #6842) into grammar.json.

NOTE: The seed file seeds/sadhana.txt must contain Tagore's Sadhana (Gutenberg #6842).
The original download used eBook #5345 which is a DIFFERENT work.
To get the correct file, run:
  curl -L -o seeds/sadhana.txt "https://www.gutenberg.org/cache/epub/6842/pg6842.txt"

Structure:
- L1: 8 individual chapters/essays
- L2: Thematic groupings
- L3: Meta-categories
"""

import json
import re
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "sadhana.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "sadhana")
OUTPUT = os.path.join(OUTPUT_DIR, "grammar.json")


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


# The 8 chapters of Sadhana
CHAPTERS = [
    {
        "id": "relation-individual-universe",
        "name": "The Relation of the Individual to the Universe",
        "title_patterns": ["THE RELATION OF THE INDIVIDUAL TO THE UNIVERSE",
                          "I THE RELATION OF THE INDIVIDUAL TO THE UNIVERSE",
                          "I\nTHE RELATION OF THE INDIVIDUAL TO THE UNIVERSE"],
        "keywords": ["individual", "universe", "Brahman", "unity", "consciousness"],
    },
    {
        "id": "soul-consciousness",
        "name": "Soul Consciousness",
        "title_patterns": ["SOUL CONSCIOUSNESS",
                          "II SOUL CONSCIOUSNESS",
                          "II\nSOUL CONSCIOUSNESS"],
        "keywords": ["soul", "consciousness", "atman", "awareness", "inner-life"],
    },
    {
        "id": "problem-of-evil",
        "name": "The Problem of Evil",
        "title_patterns": ["THE PROBLEM OF EVIL",
                          "III THE PROBLEM OF EVIL",
                          "III\nTHE PROBLEM OF EVIL"],
        "keywords": ["evil", "suffering", "morality", "imperfection", "goodness"],
    },
    {
        "id": "problem-of-self",
        "name": "The Problem of Self",
        "title_patterns": ["THE PROBLEM OF SELF",
                          "IV THE PROBLEM OF SELF",
                          "IV\nTHE PROBLEM OF SELF"],
        "keywords": ["self", "ego", "identity", "renunciation", "liberation"],
    },
    {
        "id": "realisation-in-love",
        "name": "Realisation in Love",
        "title_patterns": ["REALISATION IN LOVE",
                          "V REALISATION IN LOVE",
                          "V\nREALISATION IN LOVE",
                          "REALIZATION IN LOVE"],
        "keywords": ["love", "devotion", "bhakti", "union", "divine-love"],
    },
    {
        "id": "realisation-in-action",
        "name": "Realisation in Action",
        "title_patterns": ["REALISATION IN ACTION",
                          "VI REALISATION IN ACTION",
                          "VI\nREALISATION IN ACTION",
                          "REALIZATION IN ACTION"],
        "keywords": ["action", "karma", "duty", "work", "service"],
    },
    {
        "id": "realisation-of-beauty",
        "name": "The Realisation of Beauty",
        "title_patterns": ["THE REALISATION OF BEAUTY",
                          "VII THE REALISATION OF BEAUTY",
                          "VII\nTHE REALISATION OF BEAUTY",
                          "THE REALIZATION OF BEAUTY"],
        "keywords": ["beauty", "art", "aesthetics", "creation", "harmony"],
    },
    {
        "id": "realisation-of-infinite",
        "name": "The Realisation of the Infinite",
        "title_patterns": ["THE REALISATION OF THE INFINITE",
                          "VIII THE REALISATION OF THE INFINITE",
                          "VIII\nTHE REALISATION OF THE INFINITE",
                          "THE REALIZATION OF THE INFINITE"],
        "keywords": ["infinite", "Brahman", "transcendence", "liberation", "unity"],
    },
]


def find_chapter_boundaries(text):
    """Find where each chapter begins in the text."""
    lines = text.split('\n')
    boundaries = []

    for ch in CHAPTERS:
        found = False
        for pattern in ch["title_patterns"]:
            if '\n' in pattern:
                # Multi-line pattern — search in the full text
                idx = text.find(pattern)
                if idx != -1:
                    # Convert character offset to line number
                    line_num = text[:idx].count('\n')
                    if not any(b[0] == ch["id"] for b in boundaries):
                        boundaries.append((ch["id"], line_num))
                        found = True
                        break
            else:
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if pattern in stripped:
                        if not any(b[0] == ch["id"] for b in boundaries):
                            boundaries.append((ch["id"], i))
                            found = True
                            break
                if found:
                    break

        if not found:
            print(f"WARNING: Could not find chapter '{ch['name']}'")

    boundaries.sort(key=lambda x: x[1])
    return boundaries, lines


def parse_chapters(text):
    """Parse the 8 chapters from the text."""
    boundaries, lines = find_chapter_boundaries(text)

    if len(boundaries) < 8:
        print(f"ERROR: Only found {len(boundaries)} of 8 chapters. "
              f"The seed file may contain the wrong text.")
        print("Expected: Tagore's Sadhana: The Realisation of Life (Gutenberg #6842)")
        print("Please run: curl -L -o seeds/sadhana.txt "
              '"https://www.gutenberg.org/cache/epub/6842/pg6842.txt"')
        return None

    parsed = []
    for idx, (ch_id, start_line) in enumerate(boundaries):
        # End boundary
        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][1]
        else:
            end_line = len(lines)

        content_lines = lines[start_line:end_line]

        # Remove the title lines at the top
        cleaned = []
        skip_header = True
        for cl in content_lines:
            stripped = cl.strip()
            if skip_header:
                if not stripped:
                    continue
                # Skip ALL CAPS title lines and Roman numeral lines
                if stripped.upper() == stripped and len(stripped) > 1:
                    continue
                if re.match(r'^[IVX]+\.?$', stripped):
                    continue
                skip_header = False
            cleaned.append(cl)

        content = '\n'.join(cleaned)
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()

        ch_def = next(c for c in CHAPTERS if c["id"] == ch_id)
        parsed.append({
            "id": ch_def["id"],
            "name": ch_def["name"],
            "content": content,
            "keywords": ch_def["keywords"],
            "chapter_number": CHAPTERS.index(ch_def) + 1,
        })

    return parsed


# Thematic groupings
THEMES = [
    {
        "id": "theme-self-and-cosmos",
        "name": "The Self and the Cosmos",
        "chapters": ["relation-individual-universe", "soul-consciousness", "problem-of-self"],
        "about": "Tagore's central question: What is the relationship between the individual soul (atman) and the universal soul (Brahman)? Drawing from the Upanishads, he argues that the individual is not separate from the universe but is its deepest expression. Soul consciousness is the awakening to this unity. The problem of self is the problem of mistaking the limited ego for the whole.",
        "for_readers": "For anyone wrestling with questions of identity, isolation, and belonging. Tagore dissolves the boundary between self and world — not by erasing the self but by expanding it until it encompasses everything."
    },
    {
        "id": "theme-realisation",
        "name": "The Four Realisations",
        "chapters": ["realisation-in-love", "realisation-in-action", "realisation-of-beauty", "realisation-of-infinite"],
        "about": "The four paths to spiritual realisation: through love (bhakti), through action (karma), through beauty (the aesthetic way), and through the Infinite (jnana). Each chapter describes a different doorway to the same destination — union with the Real. Tagore insists that all four are necessary; none alone is sufficient.",
        "for_readers": "A practical guide to spiritual life through four complementary paths. Whether you are drawn to love, to service, to art, or to contemplation, Tagore shows how your particular path leads to the universal."
    },
    {
        "id": "theme-problem-and-resolution",
        "name": "The Great Problems",
        "chapters": ["problem-of-evil", "problem-of-self"],
        "about": "Tagore confronts two fundamental obstacles to spiritual realisation: the existence of evil and the illusion of the separate self. His answers draw from Vedantic philosophy but are expressed with a poet's clarity: evil is incompleteness, not a positive force; the self is not to be destroyed but to find its true scope in the Infinite.",
        "for_readers": "For those troubled by suffering, selfishness, or the apparent meaninglessness of existence. Tagore reframes these problems not as dead ends but as invitations to deeper understanding."
    },
]


def build_grammar(chapters):
    items = []
    sort_order = 0

    # L1: Individual chapters
    for ch in chapters:
        sort_order += 1
        items.append({
            "id": ch["id"],
            "name": f"Chapter {ch['chapter_number']}: {ch['name']}",
            "level": 1,
            "category": "essay",
            "sort_order": sort_order,
            "sections": {
                "Essay": ch["content"]
            },
            "keywords": ch["keywords"],
            "metadata": {
                "chapter_number": ch["chapter_number"],
            }
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
            "composite_of": theme["chapters"],
            "sort_order": sort_order,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {"chapter_count": len(theme["chapters"])}
        })

    # L3: Meta-categories
    sort_order += 1
    items.append({
        "id": "meta-complete-work",
        "name": "Sadhana: From Separation to Unity",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": ["theme-self-and-cosmos", "theme-problem-and-resolution", "theme-realisation"],
        "sort_order": sort_order,
        "sections": {
            "About": "Sadhana traces a single arc: from the recognition of the individual's relation to the universe, through the obstacles that obscure that relation (evil and egoism), to the four paths by which it is realised (love, action, beauty, and the Infinite). The word 'sadhana' itself means spiritual practice or discipline — the daily work of turning toward reality. Tagore's genius is to make this ancient Vedantic vision feel immediate, personal, and universal. These are not doctrines to be believed but experiences to be lived.",
        },
        "keywords": [],
        "metadata": {}
    })

    sort_order += 1
    items.append({
        "id": "meta-east-meets-west",
        "name": "East and West: Tagore's Bridge",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": [ch["id"] for ch in chapters],
        "sort_order": sort_order,
        "sections": {
            "About": "Sadhana was originally delivered as lectures at Harvard University in 1913, the year Tagore won the Nobel Prize in Literature. These essays represent one of the earliest and most eloquent attempts to translate Upanishadic philosophy for a Western audience. Tagore does not simplify or exoticize; he meets Western thought on its own terms, engaging with Kant, the Romantics, and modern science while drawing from the Isha Upanishad, the Mundaka Upanishad, and the devotional poetry of Kabir and the Bauls. The result is a genuine synthesis — not East explaining itself to West, but a single human voice speaking from the place where all traditions converge.",
        },
        "keywords": [],
        "metadata": {}
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    # Quick check: is this the right text?
    if "Tagore" not in raw and "sadhana" not in raw.lower() and "Realisation" not in raw:
        print("ERROR: The seed file does not appear to contain Tagore's Sadhana.")
        print("The file seeds/sadhana.txt contains a different Gutenberg text.")
        print("")
        print("To fix, download the correct text locally and push to the branch:")
        print('  curl -L -o seeds/sadhana.txt '
              '"https://www.gutenberg.org/cache/epub/6842/pg6842.txt" && \\')
        print('  git add seeds/sadhana.txt && \\')
        print('  git commit -m "Replace sadhana seed with correct Tagore text (Gutenberg #6842)" && \\')
        print('  git push origin $(git branch --show-current)')
        sys.exit(1)

    text = strip_gutenberg(raw)
    chapters = parse_chapters(text)

    if chapters is None:
        sys.exit(1)

    print(f"Parsed {len(chapters)} chapters")
    for ch in chapters:
        preview = ch["content"][:60].replace('\n', ' ')
        print(f"  {ch['name']}: {preview}...")

    items = build_grammar(chapters)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Rabindranath Tagore", "date": "1913", "note": "Author, Nobel Prize in Literature 1913"},
            ]
        },
        "name": "Sadhana: The Realisation of Life",
        "description": "Sadhana: The Realisation of Life by Rabindranath Tagore (1913). Eight essays originally delivered as lectures at Harvard University, exploring the Upanishadic vision of the individual's unity with the Infinite — through love, action, beauty, and direct realisation. A poet-philosopher's bridge between Eastern wisdom and Western thought.\n\nSource: Project Gutenberg eBook #6842 (https://www.gutenberg.org/ebooks/6842)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Tagore's own paintings and drawings — his unique style of fluid, dreamlike figures in ink and watercolor emerged later in life but captures the spirit of Sadhana perfectly. Also: Abanindranath Tagore and the Bengal School of Art (early 20th century), which shared Rabindranath's vision of synthesizing Indian spiritual tradition with modern artistic expression.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "Vedanta", "Upanishads", "sacred-text", "public-domain", "full-text", "contemplative", "non-dual", "Indian", "lectures"],
        "roots": ["eastern-wisdom", "mysticism"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan", "Shrei"],
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
