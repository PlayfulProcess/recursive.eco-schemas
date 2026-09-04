#!/usr/bin/env python3
"""
Parse Golden Ass (Apuleius, Gutenberg #1666) and Mabinogion (Gutenberg).
Two grammars in one script.
"""
import json, re, os

def truncate(text, limit=3000):
    if len(text) > limit:
        bp = text.rfind(".", 0, limit - 200)
        if bp == -1: bp = limit - 200
        remaining = len(text[bp:].split())
        return text[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"
    return text

# ═══════════════════════════════════════════════════════════════════════════
# GOLDEN ASS
# ═══════════════════════════════════════════════════════════════════════════

with open("seeds/golden-ass-apuleius.txt", encoding="utf-8") as f:
    ga_text = f.read()

ga_start = ga_text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
ga_start = ga_text.find("\n", ga_start) + 1
ga_end = ga_text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
ga_body = ga_text[ga_start:ga_end].strip()
ga_lines = ga_body.split("\n")

# Find book positions
book_headings = [
    ("THE FIRST BOOKE", "book-1", "Book I: Lucius's Journey to Thessaly"),
    ("THE SECOND BOOKE", "book-2", "Book II: The House of Milo and Pamphile"),
    ("THE THIRD BOOKE", "book-3", "Book III: The Transformation into an Ass"),
    ("THE FOURTH BOOKE", "book-4", "Book IV: Among the Robbers / Cupid and Psyche Begins"),
    # Book 5 heading is missing in this edition - the Psyche story continues
    ("THE SIXTH BOOKE", "book-6", "Book VI: Psyche's Tasks and Redemption"),
    ("THE SEVENTH BOOKE", "book-7", "Book VII: The Ass's Misadventures"),
    ("THE EIGHTH BOOKE", "book-8", "Book VIII: The Priests of the Syrian Goddess"),
    ("THE NINTH BOOKE", "book-9", "Book IX: The Miller's Wife and Other Tales"),
    ("THE TENTH BOOKE", "book-10", "Book X: The Condemned Woman and the Show"),
    ("THE ELEVENTH BOOKE", "book-11", "Book XI: Isis and Salvation"),
]

ga_items = []
sort_order = 1

book_positions = []
for heading, sid, name in book_headings:
    for i, line in enumerate(ga_lines):
        if line.strip() == heading:
            book_positions.append((i, heading, sid, name))
            break

book_positions.sort(key=lambda x: x[0])

# Also insert a synthetic Book 5 between Book 4 and Book 6
# Find the middle of the Psyche story (Books 4-6)
b4_idx = next(i for i, (ln, h, s, n) in enumerate(book_positions) if s == "book-4")
b6_idx = next(i for i, (ln, h, s, n) in enumerate(book_positions) if s == "book-6")
b4_end = book_positions[b6_idx][0]
b4_start = book_positions[b4_idx][0]
# Approximate midpoint
mid = (b4_start + b4_end) // 2
book_positions.insert(b4_idx + 1, (mid, "BOOK 5 (SYNTHETIC)", "book-5", "Book V: Cupid and Psyche — The Heart of the Tale"))
book_positions.sort(key=lambda x: x[0])

# Astrology for each book
ga_astrology = {
    "book-1": {"planets": ["Mercury"], "signs": ["Gemini"], "themes": ["journey", "curiosity"]},
    "book-2": {"planets": ["Moon", "Neptune"], "signs": ["Scorpio"], "themes": ["sorcery", "night"]},
    "book-3": {"planets": ["Pluto", "Moon"], "signs": ["Scorpio"], "themes": ["transformation", "animal-body"]},
    "book-4": {"planets": ["Venus", "Pluto"], "signs": ["Libra", "Scorpio"], "themes": ["cupid-psyche-begins", "captivity"]},
    "book-5": {"planets": ["Venus", "Pluto"], "signs": ["Scorpio", "Libra"], "themes": ["forbidden-sight", "love-in-darkness"]},
    "book-6": {"planets": ["Venus", "Saturn", "Pluto"], "signs": ["Scorpio", "Capricorn"], "themes": ["impossible-tasks", "descent-to-underworld"]},
    "book-7": {"planets": ["Saturn"], "signs": ["Capricorn"], "themes": ["servitude", "endurance"]},
    "book-8": {"planets": ["Neptune", "Jupiter"], "signs": ["Pisces"], "themes": ["false-religion", "degradation"]},
    "book-9": {"planets": ["Mars", "Saturn"], "signs": ["Aries"], "themes": ["cruelty", "adultery", "punishment"]},
    "book-10": {"planets": ["Mars", "Venus"], "signs": ["Scorpio"], "themes": ["spectacle", "degradation", "escape"]},
    "book-11": {"planets": ["Moon", "Neptune", "Jupiter"], "signs": ["Pisces", "Cancer"], "themes": ["isis", "salvation", "divine-feminine"]},
}

for idx, (start_ln, heading, sid, name) in enumerate(book_positions):
    end_ln = book_positions[idx+1][0] if idx+1 < len(book_positions) else len(ga_lines)
    content = []
    started = False
    for j in range(start_ln + 1, end_ln):
        line = ga_lines[j]
        if not started and line.strip() == "":
            continue
        started = True
        content.append(line.rstrip())
    while content and content[-1].strip() == "":
        content.pop()
    full_text = "\n".join(content)
    excerpt = truncate(full_text)

    metadata = {"origin": "Roman/North African"}
    if sid in ga_astrology:
        metadata["astrology"] = ga_astrology[sid]

    ga_items.append({
        "id": sid,
        "name": name,
        "sort_order": sort_order,
        "category": "books",
        "level": 1,
        "sections": {"Text": excerpt},
        "keywords": ["apuleius", "golden-ass", "metamorphoses", "roman"],
        "metadata": metadata
    })
    sort_order += 1

# L2: The Cupid and Psyche tale
ga_items.append({
    "id": "cycle-cupid-psyche",
    "name": "The Tale of Cupid and Psyche",
    "sort_order": sort_order,
    "category": "cycles",
    "level": 2,
    "sections": {
        "About": "Embedded in the center of the Golden Ass (Books IV-VI), the tale of Cupid and Psyche is one of the most influential stories in world literature — the prototype for Beauty and the Beast, Cinderella, and every fairy tale where love must survive impossible trials. Psyche (Soul) is so beautiful that Venus is jealous and sends Cupid (Desire) to make her fall in love with a monster. Instead, Cupid falls in love with her. He visits her only in darkness, forbidding her to see his face. When she lights a lamp and sees the god, he flees. She must complete four impossible tasks set by Venus — sorting seeds, gathering golden fleece, fetching water from the Styx, descending to the underworld — before she can be reunited with Love. Jung's favorite myth. The original sacred marriage.",
        "For Readers": "This is the story the Myths Through Many Eyes grammar calls myth-psyche-eros. Reading it in its full Apuleian context — told by an old woman to a kidnapped girl, inside a novel about a man turned into a donkey — adds layers that the mythological summary cannot capture. The tale is simultaneously a fairy tale, an allegory of the soul's journey, and a deeply funny story about the gods behaving badly."
    },
    "keywords": ["cupid", "psyche", "soul", "love", "trials", "sacred-marriage"],
    "composite_of": ["book-4", "book-5", "book-6"],
    "relationship_type": "emergence",
    "metadata": {"astrology": {"planets": ["Venus", "Pluto"], "signs": ["Libra", "Scorpio"], "themes": ["soul-and-desire", "impossible-tasks", "sacred-marriage"]}}
})
sort_order += 1

# L2: The Isis revelation
ga_items.append({
    "id": "cycle-isis",
    "name": "The Isis Revelation: Salvation Through the Divine Feminine",
    "sort_order": sort_order,
    "category": "cycles",
    "level": 2,
    "sections": {
        "About": "Book XI of the Golden Ass is unlike anything else in ancient literature — a genuine conversion narrative. After ten books of suffering, degradation, and comedy in the body of an ass, Lucius prays to the moon goddess and receives a vision of Isis, who tells him: eat the roses at tomorrow's procession and you will be restored. He does. He is transformed back into a man. He is initiated into the mysteries of Isis and Osiris. The novel ends not with laughter but with devotion. Scholars debate whether Apuleius himself was an Isis initiate; the passage's emotional sincerity suggests he was. This is the earliest surviving account of personal religious conversion in Western literature.",
        "For Readers": "Read this after the degradation of Books VII-X. The contrast is the point: the deeper the fall, the more powerful the redemption. Isis addresses Lucius by all her names — she is Minerva, Venus, Diana, Proserpina, Ceres, Juno, Bellona, Hecate, and the Queen of the Dead. She is every goddess, and her message is: I have watched your suffering, and now I come."
    },
    "keywords": ["isis", "salvation", "divine-feminine", "initiation", "mystery"],
    "composite_of": ["book-10", "book-11"],
    "relationship_type": "emergence",
    "metadata": {"astrology": {"planets": ["Moon", "Neptune"], "signs": ["Pisces", "Cancer"], "themes": ["divine-feminine-salvation", "mystery-initiation"]}}
})
sort_order += 1

# L3 meta
ga_items.append({
    "id": "meta-transformation",
    "name": "Metamorphosis: The Body Knows What the Mind Forgets",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "The Golden Ass is the only complete Latin novel to survive from antiquity — and it is about transformation. Lucius, curious about magic, is turned into a donkey and must endure every form of human cruelty and comedy before being saved by Isis. Inside this frame, the tale of Cupid and Psyche tells the same story in mythic register: the soul, curious about the face of love, must descend to the underworld before being reunited with desire. Both stories say: you cannot know love, or truth, or the divine, without first being transformed into something you did not choose to be. The body of the ass is not punishment — it is education. The darkness in which Psyche loves Cupid is not ignorance — it is trust. Transformation precedes knowledge.",
        "Contemplation": "What are you becoming that you did not choose? What animal body has your curiosity earned you? And is there, somewhere ahead, a procession of roses?"
    },
    "keywords": ["metamorphosis", "transformation", "curiosity", "redemption"],
    "composite_of": ["cycle-cupid-psyche", "cycle-isis"],
    "relationship_type": "emergence",
    "metadata": {}
})

