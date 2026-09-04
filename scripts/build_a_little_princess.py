#!/usr/bin/env python3
"""
Build grammar.json for A Little Princess by Frances Hodgson Burnett.

Source: Project Gutenberg eBook #146
Structure: 19 chapters
Levels:
  L1: Individual chapters (full text)
  L2: Thematic groupings with composite_of
  L3: Meta-categories (The Story, Themes)
"""

import json
import re
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "seeds" / "a-little-princess.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "a-little-princess"
OUTPUT_FILE = OUTPUT_DIR / "grammar.json"

CHAPTER_TITLES = {
    1: "Sara",
    2: "A French Lesson",
    3: "Ermengarde",
    4: "Lottie",
    5: "Becky",
    6: "The Diamond Mines",
    7: "The Diamond Mines Again",
    8: "In the Attic",
    9: "Melchisedec",
    10: "The Indian Gentleman",
    11: "Ram Dass",
    12: "The Other Side of the Wall",
    13: "One of the Populace",
    14: "What Melchisedec Heard and Saw",
    15: "The Magic",
    16: "The Visitor",
    17: '"It Is the Child"',
    18: '"I Tried Not to Be"',
    19: "Anne",
}

CHAPTER_SUMMARIES = {
    1: "Seven-year-old Sara Crewe arrives at Miss Minchin's boarding school in London with her adoring father, Captain Crewe. Sara is imaginative, generous, and oddly mature for her age. Her father lavishes her with everything — a private room, a French maid, and the doll Emily — before departing for India and his diamond mines.",
    2: "Sara's first day at school reveals her unusual character. She already speaks fluent French (having learned it from her mother), which embarrasses Monsieur Dufarge and irritates Miss Minchin. Sara handles the situation with characteristic grace, refusing to take credit and putting others at ease.",
    3: "Sara befriends Ermengarde St. John, a kind but slow-witted girl whom Miss Minchin treats with contempt. Sara's gift is making stories come alive — she transforms homework into adventures, helping Ermengarde see learning as discovery rather than punishment.",
    4: "Sara becomes a mother figure to little Lottie Legh, a four-year-old who throws tantrums because she has no mother. Sara comforts her by declaring she will be Lottie's 'mamma' at school — an act of imaginative love that foreshadows Sara's deeper gifts.",
    5: "Sara discovers Becky, a young scullery maid who works in the kitchen and sleeps in the attic. Sara treats Becky with the same kindness she shows everyone, sharing food and stories. Their friendship crosses the rigid class boundaries of Victorian England.",
    6: "Captain Crewe's letters become troubled — he has invested everything in diamond mines with a friend. Sara's eleventh birthday party is interrupted by devastating news: her father has died penniless. Miss Minchin, furious at losing her most profitable pupil, strips Sara of everything.",
    7: "Sara is banished to the attic next to Becky and forced to work as an errand girl and servant. She goes from princess to pauper overnight. But Sara clings to her imagination, telling herself she can pretend to be a princess even in rags — 'If I am a princess in rags and tatters, I can be a princess inside.'",
    8: "Life in the attic is cold, lonely, and hungry. Sara endures Miss Minchin's cruelty, the cook's spite, and the other students' pity or scorn. But she finds companionship with Becky, with Emily her doll, and with her own fierce imagination, which transforms the bare attic into a palace.",
    9: "Sara befriends a rat she names Melchisedec, sharing her meager crumbs with him. The rat becomes a symbol of her unbroken spirit — even in poverty, she finds someone to care for. Her ability to see dignity in a rat reflects her refusal to let circumstances define her.",
    10: "A sickly Indian gentleman, Mr. Carrisford, moves into the house next door with his Indian servant Ram Dass. He is searching desperately for the lost daughter of his former partner — Captain Crewe. Sara watches the house with curiosity, not knowing her fate is connected to it.",
    11: "Ram Dass, perched on the roof, sees Sara's bare, miserable attic through the skylight and is moved. He begins a secret campaign to comfort her — first returning a pet monkey that escapes to her room, then planning something much bigger with Mr. Carrisford.",
    12: "Sara, starving and exhausted, passes by Mr. Carrisford's house daily. The narrative moves between Sara's suffering and Mr. Carrisford's guilty search for 'the little girl.' Neither knows the other is right next door. The irony builds toward the climax.",
    13: "On a bitterly cold day, Sara finds a fourpence in the gutter and uses it to buy hot buns from a bakery. Starving as she is, she gives most of them away to a beggar girl even hungrier than herself — proving that her princess nature is real, not pretend.",
    14: "Melchisedec witnesses the secret transformation: Ram Dass and his assistants cross the rooftops at night and fill Sara's attic with warm blankets, food, a fire, and beautiful things. Sara wakes to find her garret transformed into the palace she had always imagined.",
    15: "The magic continues night after night. Sara calls it 'The Magic' — the mysterious force that keeps filling her room with comfort. She shares the bounty with Becky. Miss Minchin is baffled and furious but cannot discover the source.",
    16: "Mr. Carrisford's lawyer finally traces the lost child to Miss Minchin's school. Mr. Carrisford sends for Sara, but Miss Minchin tries to prevent the meeting. Sara is brought next door, where the truth begins to unfold.",
    17: "Mr. Carrisford recognizes Sara as Ralph Crewe's daughter — the child he has been searching for. The diamond mines, far from being worthless, have produced enormous wealth. Sara is not a pauper but an heiress. Miss Minchin arrives to protest and is thoroughly humiliated.",
    18: "Sara confronts her transformation from servant back to wealthy child. When asked if she can forgive Miss Minchin, Sara replies with quiet dignity: 'I tried not to be' — referring to her struggle not to become bitter. Her character has been tested by suffering and proven genuine.",
    19: "Sara settles into her new life next door with Mr. Carrisford, taking Becky with her as her personal attendant (not servant — companion). She returns to the bakery to arrange for the baker-woman to feed hungry children, ensuring that no child need suffer as she did. The Large Family (a family of happy children Sara used to watch longingly) welcomes her. The story ends with generosity triumphing over cruelty.",
}

