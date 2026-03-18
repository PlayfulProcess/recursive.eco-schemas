#!/usr/bin/env python3
"""
Generate the skeleton for 'The Tarot of All Tarots' grammar.

Maps cards across 7 deck schemas (RWS, Marseille, Sola Busca, Etteilla I/II/III, Tarocchino)
and produces a unified 78-card grammar with image URLs and section stubs.
"""

import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(BASE, "schemas", "tarot")

# ─── Load all decks ───────────────────────────────────────────────────────────

def load_deck(filename):
    path = os.path.join(SCHEMA_DIR, filename)
    with open(path) as f:
        return json.load(f)

rws = load_deck("rider-waide-archetypical")
marseille = load_deck("marseille")
sola_busca = load_deck("sola-busca")
etteilla_i = load_deck("etteilla-i")
etteilla_ii = load_deck("etteila-II")
etteilla_iii = load_deck("etteilla-III")
tarocchino = load_deck("tarocchino-arlecchino")

# ─── Index helpers ────────────────────────────────────────────────────────────

SUIT_MAP = {
    "pentacles": "pentacles", "coins": "coins", "deniers": "coins",
    "Coins": "coins",
    "wands": "wands", "batons": "wands", "Batons": "wands",
    "cups": "cups", "coupes": "cups", "Cups": "cups",
    "swords": "swords", "epees": "swords", "Swords": "swords",
}

# Map French rank words to standard rank numbers (1-14)
FRENCH_RANK_MAP = {
    "as": 1, "ace": 1,
    "deux": 2, "two": 2,
    "trois": 3, "three": 3,
    "quatre": 4, "four": 4,
    "cinq": 5, "five": 5,
    "six": 6,
    "sept": 7, "seven": 7,
    "huit": 8, "eight": 8,
    "neuf": 9, "nine": 9,
    "dix": 10, "ten": 10,
    "valet": 11, "page": 11, "knave": 11,
    "chevalier": 12, "knight": 12,
    "reine": 13, "queen": 13,
    "roi": 14, "king": 14,
    "le roi": 14, "la reine": 13, "le chevalier": 12, "le valet": 11,
}


def extract_rank_from_name(name):
    """Extract rank number (1-14) from card name like 'Roi de Coupe', 'Le Roi de Baton', or 'Ace of Cups'."""
    lower = name.lower().strip()
    # Strip French articles
    for article in ["le ", "la ", "l'", "les "]:
        if lower.startswith(article):
            lower = lower[len(article):]
            break
    for rank_word, rank_num in sorted(FRENCH_RANK_MAP.items(), key=lambda x: -len(x[0])):
        if lower.startswith(rank_word):
            return rank_num
    return None


def index_by_number_and_suit(deck):
    """Index cards by (arcana, rank_within_suit, normalized_suit) tuple."""
    idx = {}
    for item in deck["items"]:
        meta = item.get("metadata", {})
        arcana = meta.get("arcana", item.get("category", ""))
        number = meta.get("number")
        suit = meta.get("suit")
        norm_suit = SUIT_MAP.get(suit) if suit else None

        if arcana == "major":
            key = (arcana, number, norm_suit)
            idx[key] = item
        else:
            # For minor arcana, derive rank from name if number is global (Etteilla style)
            # Standard decks use 1-14 per suit, Etteilla uses 22-77 globally
            rank = number
            if number and number > 14:
                # Global numbering — extract rank from card name
                rank = extract_rank_from_name(item.get("name", ""))
            key = (arcana, rank, norm_suit)
            if rank is not None:
                idx[key] = item
    return idx

rws_idx = index_by_number_and_suit(rws)
mars_idx = index_by_number_and_suit(marseille)
sb_idx = index_by_number_and_suit(sola_busca)
ett1_idx = index_by_number_and_suit(etteilla_i)
ett2_idx = index_by_number_and_suit(etteilla_ii)
ett3_idx = index_by_number_and_suit(etteilla_iii)
taro_idx = index_by_number_and_suit(tarocchino)

# ─── Etteilla major arcana mapping to RWS ────────────────────────────────────
# Etteilla uses Genesis ordering. These are the ones that map to standard majors.

