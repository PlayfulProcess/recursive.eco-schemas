#!/usr/bin/env python3
"""
Parse On Liberty by John Stuart Mill (Gutenberg #34901, 1859)
into a grammar.json.

Structure:
- L1: Paragraphs within each of 5 chapters
- L2: Chapter emergence groups + thematic groups
- L3: Meta-category connecting all

Note: This edition has a long editor's Introduction (by W.L. Courtney)
which we skip -- we start from Mill's own Chapter I.
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "on-liberty.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "on-liberty")
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


CHAPTERS = [
    {
        "slug": "ch1-introductory",
        "prefix": "ch1-para",
        "title": "Introductory",
        "num": "I",
    },
    {
        "slug": "ch2-thought-and-discussion",
        "prefix": "ch2-para",
        "title": "Of the Liberty of Thought and Discussion",
        "num": "II",
    },
    {
        "slug": "ch3-individuality",
        "prefix": "ch3-para",
        "title": "Of Individuality, as One of the Elements of Well-Being",
        "num": "III",
    },
    {
        "slug": "ch4-limits-of-authority",
        "prefix": "ch4-para",
        "title": "Of the Limits to the Authority of Society Over the Individual",
        "num": "IV",
    },
    {
        "slug": "ch5-applications",
        "prefix": "ch5-para",
        "title": "Applications",
        "num": "V",
    },
]


def find_mills_chapters(text):
    """Find Mill's actual chapters (after the editor's introduction).

    The text has a TOC and then an editor's intro. Mill's text starts with
    the second occurrence of 'CHAPTER I.' after the line 'ON LIBERTY.'
    """
    lines = text.split('\n')

    # Find 'ON LIBERTY.' which marks the start of Mill's actual text
    on_liberty_line = None
    for i, line in enumerate(lines):
        if line.strip() == 'ON LIBERTY.' or line.strip() == 'On Liberty.':
            on_liberty_line = i

    if on_liberty_line is None:
        # Fallback: find the second occurrence of CHAPTER I.
        on_liberty_line = 0

    # Now find CHAPTER markers after on_liberty_line
    chapter_starts = []
    for ch in CHAPTERS:
        pattern = f"CHAPTER {ch['num']}."
        for i in range(on_liberty_line, len(lines)):
            if lines[i].strip() == pattern:
                chapter_starts.append((i, ch))
                break

    chapter_starts.sort(key=lambda x: x[0])
    return chapter_starts, lines


def extract_chapter_text(boundaries, lines):
    """Extract text for each chapter."""
    chapters = []
    for idx, (start_line, ch) in enumerate(boundaries):
        # Skip chapter number line, title line, and blank lines
        content_start = start_line + 1
        while content_start < len(lines):
            stripped = lines[content_start].strip()
            if not stripped:
                content_start += 1
                continue
            # Skip chapter title lines (ALL CAPS or title case followed by period)
            if stripped.endswith('.') and (stripped == stripped.upper() or len(stripped) < 80):
                # Check if it's a chapter title
                if any(t in stripped.upper() for t in ['INTRODUCTORY', 'LIBERTY', 'INDIVIDUALITY', 'LIMITS', 'APPLICATIONS', 'WELL-BEING', 'AUTHORITY', 'DISCUSSION']):
                    content_start += 1
                    continue
            break

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
    """Split text into paragraphs."""
    raw_paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = []

    for p in raw_paragraphs:
        cleaned = p.strip()
        if not cleaned:
            continue
        if len(cleaned) < 20:
            continue
        # Skip epigraphs / poetry fragments that are indented
        # Normalize internal whitespace
        cleaned = re.sub(r'\n\s*', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        # Skip footnote-only paragraphs
        if re.match(r'^\[\d+\]', cleaned) and len(cleaned) < 50:
            continue
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
        "id": "theme-harm-principle",
        "name": "The Harm Principle",
        "about": "Mill's central argument: the only legitimate reason for society to restrict individual liberty is to prevent harm to others. Self-regarding actions -- however foolish, self-destructive, or offensive -- are not the business of the state or the majority. This principle, radical in 1859, remains the foundation of liberal political philosophy and the touchstone of debates about drug laws, censorship, and personal freedom.",
        "for_readers": "The harm principle sounds simple but its implications are explosive. Mill argues that society has no right to interfere with an individual's choices about their own body, mind, or lifestyle, even when the majority finds those choices repugnant. The principle draws a bright line between other-regarding and self-regarding actions -- and insists that the burden of proof always falls on those who would restrict freedom.",
        "patterns": [
            "harm to others",
            "self-regarding",
            "other-regarding",
            "the only purpose for which power can be rightfully exercised",
            "his own good, either physical or moral, is not a sufficient warrant",
            "over himself, over his own body and mind, the individual is sovereign",
            "prevent harm",
            "tyranny of the majority",
        ],
    },
    {
        "id": "theme-free-speech",
        "name": "The Case for Free Speech",
        "about": "Mill's defense of absolute freedom of thought and expression -- the most sustained and influential argument for free speech ever written. He argues that silencing opinion is wrong whether the opinion is true, false, or partly both: if true, we lose truth; if false, we lose the living understanding that comes only from challenge; if partly true, we lose the correction. All silencing of discussion is an assumption of infallibility.",
        "for_readers": "Chapter II is the intellectual arsenal of free speech. Mill does not merely defend the right to speak; he argues that hearing opposing views is essential to understanding your own. An opinion held without challenge becomes 'dead dogma.' His four grounds for free speech (the silenced opinion may be true; even if false, challenging it strengthens truth; most opinions are partly true; unchallenged opinions become prejudices) remain the structure of every free speech argument today.",
        "patterns": [
            "liberty of thought",
            "freedom of opinion",
            "silencing the expression",
            "assumption of infallibility",
            "dead dogma",
            "free discussion",
            "liberty of the press",
            "marketplace of ideas",
            "complete liberty of contradicting",
            "opinion which it is attempted to suppress",
        ],
    },
    {
        "id": "theme-individuality",
        "name": "The Value of Individuality",
        "about": "Mill's passionate defense of eccentricity, originality, and the development of individual character. He argues that conformity -- even voluntary conformity -- deadens the human spirit. A society of individuals who merely follow custom is a society of sheep. Progress requires people who think for themselves, experiment with living, and dare to be different. The 'tyranny of opinion' is as dangerous as the tyranny of law.",
        "for_readers": "Chapter III is Mill at his most Romantic. He channels Wilhelm von Humboldt's vision of human flourishing through diverse self-development. His argument that 'the mere example of non-conformity' is a service to society challenges us to value the eccentric, the dissenter, the person who refuses to fit in. His warning that 'the despotism of custom' threatens to flatten all individuality into mediocrity remains urgently relevant.",
        "patterns": [
            "individuality",
            "eccentricity",
            "originality",
            "character",
            "development",
            "custom",
            "conformity",
            "experiments of living",
            "human development",
            "genius",
            "spontaneity",
            "the tyranny of opinion",
        ],
    },
    {
        "id": "theme-limits-of-state",
        "name": "Limits of State Power",
        "about": "Mill's practical philosophy of where to draw the line between individual liberty and social control. He distinguishes between actions that harm only the actor (never legitimately prohibited) and those that harm others (subject to regulation). He addresses specific cases: trade restrictions, licensing, public decency, education, marriage -- working out the implications of the harm principle in concrete detail.",
        "for_readers": "The final two chapters move from philosophy to policy. Mill considers real cases: should opium be taxed? Should polygamy be tolerated? Should education be compulsory? His answers are nuanced but consistent: the state may educate but not prescribe doctrine; it may tax harmful goods but not prohibit them; it may regulate behavior that harms others but never behavior that harms only the self. The framework remains the best guide to thinking about liberty in practice.",
        "patterns": [
            "state",
            "government",
            "legislation",
            "prohibit",
            "restrict",
            "regulate",
            "compulsory",
            "taxation",
            "trade",
            "public decency",
            "license",
        ],
    },
]


CHAPTER_ABOUTS = {
    "ch1-introductory": {
        "about": "Mill defines his subject: not metaphysical free will but civil liberty -- the limits of the power that society may legitimately exercise over the individual. He traces the history of the struggle for liberty from ancient tyrannies through representative government, identifying a new danger: the 'tyranny of the majority,' which can be more oppressive than any despot because it leaves fewer means of escape. He states his single principle: the only legitimate purpose of power over individuals is to prevent harm to others.",
        "for_readers": "The Introductory chapter is Mill's philosophical manifesto. He reframes the question of liberty: the danger is no longer kings but majorities. His 'one very simple principle' -- that power can only be exercised over an individual to prevent harm to others -- is the seed from which the entire essay grows. Note his careful qualification: this applies only to people 'in the maturity of their faculties,' not children or 'barbarians.' This limitation has been debated ever since.",
    },
    "ch2-thought-and-discussion": {
        "about": "Mill's exhaustive case for freedom of thought and expression. He argues that silencing any opinion is wrong because: (1) the opinion may be true, and denying it assumes infallibility; (2) even if false, truth needs to be tested by opposition to remain living; (3) most opinions contain partial truth, recoverable only through free debate; (4) opinions held as dogma, without challenge, become dead formulas. This is the most sustained defense of free speech in the English language.",
        "for_readers": "Chapter II is the intellectual heart of On Liberty and the foundation of modern free speech doctrine. Mill does not merely assert a right to speak; he argues that hearing opposing views is necessary for understanding one's own beliefs. His argument that an unchallenged truth becomes a 'dead dogma' -- held as prejudice rather than understanding -- is perhaps his most penetrating insight. Every contemporary debate about censorship, hate speech, and 'cancel culture' is a footnote to this chapter.",
    },
    "ch3-individuality": {
        "about": "Mill's defense of individuality as an essential element of human well-being. He argues that custom and public opinion exert a deadening conformity on modern life, suppressing originality, eccentricity, and the development of individual character. Drawing on Wilhelm von Humboldt, he insists that human development requires freedom to make one's own choices and learn from one's own mistakes. 'Experiments of living' are valuable not only to the individual but to society as a whole.",
        "for_readers": "This chapter is Mill the Romantic, Mill the champion of the extraordinary individual. His argument that 'the mere example of non-conformity, the mere refusal to bend the knee to custom, is itself a service' challenges every pressure to fit in. His fear that 'the despotism of custom' would crush all originality anticipates twentieth-century anxieties about mass society, conformism, and the loss of authentic selfhood.",
    },
    "ch4-limits-of-authority": {
        "about": "Mill works out the practical implications of his principle. What do individuals owe to society? Only not to injure the interests of others. Beyond that, their lives are their own. He considers hard cases: what about actions that are self-destructive but set a bad example? What about offensive behavior? His answer is consistent: advise, persuade, avoid -- but do not coerce. Coercion is justified only when specific, identifiable harm to others can be demonstrated.",
        "for_readers": "Chapter IV is where Mill's principle meets reality. He draws careful distinctions: society may express displeasure at foolish choices but may not punish them; it may refuse to associate with someone but may not compel them to change. His treatment of the distinction between causing offense and causing harm remains relevant to every debate about hate speech, drug policy, and personal freedom.",
    },
    "ch5-applications": {
        "about": "Mill applies his principles to specific controversies: trade restrictions, licensing of professions, sabbath laws, temperance legislation, polygamy, and education. His general rule: free trade should prevail except where public safety is at risk; education should be compulsory but not state-monopolized; individuals should be free to live as they choose so long as they do not harm others. He concludes with a warning against the growth of state bureaucracy, which threatens liberty even when well-intentioned.",
        "for_readers": "The Applications chapter reveals Mill as a practical philosopher, not merely a theorist. His discussions of specific issues -- should poisons be freely sold? should professionals be licensed? should Mormons practice polygamy? -- show how the harm principle works in practice. His final warning that a society which 'makes its best men instruments of administrative purposes' will produce only 'the small, narrow type of character' is prophetic.",
    },
}


def build_grammar(chapters):
    items = []
    sort_order = 0
    chapter_item_ids = {}

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

    # L2: Chapter groups
    for ch in chapters:
        sort_order += 1
        ids = chapter_item_ids[ch["slug"]]
        about_data = CHAPTER_ABOUTS.get(ch["slug"], {})

        items.append({
            "id": f"chapter-{ch['slug']}",
            "name": ch["title"],
            "level": 2,
            "category": "chapter",
            "relationship_type": "emergence",
            "composite_of": ids,
            "sort_order": sort_order,
            "sections": {
                "About": about_data.get("about", f"Chapter: {ch['title']}"),
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
        "id": "meta-on-liberty",
        "name": "On Liberty",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_l2_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "John Stuart Mill's On Liberty (1859) is the foundational text of modern liberalism. Written in collaboration with his wife Harriet Taylor, it argues that individual freedom is not merely a political right but an essential condition of human flourishing. Mill's 'one very simple principle' -- that the only legitimate reason to restrict individual liberty is to prevent harm to others -- remains the touchstone of every debate about censorship, drug policy, hate speech, and personal freedom. The essay moves from the philosophical foundation (Chapter I) through the case for free speech (Chapter II), the value of individuality (Chapter III), the limits of social authority (Chapter IV), to practical applications (Chapter V). Its central warning -- that 'the tyranny of the majority' can be more oppressive than any despot -- grows more urgent with every passing year.",
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

    boundaries, lines = find_mills_chapters(text)
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
                {"name": "John Stuart Mill", "date": "1859", "note": "Author"},
                {"name": "W.L. Courtney", "date": "1901", "note": "Introduction (excluded from grammar)"},
            ]
        },
        "name": "On Liberty",
        "description": "John Stuart Mill's On Liberty (1859) -- the foundational text of modern liberalism. Mill argues that individual freedom is not merely a political right but the essential condition of human flourishing. His 'one very simple principle' -- that the only legitimate purpose of power over the individual is to prevent harm to others -- defines the boundary between personal autonomy and social control. His defense of free speech, eccentricity, and 'experiments of living' remains the intellectual arsenal of everyone who believes that society has no business telling individuals how to live.\n\nSource: Project Gutenberg eBook #34901 (https://www.gutenberg.org/ebooks/34901)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Victorian-era portraits and engravings. George Frederic Watts's portrait of Mill (1873). 19th century parliamentary and political illustrations.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["politics", "philosophy", "freedom", "liberalism", "free-speech", "public-domain", "full-text"],
        "roots": ["freedom-commons"],
        "shelves": ["mirror"],
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
