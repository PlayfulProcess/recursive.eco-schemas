#!/usr/bin/env python3
"""
Parse Plato's Republic (Gutenberg #1497, Jowett translation).
Extracts Introduction, Books I-X, L2 thematic groups, L3 meta item.
"""
import json, re, os

with open("seeds/republic-plato.txt", encoding="utf-8") as f:
    text = f.read()

# Strip Gutenberg header/footer
gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()
body_lines = body.split("\n")

def find_line(target):
    """Find line number where stripped line matches target."""
    for i, line in enumerate(body_lines):
        if line.strip() == target:
            return i
    return -1

def find_line_after(target, after_line):
    """Find line matching target, but only after a given line number."""
    for i in range(after_line, len(body_lines)):
        if body_lines[i].strip() == target:
            return i
    return -1

def extract_text(start_ln, end_ln):
    """Extract text between line numbers, skipping leading/trailing blanks."""
    content = []
    started = False
    for j in range(start_ln + 1, min(end_ln, len(body_lines))):
        line = body_lines[j]
        if not started and line.strip() == "":
            continue
        started = True
        content.append(line.rstrip())
    while content and content[-1].strip() == "":
        content.pop()
    return "\n".join(content)

def truncate(text, limit=2800):
    if len(text) > limit:
        bp = text.rfind(".", 0, limit)
        if bp == -1:
            bp = limit
        remaining = len(text[bp:].split())
        return text[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    return text

# ═══════════════════════════════════════════════════════════════════════════
# LOCATE SECTIONS
# ═══════════════════════════════════════════════════════════════════════════

# Find the second occurrence of "INTRODUCTION AND ANALYSIS." (first is TOC)
intro_toc = find_line("INTRODUCTION AND ANALYSIS.")
intro_body = find_line_after("INTRODUCTION AND ANALYSIS.", intro_toc + 1)
print(f"Introduction body at line {intro_body}")

# Find "PERSONS OF THE DIALOGUE." in the body (second occurrence, after TOC)
persons_toc = find_line("PERSONS OF THE DIALOGUE.")
persons_body = find_line_after("PERSONS OF THE DIALOGUE.", persons_toc + 1)
print(f"Persons of dialogue at line {persons_body}")

# Find all BOOK headings in the body (skip TOC lines 48-57)
# The body books start after "PERSONS OF THE DIALOGUE" section
book_headings = [
    ("BOOK I.", "book-1", "Book I: Justice as a Virtue"),
    ("BOOK II.", "book-2", "Book II: The Challenge of Glaucon"),
    ("BOOK III.", "book-3", "Book III: Education and Censorship"),
    ("BOOK IV.", "book-4", "Book IV: The Just City and the Just Soul"),
    ("BOOK V.", "book-5", "Book V: Philosopher Kings and the Community of Women"),
    ("BOOK VI.", "book-6", "Book VI: The Idea of the Good"),
    ("BOOK VII.", "book-7", "Book VII: The Allegory of the Cave"),
    ("BOOK VIII.", "book-8", "Book VIII: The Decline of the State"),
    ("BOOK IX.", "book-9", "Book IX: Tyranny and the Tyrannical Soul"),
    ("BOOK X.", "book-10", "Book X: The Allegory of Er and the Banishment of Poetry"),
]

# Keywords for each book
book_keywords = {
    "book-1": ["justice", "cephalus", "polemarchus", "thrasymachus", "virtue", "old-age", "might-makes-right"],
    "book-2": ["glaucon", "adeimantus", "ring-of-gyges", "social-contract", "origins-of-justice", "city-in-speech"],
    "book-3": ["education", "censorship", "music", "poetry", "guardian-class", "noble-lie", "mimesis"],
    "book-4": ["temperance", "courage", "wisdom", "justice", "tripartite-soul", "reason", "spirit", "appetite"],
    "book-5": ["philosopher-kings", "women-guardians", "communism", "equality", "knowledge-vs-opinion"],
    "book-6": ["idea-of-good", "sun-analogy", "divided-line", "dialectic", "forms", "philosopher-nature"],
    "book-7": ["allegory-of-cave", "education", "shadows", "enlightenment", "ascent", "dialectic", "mathematics"],
    "book-8": ["timocracy", "oligarchy", "democracy", "tyranny", "decline", "political-degeneration"],
    "book-9": ["tyrannical-soul", "pleasure", "happiness", "justice-pays", "three-proofs", "appetitive-soul"],
    "book-10": ["poetry", "mimesis", "banishment-of-poets", "allegory-of-er", "afterlife", "immortality", "reincarnation"],
}

# Themes for each book
book_themes = {
    "book-1": "The nature of justice is debated through three definitions: justice as honesty and paying debts (Cephalus), justice as helping friends and harming enemies (Polemarchus), and justice as the advantage of the stronger (Thrasymachus). Socrates refutes each, establishing that justice is a virtue of the soul.",
    "book-2": "Glaucon and Adeimantus challenge Socrates to prove that justice is good in itself, not merely for its consequences. The Ring of Gyges thought experiment asks: would a just person remain just if invisible? Socrates proposes building a city in speech to find justice writ large.",
    "book-3": "The education of the guardian class through music and gymnastics. Poetry that shows gods behaving badly must be censored. The noble lie — that citizens are born from the earth with gold, silver, or bronze natures — establishes the class system.",
    "book-4": "The ideal city exhibits four virtues: wisdom (in the rulers), courage (in the auxiliaries), temperance (harmony among all classes), and justice (each class performing its proper function). The soul mirrors the city with three parts: reason, spirit, and appetite.",
    "book-5": "Three controversial proposals: women should serve as guardians equal to men, families should be held in common, and philosophers must rule as kings. The distinction between knowledge and opinion grounds the philosopher's claim to rule.",
    "book-6": "The philosopher's nature and the Idea of the Good. The sun analogy: as the sun enables sight and gives life, the Good enables knowledge and gives being to the Forms. The Divided Line distinguishes four levels of cognition from imagination to dialectic.",
    "book-7": "The Allegory of the Cave: prisoners chained to see only shadows mistake them for reality. Liberation is painful — the freed prisoner must ascend from darkness to sunlight (the Good). Education is not filling empty vessels but turning the soul toward truth. The curriculum: arithmetic, geometry, astronomy, harmonics, dialectic.",
    "book-8": "Four degenerate forms of government, each arising from the corruption of its predecessor: timocracy (honor-loving), oligarchy (wealth-loving), democracy (freedom-loving), tyranny (the worst). Each political form corresponds to a soul type.",
    "book-9": "The tyrannical soul is the most wretched — enslaved by lawless appetites. Three proofs that the just person is happier than the unjust: the argument from the three soul types, the argument from true pleasure, and the mathematical argument.",
    "book-10": "Poetry is banished as thrice removed from truth (imitating imitations of Forms). The soul is immortal. The Allegory of Er: a soldier returns from death to describe the afterlife, where souls choose their next lives — a final argument that justice is rewarded cosmically.",
}

# Key passages for each book
book_key_passages = {
    "book-1": "\"Justice is nothing else than the interest of the stronger.\" — Thrasymachus\n\n\"The just man is not a man who does no wrong, but a man who does not wish to do wrong.\" — Socrates, refuting Thrasymachus",
    "book-2": "\"Allegory of the Ring of Gyges: Suppose now that there were two such magic rings, and the just put on one of them and the unjust the other... no man would keep his hands off what was not his own when he could safely take what he liked.\"\n\n\"Let us begin and create in idea a State; and yet the true creator is necessity, who is the mother of our invention.\"",
    "book-3": "\"Then the first thing will be to establish a censorship of the writers of fiction, and let the censors receive any tale of fiction which is good, and reject the bad.\"\n\n\"The guardian must be gentle to their own and cruel to enemies — how can we find a gentle nature which has also a great spirit?\"",
    "book-4": "\"Justice is when each part of the soul performs its proper function — reason rules, spirit supports reason, and appetite obeys.\"\n\n\"The soul of man is divided into three parts — the rational, the spirited, and the appetitive — just as the city has three classes.\"",
    "book-5": "\"Until philosophers are kings, or the kings and princes of this world have the spirit and power of philosophy... cities will never have rest from their evils — nor the human race.\"\n\n\"There is no practice of a city's rulers which belongs to woman because she is a woman, or to man because he is a man.\"",
    "book-6": "\"The idea of the good is the highest knowledge, and all other things become useful and advantageous only by their use of this.\"\n\n\"The sun gives to visible things the power of being seen and also their generation, growth, and nourishment. In like manner the good gives to the objects of knowledge their truth and to the knower his power of knowing.\"",
    "book-7": "\"Allegory of the Cave: Behold! human beings living in an underground den... they see only their own shadows, or the shadows of one another, which the fire throws on the opposite wall of the cave.\"\n\n\"Education is not what certain people declare it to be — putting knowledge into souls that lack it, like putting sight into blind eyes. The power to learn is present in everyone's soul.\"",
    "book-8": "\"Democracy passes into despotism. The excess of liberty, whether in States or individuals, seems only to pass into excess of slavery.\"\n\n\"Tyranny springs from democracy, just as democracy springs from oligarchy. The most aggravated form of tyranny arises out of the most extreme liberty.\"",
    "book-9": "\"The soul of the tyrannical man is always poor and unsatisfied, full of fear and distraction. He is the most wretched of all.\"\n\n\"The lover of wisdom alone has his myth of pleasure approved by reason — therefore the pleasure of the lover of wisdom is the truest pleasure.\"",
    "book-10": "\"The poet is an imitator, and therefore, like all other imitators, he is thrice removed from the king and from the truth.\"\n\n\"Allegory of Er: The soul of Odysseus, remembering his former toils, went about for a long time looking for the life of a private man who had no cares; he had some difficulty in finding this, lying about in a corner and neglected by everybody else.\"",
}

# Find body-section book lines (skip TOC by searching after persons_body)
book_positions = []
search_after = persons_body if persons_body > 0 else 8000
for heading, bid, bname in book_headings:
    ln = find_line_after(heading, search_after)
    if ln >= 0:
        book_positions.append((ln, heading, bid, bname))
        print(f"  {heading} at line {ln}")
    else:
        print(f"  WARNING: Could not find {heading}")

# ═══════════════════════════════════════════════════════════════════════════
# BUILD ITEMS
# ═══════════════════════════════════════════════════════════════════════════

items = []
sort_order = 1

# Item 1: Introduction and Analysis
intro_end = persons_body if persons_body > 0 else book_positions[0][0]
intro_text = extract_text(intro_body, intro_end)
intro_excerpt = truncate(intro_text)

items.append({
    "id": "introduction",
    "name": "Introduction and Analysis (Jowett)",
    "sort_order": sort_order,
    "category": "introduction",
    "level": 1,
    "sections": {
        "Analysis": intro_excerpt,
        "Themes": "Jowett's introduction surveys the Republic's central arguments: the nature of justice, the ideal state, the education of guardians, the theory of Forms, the philosopher-king, the tripartite soul, the critique of poetry, and the myth of Er. He places the Republic within Plato's broader philosophical project and traces its influence on Western political and ethical thought."
    },
    "keywords": ["jowett", "introduction", "analysis", "overview", "commentary"],
    "metadata": {}
})
sort_order += 1

# Items 2-11: Books I-X
for idx, (start_ln, heading, bid, bname) in enumerate(book_positions):
    end_ln = book_positions[idx+1][0] if idx+1 < len(book_positions) else len(body_lines)
    dialogue_text = extract_text(start_ln, end_ln)
    dialogue_excerpt = truncate(dialogue_text)

    items.append({
        "id": bid,
        "name": bname,
        "sort_order": sort_order,
        "category": "dialogue",
        "level": 1,
        "sections": {
            "Dialogue": dialogue_excerpt,
            "Themes": book_themes[bid],
            "Key Passages": book_key_passages[bid]
        },
        "keywords": book_keywords[bid],
        "metadata": {}
    })
    sort_order += 1

# ═══════════════════════════════════════════════════════════════════════════
# L2: THEMATIC GROUPS
# ═══════════════════════════════════════════════════════════════════════════

l2_groups = [
    {
        "id": "group-justice-individual",
        "name": "Justice and the Individual (Books I-IV)",
        "category": "thematic-group",
        "composite_of": ["book-1", "book-2", "book-3", "book-4"],
        "about": "The first movement of the Republic asks: what is justice? Socrates dismantles conventional definitions (paying debts, helping friends, the advantage of the stronger), then builds a city in speech to find justice writ large. The ideal city requires guardian-warriors educated through carefully censored music and poetry. Justice emerges as each part — whether of the city or the soul — performing its proper function. The tripartite soul (reason, spirit, appetite) mirrors the tripartite city (rulers, auxiliaries, producers).",
        "for_readers": "These books establish the Republic's method: building a political theory to illuminate psychology, and vice versa. The refutation of Thrasymachus in Book I is a masterclass in Socratic method. The Ring of Gyges in Book II remains one of philosophy's greatest thought experiments. The tripartite soul in Book IV is the ancestor of Freud's id/ego/superego.",
        "keywords": ["justice", "tripartite-soul", "ideal-city", "education", "ring-of-gyges", "thrasymachus"]
    },
    {
        "id": "group-philosopher-vision",
        "name": "The Philosopher's Vision (Books V-VII)",
        "category": "thematic-group",
        "composite_of": ["book-5", "book-6", "book-7"],
        "about": "The philosophical heart of the Republic. Socrates makes three 'waves' of controversial proposals: women as guardians, community of families, and philosopher-kings. The distinction between knowledge and opinion grounds the philosopher's authority. The sun analogy and the Divided Line establish the metaphysics of the Forms, culminating in the Allegory of the Cave — perhaps the most famous passage in all of Western philosophy. Education is reconceived as turning the soul from shadows to sunlight.",
        "for_readers": "The Cave allegory resonates far beyond philosophy — it's a parable of awakening applicable to any domain where received opinion substitutes for direct experience. The sun analogy and Divided Line reward careful study: they contain Plato's entire epistemology in compressed form. The argument for philosopher-kings remains provocatively relevant to democratic politics.",
        "keywords": ["philosopher-kings", "allegory-of-cave", "forms", "idea-of-good", "sun-analogy", "divided-line", "education"]
    },
    {
        "id": "group-decline-soul",
        "name": "Decline and the Soul (Books VIII-X)",
        "category": "thematic-group",
        "composite_of": ["book-8", "book-9", "book-10"],
        "about": "The final movement traces political and psychological degeneration. Four corrupt regimes — timocracy, oligarchy, democracy, tyranny — each correspond to a soul type, each arising from the excess of its predecessor's virtue. The tyrant, enslaved by lawless appetites, is proved the most wretched. Poetry is banished as thrice removed from truth. The Allegory of Er closes the work with a cosmic vision: souls choosing their next lives after death, a final argument that justice matters beyond this life.",
        "for_readers": "The cycle of political decay in Book VIII reads like a commentary on contemporary politics — the passage from democratic excess to tyranny has been cited by political theorists for 2,400 years. The banishment of poetry in Book X is deliberately provocative: Plato, himself a supreme literary artist, argues against the art form that made his culture. The Myth of Er is a strange, beautiful coda — part eschatology, part moral psychology.",
        "keywords": ["political-decay", "tyranny", "democracy", "poetry", "allegory-of-er", "afterlife", "immortality"]
    },
]

for grp in l2_groups:
    items.append({
        "id": grp["id"],
        "name": grp["name"],
        "sort_order": sort_order,
        "category": grp["category"],
        "level": 2,
        "sections": {
            "About": grp["about"],
            "For Readers": grp["for_readers"]
        },
        "keywords": grp["keywords"],
        "composite_of": grp["composite_of"],
        "relationship_type": "emergence",
        "metadata": {}
    })
    sort_order += 1

# ═══════════════════════════════════════════════════════════════════════════
# L3: META ITEM
# ═══════════════════════════════════════════════════════════════════════════

items.append({
    "id": "meta-republic-complete",
    "name": "The Republic: Complete",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "Plato's Republic is the foundational text of Western political philosophy and one of the most influential works ever written. Composed as a Socratic dialogue around 375 BCE, it asks a deceptively simple question — what is justice? — and follows it through politics, psychology, education, metaphysics, aesthetics, and eschatology. The ideal city, the tripartite soul, the philosopher-king, the Allegory of the Cave, the theory of Forms, the critique of democracy, the banishment of poetry, the Myth of Er — these ideas have shaped every subsequent generation of Western thought. The Republic is not a utopian blueprint but a thought experiment: what would a perfectly just society require, and what does that tell us about the human soul?",
        "Contemplation": "Plato wrote the Republic as a dialogue — not a treatise, not a set of doctrines, but a conversation. Socrates does not simply state the truth; he leads others to discover it through questioning. The form is the message: philosophy is not a body of knowledge to be memorized but a practice of thinking together. When you read the Republic, you are not receiving Plato's conclusions — you are being invited into the same conversation."
    },
    "keywords": ["plato", "republic", "justice", "philosophy", "complete-work", "western-canon"],
    "composite_of": ["group-justice-individual", "group-philosopher-vision", "group-decline-soul"],
    "relationship_type": "emergence",
    "metadata": {}
})

