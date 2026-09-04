#!/usr/bin/env python3
"""
Build grammar.json for Gitanjali (Song Offerings) by Rabindranath Tagore.
Source: Project Gutenberg eBook #7164

Parses 103 prose poems from the Gutenberg plain text, creates L1 items
for each poem and L2/L3 thematic emergence groups.
"""

import json
import re
import os

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'gitanjali.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'gitanjali')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = '*** START OF THE PROJECT GUTENBERG EBOOK GITANJALI ***'
    end_marker = '*** END OF THE PROJECT GUTENBERG EBOOK GITANJALI ***'

    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text


def skip_introduction(text):
    """Skip Yeats' introduction, find the GITANJALI header before poem 1."""
    # Look for the GITANJALI header that precedes the poems
    match = re.search(r'\nGITANJALI\s*\n', text)
    if match:
        text = text[match.end():]
    return text


def parse_poems(text):
    """Parse 103 numbered prose poems."""
    poems = {}

    # Split on poem number markers: a number followed by period on its own line
    # Pattern: start of line, number, period, end of line
    pattern = re.compile(r'^(\d+)\.\s*$', re.MULTILINE)

    matches = list(pattern.finditer(text))

    for i, match in enumerate(matches):
        poem_num = int(match.group(1))
        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        poem_text = text[start:end].strip()
        # Normalize whitespace within paragraphs but preserve paragraph breaks
        paragraphs = re.split(r'\n\s*\n', poem_text)
        cleaned_paragraphs = []
        for p in paragraphs:
            # Join lines within a paragraph
            cleaned = ' '.join(p.split())
            if cleaned:
                cleaned_paragraphs.append(cleaned)

        poems[poem_num] = '\n\n'.join(cleaned_paragraphs)

    return poems


def truncate_name(text, max_len=80):
    """Get first line of poem, truncated to max_len chars."""
    first_line = text.split('\n')[0].strip()
    if len(first_line) <= max_len:
        return first_line
    # Truncate at word boundary
    truncated = first_line[:max_len]
    last_space = truncated.rfind(' ')
    if last_space > max_len // 2:
        truncated = truncated[:last_space]
    return truncated + '...'


