#!/usr/bin/env python3
"""
Parser for A Selection from the Discourses of Epictetus with the Encheiridion.

Source: Project Gutenberg eBook #10661
Translator: George Long

Structure:
- 57 Discourses (selected) — each starts with ALL-CAPS TITLE followed by em dash and text
- 52 Encheiridion chapters — numbered with Roman numerals (I. through LII.)

L1: Individual discourses and Encheiridion chapters
L2: Thematic groups + Encheiridion as a unit
L3: Meta-categories (The Discourses, The Encheiridion, Thematic Teachings)
"""

import json
import re
import os
from pathlib import Path

SEED_PATH = Path(__file__).parent.parent / "seeds" / "discourses-epictetus.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "discourses-epictetus"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Roman numeral conversion
ROMAN_MAP = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7,
    'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12, 'XIII': 13,
    'XIV': 14, 'XV': 15, 'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19,
    'XX': 20, 'XXI': 21, 'XXII': 22, 'XXIII': 23, 'XXIV': 24, 'XXV': 25,
    'XXVI': 26, 'XXVII': 27, 'XXVIII': 28, 'XXIX': 29, 'XXX': 30,
    'XXXI': 31, 'XXXII': 32, 'XXXIII': 33, 'XXXIV': 34, 'XXXV': 35,
    'XXXVI': 36, 'XXXVII': 37, 'XXXVIII': 38, 'XXXIX': 39, 'XL': 40,
    'XLI': 41, 'XLII': 42, 'XLIII': 43, 'XLIV': 44, 'XLV': 45,
    'XLVI': 46, 'XLVII': 47, 'XLVIII': 48, 'XLIX': 49, 'L': 50,
    'LI': 51, 'LII': 52,
}


def read_seed():
    """Read seed text and strip Gutenberg header/footer."""
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    # Strip Gutenberg header
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[text.index("\n", start_idx) + 1:]

    # Strip Gutenberg footer
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text


def title_case(s):
    """Convert ALL CAPS title to title case, preserving small words."""
    small_words = {'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor',
                   'on', 'at', 'to', 'from', 'by', 'in', 'of', 'with',
                   'not', 'is', 'are', 'we', 'our', 'his', 'her', 'who',
                   'which', 'that', 'how', 'what'}
    words = s.lower().split()
    result = []
    for i, w in enumerate(words):
        if i == 0 or w not in small_words:
            result.append(w.capitalize())
        else:
            result.append(w)
    return " ".join(result)


def make_id(title, prefix="discourse"):
    """Generate a hyphenated ID from a title."""
    # Take first few significant words
    clean = re.sub(r'[^a-z0-9\s]', '', title.lower())
    words = clean.split()[:6]
    slug = "-".join(words)
    return f"{prefix}-{slug}" if prefix else slug


def extract_keywords(text):
    """Extract keywords from discourse text based on Stoic concepts."""
    keyword_map = {
        'desire': ['desire', 'aversion'],
        'freedom': ['free', 'freedom', 'liberty', 'slave', 'slavery'],
        'judgment': ['judgment', 'opinion', 'assent', 'impression', 'appearance'],
        'virtue': ['virtue', 'virtuous', 'good', 'evil'],
        'reason': ['reason', 'rational', 'irrational', 'logic'],
        'death': ['death', 'die', 'dying', 'mortal'],
        'god': ['god', 'gods', 'zeus', 'divine', 'providence'],
        'nature': ['nature', 'natural'],
        'duty': ['duty', 'duties', 'role', 'function'],
        'tranquility': ['tranquil', 'tranquillity', 'peace', 'calm', 'undisturbed'],
        'suffering': ['suffer', 'pain', 'lament', 'grief', 'misery', 'wretched'],
        'courage': ['courage', 'courageous', 'brave', 'fear', 'coward'],
        'self-discipline': ['discipline', 'exercise', 'practice', 'training'],
        'friendship': ['friend', 'friendship', 'companion'],
        'externals': ['external', 'externals', 'body', 'property', 'reputation'],
        'will': ['will', 'choice', 'purpose', 'prohairesis', 'proairesis'],
        'progress': ['progress', 'improvement', 'improve'],
        'philosophy': ['philosophy', 'philosopher', 'philosophize'],
        'contentment': ['content', 'contentment', 'satisfied', 'happiness'],
        'indifference': ['indifferent', 'indifference'],
        'attention': ['attention', 'attentive', 'careful', 'vigilant'],
        'cynicism': ['cynic', 'cynicism', 'diogenes'],
        'socrates': ['socrates', 'socratic'],
    }
    text_lower = text.lower()
    found = []
    for keyword, triggers in keyword_map.items():
        if any(t in text_lower for t in triggers):
            found.append(keyword)
    return found[:6]  # Limit to 6 keywords


