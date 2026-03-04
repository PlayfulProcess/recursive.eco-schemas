#!/usr/bin/env python3
"""
Build grammar for Revelations of Divine Love by Julian of Norwich.
Source: Project Gutenberg eBook #52958

Parses 86 chapters organized around 16 Revelations (Shewings) from the seed text.
The text is a 14th-century mystical account by Julian of Norwich, an anchoress,
describing her visions of divine love received during a near-death illness in 1373.
"""

import json
import re
import os

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'revelations-divine-love.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'revelations-divine-love')
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


def strip_front_matter(text):
    """Remove everything before Chapter I (introduction, notes, contents, etc.)."""
    # Find "REVELATIONS OF DIVINE LOVE" followed by "CHAPTER I"
    match = re.search(r'\n\s*REVELATIONS OF DIVINE LOVE\s*\n\s*\n\s*CHAPTER I\b', text)
    if match:
        return text[match.start():].strip()
    # Fallback: find first CHAPTER I
    match = re.search(r'\n\s*CHAPTER I\b', text)
    if match:
        return text[match.start():].strip()
    return text


def roman_to_int(s):
    """Convert a Roman numeral string to integer."""
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
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


def parse_chapters(text):
    """Parse the text into chapters using 'CHAPTER <ROMAN>' headers."""
    # Pattern: CHAPTER followed by Roman numeral
    chapter_pattern = re.compile(r'\n\s*(CHAPTER\s+([IVXLC]+))\s*\n')

    matches = list(chapter_pattern.finditer(text))
    if not matches:
        print("ERROR: No chapters found!")
        return []

    chapters = []
    for i, match in enumerate(matches):
        chapter_num = roman_to_int(match.group(2))
        # Content starts after the CHAPTER line
        content_start = match.end()

        # Content ends at next chapter or end of text
        if i + 1 < len(matches):
            content_end = matches[i + 1].start()
        else:
            content_end = len(text)

        raw_content = text[content_start:content_end].strip()

        # Extract chapter subtitle (usually in quotes on the first non-empty line)
        subtitle = ''
        content_lines = raw_content.split('\n')
        content_text = raw_content

        # Look for subtitle in quotes at the start
        subtitle_lines = []
        content_start_line = 0
        for j, line in enumerate(content_lines):
            stripped = line.strip()
            if not stripped:
                if subtitle_lines:
                    content_start_line = j + 1
                    break
                continue
            # Subtitle lines are typically centered/quoted
            if stripped.startswith('"') or stripped.startswith("'") or stripped.startswith('_'):
                subtitle_lines.append(stripped)
                content_start_line = j + 1
            elif subtitle_lines:
                content_start_line = j
                break
            elif j < 4 and not stripped[0].isupper():
                # Continuation of subtitle
                subtitle_lines.append(stripped)
                content_start_line = j + 1
            else:
                content_start_line = j
                break

        if subtitle_lines:
            subtitle = ' '.join(subtitle_lines)
            # Clean up subtitle
            subtitle = re.sub(r'[_"]', '', subtitle).strip()
            # Get content after subtitle
            remaining_lines = content_lines[content_start_line:]
            content_text = '\n'.join(remaining_lines).strip()

        # Remove footnotes (lines starting with [ followed by a number)
        content_text = re.sub(r'\n\[(\d+)\][^\n]*', '', content_text)
        # Also remove inline footnote markers
        content_text = re.sub(r'\[(\d+)\]', '', content_text)
        # Clean up multiple blank lines
        content_text = re.sub(r'\n{3,}', '\n\n', content_text).strip()

        # Remove the POSTSCRIPT and anything after CHAPTER LXXXVI's main content
        if 'POSTSCRIPT BY A SCRIBE' in content_text:
            content_text = content_text[:content_text.index('POSTSCRIPT BY A SCRIBE')].strip()

        chapters.append({
            'number': chapter_num,
            'subtitle': subtitle,
            'text': content_text,
        })

    return chapters


