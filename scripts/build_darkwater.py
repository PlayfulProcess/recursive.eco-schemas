#!/usr/bin/env python3
"""
Parse "Darkwater: Voices from Within the Veil" by W.E.B. Du Bois (Gutenberg #15210, 1920)
into a grammar.json.

Structure: 10 essays interleaved with poems/stories/litanies, plus Credo and Postscript.
- L1: Paragraphs within each piece
- L2: Chapter groups (essays + their paired interludes) + thematic groups
- L3: Meta-categories
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "darkwater.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "darkwater")
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


# The pieces of Darkwater in order
PIECES = [
    {"marker": "_Credo_", "slug": "credo", "title": "Credo", "type": "poem",
     "summary": "Du Bois's declaration of faith — a prose poem that affirms belief in God, in the Negro race, in service, in liberty, in the training of children, and in patience. A creed that is both personal and political, spiritual and secular."},
    {"marker_roman": "I", "marker_title": "THE SHADOW OF YEARS", "slug": "ch01-shadow-of-years",
     "title": "I. The Shadow of Years", "type": "essay",
     "summary": "Du Bois's spiritual autobiography — from his birth in Great Barrington, Massachusetts, through Fisk, Harvard, Berlin, and Atlanta. He traces the growth of his racial consciousness and the events that shaped his thought, culminating in the Atlanta race riot and the death of his son."},
    {"marker": "_A Litany at Atlanta_", "slug": "litany-atlanta", "title": "A Litany at Atlanta", "type": "poem",
     "summary": "A prayer written during the 1906 Atlanta race riot — one of the most powerful poems of the twentieth century. Du Bois cries out to a silent God while his people are being murdered in the streets."},
    {"marker_roman": "II", "marker_title": "THE SOULS OF WHITE FOLK", "slug": "ch02-souls-white-folk",
     "title": "II. The Souls of White Folk", "type": "essay",
     "summary": "Du Bois's searing analysis of whiteness as a constructed identity built on global exploitation. He argues that World War I was fundamentally a war over the right to exploit darker peoples, and that white supremacy is not a fixed fact but a modern invention."},
    {"marker": "_The Riddle of the Sphinx_", "slug": "riddle-sphinx", "title": "The Riddle of the Sphinx", "type": "poem",
     "summary": "A poem about Africa as the Sphinx — ancient, silent, waiting. The dark daughter of the lotus leaves, a spirit panting to be free."},
    {"marker_roman": "III", "marker_title": "THE HANDS OF ETHIOPIA", "slug": "ch03-hands-ethiopia",
     "title": "III. The Hands of Ethiopia", "type": "essay",
     "summary": "An argument for African self-determination and an internationalist vision of Black liberation. Du Bois calls for democratic development in Africa and connects the fates of Black people worldwide."},
    {"marker": "_The Princess of the Hither Isles_", "slug": "princess-hither-isles",
     "title": "The Princess of the Hither Isles", "type": "story",
     "summary": "An allegorical fairy tale about a beautiful soul imprisoned between the This and Now, whose freedom depends on confronting the truth about race and empire."},
    {"marker_roman": "IV", "marker_title": "OF WORK AND WEALTH", "slug": "ch04-work-wealth",
     "title": "IV. Of Work and Wealth", "type": "essay",
     "summary": "An analysis of labor, capitalism, and racial exploitation — centered on the 1917 East St. Louis race riots. Du Bois connects economic competition, union racism, and mob violence to show how capitalism divides workers along the color line."},
    {"marker": "_The Second Coming_", "slug": "second-coming", "title": "The Second Coming", "type": "story",
     "summary": "A visionary story in which Christ returns — as a Black man in the American South."},
    {"marker_roman": "V", "marker_title": "\"THE SERVANT IN THE HOUSE\"", "slug": "ch05-servant-house",
     "title": "V. The Servant in the House", "type": "essay",
     "summary": "A meditation on domestic service and the degradation of Black labor. Du Bois recounts his own experiences as a servant and connects them to the larger system of racial economic subordination."},
    {"marker": "_Jesus Christ in Texas_", "slug": "jesus-texas", "title": "Jesus Christ in Texas", "type": "story",
     "summary": "A devastating short story: a stranger appears in a Texas town, is taken for white, reveals himself as of mixed race, and is lynched. The stranger is Christ."},
    {"marker_roman": "VI", "marker_title": "OF THE RULING OF MEN", "slug": "ch06-ruling-men",
     "title": "VI. Of the Ruling of Men", "type": "essay",
     "summary": "An argument for democracy — real democracy, extended to all people regardless of race, sex, or class. Du Bois makes the case for women's suffrage and universal franchise as the only path to just governance."},
    {"marker": "_The Call_", "slug": "the-call", "title": "The Call", "type": "poem",
     "summary": "A poem summoning the reader to action — a call to awaken and join the struggle for justice."},
    {"marker_roman": "VII", "marker_title": "THE DAMNATION OF WOMEN", "slug": "ch07-damnation-women",
     "title": "VII. The Damnation of Women", "type": "essay",
     "summary": "One of the earliest feminist essays by a male American intellectual. Du Bois argues that the oppression of women — especially Black women — is inseparable from racial oppression. He celebrates Black women as workers, mothers, and leaders."},
    {"marker": "_Children of the Moon_", "slug": "children-moon", "title": "Children of the Moon", "type": "story",
     "summary": "A mythological story about the children born of the moon — an allegory of mixed-race identity and the beauty that arises from the meeting of worlds."},
    {"marker_roman": "VIII", "marker_title": "THE IMMORTAL CHILD", "slug": "ch08-immortal-child",
     "title": "VIII. The Immortal Child", "type": "essay",
     "summary": "An argument for universal education and the protection of children. Du Bois envisions education as the great equalizer and calls for the end of child labor and racial segregation in schools."},
    {"marker": "_Almighty Death_", "slug": "almighty-death", "title": "Almighty Death", "type": "poem",
     "summary": "A meditation on death as both destroyer and liberator — the great leveler that makes all human distinctions meaningless."},
    {"marker_roman": "IX", "marker_title": "OF BEAUTY AND DEATH", "slug": "ch09-beauty-death",
     "title": "IX. Of Beauty and Death", "type": "essay",
     "summary": "Du Bois reflects on beauty, art, and the proximity of death in Black life. He describes the landscape of Maine, the horrors of the Houston riot of 1917, and the way beauty and violence coexist in the American experience."},
    {"marker": "_The Prayers of God_", "slug": "prayers-of-god", "title": "The Prayers of God", "type": "poem",
     "summary": "A dramatic poem in which God hears the prayers of different peoples and is forced to confront the violence done in His name."},
    {"marker_roman": "X", "marker_title": "THE COMET", "slug": "ch10-the-comet",
     "title": "X. The Comet", "type": "story",
     "summary": "Du Bois's science fiction story — a comet's gases kill everyone in New York except a Black man and a white woman, who find each other in the empty city. For a moment, race dissolves. Then the world returns."},
    {"marker": "_A Hymn to the Peoples_", "slug": "hymn-peoples", "title": "A Hymn to the Peoples", "type": "poem",
     "summary": "The closing poem — a hymn of solidarity addressed to all the peoples of the earth, calling for unity across the color line."},
]


def find_piece_boundaries(text):
    """Find the start line of each piece."""
    lines = text.split('\n')
    boundaries = []

    for piece in PIECES:
        if "marker" in piece:
            # Exact line match for poems/stories
            marker = piece["marker"]
            for i, line in enumerate(lines):
                if line.strip() == marker:
                    boundaries.append((i, piece))
                    break
        elif "marker_roman" in piece:
            # Roman numeral on its own line, followed by title
            roman = piece["marker_roman"]
            for i, line in enumerate(lines):
                if line.strip() == roman:
                    # Check next non-blank line for title
                    for j in range(i+1, min(i+5, len(lines))):
                        if lines[j].strip():
                            title_words = piece["marker_title"].replace('"', '').split()[:3]
                            line_text = lines[j].strip().replace('"', '')
                            if title_words[0] in line_text:
                                boundaries.append((i, piece))
                            break
                    break

    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def extract_piece_texts(boundaries, lines):
    """Extract text for each piece."""
    results = []
    for idx, (start_line, piece) in enumerate(boundaries):
        # Skip header lines
        content_start = start_line + 1
        # Skip the marker line, title line, and blank lines
        while content_start < len(lines) and not lines[content_start].strip():
            content_start += 1
        # If this is an essay with roman + title, skip the title
        if "marker_roman" in piece:
            content_start += 1  # skip title line
            while content_start < len(lines) and not lines[content_start].strip():
                content_start += 1

        # End at next boundary or end of text
        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][0]
        else:
            end_line = len(lines)

        text = '\n'.join(lines[content_start:end_line]).strip()
        results.append({"piece": piece, "text": text})
    return results


def split_into_paragraphs(text):
    """Split text into paragraphs."""
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    raw = re.split(r'\n\s*\n', text)
    paragraphs = []
    for p in raw:
        cleaned = p.strip()
        if not cleaned:
            continue
        # Normalize whitespace but preserve paragraph structure
        cleaned = re.sub(r'\n\s*', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        # Remove underscore italics markers
        cleaned = cleaned.replace('_', '')
        if len(cleaned) < 10:
            continue
        paragraphs.append(cleaned)
    return paragraphs


def first_sentence_name(text, max_len=90):
    """Extract first sentence or clause."""
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


def extract_keywords(para):
    """Extract relevant keywords."""
    keyword_map = {
        "veil": "the-veil",
        "race": "race",
        "white folk": "whiteness",
        "war": "war",
        "democracy": "democracy",
        "labor": "labor",
        "women": "women",
        "education": "education",
        "God": "religion",
        "pray": "religion",
        "beauty": "beauty",
        "death": "death",
        "Africa": "africa",
        "Ethiopia": "africa",
        "soul": "soul",
        "color": "color-line",
        "servant": "labor",
        "child": "children",
        "freedom": "freedom",
        "lynch": "violence",
    }
    para_lower = para.lower()
    seen = set()
    keywords = []
    for trigger, kw in keyword_map.items():
        if trigger.lower() in para_lower and kw not in seen:
            keywords.append(kw)
            seen.add(kw)
    return keywords


THEMATIC_GROUPS = [
    {
        "id": "theme-race-and-whiteness",
        "name": "Race and the Construction of Whiteness",
        "about": "Du Bois's analysis of race as a global system — not merely an American peculiarity but a structure of planetary exploitation. 'The Souls of White Folk' is the centerpiece: a dissection of whiteness as an ideology born of colonialism and maintained by violence. These passages anticipate critical race theory by half a century.",
        "for_readers": "Du Bois was among the first thinkers to analyze whiteness itself as a racial category rather than a neutral default. These essays show how race functions not as biology but as a system of economic and political power, maintained by the threat of violence.",
        "sources": ["ch02-souls-white-folk", "ch03-hands-ethiopia"],
    },
    {
        "id": "theme-labor-and-justice",
        "name": "Labor, Wealth, and Racial Justice",
        "about": "Du Bois's economic analysis — how capitalism uses race to divide workers, how domestic service degrades, how the wealth of nations is built on stolen labor. The East St. Louis riot of 1917 is the central case study: white workers, manipulated by capitalists, massacre Black workers who were brought in as strikebreakers.",
        "for_readers": "These chapters connect racial violence to economic structure. Du Bois argues that racism is not merely prejudice but a system of labor exploitation. The servant chapters are among the most personal in the book.",
        "sources": ["ch04-work-wealth", "ch05-servant-house"],
    },
    {
        "id": "theme-democracy-and-feminism",
        "name": "Democracy, Women, and the Vote",
        "about": "Du Bois's argument for universal democracy — not just votes for Black men, but for women of all races, for workers, for the colonized. 'The Damnation of Women' is one of the earliest feminist essays by a prominent male intellectual, celebrating Black women as workers, mothers, and leaders.",
        "for_readers": "Du Bois wrote 'The Damnation of Women' in 1920, the year the Nineteenth Amendment was ratified. His feminism was not abstract but grounded in the specific experiences of Black women. His argument for democracy extends to all colonized peoples.",
        "sources": ["ch06-ruling-men", "ch07-damnation-women"],
    },
    {
        "id": "theme-beauty-death-spirit",
        "name": "Beauty, Death, and the Spirit",
        "about": "The lyrical and spiritual dimension of Darkwater — beauty found in the midst of violence, death as both destroyer and liberator, the prayers that ascend from a suffering people. Du Bois the sociologist yields to Du Bois the poet, and the book's interleaved poems and stories carry the emotional weight that the essays analyze.",
        "for_readers": "The interludes — the Litany at Atlanta, the Prayers of God, Almighty Death — are not decorations but essential components. They carry what argument alone cannot: grief, rage, hope, and beauty. 'The Comet' is Du Bois's only science fiction, imagining a world without the color line.",
        "sources": ["ch09-beauty-death", "ch01-shadow-of-years", "ch08-immortal-child"],
    },
    {
        "id": "theme-literary-interludes",
        "name": "Poems, Stories, and Visions",
        "about": "The literary interludes that punctuate Darkwater — poems, parables, allegories, and one science fiction story. These pieces do what the essays cannot: they imagine, they pray, they mourn, they dream. Jesus Christ appears in Texas and is lynched. A comet destroys the color line. The moon bears children of impossible beauty. God hears the prayers of all peoples and weeps.",
        "for_readers": "Read the interludes alongside their paired essays. Each poem or story deepens the argument of the chapter that precedes it. The Litany at Atlanta is raw grief; The Comet is utopian imagination; Jesus Christ in Texas is bitter prophecy.",
        "sources": ["credo", "litany-atlanta", "riddle-sphinx", "princess-hither-isles",
                     "second-coming", "jesus-texas", "the-call", "children-moon",
                     "almighty-death", "prayers-of-god", "ch10-the-comet", "hymn-peoples"],
    },
]


def build_grammar():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)

    # Remove the duplicate production credits at the top
    for skip_marker in ["Produced by Suzanne Shell"]:
        idx = text.find(skip_marker)
        if idx != -1 and idx < 200:
            # Find next double newline
            end = text.find('\n\n', idx)
            if end != -1:
                text = text[end:].strip()

    boundaries, lines = find_piece_boundaries(text)
    piece_texts = extract_piece_texts(boundaries, lines)

    items = []
    sort_order = 0
    piece_item_ids = {}  # slug -> list of L1 item ids

    # --- L1: Paragraphs within each piece ---
    for pt in piece_texts:
        piece = pt["piece"]
        slug = piece["slug"]
        paragraphs = split_into_paragraphs(pt["text"])
        piece_item_ids[slug] = []

        section_name = "Passage"
        if piece["type"] == "poem":
            section_name = "Verse"
        elif piece["type"] == "story":
            section_name = "Passage"

        for i, para in enumerate(paragraphs):
            sort_order += 1
            para_id = f"{slug}-p{i+1:02d}"
            name = first_sentence_name(para)
            keywords = extract_keywords(para)

            item = {
                "id": para_id,
                "name": name,
                "level": 1,
                "category": slug,
                "sort_order": sort_order,
                "sections": {
                    section_name: para,
                },
                "keywords": keywords,
                "metadata": {
                    "paragraph_number": i + 1,
                    "piece_title": piece["title"],
                    "piece_type": piece["type"],
                },
            }
            items.append(item)
            piece_item_ids[slug].append(para_id)

    # --- L2: Piece groups ---
    for piece in PIECES:
        slug = piece["slug"]
        sort_order += 1
        ids = piece_item_ids.get(slug, [])

        items.append({
            "id": f"piece-{slug}",
            "name": piece["title"],
            "level": 2,
            "category": f"{piece['type']}-group",
            "sort_order": sort_order,
            "sections": {
                "About": piece["summary"],
            },
            "keywords": [],
            "composite_of": ids,
            "relationship_type": "emergence",
            "metadata": {"piece_type": piece["type"]},
        })

    # --- L2: Thematic groups ---
    for tg in THEMATIC_GROUPS:
        sort_order += 1
        composite_ids = []
        for src_slug in tg["sources"]:
            composite_ids.extend(piece_item_ids.get(src_slug, []))

        items.append({
            "id": tg["id"],
            "name": tg["name"],
            "level": 2,
            "category": "thematic-group",
            "sort_order": sort_order,
            "sections": {
                "About": tg["about"],
                "For Readers": tg["for_readers"],
            },
            "keywords": [],
            "composite_of": composite_ids,
            "relationship_type": "emergence",
            "metadata": {},
        })

    # --- L3: Meta-categories ---
    essay_ids = [f"piece-{p['slug']}" for p in PIECES if p["type"] == "essay"]
    literary_ids = [f"piece-{p['slug']}" for p in PIECES if p["type"] in ("poem", "story")]
    thematic_ids = [tg["id"] for tg in THEMATIC_GROUPS]

    sort_order += 1
    items.append({
        "id": "meta-voices-from-the-veil",
        "name": "Voices from Within the Veil",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "Darkwater read as Du Bois structured it — ten essays interwoven with poems, stories, and prayers. The essays argue; the interludes dream, mourn, and imagine. Together they create a polyphonic text that is simultaneously sociology, autobiography, political theory, fiction, and prayer. The Veil is both barrier and vantage point: from within it, Du Bois sees what those outside cannot.",
            "For Readers": "Read in order to experience the alternation of argument and vision. Each essay-interlude pair is a unit: the essay analyzes, the poem or story feels. The book builds from autobiography through global analysis to utopian imagination.",
        },
        "keywords": ["the-veil", "polyphonic", "essays-and-poems"],
        "composite_of": essay_ids + literary_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    sort_order += 1
    items.append({
        "id": "meta-themes-of-darkwater",
        "name": "Themes of Darkwater",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "Darkwater read thematically — the great subjects that Du Bois weaves through essays and interludes alike. Race and whiteness. Labor and economic justice. Democracy and feminism. Beauty, death, and the spirit. Literary imagination. These themes cut across the book's alternating structure, revealing how a single mind confronted the totality of the color line.",
            "For Readers": "These thematic groupings let you explore Darkwater by subject. The race and whiteness cluster gathers Du Bois's most radical analysis. The labor chapters connect economics to violence. The democracy chapters include his feminism. The literary interludes carry the emotional and imaginative weight.",
        },
        "keywords": ["themes", "the-veil", "global-color-line"],
        "composite_of": thematic_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "W. E. B. Du Bois", "date": "1920", "note": "Author"},
                {"name": "Project Gutenberg", "date": "2005", "note": "Digital source, eBook #15210"},
            ]
        },
        "name": "Darkwater: Voices from Within the Veil",
        "description": "W. E. B. Du Bois's 'Darkwater: Voices from Within the Veil' (1920) — the fiery sequel to 'The Souls of Black Folk.' Where Souls was measured and sociological, Darkwater is passionate and prophetic. Ten essays on race, labor, democracy, feminism, and empire are interwoven with poems, prayers, allegorical stories, and one remarkable science fiction tale. Du Bois analyzes whiteness as a global system of exploitation, argues for women's suffrage and workers' rights, and imagines a world transformed. Contains 'The Souls of White Folk,' 'A Litany at Atlanta,' and 'The Comet.'\n\nSource: Project Gutenberg eBook #15210 (https://www.gutenberg.org/ebooks/15210)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs of W. E. B. Du Bois circa 1920. Illustrations from the 1920 first edition published by Harcourt, Brace and Howe. Photographs from the Crisis magazine. Images from the 1900 Paris Exposition Negro Exhibit.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "race", "whiteness", "feminism", "labor", "democracy",
            "poetry", "fiction", "essay", "public-domain", "full-text",
            "african-american", "social-justice", "colonialism"
        ],
        "roots": ["african-diaspora"],
        "shelves": ["resilience", "mirror"],
        "lineages": ["Akomolafe", "Andreotti"],
        "worldview": "dialectical",
        "items": items,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"Generated {len(items)} items: {l1} L1 + {l2} L2 + {l3} L3")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    build_grammar()
