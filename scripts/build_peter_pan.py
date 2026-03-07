#!/usr/bin/env python3
"""
Build grammar.json for Peter Pan (Peter and Wendy) by J.M. Barrie.

Source: Project Gutenberg eBook #16
Structure: 17 chapters -> split into scenes within each chapter.
Levels:
  L1: Individual scenes/passages within chapters
  L2: Chapters (with composite_of referencing L1 scenes) + Thematic groups
  L3: Meta-categories (The Story, Themes)
"""

import json
import re
import textwrap
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "seeds" / "peter-pan.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "peter-pan"
OUTPUT_FILE = OUTPUT_DIR / "grammar.json"

# Chapter titles as they appear in the text
CHAPTER_TITLES = {
    1: "Peter Breaks Through",
    2: "The Shadow",
    3: "Come Away, Come Away!",
    4: "The Flight",
    5: "The Island Come True",
    6: "The Little House",
    7: "The Home Under the Ground",
    8: "The Mermaids' Lagoon",
    9: "The Never Bird",
    10: "The Happy Home",
    11: "Wendy's Story",
    12: "The Children Are Carried Off",
    13: "Do You Believe in Fairies?",
    14: "The Pirate Ship",
    15: '"Hook or Me This Time"',
    16: "The Return Home",
    17: "When Wendy Grew Up",
}

