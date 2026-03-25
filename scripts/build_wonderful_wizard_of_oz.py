#!/usr/bin/env python3
"""
Build grammar.json for The Wonderful Wizard of Oz by L. Frank Baum.

Source: Project Gutenberg eBook #55
Structure: 24 chapters + Introduction
Levels:
  L1: Individual chapters
  L2: Story arcs + thematic groups (with composite_of referencing L1 chapters)
  L3: Meta-categories
"""

import json
import re
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "seeds" / "wonderful-wizard-of-oz.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "wonderful-wizard-of-oz"
OUTPUT_FILE = OUTPUT_DIR / "grammar.json"

CHAPTER_TITLES = {
    0: "Introduction",
    1: "The Cyclone",
    2: "The Council with the Munchkins",
    3: "How Dorothy Saved the Scarecrow",
    4: "The Road Through the Forest",
    5: "The Rescue of the Tin Woodman",
    6: "The Cowardly Lion",
    7: "The Journey to the Great Oz",
    8: "The Deadly Poppy Field",
    9: "The Queen of the Field Mice",
    10: "The Guardian of the Gates",
    11: "The Emerald City of Oz",
    12: "The Search for the Wicked Witch",
    13: "The Rescue",
    14: "The Winged Monkeys",
    15: "The Discovery of Oz, the Terrible",
    16: "The Magic Art of the Great Humbug",
    17: "How the Balloon Was Launched",
    18: "Away to the South",
    19: "Attacked by the Fighting Trees",
    20: "The Dainty China Country",
    21: "The Lion Becomes the King of Beasts",
    22: "The Country of the Quadlings",
    23: "Glinda The Good Witch Grants Dorothy's Wish",
    24: "Home Again",
}


def roman_to_int(s):
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and values.get(c, 0) < values.get(s[i + 1], 0):
            result -= values[c]
        else:
            result += values[c]
    return result


