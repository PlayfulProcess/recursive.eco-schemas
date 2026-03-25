#!/usr/bin/env python3
"""
Build grammar.json for The Adventures of Pinocchio by Carlo Collodi.

Source: Project Gutenberg eBook #500, translated by Carol Della Chiesa.
Structure: 36 chapters
Levels:
  L1: Individual chapters
  L2: Story arcs + thematic groups (with composite_of referencing L1)
  L3: Meta-categories
"""

import json
import re
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "seeds" / "adventures-of-pinocchio.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "adventures-of-pinocchio"
OUTPUT_FILE = OUTPUT_DIR / "grammar.json"

CHAPTER_TITLES = {
    1: "Mastro Cherry and the Talking Wood",
    2: "Geppetto Gets the Wood",
    3: "Pinocchio Is Born",
    4: "The Talking Cricket's Warning",
    5: "The Egg and the Chick",
    6: "Pinocchio Falls Asleep by the Fire",
    7: "Geppetto Makes New Feet",
    8: "The ABC Book",
    9: "The Puppet Theater",
    10: "Fire Eater the Puppet Master",
    11: "Fire Eater Sneezes",
    12: "The Fox and the Cat",
    13: "The Inn of the Red Lobster",
    14: "The Assassins in the Dark",
    15: "Pinocchio Is Hanged",
    16: "The Beautiful Blue-Haired Fairy",
    17: "Pinocchio's Nose Grows",
    18: "The Fox and the Cat Again",
    19: "The Field of Wonders",
    20: "Pinocchio Is Robbed",
    21: "The Guard Dog Melampo",
    22: "Pinocchio Catches the Thieves",
    23: "The Death of the Fairy",
    24: "The Island of the Busy Bees",
    25: "Pinocchio Promises the Fairy",
    26: "The Land of Boobies",
    27: "The Fight with the Schoolboys",
    28: "The Terrible Dogfish",
    29: "Pinocchio Returns to the Fairy",
    30: "The Land of Toys",
    31: "Five Months of Play",
    32: "Pinocchio Becomes a Donkey",
    33: "The Donkey in the Sea",
    34: "Inside the Dogfish",
    35: "Pinocchio Finds Geppetto",
    36: "Pinocchio Becomes a Real Boy",
}

