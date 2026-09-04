#!/usr/bin/env python3
"""
Parser for Andersen's Fairy Tales by Hans Christian Andersen (Project Gutenberg #1597).
Outputs grammar.json into grammars/andersens-fairy-tales/
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'andersens-fairy-tales.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'andersens-fairy-tales')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')

# Story definitions: title as it appears in the text, clean id, display name, metadata
STORY_DEFS = [
    {
        "title_pattern": "THE EMPEROR'S NEW CLOTHES",
        "id": "the-emperors-new-clothes",
        "name": "The Emperor's New Clothes",
        "keywords": ["vanity", "deception", "truth", "pride", "honesty", "children", "society"],
        "category": "vanity-tales",
        "reflection": "A child speaks the truth no one else dares say. When have you stayed silent because everyone around you seemed to agree? What gives a child the courage that adults lose?"
    },
    {
        "title_pattern": "THE SWINEHERD",
        "id": "the-swineherd",
        "name": "The Swineherd",
        "keywords": ["vanity", "love", "rejection", "disguise", "values", "superficiality"],
        "category": "vanity-tales",
        "reflection": "The princess rejects real beauty for cheap trinkets. What do you value — the genuine rose or the glittering toy? When have you overlooked something precious because it came in humble packaging?"
    },
    {
        "title_pattern": "THE REAL PRINCESS",
        "id": "the-real-princess",
        "name": "The Real Princess",
        "keywords": ["sensitivity", "royalty", "identity", "truth", "testing", "pea"],
        "category": "identity-tales",
        "reflection": "Sensitivity is the mark of a true princess in this tale. Is extreme sensitivity a strength or a weakness? What does it mean to be 'real' in a world full of pretense?"
    },
    {
        "title_pattern": "THE SHOES OF FORTUNE",
        "id": "the-shoes-of-fortune",
        "name": "The Shoes of Fortune",
        "keywords": ["wishes", "magic", "time-travel", "dissatisfaction", "contentment", "fortune"],
        "category": "transformation-tales",
        "reflection": "Every wish the shoes grant reveals that the grass is never greener. What wish would you make — and what unexpected consequences might follow? Are we ever truly satisfied with what we have?"
    },
    {
        "title_pattern": "THE FIR TREE",
        "id": "the-fir-tree",
        "name": "The Fir Tree",
        "keywords": ["impatience", "nostalgia", "presence", "christmas", "regret", "nature", "death"],
        "category": "nature-tales",
        "reflection": "The fir tree never enjoyed the present moment — always longing for what came next, then mourning what had passed. Where in your life are you the fir tree, missing today while dreaming of tomorrow?"
    },
    {
        "title_pattern": "THE SNOW QUEEN",
        "id": "the-snow-queen",
        "name": "The Snow Queen",
        "keywords": ["love", "friendship", "cold", "warmth", "courage", "journey", "good-vs-evil", "innocence"],
        "category": "love-tales",
        "reflection": "Gerda's love for Kay is so strong it melts the Snow Queen's power. What in your life has the warmth to melt ice? When has love carried you through impossible obstacles?"
    },
    {
        "title_pattern": "THE LEAP-FROG",
        "id": "the-leap-frog",
        "name": "The Leap-Frog",
        "keywords": ["competition", "wit", "judgment", "appearance", "marriage", "irony"],
        "category": "vanity-tales",
        "reflection": "The one who wins the princess is not the highest jumper but the cleverest. Is the world fair in how it rewards? What qualities truly win in the end — talent, luck, or something else?"
    },
    {
        "title_pattern": "THE ELDERBUSH",
        "id": "the-elderbush",
        "name": "The Elderbush",
        "keywords": ["memory", "aging", "nostalgia", "nature", "love", "elder-tree", "life-cycle"],
        "category": "nature-tales",
        "reflection": "An old couple remembers their whole life through the fragrance of elder blossoms. What scent or taste carries you back to a precious memory? How does nature hold our stories?"
    },
    {
        "title_pattern": "THE BELL",
        "id": "the-bell",
        "name": "The Bell",
        "keywords": ["seeking", "nature", "truth", "beauty", "humility", "spirituality"],
        "category": "nature-tales",
        "reflection": "Everyone hears the bell but few seek its source. The prince and the poor boy find it together — in nature itself. What mysterious sound or beauty calls to you that you have not yet followed?"
    },
    {
        "title_pattern": "THE OLD HOUSE",
        "id": "the-old-house",
        "name": "The Old House",
        "keywords": ["loneliness", "memory", "friendship", "aging", "tin-soldier", "kindness"],
        "category": "kindness-tales",
        "reflection": "A boy sends his tin soldier to keep a lonely old man company. What small act of kindness could you offer someone who is alone? How do objects carry the weight of memory and love?"
    },
    {
        "title_pattern": "THE HAPPY FAMILY",
        "id": "the-happy-family",
        "name": "The Happy Family",
        "keywords": ["snails", "contentment", "simplicity", "family", "humor", "nature"],
        "category": "nature-tales",
        "reflection": "The snails believe the burdock forest is the whole world, and they are perfectly happy. Is ignorance truly bliss? When is contentment wisdom, and when is it limitation?"
    },
    {
        "title_pattern": "THE STORY OF A MOTHER",
        "id": "the-story-of-a-mother",
        "name": "The Story of a Mother",
        "keywords": ["death", "sacrifice", "love", "grief", "mother", "loss", "acceptance"],
        "category": "death-tales",
        "reflection": "A mother gives everything — her eyes, her hair, her warmth — to find her child, only to learn she must let go. What would you sacrifice for love? And when is the deepest love the willingness to release?"
    },
    {
        "title_pattern": "THE FALSE COLLAR",
        "id": "the-false-collar",
        "name": "The False Collar",
        "keywords": ["vanity", "boasting", "rejection", "humor", "objects", "pride"],
        "category": "vanity-tales",
        "reflection": "The collar boasts and proposes to everyone, yet ends up as wastepaper. What happens when we define ourselves by appearance alone? When has pride led to a humbling fall?"
    },
    {
        "title_pattern": "THE SHADOW",
        "id": "the-shadow",
        "name": "The Shadow",
        "keywords": ["identity", "darkness", "power", "doppelganger", "death", "philosophy"],
        "category": "death-tales",
        "reflection": "The shadow becomes the master and the master becomes the shadow. What parts of yourself have you let grow so large they now control you? This is Andersen's darkest tale — what does it say about the cost of losing yourself?"
    },
    {
        "title_pattern": "THE LITTLE MATCH GIRL",
        "id": "the-little-match-girl",
        "name": "The Little Match Girl",
        "keywords": ["poverty", "death", "cold", "visions", "grandmother", "compassion", "christmas"],
        "category": "death-tales",
        "reflection": "A child freezes to death while the world celebrates. This story asks not 'why did she die?' but 'where were we?' What suffering around you goes unseen? What warmth could you offer?"
    },
    {
        "title_pattern": "THE DREAM OF LITTLE TUK",
        "id": "the-dream-of-little-tuk",
        "name": "The Dream of Little Tuk",
        "keywords": ["dreams", "learning", "geography", "imagination", "childhood", "education"],
        "category": "transformation-tales",
        "reflection": "Little Tuk learns his geography lesson through a magical dream. How does imagination transform dull lessons into living knowledge? What have you learned most deeply through experience rather than memorization?"
    },
    {
        "title_pattern": "THE NAUGHTY BOY",
        "id": "the-naughty-boy",
        "name": "The Naughty Boy",
        "keywords": ["cupid", "love", "mischief", "old-man", "arrows", "heartbreak"],
        "category": "love-tales",
        "reflection": "Cupid appears as a shivering child, and the old man who helps him gets an arrow to the heart. Love arrives uninvited and wounds even the wisest. When has love caught you off guard?"
    },
    {
        "title_pattern": "THE RED SHOES",
        "id": "the-red-shoes",
        "name": "The Red Shoes",
        "keywords": ["vanity", "punishment", "repentance", "dancing", "obsession", "mercy", "redemption"],
        "category": "transformation-tales",
        "reflection": "Karen's red shoes force her to dance until she begs for her own feet to be cut off. What obsession or vanity has ever held you captive? How did you find release — through mercy, sacrifice, or surrender?"
    },
]


def read_seed():
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK ANDERSEN'S FAIRY TALES ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK ANDERSEN'S FAIRY TALES ***"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    # Also try alternate end markers
    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = text.find("End of Project Gutenberg")
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def strip_front_matter(text):
    """Remove title page and table of contents.
    Start from 'THE EMPEROR'S NEW CLOTHES' which is the first story."""
    idx = text.find("\nTHE EMPEROR'S NEW CLOTHES\n")
    if idx != -1:
        return text[idx:].strip()
    return text


