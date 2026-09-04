#!/usr/bin/env python3
"""
Parse "Narrative of the Life of Frederick Douglass, an American Slave" (Gutenberg #23, 1845)
into a grammar.json.

Structure:
- L1: Paragraphs within each chapter (plus Appendix and Parody)
- L2: Chapter emergence groups + thematic groups (bondage, education, resistance, freedom, identity)
- L3: Meta-categories ("The Arc of Liberation", "Themes of Witness")
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "frederick-douglass.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "frederick-douglass")
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


def strip_front_matter(text):
    """Remove title page, table of contents, Preface (Garrison), Letter (Phillips),
    and the biographical note — keep only Douglass's own narrative starting at CHAPTER I."""
    lines = text.split('\n')
    # Find the actual CHAPTER I line (not the TOC entry — the TOC entries are indented)
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Match "CHAPTER I" as the actual chapter heading (not indented TOC)
        if stripped == "CHAPTER I" and not line.startswith("  "):
            # Check it's the real heading, not TOC: real heading appears after the front matter
            # TOC appears around line 60-75; real Chapter I is much later
            if i > 100:  # well past the TOC
                return '\n'.join(lines[i:])
    # Fallback: find last occurrence of "CHAPTER I"
    last_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "CHAPTER I":
            last_idx = i
    if last_idx:
        return '\n'.join(lines[last_idx:])
    return text


# Chapter definitions
CHAPTERS = [
    {"num": "I", "slug": "ch01", "title": "Chapter I: Birth, Family, and the Blood-Stained Gate",
     "summary": "Douglass recounts his birth in Tuckahoe, Maryland, his uncertain age, separation from his mother, the whispered identity of his white father, and the horrifying first witness of Aunt Hester's whipping — 'the blood-stained gate, the entrance to the hell of slavery.'"},
    {"num": "II", "slug": "ch02", "title": "Chapter II: The Great House Farm",
     "summary": "Life on Colonel Lloyd's plantation — the Great House Farm as the center of the slaveholding world, the slave songs that carried hidden sorrow, the hierarchy among slaves, and the elaborate provisions for the master's table."},
    {"num": "III", "slug": "ch03", "title": "Chapter III: Colonel Lloyd's Domain",
     "summary": "The vast wealth and power of Colonel Lloyd — his garden, stables, and the constant dread among slaves. Douglass reveals how slaves were punished for telling the truth about their conditions, teaching them that honesty was dangerous."},
    {"num": "IV", "slug": "ch04", "title": "Chapter IV: The Murder of Demby",
     "summary": "The reign of overseer Austin Gore, a man 'equal to deceiving the most practiced,' and his cold-blooded murder of a slave named Demby who refused to come out of a creek during a whipping. The killing went unpunished — 'killing a slave, or any colored person, was not treated as a crime.'"},
    {"num": "V", "slug": "ch05", "title": "Chapter V: Leaving the Plantation",
     "summary": "Douglass's childhood on the plantation — hunger, cold, the coarse linen shirt his only garment. Then the miraculous news: he is to be sent to Baltimore. He scrubs himself clean with hope, sensing this departure will shape his destiny."},
    {"num": "VI", "slug": "ch06", "title": "Chapter VI: Mrs. Auld and the Alphabet",
     "summary": "In Baltimore, Sophia Auld begins teaching Douglass his letters — until her husband forbids it, declaring that learning would make a slave 'unfit' and 'discontented.' This prohibition becomes Douglass's revelation: 'I now understood what had been to me a most perplexing difficulty — the white man's power to enslave the black man.'"},
    {"num": "VII", "slug": "ch07", "title": "Chapter VII: Learning to Read and Write",
     "summary": "Douglass's determined self-education — trading bread for reading lessons from white boys, discovering The Columbian Orator, learning the word 'abolition.' Reading awakens consciousness but also torment: 'I would at times feel that learning to read had been a curse rather than a blessing.'"},
    {"num": "VIII", "slug": "ch08", "title": "Chapter VIII: The Valuation",
     "summary": "After old Master Anthony's death, Douglass is sent back to be valued alongside livestock. 'Men and women, old and young, married and single, were ranked with horses, sheep, and swine.' He narrowly avoids being sent to the cruel Andrew and returns to Baltimore."},
    {"num": "IX", "slug": "ch09", "title": "Chapter IX: Master Thomas and Religious Hypocrisy",
     "summary": "Life with Thomas Auld at St. Michael's — a master who uses religion to justify cruelty. Auld's conversion makes him worse, not better. Douglass exposes the savage irony of Christian slaveholders who quote scripture while starving and whipping their slaves."},
    {"num": "X", "slug": "ch10", "title": "Chapter X: Covey, the Turning Point, and the Fight for Freedom",
     "summary": "The longest and most dramatic chapter. Douglass is 'broken' by the slave-breaker Edward Covey, then rises up to fight him in a pivotal two-hour battle. 'This battle was the turning-point in my career as a slave. It rekindled the few expiring embers of freedom.' Later, a failed escape attempt, then time with the kind Mr. Freeland before being sent back to Baltimore."},
    {"num": "XI", "slug": "ch11", "title": "Chapter XI: Escape and Freedom",
     "summary": "Douglass's final chapter — hired out as a caulker in Baltimore, he plans and executes his escape to New York. He deliberately withholds details to protect those who helped and those still enslaved. Marriage to Anna Murray, arrival in New Bedford, discovery of The Liberator, and the beginning of his life as an abolitionist."},
]

