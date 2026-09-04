#!/usr/bin/env python3
"""
Build grammar.json for The Mahabharata (Volume 1: Books 1-3).

Source: Project Gutenberg eBook #15474 (Ganguli translation)
Translator: Kisari Mohan Ganguli (1883-1896)

Structure:
- L1: Sections (626 total across 3 books)
- L2: Sub-parvas (thematic groupings within each book)
- L3: Books (Adi Parva, Sabha Parva, Vana Parva)
"""

import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "mahabharata.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "mahabharata"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"


def roman_to_int(s):
    """Convert Roman numeral to integer."""
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    for i in range(len(s)):
        if i + 1 < len(s) and vals.get(s[i], 0) < vals.get(s[i+1], 0):
            result -= vals.get(s[i], 0)
        else:
            result += vals.get(s[i], 0)
    return result


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx >= 0:
        start_idx = text.index("\n", start_idx) + 1
    else:
        start_idx = 0
    end_idx = text.find(end_marker)
    if end_idx < 0:
        end_idx = len(text)
    return text[start_idx:end_idx]


def slugify(s):
    """Convert string to lowercase hyphenated slug."""
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# Book metadata
BOOKS = {
    1: {
        "name": "Adi Parva",
        "full_name": "Adi Parva (The Book of the Beginning)",
        "about": "The Book of the Beginning tells the origin story of the Mahabharata itself, the lineage of the Bharata dynasty, the birth of the Pandavas and Kauravas, and the events leading to the great rivalry. It includes the famous stories of Shakuntala, the churning of the ocean, the birth of Bhishma, the education of the princes, Draupadi's swayamvara, and the burning of the Khandava forest. This book establishes all the characters, relationships, and tensions that will drive the epic.",
        "for_readers": "Start here. The Adi Parva introduces the vast world of the Mahabharata through nested stories — a storyteller tells a story about a storyteller telling a story. The early sections on the snake sacrifice frame the entire epic. The tale of Shakuntala (Sections LXV-LXIX) is one of the most beloved stories in Indian literature.",
    },
    2: {
        "name": "Sabha Parva",
        "full_name": "Sabha Parva (The Book of the Assembly Hall)",
        "about": "The Book of the Assembly Hall describes the building of the Pandavas' magnificent court at Indraprastha, Yudhishthira's Rajasuya sacrifice establishing him as emperor, the fateful dice game in which Yudhishthira gambles away his kingdom, his brothers, Draupadi, and himself, and the Pandavas' exile into the forest. The humiliation of Draupadi in the assembly hall is one of the most pivotal and emotionally intense episodes in the epic.",
        "for_readers": "The Sabha Parva is the dramatic turning point. The dice game (Dyuta Parva) is the Mahabharata's equivalent of the fall — everything that follows, including the great war, flows from this moment of weakness and injustice. Draupadi's speech in the assembly hall is one of the great moments in world literature.",
    },
    3: {
        "name": "Vana Parva",
        "full_name": "Vana Parva (The Book of the Forest)",
        "about": "The Book of the Forest narrates the Pandavas' twelve years of exile in the wilderness. Far from being a mere interlude, it is the longest book in the Mahabharata, filled with philosophical teachings, embedded tales, and spiritual quests. It includes the story of Nala and Damayanti, Arjuna's quest for divine weapons, encounters with sages and celestial beings, pilgrimages to sacred sites, and the famous dialogue between Yudhishthira and the Yaksha.",
        "for_readers": "The Vana Parva is the Mahabharata's great repository of stories within stories. The tale of Nala and Damayanti (Sections L-LXXIX) is a self-contained masterpiece. Arjuna's encounter with Shiva disguised as a hunter (Kairata Parva) is an extraordinary passage. The pilgrimage sections contain India's sacred geography.",
    },
}

