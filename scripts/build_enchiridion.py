#!/usr/bin/env python3
"""
Parse The Enchiridion (Epictetus, Higginson translation, Gutenberg #45109)
into a grammar.json.

Structure:
- L1: 51 individual maxims (sections I through LI)
- L2: Thematic emergence groups (6 themes)
- L3: "The Stoic Path" meta-category
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "enchiridion.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "enchiridion")
OUTPUT = os.path.join(OUTPUT_DIR, "grammar.json")


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1:
        text = text[text.index("\n", start) + 1:]
    if end != -1:
        text = text[:end]
    return text.strip()


def roman_to_int(s):
    """Convert a Roman numeral string to an integer."""
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    result = 0
    prev = 0
    for ch in reversed(s):
        val = roman_values[ch]
        if val < prev:
            result -= val
        else:
            result += val
        prev = val
    return result


# Roman numeral pattern: matches I through LI
# Covers: I-III, IV, V-VIII, IX, X-XIII, XIV, XV-XVIII, XIX, XX-XXIII, XXIV,
#         XXV-XXVIII, XXIX, XXX-XXXIII, XXXIV, XXXV-XXXVIII, XXXIX,
#         XL-XLIII, XLIV, XLV-XLVIII, XLIX, L, LI
ROMAN_RE = re.compile(
    r'^'
    r'((?:XL|L)(?:IX|IV|V?I{0,3})|'   # 40-49, 50-53
    r'XXX(?:IX|IV|V?I{0,3})|'          # 30-39
    r'XX(?:IX|IV|V?I{0,3})|'           # 20-29
    r'X(?:IX|IV|V?I{0,3})|'            # 10-19
    r'(?:IX|IV|VI{0,3}|V|I{1,3}))'     # 1-9
    r'(?:\[\d+\])?'                     # optional footnote marker like [2]
    r'$'
)


def parse_sections(text):
    """Parse the 51 numbered sections from the Enchiridion.

    Format: centered Roman numeral on its own line, then text paragraphs below.
    We skip the introduction and start at 'THE ENCHIRIDION' header.
    """
    lines = text.split('\n')

    # Find the start: "THE ENCHIRIDION" header (the one after the introduction)
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == "THE ENCHIRIDION":
            start_idx = i
            break

    # Find all section headers (Roman numerals centered on their own line)
    section_starts = []  # list of (section_number, line_index)

    for i in range(start_idx, len(lines)):
        stripped = lines[i].strip()
        if not stripped:
            continue

        m = ROMAN_RE.match(stripped)
        if not m:
            continue

        numeral = m.group(1)
        if not numeral:
            continue

        num = roman_to_int(numeral)

        # Sanity: must be in range 1-51 and must be preceded by blank line
        if num < 1 or num > 51:
            continue

        # Check for blank line before (to avoid matching stray Roman numerals
        # in text or bibliography)
        has_blank_before = False
        for j in range(i - 1, max(i - 3, -1), -1):
            if not lines[j].strip():
                has_blank_before = True
                break
        if not has_blank_before:
            continue

        # Verify sequential order
        if section_starts and num <= section_starts[-1][0]:
            continue

        section_starts.append((num, i))

    # Extract section texts
    sections = []
    for idx, (num, line_idx) in enumerate(section_starts):
        # End boundary: next section start or end of text
        if idx + 1 < len(section_starts):
            end_idx = section_starts[idx + 1][1]
        else:
            # Find Footnotes section or end
            end_idx = len(lines)
            for i in range(line_idx + 1, len(lines)):
                stripped = lines[i].strip()
                if stripped == "Footnotes" or stripped.startswith("[1]"):
                    end_idx = i
                    break

        # Collect text lines (skip the Roman numeral header line itself)
        text_lines = lines[line_idx + 1:end_idx]
        section_text = '\n'.join(text_lines).strip()

        # Clean up: remove footnote markers like [1], [2], etc.
        section_text = re.sub(r'\[(\d+)\]', '', section_text)

        # Clean up excessive whitespace
        section_text = re.sub(r'\n{3,}', '\n\n', section_text)
        section_text = section_text.strip()

        sections.append({
            "number": num,
            "text": section_text,
        })

    return sections


# Thematic groupings for L2 emergence
# Roman numeral references converted to section numbers
THEMES = [
    {
        "id": "theme-dichotomy-of-control",
        "name": "What Is In Our Power",
        "sections": [1, 2, 5, 6, 9, 11, 14, 19, 32],
        "about": "The foundation of Stoic practice: distinguishing what is 'up to us' (opinion, desire, aversion, action) from what is not (body, property, reputation, office). Epictetus opens the Enchiridion with this dichotomy because everything else follows from it. If you master this single distinction, you are free. If you do not, you are enslaved — regardless of your external circumstances.",
        "for_readers": "This is the core of Stoic resilience. When you feel anxious or upset, ask: 'Is this within my power or not?' If not, practice releasing it. If so, focus your energy there. This simple question is the ancestor of cognitive behavioral therapy's distinction between what we can and cannot control."
    },
    {
        "id": "theme-desire-and-aversion",
        "name": "Desire and Aversion",
        "sections": [2, 3, 4, 5, 26, 34],
        "about": "Epictetus teaches that suffering arises from desiring what we cannot control and fearing what we cannot avoid. The practice is not to eliminate desire but to redirect it — desire only what is within your power, and you will never be disappointed. Avert only from what you can actually avoid, and you will never be trapped.",
        "for_readers": "Notice what you are craving or dreading right now. Is it something within your power? If you desire another person's approval, wealth, or health, you have handed your happiness to fortune. Practice desiring only your own right action, your own clear judgment. This is the Stoic path to contentment."
    },
    {
        "id": "theme-social-relations",
        "name": "Social Relations",
        "sections": [12, 13, 15, 16, 17, 24, 25, 33, 36, 42],
        "about": "Stoicism is not withdrawal from the world but engagement with it on different terms. These maxims address how to maintain inner freedom while participating in social life — handling insults, dining with others, responding to praise and blame, fulfilling social duties. The Stoic does not avoid people but refuses to be disturbed by them.",
        "for_readers": "Social anxiety, people-pleasing, and resentment all arise from placing too much weight on others' opinions. These sections offer practical guidance: when someone insults you, the injury is in your reaction, not their words. When you dine with others, take what is offered without grasping. When you fulfill your roles (parent, citizen, friend), do so from duty, not from need for approval."
    },
    {
        "id": "theme-appearances-and-judgment",
        "name": "Appearances and Judgment",
        "sections": [5, 6, 8, 10, 16, 20, 26, 27, 34, 45],
        "about": "We are disturbed not by things but by our judgments about things. This is perhaps Epictetus's most famous teaching and the direct ancestor of cognitive therapy. Every external event is neutral — it is our interpretation (phantasia, 'appearance') that makes it good or bad. The practice is to examine every impression before assenting to it.",
        "for_readers": "When something upsets you, pause. The event itself is not the problem — your judgment of it is. 'This is terrible' is an interpretation, not a fact. Epictetus teaches us to say: 'This is an appearance. Let me examine whether it concerns what is in my power.' Aaron Beck and Albert Ellis built modern CBT on exactly this Stoic insight."
    },
    {
        "id": "theme-practice-of-philosophy",
        "name": "The Practice of Philosophy",
        "sections": [46, 47, 48, 49, 50, 51],
        "about": "The final sections of the Enchiridion turn from individual maxims to the question of philosophical practice itself. How does one become a philosopher — not in theory but in life? Epictetus insists that philosophy is not about reading or debating but about transforming one's character. The philosopher is known by what they do, not what they say.",
        "for_readers": "These closing maxims are Epictetus's challenge to the reader: will you merely read this handbook, or will you live it? Philosophy is practice, not performance. Do not boast about your principles — embody them. Do not quote Chrysippus — act in harmony with nature. The Enchiridion is not a text to be studied but a manual to be used."
    },
    {
        "id": "theme-accepting-fate",
        "name": "Accepting Fate",
        "sections": [3, 8, 11, 17, 27, 31, 37, 51],
        "about": "Amor fati — love of fate — runs throughout Stoic thought. Epictetus teaches not merely passive acceptance but active embrace: 'Demand not that events should happen as you wish; but wish them to happen as they do happen, and you will go on well.' This is not resignation but alignment with cosmic order (logos). What happens is what was meant to happen; your task is to respond with virtue.",
        "for_readers": "When life delivers what you did not choose — loss, illness, disappointment — these maxims offer a radical reframe. Instead of 'Why is this happening to me?', ask 'How can I respond to this with excellence?' The Stoic does not fight reality. They work with it, finding freedom not in controlling circumstances but in choosing their response."
    },
]


def build_grammar(sections):
    items = []
    sort_order = 0

    # L1: Individual maxims
    for sec in sections:
        sort_order += 1
        # Create a short name from the first line
        first_line = sec["text"].split("\n")[0].strip()
        # Truncate for display
        if len(first_line) > 80:
            first_line = first_line[:77] + "..."

        items.append({
            "id": f"maxim-{sec['number']:02d}",
            "name": f"Maxim {sec['number']}: {first_line}",
            "level": 1,
            "category": "maxim",
            "sort_order": sort_order,
            "sections": {
                "Maxim": sec["text"]
            },
            "keywords": [],
            "metadata": {
                "section_number": sec["number"],
            }
        })

    # L2: Thematic groupings
    for theme in THEMES:
        sort_order += 1
        composite = [f"maxim-{n:02d}" for n in theme["sections"]]
        items.append({
            "id": theme["id"],
            "name": theme["name"],
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": composite,
            "sort_order": sort_order,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "section_count": len(theme["sections"]),
                "section_numbers": theme["sections"],
            }
        })

    # L3: The Stoic Path (meta connecting all themes)
    sort_order += 1
    items.append({
        "id": "meta-stoic-path",
        "name": "The Stoic Path",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": [t["id"] for t in THEMES],
        "sort_order": sort_order,
        "sections": {
            "About": "The Enchiridion is a single path with many aspects. The dichotomy of control is the foundation; managing desire and aversion is the daily practice; social relations are the testing ground; examining appearances is the method; accepting fate is the disposition; and becoming a philosopher is the goal. These six themes are not separate teachings but facets of one discipline: living in accordance with nature, maintaining inner freedom regardless of external circumstances, and finding tranquility through the exercise of reason and virtue. Epictetus distilled decades of Stoic teaching into this compact manual — a handbook small enough to carry into battle, into the forum, into grief. Twenty centuries later, it remains the most practical introduction to the examined life.",
        },
        "keywords": [],
        "metadata": {
            "theme_count": len(THEMES),
        }
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    sections = parse_sections(text)
    print(f"Parsed {len(sections)} sections")

    if len(sections) != 51:
        print(f"WARNING: Expected 51 sections, got {len(sections)}")
        for sec in sections:
            print(f"  Section {sec['number']}: {sec['text'][:60]}...")
        return

    items = build_grammar(sections)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Epictetus", "date": "~135 CE", "note": "Author (compiled by Arrian)"},
                {"name": "Thomas Wentworth Higginson", "date": "1948", "note": "English translator"},
            ]
        },
        "name": "The Enchiridion",
        "description": "The Enchiridion ('Handbook') of Epictetus, a concise manual of Stoic ethics compiled by his student Arrian. 51 maxims on what is in our power vs. what is not \u2014 the foundation of Stoic practice that directly influenced CBT, DBT, and modern resilience psychology. Thomas Wentworth Higginson translation.\n\nSource: Project Gutenberg eBook #45109 (https://www.gutenberg.org/ebooks/45109)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Roman marble busts and sculpture. The Farnese Hercules, Capitoline Marcus Aurelius. Neoclassical engravings from 18th-century Epictetus editions.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "stoicism", "ethics", "sacred-text", "public-domain", "full-text", "wisdom", "resilience", "practice"],
        "roots": ["eastern-wisdom"],
        "shelves": ["resilience"],
        "lineages": ["Linehan"],
        "worldview": "rationalist",
        "items": items,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"Grammar written to {OUTPUT}")
    print(f"  L1: {l1} maxims, L2: {l2} thematic groups, L3: {l3} meta-categories")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    main()
