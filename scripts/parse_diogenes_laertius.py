#!/usr/bin/env python3
"""
Parse Diogenes Laertius - Lives and Opinions of Eminent Philosophers.
Gutenberg #57342 (C.D. Yonge translation, 1915).
"""
import json, re, os

with open("seeds/diogenes-laertius.txt", encoding="utf-8") as f:
    text = f.read()

gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
gut_end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:gut_end].strip()
lines = body.split("\n")

def truncate(text, limit=2800):
    if len(text) > limit:
        bp = text.rfind(".", 0, limit - 200)
        if bp == -1: bp = limit - 200
        remaining = len(text[bp:].split())
        return text[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    return text

# Find all LIFE OF headings and BOOK headings
life_sections = []
for i, line in enumerate(lines):
    if line.strip().startswith("LIFE OF "):
        name = line.strip()
        if name.endswith("."): name = name[:-1]
        name = name.replace("LIFE OF ", "")
        life_sections.append((i, name))

# Find BOOK headings
book_lines = []
for i, line in enumerate(lines):
    m = re.match(r'^BOOK\s+(I{1,3}V?|IV|V?I{0,3}X?)\.$', line.strip())
    if m:
        book_lines.append((i, m.group(1)))

# Also find INTRODUCTION
intro_line = None
for i, line in enumerate(lines):
    if line.strip() == "INTRODUCTION." and i > 200:  # Skip TOC
        intro_line = i
        break

# Map each philosopher to their Book
def get_book(line_num):
    book = "I"
    for bl, bn in book_lines:
        if bl <= line_num:
            book = bn
        else:
            break
    return book

# Book descriptions
book_info = {
    "I": ("The Seven Sages", "Thales, Solon, and the legendary founders of Greek wisdom"),
    "II": ("The Ionian School & Socrates", "From Anaximander through Socrates and his immediate followers"),
    "III": ("Plato", "The life, doctrines, and dialogues of Plato"),
    "IV": ("The Academy", "Speusippus, Xenocrates, and successors of Plato's Academy"),
    "V": ("The Peripatetics", "Aristotle, Theophrastus, and the Lyceum tradition"),
    "VI": ("The Cynics", "Antisthenes, Diogenes of Sinope, and the Cynic school"),
    "VII": ("The Stoics", "Zeno of Citium, Cleanthes, Chrysippus, and Stoic philosophy"),
    "VIII": ("The Pythagoreans", "Pythagoras, Empedocles, and the Pythagorean tradition"),
    "IX": ("The Pre-Socratics & Skeptics", "Heraclitus, Parmenides, Democritus, Pyrrho, and Timon"),
    "X": ("Epicurus", "The life and doctrines of Epicurus"),
}

# Extract text between line indices
def extract_text(start, end):
    content = []
    started = False
    for j in range(start + 1, min(end, len(lines))):
        line = lines[j]
        if not started and line.strip() == "":
            continue
        started = True
        content.append(line.rstrip())
    while content and content[-1].strip() == "":
        content.pop()
    return "\n".join(content)

# Build items
items = []
sort_order = 1

# Introduction item
if intro_line is not None:
    first_life = life_sections[0][0] if life_sections else len(lines)
    intro_text = extract_text(intro_line, first_life)
    items.append({
        "id": "introduction",
        "name": "Introduction: The Origins of Philosophy",
        "sort_order": sort_order,
        "category": "introduction",
        "level": 1,
        "sections": {
            "Text": truncate(intro_text),
            "Themes": "The origins of philosophy among Greeks and barbarians. The division into Ionian and Italian schools. The meaning of 'philosopher' and 'sophist'. The succession of philosophical schools."
        },
        "keywords": ["philosophy", "origins", "barbarians", "greeks", "schools", "succession"]
    })
    sort_order += 1

# Philosopher life items
for idx, (line_num, name) in enumerate(life_sections):
    # Find end of this section
    if idx + 1 < len(life_sections):
        end_line = life_sections[idx + 1][0]
    else:
        # Last section - find FOOTNOTES or end
        end_line = len(lines)
        for i, line in enumerate(lines):
            if line.strip() == "FOOTNOTES" and i > line_num:
                end_line = i
                break

    philosopher_text = extract_text(line_num, end_line)
    book = get_book(line_num)

    # Clean up name for ID
    clean_name = name.lower().strip()
    clean_name = re.sub(r'[^a-z0-9\s]', '', clean_name)
    clean_name = re.sub(r'\s+', '-', clean_name.strip())

    # Handle duplicates (e.g., two Zenos, two Diogenes, two Crates)
    item_id = clean_name

    # Determine school/tradition
    book_name = book_info.get(book, ("Unknown", ""))[0]

    # Create display name
    display_name = name.title()
    # Fix common names
    display_name = display_name.replace("The Scythian", "the Scythian")
    display_name = display_name.replace("The Eleatic", "the Eleatic")
    display_name = display_name.replace("Of Apollonia", "of Apollonia")

    keywords = ["philosopher", "biography", "ancient-greece"]

    # Add school-specific keywords
    if book == "I":
        keywords.extend(["seven-sages", "pre-socratic"])
    elif book == "II":
        keywords.extend(["socratic", "ionian"])
    elif book == "III":
        keywords.extend(["plato", "academy", "forms"])
    elif book == "IV":
        keywords.extend(["academy", "platonic"])
    elif book == "V":
        keywords.extend(["peripatetic", "lyceum", "aristotle"])
    elif book == "VI":
        keywords.extend(["cynic", "asceticism"])
    elif book == "VII":
        keywords.extend(["stoic", "virtue", "logic"])
    elif book == "VIII":
        keywords.extend(["pythagorean", "mathematics", "harmony"])
    elif book == "IX":
        keywords.extend(["pre-socratic", "skeptic"])
    elif book == "X":
        keywords.extend(["epicurean", "pleasure", "atoms"])

    items.append({
        "id": item_id,
        "name": display_name,
        "sort_order": sort_order,
        "category": f"book-{book.lower()}",
        "level": 1,
        "sections": {
            "Life": truncate(philosopher_text),
            "School": f"Book {book}: {book_name}"
        },
        "keywords": keywords,
        "metadata": {"book": book}
    })
    sort_order += 1

# Handle duplicate IDs
id_counts = {}
for item in items:
    iid = item["id"]
    if iid in id_counts:
        id_counts[iid] += 1
        item["id"] = f"{iid}-{id_counts[iid]}"
    else:
        id_counts[iid] = 1

# Fix first duplicates too
seen = set()
for item in items:
    if item["id"] in seen:
        pass  # already fixed above
    seen.add(item["id"])

# Check for remaining duplicates and fix
all_ids = [i["id"] for i in items]
for i, item in enumerate(items):
    count = all_ids.count(item["id"])
    if count > 1:
        # Find which occurrence this is
        occ = 0
        for j in range(i + 1):
            if items[j]["id"] == item["id"]:
                occ += 1
        if occ > 1:
            item["id"] = f"{item['id']}-{occ}"

# L2 items - one per Book
l1_ids_by_book = {}
for item in items:
    if item["level"] == 1 and "metadata" in item and "book" in item["metadata"]:
        book = item["metadata"]["book"]
        if book not in l1_ids_by_book:
            l1_ids_by_book[book] = []
        l1_ids_by_book[book].append(item["id"])
    elif item["id"] == "introduction":
        if "I" not in l1_ids_by_book:
            l1_ids_by_book["I"] = []
        l1_ids_by_book["I"].insert(0, "introduction")

book_l2_ids = []
for book_num in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]:
    if book_num not in l1_ids_by_book:
        continue
    bname, bdesc = book_info.get(book_num, ("Unknown", ""))
    l2_id = f"book-{book_num.lower()}"
    items.append({
        "id": l2_id,
        "name": f"Book {book_num}: {bname}",
        "sort_order": sort_order,
        "category": "book",
        "level": 2,
        "sections": {
            "About": f"Book {book_num} of Diogenes Laertius covers {bdesc}.",
            "Philosophers": ", ".join(l1_ids_by_book[book_num])
        },
        "keywords": ["book", bname.lower().replace(" ", "-")],
        "composite_of": l1_ids_by_book[book_num],
        "relationship_type": "emergence"
    })
    book_l2_ids.append(l2_id)
    sort_order += 1

