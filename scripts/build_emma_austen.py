#!/usr/bin/env python3
"""
Build grammar.json for Emma by Jane Austen.

Source: Project Gutenberg eBook #158
Author: Jane Austen (1815)

Structure:
- L1: 55 chapters (numbered sequentially across 3 volumes)
- L2: Volume groupings (3) + Thematic threads (6)
- L3: Meta-categories (The Complete Novel, Thematic Arcs)

Emma has 3 volumes with chapters numbered I-XVIII, I-XVIII, I-XIX respectively.
We renumber them sequentially 1-55 for the grammar.
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "emma-austen.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "emma-austen"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Volume structure: (volume_num, chapter_count)
VOLUMES = [
    (1, 18),  # Volume I: Chapters 1-18
    (2, 18),  # Volume II: Chapters 19-36
    (3, 19),  # Volume III: Chapters 37-55
]

# Roman numeral conversion
ROMAN_MAP = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
    'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
    'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
    'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19,
}


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


def parse_chapters(text):
    """Parse Emma into 55 chapters across 3 volumes."""
    chapters = []

    # Find all VOLUME and CHAPTER markers with their positions
    # First, find volume boundaries
    volume_positions = []
    for match in re.finditer(r'^VOLUME\s+(I{1,3})\s*$', text, re.MULTILINE):
        vol_num = ROMAN_MAP[match.group(1)]
        volume_positions.append((vol_num, match.start()))

    # Find all chapter markers
    chapter_positions = []
    for match in re.finditer(r'^CHAPTER\s+([IVXL]+)\s*$', text, re.MULTILINE):
        roman = match.group(1)
        if roman in ROMAN_MAP:
            ch_num = ROMAN_MAP[roman]
            chapter_positions.append((ch_num, match.start(), match.end()))

    # Assign chapters to volumes
    global_chapter = 0
    for vol_idx, (vol_num, vol_start) in enumerate(volume_positions):
        # Get next volume start (or end of text)
        if vol_idx + 1 < len(volume_positions):
            vol_end = volume_positions[vol_idx + 1][1]
        else:
            vol_end = len(text)

        # Find chapters within this volume
        vol_chapters = [(cn, cs, ce) for cn, cs, ce in chapter_positions
                        if cs >= vol_start and cs < vol_end]

        for ch_idx, (ch_num, ch_start, ch_end) in enumerate(vol_chapters):
            global_chapter += 1

            # Chapter text starts after the CHAPTER heading
            text_start = ch_end

            # Chapter text ends at next chapter start, next volume, or end of text
            if ch_idx + 1 < len(vol_chapters):
                text_end = vol_chapters[ch_idx + 1][1]
            elif vol_idx + 1 < len(volume_positions):
                text_end = volume_positions[vol_idx + 1][1]
            else:
                text_end = len(text)

            chapter_text = text[text_start:text_end].strip()
            # Clean up excessive newlines
            chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)

            chapters.append({
                'volume': vol_num,
                'chapter_in_vol': ch_num,
                'global_chapter': global_chapter,
                'text': chapter_text,
            })

    return chapters


def make_chapter_id(global_num):
    """Create chapter ID like 'chapter-1', 'chapter-2'."""
    return f"chapter-{global_num}"


def extract_first_sentence(text, max_len=150):
    """Extract the first sentence for a summary."""
    clean = ' '.join(text.split())
    # Remove italic markers
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


# Chapter titles/descriptions for Emma's 55 chapters
CHAPTER_INFO = {
    1: {"title": "Emma Woodhouse", "keywords": ["emma", "woodhouse", "miss-taylor", "marriage", "matchmaking"]},
    2: {"title": "Mr. Weston's Marriage", "keywords": ["weston", "taylor", "marriage", "highbury", "society"]},
    3: {"title": "Mr. Woodhouse's Fears", "keywords": ["woodhouse", "father", "hypochondria", "gruel", "comfort"]},
    4: {"title": "Harriet Smith", "keywords": ["harriet", "smith", "friendship", "school", "influence"]},
    5: {"title": "Emma and Mr. Knightley Disagree", "keywords": ["knightley", "emma", "debate", "harriet", "judgment"]},
    6: {"title": "Mrs. Goddard's School", "keywords": ["harriet", "elton", "courtship", "drawing", "portrait"]},
    7: {"title": "Harriet's Suitor", "keywords": ["harriet", "martin", "proposal", "letter", "class"]},
    8: {"title": "Mr. Martin's Proposal Refused", "keywords": ["martin", "harriet", "refusal", "knightley", "anger"]},
    9: {"title": "Mr. Elton's Attentions", "keywords": ["elton", "charade", "courtship", "riddle", "misunderstanding"]},
    10: {"title": "Emma's Portrait of Harriet", "keywords": ["portrait", "painting", "elton", "flattery", "vanity"]},
    11: {"title": "The Martins Visit", "keywords": ["martin", "visit", "harriet", "class", "awkwardness"]},
    12: {"title": "Mr. Knightley's Warning", "keywords": ["knightley", "emma", "harriet", "elton", "warning"]},
    13: {"title": "The Westons' Dinner", "keywords": ["dinner", "weston", "society", "christmas", "perry"]},
    14: {"title": "Christmas Eve at Randalls", "keywords": ["christmas", "randalls", "dinner", "snow", "party"]},
    15: {"title": "Mr. Elton's Proposal", "keywords": ["elton", "proposal", "carriage", "shock", "rejection"]},
    16: {"title": "Emma's Mortification", "keywords": ["emma", "shame", "misjudgment", "harriet", "elton"]},
    17: {"title": "Telling Harriet", "keywords": ["harriet", "heartbreak", "confession", "friendship", "comfort"]},
    18: {"title": "Frank Churchill Expected", "keywords": ["frank-churchill", "anticipation", "weston", "visit", "mystery"]},
    19: {"title": "Emma and Frank Meet", "keywords": ["frank", "emma", "first-meeting", "charm", "impression"]},
    20: {"title": "Jane Fairfax Discussed", "keywords": ["jane-fairfax", "gossip", "talent", "reserve", "mystery"]},
    21: {"title": "Frank's Flirtation", "keywords": ["frank", "emma", "flirtation", "ball", "charm"]},
    22: {"title": "Mrs. Elton Arrives", "keywords": ["elton", "augusta", "bride", "vulgar", "pretension"]},
    23: {"title": "Mrs. Elton's Patronage", "keywords": ["mrs-elton", "patronage", "jane-fairfax", "snobbery", "offense"]},
    24: {"title": "The Coles' Dinner", "keywords": ["dinner", "coles", "piano", "jane-fairfax", "society"]},
    25: {"title": "The Pianoforte Mystery", "keywords": ["piano", "jane-fairfax", "gift", "mystery", "speculation"]},
    26: {"title": "Frank and Emma at the Coles'", "keywords": ["frank", "emma", "flirtation", "coles", "jane"]},
    27: {"title": "Emma Visits Jane Fairfax", "keywords": ["emma", "jane", "visit", "reserve", "suspicion"]},
    28: {"title": "The Ball at the Crown", "keywords": ["ball", "crown", "dancing", "frank", "society"]},
    29: {"title": "Frank's Temper", "keywords": ["frank", "temper", "haircut", "emma", "restlessness"]},
    30: {"title": "Jane's Distress", "keywords": ["jane", "illness", "letters", "post-office", "secret"]},
    31: {"title": "Frank Leaves Suddenly", "keywords": ["frank", "departure", "aunt-churchill", "disappointment", "mystery"]},
    32: {"title": "Mr. Elton Returns with His Bride", "keywords": ["elton", "mrs-elton", "bride", "harriet", "humiliation"]},
    33: {"title": "Mrs. Elton's Airs", "keywords": ["mrs-elton", "pretension", "knightley", "snobbery", "maple-grove"]},
    34: {"title": "The Ball Planned", "keywords": ["ball", "crown", "planning", "frank", "return"]},
    35: {"title": "Frank Returns", "keywords": ["frank", "return", "emma", "flirtation", "renewal"]},
    36: {"title": "The Ball at the Crown", "keywords": ["ball", "harriet", "knightley", "dancing", "elton-snub"]},
    37: {"title": "Harriet's Rescue", "keywords": ["harriet", "gypsies", "frank", "rescue", "adventure"]},
    38: {"title": "Harriet's New Attachment", "keywords": ["harriet", "attachment", "hero", "misunderstanding", "secret"]},
    39: {"title": "Frank and Emma", "keywords": ["frank", "emma", "flirtation", "word-game", "suspicion"]},
    40: {"title": "Mr. Knightley Suspects", "keywords": ["knightley", "frank", "jane", "suspicion", "observation"]},
    41: {"title": "An Awkward Gathering", "keywords": ["party", "tension", "jane", "frank", "unease"]},
    42: {"title": "Donwell Abbey", "keywords": ["donwell", "knightley", "strawberries", "mrs-elton", "england"]},
    43: {"title": "Box Hill", "keywords": ["box-hill", "picnic", "cruelty", "miss-bates", "humiliation"]},
    44: {"title": "Knightley's Rebuke", "keywords": ["knightley", "rebuke", "emma", "miss-bates", "tears"]},
    45: {"title": "Emma's Penance", "keywords": ["emma", "repentance", "miss-bates", "visit", "kindness"]},
    46: {"title": "Frank's Secret Revealed", "keywords": ["frank", "jane", "engagement", "secret", "revelation"]},
    47: {"title": "Emma Reflects", "keywords": ["emma", "reflection", "self-knowledge", "love", "knightley"]},
    48: {"title": "Harriet's Confession", "keywords": ["harriet", "knightley", "love", "confession", "shock"]},
    49: {"title": "Mr. Knightley Proposes", "keywords": ["knightley", "proposal", "emma", "love", "happiness"]},
    50: {"title": "The Engagement", "keywords": ["engagement", "knightley", "emma", "father", "living-arrangements"]},
    51: {"title": "Harriet and Mr. Martin", "keywords": ["harriet", "martin", "proposal", "acceptance", "resolution"]},
    52: {"title": "Frank's Letter", "keywords": ["frank", "letter", "explanation", "jane", "apology"]},
    53: {"title": "Mrs. Weston's News", "keywords": ["weston", "baby", "news", "happiness", "resolution"]},
    54: {"title": "All Resolved", "keywords": ["resolution", "forgiveness", "happiness", "community", "reconciliation"]},
    55: {"title": "The Wedding", "keywords": ["wedding", "knightley", "emma", "marriage", "happiness"]},
}

# Volume groupings for L2
VOLUME_GROUPS = [
    {
        "id": "volume-i",
        "name": "Volume I: Matchmaker's Overture",
        "chapters": list(range(1, 19)),
        "about": "Emma Woodhouse, handsome, clever, and rich, sets out to arrange the romantic lives of those around her. She befriends the naive Harriet Smith and attempts to match her with Mr. Elton, blind to Elton's actual designs on Emma herself. Mr. Knightley warns her, but Emma is confident in her own judgment. The volume culminates in the humiliating revelation that Elton wants Emma, not Harriet — Emma's first great miscalculation.",
        "for_readers": "The opening volume establishes Austen's comic vision: a heroine who is wrong about almost everything but impossible not to love. Watch how Emma's matchmaking reveals more about her own psychology than about anyone else's heart. The Elton proposal in the carriage (Chapter 15) is one of the great comic shocks in English fiction.",
    },
    {
        "id": "volume-ii",
        "name": "Volume II: Complications and Concealment",
        "chapters": list(range(19, 37)),
        "about": "The world of Highbury grows more complex with the arrival of Frank Churchill, Jane Fairfax, and Mrs. Elton. Emma flirts with Frank, is irritated by Jane's reserve, and endures Mrs. Elton's vulgar patronage. Beneath the social comedy, secrets multiply: Frank and Jane's hidden engagement, Harriet's shifting affections, and Emma's growing but unacknowledged feelings for Mr. Knightley. The great ball at the Crown Inn is the volume's centerpiece.",
        "for_readers": "This is Austen's most intricate plotting. On a first reading, you share Emma's bafflement at Jane Fairfax's behavior. On rereading, every scene between Frank and Jane crackles with hidden meaning. Mrs. Elton (arriving in Chapter 22) is Austen's most devastating comic creation — a masterclass in social pretension.",
    },
    {
        "id": "volume-iii",
        "name": "Volume III: Recognition and Marriage",
        "chapters": list(range(37, 56)),
        "about": "The comic machinery moves toward crisis. The Box Hill picnic (Chapter 43) is the novel's turning point — Emma's cruel wit wounds Miss Bates, and Mr. Knightley's rebuke forces her first real moment of self-knowledge. Frank and Jane's secret engagement is revealed, Harriet confesses her love for Knightley, and Emma finally recognizes what her heart has known all along. The novel resolves in a cascade of marriages — the right people finding each other at last.",
        "for_readers": "Volume III is where comedy deepens into moral drama. The Box Hill scene is devastating because we see Emma at her worst, and Knightley's 'Badly done, Emma' carries the weight of genuine love. Emma's self-reckoning in Chapters 47-48 is among the finest psychological writing of the nineteenth century. The proposal scene is Austen at her most tender.",
    },
]

# Thematic threads for L2
THEMATIC_THREADS = [
    {
        "id": "theme-matchmaking-misjudgment",
        "name": "Matchmaking and Misjudgment",
        "chapters": [1, 4, 5, 7, 8, 9, 10, 12, 15, 16, 17, 38, 48, 51],
        "about": "The novel's central arc: Emma's compulsion to arrange other people's love lives, and the disasters that follow. From her early confidence in matching Harriet with Elton, through the humiliation of Elton's misdirected proposal, to the final revelation that Harriet loves Knightley — each attempt at matchmaking reveals Emma's blindness to the real movements of the heart. Austen shows how the desire to control others' stories is really a way of avoiding one's own.",
        "for_readers": "Trace how each matchmaking scheme reflects Emma's own emotional state. She pushes Harriet toward Elton because she herself doesn't want Elton. She encourages Harriet's attachment to Frank because she isn't truly attached to Frank herself. The pattern breaks only when Harriet threatens Emma's own happiness — and that's the moment Emma finally sees clearly. This is Gottman's 'turning toward' in fictional form: the relationships that work are the ones where people actually attend to each other rather than to their fantasies.",
    },
    {
        "id": "theme-class-mobility",
        "name": "Class and Social Standing",
        "chapters": [4, 7, 8, 11, 22, 23, 32, 33, 36, 42, 43, 51],
        "about": "Highbury is a small world with rigid social hierarchies, and Emma is its self-appointed queen. The novel maps every gradation: the Woodhouses at the top, the Eltons climbing, the Martins respectable but 'beneath' Emma's notice, Harriet's unknown parentage making her a social wildcard. Mrs. Elton's arrival exposes the absurdity of these distinctions — she and Emma are mirror images, both wielding social power through patronage. The resolution validates steady worth (the Martins, the Knightleys) over pretension.",
        "for_readers": "Austen is merciless about class anxiety. Notice how Emma's objection to Robert Martin is entirely about status, not character — and how Mr. Knightley sees Martin clearly because he values substance over surface. Mrs. Elton's constant references to Maple Grove and her brother-in-law's barouche-landau are Austen's sharpest satire. The Donwell Abbey chapter (42) quietly proposes an alternative: stewardship over display, rootedness over fashion.",
    },
    {
        "id": "theme-secrecy-revelation",
        "name": "Secrecy and Revelation",
        "chapters": [18, 20, 25, 26, 29, 30, 31, 39, 40, 41, 46, 47, 52],
        "about": "Emma is a novel of hidden things. Frank Churchill and Jane Fairfax conceal their engagement; Emma conceals her growing feelings even from herself; Harriet conceals the object of her new attachment. The mystery of the pianoforte, Frank's sudden departures, Jane's inexplicable distress — all are puzzles whose solutions were visible all along if anyone had looked clearly. The novel's great revelation is not Frank's secret but Emma's: she loves Knightley, and has loved him without knowing it.",
        "for_readers": "Austen structures Emma as a detective novel where the mystery is emotional truth. On rereading, every conversation between Frank and Jane transforms — his word games, his apparent flirtation with Emma, his restless visits. But the deeper secret is Emma's own heart. Chapter 47, where she realizes 'it darted through her, with the speed of an arrow, that Mr. Knightley must marry no one but herself,' is the novel's true climax — the moment self-deception ends.",
    },
    {
        "id": "theme-language-communication",
        "name": "Language and Miscommunication",
        "chapters": [9, 21, 27, 30, 39, 41, 43, 44, 49, 52],
        "about": "Austen fills Emma with acts of communication that fail: charades misread, compliments misdirected, silences misinterpreted, word games that conceal rather than reveal. Mr. Elton's riddle seems to praise Harriet but targets Emma. Frank's word game at the party spells 'blunder' for Jane. Emma's cruel joke at Box Hill wounds where she meant only to shine. Against all this failed speech, the novel prizes the rare moments of honest utterance — Knightley's rebuke, his proposal, Emma's tears.",
        "for_readers": "Pay attention to who speaks and who stays silent. Jane Fairfax's reserve drives Emma to distraction, but it's the most honest response to an impossible situation. Miss Bates's endless, apparently meaningless chatter actually contains crucial social intelligence. And Knightley says exactly what he means, always — which is why his words cut deepest and heal most. This thread connects directly to Gottman's research on communication patterns in relationships.",
    },
    {
        "id": "theme-self-knowledge",
        "name": "Self-Knowledge and Moral Growth",
        "chapters": [5, 12, 16, 17, 43, 44, 45, 47, 48, 49, 50, 55],
        "about": "Emma's journey from self-satisfied blindness to painful self-awareness is the novel's moral spine. Each humiliation strips away a layer of complacency: the Elton debacle teaches her she misjudges others' feelings; the Box Hill rebuke teaches her she can cause real harm; Harriet's revelation about Knightley teaches her she has been blind to her own heart. By the end, Emma hasn't become a different person — she's become a more honest version of herself.",
        "for_readers": "Austen never reduces Emma's growth to a simple before/after. Emma remains Emma — witty, opinionated, a little vain. What changes is her willingness to see herself clearly. The emotional sequence from Box Hill (Chapter 43) through the proposal (Chapter 49) is one of the great arcs in fiction: cruelty, shame, repentance, terror, self-knowledge, joy. This is what Sue Johnson calls 'emotional accessibility' — the willingness to be vulnerable that makes real attachment possible.",
    },
    {
        "id": "theme-community-care",
        "name": "Community and Care",
        "chapters": [2, 3, 6, 13, 14, 24, 28, 34, 36, 42, 45, 53, 54],
        "about": "Highbury is a character in itself — a small community bound by visits, dinners, balls, and the daily exchange of news and concern. Mr. Woodhouse frets about everyone's health; Miss Bates connects every household with her cheerful commentary; the Westons host; the Coles aspire. Emma's greatest failing is not her matchmaking but her occasional contempt for this web of care — her cruelty to Miss Bates violates the community's deepest ethic. Her growth is measured by her return to genuine kindness.",
        "for_readers": "The dinner parties and balls aren't just social backdrop — they're the infrastructure of human connection. Notice how Mr. Knightley moves through Highbury: visiting the poor, supporting Robert Martin, dancing with Harriet when she's humiliated, rebuking Emma when she hurts Miss Bates. He models what care looks like in practice. The novel's happy ending isn't just individual marriages but a community restored to harmony.",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)

    # Strip front matter (table of contents)
    # Find the first actual "VOLUME I" heading (not in TOC)
    # TOC has " VOLUME I." with leading space and period
    # Actual heading is "VOLUME I" flush left without period
    match = re.search(r'^VOLUME I\s*$', text, re.MULTILINE)
    if match:
        text = text[match.start():]

    chapters = parse_chapters(text)
    print(f"Parsed {len(chapters)} chapters")

    if len(chapters) != 55:
        print(f"WARNING: Expected 55 chapters, got {len(chapters)}")

    items = []
    sort_order = 0

    # L1: Individual chapters
    for ch in chapters:
        gn = ch['global_chapter']
        chapter_id = make_chapter_id(gn)
        sort_order += 1
        info = CHAPTER_INFO.get(gn, {"title": f"Chapter {gn}", "keywords": ["emma", "austen"]})

        items.append({
            "id": chapter_id,
            "name": f"Chapter {gn}: {info['title']}",
            "sort_order": sort_order,
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": ch['text'],
            },
            "keywords": info['keywords'],
            "metadata": {
                "volume": ch['volume'],
                "chapter_in_volume": ch['chapter_in_vol'],
                "global_chapter": gn,
            }
        })
        print(f"  Ch {gn:2d} (Vol {ch['volume']}, Ch {ch['chapter_in_vol']:2d}): {info['title']} ({len(ch['text'])} chars)")

    # L2: Volume groupings
    all_volume_ids = []
    for vg in VOLUME_GROUPS:
        sort_order += 1
        vol_id = vg["id"]
        all_volume_ids.append(vol_id)
        chapter_ids = [make_chapter_id(n) for n in vg["chapters"]]

        items.append({
            "id": vol_id,
            "name": vg["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "volume",
            "relationship_type": "emergence",
            "composite_of": chapter_ids,
            "sections": {
                "About": vg["about"],
                "For Readers": vg["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "chapter_count": len(vg["chapters"]),
            }
        })

    # L2: Thematic threads
    all_theme_ids = []
    for theme in THEMATIC_THREADS:
        sort_order += 1
        theme_id = theme["id"]
        all_theme_ids.append(theme_id)
        chapter_ids = [make_chapter_id(n) for n in theme["chapters"]]

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
                "chapter_count": len(theme["chapters"]),
            }
        })

    # L3: Meta-categories
    sort_order += 1
    items.append({
        "id": "emma-complete",
        "name": "Emma: The Complete Novel",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_volume_ids,
        "sections": {
            "About": "Jane Austen's Emma (1815) is the story of a young woman who thinks she understands the human heart better than anyone in her small world — and learns, through a series of comic and painful mistakes, that she has been blind to the hearts closest to her own. Set in the village of Highbury, it follows Emma Woodhouse's misguided matchmaking, her entanglement with the charming Frank Churchill, and her slow recognition that the man she has known longest — Mr. Knightley — is the one she truly loves. Austen called Emma 'a heroine whom no one but myself will much like,' but readers have loved her for two centuries. The novel is at once a comedy of manners, a detective story about hidden feelings, and one of the most penetrating studies of self-deception ever written.",
            "For Readers": "Emma rewards rereading more than almost any novel in English. The first time through, you share Emma's surprises — Elton's proposal, Frank's secret, her own feelings for Knightley. The second time, you see what Austen saw: every clue was there from the beginning. The novel is structured in three volumes that map an emotional arc: confidence, complication, and recognition. Read it for the comedy, stay for the psychology — Austen understood relationship dynamics two centuries before relationship science existed.",
        },
        "keywords": ["emma", "austen", "novel", "comedy-of-manners", "romance", "self-knowledge"],
        "metadata": {}
    })

    sort_order += 1
    items.append({
        "id": "emma-thematic-arcs",
        "name": "Thematic Arcs of Emma",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "Six thematic threads weave through Emma, each illuminating a different facet of Austen's vision. Matchmaking and Misjudgment traces Emma's pattern of projecting her fantasies onto others. Class and Social Standing maps Highbury's rigid hierarchies and the characters who navigate or challenge them. Secrecy and Revelation structures the novel as a mystery of hidden feelings. Language and Miscommunication examines how words fail, deceive, and occasionally heal. Self-Knowledge and Moral Growth follows Emma's painful journey to honesty. Community and Care reveals the web of relationships that sustains — and is threatened by — individual self-absorption.",
            "For Readers": "These themes don't operate in isolation — they interlock like a fugue. Emma's matchmaking failures (Theme 1) stem from class prejudice (Theme 2) and feed on secrets (Theme 3) expressed through failed communication (Theme 4). Her moral growth (Theme 5) is measured by her return to genuine care for the community (Theme 6). Reading across themes reveals how tightly Austen constructed her apparently effortless comedy.",
        },
        "keywords": ["themes", "analysis", "matchmaking", "class", "secrecy", "communication", "growth", "community"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Jane Austen",
                    "date": "1815",
                    "note": "Author"
                }
            ]
        },
        "name": "Emma",
        "description": "Jane Austen's Emma (1815) — the supreme comedy of self-deception in English literature. Emma Woodhouse, handsome, clever, and rich, sets out to arrange the romantic lives of her neighbors in the village of Highbury, blind to the real movements of every heart around her — especially her own. Fifty-five chapters across three volumes trace her journey from confident matchmaker to humbled lover, as Austen constructs one of the most intricate plots in fiction. Every rereading reveals new layers of irony, foreshadowing, and psychological precision.\n\nSource: Project Gutenberg eBook #158 (https://www.gutenberg.org/ebooks/158)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Hugh Thomson's pen-and-ink illustrations for the 1896 Macmillan edition of Emma — elegant, witty line drawings that perfectly capture Austen's social comedy. C. E. Brock's illustrations for the 1898 Dent edition. Chris Hammond's illustrations for the 1898 George Allen edition.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["novel", "romance", "comedy-of-manners", "british-literature", "regency", "public-domain", "full-text"],
        "roots": ["emotion-love"],
        "shelves": ["mirror"],
        "lineages": ["Gottman", "Johnson"],
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
    print(f"  L1: {l1} chapters, L2: {l2} (volumes + themes), L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
