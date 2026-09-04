#!/usr/bin/env python3
"""
Parse Arabian Nights (Andrew Lang edition, Gutenberg #128) into grammar.json.
Creates L1 items for each story, L2 for story cycles, L3 for meta.
"""
import json, re

BASE_GRAMMAR_URL = "https://github.com/PlayfulProcess/recursive.eco-schemas/tree/main/grammars/"

with open("seeds/arabian-nights.txt", encoding="utf-8") as f:
    text = f.read()

# Strip Gutenberg header/footer
gut_start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
gut_start = text.find("\n", gut_start) + 1
end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
body = text[gut_start:end].strip()

# Define stories with their headings (in order they appear)
STORY_DEFS = [
    ("The Arabian Nights", "frame-story", "The Frame Story: Scheherazade", "frame", ["scheherazade", "frame-tale", "survival", "storytelling"]),
    ("The Story of the Merchant and the Genius", "merchant-genius", "The Merchant and the Genius", "merchants-genies", ["merchant", "genius", "dates", "tears"]),
    ("The Story of the First Old Man and of the Hind", "first-old-man-hind", "The First Old Man and the Hind", "merchants-genies", ["transformation", "jealousy", "enchantment"]),
    ("The Story of the Second Old Man, and of the Two Black Dogs", "second-old-man-dogs", "The Second Old Man and the Two Black Dogs", "merchants-genies", ["brothers", "ingratitude", "magic"]),
    ("The Story of the Fisherman", "fisherman", "The Fisherman and the Genie", "fisherman-cycle", ["fisherman", "genie", "bottle", "cleverness"]),
    ("The Story of the Greek King and the Physician Douban", "greek-king-douban", "The Greek King and the Physician Douban", "fisherman-cycle", ["physician", "ingratitude", "wisdom", "poison"]),
    ("The Story of the Husband and the Parrot", "husband-parrot", "The Husband and the Parrot", "fisherman-cycle", ["parrot", "jealousy", "deception"]),
    ("The Story of the Vizir Who Was Punished", "vizir-punished", "The Vizir Who Was Punished", "fisherman-cycle", ["vizir", "punishment", "counsel"]),
    ("The Story of the Young King of the Black Isles", "young-king-black-isles", "The Young King of the Black Isles", "fisherman-cycle", ["enchantment", "half-stone", "betrayal", "lake"]),
    ("The Story of the Three Calenders, Sons of Kings,", "three-calenders-frame", "The Three Calenders and the Five Ladies of Bagdad", "calenders-cycle", ["calenders", "ladies", "bagdad", "mystery"]),
    ("The Story of the First Calender, Son of a King", "first-calender", "The First Calender's Tale", "calenders-cycle", ["prince", "exile", "one-eyed"]),
    ("The Story of the Envious Man and of Him Who Was Envied", "envious-man", "The Envious Man and Him Who Was Envied", "calenders-cycle", ["envy", "virtue", "well"]),
    ("The Story of the Second Calendar, Son of a King", "second-calender", "The Second Calender's Tale", "calenders-cycle", ["prince", "ape", "enchantment", "princess"]),
    ("The Story of the Third Calendar, Son of a King", "third-calender", "The Third Calender's Tale", "calenders-cycle", ["prince", "magnetic-mountain", "horse", "forbidden-door"]),
    ("The Seven Voyages of Sindbad the Sailor", "sindbad-frame", "The Seven Voyages of Sindbad the Sailor", "sindbad-cycle", ["sindbad", "voyages", "sea", "adventure"]),
    ("The Little Hunchback", "little-hunchback", "The Little Hunchback", "hunchback-cycle", ["hunchback", "death", "comedy", "misunderstanding"]),
    ("The Story of the Barber's Fifth Brother", "barbers-fifth-brother", "The Barber's Fifth Brother", "hunchback-cycle", ["barber", "greed", "misfortune"]),
    ("The Story of the Barber's Sixth Brother", "barbers-sixth-brother", "The Barber's Sixth Brother", "hunchback-cycle", ["barber", "blindness", "caliph"]),
    ("The Adventures of Prince Camaralzaman and the Princess Badoura", "camaralzaman-badoura", "Prince Camaralzaman and Princess Badoura", "love-tales", ["prince", "princess", "ring", "talisman", "love"]),
    ("Noureddin and the Fair Persian", "noureddin-persian", "Noureddin and the Fair Persian", "love-tales", ["noureddin", "slave", "love", "caliph"]),
    ("Aladdin and the Wonderful Lamp", "aladdin", "Aladdin and the Wonderful Lamp", "magic-tales", ["aladdin", "lamp", "genie", "magician", "princess"]),
    ("The Adventures of Haroun-al-Raschid, Caliph of Bagdad", "haroun-al-raschid", "The Adventures of Haroun-al-Raschid", "caliph-tales", ["haroun", "caliph", "bagdad", "disguise"]),
    ("The Story of the Blind Baba-Abdalla", "blind-baba-abdalla", "The Blind Baba-Abdalla", "caliph-tales", ["blindness", "greed", "punishment", "dervish"]),
    ("The Story of Sidi-Nouman", "sidi-nouman", "Sidi-Nouman", "caliph-tales", ["wife", "ghoul", "transformation", "horse"]),
    ("The Story of Ali Colia, Merchant of Bagdad", "ali-colia", "Ali Colia, Merchant of Bagdad", "caliph-tales", ["merchant", "trust", "olives", "justice"]),
    ("The Enchanted Horse", "enchanted-horse", "The Enchanted Horse", "magic-tales", ["horse", "flight", "invention", "prince"]),
    ("The Story of Two Sisters Who Were Jealous of Their Younger Sister", "two-jealous-sisters", "The Two Jealous Sisters", "magic-tales", ["sisters", "jealousy", "bird", "singing-tree"]),
]