def create_reflection(text):
    """Create a brief reflection prompt based on the discourse content."""
    text_lower = text.lower()
    if 'desire' in text_lower or 'aversion' in text_lower:
        return "What do you desire that is not in your power? How might releasing that desire bring peace?"
    elif 'death' in text_lower or 'die' in text_lower:
        return "How does contemplating mortality change the way you see your daily concerns?"
    elif 'friend' in text_lower or 'friendship' in text_lower:
        return "What kind of friend are you? Do you bring virtue or mere convenience to your relationships?"
    elif 'free' in text_lower or 'freedom' in text_lower:
        return "Where in your life are you enslaved by things outside your control? What would true freedom look like?"
    elif 'god' in text_lower or 'providence' in text_lower:
        return "How does the idea of a rational, ordered cosmos change how you meet difficulty?"
    elif 'duty' in text_lower or 'role' in text_lower:
        return "What roles do you hold in life? Are you fulfilling them with attention and care?"
    elif 'opinion' in text_lower or 'judgment' in text_lower:
        return "Which of your judgments about events are truly yours, and which were inherited without examination?"
    elif 'progress' in text_lower or 'improv' in text_lower:
        return "Where are you making genuine progress in character, not just in knowledge or reputation?"
    elif 'extern' in text_lower:
        return "What external things are you clinging to? What would remain if they were taken away?"
    elif 'fear' in text_lower or 'coward' in text_lower:
        return "What are you afraid of? Is it truly harmful, or is the fear itself the only harm?"
    elif 'tyrant' in text_lower:
        return "Who or what acts as a tyrant in your life? What power have you given them over your inner state?"
    elif 'attention' in text_lower or 'careful' in text_lower:
        return "How attentive are you to your own thoughts and reactions throughout the day?"
    else:
        return "What is the central teaching here, and how does it apply to a situation you face right now?"


def parse_discourses(text):
    """Parse the Discourses section into individual items."""
    # Find the ACTUAL start of the discourses section (not the TOC entry).
    # The real section is the last occurrence of the heading before the Encheiridion.
    disc_matches = list(re.finditer(
        r"A SELECTION FROM THE DISCOURSES OF EPICTETUS\.", text
    ))
    if not disc_matches:
        raise ValueError("Could not find start of Discourses section")
    disc_start = disc_matches[-1].start()

    # Find the ACTUAL Encheiridion section (the last occurrence, which has content)
    ench_matches = list(re.finditer(
        r"THE ENCHEIRIDION, OR MANUAL\.", text
    ))
    if not ench_matches:
        raise ValueError("Could not find start of Encheiridion section")
    ench_start = ench_matches[-1].start()

    disc_text = text[disc_start:ench_start]

    # Two-step approach: first find all title positions using .em-dash pattern,
    # then extract text between them.
    # Titles may span multiple lines (e.g., "HOW A MAN SHOULD PROCEED FROM THE PRINCIPLE OF GOD BEING THE FATHER OF\nALL MEN TO THE REST")
    em_dash = "\u2014"
    title_pattern = re.compile(
        r"([A-Z][A-Z ,.'()\-]+(?:\n[A-Z][A-Z ,.'()\-]+)*)\." + em_dash,
    )

    matches = list(title_pattern.finditer(disc_text))
    discourses = []

    for i, match in enumerate(matches):
        raw_title = match.group(1).strip()
        # Clean up multi-line titles
        raw_title = re.sub(r"\s*\n\s*", " ", raw_title)

        # Body starts after the .— and goes until the next title or end
        body_start = match.end()
        if i + 1 < len(matches):
            body_end = matches[i + 1].start()
        else:
            body_end = len(disc_text)

        body = disc_text[body_start:body_end].strip()

        # Clean up body text - normalize whitespace
        body = re.sub(r'\n(?!\n)', ' ', body)  # Join lines within paragraphs
        body = re.sub(r'\n{2,}', '\n\n', body)  # Normalize paragraph breaks
        body = re.sub(r'  +', ' ', body)  # Collapse multiple spaces

        nice_title = title_case(raw_title)
        discourses.append({
            'title': nice_title,
            'raw_title': raw_title,
            'body': body.strip(),
        })

    return discourses


