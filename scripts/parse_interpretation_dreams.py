#!/usr/bin/env python3
"""
Parse Freud's "The Interpretation of Dreams" from Project Gutenberg into grammar.json.

Source: Project Gutenberg eBook #66048, translated by A. A. Brill (1913).
"""

import json
import re
import os

SEED_FILE = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'interpretation-of-dreams.txt')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'interpretation-of-dreams', 'grammar.json')

# Chapter definitions: (roman_numeral_centered, title_lines, id, name, keywords)
CHAPTERS = [
    {
        "roman": "I",
        "title": "THE SCIENTIFIC LITERATURE ON THE PROBLEMS OF THE DREAM",
        "id": "chapter-1-scientific-literature",
        "name": "I. The Scientific Literature on the Problems of the Dream",
        "keywords": ["dream research", "literature review", "dream theories", "history of dream interpretation"],
        "group": "theory",
    },
    {
        "roman": "II",
        "title": "METHOD OF DREAM INTERPRETATION",
        "id": "chapter-2-method-of-interpretation",
        "name": "II. Method of Dream Interpretation: The Analysis of a Sample Dream",
        "keywords": ["free association", "dream analysis", "Irma's injection", "interpretation method"],
        "group": "clinical",
    },
    {
        "roman": "III",
        "title": "THE DREAM IS THE FULFILMENT OF A WISH",
        "id": "chapter-3-wish-fulfilment",
        "name": "III. The Dream Is the Fulfilment of a Wish",
        "keywords": ["wish fulfillment", "dream function", "desire", "dream meaning"],
        "group": "theory",
    },
    {
        "roman": "IV",
        "title": "DISTORTION IN DREAMS",
        "id": "chapter-4-distortion",
        "name": "IV. Distortion in Dreams",
        "keywords": ["dream distortion", "censorship", "dream censor", "disguise", "repression"],
        "group": "theory",
    },
    {
        "roman": "V",
        "title": "THE MATERIAL AND SOURCES OF DREAMS",
        "id": "chapter-5-material-and-sources",
        "name": "V. The Material and Sources of Dreams",
        "keywords": ["dream sources", "recent impressions", "childhood memories", "somatic stimuli", "typical dreams"],
        "group": "clinical",
    },
    {
        "roman": "VI",
        "title": "THE DREAM-WORK",
        "id": "chapter-6-dream-work",
        "name": "VI. The Dream-Work",
        "keywords": ["condensation", "displacement", "symbolism", "dream-work", "secondary elaboration", "representation"],
        "group": "dreamwork",
    },
    {
        "roman": "VII",
        "title": "THE PSYCHOLOGY OF THE DREAM ACTIVITIES",
        "id": "chapter-7-psychology-of-dream-activities",
        "name": "VII. The Psychology of the Dream Activities",
        "keywords": ["forgetting dreams", "regression", "unconscious", "wish fulfillment", "dream process", "primary process"],
        "group": "theory",
    },
]

# Also capture Introductory Remarks and Prefaces as a combined item
PREFACE_ID = "introductory-remarks"

