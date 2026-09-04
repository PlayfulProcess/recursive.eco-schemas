#!/usr/bin/env python3
"""
Build grammar.json for The Alhambra by Washington Irving.

Source: Project Gutenberg eBook #49947
Author: Washington Irving (1832, revised 1851)

Structure:
- L1: 41 chapters/essays/legends
- L2: 5 thematic groupings
- L3: Meta-category (the complete work)

The Alhambra is a mix of travel writing, historical sketches, and legends
set in and around the Moorish palace of the Alhambra in Granada, Spain.
"""

import json
import re
import os
import unicodedata
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "legends-alhambra.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "legends-alhambra"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# The 41 chapters in order, with their titles as they appear in the BODY text.
# Some titles are split across multiple lines; we store them as a list of lines.
# The "display_name" is the cleaned-up title for the grammar item.
CHAPTERS = [
    {
        "num": 1,
        "title_lines": ["THE JOURNEY"],
        "display_name": "The Journey",
        "category": "chapter",
        "keywords": ["travel", "Andalusia", "Seville", "Granada", "arrival", "Spain"],
    },
    {
        "num": 2,
        "title_lines": ["PALACE OF THE ALHAMBRA"],
        "display_name": "Palace of the Alhambra",
        "category": "chapter",
        "keywords": ["Alhambra", "palace", "Moorish", "architecture", "history"],
    },
    {
        "num": 3,
        "title_lines": ["IMPORTANT NEGOTIATIONS", "THE AUTHOR SUCCEEDS TO THE THRONE OF BOABDIL"],
        "display_name": "Important Negotiations -- The Author Succeeds to the Throne of Boabdil",
        "category": "chapter",
        "keywords": ["Boabdil", "residence", "governor", "negotiations", "Alhambra"],
    },
    {
        "num": 4,
        "title_lines": ["INHABITANTS OF THE ALHAMBRA"],
        "display_name": "Inhabitants of the Alhambra",
        "category": "chapter",
        "keywords": ["inhabitants", "Tia Antonia", "Dolores", "Mateo", "community"],
    },
    {
        "num": 5,
        "title_lines": ["THE HALL OF AMBASSADORS"],
        "display_name": "The Hall of Ambassadors",
        "category": "chapter",
        "keywords": ["hall", "ambassadors", "architecture", "Moorish", "throne-room"],
    },
    {
        "num": 6,
        "title_lines": ["THE JESUITS' LIBRARY"],
        "display_name": "The Jesuits' Library",
        "category": "chapter",
        "keywords": ["library", "Jesuits", "books", "chronicles", "history"],
    },
    {
        "num": 7,
        "title_lines": ["ALHAMAR, THE FOUNDER OF THE ALHAMBRA"],
        "display_name": "Alhamar, the Founder of the Alhambra",
        "category": "chapter",
        "keywords": ["Alhamar", "founder", "Moorish", "history", "king", "Nasrid"],
    },
    {
        "num": 8,
        "title_lines": ["YUSEF ABUL HAGIG", "THE FINISHER OF THE ALHAMBRA"],
        "display_name": "Yusef Abul Hagig, the Finisher of the Alhambra",
        "category": "chapter",
        "keywords": ["Yusef", "Abul Hagig", "Alhambra", "completion", "history"],
    },
    {
        "num": 9,
        "title_lines": ["THE MYSTERIOUS CHAMBERS"],
        "display_name": "The Mysterious Chambers",
        "category": "chapter",
        "keywords": ["chambers", "mystery", "exploration", "palace", "Alhambra"],
    },
    {
        "num": 10,
        "title_lines": ["PANORAMA FROM THE TOWER OF COMARES"],
        "display_name": "Panorama from the Tower of Comares",
        "category": "chapter",
        "keywords": ["tower", "Comares", "panorama", "view", "Granada", "landscape"],
    },
    {
        "num": 11,
        "title_lines": ["THE TRUANT"],
        "display_name": "The Truant",
        "category": "chapter",
        "keywords": ["truant", "boy", "idle", "childhood", "Alhambra"],
    },
    {
        "num": 12,
        "title_lines": ["THE BALCONY"],
        "display_name": "The Balcony",
        "category": "chapter",
        "keywords": ["balcony", "evening", "moonlight", "views", "Alhambra"],
    },
    {
        "num": 13,
        "title_lines": ["THE ADVENTURE OF THE MASON"],
        "display_name": "The Adventure of the Mason",
        "category": "legend",
        "keywords": ["mason", "treasure", "adventure", "Moor", "enchantment"],
    },
    {
        "num": 14,
        "title_lines": ["THE COURT OF LIONS"],
        "display_name": "The Court of Lions",
        "category": "chapter",
        "keywords": ["court", "lions", "fountain", "architecture", "Moorish"],
    },
    {
        "num": 15,
        "title_lines": ["THE ABENCERRAGES"],
        "display_name": "The Abencerrages",
        "category": "chapter",
        "keywords": ["Abencerrages", "massacre", "history", "Boabdil", "tragedy"],
    },
    {
        "num": 16,
        "title_lines": ["MEMENTOS OF BOABDIL"],
        "display_name": "Mementos of Boabdil",
        "category": "chapter",
        "keywords": ["Boabdil", "mementos", "last Moor", "fall of Granada", "history"],
    },
    {
        "num": 17,
        "title_lines": ["PUBLIC F\u00caTES OF GRANADA"],
        "display_name": "Public F\u00eates of Granada",
        "category": "chapter",
        "keywords": ["festival", "Granada", "celebration", "public", "customs"],
    },
    {
        "num": 18,
        "title_lines": ["LOCAL TRADITIONS"],
        "display_name": "Local Traditions",
        "category": "chapter",
        "keywords": ["traditions", "local", "superstition", "folklore", "Granada"],
    },
    {
        "num": 19,
        "title_lines": ["THE HOUSE OF THE WEATHERCOCK"],
        "display_name": "The House of the Weathercock",
        "category": "legend",
        "keywords": ["weathercock", "enchantment", "Moorish", "legend", "talisman"],
    },
    {
        "num": 20,
        "title_lines": ["LEGEND OF THE ARABIAN ASTROLOGER"],
        "display_name": "Legend of the Arabian Astrologer",
        "category": "legend",
        "keywords": ["astrologer", "Arabian", "magic", "enchantment", "king", "talisman"],
    },
    {
        "num": 21,
        "title_lines": ["VISITORS TO THE ALHAMBRA"],
        "display_name": "Visitors to the Alhambra",
        "category": "chapter",
        "keywords": ["visitors", "tourists", "Alhambra", "travellers", "pilgrims"],
    },
    {
        "num": 22,
        "title_lines": ["RELICS AND GENEALOGIES"],
        "display_name": "Relics and Genealogies",
        "category": "chapter",
        "keywords": ["relics", "genealogies", "family", "heritage", "Granada"],
    },
    {
        "num": 23,
        "title_lines": ["THE GENERALIFE"],
        "display_name": "The Generalife",
        "category": "chapter",
        "keywords": ["Generalife", "gardens", "palace", "Moorish", "beauty"],
    },
    {
        "num": 24,
        "title_lines": ["LEGEND OF PRINCE AHMED AL KAMEL", "OR, THE PILGRIM OF LOVE"],
        "display_name": "Legend of Prince Ahmed al Kamel; or, The Pilgrim of Love",
        "category": "legend",
        "keywords": ["prince", "Ahmed", "love", "pilgrimage", "enchantment", "owl", "parrot"],
    },
    {
        "num": 25,
        "title_lines": ["A RAMBLE AMONG THE HILLS"],
        "display_name": "A Ramble Among the Hills",
        "category": "chapter",
        "keywords": ["ramble", "hills", "landscape", "countryside", "walking"],
    },
    {
        "num": 26,
        "title_lines": ["LEGEND OF THE MOOR'S LEGACY"],
        "display_name": "Legend of the Moor's Legacy",
        "category": "legend",
        "keywords": ["Moor", "legacy", "treasure", "water-carrier", "enchantment"],
    },
    {
        "num": 27,
        "title_lines": ["THE TOWER OF LAS INFANTAS"],
        "display_name": "The Tower of Las Infantas",
        "category": "chapter",
        "keywords": ["tower", "infantas", "princesses", "Alhambra", "history"],
    },
    {
        "num": 28,
        "title_lines": ["LEGEND OF THE THREE BEAUTIFUL PRINCESSES"],
        "display_name": "Legend of the Three Beautiful Princesses",
        "category": "legend",
        "keywords": ["princesses", "legend", "enchantment", "love", "escape", "Moorish"],
    },
    {
        "num": 29,
        "title_lines": ["LEGEND OF THE ROSE OF THE ALHAMBRA"],
        "display_name": "Legend of the Rose of the Alhambra",
        "category": "legend",
        "keywords": ["rose", "Alhambra", "enchantment", "music", "love", "ghost"],
    },
    {
        "num": 30,
        "title_lines": ["THE VETERAN"],
        "display_name": "The Veteran",
        "category": "chapter",
        "keywords": ["veteran", "soldier", "garrison", "Alhambra", "character"],
    },
    {
        "num": 31,
        "title_lines": ["THE GOVERNOR AND THE NOTARY"],
        "display_name": "The Governor and the Notary",
        "category": "chapter",
        "keywords": ["governor", "notary", "authority", "law", "humor"],
    },
    {
        "num": 32,
        "title_lines": ["GOVERNOR MANCO AND THE SOLDIER"],
        "display_name": "Governor Manco and the Soldier",
        "category": "legend",
        "keywords": ["governor", "Manco", "soldier", "enchantment", "treasure", "ghost"],
    },
    {
        "num": 33,
        "title_lines": ["A F\u00caTE IN THE ALHAMBRA"],
        "display_name": "A F\u00eate in the Alhambra",
        "category": "chapter",
        "keywords": ["f\u00eate", "celebration", "Alhambra", "Spanish", "noble"],
    },
    {
        "num": 34,
        "title_lines": ["LEGEND OF THE TWO DISCREET STATUES"],
        "display_name": "Legend of the Two Discreet Statues",
        "category": "legend",
        "keywords": ["statues", "treasure", "secret", "enchantment", "water-carrier"],
    },
    {
        "num": 35,
        "title_lines": ["THE CRUSADE OF THE GRAND MASTER OF ALC\u00c1NTARA"],
        "display_name": "The Crusade of the Grand Master of Alc\u00e1ntara",
        "category": "chapter",
        "keywords": ["crusade", "Alc\u00e1ntara", "grand master", "history", "bigotry", "reconquista"],
    },
    {
        "num": 36,
        "title_lines": ["SPANISH ROMANCE"],
        "display_name": "Spanish Romance",
        "category": "chapter",
        "keywords": ["romance", "Spanish", "chivalry", "frontier", "ballads"],
    },
    {
        "num": 37,
        "title_lines": ["LEGEND OF DON MUNIO SANCHO DE HINOJOSA"],
        "display_name": "Legend of Don Munio Sancho de Hinojosa",
        "category": "legend",
        "keywords": ["Don Munio", "Hinojosa", "crusade", "ghost", "piety", "legend"],
    },
    {
        "num": 38,
        "title_lines": ["POETS AND POETRY OF MOSLEM ANDALUS"],
        "display_name": "Poets and Poetry of Moslem Andalus",
        "category": "chapter",
        "keywords": ["poetry", "Moslem", "Andalus", "literature", "Arabic", "culture"],
    },
    {
        "num": 39,
        "title_lines": ["AN EXPEDITION IN QUEST OF A DIPLOMA"],
        "display_name": "An Expedition in Quest of a Diploma",
        "category": "chapter",
        "keywords": ["expedition", "diploma", "bureaucracy", "humor", "Granada"],
    },
    {
        "num": 40,
        "title_lines": ["THE LEGEND OF THE ENCHANTED SOLDIER"],
        "display_name": "The Legend of the Enchanted Soldier",
        "category": "legend",
        "keywords": ["enchanted", "soldier", "spell", "treasure", "mid-summer", "magic"],
    },
    {
        "num": 41,
        "title_lines": ["THE AUTHOR'S FAREWELL TO GRANADA"],
        "display_name": "The Author's Farewell to Granada",
        "category": "chapter",
        "keywords": ["farewell", "departure", "Granada", "Boabdil", "nostalgia"],
    },
]


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


