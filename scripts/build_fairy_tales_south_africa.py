#!/usr/bin/env python3
"""
Parser for Fairy Tales from South Africa by Sarah F. Bourhill & Beatrice L. Drake
(Project Gutenberg #75833). Outputs grammar.json into grammars/fairy-tales-south-africa/
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'fairy-tales-south-africa.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'fairy-tales-south-africa')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

# Story definitions — note that Serpent's Bride (VIII+IX) and Semai-mai (XIV+XV) are multi-part
STORY_DEFS = [
    {
        "id": "setuli-king-of-birds",
        "name": "Setuli; or, The King of the Birds",
        "subtitle": "A Swazi Tale",
        "keywords": ["setuli", "deaf", "dumb", "birds", "magic", "warrior", "kingdom", "swazi"],
        "category": "hero-tales",
        "reflection": "A deaf-mute man, despised by all, is granted speech and an army by a fairy. What powers lie hidden in those the world overlooks?"
    },
    {
        "id": "kings-son-magic-song",
        "name": "The Story of the King's Son and the Magic Song",
        "subtitle": "A Swazi Tale",
        "keywords": ["prince", "magic-song", "cattle", "fairy-ox", "quest", "swazi"],
        "category": "hero-tales",
        "reflection": "A magic song has the power to call back stolen cattle. What songs or words carry power in your life?"
    },
    {
        "id": "little-birds-in-cave",
        "name": "The Story of the Little Birds who Lived in a Cave",
        "subtitle": "A Zulu Nursery Tale",
        "keywords": ["birds", "cave", "ogre", "children", "rescue", "zulu"],
        "category": "children-tales",
        "reflection": "Little birds must outwit an ogre to survive. How do the small and vulnerable protect themselves against overwhelming danger?"
    },
    {
        "id": "shining-princess",
        "name": "The Story of the Shining Princess",
        "subtitle": "A 'Msuto Story",
        "keywords": ["princess", "shining", "beauty", "quest", "magic", "msuto"],
        "category": "princess-tales",
        "reflection": "A princess who literally shines — beauty as a supernatural force. What inner light do you carry that others can see?"
    },
    {
        "id": "rabbit-prince",
        "name": "The Rabbit Prince",
        "subtitle": "A Shangani Tale",
        "keywords": ["rabbit", "prince", "transformation", "marriage", "magic", "shangani"],
        "category": "transformation-tales",
        "reflection": "A prince in the form of a rabbit — appearances deceive, and true nature is revealed through patience. When has someone's true self surprised you?"
    },
    {
        "id": "unnatural-mother",
        "name": "The Unnatural Mother",
        "subtitle": "A Swazi Tale",
        "keywords": ["mother", "children", "cruelty", "rescue", "justice", "swazi"],
        "category": "family-tales",
        "reflection": "A mother who betrays her own children is one of the darkest themes in any folklore. What does this tale reveal about the sacred bond between parent and child?"
    },
    {
        "id": "three-little-eggs",
        "name": "The Three Little Eggs",
        "subtitle": "A Swazi Tale",
        "keywords": ["eggs", "magic", "girl", "quest", "kindness", "swazi"],
        "category": "magic-tales",
        "reflection": "Three magical eggs carry both fortune and danger. What small, ordinary-seeming things in your life carry extraordinary potential?"
    },
    {
        "id": "serpents-bride",
        "name": "The Serpent's Bride",
        "subtitle": "A Shangani Story",
        "keywords": ["serpent", "bride", "marriage", "transformation", "courage", "water-king", "shangani"],
        "category": "transformation-tales",
        "reflection": "A woman married to a great serpent who is secretly a king — the classic beauty-and-beast motif of South African folklore. What transformations does love make possible?"
    },
    {
        "id": "fairy-bird",
        "name": "The Fairy Bird",
        "subtitle": "A Swazi Tale",
        "keywords": ["fairy", "bird", "girl", "stepmother", "magic", "rescue", "swazi"],
        "category": "magic-tales",
        "reflection": "A fairy in bird form watches over a mistreated girl. What unseen protectors have guided you through difficult times?"
    },
    {
        "id": "cocks-kraal",
        "name": "The Cock's Kraal",
        "subtitle": "A Swazi Tale",
        "keywords": ["cock", "kraal", "boys", "adventure", "ogre", "swazi"],
        "category": "children-tales",
        "reflection": "Boys stumble upon a cock's kraal and face dangers beyond their imagination. What adventures have you fallen into by accident?"
    },
    {
        "id": "baboon-skins",
        "name": "Baboon-Skins",
        "subtitle": "A Swazi Tale",
        "keywords": ["baboon", "skins", "disguise", "princess", "transformation", "swazi"],
        "category": "transformation-tales",
        "reflection": "A beautiful woman hides beneath baboon-skins — the ultimate disguise. What masks do people wear, and what lies beneath?"
    },
    {
        "id": "reward-of-industry",
        "name": "The Reward of Industry",
        "subtitle": "A Zulu Tale",
        "keywords": ["industry", "laziness", "reward", "hard-work", "zulu"],
        "category": "moral-tales",
        "reflection": "Hard work is rewarded and laziness punished — a universal moral expressed through Zulu storytelling. How does your culture teach the value of work?"
    },
    {
        "id": "semai-mai",
        "name": "The Story of Semai-mai",
        "subtitle": "A Swazi Tale",
        "keywords": ["semai-mai", "king", "cruelty", "rebellion", "justice", "war", "swazi"],
        "category": "hero-tales",
        "reflection": "A cruel king who makes his subjects suffer — and the inevitable rebellion that follows. What happens when leaders abuse their power?"
    },
    {
        "id": "fairy-frog",
        "name": "The Fairy Frog",
        "subtitle": "A Swazi Tale",
        "keywords": ["frog", "fairy", "transformation", "princess", "magic", "swazi"],
        "category": "transformation-tales",
        "reflection": "A fairy who appears as a frog — transformation and disguise as recurring themes. What beauty hides in the most unlikely forms?"
    },
    {
        "id": "nya-nya-bulembu",
        "name": "Nya-nya Bulembu; or, The Moss-green Princess",
        "subtitle": "A Swazi Tale",
        "keywords": ["nya-nya-bulembu", "moss-green", "princess", "magic", "love", "swazi"],
        "category": "princess-tales",
        "reflection": "A moss-green princess — beauty in an unexpected color. How does strangeness become its own form of enchantment?"
    },
    {
        "id": "enchanted-buck",
        "name": "The Enchanted Buck",
        "subtitle": "A Swazi Tale",
        "keywords": ["buck", "enchantment", "hunting", "transformation", "magic", "swazi"],
        "category": "transformation-tales",
        "reflection": "An enchanted buck leads hunters into the realm of magic. What has lured you deeper into unfamiliar territory than you intended to go?"
    },
    {
        "id": "beauty-and-beast",
        "name": "The Beauty and the Beast",
        "subtitle": "A Swazi Tale",
        "keywords": ["beauty", "beast", "love", "transformation", "marriage", "swazi"],
        "category": "transformation-tales",
        "reflection": "The universal tale of beauty and the beast, told in the South African tradition. Love sees past the monstrous exterior to the soul within. What has love helped you see that others could not?"
    },
    {
        "id": "white-dove",
        "name": "The White Dove",
        "subtitle": "",
        "keywords": ["dove", "prince", "hunting", "transformation", "love", "magic"],
        "category": "transformation-tales",
        "reflection": "A white dove who is more than she seems — the final tale brings together all the themes of transformation, love, and the supernatural. What final truth about the power of transformation do you carry?"
    },
]


# L2 theme groupings
THEME_GROUPS = [
    {
        "id": "theme-transformation-and-disguise",
        "name": "Transformation and Disguise",
        "category": "themes",
        "about": "The dominant theme of South African fairy tales is transformation. Princes become rabbits, women hide beneath baboon-skins, serpents reveal themselves as water-kings, frogs are fairies, and bucks are enchanted. This is a world where nothing is as it seems, and the true nature of beings can only be revealed through courage, patience, and love. The 'Beauty and the Beast' motif appears repeatedly — always with the message that love sees past appearances to the hidden truth within.",
        "for_readers": "These transformation tales share deep roots with European fairy tales (Beauty and the Beast, The Frog Prince), but carry distinctly African qualities — the animals are local (baboons, bucks, rock-pigeons), the settings are kraals and mountain valleys, and the magic follows African spiritual traditions. Notice how transformation in these tales is always linked to moral qualities: courage reveals the prince beneath the rabbit, love frees the man within the serpent.",
        "member_ids": [
            "rabbit-prince", "serpents-bride", "baboon-skins",
            "fairy-frog", "enchanted-buck", "beauty-and-beast", "white-dove"
        ],
        "keywords": ["transformation", "disguise", "beauty-and-beast", "shapeshifting", "love"]
    },
    {
        "id": "theme-magic-and-fairy-world",
        "name": "The Fairy World and Magic Powers",
        "category": "themes",
        "about": "South African fairy tales are rich with magic — fairy birds, magic songs, enchanted eggs, water-spirits, and powerful old women who grant gifts to the worthy. The fairy world in these stories is not separate from the natural world but woven into it: fairies appear in pools, birds carry messages from the spirit realm, and the power of speech itself is a magical gift. This is a world where the supernatural is as real as the rocks and rivers.",
        "for_readers": "The fairies and spirits of South African folklore are distinct from European fairies — they often appear as old women, as animal spirits, or as water-beings. The magical powers they grant (speech, armies, protection) are always conditional and carry responsibilities. These tales encode a spiritual worldview where the visible and invisible worlds constantly interact.",
        "member_ids": [
            "setuli-king-of-birds", "kings-son-magic-song", "three-little-eggs",
            "fairy-bird", "fairy-frog", "nya-nya-bulembu"
        ],
        "keywords": ["magic", "fairy", "supernatural", "spirit", "enchantment"]
    },
    {
        "id": "theme-hero-quests",
        "name": "Heroes, Kings, and Quests",
        "category": "themes",
        "about": "Several tales feature heroes on quests — Setuli who rises from despised deaf-mute to conquering king, the prince who must recover his father's stolen cattle through a magic song, and the rebellion against the cruel King Semai-mai. These heroes are not born great; they earn their greatness through courage, loyalty, and the favor of the fairy world. The hero's journey in South African tradition always involves proving one's worth through tests of character, not just strength.",
        "for_readers": "These hero tales reflect the political realities of pre-colonial Southern Africa: ambitious chiefs building kingdoms, cattle raids between tribes, the importance of military prowess, and the sacred bond between a ruler and his people. Notice how the heroes always rely on supernatural aid — in this worldview, human achievement alone is never enough. One must also have the favor of the spirit world.",
        "member_ids": [
            "setuli-king-of-birds", "kings-son-magic-song", "semai-mai",
            "shining-princess"
        ],
        "keywords": ["hero", "quest", "king", "conquest", "courage", "kingdom"]
    },
    {
        "id": "theme-family-and-morals",
        "name": "Family, Cruelty, and Moral Lessons",
        "category": "themes",
        "about": "Dark themes of family cruelty run through these tales — unnatural mothers who betray their children, cruel stepmothers, jealous sisters. These stories do not shy away from the darkest aspects of family life, but they always resolve with justice: the cruel are punished, the virtuous are rescued, and hard work is rewarded. They serve as moral instruction encoded in compelling narrative.",
        "for_readers": "These tales were told around evening fires, and their moral lessons were serious. The 'Unnatural Mother' and 'The Fairy Bird' (with its cruel stepmother) address real anxieties about family breakdown in a society where polygamy meant complex family dynamics. The 'Reward of Industry' is a straightforward moral fable. Together they reveal a culture that used storytelling to reinforce social bonds and teach children right from wrong.",
        "member_ids": [
            "unnatural-mother", "fairy-bird", "reward-of-industry",
            "little-birds-in-cave", "cocks-kraal"
        ],
        "keywords": ["family", "mother", "cruelty", "morals", "justice", "children"]
    },
    {
        "id": "theme-princesses-and-beauty",
        "name": "Princesses and the Power of Beauty",
        "category": "themes",
        "about": "The princesses of South African fairy tales are extraordinary beings — one literally shines, another is moss-green, a third hides beneath baboon-skins. Beauty in these tales is not passive ornament but an active supernatural force that drives plots, attracts danger, and ultimately triumphs over evil. These princesses are strong, often enduring great suffering before claiming their rightful place.",
        "for_readers": "The South African princess tales share elements with Cinderella, Snow White, and other European counterparts, but are rooted in African realities — lobola (bride-price), kraals, tribal politics, and the specific landscape of mountain valleys and rivers. The heroines endure trials familiar to any girl growing up in a patriarchal society: jealousy, betrayal, and the struggle to be recognized for who they truly are.",
        "member_ids": [
            "shining-princess", "nya-nya-bulembu", "baboon-skins",
            "serpents-bride", "beauty-and-beast"
        ],
        "keywords": ["princess", "beauty", "women", "strength", "endurance"]
    },
]

L3_DEFS = [
    {
        "id": "meta-themes",
        "name": "Themes and Teachings",
        "category": "meta",
        "about": "The thematic landscape of South African fairy tales: transformation and disguise as the dominant motif, the ever-present fairy world woven into nature, heroes on quests for kingdoms, the dark truths of family cruelty balanced by justice, and princesses whose extraordinary beauty is a supernatural force. These tales, collected from Swazi, Zulu, Shangani, and Msuto storytellers, preserve a rich oral tradition that shares deep roots with fairy tales worldwide while remaining distinctly African in setting, character, and spiritual sensibility.",
        "composite_of": [
            "theme-transformation-and-disguise", "theme-magic-and-fairy-world",
            "theme-hero-quests", "theme-family-and-morals",
            "theme-princesses-and-beauty"
        ],
        "keywords": ["themes", "south-african", "kafir", "swazi", "zulu"]
    },
]


def read_seed():
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def strip_gutenberg(text):
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK FAIRY TALES FROM SOUTH AFRICA ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK FAIRY TALES FROM SOUTH AFRICA ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]
    return text.strip()


def extract_stories(text):
    """Extract stories, combining multi-part stories (Serpent's Bride I+II, Semai-mai I+II)."""
    lines = text.split('\n')

    # Find all Roman numeral chapter starts
    chapter_positions = []
    roman_pattern = re.compile(r'^[IVX]+$')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if roman_pattern.match(stripped) and len(stripped) <= 5:
            # Check next lines for a title in all caps
            for j in range(i+1, min(i+6, len(lines))):
                next_line = lines[j].strip()
                if next_line and next_line.upper() == next_line and len(next_line) > 2:
                    # Looks like a story title
                    chapter_positions.append((i, stripped))
                    break
                elif next_line and not next_line.upper() == next_line:
                    break

    # Map Roman numerals to line positions
    # We need to combine: VIII+IX (Serpent's Bride) and XIV+XV (Semai-mai)
    # Story indices (0-based from STORY_DEFS): 7=Serpent's Bride, 12=Semai-mai

    stories = []
    story_def_idx = 0

    # Track which chapters map to which story def
    # Chapters: I-VII are stories 0-6, VIII+IX are story 7, X-XIII are stories 8-11,
    # XIV+XV are story 12, XVI-XX are stories 13-17
    combined_chapters = {
        'VIII': 'IX',   # Serpent's Bride Part I + Part II
        'XIV': 'XV',    # Semai-mai Part I + Part II
    }
    skip_chapters = {'IX', 'XV'}  # These are combined into the previous

    # Find footnotes section at end
    footnotes_start = len(lines)
    for i in range(len(lines)-1, 0, -1):
        if lines[i].strip().startswith('[1]'):
            footnotes_start = i
            break

    for ch_idx, (line_num, roman) in enumerate(chapter_positions):
        if roman in skip_chapters:
            continue

        # Find the matching story def
        if story_def_idx >= len(STORY_DEFS):
            print(f"WARNING: More chapters than story definitions, skipping chapter {roman}")
            continue

        sdef = STORY_DEFS[story_def_idx]
        story_def_idx += 1

        # Determine end of this story's text
        if roman in combined_chapters:
            # Find the end of the combined chapter (Part II)
            part2_roman = combined_chapters[roman]
            part2_end = None
            for future_ch_idx, (future_line, future_roman) in enumerate(chapter_positions):
                if future_roman == part2_roman:
                    # Find the chapter AFTER the Part II
                    if future_ch_idx + 1 < len(chapter_positions):
                        part2_end = chapter_positions[future_ch_idx + 1][0]
                    else:
                        part2_end = footnotes_start
                    break
            end_line = part2_end if part2_end else footnotes_start
        else:
            if ch_idx + 1 < len(chapter_positions):
                end_line = chapter_positions[ch_idx + 1][0]
            else:
                end_line = footnotes_start

        # Extract text
        story_lines = lines[line_num:end_line]

        # Strip Roman numeral, title, subtitle, and "PART" lines
        content_start = 0
        found_content = False
        for k, sl in enumerate(story_lines):
            s = sl.strip()
            if not s:
                continue
            if not found_content:
                # Skip Roman numeral
                if roman_pattern.match(s) and len(s) <= 5:
                    content_start = k + 1
                    continue
                # Skip ALL CAPS title lines (including multi-line)
                if s.upper() == s and len(s) > 1 and not s[0].isdigit():
                    content_start = k + 1
                    continue
                # Skip subtitle lines like "A SWAZI TALE"
                if s.startswith('A ') and s.upper() == s:
                    content_start = k + 1
                    continue
                # Skip "PART I" / "PART II" lines
                if s.startswith('PART'):
                    content_start = k + 1
                    continue
                found_content = True
                content_start = k
                break

        story_text = '\n'.join(story_lines[content_start:]).strip()

        # For combined stories, also strip the Part II header
        if roman in combined_chapters:
            part2_roman = combined_chapters[roman]
            # Remove the Part II divider: Roman numeral line + title + PART II
            part2_pattern = re.compile(
                r'\n\s*' + part2_roman + r'\s*\n\s*[A-Z][A-Z\s\'\-;,]+\n(?:\s*PART II\s*\n)?',
                re.MULTILINE
            )
            match = part2_pattern.search(story_text)
            if match:
                story_text = story_text[:match.start()] + '\n\n---\n\n' + story_text[match.end():]

        # Remove footnote references [N]
        story_text = re.sub(r' ?\[\d+\]', '', story_text)

        # Remove illustration markers
        story_text = re.sub(r'\[Illustration:.*?\]', '', story_text, flags=re.DOTALL)

        # Clean up whitespace
        story_text = re.sub(r'\n{3,}', '\n\n', story_text)
        story_text = story_text.strip()

        stories.append({
            "sdef": sdef,
            "text": story_text
        })

    return stories


def build_l1_items(stories):
    items = []
    for sort_order, story in enumerate(stories):
        sdef = story["sdef"]
        sections = {"Story": story["text"]}
        if sdef["subtitle"]:
            sections["Origin"] = sdef["subtitle"]
        sections["Reflection"] = sdef["reflection"]

        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "level": 1,
            "category": sdef["category"],
            "sections": sections,
            "keywords": sdef["keywords"],
            "metadata": {
                "source": "Fairy Tales from South Africa, by Mrs. E. J. Bourhill and Mrs. J. B. Drake, 1908"
            }
        }
        items.append(item)
    return items


