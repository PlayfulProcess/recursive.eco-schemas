#!/usr/bin/env python3
"""
Parser for Folk-Lore and Legends: North American Indian (Anonymous, Project Gutenberg #22072).
Outputs grammar.json into grammars/folklore-north-american-indian/
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'folklore-north-american-indian.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'folklore-north-american-indian')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

# Story definitions: title as it appears in text, clean id, display name, keywords, thematic categories
STORY_DEFS = [
    {
        "title": "MOOWIS.",
        "id": "moowis",
        "name": "Moowis",
        "keywords": ["vanity", "pride", "love", "ice", "melting", "punishment"],
        "themes": ["love-and-vanity", "transformation"],
        "reflection": "A beautiful woman scorns all suitors until she falls in love with a figure made of snow and rags. What does this tale say about the dangers of pride and the tricks that desire can play on us?"
    },
    {
        "title": "THE GIRL WHO MARRIED THE PINE-TREE.",
        "id": "girl-who-married-pine-tree",
        "name": "The Girl Who Married the Pine-Tree",
        "keywords": ["marriage", "nature", "pine-tree", "spirits", "escape"],
        "themes": ["nature-spirits", "love-and-vanity"],
        "reflection": "Leelinau chooses the spirit of a tree over a human suitor. What does it mean to find kinship with the natural world rather than with human society?"
    },
    {
        "title": "A LEGEND OF MANABOZHO.",
        "id": "legend-of-manabozho",
        "name": "A Legend of Manabozho",
        "keywords": ["manabozho", "creation", "wolf", "spirits", "lake", "flood"],
        "themes": ["creation-and-origins", "trickster-tales"],
        "reflection": "Manabozho creates the land after losing his adopted wolf-son to water spirits. How does grief become the catalyst for world-making in this myth?"
    },
    {
        "title": "PAUPPUKKEEWIS.",
        "id": "pauppukkeewis",
        "name": "Pauppukkeewis",
        "keywords": ["pauppukkeewis", "trickster", "dance", "transformation", "chase", "manabozho"],
        "themes": ["trickster-tales", "transformation"],
        "reflection": "The wild dancer Pauppukkeewis causes chaos and transforms himself again and again to escape Manabozho's wrath. What is the nature of the trickster who cannot stop testing boundaries?"
    },
    {
        "title": "THE DISCOVERY OF THE UPPER WORLD.",
        "id": "discovery-of-upper-world",
        "name": "The Discovery of the Upper World",
        "keywords": ["upper-world", "sky", "discovery", "climbing", "spirits"],
        "themes": ["creation-and-origins", "spirit-world"],
        "reflection": "What compels human beings to seek what lies beyond the visible sky? This tale of ascending to another world mirrors the eternal human urge to know what is above and beyond."
    },
    {
        "title": "THE BOY WHO SNARED THE SUN.",
        "id": "boy-who-snared-sun",
        "name": "The Boy Who Snared the Sun",
        "keywords": ["sun", "snare", "boy", "dormouse", "light", "darkness"],
        "themes": ["creation-and-origins", "heroes-and-quests"],
        "reflection": "A tiny boy traps the sun itself. Sometimes the smallest and most overlooked among us can accomplish what the mightiest cannot."
    },
    {
        "title": "THE MAID IN THE BOX.",
        "id": "maid-in-the-box",
        "name": "The Maid in the Box",
        "keywords": ["maid", "box", "guardian", "marriage", "trial"],
        "themes": ["love-and-vanity", "heroes-and-quests"],
        "reflection": "A mysterious maiden is kept hidden in a box, only to be won by the right suitor. What does it mean to keep beauty or truth locked away, and who has the right to release it?"
    },
    {
        "title": "THE SPIRITS AND THE LOVERS.",
        "id": "spirits-and-lovers",
        "name": "The Spirits and the Lovers",
        "keywords": ["spirits", "lovers", "death", "mourning", "journey", "afterlife"],
        "themes": ["spirit-world", "love-and-vanity"],
        "reflection": "A bereaved lover follows the spirit of the beloved into the land of the dead. Can love truly cross the boundary between worlds?"
    },
    {
        "title": "THE WONDERFUL ROD.",
        "id": "wonderful-rod",
        "name": "The Wonderful Rod",
        "keywords": ["rod", "magic", "hunting", "power", "gift"],
        "themes": ["heroes-and-quests", "nature-spirits"],
        "reflection": "A magical rod grants extraordinary power. But what responsibilities come with such gifts, and what happens when we rely on magic rather than our own strength?"
    },
    {
        "title": "THE FUNERAL FIRE.",
        "id": "funeral-fire",
        "name": "The Funeral Fire",
        "keywords": ["funeral", "fire", "death", "spirit", "journey", "afterlife"],
        "themes": ["spirit-world", "creation-and-origins"],
        "reflection": "The funeral fire lights the way for the departed spirit. This tale illuminates the care and reverence with which the dead were honored and guided on their final journey."
    },
    {
        "title": "THE LEGEND OF O-NA-WUT-A-QUT-O.",
        "id": "legend-of-onawutaquto",
        "name": "The Legend of O-na-wut-a-qut-o",
        "keywords": ["onawutaquto", "sky", "star", "wife", "journey"],
        "themes": ["spirit-world", "love-and-vanity"],
        "reflection": "A man journeys to the sky world seeking his star-wife. The boundaries between earth and sky, mortal and immortal, are thinner than we think."
    },
    {
        "title": "MANABOZHO IN THE FISH'S STOMACH.",
        "id": "manabozho-in-fishs-stomach",
        "name": "Manabozho in the Fish's Stomach",
        "keywords": ["manabozho", "fish", "swallowed", "escape", "trickster"],
        "themes": ["trickster-tales", "heroes-and-quests"],
        "reflection": "Swallowed by a great fish, Manabozho must use his wits to escape from within. Sometimes the only way out is through."
    },
    {
        "title": "THE SUN AND THE MOON.",
        "id": "sun-and-moon",
        "name": "The Sun and the Moon",
        "keywords": ["sun", "moon", "sky", "origins", "celestial"],
        "themes": ["creation-and-origins"],
        "reflection": "How did the sun and moon come to share the sky? Origin stories of the celestial bodies remind us that even the most constant things in our lives have their own mysterious beginnings."
    },
    {
        "title": "THE SNAIL AND THE BEAVER.",
        "id": "snail-and-beaver",
        "name": "The Snail and the Beaver",
        "keywords": ["snail", "beaver", "animals", "contest", "cleverness"],
        "themes": ["animal-tales", "trickster-tales"],
        "reflection": "The slow snail and the industrious beaver — what happens when very different creatures must contend with one another? Cleverness takes many forms."
    },
    {
        "title": "THE STRANGE GUESTS.",
        "id": "strange-guests",
        "name": "The Strange Guests",
        "keywords": ["guests", "hospitality", "spirits", "supernatural", "feast"],
        "themes": ["spirit-world", "animal-tales"],
        "reflection": "Strange visitors arrive bearing gifts and mysteries. In many traditions, the stranger at the door may be a spirit in disguise — how we treat them reveals who we truly are."
    },
    {
        "title": "MANABOZHO AND HIS TOE.",
        "id": "manabozho-and-his-toe",
        "name": "Manabozho and His Toe",
        "keywords": ["manabozho", "toe", "trickster", "humor", "body"],
        "themes": ["trickster-tales"],
        "reflection": "Even the great Manabozho can be undone by something as small as his own toe. The trickster's body is often his greatest source of comedy and humiliation."
    },
    {
        "title": "THE GIRL WHO BECAME A BIRD.",
        "id": "girl-who-became-bird",
        "name": "The Girl Who Became a Bird",
        "keywords": ["girl", "bird", "transformation", "flight", "escape"],
        "themes": ["transformation", "nature-spirits"],
        "reflection": "A girl transforms into a bird and gains the freedom of flight. What do we gain and what do we lose when we leave our human form behind?"
    },
    {
        "title": "THE UNDYING HEAD.",
        "id": "undying-head",
        "name": "The Undying Head",
        "keywords": ["head", "undying", "warrior", "magic", "revenge", "brother", "sister"],
        "themes": ["heroes-and-quests", "spirit-world"],
        "reflection": "A severed head that will not die, sustained by the love of a faithful sister. This haunting tale explores the bonds of family loyalty and the power of the spirit to endure beyond bodily destruction."
    },
    {
        "title": "THE OLD CHIPPEWAY.",
        "id": "old-chippeway",
        "name": "The Old Chippeway",
        "keywords": ["old-man", "chippeway", "wisdom", "age", "journey"],
        "themes": ["heroes-and-quests"],
        "reflection": "An old man's journey reveals the wisdom that comes only with age and experience. What can the young learn from those who have walked the longest paths?"
    },
    {
        "title": "MUKUMIK! MUKUMIK! MUKUMIK!",
        "id": "mukumik",
        "name": "Mukumik! Mukumik! Mukumik!",
        "keywords": ["mukumik", "spirit", "call", "fear", "supernatural"],
        "themes": ["spirit-world"],
        "reflection": "The eerie cry of 'Mukumik!' echoes through the night. Some spirits announce themselves before they arrive — the question is whether we have the courage to face them."
    },
    {
        "title": "THE SWING BY THE LAKE.",
        "id": "swing-by-the-lake",
        "name": "The Swing by the Lake",
        "keywords": ["swing", "lake", "maiden", "danger", "trickery"],
        "themes": ["love-and-vanity", "heroes-and-quests"],
        "reflection": "A swing by a beautiful lake becomes a place of danger and enchantment. Beauty and peril are often found in the same place."
    },
    {
        "title": "THE FIRE PLUME.",
        "id": "fire-plume",
        "name": "The Fire Plume",
        "keywords": ["fire", "plume", "quest", "magic", "warrior"],
        "themes": ["heroes-and-quests", "nature-spirits"],
        "reflection": "The fire plume burns with a light that cannot be extinguished. What inner fire sustains us through our darkest quests?"
    },
    {
        "title": "THE JOURNEY TO THE ISLAND OF SOULS.",
        "id": "journey-to-island-of-souls",
        "name": "The Journey to the Island of Souls",
        "keywords": ["island", "souls", "afterlife", "journey", "death", "spirits"],
        "themes": ["spirit-world"],
        "reflection": "The Island of Souls lies across water that the living cannot easily cross. This tale maps the geography of the afterlife with the precision of a traveler who has glimpsed the other shore."
    },
    {
        "title": "MACHINITOU, THE EVIL SPIRIT.",
        "id": "machinitou-evil-spirit",
        "name": "Machinitou, the Evil Spirit",
        "keywords": ["machinitou", "evil", "spirit", "darkness", "danger", "battle"],
        "themes": ["spirit-world", "heroes-and-quests"],
        "reflection": "The Evil Spirit tests human courage and endurance. In facing Machinitou, the hero confronts the darkest forces of the spirit world — and discovers what lies within."
    },
    {
        "title": "THE WOMAN OF STONE.",
        "id": "woman-of-stone",
        "name": "The Woman of Stone",
        "keywords": ["stone", "woman", "transformation", "petrification", "spirit"],
        "themes": ["transformation", "nature-spirits"],
        "reflection": "To become stone is to become eternal but unfeeling. What does it mean when a living being is turned to rock — is it imprisonment or preservation?"
    },
    {
        "title": "THE MAIDEN WHO LOVED A FISH.",
        "id": "maiden-who-loved-fish",
        "name": "The Maiden Who Loved a Fish",
        "keywords": ["maiden", "fish", "love", "water", "interspecies", "nature"],
        "themes": ["love-and-vanity", "nature-spirits"],
        "reflection": "A maiden falls in love with a creature of the water. Love does not respect the boundaries between species, between elements, between worlds."
    },
    {
        "title": "THE LONE LIGHTNING.",
        "id": "lone-lightning",
        "name": "The Lone Lightning",
        "keywords": ["lightning", "thunder", "power", "sky", "storm"],
        "themes": ["nature-spirits", "heroes-and-quests"],
        "reflection": "Lightning strikes alone, sudden and brilliant. This tale captures the raw power of the storm and its meaning in the lives of those who lived beneath open skies."
    },
    {
        "title": "AGGO-DAH-GAUDA.",
        "id": "aggo-dah-gauda",
        "name": "Aggo-dah-gauda",
        "keywords": ["aggo-dah-gauda", "giant", "strength", "adventure", "spirit"],
        "themes": ["heroes-and-quests", "spirit-world"],
        "reflection": "Aggo-dah-gauda's story is one of extraordinary strength and spiritual encounter. What does it take to walk between the worlds of the seen and the unseen?"
    },
    {
        "title": "PIQUA.",
        "id": "piqua",
        "name": "Piqua",
        "keywords": ["piqua", "warrior", "adventure", "trial", "spirit"],
        "themes": ["heroes-and-quests", "spirit-world"],
        "reflection": "Piqua faces trials that test every aspect of character. The hero's journey demands not just strength, but wisdom, patience, and humility."
    },
    {
        "title": "THE EVIL MAKER.",
        "id": "evil-maker",
        "name": "The Evil Maker",
        "keywords": ["evil", "maker", "creation", "destruction", "duality"],
        "themes": ["creation-and-origins", "spirit-world"],
        "reflection": "Behind every act of creation stands the shadow of destruction. The Evil Maker reminds us that the forces that shape the world are not all benevolent."
    },
    {
        "title": "MANABOZHO THE WOLF.",
        "id": "manabozho-the-wolf",
        "name": "Manabozho the Wolf",
        "keywords": ["manabozho", "wolf", "trickster", "hunting", "transformation"],
        "themes": ["trickster-tales", "animal-tales"],
        "reflection": "Manabozho takes the form of a wolf, blurring the line between human and animal. The trickster teaches us that identity is fluid and the boundaries between beings are more porous than we imagine."
    },
    {
        "title": "THE MAN-FISH.",
        "id": "man-fish",
        "name": "The Man-Fish",
        "keywords": ["man-fish", "sea", "migration", "singing", "wonder"],
        "themes": ["transformation", "creation-and-origins"],
        "reflection": "A being half-man, half-fish emerges from the water singing beautiful songs. The Man-Fish bridges two worlds — the deep and the surface — reminding us that the boundaries of our world are not fixed."
    },
]

# Theme groupings for L2
THEME_GROUPS = [
    {
        "id": "theme-trickster-tales",
        "name": "Trickster Tales: Manabozho and Pauppukkeewis",
        "category": "themes",
        "about": "The trickster is one of the most important figures in North American Indian mythology. Manabozho — culture hero, world-maker, and fool — appears again and again, sometimes creating the world, sometimes being swallowed by a fish, sometimes losing a fight with his own toe. Pauppukkeewis is the wild dancer whose transformations cannot save him from the consequences of his mischief. These tales celebrate wit, cunning, and the cosmic humor of beings who are both divine and ridiculous.",
        "for_readers": "The trickster teaches through laughter and through failure. Notice how Manabozho is never entirely heroic or entirely foolish — he is both, simultaneously. These stories invite us to embrace the contradictions within ourselves.",
        "member_ids": ["legend-of-manabozho", "pauppukkeewis", "manabozho-in-fishs-stomach", "manabozho-and-his-toe", "snail-and-beaver", "manabozho-the-wolf"],
        "keywords": ["trickster", "manabozho", "pauppukkeewis", "humor", "cunning"]
    },
    {
        "id": "theme-spirit-world",
        "name": "The Spirit World and the Afterlife",
        "category": "themes",
        "about": "Many of these tales map the geography of the spirit world — the Island of Souls, the Upper World, the realm of ghosts and supernatural beings. The dead are not gone but dwelling elsewhere, accessible through ceremony, dreams, and the funeral fire. These stories reveal a cosmology in which the boundary between living and dead is thin, and the spirits of the departed remain intimately connected to the world of the living.",
        "for_readers": "These tales offer a vision of death as a journey rather than an ending. The spirit world is not distant but woven into the fabric of daily life. Consider how these stories might change the way you think about loss, memory, and the presence of those who have passed.",
        "member_ids": ["spirits-and-lovers", "funeral-fire", "discovery-of-upper-world", "legend-of-onawutaquto", "journey-to-island-of-souls", "machinitou-evil-spirit", "mukumik", "strange-guests"],
        "keywords": ["spirits", "afterlife", "death", "souls", "ghost", "supernatural"]
    },
    {
        "id": "theme-creation-and-origins",
        "name": "Creation and Origins",
        "category": "themes",
        "about": "How did the world come to be? How did the sun and moon take their places in the sky? Why do certain animals behave as they do? These origin stories answer the most fundamental questions through narrative rather than explanation. The world is created not by abstract forces but by beings who act, desire, grieve, and transform.",
        "for_readers": "Origin stories are not merely fanciful explanations — they are ways of relating to the world as alive, intentional, and meaningful. Each one invites you to see the natural world not as a collection of objects but as a community of beings with their own histories.",
        "member_ids": ["legend-of-manabozho", "boy-who-snared-sun", "sun-and-moon", "evil-maker", "man-fish"],
        "keywords": ["creation", "origins", "world-making", "sun", "moon"]
    },
    {
        "id": "theme-transformation",
        "name": "Transformation and Shape-Shifting",
        "category": "themes",
        "about": "Transformation is everywhere in these tales — girls become birds, tricksters become animals, a man becomes half-fish, a woman becomes stone. Shape-shifting is not just a magical trick but a reflection of the deep animist understanding that identity is fluid, that the boundaries between human, animal, and spirit are permeable, and that change is the fundamental nature of existence.",
        "for_readers": "In a world where a girl can become a bird and a man can become a wolf, what does identity really mean? These stories challenge the modern assumption that we are fixed, unchanging selves. Consider what transformations you have undergone in your own life.",
        "member_ids": ["pauppukkeewis", "girl-who-became-bird", "woman-of-stone", "man-fish", "girl-who-married-pine-tree"],
        "keywords": ["transformation", "shape-shifting", "metamorphosis", "change"]
    },
    {
        "id": "theme-love-and-vanity",
        "name": "Love, Desire, and Vanity",
        "category": "themes",
        "about": "Love in these tales is rarely simple. A proud woman falls for a figure made of snow. A maiden loves a fish. A girl chooses a tree over a human suitor. These stories explore the unpredictable, often dangerous nature of desire, and the way vanity and pride can lead us into traps of our own making.",
        "for_readers": "These tales treat love and desire with remarkable honesty. Love is not always wise, not always safe, and not always between the beings we expect. What do these stories tell us about the wildness at the heart of desire?",
        "member_ids": ["moowis", "girl-who-married-pine-tree", "maiden-who-loved-fish", "spirits-and-lovers", "maid-in-the-box", "swing-by-the-lake", "legend-of-onawutaquto"],
        "keywords": ["love", "desire", "vanity", "pride", "marriage"]
    },
    {
        "id": "theme-heroes-and-quests",
        "name": "Heroes and Quests",
        "category": "themes",
        "about": "The heroes of these tales face trials of endurance, courage, and cunning. They snare the sun, fight evil spirits, carry undying heads, and journey to the Island of Souls. Unlike the heroes of many Western traditions, these figures often succeed through patience, humility, and spiritual power rather than brute force.",
        "for_readers": "Notice how heroism in these stories often looks different from the sword-swinging warriors of European myth. The greatest feats are accomplished through spiritual strength, cleverness, and the willingness to endure. What kind of heroism does your own life demand?",
        "member_ids": ["boy-who-snared-sun", "undying-head", "fire-plume", "old-chippeway", "aggo-dah-gauda", "piqua", "machinitou-evil-spirit", "lone-lightning", "wonderful-rod"],
        "keywords": ["hero", "quest", "trial", "courage", "endurance"]
    },
    {
        "id": "theme-nature-spirits",
        "name": "Nature Spirits and the Living World",
        "category": "themes",
        "about": "Trees speak, stones come alive, lightning has personality, and fish are lovers. In these tales, the natural world is not a backdrop to human drama but a community of beings with their own intentions, powers, and relationships. This animist worldview treats rivers, mountains, and animals as persons deserving respect and capable of reciprocity.",
        "for_readers": "These stories invite us into a relationship with the natural world that modern life has largely abandoned. What would it mean to treat the trees, rivers, and animals around you as beings with their own stories and their own spirits?",
        "member_ids": ["girl-who-married-pine-tree", "woman-of-stone", "maiden-who-loved-fish", "lone-lightning", "fire-plume", "girl-who-became-bird", "wonderful-rod"],
        "keywords": ["nature", "spirits", "animism", "trees", "animals", "elements"]
    },
]

# L3 meta-categories
L3_DEFS = [
    {
        "id": "meta-themes",
        "name": "Themes and Teachings",
        "category": "meta",
        "about": "The great thematic currents running through North American Indian folklore: the trickster's cosmic comedy, the thin veil between living and dead, the fluid boundaries of identity, the wildness of love, the nature of heroism, and the living spirit of the natural world. These groupings reveal a cosmology in which everything is connected, everything is alive, and every story carries medicine for the soul.",
        "composite_of": [
            "theme-trickster-tales",
            "theme-spirit-world",
            "theme-creation-and-origins",
            "theme-transformation",
            "theme-love-and-vanity",
            "theme-heroes-and-quests",
            "theme-nature-spirits"
        ],
        "keywords": ["themes", "teachings", "worldview", "cosmology"]
    },
]


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


def strip_front_matter(text):
    """Remove everything before the first story."""
    idx = text.find("\nMOOWIS.\n")
    if idx != -1:
        # Keep the MOOWIS title line
        return text[idx + 1:].strip()
    return text


def clean_text(text):
    """Clean illustration markers, excessive whitespace."""
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_stories(text):
    """Split text into individual stories based on title patterns."""
    stories = []
    positions = []

    for i, sdef in enumerate(STORY_DEFS):
        title = sdef["title"]
        # Find the title as a standalone line
        pattern = "\n" + title + "\n"
        idx = text.find(pattern)
        if idx != -1:
            positions.append((idx, i))
        else:
            # Try at the very start of text
            if text.startswith(title + "\n") or text.startswith(title + "\r"):
                positions.append((0, i))
            else:
                # Try without trailing period
                pattern2 = "\n" + title.rstrip('.') + "\n"
                idx2 = text.find(pattern2)
                if idx2 != -1:
                    positions.append((idx2, i))
                else:
                    print(f"WARNING: Could not find story: {title}")

    positions.sort(key=lambda x: x[0])

    for pos_idx, (start_pos, def_idx) in enumerate(positions):
        sdef = STORY_DEFS[def_idx]
        if pos_idx + 1 < len(positions):
            end_pos = positions[pos_idx + 1][0]
        else:
            end_pos = len(text)

        story_text = text[start_pos:end_pos].strip()

        # Remove the title line
        lines = story_text.split('\n')
        content_start = 0
        for j, line in enumerate(lines):
            stripped = line.strip()
            if stripped == '':
                continue
            if stripped == sdef["title"] or stripped == sdef["title"].rstrip('.'):
                content_start = j + 1
            else:
                break

        story_content = '\n'.join(lines[content_start:]).strip()
        story_content = clean_text(story_content)

        stories.append({
            "def_idx": def_idx,
            "text": story_content
        })

    return stories


def build_l1_items(stories):
    """Build L1 items from extracted stories."""
    items = []
    for sort_order, story in enumerate(stories):
        sdef = STORY_DEFS[story["def_idx"]]
        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "level": 1,
            "category": "folk-tale",
            "sections": {
                "Story": story["text"],
                "Reflection": sdef["reflection"]
            },
            "keywords": sdef["keywords"],
            "metadata": {
                "source": "Folk-Lore and Legends: North American Indian, W. W. Gibbings, London, 1890"
            }
        }
        items.append(item)
    return items


def build_l2_items(l1_items):
    """Build L2 thematic groupings."""
    l2_items = []
    sort_order = len(l1_items)

    for group in THEME_GROUPS:
        l2_items.append({
            "id": group["id"],
            "name": group["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": group["category"],
            "sections": {
                "About": group["about"],
                "For Readers": group["for_readers"]
            },
            "keywords": group["keywords"],
            "composite_of": group["member_ids"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    return l2_items, sort_order


def build_l3_items(start_sort_order):
    """Build L3 meta-categories."""
    l3_items = []
    sort_order = start_sort_order

    for l3 in L3_DEFS:
        l3_items.append({
            "id": l3["id"],
            "name": l3["name"],
            "sort_order": sort_order,
            "level": 3,
            "category": l3["category"],
            "sections": {
                "About": l3["about"]
            },
            "keywords": l3["keywords"],
            "composite_of": l3["composite_of"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    return l3_items


def build_grammar(l1_items, l2_items, l3_items):
    """Assemble the complete grammar."""
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Anonymous",
                    "date": "1890",
                    "note": "Original collector and editor, Folk-Lore and Legends: North American Indian, published by W. W. Gibbings, London"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure, thematic groupings, and reflections"
                }
            ]
        },
        "name": "Folk-Lore and Legends: North American Indian",
        "description": "Thirty-one folk tales from North American Indian traditions, collected and published anonymously in London in 1890. The collection features the great trickster Manabozho, journeys to the spirit world, tales of transformation and shape-shifting, and stories of love between humans and the living natural world. These tales illuminate an animist cosmology in which trees speak, the dead are near, and the boundary between human and animal is fluid and permeable. Source: Project Gutenberg eBook #22072 (https://www.gutenberg.org/ebooks/22072).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: No specific illustrator credited in the 1890 W. W. Gibbings edition. George Catlin's paintings of Native American life (1830s-1840s) and Karl Bodmer's illustrations from 'Travels in the Interior of North America' (1832-1834) provide excellent period visual companions for these tales.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "folklore",
            "native-american",
            "mythology",
            "trickster",
            "spirits",
            "animism",
            "transformation",
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

    print("Stripping front matter...")
    text = strip_front_matter(text)

    print("Extracting stories...")
    stories = extract_stories(text)
    print(f"  Found {len(stories)} stories")

    print("Building L1 items...")
    l1_items = build_l1_items(stories)

    print("Building L2 items...")
    l2_items, next_sort = build_l2_items(l1_items)

    print("Building L3 items...")
    l3_items = build_l3_items(next_sort)

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