# Scene breakdowns for each chapter - tuples of (scene_name, keywords, start_phrase)
# We'll split chapters into scenes based on narrative shifts
SCENE_DEFINITIONS = {
    1: [
        ("The Darling Family", ["wendy", "darling", "family", "childhood"], None),
        ("Nana the Nursemaid", ["nana", "dog", "nursemaid", "nursery"], "Mrs. Darling loved to have everything just so"),
        ("Maps of Children's Minds", ["neverland", "imagination", "children", "maps"], "I don't know whether you have ever seen a map"),
        ("Peter Pan Is Mentioned", ["peter-pan", "wendy", "belief", "childhood"], "Occasionally in her travels through her children"),
        ("Leaves on the Nursery Floor", ["peter-pan", "shadow", "nursery", "mystery"], "Children have the strangest adventures"),
        ("Mrs. Darling Sees Peter", ["peter-pan", "window", "mrs-darling", "shadow"], "Next night the children were once more"),
    ],
    2: [
        ("The Shadow in the Drawer", ["shadow", "nana", "mrs-darling", "mystery"], None),
        ("Mr. Darling and the Medicine", ["mr-darling", "michael", "medicine", "pride"], "It may have been in consequence"),
        ("Nana in Disgrace", ["nana", "mr-darling", "chained", "consequence"], "Mr. Darling was frightfully ashamed"),
        ("The Darlings Go Out", ["parents", "evening", "departure", "nursery"], "Mrs. Darling put the children"),
        ("Peter and Tinker Bell Arrive", ["peter-pan", "tinker-bell", "fairy", "nursery"], "For a moment after Mr. and Mrs. Darling"),
    ],
    3: [
        ("Peter and His Shadow", ["peter-pan", "shadow", "wendy", "sewing"], None),
        ("Peter's Story", ["peter-pan", "wendy", "fairies", "origin"], "Wendy, Wendy, when you are sleeping"),
        ("The Thimble Kiss", ["peter-pan", "wendy", "kiss", "thimble"], None),
        ("Tinker Bell's Jealousy", ["tinker-bell", "jealousy", "fairy", "wendy"], "If you shut your eyes"),
        ("Come Away to Neverland", ["neverland", "flight", "invitation", "adventure"], "Peter, how old are you"),
        ("Learning to Fly", ["flying", "fairy-dust", "peter-pan", "children"], "Of course Peter had been trifling"),
    ],
    4: [
        ("Second to the Right", ["flying", "london", "night", "stars"], None),
        ("Flying Over London", ["flying", "night", "adventure", "wonder"], "In a sort of way"),
        ("Peter's Games in the Air", ["peter-pan", "mischief", "flying", "danger"], "Indeed they sometimes"),
        ("Wendy Worries About the Children", ["wendy", "mothering", "care", "responsibility"], "After a time he fell asleep"),
        ("The Neverland Appears", ["neverland", "island", "arrival", "wonder"], "I don't know whether any"),
    ],
    5: [
        ("The Island Wakes Up", ["neverland", "pirates", "lost-boys", "indians"], None),
        ("The Lost Boys", ["lost-boys", "tootles", "nibs", "slightly", "twins", "curly"], "Let us pretend to lie here"),
        ("Captain Hook", ["hook", "pirate", "villain", "fear"], "In the middle of the island"),
        ("Hook and the Crocodile", ["hook", "crocodile", "ticking", "fear"], "Hook was not his true name"),
        ("The Search for Peter Pan", ["neverland", "chase", "adventure", "circles"], "In the meantime the boys were"),
        ("Wendy Is Shot Down", ["wendy", "tootles", "shot", "arrival"], "It was well for those boys"),
    ],
    6: [
        ("Wendy Falls from the Sky", ["wendy", "tootles", "arrow", "button"], None),
        ("The Wendy House", ["wendy-house", "lost-boys", "building", "song"], "Let us build a little house"),
        ("Wendy Becomes Their Mother", ["wendy", "mothering", "lost-boys", "stories"], None),
    ],
    7: [
        ("Life Underground", ["underground", "home", "lost-boys", "daily-life"], None),
        ("The Pretend Meals", ["pretend", "meals", "make-believe", "play"], None),
        ("Peter and Wendy as Parents", ["peter-pan", "wendy", "pretend-parents", "roles"], "One of the first things Peter did"),
        ("Wendy's Troubled Heart", ["wendy", "feelings", "peter-pan", "growing-up"], None),
    ],
    8: [
        ("The Mermaids' Lagoon", ["mermaids", "lagoon", "neverland", "beauty"], None),
        ("Marooner's Rock", ["marooners-rock", "pirates", "tiger-lily", "danger"], "One of the most delightful"),
        ("Peter Saves Tiger Lily", ["peter-pan", "tiger-lily", "rescue", "bravery"], None),
        ("Stranded on the Rock", ["peter-pan", "wendy", "stranded", "danger"], "Two boys were already on it"),
        ("The Never Bird", ["never-bird", "nest", "rescue", "kindness"], None),
    ],
    9: [
        ("The Never Bird's Sacrifice", ["never-bird", "nest", "peter-pan", "rescue"], None),
    ],
    10: [
        ("The Happy Home", ["home", "underground", "family", "happiness"], None),
        ("Wendy Tells Stories", ["stories", "wendy", "darlings", "homesick"], "I don't suppose any of them"),
        ("Peter's Feelings", ["peter-pan", "feelings", "mothers", "conflict"], None),
    ],
    11: [
        ("Wendy's Story of the Darlings", ["wendy", "story", "darlings", "parents"], None),
        ("Peter's Reaction", ["peter-pan", "mothers", "rejection", "pain"], "I thought all mothers were like that"),
        ("The Window Must Stay Open", ["window", "hope", "return", "mothers"], None),
    ],
    12: [
        ("The Pirates Attack", ["pirates", "attack", "capture", "danger"], None),
        ("The Children Are Taken", ["capture", "children", "hook", "pirates"], None),
        ("Peter Sleeps Through It", ["peter-pan", "sleep", "alone", "danger"], None),
    ],
    13: [
        ("Hook Poisons Peter's Medicine", ["hook", "poison", "peter-pan", "danger"], None),
        ("Tinker Bell Drinks the Poison", ["tinker-bell", "sacrifice", "poison", "loyalty"], None),
        ("Do You Believe in Fairies?", ["tinker-bell", "belief", "clapping", "audience"], None),
        ("Peter Sets Out to Rescue", ["peter-pan", "rescue", "determination", "bravery"], None),
    ],
    14: [
        ("On the Pirate Ship", ["pirate-ship", "hook", "captives", "wendy"], None),
        ("Walk the Plank", ["walk-the-plank", "pirates", "danger", "cruelty"], None),
        ("Peter Boards the Ship", ["peter-pan", "rescue", "pirate-ship", "ticking"], None),
    ],
    15: [
        ("The Final Battle", ["battle", "peter-pan", "hook", "sword-fight"], None),
        ("Hook and Peter Duel", ["duel", "hook", "peter-pan", "climax"], None),
        ("Hook's End", ["hook", "crocodile", "defeat", "ending"], None),
    ],
    16: [
        ("Flying Home", ["flying", "home", "return", "london"], None),
        ("The Window Is Open", ["window", "open", "mother", "waiting"], None),
        ("The Reunion", ["reunion", "family", "darlings", "joy"], None),
    ],
    17: [
        ("The Lost Boys Are Adopted", ["lost-boys", "adopted", "darlings", "family"], None),
        ("Peter Refuses to Stay", ["peter-pan", "refusal", "growing-up", "freedom"], None),
        ("Spring Cleaning", ["spring-cleaning", "wendy", "peter-pan", "annual"], None),
        ("When Wendy Grew Up", ["wendy", "grown-up", "jane", "margaret"], "But, of course, Wendy had"),
        ("So Long as Children Are Innocent", ["ending", "cycle", "children", "heartless"], "As you look at Wendy"),
    ],
}