CHAPTER_REFLECTIONS = {
    1: "Sara's father says she is 'not like other children.' What does he mean? Is it good to be different from others?",
    2: "Sara already knows French but doesn't want to embarrass anyone. How do you handle knowing something others don't?",
    3: "Sara helps Ermengarde learn by turning lessons into stories. What's something hard that became easier when someone helped you?",
    4: "Sara pretends to be Lottie's mamma. Why does pretending sometimes help with real feelings?",
    5: "Sara treats Becky the same as everyone else, even though others don't. Why is it important to be kind to everyone, no matter their job?",
    6: "Everything changes for Sara in one day. Have you ever had a day that changed everything? How did you handle it?",
    7: "Sara says 'If I am a princess in rags and tatters, I can be a princess inside.' What does it mean to be a princess on the inside?",
    8: "Sara uses her imagination to make the cold attic feel like a palace. How does imagination help us when things are hard?",
    9: "Even when Sara is starving, she shares her food with a rat. Why does she do this? What does caring for others give us?",
    10: "Mr. Carrisford is searching for Sara without knowing she's right next door. Have you ever been looking for something that was closer than you thought?",
    11: "Ram Dass sees Sara's suffering and decides to help secretly. Why do you think he helps without telling her who he is?",
    12: "Sara walks past Mr. Carrisford's house every day, not knowing he holds the key to her future. What do you think about the idea that help might be closer than we realize?",
    13: "Sara gives her buns to the beggar girl even though she's starving too. What makes someone generous even when they have almost nothing?",
    14: "Sara wakes up to find her attic transformed. What would it feel like to have your biggest wish come true overnight?",
    15: "Sara calls the gifts 'The Magic.' Why does she use that word? What is magical about unexpected kindness?",
    16: "The visitor comes to take Sara away from Miss Minchin's. What do you think Sara feels in this moment — joy, fear, or both?",
    17: "Sara discovers she is rich again. But has she changed from who she was when she was poor? What stayed the same?",
    18: "Sara says 'I tried not to be' — meaning she tried not to become mean or bitter. Why is this the hardest and bravest thing she did?",
    19: "Sara uses her money to help hungry children. Why does the story end this way? What does it tell us about what wealth is really for?",
}

