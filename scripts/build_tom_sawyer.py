#!/usr/bin/env python3
"""
Build grammar.json for The Adventures of Tom Sawyer by Mark Twain.

Source: Project Gutenberg eBook #74
Structure: 35 chapters + Preface + Conclusion
Levels:
  L1: Individual chapters
  L2: Story arcs + thematic groups (with composite_of referencing L1)
  L3: Meta-categories
"""

import json
import re
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "seeds" / "tom-sawyer.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "tom-sawyer"
OUTPUT_FILE = OUTPUT_DIR / "grammar.json"


def roman_to_int(s):
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and values.get(c, 0) < values.get(s[i + 1], 0):
            result -= values[c]
        else:
            result += values[c]
    return result


CHAPTER_TITLES = {
    1: "Tom and Aunt Polly",
    2: "The Whitewashing of the Fence",
    3: "Tom the General",
    4: "Sunday School",
    5: "The Pinch-Bug in Church",
    6: "Tom Meets Becky Thatcher",
    7: "The Engaged Couple",
    8: "Tom in the Wilderness",
    9: "The Graveyard at Midnight",
    10: "The Solemn Oath",
    11: "Muff Potter in Trouble",
    12: "The Cat and the Pain-Killer",
    13: "The Pirates Set Sail",
    14: "Life on Jackson's Island",
    15: "Tom Sneaks Home",
    16: "The Pirates' Camp",
    17: "The Funeral",
    18: "Tom's Dream",
    19: "Tom Tells the Truth",
    20: "Tom Takes Becky's Punishment",
    21: "Examination Day",
    22: "Summer Miseries",
    23: "Muff Potter's Trial",
    24: "Tom the Hero",
    25: "Treasure Hunting",
    26: "The Haunted House",
    27: "Tracking the Gold",
    28: "In the Lair of Injun Joe",
    29: "The Picnic and Huck's Vigil",
    30: "Tom and Becky Lost",
    31: "Lost in the Cave",
    32: "Rescue",
    33: "The Fate of Injun Joe",
    34: "The Treasure Found",
    35: "Respectable Huck",
}