def read_and_strip_gutenberg(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE WONDERFUL WIZARD OF OZ ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE WONDERFUL WIZARD OF OZ ***"
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    # Remove illustration tags
    text = re.sub(r'\[Illustration[^\]]*\]', '', text, flags=re.DOTALL)

    return text.strip()


def extract_introduction(text):
    """Extract Baum's introduction."""
    match = re.search(r'\nIntroduction\n', text)
    if not match:
        return ""
    start = match.end()
    # Introduction ends at "Chapter I"
    ch1_match = re.search(r'\nChapter I\n', text[start:])
    if ch1_match:
        intro = text[start:start + ch1_match.start()]
    else:
        intro = text[start:start + 2000]

    # Also strip title page before Introduction
    intro = intro.strip()
    # Remove trailing title repetition if present
    intro = re.sub(r'\n\s*The Wonderful Wizard of Oz\s*$', '', intro, flags=re.MULTILINE)
    return intro.strip()


def split_into_chapters(text):
    """Split text into chapters."""
    chapter_pattern = re.compile(
        r'^Chapter\s+([IVXLC]+)\n(.+?)\n',
        re.MULTILINE
    )

    matches = list(chapter_pattern.finditer(text))
    chapters = {}

    for i, match in enumerate(matches):
        roman = match.group(1)
        chapter_num = roman_to_int(roman)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        chapters[chapter_num] = content

    return chapters


CHAPTER_SUMMARIES = {
    0: "Baum's manifesto for a new kind of fairy tale -- one that keeps the wonderment and joy but leaves out the heartaches and nightmares. Written in Chicago in 1900, it declared that modern children seek only entertainment and gladly dispense with disagreeable incidents.",
    1: "Dorothy lives on the gray Kansas prairie with Uncle Henry, Aunt Em, and her little dog Toto. A cyclone lifts the house into the air and carries it far away, setting it down in the Land of the Munchkins, where it crushes the Wicked Witch of the East.",
    2: "Dorothy meets the Good Witch of the North and the Munchkins. She learns about the four witches and the great Wizard of Oz. The Good Witch kisses her forehead for protection and tells her to follow the yellow brick road to the Emerald City.",
    3: "Dorothy discovers a Scarecrow on a pole and helps him down. He tells her he wants a brain more than anything in the world. They agree to travel together to ask the great Oz for help.",
    4: "Dorothy and the Scarecrow walk through the dark forest on the yellow brick road. They hear wild beasts growling, and the Scarecrow tells Dorothy about his life on the pole and his discovery that he has no brains.",
    5: "In the forest, they find the Tin Woodman, rusted stiff beside a tree. Dorothy oils his joints and he comes to life. He tells the sad story of how the Wicked Witch enchanted his axe, and he chopped himself to pieces and was rebuilt in tin -- but without a heart.",
    6: "A great Lion springs from the forest and strikes at the travelers, but when he tries to bite Toto, Dorothy slaps him on the nose. The Lion confesses he is a coward. He joins the company to ask Oz for courage.",
    7: "The four companions travel toward the Emerald City. They cross a deep ditch, fight the Kalidahs (monstrous beasts with tiger heads and bear bodies), and must find a way across a broad river.",
    8: "They enter a field of beautiful poppies whose scent puts Dorothy, Toto, and the Lion to sleep. The Scarecrow and the Tin Woodman, who cannot be affected by the flowers, carry Dorothy and Toto to safety but cannot move the Lion.",
    9: "The Tin Woodman saves the Queen of the Field Mice from a wildcat. In gratitude, she commands thousands of mice to pull the sleeping Lion out of the deadly poppy field on a truck built by the Woodman.",
    10: "The travelers reach the gates of the Emerald City. The Guardian of the Gates locks green spectacles on their eyes so the city's brightness won't blind them, and admits them to the city.",
    11: "Inside the Emerald City, each traveler has a separate audience with Oz, who appears in a different terrifying form to each: a great Head, a beautiful Lady, a terrible Beast, and a Ball of Fire. He tells them they must kill the Wicked Witch of the West before he will grant their wishes.",
    12: "The travelers journey west to find the Wicked Witch. She sends wolves, crows, bees, and her Winkie slaves against them, and finally uses the Golden Cap to summon the Winged Monkeys, who destroy the Scarecrow and the Tin Woodman and capture Dorothy and the Lion.",
    13: "Dorothy is made a slave in the Witch's kitchen. The Witch tries to steal her Silver Shoes. Dorothy, in a rage, throws a bucket of water on the Witch -- and she melts away to nothing. Dorothy frees the Lion and rescues the Scarecrow and Tin Woodman.",
    14: "Dorothy uses the Golden Cap to summon the Winged Monkeys, who carry the friends back to the Emerald City. The King of the Winged Monkeys tells the story of how they were enslaved by the Golden Cap.",
    15: "The travelers demand their rewards from Oz, but discover he is not a wizard at all -- just a little old man behind a screen, a balloonist from Omaha who landed in Oz long ago and has been pretending ever since.",
    16: "Despite being a humbug, Oz gives the Scarecrow a brain (bran and pins), the Tin Woodman a heart (a silk heart stuffed with sawdust), and the Lion courage (a dish of liquid courage). Each is satisfied, though the gifts are symbolic rather than magical.",
    17: "Oz builds a hot-air balloon to take Dorothy back to Kansas. On the day of departure, Toto chases a kitten and Dorothy runs after him -- the balloon lifts off without her. Oz floats away and Dorothy is stranded.",
    18: "Dorothy and her friends set off to find Glinda, the Good Witch of the South, who may know how to send Dorothy home. They travel south through pleasant countryside.",
    19: "The travelers encounter the Fighting Trees, whose branches grab and throw anyone who tries to pass. The Tin Woodman chops through them, and they find themselves at a smooth white wall.",
    20: "Beyond the wall lies the Dainty China Country, a miniature world of fragile china people and animals. The travelers walk carefully through and learn that the china people become stiff and lifeless if they leave their country.",
    21: "In a dark forest, the Lion defeats a great spider that has been terrorizing the animals. The grateful beasts declare him King of the Forest, fulfilling his deepest wish.",
    22: "The travelers cross the hill of the Hammer-Heads (armless creatures with flat heads they shoot forward) with the help of the Winged Monkeys, and reach Glinda's palace in the Country of the Quadlings.",
    23: "Glinda tells Dorothy that the Silver Shoes have had the power to take her home all along -- she need only knock the heels together three times. Dorothy kisses her friends goodbye and wishes herself back to Kansas.",
    24: "Dorothy lands on the Kansas prairie. Aunt Em runs to her. 'My darling child!' she cries. 'Where in the world did you come from?' 'From the Land of Oz,' says Dorothy. 'And here is Toto, too. And oh, Aunt Em! I'm so glad to be at home again!'",
}

CHAPTER_KEYWORDS = {
    0: ["introduction", "fairy-tale", "modernism", "children", "wonder"],
    1: ["kansas", "cyclone", "dorothy", "toto", "prairie", "munchkins"],
    2: ["munchkins", "good-witch", "silver-shoes", "yellow-brick-road", "journey"],
    3: ["scarecrow", "brain", "cornfield", "companionship", "rescue"],
    4: ["forest", "darkness", "scarecrow", "yellow-brick-road", "conversation"],
    5: ["tin-woodman", "heart", "enchantment", "rescue", "companionship"],
    6: ["lion", "cowardice", "courage", "companionship", "forest"],
    7: ["journey", "kalidahs", "river", "teamwork", "danger"],
    8: ["poppies", "sleep", "danger", "rescue", "scarecrow", "tin-woodman"],
    9: ["field-mice", "queen", "rescue", "lion", "gratitude", "kindness"],
    10: ["emerald-city", "gates", "green-spectacles", "guardian", "arrival"],
    11: ["oz", "great-head", "terrifying", "bargain", "wicked-witch"],
    12: ["wicked-witch", "wolves", "crows", "bees", "winged-monkeys", "battle"],
    13: ["dorothy", "slavery", "water", "melting", "liberation", "rescue"],
    14: ["winged-monkeys", "golden-cap", "story", "slavery", "freedom"],
    15: ["oz", "humbug", "deception", "truth", "balloon", "omaha"],
    16: ["brain", "heart", "courage", "gifts", "symbolism", "satisfaction"],
    17: ["balloon", "departure", "failure", "stranded", "toto"],
    18: ["journey", "south", "glinda", "hope", "countryside"],
    19: ["fighting-trees", "danger", "tin-woodman", "wall"],
    20: ["china-country", "fragility", "miniature", "wonder", "gentleness"],
    21: ["lion", "spider", "king", "forest", "courage", "fulfillment"],
    22: ["hammer-heads", "winged-monkeys", "quadlings", "glinda", "arrival"],
    23: ["silver-shoes", "home", "glinda", "farewell", "magic", "power"],
    24: ["kansas", "home", "aunt-em", "reunion", "dorothy", "ending"],
}

CHAPTER_REFLECTIONS = {
    0: "Baum wanted to write fairy tales without the scary parts. Do you think stories need scary parts? Why or why not?",
    1: "Dorothy's world in Kansas is described as completely gray. What does color mean in this story? Have you ever felt like your world was gray?",
    2: "Dorothy didn't mean to kill the witch -- it just happened. Have you ever done something important by accident?",
    3: "The Scarecrow thinks he needs a brain, but he already has good ideas. What's the difference between thinking you're smart and actually being smart?",
    4: "The Scarecrow says he isn't afraid of anything except fire. What are you afraid of? Is being afraid the same as being weak?",
    5: "The Tin Woodman lost his heart and thinks he can't love. But he cries when he steps on a beetle. Can you love without knowing it?",
    6: "The Lion is brave enough to fight anyone, but he's afraid inside. Is someone who acts brave even though they're scared braver than someone who isn't scared at all?",
    7: "The four friends work together -- each one contributing what they're good at. When have you been part of a team where everyone had different strengths?",
    8: "The poppies are beautiful but deadly. Can beautiful things be dangerous? Can dangerous things be beautiful?",
    9: "The Tin Woodman saved a tiny mouse, and it changed everything. Has a small act of kindness ever led to something big in your life?",
    10: "Everyone in the Emerald City wears green glasses. What if the city isn't really green at all? What does that tell us about how we see things?",
    11: "Oz appears differently to each person. Why do you think he shows each one a different face? Do people ever do that in real life?",
    12: "The Wicked Witch uses fear as her greatest weapon. Why is fear so powerful? How do you fight it?",
    13: "Dorothy defeats the most powerful witch with a bucket of water. Sometimes the simplest thing is the most powerful. When has something simple solved a big problem for you?",
    14: "The Winged Monkeys aren't evil -- they're enslaved by the Golden Cap. Does knowing that change how you feel about them?",
    15: "Oz is a humbug -- just an ordinary man. Are you disappointed, or does it make the story better? Can ordinary people do extraordinary things?",
    16: "Oz gives the Scarecrow bran for brains, the Tin Woodman a silk heart, and the Lion a drink for courage. None of it is real magic -- but it works. Why?",
    17: "Dorothy misses the balloon because she chases Toto. Sometimes the things we love most keep us from getting what we want. When has that happened to you?",
    18: "Even after everything, Dorothy doesn't give up. She just finds a new plan. How do you keep going when things don't work out?",
    19: "The Fighting Trees attack anyone who comes close. Do you know anyone like that -- someone who fights because they're protecting something?",
    20: "The china people are beautiful but they break easily. What fragile, beautiful things do you know? How do you treat them?",
    21: "The Lion was always brave enough to be king -- he just didn't know it. What might you already be that you don't know yet?",
    22: "Dorothy uses her last wish from the Golden Cap to help her friends, not herself. Why does she do that?",
    23: "The Silver Shoes could have taken Dorothy home from the very beginning. Why is it important that she didn't know?",
    24: "Dorothy says she's glad to be home. After all those adventures, what makes home special?",
}


# === Story Arc / Thematic Groups ===

STORY_ARCS = {
    "arc-kansas-to-oz": {
        "name": "From Kansas to Oz",
        "chapters": [1, 2, 3, 4, 5, 6],
        "about": "The journey begins: a gray Kansas prairie, a cyclone, and a strange new world of color. Dorothy collects her companions one by one -- the Scarecrow who wants a brain, the Tin Woodman who wants a heart, and the Cowardly Lion who wants courage. Together they follow the yellow brick road toward the Emerald City, each hoping the great Wizard will grant their deepest wish.",
        "for_parents": "These opening chapters establish one of literature's great metaphors: the journey as self-discovery. Each companion already possesses what they seek -- the Scarecrow is clever, the Tin Woodman is compassionate, the Lion is brave. Baum's genius is letting children discover this for themselves. A wonderful opening for conversations about what we already have.",
        "keywords": ["journey", "companions", "yellow-brick-road", "wishes", "friendship"],
    },
    "arc-emerald-city": {
        "name": "The Emerald City",
        "chapters": [7, 8, 9, 10, 11],
        "about": "The difficult road to the Emerald City -- deadly poppies, a river crossing, the rescue by the Field Mice -- and the revelation that Oz demands a terrible price: kill the Wicked Witch of the West. The green spectacles that everyone must wear hint at a deeper deception.",
        "for_parents": "The Emerald City is Baum's great illusion. The green spectacles are literally rose-colored glasses (green-colored, rather) -- the city may not be emerald at all. This is a sophisticated idea for young readers: that what authorities present as real may be constructed. Great for discussions about appearances versus reality.",
        "keywords": ["emerald-city", "oz", "illusion", "deception", "bargain"],
    },
    "arc-witch-battle": {
        "name": "The Battle with the Witch",
        "chapters": [12, 13, 14],
        "about": "The darkest part of the story. The Wicked Witch sends wolves, crows, bees, and the Winged Monkeys against Dorothy's company. The Scarecrow is dismantled, the Tin Woodman is battered, and Dorothy is enslaved. But Dorothy's anger -- and a simple bucket of water -- destroy the Witch. Liberation, rescue, and the flight home on the backs of the Winged Monkeys.",
        "for_parents": "These chapters contain the story's real drama. Dorothy doesn't defeat the Witch through magic or cleverness but through an emotional outburst -- she throws water in anger. Children often worry about their anger; this story validates it. Sometimes anger, properly directed, is exactly what's needed. The Winged Monkeys' backstory also teaches that villains often have their own stories of enslavement.",
        "keywords": ["witch", "battle", "slavery", "liberation", "anger", "water"],
    },
    "arc-truth-and-home": {
        "name": "The Truth About Oz and the Way Home",
        "chapters": [15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        "about": "The great unmasking: Oz is a humbug, just an ordinary man from Omaha. But his symbolic gifts satisfy the Scarecrow, the Tin Woodman, and the Lion perfectly. When the balloon fails, Dorothy must make a second journey -- south to Glinda -- through the Fighting Trees, the China Country, and past the Hammer-Heads. At last Glinda reveals that Dorothy's Silver Shoes held the power to go home all along. 'There's no place like home.'",
        "for_parents": "The second half of Oz is richer than the first. The revelation that Oz is a fraud is one of children's literature's great moments -- adults are not always what they seem, but they can still give us what we need. The symbolic gifts work because belief makes them real. And the Silver Shoes' secret -- that Dorothy always had the power -- is the book's deepest truth: the answer was inside you all along. You just had to go on the journey to discover it.",
        "keywords": ["truth", "humbug", "gifts", "journey-home", "silver-shoes", "glinda"],
    },
}

THEMATIC_GROUPS = {
    "theme-what-you-already-have": {
        "name": "You Already Have What You Seek",
        "chapters": [3, 5, 6, 15, 16, 21, 23],
        "about": "The Scarecrow is clever from the moment we meet him. The Tin Woodman weeps for beetles. The Lion fights Kalidahs. Dorothy's shoes could take her home from the start. The central message of The Wizard of Oz: what you seek is already within you. The journey doesn't give you the gift -- it helps you recognize it.",
        "for_parents": "This is Baum's most important theme and one of the great messages in children's literature. Every child worries about what they lack -- brains, heart, courage, belonging. This story teaches that the qualities we most desire are often the ones we already demonstrate. Ask your child: 'What do you think you need that you might already have?'",
        "keywords": ["self-discovery", "inner-strength", "gifts", "recognition"],
    },
    "theme-illusion-and-truth": {
        "name": "Illusion and Truth",
        "chapters": [10, 11, 15, 16, 20],
        "about": "The Emerald City's green spectacles, Oz's terrifying masks, the humbug behind the curtain, the fragile china people who seem so perfect. Baum fills his story with things that are not what they seem -- and invites readers to look beyond appearances.",
        "for_parents": "Baum was writing in the age of P.T. Barnum and the great American humbug tradition. The Wizard is literally a showman from Omaha. These chapters are wonderful for developing critical thinking: Who's wearing green glasses in our world? What powerful figures might be just ordinary people behind a curtain?",
        "keywords": ["illusion", "deception", "appearance", "truth", "spectacles"],
    },
    "theme-home-and-belonging": {
        "name": "Home and Belonging",
        "chapters": [1, 2, 17, 23, 24],
        "about": "Dorothy never stops wanting to go home. Kansas is gray and dull compared to Oz, but it's where Aunt Em is, and that's enough. The story begins and ends in Kansas -- the whole adventure is a great circle that brings Dorothy back to where she started, transformed by what she's seen.",
        "for_parents": "Why does Dorothy want to go back to gray Kansas when she could stay in magical Oz? Because home isn't about beauty or excitement -- it's about love and belonging. This theme resonates deeply with children who've moved, who miss someone, or who are simply discovering what 'home' means to them.",
        "keywords": ["home", "kansas", "belonging", "love", "return"],
    },
    "theme-friendship-and-loyalty": {
        "name": "Friendship and Loyalty",
        "chapters": [3, 5, 6, 7, 8, 9, 12, 13, 22],
        "about": "The four friends look after each other through every danger. The Scarecrow and Tin Woodman carry Dorothy through the poppies. Dorothy melts the Witch to save the Lion. The Lion fights for the group. Each gives what they have -- even when what they have is supposedly what they lack.",
        "for_parents": "The friendship at the center of Oz is one of its greatest strengths. These are friends who are different from each other -- made of straw, tin, fur, and flesh -- but who protect each other fiercely. The Tin Woodman, who thinks he has no heart, is the most caring. The Scarecrow, who thinks he has no brain, is the cleverest problem-solver. Friendship reveals who we really are.",
        "keywords": ["friendship", "loyalty", "teamwork", "protection", "difference"],
    },
}


def build_grammar():
    text = read_and_strip_gutenberg(SEED_FILE)
    intro_text = extract_introduction(text)
    chapters = split_into_chapters(text)

    items = []
    sort_order = 0

    # === L1: Introduction ===
    if intro_text:
        sort_order += 1
        items.append({
            "id": "introduction",
            "name": "Introduction",
            "sort_order": sort_order,
            "category": "introduction",
            "level": 1,
            "sections": {
                "Story": intro_text,
                "About": CHAPTER_SUMMARIES[0],
                "Reflection": CHAPTER_REFLECTIONS[0],
            },
            "keywords": CHAPTER_KEYWORDS[0],
            "metadata": {"chapter_number": 0, "chapter_name": "Introduction"},
        })

    # === L1: Chapters ===
    chapter_ids = {}
    for chapter_num in sorted(chapters.keys()):
        sort_order += 1
        item_id = f"chapter-{chapter_num:02d}"
        chapter_ids[chapter_num] = item_id

        items.append({
            "id": item_id,
            "name": f"Chapter {chapter_num} — {CHAPTER_TITLES[chapter_num]}",
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
                "chapter_name": CHAPTER_TITLES[chapter_num],
            },
        })

    # === L2: Story Arcs ===
    for arc_id, arc_data in STORY_ARCS.items():
        sort_order += 1
        composite = [chapter_ids[ch] for ch in arc_data["chapters"] if ch in chapter_ids]

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
        composite = [chapter_ids[ch] for ch in theme_data["chapters"] if ch in chapter_ids]

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
            "About": "The complete narrative arc of The Wonderful Wizard of Oz in four movements: the journey from Kansas to Oz, the arrival at the Emerald City, the battle with the Wicked Witch, and the discovery that the Wizard is a humbug and the way home was always within reach. Twenty-four chapters of the first great American fairy tale.",
            "For Parents": "The Wonderful Wizard of Oz (1900) is the foundational American fairy tale -- the first to be set entirely in an American landscape of imagination. Unlike European fairy tales with their kings and princesses, Oz features a Kansas farm girl, a confidence man from Omaha, and a quartet of misfits who discover they already have what they seek. Read it as a bedtime adventure, but know that it works on deeper levels too: as a story about self-knowledge, about the gap between appearance and reality, and about the irreplaceable power of home.",
        },
        "keywords": ["complete-story", "narrative", "chapters", "oz"],
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
            "About": "The great themes of The Wizard of Oz: that you already have what you seek, that illusion and truth are woven together, that home is where love is, and that true friendship reveals who we really are. These themes cut across the chapters, connecting scenes from different parts of the story.",
            "For Parents": "These thematic groupings help you explore Oz beyond the plot. If your child is fascinated by the Emerald City's green spectacles, follow the Illusion and Truth thread. If they ask why Dorothy wants to go back to gray Kansas, explore Home and Belonging. The book rewards reading from many angles.",
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
                    "name": "L. Frank Baum",
                    "date": "1900",
                    "note": "Author of The Wonderful Wizard of Oz",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "1993",
                    "note": "eBook #55 — digitized text",
                },
                {
                    "name": "PlayfulProcess",
                    "date": "2026-03-04",
                    "note": "Grammar construction and thematic groupings",
                },
            ],
        },
        "name": "The Wonderful Wizard of Oz",
        "description": (
            "L. Frank Baum's The Wonderful Wizard of Oz (1900) -- the first great American fairy tale. "
            "Dorothy, a Kansas farm girl, is carried by a cyclone to the Land of Oz, where she meets "
            "the Scarecrow, the Tin Woodman, and the Cowardly Lion. Together they follow the yellow brick road "
            "to the Emerald City, seeking brains, a heart, courage, and a way home -- only to discover that "
            "a humbug wizard and a pair of Silver Shoes hold truths about what we already have within us. "
            "Twenty-four chapters structured as story arcs and thematic groupings.\n\n"
            "Source: Project Gutenberg eBook #55 (https://www.gutenberg.org/ebooks/55). "
            "Text matches the original 1900 George M. Hill Company edition.\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES:\n"
            "- W.W. Denslow (1900, George M. Hill Company) -- original illustrator, iconic color plates "
            "of Dorothy, the Scarecrow, the Tin Woodman, and the Cowardly Lion in bold Art Nouveau style\n"
            "- John R. Neill (1904 onward, Reilly & Britton) -- illustrated all subsequent Oz books, "
            "elegant pen-and-ink drawings with more detailed, whimsical style"
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "children",
            "classic",
            "adventure",
            "fantasy",
            "public-domain",
            "l-frank-baum",
            "wizard-of-oz",
            "full-text",
            "chapters",
            "multi-level",
            "american",
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

    # Self-check
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
