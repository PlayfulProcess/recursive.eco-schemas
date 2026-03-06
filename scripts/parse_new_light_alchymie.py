#!/usr/bin/env python3
"""
Parser for A New Light of Alchymie (Gutenberg #61112)
by Michal Sedziwój (Sendivogius) and Paracelsus, translated by John French (1650).

Structure:
  Part I:   A New Light of Alchymie (Sendivogius) — 12 Treatises + Epilogue + Preface to Riddle + Parable + Dialogue
  Part II:  A Treatise of Sulphur (Sendivogius) — Preface + 6 chapters (Earth, Water, Aire, Fire, Three Principles, Sulphur)
  Part III: Of the Nature of Things (Paracelsus) — 9 Books with sub-sections in Books 8 & 9
  Part IV:  A Chymicall Dictionary — 24 letter sections (A-Z)
"""

import json
import re
import os

SEED = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'new-light-alchymie.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'new-light-alchymie')
OUTPUT = os.path.join(OUTPUT_DIR, 'grammar.json')

TRUNCATE_CHARS = 2800


def read_seed():
    with open(SEED, 'r', encoding='utf-8') as f:
        return f.read()


def isolate_body(text):
    """Extract text between Gutenberg START and END markers."""
    start_marker = '*** START OF THE PROJECT GUTENBERG EBOOK A NEW LIGHT OF ALCHYMIE ***'
    end_marker = '*** END OF THE PROJECT GUTENBERG EBOOK A NEW LIGHT OF ALCHYMIE ***'
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1:
        raise ValueError("Could not find Gutenberg markers")
    return text[start + len(start_marker):end]


