#!/usr/bin/env python3
"""
Build grammar.json for The Secret Garden by Frances Hodgson Burnett.

Source: Project Gutenberg eBook #113
Structure: 27 chapters
Levels:
  L1: Individual chapters (full text)
  L2: Thematic groupings with composite_of + chapter summaries
  L3: Meta-categories (The Story, Themes)
"""

import json
import re
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "seeds" / "secret-garden.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "secret-garden"
OUTPUT_FILE = OUTPUT_DIR / "grammar.json"

CHAPTER_TITLES = {
    1: "There Is No One Left",
    2: "Mistress Mary Quite Contrary",
    3: "Across the Moor",
    4: "Martha",
    5: "The Cry in the Corridor",
    6: '"There Was Someone Crying — There Was!"',
    7: "The Key to the Garden",
    8: "The Robin Who Showed the Way",
    9: "The Strangest House Anyone Ever Lived In",
    10: "Dickon",
    11: "The Nest of the Missel Thrush",
    12: '"Might I Have a Bit of Earth?"',
    13: '"I Am Colin"',
    14: "A Young Rajah",
    15: "Nest Building",
    16: '"I Won\'t!" Said Mary',
    17: "A Tantrum",
    18: '"Tha\' Munnot Waste No Time"',
    19: '"It Has Come!"',
    20: '"I Shall Live Forever — and Ever — and Ever!"',
    21: "Ben Weatherstaff",
    22: "When the Sun Went Down",
    23: "Magic",
    24: '"Let Them Laugh"',
    25: "The Curtain",
    26: '"It\'s Mother!"',
    27: "In the Garden",
}

