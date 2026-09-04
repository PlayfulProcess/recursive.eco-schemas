#!/usr/bin/env python3
"""
Build grammar.json for Thus Spoke Zarathustra from the Project Gutenberg seed text.

Source: Project Gutenberg eBook #1998
Author: Friedrich Nietzsche
Translator: Thomas Common

Structure:
- L1: Individual speeches/chapters (Prologue + 80 numbered chapters)
- L2: Parts (First through Fourth) + Thematic groupings
- L3: Meta-categories (The Four Parts, Thematic Arcs)
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "thus-spoke-zarathustra.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "thus-spoke-zarathustra"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"


def read_seed():
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        start_idx = text.index("\n", start_idx) + 1
    else:
        start_idx = 0
    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = len(text)
    return text[start_idx:end_idx]


def strip_introduction_and_appendix(text):
    """Remove Mrs Forster-Nietzsche's introduction and Ludovici's appendix notes.
    Keep only the primary text of Zarathustra."""

    # Find start of actual text: "FIRST PART. ZARATHUSTRA'S DISCOURSES."
    # But the Prologue comes before the numbered chapters, right after the intro
    # The intro starts at "INTRODUCTION BY MRS FORSTER-NIETZSCHE."
    # The actual text starts at "FIRST PART. ZARATHUSTRA'S DISCOURSES."
    first_part_match = re.search(r'^FIRST PART\.\s+ZARATHUSTRA.S DISCOURSES\.', text, re.MULTILINE)
    if first_part_match:
        text_start = first_part_match.start()
    else:
        text_start = 0

    # Find end: APPENDIX.
    appendix_match = re.search(r'^APPENDIX\.$', text, re.MULTILINE)
    if appendix_match:
        text_end = appendix_match.start()
    else:
        text_end = len(text)

    return text[text_start:text_end].strip()


def parse_chapters(text):
    """Parse the text into chapters/speeches.

    The text has:
    - ZARATHUSTRA'S PROLOGUE (before numbered chapters)
    - Numbered chapters: I. THE THREE METAMORPHOSES through LXXX. THE SIGN
    - Part markers: FIRST PART, SECOND PART (implicit), THIRD PART, FOURTH AND LAST PART
    """

    # Define the chapter pattern: Roman numeral followed by title
    # Also capture the Prologue
    chapter_pattern = re.compile(
        r'^(ZARATHUSTRA.S PROLOGUE\.|([IVXLC]+)\.\s+(.+?)\.)$',
        re.MULTILINE
    )

    chapters = []
    matches = list(chapter_pattern.finditer(text))

    for i, match in enumerate(matches):
        full_heading = match.group(0).strip().rstrip('.')
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        # Extract chapter text
        chapter_text = text[start:end].strip()

        # Clean up: remove part headers and epigraphs between chapters
        # Part headers like "THIRD PART." or "FOURTH AND LAST PART." and
        # their epigraphs appear between chapters
        part_header_pattern = re.compile(
            r'(SECOND PART\.|THIRD PART\.|FOURTH AND LAST PART\.)\s*\n.*?(?=\n[A-Z])',
            re.DOTALL
        )

        # Remove trailing part headers/epigraphs from chapter text
        # These appear at the end of the last chapter in each part
        for part_name in [
            'FIRST PART. ZARATHUSTRA\'S DISCOURSES.',
            'SECOND PART.',
            'THIRD PART.',
            'FOURTH AND LAST PART.'
        ]:
            idx = chapter_text.find(part_name)
            if idx != -1:
                chapter_text = chapter_text[:idx].strip()

        # Also remove trailing epigraphs (quotes from Zarathustra that precede new parts)
        # These typically start with a quote and end with "—ZARATHUSTRA, ..."
        epigraph_pattern = re.compile(
            r'\n\n+"[^"]*?"\s*\n\n*.*?—ZARATHUSTRA.*$',
            re.DOTALL
        )
        # Only strip trailing epigraphs (those at the very end)
        chapter_text_stripped = re.sub(
            r'\n\n\n+"[^"]*?"[^"]*?—ZARATHUSTRA[^"]*?$',
            '',
            chapter_text,
            flags=re.DOTALL
        )
        # But make sure we didn't lose too much
        if len(chapter_text_stripped) > len(chapter_text) * 0.5:
            chapter_text = chapter_text_stripped.strip()

        if match.group(0).startswith('ZARATHUSTRA'):
            roman = None
            title = "Zarathustra's Prologue"
        else:
            roman = match.group(2)
            title = match.group(3).strip()
            # Title case it
            title = title_case(title)

        chapters.append({
            'roman': roman,
            'title': title,
            'text': chapter_text,
            'full_heading': full_heading,
        })

    return chapters


def title_case(s):
    """Convert ALL CAPS title to title case."""
    # Handle special words
    small_words = {'the', 'of', 'and', 'in', 'on', 'at', 'to', 'a', 'an', 'with', 'for'}
    words = s.lower().split()
    result = []
    for i, w in enumerate(words):
        if w == '-':
            result.append('-')
        elif '-' in w:
            # Handle hyphenated words
            parts = w.split('-')
            result.append('-'.join(p.capitalize() for p in parts))
        elif i == 0 or w not in small_words:
            result.append(w.capitalize())
        else:
            result.append(w)
    return ' '.join(result)


def roman_to_int(roman):
    """Convert Roman numeral to integer."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    prev = 0
    for ch in reversed(roman):
        val = values.get(ch, 0)
        if val < prev:
            result -= val
        else:
            result += val
        prev = val
    return result


