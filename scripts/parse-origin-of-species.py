#!/usr/bin/env python3
"""
Parse Darwin's Origin of Species (Gutenberg #1228) into a grammar.json
for recursive.eco. Creates a tarot-style reflective deck.

Structure:
- L1: Key sub-topics/arguments within each chapter (~70-80 cards)
- L2: Chapters (14 + introduction = 15 emergence cards)
- L3: Thematic arcs grouping chapters (4-5 meta categories)
"""

import json
import re
import os
import textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
SOURCE_FILE = os.path.join(REPO_ROOT, "sources", "origin-of-species")
OUTPUT_DIR = os.path.join(REPO_ROOT, "grammars", "origin-of-species")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "grammar.json")

# ── Chapter metadata ──────────────────────────────────────────────
CHAPTERS = [
    {"num": 0, "title": "Introduction", "pattern": r"^INTRODUCTION\.\s*$",
     "short": "The Voyage & The Question"},
    {"num": 1, "title": "Variation Under Domestication", "pattern": r"^CHAPTER I\.\s*$",
     "short": "The Breeder's Art"},
    {"num": 2, "title": "Variation Under Nature", "pattern": r"^CHAPTER II\.\s*$",
     "short": "Nature's Diversity"},
    {"num": 3, "title": "Struggle for Existence", "pattern": r"^CHAPTER III\.\s*$",
     "short": "The Entangled Bank"},
    {"num": 4, "title": "Natural Selection", "pattern": r"^CHAPTER IV\.\s*$",
     "short": "The Invisible Hand"},
    {"num": 5, "title": "Laws of Variation", "pattern": r"^CHAPTER V\.\s*$",
     "short": "How Bodies Change"},
    {"num": 6, "title": "Difficulties on Theory", "pattern": r"^CHAPTER VI\.\s*$",
     "short": "Honest Doubts"},
    {"num": 7, "title": "Instinct", "pattern": r"^CHAPTER VII\.\s*$",
     "short": "The Wisdom of Bees"},
    {"num": 8, "title": "Hybridism", "pattern": r"^CHAPTER VIII\.\s*$",
     "short": "The Boundaries of Kind"},
    {"num": 9, "title": "On the Imperfection of the Geological Record",
     "pattern": r"^CHAPTER IX\.\s*$",
     "short": "The Missing Pages"},
    {"num": 10, "title": "On the Geological Succession of Organic Beings",
     "pattern": r"^CHAPTER X\.\s*$",
     "short": "Deep Time's Story"},
    {"num": 11, "title": "Geographical Distribution", "pattern": r"^CHAPTER XI\.\s*$",
     "short": "Islands & Continents"},
    {"num": 12, "title": "Geographical Distribution (continued)",
     "pattern": r"^CHAPTER XII\.\s*$",
     "short": "Oceans & Migrations"},
    {"num": 13, "title": "Mutual Affinities of Organic Beings",
     "pattern": r"^CHAPTER XIII\.\s*$",
     "short": "The Tree of Life"},
    {"num": 14, "title": "Recapitulation and Conclusion", "pattern": r"^CHAPTER XIV\.\s*$",
     "short": "There Is Grandeur"},
]

# Roman numeral patterns for chapter detection in the body text
ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
    "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12,
    "XIII": 13, "XIV": 14
}

