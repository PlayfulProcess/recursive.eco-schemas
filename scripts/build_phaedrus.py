#!/usr/bin/env python3
"""
Build grammar.json for Plato's Phaedrus from seed text.

The Phaedrus (c. 370 BCE) is a dialogue between Socrates and Phaedrus
about love, beauty, the soul, and the art of rhetoric. Translated by Benjamin Jowett.

Structure:
- Gutenberg header/footer (stripped)
- Jowett's Introduction (stripped - editorial commentary)
- The dialogue proper, segmented by major thematic movements

Key text boundaries in the dialogue:
- Line ~1394: "PERSONS OF THE DIALOGUE" - dialogue begins
- Line ~1570: "Listen. You know how matters stand" - Lysias' speech begins
- Line ~1700: "Indeed, you are pleased to be merry" - Lysias' speech ends, critique begins
- Line ~1810: "I will veil my face" - Socrates' first speech begins
- Line ~2028: "I mean to say that as I was about to cross" - Socrates feels the sign, first speech ends
- Line ~2116: "Know then, fair youth" - The Great Speech (Palinode) begins
- Line ~2602: "And thus, dear Eros, I have made and paid my recantation" - Palinode ends
- Line ~2615: Transition to rhetoric discussion
- Line ~3529: "At the Egyptian city of Naucratis" - Allegory of Theuth
- Line ~3717: "And now the play is played out" - transition to closing
- Line ~3778: "Beloved Pan" - closing prayer
"""

import json
import re
from pathlib import Path

SEED_PATH = Path(__file__).parent.parent / "seeds" / "phaedrus-plato.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "phaedrus-plato"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"


def read_and_extract():
    """Read seed text and extract the dialogue, stripping header/footer/introduction."""
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    start_marker = "\nPHAEDRUS\n\n\nPERSONS OF THE DIALOGUE"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK PHAEDRUS ***"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"Could not find dialogue boundaries. start={start_idx}, end={end_idx}")

    return text[start_idx:end_idx].strip()


def normalize(text):
    """Join lines within paragraphs, preserve paragraph breaks."""
    if not text:
        return ""
    text = text.strip()
    paragraphs = re.split(r'\n\n+', text)
    result = []
    for p in paragraphs:
        joined = ' '.join(line.strip() for line in p.split('\n') if line.strip())
        if joined:
            result.append(joined)
    return '\n\n'.join(result)


def extract_between(text, start, end):
    """Extract text between two markers. end=None means to end of text."""
    si = text.find(start)
    if si == -1:
        return None
    if end is None:
        return text[si:].strip()
    ei = text.find(end, si + len(start))
    if ei == -1:
        return None
    return text[si:ei].strip()


