#!/usr/bin/env python3
"""
Build grammar for Dark Night of the Soul by St. John of the Cross.
Expected source: 16th-century Spanish mystical text on the soul's journey through darkness to union with God.

NOTE: The seed file seeds/dark-night-of-the-soul.txt currently contains the WRONG text.
The Gutenberg eBook #21001 is actually "Terre-Neuve et les Terre-Neuviennes" by Henri de La Chaume
(a French book about Newfoundland), NOT Dark Night of the Soul.

Dark Night of the Soul is NOT available on the main Project Gutenberg site (gutenberg.org).
It IS available from:
  - Christian Classics Ethereal Library (CCEL): https://www.ccel.org/ccel/john_cross/dark_night.html
  - HolyBooks.com: https://www.holybooks.com/dark-night-of-the-soul-saint-john/
  - Carmelite Monks: https://www.carmelitemonks.org/Vocation/DarkNight-StJohnoftheCross.pdf
  - Internet Archive: https://archive.org/details/darknightofsoul00sain

This parser will:
1. Check if the seed file contains the correct text
2. If correct, parse it into a grammar (the text has 2 Books with multiple chapters each)
3. If wrong, print an error with instructions

Expected text structure (David Lewis translation, or E. Allison Peers):
- Poem: "In a dark night" (stanzas of the poem)
- Book I: The Dark Night of the Senses (13-14 chapters)
- Book II: The Dark Night of the Spirit (24-25 chapters)
"""

import json
import re
import os
import sys

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'dark-night-of-the-soul.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'dark-night-of-the-soul')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')


def read_seed():
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = '*** START OF THE PROJECT GUTENBERG EBOOK'
    end_marker = '*** END OF THE PROJECT GUTENBERG EBOOK'
    start_idx = text.find(start_marker)
    if start_idx != -1:
        start_idx = text.index('\n', start_idx) + 1
    else:
        start_idx = 0
    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = len(text)
    return text[start_idx:end_idx].strip()


def verify_content(text):
    """Check if the seed file contains Dark Night of the Soul."""
    indicators = [
        'dark night',
        'john of the cross',
        'purgation',
        'contemplation',
        'soul',
    ]
    text_lower = text[:5000].lower()
    matches = sum(1 for ind in indicators if ind in text_lower)
    return matches >= 3


def roman_to_int(s):
    """Convert Roman numeral to integer."""
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    s = s.upper().strip()
    for i, c in enumerate(s):
        if c not in vals:
            return 0
        v = vals[c]
        if i + 1 < len(s) and vals.get(s[i + 1], 0) > v:
            result -= v
        else:
            result += v
    return result


def parse_books_and_chapters(text):
    """Parse the text into books and chapters."""
    items = []

    # Try to find Book divisions
    book_pattern = re.compile(r'\n\s*(BOOK\s+(I{1,3}|ONE|TWO|THE\s+\w+))\s*\n', re.IGNORECASE)
    chapter_pattern = re.compile(r'\n\s*(CHAPTER\s+([IVXLC]+|\d+))\s*\n', re.IGNORECASE)

    book_matches = list(book_pattern.finditer(text))
    chapter_matches = list(chapter_pattern.finditer(text))

    if not chapter_matches:
        print("WARNING: No chapter markers found")
        return items

    for i, match in enumerate(chapter_matches):
        num_str = match.group(2)
        try:
            num = int(num_str)
        except ValueError:
            num = roman_to_int(num_str)

        content_start = match.end()
        content_end = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(text)
        content = text[content_start:content_end].strip()

        # Remove footnotes
        content = re.sub(r'\n\[(\d+)\][^\n]*', '', content)
        content = re.sub(r'\[(\d+)\]', '', content)
        content = re.sub(r'\n{3,}', '\n\n', content).strip()

        # Determine which book this chapter belongs to
        book_num = 1
        for bm in book_matches:
            if bm.start() < match.start():
                book_text = bm.group(2).upper()
                if 'II' in book_text or 'TWO' in book_text or 'SECOND' in book_text:
                    book_num = 2

        items.append({
            'book': book_num,
            'chapter': num,
            'text': content,
        })

    return items