# ── Thematic arcs (L3) ───────────────────────────────────────────
ARCS = [
    {
        "id": "arc-observation",
        "name": "Observation & Evidence",
        "chapters": [0, 1, 2],
        "about": "Darwin begins with what can be seen: the astonishing variety of life under human care and in the wild. Before theorizing, he looks — at pigeons, beetles, barnacles, and the subtle differences between closely related forms. These cards invite you to look before you leap.",
        "reflection": "What patterns have you noticed but not yet named? What's hiding in plain sight?"
    },
    {
        "id": "arc-mechanism",
        "name": "The Engine of Change",
        "chapters": [3, 4, 5],
        "about": "The heart of Darwin's insight: how struggle, selection, and variation work together to sculpt life over vast spans of time. Not cruel, not kind — simply relentless. These cards explore the forces that shape all living things, including you.",
        "reflection": "What pressures are shaping you right now? What would you become if those pressures changed?"
    },
    {
        "id": "arc-difficulties",
        "name": "Honest Difficulties",
        "chapters": [6, 7, 8],
        "about": "Darwin's most admirable quality: he sought out the strongest objections to his own theory and wrestled with them openly. The perfection of the eye, the mystery of instinct, the puzzle of sterile hybrids. These cards honor intellectual honesty.",
        "reflection": "What's the strongest argument against something you believe? Have you really sat with it?"
    },
    {
        "id": "arc-deep-time",
        "name": "Deep Time & Geography",
        "chapters": [9, 10, 11, 12],
        "about": "Darwin reads the earth itself as a text — fossils, rock strata, island species, continental distributions. The record is fragmentary, like a library with most books destroyed, yet what remains tells an astonishing story. These cards invite you to think in geological time.",
        "reflection": "What would your life look like from a thousand years away? What traces would remain?"
    },
    {
        "id": "arc-unity",
        "name": "The Grand View",
        "chapters": [13, 14],
        "about": "Darwin's conclusion: all life is connected. Morphology, embryology, rudimentary organs — everything points to common descent. The famous final paragraph, with its entangled bank and endless forms most beautiful, is one of the great passages in all of literature.",
        "reflection": "How does it feel to know you share ancestry with every living thing? What does that kinship ask of you?"
    }
]

