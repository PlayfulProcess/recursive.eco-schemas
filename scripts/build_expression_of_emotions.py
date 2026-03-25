#!/usr/bin/env python3
"""
Build grammar.json for Darwin's Expression of the Emotions in Man and Animals.

Source: Project Gutenberg eBook #1227
Author: Charles Darwin (1872)

Structure:
- Introduction + 14 chapters + Footnotes
- L1: Introduction + 14 chapters
- L2: Thematic groupings (3)
- L3: Meta-category
"""

import json
import re
from pathlib import Path

SEED_PATH = Path(__file__).parent.parent / "seeds" / "expression-of-emotions.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "expression-of-emotions"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Chapter info: (marker_in_text, clean_title, id, keywords, about)
CHAPTERS = [
    {
        "marker": "INTRODUCTION.\n\n\nMany works have been written",
        "title": "Introduction",
        "id": "introduction",
        "keywords": ["introduction", "expression", "physiognomy", "bell", "duchenne", "photography"],
        "about": "Darwin surveys the history of studying expression, from Le Brun's 'Conferences' (1667) to Sir Charles Bell's groundbreaking anatomy of expression. He introduces his methodology: photographs, direct observation of infants, the insane, different cultures, and animals. He poses the central question: why do particular muscles move in response to particular emotions?"
    },
    {
        "marker": "CHAPTER I. GENERAL PRINCIPLES OF EXPRESSION.",
        "title": "General Principles of Expression",
        "id": "chapter-1-principles",
        "keywords": ["principles", "habit", "inheritance", "reflex", "association"],
        "about": "Darwin's first principle: Serviceable Associated Habits. Certain complex actions are useful in response to certain states of mind; through habit and association, they are performed whenever the same state of mind arises, even when not useful. These habits become inherited over generations. Examples range from dogs scratching the ground to humans clenching fists in anger."
    },
    {
        "marker": "CHAPTER II. GENERAL PRINCIPLES OF EXPRESSION",
        "title": "General Principles of Expression (continued): Antithesis",
        "id": "chapter-2-antithesis",
        "keywords": ["antithesis", "opposite", "posture", "dogs", "cats", "contrast"],
        "about": "Darwin's second principle: Antithesis. When a directly opposite state of mind is induced, there is a strong tendency to perform movements of a directly opposite nature -- even though these are of no use. A dog's hostile crouch versus its joyful wriggle; a cat's arched back versus its relaxed stretch. The body speaks in contrasts."
    },
    {
        "marker": "CHAPTER III. GENERAL PRINCIPLES OF EXPRESSION",
        "title": "General Principles of Expression (concluded): Nervous Discharge",
        "id": "chapter-3-nervous-discharge",
        "keywords": ["nervous-system", "discharge", "trembling", "overflow", "excitement"],
        "about": "Darwin's third principle: Direct Action of the Nervous System. When the sensorium is strongly excited, nerve-force is generated in excess and transmitted in certain directions -- producing trembling, sweating, changes in heartbeat, and other involuntary effects. These are not purposeful but are the overflow of intense feeling."
    },
    {
        "marker": "CHAPTER IV. MEANS OF EXPRESSION IN ANIMALS.",
        "title": "Means of Expression in Animals",
        "id": "chapter-4-animal-expression",
        "keywords": ["animals", "sounds", "erection", "hair", "ears", "tail", "vocal"],
        "about": "Darwin catalogs the expressive means available to animals: vocal sounds (from insects to mammals), erection of hair and feathers, movements of ears and tails, inflation of the body. He shows how these serve as signals -- intentional or not -- and traces their evolutionary origins in serviceable habits."
    },
    {
        "marker": "CHAPTER V. SPECIAL EXPRESSIONS OF ANIMALS.",
        "title": "Special Expressions of Animals",
        "id": "chapter-5-animal-special",
        "keywords": ["dogs", "cats", "horses", "monkeys", "affection", "hostility", "submission"],
        "about": "Detailed observations of specific animal expressions: a dog's devoted gaze, a cat's purring contentment, a horse's laying back its ears, a monkey's grin of terror. Darwin draws on zoological gardens, domestic animals, and correspondents worldwide. The continuity between animal and human expression is his central theme."
    },
    {
        "marker": "CHAPTER VI. SPECIAL EXPRESSIONS OF MAN: SUFFERING AND WEEPING.",
        "title": "Suffering and Weeping",
        "id": "chapter-6-suffering-weeping",
        "keywords": ["suffering", "weeping", "tears", "screaming", "infants", "grief", "pain"],
        "about": "Why do we cry? Darwin traces the physiology of weeping from the screaming infant (whose eye muscles contract to protect blood vessels during violent expiration) to the adult who weeps silently. Tears are initially a side-effect of muscular contraction around the eyes; they become associated with suffering through habit. The chapter is both rigorous science and deeply humane observation."
    },
    {
        "marker": "CHAPTER VII. LOW SPIRITS, ANXIETY, GRIEF, DEJECTION, DESPAIR.",
        "title": "Low Spirits, Anxiety, Grief, Dejection, Despair",
        "id": "chapter-7-low-spirits",
        "keywords": ["grief", "anxiety", "despair", "dejection", "eyebrows", "corners-of-mouth", "posture"],
        "about": "The anatomy of sadness: oblique eyebrows (the 'grief muscles'), downturned corners of the mouth, slumped posture, slow movements. Darwin shows how these expressions are the antithesis of joy and high spirits. He discusses the remarkable obliquity of the eyebrows in grief -- a movement most people cannot perform voluntarily but which appears involuntarily in genuine sorrow."
    },
    {
        "marker": "CHAPTER VIII. JOY, HIGH SPIRITS, LOVE, TENDER FEELINGS, DEVOTION.",
        "title": "Joy, High Spirits, Love, Tender Feelings, Devotion",
        "id": "chapter-8-joy-love",
        "keywords": ["joy", "laughter", "smiling", "love", "tenderness", "devotion", "bright-eyes"],
        "about": "The expressions of happiness: bright eyes, upturned mouth corners, laughter's whole-body engagement. Darwin connects smiling to the contraction of the zygomatic muscles and distinguishes genuine (Duchenne) smiles from forced ones. He also explores the expressions of love -- tender gazes, gentle touches -- and devotion, linking religious feeling to the same muscular patterns as filial love."
    },
    {
        "marker": "CHAPTER IX. REFLECTION",
        "title": "Reflection, Meditation, Ill-Temper, Sulkiness, Determination",
        "id": "chapter-9-reflection-determination",
        "keywords": ["reflection", "meditation", "ill-temper", "sulkiness", "determination", "frown", "concentration"],
        "about": "The furrowed brow of thought, the pursed lips of concentration, the jutting jaw of determination. Darwin shows how the same muscles used in physical effort (squinting against sun, bracing for impact) are recruited metaphorically for mental effort. Ill-temper and sulkiness are forms of suppressed action -- the body poised to fight but restrained."
    },
    {
        "marker": "CHAPTER X. HATRED AND ANGER.",
        "title": "Hatred and Anger",
        "id": "chapter-10-hatred-anger",
        "keywords": ["hatred", "anger", "rage", "teeth", "fists", "reddening", "violence"],
        "about": "Anger engages the whole body: reddened face, dilated nostrils, bared teeth, clenched fists, quickened breathing. Darwin traces these to the preparations for physical combat -- actions once serviceable that now persist as expressions. He distinguishes rage (explosive, forward-leaning) from hatred (cold, withdrawn) and shows how anger's expression is remarkably consistent across cultures."
    },
    {
        "marker": "CHAPTER XI. DISDAIN",
        "title": "Disdain, Contempt, Disgust, Guilt, Pride",
        "id": "chapter-11-disdain-contempt",
        "keywords": ["disdain", "contempt", "disgust", "guilt", "pride", "sneer", "lip-curl"],
        "about": "The curled lip of contempt, the wrinkled nose of disgust, the averted gaze of disdain. Darwin traces disgust to the rejection of offensive food -- a literal pushing away that becomes metaphorical. The sneer (unilateral lip raise) is one of the most ancient human expressions, shared with snarling animals. Guilt is expressed through averted eyes and a desire to hide; pride through expanded chest and raised head."
    },
    {
        "marker": "CHAPTER XII. SURPRISE",
        "title": "Surprise, Astonishment, Fear, Horror",
        "id": "chapter-12-surprise-fear",
        "keywords": ["surprise", "astonishment", "fear", "horror", "wide-eyes", "open-mouth", "hair-standing"],
        "about": "The wide eyes of surprise, the open mouth of astonishment, the rigid posture of fear, the contracted features of horror. Darwin shows how surprise expressions serve sensory functions (wide eyes admit more light, open mouth allows quick breathing) while fear expressions prepare the body for flight. Hair standing on end is a vestige of the animal response that makes creatures appear larger to predators."
    },
    {
        "marker": "CHAPTER XIII. SELF-ATTENTION",
        "title": "Self-Attention, Shame, Shyness, Modesty: Blushing",
        "id": "chapter-13-blushing",
        "keywords": ["blushing", "shame", "shyness", "modesty", "self-attention", "face", "social"],
        "about": "Darwin's most original chapter. Blushing is uniquely human and uniquely social -- it cannot be produced voluntarily and occurs only when we think others are observing or judging us. It affects the face, ears, and neck because these are the parts most attended to by others. Darwin shows that blushing occurs in all human races and is more intense in those who are most attentive to the opinion of others."
    },
    {
        "marker": "CHAPTER XIV. CONCLUDING REMARKS AND SUMMARY.",
        "title": "Concluding Remarks and Summary",
        "id": "chapter-14-conclusion",
        "keywords": ["summary", "conclusion", "universality", "evolution", "cross-cultural", "continuity"],
        "about": "Darwin summarizes his three principles and their application across the animal kingdom. He emphasizes the universality of human expression across races and cultures -- evidence against the theory that expressions are culturally learned. The continuity between human and animal expression supports evolution by showing that our most intimate feelings are rooted in our animal nature."
    }
]