def make_id(title, roman=None):
    """Create a hyphenated ID from title."""
    # Clean the title
    clean = title.lower()
    clean = re.sub(r'[^a-z0-9\s-]', '', clean)
    clean = re.sub(r'\s+', '-', clean.strip())
    clean = re.sub(r'-+', '-', clean)
    return clean


def assign_part(roman, title):
    """Determine which part a chapter belongs to based on its Roman numeral."""
    if roman is None:
        return 'first-part'  # Prologue

    num = roman_to_int(roman)
    if num <= 22:
        return 'first-part'
    elif num <= 44:
        return 'second-part'
    elif num <= 60:
        return 'third-part'
    else:
        return 'fourth-part'


def assign_thematic_group(chapter_id, title, part):
    """Assign chapters to thematic groups for L2 emergence."""
    # Define thematic groups
    themes = {
        'self-overcoming': {
            'ids': [
                'the-three-metamorphoses', 'self-surpassing', 'the-way-of-the-creating-one',
                'the-bestowing-virtue', 'the-convalescent', 'the-higher-man',
                'the-spirit-of-gravity', 'old-and-new-tables',
            ],
            'name': 'Self-Overcoming and Transformation',
            'about': 'Nietzsche\'s central teaching: the human being as something to be surpassed. These speeches trace the arc from camel to lion to child — from bearing burdens to destroying old values to creating new ones.',
        },
        'critique-of-society': {
            'ids': [
                'the-new-idol', 'the-flies-in-the-market-place', 'the-tarantulas',
                'the-famous-wise-ones', 'scholars', 'the-land-of-culture',
                'the-rabble', 'the-apostates', 'the-preachers-of-death',
                'the-academic-chairs-of-virtue',
            ],
            'name': 'Critique of Society and Culture',
            'about': 'Zarathustra\'s fierce critique of the state, the marketplace, scholars, and all forms of cultural mediocrity. The tarantulas of equality, the new idol of the state, and the flies of the marketplace represent everything that suppresses the creative individual.',
        },
        'eternal-recurrence': {
            'ids': [
                'the-vision-and-the-enigma', 'the-convalescent', 'the-seven-seals',
                'the-second-dance-song', 'the-drunken-song', 'before-sunrise',
                'the-stillest-hour', 'noon-tide',
            ],
            'name': 'Eternal Recurrence and Amor Fati',
            'about': 'The most abysmal thought: that everything returns eternally. These speeches chart Zarathustra\'s confrontation with this idea — from the vision of the gateway to the midnight bell\'s twelve strokes to his final Yes-saying.',
        },
        'body-and-earth': {
            'ids': [
                'the-despisers-of-the-body', 'backworldsmen', 'on-the-olive-mount',
                'joys-and-passions', 'chastity', 'child-and-marriage',
                'the-three-evil-things', 'immaculate-perception',
            ],
            'name': 'Body, Earth, and the Senses',
            'about': 'Against the despisers of the body and the "backworldsmen" who posit another world beyond this one. Zarathustra calls humanity back to the earth, to the body as "a great reason," to sensuality and passion as holy.',
        },
        'solitude-and-return': {
            'ids': [
                'zarathustras-prologue', 'the-child-with-the-mirror', 'the-wanderer',
                'involuntary-bliss', 'the-return-home', 'the-great-longing',
                'the-honey-sacrifice', 'the-sign',
            ],
            'name': 'Solitude and Return',
            'about': 'Zarathustra\'s recurring rhythm: descent from the mountain, teaching among humans, retreat back to solitude. Each cycle deepens his wisdom and transforms his message. The tension between the need for solitude and the overflowing need to give shapes the entire work.',
        },
        'companions-and-encounters': {
            'ids': [
                'the-tree-on-the-hill', 'the-friend', 'old-and-young-women',
                'the-bite-of-the-adder', 'the-pale-criminal', 'the-pitiful',
                'the-cry-of-distress', 'talk-with-the-kings', 'the-leech',
                'the-magician', 'the-ugliest-man', 'the-voluntary-beggar',
                'the-shadow', 'the-greeting',
            ],
            'name': 'Companions and Encounters',
            'about': 'Zarathustra\'s meetings with various figures — the young man on the hill, the friend, the kings, the leech, the magician, the ugliest man. Each encounter tests and refines his teaching. In Part Four, these "higher men" gather in his cave for the final drama.',
        },
        'will-to-power': {
            'ids': [
                'war-and-warriors', 'the-thousand-and-one-goals', 'neighbour-love',
                'voluntary-death', 'the-virtuous', 'the-priests',
                'redemption', 'manly-prudence', 'the-bedwarfing-virtue',
                'on-passing-by',
            ],
            'name': 'Will, Power, and Values',
            'about': 'The revaluation of all values. Zarathustra challenges conventional morality — neighbour-love, priestly virtue, pity — and calls for a new table of values rooted in life-affirmation, strength, and creative power.',
        },
        'art-and-song': {
            'ids': [
                'reading-and-writing', 'the-night-song', 'the-dance-song',
                'the-grave-song', 'the-sublime-ones', 'poets',
                'great-events', 'the-soothsayer', 'the-song-of-melancholy',
                'science', 'among-daughters-of-the-desert', 'the-awakening',
                'the-ass-festival', 'the-supper', 'out-of-service',
            ],
            'name': 'Art, Song, and Celebration',
            'about': 'Zarathustra as poet, dancer, and singer. The night-song, dance-song, and grave-song are among the most lyrical passages in philosophy. Part Four culminates in festival, music, and the drunken song\'s midnight affirmation.',
        },
    }

    for theme_key, theme_data in themes.items():
        if chapter_id in theme_data['ids']:
            return theme_key

    return None