CHAPTER_SUMMARIES = {
    1: "We meet Tom Sawyer, a mischievous orphan living with his Aunt Polly in St. Petersburg, Missouri. Tom plays hooky, gets in a fight with a new boy in town, and sneaks home late through the window.",
    2: "The most famous scene in American literature: Aunt Polly punishes Tom by making him whitewash a fence on Saturday. Tom cons his friends into doing the work for him by pretending it's a privilege -- and they pay him for the honor.",
    3: "Tom leads the boys in mock battles, discovers the new girl (Becky Thatcher), and falls instantly in love. He shows off outside her house and goes to bed 'full of admiration for her.'",
    4: "Tom trades the loot from the whitewashing scheme for Sunday School tickets, then cashes them in for a prize Bible -- but is humiliated when he can't name the first two disciples.",
    5: "In church, Tom plays with a pinch-bug (beetle). A stray poodle sits on it and goes yelping up the aisle. The congregation tries not to laugh. Tom considers it 'a pretty good Sunday.'",
    6: "Tom meets Becky Thatcher at school. He pretends to be sick to avoid school (Aunt Polly extracts a loose tooth instead). On the way he meets Huckleberry Finn, the town outcast, and they agree to meet at midnight.",
    7: "Tom and Becky become 'engaged.' But Tom accidentally mentions his previous 'engagement' to Amy Lawrence, and Becky bursts into tears. Tom's day is ruined.",
    8: "Heartbroken, Tom runs into the woods and imagines becoming a pirate, a soldier, or an Indian chief. He wishes he could die 'temporarily' so everyone would be sorry.",
    9: "At midnight, Tom and Huck sneak to the graveyard to test a dead-cat cure for warts. They witness Injun Joe murder Dr. Robinson and frame Muff Potter. The boys are terrified.",
    10: "Tom and Huck swear a blood oath never to reveal what they saw. Tom is tormented by guilt. Muff Potter is arrested and the boys believe they are damned.",
    11: "Muff Potter languishes in jail. Tom and Huck bring him small comforts through the jail window. Tom's conscience gnaws at him relentlessly.",
    12: "Tom mopes and Aunt Polly doses him with quack remedies. Tom gives the Pain-Killer to the cat, Peter, who goes wild. Aunt Polly recognizes her own cruelty in Tom's treatment of the cat.",
    13: "Tom, Huck, and Joe Harper run away to Jackson's Island to become pirates. They raft across the Mississippi and camp on the island, free and happy under the stars.",
    14: "Life on the island: swimming, fishing, exploring, and feasting. The boys hear the cannon being fired on the river and realize the town thinks they've drowned. Tom sneaks back to spy.",
    15: "Tom crosses the river at night and hides under Aunt Polly's bed. He overhears the family mourning him and planning the funeral. He kisses Aunt Polly in her sleep and returns to the island.",
    16: "The pirates grow homesick. Tom's secret keeps them on the island. They learn to smoke (and get sick). A great storm terrifies them.",
    17: "The three boys appear at their own funeral, walking up the church aisle as the congregation sings their hymn. 'It was the proudest moment of Tom Sawyer's whole life.'",
    18: "After the funeral triumph, Tom tries to win back Becky by claiming he dreamed about the family while on the island. Aunt Polly discovers he actually sneaked home and is hurt by the deception.",
    19: "Tom tells Aunt Polly the truth about his midnight visit and the bark letter he left (but didn't deliver). She is moved by his imperfect love.",
    20: "Becky accidentally tears the schoolmaster's anatomy book and faces punishment. Tom takes the blame and the whipping. Becky's gratitude restores their bond.",
    21: "Examination Day at school. The scholars recite badly. The schoolmaster tries to draw on the blackboard while a cat lowers from the attic and snatches his wig. The boys have their revenge.",
    22: "Summer comes. Tom gets measles and is bedridden for weeks. He recovers to find a religious revival has swept the town and reformed all his friends -- but the revival passes.",
    23: "Muff Potter's trial. The town is certain of his guilt. Tom, overcome by conscience, takes the stand and names Injun Joe as the killer. Injun Joe leaps through the courtroom window and escapes.",
    24: "Tom is the village hero. But Injun Joe has disappeared, and Tom lives in terror that he'll return for revenge. His nightmares are vivid and constant.",
    25: "Tom and Huck search for buried treasure in haunted houses and under dead trees. They discuss what they'd do with treasure and the rules of treasure-hunting.",
    26: "In the haunted house, Tom and Huck hide upstairs while Injun Joe (disguised as a deaf-mute Spaniard) and a partner discover a box of gold hidden under the floorboards. Injun Joe takes the gold to his 'Number Two' hideout.",
    27: "Tom and Huck try to track Injun Joe's gold to 'Number Two.' Huck stakes out the tavern where Joe has been spotted.",
    28: "Tom and Huck break into the room at the tavern but find Injun Joe passed out drunk on the floor. They flee in terror.",
    29: "The town picnic takes Tom and Becky to McDougal's Cave. Huck follows Injun Joe and his partner through the dark streets, overhears their plan to attack the Widow Douglas, and runs to the Welshman's house for help.",
    30: "Huck's warning saves the Widow Douglas. Meanwhile, Tom and Becky are discovered to be missing from the picnic -- they've been lost in the cave all night.",
    31: "Tom and Becky wander deeper into McDougal's Cave, lost and terrified. Their candles burn out. Tom finds a way while exploring side passages -- and sees Injun Joe hiding in the cave.",
    32: "Tom finds an exit near the river. He and Becky are rescued. The town celebrates. Judge Thatcher seals the cave entrance -- not knowing Injun Joe is inside.",
    33: "Injun Joe is found dead behind the sealed cave door, starved. Tom and Huck return to the cave and find the treasure -- over twelve thousand dollars in gold.",
    34: "The treasure is revealed at a party for Huck at the Widow Douglas's house. The whole town is astonished. Tom and Huck are rich.",
    35: "The Widow Douglas takes Huck in to 'civilize' him. Huck can't stand it and runs away. Tom convinces him to come back by promising he can join Tom Sawyer's Gang of robbers -- but only if he's respectable.",
}

