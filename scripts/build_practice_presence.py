#!/usr/bin/env python3
"""
Build grammar for The Practice of the Presence of God by Brother Lawrence.
Source: Project Gutenberg eBook #5657

Parses 4 Conversations and 15 Letters from the seed text.
"""

import json
import re
import os

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'practice-presence-of-god.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'practice-presence-of-god')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

# Ordinal words for matching
ORDINALS = [
    'First', 'Second', 'Third', 'Fourth', 'Fifth',
    'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth',
    'Eleventh', 'Twelfth', 'Thirteenth', 'Fourteenth', 'Fifteenth'
]


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


def strip_preface(text):
    """Remove everything before the first conversation, including Editor's Preface
    and the Conversations introduction."""
    # Find "First Conversation:" which starts the actual content
    match = re.search(r'\nFirst Conversation:', text)
    if match:
        return text[match.start():].strip()
    return text


def parse_sections(text):
    """Parse the text into conversation and letter sections using ordinal headings."""
    # Build patterns for all conversations and letters
    section_patterns = []
    for i, ordinal in enumerate(ORDINALS[:4]):
        section_patterns.append((f'{ordinal} Conversation', 'conversation', i + 1))
    for i, ordinal in enumerate(ORDINALS[:15]):
        section_patterns.append((f'{ordinal} Letter', 'letter', i + 1))

    # Find all section start positions
    sections = []
    for label, sec_type, number in section_patterns:
        # Match "First Conversation:" or "First Letter:" at start of line or after newline
        pattern = re.compile(r'(?:^|\n)(' + re.escape(label) + r':)')
        match = pattern.search(text)
        if match:
            # The content starts at the heading
            sections.append({
                'label': label,
                'type': sec_type,
                'number': number,
                'start': match.start(),
            })

    # Sort by position in text
    sections.sort(key=lambda s: s['start'])

    # Find the "Letters" introduction marker so we can exclude it from conversation-4
    letters_intro_match = re.search(r'\nLetters\n', text)
    letters_intro_pos = letters_intro_match.start() if letters_intro_match else None

    # Extract text for each section
    for i, sec in enumerate(sections):
        if i + 1 < len(sections):
            end = sections[i + 1]['start']
        else:
            # Last section — go to end but stop before the closing line
            end = len(text)

        # If this is the last conversation and the Letters intro is between it and the next section,
        # truncate at the Letters intro
        if sec['type'] == 'conversation' and letters_intro_pos is not None:
            if sec['start'] < letters_intro_pos < end:
                end = letters_intro_pos

        raw = text[sec['start']:end].strip()
        # Remove the heading prefix (e.g., "First Conversation: ")
        colon_idx = raw.index(':')
        sec['text'] = raw[colon_idx + 1:].strip()

    return sections


def truncate_first_sentence(text, max_len=60):
    """Get a truncated version of the first sentence for letter names."""
    # Take first sentence (up to first period, question mark, or exclamation)
    match = re.match(r'([^.!?]+[.!?])', text)
    if match:
        sentence = match.group(1).strip()
    else:
        sentence = text[:max_len].strip()

    if len(sentence) > max_len:
        # Truncate at word boundary
        truncated = sentence[:max_len].rsplit(' ', 1)[0]
        return truncated + '...'
    return sentence


def build_items(sections):
    """Build L1 items from parsed sections."""
    items = []
    sort_order = 0

    for sec in sections:
        if sec['type'] == 'conversation':
            item_id = f"conversation-{sec['number']}"
            name = f"{ORDINALS[sec['number'] - 1]} Conversation"
            category = 'conversation'
        else:
            item_id = f"letter-{sec['number']:02d}"
            first_sentence = truncate_first_sentence(sec['text'])
            name = f"{ORDINALS[sec['number'] - 1]} Letter: {first_sentence}"
            category = 'letter'

        item = {
            'id': item_id,
            'name': name,
            'sort_order': sort_order,
            'category': category,
            'level': 1,
            'sections': {
                'Text': sec['text']
            },
            'keywords': [],
            'metadata': {}
        }
        items.append(item)
        sort_order += 1

    return items, sort_order


