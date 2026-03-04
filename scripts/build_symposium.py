#!/usr/bin/env python3
"""
Build grammar.json for Plato's Symposium from seed text.

The Symposium (c. 385-370 BCE) is a dialogue about the nature of Love (Eros),
structured as a series of speeches at a banquet. Translated by Benjamin Jowett.

Structure:
- Gutenberg header: lines before "*** START OF THE PROJECT GUTENBERG EBOOK SYMPOSIUM ***"
- Jowett's Introduction: from "INTRODUCTION." until the second "SYMPOSIUM" heading
- Dramatic frame: Apollodorus narrating to his companion
- The Banquet: Setting the scene at Agathon's house
- Seven speeches on Love: Phaedrus, Pausanias, Eryximachus, Aristophanes,
  Agathon, Socrates (with Diotima), Alcibiades
- Closing scene: The revellers arrive, the night ends
- Gutenberg footer

We extract the primary dialogue text (after the Introduction), strip commentary
notes in parentheses that reference other works, and structure into speeches.
"""

import json
import re
import textwrap
from pathlib import Path

SEED_PATH = Path(__file__).parent.parent / "seeds" / "symposium-plato.txt"
OUTPUT_PATH = Path(__file__).parent.parent / "grammars" / "symposium-plato" / "grammar.json"


def read_seed():
    """Read the seed text and return lines."""
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        return f.readlines()


def extract_dialogue(lines):
    """Extract the dialogue text, stripping Gutenberg header/footer and Jowett's Introduction."""
    text = "".join(lines)

    # Find the start of the actual dialogue (second occurrence of "SYMPOSIUM" after the intro)
    # The intro starts after the Gutenberg header and goes up to the second "SYMPOSIUM"
    start_marker = "\nSYMPOSIUM\n\n\nPERSONS OF THE DIALOGUE"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK SYMPOSIUM ***"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        raise ValueError("Could not find dialogue boundaries in seed text")

    dialogue = text[start_idx:end_idx].strip()
    return dialogue


def clean_text(text):
    """Clean editorial notes and normalize whitespace while preserving paragraph breaks."""
    # Remove parenthetical scholarly references like (compare Rep.), (Iliad), (Odyssey), etc.
    # But keep parenthetical dialogue content
    # Pattern: remove short parenthetical references to other works
    text = re.sub(r'\(compare [^)]+\)', '', text)
    text = re.sub(r'\(supra[^)]*\)', '', text)
    text = re.sub(r'\(Probably [^)]+\)', '', text)
    text = re.sub(r'\(A fragment of [^)]+\)', '', text)
    text = re.sub(r'\(Eurip\.[^)]*\)', '', text)
    text = re.sub(r'\(compare \d+ [^)]+\)', '', text)
    text = re.sub(r'\(Iliad[^)]*\)', '', text)
    text = re.sub(r'\(Odyssey[^)]*\)', '', text)
    text = re.sub(r'\(Rep\.[^)]*\)', '', text)
    text = re.sub(r'\(Arist\.[^)]*\)', '', text)
    text = re.sub(r'\(Greek\)', '', text)
    text = re.sub(r'\(Aesch\.[^)]*\)', '', text)

    # Normalize multiple spaces
    text = re.sub(r'  +', ' ', text)
    # Normalize paragraph breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def split_into_sections(dialogue):
    """
    Split the dialogue into named sections based on content markers.
    Returns a list of (section_name, text) tuples.
    """
    sections = []

    # Define speech boundaries by searching for key phrases
    # We'll work with the full dialogue text and find markers

    # 1. Dramatis Personae + Scene
    dp_end = dialogue.find("Concerning the things about which you ask")

    # 2. Frame narrative: Apollodorus and companion
    frame_start = dialogue.find("Concerning the things about which you ask")
    frame_end = dialogue.find("He said that he met Socrates fresh from the bath")

    # 3. Setting the Scene: Aristodemus meets Socrates, arrival at Agathon's
    scene_start = dialogue.find("He said that he met Socrates fresh from the bath")
    scene_end = dialogue.find("Phaedrus began by affirming that Love is a mighty god")

    # 4. Speech of Phaedrus
    phaedrus_start = dialogue.find("Phaedrus began by affirming that Love is a mighty god")
    phaedrus_end = dialogue.find("This, or something like this, was the speech of Phaedrus")
    # Include the closing line
    phaedrus_close = dialogue.find("the next which he\nrepeated was that of Pausanias.")
    if phaedrus_close == -1:
        phaedrus_close = dialogue.find("the next which he repeated was that of Pausanias.")

    # 5. Speech of Pausanias
    pausanias_start = dialogue.find("Phaedrus, he said, the argument has not")
    if pausanias_start == -1:
        pausanias_start = phaedrus_close
    pausanias_end = dialogue.find("Eryximachus spoke as follows:")

    # 6. Interlude: Aristophanes' hiccough
    hiccough_start = dialogue.find("Aristophanes was going to speak")
    if hiccough_start == -1:
        hiccough_start = dialogue.find("When Pausanias came to a pause")
    hiccough_end = dialogue.find("Eryximachus spoke as follows:")

    # 7. Speech of Eryximachus
    eryximachus_start = dialogue.find("Eryximachus spoke as follows:")
    eryximachus_end = dialogue.find("Aristophanes professed to open another vein of discourse")

    # 8. Speech of Aristophanes
    aristophanes_start = dialogue.find("Aristophanes professed to open another vein of discourse")
    aristophanes_end = dialogue.find("This, Eryximachus, is my discourse of love")
    # Extend to include closing
    aristophanes_close_idx = dialogue.find("each, or\nrather either, for Agathon and Socrates are the only ones left.")
    if aristophanes_close_idx == -1:
        aristophanes_close_idx = dialogue.find("Agathon and Socrates are the only ones left.")

    # 9. Interlude before Agathon
    pre_agathon_start = dialogue.find("Indeed, I am not going to attack you, said Eryximachus")
    pre_agathon_end = dialogue.find("The previous speakers, instead of praising the god Love")

    # 10. Speech of Agathon
    agathon_start = dialogue.find("The previous speakers, instead of praising the god Love")
    agathon_end = dialogue.find("When Agathon had done speaking, Aristodemus said")

    # 11. Socrates questions Agathon
    socrates_qa_start = dialogue.find("When Agathon had done speaking, Aristodemus said")
    socrates_qa_end = dialogue.find("And now, taking my leave of you, I would rehearse a tale of love")

    # 12. Socrates: Diotima - Nature of Love
    diotima_nature_start = dialogue.find("And now, taking my leave of you, I would rehearse a tale of love")
    diotima_nature_end = dialogue.find("'But Love desires the beautiful;")
    if diotima_nature_end == -1:
        diotima_nature_end = dialogue.find("But Love desires the beautiful;")

    # 13. Socrates: Diotima - Love and Immortality
    diotima_immortality_start = diotima_nature_end
    diotima_immortality_end = dialogue.find("'These are the lesser mysteries of love")
    if diotima_immortality_end == -1:
        diotima_immortality_end = dialogue.find("These are the lesser mysteries of love")

    # 14. Socrates: Diotima - The Ladder of Beauty (Greater Mysteries)
    diotima_ladder_start = diotima_immortality_end
    diotima_ladder_end = dialogue.find("Such, Phaedrus--and I speak not only to you")

    # 15. Socrates' conclusion
    socrates_conclusion_start = dialogue.find("Such, Phaedrus--and I speak not only to you")
    socrates_conclusion_end = dialogue.find("When Socrates had done speaking, the company applauded")

    # 16. Arrival of Alcibiades
    alcibiades_arrival_start = dialogue.find("When Socrates had done speaking, the company applauded")
    alcibiades_arrival_end = dialogue.find("And now, my boys, I shall praise Socrates in a figure")

    # 17. Alcibiades' speech: Socrates as Silenus/Marsyas
    alcibiades_silenus_start = dialogue.find("And now, my boys, I shall praise Socrates in a figure")
    alcibiades_silenus_end = dialogue.find("And this is what I and many others have suffered from the")
    if alcibiades_silenus_end == -1:
        alcibiades_silenus_end = dialogue.find("that is the sort of thing which I hear him say")
        if alcibiades_silenus_end != -1:
            # Move to the next paragraph break after this
            next_para = dialogue.find("\n\n", alcibiades_silenus_end)
            if next_para != -1:
                alcibiades_silenus_end = next_para

    # 18. Alcibiades' speech: Personal experience with Socrates
    alcibiades_personal_start = alcibiades_silenus_end
    alcibiades_personal_end = dialogue.find("Also, Socrates, you are not unlike him in your")
    if alcibiades_personal_end == -1:
        alcibiades_personal_end = dialogue.find("his endurance was simply marvellous")
        if alcibiades_personal_end != -1:
            next_para = dialogue.find("\n\n", alcibiades_personal_end)
            if next_para != -1:
                alcibiades_personal_end = next_para

    # 19. Alcibiades' speech: Military stories
    alcibiades_military_start = alcibiades_personal_end
    alcibiades_military_end = dialogue.find("When Alcibiades had finished, there was a laugh")

    # 20. Closing scene
    closing_start = dialogue.find("When Alcibiades had finished, there was a laugh")
    closing_end = len(dialogue)

    return {
        "frame": dialogue[frame_start:frame_end] if frame_start != -1 and frame_end != -1 else "",
        "setting": dialogue[scene_start:scene_end] if scene_start != -1 and scene_end != -1 else "",
        "phaedrus": dialogue[phaedrus_start:phaedrus_close + 100] if phaedrus_start != -1 else "",
        "pausanias": dialogue[pausanias_start:pausanias_end] if pausanias_start != -1 and pausanias_end != -1 else "",
        "eryximachus": dialogue[eryximachus_start:eryximachus_end] if eryximachus_start != -1 and eryximachus_end != -1 else "",
        "aristophanes": dialogue[aristophanes_start:aristophanes_close_idx + 100] if aristophanes_start != -1 else "",
        "agathon": dialogue[agathon_start:agathon_end] if agathon_start != -1 and agathon_end != -1 else "",
        "socrates_qa": dialogue[socrates_qa_start:socrates_qa_end] if socrates_qa_start != -1 and socrates_qa_end != -1 else "",
        "diotima_nature": dialogue[diotima_nature_start:diotima_nature_end] if diotima_nature_start != -1 and diotima_nature_end != -1 else "",
        "diotima_immortality": dialogue[diotima_immortality_start:diotima_immortality_end] if diotima_immortality_start != -1 and diotima_immortality_end != -1 else "",
        "diotima_ladder": dialogue[diotima_ladder_start:diotima_ladder_end] if diotima_ladder_start != -1 and diotima_ladder_end != -1 else "",
        "socrates_conclusion": dialogue[socrates_conclusion_start:socrates_conclusion_end] if socrates_conclusion_start != -1 and socrates_conclusion_end != -1 else "",
        "alcibiades_arrival": dialogue[alcibiades_arrival_start:alcibiades_arrival_end] if alcibiades_arrival_start != -1 and alcibiades_arrival_end != -1 else "",
        "alcibiades_silenus": dialogue[alcibiades_silenus_start:alcibiades_silenus_end] if alcibiades_silenus_start != -1 and alcibiades_silenus_end != -1 else "",
        "alcibiades_personal": dialogue[alcibiades_personal_start:alcibiades_personal_end] if alcibiades_personal_start != -1 and alcibiades_personal_end != -1 else "",
        "alcibiades_military": dialogue[alcibiades_military_start:alcibiades_military_end] if alcibiades_military_start != -1 and alcibiades_military_end != -1 else "",
        "closing": dialogue[closing_start:closing_end] if closing_start != -1 else "",
    }


