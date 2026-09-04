#!/usr/bin/env python3
"""
Parse Common Sense by Thomas Paine (Gutenberg #147, 1776)
into a grammar.json.

Structure:
- L1: Paragraphs within each chapter (id like "intro-p01", "ch1-p01", etc.)
- L2: Chapter emergence groups + thematic groups
- L3: "Common Sense" meta-category connecting all
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "common-sense.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "common-sense")
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


def strip_transcriber_additions(text):
    """Remove the 'On Common Sense' quotes section and transcriber notes added after FINIS."""
    # Find "F  I  N  I  S." which marks Paine's actual ending
    finis_match = re.search(r'F\s+I\s+N\s+I\s+S\.', text)
    if finis_match:
        text = text[:finis_match.start()].strip()
    return text


# Chapter definitions with their header patterns and slugs
CHAPTERS = [
    {
        "slug": "introduction",
        "prefix": "intro-para",
        "title": "Introduction",
        "header_pattern": r"^INTRODUCTION\.$",
    },
    {
        "slug": "origin-and-design-of-government",
        "prefix": "ch1-para",
        "title": "Of the Origin and Design of Government in General",
        "header_pattern": r"^OF THE ORIGIN AND DESIGN OF GOVERNMENT IN GENERAL",
    },
    {
        "slug": "monarchy-and-hereditary-succession",
        "prefix": "ch2-para",
        "title": "Of Monarchy and Hereditary Succession",
        "header_pattern": r"^OF MONARCHY AND HEREDITARY SUCCESSION",
    },
    {
        "slug": "present-state-of-american-affairs",
        "prefix": "ch3-para",
        "title": "Thoughts on the Present State of American Affairs",
        "header_pattern": r"^THOUGHTS ON THE PRESENT STATE OF AMERICAN AFFAIRS",
    },
    {
        "slug": "present-ability-of-america",
        "prefix": "ch4-para",
        "title": "Of the Present Ability of America",
        "header_pattern": r"^OF THE PRESENT ABILITY OF AMERICA",
    },
    {
        "slug": "appendix",
        "prefix": "appendix-para",
        "title": "Appendix",
        "header_pattern": r"^APPENDIX\.$",
    },
]


def find_chapter_boundaries(text):
    """Find the start line of each chapter by matching header patterns.

    Only matches lines that are fully uppercase and not indented (to avoid
    matching the title page table of contents which is indented).
    """
    lines = text.split('\n')
    boundaries = []

    # Skip the title page area (first ~60 lines of stripped text)
    # by requiring lines to be unindented and fully uppercase
    for ch in CHAPTERS:
        pattern = re.compile(ch["header_pattern"])
        for i, line in enumerate(lines):
            stripped = line.strip()
            raw = line
            # Must not be indented (title page TOC items are indented)
            if raw.startswith(' ') or raw.startswith('\t'):
                continue
            # Must be all uppercase (actual chapter headers are ALL CAPS)
            if stripped != stripped.upper():
                continue
            if pattern.match(stripped):
                boundaries.append((i, ch))
                break

    # Sort by line number
    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def extract_chapter_text(boundaries, lines):
    """Extract the text for each chapter between its header and the next chapter."""
    chapters = []
    for idx, (start_line, ch) in enumerate(boundaries):
        # Skip header lines (the chapter title may span 1-2 lines)
        # Find the first non-blank content line after the header
        content_start = start_line + 1
        # Skip any continuation of the header (e.g., "WITH CONCISE REMARKS...")
        # and blank lines
        while content_start < len(lines):
            stripped = lines[content_start].strip()
            # Skip blank lines and ALL-CAPS continuation lines
            if not stripped:
                content_start += 1
                continue
            if stripped == stripped.upper() and len(stripped) > 5 and not stripped.startswith('"'):
                content_start += 1
                continue
            break

        # End is the start of the next chapter, or end of text
        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][0]
        else:
            end_line = len(lines)

        chapter_text = '\n'.join(lines[content_start:end_line]).strip()
        chapters.append({
            "slug": ch["slug"],
            "prefix": ch["prefix"],
            "title": ch["title"],
            "text": chapter_text,
        })

    return chapters


def split_into_paragraphs(text):
    """Split text into paragraphs (separated by blank lines).

    Merges short fragments that are part of the same logical paragraph
    (e.g., enumerated items like 'First.--...', 'Secondly.--...').
    """
    # Split on double newlines
    raw_paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = []

    for p in raw_paragraphs:
        cleaned = p.strip()
        if not cleaned:
            continue
        # Skip the "AUTHOR" standalone line and "P.S." header artifacts
        if cleaned in ("AUTHOR", "SUBJECTS"):
            continue
        # Normalize internal whitespace (join wrapped lines)
        cleaned = re.sub(r'\n\s*', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        if len(cleaned) < 10:
            # Very short fragment - likely an artifact, skip
            continue
        paragraphs.append(cleaned)

    return paragraphs


def first_sentence_name(text, max_len=80):
    """Extract first sentence, truncated to max_len chars."""
    # Find first sentence boundary
    match = re.search(r'[.;!?]', text)
    if match and match.end() <= max_len:
        return text[:match.end()].strip()
    # No sentence boundary found within limit, truncate
    if len(text) <= max_len:
        return text
    # Truncate at word boundary
    truncated = text[:max_len]
    last_space = truncated.rfind(' ')
    if last_space > 40:
        truncated = truncated[:last_space]
    return truncated + "..."


# Thematic L2 groupings - passages curated by theme across chapters
THEMATIC_GROUPS = [
    {
        "id": "theme-government-necessary-evil",
        "name": "Government as Necessary Evil",
        "about": "Paine's foundational argument: society is a blessing, government is a necessary evil. Humans band together out of want and need; government arises only because we are not angels. The best government is the simplest, the least intrusive, the most accountable. These passages lay the philosophical groundwork that makes the leap to independence feel not radical but inevitable.",
        "for_readers": "These passages capture Paine's political philosophy at its most abstract and enduring. His distinction between society (voluntary cooperation) and government (coerced order) anticipates libertarian, anarchist, and democratic-socialist traditions alike. Every political argument since echoes here.",
    },
    {
        "id": "theme-case-against-monarchy",
        "name": "The Case Against Monarchy",
        "about": "Paine demolishes hereditary monarchy with scripture, logic, and ridicule. Kings began as thugs who seized power; hereditary succession means the sins of the father become the government of the son. The English constitution is not a balanced marvel but a contradictory mess. These passages are Paine at his most forensic and his most funny.",
        "for_readers": "Paine's anti-monarchist arguments draw on biblical history, natural law, and common observation. He makes the case that monarchy is not merely unjust but absurd -- a system that excludes a man from information yet empowers him to make the highest decisions. His mockery of hereditary right ('One of the strongest natural proofs of the folly of hereditary right in kings, is, that nature disapproves it') is devastating precisely because it is plain-spoken.",
    },
    {
        "id": "theme-urgency-of-independence",
        "name": "The Urgency of Independence",
        "about": "The emotional and strategic heart of Common Sense. Paine argues that reconciliation is not merely undesirable but impossible. The blood has already been shed. The moment is NOW -- delay only weakens the cause. These are the passages that turned readers from reluctant subjects into revolutionaries, the rhetoric that made independence feel not like a distant hope but an immediate necessity.",
        "for_readers": "These passages show Paine as propagandist-in-chief. He does not merely argue for independence; he argues that anyone who opposes it is either a coward, a profiteer, or a fool. The emotional escalation is masterful -- from cool logic to righteous fury to the soaring peroration: 'O! receive the fugitive, and prepare in time an asylum for mankind.'",
    },
    {
        "id": "theme-practical-calculation",
        "name": "Practical Calculation",
        "about": "The surprisingly detailed military and economic analysis that makes Common Sense more than a polemic. Paine calculates the cost of a navy, the value of trade, the logistics of defense. He argues that America's lack of a standing army is an advantage, that its debt is manageable, that its resources are sufficient. These passages transform revolution from abstract ideal to concrete plan.",
        "for_readers": "Paine understood that passion alone does not win wars. These passages show his practical side: how many ships, at what cost, with what timber. He argues that NOW is the cheapest time to build a navy, that America's unsettled state makes constitutional innovation possible, that commerce will fund independence. The revolutionary as accountant.",
    },
]


def build_grammar(chapters):
    items = []
    sort_order = 0

    # Track all L1 ids per chapter for chapter-level L2 composite_of
    chapter_item_ids = {}

    # L1: Paragraphs within each chapter
    for ch in chapters:
        paragraphs = split_into_paragraphs(ch["text"])
        chapter_item_ids[ch["slug"]] = []

        for i, para in enumerate(paragraphs):
            sort_order += 1
            para_id = f"{ch['prefix']}-{i+1:02d}"
            name = first_sentence_name(para)

            items.append({
                "id": para_id,
                "name": name,
                "level": 1,
                "category": ch["slug"],
                "sort_order": sort_order,
                "sections": {
                    "Passage": para,
                },
                "keywords": [],
                "metadata": {
                    "chapter": ch["title"],
                    "paragraph_number": i + 1,
                },
            })
            chapter_item_ids[ch["slug"]].append(para_id)

    # L2: Chapter emergence groups
    chapter_abouts = {
        "introduction": {
            "about": "Paine's preamble to the most influential pamphlet in American history. He announces his themes: custom masquerades as right, time makes more converts than reason, and the cause of America is the cause of all mankind. The introduction establishes Paine's voice -- plain, urgent, universal.",
            "for_readers": "The Introduction sets up everything that follows. Paine's opening line ('a long habit of not thinking a thing wrong, gives it a superficial appearance of being right') is one of the great sentences in political philosophy. Notice how he positions himself: no party, no influence, only reason and principle.",
        },
        "origin-and-design-of-government": {
            "about": "The social contract as Paine tells it: humans come together out of need, forming society. Government arises only when virtue fails -- it is 'the badge of lost innocence.' Paine then dissects the English constitution, showing that its vaunted balance of king, lords, and commons is a sham. The crown holds all real power; the rest is theater.",
            "for_readers": "This chapter is Paine's political philosophy in miniature. His thought experiment -- imagining settlers on a new island gradually inventing government -- anticipates Rawls's veil of ignorance by two centuries. His critique of the English constitution is devastating: a system that gives the commons power to check the king, then gives the king power to check the commons, is 'a mere absurdity.'",
        },
        "monarchy-and-hereditary-succession": {
            "about": "Paine's most sustained assault on the idea of kingship. Using scripture, history, and logic, he argues that monarchy was invented by heathens, condemned by God, and perpetuated by violence. Hereditary succession is worse still: it guarantees that fools and tyrants will rule, since birth is no measure of wisdom. The chapter builds from theological argument to historical evidence to pure ridicule.",
            "for_readers": "This is Paine at his most radical. He does not merely argue that George III is a bad king -- he argues that ALL kings are illegitimate. His use of the Old Testament is brilliant: God Himself warned Israel against wanting a king, and every disaster that followed proved Him right. The chapter's emotional climax compares hereditary succession to original sin: the crimes of the first king are visited on every generation.",
        },
        "present-state-of-american-affairs": {
            "about": "The strategic heart of Common Sense. Paine demolishes every argument for reconciliation: Britain did not protect America out of love but out of self-interest; the colonies' connection to Britain drags them into European wars that are none of their business; and the blood already shed at Lexington and Concord makes reconciliation a moral impossibility. The chapter escalates from patient argument to prophetic fury.",
            "for_readers": "This is where Common Sense becomes a call to action. Paine systematically addresses every objection a cautious colonist might raise ('But Britain is the parent country') and demolishes it ('Then the more shame upon her conduct'). The emotional arc is carefully constructed: he moves from reason to outrage to hope, culminating in the soaring invitation to make America 'an asylum for mankind.'",
        },
        "present-ability-of-america": {
            "about": "Paine the revolutionary accountant. He calculates the cost of a continental navy, inventories American resources, and argues that the present moment is uniquely favorable for independence. America has no debt, no entrenched aristocracy, no standing army to fear. The unsettled state of the continent is an advantage: it is easier to build a new constitution than to reform an old one.",
            "for_readers": "After the emotional heights of the previous chapter, Paine grounds the revolution in practical reality. How many ships? What will they cost? Where will the timber come from? He argues that delay will only make independence more expensive and more difficult. His proposed plan of government -- a continental congress with rotating presidency -- shows the pamphleteer thinking like a statesman.",
        },
        "appendix": {
            "about": "Written after the King's Speech reached Philadelphia, the Appendix is Paine's victory lap and his sharpest polemic. He responds to the King's threats, addresses the Quakers' pacifist objections to revolution, and makes his final case that independence is not merely desirable but divinely ordained. The tone shifts between cold legal argument and prophetic denunciation.",
            "for_readers": "The Appendix reveals Paine responding to events in real time -- the King's Speech arrived the same day Common Sense was published, and Paine seized the coincidence as proof of providence. His address to the Quakers is particularly interesting: he respects their pacifism but argues that their political testimony against independence contradicts their own principles of leaving worldly governance to God.",
        },
    }

    for ch in chapters:
        sort_order += 1
        ids = chapter_item_ids[ch["slug"]]
        about_data = chapter_abouts.get(ch["slug"], {})

        sections = {
            "About": about_data.get("about", f"Chapter: {ch['title']}"),
            "For Readers": about_data.get("for_readers", ""),
        }

        items.append({
            "id": f"chapter-{ch['slug']}",
            "name": ch["title"],
            "level": 2,
            "category": "chapter",
            "relationship_type": "emergence",
            "composite_of": ids,
            "sort_order": sort_order,
            "sections": sections,
            "keywords": [],
            "metadata": {
                "paragraph_count": len(ids),
            },
        })

    # L2: Thematic groups
    # We need to assign specific paragraph IDs to each theme.
    # We'll do this by searching paragraph text for relevant content.
    all_l1 = [item for item in items if item["level"] == 1]

    def find_paragraphs_matching(patterns):
        """Find L1 item IDs whose passage text matches any of the given patterns."""
        matched = []
        for item in all_l1:
            text = item["sections"]["Passage"].lower()
            for pat in patterns:
                if pat.lower() in text:
                    if item["id"] not in matched:
                        matched.append(item["id"])
                    break
        return matched

    # Government as Necessary Evil - from intro and ch1 mainly
    gov_evil_patterns = [
        "necessary evil",
        "badge of lost innocence",
        "society in every state is a blessing",
        "society is produced by our wants",
        "design and end of government",
        "inability of moral virtue to govern",
        "the more simple any thing is",
        "security being the true design",
        "some convenient tree will afford",
        "mode rendered necessary",
    ]
    gov_evil_ids = find_paragraphs_matching(gov_evil_patterns)

    # Case Against Monarchy - from ch1 and ch2
    monarchy_patterns = [
        "monarchical tyranny",
        "hereditary succession",
        "crowned ruffian",
        "ridiculous in the composition of monarchy",
        "distinction of men into kings",
        "government by kings was first introduced",
        "original sin",
        "evil of monarchy",
        "king shuts him from the world",
        "will of the almighty",
        "pride of kings which throw mankind",
        "no truly natural or religious reason",
        "overbearing part in the english constitution",
        "sacred majesty applied to a worm",
        "exceedingly ridiculous",
    ]
    monarchy_ids = find_paragraphs_matching(monarchy_patterns)

    # Urgency of Independence - from ch3
    urgency_patterns = [
        "arms, as the last resource",
        "reconciliation is now a falacious dream",
        "the blood of the slain",
        "asylum for mankind",
        "the period of debate is closed",
        "ye that love mankind",
        "every thing that is right or natural pleads for separation",
        "continent will feel itself like a man who continues putting off",
        "the sun never shined on a cause of greater worth",
        "now is the seed-time",
        "but britain is the parent country",
        "hath found us",
        "even brutes do not devour their young",
    ]
    urgency_ids = find_paragraphs_matching(urgency_patterns)

    # Practical Calculation - ch4's military/economic analysis
    # Only match passages specifically about practical planning, resources, costs
    practical_patterns = [
        "continental navy",
        "debt we may contract",
        "national debt is a national bond",
        "no nation ought to be without a debt",
        "tonnage",
        "saltpetre",
        "ship building",
        "one million acres",
        "a navy of seventy",
        "annual expense",
        "men of war",
        "the whole navy of england",
        "number of inhabitants",
        "continental form of government",
        "charter and petition",
        "let the assemblies be annual",
        "the commerce by which she hath enriched herself",
        "the mercantile and reasonable part",
        "three millions of debt",
        "we are not in debt",
        "four or five millions",
        "an army of twenty-five",
        "the continental belt",
        "take a general survey of things",
    ]
    practical_ids = find_paragraphs_matching(practical_patterns)

    thematic_composites = {
        "theme-government-necessary-evil": gov_evil_ids,
        "theme-case-against-monarchy": monarchy_ids,
        "theme-urgency-of-independence": urgency_ids,
        "theme-practical-calculation": practical_ids,
    }

    for theme in THEMATIC_GROUPS:
        sort_order += 1
        composite = thematic_composites.get(theme["id"], [])

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
                "passage_count": len(composite),
            },
        })

    # L3: Common Sense meta connecting all L2 items
    sort_order += 1
    all_l2_ids = [item["id"] for item in items if item["level"] == 2]
    items.append({
        "id": "meta-common-sense",
        "name": "Common Sense",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_l2_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "Thomas Paine's Common Sense is the most influential political pamphlet in American history. Published anonymously in January 1776, it sold 500,000 copies in a colonial population of 2.5 million -- the equivalent of 60 million copies today. Paine did what no one else had dared: he argued not merely for better treatment from Britain, but for complete independence. And he did it in plain language that any farmer, tradesman, or sailor could understand. The pamphlet moves from philosophical foundations (government is a necessary evil) through historical demolition (monarchy is an absurdity) to strategic urgency (the time is NOW) to practical planning (here is what a navy costs). Each chapter builds on the last, constructing an argument so cumulative and so plainly stated that by the end, independence seems not radical but obvious. 'We have it in our power to begin the world over again.'",
        },
        "keywords": [],
        "metadata": {
            "chapter_count": len(chapters),
            "theme_count": len(THEMATIC_GROUPS),
        },
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    text = strip_transcriber_additions(text)

    boundaries, lines = find_chapter_boundaries(text)
    print(f"Found {len(boundaries)} chapters:")
    for line_num, ch in boundaries:
        print(f"  Line {line_num}: {ch['title']}")

    chapters = extract_chapter_text(boundaries, lines)

    total_paragraphs = 0
    for ch in chapters:
        paras = split_into_paragraphs(ch["text"])
        total_paragraphs += len(paras)
        print(f"  {ch['title']}: {len(paras)} paragraphs")

    print(f"Total paragraphs: {total_paragraphs}")

    items = build_grammar(chapters)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Thomas Paine", "date": "1776", "note": "Author"},
            ]
        },
        "name": "Common Sense",
        "description": "Thomas Paine's Common Sense (1776) -- the pamphlet that made the American Revolution inevitable. In plain language that any colonist could understand, Paine argued that hereditary monarchy was absurd, that reconciliation with Britain was impossible, and that the time for independence was NOW. It sold 500,000 copies in a population of 2.5 million. 'A long habit of not thinking a thing wrong, gives it a superficial appearance of being right.'\n\nSource: Project Gutenberg eBook #147 (https://www.gutenberg.org/ebooks/147)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: 18th century American Revolutionary War engravings. Paul Revere's prints. John Trumbull's Declaration of Independence paintings.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["politics", "philosophy", "revolution", "freedom", "public-domain", "full-text", "pamphlet", "democracy"],
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
    print(f"  L1: {l1} paragraphs, L2: {l2} groups ({len(CHAPTERS)} chapters + {len(THEMATIC_GROUPS)} themes), L3: {l3} meta")
    print(f"  Total items: {len(items)}")

    # Validate: check composite_of references
    all_ids = {item["id"] for item in items}
    errors = 0
    for item in items:
        if "composite_of" in item:
            for ref in item["composite_of"]:
                if ref not in all_ids:
                    print(f"  ERROR: {item['id']} references non-existent {ref}")
                    errors += 1
    if errors == 0:
        print("  All composite_of references valid.")
    else:
        print(f"  {errors} reference errors found!")

    # Report thematic group sizes
    print("\nThematic group sizes:")
    for item in items:
        if item["level"] == 2 and item["category"] == "theme":
            print(f"  {item['name']}: {len(item['composite_of'])} passages")


if __name__ == "__main__":
    main()
