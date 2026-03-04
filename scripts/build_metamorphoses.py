#!/usr/bin/env python3
"""
Build grammar.json for Ovid's Metamorphoses (Books I-VII) from the
Project Gutenberg seed text.

Parses the Riley translation, extracting individual fables (myths) as L1 items,
Book groupings and thematic groupings as L2 items, and meta-categories as L3.

Strips: Gutenberg header/footer, footnotes, EXPLANATION sections, editorial
introductions, synoptical views, and transcriber's notes.
Keeps: The primary translated text of each fable, plus the synopsis/argument.
"""

import json
import re
import os
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "seeds" / "metamorphoses-ovid.txt"
OUTPUT_FILE = Path(__file__).parent.parent / "grammars" / "metamorphoses-ovid" / "grammar.json"

# Roman numeral conversion
ROMAN_MAP = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7,
    'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12, 'XIII': 13,
    'XIV': 14, 'XV': 15, 'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19,
    'XX': 20
}


def roman_to_int(s):
    return ROMAN_MAP.get(s.strip(), 0)


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        start_idx = text.index('\n', start_idx) + 1
    else:
        start_idx = 0

    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = len(text)

    return text[start_idx:end_idx]


def strip_front_matter(text):
    """Remove everything before 'BOOK THE FIRST'."""
    marker = "BOOK THE FIRST."
    idx = text.find(marker)
    if idx != -1:
        return text[idx:]
    return text


def clean_story_text(text):
    """Remove footnotes, explanations, and editorial content from story text."""
    lines = text.split('\n')
    cleaned = []
    in_footnote = False
    in_explanation = False

    for line in lines:
        stripped = line.strip()

        # Skip EXPLANATION sections
        if stripped == 'EXPLANATION.':
            in_explanation = True
            continue
        if in_explanation:
            # Explanation ends at next FABLE or BOOK heading or blank line after content
            if re.match(r'^FABLE [IVXLC]', stripped) or re.match(r'^BOOK THE', stripped):
                in_explanation = False
                # Don't add this line - it'll be handled by the parser
            else:
                continue

        # Skip footnotes (indented blocks starting with [Footnote)
        if re.match(r'\s*\[Footnote', line):
            in_footnote = True
            continue
        if in_footnote:
            if stripped.endswith(']') or stripped == '':
                if stripped.endswith(']'):
                    in_footnote = False
                elif stripped == '' and in_footnote:
                    # Check if next non-blank is a footnote continuation or not
                    in_footnote = False
                continue
            continue

        # Skip transcriber's notes
        if stripped.startswith("[Transcriber's Note"):
            continue
        if stripped.startswith("[From Bell edition") or stripped.startswith("[From McKay edition") or stripped.startswith("[By Edward Brooks"):
            continue

        cleaned.append(line)

    return '\n'.join(cleaned)


def parse_books_and_fables(text):
    """Parse the text into books, each containing fables."""
    books = {}

    # Split by BOOK headings
    book_pattern = re.compile(r'^BOOK THE (\w+)\.\s*$', re.MULTILINE)
    book_matches = list(book_pattern.finditer(text))

    book_names = {
        'FIRST': 1, 'SECOND': 2, 'THIRD': 3, 'FOURTH': 4,
        'FIFTH': 5, 'SIXTH': 6, 'SEVENTH': 7
    }

    for i, match in enumerate(book_matches):
        book_name = match.group(1)
        book_num = book_names.get(book_name, 0)
        if book_num == 0:
            continue

        start = match.end()
        end = book_matches[i + 1].start() if i + 1 < len(book_matches) else len(text)
        book_text = text[start:end]

        # Parse fables within this book
        # Match FABLE or THE ARGUMENT
        fable_pattern = re.compile(
            r'^(FABLE\s+([IVXLC]+)\.\s*\[.*?\]|THE ARGUMENT\.\s*\[.*?\])\s*$',
            re.MULTILINE
        )
        fable_matches = list(fable_pattern.finditer(book_text))

        fables = []
        for j, fm in enumerate(fable_matches):
            fable_start = fm.end()
            fable_end = fable_matches[j + 1].start() if j + 1 < len(fable_matches) else len(book_text)
            fable_text = book_text[fable_start:fable_end].strip()

            heading = fm.group(0).strip()
            if heading.startswith('THE ARGUMENT'):
                fable_num = 0
                fable_label = "The Argument"
            else:
                fable_num = roman_to_int(fm.group(2))
                fable_label = f"Fable {fable_num}"

            fables.append({
                'book': book_num,
                'fable_num': fable_num,
                'label': fable_label,
                'heading': heading,
                'raw_text': fable_text
            })

        books[book_num] = fables

    return books


def extract_synopsis_and_story(raw_text):
    """
    Separate the synopsis (indented italic text at start) from the story body.
    Also strip footnotes and explanations.
    """
    lines = raw_text.split('\n')
    synopsis_lines = []
    story_lines = []
    in_synopsis = True
    in_footnote = False
    in_explanation = False
    found_story_start = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines at the very beginning
        if in_synopsis and not stripped and not synopsis_lines:
            continue

        # Synopsis is the indented block at the start (typically 2+ spaces indent)
        if in_synopsis:
            if stripped and (line.startswith('  ') or line.startswith('\t')):
                synopsis_lines.append(stripped)
                continue
            elif stripped == '':
                if synopsis_lines:
                    in_synopsis = False
                continue
            else:
                in_synopsis = False
                # Fall through to story processing

        # Skip EXPLANATION sections
        if stripped == 'EXPLANATION.':
            in_explanation = True
            continue
        if in_explanation:
            if stripped == '' and story_lines and story_lines[-1] == '':
                # Could be end of explanation - check if next content is a new section
                pass
            # Explanation continues until we hit something that looks like a new section
            # or we run out of indented text
            if re.match(r'^FABLE [IVXLC]', stripped) or re.match(r'^BOOK THE', stripped):
                in_explanation = False
            else:
                continue

        # Skip footnotes
        if re.match(r'\s*\[Footnote', line):
            in_footnote = True
            continue
        if in_footnote:
            if stripped.endswith(']'):
                in_footnote = False
            continue

        # Skip editorial notes in brackets at beginning
        if stripped.startswith('[From ') or stripped.startswith('[By '):
            continue

        story_lines.append(line)

    synopsis = ' '.join(synopsis_lines).strip()
    # Clean up synopsis: remove {braces} translator additions for cleaner reading
    synopsis = re.sub(r'\{[^}]*\}', '', synopsis).strip()
    synopsis = re.sub(r'\s+', ' ', synopsis)

    # Process story text
    story_raw = '\n'.join(story_lines).strip()

    # Remove {braces} content (translator additions) for cleaner text
    story_clean = re.sub(r'\{([^}]*)\}', r'\1', story_raw)

    # Remove footnote reference numbers like [1], [73], etc.
    story_clean = re.sub(r'\[(\d+)\]', '', story_clean)

    # Clean up extra whitespace
    story_clean = re.sub(r'\n{3,}', '\n\n', story_clean)
    story_clean = story_clean.strip()

    return synopsis, story_clean


