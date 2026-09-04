#!/usr/bin/env python3
"""
Parser for three esoteric/alchemy seed texts:
1. The Kybalion (Gutenberg #14209)
2. Alchemy: Ancient and Modern by H. Stanley Redgrove (Gutenberg #43240)
3. Of Natural and Supernatural Things by Basilius Valentinus (Gutenberg #26340)

Outputs grammar.json for each into grammars/<name>/
"""

import json
import re
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_body(text):
    """Extract body between Gutenberg START/END markers."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    if start_idx == -1 or end_idx == -1:
        raise ValueError("Could not find Gutenberg markers")
    start_idx = text.index("\n", start_idx) + 1
    return text[start_idx:end_idx].strip()


def truncate_text(text, max_chars=2800):
    """Truncate text at ~2800 chars, at last period."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    bp = text.rfind(".", 0, max_chars)
    if bp == -1:
        bp = max_chars
    remaining_words = len(text[bp+1:].split())
    return text[:bp+1] + f" [Text continues for approximately {remaining_words} more words...]"


def clean_text(text):
    """Clean up formatting artifacts."""
    # Remove illustration markers
    text = re.sub(r'\[Illustration:.*?\]', '', text, flags=re.DOTALL)
    # Remove footnote markers like [41]
    text = re.sub(r'\[\d+\]', '', text)
    # Remove transcriber notes
    text = re.sub(r"\[Transcriber'?s note:.*?\]", '', text, flags=re.DOTALL)
    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def make_grammar_commons(attribution):
    return {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": attribution
    }


def make_item(id_, name, sort_order, category, level, sections, keywords, composite_of=None, metadata=None):
    item = {
        "id": id_,
        "name": name,
        "sort_order": sort_order,
        "category": category,
        "level": level,
        "sections": sections,
        "keywords": keywords
    }
    if composite_of:
        item["composite_of"] = composite_of
        item["relationship_type"] = "emergence"
    if metadata:
        item["metadata"] = metadata
    return item


# ============================================================
# KYBALION PARSER
# ============================================================