CHAPTER_KEYWORDS = {
    1: ["tom", "aunt-polly", "mischief", "fence", "introduction"],
    2: ["whitewashing", "fence", "cunning", "psychology", "labor"],
    3: ["war-games", "becky-thatcher", "love", "showing-off"],
    4: ["sunday-school", "tickets", "bible", "fraud", "humiliation"],
    5: ["church", "pinch-bug", "poodle", "boredom", "comedy"],
    6: ["becky-thatcher", "huck-finn", "school", "tooth", "meeting"],
    7: ["engagement", "becky", "amy-lawrence", "jealousy", "heartbreak"],
    8: ["wilderness", "fantasy", "pirate", "melancholy", "solitude"],
    9: ["graveyard", "murder", "injun-joe", "muff-potter", "midnight"],
    10: ["oath", "blood", "guilt", "secrecy", "conscience"],
    11: ["muff-potter", "jail", "guilt", "conscience", "kindness"],
    12: ["pain-killer", "cat", "aunt-polly", "medicine", "comedy"],
    13: ["pirates", "jackson-island", "mississippi", "freedom", "escape"],
    14: ["island", "swimming", "fishing", "cannon", "drowning"],
    15: ["sneaking-home", "aunt-polly", "funeral", "eavesdropping"],
    16: ["homesickness", "smoking", "storm", "island", "secret"],
    17: ["funeral", "church", "resurrection", "pride", "triumph"],
    18: ["dream", "deception", "aunt-polly", "love", "guilt"],
    19: ["truth", "bark-letter", "aunt-polly", "forgiveness"],
    20: ["becky", "anatomy-book", "punishment", "nobility", "sacrifice"],
    21: ["examination", "school", "revenge", "wig", "cat", "comedy"],
    22: ["summer", "measles", "revival", "religion", "boredom"],
    23: ["trial", "muff-potter", "injun-joe", "testimony", "courage"],
    24: ["hero", "fear", "injun-joe", "nightmares", "fame"],
    25: ["treasure", "digging", "haunted-house", "adventure"],
    26: ["haunted-house", "injun-joe", "gold", "hiding", "terror"],
    27: ["tracking", "number-two", "tavern", "detective"],
    28: ["tavern", "injun-joe", "drunk", "escape", "fear"],
    29: ["picnic", "cave", "huck", "injun-joe", "widow-douglas"],
    30: ["lost", "cave", "becky", "despair", "search"],
    31: ["cave", "darkness", "candles", "injun-joe", "discovery"],
    32: ["rescue", "cave", "exit", "celebration", "sealed"],
    33: ["injun-joe", "death", "cave", "treasure", "gold"],
    34: ["treasure", "party", "widow-douglas", "revelation", "wealth"],
    35: ["huck", "civilization", "widow-douglas", "respectability", "ending"],
}

