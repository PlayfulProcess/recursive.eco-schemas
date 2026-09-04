#!/usr/bin/env python3
"""
Build grammar.json for Beyond Good and Evil by Friedrich Nietzsche.

Source: Project Gutenberg eBook #4363
Author: Friedrich Nietzsche (1886)
Translator: Helen Zimmern

Structure:
- L1: Preface + 9 chapters + poem "From the Heights"
- L2: Thematic groupings (5 themes)
- L3: Meta-categories (The Complete Work)
"""

import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "beyond-good-and-evil.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "beyond-good-and-evil"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Sections in order as they appear in the text
SECTIONS = [
    {"id": "preface", "name": "Preface", "pattern": r"^PREFACE\s*$"},
    {"id": "chapter-1-prejudices-of-philosophers", "name": "Chapter I: Prejudices of Philosophers", "pattern": r"^CHAPTER I\.\s*PREJUDICES OF PHILOSOPHERS"},
    {"id": "chapter-2-the-free-spirit", "name": "Chapter II: The Free Spirit", "pattern": r"^CHAPTER II\.\s*THE FREE SPIRIT"},
    {"id": "chapter-3-the-religious-mood", "name": "Chapter III: The Religious Mood", "pattern": r"^CHAPTER III\.\s*THE RELIGIOUS MOOD"},
    {"id": "chapter-4-apophthegms-and-interludes", "name": "Chapter IV: Apophthegms and Interludes", "pattern": r"^CHAPTER IV\.\s*APOPHTHEGMS AND INTERLUDES"},
    {"id": "chapter-5-natural-history-of-morals", "name": "Chapter V: The Natural History of Morals", "pattern": r"^CHAPTER V\.\s*THE NATURAL HISTORY OF MORALS"},
    {"id": "chapter-6-we-scholars", "name": "Chapter VI: We Scholars", "pattern": r"^CHAPTER VI\.\s*WE SCHOLARS"},
    {"id": "chapter-7-our-virtues", "name": "Chapter VII: Our Virtues", "pattern": r"^CHAPTER VII\.\s*OUR VIRTUES"},
    {"id": "chapter-8-peoples-and-countries", "name": "Chapter VIII: Peoples and Countries", "pattern": r"^CHAPTER VIII\.\s*PEOPLES AND COUNTRIES"},
    {"id": "chapter-9-what-is-noble", "name": "Chapter IX: What is Noble?", "pattern": r"^CHAPTER IX\.\s*WHAT IS NOBLE"},
    {"id": "from-the-heights", "name": "From the Heights (Poem)", "pattern": r"^FROM THE HEIGHTS"},
]

