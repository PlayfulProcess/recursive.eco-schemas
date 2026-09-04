#!/usr/bin/env python3
"""
Build script for The Spirits' Book by Allan Kardec.

Parses OCR text from Internet Archive (seeds/kardec-spirits-book) into
grammars/spirits-book-kardec/grammar.json.

The OCR quality is very poor, so this script:
1. Attempts to find major structural boundaries (Books, Chapters)
2. Extracts and cleans text between boundaries
3. Falls back to known-structure summaries if OCR text is too garbled

The Spirits' Book structure:
- Book One: First Causes (4 chapters)
- Book Two: The Spirit World (11 chapters, though some numbering varies)
- Book Three: Moral Laws (12 chapters)
- Book Four: Hopes and Consolations (2 chapters)
"""

import json
import os
import re
import sys

SEED_FILE = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'kardec-spirits-book')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'spirits-book-kardec')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'grammar.json')

# Minimum viable text length for a chapter extraction to be considered successful
MIN_CHAPTER_TEXT_LENGTH = 200

# ── Known structure of The Spirits' Book ─────────────────────────────────────
# Used as fallback if OCR extraction fails for a given chapter.

KNOWN_STRUCTURE = {
    "book-one": {
        "title": "First Causes",
        "chapters": [
            {
                "id": "god",
                "title": "God",
                "subtopics": "God and Infinity; Proofs of the Existence of God; Attributes of the Divinity; Pantheism",
                "summary": "Opens with the foundational question 'What is God?' and receives the answer: 'God is the Supreme Intelligence — First Cause of all things.' Explores infinity, proofs of God's existence through the argument from first cause and design, the divine attributes (eternal, immutable, immaterial, unique, all-powerful, just and good), and a refutation of pantheism — distinguishing God from the created universe.",
                "questions": "1-36"
            },
            {
                "id": "general-elements-of-the-universe",
                "title": "General Elements of the Universe",
                "subtopics": "Knowledge of the First Principles of Things; Spirit and Matter; Properties of Matter; Universal Space",
                "summary": "Examines the fundamental elements of creation: spirit and matter as the two general elements of the universe. Matter is not merely what our senses perceive but includes the universal cosmic fluid from which all material forms are derived. Spirit and matter are distinct but not opposed — they are instruments of God's will. Discusses the properties of matter, ponderable and imponderable, and the nature of universal space.",
                "questions": "17-33"
            },
            {
                "id": "creation",
                "title": "Creation",
                "subtopics": "Formation of Worlds; Production of Living Beings; Peopling of the Earth; Diversity of Human Races; Plurality of Worlds; The Biblical Account of Creation",
                "summary": "Addresses how worlds are formed — through the condensation of matter scattered in space, governed by the law of gravitation. Living beings arose from the primordial elements when the earth's conditions were suitable. Humanity appeared when the earth was ready to sustain human life. Affirms the plurality of inhabited worlds throughout the universe and reinterprets the Biblical creation account as allegorical rather than literal.",
                "questions": "34-59"
            },
            {
                "id": "vital-principle",
                "title": "The Vital Principle",
                "subtopics": "Organic and Inorganic Beings; Life and Death; Intelligence and Instinct",
                "summary": "Distinguishes organic from inorganic beings and examines the vital principle — the force that animates living bodies, distinct from both matter and spirit. Discusses how life and death operate, the nature of intelligence versus instinct in animals, and whether animals possess souls. Instinct is a rudimentary intelligence; human intelligence is a higher development that includes self-awareness and moral sense.",
                "questions": "60-75"
            }
        ]
    },
    "book-two": {
        "title": "The Spirit World",
        "chapters": [
            {
                "id": "spirits",
                "title": "Spirits",
                "subtopics": "Origin and Nature of Spirits; Primitive and Normal World; Form and Ubiquity of Spirits; The Perispirit; Different Orders of Spirits; Spirit-Hierarchy; Progression of Spirits; Angels and Demons",
                "summary": "Defines spirits as 'the intelligent beings of the creation' who populate the universe. Spirits are created simple and ignorant, with the aptitude for progress. They possess a semi-material envelope called the perispirit. The spirit hierarchy ranges from impure and lower spirits through good spirits to pure spirits, with progression always possible. 'Angels' are spirits who have reached the highest degree; 'demons' are imperfect spirits, not eternally condemned.",
                "questions": "76-131"
            },
            {
                "id": "incarnation-of-spirits",
                "title": "Incarnation of Spirits",
                "subtopics": "Aim of Incarnation; The Soul; Materialism",
                "summary": "Explains that incarnation — the union of spirit with a material body — is necessary for spirits to accomplish God's purposes and to progress. The soul is an incarnated spirit; the body is merely its envelope. Addresses materialist objections, affirming that thought is not a property of matter but of the spirit acting through the brain. The soul survives bodily death and retains its individuality.",
                "questions": "132-152"
            },
            {
                "id": "return-from-corporeal-to-spirit-life",
                "title": "Return from the Corporeal to the Spirit Life",
                "subtopics": "The Soul after Death; Separation of Soul and Body; Temporarily Confused State of the Soul after Death",
                "summary": "Describes what happens at death: the soul separates from the body and re-enters the spirit world. The separation may be gradual, and a period of confusion follows in which the spirit does not immediately understand its new situation. The duration and nature of this confusion depends on the moral state of the spirit — virtuous spirits recover quickly, while those attached to material life experience prolonged bewilderment.",
                "questions": "149-165"
            },
            {
                "id": "plurality-of-existences",
                "title": "Plurality of Existences",
                "subtopics": "Reincarnation; Justice of Reincarnation; Incarnation in Different Worlds; Progressive Transmigration; Fate of Children after Death; Sex in Spirits; Kinship and Filiation",
                "summary": "The central doctrine of Spiritism: spirits undergo multiple incarnations to progress toward perfection. Reincarnation explains apparent injustices — suffering in one life may be expiation for past wrongs. Spirits can incarnate on different worlds as they progress. Reincarnation is always progressive; spirits never retrograde to a lower form. Children who die young are spirits whose trial was brief. Spirit has no fixed sex.",
                "questions": "166-222"
            },
            {
                "id": "spirit-life",
                "title": "Spirit-Life",
                "subtopics": "Errant or Wandering Spirits; Transitional Worlds; Perceptions, Sensations, and Sufferings of Spirits; Choice of Earthly Trials; Relationships Beyond the Grave; Sympathies and Antipathies of Spirits; Remembrance of Corporeal Existence; Commemoration of the Dead",
                "summary": "Explores existence between incarnations. Errant spirits wander freely, choosing when and how to reincarnate. Transitional worlds serve as way-stations. Spirits experience sensations and can suffer — not physically but morally, through regret, remorse, and unfulfilled desire. Spirits choose their own trials before incarnating. Relationships continue beyond death; spirits are drawn together by sympathy and shared affection. Spirits remember past lives but this memory may be veiled during incarnation.",
                "questions": "223-329"
            },
            {
                "id": "return-to-corporeal-life",
                "title": "Return to Corporeal Life",
                "subtopics": "Preludes to Return; Union of Soul and Body; Moral and Intellectual Faculties; Influence of Organism; Idiocy and Madness; Infancy; Terrestrial Sympathies and Antipathies; Forgetfulness of the Past",
                "summary": "Details the process of reincarnation: a spirit preparing to incarnate feels an attraction to its future body from conception. The union of soul and body is complete at birth. Moral and intellectual faculties vary because they depend on both the spirit's development and the body's capacity. Physical impairments like idiocy constrain but do not diminish the spirit within. The forgetfulness of past lives during incarnation is providential — full memory would be an obstacle to present trials.",
                "questions": "330-399"
            },
            {
                "id": "emancipation-of-the-soul",
                "title": "Emancipation of the Soul",
                "subtopics": "Sleep and Dreams; Visits between Spirits of Living Persons; Transmission of Thought; Lethargy and Catalepsy; Somnambulism; Trance; Second-Sight",
                "summary": "During sleep, the spirit partially frees itself from the body and can travel, visit other spirits, and perceive things beyond the physical senses. Dreams are partly memories of the spirit's nocturnal excursions. Somnambulism, trance, and second-sight are forms of the soul's emancipation — the spirit perceives directly rather than through bodily organs. These phenomena demonstrate the independent existence of the soul.",
                "questions": "400-455"
            },
            {
                "id": "intervention-of-spirits",
                "title": "Intervention of Spirits in the Corporeal World",
                "subtopics": "Penetration of Our Thoughts by Spirits; Influence of Spirits on Our Thoughts and Actions; Possession; Guardian Angels; Influence of Spirits on Human Life Events; Spirits and Natural Phenomena; Spirits and War; Pacts with Spirits; Occult Power; Benedictions and Curses",
                "summary": "Spirits constantly influence the corporeal world: they perceive our thoughts, inspire us toward good or ill, and serve as guardian angels or tempters. Each person has a protecting spirit (guardian angel) assigned from birth. Spirits can influence events but cannot override free will or natural law. So-called 'possession' is the strong influence of an inferior spirit, not literal inhabitation. Pacts with spirits, sorcery, and talismans are superstitions or misunderstandings of spirit influence.",
                "questions": "456-549"
            },
            {
                "id": "occupations-and-missions-of-spirits",
                "title": "Occupations and Missions of Spirits",
                "subtopics": "Occupations of Spirits; Missions of Spirits; Spirits and Corporeal Events",
                "summary": "Spirits are not idle between incarnations — they have occupations suited to their degree of advancement. Higher spirits work for the progress of humanity, inspiring great works of art, science, and moral reform. Some spirits have specific missions they carry out across multiple incarnations. Spirits participate in maintaining the harmony of nature and can intervene in human affairs when permitted by God.",
                "questions": "558-584"
            },
            {
                "id": "the-three-reigns",
                "title": "The Three Reigns",
                "subtopics": "Minerals and Plants; Animals and Men; Metempsychosis",
                "summary": "Examines the relationship between the mineral, plant, and animal kingdoms and the spirit world. The vital principle exists in all living things but only becomes intelligence in animals and self-conscious intelligence in humans. Rejects classical metempsychosis (human souls passing into animal bodies) as misunderstood — spirit always progresses forward, never regresses to a lower form. The link between animals and humans is a mystery that will be revealed in time.",
                "questions": "585-613"
            }
        ]
    },
    "book-three": {
        "title": "Moral Laws",
        "chapters": [
            {
                "id": "divine-or-natural-law",
                "title": "Divine or Natural Law",
                "subtopics": "Characteristics of Natural Law; Source and Knowledge of Natural Law; Good and Evil; Divisions of Natural Law",
                "summary": "Establishes that divine law is written in human conscience and is the only true law. It is eternal, immutable, and universal — the same for all beings. Natural law encompasses all duties: toward God, toward oneself, and toward one's neighbor. Good is whatever conforms to God's law; evil is whatever deviates from it. The moral laws are divided into ten categories covering every aspect of human conduct.",
                "questions": "614-648"
            },
            {
                "id": "law-of-adoration",
                "title": "The Law of Adoration",
                "subtopics": "Aim of Adoration; External Acts of Adoration; Life of Contemplation; Prayer; Polytheism; Sacrifices",
                "summary": "True adoration is of the heart, not of external forms. God prefers sincere inner worship to elaborate ritual. Prayer is recommended not to change God's will but to draw the person closer to God and attract the assistance of good spirits. A life of pure contemplation without useful action is selfish. Polytheism arose from misunderstanding — attributing divine qualities to created things. Sacrifices, especially of living beings, are repugnant to God.",
                "questions": "649-673"
            },
            {
                "id": "law-of-labour",
                "title": "The Law of Labour",
                "subtopics": "Necessity of Labour; Limit of Labour; Rest",
                "summary": "Labour is a law of nature imposed on all incarnated beings. It is necessary for the body's maintenance and for the spirit's development. No one is exempt from the obligation to be useful. Rest is needed to restore the body's forces, but idleness is contrary to natural law. The limit of labour is determined by the body's capacity — overwork that destroys health is not God's will.",
                "questions": "674-685"
            },
            {
                "id": "law-of-reproduction",
                "title": "The Law of Reproduction",
                "subtopics": "Population of the Globe; Succession and Improvement of Races; Obstacles to Reproduction; Marriage and Celibacy; Polygamy",
                "summary": "Reproduction is a natural law ensuring the continuation of living beings. The earth can sustain its population when resources are wisely distributed. Marriage is a progressive institution moving toward true partnership. Voluntary celibacy as selfishness is contrary to natural law, but renunciation for the purpose of devoting oneself to the service of humanity is meritorious. Polygamy reflects an imperfect social state that will disappear with moral progress.",
                "questions": "686-701"
            },
            {
                "id": "law-of-preservation",
                "title": "The Law of Preservation",
                "subtopics": "Instinct of Self-Preservation; Means of Self-Preservation; Enjoyment of the Fruits of the Earth; Necessaries and Superfluities; Voluntary Privations and Mortifications",
                "summary": "Self-preservation is an instinct given to all living beings. God provides the means for sustaining life when used wisely. Enjoyment of earthly goods is permitted but excess is condemned. The distinction between necessaries and superfluities lies in motive — true need versus vanity. Voluntary bodily mortifications have no merit; what God values is mortification of pride and selfishness.",
                "questions": "702-727"
            },
            {
                "id": "law-of-destruction",
                "title": "The Law of Destruction",
                "subtopics": "Necessary Destruction and Unjustifiable Destruction; Destructive Calamities; War; Murder; Cruelty; Duelling; Capital Punishment",
                "summary": "Destruction is a law of nature necessary for regeneration and improvement. Natural calamities serve providential purposes though they appear cruel. War will disappear as humanity advances morally. Murder is always a crime — the worst violation of natural law. Cruelty reflects the dominance of animal nature over spiritual nature. Duelling is barbarism. Capital punishment will be abolished as civilisation progresses, for society has no right to take what it cannot give.",
                "questions": "728-769"
            },
            {
                "id": "social-law",
                "title": "Social Law",
                "subtopics": "Necessity of Social Life; Life of Isolation; Vow of Silence; Family Ties",
                "summary": "Social life is a law of nature — humans are made to live together and contribute to mutual progress. Voluntary isolation and vows of silence are contrary to natural law because they deprive others of the benefit one could render. The family is the natural unit of society and family ties are not mere conventions of social life but genuine spiritual bonds formed across multiple existences.",
                "questions": "766-775"
            },
            {
                "id": "law-of-progress",
                "title": "The Law of Progress",
                "subtopics": "State of Nature; March of Progress; Degenerate Peoples; Civilisation; Progress of Human Legislation; Influence of Spiritism upon Progress",
                "summary": "Progress is the law of nature — no one can stand still. The 'state of nature' idealized by some is actually the starting point of humanity, not a golden age. Civilisation, despite its imperfections, is a stage of advancement. Degenerate peoples have failed to progress, not regressed from a higher state. True civilisation is known by the moral development of its people. Spiritism aids progress by providing proof of the afterlife and the consequences of our actions.",
                "questions": "776-815"
            },
            {
                "id": "law-of-equality",
                "title": "The Law of Equality",
                "subtopics": "Natural Equality; Inequality of Aptitudes; Social Inequalities; Inequality of Riches; Trials of Riches and Poverty; Equality of Rights of Men and Women; Equality in Death",
                "summary": "All spirits are created equal — inequalities of earthly condition are trials chosen by the spirit or consequences of past lives. Social inequality is not of God's making but of human institutions. Wealth is a trial and a trust — the rich are stewards, not owners. Men and women are equal in the eyes of God; apparent differences in social position reflect human prejudice, not divine law. Death is the great equalizer, reminding us that all earthly distinctions are temporary.",
                "questions": "803-824"
            },
            {
                "id": "law-of-liberty",
                "title": "The Law of Liberty",
                "subtopics": "Natural Liberty; Slavery; Freedom of Thought; Freedom of Conscience; Free-Will; Fatality; Foreknowledge",
                "summary": "Liberty is a natural right. Slavery in all its forms is contrary to God's law and will disappear with moral progress. Freedom of thought is absolute and cannot be suppressed. Freedom of conscience is a corollary of free thought. Free-will is real — without it there would be no merit or blame. Fatality exists only in the choice of trials before incarnation; within earthly life, humans retain free will. Foreknowledge of the future is possible but does not negate free choice.",
                "questions": "825-872"
            },
            {
                "id": "law-of-justice-love-charity",
                "title": "The Law of Justice, of Love, and of Charity",
                "subtopics": "Natural Rights and Justice; Right of Property; Charity; Love of the Neighbour; Maternal and Filial Affection",
                "summary": "Justice is respect for the rights of others — its criterion is 'Do unto others as you would have them do unto you.' The right of property is legitimate when acquired through honest labour. Charity is the supreme law: love of one's neighbour, benevolence, indulgence, and forgiveness. This law encompasses all others and is the surest means of spiritual advancement. Maternal and filial affection are sacred bonds reflecting divine love.",
                "questions": "873-919"
            },
            {
                "id": "moral-perfection",
                "title": "Moral Perfection",
                "subtopics": "Virtues and Vices; The Passions; Selfishness; Characteristics of the Virtuous Man; Self-Knowledge",
                "summary": "Virtue is the habitual practice of good; vice is the habitual practice of evil. The passions are natural forces that become vices only through excess or misdirection. Selfishness is the greatest obstacle to human progress and the root of most moral evil. The truly virtuous person practises charity in the widest sense — in thought, word, and deed. Self-knowledge is the key to moral improvement; one must examine one's own conscience as rigorously as one judges others.",
                "questions": "893-919"
            }
        ]
    },
    "book-four": {
        "title": "Hopes and Consolations",
        "chapters": [
            {
                "id": "earthly-joys-and-sorrows",
                "title": "Earthly Joys and Sorrows",
                "subtopics": "Happiness and Unhappiness; Loss of Those We Love; Disappointments and Ingratitude; Antipathetic Unions; Fear of Death; Weariness of Life and Suicide",
                "summary": "Perfect happiness is impossible on earth — corporeal life is a trial or expiation. True happiness comes from a clear conscience and faith in the future. Loss of loved ones is painful but temporary — reunion in the spirit world is certain. Disappointments and ingratitude are trials that test our character. Antipathetic unions (unhappy marriages) are often the result of past-life choices. Fear of death diminishes with spiritual understanding. Suicide is always wrong — it solves nothing and creates new suffering in the spirit world.",
                "questions": "920-957"
            },
            {
                "id": "future-joys-and-sorrows",
                "title": "Future Joys and Sorrows",
                "subtopics": "Annihilation and the Future Life; Intuition of Future Joys and Sorrows; Intervention of God in Rewards and Punishments; Nature of Future Joys and Sorrows; Temporal Penalties; Expiation and Repentance; Duration of Future Penalties; Paradise, Hell, and Purgatory",
                "summary": "Annihilation after death is impossible — the spirit lives on. Future happiness consists in the knowledge of truth, love, and progressive union with God; future suffering consists in ignorance, regret, and moral isolation. God does not personally punish — suffering is the natural consequence of imperfection. Hell is not a place of eternal fire but a state of moral suffering that is always temporary. Purgatory is the state of expiation. All spirits eventually progress — there is no eternal damnation. Repentance is the first step toward rehabilitation.",
                "questions": "958-1019"
            }
        ]
    }
}