CHAPTER_REFLECTIONS = {
    1: "Tom is punished but never really reformed. Do punishments actually change behavior? What works better?",
    2: "Tom convinces other boys that whitewashing is fun. Is that clever or dishonest? Where's the line between persuasion and manipulation?",
    3: "Tom falls in love at first sight. Have you ever felt that instant connection with someone? What happened?",
    4: "Tom cheats to win a Bible but can't answer simple questions. When have you pretended to know something you didn't?",
    5: "The whole church struggles not to laugh. Why is it so hard not to laugh when you're supposed to be serious?",
    6: "Tom meets Huck Finn, who every boy envies because he doesn't have to go to school or obey anyone. What would real freedom like Huck's actually feel like?",
    7: "Tom accidentally reveals his past 'engagement' and ruins everything with Becky. When has the truth come out at the worst possible moment?",
    8: "Tom fantasizes about dying so everyone will be sorry. Have you ever wished people would miss you more? What were you really asking for?",
    9: "Tom and Huck witness a murder and are paralyzed with fear. What would you do if you saw something terrible that you were afraid to report?",
    10: "The boys swear a blood oath of secrecy. When is keeping a secret the right thing to do, and when does it become wrong?",
    11: "Tom brings comfort to Muff Potter in jail even though he can't tell the truth yet. Is small kindness enough when you could do more?",
    12: "Tom gives the cat pain-killer and Aunt Polly realizes she's been doing the same thing to Tom. When have you seen yourself in someone else's behavior?",
    13: "The boys run away to be pirates. Why is running away so appealing? What are they really running from?",
    14: "On the island, the boys hear their own funeral cannon. What would it feel like to know everyone thinks you're dead?",
    15: "Tom sneaks home and watches his family grieve. He's moved but doesn't reveal himself. Why not? What's he getting from their grief?",
    16: "The boys get sick from smoking. Why do people keep trying things they know are bad for them?",
    17: "The boys walk into their own funeral. It's Tom's greatest triumph. Is it also his cruelest trick?",
    18: "Tom lies about the dream and is caught. Why is it so tempting to improve on the truth?",
    19: "Tom finally tells Aunt Polly the truth. What makes truth-telling so hard, and what makes it worth it?",
    20: "Tom takes a whipping to protect Becky. What's the difference between this sacrifice and his earlier showing-off?",
    21: "The boys get revenge on the schoolmaster with the cat and wig trick. When is revenge satisfying, and when does it go too far?",
    22: "The religious revival reforms everyone temporarily. Why don't the changes last? What does lasting change require?",
    23: "Tom finally tells the truth about the murder. What gave him the courage? What was the cost?",
    24: "Tom is a hero but lives in fear of Injun Joe. Is it possible to be brave and terrified at the same time?",
    25: "Tom and Huck hunt for treasure with absolute confidence they'll find it. Where does that kind of faith come from?",
    26: "The boys accidentally stumble on real treasure and real danger. When has something that started as play become suddenly serious?",
    27: "Tom and Huck become detectives. When does the adventure stop being fun and start being dangerous?",
    28: "The boys find Injun Joe but are too afraid to act. Is freezing in fear a failure or just being human?",
    29: "Huck overcomes his fear to save the Widow Douglas. What makes someone act when they're terrified?",
    30: "Tom and Becky are lost in the cave and no one knows. What is the scariest situation you can imagine being in?",
    31: "In total darkness, Tom keeps exploring while Becky gives up. Where does his determination come from?",
    32: "Tom finds a way out. The relief of rescue after real danger is one of life's most powerful feelings. When have you been rescued?",
    33: "Injun Joe dies sealed in the cave. Even a villain's death is pitiful. Can you feel sorry for someone who's done terrible things?",
    34: "Tom and Huck find the treasure. After all the danger, was it worth it?",
    35: "Huck can't stand being 'civilized' and runs away. Can a person be forced to change? Should they be?",
}