# Thematic groupings for L2
THEMATIC_GROUPS = {
    "theme-adventure-and-flight": {
        "name": "Adventure and Flight",
        "description": "The thrilling journeys through sky and sea — from flying over London to battling pirates on the high seas.",
        "for_parents": "These scenes capture the spirit of adventure that lives in every child. Use them to talk about courage, risk-taking, and the difference between bravery and recklessness. What adventures does your child dream about?",
        "keywords": ["adventure", "flying", "battle", "pirates", "neverland"],
        "chapters": [3, 4, 5, 8, 14, 15],
    },
    "theme-growing-up": {
        "name": "Growing Up and Growing Old",
        "description": "The central tension of Peter Pan — the beauty and sadness of growing up, and Peter's eternal refusal to do so.",
        "for_parents": "These passages explore what it means to grow up. Children may not fully grasp these themes yet, but planting the seeds of reflection — that growing up brings both loss and gain — is one of the gifts of this story.",
        "keywords": ["growing-up", "childhood", "time", "aging", "mothers"],
        "chapters": [1, 7, 11, 16, 17],
    },
    "theme-imagination-and-belief": {
        "name": "Imagination and Belief",
        "description": "The power of belief, make-believe, and imagination — from fairy dust to the clapping that saves Tinker Bell.",
        "for_parents": "Peter Pan celebrates the power of belief and imagination. 'Do you believe in fairies?' is one of literature's great invitations. These passages are perfect for exploring what your child believes in and why imagination matters.",
        "keywords": ["imagination", "belief", "fairies", "make-believe", "pretend"],
        "chapters": [1, 3, 7, 13],
    },
    "theme-mothers-and-home": {
        "name": "Mothers and Home",
        "description": "The ache of home that runs through the story — Mrs. Darling waiting at the window, Wendy mothering the Lost Boys, and Peter's complicated feelings about mothers.",
        "for_parents": "Barrie lost his brother at age 13 and watched his mother grieve for the rest of her life. The theme of mothers — their love, their loss, the open window — is the emotional heart of Peter Pan. These scenes are rich for conversations about family, belonging, and what 'home' really means.",
        "keywords": ["mother", "home", "family", "love", "belonging"],
        "chapters": [1, 6, 10, 11, 16, 17],
    },
    "theme-good-and-evil": {
        "name": "Good Form and Villainy",
        "description": "Captain Hook — one of literature's great villains — and the moral questions the story raises about good form, fairness, and what makes someone truly wicked.",
        "for_parents": "Hook is obsessed with 'good form' — proper behavior — even as he commits terrible acts. This paradox makes him one of the most interesting villains in children's literature. Use these scenes to explore what it really means to be good versus merely appearing good.",
        "keywords": ["hook", "villain", "good-form", "morality", "pirates"],
        "chapters": [5, 12, 13, 14, 15],
    },
}


def read_and_strip_gutenberg(filepath):
    """Read the seed text and strip Gutenberg header/footer."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Strip header
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK PETER PAN ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    # Strip footer
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK PETER PAN ***"
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    # Strip the initial metadata block (title, author, edition note, contents)
    # Find where Chapter I actually begins
    ch1_match = re.search(r'\nChapter I\.\n', text)
    if ch1_match:
        text = text[ch1_match.start():]

    # Strip "THE END" at the very end
    text = re.sub(r'\n\s*THE END\s*$', '', text.strip())

    return text.strip()


def split_into_chapters(text):
    """Split the full text into chapters."""
    # Pattern: Chapter <roman>.\nTITLE
    chapter_pattern = re.compile(
        r'^Chapter\s+(X{0,3}(?:IX|IV|V?I{0,3}))\.\n([A-Z].*?)(?=\n)',
        re.MULTILINE
    )

    matches = list(chapter_pattern.finditer(text))
    chapters = {}

    for i, match in enumerate(matches):
        roman = match.group(1)
        chapter_num = roman_to_int(roman)

        # Chapter content: from after the title line to the next chapter
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        # Clean up: remove extra blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)

        chapters[chapter_num] = content

    return chapters


def roman_to_int(s):
    """Convert Roman numeral string to integer."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
    result = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and values[c] < values[s[i + 1]]:
            result -= values[c]
        else:
            result += values[c]
    return result


