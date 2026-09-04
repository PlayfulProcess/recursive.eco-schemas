#!/usr/bin/env python3
"""
Parse Plato's Phaedo (Gutenberg #1658) and Timaeus (Gutenberg #1572),
both in Jowett translations. Outputs two grammar.json files.
"""
import json, re, os


def strip_gutenberg(text):
    """Strip Gutenberg header/footer using *** START/END markers."""
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    start = text.find("\n", start) + 1
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    return text[start:end].strip()


def truncate(text, limit=2800):
    """Truncate at ~2800 chars, find last period."""
    if len(text) > limit:
        bp = text.rfind(".", 0, limit)
        if bp == -1:
            bp = limit
        remaining = len(text[bp:].split())
        return text[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    return text


def find_line(lines, target, after=0):
    """Find line number where stripped line matches target, after given index."""
    for i in range(after, len(lines)):
        if lines[i].strip() == target:
            return i
    return -1


def find_line_containing(lines, target, after=0):
    """Find first line containing target string, after given index."""
    for i in range(after, len(lines)):
        if target in lines[i]:
            return i
    return -1


def extract_text(lines, start_ln, end_ln):
    """Extract text between line numbers, cleaning up indentation and blanks."""
    content = []
    started = False
    for j in range(start_ln, min(end_ln, len(lines))):
        line = lines[j].rstrip()
        # Strip leading indentation (Timaeus has 6-space indent)
        stripped = line.lstrip()
        if not started and stripped == "":
            continue
        started = True
        content.append(stripped)
    while content and content[-1].strip() == "":
        content.pop()
    return "\n".join(content)


def validate_grammar(items, name):
    """Run standard validation checks."""
    ids = [i["id"] for i in items]
    dupes = [x for x in ids if ids.count(x) > 1]
    bad_refs = [(i["id"], r) for i in items for r in i.get("composite_of", []) if r not in ids]
    orders = [i["sort_order"] for i in items]
    placeholders = [(i["id"], k) for i in items for k, v in i.get("sections", {}).items() if v == "Placeholder."]
    print(f"\n=== {name} ===")
    print(f"Items: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
    print(f"Sections: {sum(len(i.get('sections', {})) for i in items)}")
    print(f"Duplicate IDs: {dupes}")
    print(f"Bad refs: {bad_refs}")
    print(f"Sort orders sequential: {orders == list(range(1, len(items)+1))}")
    print(f"Remaining placeholders: {len(placeholders)}")


# ═══════════════════════════════════════════════════════════════════════════
# COMMONS
# ═══════════════════════════════════════════════════════════════════════════

def make_commons(ebook_num, title):
    return {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Plato", "date": "c. 360 BCE", "note": f"Author of {title}"},
            {"name": "Benjamin Jowett (translator)", "date": "1871", "note": "English translation, third edition revised"},
            {"name": "Project Gutenberg", "date": "2008", "note": f"eBook #{ebook_num}"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, thematic groupings, commentary"}
        ]
    }


# ═══════════════════════════════════════════════════════════════════════════
# PHAEDO
# ═══════════════════════════════════════════════════════════════════════════

def parse_phaedo():
    print("Parsing Phaedo...")
    with open("seeds/phaedo-plato.txt", encoding="utf-8") as f:
        text = f.read()

    body = strip_gutenberg(text)
    lines = body.split("\n")

    # Find dialogue start (second occurrence of "PHAEDO", the one after intro)
    first_phaedo = find_line(lines, "PHAEDO")
    dialogue_start = find_line(lines, "PHAEDO", first_phaedo + 1)
    print(f"  Dialogue heading at line {dialogue_start}")

    # Find "ECHECRATES:" — first line of actual dialogue
    first_speech = find_line_containing(lines, "ECHECRATES: Were you yourself", dialogue_start)
    print(f"  First speech at line {first_speech}")

    # Introduction: from first_phaedo+1 to dialogue_start
    intro_start = find_line(lines, "INTRODUCTION.", first_phaedo)
    intro_text = extract_text(lines, intro_start + 1, dialogue_start)
    intro_excerpt = truncate(intro_text)

    # Define thematic sections by keyword searches
    # We search for key phrases that mark topic transitions
    section_defs = [
        {
            "id": "philosopher-and-death",
            "name": "The Philosopher and Death",
            "search_start": "ECHECRATES: Were you yourself",
            "search_end": "And shall we call the opposite of dying, living?",
            "theme": "The opening of the dialogue establishes its dramatic situation: Socrates' last day alive, told by Phaedo to Echecrates. Socrates argues that true philosophers spend their lives preparing for death, since philosophy is the separation of soul from body. The body is an obstacle to knowledge — its senses deceive, its desires distract. Only when the soul is freed from the body can it apprehend truth directly. Therefore the philosopher should welcome death, not fear it.",
            "key_passage": "\"The true philosopher is ever pursuing death and dying; and if this is true, why, having had the desire for death all his life long, should he repine at that which he has always been pursuing and desiring?\"\n\n\"He who is a lover of knowledge and who is not angry with the body, and does not voluntarily take leave of it — he is not a philosopher but a lover of the body.\"",
            "keywords": ["death", "philosophy", "body", "soul", "purification", "socrates", "phaedo", "echecrates"]
        },
        {
            "id": "argument-from-opposites",
            "name": "The Argument from Opposites",
            "search_start": "Suppose we consider the question whether the souls of men after death",
            "search_end": "Your favorite doctrine, Socrates, that knowledge is simply",
            "theme": "Socrates presents his first argument for the immortality of the soul: all things come into being from their opposites. The living come from the dead, and the dead from the living. Sleep comes from waking, and waking from sleep. If death comes from life, then life must come from death — the souls of the dead must exist somewhere and return to life. Without this cycle, all things would eventually be dead and nothing would live.",
            "key_passage": "\"Then the living, whether things or persons, Cebes, are generated from the dead? That is clear, he replied. Then the inference is that our souls exist in the world below.\"\n\n\"If the two opposite processes of generation were not always going on in correspondence with each other, turning as it were in a circle, all things would at last have the same form and pass into the same state, and there would be no more generation of them.\"",
            "keywords": ["opposites", "generation", "cycle", "death", "life", "immortality"]
        },
        {
            "id": "theory-of-recollection",
            "name": "The Theory of Recollection",
            "search_start": "Your favorite doctrine, Socrates, that knowledge is simply",
            "search_end": "children, you are haunted with a fear",
            "theme": "Cebes introduces the doctrine of recollection (anamnesis): knowledge is not learned but remembered from a prior existence. When we perceive equal things, we recognize they fall short of absolute Equality — but we could not recognize this shortfall unless we already knew the Form of Equality. Since we did not acquire this knowledge in this life (we had it from birth), our souls must have existed before birth and known the Forms directly. This confirms the pre-existence of the soul.",
            "key_passage": "\"Then before we began to see or hear or perceive in any way, we must have had a knowledge of absolute equality, or we could not have referred to that standard the equals which are derived from the senses.\"\n\n\"Then allegory of recollection brought to my own recollection, and, from what Cebes has said, I am very nearly certain that if equal things are compared with the idea of equality, they must have existed before the time when we first saw them.\"",
            "keywords": ["recollection", "anamnesis", "forms", "equality", "pre-existence", "knowledge", "learning"]
        },
        {
            "id": "argument-from-affinity",
            "name": "The Argument from Affinity",
            "search_start": "children, you are haunted with a fear",
            "search_end": "Now the earth has divers wonderful regions",
            "theme": "Socrates addresses the fear that the soul might be scattered at death like smoke. He distinguishes two kinds of existence: the composite and changing (like the body, which decomposes) and the simple and unchanging (like the Forms, which are eternal). The soul resembles the divine, immortal, intelligible, uniform, and indissoluble. The body resembles the mortal, unintelligible, multiform, and dissoluble. But this argument also contains the famous 'harmony' objection by Simmias: perhaps the soul is merely a harmony of the body, as music is a harmony of the lyre — and perishes with it. Socrates refutes this at length, and presents his final, most rigorous argument: the soul, whose essential nature is life, cannot admit death, just as the odd cannot admit the even.",
            "key_passage": "\"The soul is most like that which is divine, immortal, intelligible, uniform, indissoluble, and ever self-consistent and invariable, whereas the body is most like that which is human, mortal, multiform, unintelligible, dissoluble, and never self-consistent.\"\n\n\"If the immortal is also imperishable, then the soul will be imperishable as well as immortal; but if not, some other proof of her imperishableness will have to be given.\"",
            "keywords": ["affinity", "soul", "body", "harmony", "simmias", "cebes", "forms", "immortality", "final-argument"]
        },
        {
            "id": "allegory-of-the-earth",
            "name": "The Allegory of the Earth",
            "search_start": "Now the earth has divers wonderful regions",
            "search_end": "Wherefore, Simmias, seeing all these things",
            "theme": "Having established the soul's immortality, Socrates describes his cosmological myth. The true earth is far above us — we live in hollows like creatures at the bottom of the sea who mistake the water for the sky. The true earth is adorned with jewels and pure colours; our precious stones are mere fragments. Below the earth is Tartarus, a great chasm through which underground rivers flow — rivers of fire, mud, and the icy waters of the Styx. The souls of the dead are judged and sent to appropriate regions: the incurable to Tartarus forever, the curable to purification, the holy to the pure upper earth.",
            "key_passage": "\"We who live in these hollows are deceived into the notion that we are dwelling above on the surface of the earth; which is just as if a creature who was at the bottom of the sea were to fancy that he was on the surface of the water.\"\n\n\"The true earth is pure and situated in the pure heaven — there are the stars also; and it is the heaven which is commonly spoken of by us as the ether.\"",
            "keywords": ["cosmology", "myth", "true-earth", "tartarus", "afterlife", "judgment", "rivers", "underworld"]
        },
        {
            "id": "death-of-socrates",
            "name": "The Death of Socrates",
            "search_start": "Wherefore, Simmias, seeing all these things",
            "search_end": None,  # to end
            "theme": "The concluding scenes of the dialogue. Socrates exhorts his friends to care for their souls, then calmly prepares for death — bathing, saying farewell to his children and the women of his household. The jailer, weeping, brings the hemlock. Socrates drinks it without tremor, walking about until his legs grow heavy. As the poison reaches his heart, he uncovers his face and speaks his last words: 'Crito, I owe a cock to Asclepius; will you remember to pay the debt?' Phaedo concludes: 'Such was the end of our friend; concerning whom I may truly say, that of all the men of his time whom I have known, he was the wisest and justest and best.'",
            "key_passage": "\"Then raising the cup to his lips, quite readily and cheerfully he drank off the poison.\"\n\n\"Crito, I owe a cock to Asclepius; will you remember to pay the debt?\"\n\n\"Such was the end, Echecrates, of our friend; concerning whom I may truly say, that of all the men of his time whom I have known, he was the wisest and justest and best.\"",
            "keywords": ["death", "hemlock", "poison", "socrates", "crito", "asclepius", "last-words", "courage"]
        },
    ]

    # Find section boundaries by searching for key phrases
    section_positions = []
    for sdef in section_defs:
        start_ln = find_line_containing(lines, sdef["search_start"], first_speech if sdef == section_defs[0] else 0)
        if start_ln == -1:
            # Fallback: search from dialogue start
            start_ln = find_line_containing(lines, sdef["search_start"], dialogue_start)
        if start_ln == -1:
            print(f"  WARNING: Could not find start for {sdef['id']}: '{sdef['search_start'][:40]}...'")
            start_ln = dialogue_start  # fallback
        section_positions.append(start_ln)
        print(f"  {sdef['id']} starts at line {start_ln}")

    items = []
    sort_order = 1

    # Item 1: Introduction (Jowett)
    items.append({
        "id": "introduction",
        "name": "Introduction (Jowett)",
        "sort_order": sort_order,
        "category": "introduction",
        "level": 1,
        "sections": {
            "Analysis": intro_excerpt,
            "Themes": "Jowett's introduction surveys the Phaedo's arguments for immortality, its dramatic setting on Socrates' last day, the relationship between philosophy and death, and the dialogue's place in Plato's philosophical development. He examines the four arguments for the soul's immortality and the myth of the afterlife."
        },
        "keywords": ["jowett", "introduction", "analysis", "overview", "commentary"],
        "metadata": {}
    })
    sort_order += 1

    # Items 2-7: Thematic sections of the dialogue
    l1_ids = []
    for idx, sdef in enumerate(section_defs):
        start_ln = section_positions[idx]
        if idx + 1 < len(section_positions):
            end_ln = section_positions[idx + 1]
        else:
            end_ln = len(lines)

        dialogue_text = extract_text(lines, start_ln, end_ln)
        dialogue_excerpt = truncate(dialogue_text)

        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "category": "dialogue",
            "level": 1,
            "sections": {
                "Dialogue": dialogue_excerpt,
                "Themes": sdef["theme"],
                "Key Passages": sdef["key_passage"]
            },
            "keywords": sdef["keywords"],
            "metadata": {}
        }
        items.append(item)
        l1_ids.append(sdef["id"])
        sort_order += 1

    # L2: Thematic Groups
    l2_groups = [
        {
            "id": "group-arguments-for-immortality",
            "name": "The Arguments for Immortality",
            "composite_of": ["argument-from-opposites", "theory-of-recollection", "argument-from-affinity"],
            "about": "The philosophical core of the Phaedo presents four interconnected arguments for the soul's immortality. The Argument from Opposites shows that life and death generate each other in an eternal cycle. The Theory of Recollection proves the soul existed before birth by demonstrating that we possess knowledge of the Forms that could not have been acquired through the senses. The Argument from Affinity shows that the soul resembles the eternal and unchanging Forms rather than the perishable body. Finally, the argument from essential nature (within the Affinity section) demonstrates that the soul, whose essence is life, cannot admit its opposite — death. These arguments build upon each other, each addressing weaknesses in the previous one.",
            "for_readers": "These arguments represent some of the most influential reasoning in the history of philosophy. Whether or not one finds them convincing, they establish the method of philosophical argument about the nature of consciousness, personal identity, and what (if anything) survives death. The Theory of Recollection introduces Plato's theory of Forms in its most accessible form. The harmony objection raised by Simmias anticipates modern materialist views of consciousness.",
            "keywords": ["immortality", "soul", "forms", "arguments", "philosophy", "opposites", "recollection", "affinity"]
        },
        {
            "id": "group-death-and-meaning",
            "name": "Death, Myth, and Meaning",
            "composite_of": ["philosopher-and-death", "allegory-of-the-earth", "death-of-socrates"],
            "about": "The dramatic and mythological frame of the Phaedo. The dialogue opens with Socrates explaining why philosophers should welcome death — it is the liberation of the soul from the body's distractions. The Allegory of the Earth provides a cosmological vision of the soul's journey after death, with its haunting image of humanity living in hollows like creatures at the bottom of the sea. The death scene itself — Socrates calmly drinking the hemlock, comforting his weeping friends, speaking his enigmatic last words about owing a cock to Asclepius — is one of the most powerful scenes in all of literature.",
            "for_readers": "The Phaedo's emotional power comes from the tension between its philosophical arguments and its dramatic situation. Socrates is not arguing about death in the abstract — he is facing his own death in hours. The allegory of the earth anticipates later Platonic cosmology (the Myth of Er in the Republic). Socrates' last words remain debated: was the 'debt to Asclepius' (god of healing) gratitude for being cured of the disease of life?",
            "keywords": ["death", "myth", "allegory", "socrates", "hemlock", "meaning", "courage", "philosophy"]
        },
    ]

    for grp in l2_groups:
        items.append({
            "id": grp["id"],
            "name": grp["name"],
            "sort_order": sort_order,
            "category": "thematic-group",
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

    # L3: Meta item
    items.append({
        "id": "meta-phaedo-complete",
        "name": "Phaedo: Complete",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Plato's Phaedo dramatizes the last hours of Socrates' life — his final conversation with friends before drinking the hemlock in 399 BCE. It is at once a philosophical treatise on the immortality of the soul and one of the most moving death scenes in Western literature. Through four interconnected arguments, Socrates demonstrates that the soul is immortal: it existed before birth, it resembles the eternal Forms rather than the perishable body, and its essential nature as the principle of life makes it incapable of admitting death. But the Phaedo is more than arguments — it is a portrait of a man who lived his philosophy to the very end, facing death with calm courage and even humor. Socrates' last words — 'Crito, I owe a cock to Asclepius; will you remember to pay the debt?' — have haunted readers for 2,400 years.",
            "Contemplation": "The Phaedo asks the hardest question: what happens when we die? But its deeper question is about how to live. If philosophy is 'practice for death' — the separation of soul from body, of reason from appetite — then every moment of genuine thinking is a rehearsal for eternity. Socrates does not merely argue for immortality; he embodies it. His serenity in the face of death is itself the strongest argument that the soul is something more than a harmony of the body."
        },
        "keywords": ["plato", "phaedo", "socrates", "death", "immortality", "soul", "philosophy", "complete-work"],
        "composite_of": ["group-arguments-for-immortality", "group-death-and-meaning"],
        "relationship_type": "emergence",
        "metadata": {}
    })

    # Build grammar
    grammar = {
        "_grammar_commons": make_commons(1658, "Phaedo"),
        "name": "Phaedo",
        "description": "Plato's Phaedo in Benjamin Jowett's translation — Socrates' final conversation before death, on the immortality of the soul. The dialogue presents four arguments for immortality (from opposites, from recollection, from affinity, and from essential nature), interwoven with the dramatic narrative of Socrates' last hours and his cosmological myth of the true earth and the afterlife. Includes Jowett's Introduction.\n\nSource: Project Gutenberg eBook #1658 (https://www.gutenberg.org/ebooks/1658). Benjamin Jowett translation.\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Jacques-Louis David's 'The Death of Socrates' (1787, Metropolitan Museum of Art). Ancient Greek symposium scenes from Attic red-figure pottery. Raphael's 'School of Athens' (1509-1511, Vatican).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "plato", "death", "immortality", "soul", "socrates"],
        "roots": ["western-philosophy", "classical-antiquity"],
        "shelves": ["wisdom"],
        "lineages": ["Linehan"],
        "worldview": "dialectical",
        "items": items
    }

    os.makedirs("grammars/phaedo-plato", exist_ok=True)
    with open("grammars/phaedo-plato/grammar.json", "w") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    validate_grammar(items, "Phaedo")
    print("Done! Grammar written to grammars/phaedo-plato/grammar.json")


# ═══════════════════════════════════════════════════════════════════════════
# TIMAEUS
# ═══════════════════════════════════════════════════════════════════════════

def parse_timaeus():
    print("\nParsing Timaeus...")
    with open("seeds/timaeus-plato.txt", encoding="utf-8") as f:
        text = f.read()

    body = strip_gutenberg(text)
    lines = body.split("\n")

    # Find the introduction start (body heading, not TOC)
    intro_start = find_line(lines, "INTRODUCTION AND ANALYSIS.")
    # Skip if this is the TOC line; find the body one
    if intro_start < 20:
        intro_start = find_line(lines, "INTRODUCTION AND ANALYSIS.", intro_start + 1)
    print(f"  Introduction at line {intro_start}")

    # Find dialogue start: "TIMAEUS." heading (standalone, after intro sections)
    # The dialogue heading is "TIMAEUS." (with period), after Section 8
    dialogue_heading = find_line(lines, "TIMAEUS.", 0)
    if dialogue_heading == -1:
        # Try without period
        for i in range(len(lines)):
            s = lines[i].strip()
            if s == "TIMAEUS" and i > 3000:  # Must be after the intro
                dialogue_heading = i
                break
    print(f"  Dialogue heading at line {dialogue_heading}")

    # Find "PERSONS OF THE DIALOGUE" which comes right after heading
    persons = find_line_containing(lines, "PERSONS OF THE DIALOGUE", dialogue_heading)
    print(f"  Persons of dialogue at line {persons}")

    # First speech
    first_speech = find_line_containing(lines, "SOCRATES: One, two, three", persons)
    print(f"  First speech at line {first_speech}")

    # Introduction text (from intro_start to dialogue_heading)
    intro_text = extract_text(lines, intro_start + 1, dialogue_heading)
    intro_excerpt = truncate(intro_text)

    # Define thematic sections of the dialogue
    section_defs = [
        {
            "id": "atlantis-prelude",
            "name": "The Atlantis Prelude",
            "search_start": "SOCRATES: One, two, three",
            "search_end": "Let me tell you then why the creator made this world",
            "theme": "The opening of the Timaeus connects it to the Republic (Socrates summarizes yesterday's conversation about the ideal state) and introduces the Atlantis myth. Critias tells the story he heard from his grandfather, who heard it from Solon, who heard it from Egyptian priests: nine thousand years ago, Athens defeated the mighty island empire of Atlantis, which subsequently sank beneath the sea. This is the earliest surviving account of Atlantis. The prelude establishes the dramatic frame: Timaeus will speak about the creation of the universe, Critias about ancient Athens and Atlantis.",
            "key_passage": "\"Listen, Socrates, to a tale which, though strange, is certainly true, having been attested by Solon, who was the wisest of the seven sages.\"\n\n\"There was an island situated in front of the straits which are by you called the Pillars of Heracles; the island was larger than Libya and Asia put together.\"",
            "keywords": ["atlantis", "solon", "egypt", "critias", "socrates", "republic", "prelude"]
        },
        {
            "id": "demiurge-and-creation",
            "name": "The Demiurge and Creation",
            "search_start": "Let me tell you then why the creator made this world",
            "search_end": "Now God did not make the soul after the body",
            "theme": "Timaeus begins his account of creation. The Demiurge (craftsman god) is good, and being free from jealousy, desired that all things should be as good as possible. Finding the visible world in disorder, he brought order out of chaos, fashioning the cosmos as a living creature with soul and intelligence. The universe is unique — a single, spherical, self-sufficient being. It is the fairest and best of all created things, modeled on the eternal pattern of the Forms. The Demiurge put intelligence in soul and soul in body, making the universe a blessed god.",
            "key_passage": "\"He was good, and the good can never have any jealousy of anything. And being free from jealousy, he desired that all things should be as like himself as they could be.\"\n\n\"Wherefore, using the language of probability, we may say that the world became a living creature truly endowed with soul and intelligence by the providence of God.\"",
            "keywords": ["demiurge", "creation", "order", "chaos", "cosmos", "goodness", "intelligence", "soul"]
        },
        {
            "id": "world-soul",
            "name": "The World Soul",
            "search_start": "Now God did not make the soul after the body",
            "search_end": "have a moving image of eternity",
            "theme": "The most mathematically intricate passage in the dialogue. God made the soul prior to and superior to the body. The World Soul is compounded from three elements: the Indivisible (Being), the Divisible, and a mixture of Same and Other. God divided this compound according to a complex numerical series based on the ratios 1:2:3:4:8:9:27, then bent the resulting strip into two circles (the Same and the Other, corresponding to the celestial equator and ecliptic). The World Soul permeates the entire cosmos, giving it life, motion, and rationality. This passage was enormously influential on Pythagorean, Neoplatonic, and medieval cosmology.",
            "key_passage": "\"He made the soul in origin and excellence prior to and older than the body, to be the ruler and mistress, of whom the body was to be the subject.\"\n\n\"Out of the indivisible and unchangeable, and also out of that which is divisible and has to do with material bodies, he compounded a third and intermediate kind of essence.\"",
            "keywords": ["world-soul", "mathematics", "same", "other", "harmony", "proportion", "cosmos", "circles"]
        },
        {
            "id": "time-and-heavenly-bodies",
            "name": "Time and the Heavenly Bodies",
            "search_start": "have a moving image of eternity",
            "search_end": "received from him the immortal principle of a mortal creature",
            "theme": "Time is a moving image of eternity. Before the creation of the heavens, there were no days, nights, months, or years. The Demiurge created the sun, moon, and five planets to 'distinguish and preserve the numbers of time.' Each celestial body was placed in its proper orbit. The fixed stars were created and set in the revolution of the Same. The Creator then sowed human souls in the stars, one soul per star, showing them the nature of the universe and the laws of destiny. He committed the fashioning of mortal bodies to the younger gods.",
            "key_passage": "\"He resolved to have a moving image of eternity, and when he set in order the heaven, he made this image eternal but moving according to number, while eternity itself rests in unity; and this image we call time.\"\n\n\"There were no days and nights and months and years before the heaven was created, but when he constructed the heaven he created them also.\"",
            "keywords": ["time", "eternity", "planets", "stars", "sun", "moon", "celestial", "image"]
        },
        {
            "id": "human-soul-and-body",
            "name": "The Human Soul and Body",
            "search_start": "receiving from him the immortal",
            "search_end": "God fashioned them by form and number",
            "theme": "The younger gods create the human being. They receive the immortal soul from the Creator and fashion a mortal body around it, along with a mortal soul subject to pleasure, pain, fear, anger, and desire. The mortal soul is housed in the chest, separated from the immortal soul in the head by the neck. The spirited part is placed near the head to serve as reason's ally; the appetitive part is placed below the midriff. Plato describes the construction of the body in detail: marrow as the seed of life, bones and flesh as protection, the liver as a mirror of the mind's thoughts, the intestines to prevent gluttony.",
            "key_passage": "\"They gave to the mortal nature a separate habitation in another part of the body, placing the neck between them to be the isthmus and boundary.\"\n\n\"Fearing to pollute the divine any more than was absolutely unavoidable, they gave to the mortal nature a separate habitation.\"",
            "keywords": ["human", "body", "soul", "mortal", "immortal", "head", "chest", "organs", "marrow"]
        },
        {
            "id": "elements-and-matter",
            "name": "The Elements and Matter",
            "search_start": "God fashioned them by form and number",
            "search_end": "health commonly results; when in the opposite order, disease",
            "theme": "Plato's geometric atomism — one of the most original passages in ancient philosophy. All matter is composed of two fundamental triangles: the isosceles right triangle and the scalene right triangle (half of an equilateral). From these triangles, four regular solids are constructed: the tetrahedron (fire), octahedron (air), icosahedron (water), and cube (earth). Fire, air, and water can transform into each other because they share the same basic triangle; earth cannot, because its triangle is different. This section also introduces the 'receptacle' (chora) — the space or medium in which all generation occurs, likened to a mother or nurse. The receptacle receives all forms but has no form of its own, like gold that can be shaped into any figure.",
            "key_passage": "\"Every sort of body possesses solidity, and every solid must necessarily be contained in planes; and every plane rectilinear figure is composed of triangles.\"\n\n\"The universal nature which receives all bodies — that must be always called the same; for, while receiving all things, she never departs at all from her own nature.\"",
            "keywords": ["elements", "triangles", "geometry", "fire", "earth", "water", "air", "receptacle", "chora", "matter"]
        },
        {
            "id": "diseases-and-health",
            "name": "Diseases and Health",
            "search_start": "health commonly results",
            "search_end": None,
            "theme": "The final major section applies Plato's physical theory to medicine. Disease arises when the natural processes of the body are reversed — when flesh decomposes and sends corrupted substances into the blood. Plato describes diseases of bile, phlegm, and fever, diseases of the marrow and bones, and diseases of the soul (ignorance and madness). The greatest disease is excessive pleasure or pain, which makes a man mad. The cure for both body and soul is proportionate exercise: gymnastics for the body, philosophy for the soul. The dialogue concludes with the creation of women (from degenerate men), birds, beasts, and fishes, completing the account of the living cosmos.",
            "key_passage": "\"When the flesh becomes decomposed and sends back the wasting substance into the veins, then an over-supply of blood of diverse kinds, mingling with air in the veins, contains all sorts of bile and serum and phlegm.\"\n\n\"We may now say that our discourse about the nature of the universe has an end. The world has received animals, mortal and immortal, and is fulfilled with them — the sensible God who is the image of the intellectual, the greatest, best, fairest, most perfect — the one only-begotten heaven.\"",
            "keywords": ["disease", "health", "medicine", "body", "soul", "exercise", "bile", "women", "animals"]
        },
    ]

    # Find section boundaries
    section_positions = []
    search_from = first_speech
    for sdef in section_defs:
        start_ln = find_line_containing(lines, sdef["search_start"], search_from)
        if start_ln == -1:
            start_ln = find_line_containing(lines, sdef["search_start"], dialogue_heading)
        if start_ln == -1:
            print(f"  WARNING: Could not find start for {sdef['id']}: '{sdef['search_start'][:50]}...'")
            start_ln = search_from
        section_positions.append(start_ln)
        search_from = start_ln + 1  # subsequent sections must come after
        print(f"  {sdef['id']} starts at line {start_ln}")

    items = []
    sort_order = 1

    # Item 1: Introduction and Analysis (Jowett)
    items.append({
        "id": "introduction",
        "name": "Introduction and Analysis (Jowett)",
        "sort_order": sort_order,
        "category": "introduction",
        "level": 1,
        "sections": {
            "Analysis": intro_excerpt,
            "Themes": "Jowett's extensive introduction surveys the Timaeus as the most influential yet most obscure of Plato's dialogues. He examines its cosmology, its relationship to Pre-Socratic philosophy, the mathematical structure of the World Soul, Plato's geometric atomism, his account of the human body and its diseases, and the dialogue's enormous influence on Neoplatonism, medieval philosophy, and early modern science."
        },
        "keywords": ["jowett", "introduction", "analysis", "overview", "commentary"],
        "metadata": {}
    })
    sort_order += 1

    # Items 2-8: Thematic sections
    l1_ids = []
    for idx, sdef in enumerate(section_defs):
        start_ln = section_positions[idx]
        if idx + 1 < len(section_positions):
            end_ln = section_positions[idx + 1]
        else:
            end_ln = len(lines)

        dialogue_text = extract_text(lines, start_ln, end_ln)
        dialogue_excerpt = truncate(dialogue_text)

        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "category": "dialogue",
            "level": 1,
            "sections": {
                "Dialogue": dialogue_excerpt,
                "Themes": sdef["theme"],
                "Key Passages": sdef["key_passage"]
            },
            "keywords": sdef["keywords"],
            "metadata": {}
        }
        items.append(item)
        l1_ids.append(sdef["id"])
        sort_order += 1

    # L2: Thematic Groups
    l2_groups = [
        {
            "id": "group-cosmology",
            "name": "The Creation of the Cosmos",
            "composite_of": ["demiurge-and-creation", "world-soul", "time-and-heavenly-bodies"],
            "about": "The first great movement of the Timaeus: the creation of the universe by the Demiurge. God is good, and being free from jealousy, created the best possible world — a single, spherical, living cosmos endowed with soul and intelligence. The World Soul, compounded from Being, Same, and Other in precise mathematical ratios, permeates the universe and gives it rational motion. Time is created as a 'moving image of eternity,' measured by the orbits of the sun, moon, and planets. This cosmic vision — of a mathematically ordered, living universe created by a rational craftsman — was the dominant cosmology of the Western world for nearly two thousand years.",
            "for_readers": "The Timaeus cosmology is the ancestor of both scientific cosmology and natural theology. The Demiurge is not the omnipotent creator of Genesis but a craftsman who works with pre-existing materials and is constrained by necessity. The World Soul passage, with its complex mathematical harmonies, influenced Kepler's search for the 'music of the spheres.' The doctrine that time is a 'moving image of eternity' remains one of the most profound things ever said about the nature of time.",
            "keywords": ["cosmology", "creation", "demiurge", "world-soul", "time", "eternity", "planets"]
        },
        {
            "id": "group-physics-and-biology",
            "name": "Physics, Biology, and Medicine",
            "composite_of": ["human-soul-and-body", "elements-and-matter", "diseases-and-health"],
            "about": "The second great movement: the creation of humanity and the material world. Plato's geometric atomism derives all matter from two types of triangles, constructing the four elements as regular solids — an astonishing anticipation of the idea that physical reality has mathematical structure at its deepest level. The human being is a microcosm of the universe: the immortal soul in the head mirrors the World Soul, while the mortal soul in the chest mirrors the realm of becoming. Disease arises from disruption of natural processes; the cure is proportionate exercise of body (gymnastics) and soul (philosophy).",
            "for_readers": "Plato's geometric atomism is often dismissed as quaint, but its core insight — that the properties of matter arise from mathematical structure — is precisely what modern physics confirms. The triangle theory anticipates both Dalton's atomic theory and the Standard Model's derivation of particle properties from symmetry groups. The medical sections, though pre-scientific, establish the principle that bodily and mental health are inseparable — a view that modern medicine is only now recovering.",
            "keywords": ["physics", "biology", "medicine", "triangles", "elements", "body", "soul", "health", "disease"]
        },
        {
            "id": "group-narrative-frame",
            "name": "Myth, History, and Frame",
            "composite_of": ["atlantis-prelude"],
            "about": "The dramatic and mythological frame of the Timaeus. The dialogue opens with Socrates summarizing his ideal state (from the Republic), then Critias tells the story of ancient Athens and Atlantis — the first and most famous account of the lost continent. The Atlantis prelude establishes the Timaeus as more than abstract cosmology: it is a story told by specific people on a specific day, grounded in the mythological traditions of Egypt and Greece. The connection to the Republic gives the entire cosmological account a political dimension: understanding how the universe is made helps us understand how human society should be ordered.",
            "for_readers": "The Atlantis story has generated more speculation than perhaps any other passage in ancient literature. Was it historical memory (of Thera/Santorini?), pure allegory, or political myth? Whatever its origin, it establishes one of the Timaeus's key themes: the relationship between cosmic order and political order. The universe is good because it is well-ordered; societies are good for the same reason.",
            "keywords": ["atlantis", "solon", "egypt", "myth", "republic", "frame", "narrative"]
        },
    ]

    for grp in l2_groups:
        items.append({
            "id": grp["id"],
            "name": grp["name"],
            "sort_order": sort_order,
            "category": "thematic-group",
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

    # L3: Meta item
    items.append({
        "id": "meta-timaeus-complete",
        "name": "Timaeus: Complete",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Plato's Timaeus is the most ambitious cosmological text of antiquity — an account of the creation of the universe, time, the human body, and the nature of matter. A divine Craftsman (Demiurge), being good and free from jealousy, fashions the cosmos as a living, intelligent being, endowed with a World Soul structured by mathematical harmonies. Time is a 'moving image of eternity.' Matter is composed of geometric triangles arranged as regular solids. The human being is a microcosm: immortal soul in the head, mortal soul in the chest, body as vehicle. Disease arises from disorder; the cure is philosophy and gymnastics. The dialogue also contains the earliest account of Atlantis. For nearly two thousand years, the Timaeus was the most widely read of Plato's works, shaping Neoplatonism, Islamic philosophy, medieval cosmology, and the birth of modern science.",
            "Contemplation": "The Timaeus is Plato's most daring work — an attempt to give a 'likely story' (eikos mythos) of everything: the origin of the cosmos, the structure of matter, the nature of time, the design of the human body. Plato insists that this can only be a probable account, not certain knowledge, because the physical world is always becoming, never fully being. Yet the attempt itself is magnificent. The Timaeus reminds us that the desire to understand the whole — to see the universe as a single, intelligible, beautiful creation — is the deepest impulse of philosophy."
        },
        "keywords": ["plato", "timaeus", "cosmology", "creation", "demiurge", "philosophy", "complete-work"],
        "composite_of": ["group-cosmology", "group-physics-and-biology", "group-narrative-frame"],
        "relationship_type": "emergence",
        "metadata": {}
    })

    # Build grammar
    grammar = {
        "_grammar_commons": make_commons(1572, "Timaeus"),
        "name": "Timaeus",
        "description": "Plato's Timaeus in Benjamin Jowett's translation — the most influential cosmological text of antiquity. A divine Craftsman creates the universe as a living, intelligent being with a mathematically structured World Soul. Time is a moving image of eternity. Matter is composed of geometric triangles. The human being is a microcosm of the cosmos. Contains the earliest account of Atlantis. Includes Jowett's Introduction and Analysis.\n\nSource: Project Gutenberg eBook #1572 (https://www.gutenberg.org/ebooks/1572). Benjamin Jowett translation.\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Raphael's 'School of Athens' (1509-1511, Vatican), showing Plato holding the Timaeus. Medieval diagrams of the Platonic solids and World Soul. Robert Fludd's Utriusque Cosmi (1617) cosmological engravings.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "plato", "cosmology", "creation", "mathematics", "physics"],
        "roots": ["western-philosophy", "classical-antiquity"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "dialectical",
        "items": items
    }

    os.makedirs("grammars/timaeus-plato", exist_ok=True)
    with open("grammars/timaeus-plato/grammar.json", "w") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    validate_grammar(items, "Timaeus")
    print("Done! Grammar written to grammars/timaeus-plato/grammar.json")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parse_phaedo()
    parse_timaeus()
    print("\n=== Both grammars complete! ===")