ETTEILLA_TO_RWS_MAJOR = {
    0: 0,    # La Folie → The Fool
    9: 11,   # La Justice → Justice (RWS #11, but we use 8 in some traditions)
    10: 14,  # La Tempérance → Temperance
    11: 8,   # La Force → Strength
    13: 5,   # Le Grand Prêtre → Hierophant
    14: 15,  # Le Diable → Devil
    15: 1,   # Le Magicien → Magician
    16: 20,  # Le Jugement Dernier → Judgement
    17: 13,  # La Mort → Death
    18: 9,   # Le Capucin → Hermit
    19: 16,  # Le Temple Foudroyé → Tower
    20: 10,  # La Roue de Fortune → Wheel of Fortune
}

# Etteilla cards with NO direct RWS equivalent (Genesis-specific)
ETTEILLA_GENESIS_CARDS = {
    1: "Le Chaos (The Questioner - Male)",
    2: "La Lumière (Light/Enlightenment)",
    3: "Les Plantes (Plants/Growth)",
    4: "Le Ciel (The Heavens)",
    5: "L'Homme et les Quadrupèdes (Man and Quadrupeds)",
    6: "Les Astres (The Celestial Bodies)",
    7: "Les Oiseaux et les Poissons (Birds and Fishes)",
    8: "Repos (Rest)",
    12: "La Prudence (Prudence)",
    21: "Le Despote Africain (African Despot/King)",
}

# Thematic assignments: which RWS major gets which Genesis card as a "bonus" Etteilla note
GENESIS_TO_RWS_THEMATIC = {
    1: 0,    # Chaos → Fool (both = beginnings/void)
    2: 2,    # Light → High Priestess (illumination/hidden knowledge)
    3: 3,    # Plants → Empress (fertility/growth)
    4: 4,    # Heavens → Emperor (cosmic order/structure)
    5: 6,    # Man & Beasts → Lovers (humanity/choice)
    6: 17,   # Celestial Bodies → Star (stars/hope)
    7: 18,   # Birds & Fish → Moon (creatures/intuition)
    8: 21,   # Rest → World (completion/sabbath)
    12: 7,   # Prudence → Chariot (self-mastery/direction)
    21: 19,  # African Despot → Sun (sovereign power/glory)
}

# ─── Build the 78-card spine from RWS ────────────────────────────────────────

# Standard RWS ordering
MAJOR_ARCANA = [
    (0, "The Fool"), (1, "The Magician"), (2, "The High Priestess"),
    (3, "The Empress"), (4, "The Emperor"), (5, "The Hierophant"),
    (6, "The Lovers"), (7, "The Chariot"), (8, "Strength"),
    (9, "The Hermit"), (10, "Wheel of Fortune"), (11, "Justice"),
    (12, "The Hanged Man"), (13, "Death"), (14, "Temperance"),
    (15, "The Devil"), (16, "The Tower"), (17, "The Star"),
    (18, "The Moon"), (19, "The Sun"), (20, "Judgement"),
    (21, "The World"),
]

SUITS = [
    ("wands", "Wands"),
    ("cups", "Cups"),
    ("swords", "Swords"),
    ("pentacles", "Pentacles"),
]

MINOR_NUMBERS = [
    (1, "Ace"), (2, "Two"), (3, "Three"), (4, "Four"), (5, "Five"),
    (6, "Six"), (7, "Seven"), (8, "Eight"), (9, "Nine"), (10, "Ten"),
    (11, "Page"), (12, "Knight"), (13, "Queen"), (14, "King"),
]


def get_image_url(item):
    return item.get("image_url", "")


def get_section_text(item, section_names):
    """Get text from first matching section name."""
    sections = item.get("sections", {})
    for name in section_names:
        if name in sections:
            return sections[name]
    return ""


def build_rws_section(item):
    if not item:
        return ""
    img = get_image_url(item)
    summary = get_section_text(item, ["Summary"])
    interp = get_section_text(item, ["Interpretation"])
    rev = get_section_text(item, ["Reversed"])
    parts = []
    if img:
        parts.append(f"![Rider-Waite-Smith]({img})")
    if summary:
        parts.append(f"**Core meaning:** {summary}")
    if interp:
        parts.append(f"**Upright:** {interp}")
    if rev:
        parts.append(f"**Reversed:** {rev}")
    return "\n\n".join(parts) if parts else "[To be written]"