# Sub-parva definitions for each book
# These are the named sub-sections that appear in parentheses after SECTION headings
SUB_PARVAS = {
    1: [
        # Adi Parva sub-parvas with section ranges and descriptions
        {"name": "Opening Narrative", "slug": "adi-opening", "sections": (1, 2),
         "about": "The framing narrative: Ugrasrava Sauti arrives at the sacrifice of Saunaka and begins to narrate the Mahabharata as told by Vaisampayana at the snake-sacrifice of King Janamejaya."},
        {"name": "Paushya Parva", "slug": "adi-paushya", "sections": (3, 3),
         "about": "The story of Uttanka's quest for the earrings of King Paushya's queen, which leads to the snake-sacrifice that frames the epic."},
        {"name": "Pauloma Parva", "slug": "adi-pauloma", "sections": (4, 12),
         "about": "The story of the sage Bhrigu, his wife Pauloma, and the origin of the Bhrigu lineage, including the birth of Chyavana."},
        {"name": "Astika Parva", "slug": "adi-astika", "sections": (13, 53),
         "about": "The great snake-sacrifice of King Janamejaya, the story of Garuda and the churning of the ocean for amrita, and the young Brahmin Astika who halts the sacrifice — the frame story within which the Mahabharata is told."},
        {"name": "Adivansavatarana Parva", "slug": "adi-adivansavatarana", "sections": (54, 61),
         "about": "The partial incarnations: the gods, demons, and celestial beings incarnate on earth as the heroes and villains of the Mahabharata. The genealogy of the Bharata dynasty begins."},
        {"name": "Sambhava Parva", "slug": "adi-sambhava", "sections": (62, 130),
         "about": "The birth and early life of the central characters: Bhishma's terrible vow, the stories of Shakuntala and Dushyanta, the birth of the Pandavas and Kauravas, and the growing rivalry between the cousins."},
        {"name": "Jatugriha Parva", "slug": "adi-jatugriha", "sections": (131, 138),
         "about": "The house of lac: Duryodhana's plot to burn the Pandavas alive, their escape through a secret tunnel, and their sojourn in disguise."},
        {"name": "Hidimva-vadha Parva", "slug": "adi-hidimva", "sections": (139, 142),
         "about": "Bhima's encounter with the Rakshasa Hidimba in the forest, his slaying of the demon, and his marriage to Hidimba's sister Hidimbi."},
        {"name": "Vaka-vadha Parva", "slug": "adi-vaka", "sections": (143, 152),
         "about": "The Pandavas' sojourn in Ekachakra, Bhima's slaying of the man-eating Rakshasa Vaka, and the arrival of news about Draupadi's swayamvara."},
        {"name": "Chaitraratha Parva", "slug": "adi-chaitraratha", "sections": (153, 173),
         "about": "The Pandavas' encounter with the Gandharva king Chitraratha on the banks of the Ganga, stories of Tapati and Vasishtha, and preparation for the swayamvara."},
        {"name": "Swayamvara Parva", "slug": "adi-swayamvara", "sections": (174, 185),
         "about": "Draupadi's swayamvara: Arjuna, disguised as a Brahmin, strings the great bow and wins Draupadi's hand. The five Pandavas share Draupadi as their common wife."},
        {"name": "Vaivahika Parva", "slug": "adi-vaivahika", "sections": (186, 194),
         "about": "The wedding ceremonies, Krishna's recognition of the Pandavas, and the establishment of their identity."},
        {"name": "Viduragamana Parva", "slug": "adi-viduragamana", "sections": (195, 206),
         "about": "Vidura's embassy, the Pandavas' return to Hastinapura, and the division of the kingdom — the Pandavas receive the Khandava tract."},
        {"name": "Rajya-labha Parva", "slug": "adi-rajya-labha", "sections": (207, 210),
         "about": "The acquisition of the kingdom: the Pandavas establish their capital at Indraprastha and build their magnificent city."},
        {"name": "Arjuna-vanavasa Parva", "slug": "adi-arjuna-vanavasa", "sections": (211, 216),
         "about": "Arjuna's exile and pilgrimage after inadvertently violating an agreement among the brothers, his adventures and marriages during his travels."},
        {"name": "Subhadra-harana Parva", "slug": "adi-subhadra", "sections": (217, 219),
         "about": "Arjuna's abduction of Subhadra, Krishna's sister, and their marriage — strengthening the alliance between the Pandavas and the Vrishnis."},
        {"name": "Haranaharana Parva", "slug": "adi-haranaharana", "sections": (220, 222),
         "about": "The story of the gifts and the birth of Abhimanyu and other sons of the Pandavas."},
        {"name": "Khandava-daha Parva", "slug": "adi-khandava", "sections": (223, 234),
         "about": "The burning of the Khandava forest: Krishna and Arjuna help Agni (the fire god) consume the forest, defeating Indra himself. Maya the Asura is saved and builds the magnificent assembly hall for the Pandavas."},
    ],
    2: [
        {"name": "Sabhakriya Parva", "slug": "sabha-sabhakriya", "sections": (1, 4),
         "about": "The building of the Pandavas' extraordinary assembly hall by Maya, the celestial architect, filled with wonders and illusions."},
        {"name": "Lokapala Sabhakhayana Parva", "slug": "sabha-lokapala", "sections": (5, 12),
         "about": "Narada's description of the assembly halls of the gods — Indra, Yama, Varuna, Kubera, and Brahma — inspiring Yudhishthira's imperial ambitions."},
        {"name": "Rajasuyarambha Parva", "slug": "sabha-rajasuyarambha", "sections": (13, 19),
         "about": "The beginning of the Rajasuya sacrifice: preparations for Yudhishthira's consecration as emperor, requiring the conquest of all directions."},
        {"name": "Jarasandha-badha Parva", "slug": "sabha-jarasandha", "sections": (20, 24),
         "about": "Krishna, Arjuna, and Bhima journey to Magadha to defeat the mighty king Jarasandha. Bhima kills Jarasandha in single combat, removing the chief obstacle to Yudhishthira's sovereignty."},
        {"name": "Digvijaya Parva", "slug": "sabha-digvijaya", "sections": (25, 33),
         "about": "The conquest of the four quarters: each Pandava brother leads a military campaign to subdue kings in every direction, establishing Yudhishthira's universal sovereignty."},
        {"name": "Rajasuyika Parva", "slug": "sabha-rajasuyika", "sections": (34, 37),
         "about": "The Rajasuya sacrifice itself: the grand ceremony of Yudhishthira's consecration, the gathering of kings, and the offering of the first honors."},
        {"name": "Arghyaharana Parva", "slug": "sabha-arghyaharana", "sections": (38, 42),
         "about": "The offering of the guest-gift (arghya) to Krishna, Shishupala's furious objection, and the rising tensions at the sacrifice."},
        {"name": "Sisupala-badha Parva", "slug": "sabha-sisupala", "sections": (43, 50),
         "about": "The slaying of Shishupala: Krishna beheads the king of Chedi after his hundredth insult, fulfilling an ancient promise. Duryodhana's envy of the Pandavas' glory intensifies."},
        {"name": "Dyuta Parva", "slug": "sabha-dyuta", "sections": (51, 72),
         "about": "The fateful dice game: Duryodhana, aided by the cunning Shakuni, invites Yudhishthira to a game of dice. Yudhishthira gambles away his wealth, kingdom, brothers, and finally Draupadi. The humiliation of Draupadi in the assembly hall — when Duhsasana attempts to disrobe her — is the pivotal moment of the entire epic."},
        {"name": "Anudyuta Parva", "slug": "sabha-anudyuta", "sections": (73, 79),
         "about": "The second dice game: after a brief reprieve, the Pandavas are summoned to play again. Yudhishthira loses and accepts the terms — twelve years of forest exile followed by one year in disguise."},
    ],
    3: [
        {"name": "Aranyaka Parva", "slug": "vana-aranyaka", "sections": (1, 10),
         "about": "The beginning of exile: the Pandavas enter the forest, followed by loyal Brahmins. Yudhishthira receives teachings and the divine vessel Akshaya Patra from the Sun god."},
        {"name": "Kirmirabadha Parva", "slug": "vana-kirmirabadha", "sections": (11, 12),
         "about": "Bhima slays the Rakshasa Kirmira in the Kamyaka forest, securing the Pandavas' dwelling."},
        {"name": "Arjunabhigamana Parva", "slug": "vana-arjunabhigamana", "sections": (13, 37),
         "about": "Arjuna's quest for divine weapons: at Krishna's advice, Arjuna performs severe austerities to obtain celestial weapons from the gods for the coming war."},
        {"name": "Kairata Parva", "slug": "vana-kairata", "sections": (38, 41),
         "about": "Arjuna's encounter with Shiva disguised as a Kirata (mountain hunter). Their fierce battle ends with Shiva revealing himself and granting Arjuna the devastating Pashupata weapon."},
        {"name": "Indralokagamana Parva", "slug": "vana-indralokagamana", "sections": (42, 50),
         "about": "Arjuna's ascent to heaven: he visits Indra's celestial realm, trains with the gods in warfare, and is cursed by the apsara Urvashi — a curse that will later prove a blessing."},
        {"name": "Nalopakhyana Parva", "slug": "vana-nalopakhyana", "sections": (51, 79),
         "about": "The tale of Nala and Damayanti, told to console Yudhishthira: a king loses everything to dice (paralleling Yudhishthira's own fate), wanders in despair, but is ultimately reunited with his devoted wife. One of the great love stories of Indian literature."},
        {"name": "Tirtha-yatra Parva", "slug": "vana-tirtha-yatra", "sections": (80, 153),
         "about": "The great pilgrimage: the Pandavas visit sacred sites across India, hearing stories of gods, sages, and heroes at each stop. Includes the stories of Agastya, Rishyasringa, Rama and the Ramayana, Savitri and Satyavan, and many others. A vast treasury of embedded narratives."},
        {"name": "Markandeya-Samasya Parva", "slug": "vana-markandeya", "sections": (154, 221),
         "about": "The sage Markandeya's teachings: cosmic visions of creation and dissolution, the story of the great deluge, dharma in the age of Kali, and numerous instructive tales including the famous story of the devoted wife and the fowler."},
        {"name": "Ghosha-yatra Parva", "slug": "vana-ghosha-yatra", "sections": (222, 243),
         "about": "Duryodhana's cattle expedition: the Kauravas visit the forest to mock the exiled Pandavas but are captured by Gandharvas. Arjuna rescues Duryodhana — a humiliation that deepens his hatred."},
        {"name": "Draupadi-harana Parva", "slug": "vana-draupadi-harana", "sections": (244, 283),
         "about": "The abduction of Draupadi by Jayadratha, her rescue by the Pandavas, and the story of Savitri — the woman who argued with Death himself to win back her husband's life. Includes the tale of Rama."},
        {"name": "Pativrata-mahatmya Parva", "slug": "vana-pativrata", "sections": (284, 299),
         "about": "The glorification of the devoted wife: stories celebrating fidelity, including the conclusion of the Savitri narrative and philosophical teachings on dharma."},
        {"name": "Aranya Parva (Final)", "slug": "vana-aranya-final", "sections": (300, 313),
         "about": "The final sections of the forest exile: Yudhishthira's encounter with the Yaksha at the enchanted lake — a profound dialogue of riddles testing wisdom and virtue. Yudhishthira's answers reveal his character and earn the restoration of his brothers."},
    ]
}


