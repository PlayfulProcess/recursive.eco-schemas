#!/usr/bin/env python3
"""
Transform Shakespeare Complete Works (Gutenberg) into recursive.eco grammar JSON.

Shakespeare's works are split into individual items, one per play/poem/sonnet-collection.
Each work becomes an item with the full text in sections.

Works are categorized as: comedy, tragedy, history, romance, poetry
"""

import json
import re
import os

SOURCES_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(SOURCES_DIR), "schemas", "other", "religious-texts")

# Hardcoded work boundaries (line numbers, 1-indexed) from the Gutenberg file.
# Extracted by manual inspection of the source file.
# Format: (start_line, title, short_name, category)
WORKS = [
    (85, "THE SONNETS", "The Sonnets", "poetry"),
    (2862, "ALL\u2019S WELL THAT ENDS WELL", "All's Well That Ends Well", "comedy"),
    (7826, "THE TRAGEDY OF ANTONY AND CLEOPATRA", "Antony and Cleopatra", "tragedy"),
    (14467, "AS YOU LIKE IT", "As You Like It", "comedy"),
    (18905, "THE COMEDY OF ERRORS", "The Comedy of Errors", "comedy"),
    (22106, "THE TRAGEDY OF CORIOLANUS", "Coriolanus", "tragedy"),
    (28551, "CYMBELINE", "Cymbeline", "romance"),
    (34436, "THE TRAGEDY OF HAMLET, PRINCE OF DENMARK", "Hamlet", "tragedy"),
    (41134, "THE FIRST PART OF KING HENRY THE FOURTH", "Henry IV Part 1", "history"),
    (45941, "THE SECOND PART OF KING HENRY THE FOURTH", "Henry IV Part 2", "history"),
    (51137, "THE LIFE OF KING HENRY THE FIFTH", "Henry V", "history"),
    (56083, "THE FIRST PART OF HENRY THE SIXTH", "Henry VI Part 1", "history"),
    (60713, "THE SECOND PART OF KING HENRY THE SIXTH", "Henry VI Part 2", "history"),
    (65895, "THE THIRD PART OF KING HENRY THE SIXTH", "Henry VI Part 3", "history"),
    (71017, "KING HENRY THE EIGHTH", "Henry VIII", "history"),
    (76156, "THE LIFE AND DEATH OF KING JOHN", "King John", "history"),
    (80256, "THE TRAGEDY OF JULIUS CAESAR", "Julius Caesar", "tragedy"),
    (84903, "THE TRAGEDY OF KING LEAR", "King Lear", "tragedy"),
    (91012, "LOVE\u2019S LABOUR\u2019S LOST", "Love's Labour's Lost", "comedy"),
    (96020, "THE TRAGEDY OF MACBETH", "Macbeth", "tragedy"),
    (100170, "MEASURE FOR MEASURE", "Measure for Measure", "comedy"),
    (105054, "THE MERCHANT OF VENICE", "The Merchant of Venice", "comedy"),
    (109225, "THE MERRY WIVES OF WINDSOR", "The Merry Wives of Windsor", "comedy"),
    (114048, "A MIDSUMMER NIGHT\u2019S DREAM", "A Midsummer Night's Dream", "comedy"),
    (117533, "MUCH ADO ABOUT NOTHING", "Much Ado About Nothing", "comedy"),
    (122133, "THE TRAGEDY OF OTHELLO, THE MOOR OF VENICE", "Othello", "tragedy"),
    (128415, "PERICLES, PRINCE OF TYRE", "Pericles", "romance"),
    (132567, "KING RICHARD THE SECOND", "Richard II", "history"),
    (136895, "KING RICHARD THE THIRD", "Richard III", "history"),
    (143370, "THE TRAGEDY OF ROMEO AND JULIET", "Romeo and Juliet", "tragedy"),
    (148637, "THE TAMING OF THE SHREW", "The Taming of the Shrew", "comedy"),
    (153505, "THE TEMPEST", "The Tempest", "romance"),
    (157341, "THE LIFE OF TIMON OF ATHENS", "Timon of Athens", "tragedy"),
    (161762, "THE TRAGEDY OF TITUS ANDRONICUS", "Titus Andronicus", "tragedy"),
    (165887, "TROILUS AND CRESSIDA", "Troilus and Cressida", "tragedy"),
    (172091, "TWELFTH NIGHT; OR, WHAT YOU WILL", "Twelfth Night", "comedy"),
    (176587, "THE TWO GENTLEMEN OF VERONA", "The Two Gentlemen of Verona", "comedy"),
    (180838, "THE TWO NOBLE KINSMEN", "The Two Noble Kinsmen", "romance"),
    (186349, "THE WINTER\u2019S TALE", "The Winter's Tale", "romance"),
    (191364, "A LOVER\u2019S COMPLAINT", "A Lover's Complaint", "poetry"),
    (191747, "THE PASSIONATE PILGRIM", "The Passionate Pilgrim", "poetry"),
    (192329, "THE PHOENIX AND THE TURTLE", "The Phoenix and the Turtle", "poetry"),
    (192423, "THE RAPE OF LUCRECE", "The Rape of Lucrece", "poetry"),
    (194610, "VENUS AND ADONIS", "Venus and Adonis", "poetry"),
]