# Mapping of chapters to Revelations
REVELATION_MAP = {
    # (start_chapter, end_chapter): revelation_number
    # Chapters 1-3: autobiographical preamble
    # Revelation 1: Chapters 4-9
    # Revelation 2: Chapter 10
    # Revelation 3: Chapter 11
    # Revelation 4: Chapter 12
    # Revelation 5: Chapter 13
    # Revelation 6: Chapter 14
    # Revelation 7: Chapter 15
    # Revelation 8: Chapters 16-21
    # Revelation 9: Chapters 22-23
    # Revelation 10: Chapter 24
    # Revelation 11: Chapter 25
    # Revelation 12: Chapter 26
    # Revelation 13: Chapters 27-40
    # Revelation 14: Chapters 41-63
    # Revelation 15: Chapters 64-65
    # Revelation 16 (confirming): Chapters 67-68
    # Autobiographical: Chapter 66, 69
    # Faith and Life: Chapters 70-85
    # Final: Chapter 86
}

CHAPTER_TO_REVELATION = {}
for ch in range(4, 10):
    CHAPTER_TO_REVELATION[ch] = 1
CHAPTER_TO_REVELATION[10] = 2
CHAPTER_TO_REVELATION[11] = 3
CHAPTER_TO_REVELATION[12] = 4
CHAPTER_TO_REVELATION[13] = 5
CHAPTER_TO_REVELATION[14] = 6
CHAPTER_TO_REVELATION[15] = 7
for ch in range(16, 22):
    CHAPTER_TO_REVELATION[ch] = 8
for ch in range(22, 24):
    CHAPTER_TO_REVELATION[ch] = 9
CHAPTER_TO_REVELATION[24] = 10
CHAPTER_TO_REVELATION[25] = 11
CHAPTER_TO_REVELATION[26] = 12
for ch in range(27, 41):
    CHAPTER_TO_REVELATION[ch] = 13
for ch in range(41, 64):
    CHAPTER_TO_REVELATION[ch] = 14
for ch in range(64, 66):
    CHAPTER_TO_REVELATION[ch] = 15
for ch in range(67, 69):
    CHAPTER_TO_REVELATION[ch] = 16


REVELATION_TITLES = {
    1: "The First Revelation: The Trinity and the Passion",
    2: "The Second Revelation: The Changing of His Face",
    3: "The Third Revelation: God Doeth All Things",
    4: "The Fourth Revelation: The Scourging",
    5: "The Fifth Revelation: The Fiend is Overcome",
    6: "The Sixth Revelation: The Thanking of Heaven",
    7: "The Seventh Revelation: Weal and Woe",
    8: "The Eighth Revelation: The Last Pains of Christ",
    9: "The Ninth Revelation: Joy in the Passion",
    10: "The Tenth Revelation: The Cloven Heart",
    11: "The Eleventh Revelation: His Dearworthy Mother",
    12: "The Twelfth Revelation: God is Most Worthy Being",
    13: "The Thirteenth Revelation: All Shall Be Well",
    14: "The Fourteenth Revelation: Prayer and Trust",
    15: "The Fifteenth Revelation: Fulfilment in Heaven",
    16: "The Sixteenth Revelation: The Indwelling of God",
}

REVELATION_DESCRIPTIONS = {
    1: "The Trinity is shewn through the suffering of Christ as Goodness, or Love all-working. Julian sees the blood trickle from under the crown of thorns, and in the same moment the Trinity fills her heart with joy. She sees the blessed Virgin as a simple maid, and is shown God's homely loving.",
    2: "Man's sight of God's Love is but partial because of sin's darkness. Julian sees Christ's face change colour, signifying His dearworthy Passion.",
    3: "All Being is Being of God and is good. Sin is no Being. Julian sees that God doeth all things, and all things are done that He doth.",
    4: "The stain of sin through lacking of human love is cleared away by the Death of Christ in His Love. Julian sees the plenteous shedding of His blood.",
    5: "By Love's sacrifice in Christ, the evil suffered for Love's increase is overcome forever. The Fiend is scorned and his malice turned to joy.",
    6: "The travail of Man against evil on earth is a glory accepted by Love in Heaven. God thanks His servants with worshipful joy.",
    7: "It is of God's will, for our learning, that on earth we change between joy of light and pain of darkness. We are kept securely in love in both.",
    8: "Of the oneness of God and Man in the Passion of Christ, through compassion of the Creature with Christ and of Christ with the Creature. Julian describes the drying of Christ's body, the last pains, and the great comfort that follows.",
    9: "Of the worshipful entering of Man's soul into the Joy of Love Divine in the Passion. Julian is offered the choice of looking up to heaven, and understands that the Cross is her heaven.",
    10: "Of the thankful entering of the soul into the Peace of the Endless Love opened up for Man in the time of the Passion. Christ shows His blessed heart cloven in two.",
    11: "Of Christ's Raising, fulfilling Love to the souls of men, as beheld in the love between Him and His Mother. Julian sees Mary three times in ghostly sight.",
    12: "All that the soul lives by and loves is God, through Christ. Our Lord is most worthy Being.",
    13: "Man's finite love was suffered by Infinite Love to fail, that falling thus through sin, the creature might more deeply know the Creator's Love. This longest revelation contains the famous assurance: 'All shall be well, and all shall be well, and all manner of thing shall be well.'",
    14: "Beginning on earth, Prayer makes the soul one with God. Julian is taught about beseeching and beholding, and receives deep teachings about the Lord and the Servant parable.",
    15: "Of Love's Fulfilment in Heaven. Julian sees that we shall suddenly be taken from all our pain.",
    16: "The Indwelling of God in the Soul, now and forever. 'Thou shalt not be overcome.' This confirming revelation assures Julian that the Blessed Trinity dwells endlessly in our soul.",
}


