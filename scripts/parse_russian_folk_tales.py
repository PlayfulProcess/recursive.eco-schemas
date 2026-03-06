#!/usr/bin/env python3
"""
Parse Russian Folk-Tales (Afanasyev/Magnus, Gutenberg #62509) into grammar.json.
73 tales organized into thematic L2 groups.
"""
import json, re, os

with open("seeds/russian-folk-tales.txt", encoding="utf-8") as f:
    lines = f.readlines()

# Find body start and end
body_start = None
body_end = None
for i, line in enumerate(lines):
    if i > 380 and line.strip() == "THE DUN COW":
        body_start = i
        break

for i, line in enumerate(lines):
    if line.strip() == "NOTES" and i > 11000:
        body_end = i
        break

print(f"Body: lines {body_start+1}-{body_end+1}")

# Extract all headings: centered, ALL CAPS, between blank lines
headings = []
i = body_start
while i < body_end:
    line = lines[i]
    stripped = line.strip()
    leading = len(line) - len(line.lstrip())

    # A heading is: heavily indented (>20 spaces), ALL CAPS, not a quote/song
    if (leading > 20 and stripped and
        len(stripped) > 2 and len(stripped) < 80 and
        not stripped.startswith('"') and
        not stripped.startswith("'") and
        not stripped.startswith("(") and
        not stripped.startswith("_") and
        'sleep' not in stripped.lower() and
        'awake' not in stripped.lower() and
        'pike' not in stripped.lower() and
        'pleasure' not in stripped.lower() and
        'work on your way' not in stripped.lower()):

        # Check if it's ALL CAPS (allowing accented chars and punctuation)
        alpha_chars = [c for c in stripped if c.isalpha()]
        if alpha_chars and all(c.isupper() or c in "ÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÄËÏÖÜÝÑ" or not c.isascii() for c in alpha_chars):
            # Check previous line is blank or near-blank
            prev = lines[i-1].strip() if i > 0 else ""
            if prev == "" or prev.startswith("---"):
                # Multi-line heading?
                full_heading = stripped
                # Check if next non-blank line is also a continuation
                j = i + 1
                while j < body_end and lines[j].strip() == "":
                    j += 1
                headings.append((i, full_heading))
    i += 1

print(f"Found {len(headings)} headings")

# Clean up: remove "RUSSIAN FOLK-TALES" if it snuck in
headings = [(ln, h) for ln, h in headings if h != "RUSSIAN FOLK-TALES"]

# Some headings have footnote markers like [21] - strip them
cleaned_headings = []
for ln, h in headings:
    h = re.sub(r'\[\d+\]', '', h).strip()
    cleaned_headings.append((ln, h))
headings = cleaned_headings

print(f"After cleanup: {len(headings)} headings")
for ln, h in headings[:10]:
    print(f"  {ln+1}: {h}")
print("  ...")
for ln, h in headings[-5:]:
    print(f"  {ln+1}: {h}")

# Extract text between headings
tales = []
for idx, (start_ln, heading) in enumerate(headings):
    # End is next heading or body_end
    end_ln = headings[idx + 1][0] if idx + 1 < len(headings) else body_end

    # Get text, skip the heading line and surrounding blanks
    content_lines = []
    started = False
    for j in range(start_ln + 1, end_ln):
        line = lines[j]
        if not started and line.strip() == "":
            continue
        started = True
        content_lines.append(line.rstrip())

    # Trim trailing blanks
    while content_lines and content_lines[-1].strip() == "":
        content_lines.pop()

    full_text = "\n".join(content_lines)

    # Generate ID from heading
    clean = heading.lower()
    clean = re.sub(r'[^a-z0-9\s]', '', clean)
    clean = re.sub(r'\s+', '-', clean.strip())
    if len(clean) > 40:
        clean = clean[:40].rsplit('-', 1)[0]

    # Handle duplicate IDs (3x "A Tale of the Dead")
    tale_id = clean

    # Truncate story to reasonable length
    if len(full_text) > 3000:
        bp = full_text.rfind(".", 0, 2800)
        if bp == -1:
            bp = 2800
        remaining = len(full_text[bp:].split())
        excerpt = full_text[:bp + 1] + f"\n\n[Story continues for approximately {remaining} more words...]"
    else:
        excerpt = full_text

    # Title case the heading for display
    display_name = heading.title()
    # Fix common title-case issues
    display_name = display_name.replace("And ", "and ").replace("The ", "the ").replace("Of ", "of ").replace("In ", "in ").replace("A ", "a ")
    display_name = display_name.replace("Who ", "who ").replace("How ", "how ")
    if display_name[0].islower():
        display_name = display_name[0].upper() + display_name[1:]

    tales.append({
        "heading": heading,
        "id": tale_id,
        "name": display_name,
        "text": excerpt,
        "word_count": len(full_text.split()),
    })

