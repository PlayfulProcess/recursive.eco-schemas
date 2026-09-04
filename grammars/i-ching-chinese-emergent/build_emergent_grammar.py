#!/usr/bin/env python3
"""
Build the I Ching Chinese Emergent Grammar.

Transforms the existing flat Chinese I Ching grammar (64 hexagrams at L1)
into an emergent structure that mirrors the actual metaphysical construction:

  L1: Lines (陰爻 yin, 陽爻 yang) — the two primordial elements
  L2: Trigrams (八卦 bāguà) — 8 combinations of 3 lines
  L3: Hexagrams (六十四卦) — 64 combinations of 2 trigrams

This is the natural cosmological emergence of the I Ching itself.
"""

import json
import os
from copy import deepcopy

# ─── Paths ───

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_GRAMMAR = os.path.join(
    SCRIPT_DIR,
    "..",
    "i-ching-chinese-original-with-brief-translation",
    "grammar.json",
)
OUTPUT_GRAMMAR = os.path.join(SCRIPT_DIR, "grammar.json")

# ─── Trigram name → ID mapping ───

TRIGRAM_MAP = {
    "heaven": "trigram-heaven",
    "earth": "trigram-earth",
    "thunder": "trigram-thunder",
    "water": "trigram-water",
    "mountain": "trigram-mountain",
    "wind": "trigram-wind",
    "fire": "trigram-fire",
    "lake": "trigram-lake",
}

# ─── L1: Lines ───

LINE_ITEMS = [
    {
        "id": "yang-line",
        "name": "Yang Line (陽爻)",
        "symbol": "⚊",
        "level": 1,
        "category": "line",
        "sort_order": 0,
        "keywords": ["yang", "solid", "firm", "light", "creative", "heaven", "male"],
        "metadata": {
            "chinese_name": "陽爻",
            "pinyin": "yáng yáo",
            "binary": "1",
            "line_type": "solid",
        },
        "sections": {
            "繫辭傳": (
                "天尊地卑，乾坤定矣。卑高以陳，貴賤位矣。動靜有常，剛柔斷矣。"
                "一陰一陽之謂道。"
                "乾道成男，坤道成女。乾知大始，坤作成物。"
                "剛健中正，純粹精也。"
            ),
            "Brief Translation": (
                "Heaven is lofty, Earth is low; thus Qian and Kun are determined. "
                "The high and low are displayed, and the noble and humble have their places. "
                "Movement and rest have their constancy; the firm and yielding are thus distinguished. "
                "The alternation of yin and yang is called the Dao. "
                "The way of Qian forms the male; the way of Kun forms the female. "
                "Qian knows the great beginning; Kun brings things to completion. "
                "Firm, strong, centered, and correct — this is pure essence."
            ),
            "Nature": (
                "陽 (yáng): 天、剛、動、明、父\n"
                "Yang: Heaven, firmness, movement, light, the father principle.\n\n"
                "The yang line is solid and unbroken (⚊). It represents the active, "
                "creative, initiating force in the cosmos. In a hexagram, yang lines "
                "push upward and outward. The first yang was drawn when Fu Xi looked "
                "up and observed the patterns of heaven."
            ),
        },
    },
    {
        "id": "yin-line",
        "name": "Yin Line (陰爻)",
        "symbol": "⚋",
        "level": 1,
        "category": "line",
        "sort_order": 1,
        "keywords": ["yin", "broken", "yielding", "dark", "receptive", "earth", "female"],
        "metadata": {
            "chinese_name": "陰爻",
            "pinyin": "yīn yáo",
            "binary": "0",
            "line_type": "broken",
        },
        "sections": {
            "繫辭傳": (
                "坤至柔而動也剛，至靜而德方。後得主而有常，含萬物而化光。坤道其順乎，承天而時行。"
                "坤厚載物，德合無疆。含弘光大，品物咸亨。"
            ),
            "Brief Translation": (
                "Kun is most soft yet moves with firmness; most still yet its virtue is square. "
                "It follows and finds its lord, maintaining constancy. "
                "It contains the ten thousand things and transforms with brilliance. "
                "How compliant is the way of Kun! It receives heaven and acts in season. "
                "Kun is thick and carries all things; its virtue merges with the boundless. "
                "Containing, magnifying, illuminating, enlarging — all things flourish through it."
            ),
            "Nature": (
                "陰 (yīn): 地、柔、靜、暗、母\n"
                "Yin: Earth, yielding, stillness, darkness, the mother principle.\n\n"
                "The yin line is broken (⚋), split in the middle. It represents the receptive, "
                "nurturing, completing force in the cosmos. In a hexagram, yin lines "
                "receive, contain, and give form. Where yang initiates, yin brings to "
                "completion. The two together generate the ten thousand things."
            ),
        },
    },
]