def truncate_text(text, max_chars=TRUNCATE_CHARS):
    """Truncate text at ~max_chars, ending at last period."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    bp = text.rfind(".", 0, max_chars)
    if bp == -1:
        bp = max_chars
    remaining_words = len(text[bp+1:].split())
    return text[:bp+1] + f" [Text continues for approximately {remaining_words} more words...]"


def clean_text(text):
    """Clean text: remove sidenotes, illustrations, normalize whitespace."""
    # Remove sidenotes
    text = re.sub(r'\[Sidenote:[^\]]*\]\n*', '', text)
    # Remove illustration markers
    text = re.sub(r'\[Illustration:[^\]]*\]\n*', '', text)
    # Remove page markers like [Pg 123]
    text = re.sub(r'\[Pg \d+\]', '', text)
    # Collapse multiple blank lines to double
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Join lines within paragraphs (lines that don't start a new paragraph)
    lines = text.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            result.append('')
        else:
            # If previous line is non-empty text, join
            if result and result[-1] != '' and not result[-1].endswith('\n\n'):
                result[-1] = result[-1] + ' ' + stripped
            else:
                result.append(stripped)
    text = '\n'.join(result)
    # Collapse spaces
    text = re.sub(r'  +', ' ', text)
    return text.strip()


def find_line_number(body, marker):
    """Find the character position of a marker in body."""
    pos = body.find(marker)
    if pos == -1:
        return -1
    return pos


def extract_sections(body):
    """Extract all sections with their boundaries."""
    sections = []

    # === Part I: A New Light of Alchymie ===

    # Epistle to the Reader
    reader_start = body.find('To the Reader.')
    preface_start = body.find('The Preface.\n')
    if reader_start != -1 and preface_start != -1:
        sections.append({
            'id': 'epistle-to-reader',
            'name': 'Epistle to the Reader',
            'category': 'new-light-of-alchymie',
            'text': body[reader_start:preface_start],
        })

    # Preface
    first_treatise_start = body.find('_THE FIRST TREATISE._')
    if preface_start != -1 and first_treatise_start != -1:
        sections.append({
            'id': 'preface-new-light',
            'name': 'The Preface',
            'category': 'new-light-of-alchymie',
            'text': body[preface_start:first_treatise_start],
        })

    # Twelve Treatises
    treatise_names = {
        'FIRST': 'Of Nature, What She Is, and What Her Searchers Ought to Be',
        'SECOND': 'Of the Operation of Nature in Sperme',
        'THIRD': 'Of the True First Matter of Metalls',
        'FOURTH': 'How Metalls Are Generated in the Bowells of the Earth',
        'FIFTH': 'Of the Generation of All Kinds of Stones',
        'SIXTH': 'Of the Second Matter, and Putrefaction of Things',
        'SEVENTH': 'Of the Vertue of the Second Matter',
        'EIGHTH': 'How by Art Nature Works in Seed',
        'NINTH': 'Of the Commixtion of Metalls, or the Drawing Forth Their Seed',
        'TENTH': 'Of the Supernaturall Generation of the Son of the Sun',
        'ELEVENTH': 'Of the Praxis, and Making of the Stone or Tincture by Art',
        'TWELFTH': 'Of the Stone, and Its Vertue',
    }
    treatise_ids = {
        'FIRST': 'treatise-01', 'SECOND': 'treatise-02', 'THIRD': 'treatise-03',
        'FOURTH': 'treatise-04', 'FIFTH': 'treatise-05', 'SIXTH': 'treatise-06',
        'SEVENTH': 'treatise-07', 'EIGHTH': 'treatise-08', 'NINTH': 'treatise-09',
        'TENTH': 'treatise-10', 'ELEVENTH': 'treatise-11', 'TWELFTH': 'treatise-12',
    }
    ordinals = ['FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH', 'SIXTH',
                'SEVENTH', 'EIGHTH', 'NINTH', 'TENTH', 'ELEVENTH', 'TWELFTH']

    for i, ordinal in enumerate(ordinals):
        marker = f'_THE {ordinal} TREATISE._'
        start = body.find(marker)
        if start == -1:
            continue
        # Find the end: next treatise or epilogue
        if i + 1 < len(ordinals):
            next_marker = f'_THE {ordinals[i+1]} TREATISE._'
            end = body.find(next_marker)
        else:
            end = body.find('_THE EPILOGUE, or CONCLUSION')
        if end == -1:
            end = start + 5000
        sections.append({
            'id': treatise_ids[ordinal],
            'name': f'The {ordinal.title()} Treatise: {treatise_names[ordinal]}',
            'category': 'new-light-of-alchymie',
            'text': body[start:end],
        })

    # Epilogue
    epilogue_start = body.find('_THE EPILOGUE, or CONCLUSION')
    preface_riddle_start = body.find('A Preface To the Philosophicall')
    if epilogue_start != -1 and preface_riddle_start != -1:
        sections.append({
            'id': 'epilogue',
            'name': 'The Epilogue, or Conclusion of These Twelve Treatises',
            'category': 'new-light-of-alchymie',
            'text': body[epilogue_start:preface_riddle_start],
        })

    # Preface to the Riddle
    parable_start = body.find('THE PARABLE, OR _PHILOSOPHICALL RIDLE_.')
    if preface_riddle_start != -1 and parable_start != -1:
        sections.append({
            'id': 'preface-to-riddle',
            'name': 'A Preface to the Philosophicall Riddle',
            'category': 'new-light-of-alchymie',
            'text': body[preface_riddle_start:parable_start],
        })

    # The Parable / Philosophicall Riddle
    dialogue_start = body.find('A DIALOGVE BETWEEN')
    if parable_start != -1 and dialogue_start != -1:
        sections.append({
            'id': 'parable-riddle',
            'name': 'The Parable, or Philosophicall Riddle',
            'category': 'new-light-of-alchymie',
            'text': body[parable_start:dialogue_start],
        })

    # Dialogue between Mercury, the Alchymist, and Nature
    sulphur_treatise_start = body.find('A TREATISE OF SVLPHVR:')
    if dialogue_start != -1 and sulphur_treatise_start != -1:
        sections.append({
            'id': 'dialogue-mercury',
            'name': 'A Dialogue Between Mercury, the Alchymist, and Nature',
            'category': 'new-light-of-alchymie',
            'text': body[dialogue_start:sulphur_treatise_start],
        })

    # === Part II: A Treatise of Sulphur ===

    # Sulphur Preface
    sulphur_principle_start = body.find('  OF\n  SVLPHVR:\n  _The second Principle._')
    if sulphur_treatise_start != -1 and sulphur_principle_start != -1:
        sections.append({
            'id': 'sulphur-preface',
            'name': 'A Treatise of Sulphur: The Preface',
            'category': 'treatise-of-sulphur',
            'text': body[sulphur_treatise_start:sulphur_principle_start],
        })

    # Of Sulphur, the Second Principle
    earth_start = body.find('  OF\n  The ELEMENT of the\n  EARTH.')
    if sulphur_principle_start != -1 and earth_start != -1:
        sections.append({
            'id': 'sulphur-second-principle',
            'name': 'Of Sulphur, the Second Principle',
            'category': 'treatise-of-sulphur',
            'text': body[sulphur_principle_start:earth_start],
        })

    # Of the Element of Earth
    water_start = body.find('  OF\n  The ELEMENT of\n  WATER.')
    if earth_start != -1 and water_start != -1:
        sections.append({
            'id': 'sulphur-element-earth',
            'name': 'Of the Element of Earth',
            'category': 'treatise-of-sulphur',
            'text': body[earth_start:water_start],
        })

    # Of the Element of Water
    aire_start = body.find('  OF\n  The ELEMENT of\n  AIRE.')
    if water_start != -1 and aire_start != -1:
        sections.append({
            'id': 'sulphur-element-water',
            'name': 'Of the Element of Water',
            'category': 'treatise-of-sulphur',
            'text': body[water_start:aire_start],
        })

    # Of the Element of Aire
    fire_start = body.find('  OF\n  The ELEMENT of\n  FIRE.')
    if aire_start != -1 and fire_start != -1:
        sections.append({
            'id': 'sulphur-element-aire',
            'name': 'Of the Element of Aire',
            'category': 'treatise-of-sulphur',
            'text': body[aire_start:fire_start],
        })

    # Of the Element of Fire
    principles_start = body.find('  OF THE\n  THREE PRINCIPLES\n  Of all things.')
    if fire_start != -1 and principles_start != -1:
        sections.append({
            'id': 'sulphur-element-fire',
            'name': 'Of the Element of Fire',
            'category': 'treatise-of-sulphur',
            'text': body[fire_start:principles_start],
        })

    # Of the Three Principles of All Things
    of_sulphur_start = body.find('OF SVLPHVR:\n\n\n')
    # This is the second occurrence (not the treatise title)
    if principles_start != -1 and of_sulphur_start != -1 and of_sulphur_start > principles_start:
        sections.append({
            'id': 'sulphur-three-principles',
            'name': 'Of the Three Principles of All Things',
            'category': 'treatise-of-sulphur',
            'text': body[principles_start:of_sulphur_start],
        })

    # Of Sulphur (the chapter within the treatise)
    nature_things_start = body.find('  OF THE\n  NATVRE\n  Of Things.')
    if of_sulphur_start != -1 and nature_things_start != -1:
        # Find FINIS before Nature of Things
        finis_pos = body.rfind('FINIS.', of_sulphur_start, nature_things_start)
        if finis_pos != -1:
            sulphur_end = finis_pos + len('FINIS.')
        else:
            sulphur_end = nature_things_start
        sections.append({
            'id': 'sulphur-of-sulphur',
            'name': 'Of Sulphur',
            'category': 'treatise-of-sulphur',
            'text': body[of_sulphur_start:sulphur_end],
        })

    # === Part III: Of the Nature of Things (Paracelsus) ===

    book_names = {
        1: 'Of the Generations of Naturall Things',
        2: 'Of the Growth and Increase of Naturall Things',
        3: 'Of the Preservations of Naturall Things',
        4: 'Of the Life of Naturall Things',
        5: 'Of the Death, or Ruine of All Things',
        6: 'Of the Resurrection of Naturall Things',
        7: 'Of the Transmutation of Naturall Things',
        8: 'Of the Separation of Naturall Things',
        9: 'Of the Signature of Naturall Things',
    }

    book_markers = [
        (1, '_THE FIRST BOOKE._'),
        (2, '_THE SECOND BOOK._'),
        (3, '_THE THIRD BOOK._'),
        (4, '_THE FOURTH BOOK._'),
        (5, '_THE FIFTH BOOK._'),
        (6, '_THE SIXTH BOOK._'),
        (7, '_THE SEVENTH BOOK._'),
        (8, '_THE EIGHTH BOOK._'),
        (9, '_THE NINTH BOOK._'),
    ]

    dict_start = body.find('  A CHYMICALL\n  DICTIONARY:')

    for i, (num, marker) in enumerate(book_markers):
        start = body.find(marker)
        if start == -1:
            continue
        if i + 1 < len(book_markers):
            end = body.find(book_markers[i+1][1])
        else:
            # Book 9 ends at FINIS before Dictionary
            finis_before_dict = body.rfind('_FINIS._', start, dict_start)
            if finis_before_dict != -1:
                end = finis_before_dict + len('_FINIS._')
            else:
                end = dict_start
        if end == -1:
            end = start + 10000

        ordinal_words = ['First', 'Second', 'Third', 'Fourth', 'Fifth',
                         'Sixth', 'Seventh', 'Eighth', 'Ninth']
        sections.append({
            'id': f'nature-book-{num:02d}',
            'name': f'The {ordinal_words[num-1]} Book: {book_names[num]}',
            'category': 'nature-of-things',
            'text': body[start:end],
        })

    # Sub-sections of Book 8 (Separation)
    book8_subs = [
        ('nature-book-08-separation', 'Of the Separation of Naturall Things',
         '_Of the Separation of Naturall things._'),
        ('nature-book-08-metalls', 'Of the Separation of Metalls from Their Mines',
         '_Of the Separation of Metalls from their Mines._'),
        ('nature-book-08-mineralls', 'Of the Separation of Mineralls',
         '_Of the Separation of Mineralls._'),
        ('nature-book-08-vegetables', 'Of the Separation of Vegetables',
         '_Of the Separation of Vegetables._'),
        ('nature-book-08-animalls', 'Of the Separation of Animalls',
         '_Of the Separation of Animalls._'),
    ]

    for i, (sid, sname, smarker) in enumerate(book8_subs):
        start = body.find(smarker)
        if start == -1:
            continue
        if i + 1 < len(book8_subs):
            end = body.find(book8_subs[i+1][2])
        else:
            book9_marker = '_THE NINTH BOOK._'
            end = body.find(book9_marker)
        if end == -1:
            end = start + 5000
        sections.append({
            'id': sid,
            'name': sname,
            'category': 'nature-of-things-subsections',
            'text': body[start:end],
        })

    # Sub-sections of Book 9 (Signatures)
    book9_subs = [
        ('nature-book-09-monstrous', 'Of the Monstrous Signes of Men',
         '_Of the Monstrous Signes of Men._'),
        ('nature-book-09-physiognomy', 'Of the Astrall Signes of Physiognomy in Man',
         '_Of the Astrall Signes of Physiognomy in Man._'),
        ('nature-book-09-chiromancy', 'Of the Astrall Signes of Chiromancy',
         '_Of the Astrall Signes of Chiromancy._'),
        ('nature-book-09-minerall', 'Of Minerall Signes',
         '_Of Minerall Signes._'),
        ('nature-book-09-peculiar', 'Of Some Peculiar Signes of Naturall and Supernaturall Things',
         '_Of some peculiar Signes of Naturall and Supernaturall things._'),
    ]

    for i, (sid, sname, smarker) in enumerate(book9_subs):
        start = body.find(smarker)
        if start == -1:
            continue
        if i + 1 < len(book9_subs):
            end = body.find(book9_subs[i+1][2])
        else:
            finis_pos = body.find('_FINIS._', start)
            if finis_pos != -1:
                end = finis_pos + len('_FINIS._')
            else:
                end = dict_start
        if end == -1:
            end = start + 5000
        sections.append({
            'id': sid,
            'name': sname,
            'category': 'nature-of-things-subsections',
            'text': body[start:end],
        })

    # === Part IV: A Chymicall Dictionary ===
    # We'll treat the whole dictionary as one L1 item (it's a reference, not narrative)
    transcriber_start = body.find('TRANSCRIBER\'S NOTE.')
    # Find the second occurrence (end of book)
    if transcriber_start != -1:
        # Find from after the first one
        second_trans = body.find('TRANSCRIBER\'S NOTE.', transcriber_start + 100)
        if second_trans != -1:
            dict_end = second_trans
        else:
            dict_end = len(body)
    else:
        dict_end = len(body)

    if dict_start != -1:
        sections.append({
            'id': 'chymicall-dictionary',
            'name': 'A Chymicall Dictionary',
            'category': 'chymicall-dictionary',
            'text': body[dict_start:dict_end],
        })

    return sections


def build_l1_items(sections):
    """Build L1 items from extracted sections."""
    items = []
    sort_order = 0

    for sec in sections:
        # Skip sub-sections (they'll be referenced in L2, but exist as separate L1s)
        sort_order += 1
        text = clean_text(sec['text'])
        truncated = truncate_text(text)

        item = {
            'id': sec['id'],
            'name': sec['name'],
            'sort_order': sort_order,
            'category': sec['category'],
            'level': 1,
            'sections': {
                'Text': truncated
            },
            'keywords': extract_keywords(sec['id'], sec['name'], sec['category']),
            'metadata': {}
        }
        items.append(item)

    return items


def extract_keywords(item_id, name, category):
    """Generate keywords based on section identity."""
    keywords = []

    if category == 'new-light-of-alchymie':
        keywords.extend(['alchemy', 'sendivogius', 'transmutation'])
        if 'nature' in name.lower():
            keywords.append('nature')
        if 'metall' in name.lower():
            keywords.extend(['metals', 'metallurgy'])
        if 'stone' in name.lower():
            keywords.extend(['philosophers-stone', 'tincture'])
        if 'seed' in name.lower() or 'sperm' in name.lower():
            keywords.extend(['seed', 'generation'])
        if 'dialogue' in name.lower() or 'mercury' in name.lower():
            keywords.extend(['mercury', 'dialogue'])
        if 'parable' in name.lower() or 'riddle' in name.lower():
            keywords.extend(['parable', 'allegory', 'riddle'])
        if 'epilogue' in name.lower():
            keywords.append('conclusion')
        if 'preface' in name.lower():
            keywords.append('introduction')
        if 'putrefaction' in name.lower():
            keywords.append('putrefaction')

    elif category == 'treatise-of-sulphur':
        keywords.extend(['sulphur', 'sendivogius', 'principles'])
        if 'earth' in name.lower():
            keywords.extend(['earth', 'element'])
        if 'water' in name.lower():
            keywords.extend(['water', 'element'])
        if 'aire' in name.lower():
            keywords.extend(['air', 'element'])
        if 'fire' in name.lower():
            keywords.extend(['fire', 'element'])
        if 'three principles' in name.lower():
            keywords.extend(['mercury', 'salt', 'three-principles'])
        if 'preface' in name.lower():
            keywords.append('introduction')

    elif category in ('nature-of-things', 'nature-of-things-subsections'):
        keywords.extend(['paracelsus', 'natural-philosophy'])
        if 'generation' in name.lower():
            keywords.extend(['generation', 'creation'])
        if 'growth' in name.lower():
            keywords.extend(['growth', 'increase'])
        if 'preservation' in name.lower():
            keywords.append('preservation')
        if 'life' in name.lower():
            keywords.append('life')
        if 'death' in name.lower() or 'ruine' in name.lower():
            keywords.extend(['death', 'decay'])
        if 'resurrection' in name.lower():
            keywords.extend(['resurrection', 'renewal'])
        if 'transmutation' in name.lower():
            keywords.extend(['transmutation', 'transformation'])
        if 'separation' in name.lower():
            keywords.extend(['separation', 'distillation'])
        if 'signature' in name.lower():
            keywords.extend(['signatures', 'signs'])
        if 'physiognomy' in name.lower():
            keywords.extend(['physiognomy', 'astrology'])
        if 'chiromancy' in name.lower():
            keywords.extend(['chiromancy', 'palmistry'])
        if 'minerall' in name.lower():
            keywords.append('minerals')
        if 'metall' in name.lower():
            keywords.append('metals')
        if 'vegetable' in name.lower():
            keywords.append('vegetables')
        if 'animall' in name.lower():
            keywords.append('animals')
        if 'monstrous' in name.lower():
            keywords.append('monsters')

    elif category == 'chymicall-dictionary':
        keywords.extend(['dictionary', 'glossary', 'paracelsus', 'terminology'])

    return list(set(keywords))


def build_l2_items(l1_items, start_sort):
    """Build L2 thematic groupings."""
    l2_items = []
    sort_order = start_sort

    # L2: New Light of Alchymie — The Twelve Treatises
    treatise_ids = [f'treatise-{i:02d}' for i in range(1, 13)]
    sort_order += 1
    l2_items.append({
        'id': 'l2-twelve-treatises',
        'name': 'The Twelve Treatises of Alchymie',
        'sort_order': sort_order,
        'category': 'new-light-of-alchymie',
        'level': 2,
        'composite_of': treatise_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The twelve core treatises of Sendivogius\'s A New Light of Alchymie, progressing from the nature of things through the generation of metals, the role of seed and sperm, the second matter, putrefaction, and culminating in the practical creation of the Philosophers\' Stone. Together they form a complete alchemical cosmology and methodology, moving from metaphysics to praxis.',
            'Themes': 'Nature as teacher and guide; the unity of all matter; seed and generation as universal principles; the hierarchy of metals; putrefaction as gateway to transformation; the Stone as culmination of natural philosophy.',
            'For Readers': 'Read sequentially for Sendivogius\'s full argument, or dip into individual treatises: the First for his philosophy of nature, the Sixth for putrefaction, the Eleventh for practical instruction. The progression mirrors the alchemical work itself — from raw understanding to refined practice.'
        },
        'keywords': ['alchemy', 'sendivogius', 'twelve-treatises', 'transmutation', 'philosophers-stone'],
        'metadata': {}
    })

    # L2: Supplementary Texts (Epilogue, Preface to Riddle, Parable, Dialogue)
    supp_ids = ['epilogue', 'preface-to-riddle', 'parable-riddle', 'dialogue-mercury']
    sort_order += 1
    l2_items.append({
        'id': 'l2-supplementary-texts',
        'name': 'Supplementary Alchemical Texts',
        'sort_order': sort_order,
        'category': 'new-light-of-alchymie',
        'level': 2,
        'composite_of': supp_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The supplementary texts appended to the Twelve Treatises: Sendivogius\'s Epilogue summarizing his work, a Preface introducing the allegorical Riddle, the Parable itself (a rich alchemical allegory of Neptune\'s island and the Philosophers\' Stone), and the famous Dialogue between Mercury, the Alchymist, and Nature — a satirical and instructive dramatic piece warning against misunderstanding alchemical principles.',
            'Themes': 'Allegory and parable as vehicles for esoteric truth; the comedy of the ignorant alchemist; Mercury as trickster and teacher; Nature as final authority.',
            'For Readers': 'The Parable is the literary jewel of the collection — read it as visionary fiction. The Dialogue is both entertaining satire and practical instruction, showing what happens when one pursues alchemy through book-learning alone.'
        },
        'keywords': ['allegory', 'parable', 'dialogue', 'mercury', 'satire', 'riddle'],
        'metadata': {}
    })

    # L2: Treatise of Sulphur — Elements
    element_ids = ['sulphur-element-earth', 'sulphur-element-water', 'sulphur-element-aire', 'sulphur-element-fire']
    sort_order += 1
    l2_items.append({
        'id': 'l2-four-elements',
        'name': 'The Four Elements',
        'sort_order': sort_order,
        'category': 'treatise-of-sulphur',
        'level': 2,
        'composite_of': element_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'Sendivogius\'s detailed exposition of the four classical elements — Earth, Water, Aire, and Fire — as they relate to alchemical transformation. Each element is described not merely as a substance but as a living principle with its own character, role in generation, and relationship to the others. Earth is the receptacle, Water the carrier, Aire the mediator, Fire the purifier.',
            'Themes': 'Elemental cosmology; the interplay of elements in generation and corruption; each element containing the others in seed form; the Central Fire as life-principle.',
            'For Readers': 'A systematic alchemical physics. Compare with Aristotle\'s elements or Chinese Five Elements theory. Fire is the most philosophically rich section, touching on the secret fire that drives all transformation.'
        },
        'keywords': ['elements', 'earth', 'water', 'air', 'fire', 'cosmology', 'sulphur'],
        'metadata': {}
    })

    # L2: Treatise of Sulphur — Principles
    principle_ids = ['sulphur-second-principle', 'sulphur-three-principles', 'sulphur-of-sulphur']
    sort_order += 1
    l2_items.append({
        'id': 'l2-principles',
        'name': 'The Principles of All Things',
        'sort_order': sort_order,
        'category': 'treatise-of-sulphur',
        'level': 2,
        'composite_of': principle_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The theoretical core of the Treatise of Sulphur: Sendivogius\'s account of the Three Principles (Mercury, Sulphur, Salt) and their origin from the Four Elements. Sulphur is placed first among principles as the most worthy — the tinging, congealing, and ripening force that gives metals their identity.',
            'Themes': 'Mercury-Sulphur-Salt as the tria prima; Sulphur as the soul of metals; the origin of principles from elements; the relationship between macrocosm and microcosm.',
            'For Readers': 'This is the philosophical heart of Sendivogius\'s system. Understanding his Three Principles is essential for interpreting both his and Paracelsus\'s work. The chapter "Of Sulphur" is particularly dense and rewarding.'
        },
        'keywords': ['three-principles', 'mercury', 'sulphur', 'salt', 'tria-prima'],
        'metadata': {}
    })

    # L2: Paracelsus — Generation, Growth, and Preservation (Books 1-3)
    life_cycle_1 = ['nature-book-01', 'nature-book-02', 'nature-book-03']
    sort_order += 1
    l2_items.append({
        'id': 'l2-generation-growth',
        'name': 'Generation, Growth, and Preservation',
        'sort_order': sort_order,
        'category': 'nature-of-things',
        'level': 2,
        'composite_of': life_cycle_1,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The first three books of Paracelsus\'s Nature of Things treat the coming-into-being of all natural things. Book 1 covers generation from putrefaction — including the famous recipe for generating a Homunculus. Book 2 discusses growth and increase in metals, stones, and living things. Book 3 addresses preservation: how to protect bodies from decay through balsam, salt, and the art of embalming.',
            'Themes': 'Putrefaction as the mother of generation; the Homunculus as artificial human; growth through nourishment and celestial influence; the art of preservation against corruption.',
            'For Readers': 'Begin here for Paracelsus at his most visionary and provocative. The Homunculus passage in Book 1 is one of the most famous in alchemical literature. Book 3 bridges alchemy and early medicine.'
        },
        'keywords': ['paracelsus', 'generation', 'homunculus', 'growth', 'preservation', 'putrefaction'],
        'metadata': {}
    })

    # L2: Paracelsus — Life, Death, and Resurrection (Books 4-6)
    life_cycle_2 = ['nature-book-04', 'nature-book-05', 'nature-book-06']
    sort_order += 1
    l2_items.append({
        'id': 'l2-life-death-resurrection',
        'name': 'Life, Death, and Resurrection',
        'sort_order': sort_order,
        'category': 'nature-of-things',
        'level': 2,
        'composite_of': life_cycle_2,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The middle triad of Paracelsus\'s work addresses the great cycle: Life (Book 4) explores the vital force in all things, from metals to humans; Death (Book 5) catalogs the forms of decay, destruction, and ruin; Resurrection (Book 6) treats the renewal and restoration of things thought destroyed — from metals to plants to the human body.',
            'Themes': 'The vital spirit (Archeus) as animating principle; death as transformation rather than annihilation; resurrection as the alchemist\'s supreme art; the phoenix as emblem of renewal.',
            'For Readers': 'This triad mirrors the alchemical stages of nigredo (death), albedo, and rubedo (resurrection). Book 6 on Resurrection is especially rich — Paracelsus argues that everything destroyed can be restored through art, a radical claim for any era.'
        },
        'keywords': ['paracelsus', 'life', 'death', 'resurrection', 'renewal', 'archeus'],
        'metadata': {}
    })

    # L2: Paracelsus — Transmutation and Separation (Books 7-8)
    arts = ['nature-book-07', 'nature-book-08']
    sort_order += 1
    l2_items.append({
        'id': 'l2-transmutation-separation',
        'name': 'Transmutation and Separation',
        'sort_order': sort_order,
        'category': 'nature-of-things',
        'level': 2,
        'composite_of': arts,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The practical arts of alchemical transformation. Book 7 on Transmutation covers the changing of one substance into another — metals into gold, but also broader transformations in nature. Book 8 on Separation details the art of extracting essences: separating metals from ores, refining minerals, distilling vegetables, and processing animal substances.',
            'Themes': 'Transmutation as natural process accelerated by art; the grades of metallic perfection; separation as the key alchemical operation; the extraction of quintessence.',
            'For Readers': 'These are Paracelsus\'s most technically detailed books, closest to laboratory practice. Book 8\'s sub-sections on metals, minerals, vegetables, and animals provide a complete system of alchemical processing.'
        },
        'keywords': ['paracelsus', 'transmutation', 'separation', 'distillation', 'extraction'],
        'metadata': {}
    })

    # L2: Paracelsus — Signatures (Book 9 sub-sections)
    sig_ids = ['nature-book-09-monstrous', 'nature-book-09-physiognomy',
               'nature-book-09-chiromancy', 'nature-book-09-minerall', 'nature-book-09-peculiar']
    sort_order += 1
    l2_items.append({
        'id': 'l2-signatures',
        'name': 'The Doctrine of Signatures',
        'sort_order': sort_order,
        'category': 'nature-of-things',
        'level': 2,
        'composite_of': sig_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'Book 9\'s detailed sub-sections expound Paracelsus\'s famous Doctrine of Signatures — the idea that all things bear visible signs of their inner nature and purpose. Covers monstrous signs in humans, astrological physiognomy, chiromancy (palmistry), mineral signatures, and peculiar signs of natural and supernatural things.',
            'Themes': 'The visible world as text to be read; correspondence between outer form and inner virtue; astrology as signature-reading; the body as map of the cosmos.',
            'For Readers': 'The Doctrine of Signatures influenced herbalism, homeopathy, and holistic medicine for centuries. The physiognomy and chiromancy sections show how Renaissance thinkers read the human body as a microcosm of celestial influences.'
        },
        'keywords': ['paracelsus', 'signatures', 'physiognomy', 'chiromancy', 'signs', 'doctrine-of-signatures'],
        'metadata': {}
    })

    return l2_items


def build_l3_items(start_sort):
    """Build L3 meta-categories."""
    l3_items = []
    sort_order = start_sort

    # L3: Sendivogius's Alchemical Philosophy
    sort_order += 1
    l3_items.append({
        'id': 'l3-sendivogius',
        'name': 'Sendivogius: A New Light and the Treatise of Sulphur',
        'sort_order': sort_order,
        'category': 'meta',
        'level': 3,
        'composite_of': ['l2-twelve-treatises', 'l2-supplementary-texts',
                         'l2-four-elements', 'l2-principles'],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The complete alchemical philosophy of Michal Sedziwój (Sendivogius), comprising A New Light of Alchymie and the Treatise of Sulphur. Sendivogius presents a systematic natural philosophy grounded in direct observation of nature, arguing that the Philosophers\' Stone is not a fantasy but the logical culmination of understanding how nature generates, transforms, and perfects matter. His work bridges medieval alchemy and early modern chemistry.',
            'Themes': 'Nature as the sole teacher; the unity of matter; seed and sulphur as generative principles; the four elements as living forces; the Stone as nature\'s perfection achieved through art.',
            'Historical Context': 'Sendivogius (1566-1636) was a Polish alchemist whose writings were among the most influential in 17th-century Europe. His concept of "aerial food" (cibus aereus) — a life-giving substance in the air — anticipated the discovery of oxygen by over 150 years. Newton studied his works closely.'
        },
        'keywords': ['sendivogius', 'alchemy', 'natural-philosophy', 'philosophers-stone', 'sulphur'],
        'metadata': {}
    })

    # L3: Paracelsus's Nature of Things
    sort_order += 1
    l3_items.append({
        'id': 'l3-paracelsus',
        'name': 'Paracelsus: Of the Nature of Things',
        'sort_order': sort_order,
        'category': 'meta',
        'level': 3,
        'composite_of': ['l2-generation-growth', 'l2-life-death-resurrection',
                         'l2-transmutation-separation', 'l2-signatures'],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The Nine Books of the Nature of Things by Paracelsus (1493-1541), covering the complete cycle of natural existence: generation, growth, preservation, life, death, resurrection, transmutation, separation, and signatures. This is Paracelsus\'s most systematic natural philosophy, treating all of creation — minerals, plants, animals, humans, and spirits — as subject to the same alchemical processes.',
            'Themes': 'The unity of all natural processes; the Archeus (vital force) as governing principle; putrefaction as the mother of all generation; the possibility of resurrection through art; the readable signatures of nature.',
            'Historical Context': 'Paracelsus revolutionized medicine and chemistry by insisting on observation and experiment over classical authority. His concept of the tria prima (Mercury, Sulphur, Salt) as the three principles of all things replaced the Aristotelian four-element theory and laid groundwork for modern chemistry. His Doctrine of Signatures influenced medicine into the 19th century.'
        },
        'keywords': ['paracelsus', 'nature-of-things', 'natural-philosophy', 'archeus', 'tria-prima'],
        'metadata': {}
    })

    # L3: The Complete Alchemical Library
    sort_order += 1
    l3_items.append({
        'id': 'l3-complete-work',
        'name': 'A New Light of Alchymie: The Complete Work',
        'sort_order': sort_order,
        'category': 'meta',
        'level': 3,
        'composite_of': ['l3-sendivogius', 'l3-paracelsus', 'chymicall-dictionary'],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The complete 1650 volume translated by John French, M.D., bringing together three major alchemical works: Sendivogius\'s A New Light of Alchymie and Treatise of Sulphur, Paracelsus\'s Nine Books of the Nature of Things, and a comprehensive Chymicall Dictionary. Together they form one of the most important alchemical compilations in the English language, offering theory, practice, allegory, and reference in a single volume.',
            'Themes': 'The grand synthesis of Renaissance alchemical thought; nature as divine text; the transformation of matter as spiritual practice; the unity of macrocosm and microcosm.',
            'Historical Context': 'Published in London in 1650 during the English Civil War and the flowering of English interest in Hermetic philosophy. Translator John French was a physician and chemist who sought to make Continental alchemical knowledge available to English readers. This compilation influenced figures from Robert Boyle to Isaac Newton.'
        },
        'keywords': ['alchemy', 'compilation', 'sendivogius', 'paracelsus', 'john-french', '1650'],
        'metadata': {}
    })

    return l3_items


def build_grammar():
    """Build the complete grammar."""
    text = read_seed()
    body = isolate_body(text)

    sections = extract_sections(body)
    print(f"Extracted {len(sections)} sections")

    l1_items = build_l1_items(sections)
    print(f"Built {len(l1_items)} L1 items")

    l2_items = build_l2_items(l1_items, len(l1_items))
    print(f"Built {len(l2_items)} L2 items")

    l3_items = build_l3_items(len(l1_items) + len(l2_items))
    print(f"Built {len(l3_items)} L3 items")

    all_items = l1_items + l2_items + l3_items

    # Re-number sort_order sequentially
    for i, item in enumerate(all_items):
        item['sort_order'] = i + 1

    grammar = {
        '_grammar_commons': {
            'schema_version': '1.0',
            'license': 'CC-BY-SA-4.0',
            'attribution': [
                {
                    'name': 'Michal Sedziwój (Sendivogius)',
                    'date': 'c. 1604',
                    'note': 'Author of A New Light of Alchymie and A Treatise of Sulphur'
                },
                {
                    'name': 'Paracelsus (Theophrastus von Hohenheim)',
                    'date': 'c. 1537',
                    'note': 'Author of Nine Books of the Nature of Things'
                },
                {
                    'name': 'John French',
                    'date': '1650',
                    'note': 'English translator (J.F., M.D.)'
                }
            ]
        },
        'name': 'A New Light of Alchymie',
        'description': (
            'A landmark 1650 compilation of alchemical philosophy translated by John French, M.D., '
            'bringing together Sendivogius\'s Twelve Treatises and Treatise of Sulphur, Paracelsus\'s '
            'Nine Books of the Nature of Things, and a comprehensive Chymicall Dictionary. '
            'Covers the full spectrum of Renaissance alchemical thought: the nature of matter, '
            'the four elements, the three principles (Mercury, Sulphur, Salt), the generation and '
            'transmutation of metals, the Philosophers\' Stone, and the Doctrine of Signatures.\n\n'
            'Source: Project Gutenberg eBook #61112 (https://www.gutenberg.org/ebooks/61112)\n\n'
            'PUBLIC DOMAIN ILLUSTRATION REFERENCES: Alchemical woodcuts and engravings from '
            '17th-century editions; Michael Maier\'s Atalanta Fugiens (1618) emblems; '
            'Heinrich Khunrath\'s Amphitheatrum Sapientiae Aeternae (1595) engravings; '
            'illustrations from Musaeum Hermeticum (1678).'
        ),
        'grammar_type': 'custom',
        'creator_name': 'PlayfulProcess',
        'tags': ['alchemy', 'esoteric', 'transmutation', 'philosophy', 'paracelsus'],
        'roots': ['mysticism', 'western-esotericism'],
        'shelves': ['wisdom'],
        'lineages': ['Shrei'],
        'worldview': 'animist',
        'items': all_items
    }

    return grammar


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    grammar = build_grammar()

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {OUTPUT}")
    print(f"Total items: {len(grammar['items'])}")

    # Quick validation
    items = grammar['items']
    ids = [i['id'] for i in items]
    dupes = [x for x in ids if ids.count(x) > 1]
    bad_refs = [(i['id'], r) for i in items for r in i.get('composite_of', []) if r not in ids]
    orders = [i['sort_order'] for i in items]

    print(f"\nValidation:")
    print(f"  L1: {sum(1 for i in items if i['level'] == 1)}")
    print(f"  L2: {sum(1 for i in items if i['level'] == 2)}")
    print(f"  L3: {sum(1 for i in items if i['level'] == 3)}")
    print(f"  Duplicate IDs: {dupes}")
    print(f"  Bad refs: {bad_refs}")
    print(f"  Sort orders sequential: {orders == list(range(1, len(items) + 1))}")
    print(f"  Sections: {sum(len(i.get('sections', {})) for i in items)}")


if __name__ == '__main__':
    main()