# Fable name mappings - give each fable a descriptive mythological name
FABLE_NAMES = {
    # Book I
    (1, 0): ("The Invocation", "invocation", ["poetry", "creation", "gods"], "creation"),
    (1, 1): ("The Creation from Chaos", "creation-from-chaos", ["chaos", "creation", "elements", "cosmos"], "creation"),
    (1, 2): ("The Ordering of the World", "ordering-of-the-world", ["creation", "Prometheus", "mankind", "elements"], "creation"),
    (1, 3): ("The Four Ages", "four-ages", ["golden-age", "silver-age", "bronze-age", "iron-age", "decline"], "ages-and-floods"),
    (1, 4): ("The War of the Giants", "war-of-giants", ["giants", "Jupiter", "rebellion", "blood"], "ages-and-floods"),
    (1, 5): ("The Wickedness of Mankind", "wickedness-of-mankind", ["impiety", "Jupiter", "judgment"], "ages-and-floods"),
    (1, 6): ("The Council of the Gods", "council-of-gods", ["Jupiter", "gods", "punishment", "Lycaon"], "divine-punishment"),
    (1, 7): ("Lycaon Transformed into a Wolf", "lycaon-wolf", ["Lycaon", "wolf", "transformation", "punishment"], "divine-punishment"),
    (1, 8): ("The Great Flood", "great-flood", ["flood", "Deucalion", "Pyrrha", "destruction"], "ages-and-floods"),
    (1, 9): ("Deucalion and Pyrrha", "deucalion-pyrrha", ["Deucalion", "Pyrrha", "stones", "rebirth", "humanity"], "ages-and-floods"),
    (1, 10): ("The New Creation", "new-creation", ["Python", "earth", "spontaneous-generation", "renewal"], "creation"),
    (1, 11): ("Apollo Slays Python", "apollo-slays-python", ["Apollo", "Python", "serpent", "victory"], "divine-heroes"),
    (1, 12): ("Apollo and Daphne", "apollo-daphne", ["Apollo", "Daphne", "love", "laurel", "pursuit", "Cupid"], "love-transformations"),
    (1, 13): ("Io and Jupiter", "io-jupiter", ["Io", "Jupiter", "cow", "Juno", "jealousy"], "love-transformations"),
    (1, 14): ("Mercury and Argus", "mercury-argus", ["Mercury", "Argus", "Syrinx", "reeds", "eyes", "peacock"], "divine-heroes"),
    (1, 15): ("Syrinx Transformed into Reeds", "syrinx-reeds", ["Syrinx", "Pan", "reeds", "music", "pursuit"], "love-transformations"),
    (1, 16): ("Io Restored", "io-restored", ["Io", "restoration", "Juno", "Egypt", "Epaphus"], "love-transformations"),
    (1, 17): ("Phaethon's Parentage", "phaethon-parentage", ["Phaethon", "Epaphus", "Sun", "parentage"], "divine-heroes"),

    # Book II
    (2, 1): ("Phaethon and the Chariot of the Sun", "phaethon-chariot", ["Phaethon", "Sun", "chariot", "fire", "destruction", "hubris"], "divine-punishment"),
    (2, 2): ("The Lament for Phaethon", "lament-phaethon", ["Phaethon", "grief", "Heliades", "poplars", "amber"], "grief-and-loss"),
    (2, 3): ("Cycnus Transformed into a Swan", "cycnus-swan", ["Cycnus", "swan", "grief", "transformation"], "grief-and-loss"),
    (2, 4): ("Jupiter Surveys the Damage", "jupiter-surveys-damage", ["Jupiter", "earth", "fire", "Callisto"], "divine-heroes"),
    (2, 5): ("Callisto and Jupiter", "callisto-jupiter", ["Callisto", "Jupiter", "Diana", "seduction", "bear"], "love-transformations"),
    (2, 8): ("The Crow and Minerva", "crow-minerva", ["crow", "Minerva", "Erichthonius", "white-to-black"], "divine-punishment"),
    (2, 9): ("The Raven and Coronis", "raven-coronis", ["raven", "Coronis", "Apollo", "infidelity", "black"], "divine-punishment"),
    (2, 10): ("The Birth of Aesculapius", "birth-aesculapius", ["Aesculapius", "Coronis", "Chiron", "healing"], "divine-heroes"),
    (2, 11): ("Ocyrhoe's Prophecy", "ocyrhoe-prophecy", ["Ocyrhoe", "Chiron", "prophecy", "mare"], "divine-punishment"),
    (2, 12): ("Mercury and Battus", "mercury-battus", ["Mercury", "Battus", "theft", "touchstone"], "divine-punishment"),
    (2, 13): ("Mercury and Herse", "mercury-herse", ["Mercury", "Herse", "Aglauros", "Envy", "stone"], "love-transformations"),
    (2, 14): ("The Rape of Europa", "rape-of-europa", ["Europa", "Jupiter", "bull", "Crete", "abduction"], "love-transformations"),

    # Book III
    (3, 1): ("Cadmus and the Dragon", "cadmus-dragon", ["Cadmus", "dragon", "teeth", "Thebes", "warriors"], "founding-myths"),
    (3, 2): ("The Founding of Thebes", "founding-thebes", ["Cadmus", "Thebes", "warriors", "civilization"], "founding-myths"),
    (3, 3): ("Actaeon and Diana", "actaeon-diana", ["Actaeon", "Diana", "stag", "hounds", "seeing-the-divine"], "divine-punishment"),
    (3, 4): ("Juno and Semele", "juno-semele", ["Juno", "Semele", "Jupiter", "fire", "Bacchus"], "divine-punishment"),
    (3, 5): ("Tiresias", "tiresias", ["Tiresias", "blindness", "prophecy", "gender", "Jupiter", "Juno"], "divine-heroes"),
    (3, 6): ("Narcissus and Echo", "narcissus-echo", ["Narcissus", "Echo", "reflection", "self-love", "flower"], "love-transformations"),
    (3, 7): ("Pentheus and Bacchus", "pentheus-bacchus", ["Pentheus", "Bacchus", "Tiresias", "prophecy", "denial"], "divine-punishment"),
    (3, 8): ("The Sailors and Bacchus", "sailors-bacchus", ["Bacchus", "sailors", "dolphins", "Pentheus", "Maenads"], "divine-punishment"),

    # Book IV
    (4, 1): ("Pyramus and Thisbe", "pyramus-thisbe", ["Pyramus", "Thisbe", "love", "mulberry", "tragedy", "wall"], "love-transformations"),
    (4, 2): ("Mars and Venus", "mars-venus", ["Mars", "Venus", "Vulcan", "Sun", "net", "adultery"], "love-transformations"),
    (4, 3): ("The Sun and Leucothoe", "sun-leucothoe", ["Sun", "Leucothoe", "Clytie", "jealousy", "burial"], "love-transformations"),
    (4, 4): ("Clytie Becomes a Sunflower", "clytie-sunflower", ["Clytie", "sunflower", "unrequited-love", "Sun"], "love-transformations"),
    (4, 5): ("Salmacis and Hermaphroditus", "salmacis-hermaphroditus", ["Salmacis", "Hermaphroditus", "union", "water", "androgyny"], "love-transformations"),
    (4, 6): ("The Daughters of Minyas", "daughters-of-minyas", ["Minyas", "Bacchus", "bats", "punishment", "weaving"], "divine-punishment"),
    (4, 7): ("Ino and Athamas", "ino-athamas", ["Ino", "Athamas", "Juno", "Furies", "madness", "sea"], "divine-punishment"),
    (4, 8): ("Cadmus and Harmonia Become Serpents", "cadmus-harmonia-serpents", ["Cadmus", "Harmonia", "serpents", "exile", "sorrow"], "grief-and-loss"),
    (4, 9): ("Perseus and Medusa", "perseus-medusa", ["Perseus", "Medusa", "Gorgon", "snakes", "Atlas", "stone"], "divine-heroes"),
    (4, 10): ("Perseus and Andromeda", "perseus-andromeda", ["Perseus", "Andromeda", "sea-monster", "rescue", "coral"], "divine-heroes"),

    # Book V
    (5, 1): ("The Battle at Perseus's Wedding", "battle-perseus-wedding", ["Perseus", "Phineus", "battle", "stone", "wedding"], "divine-heroes"),
    (5, 2): ("Pallas and the Muses", "pallas-muses", ["Pallas", "Muses", "Helicon", "Hippocrene", "Pegasus"], "divine-heroes"),
    (5, 3): ("The Pierides Challenge the Muses", "pierides-challenge", ["Pierides", "Muses", "contest", "magpies", "song"], "divine-punishment"),
    (5, 4): ("The Rape of Proserpina", "rape-of-proserpina", ["Proserpina", "Pluto", "Ceres", "underworld", "seasons"], "love-transformations"),
    (5, 5): ("Ceres Searches for Proserpina", "ceres-searches", ["Ceres", "Proserpina", "wandering", "grief", "Cyane", "Arethusa"], "grief-and-loss"),
    (5, 6): ("Triptolemus and Agriculture", "triptolemus-agriculture", ["Triptolemus", "Ceres", "agriculture", "Lyncus", "lynx"], "founding-myths"),
    (5, 7): ("The Pierides Become Magpies", "pierides-magpies", ["Pierides", "magpies", "hubris", "Muses"], "divine-punishment"),

    # Book VI
    (6, 1): ("Arachne and Minerva", "arachne-minerva", ["Arachne", "Minerva", "weaving", "spider", "hubris", "contest"], "divine-punishment"),
    (6, 2): ("Niobe", "niobe", ["Niobe", "Latona", "Apollo", "Diana", "children", "stone", "grief"], "divine-punishment"),
    (6, 3): ("The Lycian Peasants Become Frogs", "lycian-peasants-frogs", ["Latona", "peasants", "frogs", "water", "rudeness"], "divine-punishment"),
    (6, 4): ("Marsyas", "marsyas", ["Marsyas", "Apollo", "flute", "contest", "flaying"], "divine-punishment"),
    (6, 5): ("Tereus, Philomela, and Procne", "tereus-philomela-procne", ["Tereus", "Philomela", "Procne", "nightingale", "swallow", "violence"], "love-transformations"),
    (6, 6): ("Boreas and Orithyia", "boreas-orithyia", ["Boreas", "Orithyia", "wind", "abduction", "Argonauts"], "love-transformations"),
    (6, 7): ("The Argonauts Set Sail", "argonauts-set-sail", ["Argonauts", "Jason", "Golden-Fleece", "Calais", "Zethes"], "founding-myths"),

    # Book VII
    (7, 1): ("Medea and Jason", "medea-jason", ["Medea", "Jason", "Golden-Fleece", "magic", "love", "bulls"], "love-transformations"),
    (7, 2): ("Medea's Magic", "medea-magic", ["Medea", "Aeson", "rejuvenation", "Pelias", "trickery", "magic"], "divine-heroes"),
    (7, 3): ("Medea's Flight", "medea-flight", ["Medea", "flight", "transformations", "Aegeus", "Theseus"], "divine-heroes"),
    (7, 4): ("Theseus Returns", "theseus-returns", ["Theseus", "Aegeus", "Medea", "poison", "recognition"], "founding-myths"),
    (7, 5): ("The Plague at Aegina", "plague-aegina", ["plague", "Aegina", "death", "Myrmidons", "ants"], "ages-and-floods"),
    (7, 6): ("The Myrmidons", "myrmidons", ["Myrmidons", "ants", "warriors", "transformation", "Aeacus"], "founding-myths"),
    (7, 7): ("Cephalus and Procris", "cephalus-procris", ["Cephalus", "Procris", "Aurora", "jealousy", "fidelity"], "love-transformations"),
    (7, 8): ("The Death of Procris", "death-of-procris", ["Procris", "Cephalus", "javelin", "death", "misunderstanding"], "grief-and-loss"),
}

