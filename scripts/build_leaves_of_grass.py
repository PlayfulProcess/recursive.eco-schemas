#!/usr/bin/env python3
"""
Build grammar.json for Walt Whitman's Leaves of Grass.

Parses the Project Gutenberg text (eBook #1322) into a structured grammar
with L1 (individual poems), L2 (book/cluster groupings + thematic groups),
and L3 (meta-categories).

Source: 1891-92 "deathbed" edition.
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
SEED_FILE = PROJECT_DIR / "seeds" / "leaves-of-grass.txt"
OUTPUT_FILE = PROJECT_DIR / "grammars" / "leaves-of-grass" / "grammar.json"


def strip_gutenberg(text):
    """Remove Project Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK LEAVES OF GRASS ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK LEAVES OF GRASS ***"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def parse_books(text):
    """Split text into books by BOOK headings."""
    # Find all BOOK markers with their line positions
    # Use [^\S\n] (whitespace except newline) to avoid matching across lines
    book_pattern = re.compile(r'^(BOOK[^\S\n]*([IVXLC]+)\.?[^\S\n]*\.?[^\S\n]*(.*?))$', re.MULTILINE)
    matches = list(book_pattern.finditer(text))

    books = []
    for i, match in enumerate(matches):
        book_header = match.group(1).strip()
        roman = match.group(2).strip()
        book_name = match.group(3).strip().rstrip('.')

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        book_text = text[start:end].strip()
        books.append({
            'roman': roman,
            'name': book_name,
            'text': book_text,
            'header': book_header,
        })

    return books


