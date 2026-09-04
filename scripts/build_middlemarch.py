#!/usr/bin/env python3
"""
Build grammar.json for Middlemarch by George Eliot.

Source: Project Gutenberg eBook #145
Author: George Eliot (Mary Ann Evans) (1871-1872)

Structure:
- L1: Prelude + 86 chapters + Finale = 88 items
- L2: Book groupings (8) + Thematic threads (6)
- L3: Meta-categories (The Complete Novel, Thematic Arcs)

Middlemarch has a Prelude, 8 Books with named subtitles, 86 chapters
numbered continuously with Roman numerals, and a Finale.
Chapters have epigraphs (quotes) which we include as part of the text.
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "middlemarch.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "middlemarch"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Book structure
BOOKS = [
    {"num": 1, "title": "Miss Brooke", "chapters": list(range(1, 13))},
    {"num": 2, "title": "Old and Young", "chapters": list(range(13, 23))},
    {"num": 3, "title": "Waiting for Death", "chapters": list(range(23, 34))},
    {"num": 4, "title": "Three Love Problems", "chapters": list(range(34, 43))},
    {"num": 5, "title": "The Dead Hand", "chapters": list(range(43, 53))},
    {"num": 6, "title": "The Widow and the Wife", "chapters": list(range(53, 63))},
    {"num": 7, "title": "Two Temptations", "chapters": list(range(63, 72))},
    {"num": 8, "title": "Sunset and Sunrise", "chapters": list(range(72, 87))},
]

# Roman numeral conversion
def roman_to_int(roman):
    """Convert a Roman numeral string to integer."""
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
    return text[start_idx:end_idx].strip()


def parse_text(text):
    """Parse Middlemarch into Prelude, 86 chapters, and Finale."""
    items = []

    # Find PRELUDE
    prelude_match = re.search(r'^PRELUDE\.\s*$', text, re.MULTILINE)
    if not prelude_match:
        print("WARNING: Could not find PRELUDE")
        return items

    # Find first BOOK marker
    first_book = re.search(r'^BOOK I\.\s*$', text, re.MULTILINE)
    if first_book:
        prelude_text = text[prelude_match.end():first_book.start()].strip()
        prelude_text = re.sub(r'\n{3,}', '\n\n', prelude_text)
        items.append({
            'type': 'prelude',
            'text': prelude_text,
        })

    # Find all chapter positions
    chapter_positions = []
    for match in re.finditer(r'^CHAPTER\s+([IVXLC]+)\.\s*$', text, re.MULTILINE):
        roman = match.group(1)
        num = roman_to_int(roman)
        chapter_positions.append((num, match.start(), match.end()))

    # Find FINALE
    finale_match = re.search(r'^FINALE\.\s*$', text, re.MULTILINE)

    # Find THE END
    the_end_match = re.search(r'^THE END\s*$', text, re.MULTILINE)

    # Parse each chapter
    for i, (ch_num, ch_start, ch_end) in enumerate(chapter_positions):
        # Chapter text starts after the heading
        text_start = ch_end

        # Ends at next chapter, FINALE, or end of text
        if i + 1 < len(chapter_positions):
            text_end = chapter_positions[i + 1][1]
        elif finale_match:
            text_end = finale_match.start()
        else:
            text_end = len(text)

        chapter_text = text[text_start:text_end].strip()
        # Remove BOOK headers that appear within the chapter text span
        # (BOOK headers appear between chapters)
        chapter_text = re.sub(r'^BOOK\s+[IVXLC]+\.\s*\n[A-Z ]+\.\s*\n', '', chapter_text, flags=re.MULTILINE)
        chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)

        items.append({
            'type': 'chapter',
            'num': ch_num,
            'text': chapter_text,
        })

    # Parse FINALE
    if finale_match:
        finale_end = the_end_match.start() if the_end_match else len(text)
        finale_text = text[finale_match.end():finale_end].strip()
        finale_text = re.sub(r'\n{3,}', '\n\n', finale_text)
        items.append({
            'type': 'finale',
            'text': finale_text,
        })

    return items


def make_chapter_id(num):
    return f"chapter-{num}"


def extract_first_sentence(text, max_len=150):
    """Extract the first non-epigraph sentence."""
    # Skip epigraph (typically starts with " or — or is poetry)
    lines = text.split('\n')
    # Find first paragraph that looks like prose (not a quote)
    in_epigraph = True
    prose_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if not in_epigraph:
                continue
            # Empty line after epigraph might signal start of prose
            continue
        if in_epigraph:
            # Epigraph lines typically start with quotes, dashes, or are short poetry
            if stripped.startswith('"') or stripped.startswith("'") or stripped.startswith('—') or stripped.startswith('_'):
                continue
            if len(stripped) < 60 and not stripped[0].isupper():
                continue
            # This looks like prose
            in_epigraph = False
            prose_start = i

    clean_text = ' '.join(lines[prose_start:])
    clean = ' '.join(clean_text.split())
    clean = re.sub(r'_([^_]+)_', r'\1', clean)
    m = re.search(r'[.!?]["\u201d]?\s', clean)
    if m and m.end() <= max_len:
        return clean[:m.end()].strip()
    if len(clean) > max_len:
        truncated = clean[:max_len]
        last_space = truncated.rfind(' ')
        if last_space > max_len // 2:
            return truncated[:last_space] + "..."
        return truncated[:max_len - 3] + "..."
    return clean


# Chapter keywords
CHAPTER_KEYWORDS = {
    0: ["prelude", "saint-theresa", "vocation", "women", "aspiration"],  # Prelude
    1: ["dorothea", "brooke", "beauty", "religion", "celia"],
    2: ["casaubon", "dorothea", "courtship", "scholarship", "ambition"],
    3: ["casaubon", "proposal", "dorothea", "marriage", "devotion"],
    4: ["brooke", "chettam", "marriage", "dorothea", "politics"],
    5: ["dorothea", "casaubon", "engagement", "plans", "tipton"],
    6: ["casaubon", "dorothea", "will-ladislaw", "cousin", "art"],
    7: ["dorothea", "casaubon", "wedding", "farewell", "celia"],
    8: ["dorothea", "honeymoon", "rome", "disillusionment", "art"],
    9: ["dorothea", "casaubon", "rome", "ladislaw", "unhappiness"],
    10: ["ladislaw", "dorothea", "naumann", "art", "admiration"],
    11: ["lydgate", "middlemarch", "medicine", "ambition", "reform"],
    12: ["lydgate", "vincy", "fred", "featherstone", "society"],
    13: ["vincy", "featherstone", "garth", "money", "inheritance"],
    14: ["fred", "vincy", "debt", "featherstone", "irresponsibility"],
    15: ["lydgate", "medicine", "ambition", "research", "paris"],
    16: ["lydgate", "hospital", "bulstrode", "reform", "politics"],
    17: ["farebrother", "lydgate", "clergy", "character", "friendship"],
    18: ["casaubon", "dorothea", "marriage", "scholarship", "coldness"],
    19: ["dorothea", "casaubon", "rome", "ladislaw", "meeting"],
    20: ["dorothea", "casaubon", "rome", "ladislaw", "art"],
    21: ["dorothea", "casaubon", "return", "ladislaw", "farewell"],
    22: ["lydgate", "rosamond", "vincy", "attraction", "beauty"],
    23: ["fred", "featherstone", "illness", "garth", "money"],
    24: ["fred", "featherstone", "debt", "garth", "dishonor"],
    25: ["fred", "mary-garth", "love", "featherstone", "vigil"],
    26: ["lydgate", "hospital", "chaplain", "politics", "compromise"],
    27: ["dorothea", "casaubon", "marriage", "unhappiness", "duty"],
    28: ["dorothea", "casaubon", "quarrel", "reconciliation", "will"],
    29: ["casaubon", "ladislaw", "jealousy", "will", "codicil"],
    30: ["lydgate", "rosamond", "courtship", "flirtation", "society"],
    31: ["lydgate", "rosamond", "engagement", "love", "impulse"],
    32: ["featherstone", "death", "funeral", "will", "inheritance"],
    33: ["featherstone", "will", "reading", "rigg", "disappointment"],
    34: ["fred", "disappointed", "inheritance", "garth", "ruin"],
    35: ["lydgate", "rosamond", "engagement", "family", "objections"],
    36: ["lydgate", "rosamond", "wedding", "marriage", "ambition"],
    37: ["dorothea", "casaubon", "key-to-all-mythologies", "ladislaw", "visit"],
    38: ["dorothea", "casaubon", "ladislaw", "jealousy", "prohibition"],
    39: ["dorothea", "casaubon", "codicil", "will", "control"],
    40: ["caleb-garth", "farebrother", "lydgate", "community", "work"],
    41: ["dorothea", "casaubon", "promise", "death", "midnight"],
    42: ["casaubon", "dorothea", "death", "garden", "dawn"],
    43: ["dorothea", "widowhood", "codicil", "ladislaw", "inheritance"],
    44: ["dorothea", "casaubon", "will", "codicil", "ladislaw"],
    45: ["bulstrode", "raffles", "past", "secret", "blackmail"],
    46: ["ladislaw", "dorothea", "middlemarch", "politics", "journalism"],
    47: ["ladislaw", "dorothea", "meeting", "renunciation", "love"],
    48: ["dorothea", "farebrother", "ladislaw", "church", "reform"],
    49: ["dorothea", "ladislaw", "declaration", "renunciation", "passion"],
    50: ["lydgate", "rosamond", "debt", "financial-trouble", "marriage"],
    51: ["lydgate", "rosamond", "money", "quarrel", "house"],
    52: ["lydgate", "rosamond", "debt", "bulstrode", "compromise"],
    53: ["bulstrode", "raffles", "past", "guilt", "retribution"],
    54: ["dorothea", "casaubon", "ladislaw", "brooke", "politics"],
    55: ["dorothea", "ladislaw", "meeting", "emotion", "longing"],
    56: ["lydgate", "rosamond", "marriage", "unhappiness", "debt"],
    57: ["fred", "garth", "farebrother", "mary", "love"],
    58: ["rosamond", "ladislaw", "flirtation", "dorothea", "jealousy"],
    59: ["ladislaw", "rosamond", "dorothea", "misunderstanding", "anger"],
    60: ["fred", "mary", "farebrother", "love", "rivalry"],
    61: ["dorothea", "rosamond", "lydgate", "friendship", "sympathy"],
    62: ["dorothea", "ladislaw", "rosamond", "scene", "jealousy"],
    63: ["bulstrode", "raffles", "return", "past", "fear"],
    64: ["lydgate", "debt", "gambling", "rosamond", "desperation"],
    65: ["lydgate", "rosamond", "quarrel", "house-sale", "resistance"],
    66: ["bulstrode", "raffles", "lydgate", "loan", "compromise"],
    67: ["bulstrode", "raffles", "death", "guilt", "murder"],
    68: ["bulstrode", "scandal", "meeting", "lydgate", "disgrace"],
    69: ["lydgate", "disgrace", "rosamond", "despair", "isolation"],
    70: ["dorothea", "lydgate", "faith", "support", "compassion"],
    71: ["dorothea", "rosamond", "ladislaw", "generosity", "revelation"],
    72: ["dorothea", "night", "grief", "self-reckoning", "dawn"],
    73: ["dorothea", "rosamond", "compassion", "truth", "ladislaw"],
    74: ["lydgate", "farebrother", "bulstrode", "scandal", "clearing"],
    75: ["fred", "mary", "garth", "engagement", "resolution"],
    76: ["dorothea", "ladislaw", "proposal", "love", "storm"],
    77: ["dorothea", "ladislaw", "engagement", "celia", "reaction"],
    78: ["dorothea", "chettam", "family", "objections", "resolve"],
    79: ["caleb-garth", "bulstrode", "stone-court", "departure"],
    80: ["farebrother", "fred", "mary", "garth", "resolution"],
    81: ["fred", "mary", "garth", "love", "understanding"],
    82: ["dorothea", "brooke", "family", "ladislaw", "acceptance"],
    83: ["fred", "mary", "garth", "engagement", "happiness"],
    84: ["lydgate", "rosamond", "departure", "middlemarch", "compromise"],
    85: ["dorothea", "ladislaw", "marriage", "departure", "beginning"],
    86: ["fred", "mary", "wedding", "garth", "happiness"],
    87: ["finale", "after-years", "marriages", "dorothea", "legacy"],  # Finale
}

# Chapter titles (brief descriptive names)
CHAPTER_TITLES = {
    0: "Prelude",
    1: "Miss Brooke",
    2: "Casaubon Courts Dorothea",
    3: "The Proposal",
    4: "Mr. Brooke's Opinions",
    5: "Engagement Plans",
    6: "Will Ladislaw Introduced",
    7: "Dorothea's Farewell to Celia",
    8: "Rome and Disillusionment",
    9: "Dorothea's Tears in Rome",
    10: "Ladislaw and Naumann",
    11: "Lydgate Arrives",
    12: "The Vincy Family",
    13: "Fred and Featherstone",
    14: "Fred's Debt",
    15: "Lydgate's Ambition",
    16: "The Hospital Question",
    17: "Mr. Farebrother",
    18: "Casaubon's Marriage",
    19: "Dorothea Meets Ladislaw Again",
    20: "Art and Feeling in Rome",
    21: "Return from Rome",
    22: "Lydgate Meets Rosamond",
    23: "Fred and Featherstone's Illness",
    24: "Fred's Disgrace",
    25: "Mary Garth's Vigil",
    26: "The Chaplain Vote",
    27: "Dorothea's Unhappy Marriage",
    28: "The First Quarrel",
    29: "Casaubon's Jealousy",
    30: "Lydgate and Rosamond",
    31: "An Impulsive Engagement",
    32: "Featherstone's Funeral",
    33: "The Two Wills",
    34: "The Disappointed Heir",
    35: "The Lydgate-Vincy Alliance",
    36: "Lydgate's Wedding",
    37: "Ladislaw Visits Lowick",
    38: "Casaubon's Prohibition",
    39: "The Codicil",
    40: "Caleb Garth's Work",
    41: "The Midnight Promise",
    42: "Casaubon's Death",
    43: "Dorothea's Widowhood",
    44: "The Will Revealed",
    45: "Raffles Appears",
    46: "Ladislaw in Middlemarch",
    47: "Dorothea and Ladislaw Meet",
    48: "Farebrother and Reform",
    49: "The Passionate Renunciation",
    50: "Lydgate's Financial Trouble",
    51: "The House on Lowick Gate",
    52: "Lydgate and Bulstrode",
    53: "Bulstrode's Past",
    54: "Dorothea and Brooke",
    55: "Dorothea and Ladislaw Again",
    56: "The Lydgate Marriage",
    57: "Fred and the Garths",
    58: "Rosamond and Ladislaw",
    59: "Ladislaw's Fury",
    60: "Fred, Mary, and Farebrother",
    61: "Dorothea and Rosamond",
    62: "The Painful Discovery",
    63: "Raffles Returns",
    64: "Lydgate Gambles",
    65: "Rosamond's Resistance",
    66: "Bulstrode's Loan",
    67: "The Death of Raffles",
    68: "The Town Meeting",
    69: "Lydgate's Despair",
    70: "Dorothea's Faith in Lydgate",
    71: "Dorothea Visits Rosamond",
    72: "Dorothea's Dark Night",
    73: "The Second Visit",
    74: "Lydgate and Farebrother",
    75: "Fred and Mary Resolved",
    76: "The Storm and the Declaration",
    77: "Dorothea's Announcement",
    78: "The Family Reacts",
    79: "Bulstrode's Departure",
    80: "Farebrother's Sacrifice",
    81: "Fred and Mary's Understanding",
    82: "Mr. Brooke Accepts",
    83: "The Garth Engagement",
    84: "Lydgate and Rosamond Depart",
    85: "Dorothea and Ladislaw Married",
    86: "Fred and Mary's Wedding",
    87: "Finale",
}


# Book groupings for L2
BOOK_GROUPS = [
    {
        "id": "book-i-miss-brooke",
        "name": "Book I: Miss Brooke",
        "chapter_nums": list(range(1, 13)),
        "about": "Dorothea Brooke, ardent and idealistic, yearns for a life of great purpose. She rejects the suitable Sir James Chettam and accepts the elderly scholar Casaubon, believing his life's work — the Key to All Mythologies — will give her the epic vocation she craves. Meanwhile, the ambitious young physician Tertius Lydgate arrives in Middlemarch with grand plans for medical reform. The two central marriages begin: one a catastrophic mismatch, the other a slow-forming trap.",
        "for_readers": "The opening book introduces Eliot's method: she places you inside Dorothea's consciousness so completely that Casaubon's proposal feels inevitable — and then shows you, through every other character's reaction, how clearly wrong it is. Chapter 8 (the honeymoon in Rome) is one of the most devastating chapters in English fiction.",
    },
    {
        "id": "book-ii-old-and-young",
        "name": "Book II: Old and Young",
        "chapter_nums": list(range(13, 23)),
        "about": "The world of Middlemarch expands. Fred Vincy, charming and irresponsible, circles around his expected inheritance from old Peter Featherstone. Lydgate encounters the beautiful Rosamond Vincy. Dorothea, on her miserable honeymoon in Rome, meets her husband's young cousin Will Ladislaw — bright, warm, and everything Casaubon is not. The generational conflict intensifies: the old order (Featherstone, Casaubon, Bulstrode) grips its power while the young struggle against constraint.",
        "for_readers": "This book weaves together the novel's four major plot lines for the first time. Notice how Eliot uses parallel structure: Dorothea trapped in a cold marriage and Lydgate falling into an attraction that will become its own kind of trap. Fred's comic misadventures with money foreshadow Lydgate's later, more tragic financial entanglement.",
    },
    {
        "id": "book-iii-waiting-for-death",
        "name": "Book III: Waiting for Death",
        "chapter_nums": list(range(23, 34)),
        "about": "Featherstone lies dying, and the whole community waits — for his money. Fred's debt to Caleb Garth comes due, spreading consequences through the Garth family. Lydgate, entangled with Rosamond, finds himself engaged almost by accident. Dorothea and Casaubon quarrel for the first time; he suspects her growing sympathy for Ladislaw. Death arrives: Featherstone's, in one of the novel's great set-pieces. His will shocks everyone.",
        "for_readers": "The title's ambiguity is deliberate — everyone is waiting for someone's death, for different reasons. Mary Garth's vigil at Featherstone's deathbed (Chapter 25) is morally luminous: she refuses to burn his second will, making the most consequential decision by doing nothing. Lydgate's engagement scene (Chapter 31) shows how 'the moment of vocation' can be lost through a single impulse.",
    },
    {
        "id": "book-iv-three-love-problems",
        "name": "Book IV: Three Love Problems",
        "chapter_nums": list(range(34, 43)),
        "about": "Three couples, three kinds of difficulty. Fred Vincy must find a vocation worthy of Mary Garth. Lydgate and Rosamond marry and immediately begin the slow, terrible collision of incompatible expectations. Dorothea lives under the shadow of Casaubon's codicil — his will strips her of her inheritance if she marries Ladislaw, revealing his jealousy from beyond the grave. The dead hand reaches out to control the living.",
        "for_readers": "Chapter 42 — Casaubon's death — is the novel's structural center. But the real drama is the midnight scene before it (Chapter 41), where Dorothea struggles to promise Casaubon she will carry out his wishes, not knowing what they are. This is Eliot at her most morally searching: the cost of duty, the weight of promises, the way love dies before the body does.",
    },
    {
        "id": "book-v-the-dead-hand",
        "name": "Book V: The Dead Hand",
        "chapter_nums": list(range(43, 53)),
        "about": "Casaubon's codicil is revealed, and its public humiliation binds Dorothea and Ladislaw more tightly than any declaration could. Bulstrode's past begins to surface with the arrival of Raffles, who knows the banker's hidden history. Lydgate's marriage erodes under financial pressure — Rosamond's expectations of gentility collide with his scientific idealism. The dead hands of the past — Casaubon's will, Bulstrode's secret, Featherstone's money — tighten their grip on the living.",
        "for_readers": "The passionate scene between Dorothea and Ladislaw in Chapter 49 is extraordinary — a declaration of love that is also a renunciation, because the codicil has made their attachment shameful in the eyes of the world. Notice how Eliot parallels this with Lydgate's entrapment: both characters discover that the structures of their world constrain even their most generous impulses.",
    },
    {
        "id": "book-vi-the-widow-and-the-wife",
        "name": "Book VI: The Widow and the Wife",
        "chapter_nums": list(range(53, 63)),
        "about": "Dorothea the widow and Rosamond the wife: two women on diverging paths. Dorothea uses her freedom tentatively, reaching toward Ladislaw but constrained by propriety and the codicil. Rosamond's marriage to Lydgate deteriorates into mutual incomprehension — she flirts with Ladislaw, Lydgate withdraws into bitter silence. Fred Vincy's story offers quiet hope: under Caleb Garth's guidance, he finds meaningful work. The threads tangle as Dorothea discovers Rosamond and Ladislaw together.",
        "for_readers": "This book contains some of the novel's finest psychological writing. Lydgate's gradual capitulation to Rosamond (especially Chapter 56) is a masterclass in how relationships fail: not through dramatic betrayal but through daily erosion of respect. Dorothea's visit to Rosamond (Chapter 61) is the novel's first gesture toward the redemptive compassion that will resolve everything.",
    },
    {
        "id": "book-vii-two-temptations",
        "name": "Book VII: Two Temptations",
        "chapter_nums": list(range(63, 72)),
        "about": "The moral crises converge. Lydgate, desperate for money, is tempted to accept Bulstrode's tainted loan. Bulstrode, cornered by Raffles's blackmail, is tempted to let the sick man die — and possibly hastens his death. The town meeting that follows destroys both men's reputations. Lydgate finds himself guilty by association, and only Dorothea believes in his innocence. These chapters are the novel's moral furnace.",
        "for_readers": "Chapter 67 — the death of Raffles — is Eliot's most morally complex achievement. Did Bulstrode murder him? The text refuses a simple answer. What it shows is the terrible process by which a man of genuine religious feeling can rationalize an act of will into an act of God. Dorothea's faith in Lydgate (Chapter 70) is the counterweight: compassion based on clear moral vision, not sentimentality.",
    },
    {
        "id": "book-viii-sunset-and-sunrise",
        "name": "Book VIII: Sunset and Sunrise",
        "chapter_nums": list(range(72, 87)),
        "about": "The long resolution. Dorothea endures her dark night of the soul (Chapter 72) and emerges transformed — choosing to visit Rosamond again, to trust in Ladislaw's love despite what she saw. Rosamond, for once in her life, tells the truth. Fred and Mary find their quiet happiness. Dorothea and Ladislaw declare their love in a thunderstorm. The novel closes with the Finale's meditation on 'unhistoric acts' — the growing good of the world depends on those who live faithfully a hidden life.",
        "for_readers": "Chapter 72 is the novel's emotional climax — Dorothea alone, weeping through the night, then choosing at dawn to go out into the world again. Chapter 76, the proposal scene in the storm, is Eliot's most romantic moment. But the Finale is what makes Middlemarch transcendent: its vision of ordinary goodness as the ground of civilization. 'The growing good of the world is partly dependent on unhistoric acts.'",
    },
]

# Thematic threads for L2
THEMATIC_THREADS = [
    {
        "id": "theme-dorothea-vocation",
        "name": "Dorothea's Vocation: The New Theresa",
        "chapter_nums": [1, 2, 3, 5, 8, 9, 19, 20, 21, 27, 28, 37, 39, 41, 42, 43, 44, 47, 49, 55, 62, 70, 71, 72, 73, 76, 77, 85],
        "about": "The novel's central thread: Dorothea Brooke's search for a life of meaningful action. From the Prelude's invocation of Saint Theresa through Dorothea's catastrophic first marriage to Casaubon, her painful widowhood, and her choice of Will Ladislaw, Eliot traces how a woman of 'great soul' navigates a world that offers her no epic stage. Dorothea's vocation turns out to be not scholarship or reform but something harder to name — the capacity to extend compassion that changes everyone it touches.",
        "for_readers": "Read these chapters as a sequence and you see the architecture of the novel: Dorothea moves from aspiration (Book I) through disillusionment (Rome) and grief (Casaubon's death) to a different kind of greatness. Her dark night of the soul (Chapter 72) echoes the Prelude's Theresa — but instead of reforming a religious order, Dorothea reforms the moral life around her through individual acts of sympathy. This is what Gottman would call 'turning toward' on a civilizational scale.",
    },
    {
        "id": "theme-lydgate-rosamond",
        "name": "Lydgate and Rosamond: A Marriage of Misperception",
        "chapter_nums": [11, 15, 16, 22, 26, 30, 31, 36, 50, 51, 52, 56, 58, 64, 65, 66, 69, 74, 84],
        "about": "The novel's most painful storyline: Lydgate's brilliant medical ambitions destroyed by an ill-chosen marriage. He and Rosamond each marry a fantasy — she wants a gentleman, he wants a decorative wife who won't interfere. Every scene between them is a study in Gottman's 'Four Horsemen': criticism, contempt, defensiveness, stonewalling. Rosamond's quiet, inflexible will defeats Lydgate's every attempt at honest communication. He dies at fifty, 'what is called a successful man,' having abandoned every dream.",
        "for_readers": "This thread is the most modern thing in the novel. Lydgate and Rosamond don't fail through villainy or dramatic betrayal — they fail through daily misattunement. Notice how Eliot shows both perspectives with equal sympathy: Rosamond isn't a monster, she's a woman educated to want exactly the wrong things. Lydgate isn't weak, he's a man who applied his intelligence to everything except his own emotional life. Gottman's research confirms what Eliot intuited: marriages die from accumulated small failures to respond to bids for connection.",
    },
    {
        "id": "theme-money-vocation",
        "name": "Money, Work, and Vocation",
        "chapter_nums": [13, 14, 23, 24, 25, 32, 33, 34, 40, 45, 50, 51, 52, 57, 63, 64, 66, 67, 75, 79, 83],
        "about": "Money flows through Middlemarch like blood — sometimes nourishing, sometimes poisonous. Featherstone's contested will, Fred's debts, Lydgate's financial collapse, Bulstrode's tainted wealth — every character's moral fate is entangled with economics. Against these corruptions, Caleb Garth represents the dignity of honest work. Fred's redemption comes not through inheritance but through learning to labor. The novel insists that how one earns and spends reveals who one is.",
        "for_readers": "Follow the money and you see the novel's moral map. Featherstone's two wills in Chapter 33 dramatize how wealth distorts community. Fred's journey from debt to honest farming (guided by Caleb Garth) is the novel's quiet success story. Lydgate's descent from scientific idealism to fashionable practice is its tragedy. Bulstrode's wealth, built on fraud, eventually poisons everything it touches. Eliot understood something Adam Smith knew: economics is a moral science.",
    },
    {
        "id": "theme-knowledge-illusion",
        "name": "Knowledge and Illusion",
        "chapter_nums": [2, 3, 8, 10, 15, 18, 20, 27, 29, 37, 38, 43, 44, 46, 48, 53, 54, 68, 70, 71, 73],
        "about": "Middlemarch is a novel about knowing and not-knowing. Casaubon's Key to All Mythologies represents scholarship as self-deception — a life's work that was outdated before it began. Lydgate's medical research represents genuine intellectual ambition brought low by social blindness. Dorothea's journey is from the illusion that knowledge comes from books to the understanding that wisdom is attention to particular lives. The novel's great insight: we see others most clearly when we acknowledge our own blindness.",
        "for_readers": "Eliot was one of the most learned novelists who ever lived, and she uses that learning to interrogate learning itself. Casaubon's failure is not intellectual but emotional: he cannot bear to be seen, especially by someone who loves him. Lydgate's medical vision is genuinely advanced, but he's blind to the social web he inhabits. Dorothea's education happens not in libraries but in moments of encounter — Rome, the midnight scene, the night of weeping. Real knowledge, Eliot suggests, is the capacity to imagine another person's inner life.",
    },
    {
        "id": "theme-reform-community",
        "name": "Reform and Community",
        "chapter_nums": [4, 11, 16, 17, 26, 40, 46, 48, 54, 68, 74, 78, 79, 82],
        "about": "Middlemarch is set in 1829-1832, during the Reform Bill crisis — the great political upheaval that reshaped English society. But Eliot is more interested in how reform works at the local level: Lydgate's hospital reform, Brooke's bumbling political campaign, Ladislaw's journalism, Dorothea's quiet influence. Every reformer is compromised by the community they try to change. The novel's conclusion is not cynical but realistic: genuine reform happens through 'unhistoric acts,' not grand gestures.",
        "for_readers": "The political background isn't decoration — it's the novel's deepest theme. Every character is a would-be reformer: Dorothea wants to build cottages, Lydgate wants to advance medicine, Brooke wants to enter Parliament, Ladislaw wants to change public opinion. Each discovers that reform requires navigating existing power, accepting imperfect allies, and enduring the community's resistance. Caleb Garth, who simply does good work, may be the most effective reformer of all.",
    },
    {
        "id": "theme-women-constraint",
        "name": "Women and Constraint",
        "chapter_nums": [1, 5, 7, 8, 9, 22, 27, 35, 43, 44, 56, 58, 61, 62, 65, 71, 72, 73, 77, 78, 85],
        "about": "From the Prelude's 'many Theresas' to the Finale's 'unvisited tombs,' Middlemarch is fundamentally about the constraint of women's lives. Dorothea's ardent nature finds no adequate channel; Rosamond's education produces only a decorative will; Mary Garth's intelligence is confined to domestic virtue; even Celia, content with her lot, represents a narrowing of possibility. Eliot shows how social structures — marriage law, inheritance, education, propriety — shape women's fates as powerfully as individual character.",
        "for_readers": "Read the women of Middlemarch together and you see a spectrum of responses to the same fundamental constraint. Dorothea rebels through aspiration, Rosamond through willful manipulation, Mary through patient integrity, Mrs. Bulstrode through silent loyalty. None of them gets what they fully deserve. The novel's compassion extends even to Rosamond, whose worst qualities are precisely what her education trained her for. This is the thread that connects most directly to the Prelude's question: what becomes of a Saint Theresa born into a world with no convent to reform?",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)

    # Find the PRELUDE heading (the actual one, not the TOC entry)
    # TOC has " PRELUDE." with leading space, actual heading is "PRELUDE." flush left
    match = re.search(r'^PRELUDE\.\s*$', text, re.MULTILINE)
    if match:
        text = text[match.start():]

    parsed = parse_text(text)
    print(f"Parsed {len(parsed)} items (prelude + chapters + finale)")

    chapters = [p for p in parsed if p['type'] == 'chapter']
    print(f"  Chapters: {len(chapters)}")

    items = []
    sort_order = 0

    # L1: Prelude
    prelude = [p for p in parsed if p['type'] == 'prelude']
    if prelude:
        sort_order += 1
        items.append({
            "id": "prelude",
            "name": "Prelude",
            "sort_order": sort_order,
            "level": 1,
            "category": "prelude",
            "sections": {
                "Text": prelude[0]['text'],
            },
            "keywords": CHAPTER_KEYWORDS.get(0, ["prelude"]),
            "metadata": {}
        })
        print(f"  Prelude: {len(prelude[0]['text'])} chars")

    # L1: Chapters
    for ch in chapters:
        n = ch['num']
        chapter_id = make_chapter_id(n)
        sort_order += 1
        title = CHAPTER_TITLES.get(n, f"Chapter {n}")
        keywords = CHAPTER_KEYWORDS.get(n, ["middlemarch", "eliot"])

        items.append({
            "id": chapter_id,
            "name": f"Chapter {n}: {title}",
            "sort_order": sort_order,
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": ch['text'],
            },
            "keywords": keywords,
            "metadata": {
                "chapter_number": n,
            }
        })
        print(f"  Ch {n:2d}: {title} ({len(ch['text'])} chars)")

    # L1: Finale
    finale = [p for p in parsed if p['type'] == 'finale']
    if finale:
        sort_order += 1
        items.append({
            "id": "finale",
            "name": "Finale",
            "sort_order": sort_order,
            "level": 1,
            "category": "finale",
            "sections": {
                "Text": finale[0]['text'],
            },
            "keywords": CHAPTER_KEYWORDS.get(87, ["finale"]),
            "metadata": {}
        })
        print(f"  Finale: {len(finale[0]['text'])} chars")

    # L2: Book groupings
    all_book_ids = []
    for bg in BOOK_GROUPS:
        sort_order += 1
        book_id = bg["id"]
        all_book_ids.append(book_id)
        chapter_ids = [make_chapter_id(n) for n in bg["chapter_nums"]]

        items.append({
            "id": book_id,
            "name": bg["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "book",
            "relationship_type": "emergence",
            "composite_of": chapter_ids,
            "sections": {
                "About": bg["about"],
                "For Readers": bg["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "chapter_count": len(bg["chapter_nums"]),
            }
        })

    # L2: Thematic threads
    all_theme_ids = []
    for theme in THEMATIC_THREADS:
        sort_order += 1
        theme_id = theme["id"]
        all_theme_ids.append(theme_id)
        chapter_ids = [make_chapter_id(n) for n in theme["chapter_nums"]]

        items.append({
            "id": theme_id,
            "name": theme["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": chapter_ids,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "chapter_count": len(theme["chapter_nums"]),
            }
        })

    # L3: Meta-categories
    sort_order += 1
    items.append({
        "id": "middlemarch-complete",
        "name": "Middlemarch: A Study of Provincial Life",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_book_ids,
        "sections": {
            "About": "George Eliot's Middlemarch (1871-72) is widely regarded as the greatest English novel. Set in the fictional Midlands town of Middlemarch during the years 1829-1832, it weaves together four main plots: Dorothea Brooke's disastrous first marriage to the scholar Casaubon and her gradual awakening to love and purpose; Tertius Lydgate's brilliant medical ambitions undermined by his marriage to the beautiful, willful Rosamond Vincy; Fred Vincy's journey from irresponsible heir-in-waiting to honest farmer, guided by his love for Mary Garth; and the banker Bulstrode's hidden past catching up with him. Through these interlocking stories, Eliot creates a comprehensive vision of English provincial life — its politics, religion, medicine, marriage, money, and moral texture. The novel's method is radical sympathy: every character, even the most flawed, is understood from inside.",
            "For Readers": "Middlemarch is long but never slow. It can be read as a love story (Dorothea and Ladislaw), a cautionary tale (Lydgate and Rosamond), a mystery (Bulstrode's past), or a social panorama — but it is most truly a novel about how difficult it is to do good in an imperfect world. Virginia Woolf called it 'one of the few English novels written for grown-up people.' The eight books create a natural rhythm: each has a distinct title and emotional arc. The Prelude and Finale frame the whole as a meditation on the lives of women — 'many Theresas' whose greatness the world cannot see.",
        },
        "keywords": ["middlemarch", "eliot", "novel", "provincial-life", "marriage", "vocation", "reform"],
        "metadata": {}
    })

    sort_order += 1
    items.append({
        "id": "middlemarch-thematic-arcs",
        "name": "Thematic Arcs of Middlemarch",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "Six thematic threads run through Middlemarch, each illuminating a different dimension of Eliot's moral vision. Dorothea's Vocation traces the Prelude's 'new Theresa' through disillusionment to a different kind of greatness. The Lydgate-Rosamond Marriage is the novel's most modern story — a clinical study of how two people of intelligence and beauty can destroy each other's happiness through daily misattunement. Money, Work, and Vocation maps how economic life shapes moral character. Knowledge and Illusion explores the gap between learning and wisdom. Reform and Community tests idealism against the stubborn reality of provincial society. Women and Constraint frames the entire novel as a study of how social structures limit human possibility.",
            "For Readers": "These themes interpenetrate at every point. Dorothea's vocation is constrained by her gender; Lydgate's marriage fails because of his blindness about money and social expectation; Bulstrode's wealth corrupts reform; Fred's redemption comes through honest work. Reading across themes reveals the novel's web-like structure — what Eliot called 'the stealthy convergence of human lots.' No character exists in isolation; every choice ripples outward through the community.",
        },
        "keywords": ["themes", "analysis", "vocation", "marriage", "money", "knowledge", "reform", "women"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "George Eliot (Mary Ann Evans)",
                    "date": "1871-1872",
                    "note": "Author"
                }
            ]
        },
        "name": "Middlemarch",
        "description": "George Eliot's Middlemarch (1871-72) — widely considered the greatest English novel. Set in a fictional Midlands town during the Reform Bill era (1829-1832), it weaves together the stories of Dorothea Brooke, the ambitious physician Lydgate, the feckless Fred Vincy, and the haunted banker Bulstrode into a comprehensive vision of provincial life. Eighty-six chapters across eight named books, framed by a Prelude invoking Saint Theresa and a Finale meditating on 'unhistoric acts.' Virginia Woolf called it 'one of the few English novels written for grown-up people.'\n\nSource: Project Gutenberg eBook #145 (https://www.gutenberg.org/ebooks/145)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: W. E. F. Britten's illustrations for the 1910 Everyman's Library edition of Middlemarch. Hugh Thomson's decorative headpieces. Photographs and engravings of Coventry and Warwickshire (Eliot's model for Middlemarch) from the 1830s-1870s. George Richmond's chalk portrait of George Eliot (1849).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["novel", "realism", "provincial-life", "marriage", "british-literature", "victorian", "public-domain", "full-text"],
        "roots": ["emotion-love"],
        "shelves": ["mirror"],
        "lineages": ["Gottman"],
        "worldview": "realist",
        "items": items,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1: {l1} (prelude + chapters + finale), L2: {l2} (books + themes), L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