def clean_ocr_text(text):
    """Clean OCR artifacts from extracted text."""
    # Remove lines that are clearly page headers/footers
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip empty lines (will add controlled spacing later)
        if not stripped:
            cleaned_lines.append('')
            continue
        # Skip page numbers (standalone numbers)
        if re.match(r'^\d{1,3}$', stripped):
            continue
        # Skip lines that are mostly garbage characters
        alpha_chars = sum(1 for c in stripped if c.isalpha())
        if len(stripped) > 3 and alpha_chars / len(stripped) < 0.4:
            continue
        # Skip single-character lines
        if len(stripped) <= 2 and not stripped.isdigit():
            continue
        # Skip page headers like "GOD. 3" or "CREATION. 15" or "THE SPIRIT-WORLD, OR WORLD OF SPIRITS. 47"
        if re.match(r'^[A-Z][A-Z\s,.\-\']+\s+\d{1,3}\s*$', stripped):
            continue
        # Skip lines that are just roman numerals (page numbers)
        if re.match(r'^[xXvViIlL]+\s*$', stripped):
            continue
        # Skip header lines like "BOOK II. CHAP, VIII."
        if re.match(r'^BOOK\s+[IVX]+\.?\s+CHAP', stripped):
            continue
        cleaned_lines.append(line)

    text = '\n'.join(cleaned_lines)

    # Remove excessive blank lines (more than 2 in a row)
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Fix common OCR errors (conservative)
    # Fix "1s" -> "is" when it's clearly a word
    text = re.sub(r'\b1s\b', 'is', text)
    # Fix "1t" -> "it" when it's clearly a word
    text = re.sub(r'\b1t\b', 'it', text)
    # Fix "Ilis" -> "His"
    text = text.replace('Ilis', 'His')
    text = text.replace('Ile', 'He')
    # Fix "thes" at end of sentence -> "things" (common OCR error in this text)
    # Fix various garbled characters
    text = re.sub(r'[^\x20-\x7E\n]', '', text)  # Remove non-ASCII
    # Fix "mee" at start of lines (OCR artifact for "THE")
    text = re.sub(r'^mee\s+', '', text, flags=re.MULTILINE)

    # Collapse lines broken by hyphenation
    text = re.sub(r'-\s*\n\s*', '', text)

    return text.strip()