def build_l2_items(l1_items):
    l2_items = []
    sort_order = len(l1_items)

    for group in THEME_GROUPS:
        l2_items.append({
            "id": group["id"],
            "name": group["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": group["category"],
            "sections": {
                "About": group["about"],
                "For Readers": group["for_readers"]
            },
            "keywords": group["keywords"],
            "composite_of": group["member_ids"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    return l2_items, sort_order


def build_l3_items(start_sort_order):
    l3_items = []
    sort_order = start_sort_order

    for l3 in L3_DEFS:
        l3_items.append({
            "id": l3["id"],
            "name": l3["name"],
            "sort_order": sort_order,
            "level": 3,
            "category": l3["category"],
            "sections": {"About": l3["about"]},
            "keywords": l3["keywords"],
            "composite_of": l3["composite_of"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    return l3_items


def build_grammar(l1_items, l2_items, l3_items):
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Mrs. E. J. Bourhill (Sarah F. Bourhill)",
                    "date": "1908",
                    "note": "Collector and arranger of Fairy Tales from South Africa"
                },
                {
                    "name": "Mrs. J. B. Drake (Beatrice L. Drake)",
                    "date": "1908",
                    "note": "Co-collector and arranger"
                },
                {
                    "name": "W. Herbert Holloway",
                    "date": "1908",
                    "note": "Illustrator of the original 1908 edition"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure and reflections"
                }
            ]
        },
        "name": "Fairy Tales from South Africa",
        "description": "Eighteen fairy tales collected from the Swazi, Zulu, Shangani, and Msuto peoples of South Africa by Mrs. E. J. Bourhill and Mrs. J. B. Drake (1908). These traditional tales, told around evening fires by grandmothers and master storytellers, feature enchanted princes in animal form, shining princesses, fairy birds, serpent bridegrooms, and the ever-present theme of transformation. They share deep structural roots with European fairy tales (Beauty and the Beast, Cinderella, The Frog Prince) while remaining distinctly African in setting, spirit, and moral sensibility. The stories come from the mountain valleys and wooded lowlands of Swaziland, Natal, and the Eastern Transvaal. Source: Project Gutenberg eBook #75833 (https://www.gutenberg.org/ebooks/75833).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: W. Herbert Holloway's original illustrations for the 1908 Macmillan and Co. edition — evocative pen-and-ink drawings depicting Setuli and the Fairy, the mountains of Swaziland, warriors in leopard skins, and the fantastical creatures of South African folklore.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "fairy-tales", "african", "south-african", "folklore", "transformation",
            "swazi", "zulu", "animals", "princesses", "oracle"
        ],
        "roots": ["african-cosmology"],
        "shelves": ["earth"],
        "lineages": ["Akomolafe", "Andreotti"],
        "worldview": "animist",
        "cover_image_url": "",
        "items": l1_items + l2_items + l3_items
    }
    return grammar


def main():
    print("Reading seed text...")
    raw_text = read_seed()

    print("Stripping Gutenberg header/footer...")
    text = strip_gutenberg(raw_text)

    print("Extracting stories...")
    stories = extract_stories(text)
    print(f"  Found {len(stories)} stories")

    if len(stories) != len(STORY_DEFS):
        print(f"  WARNING: Expected {len(STORY_DEFS)} stories, found {len(stories)}")
        for i, s in enumerate(stories):
            print(f"    {i}: {s['sdef']['name']}")

    print("Building L1 items...")
    l1_items = build_l1_items(stories)

    print("Building L2 items...")
    l2_items, next_sort = build_l2_items(l1_items)

    print("Building L3 items...")
    l3_items = build_l3_items(next_sort)

    print("Assembling grammar...")
    grammar = build_grammar(l1_items, l2_items, l3_items)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Writing grammar to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    total_items = len(l1_items) + len(l2_items) + len(l3_items)
    print(f"\nDone! {total_items} items total:")
    print(f"  L1 (stories): {len(l1_items)}")
    print(f"  L2 (groups): {len(l2_items)}")
    print(f"  L3 (meta): {len(l3_items)}")


if __name__ == '__main__':
    main()
