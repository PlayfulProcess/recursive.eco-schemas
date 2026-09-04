#!/usr/bin/env python3
"""
Build grammar for The Cell of Self-Knowledge: Seven Early English Mystical Treatises.
Source: Project Gutenberg eBook #4544

Despite the seed filename 'meister-eckhart-sermons.txt', this text is actually
"The Cell of Self-Knowledge," a collection of seven 14th-century English mystical
treatises compiled by Henry Pepwell in 1521, edited by Edmund G. Gardner (1910).

The seven treatises are:
I. Benjamin (from Richard of St. Victor) - On contemplation
II. Doctrines from St. Catherine of Siena
III. From the Book of Margery Kempe
IV. Walter Hilton's Song of Angels
V. The Epistle of Prayer
VI. Epistle of Discretion in Stirrings of the Soul
VII. Discerning of Spirits

These are deeply connected to the Cloud of Unknowing tradition and Meister Eckhart's
influence on English mysticism.
"""

import json
import re
import os

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'meister-eckhart-sermons.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'meister-eckhart-sermons')
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


# Treatise definitions with their markers and metadata
TREATISES = [
    {
        'num': 1,
        'id': 'benjamin',
        'start_marker': 'HERE FOLLOWETH A VERY DEVOUT TREATISE, NAMED BENJAMIN',
        'end_marker': 'DEO GRATIAS',
        'name': 'Benjamin: On Contemplation',
        'full_name': 'A Very Devout Treatise Named Benjamin, of the Mights and Virtues of Man\'s Soul',
        'author': 'After Richard of St. Victor',
        'description': 'A paraphrase of Richard of St. Victor\'s Benjamin Minor, teaching how the soul rises through dread, sorrow, hope, and love toward the summit of contemplation. Benjamin represents contemplation itself -- the child whose birth costs the death of reason (Rachel), as the mind is rapt above itself into divine light.',
        'has_capitula': True,
    },
    {
        'num': 2,
        'id': 'catherine-doctrines',
        'start_marker': 'HERE FOLLOWETH DIVERS DOCTRINES DEVOUT AND FRUITFUL',
        'end_marker': 'DEO GRATI',  # DEO GRATIS
        'name': 'Doctrines of St. Catherine of Siena',
        'full_name': 'Divers Doctrines Devout and Fruitful, from the Life of St. Catherine of Siena',
        'author': 'From the life of St. Catherine of Siena',
        'description': 'Selected teachings from the life of Catherine of Siena (1347-1380), one of the most extraordinary women of the medieval era. The doctrines alternate between words spoken by Christ to Catherine and Catherine\'s own teachings to others, centering on self-knowledge, divine love, and the holy hate of sensuality that leads to virtue.',
        'has_capitula': False,
    },
    {
        'num': 3,
        'id': 'margery-kempe',
        'start_marker': 'HERE BEGINNETH A SHORT TREATISE OF CONTEMPLATION',
        'end_marker': 'Here endeth a short treatise of a devout ancress called Margery',
        'name': 'Revelations of Margery Kempe',
        'full_name': 'A Short Treatise of Contemplation Taught by Our Lord Jesu Christ, from the Book of Margery Kempe',
        'author': 'Margery Kempe of Lynn',
        'description': 'A precious fragment from the lost "Book of Margery Kempe" -- intimate dialogues between Christ and Margery, an anchoress of Lynn. The core teaching: contemplative love pleases God more than any outward penance or devotion. "Daughter, if thou knew how sweet thy love is to Me, thou wouldest never do other thing but love Me with all thine heart."',
        'has_capitula': False,
    },
    {
        'num': 4,
        'id': 'song-of-angels',
        'start_marker': 'HERE FOLLOWETH A DEVOUT TREATISE COMPILED BY MASTER WALTER HYLTON',
        'end_marker': 'EXPLICIT',
        'name': 'The Song of Angels',
        'full_name': 'A Devout Treatise Compiled by Master Walter Hilton of the Song of Angels',
        'author': 'Walter Hilton',
        'description': 'Walter Hilton\'s mystical treatise on the "onehead" (union) of the soul with God in perfect charity. He distinguishes true mystical consolations from delusions, and teaches that the soul must be reformed in mind, reason, and affection before it can hear the angel\'s song -- the ineffable experience of divine presence.',
        'has_capitula': False,
    },
    {
        'num': 5,
        'id': 'epistle-of-prayer',
        'start_marker': 'HERE AFTER FOLLOWETH A DEVOUT TREATISE CALLED THE EPISTLE OF PRAYER',
        'end_marker': 'FINIT EPISTOLA',
        'name': 'The Epistle of Prayer',
        'full_name': 'A Devout Treatise Called the Epistle of Prayer',
        'author': 'Anonymous (Cloud of Unknowing author)',
        'description': 'A practical guide to prayer by the anonymous author of the Cloud of Unknowing. The writer counsels beginning every prayer with the awareness that you might die before finishing it -- not as morbid thought but as liberation, freeing the soul from recklessness and kindling urgent love. Dread and hope become the two pillars of devotion.',
        'has_capitula': False,
    },
    {
        'num': 6,
        'id': 'epistle-of-discretion',
        'start_marker': 'HERE FOLLOWETH ALSO A VERY NECESSARY EPISTLE OF DISCRETION',
        'end_marker': 'FINIT EPISTOLA',
        'name': 'Epistle of Discretion in Stirrings of the Soul',
        'full_name': 'A Very Necessary Epistle of Discretion in Stirrings of the Soul',
        'author': 'Anonymous (Cloud of Unknowing author)',
        'description': 'A letter of spiritual direction on discerning whether inner stirrings come from God, from nature, or from the enemy. The author -- probably the same who wrote the Cloud of Unknowing -- teaches that stirrings of the soul must be tested by charity, humility, and the counsel of the wise. With characteristic medieval warmth and occasional humor, he warns against spiritual stirrings "conceived on the ape\'s manner."',
        'has_capitula': False,
    },
    {
        'num': 7,
        'id': 'discerning-of-spirits',
        'start_marker': 'HERE FOLLOWETH A DEVOUT TREATISE OF DISCERNING OF SPIRITS',
        'end_marker': 'FINIS. DEO GRATIAS',
        'name': 'Discerning of Spirits',
        'full_name': 'A Devout Treatise of Discerning of Spirits, Very Necessary for Ghostly Livers',
        'author': 'Anonymous (Cloud of Unknowing author)',
        'description': 'A treatise on the four spirits that speak in the human heart: the spirit of the flesh, the spirit of the world, the spirit of malice (the fiend), and the Holy Spirit. The writer teaches how to recognize each by what it speaks -- the flesh speaks soft things, the world speaks vain things, the fiend speaks bitter things -- and how to resist the first three through prayer, counsel, and the peace of heart in which God dwells.',
        'has_capitula': False,
    },
]