def build_marseille_section(item):
    if not item:
        return "[No Marseille equivalent]"
    img = get_image_url(item)
    summary = get_section_text(item, ["Summary"])
    interp = get_section_text(item, ["Interpretation"])
    rev = get_section_text(item, ["Reversed"])
    parts = []
    if img:
        parts.append(f"![Tarot de Marseille]({img})")
    if summary:
        parts.append(f"**Symbolic reading:** {summary}")
    if interp:
        parts.append(f"**CBT-informed interpretation:** {interp}")
    if rev:
        parts.append(f"**Reversed:** {rev}")
    return "\n\n".join(parts) if parts else "[To be written]"


def build_sola_busca_section(item):
    if not item:
        return "[No Sola Busca equivalent]"
    img = get_image_url(item)
    name = item.get("name", "")
    etym = get_section_text(item, ["Etymology"])
    hist_fig = get_section_text(item, ["Historical Figure"])
    hist_ctx = get_section_text(item, ["Historical Context"])
    symbolism = get_section_text(item, ["Symbolism"])
    trad = get_section_text(item, ["Traditional Equivalent"])
    interp = get_section_text(item, ["Interpretation"])
    rev = get_section_text(item, ["Reversed"])
    parts = []
    if img:
        parts.append(f"![Sola Busca — {name}]({img})")
    if name:
        parts.append(f"**Card name:** {name}")
    if etym:
        parts.append(f"**Etymology:** {etym}")
    if hist_fig:
        parts.append(f"**Historical figure:** {hist_fig}")
    if hist_ctx:
        parts.append(f"**Historical context:** {hist_ctx}")
    if symbolism:
        parts.append(f"**Symbolism:** {symbolism}")
    if interp:
        parts.append(f"**Interpretation:** {interp}")
    if rev:
        parts.append(f"**Reversed:** {rev}")
    return "\n\n".join(parts) if parts else "[To be written]"


def build_etteilla_section(item_i, item_ii, item_iii, is_genesis=False, genesis_name=""):
    """Build a combined Etteilla section showing all three editions."""
    if not item_i:
        return "[No direct Etteilla equivalent]"

    parts = []

    # Edition I
    img_i = get_image_url(item_i)
    name = item_i.get("name", "")
    french = item_i.get("metadata", {}).get("french_name", "")
    summary = get_section_text(item_i, ["Summary"])
    interp = get_section_text(item_i, ["Interpretation"])
    rev = get_section_text(item_i, ["Reversed"])
    etym = get_section_text(item_i, ["Etymology"])
    hermetic = get_section_text(item_i, ["Hermetic Correspondence"])
    genesis = get_section_text(item_i, ["Genesis Connection"])

    if is_genesis:
        parts.append(f"*In Etteilla's Genesis-based ordering, this position corresponds to {genesis_name or name} — a card unique to the Etteilla tradition with no direct RWS equivalent.*")
        parts.append("")

    parts.append("**EDITION I — Grand Etteilla (1788, Basan engravings)**")
    if img_i:
        parts.append(f"![Etteilla I — {name}]({img_i})")
    if french and french != name:
        parts.append(f"**French name:** {french}")
    if summary:
        parts.append(f"**Meaning:** {summary}")
    if rev:
        parts.append(f"**Reversed:** {rev}")
    if hermetic:
        parts.append(f"**Hermetic correspondence:** {hermetic}")
    if genesis:
        parts.append(f"**Genesis connection:** {genesis}")

    # Edition II — note changes
    if item_ii:
        img_ii = get_image_url(item_ii)
        parts.append("")
        parts.append("**EDITION II — Orsini/Blocquel (1838, letterpress engravings)**")
        if img_ii:
            parts.append(f"![Etteilla II]({img_ii})")
        parts.append("*Changes from Edition I: Basan's original engravings replaced with letterpress reproductions. Lower panels redesigned with recycled imagery. Margin titles added to all cards. Published 47 years after Etteilla's death under the pseudonym 'Julia Orsini.'*")

    # Edition III — note changes
    if item_iii:
        img_iii = get_image_url(item_iii)
        parts.append("")
        parts.append("**EDITION III — Oracle des Dames (1865, Regamey chromolithographs)**")
        if img_iii:
            parts.append(f"![Etteilla III]({img_iii})")
        parts.append("*Changes from Editions I/II: First colored Etteilla deck. Vibrant chromolithography by G. Regamey for Haugard-Mauge. Marketed as 'Oracle des Dames' (Ladies' Oracle) for middle-class parlor entertainment. Preserves Genesis ordering and Hermetic symbolism in a more visually polished format.*")

    return "\n\n".join(parts) if parts else "[To be written]"


