#!/usr/bin/env python3
"""
Build grammar.json for The Varieties of Religious Experience by William James.

Source: Project Gutenberg eBook #621
Author: William James (1902)

Structure:
- L1: Preface + 14 lecture sections (some covering multiple numbered lectures) + Postscript
- L2: Thematic groupings (5 themes)
- L3: Meta-categories (The Complete Work)

Note: Some lectures are combined (e.g., "Lectures IV and V", "Lectures VI and VII").
We treat each heading as one L1 item.
"""

import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "varieties-religious-experience.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "varieties-religious-experience"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# The sections in order as they appear
SECTIONS = [
    {"id": "preface", "name": "Preface", "pattern": r"^PREFACE\.\s*$"},
    {"id": "lecture-1-religion-and-neurology", "name": "Lecture I: Religion and Neurology", "pattern": r"^LECTURE I\. RELIGION AND NEUROLOGY"},
    {"id": "lecture-2-circumscription-of-the-topic", "name": "Lecture II: Circumscription of the Topic", "pattern": r"^LECTURE II\. CIRCUMSCRIPTION OF THE TOPIC"},
    {"id": "lecture-3-the-reality-of-the-unseen", "name": "Lecture III: The Reality of the Unseen", "pattern": r"^LECTURE III\. THE REALITY OF THE UNSEEN"},
    {"id": "lectures-4-5-healthy-mindedness", "name": "Lectures IV-V: The Religion of Healthy-Mindedness", "pattern": r"^LECTURES IV AND V\. THE RELIGION OF HEALTHY"},
    {"id": "lectures-6-7-the-sick-soul", "name": "Lectures VI-VII: The Sick Soul", "pattern": r"^LECTURES VI AND VII\. THE SICK SOUL"},
    {"id": "lecture-8-the-divided-self", "name": "Lecture VIII: The Divided Self, and the Process of Its Unification", "pattern": r"^LECTURE VIII\. THE DIVIDED SELF"},
    {"id": "lecture-9-conversion", "name": "Lecture IX: Conversion", "pattern": r"^LECTURE IX\. CONVERSION\.\s*$"},
    {"id": "lecture-10-conversion-concluded", "name": "Lecture X: Conversion Concluded", "pattern": r"^LECTURE X\. CONVERSION"},
    {"id": "lectures-11-13-saintliness", "name": "Lectures XI-XIII: Saintliness", "pattern": r"^LECTURES XI, XII, AND XIII\. SAINTLINESS"},
    {"id": "lectures-14-15-value-of-saintliness", "name": "Lectures XIV-XV: The Value of Saintliness", "pattern": r"^LECTURES XIV AND XV\. THE VALUE OF SAINTLINESS"},
    {"id": "lectures-16-17-mysticism", "name": "Lectures XVI-XVII: Mysticism", "pattern": r"^LECTURES XVI AND XVII\. MYSTICISM"},
    {"id": "lecture-18-philosophy", "name": "Lecture XVIII: Philosophy", "pattern": r"^LECTURE XVIII\. PHILOSOPHY"},
    {"id": "lecture-19-other-characteristics", "name": "Lecture XIX: Other Characteristics", "pattern": r"^LECTURE XIX\. OTHER CHARACTERISTICS"},
    {"id": "lecture-20-conclusions", "name": "Lecture XX: Conclusions", "pattern": r"^LECTURE XX\. CONCLUSIONS"},
    {"id": "postscript", "name": "Postscript", "pattern": r"^POSTSCRIPT\.\s*$"},
]

