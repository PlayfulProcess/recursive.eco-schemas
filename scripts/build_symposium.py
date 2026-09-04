#!/usr/bin/env python3
"""
Build grammar.json for Plato's Symposium from seed text.

The Symposium (c. 385-370 BCE) is a dialogue about the nature of Love (Eros),
structured as a series of speeches at a banquet. Translated by Benjamin Jowett.

Structure:
- Gutenberg header/footer (stripped)
- Jowett's Introduction (stripped - editorial commentary)
- The dialogue proper with seven speeches on Love
"""

import json
import re
from pathlib import Path

SEED_PATH = Path(__file__).parent.parent / "seeds" / "symposium-plato.txt"
OUTPUT_PATH = Path(__file__).parent.parent / "grammars" / "symposium-plato" / "grammar.json"


def read_and_extract():
    """Read seed text and extract the dialogue, stripping header/footer/introduction."""
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    # Find dialogue boundaries
    start_marker = "\nSYMPOSIUM\n\n\nPERSONS OF THE DIALOGUE"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK SYMPOSIUM ***"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        raise ValueError("Could not find dialogue boundaries")

    return text[start_idx:end_idx].strip()


def clean_text(text):
    """Remove scholarly parenthetical references, normalize whitespace."""
    # Remove parenthetical scholarly cross-references
    text = re.sub(r'\(compare [^)]+\)', '', text)
    text = re.sub(r'\(supra[^)]*\)', '', text)
    text = re.sub(r'\(Probably [^)]+\)', '', text)
    text = re.sub(r'\(A fragment of [^)]+\)', '', text)
    text = re.sub(r'\(Eurip\.[^)]*\)', '', text)
    text = re.sub(r'\(Iliad[^)]*\)', '', text)
    text = re.sub(r'\(Odyssey[^)]*\)', '', text)
    text = re.sub(r'\(Rep\.[^)]*\)', '', text)
    text = re.sub(r'\(Arist\. [^)]*\)', '', text)
    text = re.sub(r'\(Greek\)', '', text)
    text = re.sub(r'\(Aesch\.[^)]*\)', '', text)
    text = re.sub(r'\(Gorg\.[^)]*\)', '', text)
    text = re.sub(r'\(In allusion [^)]+\)', '', text)
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


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


