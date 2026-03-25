#!/usr/bin/env python3
"""
Parser for West African Folk-Tales by W. H. Barker & Cecilia Sinclair (Project Gutenberg #66923).
Outputs grammar.json into grammars/west-african-folk-tales/
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'west-african-folk-tales.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'west-african-folk-tales')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

# Story definitions with the exact title patterns as they appear in the text
STORY_DEFS = [
    {
        "title_pattern": "I. HOW WE GOT THE NAME \u2018SPIDER TALES\u2019",
        "id": "how-we-got-spider-tales",
        "name": "How We Got the Name 'Spider Tales'",
        "keywords": ["anansi", "spider", "nyankupon", "bees", "boa", "tiger", "cleverness", "origin"],
        "category": "anansi-tales",
        "reflection": "Anansi earns the right to have all stories named after him through sheer cunning. What would you be willing to do to make your name live forever?"
    },
    {
        "title_pattern": "II. HOW WISDOM BECAME THE PROPERTY OF THE HUMAN RACE",
        "id": "how-wisdom-became-property",
        "name": "How Wisdom Became the Property of the Human Race",
        "keywords": ["anansi", "wisdom", "kweku-tsin", "pot", "tree", "humility"],
        "category": "anansi-tales",
        "reflection": "Even the wisest cannot hold all wisdom alone — a child's simple suggestion proves greater than a lifetime of knowledge. When has a fresh perspective solved a problem you could not?"
    },
    {
        "title_pattern": "III. ANANSI AND NOTHING",
        "id": "anansi-and-nothing",
        "name": "Anansi and Nothing",
        "keywords": ["anansi", "nothing", "greed", "starvation", "punishment"],
        "category": "anansi-tales",
        "reflection": "Anansi's greed leads him to steal from a mysterious being called Nothing. What happens when you take from those who seem to have little?"
    },
    {
        "title_pattern": "IV. THUNDER AND ANANSI",
        "id": "thunder-and-anansi",
        "name": "Thunder and Anansi",
        "keywords": ["anansi", "thunder", "sea", "cleverness", "danger", "escape"],
        "category": "anansi-tales",
        "reflection": "Anansi faces the terrifying power of Thunder and must use all his cunning to survive. How do you navigate forces far more powerful than yourself?"
    },
    {
        "title_pattern": "V. WHY THE LIZARD CONTINUALLY MOVES HIS HEAD UP AND DOWN",
        "id": "why-lizard-moves-head",
        "name": "Why the Lizard Continually Moves His Head Up and Down",
        "keywords": ["lizard", "anansi", "princess", "marriage", "trickery", "origin"],
        "category": "anansi-tales",
        "reflection": "The lizard's constant nodding tells a story of being tricked out of a rightful reward. What habits do you carry that trace back to old injustices?"
    },
    {
        "title_pattern": "VI. TIT FOR TAT",
        "id": "tit-for-tat",
        "name": "Tit for Tat",
        "keywords": ["anansi", "wolf", "leopard", "meat", "trickery", "reciprocity"],
        "category": "anansi-tales",
        "reflection": "What goes around comes around in this tale of reciprocal trickery. When has someone turned your own tactics against you?"
    },
    {
        "title_pattern": "VII. WHY WHITE ANTS ALWAYS HARM MAN'S PROPERTY",
        "id": "why-white-ants-harm",
        "name": "Why White Ants Always Harm Man's Property",
        "keywords": ["anansi", "white-ants", "debt", "property", "destruction", "origin"],
        "category": "anansi-tales",
        "reflection": "The destructiveness of white ants is traced to an ancient debt. What old grievances continue to cause damage in the present?"
    },
    {
        "title_pattern": "VIII. THE SQUIRREL AND THE SPIDER",
        "id": "squirrel-and-spider",
        "name": "The Squirrel and the Spider",
        "keywords": ["squirrel", "anansi", "spider", "cleverness", "competition"],
        "category": "anansi-tales",
        "reflection": "The squirrel proves a worthy match for the cunning spider. Who in your life can match wits with the cleverest person you know?"
    },
    {
        "title_pattern": "IX. WHY WE SEE ANTS CARRYING BUNDLES AS BIG AS THEMSELVES",
        "id": "why-ants-carry-bundles",
        "name": "Why We See Ants Carrying Bundles as Big as Themselves",
        "keywords": ["ants", "anansi", "strength", "debt", "carrying", "origin"],
        "category": "anansi-tales",
        "reflection": "The tiny ant carries enormous loads because of an ancient obligation. What burdens do you carry that seem larger than yourself?"
    },
    {
        "title_pattern": "X. WHY SPIDERS ARE ALWAYS FOUND IN THE CORNERS OF CEILINGS",
        "id": "why-spiders-in-corners",
        "name": "Why Spiders are Always Found in the Corners of Ceilings",
        "keywords": ["anansi", "spider", "shame", "ceiling", "hiding", "origin"],
        "category": "anansi-tales",
        "reflection": "Anansi hides in the ceiling corner out of shame for his misdeeds. What do your hiding places reveal about your history?"
    },
    {
        "title_pattern": "XI. ANANSI THE BLIND FISHERMAN",
        "id": "anansi-blind-fisherman",
        "name": "Anansi the Blind Fisherman",
        "keywords": ["anansi", "blind", "fishing", "trickery", "deception"],
        "category": "anansi-tales",
        "reflection": "Anansi pretends to be blind to gain advantage. When have you seen someone feign weakness to exploit others' sympathy?"
    },
    {
        "title_pattern": "XII. ADZANUMEE AND HER MOTHER",
        "id": "adzanumee-and-mother",
        "name": "Adzanumee and Her Mother",
        "keywords": ["adzanumee", "mother", "bird", "magic", "obedience", "disobedience"],
        "category": "anansi-tales",
        "reflection": "A daughter's disobedience has magical consequences. How do the choices of children affect their parents' fates?"
    },
    {
        "title_pattern": "XIII. THE GRINDING-STONE THAT GROUND FLOUR BY ITSELF",
        "id": "grinding-stone-ground-flour",
        "name": "The Grinding-Stone that Ground Flour by Itself",
        "keywords": ["anansi", "grinding-stone", "magic", "greed", "flour"],
        "category": "anansi-tales",
        "reflection": "A magic grinding-stone provides abundance until greed intervenes. What blessings have you seen ruined by wanting too much?"
    },
    {
        "title_pattern": "XIV. \u201cMORNING SUNRISE\u201d",
        "id": "morning-sunrise",
        "name": "Morning Sunrise",
        "keywords": ["anansi", "morning", "sunrise", "song", "magic"],
        "category": "anansi-tales",
        "reflection": "The magic of morning and its song resonate through this tale. What rituals mark the beginning of your days?"
    },
    {
        "title_pattern": "XV. WHY THE SEA-TURTLE WHEN CAUGHT BEATS ITS BREAST WITH ITS FORE-LEGS",
        "id": "why-sea-turtle-beats-breast",
        "name": "Why the Sea-Turtle When Caught Beats its Breast with its Fore-Legs",
        "keywords": ["sea-turtle", "anansi", "regret", "origin", "capture"],
        "category": "anansi-tales",
        "reflection": "The turtle's gesture of distress when caught carries an ancient story. What gestures of grief or frustration have been passed down in your family?"
    },
    {
        "title_pattern": "XVI. HOW BEASTS AND SERPENTS FIRST CAME INTO THE WORLD",
        "id": "how-beasts-and-serpents-came",
        "name": "How Beasts and Serpents First Came into the World",
        "keywords": ["anansi", "beasts", "serpents", "creation", "origin", "kweku-tsin", "magic-fiddle"],
        "category": "anansi-tales",
        "reflection": "This creation story explains the origin of all beasts and serpents. How do you imagine the first appearance of the creatures that share our world?"
    },
    {
        "title_pattern": "XVII. HONOURABLE MIN",
        "id": "honourable-minu",
        "name": "Honourable Minu",
        "keywords": ["anansi", "minu", "misunderstanding", "language", "humor"],
        "category": "anansi-tales",
        "reflection": "A comic misunderstanding about a name leads to absurd consequences. When has miscommunication led you into ridiculous situations?"
    },
    {
        "title_pattern": "XVIII. WHY THE MOON AND THE STARS RECEIVE THEIR LIGHT FROM THE SUN",
        "id": "why-moon-stars-receive-light",
        "name": "Why the Moon and the Stars Receive Their Light from the Sun",
        "keywords": ["moon", "stars", "sun", "light", "origin", "cosmic", "kweku-tsin"],
        "category": "anansi-tales",
        "reflection": "The cosmic order of sun, moon, and stars has its origin in an earthly drama. How do small events create lasting arrangements?"
    },
    {
        "title_pattern": "XIX. OHIA AND THE THIEVING DEER",
        "id": "ohia-and-thieving-deer",
        "name": "Ohia and the Thieving Deer",
        "keywords": ["ohia", "deer", "animals", "language", "secret", "death", "wife"],
        "category": "misc-tales",
        "reflection": "The gift of understanding animal speech comes with a fatal condition: never reveal it. What secrets do you carry that would be dangerous to share?"
    },
    {
        "title_pattern": "XX. HOW THE TORTOISE GOT ITS SHELL",
        "id": "how-tortoise-got-shell",
        "name": "How the Tortoise Got its Shell",
        "keywords": ["tortoise", "shell", "origin", "dogs", "feast"],
        "category": "misc-tales",
        "reflection": "The tortoise's protective shell has a story behind it. What armor have you developed to protect yourself, and what event gave it to you?"
    },
    {
        "title_pattern": "XXI. THE HUNTER AND THE TORTOISE",
        "id": "hunter-and-tortoise",
        "name": "The Hunter and the Tortoise",
        "keywords": ["hunter", "tortoise", "gratitude", "rescue", "wisdom"],
        "category": "misc-tales",
        "reflection": "A hunter's kindness to a tortoise is repaid in unexpected ways. How has a small act of kindness returned to you multiplied?"
    },
    {
        "title_pattern": "XXII. THE TAIL OF THE PRINCESS ELEPHANT",
        "id": "tail-of-princess-elephant",
        "name": "The Tail of the Princess Elephant",
        "keywords": ["princess", "elephant", "transformation", "magic", "marriage"],
        "category": "misc-tales",
        "reflection": "A princess who transforms into an elephant — shape-shifting as both power and curse. What transformations have you undergone that others found frightening?"
    },
    {
        "title_pattern": "XXIII. KWOFI AND THE GODS",
        "id": "kwofi-and-the-gods",
        "name": "Kwofi and the Gods",
        "keywords": ["kwofi", "gods", "feast", "injustice", "hunger"],
        "category": "misc-tales",
        "reflection": "Kwofi is excluded from the feast of the gods. How does exclusion shape the character of those left out?"
    },
    {
        "title_pattern": "XXIV. THE LION AND THE WOLF",
        "id": "lion-and-wolf",
        "name": "The Lion and the Wolf",
        "keywords": ["lion", "wolf", "power", "trickery", "alliance"],
        "category": "misc-tales",
        "reflection": "The lion and wolf interact as forces of power and cunning. How do the strong and the clever form alliances in your world?"
    },
    {
        "title_pattern": "XXV. MAKU MAWU AND MAKU FIA",
        "id": "maku-mawu-and-maku-fia",
        "name": "Maku Mawu and Maku Fia",
        "keywords": ["maku", "brothers", "rich", "poor", "fortune", "reversal"],
        "category": "misc-tales",
        "reflection": "Two brothers — one rich, one poor — and the reversals of fortune that teach humility. When has someone's fortune changed overnight?"
    },
    {
        "title_pattern": "XXVI. THE ROBBER AND THE OLD MAN",
        "id": "robber-and-old-man",
        "name": "The Robber and the Old Man",
        "keywords": ["robber", "old-man", "wisdom", "cunning", "morals"],
        "category": "misc-tales",
        "reflection": "An old man outsmarts a robber through wisdom rather than force. How does experience triumph over aggression?"
    },
    {
        "title_pattern": "XXVII. THE LEOPARD AND THE RAM",
        "id": "leopard-and-ram",
        "name": "The Leopard and the Ram",
        "keywords": ["leopard", "ram", "courage", "bluff", "survival"],
        "category": "misc-tales",
        "reflection": "The ram faces the leopard with an unexpected strategy. When has bluffing saved you from a more powerful adversary?"
    },
    {
        "title_pattern": "XXVIII. WHY THE LEOPARD CAN ONLY CATCH PREY ON ITS LEFT SIDE",
        "id": "why-leopard-catches-left",
        "name": "Why the Leopard Can Only Catch Prey on its Left Side",
        "keywords": ["leopard", "prey", "left-side", "origin", "disability"],
        "category": "misc-tales",
        "reflection": "Even the powerful leopard has a weakness with a story behind it. What limitations do you have that carry their own hidden history?"
    },
    {
        "title_pattern": "XXIX. QUARCOO BAH-BONI",
        "id": "quarcoo-bah-boni",
        "name": "Quarcoo Bah-Boni",
        "keywords": ["quarcoo", "adventure", "magic", "quest", "hero"],
        "category": "misc-tales",
        "reflection": "Quarcoo's adventures take him through trials and wonders. What quest in your own life has tested you most?"
    },
    {
        "title_pattern": "XXX. KING CHAMELEON AND THE ANIMALS",
        "id": "king-chameleon-and-animals",
        "name": "King Chameleon and the Animals",
        "keywords": ["chameleon", "king", "animals", "leadership", "wisdom"],
        "category": "misc-tales",
        "reflection": "The chameleon — who adapts to any situation — becomes king. Is adaptability the greatest form of leadership?"
    },
    {
        "title_pattern": "XXXI. TO LOSE AN ELEPHANT FOR THE SAKE OF A WREN IS A VERY FOOLISH",
        "id": "lose-elephant-for-wren",
        "name": "To Lose an Elephant for the Sake of a Wren is a Very Foolish Thing to Do",
        "keywords": ["elephant", "wren", "greed", "foolishness", "priorities"],
        "category": "misc-tales",
        "reflection": "Chasing the small while losing the great — a universal human folly. What small distractions have cost you something far more valuable?"
    },
    {
        "title_pattern": "XXXII. THE UNGRATEFUL MAN",
        "id": "ungrateful-man",
        "name": "The Ungrateful Man",
        "keywords": ["ungrateful", "rescue", "snake", "betrayal", "justice"],
        "category": "misc-tales",
        "reflection": "A man saved from danger repays his rescuer with betrayal. How do you respond when kindness is met with ingratitude?"
    },
    {
        "title_pattern": "XXXIII. WHY TIGERS NEVER ATTACK MEN UNLESS THEY ARE PROVOKED",
        "id": "why-tigers-never-attack",
        "name": "Why Tigers Never Attack Men Unless They are Provoked",
        "keywords": ["tiger", "leopard", "man", "provocation", "origin", "respect"],
        "category": "misc-tales",
        "reflection": "The understanding between humans and great cats rests on a fragile pact of mutual respect. What agreements keep peace between potential enemies?"
    },
    {
        "title_pattern": "XXXIV. THE OMANHENE WHO LIKED RIDDLES",
        "id": "omanhene-who-liked-riddles",
        "name": "The Omanhene Who Liked Riddles",
        "keywords": ["omanhene", "riddles", "wisdom", "king", "cleverness", "contest"],
        "category": "misc-tales",
        "reflection": "A king who prizes riddles above all else — knowledge and wit as the highest currency. What puzzles do you love to solve?"
    },
    {
        "title_pattern": "XXXV. HOW MUSHROOMS FIRST GREW",
        "id": "how-mushrooms-first-grew",
        "name": "How Mushrooms First Grew",
        "keywords": ["mushrooms", "origin", "ants", "nature", "growth"],
        "category": "misc-tales",
        "reflection": "Even mushrooms have their origin story in West African lore. What everyday things around you might have a story you have never heard?"
    },
    {
        "title_pattern": "XXXVI. FARMER MYBROW AND THE FAIRIES",
        "id": "farmer-mybrow-and-fairies",
        "name": "Farmer Mybrow and the Fairies",
        "keywords": ["farmer", "fairies", "help", "wife", "promise", "disaster"],
        "category": "misc-tales",
        "reflection": "Fairies help a farmer generously — until his wife breaks a promise and destroys the harvest. What partnerships have you seen ruined by a broken promise?"
    },
]


# L2 groupings
THEME_GROUPS = [
    {
        "id": "theme-anansi-trickster",
        "name": "Anansi the Trickster",
        "category": "themes",
        "about": "Anansi the Spider is the supreme trickster of West African folklore. Conceited, cunning, and endlessly resourceful, he tricks bees into jars, blindfolds tigers, and steals from the gods themselves. Yet his cleverness often backfires — he loses all the world's wisdom, hides in ceiling corners from shame, and brings beasts and serpents into the world through his schemes. Anansi is both hero and cautionary figure: admired for his wit, warned against for his greed.",
        "for_readers": "The Anansi stories carried across the Atlantic with enslaved Africans and became the Brer Rabbit tales of the American South and the Anansi stories of the Caribbean. They represent one of the great surviving threads of African culture in the diaspora. Read them as survival literature: the small, clever creature who outwits the powerful through intelligence rather than force.",
        "member_ids": [
            "how-we-got-spider-tales", "how-wisdom-became-property", "anansi-and-nothing",
            "thunder-and-anansi", "why-lizard-moves-head", "tit-for-tat",
            "why-white-ants-harm", "squirrel-and-spider", "why-ants-carry-bundles",
            "why-spiders-in-corners", "anansi-blind-fisherman", "adzanumee-and-mother",
            "grinding-stone-ground-flour", "morning-sunrise", "why-sea-turtle-beats-breast",
            "how-beasts-and-serpents-came", "honourable-minu", "why-moon-stars-receive-light"
        ],
        "keywords": ["anansi", "spider", "trickster", "cunning", "greed", "cleverness"]
    },
    {
        "id": "theme-why-things-are",
        "name": "Why Things Are: Origin Stories",
        "category": "themes",
        "about": "Many tales in this collection explain how the world came to be the way it is — why spiders hide in ceiling corners, why ants carry enormous loads, why the lizard bobs its head, why the moon receives its light from the sun, why mushrooms grow, why the tortoise has a shell, why the leopard can only catch prey on one side. These 'Just So Stories' of West Africa encode careful observation of nature within narrative form.",
        "for_readers": "These origin stories are a form of natural philosophy expressed through narrative. Each one starts from an observation (lizards bob their heads, spiders live in corners) and works backward to create a story that explains the phenomenon. They reveal a culture that paid close attention to the natural world and found meaning in every detail.",
        "member_ids": [
            "why-lizard-moves-head", "why-white-ants-harm", "why-ants-carry-bundles",
            "why-spiders-in-corners", "why-sea-turtle-beats-breast",
            "how-beasts-and-serpents-came", "why-moon-stars-receive-light",
            "how-tortoise-got-shell", "why-leopard-catches-left",
            "why-tigers-never-attack", "how-mushrooms-first-grew"
        ],
        "keywords": ["origin", "nature", "explanation", "animals", "just-so"]
    },
    {
        "id": "theme-wisdom-and-folly",
        "name": "Wisdom, Folly, and the Consequences of Greed",
        "category": "themes",
        "about": "A recurring theme across both Anansi and non-Anansi tales: the tension between wisdom and greed, cleverness and foolishness. Characters who are generous and wise prosper; those who are greedy, ungrateful, or foolish come to ruin. The grinding-stone that provides flour until greed intervenes, the farmer whose wife breaks her promise to the fairies, the ungrateful man who betrays his rescuer — all teach the same fundamental lesson.",
        "for_readers": "These tales function as moral education encoded in entertainment. The lessons are universal: be grateful, keep your promises, do not let greed destroy your blessings. Notice how the consequences in these tales are often immediate and dramatic — the punishment fits the crime with fairy-tale precision.",
        "member_ids": [
            "how-wisdom-became-property", "anansi-and-nothing", "grinding-stone-ground-flour",
            "lose-elephant-for-wren", "ungrateful-man", "farmer-mybrow-and-fairies",
            "robber-and-old-man"
        ],
        "keywords": ["wisdom", "greed", "folly", "morals", "consequences"]
    },
    {
        "id": "theme-magic-and-transformation",
        "name": "Magic, Transformation, and the Supernatural",
        "category": "themes",
        "about": "West African folk tales are infused with the supernatural — princesses who transform into elephants, magical grinding-stones, fairies who help (and destroy) harvests, and gods who feast while mortals go hungry. These tales describe a world where the boundary between natural and supernatural is permeable, and where magical forces are as real and consequential as any earthly power.",
        "for_readers": "The supernatural elements in these tales are not mere fantasy — they reflect a worldview in which spiritual forces actively shape daily life. The fairies of 'Farmer Mybrow' have the same capricious power as the fae of European tradition. The gods of 'Kwofi' are as real and as unfair as any Greek deity. Read these as expressions of a deeply spiritual worldview.",
        "member_ids": [
            "tail-of-princess-elephant", "grinding-stone-ground-flour",
            "farmer-mybrow-and-fairies", "kwofi-and-the-gods",
            "how-beasts-and-serpents-came", "quarcoo-bah-boni"
        ],
        "keywords": ["magic", "transformation", "supernatural", "fairies", "gods"]
    },
    {
        "id": "theme-power-and-survival",
        "name": "Power, Courage, and Survival",
        "category": "themes",
        "about": "Tales of confrontation between the powerful and the resourceful: the leopard and the ram, the lion and the wolf, the hunter and the tortoise, the omanhene who tests his subjects with riddles. These stories explore how intelligence, courage, and adaptability can overcome raw power — and how even the mightiest have their weaknesses.",
        "for_readers": "These tales celebrate the resourceful over the merely strong. The ram who faces down the leopard, the chameleon who becomes king through adaptability, the tortoise who survives through wit — all offer models for navigating a world where power is unevenly distributed.",
        "member_ids": [
            "leopard-and-ram", "lion-and-wolf", "hunter-and-tortoise",
            "king-chameleon-and-animals", "omanhene-who-liked-riddles",
            "ohia-and-thieving-deer", "maku-mawu-and-maku-fia"
        ],
        "keywords": ["power", "courage", "survival", "cleverness", "leadership"]
    },
]

L3_DEFS = [
    {
        "id": "meta-themes",
        "name": "Themes and Teachings",
        "category": "meta",
        "about": "The thematic landscape of West African folk tales: the trickster genius of Anansi, the origin stories that explain the natural world, the moral lessons about wisdom and greed, the supernatural forces that permeate daily life, and the strategies for survival in a world of unequal power. Together, these themes reveal a rich intellectual tradition that has influenced storytelling across three continents — from the Gold Coast to the Caribbean to the American South.",
        "composite_of": [
            "theme-anansi-trickster", "theme-why-things-are",
            "theme-wisdom-and-folly", "theme-magic-and-transformation",
            "theme-power-and-survival"
        ],
        "keywords": ["themes", "morals", "west-african-culture", "gold-coast"]
    },
]


def read_seed():
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def strip_gutenberg(text):
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK WEST AFRICAN FOLK-TALES ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK WEST AFRICAN FOLK-TALES ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]
    return text.strip()


def extract_stories(text):
    """Extract individual stories from the text."""
    stories = []

    # Find position of each story by its title pattern
    positions = []
    for i, sdef in enumerate(STORY_DEFS):
        pattern = sdef["title_pattern"]
        idx = text.find(pattern)
        if idx != -1:
            positions.append((idx, i))
        else:
            # Try partial match for titles that might be slightly different
            # E.g., "HONOURABLE MINŪ" vs "HONOURABLE MIN"
            partial = pattern[:30]
            idx = text.find(partial)
            if idx != -1:
                positions.append((idx, i))
            else:
                print(f"WARNING: Could not find story: {pattern}")

    positions.sort(key=lambda x: x[0])

    # Find end of story content (before NOTES section)
    notes_idx = text.find("\nNOTES\n")
    if notes_idx == -1:
        notes_idx = len(text)

    for pos_idx, (start_pos, def_idx) in enumerate(positions):
        sdef = STORY_DEFS[def_idx]

        if pos_idx + 1 < len(positions):
            end_pos = positions[pos_idx + 1][0]
        else:
            end_pos = notes_idx

        story_text = text[start_pos:end_pos].strip()

        # Remove the title line(s)
        lines = story_text.split('\n')
        content_start = 0
        for j, line in enumerate(lines):
            stripped = line.strip()
            if stripped == '':
                continue
            # Skip all-caps title lines and section headers
            if stripped.upper() == stripped and len(stripped) > 2:
                content_start = j + 1
            elif stripped.startswith('"') and stripped.upper() == stripped:
                content_start = j + 1
            else:
                break

        story_content = '\n'.join(lines[content_start:]).strip()

        # Remove section headers like "I. ANANSI, OR SPIDER, TALES" and "II. MISCELLANEOUS TALES"
        story_content = re.sub(r'^I\. ANANSI, OR SPIDER, TALES\s*\n*', '', story_content)
        story_content = re.sub(r'^II\. MISCELLANEOUS TALES\s*\n*', '', story_content)

        # Remove footnote references [N]
        story_content = re.sub(r'\[(\d+)\]', '', story_content)

        # Remove illustration markers
        story_content = re.sub(r'\[Illustration:.*?\]', '', story_content, flags=re.DOTALL)

        # Remove separator lines
        story_content = re.sub(r'\s*\*\s+\*\s+\*\s+\*\s+\*\s*', '\n\n', story_content)

        # Clean up whitespace
        story_content = re.sub(r'\n{3,}', '\n\n', story_content)
        story_content = story_content.strip()

        stories.append({
            "def_idx": def_idx,
            "text": story_content
        })

    return stories


def build_l1_items(stories):
    items = []
    for sort_order, story in enumerate(stories):
        sdef = STORY_DEFS[story["def_idx"]]
        sections = {
            "Story": story["text"],
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
                "source": "West African Folk-Tales, collected by W. H. Barker and Cecilia Sinclair, 1917"
            }
        }
        items.append(item)
    return items


def build_l2_items(l1_items):
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
    l3_items = []
    sort_order = start_sort_order

    for l3 in L3_DEFS:
        l3_items.append({
            "id": l3["id"],
            "name": l3["name"],
            "sort_order": sort_order,
            "level": 3,
            "category": l3["category"],
            "sections": {"About": l3["about"]},
            "keywords": l3["keywords"],
            "composite_of": l3["composite_of"],
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
                    "name": "W. H. Barker",
                    "date": "1917",
                    "note": "Collector and arranger of West African Folk-Tales"
                },
                {
                    "name": "Cecilia Sinclair",
                    "date": "1917",
                    "note": "Co-collector and illustrator"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure and reflections"
                }
            ]
        },
        "name": "West African Folk-Tales",
        "description": "Thirty-six folk tales from the Gold Coast (modern Ghana), collected and arranged by W. H. Barker and Cecilia Sinclair (1917). Divided into Anansi (Spider) tales and miscellaneous tales, this collection preserves the oral traditions of the Akan, Fanti, and Ashanti peoples. Anansi the Spider — the great trickster of West African folklore — dominates the first half, while the second half features tales of talking animals, magical transformations, and moral lessons. These are the stories that traveled with enslaved Africans to become the Brer Rabbit tales of the American South and the Anansi stories of the Caribbean. Source: Project Gutenberg eBook #66923 (https://www.gutenberg.org/ebooks/66923).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Cecilia Sinclair's twenty-three original pen-and-ink drawings for the 1917 George G. Harrap & Company edition — charming line illustrations depicting native children, Anansi's adventures, and animal characters. The frontispiece shows 'Native Children ready for a Story.'",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "folk-tales", "african", "ghanaian", "folklore", "anansi",
            "trickster", "animals", "origin-stories", "oracle"
        ],
        "roots": ["african-cosmology"],
        "shelves": ["earth"],
        "lineages": ["Akomolafe", "Andreotti"],
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
