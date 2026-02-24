#!/usr/bin/env python3
"""
Transform source texts into recursive.eco grammar JSON format.

Handles:
  1. Zohar (Sefaria JSON) -> grammar JSON
  2. Dhammapada (Gutenberg plain text) -> grammar JSON
  3. Confucius Analects (Sacred Texts plain text) -> grammar JSON
  4. Alice in Wonderland (Gutenberg plain text) -> grammar JSON

Usage:
  python3 transform-to-grammar.py           # transform all
  python3 transform-to-grammar.py zohar     # transform just one
  python3 transform-to-grammar.py dhammapada
  python3 transform-to-grammar.py confucius
  python3 transform-to-grammar.py alice
"""

import json
import re
import os
import sys

SOURCES_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(SOURCES_DIR), "schemas", "other", "religious-texts")


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def write_grammar(filename, grammar):
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"  -> {path} ({len(grammar['items'])} items)")


def strip_gutenberg(text):
    """Remove Project Gutenberg header and footer from text."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start = text.find(start_marker)
    if start != -1:
        start = text.index("\n", start) + 1
    else:
        start = 0

    end = text.find(end_marker)
    if end == -1:
        end = len(text)

    return text[start:end].strip()


# ---------------------------------------------------------------------------
# 1. ZOHAR
# ---------------------------------------------------------------------------
def transform_zohar():
    print("Transforming Zohar...")
    path = os.path.join(SOURCES_DIR, "zohar")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    # First line is a source comment, rest is JSON
    json_start = raw.index("{")
    data = json.loads(raw[json_start:])

    schema_nodes = data.get("schema", {}).get("nodes", [])
    text_sections = data.get("text", {})

    # Build a lookup of Hebrew titles
    he_titles = {}
    for node in schema_nodes:
        he_titles[node["enTitle"]] = node.get("heTitle", "")

    items = []
    sort_order = 0

    for section_name, content in text_sections.items():
        if section_name == "Addenda":
            # Addenda has nested volumes
            for vol_name, vol_content in content.items():
                sort_order += 1
                paragraphs = _zohar_extract_paragraphs(vol_content)
                he = ""
                for node in schema_nodes:
                    if node.get("enTitle") == "Addenda":
                        for sub in node.get("nodes", []):
                            if sub["enTitle"] == vol_name:
                                he = sub.get("heTitle", "")
                items.append({
                    "id": _slugify(f"addenda-{vol_name}"),
                    "name": f"Addenda — {vol_name}",
                    "symbol": he or "✡",
                    "category": "addenda",
                    "sections": _zohar_sections(paragraphs),
                    "keywords": ["zohar", "kabbalah", "addenda"],
                    "sort_order": sort_order,
                    "metadata": {
                        "hebrew_title": he,
                        "has_content": len(paragraphs) > 0
                    }
                })
        else:
            sort_order += 1
            paragraphs = _zohar_extract_paragraphs(content)
            he = he_titles.get(section_name, "")

            # Determine category based on Torah portion grouping
            category = _zohar_category(section_name)

            item = {
                "id": _slugify(section_name),
                "name": section_name,
                "symbol": he or "✡",
                "category": category,
                "sections": _zohar_sections(paragraphs),
                "keywords": ["zohar", "kabbalah", "mysticism", section_name.lower()],
                "sort_order": sort_order,
                "metadata": {
                    "hebrew_title": he,
                    "has_content": len(paragraphs) > 0
                }
            }
            items.append(item)

    grammar = {
        "name": "Zohar — The Book of Splendor",
        "description": "The Zohar (ספר הזהר, 'Book of Radiance') is the foundational work of Jewish mystical thought known as Kabbalah. Structured as a commentary on the Torah's weekly portions (parshiot), it reveals hidden layers of meaning through allegory, mystical narrative, and cosmological teaching. This translation by Ami Silver (2020) from Sefaria contains the Bereshit section with its famous meditation on the flame and the concealed light.",
        "grammar_type": "custom",
        "tags": ["kabbalah", "zohar", "jewish-mysticism", "torah", "sefira", "sacred-text"],
        "creator_name": "Traditional (attributed to Rabbi Shimon bar Yochai)",
        "attribution": {
            "source_name": "Zohar",
            "source_author": "Traditional (attributed to Rabbi Shimon bar Yochai, compiled ~1290 CE by Moses de León)",
            "translator": "Ami Silver, 2020",
            "source_url": "https://www.sefaria.org/Zohar?tab=contents",
            "license": "Sefaria (see source for terms)",
            "note": "Most sections in this translation are empty stubs. Bereshit contains the primary translated content."
        },
        "_category_roles": {
            "bereshit": "card",
            "shemot": "card",
            "vayikra": "card",
            "bamidbar": "card",
            "devarim": "card",
            "special": "card",
            "addenda": "card"
        },
        "items": items,
        "metadata": {
            "created": "2026-02-24",
            "license": "CC-BY-SA-4.0",
            "note": "Transformed from Sefaria structured data. Most parshiot are empty in this translation — only Bereshit section 108 contains verses."
        }
    }

    write_grammar("zohar-sefaria.json", grammar)


def _zohar_extract_paragraphs(content):
    """Recursively extract non-empty strings from nested arrays."""
    paragraphs = []
    if isinstance(content, str):
        if content.strip():
            paragraphs.append(content.strip())
    elif isinstance(content, list):
        for item in content:
            paragraphs.extend(_zohar_extract_paragraphs(item))
    return paragraphs


def _zohar_sections(paragraphs):
    if not paragraphs:
        return {"Text": "(This section has not yet been translated in this edition.)"}
    return {"Text": "\n\n".join(paragraphs)}


def _zohar_category(name):
    """Map parsha names to Torah book categories."""
    bereshit = ["Introduction", "Bereshit", "Noach", "Lech Lecha", "Vayera",
                "Chayei Sara", "Toldot", "Vayetzei", "Vayishlach", "Vayeshev",
                "Miketz", "Vayigash", "Vayechi"]
    shemot = ["Shemot", "Vaera", "Bo", "Beshalach", "Yitro", "Mishpatim",
              "Terumah", "Tetzaveh", "Ki Tisa", "Vayakhel", "Pekudei"]
    vayikra = ["Vayikra", "Tzav", "Shmini", "Tazria", "Metzora",
               "Achrei Mot", "Kedoshim", "Emor", "Behar", "Bechukotai"]
    bamidbar = ["Bamidbar", "Nasso", "Beha'alotcha", "Sh'lach", "Korach",
                "Chukat", "Balak", "Pinchas", "Matot"]
    devarim = ["Vaetchanan", "Eikev", "Shoftim", "Ki Teitzei", "Vayeilech", "Ha'Azinu"]
    special = ["Sifra DiTzniuta", "Idra Rabba", "Idra Zuta"]

    if name in bereshit: return "bereshit"
    if name in shemot: return "shemot"
    if name in vayikra: return "vayikra"
    if name in bamidbar: return "bamidbar"
    if name in devarim: return "devarim"
    if name in special: return "special"
    return "other"


# ---------------------------------------------------------------------------
# 2. DHAMMAPADA
# ---------------------------------------------------------------------------
def transform_dhammapada():
    print("Transforming Dhammapada...")
    path = os.path.join(SOURCES_DIR, "Dhammapada")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    # If no Gutenberg markers, strip the header manually
    if "DHAMMAPADA" in text:
        idx = text.index("DHAMMAPADA")
        text = text[idx:]

    # Split by "Chapter N." pattern
    chapter_pattern = re.compile(r'^Chapter\s+([IVXLC]+)\.\s+(.+)$', re.MULTILINE)
    matches = list(chapter_pattern.finditer(text))

    items = []
    chapter_categories = {
        "I": "mind", "II": "mind", "III": "mind",
        "IV": "world", "V": "wisdom", "VI": "wisdom",
        "VII": "liberation", "VIII": "wisdom", "IX": "ethics",
        "X": "ethics", "XI": "world", "XII": "world",
        "XIII": "world", "XIV": "liberation", "XV": "liberation",
        "XVI": "world", "XVII": "ethics", "XVIII": "ethics",
        "XIX": "wisdom", "XX": "path", "XXI": "path",
        "XXII": "ethics", "XXIII": "path", "XXIV": "path",
        "XXV": "mastery", "XXVI": "mastery"
    }

    for i, match in enumerate(matches):
        roman = match.group(1)
        title = match.group(2).strip()
        chapter_num = i + 1

        # Extract text until next chapter or end
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chapter_text = text[start:end].strip()

        # Remove Gutenberg footer if it leaks in
        footer_idx = chapter_text.find("*** END OF THE PROJECT GUTENBERG")
        if footer_idx != -1:
            chapter_text = chapter_text[:footer_idx].strip()

        # Count verses
        verse_numbers = re.findall(r'^\d+\.', chapter_text, re.MULTILINE)
        verse_count = len(verse_numbers)

        # First and last verse numbers
        first_verse = verse_numbers[0].rstrip('.') if verse_numbers else "?"
        last_verse = verse_numbers[-1].rstrip('.') if verse_numbers else "?"

        category = chapter_categories.get(roman, "path")

        items.append({
            "id": f"dhammapada-{chapter_num:02d}-{_slugify(title)}",
            "name": f"Chapter {roman} — {title}",
            "symbol": "☸",
            "category": category,
            "sections": {
                "Text": chapter_text
            },
            "keywords": _dhammapada_keywords(title, category),
            "questions": _dhammapada_questions(title),
            "sort_order": chapter_num,
            "metadata": {
                "chapter_number": chapter_num,
                "roman_numeral": roman,
                "verse_range": f"{first_verse}–{last_verse}",
                "verse_count": verse_count
            }
        })

    grammar = {
        "name": "Dhammapada — Verses of the Dharma",
        "description": "The Dhammapada ('Path of the Dharma') is one of the best-known texts from the Pali Canon, the scriptures of Theravada Buddhism. Its 423 verses in 26 chapters distill the essence of the Buddha's teaching into practical wisdom on ethics, mind, and liberation. This is the classic translation by F. Max Müller (1881) from the Sacred Books of the East.",
        "grammar_type": "custom",
        "tags": ["buddhism", "dhammapada", "pali-canon", "theravada", "wisdom", "sacred-text", "meditation"],
        "creator_name": "Traditional (attributed to Gautama Buddha)",
        "attribution": {
            "source_name": "Dhammapada, a Collection of Verses",
            "source_author": "Traditional (attributed to Gautama Buddha, compiled ~3rd century BCE)",
            "translator": "F. Max Müller (1881)",
            "source_url": "https://www.gutenberg.org/ebooks/2017",
            "license": "Public Domain",
            "note": "From The Sacred Books of the East, Volume X, Part I. Translated from Pali."
        },
        "_category_roles": {
            "mind": "card",
            "wisdom": "card",
            "ethics": "card",
            "world": "card",
            "liberation": "card",
            "path": "card",
            "mastery": "card"
        },
        "items": items,
        "metadata": {
            "created": "2026-02-24",
            "license": "CC-BY-SA-4.0",
            "total_verses": 423,
            "note": "Complete F. Max Müller translation. Each chapter is one item containing all its verses."
        }
    }

    write_grammar("dhammapada-muller.json", grammar)


def _dhammapada_keywords(title, category):
    base = ["buddhism", "dhammapada", "dharma"]
    title_words = [w.lower().strip("()") for w in title.split() if len(w) > 2]
    return base + title_words + [category]


def _dhammapada_questions(title):
    prompts = {
        "Twin-Verses": ["What thought patterns shape your current reality?", "Where are you planting seeds of suffering or happiness?"],
        "Earnestness": ["Where in your life does earnestness need to replace carelessness?", "What would change if you were fully awake to this moment?"],
        "Thought": ["What is the quality of your mind right now?", "Can you observe your thoughts without following them?"],
        "Flowers": ["What is blooming in your life that deserves attention?", "What beauty are you overlooking?"],
        "Fool": ["Where are you acting without awareness?", "What mistake do you keep repeating?"],
        "Wise Man": ["Whose counsel do you seek?", "How do you receive correction?"],
        "Venerable": ["What would it mean to be truly free?", "What attachments still bind you?"],
        "Thousands": ["What single truth matters more than a thousand hollow words?", "Where is quality more important than quantity in your life?"],
        "Evil": ["What small unwholesome act are you tolerating?", "Where does a small choice lead to larger consequences?"],
        "Punishment": ["How do you respond when others cause harm?", "What does justice mean to you?"],
        "Old Age": ["What are you building that will last?", "How do you relate to impermanence?"],
        "Self": ["Who are you when no one is watching?", "Are you your own refuge?"],
        "World": ["What is your relationship to worldly life?", "Where do you confuse the map for the territory?"],
        "Buddha": ["What does awakening mean to you?", "Who is your teacher?"],
        "Happiness": ["What is the difference between pleasure and true happiness?", "When have you felt deepest contentment?"],
        "Pleasure": ["What attachments bring you joy and pain in equal measure?", "Can you love without clinging?"],
        "Anger": ["What triggers your anger?", "What would patience look like right now?"],
        "Impurity": ["What habits cloud your clarity?", "Where do you need purification?"],
        "Just": ["What does right action look like today?", "Are you living in accordance with your values?"],
        "Way": ["Are you on the path you want to be on?", "What is the next step?"],
        "Miscellaneous": ["What teaching do you need to hear today?", "What have you been resisting?"],
        "Downward Course": ["What consequences are you ignoring?", "Where does heedlessness lead?"],
        "Elephant": ["What is your strength?", "How do you endure difficulty?"],
        "Thirst": ["What craving drives you most?", "What would contentment feel like?"],
        "Bhikshu": ["What would a life of simplicity look like?", "What are you willing to renounce?"],
        "Brahmana": ["What does true nobility mean?", "Who is worthy of reverence?"],
    }
    # Find matching key
    for key, qs in prompts.items():
        if key.lower() in title.lower():
            return qs
    return ["What does this teaching illuminate in your life?"]


# ---------------------------------------------------------------------------
# 3. CONFUCIUS ANALECTS
# ---------------------------------------------------------------------------
def transform_confucius():
    print("Transforming Confucius Analects...")
    path = os.path.join(SOURCES_DIR, "confucius")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Remove source header and footer
    lines = raw.split("\n")

    # Find where the actual text starts (after the header info)
    text_start = 0
    for i, line in enumerate(lines):
        if re.match(r'^\s+1\s*$', line):
            text_start = i
            break

    # Find THE END
    text_end = len(lines)
    for i, line in enumerate(lines):
        if "THE END" in line:
            text_end = i
            break

    text = "\n".join(lines[text_start:text_end])

    # Split by centered book numbers
    book_pattern = re.compile(r'^\s+(\d+)\s*$', re.MULTILINE)
    matches = list(book_pattern.finditer(text))

    # Traditional book names for the Analects
    book_names = {
        1: "Xue Er (Learning)",
        2: "Wei Zheng (Governance)",
        3: "Ba Yi (Eight Rows of Dance)",
        4: "Li Ren (Living with Virtue)",
        5: "Gong Ye Chang",
        6: "Yong Ye",
        7: "Shu Er (Transmission)",
        8: "Tai Bo",
        9: "Zi Han (The Master Seldom Spoke)",
        10: "Xiang Dang (In the Village)",
        11: "Xian Jin (The Earlier Men)",
        12: "Yan Yuan",
        13: "Zi Lu",
        14: "Xian Wen (Constitutional Questions)",
        15: "Wei Ling Gong (Duke Ling of Wei)",
        16: "Ji Shi (The Ji Family)",
        17: "Yang Huo",
        18: "Wei Zi (The Viscount of Wei)",
        19: "Zi Zhang",
        20: "Yao Yue (Yao Said)"
    }

    categories = {
        1: "learning", 2: "governance", 3: "ritual", 4: "virtue",
        5: "character", 6: "character", 7: "learning", 8: "virtue",
        9: "character", 10: "conduct", 11: "character", 12: "virtue",
        13: "governance", 14: "governance", 15: "wisdom", 16: "governance",
        17: "character", 18: "character", 19: "learning", 20: "governance"
    }

    items = []
    for i, match in enumerate(matches):
        book_num = int(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        book_text = text[start:end].strip()

        # Count passages (roughly by "The Master said" or paragraph breaks)
        passages = len(re.findall(r'(?:The Master|Tsze-|The philosopher|Confucius)', book_text))

        name = book_names.get(book_num, f"Book {book_num}")
        category = categories.get(book_num, "wisdom")

        items.append({
            "id": f"analects-{book_num:02d}-{_slugify(name)}",
            "name": f"Book {book_num} — {name}",
            "symbol": "仁",
            "category": category,
            "sections": {
                "Text": book_text
            },
            "keywords": ["confucius", "analects", "chinese-philosophy", category],
            "questions": _confucius_questions(book_num),
            "sort_order": book_num,
            "metadata": {
                "book_number": book_num,
                "chinese_name": name.split("(")[0].strip() if "(" in name else "",
                "approximate_passages": passages
            }
        })

    grammar = {
        "name": "Confucian Analects — Lunyu",
        "description": "The Analects (論語, Lunyu) is the most influential collection of sayings and ideas attributed to Confucius and his contemporaries. Compiled by his disciples after his death, its 20 books cover ethics, governance, ritual propriety, and the cultivation of virtue. This is the classic James Legge translation (1893).",
        "grammar_type": "custom",
        "tags": ["confucianism", "analects", "chinese-philosophy", "ethics", "governance", "sacred-text"],
        "creator_name": "Confucius (compiled by disciples)",
        "attribution": {
            "source_name": "Confucian Analects",
            "source_author": "Confucius (551–479 BCE)",
            "translator": "James Legge (1893)",
            "source_url": "https://www.sacred-texts.com/cfu/conf1.htm",
            "license": "Public Domain",
            "note": "From The Chinese Classics, translated by James Legge."
        },
        "_category_roles": {
            "learning": "card",
            "governance": "card",
            "ritual": "card",
            "virtue": "card",
            "character": "card",
            "conduct": "card",
            "wisdom": "card"
        },
        "items": items,
        "metadata": {
            "created": "2026-02-24",
            "license": "CC-BY-SA-4.0",
            "note": "Complete James Legge translation. Each book is one item."
        }
    }

    write_grammar("confucius-analects-legge.json", grammar)


def _confucius_questions(book_num):
    prompts = {
        1: ["What are you learning with perseverance?", "Who are your true friends?"],
        2: ["How do you lead by example?", "What guides your moral compass?"],
        3: ["What rituals give structure to your life?", "Where is sincerity missing?"],
        4: ["What does living virtuously look like today?", "Where do you dwell in benevolence?"],
        5: ["How do you judge character — your own and others'?"],
        6: ["What does balance look like in your life?"],
        7: ["What wisdom have you received that you can transmit?", "What are you devoted to?"],
        8: ["Who do you admire and why?", "What legacy are you building?"],
        9: ["What words best describe who you are?", "What do you rarely speak about?"],
        10: ["How does your conduct change in different settings?", "Where are you most authentic?"],
        11: ["What do the young teach the old?", "What do you value in others?"],
        12: ["What does benevolence require of you right now?"],
        13: ["How do you correct what is wrong?", "What does righteous leadership look like?"],
        14: ["What constitutional question is your life asking you?"],
        15: ["What principle would you not abandon under any circumstance?"],
        16: ["What is the proper relationship between power and responsibility?"],
        17: ["Where does your nature conflict with your nurture?"],
        18: ["When is withdrawal from the world the right choice?"],
        19: ["What would your students say about you?"],
        20: ["What does wise governance look like in your sphere of influence?"],
    }
    return prompts.get(book_num, ["What does the Master's teaching reveal about your own path?"])


# ---------------------------------------------------------------------------
# 4. ALICE IN WONDERLAND
# ---------------------------------------------------------------------------
def transform_alice():
    print("Transforming Alice in Wonderland...")
    path = os.path.join(SOURCES_DIR, "alice-in-wonderland")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)

    # Split by CHAPTER pattern
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC]+)\.\s*\n(.+?)(?:\n|$)', re.MULTILINE)
    matches = list(chapter_pattern.finditer(text))

    items = []
    for i, match in enumerate(matches):
        roman = match.group(1)
        title = match.group(2).strip()
        chapter_num = i + 1

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chapter_text = text[start:end].strip()

        # Remove Gutenberg footer
        footer_idx = chapter_text.find("*** END OF THE PROJECT GUTENBERG")
        if footer_idx != -1:
            chapter_text = chapter_text[:footer_idx].strip()

        # Remove [Illustration] tags
        chapter_text = re.sub(r'\[Illustration(?::[^\]]+)?\]', '', chapter_text).strip()

        # Estimate word count
        word_count = len(chapter_text.split())

        category = _alice_category(title)

        items.append({
            "id": f"alice-{chapter_num:02d}-{_slugify(title)}",
            "name": f"Chapter {roman} — {title}",
            "symbol": "🐇",
            "category": category,
            "sections": {
                "Text": chapter_text
            },
            "keywords": _alice_keywords(title),
            "questions": _alice_questions(title),
            "sort_order": chapter_num,
            "metadata": {
                "chapter_number": chapter_num,
                "word_count": word_count
            }
        })

    grammar = {
        "name": "Alice's Adventures in Wonderland",
        "description": "Lewis Carroll's beloved 1865 novel follows young Alice down a rabbit hole into a fantastical world where nothing is as it seems. A masterwork of literary nonsense, it explores logic, identity, and the absurdity of adult conventions through a child's eyes. Each chapter is a self-contained adventure that works as an oracle for navigating life's surreal moments.",
        "grammar_type": "custom",
        "tags": ["literature", "fantasy", "lewis-carroll", "classic", "wonderland", "nonsense", "victorian"],
        "creator_name": "Lewis Carroll",
        "attribution": {
            "source_name": "Alice's Adventures in Wonderland",
            "source_author": "Lewis Carroll (Charles Lutwidge Dodgson)",
            "source_year": "1865",
            "source_url": "https://www.gutenberg.org/ebooks/11",
            "license": "Public Domain"
        },
        "_category_roles": {
            "descent": "card",
            "transformation": "card",
            "encounter": "card",
            "trial": "card"
        },
        "items": items,
        "metadata": {
            "created": "2026-02-24",
            "license": "CC-BY-SA-4.0",
            "note": "Complete text from Project Gutenberg. Each chapter is one item."
        }
    }

    write_grammar("alice-in-wonderland-carroll.json", grammar)


def _alice_category(title):
    descent = ["Rabbit-Hole", "Pool of Tears"]
    transformation = ["Caterpillar", "Pig and Pepper", "Little Bill"]
    trial = ["Tarts", "Evidence"]
    for d in descent:
        if d.lower() in title.lower():
            return "descent"
    for t in transformation:
        if t.lower() in title.lower():
            return "transformation"
    for t in trial:
        if t.lower() in title.lower():
            return "trial"
    return "encounter"


def _alice_keywords(title):
    base = ["alice", "wonderland", "carroll"]
    title_words = [w.lower().strip("'\"") for w in title.split() if len(w) > 2 and w.lower() not in ("the", "and")]
    return base + title_words


def _alice_questions(title):
    prompts = {
        "Rabbit-Hole": ["What unknown territory are you being drawn into?", "What curiosity is calling you?"],
        "Pool of Tears": ["What emotions are you swimming in?", "How has your sense of self been disrupted?"],
        "Caucus-Race": ["What absurd competition are you caught in?", "When does everyone win?"],
        "Little Bill": ["Where do you feel too big or too small for the situation?"],
        "Caterpillar": ["Who are you?", "What transformation is underway?"],
        "Pig and Pepper": ["What situation is chaotic beyond reason?", "What needs to be left behind?"],
        "Tea-Party": ["What social ritual has become meaningless?", "Where is time stuck?"],
        "Croquet": ["What game are you playing where the rules keep changing?"],
        "Mock Turtle": ["What are you mourning that may never have existed?"],
        "Lobster": ["What absurd dance is life asking of you?"],
        "Tarts": ["What accusation hangs in the air?", "What verdict are you waiting for?"],
        "Evidence": ["What evidence speaks for itself?", "When is it time to stand up and say 'you're nothing but a pack of cards'?"],
    }
    for key, qs in prompts.items():
        if key.lower() in title.lower():
            return qs
    return ["What does this chapter of Wonderland mirror in your life?"]


# ---------------------------------------------------------------------------
# UTILITY
# ---------------------------------------------------------------------------
def _slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = text.strip('-')
    return text


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
TRANSFORMS = {
    "zohar": transform_zohar,
    "dhammapada": transform_dhammapada,
    "confucius": transform_confucius,
    "alice": transform_alice,
}

if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(TRANSFORMS.keys())

    for name in targets:
        if name in TRANSFORMS:
            TRANSFORMS[name]()
        else:
            print(f"Unknown target: {name}. Options: {', '.join(TRANSFORMS.keys())}")
            sys.exit(1)

    print("\nDone! Grammar files written to:")
    print(f"  {OUTPUT_DIR}/")