def build_grammar():
    dialogue = read_and_extract()
    # Don't clean yet -- we need exact markers. Clean each section individually.

    items = []
    so = 0  # sort_order counter

    def add_item(item):
        nonlocal so
        item["sort_order"] = so
        items.append(item)
        so += 1

    def ct(text):
        """Clean text of a section."""
        return normalize(clean_text(text)) if text else ""

    # =========================================================================
    # L1 ITEMS
    # =========================================================================

    # 1. Frame Narrative: Apollodorus
    t = extract_between(dialogue,
        "Concerning the things about which you ask",
        "He said that he met Socrates fresh from the bath")
    add_item({
        "id": "frame-apollodorus",
        "name": "Apollodorus Sets the Scene",
        "level": 1,
        "category": "frame-narrative",
        "sections": {
            "Passage": ct(t),
            "About": "Apollodorus, the devoted follower of Socrates, recounts the story of the famous banquet to a companion. He heard it from Aristodemus, who was present. The narrative frame establishes that this is a story told and retold -- a philosophical tradition passed down through imperfect memory and passionate devotion.",
            "Reflection": "How does the act of retelling shape philosophical truth? What is lost and what is gained when wisdom passes through multiple voices?"
        },
        "keywords": ["apollodorus", "aristodemus", "narration", "memory", "devotion"],
        "metadata": {"speaker": "Apollodorus"}
    })

    # 2. Setting: Arrival at the Banquet
    t = extract_between(dialogue,
        "He said that he met Socrates fresh from the bath",
        "Phaedrus began by affirming that Love is a mighty god")
    add_item({
        "id": "setting-banquet",
        "name": "The Banquet Begins",
        "level": 1,
        "category": "frame-narrative",
        "sections": {
            "Passage": ct(t),
            "About": "Aristodemus encounters Socrates freshly bathed and sandalled -- an unusual sight. They walk to Agathon's house, where the tragic poet celebrates his first victory. Socrates falls into a trance on a neighbor's porch, arriving late. The company agrees to give speeches in praise of Love rather than drinking heavily.",
            "Reflection": "The philosopher arrives late, lost in thought. The celebration of art gives way to philosophy. What does it mean that the search for truth begins at a party?"
        },
        "keywords": ["agathon", "banquet", "socrates", "aristodemus", "celebration", "trance"],
        "metadata": {"speaker": "Aristodemus/Narrator"}
    })

    # 3. Speech of Phaedrus
    t = extract_between(dialogue,
        "Phaedrus began by affirming that Love is a mighty god",
        "This, or something like this, was the speech of Phaedrus")
    # Include closing transition
    t2 = extract_between(dialogue,
        "This, or something like this, was the speech of Phaedrus",
        "Phaedrus, he said, the argument has not")
    full_phaedrus = (t or "") + "\n\nThis, or something like this, was the speech of Phaedrus."
    if t2:
        # Get just the transition, not Pausanias' speech
        transition = t2.split("Phaedrus, he said")[0]
        full_phaedrus += "\n\n" + transition

    add_item({
        "id": "speech-phaedrus",
        "name": "Speech of Phaedrus: Love as the Eldest God",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": ct(full_phaedrus),
            "Theme": "Love is the most ancient of the gods, the source of our greatest blessings. Love inspires courage: a lover would rather die than be seen as a coward by the beloved. Phaedrus invokes Alcestis, who died for her husband, and Achilles, who avenged Patroclus knowing it meant his own death.",
            "Key Insight": "The sense of honour and dishonour, which love inspires, is the foundation of all great works by individuals and states.",
            "Reflection": "What would you dare to do, or refuse to do, in the presence of someone whose opinion you truly valued?"
        },
        "keywords": ["phaedrus", "antiquity", "courage", "honour", "alcestis", "achilles", "patroclus"],
        "metadata": {"speaker": "Phaedrus", "speech_number": 1}
    })

    # 4. Speech of Pausanias
    t = extract_between(dialogue,
        "Phaedrus, he said, the argument has not",
        "he had the hiccough")
    add_item({
        "id": "speech-pausanias",
        "name": "Speech of Pausanias: The Two Loves",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": ct(t),
            "Theme": "There are two Aphrodites and therefore two Loves. The Heavenly Love, born of Uranus alone, is noble and intellectual, directed toward virtue and the mind. The Common Love, daughter of Zeus and Dione, is indiscriminate and bodily. Actions are neither good nor evil in themselves -- only the manner of their performance makes them so.",
            "Key Insight": "The noble lover attaches himself to the enduring character of the beloved, not to the fleeting beauty of the body. A voluntary service rendered for the sake of virtue and wisdom is always honourable.",
            "Reflection": "How do you distinguish between love that elevates and love that diminishes? What does it mean to love someone's character rather than their appearance?"
        },
        "keywords": ["pausanias", "heavenly-love", "common-love", "aphrodite", "virtue", "nobility", "two-loves"],
        "metadata": {"speaker": "Pausanias", "speech_number": 2}
    })

    # 5. Aristophanes' Hiccough Interlude
    t = extract_between(dialogue,
        "he had the hiccough",
        "Eryximachus spoke as follows:")
    add_item({
        "id": "interlude-hiccough",
        "name": "Aristophanes' Hiccough",
        "level": 1,
        "category": "interludes",
        "sections": {
            "Passage": ct(t),
            "About": "A comic interlude: Aristophanes has the hiccough and cannot speak. Eryximachus the physician prescribes remedies -- holding breath, gargling, sneezing -- and offers to speak in his place. The great comic playwright is rendered speechless by his own body, a fitting irony that Plato surely relished.",
            "Reflection": "Even at a philosophical banquet, the body interrupts the mind. What role does comedy play in the pursuit of truth?"
        },
        "keywords": ["aristophanes", "hiccough", "comedy", "eryximachus", "body", "interruption"],
        "metadata": {"speaker": "Aristophanes/Eryximachus"}
    })

    # 6. Speech of Eryximachus
    t = extract_between(dialogue,
        "Eryximachus spoke as follows:",
        "Aristophanes professed to open another vein of discourse")
    add_item({
        "id": "speech-eryximachus",
        "name": "Speech of Eryximachus: Love as Cosmic Harmony",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": ct(t),
            "Theme": "Love extends beyond human souls into all of nature -- animals, plants, and the cosmos itself. The physician sees two kinds of love in the body: healthy and diseased. Medicine, music, astronomy, and divination all work by reconciling opposites. Love is the universal principle of harmony that brings order out of discord.",
            "Key Insight": "The double love is not merely an affection of the soul toward the fair, but is to be found in all that is. Love is the reconciliation of opposites -- the harmony that succeeds discord.",
            "Reflection": "Where do you see opposing forces in your life that might be reconciled rather than conquered? What would it mean to see love as a principle of nature, not just a human emotion?"
        },
        "keywords": ["eryximachus", "medicine", "harmony", "opposites", "heraclitus", "nature", "cosmos", "music"],
        "metadata": {"speaker": "Eryximachus", "speech_number": 3}
    })

    # 7. Speech of Aristophanes
    t = extract_between(dialogue,
        "Aristophanes professed to open another vein of discourse",
        "Indeed, I am not going to attack you, said Eryximachus")
    add_item({
        "id": "speech-aristophanes",
        "name": "Speech of Aristophanes: The Origin of Love",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": ct(t),
            "Theme": "Originally humans were round, with four arms and four legs, two faces, and tremendous strength. There were three sexes: male, female, and androgynous. Zeus, fearing their power, split them in two. Ever since, each half wanders seeking its other half. Love is the name for this longing to be whole again -- the desire and pursuit of the whole.",
            "Key Insight": "Love is the desire of the whole, and the pursuit of the whole is called love. We are each but half a person, searching for the one who completes us.",
            "Reflection": "Do you recognize the longing Aristophanes describes -- the sense of incompleteness that seeks reunion? Is love truly about finding our 'other half,' or is that a beautiful myth?"
        },
        "keywords": ["aristophanes", "origin", "split-humans", "wholeness", "zeus", "androgynous", "desire", "reunion"],
        "metadata": {"speaker": "Aristophanes", "speech_number": 4}
    })

    # 8. Pre-Agathon Interlude
    t = extract_between(dialogue,
        "Indeed, I am not going to attack you, said Eryximachus",
        "The previous speakers, instead of praising the god Love")
    if t and len(t.strip()) > 100:
        add_item({
            "id": "interlude-pre-agathon",
            "name": "Before Agathon Speaks",
            "level": 1,
            "category": "interludes",
            "sections": {
                "Passage": ct(t),
                "About": "A brief exchange between the remaining speakers. Eryximachus praises Aristophanes' speech. Socrates and Agathon spar lightly about performance anxiety -- Agathon, who has faced the theatre crowd, should not fear a small party of friends. Phaedrus intervenes to keep them on task.",
                "Reflection": "How does the interplay between speakers shape the argument? Notice how Socrates is already shifting the terms of debate."
            },
            "keywords": ["agathon", "socrates", "dialogue", "theatre", "audience"],
            "metadata": {"speaker": "Various"}
        })

    # 9. Speech of Agathon
    t = extract_between(dialogue,
        "The previous speakers, instead of praising the god Love",
        "When Agathon had done speaking, Aristodemus said")
    add_item({
        "id": "speech-agathon",
        "name": "Speech of Agathon: Love as the Fairest God",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": ct(t),
            "Theme": "Agathon, the tragic poet, delivers an ornate, poetic speech. Love is not ancient but the youngest of the gods -- young, tender, flexible, dwelling among flowers and in the softest hearts. Love possesses all virtues: justice, temperance, courage, and wisdom. He is the supreme poet who inspires all creation.",
            "Key Insight": "Love is the fairest and best in himself, and the cause of what is fairest and best in all other things. He gives peace on earth and calms the stormy deep.",
            "Reflection": "Is Agathon's praise beautiful but empty, as Socrates will suggest? Or does poetic truth capture something that logical argument cannot?"
        },
        "keywords": ["agathon", "beauty", "youth", "poetry", "virtues", "justice", "temperance", "courage", "wisdom"],
        "metadata": {"speaker": "Agathon", "speech_number": 5}
    })

    # 10. Socrates Questions Agathon
    t = extract_between(dialogue,
        "When Agathon had done speaking, Aristodemus said",
        "And now, taking my leave of you, I would rehearse a tale of love")
    add_item({
        "id": "speech-socrates-questioning",
        "name": "Socrates Questions Agathon",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Passage": ct(t),
            "Theme": "Before his own speech, Socrates dismantles Agathon's praise through dialectic questioning. Love is of something -- it desires what it lacks. If Love desires beauty, Love itself cannot be beautiful. If the beautiful is the good, then Love lacks goodness too. Agathon gracefully concedes: 'I cannot refute you, Socrates.' Socrates replies: 'Say rather that you cannot refute the truth.'",
            "Key Insight": "Love is not the possession of beauty and goodness, but the desire for them. We do not desire what we already have. This simple distinction overturns all the previous speeches.",
            "Reflection": "What is the difference between praising something and understanding it? Does Socrates' method -- questioning rather than proclaiming -- get closer to truth?"
        },
        "keywords": ["socrates", "agathon", "dialectic", "desire", "lack", "truth", "questioning"],
        "metadata": {"speaker": "Socrates", "speech_number": 6}
    })

    # 11. Diotima: Nature of Love as Daimon
    # From start of Diotima narrative to the transition to "manner of the pursuit"
    t = extract_between(dialogue,
        "And now, taking my leave of you, I would rehearse a tale of love",
        "'Then if this be the nature of love, can you tell me further,")
    add_item({
        "id": "speech-diotima-nature",
        "name": "Diotima's Teaching: Love as Daimon",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": ct(t),
            "Theme": "Socrates recounts the teachings of Diotima of Mantinea, a wise woman who instructed him in the mysteries of love. Love is neither beautiful nor ugly, neither god nor mortal, but a great daimon -- a spirit intermediate between divine and human. Born of Plenty and Poverty at Aphrodite's birthday feast, Love is bold yet always in want, a philosopher who is neither wise nor ignorant but forever seeking wisdom.",
            "Key Insight": "Love is a great spirit, intermediate between the divine and the mortal. He interprets between gods and men, conveying prayers upward and commands downward. Through Love, all is bound together.",
            "Reflection": "What does it mean that love is not a god but an intermediary? How does Diotima's portrait of Love as a barefoot philosopher change the way we think about desire?"
        },
        "keywords": ["diotima", "daimon", "spirit", "poverty", "plenty", "intermediate", "philosopher", "wisdom"],
        "metadata": {"speaker": "Socrates/Diotima"}
    })

    # 12. Diotima: Love, Birth in Beauty, and Immortality
    t = extract_between(dialogue,
        "'Then if this be the nature of love, can you tell me further,",
        "'These are the lesser mysteries of love")
    if not t:
        t = extract_between(dialogue,
            "'Then if this be the nature of love, can you tell me further,",
            "These are the lesser mysteries of love")
    add_item({
        "id": "speech-diotima-immortality",
        "name": "Diotima's Teaching: Love and Immortality",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": ct(t),
            "Theme": "Love desires not merely the beautiful but the everlasting possession of the good -- this is happiness. Love is of birth in beauty, because all beings desire immortality. Mortal creatures achieve immortality through procreation: the body replaces itself constantly, and even knowledge must be continually renewed. Those pregnant in body beget children; those pregnant in soul create wisdom, virtue, poetry, and laws -- children of the mind more lasting than mortal offspring.",
            "Key Insight": "Love is not of beauty only, but of birth in beauty -- the principle of immortality in a mortal creature. Those creative in soul leave behind poems, laws, and philosophies more lasting than mortal offspring.",
            "Reflection": "What are you trying to bring to birth? Is your deepest desire for beauty, or for something beauty makes possible -- creation, legacy, immortality?"
        },
        "keywords": ["diotima", "immortality", "birth", "beauty", "creation", "soul", "procreation", "legacy"],
        "metadata": {"speaker": "Socrates/Diotima"}
    })

    # 13. Diotima: The Ladder of Beauty (Greater Mysteries)
    t = extract_between(dialogue,
        "'These are the lesser mysteries of love",
        "Such, Phaedrus--and I speak not only to you")
    if not t:
        t = extract_between(dialogue,
            "These are the lesser mysteries of love",
            "Such, Phaedrus--and I speak not only to you")
    add_item({
        "id": "speech-diotima-ladder",
        "name": "Diotima's Teaching: The Ladder of Beauty",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": ct(t),
            "Theme": "The summit of Diotima's teaching: the Greater Mysteries of Love. One begins by loving a single beautiful form, then perceives that all beauty is of one kindred. From beautiful bodies one ascends to beautiful minds, then to beautiful laws and institutions, then to the sciences. Finally, one beholds Beauty itself -- absolute, eternal, unchanging, the source of all particular beauties. This is the famous 'Ladder of Love.'",
            "Key Insight": "He who has been instructed thus far in the things of love, when he comes toward the end will suddenly perceive a nature of wondrous beauty -- everlasting, not growing and decaying, beauty absolute, separate, simple, and everlasting.",
            "Reflection": "Have you ever had a moment when the beauty of a particular thing opened into something universal? What would it mean to love Beauty itself, rather than any single beautiful thing?"
        },
        "keywords": ["diotima", "ladder", "ascent", "absolute-beauty", "contemplation", "eternal", "forms", "mysteries"],
        "metadata": {"speaker": "Socrates/Diotima"}
    })

    # 14. Socrates' Conclusion
    t = extract_between(dialogue,
        "Such, Phaedrus--and I speak not only to you",
        "When Socrates had done speaking, the company applauded")
    add_item({
        "id": "speech-socrates-conclusion",
        "name": "Socrates' Conclusion: Honour Love",
        "level": 1,
        "category": "speeches",
        "sections": {
            "Passage": ct(t),
            "About": "Socrates concludes by affirming Diotima's teaching: in the attainment of beauty and goodness, human nature will not easily find a helper better than Love. Every person ought to honour Love and walk in his ways.",
            "Reflection": "After all the elaborate speeches, Socrates ends with simplicity: honour love. What does it mean to walk in love's ways?"
        },
        "keywords": ["socrates", "conclusion", "honour", "love", "diotima"],
        "metadata": {"speaker": "Socrates"}
    })

    # 15. Arrival of Alcibiades
    t = extract_between(dialogue,
        "When Socrates had done speaking, the company applauded",
        "And now, my boys, I shall praise Socrates in a figure")
    add_item({
        "id": "arrival-alcibiades",
        "name": "The Arrival of Alcibiades",
        "level": 1,
        "category": "alcibiades",
        "sections": {
            "Passage": ct(t),
            "About": "The philosophical heights of Diotima's teaching are shattered by the eruption of the real world. Alcibiades bursts in drunk, crowned with ivy and violets, carried by a flute-girl and companions. He has come to crown Agathon but discovers Socrates beside him. A comic struggle ensues. Alcibiades proposes to praise not Love, but Socrates himself.",
            "Reflection": "After the ascent to eternal beauty, a drunk man stumbles in. What does Plato achieve by this dramatic contrast? Is Alcibiades the embodiment of earthly love breaking into philosophical abstraction?"
        },
        "keywords": ["alcibiades", "drunk", "arrival", "crown", "agathon", "socrates", "contrast"],
        "metadata": {"speaker": "Alcibiades"}
    })

    # 16. Alcibiades: Socrates as Silenus and Marsyas
    t = extract_between(dialogue,
        "And now, my boys, I shall praise Socrates in a figure",
        "And this is what I and many others have suffered from the flute-playing")
    add_item({
        "id": "speech-alcibiades-silenus",
        "name": "Alcibiades' Praise: Socrates as Silenus and Marsyas",
        "level": 1,
        "category": "alcibiades",
        "sections": {
            "Speech": ct(t),
            "Theme": "Alcibiades compares Socrates to the busts of Silenus -- ugly on the outside but containing golden images of the gods within. He is like Marsyas the satyr, but produces his enchantment with words alone, without a flute. Socrates' words shame Alcibiades, making him weep and feel that his life is not worth living. No other orator, not even Pericles, has this power.",
            "Key Insight": "The outward ugliness of Socrates conceals an inner divine beauty. His words possess souls and reveal truths that their hearers would rather not face.",
            "Reflection": "Have you ever encountered someone whose words made you ashamed of how you were living? What is the difference between persuasion and the kind of soul-shaking effect Alcibiades describes?"
        },
        "keywords": ["alcibiades", "silenus", "marsyas", "satyr", "enchantment", "words", "shame", "beauty-within"],
        "metadata": {"speaker": "Alcibiades", "speech_number": 7}
    })

    # 17. Alcibiades: The Inner Silenus and the Attempted Seduction
    t = extract_between(dialogue,
        "And this is what I and many others have suffered from the flute-playing",
        "All this happened before he and I went on the expedition\nto Potidaea")
    add_item({
        "id": "speech-alcibiades-personal",
        "name": "Alcibiades' Praise: The Attempted Seduction",
        "level": 1,
        "category": "alcibiades",
        "sections": {
            "Speech": ct(t),
            "Theme": "Alcibiades reveals Socrates' inner nature: beneath the outer mask of the Silenus lie divine golden images of surpassing beauty. He confesses his attempt to win Socrates' love -- sending away attendants, dining alone, wrestling together, even sharing a couch through the night. But Socrates remained utterly unmoved. The most beautiful and powerful young man in Athens could not tempt the philosopher.",
            "Key Insight": "Socrates' self-mastery is absolute. He has overcome his passions not by lacking them but by ruling them. His indifference to physical beauty is the living proof of the philosophical ascent Diotima described.",
            "Reflection": "What is the relationship between self-mastery and love? Can true philosophical wisdom coexist with human desire, or must one conquer the other?"
        },
        "keywords": ["alcibiades", "seduction", "rejection", "self-mastery", "desire", "wisdom", "humiliation"],
        "metadata": {"speaker": "Alcibiades"}
    })

    # 18. Alcibiades: Socrates in Battle
    t = extract_between(dialogue,
        "All this happened before he and I went on the expedition\nto Potidaea",
        "When Alcibiades had finished, there was a laugh")
    add_item({
        "id": "speech-alcibiades-military",
        "name": "Alcibiades' Praise: Socrates in Battle",
        "level": 1,
        "category": "alcibiades",
        "sections": {
            "Speech": ct(t),
            "Theme": "Alcibiades recounts Socrates' extraordinary conduct in military campaigns. At Potidaea, Socrates endured cold and hardship beyond all others, walking barefoot on ice. He stood motionless for an entire day and night, lost in thought, while soldiers watched in amazement. He saved Alcibiades' life in battle and showed supreme courage during the retreat at Delium. He is utterly unlike any other human being -- comparable only to a satyr.",
            "Key Insight": "The philosopher who contemplates eternal beauty is also the bravest man on the battlefield. Socrates' otherworldly nature manifests not just in thought but in superhuman endurance and courage.",
            "Reflection": "How does Socrates' physical courage relate to his philosophical vision? Is the person who has seen something beyond this world freed from ordinary fears?"
        },
        "keywords": ["alcibiades", "potidaea", "delium", "courage", "endurance", "military", "trance", "battle"],
        "metadata": {"speaker": "Alcibiades"}
    })

    # 19. Closing Scene
    t = extract_between(dialogue,
        "When Alcibiades had finished, there was a laugh",
        None)
    add_item({
        "id": "closing-scene",
        "name": "The Night Ends: Comedy and Tragedy Are One",
        "level": 1,
        "category": "frame-narrative",
        "sections": {
            "Passage": ct(t),
            "About": "After Alcibiades finishes, a final wave of revellers bursts in, bringing disorder. The sober guests depart. Aristodemus falls asleep. When he wakes at dawn, only Socrates, Aristophanes, and Agathon remain, drinking from a large goblet. Socrates is arguing that the genius of comedy is the same as that of tragedy -- the true artist in one must be master of both. First Aristophanes, then Agathon fall asleep. Socrates rises, bathes, and goes about his day as usual.",
            "Reflection": "The dialogue ends where philosophy and life meet: Socrates, having spoken of eternal beauty, outlasts everyone at the party and walks into the morning unchanged. What does it mean that comedy and tragedy are one?"
        },
        "keywords": ["socrates", "aristophanes", "agathon", "comedy", "tragedy", "dawn", "endurance", "closing"],
        "metadata": {"speaker": "Aristodemus/Narrator"}
    })

    # =========================================================================
    # L2 ITEMS: By Speaker
    # =========================================================================

    l1_ids = {i["id"] for i in items}

    add_item({
        "id": "speaker-phaedrus",
        "name": "Phaedrus on Love",
        "level": 2,
        "category": "by-speaker",
        "composite_of": ["speech-phaedrus"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Phaedrus, who initiated the idea of speeches in praise of Love, offers the first and most mythological speech. He sees Love as the eldest god and the source of courage and honour. His approach is ethical and traditional, drawing on Homer and Hesiod.",
            "For Readers": "Start here for the foundational claim: Love is ancient, and Love makes us brave."
        },
        "keywords": ["phaedrus", "mythology", "courage", "antiquity"],
        "metadata": {}
    })

    add_item({
        "id": "speaker-pausanias",
        "name": "Pausanias on Love",
        "level": 2,
        "category": "by-speaker",
        "composite_of": ["speech-pausanias"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Pausanias introduces the crucial distinction between Heavenly and Common love. His speech is more analytical than Phaedrus', separating noble love (of the mind and character) from base love (of the body). He is the political speaker, concerned with social customs and laws.",
            "For Readers": "Read Pausanias for the first attempt at philosophical discrimination: not all love is equal."
        },
        "keywords": ["pausanias", "heavenly-love", "common-love", "discrimination"],
        "metadata": {}
    })

    add_item({
        "id": "speaker-eryximachus",
        "name": "Eryximachus on Love",
        "level": 2,
        "category": "by-speaker",
        "composite_of": ["interlude-hiccough", "speech-eryximachus"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Eryximachus the physician extends love beyond the human into a cosmic principle. Influenced by Heraclitus, he sees love as the harmony of opposites that governs medicine, music, astronomy, and all the arts. His speech is the most 'scientific' -- the physician's attempt to find love in nature itself.",
            "For Readers": "Read Eryximachus for the expansion of love from a human emotion to a universal principle of harmony."
        },
        "keywords": ["eryximachus", "medicine", "harmony", "nature", "cosmos"],
        "metadata": {}
    })

    add_item({
        "id": "speaker-aristophanes",
        "name": "Aristophanes on Love",
        "level": 2,
        "category": "by-speaker",
        "composite_of": ["interlude-hiccough", "speech-aristophanes"],
        "relationship_type": "emergence",
        "sections": {
            "About": "The comic playwright delivers the most famous speech: the myth of the split humans. Originally whole and powerful, humans were cleaved in two by Zeus. Love is the longing to restore our original wholeness. Comic in form, deeply serious in substance -- Aristophanes touches the universal experience of incompleteness and the desire for reunion.",
            "For Readers": "This is the speech everyone remembers. Read it for the mythic origin of romantic love and the ache of human incompleteness."
        },
        "keywords": ["aristophanes", "myth", "wholeness", "split-humans", "comedy"],
        "metadata": {}
    })

    agathon_refs = ["speech-agathon"]
    if "interlude-pre-agathon" in l1_ids:
        agathon_refs = ["interlude-pre-agathon", "speech-agathon"]
    add_item({
        "id": "speaker-agathon",
        "name": "Agathon on Love",
        "level": 2,
        "category": "by-speaker",
        "composite_of": agathon_refs,
        "relationship_type": "emergence",
        "sections": {
            "About": "The tragic poet and host delivers a virtuoso poetic performance. Agathon's Love is young, beautiful, and the source of all the virtues. His speech is deliberate rhetoric -- beautiful but, as Socrates will show, not quite true. Yet Agathon contributes the key insight that Love must be distinguished from Love's works.",
            "For Readers": "Read Agathon for the most purely beautiful speech, and as the necessary foil to Socrates' dialectic."
        },
        "keywords": ["agathon", "poetry", "beauty", "rhetoric", "virtues"],
        "metadata": {}
    })

    add_item({
        "id": "speaker-socrates",
        "name": "Socrates and Diotima on Love",
        "level": 2,
        "category": "by-speaker",
        "composite_of": [
            "speech-socrates-questioning",
            "speech-diotima-nature",
            "speech-diotima-immortality",
            "speech-diotima-ladder",
            "speech-socrates-conclusion"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "The philosophical heart of the Symposium. Socrates first dismantles Agathon's speech through dialectic, then recounts the teachings of Diotima of Mantinea. Love is not a god but a daimon, born of Plenty and Poverty. Love desires the everlasting possession of the good. Through the famous Ladder of Beauty, one ascends from earthly love to the contemplation of Beauty itself -- absolute, eternal, and divine.",
            "For Readers": "This is the philosophical summit of Western thought about love. Read the questioning of Agathon for Socratic method in action. Read Diotima for one of the most profound visions of love, beauty, and transcendence ever written."
        },
        "keywords": ["socrates", "diotima", "dialectic", "daimon", "ladder", "beauty", "transcendence", "philosophy"],
        "metadata": {}
    })

    add_item({
        "id": "speaker-alcibiades",
        "name": "Alcibiades on Socrates",
        "level": 2,
        "category": "by-speaker",
        "composite_of": [
            "arrival-alcibiades",
            "speech-alcibiades-silenus",
            "speech-alcibiades-personal",
            "speech-alcibiades-military"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "After the philosophical ascent to eternal beauty, Alcibiades crashes in drunk and praises not Love but Socrates -- the living embodiment of the philosophical lover. Socrates is like Silenus: ugly outside, divine within. His words enchant souls. He endures superhuman hardships. He is immune to seduction. The most powerful man in Athens confesses himself utterly conquered by a barefoot philosopher.",
            "For Readers": "Read Alcibiades for the human dimension of philosophy: what it feels like to be in the presence of someone who has truly seen the good. His speech is confession, love letter, and warning."
        },
        "keywords": ["alcibiades", "socrates", "silenus", "confession", "embodiment", "contrast"],
        "metadata": {}
    })

    # =========================================================================
    # L2 ITEMS: By Theme
    # =========================================================================

    add_item({
        "id": "theme-nature-of-love",
        "name": "What Is Love?",
        "level": 2,
        "category": "by-theme",
        "composite_of": [
            "speech-phaedrus", "speech-pausanias", "speech-eryximachus",
            "speech-aristophanes", "speech-agathon", "speech-socrates-questioning",
            "speech-diotima-nature"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "Each speaker offers a different answer to 'What is Love?' Phaedrus: the eldest god, source of courage. Pausanias: two loves, heavenly and common. Eryximachus: cosmic harmony. Aristophanes: the desire for wholeness. Agathon: the youngest and fairest god. Socrates/Diotima: a daimon, neither god nor mortal, the child of Plenty and Poverty.",
            "For Readers": "Trace the evolution of understanding from speech to speech. Notice how each view is partly true and partly limited, building toward Socrates' synthesis."
        },
        "keywords": ["love", "definition", "nature", "evolution", "synthesis"],
        "metadata": {}
    })

    add_item({
        "id": "theme-love-and-beauty",
        "name": "Love and Beauty",
        "level": 2,
        "category": "by-theme",
        "composite_of": [
            "speech-agathon", "speech-socrates-questioning", "speech-diotima-ladder"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "The relationship between love and beauty is the Symposium's deepest question. Agathon claims Love is beautiful. Socrates shows that Love desires beauty, and therefore lacks it. Diotima reveals that love is the path from particular beauties to Beauty itself -- the famous ascent from bodies to souls to laws to sciences to the Form of Beauty, absolute and eternal.",
            "For Readers": "These three passages contain the philosophical core. Read them together to follow the argument from beautiful praise to beautiful truth."
        },
        "keywords": ["beauty", "form", "ascent", "absolute", "ladder", "desire"],
        "metadata": {}
    })

    add_item({
        "id": "theme-love-and-mortality",
        "name": "Love and Immortality",
        "level": 2,
        "category": "by-theme",
        "composite_of": [
            "speech-phaedrus", "speech-aristophanes", "speech-diotima-immortality"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "Love's relationship to death and immortality runs through the Symposium. Phaedrus tells of Alcestis dying for love and Achilles choosing death for honour. Aristophanes' split humans are driven by fear of further division. Diotima teaches that love is ultimately about birth in beauty -- the mortal's way of participating in the eternal through children, art, laws, and philosophy.",
            "For Readers": "Follow this thread to understand why love matters so deeply: it is the mortal's path to the immortal."
        },
        "keywords": ["immortality", "death", "birth", "creation", "legacy", "mortality"],
        "metadata": {}
    })

    add_item({
        "id": "theme-portrait-of-socrates",
        "name": "The Portrait of Socrates",
        "level": 2,
        "category": "by-theme",
        "composite_of": [
            "setting-banquet", "speech-socrates-questioning",
            "speech-alcibiades-silenus", "speech-alcibiades-personal",
            "speech-alcibiades-military", "closing-scene"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "The Symposium is, among other things, the greatest portrait of Socrates ever written. He arrives in a trance, questions rather than proclaims, and professes to know only the art of love. Alcibiades reveals him as Silenus -- grotesque outside, golden within. He is superhuman in endurance, immune to seduction, unmatched in battle. At dawn, having outlasted everyone, he simply walks into another day.",
            "For Readers": "Read these passages together for the full picture of what a philosopher looks like in the flesh -- beautiful, strange, and utterly unlike anyone else."
        },
        "keywords": ["socrates", "portrait", "philosopher", "silenus", "endurance", "self-mastery"],
        "metadata": {}
    })

    # =========================================================================
    # L3 ITEMS: Meta-categories
    # =========================================================================

    add_item({
        "id": "meta-speeches",
        "name": "The Seven Speeches on Love",
        "level": 3,
        "category": "meta",
        "composite_of": [
            "speaker-phaedrus", "speaker-pausanias", "speaker-eryximachus",
            "speaker-aristophanes", "speaker-agathon", "speaker-socrates",
            "speaker-alcibiades"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "The Symposium's seven speeches form a dramatic and philosophical arc. Each speaker contributes something to the final understanding of love, and each is characteristic of the speaker. The mythological Phaedrus, the political Pausanias, the scientific Eryximachus, the comic Aristophanes, the poetic Agathon, the philosophical Socrates, and the confessional Alcibiades -- together they compose a complete portrait of love from every human perspective.",
            "How to Use": "Read the speeches in order for the full dramatic experience. Or dip into individual speakers to explore different facets of love."
        },
        "keywords": ["speeches", "love", "speakers", "arc", "philosophy", "drama"],
        "metadata": {"speech_count": 7}
    })

    add_item({
        "id": "meta-themes",
        "name": "Great Themes of the Symposium",
        "level": 3,
        "category": "meta",
        "composite_of": [
            "theme-nature-of-love", "theme-love-and-beauty",
            "theme-love-and-mortality", "theme-portrait-of-socrates"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "The Symposium weaves together several great themes: the nature of love itself, the relationship between love and beauty, love's connection to mortality and immortality, and the portrait of the philosopher as the true lover. These themes interpenetrate, each speech adding new facets.",
            "How to Use": "Browse by theme when you want to follow a single thread across all the speeches. Each theme gathers the relevant passages from different speakers."
        },
        "keywords": ["themes", "beauty", "immortality", "philosophy", "love"],
        "metadata": {"theme_count": 4}
    })

    pre_agathon_refs = ["frame-apollodorus", "setting-banquet", "interlude-hiccough",
                        "arrival-alcibiades", "closing-scene"]
    if "interlude-pre-agathon" in l1_ids:
        pre_agathon_refs.insert(3, "interlude-pre-agathon")

    add_item({
        "id": "meta-dramatic-structure",
        "name": "The Dramatic Structure",
        "level": 3,
        "category": "meta",
        "composite_of": pre_agathon_refs,
        "relationship_type": "emergence",
        "sections": {
            "About": "The Symposium is not just philosophy but supreme dramatic art. The frame narrative (Apollodorus retelling a story from Aristodemus) creates deliberate distance. The setting at a victory banquet grounds the philosophy in life. Comic interludes punctuate the serious speeches. The closing -- Socrates arguing that comedy and tragedy are one, while the poets fall asleep -- is one of the most extraordinary endings in literature.",
            "How to Use": "Read the frame and interludes to appreciate the Symposium as a work of art, not just a collection of arguments."
        },
        "keywords": ["drama", "structure", "frame", "narrative", "art", "comedy", "tragedy"],
        "metadata": {}
    })

    # =========================================================================
    # Assemble Grammar
    # =========================================================================

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Plato", "date": "c. 385-370 BCE", "note": "Author"},
                {"name": "Benjamin Jowett", "date": "1871", "note": "Translator"},
                {"name": "Project Gutenberg", "date": "1999",
                 "note": "eBook #1600 (https://www.gutenberg.org/ebooks/1600)"}
            ]
        },
        "name": "Symposium",
        "description": (
            "Plato's Symposium (c. 385-370 BCE) -- the most perfect dialogue on the nature "
            "of love ever written. At a banquet celebrating the tragic poet Agathon's first "
            "victory, seven speakers offer speeches in praise of Love (Eros). From Phaedrus' "
            "mythological praise through Aristophanes' famous myth of the split humans to "
            "Socrates' account of Diotima's 'Ladder of Beauty' -- the ascent from earthly "
            "love to the contemplation of Beauty itself -- the Symposium traces every dimension "
            "of love: ethical, cosmic, comic, poetic, philosophical, and confessional. "
            "Benjamin Jowett translation. Source: Project Gutenberg eBook #1600 "
            "(https://www.gutenberg.org/ebooks/1600).\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Anselm Feuerbach's 'The Symposium' "
            "(1869, second version 1873) -- monumental oil painting of the banquet scene, "
            "Nationalgalerie Berlin, public domain. Greek red-figure pottery depicting symposia "
            "(banquet scenes), widely available from museum collections. Jacques-Louis David's "
            "'The Death of Socrates' (1787) for the figure of Socrates. Raphael's 'The School "
            "of Athens' (1509-1511) for Plato's figure. John Flaxman's line illustrations of "
            "Greek subjects (early 19th century), public domain."
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "philosophy", "love", "plato", "greek", "dialogue",
            "beauty", "wisdom", "public-domain", "full-text"
        ],
        "roots": ["greek-philosophy"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "dialectical",
        "items": items
    }

    return grammar


def main():
    print("Building Symposium grammar...")
    grammar = build_grammar()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in grammar["items"] if i["level"] == 1)
    l2 = sum(1 for i in grammar["items"] if i["level"] == 2)
    l3 = sum(1 for i in grammar["items"] if i["level"] == 3)
    print(f"Written to {OUTPUT_PATH}")
    print(f"Total items: {len(grammar['items'])} (L1: {l1}, L2: {l2}, L3: {l3})")

    # Check for empty content
    warnings = 0
    for item in grammar["items"]:
        for section_name, section_text in item.get("sections", {}).items():
            if section_name in ("Speech", "Passage") and len(section_text.strip()) < 50:
                print(f"  WARNING: {item['id']} has short {section_name} ({len(section_text.strip())} chars)")
                warnings += 1
    if warnings == 0:
        print("All speech/passage sections have content.")


if __name__ == "__main__":
    main()