def normalize_paragraph(text):
    """Normalize a block of text: join lines within paragraphs, preserve paragraph breaks."""
    if not text:
        return ""
    text = text.strip()
    # Split on double newlines to get paragraphs
    paragraphs = re.split(r'\n\n+', text)
    result = []
    for p in paragraphs:
        # Join single newlines within a paragraph
        joined = ' '.join(line.strip() for line in p.split('\n') if line.strip())
        if joined:
            result.append(joined)
    return '\n\n'.join(result)


def build_grammar():
    """Build the complete grammar.json for the Symposium."""
    lines = read_seed()
    dialogue = extract_dialogue(lines)
    dialogue = clean_text(dialogue)

    # Now we'll manually parse the dialogue into well-defined passages
    # Rather than relying on fragile string splitting, we'll extract full text blocks

    items = []
    sort_order = 0

    # === L1 ITEMS: Individual speeches and passages ===

    # --- Frame Narrative ---
    frame_text = extract_between(dialogue,
        "Concerning the things about which you ask",
        "He said that he met Socrates fresh from the bath")
    if frame_text:
        items.append({
            "id": "frame-apollodorus",
            "name": "Apollodorus Sets the Scene",
            "sort_order": sort_order,
            "level": 1,
            "category": "frame-narrative",
            "sections": {
                "Passage": normalize_paragraph(frame_text),
                "About": "Apollodorus, the devoted follower of Socrates, recounts the story of the famous banquet to a companion. He heard it from Aristodemus, who was present. The narrative frame establishes that this is a story told and retold -- a philosophical tradition passed down through imperfect memory and passionate devotion.",
                "Reflection": "How does the act of retelling shape philosophical truth? What is lost and what is gained when wisdom passes through multiple voices?"
            },
            "keywords": ["apollodorus", "aristodemus", "narration", "memory", "devotion"],
            "metadata": {"speaker": "Apollodorus"}
        })
        sort_order += 1

    # --- Setting: Arrival at Agathon's ---
    setting_text = extract_between(dialogue,
        "He said that he met Socrates fresh from the bath",
        "Phaedrus began by affirming that Love is a mighty god")
    if setting_text:
        items.append({
            "id": "setting-banquet",
            "name": "The Banquet Begins",
            "sort_order": sort_order,
            "level": 1,
            "category": "frame-narrative",
            "sections": {
                "Passage": normalize_paragraph(setting_text),
                "About": "Aristodemus encounters Socrates freshly bathed and sandalled -- an unusual sight. They walk to Agathon's house together, where the tragic poet is celebrating his first victory. Socrates falls into a trance on a neighbor's porch, arriving late. The company agrees to give speeches in praise of Love rather than drinking heavily.",
                "Reflection": "The philosopher arrives late, lost in thought. The celebration of art gives way to philosophy. What does it mean that the search for truth begins at a party?"
            },
            "keywords": ["agathon", "banquet", "socrates", "aristodemus", "celebration", "trance"],
            "metadata": {"speaker": "Aristodemus/Narrator"}
        })
        sort_order += 1

    # --- Speech of Phaedrus ---
    phaedrus_text = extract_between(dialogue,
        "Phaedrus began by affirming that Love is a mighty god",
        "This, or something like this, was the speech of Phaedrus")
    phaedrus_closing = extract_between(dialogue,
        "This, or something like this, was the speech of Phaedrus",
        "Phaedrus, he said, the argument has not")
    phaedrus_full = (phaedrus_text or "") + "\n\n" + "This, or something like this, was the speech of Phaedrus." + "\n\n" + (phaedrus_closing or "").split("Phaedrus, he said")[0]

    items.append({
        "id": "speech-phaedrus",
        "name": "Speech of Phaedrus: Love as the Eldest God",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": normalize_paragraph(phaedrus_full),
            "Theme": "Love is the most ancient of the gods, the source of our greatest blessings. Love inspires courage: a lover would rather die than be seen as a coward by the beloved. Phaedrus invokes Alcestis, who died for her husband, and Achilles, who avenged Patroclus knowing it meant his own death.",
            "Key Insight": "The sense of honour and dishonour, which love inspires, is the foundation of all great works by individuals and states.",
            "Reflection": "What would you dare to do, or refuse to do, in the presence of someone whose opinion you truly valued?"
        },
        "keywords": ["phaedrus", "antiquity", "courage", "honour", "alcestis", "achilles", "patroclus"],
        "metadata": {"speaker": "Phaedrus", "speech_number": 1}
    })
    sort_order += 1

    # --- Speech of Pausanias ---
    pausanias_text = extract_between(dialogue,
        "Phaedrus, he said, the argument has not",
        "When Pausanias came to a pause")
    if not pausanias_text:
        pausanias_text = extract_between(dialogue,
            "Phaedrus, he said, the argument has not",
            "Aristophanes was going to speak")
    if not pausanias_text:
        pausanias_text = extract_between(dialogue,
            "Phaedrus, he said, the argument has not",
            "I will do both, said Eryximachus")

    items.append({
        "id": "speech-pausanias",
        "name": "Speech of Pausanias: The Two Loves",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": normalize_paragraph(pausanias_text or ""),
            "Theme": "There are two Aphrodites and therefore two Loves. The Heavenly Love, born of Uranus alone, is noble and intellectual, directed toward virtue and the mind. The Common Love, daughter of Zeus and Dione, is indiscriminate and bodily. Actions are neither good nor evil in themselves -- only the manner of their performance makes them so.",
            "Key Insight": "The noble lover attaches himself to the enduring character of the beloved, not to the fleeting beauty of the body. A voluntary service rendered for the sake of virtue and wisdom is always honourable.",
            "Reflection": "How do you distinguish between love that elevates and love that diminishes? What does it mean to love someone's character rather than their appearance?"
        },
        "keywords": ["pausanias", "heavenly-love", "common-love", "aphrodite", "virtue", "nobility", "two-loves"],
        "metadata": {"speaker": "Pausanias", "speech_number": 2}
    })
    sort_order += 1

    # --- Aristophanes' Hiccough Interlude ---
    hiccough_text = extract_between(dialogue,
        "When Pausanias came to a pause",
        "Eryximachus spoke as follows:")
    if not hiccough_text:
        hiccough_text = extract_between(dialogue,
            "Aristophanes was going to speak",
            "Eryximachus spoke as follows:")

    items.append({
        "id": "interlude-hiccough",
        "name": "Aristophanes' Hiccough",
        "sort_order": sort_order,
        "level": 1,
        "category": "interludes",
        "sections": {
            "Passage": normalize_paragraph(hiccough_text or ""),
            "About": "A comic interlude: Aristophanes has the hiccough and cannot speak. Eryximachus the physician prescribes remedies -- holding breath, gargling, sneezing -- and offers to speak in his place. The great comic playwright is rendered speechless by his own body, a fitting irony that Plato surely relished.",
            "Reflection": "Even at a philosophical banquet, the body interrupts the mind. What role does comedy play in the pursuit of truth?"
        },
        "keywords": ["aristophanes", "hiccough", "comedy", "eryximachus", "body", "interruption"],
        "metadata": {"speaker": "Aristophanes/Eryximachus"}
    })
    sort_order += 1

    # --- Speech of Eryximachus ---
    eryximachus_text = extract_between(dialogue,
        "Eryximachus spoke as follows:",
        "Aristophanes professed to open another vein of discourse")

    items.append({
        "id": "speech-eryximachus",
        "name": "Speech of Eryximachus: Love as Cosmic Harmony",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": normalize_paragraph(eryximachus_text or ""),
            "Theme": "Love extends beyond human souls into all of nature -- animals, plants, and the cosmos itself. The physician sees two kinds of love in the body: healthy and diseased. Medicine, music, astronomy, and divination all work by reconciling opposites. Love is the universal principle of harmony that brings order out of discord.",
            "Key Insight": "The double love is not merely an affection of the soul toward the fair, but is to be found in all that is. Love is the reconciliation of opposites -- the harmony that succeeds discord.",
            "Reflection": "Where do you see opposing forces in your life that might be reconciled rather than conquered? What would it mean to see love as a principle of nature, not just a human emotion?"
        },
        "keywords": ["eryximachus", "medicine", "harmony", "opposites", "heraclitus", "nature", "cosmos", "music"],
        "metadata": {"speaker": "Eryximachus", "speech_number": 3}
    })
    sort_order += 1

    # --- Speech of Aristophanes ---
    aristophanes_text = extract_between(dialogue,
        "Aristophanes professed to open another vein of discourse",
        "This, Eryximachus, is my discourse of love")
    aristophanes_closing = extract_between(dialogue,
        "This, Eryximachus, is my discourse of love",
        "Indeed, I am not going to attack you, said Eryximachus")
    aristophanes_full = (aristophanes_text or "") + "\n\nThis, Eryximachus, is my discourse of love" + (aristophanes_closing or "").split("Indeed, I am not")[0]

    items.append({
        "id": "speech-aristophanes",
        "name": "Speech of Aristophanes: The Origin of Love",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": normalize_paragraph(aristophanes_full),
            "Theme": "Originally humans were round, with four arms and four legs, two faces, and tremendous strength. There were three sexes: male, female, and androgynous. Zeus, fearing their power, split them in two. Ever since, each half wanders seeking its other half. Love is the name for this longing to be whole again -- the desire and pursuit of the whole.",
            "Key Insight": "Love is the desire of the whole, and the pursuit of the whole is called love. We are each but half a person, searching for the one who completes us.",
            "Reflection": "Do you recognize the longing Aristophanes describes -- the sense of incompleteness that seeks reunion? Is love truly about finding our 'other half,' or is that a beautiful myth?"
        },
        "keywords": ["aristophanes", "origin", "split-humans", "wholeness", "zeus", "androgynous", "desire", "reunion"],
        "metadata": {"speaker": "Aristophanes", "speech_number": 4}
    })
    sort_order += 1

    # --- Pre-Agathon Interlude ---
    pre_agathon_text = extract_between(dialogue,
        "Indeed, I am not going to attack you, said Eryximachus",
        "The previous speakers, instead of praising the god Love")

    if pre_agathon_text and len(pre_agathon_text.strip()) > 50:
        items.append({
            "id": "interlude-pre-agathon",
            "name": "Before Agathon Speaks",
            "sort_order": sort_order,
            "level": 1,
            "category": "interludes",
            "sections": {
                "Passage": normalize_paragraph(pre_agathon_text),
                "About": "A brief exchange between the remaining speakers. Eryximachus praises Aristophanes' speech. Socrates and Agathon spar lightly about performance anxiety -- Agathon, who has faced the theatre crowd, should not fear a small party of friends. Phaedrus intervenes to keep them on task.",
                "Reflection": "How does the interplay between speakers shape the philosophical argument? Notice how Socrates is already beginning to shift the terms of debate."
            },
            "keywords": ["agathon", "socrates", "dialogue", "theatre", "audience"],
            "metadata": {"speaker": "Various"}
        })
        sort_order += 1

    # --- Speech of Agathon ---
    agathon_text = extract_between(dialogue,
        "The previous speakers, instead of praising the god Love",
        "When Agathon had done speaking, Aristodemus said")

    items.append({
        "id": "speech-agathon",
        "name": "Speech of Agathon: Love as the Fairest God",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": normalize_paragraph(agathon_text or ""),
            "Theme": "Agathon, the tragic poet, delivers an ornate, poetic speech. Love is not ancient but the youngest of the gods -- young, tender, flexible, dwelling among flowers and in the softest hearts. Love possesses all virtues: justice (none serve him against their will), temperance (he masters all desires), courage (he conquers even Ares), and wisdom (he is the supreme poet who inspires all creation).",
            "Key Insight": "Love is the fairest and best in himself, and the cause of what is fairest and best in all other things. He gives peace on earth and calms the stormy deep.",
            "Reflection": "Is Agathon's praise beautiful but empty, as Socrates will suggest? Or does poetic truth capture something that logical argument cannot?"
        },
        "keywords": ["agathon", "beauty", "youth", "poetry", "virtues", "justice", "temperance", "courage", "wisdom"],
        "metadata": {"speaker": "Agathon", "speech_number": 5}
    })
    sort_order += 1

    # --- Socrates Questions Agathon ---
    socrates_qa_text = extract_between(dialogue,
        "When Agathon had done speaking, Aristodemus said",
        "And now, taking my leave of you, I would rehearse a tale of love")

    items.append({
        "id": "speech-socrates-questioning",
        "name": "Socrates Questions Agathon",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Passage": normalize_paragraph(socrates_qa_text or ""),
            "Theme": "Before his own speech, Socrates dismantles Agathon's praise through dialectic questioning. Love is of something -- it desires what it lacks. If Love desires beauty, Love itself cannot be beautiful. If the beautiful is the good, then Love lacks goodness too. Agathon gracefully concedes: 'I cannot refute you, Socrates.' Socrates replies: 'Say rather that you cannot refute the truth.'",
            "Key Insight": "Love is not the possession of beauty and goodness, but the desire for them. We do not desire what we already have. This simple distinction overturns all the previous speeches.",
            "Reflection": "What is the difference between praising something and understanding it? Does Socrates' method -- questioning rather than proclaiming -- get closer to truth?"
        },
        "keywords": ["socrates", "agathon", "dialectic", "desire", "lack", "truth", "questioning"],
        "metadata": {"speaker": "Socrates", "speech_number": 6}
    })
    sort_order += 1

    # --- Socrates/Diotima: Nature of Love (Daimon) ---
    diotima_nature_text = extract_between(dialogue,
        "And now, taking my leave of you, I would rehearse a tale of love",
        "'But Love desires the beautiful;")
    if not diotima_nature_text:
        diotima_nature_text = extract_between(dialogue,
            "And now, taking my leave of you, I would rehearse a tale of love",
            "But Love desires the beautiful;")

    items.append({
        "id": "speech-diotima-nature",
        "name": "Diotima's Teaching: Love as Daimon",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": normalize_paragraph(diotima_nature_text or ""),
            "Theme": "Socrates recounts the teachings of Diotima of Mantinea, a wise woman who instructed him in the mysteries of love. Love is neither beautiful nor ugly, neither god nor mortal, but a great daimon -- a spirit intermediate between divine and human. Born of Plenty and Poverty at Aphrodite's birthday feast, Love is bold yet always in want, a philosopher who is neither wise nor ignorant but forever seeking wisdom.",
            "Key Insight": "Love is a great spirit, intermediate between the divine and the mortal. He interprets between gods and men, conveying prayers upward and commands downward. Through Love, all is bound together.",
            "Reflection": "What does it mean that love is not a god but an intermediary? How does Diotima's portrait of Love as a barefoot philosopher change the way we think about desire?"
        },
        "keywords": ["diotima", "daimon", "spirit", "poverty", "plenty", "intermediate", "philosopher", "wisdom"],
        "metadata": {"speaker": "Socrates/Diotima"}
    })
    sort_order += 1

    # --- Socrates/Diotima: Love, Beauty, and Immortality ---
    diotima_imm_text = extract_between(dialogue,
        "'But Love desires the beautiful;",
        "'These are the lesser mysteries of love")
    if not diotima_imm_text:
        diotima_imm_text = extract_between(dialogue,
            "But Love desires the beautiful;",
            "These are the lesser mysteries of love")
    if not diotima_imm_text:
        # Try harder - look for surrounding text
        diotima_imm_text = extract_between(dialogue,
            "love desires the beautiful",
            "lesser mysteries of love")

    items.append({
        "id": "speech-diotima-immortality",
        "name": "Diotima's Teaching: Love and Immortality",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": normalize_paragraph(diotima_imm_text or ""),
            "Theme": "Love desires not merely the beautiful but the everlasting possession of the good -- this is happiness. Love is of birth in beauty, because all beings desire immortality. Mortal creatures achieve immortality through procreation: the body replaces itself constantly, and even knowledge must be continually renewed through recollection. Those who are pregnant in body beget children; those pregnant in soul create wisdom, virtue, poetry, and laws.",
            "Key Insight": "Love is not of beauty only, but of birth in beauty -- the principle of immortality in a mortal creature. Those creative in soul leave behind children of the mind: poems, laws, and philosophies more lasting than mortal offspring.",
            "Reflection": "What are you trying to bring to birth? Is your deepest desire for beauty, or for something beauty makes possible -- creation, legacy, immortality?"
        },
        "keywords": ["diotima", "immortality", "birth", "beauty", "creation", "soul", "procreation", "legacy"],
        "metadata": {"speaker": "Socrates/Diotima"}
    })
    sort_order += 1

    # --- Socrates/Diotima: The Ladder of Beauty ---
    diotima_ladder_text = extract_between(dialogue,
        "'These are the lesser mysteries of love",
        "Such, Phaedrus--and I speak not only to you")
    if not diotima_ladder_text:
        diotima_ladder_text = extract_between(dialogue,
            "These are the lesser mysteries of love",
            "Such, Phaedrus--and I speak not only to you")

    items.append({
        "id": "speech-diotima-ladder",
        "name": "Diotima's Teaching: The Ladder of Beauty",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Speech": normalize_paragraph(diotima_ladder_text or ""),
            "Theme": "The summit of Diotima's teaching: the Greater Mysteries of Love. One begins by loving a single beautiful form, then perceives that all beauty is of one kindred. From beautiful bodies one ascends to beautiful minds, then to beautiful laws and institutions, then to the sciences. Finally, one beholds Beauty itself -- absolute, eternal, unchanging, the source of all particular beauties. This is the famous 'Ladder of Love' or 'Ladder of Beauty.'",
            "Key Insight": "He who has been instructed thus far in the things of love, when he comes toward the end will suddenly perceive a nature of wondrous beauty -- everlasting, not growing and decaying, beauty absolute, separate, simple, and everlasting.",
            "Reflection": "Have you ever had a moment when the beauty of a particular thing opened into something universal? What would it mean to love Beauty itself, rather than any single beautiful thing?"
        },
        "keywords": ["diotima", "ladder", "ascent", "absolute-beauty", "contemplation", "eternal", "forms", "mysteries"],
        "metadata": {"speaker": "Socrates/Diotima"}
    })
    sort_order += 1

    # --- Socrates' Conclusion ---
    socrates_concl_text = extract_between(dialogue,
        "Such, Phaedrus--and I speak not only to you",
        "When Socrates had done speaking, the company applauded")

    items.append({
        "id": "speech-socrates-conclusion",
        "name": "Socrates' Conclusion: Honour Love",
        "sort_order": sort_order,
        "level": 1,
        "category": "speeches",
        "sections": {
            "Passage": normalize_paragraph(socrates_concl_text or ""),
            "About": "Socrates concludes by affirming Diotima's teaching: in the attainment of beauty and goodness, human nature will not easily find a helper better than Love. Every person ought to honour Love and walk in his ways.",
            "Reflection": "After all the elaborate speeches, Socrates ends with simplicity: honour love. What does it mean to walk in love's ways?"
        },
        "keywords": ["socrates", "conclusion", "honour", "love", "diotima"],
        "metadata": {"speaker": "Socrates"}
    })
    sort_order += 1

    # --- Arrival of Alcibiades ---
    alcibiades_arr_text = extract_between(dialogue,
        "When Socrates had done speaking, the company applauded",
        "And now, my boys, I shall praise Socrates in a figure")

    items.append({
        "id": "arrival-alcibiades",
        "name": "The Arrival of Alcibiades",
        "sort_order": sort_order,
        "level": 1,
        "category": "alcibiades",
        "sections": {
            "Passage": normalize_paragraph(alcibiades_arr_text or ""),
            "About": "The philosophical heights of Diotima's teaching are shattered by the eruption of the real world. Alcibiades bursts in drunk, crowned with ivy and violets, carried by a flute-girl and companions. He has come to crown Agathon but discovers Socrates beside him. A comic struggle ensues. Alcibiades proposes to praise not Love, but Socrates himself.",
            "Reflection": "After the ascent to eternal beauty, a drunk man stumbles in. What does Plato achieve by this dramatic contrast? Is Alcibiades the embodiment of earthly love breaking into philosophical abstraction?"
        },
        "keywords": ["alcibiades", "drunk", "arrival", "crown", "agathon", "socrates", "contrast"],
        "metadata": {"speaker": "Alcibiades"}
    })
    sort_order += 1

    # --- Alcibiades: Socrates as Silenus ---
    alc_silenus_text = extract_between(dialogue,
        "And now, my boys, I shall praise Socrates in a figure",
        "And are you not a flute-player?")
    # Get more of the speech - the Marsyas comparison and effect of Socrates' words
    alc_marsyas_text = extract_between(dialogue,
        "And are you not a flute-player?",
        "I have heard Pericles and other great orators")
    alc_effect_text = extract_between(dialogue,
        "I have heard Pericles and other great orators",
        "if he were to die, I should be ashamed")
    if not alc_effect_text:
        alc_effect_text = extract_between(dialogue,
            "I have heard Pericles and other great orators",
            "he makes me confess that I ought not to live as I do")

    combined_silenus = (alc_silenus_text or "") + "\n\n" + (alc_marsyas_text or "") + "\n\n" + (alc_effect_text or "")

    items.append({
        "id": "speech-alcibiades-silenus",
        "name": "Alcibiades' Praise: Socrates as Silenus and Marsyas",
        "sort_order": sort_order,
        "level": 1,
        "category": "alcibiades",
        "sections": {
            "Speech": normalize_paragraph(combined_silenus),
            "Theme": "Alcibiades compares Socrates to the busts of Silenus -- ugly on the outside but containing golden images of the gods within. He is like Marsyas the satyr, but produces his enchantment with words alone, without a flute. Socrates' words shame Alcibiades, making him weep and feel that his life is not worth living. No other orator, not even Pericles, has this power.",
            "Key Insight": "The outward ugliness of Socrates conceals an inner divine beauty. His words possess souls and reveal truths that their hearers would rather not face.",
            "Reflection": "Have you ever encountered someone whose words made you ashamed of how you were living? What is the difference between persuasion and the kind of soul-shaking effect Alcibiades describes?"
        },
        "keywords": ["alcibiades", "silenus", "marsyas", "satyr", "enchantment", "words", "shame", "beauty-within"],
        "metadata": {"speaker": "Alcibiades", "speech_number": 7}
    })
    sort_order += 1

    # --- Alcibiades: Personal Experience / Attempted Seduction ---
    alc_personal_text = extract_between(dialogue,
        "he makes me confess that I ought not to live as I do",
        "One day he asked me to go with him to the gymnasium")
    if not alc_personal_text:
        alc_personal_text = extract_between(dialogue,
            "And this is what I and many others have suffered",
            "One day he asked me to go with him to the gymnasium")
    if not alc_personal_text:
        # Broader extraction
        alc_personal_text = extract_between(dialogue,
            "in the days of his strength",
            "his endurance was simply marvellous")

    alc_seduction_text = extract_between(dialogue,
        "One day he asked me to go with him to the gymnasium",
        "In the morning when I awoke")
    if not alc_seduction_text:
        alc_seduction_text = extract_between(dialogue,
            "he makes me confess that I ought not to live as I do",
            "his endurance was simply marvellous")

    items.append({
        "id": "speech-alcibiades-personal",
        "name": "Alcibiades' Praise: The Attempted Seduction",
        "sort_order": sort_order,
        "level": 1,
        "category": "alcibiades",
        "sections": {
            "Speech": normalize_paragraph(alc_seduction_text or alc_personal_text or ""),
            "Theme": "Alcibiades confesses his attempt to win Socrates' love -- not for its own sake, but to gain access to Socrates' wisdom. He invited Socrates to dine alone, to exercise together, even to share a couch. But Socrates remained unmoved. The great beauty of Athens could not tempt the philosopher. Alcibiades felt humiliated yet more captivated than ever.",
            "Key Insight": "Socrates' self-mastery is absolute. He has overcome his passions not by lacking them but by ruling them. His indifference to physical beauty is the living proof of the philosophical ascent Diotima described.",
            "Reflection": "What is the relationship between self-mastery and love? Can true philosophical wisdom coexist with human desire, or must one conquer the other?"
        },
        "keywords": ["alcibiades", "seduction", "rejection", "self-mastery", "desire", "wisdom", "humiliation"],
        "metadata": {"speaker": "Alcibiades"}
    })
    sort_order += 1

    # --- Alcibiades: Military Stories ---
    alc_military_text = extract_between(dialogue,
        "his endurance was simply marvellous",
        "When Alcibiades had finished, there was a laugh")
    if not alc_military_text:
        alc_military_text = extract_between(dialogue,
            "his powers of enduring cold were also surprising",
            "When Alcibiades had finished, there was a laugh")
    if not alc_military_text:
        alc_military_text = extract_between(dialogue,
            "I will also tell, if you please",
            "When Alcibiades had finished, there was a laugh")

    items.append({
        "id": "speech-alcibiades-military",
        "name": "Alcibiades' Praise: Socrates in Battle",
        "sort_order": sort_order,
        "level": 1,
        "category": "alcibiades",
        "sections": {
            "Speech": normalize_paragraph(alc_military_text or ""),
            "Theme": "Alcibiades recounts Socrates' extraordinary conduct in military campaigns. At Potidaea, Socrates endured cold and hardship beyond all others. He stood motionless for an entire day and night, lost in thought, while soldiers watched in amazement. He saved Alcibiades' life in battle and showed supreme courage during the retreat at Delium, stalking calmly through the rout. He is utterly unlike any other human being -- comparable only to a satyr.",
            "Key Insight": "The philosopher who contemplates eternal beauty is also the bravest man on the battlefield. Socrates' otherworldly nature manifests not just in thought but in superhuman endurance and courage.",
            "Reflection": "How does Socrates' physical courage relate to his philosophical vision? Is the person who has seen something beyond this world freed from ordinary fears?"
        },
        "keywords": ["alcibiades", "potidaea", "delium", "courage", "endurance", "military", "trance", "battle"],
        "metadata": {"speaker": "Alcibiades"}
    })
    sort_order += 1

    # --- Closing Scene ---
    closing_text = extract_between(dialogue,
        "When Alcibiades had finished, there was a laugh",
        None)  # Go to end

    items.append({
        "id": "closing-scene",
        "name": "The Night Ends: Comedy and Tragedy Are One",
        "sort_order": sort_order,
        "level": 1,
        "category": "frame-narrative",
        "sections": {
            "Passage": normalize_paragraph(closing_text or ""),
            "About": "After Alcibiades finishes, a final wave of revellers bursts in, bringing disorder. The sober guests depart. Aristodemus falls asleep. When he wakes at dawn, only Socrates, Aristophanes, and Agathon remain, drinking from a large goblet. Socrates is arguing that the genius of comedy is the same as that of tragedy -- the true artist in one must be master of both. First Aristophanes, then Agathon fall asleep. Socrates rises, bathes, and goes about his day as usual.",
            "Reflection": "The dialogue ends where philosophy and life meet: Socrates, having spoken of eternal beauty, outlasts everyone at the party and walks into the morning unchanged. What does it mean that comedy and tragedy are one?"
        },
        "keywords": ["socrates", "aristophanes", "agathon", "comedy", "tragedy", "dawn", "endurance", "closing"],
        "metadata": {"speaker": "Aristodemus/Narrator"}
    })
    sort_order += 1

    # === L2 ITEMS: Groups by Speaker ===

    # Group: Phaedrus
    items.append({
        "id": "speaker-phaedrus",
        "name": "Phaedrus on Love",
        "sort_order": sort_order,
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
    sort_order += 1

    # Group: Pausanias
    items.append({
        "id": "speaker-pausanias",
        "name": "Pausanias on Love",
        "sort_order": sort_order,
        "level": 2,
        "category": "by-speaker",
        "composite_of": ["speech-pausanias"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Pausanias introduces the crucial distinction between Heavenly and Common love. His speech is more analytical than Phaedrus', attempting to separate noble love (of the mind and character) from base love (of the body). He is the political speaker, concerned with social customs and laws.",
            "For Readers": "Read Pausanias for the first attempt at philosophical discrimination: not all love is equal."
        },
        "keywords": ["pausanias", "heavenly-love", "common-love", "discrimination"],
        "metadata": {}
    })
    sort_order += 1

    # Group: Eryximachus
    items.append({
        "id": "speaker-eryximachus",
        "name": "Eryximachus on Love",
        "sort_order": sort_order,
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
    sort_order += 1

    # Group: Aristophanes
    items.append({
        "id": "speaker-aristophanes",
        "name": "Aristophanes on Love",
        "sort_order": sort_order,
        "level": 2,
        "category": "by-speaker",
        "composite_of": ["interlude-hiccough", "speech-aristophanes"],
        "relationship_type": "emergence",
        "sections": {
            "About": "The comic playwright delivers the most famous and beloved speech: the myth of the split humans. Originally whole and powerful, humans were cleaved in two by Zeus. Love is the longing to restore our original wholeness. Comic in form, deeply serious in substance -- Aristophanes touches the universal human experience of incompleteness and the desire for reunion.",
            "For Readers": "This is the speech everyone remembers. Read it for the mythic origin of romantic love and the ache of human incompleteness."
        },
        "keywords": ["aristophanes", "myth", "wholeness", "split-humans", "comedy"],
        "metadata": {}
    })
    sort_order += 1

    # Group: Agathon
    items.append({
        "id": "speaker-agathon",
        "name": "Agathon on Love",
        "sort_order": sort_order,
        "level": 2,
        "category": "by-speaker",
        "composite_of": ["speech-agathon", "interlude-pre-agathon"] if any(i["id"] == "interlude-pre-agathon" for i in items) else ["speech-agathon"],
        "relationship_type": "emergence",
        "sections": {
            "About": "The tragic poet and host of the banquet delivers a virtuoso poetic performance. Agathon's Love is young, beautiful, and the source of all the virtues. His speech is deliberate rhetoric -- beautiful but, as Socrates will show, not quite true. Yet Agathon contributes the key insight that Love must be distinguished from Love's works.",
            "For Readers": "Read Agathon for the most purely beautiful speech, and as the necessary foil to Socrates' dialectic."
        },
        "keywords": ["agathon", "poetry", "beauty", "rhetoric", "virtues"],
        "metadata": {}
    })
    sort_order += 1

    # Group: Socrates/Diotima
    items.append({
        "id": "speaker-socrates",
        "name": "Socrates and Diotima on Love",
        "sort_order": sort_order,
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
            "About": "The philosophical heart of the Symposium. Socrates first dismantles Agathon's speech through dialectic, then recounts the teachings of Diotima of Mantinea. Love is not a god but a daimon, born of Plenty and Poverty. Love desires the everlasting possession of the good. Through the famous Ladder of Beauty, one ascends from love of a single beautiful body to love of Beauty itself -- absolute, eternal, and divine. This is the philosophical climax: love as the path to transcendence.",
            "For Readers": "This is the philosophical summit of Western thought about love. Read the questioning of Agathon for Socratic method in action. Read Diotima for one of the most profound visions of love, beauty, and transcendence ever written."
        },
        "keywords": ["socrates", "diotima", "dialectic", "daimon", "ladder", "beauty", "transcendence", "philosophy"],
        "metadata": {}
    })
    sort_order += 1

    # Group: Alcibiades
    items.append({
        "id": "speaker-alcibiades",
        "name": "Alcibiades on Socrates",
        "sort_order": sort_order,
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
            "About": "After the philosophical ascent to eternal beauty, Alcibiades crashes in drunk and delivers a praise not of Love but of Socrates -- the living embodiment of the philosophical lover. Socrates is like Silenus: ugly outside, divine within. His words enchant souls. He endures superhuman hardships. He is immune to seduction. The most powerful man in Athens confesses himself utterly conquered by a barefoot philosopher. Alcibiades provides the dramatic proof of everything Diotima taught.",
            "For Readers": "Read Alcibiades for the human dimension of philosophy: what it feels like to be in the presence of someone who has truly seen the good. His speech is confession, love letter, and warning."
        },
        "keywords": ["alcibiades", "socrates", "silenus", "confession", "embodiment", "contrast"],
        "metadata": {}
    })
    sort_order += 1

    # === L2 ITEMS: Thematic Groups ===

    # Theme: The Nature of Love
    items.append({
        "id": "theme-nature-of-love",
        "name": "What Is Love?",
        "sort_order": sort_order,
        "level": 2,
        "category": "by-theme",
        "composite_of": [
            "speech-phaedrus",
            "speech-pausanias",
            "speech-eryximachus",
            "speech-aristophanes",
            "speech-agathon",
            "speech-socrates-questioning",
            "speech-diotima-nature"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "Each speaker offers a different answer to the question 'What is Love?' Phaedrus: the eldest god, source of courage. Pausanias: two loves, heavenly and common. Eryximachus: cosmic harmony. Aristophanes: the desire for wholeness. Agathon: the youngest and fairest god. Socrates/Diotima: a daimon, neither god nor mortal, the child of Plenty and Poverty, the desire for what we lack.",
            "For Readers": "Trace the evolution of understanding from speech to speech. Notice how each view is partly true and partly limited, building toward Socrates' synthesis."
        },
        "keywords": ["love", "definition", "nature", "evolution", "synthesis"],
        "metadata": {}
    })
    sort_order += 1

    # Theme: Love and Beauty
    items.append({
        "id": "theme-love-and-beauty",
        "name": "Love and Beauty",
        "sort_order": sort_order,
        "level": 2,
        "category": "by-theme",
        "composite_of": [
            "speech-agathon",
            "speech-socrates-questioning",
            "speech-diotima-ladder"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "The relationship between love and beauty is the Symposium's deepest question. Agathon claims Love is beautiful. Socrates shows that Love desires beauty, and therefore lacks it. Diotima reveals that love is the path from particular beauties to Beauty itself -- the famous ascent from bodies to souls to laws to sciences to the Form of Beauty, absolute and eternal.",
            "For Readers": "These three passages contain the philosophical core. Read them together to follow the argument from beautiful praise to beautiful truth."
        },
        "keywords": ["beauty", "form", "ascent", "absolute", "ladder", "desire"],
        "metadata": {}
    })
    sort_order += 1

    # Theme: Love and Mortality
    items.append({
        "id": "theme-love-and-mortality",
        "name": "Love and Immortality",
        "sort_order": sort_order,
        "level": 2,
        "category": "by-theme",
        "composite_of": [
            "speech-phaedrus",
            "speech-aristophanes",
            "speech-diotima-immortality"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "Love's relationship to death and immortality runs through the Symposium. Phaedrus tells of Alcestis dying for love and Achilles choosing death for honour. Aristophanes' split humans are driven by fear of further division. Diotima teaches that love is ultimately about birth in beauty -- the mortal creature's way of participating in the eternal through children, works of art, laws, and philosophical understanding.",
            "For Readers": "Follow this thread to understand why love matters so deeply: it is the mortal's path to the immortal."
        },
        "keywords": ["immortality", "death", "birth", "creation", "legacy", "mortality"],
        "metadata": {}
    })
    sort_order += 1

    # Theme: Socrates the Philosopher
    items.append({
        "id": "theme-portrait-of-socrates",
        "name": "The Portrait of Socrates",
        "sort_order": sort_order,
        "level": 2,
        "category": "by-theme",
        "composite_of": [
            "setting-banquet",
            "speech-socrates-questioning",
            "speech-alcibiades-silenus",
            "speech-alcibiades-personal",
            "speech-alcibiades-military",
            "closing-scene"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "The Symposium is, among other things, the greatest portrait of Socrates ever written. He arrives in a trance, questions rather than proclaims, and professes to know only the art of love. Alcibiades reveals him as Silenus -- grotesque outside, golden within. He is superhuman in endurance, immune to seduction, unmatched in battle. At dawn, having outlasted everyone, he simply walks into another day.",
            "For Readers": "Read these passages together for the full picture of what a philosopher looks like in the flesh -- beautiful, strange, and utterly unlike anyone else."
        },
        "keywords": ["socrates", "portrait", "philosopher", "silenus", "endurance", "self-mastery"],
        "metadata": {}
    })
    sort_order += 1

    # === L3 ITEMS: Meta-categories ===

    items.append({
        "id": "meta-speeches",
        "name": "The Seven Speeches on Love",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "composite_of": [
            "speaker-phaedrus",
            "speaker-pausanias",
            "speaker-eryximachus",
            "speaker-aristophanes",
            "speaker-agathon",
            "speaker-socrates",
            "speaker-alcibiades"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "The Symposium's seven speeches form a dramatic and philosophical arc. Each speaker contributes something to the final understanding of love, and each is characteristic of the speaker. The mythological Phaedrus, the political Pausanias, the scientific Eryximachus, the comic Aristophanes, the poetic Agathon, the philosophical Socrates, and the confessional Alcibiades -- together they compose a complete portrait of love from every human perspective: ethical, social, natural, mythic, aesthetic, metaphysical, and personal.",
            "How to Use": "Read the speeches in order for the full dramatic experience. Or dip into individual speakers to explore different facets of love. The Symposium rewards both sequential reading and thematic exploration."
        },
        "keywords": ["speeches", "love", "speakers", "arc", "philosophy", "drama"],
        "metadata": {"speech_count": 7}
    })
    sort_order += 1

    items.append({
        "id": "meta-themes",
        "name": "Great Themes of the Symposium",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "composite_of": [
            "theme-nature-of-love",
            "theme-love-and-beauty",
            "theme-love-and-mortality",
            "theme-portrait-of-socrates"
        ],
        "relationship_type": "emergence",
        "sections": {
            "About": "The Symposium weaves together several great themes: the nature of love itself, the relationship between love and beauty, love's connection to mortality and immortality, and the portrait of the philosopher as the true lover. These themes do not develop in isolation -- they interpenetrate, each speech adding new facets. The dialogue moves from common opinions about love through scientific and mythic understandings to the philosophical vision of love as the path to eternal truth.",
            "How to Use": "Browse by theme when you want to follow a single thread across all the speeches. Each theme gathers the relevant passages from different speakers, showing how the same question looks from mythological, comic, poetic, and philosophical perspectives."
        },
        "keywords": ["themes", "beauty", "immortality", "philosophy", "love"],
        "metadata": {"theme_count": 4}
    })
    sort_order += 1

    items.append({
        "id": "meta-dramatic-structure",
        "name": "The Dramatic Structure",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "composite_of": [
            "frame-apollodorus",
            "setting-banquet",
            "interlude-hiccough",
            "arrival-alcibiades",
            "closing-scene"
        ] + (["interlude-pre-agathon"] if any(i["id"] == "interlude-pre-agathon" for i in items) else []),
        "relationship_type": "emergence",
        "sections": {
            "About": "The Symposium is not just philosophy but supreme dramatic art. The frame narrative (Apollodorus retelling a story he heard from Aristodemus) creates deliberate distance. The setting at a victory banquet grounds the philosophy in life. Comic interludes (the hiccough, Alcibiades' drunken entrance) punctuate the serious speeches. The closing scene -- Socrates arguing that comedy and tragedy are one, while the poets fall asleep -- is one of the most extraordinary endings in literature.",
            "How to Use": "Read the frame and interludes to appreciate the Symposium as a work of art, not just a collection of arguments. Plato is a dramatist as much as a philosopher."
        },
        "keywords": ["drama", "structure", "frame", "narrative", "art", "comedy", "tragedy"],
        "metadata": {}
    })
    sort_order += 1

    # Build the grammar
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Plato",
                    "date": "c. 385-370 BCE",
                    "note": "Author"
                },
                {
                    "name": "Benjamin Jowett",
                    "date": "1871",
                    "note": "Translator"
                },
                {
                    "name": "Project Gutenberg",
                    "date": "1999",
                    "note": "eBook #1600 (https://www.gutenberg.org/ebooks/1600)"
                }
            ]
        },
        "name": "Symposium",
        "description": "Plato's Symposium (c. 385-370 BCE) -- the most perfect dialogue on the nature of love ever written. At a banquet celebrating the tragic poet Agathon's first victory, seven speakers offer speeches in praise of Love (Eros). From Phaedrus' mythological praise through Aristophanes' famous myth of the split humans to Socrates' account of Diotima's 'Ladder of Beauty' -- the ascent from earthly love to the contemplation of Beauty itself -- the Symposium traces every dimension of love: ethical, cosmic, comic, poetic, philosophical, and confessional. Benjamin Jowett translation. Source: Project Gutenberg eBook #1600 (https://www.gutenberg.org/ebooks/1600).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Anselm Feuerbach's 'The Symposium' (1869, second version 1873) -- monumental oil painting of the banquet scene, Nationalgalerie Berlin, public domain. Greek red-figure pottery depicting symposia (banquet scenes), widely available from museum collections. Jacques-Louis David's 'The Death of Socrates' (1787) for the figure of Socrates. Raphael's 'The School of Athens' (1509-1511) for Plato's figure. John Flaxman's line illustrations of Greek subjects (early 19th century), public domain.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "philosophy",
            "love",
            "plato",
            "greek",
            "dialogue",
            "beauty",
            "wisdom",
            "public-domain",
            "full-text"
        ],
        "roots": [
            "greek-philosophy"
        ],
        "shelves": [
            "wisdom"
        ],
        "lineages": [
            "Shrei",
            "Andreotti"
        ],
        "worldview": "dialectical",
        "items": items
    }

    return grammar