# L2 groupings
L2_GROUPS = [
    {
        "id": "theory-of-dreams",
        "name": "Theory of Dreams",
        "category": "thematic-group",
        "keywords": ["dream theory", "wish fulfillment", "dream psychology", "unconscious"],
        "composite_of": ["chapter-1-scientific-literature", "chapter-3-wish-fulfilment", "chapter-4-distortion", "chapter-7-psychology-of-dream-activities"],
        "about": "These chapters present Freud's theoretical framework for understanding dreams. Beginning with a comprehensive survey of prior dream research (Chapter I), Freud establishes the central thesis that every dream represents the fulfillment of a wish (Chapter III), explains the mechanisms of disguise and censorship that obscure dream meaning (Chapter IV), and concludes with a sweeping model of the psychic apparatus and the role of the unconscious in dream formation (Chapter VII). Together they form the philosophical and psychological backbone of psychoanalytic dream theory.",
        "how_to_use": "Read these chapters to understand Freud's core argument: that dreams are meaningful psychological products, not random neural firings. Chapter I provides historical context, Chapter III the thesis, Chapter IV the first complication (why dreams aren't obviously wish-fulfilling), and Chapter VII the full theoretical synthesis. These chapters reward slow reading and re-reading.",
    },
    {
        "id": "dream-work-chapters",
        "name": "The Dream-Work",
        "category": "thematic-group",
        "keywords": ["condensation", "displacement", "symbolism", "dream mechanisms", "representation"],
        "composite_of": ["chapter-6-dream-work"],
        "about": "Chapter VI is the longest and most technically detailed chapter in the book, comprising nearly a third of the entire text. It describes the four mechanisms by which latent dream-thoughts are transformed into the manifest dream content: condensation (combining multiple ideas into one image), displacement (shifting emotional emphasis), representability (translating abstract thoughts into visual images), and secondary elaboration (the mind's attempt to impose narrative coherence on the dream). This chapter is the operational heart of Freud's dream theory.",
        "how_to_use": "This chapter is essential for anyone who wants to actually interpret dreams using Freud's method. Each mechanism is illustrated with detailed dream examples. Read it as a practical manual alongside the theoretical chapters.",
    },
    {
        "id": "clinical-chapters",
        "name": "Clinical Method and Dream Material",
        "category": "thematic-group",
        "keywords": ["clinical method", "free association", "dream examples", "case studies", "dream sources"],
        "composite_of": ["introductory-remarks", "chapter-2-method-of-interpretation", "chapter-5-material-and-sources"],
        "about": "These chapters demonstrate Freud's clinical approach to dreams. The Introductory Remarks frame the work's therapeutic origins. Chapter II introduces the method of free association through the famous 'Dream of Irma's Injection' — the first complete dream analysis ever published. Chapter V explores where dreams get their raw material: recent experiences, childhood memories, and bodily sensations, including a rich catalogue of 'typical dreams' (falling, flying, nakedness, death of loved ones, examinations). Together they show psychoanalytic dream interpretation in practice.",
        "how_to_use": "Start with Chapter II for the clearest demonstration of Freud's method. Chapter V is the most accessible and entertaining chapter, full of vivid dream examples. These chapters are the best entry point for readers new to Freud.",
    },
]


def verify_seed(text):
    """Confirm this is the right text."""
    assert "Interpretation of Dreams" in text[:1000], "Wrong seed file"
    assert "Sigmund Freud" in text[:1000] or "SIGMUND FREUD" in text[:1000], "Wrong seed file"