# ─── L2: Trigrams ───

TRIGRAM_ITEMS = [
    {
        "id": "trigram-heaven",
        "name": "Heaven (乾 Qián)",
        "symbol": "☰",
        "level": 2,
        "category": "trigram",
        "sort_order": 2,
        "relationship_type": "emergence",
        "composite_of": ["yang-line"],
        "keywords": ["creative", "strong", "heaven", "father", "initiating", "dragon", "power"],
        "metadata": {
            "chinese_name": "乾",
            "pinyin": "Qián",
            "binary": "111",
            "family_role": "父 (Father)",
            "element": "天 (Heaven)",
            "direction": "西北 (Northwest)",
            "body": "首 (Head)",
            "animal": "馬 (Horse)",
        },
        "sections": {
            "說卦傳": (
                "乾為天、為圜、為君、為父、為玉、為金、為寒、為冰、為大赤、"
                "為良馬、為老馬、為瘠馬、為駁馬、為木果。"
                "乾，健也。"
            ),
            "Brief Translation": (
                "Qian is heaven, is round, is the ruler, is the father, is jade, is metal, "
                "is cold, is ice, is deep red, is a good horse, an old horse, a lean horse, "
                "a piebald horse, is tree fruit. "
                "Qian means strong, untiring."
            ),
            "Nature": (
                "天 (Heaven) · 父 (Father) · 西北 (Northwest) · 首 (Head)\n\n"
                "Three yang lines rising: pure creative force, undivided strength. "
                "Heaven moves ceaselessly — the superior man makes himself strong and untiring. "
                "When both trigrams in a hexagram are Heaven, creative power is at its purest (Hexagram 1)."
            ),
            "Structure": (
                "⚊ 陽 yang (top)\n⚊ 陽 yang (middle)\n⚊ 陽 yang (bottom)\n\n"
                "三陽 — Three yang lines. Pure, undivided creative force."
            ),
        },
    },
    {
        "id": "trigram-earth",
        "name": "Earth (坤 Kūn)",
        "symbol": "☷",
        "level": 2,
        "category": "trigram",
        "sort_order": 3,
        "relationship_type": "emergence",
        "composite_of": ["yin-line"],
        "keywords": ["receptive", "yielding", "earth", "mother", "nourishing", "mare", "devotion"],
        "metadata": {
            "chinese_name": "坤",
            "pinyin": "Kūn",
            "binary": "000",
            "family_role": "母 (Mother)",
            "element": "地 (Earth)",
            "direction": "西南 (Southwest)",
            "body": "腹 (Belly)",
            "animal": "牛 (Ox)",
        },
        "sections": {
            "說卦傳": (
                "坤為地、為母、為布、為釜、為吝嗇、為均、為子母牛、"
                "為大輿、為文、為眾、為柄。其於地也，為黑。"
                "坤，順也。"
            ),
            "Brief Translation": (
                "Kun is earth, is the mother, is cloth, is a cauldron, is thrift, "
                "is levelness, is a cow with calf, is a great cart, is pattern, "
                "is the multitude, is a handle. Among soils, it is black. "
                "Kun means yielding, devoted."
            ),
            "Nature": (
                "地 (Earth) · 母 (Mother) · 西南 (Southwest) · 腹 (Belly)\n\n"
                "Three yin lines: pure receptive force, total openness. "
                "Earth's nature is to receive and to carry. "
                "When both trigrams are Earth, receptivity is at its deepest (Hexagram 2)."
            ),
            "Structure": (
                "⚋ 陰 yin (top)\n⚋ 陰 yin (middle)\n⚋ 陰 yin (bottom)\n\n"
                "三陰 — Three yin lines. Pure, undivided receptive force."
            ),
        },
    },
    {
        "id": "trigram-thunder",
        "name": "Thunder (震 Zhèn)",
        "symbol": "☳",
        "level": 2,
        "category": "trigram",
        "sort_order": 4,
        "relationship_type": "emergence",
        "composite_of": ["yang-line", "yin-line"],
        "keywords": ["arousing", "shock", "thunder", "eldest-son", "movement", "spring", "awakening"],
        "metadata": {
            "chinese_name": "震",
            "pinyin": "Zhèn",
            "binary": "100",
            "family_role": "長男 (Eldest Son)",
            "element": "雷 (Thunder)",
            "direction": "東 (East)",
            "body": "足 (Foot)",
            "animal": "龍 (Dragon)",
        },
        "sections": {
            "說卦傳": (
                "震為雷、為龍、為玄黃、為旉、為大塗、為長子、為決躁、"
                "為蒼筤竹、為萑葦。其於馬也，為善鳴、為馵足、為作足、為的顙。"
                "其於稼也，為反生。其究為健，為蕃鮮。"
                "震，動也。"
            ),
            "Brief Translation": (
                "Zhen is thunder, is the dragon, is dark yellow, is spreading, "
                "is a great road, is the eldest son, is decisiveness and restlessness, "
                "is green young bamboo, is reeds and rushes. Among horses, it is one that "
                "neighs well, has white hind legs, gallops, has a white forehead. "
                "Among crops, it is one that grows back. Its ultimate meaning is strength, "
                "luxuriant freshness. Zhen means movement, arousal."
            ),
            "Nature": (
                "雷 (Thunder) · 長男 (Eldest Son) · 東 (East) · 足 (Foot)\n\n"
                "One yang below two yin: yang energy bursts forth from beneath the earth. "
                "Thunder shakes and awakens. Spring begins with thunder — "
                "the first son moves out from the receptive mother."
            ),
            "Structure": (
                "⚋ 陰 yin (top)\n⚋ 陰 yin (middle)\n⚊ 陽 yang (bottom)\n\n"
                "一陽二陰 — One yang rising beneath two yin. Arousing movement from below."
            ),
        },
    },
    {
        "id": "trigram-water",
        "name": "Water (坎 Kǎn)",
        "symbol": "☵",
        "level": 2,
        "category": "trigram",
        "sort_order": 5,
        "relationship_type": "emergence",
        "composite_of": ["yang-line", "yin-line"],
        "keywords": ["abysmal", "danger", "water", "middle-son", "depth", "flow", "pit"],
        "metadata": {
            "chinese_name": "坎",
            "pinyin": "Kǎn",
            "binary": "010",
            "family_role": "中男 (Middle Son)",
            "element": "水 (Water)",
            "direction": "北 (North)",
            "body": "耳 (Ear)",
            "animal": "豕 (Pig)",
        },
        "sections": {
            "說卦傳": (
                "坎為水、為溝瀆、為隱伏、為矯輮、為弓輪。"
                "其於人也，為加憂、為心病、為耳痛、為血卦、為赤。"
                "其於馬也，為美脊、為亟心、為下首、為薄蹄、為曳。"
                "其於輿也，為多眚。為通、為月、為盜。"
                "其於木也，為堅多心。"
                "坎，陷也。"
            ),
            "Brief Translation": (
                "Kan is water, is ditches and channels, is concealment, is bending and straightening, "
                "is the bow and wheel. For people, it is added worry, heart sickness, earache; "
                "it is the blood trigram, is red. Among horses, it is one with fine spine, "
                "anxious heart, drooping head, thin hooves, that stumbles. "
                "Among carts, it has many defects. It is penetration, the moon, the thief. "
                "Among trees, it is firm with much pith. Kan means falling in, the pit."
            ),
            "Nature": (
                "水 (Water) · 中男 (Middle Son) · 北 (North) · 耳 (Ear)\n\n"
                "Yang trapped between two yin: light enclosed in darkness, "
                "like water flowing through a ravine. Danger and depth — "
                "but also the way that finds its course through any obstacle."
            ),
            "Structure": (
                "⚋ 陰 yin (top)\n⚊ 陽 yang (middle)\n⚋ 陰 yin (bottom)\n\n"
                "一陽陷二陰 — One yang sunk between two yin. Light within darkness, danger within depth."
            ),
        },
    },
    {
        "id": "trigram-mountain",
        "name": "Mountain (艮 Gèn)",
        "symbol": "☶",
        "level": 2,
        "category": "trigram",
        "sort_order": 6,
        "relationship_type": "emergence",
        "composite_of": ["yang-line", "yin-line"],
        "keywords": ["keeping-still", "mountain", "youngest-son", "stopping", "meditation", "boundary", "gate"],
        "metadata": {
            "chinese_name": "艮",
            "pinyin": "Gèn",
            "binary": "001",
            "family_role": "少男 (Youngest Son)",
            "element": "山 (Mountain)",
            "direction": "東北 (Northeast)",
            "body": "手 (Hand)",
            "animal": "狗 (Dog)",
        },
        "sections": {
            "說卦傳": (
                "艮為山、為徑路、為小石、為門闕、為果蓏、為閽寺、為指、"
                "為狗、為鼠、為黔喙之屬。"
                "其於木也，為堅多節。"
                "艮，止也。"
            ),
            "Brief Translation": (
                "Gen is mountain, is a bypath, is small stones, is a gate or watchtower, "
                "is fruits and gourds, is a gatekeeper, is the finger, "
                "is the dog, is the rat, is black-billed birds. "
                "Among trees, it is firm with many knots. "
                "Gen means stopping, keeping still."
            ),
            "Nature": (
                "山 (Mountain) · 少男 (Youngest Son) · 東北 (Northeast) · 手 (Hand)\n\n"
                "Yang resting atop two yin: movement that has come to rest, "
                "like a mountain rising from the earth. Stillness, boundaries, meditation — "
                "knowing when to stop is the deepest wisdom."
            ),
            "Structure": (
                "⚊ 陽 yang (top)\n⚋ 陰 yin (middle)\n⚋ 陰 yin (bottom)\n\n"
                "一陽止二陰上 — One yang resting atop two yin. Stillness crowning openness."
            ),
        },
    },
    {
        "id": "trigram-wind",
        "name": "Wind (巽 Xùn)",
        "symbol": "☴",
        "level": 2,
        "category": "trigram",
        "sort_order": 7,
        "relationship_type": "emergence",
        "composite_of": ["yang-line", "yin-line"],
        "keywords": ["gentle", "penetrating", "wind", "eldest-daughter", "wood", "gradual", "influence"],
        "metadata": {
            "chinese_name": "巽",
            "pinyin": "Xùn",
            "binary": "011",
            "family_role": "長女 (Eldest Daughter)",
            "element": "風/木 (Wind/Wood)",
            "direction": "東南 (Southeast)",
            "body": "股 (Thigh)",
            "animal": "雞 (Rooster)",
        },
        "sections": {
            "說卦傳": (
                "巽為木、為風、為長女、為繩直、為工、為白、為長、為高、"
                "為進退、為不果、為臭。"
                "其於人也，為寡髮、為廣顙、為多白眼、為近利市三倍。"
                "其究為躁卦。"
                "巽，入也。"
            ),
            "Brief Translation": (
                "Xun is wood, is wind, is the eldest daughter, is the plumb line, "
                "is the carpenter, is white, is long, is high, "
                "is advancing and retreating, is indecision, is smell. "
                "For people, it is thin hair, wide forehead, much white in the eyes, "
                "and profit close to threefold in the market. "
                "Its ultimate meaning is the trigram of restlessness. "
                "Xun means entering, penetrating gently."
            ),
            "Nature": (
                "風/木 (Wind/Wood) · 長女 (Eldest Daughter) · 東南 (Southeast) · 股 (Thigh)\n\n"
                "Yin yielding beneath two yang: gentle penetration from below, "
                "like wind entering everywhere or roots growing into earth. "
                "What force cannot break, persistent gentleness penetrates."
            ),
            "Structure": (
                "⚊ 陽 yang (top)\n⚊ 陽 yang (middle)\n⚋ 陰 yin (bottom)\n\n"
                "一陰入二陽下 — One yin entering beneath two yang. Gentle penetration from below."
            ),
        },
    },
    {
        "id": "trigram-fire",
        "name": "Fire (離 Lí)",
        "symbol": "☲",
        "level": 2,
        "category": "trigram",
        "sort_order": 8,
        "relationship_type": "emergence",
        "composite_of": ["yang-line", "yin-line"],
        "keywords": ["clinging", "brightness", "fire", "middle-daughter", "clarity", "illumination", "sun"],
        "metadata": {
            "chinese_name": "離",
            "pinyin": "Lí",
            "binary": "101",
            "family_role": "中女 (Middle Daughter)",
            "element": "火 (Fire)",
            "direction": "南 (South)",
            "body": "目 (Eye)",
            "animal": "雉 (Pheasant)",
        },
        "sections": {
            "說卦傳": (
                "離為火、為日、為電、為中女、為甲胄、為戈兵。"
                "其於人也，為大腹。為乾卦。為鱉、為蟹、為蠃、為蚌、為龜。"
                "其於木也，為科上槁。"
                "離，麗也。"
            ),
            "Brief Translation": (
                "Li is fire, is the sun, is lightning, is the middle daughter, "
                "is armor and helmets, is spears and weapons. "
                "For people, it is a large belly. It is the trigram of dryness. "
                "It is the turtle, the crab, the snail, the mussel, the tortoise. "
                "Among trees, it is hollow above and dry. "
                "Li means clinging, brightness, beauty."
            ),
            "Nature": (
                "火 (Fire) · 中女 (Middle Daughter) · 南 (South) · 目 (Eye)\n\n"
                "Yin held between two yang: darkness within brightness, "
                "like flame that clings to fuel to shine. "
                "Fire illuminates but must depend on what it burns — "
                "clarity requires something to illuminate."
            ),
            "Structure": (
                "⚊ 陽 yang (top)\n⚋ 陰 yin (middle)\n⚊ 陽 yang (bottom)\n\n"
                "一陰麗二陽中 — One yin clinging between two yang. Brightness embracing darkness within."
            ),
        },
    },
    {
        "id": "trigram-lake",
        "name": "Lake (兌 Duì)",
        "symbol": "☱",
        "level": 2,
        "category": "trigram",
        "sort_order": 9,
        "relationship_type": "emergence",
        "composite_of": ["yang-line", "yin-line"],
        "keywords": ["joyous", "lake", "youngest-daughter", "pleasure", "openness", "mouth", "gathering"],
        "metadata": {
            "chinese_name": "兌",
            "pinyin": "Duì",
            "binary": "110",
            "family_role": "少女 (Youngest Daughter)",
            "element": "澤 (Lake/Marsh)",
            "direction": "西 (West)",
            "body": "口 (Mouth)",
            "animal": "羊 (Sheep)",
        },
        "sections": {
            "說卦傳": (
                "兌為澤、為少女、為巫、為口舌、為毀折、為附決。"
                "其於地也，為剛鹵。為妾、為羊。"
                "兌，說也。"
            ),
            "Brief Translation": (
                "Dui is the lake/marsh, is the youngest daughter, is the shaman/sorceress, "
                "is the mouth and tongue, is breaking and destroying, is bursting open. "
                "Among soils, it is hard and salty. It is the concubine, is the sheep. "
                "Dui means joy, delight, speaking."
            ),
            "Nature": (
                "澤 (Lake) · 少女 (Youngest Daughter) · 西 (West) · 口 (Mouth)\n\n"
                "Yin resting atop two yang: openness above strength, "
                "like a lake that gathers water in a basin and reflects the sky. "
                "Joy, exchange, and the pleasure of gathering together."
            ),
            "Structure": (
                "⚋ 陰 yin (top)\n⚊ 陽 yang (middle)\n⚊ 陽 yang (bottom)\n\n"
                "一陰悅二陽上 — One yin opening above two yang. Joyous openness crowning strength."
            ),
        },
    },
]