# Fix duplicate IDs
id_counts = {}
for t in tales:
    if t["id"] in id_counts:
        id_counts[t["id"]] += 1
        t["id"] = f"{t['id']}-{id_counts[t['id']]}"
    else:
        id_counts[t["id"]] = 1
# Also fix the first occurrence if there are dupes
for tid, count in id_counts.items():
    if count > 1:
        first = True
        for t in tales:
            if t["id"] == tid and first:
                t["id"] = f"{tid}-1"
                first = False

print(f"\nExtracted {len(tales)} tales")
for t in tales[:5]:
    print(f"  {t['id']}: {t['name']} ({t['word_count']} words)")

# ═══════════════════════════════════════════════════════════════════════════
# BUILD GRAMMAR ITEMS
# ═══════════════════════════════════════════════════════════════════════════

items = []
sort_order = 1

# Thematic categories for L2 grouping
THEME_MAP = {
    # Supernatural & Magic
    "supernatural": ["the-dun-cow", "a-tale-of-the-dead-1", "a-tale-of-the-dead-2",
                     "a-tale-of-the-dead-3", "the-midnight-dance", "vasilisa-the-fair",
                     "the-witch-and-the-sister-of-the-sun", "the-enchanted-tsarevich",
                     "the-snake-princess", "marya-morevna", "the-realm-of-stone"],
    # Tricksters & Clever Folk
    "tricksters": ["the-sorry-drunkard", "the-wolf-and-the-tailor", "donotknow",
                   "shemyak-the-judge", "the-potter", "nikita-the-tanner",
                   "at-the-behest-of-the-pike", "chufil-filyushka", "never-wash"],
    # Heroes & Knights
    "heroes": ["egori-the-brave-and-the-gipsy", "danilo-the-unfortunate",
               "the-foundling-prince", "ilya-muromets-and-svyatogor",
               "the-soldier-and-death", "the-soldier-and-the-tsar-in",
               "alyosha-popovich", "the-legless-knight-and-the-blind"],
    # Women's Tales
    "women": ["the-tale-of-the-silver-saucer-and", "baba-yaga-and-zamoryshek",
              "vasilisa-popovna", "the-princess-who-would-not-smile",
              "the-tsaritsa-harpist", "the-sea-tsar-and-vasilisa-the"],
    # Moral & Religious
    "moral": ["mark-the-rich", "by-command-of-the-prince-daniel",
              "the-thoughtless-word", "the-brother-of-christ",
              "gods-blessing-compasses-all-things", "a-story-of-saint-nicholas",
              "christ-and-the-geese", "christ-and-folk-songs",
              "the-journey-to-jerusalem", "elijah-the-prophet-and-st"],
    # Animal Tales
    "animals": ["the-bear-the-dog-and-the-cat", "the-language-of-the-birds",
                "the-animals-in-the-pit", "the-animals-winter-quarters"],
    # Family & Fate
    "family": ["the-miraculous-hen", "the-poor-widow", "the-dream",
               "the-tale-of-alexander-of-macedon", "the-tsarevich-and-dyadka",
               "prince-evstafi", "the-quarrelsome-wife", "iváshko-and-the-wise-woman",
               "sorrow", "beer-and-bread", "the-feast-of-the-dead",
               "the-story-of-tsar-angey-and-how"],
    # Nature & Place
    "nature": ["the-sun-and-how-it-was-made-by", "the-wood-sprite",
               "vazuza-and-volga", "the-sun-the-moon-and-crow-crowson",
               "the-princess-to-be-kissed-at-a",
               "the-realms-of-copper-silver-and",
               "the-singing-tree-and-the-speaking",
               "the-devil-in-the-dough-pan",
               "a-cure-for-story-telling"],
}

