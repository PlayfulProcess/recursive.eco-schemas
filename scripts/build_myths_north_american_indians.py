#!/usr/bin/env python3
"""
Parser for The Myths of the North American Indians by Lewis Spence (Project Gutenberg #42390).
Outputs grammar.json into grammars/myths-north-american-indians/

This is a complex text that weaves scholarly commentary with myth narratives.
Chapters I-II are pure scholarship; chapters III-VII contain myths organized
by tribal group. We extract named sub-sections from chapters III-VII as
individual myth items.
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'myths-north-american-indians.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'myths-north-american-indians')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

# Chapter definitions with tribal group info
CHAPTERS = [
    {"marker": "CHAPTER III: ALGONQUIAN MYTHS AND LEGENDS", "id_prefix": "algonquian", "tribe": "Algonquian", "category": "algonquian-myths"},
    {"marker": "CHAPTER IV: IROQUOIS MYTHS AND LEGENDS", "id_prefix": "iroquois", "tribe": "Iroquois", "category": "iroquois-myths"},
    {"marker": "CHAPTER V: SIOUX MYTHS AND LEGENDS", "id_prefix": "sioux", "tribe": "Sioux/Dakota", "category": "sioux-myths"},
    {"marker": "CHAPTER VI: MYTHS AND LEGENDS OF THE PAWNEES", "id_prefix": "pawnee", "tribe": "Pawnee/Caddoan", "category": "pawnee-myths"},
    {"marker": "CHAPTER VII: MYTHS AND LEGENDS OF THE NORTHERN AND NORTH-WESTERN INDIANS", "id_prefix": "northwest", "tribe": "Northern/North-Western", "category": "northwest-myths"},
]

# Sub-sections to skip (pure commentary, not narrative myths)
SKIP_HEADINGS = {
    # Commentary/analytical sections
    "Scandinavian Analogies",
    "The Sioux or Dakota Indians",
    "Iroquois Gods and Heroes",
    "The Pawnees, or Caddoan Indians",
    "Haida Demi-Gods",
    "Chinook Tales",
    "Beliefs of the Californian Tribes",
    "Myths of the Athapascans",
    "Witches and Witchcraft",
}

# Sections that are continuations of the previous story (merge with previous)
CONTINUATION_HEADINGS = {
    "Algon's Strategy": "The Star-Maiden",
    "The Star-Maiden's Escape": "The Star-Maiden",
    "Cloud-Carrier and the Star-Folk": "The Star-Maiden",
    "The Star-Country": "The Star-Maiden",
    "The Sacrifice": "The Star-Maiden",
    "The Lover's Revenge": "The Snow-Man Husband",
    "The Return to Earth": None,  # Multiple uses; handle contextually
    "The Lord of Cold Weather": "The Snow-Lodge",
    "The Elves of Light": "How Glooskap Caught the Summer",
    "Glooskap's Gifts": "Glooskap and Malsum",
    "The Struggle": "The Maize Spirit",
    "The Final Contest": "The Maize Spirit",
    "The Chase": "The Seven Brothers",
    "How Kutoyis was Born": "The Story of Kutoyis",
    "Kutoyis on his Travels": "The Story of Kutoyis",
    "The Wrestling Woman": "The Story of Kutoyis",
    "The Herds of Buffalo-Stealer": "Nápi and the Buffalo-Stealer",
    "Bear Magic": "The Sacred Bear-Spear",
    "How the Magic Worked": "The Sacred Bear-Spear",
    "The Gift": "The Lodge of Animals",
    "The Friendly Wolf": "The Medicine Wolf",
    "The Sun-God's Decree": "The Story of Scar-face",
    "The Chase of the Savage Birds": "The Story of Scar-face",
    "The Great Turnip": "The Legend of Poïa",
    "Otter-Heart's Stratagem": "The Ball-Players",
    "Moose Demands a Wife": "The Fairy Wives",
    "The Red Star and the Yellow Star": "The Fairy Wives",
    "The Escape from Lox": "The Fairy Wives",
    "The Death-Swing": "The Malicious Mother-in-Law",
    "The Silver Girdle": "The Malicious Mother-in-Law",
    "The Fate of the Head": "The Pursuing Head",
    "Ictinike and the Buzzard": "The Adventures of Ictinike",
    "Ictinike and the Creators": "The Adventures of Ictinike",
    "The Men-Serpents": "The Story of Wabaskaha",
    "The Three Tests": "The Snake-Ogre",
    "The Race": "The Snake-Ogre",
    "The Snake's Quest": "The Magic Moccasins",
    "Salmon's Magic Bath": "The Story of the Salmon",
    "The Drowned Child": "The Wolf Lodge",
    "The Ring Unavailing": "The Snake-Wife",
    "The Finding of the Snake-Wife": "The Snake-Wife",
    "Lost Underground": "A Subterranean Adventure",
    "In Search of the Giants": "White Feather the Giant-Killer",
    "Chácopee's Downfall": "White Feather the Giant-Killer",
    "The Transformation": "White Feather the Giant-Killer",
    "The Bear-Man Slain": "The Bear-Man",
    "The Resuscitation of the Bear-Man": "The Bear-Man",
    "The Birth of Sîñ": "The Supernatural Sister",
    "The Finding of Porcupine": "The Beaver and the Porcupine",
    "The Marriage of Ioi": "The Story of Blue Jay and Ioi",
    "A Fishing Expedition in Shadow-land": "The Story of Blue Jay and Ioi",
    "Blue Jay and Ioi Go Visiting": "The Story of Blue Jay and Ioi",
    "The Whale-catcher": "The Heaven-sought Bride",
    "The Four Tests": "The Chinooks Visit the Supernaturals",
    "The Thunderer": "The Thunderer's Son-in-Law",
    "The Beast Comrades": "The Thunderer's Son-in-Law",
    "The Tests": "The Thunderer's Son-in-Law",
    "The Spirit-land": "The Thunderer's Son-in-Law",
    "The Stone Giants": "Hi'nun",
    "The Pigmies": None,
    "The Quarrel": "The Peace Queen",
    "The Offers": "The Peace Queen",
    "The Finding of the Waters": "The Healing Waters",
    "The Pity of the Trees": "The Healing Waters",
}


def read_seed():
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[text.index('\n', start_idx) + 1:]
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]
    return text.strip()


def clean_text(text):
    """Clean illustration markers, page markers, footnotes."""
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    text = re.sub(r'\{[\divx]+\}', '', text)
    text = re.sub(r'\n\n\[(\d+)\][^\n]*\n', '\n\n', text)
    text = re.sub(r'\[(\d+)\]', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def make_id(prefix, title):
    """Create a clean ID from a prefix and title."""
    # Remove special characters and convert to lowercase
    clean = re.sub(r'[^\w\s-]', '', title.lower())
    clean = re.sub(r'\s+', '-', clean.strip())
    clean = re.sub(r'-+', '-', clean)
    return f"{prefix}-{clean}"


def is_heading(line, prev_line, next_line):
    """Check if a line looks like a section heading."""
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith('CHAPTER'):
        return True
    if re.match(r'^\{[\divx]+\}$', stripped):
        return False
    if stripped.startswith('['):
        return False
    if len(stripped) > 80:
        return False
    if len(stripped) < 5:
        return False

    prev = prev_line.strip() if prev_line else ''
    nxt = next_line.strip() if next_line else ''

    # Must be preceded by blank line
    if prev != '' and not re.match(r'^\{[\divx]+\}$', prev):
        return False

    # Must be followed by blank line or page marker
    if nxt != '' and not re.match(r'^\{[\divx]+\}$', nxt):
        return False

    # Must start with uppercase
    words = stripped.split()
    if not words or not words[0][0].isupper():
        return False

    # Must not end with period (that's a sentence)
    if stripped.endswith('.') and stripped.count('.') == 1 and len(stripped) > 40:
        return False

    # Must have at least 2 words (with some exceptions)
    if len(words) < 2 and stripped not in ('Hi\'nun',):
        return False

    # Must not end with a period (sentence, not heading)
    if stripped.endswith('.'):
        return False

    # Must not start with lowercase articles or connecting words (sentence fragments)
    if words[0].lower() in ('the', 'a', 'an', 'but', 'and', 'or', 'so', 'then', 'when', 'he', 'she', 'they', 'one', 'another', 'softly', 'still'):
        # Unless it's clearly a title (starts with "The" and is short)
        if words[0] == 'The' and len(stripped) < 50:
            pass  # Allow "The Star-Maiden" etc.
        elif words[0] in ('A', 'An') and len(stripped) < 50:
            pass  # Allow "A Strange Transformation" etc.
        else:
            return False

    # Filter out entries that look like index entries (contain page numbers)
    if re.search(r'\d{2,3}[-,]?\s*\d{2,3}', stripped):
        return False
    if re.search(r'\d{2,3}$', stripped):
        return False

    # Filter out sentences (multiple lowercase words in sequence)
    lowercase_runs = re.findall(r'\b[a-z]+\b', stripped)
    if len(lowercase_runs) > 5:
        return False

    return True


def extract_sections(text):
    """Extract all heading-delimited sections from chapters III-VII."""
    # Find chapter boundaries
    chapter_starts = []
    for ch in CHAPTERS:
        idx = text.find(ch["marker"])
        if idx != -1:
            chapter_starts.append((idx, ch))

    # End marker - stop before bibliography/glossary
    # Search for these markers anywhere (they may be preceded by page markers)
    bib_match = re.search(r'\nBIBLIOGRAPHY\s*\n', text)
    glossary_match = re.search(r'\nGLOSSARY AND INDEX\s*\n', text)
    bib_pos = bib_match.start() if bib_match else len(text)
    glossary_pos = glossary_match.start() if glossary_match else len(text)
    bib_idx = min(bib_pos, glossary_pos)

    all_sections = []
    lines = text.split('\n')

    # Find all headings in the myths section
    start_offset = chapter_starts[0][0] if chapter_starts else 0
    start_line = text[:start_offset].count('\n')

    # Calculate the line number where bibliography/glossary starts
    end_line_limit = text[:bib_idx].count('\n')

    headings = []
    for i in range(start_line, min(len(lines), end_line_limit)):
        prev = lines[i - 1] if i > 0 else ''
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if is_heading(lines[i], prev, nxt):
            headings.append((i, lines[i].strip()))

    # Determine which chapter each heading belongs to
    chapter_lines = []
    for ch_start, ch_info in chapter_starts:
        ch_line = text[:ch_start].count('\n')
        chapter_lines.append((ch_line, ch_info))

    # Process headings into sections
    for h_idx, (line_no, heading) in enumerate(headings):
        if heading.startswith('CHAPTER'):
            continue

        # Find which chapter this belongs to
        chapter_info = None
        for cl, ci in reversed(chapter_lines):
            if line_no > cl:
                chapter_info = ci
                break

        if chapter_info is None:
            continue

        # Find end of this section
        if h_idx + 1 < len(headings):
            end_line = headings[h_idx + 1][0]
        else:
            end_bib = text[:bib_idx].count('\n')
            end_line = end_bib

        section_text = '\n'.join(lines[line_no + 1:end_line])
        section_text = clean_text(section_text)

        if len(section_text.strip()) < 100:
            continue

        all_sections.append({
            "heading": heading,
            "text": section_text,
            "chapter": chapter_info,
            "line_no": line_no
        })

    return all_sections


def merge_sections(sections):
    """Merge continuation sections into their parent stories."""
    merged = {}
    section_order = []

    for sec in sections:
        heading = sec["heading"]
        # Remove footnote markers from heading
        heading_clean = re.sub(r'\[\d+\]', '', heading).strip()

        if heading_clean in SKIP_HEADINGS:
            continue

        if heading_clean in CONTINUATION_HEADINGS:
            parent = CONTINUATION_HEADINGS[heading_clean]
            if parent is None:
                continue
            if parent in merged:
                merged[parent]["text"] += "\n\n\n" + heading_clean + "\n\n" + sec["text"]
                continue
            # If parent not found yet, treat as standalone
            # (this handles the case where continuation appears before parent)

        merged[heading_clean] = {
            "heading": heading_clean,
            "text": sec["text"],
            "chapter": sec["chapter"],
            "line_no": sec["line_no"]
        }
        section_order.append(heading_clean)

    return [merged[h] for h in section_order if h in merged]


def generate_keywords(heading, text, chapter_info):
    """Generate keywords based on heading and content."""
    keywords = []
    heading_lower = heading.lower()

    # Add tribe-related keywords
    tribe = chapter_info.get("tribe", "")
    if tribe:
        keywords.append(tribe.lower().split('/')[0].strip())

    # Extract key terms from heading
    words = re.findall(r'\b[A-Z][a-z]+\b', heading)
    for w in words:
        if w.lower() not in ('the', 'and', 'of', 'in', 'a', 'an', 'how', 'why'):
            keywords.append(w.lower())

    # Add thematic keywords based on content
    text_lower = text.lower()
    theme_keywords = {
        "trickster": ["trickster", "tricked", "cunning", "outwit"],
        "creation": ["created", "creation", "beginning", "first"],
        "spirit": ["spirit", "ghost", "supernatural", "vision"],
        "animal": ["bear", "wolf", "eagle", "beaver", "buffalo", "rabbit", "turtle"],
        "magic": ["magic", "magical", "enchant", "spell", "medicine"],
        "hero": ["warrior", "brave", "courage", "battle", "quest"],
        "transformation": ["transform", "changed", "became", "shape"],
        "love": ["love", "maiden", "wife", "husband", "marriage"],
    }
    for theme, terms in theme_keywords.items():
        for term in terms:
            if term in text_lower[:500]:
                keywords.append(theme)
                break

    return list(set(keywords))[:8]


def build_items(sections):
    """Build L1 items from extracted sections."""
    items = []
    used_ids = set()

    for sort_order, sec in enumerate(sections):
        prefix = sec["chapter"]["id_prefix"]
        heading = sec["heading"]
        item_id = make_id(prefix, heading)

        # Handle duplicate IDs
        if item_id in used_ids:
            item_id = item_id + "-2"
        used_ids.add(item_id)

        keywords = generate_keywords(heading, sec["text"], sec["chapter"])
        tribe = sec["chapter"]["tribe"]

        item = {
            "id": item_id,
            "name": heading,
            "sort_order": sort_order,
            "level": 1,
            "category": sec["chapter"]["category"],
            "sections": {
                "Story": sec["text"],
                "Tribal Tradition": tribe
            },
            "keywords": keywords,
            "metadata": {
                "source": "The Myths of the North American Indians by Lewis Spence, George G. Harrap & Co., London, 1914",
                "chapter": sec["chapter"]["marker"],
                "tribe": tribe
            }
        }
        items.append(item)

    return items


def build_l2_items(l1_items):
    """Build L2 groupings by chapter/tribal group and by theme."""
    l2_items = []
    sort_order = len(l1_items)

    # Group by chapter/tribe
    chapter_groups = {
        "algonquian-myths": {
            "id": "group-algonquian",
            "name": "Algonquian Myths and Legends",
            "about": "The Algonquian peoples — including the Micmac, Chippeway, Blackfeet, and many others — possessed perhaps the most extensive mythology of all North American peoples. Central to their traditions is Glooskap (or Glooscap), the trickster-creator who made the world habitable for humans, fought monsters, and finally departed in a great canoe, promising to return. The Algonquian myths also include beautiful tales of star-maidens, the spirit of Winter, and the sacred origins of medicine bundles and war customs.",
            "for_readers": "These stories come from peoples who lived across the vast forests and plains of northeastern North America. Their mythology reflects an intimate relationship with the seasons, with the struggle between winter and summer, and with the animals of forest and prairie. Glooskap is a figure of extraordinary depth — at once a world-creator and a comic fool who cannot make a baby stop crying.",
            "keywords": ["algonquian", "glooskap", "micmac", "chippeway", "blackfeet", "forest", "winter"]
        },
        "iroquois-myths": {
            "id": "group-iroquois",
            "name": "Iroquois Myths and Legends",
            "about": "The Iroquois Confederacy — the Mohawk, Oneida, Onondaga, Cayuga, Seneca, and later the Tuscarora — created one of the most remarkable political institutions of pre-Columbian America. Their myths reflect this genius for organization, featuring the Thunder-god Hi'nun, the stone giants, and the legendary peace-maker Hiawatha. These tales blend cosmic mythology with semi-historical legend, showing how myth gathers around great leaders and events.",
            "for_readers": "The Iroquois myths are notable for their blend of the cosmic and the political. The founding of the great Confederacy is told as both history and myth, with supernatural beings intervening in human affairs. These stories also feature remarkable female figures, including the Peace Queen and the mysterious Stone Giantess.",
            "keywords": ["iroquois", "confederacy", "hinun", "thunder", "hiawatha", "peace", "stone-giants"]
        },
        "sioux-myths": {
            "id": "group-sioux",
            "name": "Sioux Myths and Legends",
            "about": "The Sioux (Dakota) Indians, dwelling along the Mississippi and Missouri rivers, tell of the trickster Ictinike — son of the sun-god, expelled from heaven for his misdeeds. Their mythology also includes tales of snake-wives, magic moccasins, subterranean adventures, and the great hero White Feather. The Sioux myths are marked by their intensity, their sense of the numinous in nature, and their complex relationship between the human and spirit worlds.",
            "for_readers": "The Sioux myths carry a particular intensity and darkness. Ictinike is one of the most interesting trickster figures — not merely mischievous but genuinely malicious, a 'Father of Lies' who teaches humanity all its bad habits. The snake-wife stories explore the boundaries between human and animal in haunting ways.",
            "keywords": ["sioux", "dakota", "ictinike", "trickster", "snake-wife", "white-feather"]
        },
        "pawnee-myths": {
            "id": "group-pawnee",
            "name": "Pawnee Myths and Legends",
            "about": "The Pawnees (Caddoan Indians) were gifted with an elaborate form of religious ceremonial. Their myths center on sacred bundles, magical feathers, and the bear-man — a figure who embodies the power that flows between human and animal. These tales are deeply imbued with spiritual significance, showing how the supernatural constantly interpenetrates daily life.",
            "for_readers": "The Pawnee myths are perhaps the most overtly spiritual of all the traditions collected here. Every object has sacred significance, every encounter with an animal may be an encounter with power. The story of the sacred bundle shows how divine gifts must be treated with absolute reverence.",
            "keywords": ["pawnee", "caddoan", "sacred-bundle", "ceremony", "bear-man", "spiritual"]
        },
        "northwest-myths": {
            "id": "group-northwest",
            "name": "Myths of the Northern and North-Western Indians",
            "about": "The myths of the Haida, Tlingit, Chinook, and other Pacific Northwest peoples are among the most imaginative and artistically sophisticated in all of Native American tradition. They tell of shape-shifting beings, journeys to Shadow-land, supernatural marriages, and the cosmic figure of the Thunderer. The Blue Jay tales of the Chinook are particularly celebrated for their humor and their vivid portrayal of the spirit world.",
            "for_readers": "These myths come from the great carving and totem-pole cultures of the Northwest Coast. Their stories are visually vivid, dramatically complex, and often darkly humorous. The Blue Jay stories in particular are masterpieces of comic storytelling, with Blue Jay as a rude and bumbling visitor to the land of the dead.",
            "keywords": ["haida", "chinook", "tlingit", "northwest", "totem", "blue-jay", "thunderer", "shadow-land"]
        },
    }

    for cat, group in chapter_groups.items():
        member_ids = [item["id"] for item in l1_items if item["category"] == cat]
        if member_ids:
            l2_items.append({
                "id": group["id"],
                "name": group["name"],
                "sort_order": sort_order,
                "level": 2,
                "category": "tribal-group",
                "sections": {
                    "About": group["about"],
                    "For Readers": group["for_readers"]
                },
                "keywords": group["keywords"],
                "composite_of": member_ids,
                "relationship_type": "emergence",
                "metadata": {}
            })
            sort_order += 1

    # Thematic groupings across tribes
    theme_groups = [
        {
            "id": "theme-trickster",
            "name": "Trickster Figures",
            "about": "The trickster is one of the central figures of North American mythology — Glooskap of the Algonquians, Ictinike of the Sioux, Blue Jay of the Chinook, and Nápi of the Blackfeet. These beings are creators and destroyers, heroes and fools, benefactors and nuisances. They teach through their failures as much as their successes, and their stories carry the deepest truths about human nature wrapped in the wildest comedy.",
            "for_readers": "The trickster is the most human of the mythological figures — brilliant and stupid, generous and selfish, creative and destructive. These stories are often very funny, but the humor carries profound wisdom about the nature of intelligence, desire, and the limits of cleverness.",
            "match_categories": ["algonquian-myths", "sioux-myths", "northwest-myths"],
            "match_keywords": ["trickster"],
            "keywords": ["trickster", "glooskap", "ictinike", "blue-jay", "napi"]
        },
        {
            "id": "theme-creation-origins",
            "name": "Creation and Origin Tales",
            "about": "How was the world made? How did summer come to the frozen north? Where did the maize plant come from? These origin stories from different tribes share common themes — the earth-diver who brings up mud from beneath the primordial waters, the culture hero who steals fire or captures summer, the sacred being who teaches humanity the arts of civilization.",
            "for_readers": "Compare the creation and origin stories from different tribes. Notice what they share and where they differ. Each version reveals something about the particular relationship between a people and their environment.",
            "match_categories": ["algonquian-myths", "pawnee-myths"],
            "match_keywords": ["creation"],
            "keywords": ["creation", "origins", "world-making", "culture-hero"]
        },
        {
            "id": "theme-spirit-encounters",
            "name": "Spirit World Encounters",
            "about": "The boundary between the human world and the spirit world is thin in North American mythology. Hunters meet supernatural beings in the forest. A man descends underground and returns transformed. The dead are visited in Shadow-land. Spirit-brides cross from one world to another. These tales map a cosmology in which the unseen world is always close, always accessible to those with the eyes to see.",
            "for_readers": "These stories treat the spirit world as a real place with its own geography, inhabitants, and rules. The encounters described here range from the terrifying to the tender. What do they reveal about the relationship between the seen and unseen dimensions of reality?",
            "match_categories": ["algonquian-myths", "iroquois-myths", "sioux-myths", "northwest-myths"],
            "match_keywords": ["spirit", "supernatural"],
            "keywords": ["spirit-world", "supernatural", "vision", "shadow-land"]
        },
        {
            "id": "theme-heroes-warriors",
            "name": "Heroes and Warriors",
            "about": "From White Feather the Giant-Killer to Kutoyis the Blood-Clot Boy, from the Seneca warrior who takes revenge to the young brave who faces the Stone Giants, these hero tales celebrate courage, endurance, and the willingness to face impossible odds. North American heroes are not merely strong — they are resourceful, patient, and often aided by supernatural power earned through spiritual discipline.",
            "for_readers": "The heroes of these stories earn their power through fasting, prayer, and spiritual trial. Physical strength alone is never enough. These tales model a form of heroism rooted in spiritual preparation and moral integrity.",
            "match_categories": ["algonquian-myths", "iroquois-myths", "sioux-myths"],
            "match_keywords": ["hero", "warrior"],
            "keywords": ["hero", "warrior", "courage", "giant-killer", "quest"]
        },
        {
            "id": "theme-animal-medicine",
            "name": "Animal Medicine and Sacred Animals",
            "about": "Animals in North American mythology are not merely animals — they are persons, teachers, and sources of sacred power. The bear gives medicine. The wolf offers friendship. The beaver and porcupine carry cosmic significance. The eagle's feather confers spiritual authority. These tales illuminate the deep reciprocal relationship between humans and the animal world that lies at the heart of indigenous cosmology.",
            "for_readers": "In these stories, animals choose to share their power with humans — but only with those who approach with respect and humility. The concept of 'animal medicine' reflects a worldview in which every creature possesses its own form of spiritual power and wisdom.",
            "match_categories": ["algonquian-myths", "pawnee-myths", "northwest-myths"],
            "match_keywords": ["animal", "medicine"],
            "keywords": ["animals", "medicine", "bear", "wolf", "eagle", "sacred"]
        },
    ]

    for tgroup in theme_groups:
        member_ids = []
        for item in l1_items:
            if item["category"] in tgroup["match_categories"]:
                for kw in tgroup["match_keywords"]:
                    if kw in item.get("keywords", []):
                        member_ids.append(item["id"])
                        break
        if not member_ids:
            # Fall back to at least grabbing some items
            for item in l1_items:
                if item["category"] in tgroup["match_categories"]:
                    member_ids.append(item["id"])
                    if len(member_ids) >= 5:
                        break

        if member_ids:
            l2_items.append({
                "id": tgroup["id"],
                "name": tgroup["name"],
                "sort_order": sort_order,
                "level": 2,
                "category": "themes",
                "sections": {
                    "About": tgroup["about"],
                    "For Readers": tgroup["for_readers"]
                },
                "keywords": tgroup["keywords"],
                "composite_of": member_ids,
                "relationship_type": "emergence",
                "metadata": {}
            })
            sort_order += 1

    return l2_items, sort_order


def build_l3_items(start_sort_order, l2_items):
    """Build L3 meta-categories."""
    tribal_ids = [item["id"] for item in l2_items if item["category"] == "tribal-group"]
    theme_ids = [item["id"] for item in l2_items if item["category"] == "themes"]

    l3_items = []
    sort_order = start_sort_order

    if tribal_ids:
        l3_items.append({
            "id": "meta-tribal-traditions",
            "name": "Tribal Traditions",
            "sort_order": sort_order,
            "level": 3,
            "category": "meta",
            "sections": {
                "About": "The myths of the North American Indians are organized here by the great tribal and linguistic families that Spence treats: Algonquian, Iroquois, Sioux, Pawnee, and the Northern and North-Western peoples. Each tradition has its own character — the Algonquian myths are dominated by the trickster-creator Glooskap, the Iroquois by the Thunder-god Hi'nun and the great Confederacy, the Sioux by the dark trickster Ictinike, the Pawnee by sacred ceremony, and the Northwest by shape-shifting beings and shadow-land journeys. Together they form a continent-spanning tapestry of imagination, spiritual insight, and narrative art."
            },
            "keywords": ["tribal", "traditions", "peoples", "nations"],
            "composite_of": tribal_ids,
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    if theme_ids:
        l3_items.append({
            "id": "meta-themes",
            "name": "Themes Across Traditions",
            "sort_order": sort_order,
            "level": 3,
            "category": "meta",
            "sections": {
                "About": "Across all the tribal traditions collected by Spence, certain great themes recur: the trickster who creates and disrupts, the spirit world that lies just beyond the veil of the visible, the hero who earns power through spiritual discipline, the sacred animals who share their medicine with humanity, and the origin stories that explain how the world came to be as it is. These thematic groupings reveal the deep structural unity beneath the surface diversity of North American mythologies."
            },
            "keywords": ["themes", "cross-tribal", "unity", "patterns"],
            "composite_of": theme_ids,
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    return l3_items


def build_grammar(l1_items, l2_items, l3_items):
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Lewis Spence",
                    "date": "1914",
                    "note": "Author, The Myths of the North American Indians, George G. Harrap & Co., London"
                },
                {
                    "name": "James Jack",
                    "date": "1914",
                    "note": "Illustrator of the original edition (32 colour plates)"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure, thematic groupings, and descriptions"
                }
            ]
        },
        "name": "The Myths of the North American Indians",
        "description": "A comprehensive collection of myths and legends from the major North American Indian tribal groups — Algonquian, Iroquois, Sioux, Pawnee, and the Northern and North-Western peoples — as recorded and retold by Lewis Spence (1914). Features the trickster-creator Glooskap, the Thunder-god Hi'nun, the dark trickster Ictinike, sacred ceremonial traditions, and the extraordinary mythology of the Pacific Northwest. Spence draws on the fieldwork of the Bureau of American Ethnology to present these myths as living spiritual traditions of extraordinary depth and beauty. Source: Project Gutenberg eBook #42390 (https://www.gutenberg.org/ebooks/42390).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: James Jack's original 32 colour plates for the 1914 George G. Harrap edition — vivid paintings of mythological scenes. George Catlin's paintings of Native American life and ceremony (1830s-1840s). Karl Bodmer's illustrations from 'Travels in the Interior of North America' (1832-1834). Edward S. Curtis photographs of Native American peoples (early 1900s, Library of Congress).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "mythology",
            "native-american",
            "trickster",
            "spirits",
            "animism",
            "creation",
            "heroes",
            "ceremony",
            "oracle"
        ],
        "roots": ["indigenous-mythology"],
        "shelves": ["earth"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "animist",
        "cover_image_url": "",
        "items": l1_items + l2_items + l3_items
    }
    return grammar


def main():
    print("Reading seed text...")
    raw_text = read_seed()

    print("Stripping Gutenberg header/footer...")
    text = strip_gutenberg(raw_text)

    print("Extracting sections from chapters III-VII...")
    sections = extract_sections(text)
    print(f"  Found {len(sections)} raw sections")

    print("Merging continuation sections...")
    merged = merge_sections(sections)
    print(f"  {len(merged)} merged stories")

    print("Building L1 items...")
    l1_items = build_items(merged)

    print("Building L2 items...")
    l2_items, next_sort = build_l2_items(l1_items)

    print("Building L3 items...")
    l3_items = build_l3_items(next_sort, l2_items)

    print("Assembling grammar...")
    grammar = build_grammar(l1_items, l2_items, l3_items)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Writing grammar to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    total_items = len(l1_items) + len(l2_items) + len(l3_items)
    print(f"\nDone! {total_items} items total:")
    print(f"  L1 (stories): {len(l1_items)}")
    print(f"  L2 (groups): {len(l2_items)}")
    print(f"  L3 (meta): {len(l3_items)}")


if __name__ == '__main__':
    main()