# Thematic groupings for L2
THEMATIC_GROUPS = {
    "creation": {
        "name": "Creation and Cosmos",
        "about": "The birth of the world from primordial chaos, the ordering of the elements, and the creation of humankind. Ovid opens with the grandest transformation of all: nothingness becoming everything.",
        "reflection": "What does it mean that the world begins in chaos? Every act of creation requires an act of separation -- light from dark, sea from sky, self from other. Where do you see creation emerging from confusion in your own life?",
        "keywords": ["creation", "chaos", "cosmos", "elements", "Prometheus", "order"]
    },
    "ages-and-floods": {
        "name": "The Ages of Man and the Great Flood",
        "about": "The decline from the Golden Age through Silver, Bronze, and Iron Ages, culminating in the Great Flood and the renewal of humanity through Deucalion and Pyrrha. A cycle of degeneration and rebirth.",
        "reflection": "Ovid shows humanity declining from innocence to violence. Yet after the flood, renewal comes not from divine creation but from human faith -- Deucalion and Pyrrha casting stones behind them. What does it mean to rebuild after catastrophe?",
        "keywords": ["golden-age", "decline", "flood", "renewal", "Deucalion", "Pyrrha"]
    },
    "divine-punishment": {
        "name": "Divine Punishment and Hubris",
        "about": "The gods do not tolerate those who challenge their authority, deny their worship, or transgress sacred boundaries. From Lycaon to Arachne to Niobe, mortals who dare to rival or defy the gods are struck down and transformed -- warnings etched into the natural world.",
        "reflection": "Is divine punishment just, or merely the exercise of power? Ovid presents these stories with sympathy for the punished. Arachne's weaving was magnificent; Niobe loved her children. When power meets talent, who really loses?",
        "keywords": ["punishment", "hubris", "gods", "transformation", "power", "defiance"]
    },
    "love-transformations": {
        "name": "Love and Metamorphosis",
        "about": "Love in Ovid is the supreme transformative force -- more powerful than any god. It drives Apollo to chase Daphne, Jupiter to become a bull, Narcissus to waste away, and Pyramus and Thisbe to their deaths. Bodies change because desire changes everything.",
        "reflection": "Ovid's love stories rarely end well. Love transforms, but it also consumes. Apollo gets a tree instead of a bride; Narcissus gets a flower instead of himself. What does it mean when love changes you into something you never intended to become?",
        "keywords": ["love", "desire", "pursuit", "transformation", "tragedy", "beauty"]
    },
    "divine-heroes": {
        "name": "Heroes and Divine Deeds",
        "about": "Gods and mortals who accomplish great feats: Apollo slaying Python, Perseus beheading Medusa, Mercury outwitting Argus, Medea wielding her terrible magic. These are stories of power, cunning, and the thin line between heroism and violence.",
        "reflection": "Heroes in Ovid are complex -- Mercury is a thief, Perseus turns people to stone, Medea's magic serves both love and murder. What makes someone a hero when the tools of salvation and destruction are the same?",
        "keywords": ["heroes", "gods", "Perseus", "Apollo", "Mercury", "Medea", "power"]
    },
    "grief-and-loss": {
        "name": "Grief, Loss, and Mourning",
        "about": "Some of Ovid's most poignant tales center on irreversible loss: Phaethon's sisters weeping until they become trees, Cycnus dissolved in grief, Cadmus and Harmonia losing everything, Cephalus accidentally killing Procris. Grief itself is a transformation.",
        "reflection": "Ovid shows grief as a force that literally reshapes the body. The Heliades weep until they become poplars. Niobe turns to stone but keeps weeping. What would it look like to honor grief rather than trying to escape it?",
        "keywords": ["grief", "loss", "mourning", "death", "transformation", "tears"]
    },
    "founding-myths": {
        "name": "Founding Myths and Civilization",
        "about": "The stories behind cities, nations, and institutions: Cadmus founding Thebes from dragon's teeth, the Argonauts setting sail, Triptolemus bringing agriculture to humankind, Theseus returning to Athens. These are tales of how the world we know came to be.",
        "reflection": "Every civilization begins with a myth of origin. Thebes grows from a dragon's teeth sown in the earth -- violence and creation intertwined. What founding stories shape your own sense of home and belonging?",
        "keywords": ["founding", "civilization", "Thebes", "Argonauts", "agriculture", "origins"]
    }
}