# ── Sub-topic definitions per chapter ─────────────────────────────
# Each is (id_suffix, display_name, search_pattern_in_text, reflection_prompt)
# search_pattern is used to find the section in the raw text
SUBTOPICS = {
    0: [  # Introduction
        ("the-voyage", "The Voyage of the Beagle",
         r"When on board H\.M\.S\.",
         "Every great insight begins with a journey. What voyage — literal or metaphorical — first opened your eyes?"),
        ("mystery-of-mysteries", "The Mystery of Mysteries",
         r"origin of species.*mystery of mysteries",
         "What is YOUR mystery of mysteries — the question that won't let you go?"),
        ("this-abstract", "An Honest Abstract",
         r"This Abstract, which I now publish",
         "Darwin published knowing his work was incomplete. What are you holding back until it's 'perfect'?"),
        ("overview-of-chapters", "The Argument's Architecture",
         r"In considering the Origin of Species",
         "How do you build an argument? Do you start with evidence or with intuition?"),
    ],
    1: [  # Variation Under Domestication
        ("causes-of-variability", "Causes of Variability",
         r"Causes of Variability\.|causes of variability",
         "What conditions allowed you to become who you are? What variation was latent in you?"),
        ("effects-of-habit", "Effects of Habit and Use",
         r"Effects of Habit|Changed habits produce|effects of habit",
         "What habits have literally shaped you — your body, your mind, your character?"),
        ("domestic-pigeons", "The Pigeon Fanciers",
         r"On the Breeds of the Domestic Pigeon",
         "Darwin saw the whole theory in a pigeon loft. Where might you find the universe in a grain of sand?"),
        ("principle-of-selection", "The Principle of Selection",
         r"_Selection_\.",
         "What are you selecting for in your own life? What are you unconsciously breeding?"),
        ("unconscious-selection", "Unconscious Selection",
         r"Unconscious Selection",
         "What changes are you making without realizing it? What's being shaped by your daily choices?"),
    ],
    2: [  # Variation Under Nature
        ("individual-differences", "Individual Differences",
         r"Individual Differences|individual differences",
         "No two organisms are identical. What makes you irreplaceable?"),
        ("doubtful-species", "Doubtful Species",
         r"Doubtful species|doubtful species",
         "The line between 'variety' and 'species' is blurry. Where do you draw lines that nature doesn't?"),
        ("wide-ranging-species", "Wide-Ranging Species Vary Most",
         r"plants which have very wide ranges generally present varieties|Wide ranging, much diffused",
         "Those who travel widest change most. How has exposure to difference changed you?"),
        ("larger-genera", "The Larger Genera",
         r"larger genera.*vary more|species of the larger genera",
         "Success breeds diversity. Where in your life has abundance led to further creativity?"),
    ],
    3: [  # Struggle for Existence
        ("geometrical-increase", "Geometrical Powers of Increase",
         r"Geometrical powers of increase|geometrical ratio of increase|geometrical powers",
         "Every organism could fill the earth if unchecked. What would happen if your deepest drive had no limit?"),
        ("checks-to-increase", "Checks to Increase",
         r"Nature of the checks to increase|checks to increase",
         "What invisible forces keep you in balance? What would break if those checks were removed?"),
        ("complex-relations", "Complex Relations",
         r"Complex relations of all animals|complex relations",
         "Darwin traces chains of cause from cats to clover to bees. What hidden connections sustain your life?"),
        ("struggle-same-species", "Struggle Within the Same Species",
         r"most severe between.*individuals of the same species|Struggle for life most severe",
         "Your fiercest competition isn't with strangers — it's with those most like you. Where do you feel this?"),
    ],
    4: [  # Natural Selection
        ("natural-selection-power", "The Power of Natural Selection",
         r"Natural Selection.*power compared|How will the struggle for existence",
         "Nature selects with infinite patience. What would you change if you had a million years?"),
        ("sexual-selection", "Sexual Selection",
         r"_Sexual Selection_\.",
         "Beauty, song, display — nature rewards charm as well as strength. What do you display?"),
        ("illustrations-of-selection", "Illustrations of Natural Selection",
         r"_Illustrations of the action of Natural Selection_",
         "Darwin uses imaginary examples to make the invisible visible. Can you narrate the selection pressures in your own environment?"),
        ("intercrossing", "On Intercrossing",
         r"_On the Intercrossing of Individuals_",
         "Mixing matters. Where do you cross-pollinate ideas? Where are you too isolated?"),
        ("divergence-of-character", "Divergence of Character",
         r"_Divergence of Character_\.",
         "Descendants diverge to fill different niches. How have you and your siblings (literal or metaphorical) diverged?"),
        ("extinction", "Extinction",
         r"_Extinction_\.",
         "Every species that ever lived is, statistically, extinct. What in your life has gone extinct? What needed to?"),
    ],
    5: [  # Laws of Variation
        ("use-and-disuse", "Use and Disuse",
         r"_Effects of Use and Disuse_",
         "What you use grows stronger; what you neglect atrophies. What are you exercising? What's withering?"),
        ("acclimatisation", "Acclimatisation",
         r"_Acclimatisation_\.",
         "Organisms adapt to new conditions over generations. What have you acclimatised to that once felt impossible?"),
        ("correlation-of-growth", "Correlation of Growth",
         r"_Correlation of Growth_\.",
         "Change one part and others change too. What unexpected side effects have your choices produced?"),
        ("variation-summary", "Summary: Our Profound Ignorance",
         r"_Summary_.*ignorance of the laws of variation",
         "Darwin admits how little he knows. When did admitting ignorance open a door for you?"),
    ],
    6: [  # Difficulties on Theory
        ("transitional-varieties", "Absence of Transitional Varieties",
         r"Absence or rarity of transitional|transitional varieties",
         "The gaps in the record trouble Darwin. What gaps in your own story do you struggle to explain?"),
        ("extreme-perfection", "Organs of Extreme Perfection",
         r"_Organs of extreme perfection",
         "The eye seems impossibly complex — yet Darwin explains it step by step. What in your life seems too complex to have evolved naturally?"),
        ("organs-little-importance", "Organs of Little Importance",
         r"_Organs of little apparent importance_",
         "Tiny things matter to selection. What small detail in your life turned out to be crucial?"),
        ("natura-non-facit-saltum", "Natura Non Facit Saltum",
         r"Natura non facit saltum|natura non facit saltum",
         "Nature doesn't make leaps. Neither does real growth. Where are you trying to skip steps?"),
    ],
    7: [  # Instinct
        ("instinct-vs-habit", "Instinct Compared with Habit",
         r"Instincts comparable with habits|instincts comparable",
         "Some knowledge is born into the body. What do you know without having learned it?"),
        ("slave-making-ants", "Slave-Making Ants",
         r"_Slave-making instinct_",
         "Darwin documents ants that enslave other ants. Nature is not always kind. How do you sit with nature's cruelty?"),
        ("hive-bee-cells", "The Hive-Bee's Cell",
         r"_Cell-making instinct of the Hive-Bee_",
         "Bees build mathematically perfect hexagons by instinct. What do you build without fully understanding how?"),
        ("neuter-insects", "Neuter Insects",
         r"Neuter or sterile insects|neuter or sterile",
         "Sterile worker ants seem to defy selection — until you think about family. What do you sacrifice for the group?"),
    ],
    8: [  # Hybridism
        ("sterility-of-hybrids", "Sterility of Hybrids",
         r"Distinction between the sterility|sterility of first crosses",
         "Hybrids are often sterile — nature draws boundaries. Where do your worlds refuse to merge?"),
        ("laws-of-sterility", "Laws Governing Sterility",
         r"_Laws governing the Sterility of first Crosses|Laws governing the Sterility",
         "Some crosses are fertile, some aren't, and the rules are mysterious. What combinations in your life work, and which don't?"),
        ("fertility-of-varieties", "Fertility of Varieties",
         r"Fertility of varieties when crossed|fertility of varieties",
         "Varieties of the same species cross freely. What 'varieties' of yourself can you recombine?"),
    ],
    9: [  # Imperfection of Geological Record
        ("lapse-of-time", "The Vast Lapse of Time",
         r"_On the lapse of Time_",
         "Darwin asks you to imagine millions of years. Can you feel the weight of deep time?"),
        ("poorness-of-collections", "The Poorness of Our Collections",
         r"_On the poorness of our Pal",
         "We have only scraps of the fossil record. What scraps of your own past do you build your story from?"),
        ("sudden-appearance", "Sudden Appearance of Groups",
         r"_On the sudden appearance of whole groups|sudden appearance of whole groups of Allied Species",
         "Whole groups seem to appear at once — but only because the earlier chapters are lost. What origin story are you missing?"),
    ],
    10: [  # Geological Succession
        ("slow-appearance", "Slow Appearance of New Species",
         r"slow and successive appearance|On the slow",
         "New species arrive slowly, like dawn. What's slowly dawning in your life?"),
        ("species-once-lost", "Species Once Lost Do Not Reappear",
         r"Species once lost do not reappear",
         "Extinction is forever. What have you lost that will never return? Can you make peace with that?"),
        ("on-extinction", "On Extinction",
         r"_On Extinction_\.",
         "Extinction is as natural as birth. What needs to die so something new can live?"),
        ("same-types-same-areas", "Same Types in Same Areas",
         r"succession of the same types|same types within the same areas",
         "Marsupials in Australia, armadillos in South America — geography echoes history. What patterns in your life echo where you came from?"),
    ],
    11: [  # Geographical Distribution
        ("barriers-and-distribution", "Importance of Barriers",
         r"Importance of barriers|importance of barriers",
         "Mountains, oceans, deserts shape who lives where. What barriers have shaped your world?"),
        ("centres-of-creation", "Centres of Creation",
         r"Centres of creation|centres of creation",
         "Each species arose somewhere specific. Where is your centre of creation?"),
        ("means-of-dispersal", "Means of Dispersal",
         r"_Means of Dispersal_",
         "Seeds ride on birds, insects fly across oceans. How did your ideas travel to reach you?"),
        ("glacial-dispersal", "Dispersal During the Glacial Period",
         r"_Dispersal during the Glacial period_",
         "Ice ages pushed life toward the equator, then let it spread again. What crisis scattered you, then let you resettle?"),
    ],
    12: [  # Geographical Distribution (continued)
        ("freshwater-productions", "Freshwater Productions",
         r"Distribution of fresh-water productions|fresh-water productions",
         "Freshwater species are remarkably widespread. What connects distant pools in your life?"),
        ("oceanic-islands", "Inhabitants of Oceanic Islands",
         r"_On the Inhabitants of Oceanic Islands_",
         "Islands have unique species — isolation breeds novelty. What has your isolation created?"),
        ("absence-of-batrachians", "Absence of Frogs on Islands",
         r"Absence of Batrachians|absence of Batrachians",
         "No frogs on oceanic islands — they can't cross salt water. What can't cross the barriers in your life?"),
    ],
    13: [  # Mutual Affinities
        ("classification", "Classification and the Natural System",
         r"CLASSIFICATION, groups subordinate|Classification|Natural system",
         "We classify life into nested groups — because life actually IS nested groups. How do you classify your own experiences?"),
        ("morphology", "Morphology",
         r"_Morphology_\.",
         "A human hand, a bat wing, a whale flipper — the same bones, rearranged. What hidden structure connects your different roles?"),
        ("embryology", "Embryology",
         r"_Embryology_\.",
         "Embryos of different species look remarkably alike. What did all your current selves look like at the beginning?"),
        ("rudimentary-organs", "Rudimentary Organs",
         r"_Rudimentary, atrophied, or aborted organs_",
         "Vestigial organs are echoes of ancestors. What vestigial habits or beliefs do you still carry?"),
    ],
    14: [  # Recapitulation and Conclusion
        ("recapitulation", "Recapitulation of the Argument",
         r"Recapitulation of the difficulties|recapitulation of the general",
         "Darwin gathers all the threads. Can you recapitulate the argument of your own life so far?"),
        ("immutability-belief", "Why We Believe in Immutability",
         r"immutability of species|belief in the immutability",
         "We resist the idea that things change. What are you treating as permanent that isn't?"),
        ("how-far-extended", "How Far the Theory Extends",
         r"how far the theory of natural selection may be extended|Authors of the highest eminence seem to be fully satisfied",
         "Darwin wonders how far his idea reaches. How far does your core insight extend?"),
        ("entangled-bank", "The Entangled Bank",
         r"There is grandeur in this view of life|entangled bank",
         "Darwin's final image: an entangled bank, clothed with many plants, birds singing, insects flitting — all produced by laws acting around us. What is YOUR entangled bank?"),
    ],
}