CHAPTER_SUMMARIES = {
    1: "Mary Lennox, a sickly, disagreeable child raised by servants in India, is orphaned by a cholera epidemic that kills her parents and all the household. Found alone and forgotten, she is sent to England to live with her uncle, Archibald Craven, at Misselthwaite Manor on the Yorkshire moors.",
    2: "Mary arrives in England — cold, cross, and unloved. She meets Mrs. Medlock, the housekeeper, who tells her about the vast, gloomy manor, her reclusive uncle, and the moors. Mary learns that there are a hundred rooms, most locked, and that her uncle is a hunchback grieving his dead wife.",
    3: "The journey across the dark, wild moor to Misselthwaite Manor. Mary sees nothing but emptiness and is told about the moors by Mrs. Medlock. She arrives at the enormous house to find it dark and cold — a lonely place for a lonely child.",
    4: "Mary meets Martha Sowerby, a cheerful Yorkshire maid who treats her as an equal, not a little maharani. Martha tells Mary about her family — especially her brother Dickon, who can charm animals — and about the locked garden. Mary's curiosity awakens for the first time.",
    5: "Mary explores the grounds and meets Ben Weatherstaff, a crusty old gardener, and a friendly robin. She begins to feel the first stirrings of health from the fresh air. At night, she hears a mysterious crying in the corridors that the servants deny.",
    6: "Mary confronts Mrs. Medlock about the crying she heard. The servants insist it was the wind, but Mary knows better. Her stubborn, contrary nature becomes an asset — she refuses to accept the lie and begins investigating the mystery of the hidden rooms.",
    7: "Mary discovers the key to the locked garden, buried in the earth where a robin digs. The garden was locked ten years ago when Archibald Craven's wife died after a branch broke and she fell. Finding the key fills Mary with a thrill of secret ownership.",
    8: "The robin shows Mary the hidden door behind the ivy. She pushes through and enters the secret garden for the first time — a walled, abandoned space where roses still grow tangled and wild. Something in Mary's hard, little heart begins to soften.",
    9: "Mary continues exploring the manor's many rooms, finding treasures and oddities. She hears the crying again and follows it through corridors to discover Colin Craven — her cousin, a bedridden boy who believes he is going to die.",
    10: "Mary meets Dickon Sowerby on the moor — a boy who speaks to animals and carries a fox cub and a crow. She tells him about the secret garden, and he becomes her co-conspirator in bringing it back to life. Dickon teaches her about plants, bulbs, and the earth's patience.",
    11: "Mary works in the garden with increasing joy, learning to dig, plant, and tend growing things. The robin is nesting. Mary begins to change physically — her appetite grows, her cheeks take color, and her manner softens. The garden is healing her as she heals it.",
    12: "Mary musters the courage to ask her uncle if she might 'have a bit of earth' — a garden to plant in. Archibald Craven, moved by her directness, agrees. This brief encounter is significant: Mary sees her uncle's grief and begins to understand that adults can be broken too.",
    13: "Mary finds Colin again and they talk through the night. Colin is imperious, hypochondriacal, and terrified of death — but also desperately lonely. Mary tells him about the moor, about Dickon, about the secret garden (without revealing it). For the first time, Colin has something to look forward to.",
    14: "Colin plays the 'young rajah,' ordering servants about and demanding Mary's company. But Mary stands up to him — she is the first person who refuses to pity or obey him. Their battles are fierce but productive, as each challenges the other's worst habits.",
    15: "Spring arrives in the garden. Dickon brings seeds and tools, and Mary works alongside him while telling Colin about everything growing outside. The garden becomes a living counterpart to Colin's sickroom — one bursting with life, the other stifled by fear.",
    16: "Mary and Colin have a tremendous argument. Colin throws a tantrum, convinced he's going to die. Mary, furious, shouts that there's nothing wrong with his back and he's not going to die. Her blunt honesty — born of her own contrary nature — is exactly what Colin needs.",
    17: "Colin has a full tantrum, screaming and thrashing. Mary storms in, matches his fury with her own, and forces him to see that his 'lump' is just his spine — all spines have bumps. The tantrum breaks like a fever. Colin asks Mary to tell him about the garden, and he falls asleep listening.",
    18: "Dickon comes to Colin's room for the first time, bringing the moor inside — a newborn lamb, a crow, a fox cub. Colin is enchanted. For the first time, he wants to go outside. The three children plan to get Colin into the garden.",
    19: "Spring explodes across the moor and garden. Colin goes outside for the first time, carried in his wheelchair. He sees the sky, smells the earth, feels the wind. When they bring him into the secret garden, he is overwhelmed — 'I shall live forever — and ever — and ever!'",
    20: "Colin stands for the first time in the garden, supported by Dickon and Mary. He feels the life force rising in him — what he calls 'the Magic.' He begins a daily practice of affirmation, declaring that he will get well, that the Magic is in him. The garden and the boy heal together.",
    21: "Ben Weatherstaff, the old gardener, discovers the children in the locked garden by climbing a ladder. He is furious — then stunned to see Colin on his feet. Ben reveals that he has secretly tended the roses all these years, climbing over the wall because Mrs. Craven loved them.",
    22: "Colin experiments with the Magic — deep breathing, positive thinking, physical exercise. He and Dickon and Mary make the garden their laboratory. Colin grows stronger each day, walking, then running. The servants are baffled by his transformation but the children keep their secret.",
    23: "Colin articulates his philosophy of 'the Magic' — the life force in everything, the power of believing in good things. He leads the children in a kind of ceremony in the garden, chanting affirmations. This chapter is Burnett's most direct statement of her own New Thought beliefs about the power of the mind.",
    24: "Colin struggles with wanting to keep his recovery secret so he can surprise his father. He pretends to still be ill, which requires elaborate deception. Meanwhile, Susan Sowerby — Martha and Dickon's mother, a wise presence throughout the book — finally visits the garden and blesses the children's work.",
    25: "Archibald Craven, wandering in grief through Europe, has a dream and a letter that call him home. Susan Sowerby's letter tells him he must come back. He begins the journey to Misselthwaite Manor, sensing that something has changed.",
    26: "Craven arrives at Misselthwaite and is directed to the garden. He hears laughter behind the locked door. Colin — strong, healthy, running — bursts out of the garden and into his father's arms. The locked garden door opens, and with it, the locked grief of ten years.",
    27: "The final chapter brings everything together. Father and son walk back to the manor together — Colin strong and upright, Craven weeping with joy. The servants are astonished. Mrs. Medlock, Ben Weatherstaff, and everyone at the manor witness the miracle that the garden has wrought. The secret is out, and it is glorious.",
}