def parse_encheiridion(text):
    """Parse the Encheiridion into individual chapters."""
    ench_matches = list(re.finditer(r"THE ENCHEIRIDION, OR MANUAL\.", text))
    if not ench_matches:
        raise ValueError("Could not find Encheiridion")
    ench_start = ench_matches[-1].start()

    ench_text = text[ench_start:]

    # Split by Roman numeral markers (standalone lines like "I.", "II.", etc.)
    pattern = re.compile(r'^([IVXLC]+)\.\s*$', re.MULTILINE)
    matches = list(pattern.finditer(ench_text))

    chapters = []
    for i, match in enumerate(matches):
        roman = match.group(1)
        num = ROMAN_MAP.get(roman)
        if num is None:
            continue

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(ench_text)
        body = ench_text[start:end].strip()

        # Clean up body text
        body = re.sub(r'\n(?!\n)', ' ', body)
        body = re.sub(r'\n{2,}', '\n\n', body)
        body = re.sub(r'  +', ' ', body)

        chapters.append({
            'roman': roman,
            'number': num,
            'body': body.strip(),
        })

    return chapters


# Thematic groupings for L2 emergence
THEMATIC_GROUPS = {
    'desire-and-aversion': {
        'name': 'Desire and Aversion',
        'about': 'Epictetus returns constantly to the discipline of desire: wanting only what is in our power, and being averse only to what is truly harmful. These discourses train the student to redirect desire from externals (wealth, fame, comfort) toward the only true good — a virtuous will.',
        'for_readers': 'Begin here if you struggle with wanting things you cannot control, or if fear and anxiety dominate your life. These teachings form the foundation of Stoic practice.',
        'keywords': ['desire', 'aversion', 'will', 'self-discipline'],
    },
    'judgment-and-impressions': {
        'name': 'Judgment and Impressions',
        'about': 'For Epictetus, suffering comes not from events but from our judgments about them. These discourses explore how to examine impressions before assenting to them, how to distinguish what is truly good from what merely appears so, and how to use reason as the governing faculty of life.',
        'for_readers': 'Essential for anyone who wants to understand how thoughts shape experience. These passages are the ancient root of cognitive behavioral therapy.',
        'keywords': ['judgment', 'reason', 'virtue', 'philosophy'],
    },
    'freedom-and-the-will': {
        'name': 'Freedom and the Will',
        'about': 'True freedom, Epictetus teaches, belongs only to the person whose will is aligned with nature. No tyrant, prison, or exile can touch the free person, because freedom is not the absence of constraint but the mastery of one\'s own choices. These discourses explore the radical Stoic claim that a slave can be freer than an emperor.',
        'for_readers': 'Read these when you feel trapped by circumstances. Epictetus, himself a former slave, speaks with unique authority on inner freedom.',
        'keywords': ['freedom', 'will', 'courage', 'externals'],
    },
    'social-roles-and-duty': {
        'name': 'Social Roles and Duty',
        'about': 'Stoicism is not withdrawal from the world. Epictetus insists that we discover our duties by examining the names we bear — parent, child, citizen, friend, human being. Each role carries obligations that we must fulfill with attention and care, without being disturbed by outcomes we cannot control.',
        'for_readers': 'Practical guidance for relationships, work, and community life. How to be fully engaged in your roles without being enslaved by them.',
        'keywords': ['duty', 'friendship', 'virtue', 'attention'],
    },
    'facing-adversity': {
        'name': 'Facing Adversity',
        'about': 'Sickness, exile, poverty, death — Epictetus addresses each directly. These discourses teach that adversity is not an obstacle to the good life but the very material from which virtue is formed. The wrestler needs an opponent; the philosopher needs difficulty.',
        'for_readers': 'Turn to these discourses in times of trouble. They offer not comfort but something more durable: a way of seeing hardship as the occasion for strength.',
        'keywords': ['suffering', 'courage', 'death', 'tranquility'],
    },
    'the-philosophic-life': {
        'name': 'The Philosophic Life',
        'about': 'What does it mean to actually live as a philosopher, rather than merely talk about philosophy? Epictetus is relentless on this point: philosophy is not a set of doctrines to memorize but a way of life to practice. These discourses critique mere bookishness and call for embodied wisdom.',
        'for_readers': 'A corrective for anyone who reads more than they practice. Epictetus asks: what has your philosophy actually changed in your life?',
        'keywords': ['philosophy', 'progress', 'self-discipline', 'attention'],
    },
    'god-nature-and-providence': {
        'name': 'God, Nature, and Providence',
        'about': 'Epictetus sees the cosmos as rationally ordered and governed by divine providence. Human reason is a fragment of the divine logos. These discourses explore what it means to live in harmony with a rational universe, to see ourselves as citizens of the cosmos, and to accept what happens as the will of God.',
        'for_readers': 'These passages reveal the theological dimension of Stoicism — not as dogma but as a lived relationship with the rational order of things.',
        'keywords': ['god', 'nature', 'reason', 'contentment'],
    },
}

