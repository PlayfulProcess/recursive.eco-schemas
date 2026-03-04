#!/usr/bin/env python3
"""
Build the I Ching Leibniz Binary Emergent Grammar.

Maps the complete I Ching as a binary tree of change, following the insight
Leibniz had in 1703 when he recognized the Fu Xi/Shao Yong hexagram sequence
as binary counting from 0 (坤 Kun) to 63 (乾 Qian).

Structure:
  L1: 2 foundation lines (yin, yang) + 384 specific hexagram lines
      Each specific line is a transformation edge — when it changes,
      it transforms one hexagram into another by flipping a single bit.
  L2: 8 trigrams (ordered by Leibniz binary value 0-7)
  L3: 64 hexagrams (ordered by Leibniz value 0-63)

The 64 hexagrams form the vertices of a 6-dimensional binary hypercube.
The 384 lines are the directed edges connecting them.

Binary encoding:
  binary_str[0] = Line 1 (bottom), binary_str[5] = Line 6 (top)
  Leibniz value = int(binary_str, 2)
  (bottom line = MSB, matching Leibniz's convention)
"""

import json
import os
from copy import deepcopy

# ─── Paths ───

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_GRAMMAR = os.path.join(
    SCRIPT_DIR, "..", "i-ching-chinese-original-with-brief-translation", "grammar.json"
)
OUTPUT_GRAMMAR = os.path.join(SCRIPT_DIR, "grammar.json")

# ─── Trigram binary → info mapping (Leibniz order) ───

TRIGRAM_INFO = {
    "000": {"name": "earth",    "id": "trigram-earth",    "chinese": "坤", "pinyin": "Kūn",  "symbol": "☷", "leibniz": 0},
    "001": {"name": "mountain", "id": "trigram-mountain", "chinese": "艮", "pinyin": "Gèn",  "symbol": "☶", "leibniz": 1},
    "010": {"name": "water",    "id": "trigram-water",    "chinese": "坎", "pinyin": "Kǎn",  "symbol": "☵", "leibniz": 2},
    "011": {"name": "wind",     "id": "trigram-wind",     "chinese": "巽", "pinyin": "Xùn",  "symbol": "☴", "leibniz": 3},
    "100": {"name": "thunder",  "id": "trigram-thunder",  "chinese": "震", "pinyin": "Zhèn", "symbol": "☳", "leibniz": 4},
    "101": {"name": "fire",     "id": "trigram-fire",     "chinese": "離", "pinyin": "Lí",   "symbol": "☲", "leibniz": 5},
    "110": {"name": "lake",     "id": "trigram-lake",     "chinese": "兌", "pinyin": "Duì",  "symbol": "☱", "leibniz": 6},
    "111": {"name": "heaven",   "id": "trigram-heaven",   "chinese": "乾", "pinyin": "Qián", "symbol": "☰", "leibniz": 7},
}

# ─── L1: Foundation Lines (yin and yang archetypes) ───

FOUNDATION_LINES = [
    {
        "id": "yang-line",
        "name": "Yang Line (陽爻)",
        "symbol": "⚊",
        "level": 1,
        "category": "foundation",
        "sort_order": 0,
        "keywords": ["yang", "solid", "firm", "light", "creative", "heaven", "male", "one"],
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
                "creative, initiating force in the cosmos. In Leibniz's binary notation, "
                "yang = 1. In a hexagram, yang lines push upward and outward."
            ),
        },
    },
    {
        "id": "yin-line",
        "name": "Yin Line (陰爻)",
        "symbol": "⚋",
        "level": 1,
        "category": "foundation",
        "sort_order": 1,
        "keywords": ["yin", "broken", "yielding", "dark", "receptive", "earth", "female", "zero"],
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
                "nurturing, completing force in the cosmos. In Leibniz's binary notation, "
                "yin = 0. Where yang initiates, yin brings to completion."
            ),
        },
    },
]

# ─── L2: Trigram section content (說卦傳) ───

