#!/usr/bin/env python3
"""
Parser for Celtic Fairy Tales compiled by Joseph Jacobs (Project Gutenberg #7885).
Illustrated by John D. Batten. Outputs grammar.json into grammars/celtic-fairy-tales/
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'celtic-fairy-tales.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'celtic-fairy-tales')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

STORY_DEFS = [
    {
        "title": "CONNLA AND THE FAIRY MAIDEN",
        "id": "connla-fairy-maiden",
        "name": "Connla and the Fairy Maiden",
        "keywords": ["fairy", "maiden", "enchantment", "otherworld", "love", "druid", "irish"],
        "reflection": "A fairy maiden calls Connla to the Land of the Ever Living, and no druid's power can silence her song. This tale captures the ancient Celtic tension between the mortal world and the irresistible pull of the Otherworld."
    },
    {
        "title": "GULEESH",
        "id": "guleesh",
        "name": "Guleesh",
        "keywords": ["fairies", "princess", "speech", "rescue", "patience", "irish"],
        "reflection": "Guleesh rides with the fairies and saves a princess, but she is struck dumb by fairy magic. His patient devotion through a year of silence teaches that true love is not a moment of rescue but a long season of faithfulness."
    },
    {
        "title": "THE FIELD OF BOLIAUNS",
        "id": "field-of-boliauns",
        "name": "The Field of Boliauns",
        "keywords": ["leprechaun", "treasure", "cleverness", "trickery", "irish"],
        "reflection": "A man catches a leprechaun and marks the spot where treasure is buried — only to find the clever fairy has outwitted him entirely. The treasure that can be tricked out of the Otherworld is no treasure at all."
    },
    {
        "title": "THE HORNED WOMEN",
        "id": "horned-women",
        "name": "The Horned Women",
        "keywords": ["witches", "spinning", "protection", "banshee", "irish"],
        "reflection": "Twelve horned witches invade a woman's home on a dark night, and only the Spirit of the Well can tell her how to break their spell. This eerie tale preserves ancient protective rituals wrapped in a story of courage and quick thinking."
    },
    {
        "title": "CONALL YELLOWCLAW",
        "id": "conal-yellowclaw",
        "name": "Conal Yellowclaw",
        "keywords": ["giant", "quest", "hero", "scottish", "adventure", "courage"],
        "reflection": "Conal Yellowclaw faces a giant and endures terrible trials with cunning and bravery. His story is a classic Highland hero tale — raw, violent, and thrilling — where survival depends on wit as much as strength."
    },
    {
        "title": "HUDDEN AND DUDDEN AND DONALD O'NEARY",
        "id": "hudden-dudden-donald-oneary",
        "name": "Hudden and Dudden and Donald O'Neary",
        "keywords": ["trickster", "humor", "revenge", "cleverness", "irish"],
        "reflection": "Donald O'Neary turns every attempt on his life into profit, outwitting his greedy neighbors at every turn. This rollicking Irish droll celebrates the triumph of the clever underdog over the stupid and the mean."
    },
    {
        "title": "THE SHEPHERD OF MYDDVAI",
        "id": "shepherd-of-myddvai",
        "name": "The Shepherd of Myddvai",
        "keywords": ["fairy", "wife", "lake", "taboo", "welsh", "physicians"],
        "reflection": "A shepherd wins a fairy bride from a lake, but loses her when he breaks a mysterious taboo. The Physicians of Myddvai, her descendants, inherit her healing knowledge — a beautiful origin story linking the fairy world to the art of medicine."
    },
    {
        "title": "THE SPRIGHTLY TAILOR",
        "id": "sprightly-tailor",
        "name": "The Sprightly Tailor",
        "keywords": ["tailor", "ghost", "courage", "humor", "scottish"],
        "reflection": "A brave tailor agrees to sew trousers in a haunted church at midnight and faces a terrifying apparition with cheerful defiance. Courage in this tale is not the absence of fear but the refusal to stop working."
    },
    {
        "title": "THE STORY OF DEIRDRE",
        "id": "story-of-deirdre",
        "name": "The Story of Deirdre",
        "keywords": ["deirdre", "naoise", "tragedy", "love", "fate", "irish", "ulster"],
        "reflection": "Deirdre of the Sorrows — the most beautiful and tragic figure in Celtic mythology. Her doomed love for Naoise and their flight from King Conor is a story of passion, betrayal, and grief that has haunted Irish literature for over a thousand years."
    },
    {
        "title": "MUNACHAR AND MANACHAR",
        "id": "munachar-manachar",
        "name": "Munachar and Manachar",
        "keywords": ["chain-tale", "cumulative", "humor", "irish", "repetition"],
        "reflection": "One thing leads to another in this delightful chain tale — a Celtic 'House That Jack Built' where every solution creates a new problem. The humor lies in the absurd, ever-growing chain of demands."
    },
    {
        "title": "GOLD-TREE AND SILVER-TREE",
        "id": "gold-tree-silver-tree",
        "name": "Gold-Tree and Silver-Tree",
        "keywords": ["stepmother", "jealousy", "beauty", "scottish", "snow-white"],
        "reflection": "A Celtic Snow White: Silver-Tree, maddened by jealousy of her daughter Gold-Tree's beauty, tries to murder her. This Scottish tale shares deep roots with the most famous fairy tale in the world, but its resolution has a distinctly Celtic flavor."
    },
    {
        "title": "KING O'TOOLE AND HIS GOOSE",
        "id": "king-otoole-goose",
        "name": "King O'Toole and His Goose",
        "keywords": ["king", "goose", "saint", "bargain", "humor", "irish"],
        "reflection": "King O'Toole loves his old goose more than his kingdom, and Saint Kevin strikes a peculiar bargain that gives this comic tale its moral: sometimes the things we love most are the things we must surrender."
    },
    {
        "title": "THE WOOING OF OLWEN",
        "id": "wooing-of-olwen",
        "name": "The Wooing of Olwen",
        "keywords": ["culhwch", "olwen", "arthur", "quest", "giant", "welsh", "mabinogion"],
        "reflection": "Culhwch must complete impossible tasks set by the giant Ysbaddaden to win Olwen, whose footsteps leave white clover. This ancient Welsh tale from the Mabinogion is one of the earliest Arthurian stories and one of the greatest quest narratives in European literature."
    },
    {
        "title": "JACK AND HIS COMRADES",
        "id": "jack-and-comrades",
        "name": "Jack and His Comrades",
        "keywords": ["jack", "animals", "robbers", "journey", "irish", "bremen"],
        "reflection": "Jack gathers a donkey, dog, cat, and rooster on his travels, and together they defeat a band of robbers. A Celtic cousin of the Bremen Town Musicians, this tale celebrates the power of unlikely alliances."
    },
    {
        "title": "THE SHEE AN GANNON AND THE GRUAGACH GAIRE",
        "id": "shee-an-gannon",
        "name": "The Shee an Gannon and the Gruagach Gaire",
        "keywords": ["fairy", "laughter", "quest", "enchantment", "devotion", "irish"],
        "reflection": "The Shee an Gannon must restore the Gruagach Gaire's lost laughter — a quest that takes him through enchantment and danger. This tale asks a profound question: what does it take to bring joy back to someone who has lost it entirely?"
    },
    {
        "title": "THE STORY-TELLER AT FAULT",
        "id": "story-teller-at-fault",
        "name": "The Story-Teller at Fault",
        "keywords": ["storyteller", "fairy", "humor", "meta", "irish"],
        "reflection": "A famous storyteller runs out of tales and must face the consequences — a delightfully self-aware story about the power and peril of storytelling itself. In the Celtic world, a tale-teller who cannot tell tales has lost everything."
    },
    {
        "title": "THE SEA-MAIDEN",
        "id": "sea-maiden",
        "name": "The Sea-Maiden",
        "keywords": ["sea-maiden", "hero", "quest", "magic", "scottish", "giant"],
        "reflection": "A young hero makes a bargain with a sea-maiden and must face giants, enchantments, and tests of loyalty. This sprawling Scottish tale is a masterpiece of adventure storytelling, layering quest upon quest until the hero earns his freedom."
    },
    {
        "title": "A LEGEND OF KNOCKMANY",
        "id": "legend-of-knockmany",
        "name": "A Legend of Knockmany",
        "keywords": ["finn", "cucullin", "giant", "oonagh", "humor", "irish"],
        "reflection": "Finn McCool is terrified of the giant Cucullin — but his clever wife Oonagh devises a hilarious plan involving a baby disguise. This comic masterpiece shows that behind every legendary hero stands someone even cleverer."
    },
    {
        "title": "FAIR, BROWN, AND TREMBLING",
        "id": "fair-brown-trembling",
        "name": "Fair, Brown, and Trembling",
        "keywords": ["cinderella", "sisters", "prince", "magic", "irish"],
        "reflection": "An Irish Cinderella: Trembling is kept from church by her jealous sisters Fair and Brown, until a fairy dressmaker transforms her. The glass slipper becomes a shoe of white silk, but the story's heart is the same — hidden worth will be revealed."
    },
    {
        "title": "JACK AND HIS MASTER",
        "id": "jack-and-master",
        "name": "Jack and His Master",
        "keywords": ["jack", "master", "cleverness", "bargain", "humor", "irish"],
        "reflection": "Jack serves a master and learns that the cleverest bargain is the one where you know exactly what words mean. This tale of wit and wordplay celebrates the Irish love of language turned to sharp advantage."
    },
    {
        "title": "BETH GELLERT",
        "id": "beth-gellert",
        "name": "Beth Gellert",
        "keywords": ["dog", "loyalty", "tragedy", "hound", "welsh", "llewelyn"],
        "reflection": "Prince Llewelyn kills his faithful hound Gellert, believing it attacked his child — only to find the dog had saved the baby from a wolf. This devastating Welsh tale is one of the most powerful stories ever told about loyalty, haste, and irreversible regret."
    },
    {
        "title": "THE TALE OF IVAN",
        "id": "tale-of-ivan",
        "name": "The Tale of Ivan",
        "keywords": ["ivan", "devotion", "wife", "sacrifice", "welsh"],
        "reflection": "Ivan's tale is one of quiet devotion tested by extraordinary circumstances. In the Celtic tradition, love is proven not by grand gestures but by steadfast faithfulness through impossible trials."
    },
    {
        "title": "ANDREW COFFEY",
        "id": "andrew-coffey",
        "name": "Andrew Coffey",
        "keywords": ["fairy", "humor", "bargain", "irish", "adventure"],
        "reflection": "Andrew Coffey stumbles into a fairy adventure and must use his wits to come out the other side. This comic tale reminds us that in Ireland, even the most ordinary person may find themselves caught up in the extraordinary."
    },
    {
        "title": "THE BATTLE OF THE BIRDS",
        "id": "battle-of-birds",
        "name": "The Battle of the Birds",
        "keywords": ["birds", "quest", "magic", "giant", "scottish", "transformation"],
        "reflection": "A king's son befriends a raven after a great battle of the birds and is drawn into a sprawling adventure of enchantment and impossible tasks. This magnificent Scottish tale is one of the longest and richest in the Celtic tradition."
    },
    {
        "title": "BREWERY OF EGGSHELLS",
        "id": "brewery-of-eggshells",
        "name": "Brewery of Eggshells",
        "keywords": ["changeling", "fairy", "child", "eggshells", "welsh"],
        "reflection": "A mother suspects her child has been replaced by a fairy changeling and uses the eggshell brewery trick to force the fairy to reveal itself. This widely-told tale reflects deep anxieties about children, identity, and the thin boundary between human and fairy worlds."
    },
    {
        "title": "THE LAD WITH THE GOAT-SKIN",
        "id": "lad-with-goat-skin",
        "name": "The Lad with the Goat-Skin",
        "keywords": ["hero", "goat-skin", "quest", "giant", "princess", "irish"],
        "reflection": "A young lad in a goat-skin sets out to seek his fortune and defeats giants and enchantments through courage and good nature. This classic Irish hero tale celebrates the power of a generous heart over brute strength."
    },
]

THEME_GROUPS = [
    {
        "id": "theme-fairy-encounters",
        "name": "Fairy Encounters and Enchantment",
        "category": "themes",
        "about": "The Celtic world is alive with fairies — not the tiny winged creatures of Victorian fancy, but powerful, dangerous, beautiful beings who live just beyond the edge of the mortal world. These tales explore encounters with the fairy realm: leprechauns guarding treasure, fairy maidens calling mortals to the Otherworld, horned witches spinning at midnight, changeling children, and the mysterious fairy wife who emerges from a Welsh lake. In every tale, the boundary between human and fairy is thin and perilous.",
        "for_readers": "Notice how fairies in Celtic tradition are never simply good or evil — they are other. They operate by their own rules, and mortals who cross into their world must learn those rules or be lost. What do these tales tell us about the Celtic relationship with the unknown, the wild, and the sacred?",
        "member_ids": ["connla-fairy-maiden", "guleesh", "field-of-boliauns", "horned-women", "shepherd-of-myddvai", "brewery-of-eggshells"],
        "keywords": ["fairy", "enchantment", "otherworld", "leprechaun", "changeling"]
    },
    {
        "id": "theme-heroes-quests",
        "name": "Heroes and Quests",
        "category": "themes",
        "about": "The Celtic hero is not a simple strongman — he is a quester, a wanderer, a seeker who must pass through danger, enchantment, and impossible tasks to prove his worth. Culhwch seeks Olwen through the labors set by her giant father. Conal Yellowclaw faces giants in the Scottish Highlands. The Sea-Maiden's hero must fulfill a terrible bargain. Deirdre's Naoise is a hero of love rather than war. These tales draw from the deepest wells of Celtic mythology — the Mabinogion, the Ulster Cycle, and the living folk tradition of Ireland and Scotland.",
        "for_readers": "The quests in these tales are never merely physical — they test character, loyalty, and wisdom. Pay attention to what each hero must sacrifice or learn to complete their journey. The Celtic quest is always a transformation as much as a destination.",
        "member_ids": ["conal-yellowclaw", "story-of-deirdre", "wooing-of-olwen", "sea-maiden", "battle-of-birds", "lad-with-goat-skin"],
        "keywords": ["hero", "quest", "giant", "adventure", "courage", "transformation"]
    },
    {
        "id": "theme-wit-trickery",
        "name": "Wit, Trickery, and Humor",
        "category": "themes",
        "about": "The Celtic peoples are famous for their love of wit, wordplay, and the comic tale. Donald O'Neary outwits his murderous neighbors with outrageous tricks. King O'Toole is charmed out of his kingdom by a smooth-talking saint. Jack bargains with animals and masters through sheer cleverness. The Sprightly Tailor sews trousers while a ghost tries to terrify him. The Story-Teller at Fault loses his most precious possession — his tales. And Munachar and Manachar spin an absurd chain of demands. These are the drolls and comic tales that made long winter nights bearable.",
        "for_readers": "Humor in Celtic tales is never merely entertainment — it is a survival strategy. The clever underdog defeats the powerful through wit, and the audience delights in seeing the mighty brought low. Notice how many of these tales feature characters who are poor, small, or overlooked — yet who triumph through intelligence and audacity.",
        "member_ids": ["hudden-dudden-donald-oneary", "sprightly-tailor", "munachar-manachar", "king-otoole-goose", "jack-and-comrades", "jack-and-master", "andrew-coffey", "story-teller-at-fault"],
        "keywords": ["wit", "trickster", "humor", "cleverness", "droll", "comic"]
    },
    {
        "id": "theme-love-loyalty",
        "name": "Love, Loyalty, and Sacrifice",
        "category": "themes",
        "about": "Celtic tales of love are rarely gentle — they burn with passion, ache with loss, and demand terrible sacrifices. Deirdre dies of sorrow for Naoise. Gellert the faithful hound is killed by the master he saved. Gold-Tree is nearly murdered by her jealous mother. Fair, Brown, and Trembling is an Irish Cinderella whose hidden worth must be revealed. The Shee an Gannon quests to restore lost laughter. Ivan endures impossible trials for devotion. In the Celtic world, love is not a feeling but a commitment tested by fire.",
        "for_readers": "These tales do not promise happy endings — they promise truth. Love and loyalty are the highest virtues in Celtic tradition, but they come at a cost. Beth Gellert is one of the most devastating stories ever told because it shows what happens when loyalty is met with haste and suspicion. What do these tales teach about the price of devotion?",
        "member_ids": ["gold-tree-silver-tree", "fair-brown-trembling", "beth-gellert", "tale-of-ivan", "shee-an-gannon"],
        "keywords": ["love", "loyalty", "sacrifice", "devotion", "tragedy"]
    },
    {
        "id": "theme-giants-legends",
        "name": "Giants and Legendary Figures",
        "category": "themes",
        "about": "Finn McCool, the greatest hero of Irish legend, is terrified of a rival giant — and his clever wife Oonagh must save him with a hilarious plan involving a baby disguise and bread baked with iron griddles. This comic masterpiece stands at the intersection of mythology and folk humor, taking the grandest figures of Celtic legend and making them delightfully, absurdly human.",
        "for_readers": "The Legend of Knockmany shows us something essential about Celtic storytelling: even the greatest heroes are allowed to be afraid, and the real power often belongs to the women standing behind them. Oonagh's cleverness is the true heroism of this tale.",
        "member_ids": ["legend-of-knockmany"],
        "keywords": ["giant", "finn", "legend", "humor", "oonagh"]
    },
]

L3_DEFS = [
    {
        "id": "celtic-imagination",
        "name": "The Celtic Imagination",
        "category": "meta",
        "about": "Celtic fairy tales spring from a world where the boundary between the seen and unseen is thin as morning mist. Fairies are not charming fantasies but real powers. Heroes quest through landscapes charged with enchantment. Humor and tragedy sit side by side, often in the same tale. Love demands sacrifice. Wit defeats strength. And the storyteller — the seanchai — holds a position of sacred importance. Joseph Jacobs gathered these twenty-six tales from Irish, Scottish, and Welsh traditions to reveal the unity and richness of the Celtic storytelling imagination. Five thematic streams — fairy encounters, heroic quests, comic wit, love and loyalty, and legendary figures — weave together into a tradition that has shaped the fairy tale heritage of the English-speaking world.",
        "composite_of": [
            "theme-fairy-encounters",
            "theme-heroes-quests",
            "theme-wit-trickery",
            "theme-love-loyalty",
            "theme-giants-legends"
        ],
        "keywords": ["celtic", "imagination", "fairy-tale", "tradition", "irish", "scottish", "welsh"]
    },
]


def read_seed():
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    # Try alternate markers
    alt_start = "*** START OF THIS PROJECT GUTENBERG EBOOK"
    alt_end = "*** END OF THIS PROJECT GUTENBERG EBOOK"

    start_idx = text.find(start_marker)
    if start_idx == -1:
        start_idx = text.find(alt_start)
    if start_idx != -1:
        text = text[text.index('\n', start_idx) + 1:]

    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = text.find(alt_end)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def strip_front_matter(text):
    """Remove everything before the first tale (Connla and the Fairy Maiden)."""
    # Look for the first tale title in ALL CAPS
    pattern = re.compile(r'^CONNLA AND THE FAIRY MAIDEN\s*$', re.MULTILINE)
    m = pattern.search(text)
    if m:
        return text[m.start():].strip()
    # Fallback: try to find it case-insensitively
    pattern2 = re.compile(r'^CONNLA\s+AND\s+THE\s+FAIRY\s+MAIDEN\s*$', re.MULTILINE | re.IGNORECASE)
    m2 = pattern2.search(text)
    if m2:
        return text[m2.start():].strip()
    print("WARNING: Could not find start of first tale (Connla and the Fairy Maiden)")
    return text


def strip_end_matter(text):
    """Remove Notes and References section and anything after."""
    pattern = re.compile(r'^NOTES AND REFERENCES\s*$', re.MULTILINE)
    m = pattern.search(text)
    if m:
        return text[:m.start()].strip()
    # Try variations
    for variant in [r'^NOTES\s+AND\s+REFERENCES', r'^NOTES$']:
        pat = re.compile(variant, re.MULTILINE)
        m2 = pat.search(text)
        if m2:
            return text[:m2.start()].strip()
    print("WARNING: Could not find end matter marker (NOTES AND REFERENCES)")
    return text


def clean_text(text):
    """Clean illustration markers, footnotes, excessive whitespace."""
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    text = re.sub(r'\[Footnote[^\]]*\]', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove separator lines
    text = re.sub(r'\n\s*\*\s+\*\s+\*\s+\*\s+\*\s*\n', '\n\n', text)
    text = re.sub(r'\n\s*\*\s+\*\s+\*\s*\n', '\n\n', text)
    return text.strip()


def find_tale_positions(text):
    """Find the position of each tale title in the text.

    Tales are identified by their ALL CAPS title on its own line.
    Uses flexible matching to handle variations in the source text.
    """
    positions = []

    for i, sdef in enumerate(STORY_DEFS):
        title = sdef["title"]

        # Build a flexible regex: allow optional "A " prefix, flexible whitespace
        # For "A LEGEND OF KNOCKMANY", also try "LEGEND OF KNOCKMANY"
        escaped = re.escape(title)
        pattern = re.compile(r'^\s*' + escaped + r'\s*$', re.MULTILINE)
        m = pattern.search(text)

        if m is None and title.startswith("A "):
            # Try without the leading "A "
            alt_title = title[2:]
            alt_escaped = re.escape(alt_title)
            pattern2 = re.compile(r'^\s*(?:A\s+)?' + alt_escaped + r'\s*$', re.MULTILINE)
            m = pattern2.search(text)

        if m is None:
            # Try with flexible spacing
            words = title.split()
            flex_pattern = r'^\s*' + r'\s+'.join(re.escape(w) for w in words) + r'\s*$'
            pattern3 = re.compile(flex_pattern, re.MULTILINE)
            m = pattern3.search(text)

        if m is not None:
            positions.append((m.start(), i))
        else:
            print(f"WARNING: Could not find tale: {title}")

    positions.sort(key=lambda x: x[0])
    return positions


def extract_stories(text):
    """Split text into individual tales based on ALL CAPS titles."""
    positions = find_tale_positions(text)
    stories = []

    for pos_idx, (start_pos, def_idx) in enumerate(positions):
        sdef = STORY_DEFS[def_idx]

        if pos_idx + 1 < len(positions):
            end_pos = positions[pos_idx + 1][0]
        else:
            end_pos = len(text)

        tale_text = text[start_pos:end_pos].strip()

        # Remove the title line(s) from the beginning
        lines = tale_text.split('\n')
        content_start = 0
        for j, line in enumerate(lines):
            stripped = line.strip()
            if stripped == '' or stripped.upper() == sdef["title"] or stripped.upper() == sdef["title"].lstrip("A "):
                content_start = j + 1
            else:
                break

        story_content = '\n'.join(lines[content_start:]).strip()
        story_content = clean_text(story_content)

        stories.append({
            "def_idx": def_idx,
            "text": story_content
        })

    return stories


def build_l1_items(stories):
    items = []
    for sort_order, story in enumerate(stories):
        sdef = STORY_DEFS[story["def_idx"]]
        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "level": 1,
            "category": "fairy-tale",
            "sections": {
                "Story": story["text"],
                "Reflection": sdef["reflection"]
            },
            "keywords": sdef["keywords"],
            "metadata": {
                "source": "Celtic Fairy Tales, selected and edited by Joseph Jacobs, illustrated by John D. Batten, London, David Nutt, 1892"
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
            "sections": {
                "About": l3["about"]
            },
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
                    "name": "Joseph Jacobs",
                    "date": "1892",
                    "note": "Selected and edited Celtic Fairy Tales, David Nutt, London"
                },
                {
                    "name": "John D. Batten",
                    "date": "1892",
                    "note": "Illustrator of the original edition"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure, thematic groupings, and reflections"
                }
            ]
        },
        "name": "Celtic Fairy Tales",
        "description": "Twenty-six fairy tales from Irish, Scottish, and Welsh tradition, selected and edited by Joseph Jacobs (1892) with illustrations by John D. Batten. This landmark anthology gathers tales of fairy enchantment, heroic quests, comic trickery, tragic love, and legendary giants from across the Celtic world — from the ancient Mabinogion and the Ulster Cycle to the living folk tradition of the fireside seanchai. Includes the great tales of Deirdre of the Sorrows, the Wooing of Olwen, Finn McCool at Knockmany, and the Irish Cinderella. Source: Project Gutenberg eBook #7885 (https://www.gutenberg.org/ebooks/7885).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: John D. Batten's original illustrations for the 1892 David Nutt edition — striking line drawings and color plates in Arts and Crafts style depicting scenes from each tale, including ornamental chapter headings and full-page illustrations of fairy maidens, giants, and Celtic heroes. Batten's work for both Celtic Fairy Tales and its companion volume More Celtic Fairy Tales (1894) represents some of the finest fairy tale illustration of the Victorian era.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "fairy-tales",
            "celtic",
            "irish",
            "scottish",
            "welsh",
            "folklore",
            "public-domain",
            "full-text"
        ],
        "roots": ["indigenous-mythology", "european-tradition"],
        "shelves": ["wonder", "children"],
        "lineages": ["Shrei", "Andreotti"],
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

    print("Stripping front matter (preface, contents)...")
    text = strip_front_matter(text)

    print("Stripping end matter (notes and references)...")
    text = strip_end_matter(text)

    print("Extracting tales...")
    stories = extract_stories(text)
    print(f"  Found {len(stories)} tales (expected 26)")

    if len(stories) < 26:
        print(f"  WARNING: Only found {len(stories)} of 26 tales!")
        found_ids = {STORY_DEFS[s["def_idx"]]["id"] for s in stories}
        for sdef in STORY_DEFS:
            if sdef["id"] not in found_ids:
                print(f"    MISSING: {sdef['name']}")

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
    print(f"  L1 (tales): {len(l1_items)}")
    print(f"  L2 (themes): {len(l2_items)}")
    print(f"  L3 (meta): {len(l3_items)}")


if __name__ == '__main__':
    main()