def strip_illustrations(text):
    """Remove [Illustration: ...] markers, which may span multiple lines."""
    # Handle single-line illustrations
    text = re.sub(r'\[Illustration:[^\]]*\]', '', text)
    # Handle multi-line illustrations
    text = re.sub(r'\[Illustration:.*?\]', '', text, flags=re.DOTALL)
    return text


def strip_footnotes_inline(text):
    """Remove inline footnote markers like [1], [2], etc."""
    return re.sub(r'\[\d+\]', '', text)


def normalize_for_matching(s):
    """Normalize a string for case-insensitive, accent-insensitive matching."""
    # Normalize smart quotes/apostrophes to straight
    s = s.replace('\u2018', "'").replace('\u2019', "'")
    s = s.replace('\u201c', '"').replace('\u201d', '"')
    # Decompose unicode, strip combining marks, uppercase
    nfkd = unicodedata.normalize('NFKD', s)
    stripped = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return stripped.upper().strip()


def find_chapter_starts(lines):
    """Find the starting line index of each chapter in the body text.

    Returns a list of (chapter_index, start_line) tuples.
    Each chapter's title may span multiple consecutive ALL CAPS lines.
    """
    results = []
    # Normalize all chapter title lines for matching
    normalized_titles = []
    for ch in CHAPTERS:
        normalized_titles.append([normalize_for_matching(tl) for tl in ch["title_lines"]])

    # Skip past the CONTENTS section to find the body text.
    # The body starts after the last CONTENTS entry and a blank region,
    # typically with "THE ALHAMBRA" as a divider, then the first chapter.
    body_start = 0
    for i, line in enumerate(lines):
        # The body "THE JOURNEY" is the first chapter heading
        if normalize_for_matching(line) == "THE JOURNEY" and i > 100:
            body_start = i
            break

    for ch_idx, ch in enumerate(CHAPTERS):
        title_norms = normalized_titles[ch_idx]
        first_title = title_norms[0]
        num_title_lines = len(title_norms)

        # Search from body_start onward
        for i in range(body_start, len(lines)):
            line_norm = normalize_for_matching(lines[i])
            if not line_norm:
                continue

            # Check if the first title line matches
            if first_title == line_norm:
                # If multi-line title, verify subsequent lines match
                if num_title_lines > 1:
                    match = True
                    for j in range(1, num_title_lines):
                        # Skip blank lines between title parts
                        next_idx = i + 1
                        while next_idx < len(lines) and lines[next_idx].strip() == '':
                            next_idx += 1
                        # Adjust: look through next few lines for the match
                        found_sub = False
                        for k in range(i + 1, min(i + 5, len(lines))):
                            if normalize_for_matching(lines[k]) == title_norms[j]:
                                found_sub = True
                                break
                        if not found_sub:
                            match = False
                            break
                    if not match:
                        continue

                results.append((ch_idx, i))
                # Move body_start past this match to avoid re-matching
                body_start = i + num_title_lines
                break

    return results