TRIGRAM_SECTIONS = {
    "000": {  # Earth
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
            "Leibniz value 0 — the origin, the empty ground from which all emerges."
        ),
        "Structure": (
            "⚋ 陰 yin (top)\n⚋ 陰 yin (middle)\n⚋ 陰 yin (bottom)\n\n"
            "三陰 — Three yin lines. Binary 000. Pure receptive force."
        ),
        "keywords": ["receptive", "yielding", "earth", "mother", "nourishing", "mare", "devotion"],
        "composite_of": ["yin-line"],
        "family_role": "母 (Mother)", "element": "地 (Earth)",
        "direction": "西南 (Southwest)", "body": "腹 (Belly)", "animal": "牛 (Ox)",
    },
    "001": {  # Mountain
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
            "Yang resting atop two yin: movement that has come to rest. "
            "Leibniz value 1 — the first differentiation from pure yin."
        ),
        "Structure": (
            "⚊ 陽 yang (top)\n⚋ 陰 yin (middle)\n⚋ 陰 yin (bottom)\n\n"
            "一陽止二陰上 — One yang atop two yin. Binary 001."
        ),
        "keywords": ["keeping-still", "mountain", "youngest-son", "stopping", "meditation", "boundary", "gate"],
        "composite_of": ["yang-line", "yin-line"],
        "family_role": "少男 (Youngest Son)", "element": "山 (Mountain)",
        "direction": "東北 (Northeast)", "body": "手 (Hand)", "animal": "狗 (Dog)",
    },
    "010": {  # Water
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
            "Yang trapped between two yin: light enclosed in darkness. "
            "Leibniz value 2 — danger and depth, the way through obstacles."
        ),
        "Structure": (
            "⚋ 陰 yin (top)\n⚊ 陽 yang (middle)\n⚋ 陰 yin (bottom)\n\n"
            "一陽陷二陰 — One yang between two yin. Binary 010."
        ),
        "keywords": ["abysmal", "danger", "water", "middle-son", "depth", "flow", "pit"],
        "composite_of": ["yang-line", "yin-line"],
        "family_role": "中男 (Middle Son)", "element": "水 (Water)",
        "direction": "北 (North)", "body": "耳 (Ear)", "animal": "豕 (Pig)",
    },
    "011": {  # Wind
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
            "Yin yielding beneath two yang: gentle penetration from below. "
            "Leibniz value 3 — what force cannot break, persistent gentleness penetrates."
        ),
        "Structure": (
            "⚊ 陽 yang (top)\n⚊ 陽 yang (middle)\n⚋ 陰 yin (bottom)\n\n"
            "一陰入二陽下 — One yin beneath two yang. Binary 011."
        ),
        "keywords": ["gentle", "penetrating", "wind", "eldest-daughter", "wood", "gradual", "influence"],
        "composite_of": ["yang-line", "yin-line"],
        "family_role": "長女 (Eldest Daughter)", "element": "風/木 (Wind/Wood)",
        "direction": "東南 (Southeast)", "body": "股 (Thigh)", "animal": "雞 (Rooster)",
    },
    "100": {  # Thunder
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
            "Leibniz value 4 — thunder shakes and awakens."
        ),
        "Structure": (
            "⚋ 陰 yin (top)\n⚋ 陰 yin (middle)\n⚊ 陽 yang (bottom)\n\n"
            "一陽二陰 — One yang rising beneath two yin. Binary 100."
        ),
        "keywords": ["arousing", "shock", "thunder", "eldest-son", "movement", "spring", "awakening"],
        "composite_of": ["yang-line", "yin-line"],
        "family_role": "長男 (Eldest Son)", "element": "雷 (Thunder)",
        "direction": "東 (East)", "body": "足 (Foot)", "animal": "龍 (Dragon)",
    },
    "101": {  # Fire
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
            "Yin held between two yang: darkness within brightness. "
            "Leibniz value 5 — clarity requires something to illuminate."
        ),
        "Structure": (
            "⚊ 陽 yang (top)\n⚋ 陰 yin (middle)\n⚊ 陽 yang (bottom)\n\n"
            "一陰麗二陽中 — One yin between two yang. Binary 101."
        ),
        "keywords": ["clinging", "brightness", "fire", "middle-daughter", "clarity", "illumination", "sun"],
        "composite_of": ["yang-line", "yin-line"],
        "family_role": "中女 (Middle Daughter)", "element": "火 (Fire)",
        "direction": "南 (South)", "body": "目 (Eye)", "animal": "雉 (Pheasant)",
    },
    "110": {  # Lake
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
            "Yin resting atop two yang: openness above strength. "
            "Leibniz value 6 — joy, exchange, and the pleasure of gathering together."
        ),
        "Structure": (
            "⚋ 陰 yin (top)\n⚊ 陽 yang (middle)\n⚊ 陽 yang (bottom)\n\n"
            "一陰悅二陽上 — One yin opening above two yang. Binary 110."
        ),
        "keywords": ["joyous", "lake", "youngest-daughter", "pleasure", "openness", "mouth", "gathering"],
        "composite_of": ["yang-line", "yin-line"],
        "family_role": "少女 (Youngest Daughter)", "element": "澤 (Lake/Marsh)",
        "direction": "西 (West)", "body": "口 (Mouth)", "animal": "羊 (Sheep)",
    },
    "111": {  # Heaven
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
            "Leibniz value 7 — the maximum, heaven moves ceaselessly."
        ),
        "Structure": (
            "⚊ 陽 yang (top)\n⚊ 陽 yang (middle)\n⚊ 陽 yang (bottom)\n\n"
            "三陽 — Three yang lines. Binary 111. Pure creative force."
        ),
        "keywords": ["creative", "strong", "heaven", "father", "initiating", "dragon", "power"],
        "composite_of": ["yang-line"],
        "family_role": "父 (Father)", "element": "天 (Heaven)",
        "direction": "西北 (Northwest)", "body": "首 (Head)", "animal": "馬 (Horse)",
    },
}

# ─── Line position names (Chinese tradition) ───

LINE_POSITION_NAMES = {
    1: ("初", "Beginning"),    # Bottom line
    2: ("二", "Second"),
    3: ("三", "Third"),
    4: ("四", "Fourth"),
    5: ("五", "Fifth"),
    6: ("上", "Top"),          # Top line
}

LINE_TYPE_CHINESE = {
    "1": ("九", "yang", "⚊"),   # Yang = Nine
    "0": ("六", "yin", "⚋"),    # Yin = Six
}


def load_source():
    """Load the existing Chinese I Ching grammar."""
    with open(SOURCE_GRAMMAR, "r", encoding="utf-8") as f:
        return json.load(f)


def build_lookups(source_items):
    """Build lookup tables from source hexagram data."""
    binary_to_item = {}
    for item in source_items:
        binary_to_item[item["metadata"]["binary"]] = item
    return binary_to_item


def flip_bit(binary_str, position):
    """Flip bit at position (0-indexed) in binary string."""
    bits = list(binary_str)
    bits[position] = "0" if bits[position] == "1" else "1"
    return "".join(bits)


def leibniz_value(binary_str):
    """Compute the Leibniz/Fu Xi sequence number from binary string."""
    return int(binary_str, 2)


