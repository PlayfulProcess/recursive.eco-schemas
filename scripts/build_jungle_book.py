#!/usr/bin/env python3
"""
Build The Jungle Book grammar from Project Gutenberg seed text.

Parses seeds/jungle-book.txt into grammars/jungle-book/grammar.json.

Structure:
- L1: 7 stories + 7 songs/poems (+ epigraph Night-Song)
- L2: Story cycles (Mowgli stories, standalone stories) + thematic groups
- L3: Meta-categories
"""

import json
import re
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
SEED = ROOT / "seeds" / "jungle-book.txt"
OUTPUT_DIR = ROOT / "grammars" / "jungle-book"
OUTPUT = OUTPUT_DIR / "grammar.json"


def read_seed():
    with open(SEED, "r", encoding="utf-8") as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Project Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE JUNGLE BOOK ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE JUNGLE BOOK ***"
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1:
        raise ValueError("Could not find Gutenberg markers")
    return text[start + len(start_marker):end].strip()


def strip_illustrations(text):
    """Remove [Illustration: ...] tags, handling multi-line ones."""
    # Multi-line illustrations
    text = re.sub(r'\[Illustration[^\]]*\]', '', text, flags=re.DOTALL)
    return text


def strip_front_matter(text):
    """Remove title page, contents, list of illustrations."""
    # Find the first actual story content - the Night-Song epigraph
    # which starts with "Now Rann, the Kite"
    match = re.search(r'\n\s*Now Rann, the Kite, brings home the night', text)
    if match:
        return text[match.start():]
    return text


def strip_transcriber_notes(text):
    """Remove transcriber's notes at end."""
    match = re.search(r'\n\s*Transcriber\'s Notes:', text)
    if match:
        return text[:match.start()]
    return text


def clean_text(text):
    """Clean up whitespace and formatting artifacts."""
    # Remove excessive blank lines (more than 2 in a row)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    # Remove leading/trailing whitespace from lines but preserve indentation for poetry
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        # Strip trailing whitespace only
        cleaned.append(line.rstrip())
    return '\n'.join(cleaned)


# Define the sections of the book with their boundaries
# Each tuple: (title_pattern, id, name, is_song, category_hint)
SECTIONS = [
    ("night-song", "night-song-in-the-jungle", "Night-Song in the Jungle", True, "epigraph"),
    ("MOWGLI'S BROTHERS", "mowglis-brothers", "Mowgli's Brothers", False, "mowgli-stories"),
    ("HUNTING-SONG OF THE SEEONEE PACK", "hunting-song-of-the-seeonee-pack", "Hunting-Song of the Seeonee Pack", True, "mowgli-songs"),
    ("KAA'S HUNTING", "kaas-hunting", "Kaa's Hunting", False, "mowgli-stories"),
    ("ROAD-SONG OF THE BANDAR-LOG", "road-song-of-the-bandar-log", "Road-Song of the Bandar-Log", True, "mowgli-songs"),
    ("\"TIGER! TIGER!\"", "tiger-tiger", "\"Tiger! Tiger!\"", False, "mowgli-stories"),
    ("MOWGLI'S SONG", "mowglis-song", "Mowgli's Song", True, "mowgli-songs"),
    ("THE WHITE SEAL", "the-white-seal", "The White Seal", False, "standalone-stories"),
    ("LUKANNON", "lukannon", "Lukannon", True, "standalone-songs"),
    ("\"RIKKI-TIKKI-TAVI\"", "rikki-tikki-tavi", "Rikki-Tikki-Tavi", False, "standalone-stories"),
    ("DARZEE'S CHAUNT", "darzees-chaunt", "Darzee's Chaunt", True, "standalone-songs"),
    ("TOOMAI OF THE ELEPHANTS", "toomai-of-the-elephants", "Toomai of the Elephants", False, "standalone-stories"),
    ("SHIV AND THE GRASSHOPPER", "shiv-and-the-grasshopper", "Shiv and the Grasshopper", True, "standalone-songs"),
    ("HER MAJESTY'S SERVANTS", "her-majestys-servants", "Her Majesty's Servants", False, "standalone-stories"),
    ("PARADE-SONG OF THE CAMP ANIMALS", "parade-song-of-the-camp-animals", "Parade-Song of the Camp Animals", True, "standalone-songs"),
]