# Also add Sindbad individual voyages
SINDBAD_VOYAGES = [
    ("First Voyage", "sindbad-voyage-1", "Sindbad's First Voyage", "sindbad-cycle", ["whale-island", "shipwreck"]),
    ("Second Voyage", "sindbad-voyage-2", "Sindbad's Second Voyage", "sindbad-cycle", ["roc", "diamonds", "valley"]),
    ("Third Voyage", "sindbad-voyage-3", "Sindbad's Third Voyage", "sindbad-cycle", ["cyclops", "giant", "serpents"]),
    ("Fourth Voyage", "sindbad-voyage-4", "Sindbad's Fourth Voyage", "sindbad-cycle", ["cannibals", "buried-alive", "wife"]),
    ("Fifth Voyage", "sindbad-voyage-5", "Sindbad's Fifth Voyage", "sindbad-cycle", ["roc-again", "old-man-of-sea"]),
    ("Sixth Voyage", "sindbad-voyage-6", "Sindbad's Sixth Voyage", "sindbad-cycle", ["river", "underground", "gems"]),
    ("Seventh and Last Voyage", "sindbad-voyage-7", "Sindbad's Seventh and Last Voyage", "sindbad-cycle", ["elephant", "ivory", "final-journey"]),
]

ALL_STORIES = STORY_DEFS + SINDBAD_VOYAGES

# Extract story texts
# Build a list of (heading, start_pos) pairs
heading_positions = []
for heading, sid, name, cat, kw in ALL_STORIES:
    pos = body.find("\n" + heading + "\n")
    if pos == -1:
        pos = body.find("\n" + heading)
    if pos == -1:
        print(f"WARNING: Could not find heading '{heading}'")
        heading_positions.append((heading, sid, name, cat, kw, -1))
    else:
        heading_positions.append((heading, sid, name, cat, kw, pos))

# Sort by position
heading_positions.sort(key=lambda x: x[5] if x[5] >= 0 else 999999)

# Extract text between headings
items = []
sort_order = 1

for idx, (heading, sid, name, cat, kw, pos) in enumerate(heading_positions):
    if pos < 0:
        continue
    # Find next heading position
    next_pos = len(body)
    for _, _, _, _, _, npos in heading_positions:
        if npos > pos:
            next_pos = min(next_pos, npos)
            break
    # Get all positions after this one
    later = [npos for _, _, _, _, _, npos in heading_positions if npos > pos]
    if later:
        next_pos = min(later)

    story_text = body[pos:next_pos].strip()
    # Remove the heading itself
    lines = story_text.split("\n")
    # Skip heading lines
    content_lines = []
    started = False
    for line in lines:
        if not started:
            if line.strip() == "" or line.strip() == heading.strip():
                continue
            started = True
        content_lines.append(line)

    full_text = "\n".join(content_lines).strip()

    # Truncate to first ~2000 chars for the story section, keep it readable
    if len(full_text) > 3000:
        # Find a good break point
        break_point = full_text.rfind(".", 0, 2500)
        if break_point == -1:
            break_point = 2500
        excerpt = full_text[:break_point + 1]
        remaining_words = len(full_text[break_point:].split())
        story_section = excerpt + f"\n\n[Story continues for approximately {remaining_words} more words...]"
    else:
        story_section = full_text

    items.append({
        "id": sid,
        "name": name,
        "sort_order": sort_order,
        "category": cat,
        "level": 1,
        "sections": {
            "Story": story_section
        },
        "keywords": ["arabian-nights", "1001-nights"] + kw,
        "metadata": {"origin": "Persian/Arabic"}
    })
    sort_order += 1

# ═══════════════════════════════════════════════════════════════════════════
# L2: Story Cycles
# ═══════════════════════════════════════════════════════════════════════════

