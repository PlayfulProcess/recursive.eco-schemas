#!/usr/bin/env python3
"""
Parse "The Interesting Narrative of the Life of Olaudah Equiano" (Gutenberg #15399, 1789)
into a grammar.json.

Structure: 12 chapters of autobiography
- L1: Paragraphs within each chapter
- L2: Chapter groups + thematic groups
- L3: Meta-categories
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "olaudah-equiano.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "olaudah-equiano")
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
    {"num": 1, "slug": "ch01", "title": "Chapter I: Igbo Country and Customs",
     "summary": "Equiano describes his homeland in what is now Nigeria — the customs, governance, religion, and daily life of the Igbo people. He portrays a rich, orderly society with its own arts, agriculture, and justice system, establishing Africa as a place of civilization before narrating its destruction by the slave trade."},
    {"num": 2, "slug": "ch02", "title": "Chapter II: Kidnapping and the Middle Passage",
     "summary": "The most harrowing chapter — Equiano and his sister are kidnapped from their home, separated, and Equiano is carried through a succession of African households before reaching the coast. His first sight of the slave ship fills him with terror. The horrors of the Middle Passage: the stench, the chains, the floggings, the suicides, the arrival at Barbados."},
    {"num": 3, "slug": "ch03", "title": "Chapter III: Virginia and the Navy",
     "summary": "Equiano is sold to a Virginia planter, then purchased by Michael Henry Pascal, a Royal Navy lieutenant. He is renamed Gustavus Vassa, taken to England, and serves aboard warships during the Seven Years' War. He begins to learn English, encounters snow for the first time, and forms a friendship with a boy named Richard Baker."},
    {"num": 4, "slug": "ch04", "title": "Chapter IV: Baptism and Naval Service",
     "summary": "Equiano is baptized, continues his naval service, participates in battles, and develops his education. He serves on multiple ships, witnesses the siege of Louisbourg, and grows in confidence and skill — only to be betrayed when Pascal sells him back into slavery."},
    {"num": 5, "slug": "ch05", "title": "Chapter V: Return to Slavery",
     "summary": "The devastating reversal — after years of relatively free naval service, Equiano is sold to Robert King, a Quaker merchant in the West Indies. He witnesses the extreme cruelty of Caribbean slavery, describes the treatment of enslaved people, and begins trading to earn money toward his own freedom."},
    {"num": 6, "slug": "ch06", "title": "Chapter VI: Trading Toward Freedom",
     "summary": "Equiano's entrepreneurial efforts to purchase his freedom — trading goods between islands, saving every penny, navigating the constant danger of being cheated or re-enslaved. He describes the precarious existence of even free Black people in the colonial Caribbean."},
    {"num": 7, "slug": "ch07", "title": "Chapter VII: Freedom Achieved",
     "summary": "The climactic chapter — Equiano finally purchases his freedom for forty pounds sterling. The moment of manumission is both triumphant and bittersweet. He describes the immediate dangers a free Black man faces and begins his life as a free sailor and trader."},
    {"num": 8, "slug": "ch08", "title": "Chapter VIII: Life as a Free Man",
     "summary": "Equiano's early years of freedom — sailing, trading, and repeatedly facing the dangers of being kidnapped back into slavery. Despite his free papers, he is attacked, cheated, and threatened. Freedom in a slave society is precarious and constantly contested."},
    {"num": 9, "slug": "ch09", "title": "Chapter IX: Voyages and Adventures",
     "summary": "Equiano's travels as a free man — shipwrecks, near-death experiences, visits to Turkey and other Mediterranean ports. He continues to build his skills as a sailor and trader while reflecting on the injustice of slavery he witnesses everywhere."},
    {"num": 10, "slug": "ch10", "title": "Chapter X: Arctic Expedition and Conversion",
     "summary": "Equiano joins an expedition to the Arctic, seeking a passage to India. He describes the ice, the danger, and the beauty. He also undergoes a profound religious conversion to Methodism, finding in Christianity both personal salvation and a moral framework for opposing slavery."},
    {"num": 11, "slug": "ch11", "title": "Chapter XI: Further Travels and Witness",
     "summary": "Continued voyages — Equiano travels to Central America, witnesses the exploitation of the Mosquito Coast, works with Dr. Irving on a plantation scheme that fails. He continues to document the cruelties of slavery and the precariousness of Black life across the Atlantic world."},
    {"num": 12, "slug": "ch12", "title": "Chapter XII: Abolitionism and Legacy",
     "summary": "The final chapter — Equiano settles in England, becomes involved in the abolitionist movement, petitions the Queen, and publishes his Narrative. He describes his marriage to Susanna Cullen and his hope that his testimony will contribute to the abolition of the slave trade."},
]


def find_chapter_boundaries(text):
    """Find chapter boundaries: CHAPTER I. or CHAP. II. etc."""
    lines = text.split('\n')
    boundaries = []

    # Find the dedication/address to Parliament
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("To the Lords Spiritual"):
            boundaries.append((i, "dedication", None))
            break

    # Find chapters
    for ch in CHAPTERS:
        if ch["num"] == 1:
            pattern = r'^CHAPTER\s+I\.\s*$'
        else:
            roman = _to_roman(ch["num"])
            pattern = rf'^CHAP\.\s+{roman}\.?\s*$'

        for i, line in enumerate(lines):
            if re.match(pattern, line.strip()):
                boundaries.append((i, ch["slug"], ch))
                break

    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def _to_roman(n):
    """Convert integer to Roman numeral."""
    vals = [(10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    result = ''
    for val, sym in vals:
        while n >= val:
            result += sym
            n -= val
    return result


def extract_sections(boundaries, lines):
    """Extract text for each section."""
    sections = []
    for idx, (start_line, slug, ch_info) in enumerate(boundaries):
        content_start = start_line + 1
        while content_start < len(lines) and not lines[content_start].strip():
            content_start += 1

        # Skip the italic chapter summary (indented, starts with underscore)
        if ch_info:
            # Check for italic summary block
            if content_start < len(lines) and lines[content_start].strip().startswith('_'):
                # Skip until end of italic block (ends with _)
                while content_start < len(lines):
                    line = lines[content_start].strip()
                    if not line:
                        content_start += 1
                        break
                    if line.endswith('_'):
                        content_start += 1
                        break
                    content_start += 1
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
    # Remove footnotes
    text = re.sub(r'\[Footnote [A-Z].*?\]', '', text)
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    raw = re.split(r'\n\s*\n', text)
    paragraphs = []
    for p in raw:
        cleaned = p.strip()
        if not cleaned:
            continue
        # Skip subscriber lists and short formatting artifacts
        if cleaned.startswith('[') and cleaned.endswith(']'):
            continue
        # Normalize
        cleaned = re.sub(r'\n\s*', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        # Remove italic underscores
        cleaned = cleaned.replace('_', '')
        if len(cleaned) < 15:
            continue
        # Skip lines that look like lists of subscribers
        if re.match(r'^(Mr\.|Mrs\.|Miss|Rev|Dr\.|The Right)', cleaned) and len(cleaned) < 100:
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
        "Africa": "africa",
        "ship": "maritime",
        "sea": "maritime",
        "sail": "maritime",
        "freedom": "freedom",
        "free": "freedom",
        "master": "master",
        "bought": "commerce",
        "sold": "commerce",
        "trade": "commerce",
        "God": "religion",
        "Christian": "religion",
        "pray": "religion",
        "bapti": "religion",
        "cruelty": "violence",
        "whip": "violence",
        "chain": "violence",
        "kidnap": "kidnapping",
        "mother": "family",
        "sister": "family",
        "England": "england",
        "West Indies": "caribbean",
        "Barbados": "caribbean",
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
        "id": "theme-africa-and-identity",
        "name": "Africa and Igbo Identity",
        "about": "Equiano's account of his homeland — the only detailed first-person description of Igbo society from the eighteenth century. He describes governance, religion, customs, agriculture, and daily life, establishing Africa as a place of order and beauty before narrating its destruction. These passages are both ethnography and elegy: a world described because it was destroyed.",
        "for_readers": "Chapter I is one of the most valuable documents in African history — a firsthand account of pre-colonial Igbo life. Equiano writes with pride and precision about his people's customs, justice system, and spiritual beliefs. The detail is not mere nostalgia; it is evidence that Africa had sophisticated civilizations that the slave trade obliterated.",
        "chapter_sources": ["ch01"],
    },
    {
        "id": "theme-middle-passage-slavery",
        "name": "The Middle Passage and Slavery's Horrors",
        "about": "The chapters that document the machinery of slavery — kidnapping, the terrifying Middle Passage, the auction block, the plantation, the casual violence. Equiano's account of the slave ship is one of the defining texts of abolitionist literature: the stench, the chains, the women's screams, the sharks following the ship. He also documents Caribbean slavery's particular brutality.",
        "for_readers": "These passages are among the most important documents in the history of the Atlantic slave trade. Equiano writes as an eyewitness and a survivor. His account of the Middle Passage has shaped every subsequent representation of the slave trade. The Caribbean chapters reveal a world of routine torture that even hardened readers find shocking.",
        "chapter_sources": ["ch02", "ch03", "ch05"],
    },
    {
        "id": "theme-freedom-and-enterprise",
        "name": "The Pursuit of Freedom",
        "about": "Equiano's remarkable journey from slavery to freedom through sheer entrepreneurial determination. He trades goods between islands, saves money penny by penny, navigates constant danger of being cheated or re-enslaved, and finally purchases his freedom for forty pounds. These chapters are a testament to human agency within a system designed to deny it.",
        "for_readers": "The freedom chapters reveal both Equiano's extraordinary resourcefulness and the system's extraordinary cruelty. Even after purchasing his freedom, he is attacked, robbed, and threatened with re-enslavement. Freedom in a slave society was not a destination but a constant struggle.",
        "chapter_sources": ["ch06", "ch07", "ch08"],
    },
    {
        "id": "theme-faith-and-conversion",
        "name": "Faith, Conversion, and Moral Vision",
        "about": "Equiano's spiritual journey — from Igbo traditional religion through his encounter with Christianity to his Methodist conversion. Faith provides him not only with personal consolation but with a moral framework for opposing slavery. He uses Christian arguments to condemn Christian slaveholders, turning the religion of the masters against the institution they profited from.",
        "for_readers": "Equiano's religious conversion is genuine and deeply felt, but it also serves a rhetorical purpose: it establishes him as a fellow Christian addressing a Christian audience. His ability to quote scripture more convincingly than the slaveholders who claimed to follow it is one of the Narrative's most powerful weapons.",
        "chapter_sources": ["ch04", "ch10"],
    },
    {
        "id": "theme-voyages-and-witness",
        "name": "Voyages, Adventures, and Global Witness",
        "about": "Equiano as a citizen of the Atlantic world — his voyages from Africa to the Caribbean to England to the Arctic to Central America. He is shipwrecked, joins an Arctic expedition, works on a plantation scheme in Central America, and travels the Mediterranean. Throughout, he bears witness to the slave trade's reach across the entire world.",
        "for_readers": "These chapters reveal the global scale of the eighteenth-century Atlantic world. Equiano's travels take him from equator to Arctic, from Africa to Turkey. Everywhere he goes, he encounters slavery and racial prejudice — but also friendship, adventure, and beauty. His is one of the great travel narratives of the age.",
        "chapter_sources": ["ch09", "ch10", "ch11"],
    },
    {
        "id": "theme-abolition-legacy",
        "name": "Abolitionism and Legacy",
        "about": "The final movement — Equiano settles in England, becomes an abolitionist activist, petitions the Queen, and publishes the Narrative that will outlive him by centuries. His testimony is both personal and political: one man's story wielded as an argument for the abolition of the slave trade. The book itself is an act of resistance.",
        "for_readers": "The final chapter reveals the Narrative's purpose: not merely autobiography but abolitionist argument. Equiano addresses Parliament, names subscribers, and marshals his life story as evidence. The book was a bestseller in its time and a key document in the campaign that led to the abolition of the British slave trade in 1807.",
        "chapter_sources": ["ch12"],
    },
]


def build_grammar():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)

    # Remove subscriber list — find "LIST of SUBSCRIBERS" and skip to CHAPTER I
    sub_idx = text.find("LIST of SUBSCRIBERS")
    if sub_idx != -1:
        ch_idx = text.find("CHAPTER I.", sub_idx)
        if ch_idx != -1:
            # Keep everything before subscriber list and from CHAPTER I onward
            pre_sub = text[:sub_idx]
            text = pre_sub + text[ch_idx:]

    boundaries, lines = find_chapter_boundaries(text)
    sections = extract_sections(boundaries, lines)

    # Skip dedication (too short/formal)
    sections = [s for s in sections if s["slug"] != "dedication"]

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
                item["metadata"]["chapter"] = ch_info["title"]
            items.append(item)
            chapter_item_ids[slug].append(para_id)

    # --- L2: Chapter groups ---
    for ch in CHAPTERS:
        slug = ch["slug"]
        sort_order += 1
        ids = chapter_item_ids.get(slug, [])

        items.append({
            "id": f"chapter-{slug}",
            "name": ch["title"],
            "level": 2,
            "category": "chapter-group",
            "sort_order": sort_order,
            "sections": {"About": ch["summary"]},
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
    chapter_l2_ids = [f"chapter-{ch['slug']}" for ch in CHAPTERS]
    thematic_l2_ids = [tg["id"] for tg in THEMATIC_GROUPS]

    sort_order += 1
    items.append({
        "id": "meta-arc-of-testimony",
        "name": "The Arc of Testimony",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "The Interesting Narrative read as Equiano structured it — a journey from Africa through slavery, the Middle Passage, naval service, Caribbean bondage, the purchase of freedom, and finally abolitionist activism. It is autobiography as argument: every experience marshaled to prove that enslaved Africans are fully human, fully rational, and fully deserving of liberty. The arc moves from innocence through suffering to agency.",
            "For Readers": "Read in order to experience the full force of Equiano's argument. The Igbo chapters establish what was lost; the Middle Passage reveals the horror; the freedom chapters show what human agency can achieve even within an inhuman system; the final chapter reveals the purpose of the entire testimony.",
        },
        "keywords": ["autobiography", "testimony", "atlantic-world"],
        "composite_of": chapter_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    sort_order += 1
    items.append({
        "id": "meta-themes-of-the-narrative",
        "name": "Themes of the Narrative",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "The Interesting Narrative read thematically — organized by the great subjects that animate Equiano's testimony. African identity and loss. The horrors of the slave trade. The pursuit of freedom. Faith and moral vision. Global voyages. Abolitionism. These themes reveal the many dimensions of a text that is simultaneously ethnography, adventure story, spiritual autobiography, economic treatise, and political argument.",
            "For Readers": "Use these thematic groupings to explore the Narrative by subject. The Africa theme recovers a lost world. The slavery theme confronts the reader with documented horror. The freedom theme celebrates human agency. The faith theme shows how Equiano turned Christianity against the Christians who enslaved him.",
        },
        "keywords": ["themes", "testimony", "atlantic-slave-trade"],
        "composite_of": thematic_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Olaudah Equiano", "date": "1789", "note": "Author"},
                {"name": "Project Gutenberg", "date": "2005", "note": "Digital source, eBook #15399"},
            ]
        },
        "name": "The Interesting Narrative of the Life of Olaudah Equiano",
        "description": "Olaudah Equiano's 'The Interesting Narrative of the Life of Olaudah Equiano, or Gustavus Vassa, the African, Written by Himself' (1789) — one of the earliest and most influential slave narratives ever published. Born in what is now Nigeria, Equiano was kidnapped at age eleven, survived the Middle Passage, served in the Royal Navy, purchased his own freedom, and became a leading voice in the British abolitionist movement. His Narrative is at once ethnography of Igbo society, testimony of the slave trade's horrors, adventure story, spiritual autobiography, and political argument for abolition.\n\nSource: Project Gutenberg eBook #15399 (https://www.gutenberg.org/ebooks/15399)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Frontispiece portrait of Olaudah Equiano from the 1789 first edition. Illustrations of slave ships and the Middle Passage from 18th-century abolitionist publications. Maps of the Atlantic slave trade routes. Engravings from the period depicting West African life.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "autobiography", "slavery", "abolition", "middle-passage",
            "africa", "maritime", "public-domain", "full-text",
            "testimony", "igbo", "atlantic-world"
        ],
        "roots": ["african-cosmology"],
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