# Book summaries for L2
BOOK_SUMMARIES = {
    1: {
        "name": "Book I: Creation, Chaos, and the First Transformations",
        "about": "From the creation of the world out of Chaos to the first love stories of the gods. Book I establishes the grand arc: the universe forms, humanity rises and falls, the gods intervene, and love begins its work of transformation. Features the creation, the Four Ages, the Great Flood, Apollo and Daphne, and Io.",
        "reflection": "Book I moves from cosmic scale to intimate desire. The same forces that separate sea from sky also drive Apollo to chase Daphne. What connects the ordering of the universe to the chaos of love?"
    },
    2: {
        "name": "Book II: Fire, Jealousy, and the Transforming Sky",
        "about": "Phaethon's catastrophic ride across the sky sets the tone for a book dominated by celestial transformations. Stars are made from Callisto and Arcas, ravens turn black, and Mercury conducts his divine mischief. Europa is carried across the sea by Jupiter disguised as a bull.",
        "reflection": "Book II is full of boundary crossings -- between earth and sky, mortal and divine, male and female, white and black. Phaethon reaches too high; Europa is carried too far. Where are the boundaries in your life that beckon and terrify?"
    },
    3: {
        "name": "Book III: Thebes, Identity, and Dangerous Seeing",
        "about": "The founding and early tragedies of Thebes. Cadmus kills a dragon and builds a city; his grandson Actaeon sees what he shouldn't; Narcissus falls in love with his own reflection; Pentheus refuses to see what he must. Seeing and being seen carry mortal consequences.",
        "reflection": "Book III asks: what happens when you see the truth? Actaeon sees Diana and is destroyed. Narcissus sees himself and wastes away. Pentheus refuses to see Bacchus and is torn apart. How does seeing -- really seeing -- change you?"
    },
    4: {
        "name": "Book IV: Love, Madness, and the Sea",
        "about": "Stories told during the forbidden festival of Bacchus: Pyramus and Thisbe, Mars and Venus, Salmacis and Hermaphroditus. The daughters of Minyas are punished for their defiance. Ino goes mad, Cadmus becomes a serpent, and Perseus begins his adventures with Medusa and Andromeda.",
        "reflection": "Book IV's stories are tales within tales, told by women who refuse to worship Bacchus. Their stories explore the boundaries of love and identity, while their own defiance demonstrates the danger of refusing to surrender to forces greater than oneself."
    },
    5: {
        "name": "Book V: Contests, Abductions, and the Underworld",
        "about": "Perseus petrifies his enemies, Pallas visits the Muses, and the great myth of Proserpina's abduction unfolds. Ceres searches the earth for her daughter while Cyane dissolves into water from grief. The Pierides challenge the Muses and lose everything.",
        "reflection": "Book V returns to the theme of contests -- between Perseus and Phineus, the Muses and Pierides, Ceres and Pluto. Every contest is also a transformation. Who wins when the prize is someone else's freedom?"
    },
    6: {
        "name": "Book VI: Weaving, Violence, and Artistic Rivalry",
        "about": "Arachne challenges Minerva to a weaving contest and pays the price. Niobe boasts of her children and loses them all. Tereus commits unspeakable violence against Philomela, who weaves her story into cloth. Art and violence intertwine.",
        "reflection": "Book VI is Ovid's meditation on art and power. Arachne weaves the gods' crimes honestly; Minerva weaves their glory. Philomela, silenced by violence, tells her story through weaving. Can art speak truths that words cannot?"
    },
    7: {
        "name": "Book VII: Magic, Plague, and Jealousy",
        "about": "Medea's powerful magic dominates the first half -- she helps Jason, rejuvenates Aeson, and murders Pelias. A devastating plague strikes Aegina, and new warriors spring from ants. Cephalus's tale of love, jealousy, and accidental death closes the volume.",
        "reflection": "Book VII shows power at its most ambiguous. Medea's magic can heal or destroy. The Myrmidons are born from ants but become warriors. Cephalus's perfect love becomes his greatest weapon. When does a gift become a curse?"
    }
}


