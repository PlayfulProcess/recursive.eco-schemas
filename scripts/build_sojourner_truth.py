#!/usr/bin/env python3
"""
Parse "Narrative of Sojourner Truth" (Gutenberg #1674, 1850)
into a grammar.json.

Structure:
- L1: Individual chapters (30 chapters + certificates appendix)
- L2: Thematic groupings (7 themes tracing the arc from slavery to prophecy)
- L3: Meta-category ("The Journey from Isabella to Sojourner Truth")
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "sojourner-truth.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "sojourner-truth")
OUTPUT = os.path.join(OUTPUT_DIR, "grammar.json")


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1:
        text = text[text.index("\n", start) + 1:]
    if end != -1:
        text = text[:end]
    return text.strip()


# Chapter definitions: (body_heading, slug, display_name, keywords)
# Body headings include the period and exact casing as they appear in the text.
CHAPTERS = [
    ("HER BIRTH AND PARENTAGE.", "her-birth-and-parentage",
     "Her Birth and Parentage",
     ["birth", "parentage", "slavery", "Ulster County", "Dutch"]),
    ("ACCOMMODATIONS.", "accommodations",
     "Accommodations",
     ["cellar", "conditions", "poverty", "enslaved-quarters"]),
    ("HER BROTHERS AND SISTERS.", "her-brothers-and-sisters",
     "Her Brothers and Sisters",
     ["family", "siblings", "separation", "auction"]),
    ("HER RELIGIOUS INSTRUCTION.", "her-religious-instruction",
     "Her Religious Instruction",
     ["religion", "prayer", "God", "instruction"]),
    ("THE AUCTION.", "the-auction",
     "The Auction",
     ["auction", "sale", "property", "separation"]),
    ("DEATH OF MAU-MAU BETT.", "death-of-mau-mau-bett",
     "Death of Mau-Mau Bett",
     ["death", "mother", "Mau-Mau Bett", "grief"]),
    ("LAST DAYS OF BOMEFREE.", "last-days-of-bomefree",
     "Last Days of Bomefree",
     ["father", "Bomefree", "aging", "abandonment"]),
    ("DEATH OF BOMEFREE.", "death-of-bomefree",
     "Death of Bomefree",
     ["death", "father", "Bomefree", "mourning"]),
    ("COMMENCEMENT OF ISABELLA'S TRIALS IN LIFE.", "commencement-of-isabellas-trials",
     "Commencement of Isabella's Trials in Life",
     ["trials", "suffering", "masters", "cruelty"]),
    ("TRIALS CONTINUED.", "trials-continued",
     "Trials Continued",
     ["trials", "suffering", "endurance", "labor"]),
    ("HER STANDING WITH HER NEW MASTER AND MISTRESS.", "her-standing-with-new-master",
     "Her Standing with Her New Master and Mistress",
     ["Dumont", "master", "mistress", "servitude"]),
    ("ISABELLA'S MARRIAGE.", "isabellas-marriage",
     "Isabella's Marriage",
     ["marriage", "Thomas", "family", "enslaved-marriage"]),
    ("ISABELLA AS A MOTHER.", "isabella-as-a-mother",
     "Isabella as a Mother",
     ["motherhood", "children", "family", "enslaved-motherhood"]),
    ("SLAVEHOLDER'S PROMISES.", "slaveholders-promises",
     "Slaveholder's Promises",
     ["promises", "freedom", "betrayal", "Dumont"]),
    ("HER ESCAPE.", "her-escape",
     "Her Escape",
     ["escape", "freedom", "Van Wagenen", "courage"]),
    ("ILLEGAL SALE OF HER SON.", "illegal-sale-of-her-son",
     "Illegal Sale of Her Son",
     ["son", "Peter", "illegal-sale", "Alabama", "justice"]),
    ("IT IS OFTEN DARKEST JUST BEFORE DAWN.", "darkest-before-dawn",
     "It Is Often Darkest Just Before Dawn",
     ["legal-battle", "son", "justice", "perseverance"]),
    ("DEATH OF MRS. ELIZA FOWLER.", "death-of-mrs-eliza-fowler",
     "Death of Mrs. Eliza Fowler",
     ["death", "Mrs. Fowler", "mourning", "faith"]),
    ("ISABELLA'S RELIGIOUS EXPERIENCE.", "isabellas-religious-experience",
     "Isabella's Religious Experience",
     ["religion", "conversion", "God", "spiritual-awakening", "Jesus"]),
    ("NEW TRIALS.", "new-trials",
     "New Trials",
     ["New York City", "service", "trials", "domestic-work"]),
    ("FINDING A BROTHER AND SISTER.", "finding-a-brother-and-sister",
     "Finding a Brother and Sister",
     ["siblings", "reunion", "family", "Michael", "Sophia"]),
    ("GLEANINGS.", "gleanings",
     "Gleanings",
     ["reflections", "observations", "slavery", "memory"]),
    ("THE MATTHIAS DELUSION.", "the-matthias-delusion",
     "The Matthias Delusion",
     ["Matthias", "cult", "delusion", "prophet", "religion"]),
    ("FASTING.", "fasting",
     "Fasting",
     ["fasting", "spirituality", "discipline", "faith"]),
    ("THE CAUSE OF HER LEAVING THE CITY.", "cause-of-leaving-the-city",
     "The Cause of Her Leaving the City",
     ["Sojourner Truth", "name-change", "mission", "calling", "journey"]),
    ("THE CONSEQUENCES OF REFUSING A TRAVELLER A NIGHT'S LODGING.",
     "consequences-of-refusing-a-traveller",
     "The Consequences of Refusing a Traveller a Night's Lodging",
     ["hospitality", "preaching", "travel", "moral-lessons"]),
    ("SOME OF HER VIEWS AND REASONINGS.", "some-of-her-views-and-reasonings",
     "Some of Her Views and Reasonings",
     ["philosophy", "views", "reasoning", "slavery", "morality"]),
    ("THE SECOND ADVENT DOCTRINES.", "the-second-advent-doctrines",
     "The Second Advent Doctrines",
     ["Second Advent", "Millerism", "prophecy", "end-times"]),
    ("ANOTHER CAMP MEETING.", "another-camp-meeting",
     "Another Camp-Meeting",
     ["camp-meeting", "preaching", "mob", "courage", "faith"]),
    ("HER LAST INTERVIEW WITH HER MASTER.", "her-last-interview-with-her-master",
     "Last Interview with Her Master",
     ["Dumont", "reconciliation", "forgiveness", "final-meeting"]),
]


# Thematic L2 groupings
THEMATIC_GROUPS = [
    {
        "id": "theme-childhood-in-slavery",
        "name": "Childhood in Slavery",
        "chapter_indices": [0, 1, 2, 3, 4],  # chapters 1-5
        "about": "The earliest years of Isabella's life as an enslaved child in Ulster County, New York. Born the property of a Dutch-speaking master, she grew up in a damp cellar with her family, learned to pray in Low Dutch, watched her siblings sold away one by one, and was herself auctioned off as a small child alongside a flock of sheep. These chapters establish the world Isabella was born into — a world where human beings were inventory and families existed only at the master's pleasure.",
        "for_readers": "These opening chapters ground the narrative in the physical reality of Northern slavery — often overlooked in favor of Southern plantation stories. Notice the sensory details: the cellar dwelling, the Dutch language of prayer, the auction block. Isabella's early life dismantles the myth that Northern slavery was somehow gentler. The separation of her family is told with quiet devastation.",
        "keywords": ["childhood", "slavery", "family", "Dutch", "auction", "New York"],
    },
    {
        "id": "theme-loss-and-death",
        "name": "Loss and Death",
        "chapter_indices": [5, 6, 7],  # chapters 6-8
        "about": "The deaths of Isabella's parents — Mau-Mau Bett and Bomefree — who were left to die in poverty and neglect after a lifetime of enslaved labor. Freed in old age when they could no longer work, they were given no resources, no care, no pension for decades of stolen labor. Mau-Mau Bett collapsed from palsy; Bomefree froze to death in a makeshift shelter. These chapters are an indictment of a system that used human beings to exhaustion and discarded them.",
        "for_readers": "The deaths of Isabella's parents are among the most quietly devastating passages in American autobiography. There is no melodrama — only the plain facts of abandonment. Bomefree, blind and lame, dying alone in the cold. The system that enslaved them did not even grant them a dignified death. Isabella's grief becomes the fuel for everything that follows.",
        "keywords": ["death", "parents", "grief", "abandonment", "Mau-Mau Bett", "Bomefree"],
    },
    {
        "id": "theme-trials-and-suffering",
        "name": "Trials and Suffering",
        "chapter_indices": [8, 9, 10, 11, 12],  # chapters 9-13
        "about": "Isabella's years of hard labor, brutal treatment, forced marriage, and motherhood under slavery. She endured beatings, overwork, and the constant threat of family separation. Her marriage to Thomas was arranged by her master; her children were born into bondage. Through it all, she maintained her faith and her fierce will to survive. These chapters chronicle the middle years of enslavement — the grinding daily reality that lies between the dramatic moments of auction and escape.",
        "for_readers": "These chapters reveal the ordinary cruelty of slavery — not the spectacular violence of the auction block, but the daily degradation of being owned. Isabella's marriage is not a love story but a transaction between masters. Her motherhood is shadowed by the knowledge that her children are property. Pay attention to the small acts of resistance and dignity she preserves even under these conditions.",
        "keywords": ["trials", "suffering", "marriage", "motherhood", "labor", "endurance"],
    },
    {
        "id": "theme-escape-and-justice",
        "name": "Escape and Justice",
        "chapter_indices": [13, 14, 15, 16],  # chapters 14-17
        "about": "The turning point: Isabella escapes from the Dumont household and wages a legal battle to recover her son Peter, who was illegally sold into slavery in Alabama. Taking her case to court — an almost unheard-of act for a Black woman in the 1820s — she wins, becoming one of the first Black women in America to successfully sue a white man. These chapters mark the transformation from endurance to action, from survival to justice-seeking.",
        "for_readers": "Isabella's escape and her legal battle for her son are remarkable for their courage and their historical significance. She walks away from slavery not in the dead of night but in the light of day, carrying her infant. Her decision to go to court — to insist that the law protect her child — prefigures the entire civil rights movement. The chapter 'It Is Often Darkest Just Before Dawn' shows her at her most determined and her most vulnerable.",
        "keywords": ["escape", "freedom", "legal-battle", "justice", "son", "courage"],
    },
    {
        "id": "theme-spiritual-awakening",
        "name": "Spiritual Awakening",
        "chapter_indices": [17, 18, 19, 20, 21],  # chapters 18-22
        "about": "Isabella's profound religious transformation — a direct mystical encounter with God that reshapes her entire being, followed by her discovery of Jesus as intercessor and friend. Moving to New York City, she navigates new trials in domestic service while deepening her spiritual life. She finds long-lost siblings and gathers fragments of her scattered family. These chapters trace the inner revolution that will eventually produce the public prophet Sojourner Truth.",
        "for_readers": "Isabella's religious experience is not conventional churchgoing — it is raw, ecstatic, and deeply personal. Her encounter with God terrifies her before it comforts her; her discovery of Jesus comes not through doctrine but through direct spiritual crisis. These chapters show the forging of the prophetic voice that will later challenge the nation. The reunion with her siblings is a tender counterpoint to the spiritual intensity.",
        "keywords": ["religion", "spirituality", "conversion", "New York", "siblings", "awakening"],
    },
    {
        "id": "theme-the-prophets-world",
        "name": "The Prophet's World",
        "chapter_indices": [22, 23, 24, 25],  # chapters 23-26
        "about": "Isabella's entanglement with the cult of Robert Matthias — a false prophet who exploited her faith and labor — followed by her dramatic departure from New York City. The Matthias episode teaches her to distinguish true spiritual calling from manipulation. When she finally leaves the city, she takes a new name: Sojourner Truth. The old Isabella dies; the prophet is born. She sets out on foot, trusting God to direct her path.",
        "for_readers": "The Matthias chapters are often overlooked but are crucial to understanding Sojourner Truth's development. She had to learn, painfully, the difference between genuine spiritual authority and charismatic fraud. Her departure from the city and assumption of a new name is one of the great self-creation moments in American history — a formerly enslaved woman naming herself Truth and walking into the unknown.",
        "keywords": ["Matthias", "cult", "departure", "Sojourner Truth", "name-change", "calling"],
    },
    {
        "id": "theme-truths-voice",
        "name": "Truth's Voice",
        "chapter_indices": [26, 27, 28, 29],  # chapters 27-30
        "about": "Sojourner Truth in her own words — her views on slavery, morality, religion, and the human condition. She confronts Second Advent preachers, faces down hostile mobs at camp meetings with nothing but her voice and her faith, and returns to meet her former master Dumont, now humbled and repentant. These final chapters reveal the fully formed prophet: fearless, wise, sharp-witted, and grounded in a faith that has survived every test.",
        "for_readers": "These chapters give us Sojourner Truth as the nation would come to know her — the woman whose voice could silence a mob, whose reasoning cut through hypocrisy, whose humor disarmed hostility. The camp-meeting scene where she stands alone against a threatening crowd is one of the great moments of moral courage in American literature. Her final interview with the now-penitent Dumont closes the narrative with unexpected grace.",
        "keywords": ["preaching", "views", "camp-meeting", "courage", "reconciliation", "voice"],
    },
]


def find_body_start(lines):
    """Find where the body text begins (after the TOC and second 'NARRATIVE OF SOJOURNER TRUTH')."""
    # The body starts at the second occurrence of "NARRATIVE OF SOJOURNER TRUTH" (line ~98)
    count = 0
    for i, line in enumerate(lines):
        if line.strip() == "NARRATIVE OF SOJOURNER TRUTH":
            count += 1
            if count == 2:
                return i + 1
    # Fallback: start after line 95
    return 95


def find_chapter_boundaries(lines, body_start):
    """Find the start line of each chapter heading in the body text."""
    boundaries = []

    for ch_heading, slug, display_name, keywords in CHAPTERS:
        found = False
        for i in range(body_start, len(lines)):
            stripped = lines[i].strip()
            if stripped == ch_heading:
                boundaries.append((i, slug, display_name, keywords))
                found = True
                break
        if not found:
            print(f"WARNING: Could not find chapter heading: {ch_heading}")

    # Find CERTIFICATES OF CHARACTER
    for i in range(body_start, len(lines)):
        stripped = lines[i].strip()
        if stripped == "CERTIFICATES OF CHARACTER.":
            boundaries.append((i, "certificates-of-character",
                             "Certificates of Character",
                             ["certificates", "character", "testimony", "Garrison"]))
            break

    boundaries.sort(key=lambda x: x[0])
    return boundaries


def extract_chapter_text(boundaries, lines):
    """Extract text content for each chapter between boundaries."""
    chapters = []
    for idx, (start_line, slug, display_name, keywords) in enumerate(boundaries):
        # Skip the heading line and blank lines after it
        content_start = start_line + 1
        while content_start < len(lines) and not lines[content_start].strip():
            content_start += 1

        # End at next boundary or end of text
        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][0]
        else:
            end_line = len(lines)

        # Collect text, normalizing whitespace
        raw_text = '\n'.join(lines[content_start:end_line]).strip()

        # Clean up: normalize multiple blank lines, strip trailing whitespace
        raw_text = re.sub(r'\n{3,}', '\n\n', raw_text)
        raw_text = raw_text.strip()

        chapters.append({
            "slug": slug,
            "display_name": display_name,
            "keywords": keywords,
            "text": raw_text,
        })
    return chapters


def build_grammar():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    lines = text.split('\n')

    body_start = find_body_start(lines)
    print(f"Body starts at line {body_start}")

    boundaries = find_chapter_boundaries(lines, body_start)
    print(f"Found {len(boundaries)} chapter boundaries")

    chapters = extract_chapter_text(boundaries, lines)

    items = []
    sort_order = 0
    chapter_ids = []  # list of L1 chapter IDs in order (excluding certificates)

    # --- L1: Individual chapters ---
    for ch in chapters:
        sort_order += 1
        item_id = ch["slug"]

        category = "chapter"
        if item_id == "certificates-of-character":
            category = "appendix"

        item = {
            "id": item_id,
            "name": ch["display_name"],
            "level": 1,
            "category": category,
            "sort_order": sort_order,
            "sections": {
                "Narrative": ch["text"],
            },
            "keywords": ch["keywords"],
            "metadata": {},
        }

        items.append(item)
        if category == "chapter":
            chapter_ids.append(item_id)

    # --- L2: Thematic groupings ---
    thematic_l2_ids = []
    for tg in THEMATIC_GROUPS:
        sort_order += 1
        # Collect the L1 chapter IDs for this thematic group
        composite_ids = []
        for ci in tg["chapter_indices"]:
            if ci < len(chapter_ids):
                composite_ids.append(chapter_ids[ci])

        item = {
            "id": tg["id"],
            "name": tg["name"],
            "level": 2,
            "category": "thematic-group",
            "sort_order": sort_order,
            "sections": {
                "About": tg["about"],
                "For Readers": tg["for_readers"],
            },
            "keywords": tg["keywords"],
            "composite_of": composite_ids,
            "relationship_type": "emergence",
            "metadata": {},
        }
        items.append(item)
        thematic_l2_ids.append(tg["id"])

    # --- L3: Meta-category ---
    sort_order += 1
    items.append({
        "id": "meta-isabella-to-sojourner-truth",
        "name": "The Journey from Isabella to Sojourner Truth",
        "level": 3,
        "category": "meta-category",
        "sort_order": sort_order,
        "sections": {
            "About": "The complete arc of one of the most extraordinary lives in American history — from an enslaved child named Isabella, born in a damp cellar in Ulster County, New York, to the prophet Sojourner Truth, whose voice would challenge the conscience of a nation. This narrative traces the journey through childhood bondage, the deaths of her parents in poverty, years of brutal labor and forced marriage, a daring escape, a precedent-setting legal battle for her son, a shattering spiritual awakening, entanglement with a false prophet, and finally the moment of self-creation when she took a new name and walked out of the city to speak truth to power. It is a story of resilience, faith, and the refusal to be silenced.",
            "For Readers": "Read this narrative as the story of a woman who literally renamed herself Truth. The arc moves from powerlessness to prophecy, from being owned to owning her own voice. Each thematic grouping represents a stage in this transformation: the wound of childhood slavery, the grief of losing family, the endurance of daily suffering, the courage of escape and legal action, the fire of spiritual awakening, the hard lessons of false religion, and finally the emergence of one of America's most powerful moral voices. Sojourner Truth's story is not just historical testimony — it is a living grammar of liberation.",
        },
        "keywords": ["autobiography", "liberation", "transformation", "prophecy", "resilience"],
        "composite_of": thematic_l2_ids,
        "relationship_type": "emergence",
        "metadata": {},
    })

    # --- Build the grammar ---
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Sojourner Truth",
                    "date": "1850",
                    "note": "Narrator"
                },
                {
                    "name": "Olive Gilbert",
                    "date": "1850",
                    "note": "Editor/Author"
                },
                {
                    "name": "Project Gutenberg",
                    "date": "1999",
                    "note": "Digital source, eBook #1674"
                }
            ]
        },
        "name": "Narrative of Sojourner Truth",
        "description": (
            "The Narrative of Sojourner Truth (1850), dictated by Sojourner Truth and "
            "edited by Olive Gilbert — the autobiography of one of America's most powerful "
            "voices for abolition and women's rights. Born into slavery as Isabella in Ulster "
            "County, New York, around 1797, she endured decades of bondage, escaped to freedom, "
            "won a landmark legal case to recover her illegally sold son, experienced a profound "
            "spiritual transformation, and renamed herself Sojourner Truth as she set out to "
            "preach against slavery and injustice. This narrative captures her life from birth "
            "through her emergence as a prophetic public figure.\n\n"
            "Source: Project Gutenberg eBook #1674 (https://www.gutenberg.org/ebooks/1674)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs and cartes de visite of "
            "Sojourner Truth, particularly the iconic seated portraits (c. 1864) she sold with "
            "the caption 'I Sell the Shadow to Support the Substance.' Frontispiece portrait "
            "from the 1850 first edition published in Boston. Illustrations from abolitionist "
            "publications and anti-slavery almanacs. Engravings from the 1875 expanded edition "
            "'Narrative of Sojourner Truth; a Bondswoman of Olden Time' with added 'Book of Life.'"
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "autobiography",
            "slavery",
            "abolition",
            "women",
            "african-american",
            "public-domain",
            "full-text",
            "spiritual",
            "justice"
        ],
        "roots": [
            "justice-liberation",
            "african-diaspora"
        ],
        "shelves": [
            "resilience"
        ],
        "lineages": [
            "Akomolafe",
            "Andreotti"
        ],
        "worldview": "prophetic",
        "items": items,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Print summary
    l1_count = sum(1 for item in items if item["level"] == 1)
    l2_count = sum(1 for item in items if item["level"] == 2)
    l3_count = sum(1 for item in items if item["level"] == 3)
    print(f"Generated {len(items)} items: {l1_count} L1 + {l2_count} L2 + {l3_count} L3")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    build_grammar()
