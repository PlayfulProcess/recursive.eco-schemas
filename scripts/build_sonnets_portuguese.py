#!/usr/bin/env python3
"""
Parser for Sonnets from the Portuguese by Elizabeth Barrett Browning.
Reads seeds/sonnets-from-portuguese.txt (Gutenberg #2002) and generates
grammars/sonnets-from-portuguese/grammar.json

44 sonnets numbered I through XLIV, with L2 thematic emergence groups
tracing the arc of a love story, and L3 meta-category.
"""

import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SEED_FILE = os.path.join(PROJECT_ROOT, "seeds", "sonnets-from-portuguese.txt")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "grammars", "sonnets-from-portuguese")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "grammar.json")


def roman_to_int(s):
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    for i in range(len(s)):
        if i + 1 < len(s) and vals[s[i]] < vals[s[i + 1]]:
            result -= vals[s[i]]
        else:
            result += vals[s[i]]
    return result


def int_to_roman(n):
    pairs = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    result = ''
    for value, numeral in pairs:
        while n >= value:
            result += numeral
            n -= value
    return result


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    lines = text.split('\n')
    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i + 1
        if end_marker in line:
            end_idx = i
            break

    return '\n'.join(lines[start_idx:end_idx])


def parse_sonnets(text):
    """Parse 44 sonnets from the stripped text."""
    lines = text.split('\n')

    # Skip the index of first lines and front matter.
    # Find where the actual sonnets begin: look for a line that is just "I"
    # after the INDEX OF FIRST LINES section.
    sonnet_start = None
    past_index = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "INDEX OF FIRST LINES":
            past_index = True
            continue
        # After the index, look for a standalone Roman numeral "I"
        if past_index and stripped == "I":
            sonnet_start = i
            break

    if sonnet_start is None:
        raise ValueError("Could not find start of sonnets")

    # Now parse sonnets from sonnet_start onward
    content_lines = lines[sonnet_start:]

    # Valid Roman numerals for sonnets I-XLIV
    valid_romans = set(int_to_roman(n) for n in range(1, 45))

    sonnets = []
    current_numeral = None
    current_lines = []

    for line in content_lines:
        stripped = line.strip()

        # Check if this line is a Roman numeral header
        if stripped in valid_romans and not current_lines_have_content(current_lines):
            # If we have a previous sonnet, save it
            if current_numeral is not None:
                sonnets.append((current_numeral, extract_poem(current_lines)))
            current_numeral = stripped
            current_lines = []
        elif stripped in valid_romans and current_numeral is not None:
            # New sonnet header after content - save previous
            sonnets.append((current_numeral, extract_poem(current_lines)))
            current_numeral = stripped
            current_lines = []
        else:
            current_lines.append(line)

    # Don't forget the last sonnet
    if current_numeral is not None:
        sonnets.append((current_numeral, extract_poem(current_lines)))

    return sonnets


def current_lines_have_content(lines):
    """Check if the accumulated lines have any actual poem content (non-blank)."""
    for line in lines:
        if line.strip():
            return True
    return False


def extract_poem(lines):
    """Extract the poem text from raw lines, stripping leading/trailing blanks."""
    # Find first and last non-empty lines
    poem_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            # Remove the leading indentation but preserve relative indentation
            poem_lines.append(line.rstrip())

    if not poem_lines:
        return ""

    # Find minimum indentation
    min_indent = float('inf')
    for line in poem_lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            min_indent = min(min_indent, indent)

    if min_indent == float('inf'):
        min_indent = 0

    # Strip common indentation
    result = []
    for line in poem_lines:
        if line.strip():
            result.append(line[min_indent:])
        else:
            result.append("")

    return '\n'.join(result)