def build_l2_items(sort_start):
    """Build L2 thematic grouping items."""
    items = []
    sort_order = sort_start

    # The Conversations
    items.append({
        'id': 'the-conversations',
        'name': 'The Conversations',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': ['conversation-1', 'conversation-2', 'conversation-3', 'conversation-4'],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'Four recorded conversations between Joseph de Beaufort and Brother Lawrence, conducted when Brother Lawrence was in his late fifties. De Beaufort, representative and counsel to the local archbishop, interviewed the crippled friar who had become renowned for his extraordinary peace and joy. These conversations capture Brother Lawrence\'s method in his own words — how he found God not through elaborate devotions but through simple, continuous attention to the divine presence in every moment.',
            'For Readers': 'Read these as a portrait of a man who has found something real. Notice how practical his advice is — no mystical jargon, no complex theology. He speaks of kitchen work, buying wine, picking up straws from the ground. The conversations progress from his initial conversion story to increasingly specific guidance on maintaining awareness of God.'
        },
        'keywords': ['interview', 'biography', 'method', 'practice'],
        'metadata': {}
    })
    sort_order += 1

    # The Letters
    items.append({
        'id': 'the-letters',
        'name': 'The Letters',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': [f'letter-{i:02d}' for i in range(1, 16)],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'Fifteen letters written during the last ten years of Brother Lawrence\'s life, mostly to long-time friends including a Carmelite sister and a sister at a nearby convent. These letters are the heart and soul of the work — direct spiritual counsel from a man who had practiced God\'s presence for over forty years. They range from detailed descriptions of his method to tender encouragement of those suffering illness and spiritual dryness.',
            'For Readers': 'These letters are intimate and personal. Brother Lawrence writes to real people with real struggles — chronic pain, wandering thoughts, spiritual doubt. His advice is always the same simple prescription: think of God often, in everything you do, and trust Him completely. The repetition itself is part of the teaching.'
        },
        'keywords': ['letters', 'correspondence', 'spiritual direction', 'counsel'],
        'metadata': {}
    })
    sort_order += 1

    # Finding God in Kitchen Work
    items.append({
        'id': 'finding-god-in-kitchen-work',
        'name': 'Finding God in Kitchen Work',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': [
            'conversation-1', 'conversation-2', 'conversation-4',
            'letter-01', 'letter-05', 'letter-06', 'letter-07'
        ],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'Brother Lawrence\'s most radical teaching: that washing dishes, cooking for a hundred monks, repairing sandals, and buying wine are not obstacles to prayer but the very substance of it. "The time of business does not with me differ from the time of prayer. In the noise and clutter of my kitchen, while several persons are at the same time calling for different things, I possess God in as great tranquillity as if I were upon my knees at the Blessed Supper." This theme runs through the conversations where he describes his kitchen work and the letters where he counsels others to find God in their daily tasks.',
            'For Readers': 'This is the thread that makes Brother Lawrence timeless. He was not a theologian or a mystic in a cave — he was a cook with a bad leg. His insight was that every mundane task is a chance to practice awareness. Modern mindfulness traditions echo this same discovery: presence is available in every moment, especially the ordinary ones.'
        },
        'keywords': ['ordinary work', 'kitchen', 'mundane', 'mindfulness', 'daily life', 'sacred ordinary'],
        'metadata': {}
    })
    sort_order += 1

    # The Dark Night and Perseverance
    items.append({
        'id': 'dark-night-and-perseverance',
        'name': 'The Dark Night and Perseverance',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': [
            'conversation-2', 'conversation-3',
            'letter-01', 'letter-02', 'letter-06',
            'letter-11', 'letter-12', 'letter-13', 'letter-14'
        ],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'Brother Lawrence\'s first ten years of monastic life were marked by severe spiritual suffering — he believed he was damned, felt that God, reason, and all creatures were against him, and only faith sustained him. This "dark night" is the honest counterweight to his later joy. The letters to suffering friends show how his own experience of struggle made him a compassionate counselor. He never minimizes pain but reframes it: suffering with God becomes sweet, and perseverance through difficulty is the path to the habitual peace he eventually found.',
            'For Readers': 'Brother Lawrence is not selling easy comfort. He struggled for a decade before his breakthrough. This honesty is what makes his testimony credible. If you are in a difficult season — spiritual dryness, chronic pain, doubt — these passages speak directly to that experience. His counsel: do not be discouraged, continue the practice imperfectly, and trust that the habit will form.'
        },
        'keywords': ['dark night', 'suffering', 'perseverance', 'struggle', 'doubt', 'breakthrough'],
        'metadata': {}
    })
    sort_order += 1

    # Continuous Prayer
    items.append({
        'id': 'continuous-prayer',
        'name': 'Continuous Prayer',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': [
            'conversation-1', 'conversation-2', 'conversation-3', 'conversation-4',
            'letter-01', 'letter-02', 'letter-04', 'letter-05',
            'letter-06', 'letter-08', 'letter-09', 'letter-10', 'letter-15'
        ],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The central practice that gives the book its name: maintaining a continuous, loving awareness of God\'s presence moment-to-moment. Brother Lawrence describes this not as intense concentration but as a gentle, habitual turning of attention — "a little lifting up of the heart," "a simple attention, an affectionate regard for God." He compares it to an infant at the mother\'s breast, to a stone before a carver. The practice requires no special setting, no elaborate method — only a heart resolved to think of God often and in all things.',
            'For Readers': 'This is Brother Lawrence\'s core method, and it is strikingly similar to contemplative practices across traditions: mindfulness in Buddhism, dhikr in Sufism, the Jesus Prayer in Eastern Orthodoxy. The key insight is that awareness of the divine is not reserved for set prayer times but can become the background music of every waking moment. Start small: one moment of attention, then another, then another.'
        },
        'keywords': ['presence', 'awareness', 'prayer', 'attention', 'habit', 'contemplation', 'mindfulness'],
        'metadata': {}
    })
    sort_order += 1

    return items, sort_order