# ═══════════════════════════════════════════════════════════════════════════
# BUILD GRAMMAR
# ═══════════════════════════════════════════════════════════════════════════

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Plato", "date": "c. 375 BCE", "note": "Author of The Republic"},
            {"name": "Benjamin Jowett (translator)", "date": "1871", "note": "English translation, third edition revised"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, thematic groupings, key passages"}
        ]
    },
    "name": "Republic",
    "description": "Plato's Republic in Benjamin Jowett's translation — the foundational text of Western political philosophy. A Socratic dialogue in ten books exploring justice, the ideal state, the tripartite soul, the philosopher-king, the Allegory of the Cave, the theory of Forms, and the Myth of Er. Includes Jowett's Introduction and Analysis.\n\nSource: Project Gutenberg eBook #1497 (https://www.gutenberg.org/ebooks/1497). Benjamin Jowett translation.\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Raphael's 'School of Athens' (1509-1511, Vatican). Ancient Greek symposium scenes from Attic red-figure pottery. William Blake's illustrations of Platonic themes.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["philosophy", "plato", "political-philosophy", "justice", "ethics", "metaphysics", "education"],
    "roots": ["western-philosophy", "classical-antiquity"],
    "shelves": ["wisdom"],
    "lineages": ["Linehan"],
    "worldview": "dialectical",
    "items": items
}

os.makedirs("grammars/republic-plato", exist_ok=True)
with open("grammars/republic-plato/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

# Validation
ids = [i["id"] for i in items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in items for r in i.get("composite_of", []) if r not in ids]
orders = [i["sort_order"] for i in items]
print(f"\nItems: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
print(f"Sections: {sum(len(i.get('sections', {})) for i in items)}")
print(f"Duplicate IDs: {dupes}")
print(f"Bad refs: {bad_refs}")
print(f"Sort orders sequential: {orders == list(range(1, len(items)+1))}")
print("Done! Grammar written to grammars/republic-plato/grammar.json")
