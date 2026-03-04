#!/usr/bin/env python3
"""
Build grammar.json for Philippine Folk Tales from seeds/philippine-folk-tales.txt
(Project Gutenberg #12814, Mabel Cook Cole, 1916)

Stories organized into 5 tribal groups: Tinguian, Igorot, Wild Tribes of Mindanao, Moro, Christianized Tribes.
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SEED_FILE = os.path.join(ROOT_DIR, "seeds", "philippine-folk-tales.txt")
OUTPUT_DIR = os.path.join(ROOT_DIR, "grammars", "philippine-folk-tales")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "grammar.json")


# Story definitions - title as it appears in the text, group, and sub-group
STORIES = [
    # Tinguian
    {"title": "Aponibolinayen and the Sun", "group": "tinguian", "sub": "Tinguian"},
    {"title": "Aponibolinayen", "group": "tinguian", "sub": "Tinguian"},
    {"title": "Gawigawen of Adasen", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Story of Gaygayoma Who Lives up Above", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Story of Dumalawi", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Story of Kanag", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Story of Tikgi", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Story of Sayen", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Sun and the Moon", "group": "tinguian", "sub": "Tinguian"},
    {"title": "How the Tinguian Learned to Plant", "group": "tinguian", "sub": "Tinguian"},
    {"title": "Magsawi", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Tree with the Agate Beads", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Striped Blanket", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Alan and the Hunters", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Man and the Alan", "group": "tinguian", "sub": "Tinguian"},
    {"title": "Sogsogot", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Mistaken Gifts", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Boy Who Became a Stone", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Turtle and the Lizard", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Man with the Cocoanuts", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Carabao and the Shell", "group": "tinguian", "sub": "Tinguian"},
    {"title": "The Alligator's Fruit", "group": "tinguian", "sub": "Tinguian"},
    {"title": "Dogedog", "group": "tinguian", "sub": "Tinguian"},
    # Igorot
    {"title": "The Creation", "group": "igorot", "sub": "Igorot"},
    {"title": "The Flood Story", "group": "igorot", "sub": "Igorot"},
    {"title": "Lumawig on Earth", "group": "igorot", "sub": "Igorot"},
    {"title": "How the First Head Was Taken", "group": "igorot", "sub": "Igorot"},
    {"title": "The Serpent Eagle", "group": "igorot", "sub": "Igorot"},
    {"title": "The Tattooed Men", "group": "igorot", "sub": "Igorot"},
    {"title": "Tilin, the Rice Bird", "group": "igorot", "sub": "Igorot"},
    # Wild Tribes of Mindanao - Bukidnon
    {"title": "How the Moon and Stars Came to Be", "group": "mindanao", "sub": "Bukidnon"},
    {"title": "The Flood Story", "group": "mindanao", "sub": "Bukidnon"},
    {"title": "Magbangal", "group": "mindanao", "sub": "Bukidnon"},
    {"title": "How Children Became Monkeys", "group": "mindanao", "sub": "Bukidnon"},
    {"title": "Bulanawan and Aguio", "group": "mindanao", "sub": "Bukidnon"},
    # Bagobo
    {"title": "Origin", "group": "mindanao", "sub": "Bagobo"},
    {"title": "Lumabet", "group": "mindanao", "sub": "Bagobo"},
    # Bilaan
    {"title": "The Story of the Creation", "group": "mindanao", "sub": "Bilaan"},
    {"title": "In the Beginning", "group": "mindanao", "sub": "Bilaan"},
    # Mandaya
    {"title": "The Children of the Limokon", "group": "mindanao", "sub": "Mandaya"},
    {"title": "The Sun and the Moon", "group": "mindanao", "sub": "Mandaya"},
    # Subanun
    {"title": "The Widow's Son", "group": "mindanao", "sub": "Subanun"},
    # Moro
    {"title": "Mythology of Mindanao", "group": "moro", "sub": "Moro"},
    {"title": "The Story of Bantugan", "group": "moro", "sub": "Moro"},
    # Christianized Tribes - Ilocano
    {"title": "The Monkey and the Turtle", "group": "christian", "sub": "Ilocano"},
    {"title": "The Poor Fisherman and His Wife", "group": "christian", "sub": "Ilocano"},
    {"title": "The Presidente Who Had Horns", "group": "christian", "sub": "Ilocano"},
    {"title": "The Story of a Monkey", "group": "christian", "sub": "Ilocano"},
    {"title": "The White Squash", "group": "christian", "sub": "Ilocano"},
    # Tagalog
    {"title": "The Creation Story", "group": "christian", "sub": "Tagalog"},
    {"title": "The Story of Benito", "group": "christian", "sub": "Tagalog"},
    {"title": "The Adventures of Juan", "group": "christian", "sub": "Tagalog"},
    {"title": "Juan Gathers Guavas", "group": "christian", "sub": "Tagalog"},
    # Visayan
    {"title": "The Sun and the Moon", "group": "christian", "sub": "Visayan"},
    {"title": "The First Monkey", "group": "christian", "sub": "Visayan"},
    {"title": "The Virtue of the Cocoanut", "group": "christian", "sub": "Visayan"},
    {"title": "Mansumandig", "group": "christian", "sub": "Visayan"},
    {"title": "Why Dogs Wag Their Tails", "group": "christian", "sub": "Visayan"},
    {"title": "The Hawk and the Hen", "group": "christian", "sub": "Visayan"},
    {"title": "The Spider and the Fly", "group": "christian", "sub": "Visayan"},
    {"title": "The Battle of the Crabs", "group": "christian", "sub": "Visayan"},
]


def read_seed():
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    lines = text.split("\n")
    start_idx = 0
    end_idx = len(lines)
    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i + 1
            break
    for i, line in enumerate(lines):
        if end_marker in line:
            end_idx = i
            break
    return "\n".join(lines[start_idx:end_idx])


def strip_footnotes(text):
    """Remove footnote markers like [1], [2]."""
    return re.sub(r'\s*\[\d+\]', '', text)


def make_id(title, group, sub):
    """Create a unique ID from title, handling duplicates via group prefix."""
    base = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    # Some titles repeat across groups (e.g., "The Flood Story", "The Sun and the Moon")
    # Prefix with sub-group to disambiguate
    return f"{sub.lower()}-{base}"


def find_story_positions(text):
    """Find the position of each story in the text by matching title lines."""
    lines = text.split("\n")

    # Find the start of actual stories (after preface/TOC)
    # Stories start after the first group marker "TINGUIAN"
    story_start_line = 0
    for i, line in enumerate(lines):
        if line.strip() == "TINGUIAN":
            story_start_line = i
            break

    # Find end of stories (Pronunciation section)
    story_end_line = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == "Pronunciation of Philippine Names" and i > story_start_line:
            story_end_line = i
            break

    # For each story, find its title line in the text
    positions = []
    used_lines = set()

    for story_idx, story in enumerate(STORIES):
        title = story["title"]
        found = False

        for i in range(story_start_line, story_end_line):
            if i in used_lines:
                continue
            stripped = lines[i].strip()
            # Case-insensitive match, also handle minor variations (e.g., "The Story of the Tikgi")
            if stripped.lower() == title.lower() or (
                title.lower() in stripped.lower() and
                len(stripped) <= len(title) + 10 and
                len(stripped) >= len(title) - 5
            ):
                # Verify: for stories that appear multiple times (like "The Flood Story"),
                # check that the tribal attribution nearby matches
                # Look for _Sub_ marker within a few lines
                sub = story["sub"]
                nearby_has_sub = False
                for j in range(max(0, i - 5), min(len(lines), i + 5)):
                    if f"_{sub}_" in lines[j] or lines[j].strip() == f"_{sub}_":
                        nearby_has_sub = True
                        break

                # Also check if we're in the right group section
                in_right_section = False
                group_markers = {
                    "tinguian": "TINGUIAN",
                    "igorot": "IGOROT",
                    "mindanao": "WILD TRIBES OF MINDANAO",
                    "moro": "MORO",
                    "christian": "CHRISTIANIZED TRIBES"
                }
                marker = group_markers[story["group"]]
                # Look backward to find which section we're in
                for j in range(i, story_start_line - 1, -1):
                    if lines[j].strip() in group_markers.values():
                        if lines[j].strip() == marker:
                            in_right_section = True
                        break

                if in_right_section:
                    positions.append((i, story_idx))
                    used_lines.add(i)
                    found = True
                    break

        if not found:
            print(f"WARNING: Could not find story: '{title}' ({story['sub']})")

    # Sort by position
    positions.sort(key=lambda x: x[0])
    return positions, lines, story_start_line, story_end_line


def extract_stories(text):
    """Extract all stories from the text."""
    positions, lines, story_start_line, story_end_line = find_story_positions(text)

    stories = []
    for pos_idx, (line_num, story_idx) in enumerate(positions):
        story_def = STORIES[story_idx]

        # Find end: next story's title line or group marker or end
        if pos_idx + 1 < len(positions):
            end_line = positions[pos_idx + 1][0]
            # Back up past group markers and introductions
        else:
            end_line = story_end_line

        # Also check for group markers between this story and the next
        # to avoid capturing introductions of the next group
        for i in range(line_num + 1, end_line):
            stripped = lines[i].strip()
            if stripped in ("TINGUIAN", "IGOROT", "WILD TRIBES OF MINDANAO", "MORO", "CHRISTIANIZED TRIBES"):
                end_line = i
                break

        # Extract content, skipping title and tribal attribution lines
        content_start = line_num + 1
        while content_start < end_line and lines[content_start].strip() == "":
            content_start += 1
        # Skip tribal attribution (e.g., "_Tinguian_")
        if content_start < end_line and re.match(r'^_[A-Za-z]+_$', lines[content_start].strip()):
            content_start += 1
        while content_start < end_line and lines[content_start].strip() == "":
            content_start += 1

        story_text = "\n".join(lines[content_start:end_line]).strip()
        story_text = strip_footnotes(story_text)
        story_text = re.sub(r'\n{3,}', '\n\n', story_text)

        stories.append({
            "title": story_def["title"],
            "group": story_def["group"],
            "sub": story_def["sub"],
            "text": story_text,
            "id": make_id(story_def["title"], story_def["group"], story_def["sub"])
        })

    return stories


# Group definitions for L2
GROUPS = {
    "tinguian": {
        "name": "Tinguian Stories",
        "about": "The Tinguian inhabit the rugged mountains of northwestern Luzon. Their stories are the largest collection here — tales of the 'first times' when heroes had magical powers, talked with jars, created humans from betel-nuts, and married star-maidens. The characters Aponitolau and Aponibolinayen appear again and again, along with the fearsome warrior Gawigawen. These are not fairy tales but the living mythology of a people who still commune with spirits.",
        "for_readers": "The Tinguian tales divide into epic myths of the first heroes (stories 1-8), origin legends explaining customs and crafts (9-16), and animal fables told for amusement and instruction (17-23). The epic myths are densely allusive — characters transform, names shift, and the supernatural is woven into every action."
    },
    "igorot": {
        "name": "Igorot Stories",
        "about": "The Igorot are neighbors of the Tinguian, living further south and east in the mountains of Luzon. Their stories center on Lumawig, the great spirit who walked the earth in human form — creating the world, teaching the people, and establishing the customs of head-hunting and rice cultivation. The Igorot creation and flood stories show striking parallels to traditions found across the Pacific.",
        "for_readers": "The Igorot tales are shorter and more mythological than the Tinguian epics. Lumawig is a fascinating figure — a creator-god who is also a trickster, who punishes disobedience but also takes human wives and has very human emotions. The flood story and creation tale are among the most vivid origin myths in Philippine folklore."
    },
    "mindanao": {
        "name": "Wild Tribes of Mindanao",
        "about": "Five distinct peoples of the great southern island of Mindanao contribute these tales: the Bukidnon (mountain dwellers), the Bagobo (brass-workers), the Bilaan (bead-makers), the Mandaya, and the Subanun. Their creation stories, flood myths, and origin tales show both common Austronesian themes and unique local variations — the moon beaten by the sun, children turned to monkeys, and the limokon bird as divine messenger.",
        "for_readers": "These are some of the most striking origin stories in the collection — how the moon got her scars, how children became monkeys through disobedience, why certain birds are sacred. Each tribe has its own version of creation, and comparing them reveals shared patterns across the Philippine archipelago."
    },
    "moro": {
        "name": "Moro Stories",
        "about": "The Moro are the Islamicized peoples of the southern Philippines — former warriors and seafarers whose mythology blends ancient Malay tradition with Islamic influence. The mythology of Mindanao and the epic of Bantugan — a prince so beautiful that even the gods desire him — show a literary tradition quite different from the northern mountain peoples.",
        "for_readers": "The Moro tales are more elaborate and courtly than those of the hill tribes. The story of Bantugan is a full epic, with the hero dying and being restored to life, traveling through enchanted realms, and confronting jealous kings. It represents a sophisticated oral literary tradition."
    },
    "christian": {
        "name": "Christianized Tribes",
        "about": "The coastal peoples of the Philippines — Ilocano, Tagalog, and Visayan — were the first to encounter Spanish colonialism and Christianity. Their folk tales show a fascinating mixture of indigenous beliefs and foreign influence: animal trickster tales (the monkey and the turtle), origin myths (how the first monkey came to be), and adventure stories featuring Juan, the Filipino Everyman who outwits the powerful through cleverness.",
        "for_readers": "These tales are the most accessible in the collection — shorter, funnier, and more clearly structured as fables with morals. They are excellent for reading aloud. Notice how many feature contests between the clever and the strong, the small and the large — the monkey vs. the turtle, the hawk vs. the hen. The Juan tales are a Philippine folk tradition that parallels the trickster cycles found across Southeast Asia."
    }
}


def build_grammar():
    raw_text = read_seed()
    text = strip_gutenberg(raw_text)
    stories = extract_stories(text)

    print(f"Extracted {len(stories)} stories")

    items = []
    sort_order = 0
    group_ids = {g: [] for g in GROUPS}

    # L1: Individual stories
    for story in stories:
        item_id = story["id"]
        group_ids[story["group"]].append(item_id)

        keywords = [story["sub"].lower()]
        text_lower = story["text"].lower()
        for kw in ["creation", "flood", "sun", "moon", "spirit", "magic", "animal",
                    "monkey", "turtle", "bird", "fish", "giant", "hero"]:
            if kw in text_lower:
                keywords.append(kw)

        items.append({
            "id": item_id,
            "name": story["title"],
            "sort_order": sort_order,
            "category": story["group"],
            "level": 1,
            "sections": {
                "Story": story["text"],
                "Tribal Source": f"{story['sub']} people of the Philippines"
            },
            "keywords": keywords,
            "metadata": {
                "tribal_group": story["sub"],
                "region_group": story["group"]
            }
        })
        sort_order += 1

    # L2: Tribal group groupings
    l2_ids = []
    for group_key, group_def in GROUPS.items():
        group_id = f"group-{group_key}"
        l2_ids.append(group_id)
        composite = group_ids.get(group_key, [])

        items.append({
            "id": group_id,
            "name": group_def["name"],
            "sort_order": sort_order,
            "category": "tribal-group",
            "level": 2,
            "sections": {
                "About": group_def["about"],
                "For Readers": group_def["for_readers"]
            },
            "keywords": [],
            "metadata": {},
            "composite_of": composite,
            "relationship_type": "emergence"
        })
        sort_order += 1

    # L2: Thematic groupings across tribes
    # Creation & Origin stories
    creation_ids = [s["id"] for s in stories if any(w in s["title"].lower() for w in
        ["creation", "origin", "beginning", "how the moon", "how children", "first monkey",
         "flood", "children of the limokon"])]

    items.append({
        "id": "theme-creation-origins",
        "name": "Creation and Origin Stories",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "Creation and origin stories from across the Philippine archipelago — how the world was made, how the flood came, how the moon got her scars, how monkeys came from children, and where the people themselves originated. Comparing these tales across tribes reveals shared Austronesian creation patterns while showing each people's unique imagination.",
            "For Readers": "Read these creation stories side by side to see how different peoples answer the same fundamental questions: Where did we come from? Why is the world the way it is? Notice the recurring flood motif — found in nearly every Philippine tribe — and the theme of transformation between human and animal forms."
        },
        "keywords": ["creation", "origin", "flood", "cosmogony"],
        "metadata": {},
        "composite_of": creation_ids,
        "relationship_type": "emergence"
    })
    l2_ids.append("theme-creation-origins")
    sort_order += 1

    # Animal fables
    animal_ids = [s["id"] for s in stories if any(w in s["title"].lower() for w in
        ["monkey", "turtle", "carabao", "shell", "alligator", "hawk", "hen", "spider",
         "fly", "crab", "dog", "eagle", "bird", "tilin"])]

    items.append({
        "id": "theme-animal-fables",
        "name": "Animal Fables and Trickster Tales",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "sections": {
            "About": "Animal fables from across the Philippines — the monkey's tricks, the turtle's patience, the hawk's bargain with the hen, the spider's trap for the fly. These stories are told to amuse children and teach moral lessons, and many show connections to fable traditions across Southeast Asia and even Europe.",
            "For Readers": "These are the lightest and most entertaining tales in the collection. Many feature a contest between cleverness and brute force, or between patience and greed. They are perfect for reading aloud to children, and for comparing with Aesop's Fables or the Jataka tales."
        },
        "keywords": ["animals", "fable", "trickster", "moral"],
        "metadata": {},
        "composite_of": animal_ids,
        "relationship_type": "emergence"
    })
    l2_ids.append("theme-animal-fables")
    sort_order += 1

    # L3: Meta
    meta_item = {
        "id": "philippine-folk-tales-meta",
        "name": "Philippine Folk Tales",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Philippine Folk Tales, compiled and annotated by Mabel Cook Cole (1916), drawn from four years of fieldwork among the wild tribes and Christianized peoples of the Philippine Islands. Sixty-two tales from five cultural groups — Tinguian, Igorot, the Wild Tribes of Mindanao (Bukidnon, Bagobo, Bilaan, Mandaya, Subanun), Moro, and the Christianized coastal tribes (Ilocano, Tagalog, Visayan). A remarkable collection spanning creation myths, epic hero tales, origin legends, and animal fables from one of the world's most culturally diverse archipelagos.",
            "For Readers": "This collection maps the extraordinary diversity of Philippine oral tradition — from the shamanic epics of the Tinguian mountain people to the courtly romance of the Moro to the trickster fables of the Christianized coast. Read it as a journey through the islands: north to south, mountain to sea, ancient to modern. The tales reveal a world where spirits inhabit every tree and stone, where heroes fly through the air and talk with jars, and where the boundary between human and animal is always permeable."
        },
        "keywords": ["philippine", "folklore", "tinguian", "igorot", "moro", "creation-myth", "fables"],
        "metadata": {},
        "composite_of": l2_ids,
        "relationship_type": "emergence"
    }
    items.append(meta_item)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Mabel Cook Cole", "date": "1916", "note": "Compiler and annotator"},
                {"name": "Philippine oral traditions", "date": "traditional", "note": "Tinguian, Igorot, Bukidnon, Bagobo, Bilaan, Mandaya, Subanun, Moro, Ilocano, Tagalog, Visayan peoples"}
            ]
        },
        "name": "Philippine Folk Tales",
        "description": "Philippine Folk Tales, compiled and annotated by Mabel Cook Cole (1916), from four years of fieldwork among the tribes of the Philippine Islands. Sixty-two tales from five cultural groups spanning creation myths, shamanic epics, hero legends, and animal fables — the Tinguian heroes of the 'first times,' the Igorot creator-spirit Lumawig, the Moro prince Bantugan, and the trickster animal tales of the coastal peoples. One of the most important early collections of Philippine oral literature.\n\nSource: Project Gutenberg eBook #12814 (https://www.gutenberg.org/ebooks/12814)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: The original 1916 A.C. McClurg edition includes photographs of Philippine tribal life. Dean C. Worcester's photographs of Philippine peoples (1898-1914, National Geographic). Charles Martin's hand-tinted photographs of the Philippines (early 1900s, National Geographic).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["folklore", "philippine", "indigenous", "creation-myth", "fables", "shamanism", "public-domain", "full-text"],
        "roots": ["indigenous-mythology"],
        "shelves": ["earth"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"Generated {OUTPUT_FILE}")
    print(f"  L1 items (stories): {l1}")
    print(f"  L2 items (groups + themes): {l2}")
    print(f"  L3 items (meta): {l3}")
    print(f"  Total items: {len(items)}")

    # Group breakdown
    for group_key in GROUPS:
        count = len(group_ids.get(group_key, []))
        print(f"  {GROUPS[group_key]['name']}: {count} stories")


if __name__ == "__main__":
    build_grammar()