def split_chapter_into_scenes(chapter_num, chapter_text, scene_defs):
    """Split a chapter's text into scenes based on scene definitions."""
    scenes = []
    num_scenes = len(scene_defs)

    if num_scenes == 1:
        # Single scene — use the whole chapter
        scene_name, keywords, _ = scene_defs[0]
        scenes.append((scene_name, chapter_text.strip(), keywords))
        return scenes

    # Split text into paragraphs
    paragraphs = re.split(r'\n\s*\n', chapter_text.strip())
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if not paragraphs:
        return scenes

    # Try to find split points using start phrases
    split_indices = [0]  # First scene always starts at 0
    for i in range(1, num_scenes):
        scene_name, keywords, start_phrase = scene_defs[i]
        if start_phrase:
            # Find the paragraph that starts with this phrase
            found = False
            for j, para in enumerate(paragraphs):
                if para.startswith(start_phrase):
                    split_indices.append(j)
                    found = True
                    break
            if not found:
                # Approximate: divide remaining evenly
                split_indices.append(None)
        else:
            split_indices.append(None)

    # Fill in None values with even distribution
    filled = [split_indices[0]]
    for i in range(1, len(split_indices)):
        if split_indices[i] is not None:
            filled.append(split_indices[i])
        else:
            # Find the next known index
            next_known = None
            next_known_pos = None
            for j in range(i + 1, len(split_indices)):
                if split_indices[j] is not None:
                    next_known = split_indices[j]
                    next_known_pos = j
                    break

            prev_known = filled[-1]

            if next_known is not None:
                # Distribute evenly between prev_known and next_known
                gap = next_known - prev_known
                steps = next_known_pos - (i - 1)
                step_size = max(1, gap // steps)
                filled.append(min(prev_known + step_size, len(paragraphs) - 1))
            else:
                # Distribute evenly to the end
                remaining_scenes = num_scenes - i
                remaining_paras = len(paragraphs) - prev_known
                step_size = max(1, remaining_paras // (remaining_scenes + 1))
                filled.append(min(prev_known + step_size, len(paragraphs) - 1))

    # Ensure split indices are strictly increasing
    for i in range(1, len(filled)):
        if filled[i] <= filled[i - 1]:
            filled[i] = min(filled[i - 1] + 1, len(paragraphs) - 1)

    # Build scenes from paragraphs
    for i in range(num_scenes):
        scene_name, keywords, _ = scene_defs[i]
        start_para = filled[i]
        end_para = filled[i + 1] if i + 1 < len(filled) else len(paragraphs)

        scene_paragraphs = paragraphs[start_para:end_para]
        scene_text = "\n\n".join(scene_paragraphs)

        if scene_text.strip():
            scenes.append((scene_name, scene_text.strip(), keywords))

    return scenes


def make_id(chapter_num, scene_name):
    """Generate a hyphenated ID from chapter number and scene name."""
    slug = scene_name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return f"ch{chapter_num:02d}-{slug}"


def generate_reflection(scene_name, chapter_title, keywords):
    """Generate a reflection prompt based on scene content."""
    reflections = {
        "growing-up": "What does it mean to grow up? Is it something that happens all at once, or little by little?",
        "flying": "What would it feel like to fly? What would you see from up high?",
        "adventure": "What makes an adventure exciting — and when does it become scary?",
        "imagination": "What's the most wonderful thing you've ever imagined?",
        "mother": "What does home feel like to you? What would you miss most if you went far away?",
        "home": "Why do people want to come home, even when they're having an adventure?",
        "belief": "What do you believe in that other people might not? Why does believing matter?",
        "peter-pan": "Why do you think Peter never wants to grow up? Is that brave or sad — or both?",
        "hook": "What makes someone a villain? Is Captain Hook just mean, or is there more to him?",
        "wendy": "Why does Wendy want to be a mother to the Lost Boys? What does taking care of others teach us?",
        "lost-boys": "What would it be like to live without any grown-ups? What would be fun, and what would be hard?",
        "tinker-bell": "Have you ever been jealous of someone your friend liked? How did it feel?",
        "neverland": "If you could create your own magical island, what would be on it?",
        "pirates": "Pirates in stories seem exciting, but they're also cruel. Why do you think stories have villains?",
        "family": "What makes a family? Is it just the people you're related to?",
    }

    for kw in keywords:
        if kw in reflections:
            return reflections[kw]

    return "What does this part of the story make you think about? What feelings does it bring up?"


def build_grammar():
    """Build the complete Peter Pan grammar."""
    text = read_and_strip_gutenberg(SEED_FILE)
    chapters = split_into_chapters(text)

    items = []
    sort_order = 0
    chapter_scene_ids = {}  # chapter_num -> list of L1 scene ids

    # === L1: Individual scenes ===
    for chapter_num in sorted(chapters.keys()):
        chapter_text = chapters[chapter_num]
        scene_defs = SCENE_DEFINITIONS.get(chapter_num, [("Full Chapter", [], None)])
        scenes = split_chapter_into_scenes(chapter_num, chapter_text, scene_defs)

        chapter_scene_ids[chapter_num] = []

        for scene_name, scene_text, keywords in scenes:
            sort_order += 1
            item_id = make_id(chapter_num, scene_name)
            chapter_scene_ids[chapter_num].append(item_id)

            reflection = generate_reflection(scene_name, CHAPTER_TITLES.get(chapter_num, ""), keywords)

            item = {
                "id": item_id,
                "name": scene_name,
                "sort_order": sort_order,
                "category": f"chapter-{chapter_num:02d}",
                "level": 1,
                "sections": {
                    "Story": scene_text,
                    "Reflection": reflection,
                },
                "keywords": keywords,
                "metadata": {
                    "chapter_number": chapter_num,
                    "chapter_name": CHAPTER_TITLES.get(chapter_num, ""),
                },
            }
            items.append(item)

    # === L2: Chapter summaries ===
    chapter_summaries = {
        1: "We meet the Darling family — practical Mr. Darling, romantic Mrs. Darling, and their three children Wendy, John, and Michael, looked after by Nana the Newfoundland dog. Mrs. Darling discovers the name 'Peter Pan' in her children's minds, and one night sees a strange boy at the nursery window.",
        2: "Peter's shadow is caught by Nana and locked in a drawer. Mr. Darling, in a fit of wounded pride, chains Nana outside. The Darling parents leave for a dinner party, and while they're gone, Peter Pan and his fairy companion Tinker Bell slip into the nursery.",
        3: "Wendy sews Peter's shadow back on. Peter tells her about the Lost Boys and Neverland, and invites her to come and be their mother. After sprinkling fairy dust, the children learn to fly — 'You just think lovely wonderful thoughts and they lift you up in the air.'",
        4: "The children fly through the night sky over London, guided by Peter's directions: 'Second to the right, and straight on till morning.' The flight is long and exhausting, full of Peter's dangerous games, until at last Neverland appears on the horizon.",
        5: "Neverland awakens with Peter's return. We meet the Lost Boys, the pirates led by Captain Hook, and the brave Tiger Lily and her warriors. Hook is haunted by a ticking crocodile that once tasted his hand. Wendy is accidentally shot from the sky by Tootles.",
        6: "Wendy survives — saved by a button Peter gave her. The Lost Boys build a little house around her where she fell, and she agrees to be their mother and tell them stories every night.",
        7: "The children settle into a cozy underground home with mushroom chimneys and make-believe meals. Peter and Wendy play at being father and mother, but Wendy's feelings grow complicated as she realizes Peter only pretends.",
        8: "An afternoon at the Mermaids' Lagoon turns dangerous when Hook's pirates arrive with the captured Tiger Lily. Peter saves her through clever mimicry of Hook's voice. Peter and Wendy are left stranded on Marooner's Rock as the tide rises.",
        9: "Stranded on the rock, Peter is saved by the Never Bird, who floats her nest to him as a boat. Even the bird's selfless act carries Barrie's characteristic humor and pathos.",
        10: "Domestic life in the underground home — Wendy keeps house, tells stories, and tucks the boys in. But the children begin to forget their real parents, and only Wendy holds onto the memory of the nursery window left open for them.",
        11: "Wendy tells the Lost Boys the story of the Darling children, making them homesick. Peter reacts with pain and defiance — 'Long ago I thought like you that my mother would always keep the window open for me... but the window was barred.' He refuses to go back.",
        12: "While the children prepare to leave Neverland, Hook's pirates ambush them. One by one the children are captured and carried to the pirate ship. Peter, alone underground, sleeps through it all.",
        13: "Hook sneaks underground and poisons Peter's medicine. Tinker Bell discovers the plot and drinks the poison herself to save Peter. As she lies dying, Peter begs children everywhere to clap if they believe in fairies — and they do.",
        14: "On the pirate ship, Hook forces Wendy to be the pirates' mother. The boys are lined up to walk the plank. But then — tick, tick, tick — they hear the sound of the crocodile. It's not the crocodile. It's Peter.",
        15: "The great battle on the pirate ship. Peter and the Lost Boys fight the pirates, and Peter faces Hook in single combat. Hook, defeated and unable to bear Peter's 'good form,' throws himself to the crocodile. Peter takes command of the ship.",
        16: "The children fly home to London. Mrs. Darling has kept the nursery window open all this time, waiting. The reunion is joyful — even Mr. Darling is transformed. All the Lost Boys are adopted, except Peter, who watches from outside the window.",
        17: "Years pass. The Lost Boys grow up and go to offices. Peter returns for Wendy one spring, but she is a woman now with a daughter of her own — Jane. Peter takes Jane to Neverland instead, and so it goes on, generation after generation, 'so long as children are gay and innocent and heartless.'",
    }

    for chapter_num in sorted(chapters.keys()):
        sort_order += 1
        chapter_id = f"chapter-{chapter_num:02d}"
        scene_ids = chapter_scene_ids.get(chapter_num, [])

        item = {
            "id": chapter_id,
            "name": f"Chapter {chapter_num} — {CHAPTER_TITLES[chapter_num]}",
            "sort_order": sort_order,
            "category": "chapter-summary",
            "level": 2,
            "relationship_type": "emergence",
            "composite_of": scene_ids,
            "sections": {
                "About": chapter_summaries.get(chapter_num, ""),
                "For Parents": get_chapter_parent_note(chapter_num),
            },
            "keywords": get_chapter_keywords(chapter_num),
            "metadata": {
                "chapter_number": chapter_num,
                "chapter_name": CHAPTER_TITLES[chapter_num],
            },
        }
        items.append(item)

    # === L2: Thematic groups ===
    for theme_id, theme_data in THEMATIC_GROUPS.items():
        sort_order += 1

        # Collect all L1 scene IDs from the relevant chapters
        theme_scene_ids = []
        for ch_num in theme_data["chapters"]:
            theme_scene_ids.extend(chapter_scene_ids.get(ch_num, []))

        item = {
            "id": theme_id,
            "name": theme_data["name"],
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "relationship_type": "emergence",
            "composite_of": theme_scene_ids,
            "sections": {
                "About": theme_data["description"],
                "For Parents": theme_data["for_parents"],
            },
            "keywords": theme_data["keywords"],
            "metadata": {},
        }
        items.append(item)

    # === L3: Meta-categories ===
    all_chapter_ids = [f"chapter-{n:02d}" for n in sorted(chapters.keys())]
    all_theme_ids = list(THEMATIC_GROUPS.keys())

    sort_order += 1
    items.append({
        "id": "meta-the-story",
        "name": "The Story",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "relationship_type": "emergence",
        "composite_of": all_chapter_ids,
        "sections": {
            "About": "The complete narrative arc of Peter Pan, from the Darling nursery to Neverland and back again. Seventeen chapters trace the journey of Wendy, John, and Michael to the island where children never grow up — and the bittersweet return home that changes everything.",
            "For Parents": "Peter Pan is often thought of as a simple adventure story, but it is one of the most emotionally complex works in children's literature. Barrie wrote from deep personal loss — the death of his older brother David at age 13, and the way his mother clung to the memory of the boy who would never grow up. The story works on two levels: as a thrilling adventure for children, and as a meditation on time, memory, and what we lose when we leave childhood behind. Read it together and let it grow with your child.",
        },
        "keywords": ["peter-pan", "complete-story", "narrative", "chapters"],
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
            "About": "The great themes woven through Peter Pan — adventure and flight, growing up, imagination, the meaning of home, and the nature of good and evil. These thematic groups cut across the chapters, revealing how Barrie returns again and again to the same deep questions.",
            "For Parents": "These thematic groupings help you explore Peter Pan beyond the plot. Each theme connects scenes from different chapters that share a common thread. If your child is captivated by the flying scenes, follow the Adventure thread. If they ask why Peter won't grow up, explore the Growing Up theme. The story rewards multiple readings from many angles.",
        },
        "keywords": ["themes", "analysis", "groupings", "perspectives"],
        "metadata": {},
    })

    # === Build the grammar ===
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "J.M. Barrie",
                    "date": "1911",
                    "note": "Original author of Peter and Wendy (Peter Pan)",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2008",
                    "note": "eBook #16 — digitized by Duncan Research",
                },
                {
                    "name": "PlayfulProcess",
                    "date": "2026-03-04",
                    "note": "Grammar construction and scene breakdown",
                },
            ],
        },
        "name": "Peter Pan",
        "description": (
            "J.M. Barrie's Peter Pan (originally published as Peter and Wendy, 1911) — "
            "the beloved story of the boy who never grew up, the Darling children's flight to Neverland, "
            "and the bittersweet truth that all children, except one, grow up. "
            "Structured as scenes within 17 chapters, with thematic groupings for adventure, imagination, "
            "growing up, mothers and home, and good and evil.\n\n"
            "Source: Project Gutenberg eBook #16 (https://www.gutenberg.org/ebooks/16). "
            "Text matches the 1911 original publication.\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES:\n"
            "- F.D. Bedford (1911, Hodder & Stoughton) — original edition illustrator, "
            "detailed pen-and-ink drawings of Neverland, the Darling nursery, and the pirate ship\n"
            "- Arthur Rackham (1906, Hodder & Stoughton) — illustrated Peter Pan in Kensington Gardens, "
            "atmospheric watercolors of fairies and the Serpentine\n"
            "- Mabel Lucie Attwell (1921, Hodder & Stoughton) — charming, rounded children's illustrations"
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "children",
            "classic",
            "adventure",
            "fantasy",
            "public-domain",
            "j-m-barrie",
            "peter-pan",
            "neverland",
            "full-text",
            "scenes",
            "multi-level",
        ],
        "roots": ["western-literary", "romanticism"],
        "shelves": ["children", "wonder"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "romantic",
        "items": items,
    }

    return grammar


