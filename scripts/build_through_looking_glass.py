#!/usr/bin/env python3
"""
Build grammar.json for Through the Looking-Glass by Lewis Carroll.

Parses the Project Gutenberg text, strips header/footer, extracts chapters,
splits into scenes/passages (L1), creates chapter-level items (L2),
thematic groupings (L2), and meta-categories (L3).
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
SEED_FILE = PROJECT_DIR / "seeds" / "through-the-looking-glass.txt"
OUTPUT_DIR = PROJECT_DIR / "grammars" / "through-the-looking-glass"
OUTPUT_FILE = OUTPUT_DIR / "grammar.json"


def strip_gutenberg(text):
    """Remove Project Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        start_idx = text.index("\n", start_idx) + 1
    else:
        start_idx = 0

    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = len(text)

    return text[start_idx:end_idx].strip()


def extract_chapters(text):
    """Split text into chapters using CHAPTER markers."""
    # Pattern matches "CHAPTER I." or "CHAPTER II." etc.
    chapter_pattern = re.compile(r'\n(CHAPTER\s+[IVXLC]+\.)\n(.+?)(?=\nCHAPTER\s+[IVXLC]+\.\n|\nTHE END\n|$)', re.DOTALL)

    chapters = []
    for match in chapter_pattern.finditer(text):
        header = match.group(1).strip()
        body = match.group(2).strip()

        # Extract chapter number
        num_match = re.search(r'CHAPTER\s+([IVXLC]+)', header)
        roman = num_match.group(1) if num_match else ""

        # First line of body is the title
        lines = body.split("\n", 1)
        title = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""

        chapters.append({
            "roman": roman,
            "title": title,
            "content": content,
        })

    return chapters