def extract_between(text, start_marker, end_marker):
    """Extract text between two markers. If end_marker is None, extract to end."""
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return None
    if end_marker is None:
        return text[start_idx:].strip()
    end_idx = text.find(end_marker, start_idx + len(start_marker))
    if end_idx == -1:
        return None
    return text[start_idx:end_idx].strip()


def main():
    print("Building Symposium grammar...")
    grammar = build_grammar()

    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Print summary
    l1_count = sum(1 for i in grammar["items"] if i["level"] == 1)
    l2_count = sum(1 for i in grammar["items"] if i["level"] == 2)
    l3_count = sum(1 for i in grammar["items"] if i["level"] == 3)
    total = len(grammar["items"])

    print(f"Written to {OUTPUT_PATH}")
    print(f"Total items: {total}")
    print(f"  L1 (passages): {l1_count}")
    print(f"  L2 (groups):   {l2_count}")
    print(f"  L3 (meta):     {l3_count}")

    # Verify no empty speeches
    empty_count = 0
    for item in grammar["items"]:
        for section_name, section_text in item.get("sections", {}).items():
            if section_name in ("Speech", "Passage") and len(section_text.strip()) < 50:
                print(f"  WARNING: {item['id']} has very short {section_name} ({len(section_text.strip())} chars)")
                empty_count += 1
    if empty_count == 0:
        print("  All speech/passage sections have content.")


if __name__ == "__main__":
    main()