def extract_chapter_text(lines, start_line, end_line):
    """Extract and clean text for a chapter between line numbers."""
    chapter_lines = lines[start_line:end_line]
    raw_text = '\n'.join(chapter_lines)
    return clean_ocr_text(raw_text)


def find_chapter_boundaries(lines):
    """
    Find the line numbers where each chapter begins and ends.
    Returns a list of (book_key, chapter_idx, start_line, end_line) tuples.
    """
    # Define the markers we're looking for
    # These are approximate line numbers from our grep analysis
    book_markers = [
        (2835, "book-one"),    # BOOK FIRST.—CAUSES
        (4347, "book-two"),    # BOOK SECOND—THE SPIRIT-WORLD
        (15734, "book-three"), # BOOK THIRD—MORAL LAWS
        (21587, "book-four"),  # FOURTH BOOK.—HOPES AND
    ]

    # Chapter start lines (0-indexed), paired with book and chapter index
    chapter_starts = [
        # Book One
        ("book-one", 0, 2841),   # Ch I: God
        ("book-one", 1, 3145),   # Ch II: General Elements
        ("book-one", 2, 3509),   # Ch III: Creation
        ("book-one", 3, 4042),   # Ch IV: Vital Principle

        # Book Two
        ("book-two", 0, 4351),   # Ch I: Spirits
        ("book-two", 1, 5562),   # Ch II: Incarnation of Spirits
        ("book-two", 2, 6043),   # Ch III: Return from Corporeal to Spirit Life
        ("book-two", 3, 6448),   # Ch IV: Plurality of Existences
        ("book-two", 4, 8156),   # Ch V(VII): Spirit-Life (labeled VII in OCR)
        ("book-two", 5, 10243),  # Ch VI(VIII): Return to Corporeal Life
        ("book-two", 6, 11531),  # Ch VII(VIII): Emancipation of the Soul
        ("book-two", 7, 12787),  # Ch VIII(IX): Intervention of Spirits
        # Ch IX: Occupations and Missions — try to find it
        ("book-two", 9, 15083),  # Ch XI: The Three Reigns

        # Book Three
        ("book-three", 0, 15737),  # Ch I: Divine or Natural Law
        ("book-three", 1, 16268),  # Ch II: Law of Adoration
        ("book-three", 2, 16842),  # Ch III: Law of Labour
        ("book-three", 3, 17024),  # Ch IV: Law of Reproduction
        ("book-three", 4, 17274),  # Ch V: Law of Preservation
        ("book-three", 5, 17696),  # Ch VI: Law of Destruction
        ("book-three", 6, 18299),  # Ch VII: Social Law
        ("book-three", 7, 18452),  # Ch VIII: Law of Progress
        ("book-three", 8, 19100),  # Ch IX: Law of Equality
        ("book-three", 9, 19475),  # Ch X: Law of Liberty
        ("book-three", 10, 20457), # Ch XI: Law of Justice, Love, Charity
        ("book-three", 11, 20849), # Ch XII: Moral Perfection

        # Book Four
        ("book-four", 0, 21591),   # Ch I: Earthly Joys and Sorrows
        ("book-four", 1, 22539),   # Ch II: Future Joys and Sorrows
    ]

    # Calculate end lines: each chapter ends where the next begins
    boundaries = []
    for i, (book, ch_idx, start) in enumerate(chapter_starts):
        if i + 1 < len(chapter_starts):
            end = chapter_starts[i + 1][2]
        else:
            # Last chapter: end at the Conclusion or table of contents
            # The conclusion starts around line 24700
            end = min(len(lines), 24700)
        boundaries.append((book, ch_idx, start, end))

    return boundaries