# Build Golden Ass grammar
ga_grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Apuleius", "date": "c. 170 CE", "note": "Original Latin text (Metamorphoses / Asinus Aureus)"},
            {"name": "William Adlington (translator)", "date": "1566", "note": "First English translation"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, astrology, meta interpretation"}
        ]
    },
    "name": "The Golden Ass (Metamorphoses)",
    "description": "The only complete Latin novel surviving from antiquity — Apuleius's tale of Lucius, transformed into a donkey by misadventure with magic, who endures every form of human cruelty and comedy before being saved by the goddess Isis. At its center: the tale of Cupid and Psyche, the original Beauty and the Beast, Jung's favorite myth of the soul's journey to love. William Adlington's Elizabethan translation (1566).\n\nSource: Project Gutenberg eBook #1666 (https://www.gutenberg.org/ebooks/1666).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: William Morris and Edward Burne-Jones illustrations for the Kelmscott Press Cupid and Psyche (1897). Raphael's Loggia paintings of Cupid and Psyche (1518). Antonio Canova's sculptures of Psyche. Classical Roman frescoes from Pompeii.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["apuleius", "golden-ass", "cupid-psyche", "roman", "metamorphosis", "isis", "fairy-tale"],
    "roots": ["mysticism", "western-philosophy"],
    "shelves": ["wisdom", "wonder"],
    "lineages": ["Shrei"],
    "worldview": "devotional",
    "items": ga_items
}

