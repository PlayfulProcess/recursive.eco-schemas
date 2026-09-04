#!/usr/bin/env python3
"""
Parser for Songs of Kabir (Project Gutenberg #6519).
Reads seeds/songs-of-kabir.txt and generates grammars/songs-of-kabir/grammar.json.

Kabir, translated by Rabindranath Tagore, introduction by Evelyn Underhill (1915).
"""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
INPUT_FILE = os.path.join(PROJECT_ROOT, "seeds", "songs-of-kabir.txt")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "grammars", "songs-of-kabir")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "grammar.json")


# --- Roman numeral helpers ---

ROMAN_VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]

def roman_to_int(s):
    """Convert a Roman numeral string to an integer."""
    s = s.strip().upper()
    result = 0
    i = 0
    for value, numeral in ROMAN_VALUES:
        while s[i:i+len(numeral)] == numeral:
            result += value
            i += len(numeral)
    return result


def int_to_roman(n):
    """Convert an integer to a Roman numeral string."""
    result = []
    for value, numeral in ROMAN_VALUES:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)


# --- Parsing ---

def read_source():
    """Read the source file and return lines."""
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return f.readlines()


def strip_gutenberg(lines):
    """Strip Gutenberg header and footer, return content lines."""
    start = None
    end = None
    for i, line in enumerate(lines):
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in line:
            start = i + 1
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line:
            end = i
            break
    if start is None or end is None:
        print("ERROR: Could not find Gutenberg markers", file=sys.stderr)
        sys.exit(1)
    return lines[start:end]


def find_poems_start(lines):
    """Find the line index where 'KABIR'S POEMS' header appears."""
    for i, line in enumerate(lines):
        if line.strip() == "KABIR'S POEMS":
            return i
    print("ERROR: Could not find KABIR'S POEMS header", file=sys.stderr)
    sys.exit(1)


def parse_poems(lines):
    """Parse all poems from the text. Returns list of poem dicts."""
    # Roman numeral line pattern: 2 spaces + roman numeral only
    roman_re = re.compile(r"^  ([IVXLC]+)$")
    # Reference line pattern: e.g. "  I. 13.  _mo ko kahân dhûnro bande_"
    # or "  II. 61. _grah candra tapan jot varat hai_"
    ref_re = re.compile(r"^  ([IVX]+\.\s+\d+\.)\s+_(.+?)_\s*$")

    # Find all poem start positions (Roman numeral lines)
    poem_starts = []
    for i, line in enumerate(lines):
        m = roman_re.match(line)
        if m:
            num = roman_to_int(m.group(1))
            poem_starts.append((i, num, m.group(1)))

    poems = []
    for idx, (start_line, song_num, roman_str) in enumerate(poem_starts):
        # Determine end of this poem (start of next poem or end of text)
        if idx + 1 < len(poem_starts):
            end_line = poem_starts[idx + 1][0]
        else:
            end_line = len(lines)

        # Extract the block for this poem
        block = lines[start_line + 1 : end_line]

        # Parse reference line and Hindi title
        reference = ""
        hindi_title = ""
        verse_lines = []
        found_ref = False

        for bline in block:
            stripped = bline.rstrip("\n")
            if not found_ref:
                rm = ref_re.match(stripped)
                if rm:
                    reference = rm.group(1).strip()
                    hindi_title = rm.group(2).strip()
                    found_ref = True
                    continue
                # Skip blank lines before reference
                if stripped.strip() == "":
                    continue
            else:
                verse_lines.append(stripped)

        # Clean up verse text: strip leading/trailing blank lines, remove 2-space indent
        # Trim trailing blank lines
        while verse_lines and verse_lines[-1].strip() == "":
            verse_lines.pop()
        # Trim leading blank lines
        while verse_lines and verse_lines[0].strip() == "":
            verse_lines.pop(0)

        # Remove the common 2-space indent
        cleaned = []
        for vl in verse_lines:
            if vl.startswith("  "):
                cleaned.append(vl[2:])
            else:
                cleaned.append(vl)

        verse_text = "\n".join(cleaned)

        # Get first line for the name (truncate to 60 chars)
        first_line = ""
        for cl in cleaned:
            if cl.strip():
                first_line = cl.strip()
                break
        if len(first_line) > 60:
            first_line = first_line[:57] + "..."

        poems.append({
            "song_number": song_num,
            "roman": roman_str,
            "reference": reference,
            "hindi_title": hindi_title,
            "first_line": first_line,
            "verse": verse_text,
        })

    return poems