cycles = {
    "merchants-genies": {
        "name": "The Merchant and the Genius Cycle",
        "about": "The opening cycle of stories within the frame tale. A merchant accidentally kills the son of a genius (jinn) by throwing date-stones. Three old men each tell a tale of their own misfortune to buy the merchant's life, story by story. The pattern of the whole Nights in miniature: narrative as ransom, each tale buying time.",
        "ids": ["merchant-genius", "first-old-man-hind", "second-old-man-dogs"]
    },
    "fisherman-cycle": {
        "name": "The Fisherman Cycle",
        "about": "The fisherman who pulls a sealed jar from the sea and releases a genie who has been imprisoned for centuries. The genie, grateful at first, turns murderous — and the fisherman must use his wits to survive. Nested within: stories of physicians, parrots, and enchanted kings. The theme throughout is the danger of power unleashed and the counter-power of cleverness.",
        "ids": ["fisherman", "greek-king-douban", "husband-parrot", "vizir-punished", "young-king-black-isles"]
    },
    "calenders-cycle": {
        "name": "The Three Calenders Cycle",
        "about": "Three one-eyed princes, each blinded by fate and curiosity, meet by chance at the house of three mysterious women in Bagdad. Each tells the tale of his misfortune. The longest cycle in the Nights, it explores the theme of forbidden knowledge — every prince loses an eye because he opened a door he was told not to open. The Bluebeard pattern, multiplied by three.",
        "ids": ["three-calenders-frame", "first-calender", "envious-man", "second-calender", "third-calender"]
    },
    "sindbad-cycle": {
        "name": "The Seven Voyages of Sindbad",
        "about": "Sindbad the Sailor tells his seven voyages to Sindbad the Porter — a poor man who complained about the injustice of wealth. Each voyage is a disaster survived: whale-islands, giant birds, cyclopes, cannibals, the Old Man of the Sea. The structure is repetitive and intentional: Sindbad goes out, is shipwrecked, faces wonders and horrors, finds treasure, returns. Seven times. The myth of the merchant-adventurer who cannot stop risking everything, no matter how much he already has.",
        "ids": ["sindbad-frame", "sindbad-voyage-1", "sindbad-voyage-2", "sindbad-voyage-3", "sindbad-voyage-4", "sindbad-voyage-5", "sindbad-voyage-6", "sindbad-voyage-7"]
    },
    "hunchback-cycle": {
        "name": "The Hunchback Cycle",
        "about": "A comic masterpiece: a hunchback dies (or seems to die) at a dinner party, and the terrified hosts pass his body from house to house, each thinking they have killed him. A Christian broker, a Jewish doctor, an Islamic steward, and a Chinese tailor each confess to the 'murder.' A barber and his six brothers provide the comic counterpoint. The darkest comedy in the Nights — death as farce, confession as entertainment.",
        "ids": ["little-hunchback", "barbers-fifth-brother", "barbers-sixth-brother"]
    },
    "love-tales": {
        "name": "Tales of Love and Devotion",
        "about": "The great love stories of the Nights — Prince Camaralzaman and Princess Badoura, whose love begins when jinns carry them together while they sleep; Noureddin and the Fair Persian, whose love survives exile and poverty. These are not fairy tales but romances: sprawling, passionate, full of disguise and mistaken identity, driven by the Nights' conviction that love is the force that moves the plot of the universe.",
        "ids": ["camaralzaman-badoura", "noureddin-persian"]
    },
    "magic-tales": {
        "name": "Tales of Magic and Wonder",
        "about": "The most famous stories of the Nights: Aladdin's lamp, the enchanted horse, the singing tree and the speaking bird. These are the stories that made the Nights world-famous — pure fantasy, where every wish has consequences, every magical object comes with a price, and the moral is always: be careful what you want, because you might get it.",
        "ids": ["aladdin", "enchanted-horse", "two-jealous-sisters"]
    },
    "caliph-tales": {
        "name": "The Caliph's Tales",
        "about": "Stories told in the court of Haroun-al-Raschid, the legendary Caliph of Bagdad who wandered his city in disguise to discover truth. The Blind Baba-Abdalla, punished for greed; Sidi-Nouman, cursed by a ghoul-wife; Ali Colia, whose trust is betrayed by olives. These are moral tales with judicial endings — the Caliph as the final arbiter of justice, wisdom personified as a man who listens.",
        "ids": ["haroun-al-raschid", "blind-baba-abdalla", "sidi-nouman", "ali-colia"]
    },
}