def slugify(text):
    text = text.lower()
    text = text.replace("\u2019", "")  # curly apostrophe
    text = text.replace("'", "")
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    return text.strip('-')


def get_questions(name, category):
    """Generate reflective questions based on work and category."""
    tragedy_qs = [
        "What fatal flaw do you recognize in yourself?",
        "Where is pride leading you astray?",
        "What truth are you refusing to see?"
    ]
    comedy_qs = [
        "What misunderstanding needs to be resolved in your life?",
        "Where could laughter heal what logic cannot?",
        "What disguise are you wearing, and what would happen if you removed it?"
    ]
    history_qs = [
        "What does power cost?",
        "How does the past shape your present choices?",
        "What legacy are you building?"
    ]
    romance_qs = [
        "What needs to be forgiven before healing can begin?",
        "What has been lost that might yet be restored?",
        "Where is the boundary between justice and mercy?"
    ]
    poetry_qs = [
        "What beauty deserves to be preserved?",
        "How does time shape what you love?",
        "What would you say to the one you cannot reach?"
    ]

    base = {
        "tragedy": tragedy_qs,
        "comedy": comedy_qs,
        "history": history_qs,
        "romance": romance_qs,
        "poetry": poetry_qs,
    }
    return base.get(category, ["What does this work reveal about your own story?"])


def get_symbol(category):
    symbols = {
        "tragedy": "🗡",
        "comedy": "🎭",
        "history": "👑",
        "romance": "🌊",
        "poetry": "🪶",
    }
    return symbols.get(category, "📜")


def transform_shakespeare():
    print("Transforming Shakespeare Complete Works...")

    path = os.path.join(SOURCES_DIR, "shakespeare")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)

    # Find end marker
    end_marker_line = total_lines
    for i in range(total_lines - 1, max(total_lines - 200, 0), -1):
        if "*** END OF THE PROJECT GUTENBERG" in lines[i]:
            end_marker_line = i
            break

    items = []
    for idx, (start_line, raw_title, short_name, category) in enumerate(WORKS):
        # Determine end of this work (start of next work, or end of file)
        if idx + 1 < len(WORKS):
            end_line = WORKS[idx + 1][0] - 1
        else:
            end_line = end_marker_line

        # Extract text (convert from 1-indexed to 0-indexed)
        work_text = "".join(lines[start_line - 1:end_line]).strip()

        # Remove any trailing blank lines
        work_text = work_text.rstrip()

        # Count lines and estimate word count
        work_lines = work_text.count('\n') + 1
        word_count = len(work_text.split())

        # Detect acts/scenes for plays
        acts = len(re.findall(r'^ACT [IVX]+', work_text, re.MULTILINE))
        scenes = len(re.findall(r'^(?:SCENE|Scene) [IVX]+', work_text, re.MULTILINE))

        sort_order = idx + 1

        item = {
            "id": f"shakespeare-{sort_order:02d}-{slugify(short_name)}",
            "name": short_name,
            "symbol": get_symbol(category),
            "category": category,
            "sections": {
                "Text": work_text
            },
            "keywords": _keywords(short_name, category),
            "questions": get_questions(short_name, category),
            "sort_order": sort_order,
            "metadata": {
                "full_title": raw_title,
                "word_count": word_count,
                "line_count": work_lines,
            }
        }

        if acts > 0:
            item["metadata"]["acts"] = acts
        if scenes > 0:
            item["metadata"]["scenes"] = scenes

        items.append(item)
        print(f"  [{sort_order:2d}/{len(WORKS)}] {short_name} ({word_count:,} words, {category})")

    grammar = {
        "name": "The Complete Works of William Shakespeare",
        "description": "The complete works of William Shakespeare (1564–1616): 37 plays, 154 sonnets, and 5 longer poems. Comedies of mistaken identity, tragedies of ambition and jealousy, histories of power and succession, romances of loss and restoration, and poetry of love and mortality. Each work is a self-contained item — draw one and let the Bard speak to your situation.",
        "grammar_type": "custom",
        "tags": ["shakespeare", "literature", "drama", "poetry", "classic", "english-literature", "theater"],
        "creator_name": "William Shakespeare",
        "attribution": {
            "source_name": "The Complete Works of William Shakespeare",
            "source_author": "William Shakespeare (1564–1616)",
            "source_url": "https://www.gutenberg.org/ebooks/100",
            "license": "Public Domain"
        },
        "_category_roles": {
            "tragedy": "card",
            "comedy": "card",
            "history": "card",
            "romance": "card",
            "poetry": "card"
        },
        "items": items,
        "metadata": {
            "created": "2026-02-24",
            "license": "CC-BY-SA-4.0",
            "total_works": len(items),
            "note": "Complete works from Project Gutenberg. Each play/poem is one item with full text."
        }
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    outpath = os.path.join(OUTPUT_DIR, "shakespeare-complete.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    total_words = sum(item["metadata"]["word_count"] for item in items)
    print(f"\n  -> {outpath}")
    print(f"     {len(items)} works, {total_words:,} total words")


def _keywords(name, category):
    base = ["shakespeare", category]
    name_words = [w.lower().strip("',") for w in name.split() if len(w) > 2 and w.lower() not in ("the", "and", "of")]
    return base + name_words


if __name__ == "__main__":
    transform_shakespeare()