def parse_chapters(text):
    """Parse the text into chapters."""
    lines = text.split('\n')
    chapter_starts = find_chapter_starts(lines)

    if len(chapter_starts) != len(CHAPTERS):
        print(f"WARNING: Expected {len(CHAPTERS)} chapters, found {len(chapter_starts)}")
        found_nums = [CHAPTERS[ci]["num"] for ci, _ in chapter_starts]
        for ch in CHAPTERS:
            if ch["num"] not in found_nums:
                print(f"  Missing: {ch['display_name']}")

    chapters = []
    for idx, (ch_idx, start_line) in enumerate(chapter_starts):
        ch_def = CHAPTERS[ch_idx]
        num_title_lines = len(ch_def["title_lines"])

        # Content starts after the title line(s) and any blank lines
        content_start = start_line + 1
        # Skip all remaining title lines and blanks
        while content_start < len(lines):
            stripped = lines[content_start].strip()
            if stripped == '':
                content_start += 1
                continue
            # Check if this is a continuation title line (ALL CAPS, short)
            norm = normalize_for_matching(stripped)
            is_title_continuation = False
            for tl in ch_def["title_lines"][1:]:
                if normalize_for_matching(tl) == norm:
                    is_title_continuation = True
                    break
            if is_title_continuation:
                content_start += 1
                continue
            break

        # Content ends at the start of the next chapter (or end of text)
        if idx + 1 < len(chapter_starts):
            content_end = chapter_starts[idx + 1][1]
        else:
            content_end = len(lines)

        chapter_text = '\n'.join(lines[content_start:content_end]).strip()

        # Clean up the text
        chapter_text = strip_illustrations(chapter_text)
        chapter_text = strip_footnotes_inline(chapter_text)
        # Remove footnote sections (indented text starting with [number])
        chapter_text = re.sub(r'\n\s*NOTES TO THE ENCHANTED SOLDIER.*', '', chapter_text, flags=re.DOTALL)
        chapter_text = re.sub(r'\n\s*FOOTNOTES:.*', '', chapter_text, flags=re.DOTALL)
        # Remove separator lines (* * * * *)
        chapter_text = re.sub(r'\s*\*\s+\*\s+\*\s+\*\s+\*\s*', '\n\n', chapter_text)
        # Remove "THE END" near the end of text
        chapter_text = re.sub(r'\n\s*THE END\s*$', '', chapter_text)
        # Normalize excessive whitespace
        chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)
        chapter_text = chapter_text.strip()

        chapters.append({
            'num': ch_def['num'],
            'display_name': ch_def['display_name'],
            'category': ch_def['category'],
            'keywords': ch_def['keywords'],
            'text': chapter_text,
        })

    return chapters