SECTION_KEYWORDS = {
    "preface": ["dogmatism", "truth", "Plato", "Europe", "philosophy", "perspective"],
    "chapter-1-prejudices-of-philosophers": ["will-to-truth", "prejudice", "metaphysics", "values", "instinct", "Kant", "Spinoza"],
    "chapter-2-the-free-spirit": ["free-spirit", "independence", "masks", "solitude", "danger", "perspective"],
    "chapter-3-the-religious-mood": ["religion", "Christianity", "asceticism", "soul", "piety", "sacrifice"],
    "chapter-4-apophthegms-and-interludes": ["aphorism", "wisdom", "wit", "paradox", "observation"],
    "chapter-5-natural-history-of-morals": ["morality", "herd", "instinct", "command", "obedience", "nature"],
    "chapter-6-we-scholars": ["scholars", "science", "philosophy", "objectivity", "skepticism"],
    "chapter-7-our-virtues": ["virtues", "honesty", "woman", "cruelty", "suffering", "morality"],
    "chapter-8-peoples-and-countries": ["Europe", "nations", "culture", "music", "Wagner", "Germany", "France"],
    "chapter-9-what-is-noble": ["nobility", "rank", "aristocracy", "master-morality", "slave-morality", "pathos-of-distance"],
    "from-the-heights": ["solitude", "poetry", "heights", "friendship", "noon"],
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
    return text[start_idx:end_idx]


def strip_front_matter(text):
    """Remove title page and table of contents before Preface."""
    match = re.search(r'^PREFACE\s*$', text, re.MULTILINE)
    if match:
        return text[match.start():]
    return text


def parse_sections(text):
    """Parse the book into its sections (preface + 9 chapters + poem)."""
    sections = []

    for i, section in enumerate(SECTIONS):
        match = re.search(section["pattern"], text, re.MULTILINE)
        if not match:
            print(f"WARNING: Could not find '{section['name']}'")
            continue

        # Start after the heading line
        heading_end = text.index('\n', match.start()) + 1
        start = heading_end

        # Find the next section or end of text
        if i + 1 < len(SECTIONS):
            next_match = re.search(SECTIONS[i + 1]["pattern"], text[start:], re.MULTILINE)
            if next_match:
                end = start + next_match.start()
            else:
                end = len(text)
        else:
            end = len(text)

        section_text = text[start:end].strip()
        # Clean up whitespace
        section_text = re.sub(r'\n{3,}', '\n\n', section_text)

        sections.append({
            'id': section['id'],
            'name': section['name'],
            'text': section_text,
            'num': i,
        })

    return sections


# Thematic groupings for L2
THEMES = [
    {
        "id": "theme-critique-of-philosophy",
        "name": "The Critique of Philosophy",
        "sections": ["preface", "chapter-1-prejudices-of-philosophers", "chapter-6-we-scholars"],
        "about": "Nietzsche's devastating attack on the philosophical tradition. Every great philosophy, he argues, is really its author's confession — a disguised autobiography driven by instinct, not reason. Philosophers have always been unconscious advocates of their own prejudices, which they dignify with the name 'truth.' The will to truth itself must be questioned: why truth rather than untruth? Nietzsche extends this critique to modern scholars, who he sees as industrious but spiritually mediocre — grinding mills that need to be set in motion by a genuine philosopher's commanding vision.",
        "for_readers": "The Preface sets the tone with its audacious opening image of Truth as a woman whom clumsy dogmatists have failed to seduce. Chapter I is perhaps the most concentrated philosophical dynamite in the book — every section is quotable. Chapter VI on scholars is Nietzsche's portrait of academic philosophy, still painfully recognizable. Together they constitute his case that philosophy needs to be refounded on entirely new principles.",
    },
    {
        "id": "theme-freedom-and-danger",
        "name": "Freedom and Danger",
        "sections": ["chapter-2-the-free-spirit", "chapter-3-the-religious-mood"],
        "about": "What does genuine intellectual freedom look like? Nietzsche's 'free spirit' is not a libertine but someone who has endured the discipline of many perspectives, who can wear masks and still know who they are, who has earned their independence through suffering. The religious mood is explored not as something to be simply rejected but as a profound human phenomenon — asceticism, the religious sacrifice of the intellect, the 'holy lie' — that reveals deep truths about the psychology of belief and self-overcoming.",
        "for_readers": "Chapter II introduces one of Nietzsche's most attractive figures: the free spirit who has liberated themselves through intellectual courage and is now 'bound to no one thing.' Chapter III on religion is more nuanced than many expect — Nietzsche takes religious experience seriously as psychology even while rejecting its metaphysical claims. The discussion of Pascal is particularly moving.",
    },
    {
        "id": "theme-morality-revalued",
        "name": "Morality Revalued",
        "sections": ["chapter-5-natural-history-of-morals", "chapter-7-our-virtues", "chapter-9-what-is-noble"],
        "about": "The heart of the book: Nietzsche's revaluation of morality. He distinguishes 'master morality' (which creates values) from 'slave morality' (which reacts against the powerful). Current morality is essentially herd morality — the morality of the weak, disguised as universal truth. Against this, Nietzsche champions a 'pathos of distance,' an aristocratic order of rank among souls. Our supposed 'virtues' are often masked cruelties or weaknesses. True nobility is rare, dangerous, and beautiful.",
        "for_readers": "Chapter V (Natural History of Morals) is essential — read it alongside the Genealogy of Morals for the full picture. Chapter VII on 'Our Virtues' contains Nietzsche's most provocative claims about honesty, cruelty, and women (the latter controversial even in his time). Chapter IX on nobility is the book's climax and contains the master-slave morality distinction in its most developed form. These are the chapters that changed moral philosophy forever.",
    },
    {
        "id": "theme-aphorisms-and-observations",
        "name": "Aphorisms and Observations",
        "sections": ["chapter-4-apophthegms-and-interludes", "chapter-8-peoples-and-countries"],
        "about": "Nietzsche the stylist and observer. Chapter IV is a collection of standalone aphorisms — compressed wisdom, wit, and provocation in single sentences or short paragraphs. Chapter VIII applies his observational genius to European peoples and cultures: Germany, France, England, Russia, the Jews, and the prospect of a unified Europe. These chapters showcase Nietzsche's extraordinary literary gifts and his penetrating psychological eye.",
        "for_readers": "Chapter IV is the most accessible and quotable section — a treasury of one-liners that reward slow reading and repeated return. 'Whoever fights monsters should see to it that in the process he does not become a monster.' Chapter VIII is a fascinating portrait of 1880s Europe, surprisingly relevant to European identity debates today. Read these for pleasure as much as philosophy.",
    },
    {
        "id": "theme-poetry-and-solitude",
        "name": "Poetry and Solitude",
        "sections": ["from-the-heights"],
        "about": "The book closes with a poem, 'From the Heights,' translated by L.A. Magnus. After nine chapters of philosophical combat, Nietzsche steps into verse — a shift from argument to music, from the public forum to the mountain solitude he cherished. The poem enacts the solitude of the thinker who has climbed beyond good and evil and looks down at the world with a mixture of longing and distance.",
        "for_readers": "The poem is easily overlooked but rewards attention. It echoes themes from Thus Spoke Zarathustra — the heights, the midday, the absent friends — and provides an emotional counterpoint to the book's intellectual aggression. Nietzsche was a serious poet and composer; this closing shows the lyrical sensibility beneath the philosophical hammer.",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = strip_front_matter(text)

    sections = parse_sections(text)
    print(f"Parsed {len(sections)} sections")

    items = []
    sort_order = 0

    # L1: Individual sections
    for sec in sections:
        sort_order += 1
        keywords = SECTION_KEYWORDS.get(sec['id'], ["philosophy", "Nietzsche"])

        items.append({
            "id": sec['id'],
            "name": sec['name'],
            "sort_order": sort_order,
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": sec['text'],
            },
            "keywords": keywords,
            "metadata": {
                "section_number": sec['num'],
            }
        })
        print(f"  {sec['name']} ({len(sec['text'])} chars)")

    # L2: Thematic groupings
    all_theme_ids = []
    for theme in THEMES:
        sort_order += 1
        theme_id = theme["id"]
        all_theme_ids.append(theme_id)

        items.append({
            "id": theme_id,
            "name": theme["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": theme["sections"],
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "section_count": len(theme["sections"]),
            }
        })

    # L3: Meta-category
    sort_order += 1
    items.append({
        "id": "beyond-good-and-evil-complete",
        "name": "Beyond Good and Evil: Prelude to a Philosophy of the Future",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "Friedrich Nietzsche's Beyond Good and Evil (Jenseits von Gut und Bose, 1886) is his most systematic attempt to revalue all values. Written in a mixture of sustained argument and brilliant aphorism, it attacks the philosophical tradition (especially Plato and Kant), develops the concepts of will to power and the free spirit, analyzes the psychology of morality and religion, and introduces the master-slave morality distinction that would become one of the most influential ideas in modern thought. The book moves from a critique of philosophy's prejudices through an account of the free spirit's independence, a natural history of morals, and a vision of a new aristocratic order of rank among souls. It is at once a philosophical treatise, a work of literary art, and a provocation designed to disturb every comfortable assumption.",
            "For Readers": "Beyond Good and Evil can be read straight through or browsed — Nietzsche's aphoristic style means every section is relatively self-contained. For the philosophical core, focus on Chapters I, V, and IX. For pleasure and provocation, try Chapter IV (the aphorisms). For cultural commentary, Chapter VIII. The Preface is one of the finest openings in philosophy. Nietzsche writes to be re-read: sentences that seem outrageous on first encounter often reveal unsuspected depths on return. Helen Zimmern's translation, done under Nietzsche's own supervision, remains remarkably vivid.",
        },
        "keywords": ["Nietzsche", "morality", "will-to-power", "free-spirit", "master-morality", "slave-morality", "aphorism", "revaluation"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Friedrich Nietzsche",
                    "date": "1886",
                    "note": "Author"
                },
                {
                    "name": "Helen Zimmern",
                    "date": "1906",
                    "note": "Translator"
                }
            ]
        },
        "name": "Beyond Good and Evil",
        "description": "Friedrich Nietzsche's Beyond Good and Evil: Prelude to a Philosophy of the Future (1886) — his most systematic revaluation of Western philosophy and morality. Nine chapters and a preface, mixing sustained argument with brilliant aphorism, attacking the prejudices of philosophers, analyzing the psychology of religion and morality, and introducing the master-slave morality distinction. Translated by Helen Zimmern, whose work was supervised by Nietzsche himself.\n\nSource: Project Gutenberg eBook #4363 (https://www.gutenberg.org/ebooks/4363)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs of Nietzsche (various, 1860s-1880s), including the famous 1882 portrait by Gustav Schultze. Images of Sils-Maria in the Upper Engadine where Nietzsche wrote. Edvard Munch's portrait of Nietzsche (1906). Title pages from early editions.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "morality", "aphorism", "nihilism", "revaluation", "public-domain", "full-text"],
        "roots": ["western-philosophy"],
        "shelves": ["mirror"],
        "lineages": ["Akomolafe"],
        "worldview": "dialectical",
        "items": items,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1: {l1} sections, L2: {l2} themes, L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