# Build L1 items
for t in tales:
    items.append({
        "id": t["id"],
        "name": t["name"],
        "sort_order": sort_order,
        "category": "tales",
        "level": 1,
        "sections": {
            "Story": t["text"]
        },
        "keywords": ["russian", "folk-tale", "afanasyev"],
        "metadata": {"origin": "Russian", "word_count": t["word_count"]}
    })
    sort_order += 1

# Assign tales to themes (best effort - some won't match due to ID generation)
all_ids = {i["id"] for i in items}

# Build L2 theme items
THEME_NAMES = {
    "supernatural": ("Supernatural and Enchantment", "Tales of witches, enchantments, the undead, and shape-shifting — the supernatural world that is never far from the Russian village. Bába Yagá and her hut on chicken legs. The beautiful Vasilísa with her magical doll. Enchanted tsareviches trapped in animal form. The dead who walk and dance at midnight. In Russian folk tradition, the boundary between the natural and supernatural is thin as birch bark."),
    "tricksters": ("Tricksters and Clever Folk", "The common people outwitting the powerful through cunning, laziness turned to advantage, and sheer audacity. The Russian trickster is not a mythological figure like Coyote or Anansi — he is a drunkard, a soldier, a peasant, a fool who turns out not to be foolish at all. These tales celebrate the intelligence of the powerless."),
    "heroes": ("Heroes and Bogatyrs", "The bogatyrs — heroic knights of Russian epic — and the soldiers, princes, and brave common folk who face impossible odds. Ilyá Múromets, who lay on the stove for thirty-three years before rising to become the greatest of Russian heroes. Egóri the Brave. The unnamed soldiers who outwit Death herself."),
    "women": ("Women of Power", "The women who drive these tales: Vasilísa the Fair with her magical doll, Vasilísa Popóvna who disguises as a warrior, the Tsarítsa Harpist, the Sea Tsar's wise daughter. Russian folk tales give women more agency than their Western European counterparts — they scheme, fight, shape-shift, and frequently rescue the men."),
    "moral": ("Saints, Sinners, and Judgment", "Tales with religious and moral dimensions — the saints who intervene, the sinners who are punished, the divine justice that operates through strange channels. These tales blend Christian theology with much older pagan wisdom, creating a uniquely Russian moral universe where Christ walks the fields and the devil hides in the dough-pan."),
    "animals": ("Animal Tales", "The animals of the Russian forest as characters: bears who are strong but foolish, foxes who are cunning, birds who speak the language of prophecy. These are the oldest layer of folk narrative — tales told before Christianity, before the tsars, when the forest was the only kingdom."),
    "family": ("Family, Fate, and Fortune", "Tales of family life — cruel stepmothers, devoted siblings, ungrateful children, wise fools. The domestic world of the Russian folk tale, where poverty is the common condition and fortune (good or bad) arrives unannounced. Sorrow personified follows a man through his life. A miraculous hen changes a family's fate. A dream foretells a future that cannot be avoided."),
    "nature": ("Nature, Place, and Cosmology", "Tales of the natural world and the forces that govern it: how the sun was made, why rivers flow where they do, the wood sprites who guard the forest. The Russian cosmological imagination, where landscape is alive and every natural feature has a story."),
}

for theme_id, (theme_name, theme_about) in THEME_NAMES.items():
    # Find matching tale IDs
    refs = [r for r in THEME_MAP.get(theme_id, []) if r in all_ids]
    # Also try partial matching for IDs that got truncated
    for map_id in THEME_MAP.get(theme_id, []):
        if map_id not in all_ids:
            # Try finding closest match
            for real_id in all_ids:
                if real_id.startswith(map_id[:15]):
                    if real_id not in refs:
                        refs.append(real_id)

    items.append({
        "id": f"theme-{theme_id}",
        "name": theme_name,
        "sort_order": sort_order,
        "category": "themes",
        "level": 2,
        "sections": {
            "About": theme_about,
            "For Readers": f"These tales share the theme of {theme_name.lower()}. Read them as a group to see how Russian folk imagination circles around the same ideas from different angles. Notice the recurring motifs: the number three (three tasks, three sons, three sisters), the forest as threshold between worlds, the transformation that reveals true nature."
        },
        "keywords": ["russian", "folk-tale", theme_id],
        "composite_of": refs,
        "relationship_type": "emergence",
        "metadata": {}
    })
    sort_order += 1

