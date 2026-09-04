#!/usr/bin/env python3
"""
Parse "The Souls of Black Folk" by W.E.B. Du Bois (Gutenberg #408, 1903) into a grammar.json.

Structure:
- L1: Paragraphs within each chapter (plus Forethought and Afterthought)
- L2: Chapter groups + thematic groups
- L3: Meta-categories ("The Arc of the Veil", "Themes of the Color Line")
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "souls-of-black-folk.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "souls-of-black-folk")
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
    {"roman": "I", "slug": "ch01", "title": "Of Our Spiritual Strivings",
     "summary": "Du Bois opens with the question that haunts the book: 'How does it feel to be a problem?' He introduces the concept of double consciousness — 'this sense of always looking at one's self through the eyes of others' — and traces the spiritual strivings of Black Americans from slavery through Emancipation to the present."},
    {"roman": "II", "slug": "ch02", "title": "Of the Dawn of Freedom",
     "summary": "A history of the Freedmen's Bureau — the federal agency created to manage the transition from slavery to freedom. Du Bois examines its achievements and failures, showing how the promise of Emancipation was compromised by political expediency and the endurance of racial caste."},
    {"roman": "III", "slug": "ch03", "title": "Of Mr. Booker T. Washington and Others",
     "summary": "Du Bois's measured but devastating critique of Booker T. Washington's program of industrial education and political accommodation. He argues that Washington's compromise — accepting disenfranchisement and social inequality in exchange for economic opportunity — has failed on its own terms and surrendered essential rights."},
    {"roman": "IV", "slug": "ch04", "title": "Of the Meaning of Progress",
     "summary": "Du Bois returns to the rural Tennessee community where he taught school as a young man. A deeply personal chapter that reveals the gap between the hope of education and the grinding reality of Black rural life. When he returns years later, he finds progress has been uneven and fragile."},
    {"roman": "V", "slug": "ch05", "title": "Of the Wings of Atalanta",
     "summary": "Using the myth of Atalanta who was tempted by golden apples, Du Bois warns that the South's pursuit of material wealth threatens to corrupt the higher aims of education. He argues for the university ideal — the training of minds, not just hands."},
    {"roman": "VI", "slug": "ch06", "title": "Of the Training of Black Men",
     "summary": "A direct argument for higher education for Black Americans, against the prevailing emphasis on industrial training alone. Du Bois presents data on Black college graduates and argues that the 'Talented Tenth' must be educated to lead."},
    {"roman": "VII", "slug": "ch07", "title": "Of the Black Belt",
     "summary": "A sociological journey through the Black Belt of Georgia — the cotton country where the majority of Black Southerners live. Du Bois describes the landscape, the tenant farming system, the country stores, and the persistent poverty that slavery left behind."},
    {"roman": "VIII", "slug": "ch08", "title": "Of the Quest of the Golden Fleece",
     "summary": "An economic analysis of the cotton economy and its human cost. Du Bois traces how the crop-lien system and tenant farming created a new form of bondage, trapping Black farmers in cycles of debt and dependency."},
    {"roman": "IX", "slug": "ch09", "title": "Of the Sons of Master and Man",
     "summary": "An analysis of race relations in the post-Reconstruction South — the points of contact and separation between Black and white communities. Du Bois examines the legal system, economic life, and social intercourse across the color line."},
    {"roman": "X", "slug": "ch10", "title": "Of the Faith of the Fathers",
     "summary": "A study of the Black church — its origins in African religion, its transformation under slavery, and its central role in Black community life. Du Bois identifies three attitudes among Black Americans: revolt, submission, and compromise."},
    {"roman": "XI", "slug": "ch11", "title": "Of the Passing of the First-Born",
     "summary": "The most intimate chapter — Du Bois's elegy for his infant son Burghardt, who died in Atlanta. A meditation on love, loss, and the bitter knowledge that his son has escaped the Veil: 'Not dead, not dead, but escaped; not bond, but free.'"},
    {"roman": "XII", "slug": "ch12", "title": "Of Alexander Crummell",
     "summary": "A biographical sketch of Alexander Crummell — the Black Episcopal priest and intellectual who overcame rejection, exile, and despair to dedicate his life to the uplift of his people. Du Bois presents him as a model of spiritual persistence."},
    {"roman": "XIII", "slug": "ch13", "title": "Of the Coming of John",
     "summary": "A short story — the tale of John Jones, a young Black man who goes North to college and returns to his Georgia hometown transformed. His new consciousness makes him unfit for the old world, leading to tragedy. Du Bois's most powerful fiction."},
    {"roman": "XIV", "slug": "ch14", "title": "Of the Sorrow Songs",
     "summary": "The final essay — a study of the spirituals ('Sorrow Songs') as the most original and beautiful expression of American music. Du Bois traces their African roots, their transformation under slavery, and their enduring message of hope, sorrow, and faith."},
]


def find_chapter_boundaries(text):
    """Find the start line of each chapter, plus Forethought and Afterthought."""
    lines = text.split('\n')
    boundaries = []

    # Find Forethought
    for i, line in enumerate(lines):
        if line.strip() == "The Forethought":
            boundaries.append((i, "forethought", None))
            break

    # Find chapters: pattern is a line with just the roman numeral, followed by the title
    for ch in CHAPTERS:
        pattern = f"{ch['roman']}."
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == pattern:
                # Verify next non-blank line is the chapter title
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip():
                        if ch["title"].split()[0] in lines[j].strip():
                            boundaries.append((i, ch["slug"], ch))
                        break
                else:
                    boundaries.append((i, ch["slug"], ch))
                break

    # Find Afterthought
    for i, line in enumerate(lines):
        if line.strip() == "The Afterthought":
            boundaries.append((i, "afterthought", None))
            break

    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def extract_sections(boundaries, lines):
    """Extract text for each section between boundaries."""
    sections = []
    for idx, (start_line, slug, ch_info) in enumerate(boundaries):
        # Skip header line(s) and find content start
        content_start = start_line + 1
        # For chapters, skip roman numeral line and title line
        if ch_info:
            # Skip blank lines and title line
            while content_start < len(lines) and not lines[content_start].strip():
                content_start += 1
            # Skip the title line itself
            content_start += 1

        while content_start < len(lines) and not lines[content_start].strip():
            content_start += 1

        # End at next boundary or end of text
        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][0]
        else:
            end_line = len(lines)

        section_text = '\n'.join(lines[content_start:end_line]).strip()
        sections.append({
            "slug": slug,
            "ch_info": ch_info,
            "text": section_text,
        })
    return sections


def split_into_paragraphs(text):
    """Split text into paragraphs (separated by blank lines).
    Strip epigraph poetry at the start of chapters."""
    # Remove [Illustration] markers
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)

    raw_paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = []
    # Track whether we've passed the epigraph
    past_epigraph = False

    for p in raw_paragraphs:
        cleaned = p.strip()
        if not cleaned:
            continue

        # Skip epigraph lines (poetry/attribution at start of chapter)
        # Epigraphs tend to have indented lines or be short attributions
        if not past_epigraph:
            lines = cleaned.split('\n')
            # Check if all lines are indented (poetry) or very short (attribution)
            all_indented = all(line.startswith('    ') or line.startswith('\t') or not line.strip() for line in lines)
            is_attribution = len(cleaned) < 100 and (cleaned.isupper() or cleaned.startswith('—') or cleaned.startswith('ARTHUR') or cleaned.startswith('SWINBURNE') or cleaned.endswith('.') and len(lines) == 1 and len(cleaned.split()) < 6)

            if all_indented or is_attribution:
                continue
            past_epigraph = True

        # Normalize internal whitespace
        cleaned = re.sub(r'\n\s*', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        if len(cleaned) < 15:
            continue
        paragraphs.append(cleaned)
    return paragraphs


def first_sentence_name(text, max_len=90):
    """Extract first sentence or clause, truncated to max_len chars."""
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
    """Extract relevant keywords from paragraph content."""
    keyword_map = {
        "veil": "the-veil",
        "color line": "color-line",
        "color-line": "color-line",
        "double consciousness": "double-consciousness",
        "soul": "soul",
        "freedom": "freedom",
        "emancipation": "emancipation",
        "slave": "slavery",
        "education": "education",
        "school": "education",
        "university": "education",
        "church": "religion",
        "religion": "religion",
        "pray": "religion",
        "God": "religion",
        "sorrow": "sorrow",
        "song": "music",
        "sing": "music",
        "cotton": "economy",
        "labor": "labor",
        "land": "land",
        "tenant": "tenant-farming",
        "Washington": "booker-t-washington",
        "Negro": "negro",
        "race": "race",
        "white": "race-relations",
        "Jim Crow": "jim-crow",
        "justice": "justice",
        "death": "death",
        "child": "family",
        "mother": "family",
        "father": "family",
    }
    para_lower = para.lower()
    seen = set()
    keywords = []
    for trigger, kw in keyword_map.items():
        if trigger.lower() in para_lower and kw not in seen:
            keywords.append(kw)
            seen.add(kw)
    return keywords


# Thematic groups
THEMATIC_GROUPS = [
    {
        "id": "theme-double-consciousness",
        "name": "Double Consciousness and the Veil",
        "about": "The passages that develop Du Bois's most enduring concepts: the Veil that separates Black and white America, and the 'double consciousness' that forces Black Americans to see themselves through the eyes of a contemptuous other world. These are not merely metaphors but descriptions of a lived psychological reality — the sense of 'two-ness,' of being both American and Black, of belonging and exile at once.",
        "for_readers": "Du Bois's concept of double consciousness has become one of the most cited ideas in American thought. Trace how the Veil appears across these chapters — sometimes as barrier, sometimes as gift (seeing what others cannot), sometimes as curse. The tension between these uses is deliberate.",
        "chapter_sources": ["ch01", "ch09", "ch14"],
    },
    {
        "id": "theme-education-debate",
        "name": "The Education Debate",
        "about": "The great argument of the book: what kind of education will uplift the race? Du Bois challenges Booker T. Washington's emphasis on industrial training, arguing for the university ideal — the Talented Tenth trained in the liberal arts to lead. This is not mere academic politics; it is a debate about whether Black Americans will be trained as workers or educated as thinkers and citizens.",
        "for_readers": "The Washington-Du Bois debate shaped African American thought for generations. Du Bois does not reject industrial education — he insists that it is insufficient without higher learning. The myth of Atalanta (Chapter V) is his allegory: do not trade wisdom for gold.",
        "chapter_sources": ["ch03", "ch05", "ch06"],
    },
    {
        "id": "theme-black-belt-economy",
        "name": "The Black Belt and Its Economy",
        "about": "Du Bois the sociologist takes the reader on a journey through the cotton country of Georgia — the Black Belt where most African Americans lived. These chapters are empirical, detailed, and devastating: the tenant farming system, the crop-lien economy, the country stores that kept farmers in perpetual debt. Slavery ended, but a new form of economic bondage replaced it.",
        "for_readers": "These are the most data-driven chapters of the book. Du Bois uses statistics, landscape description, and individual portraits to build an argument that the post-slavery economy was designed to maintain racial subordination. The 'Golden Fleece' is cotton — and like Jason's quest, its pursuit destroys those who seek it.",
        "chapter_sources": ["ch04", "ch07", "ch08"],
    },
    {
        "id": "theme-spirit-and-sorrow",
        "name": "Spirit, Sorrow, and Song",
        "about": "The spiritual dimension of the book — the Black church, the Sorrow Songs, the personal grief of losing a child, the faith that sustained a people through centuries of oppression. Du Bois was not conventionally religious, but he understood the centrality of spiritual life to Black culture and gave it his most lyrical prose.",
        "for_readers": "These chapters move from sociology to poetry. The death of Du Bois's son (Chapter XI) is the most personal passage in the book; the Sorrow Songs (Chapter XIV) are its musical culmination. Together they reveal what statistics cannot: the inner life of a people behind the Veil.",
        "chapter_sources": ["ch10", "ch11", "ch14"],
    },
    {
        "id": "theme-portraits-and-stories",
        "name": "Portraits and Stories",
        "about": "Du Bois as portraitist and storyteller — the biographical sketch of Alexander Crummell, the tragic fiction of John Jones, the memoir of teaching in rural Tennessee. These chapters show Du Bois working in intimate, narrative modes rather than argument or analysis. Individual lives become windows into the larger condition.",
        "for_readers": "The Coming of John (Chapter XIII) is one of the great American short stories, though it is rarely anthologized as such. Crummell's biography (Chapter XII) is a study in spiritual persistence. The Meaning of Progress (Chapter IV) is autobiography as social document. In each, Du Bois lets a single life carry the weight of the whole.",
        "chapter_sources": ["ch04", "ch12", "ch13"],
    },
]


def build_grammar():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)

    boundaries, lines = find_chapter_boundaries(text)
    sections = extract_sections(boundaries, lines)

    items = []
    sort_order = 0
    chapter_item_ids = {}  # slug -> list of L1 item ids

    # --- L1: Paragraphs within each section ---
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
                "sections": {
                    "Passage": para,
                },
                "keywords": keywords,
                "metadata": {
                    "paragraph_number": i + 1,
                },
            }

            if ch_info:
                item["metadata"]["chapter"] = f"{ch_info['roman']}. {ch_info['title']}"

            items.append(item)
            chapter_item_ids[slug].append(para_id)

    # --- L2: Chapter emergence groups ---
    chapter_abouts = {}
    for ch in CHAPTERS:
        chapter_abouts[ch["slug"]] = ch["summary"]

    for section in sections:
        slug = section["slug"]
        ch_info = section["ch_info"]
        sort_order += 1
        ids = chapter_item_ids.get(slug, [])

        if ch_info:
            title = f"{ch_info['roman']}. {ch_info['title']}"
            about = chapter_abouts.get(slug, f"Chapter {ch_info['roman']}")
        elif slug == "forethought":
            title = "The Forethought"
            about = "Du Bois's preface to The Souls of Black Folk — a map of the book's terrain. He announces the central thesis ('the problem of the Twentieth Century is the problem of the color line'), describes the structure of the fourteen chapters, and acknowledges that before each chapter stands 'a bar of the Sorrow Songs — some echo of haunting melody from the only American music which welled up from black souls in the dark past.'"
        elif slug == "afterthought":
            title = "The Afterthought"
            about = "Du Bois's brief closing meditation — a prayer and a hope addressed to the reader who has journeyed through the book. He asks that his words be received 'not as a curse but a sign of the spirit's longing.'"
        else:
            title = slug
            about = ""

        item = {
            "id": f"chapter-{slug}",
            "name": title,
            "level": 2,
            "category": "chapter-group",
            "sort_order": sort_order,
            "sections": {
                "About": about,
            },
            "keywords": [],
            "composite_of": ids,
            "relationship_type": "emergence",
            "metadata": {},
        }
        items.append(item)

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
        "id": "meta-arc-of-the-veil",
        "name": "The Arc of the Veil",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "The Souls of Black Folk read as Du Bois structured it — a journey that begins with the personal revelation of double consciousness, moves through history and political argument, descends into the empirical reality of the Black Belt, and emerges into the spiritual realms of religion, grief, biography, fiction, and music. The book's arc is both intellectual and emotional: it asks the reader to think, then to feel, then to think again with feeling. The Forethought announces the problem of the color line; the Afterthought releases the reader back into the world, changed.",
            "For Readers": "Read the chapters in order at least once. Du Bois placed them with care: the personal opens to the political, the political to the economic, the economic to the spiritual. The Sorrow Songs at each chapter's head are not decoration — they are the other voice of the book, the musical counterpart to the prose argument.",
        },
        "keywords": ["autobiography", "sociology", "the-veil", "chronology"],
        "composite_of": chapter_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    sort_order += 1
    items.append({
        "id": "meta-themes-of-the-color-line",
        "name": "Themes of the Color Line",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "The Souls of Black Folk read thematically — organized by the great subjects that animate Du Bois's vision. Double consciousness and the Veil. The education debate. The economics of racial subordination. The spiritual life behind the Veil. Individual portraits and stories. These themes cut across the book's fourteen chapters, revealing how the same problem — the color line — manifests in psychology, politics, economics, religion, and art.",
            "For Readers": "Use these thematic groupings to explore the book by subject. The education debate gathers the chapters that argue with Washington. The Black Belt sections provide the empirical foundation. Spirit and Sorrow trace the book's emotional and musical dimension. Each theme is a different lens on the same central reality.",
        },
        "keywords": ["themes", "color-line", "double-consciousness"],
        "composite_of": thematic_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    # --- Build the grammar ---
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "W. E. B. Du Bois", "date": "1903", "note": "Author"},
                {"name": "Project Gutenberg", "date": "1996", "note": "Digital source, eBook #408"},
            ]
        },
        "name": "The Souls of Black Folk",
        "description": "W. E. B. Du Bois's 'The Souls of Black Folk' (1903) — the book that defined the African American intellectual tradition. In fourteen essays that blend sociology, history, memoir, fiction, and music criticism, Du Bois introduced the concepts of 'the Veil' and 'double consciousness,' challenged Booker T. Washington's program of accommodation, documented the economic realities of the Black Belt, and elevated the Sorrow Songs to their rightful place as America's greatest musical achievement. 'The problem of the Twentieth Century is the problem of the color line.'\n\nSource: Project Gutenberg eBook #408 (https://www.gutenberg.org/ebooks/408)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs of W. E. B. Du Bois. Illustrations from the 1903 first edition published by A. C. McClurg & Co., Chicago. Photographs of Black Belt Georgia by Du Bois and others from the 1900 Paris Exposition display. Sheet music and notation of the Sorrow Songs.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "sociology", "race", "double-consciousness", "the-veil",
            "education", "music", "memoir", "public-domain", "full-text",
            "american-literature", "social-justice", "african-american"
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