def load_source_grammar():
    """Load the existing Chinese I Ching grammar."""
    with open(SOURCE_GRAMMAR, "r", encoding="utf-8") as f:
        return json.load(f)


def transform_hexagrams(source_items):
    """Transform the 64 hexagrams from L1 to L3, adding trigram references."""
    hexagrams = []
    for i, item in enumerate(source_items):
        hex_item = deepcopy(item)

        # Set to level 3
        hex_item["level"] = 3
        hex_item["category"] = "hexagram"
        hex_item["relationship_type"] = "emergence"
        hex_item["sort_order"] = 10 + i

        # Map trigram names to IDs for composite_of
        trigram_above = item["metadata"].get("trigram_above", "")
        trigram_below = item["metadata"].get("trigram_below", "")

        above_id = TRIGRAM_MAP.get(trigram_above)
        below_id = TRIGRAM_MAP.get(trigram_below)

        if above_id and below_id:
            # Lower trigram listed first (it's the foundation), upper second
            hex_item["composite_of"] = [below_id, above_id]
        else:
            print(f"WARNING: Missing trigram mapping for {item['id']}: "
                  f"above={trigram_above}, below={trigram_below}")
            hex_item["composite_of"] = []

        # Clean up fields that don't fit the new structure
        hex_item.pop("origin", None)
        hex_item.pop("subcategory", None)
        hex_item.pop("grammar_type", None)

        hexagrams.append(hex_item)

    return hexagrams