def find_treatise_text(text, treatise):
    """Extract the text of a single treatise."""
    start_idx = text.find(treatise['start_marker'])
    if start_idx == -1:
        print(f"WARNING: Could not find start marker for {treatise['name']}")
        return ''

    # For end marker, search after start
    end_idx = text.find(treatise['end_marker'], start_idx + len(treatise['start_marker']))
    if end_idx == -1:
        print(f"WARNING: Could not find end marker for {treatise['name']}")
        end_idx = len(text)
    else:
        # Include the end marker line
        end_idx = text.index('\n', end_idx) if '\n' in text[end_idx:] else len(text)

    raw = text[start_idx:end_idx].strip()

    # Remove the header line(s)
    # Skip past the title heading to the actual content
    lines = raw.split('\n')
    content_start = 0
    # Skip title lines (all caps)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.isupper() and not stripped.startswith('HERE') and i > 0:
            content_start = i
            break

    content = '\n'.join(lines[content_start:]).strip()

    # Remove footnotes
    content = re.sub(r'\n\[(\d+)\][^\n]*', '', content)
    content = re.sub(r'\[(\d+)\]', '', content)
    content = re.sub(r'\n{3,}', '\n\n', content).strip()

    return content


def parse_benjamin_chapters(text):
    """Parse the Benjamin treatise into its capitula (chapters)."""
    chapters = []

    # Find THE PROLOGUE
    prologue_match = re.search(r'\bTHE PROLOGUE\b', text)
    cap_pattern = re.compile(r'\n\s*(CAPITULUM\s+([IVXLC]+))\s*\n')

    cap_matches = list(cap_pattern.finditer(text))

    # Prologue
    if prologue_match:
        if cap_matches:
            prologue_text = text[prologue_match.end():cap_matches[0].start()].strip()
        else:
            prologue_text = text[prologue_match.end():].strip()

        # Clean: skip subtitle line(s)
        lines = prologue_text.split('\n')
        clean_lines = []
        started = False
        for line in lines:
            stripped = line.strip()
            if not started:
                if stripped and not stripped.isupper() and not stripped.startswith('A TREATISE'):
                    started = True
                    clean_lines.append(line)
            else:
                clean_lines.append(line)

        chapters.append({
            'id': 'benjamin-prologue',
            'name': 'Benjamin: The Prologue',
            'text': '\n'.join(clean_lines).strip(),
            'category': 'benjamin',
        })

    # Capitula
    for i, match in enumerate(cap_matches):
        cap_num_roman = match.group(2)
        cap_num = roman_to_int(cap_num_roman)

        content_start = match.end()
        if i + 1 < len(cap_matches):
            content_end = cap_matches[i + 1].start()
        else:
            # End at DEO GRATIAS or end of text
            deo_idx = text.find('DEO GRATIAS', content_start)
            content_end = deo_idx if deo_idx != -1 else len(text)

        raw_content = text[content_start:content_end].strip()

        # Extract subtitle (usually ALL CAPS line after CAPITULUM)
        lines = raw_content.split('\n')
        subtitle = ''
        content_lines = []
        found_content = False
        for line in lines:
            stripped = line.strip()
            if not found_content:
                if stripped.isupper() and len(stripped) > 5:
                    subtitle = stripped.title()
                elif stripped and not stripped.isupper():
                    found_content = True
                    content_lines.append(line)
            else:
                content_lines.append(line)

        cap_name = f"Benjamin, Chapter {cap_num}"
        if subtitle:
            cap_name += f": {subtitle}"

        chapters.append({
            'id': f'benjamin-cap-{cap_num}',
            'name': cap_name,
            'text': '\n'.join(content_lines).strip(),
            'category': 'benjamin',
        })

    return chapters