def build_l1_items(books):
    """Build L1 items from parsed fables."""
    items = []
    sort_order = 0

    for book_num in sorted(books.keys()):
        fables = books[book_num]
        for fable in fables:
            key = (fable['book'], fable['fable_num'])

            if key not in FABLE_NAMES:
                print(f"  Warning: No name mapping for Book {fable['book']}, Fable {fable['fable_num']} - skipping")
                continue

            name, item_id, keywords, theme = FABLE_NAMES[key]
            synopsis, story = extract_synopsis_and_story(fable['raw_text'])

            if not story.strip():
                print(f"  Warning: Empty story for {item_id}")
                continue

            # Determine the transformation that occurs
            transformation = synopsis if synopsis else "A metamorphosis unfolds."

            sections = {
                "Story": story,
                "Transformation": transformation,
                "Reflection": generate_reflection(item_id, name, keywords)
            }

            item = {
                "id": item_id,
                "name": name,
                "sort_order": sort_order,
                "level": 1,
                "category": f"book-{fable['book']}",
                "sections": sections,
                "keywords": keywords,
                "metadata": {
                    "source": "Metamorphoses, trans. Henry T. Riley, 1851",
                    "book": fable['book'],
                    "fable_number": fable['fable_num'],
                    "theme": theme
                }
            }

            items.append(item)
            sort_order += 1

    return items