# L3 meta
items.append({
    "id": "lives-complete",
    "name": "Lives and Opinions of Eminent Philosophers: Complete",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "The complete work of Diogenes Laertius, covering the lives, doctrines, and sayings of ancient Greek philosophers across ten books. From the Seven Sages through the Stoics, Epicureans, and Skeptics, this is our primary source for many ancient philosophers whose original works are lost.",
        "Structure": "Book I: The Seven Sages. Book II: The Ionian School & Socrates. Book III: Plato. Book IV: The Academy. Book V: The Peripatetics. Book VI: The Cynics. Book VII: The Stoics. Book VIII: The Pythagoreans. Book IX: The Pre-Socratics & Skeptics. Book X: Epicurus."
    },
    "keywords": ["philosophy", "biography", "ancient-greece", "complete"],
    "composite_of": book_l2_ids,
    "relationship_type": "emergence"
})

# Re-number sort orders
for i, item in enumerate(items):
    item["sort_order"] = i + 1

# Remove metadata.book from L1 items (internal use only)
for item in items:
    if "metadata" in item and "book" in item["metadata"]:
        del item["metadata"]["book"]
    if "metadata" in item and not item["metadata"]:
        del item["metadata"]

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Diogenes Laertius", "date": "3rd century CE", "note": "Author"},
            {"name": "C.D. Yonge", "date": "1915", "note": "Translator"},
            {"name": "Project Gutenberg", "date": "2018", "note": "Source: eBook #57342"}
        ]
    },
    "name": "Lives and Opinions of Eminent Philosophers",
    "description": "Diogenes Laertius's compendium of ancient Greek philosophy — biographical sketches, doctrines, sayings, and anecdotes of philosophers from Thales to Epicurus, spanning seven centuries of thought. Translated by C.D. Yonge (1915).\n\nSource: Project Gutenberg eBook #57342 (https://www.gutenberg.org/ebooks/57342)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Thomas Stanley's 'History of Philosophy' (1655-1662) contains engraved portraits of ancient philosophers. The Nuremberg Chronicle (1493) includes woodcut portraits of philosophers.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["philosophy", "biography", "ancient-greece", "pre-socratics", "plato", "aristotle", "stoics", "epicureans", "cynics", "skeptics"],
    "roots": ["western-philosophy", "classical-antiquity"],
    "shelves": ["wisdom"],
    "lineages": ["Linehan", "Andreotti"],
    "worldview": "dialectical",
    "items": items
}

os.makedirs("grammars/diogenes-laertius", exist_ok=True)
with open("grammars/diogenes-laertius/grammar.json", "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

print(f"Generated {len(items)} items")
print(f"L1: {sum(1 for i in items if i['level']==1)}")
print(f"L2: {sum(1 for i in items if i['level']==2)}")
print(f"L3: {sum(1 for i in items if i['level']==3)}")
