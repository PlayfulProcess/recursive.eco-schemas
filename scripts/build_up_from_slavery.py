#!/usr/bin/env python3
"""
Parse "Up from Slavery" by Booker T. Washington (Gutenberg #2376, 1901) into a grammar.json.

Structure:
- L1: Paragraphs within each chapter (including Preface and Introduction)
- L2: Chapter groups + thematic groups
- L3: Meta-categories
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "up-from-slavery.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "up-from-slavery")
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
    {"roman": "I", "slug": "ch01", "title": "A Slave Among Slaves",
     "summary": "Washington's earliest memories — born a slave in Virginia, living in a one-room cabin, wearing a flax shirt, eating scraps. The arrival of freedom comes as both liberation and bewilderment. The family moves to West Virginia where young Booker works in salt furnaces and coal mines while desperately seeking education."},
    {"roman": "II", "slug": "ch02", "title": "Boyhood Days",
     "summary": "Washington's childhood pursuit of education — learning the alphabet from a spelling book, attending school while working, adopting the surname 'Washington.' His mother's quiet determination, his first experience with a surname and a birth date, and his resolve to reach Hampton Institute."},
    {"roman": "III", "slug": "ch03", "title": "The Struggle For An Education",
     "summary": "The journey to Hampton Normal and Agricultural Institute — traveling five hundred miles with almost no money, sleeping under a sidewalk in Richmond, and arriving at Hampton penniless. His admission test: sweeping a room. Under General Armstrong's influence, Washington discovers the dignity of labor and the transforming power of practical education."},
    {"roman": "IV", "slug": "ch04", "title": "Helping Others",
     "summary": "After Hampton, Washington returns home to teach, then attends Wayland Seminary in Washington, D.C. He contrasts the practical education of Hampton with the impractical pretensions he finds in the capital. He returns to Hampton to lead the night school and teach Native American students."},
    {"roman": "V", "slug": "ch05", "title": "The Reconstruction Period",
     "summary": "Washington's assessment of Reconstruction — its mistakes and its lessons. He argues that the sudden bestowal of political power without economic preparation led to failure. A chapter that reveals both Washington's conservatism and his pragmatism."},
    {"roman": "VI", "slug": "ch06", "title": "Black Race And Red Race",
     "summary": "Washington's work with Native American students at Hampton — the parallels and differences between the two oppressed groups. He describes the challenges of educating students from the reservations and the mutual lessons learned."},
    {"roman": "VII", "slug": "ch07", "title": "Early Days At Tuskegee",
     "summary": "The founding of Tuskegee Normal and Industrial Institute in Alabama, 1881. Washington arrives to find no land, no building, no equipment — only the authorization from the state legislature. He begins teaching in a shanty and a church, with thirty students and boundless determination."},
    {"roman": "VIII", "slug": "ch08", "title": "Teaching School In A Stable And A Hen-House",
     "summary": "The early struggles of Tuskegee — acquiring land, building structures with student labor, improvising everything. Washington describes the transformation of students who learn to build the very school they attend, making bricks, farming, and constructing buildings."},
    {"roman": "IX", "slug": "ch09", "title": "Anxious Days And Sleepless Nights",
     "summary": "The financial struggles of Tuskegee — debts, mortgages, and the constant need for funds. Washington describes the anxiety of building an institution with almost no resources and the generosity of both Northern philanthropists and poor Black families."},
    {"roman": "X", "slug": "ch10", "title": "A Harder Task Than Making Bricks Without Straw",
     "summary": "Building the brickmaking industry at Tuskegee — three failed kilns before success. Washington uses brickmaking as a parable for the larger enterprise: learning through failure, the dignity of manual labor, and the creation of real economic value."},
    {"roman": "XI", "slug": "ch11", "title": "Making Their Beds Before They Could Lie On Them",
     "summary": "The expansion of Tuskegee's industrial education program — teaching students to produce what they consume, from mattresses to buildings. Washington's philosophy that education must connect mind and hand, theory and practice."},
    {"roman": "XII", "slug": "ch12", "title": "Raising Money",
     "summary": "Washington's fundraising methods and philosophy — meeting donors, giving speeches, writing appeals. He describes encounters with major philanthropists and the principle that one should earn support through demonstrated results rather than appeals to sympathy."},
    {"roman": "XIII", "slug": "ch13", "title": "Two Thousand Miles For A Five-Minute Speech",
     "summary": "The invitation to speak at the Atlanta Cotton States and International Exposition in 1895 — the opportunity that would make Washington the most prominent Black leader in America. He describes the journey, the anxiety, and the preparation."},
    {"roman": "XIV", "slug": "ch14", "title": "The Atlanta Exposition Address",
     "summary": "The most famous chapter — Washington's account of his Atlanta Compromise speech, with the full text included. 'Cast down your bucket where you are.' The speech that proposed economic cooperation between the races at the cost of social equality. Washington describes the response: acclaim from whites, acceptance from many Blacks, controversy from others."},
    {"roman": "XV", "slug": "ch15", "title": "The Secret Of Success In Public Speaking",
     "summary": "Washington's philosophy and technique of public speaking — sincerity over polish, substance over style. He describes his methods, his famous addresses, and his belief that a speaker must have something genuine to say."},
    {"roman": "XVI", "slug": "ch16", "title": "Europe",
     "summary": "Washington's trip to Europe — audiences with Queen Victoria, meetings with prominent Europeans, and observations on class and race across the Atlantic. He compares the status of Black Americans with European working classes."},
    {"roman": "XVII", "slug": "ch17", "title": "Last Words",
     "summary": "Washington's concluding chapter — reflections on race relations, the future of Tuskegee, and the philosophy of self-help and uplift that has guided his life. He calls for patience, hard work, and economic self-sufficiency as the path to racial progress."},
]


def find_chapter_boundaries(text):
    """Find the start line of each chapter, plus Preface and Introduction."""
    lines = text.split('\n')
    boundaries = []

    # Find Preface
    for i, line in enumerate(lines):
        if line.strip() == "Preface":
            boundaries.append((i, "preface", None))
            break

    # Find Introduction
    for i, line in enumerate(lines):
        if line.strip() == "Introduction":
            # Make sure it's the actual Introduction, not a TOC entry
            if i > 80:
                boundaries.append((i, "introduction", None))
                break

    # Find chapters: "Chapter I." followed by title on next line
    for ch in CHAPTERS:
        pattern = f"Chapter {ch['roman']}."
        for i, line in enumerate(lines):
            if line.strip() == pattern:
                # Verify next non-blank line matches title
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip():
                        if ch["title"].split()[0] in lines[j].strip():
                            boundaries.append((i, ch["slug"], ch))
                        break
                break

    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def extract_sections(boundaries, lines):
    """Extract text for each section."""
    sections = []
    for idx, (start_line, slug, ch_info) in enumerate(boundaries):
        content_start = start_line + 1
        # Skip header lines
        if ch_info:
            # Skip "Chapter X." and title line
            while content_start < len(lines) and not lines[content_start].strip():
                content_start += 1
            content_start += 1  # skip title line
        while content_start < len(lines) and not lines[content_start].strip():
            content_start += 1

        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][0]
        else:
            end_line = len(lines)

        text = '\n'.join(lines[content_start:end_line]).strip()
        sections.append({"slug": slug, "ch_info": ch_info, "text": text})
    return sections


def split_into_paragraphs(text):
    """Split text into paragraphs."""
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    # Remove footnote markers like "   * For this interesting..."
    text = re.sub(r'\n\s+\*\s+.*?(?=\n\n)', '', text, flags=re.DOTALL)
    raw = re.split(r'\n\s*\n', text)
    paragraphs = []
    for p in raw:
        cleaned = p.strip()
        if not cleaned:
            continue
        # Skip footnotes that start with asterisk
        if cleaned.startswith('*') and len(cleaned) < 200:
            continue
        cleaned = re.sub(r'\n\s*', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        if len(cleaned) < 15:
            continue
        paragraphs.append(cleaned)
    return paragraphs


def first_sentence_name(text, max_len=90):
    """Extract first sentence."""
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
    """Extract keywords."""
    keyword_map = {
        "slave": "slavery",
        "education": "education",
        "school": "education",
        "Hampton": "hampton",
        "Tuskegee": "tuskegee",
        "work": "labor",
        "labor": "labor",
        "industrial": "industrial-education",
        "brick": "brickmaking",
        "money": "fundraising",
        "speech": "public-speaking",
        "Atlanta": "atlanta",
        "freedom": "freedom",
        "race": "race-relations",
        "white": "race-relations",
        "church": "religion",
        "mother": "family",
        "Armstrong": "general-armstrong",
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
        "id": "theme-from-slavery-to-freedom",
        "name": "From Slavery to Freedom",
        "about": "The earliest chapters trace Washington's journey from bondage to liberation — the one-room cabin, the flax shirt, the bewildering day of emancipation. These passages describe not only the physical conditions of slavery but the psychological transformation of freedom: the sudden need for a surname, a birthdate, an identity.",
        "for_readers": "Washington's account of slavery is markedly different from Douglass's: less confrontational, more focused on what was learned from hardship. His claim that slavery was 'not, by any means, wholly bad' is one of the most contested passages in African American literature.",
        "chapter_sources": ["ch01", "ch02"],
    },
    {
        "id": "theme-education-and-self-improvement",
        "name": "Education and Self-Improvement",
        "about": "Washington's philosophy of education is the spine of the book. From Hampton's entrance exam (sweeping a room) to Tuskegee's industrial curriculum, he argues that practical education — learning to work with one's hands — is the surest path to dignity and independence. This is not merely a pedagogical theory but a philosophy of racial uplift through demonstrated competence.",
        "for_readers": "Washington's educational philosophy was enormously influential and deeply controversial. Du Bois would argue that industrial education alone was insufficient. Read these chapters to understand the case Washington made — it is more nuanced than its critics sometimes suggest.",
        "chapter_sources": ["ch03", "ch04", "ch07", "ch08", "ch10", "ch11"],
    },
    {
        "id": "theme-building-tuskegee",
        "name": "Building Tuskegee",
        "about": "The practical epic of building an institution from nothing — acquiring land, making bricks, constructing buildings, raising money. Washington presents Tuskegee as proof of his philosophy: education through labor, dignity through production, self-reliance through demonstrated achievement. Every brick laid is an argument.",
        "for_readers": "The Tuskegee chapters are Washington at his most compelling — a master storyteller describing the creation of something real. The three failed brick kilns before success is one of the great American parables of perseverance.",
        "chapter_sources": ["ch07", "ch08", "ch09", "ch10", "ch11", "ch12"],
    },
    {
        "id": "theme-atlanta-compromise",
        "name": "The Atlanta Compromise and Public Life",
        "about": "The chapters surrounding Washington's famous 1895 Atlanta Exposition Address — the speech that proposed economic cooperation between the races in exchange for social separation. 'In all things that are purely social we can be as separate as the fingers, yet one as the hand in all things essential to mutual progress.' This speech made Washington the most powerful Black leader in America and the most criticized.",
        "for_readers": "The Atlanta Address is the most famous and most debated speech in African American history. Washington presents it here as a triumph; Du Bois and others would call it a surrender. Read the full text and decide: was this pragmatic wisdom or dangerous compromise?",
        "chapter_sources": ["ch13", "ch14", "ch15"],
    },
    {
        "id": "theme-race-relations-philosophy",
        "name": "Race Relations and Washington's Philosophy",
        "about": "Washington's views on race relations — his assessment of Reconstruction, his arguments for patience and self-help, his belief that economic achievement would eventually dissolve racial barriers. He argues that Black Americans should focus on building wealth and character rather than demanding political rights. This philosophy of accommodation was both strategically shrewd and morally contested.",
        "for_readers": "Washington's racial philosophy must be understood in historical context. Writing in the nadir of American race relations, with lynching commonplace and voting rights evaporating, he chose a path of pragmatic accommodation. Whether this was wisdom or capitulation remains one of the great debates in African American thought.",
        "chapter_sources": ["ch05", "ch06", "ch16", "ch17"],
    },
]


def build_grammar():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)

    # Strip front matter up to Preface
    # The text starts with title page and dedication — we want to start at Preface
    idx = text.find("\nPreface\n")
    if idx == -1:
        idx = text.find("\nPreface\r\n")
    if idx != -1:
        text = text[idx+1:]

    boundaries, lines = find_chapter_boundaries(text)
    sections = extract_sections(boundaries, lines)

    items = []
    sort_order = 0
    chapter_item_ids = {}

    # --- L1: Paragraphs ---
    for section in sections:
        slug = section["slug"]
        ch_info = section["ch_info"]
        paragraphs = split_into_paragraphs(section["text"])
        chapter_item_ids[slug] = []

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
                "sections": {"Passage": para},
                "keywords": keywords,
                "metadata": {"paragraph_number": i + 1},
            }
            if ch_info:
                item["metadata"]["chapter"] = f"{ch_info['roman']}. {ch_info['title']}"
            items.append(item)
            chapter_item_ids[slug].append(para_id)

    # --- L2: Chapter groups ---
    for section in sections:
        slug = section["slug"]
        ch_info = section["ch_info"]
        sort_order += 1
        ids = chapter_item_ids.get(slug, [])

        if ch_info:
            title = f"{ch_info['roman']}. {ch_info['title']}"
            about = ch_info["summary"]
        elif slug == "preface":
            title = "Preface"
            about = "Washington's brief preface explaining the origin of the book — articles written for The Outlook magazine, composed on trains and in hotels between his ceaseless work for Tuskegee."
        elif slug == "introduction":
            title = "Introduction"
            about = "An introduction tracing Washington's intellectual lineage from Mark Hopkins through Samuel Armstrong to Washington himself — a chain of educational influence from Williams College through Hampton to Tuskegee."
        else:
            title = slug
            about = ""

        items.append({
            "id": f"chapter-{slug}",
            "name": title,
            "level": 2,
            "category": "chapter-group",
            "sort_order": sort_order,
            "sections": {"About": about},
            "keywords": [],
            "composite_of": ids,
            "relationship_type": "emergence",
            "metadata": {},
        })

    # --- L2: Thematic groups ---
    for tg in THEMATIC_GROUPS:
        sort_order += 1
        composite_ids = []
        for ch_slug in tg["chapter_sources"]:
            composite_ids.extend(chapter_item_ids.get(ch_slug, []))

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
    chapter_l2_ids = [f"chapter-{s['slug']}" for s in sections]
    thematic_l2_ids = [tg["id"] for tg in THEMATIC_GROUPS]

    sort_order += 1
    items.append({
        "id": "meta-arc-of-uplift",
        "name": "The Arc of Uplift",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "Up from Slavery read as Washington structured it — a rising arc from the slave cabin to the White House dinner table, from illiteracy to international renown. The narrative is deliberately shaped as a success story, an American Dream in Black: through hard work, self-improvement, and strategic accommodation, a slave-born child becomes the most powerful Black man in America. The arc is both inspiring and troubling — a story of what was gained and, critics would argue, what was conceded.",
            "For Readers": "Read in order to experience Washington's narrative strategy. The book builds from poverty to triumph, from local to national to international. Each chapter adds another layer of achievement. But notice what is left out: the violence, the political disenfranchisement, the rage. Washington's silence on these subjects is as revealing as Douglass's eloquence about them.",
        },
        "keywords": ["autobiography", "uplift", "self-help"],
        "composite_of": chapter_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    sort_order += 1
    items.append({
        "id": "meta-themes-of-uplift",
        "name": "Themes of Self-Reliance",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "Up from Slavery read thematically — the great subjects that organize Washington's vision. The journey from slavery. The philosophy of practical education. The building of Tuskegee. The Atlanta Compromise and public life. Race relations and accommodation. These themes reveal the architecture of Washington's thought: work, produce, demonstrate, and eventually the barriers will fall.",
            "For Readers": "These thematic groupings help navigate Washington's argument by subject. The education chapters explain his philosophy. The Tuskegee chapters show it in practice. The Atlanta chapters reveal its political implications. The race relations chapters expose its limitations and its logic.",
        },
        "keywords": ["themes", "self-reliance", "industrial-education"],
        "composite_of": thematic_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Booker T. Washington", "date": "1901", "note": "Author"},
                {"name": "Project Gutenberg", "date": "2000", "note": "Digital source, eBook #2376"},
            ]
        },
        "name": "Up from Slavery",
        "description": "Booker T. Washington's 'Up from Slavery: An Autobiography' (1901) — the most widely read African American autobiography of its era. Born into slavery in Virginia, Washington worked his way through Hampton Institute, founded Tuskegee Institute in Alabama, and became the most influential Black leader in America after his 1895 Atlanta Exposition Address. This autobiography is both an inspiring narrative of self-made achievement and a political document arguing for industrial education and racial accommodation — a philosophy that W. E. B. Du Bois would challenge in 'The Souls of Black Folk' two years later.\n\nSource: Project Gutenberg eBook #2376 (https://www.gutenberg.org/ebooks/2376)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs of Booker T. Washington. Images of Tuskegee Institute from its early decades. Photographs from the Atlanta Cotton States Exposition of 1895. Portraits by Frances Benjamin Johnston and other period photographers.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "autobiography", "education", "self-help", "tuskegee",
            "race-relations", "public-domain", "full-text",
            "african-american", "industrial-education"
        ],
        "roots": ["african-diaspora"],
        "shelves": ["resilience"],
        "lineages": ["Akomolafe", "Andreotti"],
        "worldview": "testimonial",
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