# Map discourse titles (lowercase) to thematic groups
# We assign each discourse to its best-fitting theme based on content
DISCOURSE_THEME_MAP = {
    'of the things which are in our power and not in our power': 'desire-and-aversion',
    'how a man on every occasion can maintain his proper character': 'judgment-and-impressions',
    'how a man should proceed from the principle of god being the father of all men to the rest': 'god-nature-and-providence',
    'of progress or improvement': 'the-philosophic-life',
    'against the academics': 'judgment-and-impressions',
    'of providence': 'god-nature-and-providence',
    'consequences': 'judgment-and-impressions',
    'of contentment': 'god-nature-and-providence',
    'how everything may be done acceptably to the gods': 'god-nature-and-providence',
    'what philosophy promises': 'the-philosophic-life',
    'how we should behave to tyrants': 'freedom-and-the-will',
    'against those who wish to be admired': 'desire-and-aversion',
    'how we should struggle with circumstances': 'facing-adversity',
    'on the same': 'facing-adversity',
    'against them': 'judgment-and-impressions',
    'great things among men': 'judgment-and-impressions',
    'how magnanimity is consistent with care': 'judgment-and-impressions',
    'of indifference': 'judgment-and-impressions',
    'how we ought to use divination': 'god-nature-and-providence',
    'we assume the character of a philosopher': 'the-philosophic-life',
    'how we may discover the duties of life from names': 'social-roles-and-duty',
    'what the beginning of philosophy is': 'the-philosophic-life',
    'of disputation or discussion': 'the-philosophic-life',
    'to naso': 'the-philosophic-life',
    'determined': 'desire-and-aversion',
    'that we do not strive to use our opinions about good and evil': 'judgment-and-impressions',
    'how we must adapt preconceptions to particular cases': 'judgment-and-impressions',
    'how we should struggle against appearances': 'judgment-and-impressions',
    'of inconsistency': 'judgment-and-impressions',
    'on friendship': 'social-roles-and-duty',
    'on the power of speaking': 'the-philosophic-life',
    'that logic is necessary': 'the-philosophic-life',
    'of finery in dress': 'desire-and-aversion',
    'we neglect the chief things': 'desire-and-aversion',
    'we ought chiefly to practise ourselves': 'desire-and-aversion',
    'miscellaneous': 'the-philosophic-life',
    'to the administrator of the free cities who was an epicurean': 'social-roles-and-duty',
    'to a certain rhetorician who was going up to rome on a suit': 'social-roles-and-duty',
    'in what manner we ought to bear sickness': 'facing-adversity',
    'about exercise': 'self-discipline-not-used',
    'what solitude is, and what kind of person a solitary man is': 'freedom-and-the-will',
    'certain miscellaneous matters': 'the-philosophic-life',
    'men': 'social-roles-and-duty',
    'about cynicism': 'the-philosophic-life',
    'in our power': 'desire-and-aversion',
    'to those who fear want': 'facing-adversity',
    'about freedom': 'freedom-and-the-will',
    'on familiar intimacy': 'social-roles-and-duty',
    'what things we should exchange for other things': 'desire-and-aversion',
    'to those who are desirous of passing life in tranquillity': 'desire-and-aversion',
    'against the quarrelsome and ferocious': 'social-roles-and-duty',
    'against those who lament over being pitied': 'facing-adversity',
    'on freedom from fear': 'freedom-and-the-will',
    'to a person who had been changed to a character of shamelessness': 'social-roles-and-duty',
    'what things we ought to despise and what things we ought to value': 'judgment-and-impressions',
    'on attention': 'desire-and-aversion',
    'against or to those who readily tell their own affairs': 'social-roles-and-duty',
}