def build_l2_themes():
    """Define L2 thematic emergence groups."""
    return [
        {
            "id": "theme-infinite-gift",
            "name": "The Infinite Gift",
            "poems": [1, 2, 5, 17, 34, 56, 75, 103],
            "about": "Poems about God's boundless giving and the soul's smallness before infinity. Tagore returns again and again to the image of tiny hands receiving endless gifts, a small vessel filled and emptied and filled again. These poems hold the paradox at the heart of devotion: the infinite chooses to pour itself into the finite, and the finite can never be full.",
            "for_readers": "Read these when you feel small before something vast -- the night sky, a great love, the mystery of being alive at all. Let Tagore's wonder at receiving become your own. These poems are medicine for scarcity thinking: they insist that the universe is generous beyond measure."
        },
        {
            "id": "theme-beloved-arrival",
            "name": "The Beloved's Arrival",
            "poems": [9, 14, 19, 23, 31, 44, 63, 78, 97],
            "about": "Poems of longing, anticipation, and the lover-God arriving at the door. The beloved in Gitanjali is always approaching -- footsteps in the corridor, a knock at midnight, a presence felt but not yet seen. Tagore inhabits the ache of waiting with such tenderness that the longing itself becomes a form of communion.",
            "for_readers": "These poems speak to anyone who has waited -- for a person, for meaning, for grace. They transform waiting from passive emptiness into active devotion. Read them slowly, one at a time, and notice how Tagore makes the threshold between absence and presence shimmer."
        },
        {
            "id": "theme-surrender-service",
            "name": "Surrender and Service",
            "poems": [10, 11, 15, 26, 36, 48, 53, 73, 87],
            "about": "Poems about offering one's work to God and finding joy in humble service. Here the poet is servant, instrument, and offering all at once. The act of creation itself becomes prayer -- not grand gestures but the daily labor of living offered upward. Tagore dissolves the boundary between sacred and mundane.",
            "for_readers": "Read these when your work feels meaningless or when you need to remember why you do what you do. Tagore suggests that every act of honest labor is a form of worship. These poems pair beautifully with the Bhagavad Gita's teaching on karma yoga -- action without attachment to results."
        },
        {
            "id": "theme-nature-prayer",
            "name": "Nature as Prayer",
            "poems": [25, 27, 30, 39, 40, 57, 59, 64, 68, 72],
            "about": "Poems where dawn, rain, flowers, rivers, and the turning seasons speak of the divine. For Tagore, nature is not metaphor for God -- it is God's own speech. The monsoon rain is not 'like' grace; it is grace. These poems collapse the distance between the natural world and the sacred, finding temple in every garden.",
            "for_readers": "Take these poems outside. Read them under a tree, beside water, in rain. They are meant to be read with bare feet on grass. If you love the natural world but struggle with traditional religious language, Tagore offers a bridge: here is devotion that smells of wet earth and jasmine."
        },
        {
            "id": "theme-death-departure",
            "name": "Death and Departure",
            "poems": [82, 83, 86, 87, 90, 91, 93, 95, 96],
            "about": "Poems about dying as returning home, parting as reunion, and the dissolution of self into the eternal. The final movement of Gitanjali turns toward death with extraordinary serenity. For Tagore, death is not ending but homecoming -- the river reaching the sea, the lamp extinguished because dawn has come. These poems carry no fear, only a quiet readiness.",
            "for_readers": "These poems are for times of grief, for contemplating mortality, for sitting with someone who is dying. They offer neither false comfort nor despair, but a profound trust in the wholeness of the cycle. W.B. Yeats singled out these poems as among the most moving: 'And because I love this life, I know I shall love death as well.'"
        },
        {
            "id": "theme-child",
            "name": "The Child",
            "poems": [60, 61, 62, 65, 80, 84],
            "about": "Poems about children, innocence, and the wisdom of play. Tagore was a lifelong educator who founded a school (Santiniketan) based on the belief that children learn best in nature, through wonder. These poems see the child not as incomplete adult but as natural mystic -- building sand houses, playing with shells, knowing without knowing.",
            "for_readers": "Read these to or with children, but also read them alone to recover your own sense of play. Tagore suggests that the child's relationship to the world -- immediate, trusting, astonished -- is the very relationship the mystic labors to recover. These poems pair well with his essay collection 'The Crescent Moon.'"
        },
        {
            "id": "theme-journey",
            "name": "The Journey",
            "poems": [12, 18, 22, 37, 46, 47, 55, 76, 98, 100],
            "about": "Poems about the path, the road, the pilgrimage of life. Tagore's traveler is always in motion -- setting out at dawn, crossing rivers, walking dusty roads. But the journey is not toward a distant goal; it is the discovery that every step is already arrival. The road itself is the temple.",
            "for_readers": "These poems are companions for transitions -- starting something new, leaving something behind, feeling lost in the middle of life. They insist that the journey matters more than the destination, that getting lost is a form of finding. Read them when you need courage to keep walking."
        },
        {
            "id": "theme-joy-celebration",
            "name": "Joy and Celebration",
            "poems": [3, 4, 6, 7, 16, 28, 57, 69, 74, 99],
            "about": "Poems of ecstatic praise, singing, dancing, and the sheer overflow of being alive. Here Tagore is at his most exuberant -- the poet who cannot contain his joy, whose songs burst from him like birds from a cage. These poems celebrate existence itself as gift, music, and festival.",
            "for_readers": "Read these aloud. They are meant to be sung, and even in English prose translation they carry rhythm and exaltation. These are poems for good days, for gratitude, for moments when the world suddenly looks unbearably beautiful. Let them amplify whatever joy you already carry."
        },
    ]