for cat_id, cycle in cycles.items():
    items.append({
        "id": f"cycle-{cat_id}",
        "name": cycle["name"],
        "sort_order": sort_order,
        "category": "cycles",
        "level": 2,
        "sections": {
            "About": cycle["about"],
            "For Readers": f"Read the stories in this cycle in order — the nesting is the point. Each tale is told by a character within the previous tale, creating the fractal structure that defines the Nights. Notice how each story earns something: time, a life, a pardon. Narrative is never free in the Nights — it always costs or saves."
        },
        "keywords": ["arabian-nights", "cycle", cat_id],
        "composite_of": cycle["ids"],
        "relationship_type": "emergence",
        "metadata": {}
    })
    sort_order += 1

# ═══════════════════════════════════════════════════════════════════════════
# L3: Meta cards
# ═══════════════════════════════════════════════════════════════════════════

items.append({
    "id": "meta-frame-tale",
    "name": "The Frame Tale: Story as Survival",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "Every story in the Nights exists because Scheherazade is telling it to stay alive. This frame is not decoration — it is the deepest statement the collection makes: narrative is a survival technology. The king kills because he has been traumatized (his wife's betrayal); Scheherazade heals because she tells stories. The thousand and one nights are a therapy session measured in cliffhangers. Marina Warner reads this as the archetypal demonstration of women's narrative power; the structure itself — stories within stories within stories — is Scheherazade's argument that the world is inexhaustible, and therefore worth living in.",
        "Contemplation": "When have you told a story to save something — a relationship, a mood, a child's bedtime? The Nights says all storytelling is this. We narrate to postpone the ending. We listen because we are not ready for dawn."
    },
    "keywords": ["frame-tale", "scheherazade", "survival", "narrative-power"],
    "composite_of": [f"cycle-{c}" for c in cycles],
    "relationship_type": "emergence",
    "metadata": {}
})
sort_order += 1

items.append({
    "id": "meta-nested-worlds",
    "name": "Nested Worlds: The Fractal Architecture of the Nights",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "sections": {
        "About": "The Arabian Nights invented a narrative structure that would not be rediscovered in Western literature until Borges: the mise en abyme, the story within the story within the story. The Fisherman tells the Genie a story. Within that story, the Greek King tells a story. Within that story, a parrot tells a story. This is not mere cleverness — it is a cosmology. The Nights proposes that reality itself is nested: every person contains stories, every story contains persons, and there is no bottom level. To read the Nights is to experience the vertigo of infinite regression — and to realize that this vertigo is the human condition.",
        "Contemplation": "You are inside a story right now — the story of your life, which is inside the story of your family, which is inside the story of your culture. How many levels deep can you see? And who is telling the outermost story?"
    },
    "keywords": ["nested", "fractal", "mise-en-abyme", "infinity"],
    "composite_of": ["cycle-merchants-genies", "cycle-fisherman-cycle", "cycle-calenders-cycle", "cycle-sindbad-cycle"],
    "relationship_type": "emergence",
    "metadata": {}
})
sort_order += 1

# ═══════════════════════════════════════════════════════════════════════════
# Build grammar
# ═══════════════════════════════════════════════════════════════════════════

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Andrew Lang (editor)", "date": "1898", "note": "Selected and edited edition, Longmans, Green and Co."},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar structure, cycle summaries, and meta interpretation"}
        ]
    },
    "name": "The Arabian Nights Entertainments",
    "description": "The Thousand and One Nights — one of the greatest story collections in world literature — told through Andrew Lang's 1898 selection. Thirty-four tales organized into eight story cycles, from the frame story of Scheherazade's life-saving narration through the voyages of Sindbad, the wonders of Aladdin, and the justice of Haroun-al-Raschid. Each story exists because a life depends on its telling.\n\nSource: Project Gutenberg eBook #128 (https://www.gutenberg.org/ebooks/128). Andrew Lang's edition, after Longmans, Green and Co, 1918 (1898).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Edmund Dulac's illustrations for Stories from the Arabian Nights (1907) — the definitive visual companion. Maxfield Parrish's Arabian Nights illustrations (1909). René Bull's illustrations for the Newnes edition. William Harvey's woodcuts for Lane's translation (1841). Persian and Mughal miniature paintings depicting scenes from Alf Layla wa-Layla.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": ["arabian-nights", "1001-nights", "fairy-tales", "frame-tale", "scheherazade", "storytelling", "persian", "arabic"],
    "roots": ["eastern-wisdom", "oral-tradition"],
    "shelves": ["wisdom", "wonder"],
    "lineages": ["Warner", "Shrei"],
    "worldview": "narrative",
    "items": items
}

# Save
import os
os.makedirs("grammars/arabian-nights", exist_ok=True)
with open("grammars/arabian-nights/grammar.json", "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

print(f"Stories extracted: {sum(1 for i in items if i['level'] == 1)}")
print(f"Cycles (L2): {sum(1 for i in items if i['level'] == 2)}")
print(f"Meta (L3): {sum(1 for i in items if i['level'] == 3)}")
print(f"Total items: {len(items)}")
print(f"Sections: {sum(len(i.get('sections', {})) for i in items)}")