def build_grammar(parsed_items):
    """Build the complete grammar."""
    items = []
    sort_order = 0

    for pi in parsed_items:
        item_id = f"book-{pi['book']}-ch-{pi['chapter']}"
        name = f"Book {pi['book']}, Chapter {pi['chapter']}"

        # Extract first sentence as subtitle
        match = re.match(r'([^.!?]+[.!?])', pi['text'][:200])
        if match:
            sub = match.group(1).strip()
            if len(sub) > 80:
                sub = sub[:77] + '...'
            name += f": {sub}"

        book_cat = 'dark-night-of-senses' if pi['book'] == 1 else 'dark-night-of-spirit'

        text_lower = pi['text'].lower()
        keywords = []
        for term, kw in [
            ('dark', 'darkness'), ('night', 'night'), ('soul', 'soul'),
            ('purgation', 'purgation'), ('love', 'love'), ('contemplation', 'contemplation'),
            ('suffering', 'suffering'), ('prayer', 'prayer'), ('union', 'union'),
        ]:
            if term in text_lower:
                keywords.append(kw)

        items.append({
            'id': item_id,
            'name': name,
            'sort_order': sort_order,
            'category': book_cat,
            'level': 1,
            'sections': {'Text': pi['text']},
            'keywords': keywords[:6],
            'metadata': {'book': pi['book'], 'chapter': pi['chapter']}
        })
        sort_order += 1

    # L2: Book groupings
    book1_ids = [i['id'] for i in items if i.get('metadata', {}).get('book') == 1]
    book2_ids = [i['id'] for i in items if i.get('metadata', {}).get('book') == 2]

    if book1_ids:
        items.append({
            'id': 'dark-night-of-senses',
            'name': 'Book I: The Dark Night of the Senses',
            'sort_order': sort_order,
            'category': 'book',
            'level': 2,
            'composite_of': book1_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': "The first stage of the soul's purification: the night of the senses. John of the Cross describes how God withdraws sensory consolations from the soul, leaving it in dryness, darkness, and apparent abandonment. This is not punishment but medicine -- the soul is being weaned from attachment to spiritual pleasure so it can begin to love God for God's own sake. John catalogs the seven capital sins as they manifest in spiritual life, showing how each is purged through the dark night.",
                'For Readers': "If you have ever experienced spiritual dryness -- a time when prayer feels empty, when God seems absent, when the practices that once brought joy now bring nothing -- John of the Cross is speaking directly to you. His radical insight: this is not failure but progress."
            },
            'keywords': ['senses', 'purgation', 'dryness', 'beginners'],
            'metadata': {}
        })
        sort_order += 1

    if book2_ids:
        items.append({
            'id': 'dark-night-of-spirit',
            'name': 'Book II: The Dark Night of the Spirit',
            'sort_order': sort_order,
            'category': 'book',
            'level': 2,
            'composite_of': book2_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': "The deeper and more terrible purification: the night of the spirit. Here the soul undergoes a radical transformation at the very center of its being. The darkness is more profound, the suffering more acute, but the purpose is the same: the soul is being prepared for union with God. John describes this night as a 'living death' -- the old self dying so that the new self, united with the divine, can be born. The concluding chapters describe the dawn of contemplative union.",
                'For Readers': "This is among the most intense spiritual writing in any tradition. John does not soften the experience but insists that the darkness itself is the light -- that what feels like God's absence is actually God's overwhelming presence, too bright for the soul's weak eyes."
            },
            'keywords': ['spirit', 'deep-purgation', 'union', 'transformation'],
            'metadata': {}
        })
        sort_order += 1

    # L3
    l2_ids = [i['id'] for i in items if i['level'] == 2]
    if l2_ids:
        items.append({
            'id': 'the-dark-night',
            'name': 'The Dark Night of the Soul',
            'sort_order': sort_order,
            'category': 'meta-theme',
            'level': 3,
            'composite_of': l2_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': "St. John of the Cross's Dark Night of the Soul is one of the most profound works in the literature of mysticism. Written by a 16th-century Spanish Carmelite friar who himself endured imprisonment and torture, it maps the soul's journey through two successive 'nights' of purification -- the night of the senses and the night of the spirit -- toward union with God. The central paradox: what appears as abandonment is actually the deepest intimacy; what feels like death is actually birth. The phrase 'dark night of the soul' has entered common language, but its original meaning is far richer and more hopeful than popular usage suggests.",
                'Legacy': "John of the Cross profoundly influenced Teresa of Avila, the Carmelite tradition, and all subsequent Western mysticism. His psychological mapping of spiritual development anticipates modern understandings of transformative suffering. Marsha Linehan's DBT work on 'radical acceptance' of suffering as a path to transformation echoes John's teaching that the dark night is not an obstacle to growth but the means of growth itself."
            },
            'keywords': ['dark-night', 'mysticism', 'purification', 'union', 'transformation'],
            'metadata': {}
        })

    grammar = {
        '_grammar_commons': {
            'schema_version': '1.0',
            'license': 'CC-BY-SA-4.0',
            'attribution': [
                {'name': 'St. John of the Cross', 'date': '1577-1579', 'note': 'Author, Spanish Carmelite mystic'},
                {'name': 'David Lewis', 'date': '1864', 'note': 'English translator (or E. Allison Peers, 1935)'}
            ]
        },
        'name': 'Dark Night of the Soul',
        'description': (
            "St. John of the Cross's Dark Night of the Soul (c. 1577-1579) -- a 16th-century masterpiece of "
            "mystical literature mapping the soul's journey through darkness and purification toward union with "
            "God. Written by a Spanish Carmelite friar who endured imprisonment, it teaches that spiritual "
            "dryness and suffering are not signs of God's absence but of God's deepest work in the soul. "
            "The phrase 'dark night of the soul' has entered common speech, but the original is far richer "
            "and more hopeful than popular usage.\n\n"
            "Note: This text is not available on the main Project Gutenberg site. The seed file should be "
            "sourced from CCEL, HolyBooks.com, or Internet Archive.\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: El Greco's mystical paintings. "
            "Zurbar\u00e1n's Carmelite monks. Spanish baroque religious art. "
            "Images of the Carmelite monastery at Segovia where John was imprisoned."
        ),
        'grammar_type': 'custom',
        'creator_name': 'PlayfulProcess',
        'tags': ['mysticism', 'christian', 'contemplative', 'carmelite', 'wisdom', 'suffering', 'transformation'],
        'roots': ['western-mysticism', 'contemplative-practice'],
        'shelves': ['wisdom'],
        'lineages': ['Linehan'],
        'worldview': 'contemplative',
        'items': items
    }

    return grammar


