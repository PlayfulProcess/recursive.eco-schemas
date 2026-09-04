#!/usr/bin/env python3
"""
Generate storyboard grammars from kids/mythlands grammars.

Each L1 story is split into scenes (4-8 per story) that form a narration arc.
Each scene has:
  - Narration: the verse lines to be read aloud
  - Direction: camera/visual direction notes
  - ImagePrompt: ready-to-paste prompt for AI image generation
  - timing_seconds in metadata
  - public_domain_refs for illustration matching

Scenes become L1 items. Original stories become L2 episodes.
"""

import json
import re
import sys
import textwrap


# Visual style palettes per tradition/mythology
VISUAL_STYLES = {
    # Alice Mythlands traditions
    "Haida / Tlingit / Tsimshian (Pacific Northwest)": {
        "style": "Pacific Northwest formline art, bold red and black on cedar, ovoid shapes, U-forms, split representation",
        "palette": "deep red, black, white, cedar brown",
        "reference_artists": "Bill Reid (Haida, 1920-1998), Robert Davidson (Haida, b.1946)",
        "ai_style_suffix": "in the style of Pacific Northwest Coast formline art, bold graphic shapes, red and black cedar carving aesthetic"
    },
    "Akan / Ashanti (West Africa)": {
        "style": "Akan kente cloth patterns, Adinkra symbols, warm earth tones with gold accents, geometric textile motifs",
        "palette": "gold, deep green, terracotta, indigo, kente yellow",
        "reference_artists": "Adinkra symbol tradition, Akan gold weights",
        "ai_style_suffix": "in the style of West African textile art, kente cloth patterns, Adinkra symbols, warm gold and earth tones"
    },
    "Inuit (Central Arctic)": {
        "style": "Inuit stone carving aesthetic, Cape Dorset printmaking, flowing organic lines, arctic light",
        "palette": "ice blue, deep ocean, bone white, aurora green, twilight purple",
        "reference_artists": "Kenojuak Ashevak (Inuit, 1927-2013), Pitseolak Ashoona (Inuit, 1904-1983)",
        "ai_style_suffix": "in the style of Inuit Cape Dorset printmaking, flowing organic forms, arctic light on ice and ocean"
    },
    "Japanese (Shinto)": {
        "style": "Ukiyo-e woodblock print aesthetic, flat color planes, bold outlines, dynamic composition",
        "palette": "vermillion red, indigo, gold leaf, ink black, snow white",
        "reference_artists": "Hokusai (1760-1849), Hiroshige (1797-1858), Yoshitoshi (1839-1892)",
        "ai_style_suffix": "in the style of Japanese ukiyo-e woodblock prints, flat color planes, bold outlines, Hokusai aesthetic"
    },
    "K'iche' Maya (Mesoamerica)": {
        "style": "Maya codex style, stepped pyramids, jaguar motifs, jade green, painted ceramic vessel aesthetic",
        "palette": "jade green, obsidian black, cinnabar red, turquoise, maize gold",
        "reference_artists": "Maya codex illustration tradition, Bonampak murals",
        "ai_style_suffix": "in the style of ancient Maya painted ceramics and codex illustrations, jade green and obsidian, stepped pyramid geometry"
    },
    "Pan-North American Indigenous (Navajo, Klamath, and many nations)": {
        "style": "Southwest sandpainting aesthetic, star quilt geometry, night sky over desert, sand and sage",
        "palette": "desert sand, turquoise, red earth, midnight blue, sage green",
        "reference_artists": "Navajo sandpainting tradition, ledger art",
        "ai_style_suffix": "in the style of Southwest Indigenous art, sandpainting geometry, turquoise and desert earth under vast star-filled skies"
    },
    "Sumerian (Mesopotamia, c. 1900-1600 BCE)": {
        "style": "Mesopotamian cylinder seal aesthetic, cuneiform tablet borders, lapis lazuli blue, gold leaf, zigzag patterns",
        "palette": "lapis lazuli blue, gold, terracotta, ivory, deep bronze",
        "reference_artists": "Sumerian cylinder seal engravings, Ur III period art",
        "ai_style_suffix": "in the style of ancient Sumerian cylinder seal engravings, lapis lazuli blue and gold, cuneiform borders, ziggurat silhouettes"
    },
    "Osage / Cherokee (Great Plains & Southeast)": {
        "style": "Southeastern Ceremonial Complex, shell gorget engraving, ribbon appliqué, earth pigments",
        "palette": "earth brown, sky blue, corn gold, forest green, clay red",
        "reference_artists": "Southeastern Ceremonial Complex engravings, Cherokee basket weaving patterns",
        "ai_style_suffix": "in the style of Southeastern Indigenous art, shell gorget engravings, ribbon appliqué patterns, earth pigments under wide skies"
    },
    "Cherokee": {
        "style": "Cherokee basket weave patterns, flame and animal motifs, Appalachian forest palette",
        "palette": "flame orange, forest green, river blue, bark brown, smoke gray",
        "reference_artists": "Cherokee double-weave basket tradition",
        "ai_style_suffix": "in the style of Cherokee art traditions, basket weave patterns, flame motifs, Appalachian forest colors"
    },
    # Bedtime mythology series styles
    "biblical": {
        "style": "Gustave Doré Bible engraving aesthetic, dramatic chiaroscuro, cosmic scale, William Blake visionary watercolor",
        "palette": "dramatic black and white with gold accents, deep shadow, celestial light",
        "reference_artists": "Gustave Doré (1832-1883), William Blake (1757-1827), James Tissot (1836-1902)",
        "ai_style_suffix": "in the style of Gustave Doré Bible engravings, dramatic chiaroscuro lighting, cosmic scale, detailed crosshatching"
    },
    "homer": {
        "style": "Greek black-figure and red-figure pottery aesthetic, Mediterranean light, Aegean sea colors",
        "palette": "terracotta red, black figure, Mediterranean blue, olive gold, marble white",
        "reference_artists": "John Flaxman (1755-1826, Homer illustrations), Greek vase painters",
        "ai_style_suffix": "in the style of ancient Greek red-figure pottery and John Flaxman's Homer line drawings, Mediterranean colors, heroic scale"
    },
    "norse": {
        "style": "Viking runestone carving aesthetic, Urnes style interlace, Norse manuscript illumination",
        "palette": "iron gray, blood red, ice white, pine green, gold knotwork",
        "reference_artists": "Arthur Rackham (Norse myths), Viking Age runestone carvers",
        "ai_style_suffix": "in the style of Viking runestone carvings and Arthur Rackham's Norse illustrations, interlace patterns, iron and ice palette"
    },
    "arthurian": {
        "style": "Pre-Raphaelite medieval romance, illuminated manuscript borders, stained glass light",
        "palette": "heraldic red and gold, forest green, stone gray, stained glass blue",
        "reference_artists": "Aubrey Beardsley (1872-1898, Le Morte Darthur), Howard Pyle (1853-1911)",
        "ai_style_suffix": "in the style of Aubrey Beardsley's Le Morte Darthur woodcuts, Pre-Raphaelite medieval romance, illuminated manuscript borders"
    },
    "egyptian": {
        "style": "Ancient Egyptian tomb painting, flat profile figures, hieroglyphic borders, papyrus texture",
        "palette": "gold, lapis blue, papyrus cream, desert sand, hieroglyphic black",
        "reference_artists": "Ancient Egyptian tomb painters, Art Deco Egyptomania (Erté)",
        "ai_style_suffix": "in the style of ancient Egyptian tomb paintings, flat profile figures, hieroglyphic borders, gold and lapis on papyrus"
    },
    "ramayana": {
        "style": "Indian miniature painting, Pahari school, Mughal botanical borders, jewel-tone gouache",
        "palette": "jewel tones: ruby red, sapphire blue, emerald green, gold, lotus pink",
        "reference_artists": "Pahari miniature painters (17th-19th c.), Tanjore painting tradition",
        "ai_style_suffix": "in the style of Indian Pahari miniature painting, jewel-tone gouache, elaborate floral borders, divine radiance"
    },
    "polynesian": {
        "style": "Tapa cloth patterns, Marquesan tattoo geometry, ocean and volcanic colors",
        "palette": "ocean turquoise, volcanic black, tapa brown, coral pink, palm green",
        "reference_artists": "Traditional tapa cloth and tattoo pattern design",
        "ai_style_suffix": "in the style of Polynesian tapa cloth and tattoo art, bold geometric patterns, ocean turquoise and volcanic black"
    },
    "west-african": {
        "style": "Akan gold weight casting, Adinkra cloth stamping, spider web motifs, storytelling circle composition",
        "palette": "gold, indigo, kente yellow and green, spider-silk silver, warm brown",
        "reference_artists": "Akan gold weight tradition, Adinkra symbol makers",
        "ai_style_suffix": "in the style of Akan gold weights and Adinkra symbols, spider web composition, gold and indigo, warm storytelling firelight"
    },
    "maya": {
        "style": "Maya painted ceramics, Dresden Codex illustration, Hero Twin imagery, underworld jaguar motifs",
        "palette": "jade green, obsidian, cinnabar red, bone white, underworld black",
        "reference_artists": "Maya ceramic painters, codex illustrators",
        "ai_style_suffix": "in the style of ancient Maya painted ceramics and codex illustrations, jade and obsidian, Hero Twin imagery"
    },
    "dreamtime": {
        "style": "Aboriginal dot painting, x-ray bark painting, ochre earth palette, Songline mapping aesthetic",
        "palette": "ochre red, sand yellow, charcoal black, sky blue, white dot",
        "reference_artists": "Contemporary Aboriginal dot painting tradition (public domain patterns only)",
        "ai_style_suffix": "in the style of Aboriginal Australian dot painting and bark art, ochre palette, concentric circles, x-ray animal forms"
    },
    "tibetan": {
        "style": "Tibetan thangka painting, mandala geometry, bardo realm imagery, lotus and cloud motifs",
        "palette": "deep blue, saffron gold, lotus pink, cloud white, dharma red",
        "reference_artists": "Traditional thangka painters, Tibetan manuscript illumination",
        "ai_style_suffix": "in the style of Tibetan thangka painting, mandala geometry, jewel-tone pigments, cloud and lotus motifs, luminous bardo imagery"
    },
}