def build_tarocchino_section(item):
    if not item:
        return "[No Tarocchino equivalent — the Bolognese deck omits pip cards 2–5 from each suit]"
    img = get_image_url(item)
    name = item.get("name", "")
    summary = get_section_text(item, ["Summary"])
    interp = get_section_text(item, ["Interpretation"])
    rev = get_section_text(item, ["Reversed"])
    parts = []
    if img:
        parts.append(f"![Tarocchino — {name}]({img})")
    if name:
        parts.append(f"**Bolognese name:** {name}")
    if summary:
        parts.append(f"**Commedia dell'Arte reading:** {summary}")
    if interp:
        parts.append(f"**Interpretation:** {interp}")
    if rev:
        parts.append(f"**Reversed:** {rev}")
    return "\n\n".join(parts) if parts else "[To be written]"


def find_etteilla_for_rws_major(rws_number):
    """Find the Etteilla card(s) that correspond to a given RWS major number."""
    # First check direct mapping
    ett_numbers = [ett_num for ett_num, rws_num in ETTEILLA_TO_RWS_MAJOR.items() if rws_num == rws_number]
    # Also check genesis thematic assignments
    genesis_numbers = [ett_num for ett_num, rws_num in GENESIS_TO_RWS_THEMATIC.items() if rws_num == rws_number]

    results = {
        "direct": None, "direct_i": None, "direct_ii": None, "direct_iii": None,
        "genesis": None, "genesis_i": None, "genesis_ii": None, "genesis_iii": None,
        "genesis_name": "",
    }

    if ett_numbers:
        ett_num = ett_numbers[0]
        key = ("major", ett_num, None)
        results["direct_i"] = ett1_idx.get(key)
        results["direct_ii"] = ett2_idx.get(key)
        results["direct_iii"] = ett3_idx.get(key)

    if genesis_numbers:
        gen_num = genesis_numbers[0]
        key = ("major", gen_num, None)
        results["genesis_i"] = ett1_idx.get(key)
        results["genesis_ii"] = ett2_idx.get(key)
        results["genesis_iii"] = ett3_idx.get(key)
        results["genesis_name"] = ETTEILLA_GENESIS_CARDS.get(gen_num, "")

    return results


# ─── Build items ──────────────────────────────────────────────────────────────

items = []
sort_order = 0

# Major Arcana
for number, name in MAJOR_ARCANA:
    card_id = name.lower().replace(" ", "-").replace("'", "")

    # Find in each deck
    rws_key = ("major", number, None)
    rws_card = rws_idx.get(rws_key)
    mars_card = mars_idx.get(rws_key)
    sb_card = sb_idx.get(rws_key)

    # Tarocchino — no Fool in standard position, it's at 61
    if number == 0:
        taro_card = taro_idx.get(("major", 61, None))
    else:
        # Tarocchino numbers start at 0=Magician, offset by 1 from RWS
        taro_card = taro_idx.get(("major", number - 1, None))

    # Etteilla mapping
    ett_info = find_etteilla_for_rws_major(number)

    # Build sections
    sections = {
        "Archetype": "[To be written — universal, deck-agnostic interpretation]",
        "Professional": "[To be written — the card in context of work, career, creative projects]",
        "Relationship": "[To be written — the card in context of love, family, partnership]",
        "Consciousness": "[To be written — the card in context of inner life, meditation, spiritual growth]",
        "Shadow": "[To be written — what the card warns against, reversed/blocked energy]",
        "Rider-Waite-Smith (1909)": build_rws_section(rws_card),
        "Tarot de Marseille (1760)": build_marseille_section(mars_card),
        "Sola Busca (1491)": build_sola_busca_section(sb_card),
    }

    # Etteilla section — combine direct mapping and genesis card if both exist
    if ett_info["direct_i"]:
        sections["Etteilla (1788–1865)"] = build_etteilla_section(
            ett_info["direct_i"], ett_info["direct_ii"], ett_info["direct_iii"]
        )
        if ett_info["genesis_i"]:
            sections["Etteilla Genesis Tradition"] = build_etteilla_section(
                ett_info["genesis_i"], ett_info["genesis_ii"], ett_info["genesis_iii"],
                is_genesis=True, genesis_name=ett_info["genesis_name"]
            )
    elif ett_info["genesis_i"]:
        sections["Etteilla (1788–1865)"] = build_etteilla_section(
            ett_info["genesis_i"], ett_info["genesis_ii"], ett_info["genesis_iii"],
            is_genesis=True, genesis_name=ett_info["genesis_name"]
        )
    else:
        sections["Etteilla (1788–1865)"] = "[No Etteilla equivalent for this card]"

    sections["Tarocchino Bolognese"] = build_tarocchino_section(taro_card)

    # Primary image from RWS
    image_url = get_image_url(rws_card) if rws_card else ""

    item = {
        "id": card_id,
        "name": name,
        "sort_order": sort_order,
        "category": "major-arcana",
        "level": 1,
        "sections": sections,
        "keywords": rws_card.get("keywords", []) if rws_card else [],
        "metadata": {
            "arcana": "major",
            "number": number,
            "suit": None,
            "rws_image": get_image_url(rws_card) if rws_card else "",
            "marseille_image": get_image_url(mars_card) if mars_card else "",
            "sola_busca_image": get_image_url(sb_card) if sb_card else "",
            "sola_busca_name": sb_card.get("name", "") if sb_card else "",
            "tarocchino_name": taro_card.get("name", "") if taro_card else "",
        },
    }
    if image_url:
        item["image_url"] = image_url

    items.append(item)
    sort_order += 1