def extract_stories(text):
    """Split text into individual stories based on title patterns."""
    stories = []

    # Build a list of (position, story_def_index) for each story title found
    positions = []
    for i, sdef in enumerate(STORY_DEFS):
        pattern = "\n" + sdef["title_pattern"] + "\n"
        idx = text.find(pattern)
        if idx != -1:
            positions.append((idx, i))
        else:
            # Try without leading newline (for first story)
            if text.startswith(sdef["title_pattern"] + "\n"):
                positions.append((0, i))
            else:
                print(f"WARNING: Could not find story: {sdef['title_pattern']}")

    # Sort by position in text
    positions.sort(key=lambda x: x[0])

    for pos_idx, (start_pos, def_idx) in enumerate(positions):
        sdef = STORY_DEFS[def_idx]

        # Find end of this story (start of next story or end of text)
        if pos_idx + 1 < len(positions):
            end_pos = positions[pos_idx + 1][0]
        else:
            end_pos = len(text)

        story_text = text[start_pos:end_pos].strip()

        # Remove the title line from the story text
        lines = story_text.split('\n')
        content_start = 0
        for j, line in enumerate(lines):
            stripped = line.strip()
            if stripped == '':
                continue
            # Check if this line is the title (all caps and matches)
            if stripped.upper() == stripped and len(stripped) > 2:
                content_start = j + 1
            else:
                break

        story_content = '\n'.join(lines[content_start:]).strip()

        # Clean up: remove excessive blank lines
        story_content = re.sub(r'\n{3,}', '\n\n', story_content)

        # Remove any trailing blank lines or whitespace
        story_content = story_content.rstrip()

        stories.append({
            "def_idx": def_idx,
            "text": story_content
        })

    return stories


