#!/usr/bin/env python3
"""
Build grammar for The Interior Castle by St. Teresa of Avila.
Expected source: 16th-century Spanish mystical text on the soul's journey through
seven "mansions" or dwelling places toward union with God.

NOTE: The seed file seeds/interior-castle.txt currently contains the WRONG text.
The Gutenberg eBook #45060 is actually "La Comedie humaine - Volume 03" by Honore de Balzac
(a French novel), NOT The Interior Castle.

The Interior Castle is NOT available on the main Project Gutenberg site (gutenberg.org).
The Gutenberg author page for Teresa of Avila (author #2651) lists only her autobiography
and an appreciation, not The Interior Castle. It IS available from:
  - Carmelite Monks: https://www.carmelitemonks.org/Vocation/StTeresa-TheInteriorCastle.pdf
  - Internet Archive: https://archive.org/details/interiorcastleor00tere
  - CCEL (Christian Classics Ethereal Library)

This parser will:
1. Check if the seed file contains the correct text
2. If correct, parse it into a grammar (7 Mansions/Dwelling Places, each with chapters)
3. If wrong, print an error with instructions

Expected text structure (E. Allison Peers or Benedictines of Stanbrook translations):
- Seven Mansions (Moradas), each with multiple chapters
- First Mansion: Self-knowledge and the beginning of prayer
- Second Mansion: The practice of prayer amid temptation
- Third Mansion: The danger of false security
- Fourth Mansion: The prayer of quiet (supernatural prayer begins)
- Fifth Mansion: The prayer of union
- Sixth Mansion: Spiritual betrothal (the longest section)
- Seventh Mansion: Spiritual marriage / full union with God
"""

import json
import re
import os
import sys

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'interior-castle.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'interior-castle')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

MANSION_NAMES = {
    1: "The First Mansion: Self-Knowledge",
    2: "The Second Mansion: The Practice of Prayer",
    3: "The Third Mansion: The Danger of False Security",
    4: "The Fourth Mansion: The Prayer of Quiet",
    5: "The Fifth Mansion: The Prayer of Union",
    6: "The Sixth Mansion: Spiritual Betrothal",
    7: "The Seventh Mansion: Spiritual Marriage",
}