# ─── Relationship computation functions ───


def compute_inverse(binary_str):
    """綜卦 (Zōngguà): flip upside down — reverse the line order."""
    return binary_str[::-1]


def compute_complement(binary_str):
    """錯卦 (Cuòguà): swap all yin↔yang — bitwise NOT."""
    return "".join("1" if b == "0" else "0" for b in binary_str)


def compute_nuclear(binary_str):
    """互卦 (Hùguà): inner hexagram — lines 2-3-4 as lower, 3-4-5 as upper."""
    return binary_str[1:4] + binary_str[2:5]


def compute_king_wen_pair(kw_number):
    """序卦傳: adjacent pair in King Wen sequence (1↔2, 3↔4, ... 63↔64)."""
    return kw_number + 1 if kw_number % 2 == 1 else kw_number - 1


# ─── Jing Fang's Eight Palaces (京房八宮) ───

PALACE_POSITION_NAMES = {
    1: "本宮 (Palace Master)",
    2: "一世 (1st Generation)",
    3: "二世 (2nd Generation)",
    4: "三世 (3rd Generation)",
    5: "四世 (4th Generation)",
    6: "五世 (5th Generation)",
    7: "遊魂 (Wandering Soul)",
    8: "歸魂 (Returning Soul)",
}


def build_palace_map():
    """Compute Jing Fang's Eight Palaces.

    Algorithm: start from each pure (doubled-trigram) hexagram, then
    cumulatively change lines 1→2→3→4→5. Position 7 (遊魂) restores line 4.
    Position 8 (歸魂) restores the lower trigram to the palace trigram.
    Line 6 never changes — the upper trigram defines the palace.

    Returns: {binary_str: (palace_chinese, palace_position)}
    """
    palace_map = {}
    # The 8 pure hexagrams (doubled trigrams)
    pure_binaries = [
        "111111", "000000", "010010", "101101",
        "100100", "001001", "011011", "110110",
    ]

    for pure_bin in pure_binaries:
        palace_chinese = TRIGRAM_INFO[pure_bin[0:3]]["chinese"]
        current = pure_bin
        palace_map[pure_bin] = (palace_chinese, 1)

        # Positions 2-6: cumulatively flip lines 1 through 5
        for pos in range(2, 7):
            line_idx = pos - 2  # line 1 = index 0, line 2 = index 1, ...
            current = flip_bit(current, line_idx)
            palace_map[current] = (palace_chinese, pos)

        # Position 7 (遊魂): restore line 4 (flip index 3 back)
        current = flip_bit(current, 3)
        palace_map[current] = (palace_chinese, 7)

        # Position 8 (歸魂): restore lower trigram to palace trigram
        current = pure_bin[0:3] + current[3:6]
        palace_map[current] = (palace_chinese, 8)

    return palace_map


# ─── Mawangdui Sequence (馬王堆) ───
# From the 168 BCE silk manuscript discovered in 1973 at Mawangdui, Changsha.
# Groups hexagrams by upper trigram. The upper and lower trigram orderings
# follow a specific pattern documented by Edward Shaughnessy (1996).
#
# Upper trigram order: 乾 坤 艮 兌 坎 離 震 巽
# Lower trigram order within each group: 乾 坤 艮 兌 坎 離 震 巽
# (same order — creating an 8×8 matrix read row by row)

MAWANGDUI_UPPER_ORDER = ["111", "000", "001", "110", "010", "101", "100", "011"]
MAWANGDUI_LOWER_ORDER = ["111", "000", "001", "110", "010", "101", "100", "011"]


def build_mawangdui_map():
    """Compute Mawangdui silk manuscript positions (1-64).

    Returns: {binary_str: position}
    """
    mawangdui_map = {}
    pos = 1
    for upper in MAWANGDUI_UPPER_ORDER:
        for lower in MAWANGDUI_LOWER_ORDER:
            binary = lower + upper  # binary_str[0:3] = lower, [3:6] = upper
            mawangdui_map[binary] = pos
            pos += 1
    return mawangdui_map


# ─── 雜卦傳 (Zá Guà Zhuàn) — Miscellaneous Notes Pairings ───
# One of the Ten Wings — pairs hexagrams by philosophical contrast.
# 32 pairs with brief Chinese characterizations.
# Format: (kw_a, kw_b): (characterization_a, characterization_b)

ZAGUA_PAIRS = {
    (1, 2): ("剛", "柔"),
    (3, 4): ("見而不失其居", "雜而著"),
    (5, 6): ("不進", "不親"),
    (7, 8): ("眾", "樂"),  # 師 = multitude, 比 = closeness
    (9, 10): ("寡", "不處"),
    (11, 12): ("通", "否"),  # 泰 = open, 否 = blocked
    (13, 14): ("親", "眾"),  # 同人 = kinship, 大有 = abundance
    (15, 16): ("輕", "怠"),
    (17, 18): ("無故", "則飭"),
    (19, 20): ("與", "求"),  # 臨 = giving approach, 觀 = seeking observation
    (21, 22): ("食", "無色"),
    (23, 24): ("爛", "反"),
    (25, 26): ("災", "時"),  # 無妄 = calamity, 大畜 = timely
    (27, 28): ("養正", "顛"),  # 頤 = nourishing, 大過 = toppling
    (29, 30): ("陷", "麗"),  # 坎 = falling in, 離 = clinging beauty
    (31, 32): ("速", "久"),
    (33, 34): ("退", "壯"),  # 遯 = withdrawing, 大壯 = great strength
    (35, 36): ("晝", "誅"),
    (37, 38): ("內", "外"),
    (39, 40): ("難", "緩"),
    (41, 42): ("衰之始", "盛之始"),
    (43, 44): ("決", "遇"),
    (45, 46): ("聚", "升"),  # 萃 = gathering, 升 = ascending
    (47, 48): ("困乎上", "通乎下"),  # 困 = confined above, 井 = flowing below
    (49, 50): ("去故", "取新"),
    (51, 52): ("起", "止"),
    (53, 54): ("女歸待男行", "女之終"),
    (55, 56): ("多故", "親寡"),
    (57, 58): ("伏", "見"),  # 巽 = hidden, 兌 = manifest
    (59, 60): ("離", "止"),  # 渙 = dispersal, 節 = restraint
    (61, 62): ("信", "過"),  # 中孚 = sincerity, 小過 = excess
    (63, 64): ("定", "男之窮"),
}