def try_find_occupations_chapter(lines):
    """Try to find the Occupations and Missions chapter which has no clean CHAPTER marker."""
    for i, line in enumerate(lines[13500:15083], start=13500):
        if 'OCCUPATIONS' in line.upper() and 'MISSION' in line.upper():
            return i
        if 'OCCUPATIONS' in line.upper() and 'SPIRITS' in line.upper():
            return i
    return None


def build_grammar():
    """Build the grammar JSON from OCR text and known structure."""
    # Read the seed file
    with open(SEED_FILE, 'r', encoding='utf-8', errors='replace') as f:
        raw_text = f.read()

    lines = raw_text.split('\n')
    total_lines = len(lines)
    print(f"Read {total_lines} lines from seed file")

    # Try to find the Occupations chapter
    occ_line = try_find_occupations_chapter(lines)
    if occ_line:
        print(f"Found Occupations and Missions chapter at line {occ_line}")

    # Find chapter boundaries
    boundaries = find_chapter_boundaries(lines)

    # If we found the Occupations chapter, insert it
    if occ_line:
        # Insert before The Three Reigns (book-two, index 9)
        new_boundaries = []
        for b in boundaries:
            if b[0] == "book-two" and b[1] == 9:
                # Add occupations chapter before Three Reigns
                new_boundaries.append(("book-two", 8, occ_line, b[2]))
            new_boundaries.append(b)
        boundaries = new_boundaries

    # Extract text for each chapter
    chapter_texts = {}
    for book_key, ch_idx, start, end in boundaries:
        key = f"{book_key}-{ch_idx}"
        text = extract_chapter_text(lines, start - 1, end - 1)  # Convert to 0-indexed
        chapter_texts[key] = text
        print(f"  {key}: {len(text)} chars extracted (lines {start}-{end})")

    # Build items
    items = []
    sort_order = 0

    # L1 items: chapters
    for book_key, book_data in KNOWN_STRUCTURE.items():
        for ch_idx, chapter in enumerate(book_data["chapters"]):
            text_key = f"{book_key}-{ch_idx}"
            extracted_text = chapter_texts.get(text_key, "")

            # Decide whether to use extracted text or fallback summary
            use_extracted = len(extracted_text) >= MIN_CHAPTER_TEXT_LENGTH

            sections = {}
            sections["About"] = chapter["summary"]
            sections["Topics"] = chapter["subtopics"]

            if chapter.get("questions"):
                sections["Questions"] = f"Questions {chapter['questions']}"

            if use_extracted:
                # Clean and truncate very long texts
                cleaned = extracted_text
                # Remove the chapter heading itself from the text
                # (first few lines are usually the heading)
                heading_end = min(10, len(cleaned.split('\n')))
                text_lines = cleaned.split('\n')
                # Find where the actual Q&A content begins
                content_start = 0
                for i, line in enumerate(text_lines[:20]):
                    if re.match(r'^\d+\.?\s+', line.strip()):
                        content_start = i
                        break
                if content_start > 0:
                    cleaned = '\n'.join(text_lines[content_start:])
                else:
                    # Skip the first few header lines
                    cleaned = '\n'.join(text_lines[min(5, len(text_lines)):])

                # Trim to reasonable length for the JSON
                if len(cleaned) > 15000:
                    cleaned = cleaned[:15000] + "\n\n[Text truncated for length. The complete chapter continues with further Q&A on this topic.]"

                sections["Text"] = cleaned
                sections["Note"] = "This text was extracted from OCR and may contain artifacts, garbled characters, or formatting errors."
            else:
                sections["Note"] = "OCR text was too garbled to extract reliably. The summary above describes the chapter's content."

            item_id = f"{book_key}-{chapter['id']}"
            item = {
                "id": item_id,
                "name": chapter["title"],
                "sort_order": sort_order,
                "level": 1,
                "category": book_key,
                "sections": sections,
                "keywords": [kw.strip().lower() for kw in chapter["subtopics"].split(";")],
                "metadata": {
                    "source": "The Spirits' Book, Allan Kardec, trans. Anna Blackwell, 1875",
                    "book": book_data["title"],
                    "question_range": chapter.get("questions", "")
                }
            }
            items.append(item)
            sort_order += 1

    # L2 items: the four Books
    book_l2 = [
        {
            "id": "book-one",
            "name": "Book One: First Causes",
            "about": "The first book addresses the most fundamental questions of existence: the nature of God, the general elements of the universe, how creation works, and the vital principle that animates living beings. Through questions posed to the spirits and their answers, Kardec builds the metaphysical foundation of Spiritist doctrine — establishing God as the Supreme Intelligence and First Cause, matter and spirit as the two primary elements of creation, and the vital principle as the force connecting spirit to matter in organic beings.",
            "chapters": [f"book-one-{ch['id']}" for ch in KNOWN_STRUCTURE["book-one"]["chapters"]],
            "category": "books"
        },
        {
            "id": "book-two",
            "name": "Book Two: The Spirit World",
            "about": "The most extensive section of the work, Book Two maps the entire landscape of spirit existence: what spirits are, how they incarnate and why, what happens at death, the doctrine of reincarnation (plurality of existences), life between incarnations, the emancipation of the soul during sleep and trance states, how spirits intervene in the physical world, and the relationship between the mineral, plant, animal, and human kingdoms. This book contains the core Spiritist teachings on reincarnation, the spirit hierarchy, guardian angels, and the continuity of consciousness beyond death.",
            "chapters": [f"book-two-{ch['id']}" for ch in KNOWN_STRUCTURE["book-two"]["chapters"]],
            "category": "books"
        },
        {
            "id": "book-three",
            "name": "Book Three: Moral Laws",
            "about": "Book Three systematically presents the moral teachings of Spiritism through ten categories of divine or natural law. Beginning with the characteristics of natural law (eternal, universal, written in conscience), it proceeds through the laws of adoration, labour, reproduction, preservation, destruction, social life, progress, equality, liberty, and justice/love/charity, culminating in a chapter on moral perfection. The central teaching is that charity — understood as love of neighbour in thought, word, and deed — encompasses all other laws and is the surest path to spiritual advancement.",
            "chapters": [f"book-three-{ch['id']}" for ch in KNOWN_STRUCTURE["book-three"]["chapters"]],
            "category": "books"
        },
        {
            "id": "book-four",
            "name": "Book Four: Hopes and Consolations",
            "about": "The concluding book addresses the practical and existential concerns that follow from Spiritist doctrine: how to understand earthly suffering and joy, the fear of death, the tragedy of suicide, and the nature of future rewards and punishments. It dismantles the concept of eternal damnation, replacing it with a vision of progressive purification in which all spirits eventually advance. Paradise, hell, and purgatory are understood not as physical places but as states of the spirit — happiness arising from knowledge and love, suffering from ignorance and moral isolation, both always temporary.",
            "chapters": [f"book-four-{ch['id']}" for ch in KNOWN_STRUCTURE["book-four"]["chapters"]],
            "category": "books"
        }
    ]

    for bl2 in book_l2:
        item = {
            "id": bl2["id"],
            "name": bl2["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": bl2["category"],
            "composite_of": bl2["chapters"],
            "relationship_type": "emergence",
            "sections": {
                "About": bl2["about"],
                "How to Use": "Each chapter within this book can be explored individually as a self-contained teaching, or read in sequence to follow the logical progression of the Spiritist argument. The Q&A format makes it easy to find specific topics of interest."
            },
            "keywords": [],
            "metadata": {
                "source": "The Spirits' Book, Allan Kardec, trans. Anna Blackwell, 1875"
            }
        }
        items.append(item)
        sort_order += 1

    # L3 item: the complete work
    all_chapter_ids = []
    for book_key in ["book-one", "book-two", "book-three", "book-four"]:
        for ch in KNOWN_STRUCTURE[book_key]["chapters"]:
            all_chapter_ids.append(f"{book_key}-{ch['id']}")

    l3_item = {
        "id": "the-spirits-book",
        "name": "The Spirits' Book — Complete Work",
        "sort_order": sort_order,
        "level": 3,
        "category": "complete-work",
        "composite_of": ["book-one", "book-two", "book-three", "book-four"],
        "relationship_type": "emergence",
        "sections": {
            "About": "The Spirits' Book (Le Livre des Esprits), first published in 1857 by Allan Kardec, is the foundational text of Spiritism. Structured as 1,019 questions posed to spirits of high degree and transmitted through various mediums, it systematically addresses the nature of God, the origin and destiny of spirits, reincarnation, moral law, and the afterlife. Kardec — the pen name of Hippolyte Leon Denizard Rivail, a French educator and polymath — compiled, organized, and annotated these communications into a coherent philosophical system that has influenced millions, particularly in Brazil where Spiritism remains a major spiritual movement. The work bridges Enlightenment rationalism with spiritual inquiry, presenting its teachings as a science of the spirit rather than a dogmatic religion.",
            "Structure": "The work is divided into four books: First Causes (metaphysics and cosmology), The Spirit World (the nature of spirits, reincarnation, and the afterlife), Moral Laws (a systematic ethical framework in ten laws), and Hopes and Consolations (practical guidance on suffering, death, and future existence). The Q&A format — question from Kardec, answer from the spirits, followed by Kardec's commentary — creates a dialectical structure that anticipates objections and builds understanding progressively.",
            "Historical Context": "Published two years before Darwin's Origin of Species and contemporary with the great age of Spiritualism in Europe and America, The Spirits' Book distinguished itself from mere table-turning and seances by insisting on rational examination of spirit communications. Kardec treated the phenomena as empirical data to be systematized, not as entertainment or superstition. The book went through multiple French editions in Kardec's lifetime and was translated into English by Anna Blackwell in 1875.",
            "How to Use": "This grammar can be explored by browsing individual chapters on topics of interest (the Q&A format makes each chapter relatively self-contained), by following the four-book structure from metaphysics through ethics to consolation, or by drawing a random chapter as a 'spiritual reading' for reflection. The teachings on reincarnation, moral law, and the nature of suffering remain startlingly relevant."
        },
        "keywords": ["spiritism", "reincarnation", "moral law", "afterlife", "God", "philosophy", "ethics"],
        "metadata": {
            "source": "The Spirits' Book, Allan Kardec, trans. Anna Blackwell, 1875",
            "original_title": "Le Livre des Esprits",
            "original_language": "French",
            "total_questions": "1,019"
        }
    }
    items.append(l3_item)

    # Build the grammar
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Allan Kardec",
                    "date": "1857",
                    "note": "Author (pen name of Hippolyte Leon Denizard Rivail)"
                },
                {
                    "name": "Anna Blackwell",
                    "date": "1875",
                    "note": "English translator"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar construction"
                }
            ]
        },
        "name": "The Spirits' Book",
        "description": "The foundational text of Spiritism by Allan Kardec (1857), structured as 1,019 questions posed to spirits and their answers, covering God, the spirit world, reincarnation, moral laws, and the afterlife. Translated by Anna Blackwell (1875). Source: Internet Archive OCR text (https://archive.org/details/AllanKardecTheSpiritsBook). Note: The source text was obtained via OCR from a scanned Internet Archive copy and contains artifacts and garbled passages; chapter summaries have been provided alongside extracted text to ensure readability.\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Engravings from 19th-century French Spiritist publications, particularly those from the Revue Spirite (founded by Kardec in 1858). Portraits of Allan Kardec from the 1860s-1870s — widely reproduced, public domain. Illustrations from early editions published by Didier et Cie, Paris. Symbolic and allegorical engravings of spirit communication, table-turning, and the afterlife from 19th-century Spiritualist and Spiritist literature.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "spiritism",
            "philosophy",
            "spirituality",
            "Kardec",
            "afterlife",
            "ethics",
            "public-domain",
            "full-text"
        ],
        "roots": [
            "mysticism",
            "european-tradition"
        ],
        "shelves": [
            "wisdom",
            "contested"
        ],
        "lineages": [
            "Shrei"
        ],
        "worldview": "spiritist",
        "cover_image_url": "",
        "items": items
    }

    return grammar