def roman_to_int(s):
    """Convert Roman numeral to integer."""
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    s = s.upper().strip()
    for i, c in enumerate(s):
        if c not in roman_values:
            return 0
        val = roman_values[c]
        if i + 1 < len(s) and roman_values.get(s[i + 1], 0) > val:
            result -= val
        else:
            result += val
    return result


def build_items(text):
    """Build all L1 items from the seven treatises."""
    items = []
    sort_order = 0

    for treatise in TREATISES:
        treatise_text = find_treatise_text(text, treatise)
        if not treatise_text:
            print(f"WARNING: Empty text for {treatise['name']}")
            continue

        if treatise['has_capitula'] and treatise['id'] == 'benjamin':
            # Parse Benjamin into individual chapters
            chapters = parse_benjamin_chapters(treatise_text)
            for ch in chapters:
                # Remove footnotes from chapter text
                cleaned_text = re.sub(r'\n\[(\d+)\][^\n]*', '', ch['text'])
                cleaned_text = re.sub(r'\[(\d+)\]', '', cleaned_text)
                cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text).strip()

                items.append({
                    'id': ch['id'],
                    'name': ch['name'],
                    'sort_order': sort_order,
                    'category': ch['category'],
                    'level': 1,
                    'sections': {
                        'Text': cleaned_text
                    },
                    'keywords': extract_keywords(cleaned_text),
                    'metadata': {'treatise': 'benjamin', 'author': 'After Richard of St. Victor'}
                })
                sort_order += 1
        else:
            # Single item for the whole treatise
            # Remove footnotes
            cleaned_text = re.sub(r'\n\[(\d+)\][^\n]*', '', treatise_text)
            cleaned_text = re.sub(r'\[(\d+)\]', '', cleaned_text)
            cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text).strip()
            # Also remove end markers from the text
            for marker in ['DEO GRATIS', 'DEO GRATIAS', 'EXPLICIT', 'FINIT EPISTOLA', 'FINIS. DEO GRATIAS']:
                cleaned_text = cleaned_text.replace(marker, '').strip()

            items.append({
                'id': treatise['id'],
                'name': treatise['name'],
                'sort_order': sort_order,
                'category': 'treatise',
                'level': 1,
                'sections': {
                    'Text': cleaned_text,
                    'About': treatise['description'],
                },
                'keywords': extract_keywords(cleaned_text),
                'metadata': {'treatise': treatise['id'], 'author': treatise['author']}
            })
            sort_order += 1

    return items, sort_order