def parse_mahabharata(text):
    """Parse the Mahabharata into books and sections."""
    # Find book boundaries
    book_starts = []
    for m in re.finditer(r'^BOOK (\d+)\s*$', text, re.MULTILINE):
        book_starts.append((int(m.group(1)), m.start()))

    # Find all section markers
    section_pattern = re.compile(r'^SECTION ([IVXLCDM]+)\s*$', text_flags := re.MULTILINE)
    all_sections = []
    for m in section_pattern.finditer(text):
        sec_num = roman_to_int(m.group(1))
        all_sections.append((sec_num, m.start()))

    # Also find END OF markers and FOOTNOTES to exclude
    end_markers = []
    for m in re.finditer(r'^(END OF .* PARVA|FOOTNOTES)\s*$', text, re.MULTILINE):
        end_markers.append(m.start())

    # Assign sections to books
    books = {}
    for i, (book_num, book_start) in enumerate(book_starts):
        if i + 1 < len(book_starts):
            book_end = book_starts[i + 1][1]
        else:
            book_end = len(text)

        book_sections = [(sn, sp) for sn, sp in all_sections if book_start <= sp < book_end]
        books[book_num] = {"sections": {}, "start": book_start, "end": book_end}

        for j, (sec_num, sec_pos) in enumerate(book_sections):
            # Find end of section
            if j + 1 < len(book_sections):
                sec_end = book_sections[j + 1][1]
            else:
                # End at book end, but exclude end markers/footnotes
                sec_end = book_end
                for em in end_markers:
                    if sec_pos < em < book_end:
                        sec_end = min(sec_end, em)
                        break

            chunk = text[sec_pos:sec_end].strip()
            lines = chunk.split('\n')

            # First line is "SECTION {roman}"
            # Second line might be blank, then sub-parva name in parens, then text
            text_start = 1
            sub_parva = None

            # Skip blank lines after heading
            while text_start < len(lines) and not lines[text_start].strip():
                text_start += 1

            # Check for sub-parva annotation
            if text_start < len(lines):
                parva_match = re.match(r'^\((.+? Parva)\)\s*$', lines[text_start])
                if parva_match:
                    sub_parva = parva_match.group(1)
                    text_start += 1
                    # Skip blank lines after parva annotation
                    while text_start < len(lines) and not lines[text_start].strip():
                        text_start += 1

            section_text = '\n'.join(lines[text_start:]).strip()
            section_text = re.sub(r'\n{3,}', '\n\n', section_text)

            books[book_num]["sections"][sec_num] = {
                "text": section_text,
                "sub_parva": sub_parva,
            }

    return books


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)

    books = parse_mahabharata(text)

    for bn, bd in sorted(books.items()):
        print(f"Book {bn}: {len(bd['sections'])} sections")

    items = []
    sort_order = 0

    # Track all sub-parva IDs for L3 composites
    book_subparva_ids = {1: [], 2: [], 3: []}

    for book_num in sorted(books.keys()):
        book_data = books[book_num]
        book_info = BOOKS[book_num]
        sub_parvas = SUB_PARVAS[book_num]

        section_ids_in_book = []

        # L1: Individual sections
        for sec_num in sorted(book_data["sections"].keys()):
            sort_order += 1
            sec = book_data["sections"][sec_num]
            sec_id = f"book{book_num}-section-{sec_num}"
            section_ids_in_book.append(sec_id)

            sec_name = f"Book {book_num}, Section {sec_num}"
            if sec["sub_parva"]:
                sec_name += f" ({sec['sub_parva']})"

            keywords = [f"book-{book_num}", book_info["name"].lower().replace(" ", "-")]
            if sec["sub_parva"]:
                keywords.append(slugify(sec["sub_parva"]))

            items.append({
                "id": sec_id,
                "name": sec_name,
                "sort_order": sort_order,
                "level": 1,
                "category": f"book-{book_num}",
                "sections": {
                    "Text": sec["text"],
                },
                "keywords": keywords,
                "metadata": {
                    "book": book_num,
                    "section": sec_num,
                    "sub_parva": sec["sub_parva"],
                }
            })

        # L2: Sub-parvas
        for sp in sub_parvas:
            sort_order += 1
            sp_id = sp["slug"]
            book_subparva_ids[book_num].append(sp_id)
            start_sec, end_sec = sp["sections"]

            composite = [f"book{book_num}-section-{s}" for s in range(start_sec, end_sec + 1)
                         if s in book_data["sections"]]

            items.append({
                "id": sp_id,
                "name": sp["name"],
                "sort_order": sort_order,
                "level": 2,
                "category": f"book-{book_num}-sub-parva",
                "relationship_type": "emergence",
                "composite_of": composite,
                "sections": {
                    "About": sp["about"],
                },
                "keywords": [f"book-{book_num}", slugify(sp["name"])],
                "metadata": {
                    "book": book_num,
                    "section_range": list(sp["sections"]),
                }
            })

    # L3: Books
    for book_num in sorted(BOOKS.keys()):
        sort_order += 1
        book_info = BOOKS[book_num]
        items.append({
            "id": f"book-{book_num}-{slugify(book_info['name'])}",
            "name": book_info["full_name"],
            "sort_order": sort_order,
            "level": 3,
            "category": "book",
            "relationship_type": "emergence",
            "composite_of": book_subparva_ids[book_num],
            "sections": {
                "About": book_info["about"],
                "For Readers": book_info["for_readers"],
            },
            "keywords": [f"book-{book_num}", slugify(book_info["name"]), "parva"],
            "metadata": {
                "book": book_num,
            }
        })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Vyasa (traditional author)",
                    "date": "ancient",
                    "note": "Traditional author of the Mahabharata"
                },
                {
                    "name": "Kisari Mohan Ganguli",
                    "date": "1883-1896",
                    "note": "English translator"
                }
            ]
        },
        "name": "The Mahabharata (Volume 1: Books 1-3)",
        "description": "The Mahabharata of Krishna-Dwaipayana Vyasa, Volume 1, in the English prose translation of Kisari Mohan Ganguli (1883-1896). This volume contains the first three of the epic's eighteen books: Adi Parva (The Book of the Beginning), Sabha Parva (The Book of the Assembly Hall), and Vana Parva (The Book of the Forest). Together they tell the origin of the Bharata dynasty, the birth of the Pandavas and Kauravas, the fateful dice game, and the twelve-year forest exile — the great arc from which the rest of the epic unfolds. The Mahabharata is the longest epic poem in the world, a vast ocean of stories containing philosophy, dharma, mythology, and the human condition in all its complexity.\n\nSource: Project Gutenberg eBook #15474 (https://www.gutenberg.org/ebooks/15474)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Indian miniature paintings of Mahabharata scenes from Mughal and Rajput traditions (16th-18th centuries). Raja Ravi Varma's paintings of Draupadi, Arjuna, and other characters (1890s). Illustrations from early 20th century editions published by the Bharata Karyalaya.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["epic", "mythology", "dharma", "hinduism", "sanskrit-literature", "philosophy", "public-domain", "full-text"],
        "roots": ["eastern-wisdom"],
        "shelves": ["earth"],
        "lineages": ["Shrei"],
        "worldview": "devotional",
        "items": items,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1: {l1} sections, L2: {l2} sub-parvas, L3: {l3} books")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