def get_chapter_keywords(chapter_num):
    """Return keywords for a chapter summary."""
    keywords_map = {
        1: ["darling-family", "nana", "nursery", "peter-pan", "neverland"],
        2: ["shadow", "mr-darling", "nana", "peter-pan", "tinker-bell"],
        3: ["shadow", "sewing", "fairy-dust", "flying", "neverland"],
        4: ["flying", "london", "night", "stars", "neverland"],
        5: ["neverland", "lost-boys", "hook", "pirates", "tiger-lily"],
        6: ["wendy", "wendy-house", "mothering", "lost-boys"],
        7: ["underground", "home", "pretend", "family"],
        8: ["mermaids", "lagoon", "hook", "tiger-lily", "rescue"],
        9: ["never-bird", "rescue", "sacrifice"],
        10: ["home", "stories", "forgetting", "homesick"],
        11: ["story", "mothers", "window", "peter-pan"],
        12: ["pirates", "capture", "ambush", "danger"],
        13: ["poison", "tinker-bell", "belief", "fairies"],
        14: ["pirate-ship", "plank", "peter-pan", "rescue"],
        15: ["battle", "hook", "peter-pan", "sword-fight"],
        16: ["return", "london", "window", "reunion"],
        17: ["growing-up", "time", "jane", "margaret", "cycle"],
    }
    return keywords_map.get(chapter_num, [])