def generate_reflection(item_id, name, keywords):
    """Generate a reflection question for each myth."""
    reflections = {
        "invocation": "What would it mean to tell the story of all change? Every narrative begins with an invocation -- a call for help from forces greater than ourselves. What story are you asking the universe to help you tell?",
        "creation-from-chaos": "Before there was order, there was everything and nothing at once. Chaos is not emptiness but fullness without form. What in your life is waiting to be separated into its proper elements?",
        "ordering-of-the-world": "Creation requires both a divine spark and the raw material of earth and water. We are shaped from the world we inhabit. What elements have shaped you?",
        "four-ages": "We often feel we live in a fallen age. But Ovid reminds us that every age carries the seeds of the next. What golden qualities persist even in iron times?",
        "war-of-giants": "The Giants stacked mountains to reach heaven and were struck down. What towers are you building, and what are they really reaching for?",
        "wickedness-of-mankind": "Jupiter surveys humanity and finds it wanting. But who among the gods is truly blameless? When you judge others, what are you really measuring?",
        "council-of-gods": "Even the king of the gods calls a council before acting. Power without deliberation is mere violence. When do you pause to consult before acting?",
        "lycaon-wolf": "Lycaon tested Jupiter with human flesh and was made to match his inner nature. What would you become if your outer form reflected your inner truth?",
        "great-flood": "The flood destroys everything to make renewal possible. What needs to be washed away in your life so something new can grow?",
        "deucalion-pyrrha": "New life comes from casting stones behind them -- from letting go of the past. What would it mean to throw something behind you and trust what emerges?",
        "new-creation": "After catastrophe, life returns spontaneously from the warm mud. Nature does not wait for permission to create. Where is new life emerging unbidden in your world?",
        "apollo-slays-python": "Apollo's first great deed is killing the serpent of chaos. What dragons guard the threshold of your next transformation?",
        "apollo-daphne": "Apollo is the god of reason, yet love makes him irrational. Daphne would rather become a tree than surrender her autonomy. When has desire led you to chase what was not yours to have?",
        "io-jupiter": "Io is changed against her will, watched constantly, and yet eventually restored. What parts of yourself have you lost that might yet return?",
        "mercury-argus": "Mercury defeats the hundred-eyed watchman not through force but through story -- the tale of Syrinx lulls Argus to sleep. When has a story been more powerful than a weapon?",
        "syrinx-reeds": "Syrinx escapes Pan by becoming music itself. Sometimes the only way out is through -- through transformation into something entirely new. What would it mean to become your art?",
        "io-restored": "After suffering transformation and exile, Io is finally restored. Not all metamorphosis is permanent. What restoration are you waiting for?",
        "phaethon-parentage": "Phaethon needs to prove he is the Sun's son. What inheritance are you trying to claim, and what will it cost you?",
        "phaethon-chariot": "Phaethon asks for what he cannot handle and burns the world. The distance between desire and capacity can be catastrophic. Where do you need to know your limits?",
        "lament-phaethon": "Phaethon's sisters weep until they become trees, their tears hardening into amber. Grief that will not stop transforms the mourner. How has grief shaped you?",
        "cycnus-swan": "Cycnus grieves until he becomes a swan -- his sorrow becomes beauty. What beautiful thing has your suffering created?",
        "jupiter-surveys-damage": "After the fire, Jupiter walks the damaged earth to assess what can be saved. When have you surveyed the aftermath of a catastrophe in your own life?",
        "callisto-jupiter": "Callisto is punished for what was done to her, not what she chose. The powerful often blame those they harm. Where do you see the punished being blamed for the crimes of the powerful?",
        "crow-minerva": "The crow was punished for telling the truth. Sometimes honesty costs everything. When has speaking truth brought you consequences?",
        "raven-coronis": "The raven ignored the crow's warning and told Apollo of Coronis's betrayal. Not every truth needs to be reported. When is silence wiser than speech?",
        "birth-aesculapius": "From Coronis's death comes Aesculapius, the greatest healer. What healing has emerged from destruction in your life?",
        "ocyrhoe-prophecy": "Ocyrhoe is punished for speaking the future. Some knowledge is dangerous to share. What do you know that you dare not say?",
        "mercury-battus": "Battus promised silence but broke his word. Trust, once broken, turns the betrayer to stone. Where have broken promises hardened you?",
        "mercury-herse": "Aglauros is consumed by envy until she becomes a stone. Envy petrifies the soul before it petrifies the body. What envy is hardening your heart?",
        "rape-of-europa": "Europa is charmed by Jupiter's beauty as a bull and carried away. The most dangerous things often wear the most beautiful faces. What beauty has carried you farther than you intended to go?",
        "cadmus-dragon": "Cadmus kills the dragon and sows its teeth to grow warriors. From every monster defeated, something unexpected grows. What has grown from your victories?",
        "founding-thebes": "Thebes is built on dragon's blood and the labor of men born from teeth. Every civilization rests on violence and transformation. What foundations -- beautiful and terrible -- support your world?",
        "actaeon-diana": "Actaeon stumbles upon a truth he was never meant to see and is destroyed by it. Some encounters with the sacred are fatal. What sacred boundary have you approached?",
        "juno-semele": "Semele asks to see Jupiter in his true form and is incinerated. Some desires, granted, destroy us. What would it mean to see the truth of someone you love?",
        "tiresias": "Tiresias knows both sides of every question and is punished for his honesty. Wisdom comes at a price. What have you learned that cost you something precious?",
        "narcissus-echo": "Echo can only repeat what others say; Narcissus can only love himself. These are twin tragedies of communication. Where are you stuck repeating patterns, or trapped in self-regard?",
        "pentheus-bacchus": "Pentheus refuses to acknowledge the god of ecstasy and is torn apart. What are you refusing to see that may destroy you?",
        "sailors-bacchus": "The sailors try to kidnap a god and become dolphins. You cannot contain the divine in mortal nets. What have you tried to control that was beyond your power?",
        "pyramus-thisbe": "A wall separates the lovers; a misunderstanding kills them; their blood colors the mulberry. Love finds every crack in every wall, but miscommunication can be fatal. What wall stands between you and the one you love?",
        "mars-venus": "The gods laugh at Mars and Venus caught in Vulcan's net. Love exposed to public view becomes comedy. What private truth would change meaning if made public?",
        "sun-leucothoe": "The Sun, who sees everything, cannot resist desire. Even perfect vision does not protect against longing. What do you see clearly but cannot resist?",
        "clytie-sunflower": "Clytie turns her face forever toward the Sun who abandoned her. Unrequited love can become devotion or imprisonment. Where are you still turning toward someone who has turned away?",
        "salmacis-hermaphroditus": "Two become one in the pool of Salmacis. Union transforms both parties beyond recognition. How has merging with another changed who you are?",
        "daughters-of-minyas": "The sisters refuse to worship Bacchus and spin their tales instead. But the god of ecstasy cannot be denied through reason alone. When has your refusal to surrender brought unexpected consequences?",
        "ino-athamas": "Juno sends the Furies to drive Ino and Athamas mad. Divine anger destroys families. How do inherited patterns of rage play out in your own family?",
        "cadmus-harmonia-serpents": "After losing everything -- children, grandchildren, kingdom -- Cadmus and Harmonia become serpents together. What is left when everything is lost? Perhaps only each other.",
        "perseus-medusa": "Perseus defeats Medusa by looking at her reflection. Some dangers can only be faced indirectly. What in your life can you only approach sideways?",
        "perseus-andromeda": "Perseus rescues Andromeda from a sea monster, and even seaweed becomes coral at his touch. The hero transforms everything around him. How does your presence change the world you touch?",
        "battle-perseus-wedding": "Even at a wedding feast, violence erupts. Perseus turns his enemies to stone. The boundary between celebration and destruction is thinner than we think. When has joy turned suddenly to conflict?",
        "pallas-muses": "Pallas visits the Muses at their spring, created by Pegasus's hoof. Art and the sacred share the same source. Where do creativity and the divine meet in your life?",
        "pierides-challenge": "Nine sisters challenge the Muses and lose. The contest between mortal and divine art always has the same outcome -- but the mortal song is sometimes truer. When has losing a contest taught you more than winning?",
        "rape-of-proserpina": "Proserpina picks flowers and is swallowed by the earth. The underworld takes what it wants. What has been taken from you without warning?",
        "ceres-searches": "Ceres searches the whole earth for her daughter, and in her grief, nothing grows. A mother's grief can starve the world. What grief has left your world barren?",
        "triptolemus-agriculture": "Ceres gives Triptolemus the gift of agriculture -- civilization born from a mother's search for her child. What gifts have emerged from your deepest losses?",
        "pierides-magpies": "The Pierides become chattering magpies -- they keep their voices but lose their meaning. When has your speech become mere noise?",
        "arachne-minerva": "Arachne weaves the truth of the gods' crimes and is punished for her honesty and skill. She becomes a spider, weaving forever. What truth have you woven that the powerful did not want to see?",
        "niobe": "Niobe boasts of her fourteen children and loses them all. Pride in what we love makes us vulnerable. What do you treasure that you hold too tightly?",
        "lycian-peasants-frogs": "The peasants refuse Latona a drink of water and become frogs, croaking forever in the mud they guarded. Small cruelties carry large consequences. What small act of unkindness might transform you?",
        "marsyas": "Marsyas challenges Apollo to a musical contest and is flayed alive. The gods do not share glory gracefully. When have you competed against forces far beyond your power?",
        "tereus-philomela-procne": "Silenced by violence, Philomela weaves her story into cloth. Her art becomes her voice, her vengeance becomes transformation. What voice do you have when words are taken from you?",
        "boreas-orithyia": "The North Wind gives up persuasion and simply takes what he wants. Force is the last resort of those who cannot charm. When has patience given way to force in your life?",
        "argonauts-set-sail": "The Argonauts set sail for the Golden Fleece -- the first great collective quest. What journey are you being called to join?",
        "medea-jason": "Medea's love for Jason wars with her duty to her father. Love asks us to betray everything we know. What has love asked you to leave behind?",
        "medea-magic": "Medea can reverse aging and restore youth -- but the same power that heals can destroy. What power do you possess that could serve either purpose?",
        "medea-flight": "Medea flies over the earth, passing a catalogue of transformations. From above, the whole world is a tapestry of change. If you could see your life from a great height, what pattern would emerge?",
        "theseus-returns": "Theseus returns home and is almost poisoned by Medea before his father recognizes him. Recognition comes at the last possible moment. What recognition are you still waiting for?",
        "plague-aegina": "A plague devastates Aegina, killing nearly everyone. Aeacus prays and new people spring from ants. What has survived the plagues of your life, and what new forms have emerged?",
        "myrmidons": "Warriors born from ants retain the ants' industriousness and discipline. Our origins shape us even when we are transformed. What qualities from your origins persist in who you are now?",
        "cephalus-procris": "Cephalus tests his wife's fidelity by disguising himself, and the test destroys their trust. Some truths are better left unexamined. What relationship have you damaged by testing it?",
        "death-of-procris": "Cephalus calls to the breeze, Procris thinks he calls to a lover, and his javelin kills her by accident. Misunderstanding is the most tragic form of transformation. What misunderstanding haunts you?",
    }
    return reflections.get(item_id, f"What transformation does the story of {name} invite you to consider in your own life?")