STORY_ARCS = {
    "arc-village-life": {
        "name": "Village Life and Childhood Schemes",
        "chapters": [1, 2, 3, 4, 5, 6, 7, 8],
        "about": "The first eight chapters establish Tom Sawyer's world: the drowsy Mississippi River town of St. Petersburg, Aunt Polly's household, the schoolroom, the church, and the social order of childhood. Tom whitewashes the fence, cons Sunday School, meets Becky Thatcher, and begins to dream of escape. These chapters are pure comedy, but they lay the groundwork for everything that follows.",
        "for_parents": "Twain's genius in these opening chapters is making childhood simultaneously hilarious and recognizable. Tom's manipulation of the fence-painting boys is a masterclass in psychology. His humiliation at Sunday School is every child's nightmare. His instant love for Becky is pitch-perfect. Read these chapters aloud -- Twain's rhythm and timing are best experienced through the voice.",
        "keywords": ["village-life", "schemes", "comedy", "childhood", "becky", "school"],
    },
    "arc-graveyard-and-guilt": {
        "name": "The Graveyard and the Burden of Guilt",
        "chapters": [9, 10, 11, 12],
        "about": "The story darkens. Tom and Huck witness a murder in the graveyard and are bound by blood oath to silence. Muff Potter is falsely accused. Tom's guilt eats at him -- he can't sleep, can't enjoy life, sees the murdered man in his dreams. Aunt Polly's patent medicines and the Pain-Killer cat scene provide comic relief, but the guilt remains.",
        "for_parents": "This is where Tom Sawyer becomes more than a comedy. The moral burden of witnessing injustice and staying silent is real and heavy. Tom is a child carrying an adult's dilemma. These chapters are powerful for talking about moral courage, the cost of silence, and the difference between a promise that should be kept and one that shouldn't.",
        "keywords": ["murder", "guilt", "oath", "injustice", "silence", "conscience"],
    },
    "arc-jackson-island": {
        "name": "Jackson's Island and the Pirate Life",
        "chapters": [13, 14, 15, 16, 17],
        "about": "The great escape: Tom, Huck, and Joe Harper flee to Jackson's Island and live as pirates. Swimming, fishing, storms, and the delicious guilt of letting the town think they're dead. Tom sneaks home and overhears his own funeral plans. The climax: the three boys walk into their own funeral service. It is Tom Sawyer's finest hour -- and his most self-serving.",
        "for_parents": "The Jackson's Island sequence is the heart of the book's celebration of boyhood freedom. But Twain is sharp-eyed: Tom's 'resurrection' at the funeral is both triumphant and cruel. He let Aunt Polly grieve for days. The tension between Tom's genuine love for his aunt and his appetite for drama is one of the book's deepest themes. Ask your child: 'Was the funeral trick funny or mean?'",
        "keywords": ["pirates", "island", "freedom", "mississippi", "funeral", "resurrection"],
    },
    "arc-becky-and-school": {
        "name": "Tom and Becky",
        "chapters": [18, 19, 20, 21, 22],
        "about": "The aftermath of the pirate adventure: Tom's relationship with Aunt Polly is strained by his deception. He takes a whipping to protect Becky from the schoolmaster's wrath. Examination Day brings the boys' revenge on the schoolmaster. Summer arrives with measles and a religious revival that transforms and then releases the town.",
        "for_parents": "Chapter 20, where Tom takes Becky's punishment, is a turning point in his character. For the first time, he sacrifices something for someone else without an audience to admire him. This is genuine growth, even if Tom doesn't recognize it himself. The religious revival chapter is one of Twain's most satirical -- a preview of the deeper social criticism in Huckleberry Finn.",
        "keywords": ["becky", "school", "sacrifice", "summer", "revival", "growth"],
    },
    "arc-trial-and-testimony": {
        "name": "The Trial of Muff Potter",
        "chapters": [23, 24],
        "about": "The moral climax: Muff Potter stands trial for murder, and the whole town believes he's guilty. Tom, tormented past endurance, takes the witness stand and names Injun Joe as the killer. Joe escapes through the window. Tom is a hero, but Injun Joe is free -- and Tom knows he'll want revenge.",
        "for_parents": "Tom's testimony is the book's single bravest act. After weeks of torment, he does the right thing knowing it puts his life in danger. This is genuine moral courage -- not showing off, not scheming, but standing up for truth when it's terrifying. The contrast with his earlier antics is striking. Tom is growing up, whether he knows it or not.",
        "keywords": ["trial", "testimony", "courage", "justice", "injun-joe", "danger"],
    },
    "arc-treasure-and-cave": {
        "name": "The Treasure Hunt and the Cave",
        "chapters": [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],
        "about": "The grand adventure: treasure hunting in haunted houses, tracking Injun Joe through dark streets, the picnic at McDougal's Cave, Huck's heroic warning to save the Widow Douglas, Tom and Becky lost in the cave in total darkness, the discovery of Injun Joe hiding underground, the desperate escape, the discovery of twelve thousand dollars in gold, and Huck's reluctant adoption into respectability.",
        "for_parents": "The final act combines adventure, real danger, and moral resolution. Huck's decision to warn the Welshman about Injun Joe's plot against the Widow Douglas is his own moment of moral courage -- parallel to Tom's testimony at the trial. The cave sequence is genuinely terrifying and shows Tom at his most resourceful. Injun Joe's death -- starving behind a sealed door -- is haunting and raises hard questions about justice versus cruelty. The ending is deliberately ambiguous: is Huck's 'civilization' a rescue or a trap?",
        "keywords": ["treasure", "cave", "injun-joe", "danger", "gold", "huck", "civilization"],
    },
}