# Minor Arcana
for suit_key, suit_display in SUITS:
    for number, rank_name in MINOR_NUMBERS:
        card_name = f"{rank_name} of {suit_display}"
        card_id = f"{rank_name.lower()}-of-{suit_display.lower()}"

        # RWS uses "pentacles", others use "coins"
        rws_card = rws_idx.get(("minor", number, suit_key))
        # Marseille uses same suit key after normalization
        mars_card = mars_idx.get(("minor", number, suit_key if suit_key != "pentacles" else "coins"))
        if not mars_card:
            mars_card = mars_idx.get(("minor", number, suit_key))
        # Sola Busca
        sb_card = sb_idx.get(("minor", number, suit_key if suit_key != "pentacles" else "coins"))
        if not sb_card:
            sb_card = sb_idx.get(("minor", number, suit_key))
        # Etteilla (all suits normalized to cups/swords/wands/coins)
        ett_suit = suit_key if suit_key != "pentacles" else "coins"
        ett1_card = ett1_idx.get(("minor", number, ett_suit))
        ett2_card = ett2_idx.get(("minor", number, ett_suit))
        ett3_card = ett3_idx.get(("minor", number, ett_suit))
        # Tarocchino (missing pip 2-5)
        taro_card = taro_idx.get(("minor", number, suit_key if suit_key != "pentacles" else "coins"))
        if not taro_card:
            taro_card = taro_idx.get(("minor", number, suit_key))

        sections = {
            "Archetype": "[To be written]",
            "Professional": "[To be written]",
            "Relationship": "[To be written]",
            "Consciousness": "[To be written]",
            "Shadow": "[To be written]",
            "Rider-Waite-Smith (1909)": build_rws_section(rws_card),
            "Tarot de Marseille (1760)": build_marseille_section(mars_card),
            "Sola Busca (1491)": build_sola_busca_section(sb_card),
            "Etteilla (1788–1865)": build_etteilla_section(ett1_card, ett2_card, ett3_card),
            "Tarocchino Bolognese": build_tarocchino_section(taro_card),
        }

        image_url = get_image_url(rws_card) if rws_card else ""

        item = {
            "id": card_id,
            "name": card_name,
            "sort_order": sort_order,
            "category": f"minor-arcana-{suit_display.lower()}",
            "level": 1,
            "sections": sections,
            "keywords": rws_card.get("keywords", []) if rws_card else [],
            "metadata": {
                "arcana": "minor",
                "number": number,
                "suit": suit_display.lower(),
                "rank": rank_name.lower(),
            },
        }
        if image_url:
            item["image_url"] = image_url

        items.append(item)
        sort_order += 1