def find_section_boundaries(text):
    """Find the start positions of each section in the text."""
    lines = text.split('\n')
    boundaries = []

    # Night-Song is the epigraph at the very beginning
    for i, line in enumerate(lines):
        if 'Now Rann, the Kite, brings home the night' in line:
            boundaries.append(("night-song", i))
            break

    # Find each titled section
    title_patterns = [
        ("MOWGLI'S BROTHERS", "MOWGLI'S BROTHERS"),
        ("HUNTING-SONG OF THE SEEONEE PACK", "HUNTING-SONG OF THE SEEONEE PACK"),
        ("KAA'S HUNTING", "KAA'S HUNTING"),
        ("ROAD-SONG OF THE BANDAR-LOG", "ROAD-SONG OF THE BANDAR-LOG"),
        ("\"TIGER! TIGER!\"", "TIGER! TIGER!"),
        ("MOWGLI'S SONG", "MOWGLI'S SONG"),
        ("THE WHITE SEAL", "THE WHITE SEAL"),
        ("LUKANNON", "LUKANNON"),
        ("\"RIKKI-TIKKI-TAVI\"", "RIKKI-TIKKI-TAVI"),
        ("DARZEE'S CHAUNT", "DARZEE'S CHAUNT"),
        ("TOOMAI OF THE ELEPHANTS", "TOOMAI OF THE ELEPHANTS"),
        ("SHIV AND THE GRASSHOPPER", "SHIV AND THE GRASSHOPPER"),
        ("HER MAJESTY'S SERVANTS", "HER MAJESTY'S SERVANTS"),
        ("PARADE-SONG OF THE CAMP ANIMALS", "PARADE-SONG OF THE CAMP ANIMALS"),
    ]

    # We need to skip table-of-contents occurrences and find the actual story starts
    # Stories appear after the front matter is stripped, so we look for centered titles
    # that appear as standalone lines (not in TOC format with page numbers)

    found_sections = set()

    for i, line in enumerate(lines):
        stripped = line.strip()
        for key, pattern in title_patterns:
            # Skip if already found (we want the LAST occurrence which is the actual text,
            # not TOC or illustration references)
            # Actually we want the first occurrence AFTER front matter
            if key in found_sections:
                continue

            # Check for centered title (lots of leading spaces, matching pattern)
            if stripped == pattern or stripped == f'"{pattern}"':
                # Make sure this isn't in the TOC (TOC lines have page numbers after)
                # Check it's a centered heading by looking at indentation
                if len(line) - len(line.lstrip()) > 10:  # significantly indented = centered
                    # Check next few lines aren't page-number style TOC entries
                    is_toc = False
                    for j in range(max(0, i-3), min(len(lines), i+3)):
                        if re.search(r'\d+\s*$', lines[j].strip()) and len(lines[j].strip()) > 20:
                            # Could be TOC
                            pass
                    # For stories, look for the actual story text following
                    # Skip if there's a duplicate (story titles appear twice sometimes)
                    # Use heuristic: if the next non-blank line is also a centered title, skip
                    next_content = ""
                    for j in range(i+1, min(len(lines), i+10)):
                        if lines[j].strip():
                            next_content = lines[j].strip()
                            break

                    # If next content is the same title repeated, this is the first occurrence
                    # (decorative), skip it
                    if next_content == stripped or next_content == f'"{pattern}"' or next_content == pattern:
                        continue

                    boundaries.append((key, i))
                    found_sections.add(key)
                    break

    return boundaries, lines


def extract_sections(text):
    """Extract all story/poem sections from the text."""
    boundaries, lines = find_section_boundaries(text)

    sections = {}
    for idx, (key, start_line) in enumerate(boundaries):
        # End is the start of the next section, or end of text
        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][1]
        else:
            end_line = len(lines)

        # Extract the text
        section_text = '\n'.join(lines[start_line:end_line])
        sections[key] = section_text.strip()

    return sections


def clean_story_text(text, is_song=False):
    """Clean a story or song text for inclusion in the grammar."""
    # Remove the title line(s) at the beginning
    lines = text.split('\n')
    # Skip title and subtitle lines (centered, all caps or mostly caps)
    content_start = 0
    blank_after_title = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if i > 0:
                blank_after_title = True
            continue
        # Title lines are centered (heavily indented) and mostly uppercase
        if len(line) - len(line.lstrip()) > 10 and (stripped.isupper() or stripped.startswith('"') and stripped.endswith('"')):
            content_start = i + 1
            blank_after_title = False
            continue
        # Subtitle lines like "THAT HE SANG AT THE COUNCIL ROCK..."
        if len(line) - len(line.lstrip()) > 10 and stripped.isupper():
            content_start = i + 1
            blank_after_title = False
            continue
        # If we hit content after blank line after title, we're done
        if blank_after_title:
            content_start = i
            break
        if i > 0:
            content_start = i
            break

    content = '\n'.join(lines[content_start:])

    # Remove illustration tags
    content = re.sub(r'\[Illustration[^\]]*\]', '', content, flags=re.DOTALL)

    # For songs, check for subtitle lines like "(THE SONG THAT TOOMAI'S MOTHER SANG...)"
    if is_song:
        content = re.sub(r'^\s*\(THE SONG[^\)]+\)\s*\n', '', content, flags=re.MULTILINE)

    # Clean up excessive whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()

    return content


