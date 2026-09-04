#!/usr/bin/env python3
"""
Parser for Indian Fairy Tales compiled by Joseph Jacobs (Project Gutenberg #7128).
Outputs grammar.json into grammars/indian-fairy-tales/
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'indian-fairy-tales.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'indian-fairy-tales')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

STORY_DEFS = [
    {
        "title": "The Lion and the Crane",
        "id": "lion-and-crane",
        "name": "The Lion and the Crane",
        "keywords": ["lion", "crane", "ingratitude", "jataka", "buddha", "service"],
        "themes": ["animal-fables", "wisdom"],
        "reflection": "The crane saves the lion's life, but the lion offers only contempt in return. This Jataka tale teaches that some beings are incapable of gratitude — and that wisdom lies in knowing when to walk away."
    },
    {
        "title": "How the Raja's Son won the Princess Labam.",
        "id": "rajas-son-princess-labam",
        "name": "How the Raja's Son Won the Princess Labam",
        "keywords": ["prince", "princess", "magic", "quest", "love", "fakir"],
        "themes": ["quest-tales", "love-tales"],
        "reflection": "A prince's journey to win Princess Labam takes him through trials of patience and magic. True love in this tale requires not just desire but endurance and the willingness to follow guidance."
    },
    {
        "title": "The Lambikin",
        "id": "the-lambikin",
        "name": "The Lambikin",
        "keywords": ["lamb", "drumikin", "cleverness", "journey", "animals", "song"],
        "themes": ["animal-fables", "wit-tales"],
        "reflection": "The clever Lambikin outsmarts predator after predator with a song and a rolling drum. But what happens when cleverness meets its match? Sometimes the last trick is the one that fails."
    },
    {
        "title": "Punchkin",
        "id": "punchkin",
        "name": "Punchkin",
        "keywords": ["punchkin", "seven-queens", "magic", "parrot", "rescue", "evil"],
        "themes": ["quest-tales", "magic-tales"],
        "reflection": "The evil magician Punchkin's life is hidden in a parrot, in a cage, on a tree — echoing the worldwide motif of the external soul. What does it mean when your deepest vulnerability is hidden in the most distant and unexpected place?"
    },
    {
        "title": "The Broken Pot",
        "id": "the-broken-pot",
        "name": "The Broken Pot",
        "keywords": ["pot", "daydream", "poverty", "plans", "folly"],
        "themes": ["wisdom", "wit-tales"],
        "reflection": "A poor man builds an entire future on the profits of a pot of rice — until the pot breaks. This famous tale warns against counting chickens before they hatch, and reminds us that dreams without action are castles in the air."
    },
    {
        "title": "The Magic Fiddle",
        "id": "the-magic-fiddle",
        "name": "The Magic Fiddle",
        "keywords": ["fiddle", "sisters", "transformation", "bamboo", "jealousy"],
        "themes": ["magic-tales", "family-tales"],
        "reflection": "A murdered sister's spirit lives on in a bamboo fiddle that sings the truth. This haunting tale shows that injustice cannot remain hidden forever — the truth will find a way to be heard."
    },
    {
        "title": "The Cruel Crane Outwitted",
        "id": "cruel-crane-outwitted",
        "name": "The Cruel Crane Outwitted",
        "keywords": ["crane", "crab", "fish", "trickery", "jataka", "justice"],
        "themes": ["animal-fables", "wisdom"],
        "reflection": "A crane pretends to help fish by carrying them to a new lake, but devours them instead — until the crab turns the tables. In this Jataka tale, the trickster meets a trickster, and justice arrives with a snap of claws."
    },
    {
        "title": "Loving Laili",
        "id": "loving-laili",
        "name": "Loving Laili",
        "keywords": ["laili", "majnun", "love", "devotion", "separation", "fate"],
        "themes": ["love-tales"],
        "reflection": "The legendary love of Laili and Majnun — a devotion so intense it transcends reason, society, and even death. What does it mean to love so completely that the world itself becomes irrelevant?"
    },
    {
        "title": "The Tiger, the Brahman, and the Jackal",
        "id": "tiger-brahman-jackal",
        "name": "The Tiger, the Brahman, and the Jackal",
        "keywords": ["tiger", "brahman", "jackal", "cleverness", "justice", "trickery"],
        "themes": ["animal-fables", "wit-tales"],
        "reflection": "The Brahman frees a tiger, who then wants to eat him. Only the clever jackal can solve this dilemma — by pretending to be too stupid to understand. Sometimes the best weapon against power is apparent foolishness."
    },
    {
        "title": "The Soothsayer's Son",
        "id": "soothsayers-son",
        "name": "The Soothsayer's Son",
        "keywords": ["soothsayer", "fate", "prophecy", "prince", "death", "destiny"],
        "themes": ["quest-tales", "wisdom"],
        "reflection": "A father reads his own son's fate in the stars — ten years of poverty, ten years of imprisonment, death by the sea-shore. Can destiny be outrun, or must we learn to walk through it?"
    },
    {
        "title": "Harisarman",
        "id": "harisarman",
        "name": "Harisarman",
        "keywords": ["harisarman", "brahman", "fraud", "luck", "cleverness", "detective"],
        "themes": ["wit-tales"],
        "reflection": "A poor Brahman bluffs his way to fame as a detective through sheer luck and quick thinking. Harisarman is a lovable fraud who reminds us that sometimes fortune favors the bold — and the brazen."
    },
    {
        "title": "The Charmed Ring",
        "id": "the-charmed-ring",
        "name": "The Charmed Ring",
        "keywords": ["ring", "magic", "dog", "cat", "snake", "gratitude", "prince"],
        "themes": ["magic-tales", "quest-tales"],
        "reflection": "A prince saves a snake and receives a wishing ring, but loses it through the treachery of his wife. His faithful dog and cat journey to recover it. This tale celebrates the loyalty of animals and the fickleness of fortune."
    },
    {
        "title": "The Talkative Tortoise",
        "id": "talkative-tortoise",
        "name": "The Talkative Tortoise",
        "keywords": ["tortoise", "geese", "talking", "silence", "jataka", "folly"],
        "themes": ["animal-fables", "wisdom"],
        "reflection": "A tortoise convinces two geese to carry him by holding a stick in his mouth — but he cannot resist talking, and falls to his death. The simplest lessons are often the hardest to learn: sometimes silence is survival."
    },
    {
        "title": "A Lac of Rupees for a Bit of Advice",
        "id": "lac-of-rupees",
        "name": "A Lac of Rupees for a Piece of Advice",
        "keywords": ["advice", "rupees", "wisdom", "patience", "merchant"],
        "themes": ["wisdom"],
        "reflection": "A merchant pays a fortune for three pieces of advice — and each one saves his life at a crucial moment. The most expensive wisdom is the wisdom we refuse to hear until we need it most."
    },
    {
        "title": "The Gold-giving Serpent",
        "id": "gold-giving-serpent",
        "name": "The Gold-Giving Serpent",
        "keywords": ["serpent", "gold", "greed", "farmer", "respect"],
        "themes": ["animal-fables", "wisdom"],
        "reflection": "A farmer discovers that a serpent will give gold coins in exchange for offerings of milk — but greed destroys the arrangement. This tale teaches that reciprocity requires respect, and that trying to take more than is offered destroys the gift."
    },
    {
        "title": "The Son of Seven Queens",
        "id": "son-of-seven-queens",
        "name": "The Son of Seven Queens",
        "keywords": ["prince", "queens", "step-mother", "magic", "truth", "justice"],
        "themes": ["quest-tales", "family-tales"],
        "reflection": "A prince born to seven imprisoned queens must uncover the truth of his origins and free his mothers. This tale of hidden identity and patient justice shows that truth, though buried, always rises."
    },
    {
        "title": "A Lesson for Kings",
        "id": "lesson-for-kings",
        "name": "A Lesson for Kings",
        "keywords": ["king", "lesson", "justice", "jataka", "wisdom", "foolishness"],
        "themes": ["wisdom", "animal-fables"],
        "reflection": "This Jataka tale teaches kings — and all who hold power — that wisdom lies in seeing things as they truly are, not as flattery would have us believe."
    },
    {
        "title": "Pride goeth before a Fall",
        "id": "pride-before-fall",
        "name": "Pride Goeth Before a Fall",
        "keywords": ["pride", "fall", "jataka", "lion", "foolishness"],
        "themes": ["wisdom", "animal-fables"],
        "reflection": "Pride blinds us to our own vulnerability. This tale reminds us that the higher we climb on the ladder of self-importance, the harder we fall."
    },
    {
        "title": "Raja Rasalu.",
        "id": "raja-rasalu",
        "name": "Raja Rasalu",
        "keywords": ["raja-rasalu", "hero", "chaupur", "quest", "courage", "punjab"],
        "themes": ["quest-tales"],
        "reflection": "Raja Rasalu is one of India's great legendary heroes — a prince who wanders the land facing challenges of wit and courage. His story celebrates the hero who fights not just with weapons but with intelligence and integrity."
    },
    {
        "title": "The Ass in the Lion's Skin",
        "id": "ass-in-lions-skin",
        "name": "The Ass in the Lion's Skin",
        "keywords": ["donkey", "lion", "disguise", "jataka", "pretense", "exposure"],
        "themes": ["animal-fables", "wisdom"],
        "reflection": "An ass wraps himself in a lion's skin and terrifies the countryside — until his bray gives him away. We can wear any mask we like, but sooner or later, our true nature reveals itself."
    },
    {
        "title": "The Farmer and the Money-lender",
        "id": "farmer-and-moneylender",
        "name": "The Farmer and the Money-Lender",
        "keywords": ["farmer", "money-lender", "justice", "cleverness", "poverty"],
        "themes": ["wit-tales", "wisdom"],
        "reflection": "A clever farmer outwits a greedy money-lender who tries to cheat him. This tale delights in the triumph of the common person over corrupt power through sheer resourcefulness."
    },
    {
        "title": "The Boy who had a Moon on his Forehead and a Star on his Chin",
        "id": "boy-moon-forehead-star-chin",
        "name": "The Boy Who Had a Moon on His Forehead and a Star on His Chin",
        "keywords": ["moon", "star", "prince", "magic", "identity", "quest"],
        "themes": ["quest-tales", "magic-tales"],
        "reflection": "A boy marked by celestial signs must find his true identity and place in the world. The moon and star are signs that cannot be hidden — just as our true nature will always shine through, no matter how we are disguised."
    },
    {
        "title": "The Prince and the Fakir",
        "id": "prince-and-fakir",
        "name": "The Prince and the Fakir",
        "keywords": ["prince", "fakir", "magic", "quest", "transformation"],
        "themes": ["quest-tales", "magic-tales"],
        "reflection": "A prince and a holy man cross paths in a tale of magical transformation and spiritual testing. The encounter between worldly power and spiritual power reveals what each truly values."
    },
    {
        "title": "Why the Fish Laughed.",
        "id": "why-fish-laughed",
        "name": "Why the Fish Laughed",
        "keywords": ["fish", "laughter", "queen", "mystery", "disguise", "cleverness"],
        "themes": ["wit-tales", "wisdom"],
        "reflection": "A fish laughs at the king's court, and the mystery of its laughter sets off a chain of discoveries about hidden truths and disguised identities. Sometimes the most unsettling questions lead to the most important answers."
    },
    {
        "title": "The Demon with the Matted Hair",
        "id": "demon-matted-hair",
        "name": "The Demon with the Matted Hair",
        "keywords": ["demon", "hair", "jataka", "wisdom", "non-violence", "compassion"],
        "themes": ["wisdom"],
        "reflection": "A prince faces a demon who cannot be defeated by violence — only by non-resistance and wisdom. This profound Jataka tale teaches that the greatest victory is won not by fighting but by understanding."
    },
    {
        "title": "The Ivory City and its Fairy Princess",
        "id": "ivory-city-fairy-princess",
        "name": "The Ivory City and Its Fairy Princess",
        "keywords": ["ivory-city", "fairy", "princess", "prince", "magic", "adventure"],
        "themes": ["quest-tales", "love-tales"],
        "reflection": "A prince journeys to a magical ivory city where a fairy princess dwells. This sprawling adventure tale takes the hero through dangers, enchantments, and the bewildering landscape of desire."
    },
    {
        "title": "How Sun, Moon, and Wind went out to Dinner",
        "id": "sun-moon-wind-dinner",
        "name": "Sun, Moon, and Wind Go Out to Dinner",
        "keywords": ["sun", "moon", "wind", "dinner", "sharing", "selfishness", "mother-star"],
        "themes": ["wisdom", "family-tales"],
        "reflection": "Sun and Wind feast selfishly at their uncle's dinner, while Moon brings food home for her mother, the Star. This simple tale carries a luminous moral: those who share are blessed, and those who hoard are cursed."
    },
    {
        "title": "How the Wicked Sons were Duped.",
        "id": "wicked-sons-duped",
        "name": "How the Wicked Sons Were Duped",
        "keywords": ["sons", "father", "greed", "treasure", "justice", "cleverness"],
        "themes": ["wisdom", "family-tales"],
        "reflection": "Wicked sons who mistreat their father are taught a lesson they will never forget. This tale celebrates the cunning of the old and the comeuppance of the ungrateful."
    },
    {
        "title": "The Pigeon and the Crow",
        "id": "pigeon-and-crow",
        "name": "The Pigeon and the Crow",
        "keywords": ["pigeon", "crow", "greed", "hospitality", "jataka", "punishment"],
        "themes": ["animal-fables"],
        "reflection": "A crow abuses the hospitality of a pigeon and suffers the consequences. The lesson is ancient and universal: do not mistake kindness for weakness, and do not repay generosity with greed."
    },
]

THEME_GROUPS = [
    {
        "id": "theme-animal-fables",
        "name": "Animal Fables and Jataka Tales",
        "category": "themes",
        "about": "Many of these tales come from the Jatakas, the Buddhist birth stories — the oldest collection of folk tales in the world, gathered more than two thousand years ago. Lions, cranes, crows, tortoises, and asses act out dramas of ingratitude, cleverness, pride, and justice. These fables are the ancestors of Aesop, and their wisdom has traveled from India across the entire world.",
        "for_readers": "These animal fables carry moral weight that is as relevant today as it was two millennia ago. Notice how each animal embodies a human failing or virtue. The talking tortoise who cannot keep silent, the ass who pretends to be a lion, the crane who tricks the fish — each is a mirror held up to human nature.",
        "member_ids": ["lion-and-crane", "the-lambikin", "cruel-crane-outwitted", "tiger-brahman-jackal", "talkative-tortoise", "gold-giving-serpent", "lesson-for-kings", "pride-before-fall", "ass-in-lions-skin", "pigeon-and-crow"],
        "keywords": ["animals", "jataka", "fable", "moral", "buddha"]
    },
    {
        "id": "theme-wisdom",
        "name": "Tales of Wisdom and Folly",
        "category": "themes",
        "about": "Indian fairy tales are saturated with practical wisdom. A pot of rice becomes a lesson in the danger of daydreams. A lac of rupees buys three pieces of life-saving advice. A demon cannot be defeated by violence but only by compassion. These tales teach through story what philosophy teaches through argument — and they do it with more humor and more heart.",
        "for_readers": "The wisdom in these tales is never abstract — it is always embodied in action and consequence. Pay attention to the moments when characters succeed or fail: the pattern reveals deep truths about patience, gratitude, humility, and the limits of cleverness.",
        "member_ids": ["the-broken-pot", "lac-of-rupees", "soothsayers-son", "harisarman", "demon-matted-hair", "sun-moon-wind-dinner", "wicked-sons-duped", "why-fish-laughed", "farmer-and-moneylender"],
        "keywords": ["wisdom", "folly", "advice", "moral", "lesson"]
    },
    {
        "id": "theme-quest-tales",
        "name": "Quest and Adventure Tales",
        "category": "themes",
        "about": "Princes win princesses through magical trials. Heroes journey to ivory cities and face terrible enchantments. The Son of Seven Queens must uncover his true identity. Raja Rasalu wanders the land facing challenges of wit and courage. These are the great adventure tales of India — sprawling, magical, and deeply satisfying in their resolution.",
        "for_readers": "These quest tales are some of the oldest adventure stories in the world. Many of their plot patterns — the hidden identity, the magical helper, the impossible task — have traveled from India to become the fairy tales of Europe. As you read, notice familiar patterns appearing in unfamiliar settings.",
        "member_ids": ["rajas-son-princess-labam", "punchkin", "the-charmed-ring", "son-of-seven-queens", "raja-rasalu", "boy-moon-forehead-star-chin", "prince-and-fakir", "ivory-city-fairy-princess"],
        "keywords": ["quest", "adventure", "prince", "princess", "magic", "hero"]
    },
    {
        "id": "theme-wit-tales",
        "name": "Tales of Wit and Cleverness",
        "category": "themes",
        "about": "Cleverness is the supreme virtue in many Indian tales. The jackal outsmarts the tiger. The lambikin tricks every predator on the road. Harisarman bluffs his way to fortune. The farmer defeats the money-lender through pure resourcefulness. These drolls — comic tales of wit — are India's great contribution to world folklore, and they are endlessly entertaining.",
        "for_readers": "These tales celebrate intelligence, quick thinking, and the ability to turn disadvantage into advantage. But they also sometimes show that cleverness has its limits — the lambikin's last trick fails, and even the cleverest trickster can be outtricked. What distinguishes wise cleverness from foolish cleverness?",
        "member_ids": ["the-lambikin", "tiger-brahman-jackal", "harisarman", "farmer-and-moneylender", "why-fish-laughed"],
        "keywords": ["wit", "cleverness", "trickster", "humor", "droll"]
    },
    {
        "id": "theme-love-tales",
        "name": "Tales of Love and Devotion",
        "category": "themes",
        "about": "From the legendary passion of Laili and Majnun to the prince's quest for Princess Labam and the fairy princess of the Ivory City, these tales explore love in all its forms — romantic obsession, patient devotion, and the love that survives death and separation. Indian love stories are rarely simple; they are tests of character as much as tests of feeling.",
        "for_readers": "Love in these tales is never easy — it requires quests, patience, sacrifice, and sometimes the acceptance of loss. These stories ask: what are you willing to endure for love? And is the love that demands everything worth the price?",
        "member_ids": ["rajas-son-princess-labam", "loving-laili", "ivory-city-fairy-princess"],
        "keywords": ["love", "devotion", "romance", "sacrifice", "passion"]
    },
    {
        "id": "theme-magic-tales",
        "name": "Tales of Magic and Enchantment",
        "category": "themes",
        "about": "Magic fiddles that sing the truth, charmed rings that grant wishes, evil magicians whose lives are hidden in parrots, boys born with moons on their foreheads — the magical world of Indian fairy tales is rich, vivid, and enchanting. These tales come from a tradition where magic is not fantasy but a dimension of reality that the wise can access and the foolish stumble into.",
        "for_readers": "The magic in these tales is not random — it follows rules. Wishes have consequences, enchantments can be broken, and every magical object has its own logic. Pay attention to the rules of magic in each story — they reveal deep truths about power, desire, and responsibility.",
        "member_ids": ["punchkin", "the-magic-fiddle", "the-charmed-ring", "boy-moon-forehead-star-chin", "prince-and-fakir"],
        "keywords": ["magic", "enchantment", "transformation", "wonder"]
    },
    {
        "id": "theme-family-tales",
        "name": "Family: Parents, Children, and Siblings",
        "category": "themes",
        "about": "The bonds of family — and the ruptures within it — drive many of these tales. Jealous sisters murder their sibling. Wicked sons mistreat their father. Seven queens are imprisoned. A mother-star blesses her generous child and curses her selfish ones. These stories explore the deepest of human relationships with unflinching honesty.",
        "for_readers": "Family in these tales is both the source of greatest love and greatest betrayal. These stories do not shy away from the darkness within families — but they also show that justice, love, and truth ultimately prevail. What do these tales teach about forgiveness, loyalty, and the obligations we owe to those closest to us?",
        "member_ids": ["the-magic-fiddle", "son-of-seven-queens", "sun-moon-wind-dinner", "wicked-sons-duped"],
        "keywords": ["family", "parents", "children", "siblings", "loyalty"]
    },
]

L3_DEFS = [
    {
        "id": "meta-themes",
        "name": "Themes and Traditions",
        "category": "meta",
        "about": "Indian fairy tales draw from the world's oldest story traditions — the Jatakas of Buddhist scripture, the great Sanskrit collections, and the living folk memory of the Indian subcontinent. Seven thematic streams — animal fables, wisdom tales, quests, wit, love, magic, and family — flow together to create a literary tradition of extraordinary richness. Joseph Jacobs called this collection 'a sort of Indian Grimm' — and he was right. These are the tales from which much of the world's fairy tale tradition ultimately springs.",
        "composite_of": [
            "theme-animal-fables",
            "theme-wisdom",
            "theme-quest-tales",
            "theme-wit-tales",
            "theme-love-tales",
            "theme-magic-tales",
            "theme-family-tales"
        ],
        "keywords": ["themes", "traditions", "indian", "folklore", "jataka"]
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
    idx = text.find("\nThe Lion and the Crane\n")
    if idx != -1:
        return text[idx + 1:].strip()
    return text


def strip_end_matter(text):
    """Remove Notes and References section."""
    idx = text.find("\nNotes and References\n")
    if idx != -1:
        return text[:idx].strip()
    # Try alternate form
    idx = text.find("\nNOTES AND REFERENCES\n")
    if idx != -1:
        return text[:idx].strip()
    return text


def clean_text(text):
    """Clean illustration markers, footnotes, excessive whitespace."""
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    text = re.sub(r'\[Footnote[^\]]*\]', '', text)
    # Remove carat superscripts notation
    text = re.sub(r'\^([a-z])', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove separator lines
    text = re.sub(r'\n\s*\*\s+\*\s+\*\s+\*\s+\*\s*\n', '\n\n', text)
    return text.strip()


def extract_stories(text):
    """Split text into individual stories."""
    stories = []
    positions = []

    for i, sdef in enumerate(STORY_DEFS):
        title = sdef["title"]
        pattern = "\n" + title + "\n"
        idx = text.find(pattern)

        if idx == -1:
            # Try at beginning of text
            if text.startswith(title + "\n"):
                idx = 0
            elif text.startswith(title + "\r"):
                idx = 0

        if idx == -1:
            # Try without trailing period
            title_nop = title.rstrip('.')
            pattern2 = "\n" + title_nop + "\n"
            idx = text.find(pattern2)

        if idx != -1:
            positions.append((idx, i))
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

        # Remove the title line(s)
        lines = story_text.split('\n')
        content_start = 0
        for j, line in enumerate(lines):
            stripped = line.strip()
            if stripped == '' or stripped == sdef["title"] or stripped == sdef["title"].rstrip('.'):
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
    items = []
    for sort_order, story in enumerate(stories):
        sdef = STORY_DEFS[story["def_idx"]]
        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "level": 1,
            "category": "fairy-tale",
            "sections": {
                "Story": story["text"],
                "Reflection": sdef["reflection"]
            },
            "keywords": sdef["keywords"],
            "metadata": {
                "source": "Indian Fairy Tales, selected and edited by Joseph Jacobs, illustrated by John D. Batten, London, David Nutt, 1892"
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
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Joseph Jacobs",
                    "date": "1892",
                    "note": "Selected and edited Indian Fairy Tales, David Nutt, London"
                },
                {
                    "name": "John D. Batten",
                    "date": "1892",
                    "note": "Illustrator of the original edition"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure, thematic groupings, and reflections"
                }
            ]
        },
        "name": "Indian Fairy Tales",
        "description": "Twenty-nine fairy tales from the Indian subcontinent, selected and edited by Joseph Jacobs (1892) with illustrations by John D. Batten. Drawing from the ancient Jatakas (Buddhist birth stories), Sanskrit collections, and modern Indian folk-tale collectors, this landmark anthology gathers animal fables, quest tales, stories of wit and magic, and legends of love and wisdom from one of the richest storytelling traditions on Earth. Jacobs called it 'a sort of Indian Grimm' — these are the tales from which much of the world's fairy tale heritage ultimately springs. Source: Project Gutenberg eBook #7128 (https://www.gutenberg.org/ebooks/7128).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: John D. Batten's original illustrations for the 1892 David Nutt edition — beautiful line drawings and color plates in Arts and Crafts style depicting scenes from each tale. Warwick Goble's illustrations for 'Indian Myth and Legend' by Donald A. Mackenzie (1913, Gresham Publishing) — watercolor plates of Indian scenes. W. Heath Robinson's illustrations for 'A Song of the English' and Indian subjects (early 1900s).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "fairy-tales",
            "indian",
            "folklore",
            "jataka",
            "buddhist",
            "animals",
            "wisdom",
            "magic",
            "oracle"
        ],
        "roots": ["eastern-wisdom", "indigenous-mythology"],
        "shelves": ["wonder", "wisdom"],
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