def build_grammar():
    """Build the complete emergent grammar."""
    source = load_source_grammar()

    # Transform hexagrams
    hexagrams = transform_hexagrams(source["items"])

    # Combine all items: lines + trigrams + hexagrams
    all_items = LINE_ITEMS + TRIGRAM_ITEMS + hexagrams

    # Build grammar envelope
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "I Ching (易經)",
                    "date": "c. 1000-750 BCE",
                    "note": "Original Chinese text from Project Gutenberg eBook #25501",
                },
                {
                    "name": "說卦傳 (Shuo Gua Zhuan / Discussion of Trigrams)",
                    "date": "c. 300 BCE",
                    "note": "Classical commentary on the eight trigrams, part of the Ten Wings (十翼)",
                },
                {
                    "name": "繫辭傳 (Xi Ci Zhuan / Great Commentary)",
                    "date": "c. 300 BCE",
                    "note": "Classical commentary on yin-yang philosophy, part of the Ten Wings (十翼)",
                },
            ],
        },
        "name": "易經 · Emergent Structure (Lines → Trigrams → Hexagrams)",
        "description": (
            "The I Ching reorganized to mirror its own cosmological emergence: "
            "from the two primordial lines (陰 yin and 陽 yang), "
            "through the eight trigrams (八卦 bāguà), "
            "to the sixty-four hexagrams (六十四卦). "
            "Classical Chinese text throughout, with brief English translations for lines and trigrams. "
            "Hexagram text extracted from Project Gutenberg eBook #25501. "
            "Trigram descriptions from the 說卦傳 (Shuo Gua Zhuan / Discussion of Trigrams). "
            "Line philosophy from the 繫辭傳 (Xi Ci Zhuan / Great Commentary).\n\n"
            "Source: Project Gutenberg eBook #25501 (https://www.gutenberg.org/ebooks/25501)"
        ),
        "grammar_type": "iching",
        "creator_name": "PlayfulProcess",
        "tags": [
            "chinese",
            "original",
            "emergent",
            "lines",
            "trigrams",
            "hexagrams",
            "classical",
            "public-domain",
        ],
        "items": all_items,
    }

    return grammar