def get_epigraph_text(sections):
    """Extract the Night-Song in the Jungle epigraph."""
    text = sections.get("night-song", "")
    if not text:
        return ""
    # It's a short poem
    lines = text.split('\n')
    poem_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('_Night-Song'):
            poem_lines.append(line.rstrip())
        elif stripped.startswith('_Night-Song'):
            break
    return '\n'.join(poem_lines).strip()


def build_items(sections):
    """Build all L1, L2, and L3 items."""
    items = []
    sort_order = 0

    # === L1 ITEMS ===

    # Story and song definitions with metadata
    story_meta = {
        "night-song": {
            "name": "Night-Song in the Jungle",
            "id": "night-song-in-the-jungle",
            "is_song": True,
            "category": "epigraph",
            "keywords": ["jungle", "night", "hunting", "law", "freedom"],
            "summary": "A brief verse celebrating the hour when the jungle's hunters are loosed -- the hour of pride and power, talon and tush and claw.",
        },
        "MOWGLI'S BROTHERS": {
            "name": "Mowgli's Brothers",
            "id": "mowglis-brothers",
            "is_song": False,
            "category": "mowgli-stories",
            "keywords": ["mowgli", "wolves", "shere-khan", "akela", "bagheera", "adoption", "belonging", "pack-law"],
            "summary": "A man-cub is brought to the wolf pack by Father and Mother Wolf. Bagheera the panther and Baloo the bear speak for him at the Council Rock. As Mowgli grows, the lame tiger Shere Khan plots against him, and when Akela the pack leader misses his kill, Mowgli must fight for his place -- or leave the jungle forever.",
        },
        "HUNTING-SONG OF THE SEEONEE PACK": {
            "name": "Hunting-Song of the Seeonee Pack",
            "id": "hunting-song-of-the-seeonee-pack",
            "is_song": True,
            "category": "mowgli-songs",
            "keywords": ["wolves", "hunting", "dawn", "pack", "tracking"],
            "summary": "The wolf pack's hunting song, celebrating the chase at dawn -- feet that leave no mark, eyes that see in the dark.",
        },
        "KAA'S HUNTING": {
            "name": "Kaa's Hunting",
            "id": "kaas-hunting",
            "is_song": False,
            "category": "mowgli-stories",
            "keywords": ["mowgli", "kaa", "bandar-log", "baloo", "bagheera", "monkeys", "cold-lairs", "rescue", "discipline"],
            "summary": "The Bandar-log (monkey people) kidnap Mowgli and carry him to the Cold Lairs, the ruined city. Baloo and Bagheera pursue, but it is Kaa the great python whose ancient power and hypnotic dance rescue the man-cub. Mowgli learns why the Jungle People despise the monkeys -- those without law.",
        },
        "ROAD-SONG OF THE BANDAR-LOG": {
            "name": "Road-Song of the Bandar-Log",
            "id": "road-song-of-the-bandar-log",
            "is_song": True,
            "category": "mowgli-songs",
            "keywords": ["monkeys", "boasting", "vanity", "satire", "swinging"],
            "summary": "The monkeys' self-glorifying song -- all talk and no substance, dreaming of deeds they will never do. 'Brother, thy tail hangs down behind!'",
        },
        "\"TIGER! TIGER!\"": {
            "name": "\"Tiger! Tiger!\"",
            "id": "tiger-tiger",
            "is_song": False,
            "category": "mowgli-stories",
            "keywords": ["mowgli", "shere-khan", "village", "buffaloes", "gray-brother", "identity", "exile", "revenge"],
            "summary": "Mowgli goes to live among men in a village, where he is set to herding buffaloes. With Gray Brother's help, he traps and kills Shere Khan with a stampede. But the villagers, fearing his power over animals, cast him out as a sorcerer. Mowgli dances on the tiger's hide and returns to the jungle -- belonging to neither world.",
        },
        "MOWGLI'S SONG": {
            "name": "Mowgli's Song",
            "id": "mowglis-song",
            "is_song": True,
            "category": "mowgli-songs",
            "keywords": ["mowgli", "shere-khan", "triumph", "exile", "identity", "sorrow"],
            "summary": "Mowgli's victory song after killing Shere Khan -- exultant yet sorrowful. He is two Mowglis: the triumphant hunter and the exile who belongs nowhere. 'My heart is heavy with the things that I do not understand.'",
        },
        "THE WHITE SEAL": {
            "name": "The White Seal",
            "id": "the-white-seal",
            "is_song": False,
            "category": "standalone-stories",
            "keywords": ["kotick", "seals", "sea", "quest", "slaughter", "sanctuary", "perseverance", "leadership"],
            "summary": "Kotick, a rare white seal born on the beaches of Novastoshnah, witnesses the annual seal slaughter and vows to find a safe beach for his people. After years of searching the oceans, he discovers a hidden paradise and returns to lead the seals to safety -- though he must fight every seal on the beach to prove his right to lead.",
        },
        "LUKANNON": {
            "name": "Lukannon",
            "id": "lukannon",
            "is_song": True,
            "category": "standalone-songs",
            "keywords": ["seals", "lament", "loss", "beaches", "memory", "slaughter"],
            "summary": "A mournful seal lament for Lukannon beach, the old gathering place. The seals remember the days before the hunters came, when the beaches were thick with their kind.",
        },
        "\"RIKKI-TIKKI-TAVI\"": {
            "name": "Rikki-Tikki-Tavi",
            "id": "rikki-tikki-tavi",
            "is_song": False,
            "category": "standalone-stories",
            "keywords": ["mongoose", "cobra", "nag", "nagaina", "courage", "protection", "garden", "battle"],
            "summary": "A young mongoose is washed out of his burrow by a flood and adopted by a human family. In their garden he discovers Nag and Nagaina, two deadly cobras who plot to kill the family. Through courage, cunning, and relentless fighting, Rikki-tikki destroys the cobras and makes the garden safe -- the great war that he fought single-handed.",
        },
        "DARZEE'S CHAUNT": {
            "name": "Darzee's Chaunt",
            "id": "darzees-chaunt",
            "is_song": True,
            "category": "standalone-songs",
            "keywords": ["tailorbird", "praise", "rikki-tikki", "victory", "garden", "celebration"],
            "summary": "Darzee the tailorbird's song of praise for Rikki-tikki-tavi, the red-eyed avenger who slew the cobras. A garden celebration of deliverance.",
        },
        "TOOMAI OF THE ELEPHANTS": {
            "name": "Toomai of the Elephants",
            "id": "toomai-of-the-elephants",
            "is_song": False,
            "category": "standalone-stories",
            "keywords": ["elephants", "toomai", "kala-nag", "dance", "wonder", "mystery", "initiation", "india"],
            "summary": "Little Toomai, son and grandson of elephant handlers, rides Kala Nag into the jungle at night and witnesses the secret elephant dance that no man has seen before. His vision earns him the title 'Toomai of the Elephants' -- the boy who has seen what no tracker or hunter will ever see.",
        },
        "SHIV AND THE GRASSHOPPER": {
            "name": "Shiv and the Grasshopper",
            "id": "shiv-and-the-grasshopper",
            "is_song": True,
            "category": "standalone-songs",
            "keywords": ["shiva", "lullaby", "creation", "providence", "mother", "india", "devotion"],
            "summary": "A lullaby sung by Toomai's mother. Shiva the Preserver gives every creature its portion -- even the least grasshopper hidden in Parbati's breast is fed. A mother's song of divine care for all living things.",
        },
        "HER MAJESTY'S SERVANTS": {
            "name": "Her Majesty's Servants",
            "id": "her-majestys-servants",
            "is_song": False,
            "category": "standalone-stories",
            "keywords": ["army", "animals", "service", "obedience", "fear", "duty", "empire", "hierarchy"],
            "summary": "On a rainy night at a military camp in India, the narrator overhears the camp animals -- mules, horses, bullocks, camels, and an elephant -- arguing about fear, duty, and obedience. Each serves differently, each fears different things, but all serve the chain of command. An Afghan chief marvels: in his country, they obey only their own wills.",
        },
        "PARADE-SONG OF THE CAMP ANIMALS": {
            "name": "Parade-Song of the Camp Animals",
            "id": "parade-song-of-the-camp-animals",
            "is_song": True,
            "category": "standalone-songs",
            "keywords": ["military", "service", "animals", "march", "duty", "empire"],
            "summary": "Each camp animal sings its own verse -- elephants, gun-bullocks, cavalry horses, screw-gun mules, commissariat camels -- each proud of its role. Together they are 'children of the yoke and goad,' marching to war.",
        },
    }

    for key, meta in story_meta.items():
        raw = sections.get(key, "")
        if not raw:
            continue

        text = clean_story_text(raw, is_song=meta["is_song"])

        if meta["is_song"]:
            section_dict = {
                "Poem": text,
                "About": meta["summary"],
                "Reflection": get_song_reflection(meta["id"]),
            }
        else:
            section_dict = {
                "Story": text,
                "About": meta["summary"],
                "Reflection": get_story_reflection(meta["id"]),
            }

        item = {
            "id": meta["id"],
            "name": meta["name"],
            "sort_order": sort_order,
            "level": 1,
            "category": meta["category"],
            "sections": section_dict,
            "keywords": meta["keywords"],
            "metadata": {
                "source": "The Jungle Book, Rudyard Kipling, 1894"
            }
        }
        items.append(item)
        sort_order += 1

    # === L2 ITEMS ===

    # Mowgli Story Cycle
    items.append({
        "id": "cycle-mowgli-stories",
        "name": "The Mowgli Stories",
        "sort_order": sort_order,
        "level": 2,
        "category": "story-cycles",
        "composite_of": ["mowglis-brothers", "kaas-hunting", "tiger-tiger"],
        "relationship_type": "emergence",
        "sections": {
            "About": "The three Mowgli stories form a continuous narrative arc: a human child adopted by wolves, educated by the jungle's wisest teachers, and ultimately exiled from both worlds. Mowgli's Brothers introduces the man-cub to the wolf pack and establishes the conflict with Shere Khan. Kaa's Hunting tests Mowgli's allegiances when the lawless monkeys kidnap him. 'Tiger! Tiger!' brings the arc to its climax as Mowgli kills Shere Khan but is cast out by both village and jungle. Together they tell the oldest story: the one who belongs to two worlds and must forge an identity between them.",
            "For Parents": "These three stories work beautifully read in sequence over several evenings. They explore belonging, identity, growing up between cultures, and the painful discovery that being different can mean being feared. Great for children navigating new schools, blended families, or any situation where they feel caught between two worlds."
        },
        "keywords": ["mowgli", "wolves", "identity", "belonging", "jungle-law", "coming-of-age"],
        "metadata": {"story_count": 3}
    })
    sort_order += 1

    # Mowgli Songs
    items.append({
        "id": "cycle-mowgli-songs",
        "name": "Songs of the Mowgli Stories",
        "sort_order": sort_order,
        "level": 2,
        "category": "story-cycles",
        "composite_of": ["night-song-in-the-jungle", "hunting-song-of-the-seeonee-pack", "road-song-of-the-bandar-log", "mowglis-song"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Each Mowgli story ends with a song or poem that distills its emotional core. The Night-Song opens the book with the jungle's predatory beauty. The Hunting-Song celebrates the wolf pack's unity. The Road-Song of the Bandar-Log satirizes the monkeys' empty boasting. Mowgli's Song is the most powerful -- a victory cry laced with sorrow, the voice of someone who has won everything and lost everything at once.",
            "For Parents": "These poems are wonderful for reading aloud. Children love the rhythmic, chant-like quality. Mowgli's Song in particular opens deep conversations about mixed feelings -- can you be happy and sad at the same time? Can winning feel like losing?"
        },
        "keywords": ["poetry", "songs", "mowgli", "emotion", "jungle"],
        "metadata": {"song_count": 4}
    })
    sort_order += 1

    # Standalone Stories
    items.append({
        "id": "cycle-standalone-stories",
        "name": "The Standalone Stories",
        "sort_order": sort_order,
        "level": 2,
        "category": "story-cycles",
        "composite_of": ["the-white-seal", "rikki-tikki-tavi", "toomai-of-the-elephants", "her-majestys-servants"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Four stories set outside the Mowgli universe, each in a distinct world: the seal beaches of the Bering Sea, a garden in colonial India, the elephant camps of the Indian jungle, and a British military encampment. Each features an animal (or animals) whose courage, perseverance, or service drives the narrative. While independent, they share Kipling's central fascination: the relationship between wild nature, trained discipline, and the mysterious borderland between them.",
            "For Parents": "Each standalone story is perfect as a self-contained bedtime read. Rikki-Tikki-Tavi is perhaps the most beloved -- a thrilling tale of courage that children adore. The White Seal teaches perseverance. Toomai inspires wonder. Her Majesty's Servants is more complex, exploring duty and obedience, and suits older children ready for nuance."
        },
        "keywords": ["adventure", "courage", "animals", "india", "sea"],
        "metadata": {"story_count": 4}
    })
    sort_order += 1

    # Standalone Songs
    items.append({
        "id": "cycle-standalone-songs",
        "name": "Songs of the Standalone Stories",
        "sort_order": sort_order,
        "level": 2,
        "category": "story-cycles",
        "composite_of": ["lukannon", "darzees-chaunt", "shiv-and-the-grasshopper", "parade-song-of-the-camp-animals"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Each standalone story has its companion poem. Lukannon mourns the lost seal beaches. Darzee's Chaunt celebrates Rikki-tikki's victory in the garden. Shiv and the Grasshopper is a Hindu lullaby about divine providence. The Parade-Song gives voice to each camp animal in turn. Together they show Kipling's belief that every world has its own music.",
            "For Parents": "Shiv and the Grasshopper makes a beautiful bedtime lullaby. Darzee's Chaunt is fun to read aloud after the excitement of Rikki-Tikki-Tavi. The Parade-Song, with its different animal voices, is great for dramatic reading with children taking different parts."
        },
        "keywords": ["poetry", "songs", "celebration", "lament", "devotion"],
        "metadata": {"song_count": 4}
    })
    sort_order += 1

    # Thematic: Courage and Battle
    items.append({
        "id": "theme-courage-and-battle",
        "name": "Courage and Battle",
        "sort_order": sort_order,
        "level": 2,
        "category": "themes",
        "composite_of": ["tiger-tiger", "rikki-tikki-tavi", "the-white-seal", "mowglis-song", "darzees-chaunt"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Kipling's heroes fight -- not from bloodlust but from necessity. Mowgli faces Shere Khan to survive. Rikki-tikki battles the cobras to protect his family. Kotick fights the entire seal beach to save his people. These stories celebrate physical and moral courage: the willingness to face what must be faced, alone if necessary, and to see it through to the end.",
            "For Parents": "These stories are powerful for children struggling with bullies, fears, or situations that require standing up for themselves or others. They teach that courage isn't the absence of fear -- it's acting despite fear. Discuss: what was the character most afraid of? What made them fight anyway?"
        },
        "keywords": ["courage", "battle", "bravery", "standing-up", "protection"],
        "metadata": {"story_count": 5}
    })
    sort_order += 1

    # Thematic: Belonging and Identity
    items.append({
        "id": "theme-belonging-and-identity",
        "name": "Belonging and Identity",
        "sort_order": sort_order,
        "level": 2,
        "category": "themes",
        "composite_of": ["mowglis-brothers", "tiger-tiger", "mowglis-song", "the-white-seal"],
        "relationship_type": "emergence",
        "sections": {
            "About": "The deepest current in The Jungle Book: who do you belong to? Mowgli is claimed by wolves but rejected by the pack, accepted by villagers but cast out as a sorcerer. Kotick is white among brown seals, a visionary among the contented. These are stories about being different, about the loneliness of seeing what others cannot see, and about the courage to forge your own path when no ready-made world will have you.",
            "For Parents": "Essential reading for any child who feels different or caught between groups. Mowgli's story resonates particularly with children in multicultural families, adopted children, or anyone navigating multiple identities. The key question: can you belong to yourself even when no group fully claims you?"
        },
        "keywords": ["identity", "belonging", "exile", "outsider", "two-worlds"],
        "metadata": {"story_count": 4}
    })
    sort_order += 1

    # Thematic: Law and Order
    items.append({
        "id": "theme-law-and-order",
        "name": "Law, Discipline, and the Pack",
        "sort_order": sort_order,
        "level": 2,
        "category": "themes",
        "composite_of": ["mowglis-brothers", "kaas-hunting", "her-majestys-servants", "road-song-of-the-bandar-log", "parade-song-of-the-camp-animals"],
        "relationship_type": "emergence",
        "sections": {
            "About": "The Jungle Law runs through the book like a spine. The wolf pack lives by it. The Bandar-log are despised because they have none. The camp animals serve because they obey the chain of command. Kipling believed deeply in law as the foundation of community -- not law as oppression, but law as the agreement that makes trust possible. 'The strength of the pack is the wolf, and the strength of the wolf is the pack.'",
            "For Parents": "These stories open conversations about rules, fairness, and why communities need agreements. Children naturally push against rules; these stories show what happens in communities without them (the Bandar-log) and what's possible when everyone plays their part (the wolf pack, the army camp). Good for discussing family rules, school rules, and social contracts."
        },
        "keywords": ["law", "discipline", "obedience", "community", "order", "pack"],
        "metadata": {"story_count": 5}
    })
    sort_order += 1

    # Thematic: Wonder and Mystery
    items.append({
        "id": "theme-wonder-and-mystery",
        "name": "Wonder and the Wild",
        "sort_order": sort_order,
        "level": 2,
        "category": "themes",
        "composite_of": ["toomai-of-the-elephants", "shiv-and-the-grasshopper", "night-song-in-the-jungle", "kaas-hunting"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Some moments in The Jungle Book reach beyond adventure into pure wonder. Little Toomai witnessing the secret elephant dance. The Night-Song's celebration of the predatory hour. Kaa's ancient, hypnotic power over the Bandar-log. Shiv's care for even the smallest grasshopper. These passages remind us that the natural world holds mysteries no human mind can fully contain -- and that witnessing them is a kind of initiation.",
            "For Parents": "These are the passages to read slowly, in a hushed voice. They cultivate a sense of awe and mystery about the natural world. Great for children who love animals, nature, or who are beginning to ask the big questions about how the world works. Toomai's elephant dance is one of the most magical scenes in children's literature."
        },
        "keywords": ["wonder", "mystery", "nature", "awe", "elephants", "wild"],
        "metadata": {"story_count": 4}
    })
    sort_order += 1

    # === L3 ITEMS ===

    items.append({
        "id": "meta-story-cycles",
        "name": "The Story Cycles",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "composite_of": ["cycle-mowgli-stories", "cycle-mowgli-songs", "cycle-standalone-stories", "cycle-standalone-songs"],
        "relationship_type": "emergence",
        "sections": {
            "About": "The Jungle Book is built as a series of paired stories and songs. Each prose tale is followed by a poem that reflects on it from a different angle -- sometimes celebratory, sometimes mournful, sometimes satirical. The Mowgli stories form a connected arc; the standalone stories are independent worlds. Together they create Kipling's vision of the animal kingdom as a mirror for human society: its laws, its courage, its cruelty, and its wonder.",
            "How to Use": "Start with the Mowgli stories for the central narrative arc, or dip into standalone stories for self-contained adventures. Read stories and their companion songs together for the full Kipling experience. The songs are wonderful for reading aloud."
        },
        "keywords": ["structure", "stories", "songs", "cycles", "narrative"],
        "metadata": {"group_count": 4}
    })
    sort_order += 1

    items.append({
        "id": "meta-themes",
        "name": "Themes of The Jungle Book",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "composite_of": ["theme-courage-and-battle", "theme-belonging-and-identity", "theme-law-and-order", "theme-wonder-and-mystery"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Beneath the adventure stories, The Jungle Book explores enduring human themes. Courage and battle: what it takes to face danger alone. Belonging and identity: the pain and freedom of living between worlds. Law and discipline: why communities need rules and what happens without them. Wonder and the wild: the mysteries of nature that humble and initiate us. These themes interweave throughout both the Mowgli cycle and the standalone tales, giving the book its depth and its lasting power.",
            "How to Use": "Browse by theme when you want stories that speak to a particular situation in a child's life. A child dealing with bullies might need the courage stories. A child who feels like an outsider might find kinship in the belonging stories. A child pushing against rules might benefit from the law stories. A child hungry for magic and mystery will love the wonder stories."
        },
        "keywords": ["themes", "meaning", "teaching", "values", "growth"],
        "metadata": {"group_count": 4}
    })
    sort_order += 1

    return items