def build_grammar(poems):
    """Build the complete grammar.json structure."""
    items = []
    sort_order = 0

    # L1: Individual poems
    for num in range(1, 104):
        if num not in poems:
            print(f"WARNING: Poem {num} not found!")
            continue

        poem_text = poems[num]
        item = {
            "id": f"poem-{num:03d}",
            "name": truncate_name(poem_text),
            "sort_order": sort_order,
            "category": "poem",
            "level": 1,
            "sections": {
                "Verse": poem_text
            },
            "keywords": [],
            "metadata": {
                "poem_number": num
            }
        }
        items.append(item)
        sort_order += 1

    # L2: Thematic emergence groups
    themes = build_l2_themes()
    for theme in themes:
        composite_ids = [f"poem-{n:03d}" for n in theme["poems"]]
        item = {
            "id": theme["id"],
            "name": theme["name"],
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"]
            },
            "keywords": [],
            "metadata": {
                "composite_of": composite_ids,
                "relationship_type": "emergence"
            }
        }
        items.append(item)
        sort_order += 1

    # L3: Meta-category
    all_theme_ids = [t["id"] for t in themes]
    l3_item = {
        "id": "song-offerings",
        "name": "Song Offerings",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Gitanjali means 'Song Offerings' -- from the Bengali 'gita' (song) and 'anjali' (offering, as in cupped hands raised in devotion). These 103 prose poems, translated from Bengali by Tagore himself in 1912, move through the full arc of devotional experience: wonder at creation, longing for the divine beloved, surrender through service, communion with nature, the innocence of children, the pilgrimage of life, ecstatic celebration, and finally the serene acceptance of death as homecoming. Together they form one continuous prayer -- a single salutation that begins in smallness and ends in infinity.",
            "For Readers": "Gitanjali can be read straight through as a devotional arc, or dipped into at random like an oracle. The thematic groupings here offer a middle path: follow one thread (nature, death, joy) and discover how Tagore circles the same mysteries from different angles. These poems belong to no single religion -- they have been claimed by Hindus, Christians, Sufis, and secular humanists alike. Tagore himself resisted labels: 'My religion is in the reconciliation of the superpersonal Man, the universal human spirit, in my own individual being.'"
        },
        "keywords": ["devotion", "bengali", "nobel-prize", "prayer", "offering"],
        "metadata": {
            "composite_of": all_theme_ids,
            "relationship_type": "emergence"
        }
    }
    items.append(l3_item)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Rabindranath Tagore", "date": "1912", "note": "Author and translator from Bengali"},
                {"name": "W.B. Yeats", "date": "1912", "note": "Introduction"}
            ]
        },
        "name": "Gitanjali: Song Offerings",
        "description": "Gitanjali ('Song Offerings'), 103 prose poems by Rabindranath Tagore, translated from Bengali by the author himself. These devotional poems won the 1913 Nobel Prize in Literature \u2014 the first non-European to receive it. W.B. Yeats wrote in his introduction: 'I have carried the manuscript of these translations about with me for days, reading it in railway trains, or on the top of omnibuses and in restaurants, and I have often had to close it lest some stranger would see how much it moved me.'\n\nSource: Project Gutenberg eBook #7164 (https://www.gutenberg.org/ebooks/7164)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Abanindranath Tagore's Bengal School paintings, Nandalal Bose's ink wash illustrations. The gentle watercolor style of early 20th century Bengali art \u2014 lotus flowers, rivers, figures in devotion.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["poetry", "devotional", "indian", "bengali", "sacred-text", "public-domain", "full-text", "wisdom", "nobel-prize"],
        "roots": ["eastern-wisdom"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "devotional",
        "items": items
    }

    return grammar


def main():
    # Read source
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        text = f.read()

    # Strip Gutenberg wrapper
    text = strip_gutenberg(text)

    # Skip Yeats' introduction
    text = skip_introduction(text)

    # Parse poems
    poems = parse_poems(text)

    print(f"Parsed {len(poems)} poems")

    # Verify we got all 103
    missing = [n for n in range(1, 104) if n not in poems]
    if missing:
        print(f"WARNING: Missing poems: {missing}")

    # Verify poem numbers
    unexpected = [n for n in poems if n < 1 or n > 103]
    if unexpected:
        print(f"WARNING: Unexpected poem numbers: {unexpected}")

    # Build grammar
    grammar = build_grammar(poems)

    # Count items by level
    l1_count = sum(1 for item in grammar['items'] if item['level'] == 1)
    l2_count = sum(1 for item in grammar['items'] if item['level'] == 2)
    l3_count = sum(1 for item in grammar['items'] if item['level'] == 3)
    print(f"L1 items: {l1_count}")
    print(f"L2 items: {l2_count}")
    print(f"L3 items: {l3_count}")
    print(f"Total items: {len(grammar['items'])}")

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