def clean_text(text):
    """Remove scholarly parenthetical notes, normalize whitespace."""
    if not text:
        return ""
    # Remove parenthetical scholarly cross-references (but keep normal parentheses)
    text = re.sub(r'\(compare [^)]+\)', '', text)
    text = re.sub(r'\(supra[^)]*\)', '', text)
    text = re.sub(r'\(Probably [^)]+\)', '', text)
    text = re.sub(r'\(A proverb[^)]+\)', '', text)
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def build_grammar():
    dialogue = read_and_extract()

    items = []
    so = 0

    def add_item(item):
        nonlocal so
        item["sort_order"] = so
        items.append(item)
        so += 1

    def ct(text):
        return normalize(clean_text(text)) if text else ""

    # =========================================================================
    # L1 ITEMS - Major sections of the dialogue
    # =========================================================================

    # 1. Opening: The Walk to the Ilissus
    t = extract_between(dialogue,
        "SOCRATES: My dear Phaedrus, whence come you",
        "PHAEDRUS: Listen. You know how matters stand with me")
    add_item({
        "id": "opening-walk",
        "name": "The Walk to the Ilissus",
        "level": 1,
        "category": "dialogue",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates encounters Phaedrus outside the city walls. Phaedrus has been listening to Lysias, the famous rhetorician, discourse on love. They walk together along the river Ilissus to a shady plane tree, where Socrates marvels at the beauty of nature -- a rare admission from one who usually stays within the city.",
            "Reflection": "What draws us out of our familiar paths? How does a change of setting open us to new ideas about love and beauty?"
        },
        "keywords": ["socrates", "phaedrus", "lysias", "ilissus", "nature", "walking"],
        "metadata": {"speakers": ["Socrates", "Phaedrus"]}
    })

    # 2. Speech of Lysias: The Non-Lover
    t = extract_between(dialogue,
        "PHAEDRUS: Listen. You know how matters stand with me",
        "PHAEDRUS: Indeed, you are pleased to be merry.")
    add_item({
        "id": "speech-lysias",
        "name": "The Speech of Lysias: In Praise of the Non-Lover",
        "level": 1,
        "category": "speeches-on-love",
        "sections": {
            "Passage": ct(t),
            "About": "Phaedrus reads aloud the speech of Lysias, which argues paradoxically that one should yield to the non-lover rather than the lover. The non-lover is rational, stable, and free from jealousy. This clever but shallow argument treats love as a disease to be avoided -- a position Socrates will systematically dismantle.",
            "Reflection": "When we argue against love in favor of reason, what are we really protecting? Is the fear of love's irrationality itself a kind of blindness?"
        },
        "keywords": ["lysias", "non-lover", "rhetoric", "rationality", "persuasion"],
        "metadata": {"speaker": "Lysias (read by Phaedrus)"}
    })

    # 3. Socrates' critique of Lysias and transition
    t = extract_between(dialogue,
        "PHAEDRUS: Indeed, you are pleased to be merry.",
        "SOCRATES: I will veil my face and gallop through")
    add_item({
        "id": "critique-transition",
        "name": "Socrates Challenges Lysias",
        "level": 1,
        "category": "dialogue",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates critiques Lysias' speech for its repetitiveness and lack of philosophical foundation. Phaedrus is initially defensive, but Socrates claims he can deliver a better speech on the same theme. Challenged and bound by oath, Socrates prepares to speak -- veiling his face in anticipation of what he is about to say.",
            "Reflection": "Why does Socrates feel the need to cover his face before speaking about love? What is the relationship between shame and truth-telling?"
        },
        "keywords": ["critique", "lysias", "rhetoric", "challenge", "oath"],
        "metadata": {"speakers": ["Socrates", "Phaedrus"]}
    })

    # 4. Socrates' First Speech: Love as Harmful Madness
    t = extract_between(dialogue,
        "SOCRATES: I will veil my face and gallop through",
        "SOCRATES: I mean to say that as I was about to cross the stream")
    add_item({
        "id": "speech-socrates-first",
        "name": "Socrates' First Speech: The Lover as Madman",
        "level": 1,
        "category": "speeches-on-love",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates, covering his face in shame, delivers his own speech arguing that the lover is a kind of madman -- driven by desire, possessive, jealous, and ultimately harmful to the beloved. He defines love as irrational desire that overpowers reasoned judgment. Yet Socrates feels uneasy: his inner voice (daimonion) tells him he has committed an offense against Love.",
            "Reflection": "Is there truth in the idea that love makes us possessive? When does devotion become domination? Socrates feels ashamed of his own argument -- what does that shame reveal?"
        },
        "keywords": ["socrates", "love", "madness", "desire", "reason", "shame", "daimonion"],
        "metadata": {"speaker": "Socrates"}
    })

    # 5. The Recantation Introduction
    t = extract_between(dialogue,
        "SOCRATES: I mean to say that as I was about to cross the stream",
        "SOCRATES: Know then, fair youth, that the former discourse")
    add_item({
        "id": "recantation-introduction",
        "name": "The Call to Recant: Socrates' Divine Sign",
        "level": 1,
        "category": "speeches-on-love",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates reports that his daimonion -- the divine sign that always forbids but never commands -- stopped him from leaving. He realizes both speeches have blasphemed against Eros. Like Stesichorus, who was blinded for reviling Helen and regained his sight through a palinode (recantation), Socrates must now make amends to Love. He will speak this time 'with forehead bold and bare.'",
            "Reflection": "Have you ever spoken against something sacred and felt the need to recant? What inner voice alerts us when we have wronged love?"
        },
        "keywords": ["daimonion", "recantation", "palinode", "stesichorus", "helen", "divine-sign"],
        "metadata": {"speaker": "Socrates"}
    })

    # 6. The Great Speech / Palinode - Part 1: The Soul's Immortality and Chariot
    t = extract_between(dialogue,
        "SOCRATES: Know then, fair youth, that the former discourse",
        "Thus far I have been speaking of the fourth and last kind of madness")
    add_item({
        "id": "palinode-soul-chariot",
        "name": "The Great Speech: The Chariot of the Soul",
        "level": 1,
        "category": "speeches-on-love",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates' palinode begins with proof of the soul's immortality: what is always in motion is immortal. The soul is like a charioteer driving a pair of winged horses -- one noble and obedient, the other unruly and base. Before birth, souls follow the gods in a great procession through the heavens, glimpsing the Forms of Beauty, Justice, and Truth beyond the vault of heaven. Those who see the most are born as philosophers; those who see less descend into lower lives across a cycle of ten thousand years.",
            "Reflection": "What if falling in love is actually remembering something eternal? How does the image of the charioteer speak to your own inner conflicts between aspiration and appetite?"
        },
        "keywords": ["soul", "chariot", "wings", "divine-madness", "beauty", "forms", "recollection", "immortality", "horses"],
        "metadata": {"speaker": "Socrates"}
    })

    # 7. The Palinode Part 2: Love as Recollection of Beauty
    t = extract_between(dialogue,
        "Thus far I have been speaking of the fourth and last kind of madness",
        "And thus, dear Eros, I have made and paid my recantation")
    add_item({
        "id": "palinode-love-beauty",
        "name": "Love as Recollection of Divine Beauty",
        "level": 1,
        "category": "speeches-on-love",
        "sections": {
            "Passage": ct(t),
            "About": "The fourth divine madness -- love -- is the greatest. When the soul beholds earthly beauty, it remembers the divine Beauty it once witnessed. The soul's wings begin to grow, causing a sweet pain and agitation we call 'falling in love.' The true lover, through discipline and philosophy, leads the beloved upward toward wisdom rather than downward into mere physical gratification. Lovers who master the unruly horse become 'winged' and free.",
            "Reflection": "What does it feel like when beauty stops you in your tracks? Is that moment a kind of remembering? How do we honor the divine in the people we love?"
        },
        "keywords": ["beauty", "recollection", "wings", "eros", "madness", "philosophy", "beloved"],
        "metadata": {"speaker": "Socrates"}
    })

    # 8. End of the Palinode and transition to rhetoric
    t = extract_between(dialogue,
        "And thus, dear Eros, I have made and paid my recantation",
        "SOCRATES: Every one is aware that about some things we are agreed")
    add_item({
        "id": "transition-to-rhetoric",
        "name": "From Love to Rhetoric: What Makes a Good Speech?",
        "level": 1,
        "category": "rhetoric",
        "sections": {
            "Passage": ct(t),
            "About": "The great speech concluded, Phaedrus and Socrates reflect on what made it so much more powerful than Lysias' speech. This leads naturally to the question: what is the art of good speaking and writing? Socrates suggests they examine both speeches as examples. The dialogue's famous turn from love to rhetoric begins here.",
            "Reflection": "Why did Socrates' speech move you more than Lysias'? What makes the difference between speech that merely persuades and speech that transforms?"
        },
        "keywords": ["rhetoric", "writing", "speech", "lysias", "comparison", "art"],
        "metadata": {"speakers": ["Socrates", "Phaedrus"]}
    })

    # 9. The art of rhetoric proper
    t = extract_between(dialogue,
        "SOCRATES: Every one is aware that about some things we are agreed",
        "SOCRATES: Then I perceive that the Nymphs of Achelous")
    add_item({
        "id": "art-of-rhetoric",
        "name": "True Rhetoric: Knowledge of the Soul",
        "level": 1,
        "category": "rhetoric",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates develops his theory of true rhetoric. The rhetorician must know the truth about the subject, must understand the different kinds of souls in the audience, and must match speech-types to soul-types. Rhetoric without philosophy is mere cookery -- a knack for flattery, not a genuine art. The method of collection and division (dialectic) is the philosopher's true tool.",
            "Reflection": "How do you speak differently to different people about the same truth? What is the difference between adjusting your message and manipulating your audience?"
        },
        "keywords": ["rhetoric", "soul", "truth", "dialectic", "collection", "division", "persuasion"],
        "metadata": {"speakers": ["Socrates", "Phaedrus"]}
    })

    # 10. The Cicadas and rhetoric continued
    t = extract_between(dialogue,
        "SOCRATES: Then I perceive that the Nymphs of Achelous",
        "SOCRATES: Enough appears to have been said by us of a true and false art")
    add_item({
        "id": "cicadas-rhetoric",
        "name": "The Myth of the Cicadas",
        "level": 1,
        "category": "rhetoric",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates tells how cicadas were once humans so enchanted by the Muses' song that they forgot to eat and died singing. They were reborn as cicadas, who need no sustenance but song, and report to the Muses which humans honor their arts. This charming myth frames the ongoing discussion of what rhetoric requires -- not just technique, but genuine knowledge.",
            "Reflection": "Have you ever been so absorbed in discourse or beauty that you forgot your bodily needs? What do the cicadas teach us about the dangers and glories of intellectual passion?"
        },
        "keywords": ["cicadas", "muses", "song", "rhetoric", "enchantment", "discourse"],
        "metadata": {"speaker": "Socrates"}
    })

    # 11. Writing vs. Speech - Allegory of Theuth
    t = extract_between(dialogue,
        "SOCRATES: Enough appears to have been said by us of a true and false art",
        "SOCRATES: He would be a very simple person")
    add_item({
        "id": "allegory-theuth",
        "name": "The Allegory of Theuth: Writing and Memory",
        "level": 1,
        "category": "rhetoric",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates tells the Egyptian myth of Theuth (Thoth), who invented writing and presented it to King Thamus as a gift that would improve memory and wisdom. Thamus rejected the claim: writing would produce forgetfulness, not memory, for people would rely on external marks rather than internal understanding. Written words are like paintings -- they seem alive but cannot answer questions.",
            "Reflection": "Does writing (or any recording technology) genuinely preserve wisdom, or does it create an illusion of knowledge? What can only be learned through living conversation?"
        },
        "keywords": ["writing", "memory", "theuth", "thamus", "egypt", "technology", "knowledge"],
        "metadata": {"speaker": "Socrates"}
    })

    # 12. The Living Word vs. the Written Word
    t = extract_between(dialogue,
        "SOCRATES: He would be a very simple person",
        "SOCRATES: And now the play is played out")
    add_item({
        "id": "living-word",
        "name": "The Living Word: Writing in the Soul",
        "level": 1,
        "category": "rhetoric",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates distinguishes between the written word and the living word 'written in the soul of the learner.' The true rhetorician plants seeds of knowledge in receptive souls through dialectic. Written words are the 'garden of letters' -- pleasant to cultivate but not the serious work of philosophy. The philosopher writes for play, storing up reminders for old age.",
            "Reflection": "What is the relationship between words on a page and wisdom in a life? Where in your experience has a living conversation changed you in ways that reading never could?"
        },
        "keywords": ["living-word", "soul", "dialectic", "philosophy", "writing", "seeds"],
        "metadata": {"speakers": ["Socrates", "Phaedrus"]}
    })

    # 13. Closing: The Prayer to Pan
    t = extract_between(dialogue,
        "SOCRATES: And now the play is played out",
        None)
    add_item({
        "id": "prayer-to-pan",
        "name": "The Prayer to Pan",
        "level": 1,
        "category": "dialogue",
        "sections": {
            "Passage": ct(t),
            "About": "The dialogue ends with one of the most beautiful prayers in Western literature. Socrates asks Pan for inner beauty, harmony between outer and inner self, and only as much wealth as a wise person needs. Phaedrus asks for the same, invoking the proverb that friends share everything. They depart together, their conversation complete.",
            "Reflection": "What would it mean for your outward and inward self to be at one? What is 'enough' -- in gold, in knowledge, in love?"
        },
        "keywords": ["pan", "prayer", "beauty", "harmony", "temperance", "friendship", "closure"],
        "metadata": {"speakers": ["Socrates", "Phaedrus"]}
    })

    # =========================================================================
    # L2 ITEMS - Thematic groupings
    # =========================================================================

    add_item({
        "id": "theme-love-speeches",
        "name": "The Three Speeches on Love",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "The first half of the Phaedrus presents three speeches on love in ascending order of truth: Lysias argues for the non-lover (mere calculation), Socrates first argues against the lover (love as harmful madness), then recants with his Great Speech (love as divine madness that returns the soul to beauty). Together they enact the philosophical journey from surface cleverness to genuine wisdom.",
            "For Readers": "Read these three speeches as a progression. Notice how each builds on and transforms the previous one. The movement from Lysias' cold rationality to Socrates' vision of love as cosmic force mirrors the soul's own ascent toward truth."
        },
        "keywords": ["love", "speeches", "eros", "progression", "wisdom"],
        "metadata": {},
        "composite_of": ["speech-lysias", "speech-socrates-first", "recantation-introduction", "palinode-soul-chariot", "palinode-love-beauty"]
    })

    add_item({
        "id": "theme-rhetoric-truth",
        "name": "Rhetoric, Dialectic, and the Written Word",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "The second half turns from love to rhetoric, but the connection is deep: both require genuine knowledge of the soul. True rhetoric is not manipulation but a form of love -- the desire to lead another soul toward truth. The discussion culminates in the myth of Theuth and the superiority of living dialogue over dead letters.",
            "For Readers": "These sections are surprisingly relevant to our digital age. Consider Plato's warnings about writing in light of our own information technologies. Does the abundance of written (and now digital) text make us wiser, or does it substitute the appearance of knowledge for the reality?"
        },
        "keywords": ["rhetoric", "dialectic", "writing", "truth", "soul", "philosophy"],
        "metadata": {},
        "composite_of": ["transition-to-rhetoric", "art-of-rhetoric", "cicadas-rhetoric", "allegory-theuth", "living-word"]
    })

    add_item({
        "id": "theme-frame-setting",
        "name": "The Sacred Setting: Nature and Prayer",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "The dialogue is uniquely set outside the city walls, along the river Ilissus under a great plane tree. Socrates, who famously never leaves Athens, is drawn into nature by the promise of discourse about love. The setting is not mere backdrop -- the beauty of the natural world mirrors the beauty that love reveals in the soul. The closing prayer to Pan sanctifies the entire conversation.",
            "For Readers": "Pay attention to how setting shapes philosophical insight. The Phaedrus suggests that some truths can only be discovered outside our habitual environments, in places of natural beauty where the divine is close."
        },
        "keywords": ["nature", "ilissus", "plane-tree", "pan", "setting", "sacred"],
        "metadata": {},
        "composite_of": ["opening-walk", "critique-transition", "prayer-to-pan"]
    })

    # =========================================================================
    # L3 ITEMS - Meta-categories
    # =========================================================================

    add_item({
        "id": "meta-love-and-truth",
        "name": "Love and Truth: The Unity of the Phaedrus",
        "level": 3,
        "category": "meta-category",
        "sections": {
            "About": "The Phaedrus weaves together love, rhetoric, philosophy, and the soul into a single vision. Love is the experience of divine beauty; rhetoric is the art of soul-leading; philosophy is the discipline of truth; and the soul is the arena where all three meet. What unites them is the conviction that genuine relationship -- between lovers, between speaker and listener, between teacher and student -- requires knowledge of the other's soul and fidelity to truth.",
            "For Readers": "The Phaedrus is Plato's most intimate and personal dialogue. It is also his meditation on whether philosophy can be transmitted at all. Read it as a love letter to the philosophical life -- one that doubts its own medium (writing) even as it creates an imperishable work of written art."
        },
        "keywords": ["unity", "love", "truth", "rhetoric", "soul", "philosophy", "plato"],
        "metadata": {},
        "composite_of": ["theme-love-speeches", "theme-rhetoric-truth", "theme-frame-setting"]
    })

    # =========================================================================
    # BUILD GRAMMAR
    # =========================================================================

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Plato", "date": "c. 370 BCE", "note": "Author"},
                {"name": "Benjamin Jowett", "date": "1892", "note": "Translator"},
                {"name": "Project Gutenberg", "date": "1999", "note": "Source: eBook #1636 (https://www.gutenberg.org/ebooks/1636)"}
            ]
        },
        "name": "Phaedrus",
        "description": "Plato's dialogue on love, beauty, the soul, and rhetoric -- one of the most lyrical works in Western philosophy. Socrates and Phaedrus walk along the river Ilissus, deliver speeches on the nature of love, explore the myth of the winged soul, and debate whether writing can transmit genuine wisdom. Translated by Benjamin Jowett.\n\nSource: Project Gutenberg eBook #1636 (https://www.gutenberg.org/ebooks/1636)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Greek vase paintings depicting Eros and the soul; William Blake's illustrations of divine vision and the human form; Gustave Moreau's mythological paintings of divine love and madness (1880s); John Flaxman's neoclassical line illustrations of Greek philosophy (1793).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "love", "rhetoric", "soul", "plato", "socrates", "dialogue", "ancient-greece", "beauty", "divine-madness"],
        "roots": ["emotion-love"],
        "shelves": ["wonder"],
        "lineages": ["Shrei", "Johnson"],
        "worldview": "non-dual",
        "items": items
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"Built Phaedrus grammar: {len(items)} items")
    for item in items:
        passage = item["sections"].get("Passage", "")
        print(f"  L{item['level']}: {item['id']} - {item['name']} ({len(passage)} chars)")


if __name__ == "__main__":
    build_grammar()