def build_items(chapters):
    """Build L1 items from parsed chapters."""
    items = []
    sort_order = 0

    for ch in chapters:
        num = ch['number']
        item_id = f"chapter-{num}"

        # Build name
        name = f"Chapter {num}"
        if ch['subtitle']:
            # Truncate long subtitles
            sub = ch['subtitle']
            if len(sub) > 80:
                sub = sub[:77] + '...'
            name = f"Chapter {num}: {sub}"

        # Determine category
        rev = CHAPTER_TO_REVELATION.get(num)
        if rev:
            category = f"revelation-{rev}"
        elif num <= 3:
            category = "preamble"
        elif num in (66, 69):
            category = "autobiographical"
        elif num >= 70 and num <= 85:
            category = "faith-and-life"
        elif num == 86:
            category = "conclusion"
        else:
            category = "teaching"

        # Build keywords from content
        keywords = []
        text_lower = ch['text'].lower()
        keyword_checks = [
            ('love', 'love'), ('prayer', 'prayer'), ('sin', 'sin'),
            ('passion', 'passion'), ('trinity', 'trinity'), ('mercy', 'mercy'),
            ('compassion', 'compassion'), ('joy', 'joy'), ('suffering', 'suffering'),
            ('faith', 'faith'), ('grace', 'grace'), ('bliss', 'bliss'),
            ('soul', 'soul'), ('mother', 'motherhood'), ('wound', 'wounds'),
        ]
        for term, kw in keyword_checks:
            if term in text_lower:
                keywords.append(kw)
        keywords = keywords[:6]  # Limit keywords

        item = {
            'id': item_id,
            'name': name,
            'sort_order': sort_order,
            'category': category,
            'level': 1,
            'sections': {
                'Text': ch['text']
            },
            'keywords': keywords,
            'metadata': {
                'chapter_number': num,
            }
        }
        if rev:
            item['metadata']['revelation_number'] = rev

        items.append(item)
        sort_order += 1

    return items, sort_order


