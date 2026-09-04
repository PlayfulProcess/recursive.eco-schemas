#!/usr/bin/env python3
"""
Parse The Imitation of Christ (Thomas à Kempis, Gutenberg #1653) into grammar.json.

Structure:
- L1: Individual chapters (4 books, ~114 chapters total)
- L2: The four books + thematic groupings
- L3: Meta-categories
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "imitation-of-christ.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "imitation-of-christ")
OUTPUT = os.path.join(OUTPUT_DIR, "grammar.json")


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1:
        text = text[text.index("\n", start) + 1:]
    if end != -1:
        text = text[:end]
    return text.strip()


def roman_to_int(roman):
    """Convert Roman numeral string to integer."""
    roman = roman.strip().upper()
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    for i, c in enumerate(roman):
        if c not in values:
            return 0
        if i + 1 < len(roman) and values.get(c, 0) < values.get(roman[i + 1], 0):
            result -= values[c]
        else:
            result += values[c]
    return result


def clean_text(text):
    """Clean chapter text: strip footnotes, normalize whitespace."""
    # Remove footnote references like (1), (2) etc inline
    # Remove footnote lines at end (lines starting with (N) pattern)
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        # Skip standalone footnote lines like "(1) John viii. 12. (2) ..."
        if re.match(r'^\s*\(\d+\)\s+\w', line) and ('.' in line[5:]):
            # Check if it looks like a footnote reference line
            if re.match(r'^\s*(\(\d+\)\s+\S.*?\.?\s*)+$', line.strip()):
                continue
        cleaned.append(line)

    text = '\n'.join(cleaned)
    # Remove inline footnote markers like ,(1) or (2)
    text = re.sub(r'\(\d+\)', '', text)
    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_text(text):
    """Parse the Imitation of Christ into books and chapters."""
    lines = text.split('\n')

    # Find the start of actual text (after INTRODUCTORY NOTE, at "THE FIRST BOOK")
    # First skip past any introductory note
    books = []
    book_info = [
        ("THE FIRST BOOK", "Admonitions Profitable for the Spiritual Life", 1),
        ("THE SECOND BOOK", "Admonitions Concerning the Inner Life", 2),
        ("THE THIRD BOOK", "On Inward Consolation", 3),
        ("THE FOURTH BOOK", "Of the Sacrament of the Altar", 4),
    ]

    # Find line indices for each book start
    book_starts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "THE FIRST BOOK":
            book_starts.append((i, book_info[0]))
        elif stripped == "THE SECOND BOOK":
            book_starts.append((i, book_info[1]))
        elif stripped == "THE THIRD BOOK":
            book_starts.append((i, book_info[2]))
        elif stripped == "THE FOURTH BOOK":
            book_starts.append((i, book_info[3]))

    # Now parse chapters within each book
    all_chapters = []

    for b_idx, (book_start_line, (book_title, book_subtitle, book_num)) in enumerate(book_starts):
        # End of this book section
        if b_idx + 1 < len(book_starts):
            book_end_line = book_starts[b_idx + 1][0]
        else:
            book_end_line = len(lines)

        book_lines = lines[book_start_line:book_end_line]

        # Find chapters within this book section
        chapter_indices = []
        for i, line in enumerate(book_lines):
            m = re.match(r'^CHAPTER\s+([IVXLC]+)\s*$', line.strip())
            if m:
                ch_roman = m.group(1)
                ch_num = roman_to_int(ch_roman)
                if ch_num > 0:
                    chapter_indices.append((i, ch_num, ch_roman))

        # Extract each chapter
        for c_idx, (ch_line_idx, ch_num, ch_roman) in enumerate(chapter_indices):
            # End boundary
            if c_idx + 1 < len(chapter_indices):
                ch_end = chapter_indices[c_idx + 1][0]
            else:
                ch_end = len(book_lines)

            ch_lines = book_lines[ch_line_idx:ch_end]

            # First line is "CHAPTER X", skip it
            # Next non-blank lines are the chapter title
            title_lines = []
            content_start = 1
            found_title = False
            blank_after_header = False

            for j in range(1, len(ch_lines)):
                stripped = ch_lines[j].strip()
                if not stripped:
                    if found_title:
                        content_start = j + 1
                        break
                    blank_after_header = True
                    continue
                if blank_after_header and not found_title:
                    # This is the start of the title
                    found_title = True
                    title_lines.append(stripped)
                elif found_title:
                    title_lines.append(stripped)
                elif not blank_after_header:
                    # Title on same line group as CHAPTER
                    found_title = True
                    title_lines.append(stripped)

            title = ' '.join(title_lines) if title_lines else f"Chapter {ch_roman}"

            # Find the actual content start (after title and blank lines)
            content_lines = []
            in_content = False
            for j in range(content_start, len(ch_lines)):
                stripped = ch_lines[j].strip()
                if not in_content:
                    if stripped and not stripped == title:
                        in_content = True
                        content_lines.append(ch_lines[j])
                else:
                    content_lines.append(ch_lines[j])

            content = '\n'.join(content_lines)
            content = clean_text(content)

            all_chapters.append({
                "book_num": book_num,
                "book_title": book_title,
                "book_subtitle": book_subtitle,
                "chapter_num": ch_num,
                "chapter_roman": ch_roman,
                "title": title,
                "content": content,
            })

    return all_chapters


# Thematic groupings
THEMES = [
    {
        "id": "theme-humility-self-knowledge",
        "name": "Humility and Self-Knowledge",
        "description": "The foundation of the spiritual life: knowing oneself truly, thinking lowly of oneself, and finding freedom in that lowliness. Thomas returns to this theme obsessively — not as self-hatred, but as the ground from which genuine love can grow.",
        "for_readers": "These chapters speak directly to the inner critic and the need for validation. Linehan's radical acceptance shares this root: see yourself clearly, without judgment, and begin from there.",
        "chapters": [
            (1, 1), (1, 2), (1, 7), (1, 11), (1, 19), (1, 22), (1, 25),
            (2, 2), (2, 5),
            (3, 4), (3, 7), (3, 8), (3, 14), (3, 20), (3, 40),
        ],
    },
    {
        "id": "theme-detachment-world",
        "name": "Detachment from the World",
        "description": "Letting go of worldly attachments, honors, pleasures, and the opinions of others. Not hatred of the world, but freedom from its grip — so that the soul can turn toward what is eternal and real.",
        "for_readers": "For anyone feeling trapped by external expectations. These chapters offer permission to stop performing, stop accumulating, stop seeking approval.",
        "chapters": [
            (1, 1), (1, 6), (1, 10), (1, 20),
            (2, 1),
            (3, 9), (3, 10), (3, 16), (3, 27), (3, 31), (3, 32), (3, 41), (3, 42), (3, 43), (3, 44),
        ],
    },
    {
        "id": "theme-inner-life-silence",
        "name": "The Inner Life and Silence",
        "description": "Thomas's deepest teaching: the soul must turn inward, away from noise and distraction, to hear the voice of Christ within. Solitude, silence, and recollection are not luxuries but necessities of the spiritual life.",
        "for_readers": "A contemplative practice manual written centuries before mindfulness became a buzzword. These chapters teach the art of inner attention.",
        "chapters": [
            (1, 10), (1, 20), (1, 21),
            (2, 1), (2, 6),
            (3, 1), (3, 2), (3, 3), (3, 16), (3, 21), (3, 25),
        ],
    },
    {
        "id": "theme-suffering-patience",
        "name": "Suffering, Patience, and the Cross",
        "description": "The royal way of the Holy Cross: suffering is not punishment but transformation. Thomas sees every trial as an invitation to deeper surrender. The cross is not merely endured — it is embraced as the path to freedom.",
        "for_readers": "For those in pain. These chapters do not minimize suffering but reframe it entirely — not as meaningless but as the refining fire of love. Resonates deeply with DBT's distress tolerance.",
        "chapters": [
            (1, 12), (1, 13), (1, 24),
            (2, 9), (2, 11), (2, 12),
            (3, 12), (3, 18), (3, 19), (3, 29), (3, 35), (3, 46), (3, 47), (3, 48), (3, 50), (3, 56),
        ],
    },
    {
        "id": "theme-love-devotion",
        "name": "Divine Love and Devotion",
        "description": "The heart of the book: love of God above all things, love of Jesus as friend and beloved. Thomas writes with the ardor of a mystic lover — not theological argument but direct, passionate devotion.",
        "for_readers": "The emotional core of Christian mysticism. Whether or not you share the theology, these chapters reveal what it means to give the whole heart to something greater than oneself.",
        "chapters": [
            (2, 7), (2, 8),
            (3, 5), (3, 6), (3, 21), (3, 34),
            (4, 1), (4, 2), (4, 13), (4, 14), (4, 17),
        ],
    },
    {
        "id": "theme-grace-nature",
        "name": "Grace versus Nature",
        "description": "The great struggle between the movements of nature (self-will, pride, desire) and the movements of grace (surrender, humility, love). Thomas maps these opposing forces with psychological precision.",
        "for_readers": "A medieval cognitive-behavioral framework. Thomas distinguishes the voice of ego from the voice of grace with startling clarity — directly ancestral to Linehan's distinction between emotion mind and wise mind.",
        "chapters": [
            (3, 53), (3, 54), (3, 55), (3, 56), (3, 57), (3, 58), (3, 59),
        ],
    },
    {
        "id": "theme-sacramental-life",
        "name": "The Sacramental Life",
        "description": "The entire Fourth Book: on receiving the Eucharist with reverence, devotion, and self-emptying. For Thomas, the Sacrament is the supreme meeting place of human and divine — where all the book's teachings converge in a single act of communion.",
        "for_readers": "Even outside a sacramental tradition, these chapters speak to the question: How do we prepare ourselves to receive what is sacred? How do we approach the holy without domesticating it?",
        "chapters": [
            (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
            (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15),
            (4, 16), (4, 17), (4, 18),
        ],
    },
]


def make_chapter_id(book_num, chapter_num):
    return f"book-{book_num}-ch-{chapter_num}"


def build_grammar(chapters):
    items = []
    sort_order = 0

    # L1: Individual chapters
    for ch in chapters:
        sort_order += 1
        ch_id = make_chapter_id(ch["book_num"], ch["chapter_num"])

        # Determine section names based on book
        sections = {}
        if ch["book_num"] == 3:
            # Book 3 is dialogue; some chapters have "The Voice of the Beloved" / "The Voice of the Disciple"
            sections["Teaching"] = ch["content"]
        elif ch["book_num"] == 4:
            sections["Meditation"] = ch["content"]
        else:
            sections["Teaching"] = ch["content"]

        items.append({
            "id": ch_id,
            "name": f"Book {ch['book_num']}, Ch. {ch['chapter_num']}: {ch['title']}",
            "level": 1,
            "category": f"book-{ch['book_num']}",
            "sort_order": sort_order,
            "sections": sections,
            "keywords": [],
            "metadata": {
                "book_number": ch["book_num"],
                "book_title": ch["book_subtitle"],
                "chapter_number": ch["chapter_num"],
                "chapter_roman": ch["chapter_roman"],
            }
        })

    # L2: The four books
    book_data = [
        {
            "id": "book-1",
            "name": "Book 1: Admonitions Profitable for the Spiritual Life",
            "about": "Twenty-five practical counsels for those beginning the spiritual journey: humility, detachment, resisting temptation, the love of solitude, meditation on death. Thomas lays the foundation — not doctrine but discipline, not theology but the daily work of turning the soul toward God.",
            "book_num": 1,
        },
        {
            "id": "book-2",
            "name": "Book 2: Admonitions Concerning the Inner Life",
            "about": "Twelve chapters on the interior landscape: the inward life, submission, peace of conscience, the love of Jesus, the way of the Cross. The focus shifts from external behavior to the movements of the heart. This is the pivot of the book — from doing to being.",
            "book_num": 2,
        },
        {
            "id": "book-3",
            "name": "Book 3: On Inward Consolation",
            "about": "The longest and most intimate book: fifty-nine chapters of dialogue between Christ and the soul. Thomas ventriloquizes the voice of the Beloved, offering consolation, instruction, and correction. This is the mystical heart of the work — direct encounter with the divine.",
            "book_num": 3,
        },
        {
            "id": "book-4",
            "name": "Book 4: Of the Sacrament of the Altar",
            "about": "Eighteen chapters on the Eucharist: preparation, reverence, gratitude, and the mystery of communion. The book culminates here — all the self-emptying and inner purification of the first three books prepares the soul for this one act of receiving.",
            "book_num": 4,
        },
    ]

    for bd in book_data:
        sort_order += 1
        composite = [make_chapter_id(bd["book_num"], ch["chapter_num"])
                     for ch in chapters if ch["book_num"] == bd["book_num"]]
        items.append({
            "id": bd["id"],
            "name": bd["name"],
            "level": 2,
            "category": "book",
            "relationship_type": "emergence",
            "composite_of": composite,
            "sort_order": sort_order,
            "sections": {
                "About": bd["about"],
            },
            "keywords": [],
            "metadata": {"book_number": bd["book_num"], "chapter_count": len(composite)}
        })

    # L2: Thematic groupings
    for theme in THEMES:
        sort_order += 1
        composite = [make_chapter_id(b, c) for b, c in theme["chapters"]]
        # Deduplicate while preserving order
        seen = set()
        unique_composite = []
        for cid in composite:
            if cid not in seen:
                seen.add(cid)
                unique_composite.append(cid)

        items.append({
            "id": theme["id"],
            "name": theme["name"],
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": unique_composite,
            "sort_order": sort_order,
            "sections": {
                "About": theme["description"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {"chapter_count": len(unique_composite)}
        })

    # L3: Meta-categories
    sort_order += 1
    items.append({
        "id": "meta-four-books",
        "name": "The Four Books: A Journey Inward",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": ["book-1", "book-2", "book-3", "book-4"],
        "sort_order": sort_order,
        "sections": {
            "About": "The Imitation of Christ traces a spiral inward: from external conduct (Book 1) to interior disposition (Book 2) to mystical dialogue (Book 3) to sacramental union (Book 4). Each book presupposes the one before it. You cannot hear the voice of the Beloved until you have learned silence; you cannot receive the Sacrament truly until you have emptied yourself of self-will. The structure is itself a teaching: the spiritual life is not a set of beliefs but a progressive transformation of the whole person.",
        },
        "keywords": [],
        "metadata": {}
    })

    sort_order += 1
    items.append({
        "id": "meta-themes",
        "name": "Seven Streams: The Inner Topography of Devotion",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": [t["id"] for t in THEMES],
        "sort_order": sort_order,
        "sections": {
            "About": "Seven thematic currents flow through The Imitation of Christ, crossing the boundaries of the four books. Humility and self-knowledge form the foundation; detachment clears the ground; silence opens the ear; suffering purifies; love ignites; grace transforms; and the Sacrament consummates. A single chapter may touch several themes at once — the book is woven, not divided. These groupings are doorways, not walls.",
        },
        "keywords": [],
        "metadata": {"theme_count": len(THEMES)}
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    chapters = parse_text(text)
    print(f"Parsed {len(chapters)} chapters across {len(set(ch['book_num'] for ch in chapters))} books")

    for b in range(1, 5):
        b_chapters = [ch for ch in chapters if ch["book_num"] == b]
        print(f"  Book {b}: {len(b_chapters)} chapters")

    items = build_grammar(chapters)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Thomas à Kempis", "date": "c. 1418-1427", "note": "Author (attributed)"},
                {"name": "William Benham", "date": "1886", "note": "English translator"},
            ]
        },
        "name": "The Imitation of Christ",
        "description": "The Imitation of Christ by Thomas à Kempis (c. 1418-1427) is the most widely read Christian devotional work after the Bible. Four books of practical mysticism: from external discipline through interior silence to mystical dialogue with Christ and sacramental union. William Benham translation.\n\nSource: Project Gutenberg eBook #1653 (https://www.gutenberg.org/ebooks/1653)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Medieval illuminated manuscript traditions, particularly the Devotio Moderna style of the Low Countries (15th century). The woodcuts of early printed editions (1470s-1500s) capture the austere beauty of the text. Also: Fra Angelico's frescoes at San Marco, Florence — their luminous simplicity matches Thomas's devotional intensity.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["christian-mysticism", "devotional", "medieval", "sacred-text", "public-domain", "full-text", "contemplative", "monastic"],
        "roots": ["christian-mysticism", "contemplative-practice"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan", "Shrei"],
        "worldview": "devotional",
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