THEMATIC_GROUPS = {
    "theme-conscience-and-courage": {
        "name": "Conscience and Moral Courage",
        "chapters": [9, 10, 11, 20, 23, 24, 29],
        "about": "The moral spine of the novel: Tom's struggle with the knowledge of Injun Joe's crime, his guilt about Muff Potter, his decision to testify at the trial, and his willingness to take punishment for Becky. Huck's parallel journey -- overcoming fear to save the Widow Douglas. Twain shows that real courage is not the absence of fear but action in its presence.",
        "for_parents": "Tom Sawyer is often thought of as a book about boyhood fun, but its moral architecture is serious. Tom's guilt about Muff Potter builds slowly across multiple chapters. When he finally acts, it costs him -- Injun Joe becomes his nemesis. The message is clear: doing the right thing is hard, dangerous, and often unrewarded in the short term. But it's the only thing that lets you sleep at night.",
        "keywords": ["conscience", "courage", "testimony", "sacrifice", "right-thing"],
    },
    "theme-freedom-and-rebellion": {
        "name": "Freedom and Rebellion",
        "chapters": [6, 8, 13, 14, 16, 35],
        "about": "Tom dreams of being a pirate. Huck lives outside society entirely. The Jackson's Island adventure is a trial run of absolute freedom. But freedom has limits -- the boys get homesick, the storm is frightening, and Huck's freedom comes with hunger and loneliness. Twain celebrates the dream of freedom while honestly showing its costs.",
        "for_parents": "Every child dreams of running away, and Twain takes that dream seriously. He lets the boys live it fully -- and then shows what happens. They miss their beds, their families, their regular meals. Huck, who has the freedom every boy envies, is the loneliest character in the book. The final chapter, where Huck can't stand being 'civilized,' asks the deepest question: Is respectability worth having if it kills your spirit?",
        "keywords": ["freedom", "piracy", "rebellion", "huck", "island", "civilization"],
    },
    "theme-performance-and-identity": {
        "name": "Performance and Identity",
        "chapters": [2, 3, 4, 7, 17, 18, 21],
        "about": "Tom is always performing -- whitewashing the fence as an art form, showing off for Becky, staging his own funeral. Twain shows a boy who constructs his identity through performance. But the performances reveal genuine qualities: Tom's cleverness, his need to be seen, his desperate desire to matter. The gap between who Tom performs and who he really is narrows as the book progresses.",
        "for_parents": "Social media has made performance anxiety universal, but Twain understood it in 1876. Tom's whitewashing con is Instagram before Instagram -- turning labor into content, making others envy what is actually a punishment. These chapters are wonderful for talking about authenticity, showing off, and the difference between being admired and being truly known.",
        "keywords": ["performance", "identity", "showing-off", "whitewashing", "funeral", "deception"],
    },
    "theme-superstition-and-imagination": {
        "name": "Superstition, Imagination, and Play",
        "chapters": [6, 8, 9, 25, 26],
        "about": "Dead cats cure warts. Treasure is found by digging under dead trees at midnight. Haunted houses contain real ghosts -- and real villains. Twain fills the book with the superstitions and fantasies of childhood, treating them with affectionate humor. Tom and Huck live in a world where imagination and reality blur constantly -- and sometimes the imaginary world turns out to be more right than wrong.",
        "for_parents": "Twain's treatment of childhood superstition is both humorous and respectful. The boys' beliefs are 'wrong' by adult standards, but their dead-cat expedition leads to witnessing a real murder. Their treasure hunt leads to real gold. Twain suggests that the imaginative life of childhood, however foolish it appears, has its own kind of wisdom. A wonderful thread for celebrating children's imaginations while gently testing their beliefs.",
        "keywords": ["superstition", "imagination", "dead-cat", "treasure", "haunted-house", "play"],
    },
}