def assign_theme(title):
    """Assign a discourse to a thematic group based on its title."""
    title_lower = title.lower()
    # Try exact match from map
    for key, theme in DISCOURSE_THEME_MAP.items():
        if key in title_lower:
            return theme
    # Fallback: keyword-based assignment
    if any(w in title_lower for w in ['desire', 'aversion', 'want', 'content', 'admire', 'dress', 'exchange']):
        return 'desire-and-aversion'
    if any(w in title_lower for w in ['judgment', 'opinion', 'impression', 'appear', 'preconception', 'inconsist']):
        return 'judgment-and-impressions'
    if any(w in title_lower for w in ['free', 'tyrant', 'power', 'solitude', 'fear']):
        return 'freedom-and-the-will'
    if any(w in title_lower for w in ['duty', 'friend', 'role', 'intimacy', 'quarrel', 'rhetorician', 'administrator']):
        return 'social-roles-and-duty'
    if any(w in title_lower for w in ['sick', 'death', 'exile', 'adversity', 'lament', 'pity', 'bear']):
        return 'facing-adversity'
    if any(w in title_lower for w in ['philosophy', 'philosopher', 'progress', 'logic', 'disputation', 'cynic', 'speaking']):
        return 'the-philosophic-life'
    if any(w in title_lower for w in ['god', 'providence', 'nature', 'divine']):
        return 'god-nature-and-providence'
    return 'the-philosophic-life'  # default