def roman_to_int(roman):
    """Convert Roman numeral to integer."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    for i, c in enumerate(roman):
        if i + 1 < len(roman) and values.get(c, 0) < values.get(roman[i + 1], 0):
            result -= values.get(c, 0)
        else:
            result += values.get(c, 0)
    return result


def parse_poems_from_book(book_text):
    """Extract individual poems from a book's text.

    Poems are identified by title lines (lines with capitalized words that
    aren't indented verse lines) followed by indented verse content.
    """
    lines = book_text.split('\n')
    poems = []
    current_title = None
    current_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines at start
        if not stripped and current_title is None:
            i += 1
            continue

        # Detect poem title: non-empty, not heavily indented, not a numbered section marker,
        # not starting with common verse patterns
        is_title = False
        if stripped and not line.startswith('  ') and not line.startswith('\t'):
            # Title lines are flush left or nearly so
            # They should not be just a number (section markers like "1", "2")
            if not re.match(r'^\d+$', stripped):
                # Check it's not just a continuation of verse
                # Titles are typically Title Case or ALL CAPS
                if (re.match(r'^[A-Z]', stripped) and
                    not stripped.startswith('(') and
                    len(stripped) > 1):
                    is_title = True

        if is_title:
            # Save previous poem
            if current_title is not None:
                poem_text = '\n'.join(current_lines).strip()
                if poem_text:
                    poems.append((current_title, poem_text))
            current_title = stripped
            current_lines = []
        else:
            if current_title is not None:
                current_lines.append(line)

        i += 1

    # Save last poem
    if current_title is not None:
        poem_text = '\n'.join(current_lines).strip()
        if poem_text:
            poems.append((current_title, poem_text))

    return poems


def clean_poem_text(text):
    """Clean up poem text - remove excessive blank lines, normalize indentation."""
    lines = text.split('\n')
    # Remove leading/trailing blank lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    # Collapse runs of 3+ blank lines to 2
    cleaned = []
    blank_count = 0
    for line in lines:
        if not line.strip():
            blank_count += 1
            if blank_count <= 2:
                cleaned.append(line)
        else:
            blank_count = 0
            cleaned.append(line)

    return '\n'.join(cleaned)


def make_id(name):
    """Convert a poem name to a valid ID."""
    # Remove special characters, lowercase, hyphenate
    s = name.lower()
    s = re.sub(r"[''']", '', s)
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    # Truncate very long IDs
    if len(s) > 60:
        s = s[:60].rsplit('-', 1)[0]
    return s


def generate_keywords(title, text):
    """Generate keywords from poem title and content."""
    keywords = []

    # Theme detection from common Whitman motifs
    theme_patterns = {
        'democracy': r'\bdemocra\w+\b',
        'nature': r'\b(?:grass|tree|leaf|leaves|bird|sea|ocean|river|earth|star|sun|moon|flower|wind)\b',
        'body': r'\b(?:body|bodies|flesh|blood|physiology|limb|muscle|organ)\b',
        'soul': r'\b(?:soul|spirit|eternal|immortal)\b',
        'death': r'\b(?:death|dead|die|dying|grave|burial|coffin|corpse)\b',
        'war': r'\b(?:war|battle|soldier|army|camp|drum|march|wound|military)\b',
        'love': r'\b(?:love|lover|beloved|kiss|embrace|passion|desire)\b',
        'identity': r'\b(?:self|myself|identity|who am i|contain)\b',
        'america': r'\b(?:america|states|manhattan|brooklyn|california|new york|union)\b',
        'comradeship': r'\b(?:comrade|companion|friend|camerado|manly love)\b',
        'sea': r'\b(?:sea|ocean|ship|sail|voyage|shore|wave|tide|mariner)\b',
        'music': r'\b(?:sing|song|chant|music|hymn|carol|poem)\b',
        'labor': r'\b(?:work|labor|toil|build|carpenter|mechanic|farmer|occupation)\b',
        'night': r'\b(?:night|dark|midnight|sleep|dream|star)\b',
        'city': r'\b(?:city|street|crowd|broadway|pavement|omnibus)\b',
        'spirituality': r'\b(?:god|divine|prayer|worship|faith|sacred|holy)\b',
        'freedom': r'\b(?:free|freedom|liberty|libertad)\b',
        'transcendence': r'\b(?:transcend|infinite|cosmos|universe|eternal|vast)\b',
        'old-age': r'\b(?:old age|seventy|aged|twilight|last|farewell|good-bye)\b',
        'memory': r'\b(?:memory|remember|recollect|reminiscence)\b',
    }

    combined = (title + ' ' + text[:2000]).lower()
    for keyword, pattern in theme_patterns.items():
        if re.search(pattern, combined, re.IGNORECASE):
            keywords.append(keyword)

    return keywords[:8]  # Limit to 8 keywords


# Book number -> (cluster name, category slug)
# Maps the 35 books to their traditional cluster names
BOOK_CLUSTERS = {
    'I': ('Inscriptions', 'inscriptions'),
    'II': ('Starting from Paumanok', 'starting-from-paumanok'),
    'III': ('Song of Myself', 'song-of-myself'),
    'IV': ('Children of Adam', 'children-of-adam'),
    'V': ('Calamus', 'calamus'),
    'VI': ('Salut au Monde!', 'salut-au-monde'),
    'VII': ('Song of the Open Road', 'song-of-the-open-road'),
    'VIII': ('Crossing Brooklyn Ferry', 'crossing-brooklyn-ferry'),
    'IX': ('Song of the Answerer', 'song-of-the-answerer'),
    'X': ('Our Old Feuillage', 'our-old-feuillage'),
    'XI': ('A Song of Joys', 'a-song-of-joys'),
    'XII': ('Song of the Broad-Axe', 'song-of-the-broad-axe'),
    'XIII': ('Song of the Exposition', 'song-of-the-exposition'),
    'XIV': ('Song of the Redwood-Tree', 'song-of-the-redwood-tree'),
    'XV': ('A Song for Occupations', 'a-song-for-occupations'),
    'XVI': ('A Song of the Rolling Earth', 'a-song-of-the-rolling-earth'),
    'XVII': ('Birds of Passage', 'birds-of-passage'),
    'XVIII': ('A Broadway Pageant', 'a-broadway-pageant'),
    'XIX': ('Sea-Drift', 'sea-drift'),
    'XX': ('By the Roadside', 'by-the-roadside'),
    'XXI': ('Drum-Taps', 'drum-taps'),
    'XXII': ('Memories of President Lincoln', 'memories-of-president-lincoln'),
    'XXIII': ('By Blue Ontario\'s Shore', 'by-blue-ontarios-shore'),
    'XXIV': ('Autumn Rivulets', 'autumn-rivulets'),
    'XXV': ('Proud Music of the Storm', 'proud-music-of-the-storm'),
    'XXVI': ('Passage to India', 'passage-to-india'),
    'XXVII': ('Prayer of Columbus', 'prayer-of-columbus'),
    'XXVIII': ('The Sleepers', 'the-sleepers'),
    'XXIX': ('To Think of Time', 'to-think-of-time'),
    'XXX': ('Whispers of Heavenly Death', 'whispers-of-heavenly-death'),
    'XXXI': ('Thou Mother with Thy Equal Brood', 'thou-mother-with-thy-equal-brood'),
    'XXXII': ('From Noon to Starry Night', 'from-noon-to-starry-night'),
    'XXXIII': ('Songs of Parting', 'songs-of-parting'),
    'XXXIV': ('Sands at Seventy', 'sands-at-seventy'),
    'XXXV': ('Good-Bye My Fancy', 'good-bye-my-fancy'),
}


# Thematic groupings that cross book boundaries
THEMATIC_GROUPS = {
    'theme-self-identity': {
        'name': 'The Self and Identity',
        'about': 'Poems exploring the nature of selfhood, individuality, and the vast multitudes contained within a single person. Whitman\'s radical project of self-celebration as a path to universal understanding.',
        'for_readers': 'Begin with "Song of Myself" and "One\'s-Self I Sing" to encounter Whitman\'s revolutionary vision of the self as both singular and cosmic. These poems invite you to discover your own multitudes.',
        'keywords': ['identity', 'soul', 'transcendence', 'body'],
    },
    'theme-democracy-america': {
        'name': 'Democracy and America',
        'about': 'Whitman\'s vision of America as a living poem — its workers, cities, landscapes, and democratic ideals. These poems celebrate the promise and struggle of the democratic experiment.',
        'for_readers': 'Read these poems as a vision of what democracy could be — not a political system but a way of being together. Whitman sees every worker, every city street, every open road as sacred democratic ground.',
        'keywords': ['democracy', 'america', 'freedom', 'labor'],
    },
    'theme-body-sexuality': {
        'name': 'The Body Electric',
        'about': 'Whitman\'s bold, boundary-breaking poems celebrating the human body, physical love, and sexuality. The Children of Adam and Calamus clusters form the core, but bodily celebration runs throughout.',
        'for_readers': 'These poems were scandalous in their time for celebrating the body as sacred. Read them as an invitation to honor your own physicality without shame.',
        'keywords': ['body', 'love', 'comradeship'],
    },
    'theme-nature-cosmos': {
        'name': 'Nature and the Cosmos',
        'about': 'Poems that find the divine in grass, sea, stars, and the rolling earth. Whitman\'s nature is never merely scenery — it is a living presence that mirrors and contains human consciousness.',
        'for_readers': 'Let these poems slow you down. Whitman asks you to really see the grass beneath your feet, the sea before you, the stars above. Each natural image opens into infinity.',
        'keywords': ['nature', 'sea', 'transcendence', 'spirituality'],
    },
    'theme-war-death': {
        'name': 'War, Death, and Mourning',
        'about': 'From the Civil War poems of Drum-Taps to the great Lincoln elegies to the late meditations on mortality, these poems confront death with unflinching tenderness.',
        'for_readers': 'Whitman served as a wound-dresser in Civil War hospitals. These poems carry that direct witness. They do not glorify war but honor the dead and dying with radical compassion.',
        'keywords': ['war', 'death', 'memory', 'love'],
    },
    'theme-comradeship-love': {
        'name': 'Comradeship and Adhesiveness',
        'about': 'Whitman\'s poems of "manly love" and deep friendship — the Calamus cluster and related poems celebrating bonds between men, the love of comrades, and democratic fellowship.',
        'for_readers': 'The Calamus poems are among the most openly homoerotic literature of the 19th century. Read them as expressions of love in its fullest sense — personal, political, and spiritual.',
        'keywords': ['comradeship', 'love', 'democracy'],
    },
    'theme-old-age-farewell': {
        'name': 'Old Age and Farewell',
        'about': 'The late poems of Sands at Seventy and Good-Bye My Fancy — Whitman in his final years, looking back with gratitude and forward with curiosity. These poems have the transparency of late autumn light.',
        'for_readers': 'These are poems written by someone who knows they are near the end. They carry a unique wisdom — neither resigned nor afraid, but luminous with acceptance.',
        'keywords': ['old-age', 'death', 'memory', 'spirituality'],
    },
    'theme-sea-voyaging': {
        'name': 'The Sea and Voyaging',
        'about': 'The sea as Whitman\'s great metaphor — for death, for the unconscious, for the passage between worlds. The Sea-Drift cluster contains some of his finest lyric poetry.',
        'for_readers': 'Whitman\'s sea poems reach for the oceanic feeling — that dissolution of boundaries between self and world. "Out of the Cradle Endlessly Rocking" is one of the great American poems.',
        'keywords': ['sea', 'death', 'music', 'nature'],
    },
}

# Map poem IDs to thematic groups (will be populated during parsing)
# Key poems for each theme:
THEME_POEM_PATTERNS = {
    'theme-self-identity': [
        'ones-self-i-sing', 'song-of-myself', 'me-imperturbe', 'i-sing-the-body-electric',
        'starting-from-paumanok', 'to-you', 'as-i-ponderd-in-silence',
        'beginning-my-studies', 'eidolons',
    ],
    'theme-democracy-america': [
        'for-you-o-democracy', 'i-hear-america-singing', 'to-a-historian',
        'to-thee-old-cause', 'to-the-states', 'by-blue-ontarios-shore',
        'song-of-the-broad-axe', 'song-of-the-exposition',
        'a-song-for-occupations', 'a-broadway-pageant',
        'thou-mother-with-thy-equal-brood', 'our-old-feuillage',
    ],
    'theme-body-sexuality': [
        'to-the-garden-the-world', 'from-pent-up-aching-rivers',
        'i-sing-the-body-electric', 'a-woman-waits-for-me',
        'spontaneous-me', 'one-hour-to-madness-and-joy',
        'native-moments', 'o-hymen-o-hymenee',
    ],
    'theme-nature-cosmos': [
        'song-of-the-redwood-tree', 'a-song-of-the-rolling-earth',
        'crossing-brooklyn-ferry', 'salut-au-monde',
        'this-compost', 'on-the-beach-at-night',
        'on-the-beach-at-night-alone', 'the-world-below-the-brine',
        'passage-to-india', 'unseen-buds',
    ],
    'theme-war-death': [
        'beat-beat-drums', 'come-up-from-the-fields-father',
        'vigil-strange-i-kept-on-the-field-one-night',
        'a-sight-in-camp-in-the-daybreak',
        'the-wound-dresser', 'reconciliation',
        'when-lilacs-last-in-the-dooryard',
        'o-captain-my-captain', 'to-think-of-time',
    ],
    'theme-comradeship-love': [
        'in-paths-untrodden', 'scented-herbage-of-my-breast',
        'whoever-you-are-holding-me-now-in-hand',
        'i-saw-in-louisiana-a-live-oak-growing',
        'city-of-orgies', 'we-two-boys-together-clinging',
        'when-i-heard-at-the-close-of-the-day',
        'a-glimpse', 'fast-anchord-eternal-o-love',
    ],
    'theme-old-age-farewell': [
        'mannahatta', 'paumanok', 'to-those-whove-faild',
        'after-the-supper-and-talk', 'good-bye-my-fancy',
        'sail-out-for-good-eidolon-yacht', 'the-unexpressd',
        'grand-is-the-seen', 'good-bye-my-fancy-1',
        'l-of-gs-purport', 'old-ages-lambent-peaks',
    ],
    'theme-sea-voyaging': [
        'in-cabind-ships-at-sea', 'out-of-the-cradle-endlessly',
        'as-i-ebbd-with-the-ocean-of-life',
        'on-the-beach-at-night', 'the-world-below-the-brine',
        'in-cabind-ships-at-sea', 'passage-to-india',
        'prayer-of-columbus', 'the-ship-starting',
        'sail-out-for-good-eidolon-yacht',
    ],
}


def generate_reflection(title, text_snippet):
    """Generate a brief reflection/prompt for each poem."""
    reflections = {
        'song-of-myself': 'What multitudes do you contain? Whitman invites you to celebrate the contradictions within yourself — not as flaws, but as the very texture of being alive.',
        'ones-self-i-sing': 'How do you hold both your individuality and your connection to the mass of humanity? Whitman begins his life\'s work with this paradox.',
        'i-hear-america-singing': 'What is your song? Whitman hears the unique melody each worker brings to the day. What does your daily labor sing?',
        'o-captain-my-captain': 'How do we mourn a leader who gave everything? This poem captures the terrible gap between victory and loss.',
        'crossing-brooklyn-ferry': 'Whitman speaks directly to you across time. Can you feel the connection he insists is real — between his moment and yours?',
        'out-of-the-cradle-endlessly': 'When did you first learn the word that the sea whispers — the word that is both loss and the beginning of poetry?',
        'the-wound-dresser': 'What wounds have you tended? Whitman discovered that the deepest service is presence — simply being with those who suffer.',
        'when-lilacs-last-in-the-dooryard': 'How do we transform grief into something that blooms? Whitman\'s great elegy finds consolation not in answers but in the persistence of spring.',
        'passage-to-india': 'What passage are you making? Whitman sees all human exploration — geographic, scientific, spiritual — as one great voyage toward the soul.',
        'i-sing-the-body-electric': 'Do you honor your body as sacred? Whitman insists that flesh is as worthy of celebration as spirit.',
    }

    poem_id = make_id(title)
    if poem_id in reflections:
        return reflections[poem_id]

    # Generate generic but meaningful reflection
    return f'Sit with this poem and let its rhythms work on you. Whitman wrote for the open air — try reading it aloud.'


def build_grammar():
    """Main function to build the Leaves of Grass grammar."""

    # Read and clean source text
    raw_text = SEED_FILE.read_text(encoding='utf-8')
    text = strip_gutenberg(raw_text)

    # Remove the title page (before first BOOK)
    book_start = text.find('BOOK ')
    if book_start > 0:
        # Keep the epigraph
        epigraph_text = text[:book_start].strip()
        text = text[book_start:]

    # Parse into books
    books = parse_books(text)

    items = []
    sort_order = 0
    book_l2_items = []  # Track L2 book items
    all_poem_ids_by_book = {}  # book_roman -> [poem_ids]
    id_counts = {}  # Track duplicate IDs

    for book in books:
        roman = book['roman']
        cluster_name, category_slug = BOOK_CLUSTERS.get(roman, (f'Book {roman}', f'book-{roman.lower()}'))

        # Parse poems from this book
        poems = parse_poems_from_book(book['text'])

        if not poems:
            continue

        poem_ids = []

        for title, poem_text in poems:
            poem_text = clean_poem_text(poem_text)
            if not poem_text.strip():
                continue

            poem_id = make_id(title)

            # Handle duplicate IDs
            if poem_id in id_counts:
                id_counts[poem_id] += 1
                poem_id = f"{poem_id}-{id_counts[poem_id]}"
            else:
                id_counts[poem_id] = 0

            keywords = generate_keywords(title, poem_text)
            reflection = generate_reflection(title, poem_text[:500])

            # Determine sections
            sections = {
                'Poem': poem_text,
            }

            # Add reflection
            sections['Reflection'] = reflection

            item = {
                'id': poem_id,
                'name': title,
                'sort_order': sort_order,
                'level': 1,
                'category': category_slug,
                'sections': sections,
                'keywords': keywords if keywords else ['poetry', 'whitman'],
                'metadata': {
                    'book': f'Book {roman}',
                    'cluster': cluster_name,
                    'source': 'Leaves of Grass, Walt Whitman, 1891-92 deathbed edition'
                }
            }

            items.append(item)
            poem_ids.append(poem_id)
            sort_order += 1

        all_poem_ids_by_book[roman] = poem_ids

    # Build L2 items: Book/Cluster groupings
    l2_start = sort_order

    # Book descriptions for L2
    book_descriptions = {
        'I': 'The opening cluster of Leaves of Grass — short lyric poems that announce Whitman\'s themes: the self, democracy, the body, the soul, and the poetic vocation.',
        'II': 'A sweeping overture to the entire collection. Whitman declares his origins, his ambitions, and his vision of poetry as the voice of democratic America.',
        'III': 'Whitman\'s masterwork — a vast, ecstatic poem that contains multitudes. The self expands to encompass all of America, all of nature, all of human experience.',
        'IV': 'Poems celebrating sexuality, the body, and procreative love. These poems scandalized Whitman\'s contemporaries and remain among his most daring work.',
        'V': 'Poems of "adhesiveness" — the love between men, comradeship, and democratic fellowship. The calamus plant, with its aromatic root, symbolizes this hidden, powerful love.',
        'VI': 'A great catalog poem greeting the entire world — every nation, every people, every landscape. Whitman\'s vision is radically inclusive.',
        'VII': 'One of Whitman\'s most beloved poems — a hymn to freedom, movement, and the open possibilities of life on the road.',
        'VIII': 'A meditation on time, connection, and the ferry crossing between Brooklyn and Manhattan. Whitman speaks directly to future readers across the centuries.',
        'IX': 'A poem about the role of the poet as answerer — the one who resolves, reconciles, and gives voice to what others cannot say.',
        'X': 'A panoramic catalog of American scenes, landscapes, and people from every region of the country.',
        'XI': 'A celebration of joy in all its forms — physical, spiritual, creative, natural. Each stanza opens a new dimension of delight.',
        'XII': 'The broad-axe as symbol of American building, clearing, and creating. From frontier labor to the shaping of cities and civilizations.',
        'XIII': 'A poem written for the American Industrial Exhibition — celebrating workers, builders, and the dignity of practical labor.',
        'XIV': 'The redwood tree as voice of nature yielding to human civilization — a complex poem about progress and loss.',
        'XV': 'A celebration of work and workers — every trade, every craft, every daily labor honored as part of the democratic whole.',
        'XVI': 'The earth itself as poem and teacher. Whitman finds language, meaning, and spiritual instruction in the physical world.',
        'XVII': 'A cluster of poems on migration, movement, and the passage of peoples across history and geography.',
        'XVIII': 'A poem written for the 1860 arrival of Japanese ambassadors in New York — celebrating the meeting of East and West.',
        'XIX': 'Poems of the sea — among Whitman\'s finest lyric work. The ocean as metaphor for the unconscious, for death, and for the origins of poetry.',
        'XX': 'Short poems and observations from life\'s journey — glimpses, encounters, and moments of recognition along the way.',
        'XXI': 'Civil War poems written from direct experience. Whitman served as a wound-dresser in Washington hospitals, and these poems carry that witness.',
        'XXII': 'The great Lincoln elegies — including "When Lilacs Last in the Dooryard Bloom\'d" and "O Captain! My Captain!" Whitman\'s response to the assassination.',
        'XXIII': 'A long poem on the American democratic vision, written after the Civil War. Whitman reclaims his faith in the country\'s possibility.',
        'XXIV': 'A diverse cluster of poems on many themes — nature, memory, spirituality, and the flow of life. The "rivulets" metaphor suggests many streams feeding one river.',
        'XXV': 'A dream-poem of all the world\'s music converging into one great symphony — opera, folk song, nature, and the music of the spheres.',
        'XXVI': 'One of Whitman\'s most ambitious late poems — celebrating the Suez Canal, the transcontinental railroad, and the spiritual journey of humanity.',
        'XXVII': 'Columbus in old age, shipwrecked and forgotten, praying to God. A poem Whitman identified with deeply in his own declining years.',
        'XXVIII': 'A visionary night-poem of dreams, wandering, and the democracy of sleep. All sleepers are equal in the dark.',
        'XXIX': 'A meditation on mortality and the meaning of time. What does it mean to really think about the fact that we will die?',
        'XXX': 'Poems approaching death with spiritual curiosity rather than fear. Death as a whisper, a passage, a continuation.',
        'XXXI': 'A poem addressing America as mother — celebrating the nation\'s diversity, unity, and future potential.',
        'XXXII': 'A varied cluster of later poems — some visionary, some personal, ranging from noon brightness to night contemplation.',
        'XXXIII': 'Farewell poems — Whitman preparing to take leave. Not mournful but luminous, turning departure into continuation.',
        'XXXIV': 'Late poems written in Whitman\'s seventies — shorter, more crystalline, with the clarity of someone who has lived fully and faces the end openly.',
        'XXXV': 'The final annex — Whitman\'s very last poems, written as he prepared for death. A poet saying good-bye to fancy, to the world, to the reader.',
    }

    for roman, poem_ids in all_poem_ids_by_book.items():
        if not poem_ids:
            continue

        cluster_name, category_slug = BOOK_CLUSTERS.get(roman, (f'Book {roman}', f'book-{roman.lower()}'))
        book_num = roman_to_int(roman)
        l2_id = f'cluster-{category_slug}'

        description = book_descriptions.get(roman, f'Book {roman} of Leaves of Grass.')

        l2_item = {
            'id': l2_id,
            'name': f'{cluster_name}',
            'sort_order': sort_order,
            'level': 2,
            'category': 'book-clusters',
            'composite_of': poem_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': description,
                'For Readers': f'This cluster contains {len(poem_ids)} poem{"s" if len(poem_ids) != 1 else ""}. ' +
                    (f'Start with "{poems[0][0]}" and let the sequence carry you.' if poem_ids else ''),
            },
            'keywords': ['whitman', 'poetry', 'leaves-of-grass'],
            'metadata': {
                'book_number': book_num,
                'source': 'Leaves of Grass, Walt Whitman, 1891-92 deathbed edition'
            }
        }

        book_l2_items.append(l2_item)
        items.append(l2_item)
        sort_order += 1

    # Build L2 items: Thematic groupings
    all_item_ids = {item['id'] for item in items if item['level'] == 1}
    thematic_l2_ids = []

    for theme_id, theme_info in THEMATIC_GROUPS.items():
        # Find matching poem IDs from patterns
        pattern_ids = THEME_POEM_PATTERNS.get(theme_id, [])
        matched_ids = []
        for pid in pattern_ids:
            # Try exact match first
            if pid in all_item_ids:
                matched_ids.append(pid)
            else:
                # Try partial match
                for real_id in all_item_ids:
                    if real_id.startswith(pid) or pid.startswith(real_id):
                        matched_ids.append(real_id)
                        break

        # Also scan all poems for keyword matches
        for item in items:
            if item['level'] != 1:
                continue
            item_keywords = item.get('keywords', [])
            theme_keywords = theme_info.get('keywords', [])
            if any(k in item_keywords for k in theme_keywords):
                if item['id'] not in matched_ids:
                    matched_ids.append(item['id'])

        # Deduplicate while preserving order
        seen = set()
        unique_ids = []
        for mid in matched_ids:
            if mid not in seen:
                seen.add(mid)
                unique_ids.append(mid)
        matched_ids = unique_ids

        if not matched_ids:
            continue

        l2_item = {
            'id': theme_id,
            'name': theme_info['name'],
            'sort_order': sort_order,
            'level': 2,
            'category': 'thematic-groups',
            'composite_of': matched_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': theme_info['about'],
                'For Readers': theme_info['for_readers'],
            },
            'keywords': theme_info.get('keywords', []),
            'metadata': {
                'grouping': 'thematic',
                'source': 'Leaves of Grass, Walt Whitman, 1891-92 deathbed edition'
            }
        }

        items.append(l2_item)
        thematic_l2_ids.append(theme_id)
        sort_order += 1

    # Build L3 meta-categories
    book_cluster_ids = [item['id'] for item in book_l2_items]

    l3_items = [
        {
            'id': 'meta-whitman-architecture',
            'name': 'Whitman\'s Architecture: The Books of Leaves of Grass',
            'sort_order': sort_order,
            'level': 3,
            'category': 'meta-categories',
            'composite_of': book_cluster_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': 'The 35 books of Leaves of Grass as Whitman arranged them in his final "deathbed" edition of 1891-92. This structure represents his life\'s work in its definitive form — from the opening Inscriptions through the great central poems to the late annexes. The architecture is both chronological (early, middle, late work) and thematic (the self, love, war, death, farewell).',
                'For Readers': 'Follow Whitman\'s own path through the collection. He spent decades arranging and rearranging these poems. The sequence matters — it\'s a journey from the first announcement of self to the final farewell.',
            },
            'keywords': ['poetry', 'whitman', 'structure'],
            'metadata': {}
        },
        {
            'id': 'meta-thematic-currents',
            'name': 'Thematic Currents: The Great Themes of Whitman',
            'sort_order': sort_order + 1,
            'level': 3,
            'category': 'meta-categories',
            'composite_of': thematic_l2_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': 'The great themes that flow through Leaves of Grass, cutting across the book structure. These thematic groupings reveal how Whitman returns again and again to his core preoccupations: the self, democracy, the body, nature, war, death, comradeship, and the sea. A single poem may belong to several currents.',
                'For Readers': 'Use these thematic groupings to explore Whitman by mood and interest rather than by sequence. If you\'re drawn to the sea, start there. If you\'re thinking about mortality, follow that thread. Whitman wrote for browsers as much as for sequential readers.',
            },
            'keywords': ['poetry', 'whitman', 'themes'],
            'metadata': {}
        },
    ]

    items.extend(l3_items)

    # Build the full grammar
    grammar = {
        '_grammar_commons': {
            'schema_version': '1.0',
            'license': 'CC-BY-SA-4.0',
            'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/',
            'attribution': [
                {
                    'name': 'Walt Whitman',
                    'date': '1891',
                    'note': 'Author of Leaves of Grass (1855-1891). This is the "deathbed" edition of 1891-92.'
                },
                {
                    'name': 'Project Gutenberg',
                    'date': '1998',
                    'note': 'Digital text from Project Gutenberg eBook #1322, credited to G. Fuhrman and David Widger.'
                },
                {
                    'name': 'PlayfulProcess',
                    'date': '2026-03-04',
                    'note': 'Grammar structure, thematic groupings, and reflections.'
                }
            ]
        },
        'name': 'Leaves of Grass',
        'description': (
            'Walt Whitman\'s Leaves of Grass — the complete "deathbed" edition of 1891-92, '
            'containing nearly 400 poems spanning four decades of work. From the cosmic '
            'ecstasy of "Song of Myself" to the Civil War witness of "Drum-Taps" to the '
            'luminous late poems of "Sands at Seventy," this is the foundational text of '
            'American poetry and one of the great sacred books of democratic civilization. '
            'Source: Project Gutenberg eBook #1322 (https://www.gutenberg.org/ebooks/1322).'
            '\n\n'
            'PUBLIC DOMAIN ILLUSTRATION REFERENCES: Thomas Eakins\' 1887 portrait of Whitman '
            '(oil on canvas, Pennsylvania Academy of Fine Arts) — intimate, luminous portrait '
            'of the poet in old age. Samuel Hollyer\'s 1855 engraving of Whitman (frontispiece '
            'to the first edition) — the young Whitman in workman\'s clothes, hat cocked. '
            'George C. Cox\'s 1887 photographs of Whitman — multiple poses showing the '
            '"Good Gray Poet" in his Camden years. Frederick Gutekunst\'s 1889 photograph — '
            'the iconic white-bearded profile.'
        ),
        'grammar_type': 'custom',
        'creator_name': 'PlayfulProcess',
        'creator_link': 'https://lifeisprocess.substack.com/',
        'tags': [
            'poetry', 'american-literature', 'democracy', 'transcendentalism',
            'nature', 'war', 'love', 'body', 'soul', 'death', 'civil-war',
            'spirituality', 'identity', 'public-domain', 'oracle'
        ],
        'roots': ['transcendentalism', 'democratic-thought', 'mysticism'],
        'shelves': ['wisdom', 'mirror'],
        'lineages': ['Shrei', 'Akomolafe', 'Kelty'],
        'worldview': 'non-dual',
        'cover_image_url': '',
        'items': items,
    }

    return grammar


def main():
    print("Building Leaves of Grass grammar...")
    grammar = build_grammar()

    # Count levels
    l1 = sum(1 for item in grammar['items'] if item['level'] == 1)
    l2 = sum(1 for item in grammar['items'] if item['level'] == 2)
    l3 = sum(1 for item in grammar['items'] if item['level'] == 3)

    print(f"  L1 poems: {l1}")
    print(f"  L2 groupings: {l2}")
    print(f"  L3 meta-categories: {l3}")
    print(f"  Total items: {len(grammar['items'])}")

    # Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"  Written to: {OUTPUT_FILE}")

    # Quick validation
    ids = [item['id'] for item in grammar['items']]
    id_set = set(ids)
    dupes = [x for x in ids if ids.count(x) > 1]
    if dupes:
        print(f"  WARNING: Duplicate IDs: {set(dupes)}")

    # Check composite_of references
    bad_refs = []
    for item in grammar['items']:
        for ref in item.get('composite_of', []):
            if ref not in id_set:
                bad_refs.append((item['id'], ref))
    if bad_refs:
        print(f"  WARNING: Bad composite_of references:")
        for item_id, ref in bad_refs[:10]:
            print(f"    {item_id} -> {ref}")
    else:
        print("  All composite_of references valid.")


if __name__ == '__main__':
    main()