# Alice's consistent character description for AI prompts
ALICE_CHARACTER = "a girl of about 10 with shoulder-length dark hair, wearing a blue dress with white pinafore (Alice in Wonderland style), curious wide eyes, expressive face"

# Camera directions for different scene types
CAMERA_TYPES = {
    "establish": "Wide shot establishing the world. Slow zoom in.",
    "dialogue": "Medium shot, character faces visible. Gentle sway.",
    "action": "Dynamic angle, diagonal composition. Quick cuts.",
    "wonder": "Close-up on Alice's face reacting. Soft focus background.",
    "reveal": "Pull back to reveal the full scene. Hold wide.",
    "climax": "Low angle, dramatic lighting. Push in slowly.",
    "transition": "Dissolve/morph between worlds. Swirling motion.",
    "quiet": "Overhead or side angle. Stillness. Ambient sounds only.",
    "closing": "Slow pull back to wide. World recedes. Fade.",
}


def detect_scene_type(stanza_text, position, total_stanzas):
    """Detect the narrative function of a stanza for camera direction."""
    text_lower = stanza_text.lower()

    if position == 0:
        return "establish"
    if position >= total_stanzas - 1:
        return "closing"
    if position == total_stanzas - 2:
        return "quiet"

    # Dialogue indicators
    if "'" in stanza_text and ("said" in text_lower or "asked" in text_lower or "cried" in text_lower):
        return "dialogue"

    # Action indicators
    if any(w in text_lower for w in ["flew", "burst", "grabbed", "ran", "leapt", "fought",
                                       "struck", "threw", "opened", "transformed", "screamed"]):
        return "action"

    # Reveal indicators
    if any(w in text_lower for w in ["beheld", "appeared", "saw", "blazed", "shone",
                                       "revealed", "there stood", "there was"]):
        return "reveal"

    # Wonder/reaction
    if any(w in text_lower for w in ["oh!", "blinked", "wondered", "stared", "thought",
                                       "felt", "watched"]):
        return "wonder"

    # Climax tends to be in the 70-85% range
    ratio = position / total_stanzas
    if 0.65 < ratio < 0.85:
        return "climax"

    return "action"