CHAPTER_SUMMARIES = {
    1: "A piece of wood in Mastro Cherry's shop weeps and laughs like a child. The carpenter is terrified and gives it away to his neighbor Geppetto, who wants to make a marionette.",
    2: "Geppetto and Mastro Cherry quarrel and fight over the wood. Geppetto takes it home, planning to make a puppet that can dance and turn somersaults.",
    3: "Geppetto carves Pinocchio, who immediately begins to misbehave -- his eyes move, his nose grows as it's carved, his mouth laughs, his hands snatch Geppetto's wig. The moment his legs are finished, Pinocchio runs away into the street.",
    4: "Pinocchio meets the Talking Cricket, who warns him that boys who disobey their parents come to grief. Pinocchio, furious at the lecture, throws a hammer and kills the Cricket. This is the first of Pinocchio's many acts of impulsive cruelty.",
    5: "Alone and hungry, Pinocchio searches for food. He finds an egg but when he cracks it, a chick flies out. Cold and miserable, he falls asleep with his feet on the brazier.",
    6: "Pinocchio wakes to find his feet have burned off. Geppetto returns from prison and feeds him pears. Pinocchio promises to go to school, and Geppetto makes him new feet.",
    7: "Geppetto makes new feet for Pinocchio and sells his own coat to buy an ABC book. Pinocchio is deeply moved and promises to learn to read and become a good boy.",
    8: "On the way to school, Pinocchio hears music from a puppet theater and sells his ABC book for admission. The book Geppetto bought by selling his only coat -- traded for a moment of entertainment.",
    9: "At the puppet theater, the marionettes recognize Pinocchio as one of their own and welcome him onto the stage, disrupting the show. The puppet master, Fire Eater, is furious.",
    10: "The terrifying Fire Eater plans to burn Pinocchio for firewood. Pinocchio begs for mercy and tells about poor Geppetto who gave up his coat.",
    11: "Fire Eater, moved by Pinocchio's story, sneezes instead of punishing him (sneezing is how he shows compassion). He gives Pinocchio five gold pieces to take to Geppetto.",
    12: "On the road home, Pinocchio meets the Fox and the Cat, who pretend to be lame and blind. They tell him about the Field of Wonders, where gold pieces multiply overnight.",
    13: "The three stop at the Inn of the Red Lobster. The Fox and Cat feast and charge it to Pinocchio. They leave at midnight, planning to meet at the Field of Wonders.",
    14: "Alone on a dark road, Pinocchio is attacked by two Assassins (the Fox and Cat in disguise). He fights and runs, and the ghost of the Talking Cricket warns him.",
    15: "The Assassins catch Pinocchio and hang him from a tree. Left for dead, he swings in the wind. This is the original serial ending -- Collodi initially killed Pinocchio here.",
    16: "A Beautiful Fairy with blue hair sends her falcon to rescue Pinocchio. She calls doctors to examine him. Pinocchio refuses his medicine until undertakers arrive for his coffin.",
    17: "The Fairy questions Pinocchio, who lies about the gold pieces. With each lie, his nose grows longer and longer until he cannot turn around in the room. The Fairy laughs and calls woodpeckers to peck it back to size.",
    18: "Leaving the Fairy's house, Pinocchio meets the Fox and the Cat again on the road. Despite everything, he falls for their scheme once more and follows them to the Field of Wonders.",
    19: "At the Field of Wonders, Pinocchio buries his gold pieces and waters them, expecting a money tree to grow. When he returns, the gold is gone -- stolen by the Fox and the Cat.",
    20: "Pinocchio goes to court, but the judge (an ape) sentences him to prison for being foolish enough to be robbed. After four months, he is freed in a general amnesty.",
    21: "Pinocchio is caught in a trap by a farmer who chains him up as a guard dog, replacing the dead dog Melampo.",
    22: "Pinocchio catches chicken thieves (weasels) and is freed by the grateful farmer. He learns that honesty has its rewards.",
    23: "Pinocchio returns to the Fairy's house but finds a gravestone saying she died of grief because a certain puppet abandoned her. Pinocchio weeps with remorse.",
    24: "A pigeon carries Pinocchio to the seashore where he sees Geppetto sailing out in a tiny boat, searching for him. A wave capsizes the boat. Pinocchio swims to the Island of the Busy Bees.",
    25: "On the island, Pinocchio finds the Fairy alive again, now grown into a woman. She promises to make him a real boy if he is good and studies hard. Pinocchio agrees.",
    26: "Pinocchio tries to be good at school but is led astray by his classmate Lampwick, who tells him about the Land of Boobies where there is no school.",
    27: "Pinocchio gets in a fight with schoolboys at the beach. A boy is hurt, and Pinocchio is arrested. He escapes but is caught by a terrible dog and nearly drowns.",
    28: "Pinocchio is caught by a fisherman who mistakes him for a rare fish and tries to fry him. The Dogfish's shadow appears. The brave dog Alidoro saves Pinocchio.",
    29: "Pinocchio returns to the Fairy and promises once again to be good. He studies hard and is told he will become a real boy tomorrow.",
    30: "On the eve of becoming a real boy, Lampwick convinces Pinocchio to come to the Land of Toys instead -- a place of perpetual play with no school, no work, and no books.",
    31: "Five months of play in the Land of Toys. Pinocchio and Lampwick play from dawn to dusk with thousands of other boys. Then one morning, Pinocchio wakes with donkey ears.",
    32: "Pinocchio transforms fully into a donkey. A farmer buys him and works him until he goes lame, then sells him to a man who wants to make a drumhead from his skin. Thrown into the sea to drown, the fish eat the donkey skin and Pinocchio emerges as a puppet again.",
    33: "Pinocchio swims free but is swallowed by the terrible Dogfish (the same one that swallowed Geppetto). In the darkness of the Dogfish's belly, he sees a faint light.",
    34: "Inside the Dogfish, Pinocchio follows the light and discovers a table set with food, a candle, and old Geppetto, who has been living inside the Dogfish for two years.",
    35: "Pinocchio and Geppetto escape from the sleeping Dogfish's mouth. Pinocchio carries the weak old man on his back, swimming through the night sea. A tuna fish helps them reach shore.",
    36: "Pinocchio works tirelessly to support the sick Geppetto, drawing water, weaving baskets, and building a cart to wheel him around. One night, in a dream, the Fairy appears and praises him. Pinocchio wakes to find himself transformed into a real boy, with real money in his pocket and Geppetto healthy and strong.",
}

