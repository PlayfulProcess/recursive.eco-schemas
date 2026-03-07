#!/usr/bin/env python3
"""
Parse Rights of Man by Thomas Paine (Gutenberg #3742, 1791-1792)
into a grammar.json.

Structure:
- L1: Paragraphs within each section/chapter
- L2: Section/chapter emergence groups + thematic groups
- L3: Meta-category connecting all

Note: This edition (Conway ed.) includes an editor's introduction, dedications,
prefaces, and notes. We extract only Paine's own text: Part I body + Miscellaneous
Chapter + Conclusion, and Part II Introduction + Chapters I-V + Appendix.
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "rights-of-man.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "rights-of-man")
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


# Sections to extract. We use line-based detection.
SECTIONS = [
    # Part I
    {
        "slug": "part1-main",
        "prefix": "p1-para",
        "title": "Rights of Man, Part the First",
        "start_pattern": r"^RIGHTS OF MAN\. PART THE FIRST",
        "skip_patterns": [r"^BEING AN ANSWER"],
    },
    {
        "slug": "part1-miscellaneous",
        "prefix": "p1-misc-para",
        "title": "Miscellaneous Chapter",
        "start_pattern": r"^MISCELLANEOUS CHAPTER",
        "skip_patterns": [],
    },
    {
        "slug": "part1-conclusion",
        "prefix": "p1-concl-para",
        "title": "Conclusion of Part the First",
        "start_pattern": r"^CONCLUSION$",
        "skip_patterns": [],
    },
    # Part II
    {
        "slug": "part2-introduction",
        "prefix": "p2-intro-para",
        "title": "Introduction to Part the Second",
        "start_pattern": r"^INTRODUCTION\.$",
        "skip_patterns": [],
    },
    {
        "slug": "part2-ch1-society",
        "prefix": "p2-ch1-para",
        "title": "Of Society and Civilisation",
        "start_pattern": r"^CHAPTER I\. OF SOCIETY AND CIVILISATION",
        "skip_patterns": [],
    },
    {
        "slug": "part2-ch2-old-governments",
        "prefix": "p2-ch2-para",
        "title": "Of the Origin of the Present Old Governments",
        "start_pattern": r"^CHAPTER II\. OF THE ORIGIN",
        "skip_patterns": [],
    },
    {
        "slug": "part2-ch3-old-new-systems",
        "prefix": "p2-ch3-para",
        "title": "Of the Old and New Systems of Government",
        "start_pattern": r"^CHAPTER III\. OF THE OLD AND NEW",
        "skip_patterns": [],
    },
    {
        "slug": "part2-ch4-constitutions",
        "prefix": "p2-ch4-para",
        "title": "Of Constitutions",
        "start_pattern": r"^CHAPTER IV\. OF CONSTITUTIONS",
        "skip_patterns": [],
    },
    {
        "slug": "part2-ch5-ways-and-means",
        "prefix": "p2-ch5-para",
        "title": "Ways and Means of Improving the Condition of Europe",
        "start_pattern": r"^CHAPTER V\. WAYS AND MEANS",
        "skip_patterns": [],
    },
    {
        "slug": "part2-appendix",
        "prefix": "p2-app-para",
        "title": "Appendix",
        "start_pattern": r"^APPENDIX$",
        "skip_patterns": [],
    },
]


def find_section_boundaries(text):
    """Find section start lines. Only match after the editor's intro ends."""
    lines = text.split('\n')
    boundaries = []

    # Find the start of Paine's actual text (after editor's intro)
    # The editor's intro ends and Paine's Part I begins with:
    # "RIGHTS OF MAN. PART THE FIRST BEING AN ANSWER TO MR. BURKE'S ATTACK ON"
    paine_start = 0
    for i, line in enumerate(lines):
        if 'RIGHTS OF MAN. PART THE FIRST' in line.strip():
            paine_start = i
            break

    # For Part II intro, we need the one after "RIGHTS OF MAN PART II."
    part2_start = 0
    for i, line in enumerate(lines):
        if 'RIGHTS OF MAN PART II' in line.strip() or 'RIGHTS OF MAN. PART SECOND' in line.strip():
            part2_start = i

    for sec in SECTIONS:
        pattern = re.compile(sec["start_pattern"])
        search_start = paine_start
        # For Part II sections, search from part2_start
        if sec["slug"].startswith("part2"):
            search_start = part2_start

        for i in range(search_start, len(lines)):
            stripped = lines[i].strip()
            if pattern.match(stripped):
                boundaries.append((i, sec))
                break

    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def extract_section_text(boundaries, lines):
    """Extract text for each section."""
    sections = []

    # Define stop patterns for certain sections
    # Part 1 main stops at MISCELLANEOUS CHAPTER
    # Editor's notes should be excluded

    for idx, (start_line, sec) in enumerate(boundaries):
        content_start = start_line + 1
        # Skip header continuation lines
        while content_start < len(lines):
            stripped = lines[content_start].strip()
            if not stripped:
                content_start += 1
                continue
            # Skip ALL-CAPS continuation of header
            if stripped == stripped.upper() and len(stripped) > 5:
                content_start += 1
                continue
            break

        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][0]
        else:
            end_line = len(lines)

        # For the appendix, stop at NOTES section if present
        if sec["slug"] == "part2-appendix":
            for i in range(start_line, end_line):
                if lines[i].strip() == "NOTES" or lines[i].strip() == "NOTES.":
                    end_line = i
                    break

        # For part1-conclusion, stop at "END OF PART I."
        if sec["slug"] == "part1-conclusion":
            for i in range(start_line, end_line):
                if "END OF PART I" in lines[i]:
                    end_line = i
                    break

        section_text = '\n'.join(lines[content_start:end_line]).strip()
        sections.append({
            "slug": sec["slug"],
            "prefix": sec["prefix"],
            "title": sec["title"],
            "text": section_text,
        })

    return sections