CHAPTER_REFLECTIONS = {
    1: "Mary is described as disagreeable and unloved. Do you think she was born that way, or did her circumstances make her that way?",
    2: "Mary has never had to dress herself or do anything on her own. What happens when we do too much for someone?",
    3: "The moor seems empty and frightening to Mary. Have you ever been scared of a new place that turned out to be wonderful?",
    4: "Martha treats Mary differently from the Indian servants. Why is it sometimes good when people don't just do what you want?",
    5: "Mary starts feeling better from being outside. Why do you think fresh air and nature make us feel healthier?",
    6: "Mary refuses to believe the servants' lies about the crying. When is being stubborn actually a good thing?",
    7: "Finding the key to the garden feels magical to Mary. Have you ever found something hidden that felt like it was meant for you?",
    8: "When Mary enters the secret garden, something in her heart begins to change. What is it about a secret, beautiful place that changes us?",
    9: "Mary finds Colin — another lonely, neglected child. Why do you think the story brings these two together?",
    10: "Dickon can communicate with animals and seems to belong to the moor itself. What would it be like to feel that connected to nature?",
    11: "Mary is changing physically — getting stronger and healthier — as she works in the garden. How does caring for something else change us?",
    12: "Mary asks for 'a bit of earth.' What does it mean to have your own small piece of the world to tend?",
    13: "Colin is afraid he's going to die. How does fear change the way we live? What happens when someone helps us see past our fears?",
    14: "Mary and Colin are both stubborn and difficult. Why does their friendship work when both are so contrary?",
    15: "The garden is coming alive in spring. How is the garden like a mirror of what's happening to Mary and Colin?",
    16: "Mary shouts at Colin that he's not going to die. Sometimes the truth is hard to hear. Can harsh honesty be a form of love?",
    17: "After his tantrum breaks, Colin wants to hear about the garden. Why does calming down open us to beautiful things?",
    18: "Dickon brings the moor to Colin's room. What happens when someone brings the outside world to someone who is trapped?",
    19: "Colin sees the sky and garden for the first time and says he'll live forever. What does it feel like to discover the world is bigger and more beautiful than you imagined?",
    20: "Colin calls the life force 'the Magic.' What do you think the Magic really is?",
    21: "Ben Weatherstaff secretly tended the roses for ten years out of love for Mrs. Craven. What acts of love do people do that no one sees?",
    22: "Colin practices getting well the way an athlete trains. How does practice and belief change what our bodies can do?",
    23: "Colin says the Magic is in everything — in the sun, in the earth, in people. Do you feel that? Where do you feel it most?",
    24: "Susan Sowerby is called 'a comfortable woman.' What does it mean to be a comforting presence for others?",
    25: "Archibald Craven has been running from his grief for ten years. Why do people run from sadness? What makes them ready to face it?",
    26: "Colin runs out of the garden into his father's arms. Why is this moment so powerful? What has been unlocked besides the garden door?",
    27: "The story ends with the whole manor witnessing the transformation. Why does Burnett want everyone to see the miracle, not just the family?",
}