def main():
    raw = read_seed()
    text = strip_gutenberg(raw)

    if not verify_content(text):
        print("ERROR: The seed file does not contain Dark Night of the Soul.")
        print()
        print("The file seeds/dark-night-of-the-soul.txt currently contains a French")
        print("book about Newfoundland (Gutenberg eBook #21001: 'Terre-Neuve et les")
        print("Terre-Neuviennes' by Henri de La Chaume).")
        print()
        print("Dark Night of the Soul is NOT available on the main Project Gutenberg site.")
        print("To obtain the correct text, download from one of these sources:")
        print()
        print("  CCEL: https://www.ccel.org/ccel/john_cross/dark_night.html")
        print("  HolyBooks: https://www.holybooks.com/dark-night-of-the-soul-saint-john/")
        print("  Carmelite Monks: https://www.carmelitemonks.org/Vocation/DarkNight-StJohnoftheCross.pdf")
        print("  Internet Archive: https://archive.org/details/darknightofsoul00sain")
        print()
        print("Save the text as seeds/dark-night-of-the-soul.txt and re-run this script.")
        sys.exit(1)

    parsed = parse_books_and_chapters(text)
    print(f"Found {len(parsed)} chapters")

    grammar = build_grammar(parsed)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    item_counts = {}
    for item in grammar['items']:
        level = item['level']
        item_counts[level] = item_counts.get(level, 0) + 1

    print(f"\nGrammar written to {OUTPUT_PATH}")
    for level in sorted(item_counts):
        print(f"  L{level} items: {item_counts[level]}")
    print(f"  Total: {len(grammar['items'])} items")


if __name__ == '__main__':
    main()