CHAPTER_KEYWORDS = {
    1: ["wood", "magic", "mastro-cherry", "carpenter", "mystery"],
    2: ["geppetto", "quarrel", "puppet", "creation", "wood"],
    3: ["pinocchio", "birth", "mischief", "geppetto", "running-away"],
    4: ["talking-cricket", "warning", "disobedience", "conscience", "cruelty"],
    5: ["hunger", "egg", "consequences", "loneliness", "cold"],
    6: ["fire", "burned-feet", "geppetto", "love", "pears"],
    7: ["new-feet", "abc-book", "sacrifice", "coat", "school"],
    8: ["puppet-theater", "temptation", "abc-book", "impulsiveness"],
    9: ["marionettes", "theater", "fire-eater", "recognition"],
    10: ["fire-eater", "danger", "mercy", "geppetto", "story"],
    11: ["compassion", "gold-pieces", "sneezing", "generosity"],
    12: ["fox", "cat", "tricksters", "field-of-wonders", "greed"],
    13: ["inn", "fox", "cat", "deception", "feast"],
    14: ["assassins", "night", "danger", "darkness", "cricket-ghost"],
    15: ["hanging", "death", "punishment", "tree", "darkness"],
    16: ["blue-fairy", "rescue", "medicine", "coffin", "fear"],
    17: ["lying", "nose-grows", "fairy", "woodpeckers", "truth"],
    18: ["fox", "cat", "gullibility", "temptation", "repetition"],
    19: ["field-of-wonders", "gold-pieces", "theft", "foolishness"],
    20: ["prison", "justice", "absurdity", "court", "freedom"],
    21: ["guard-dog", "farmer", "trap", "melampo", "captivity"],
    22: ["thieves", "honesty", "reward", "weasels", "freedom"],
    23: ["fairy", "death", "grief", "remorse", "abandonment"],
    24: ["pigeon", "sea", "geppetto", "search", "swimming", "island"],
    25: ["fairy", "promise", "island", "real-boy", "goodness"],
    26: ["lampwick", "temptation", "school", "land-of-boobies"],
    27: ["fight", "schoolboys", "beach", "arrest", "dog"],
    28: ["fisherman", "frying", "dogfish", "alidoro", "rescue"],
    29: ["fairy", "promise", "study", "real-boy", "transformation"],
    30: ["land-of-toys", "lampwick", "temptation", "play", "no-school"],
    31: ["play", "donkey-ears", "transformation", "consequences"],
    32: ["donkey", "slavery", "work", "sea", "puppet-again"],
    33: ["dogfish", "swallowed", "darkness", "light", "belly"],
    34: ["geppetto", "inside-dogfish", "reunion", "candle", "survival"],
    35: ["escape", "swimming", "carrying", "tuna", "shore", "devotion"],
    36: ["real-boy", "transformation", "work", "fairy", "love", "redemption"],
}