os.makedirs("grammars/golden-ass-apuleius", exist_ok=True)
with open("grammars/golden-ass-apuleius/grammar.json", "w") as f:
    json.dump(ga_grammar, f, indent=2, ensure_ascii=False)

ids = [i["id"] for i in ga_items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in ga_items for r in i.get("composite_of", []) if r not in ids]
print(f"Golden Ass: {len(ga_items)} items, L1={sum(1 for i in ga_items if i['level']==1)}, L2={sum(1 for i in ga_items if i['level']==2)}, L3={sum(1 for i in ga_items if i['level']==3)}")
print(f"  Dupes: {dupes}, Bad refs: {bad_refs}")

# ═══════════════════════════════════════════════════════════════════════════
# MABINOGION
# ═══════════════════════════════════════════════════════════════════════════

with open("seeds/mabinogion.txt", encoding="utf-8") as f:
    mab_text = f.read()

mab_start = mab_text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
if mab_start < 0:
    mab_start = mab_text.find("*** START OF THIS PROJECT GUTENBERG EBOOK")
if mab_start < 0:
    # Try another marker
    mab_start = 0
mab_start = mab_text.find("\n", mab_start) + 1
mab_end = mab_text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
if mab_end < 0:
    mab_end = mab_text.find("*** END OF THIS PROJECT GUTENBERG EBOOK")