def extract_keywords(text):
    """Extract keywords from text based on common mystical terms."""
    keywords = []
    text_lower = text.lower()
    keyword_checks = [
        ('contemplation', 'contemplation'), ('prayer', 'prayer'), ('love', 'love'),
        ('dread', 'dread'), ('sorrow', 'sorrow'), ('hope', 'hope'),
        ('soul', 'soul'), ('charity', 'charity'), ('grace', 'grace'),
        ('angel', 'angels'), ('spirit', 'spirit'), ('flesh', 'flesh'),
        ('devotion', 'devotion'), ('silence', 'silence'), ('suffering', 'suffering'),
        ('virtue', 'virtue'), ('sin', 'sin'), ('humility', 'humility'),
    ]
    for term, kw in keyword_checks:
        if term in text_lower:
            keywords.append(kw)
    return keywords[:6]


def build_l2_items(l1_items, sort_start):
    """Build L2 thematic grouping items."""
    items = []
    sort_order = sort_start

    # The Benjamin treatise as a group
    benjamin_ids = [i['id'] for i in l1_items if i.get('metadata', {}).get('treatise') == 'benjamin']
    items.append({
        'id': 'treatise-benjamin',
        'name': 'Treatise I: Benjamin — The Way to Contemplation',
        'sort_order': sort_order,
        'category': 'treatise-group',
        'level': 2,
        'composite_of': benjamin_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': "A paraphrase of Richard of St. Victor's Benjamin Minor, this is the longest and most systematic treatise in the collection. Using the allegory of Jacob's wives and children, it maps the soul's ascent through affection and reason toward contemplation. The twelve children of Jacob represent twelve spiritual virtues: dread, sorrow, hope, love, joy, hatred of sin, shame, abstinence, patience, discretion, and finally Benjamin -- contemplation itself, born at the cost of Rachel (reason). The treatise teaches that contemplation surpasses reason and cannot be reached by human effort alone.",
            'For Readers': "This is medieval psychology at its most luminous. The allegory may seem elaborate, but the insight is profound: the spiritual life begins with dread and sorrow, passes through hope and love, and culminates in an experience that transcends rational thought. This is the same trajectory that later contemplatives like John of the Cross and Teresa of Avila would describe."
        },
        'keywords': ['contemplation', 'virtue', 'allegory', 'reason', 'affection'],
        'metadata': {}
    })
    sort_order += 1

    # The Women Mystics group
    items.append({
        'id': 'women-mystics',
        'name': 'Voices of the Women Mystics',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': ['catherine-doctrines', 'margery-kempe'],
        'relationship_type': 'emergence',
        'sections': {
            'About': "Two remarkable women's voices: Catherine of Siena (1347-1380), the Italian mystic who counseled popes and kings, and Margery Kempe of Lynn, the English anchoress whose intimate dialogues with Christ are among the most tender in medieval literature. Catherine teaches the fierce discipline of self-knowledge and holy hatred of sin; Margery receives the gentle assurance that contemplative love outweighs all outward devotion. Together they represent the full range of feminine mystical experience.",
            'For Readers': "Notice the contrast: Catherine's voice is bold and prophetic, while Margery's is intimate and personal. Both women assert the authority of direct experience over institutional learning. Catherine: 'If thou know well these two words, thou art and shalt be blessed.' Margery: 'Daughter, if thou knew how sweet thy love is to Me, thou wouldest never do other thing but love Me.'"
        },
        'keywords': ['women', 'feminine', 'mysticism', 'contemplation', 'love'],
        'metadata': {}
    })
    sort_order += 1

    # The Cloud of Unknowing school
    cloud_ids = ['epistle-of-prayer', 'epistle-of-discretion', 'discerning-of-spirits']
    items.append({
        'id': 'cloud-school',
        'name': 'The Cloud of Unknowing School: Three Epistles',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': cloud_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': "Three treatises attributed to the anonymous author of the Cloud of Unknowing, the masterpiece of English mysticism. These epistles bring the Cloud's teaching down to practical guidance: how to pray (begin as if you will die before finishing), how to discern whether inner stirrings come from God or from the enemy, and how to distinguish the spirits of flesh, world, and malice from the Holy Spirit. Written with warmth, humor, and deep psychological insight.",
            'For Readers': "These are among the most practical texts in the mystical tradition. The author is not describing lofty experiences but giving concrete advice to spiritual beginners. The Epistle of Prayer is especially relevant for anyone who struggles with distraction in meditation: its counsel to begin with awareness of mortality is startlingly effective."
        },
        'keywords': ['prayer', 'discernment', 'practical', 'cloud-of-unknowing', 'guidance'],
        'metadata': {}
    })
    sort_order += 1

    # Walter Hilton
    items.append({
        'id': 'hilton-angels',
        'name': 'Walter Hilton: The Song of Angels',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': ['song-of-angels'],
        'relationship_type': 'emergence',
        'sections': {
            'About': "Walter Hilton's mystical treatise on the union of the soul with God, and how to distinguish true divine consolation from sensory delusion. Hilton teaches that the 'onehead' (union) with God requires the reformation of mind, reason, and affection -- a comprehensive transformation of the whole person. The 'song of angels' is not a literal sound but the soul's experience of being drawn into divine harmony.",
            'For Readers': "Hilton is the most careful and discerning of the English mystics. Where others soar, he tests. His teaching on distinguishing true from false spiritual experience is invaluable for anyone on a contemplative path."
        },
        'keywords': ['angels', 'union', 'discernment', 'hilton', 'reformation'],
        'metadata': {}
    })
    sort_order += 1

    # Love and Self-Knowledge theme
    all_ids = [i['id'] for i in l1_items]
    items.append({
        'id': 'love-and-self-knowledge',
        'name': 'Love and Self-Knowledge: The Heart of the Collection',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': ['benjamin-cap-1', 'benjamin-cap-4', 'catherine-doctrines', 'margery-kempe', 'epistle-of-prayer'],
        'relationship_type': 'emergence',
        'sections': {
            'About': "The unifying theme of the entire collection: the cell of self-knowledge, borrowed from St. Catherine of Siena. All seven treatises teach that the way to God begins with knowing oneself -- one's nothingness before God and one's capacity for divine love. Richard of St. Victor: 'Full knowledge of the rational spirit is a great and high mountain.' Catherine: 'Thou art she that art nought; and I am He that am ought.' The path from self-knowledge to divine love runs through every page.",
            'For Readers': "This is the golden thread. Whether the writer is a systematic theologian like Richard of St. Victor, a passionate mystic like Catherine, or a humble cook like Margery Kempe, the teaching is the same: know yourself truly, and you will find God. This is contemplative practice at its most essential."
        },
        'keywords': ['self-knowledge', 'love', 'contemplation', 'unity'],
        'metadata': {}
    })
    sort_order += 1

    return items, sort_order


