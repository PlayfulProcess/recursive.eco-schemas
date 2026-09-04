#!/usr/bin/env python3
"""
Build grammar.json for the Song of Songs (Song of Solomon) from KJV Bible seed text.

Source: Project Gutenberg eBook #10900 (The King James Bible)
The Song of Songs is located between Ecclesiastes and Isaiah in the full KJV text.

Structure:
- 8 chapters of love poetry
- L1: Individual chapters (8)
- L2: Thematic groupings (by movement of the love story)
- L3: Meta-category
"""

import json
import re
from pathlib import Path

SEED_PATH = Path(__file__).parent.parent / "seeds" / "song-of-songs.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "song-of-songs"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"


def read_and_extract():
    """Read KJV Bible and extract Song of Solomon."""
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    # Find the actual Song of Solomon text (not the table of contents entry)
    # The actual text starts with the heading followed by "Chapter" and then verse 1:1
    start_marker = "\nSong of Solomon\n\nChapter\n"
    start_idx = text.find(start_marker)
    if start_idx == -1:
        # Try alternate: sometimes the heading is just before 1:1
        start_idx = text.find("\n1:1 The song of songs")
        if start_idx == -1:
            raise ValueError("Could not find Song of Solomon text")

    # Find the next book - Isaiah
    end_idx = text.find("\n\n\n\n\n\nIsaiah\n", start_idx)
    if end_idx == -1:
        end_idx = text.find("\nIsaiah\n\nChapter\n", start_idx)
    if end_idx == -1:
        # Fallback: find Isaiah anywhere after Song of Solomon
        end_idx = text.find("\nIsaiah\n", start_idx + 100)
    if end_idx == -1:
        raise ValueError("Could not find Isaiah marker")

    return text[start_idx:end_idx].strip()


def parse_chapters(text):
    """Parse the Song into chapters, each containing its verses."""
    # Find all verses with chapter:verse pattern
    verse_pattern = re.compile(r'^(\d+):(\d+)\s+(.+?)(?=\n\d+:\d+|\n\n\n|\Z)', re.MULTILINE | re.DOTALL)

    chapters = {}
    for match in verse_pattern.finditer(text):
        ch = int(match.group(1))
        vs = int(match.group(2))
        content = match.group(3).strip()
        # Join continuation lines
        content = ' '.join(line.strip() for line in content.split('\n') if line.strip())

        if ch not in chapters:
            chapters[ch] = []
        chapters[ch].append((vs, content))

    return chapters


def format_chapter(verses):
    """Format a list of (verse_num, text) tuples into readable text."""
    lines = []
    for vs, text in sorted(verses):
        lines.append(f"{vs}. {text}")
    return '\n\n'.join(lines)