def build_grammar():
    text = read_seed()
    discourses = parse_discourses(text)
    encheiridion = parse_encheiridion(text)

    print(f"Parsed {len(discourses)} discourses and {len(encheiridion)} Encheiridion chapters")

    items = []
    sort_order = 0

    # Track IDs for L2 composite_of
    discourse_ids = []
    theme_to_ids = {k: [] for k in THEMATIC_GROUPS}
    encheiridion_ids = []

    # ---- L1: Discourses ----
    for i, disc in enumerate(discourses):
        disc_id = f"discourse-{i+1:02d}"
        # Ensure unique IDs
        discourse_ids.append(disc_id)
        theme = assign_theme(disc['title'])
        if theme in theme_to_ids:
            theme_to_ids[theme].append(disc_id)
        else:
            theme_to_ids.setdefault('the-philosophic-life', []).append(disc_id)

        keywords = extract_keywords(disc['body'])
        reflection = create_reflection(disc['body'])

        items.append({
            'id': disc_id,
            'name': disc['title'],
            'sort_order': sort_order,
            'category': 'discourses',
            'level': 1,
            'sections': {
                'Teaching': disc['body'],
                'Reflection': reflection,
            },
            'keywords': keywords if keywords else ['philosophy', 'stoicism'],
            'metadata': {
                'discourse_number': i + 1,
                'source': 'Discourses of Epictetus, trans. George Long, 1877',
            },
        })
        sort_order += 1

    # ---- L1: Encheiridion chapters ----
    for ch in encheiridion:
        ch_id = f"encheiridion-{ch['number']:02d}"
        encheiridion_ids.append(ch_id)

        keywords = extract_keywords(ch['body'])
        reflection = create_reflection(ch['body'])

        items.append({
            'id': ch_id,
            'name': f"Encheiridion {ch['roman']}",
            'sort_order': sort_order,
            'category': 'encheiridion',
            'level': 1,
            'sections': {
                'Teaching': ch['body'],
                'Reflection': reflection,
            },
            'keywords': keywords if keywords else ['philosophy', 'stoicism'],
            'metadata': {
                'chapter_number': ch['number'],
                'roman_numeral': ch['roman'],
                'source': 'The Encheiridion (Manual), Epictetus, trans. George Long, 1877',
            },
        })
        sort_order += 1

    # ---- L2: Thematic groups for Discourses ----
    for theme_id, theme_info in THEMATIC_GROUPS.items():
        member_ids = theme_to_ids.get(theme_id, [])
        if not member_ids:
            continue

        items.append({
            'id': f"theme-{theme_id}",
            'name': theme_info['name'],
            'sort_order': sort_order,
            'category': 'thematic-groups',
            'level': 2,
            'composite_of': member_ids,
            'relationship_type': 'emergence',
            'sections': {
                'About': theme_info['about'],
                'For Readers': theme_info['for_readers'],
            },
            'keywords': theme_info['keywords'],
            'metadata': {
                'discourse_count': len(member_ids),
            },
        })
        sort_order += 1

    # ---- L2: The Encheiridion as a unit ----
    items.append({
        'id': 'section-encheiridion',
        'name': 'The Encheiridion (Manual)',
        'sort_order': sort_order,
        'category': 'sections',
        'level': 2,
        'composite_of': encheiridion_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The Encheiridion (Greek: Enchiridion, meaning "handbook" or "manual") is a short compilation of Epictetus\' core teachings, assembled by his student Arrian. While the Discourses record extended lectures and dialogues, the Encheiridion distills the essential principles into brief, memorable maxims meant to be kept close at hand — a portable guide to Stoic practice. It opens with the most fundamental distinction in Stoic ethics: some things are in our power, and others are not.',
            'For Readers': 'The Encheiridion is the best entry point to Epictetus. Read it first as a whole, then return to individual chapters for daily practice. Many Stoic practitioners read one chapter per day as a morning exercise.',
        },
        'keywords': ['philosophy', 'stoicism', 'self-discipline', 'will', 'freedom'],
        'metadata': {
            'chapter_count': len(encheiridion_ids),
        },
    })
    sort_order += 1

    # ---- L2: The Discourses as a unit ----
    items.append({
        'id': 'section-discourses',
        'name': 'The Discourses (Selected)',
        'sort_order': sort_order,
        'category': 'sections',
        'level': 2,
        'composite_of': discourse_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'The Discourses (Diatribai) of Epictetus were recorded by his student Arrian of Nicomedia, who attended his lectures at Nicopolis around 108 CE. Originally in eight books, only four survive. This selection by George Long draws from the surviving books, presenting the most essential teachings on freedom, desire, judgment, duty, and the philosophic life. The discourses are informal, conversational, and often sharp — Epictetus challenges, mocks, and exhorts his students like a Stoic Socrates.',
            'For Readers': 'These are extended teachings. Browse by theme using the thematic groups, or read sequentially. Epictetus repeats his core ideas in many contexts — this is intentional. Repetition is practice.',
        },
        'keywords': ['philosophy', 'stoicism', 'teaching', 'wisdom'],
        'metadata': {
            'discourse_count': len(discourse_ids),
        },
    })
    sort_order += 1

    # ---- L3: Meta-categories ----
    thematic_ids = [f"theme-{k}" for k in THEMATIC_GROUPS if theme_to_ids.get(k)]

    items.append({
        'id': 'meta-stoic-practice',
        'name': 'The Three Disciplines of Stoic Practice',
        'sort_order': sort_order,
        'category': 'meta',
        'level': 3,
        'composite_of': thematic_ids,
        'relationship_type': 'emergence',
        'sections': {
            'About': 'Epictetus organizes Stoic practice around three disciplines (topoi): the Discipline of Desire (what to want and what to avoid), the Discipline of Action (how to act rightly in relationships and roles), and the Discipline of Assent (how to judge impressions correctly). Every discourse and every chapter of the Encheiridion addresses one or more of these disciplines. The thematic groups in this grammar map roughly to this framework: Desire and Aversion and Facing Adversity train the first discipline; Social Roles and Duty train the second; Judgment and Impressions and Freedom and the Will train the third.',
            'For Readers': 'Use this as a map of the entire teaching. Start with whichever discipline speaks to your current situation: if you are anxious, start with Desire and Aversion; if your relationships are strained, start with Social Roles; if you are confused or overwhelmed, start with Judgment and Impressions.',
        },
        'keywords': ['stoicism', 'philosophy', 'self-discipline', 'virtue', 'wisdom'],
        'metadata': {},
    })
    sort_order += 1

    items.append({
        'id': 'meta-complete-works',
        'name': 'The Complete Teaching of Epictetus',
        'sort_order': sort_order,
        'category': 'meta',
        'level': 3,
        'composite_of': ['section-discourses', 'section-encheiridion'],
        'relationship_type': 'emergence',
        'sections': {
            'About': 'Epictetus (c. 50-135 CE) was born a slave in Hierapolis, Phrygia. He studied under Musonius Rufus in Rome, gained his freedom, and after the philosophers were expelled by Domitian in 89 CE, established a school at Nicopolis in Epirus. He taught until old age, never writing a word — everything we have was recorded by his devoted student Arrian. This grammar contains the two surviving works: a selection from the Discourses (extended lectures) and the complete Encheiridion (a handbook of essential teachings). Together they form the most complete and accessible expression of late Stoic philosophy.',
            'For Readers': 'For beginners: start with the Encheiridion, then explore the Discourses by theme. For serious study: read the Discourses sequentially, then use the Encheiridion as a daily companion. The repetition across the two works is not redundancy — it is the practice itself.',
        },
        'keywords': ['stoicism', 'philosophy', 'wisdom', 'virtue', 'freedom'],
        'metadata': {},
    })
    sort_order += 1

    # ---- Build the grammar ----
    grammar = {
        '_grammar_commons': {
            'schema_version': '1.0',
            'license': 'CC-BY-SA-4.0',
            'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/',
            'attribution': [
                {
                    'name': 'PlayfulProcess',
                    'url': 'https://lifeisprocess.substack.com/',
                    'date': '2026-03-04',
                    'note': 'Grammar structure and organization',
                },
                {
                    'name': 'Epictetus',
                    'date': 'c. 108 CE',
                    'note': 'Original teachings (as recorded by Arrian)',
                },
                {
                    'name': 'George Long',
                    'date': '1877',
                    'note': 'English translation (public domain via Project Gutenberg)',
                },
            ],
        },
        'name': 'Discourses of Epictetus with the Encheiridion',
        'description': (
            'A selection from the Discourses of Epictetus (c. 50-135 CE), the Stoic philosopher '
            'who was born a slave and became one of the most influential teachers of practical ethics '
            'in the ancient world. Includes the complete Encheiridion (Manual), a distillation of his '
            'core teachings. Translated by George Long (1877). "It is not things that disturb us, but '
            'our judgments about things." Epictetus taught that freedom lies not in controlling '
            'circumstances but in mastering our responses to them — a teaching that directly influenced '
            'Marcus Aurelius, and centuries later, cognitive behavioral therapy. '
            'Source: Project Gutenberg eBook #10661 (https://www.gutenberg.org/ebooks/10661).\n\n'
            'PUBLIC DOMAIN ILLUSTRATION REFERENCES: Engraved portrait of Epictetus from Thomas Stanley\'s '
            '"History of Philosophy" (1655). Illustrations from 17th and 18th century editions of the '
            'Encheiridion. Classical Greek and Roman sculpture photography — busts of Stoic philosophers. '
            'Manuscript illuminations from medieval copies of the Discourses. Engravings of Nicopolis ruins '
            'where Epictetus taught. Illustrations from Edward Poynter and Lawrence Alma-Tadema depicting '
            'Roman philosophical life.'
        ),
        'grammar_type': 'custom',
        'creator_name': 'PlayfulProcess',
        'creator_link': 'https://lifeisprocess.substack.com/',
        'tags': [
            'philosophy',
            'stoicism',
            'greek',
            'ethics',
            'wisdom',
            'public-domain',
            'full-text',
            'epictetus',
            'ancient',
            'self-help',
            'freedom',
            'virtue',
        ],
        'roots': ['greek-philosophy'],
        'shelves': ['wisdom'],
        'lineages': ['Linehan'],
        'worldview': 'rationalist',
        'cover_image_url': '',
        'items': items,
    }

    return grammar


def main():
    grammar = build_grammar()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write grammar
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Summary
    items = grammar['items']
    l1 = [i for i in items if i['level'] == 1]
    l2 = [i for i in items if i['level'] == 2]
    l3 = [i for i in items if i['level'] == 3]
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1 items: {len(l1)} ({len([i for i in l1 if i['category'] == 'discourses'])} discourses, {len([i for i in l1 if i['category'] == 'encheiridion'])} encheiridion)")
    print(f"  L2 items: {len(l2)} ({len([i for i in l2 if i['category'] == 'thematic-groups'])} thematic groups, {len([i for i in l2 if i['category'] == 'sections'])} sections)")
    print(f"  L3 items: {len(l3)}")
    print(f"  Total: {len(items)}")


if __name__ == '__main__':
    main()