def read_source():
    """Read the full source text."""
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        return f.read()


def split_into_chapters(text):
    """Split text into chapter blocks. Returns dict of chapter_num -> text."""
    lines = text.split("\n")

    # Find the actual body text start (after "ON THE ORIGIN OF SPECIES." header)
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "INTRODUCTION." and i > 300:
            body_start = i
            break

    # Find chapter boundaries
    chapter_starts = [(0, body_start)]  # Introduction
    for i in range(body_start, len(lines)):
        line = lines[i].strip()
        m = re.match(r"^CHAPTER ([IVXL]+)\.\s*$", line)
        if m:
            num = ROMAN.get(m.group(1), 0)
            if num > 0:
                chapter_starts.append((num, i))

    # Find INDEX as end marker
    end_line = len(lines)
    for i in range(len(lines) - 1, 0, -1):
        if lines[i].strip() == "INDEX.":
            end_line = i
            break

    # Split into chapters
    chapters = {}
    for idx, (num, start) in enumerate(chapter_starts):
        if idx + 1 < len(chapter_starts):
            end = chapter_starts[idx + 1][1]
        else:
            end = end_line
        chapters[num] = "\n".join(lines[start:end])

    return chapters


def extract_first_paragraphs(text, pattern, max_chars=800):
    """Find the section matching pattern and extract the first ~2 paragraphs."""
    # First try normal search, then try with newlines collapsed
    m = re.search(pattern, text, re.IGNORECASE)
    if not m:
        # Try matching against newline-collapsed text
        collapsed = re.sub(r"\n(?!\n)", " ", text)
        m2 = re.search(pattern, collapsed, re.IGNORECASE)
        if m2:
            # Map position back to original text approximately
            # Find the same paragraph in original
            snippet = collapsed[max(0, m2.start()-20):m2.start()+80]
            # Search for a unique chunk in original
            words = collapsed[m2.start():m2.start()+40].split()
            if len(words) >= 3:
                search_chunk = " ".join(words[:3])
                # Try to find in collapsed original paragraphs
                paras = re.split(r"\n\s*\n", text)
                for pi, p in enumerate(paras):
                    p_clean = re.sub(r"\s+", " ", p.strip())
                    if search_chunk in p_clean:
                        result = [p_clean]
                        total_len = len(p_clean)
                        for np in paras[pi+1:pi+3]:
                            np_clean = re.sub(r"\s+", " ", np.strip())
                            if not np_clean:
                                continue
                            result.append(np_clean)
                            total_len += len(np_clean)
                            if total_len > max_chars:
                                break
                        return "\n\n".join(result) if result else None
            return None
    if not m:
        return None

    # Get text from match point
    start = m.start()
    # Find the paragraph (go back to start of line)
    line_start = text.rfind("\n", 0, start)
    if line_start == -1:
        line_start = 0

    remaining = text[line_start:].strip()

    # Split into paragraphs and take first 2-3
    paragraphs = re.split(r"\n\s*\n", remaining)
    result = []
    total_len = 0
    for p in paragraphs[:3]:
        p = p.strip()
        if not p:
            continue
        # Clean up whitespace
        p = re.sub(r"\s+", " ", p)
        result.append(p)
        total_len += len(p)
        if total_len > max_chars:
            break

    return "\n\n".join(result) if result else None


