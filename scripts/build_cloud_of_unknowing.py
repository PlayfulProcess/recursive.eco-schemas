#!/usr/bin/env python3
"""
Build grammar for The Cloud of Unknowing.
Expected source: A 14th-century English mystical text, anonymous.

NOTE: The seed file seeds/cloud-of-unknowing.txt currently contains the WRONG text.
The Gutenberg eBook #20508 is actually "Como eu atravessei Africa" (a Portuguese travel book),
NOT The Cloud of Unknowing. The Cloud of Unknowing is not available on the main Project
Gutenberg site (gutenberg.org). It IS available from:
  - Christian Classics Ethereal Library (CCEL): https://ccel.org/ccel/anonymous2/cloud
  - Global Grey: https://www.globalgreyebooks.com/cloud-of-unknowing-ebook.html
  - Internet Archive: https://archive.org/details/bookofcontemplat00unde

This parser will:
1. Check if the seed file contains the correct text
2. If correct, parse it into a grammar
3. If wrong, print an error with instructions

The expected text structure (Evelyn Underhill's 1922 edition):
- 75 short chapters of mystical instruction on contemplative prayer
- The core teaching: approach God not through knowledge but through love,
  entering the "cloud of unknowing" where the intellect falls away
"""

import json
import re
import os
import sys

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'cloud-of-unknowing.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'cloud-of-unknowing')
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
    """Check if the seed file contains The Cloud of Unknowing."""
    indicators = [
        'cloud of unknowing',
        'cloud of forgetting',
        'contemplation',
        'naked intent',
        'this work',
    ]
    text_lower = text[:5000].lower()
    matches = sum(1 for ind in indicators if ind in text_lower)
    return matches >= 3


def parse_chapters(text):
    """Parse the text into chapters. Handles multiple possible formats."""
    chapters = []

    # Try pattern: CHAPTER followed by Roman or Arabic numerals
    chapter_pattern = re.compile(
        r'\n\s*(CHAPTER|Chapter)\s+([IVXLC]+|\d+)\s*\n',
        re.IGNORECASE
    )
    matches = list(chapter_pattern.finditer(text))

    if not matches:
        # Try alternate: just Roman numerals on their own line
        chapter_pattern = re.compile(r'\n\s*([IVXLC]{1,10})\.\s*\n')
        matches = list(chapter_pattern.finditer(text))

    if not matches:
        print("WARNING: Could not find chapter markers in text")
        return chapters

    for i, match in enumerate(matches):
        num_str = match.group(2) if match.lastindex >= 2 else match.group(1)
        try:
            num = int(num_str)
        except ValueError:
            num = roman_to_int(num_str)

        content_start = match.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[content_start:content_end].strip()

        # Remove footnotes
        content = re.sub(r'\n\[(\d+)\][^\n]*', '', content)
        content = re.sub(r'\[(\d+)\]', '', content)
        content = re.sub(r'\n{3,}', '\n\n', content).strip()

        chapters.append({
            'number': num,
            'text': content,
        })

    return chapters


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