def build_zagua_lookup():
    """Build bidirectional lookup from ZAGUA_PAIRS.

    Returns: {kw_number: (pair_kw, own_characterization, pair_characterization)}
    """
    lookup = {}
    for (kw_a, kw_b), (char_a, char_b) in ZAGUA_PAIRS.items():
        lookup[kw_a] = (kw_b, char_a, char_b)
        lookup[kw_b] = (kw_a, char_b, char_a)
    return lookup


def build_trigram_items():
    """Build the 8 trigram items in Leibniz binary order (0-7)."""
    trigrams = []
    for binary_key in sorted(TRIGRAM_INFO.keys(), key=lambda b: int(b, 2)):
        info = TRIGRAM_INFO[binary_key]
        sections_data = TRIGRAM_SECTIONS[binary_key]

        trigram = {
            "id": info["id"],
            "name": f"{info['name'].title()} ({info['chinese']} {info['pinyin']})",
            "symbol": info["symbol"],
            "level": 2,
            "category": "trigram",
            "relationship_type": "emergence",
            "composite_of": sections_data["composite_of"],
            "keywords": sections_data["keywords"],
            "metadata": {
                "chinese_name": info["chinese"],
                "pinyin": info["pinyin"],
                "binary": binary_key,
                "leibniz_number": info["leibniz"],
                "family_role": sections_data["family_role"],
                "element": sections_data["element"],
                "direction": sections_data["direction"],
                "body": sections_data["body"],
                "animal": sections_data["animal"],
            },
            "sections": {
                "說卦傳": sections_data["說卦傳"],
                "Brief Translation": sections_data["Brief Translation"],
                "Nature": sections_data["Nature"],
                "Structure": sections_data["Structure"],
            },
        }
        trigrams.append(trigram)

    return trigrams


def build_line_items(source_items, binary_to_item):
    """Build the 384 specific line items as transformation edges."""
    lines = []

    # Sort hexagrams by Leibniz value for ordering
    sorted_hexagrams = sorted(
        source_items, key=lambda x: leibniz_value(x["metadata"]["binary"])
    )

    for hex_item in sorted_hexagrams:
        binary = hex_item["metadata"]["binary"]
        hex_num = hex_item["metadata"]["number"]
        hex_chinese = hex_item["metadata"]["chinese_name"]
        hex_name = hex_item["name"]
        parent_leibniz = leibniz_value(binary)

        for line_pos in range(1, 7):
            idx = line_pos - 1
            line_bit = binary[idx]
            line_chinese_num, line_type, line_symbol = LINE_TYPE_CHINESE[line_bit]
            pos_chinese, pos_english = LINE_POSITION_NAMES[line_pos]

            # Compute transformation target
            new_binary = flip_bit(binary, idx)
            target_item = binary_to_item[new_binary]
            target_num = target_item["metadata"]["number"]
            target_chinese = target_item["metadata"]["chinese_name"]
            target_name = target_item["name"]
            target_leibniz = leibniz_value(new_binary)

            # Get the original Chinese line text
            line_section_key = f"Line {line_pos}"
            chinese_text = hex_item["sections"].get(line_section_key, "")

            # Traditional line name: e.g. "初九" (Beginning Nine) or "六二" (Six in Second)
            if line_pos == 1:
                trad_name = f"{pos_chinese}{line_chinese_num}"  # 初九 or 初六
            elif line_pos == 6:
                trad_name = f"{pos_chinese}{line_chinese_num}"  # 上九 or 上六
            else:
                trad_name = f"{line_chinese_num}{pos_chinese}"  # 九二 or 六三

            line_item = {
                "id": f"hexagram-{hex_num}-line-{line_pos}",
                "name": f"{hex_chinese} {trad_name} · {hex_name} Line {line_pos}",
                "symbol": line_symbol,
                "level": 1,
                "category": "line",
                "keywords": [
                    line_type,
                    f"line-{line_pos}",
                    f"hexagram-{hex_num}",
                    f"transforms-to-{target_num}",
                ],
                "metadata": {
                    "parent_hexagram": f"hexagram-{hex_num}",
                    "transforms_to": f"hexagram-{target_num}",
                    "line_position": line_pos,
                    "line_type": line_type,
                    "traditional_name": trad_name,
                    "leibniz_parent": parent_leibniz,
                    "leibniz_target": target_leibniz,
                    "binary_flip": f"{binary} → {new_binary}",
                    "xor_value": 2 ** (5 - idx),
                },
                "sections": {
                    "經文": chinese_text,
                    "Transformation": (
                        f"此{line_type == 'yang' and '陽' or '陰'}爻變時，"
                        f"{hex_chinese}（{hex_name}，第{hex_num}卦）"
                        f"化為{target_chinese}（{target_name}，第{target_num}卦）。\n\n"
                        f"When this {'yang (solid)' if line_type == 'yang' else 'yin (broken)'} "
                        f"line changes → "
                        f"{target_chinese} ({target_name}, #{target_num}).\n"
                        f"Binary: {binary} → {new_binary}\n"
                        f"Leibniz: {parent_leibniz} → {target_leibniz} "
                        f"(XOR {2 ** (5 - idx)})"
                    ),
                },
            }
            lines.append(line_item)

    return lines