def read_and_extract():
    """Read seed text, strip Gutenberg header/footer."""
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start == -1 or end == -1:
        raise ValueError("Could not find Gutenberg markers")

    text = text[start:end]
    text = text[text.find('\n') + 1:]

    # Remove footnotes section at end
    fn_start = text.find("\nFOOTNOTES:\n")
    if fn_start != -1:
        text = text[:fn_start]

    return text.strip()


def clean_text(text):
    """Remove footnote refs, illustration markers, normalize."""
    if not text:
        return ""
    # Remove inline footnote references like [101], [1]
    text = re.sub(r'\[\d+\]', '', text)
    # Remove illustration/figure references
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    text = re.sub(r'\[See Illustration[^\]]*\]', '', text)
    # Remove italic markers
    text = re.sub(r'_([^_]+)_', r'\1', text)
    # Normalize whitespace
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


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
    full_text = read_and_extract()

    items = []
    so = 0

    def add_item(item):
        nonlocal so
        item["sort_order"] = so
        items.append(item)
        so += 1

    def ct(text):
        return normalize(clean_text(text))

    # =========================================================================
    # L1 ITEMS - Chapters
    # =========================================================================

    chapter_ids = []
    for i, ch in enumerate(CHAPTERS):
        # Find chapter text
        start_idx = full_text.find(ch["marker"])
        if start_idx == -1:
            print(f"WARNING: Could not find marker for {ch['title']}: '{ch['marker']}'")
            continue

        # Find next chapter (or end)
        if i + 1 < len(CHAPTERS):
            next_marker = CHAPTERS[i + 1]["marker"]
            end_idx = full_text.find(next_marker, start_idx + len(ch["marker"]))
            if end_idx == -1:
                chapter_text = full_text[start_idx:]
            else:
                chapter_text = full_text[start_idx:end_idx]
        else:
            chapter_text = full_text[start_idx:]

        # Skip the chapter heading and summary line (first paragraph or two)
        # Keep the body text
        chapter_text = chapter_text.strip()

        chapter_ids.append(ch["id"])
        add_item({
            "id": ch["id"],
            "name": ch["title"],
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": ct(chapter_text),
                "About": ch["about"],
                "Reflection": "What does Darwin's careful observation of this emotion teach us about the connection between body and mind? How do you recognize this expression in yourself and others?"
            },
            "keywords": ch["keywords"],
            "metadata": {"chapter": i if ch["id"] == "introduction" else i}
        })

    # =========================================================================
    # L2 ITEMS - Thematic groupings
    # =========================================================================

    add_item({
        "id": "theme-foundations",
        "name": "The Three Principles and Animal Expression",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "The first five chapters establish Darwin's theoretical framework: three principles explain virtually all expressions in humans and animals. (1) Serviceable Associated Habits: actions useful in one context become habitual and persist even when not useful. (2) Antithesis: opposite mental states produce opposite bodily movements. (3) Direct Nervous Discharge: excess nerve-force overflows into trembling, sweating, and other involuntary effects. These principles are then demonstrated across the animal kingdom.",
            "For Readers": "Darwin's three principles remain influential in emotion science today. Notice how he builds from simple observations (a dog turning in circles before lying down) to profound theories about the evolution of feeling itself."
        },
        "keywords": ["principles", "habits", "antithesis", "nervous-discharge", "animals", "evolution"],
        "metadata": {},
        "composite_of": ["introduction", "chapter-1-principles", "chapter-2-antithesis", "chapter-3-nervous-discharge", "chapter-4-animal-expression", "chapter-5-animal-special"]
    })

    add_item({
        "id": "theme-dark-emotions",
        "name": "The Dark Emotions: Suffering, Grief, Anger, Fear",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "Darwin's exploration of painful emotions -- from the tears of suffering through the slumped posture of grief to the clenched fists of anger and the wide eyes of terror. These chapters are remarkable for their combination of precise anatomical description and deep empathy. Darwin sees in every grimace and tremor both a biological mechanism and a window into the universal experience of being alive.",
            "For Readers": "These chapters form the heart of the book. Darwin's descriptions of grief, anger, and fear are so precise that they can be used as a guide to reading the emotions of people around you. Notice how he consistently traces 'higher' human emotions back to bodily preparations for action."
        },
        "keywords": ["suffering", "grief", "anger", "fear", "horror", "tears", "rage"],
        "metadata": {},
        "composite_of": ["chapter-6-suffering-weeping", "chapter-7-low-spirits", "chapter-10-hatred-anger", "chapter-12-surprise-fear"]
    })

    add_item({
        "id": "theme-social-emotions",
        "name": "The Social Emotions: Joy, Love, Shame, and Blushing",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "Darwin's exploration of emotions that arise specifically in social context -- the bright eyes of joy, the tender gaze of love, the averted eyes of guilt, and above all, the uniquely human phenomenon of blushing. These chapters reveal Darwin at his most original: blushing, he argues, is evidence that human consciousness is fundamentally social. We flush not from heat or exertion but from the mere thought that others are looking at us.",
            "For Readers": "Darwin's chapter on blushing is perhaps the most philosophically rich in the book. It shows that our bodies are social instruments: they respond not just to physical stimuli but to the gaze and judgment of others. This is Darwin's contribution to understanding what makes humans unique."
        },
        "keywords": ["joy", "love", "shame", "blushing", "pride", "social", "self-consciousness"],
        "metadata": {},
        "composite_of": ["chapter-8-joy-love", "chapter-9-reflection-determination", "chapter-11-disdain-contempt", "chapter-13-blushing", "chapter-14-conclusion"]
    })

    # =========================================================================
    # L3 ITEMS - Meta-category
    # =========================================================================

    add_item({
        "id": "meta-expression-emotions",
        "name": "The Expression of the Emotions: Darwin's Human Science",
        "level": 3,
        "category": "meta-category",
        "sections": {
            "About": "Published in 1872, The Expression of the Emotions in Man and Animals is Darwin's most humanistic work. While On the Origin of Species established evolution as a biological fact, this book extends it into the realm of feeling, arguing that our most intimate emotional experiences -- grief, joy, love, shame -- are continuous with those of other animals and are universal across all human cultures. Darwin's three principles of expression remain foundational in affective science, and his method of combining cross-cultural observation, infant studies, photography, and animal behavior set the pattern for modern emotion research.",
            "For Readers": "This book is Darwin at his most accessible and his most profound. Every chapter offers practical insights into reading emotions in yourself and others. It is also a quietly revolutionary argument: that there is no emotion, no matter how 'spiritual' it seems, that does not have its roots in the body and its parallels in the animal world."
        },
        "keywords": ["darwin", "evolution", "emotion", "expression", "universality", "animals", "humans", "science"],
        "metadata": {},
        "composite_of": ["theme-foundations", "theme-dark-emotions", "theme-social-emotions"]
    })

    # =========================================================================
    # BUILD GRAMMAR
    # =========================================================================

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Charles Darwin", "date": "1872", "note": "Author"},
                {"name": "Project Gutenberg", "date": "1998", "note": "Source: eBook #1227 (https://www.gutenberg.org/ebooks/1227)"}
            ]
        },
        "name": "The Expression of the Emotions in Man and Animals",
        "description": "Darwin's groundbreaking study of emotional expression across humans and animals (1872). Combining photography, cross-cultural surveys, infant observation, and comparative anatomy, Darwin argues that our emotions are not cultural inventions but biological inheritances shared with other species. Fourteen chapters trace the expressions of grief, joy, anger, love, fear, shame, and more, establishing the foundations of modern affective science.\n\nSource: Project Gutenberg eBook #1227 (https://www.gutenberg.org/ebooks/1227)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: The book's own photographic plates by Oscar Rejlander and others (1872 edition); drawings by Mr. T.W. Wood and Mr. A. May of animal expressions; the Duchenne de Boulogne photographs of facial muscles and expression (1862).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["science", "emotion", "darwin", "evolution", "expression", "animals", "psychology", "body", "universality", "photography"],
        "roots": ["emotion-love"],
        "shelves": ["mirror"],
        "lineages": ["Gottman", "Johnson"],
        "worldview": "rationalist",
        "items": items
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"Built Expression of Emotions grammar: {len(items)} items")
    for item in items:
        text_len = len(item["sections"].get("Text", ""))
        print(f"  L{item['level']}: {item['id']} - {item['name']} ({text_len} chars)")


if __name__ == "__main__":
    build_grammar()