def get_story_reflection(story_id):
    """Return a reflection question for each story."""
    reflections = {
        "mowglis-brothers": "Mowgli is accepted by wolves and rejected by the tiger. Who in your life has spoken for you when others doubted you? What does it mean to be 'bought' into a community -- what price does belonging cost?",
        "kaas-hunting": "The Bandar-log talk endlessly about what they will do but never follow through. Baloo teaches the Law of the Jungle, which is discipline and memory. Where in your life do you see the difference between intention and action? What 'laws' hold your own community together?",
        "tiger-tiger": "Mowgli triumphs over Shere Khan but is cast out by the very people he protected. Have you ever been punished for doing the right thing? What does it feel like to belong to two worlds and be fully accepted by neither?",
        "the-white-seal": "Kotick searched for years while others told him to give up. What dream or conviction have you held onto when everyone around you said it was impossible? What did it cost you to keep looking?",
        "rikki-tikki-tavi": "Rikki-tikki fought alone against a danger no one else could see clearly. When have you had to be brave not for yourself but to protect someone you love? What gives a small creature the courage to face a much larger foe?",
        "toomai-of-the-elephants": "Little Toomai saw what no adult had ever witnessed. What mysteries has a child shown you that you had stopped seeing? What happens when we are still enough and brave enough to follow wonder into the dark?",
        "her-majestys-servants": "Each animal serves according to its nature and fears according to its nature. What is your nature of service? What are you afraid of, and does your fear shape how you serve?",
    }
    return reflections.get(story_id, "What does this story teach about the relationship between humans and the wild?")