def build_hexagram_items(source_items, binary_to_item, palace_map,
                         mawangdui_map, zagua_lookup):
    """Transform source hexagrams to L3 items in Leibniz order."""
    hexagrams = []

    sorted_items = sorted(
        source_items, key=lambda x: leibniz_value(x["metadata"]["binary"])
    )

    for hex_item in sorted_items:
        item = deepcopy(hex_item)
        binary = item["metadata"]["binary"]
        hex_num = item["metadata"]["number"]
        lv = leibniz_value(binary)

        # Determine trigrams from binary string (NOT from the reversed metadata labels)
        lower_binary = binary[0:3]
        upper_binary = binary[3:6]
        lower_info = TRIGRAM_INFO[lower_binary]
        upper_info = TRIGRAM_INFO[upper_binary]

        # Set level and category
        item["level"] = 3
        item["category"] = "hexagram"
        item["relationship_type"] = "emergence"

        # composite_of → the 6 specific line IDs
        item["composite_of"] = [
            f"hexagram-{hex_num}-line-{pos}" for pos in range(1, 7)
        ]

        # Remove the Line 1-6 sections from the hexagram (they're now in separate L1 items)
        # Keep only Judgment and Image
        kept_sections = {}
        for key in ["Judgment", "Image"]:
            if key in item["sections"]:
                kept_sections[key] = item["sections"][key]
        # Add a Trigrams section showing the composition
        kept_sections["Trigrams"] = (
            f"上卦 (Upper): {upper_info['symbol']} {upper_info['chinese']} "
            f"{upper_info['name'].title()} ({upper_info['pinyin']})\n"
            f"下卦 (Lower): {lower_info['symbol']} {lower_info['chinese']} "
            f"{lower_info['name'].title()} ({lower_info['pinyin']})"
        )
        item["sections"] = kept_sections

        # Update metadata
        item["metadata"]["leibniz_number"] = lv
        item["metadata"]["leibniz_binary"] = format(lv, "06b")
        item["metadata"]["lower_trigram"] = lower_info["id"]
        item["metadata"]["upper_trigram"] = upper_info["id"]
        item["metadata"]["lower_trigram_name"] = (
            f"{lower_info['chinese']} {lower_info['name'].title()}"
        )
        item["metadata"]["upper_trigram_name"] = (
            f"{upper_info['chinese']} {upper_info['name'].title()}"
        )
        item["metadata"]["leibniz_matrix"] = (
            f"row {lower_info['leibniz']} ({lower_info['chinese']}), "
            f"col {upper_info['leibniz']} ({upper_info['chinese']})"
        )

        # ─── Relationship 1: 綜卦 Inverse (reverse line order) ───
        inverse_bin = compute_inverse(binary)
        inverse_kw = binary_to_item[inverse_bin]["metadata"]["number"]
        item["metadata"]["inverse_id"] = f"hexagram-{inverse_kw}"
        item["metadata"]["inverse_name"] = "綜卦"
        item["metadata"]["is_palindrome"] = (binary == inverse_bin)

        # ─── Relationship 2: 錯卦 Complement (flip all bits) ───
        complement_bin = compute_complement(binary)
        complement_kw = binary_to_item[complement_bin]["metadata"]["number"]
        item["metadata"]["complement_id"] = f"hexagram-{complement_kw}"
        item["metadata"]["complement_name"] = "錯卦"

        # ─── Relationship 3: 互卦 Nuclear (inner hexagram) ───
        nuclear_bin = compute_nuclear(binary)
        nuclear_kw = binary_to_item[nuclear_bin]["metadata"]["number"]
        item["metadata"]["nuclear_id"] = f"hexagram-{nuclear_kw}"
        item["metadata"]["nuclear_name"] = "互卦"

        # ─── Relationship 4: 序卦 King Wen Pair ───
        pair_kw = compute_king_wen_pair(hex_num)
        item["metadata"]["king_wen_pair_id"] = f"hexagram-{pair_kw}"
        item["metadata"]["king_wen_pair_name"] = "序卦"

        # ─── Relationship 5: 京房八宮 Jing Fang Palace ───
        palace_chinese, palace_pos = palace_map[binary]
        item["metadata"]["palace"] = palace_chinese
        item["metadata"]["palace_position"] = palace_pos
        item["metadata"]["palace_position_name"] = PALACE_POSITION_NAMES[palace_pos]

        # ─── Relationship 6: 馬王堆 Mawangdui Position ───
        item["metadata"]["mawangdui_position"] = mawangdui_map[binary]

        # ─── Relationship 7: 雜卦傳 Zagua Pairing ───
        if hex_num in zagua_lookup:
            pair_kw_z, own_char, pair_char = zagua_lookup[hex_num]
            item["metadata"]["zagua_pair_id"] = f"hexagram-{pair_kw_z}"
            item["metadata"]["zagua_characterization"] = own_char
            item["metadata"]["zagua_pair_characterization"] = pair_char
            item["metadata"]["zagua_name"] = "雜卦傳"

        # Clean up legacy fields
        item.pop("origin", None)
        item.pop("subcategory", None)
        item.pop("grammar_type", None)
        # Remove reversed trigram labels from metadata
        item["metadata"].pop("trigram_above", None)
        item["metadata"].pop("trigram_below", None)

        hexagrams.append(item)

    return hexagrams