def build_grammar(sonnets):
    """Build the full grammar.json structure."""
    if len(sonnets) != 44:
        raise ValueError(f"Expected 44 sonnets, got {len(sonnets)}")

    items = []

    # L1: Individual sonnets
    for numeral, poem_text in sonnets:
        num = roman_to_int(numeral)
        sonnet_id = f"sonnet-{num:02d}"

        first_line = poem_text.split('\n')[0].strip()
        # Truncate first line to 50 chars for the name
        if len(first_line) > 50:
            truncated = first_line[:50].rstrip()
            # Try to break at a word boundary
            last_space = truncated.rfind(' ')
            if last_space > 30:
                truncated = truncated[:last_space]
            truncated += "..."
        else:
            truncated = first_line

        name = f"Sonnet {numeral}: {truncated}"

        items.append({
            "id": sonnet_id,
            "name": name,
            "sort_order": num,
            "category": "sonnet",
            "level": 1,
            "sections": {
                "Verse": poem_text
            },
            "keywords": extract_keywords(poem_text, num),
            "metadata": {
                "sonnet_number": num,
                "first_line": first_line
            }
        })

    # L2: Thematic emergence groups
    l2_groups = [
        {
            "id": "awakening-to-love",
            "name": "Awakening to Love",
            "sort_order": 45,
            "sonnets": list(range(1, 8)),
            "about": "The sequence opens with the shock of love arriving unbidden. Barrett Browning had resigned herself to illness, solitude, and death when Robert Browning's letters broke through her sealed world. These seven sonnets capture the trembling disbelief of a woman who thought love had passed her by — the mystical voice that says 'Not Death, but Love,' the three witnesses in God's universe, the self-deprecation of one who sees herself as unworthy. Love arrives not as comfort but as earthquake.",
            "for_readers": "Read these sonnets as a portrait of what it feels like when something you'd given up on suddenly becomes possible. Notice how Barrett Browning uses images of death, shadow, and weeping even as love enters — the joy is inseparable from the terror of hoping again. These are sonnets for anyone who has been surprised by love after loss."
        },
        {
            "id": "resistance-and-surrender",
            "name": "Resistance and Surrender",
            "sort_order": 46,
            "sonnets": list(range(8, 15)),
            "about": "Having felt love's arrival, Barrett Browning now wrestles with it. Can she give what she has? Is it right to accept what is offered? These sonnets move between generosity and self-doubt, between the desire to fashion love into speech and the fear that words will cheapen it. The famous Sonnet XIV ('If thou must love me, let it be for nought') is the hinge — love must be for love's sake alone, not for pity or for any quality that time might change.",
            "for_readers": "These are the sonnets of anyone who has tried to talk themselves out of love, who has listed all the reasons it cannot work. Watch how Barrett Browning's resistance gradually softens — not because she is conquered, but because love proves itself patient enough to outlast her objections. The surrender is not defeat but recognition."
        },
        {
            "id": "growing-into-love",
            "name": "Growing Into Love",
            "sort_order": 47,
            "sonnets": list(range(15, 23)),
            "about": "The resistance breaks. Barrett Browning begins to let love reshape her. She gives a lock of hair, acknowledges the soul's commerce, asks to hear 'I love you' again and again. The poet who could barely believe in love now stands erect and strong beside her beloved, imagining their two souls meeting. These sonnets chart the slow, brave work of learning to receive — to let joy in without immediately preparing for its loss.",
            "for_readers": "Pay attention to the transformation happening sonnet by sonnet. The heavy heart of the early poems is being replaced by something lighter, though never naive. Barrett Browning earns her joy through honesty about her fears. These sonnets speak to the courage required not just to love, but to let yourself be loved."
        },
        {
            "id": "love-in-full-bloom",
            "name": "Love in Full Bloom",
            "sort_order": 48,
            "sonnets": list(range(23, 31)),
            "about": "Joy arrives — not the giddy joy of new infatuation, but the deep gladness of love that has been tested and found true. Barrett Browning writes of visions replaced by a living presence, of thoughts that twine and bud like vines, of seeing the beloved's image through grateful tears. The world's sharpness folds shut like a clasping knife. These are the sonnets of a woman who has crossed from fear to trust and found the other side more beautiful than she imagined.",
            "for_readers": "These sonnets are best read aloud and slowly. They carry the warmth of embodied love — not abstract devotion but the real, physical, daily experience of being with someone who has transformed your world. Notice how Barrett Browning's imagery shifts from shadow and death to flowers, light, and growing things."
        },
        {
            "id": "loves-permanence",
            "name": "Love's Permanence",
            "sort_order": 49,
            "sonnets": list(range(31, 36)),
            "about": "Love having arrived and been accepted, Barrett Browning now asks: will it last? These sonnets confront the fear of impermanence head-on. The sun rises on an oath; a pet-name becomes a talisman; she offers to leave everything behind. The tension between the eternal feeling of love and the mortal bodies that contain it produces some of the most poignant writing in the sequence.",
            "for_readers": "These are the sonnets of commitment — the moment when love stops being a feeling and becomes a vow. Barrett Browning does not pretend that permanence is easy or guaranteed. She earns it through unflinching honesty about what must be given up and what might be lost. Read these when you need courage to commit."
        },
        {
            "id": "the-beloved",
            "name": "The Beloved",
            "sort_order": 50,
            "sonnets": list(range(36, 45)),
            "about": "The final nine sonnets turn outward to celebrate the beloved directly. Barrett Browning moves from her own inner drama to address Robert with growing confidence and tenderness. The sequence builds to the magnificent Sonnet XLIII ('How do I love thee? Let me count the ways') and closes with XLIV, offering the poems themselves as flowers gathered from the garden of her heart. The woman who began in shadow ends in light, giving her art as a gift of love.",
            "for_readers": "This is the culmination of the entire sequence. The poet who could barely accept love now overflows with it. Sonnet XLIII is justly famous, but read it in context — after the forty-two sonnets of struggle, resistance, and gradual opening, its declaration lands with the full weight of everything that came before. The final sonnet, offering these poems as flowers, is one of the most graceful endings in all of poetry."
        }
    ]

    for group in l2_groups:
        composite_ids = [f"sonnet-{n:02d}" for n in group["sonnets"]]
        items.append({
            "id": group["id"],
            "name": group["name"],
            "sort_order": group["sort_order"],
            "category": "theme",
            "level": 2,
            "composite_of": composite_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": group["about"],
                "For Readers": group["for_readers"]
            },
            "keywords": [],
            "metadata": {}
        })

    # L3: Meta-category
    l3_composite = [g["id"] for g in l2_groups]
    items.append({
        "id": "love-story-in-sonnets",
        "name": "A Love Story in Sonnets",
        "sort_order": 51,
        "category": "arc",
        "level": 3,
        "composite_of": l3_composite,
        "relationship_type": "emergence",
        "sections": {
            "About": "The forty-four Sonnets from the Portuguese trace one of literature's great love stories from first trembling to full-throated declaration. Elizabeth Barrett Browning wrote them in secret during her courtship with Robert Browning (1845-1846), and they were published in 1850 under the fiction that they were translations from Portuguese — a private joke, since Robert called Elizabeth 'my little Portuguese' after her poem 'Catarina to Camoens.' The arc moves through six phases: the shock of love arriving to a woman who expected only death; her fierce resistance and eventual surrender; the slow, brave work of learning to trust; love in full bloom; the confrontation with permanence and mortality; and finally, the celebration of the beloved himself. Read as a sequence, they form a complete narrative of transformation — from isolation to communion, from grief to gratitude, from silence to song.",
            "For Readers": "To experience the full power of this sequence, read the sonnets in order from I to XLIV in a single sitting. The arc is cumulative — each sonnet builds on what came before. You will feel the resistance slowly melt, the imagery shift from shadow to light, the voice grow from whisper to song. This is not just one of the greatest love poems in English — it is one of the greatest love stories, told entirely in the first person, entirely in the present tense of feeling."
        },
        "keywords": ["love-story", "courtship", "transformation", "victorian", "sonnets"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Elizabeth Barrett Browning", "date": "1850", "note": "Author"}
            ]
        },
        "name": "Sonnets from the Portuguese",
        "description": "44 love sonnets by Elizabeth Barrett Browning, written during her courtship with Robert Browning (1845-1846) and published in 1850. 'How do I love thee? Let me count the ways' (Sonnet XLIII) is among the most famous love poems in English. The title was a disguise \u2014 Browning called his wife 'my little Portuguese,' and the poems were presented as translations rather than the deeply personal love letters they truly were.\n\nSource: Project Gutenberg eBook #2002 (https://www.gutenberg.org/ebooks/2002)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Pre-Raphaelite paintings by Dante Gabriel Rossetti, Edward Burne-Jones. The Rossetti portrait of Elizabeth Siddal. William Morris's floral borders and Arts and Crafts typography.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["poetry", "love", "sonnets", "victorian", "public-domain", "full-text", "romance"],
        "roots": ["emotion-love"],
        "shelves": ["wonder"],
        "lineages": ["Johnson"],
        "worldview": "devotional",
        "items": items
    }

    return grammar


