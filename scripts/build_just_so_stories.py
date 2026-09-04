#!/usr/bin/env python3
"""
Build grammar.json for Just So Stories by Rudyard Kipling.

Source: Project Gutenberg eBook #2781
Structure: 12 stories, each with an accompanying poem
Levels:
  L1: Individual stories (story text + poem)
  L2: Thematic groups (by subject, by theme)
  L3: Meta-categories
"""

import json
import re
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "seeds" / "just-so-stories.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "just-so-stories"
OUTPUT_FILE = OUTPUT_DIR / "grammar.json"

# Story titles in order as they appear
STORIES = [
    {
        "title_pattern": "HOW THE WHALE GOT HIS THROAT",
        "id": "how-the-whale-got-his-throat",
        "name": "How the Whale Got His Throat",
        "keywords": ["whale", "mariner", "stute-fish", "throat", "grating", "sea"],
        "summary": "A Whale eats all the fish in the sea until only one small 'Stute Fish is left. The 'Stute Fish directs the Whale to a shipwrecked Mariner, who dances and prances inside the Whale's belly until the Whale agrees to take him home. The clever Mariner wedges a grating in the Whale's throat, so he can never again swallow anything larger than a fish.",
        "reflection": "The little 'Stute Fish outsmarted the biggest creature in the sea. When have you seen someone small solve a problem that someone big could not?",
    },
    {
        "title_pattern": "HOW THE CAMEL GOT HIS HUMP",
        "id": "how-the-camel-got-his-hump",
        "name": "How the Camel Got His Hump",
        "keywords": ["camel", "hump", "laziness", "work", "djinn", "desert"],
        "summary": "In the beginning of years, the Camel lives in the desert and refuses to work, answering every request with 'Humph!' The Horse, Dog, and Ox complain to the Djinn of All Deserts, who gives the Camel a great big humph (hump) on his back so he can work three days without eating -- to make up for the three days he missed.",
        "reflection": "The Camel's laziness gave him his hump. What habits do you have that might be shaping you, for better or worse? Is there ever a good reason to say 'Humph'?",
    },
    {
        "title_pattern": "HOW THE RHINOCEROS GOT HIS SKIN",
        "id": "how-the-rhinoceros-got-his-skin",
        "name": "How the Rhinoceros Got His Skin",
        "keywords": ["rhinoceros", "parsee", "cake", "skin", "wrinkles", "red-sea"],
        "summary": "A Parsee bakes a cake on an uninhabited island. A Rhinoceros with smooth, tight skin steals and eats it. The Parsee takes revenge: when the Rhinoceros removes his skin to bathe, the Parsee fills it with stale cake crumbs. The Rhinoceros puts it back on, and the itching and scratching turn his smooth skin into the wrinkled, baggy thing it is today.",
        "reflection": "The Parsee got his revenge in a very creative way. Is revenge ever a good idea? What's the difference between getting even and standing up for yourself?",
    },
    {
        "title_pattern": "HOW THE LEOPARD GOT HIS SPOTS",
        "id": "how-the-leopard-got-his-spots",
        "name": "How the Leopard Got His Spots",
        "keywords": ["leopard", "ethiopian", "spots", "camouflage", "hunting", "change"],
        "summary": "The Leopard and the Ethiopian hunt in the bare, sandy High Veldt where the Giraffe, Zebra, and other animals are easy to see. But the animals move to a shadowy forest and develop stripes and spots to hide. A wise Baboon tells the hunters to 'go into other spots.' The Ethiopian changes his skin to black, and paints spots on the Leopard with his fingertips.",
        "reflection": "The animals changed to fit their new home. When have you had to change to fit into a new situation? Did it change who you really are inside?",
    },
    {
        "title_pattern": "THE ELEPHANT'S CHILD",
        "id": "the-elephants-child",
        "name": "The Elephant's Child",
        "keywords": ["elephant", "trunk", "crocodile", "curiosity", "limpopo", "spanking"],
        "summary": "In the High and Far-Off Times, the Elephant had no trunk, just a blackish, bulgy nose. The Elephant's Child, full of 'satiable curiosity, goes to the banks of the great grey-green, greasy Limpopo River to ask the Crocodile what he has for dinner. The Crocodile seizes his nose and pulls and pulls, stretching it into the trunk that all elephants have today. The Elephant's Child discovers the trunk is wonderfully useful.",
        "reflection": "The Elephant's Child was punished for being curious, but his curiosity gave elephants their most useful feature. When has your curiosity gotten you into trouble -- and turned out to be a gift?",
    },
    {
        "title_pattern": "THE SING-SONG OF OLD MAN KANGAROO",
        "id": "the-sing-song-of-old-man-kangaroo",
        "name": "The Sing-Song of Old Man Kangaroo",
        "keywords": ["kangaroo", "running", "dingo", "legs", "ngarrong", "chase"],
        "summary": "Old Man Kangaroo wants to be different from all other animals. He asks Nqong (who sits on the Doorsill of the Doorways of the Beginning) to make him popular and run after by five o'clock in the afternoon. Nqong sets Yellow-Dog Dingo to chase him across Australia. The running stretches his hind legs long and strong -- and he's been running from Dingo ever since.",
        "reflection": "Old Man Kangaroo wanted to be special, and he got his wish -- but not the way he expected. Have you ever wished for something and gotten it in a surprising way?",
    },
    {
        "title_pattern": "THE BEGINNING OF THE ARMADILLOS",
        "id": "the-beginning-of-the-armadillos",
        "name": "The Beginning of the Armadillos",
        "keywords": ["armadillo", "hedgehog", "tortoise", "jaguar", "confusion", "amazon"],
        "summary": "A young Painted Jaguar is confused by a clever Stickly-Prickly Hedgehog and Slow-Solid Tortoise, who keep giving him contradictory advice about which one curls up and which one swims. Over time, the Hedgehog learns to swim and the Tortoise learns to curl up, and they both develop overlapping scaly armor -- becoming the first Armadillos.",
        "reflection": "The Hedgehog and the Tortoise each learned from the other and became something new. When have you learned something from a friend that changed you?",
    },
    {
        "title_pattern": "HOW THE FIRST LETTER WAS WRITTEN",
        "id": "how-the-first-letter-was-written",
        "name": "How the First Letter Was Written",
        "keywords": ["letter", "writing", "tegumai", "taffy", "communication", "misunderstanding"],
        "summary": "Tegumai Bopsulai and his daughter Taffy are fishing when his spear breaks. Taffy draws a picture-message on birch bark and sends it with a Stranger to her mother. But the picture is wildly misinterpreted -- the Stranger is attacked and Tegumai is 'rescued' from a danger that doesn't exist. The hilarious misunderstanding shows why picture-writing needed to become real writing.",
        "reflection": "Taffy's message caused chaos because pictures can mean different things to different people. When has a message you sent been misunderstood? What makes communication work?",
    },
    {
        "title_pattern": "HOW THE ALPHABET WAS MADE",
        "id": "how-the-alphabet-was-made",
        "name": "How the Alphabet Was Made",
        "keywords": ["alphabet", "letters", "tegumai", "taffy", "language", "invention", "sounds"],
        "summary": "After the picture-writing disaster, Tegumai and Taffy invent the alphabet. They notice that mouth-shapes for different sounds look like different things -- S like a snake, O like an egg, A like a carp-mouth. Sound by sound, they build a system where marks represent noises instead of pictures. The story celebrates the miracle of writing.",
        "reflection": "Tegumai and Taffy invented letters by looking at how mouths move when making sounds. What everyday miracle do you take for granted? What would life be like without writing?",
    },
    {
        "title_pattern": "THE CRAB THAT PLAYED WITH THE SEA",
        "id": "the-crab-that-played-with-the-sea",
        "name": "The Crab That Played with the Sea",
        "keywords": ["crab", "sea", "tides", "eldest-magician", "pau-amma", "creation", "moon"],
        "summary": "In the very beginning, the Eldest Magician sets the Animals to play their Play. The great crab Pau Amma disobeys and plays by himself in the deep sea, making the tides rise and fall as he breathes. The Eldest Magician sends the Man to catch Pau Amma. The Moon is given power over the tides, and Pau Amma is allowed to come ashore once in his life -- which is why crabs run in and out of the sea.",
        "reflection": "Pau Amma wanted to play by his own rules instead of following the Eldest Magician's plan. When is it right to go your own way, and when does it cause trouble for everyone?",
    },
    {
        "title_pattern": "THE CAT THAT WALKED BY HIMSELF",
        "id": "the-cat-that-walked-by-himself",
        "name": "The Cat That Walked by Himself",
        "keywords": ["cat", "dog", "horse", "cow", "woman", "independence", "wildness", "domestication"],
        "summary": "In the Wet Wild Woods, the Woman domesticates the animals one by one: the Dog for protection, the Horse for riding, the Cow for milk. But the Cat negotiates his own terms -- he will catch mice and be kind to babies, but he will never be truly tamed. 'I am the Cat who walks by himself, and all places are alike to me.' He keeps his bargain, but the Dog is allowed to chase him and the Man is allowed to throw things at him whenever he forgets.",
        "reflection": "The Cat chose freedom over comfort. The Dog chose belonging over independence. Which would you choose? Is it possible to have both?",
    },
    {
        "title_pattern": "THE BUTTERFLY THAT STAMPED",
        "id": "the-butterfly-that-stamped",
        "name": "The Butterfly That Stamped",
        "keywords": ["butterfly", "solomon", "balkis", "wives", "stamp", "wisdom", "humility"],
        "summary": "King Solomon, the wisest of men, is pestered by his 999 quarrelling wives. A Butterfly boasts to his wife that he has only to stamp his foot and Solomon's palace will disappear. Queen Balkis overhears and conspires with Solomon: when the Butterfly stamps, Solomon makes the palace vanish (using his ring). The trick humbles the quarrelling wives. Balkis shows Solomon that even a butterfly's boast can be useful -- and that the wisest husband is the one who listens to his wife.",
        "reflection": "The Butterfly's boast was empty, but it was used wisely. When has something small or silly turned out to be exactly what was needed?",
    },
]