def build_l3_items(sort_start):
    """Build L3 meta-category items."""
    items = []
    sort_order = sort_start

    items.append({
        'id': 'the-cell-of-self-knowledge',
        'name': 'The Cell of Self-Knowledge',
        'sort_order': sort_order,
        'category': 'meta-theme',
        'level': 3,
        'composite_of': [
            'treatise-benjamin', 'women-mystics', 'cloud-school',
            'hilton-angels', 'love-and-self-knowledge'
        ],
        'relationship_type': 'emergence',
        'sections': {
            'About': "The Cell of Self-Knowledge gathers seven luminous treatises from the golden age of English mysticism (late 14th century), first printed by Henry Pepwell in 1521. Together they represent every major stream of medieval contemplative practice: the systematic theology of Richard of St. Victor, the passionate devotion of the women mystics (Catherine of Siena, Margery Kempe), the careful psychology of Walter Hilton, and the practical wisdom of the anonymous Cloud of Unknowing author. The title comes from Catherine of Siena: 'Let us stay in the cell of self-knowledge, knowing ourselves through ourselves to be nothing, and the goodness of God in us.' These texts are the headwaters of the English contemplative tradition that would flow through the Metaphysical Poets, the Quakers, and into modern contemplative Christianity.",
            'Legacy': "This collection documents the moment when mystical theology moved from Latin into the vernacular -- when the deepest spiritual teachings became available to ordinary people in their own language. The authors represented here influenced Meister Eckhart, the Rhineland mystics, the Devotio Moderna, and ultimately the Reformation's emphasis on individual spiritual experience. Their teachings on self-knowledge, contemplative prayer, and discernment of spirits anticipate modern mindfulness practice and dialectical thinking. The Cloud of Unknowing school's emphasis on unknowing prefigures apophatic theology across traditions."
        },
        'keywords': ['mysticism', 'self-knowledge', 'contemplation', 'medieval', 'english', 'collection'],
        'metadata': {}
    })
    sort_order += 1

    return items, sort_order