def assign_sort_orders(foundation, lines, trigrams, hexagrams):
    """Assign sequential sort_order to all items."""
    offset = 0
    # Foundation lines: 0-1
    for i, item in enumerate(foundation):
        item["sort_order"] = offset + i
    offset += len(foundation)

    # Specific lines: 2-385
    for i, item in enumerate(lines):
        item["sort_order"] = offset + i
    offset += len(lines)

    # Trigrams: 386-393
    for i, item in enumerate(trigrams):
        item["sort_order"] = offset + i
    offset += len(trigrams)

    # Hexagrams: 394-457
    for i, item in enumerate(hexagrams):
        item["sort_order"] = offset + i


def build_grammar():
    """Build the complete Leibniz binary emergent grammar."""
    source = load_source()
    binary_to_item = build_lookups(source["items"])

    # Build relationship maps
    palace_map = build_palace_map()
    mawangdui_map = build_mawangdui_map()
    zagua_lookup = build_zagua_lookup()

    # Build all item groups
    foundation = deepcopy(FOUNDATION_LINES)
    lines = build_line_items(source["items"], binary_to_item)
    trigrams = build_trigram_items()
    hexagrams = build_hexagram_items(
        source["items"], binary_to_item, palace_map, mawangdui_map, zagua_lookup
    )

    # Assign sort orders
    assign_sort_orders(foundation, lines, trigrams, hexagrams)

    # Combine
    all_items = foundation + lines + trigrams + hexagrams

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
                    "note": "Trigram descriptions from the Ten Wings (十翼)",
                },
                {
                    "name": "繫辭傳 (Xi Ci Zhuan / Great Commentary)",
                    "date": "c. 300 BCE",
                    "note": "Yin-yang philosophy from the Ten Wings (十翼)",
                },
                {
                    "name": "Gottfried Wilhelm Leibniz",
                    "date": "1703",
                    "note": (
                        "Binary classification from 'Explication de l'Arithmétique Binaire' (1703). "
                        "Leibniz recognized the Fu Xi/Shao Yong hexagram sequence as binary counting 0-63 "
                        "after receiving the Xiantian diagram from Joachim Bouvet in 1701."
                    ),
                },
                {
                    "name": "邵雍 Shao Yong (Shào Yōng)",
                    "date": "1011-1077 CE",
                    "note": (
                        "Song dynasty philosopher who created the Xiantian (先天) hexagram arrangement "
                        "that Leibniz later recognized as binary. The ordering predates Leibniz by 600 years."
                    ),
                },
                {
                    "name": "序卦傳 / 雜卦傳 (Xù Guà Zhuàn / Zá Guà Zhuàn)",
                    "date": "c. 300 BCE",
                    "note": (
                        "Two of the Ten Wings (十翼): the Sequence of Hexagrams explains the King Wen "
                        "pairing logic; the Miscellaneous Notes pairs hexagrams by philosophical contrast."
                    ),
                },
                {
                    "name": "京房 Jing Fang (Jīng Fáng)",
                    "date": "78-37 BCE",
                    "note": (
                        "Han dynasty scholar who created the Eight Palaces (八宮) system, classifying "
                        "all 64 hexagrams into 8 groups of 8 by progressive line changes from pure trigrams. "
                        "From his work 京氏易傳 (Jīng Shì Yì Zhuàn)."
                    ),
                },
                {
                    "name": "馬王堆帛書 Mawangdui Silk Manuscript",
                    "date": "168 BCE (discovered 1973)",
                    "note": (
                        "Alternative hexagram sequence found in a Han dynasty tomb at Mawangdui, Changsha. "
                        "Groups hexagrams by upper trigram. Studied by Edward Shaughnessy (1996)."
                    ),
                },
            ],
        },
        "name": "易經 · Leibniz Binary Tree of Change (Lines → Trigrams → Hexagrams)",
        "description": (
            "The I Ching mapped as a 6-dimensional binary hypercube, following the insight "
            "Gottfried Wilhelm Leibniz had in 1703 when he recognized the Fu Xi/Shao Yong "
            "hexagram sequence as binary counting from 0 (坤 Kun, all yin) to 63 (乾 Qian, all yang). "
            "384 individual lines serve as transformation edges — when a line changes, it flips "
            "one bit and transforms one hexagram into another. The 64 hexagrams are vertices "
            "of the hypercube, connected by their 6 lines to 6 neighboring hexagrams. "
            "8 trigrams represent the 3-bit building blocks. "
            "Each hexagram carries 7 historical relationship systems in its metadata: "
            "綜卦 (inverse), 錯卦 (complement), 互卦 (nuclear), 序卦 (King Wen pair), "
            "京房八宮 (Jing Fang's Eight Palaces), 馬王堆 (Mawangdui sequence), "
            "and 雜卦傳 (Miscellaneous Notes pairings). "
            "All hexagram text is classical Chinese from Project Gutenberg eBook #25501.\n\n"
            "Source: Project Gutenberg eBook #25501 (https://www.gutenberg.org/ebooks/25501)\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES: "
            "The Leibniz-Bouvet diagram (1703) showing the 64 hexagrams arranged in binary order, "
            "housed at the Niedersächsische Landesbibliothek, Hanover. "
            "Shao Yong's Xiantian circular arrangement from various Song dynasty editions."
        ),
        "grammar_type": "iching",
        "creator_name": "PlayfulProcess",
        "tags": [
            "chinese",
            "original",
            "leibniz",
            "binary",
            "emergent",
            "lines",
            "trigrams",
            "hexagrams",
            "fu-xi",
            "shao-yong",
            "hypercube",
            "transformation",
            "classical",
            "public-domain",
            "inverse",
            "complement",
            "nuclear",
            "king-wen",
            "jing-fang",
            "eight-palaces",
            "mawangdui",
            "zagua",
            "relationships",
        ],
        "items": all_items,
    }

    return grammar