def build_l2_items(chapters, sort_start):
    """Build L2 items: one for each Revelation, plus structural groupings."""
    items = []
    sort_order = sort_start

    # Preamble group
    items.append({
        'id': 'preamble',
        'name': 'Preamble: The Three Desires',
        'sort_order': sort_order,
        'category': 'structural-group',
        'level': 2,
        'composite_of': ['chapter-1', 'chapter-2', 'chapter-3'],
        'relationship_type': 'emergence',
        'sections': {
            'About': "Julian's autobiographical introduction to the Sixteen Shewings. She describes the three gifts she desired from God: a vivid sense of Christ's Passion, a bodily sickness unto death at age thirty, and three spiritual wounds (contrition, compassion, and longing for God). The sickness came as asked, and during it the visions were granted.",
            'For Readers': "These opening chapters set the stage. Julian is not a theologian constructing arguments but a woman reporting an experience. Notice her humility ('a simple creature unlettered') and her precision -- she carefully notes dates, times, and physical sensations. This combination of mystical openness and careful observation runs through the entire work."
        },
        'keywords': ['autobiography', 'desire', 'sickness', 'preparation'],
        'metadata': {}
    })
    sort_order += 1

    # One L2 per Revelation
    for rev_num in range(1, 17):
        rev_chapters = [f"chapter-{ch}" for ch in sorted(
            [c for c, r in CHAPTER_TO_REVELATION.items() if r == rev_num]
        )]
        if not rev_chapters:
            continue

        items.append({
            'id': f'revelation-{rev_num}',
            'name': REVELATION_TITLES[rev_num],
            'sort_order': sort_order,
            'category': 'revelation',
            'level': 2,
            'composite_of': rev_chapters,
            'relationship_type': 'emergence',
            'sections': {
                'About': REVELATION_DESCRIPTIONS[rev_num],
                'For Readers': ("This is the longest and most complex revelation, containing Julian's most famous passage. Read slowly and contemplatively, as Julian herself would have done in her anchorhold at Norwich." if rev_num == 13 else "This is the core content of the revelation. Read slowly and contemplatively, as Julian herself would have done in her anchorhold at Norwich.")
            },
            'keywords': ['revelation', 'shewing', 'vision'],
            'metadata': {'revelation_number': rev_num}
        })
        sort_order += 1

    # Autobiographical interludes
    items.append({
        'id': 'autobiographical-interludes',
        'name': 'Autobiographical Interludes: Assaying of Faith',
        'sort_order': sort_order,
        'category': 'structural-group',
        'level': 2,
        'composite_of': ['chapter-66', 'chapter-69'],
        'relationship_type': 'emergence',
        'sections': {
            'About': "Two deeply honest autobiographical chapters in which Julian describes her falls into doubt after the Shewings. In Chapter 66, she recounts how she fell through frailty into questioning whether the whole experience was delirium; in Chapter 69, she describes a terrifying dream of fiends. Both times she was rescued by grace. These chapters ground the mystical visions in lived human experience.",
            'For Readers': "These are perhaps the most humanly relatable passages in the book. Julian does not present herself as a spiritual hero but as someone who doubted her own experience -- 'I raved' -- and had to be brought back to trust. The honesty is what makes her testimony credible."
        },
        'keywords': ['doubt', 'temptation', 'honesty', 'faith', 'struggle'],
        'metadata': {}
    })
    sort_order += 1

    # Faith and Life
    faith_chapters = [f"chapter-{ch}" for ch in range(70, 86)]
    items.append({
        'id': 'faith-and-life',
        'name': 'The Life of Faith: Charity, Hope, and the Meaning',
        'sort_order': sort_order,
        'category': 'structural-group',
        'level': 2,
        'composite_of': faith_chapters,
        'relationship_type': 'emergence',
        'sections': {
            'About': "The extended meditation that follows the Sixteen Revelations, in which Julian reflects on the life of faith as kept by Charity and led by Hope. These chapters integrate the visions into a coherent theology of love, addressing sin, suffering, prayer, and the soul's relationship to God. They culminate in the luminous Chapter 86: 'Love was His meaning.'",
            'For Readers': "These later chapters are where Julian becomes a theologian, though she would never have called herself one. She weaves together everything she has been shown into a vision of reality grounded in love. The final chapter is one of the most quoted passages in all mystical literature."
        },
        'keywords': ['faith', 'charity', 'hope', 'theology', 'love', 'meaning'],
        'metadata': {}
    })
    sort_order += 1

    # Conclusion
    items.append({
        'id': 'love-was-his-meaning',
        'name': '"Love Was His Meaning"',
        'sort_order': sort_order,
        'category': 'structural-group',
        'level': 2,
        'composite_of': ['chapter-86'],
        'relationship_type': 'emergence',
        'sections': {
            'About': "The luminous final chapter in which Julian receives the key to her entire Revelation, fifteen years after the visions themselves: 'Wouldst thou learn thy Lord's meaning in this thing? Learn it well: Love was His meaning. Who shewed it thee? Love. What shewed He thee? Love. Wherefore shewed it He? For Love.' This is the heart of the whole book.",
            'For Readers': "Read this chapter last, and then read it first. It is both the conclusion and the key. Everything in the Revelations -- the suffering, the joy, the doubt, the teaching about sin and prayer -- resolves into this single insight: Love."
        },
        'keywords': ['love', 'meaning', 'conclusion', 'revelation'],
        'metadata': {}
    })
    sort_order += 1

    # Thematic groupings
    items.append({
        'id': 'all-shall-be-well',
        'name': 'All Shall Be Well: Julian on Sin and Redemption',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': [
            'chapter-11', 'chapter-27', 'chapter-29', 'chapter-30',
            'chapter-31', 'chapter-32', 'chapter-33', 'chapter-35',
            'chapter-38', 'chapter-39', 'chapter-40', 'chapter-85', 'chapter-86'
        ],
        'relationship_type': 'emergence',
        'sections': {
            'About': "Julian's most famous and most controversial teaching: that despite the reality of sin, 'all shall be well, and all shall be well, and all manner of thing shall be well.' This is not naive optimism but a hard-won trust, arrived at through honest confrontation with the horror of sin and suffering. Julian wrestles with the problem of evil more honestly than most theologians, ultimately resting in trust that God has a 'Great Deed' yet to be done that will make all things well in ways we cannot now understand.",
            'For Readers': "This theme makes Julian astonishingly modern. She does not explain away suffering or minimize sin. She simply reports what she was shown: that Love is stronger. The phrase 'all shall be well' has entered common speech, but in context it is far more radical and more costly than it sounds."
        },
        'keywords': ['sin', 'redemption', 'hope', 'well-being', 'optimism', 'trust'],
        'metadata': {}
    })
    sort_order += 1

    items.append({
        'id': 'god-as-mother',
        'name': 'God as Mother: Julian on Divine Motherhood',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': [
            'chapter-25', 'chapter-52', 'chapter-57', 'chapter-58',
            'chapter-59', 'chapter-60', 'chapter-61', 'chapter-62', 'chapter-63'
        ],
        'relationship_type': 'emergence',
        'sections': {
            'About': "Julian's extraordinary teaching on God as Mother -- one of the most developed maternal theologies in Christian history. She teaches that Christ is our true Mother, who bears us, feeds us, tends us, and never abandons us. This is not metaphor layered onto theology but reported experience: Julian saw motherhood as intrinsic to the divine nature. 'As verily as God is our Father, so verily is God our Mother.'",
            'For Readers': "This theme has made Julian beloved in feminist theology, but she would not have thought of herself as radical. She was simply reporting what she saw. The language of divine motherhood was not unknown in medieval mysticism (Bernard of Clairvaux, Anselm), but Julian develops it further than any other writer of her era."
        },
        'keywords': ['mother', 'motherhood', 'feminine', 'nurture', 'Christ', 'tenderness'],
        'metadata': {}
    })
    sort_order += 1

    items.append({
        'id': 'prayer-and-seeking',
        'name': 'Prayer and Seeking: The Soul Before God',
        'sort_order': sort_order,
        'category': 'thematic-group',
        'level': 2,
        'composite_of': [
            'chapter-5', 'chapter-6', 'chapter-41', 'chapter-42',
            'chapter-43', 'chapter-44', 'chapter-45', 'chapter-46'
        ],
        'relationship_type': 'emergence',
        'sections': {
            'About': "Julian's teaching on prayer, in which she discovers that God is the ground of our beseeching -- we do not pray to a distant God but from within God. Prayer is not about changing God's mind but about aligning our will with Love. 'I am the Ground of thy beseeching.' This is contemplative prayer at its deepest: not asking for things but entering into union.",
            'For Readers': "Julian anticipates what later contemplatives would call 'centering prayer' or 'prayer of the heart.' Her insight -- that prayer originates in God, not in us -- is liberating for anyone who has struggled with feeling that their prayers are inadequate."
        },
        'keywords': ['prayer', 'seeking', 'contemplation', 'union', 'beseeching'],
        'metadata': {}
    })
    sort_order += 1

    return items, sort_order


