#!/usr/bin/env python3
"""
Parse "The Negro" by W.E.B. Du Bois (Gutenberg #15359, 1915) into a grammar.json.

Structure: 12 chapters of historical essay + Preface + Suggestions for Further Reading
- L1: Paragraphs within each chapter
- L2: Chapter groups + thematic groups
- L3: Meta-categories
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "the-negro.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "the-negro")
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
    {"roman": "I", "marker": "I AFRICA", "slug": "ch01-africa", "title": "Africa",
     "summary": "An overview of the African continent — its geography, peoples, and the deep roots of human civilization on African soil. Du Bois challenges the prevailing view of Africa as a 'dark continent' by revealing its ancient complexity."},
    {"roman": "II", "marker": "II THE COMING OF BLACK MEN", "slug": "ch02-coming-black-men",
     "title": "The Coming of Black Men",
     "summary": "The earliest history of Black peoples — their migrations across Africa and the ancient mixing of races. Du Bois traces the racial diversity within Africa and challenges simplistic racial classifications."},
    {"roman": "III", "marker": "III ETHIOPIA AND EGYPT", "slug": "ch03-ethiopia-egypt",
     "title": "Ethiopia and Egypt",
     "summary": "The great civilizations of ancient Africa — Ethiopia (Kush, Meroe) and Egypt. Du Bois argues that these civilizations were substantially African and Black, challenging the prevailing scholarly erasure of African contributions to classical civilization."},
    {"roman": "IV", "marker": "IV THE NIGER AND ISLAM", "slug": "ch04-niger-islam",
     "title": "The Niger and Islam",
     "summary": "The West African empires — Ghana, Mali, Songhay — and the influence of Islam on African civilization. Du Bois describes the universities of Timbuktu, the wealth of Mansa Musa, and the sophisticated political systems of the Western Sudan."},
    {"roman": "V", "marker": "V GUINEA AND CONGO", "slug": "ch05-guinea-congo",
     "title": "Guinea and Congo",
     "summary": "The civilizations of the Guinea coast and the Congo basin — the Ashanti, the Dahomey, the Kongo kingdom. Du Bois describes the sophisticated political and artistic achievements of these societies before European contact."},
    {"roman": "VI", "marker": "VI THE GREAT LAKES AND ZYMBABWE", "slug": "ch06-great-lakes",
     "title": "The Great Lakes and Zymbabwe",
     "summary": "The kingdoms of the African Great Lakes region and the mystery of Great Zimbabwe. Du Bois describes the Buganda, the Ruanda, and other kingdoms, and argues for the African origin of the Zimbabwe ruins."},
    {"roman": "VII", "marker": "VII THE WAR OF RACES AT LAND'S END", "slug": "ch07-war-races",
     "title": "The War of Races at Land's End",
     "summary": "South Africa — the collision of European settlers, Bantu peoples, and Khoisan communities. Du Bois traces the history of racial conflict from the earliest European arrival through the Zulu wars and the beginnings of apartheid."},
    {"roman": "VIII", "marker": "VIII AFRICAN CULTURE", "slug": "ch08-african-culture",
     "title": "African Culture",
     "summary": "A comprehensive survey of African cultural achievements — art, music, religion, social organization, metallurgy, and agriculture. Du Bois argues that African civilization was rich, complex, and influential long before European contact."},
    {"roman": "IX", "marker": "IX THE TRADE IN MEN", "slug": "ch09-trade-men",
     "title": "The Trade in Men",
     "summary": "The Atlantic slave trade — its origins, its scale, its devastating impact on African societies. Du Bois connects the trade to European capitalism and imperialism, showing how the theft of African labor fueled the Industrial Revolution."},
    {"roman": "X", "marker": "X THE WEST INDIES AND LATIN AMERICA", "slug": "ch10-west-indies",
     "title": "The West Indies and Latin America",
     "summary": "The African diaspora in the Caribbean and Latin America — Haiti's revolution, Jamaica's Maroons, Brazil's Afro-Brazilian culture. Du Bois traces the continuing influence of African people and culture in the Western Hemisphere."},
    {"roman": "XI", "marker": "XI THE NEGRO IN THE UNITED STATES", "slug": "ch11-negro-us",
     "title": "The Negro in the United States",
     "summary": "The history of Black Americans from slavery through Reconstruction to the present. Du Bois traces the economic exploitation, political disenfranchisement, and cultural achievements of African Americans."},
    {"roman": "XII", "marker": "XII THE NEGRO PROBLEMS", "slug": "ch12-negro-problems",
     "title": "The Negro Problems",
     "summary": "Du Bois's concluding analysis — the global 'Negro problem' as a problem of colonialism, capitalism, and white supremacy. He argues for self-determination, education, and international solidarity among darker peoples."},
]


def find_chapter_boundaries(text):
    """Find chapter boundaries using the chapter heading format."""
    lines = text.split('\n')
    boundaries = []

    # Find Preface
    for i, line in enumerate(lines):
        if line.strip() == "PREFACE":
            boundaries.append((i, "preface", None))
            break

    # Find chapters: "I AFRICA" etc.
    for ch in CHAPTERS:
        marker = ch["marker"]
        for i, line in enumerate(lines):
            if line.strip() == marker:
                boundaries.append((i, ch["slug"], ch))
                break

    # Find Suggestions for Further Reading
    for i, line in enumerate(lines):
        if "Suggestions for Further Reading" in line.strip() or "SUGGESTIONS FOR FURTHER READING" in line.strip():
            boundaries.append((i, "bibliography", None))
            break

    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def extract_sections(boundaries, lines):
    """Extract text for each section."""
    sections = []
    for idx, (start_line, slug, ch_info) in enumerate(boundaries):
        content_start = start_line + 1
        while content_start < len(lines) and not lines[content_start].strip():
            content_start += 1

        # Skip epigraph for chapters (indented poetry)
        if ch_info:
            # Check if first content is an epigraph (starts with quote mark or indented)
            temp_start = content_start
            while temp_start < len(lines):
                line = lines[temp_start]
                stripped = line.strip()
                if not stripped:
                    temp_start += 1
                    continue
                # If line starts with quote/poetry markers or is indented, skip block
                if line.startswith('    ') or line.startswith('"') and len(stripped) < 100:
                    # Skip until blank line
                    while temp_start < len(lines) and lines[temp_start].strip():
                        temp_start += 1
                    while temp_start < len(lines) and not lines[temp_start].strip():
                        temp_start += 1
                    # Check for attribution line (e.g., "MILLER")
                    if temp_start < len(lines) and lines[temp_start].strip().isupper() and len(lines[temp_start].strip()) < 40:
                        temp_start += 1
                        while temp_start < len(lines) and not lines[temp_start].strip():
                            temp_start += 1
                    content_start = temp_start
                break

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
    text = re.sub(r'\[Transcriber\'s Notes[^\]]*\]', '', text, flags=re.DOTALL)
    raw = re.split(r'\n\s*\n', text)
    paragraphs = []
    for p in raw:
        cleaned = p.strip()
        if not cleaned:
            continue
        # Skip illustration references and map references
        if cleaned.startswith('[') and cleaned.endswith(']'):
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
        "Africa": "africa",
        "Egypt": "egypt",
        "Ethiopia": "ethiopia",
        "slave": "slavery",
        "trade": "slave-trade",
        "Islam": "islam",
        "Congo": "congo",
        "Haiti": "haiti",
        "Negro": "negro",
        "race": "race",
        "civilization": "civilization",
        "culture": "culture",
        "iron": "metallurgy",
        "art": "art",
        "empire": "empire",
        "colonial": "colonialism",
        "European": "europe",
        "America": "americas",
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
        "id": "theme-ancient-africa",
        "name": "Ancient African Civilizations",
        "about": "The chapters that recover Africa's ancient grandeur — Ethiopia and Egypt as African civilizations, the Great Zimbabwe, the kingdoms of the Great Lakes. Du Bois marshals archaeological and historical evidence to demolish the myth of Africa as a continent without history, arguing that some of humanity's greatest achievements originated on African soil.",
        "for_readers": "Du Bois wrote in 1915, when mainstream scholarship denied Africa any civilizational achievement. His claims about Egyptian and Ethiopian civilization, once dismissed, have been substantially vindicated by subsequent archaeology. These chapters are both history and polemic — a Black scholar insisting on a past that the white academy refused to see.",
        "chapter_sources": ["ch01-africa", "ch02-coming-black-men", "ch03-ethiopia-egypt", "ch06-great-lakes"],
    },
    {
        "id": "theme-african-kingdoms",
        "name": "Medieval African Kingdoms and Culture",
        "about": "The great states of medieval Africa — the empires of the Western Sudan (Ghana, Mali, Songhay), the kingdoms of Guinea and Congo, and the rich cultural traditions of the continent. Du Bois describes Timbuktu's universities, Benin's bronze art, and the political sophistication of African states that rivaled their European contemporaries.",
        "for_readers": "These chapters describe African civilizations that most Western education still ignores. The wealth of Mansa Musa, the libraries of Timbuktu, the art of Ife and Benin — Du Bois was among the first scholars to present these achievements to a general audience.",
        "chapter_sources": ["ch04-niger-islam", "ch05-guinea-congo", "ch07-war-races", "ch08-african-culture"],
    },
    {
        "id": "theme-slave-trade-diaspora",
        "name": "The Slave Trade and African Diaspora",
        "about": "The catastrophic chapters — the Atlantic slave trade and its aftermath across the Americas. Du Bois traces how European capitalism destroyed African societies, transported millions into bondage, and created the African diaspora in the Caribbean, Latin America, and the United States. Haiti's revolution stands as the great counter-narrative: enslaved people who freed themselves and founded a nation.",
        "for_readers": "Du Bois connects the slave trade to capitalism and colonialism in ways that anticipate modern scholarship by decades. His account of Haiti's revolution is particularly significant — written at a time when the U.S. was occupying Haiti and suppressing its history of Black self-liberation.",
        "chapter_sources": ["ch09-trade-men", "ch10-west-indies"],
    },
    {
        "id": "theme-negro-america-future",
        "name": "The Negro in America and the Future",
        "about": "The concluding chapters that bring the global story to America and forward to the present. Du Bois traces Black American history from slavery through Reconstruction and argues that the 'Negro problem' is fundamentally a problem of colonial capitalism and white supremacy — not of Black deficiency. He calls for education, self-determination, and global solidarity.",
        "for_readers": "The final chapters connect Africa's history to the present condition of Black Americans. Du Bois's argument that racism is a function of economic exploitation, not inherent prejudice, remains foundational to critical race theory.",
        "chapter_sources": ["ch11-negro-us", "ch12-negro-problems"],
    },
]


def build_grammar():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)

    # Remove front matter: production credits, title page, etc.
    # Find PREFACE
    preface_idx = text.find("PREFACE")
    if preface_idx != -1:
        text = text[preface_idx:]

    boundaries, lines = find_chapter_boundaries(text)
    sections = extract_sections(boundaries, lines)

    # Skip bibliography section
    sections = [s for s in sections if s["slug"] != "bibliography"]

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
            about = "Du Bois's preface acknowledging the difficulties of writing African history in 1915 — archaeological research barely begun, sources in many languages unavailable, and racial prejudice distorting scholarship. He offers this 'short general statement' as a beginning, not a conclusion."
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
        "id": "meta-arc-of-african-history",
        "name": "The Arc of African History",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "The Negro read as Du Bois structured it — a sweeping chronological arc from the geography of Africa through ancient civilizations, medieval kingdoms, the catastrophe of the slave trade, and the modern condition of the African diaspora. Du Bois tells the story of a people across millennia and continents, insisting that African history is world history.",
            "For Readers": "Read in order to experience the full scope of Du Bois's vision. The book begins in deep time and ends in the present. Each chapter builds on the last, creating a narrative of civilization, catastrophe, and resilience.",
        },
        "keywords": ["african-history", "civilization", "chronology"],
        "composite_of": chapter_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    sort_order += 1
    items.append({
        "id": "meta-themes-of-the-negro",
        "name": "Themes of The Negro",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "The Negro read thematically — ancient civilizations, medieval kingdoms, the slave trade and diaspora, and the modern condition. These themes reveal Du Bois's argument: that Africa was a continent of great achievement before European contact, that the slave trade was a catastrophe of global capitalism, and that the 'Negro problem' is a problem created by white supremacy, not by Black deficiency.",
            "For Readers": "Use these groupings to explore by subject. Ancient Africa gathers the civilizational arguments. Medieval Africa shows the continuing achievement. The slave trade chapters connect exploitation to capitalism. The modern chapters bring the story to the present.",
        },
        "keywords": ["themes", "african-history", "pan-africanism"],
        "composite_of": thematic_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "W. E. B. Du Bois", "date": "1915", "note": "Author"},
                {"name": "Project Gutenberg", "date": "2005", "note": "Digital source, eBook #15359"},
            ]
        },
        "name": "The Negro",
        "description": "W. E. B. Du Bois's 'The Negro' (1915) — one of the first comprehensive histories of African peoples written by a Black scholar. In twelve chapters, Du Bois traces the history of Black civilizations from ancient Egypt and Ethiopia through the great kingdoms of West and Central Africa, through the catastrophe of the Atlantic slave trade, to the modern diaspora in the Americas. Written at a time when mainstream scholarship denied Africa any civilizational achievement, this book was a revolutionary act of intellectual recovery.\n\nSource: Project Gutenberg eBook #15359 (https://www.gutenberg.org/ebooks/15359)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Maps from the 1915 first edition published by Henry Holt and Company. Photographs from Du Bois's research. Illustrations of African art, architecture, and artifacts from early 20th century ethnographic collections.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "african-history", "civilization", "pan-africanism",
            "slavery", "colonialism", "public-domain", "full-text",
            "history", "sociology", "race"
        ],
        "roots": ["african-cosmology"],
        "shelves": ["mirror"],
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