if mab_end < 0:
    mab_end = len(mab_text)
mab_body = mab_text[mab_start:mab_end].strip()
mab_lines = mab_body.split("\n")

# Find story headings from TOC
STORIES = [
    ("The Lady of the Fountain", "lady-fountain", "The Lady of the Fountain"),
    ("Peredur the Son of Evrawc", "peredur", "Peredur the Son of Evrawc"),
    ("Geraint the son of Erbin", "geraint", "Geraint the Son of Erbin"),
    ("Kilhwch and Olwen", "kilhwch-olwen", "Kilhwch and Olwen"),
    ("The dream of Rhonabwy", "dream-rhonabwy", "The Dream of Rhonabwy"),
    ("Pwyll Prince of Dyved", "pwyll", "Pwyll, Prince of Dyved"),
    ("Branwen the daughter of Llyr", "branwen", "Branwen the Daughter of Llyr"),
    ("Manawyddan the son of Llyr", "manawyddan", "Manawyddan the Son of Llyr"),
    ("Math the son of Mathonwy", "math", "Math the Son of Mathonwy"),
    ("The dream of Maxen Wledig", "dream-maxen", "The Dream of Maxen Wledig"),
    ("HERE IS THE STORY OF LLUDD AND LLEVELYS", "lludd-llevelys", "The Story of Lludd and Llevelys"),
    ("Taliesin", "taliesin", "Taliesin"),
]

mab_positions = []
for heading, sid, name in STORIES:
    for i, line in enumerate(mab_lines):
        # Match heading at start of a line after the TOC
        if line.strip() == heading and i > 100:
            mab_positions.append((i, heading, sid, name))
            break
    else:
        # Try case-insensitive
        for i, line in enumerate(mab_lines):
            if line.strip().lower() == heading.lower() and i > 100:
                mab_positions.append((i, heading, sid, name))
                break
        else:
            print(f"WARNING (Mab): Could not find '{heading}'")

mab_positions.sort(key=lambda x: x[0])
print(f"\nMabinogion: found {len(mab_positions)} stories")

mab_items = []
sort_order = 1