def get_chapter_parent_note(chapter_num):
    """Return a 'For Parents' note for each chapter."""
    notes = {
        1: "This opening chapter introduces the Darling family with Barrie's characteristic blend of humor and melancholy. The famous opening line — 'All children, except one, grow up' — sets the tone for the whole book. The passage about 'maps of children's minds' is a beautiful way to start a conversation about imagination.",
        2: "The conflict between Mr. Darling and Nana is both comic and consequential — his wounded pride leads directly to the children's departure. This is a good chapter for talking about how grown-ups sometimes make mistakes when they feel embarrassed.",
        3: "The scene where Wendy sews Peter's shadow on is rich with symbolism — Wendy literally helps Peter become whole. Peter's boastfulness and Wendy's nurturing instinct are established here. The fairy dust scene is pure magic.",
        4: "The flight to Neverland is one of literature's great journeys. But notice how Peter is careless with the children's safety — he forgets to feed them, plays dangerous games. This is a good opening for talking about the difference between fun and responsibility.",
        5: "This chapter introduces the full cast of Neverland. Hook is presented as both terrifying and absurd — obsessed with 'good form' even as he plots murder. The shooting of Wendy is a genuinely shocking moment that children often want to discuss.",
        6: "The building of Wendy's house is one of the most tender scenes in the book. The Lost Boys' desire for a mother is heartbreaking in its simplicity. This chapter raises questions about what children need most.",
        7: "The pretend meals and pretend family are both funny and sad. Peter cannot tell the difference between pretend and real, which delights the boys but troubles Wendy. A good chapter for exploring what's real versus what's make-believe.",
        8: "The Mermaids' Lagoon is the book's great adventure set piece. Peter's bravery is real but so is his recklessness. The line 'To die will be an awfully big adventure' is one of the most famous — and most debated — in children's literature.",
        9: "A short, beautiful chapter about the Never Bird's sacrifice. Even nature in Neverland has a fierce maternal instinct. Good for talking about kindness from unexpected places.",
        10: "The happy domestic life underground is shadowed by the children forgetting their real parents. This tension — between the freedom of Neverland and the pull of home — is the heart of the story.",
        11: "This is the emotional climax before the action climax. Peter's confession that his mother barred the window is devastating. It explains everything about why he won't grow up — and why he can't love.",
        12: "The pirate attack is swift and brutal — a reminder that Neverland has real dangers. Peter sleeping through the capture underscores his strange disconnection from others' needs.",
        13: "The 'Do you believe in fairies?' scene breaks the fourth wall in a way that still electrifies audiences. Tinker Bell's sacrifice and the audience's role in saving her raise beautiful questions about the power of collective belief.",
        14: "The rescue scene is pure adventure. Peter's imitation of the crocodile's ticking shows his cunning, while the tension of the walk-the-plank scene keeps children on the edge of their seats.",
        15: "The final battle is cathartic but also complex. Hook's obsession with 'good form' — and his realization that Peter has it naturally — drives him to his end. There's a philosophical depth here about authenticity versus performance.",
        16: "The reunion is joyous but tinged with Peter watching from outside the window. The image of the open window — Mrs. Darling's faith rewarded — is one of the most powerful in the book. A beautiful chapter for talking about homecoming.",
        17: "The final chapter is one of the most poignant in children's literature. Wendy grows up, and Peter cannot understand it. The cycle repeats with Jane, then Margaret, 'so long as children are gay and innocent and heartless.' That last word — 'heartless' — is Barrie's final, unforgettable note.",
    }
    return notes.get(chapter_num, "")


def main():
    print(f"Reading seed text from {SEED_FILE}...")
    grammar = build_grammar()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write grammar
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Print stats
    items = grammar["items"]
    l1 = [i for i in items if i["level"] == 1]
    l2 = [i for i in items if i["level"] == 2]
    l3 = [i for i in items if i["level"] == 3]

    print(f"Grammar written to {OUTPUT_FILE}")
    print(f"  L1 scenes: {len(l1)}")
    print(f"  L2 chapters + themes: {len(l2)}")
    print(f"  L3 meta-categories: {len(l3)}")
    print(f"  Total items: {len(items)}")

    # Quick self-check
    ids = [i["id"] for i in items]
    id_set = set(ids)
    dupes = len(ids) - len(id_set)
    if dupes:
        print(f"  WARNING: {dupes} duplicate IDs found!")

    # Check composite_of references
    broken = []
    for item in items:
        for ref in item.get("composite_of", []):
            if ref not in id_set:
                broken.append((item["id"], ref))
    if broken:
        print(f"  WARNING: {len(broken)} broken references:")
        for item_id, ref in broken:
            print(f"    {item_id} -> {ref}")


if __name__ == "__main__":
    main()