def build_l2_book_items(books, l1_items):
    """Build L2 items for book groupings."""
    items = []
    sort_order = len(l1_items)

    for book_num in sorted(BOOK_SUMMARIES.keys()):
        info = BOOK_SUMMARIES[book_num]
        # Find all L1 items in this book
        book_item_ids = [item['id'] for item in l1_items if item['metadata'].get('book') == book_num]

        if not book_item_ids:
            continue

        item = {
            "id": f"book-{book_num}",
            "name": info["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "books",
            "composite_of": book_item_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": info["about"],
                "Reflection": info["reflection"]
            },
            "keywords": ["ovid", "metamorphoses", f"book-{book_num}"],
            "metadata": {
                "book": book_num
            }
        }
        items.append(item)
        sort_order += 1

    return items


def build_l2_theme_items(l1_items, sort_start):
    """Build L2 items for thematic groupings."""
    items = []
    sort_order = sort_start

    for theme_key, theme_info in THEMATIC_GROUPS.items():
        # Find all L1 items with this theme
        theme_item_ids = [
            item['id'] for item in l1_items
            if item['metadata'].get('theme') == theme_key
        ]

        if not theme_item_ids:
            continue

        item = {
            "id": f"theme-{theme_key}",
            "name": theme_info["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "themes",
            "composite_of": theme_item_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": theme_info["about"],
                "Reflection": theme_info["reflection"]
            },
            "keywords": theme_info["keywords"],
            "metadata": {
                "grouping": "thematic"
            }
        }
        items.append(item)
        sort_order += 1

    return items