CHAPTER_PARENT_NOTES = {
    1: "The opening is deliberately harsh — Mary is presented as ugly, unloved, and unlovable. Burnett wants readers to see how neglect creates disagreeable children, not nature. This is crucial framing: Mary isn't bad, she's been badly raised. Discuss how circumstances shape personality.",
    2: "Mrs. Medlock's description of Misselthwaite establishes the emotional landscape: locked rooms, a grieving uncle, a dead garden. Everything is closed, hidden, shut away. The manor is a physical metaphor for unexpressed grief.",
    3: "The moor is central to the book's meaning — it represents the wild, living world that will heal both children. Its initial appearance as desolate and frightening mirrors Mary's own bleak emotional state.",
    4: "Martha is the book's first agent of change. By treating Mary as ordinary rather than special, she inadvertently teaches Mary self-reliance. The contrast between Indian servants (who obeyed) and Yorkshire Martha (who speaks plainly) begins Mary's transformation.",
    5: "The robin is one of the book's key symbols — a wild creature that chooses to befriend Mary. Notice that Mary must be outdoors, in the air, before the healing can begin. Burnett is making a case for nature as medicine.",
    6: "Mary's contrariness — the trait that made her so disagreeable — becomes the tool that unlocks the mystery. Burnett argues that difficult traits aren't simply bad; they can be redirected toward discovery and truth-seeking.",
    7: "Finding the key is the first fairy-tale moment in an otherwise realistic novel. The robin, the freshly turned earth, the buried key — all suggest that nature itself is conspiring to help Mary. Discuss how readiness attracts discovery.",
    8: "The secret garden scene is the emotional pivot of the book. The tangled, dormant roses are alive — just neglected, like Mary herself. The parallel is explicit: the garden needs tending, Mary needs love, and tending the garden IS the love.",
    9: "The discovery of Colin mirrors Mary's own situation — another neglected child, isolated and afraid. But while Mary was neglected through indifference, Colin is smothered through fear. Both forms of parental failure produce the same result: a miserable child.",
    10: "Dickon represents Burnett's ideal of natural wholeness. He is at home in the world, at ease with animals, rooted in the earth. He's not supernatural — he's simply undamaged. His friendship teaches Mary and Colin what it looks like to be well.",
    11: "The garden-as-therapy metaphor becomes explicit here. Mary grows healthier as she gardens — the physical labor, the fresh air, the purpose. Modern research confirms what Burnett intuited: gardening genuinely heals mind and body.",
    12: "The brief scene with Archibald Craven is perfectly calibrated. Mary sees past his grief to the person underneath. His gift of 'a bit of earth' is both literal and metaphorical — he's giving her permission to put down roots.",
    13: "Colin is the book's most challenging character — imperious, self-pitying, and terrified. But Burnett shows that his behavior comes from fear, not malice. He has been told he will die, and no one has challenged this narrative. Mary will.",
    14: "The 'young rajah' chapter shows both children at their worst — and their best. Their conflicts are productive because both are fierce. Neither will coddle the other. This is a relationship of equals, and it's exactly what Colin needs.",
    15: "Spring in the garden is Burnett's great crescendo. The life returning to the garden mirrors the life returning to the children. This is not metaphor — it's the argument: nature heals. Get children outside, in the dirt, with growing things.",
    16: "Mary's refusal to pity Colin is the book's turning point. By insisting he's not dying, she gives him permission to live. This is radical for a children's book: sometimes love means refusing to accept someone's self-destructive story.",
    17: "The tantrum scene is cathartic — Colin's fear and rage pour out, and Mary matches him. When the storm passes, Colin is ready to hear about the garden. The emotional release precedes the physical healing. This pattern is psychologically astute.",
    18: "Dickon's arrival in Colin's room is magical because he brings the living world to a dying space. The animals, the stories, the earth-smell — all are medicine. Colin's desire to go outside is the desire to live.",
    19: "Colin's first time outside is one of literature's great scenes of awakening. His exclamation — 'I shall live forever' — is childish and beautiful. Burnett gives us permission to feel that spring IS resurrection, that life force IS magic.",
    20: "Colin's 'Magic' philosophy is Burnett's own belief in New Thought — the idea that positive thinking and affirmation can heal. Whether or not you share this philosophy, the story's emotional truth is undeniable: believing in life helps you live.",
    21: "Ben Weatherstaff's secret reveals that love doesn't stop because a door is locked. He climbed over the wall for ten years to tend the roses. This stubborn, gruff devotion mirrors the book's central message: life finds a way through walls.",
    22: "The 'scientific experiment' chapter shows Colin approaching healing with the same intensity he once brought to his fear. The shift from hypochondria to health is a redirect of energy, not a different kind. Strong wills can point in any direction.",
    23: "The Magic chapter is the most philosophical — and most controversial — in the book. Burnett's New Thought beliefs are on full display. Read it as a child's first encounter with the idea that consciousness matters, that how we think shapes how we live.",
    24: "Susan Sowerby is the book's true maternal figure — mother of twelve, wise without education, rooted in the earth. Her visit to the garden is a blessing. She represents the ordinary, practical magic of good mothering.",
    25: "Craven's return is triggered by dream and intuition — Burnett suggesting that the Magic works on him too, calling him home. His long avoidance of Misselthwaite mirrors Colin's avoidance of life: father and son share the same fear of facing what hurts.",
    26: "The reunion of Colin and his father is emotionally overwhelming. Colin runs — something everyone said he'd never do. The locked door opens. Craven weeps. Ten years of grief break like Colin's tantrum broke — suddenly, completely, and with healing on the other side.",
    27: "The ending is deliberately public — the whole household witnesses the miracle. Burnett insists that healing isn't private; it transforms communities. The secret garden's door is finally, permanently open. The secret is joy, and joy cannot stay hidden.",
}