def validate_grammar(grammar):
    """Validate the grammar structure."""
    items = grammar["items"]

    # Check total count
    assert len(items) == 74, f"Expected 74 items, got {len(items)}"

    # Check level distribution
    levels = {}
    for item in items:
        l = item["level"]
        levels[l] = levels.get(l, 0) + 1
    assert levels == {1: 2, 2: 8, 3: 64}, f"Unexpected level distribution: {levels}"

    # Check no duplicate IDs
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found: {[x for x in ids if ids.count(x) > 1]}"

    # Check all composite_of references resolve
    id_set = set(ids)
    for item in items:
        for ref in item.get("composite_of", []):
            assert ref in id_set, f"Broken reference in {item['id']}: {ref} not found"

    # Check sort_order is sequential
    sort_orders = [item["sort_order"] for item in items]
    assert sort_orders == list(range(74)), f"sort_order not sequential: {sort_orders[:15]}..."

    # Check all items have required fields
    required = {"id", "name", "sections", "level", "category"}
    for item in items:
        missing = required - set(item.keys())
        assert not missing, f"Item {item['id']} missing fields: {missing}"

    print("✓ All validations passed!")
    print(f"  - {len(items)} total items")
    print(f"  - Level distribution: L1={levels[1]}, L2={levels[2]}, L3={levels[3]}")
    print(f"  - No duplicate IDs")
    print(f"  - All composite_of references valid")
    print(f"  - Sort order sequential (0-73)")


def main():
    grammar = build_grammar()
    validate_grammar(grammar)

    with open(OUTPUT_GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(grammar, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Grammar written to {OUTPUT_GRAMMAR}")


if __name__ == "__main__":
    main()