def main():
    grammar = build_grammar()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Write grammar
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Validate
    item_ids = [item["id"] for item in grammar["items"]]
    print(f"\nGenerated {len(grammar['items'])} items:")
    print(f"  L1 (chapters): {sum(1 for i in grammar['items'] if i['level'] == 1)}")
    print(f"  L2 (books): {sum(1 for i in grammar['items'] if i['level'] == 2)}")
    print(f"  L3 (complete): {sum(1 for i in grammar['items'] if i['level'] == 3)}")

    # Check for duplicate IDs
    seen = set()
    dupes = []
    for iid in item_ids:
        if iid in seen:
            dupes.append(iid)
        seen.add(iid)
    if dupes:
        print(f"\n  WARNING: Duplicate IDs found: {dupes}")
    else:
        print("  No duplicate IDs.")

    # Check composite_of references
    id_set = set(item_ids)
    bad_refs = []
    for item in grammar["items"]:
        if "composite_of" in item:
            for ref in item["composite_of"]:
                if ref not in id_set:
                    bad_refs.append((item["id"], ref))
    if bad_refs:
        print(f"\n  WARNING: Broken composite_of references: {bad_refs}")
    else:
        print("  All composite_of references valid.")

    print(f"\nGrammar written to {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE):,} bytes")


if __name__ == "__main__":
    main()