THEMATIC_GROUPS = {
    "theme-healing-through-nature": {
        "name": "Healing Through Nature",
        "description": "The central argument of The Secret Garden: nature heals. Fresh air, growing things, soil, and sunlight transform both Mary and Colin from sickly, cross children into vibrant, healthy ones. The garden is doctor, therapist, and teacher.",
        "for_parents": "Burnett anticipated modern research on nature therapy by a century. The evidence is now strong: time outdoors reduces anxiety, improves physical health, and builds resilience. These chapters make the case through story, showing how digging in the dirt, watching things grow, and breathing open air can transform a child's life. If your family can garden together, this book is the perfect companion.",
        "keywords": ["nature", "healing", "garden", "growth", "outdoors", "health"],
        "chapters": [5, 8, 10, 11, 15, 19, 20],
    },
    "theme-locked-doors-and-hidden-things": {
        "name": "Locked Doors and Hidden Things",
        "description": "The manor is full of locked rooms, hidden children, and buried keys. The garden is locked; Colin is hidden; Craven's grief is sealed away. These chapters trace the unlocking — of doors, secrets, and hearts.",
        "for_parents": "Burnett uses locked doors as a metaphor for emotional suppression. Everything at Misselthwaite is hidden: Colin behind locked doors, the garden behind walls, Craven's grief behind travel. The story argues that locked things become sick things — healing requires opening up, letting air and light in. These chapters are valuable for discussing secrets, hiding, and the courage to open up.",
        "keywords": ["secrets", "locked", "hidden", "discovery", "opening", "walls"],
        "chapters": [5, 6, 7, 8, 9, 13, 26],
    },
    "theme-contrariness-as-strength": {
        "name": "Contrariness as Strength",
        "description": "Mary is 'quite contrary' — stubborn, demanding, and difficult. But these same traits drive her to find the garden, challenge Colin's self-pity, and refuse to accept lies. Burnett argues that difficult children have power they haven't learned to use well.",
        "for_parents": "This is one of the book's most radical messages: 'difficult' traits are not simply bad. Mary's stubbornness makes her a detective, a gardener, and a healer. Colin's fierce will, once redirected from fear to life, makes him strong. If you have a contrary child, this book validates their intensity while showing how it can be channeled toward good.",
        "keywords": ["stubborn", "contrary", "difficult", "will", "strength", "transformation"],
        "chapters": [2, 4, 6, 14, 16, 17],
    },
    "theme-the-magic": {
        "name": "The Magic",
        "description": "Colin's name for the life force he feels rising in the garden — the sun, the spring, the growing things, the power of belief. These chapters explore Burnett's philosophy that positive thought and connection to nature can heal body and spirit.",
        "for_parents": "Burnett was deeply influenced by New Thought philosophy — the idea that consciousness shapes reality. Colin's 'Magic' is her version of this for children. You don't have to accept the philosophy literally to appreciate the story's truth: believing in your own recovery matters, optimism has real effects, and connecting to living things changes us. These chapters invite philosophical conversations with older children.",
        "keywords": ["magic", "belief", "life-force", "affirmation", "healing", "positive-thinking"],
        "chapters": [19, 20, 22, 23, 24],
    },
    "theme-broken-families-mended": {
        "name": "Broken Families, Mended",
        "description": "Every family in The Secret Garden is broken — Mary's neglectful parents, Colin's absent father, the dead mother at the center. But the Sowerby family, whole and warm, shows what love looks like. The story traces the mending of the Craven family through the garden's healing power.",
        "for_parents": "The Secret Garden is fundamentally about what happens to children when families fail — and how they can heal. Mary's parents ignored her; Colin's father fled from him; Mrs. Craven died. The Sowerby family provides the model of healthy family life. The ending — Colin running into his father's arms — is a reunion made possible by the garden's work. These chapters are powerful for families working through their own difficulties.",
        "keywords": ["family", "grief", "neglect", "reunion", "healing", "mothering"],
        "chapters": [1, 9, 12, 24, 25, 26, 27],
    },
}