def extract_key_quote(text, pattern, max_len=300):
    """Extract a short representative quote from near the section start."""
    m = re.search(pattern, text, re.IGNORECASE)
    if not m:
        return None

    # Get text after match
    remaining = text[m.start():m.start() + 2000]

    # Look for sentences that feel quotable (contain key phrases)
    sentences = re.split(r"(?<=[.!?])\s+", remaining)

    # Return the first 2-3 sentences that make a coherent thought
    result = []
    total_len = 0
    for s in sentences[0:4]:
        s = re.sub(r"\s+", " ", s.strip())
        if not s:
            continue
        result.append(s)
        total_len += len(s)
        if total_len > max_len:
            break

    quote = " ".join(result)
    if len(quote) > max_len:
        # Truncate at last sentence boundary
        cut = quote[:max_len].rfind(".")
        if cut > 100:
            quote = quote[:cut + 1]

    return quote


def make_id(chapter_num, suffix):
    """Create a standardized item ID."""
    if chapter_num == 0:
        return f"intro-{suffix}"
    return f"ch{chapter_num:02d}-{suffix}"


def build_grammar(chapters_text):
    """Build the full grammar JSON."""
    items = []
    sort_order = 1

    # ── L1 items: sub-topics ──────────────────────────────────────
    for ch_num, subtopics in SUBTOPICS.items():
        ch_text = chapters_text.get(ch_num, "")
        ch_meta = CHAPTERS[ch_num] if ch_num < len(CHAPTERS) else CHAPTERS[-1]

        for suffix, name, pattern, reflection in subtopics:
            item_id = make_id(ch_num, suffix)

            # Extract passage from source text
            passage = extract_first_paragraphs(ch_text, pattern)
            quote = extract_key_quote(ch_text, pattern) if not passage else None

            sections = {}

            if passage:
                # Trim to a reasonable reading length
                if len(passage) > 600:
                    # Cut at a sentence boundary
                    cut = passage[:600].rfind(".")
                    if cut > 200:
                        passage = passage[:cut + 1]
                sections["Darwin's Words"] = passage

            sections["Reflection"] = reflection

            # Add a "The Argument" summary section
            sections["The Argument"] = f"From Chapter {'Introduction' if ch_num == 0 else ch_num}: {ch_meta['title']}"

            item = {
                "id": item_id,
                "name": name,
                "level": 1,
                "category": f"chapter-{ch_num:02d}",
                "sort_order": sort_order,
                "sections": sections,
                "keywords": [],
                "metadata": {
                    "chapter_number": ch_num,
                    "chapter_name": ch_meta["title"],
                }
            }
            items.append(item)
            sort_order += 1

    # ── L2 items: chapters ────────────────────────────────────────
    for ch in CHAPTERS:
        ch_num = ch["num"]
        child_ids = [make_id(ch_num, s[0]) for s in SUBTOPICS.get(ch_num, [])]

        # Build a summary of what this chapter covers
        topic_names = [s[1] for s in SUBTOPICS.get(ch_num, [])]

        item = {
            "id": f"chapter-{ch_num:02d}" if ch_num > 0 else "chapter-intro",
            "name": f"{ch['short']}",
            "level": 2,
            "category": "chapter",
            "sort_order": sort_order,
            "sections": {
                "About": f"Chapter {'Introduction' if ch_num == 0 else ch_num}: {ch['title']}. Darwin explores: {', '.join(topic_names)}.",
                "For Readers": f"This chapter contains {len(child_ids)} cards for reflection. Draw one when you need Darwin's perspective on {ch['short'].lower()}.",
            },
            "keywords": [],
            "metadata": {
                "chapter_number": ch_num,
                "chapter_name": ch["title"],
            },
            "composite_of": child_ids,
            "relationship_type": "emergence"
        }
        items.append(item)
        sort_order += 1

    # ── L3 items: thematic arcs ───────────────────────────────────
    for arc in ARCS:
        chapter_ids = [
            f"chapter-{c:02d}" if c > 0 else "chapter-intro"
            for c in arc["chapters"]
        ]

        item = {
            "id": arc["id"],
            "name": arc["name"],
            "level": 3,
            "category": "arc",
            "sort_order": sort_order,
            "sections": {
                "About": arc["about"],
                "Reflection": arc["reflection"],
            },
            "keywords": [],
            "metadata": {},
            "composite_of": chapter_ids,
            "relationship_type": "emergence"
        }
        items.append(item)
        sort_order += 1

    # ── Assemble grammar ──────────────────────────────────────────
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Charles Darwin",
                    "date": "1859",
                    "note": "On the Origin of Species by Means of Natural Selection, First Edition"
                },
                {
                    "name": "Project Gutenberg",
                    "date": "1998",
                    "note": "eBook #1228, digitized by Sue Asscher and David Widger"
                }
            ]
        },
        "name": "On the Origin of Species — A Naturalist's Oracle",
        "description": "Charles Darwin's 1859 masterwork, reimagined as a deck of 60+ reflective cards. Each card carries one of Darwin's key arguments alongside a question for contemplation. Draw a card when you need the long view — when you're struggling, adapting, going extinct, or evolving into something new.\n\nSource: Project Gutenberg eBook #1228, First Edition (1859). https://www.gutenberg.org/ebooks/1228\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES:\n- Charles Darwin's own sketches and notebooks (1837-1859), including the famous 'I think' tree of life diagram\n- Ernst Haeckel, Kunstformen der Natur (1904) — stunning biological illustrations of radiolarians, jellyfish, orchids\n- Philip Henry Gosse, Actinologia Britannica (1860) — sea anemones and marine life\n- Audubon, Birds of America (1827-1838) — for chapters on island biogeography\n- Plates from the Voyage of the Beagle (1839) — landscapes and specimens from Darwin's journey",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "science",
            "evolution",
            "darwin",
            "natural-selection",
            "biology",
            "oracle",
            "reflective",
            "public-domain",
            "classic",
            "philosophy-of-science",
            "deep-time"
        ],
        "roots": ["rationalist-inquiry", "natural-philosophy"],
        "shelves": ["wisdom", "earth"],
        "lineages": ["Akomolafe"],
        "worldview": "rationalist",
        "items": items
    }

    return grammar