def build_l3_items(sort_start):
    """Build L3 meta-category items."""
    items = []
    sort_order = sort_start

    items.append({
        'id': 'the-sixteen-revelations',
        'name': 'The Sixteen Revelations',
        'sort_order': sort_order,
        'category': 'meta-theme',
        'level': 3,
        'composite_of': [f'revelation-{i}' for i in range(1, 17)],
        'relationship_type': 'emergence',
        'sections': {
            'About': "The sixteen visions or 'Shewings' granted to Julian of Norwich on May 13, 1373, during a near-fatal illness. They came in rapid succession over about five hours, with a final confirming vision the following night. Together they form one of the most profound and coherent mystical documents in the English language -- a sustained meditation on divine love as the ground and meaning of all existence.",
            'Legacy': "Julian's Revelations are the earliest surviving book written by a woman in English. They have influenced six centuries of contemplative thought, from the medieval mystics through the Anglican divines to modern writers like T.S. Eliot (who quotes Julian in Four Quartets) and Thomas Merton. Her theology of universal love, divine motherhood, and ultimate redemption continues to speak to seekers across traditions."
        },
        'keywords': ['revelations', 'visions', 'shewings', 'mysticism', 'love', 'divine'],
        'metadata': {}
    })
    sort_order += 1

    items.append({
        'id': 'julians-theology-of-love',
        'name': "Julian's Theology of Love",
        'sort_order': sort_order,
        'category': 'meta-theme',
        'level': 3,
        'composite_of': [
            'all-shall-be-well', 'god-as-mother', 'prayer-and-seeking',
            'love-was-his-meaning', 'autobiographical-interludes', 'faith-and-life'
        ],
        'relationship_type': 'emergence',
        'sections': {
            'About': "The thematic architecture of Julian's work: her teaching on sin and redemption ('All shall be well'), her theology of divine motherhood, her understanding of prayer as arising from within God, and her ultimate insight that Love is the meaning of everything. These themes interweave throughout the Revelations and the extended meditations that follow, forming a coherent and radical theology grounded entirely in experienced love.",
            'Legacy': "Julian's influence extends far beyond Christian mysticism. Her insistence on universal love, her refusal to accept that any soul is ultimately lost, her gentle feminism, and her contemplative approach to doubt and suffering resonate with Buddhist compassion practice, Sufi love-mysticism, and modern mindfulness traditions. Marsha Linehan's dialectical emphasis on acceptance within change echoes Julian's holding of suffering and joy in one vision."
        },
        'keywords': ['theology', 'love', 'mysticism', 'contemplation', 'wisdom'],
        'metadata': {}
    })
    sort_order += 1

    return items, sort_order


