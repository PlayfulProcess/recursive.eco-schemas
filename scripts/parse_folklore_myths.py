#!/usr/bin/env python3
"""
Parse four mythology/folklore seed files into grammar.json files:
1. Hero-Myths & Legends of the British Race (Ebbutt, Gutenberg #25502)
2. Tibetan Tales, Derived from Indian Sources (Schiefner/Ralston, Gutenberg #66870)
3. Folk Tales from Tibet (O'Connor, Gutenberg #75000)
4. Myths and Legends of Ancient Egypt (Spence, Gutenberg #43662)
"""
import json, re, os, sys


def read_seed(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    # Find Gutenberg body boundaries
    start = end = None
    for i, line in enumerate(lines):
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in line:
            start = i + 1
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line:
            end = i
    if start is None or end is None:
        raise ValueError(f"Could not find Gutenberg markers in {path}")
    return lines, start, end


def truncate_text(text, max_chars=2800):
    text = text.strip()
    if len(text) <= max_chars:
        return text
    bp = text.rfind(".", 0, max_chars)
    if bp == -1:
        bp = max_chars
    remaining_words = len(text[bp+1:].split())
    return text[:bp+1] + f" [Text continues for approximately {remaining_words} more words...]"


def make_id(text):
    """Convert a title to a lowercase-hyphenated ID."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text[:60]


def clean_text(text):
    """Clean extracted text: strip footnote markers, [Illustration] blocks, excess whitespace."""
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def build_grammar(name, description, tags, roots, shelves, lineages, worldview,
                  attribution, items, grammar_type="custom"):
    return {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": attribution
        },
        "name": name,
        "description": description,
        "grammar_type": grammar_type,
        "creator_name": "PlayfulProcess",
        "tags": tags,
        "roots": roots,
        "shelves": shelves,
        "lineages": lineages,
        "worldview": worldview,
        "items": items
    }


def write_grammar(output_dir, grammar):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "grammar.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {path} ({len(grammar['items'])} items)")
    return path


def validate_grammar(path):
    with open(path) as f:
        g = json.load(f)
    items = g['items']
    ids = [i['id'] for i in items]
    dupes = list(set(x for x in ids if ids.count(x) > 1))
    bad_refs = [(i['id'], r) for i in items for r in i.get('composite_of', []) if r not in ids]
    orders = [i['sort_order'] for i in items]
    l1 = sum(1 for i in items if i['level'] == 1)
    l2 = sum(1 for i in items if i['level'] == 2)
    l3 = sum(1 for i in items if i['level'] == 3)
    sections = sum(len(i.get('sections', {})) for i in items)
    seq = orders == list(range(1, len(items) + 1))
    print(f"  Items: {len(items)}, L1: {l1}, L2: {l2}, L3: {l3}, Sections: {sections}")
    print(f"  Duplicate IDs: {dupes}")
    print(f"  Bad refs: {bad_refs}")
    print(f"  Sort orders sequential: {seq}")
    if dupes or bad_refs or not seq:
        print("  *** VALIDATION FAILED ***")
        return False
    return True


# =============================================================================
# 1. HERO-MYTHS & LEGENDS OF THE BRITISH RACE
# =============================================================================
def parse_hero_myths_british():
    print("\n=== Hero-Myths & Legends of the British Race ===")
    lines, body_start, body_end = read_seed("seeds/hero-myths-british.txt")

    # Find chapters: CHAPTER I: BEOWULF etc.
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC]+):\s+(.+)$')
    chapters = []
    for i in range(body_start, body_end):
        m = chapter_pattern.match(lines[i].strip())
        if m:
            chapters.append((i, m.group(1), m.group(2).strip()))

    print(f"  Found {len(chapters)} chapters")

    # Find GLOSSARY AND INDEX to stop before it
    glossary_line = body_end
    for i in range(body_start, body_end):
        if lines[i].strip() == "GLOSSARY AND INDEX":
            glossary_line = i
            break

    # Extract chapter texts
    l1_items = []
    for idx, (start_ln, roman, title) in enumerate(chapters):
        end_ln = chapters[idx + 1][0] if idx + 1 < len(chapters) else glossary_line

        content_lines = []
        for j in range(start_ln + 1, end_ln):
            content_lines.append(lines[j].rstrip())

        text = clean_text("\n".join(content_lines))
        text = truncate_text(text)

        cid = make_id(title)
        l1_items.append({
            "id": cid,
            "name": title.title() if title == title.upper() else title,
            "sort_order": 0,
            "category": "legends",
            "level": 1,
            "sections": {
                "Story": text
            },
            "keywords": [w.lower() for w in title.split()[:4] if len(w) > 2],
            "metadata": {"chapter": roman}
        })

    # L2: Group by cultural cycle
    GROUPS = {
        "anglo-saxon-legends": {
            "name": "Anglo-Saxon Legends",
            "ids": ["beowulf", "havelok-the-dane", "hereward-the-wake"],
            "about": "Stories from the Anglo-Saxon tradition, featuring warrior heroes who embody the ideals of loyalty, courage, and duty that defined early English culture.",
            "keywords": ["anglo-saxon", "warriors", "england"]
        },
        "celtic-legends": {
            "name": "Celtic Legends",
            "ids": ["the-dream-of-maxen-wledig", "cuchulain-the-champion-of-ireland",
                     "the-marriage-of-sir-gawayne", "black-colin-of-loch-awe",
                     "the-countess-cathleen"],
            "about": "Tales from the Celtic world — Welsh, Irish, and Scottish — where the supernatural and human realms intertwine freely.",
            "keywords": ["celtic", "ireland", "wales", "scotland"]
        },
        "christian-roman-legends": {
            "name": "Christian & Roman-British Legends",
            "ids": ["the-story-of-constantine-and-elene", "the-compassion-of-constantine"],
            "about": "Legends where Roman imperial history meets Christian miracle, reflecting the Christianization of Britain.",
            "keywords": ["constantine", "christian", "roman"]
        },
        "norman-medieval-legends": {
            "name": "Norman & Medieval Legends",
            "ids": ["roland-the-hero-of-early-france", "the-tale-of-gamelyn",
                     "william-of-cloudeslee", "king-horn"],
            "about": "Stories of the High Middle Ages — outlaws, knights, and kings — where personal honour and feudal loyalty are tested.",
            "keywords": ["medieval", "norman", "chivalry"]
        },
        "outlaw-legends": {
            "name": "Outlaw Legends",
            "ids": ["robin-hood", "howard-the-halt"],
            "about": "Heroes who live outside the law, using cunning and courage to right wrongs and protect the vulnerable.",
            "keywords": ["outlaw", "robin-hood", "justice"]
        }
    }

    # Build actual ID list from what we parsed
    parsed_ids = [item['id'] for item in l1_items]

    l2_items = []
    for group_id, group in GROUPS.items():
        valid_refs = [rid for rid in group['ids'] if rid in parsed_ids]
        if not valid_refs:
            # Try partial matching
            for target_id in group['ids']:
                for pid in parsed_ids:
                    if target_id in pid or pid in target_id:
                        valid_refs.append(pid)
        valid_refs = list(dict.fromkeys(valid_refs))  # dedupe preserving order
        if valid_refs:
            l2_items.append({
                "id": group_id,
                "name": group['name'],
                "sort_order": 0,
                "category": "cultural-cycles",
                "level": 2,
                "sections": {
                    "About": group['about'],
                    "For Readers": "These stories can be read individually or as a cycle. Look for recurring themes of loyalty, sacrifice, and the relationship between mortal heroes and the supernatural world."
                },
                "composite_of": valid_refs,
                "relationship_type": "emergence",
                "keywords": group['keywords'],
                "metadata": {}
            })

    # L3 meta
    l3_item = {
        "id": "british-heroic-tradition",
        "name": "The British Heroic Tradition",
        "sort_order": 0,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "The full sweep of British heroic legend, from Anglo-Saxon warriors through Celtic myth to medieval outlaws. These stories span nearly a thousand years and weave together Germanic, Celtic, Norman, and Christian traditions into the fabric of British identity.",
            "For Readers": "Read across cultural cycles to see how the idea of heroism evolves — from Beowulf's monster-slaying to Robin Hood's social justice. Each era redefines what it means to be a hero."
        },
        "composite_of": [g for g in GROUPS.keys()],
        "relationship_type": "emergence",
        "keywords": ["british", "heroism", "mythology", "legends"],
        "metadata": {}
    }

    all_items = l1_items + l2_items + [l3_item]
    for i, item in enumerate(all_items):
        item['sort_order'] = i + 1

    grammar = build_grammar(
        name="Hero-Myths & Legends of the British Race",
        description="Sixteen hero-legends from across the British Isles, retold by M. I. Ebbutt (1910). From the Anglo-Saxon Beowulf to Celtic Cuchulain to Robin Hood, these tales trace the evolution of British heroic ideals across a thousand years.\n\nSource: Project Gutenberg eBook #25502 (https://www.gutenberg.org/ebooks/25502)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: J. H. F. Bacon A.R.A., Byam Shaw, W. H. Margetson R.I., Gertrude Demain Hammond — original illustrations from the 1910 George G. Harrap & Company edition.",
        tags=["mythology", "british", "legends", "heroes", "celtic", "anglo-saxon"],
        roots=["western-mythology"],
        shelves=["wonder"],
        lineages=["Akomolafe"],
        worldview="animist",
        attribution=[{
            "name": "M. I. Ebbutt",
            "date": "1910",
            "note": "Hero-Myths & Legends of the British Race, George G. Harrap & Co. Project Gutenberg eBook #25502."
        }],
        items=all_items
    )

    path = write_grammar("grammars/hero-myths-british", grammar)
    validate_grammar(path)


# =============================================================================
# 2. TIBETAN TALES, DERIVED FROM INDIAN SOURCES
# =============================================================================
def parse_tibetan_tales():
    print("\n=== Tibetan Tales, Derived from Indian Sources ===")
    lines, body_start, body_end = read_seed("seeds/tibetan-tales.txt")

    # Chapters are roman numerals on their own line, followed by blank + TITLE [nn]
    chapter_pattern = re.compile(r'^([IVXLC]+)\.$')

    # Find NOTES section to stop before it
    notes_line = body_end
    for i in range(body_start, body_end):
        if lines[i].strip() == "NOTES" and i > 13000:
            notes_line = i
            break

    # Skip the INTRODUCTION - find the first chapter marker after "TIBETAN TALES."
    tales_start = body_start
    for i in range(body_start, body_end):
        if lines[i].strip() == "TIBETAN TALES.":
            tales_start = i
            break

    chapters = []
    for i in range(tales_start, notes_line):
        m = chapter_pattern.match(lines[i].strip())
        if m:
            roman = m.group(1)
            # Next non-blank line is the title
            title = ""
            for j in range(i + 1, min(i + 5, notes_line)):
                if lines[j].strip():
                    title = lines[j].strip()
                    title = re.sub(r'\s*\[\d+\]', '', title)  # strip footnote refs
                    break
            if title:
                chapters.append((i, roman, title))

    print(f"  Found {len(chapters)} tales")

    # The TOC lists 50 tales; let's verify
    # Extract chapter texts
    l1_items = []
    for idx, (start_ln, roman, title) in enumerate(chapters):
        end_ln = chapters[idx + 1][0] if idx + 1 < len(chapters) else notes_line

        content_lines = []
        # Skip the roman numeral line and the title line
        skip_count = 0
        for j in range(start_ln, end_ln):
            stripped = lines[j].strip()
            if skip_count < 3 and (stripped == "" or stripped == f"{roman}." or stripped == title or re.match(r'^' + re.escape(title), stripped)):
                skip_count += 1
                continue
            content_lines.append(lines[j].rstrip())

        text = clean_text("\n".join(content_lines))
        text = truncate_text(text)

        cid = make_id(title)
        if not cid:
            cid = f"tale-{roman.lower()}"

        # Avoid duplicate IDs
        existing_ids = [item['id'] for item in l1_items]
        if cid in existing_ids:
            cid = f"{cid}-{roman.lower()}"

        l1_items.append({
            "id": cid,
            "name": title.title() if title == title.upper() else title,
            "sort_order": 0,
            "category": "tales",
            "level": 1,
            "sections": {
                "Story": text
            },
            "keywords": [w.lower() for w in title.split()[:4] if len(w) > 2],
            "metadata": {"chapter": roman}
        })

    # L2: Group by theme
    parsed_ids = [item['id'] for item in l1_items]

    # Identify groups by content type
    GROUPS = {
        "royal-tales": {
            "name": "Royal Tales & Jatakas",
            "pattern": ["king", "prince", "kua", "mandh", "jataka", "vivaara", "jvaka"],
            "about": "Stories of kings, princes, and past lives of the Buddha, drawn from the Jataka tradition. These tales explore sovereignty, duty, and the karmic consequences of royal power.",
            "keywords": ["kings", "royalty", "jataka", "karma"]
        },
        "virtue-tales": {
            "name": "Tales of Virtue & Devotion",
            "pattern": ["virtuous", "grateful", "faithful", "prophecy", "punishment", "avarice", "love"],
            "about": "Stories that illustrate Buddhist moral teachings — generosity, gratitude, devotion, and the consequences of vice. Each tale carries a dharmic lesson.",
            "keywords": ["virtue", "devotion", "morality", "dharma"]
        },
        "animal-fables": {
            "name": "Animal Fables",
            "pattern": ["jackal", "monkey", "lion", "dog", "ox", "ass", "wolf", "sheep",
                        "otter", "elephant", "cat", "gazelle", "peacock", "crow", "pheasant",
                        "ichneumon", "mouse", "beast", "snake"],
            "about": "Animal fables in the tradition of the Panchatantra and Jataka tales. Animals speak, scheme, and teach — embodying human virtues and vices in fur and feather.",
            "keywords": ["animals", "fables", "panchatantra", "wisdom"]
        },
        "women-tales": {
            "name": "Tales of Remarkable Women",
            "pattern": ["viakh", "utpala", "kri", "gaut", "suro", "woman", "bhadr"],
            "about": "Stories centered on women — devoted wives, wise mothers, and enlightened nuns. These tales from the Kah-gyur highlight feminine wisdom and spiritual attainment.",
            "keywords": ["women", "devotion", "wisdom", "enlightenment"]
        },
        "trickster-tales": {
            "name": "Trickster & Wit Tales",
            "pattern": ["thief", "clever", "actor", "cripple", "magician", "overreach", "dumb", "artist", "anecdote"],
            "about": "Stories of cunning, deception, and wit. Thieves outwit authorities, actors play tricks, and cleverness is both celebrated and cautioned against.",
            "keywords": ["trickster", "cunning", "wit", "deception"]
        }
    }

    l2_items = []
    assigned = set()
    for group_id, group in GROUPS.items():
        refs = []
        for item in l1_items:
            item_text = (item['id'] + " " + item['name']).lower()
            if any(p in item_text for p in group['pattern']) and item['id'] not in assigned:
                refs.append(item['id'])
                assigned.add(item['id'])
        if refs:
            l2_items.append({
                "id": group_id,
                "name": group['name'],
                "sort_order": 0,
                "category": "thematic-groups",
                "level": 2,
                "sections": {
                    "About": group['about'],
                    "For Readers": "These tales can be read individually or as a thematic collection. Look for recurring motifs and moral patterns that connect them."
                },
                "composite_of": refs,
                "relationship_type": "emergence",
                "keywords": group['keywords'],
                "metadata": {}
            })

    # Catch any unassigned items into a miscellaneous group
    unassigned = [item['id'] for item in l1_items if item['id'] not in assigned]
    if unassigned:
        l2_items.append({
            "id": "miscellaneous-tales",
            "name": "Other Tales",
            "sort_order": 0,
            "category": "thematic-groups",
            "level": 2,
            "sections": {
                "About": "Additional tales from the Kah-gyur that weave together themes of human nature, moral consequence, and the interplay of worldly and spiritual life.",
                "For Readers": "Each tale stands alone as a complete story, often with a pointed moral or unexpected twist."
            },
            "composite_of": unassigned,
            "relationship_type": "emergence",
            "keywords": ["tales", "miscellaneous", "tibetan"],
            "metadata": {}
        })

    # L3
    l3_item = {
        "id": "tibetan-tales-collection",
        "name": "Tibetan Tales from the Kah-Gyur",
        "sort_order": 0,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Fifty tales translated from the Tibetan Kah-gyur (the 'Translated Word' of the Buddha), themselves derived from Sanskrit originals. These stories — Jatakas, animal fables, moral tales, and legends — form part of the vast Buddhist narrative tradition that travelled from India to Tibet along the Silk Road.",
            "For Readers": "Read these tales as windows into the Buddhist moral universe. Whether featuring kings or jackals, devoted wives or cunning thieves, each story illuminates a facet of dharma — karma, compassion, wisdom, and the consequences of action."
        },
        "composite_of": [item['id'] for item in l2_items],
        "relationship_type": "emergence",
        "keywords": ["tibetan", "buddhist", "kah-gyur", "jataka"],
        "metadata": {}
    }

    all_items = l1_items + l2_items + [l3_item]
    for i, item in enumerate(all_items):
        item['sort_order'] = i + 1

    grammar = build_grammar(
        name="Tibetan Tales, Derived from Indian Sources",
        description="Fifty tales from the Tibetan Kah-gyur, translated by F. Anton von Schiefner and rendered into English by W. R. S. Ralston (1906). Jataka tales, animal fables, stories of kings and saints — the Buddhist narrative tradition as it travelled from India to Tibet.\n\nSource: Project Gutenberg eBook #66870 (https://www.gutenberg.org/ebooks/66870)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: No illustrations in the original edition. Tibetan thangka painting traditions and Indian Jataka relief carvings from Sanchi, Bharhut, and Ajanta would provide appropriate visual companions.",
        tags=["tibet", "folk-tales", "buddhism", "india", "fables"],
        roots=["eastern-wisdom", "buddhism"],
        shelves=["wonder"],
        lineages=["Shrei"],
        worldview="animist",
        attribution=[{
            "name": "F. Anton von Schiefner (translator from Tibetan)",
            "date": "1882",
            "note": "Tibetan Tales, Derived from Indian Sources, translated from the Kah-gyur."
        }, {
            "name": "W. R. S. Ralston (English translator)",
            "date": "1906",
            "note": "English translation from Schiefner's German. Project Gutenberg eBook #66870."
        }],
        items=all_items
    )

    path = write_grammar("grammars/tibetan-tales", grammar)
    validate_grammar(path)


# =============================================================================
# 3. FOLK TALES FROM TIBET
# =============================================================================
def parse_folk_tales_tibet():
    print("\n=== Folk Tales from Tibet ===")
    lines, body_start, body_end = read_seed("seeds/folk-tales-tibet.txt")

    # Stories are marked: STORY No. I. / STORY No. II. etc.
    story_pattern = re.compile(r'^STORY No\.\s+([IVXLC]+)\.$')

    # Find NOTES/LOVE-SONGS to stop
    stop_line = body_end
    for i in range(body_start, body_end):
        if lines[i].strip() == "SOME VERSES FROM TIBETAN LOVE-SONGS.":
            stop_line = i
            break

    stories = []
    for i in range(body_start, stop_line):
        m = story_pattern.match(lines[i].strip())
        if m:
            roman = m.group(1)
            # Next non-blank line is the title (usually ALL CAPS)
            title = ""
            for j in range(i + 1, min(i + 5, stop_line)):
                stripped = lines[j].strip()
                if stripped and stripped != "":
                    title = stripped
                    # Remove trailing period
                    title = title.rstrip('.')
                    break
            if title:
                stories.append((i, roman, title))

    print(f"  Found {len(stories)} stories")

    l1_items = []
    for idx, (start_ln, roman, title) in enumerate(stories):
        end_ln = stories[idx + 1][0] if idx + 1 < len(stories) else stop_line

        content_lines = []
        skip = True
        for j in range(start_ln + 2, end_ln):  # skip STORY No. and title lines
            stripped = lines[j].strip()
            if skip and stripped == "":
                continue
            skip = False
            content_lines.append(lines[j].rstrip())

        text = clean_text("\n".join(content_lines))
        text = truncate_text(text)

        # Clean up title for display
        display_title = title.title() if title == title.upper() else title

        cid = make_id(title)
        if not cid:
            cid = f"story-{roman.lower()}"

        existing_ids = [item['id'] for item in l1_items]
        if cid in existing_ids:
            cid = f"{cid}-{roman.lower()}"

        l1_items.append({
            "id": cid,
            "name": display_title,
            "sort_order": 0,
            "category": "folk-tales",
            "level": 1,
            "sections": {
                "Story": text
            },
            "keywords": [w.lower() for w in title.split()[:4] if len(w) > 2],
            "metadata": {"story_number": roman}
        })

    # L2: Group by character type / theme
    parsed_ids = [item['id'] for item in l1_items]

    GROUPS = {
        "animal-tales": {
            "name": "Animal Tales",
            "pattern": ["hare", "tiger", "cat", "mice", "mouse", "fox", "wolf", "kyang",
                        "frog", "crow", "lion", "sheep", "lamb", "jackal", "monkey", "tortoise", "drake"],
            "about": "Tibetan animal tales where hares outwit tigers, wolves are fooled, and the natural world mirrors human society. The hare appears as a recurring trickster figure.",
            "keywords": ["animals", "trickster", "hare", "tibet"]
        },
        "human-tales": {
            "name": "Human Tales & Adventures",
            "pattern": ["boy", "prince", "man", "mussulman", "neighbour", "thief", "thieves",
                        "lama", "servant", "stone-lion", "stone lion", "home-bred", "room-bacha", "ogre",
                        "good-faith", "faith"],
            "about": "Stories of human characters — princes, servants, fools, and adventurers — navigating a world of magic, trickery, and moral consequence in traditional Tibet.",
            "keywords": ["adventure", "human", "tibet", "magic"]
        }
    }

    l2_items = []
    assigned = set()
    for group_id, group in GROUPS.items():
        refs = []
        for item in l1_items:
            item_text = (item['id'] + " " + item['name']).lower()
            if any(p in item_text for p in group['pattern']) and item['id'] not in assigned:
                refs.append(item['id'])
                assigned.add(item['id'])
        if refs:
            l2_items.append({
                "id": group_id,
                "name": group['name'],
                "sort_order": 0,
                "category": "thematic-groups",
                "level": 2,
                "sections": {
                    "About": group['about'],
                    "For Readers": "These tales were collected by Captain W. F. O'Connor during his time in Tibet (1904-1906), told by village headmen, monks, servants, and traders. Read them as living folklore, told around fires in a land of high plateaus and ancient monasteries."
                },
                "composite_of": refs,
                "relationship_type": "emergence",
                "keywords": group['keywords'],
                "metadata": {}
            })

    # Catch unassigned
    unassigned = [item['id'] for item in l1_items if item['id'] not in assigned]
    if unassigned:
        l2_items.append({
            "id": "other-folk-tales",
            "name": "Other Folk Tales",
            "sort_order": 0,
            "category": "thematic-groups",
            "level": 2,
            "sections": {
                "About": "Additional folk tales from Tibet that blend animal and human worlds, magic and morality.",
                "For Readers": "Each tale stands alone as a window into Tibetan folk imagination."
            },
            "composite_of": unassigned,
            "relationship_type": "emergence",
            "keywords": ["tibet", "folk-tales"],
            "metadata": {}
        })

    # L3
    l3_item = {
        "id": "folk-tales-tibet-collection",
        "name": "Folk Tales from Tibet",
        "sort_order": 0,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Twenty-two folk tales collected and translated by Captain W. F. O'Connor during the British Mission to Lhasa (1904). Told by village headmen, monks, servants, and traders across Tibet, these stories preserve the folk imagination of a people whose oral traditions were largely unknown to the outside world.",
            "For Readers": "These tales are windows into Tibetan folk culture at the turn of the twentieth century — a world of clever hares, magical princes, and moral lessons woven through with Buddhist sensibility and the dry humor of the high plateau."
        },
        "composite_of": [item['id'] for item in l2_items],
        "relationship_type": "emergence",
        "keywords": ["tibet", "folk-tales", "oral-tradition", "buddhism"],
        "metadata": {}
    }

    all_items = l1_items + l2_items + [l3_item]
    for i, item in enumerate(all_items):
        item['sort_order'] = i + 1

    grammar = build_grammar(
        name="Folk Tales from Tibet",
        description="Twenty-two folk tales collected and translated by Captain W. F. O'Connor during the British Mission to Lhasa (1904). Animal trickster tales, magical adventures, and moral fables from the oral tradition of Tibet.\n\nSource: Project Gutenberg eBook #75000 (https://www.gutenberg.org/ebooks/75000)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Original illustrations by an unnamed Tibetan artist resident at Gyantse, commissioned for the 1906 Hurst and Blackett edition. Traditional Tibetan folk art style.",
        tags=["tibet", "folk-tales", "buddhism", "children"],
        roots=["eastern-wisdom", "buddhism"],
        shelves=["wonder"],
        lineages=["Shrei"],
        worldview="animist",
        attribution=[{
            "name": "Captain W. F. O'Connor (collector and translator)",
            "date": "1906",
            "note": "Folk Tales from Tibet, Hurst and Blackett, London. Project Gutenberg eBook #75000."
        }],
        items=all_items
    )

    path = write_grammar("grammars/folk-tales-tibet", grammar)
    validate_grammar(path)


# =============================================================================
# 4. MYTHS AND LEGENDS OF ANCIENT EGYPT
# =============================================================================
def parse_myths_legends_egypt():
    print("\n=== Myths and Legends of Ancient Egypt ===")
    lines, body_start, body_end = read_seed("seeds/myths-legends-egypt-spence.txt")

    # Chapters: CHAPTER I: INTRODUCTORY, etc.
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC]+):\s+(.+)$')

    # Find GLOSSARY AND INDEX to stop
    glossary_line = body_end
    for i in range(body_start, body_end):
        if lines[i].strip() == "GLOSSARY AND INDEX" and i > 9000:
            glossary_line = i
            break

    chapters = []
    for i in range(body_start, glossary_line):
        m = chapter_pattern.match(lines[i].strip())
        if m:
            chapters.append((i, m.group(1), m.group(2).strip()))

    print(f"  Found {len(chapters)} chapters")

    l1_items = []
    for idx, (start_ln, roman, title) in enumerate(chapters):
        end_ln = chapters[idx + 1][0] if idx + 1 < len(chapters) else glossary_line

        content_lines = []
        for j in range(start_ln + 1, end_ln):
            content_lines.append(lines[j].rstrip())

        text = clean_text("\n".join(content_lines))
        text = truncate_text(text)

        cid = make_id(title)
        display_title = title.title() if title == title.upper() else title

        l1_items.append({
            "id": cid,
            "name": display_title,
            "sort_order": 0,
            "category": "chapters",
            "level": 1,
            "sections": {
                "Content": text
            },
            "keywords": [w.lower() for w in title.split()[:4] if len(w) > 2],
            "metadata": {"chapter": roman}
        })

    # L2: Group by subject matter
    GROUPS = {
        "history-and-context": {
            "name": "History & Context",
            "ids": ["introductory", "exploration-history-and-customs"],
            "about": "The historical and cultural foundation of ancient Egypt — its geography, peoples, customs, and the story of its modern rediscovery through archaeology and exploration.",
            "keywords": ["history", "egypt", "archaeology", "customs"]
        },
        "religion-and-ritual": {
            "name": "Religion & Ritual",
            "ids": ["the-priesthood-mysteries-and-temples", "the-cult-of-osiris",
                    "magic", "foreign-and-animal-gods-the-late-period"],
            "about": "The religious world of ancient Egypt — from the Osirian mysteries and temple rites to magical practices and the incorporation of foreign deities in the Late Period.",
            "keywords": ["religion", "osiris", "magic", "temples", "gods"]
        },
        "gods-and-literature": {
            "name": "Gods, Myths & Literature",
            "ids": ["the-great-gods", "egyptian-literature"],
            "about": "The great deities of Egypt — Ra, Isis, Thoth, Horus — and the rich literary tradition that preserved their myths, from the Pyramid Texts to the tales of the New Kingdom.",
            "keywords": ["gods", "myths", "literature", "ra", "isis"]
        },
        "art-culture": {
            "name": "Art & Material Culture",
            "ids": ["egyptian-art"],
            "about": "The artistic traditions of ancient Egypt — from the monumental architecture of the pyramids to the delicate beauty of tomb paintings and the symbolic language of hieroglyphic art.",
            "keywords": ["art", "architecture", "sculpture", "painting"]
        }
    }

    parsed_ids = [item['id'] for item in l1_items]

    l2_items = []
    for group_id, group in GROUPS.items():
        valid_refs = [rid for rid in group['ids'] if rid in parsed_ids]
        if not valid_refs:
            # Try partial matching
            for target_id in group['ids']:
                for pid in parsed_ids:
                    if target_id in pid or pid in target_id:
                        if pid not in valid_refs:
                            valid_refs.append(pid)
        if valid_refs:
            l2_items.append({
                "id": group_id,
                "name": group['name'],
                "sort_order": 0,
                "category": "thematic-groups",
                "level": 2,
                "sections": {
                    "About": group['about'],
                    "For Readers": "Read these chapters together to build a comprehensive picture of this aspect of Egyptian civilization. Cross-reference with other groups for deeper understanding."
                },
                "composite_of": valid_refs,
                "relationship_type": "emergence",
                "keywords": group['keywords'],
                "metadata": {}
            })

    # L3
    l3_item = {
        "id": "myths-legends-egypt-collection",
        "name": "Myths and Legends of Ancient Egypt",
        "sort_order": 0,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "Lewis Spence's comprehensive survey of Egyptian mythology, religion, and culture (1915), written in the light of modern comparative mythology. From the creation myths of Heliopolis to the magical papyri of the Late Period, this work traces the full arc of Egyptian sacred imagination.",
            "For Readers": "Use the thematic groups to navigate — begin with History & Context for grounding, explore the Gods and their myths, then delve into the ritual and magical dimensions. Spence writes as a mythologist, not just an Egyptologist, drawing connections to universal patterns in world mythology."
        },
        "composite_of": [item['id'] for item in l2_items],
        "relationship_type": "emergence",
        "keywords": ["egypt", "mythology", "gods", "ancient-religion"],
        "metadata": {}
    }

    all_items = l1_items + l2_items + [l3_item]
    for i, item in enumerate(all_items):
        item['sort_order'] = i + 1

    grammar = build_grammar(
        name="Myths and Legends of Ancient Egypt",
        description="Lewis Spence's survey of Egyptian mythology, religion, magic, and culture (1915). Nine chapters covering the gods, the Osirian mysteries, temple rites, magical practices, and Egyptian art — a comprehensive introduction to the sacred world of the Nile Valley.\n\nSource: Project Gutenberg eBook #43662 (https://www.gutenberg.org/ebooks/43662)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Evelyn Paul — colour plates for the 1915 David D. Nickerson & Company edition. Also: Egyptian tomb paintings, papyrus illustrations (Book of the Dead), and temple reliefs from Karnak, Luxor, and Abu Simbel.",
        tags=["egypt", "mythology", "gods", "creation-myth", "ancient-religion"],
        roots=["eastern-wisdom", "mysticism"],
        shelves=["wonder"],
        lineages=["Shrei"],
        worldview="animist",
        attribution=[{
            "name": "Lewis Spence",
            "date": "1915",
            "note": "Myths and Legends of Ancient Egypt, David D. Nickerson & Company, Boston. Project Gutenberg eBook #43662."
        }],
        items=all_items
    )

    path = write_grammar("grammars/myths-legends-egypt-spence", grammar)
    validate_grammar(path)


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    print("Parsing four mythology/folklore grammars...")
    parse_hero_myths_british()
    parse_tibetan_tales()
    parse_folk_tales_tibet()
    parse_myths_legends_egypt()
    print("\nDone!")