def build_l1_items(stories):
    """Build L1 items from extracted stories."""
    items = []
    for sort_order, story in enumerate(stories):
        sdef = STORY_DEFS[story["def_idx"]]

        sections = {
            "Story": story["text"].strip(),
            "Reflection": sdef["reflection"]
        }

        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "level": 1,
            "category": sdef["category"],
            "sections": sections,
            "keywords": sdef["keywords"],
            "metadata": {
                "source": "Andersen's Fairy Tales, Hans Christian Andersen, Project Gutenberg #1597"
            }
        }
        items.append(item)

    return items


def build_l2_items(l1_items):
    """Build L2 groupings by theme and character type."""
    l2_items = []
    sort_order = len(l1_items)

    # --- Theme groupings ---
    theme_groups = [
        {
            "id": "theme-transformation-and-redemption",
            "name": "Transformation and Redemption",
            "category": "themes",
            "about": "Tales of magical change — wishes that go wrong, shoes that dance on their own, dreams that teach, and the painful path from vanity to grace. Andersen's transformations are never easy: they require suffering, surrender, or the loss of something precious before a new self can emerge.",
            "for_parents": "These stories explore how people change — sometimes through magic, sometimes through hard experience. Ask children: What did the character have to give up to be transformed? Was the change worth it? These tales can open conversations about growth, making mistakes, and the courage it takes to become someone new.",
            "member_ids": ["the-shoes-of-fortune", "the-red-shoes", "the-dream-of-little-tuk"],
            "keywords": ["transformation", "change", "magic", "redemption", "growth"]
        },
        {
            "id": "theme-kindness-and-compassion",
            "name": "Kindness and Compassion",
            "category": "themes",
            "about": "Stories where small acts of kindness illuminate dark worlds — a boy sending his tin soldier to a lonely old man, Gerda's tears melting the Snow Queen's spell. Andersen knew loneliness deeply, and his kindest stories carry the weight of someone who understood what it means to be on the outside looking in.",
            "for_parents": "These are gentle stories that show children the power of small kindnesses. They are especially good for talking about loneliness and how to notice when someone needs a friend. Ask: Who in the story was lonely? What small thing made the biggest difference?",
            "member_ids": ["the-old-house", "the-snow-queen", "the-little-match-girl"],
            "keywords": ["kindness", "compassion", "loneliness", "friendship", "warmth"]
        },
        {
            "id": "theme-nature-and-wonder",
            "name": "Nature and Wonder",
            "category": "themes",
            "about": "Andersen found magic in the natural world — in elder trees that hold a lifetime of memories, in bells that ring from the heart of nature, in snail families content beneath burdock leaves, and in fir trees that never learned to enjoy the forest. These tales reveal a world alive with meaning, where every plant and creature has its own story.",
            "for_parents": "Take these stories outside! Read 'The Fir Tree' beside a real tree. Listen for bells in nature after reading 'The Bell.' Andersen's nature tales teach children to pay attention to the living world around them. Ask: What story might this flower tell? What would the birds say if they could talk?",
            "member_ids": ["the-fir-tree", "the-elderbush", "the-bell", "the-happy-family"],
            "keywords": ["nature", "trees", "wonder", "beauty", "presence", "seasons"]
        },
        {
            "id": "theme-vanity-and-pride",
            "name": "Vanity and Pride",
            "category": "themes",
            "about": "Nobody skewered vanity like Andersen. From the Emperor parading naked to the collar proposing to everyone it meets, these stories expose the absurdity of pride with wit, irony, and a child's clear-eyed honesty. The princess who rejects a real rose for a mechanical toy and the leap-frog who wins by luck — Andersen's satirical eye spares no one.",
            "for_parents": "These are funny stories with serious lessons. Children instinctively understand the Emperor's foolishness — they ARE the child who shouts 'But he has nothing on!' Use these tales to talk about peer pressure, honesty, and the difference between what things look like and what they really are.",
            "member_ids": ["the-emperors-new-clothes", "the-swineherd", "the-leap-frog", "the-false-collar"],
            "keywords": ["vanity", "pride", "honesty", "satire", "appearance", "truth"]
        },
        {
            "id": "theme-love-and-sacrifice",
            "name": "Love and Sacrifice",
            "category": "themes",
            "about": "Love in Andersen's world is fierce, sacrificial, and often heartbreaking. A mother trades her eyes and hair to find her dying child. Gerda walks barefoot across the world for her friend Kay. Cupid's arrow strikes the kindly old man. These are not sweet romances — they are stories about love as a force that transforms, wounds, and ultimately redeems.",
            "for_parents": "These stories treat love with profound seriousness. 'The Story of a Mother' is among the most powerful tales ever written about parental love and may bring tears. Read these with older children and be prepared for deep conversations about what we would give up for those we love.",
            "member_ids": ["the-snow-queen", "the-story-of-a-mother", "the-naughty-boy"],
            "keywords": ["love", "sacrifice", "devotion", "grief", "motherhood", "heartbreak"]
        },
        {
            "id": "theme-death-and-darkness",
            "name": "Death and Darkness",
            "category": "themes",
            "about": "Andersen did not shield children from death. The little match girl freezes on New Year's Eve. The shadow swallows the scholar. The mother must surrender her child to Death. These are haunting, unforgettable tales that treat mortality with honesty and tenderness — acknowledging that darkness is part of life, not something to be hidden from.",
            "for_parents": "These are Andersen's most challenging stories and should be read with care depending on the child's age and readiness. They are profoundly valuable for children who have experienced loss or who are beginning to understand mortality. Never force these stories — let children come to them when ready. Ask gently: How did this story make you feel? What questions do you have?",
            "member_ids": ["the-little-match-girl", "the-shadow", "the-story-of-a-mother", "the-red-shoes"],
            "keywords": ["death", "darkness", "loss", "mortality", "grief", "acceptance"]
        },
    ]

    # --- Character type groupings ---
    character_groups = [
        {
            "id": "characters-royalty-and-nobility",
            "name": "Royalty and Nobility",
            "category": "characters",
            "about": "Emperors, princes, and princesses populate Andersen's world — but rarely as heroes. The Emperor is a vain fool, the princess rejects genuine beauty, and the 'real' princess is identified by her neurotic sensitivity. Andersen, the son of a cobbler, wrote royalty with a mix of fascination and subversive irony.",
            "for_parents": "These stories question authority and status. They show children that being a king or princess does not make you wise or good. Ask: Was the Emperor really powerful? What makes someone truly noble — a crown or their character?",
            "member_ids": ["the-emperors-new-clothes", "the-swineherd", "the-real-princess", "the-leap-frog"],
            "keywords": ["royalty", "emperor", "princess", "prince", "authority", "status"]
        },
        {
            "id": "characters-children-and-innocence",
            "name": "Children and Innocence",
            "category": "characters",
            "about": "Andersen's children are truth-tellers, dreamers, and sufferers. The child who exposes the Emperor, little Tuk who learns through dreams, the match girl who sees visions of warmth, Gerda whose innocent love defeats the Snow Queen — children in Andersen represent clarity of vision and the courage adults have lost.",
            "for_parents": "These stories honor the child's perspective. They validate what children already know: that they see things adults miss, that their feelings are real, and that their love is powerful. Ask your child: What do you notice that grown-ups don't see?",
            "member_ids": ["the-emperors-new-clothes", "the-snow-queen", "the-little-match-girl", "the-dream-of-little-tuk", "the-naughty-boy", "the-red-shoes"],
            "keywords": ["children", "innocence", "truth", "dreams", "vision", "courage"]
        },
        {
            "id": "characters-lonely-and-forgotten",
            "name": "The Lonely and Forgotten",
            "category": "characters",
            "about": "The old man in the old house, the fir tree discarded after Christmas, the match girl invisible to the celebrating crowd — Andersen returns again and again to figures who are overlooked, discarded, or forgotten. As an outsider himself, he gave voice to those society ignores.",
            "for_parents": "These stories build empathy. They ask children to notice who is missing from the celebration, who sits alone, who has been thrown away. After reading, ask: Who in your school or neighborhood might feel like the old man in the old house? What could you do?",
            "member_ids": ["the-old-house", "the-fir-tree", "the-little-match-girl", "the-shadow"],
            "keywords": ["loneliness", "forgotten", "outsider", "empathy", "invisibility"]
        },
        {
            "id": "characters-talking-objects",
            "name": "Talking Objects and Animals",
            "category": "characters",
            "about": "Collars that boast, snails that philosophize, tin soldiers that travel, and elder trees that remember. Andersen animated the entire material world, giving voice to objects and creatures that reveal human nature through their small, absurd dramas. This is his most distinctive gift — finding the epic in the everyday.",
            "for_parents": "Children already imagine their toys are alive — Andersen validates this. These stories are wonderful for creative play. After reading, ask: If your favorite toy could talk, what would it say? What story would your shoes tell about today?",
            "member_ids": ["the-false-collar", "the-happy-family", "the-fir-tree", "the-elderbush", "the-old-house"],
            "keywords": ["objects", "animals", "animation", "imagination", "humor"]
        },
    ]

    for group in theme_groups:
        l2_items.append({
            "id": group["id"],
            "name": group["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": group["category"],
            "sections": {
                "About": group["about"],
                "For Parents": group["for_parents"]
            },
            "keywords": group["keywords"],
            "composite_of": group["member_ids"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    for group in character_groups:
        l2_items.append({
            "id": group["id"],
            "name": group["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": group["category"],
            "sections": {
                "About": group["about"],
                "For Parents": group["for_parents"]
            },
            "keywords": group["keywords"],
            "composite_of": group["member_ids"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    return l2_items, sort_order


def build_l3_items(start_sort_order):
    """Build L3 meta-categories."""
    l3_items = []
    sort_order = start_sort_order

    l3_defs = [
        {
            "id": "meta-themes",
            "name": "Themes and Morals",
            "category": "meta",
            "about": "The great currents running through Andersen's fairy tales: transformation, kindness, nature's wonder, the folly of vanity, the power of love, and the reality of death. Unlike the Grimms' sturdy peasant morality, Andersen's themes are deeply personal — shaped by his own loneliness, ambition, and longing for acceptance. His stories do not always end happily, but they always end honestly.",
            "how_to_use": "Browse by theme to find stories that match a mood, a question, or a teaching moment. The vanity tales are wonderful for humor and discussion. The death tales require more care and readiness. The nature tales are perfect for reading outdoors. Let the themes guide you to the story the moment calls for.",
            "composite_of": [
                "theme-transformation-and-redemption",
                "theme-kindness-and-compassion",
                "theme-nature-and-wonder",
                "theme-vanity-and-pride",
                "theme-love-and-sacrifice",
                "theme-death-and-darkness"
            ],
            "keywords": ["themes", "morals", "values", "andersen"]
        },
        {
            "id": "meta-characters",
            "name": "Character Types",
            "category": "meta",
            "about": "The archetypal figures of Andersen's world: foolish royalty, clear-eyed children, lonely outcasts, and talking objects. Andersen populated his stories with characters drawn from every level of society and every corner of the material world. His royalty are satirical, his children are wise, his outcasts are heartbreaking, and his objects are philosophically absurd.",
            "how_to_use": "Browse by character type to discover patterns across the tales. Notice how Andersen treats royalty versus children, or how objects reveal what people cannot say about themselves. These groupings reveal Andersen's deepest sympathies — always with the small, the overlooked, and the honest.",
            "composite_of": [
                "characters-royalty-and-nobility",
                "characters-children-and-innocence",
                "characters-lonely-and-forgotten",
                "characters-talking-objects"
            ],
            "keywords": ["characters", "archetypes", "types"]
        }
    ]

    for l3 in l3_defs:
        l3_items.append({
            "id": l3["id"],
            "name": l3["name"],
            "sort_order": sort_order,
            "level": 3,
            "category": l3["category"],
            "sections": {
                "About": l3["about"],
                "How to Use": l3["how_to_use"]
            },
            "keywords": l3["keywords"],
            "composite_of": l3["composite_of"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    return l3_items


def build_grammar(l1_items, l2_items, l3_items):
    """Assemble the complete grammar."""
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Hans Christian Andersen",
                    "date": "1835-1872",
                    "note": "Author of the original fairy tales"
                },
                {
                    "name": "Project Gutenberg",
                    "date": "1999",
                    "note": "Digital text, eBook #1597. Produced by Dianne Bean and David Widger."
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure and reflections"
                }
            ]
        },
        "name": "Andersen's Fairy Tales",
        "description": "Eighteen fairy tales by Hans Christian Andersen (1805-1875), the Danish master whose stories transformed children's literature forever. From the naked Emperor to the freezing match girl, from the Snow Queen's icy palace to the red shoes that would not stop dancing, these tales blend wonder, humor, and an unflinching honesty about suffering that sets Andersen apart from all other fairy tale writers. Unlike the Grimms, Andersen wrote original literary fairy tales drawn from his own imagination and his own pain — and they are among the most widely translated works in all of literature. Source: Project Gutenberg eBook #1597 (https://www.gutenberg.org/ebooks/1597).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Vilhelm Pedersen's original illustrations for Andersen's tales (1849-1850s) — the first and most iconic illustrations, pen-and-ink, public domain. Lorenz Frølich's illustrations (1870s) — refined pen-and-ink drawings, public domain. Arthur Rackham's illustrations for 'Fairy Tales by Hans Andersen' (1932, Harrap) — watercolor and pen-and-ink in Rackham's distinctive style, public domain. Edmund Dulac's illustrations for 'Stories from Hans Andersen' (1911, Hodder & Stoughton) — luminous color plates, public domain. W. Heath Robinson's illustrations for 'Hans Andersen's Fairy Tales' (1913, Constable) — pen-and-ink with gentle humor, public domain. Kay Nielsen's illustrations for 'Fairy Tales by Hans Andersen' (1924, Hodder & Stoughton) — Art Nouveau masterworks, public domain.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "fairy-tales",
            "kids",
            "danish",
            "andersen",
            "morals",
            "fantasy",
            "classic",
            "oracle"
        ],
        "roots": ["european-letters", "romanticism"],
        "shelves": ["children", "wonder"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "devotional",
        "cover_image_url": "",
        "items": l1_items + l2_items + l3_items
    }

    return grammar


def main():
    print("Reading seed text...")
    raw_text = read_seed()

    print("Stripping Gutenberg header/footer...")
    text = strip_gutenberg(raw_text)

    print("Stripping front matter...")
    text = strip_front_matter(text)

    print("Extracting stories...")
    stories = extract_stories(text)
    print(f"  Found {len(stories)} stories")

    if len(stories) != len(STORY_DEFS):
        print(f"  WARNING: Expected {len(STORY_DEFS)} stories, found {len(stories)}")

    print("Building L1 items...")
    l1_items = build_l1_items(stories)

    print("Building L2 items...")
    l2_items, next_sort = build_l2_items(l1_items)

    print("Building L3 items...")
    l3_items = build_l3_items(next_sort)

    print("Assembling grammar...")
    grammar = build_grammar(l1_items, l2_items, l3_items)

    # Ensure output directory exists
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