def get_song_reflection(song_id):
    """Return a reflection for each song/poem."""
    reflections = {
        "night-song-in-the-jungle": "What is your 'hour of pride and power'? When do you feel most alive and free?",
        "hunting-song-of-the-seeonee-pack": "What does it feel like to be part of a group working together toward a shared goal? When have you experienced the joy of the pack?",
        "road-song-of-the-bandar-log": "The monkeys boast about things they will never do. When have you caught yourself dreaming instead of doing? What's the difference between healthy imagination and empty talk?",
        "mowglis-song": "'I am two Mowglis.' Have you ever felt torn between two identities, two worlds, two feelings at once? Can joy and grief live in the same heart?",
        "lukannon": "What place from your past do you mourn? What has been lost that can never be recovered? How do we carry lost places inside us?",
        "darzees-chaunt": "Who in your life deserves a song of praise? When has someone fought for you and earned your gratitude?",
        "shiv-and-the-grasshopper": "Even the smallest creature is fed. What does it mean to trust that there is enough? Where do you see care for the least and smallest in your own world?",
        "parade-song-of-the-camp-animals": "Each animal has its own song and its own role. What is your song? What role do you play in the larger march?",
    }
    return reflections.get(song_id, "What feeling does this poem evoke? What images stay with you?")


def build_grammar(items):
    """Assemble the complete grammar JSON."""
    return {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Rudyard Kipling",
                    "date": "1894",
                    "note": "Author of The Jungle Book"
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2011",
                    "note": "Digital text source, eBook #35997"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure and editorial content"
                }
            ]
        },
        "name": "The Jungle Book",
        "description": "Rudyard Kipling's masterwork of animal fable and adventure (1894) -- seven stories and seven companion poems set in the jungles of India, the seal beaches of the Bering Sea, and the military camps of the British Raj. At its heart are the Mowgli stories: a human child raised by wolves who must find his identity between the jungle and the village. Alongside them, Rikki-tikki-tavi battles cobras in a garden, Kotick the white seal searches the oceans for sanctuary, Little Toomai witnesses the secret elephant dance, and the camp animals debate duty and fear. Source: Project Gutenberg eBook #35997 (https://www.gutenberg.org/ebooks/35997).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: The original 1894 Century Co. edition illustrated by John Lockwood Kipling (Rudyard's father), W.H. Drake, and P. Frenzeny -- detailed pen-and-ink drawings of jungle animals, Indian landscapes, and colonial settings. Maurice and Edward Detmold's 1908 illustrations for 'The Jungle Book' (Macmillan) -- lush, painterly watercolors of Mowgli, the wolves, and the jungle, widely considered the finest Jungle Book illustrations. Aldren Watson's 1948 illustrations (Grosset & Dunlap) -- classic mid-century pen-and-ink. Fritz Eichenberg's 1950 woodcut illustrations -- bold, dramatic black-and-white.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "children",
            "adventure",
            "animals",
            "jungle",
            "india",
            "fables",
            "poetry",
            "coming-of-age",
            "nature",
            "identity"
        ],
        "roots": ["romanticism", "colonialism"],
        "shelves": ["children", "wonder"],
        "lineages": ["Akomolafe", "Andreotti"],
        "worldview": "animist",
        "cover_image_url": "",
        "items": items
    }


