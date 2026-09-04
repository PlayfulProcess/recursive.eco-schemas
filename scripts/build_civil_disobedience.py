#!/usr/bin/env python3
"""
Parse Civil Disobedience (Thoreau, Gutenberg #71) into a grammar.json.

Structure:
- L1: Individual paragraphs (double-newline separated)
- L2: Thematic emergence groups (6 themes, assigned by position)
- L3: The complete essay
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "civil-disobedience.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "civil-disobedience")
OUTPUT = os.path.join(OUTPUT_DIR, "grammar.json")


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    if start != -1:
        text = text[text.index("\n", start) + 1:]
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if end != -1:
        text = text[:end]
    return text.strip()


def strip_title_block(text):
    """Remove the title/author block at the top of the essay text.

    The text after Gutenberg header starts with:
      On the Duty of Civil Disobedience
      by Henry David Thoreau
      1849, original title: Resistance to Civil Government

    We skip to the first real paragraph which starts with 'I heartily accept'.
    """
    # Find the first paragraph of the actual essay
    marker = "I heartily accept the motto"
    idx = text.find(marker)
    if idx != -1:
        return text[idx:]
    return text


def extract_first_sentence(text, max_len=80):
    """Extract the first sentence from a paragraph, truncated to max_len chars."""
    # Clean up underscores (italic markers) for the name
    clean = re.sub(r'_([^_]+)_', r'\1', text)
    # Remove leading whitespace on each line and join
    clean = ' '.join(clean.split())

    # Try to find end of first sentence
    # Look for sentence-ending punctuation followed by space or end
    m = re.search(r'[.!?]["\u201d]?\s', clean)
    if m and m.end() <= max_len:
        return clean[:m.end()].strip()

    # If first sentence is too long, truncate
    if len(clean) > max_len:
        # Try to break at a word boundary
        truncated = clean[:max_len]
        last_space = truncated.rfind(' ')
        if last_space > max_len // 2:
            return truncated[:last_space] + "..."
        return truncated[:max_len - 3] + "..."
    return clean


def parse_paragraphs(text):
    """Split essay into paragraphs on double newlines.

    Handles the case where poetry/quotes are embedded in paragraphs.
    We rejoin short quoted verse blocks with adjacent paragraphs when
    they appear to be continuations, but generally trust double-newline
    as the paragraph boundary.
    """
    # Split on two or more newlines
    raw_blocks = re.split(r'\n{2,}', text)

    paragraphs = []
    for block in raw_blocks:
        stripped = block.strip()
        if not stripped:
            continue

        # Check if this is a standalone poetry/verse block (all lines indented)
        # Must check BEFORE stripping the block, since strip() removes leading spaces
        raw_lines = block.split('\n')
        all_indented = all(line.startswith('  ') or not line.strip() for line in raw_lines)

        if all_indented and paragraphs:
            # This is an indented verse block — append to previous paragraph
            paragraphs[-1] += '\n\n' + stripped
        else:
            paragraphs.append(stripped)

    return paragraphs


# Thematic groupings — assigned by position in the essay flow
# The essay flows: general principles → specific grievances → personal narrative → broader vision
THEMES = [
    {
        "id": "theme-illegitimacy-of-government",
        "name": "The Illegitimacy of Government",
        "about": "Thoreau opens with a radical premise: 'That government is best which governs not at all.' He argues that government is at best an expedient, usually inexpedient, and that the standing government is as liable to abuse as a standing army. The American government is a tradition losing its integrity, a wooden gun that would split if ever used in earnest. The character inherent in the American people, not their government, has accomplished everything worthy.",
        "for_readers": "Begin here. Thoreau's opening is one of the most famous critiques of governmental legitimacy ever written. Notice how he doesn't reject government entirely — he asks for 'at once a better government.' The radicalism is in the standard he sets, not in nihilism.",
    },
    {
        "id": "theme-mexican-war-and-slavery",
        "name": "The Mexican War and Slavery",
        "about": "From abstract principle, Thoreau moves to concrete outrage: the Mexican-American War (1846-48) and the institution of slavery. These are not theoretical injustices but active crimes committed by the state with the passive consent of its citizens. The soldier who serves the state serves it 'not as men mainly, but as machines.' The majority rules not because it is right but because it is physically strongest.",
        "for_readers": "Thoreau wrote in 1849, twelve years before the Civil War. His moral clarity about slavery — that it made every citizen complicit — was not the mainstream view. Read these paragraphs as a man on fire with specific grievance, not abstract philosophy.",
    },
    {
        "id": "theme-duty-to-resist",
        "name": "The Duty to Resist",
        "about": "The moral heart of the essay: when a government supports injustice, the citizen has not merely a right but a duty to withdraw support. Voting is insufficient — 'a wise man will not leave the right to the mercy of chance.' Action, not opinion, is what matters. Even one honest man ceasing to hold slaves and going to jail for it would be 'the abolition of slavery in America.' Under an unjust government, 'the true place for a just man is also a prison.'",
        "for_readers": "This is where Gandhi found satyagraha and King found the Birmingham jail. The argument that changed history: that compliance with injustice is itself injustice, and that the individual conscience outranks the law.",
    },
    {
        "id": "theme-night-in-jail",
        "name": "The Night in Jail",
        "about": "Thoreau's famous autobiographical account of his night in the Concord jail for refusing to pay the poll tax. He describes his cellmate, the view from the window, the morning breakfast in tin pans. Rather than diminishing him, jail gave him a 'closer view of my native town' — he saw its institutions clearly for the first time. When released the next morning, he joined a huckleberry party, and 'the State was nowhere to be seen.'",
        "for_readers": "The most human section of the essay. Thoreau the philosopher becomes Thoreau the storyteller — wry, observant, almost amused. His refusal to be diminished by imprisonment anticipates every political prisoner's memoir since.",
    },
    {
        "id": "theme-individual-and-state",
        "name": "The Individual and the State",
        "about": "After the personal narrative, Thoreau returns to philosophy: the relationship between conscience and law, the individual and the collective. He examines Daniel Webster's compromises on slavery, the limits of statesmanship without moral vision, and the difference between the lawyer's 'consistent expediency' and actual Truth. Those who know purer sources of truth must continue their pilgrimage toward its fountain-head.",
        "for_readers": "Thoreau's critique of Webster — the most respected politician of his era — shows that eloquence without moral courage is worthless. This section resonates whenever we see leaders choosing pragmatism over justice.",
    },
    {
        "id": "theme-better-government",
        "name": "A Better Government",
        "about": "Thoreau ends not with anarchism but with vision. Democracy is progress — from absolute monarchy to limited monarchy to democracy — but it is not the final step. A truly free state would 'recognize the individual as a higher and independent power, from which all its own power and authority are derived.' He imagines a State that can afford to be just to all, that treats the individual with respect as a neighbor.",
        "for_readers": "The essay's closing paragraphs are often overlooked, but they are essential. Thoreau is not merely against the state — he imagines what governance could be. The progress he describes has not yet been completed.",
    },
]


def assign_themes(paragraphs):
    """Assign paragraph indices to themes based on position.

    The essay flows roughly:
    - Paragraphs 1-7: Opening argument about government legitimacy
    - Paragraphs 8-14: Mexican War, slavery, soldiers as machines, voting
    - Paragraphs 15-24: Duty to resist, withdrawal, tax refusal, prison as proper place
    - Paragraphs 25-37: Night in jail narrative (starting with "Some years ago" through "My Prisons")
    - Paragraphs 38-44: Individual vs state, Webster critique, legislators
    - Paragraphs 45+: Vision for better government

    We'll adjust these boundaries based on the actual paragraph count.
    """
    total = len(paragraphs)

    # Look for key markers to set boundaries more precisely
    boundaries = {}

    for i, para in enumerate(paragraphs):
        text = para[:200].lower()
        # "How does it become a man to behave toward the American government" — shift to specific grievances
        if "how does it become a man to behave toward" in text:
            boundaries.setdefault("grievances_start", i)
        # "It is not a man's duty" — shift to duty to resist
        if "it is not a man\u2019s duty" in text or "it is not a man's duty" in text:
            boundaries.setdefault("resist_start", i)
        # "Some years ago, the State met me" — jail narrative begins
        if "some years ago, the state met me" in text:
            boundaries.setdefault("jail_start", i)
        # "I have never declined paying the highway tax" — after jail, individual vs state
        if "i have never declined paying the highway tax" in text:
            boundaries.setdefault("post_jail", i)
        # "They who know of no purer sources of truth" — vision section
        if "they who know of no purer sources of truth" in text:
            boundaries.setdefault("vision_start", i)

    # Set theme boundaries with fallbacks
    t1_end = boundaries.get("grievances_start", min(7, total))
    t2_end = boundaries.get("resist_start", min(14, total))
    t3_end = boundaries.get("jail_start", min(26, total))
    t4_end = boundaries.get("post_jail", min(37, total))
    t5_end = boundaries.get("vision_start", min(45, total))

    theme_ranges = [
        (0, t1_end),          # Illegitimacy of Government
        (t1_end, t2_end),     # Mexican War and Slavery
        (t2_end, t3_end),     # Duty to Resist
        (t3_end, t4_end),     # Night in Jail
        (t4_end, t5_end),     # Individual and State
        (t5_end, total),      # Better Government
    ]

    return theme_ranges


def build_grammar(paragraphs):
    items = []
    sort_order = 0

    # L1: Individual paragraphs
    for i, para in enumerate(paragraphs):
        sort_order += 1
        para_num = i + 1
        para_id = f"para-{para_num:02d}"
        first_sentence = extract_first_sentence(para)

        items.append({
            "id": para_id,
            "name": first_sentence,
            "level": 1,
            "category": "paragraph",
            "sort_order": sort_order,
            "sections": {
                "Passage": para,
            },
            "keywords": [],
            "metadata": {
                "paragraph_number": para_num,
            }
        })

    # Assign paragraphs to themes
    theme_ranges = assign_themes(paragraphs)

    # L2: Thematic emergence groups
    all_theme_ids = []
    for idx, theme in enumerate(THEMES):
        sort_order += 1
        start, end = theme_ranges[idx]
        composite = [f"para-{j+1:02d}" for j in range(start, end)]
        theme_id = theme["id"]
        all_theme_ids.append(theme_id)

        items.append({
            "id": theme_id,
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
                "paragraph_range": f"{start + 1}-{end}",
                "paragraph_count": end - start,
            }
        })

    # L3: The complete essay
    sort_order += 1
    items.append({
        "id": "civil-disobedience",
        "name": "Civil Disobedience",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "Henry David Thoreau's 'Civil Disobedience' (1849) is a single continuous essay that flows from abstract political philosophy through specific moral outrage to personal narrative and back to visionary philosophy. Written after a night in jail for refusing to pay a poll tax that supported slavery and the Mexican-American War, it argues that the individual conscience is the highest authority — higher than any government, any majority, any law. This essay directly inspired Gandhi's satyagraha, Martin Luther King Jr.'s civil rights strategy, the Danish resistance to the Nazis, and every nonviolent resistance movement since. Its central claim — that compliance with injustice is itself injustice — remains the moral foundation of civil disobedience worldwide.",
            "For Readers": "Read the essay straight through at least once — Thoreau wrote it as a single arc, and its power builds cumulatively. Then use the thematic groupings to return to specific arguments. The jail narrative (theme 4) is the emotional center; the opening and closing (themes 1 and 6) are the intellectual frame. Notice how Thoreau moves between the universal and the personal, the philosophical and the practical. This is not an academic treatise — it is a man explaining why he went to jail, and why you should consider it too.",
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
    text = strip_title_block(text)
    paragraphs = parse_paragraphs(text)
    print(f"Parsed {len(paragraphs)} paragraphs")

    # Show first sentence of each paragraph for verification
    for i, para in enumerate(paragraphs):
        first = extract_first_sentence(para, max_len=70)
        print(f"  {i+1:2d}: {first}")

    items = build_grammar(paragraphs)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Henry David Thoreau", "date": "1849", "note": "Author (original title: Resistance to Civil Government)"}
            ]
        },
        "name": "Civil Disobedience",
        "description": "Henry David Thoreau's 'Civil Disobedience' (1849, originally 'Resistance to Civil Government') — the foundational text of nonviolent resistance. Written after Thoreau spent a night in jail for refusing to pay a poll tax that supported slavery and the Mexican-American War. This essay directly influenced Gandhi's satyagraha, Martin Luther King Jr.'s civil rights strategy, and every nonviolent resistance movement since. 'Under a government which imprisons any unjustly, the true place for a just man is also a prison.'\n\nSource: Project Gutenberg eBook #71 (https://www.gutenberg.org/ebooks/71)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Daguerreotypes of Thoreau. Illustrations from early editions of Walden. Concord, Massachusetts landscapes by the Hudson River School painters.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "politics", "resistance", "freedom", "public-domain", "full-text", "essay", "nonviolence"],
        "roots": ["freedom-commons"],
        "shelves": ["resilience"],
        "lineages": ["Kelty"],
        "worldview": "rationalist",
        "items": items,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT}")
    print(f"  L1: {l1} paragraphs, L2: {l2} thematic groups, L3: {l3} meta")
    print(f"  Total items: {len(items)}")

    # Print theme assignments
    theme_ranges = assign_themes(paragraphs)
    print("\nTheme assignments:")
    for idx, theme in enumerate(THEMES):
        start, end = theme_ranges[idx]
        print(f"  {theme['name']}: paragraphs {start+1}-{end} ({end-start} paragraphs)")


if __name__ == "__main__":
    main()