def build_grammar():
    """Build the complete grammar."""
    raw = read_seed()
    text = strip_gutenberg(raw)

    # Strip the introduction (everything before the first treatise begins)
    first_treatise_start = text.find('HERE FOLLOWETH A VERY DEVOUT TREATISE, NAMED BENJAMIN')
    if first_treatise_start == -1:
        # Try alternate
        first_treatise_start = text.find('I.\n\nHERE FOLLOWETH')
    if first_treatise_start != -1:
        intro_text = text[:first_treatise_start]
        main_text = text[first_treatise_start:]
    else:
        main_text = text

    # Build items
    l1_items, next_sort = build_items(main_text)
    l2_items, next_sort = build_l2_items(l1_items, next_sort)
    l3_items, next_sort = build_l3_items(next_sort)

    all_items = l1_items + l2_items + l3_items

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
                {'name': 'Richard of St. Victor', 'date': 'd. 1173', 'note': 'Author of Benjamin Minor (Treatise I source)'},
                {'name': 'St. Catherine of Siena', 'date': '1347-1380', 'note': 'Source of Treatise II doctrines'},
                {'name': 'Margery Kempe', 'date': '14th century', 'note': 'Author/subject of Treatise III'},
                {'name': 'Walter Hilton', 'date': 'd. 1396', 'note': 'Author of Treatise IV'},
                {'name': 'Henry Pepwell', 'date': '1521', 'note': 'Original compiler/printer'},
                {'name': 'Edmund G. Gardner', 'date': '1910', 'note': 'Editor of this edition'},
            ]
        },
        'name': 'The Cell of Self-Knowledge',
        'description': (
            "Seven early English mystical treatises from the golden age of medieval contemplative writing "
            "(late 14th century), compiled by Henry Pepwell in 1521 and edited by Edmund G. Gardner in 1910. "
            "The collection includes works by or inspired by Richard of St. Victor, St. Catherine of Siena, "
            "Margery Kempe, Walter Hilton, and the anonymous author of the Cloud of Unknowing. Together they "
            "form a complete curriculum in medieval contemplative practice: from the systematic psychology of "
            "contemplation (Benjamin) through the passionate devotion of the women mystics, to the practical "
            "guidance on prayer and discernment from the Cloud school. The title comes from Catherine of Siena: "
            "'Let us stay in the cell of self-knowledge.'\n\n"
            "Source: Project Gutenberg eBook #4544 (https://www.gutenberg.org/ebooks/4544)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Medieval manuscript illuminations from English and Italian "
            "sources. Fra Angelico's contemplative scenes. Giovanni di Paolo's illustrations of Catherine of Siena. "
            "Medieval anchoress cells and scriptorium scenes."
        ),
        'grammar_type': 'custom',
        'creator_name': 'PlayfulProcess',
        'tags': ['mysticism', 'christian', 'contemplative', 'medieval', 'public-domain', 'full-text', 'wisdom', 'collection'],
        'roots': ['western-mysticism', 'contemplative-practice'],
        'shelves': ['wisdom'],
        'lineages': ['Linehan', 'Shrei'],
        'worldview': 'contemplative',
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
    print(f"  L1 items: {l1_count} (treatise sections)")
    print(f"  L2 items: {l2_count} (thematic groups)")
    print(f"  L3 items: {l3_count}")
    print(f"  Total: {len(all_items)} items")


if __name__ == '__main__':
    build_grammar()
