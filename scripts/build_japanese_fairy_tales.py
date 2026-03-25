#!/usr/bin/env python3
"""
Parser for Japanese Fairy Tales by Yei Theodora Ozaki (Project Gutenberg #4018).
Outputs grammar.json into grammars/japanese-fairy-tales/
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'japanese-fairy-tales.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'japanese-fairy-tales')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

# Story titles as they appear in the text, mapped to clean IDs and display names
STORY_DEFS = [
    {
        "title_pattern": "MY LORD BAG OF RICE",
        "id": "my-lord-bag-of-rice",
        "name": "My Lord Bag of Rice",
        "keywords": ["warrior", "dragon", "gratitude", "courage", "bravery", "centipede", "lake-biwa"],
        "category": "hero-tales",
        "reflection": "What does it mean to show courage not through fighting, but through willingness to help? Consider how true bravery often appears when we face challenges for the sake of others."
    },
    {
        "title_pattern": "THE TONGUE-CUT SPARROW",
        "id": "the-tongue-cut-sparrow",
        "name": "The Tongue-Cut Sparrow",
        "keywords": ["sparrow", "kindness", "greed", "punishment", "old-man", "wife", "treasure"],
        "category": "animal-tales",
        "reflection": "This story shows how kindness brings its own rewards, while greed leads to ruin. What small kindnesses in your life have led to unexpected gifts?"
    },
    {
        "title_pattern": "THE STORY OF URASHIMA TARO, THE FISHER LAD",
        "id": "urashima-taro",
        "name": "The Story of Urashima Taro, the Fisher Lad",
        "keywords": ["fisherman", "turtle", "sea-palace", "time", "aging", "dragon-princess", "loss"],
        "category": "supernatural-tales",
        "reflection": "Urashima Taro's tale warns about longing for what we've left behind. Have you ever tried to return to a place or time, only to find everything changed?"
    },
    {
        "title_pattern": "THE FARMER AND THE BADGER",
        "id": "the-farmer-and-the-badger",
        "name": "The Farmer and the Badger",
        "keywords": ["badger", "rabbit", "revenge", "justice", "farmer", "trickery"],
        "category": "animal-tales",
        "reflection": "Justice arrives in unexpected ways in this tale. When have you seen a friend stand up for someone who could not defend themselves?"
    },
    {
        "title_pattern": 'THE \u201cSHINANSHA,\u201d OR THE SOUTH POINTING CARRIAGE',
        "id": "the-south-pointing-carriage",
        "name": "The South Pointing Carriage",
        "keywords": ["invention", "emperor", "compass", "wisdom", "ancient-china", "ingenuity"],
        "category": "legend-tales",
        "reflection": "This tale celebrates human ingenuity and the power of invention. What inventions or ideas have changed the direction of your life?"
    },
    {
        "title_pattern": "THE ADVENTURES OF KINTARO, THE GOLDEN BOY",
        "id": "kintaro-the-golden-boy",
        "name": "The Adventures of Kintaro, the Golden Boy",
        "keywords": ["kintaro", "strength", "nature", "animals", "mountain", "mother", "warrior"],
        "category": "hero-tales",
        "reflection": "Kintaro grows up wild in nature, befriending animals and growing strong. What can children learn from spending time in nature rather than in structured settings?"
    },
    {
        "title_pattern": "THE STORY OF PRINCESS HASE",
        "id": "princess-hase",
        "name": "The Story of Princess Hase",
        "keywords": ["princess", "stepmother", "loyalty", "devotion", "prayer", "perseverance", "virtue"],
        "category": "princess-tales",
        "reflection": "Princess Hase endures cruelty with grace and patience. Is there a time when quiet endurance and faith helped you through difficulty?"
    },
    {
        "title_pattern": "THE STORY OF THE MAN WHO DID NOT WISH TO DIE",
        "id": "the-man-who-did-not-wish-to-die",
        "name": "The Story of the Man Who Did Not Wish to Die",
        "keywords": ["immortality", "mortality", "paradise", "longing", "time", "regret", "sentoku"],
        "category": "supernatural-tales",
        "reflection": "Seeking to escape death, this man finds that eternal life without connection is its own kind of loss. What would you do with endless time?"
    },
    {
        "title_pattern": "THE BAMBOO-CUTTER AND THE MOON-CHILD",
        "id": "the-bamboo-cutter-and-the-moon-child",
        "name": "The Bamboo-Cutter and the Moon-Child",
        "keywords": ["kaguya-hime", "moon", "bamboo", "beauty", "suitors", "celestial", "parting", "emperor"],
        "category": "princess-tales",
        "reflection": "Kaguya-hime's story is one of beauty that cannot be possessed and love that must let go. When have you had to release something precious back to where it belonged?"
    },
    {
        "title_pattern": "THE MIRROR OF MATSUYAMA",
        "id": "the-mirror-of-matsuyama",
        "name": "The Mirror of Matsuyama",
        "keywords": ["mirror", "mother", "daughter", "love", "memory", "devotion", "stepmother"],
        "category": "family-tales",
        "reflection": "A daughter sees her mother's face in a mirror and keeps her memory alive. How do you carry the memory of loved ones with you?"
    },
    {
        "title_pattern": "THE GOBLIN OF ADACHIGAHARA",
        "id": "the-goblin-of-adachigahara",
        "name": "The Goblin of Adachigahara",
        "keywords": ["goblin", "monk", "danger", "prayer", "evil", "escape", "oni"],
        "category": "supernatural-tales",
        "reflection": "The monks' faith and quick thinking save them from a terrible fate. When has awareness of hidden danger helped you avoid harm?"
    },
    {
        "title_pattern": "THE SAGACIOUS MONKEY AND THE BOAR",
        "id": "the-sagacious-monkey-and-the-boar",
        "name": "The Sagacious Monkey and the Boar",
        "keywords": ["monkey", "boar", "cleverness", "trickery", "hunter", "wit"],
        "category": "animal-tales",
        "reflection": "Cleverness can be a double-edged sword. When is it wise to use wit, and when might simplicity serve better?"
    },
    {
        "title_pattern": "THE HAPPY HUNTER AND THE SKILLFUL FISHER",
        "id": "the-happy-hunter-and-the-skillful-fisher",
        "name": "The Happy Hunter and the Skillful Fisher",
        "keywords": ["brothers", "sea-god", "fish-hook", "dragon-palace", "magic", "jewels", "mythology"],
        "category": "hero-tales",
        "reflection": "This myth of two divine brothers shows how different gifts can complement each other. How do you honor the unique strengths of those around you?"
    },
    {
        "title_pattern": "THE STORY OF THE OLD MAN WHO MADE WITHERED TREES TO FLOWER",
        "id": "the-old-man-who-made-withered-trees-flower",
        "name": "The Old Man Who Made Withered Trees to Flower",
        "keywords": ["old-man", "dog", "kindness", "greed", "neighbor", "cherry-blossoms", "magic"],
        "category": "family-tales",
        "reflection": "Like the tongue-cut sparrow, this tale shows kindness rewarded and greed punished. The cherry blossoms bloom for the pure of heart. What makes your heart bloom?"
    },
    {
        "title_pattern": "THE JELLY FISH AND THE MONKEY",
        "id": "the-jelly-fish-and-the-monkey",
        "name": "The Jelly Fish and the Monkey",
        "keywords": ["jellyfish", "monkey", "sea-queen", "trickery", "punishment", "dragon-palace"],
        "category": "animal-tales",
        "reflection": "The jellyfish lost its bones through failure, and the monkey escaped through cleverness. What do these transformations tell us about consequences?"
    },
    {
        "title_pattern": "THE QUARREL OF THE MONKEY AND THE CRAB",
        "id": "the-quarrel-of-the-monkey-and-the-crab",
        "name": "The Quarrel of the Monkey and the Crab",
        "keywords": ["monkey", "crab", "revenge", "justice", "persimmon", "trickery", "allies"],
        "category": "animal-tales",
        "reflection": "When the crab is wronged, unlikely allies come together for justice. Have you ever found help from unexpected friends?"
    },
    {
        "title_pattern": "THE WHITE HARE AND THE CROCODILES",
        "id": "the-white-hare-and-the-crocodiles",
        "name": "The White Hare and the Crocodiles",
        "keywords": ["hare", "crocodile", "trickery", "compassion", "okuninushi", "healing", "mythology"],
        "category": "animal-tales",
        "reflection": "The hare's trickery leads to suffering, but true compassion brings healing. How does genuine kindness differ from the false advice of those who wish us harm?"
    },
    {
        "title_pattern": "THE STORY OF PRINCE YAMATO TAKE",
        "id": "prince-yamato-take",
        "name": "The Story of Prince Yamato Take",
        "keywords": ["prince", "warrior", "sword", "fire", "bravery", "sacrifice", "mythology", "hero"],
        "category": "hero-tales",
        "reflection": "Prince Yamato Take is Japan's greatest legendary hero, whose courage never wavered even in death. What does his story teach about the cost of heroism?"
    },
    {
        "title_pattern": "MOMOTARO, OR THE STORY OF THE SON OF A PEACH",
        "id": "momotaro",
        "name": "Momotaro, or the Story of the Son of a Peach",
        "keywords": ["momotaro", "peach", "ogre", "dog", "monkey", "pheasant", "adventure", "hero"],
        "category": "hero-tales",
        "reflection": "Momotaro gathers loyal companions and defeats the ogres through teamwork. What companions would you choose for your own adventure, and why?"
    },
    {
        "title_pattern": "THE OGRE OF RASHOMON",
        "id": "the-ogre-of-rashomon",
        "name": "The Ogre of Rashomon",
        "keywords": ["ogre", "warrior", "bravery", "rashomon", "watanabe", "arm", "disguise"],
        "category": "hero-tales",
        "reflection": "Watanabe's courage at Rashomon gate is tested twice — once in battle and once by deception. How do you stay brave when danger takes a familiar form?"
    },
    {
        "title_pattern": "HOW AN OLD MAN LOST HIS WEN",
        "id": "how-an-old-man-lost-his-wen",
        "name": "How an Old Man Lost His Wen",
        "keywords": ["old-man", "wen", "demons", "dancing", "greed", "neighbor", "punishment"],
        "category": "family-tales",
        "reflection": "One old man dances with joy and is rewarded; his neighbor dances with greed and is punished. What is the difference between doing something for love and doing it for gain?"
    },
    {
        "title_pattern": "THE STONES OF FIVE COLORS AND THE EMPRESS JOKWA",
        "id": "the-stones-of-five-colors",
        "name": "The Stones of Five Colors and the Empress Jokwa",
        "keywords": ["empress", "creation", "sky", "stones", "mythology", "china", "cosmic-repair"],
        "category": "legend-tales",
        "reflection": "Empress Jokwa repairs the very heavens themselves. What broken things in your world might you have the power to mend?"
    },
]


def read_seed():
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK JAPANESE FAIRY TALES ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK JAPANESE FAIRY TALES ***"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def strip_front_matter(text):
    """Remove title page, dedication, preface, and table of contents.
    Start from 'MY LORD BAG OF RICE' which is the first story."""
    # Find the first story title
    idx = text.find("\nMY LORD BAG OF RICE\n")
    if idx != -1:
        return text[idx:].strip()
    return text


def strip_end_matter(text):
    """Remove 'THE END.' marker."""
    idx = text.rfind("THE END.")
    if idx != -1:
        text = text[:idx].strip()
    return text


def extract_stories(text):
    """Split text into individual stories based on title patterns."""
    stories = []

    # Build a list of (position, story_def_index) for each story title found
    positions = []
    for i, sdef in enumerate(STORY_DEFS):
        pattern = sdef["title_pattern"]
        # Search for the title as a standalone line
        idx = text.find(pattern)
        if idx != -1:
            positions.append((idx, i))
        else:
            print(f"WARNING: Could not find story: {pattern}")

    # Sort by position in text
    positions.sort(key=lambda x: x[0])

    for pos_idx, (start_pos, def_idx) in enumerate(positions):
        sdef = STORY_DEFS[def_idx]

        # Find end of this story (start of next story or end of text)
        if pos_idx + 1 < len(positions):
            end_pos = positions[pos_idx + 1][0]
        else:
            end_pos = len(text)

        story_text = text[start_pos:end_pos].strip()

        # Remove the title line(s) from the story text
        # Title may span multiple lines (e.g., "THE STORY OF PRINCESS HASE.\nA STORY OF OLD JAPAN")
        lines = story_text.split('\n')
        # Skip blank lines and title lines at the beginning
        content_start = 0
        for j, line in enumerate(lines):
            stripped = line.strip()
            if stripped == '':
                continue
            # Check if this line is part of the title
            if stripped.upper() == stripped and len(stripped) > 2:
                content_start = j + 1
            else:
                break

        story_content = '\n'.join(lines[content_start:]).strip()

        # Clean up: remove excessive blank lines
        story_content = re.sub(r'\n{3,}', '\n\n', story_content)

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

        sections = {
            "Story": story["text"].strip(),
            "Reflection": sdef["reflection"]
        }

        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "level": 1,
            "category": sdef["category"],
            "sections": sections,
            "keywords": sdef["keywords"],
            "metadata": {
                "source": "Japanese Fairy Tales, compiled by Yei Theodora Ozaki, 1908"
            }
        }
        items.append(item)

    return items


def build_l2_items(l1_items):
    """Build L2 groupings by theme and character type."""
    l2_items = []
    sort_order = len(l1_items)

    # --- Theme groupings ---
    theme_groups = [
        {
            "id": "theme-courage-and-heroism",
            "name": "Courage and Heroism",
            "category": "themes",
            "about": "Tales of brave warriors, legendary heroes, and those who face danger with unwavering spirit. These stories celebrate the Japanese ideal of the hero who serves others through courage — from Momotaro's quest against the ogres to Prince Yamato Take's epic journey across Japan.",
            "for_parents": "These stories are wonderful for inspiring bravery and a sense of purpose. They show children that true courage is not the absence of fear but the willingness to act despite it. Discuss with children: What made each hero brave? Was it strength alone, or something deeper?",
            "member_ids": ["my-lord-bag-of-rice", "kintaro-the-golden-boy", "the-happy-hunter-and-the-skillful-fisher", "prince-yamato-take", "momotaro", "the-ogre-of-rashomon"],
            "keywords": ["courage", "hero", "warrior", "bravery", "quest"]
        },
        {
            "id": "theme-kindness-and-greed",
            "name": "Kindness Rewarded, Greed Punished",
            "category": "themes",
            "about": "A beloved pattern in Japanese fairy tales: the kind, humble person is rewarded, while the greedy neighbor or spouse who tries to imitate them meets misfortune. These stories carry deep moral weight about the nature of generosity and the self-defeating nature of envy.",
            "for_parents": "These paired-outcome stories are excellent for moral discussions. Ask children to compare the two characters: What made one succeed and the other fail? Was it luck, or character? Help children see that the stories are not about punishment, but about the natural consequences of how we treat others.",
            "member_ids": ["the-tongue-cut-sparrow", "the-old-man-who-made-withered-trees-flower", "how-an-old-man-lost-his-wen"],
            "keywords": ["kindness", "greed", "morals", "reward", "punishment", "generosity"]
        },
        {
            "id": "theme-supernatural-realms",
            "name": "Journeys to Supernatural Realms",
            "category": "themes",
            "about": "Stories of mortals who travel to enchanted places — the Dragon Palace beneath the sea, the land of eternal youth, the moon — and face the bittersweet consequences of crossing between worlds. These tales explore the human longing for paradise and the pain of return.",
            "for_parents": "These stories touch on deep themes of time, loss, and the impossibility of returning to the past. They are good starting points for conversations about change, growing up, and appreciating the present moment. Ask: Why couldn't the hero stay in the magical place? What did they lose by leaving — and what might they have lost by staying?",
            "member_ids": ["urashima-taro", "the-man-who-did-not-wish-to-die", "the-bamboo-cutter-and-the-moon-child", "the-goblin-of-adachigahara"],
            "keywords": ["supernatural", "magic", "otherworld", "dragon-palace", "transformation"]
        },
        {
            "id": "theme-cleverness-and-trickery",
            "name": "Cleverness and Trickery",
            "category": "themes",
            "about": "Tales where wit, cunning, and clever schemes drive the plot. Animals trick each other, the clever escape danger, and sometimes trickery backfires. These stories value intelligence and resourcefulness alongside — and sometimes above — brute strength.",
            "for_parents": "These stories are fun and engaging, but also raise interesting moral questions. Is trickery always wrong? When is cleverness admirable, and when does it cross a line? These tales can spark great discussions about honesty, strategy, and the difference between outsmarting and deceiving.",
            "member_ids": ["the-farmer-and-the-badger", "the-sagacious-monkey-and-the-boar", "the-jelly-fish-and-the-monkey", "the-quarrel-of-the-monkey-and-the-crab", "the-white-hare-and-the-crocodiles"],
            "keywords": ["cleverness", "trickery", "wit", "cunning", "animals"]
        },
        {
            "id": "theme-love-and-devotion",
            "name": "Love and Devotion",
            "category": "themes",
            "about": "Stories centered on the bonds of family — a daughter's love for her mother, a princess's devotion through hardship, the enduring memory of those we have lost. These tales celebrate loyalty, filial piety, and the quiet strength of love.",
            "for_parents": "These are tender stories that may bring up feelings about family, loss, and memory. They are wonderful for reading together and talking about the people children love. Ask: How did the characters show their love? How do we remember people who are far away or gone?",
            "member_ids": ["princess-hase", "the-mirror-of-matsuyama"],
            "keywords": ["love", "family", "devotion", "mother", "daughter", "loyalty"]
        },
        {
            "id": "theme-origins-and-legends",
            "name": "Origins and Legends",
            "category": "themes",
            "about": "Grand tales that explain the origins of things — why the jellyfish has no bones, how the compass was invented, how the Empress Jokwa repaired the sky. These are the myths and legends that connect Japanese (and Chinese) fairy tales to deeper mythological traditions.",
            "for_parents": "Origin stories spark curiosity and wonder. They invite children to ask 'why?' and to imagine explanations for the world around them. After reading these, encourage children to make up their own origin stories: Why does the cat purr? Why is the sky blue?",
            "member_ids": ["the-south-pointing-carriage", "the-jelly-fish-and-the-monkey", "the-stones-of-five-colors"],
            "keywords": ["origin", "legend", "mythology", "creation", "explanation"]
        },
    ]

    # --- Character type groupings ---
    character_groups = [
        {
            "id": "characters-animal-stories",
            "name": "Animal Stories",
            "category": "characters",
            "about": "Tales featuring animal characters — monkeys, crabs, hares, badgers, sparrows, and jellyfish. In Japanese folklore, animals are tricksters, helpers, victims, and teachers. They carry human qualities and demonstrate moral lessons through their adventures.",
            "for_parents": "Children naturally love animal characters. Use these stories to explore how animals in folklore represent different human traits: the monkey's cleverness, the hare's boastfulness, the sparrow's gentleness. Ask: If you were an animal in a fairy tale, which would you be?",
            "member_ids": ["the-tongue-cut-sparrow", "the-farmer-and-the-badger", "the-sagacious-monkey-and-the-boar", "the-jelly-fish-and-the-monkey", "the-quarrel-of-the-monkey-and-the-crab", "the-white-hare-and-the-crocodiles"],
            "keywords": ["animals", "monkey", "sparrow", "hare", "badger", "crab", "jellyfish"]
        },
        {
            "id": "characters-warriors-and-heroes",
            "name": "Warriors and Heroes",
            "category": "characters",
            "about": "Japan's legendary heroes — brave samurai, divine princes, and supernatural children of miraculous birth. Hidesato slays the centipede, Kintaro wrestles bears, Momotaro defeats the ogres, and Yamato Take conquers with sword and cunning. These are the foundational hero stories of Japanese culture.",
            "for_parents": "Hero stories are foundational for children's moral development. They model courage, loyalty, and self-sacrifice. Compare these Japanese heroes with heroes from other cultures your child knows. Ask: What makes someone a hero? Is it strength, kindness, or something else?",
            "member_ids": ["my-lord-bag-of-rice", "kintaro-the-golden-boy", "the-happy-hunter-and-the-skillful-fisher", "prince-yamato-take", "momotaro", "the-ogre-of-rashomon"],
            "keywords": ["warrior", "hero", "samurai", "strength", "quest"]
        },
        {
            "id": "characters-princesses-and-maidens",
            "name": "Princesses and Maidens",
            "category": "characters",
            "about": "Stories centered on noble women — the celestial Kaguya-hime born from bamboo, the steadfast Princess Hase, and the devoted daughter of Matsuyama. These women show strength through endurance, grace, and unwavering love rather than through combat.",
            "for_parents": "These stories offer a different model of strength — one based on patience, devotion, and inner fortitude. Discuss with children how these princesses are strong in their own way. Ask: How is Princess Hase brave even though she never fights?",
            "member_ids": ["princess-hase", "the-bamboo-cutter-and-the-moon-child", "the-mirror-of-matsuyama"],
            "keywords": ["princess", "maiden", "devotion", "beauty", "strength"]
        },
        {
            "id": "characters-old-folk",
            "name": "Old Men and Women of the Tales",
            "category": "characters",
            "about": "Many Japanese fairy tales feature elderly characters — kind old men, grumbling old wives, humble woodcutters. These characters often serve as moral exemplars (or cautionary tales), showing that wisdom comes with age, but so can greed and foolishness.",
            "for_parents": "These stories honor the elderly and explore the virtues and vices of old age. They can help children appreciate grandparents and older people in their lives. Ask: What did the kind old man do differently from the greedy one? What can we learn from older people?",
            "member_ids": ["the-tongue-cut-sparrow", "the-old-man-who-made-withered-trees-flower", "how-an-old-man-lost-his-wen", "the-bamboo-cutter-and-the-moon-child"],
            "keywords": ["old-man", "old-woman", "elderly", "wisdom", "kindness", "greed"]
        },
    ]

    for group in theme_groups:
        l2_items.append({
            "id": group["id"],
            "name": group["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": group["category"],
            "sections": {
                "About": group["about"],
                "For Parents": group["for_parents"]
            },
            "keywords": group["keywords"],
            "composite_of": group["member_ids"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    for group in character_groups:
        l2_items.append({
            "id": group["id"],
            "name": group["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": group["category"],
            "sections": {
                "About": group["about"],
                "For Parents": group["for_parents"]
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

    l3_defs = [
        {
            "id": "meta-themes",
            "name": "Themes and Morals",
            "category": "meta",
            "about": "The great moral and thematic currents that run through Japanese fairy tales: courage, kindness, the supernatural, cleverness, love, and the origins of things. These groupings reveal the values and worldview embedded in Japanese folklore — a culture that prizes loyalty, humility, and harmony with nature.",
            "composite_of": [
                "theme-courage-and-heroism",
                "theme-kindness-and-greed",
                "theme-supernatural-realms",
                "theme-cleverness-and-trickery",
                "theme-love-and-devotion",
                "theme-origins-and-legends"
            ],
            "keywords": ["themes", "morals", "values", "japanese-culture"]
        },
        {
            "id": "meta-characters",
            "name": "Character Types",
            "category": "meta",
            "about": "The archetypal characters of Japanese fairy tales: clever animals, brave warriors, graceful princesses, and wise (or foolish) elders. These character types reflect the social world of old Japan and carry universal human qualities that resonate across all cultures.",
            "composite_of": [
                "characters-animal-stories",
                "characters-warriors-and-heroes",
                "characters-princesses-and-maidens",
                "characters-old-folk"
            ],
            "keywords": ["characters", "archetypes", "types"]
        }
    ]

    for l3 in l3_defs:
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
                    "name": "Yei Theodora Ozaki",
                    "date": "1908",
                    "note": "Compiler and translator of Japanese Fairy Tales"
                },
                {
                    "name": "Sadanami Sanjin",
                    "date": "1908",
                    "note": "Author of the modern Japanese versions from which these tales were translated"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure and reflections"
                }
            ]
        },
        "name": "Japanese Fairy Tales",
        "description": "Twenty-two classic Japanese fairy tales compiled by Yei Theodora Ozaki (1908), translated from the modern Japanese versions of Sadanami Sanjin. These beloved stories — including Momotaro, Urashima Taro, Kaguya-hime, and Kintaro — are the foundational fairy tales of Japan, featuring brave warriors, clever animals, enchanted princesses, and journeys to supernatural realms. They carry deep moral teachings about courage, kindness, loyalty, and the consequences of greed. Source: Project Gutenberg eBook #4018 (https://www.gutenberg.org/ebooks/4018).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Kakuzo Fujiyama's original illustrations for the 1908 Archibald Constable & Co. edition of 'Japanese Fairy Tales' — color plates in traditional Japanese art style. Hasegawa Takejiro's 'Japanese Fairy Tale Series' (1885-1922, T. Hasegawa, Tokyo) — beautiful color woodblock-printed crêpe paper books, public domain. Warwick Goble's illustrations for 'Green Willow and Other Japanese Fairy Tales' (1910, Macmillan) — watercolor illustrations of Japanese scenes and characters, public domain.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "fairy-tales",
            "kids",
            "japanese",
            "folklore",
            "animals",
            "heroes",
            "morals",
            "mythology",
            "oracle"
        ],
        "roots": ["eastern-wisdom", "animism"],
        "shelves": ["wonder", "children", "wisdom"],
        "lineages": ["Shrei", "Akomolafe"],
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

    print("Stripping end matter...")
    text = strip_end_matter(text)

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

    # Ensure output directory exists
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