def read_and_strip_gutenberg(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK JUST SO STORIES ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK JUST SO STORIES ***"
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def normalize_apostrophes(text):
    """Replace curly apostrophes with straight ones."""
    return text.replace('\u2019', "'").replace('\u2018', "'")


def extract_stories(text):
    """Extract each story by finding its title boundary and the next story's title."""
    # Normalize apostrophes in the text for matching
    text = normalize_apostrophes(text)
    story_texts = {}

    titles = [s["title_pattern"] for s in STORIES]
    # Build a regex that matches any of the story titles as a line
    # Find positions of each title
    positions = []
    for title in titles:
        # Match the title on its own line (not indented = actual story, not TOC)
        pattern = re.compile(r'^' + re.escape(title) + r'\s*$', re.MULTILINE)
        matches = list(pattern.finditer(text))
        if matches:
            # Use the last non-indented match (the actual story heading, not TOC)
            positions.append((title, matches[-1].start()))
        else:
            print(f"  WARNING: Could not find title: {title}")

    positions.sort(key=lambda x: x[1])

    for i, (title, start) in enumerate(positions):
        end = positions[i + 1][1] if i + 1 < len(positions) else len(text)
        story_text = text[start:end].strip()
        # Remove the title line itself
        lines = story_text.split('\n')
        # Skip title line
        content_start = 0
        for j, line in enumerate(lines):
            if line.strip() == title:
                content_start = j + 1
                break
        content = '\n'.join(lines[content_start:]).strip()
        # Remove excessive whitespace
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        story_texts[title] = content

    return story_texts


def build_grammar():
    text = read_and_strip_gutenberg(SEED_FILE)
    story_texts = extract_stories(text)

    items = []
    sort_order = 0
    story_ids = []

    # === L1: Stories ===
    for story_def in STORIES:
        sort_order += 1
        raw_text = story_texts.get(story_def["title_pattern"], "")
        if not raw_text:
            print(f"  WARNING: No text found for {story_def['title_pattern']}")
            continue

        story_ids.append(story_def["id"])

        items.append({
            "id": story_def["id"],
            "name": story_def["name"],
            "sort_order": sort_order,
            "category": "story",
            "level": 1,
            "sections": {
                "Story": raw_text,
                "About": story_def["summary"],
                "Reflection": story_def["reflection"],
            },
            "keywords": story_def["keywords"],
            "metadata": {},
        })

    # === L2: Thematic Groups ===

    # Animal Origin Stories
    animal_stories = [
        "how-the-whale-got-his-throat",
        "how-the-camel-got-his-hump",
        "how-the-rhinoceros-got-his-skin",
        "how-the-leopard-got-his-spots",
        "the-elephants-child",
        "the-sing-song-of-old-man-kangaroo",
        "the-beginning-of-the-armadillos",
    ]
    sort_order += 1
    items.append({
        "id": "group-animal-origins",
        "name": "How Animals Got Their Features",
        "sort_order": sort_order,
        "category": "thematic-group",
        "level": 2,
        "relationship_type": "emergence",
        "composite_of": animal_stories,
        "sections": {
            "About": "Seven stories explaining how animals came to look and behave the way they do: the Whale's throat-grating, the Camel's hump, the Rhinoceros's wrinkly skin, the Leopard's spots, the Elephant's trunk, the Kangaroo's long legs, and the Armadillo's armor. These are Kipling's version of origin myths -- pourquoi tales that answer 'Why?' with humor, imagination, and rhythmic prose.",
            "For Parents": "These seven stories form the heart of the collection. Children love the 'why?' format -- it mirrors their own endless questions about the natural world. Each story rewards reading aloud: the rolling rhythms, the coined words ('satiable curiosity'), and the ritual phrases ('O Best Beloved') are designed to be heard, not just read. Great for sparking nature observations: 'Why do you think elephants really have trunks?'",
        },
        "keywords": ["animals", "origins", "pourquoi", "nature", "explanation"],
        "metadata": {},
    })

    # Human Invention Stories
    human_stories = [
        "how-the-first-letter-was-written",
        "how-the-alphabet-was-made",
    ]
    sort_order += 1
    items.append({
        "id": "group-human-inventions",
        "name": "The Invention of Writing",
        "sort_order": sort_order,
        "category": "thematic-group",
        "level": 2,
        "relationship_type": "emergence",
        "composite_of": human_stories,
        "sections": {
            "About": "Two companion stories about Tegumai and his daughter Taffy inventing written communication. The first letter (a picture) causes hilarious misunderstanding. The alphabet (sound-symbols) solves the problem. Together they celebrate the miracle of writing and the ingenuity of a father-daughter team working out one of humanity's greatest inventions.",
            "For Parents": "These two stories are best read together, as the second directly solves the problem revealed by the first. They're wonderful for children who are learning to read and write -- making the abstract miracle of literacy into a concrete, funny story. Try having your child invent their own symbols for sounds after reading these.",
        },
        "keywords": ["writing", "alphabet", "communication", "invention", "tegumai", "taffy"],
        "metadata": {},
    })

    # Cosmic/Mythic Stories
    cosmic_stories = [
        "the-crab-that-played-with-the-sea",
        "the-cat-that-walked-by-himself",
        "the-butterfly-that-stamped",
    ]
    sort_order += 1
    items.append({
        "id": "group-cosmic-tales",
        "name": "Cosmic Tales",
        "sort_order": sort_order,
        "category": "thematic-group",
        "level": 2,
        "relationship_type": "emergence",
        "composite_of": cosmic_stories,
        "sections": {
            "About": "Three stories that operate on a larger scale than the animal tales. The Crab explains the tides through a creation myth. The Cat explores the ancient contract between wildness and domestication. The Butterfly uses Solomon's wisdom to explore the paradox that even empty boasts can serve a purpose. These are the collection's most philosophical stories.",
            "For Parents": "The Cat That Walked by Himself is the jewel of this group -- and possibly the whole collection. Its exploration of independence versus belonging resonates with every child (and adult) who has struggled with the tension between freedom and community. The ending is ambiguous and rich. The Butterfly That Stamped has surprising depth about wisdom, marriage, and humility.",
        },
        "keywords": ["mythology", "creation", "independence", "wisdom", "philosophy"],
        "metadata": {},
    })

    # Theme: Curiosity and Consequence
    curiosity_stories = [
        "the-elephants-child",
        "how-the-whale-got-his-throat",
        "how-the-first-letter-was-written",
        "the-crab-that-played-with-the-sea",
    ]
    sort_order += 1
    items.append({
        "id": "theme-curiosity-and-consequence",
        "name": "Curiosity and Consequence",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "relationship_type": "emergence",
        "composite_of": curiosity_stories,
        "sections": {
            "About": "Stories where curiosity, cleverness, or disobedience leads to permanent change. The Elephant's Child asks one question too many and gets a trunk. The Mariner's resourcefulness gives the Whale a grating. Taffy's picture-letter causes chaos. Pau Amma's rebellious play shapes the tides. In Kipling's world, every action leaves a permanent mark on the world.",
            "For Parents": "Kipling celebrates curiosity even as he shows its dangers. The Elephant's Child is spanked by every relative for asking questions -- but his curiosity gives elephants their most useful feature. This is a wonderful theme for encouraging children's questions while talking honestly about the consequences of impulsive action.",
        },
        "keywords": ["curiosity", "consequence", "change", "questions", "action"],
        "metadata": {},
    })

    # Theme: Laziness and Trickery
    laziness_stories = [
        "how-the-camel-got-his-hump",
        "how-the-rhinoceros-got-his-skin",
        "the-sing-song-of-old-man-kangaroo",
        "the-beginning-of-the-armadillos",
    ]
    sort_order += 1
    items.append({
        "id": "theme-laziness-and-trickery",
        "name": "Laziness, Vanity, and Trickery",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "relationship_type": "emergence",
        "composite_of": laziness_stories,
        "sections": {
            "About": "Stories where character flaws -- laziness, greed, vanity -- lead to transformation. The Camel's refusal to work earns him a hump. The Rhinoceros's rudeness earns him wrinkly skin. Old Man Kangaroo's vanity sets a Dingo on his tail forever. The Hedgehog and Tortoise's trickery confuses a Jaguar and creates a new creature entirely.",
            "For Parents": "These stories are moral fables dressed in comedy. The consequences in Kipling's world are permanent but often funny rather than cruel -- the Camel can now work three days without eating, the Armadillo is a marvel of adaptation. Great for conversations about how our habits and choices shape who we become -- literally, in these stories.",
        },
        "keywords": ["laziness", "vanity", "trickery", "consequences", "transformation"],
        "metadata": {},
    })

    # Theme: Independence and Belonging
    independence_stories = [
        "the-cat-that-walked-by-himself",
        "the-butterfly-that-stamped",
        "the-crab-that-played-with-the-sea",
    ]
    sort_order += 1
    items.append({
        "id": "theme-independence-and-belonging",
        "name": "Independence and Belonging",
        "sort_order": sort_order,
        "category": "theme",
        "level": 2,
        "relationship_type": "emergence",
        "composite_of": independence_stories,
        "sections": {
            "About": "The Cat walks alone. Pau Amma plays by himself while others follow the rules. The Butterfly boasts of power he doesn't have. These stories explore the tension between independence and community, between following your own path and accepting your place in the larger order. Kipling's answers are nuanced: the Cat gets his freedom but pays a price; Pau Amma is disciplined but not destroyed.",
            "For Parents": "The Cat story is a philosophical gem. Children who are fiercely independent will identify with the Cat; children who value belonging will side with the Dog. Neither is wrong. This is a wonderful story for exploring different temperaments and the idea that there's more than one valid way to live.",
        },
        "keywords": ["independence", "belonging", "freedom", "community", "choice"],
        "metadata": {},
    })

    # === L3: Meta-categories ===
    all_group_ids = ["group-animal-origins", "group-human-inventions", "group-cosmic-tales"]
    all_theme_ids = ["theme-curiosity-and-consequence", "theme-laziness-and-trickery", "theme-independence-and-belonging"]

    sort_order += 1
    items.append({
        "id": "meta-the-stories",
        "name": "The Stories",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "relationship_type": "emergence",
        "composite_of": all_group_ids,
        "sections": {
            "About": "The complete Just So Stories: twelve tales in three natural groups. Seven animal origin stories explain how creatures got their distinctive features. Two Tegumai stories celebrate the invention of writing. Three cosmic tales explore the tides, the contract between wildness and civilization, and the uses of wisdom. All twelve are told in Kipling's unmistakable voice -- rolling, rhythmic, playful, designed to be read aloud to a beloved child.",
            "How to Use": "Start with The Elephant's Child -- it's the most beloved and the most fun to read aloud. Then try How the Whale Got His Throat for its wonderful rhythmic language. Save The Cat That Walked by Himself for last -- it's the most complex and rewards a reader who already knows Kipling's voice.",
        },
        "keywords": ["stories", "collection", "structure", "groups"],
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
            "About": "The themes that run through Just So Stories: curiosity and its consequences, laziness and trickery and the transformations they bring, and the tension between independence and belonging. These themes cut across the story groupings, connecting the animal tales to the cosmic ones and revealing the deeper questions Kipling was exploring beneath the humor.",
            "How to Use": "Browse by theme when a particular question is alive in your child's life. A child who asks 'why?' endlessly will love the curiosity stories. A child struggling with rules or chores will find the laziness tales illuminating. A child navigating the tension between fitting in and being themselves will connect deeply with the independence stories.",
        },
        "keywords": ["themes", "analysis", "perspectives", "meaning"],
        "metadata": {},
    })

    # === Build Grammar ===
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Rudyard Kipling",
                    "date": "1902",
                    "note": "Author of Just So Stories for Little Children",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2001",
                    "note": "eBook #2781 — digitized text",
                },
                {
                    "name": "PlayfulProcess",
                    "date": "2026-03-04",
                    "note": "Grammar construction and thematic groupings",
                },
            ],
        },
        "name": "Just So Stories",
        "description": (
            "Rudyard Kipling's Just So Stories for Little Children (1902) -- twelve pourquoi tales "
            "explaining how animals got their features and how humanity invented writing, told in "
            "Kipling's rolling, rhythmic, endlessly quotable prose. From the Elephant's 'satiable curiosity "
            "to the Cat who walks by himself, these are among the most-read-aloud stories in the English language.\n\n"
            "Source: Project Gutenberg eBook #2781 (https://www.gutenberg.org/ebooks/2781).\n\n"
            "Note: These stories reflect Kipling's colonial-era worldview and contain descriptions of "
            "non-European peoples that reflect period attitudes. The story 'How the Leopard Got His Spots' "
            "includes racial characterizations that modern readers should discuss critically.\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES:\n"
            "- Rudyard Kipling (1902, Macmillan) -- Kipling himself illustrated the original edition "
            "with distinctive pen-and-ink drawings, each with a detailed caption explaining the illustration\n"
            "- Joseph M. Gleeson (1912, Doubleday) -- color plate illustrations for the American edition"
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "children",
            "classic",
            "fables",
            "animals",
            "public-domain",
            "rudyard-kipling",
            "pourquoi-tales",
            "read-aloud",
            "full-text",
            "multi-level",
        ],
        "roots": ["wonder-imagination"],
        "shelves": ["children", "wonder", "contested"],
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
    print(f"  L1 stories: {len(l1)}")
    print(f"  L2 groups + themes: {len(l2)}")
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