def build_grammar():
    """Build the complete grammar."""
    raw = read_seed()
    text = strip_gutenberg(raw)
    text = strip_front_matter(text)

    chapters = parse_chapters(text)
    print(f"Found {len(chapters)} chapters")

    if len(chapters) < 80:
        print(f"WARNING: Expected ~86 chapters, found {len(chapters)}")

    # Build items
    l1_items, next_sort = build_items(chapters)
    l2_items, next_sort = build_l2_items(chapters, next_sort)
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
                {'name': 'Julian of Norwich', 'date': '1373-1393', 'note': 'Author, anchoress at St Julian\'s Church, Norwich'},
                {'name': 'Grace Warrack', 'date': '1901', 'note': 'Editor, from the Sloane MS. in the British Museum'}
            ]
        },
        'name': 'Revelations of Divine Love',
        'description': (
            "Julian of Norwich's Revelations of Divine Love (c. 1393) -- the earliest surviving book "
            "written by a woman in English. On May 13, 1373, during a near-fatal illness, Julian received "
            "sixteen visions ('Shewings') of divine love, which she spent the next twenty years meditating "
            "upon and writing down. The result is one of the most profound mystical texts in any language: "
            "a sustained theology of love as the ground and meaning of all existence, containing the famous "
            "assurance 'All shall be well, and all shall be well, and all manner of thing shall be well.' "
            "Julian's teachings on divine motherhood, contemplative prayer, and the ultimate redemption of "
            "all things remain startlingly relevant.\n\n"
            "Source: Project Gutenberg eBook #52958 (https://www.gutenberg.org/ebooks/52958). "
            "Grace Warrack edition (1901), from the Sloane MS. in the British Museum.\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Medieval illuminated manuscripts of the Norwich school. "
            "Images from the Luttrell Psalter (c. 1325-1340). Anchoress cells and medieval church architecture. "
            "Phoebe Anna Traquair's title-page design for the 1901 Warrack edition."
        ),
        'grammar_type': 'custom',
        'creator_name': 'PlayfulProcess',
        'tags': ['mysticism', 'christian', 'contemplative', 'medieval', 'public-domain', 'full-text', 'wisdom', 'feminine-voice', 'love'],
        'roots': ['western-mysticism', 'contemplative-practice'],
        'shelves': ['wisdom'],
        'lineages': ['Linehan'],
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
    print(f"  L1 items: {l1_count} (chapters)")
    print(f"  L2 items: {l2_count} (revelations + thematic groups)")
    print(f"  L3 items: {l3_count}")
    print(f"  Total: {len(all_items)} items")


if __name__ == '__main__':
    build_grammar()