def build_l3_items(l2_items, sort_start):
    """Build L3 meta-category items."""
    items = []

    book_ids = [item['id'] for item in l2_items if item['category'] == 'books']
    theme_ids = [item['id'] for item in l2_items if item['category'] == 'themes']

    if book_ids:
        items.append({
            "id": "meta-books",
            "name": "The Fifteen Books (I-VII)",
            "sort_order": sort_start,
            "level": 3,
            "category": "meta",
            "composite_of": book_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": "Ovid organized his Metamorphoses into fifteen books, of which this grammar contains the first seven (as translated by Henry T. Riley). Each book flows seamlessly into the next, creating a continuous narrative river from the creation of the world through the founding myths of Greece. The book divisions provide natural resting points in what is really one unbroken song of change.",
                "How to Use": "Read the books in order for Ovid's intended narrative flow, or dip into individual books that call to you. Book I for beginnings and creation. Book III for identity and self-knowledge. Book IV for tales of love and their costs. Book VI for art and its consequences."
            },
            "keywords": ["books", "structure", "narrative", "Ovid"],
            "metadata": {}
        })

    if theme_ids:
        items.append({
            "id": "meta-themes",
            "name": "Threads of Transformation",
            "sort_order": sort_start + 1,
            "level": 3,
            "category": "meta",
            "composite_of": theme_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": "Across all seven books, certain themes recur like threads in a vast tapestry: creation and cosmos, divine punishment, love's transforming power, the grief of loss, the founding of civilizations, and the deeds of heroes. These thematic groupings cut across Ovid's book structure to reveal deeper patterns -- the same forces acting again and again in different forms. Which is, of course, exactly what metamorphosis means.",
                "How to Use": "Browse by theme when you want to explore a particular dimension of transformation. 'Love and Metamorphosis' for stories of desire and its consequences. 'Divine Punishment and Hubris' when you need to think about power and its limits. 'Grief, Loss, and Mourning' when sorrow needs a mirror."
            },
            "keywords": ["themes", "patterns", "transformation", "metamorphosis"],
            "metadata": {}
        })

    return items


def build_grammar(books):
    """Assemble the complete grammar."""
    print("Building L1 items...")
    l1_items = build_l1_items(books)
    print(f"  Built {len(l1_items)} L1 items")

    print("Building L2 book items...")
    l2_books = build_l2_book_items(books, l1_items)
    print(f"  Built {len(l2_books)} L2 book items")

    print("Building L2 theme items...")
    l2_themes = build_l2_theme_items(l1_items, len(l1_items) + len(l2_books))
    print(f"  Built {len(l2_themes)} L2 theme items")

    l2_items = l2_books + l2_themes

    print("Building L3 meta items...")
    l3_items = build_l3_items(l2_items, len(l1_items) + len(l2_items))
    print(f"  Built {len(l3_items)} L3 items")

    all_items = l1_items + l2_items + l3_items

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Ovid (Publius Ovidius Naso)",
                    "date": "8 CE",
                    "note": "Original author of the Metamorphoses"
                },
                {
                    "name": "Henry T. Riley",
                    "date": "1851",
                    "note": "English prose translator"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure and editorial content"
                }
            ]
        },
        "name": "Ovid's Metamorphoses",
        "description": "The Metamorphoses of Ovid (Books I-VII), the great Roman poem of transformation, rendered into English prose by Henry T. Riley (1851). Spanning from the creation of the world out of Chaos to the magical flights of Medea, these 66 myths form a continuous river of change: gods become animals, mortals become trees, love becomes loss, and grief becomes landscape. Every story is a metamorphosis -- and every metamorphosis asks what it means to become something other than what you were. Source: Project Gutenberg eBook #21765 (https://www.gutenberg.org/ebooks/21765).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Arthur Rackham's illustrations for 'Tales from Shakespeare' and mythological subjects (early 1900s) -- atmospheric watercolors of classical scenes. John William Waterhouse's paintings of mythological subjects (1880s-1910s) -- Pre-Raphaelite oil paintings of Apollo, Narcissus, Hylas, etc. Gustave Dore's illustrations for classical texts -- dramatic engravings. Walter Crane's illustrations for classical mythology (1890s) -- decorative Arts and Crafts style. Virgil Solis woodcuts for the 1563 Frankfurt edition of the Metamorphoses -- the earliest major illustrated edition, 178 woodcuts, public domain. Bernard Salomon's woodcuts for the 1557 Lyon Metamorphoses -- elegant Renaissance illustrations, public domain.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "mythology",
            "transformation",
            "classical",
            "roman",
            "greek",
            "poetry",
            "love",
            "gods",
            "nature",
            "oracle",
            "wisdom"
        ],
        "roots": ["greek-philosophy", "mythology"],
        "shelves": ["wonder"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "animist",
        "cover_image_url": "",
        "items": all_items
    }

    return grammar


def main():
    print(f"Reading seed text from {SEED_FILE}...")
    with open(SEED_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    print("Stripping Gutenberg header/footer...")
    text = strip_gutenberg(text)

    print("Stripping front matter...")
    text = strip_front_matter(text)

    print("Parsing books and fables...")
    books = parse_books_and_fables(text)

    for book_num in sorted(books.keys()):
        fables = books[book_num]
        print(f"  Book {book_num}: {len(fables)} fables")

    grammar = build_grammar(books)

    print(f"\nWriting grammar to {OUTPUT_FILE}...")
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    total_items = len(grammar['items'])
    l1_count = sum(1 for item in grammar['items'] if item['level'] == 1)
    l2_count = sum(1 for item in grammar['items'] if item['level'] == 2)
    l3_count = sum(1 for item in grammar['items'] if item['level'] == 3)
    print(f"\nDone! Total items: {total_items} (L1: {l1_count}, L2: {l2_count}, L3: {l3_count})")


if __name__ == '__main__':
    main()