CHAPTER_REFLECTIONS = {
    1: "A piece of ordinary wood turns out to be alive. What ordinary things in your world might have hidden life in them?",
    2: "Geppetto wants to make a puppet that will earn him a living. Parents have dreams for their children too. What dreams do the adults in your life have for you?",
    3: "Pinocchio is mischievous from the very first moment. Is being naughty part of being alive? Can you be good without ever being bad?",
    4: "The Cricket tries to give good advice and Pinocchio destroys him. Have you ever pushed away someone who was trying to help?",
    5: "Pinocchio is hungry and cold because of his own choices. When have your own choices led to difficult consequences?",
    6: "Geppetto comes home from prison and the first thing he does is feed Pinocchio. What does that tell us about love?",
    7: "Geppetto sells his only coat so Pinocchio can have a schoolbook. What is the biggest sacrifice someone has made for you?",
    8: "Pinocchio sells the ABC book for a ticket to a puppet show. What important things have you given up for something fun?",
    9: "The puppet marionettes recognize Pinocchio as one of their own. What does it feel like to find people who are like you?",
    10: "Fire Eater is terrifying but turns out to have a good heart. Have you ever been scared of someone who turned out to be kind?",
    11: "Fire Eater shows kindness through sneezing. Everyone shows feelings differently. How do the people you love show they care?",
    12: "The Fox and Cat tell Pinocchio exactly what he wants to hear. How can you tell the difference between good advice and flattery?",
    13: "Pinocchio is warned again and again but keeps making the same mistake. Why is it so hard to learn from warnings?",
    14: "Alone in the dark, Pinocchio faces real danger. When have you felt alone and scared? What helped you get through it?",
    15: "Collodi originally ended the story here, with Pinocchio dead. Why do you think he decided to continue? Does a character deserve a second chance?",
    16: "The Blue Fairy rescues Pinocchio and cares for him like a mother. Who in your life has taken care of you when you were in trouble?",
    17: "Pinocchio's nose grows when he lies. If everyone's lies were visible, how would the world be different?",
    18: "Pinocchio falls for the same trick twice. Why do we sometimes make the same mistake even when we know better?",
    19: "Pinocchio believes money can grow on trees. What 'too good to be true' stories have you encountered?",
    20: "The judge punishes Pinocchio for being the victim. Have you ever been blamed for something that wasn't your fault?",
    21: "Pinocchio is chained up like a dog. What does it feel like to lose your freedom?",
    22: "Pinocchio does the right thing and is rewarded. Does being honest always lead to good results? Should you be honest anyway?",
    23: "The gravestone says the Fairy died of grief because Pinocchio abandoned her. How do our actions affect the people who love us?",
    24: "Geppetto sailed into the ocean looking for Pinocchio. What does it mean to search for someone you love, no matter what?",
    25: "Pinocchio promises to be good -- again. How many chances should someone get? When does patience run out?",
    26: "Lampwick is the 'cool kid' who leads others astray. Who in your life pushes you toward good choices? Who pushes you toward bad ones?",
    27: "A fight at the beach leads to serious consequences. How do small conflicts escalate into big problems?",
    28: "Pinocchio is almost fried like a fish. Sometimes life puts us in absurd, terrifying situations. What got you through your scariest moment?",
    29: "Pinocchio is so close to becoming a real boy. Have you ever been very close to achieving a goal? What did that feel like?",
    30: "The Land of Toys promises fun forever with no consequences. Does that sound like paradise or a trap? Why?",
    31: "Five months of pure play leads to becoming a donkey. What happens when we only seek pleasure and never work or learn?",
    32: "Pinocchio suffers terribly as a donkey. Is suffering sometimes necessary for growth? Can you grow without it?",
    33: "Pinocchio is swallowed by the Dogfish. In the belly of the beast, he finds a tiny light. When things are darkest, what lights do you look for?",
    34: "Pinocchio finds Geppetto alive inside the Dogfish. Reunions after long separations are powerful. What reunion have you wished for most?",
    35: "Pinocchio carries Geppetto on his back through the sea. The child saves the parent. When have you taken care of someone who usually takes care of you?",
    36: "Pinocchio becomes real not through magic but through love and hard work. What does it mean to become 'real'?",
}