SECTION_KEYWORDS = {
    "preface": ["Gifford-lectures", "psychology", "religion", "Edinburgh"],
    "lecture-1-religion-and-neurology": ["neurology", "psychology", "pathology", "George-Fox", "religious-genius"],
    "lecture-2-circumscription-of-the-topic": ["definition", "personal-religion", "institutional-religion", "feeling", "theology"],
    "lecture-3-the-reality-of-the-unseen": ["unseen", "abstract", "God", "presence", "belief", "conviction"],
    "lectures-4-5-healthy-mindedness": ["optimism", "happiness", "mind-cure", "healthy-mindedness", "once-born"],
    "lectures-6-7-the-sick-soul": ["melancholy", "evil", "pessimism", "sick-soul", "twice-born", "suffering"],
    "lecture-8-the-divided-self": ["divided-self", "unification", "counter-conversion", "discordant-personality"],
    "lecture-9-conversion": ["conversion", "transformation", "subconscious", "sudden-conversion", "gradual"],
    "lecture-10-conversion-concluded": ["conversion", "fruits", "sanctification", "automatisms", "subconscious"],
    "lectures-11-13-saintliness": ["saintliness", "asceticism", "charity", "purity", "devotion", "tenderness"],
    "lectures-14-15-value-of-saintliness": ["value", "fanaticism", "excess", "practical-fruits", "empirical-test"],
    "lectures-16-17-mysticism": ["mysticism", "ineffability", "noetic-quality", "transiency", "passivity", "union"],
    "lecture-18-philosophy": ["philosophy", "theology", "attributes", "idealism", "pragmatism"],
    "lecture-19-other-characteristics": ["aesthetic", "imagination", "prayer", "sacrifice", "confession"],
    "lecture-20-conclusions": ["conclusions", "subconscious", "over-beliefs", "pluralism", "pragmatism", "God"],
    "postscript": ["supernaturalism", "pluralism", "piecemeal", "universalistic", "philosophy"],
}


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        start_idx = text.index("\n", start_idx) + 1
    else:
        start_idx = 0
    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = len(text)
    return text[start_idx:end_idx]


def strip_front_matter(text):
    """Remove title page and contents before Preface."""
    match = re.search(r'^PREFACE\.\s*$', text, re.MULTILINE)
    if match:
        return text[match.start():]
    return text


def strip_back_matter(text):
    """Remove Index and Footnotes from end of text."""
    # Find INDEX section
    match = re.search(r'^INDEX\.\s*$', text, re.MULTILINE)
    if match:
        return text[:match.start()].strip()
    return text


def parse_sections(text):
    """Parse the book into its sections."""
    sections = []

    for i, section in enumerate(SECTIONS):
        match = re.search(section["pattern"], text, re.MULTILINE)
        if not match:
            print(f"WARNING: Could not find '{section['name']}'")
            continue

        # Start after the heading line
        heading_end = text.index('\n', match.start()) + 1
        start = heading_end

        # Find the next section or end of text
        if i + 1 < len(SECTIONS):
            next_match = re.search(SECTIONS[i + 1]["pattern"], text[start:], re.MULTILINE)
            if next_match:
                end = start + next_match.start()
            else:
                end = len(text)
        else:
            end = len(text)

        section_text = text[start:end].strip()
        # Clean up whitespace
        section_text = re.sub(r'\n{3,}', '\n\n', section_text)
        # Strip footnote reference numbers like (123)
        # Keep them — they're part of the text flow

        sections.append({
            'id': section['id'],
            'name': section['name'],
            'text': section_text,
            'num': i,
        })

    return sections