# L3 Meta
items.append({
    "id": "meta-russian-soul",
    "name": "The Russian Folk Soul",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "Seventy-three tales from the collection of Alexander Afanasyev — the Russian Grimm, who gathered these stories from across the Russian Empire in the mid-nineteenth century. This is the wild forest of Russian imagination: older than the tsars, older than Christianity (though it absorbed both), shaped by endless winters, vast distances, and the knowledge that the supernatural is never more than a footstep away. Bába Yagá guards the threshold between worlds. The dead dance at midnight. Animals speak truth that humans cannot. The bogatyrs ride out against impossible odds. The fool on the stove turns out to be the wisest of all. These tales were told by peasants to peasants, and their wisdom is the wisdom of people who have survived everything.",
        "Contemplation": "Which character are you in the folk tale of your own life right now? Are you the youngest son setting out with nothing? The enchanted prisoner waiting to be freed? The clever wife solving the puzzle the hero cannot? The fool on the stove, not yet ready to rise? The tale knows — and so do you, if you listen."
    },
    "keywords": ["russian", "folk-tale", "afanasyev", "soul", "collective"],
    "composite_of": [f"theme-{t}" for t in THEME_NAMES],
    "relationship_type": "emergence",
    "metadata": {}
})
sort_order += 1

# ═══════════════════════════════════════════════════════════════════════════
# BUILD GRAMMAR
# ═══════════════════════════════════════════════════════════════════════════

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "A. N. Afanasyev (collector)", "date": "1855-1867", "note": "Original Russian collection (Narodnye russkie skazki)"},
            {"name": "Leonard A. Magnus (translator)", "date": "1915", "note": "English translation"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, thematic groupings, and meta interpretation"}
        ]
    },
    "name": "Russian Folk-Tales",
    "description": f"Seventy-three Russian folk tales from the collection of Alexander Afanasyev, translated by Leonard A. Magnus (1915). The wild forest of Russian imagination: Bába Yagá and her hut on chicken legs, enchanted tsareviches, clever fools, heroic bogatyrs, talking animals, and the dead who dance at midnight. Organized into eight thematic groups from supernatural enchantment to animal tales to the cosmic stories of sun, moon, and river.\n\nSource: Project Gutenberg eBook #62509 (https://www.gutenberg.org/ebooks/62509).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Ivan Bilibin's illustrations for Russian fairy tales (1899-1902) — the definitive visual style. Viktor Vasnetsov's paintings of Russian folklore subjects (1880s-1920s). Elena Polenova's folk art illustrations. Palekh miniature lacquer box paintings of folk tale scenes.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["russian", "folk-tales", "fairy-tales", "afanasyev", "slavic", "baba-yaga", "bogatyr"],
    "roots": ["oral-tradition", "mysticism"],
    "shelves": ["wonder", "wisdom"],
    "lineages": ["Shrei", "Akomolafe"],
    "worldview": "animist",
    "items": items
}

os.makedirs("grammars/russian-folk-tales", exist_ok=True)
with open("grammars/russian-folk-tales/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

# Validate
ids = [i["id"] for i in items]
dupes = [x for x in ids if ids.count(x) > 1]
bad_refs = []
for i in items:
    for ref in i.get("composite_of", []):
        if ref not in ids:
            bad_refs.append((i["id"], ref))

print(f"\nTotal items: {len(items)}")
print(f"L1 tales: {sum(1 for i in items if i['level'] == 1)}")
print(f"L2 themes: {sum(1 for i in items if i['level'] == 2)}")
print(f"L3 meta: {sum(1 for i in items if i['level'] == 3)}")
print(f"Sections: {sum(len(i.get('sections', {})) for i in items)}")
print(f"Duplicate IDs: {dupes}")
print(f"Bad refs: {bad_refs}")
print(f"Sort orders OK: {[i['sort_order'] for i in items] == list(range(1, len(items)+1))}")