# --- L2 Theme Groups ---

THEMES = [
    {
        "id": "theme-beloved-within",
        "name": "The Beloved Within",
        "songs": [1, 3, 6, 9, 20, 41, 43, 61, 67],
        "about": (
            "These songs proclaim Kabir's most radical insight: that the Divine "
            "is not to be found in temples, mosques, pilgrimages, or rituals, but "
            "within the human body itself. 'O servant, where dost thou seek Me? "
            "Lo! I am beside thee.' This theme runs through all of Kabir's work "
            "but finds its purest expression in these songs, where every breath "
            "becomes a prayer and every heartbeat a hymn."
        ),
        "for_readers": (
            "Read these songs when you feel distant from the sacred. Kabir's "
            "insistence that divinity dwells within — not in any institution or "
            "practice — is both comforting and challenging. Let these verses shift "
            "your attention from seeking outward to listening inward. What if the "
            "One you seek has been here all along?"
        ),
    },
    {
        "id": "theme-music-of-infinite",
        "name": "The Music of the Infinite",
        "songs": [17, 18, 19, 38, 39, 41, 68, 76],
        "about": (
            "Kabir is a poet of sound. These songs speak of the 'unstruck music' "
            "(anahata nada) — the divine vibration that pervades all creation but "
            "is heard only by the awakened soul. Drums beat without hands, bells "
            "ring without being struck, and the entire cosmos becomes an orchestra "
            "of the Infinite. This is the mystical tradition of Shabd or Nada Yoga, "
            "the yoga of sacred sound."
        ),
        "for_readers": (
            "These are songs to read slowly, perhaps aloud. Notice how Kabir uses "
            "musical imagery to describe states beyond words. The 'unstruck chord' "
            "is a doorway to contemplative practice — what would it mean to listen "
            "for a music that has no source? Let these poems tune your attention to "
            "the subtlest layers of experience."
        ),
    },
    {
        "id": "theme-maya-illusion",
        "name": "Maya and Illusion",
        "songs": [5, 7, 8, 14, 16, 24, 42, 63, 74],
        "about": (
            "Kabir sees through the veil of Maya — the world of appearances, "
            "attachments, and mistaken identities. These songs challenge the sleeper "
            "to wake up: wealth is nothing, the body is temporary, pride and caste "
            "are illusions. Yet Kabir is no ascetic — he does not reject the world "
            "but asks us to see it truly, to stop clinging to what was never ours."
        ),
        "for_readers": (
            "These songs hold a mirror to our attachments. Kabir's voice is urgent, "
            "sometimes fierce — he wants to shake us awake. Read them when you feel "
            "caught in the surface of things. What are you clinging to? What would "
            "it mean to let go — not of life itself, but of the illusions that "
            "obscure it?"
        ),
    },
    {
        "id": "theme-love-and-longing",
        "name": "Love and Longing",
        "songs": [2, 11, 21, 26, 27, 31, 36, 50, 65, 86],
        "about": (
            "At the heart of Kabir's mysticism is love — not abstract theology but "
            "the raw, aching desire of the soul for its Beloved. These songs use "
            "the language of romantic love to describe the soul's yearning for God: "
            "the Beloved is absent, the nights are long, the lover waits and weeps "
            "and sings. This is the tradition of viraha — love-in-separation — "
            "shared by Sufi poets and the bhakti saints."
        ),
        "for_readers": (
            "These are among Kabir's most emotionally powerful songs. The longing "
            "they express is universal — whether you read it as spiritual seeking "
            "or human desire, the ache is real. Let yourself feel the yearning "
            "without rushing to resolve it. In Kabir's world, the longing itself "
            "is a form of connection."
        ),
    },
    {
        "id": "theme-death-liberation",
        "name": "Death and Liberation",
        "songs": [4, 12, 23, 32, 45, 87, 89, 90, 96],
        "about": (
            "Kabir speaks of death not with fear but with the familiarity of a weaver "
            "who knows the thread must end. These songs explore the body's mortality, "
            "the moment of dissolution, and the liberation that comes when the soul "
            "recognizes its true nature. 'If your bonds be not broken whilst living, "
            "what hope of deliverance in death?' The urgency is to awaken now."
        ),
        "for_readers": (
            "Death is Kabir's great teacher. These songs do not offer easy comfort "
            "but rather the fierce clarity of someone who has looked directly at "
            "impermanence. Read them when you need perspective, when the small "
            "worries of life need to be set against the vast backdrop of existence. "
            "What would you do differently if you truly accepted that this body "
            "will not last?"
        ),
    },
    {
        "id": "theme-guru-teaching",
        "name": "The Guru's Teaching",
        "songs": [10, 13, 28, 33, 46, 55, 58, 97],
        "about": (
            "Kabir reveres the guru — the true teacher who transmits not information "
            "but transformation. These songs celebrate the moment of awakening that "
            "comes through the teacher's grace, the word that shatters illusion, "
            "the glance that opens the inner eye. Yet Kabir also warns against "
            "false gurus and empty learning: 'Reading book after book the whole "
            "world died, and none ever became learned.'"
        ),
        "for_readers": (
            "These songs speak to anyone on a path of learning. Kabir's guru is not "
            "an authority figure but a mirror — someone who helps you see what was "
            "always there. Consider: who have been the true teachers in your life? "
            "Not necessarily those with titles, but those whose presence changed "
            "something in you."
        ),
    },
    {
        "id": "theme-beyond-hindu-muslim",
        "name": "Beyond Hindu and Muslim",
        "songs": [1, 2, 9, 15, 42, 57, 69, 75, 99],
        "about": (
            "Kabir's most historically radical songs are those that refuse the "
            "boundaries between Hindu and Muslim, between temple and mosque. Born "
            "into a Muslim weaver family, initiated by the Hindu guru Ramananda, "
            "Kabir belonged to neither tradition and claimed both. 'I am at once "
            "the child of Allah and of Ram.' These songs challenge all religious "
            "exclusivism and point to a truth beyond any single tradition."
        ),
        "for_readers": (
            "In an age of religious division, Kabir's syncretism feels prophetic. "
            "These songs do not propose a bland universalism but a fierce insistence "
            "that the Beloved cannot be contained by any human institution. Read them "
            "as an invitation to examine your own boundaries — where do you draw "
            "lines that the Infinite does not recognize?"
        ),
    },
]