def build_grammar(chapters):
    """Build the complete grammar from parsed chapters."""
    items = []
    sort_order = 0

    # L1: individual chapters
    for ch in chapters:
        num = ch['number']
        # Extract first sentence as subtitle
        first_sent = ''
        match = re.match(r'([^.!?]+[.!?])', ch['text'][:200])
        if match:
            first_sent = match.group(1).strip()
            if len(first_sent) > 80:
                first_sent = first_sent[:77] + '...'

        name = f"Chapter {num}"
        if first_sent:
            name += f": {first_sent}"

        text_lower = ch['text'].lower()
        keywords = []
        for term, kw in [
            ('cloud', 'cloud'), ('unknowing', 'unknowing'), ('love', 'love'),
            ('prayer', 'prayer'), ('contemplation', 'contemplation'),
            ('forgetting', 'forgetting'), ('darkness', 'darkness'), ('god', 'God'),
        ]:
            if term in text_lower:
                keywords.append(kw)

        items.append({
            'id': f'chapter-{num}',
            'name': name,
            'sort_order': sort_order,
            'category': 'chapter',
            'level': 1,
            'sections': {'Text': ch['text']},
            'keywords': keywords[:6],
            'metadata': {'chapter_number': num}
        })
        sort_order += 1

    # L2: thematic groups
    all_chapter_ids = [f"chapter-{ch['number']}" for ch in chapters]
    early = [f"chapter-{i}" for i in range(1, 8) if f"chapter-{i}" in set(all_chapter_ids)]
    middle = [f"chapter-{i}" for i in range(8, 40) if f"chapter-{i}" in set(all_chapter_ids)]
    later = [f"chapter-{i}" for i in range(40, 76) if f"chapter-{i}" in set(all_chapter_ids)]

    if early:
        items.append({
            'id': 'the-call-to-contemplation',
            'name': 'The Call to Contemplation',
            'sort_order': sort_order,
            'category': 'thematic-group',
            'level': 2,
            'composite_of': early,
            'relationship_type': 'emergence',
            'sections': {
                'About': "The opening chapters establish the central teaching: that God is to be approached not through knowledge but through love. The author instructs his student to put all created things beneath a 'cloud of forgetting' and reach toward God through the 'cloud of unknowing' with a 'naked intent' of love.",
                'For Readers': "These chapters are the essential introduction. The Cloud author writes with extraordinary directness and warmth, addressing his reader as a friend and fellow traveler."
            },
            'keywords': ['introduction', 'unknowing', 'love', 'contemplation'],
            'metadata': {}
        })
        sort_order += 1

    if middle:
        items.append({
            'id': 'the-practice',
            'name': 'The Practice of Unknowing',
            'sort_order': sort_order,
            'category': 'thematic-group',
            'level': 2,
            'composite_of': middle,
            'relationship_type': 'emergence',
            'sections': {
                'About': "The practical heart of the book: detailed instruction on how to practice contemplative prayer, how to handle distractions, the role of humility, and the difference between the active and contemplative lives. The author teaches the use of short prayer-words and the discipline of repeatedly returning attention to the simple intent of love.",
                'For Readers': "This is where the Cloud becomes a practical manual. The teaching on handling distractions -- acknowledge them, then let them go -- is strikingly similar to modern mindfulness instruction."
            },
            'keywords': ['practice', 'prayer', 'distraction', 'humility'],
            'metadata': {}
        })
        sort_order += 1

    if later:
        items.append({
            'id': 'advanced-teaching',
            'name': 'Advanced Teaching: Discernment and Grace',
            'sort_order': sort_order,
            'category': 'thematic-group',
            'level': 2,
            'composite_of': later,
            'relationship_type': 'emergence',
            'sections': {
                'About': "The later chapters address more advanced topics: the relationship between contemplation and knowledge, warnings against spiritual pride and false mystical experiences, the necessity of grace, and the signs of genuine spiritual progress. The author balances encouragement with caution.",
                'For Readers': "These chapters show the Cloud author at his wisest and most discerning. His warnings against spiritual exhibitionism and self-deception are timeless."
            },
            'keywords': ['discernment', 'grace', 'advanced', 'wisdom'],
            'metadata': {}
        })
        sort_order += 1

    # L3
    l2_ids = [i['id'] for i in items if i['level'] == 2]
    if l2_ids:
        items.append({
            'id': 'the-cloud',
            'name': 'The Cloud of Unknowing',
            'sort_order': sort_order,
            'category': 'meta-theme',
            'level': 3,
            'composite_of': l2_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': "The Cloud of Unknowing is one of the masterpieces of Western mystical literature -- a 14th-century guide to contemplative prayer that teaches approaching God not through thought but through love. Its central image -- the 'cloud of unknowing' between the soul and God, penetrated only by the 'sharp dart of longing love' -- has influenced contemplatives for six centuries. The anonymous author writes with extraordinary warmth, humor, and psychological insight.",
                'Legacy': "The Cloud profoundly influenced the Carmelite mystics (John of the Cross, Teresa of Avila), the Quaker tradition of silent worship, Thomas Merton's contemplative writings, and the modern centering prayer movement. Its emphasis on unknowing as a path to knowledge anticipates apophatic theology across traditions."
            },
            'keywords': ['mysticism', 'contemplation', 'unknowing', 'love', 'prayer'],
            'metadata': {}
        })

    grammar = {
        '_grammar_commons': {
            'schema_version': '1.0',
            'license': 'CC-BY-SA-4.0',
            'attribution': [
                {'name': 'Anonymous', 'date': 'c. 1375', 'note': 'Author, an English contemplative priest'},
                {'name': 'Evelyn Underhill', 'date': '1922', 'note': 'Editor and translator'}
            ]
        },
        'name': 'The Cloud of Unknowing',
        'description': (
            "The Cloud of Unknowing -- a 14th-century masterpiece of English mystical literature by an "
            "anonymous contemplative, teaching that God is to be approached not through knowledge but through "
            "love. The seeker must put all created things beneath a 'cloud of forgetting' and reach toward God "
            "through the 'cloud of unknowing' with nothing but a 'naked intent' of love. One of the most "
            "influential texts in the Western contemplative tradition.\n\n"
            "Note: This text is not available on the main Project Gutenberg site. The seed file should be "
            "sourced from CCEL, Global Grey, or Internet Archive.\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Medieval English manuscript illuminations. "
            "Cloud imagery from medieval psalters and books of hours. Images of contemplative monks "
            "in medieval settings."
        ),
        'grammar_type': 'custom',
        'creator_name': 'PlayfulProcess',
        'tags': ['mysticism', 'christian', 'contemplative', 'medieval', 'wisdom', 'apophatic', 'prayer'],
        'roots': ['western-mysticism', 'contemplative-practice'],
        'shelves': ['wisdom'],
        'lineages': ['Linehan', 'Shrei'],
        'worldview': 'contemplative',
        'items': items
    }

    return grammar


def main():
    raw = read_seed()
    text = strip_gutenberg(raw)

    if not verify_content(text):
        print("ERROR: The seed file does not contain The Cloud of Unknowing.")
        print()
        print("The file seeds/cloud-of-unknowing.txt currently contains a Portuguese")
        print("travel book (Gutenberg eBook #20508: 'Como eu atravessei Africa').")
        print()
        print("The Cloud of Unknowing is NOT available on the main Project Gutenberg site.")
        print("To obtain the correct text, download from one of these sources:")
        print()
        print("  CCEL: https://ccel.org/ccel/anonymous2/cloud")
        print("  Global Grey: https://www.globalgreyebooks.com/cloud-of-unknowing-ebook.html")
        print("  Internet Archive: https://archive.org/details/bookofcontemplat00unde")
        print()
        print("Save the text as seeds/cloud-of-unknowing.txt and re-run this script.")
        sys.exit(1)

    chapters = parse_chapters(text)
    print(f"Found {len(chapters)} chapters")

    if len(chapters) < 70:
        print(f"WARNING: Expected ~75 chapters, found {len(chapters)}")

    grammar = build_grammar(chapters)

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