def extract_keywords(text, title):
    """Extract keywords from chapter text and title."""
    # Thematic keyword mapping based on title words and content
    keyword_map = {
        'metamorphos': ['transformation', 'spirit', 'camel', 'lion', 'child'],
        'virtue': ['virtue', 'morality', 'giving', 'power'],
        'backworld': ['otherworldly', 'denial', 'body', 'earth'],
        'body': ['body', 'self', 'reason', 'senses'],
        'passion': ['passion', 'desire', 'virtue'],
        'criminal': ['crime', 'guilt', 'punishment', 'madness'],
        'reading': ['writing', 'blood', 'wisdom', 'lightness'],
        'tree': ['youth', 'loneliness', 'growth'],
        'death': ['death', 'meaning', 'life-denial'],
        'war': ['war', 'courage', 'enemy', 'struggle'],
        'idol': ['state', 'power', 'destruction', 'freedom'],
        'flies': ['marketplace', 'fame', 'solitude', 'crowd'],
        'chastity': ['chastity', 'desire', 'virtue', 'innocence'],
        'friend': ['friendship', 'enemy', 'love', 'war'],
        'goal': ['values', 'peoples', 'creation', 'good-and-evil'],
        'neighbour': ['love', 'self', 'distance', 'future'],
        'creating': ['creation', 'solitude', 'freedom', 'suffering'],
        'women': ['woman', 'man', 'love', 'pregnancy'],
        'adder': ['revenge', 'forgiveness', 'justice'],
        'marriage': ['marriage', 'children', 'future', 'love'],
        'voluntary death': ['death', 'timing', 'meaning', 'legacy'],
        'bestow': ['virtue', 'giving', 'gold', 'power'],
        'mirror': ['return', 'teaching', 'enemies'],
        'happy isle': ['creation', 'will', 'becoming', 'gods'],
        'pitiful': ['pity', 'suffering', 'weakness', 'strength'],
        'priest': ['religion', 'god', 'suffering', 'redemption'],
        'virtuous': ['virtue', 'revenge', 'punishment', 'morality'],
        'rabble': ['disgust', 'height', 'purity', 'nausea'],
        'tarantula': ['equality', 'revenge', 'justice', 'power'],
        'wise': ['wisdom', 'people', 'service', 'truth'],
        'night': ['loneliness', 'light', 'giving', 'overflow'],
        'dance': ['life', 'woman', 'wisdom', 'joy'],
        'grave': ['memory', 'youth', 'will', 'resurrection'],
        'surpass': ['self-overcoming', 'life', 'power', 'obedience'],
        'sublime': ['beauty', 'stillness', 'hero', 'grace'],
        'culture': ['culture', 'masks', 'homelessness', 'history'],
        'immaculate': ['perception', 'desire', 'hypocrisy', 'moon'],
        'scholar': ['knowledge', 'independence', 'sting', 'spirit'],
        'poet': ['poetry', 'lying', 'truth', 'beauty'],
        'great event': ['fire-dog', 'revolution', 'silence', 'depth'],
        'soothsayer': ['weariness', 'nihilism', 'emptiness', 'will'],
        'redemption': ['past', 'will', 'revenge', 'creation'],
        'prudence': ['caution', 'disguise', 'lightning', 'cloud'],
        'stillest': ['silence', 'power', 'command', 'obedience'],
        'wanderer': ['wandering', 'solitude', 'height', 'abyss'],
        'vision': ['eternal-recurrence', 'gateway', 'dwarf', 'moment'],
        'involuntary': ['bliss', 'happiness', 'temptation', 'return'],
        'sunrise': ['sky', 'chance', 'freedom', 'innocence'],
        'bedwarf': ['smallness', 'virtue', 'mediocrity', 'modesty'],
        'olive': ['winter', 'solitude', 'laughter', 'wisdom'],
        'passing': ['city', 'disgust', 'fire', 'fool'],
        'apostate': ['believers', 'piety', 'regression', 'fear'],
        'return home': ['solitude', 'cave', 'silence', 'homecoming'],
        'three evil': ['sensuality', 'lust-for-power', 'selfishness'],
        'gravity': ['spirit-of-gravity', 'dancing', 'lightness', 'earth'],
        'table': ['values', 'law', 'creation', 'destruction'],
        'convalescent': ['eternal-recurrence', 'animals', 'sickness', 'recovery'],
        'great longing': ['soul', 'overflowing', 'wine', 'destiny'],
        'second dance': ['life', 'eternity', 'midnight', 'bell'],
        'seven seal': ['eternity', 'love', 'ring', 'affirmation'],
        'honey': ['sacrifice', 'bait', 'higher-men', 'descent'],
        'cry': ['pity', 'distress', 'higher-man', 'temptation'],
        'king': ['kings', 'disgust', 'mob', 'nobility'],
        'leech': ['science', 'conscience', 'brain', 'spirit'],
        'magician': ['art', 'deception', 'suffering', 'penitent'],
        'out of service': ['pope', 'god-is-dead', 'piety', 'service'],
        'ugliest': ['murder-of-god', 'pity', 'shame', 'ugliness'],
        'beggar': ['poverty', 'happiness', 'cows', 'rumination'],
        'shadow': ['wandering', 'freedom', 'homelessness', 'goal'],
        'noon': ['noon', 'stillness', 'perfection', 'eternity'],
        'greeting': ['higher-men', 'gathering', 'cave', 'waiting'],
        'supper': ['last-supper', 'feast', 'lamb', 'wine'],
        'higher man': ['higher-man', 'suffering', 'laughter', 'creation'],
        'melancholy': ['song', 'melancholy', 'desert', 'Europe'],
        'science': ['fear', 'courage', 'knowledge', 'depth'],
        'daughter': ['desert', 'oasis', 'orient', 'dance'],
        'awakening': ['ass', 'worship', 'god', 'prayer'],
        'ass-festival': ['festival', 'laughter', 'piety', 'folly'],
        'drunken': ['midnight', 'eternal-recurrence', 'joy', 'pain'],
        'sign': ['lion', 'doves', 'children', 'morning'],
        'prologue': ['descent', 'overman', 'tightrope', 'last-man'],
    }

    title_lower = title.lower()
    for key, keywords in keyword_map.items():
        if key in title_lower:
            return keywords

    # Fallback
    return ['philosophy', 'wisdom', 'transformation']