def parse_kybalion():
    seed_path = os.path.join(REPO, "seeds", "kybalion.txt")
    with open(seed_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    body = extract_body(raw)

    # Chapter definitions: (heading_pattern, id, name, category)
    chapters = [
        ("INTRODUCTION", "introduction", "Introduction", "introduction"),
        ("CHAPTER I", "chapter-1", "The Hermetic Philosophy", "hermetic-philosophy"),
        ("CHAPTER II", "chapter-2", "The Seven Hermetic Principles", "seven-principles"),
        ("CHAPTER III", "chapter-3", "Mental Transmutation", "mental-transmutation"),
        ("CHAPTER IV", "chapter-4", "The All", "the-all"),
        ("CHAPTER V", "chapter-5", "The Mental Universe", "the-all"),
        ("CHAPTER VI", "chapter-6", "The Divine Paradox", "the-all"),
        ("CHAPTER VII", "chapter-7", "\"The All\" in All", "the-all"),
        ("CHAPTER VIII", "chapter-8", "Planes of Correspondence", "correspondence"),
        ("CHAPTER IX", "chapter-9", "Vibration", "vibration"),
        ("CHAPTER X", "chapter-10", "Polarity", "polarity"),
        ("CHAPTER XI", "chapter-11", "Rhythm", "rhythm"),
        ("CHAPTER XII", "chapter-12", "Causation", "causation"),
        ("CHAPTER XIII", "chapter-13", "Gender", "gender"),
        ("CHAPTER XIV", "chapter-14", "Mental Gender", "gender"),
        ("CHAPTER XV", "chapter-15", "Hermetic Axioms", "axioms"),
    ]

    lines = body.split('\n')

    # Find line indices for each chapter heading
    chapter_starts = []
    for heading, id_, name, cat in chapters:
        for i, line in enumerate(lines):
            stripped = line.strip()
            if heading == "INTRODUCTION" and stripped == "INTRODUCTION":
                chapter_starts.append((i, id_, name, cat))
                break
            elif heading.startswith("CHAPTER") and stripped == heading:
                chapter_starts.append((i, id_, name, cat))
                break

    # Extract text for each chapter
    items = []
    sort_order = 1
    l1_ids = []

    for idx, (start_line, id_, name, cat) in enumerate(chapter_starts):
        if idx + 1 < len(chapter_starts):
            end_line = chapter_starts[idx + 1][0]
        else:
            end_line = len(lines)

        # Skip heading lines (chapter number + title)
        content_start = start_line
        # Skip blank lines and title lines after heading
        for j in range(start_line, min(start_line + 10, end_line)):
            stripped = lines[j].strip()
            if stripped and not stripped.startswith("CHAPTER") and stripped != "INTRODUCTION" and stripped == stripped.upper() and len(stripped) > 3:
                content_start = j + 1
                continue
            elif stripped.startswith("CHAPTER") or stripped == "INTRODUCTION":
                content_start = j + 1
                continue
            elif stripped == "":
                content_start = j + 1
                continue
            else:
                content_start = j
                break

        text = '\n'.join(lines[content_start:end_line])
        text = clean_text(text)
        text = truncate_text(text)

        keywords = ["hermeticism", "kybalion"]
        if "principle" in name.lower():
            keywords.append("seven-principles")
        if "mental" in name.lower():
            keywords.append("mentalism")

        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category=cat, level=1,
            sections={"Teaching": text},
            keywords=keywords
        ))
        l1_ids.append(id_)
        sort_order += 1

    # L2: Thematic groups
    l2_groups = [
        ("foundations", "Foundations of Hermetic Philosophy", "foundations",
         ["introduction", "chapter-1", "chapter-2"],
         "The opening chapters introduce the Hermetic tradition and its seven core principles.",
         ["hermeticism", "philosophy", "foundations"]),
        ("nature-of-the-all", "The Nature of The All", "the-all",
         ["chapter-3", "chapter-4", "chapter-5", "chapter-6", "chapter-7"],
         "These chapters explore the nature of The All — the Universal Mind — and the paradoxes of existence within it.",
         ["the-all", "mentalism", "paradox"]),
        ("seven-principles-applied", "The Seven Principles Applied", "principles-applied",
         ["chapter-8", "chapter-9", "chapter-10", "chapter-11", "chapter-12", "chapter-13", "chapter-14"],
         "Each principle is explored in depth: Correspondence, Vibration, Polarity, Rhythm, Causation, and Gender.",
         ["principles", "application", "practice"]),
        ("synthesis", "Hermetic Synthesis", "synthesis",
         ["chapter-15"],
         "The final chapter distills the teachings into practical axioms for the Hermetic student.",
         ["axioms", "synthesis", "practice"]),
    ]

    for id_, name, cat, refs, about, kw in l2_groups:
        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category=cat, level=2,
            sections={
                "About": about,
                "For Readers": "Read these chapters together to understand how the Hermetic principles interrelate and build upon each other."
            },
            keywords=kw,
            composite_of=refs
        ))
        sort_order += 1

    # L3: Meta
    items.append(make_item(
        id_="hermetic-teaching", name="The Hermetic Teaching", sort_order=sort_order,
        category="meta", level=3,
        sections={
            "About": "The Kybalion presents a complete system of Hermetic philosophy through seven principles: Mentalism, Correspondence, Vibration, Polarity, Rhythm, Cause and Effect, and Gender. These principles describe the fundamental laws governing the universe from the perspective of the ancient Hermetic tradition attributed to Hermes Trismegistus.",
            "How to Use": "Begin with the Foundations to understand the tradition, then explore The All to grasp the metaphysical framework, then study each principle individually, and finally integrate them through the Hermetic Axioms."
        },
        keywords=["hermeticism", "hermetic-philosophy", "seven-principles", "meta"],
        composite_of=["foundations", "nature-of-the-all", "seven-principles-applied", "synthesis"]
    ))

    grammar = {
        "_grammar_commons": make_grammar_commons([
            {"name": "Three Initiates", "date": "1912", "note": "Original authors"},
            {"name": "Project Gutenberg", "date": "2004", "note": "eBook #14209"}
        ]),
        "name": "The Kybalion",
        "description": "The Kybalion by Three Initiates (1912) — a study of Hermetic philosophy covering the seven Hermetic principles: Mentalism, Correspondence, Vibration, Polarity, Rhythm, Cause and Effect, and Gender. Originally published by The Yogi Publication Society.\n\nSource: Project Gutenberg eBook #14209 (https://www.gutenberg.org/ebooks/14209)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Hermetic and alchemical emblems from works such as the Mutus Liber (1677), Atalanta Fugiens by Michael Maier (1618), and the Rosarium Philosophorum (16th century) — rich symbolic imagery associated with the Hermetic tradition.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["hermeticism", "alchemy", "philosophy", "esoteric", "seven-principles"],
        "roots": ["mysticism", "western-esotericism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }

    out_dir = os.path.join(REPO, "grammars", "kybalion")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "grammar.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"Kybalion: {len(items)} items written to {out_path}")
    return grammar


# ============================================================
# ALCHEMY: ANCIENT AND MODERN PARSER
# ============================================================

def parse_alchemy():
    seed_path = os.path.join(REPO, "seeds", "alchemy-ancient-modern.txt")
    with open(seed_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    body = extract_body(raw)
    lines = body.split('\n')

    # Find body chapters (skip TOC chapters)
    # TOC chapters appear around lines 346-456 of original file
    # Body chapters start with "CHAPTER I" after all the front matter
    chapters = [
        ("CHAPTER I", "chapter-1", "The Meaning of Alchemy", "meaning"),
        ("CHAPTER II", "chapter-2", "The Theory of Physical Alchemy", "theory"),
        ("CHAPTER III", "chapter-3", "The Alchemists: Before Paracelsus", "alchemists"),
        ("CHAPTER IV", "chapter-4", "The Alchemists: Paracelsus and After", "alchemists"),
        ("CHAPTER V", "chapter-5", "The Outcome of Alchemy", "outcome"),
        ("CHAPTER VI", "chapter-6", "The Age of Modern Chemistry", "modern-chemistry"),
        ("CHAPTER VII", "chapter-7", "Modern Alchemy", "modern-alchemy"),
    ]

    # Also need to find PREFACE sections
    preface_sections = []

    # Find chapter line positions - skip TOC, find body chapters
    chapter_starts = []
    found_body = False
    toc_end = 0

    # Find the end of the TOC / front matter area
    # The TOC in alchemy text has indented chapter entries
    # Body chapters are flush left "CHAPTER I" after the front matter
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Look for PREFACE sections first
        if stripped == "PREFACE TO THE SECOND EDITION":
            preface_sections.append((i, "preface-2nd", "Preface to the Second Edition"))
        elif stripped == "PREFACE TO THE FIRST EDITION":
            preface_sections.append((i, "preface-1st", "Preface to the First Edition"))

    # Find body chapters - they appear without leading spaces
    for heading, id_, name, cat in chapters:
        found = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == heading and not line.startswith(' ') and not line.startswith('\t'):
                # Check it's not in a TOC context (TOC has indented entries)
                # Accept the LAST occurrence of each chapter heading (body, not TOC)
                chapter_starts.append((i, id_, name, cat))
                found = True
        if found and len(chapter_starts) > 0:
            # Keep only the last match for this chapter (body, not TOC)
            matches = [(i, id2, name2, cat2) for i, id2, name2, cat2 in chapter_starts if id2 == id_]
            if len(matches) > 1:
                # Remove earlier matches
                chapter_starts = [x for x in chapter_starts if x[1] != id_]
                chapter_starts.append(matches[-1])

    # Sort by line number
    chapter_starts.sort(key=lambda x: x[0])

    items = []
    sort_order = 1

    # Add preface items
    for pref_idx, (start_line, id_, name) in enumerate(preface_sections):
        if pref_idx + 1 < len(preface_sections):
            end_line = preface_sections[pref_idx + 1][0]
        elif chapter_starts:
            end_line = chapter_starts[0][0]
        else:
            end_line = start_line + 200

        content_start = start_line + 2  # skip heading + blank
        text = '\n'.join(lines[content_start:end_line])
        text = clean_text(text)
        text = truncate_text(text)

        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category="preface", level=1,
            sections={"Text": text},
            keywords=["alchemy", "preface"]
        ))
        sort_order += 1

    # Add chapter items
    l1_ids = [item["id"] for item in items]
    for idx, (start_line, id_, name, cat) in enumerate(chapter_starts):
        if idx + 1 < len(chapter_starts):
            end_line = chapter_starts[idx + 1][0]
        else:
            end_line = len(lines)

        # Skip heading lines
        content_start = start_line
        for j in range(start_line, min(start_line + 15, end_line)):
            stripped = lines[j].strip()
            if not stripped or stripped.startswith("CHAPTER") or (stripped == stripped.upper() and len(stripped) > 3 and "THE" in stripped):
                content_start = j + 1
            elif stripped.startswith("(") and stripped.endswith(")"):
                content_start = j + 1
            else:
                break

        text = '\n'.join(lines[content_start:end_line])
        text = clean_text(text)
        text = truncate_text(text)

        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category=cat, level=1,
            sections={"Text": text},
            keywords=["alchemy", cat]
        ))
        l1_ids.append(id_)
        sort_order += 1

    # L2: Thematic groups
    l2_groups = [
        ("foundations-of-alchemy", "Foundations of Alchemy", "foundations",
         ["preface-2nd", "chapter-1", "chapter-2"],
         "The conceptual foundations of alchemy: what it meant, what it aimed to achieve, and the theoretical basis for transmutation.",
         ["alchemy", "theory", "foundations"]),
        ("the-great-alchemists", "The Great Alchemists", "alchemists",
         ["chapter-3", "chapter-4"],
         "Biographical and intellectual portraits of the great alchemists, from the early practitioners through Paracelsus and beyond.",
         ["alchemists", "biography", "history"]),
        ("alchemy-to-chemistry", "From Alchemy to Chemistry", "transition",
         ["chapter-5", "chapter-6", "chapter-7"],
         "The transformation of alchemy into modern chemistry, and the surprising return of transmutation in modern physics.",
         ["chemistry", "transmutation", "modern-science"]),
    ]

    for id_, name, cat, refs, about, kw in l2_groups:
        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category=cat, level=2,
            sections={
                "About": about,
                "For Readers": "These chapters work as a unit to build understanding of the alchemical tradition from theory through practice to modern legacy."
            },
            keywords=kw,
            composite_of=refs
        ))
        sort_order += 1

    # L3: Meta
    items.append(make_item(
        id_="alchemy-complete", name="Alchemy: Ancient and Modern — Complete", sort_order=sort_order,
        category="meta", level=3,
        sections={
            "About": "H. Stanley Redgrove's comprehensive study traces alchemy from its philosophical and mystical origins through the lives of the great alchemists to its surprising connections with modern atomic physics. The book reveals alchemy as far more than failed chemistry — it was a complete worldview uniting matter, spirit, and transformation.",
            "How to Use": "Start with the Foundations to understand what alchemy really meant, then explore the lives of the Alchemists, and finally trace the surprising thread from ancient transmutation to modern nuclear physics."
        },
        keywords=["alchemy", "history", "transmutation", "meta"],
        composite_of=["foundations-of-alchemy", "the-great-alchemists", "alchemy-to-chemistry"]
    ))

    grammar = {
        "_grammar_commons": make_grammar_commons([
            {"name": "H. Stanley Redgrove", "date": "1922", "note": "Author, Second Edition"},
            {"name": "Project Gutenberg", "date": "2013", "note": "eBook #43240"}
        ]),
        "name": "Alchemy: Ancient and Modern",
        "description": "Alchemy: Ancient and Modern by H. Stanley Redgrove (1922, 2nd edition) — a comprehensive study of alchemistic doctrines, their relations to mysticism and modern physical science, with biographical accounts of noted alchemists.\n\nSource: Project Gutenberg eBook #43240 (https://www.gutenberg.org/ebooks/43240)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: The original book includes 16 full-page illustrations including a portrait of Paracelsus. Additional relevant imagery: alchemical emblems from Michael Maier's Atalanta Fugiens (1618), illustrations from the Splendor Solis (1582), and woodcuts from Basil Valentine's works.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["alchemy", "chemistry", "history-of-science", "esoteric", "transmutation"],
        "roots": ["mysticism", "western-esotericism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }

    out_dir = os.path.join(REPO, "grammars", "alchemy-ancient-modern")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "grammar.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"Alchemy: {len(items)} items written to {out_path}")
    return grammar


# ============================================================
# OF NATURAL AND SUPERNATURAL THINGS PARSER
# ============================================================

def parse_natural_supernatural():
    seed_path = os.path.join(REPO, "seeds", "natural-supernatural-things.txt")
    with open(seed_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    body = extract_body(raw)
    lines = body.split('\n')

    # Section definitions for the main Basilius Valentinus text
    bv_chapters = [
        ("CHAP. I.", "bv-chapter-1", "Of Natural and Supernatural Things", "natural-supernatural"),
        ("CHAP. II.", "bv-chapter-2", "Of the First Tincture and Roots of Metals", "tinctures"),
        ("CHAP. III.", "bv-chapter-3", "Of the Spirit of Mercury", "metals"),
        ("CHAP. IV.", "bv-chapter-4", "Of the Spirit of Copper", "metals"),
        ("CHAP. V.", "bv-chapter-5", "Of the Spirit and Tincture of Mars", "metals"),
        ("CHAP. VI.", "bv-chapter-6", "Of the Spirit of Gold", "metals"),
        ("CHAP. VII.", "bv-chapter-7", "Of the Spirit of Silver", "metals"),
        ("CHAP. VIII.", "bv-chapter-8", "Of the Soul or Tincture of Tin", "metals"),
        ("CHAP. IX.", "bv-chapter-9", "Of the Spirit of Saturn, or Tincture of Lead", "metals"),
    ]

    # Find chapter line positions
    chapter_starts = []
    for heading, id_, name, cat in bv_chapters:
        for i, line in enumerate(lines):
            if line.strip() == heading:
                chapter_starts.append((i, id_, name, cat))
                break

    # Find the Roger Bacon section
    bacon_start = None
    holland_start = None
    for i, line in enumerate(lines):
        if "_Of the Medicine or Tincture of_ Antimony" in line:
            bacon_start = i
        if "_A Work of_ Saturn, _of Mr._ John Isaac Holland" in line:
            holland_start = i

    items = []
    sort_order = 1

    # Process Basilius Valentinus chapters
    for idx, (start_line, id_, name, cat) in enumerate(chapter_starts):
        if idx + 1 < len(chapter_starts):
            end_line = chapter_starts[idx + 1][0]
        elif bacon_start:
            end_line = bacon_start
        else:
            end_line = len(lines)

        # Skip heading and subtitle lines
        content_start = start_line + 1
        for j in range(start_line + 1, min(start_line + 10, end_line)):
            stripped = lines[j].strip()
            if not stripped or stripped.startswith("_Of ") or stripped.startswith("_of "):
                content_start = j + 1
            else:
                break

        text = '\n'.join(lines[content_start:end_line])
        text = clean_text(text)
        text = truncate_text(text)

        kw = ["basilius-valentinus", "alchemy"]
        if cat == "metals":
            metal = name.split("of ")[-1] if "of " in name else ""
            if metal:
                kw.append(metal.lower().replace(",", "").strip())

        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category=cat, level=1,
            sections={"Text": text},
            keywords=kw
        ))
        sort_order += 1

    # Roger Bacon section
    if bacon_start:
        end_line = holland_start if holland_start else len(lines)
        text = '\n'.join(lines[bacon_start:end_line])
        text = clean_text(text)
        text = truncate_text(text)

        items.append(make_item(
            id_="roger-bacon-antimony", name="Of the Medicine or Tincture of Antimony (Roger Bacon)",
            sort_order=sort_order,
            category="supplementary", level=1,
            sections={"Text": text},
            keywords=["roger-bacon", "antimony", "alchemy", "tincture"]
        ))
        sort_order += 1

    # Holland section
    if holland_start:
        text = '\n'.join(lines[holland_start:])
        text = clean_text(text)
        text = truncate_text(text)

        items.append(make_item(
            id_="holland-saturn", name="A Work of Saturn (John Isaac Holland)",
            sort_order=sort_order,
            category="supplementary", level=1,
            sections={"Text": text},
            keywords=["john-isaac-holland", "saturn", "lead", "alchemy"]
        ))
        sort_order += 1

    # L2: Thematic groups
    l2_groups = [
        ("foundations-natural", "Foundations: Natural and Supernatural", "foundations",
         ["bv-chapter-1", "bv-chapter-2"],
         "The opening chapters establish the metaphysical framework — the distinction between natural and supernatural — and introduce the first tincture and roots from which all metals grow.",
         ["foundations", "tincture", "metaphysics"]),
        ("planetary-metals", "The Planetary Metals", "planetary-metals",
         ["bv-chapter-3", "bv-chapter-4", "bv-chapter-5", "bv-chapter-6", "bv-chapter-7", "bv-chapter-8", "bv-chapter-9"],
         "Each metal is governed by a planetary spirit: Mercury, Venus (Copper), Mars (Iron), Sol (Gold), Luna (Silver), Jupiter (Tin), and Saturn (Lead). Basilius reveals the tincture and spirit of each.",
         ["metals", "planets", "tinctures", "spirits"]),
        ("supplementary-works", "Supplementary Alchemical Works", "supplementary",
         ["roger-bacon-antimony", "holland-saturn"],
         "Two additional alchemical treatises appended to the main work: Roger Bacon on the Medicine of Antimony, and John Isaac Holland's Work of Saturn.",
         ["roger-bacon", "holland", "antimony", "saturn"]),
    ]

    for id_, name, cat, refs, about, kw in l2_groups:
        items.append(make_item(
            id_=id_, name=name, sort_order=sort_order,
            category=cat, level=2,
            sections={
                "About": about,
                "For Readers": "These chapters reveal the alchemical worldview where metals are living beings animated by planetary spirits, each carrying a unique tincture toward perfection."
            },
            keywords=kw,
            composite_of=refs
        ))
        sort_order += 1

    # L3: Meta
    items.append(make_item(
        id_="natural-supernatural-complete", name="Of Natural and Supernatural Things — Complete",
        sort_order=sort_order,
        category="meta", level=3,
        sections={
            "About": "Basilius Valentinus's treatise on the spiritual essences of metals, with supplementary works by Roger Bacon and John Isaac Holland. The text reveals the alchemical understanding of matter as animated by planetary spirits, each metal carrying a tincture that can be awakened through the art of transmutation.",
            "How to Use": "Begin with the Foundations to understand the natural/supernatural framework, then explore each Planetary Metal to see how the seven classical metals correspond to the seven planets. The Supplementary Works offer practical applications of these principles."
        },
        keywords=["basilius-valentinus", "alchemy", "metals", "transmutation", "meta"],
        composite_of=["foundations-natural", "planetary-metals", "supplementary-works"]
    ))

    grammar = {
        "_grammar_commons": make_grammar_commons([
            {"name": "Basilius Valentinus", "date": "c. 15th century", "note": "Attributed author, Benedictine monk"},
            {"name": "Daniel Cable", "date": "1671", "note": "Translator from High Dutch"},
            {"name": "Project Gutenberg", "date": "2008", "note": "eBook #26340"}
        ]),
        "name": "Of Natural and Supernatural Things",
        "description": "Of Natural and Supernatural Things by Basilius Valentinus (c. 15th century), translated by Daniel Cable (1671) — a treatise on the first tincture, root, and spirit of metals and minerals, with supplementary works by Roger Bacon on Antimony and John Isaac Holland on Saturn.\n\nSource: Project Gutenberg eBook #26340 (https://www.gutenberg.org/ebooks/26340)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Woodcuts and engravings from Basil Valentine's Twelve Keys (Musaeum Hermeticum, 1678), the alchemical illustrations of the Splendor Solis (c. 1582), and planetary metal symbols from Athanasius Kircher's works.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["alchemy", "esoteric", "basilius-valentinus", "transmutation"],
        "roots": ["mysticism", "western-esotericism"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "animist",
        "items": items
    }

    out_dir = os.path.join(REPO, "grammars", "natural-supernatural-things")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "grammar.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"Natural/Supernatural: {len(items)} items written to {out_path}")
    return grammar


if __name__ == "__main__":
    print("Parsing esoteric/alchemy seed texts...")
    print()
    parse_kybalion()
    print()
    parse_alchemy()
    print()
    parse_natural_supernatural()
    print()
    print("Done!")