def build_grammar(poems):
    """Build the complete grammar.json structure."""
    items = []

    # L1: Individual songs
    for poem in poems:
        song_id = f"song-{poem['song_number']:03d}"
        name = f"Song {poem['roman']}: {poem['first_line']}"
        if len(name) > 80:
            name = name[:77] + "..."

        item = {
            "id": song_id,
            "name": name,
            "sort_order": poem["song_number"],
            "category": "song",
            "level": 1,
            "sections": {
                "Verse": poem["verse"],
            },
            "keywords": ["kabir", "devotional", "poetry"],
            "metadata": {
                "song_number": poem["song_number"],
                "roman_numeral": poem["roman"],
                "reference": poem["reference"],
                "hindi_title": poem["hindi_title"],
            },
        }
        items.append(item)

    # Build a set of valid song IDs for composite_of references
    valid_ids = {item["id"] for item in items}

    # L2: Thematic emergence groups
    sort_base = 200
    for i, theme in enumerate(THEMES):
        composite = [f"song-{n:03d}" for n in theme["songs"] if f"song-{n:03d}" in valid_ids]

        item = {
            "id": theme["id"],
            "name": theme["name"],
            "sort_order": sort_base + i,
            "category": "theme",
            "level": 2,
            "composite_of": composite,
            "relationship_type": "emergence",
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": ["kabir", "theme", "emergence"],
            "metadata": {},
        }
        items.append(item)

    # L3: Meta-category connecting all themes
    all_theme_ids = [t["id"] for t in THEMES]
    meta_item = {
        "id": "meta-songs-of-kabir",
        "name": "The Songs of Kabir",
        "sort_order": 300,
        "category": "meta",
        "level": 3,
        "composite_of": all_theme_ids,
        "relationship_type": "emergence",
        "sections": {
            "About": (
                "The hundred songs collected here represent the essential Kabir — "
                "a 15th-century Indian mystic who defied every category his world "
                "offered him. Muslim by birth, Hindu by initiation, neither by "
                "conviction, Kabir was a weaver who wove not only cloth but a "
                "spiritual vision that transcended all boundaries. His songs move "
                "between Sufi ecstasy and Vedantic clarity, between fierce social "
                "criticism and tender devotional longing. Seven thematic streams "
                "flow through this collection: the God within, the music of the "
                "cosmos, the illusion of appearances, the ache of love, the door "
                "of death, the guru's transmission, and the refusal of all "
                "religious walls."
            ),
            "For Readers": (
                "These songs were meant to be sung, not studied. They come from "
                "an oral tradition of weavers and wanderers, not from scholarly "
                "libraries. Read them aloud if you can. Let the repetitions and "
                "refrains work on you. Kabir does not argue — he sings, he "
                "provokes, he laughs. The themes overlap because Kabir's vision "
                "is unified: the Beloved within IS the unstruck music IS the "
                "dissolution of illusion IS the love that transcends all borders. "
                "Start anywhere. Follow what calls to you."
            ),
        },
        "keywords": ["kabir", "meta", "complete-collection"],
        "metadata": {},
    }
    items.append(meta_item)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Kabir", "date": "~1440-1518", "note": "Author"},
                {"name": "Rabindranath Tagore", "date": "1915", "note": "Translator from Hindi"},
                {"name": "Evelyn Underhill", "date": "1915", "note": "Introduction"},
            ],
        },
        "name": "Songs of Kabir",
        "description": (
            "100 devotional songs by the 15th-century Indian mystic poet Kabir, "
            "translated by Rabindranath Tagore with an introduction by Evelyn Underhill. "
            "Kabir was born Muslim, studied under a Hindu guru, and refused all religious "
            "boundaries: 'I am at once the child of Allah and of Ram.' His songs fuse Sufi "
            "ecstasy with Vedantic non-duality — the divine lover is found not in temples "
            "or mosques but in the breath, the heartbeat, the ordinary.\n\n"
            "Source: Project Gutenberg eBook #6519 (https://www.gutenberg.org/ebooks/6519)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Indian miniature paintings from the "
            "Mughal and Rajput traditions. Illustrations from early 20th century editions "
            "of Tagore's translations. Simple ink drawings in the Bengali tradition."
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "poetry", "devotional", "indian", "mysticism", "sacred-text",
            "public-domain", "full-text", "wisdom", "sufi", "vedanta", "syncretism",
        ],
        "roots": ["eastern-wisdom", "mysticism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "non-dual",
        "items": items,
    }

    return grammar