# ─── Assemble grammar ────────────────────────────────────────────────────────

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {
                "name": "Pamela Colman Smith & Arthur Edward Waite",
                "date": "1909",
                "note": "Rider-Waite-Smith Tarot — the most influential modern tarot deck",
            },
            {
                "name": "Nicolas Conver",
                "date": "1760",
                "note": "Tarot de Marseille — the oldest widely-reproduced tarot tradition",
            },
            {
                "name": "Unknown (Ferrara workshop)",
                "date": "c. 1491",
                "note": "Sola Busca Tarot — the earliest complete 78-card illustrated deck, now in Pinacoteca di Brera",
            },
            {
                "name": "Jean-Baptiste Alliette (Etteilla)",
                "date": "1788–1791",
                "note": "Grand Etteilla I — the first purpose-built cartomancy deck, with Basan engravings",
            },
            {
                "name": "Simon-François Blocquel (as 'Julia Orsini')",
                "date": "1838",
                "note": "Grand Etteilla II — letterpress edition with redesigned panels",
            },
            {
                "name": "G. Regamey / Haugard-Mauge",
                "date": "1865",
                "note": "Grand Etteilla III (Oracle des Dames) — first chromolithograph Etteilla edition",
            },
            {
                "name": "Yve Lepkowski",
                "date": "2022",
                "note": "Tarocchino Arlecchino — Bolognese tarot in the Commedia dell'Arte tradition",
            },
            {
                "name": "PlayfulProcess",
                "date": "2026",
                "note": "Grammar architecture — unifying five centuries of tarot into a single prismatic reading system",
            },
        ],
    },
    "name": "The Tarot of All Tarots — Five Centuries of the Cards",
    "description": "A meta-tarot holding five public domain decks in dialogue across 78 cards. Each card is a prism: the same archetype seen through the Rider-Waite-Smith (1909), Tarot de Marseille (1760), Sola Busca (1491), three editions of Etteilla (1788/1838/1865), and the Bolognese Tarocchino. Every card includes contextual readings for professional, relationship, and consciousness questions, plus a shadow reading.\n\nThe deck images render inline — you see Colman Smith's golden Fool beside Conver's woodcut Le Mat beside the Sola Busca's wild-haired Mato, each carrying the same archetype through different centuries and sensibilities. The three Etteilla editions show how a single deck evolved across 77 years: from Basan's austere engravings (1788) through Blocquel's recycled letterpress (1838) to Regamey's vibrant chromolithographs (1865).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Pamela Colman Smith's original 1909 RWS illustrations (Wikimedia Commons), Nicolas Conver's 1760 Marseille woodcuts (Gallica/BnF via Wikimedia), Sola Busca engravings c. 1491 (Pinacoteca di Brera via Wikimedia), Etteilla I Basan engravings 1788 (Benebell Wen reconstruction), Etteilla II Blocquel letterpress 1838, Etteilla III Regamey chromolithographs 1865, Tarocchino Arlecchino by Yve Lepkowski 2022.",
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "tags": [
        "tarot",
        "meta-tarot",
        "comparative",
        "RWS",
        "marseille",
        "sola-busca",
        "etteilla",
        "tarocchino",
        "divination",
        "cartomancy",
        "hermetic",
        "major-arcana",
        "minor-arcana",
    ],
    "roots": ["mysticism", "western-esoteric"],
    "shelves": ["wisdom", "mirror"],
    "lineages": ["Shrei"],
    "worldview": "non-dual",
    "items": items,
}

# ─── Write output ─────────────────────────────────────────────────────────────

output_dir = os.path.join(BASE, "grammars", "tarot-of-all-tarots")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "grammar.json")

with open(output_path, "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

# Stats
majors = [i for i in items if i["category"] == "major-arcana"]
minors = [i for i in items if i["category"].startswith("minor-arcana")]
print(f"Generated {len(items)} cards ({len(majors)} major, {len(minors)} minor)")
print(f"Output: {output_path}")
print(f"File size: {os.path.getsize(output_path) / 1024:.0f} KB")

# Check mapping coverage
filled = 0
stubs = 0
for item in items:
    for section_name, text in item["sections"].items():
        if "[To be written" in text or "[No " in text:
            stubs += 1
        else:
            filled += 1
print(f"Sections: {filled} filled from schemas, {stubs} stubs to write")