def split_into_paragraphs(text):
    """Split text into paragraphs."""
    raw_paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = []

    for p in raw_paragraphs:
        cleaned = p.strip()
        if not cleaned:
            continue
        if len(cleaned) < 20:
            continue
        # Skip footnote references
        if re.match(r'^\*?\[\d+\]', cleaned):
            continue
        # Skip editorial markers
        if cleaned.startswith('[Redactor') or cleaned.startswith('[Editor'):
            continue
        # Normalize internal whitespace
        cleaned = re.sub(r'\n\s*', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        paragraphs.append(cleaned)

    return paragraphs


def first_sentence_name(text, max_len=80):
    """Extract first sentence, truncated to max_len chars."""
    match = re.search(r'[.;!?]', text)
    if match and match.end() <= max_len:
        return text[:match.end()].strip()
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_space = truncated.rfind(' ')
    if last_space > 40:
        truncated = truncated[:last_space]
    return truncated + "..."


THEMATIC_GROUPS = [
    {
        "id": "theme-natural-rights",
        "name": "Natural Rights",
        "about": "Paine's foundational argument: rights are not granted by governments but belong to every person by nature. They originate in the creation of humanity itself. Civil rights are natural rights exchanged for the security of society, but no generation can bind the next, and no government can take away what nature has given. These passages establish the philosophical basis for democratic revolution.",
        "for_readers": "Paine's theory of natural rights is both radical and lucid. He distinguishes between natural rights (those we possess as individuals: freedom of thought, conscience, and pursuit of happiness) and civil rights (those we exchange for social protection). The key insight: rights belong to the living, not to the dead. No parliament, no constitution, no treaty can bind future generations. Every age must be free to act for itself.",
        "patterns": [
            "natural rights",
            "rights of man",
            "unalienable",
            "civil rights",
            "every generation",
            "born equal",
            "the right of the living",
            "authority of the dead",
            "creation",
            "inherent",
        ],
    },
    {
        "id": "theme-against-monarchy",
        "name": "Against Monarchy and Aristocracy",
        "about": "Paine's devastating assault on hereditary government. Kings and nobles derive their power not from merit but from conquest and theft. Hereditary succession is absurd -- a system that grants power based on birth rather than ability. Burke's defense of the 'age of chivalry' is nostalgia for oppression. The 'rights of man' are incompatible with the privileges of aristocracy.",
        "for_readers": "Paine brings the same anti-monarchist arguments from Common Sense into direct confrontation with Edmund Burke. Where Burke mourns the fall of Marie Antoinette and the 'age of chivalry,' Paine mourns the millions who suffered under it. His argument is simple: if we would not choose a king by lottery, hereditary succession is worse -- because at least a lottery does not pretend merit. Every line drips with democratic contempt for inherited privilege.",
        "patterns": [
            "monarchy",
            "aristocracy",
            "hereditary",
            "burke",
            "chivalry",
            "crown",
            "nobility",
            "bastille",
            "french revolution",
            "despotism",
            "throne",
        ],
    },
    {
        "id": "theme-republican-government",
        "name": "Republican Government",
        "about": "Paine's vision of representative government grounded in reason and the will of the people. A constitution is not a gift from government to the people but an act of the people creating government. The American and French revolutions are not merely political events but the dawn of a new age of reason in government. Republican government is cheaper, more efficient, and more just than monarchy.",
        "for_readers": "Paine's republicanism is practical as well as philosophical. He argues that representative government costs less (no courts, no pensions for aristocrats, no standing armies for foreign wars), governs better (because it is accountable), and respects rights (because it is founded on them). His detailed comparison of British and American/French government expenses is devastating -- the simplicity of the republic versus the bloated luxury of the crown.",
        "patterns": [
            "republic",
            "representative",
            "constitution",
            "america",
            "democratic",
            "election",
            "consent of the governed",
            "reason",
            "declaration of rights",
            "national assembly",
        ],
    },
    {
        "id": "theme-social-welfare",
        "name": "Social Welfare and Reform",
        "about": "The most forward-looking passages in Rights of Man. Paine proposes a comprehensive system of social welfare: universal education, old-age pensions, child allowances, public employment, progressive taxation. He argues that poverty is not natural but the product of bad government, and that a just society would abolish it through redistribution. These proposals anticipated the welfare state by 150 years.",
        "for_readers": "Chapter V of Part II is one of the most remarkable documents in political history. Writing in 1792, Paine proposes: free public education for all children, allowances for poor families, pensions for the elderly, public works for the unemployed, and progressive taxation to fund it all. His detailed calculations -- how much per child, how many elderly, what tax rate -- show a mind that combines revolutionary passion with accountant's precision. The modern welfare state is a partial fulfillment of Paine's vision.",
        "patterns": [
            "education",
            "poor",
            "pension",
            "taxation",
            "revenue",
            "children",
            "welfare",
            "employment",
            "relief",
            "progressive",
            "condition of europe",
        ],
    },
]


SECTION_ABOUTS = {
    "part1-main": {
        "about": "The body of Part I: Paine's direct response to Burke's Reflections on the Revolution in France. He defends the French Revolution as the natural assertion of rights against tyranny, demolishes Burke's reverence for tradition and precedent, and argues that every generation has the right to govern itself. The famous passage: 'He pities the plumage but forgets the dying bird' -- Burke mourns the fate of Marie Antoinette while ignoring the millions who suffered under the old regime.",
        "for_readers": "Part I is Paine at his polemical best. He systematically dismantles Burke's case for tradition, precedent, and inherited institutions. His argument is devastatingly simple: if the living have no right to govern themselves, they are slaves to the dead. His account of the fall of the Bastille and the Declaration of the Rights of Man reads like revolutionary journalism -- vivid, urgent, and partisan. The contrast between Burke's ornate prose and Paine's plain speech is itself an argument for democracy.",
    },
    "part1-miscellaneous": {
        "about": "Paine's supplementary observations on the French Revolution and the nature of government. He addresses specific objections, discusses the role of constitutions, and compares the emerging French system with the British. The chapter reinforces his central argument that legitimate government can only be founded on the rights of the people.",
        "for_readers": "The Miscellaneous Chapter fills in arguments that did not fit the main polemic. Paine discusses the nature of constitutions (a government cannot make one; only the people can), the difference between a country and a court, and the absurdity of primogeniture. Less focused than Part I but full of sharp observations.",
    },
    "part1-conclusion": {
        "about": "Paine's summation of Part I. He predicts that the revolutionary principles of natural rights and representative government will spread across Europe. The age of reason in government has begun, and nothing can stop it. His tone is prophetic: revolution is not an event but a process, and the Rights of Man will triumph everywhere.",
        "for_readers": "The conclusion to Part I is Paine at his most visionary. He sees the French Revolution not as a local event but as the beginning of a worldwide transformation. His prophecy was partly fulfilled: the ideas he championed -- natural rights, popular sovereignty, written constitutions -- did spread across the world, though the path was bloodier and slower than he imagined.",
    },
    "part2-introduction": {
        "about": "Paine's introduction to Part II, written in February 1792. He reaffirms his principles, responds to critics, and announces the broader scope of Part II: not merely defending the French Revolution but proposing practical reforms for all of Europe. The introduction sets up Part II's shift from polemic to constructive political philosophy.",
        "for_readers": "The Part II introduction shows Paine responding to the enormous controversy created by Part I. He had been burned in effigy, prosecuted for sedition, and celebrated as a hero. His tone is confident: the principles of Part I have been vindicated by events, and now he will show how to apply them. The shift from defense to offense marks Part II's ambition to be not merely a reply to Burke but a blueprint for a new society.",
    },
    "part2-ch1-society": {
        "about": "Paine distinguishes between society and government: society is natural, arising from human needs and affections; government is artificial, arising from human wickedness. Most of what we attribute to government is actually done by society itself. If government were abolished tomorrow, society would continue to function. This chapter establishes the theoretical foundation for Paine's argument that government should be minimal and representative.",
        "for_readers": "Chapter I echoes Common Sense's distinction between society and government but develops it further. Paine's argument that 'the more perfect civilisation is, the less occasion has it for government' is the seed of both libertarian and anarchist thought. His observation that most social order is maintained not by laws but by 'the mutual dependence and reciprocal interest which man has upon man' anticipates Kropotkin's Mutual Aid by a century.",
    },
    "part2-ch2-old-governments": {
        "about": "Paine traces the origin of existing governments to conquest and superstition. The 'present old governments' of Europe -- monarchies and aristocracies -- did not arise from the consent of the people but from the sword. They have been maintained by controlling information, restricting education, and mystifying power. A government founded on reason and rights would look entirely different.",
        "for_readers": "This short, devastating chapter strips away the legitimacy of European monarchies. Paine argues that every existing government in Europe (except the new French republic and the American republic) is founded on force and fraud. The simplicity of his analysis is its strength: if you trace any monarchy back to its origin, you find a conqueror. Everything after is rationalization.",
    },
    "part2-ch3-old-new-systems": {
        "about": "Paine compares the 'old system' of hereditary government with the 'new system' of representative government. The old system treats the nation as property of the crown; the new treats government as the servant of the people. Representative government is founded on reason; hereditary government on superstition. The American and French revolutions have demonstrated that the new system works, and works better.",
        "for_readers": "Chapter III is Paine's systematic comparison of monarchy and republic. He argues that representative government is not merely more just but more efficient, less expensive, less war-prone, and more stable. His analysis of why monarchies go to war (personal ambition, dynastic rivalry, the need for military glory) versus why republics tend toward peace (the people who pay for wars are the ones who decide on them) anticipates Kant's 'perpetual peace' by three years.",
    },
    "part2-ch4-constitutions": {
        "about": "Paine's theory of constitutions. A constitution is not an act of government but an act of the people creating government. It must be written, explicit, and supreme over the government it creates. England has no constitution because its 'constitution' is merely whatever Parliament decides -- there is no higher law that Parliament cannot change. America and France have real constitutions because they were created by the people in special conventions.",
        "for_readers": "Chapter IV is Paine's most sustained piece of constitutional theory. His distinction between a constitution (created by the people, binding on government) and ordinary legislation (created by government, binding on the people) remains fundamental to constitutional law. His argument that England has no constitution -- because Parliament can change any law, including its own powers -- was and remains provocative. The American model of a written constitution, ratified by convention, is Paine's ideal.",
    },
    "part2-ch5-ways-and-means": {
        "about": "Paine's blueprint for a just society. He proposes: abolishing primogeniture, progressive taxation on large estates, universal free education, child allowances for poor families, old-age pensions, public employment programs, and funeral allowances. He calculates the costs in detail and shows they can be funded by eliminating the waste of monarchical government. This is the first comprehensive proposal for what we now call the welfare state.",
        "for_readers": "Chapter V is perhaps the most remarkable chapter in all of Paine's writing. In 1792, he proposes a system of social insurance that anticipates the welfare state by 150 years: free education, child benefits, old-age pensions, unemployment relief, progressive taxation. His arithmetic is detailed and specific -- he calculates the number of poor children, the cost per child, the revenue from progressive taxes. This is not utopian dreaming but practical policy, and much of it has since been implemented.",
    },
    "part2-appendix": {
        "about": "Paine's appendix to Part II, addressing additional observations on the French constitution, the nature of revolutions, and the future of European politics. He responds to specific criticisms and reinforces his argument that the age of revolution is just beginning.",
        "for_readers": "The appendix adds supplementary arguments and addresses critics. Paine discusses the practicalities of constitutional reform and predicts that the revolutionary principles of natural rights will spread from France and America to the rest of Europe. His optimism, while premature, proved prophetic in the long run.",
    },
}


def build_grammar(sections_data):
    items = []
    sort_order = 0
    section_item_ids = {}

    for sec in sections_data:
        paragraphs = split_into_paragraphs(sec["text"])
        section_item_ids[sec["slug"]] = []

        for i, para in enumerate(paragraphs):
            sort_order += 1
            para_id = f"{sec['prefix']}-{i+1:02d}"
            name = first_sentence_name(para)

            items.append({
                "id": para_id,
                "name": name,
                "level": 1,
                "category": sec["slug"],
                "sort_order": sort_order,
                "sections": {
                    "Passage": para,
                },
                "keywords": [],
                "metadata": {
                    "section": sec["title"],
                    "paragraph_number": i + 1,
                },
            })
            section_item_ids[sec["slug"]].append(para_id)

    # L2: Section groups
    for sec in sections_data:
        sort_order += 1
        ids = section_item_ids[sec["slug"]]
        about_data = SECTION_ABOUTS.get(sec["slug"], {})

        items.append({
            "id": f"section-{sec['slug']}",
            "name": sec["title"],
            "level": 2,
            "category": "section",
            "relationship_type": "emergence",
            "composite_of": ids,
            "sort_order": sort_order,
            "sections": {
                "About": about_data.get("about", f"Section: {sec['title']}"),
                "For Readers": about_data.get("for_readers", ""),
            },
            "keywords": [],
            "metadata": {
                "paragraph_count": len(ids),
            },
        })

    # L2: Thematic groups
    all_l1 = [item for item in items if item["level"] == 1]

    def find_paragraphs_matching(patterns):
        matched = []
        for item in all_l1:
            text = item["sections"]["Passage"].lower()
            for pat in patterns:
                if pat.lower() in text:
                    if item["id"] not in matched:
                        matched.append(item["id"])
                    break
        return matched

    for theme in THEMATIC_GROUPS:
        sort_order += 1
        composite = find_paragraphs_matching(theme["patterns"])

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

    # L3: Meta
    sort_order += 1
    all_l2_ids = [item["id"] for item in items if item["level"] == 2]
    items.append({
        "id": "meta-rights-of-man",
        "name": "Rights of Man",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_l2_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "Thomas Paine's Rights of Man (1791-1792) is the great manifesto of democratic revolution. Written as a reply to Edmund Burke's Reflections on the Revolution in France, it became far more: a comprehensive argument for natural rights, representative government, and social welfare. Part I defends the French Revolution and demolishes hereditary monarchy. Part II proposes a new system of government founded on reason, including the first detailed blueprint for what we now call the welfare state -- universal education, old-age pensions, child allowances, and progressive taxation. Together, the two parts constitute the most influential argument for democratic government and social justice in the English language. Paine was prosecuted for sedition, burned in effigy, and eventually forced into exile -- but his ideas conquered the world.",
        },
        "keywords": [],
        "metadata": {
            "section_count": len(sections_data),
            "theme_count": len(THEMATIC_GROUPS),
        },
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)

    boundaries, lines = find_section_boundaries(text)
    print(f"Found {len(boundaries)} sections:")
    for line_num, sec in boundaries:
        print(f"  Line {line_num}: {sec['title']}")

    sections_data = extract_section_text(boundaries, lines)

    total_paragraphs = 0
    for sec in sections_data:
        paras = split_into_paragraphs(sec["text"])
        total_paragraphs += len(paras)
        print(f"  {sec['title']}: {len(paras)} paragraphs")

    print(f"Total paragraphs: {total_paragraphs}")

    items = build_grammar(sections_data)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Thomas Paine", "date": "1791-1792", "note": "Author"},
                {"name": "Moncure Daniel Conway", "date": "1894", "note": "Editor"},
            ]
        },
        "name": "Rights of Man",
        "description": "Thomas Paine's Rights of Man (1791-1792) -- the great manifesto of democratic revolution. Written as a reply to Edmund Burke's attack on the French Revolution, it became the most influential argument for natural rights, representative government, and social welfare in the English language. Part I defends the French Revolution and demolishes hereditary monarchy. Part II proposes a comprehensive system of social welfare -- universal education, old-age pensions, child allowances, progressive taxation -- anticipating the welfare state by 150 years. Paine was prosecuted for sedition and burned in effigy; his ideas conquered the world.\n\nSource: Project Gutenberg eBook #3742 (https://www.gutenberg.org/ebooks/3742)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: 18th century political engravings and caricatures. James Gillray's satirical prints. George Romney's portrait of Paine. French Revolution illustrations by contemporary artists.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["politics", "philosophy", "revolution", "rights", "democracy", "welfare", "public-domain", "full-text"],
        "roots": ["freedom-commons"],
        "shelves": ["resilience"],
        "lineages": ["Kelty", "Andreotti"],
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
    print(f"  L1: {l1} paragraphs, L2: {l2} groups, L3: {l3} meta")
    print(f"  Total items: {len(items)}")

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

    print("\nThematic group sizes:")
    for item in items:
        if item["level"] == 2 and item["category"] == "theme":
            print(f"  {item['name']}: {len(item['composite_of'])} passages")


if __name__ == "__main__":
    main()