APPENDIX_SLUG = "appendix"
PARODY_SLUG = "parody"


def find_chapter_boundaries(text):
    """Find the start line of each chapter, plus appendix and parody."""
    lines = text.split('\n')
    boundaries = []

    for ch in CHAPTERS:
        pattern = f"CHAPTER {ch['num']}"
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == pattern:
                boundaries.append((i, ch["slug"], ch))
                break

    # Find APPENDIX
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "APPENDIX":
            boundaries.append((i, APPENDIX_SLUG, None))
            break

    # Find A PARODY
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "A PARODY":
            boundaries.append((i, PARODY_SLUG, None))
            break

    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def extract_sections(boundaries, lines):
    """Extract text for each section between boundaries."""
    sections = []
    for idx, (start_line, slug, ch_info) in enumerate(boundaries):
        # Skip header line(s) and blank lines
        content_start = start_line + 1
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
    """Split text into paragraphs (separated by blank lines)."""
    raw_paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = []
    for p in raw_paragraphs:
        cleaned = p.strip()
        if not cleaned:
            continue
        # Normalize internal whitespace
        cleaned = re.sub(r'\n\s*', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        # Strip Gutenberg-style italics markers
        cleaned = cleaned.replace('_', '')
        if len(cleaned) < 10:
            continue
        paragraphs.append(cleaned)
    return paragraphs


def first_sentence_name(text, max_len=90):
    """Extract first sentence or clause, truncated to max_len chars."""
    # Find first sentence boundary
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


def extract_keywords_from_para(para):
    """Extract relevant keywords from paragraph content."""
    keywords = []
    keyword_map = {
        "slave": "slavery",
        "slaveholder": "slaveholding",
        "master": "master",
        "whip": "violence",
        "lash": "violence",
        "blood": "violence",
        "free": "freedom",
        "freedom": "freedom",
        "liberty": "freedom",
        "read": "literacy",
        "write": "literacy",
        "learn": "education",
        "book": "education",
        "God": "religion",
        "Christian": "religion",
        "pray": "religion",
        "church": "religion",
        "mother": "family",
        "father": "family",
        "children": "family",
        "wife": "family",
        "escape": "escape",
        "flee": "escape",
        "runaway": "escape",
        "fight": "resistance",
        "resist": "resistance",
        "plantation": "plantation",
        "overseer": "plantation",
        "Baltimore": "Baltimore",
        "hunger": "deprivation",
        "cold": "deprivation",
        "naked": "deprivation",
        "song": "music",
        "sing": "music",
    }
    para_lower = para.lower()
    seen = set()
    for trigger, kw in keyword_map.items():
        if trigger.lower() in para_lower and kw not in seen:
            keywords.append(kw)
            seen.add(kw)
    return keywords


# Thematic L2 groupings with curated paragraph references
# These will be populated after parsing by matching chapter slugs to themes
THEMATIC_GROUPS = [
    {
        "id": "theme-bondage-and-dehumanization",
        "name": "Bondage and Dehumanization",
        "about": "The passages that lay bare the systematic machinery of slavery — the separation of mother and child, the erasure of birthdays and family histories, the equation of human beings with livestock, the casual violence that maintained the system. Douglass shows slavery not as an abstraction but as a lived reality of bodies counted, valued, whipped, and discarded.",
        "for_readers": "These passages confront the reader with slavery's daily mechanics. Douglass refuses to let the reader look away: the blood-stained gate, the midnight whippings, the valuation alongside cattle. His power lies in precise, unflinching detail — not rhetoric but testimony.",
        "chapter_sources": ["ch01", "ch02", "ch03", "ch04", "ch05", "ch08"],
    },
    {
        "id": "theme-education-and-awakening",
        "name": "Education and Awakening",
        "about": "The forbidden knowledge that changed everything. From Mrs. Auld's first alphabet lessons to the stolen reading sessions with white boys to the discovery of The Columbian Orator, these passages trace the kindling of Douglass's consciousness. Literacy did not bring peace — it brought anguish, the terrible clarity of understanding one's own condition. 'Learning to read had been a curse rather than a blessing.'",
        "for_readers": "Douglass's account of learning to read is one of the great education narratives in literature. Note how Master Auld's prohibition becomes the key that unlocks everything: by forbidding literacy, he reveals its power. The paradox that knowledge brings suffering before it brings liberation resonates far beyond the context of slavery.",
        "chapter_sources": ["ch06", "ch07"],
    },
    {
        "id": "theme-resistance-and-transformation",
        "name": "Resistance and Transformation",
        "about": "The arc from submission to defiance. Douglass's fight with Covey is the dramatic center of the Narrative — the moment a 'slave in form' becomes 'a slave no longer.' But resistance takes many forms: the failed escape attempt, the Sabbath school teaching, the quiet accumulation of skills and knowledge that would eventually make freedom possible.",
        "for_readers": "The fight with Covey is often called the turning point of the entire slave narrative tradition. But pay attention to the subtler resistances throughout: Douglass trading bread for literacy, mentally rehearsing arguments from The Columbian Orator, maintaining his sense of self under Covey's systematic breaking. Physical resistance was the climax, but intellectual resistance was the foundation.",
        "chapter_sources": ["ch10"],
    },
    {
        "id": "theme-freedom-and-identity",
        "name": "Freedom and New Identity",
        "about": "The journey from bondage to liberty — the dangerous escape Douglass deliberately leaves vague, the terror and exhilaration of arrival in New York, the assumption of a new name, the discovery of a community of free Black people in New Bedford. Freedom is not an endpoint but a new beginning, marked by the joy of earning one's own wages and the shock of discovering that free labor works better than slave labor.",
        "for_readers": "Douglass's account of freedom is notably complex. He describes the 'loneliness' of being a fugitive, the fear that pursued him even in the North, and the gradual discovery that freedom requires its own education. His choice of the name 'Douglass' (from Walter Scott's Lady of the Lake) and his encounter with The Liberator mark the birth of the public intellectual.",
        "chapter_sources": ["ch11"],
    },
    {
        "id": "theme-religious-hypocrisy",
        "name": "Religious Hypocrisy",
        "about": "Douglass's devastating critique of American Christianity — not Christianity itself, but the 'slaveholding religion' that used scripture to justify bondage. Masters who prayed on Sunday and whipped on Monday; revivals that produced not compassion but cruelty; the grotesque parody of 'heavenly union' that sanctified human trafficking. Douglass distinguishes sharply between the Christianity of Christ and the Christianity of America.",
        "for_readers": "This theme runs throughout the Narrative and culminates in the Appendix and Parody. Douglass is not anti-religious — he is anti-hypocrisy. His critique anticipates liberation theology by over a century: the gospel weaponized by the powerful against the powerless is not the gospel at all. The Parody of 'heavenly union' is dark satire that cuts to the bone.",
        "chapter_sources": ["ch09", "appendix", "parody"],
    },
]

# Map chapters to thematic groups
CHAPTER_THEME_MAP = {}
for tg in THEMATIC_GROUPS:
    for ch_slug in tg["chapter_sources"]:
        if ch_slug not in CHAPTER_THEME_MAP:
            CHAPTER_THEME_MAP[ch_slug] = []
        CHAPTER_THEME_MAP[ch_slug].append(tg["id"])


def build_grammar():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    text = strip_front_matter(text)

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
            keywords = extract_keywords_from_para(para)

            section_name = "Passage"
            if slug == PARODY_SLUG:
                section_name = "Verse"

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
                },
            }

            if ch_info:
                item["metadata"]["chapter"] = ch_info["title"]

            items.append(item)
            chapter_item_ids[slug].append(para_id)

    # --- L2: Chapter emergence groups ---
    chapter_abouts = {
        "ch01": {
            "about": "Douglass's origins — born in Tuckahoe, Maryland, with no knowledge of his own birthday. Separated from his mother as an infant, fathered by an unnamed white man (possibly his master). His first memory of slavery's violence: the whipping of Aunt Hester, which he calls 'the blood-stained gate, the entrance to the hell of slavery.' This chapter establishes the systematic erasure of identity that slavery requires.",
            "for_readers": "Notice how Douglass begins with what he does NOT know: his birthday, his father's name, his mother's face in daylight. Slavery is defined first as an absence — of information, of family, of selfhood. Then the chapter closes with the most vivid presence imaginable: blood, screams, the cowskin. The structure is deliberate: from silence to violence.",
        },
        "ch02": {
            "about": "The Great House Farm of Colonel Lloyd — the economic and social center of a vast slaveholding enterprise. Douglass describes the monthly food allowances, the annual clothing rations, and the slave songs whose sorrow he only understood later. 'I have often been utterly astonished to find persons who could speak of the singing among slaves as evidence of their contentment and happiness.'",
            "for_readers": "The description of slave songs is one of the most important passages in American literature. Douglass insists that the songs expressed not joy but 'the prayer and complaint of souls boiling over with the bitterest anguish.' He challenges readers who sentimentalize slave music to hear the grief beneath the melody.",
        },
        "ch03": {
            "about": "Colonel Lloyd's vast domain — his fine garden, his prized horses, his absolute power. Slaves who dared to tell the truth about their conditions were punished, teaching them that even honest speech was dangerous. The maxim among slaves became: 'a still tongue makes a wise head.'",
            "for_readers": "This chapter reveals how slavery enforced its own silence. Slaves learned to suppress truth, to perform contentment, to tell masters what they wanted to hear. Douglass shows how this self-censorship was not cowardice but survival — and how it made the system nearly impossible to challenge from within.",
        },
        "ch04": {
            "about": "The terrifying overseer Austin Gore and his cold-blooded murder of the slave Demby, who was shot dead for refusing to come out of a creek during a whipping. Gore justified it as 'necessary as an example to the other slaves.' No investigation, no trial, no consequence. Douglass catalogues additional unpunished killings to show this was systemic, not exceptional.",
            "for_readers": "This is Douglass at his most forensic. He does not merely describe violence — he describes the legal and social structures that made violence consequence-free. The murder of Demby is not an aberration but the logical endpoint of a system in which Black testimony was inadmissible and Black life had no legal value.",
        },
        "ch05": {
            "about": "Childhood deprivation on the plantation — sleeping on the cold floor, wearing only a coarse linen shirt, eating from a communal trough. Then the life-changing news: Douglass is selected to go to Baltimore. He washes himself with hope and leaves the plantation, sensing that this moment will change his fate forever.",
            "for_readers": "The transition from plantation to Baltimore is the first great turning point. Notice Douglass's extraordinary intuition — even as a child, he felt that going to Baltimore was 'the first plain manifestation of that kind providence which has ever since attended me.' The detail of scrubbing himself clean is both literal and symbolic: a preparation for a new life.",
        },
        "ch06": {
            "about": "Sophia Auld, the kindest person Douglass has yet encountered, begins teaching him the alphabet. But when her husband discovers this, he erupts: 'If you teach that nigger how to read, there would be no keeping him.' This prohibition becomes Douglass's greatest insight — the revelation that literacy is the pathway from slavery to freedom.",
            "for_readers": "Hugh Auld's speech is one of the pivotal moments in American autobiography. By articulating exactly why slaves must not read, he hands Douglass the key to his own liberation. Douglass calls it 'a new and special revelation.' The irony is perfect: the slaveholder, in trying to keep his slave ignorant, teaches him the most important lesson of all.",
        },
        "ch07": {
            "about": "Douglass's heroic self-education in Baltimore — learning to read from street boys by trading bread for lessons, discovering The Columbian Orator and its arguments for emancipation, learning the word 'abolition.' But literacy brings anguish: understanding his condition without being able to change it is torment. He teaches himself to write by copying letters in shipyards and challenging boys to writing contests.",
            "for_readers": "This is perhaps the most celebrated chapter. Douglass's ingenuity in learning to read and write — the bread-for-lessons exchanges, the shipyard letters, the copybook tricks — shows a mind that cannot be contained. But notice the dark center: 'I would at times feel that learning to read had been a curse rather than a blessing.' Knowledge without power is its own form of suffering.",
        },
        "ch08": {
            "about": "After old Master Anthony's death, all his property — human and otherwise — must be valued and divided. Douglass stands alongside cattle and pigs to be appraised. The chapter strips away any pretense that slavery was paternalistic: it was, at bottom, an accounting exercise. Douglass narrowly avoids being given to the cruel Andrew and returns to Baltimore.",
            "for_readers": "The valuation scene is among the most devastating in the Narrative. Douglass makes the reader see what slavery looked like at its most bureaucratic: human beings ranked, priced, and distributed like farm equipment. The randomness of the outcome — freedom or hell depending on which heir claims you — reveals slavery's essential arbitrariness.",
        },
        "ch09": {
            "about": "Thomas Auld at St. Michael's — a slaveholder whose religious conversion makes him crueler, not kinder. Auld starves his slaves, justifies cruelty with scripture, and hosts Methodist preachers who dine at his table while his slaves go hungry. Douglass is sent to the slave-breaker Edward Covey as punishment for his 'unmanageable' spirit.",
            "for_readers": "This chapter is Douglass's most sustained critique of religious hypocrisy. Thomas Auld's piety serves not as a check on cruelty but as its justification. The detail of Auld quoting scripture while slaves starve is not rhetorical exaggeration — it is the precise moral anatomy of a system that weaponized Christianity.",
        },
        "ch10": {
            "about": "The longest chapter and the dramatic heart of the Narrative. Under Covey, Douglass is systematically broken in body and spirit — until the day he fights back. The two-hour battle with Covey is the turning point: 'It rekindled the few expiring embers of freedom, and revived within me a sense of my own manhood.' Later chapters within this section cover the failed first escape attempt, the Sabbath school, time with the comparatively kind William Freeland, and the return to Baltimore.",
            "for_readers": "The fight with Covey is the most anthologized passage in all of slave narrative literature. But read the context: six months of systematic dehumanization precede it, and the aftermath is not triumph but ongoing enslavement. Douglass's physical resistance did not free him — it restored his will to be free. The distinction matters enormously.",
        },
        "ch11": {
            "about": "The final chapter — Douglass's escape from slavery, deliberately told without details that might endanger others. Hired out as a caulker, he experiences the injustice of handing his wages to Master Hugh. He escapes to New York, marries Anna Murray, settles in New Bedford, chooses the name Douglass, and discovers The Liberator and the anti-slavery movement that will become his life's work.",
            "for_readers": "Douglass's refusal to narrate the details of his escape is itself a powerful statement: the story of freedom cannot be told if telling it would endanger those still in bondage. Notice the transformative power of New Bedford — Douglass's astonishment that free labor produces more prosperity than slave labor, that a 'fugitive' can live with dignity. The discovery of The Liberator is the final awakening.",
        },
        "appendix": {
            "about": "Douglass clarifies his critique of religion: he opposes not Christianity itself but the 'slaveholding religion of this land.' Between the Christianity of Christ and the Christianity of America, he recognizes 'the widest possible difference.' He quotes Jeremiah, Isaiah, and Matthew against the hypocrisy of Christian slaveholders.",
            "for_readers": "The Appendix is essential for understanding Douglass's moral framework. He is not a secularist attacking religion — he is a believer exposing false religion. His distinction between Christianity proper and slaveholding Christianity anticipates the entire tradition of liberation theology. The biblical quotations he marshals are devastating precisely because they are wielded by someone the slaveholders claimed was not fully human.",
        },
        "parody": {
            "about": "A biting satirical hymn — a parody of 'heavenly union' that exposes how Southern preachers sanctified slavery. 'Come, saints and sinners, hear me tell / How pious priests whip Jack and Nell.' Each stanza pairs religious devotion with slaveholding cruelty, making the hypocrisy impossible to ignore.",
            "for_readers": "The Parody closes the Narrative with dark, unforgettable satire. Set to the meter of a hymn, it forces the reader to hear how Christianity sounded from the slave's perspective — as a soundtrack to violence. The sing-song rhythm makes the horror more, not less, disturbing.",
        },
    }

    for section in sections:
        slug = section["slug"]
        ch_info = section["ch_info"]
        sort_order += 1
        ids = chapter_item_ids.get(slug, [])
        about_data = chapter_abouts.get(slug, {})

        if ch_info:
            title = ch_info["title"]
        elif slug == APPENDIX_SLUG:
            title = "Appendix: On Christianity and Slaveholding Religion"
        elif slug == PARODY_SLUG:
            title = "A Parody: Heavenly Union"
        else:
            title = slug

        sections_dict = {
            "About": about_data.get("about", f"Section: {title}"),
            "For Readers": about_data.get("for_readers", ""),
        }

        item = {
            "id": f"chapter-{slug}",
            "name": title,
            "level": 2,
            "category": "chapter-group",
            "sort_order": sort_order,
            "sections": sections_dict,
            "keywords": [],
            "composite_of": ids,
            "relationship_type": "emergence",
            "metadata": {},
        }
        items.append(item)

    # --- L2: Thematic groups ---
    for tg in THEMATIC_GROUPS:
        sort_order += 1
        # Collect all L1 ids from the source chapters
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
        "id": "meta-arc-of-liberation",
        "name": "The Arc of Liberation",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "The chronological arc of Douglass's Narrative — from birth in bondage through awakening, resistance, and escape to freedom and public voice. Each chapter marks a stage in the journey from property to person, from silence to testimony. This is the story read as autobiography: one man's passage through the machinery of slavery and out the other side, transformed.",
            "For Readers": "Read the chapters in order to experience the Narrative as Douglass structured it — a carefully shaped argument in the form of a life. Each chapter builds on the last: ignorance gives way to knowledge, submission to resistance, bondage to freedom. The arc is not merely personal but political: Douglass's individual liberation is presented as evidence against the entire system.",
        },
        "keywords": ["autobiography", "liberation", "chronology"],
        "composite_of": chapter_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    sort_order += 1
    items.append({
        "id": "meta-themes-of-witness",
        "name": "Themes of Witness",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "The Narrative read thematically rather than chronologically — organized by the great recurring subjects that structure Douglass's testimony. Bondage and dehumanization. The forbidden power of literacy. Physical and intellectual resistance. The complex arrival at freedom. The corrosive hypocrisy of slaveholding religion. These themes cut across chapters and reveal the deep architecture of Douglass's argument.",
            "For Readers": "These thematic groupings let you explore the Narrative by subject rather than sequence. Want to understand how Douglass thinks about education? Start with 'Education and Awakening.' Want to confront slavery's violence? 'Bondage and Dehumanization' gathers the testimony. Each theme connects passages from across the Narrative, revealing patterns that the chronological reading may obscure.",
        },
        "keywords": ["themes", "witness", "testimony"],
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
                {
                    "name": "Frederick Douglass",
                    "date": "1845",
                    "note": "Author"
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2006",
                    "note": "Digital source, eBook #23"
                }
            ]
        },
        "name": "Narrative of the Life of Frederick Douglass",
        "description": "Frederick Douglass's 'Narrative of the Life of Frederick Douglass, an American Slave, Written by Himself' (1845) — one of the most powerful and influential autobiographies in American literature. Born into slavery in Maryland, Douglass taught himself to read, fought his overseer, escaped to freedom, and became the most prominent voice of the abolitionist movement. This Narrative is testimony, argument, and literature at once: a first-person account that dismantled every justification for slavery and changed the conscience of a nation.\n\nSource: Project Gutenberg eBook #23 (https://www.gutenberg.org/ebooks/23)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Daguerreotypes and photographs of Frederick Douglass (the most photographed American of the 19th century). Illustrations from the 1845 first edition published by the Anti-Slavery Office, Boston. Woodcuts and engravings from abolitionist publications including The Liberator. Portraits by Elisha Hammond and other period artists.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "autobiography",
            "slavery",
            "abolition",
            "resistance",
            "freedom",
            "literacy",
            "public-domain",
            "full-text",
            "american-literature",
            "social-justice",
            "testimony"
        ],
        "roots": [
            "social-justice",
            "freedom-commons"
        ],
        "shelves": [
            "resilience",
            "mirror"
        ],
        "lineages": [
            "Akomolafe",
            "Andreotti"
        ],
        "worldview": "dialectical",
        "items": items,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Print summary
    l1_count = sum(1 for item in items if item["level"] == 1)
    l2_count = sum(1 for item in items if item["level"] == 2)
    l3_count = sum(1 for item in items if item["level"] == 3)
    print(f"Generated {len(items)} items: {l1_count} L1 + {l2_count} L2 + {l3_count} L3")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    build_grammar()