def read_and_strip_gutenberg(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE ADVENTURES OF TOM SAWYER, COMPLETE ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE ADVENTURES OF TOM SAWYER, COMPLETE ***"
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def extract_preface(text):
    """Extract Twain's preface."""
    # Look for the PREFACE section
    preface_match = re.search(r'\nPREFACE\n', text)
    if not preface_match:
        return ""
    start = preface_match.end()
    # End at CHAPTER I or next major section
    ch1_match = re.search(r'\nCHAPTER I\b', text[start:])
    if ch1_match:
        preface = text[start:start + ch1_match.start()]
    else:
        preface = text[start:start + 2000]
    return preface.strip()


def extract_conclusion(text):
    """Extract Twain's conclusion."""
    concl_match = re.search(r'\nCONCLUSION\n', text)
    if not concl_match:
        return ""
    return text[concl_match.end():].strip()


def split_into_chapters(text):
    """Split text into chapters. Format: CHAPTER I, CHAPTER II, etc."""
    # Find chapter markers in the body text (not TOC)
    # The body chapters come after the illustrations list / front matter
    # Body chapters start with CHAPTER on its own (no period or descriptive text after)
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC]+)\s*$', re.MULTILINE)

    matches = list(chapter_pattern.finditer(text))

    # The TOC also has CHAPTER entries, but those are followed by descriptive text on the same line
    # Filter to only the standalone CHAPTER lines that are after the front matter
    # We can use the PREFACE or HARTFORD as a landmark
    body_start = 0
    hartford = text.find("HARTFORD")
    if hartford != -1:
        body_start = hartford

    body_matches = [m for m in matches if m.start() > body_start]

    chapters = {}
    for i, match in enumerate(body_matches):
        roman = match.group(1)
        chapter_num = roman_to_int(roman)
        start = match.end()
        end = body_matches[i + 1].start() if i + 1 < len(body_matches) else len(text)
        content = text[start:end].strip()

        # Remove CONCLUSION from last chapter
        concl_idx = content.rfind('\nCONCLUSION\n')
        if concl_idx != -1:
            content = content[:concl_idx].strip()

        content = re.sub(r'\n{4,}', '\n\n\n', content)
        chapters[chapter_num] = content

    return chapters