# Astrology for Mabinogion stories
mab_astrology = {
    "lady-fountain": {"planets": ["Neptune", "Moon"], "signs": ["Pisces", "Cancer"], "themes": ["enchanted-fountain", "otherworld"]},
    "peredur": {"planets": ["Mars", "Moon"], "signs": ["Aries", "Scorpio"], "themes": ["grail-quest", "innocence", "blood"]},
    "geraint": {"planets": ["Mars", "Venus"], "signs": ["Aries", "Libra"], "themes": ["honor", "marriage", "jealousy"]},
    "kilhwch-olwen": {"planets": ["Mars", "Venus"], "signs": ["Aries", "Taurus"], "themes": ["impossible-tasks", "giant", "love-quest"]},
    "dream-rhonabwy": {"planets": ["Neptune", "Saturn"], "signs": ["Pisces"], "themes": ["vision", "arthur", "past"]},
    "pwyll": {"planets": ["Pluto", "Jupiter"], "signs": ["Scorpio", "Sagittarius"], "themes": ["otherworld-king", "exchange", "sovereignty"]},
    "branwen": {"planets": ["Moon", "Mars"], "signs": ["Cancer", "Aries"], "themes": ["grief", "war", "cauldron-of-rebirth"]},
    "manawyddan": {"planets": ["Saturn", "Mercury"], "signs": ["Capricorn", "Gemini"], "themes": ["enchantment", "patience", "craft"]},
    "math": {"planets": ["Moon", "Mercury", "Pluto"], "signs": ["Cancer", "Gemini", "Scorpio"], "themes": ["shapeshifting", "flowers-to-woman", "punishment"]},
    "dream-maxen": {"planets": ["Neptune", "Sun"], "signs": ["Pisces", "Leo"], "themes": ["vision", "imperial-destiny", "dream-wife"]},
    "lludd-llevelys": {"planets": ["Mercury", "Jupiter"], "signs": ["Gemini", "Sagittarius"], "themes": ["three-plagues", "wisdom", "sovereignty"]},
    "taliesin": {"planets": ["Mercury", "Moon", "Pluto"], "signs": ["Gemini", "Cancer", "Scorpio"], "themes": ["cauldron", "shapeshifting", "poetic-inspiration"]},
}

for idx, (start_ln, heading, sid, name) in enumerate(mab_positions):
    end_ln = mab_positions[idx+1][0] if idx+1 < len(mab_positions) else len(mab_lines)
    content = []
    started = False
    for j in range(start_ln + 1, end_ln):
        line = mab_lines[j]
        if not started and line.strip() == "":
            continue
        started = True
        content.append(line.rstrip())
    while content and content[-1].strip() == "":
        content.pop()
    full_text = "\n".join(content)
    excerpt = truncate(full_text)

    metadata = {"origin": "Welsh/Celtic"}
    if sid in mab_astrology:
        metadata["astrology"] = mab_astrology[sid]

    mab_items.append({
        "id": sid,
        "name": name,
        "sort_order": sort_order,
        "category": "tales",
        "level": 1,
        "sections": {"Text": excerpt},
        "keywords": ["mabinogion", "welsh", "celtic", "arthurian"],
        "metadata": metadata
    })
    sort_order += 1

# L2: The Four Branches
mab_items.append({
    "id": "group-four-branches",
    "name": "The Four Branches of the Mabinogi",
    "sort_order": sort_order,
    "category": "groups",
    "level": 2,
    "sections": {
        "About": "The Four Branches of the Mabinogi — Pwyll, Branwen, Manawyddan, and Math — are the oldest Welsh prose tales, written down in the 12th-13th centuries but drawing on much older oral traditions. They form a loose cycle centered on the family of Llyr and the children of Dôn, moving between the human world and the Otherworld (Annwn). Themes: sovereignty and its obligations, shapeshifting and transformation, the cauldron of rebirth, women as agents of fate. These are the source texts for the Fisher King and Taliesin myths referenced in the Myths Through Many Eyes grammar.",
        "For Readers": "Read these four tales in order — they form a single arc from Pwyll's descent into Annwn through to Math's magical punishments. Notice the cauldron (it appears in Branwen — a cauldron that resurrects the dead), the shapeshifting (Math transforms his nephews into animals as punishment), and the sovereignty theme (the land's health depends on the ruler's virtue)."
    },
    "keywords": ["four-branches", "mabinogi", "welsh", "otherworld"],
    "composite_of": ["pwyll", "branwen", "manawyddan", "math"],
    "relationship_type": "emergence",
    "metadata": {}
})
sort_order += 1