def group_stanzas_into_scenes(stanzas, target_scenes=6):
    """Group stanzas into scenes based on narrative beats."""
    n = len(stanzas)
    if n <= target_scenes:
        # Each stanza is its own scene
        return [[s] for s in stanzas]

    # Group into roughly equal scenes, respecting narrative structure
    scenes = []
    stanzas_per_scene = max(2, n // target_scenes)

    current_scene = []
    for i, stanza in enumerate(stanzas):
        current_scene.append(stanza)

        # Scene break conditions:
        # 1. Hit target length
        at_target = len(current_scene) >= stanzas_per_scene
        # 2. Natural break (short stanza = beat change)
        is_short = len(stanza.split()) < 12
        # 3. Don't make too many scenes
        remaining = n - i - 1
        remaining_scenes = target_scenes - len(scenes) - 1

        if at_target and (remaining_scenes > 0 or remaining == 0):
            scenes.append(current_scene)
            current_scene = []
        elif is_short and len(current_scene) >= 2 and remaining_scenes > 0:
            scenes.append(current_scene)
            current_scene = []

    if current_scene:
        if scenes and len(current_scene) <= 2:
            # Merge tiny last scene with previous
            scenes[-1].extend(current_scene)
        else:
            scenes.append(current_scene)

    return scenes


def generate_image_prompt(scene_text, tradition, alice_present=True, scene_type="action"):
    """Generate an AI image generation prompt for a scene."""
    style_info = VISUAL_STYLES.get(tradition, {})
    style_suffix = style_info.get("ai_style_suffix", "illustrated in a mythological art style")
    palette = style_info.get("palette", "rich earth tones")

    # Extract the key visual moment from the scene text
    # Take the most visually descriptive line
    lines = scene_text.strip().split("\n")
    # Find line with most concrete nouns/adjectives
    visual_line = max(lines, key=lambda l: len([w for w in l.split()
                      if len(w) > 4 and w[0].isupper()]))

    # Build the prompt
    parts = []
    parts.append("Children's book illustration, full page, highly detailed")

    if alice_present and "alice" in scene_text.lower():
        parts.append(f"showing {ALICE_CHARACTER}")
        # Extract what Alice is doing
        for line in lines:
            if "alice" in line.lower():
                action = line.strip().rstrip(",.")
                if len(action) < 100:
                    parts.append(f"Scene: {action}")
                break
    else:
        # Extract the main action
        parts.append(f"Scene: {visual_line.strip()[:120]}")

    parts.append(f"Color palette: {palette}")
    parts.append(style_suffix)
    parts.append("No text or words in the image. Suitable for ages 4-10.")

    return ". ".join(parts)


def get_public_domain_refs(tradition):
    """Return public domain illustration references for a tradition."""
    refs = {
        "Haida / Tlingit / Tsimshian (Pacific Northwest)": [
            {"collection": "British Museum Haida collection", "note": "Historical drawings of Raven totem poles and masks, pre-1900"},
            {"collection": "Franz Boas field sketches (1897)", "note": "Tsimshian art documentation, public domain anthropological illustrations"},
        ],
        "Akan / Ashanti (West Africa)": [
            {"collection": "R.S. Rattray, Religion and Art in Ashanti (1927)", "note": "Plates of Akan gold weights, spider motifs, public domain"},
            {"collection": "Barker & Sinclair, West African Folk-Tales (1917)", "note": "Interior illustrations of Anansi stories"},
        ],
        "Inuit (Central Arctic)": [
            {"collection": "Fifth Thule Expedition illustrations (1921-24)", "note": "Knud Rasmussen expedition, Inuit life and myth documentation"},
        ],
        "Japanese (Shinto)": [
            {"collection": "Hokusai Manga (1814-1878)", "note": "15 volumes of sketches including mythological subjects, public domain"},
            {"collection": "Yoshitoshi, 100 Aspects of the Moon (1885-1892)", "note": "Ukiyo-e prints including Amaterasu cave scene"},
        ],
        "K'iche' Maya (Mesoamerica)": [
            {"collection": "Dresden Codex facsimile", "note": "Pre-Columbian Maya manuscript, public domain reproductions"},
            {"collection": "Frederick Catherwood, Views of Ancient Monuments (1844)", "note": "Detailed lithographs of Maya ruins and carvings"},
        ],
        "Sumerian (Mesopotamia, c. 1900-1600 BCE)": [
            {"collection": "British Museum cylinder seal impressions", "note": "Inanna/Ishtar descent imagery, public domain casts"},
            {"collection": "Leonard Woolley, Ur Excavations (1927-1934)", "note": "Archaeological illustration plates"},
        ],
        "biblical": [
            {"collection": "Gustave Doré, La Grande Bible de Tours (1866)", "note": "241 dramatic engravings, public domain"},
            {"collection": "William Blake visionary paintings (1795-1827)", "note": "Cosmic/esoteric biblical scenes"},
            {"collection": "James Tissot, Life of Our Lord (1886-1902)", "note": "Full color watercolors, Brooklyn Museum"},
            {"collection": "Julius Schnorr von Carolsfeld, Die Bibel in Bildern (1860)", "note": "240 clear woodcuts"},
        ],
        "homer": [
            {"collection": "John Flaxman, Iliad and Odyssey (1793)", "note": "Neoclassical line engravings of every major scene, public domain"},
            {"collection": "Greek vase paintings (British Museum, Met)", "note": "Red-figure and black-figure pottery depicting Trojan War and Odyssey scenes"},
        ],
        "norse": [
            {"collection": "Arthur Rackham, Norse Myths (various)", "note": "Atmospheric watercolors and pen drawings"},
            {"collection": "Lorenz Frølich, Norse mythology illustrations (1895)", "note": "Detailed engravings of Eddic scenes"},
        ],
        "arthurian": [
            {"collection": "Aubrey Beardsley, Le Morte Darthur (1893-1894)", "note": "Art Nouveau woodcuts for every book"},
            {"collection": "Howard Pyle, The Story of King Arthur (1903)", "note": "Full color plates and pen drawings"},
            {"collection": "Walter Crane, King Arthur's Knights (1911)", "note": "Decorative Arts & Crafts illustrations"},
        ],
        "egyptian": [
            {"collection": "Description de l'Égypte (1809-1829)", "note": "Napoleon expedition plates, temples and tomb paintings"},
            {"collection": "E.A. Wallis Budge, Gods of the Egyptians (1904)", "note": "Hieroglyphic and deity illustrations"},
        ],
        "ramayana": [
            {"collection": "Pahari miniature paintings (17th-19th c.)", "note": "Ramayana narrative scenes, various museum collections"},
            {"collection": "Ravi Varma Press chromolithographs (1894-1901)", "note": "Popular Indian mythological prints, public domain"},
        ],
    }
    return refs.get(tradition, [])


def estimate_timing(scene_text, narration_wpm=140):
    """Estimate scene duration in seconds."""
    words = len(scene_text.split())
    narration_secs = (words / narration_wpm) * 60
    # Add visual hold time (1.5 sec per image transition)
    visual_hold = 3.0
    return round(narration_secs + visual_hold)


def build_storyboard_grammar(source_grammar_path, grammar_slug, tradition_key, output_path):
    """Build a storyboard grammar from a source grammar."""
    with open(source_grammar_path, "r", encoding="utf-8") as f:
        source = json.load(f)

    # Determine field names
    verse_field = "Verse" if any("Verse" in i.get("sections", {})
                                 for i in source["items"] if i.get("level") == 1) else "Story"

    items = []
    sort_order = 0
    episode_num = 0

    for source_item in source["items"]:
        if source_item.get("level", 1) != 1:
            continue

        episode_num += 1
        verse = source_item["sections"].get(verse_field, "")
        if not verse:
            continue

        # Get tradition for this item
        meta = source_item.get("metadata", {})
        tradition = meta.get("tradition", tradition_key)

        # Split into stanzas
        stanzas = [s.strip() for s in verse.split("\n\n") if s.strip()]
        # Group into scenes
        scenes = group_stanzas_into_scenes(stanzas)

        scene_ids = []
        for scene_idx, scene_stanzas in enumerate(scenes):
            sort_order += 1
            scene_text = "\n\n".join(scene_stanzas)
            scene_type = detect_scene_type(scene_text, scene_idx, len(scenes))
            camera = CAMERA_TYPES.get(scene_type, CAMERA_TYPES["action"])

            scene_id = f"{source_item['id']}-scene-{scene_idx + 1:02d}"
            scene_ids.append(scene_id)

            # Determine if Alice is in this scene
            has_alice = "alice" in scene_text.lower() or grammar_slug == "alice-in-the-mythlands-storyboard"
            image_prompt = generate_image_prompt(scene_text, tradition, has_alice, scene_type)

            timing = estimate_timing(scene_text)
            word_count = len(scene_text.split())

            scene_item = {
                "id": scene_id,
                "name": f"Ep{episode_num} Scene {scene_idx + 1}: {source_item['name']}",
                "sort_order": sort_order,
                "category": source_item.get("category", source_item["id"]),
                "level": 1,
                "sections": {
                    "Narration": scene_text,
                    "Direction": f"[{scene_type.upper()}] {camera}",
                    "ImagePrompt": image_prompt,
                },
                "keywords": source_item.get("keywords", []) + [scene_type, f"scene-{scene_idx + 1}"],
                "metadata": {
                    "episode_id": source_item["id"],
                    "episode_name": source_item["name"],
                    "scene_number": scene_idx + 1,
                    "total_scenes": len(scenes),
                    "scene_type": scene_type,
                    "timing_seconds": timing,
                    "word_count": word_count,
                    "narration_wpm": 140,
                    "visual_style": VISUAL_STYLES.get(tradition, VISUAL_STYLES.get(tradition_key, {})),
                    "public_domain_refs": get_public_domain_refs(tradition) or get_public_domain_refs(tradition_key),
                    "camera": camera,
                }
            }

            # Add Original section if present
            if "Original" in source_item.get("sections", {}):
                if scene_idx == 0:  # Only on first scene of episode
                    scene_item["sections"]["SourceQuote"] = source_item["sections"]["Original"]

            items.append(scene_item)

        # Add L2 episode item
        sort_order += 1
        total_time = sum(
            item["metadata"]["timing_seconds"]
            for item in items
            if item.get("metadata", {}).get("episode_id") == source_item["id"]
        )

        wonder = source_item["sections"].get("Wonder", "")
        whisper = source_item["sections"].get("Whisper", "")
        note = source_item["sections"].get("Note for Grown-Ups", "")

        episode_item = {
            "id": f"episode-{source_item['id']}",
            "name": f"Episode {episode_num}: {source_item['name']}",
            "sort_order": sort_order,
            "category": "episodes",
            "level": 2,
            "composite_of": scene_ids,
            "relationship_type": "emergence",
            "sections": {
                "About": f"Episode {episode_num} of the series. {len(scenes)} scenes, ~{total_time} seconds total narration.",
                "Arc": f"Scenes: {' → '.join(scenes[i][0].split(chr(10))[0][:40] + '...' for i in range(min(4, len(scenes))))}",
                "Wonder": wonder if wonder else "What did you notice in this story?",
                "Whisper": whisper if whisper else "",
            },
            "keywords": source_item.get("keywords", []) + ["episode"],
            "metadata": {
                "total_scenes": len(scenes),
                "total_seconds": total_time,
                "total_minutes": round(total_time / 60, 1),
                "tradition": tradition,
                "visual_style": VISUAL_STYLES.get(tradition, VISUAL_STYLES.get(tradition_key, {})),
            }
        }
        if note:
            episode_item["sections"]["Note for Grown-Ups"] = note

        items.append(episode_item)

    # Build the storyboard grammar
    storyboard = {
        "_grammar_commons": source.get("_grammar_commons", {}),
        "name": source["name"] + " — Storyboard",
        "description": f"Production storyboard for animated series based on {source['name']}. "
                       f"Each story is split into {4}-{8} scenes with narration arcs, "
                       f"AI image generation prompts, camera directions, and public domain "
                       f"illustration references. Designed for 5-minute AI-animated episodes "
                       f"in the style of Mati and Dada.",
        "grammar_type": "sequence",
        "creator_name": source.get("creator_name", "PlayfulProcess"),
        "tags": source.get("tags", []) + ["storyboard", "animation", "ai-cartoon", "5-minute-episodes"],
        "roots": source.get("roots", []),
        "shelves": source.get("shelves", []),
        "lineages": source.get("lineages", []),
        "worldview": source.get("worldview", "animist"),
        "production_metadata": {
            "format": "5-minute animated episodes",
            "style_reference": "Mati and Dada (arte.tv)",
            "target_audience": "ages 4-10",
            "narration_speed_wpm": 140,
            "total_episodes": episode_num,
            "total_scenes": len([i for i in items if i.get("level") == 1]),
            "visual_style_guide": VISUAL_STYLES.get(tradition_key, {}),
            "alice_character_description": ALICE_CHARACTER if "alice" in grammar_slug else None,
        },
        "items": items,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(storyboard, f, indent=2, ensure_ascii=False)

    return episode_num, len([i for i in items if i.get("level") == 1])


def main():
    # Define all grammar → storyboard mappings
    mappings = [
        {
            "source": "grammars/alice-in-the-mythlands/grammar.json",
            "slug": "alice-in-the-mythlands-storyboard",
            "tradition_key": "Haida / Tlingit / Tsimshian (Pacific Northwest)",  # Default, overridden per item
            "output": "grammars/alice-in-the-mythlands-storyboard/grammar.json",
        },
        {
            "source": "grammars/biblical-stories-kids/grammar.json",
            "slug": "biblical-stories-kids-storyboard",
            "tradition_key": "biblical",
            "output": "grammars/biblical-stories-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/homer-kids/grammar.json",
            "slug": "homer-kids-storyboard",
            "tradition_key": "homer",
            "output": "grammars/homer-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/norse-kids/grammar.json",
            "slug": "norse-kids-storyboard",
            "tradition_key": "norse",
            "output": "grammars/norse-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/king-arthur-kids/grammar.json",
            "slug": "king-arthur-kids-storyboard",
            "tradition_key": "arthurian",
            "output": "grammars/king-arthur-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/egyptian-kids/grammar.json",
            "slug": "egyptian-kids-storyboard",
            "tradition_key": "egyptian",
            "output": "grammars/egyptian-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/ramayana-kids/grammar.json",
            "slug": "ramayana-kids-storyboard",
            "tradition_key": "ramayana",
            "output": "grammars/ramayana-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/polynesian-kids/grammar.json",
            "slug": "polynesian-kids-storyboard",
            "tradition_key": "polynesian",
            "output": "grammars/polynesian-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/west-african-kids/grammar.json",
            "slug": "west-african-kids-storyboard",
            "tradition_key": "west-african",
            "output": "grammars/west-african-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/maya-kids/grammar.json",
            "slug": "maya-kids-storyboard",
            "tradition_key": "maya",
            "output": "grammars/maya-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/dreamtime-kids/grammar.json",
            "slug": "dreamtime-kids-storyboard",
            "tradition_key": "dreamtime",
            "output": "grammars/dreamtime-kids-storyboard/grammar.json",
        },
        {
            "source": "grammars/tibetan-dream-kids/grammar.json",
            "slug": "tibetan-dream-kids-storyboard",
            "tradition_key": "tibetan",
            "output": "grammars/tibetan-dream-kids-storyboard/grammar.json",
        },
    ]

    # Filter to specific grammar if specified
    if len(sys.argv) > 1:
        filter_name = sys.argv[1]
        mappings = [m for m in mappings if filter_name in m["slug"] or filter_name in m["source"]]

    for m in mappings:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Building storyboard: {m['slug']}", file=sys.stderr)

        # Ensure output directory exists
        import os
        os.makedirs(os.path.dirname(m["output"]), exist_ok=True)

        episodes, scenes = build_storyboard_grammar(
            m["source"], m["slug"], m["tradition_key"], m["output"]
        )
        print(f"  → {episodes} episodes, {scenes} scenes", file=sys.stderr)
        print(f"  → Wrote {m['output']}", file=sys.stderr)


if __name__ == "__main__":
    main()