def clean_chapter_text(text):
    """Clean up chapter text - remove section numbers, normalize whitespace."""
    # Remove leading/trailing whitespace
    text = text.strip()

    # Normalize multiple blank lines to double
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


def split_numbered_sections(text):
    """Some chapters have numbered sections (1., 2., 3.). Split them."""
    stripped = text.strip()

    # Check if "1." appears on its own line (possibly after a subtitle line)
    # Find the first occurrence of "1.\n"
    match_1 = re.search(r'(?:^|\n)\s*1\.\s*\n', stripped)
    if not match_1:
        return None

    # If there's text before the "1.", treat it as a preamble
    preamble = stripped[:match_1.start()].strip()
    numbered_text = stripped[match_1.start():]

    # Split on numbered section markers (number on its own line)
    sections = re.split(r'\n\s*(?=\d+\.\s*\n)', numbered_text)
    result = []
    for sec in sections:
        # Remove the section number line
        sec = re.sub(r'^\s*\d+\.\s*\n+', '', sec).strip()
        if sec:
            result.append(sec)

    if len(result) > 1:
        # If there was a preamble, prepend it to the first section
        if preamble:
            result[0] = preamble + "\n\n" + result[0]
        return result
    return None


def build_grammar():
    raw = read_seed()
    text = strip_gutenberg(raw)
    text = strip_introduction_and_appendix(text)

    chapters = parse_chapters(text)

    # Part definitions
    parts = {
        'first-part': {
            'name': 'First Part',
            'part_label': 'Part One',
            'description': 'Zarathustra descends from his mountain solitude to teach humanity about the Overman. Through his Prologue and twenty-two discourses, he introduces his core teachings: the three metamorphoses of the spirit, fidelity to the earth, the critique of the state and marketplace, and the bestowing virtue.',
            'chapters': [],
        },
        'second-part': {
            'name': 'Second Part',
            'part_label': 'Part Two',
            'description': 'Zarathustra returns from solitude to deepen his teaching. The discourses grow more lyrical and personal — the night-song, dance-song, and grave-song. He confronts self-surpassing, challenges the priests and scholars, and faces the terrifying whisper of the stillest hour that commands him to speak his most abysmal thought.',
            'chapters': [],
        },
        'third-part': {
            'name': 'Third Part',
            'part_label': 'Part Three',
            'description': 'The philosophical climax. Zarathustra confronts the eternal recurrence in the vision of the gateway, nearly perishes from the weight of this thought during his convalescence, and finally affirms it in the ecstatic Seven Seals. Old and New Tables provides a comprehensive restatement of his philosophy.',
            'chapters': [],
        },
        'fourth-part': {
            'name': 'Fourth and Last Part',
            'part_label': 'Part Four',
            'description': 'A dramatic narrative: various "higher men" — kings, a leech, a magician, a pope, the ugliest man — seek out Zarathustra in his cave. They feast, sing the melancholy song and the drunken song, and enact the ass-festival. Zarathustra overcomes his final temptation (pity) and greets the sign of his children.',
            'chapters': [],
        },
    }

    # Thematic group definitions
    thematic_groups = {
        'self-overcoming': {
            'name': 'Self-Overcoming and Transformation',
            'about': 'Nietzsche\'s central teaching: the human being as something to be surpassed. These speeches trace the arc from camel to lion to child — from bearing burdens to destroying old values to creating new ones.',
            'for_readers': 'Read these speeches when you feel the call to transform — when the old skin no longer fits. Start with The Three Metamorphoses for the map, then trace Zarathustra\'s own transformation through Self-Surpassing and The Convalescent.',
            'ids': [],
        },
        'critique-of-society': {
            'name': 'Critique of Society and Culture',
            'about': 'Zarathustra\'s fierce critique of the state, the marketplace, scholars, and all forms of cultural mediocrity. The tarantulas of equality, the new idol of the state, and the flies of the marketplace represent everything that suppresses the creative individual.',
            'for_readers': 'These speeches hit hardest when you feel crushed by conformity. The New Idol on the state, The Tarantulas on the revenge hidden inside demands for equality, The Flies in the Market-place on fame — each strips away a comfortable illusion.',
            'ids': [],
        },
        'eternal-recurrence': {
            'name': 'Eternal Recurrence and Amor Fati',
            'about': 'The most abysmal thought: that everything returns eternally. These speeches chart Zarathustra\'s confrontation with this idea — from the vision of the gateway to the midnight bell\'s twelve strokes to his final Yes-saying.',
            'for_readers': 'The deepest thread in the book. Begin with The Vision and the Enigma, then The Convalescent for the crisis, and finish with The Drunken Song\'s midnight bells. Ask yourself: could I will this life again, eternally?',
            'ids': [],
        },
        'body-and-earth': {
            'name': 'Body, Earth, and the Senses',
            'about': 'Against the despisers of the body and the "backworldsmen" who posit another world beyond this one. Zarathustra calls humanity back to the earth, to the body as "a great reason," to sensuality and passion as holy.',
            'for_readers': 'Read these when you need grounding. The Despisers of the Body contains one of Nietzsche\'s most radical claims: "Body am I entirely, and nothing else; and soul is only a word for something about the body."',
            'ids': [],
        },
        'solitude-and-return': {
            'name': 'Solitude and Return',
            'about': 'Zarathustra\'s recurring rhythm: descent from the mountain, teaching among humans, retreat back to solitude. Each cycle deepens his wisdom and transforms his message.',
            'for_readers': 'Follow Zarathustra\'s pattern of withdrawal and engagement. The Prologue is the first descent, The Child with the Mirror begins the second, The Wanderer the third. Notice how each return from solitude brings new depth.',
            'ids': [],
        },
        'companions-and-encounters': {
            'name': 'Companions and Encounters',
            'about': 'Zarathustra\'s meetings with various figures — the young man on the hill, the friend, the kings, the leech, the magician, the ugliest man. Each encounter tests and refines his teaching.',
            'for_readers': 'Part Four reads almost like a novel. Each "higher man" represents a different incomplete attempt at greatness. Together in Zarathustra\'s cave, they form a comic and poignant assembly of seekers.',
            'ids': [],
        },
        'will-to-power': {
            'name': 'Will, Power, and Values',
            'about': 'The revaluation of all values. Zarathustra challenges conventional morality — neighbour-love, priestly virtue, pity — and calls for a new table of values rooted in life-affirmation.',
            'for_readers': 'These speeches dismantle familiar moral concepts. Neighbour-Love reveals self-flight disguised as altruism. The Priests shows religion as life-denial. Old and New Tables is Nietzsche\'s most comprehensive ethical vision.',
            'ids': [],
        },
        'art-and-song': {
            'name': 'Art, Song, and Celebration',
            'about': 'Zarathustra as poet, dancer, and singer. The night-song, dance-song, and grave-song are among the most lyrical passages in philosophy. Part Four culminates in festival and song.',
            'for_readers': 'The most beautiful writing in the book. The Night-Song is a masterpiece of loneliness and overflow. The Drunken Song\'s twelve midnight strokes are unforgettable. Read these aloud.',
            'ids': [],
        },
    }

    items = []
    sort_order = 0

    # Build L1 items
    for ch in chapters:
        chapter_id = make_id(ch['title'], ch['roman'])
        part_key = assign_part(ch['roman'], ch['title'])
        parts[part_key]['chapters'].append(chapter_id)

        # Assign thematic group
        theme = assign_thematic_group(chapter_id, ch['title'], part_key)
        if theme and theme in thematic_groups:
            thematic_groups[theme]['ids'].append(chapter_id)

        # Build sections
        chapter_text = clean_chapter_text(ch['text'])

        sections = {}

        # Check for numbered sub-sections
        numbered = split_numbered_sections(chapter_text)
        if numbered:
            for j, sec_text in enumerate(numbered):
                sections[f"Section {j+1}"] = sec_text
        else:
            sections["Speech"] = chapter_text

        # Add keywords
        keywords = extract_keywords(chapter_text, ch['title'])

        # Determine category based on part
        part_num = {'first-part': 1, 'second-part': 2, 'third-part': 3, 'fourth-part': 4}[part_key]

        item = {
            "id": chapter_id,
            "name": ch['title'],
            "sort_order": sort_order,
            "level": 1,
            "category": part_key,
            "sections": sections,
            "keywords": keywords,
            "metadata": {
                "part": part_num,
                "source": "Thus Spoke Zarathustra, trans. Thomas Common, 1909"
            }
        }

        if ch['roman']:
            item['metadata']['chapter_number'] = roman_to_int(ch['roman'])

        items.append(item)
        sort_order += 1

    # Build L2 items: Parts
    for part_key, part_data in parts.items():
        part_id = part_key
        item = {
            "id": part_id,
            "name": part_data['part_label'],
            "sort_order": sort_order,
            "level": 2,
            "category": "parts",
            "composite_of": part_data['chapters'],
            "relationship_type": "emergence",
            "sections": {
                "About": part_data['description'],
                "For Readers": f"This part contains {len(part_data['chapters'])} speeches. " +
                    ("Begin with the Prologue — Zarathustra's famous descent from the mountain and his first encounter with humanity."
                     if part_key == 'first-part' else
                     "Return to these speeches when the earlier teachings have settled and you hunger for more."
                     if part_key == 'second-part' else
                     "The philosophical heart of the work. Read The Vision and the Enigma and The Seven Seals for the full arc of eternal recurrence."
                     if part_key == 'third-part' else
                     "A dramatic narrative best read in sequence. The gathering of the higher men is both comedy and tragedy.")
            },
            "keywords": ["structure", "part", "organization"],
            "metadata": {}
        }
        items.append(item)
        sort_order += 1

    # Build L2 items: Thematic groups
    for theme_key, theme_data in thematic_groups.items():
        if not theme_data['ids']:
            continue
        item = {
            "id": f"theme-{theme_key}",
            "name": theme_data['name'],
            "sort_order": sort_order,
            "level": 2,
            "category": "thematic-groups",
            "composite_of": theme_data['ids'],
            "relationship_type": "emergence",
            "sections": {
                "About": theme_data['about'],
                "For Readers": theme_data['for_readers'],
            },
            "keywords": [theme_key.replace('-', ' '), "theme", "grouping"],
            "metadata": {}
        }
        items.append(item)
        sort_order += 1

    # Build L3 items: Meta-categories
    part_ids = [pk for pk in parts.keys()]
    theme_ids = [f"theme-{tk}" for tk, tv in thematic_groups.items() if tv['ids']]

    l3_items = [
        {
            "id": "the-four-parts",
            "name": "The Four Parts of Zarathustra",
            "sort_order": sort_order,
            "level": 3,
            "category": "meta-structure",
            "composite_of": part_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": "Thus Spoke Zarathustra unfolds in four parts, each with its own character. Part One introduces the teaching. Part Two deepens it through song and confrontation. Part Three reaches the philosophical climax with the eternal recurrence. Part Four stages a dramatic gathering of seekers in Zarathustra's cave. The four parts mirror the four seasons, four phases of a life, four movements of a symphony.",
                "For Readers": "Read the parts in order on first encounter. On re-reading, each part can stand alone as a distinct mood and mode of philosophical expression. Part One is declarative, Part Two is lyrical, Part Three is visionary, Part Four is dramatic."
            },
            "keywords": ["structure", "four-parts", "organization", "overview"],
            "metadata": {}
        },
        {
            "id": "thematic-arcs",
            "name": "Thematic Arcs of Zarathustra",
            "sort_order": sort_order + 1,
            "level": 3,
            "category": "meta-themes",
            "composite_of": theme_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": "Eight thematic threads weave through the eighty speeches of Zarathustra. Self-overcoming is the central pillar. Eternal recurrence is the deepest challenge. The critique of society clears ground. Body and earth provide foundation. Solitude and return give rhythm. Companions provide drama. Will and power revalue all values. Art and song give wings. No single thread tells the whole story — together they form Nietzsche's philosophical symphony.",
                "For Readers": "Use these thematic groupings to explore Zarathustra non-linearly. If you are drawn to the lyrical Nietzsche, follow Art and Song. If you want the ethical revolutionary, follow Will, Power, and Values. If you seek the existential depths, follow Eternal Recurrence."
            },
            "keywords": ["themes", "arcs", "overview", "non-linear"],
            "metadata": {}
        }
    ]
    items.extend(l3_items)

    # Build the grammar
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Friedrich Nietzsche",
                    "date": "1883-1885",
                    "note": "Author"
                },
                {
                    "name": "Thomas Common",
                    "date": "1909",
                    "note": "Translator"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar creator"
                }
            ]
        },
        "name": "Thus Spoke Zarathustra",
        "description": "Friedrich Nietzsche's philosophical masterpiece, written between 1883 and 1885 — a prose-poem in four parts in which the prophet Zarathustra descends from mountain solitude to teach humanity about the Overman, the eternal recurrence, and the will to power. Through eighty speeches of extraordinary lyrical force, Nietzsche dismantles conventional morality and calls for a radical affirmation of life. Thomas Common translation (1909). Source: Project Gutenberg eBook #1998 (https://www.gutenberg.org/ebooks/1998).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: No widely known public domain illustration editions exist specifically for Zarathustra, but appropriate visual companions include: Caspar David Friedrich's paintings (1774-1840) — 'Wanderer above the Sea of Fog' and mountain landscapes that capture Zarathustra's solitary heights. William Blake's visionary prints (1757-1827) — prophetic figures and cosmic imagery fitting Nietzsche's tone. Gustave Doré's biblical and literary illustrations (1832-1883) — mountain scenes, prophetic figures, and cosmic vistas.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "philosophy",
            "nietzsche",
            "existentialism",
            "overman",
            "eternal-recurrence",
            "will-to-power",
            "german-philosophy",
            "prose-poetry",
            "wisdom",
            "oracle"
        ],
        "roots": ["western-philosophy", "mysticism", "individualism"],
        "shelves": ["wisdom", "mirror"],
        "lineages": ["Shrei", "Akomolafe", "Andreotti"],
        "worldview": "non-dual",
        "cover_image_url": "",
        "items": items
    }

    # Write output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"Generated {OUTPUT_PATH}")
    print(f"  L1 items (speeches): {sum(1 for i in items if i['level'] == 1)}")
    print(f"  L2 items (parts + themes): {sum(1 for i in items if i['level'] == 2)}")
    print(f"  L3 items (meta-categories): {sum(1 for i in items if i['level'] == 3)}")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