def roman_to_int(roman):
    """Convert Roman numeral to integer."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    for i, c in enumerate(roman):
        if i + 1 < len(roman) and values.get(c, 0) < values.get(roman[i + 1], 0):
            result -= values.get(c, 0)
        else:
            result += values.get(c, 0)
    return result


def normalize_quotes(text):
    """Normalize smart/curly quotes to straight quotes."""
    text = text.replace('\u2018', "'")  # left single quote
    text = text.replace('\u2019', "'")  # right single quote
    text = text.replace('\u201C', '"')  # left double quote
    text = text.replace('\u201D', '"')  # right double quote
    text = text.replace('\u2014', '--')  # em dash
    text = text.replace('\u2013', '-')   # en dash
    return text


def clean_text(text):
    """Clean up text: remove illustration markers, normalize whitespace."""
    # Normalize smart quotes
    text = normalize_quotes(text)
    # Remove [Illustration...] markers
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    # Remove asterisk dividers
    text = re.sub(r'\n\s*\*\s+\*\s+\*[\s\*]+\n', '\n\n---\n\n', text)
    # Normalize multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def split_into_scenes(chapter_num, title, content):
    """Split a chapter into meaningful scenes/passages."""
    scenes = []

    # Chapter-specific scene splits based on content analysis
    scene_defs = get_scene_definitions(chapter_num, title)

    if scene_defs:
        for scene_def in scene_defs:
            scene_text = extract_scene_text(content, scene_def["start"], scene_def.get("end"))
            if scene_text and len(scene_text.strip()) > 50:
                scenes.append({
                    "name": scene_def["name"],
                    "text": clean_text(scene_text),
                    "keywords": scene_def["keywords"],
                    "reflection": scene_def["reflection"],
                })

    return scenes


def extract_scene_text(content, start_phrase, end_phrase=None):
    """Extract text between two phrases."""
    start_idx = 0
    if start_phrase:
        idx = content.find(start_phrase)
        if idx == -1:
            # Try case-insensitive
            lower = content.lower()
            idx = lower.find(start_phrase.lower())
        if idx != -1:
            start_idx = idx
        else:
            return ""

    end_idx = len(content)
    if end_phrase:
        idx = content.find(end_phrase, start_idx + 1)
        if idx == -1:
            lower = content.lower()
            idx = lower.find(end_phrase.lower(), start_idx + 1)
        if idx != -1:
            end_idx = idx

    return content[start_idx:end_idx].strip()


def get_scene_definitions(chapter_num, title):
    """Define scene boundaries for each chapter."""

    defs = {
        1: [
            {
                "name": "Alice and the Kittens",
                "start": "One thing was certain",
                "end": "Kitty, can you play chess",
                "keywords": ["kittens", "home", "play", "winter", "imagination"],
                "reflection": "How does play with animals open doorways to imagination? What games of pretend have shaped your own inner world?",
            },
            {
                "name": "Let's Pretend",
                "start": "Kitty, can you play chess",
                "end": "In another moment Alice was through the glass",
                "keywords": ["pretend", "chess", "mirror", "imagination", "crossing"],
                "reflection": "What would it mean to step through a mirror into a world where everything is reversed? Where in your life have you crossed a threshold into the unknown?",
            },
            {
                "name": "Through the Glass",
                "start": "In another moment Alice was through the glass",
                "end": "Here are the Red King and the Red Queen",
                "keywords": ["mirror", "reflection", "reversal", "wonder", "crossing"],
                "reflection": "The Looking-glass room looks the same but is subtly different. When have familiar things suddenly seemed strange to you?",
            },
            {
                "name": "The Living Chess Pieces",
                "start": "Here are the Red King and the Red Queen",
                "end": "This was the poem that Alice read",
                "keywords": ["chess", "invisible", "power", "writing", "agency"],
                "reflection": "Alice is invisible to the chess pieces and can move them at will. What does it feel like to have power over others who don't know you're there?",
            },
            {
                "name": "Jabberwocky",
                "start": "This was the poem that Alice read",
                "end": "She was out of the room in a moment",
                "keywords": ["nonsense", "poetry", "language", "invention", "courage"],
                "reflection": "Jabberwocky makes us feel meaning even when the words are invented. How can something you don't fully understand still move you deeply?",
            },
        ],
        2: [
            {
                "name": "The Contrary Path",
                "start": "I should see the garden far better",
                "end": "O Tiger-lily",
                "keywords": ["path", "logic", "reversal", "frustration", "persistence"],
                "reflection": "In Looking-glass land, walking toward something takes you away from it. Where in your life has the direct approach failed, and the indirect path succeeded?",
            },
            {
                "name": "The Garden of Live Flowers",
                "start": "O Tiger-lily",
                "end": "I think I'll go and meet her",
                "keywords": ["flowers", "talking", "criticism", "perspective", "nature"],
                "reflection": "The flowers judge Alice by their own standards. When have you been judged by rules that weren't your own? How did you respond?",
            },
            {
                "name": "Meeting the Red Queen",
                "start": "I think I'll go and meet her",
                "end": "it takes all the running",
                "keywords": ["queen", "authority", "rules", "chess", "backwards"],
                "reflection": "To reach the Red Queen, Alice must walk away from her. What truths in your life have you found only by letting go of pursuing them directly?",
            },
            {
                "name": "Running to Stay in Place",
                "start": "it takes all the running",
                "end": "she was a Pawn, and that it would soon be time",
                "keywords": ["running", "effort", "progress", "exhaustion", "wisdom"],
                "reflection": "'It takes all the running you can do, to keep in the same place.' Where in your life does this feel true? What would it mean to run twice as fast?",
            },
        ],
        3: [
            {
                "name": "The Railway Carriage",
                "start": "Of course the first thing to do",
                "end": "she found herself sitting quietly under a tree",
                "keywords": ["train", "tickets", "absurdity", "rules", "chorus", "journey"],
                "reflection": "Everyone on the train speaks in chorus and demands tickets Alice doesn't have. When have you felt out of place in a system everyone else seems to understand?",
            },
            {
                "name": "Looking-Glass Insects",
                "start": "she found herself sitting quietly under a tree",
                "end": "She very soon came to an open field",
                "keywords": ["insects", "names", "wordplay", "puns", "fragility", "humor"],
                "reflection": "The Looking-glass insects are made of impossible things and cannot survive. What beautiful but fragile things in your world deserve tender attention?",
            },
            {
                "name": "The Wood Where Things Have No Names",
                "start": "She very soon came to an open field",
                "end": "she came upon two fat little men",
                "keywords": ["identity", "names", "forgetting", "friendship", "fear", "fawn"],
                "reflection": "When Alice and the Fawn forget their names, they walk together without fear. What separations might dissolve if we could forget our labels?",
            },
        ],
        4: [
            {
                "name": "Meeting the Twins",
                "start": "They were standing under a tree",
                "end": "The Walrus and the Carpenter",
                "keywords": ["twins", "logic", "contrariwise", "dance", "manners"],
                "reflection": "Tweedledum and Tweedledee are identical yet insist on being different. What does it mean to define yourself against someone who is just like you?",
            },
            {
                "name": "The Walrus and the Carpenter",
                "start": "The sun was shining on the sea",
                "end": "I like the Walrus best",
                "keywords": ["oysters", "deception", "sympathy", "cruelty", "poetry", "moral"],
                "reflection": "Alice tries to decide who is worse -- the Walrus who weeps while eating, or the Carpenter who eats without pretense. Is false sympathy better or worse than honest indifference?",
            },
            {
                "name": "The Red King's Dream",
                "start": "It's only the Red King snoring",
                "end": "I know they're talking nonsense",
                "keywords": ["dream", "reality", "existence", "philosophy", "tears"],
                "reflection": "If you are only a figure in someone else's dream, are your tears real? What makes you certain you exist?",
            },
            {
                "name": "The Battle of the Brothers",
                "start": "I know they're talking nonsense",
                "end": "CHAPTER V",
                "keywords": ["battle", "rattle", "anger", "brothers", "crow", "conflict"],
                "reflection": "The twins prepare for war over a broken rattle. What trivial things have you fought over that seemed monumental at the time?",
            },
        ],
        5: [
            {
                "name": "The White Queen's Shawl",
                "start": "She caught the shawl",
                "end": "Living backwards",
                "keywords": ["queen", "untidy", "help", "kindness", "jam", "rules"],
                "reflection": "The White Queen offers jam yesterday and jam tomorrow, but never jam today. Where in your life is satisfaction always just out of reach?",
            },
            {
                "name": "Living Backwards",
                "start": "Living backwards",
                "end": "By this time it was getting light",
                "keywords": ["time", "backwards", "memory", "impossible", "belief", "future"],
                "reflection": "'I've believed as many as six impossible things before breakfast.' What impossible things might you practice believing? How would that change your day?",
            },
            {
                "name": "The Sheep's Shop",
                "start": "Oh, much better!",
                "end": "Can you row?",
                "keywords": ["shop", "sheep", "knitting", "elusive", "perception", "transformation"],
                "reflection": "Everything in the shop moves to a different shelf when Alice looks directly at it. What in your life seems to slip away the moment you try to grasp it?",
            },
            {
                "name": "Rowing and Rushes",
                "start": "Can you row?",
                "end": "CHAPTER VI",
                "keywords": ["river", "rowing", "rushes", "beauty", "fading", "impermanence"],
                "reflection": "The dream-rushes melt away the moment Alice picks them. What beautiful moments have you tried to hold onto, only to watch them fade?",
            },
        ],
        6: [
            {
                "name": "Meeting Humpty Dumpty",
                "start": "However, the egg only got larger",
                "end": "Must a name mean something",
                "keywords": ["egg", "wall", "pride", "nursery-rhyme", "fragility"],
                "reflection": "Humpty Dumpty sits precariously on a wall, certain he cannot fall. Where does your own confidence rest on a fragile perch?",
            },
            {
                "name": "The Meaning of Words",
                "start": "Must a name mean something",
                "end": "You seem very clever at explaining words",
                "keywords": ["language", "meaning", "power", "words", "mastery", "portmanteau"],
                "reflection": "'When I use a word, it means just what I choose it to mean.' Who gets to decide what words mean? Is language a democracy or a dictatorship?",
            },
            {
                "name": "Explaining Jabberwocky",
                "start": "You seem very clever at explaining words",
                "end": "The piece I'm going to repeat",
                "keywords": ["jabberwocky", "explanation", "nonsense", "definitions", "imagination"],
                "reflection": "Humpty Dumpty explains Jabberwocky with perfect confidence. Does explaining a mystery enhance it or diminish it?",
            },
            {
                "name": "Humpty Dumpty's Song and Fall",
                "start": "The piece I'm going to repeat",
                "end": "CHAPTER VII",
                "keywords": ["song", "fish", "fall", "crash", "ending", "farewell"],
                "reflection": "Humpty Dumpty's great fall shakes the whole forest. How do the falls of the proud ripple outward and affect everyone around them?",
            },
        ],
        7: [
            {
                "name": "The King's Men",
                "start": "The next moment soldiers came running",
                "end": "I see nobody on the road",
                "keywords": ["soldiers", "king", "messenger", "confusion", "army"],
                "reflection": "The soldiers stumble and fall over each other in their rush. When has organized effort dissolved into comical chaos around you?",
            },
            {
                "name": "Seeing Nobody",
                "start": "I see nobody on the road",
                "end": "Who did you pass on the road",
                "keywords": ["nobody", "wordplay", "literal", "language", "misunderstanding"],
                "reflection": "The King takes 'nobody' literally -- as a person. How often do miscommunications arise from taking words at face value?",
            },
            {
                "name": "The Lion and the Unicorn",
                "start": "Who did you pass on the road",
                "end": "CHAPTER VIII",
                "keywords": ["lion", "unicorn", "battle", "crown", "belief", "fabulous", "cake"],
                "reflection": "The Unicorn says 'If you'll believe in me, I'll believe in you.' What mutual acts of belief sustain your most important relationships?",
            },
        ],
        8: [
            {
                "name": "The Battle of the Knights",
                "start": "After a while the noise seemed gradually",
                "end": "So you will, when you've crossed the next brook",
                "keywords": ["knights", "battle", "rescue", "chess", "prisoner", "queen"],
                "reflection": "Alice doesn't want to be anyone's prisoner -- she wants to be a Queen. When have you refused to be defined by others' claims on you?",
            },
            {
                "name": "The White Knight's Inventions",
                "start": "So you will, when you've crossed the next brook",
                "end": "let me sing you a song to comfort you",
                "keywords": ["inventions", "creativity", "absurdity", "kindness", "impractical", "imagination"],
                "reflection": "The White Knight's inventions never quite work, but he never stops inventing. What is the value of creative effort that doesn't succeed in practical terms?",
            },
            {
                "name": "The Aged Aged Man",
                "start": "let me sing you a song to comfort you",
                "end": "I hope it encouraged him",
                "keywords": ["song", "memory", "farewell", "tenderness", "nostalgia", "beauty"],
                "reflection": "This is the scene Alice remembers most clearly of all her journey. What moments from your own life are etched most vividly in memory, and why?",
            },
            {
                "name": "Becoming a Queen",
                "start": "I hope it encouraged him",
                "end": "CHAPTER IX",
                "keywords": ["crown", "queen", "achievement", "transformation", "brook", "crossing"],
                "reflection": "Alice crosses the last brook and finds a golden crown on her head. What transformations in your life arrived so quietly you almost didn't notice?",
            },
        ],
        9: [
            {
                "name": "Queen Alice's Examination",
                "start": "Well, this _is_ grand!",
                "end": "She can't do sums a _bit_!",
                "keywords": ["queen", "examination", "logic", "absurdity", "authority", "riddles"],
                "reflection": "The Queens test Alice with impossible questions. When have you been tested by standards that made no sense? How did you hold your ground?",
            },
            {
                "name": "The Dinner Party",
                "start": "Can _you_ do sums?",
                "end": "I can't stand this any longer!",
                "keywords": ["feast", "chaos", "mutton", "pudding", "etiquette", "rebellion"],
                "reflection": "Alice is introduced to her dinner and told she can't eat anyone she's been introduced to. What social rules have you encountered that defeated their own purpose?",
            },
            {
                "name": "Alice Seizes the Tablecloth",
                "start": "I can't stand this any longer!",
                "end": "CHAPTER X",
                "keywords": ["rebellion", "power", "chaos", "agency", "shaking", "ending"],
                "reflection": "Alice finally takes control, pulling the tablecloth and toppling everything. When have you reached the point of 'I can't stand this any longer' -- and what happened when you acted?",
            },
        ],
        10: [
            {
                "name": "Shaking",
                "start": "She took her off the table",
                "end": "",
                "keywords": ["shaking", "transformation", "ending", "dream", "kitten"],
                "reflection": "The Red Queen shrinks and softens into a kitten. How do the terrifying figures of our lives sometimes reveal themselves as small and harmless?",
            },
        ],
        11: [
            {
                "name": "Waking",
                "start": "and it really _was_ a kitten",
                "end": "",
                "keywords": ["waking", "kitten", "dream", "reality", "return"],
                "reflection": "The entire adventure collapses into the simple reality of a kitten. What grand experiences in your life have dissolved back into the everyday?",
            },
        ],
        12: [
            {
                "name": "Which Dreamed It?",
                "start": "Your majesty shouldn't purr so loud",
                "end": "Life, what is it but a dream?",
                "keywords": ["dream", "reality", "philosophy", "question", "wonder", "identity"],
                "reflection": "'Was it the Red King, Kitty?' The question of who is dreaming whom is never answered. What if the deepest questions in life are meant to remain open?",
            },
        ],
    }

    return defs.get(chapter_num, [])


def build_l1_items(chapters):
    """Build Level 1 items: individual scenes within chapters."""
    items = []
    sort_order = 0
    scene_ids_by_chapter = {}

    for chapter in chapters:
        ch_num = roman_to_int(chapter["roman"])
        content = chapter["content"]
        scenes = split_into_scenes(ch_num, chapter["title"], content)

        chapter_scene_ids = []

        for scene in scenes:
            scene_id = f"ch{ch_num}-{slugify(scene['name'])}"

            item = {
                "id": scene_id,
                "name": scene["name"],
                "sort_order": sort_order,
                "level": 1,
                "category": f"chapter-{ch_num}",
                "sections": {
                    "Story": scene["text"],
                    "Reflection": scene["reflection"],
                },
                "keywords": scene["keywords"],
                "metadata": {
                    "source": "Through the Looking-Glass, Lewis Carroll, 1871",
                    "chapter": f"Chapter {chapter['roman']}. {chapter['title']}",
                },
            }
            items.append(item)
            chapter_scene_ids.append(scene_id)
            sort_order += 1

        scene_ids_by_chapter[ch_num] = chapter_scene_ids

    return items, sort_order, scene_ids_by_chapter


def slugify(name):
    """Convert name to lowercase hyphenated slug."""
    s = name.lower()
    s = re.sub(r"[''']", "", s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s


def build_l2_chapter_items(chapters, scene_ids_by_chapter, sort_order):
    """Build Level 2 items: one per chapter."""
    items = []
    chapter_item_ids = []

    chapter_descriptions = {
        1: {
            "about": "Alice's journey begins in the warmth of her drawing room, playing with kittens on a winter evening. Through imagination and the magic of the looking-glass, she crosses into a reversed world where chess pieces walk and books read backwards. She discovers Jabberwocky -- the most famous nonsense poem in English.",
            "for_parents": "This chapter is perfect for exploring imagination and the boundary between real and pretend. Ask: 'If you could step through a mirror, what would be different on the other side?' Read the Jabberwocky aloud together -- children love the sounds even before they understand the meanings.",
        },
        2: {
            "about": "Alice enters the garden where flowers talk and criticize, paths lead backwards, and the Red Queen explains the rules of Looking-glass chess. The famous scene of running to stay in place captures one of the book's most enduring philosophical images.",
            "for_parents": "The Red Queen's 'running to stay in place' is a wonderful metaphor to discuss with children. Ask: 'Do you ever feel like you're running but not getting anywhere?' The talking flowers introduce the idea that others see us very differently than we see ourselves.",
        },
        3: {
            "about": "Alice travels by railway through the looking-glass landscape, encounters charming insects made of impossible things (Bread-and-Butterflies, Rocking-horse-flies), and enters the haunting wood where things have no names. Her brief friendship with the Fawn, lost when names return, is one of Carroll's most poignant scenes.",
            "for_parents": "The wood where things have no names is a profound scene for discussing identity. Ask: 'If you forgot your name, would you still be you? Would you be friends with different people?' The Gnat's sadness about its own jokes opens a conversation about humor and empathy.",
        },
        4: {
            "about": "Alice meets Tweedledum and Tweedledee, who recite 'The Walrus and the Carpenter' -- a masterpiece of narrative poetry about deception and sympathy. The twins then confront Alice with the disturbing idea that she exists only in the Red King's dream, before their own petty battle is interrupted by the monstrous crow.",
            "for_parents": "This chapter raises big philosophical questions in child-sized form. After 'The Walrus and the Carpenter,' ask: 'Who was worse -- the one who cried, or the one who didn't?' The Red King's dream scene is perfect for 'How do you know you're real?' conversations.",
        },
        5: {
            "about": "The White Queen lives backwards in time, screaming before she pricks her finger and offering jam yesterday and jam tomorrow but never today. The chapter transforms into the Sheep's shop where everything shifts when you look at it, then into a dreamlike boat ride among melting rushes.",
            "for_parents": "The White Queen's 'six impossible things before breakfast' is a famous encouragement to expand imagination. The fading rushes offer a gentle lesson about impermanence. Ask: 'Have you ever tried to hold onto a beautiful moment and felt it slip away?'",
        },
        6: {
            "about": "Humpty Dumpty, sitting on his wall with magnificent arrogance, delivers Carroll's most celebrated philosophy of language: 'When I use a word, it means just what I choose it to mean.' He explains Jabberwocky, introduces the concept of portmanteau words, and recites his own strange poem before his inevitable great fall.",
            "for_parents": "This chapter is a goldmine for language play. Humpty Dumpty's claim that he can make words mean whatever he wants invites discussion: 'Can you just decide what a word means? Who gets to decide?' Try inventing portmanteau words together as a family game.",
        },
        7: {
            "about": "The Lion and the Unicorn fight for the White King's crown in a scene drawn from the old nursery rhyme. The King's literal interpretation of 'nobody' creates delicious wordplay, and the Unicorn's bargain with Alice -- 'I'll believe in you if you'll believe in me' -- is one of the book's most memorable moments.",
            "for_parents": "The mutual belief bargain between Alice and the Unicorn is a beautiful starting point for discussing how belief and trust work in relationships. The 'nobody' wordplay helps children see how language can trick us when we take it too literally.",
        },
        8: {
            "about": "The White Knight, Carroll's most autobiographical and tender creation, escorts Alice to the edge of queenhood. His absurd inventions, terrible riding, and beautiful farewell song ('The Aged Aged Man') create the book's emotional heart. This is the scene Alice remembers most vividly of all.",
            "for_parents": "Many readers see the White Knight as Carroll himself, saying goodbye to Alice as she grows up. The farewell scene is deeply moving. Ask: 'Why do you think Alice remembered the White Knight most of all?' This chapter explores the beauty of impractical creativity and the tenderness of goodbye.",
        },
        9: {
            "about": "Alice becomes a Queen but finds it's not what she expected. The Red and White Queens quiz her with impossible logic, and a grand dinner party descends into magnificent chaos -- food that talks back, guests who drink from their heads, and a pudding that objects to being sliced. Alice finally rebels, pulling the tablecloth and toppling everything.",
            "for_parents": "The dinner party chaos is pure comic joy for reading aloud. But it also shows Alice finding her voice and taking action. Ask: 'When have you felt like everything around you was going crazy? What did you do?' The examination scene parodies the absurdity of testing.",
        },
        10: {
            "about": "In the shortest chapter, Alice shakes the Red Queen, who shrinks and softens and transforms. The grand, terrifying figure becomes something small and familiar.",
            "for_parents": "This tiny chapter packs a big idea: the things that seem powerful and frightening can turn out to be small and soft when you take hold of them. Ask: 'What scary things in your life turned out to be not so scary when you faced them?'",
        },
        11: {
            "about": "A single sentence: the Red Queen was a kitten all along. The dream ends.",
            "for_parents": "The shortest chapter in the book -- just one line. The magic dissolves into the ordinary. A perfect moment to pause and let the child feel the shift from dream to waking.",
        },
        12: {
            "about": "Alice wakes and interrogates her kittens about who became whom in the dream. The book ends with the unanswered question: 'Which dreamed it?' Was Alice dreaming the Red King, or was the Red King dreaming Alice? Carroll's acrostic poem, spelling ALICE PLEASANCE LIDDELL, closes the book.",
            "for_parents": "The final question -- 'Which dreamed it?' -- is one of the great open questions in children's literature. Don't rush to answer it. Let your child sit with the mystery. The acrostic poem rewards close reading: the first letters of each line spell the real Alice's full name.",
        },
    }

    for chapter in chapters:
        ch_num = roman_to_int(chapter["roman"])
        scene_ids = scene_ids_by_chapter.get(ch_num, [])
        desc = chapter_descriptions.get(ch_num, {"about": "", "for_parents": ""})

        ch_id = f"chapter-{ch_num}"

        item = {
            "id": ch_id,
            "name": f"Chapter {chapter['roman']}. {chapter['title']}",
            "sort_order": sort_order,
            "level": 2,
            "category": "chapters",
            "composite_of": scene_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": desc["about"],
                "For Parents": desc["for_parents"],
            },
            "keywords": [slugify(chapter["title"]), "chapter"],
            "metadata": {
                "source": "Through the Looking-Glass, Lewis Carroll, 1871",
            },
        }
        items.append(item)
        chapter_item_ids.append(ch_id)
        sort_order += 1

    return items, sort_order, chapter_item_ids


def build_l2_thematic_groups(scene_ids_by_chapter, sort_order):
    """Build Level 2 thematic groupings."""
    items = []
    thematic_ids = []

    themes = [
        {
            "id": "theme-language-wordplay",
            "name": "Language and Wordplay",
            "composite_of": [
                "ch1-jabberwocky",
                "ch3-looking-glass-insects",
                "ch6-the-meaning-of-words",
                "ch6-explaining-jabberwocky",
                "ch7-seeing-nobody",
            ],
            "about": "Carroll was a logician, and Through the Looking-Glass is his playground for exploring how language works -- and fails. From the invented words of Jabberwocky to Humpty Dumpty's claim that words mean whatever he says, these scenes probe the foundations of meaning, naming, and communication.",
            "for_parents": "These scenes are wonderful for developing language awareness. Try: invent your own portmanteau words, write nonsense poetry together, or play 'what does this word REALLY mean?' Carroll shows children that language is not fixed -- it is a living, playful, sometimes treacherous thing.",
            "keywords": ["language", "wordplay", "nonsense", "meaning", "puns", "portmanteau"],
        },
        {
            "id": "theme-chess-game",
            "name": "The Chess Game",
            "composite_of": [
                "ch1-the-living-chess-pieces",
                "ch2-meeting-the-red-queen",
                "ch2-running-to-stay-in-place",
                "ch8-the-battle-of-the-knights",
                "ch8-becoming-a-queen",
                "ch9-queen-alices-examination",
            ],
            "about": "The entire book is structured as a chess game, with Alice as a White Pawn advancing square by square to become a Queen. These scenes trace the game's key moves -- encounters with Queens and Knights, the rules of this strange chessboard, and Alice's coronation.",
            "for_parents": "The chess structure gives children a framework for understanding the story's progression. You don't need to know chess to enjoy it, but knowing the basics adds a layer. Ask: 'What does it mean to start as a Pawn and become a Queen? What journey is that like in real life?'",
            "keywords": ["chess", "pawn", "queen", "game", "rules", "strategy"],
        },
        {
            "id": "theme-identity",
            "name": "Identity and Existence",
            "composite_of": [
                "ch3-the-wood-where-things-have-no-names",
                "ch4-the-red-kings-dream",
                "ch6-meeting-humpty-dumpty",
                "ch12-which-dreamed-it",
            ],
            "about": "Who are you when you forget your name? Are you real if someone else is dreaming you? Carroll weaves philosophy through his fantasy, asking questions about identity and existence that philosophers still debate. These scenes explore the slippery nature of the self.",
            "for_parents": "These are some of the most philosophically rich scenes in children's literature. They invite genuine wonder: 'If you forgot your name, would you still be you?' 'How do you know you're not in someone else's dream?' Let children wrestle with these -- there are no wrong answers.",
            "keywords": ["identity", "names", "dream", "reality", "existence", "self"],
        },
        {
            "id": "theme-mirrors-reversal",
            "name": "Mirrors and Reversal",
            "composite_of": [
                "ch1-lets-pretend",
                "ch1-through-the-glass",
                "ch2-the-contrary-path",
                "ch5-living-backwards",
                "ch5-the-sheeps-shop",
                "ch10-shaking",
                "ch11-waking",
            ],
            "about": "The Looking-glass world runs on reversal: walk toward something and you move away; run fast to stay still; remember the future, not the past; scream before you're hurt. These scenes explore Carroll's central metaphor of a world where everything is backwards.",
            "for_parents": "The reversal theme helps children think about perspective and assumptions. Play 'what if everything were backwards?' games: What if you ate dessert first? What if school started with recess? What if you had to walk backwards to go forward? Carroll shows that questioning our assumptions is the beginning of wonder.",
            "keywords": ["mirror", "reversal", "backwards", "reflection", "opposite", "symmetry"],
        },
        {
            "id": "theme-authority-rules",
            "name": "Authority and Absurd Rules",
            "composite_of": [
                "ch2-meeting-the-red-queen",
                "ch3-the-railway-carriage",
                "ch5-the-white-queens-shawl",
                "ch9-queen-alices-examination",
                "ch9-the-dinner-party",
                "ch9-alice-seizes-the-tablecloth",
            ],
            "about": "Queens who make rules that contradict themselves, guards who demand tickets that don't exist, jam that can never be had today -- Carroll gleefully skewers arbitrary authority. Alice's final rebellion, seizing the tablecloth and toppling the feast, is her declaration of independence from nonsensical rule.",
            "for_parents": "These scenes help children think critically about rules and authority. Ask: 'Which rules in the story make sense? Which don't? How can you tell the difference?' Alice's rebellion at the dinner party shows that sometimes the right thing to do is stand up and say 'enough.'",
            "keywords": ["authority", "rules", "queens", "rebellion", "absurdity", "power"],
        },
        {
            "id": "theme-poetry-songs",
            "name": "Poetry and Songs",
            "composite_of": [
                "ch1-jabberwocky",
                "ch4-the-walrus-and-the-carpenter",
                "ch6-humpty-dumptys-song-and-fall",
                "ch8-the-aged-aged-man",
            ],
            "about": "Through the Looking-Glass contains some of the most beloved poems in the English language. Jabberwocky, The Walrus and the Carpenter, and the White Knight's song are masterpieces of nonsense verse that resonate with genuine emotion beneath their absurdity.",
            "for_parents": "Read these poems aloud -- they are meant to be heard. Jabberwocky rewards dramatic reading. The Walrus and the Carpenter invites moral debate. The White Knight's song is genuinely moving. Ask: 'How can something that doesn't quite make sense still make you feel something?'",
            "keywords": ["poetry", "songs", "verse", "jabberwocky", "walrus", "nonsense"],
        },
    ]

    for theme in themes:
        item = {
            "id": theme["id"],
            "name": theme["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "themes",
            "composite_of": theme["composite_of"],
            "relationship_type": "emergence",
            "sections": {
                "About": theme["about"],
                "For Parents": theme["for_parents"],
            },
            "keywords": theme["keywords"],
            "metadata": {
                "source": "Through the Looking-Glass, Lewis Carroll, 1871",
            },
        }
        items.append(item)
        thematic_ids.append(theme["id"])
        sort_order += 1

    return items, sort_order, thematic_ids


def build_l3_items(chapter_item_ids, thematic_ids, sort_order):
    """Build Level 3 meta-category items."""
    items = []

    l3_defs = [
        {
            "id": "meta-narrative-journey",
            "name": "The Narrative Journey",
            "composite_of": chapter_item_ids,
            "about": "Through the Looking-Glass follows Alice's journey across a giant chessboard, from Pawn to Queen, through twelve chapters that mirror the structure of a chess game. Each chapter is a square on the board, each encounter a move. The narrative is simultaneously a children's adventure, a chess problem, a philosophical inquiry, and a love letter from an aging mathematician to a child who is growing up.",
            "keywords": ["narrative", "journey", "chess", "chapters", "structure"],
        },
        {
            "id": "meta-themes-ideas",
            "name": "Themes and Ideas",
            "composite_of": thematic_ids,
            "about": "Beneath its playful surface, Through the Looking-Glass explores themes that have occupied philosophers for centuries: the nature of identity, the relationship between language and meaning, the experience of time, the arbitrariness of authority, and the question of what is real. Carroll approaches these themes through nonsense, paradox, and wordplay -- making them accessible to children while remaining genuinely profound for adults.",
            "keywords": ["themes", "philosophy", "ideas", "language", "identity", "meaning"],
        },
    ]

    for l3 in l3_defs:
        item = {
            "id": l3["id"],
            "name": l3["name"],
            "sort_order": sort_order,
            "level": 3,
            "category": "meta",
            "composite_of": l3["composite_of"],
            "relationship_type": "emergence",
            "sections": {
                "About": l3["about"],
            },
            "keywords": l3["keywords"],
            "metadata": {
                "source": "Through the Looking-Glass, Lewis Carroll, 1871",
            },
        }
        items.append(item)
        sort_order += 1

    return items, sort_order


def build_grammar():
    """Main function to build the grammar."""
    # Read and clean text
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    text = strip_gutenberg(raw_text)
    text = clean_text(text)

    # Extract chapters
    chapters = extract_chapters(text)
    print(f"Found {len(chapters)} chapters")

    for ch in chapters:
        ch_num = roman_to_int(ch["roman"])
        print(f"  Chapter {ch['roman']} ({ch_num}): {ch['title']}")

    # Build items at each level
    l1_items, sort_order, scene_ids_by_chapter = build_l1_items(chapters)
    print(f"Built {len(l1_items)} L1 items (scenes)")

    l2_chapter_items, sort_order, chapter_item_ids = build_l2_chapter_items(
        chapters, scene_ids_by_chapter, sort_order
    )
    print(f"Built {len(l2_chapter_items)} L2 chapter items")

    l2_thematic_items, sort_order, thematic_ids = build_l2_thematic_groups(
        scene_ids_by_chapter, sort_order
    )
    print(f"Built {len(l2_thematic_items)} L2 thematic items")

    l3_items, sort_order = build_l3_items(chapter_item_ids, thematic_ids, sort_order)
    print(f"Built {len(l3_items)} L3 items")

    all_items = l1_items + l2_chapter_items + l2_thematic_items + l3_items
    print(f"Total items: {len(all_items)}")

    # Build the grammar
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Lewis Carroll",
                    "date": "1871",
                    "note": "Original author (Charles Lutwidge Dodgson, 1832-1898)",
                },
                {
                    "name": "Project Gutenberg",
                    "url": "https://www.gutenberg.org/ebooks/12",
                    "date": "2008",
                    "note": "Digital text source, eBook #12",
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure, reflections, and thematic organization",
                },
            ],
        },
        "name": "Through the Looking-Glass",
        "description": "Lewis Carroll's beloved sequel to Alice's Adventures in Wonderland (1871), in which Alice steps through a mirror into a world where everything runs backwards. Structured as a chess game, the story follows Alice from Pawn to Queen through encounters with Tweedledum and Tweedledee, Humpty Dumpty, the White Knight, and the Red Queen. Contains some of the most famous poems in the English language, including Jabberwocky and The Walrus and the Carpenter. Source: Project Gutenberg eBook #12 (https://www.gutenberg.org/ebooks/12).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: John Tenniel's original 1871 illustrations for 'Through the Looking-Glass' (Macmillan) -- the definitive visual companion, featuring detailed wood engravings of Alice, Humpty Dumpty, the Jabberwock, the White Knight, and all major characters. Peter Newell's 1902 illustrations (Harper & Brothers) -- softer, more whimsical pen-and-ink drawings. Arthur Rackham's 1907 illustrations for 'Alice's Adventures in Wonderland' (Heinemann) -- while primarily for the first book, Rackham's style perfectly complements the Looking-Glass world. Blanche McManus's 1899 illustrations -- color plates with Art Nouveau influences.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "alice",
            "carroll",
            "chess",
            "mirror",
            "nonsense",
            "children",
            "fantasy",
            "wordplay",
            "philosophy",
            "victorian",
            "poetry",
        ],
        "cover_image_url": "",
        "roots": ["western-philosophy", "imagination"],
        "shelves": ["children", "wonder"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "dialectical",
        "items": all_items,
    }

    # Write output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"\nGrammar written to {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")


if __name__ == "__main__":
    build_grammar()