def extract_body(text):
    """Extract text between Gutenberg markers."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE INTERPRETATION OF DREAMS ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE INTERPRETATION OF DREAMS ***"
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker)
    return text[start:end]


def find_chapter_boundaries(lines):
    """Find the line indices where each chapter starts."""
    boundaries = {}

    # Find "INTRODUCTORY REMARKS"
    for i, line in enumerate(lines):
        if line.strip() == "INTRODUCTORY REMARKS":
            boundaries["preface"] = i
            break

    # Find each chapter by its centered Roman numeral
    # Pattern: line is just the roman numeral (centered with spaces), followed by the title
    for ch in CHAPTERS:
        roman = ch["roman"]
        title_start = ch["title"].split()[0:3]  # first few words of title
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == roman:
                # Check next non-empty line contains the chapter title start
                for j in range(i + 1, min(i + 5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and all(w in next_line for w in title_start[:2]):
                        # Skip if this is in the CONTENTS section (before line ~300 in body)
                        if i < 250:  # rough check - CONTENTS is near start
                            # Verify it's not in CONTENTS by checking for page numbers
                            if any(c.isdigit() for c in next_line[-5:]):
                                continue
                        boundaries[ch["id"]] = i
                        break
                if ch["id"] in boundaries:
                    break

    # Find LITERARY INDEX (VIII) to know where VII ends
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "VIII":
            for j in range(i + 1, min(i + 5, len(lines))):
                if "LITERARY INDEX" in lines[j]:
                    boundaries["literary-index"] = i
                    break
            if "literary-index" in boundaries:
                break

    return boundaries


def truncate_text(text, max_chars=2800):
    """Truncate text at ~max_chars, finding last period before cutoff."""
    if len(text) <= max_chars:
        return text
    bp = text.rfind(".", 0, max_chars)
    if bp == -1:
        bp = max_chars
    truncated = text[:bp + 1]
    remaining_words = len(text[bp + 1:].split())
    return truncated + f" [Text continues for approximately {remaining_words} more words...]"


def clean_text(text):
    """Clean extracted text: normalize whitespace, strip footnote markers."""
    # Remove footnote markers like [1], [66], etc.
    text = re.sub(r'\[(?:Footnote )?\d+\]', '', text)
    # Remove [D], [E] etc. reference markers
    text = re.sub(r'\[[A-Z]\]', '', text)
    # Normalize multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


def extract_chapter_text(lines, start_idx, end_idx):
    """Extract and clean the text of a chapter."""
    raw = "\n".join(lines[start_idx:end_idx])
    return clean_text(raw)


def main():
    with open(SEED_FILE, 'r', encoding='utf-8') as f:
        full_text = f.read()

    verify_seed(full_text)
    body = extract_body(full_text)
    lines = body.split('\n')

    boundaries = find_chapter_boundaries(lines)
    print(f"Found boundaries: {list(boundaries.keys())}")
    for k, v in boundaries.items():
        print(f"  {k}: line {v} -> {lines[v].strip()}")

    # Build ordered list of boundary positions for determining chapter end points
    chapter_ids_ordered = ["preface"] + [ch["id"] for ch in CHAPTERS] + ["literary-index"]
    boundary_positions = []
    for cid in chapter_ids_ordered:
        if cid in boundaries:
            boundary_positions.append((cid, boundaries[cid]))

    items = []
    sort_order = 1

    # Extract each chapter's text
    for idx, (cid, start_line) in enumerate(boundary_positions):
        if cid == "literary-index":
            break  # Don't include the index

        # End is the start of the next section
        if idx + 1 < len(boundary_positions):
            end_line = boundary_positions[idx + 1][1]
        else:
            end_line = len(lines)

        text = extract_chapter_text(lines, start_line, end_line)
        truncated = truncate_text(text)

        if cid == "preface":
            item = {
                "id": PREFACE_ID,
                "name": "Introductory Remarks and Prefaces",
                "sort_order": sort_order,
                "category": "preface",
                "level": 1,
                "sections": {
                    "Text": truncated,
                    "About": "Freud's introductory remarks and prefaces to the first three editions of The Interpretation of Dreams. He explains why he had to use his own dreams as primary material — patient dreams were complicated by neurotic features, and using his own required painful self-exposure. The prefaces to later editions note the book's growing recognition and Freud's conviction that it contains his most valuable discoveries.",
                    "Significance": "These pages reveal Freud's awareness that he was doing something unprecedented: systematically analysing his own unconscious. His candour about the personal cost of this self-exposure — and his insistence that the scientific value justified it — set the tone for the entire work."
                },
                "keywords": ["preface", "self-analysis", "methodology", "personal disclosure"],
                "metadata": {}
            }
        else:
            ch = next(c for c in CHAPTERS if c["id"] == cid)
            item = {
                "id": ch["id"],
                "name": ch["name"],
                "sort_order": sort_order,
                "category": "chapter",
                "level": 1,
                "sections": {
                    "Text": truncated,
                    "Keywords": ", ".join(ch["keywords"]),
                },
                "keywords": ch["keywords"],
                "metadata": {}
            }

        items.append(item)
        sort_order += 1
        print(f"  Created L1: {item['id']} ({len(text)} chars -> {len(truncated)} chars)")

    # Add chapter-specific About and Significance sections
    chapter_descriptions = {
        "chapter-1-scientific-literature": {
            "About": "A comprehensive survey of all prior scientific and philosophical writing on dreams, from Aristotle to the late 19th century. Freud systematically reviews theories about dream sources (external stimuli, internal sensations, psychic causes), the relationship between dreaming and waking life, the moral character of dreams, and theories of dream function. He identifies the key unsolved problems that his own theory will address.",
            "Significance": "This chapter establishes Freud's scholarly credentials and frames the interpretive void his work will fill. By showing that no prior theory could adequately explain why dreams take their particular form, he prepares the ground for his revolutionary claim that dreams have hidden meaning accessible through a specific analytical method."
        },
        "chapter-2-method-of-interpretation": {
            "About": "Freud introduces the method of free association as an alternative to both symbolic dream interpretation (assigning fixed meanings) and cipher methods (decoding element by element). He then demonstrates the method through the complete analysis of his own 'Dream of Irma's Injection' (July 23-24, 1895) — the first fully interpreted dream in the history of psychoanalysis. The analysis reveals the dream as fulfilling Freud's wish to be absolved of responsibility for a patient's incomplete cure.",
            "Significance": "The Dream of Irma's Injection is psychoanalysis's founding dream. Freud's willingness to expose his professional anxieties, rivalries, and guilt through this analysis established the template for all subsequent dream interpretation. The chapter demonstrates that even seemingly bizarre dream content yields coherent meaning when each element is traced through free association."
        },
        "chapter-3-wish-fulfilment": {
            "About": "Building on the Irma dream analysis, Freud advances his central thesis: every dream is the fulfilment of a wish. He supports this with children's dreams (which transparently fulfill wishes like eating cherries or visiting a lake) and 'convenience dreams' (dreaming of drinking water when thirsty). The brevity and clarity of children's dreams reveal the basic dream mechanism before the complications of adult psychic life distort it.",
            "Significance": "This short, pivotal chapter states the book's core claim with striking boldness. By beginning with children's dreams — simple, transparent, and undeniable — Freud builds an intuitive foundation before addressing the obvious objection: what about anxiety dreams and nightmares? That objection drives the next chapter."
        },
        "chapter-4-distortion": {
            "About": "Freud addresses the central objection to wish-fulfilment theory: many dreams are unpleasant or frightening. He introduces the concept of dream distortion — the process by which the 'dream censor' disguises unacceptable wishes to allow them past the threshold of consciousness. Using political censorship as an analogy, Freud argues that the more objectionable the wish, the more thoroughly it is disguised. Dreams that appear to contradict wish-fulfilment theory actually confirm it: their unpleasantness is the disguise itself.",
            "Significance": "The dream censor is one of Freud's most influential concepts, prefiguring the later structural model of id, ego, and superego. This chapter transforms a potential refutation of his theory into its strongest support, demonstrating Freud's remarkable dialectical skill."
        },
        "chapter-5-material-and-sources": {
            "About": "An encyclopedic exploration of where dreams get their raw material. Freud examines four major sources: recent experiences (especially 'indifferent' impressions from the day before), childhood memories (which surface in dreams with startling vividness), somatic stimuli (bodily sensations woven into dream imagery), and 'typical dreams' shared across individuals. The chapter includes extensive analyses of dreams about nakedness, the death of loved ones, examination anxiety, flying, and falling.",
            "Significance": "This is the book's most accessible and richly illustrated chapter. The catalogue of typical dreams has entered popular culture — the naked-in-public dream, the examination dream, the falling dream. Freud's claim that death-of-a-loved-one dreams reveal repressed childhood wishes remains his most controversial and psychologically provocative assertion."
        },
        "chapter-6-dream-work": {
            "About": "The longest and most technical chapter, describing the four mechanisms that transform latent dream-thoughts into manifest dream content. Condensation compresses multiple ideas into single images. Displacement shifts emotional intensity from significant to trivial elements. Considerations of representability translate abstract thoughts into visual scenes. Secondary elaboration imposes logical coherence on the assembled dream. Freud also provides an extensive discussion of dream symbolism, including sexual symbols.",
            "Significance": "The dream-work mechanisms are Freud's most enduring contribution to the understanding of unconscious mental processes. Condensation and displacement were later recognized as analogous to metaphor and metonymy in linguistics (Jakobson), influencing structuralism and literary theory far beyond psychology. This chapter is the operational manual of psychoanalytic interpretation."
        },
        "chapter-7-psychology-of-dream-activities": {
            "About": "Freud's most ambitious and speculative chapter, constructing a full model of the psychic apparatus to explain dream formation. He introduces the concepts of psychic regression (dreams moving backward from thought to perception), the distinction between primary process (unconscious, wish-driven) and secondary process (rational, reality-oriented), and the relationship between dreaming and neurosis. The chapter concludes with a meditation on the theoretical status of the unconscious.",
            "Significance": "This chapter contains Freud's first systematic account of the architecture of the mind — the 'topographic model' that would evolve into the id/ego/superego structural model. His concept of primary process thinking (governed by the pleasure principle, using condensation and displacement) versus secondary process (governed by the reality principle) remains foundational to psychoanalytic theory and has influenced cognitive science, neuroscience, and philosophy of mind."
        },
    }

    for item in items:
        if item["id"] in chapter_descriptions:
            item["sections"]["About"] = chapter_descriptions[item["id"]]["About"]
            item["sections"]["Significance"] = chapter_descriptions[item["id"]]["Significance"]

    # Add L2 group items
    for group in L2_GROUPS:
        item = {
            "id": group["id"],
            "name": group["name"],
            "sort_order": sort_order,
            "category": group["category"],
            "level": 2,
            "composite_of": group["composite_of"],
            "relationship_type": "emergence",
            "sections": {
                "About": group["about"],
                "How to Use": group["how_to_use"],
            },
            "keywords": group["keywords"],
            "metadata": {}
        }
        items.append(item)
        sort_order += 1
        print(f"  Created L2: {item['id']}")

    # Add L3 meta item
    l3_item = {
        "id": "complete-work",
        "name": "The Interpretation of Dreams — Complete Work",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": ["theory-of-dreams", "dream-work-chapters", "clinical-chapters"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Sigmund Freud's The Interpretation of Dreams (Die Traumdeutung, 1900) is the founding text of psychoanalysis and one of the most influential books of the twentieth century. Freud argues that dreams are not meaningless by-products of sleep but meaningful psychological acts — specifically, the disguised fulfilment of repressed wishes. Through meticulous analysis of his own dreams and those of his patients, he develops a systematic method of interpretation based on free association and introduces concepts that have become part of the common intellectual heritage: the unconscious, repression, the dream-work (condensation, displacement, symbolism), and the distinction between manifest and latent dream content. The book culminates in a speculative model of the psychic apparatus that prefigures Freud's later structural theory of id, ego, and superego.",
            "Legacy": "Published at the turn of the twentieth century (Freud insisted on the symbolic publication date of 1900, though it actually appeared in November 1899), The Interpretation of Dreams initially sold poorly — only 351 copies in its first six years. Yet it went on to reshape psychology, psychiatry, literary criticism, art, and popular culture. Its influence extends far beyond those who accept Freud's specific claims: the very idea that dreams have interpretable meaning, that the mind contains hidden layers, and that self-knowledge requires excavating the unconscious — these have become foundational assumptions of modern self-understanding. The book remains essential reading for anyone interested in the origins of psychoanalysis, the nature of consciousness, or the human capacity for self-deception and self-discovery.",
            "How to Use": "This grammar presents each chapter of The Interpretation of Dreams as a self-contained item, with the opening text and contextual commentary. The chapters are grouped thematically into Theory (the framework), Dream-Work (the mechanisms), and Clinical (the method and evidence). Readers new to Freud may wish to start with Chapter II (the Irma dream) or Chapter V (typical dreams) for the most vivid and accessible material, then work through the theoretical chapters. Chapter VII rewards careful study but is the most demanding.",
        },
        "keywords": ["psychoanalysis", "dream interpretation", "unconscious", "Freud", "wish fulfillment", "complete work"],
        "metadata": {}
    }
    items.append(l3_item)
    sort_order += 1
    print(f"  Created L3: {l3_item['id']}")

    # Build grammar
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Sigmund Freud",
                    "date": "1900",
                    "note": "Original author. First published as Die Traumdeutung (Leipzig and Vienna: Franz Deuticke, 1900)."
                },
                {
                    "name": "A. A. Brill",
                    "date": "1913",
                    "note": "Translator. Authorised English translation of the third edition (New York: The Macmillan Company, 1913)."
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2021",
                    "note": "Digital source. eBook #66048 (https://www.gutenberg.org/ebooks/66048)."
                }
            ]
        },
        "name": "The Interpretation of Dreams",
        "description": (
            "Sigmund Freud's foundational text of psychoanalysis (1900), in which he argues that dreams are the "
            "disguised fulfilment of repressed wishes and develops the method of free association for their interpretation. "
            "This grammar presents all seven chapters plus introductory material, covering the scientific literature on dreams, "
            "the dream of Irma's injection, wish-fulfilment theory, dream distortion, sources of dream material, "
            "the dream-work (condensation, displacement, symbolism, secondary elaboration), and the psychology of the "
            "dream activities. Translated by A. A. Brill (1913).\n\n"
            "Source: Project Gutenberg eBook #66048 (https://www.gutenberg.org/ebooks/66048)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: The original German editions featured no illustrations, but "
            "later editions and related works offer visual material. Consider Max Halberstadt's iconic 1921 photograph "
            "of Freud at his desk; the surrealist dream imagery of Salvador Dalí (who met Freud in 1938); "
            "and Art Nouveau book designs of the early Vienna Secession period (Koloman Moser, Gustav Klimt) "
            "which were contemporary with the book's first publication."
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["psychoanalysis", "freud", "dreams", "unconscious", "psychology", "wish-fulfillment"],
        "roots": ["western-philosophy", "psychology"],
        "shelves": ["mirror"],
        "lineages": ["Linehan"],
        "worldview": "rationalist",
        "items": items
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {len(items)} items to {OUTPUT_FILE}")
    print(f"  L1: {sum(1 for i in items if i['level'] == 1)}")
    print(f"  L2: {sum(1 for i in items if i['level'] == 2)}")
    print(f"  L3: {sum(1 for i in items if i['level'] == 3)}")


if __name__ == "__main__":
    main()