# Thematic groupings for L2
THEMES = [
    {
        "id": "theme-foundations-method",
        "name": "Foundations and Method",
        "sections": ["preface", "lecture-1-religion-and-neurology", "lecture-2-circumscription-of-the-topic", "lecture-3-the-reality-of-the-unseen"],
        "about": "James establishes his method: the psychological study of religion through its most intense individual expressions. He distinguishes the existential question (what is religion's nature and origin?) from the spiritual question (what is its value?). He defends studying 'religious geniuses' — often psychologically extreme personalities — against the charge that their experiences are 'merely' pathological. Religion is defined as 'the feelings, acts, and experiences of individual men in their solitude, so far as they apprehend themselves to stand in relation to whatever they may consider the divine.'",
        "for_readers": "Lecture I is essential — James's defense of studying extreme religious experience against medical materialism is still the best argument of its kind. His portrait of George Fox (the Quaker founder as psychopath and genius simultaneously) sets the tone. Lecture II defines what James means by religion — personal, not institutional. Lecture III on the 'reality of the unseen' shows how abstract objects can be as psychologically real as sensory ones.",
    },
    {
        "id": "theme-healthy-and-sick",
        "name": "The Healthy and the Sick Soul",
        "sections": ["lectures-4-5-healthy-mindedness", "lectures-6-7-the-sick-soul", "lecture-8-the-divided-self"],
        "about": "James's great typology of religious temperaments. The 'healthy-minded' or 'once-born' see the world as fundamentally good — they need only to open themselves to its goodness (Walt Whitman, the mind-cure movement). The 'sick soul' or 'twice-born' have experienced the reality of evil and suffering so deeply that simple optimism is impossible — they need a second birth, a conversion (Tolstoy, Bunyan, the authors of Ecclesiastes and Job). The 'divided self' struggles between these poles, seeking unification.",
        "for_readers": "This is the emotional heart of the book. Lectures IV-V on healthy-mindedness are surprisingly sympathetic to what James calls 'the religion of healthy-mindedness' — including the mind-cure movement of his day. Lectures VI-VII on the sick soul are devastating — James's accounts of melancholy and the 'fear of the universe' include his own thinly disguised experience of suicidal depression. Lecture VIII on the divided self bridges to the conversion lectures.",
    },
    {
        "id": "theme-conversion-transformation",
        "name": "Conversion and Transformation",
        "sections": ["lecture-9-conversion", "lecture-10-conversion-concluded"],
        "about": "James's analysis of religious conversion as a psychological process. Drawing on extensive case studies, he distinguishes gradual conversion (a slow recentering of the personality) from sudden conversion (a dramatic breakthrough, often involving the subconscious). He introduces the concept of the 'subliminal self' — the vast region of consciousness below the threshold of awareness — as the mechanism through which conversion operates. The subconscious is the gateway between the individual and whatever 'higher powers' may exist.",
        "for_readers": "These lectures are James at his most original — combining rigorous psychology with genuine openness to the possibility of transcendent influence. His theory of the subconscious as the meeting point between the human and the divine is one of the book's most enduring contributions. The case studies are vivid and often moving. Read alongside modern research on sudden personality change and 'quantum change' experiences.",
    },
    {
        "id": "theme-saintliness-mysticism",
        "name": "Saintliness and Mysticism",
        "sections": ["lectures-11-13-saintliness", "lectures-14-15-value-of-saintliness", "lectures-16-17-mysticism"],
        "about": "The fruits of religious experience: saintliness (the practical life of the transformed person) and mysticism (the direct experience of union with the divine). James catalogs the characteristics of saintliness — asceticism, strength of soul, purity, charity — and then subjects them to pragmatic evaluation: do they produce good results? His account of mysticism identifies four marks: ineffability, noetic quality, transiency, and passivity. Mystical states, he argues, are authoritative for those who have them but cannot compel belief in others.",
        "for_readers": "The saintliness lectures are a remarkable exercise in empirical ethics — James tests religious virtue by its practical fruits, sometimes finding excess (fanaticism, ascetic self-torture) alongside genuine goodness. The mysticism lectures contain his famous four marks of mystical experience and a tour through mystical traditions from Sufism to Vedanta. His conclusion — that mystical states 'break down the authority of the non-mystical or rationalistic consciousness' — remains provocative.",
    },
    {
        "id": "theme-philosophy-conclusions",
        "name": "Philosophy and Conclusions",
        "sections": ["lecture-18-philosophy", "lecture-19-other-characteristics", "lecture-20-conclusions", "postscript"],
        "about": "James's philosophical summing-up. He critiques systematic theology and rationalistic proofs of God as lifeless abstractions that add nothing to the concrete religious experience they claim to ground. His own conclusion is frankly pragmatic: the subconscious self is the mediating term between the individual and 'a wider self through which saving experiences come.' He stops short of specifying what this wider self is — it may be God, it may be something else — but insists that it is real because its effects are real. The Postscript clarifies his 'piecemeal supernaturalism' and pluralistic worldview.",
        "for_readers": "Lecture XVIII is a devastating critique of natural theology — James dismantles the traditional proofs of God with surgical precision. Lecture XX is the payoff: James's own 'over-beliefs' and his famous conclusion that 'the unseen order' is real because it produces real effects in human lives. The Postscript is essential — it places James's position on the philosophical map and introduces his pluralistic hypothesis. These lectures connect directly to Pragmatism (1907).",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = strip_front_matter(text)
    text = strip_back_matter(text)

    sections = parse_sections(text)
    print(f"Parsed {len(sections)} sections")

    items = []
    sort_order = 0

    # L1: Individual sections
    for sec in sections:
        sort_order += 1
        keywords = SECTION_KEYWORDS.get(sec['id'], ["religion", "psychology", "experience"])

        items.append({
            "id": sec['id'],
            "name": sec['name'],
            "sort_order": sort_order,
            "level": 1,
            "category": "lecture",
            "sections": {
                "Text": sec['text'],
            },
            "keywords": keywords,
            "metadata": {
                "section_number": sec['num'],
            }
        })
        print(f"  {sec['name']} ({len(sec['text'])} chars)")

    # L2: Thematic groupings
    all_theme_ids = []
    for theme in THEMES:
        sort_order += 1
        theme_id = theme["id"]
        all_theme_ids.append(theme_id)

        items.append({
            "id": theme_id,
            "name": theme["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": theme["sections"],
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "section_count": len(theme["sections"]),
            }
        })

    # L3: Meta-category
    sort_order += 1
    items.append({
        "id": "varieties-complete",
        "name": "The Varieties of Religious Experience: A Study in Human Nature",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "William James's The Varieties of Religious Experience (1902) is the founding text of the psychology of religion and one of the most influential books of the twentieth century. Based on the Gifford Lectures delivered at Edinburgh in 1901-1902, it takes a radical empirical approach to religious experience: instead of arguing for or against religion's truth, James collects and examines the most intense first-person accounts of religious states — conversion, mysticism, saintliness, the 'sick soul,' the 'divided self.' His method is descriptive and pragmatic: what are these experiences like? What effects do they produce? The book develops a typology (healthy-minded vs. sick souls, once-born vs. twice-born), a psychology (the subliminal self as gateway to the transcendent), and a philosophy (pragmatic pluralism). James concludes that religious experience points to a 'wider self' beyond ordinary consciousness, though he refuses to specify its ultimate nature. The book remains astonishingly fresh — its case studies are vivid, its analysis subtle, and its conclusions open-ended in a way that neither believers nor skeptics find entirely comfortable.",
            "For Readers": "The Varieties rewards both sequential and selective reading. For the full arc, read straight through — James builds his case carefully across twenty lectures. For highlights: start with Lectures I-II (method and definition), then Lectures VI-VII (the sick soul — James's most powerful writing), then Lectures XVI-XVII (mysticism), and finally Lecture XX (conclusions). James writes with warmth, wit, and extraordinary psychological acuity. He is that rarest of things: a rigorous thinker who takes subjective experience seriously without sentimentality.",
        },
        "keywords": ["religion", "psychology", "mysticism", "conversion", "James", "Gifford-lectures", "pragmatism", "consciousness"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "William James",
                    "date": "1902",
                    "note": "Author"
                }
            ]
        },
        "name": "The Varieties of Religious Experience",
        "description": "William James's The Varieties of Religious Experience: A Study in Human Nature (1902) — the founding text of the psychology of religion. Twenty Gifford Lectures delivered at Edinburgh, taking a radical empirical approach to religious experience: conversion, mysticism, saintliness, the sick soul, healthy-mindedness. James collects vivid first-person accounts of religious states and subjects them to psychological analysis and pragmatic evaluation, concluding that they point to a 'wider self' beyond ordinary consciousness.\n\nSource: Project Gutenberg eBook #621 (https://www.gutenberg.org/ebooks/621)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs of William James (various, 1890s-1900s). Images of the University of Edinburgh and McEwan Hall where the Gifford Lectures were delivered. Portraits of figures discussed: George Fox, John Bunyan, Teresa of Avila, Tolstoy.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["religion", "psychology", "mysticism", "conversion", "consciousness", "pragmatism", "public-domain", "full-text"],
        "roots": ["process-philosophy"],
        "shelves": ["mirror"],
        "lineages": ["Linehan", "Shrei"],
        "worldview": "dialectical",
        "items": items,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1: {l1} lectures, L2: {l2} themes, L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