def validate_grammar(grammar):
    """Comprehensive validation."""
    items = grammar["items"]

    # 1. Total count
    assert len(items) == 458, f"Expected 458 items, got {len(items)}"

    # 2. Level distribution
    levels = {}
    for item in items:
        l = item["level"]
        levels[l] = levels.get(l, 0) + 1
    assert levels == {1: 386, 2: 8, 3: 64}, f"Unexpected levels: {levels}"

    # 3. No duplicate IDs
    ids = [item["id"] for item in items]
    dupes = [x for x in ids if ids.count(x) > 1]
    assert len(ids) == len(set(ids)), f"Duplicate IDs: {set(dupes)}"

    # 4. All composite_of references resolve
    id_set = set(ids)
    for item in items:
        for ref in item.get("composite_of", []):
            assert ref in id_set, f"Broken ref in {item['id']}: {ref}"

    # 5. All transforms_to references resolve
    hex_ids = {item["id"] for item in items if item["level"] == 3}
    for item in items:
        target = item.get("metadata", {}).get("transforms_to")
        if target:
            assert target in hex_ids, f"Bad transforms_to in {item['id']}: {target}"

    # 6. Each hexagram has exactly 6 line children
    for item in items:
        if item["level"] == 3:
            refs = item.get("composite_of", [])
            assert len(refs) == 6, f"{item['id']} has {len(refs)} line refs, expected 6"
            for ref in refs:
                assert ref in id_set, f"Broken line ref in {item['id']}: {ref}"

    # 7. Sort order sequential
    sort_orders = [item["sort_order"] for item in items]
    assert sort_orders == list(range(458)), (
        f"sort_order not sequential (first mismatch at {next(i for i, (a, b) in enumerate(zip(sort_orders, range(458))) if a != b)})"
    )

    # 8. Leibniz ordering check: trigrams 0-7, hexagrams 0-63
    trigram_leibniz = [
        item["metadata"]["leibniz_number"]
        for item in items
        if item["level"] == 2
    ]
    assert trigram_leibniz == list(range(8)), f"Trigrams not in Leibniz order: {trigram_leibniz}"

    hex_leibniz = [
        item["metadata"]["leibniz_number"]
        for item in items
        if item["level"] == 3
    ]
    assert hex_leibniz == list(range(64)), f"Hexagrams not in Leibniz order: {hex_leibniz[:10]}..."

    # 9. Verify transformation symmetry: if hex A line N → hex B, then hex B line N → hex A
    line_items = [item for item in items if item["level"] == 1 and "transforms_to" in item.get("metadata", {})]
    transform_map = {}
    for item in line_items:
        m = item["metadata"]
        key = (m["parent_hexagram"], m["line_position"])
        transform_map[key] = m["transforms_to"]

    for item in line_items:
        m = item["metadata"]
        parent = m["parent_hexagram"]
        target = m["transforms_to"]
        pos = m["line_position"]
        reverse_key = (target, pos)
        if reverse_key in transform_map:
            assert transform_map[reverse_key] == parent, (
                f"Asymmetric transform: {parent} line {pos} → {target}, "
                f"but {target} line {pos} → {transform_map[reverse_key]}"
            )

    # ─── Validate 7 Historical Relationship Systems ───

    hex_items = [item for item in items if item["level"] == 3]
    hex_id_to_item = {item["id"]: item for item in hex_items}
    hex_id_to_binary = {}
    for item in hex_items:
        hex_id_to_binary[item["id"]] = item["metadata"]["binary"]

    # 10. Inverse (綜卦): inverse(inverse(x)) == x
    palindrome_count = 0
    for item in hex_items:
        binary = item["metadata"]["binary"]
        inv_id = item["metadata"]["inverse_id"]
        assert inv_id in hex_id_to_item, f"Bad inverse_id in {item['id']}: {inv_id}"
        inv_item = hex_id_to_item[inv_id]
        assert inv_item["metadata"]["inverse_id"] == item["id"], (
            f"Inverse not symmetric: {item['id']} → {inv_id} → {inv_item['metadata']['inverse_id']}"
        )
        if item["metadata"]["is_palindrome"]:
            assert inv_id == item["id"], f"Palindrome {item['id']} should be its own inverse"
            palindrome_count += 1
    assert palindrome_count == 8, f"Expected 8 palindromes, got {palindrome_count}"

    # 11. Complement (錯卦): complement(complement(x)) == x, Leibniz sum == 63
    for item in hex_items:
        comp_id = item["metadata"]["complement_id"]
        assert comp_id in hex_id_to_item, f"Bad complement_id in {item['id']}: {comp_id}"
        comp_item = hex_id_to_item[comp_id]
        assert comp_item["metadata"]["complement_id"] == item["id"], (
            f"Complement not symmetric: {item['id']} → {comp_id} → {comp_item['metadata']['complement_id']}"
        )
        lv_sum = item["metadata"]["leibniz_number"] + comp_item["metadata"]["leibniz_number"]
        assert lv_sum == 63, (
            f"Complement Leibniz sum != 63: {item['id']}({item['metadata']['leibniz_number']}) + "
            f"{comp_id}({comp_item['metadata']['leibniz_number']}) = {lv_sum}"
        )

    # 12. Nuclear (互卦): all nuclear_id point to valid hexagram IDs
    for item in hex_items:
        nuc_id = item["metadata"]["nuclear_id"]
        assert nuc_id in hex_id_to_item, f"Bad nuclear_id in {item['id']}: {nuc_id}"

    # 13. King Wen Pair (序卦): symmetric, 32 unique pairs
    kw_pairs = set()
    for item in hex_items:
        pair_id = item["metadata"]["king_wen_pair_id"]
        assert pair_id in hex_id_to_item, f"Bad king_wen_pair_id in {item['id']}: {pair_id}"
        pair_item = hex_id_to_item[pair_id]
        assert pair_item["metadata"]["king_wen_pair_id"] == item["id"], (
            f"KW pair not symmetric: {item['id']} → {pair_id}"
        )
        pair_key = tuple(sorted([item["id"], pair_id]))
        kw_pairs.add(pair_key)
    assert len(kw_pairs) == 32, f"Expected 32 KW pairs, got {len(kw_pairs)}"

    # 14. Eight Palaces (八宮): 64 unique assignments, 8 palaces × 8 positions
    palace_assignments = set()
    palace_counts = {}
    for item in hex_items:
        palace = item["metadata"]["palace"]
        pos = item["metadata"]["palace_position"]
        key = (palace, pos)
        assert key not in palace_assignments, (
            f"Duplicate palace assignment: {palace} pos {pos} for {item['id']}"
        )
        palace_assignments.add(key)
        palace_counts[palace] = palace_counts.get(palace, 0) + 1
    assert len(palace_assignments) == 64, f"Expected 64 palace assignments, got {len(palace_assignments)}"
    for palace, count in palace_counts.items():
        assert count == 8, f"Palace {palace} has {count} members, expected 8"
    assert len(palace_counts) == 8, f"Expected 8 palaces, got {len(palace_counts)}"

    # 14b. Spot check: Qian palace should be KW# 1, 44, 33, 12, 20, 23, 35, 14
    qian_palace_kw = sorted([
        item["metadata"]["number"]
        for item in hex_items
        if item["metadata"]["palace"] == "乾"
    ])
    expected_qian = sorted([1, 44, 33, 12, 20, 23, 35, 14])
    assert qian_palace_kw == expected_qian, (
        f"Qian palace KW numbers wrong: {qian_palace_kw} != {expected_qian}"
    )

    # 15. Mawangdui: all 64 positions assigned, values 1-64
    mwd_positions = sorted([item["metadata"]["mawangdui_position"] for item in hex_items])
    assert mwd_positions == list(range(1, 65)), (
        f"Mawangdui positions not 1-64: {mwd_positions[:5]}...{mwd_positions[-5:]}"
    )

    # 16. Zagua (雜卦傳): all 64 hexagrams have pairs, all symmetric
    zagua_count = 0
    for item in hex_items:
        if "zagua_pair_id" in item["metadata"]:
            zagua_count += 1
            zpair_id = item["metadata"]["zagua_pair_id"]
            assert zpair_id in hex_id_to_item, f"Bad zagua_pair_id in {item['id']}: {zpair_id}"
            zpair_item = hex_id_to_item[zpair_id]
            assert "zagua_pair_id" in zpair_item["metadata"], (
                f"Zagua pair {zpair_id} missing zagua_pair_id"
            )
            assert zpair_item["metadata"]["zagua_pair_id"] == item["id"], (
                f"Zagua not symmetric: {item['id']} → {zpair_id} → {zpair_item['metadata']['zagua_pair_id']}"
            )
    assert zagua_count == 64, f"Expected 64 hexagrams with zagua pairs, got {zagua_count}"

    # ─── All relationship references resolve ───
    for item in hex_items:
        for field in ["inverse_id", "complement_id", "nuclear_id",
                      "king_wen_pair_id"]:
            ref = item["metadata"][field]
            assert ref in hex_id_to_item, f"Bad {field} in {item['id']}: {ref}"

    print("✓ All validations passed!")
    print(f"  - {len(items)} total items (2 foundation + 384 lines + 8 trigrams + 64 hexagrams)")
    print(f"  - Level distribution: L1={levels[1]}, L2={levels[2]}, L3={levels[3]}")
    print(f"  - No duplicate IDs")
    print(f"  - All composite_of and transforms_to references valid")
    print(f"  - Transformation symmetry verified (A→B implies B→A)")
    print(f"  - Leibniz ordering verified (trigrams 0-7, hexagrams 0-63)")
    print(f"  - Sort order sequential (0-457)")
    print(f"  - 綜卦 Inverse: symmetric, {palindrome_count} palindromes")
    print(f"  - 錯卦 Complement: symmetric, all Leibniz sums = 63")
    print(f"  - 互卦 Nuclear: all references valid")
    print(f"  - 序卦 King Wen pairs: {len(kw_pairs)} symmetric pairs")
    print(f"  - 八宮 Eight Palaces: {len(palace_counts)} palaces × 8 = {len(palace_assignments)} assignments")
    print(f"  - 八宮 Qian palace spot check: {expected_qian} ✓")
    print(f"  - 馬王堆 Mawangdui: positions 1-64 assigned")
    print(f"  - 雜卦傳 Zagua: {zagua_count} hexagrams paired, all symmetric")


def main():
    grammar = build_grammar()
    validate_grammar(grammar)

    with open(OUTPUT_GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(grammar, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Grammar written to {OUTPUT_GRAMMAR}")
    print(f"  {os.path.getsize(OUTPUT_GRAMMAR) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