STORY_ARCS = {
    "arc-birth-and-first-lessons": {
        "name": "Birth and First Lessons",
        "chapters": [1, 2, 3, 4, 5, 6, 7],
        "about": "Pinocchio comes into being: a magical piece of wood, a lonely old man's dream, and a puppet who runs away the moment he can walk. The early chapters establish the pattern that will repeat throughout the story -- Pinocchio misbehaves, suffers consequences, repents, and promises to change. Geppetto's sacrifice of his only coat to buy the ABC book is the story's first great act of love.",
        "for_parents": "These opening chapters set up the fundamental dynamic between Pinocchio and Geppetto: unconditional parental love meeting childish selfishness. The Talking Cricket (Jiminy Cricket in the Disney version) appears here and is immediately killed -- a much darker start than most children expect. Collodi was writing a cautionary tale, and it shows. Great for talking about consequences and the difference between knowing the right thing and doing it.",
        "keywords": ["creation", "geppetto", "disobedience", "consequences", "love"],
    },
    "arc-theater-and-tricksters": {
        "name": "The Theater and the Tricksters",
        "chapters": [8, 9, 10, 11, 12, 13, 14, 15],
        "about": "Pinocchio's first venture into the world: he sells his schoolbook for a puppet show, meets the fearsome but kind Fire Eater, receives gold pieces, and immediately falls prey to the Fox and the Cat -- the story's great con artists. This arc ends with Pinocchio hanged from a tree, the original ending of the serialized story before readers demanded Collodi continue.",
        "for_parents": "The Fox and Cat are among literature's great swindlers, ancestors of every con artist in every children's story since. They exploit Pinocchio's greed and naivety with the Field of Wonders scheme. The hanging at the end of Chapter 15 is genuinely disturbing -- Collodi intended it as a final moral lesson. That readers rebelled and demanded Pinocchio's survival tells us something about how stories work: we need the possibility of redemption.",
        "keywords": ["theater", "tricksters", "fox", "cat", "gold", "hanging", "danger"],
    },
    "arc-the-fairy-and-new-chances": {
        "name": "The Fairy and New Chances",
        "chapters": [16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
        "about": "The Blue-Haired Fairy enters the story as a mother figure who rescues, teaches, and tests Pinocchio. His nose grows when he lies. He falls for the Fox and Cat's trick a second time and goes to prison. He serves as a guard dog, catches thieves, and is freed. The Fairy appears to die of grief at his behavior, then reappears on the Island of the Busy Bees. She promises to make him a real boy if he is good.",
        "for_parents": "The Fairy is both mother figure and moral compass. Her 'death' from grief when Pinocchio abandons her is a powerful lesson about how our actions affect those who love us. The growing nose scene is the most famous in the book and a perfect conversation starter about lying. Note how Pinocchio keeps getting second (and third, and fourth) chances -- Collodi believes in redemption but makes the road long.",
        "keywords": ["fairy", "lying", "nose", "redemption", "prison", "promise", "mother"],
    },
    "arc-temptation-and-transformation": {
        "name": "Temptation and Transformation",
        "chapters": [26, 27, 28, 29, 30, 31, 32, 33],
        "about": "The final great temptation: the Land of Toys, where boys play all day without school or work. Lampwick leads Pinocchio astray on the very eve of becoming a real boy. Five months of play transform both boys into donkeys. Pinocchio is enslaved, worked nearly to death, thrown into the sea, and swallowed by the terrible Dogfish -- the same creature that swallowed Geppetto.",
        "for_parents": "The Land of Toys sequence is Collodi's most powerful moral parable. The transformation into donkeys is terrifying -- Collodi doesn't soften it. Lampwick's weeping as donkey ears sprout from his head is genuinely heartbreaking. This is the story at its darkest, and it's essential: Pinocchio must lose everything before he can become real. For children, this arc raises profound questions about pleasure versus purpose, freedom versus responsibility.",
        "keywords": ["land-of-toys", "donkey", "transformation", "slavery", "dogfish", "darkness"],
    },
    "arc-redemption": {
        "name": "Redemption",
        "chapters": [34, 35, 36],
        "about": "Inside the Dogfish, Pinocchio finds Geppetto -- alive but weakened, sustained by a candle and a few provisions. Together they escape through the sleeping Dogfish's mouth. Pinocchio carries the old man through the sea, works tirelessly to support him, and finally -- through labor, love, and selflessness -- earns his transformation into a real boy.",
        "for_parents": "The ending of Pinocchio is often misremembered because of the Disney film. In Collodi's original, there is no fairy godmother moment -- Pinocchio earns his humanity through months of backbreaking work to support his sick father. He draws water, weaves baskets, builds a cart. The transformation comes as a quiet miracle during sleep, not a spectacle. This is Collodi's deepest message: you become real not through magic but through love expressed as action.",
        "keywords": ["reunion", "escape", "work", "love", "real-boy", "redemption"],
    },
}

THEMATIC_GROUPS = {
    "theme-conscience-and-temptation": {
        "name": "Conscience and Temptation",
        "chapters": [4, 8, 12, 13, 18, 19, 26, 30, 31],
        "about": "From the Talking Cricket's first warning to the Land of Toys, Pinocchio is torn between what he knows is right and what he wants to do. The Cricket speaks for conscience; the Fox, the Cat, and Lampwick speak for temptation. Pinocchio hears both and nearly always chooses wrong -- until suffering teaches him what words could not.",
        "for_parents": "Every child knows the experience of choosing fun over duty, impulse over wisdom. Pinocchio's story validates this struggle without excusing it. Collodi shows that knowing right from wrong (which Pinocchio always does) is not the same as choosing right over wrong. The repetition is deliberate -- Pinocchio falls for the same tricks again and again, because that's how human beings actually learn: slowly, painfully, through repetition.",
        "keywords": ["conscience", "temptation", "cricket", "fox", "cat", "lampwick", "choices"],
    },
    "theme-love-and-sacrifice": {
        "name": "Love and Sacrifice",
        "chapters": [6, 7, 11, 16, 23, 24, 25, 34, 35, 36],
        "about": "Geppetto sells his coat for a schoolbook. Fire Eater spares Pinocchio out of compassion. The Fairy rescues, heals, and guides Pinocchio like a mother. Geppetto sails the ocean searching for his puppet son. Pinocchio carries Geppetto through the sea and works to support him. Love in Pinocchio is not sentimental -- it is expressed through sacrifice and action.",
        "for_parents": "Collodi's vision of love is demanding and practical. Geppetto doesn't just say he loves Pinocchio -- he sells his coat, goes to prison, and sails into the ocean for him. The Fairy doesn't just forgive -- she sets conditions and tests. And Pinocchio's final transformation comes not from saying 'I'll be good' but from months of labor. This is a powerful counter-narrative to stories where love is easy and magic fixes everything.",
        "keywords": ["love", "sacrifice", "geppetto", "fairy", "devotion", "work"],
    },
    "theme-becoming-real": {
        "name": "Becoming Real",
        "chapters": [3, 17, 25, 29, 30, 31, 32, 36],
        "about": "What does it mean to be 'real'? Pinocchio begins as a piece of wood, becomes a puppet that runs and talks, and spends the whole story trying to become a flesh-and-blood boy. But becoming real is not a physical transformation -- it's a moral one. Each step toward selflessness is a step toward humanity. Each act of selfish impulse pulls him back toward wood.",
        "for_parents": "This theme connects directly to every child's experience of growing up. Being 'real' in Collodi's sense means being accountable, empathetic, and willing to work for others. The Velveteen Rabbit would later explore this theme differently, but Collodi's version is harder: you become real not by being loved but by learning to love. A profound theme for conversations about maturity, responsibility, and what it really means to grow up.",
        "keywords": ["real-boy", "transformation", "humanity", "maturity", "growth"],
    },
    "theme-tricksters-and-justice": {
        "name": "Tricksters and Justice",
        "chapters": [12, 13, 14, 18, 19, 20, 21, 22],
        "about": "The Fox and the Cat are the story's recurring villains -- con artists who exploit Pinocchio's greed and gullibility. But the justice system is no better: the judge punishes Pinocchio for being robbed. The farmer chains him up for trespassing. In Collodi's world, the law serves the powerful, and the naive must learn to protect themselves.",
        "for_parents": "Collodi wrote in post-unification Italy, a time of great social upheaval and corruption. His satire of the justice system (the ape judge who imprisons victims) reflects real cynicism about institutions. For children, these chapters raise important questions about fairness: Is it Pinocchio's fault he was tricked? Should victims be punished? What do we do when the system isn't fair?",
        "keywords": ["fox", "cat", "tricksters", "justice", "prison", "fairness", "satire"],
    },
}


def read_and_strip_gutenberg(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE ADVENTURES OF PINOCCHIO ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE ADVENTURES OF PINOCCHIO ***"
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    # Strip producer notes and title block
    ch1_match = re.search(r'\nCHAPTER 1\n', text)
    if ch1_match:
        text = text[ch1_match.start():]

    return text.strip()


def split_into_chapters(text):
    """Split text into chapters. Each chapter starts with 'CHAPTER N' followed by a description."""
    chapter_pattern = re.compile(r'^CHAPTER\s+(\d+)\s*$', re.MULTILINE)
    matches = list(chapter_pattern.finditer(text))
    chapters = {}

    for i, match in enumerate(matches):
        chapter_num = int(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        # The first paragraph is the chapter description/subtitle
        # Split it off and include it
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        chapters[chapter_num] = content

    return chapters


def build_grammar():
    text = read_and_strip_gutenberg(SEED_FILE)
    chapters = split_into_chapters(text)

    items = []
    sort_order = 0
    chapter_id_map = {}

    # === L1: Chapters ===
    for chapter_num in sorted(chapters.keys()):
        sort_order += 1
        item_id = f"chapter-{chapter_num:02d}"
        chapter_id_map[chapter_num] = item_id

        items.append({
            "id": item_id,
            "name": f"Chapter {chapter_num} — {CHAPTER_TITLES.get(chapter_num, '')}",
            "sort_order": sort_order,
            "category": f"chapter-{chapter_num:02d}",
            "level": 1,
            "sections": {
                "Story": chapters[chapter_num],
                "About": CHAPTER_SUMMARIES.get(chapter_num, ""),
                "Reflection": CHAPTER_REFLECTIONS.get(chapter_num, "What does this chapter make you think about?"),
            },
            "keywords": CHAPTER_KEYWORDS.get(chapter_num, []),
            "metadata": {
                "chapter_number": chapter_num,
                "chapter_name": CHAPTER_TITLES.get(chapter_num, ""),
            },
        })

    # === L2: Story Arcs ===
    for arc_id, arc_data in STORY_ARCS.items():
        sort_order += 1
        composite = [chapter_id_map[ch] for ch in arc_data["chapters"] if ch in chapter_id_map]
        items.append({
            "id": arc_id,
            "name": arc_data["name"],
            "sort_order": sort_order,
            "category": "story-arc",
            "level": 2,
            "relationship_type": "emergence",
            "composite_of": composite,
            "sections": {
                "About": arc_data["about"],
                "For Parents": arc_data["for_parents"],
            },
            "keywords": arc_data["keywords"],
            "metadata": {},
        })

    # === L2: Thematic Groups ===
    for theme_id, theme_data in THEMATIC_GROUPS.items():
        sort_order += 1
        composite = [chapter_id_map[ch] for ch in theme_data["chapters"] if ch in chapter_id_map]
        items.append({
            "id": theme_id,
            "name": theme_data["name"],
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "relationship_type": "emergence",
            "composite_of": composite,
            "sections": {
                "About": theme_data["about"],
                "For Parents": theme_data["for_parents"],
            },
            "keywords": theme_data["keywords"],
            "metadata": {},
        })

    # === L3: Meta-categories ===
    all_arc_ids = list(STORY_ARCS.keys())
    all_theme_ids = list(THEMATIC_GROUPS.keys())

    sort_order += 1
    items.append({
        "id": "meta-the-story",
        "name": "The Story",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "relationship_type": "emergence",
        "composite_of": all_arc_ids,
        "sections": {
            "About": "The complete adventure of Pinocchio in five movements: birth and first lessons, the theater and the tricksters, the Fairy and new chances, temptation and transformation, and redemption. Thirty-six chapters tracing a puppet's long, painful, often hilarious journey from wood to flesh, from selfishness to love.",
            "For Parents": "The Adventures of Pinocchio (1883) is far darker and funnier than the Disney adaptation suggests. Collodi wrote it as a serial cautionary tale -- he originally killed Pinocchio in Chapter 15. Readers demanded his resurrection, and the story grew into something much richer: a picaresque epic about becoming fully human. It is the Italian Pilgrim's Progress, an odyssey of moral growth through suffering. Read it with your children and let them discover that the original Pinocchio is wilder, scarier, and more moving than they expect.",
        },
        "keywords": ["complete-story", "narrative", "chapters", "pinocchio"],
        "metadata": {},
    })

    sort_order += 1
    items.append({
        "id": "meta-themes",
        "name": "Themes",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "The great themes of Pinocchio: conscience versus temptation, love expressed through sacrifice, the long road to becoming real, and the corrupt world of tricksters and unjust laws. These themes weave through all thirty-six chapters, connecting scenes from different parts of the story.",
            "For Parents": "These thematic groupings let you explore Pinocchio from different angles. If your child is fascinated by the growing nose, follow the Conscience thread. If they ask why Geppetto sells his coat, explore Love and Sacrifice. If the Land of Toys captivates them, discuss what 'becoming real' truly means.",
        },
        "keywords": ["themes", "analysis", "groupings", "perspectives"],
        "metadata": {},
    })

    # === Build Grammar ===
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Carlo Collodi",
                    "date": "1883",
                    "note": "Author of Le Avventure di Pinocchio",
                },
                {
                    "name": "Carol Della Chiesa",
                    "date": "1925",
                    "note": "English translator",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2006",
                    "note": "eBook #500 — digitized text",
                },
                {
                    "name": "PlayfulProcess",
                    "date": "2026-03-04",
                    "note": "Grammar construction and thematic groupings",
                },
            ],
        },
        "name": "The Adventures of Pinocchio",
        "description": (
            "Carlo Collodi's The Adventures of Pinocchio (Le Avventure di Pinocchio, 1883) -- "
            "the original Italian tale of a wooden puppet's long, painful, hilarious journey to become a real boy. "
            "Far darker and richer than the Disney adaptation, Collodi's Pinocchio is a picaresque epic: "
            "the puppet is hanged, enslaved, turned into a donkey, swallowed by a dogfish, and finally redeemed "
            "through labor and love. Thirty-six chapters in the Carol Della Chiesa translation, structured as "
            "story arcs and thematic groupings.\n\n"
            "Source: Project Gutenberg eBook #500 (https://www.gutenberg.org/ebooks/500). "
            "English translation by Carol Della Chiesa.\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES:\n"
            "- Enrico Mazzanti (1883, Felice Paggi) -- original illustrator, "
            "bold pen-and-ink drawings capturing the story's blend of comedy and menace\n"
            "- Attilio Mussino (1911, Bemporad) -- definitive color illustrations, "
            "vivid watercolors that set the visual standard for Pinocchio worldwide\n"
            "- Carlo Chiostri (1901, Bemporad) -- elegant, detailed ink illustrations\n"
            "- Alice Carsey (1904, Ginn and Company) -- early American edition illustrations"
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "children",
            "classic",
            "adventure",
            "fantasy",
            "public-domain",
            "carlo-collodi",
            "pinocchio",
            "full-text",
            "chapters",
            "multi-level",
            "italian",
            "translation",
        ],
        "roots": ["wonder-imagination"],
        "shelves": ["children", "wonder"],
        "lineages": ["universal"],
        "worldview": "imaginative",
        "items": items,
    }

    return grammar


def main():
    print(f"Reading seed text from {SEED_FILE}...")
    grammar = build_grammar()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    items = grammar["items"]
    l1 = [i for i in items if i["level"] == 1]
    l2 = [i for i in items if i["level"] == 2]
    l3 = [i for i in items if i["level"] == 3]

    print(f"Grammar written to {OUTPUT_FILE}")
    print(f"  L1 chapters: {len(l1)}")
    print(f"  L2 arcs + themes: {len(l2)}")
    print(f"  L3 meta-categories: {len(l3)}")
    print(f"  Total items: {len(items)}")

    ids = [i["id"] for i in items]
    id_set = set(ids)
    dupes = len(ids) - len(id_set)
    if dupes:
        print(f"  WARNING: {dupes} duplicate IDs found!")

    broken = []
    for item in items:
        for ref in item.get("composite_of", []):
            if ref not in id_set:
                broken.append((item["id"], ref))
    if broken:
        print(f"  WARNING: {len(broken)} broken references:")
        for item_id, ref in broken:
            print(f"    {item_id} -> {ref}")
    else:
        print("  All references valid.")


if __name__ == "__main__":
    main()