def main():
    print("Reading seed text...")
    raw = read_seed()

    print("Stripping Gutenberg header/footer...")
    text = strip_gutenberg(raw)

    print("Stripping front matter...")
    text = strip_front_matter(text)

    print("Stripping transcriber notes...")
    text = strip_transcriber_notes(text)

    print("Cleaning text...")
    text = clean_text(text)

    print("Finding section boundaries...")
    sections = extract_sections(text)
    print(f"  Found {len(sections)} sections: {list(sections.keys())}")

    print("Building items...")
    items = build_items(sections)
    print(f"  Built {len(items)} items ({sum(1 for i in items if i['level']==1)} L1, "
          f"{sum(1 for i in items if i['level']==2)} L2, "
          f"{sum(1 for i in items if i['level']==3)} L3)")

    print("Assembling grammar...")
    grammar = build_grammar(items)

    print(f"Writing to {OUTPUT}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Quick self-validation
    print("\nSelf-check:")
    ids = [item["id"] for item in items]
    id_set = set(ids)
    dupes = [x for x in ids if ids.count(x) > 1]
    if dupes:
        print(f"  WARNING: Duplicate IDs: {set(dupes)}")
    else:
        print(f"  No duplicate IDs ({len(ids)} items)")

    for item in items:
        for ref in item.get("composite_of", []):
            if ref not in id_set:
                print(f"  WARNING: {item['id']} references missing ID: {ref}")

    file_size = os.path.getsize(OUTPUT)
    print(f"  Output size: {file_size:,} bytes")
    print("Done!")


if __name__ == "__main__":
    main()
