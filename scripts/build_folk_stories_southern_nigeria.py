#!/usr/bin/env python3
"""
Parser for Folk Stories from Southern Nigeria by Elphinstone Dayrell (Project Gutenberg #34655).
Outputs grammar.json into grammars/folk-stories-southern-nigeria/
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'folk-stories-southern-nigeria.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'folk-stories-southern-nigeria')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

STORY_DEFS = [
    {
        "num": "I", "id": "tortoise-pretty-daughter",
        "name": "The Tortoise with a Pretty Daughter",
        "keywords": ["tortoise", "beauty", "marriage", "king", "prince", "love", "wisdom"],
        "category": "animal-tales",
        "reflection": "The tortoise's wisdom lies not in cleverness but in recognizing beauty and protecting it. What treasures do you guard even when the world says they are dangerous?"
    },
    {
        "num": "II", "id": "hunter-and-friends",
        "name": "How a Hunter Obtained Money from his Friends the Leopard, Goat, Bush Cat, and Cock",
        "keywords": ["hunter", "leopard", "goat", "bush-cat", "cock", "debt", "trickery"],
        "category": "animal-tales",
        "reflection": "Borrowing from friends can turn friendship into enmity. What happens when trust is broken by unpaid debts?"
    },
    {
        "num": "III", "id": "woman-with-two-skins",
        "name": "The Woman with Two Skins",
        "keywords": ["woman", "beauty", "jealousy", "ju-ju", "magic", "prince", "transformation"],
        "category": "magic-tales",
        "reflection": "Beauty hidden beneath an ugly exterior, and jealousy that destroys — this tale asks us to see beyond appearances. Who do you know whose true beauty is hidden?"
    },
    {
        "num": "IV", "id": "kings-magic-drum",
        "name": "The King's Magic Drum",
        "keywords": ["king", "drum", "magic", "food", "tortoise", "tabu", "consequences"],
        "category": "magic-tales",
        "reflection": "A magic drum that provides abundance — but only if you follow its rules. What blessings in your life come with conditions you must respect?"
    },
    {
        "num": "V", "id": "ituen-and-kings-wife",
        "name": "Ituen and the King's Wife",
        "keywords": ["ituen", "king", "wife", "forbidden-love", "punishment", "egbo"],
        "category": "human-tales",
        "reflection": "Forbidden desire leads to destruction for an entire family line. How do the consequences of one person's choices ripple through generations?"
    },
    {
        "num": "VI", "id": "pretty-stranger-killed-king",
        "name": "Of the Pretty Stranger who Killed the King",
        "keywords": ["stranger", "beauty", "death", "king", "danger", "seduction"],
        "category": "human-tales",
        "reflection": "Beauty can be a weapon as deadly as any sword. When have appearances deceived you about someone's true nature?"
    },
    {
        "num": "VII", "id": "why-bat-flies-by-night",
        "name": "Why the Bat Flies by Night",
        "keywords": ["bat", "bush-rat", "cooking", "shame", "night", "origin"],
        "category": "why-stories",
        "reflection": "The bat hides from daylight out of shame. What small deceptions have you seen lead to lasting consequences?"
    },
    {
        "num": "VIII", "id": "disobedient-daughter-married-skull",
        "name": "The Disobedient Daughter who Married a Skull",
        "keywords": ["daughter", "skull", "death", "disobedience", "marriage", "spirit-world"],
        "category": "spirit-tales",
        "reflection": "A daughter who chooses a handsome stranger against her parents' advice finds herself in the land of the dead. What warnings have you ignored that you later wished you had heeded?"
    },
    {
        "num": "IX", "id": "king-married-cocks-daughter",
        "name": "The King who Married the Cock's Daughter",
        "keywords": ["king", "cock", "daughter", "marriage", "nature", "instinct"],
        "category": "animal-tales",
        "reflection": "You cannot change a creature's true nature through marriage or status. How do people reveal their true selves despite the roles they play?"
    },
    {
        "num": "X", "id": "woman-ape-and-child",
        "name": "Concerning the Woman, the Ape, and the Child",
        "keywords": ["woman", "ape", "child", "law", "justice", "egbo"],
        "category": "human-tales",
        "reflection": "This tale illustrates how law and custom govern even the most primal bonds. When has justice seemed to conflict with what feels right?"
    },
    {
        "num": "XI", "id": "fish-and-leopards-wife",
        "name": "The Fish and the Leopard's Wife; or, Why the Fish Lives in the Water",
        "keywords": ["fish", "leopard", "water", "origin", "betrayal"],
        "category": "why-stories",
        "reflection": "The fish retreats to the water to escape the leopard's anger. What safe places do you retreat to when conflict threatens?"
    },
    {
        "num": "XII", "id": "why-bat-ashamed-daytime",
        "name": "Why the Bat is Ashamed to be Seen in the Daytime",
        "keywords": ["bat", "shame", "debt", "bush-rat", "night", "origin"],
        "category": "why-stories",
        "reflection": "Another tale of the bat's shame — this time over unpaid debts. How does shame shape the way we move through the world?"
    },
    {
        "num": "XIII", "id": "why-worms-live-underground",
        "name": "Why the Worms Live Underneath the Ground",
        "keywords": ["worms", "underground", "origin", "animals"],
        "category": "why-stories",
        "reflection": "Even the smallest creatures have a story about how they came to live where they do. What is the origin story of the place you call home?"
    },
    {
        "num": "XIV", "id": "elephant-and-tortoise",
        "name": "The Elephant and the Tortoise; or, Why the Worms are Blind and the Elephant has Small Eyes",
        "keywords": ["elephant", "tortoise", "worms", "eyes", "origin", "wisdom"],
        "category": "why-stories",
        "reflection": "The tortoise's wisdom outmatches the elephant's size. How does cunning compare to strength in the challenges you face?"
    },
    {
        "num": "XV", "id": "why-hawk-kills-chickens",
        "name": "Why a Hawk Kills Chickens",
        "keywords": ["hawk", "chicken", "betrayal", "origin", "predator"],
        "category": "why-stories",
        "reflection": "A broken promise turns a friend into a predator. What friendships have you seen destroyed by broken trust?"
    },
    {
        "num": "XVI", "id": "why-sun-and-moon-live-in-sky",
        "name": "Why the Sun and the Moon Live in the Sky",
        "keywords": ["sun", "moon", "water", "sky", "origin", "hospitality"],
        "category": "why-stories",
        "reflection": "The sun invited water into his home, and water filled it to overflowing. What happens when generosity meets an overwhelming guest?"
    },
    {
        "num": "XVII", "id": "why-flies-bother-cows",
        "name": "Why the Flies Bother the Cows",
        "keywords": ["flies", "cows", "origin", "annoyance"],
        "category": "why-stories",
        "reflection": "Small irritations often have deep roots. What minor annoyances in your life might have a story behind them?"
    },
    {
        "num": "XVIII", "id": "why-cat-kills-rats",
        "name": "Why the Cat Kills Rats",
        "keywords": ["cat", "rat", "enmity", "origin", "betrayal"],
        "category": "why-stories",
        "reflection": "The ancient enmity between cat and rat begins with a broken bond. What feuds in your world started from a single betrayal?"
    },
    {
        "num": "XIX", "id": "lightning-and-thunder",
        "name": "The Story of the Lightning and the Thunder",
        "keywords": ["lightning", "thunder", "storm", "origin", "mother-son", "destruction"],
        "category": "why-stories",
        "reflection": "Lightning is a wild son whose mother Thunder follows, trying to control him. How do parents manage children whose power exceeds their wisdom?"
    },
    {
        "num": "XX", "id": "bush-cow-and-elephant",
        "name": "Why the Bush Cow and the Elephant are Bad Friends",
        "keywords": ["bush-cow", "elephant", "enmity", "origin", "conflict"],
        "category": "why-stories",
        "reflection": "Even the mightiest creatures have their rivalries. What conflicts between powerful forces have you witnessed?"
    },
    {
        "num": "XXI", "id": "cock-caused-fight-between-towns",
        "name": "The Cock who Caused a Fight Between Two Towns",
        "keywords": ["cock", "fight", "towns", "war", "justice", "egbo"],
        "category": "human-tales",
        "reflection": "A small incident escalates into a war between communities. How do minor disputes grow into major conflicts?"
    },
    {
        "num": "XXII", "id": "hippopotamus-and-tortoise",
        "name": "The Affair of the Hippopotamus and the Tortoise; or, Why the Hippopotamus Lives in the Water",
        "keywords": ["hippopotamus", "tortoise", "name", "secret", "water", "origin"],
        "category": "why-stories",
        "reflection": "The power of knowing someone's secret name — knowledge as power. What secrets give people power over others?"
    },
    {
        "num": "XXIII", "id": "why-dead-people-are-buried",
        "name": "Why Dead People are Buried",
        "keywords": ["death", "burial", "creator", "origin", "worm"],
        "category": "why-stories",
        "reflection": "This origin myth explains humanity's relationship with death itself. How do different cultures make sense of death and burial?"
    },
    {
        "num": "XXIV", "id": "fat-woman-who-melted-away",
        "name": "Of the Fat Woman who Melted Away",
        "keywords": ["woman", "beauty", "melting", "sun", "resurrection", "magic"],
        "category": "magic-tales",
        "reflection": "A woman so beautiful she melts in the sun, yet can be revived from a single toe. What does it mean to be so delicate that the world itself can destroy you?"
    },
    {
        "num": "XXV", "id": "leopard-squirrel-and-tortoise",
        "name": "Concerning the Leopard, the Squirrel, and the Tortoise",
        "keywords": ["leopard", "squirrel", "tortoise", "cunning", "origin"],
        "category": "animal-tales",
        "reflection": "Cunning and quick-thinking save the small from the powerful. How do the clever survive among the strong?"
    },
    {
        "num": "XXVI", "id": "why-moon-waxes-and-wanes",
        "name": "Why the Moon Waxes and Wanes",
        "keywords": ["moon", "sun", "waxing", "waning", "origin", "cosmic"],
        "category": "why-stories",
        "reflection": "The moon's changing face tells a story of cosmic relationships. How do cycles of growth and decline shape your own life?"
    },
    {
        "num": "XXVII", "id": "leopard-tortoise-and-bush-rat",
        "name": "The Story of the Leopard, the Tortoise, and the Bush Rat",
        "keywords": ["leopard", "tortoise", "bush-rat", "cunning", "survival"],
        "category": "animal-tales",
        "reflection": "In the animal world, every creature must use its gifts to survive. What unique gift do you bring to difficult situations?"
    },
    {
        "num": "XXVIII", "id": "king-and-ju-ju-tree",
        "name": "The King and the Ju Ju Tree",
        "keywords": ["king", "ju-ju", "tree", "spirit", "sacrifice", "princess", "spirit-world"],
        "category": "spirit-tales",
        "reflection": "The princess must journey to the spirit world and follow strict instructions to return safely. What rules must you follow when entering unfamiliar territory?"
    },
    {
        "num": "XXIX", "id": "tortoise-overcame-elephant-and-hippo",
        "name": "How the Tortoise Overcame the Elephant and the Hippopotamus",
        "keywords": ["tortoise", "elephant", "hippopotamus", "cunning", "trickery", "strength"],
        "category": "animal-tales",
        "reflection": "The tortoise defeats two giants through wit alone. When has cleverness accomplished what strength could not?"
    },
    {
        "num": "XXX", "id": "pretty-girl-and-seven-jealous-women",
        "name": "Of the Pretty Girl and the Seven Jealous Women",
        "keywords": ["girl", "jealousy", "women", "beauty", "revenge", "bird"],
        "category": "human-tales",
        "reflection": "Seven jealous women conspire against beauty. How does jealousy corrupt those who harbor it?"
    },
    {
        "num": "XXXI", "id": "cannibals-insofan-mountain",
        "name": "How the Cannibals Drove the People from Insofan Mountain to the Cross River",
        "keywords": ["cannibals", "mountain", "migration", "fear", "sacrifice"],
        "category": "human-tales",
        "reflection": "Fear of cannibals drives an entire people from their homeland. What forces have driven communities from the places they loved?"
    },
    {
        "num": "XXXII", "id": "lucky-fisherman",
        "name": "The Lucky Fisherman",
        "keywords": ["fisherman", "luck", "fortune", "river"],
        "category": "human-tales",
        "reflection": "Sometimes fortune smiles on the least likely person. When has luck changed the course of your life?"
    },
    {
        "num": "XXXIII", "id": "orphan-boy-and-magic-stone",
        "name": "The Orphan Boy and the Magic Stone",
        "keywords": ["orphan", "magic", "stone", "witch", "justice", "poison-ordeal"],
        "category": "magic-tales",
        "reflection": "An orphan's magic stone reveals the truth about witchcraft. How do the powerless find tools to defend themselves?"
    },
    {
        "num": "XXXIV", "id": "slave-girl-kill-mistress",
        "name": "The Slave Girl who Tried to Kill her Mistress",
        "keywords": ["slave", "girl", "mistress", "betrayal", "false-bride", "resurrection"],
        "category": "human-tales",
        "reflection": "The false bride usurps the true one's place, but truth rises from the water. How does the truth eventually surface even when buried?"
    },
    {
        "num": "XXXV", "id": "king-and-nsiat-bird",
        "name": "The King and the 'Nsiat Bird",
        "keywords": ["king", "bird", "nsiat", "twins", "origin"],
        "category": "why-stories",
        "reflection": "This tale connects to the once-widespread practice of killing twins. How do customs that seem cruel arise, and how are they challenged?"
    },
    {
        "num": "XXXVI", "id": "fate-of-essido",
        "name": "Concerning the Fate of Essido and his Evil Companions",
        "keywords": ["essido", "evil", "companions", "punishment", "poison", "ordeal"],
        "category": "human-tales",
        "reflection": "Evil companions lead Essido to his doom. How do the people you surround yourself with shape your fate?"
    },
    {
        "num": "XXXVII", "id": "hawk-and-owl",
        "name": "Concerning the Hawk and the Owl",
        "keywords": ["hawk", "owl", "enmity", "origin", "birds"],
        "category": "why-stories",
        "reflection": "The hawk and owl become enemies, dividing day and night between them. How do rivals carve up territory to avoid conflict?"
    },
    {
        "num": "XXXVIII", "id": "drummer-and-alligators",
        "name": "The Story of the Drummer and the Alligators",
        "keywords": ["drummer", "alligator", "secret-society", "danger", "music"],
        "category": "spirit-tales",
        "reflection": "A drummer encounters the terrifying world of secret societies. What hidden powers operate beneath the surface of your community?"
    },
    {
        "num": "XXXIX", "id": "nsasak-bird-and-odudu-bird",
        "name": "The 'Nsasak Bird and the Odudu Bird",
        "keywords": ["nsasak", "odudu", "birds", "origin", "competition"],
        "category": "why-stories",
        "reflection": "Two birds whose rivalry explains the natural world. What competing forces in nature do you observe?"
    },
    {
        "num": "XL", "id": "election-of-king-bird",
        "name": "The Election of the King Bird",
        "keywords": ["birds", "king", "election", "eagle", "competition", "leadership"],
        "category": "animal-tales",
        "reflection": "All the birds compete to choose their king through combat. What makes a good leader — strength, wisdom, or something else entirely?"
    },
]


# L2 theme groupings
THEME_GROUPS = [
    {
        "id": "theme-why-the-world-is-so",
        "name": "Why the World Is So: Origin Stories",
        "category": "themes",
        "about": "The largest group of stories in this collection explains why things are the way they are — why the bat flies at night, why the sun lives in the sky, why the moon waxes and wanes, why hawks kill chickens. These 'Just So Stories' of Southern Nigeria reveal a worldview where every feature of the natural world has a narrative explanation rooted in character, conflict, and consequence.",
        "for_readers": "These origin stories are not just entertainment — they represent a way of understanding the world through narrative rather than analysis. Each story encodes an observation about nature (bats are nocturnal, cats hunt rats) and wraps it in a moral or social lesson. Read them as a window into how people made sense of the world before science, and notice how many of the moral lessons still apply.",
        "member_ids": [
            "why-bat-flies-by-night", "why-bat-ashamed-daytime", "why-worms-live-underground",
            "elephant-and-tortoise", "why-hawk-kills-chickens", "why-sun-and-moon-live-in-sky",
            "why-flies-bother-cows", "why-cat-kills-rats", "lightning-and-thunder",
            "bush-cow-and-elephant", "hippopotamus-and-tortoise", "why-dead-people-are-buried",
            "why-moon-waxes-and-wanes", "fish-and-leopards-wife", "hawk-and-owl",
            "nsasak-bird-and-odudu-bird", "king-and-nsiat-bird"
        ],
        "keywords": ["origin", "nature", "animals", "explanation", "just-so"]
    },
    {
        "id": "theme-tortoise-wisdom",
        "name": "The Wisdom of the Tortoise",
        "category": "themes",
        "about": "The tortoise is the trickster hero of Southern Nigerian folk tales, revered as 'the wisest of all men and animals.' Like Anansi the Spider in West African tradition or Brer Rabbit in the American South, the tortoise uses cunning, patience, and strategic thinking to overcome creatures far larger and more powerful than himself. These tales celebrate intelligence over brute force.",
        "for_readers": "The tortoise tales show a consistent philosophy: in a world of leopards and elephants, the small and clever survive through wit. Notice how the tortoise's wisdom is not always moral — sometimes he tricks, cheats, or manipulates. These are survival stories from a world where power is dangerous and the powerless must be resourceful.",
        "member_ids": [
            "tortoise-pretty-daughter", "kings-magic-drum", "leopard-squirrel-and-tortoise",
            "leopard-tortoise-and-bush-rat", "tortoise-overcame-elephant-and-hippo",
            "hippopotamus-and-tortoise", "elephant-and-tortoise"
        ],
        "keywords": ["tortoise", "wisdom", "cunning", "trickster", "survival"]
    },
    {
        "id": "theme-beauty-and-danger",
        "name": "Beauty, Marriage, and Danger",
        "category": "themes",
        "about": "Many tales in this collection revolve around beautiful women, marriage customs, and the dangers that beauty attracts. From the tortoise's pretty daughter to the disobedient girl who married a skull, these stories explore how beauty, desire, and social convention intertwine — often with deadly consequences. They reflect the bride-price system, the power dynamics of marriage, and the perils of transgressing social boundaries.",
        "for_readers": "These stories reveal how deeply marriage and beauty were woven into the social fabric of Southern Nigerian communities. The bride-price system, the role of the king's authority over marriage, and the fatal consequences of disobedience all reflect real social structures. Read them as both entertainment and social commentary.",
        "member_ids": [
            "tortoise-pretty-daughter", "woman-with-two-skins", "pretty-stranger-killed-king",
            "disobedient-daughter-married-skull", "king-married-cocks-daughter",
            "fat-woman-who-melted-away", "pretty-girl-and-seven-jealous-women",
            "slave-girl-kill-mistress"
        ],
        "keywords": ["beauty", "marriage", "danger", "bride-price", "women"]
    },
    {
        "id": "theme-spirit-world",
        "name": "The Spirit World and Ju Ju Power",
        "category": "themes",
        "about": "A distinct set of tales deals with the spirit world — Ju Ju trees, the land of the dead, secret societies, and the terrifying power of Egbo. These stories feature journeys to the spirit realm, encounters with supernatural beings, and the strict rules that govern contact between the living and the dead. They reveal a world saturated with spiritual power, where the boundary between the living and the dead is thin and dangerous.",
        "for_readers": "The Ju Ju and Egbo references in these stories are not mere fantasy — they reflect real spiritual and political institutions of the Cross River region. The Egbo societies wielded real judicial power, and Ju Ju (spiritual power invested in objects and places) was a lived reality. These tales encode both wonder and warning about powers beyond ordinary human control.",
        "member_ids": [
            "disobedient-daughter-married-skull", "king-and-ju-ju-tree",
            "drummer-and-alligators", "fate-of-essido", "woman-with-two-skins",
            "orphan-boy-and-magic-stone"
        ],
        "keywords": ["spirit", "ju-ju", "egbo", "dead", "supernatural", "secret-society"]
    },
    {
        "id": "theme-justice-and-power",
        "name": "Justice, Power, and Social Order",
        "category": "themes",
        "about": "Several tales explore the workings of justice, kingship, and social power in Calabar society. Kings make laws, Egbo societies enforce them, and individuals navigate a world where power can be capricious and punishment severe. These tales portray a society grappling with questions of authority, fairness, and the consequences of transgression.",
        "for_readers": "These stories provide a window into the political structures of pre-colonial Southern Nigeria. The king's word is law, but even kings must negotiate with the Egbo societies. Justice can be swift and brutal, but it follows its own logic. Read these as case studies in how societies balance power, law, and individual freedom.",
        "member_ids": [
            "ituen-and-kings-wife", "cock-caused-fight-between-towns",
            "woman-ape-and-child", "cannibals-insofan-mountain",
            "lucky-fisherman", "hunter-and-friends"
        ],
        "keywords": ["justice", "power", "king", "law", "egbo", "punishment"]
    },
]

CHARACTER_GROUPS = [
    {
        "id": "characters-birds",
        "name": "Bird Stories",
        "category": "characters",
        "about": "Birds feature prominently in Southern Nigerian folklore — from the bat (who cannot decide if he is bird or beast) to the hawk, owl, nsiat, and the grand election of the king bird. Each bird carries its own personality and its own origin mystery.",
        "for_readers": "Southern Nigerian birds are characters with human-like motivations. The bat's shame, the hawk's betrayal, the owl's nocturnal habits — each is explained through a story of character and consequence. Watch how birds serve as mirrors for human behavior.",
        "member_ids": [
            "why-bat-flies-by-night", "why-bat-ashamed-daytime", "why-hawk-kills-chickens",
            "hawk-and-owl", "nsasak-bird-and-odudu-bird", "election-of-king-bird",
            "king-and-nsiat-bird"
        ],
        "keywords": ["birds", "bat", "hawk", "owl", "eagle"]
    },
    {
        "id": "characters-big-beasts",
        "name": "The Great Beasts: Elephant, Leopard, and Hippopotamus",
        "category": "characters",
        "about": "The great beasts of Southern Nigeria — elephant, leopard, and hippopotamus — appear as powerful but often outwitted characters. The leopard is fierce but foolish, the elephant is strong but vain, and the hippopotamus guards his secret name. These animals represent raw power in a world where cunning matters more.",
        "for_readers": "Notice how the largest, most powerful animals are rarely the heroes. The elephant has small eyes because the tortoise outwitted him. The hippopotamus hides in water because the tortoise learned his name. Power without wisdom is a vulnerability in these tales.",
        "member_ids": [
            "elephant-and-tortoise", "bush-cow-and-elephant",
            "leopard-squirrel-and-tortoise", "leopard-tortoise-and-bush-rat",
            "tortoise-overcame-elephant-and-hippo", "hippopotamus-and-tortoise",
            "fish-and-leopards-wife", "hunter-and-friends"
        ],
        "keywords": ["elephant", "leopard", "hippopotamus", "power", "beasts"]
    },
]

L3_DEFS = [
    {
        "id": "meta-themes",
        "name": "Themes and Teachings",
        "category": "meta",
        "about": "The thematic currents of Southern Nigerian folk tales: origin myths that explain the natural world, the trickster wisdom of the tortoise, the dangerous intersection of beauty and marriage, the power of the spirit world, and the social dynamics of justice and authority. Together they reveal a rich, complex worldview where every creature, every natural phenomenon, and every social custom has its story.",
        "composite_of": [
            "theme-why-the-world-is-so", "theme-tortoise-wisdom",
            "theme-beauty-and-danger", "theme-spirit-world",
            "theme-justice-and-power"
        ],
        "keywords": ["themes", "morals", "nigerian-culture", "calabar"]
    },
    {
        "id": "meta-characters",
        "name": "Character Types",
        "category": "meta",
        "about": "The cast of characters in Southern Nigerian folklore: clever tortoises, powerful but outwitted beasts, birds with their own origin mysteries, and humans caught between the forces of beauty, power, and the spirit world. These character types reflect the social and natural world of the Cross River region.",
        "composite_of": [
            "characters-birds", "characters-big-beasts"
        ],
        "keywords": ["characters", "archetypes", "animals"]
    }
]


def read_seed():
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK FOLK STORIES FROM SOUTHERN NIGERIA, WEST AFRICA ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK FOLK STORIES FROM SOUTHERN NIGERIA, WEST AFRICA ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]
    return text.strip()


def find_story_starts(text):
    """Find the start positions of each story using Roman numeral patterns."""
    lines = text.split('\n')
    roman_map = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^[IVX]+$', stripped) and len(stripped) <= 7:
            # Check if next non-blank line starts with underscore (title)
            for j in range(i+1, min(i+4, len(lines))):
                if lines[j].strip():
                    if lines[j].strip().startswith('_') or lines[j].strip().startswith('FOLK STORIES'):
                        roman_map[stripped] = i
                    break
    return lines, roman_map


def extract_stories(text):
    """Extract individual stories from the text."""
    lines = text.split('\n')

    # Find the first story (Roman numeral I on its own line after the introduction)
    story_positions = []
    roman_nums = [s["num"] for s in STORY_DEFS]

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in roman_nums:
            # Verify next non-blank line starts with underscore (story title)
            for j in range(i+1, min(i+4, len(lines))):
                next_line = lines[j].strip()
                if next_line:
                    if next_line.startswith('_'):
                        story_positions.append((stripped, i))
                    break

    stories = []
    for idx, (roman, start_line) in enumerate(story_positions):
        # Find the matching story def
        sdef = None
        for sd in STORY_DEFS:
            if sd["num"] == roman:
                sdef = sd
                break
        if not sdef:
            continue

        # Find end of story
        if idx + 1 < len(story_positions):
            end_line = story_positions[idx + 1][1]
        else:
            end_line = len(lines)

        # Extract story text
        story_lines = lines[start_line:end_line]

        # Skip the Roman numeral line and title line(s)
        content_start = 0
        in_title = True
        for k, sl in enumerate(story_lines):
            s = sl.strip()
            if not s:
                if not in_title:
                    continue
                continue
            if in_title:
                # Skip Roman numeral, title (in underscores), subtitle lines
                if re.match(r'^[IVX]+$', s):
                    content_start = k + 1
                    continue
                if s.startswith('_') and s.endswith('_'):
                    content_start = k + 1
                    continue
                if s.startswith('_'):
                    # Multi-line title
                    content_start = k + 1
                    continue
                if s.endswith('_'):
                    content_start = k + 1
                    in_title = False
                    continue
                in_title = False
                content_start = k
                break
            break

        story_text = '\n'.join(story_lines[content_start:]).strip()

        # Remove footnotes
        story_text = re.sub(r'\[Footnote \d+:.*?\]', '', story_text, flags=re.DOTALL)
        story_text = re.sub(r'\[\d+\]', '', story_text)

        # Remove illustration markers
        story_text = re.sub(r'\[Illustration:.*?\]', '', story_text, flags=re.DOTALL)

        # Remove separator lines
        story_text = re.sub(r'\s*\*\s+\*\s+\*\s+\*\s+\*\s*', '\n\n', story_text)

        # Clean up whitespace
        story_text = re.sub(r'\n{3,}', '\n\n', story_text)
        story_text = story_text.strip()

        # Extract moral if present
        moral = ""
        moral_match = re.search(r'MORAL\.--(.+?)(?:\n\n|\Z)', story_text, re.DOTALL)
        if moral_match:
            moral = moral_match.group(1).strip()
            story_text = story_text[:moral_match.start()].strip()

        stories.append({
            "sdef": sdef,
            "text": story_text,
            "moral": moral
        })

    return stories


def build_l1_items(stories):
    items = []
    for sort_order, story in enumerate(stories):
        sdef = story["sdef"]
        sections = {"Story": story["text"]}
        if story["moral"]:
            sections["Moral"] = story["moral"]
        sections["Reflection"] = sdef["reflection"]

        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "level": 1,
            "category": sdef["category"],
            "sections": sections,
            "keywords": sdef["keywords"],
            "metadata": {
                "source": "Folk Stories from Southern Nigeria, by Elphinstone Dayrell, 1910"
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

    for group in CHARACTER_GROUPS:
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
                    "name": "Elphinstone Dayrell",
                    "date": "1910",
                    "note": "Collector and author of Folk Stories from Southern Nigeria"
                },
                {
                    "name": "Andrew Lang",
                    "date": "1910",
                    "note": "Author of the Introduction"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure and reflections"
                }
            ]
        },
        "name": "Folk Stories from Southern Nigeria",
        "description": "Forty folk stories from the Cross River region of Southern Nigeria, collected by Elphinstone Dayrell, District Commissioner, with an introduction by Andrew Lang (1910). These tales from the Efik and Ibibio peoples feature the cunning tortoise as trickster hero, powerful Ju Ju magic, the fearsome Egbo secret societies, and a rich bestiary of animal characters whose conflicts explain the origins of the natural world. The stories blend earthy humor with moral instruction, supernatural terror with social commentary, and reveal a complex civilization where beauty is dangerous, wisdom is survival, and every creature has its story. Source: Project Gutenberg eBook #34655 (https://www.gutenberg.org/ebooks/34655).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Major G. M. de L. Dayrell's color drawing of a Ju-Ju mask from Ibo Country (frontispiece of the 1910 Longmans, Green and Co. edition). The original 1910 edition contains no other illustrations but the mask drawing is a striking representation of the spiritual world these tales inhabit.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "folk-tales", "african", "nigerian", "folklore", "animals",
            "trickster", "origin-stories", "tortoise", "oracle"
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