def build_grammar():
    text = read_and_strip_gutenberg(SEED_FILE)
    preface_text = extract_preface(text)
    conclusion_text = extract_conclusion(text)
    chapters = split_into_chapters(text)

    items = []
    sort_order = 0
    chapter_id_map = {}

    # === L1: Preface ===
    if preface_text:
        sort_order += 1
        items.append({
            "id": "preface",
            "name": "Preface",
            "sort_order": sort_order,
            "category": "preface",
            "level": 1,
            "sections": {
                "Story": preface_text,
                "About": "Twain's brief preface, stating that the characters are drawn from real people and that most of the adventures really occurred. He notes that the book is 'intended mainly for the entertainment of boys and girls' but hopes adults will enjoy it too.",
                "Reflection": "Twain says this story is based on real people and real adventures. What stories from your own childhood might someone tell as a novel?",
            },
            "keywords": ["preface", "twain", "autobiography", "childhood"],
            "metadata": {},
        })

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

    # === L1: Conclusion ===
    if conclusion_text:
        sort_order += 1
        items.append({
            "id": "conclusion",
            "name": "Conclusion",
            "sort_order": sort_order,
            "category": "conclusion",
            "level": 1,
            "sections": {
                "Story": conclusion_text,
                "About": "Twain's brief conclusion, noting that the story must stop here because it's 'strictly a history of a boy' and going further would make it 'the history of a man.' He hints at a sequel following the characters into adulthood.",
                "Reflection": "Twain says the story of a boy must stop here. What does it mean to cross the line from boy to man, from girl to woman? When does childhood end?",
            },
            "keywords": ["conclusion", "ending", "boyhood", "growing-up"],
            "metadata": {},
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
            "About": "The complete narrative of The Adventures of Tom Sawyer in six movements: village life and childhood schemes, the graveyard murder and the burden of guilt, the pirate adventure on Jackson's Island, Tom and Becky's relationship, the trial of Muff Potter, and the treasure hunt in the cave. Thirty-five chapters tracing a summer in the life of a boy in a Mississippi River town before the Civil War.",
            "For Parents": "The Adventures of Tom Sawyer (1876) is often read as a nostalgic comedy, but Twain packed it with moral complexity. Tom witnesses murder, grapples with conscience, risks his life for justice, and confronts real evil in Injun Joe. The book celebrates boyhood freedom while honestly showing its limits. It is also a product of its time: the character of Injun Joe reflects racial attitudes that demand critical discussion.\n\nNote on racial content: Twain's portrayal of Injun Joe draws on harmful stereotypes of Native Americans. The character is presented as the story's villain in ways that reflect 19th-century prejudices. This is an opportunity for important conversations about how stories can both entertain and perpetuate harmful ideas.",
        },
        "keywords": ["complete-story", "narrative", "chapters", "tom-sawyer"],
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
            "About": "The great themes of Tom Sawyer: conscience and moral courage, freedom and rebellion, performance and identity, and the strange power of superstition and imagination. These themes run through the entire novel, connecting the comedy of the early chapters to the genuine moral drama of the later ones.",
            "For Parents": "These thematic groupings help you explore Tom Sawyer beyond the plot. If your child is drawn to the whitewashing scene, follow the Performance and Identity thread. If they're disturbed by the graveyard murder, explore Conscience and Courage. If they love the Jackson's Island adventure, discuss Freedom and Rebellion. The book grows richer with each re-reading.",
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
                    "name": "Mark Twain (Samuel Langhorne Clemens)",
                    "date": "1876",
                    "note": "Author of The Adventures of Tom Sawyer",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2004",
                    "note": "eBook #74 — digitized text",
                },
                {
                    "name": "PlayfulProcess",
                    "date": "2026-03-04",
                    "note": "Grammar construction and thematic groupings",
                },
            ],
        },
        "name": "The Adventures of Tom Sawyer",
        "description": (
            "Mark Twain's The Adventures of Tom Sawyer (1876) -- the great American novel of boyhood. "
            "Tom Sawyer whitewashes a fence, falls in love, witnesses a murder, runs away to be a pirate, "
            "attends his own funeral, testifies at a murder trial, gets lost in a cave, and finds buried treasure -- "
            "all in one summer along the Mississippi River. Thirty-five chapters of comedy, adventure, and "
            "surprising moral depth.\n\n"
            "Source: Project Gutenberg eBook #74 (https://www.gutenberg.org/ebooks/74).\n\n"
            "Note on racial content: The character of Injun Joe reflects 19th-century racial stereotypes "
            "of Native Americans. Twain uses 'Injun' and presents the character through the lens of period "
            "prejudices. These elements require critical discussion, particularly with young readers.\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES:\n"
            "- True Williams (1876, American Publishing Company) -- original illustrator, over 160 "
            "pen-and-ink drawings capturing every scene of small-town Missouri life\n"
            "- E.W. Kemble (1884, Chatto & Windus) -- British edition illustrator\n"
            "- Worth Brehm (1910, Harper & Brothers) -- classic early 20th-century color plates\n"
            "- Norman Rockwell (1936, Heritage Press) -- iconic American realist illustrations"
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "children",
            "classic",
            "adventure",
            "comedy",
            "public-domain",
            "mark-twain",
            "tom-sawyer",
            "mississippi",
            "full-text",
            "chapters",
            "multi-level",
            "american",
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