def extract_keywords(poem_text, sonnet_number):
    """Extract a few relevant keywords from each sonnet."""
    keywords = ["love", "sonnet"]

    text_lower = poem_text.lower()

    keyword_map = {
        "death": "death",
        "heart": "heart",
        "soul": "soul",
        "tears": "tears",
        "god": "God",
        "kiss": "kiss",
        "beloved": "beloved",
        "angels": "angels",
        "silence": "silence",
        "flowers": "flowers",
        "music": "music",
        "grief": "grief",
        "hope": "hope",
        "light": "light",
        "shadow": "shadow",
        "weep": "weeping",
    }

    for trigger, kw in keyword_map.items():
        if trigger in text_lower:
            keywords.append(kw)

    return list(dict.fromkeys(keywords))  # deduplicate preserving order


def main():
    # Read seed file
    with open(SEED_FILE, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Strip Gutenberg header/footer
    text = strip_gutenberg(raw_text)

    # Parse sonnets
    sonnets = parse_sonnets(text)

    print(f"Parsed {len(sonnets)} sonnets")
    for numeral, poem in sonnets:
        num = roman_to_int(numeral)
        first_line = poem.split('\n')[0].strip()
        line_count = len([l for l in poem.split('\n') if l.strip()])
        print(f"  {numeral:>6} (#{num:02d}): {first_line[:60]}  [{line_count} lines]")

    # Build grammar
    grammar = build_grammar(sonnets)

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {OUTPUT_FILE}")
    print(f"Total items: {len(grammar['items'])} (44 L1 + 6 L2 + 1 L3)")


if __name__ == "__main__":
    main()