def make_id(num, name):
    """Create a hyphenated ID from chapter number and name."""
    clean = name.lower()
    # Remove accented characters
    nfkd = unicodedata.normalize('NFKD', clean)
    clean = ''.join(c for c in nfkd if not unicodedata.combining(c))
    clean = re.sub(r'[^a-z0-9\s-]', '', clean)
    clean = re.sub(r'\s+', '-', clean.strip())
    clean = re.sub(r'-+', '-', clean)
    # Truncate long IDs
    if len(clean) > 50:
        clean = clean[:50].rstrip('-')
    return f"ch-{num:02d}-{clean}"


# L2 Thematic groupings
THEMES = [
    {
        "id": "theme-journey-to-alhambra",
        "name": "The Journey to the Alhambra",
        "chapter_nums": [1, 2, 3, 4],
        "about": "Washington Irving's arrival in Andalusia and his enchanted first encounter with the Alhambra. From the rough road through the mountains to the gates of the Moorish palace, from nervous negotiations with the governor to settling in among the curious inhabitants of the crumbling fortress. These chapters establish Irving as the dreaming American who has stumbled into a half-real, half-legendary world -- and who will never quite leave it.",
        "for_readers": "Start here for Irving's irresistible travel voice: the comic misadventures of the road, the first breathtaking sight of the Alhambra, and the wonderful cast of characters who inhabit its ruins. Irving writes himself into the palace the way a good guest enters a house -- noticing everything, judging nothing, falling in love.",
    },
    {
        "id": "theme-palace-and-history",
        "name": "The Palace and Its History",
        "chapter_nums": [5, 6, 7, 8, 9, 10, 14, 15, 16],
        "about": "The Alhambra as a physical and historical presence. Irving explores the Hall of Ambassadors, the Jesuits' Library, the Mysterious Chambers, the Tower of Comares, and the Court of Lions. Interwoven with these architectural meditations are the histories of Alhamar the founder, Yusef Abul Hagig the finisher, and the tragic Abencerrages, culminating in the mementos of Boabdil, the last Moorish king. Architecture and history become inseparable -- every carved wall tells a story of glory and loss.",
        "for_readers": "These chapters work best read in the palace's own sequence: walk through the Hall of Ambassadors, climb the Tower of Comares, stand in the Court of Lions where the Abencerrages were massacred. Irving brings the stones alive. The chapters on Alhamar and Yusef provide the dynastic history; the Abencerrages chapter is pure historical drama.",
    },
    {
        "id": "theme-life-in-alhambra",
        "name": "Life in the Alhambra",
        "chapter_nums": [11, 12, 17, 21, 22, 23, 25, 30, 31, 33, 39],
        "about": "The daily rhythms and social world of Irving's sojourn. Watching a truant boy from the balcony, attending public fetes, receiving curious visitors, rambling among the hills, meeting veterans and governors and notaries, celebrating a feast day, and venturing out on a comic expedition for a diploma. These chapters capture the texture of lived experience in the Alhambra -- the lazy afternoons, the moonlit balconies, the gossiping neighbors, the absurd bureaucracy of provincial Spain.",
        "for_readers": "These are Irving at his most charming and observant. The Balcony is a perfect vignette of evening in Granada. A Ramble Among the Hills is gorgeous landscape writing. The Governor and the Notary and An Expedition in Quest of a Diploma are comic gems. Read them as a portrait of a vanished way of life -- slow, sociable, touched with melancholy.",
    },
    {
        "id": "theme-legends",
        "name": "The Legends",
        "chapter_nums": [13, 19, 20, 24, 26, 27, 28, 29, 32, 34, 37, 40],
        "about": "The enchanted heart of the book. Irving retells the legends and tales that cling to the Alhambra like moss to its walls: the adventure of the mason who stumbles on Moorish treasure; the Arabian astrologer whose talismans protect a kingdom; Prince Ahmed al Kamel's pilgrimage of love guided by an owl and a parrot; the Moor's legacy and the water-carrier's fortune; the three beautiful princesses imprisoned in a tower; the rose of the Alhambra whose music breaks an ancient spell; Governor Manco outwitted by a spectral soldier; the two discreet statues who guard a secret; Don Munio's ghostly crusade; and the enchanted soldier who waits on midsummer eve. These legends blur the line between history and fairy tale, between the real Alhambra and the dream palace.",
        "for_readers": "The legends are the jewels of the book. Legend of Prince Ahmed al Kamel is the longest and most delightful -- a full fairy tale. Legend of the Arabian Astrologer is Irving's most atmospheric piece. The shorter legends (the Mason, the Moor's Legacy, the Enchanted Soldier) are perfect campfire stories. Read them in moonlight if you can.",
    },
    {
        "id": "theme-history-and-culture",
        "name": "History and Culture",
        "chapter_nums": [6, 7, 8, 15, 18, 35, 36, 38, 41],
        "about": "Irving as historian and cultural observer. The Jesuits' Library opens the chronicles of Moorish Spain; the histories of Alhamar and Yusef Abul Hagig trace the Alhambra's construction; the Abencerrages chapter recounts one of history's most famous massacres; Local Traditions records the superstitions of Granada's people; the Crusade of the Grand Master of Alcantara exposes religious bigotry; Spanish Romance celebrates the frontier ballad tradition; and the Poets and Poetry of Moslem Andalus recovers a lost literary world. The farewell chapter brings history full circle -- Irving departing like Boabdil, the last king, looking back at paradise lost.",
        "for_readers": "These chapters reveal Irving's deeper purpose: to recover the memory of Moorish Spain at a time when it was being systematically erased. Poets and Poetry of Moslem Andalus is a remarkable piece of cultural recovery. The Crusade of the Grand Master shows Irving's unflinching view of religious persecution. The Author's Farewell is one of the most moving endings in travel literature.",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)

    chapters = parse_chapters(text)
    print(f"Parsed {len(chapters)} chapters")

    items = []
    sort_order = 0
    ch_id_map = {}  # num -> id

    # L1: Individual chapters
    for ch in chapters:
        item_id = make_id(ch['num'], ch['display_name'])
        ch_id_map[ch['num']] = item_id
        sort_order += 1

        items.append({
            "id": item_id,
            "name": ch['display_name'],
            "sort_order": sort_order,
            "level": 1,
            "category": ch['category'],
            "sections": {
                "Text": ch['text'],
            },
            "keywords": ch['keywords'],
            "metadata": {
                "chapter_number": ch['num'],
            },
        })
        print(f"  Ch {ch['num']:2d}: {ch['display_name']} [{ch['category']}] ({len(ch['text'])} chars)")

    # L2: Thematic groupings
    theme_ids = []
    for theme in THEMES:
        sort_order += 1
        composite = [ch_id_map[n] for n in theme["chapter_nums"] if n in ch_id_map]
        items.append({
            "id": theme["id"],
            "name": theme["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": composite,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "chapter_count": len(theme["chapter_nums"]),
            },
        })
        theme_ids.append(theme["id"])

    # L3: Meta-category
    sort_order += 1
    items.append({
        "id": "alhambra-complete",
        "name": "The Alhambra: Between History and Legend",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": theme_ids,
        "sections": {
            "About": "Washington Irving's The Alhambra (1832, revised 1851) is the book that introduced the English-speaking world to the magic of Moorish Spain. Part travel journal, part historical sketch, part fairy-tale collection, it records Irving's months living in the crumbling palace of the Alhambra in Granada -- exploring its halls, befriending its eccentric inhabitants, and gathering the legends that clung to its walls. Irving blurs the line between the real palace and the dream palace, between documented history and fireside tale, creating a book that is itself a kind of enchantment. The 41 chapters move between close observation of daily life, passionate recovery of Moorish history and culture, and retelling of legends in which treasure hunters stumble on Moorish gold, princesses escape from towers, enchanted soldiers stand guard on midsummer eve, and love breaks every spell.",
            "For Readers": "The Alhambra can be read straight through as a travel narrative with an enchanted arc -- arrival, settlement, exploration, legend, farewell. Or browse by mood: the travel chapters for Irving's comic, humane voice; the history chapters for the tragedy of Moorish Spain; the legends for pure storytelling magic. Irving's prose is lucid and unhurried, the ideal companion for an afternoon in any garden. This book created the romantic image of the Alhambra that persists to this day.",
        },
        "keywords": ["Alhambra", "Irving", "Granada", "Moorish", "Spain", "legends", "travel-writing"],
        "metadata": {},
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Washington Irving",
                    "date": "1832 (revised 1851)",
                    "note": "Author",
                },
            ],
        },
        "name": "The Alhambra",
        "description": "Washington Irving's The Alhambra (1832, revised 1851) -- the book that introduced the English-speaking world to the enchantment of Moorish Spain. Part travel journal, part historical chronicle, part fairy-tale collection, it records Irving's months living in the crumbling palace of the Alhambra in Granada, exploring its halls, befriending its inhabitants, and gathering the legends that haunt its walls. 41 chapters of travel writing, historical sketches, and legends of enchanted treasure, imprisoned princesses, spectral soldiers, and the last Moorish king.\n\nSource: Project Gutenberg eBook #49947 (https://www.gutenberg.org/ebooks/49947)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Joseph Pennell's illustrations for the 1896 Macmillan edition of The Alhambra. George Cattermole's illustrations for earlier editions. Photographs and engravings of the Alhambra from the 19th century, including those by Charles Clifford (1850s-60s). David Roberts' lithographs of Spanish and Moorish architecture (1830s-40s). Gustave Dor\u00e9's engravings of Spain (1874).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["travel-writing", "legends", "Moorish", "Spain", "Granada", "history", "public-domain", "full-text"],
        "roots": ["european-tradition", "indigenous-mythology"],
        "shelves": ["wonder"],
        "lineages": ["Andreotti"],
        "worldview": "romantic",
        "items": items,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1: {l1} chapters/legends, L2: {l2} themes, L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