def enrich_with_quotes(grammar, chapters_text):
    """Second pass: add Darwin quotes to L1 items that are missing them."""
    for item in grammar["items"]:
        if item["level"] != 1:
            continue
        if "Darwin's Words" in item["sections"] and len(item["sections"]["Darwin's Words"]) > 100:
            continue

        ch_num = item["metadata"].get("chapter_number", 0)
        ch_text = chapters_text.get(ch_num, "")

        # Try to find the subtopic definition
        suffix = item["id"].split("-", 2)[-1] if "-" in item["id"] else item["id"]
        for s_suffix, s_name, s_pattern, s_reflection in SUBTOPICS.get(ch_num, []):
            if s_suffix == suffix or item["id"].endswith(s_suffix):
                passage = extract_first_paragraphs(ch_text, s_pattern, max_chars=600)
                if passage:
                    item["sections"]["Darwin's Words"] = passage
                break


def main():
    print("Reading source text...")
    text = read_source()
    print(f"  {len(text):,} characters")

    print("Splitting into chapters...")
    chapters = split_into_chapters(text)
    print(f"  Found {len(chapters)} chapters")
    for num, ch_text in sorted(chapters.items()):
        print(f"    Ch {num}: {len(ch_text):,} chars")

    print("Building grammar...")
    grammar = build_grammar(chapters)

    print("Enriching with quotes...")
    enrich_with_quotes(grammar, chapters)

    # Count items by level
    l1 = sum(1 for i in grammar["items"] if i["level"] == 1)
    l2 = sum(1 for i in grammar["items"] if i["level"] == 2)
    l3 = sum(1 for i in grammar["items"] if i["level"] == 3)
    print(f"  L1: {l1} cards, L2: {l2} chapters, L3: {l3} arcs")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Writing {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # File size
    size = os.path.getsize(OUTPUT_FILE)
    print(f"  {size:,} bytes ({size/1024:.1f} KB)")

    # Validate basics
    print("\nValidation:")
    ids = [i["id"] for i in grammar["items"]]
    dupes = [x for x in ids if ids.count(x) > 1]
    if dupes:
        print(f"  FAIL Duplicate IDs: {set(dupes)}")
    else:
        print(f"  OK No duplicate IDs")

    # Check composite_of references
    id_set = set(ids)
    bad_refs = []
    for item in grammar["items"]:
        for ref in item.get("composite_of", []):
            if ref not in id_set:
                bad_refs.append((item["id"], ref))
    if bad_refs:
        print(f"  FAIL Broken references: {bad_refs}")
    else:
        print(f"  OK All composite_of references valid")

    # Check Darwin's Words coverage
    missing_quotes = [i["id"] for i in grammar["items"]
                      if i["level"] == 1 and "Darwin's Words" not in i["sections"]]
    if missing_quotes:
        print(f"  WARN {len(missing_quotes)} L1 items missing Darwin's Words: {missing_quotes[:5]}...")
    else:
        print(f"  OK All L1 items have Darwin's Words")

    print("\nDone! Grammar written to grammars/origin-of-species/grammar.json")


if __name__ == "__main__":
    main()