CHAPTER_PARENT_NOTES = {
    1: "This opening chapter establishes Sara as an extraordinary child — not because of her father's wealth, but because of her imagination and emotional intelligence. Notice how Burnett makes Sara sympathetic without making her perfect: she's opinionated, stubborn, and odd. A wonderful starting point for discussing what makes someone special.",
    2: "The French lesson scene is a masterclass in social grace. Sara's instinct to protect Monsieur Dufarge's feelings rather than show off her knowledge reveals her essential character. This is a great chapter for talking about humility versus false modesty.",
    3: "Sara's friendship with Ermengarde models how the gifted can support others without condescension. Sara doesn't do Ermengarde's work for her — she transforms it into something Ermengarde can love. A beautiful example of teaching through storytelling.",
    4: "Sara's adoption of Lottie as her 'little mamma' shows how children create the relationships they need. Lottie needs a mother; Sara needs someone to care for. Their bond is built on imaginative love — pretending that becomes real through devotion.",
    5: "The Sara-Becky friendship is radical for its time. Burnett deliberately crosses class lines, showing that kindness recognizes no social boundary. This chapter offers rich ground for discussing fairness, privilege, and how we treat people who serve us.",
    6: "The reversal of fortune is swift and brutal. Miss Minchin's transformation from fawning to cruel reveals her true character. This is an important chapter for discussing how people treat others based on money, and what that reveals about character.",
    7: "Sara's famous declaration about being 'a princess inside' is the moral center of the book. Burnett argues that true nobility is a quality of character, not circumstance. This chapter is powerful for children experiencing hardship — it validates the inner self against outer conditions.",
    8: "The attic chapters are the emotional core of the novel. Sara's suffering is real and unvarnished, but so is her resilience. Burnett doesn't pretend imagination erases pain — it transforms it. This is a crucial distinction for children to understand.",
    9: "The Melchisedec chapter reveals Sara's fundamental nature: she is a caregiver. Even at her lowest, she finds someone to nurture. This reflects Burnett's belief that generosity is not about having much, but about the impulse to share whatever you have.",
    10: "The dramatic irony begins here — the reader knows (or suspects) that Mr. Carrisford is connected to Sara, but neither character knows. This is a good chapter for discussing how stories create suspense and why it's satisfying when pieces come together.",
    11: "Ram Dass is one of literature's quiet heroes. His compassion crosses cultural and class boundaries. The rooftop scenes are magical in the literal sense — they prepare for the transformation that Sara will call 'The Magic.'",
    12: "The parallel narrative — Sara suffering on one side of the wall, Carrisford searching on the other — is structurally brilliant. Burnett uses architecture as metaphor: the wall between them is thin, but neither can see through it.",
    13: "The bun scene is the moral climax of the novel. Sara, who has been a 'princess' in imagination, proves it in action. Giving away food when you're starving is the ultimate test of character. The baker-woman's reaction — watching this starving child feed someone hungrier — is deeply moving.",
    14: "The secret transformation of the attic is pure fairy tale magic brought into a realistic novel. Notice that Burnett doesn't make it supernatural — it's human kindness working through human hands. But Sara's word for it — 'Magic' — captures something true about unexpected grace.",
    15: "The Magic chapters balance between fairy tale and realism. Sara knows someone is helping her, but she chooses to call it Magic because that's how it feels. This distinction between explanation and experience is worth discussing with older children.",
    16: "The climax approaches. Miss Minchin's attempts to prevent Sara's rescue reveal her as the true villain — not poverty, not fate, but human cruelty. This chapter builds toward the confrontation that will resolve everything.",
    17: "The recognition scene is emotionally complex. Sara is not simply restored to wealth — she is recognized as the person she always was. Mr. Carrisford's guilt and relief, Miss Minchin's fury, Sara's quiet dignity — all come together in this chapter.",
    18: "'I tried not to be' is one of the most powerful lines in children's literature. Sara is not claiming perfection — she's admitting the struggle. She wanted to be bitter, wanted to be cruel, but she fought against it. This honest admission of inner conflict is far more powerful than simple goodness.",
    19: "The ending is not just about Sara getting her happy ending — it's about her using her restored fortune to create justice. The bakery arrangement ensures other hungry children will be fed. Burnett argues that wealth is only meaningful when it serves others.",
}