MANSION_DESCRIPTIONS = {
    1: "The outermost rooms of the castle, where the soul first begins to turn inward. Teresa teaches that self-knowledge is the foundation of all spiritual growth. Here the soul is still surrounded by worldly distractions -- 'reptiles and vermin' that keep it from going deeper -- but has heard the King's call and begun to respond.",
    2: "The soul that has begun to practice prayer now faces fierce temptation to turn back. The devil's assaults are strongest here, because the soul is beginning to be dangerous to him. Teresa encourages perseverance: the struggles of this mansion are signs of real spiritual progress, not of failure.",
    3: "A deceptive resting place where the soul, having achieved some virtue and regularity in prayer, may believe it has arrived. Teresa warns that this false security is perilous -- the soul must be willing to let go of its own goodness and enter the deeper, darker mansions where God does the work.",
    4: "The great turning point: here supernatural prayer begins. The 'prayer of quiet' is God's gift, not the soul's achievement. Teresa distinguishes between the 'consolations' of meditation (which the soul produces) and the 'spiritual delights' of contemplation (which God gives). The water metaphor: the first three mansions are like water carried by aqueduct; from here, the spring rises from within.",
    5: "The prayer of union, in which the soul is absorbed in God for short periods. Teresa uses the famous image of the silkworm that dies in its cocoon and is reborn as a butterfly -- the old self must die for the new self to emerge. This is brief, overwhelming, and utterly beyond the soul's control.",
    6: "The longest and most complex section, describing spiritual betrothal -- the period of intense purification and extraordinary graces that precedes the final union. Teresa describes visions, locutions, raptures, and the 'wound of love,' alongside terrible suffering, illness, and misunderstanding. This is the dark night at its most acute.",
    7: "The innermost room where the King dwells. Spiritual marriage: permanent, peaceful, unshakeable union with God. Teresa describes this not as ecstasy but as a deep, quiet certainty -- 'the centre of the soul.' The fruit of this union is not withdrawal from the world but extraordinary practical love: 'Martha and Mary must work together.'",
}


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
    """Check if the seed file contains The Interior Castle."""
    indicators = [
        'interior castle',
        'mansions',
        'dwelling',
        'teresa',
        'prayer',
        'morada',
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


def parse_mansions_and_chapters(text):
    """Parse into mansions and chapters."""
    items = []

    # Various patterns for mansion/dwelling headers
    mansion_pattern = re.compile(
        r'\n\s*((?:THE\s+)?(?:FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH)\s+(?:MANSION|DWELLING|MORADA)S?)\s*\n',
        re.IGNORECASE
    )
    chapter_pattern = re.compile(
        r'\n\s*(CHAPTER\s+([IVXLC]+|\d+))\s*\n',
        re.IGNORECASE
    )

    mansion_matches = list(mansion_pattern.finditer(text))
    chapter_matches = list(chapter_pattern.finditer(text))

    if not chapter_matches:
        print("WARNING: No chapter markers found")
        return items

    # Map ordinals to numbers
    ordinal_map = {
        'FIRST': 1, 'SECOND': 2, 'THIRD': 3, 'FOURTH': 4,
        'FIFTH': 5, 'SIXTH': 6, 'SEVENTH': 7
    }

    # Build mansion position map
    mansion_positions = []
    for mm in mansion_matches:
        text_upper = mm.group(1).upper()
        for word, num in ordinal_map.items():
            if word in text_upper:
                mansion_positions.append((mm.start(), num))
                break

    for i, match in enumerate(chapter_matches):
        num_str = match.group(2)
        try:
            ch_num = int(num_str)
        except ValueError:
            ch_num = roman_to_int(num_str)

        content_start = match.end()
        content_end = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(text)
        content = text[content_start:content_end].strip()

        # Remove footnotes
        content = re.sub(r'\n\[(\d+)\][^\n]*', '', content)
        content = re.sub(r'\[(\d+)\]', '', content)
        content = re.sub(r'\n{3,}', '\n\n', content).strip()

        # Determine mansion
        mansion_num = 1
        for pos, mnum in mansion_positions:
            if pos < match.start():
                mansion_num = mnum

        items.append({
            'mansion': mansion_num,
            'chapter': ch_num,
            'text': content,
        })

    return items


def build_grammar(parsed_items):
    """Build the complete grammar."""
    items = []
    sort_order = 0

    for pi in parsed_items:
        item_id = f"mansion-{pi['mansion']}-ch-{pi['chapter']}"
        name = f"Mansion {pi['mansion']}, Chapter {pi['chapter']}"

        match = re.match(r'([^.!?]+[.!?])', pi['text'][:200])
        if match:
            sub = match.group(1).strip()
            if len(sub) > 70:
                sub = sub[:67] + '...'
            name += f": {sub}"

        text_lower = pi['text'].lower()
        keywords = []
        for term, kw in [
            ('prayer', 'prayer'), ('soul', 'soul'), ('love', 'love'),
            ('union', 'union'), ('mansion', 'mansions'), ('contemplation', 'contemplation'),
            ('humility', 'humility'), ('obedience', 'obedience'), ('suffering', 'suffering'),
        ]:
            if term in text_lower:
                keywords.append(kw)

        items.append({
            'id': item_id,
            'name': name,
            'sort_order': sort_order,
            'category': f'mansion-{pi["mansion"]}',
            'level': 1,
            'sections': {'Text': pi['text']},
            'keywords': keywords[:6],
            'metadata': {'mansion': pi['mansion'], 'chapter': pi['chapter']}
        })
        sort_order += 1

    # L2: One per mansion
    for m in range(1, 8):
        mansion_ids = [i['id'] for i in items if i.get('metadata', {}).get('mansion') == m]
        if mansion_ids:
            items.append({
                'id': f'mansion-{m}',
                'name': MANSION_NAMES.get(m, f'Mansion {m}'),
                'sort_order': sort_order,
                'category': 'mansion',
                'level': 2,
                'composite_of': mansion_ids,
                'relationship_type': 'emergence',
                'sections': {
                    'About': MANSION_DESCRIPTIONS.get(m, ''),
                    'For Readers': f"{'This is the beginning of the journey. Teresa writes with warmth and humor, encouraging the reader not to be afraid.' if m <= 2 else 'Read contemplatively, allowing Teresa to guide you inward.'}"
                },
                'keywords': ['mansion', 'dwelling', 'prayer', 'journey'],
                'metadata': {'mansion_number': m}
            })
            sort_order += 1

    # Thematic groupings
    outer_ids = [f'mansion-{i}' for i in range(1, 4) if any(it['id'] == f'mansion-{i}' for it in items)]
    inner_ids = [f'mansion-{i}' for i in range(4, 8) if any(it['id'] == f'mansion-{i}' for it in items)]

    if outer_ids:
        items.append({
            'id': 'outer-mansions',
            'name': 'The Outer Mansions: Human Effort and the Active Life',
            'sort_order': sort_order,
            'category': 'thematic-group',
            'level': 2,
            'composite_of': outer_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': "The first three mansions represent the soul's active work: self-knowledge, perseverance in prayer, and the cultivation of virtue. Here the soul labors with its own powers, and God cooperates. Teresa calls these the 'mansions of humility.' The danger is stopping here and mistaking moral goodness for spiritual maturity.",
                'For Readers': "These mansions map onto the beginning of any contemplative journey. They are about showing up, doing the work, and not giving up when it feels dry or difficult."
            },
            'keywords': ['active-life', 'effort', 'beginners', 'humility'],
            'metadata': {}
        })
        sort_order += 1

    if inner_ids:
        items.append({
            'id': 'inner-mansions',
            'name': 'The Inner Mansions: Divine Gift and the Contemplative Life',
            'sort_order': sort_order,
            'category': 'thematic-group',
            'level': 2,
            'composite_of': inner_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': "From the Fourth Mansion onward, the initiative passes from the soul to God. Supernatural prayer begins, the soul is progressively purified and transformed, and the journey culminates in the Seventh Mansion's 'spiritual marriage' -- permanent, peaceful union with God. Teresa insists this is not withdrawal from the world but the foundation for extraordinary love and service.",
                'For Readers': "Teresa writes from direct experience. She describes states that few reach but does so with such clarity and practicality that the reader feels she is a trustworthy guide, not a distant authority."
            },
            'keywords': ['contemplative-life', 'divine-gift', 'union', 'transformation'],
            'metadata': {}
        })
        sort_order += 1

    # L3
    l2_ids = [i['id'] for i in items if i['level'] == 2]
    if l2_ids:
        items.append({
            'id': 'the-interior-castle',
            'name': 'The Interior Castle',
            'sort_order': sort_order,
            'category': 'meta-theme',
            'level': 3,
            'composite_of': l2_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': "St. Teresa of Avila's Interior Castle (1577) is the supreme masterpiece of mystical psychology -- a complete map of the soul's journey from the outermost rooms of self-knowledge to the innermost chamber where God dwells. Written at the command of her confessor when Teresa was sixty-two, it draws on decades of contemplative experience to describe, with extraordinary precision, warmth, and humor, the seven 'mansions' or stages of the spiritual life. The governing image -- the soul as a crystal castle with God at its center -- is one of the most powerful in spiritual literature.",
                'Legacy': "Teresa's Interior Castle is the companion volume to John of the Cross's Dark Night -- where John maps the purification, Teresa maps the growth. Together they form the most complete description of the contemplative journey in Western literature. Teresa's influence extends through the Carmelite tradition, through Edith Stein's philosophical appropriation, through Thomas Merton, and into contemporary contemplative practice. Her insistence that the highest spiritual states produce not withdrawal but active love anticipates the engaged spirituality movements of the 20th and 21st centuries."
            },
            'keywords': ['castle', 'mansions', 'mysticism', 'prayer', 'union', 'journey'],
            'metadata': {}
        })

    grammar = {
        '_grammar_commons': {
            'schema_version': '1.0',
            'license': 'CC-BY-SA-4.0',
            'attribution': [
                {'name': 'St. Teresa of Avila', 'date': '1577', 'note': 'Author, Spanish Carmelite reformer and Doctor of the Church'},
                {'name': 'Benedictines of Stanbrook', 'date': '1921', 'note': 'English translators (or E. Allison Peers, 1946)'}
            ]
        },
        'name': 'The Interior Castle',
        'description': (
            "St. Teresa of Avila's Interior Castle (1577) -- the supreme masterpiece of mystical psychology, "
            "mapping the soul's journey through seven 'mansions' or dwelling places from self-knowledge to "
            "divine union. Written at sixty-two from decades of contemplative experience, Teresa describes "
            "with extraordinary precision, warmth, and humor the progressive stages of prayer, purification, "
            "and transformation. Her governing image -- the soul as a crystal castle with God at its luminous "
            "center -- is one of the most powerful in all spiritual literature.\n\n"
            "Note: This text is not available on the main Project Gutenberg site. The seed file should be "
            "sourced from CCEL, Carmelite Monks, or Internet Archive.\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Spanish baroque religious art. "
            "Bernini's Ecstasy of Saint Teresa. Paintings of Avila's medieval walls and castle. "
            "17th-century Carmelite convent imagery."
        ),
        'grammar_type': 'custom',
        'creator_name': 'PlayfulProcess',
        'tags': ['mysticism', 'christian', 'contemplative', 'carmelite', 'wisdom', 'prayer', 'feminine-voice'],
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
        print("ERROR: The seed file does not contain The Interior Castle.")
        print()
        print("The file seeds/interior-castle.txt currently contains Balzac's")
        print("'La Comedie humaine - Volume 03' in French (Gutenberg eBook #45060).")
        print()
        print("The Interior Castle is NOT available on the main Project Gutenberg site.")
        print("Teresa of Avila's Gutenberg author page (#2651) lists only her autobiography.")
        print("To obtain the correct text, download from one of these sources:")
        print()
        print("  Carmelite Monks: https://www.carmelitemonks.org/Vocation/StTeresa-TheInteriorCastle.pdf")
        print("  Internet Archive: https://archive.org/details/interiorcastleor00tere")
        print("  CCEL: Christian Classics Ethereal Library")
        print()
        print("Save as plain text to seeds/interior-castle.txt and re-run this script.")
        sys.exit(1)

    parsed = parse_mansions_and_chapters(text)
    print(f"Found {len(parsed)} chapters across {len(set(p['mansion'] for p in parsed))} mansions")

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