# L2: Arthurian romances
mab_items.append({
    "id": "group-arthurian",
    "name": "The Welsh Arthurian Romances",
    "sort_order": sort_order,
    "category": "groups",
    "level": 2,
    "sections": {
        "About": "Three tales — The Lady of the Fountain, Peredur, and Geraint — that parallel the French romances of Chrétien de Troyes but preserve older, wilder elements. The Lady of the Fountain is the Welsh Ywain; Peredur is the Welsh Perceval (and contains a version of the Grail scene); Geraint is the Welsh Erec. Kilhwch and Olwen, the oldest Arthurian prose tale, contains the most archaic Arthur — not a chivalric king but a wild hunter-chieftain whose court includes men who can hear ants stirring fifty miles away.",
        "For Readers": "These are not medieval romances but something older and stranger. Pay attention to the lists — Kilhwch's invocation of Arthur's court names over 200 heroes, many of them magical. Peredur's Grail scene is not a chalice but a severed head on a platter. The Lady of the Fountain's magic ring makes you invisible. This is the deep Celtic stratum beneath the polished French surface."
    },
    "keywords": ["arthurian", "welsh", "grail", "romance"],
    "composite_of": ["lady-fountain", "peredur", "geraint", "kilhwch-olwen"],
    "relationship_type": "emergence",
    "metadata": {}
})
sort_order += 1

# L3 meta
mab_items.append({
    "id": "meta-welsh-otherworld",
    "name": "The Welsh Otherworld: Where the Veil Is Thin",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "The Mabinogion is the gateway to the Celtic mythic imagination — a world where the boundary between this world and the Otherworld (Annwn) is thin as mist, where kings exchange shapes with their doubles, where a woman made of flowers becomes an owl, and where the severed head of Brân the Blessed continues to feast and talk for eighty years. This is the tradition that fed the Arthurian romances, the Grail quest, and — through the tale of Taliesin — the entire Western tradition of poetic inspiration as a divine gift earned through transformation. Shaw and Campbell both drew from this well: the cauldron of Ceridwen, the Wasteland of the Fisher King, the shapeshifting that earns wisdom.",
        "Contemplation": "The Welsh poets said that the Otherworld is not elsewhere — it is here, seen differently. Not a place you travel to but a way of perceiving the place you are in. Where in your ordinary world does the veil feel thin?"
    },
    "keywords": ["otherworld", "annwn", "welsh", "celtic", "veil", "transformation"],
    "composite_of": ["group-four-branches", "group-arthurian"],
    "relationship_type": "emergence",
    "metadata": {}
})

mab_grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Lady Charlotte Guest (translator)", "date": "1838-1849", "note": "First English translation of the Mabinogion"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, astrology, groupings"}
        ]
    },
    "name": "The Mabinogion",
    "description": "The great collection of Welsh mythology and romance — twelve tales drawn from the Red Book of Hergest and the White Book of Rhydderch (13th-14th century manuscripts preserving much older oral traditions). Contains the Four Branches of the Mabinogi (the oldest Welsh mythic cycle), the Welsh Arthurian romances (including the earliest prose Grail story), and the tale of Taliesin's transformation. The gateway to the Celtic Otherworld.\n\nSource: Project Gutenberg. Lady Charlotte Guest translation (1838-1849).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Alan Lee's Mabinogion illustrations (check copyright). Arthur Rackham's Celtic mythology illustrations. Edward Burne-Jones's tapestries of the Holy Grail. Medieval Welsh manuscript illuminations from the Red Book of Hergest.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["welsh", "celtic", "mabinogion", "arthurian", "grail", "otherworld", "mythology"],
    "roots": ["mysticism", "oral-tradition"],
    "shelves": ["wisdom", "wonder"],
    "lineages": ["Shrei", "Akomolafe"],
    "worldview": "animist",
    "items": mab_items
}

os.makedirs("grammars/mabinogion", exist_ok=True)
with open("grammars/mabinogion/grammar.json", "w") as f:
    json.dump(mab_grammar, f, indent=2, ensure_ascii=False)

ids = [i["id"] for i in mab_items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = [(i["id"], r) for i in mab_items for r in i.get("composite_of", []) if r not in ids]
print(f"Mabinogion: {len(mab_items)} items, L1={sum(1 for i in mab_items if i['level']==1)}, L2={sum(1 for i in mab_items if i['level']==2)}, L3={sum(1 for i in mab_items if i['level']==3)}")
print(f"  Dupes: {dupes}, Bad refs: {bad_refs}")