# Thematic groupings
THEMATIC_GROUPS = {
    "theme-imagination-as-survival": {
        "name": "Imagination as Survival",
        "description": "Sara's greatest gift is her imagination — the ability to transform cold attics into palaces, loneliness into adventure, and suffering into story. These chapters show how the inner life sustains the outer one.",
        "for_parents": "Burnett believed that imagination was not escape but survival. Sara doesn't pretend her suffering isn't real — she transforms it through storytelling. These chapters are powerful for children going through difficult times, showing that the stories we tell ourselves about our circumstances matter as much as the circumstances themselves.",
        "keywords": ["imagination", "storytelling", "resilience", "pretending", "inner-life"],
        "chapters": [1, 3, 7, 8, 15],
    },
    "theme-kindness-across-boundaries": {
        "name": "Kindness Across Boundaries",
        "description": "Sara treats everyone with equal dignity — from the wealthy Ermengarde to the scullery maid Becky, from a beggar girl to a rat. These chapters explore how true kindness ignores social boundaries.",
        "for_parents": "Victorian England was rigidly stratified by class, and Burnett deliberately challenges this. Sara's friendships with Becky, Lottie, Ermengarde, and even Melchisedec the rat all cross boundaries that society says should not be crossed. These chapters open conversations about fairness, privilege, and seeing the person behind the role.",
        "keywords": ["kindness", "class", "friendship", "equality", "generosity"],
        "chapters": [3, 4, 5, 9, 13, 19],
    },
    "theme-reversal-of-fortune": {
        "name": "Reversal of Fortune",
        "description": "From princess to pauper and back again — the dramatic arc of Sara's life tests whether character depends on circumstance. These chapters trace the falls and rises that reveal who people truly are.",
        "for_parents": "The reversal of fortune is the engine of the plot, but Burnett uses it to ask a deeper question: does wealth make you good? Sara's answer is no — goodness is tested by hardship, not granted by privilege. Miss Minchin's behavior changes with Sara's fortune; Sara's does not. This contrast is the moral heart of the book.",
        "keywords": ["wealth", "poverty", "character", "fortune", "testing"],
        "chapters": [1, 6, 7, 8, 17, 18],
    },
    "theme-the-magic-of-kindness": {
        "name": "The Magic of Kindness",
        "description": "Ram Dass, Mr. Carrisford, and the unseen helpers who transform Sara's attic represent the magic that exists in human compassion. These chapters explore how kindness, when it appears unexpectedly, feels like real magic.",
        "for_parents": "Sara calls the secret gifts 'The Magic,' and Burnett is making a point: real magic is not supernatural — it's what happens when compassionate people act on what they see. Ram Dass sees suffering and responds. Mr. Carrisford tries to make amends. These chapters show children that the world contains helpers, and that they can be helpers too.",
        "keywords": ["magic", "compassion", "secret-help", "transformation", "grace"],
        "chapters": [10, 11, 14, 15, 16],
    },
    "theme-inner-princess": {
        "name": "The Inner Princess",
        "description": "Sara's defining belief: that being a princess is about character, not circumstance. Whether in silk or rags, she holds to the idea that dignity, generosity, and grace are choices, not gifts of fortune.",
        "for_parents": "The 'inner princess' concept is Burnett's central argument. Sara doesn't mean literal royalty — she means the choice to be generous, dignified, and kind regardless of how you're treated. This is especially powerful for children facing unfair treatment: your circumstances don't define you, your choices do. The chapters where Sara is tested most severely are where this theme shines brightest.",
        "keywords": ["princess", "dignity", "character", "identity", "resilience"],
        "chapters": [1, 7, 13, 17, 18],
    },
}


