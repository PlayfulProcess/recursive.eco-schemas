# -*- coding: utf-8 -*-
"""Generate grammars/tarot-de-besancon/grammar.json.

The Tarot de Besançon / Swiss "1JJ" type — a Marseille variant whose defining
feature is a Protestant-era substitution: JUNO replaces the Popess (II) and JUPITER
replaces the Pope (V), removing the two Catholic clergy from the deck. (The "1JJ"
name comes from the two J-cards, Juno and Jupiter.)

This is a PARTIAL, variant-highlights grammar: only the cards available as clean
public-domain scans on Wikimedia Commons (Category:Tarot 1JJ) — the two signature
cards plus a representative selection of trumps and pips. It documents the variant,
not the full 78.

Images: Wikimedia Commons, Category:Tarot 1JJ (public domain).
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "tarot-de-besancon")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"


def img(fn):
    return COMMONS + urllib.parse.quote(fn) + ("?width=600" if fn.lower().endswith(".png") else "")


NOTE = ("The Tarot de Besançon was a GAME deck, not a divination deck; reading-meanings "
        "are a later overlay. It is a regional cousin of the Tarot de Marseille (Dummett C-order).")

# (id, name, number, filename, iconography, variant note)
CARDS = [
    ("junon", "Juno (in place of the Popess)", 2, "Tarot 1JJ - Junon - 1. Version.png",
     "The goddess Juno stands with her peacock — replacing the Marseille's Popess.",
     "THE defining card of the Besançon variant. The scandalous female 'Pope' is swapped for the pagan "
     "goddess Juno — one of the two 'J' cards that give the 1JJ its name. A Protestant-friendly redesign "
     "that removes the Catholic clergy."),
    ("jupiter", "Jupiter (in place of the Pope)", 5, "Tarot 1JJ - Jupiter.png",
     "Jupiter enthroned with his eagle and thunderbolt — replacing the Marseille's Pope.",
     "The second defining card: the Pope becomes the god Jupiter. With Juno, this removes both Church "
     "figures from the deck — the hallmark of the Besançon / Swiss type."),
    ("emperor", "The Emperor (Der Herrscher)", 4, "1JJ Tarot - Trump 04 - German - Der Herrscher.jpg",
     "A crowned, bearded sovereign — labelled in German ('Der Herrscher') in this trilingual Swiss edition.",
     "The Emperor survives the substitution. Swiss 1JJ cards were printed with French, German, and English titles."),
    ("chariot", "The Chariot", 7, "1JJ Tarot - Trump 07 - English - The Chariot.jpg",
     "A crowned prince in a triumphal car.", "Triumph; here titled in English."),
    ("strength", "Strength (La Force)", 11, "1JJ Tarot - Trump 11 - French - La Force.jpg",
     "A woman parting a lion's jaws — Strength at XI, the older Marseille numbering.",
     "Keeps the Marseille order (Strength XI, not the Golden Dawn's VIII)."),
    ("temperance", "Temperance", 14, "1JJ Tarot - Trump 14 - English - Temperance.jpg",
     "A winged figure pouring between two vessels.", "The tempering virtue."),
    ("devil", "The Devil (Der Teufel)", 15, "1JJ Tarot - Trump 15 - German - Der Teufel.jpg",
     "A horned devil over bound figures.", "Bondage and appetite; German title here."),
    ("tower", "The Tower (La Maison de Dieu)", 16, "1JJ Tarot - Trump 16 - French - La Maison de Dieu.jpg",
     "Figures fall from a tower struck by fire — the 'House of God'.", "Sudden ruin."),
    ("world", "The World (Le Monde)", 21, "1JJ Tarot - Trump 21 - French - Le Monde.jpg",
     "A dancing figure in a wreath with the four beasts.", "Completion, the highest numbered trump."),
    ("swords-ace", "Ace of Swords", None, "1JJ Tarot - Swords 01.jpg",
     "A single sword crowned, amid the suit's emblems.", "Root of the sword suit (Air)."),
    ("cups-two", "Two of Cups", None, "1JJ Tarot - Cups 02.jpg",
     "Two cups amid foliate scrollwork.", "Pairing in the cup suit (Water)."),
    ("wands-two", "Two of Batons", None, "1JJ Tarot - Wands 02.jpg",
     "Two crossed batons.", "Pairing in the baton suit (Fire)."),
    ("coins-three", "Three of Coins", None, "1JJ Tarot - Disks 03.jpg",
     "Three coins arranged with decoration.", "Growth in the coin suit (Earth)."),
]

items = []
so = 0
for cid, name, num, fn, icon, note in CARDS:
    u = img(fn)
    is_minor = num is None
    md = {"arcana": ("minor" if is_minor else "trump"), "number": num, "tradition": "besancon-swiss",
          "illustrations": [{"url": u, "artist": "Swiss card-makers (1JJ type)",
                             "artist_dates": "18th–19th c.", "edition": "Tarot de Besançon / Swiss 1JJ",
                             "scene": name, "license": "Public Domain", "is_primary": True}]}
    if is_minor and " of " in name:
        r, s = name.split(" of ", 1)
        md["rank"], md["suit"] = r.strip(), s.strip()
    items.append({
        "id": f"card-{cid}", "name": name, "sort_order": so,
        "category": ("minor" if is_minor else "trump"), "level": 1,
        "keywords": [name.lower(), "besancon", "1jj", "swiss", "marseille-variant"],
        "image_url": u, "metadata": md,
        "sections": {"Iconography": icon, "The Besançon variant": note, "Tradition Note": NOTE},
    })
    so += 1

items.append({
    "id": "emg-juno-jupiter", "name": "Juno & Jupiter — The Besançon Substitution", "sort_order": so,
    "category": "emergence", "level": 2, "composite_of": ["card-junon", "card-jupiter"],
    "relationship_type": "emergence", "image_url": img("Tarot 1JJ - Jupiter.png"),
    "metadata": {},
    "sections": {
        "What changed": "The Tarot de Besançon's one defining move: it replaces the Popess (II) with the "
        "goddess JUNO and the Pope (V) with JUPITER, removing both Catholic clergy from the deck. The two "
        "'J' cards give the 'Swiss 1JJ' its name.",
        "Why": "Made for Protestant and mixed-confessional regions (eastern France, Switzerland, the "
        "Rhineland) where the Popess and Pope were unwelcome, the substitution let the Marseille pattern "
        "travel into Reformed territory. The cards were often printed trilingually (French/German/English)."},
})

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Swiss card-making tradition (1JJ type)", "date": "18th–19th c.",
             "note": "Tarot de Besançon / Swiss 1JJ — Juno & Jupiter variant of the Marseille"},
            {"name": "Wikimedia Commons", "date": "public domain", "note": "Category:Tarot 1JJ"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar architecture and summaries"},
        ],
    },
    "name": "Tarot de Besançon / Swiss 1JJ — The Juno & Jupiter Variant",
    "description": (
        "A regional variant of the Tarot de Marseille (Dummett C-order) defined by one striking change: it "
        "replaces the Popess with the goddess JUNO and the Pope with JUPITER, removing both Catholic clergy "
        "from the deck. The two 'J' cards give the 'Swiss 1JJ' its name. Made for Protestant and "
        "mixed-confessional regions — eastern France around Besançon, Switzerland, the Rhineland — it let the "
        "Marseille pattern travel into Reformed territory, and its cards were often printed trilingually "
        "(French / German / English).\n\n"
        "This is a PARTIAL, variant-highlights grammar: it holds only the cards available as clean "
        "public-domain scans on Wikimedia Commons — the two signature cards (Juno, Jupiter) plus a "
        "representative selection of trumps and pips — to document the variant rather than the full 78. It "
        "was a GAME deck; the Tradition Note is on every card.\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Tarot de Besançon / Swiss 1JJ cards (Wikimedia Commons, "
        "Category:Tarot 1JJ). For a complete deck, the AGMüller / Lo Scarabeo 1JJ facsimiles are the "
        "modern reference (in copyright); period Besançon decks (Renault, Lequart) survive in museum "
        "collections."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": img("Tarot 1JJ - Junon - 1. Version.png"),
    "tags": ["tarot", "besancon", "swiss", "1jj", "juno", "jupiter", "marseille-variant",
             "c-order", "history", "partial"],
    "roots": ["western-esoteric", "renaissance"],
    "shelves": ["wonder", "mirror"],
    "lineages": ["Andreotti"],
    "worldview": "historical",
    "is_published": False,
    "items": items,
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, "grammar.json"), "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)
print(f"Wrote tarot-de-besancon/grammar.json — {len(items)} items, imaged {sum(1 for it in items if it.get('image_url'))}")