def read_and_strip_gutenberg(filepath):
    """Read the seed text and strip Gutenberg header/footer."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE SECRET GARDEN ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE SECRET GARDEN ***"
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


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


def split_into_chapters(text):
    """Split the full text into chapters.

    The Secret Garden uses: CHAPTER I.\nTITLE or CHAPTER V\nTITLE
    """
    chapter_pattern = re.compile(
        r'^CHAPTER\s+((?:X{0,3})(?:IX|IV|V?I{0,3}))\.?\s*\n([^\n]+)',
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

        # Clean up extra blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)

        chapters[chapter_num] = content

    return chapters


def get_chapter_keywords(chapter_num):
    """Return keywords for a chapter."""
    keywords_map = {
        1: ["mary-lennox", "india", "cholera", "orphan", "alone"],
        2: ["mary", "mrs-medlock", "misselthwaite", "moor", "uncle"],
        3: ["moor", "journey", "manor", "arrival", "lonely"],
        4: ["martha", "yorkshire", "dickon", "garden", "curiosity"],
        5: ["robin", "ben-weatherstaff", "outdoors", "crying", "mystery"],
        6: ["crying", "investigation", "stubborn", "corridors", "secret"],
        7: ["key", "robin", "discovery", "buried", "garden"],
        8: ["secret-garden", "door", "ivy", "roses", "wonder"],
        9: ["manor", "rooms", "colin", "discovery", "hidden-child"],
        10: ["dickon", "moor", "animals", "gardening", "friendship"],
        11: ["garden", "planting", "robin", "growth", "healing"],
        12: ["archibald-craven", "bit-of-earth", "permission", "grief"],
        13: ["colin", "night", "conversation", "fear", "loneliness"],
        14: ["colin", "rajah", "conflict", "stubbornness", "challenge"],
        15: ["spring", "seeds", "garden", "life", "growth"],
        16: ["argument", "honesty", "truth", "backbone", "courage"],
        17: ["tantrum", "fear", "breakthrough", "healing", "catharsis"],
        18: ["dickon", "animals", "colin", "outdoors", "desire"],
        19: ["spring", "outside", "wheelchair", "sky", "awakening"],
        20: ["standing", "magic", "affirmation", "healing", "belief"],
        21: ["ben-weatherstaff", "roses", "secret", "devotion", "wall"],
        22: ["exercise", "experiment", "strength", "practice", "health"],
        23: ["magic", "philosophy", "life-force", "ceremony", "belief"],
        24: ["susan-sowerby", "mother", "secret", "blessing", "deception"],
        25: ["craven", "dream", "return", "journey", "grief"],
        26: ["reunion", "running", "father", "son", "joy"],
        27: ["finale", "manor", "miracle", "public", "transformation"],
    }
    return keywords_map.get(chapter_num, [])


def build_grammar():
    """Build the complete Secret Garden grammar."""
    text = read_and_strip_gutenberg(SEED_FILE)
    chapters = split_into_chapters(text)

    if len(chapters) != 27:
        print(f"WARNING: Expected 27 chapters, found {len(chapters)}: {sorted(chapters.keys())}")

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
            "About": "The complete narrative of The Secret Garden: two damaged children and a hidden garden heal each other. Twenty-seven chapters trace Mary Lennox's arrival at Misselthwaite Manor, her discovery of the locked garden, her friendship with Dickon and Colin, and the miraculous return of health, hope, and family. Burnett's masterpiece argues that nature, honesty, and connection can mend what neglect and grief have broken.",
            "For Parents": "The Secret Garden is one of the most psychologically sophisticated children's novels ever written. Published in 1911, it anticipates modern understanding of childhood trauma, the healing power of nature, and the damage done by emotional neglect. Read it with your children and let the garden metaphor work on you too — we all have locked doors, buried keys, and dormant roses waiting for spring.",
        },
        "keywords": ["complete-story", "narrative", "chapters"],
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
            "About": "The great themes of The Secret Garden — healing through nature, locked doors and hidden things, contrariness as strength, the Magic, and broken families mended. These groupings reveal how Burnett weaves together physical healing, emotional growth, and spiritual awakening into a single story.",
            "For Parents": "These thematic groupings help you explore the novel beyond the plot. Each theme connects chapters that share a common thread. If your child is drawn to the garden scenes, explore 'Healing Through Nature.' If they're fascinated by Colin, 'The Magic' and 'Contrariness as Strength' offer different lenses. The story rewards re-reading from every angle.",
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
                    "date": "1911",
                    "note": "Original author of The Secret Garden",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "1994",
                    "note": "eBook #113",
                },
                {
                    "name": "PlayfulProcess",
                    "date": "2026-03-04",
                    "note": "Grammar construction, chapter summaries, and thematic groupings",
                },
            ],
        },
        "name": "The Secret Garden",
        "description": (
            "Frances Hodgson Burnett's The Secret Garden (1911) — the story of Mary Lennox, "
            "a disagreeable orphan who discovers a locked garden on the Yorkshire moors and, "
            "in bringing it back to life, heals herself, a hidden invalid boy, and a broken family. "
            "One of the most beloved children's novels ever written, exploring healing through nature, "
            "the power of fresh air and growing things, and the magic of believing in life.\n\n"
            "Source: Project Gutenberg eBook #113 (https://www.gutenberg.org/ebooks/113).\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES:\n"
            "- Maria Louise Kirk (1911, Frederick A. Stokes) — original American edition illustrator, "
            "beautiful color plates of Mary in the garden, Dickon with animals, Colin in his wheelchair\n"
            "- Charles Robinson (1911, Heinemann) — original British edition illustrator, "
            "delicate pen-and-ink drawings with Art Nouveau styling\n"
            "- Jessie Willcox Smith (early 20th century) — celebrated children's illustrator whose style "
            "perfectly suits Burnett's world"
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "children",
            "classic",
            "nature",
            "healing",
            "garden",
            "public-domain",
            "frances-hodgson-burnett",
            "full-text",
            "chapters",
            "multi-level",
            "victorian",
        ],
        "roots": ["wonder-imagination"],
        "shelves": ["children"],
        "lineages": ["Shrei"],
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