def read_and_strip_gutenberg(filepath):
    """Read the seed text and strip Gutenberg header/footer."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK A LITTLE PRINCESS ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK A LITTLE PRINCESS ***"
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def split_into_chapters(text):
    """Split the full text into chapters.

    A Little Princess uses a simple format:
    <number>

    <Title>

    <text>
    """
    # Pattern: a line with just a number, then blank line, then title
    chapter_pattern = re.compile(
        r'(?:^|\n)\n(\d{1,2})\n\n([^\n]+)\n',
        re.MULTILINE
    )

    matches = list(chapter_pattern.finditer(text))
    chapters = {}

    for i, match in enumerate(matches):
        chapter_num = int(match.group(1))
        # Only process chapters 1-19
        if chapter_num < 1 or chapter_num > 19:
            continue

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        # Clean up extra blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)

        chapters[chapter_num] = content

    return chapters


def build_grammar():
    """Build the complete A Little Princess grammar."""
    text = read_and_strip_gutenberg(SEED_FILE)
    chapters = split_into_chapters(text)

    if len(chapters) != 19:
        print(f"WARNING: Expected 19 chapters, found {len(chapters)}: {sorted(chapters.keys())}")

    items = []
    sort_order = 0
    chapter_ids = {}

    # === L1: Individual chapters ===
    for chapter_num in sorted(chapters.keys()):
        sort_order += 1
        item_id = f"chapter-{chapter_num:02d}"
        chapter_ids[chapter_num] = item_id

        chapter_text = chapters[chapter_num]

        item = {
            "id": item_id,
            "name": f"Chapter {chapter_num}: {CHAPTER_TITLES[chapter_num]}",
            "sort_order": sort_order,
            "category": f"chapter-{chapter_num:02d}",
            "level": 1,
            "sections": {
                "Story": chapter_text,
                "Reflection": CHAPTER_REFLECTIONS.get(chapter_num, "What does this chapter make you think about?"),
                "For Parents": CHAPTER_PARENT_NOTES.get(chapter_num, ""),
            },
            "keywords": get_chapter_keywords(chapter_num),
            "metadata": {
                "chapter_number": chapter_num,
                "chapter_name": CHAPTER_TITLES[chapter_num],
            },
        }
        items.append(item)

    # === L2: Chapter summaries ===
    for chapter_num in sorted(chapters.keys()):
        sort_order += 1
        summary_id = f"summary-chapter-{chapter_num:02d}"

        item = {
            "id": summary_id,
            "name": f"Summary: {CHAPTER_TITLES[chapter_num]}",
            "sort_order": sort_order,
            "category": "chapter-summary",
            "level": 2,
            "relationship_type": "emergence",
            "composite_of": [chapter_ids[chapter_num]],
            "sections": {
                "About": CHAPTER_SUMMARIES.get(chapter_num, ""),
                "For Parents": CHAPTER_PARENT_NOTES.get(chapter_num, ""),
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

        theme_chapter_ids = [chapter_ids[ch] for ch in theme_data["chapters"] if ch in chapter_ids]

        item = {
            "id": theme_id,
            "name": theme_data["name"],
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "relationship_type": "emergence",
            "composite_of": theme_chapter_ids,
            "sections": {
                "About": theme_data["description"],
                "For Parents": theme_data["for_parents"],
            },
            "keywords": theme_data["keywords"],
            "metadata": {},
        }
        items.append(item)

    # === L3: Meta-categories ===
    all_summary_ids = [f"summary-chapter-{n:02d}" for n in sorted(chapters.keys())]
    all_theme_ids = list(THEMATIC_GROUPS.keys())

    sort_order += 1
    items.append({
        "id": "meta-the-story",
        "name": "The Story",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "relationship_type": "emergence",
        "composite_of": all_summary_ids,
        "sections": {
            "About": "The complete narrative of A Little Princess: Sara Crewe's journey from pampered pupil to abused servant and back to heiress. Nineteen chapters trace how imagination, kindness, and inner dignity survive the cruelest reversals of fortune. At its heart, this is a story about what it means to be a princess — not by birth or wealth, but by the quality of one's character.",
            "For Parents": "A Little Princess works on multiple levels. For younger children, it's a Cinderella story with a satisfying ending. For older children, it raises profound questions about wealth, class, identity, and what defines a person's worth. Burnett wrote from her own experience of poverty and wealth, and the book's emotional truth runs deep. Read it together and let the conversations about fairness, imagination, and character unfold naturally.",
        },
        "keywords": ["complete-story", "narrative", "sara-crewe", "chapters"],
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
            "About": "The great themes woven through A Little Princess — imagination as survival, kindness across boundaries, the reversal of fortune, the magic of compassion, and the inner princess. These groupings reveal how Burnett returns again and again to questions of character versus circumstance.",
            "For Parents": "These thematic groupings help you explore the novel beyond the plot. Each theme connects chapters that share a common thread. If your child is drawn to Sara's storytelling, explore 'Imagination as Survival.' If they're troubled by Miss Minchin's cruelty, 'Reversal of Fortune' provides context. The story rewards re-reading from many angles.",
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
                    "name": "Frances Hodgson Burnett",
                    "date": "1905",
                    "note": "Original author of A Little Princess",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "1994",
                    "note": "eBook #146 — produced by Judith Boss, HTML version by Al Haines",
                },
                {
                    "name": "PlayfulProcess",
                    "date": "2026-03-04",
                    "note": "Grammar construction, chapter summaries, and thematic groupings",
                },
            ],
        },
        "name": "A Little Princess",
        "description": (
            "Frances Hodgson Burnett's A Little Princess (1905) — the beloved story of Sara Crewe, "
            "a girl whose imagination and inner dignity sustain her through the cruelest reversal of fortune. "
            "From pampered pupil to attic servant and back to heiress, Sara proves that being a princess "
            "is about character, not circumstance. Structured as 19 chapters with thematic groupings "
            "exploring imagination, kindness, resilience, and the magic of compassion.\n\n"
            "Source: Project Gutenberg eBook #146 (https://www.gutenberg.org/ebooks/146).\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES:\n"
            "- Ethel Franklin Betts (1905, Charles Scribner's Sons) — original edition illustrator, "
            "elegant pen-and-ink drawings of Sara in both her wealthy and impoverished states\n"
            "- Reginald Birch (1888, illustrated Little Lord Fauntleroy) — Burnett's preferred illustrator, "
            "whose style defined the visual world of her children's novels\n"
            "- Harold Piffard (1905, Frederick Warne) — UK edition illustrations"
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "children",
            "classic",
            "resilience",
            "imagination",
            "public-domain",
            "frances-hodgson-burnett",
            "full-text",
            "chapters",
            "multi-level",
            "victorian",
        ],
        "roots": ["wonder-imagination"],
        "shelves": ["children"],
        "lineages": ["Linehan"],
        "worldview": "imaginative",
        "items": items,
    }

    return grammar


def get_chapter_keywords(chapter_num):
    """Return keywords for a chapter."""
    keywords_map = {
        1: ["sara", "captain-crewe", "arrival", "school", "emily", "imagination"],
        2: ["french", "lesson", "miss-minchin", "grace", "humility"],
        3: ["ermengarde", "friendship", "stories", "learning", "imagination"],
        4: ["lottie", "mothering", "comfort", "pretending", "care"],
        5: ["becky", "scullery-maid", "kindness", "class", "friendship"],
        6: ["diamond-mines", "birthday", "death", "reversal", "loss"],
        7: ["attic", "poverty", "princess-inside", "resilience", "dignity"],
        8: ["attic", "suffering", "imagination", "survival", "cold"],
        9: ["melchisedec", "rat", "sharing", "companionship", "generosity"],
        10: ["indian-gentleman", "carrisford", "search", "mystery", "neighbor"],
        11: ["ram-dass", "rooftop", "compassion", "secret-help", "observation"],
        12: ["wall", "irony", "search", "proximity", "suffering"],
        13: ["buns", "beggar-girl", "generosity", "sacrifice", "true-princess"],
        14: ["transformation", "attic", "magic", "gifts", "wonder"],
        15: ["magic", "mystery", "kindness", "sharing", "becky"],
        16: ["visitor", "recognition", "rescue", "discovery"],
        17: ["recognition", "diamond-mines", "wealth", "restoration", "miss-minchin"],
        18: ["forgiveness", "character", "testing", "dignity", "resilience"],
        19: ["anne", "bakery", "generosity", "new-life", "helping-others"],
    }
    return keywords_map.get(chapter_num, [])


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
    print(f"  L2 summaries + themes: {len(l2)}")
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


if __name__ == "__main__":
    main()