def build_grammar():
    song_text = read_and_extract()
    chapters = parse_chapters(song_text)

    if len(chapters) != 8:
        print(f"Warning: Expected 8 chapters, found {len(chapters)}: {sorted(chapters.keys())}")

    items = []
    so = 0

    def add_item(item):
        nonlocal so
        item["sort_order"] = so
        items.append(item)
        so += 1

    # =========================================================================
    # L1 ITEMS - Individual chapters
    # =========================================================================

    chapter_info = [
        {
            "id": "chapter-1",
            "name": "Chapter 1: The Song Begins -- Desire and Dark Beauty",
            "about": "The Beloved speaks first: 'Let him kiss me with the kisses of his mouth.' She declares herself 'black but comely' -- darkened by the sun, made keeper of others' vineyards while neglecting her own. The Lover responds with praise, comparing her to a mare among Pharaoh's chariots. Their exchange pulses with longing and the intoxication of new love.",
            "reflection": "What does it mean to be beautiful on one's own terms? How does the Beloved's self-description challenge conventional beauty standards even today?",
            "keywords": ["desire", "beauty", "dark-skin", "vineyards", "kisses", "longing"]
        },
        {
            "id": "chapter-2",
            "name": "Chapter 2: The Rose of Sharon -- Spring and Invitation",
            "about": "'I am the rose of Sharon, and the lily of the valleys.' The Beloved declares herself in the language of flowers. The Lover invites her to rise: 'the winter is past, the rain is over and gone; the flowers appear on the earth.' The world itself blossoms in response to their love. She warns the daughters of Jerusalem not to awaken love before its time.",
            "reflection": "When has love transformed how you see the natural world? What does the refrain 'stir not up nor awake my love till he please' mean about the timing of love?",
            "keywords": ["rose", "lily", "spring", "flowers", "invitation", "awakening"]
        },
        {
            "id": "chapter-3",
            "name": "Chapter 3: The Night Search -- Seeking the Beloved",
            "about": "By night on her bed she seeks the one her soul loves -- and cannot find him. She rises, goes through the city streets, asks the watchmen. At last she finds him and will not let him go. The chapter then shifts to Solomon's wedding procession: sixty warriors, a chariot of Lebanon wood, pillars of silver. Public ceremony frames private passion.",
            "reflection": "What does it feel like to search for someone in the dark? How does the transition from private longing to public celebration illuminate the nature of love?",
            "keywords": ["night", "seeking", "city", "watchmen", "solomon", "procession", "wedding"]
        },
        {
            "id": "chapter-4",
            "name": "Chapter 4: The Garden Enclosed -- Praise of the Beloved",
            "about": "The Lover's most extended praise: 'Behold, thou art fair, my love.' He describes her from eyes (doves behind a veil) to breasts (twin fawns among lilies), from the tower of her neck to the pomegranate of her temples. She is a garden enclosed, a spring shut up, a fountain sealed. He calls the winds to blow upon his garden -- and she opens: 'Let my beloved come into his garden.'",
            "reflection": "How does the language of gardens and nature express what direct speech cannot? What does the image of the 'enclosed garden' say about intimacy, privacy, and the gift of opening oneself?",
            "keywords": ["garden", "praise", "beauty", "doves", "lilies", "fountain", "Lebanon", "spices"]
        },
        {
            "id": "chapter-5",
            "name": "Chapter 5: The Missed Encounter -- Longing and Loss",
            "about": "He knocks at night but she hesitates -- her hands drip with myrrh on the lock -- and when she opens, he is gone. She searches the city again but this time the watchmen find her and strike her. The daughters of Jerusalem ask: 'What is thy beloved more than another beloved?' She responds with the poem's most famous blazon: 'My beloved is white and ruddy, the chiefest among ten thousand.'",
            "reflection": "Why does she hesitate at the door? What do the watchmen represent? How does the pain of missing someone deepen our understanding of what they mean to us?",
            "keywords": ["hesitation", "myrrh", "loss", "watchmen", "blazon", "praise", "ten-thousand"]
        },
        {
            "id": "chapter-6",
            "name": "Chapter 6: The Return -- Finding and Being Found",
            "about": "'My beloved is gone down into his garden.' The separation resolves as she finds him among the lilies. He responds with renewed praise: she is beautiful as Tirzah, terrible as an army with banners. Among sixty queens and eighty concubines, she is the unique one, the perfect one, the only one of her mother.",
            "reflection": "What does it mean to be someone's 'only one'? How does the image of beauty that is also 'terrible as an army with banners' expand our understanding of love's power?",
            "keywords": ["return", "garden", "lilies", "tirzah", "uniqueness", "army", "queens"]
        },
        {
            "id": "chapter-7",
            "name": "Chapter 7: The Dance -- Celebration of the Body",
            "about": "The Shulamite dances and the Lover praises her body from feet to crown: her navel is a round goblet, her belly a heap of wheat set about with lilies, her stature like a palm tree. 'I said, I will go up to the palm tree, I will take hold of the boughs thereof.' She invites him to the fields, the vineyards, the villages. 'There will I give thee my loves.'",
            "reflection": "How does the celebration of the body become a celebration of the whole person? What is the relationship between physical desire and spiritual devotion in this poem?",
            "keywords": ["dance", "body", "palm-tree", "vineyards", "fields", "desire", "celebration"]
        },
        {
            "id": "chapter-8",
            "name": "Chapter 8: Love Strong as Death -- The Seal",
            "about": "The poem's climax and conclusion: 'Set me as a seal upon thine heart, as a seal upon thine arm: for love is strong as death; jealousy is cruel as the grave: the coals thereof are coals of fire, which hath a most vehement flame. Many waters cannot quench love, neither can the floods drown it.' The little sister, the vineyard, Solomon's thousand -- all resolve into the final call: 'Make haste, my beloved.'",
            "reflection": "What does it mean that love is 'strong as death'? In what sense is the deepest love a kind of fire that nothing can extinguish? How does the poem's ending echo its beginning?",
            "keywords": ["seal", "death", "fire", "waters", "jealousy", "vineyard", "closure", "flame"]
        }
    ]

    chapter_ids = []
    for i, info in enumerate(chapter_info):
        ch_num = i + 1
        verses = chapters.get(ch_num, [])
        chapter_ids.append(info["id"])
        add_item({
            "id": info["id"],
            "name": info["name"],
            "level": 1,
            "category": "chapter",
            "sections": {
                "Verse": format_chapter(verses),
                "About": info["about"],
                "Reflection": info["reflection"]
            },
            "keywords": info["keywords"],
            "metadata": {"chapter": ch_num, "verse_count": len(verses)}
        })

    # =========================================================================
    # L2 ITEMS - Thematic groupings
    # =========================================================================

    add_item({
        "id": "theme-awakening",
        "name": "The Awakening of Desire (Chapters 1-3)",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "The first movement of the Song traces desire from its first spark ('Let him kiss me') through the blossoming of spring to the frantic night search through the city. Love declares itself, nature responds, and the beloved learns that what the soul loves cannot be summoned but must be sought. The refrain to the daughters of Jerusalem -- 'stir not up love till he please' -- warns that love has its own timing.",
            "For Readers": "These three chapters move from longing to ecstasy to anxious seeking. Notice how the natural world (vineyards, lilies, foxes, the spring rains) becomes the language of inner experience. This is poetry that erases the boundary between body and landscape."
        },
        "keywords": ["awakening", "desire", "spring", "seeking", "nature"],
        "metadata": {},
        "composite_of": ["chapter-1", "chapter-2", "chapter-3"]
    })

    add_item({
        "id": "theme-praise-and-loss",
        "name": "Praise and Loss: The Garden of the Body (Chapters 4-6)",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "The central movement presents the Song's deepest paradox: the beloved is most fully praised at the moment of potential loss. Chapter 4's exquisite garden imagery opens into chapter 5's missed encounter -- she hesitates, he vanishes, and the watchmen wound her. Only through loss does she discover how to describe what she loves. Chapter 6 resolves the crisis: he is found again in his garden.",
            "For Readers": "The middle section contains the Song's most intense imagery and its most painful moment. The pattern of finding-losing-finding is the heartbeat of all great love poetry. Notice how each separation deepens the lovers' knowledge of each other."
        },
        "keywords": ["praise", "loss", "garden", "separation", "reunion", "blazon"],
        "metadata": {},
        "composite_of": ["chapter-4", "chapter-5", "chapter-6"]
    })

    add_item({
        "id": "theme-consummation",
        "name": "Love Strong as Death: Consummation and Seal (Chapters 7-8)",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "The final movement celebrates the body in ecstatic dance and arrives at the poem's supreme declaration: love is strong as death, unquenchable by many waters. The personal becomes cosmic. The vineyard imagery from chapter 1 returns transformed -- Solomon's thousand pieces of silver are nothing beside the vineyard of the beloved. The poem ends as it began, with a cry of urgency: 'Make haste, my beloved.'",
            "For Readers": "Chapter 8 contains what may be the most powerful lines ever written about love. 'Set me as a seal upon thine heart' has been recited at weddings for three thousand years. Consider why this ancient poem still speaks so directly to the experience of love."
        },
        "keywords": ["consummation", "death", "seal", "fire", "water", "vineyard", "eternity"],
        "metadata": {},
        "composite_of": ["chapter-7", "chapter-8"]
    })

    # =========================================================================
    # L3 ITEMS - Meta-category
    # =========================================================================

    add_item({
        "id": "meta-song-of-songs",
        "name": "The Song of Songs: Sacred Eros",
        "level": 3,
        "category": "meta-category",
        "sections": {
            "About": "The Song of Songs is the most extraordinary text in the biblical canon: an unabashed celebration of erotic love between two unnamed lovers, set among the gardens, vineyards, and hills of ancient Israel. It contains no mention of God, no moral instruction, no narrative of salvation -- only the voices of desire, praise, longing, and consummation. Jewish tradition reads it as an allegory of God's love for Israel; Christian tradition as Christ's love for the Church; but its primary meaning is the holiness of human love itself. It is the oldest and greatest love poem in Western literature.",
            "For Readers": "Whether you read it as sacred allegory or secular poetry (or both), the Song of Songs insists that bodily love -- the love of skin and scent, of gardens and gazelles, of night searches and morning praise -- is not opposed to spiritual depth but is its very medium. 'Love is strong as death' is a theological statement made entirely through the language of desire."
        },
        "keywords": ["song-of-songs", "sacred", "eros", "love", "beauty", "death", "garden", "seal", "bible"],
        "metadata": {},
        "composite_of": ["theme-awakening", "theme-praise-and-loss", "theme-consummation"]
    })

    # =========================================================================
    # BUILD GRAMMAR
    # =========================================================================

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Unknown (attributed to Solomon)", "date": "c. 950-300 BCE", "note": "Author"},
                {"name": "King James Bible translators", "date": "1611", "note": "Translation"},
                {"name": "Project Gutenberg", "date": "2004", "note": "Source: eBook #10900 (https://www.gutenberg.org/ebooks/10900)"}
            ]
        },
        "name": "Song of Songs",
        "description": "The Song of Songs (Song of Solomon) -- the Bible's great poem of erotic love, in 8 chapters of dialogue between two unnamed lovers. One of the oldest and most beautiful love poems in world literature, it celebrates desire, beauty, longing, and union through the imagery of gardens, vineyards, and the natural world. From the King James Version.\n\nSource: Project Gutenberg eBook #10900 (https://www.gutenberg.org/ebooks/10900)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Marc Chagall's Song of Songs illustrations (1957-1966, check copyright); Gustave Moreau's biblical paintings of love and beauty (1880s); medieval manuscript illuminations of the Song of Songs from the Rothschild Canticles (c. 1300).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["poetry", "love", "bible", "sacred", "eros", "beauty", "garden", "desire", "ancient-world", "hebrew"],
        "roots": ["emotion-love"],
        "shelves": ["wonder"],
        "lineages": ["Shrei", "Johnson"],
        "worldview": "devotional",
        "items": items
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    total_verses = sum(len(chapters.get(i, [])) for i in range(1, 9))
    print(f"Built Song of Songs grammar: {len(items)} items, {total_verses} verses across 8 chapters")
    for item in items:
        verse = item["sections"].get("Verse", "")
        print(f"  L{item['level']}: {item['id']} - {item['name']} ({len(verse)} chars)")


if __name__ == "__main__":
    build_grammar()