def build_l3_item(sort_order):
    """Build L3 meta-category."""
    return {
        'id': 'the-practice',
        'name': 'The Practice',
        'sort_order': sort_order,
        'category': 'meta-theme',
        'level': 3,
        'composite_of': [
            'the-conversations', 'the-letters',
            'finding-god-in-kitchen-work', 'dark-night-and-perseverance',
            'continuous-prayer'
        ],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The Practice of the Presence of God is one of the most influential short works in Christian contemplative history. Written not by a theologian but by a kitchen worker, it teaches that the highest spiritual life is available to anyone willing to practice simple, continuous attention to God. Brother Lawrence\'s method prefigures modern mindfulness: the radical claim that awareness itself — sustained, gentle, returning again and again — transforms ordinary life into sacred ground. The conversations give us the man; the letters give us his counsel to others; and the thematic threads reveal a teaching that is at once deeply Christian and universally human.',
            'Legacy': 'Brother Lawrence\'s little book has influenced contemplatives across traditions for over three centuries. It shaped the Quietist movement, informed the development of centering prayer, and continues to be one of the most recommended texts for anyone beginning a contemplative practice. His influence extends to Marsha Linehan\'s emphasis on radical acceptance and mindfulness in dialectical behavioral therapy — the secular echo of a friar who found peace by paying attention.'
        },
        'keywords': ['practice', 'presence', 'contemplation', 'mysticism', 'simplicity', 'transformation'],
        'metadata': {}
    }


def build_grammar():
    """Build the complete grammar."""
    raw = read_seed()
    text = strip_gutenberg(raw)
    text = strip_preface(text)

    sections = parse_sections(text)

    # Count what we found
    conversations = [s for s in sections if s['type'] == 'conversation']
    letters = [s for s in sections if s['type'] == 'letter']
    print(f"Found {len(conversations)} conversations and {len(letters)} letters")

    if len(conversations) != 4:
        print(f"WARNING: Expected 4 conversations, found {len(conversations)}")
    if len(letters) != 15:
        print(f"WARNING: Expected 15 letters, found {len(letters)}")

    # Build items
    l1_items, next_sort = build_items(sections)
    l2_items, next_sort = build_l2_items(next_sort)
    l3_item = build_l3_item(next_sort)

    all_items = l1_items + l2_items + [l3_item]

    # Validate composite_of references
    all_ids = {item['id'] for item in all_items}
    for item in all_items:
        if 'composite_of' in item:
            for ref in item['composite_of']:
                if ref not in all_ids:
                    print(f"WARNING: {item['id']} references non-existent id: {ref}")

    grammar = {
        '_grammar_commons': {
            'schema_version': '1.0',
            'license': 'CC-BY-SA-4.0',
            'attribution': [
                {'name': 'Brother Lawrence', 'date': '~1691', 'note': 'Author'},
                {'name': 'Joseph de Beaufort', 'date': '1692', 'note': 'Original compiler'}
            ]
        },
        'name': 'The Practice of the Presence of God',
        'description': (
            "Brother Lawrence's Practice of the Presence of God \u2014 4 conversations and "
            "15 letters from a 17th-century Carmelite friar who found God not in grand "
            "mystical visions but in washing dishes and repairing sandals. His method was "
            "radical simplicity: maintain a continuous, loving awareness of God's presence "
            "in every ordinary moment. This is the contemplative root of mindfulness practice "
            "in the Christian tradition.\n\n"
            "Source: Project Gutenberg eBook #5657 (https://www.gutenberg.org/ebooks/5657)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: 17th century French monastery paintings. "
            "Georges de La Tour's candlelit scenes. Zurbar\u00e1n's monks in contemplation."
        ),
        'grammar_type': 'custom',
        'creator_name': 'PlayfulProcess',
        'tags': ['mysticism', 'christian', 'contemplative', 'practice', 'public-domain', 'full-text', 'wisdom', 'mindfulness'],
        'roots': ['mysticism'],
        'shelves': ['wisdom'],
        'lineages': ['Linehan'],
        'worldview': 'devotional',
        'items': all_items
    }

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Summary
    l1_count = len([i for i in all_items if i['level'] == 1])
    l2_count = len([i for i in all_items if i['level'] == 2])
    l3_count = len([i for i in all_items if i['level'] == 3])
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1 items: {l1_count} ({len(conversations)} conversations + {len(letters)} letters)")
    print(f"  L2 items: {l2_count}")
    print(f"  L3 items: {l3_count}")
    print(f"  Total: {len(all_items)} items")


if __name__ == '__main__':
    build_grammar()