def main():
    print(f"Reading source: {INPUT_FILE}")
    lines = read_source()
    print(f"  Total lines: {len(lines)}")

    # Strip Gutenberg wrapper
    content_lines = strip_gutenberg(lines)
    print(f"  Content lines (after stripping Gutenberg): {len(content_lines)}")

    # Find where poems begin
    poems_start = find_poems_start(content_lines)
    print(f"  KABIR'S POEMS header at content line {poems_start}")

    # Parse poems from the poems section onward
    poem_lines = content_lines[poems_start:]
    poems = parse_poems(poem_lines)
    print(f"  Parsed {len(poems)} songs")

    if len(poems) != 100:
        print(f"  WARNING: Expected 100 songs, got {len(poems)}", file=sys.stderr)

    # Show first few for verification
    for p in poems[:3]:
        print(f"    Song {p['roman']} ({p['song_number']}): {p['first_line'][:50]}...")
        print(f"      Ref: {p['reference']}  Hindi: {p['hindi_title'][:40]}")
    print(f"    ...")
    for p in poems[-2:]:
        print(f"    Song {p['roman']} ({p['song_number']}): {p['first_line'][:50]}...")

    # Build grammar
    grammar = build_grammar(poems)

    # Count items by level
    l1 = sum(1 for item in grammar["items"] if item["level"] == 1)
    l2 = sum(1 for item in grammar["items"] if item["level"] == 2)
    l3 = sum(1 for item in grammar["items"] if item["level"] == 3)
    print(f"\n  Grammar items: {len(grammar['items'])} total ({l1} L1, {l2} L2, {l3} L3)")

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"\n  Written to: {OUTPUT_FILE}")
    print("  Done!")


if __name__ == "__main__":
    main()
