# -*- coding: utf-8 -*-
"""Generate grammars/tarocchino-bologna/grammar.json.

The REAL Tarocchino di Bologna — the 62-card Bolognese game deck (Dummett's
A-order), as distinct from the library's modern Marseille-named "Tarocchino
Arlecchino" homage. Structure-accurate; built from documented Bolognese composition
and trump order.

Distinctive features it exists to document:
  * 62 cards: the pips 2,3,4,5 are removed (Ace, 6–10, + four courts per suit).
  * The FOUR PAPI ("Quattro Mori") — four equal, interchangeable cards that replace
    the Popess, Empress, Emperor and Pope of standard tarot.
  * The ANGEL (Judgement) is the HIGHEST trump — above even the World.
  * The three virtues (Temperance, Justice, Strength) sit clustered in the middle.

IMAGE NOTE: no clean per-card public-domain scan of a Bolognese deck exists on
Commons (the BnF albums btv1b105138709 / btv1b105088141 are 100+ UNLABELLED
sequential scans; identifying each card needs vision). So this ships structure-first
with the composite deck sheet as cover; per-card images are a vision-mapping TODO.
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "tarocchino-bologna")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"
COVER = COMMONS + urllib.parse.quote("Tarocco Bolognese.png") + "?width=900"

NOTE = (
    "The Tarocchino was made to play a fast Bolognese trick-taking game, not for "
    "divination. The notes here are historical and structural; any reading is a later "
    "overlay, not part of the deck's original use."
)

# Trumps, LOW to HIGH in the Bolognese order. (slug, name, italian, iconography, note)
TRUMPS = [
    ("matto", "The Fool", "Il Matto",
     "A ragged fool — unnumbered, the 'Excuse' of the game, exempt from following suit.",
     "Stands outside the ranking, like the Fool everywhere."),
    ("bagatto", "The Magician", "Il Bagattino",
     "A craftsman at his table — the lowest of the trumps proper.",
     "The base of the trump ladder; the everyman who opens the parade."),
    ("papa-a", "Papa (Moor) I", "Papa / Moro",
     "One of four near-identical crowned/turbaned figures.",
     "THE FOUR PAPI are the signature of the Bolognese deck: four equal, interchangeable cards that replace the Popess, Empress, Emperor and Pope. They rank only among themselves, by order of play."),
    ("papa-b", "Papa (Moor) II", "Papa / Moro",
     "The second of the four equal Papi.", "One of the four interchangeable Papi (see Papa I)."),
    ("papa-c", "Papa (Moor) III", "Papa / Moro",
     "The third of the four equal Papi.", "One of the four interchangeable Papi (see Papa I)."),
    ("papa-d", "Papa (Moor) IV", "Papa / Moro",
     "The fourth of the four equal Papi.", "One of the four interchangeable Papi (see Papa I)."),
    ("amore", "Love", "L'Amore",
     "A couple beneath a winged Cupid.", "Union and choice, just above the Papi."),
    ("carro", "The Chariot", "Il Carro",
     "A victor in a triumphal car.", "Triumph; opens the central virtue cluster."),
    ("temperanza", "Temperance", "La Temperanza",
     "A figure pouring between two vessels.", "First of the three virtues, grouped together in the Bolognese order."),
    ("giustizia", "Justice", "La Giustizia",
     "An enthroned woman with sword and scales.", "The middle virtue of the central cluster."),
    ("forza", "Strength", "La Forza",
     "A figure mastering a lion or column.", "The third clustered virtue."),
    ("ruota", "Wheel of Fortune", "La Ruota",
     "A turning wheel with rising and falling figures.", "Fortune's turn, above the virtues."),
    ("vecchio", "The Old Man (Time)", "Il Vecchio",
     "A bent old man with an hourglass — Time, the Bolognese 'Hermit'.", "Time and age."),
    ("traditore", "The Traitor (Hanged Man)", "Il Traditore",
     "A youth hung by one foot — the shaming image of a traitor.", "Suspension and disgrace."),
    ("morte", "Death", "La Morte",
     "A skeletal reaper among the fallen.", "The great leveller."),
    ("diavolo", "The Devil", "Il Diavolo",
     "A horned figure over bound captives.", "Bondage and appetite."),
    ("torre", "The Lightning (Tower)", "La Saetta / La Torre",
     "A tower struck by a bolt — called 'La Saetta' (the lightning) in Bologna.", "Sudden ruin."),
    ("stella", "The Star", "La Stella",
     "A figure beneath a great star.", "First of the three heavenly lights."),
    ("luna", "The Moon", "La Luna",
     "The Moon over the night world.", "The second light."),
    ("sole", "The Sun", "Il Sole",
     "A radiant sun over the day world.", "The third light."),
    ("mondo", "The World", "Il Mondo",
     "A figure within a cosmic frame.", "Near the summit — but NOT the highest in Bologna."),
    ("angelo", "The Angel (Judgement)", "L'Angelo",
     "Angels with trumpets; the dead rise.", "The HIGHEST trump of the Bolognese deck — uniquely placed ABOVE the World."),
]

SUITS = [("coins", "Coins", "Denari", "Earth"), ("cups", "Cups", "Coppe", "Water"),
         ("swords", "Swords", "Spade", "Air"), ("batons", "Batons", "Bastoni", "Fire")]
# Bolognese minors: Ace, 6,7,8,9,10 + Fante, Cavallo, Regina, Re (pips 2-5 removed)
RANKS = [("ace", "Ace", 1), ("six", "Six", 6), ("seven", "Seven", 7), ("eight", "Eight", 8),
         ("nine", "Nine", 9), ("ten", "Ten", 10),
         ("fante", "Knave (Fante)", None), ("cavallo", "Knight (Cavallo)", None),
         ("regina", "Queen (Regina)", None), ("re", "King (Re)", None)]

items = []
so = 0
for slug, name, ital, icon, note in TRUMPS:
    items.append({
        "id": f"trump-{slug}", "name": name, "sort_order": so,
        "category": "trump", "level": 1,
        "keywords": [name.lower().replace("the ", ""), ital.lower(), "bolognese", "tarocchino", "trionfi"],
        "metadata": {"arcana": "trump", "italian_name": ital, "tradition": "bolognese"},
        "sections": {"Iconography": icon, "In the Bolognese deck": note, "Tradition Note": NOTE},
    })
    so += 1

for sid, sdisp, sital, element in SUITS:
    for rslug, rname, pip in RANKS:
        is_court = pip is None
        items.append({
            "id": f"{sid}-{rslug}", "name": f"{rname} of {sdisp}", "sort_order": so,
            "category": f"suit-{sid}", "level": 1,
            "keywords": [sdisp.lower(), element.lower(), rslug, sital.lower(),
                         "court" if is_court else "pip"],
            "metadata": {"arcana": "minor", "suit": sdisp, "suit_italian": sital, "element": element,
                         "rank": rname, "court": is_court},
            "sections": {
                "Iconography": (f"{rname} of {sdisp} ({sital}). " + ("A courtly figure of the suit." if is_court
                                else f"The suit-emblems of {sdisp.lower()} in the Bolognese pattern.")),
                "In the Bolognese deck": ("The Bolognese keeps the full four-card court (King, Queen, Knight, "
                                          "Knave)." if is_court else
                                          "The Tarocchino REMOVES the pips 2–5 — only the Ace and 6–10 remain, "
                                          "the cut that makes it a 62-card deck."),
                "Tradition Note": NOTE,
            },
        })
        so += 1

# Emergences
all_ids = {it["id"] for it in items}
papi_ids = [it["id"] for it in items if it["id"].startswith("trump-papa")]
trump_ids = [it["id"] for it in items if it["category"] == "trump"]
emgs = [
    ("emg-papi", "The Four Papi — the Bolognese Signature", papi_ids,
     {"About these cards": "The single most distinctive feature of the Bolognese deck: four equal, "
      "interchangeable 'Papi' (also called the four Moors) replace the Popess, Empress, Emperor and Pope. "
      "They have no fixed order among themselves — whichever is played first outranks the others on that "
      "trick. The heretical Popess simply vanishes.",
      "Why it matters": "This is exactly what a modern Marseille-named 'Tarocchino' deck gets wrong. The "
      "Papi are the test of whether a deck is really Bolognese."}),
    ("emg-trumps", "The Trumps in the Bolognese Order", trump_ids,
     {"About this order": "The Bolognese trump order differs from the Marseille: the three virtues "
      "(Temperance, Justice, Strength) sit clustered in the middle, and — uniquely — the ANGEL (Judgement) "
      "is the HIGHEST trump, ranked ABOVE the World. The deck is one of Dummett's A-order traditions.",
      "How to use": "Read the trumps from the Bagattino up to the Angel to see a trump sequence that the "
      "printed Marseille never standardised."}),
]
for sid, sdisp, sital, element in SUITS:
    kids = [it["id"] for it in items if it["category"] == f"suit-{sid}"]
    emgs.append((f"emg-suit-{sid}", f"Suit of {sdisp} ({sital}) — pips 2–5 removed", kids,
                 {"About this suit": f"The {sdisp} ({sital}) of the Tarocchino: Ace and 6–10 only, plus the "
                  f"four courts — the Bolognese 'stripping' of the low pips that gives the 62-card deck."}))
for eid, ename, kids, sections in emgs:
    kids = [k for k in kids if k in all_ids]
    items.append({"id": eid, "name": ename, "sort_order": so, "category": "emergence", "level": 2,
                  "composite_of": kids, "relationship_type": "emergence",
                  "image_url": COVER, "metadata": {}, "sections": sections})
    so += 1

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Bolognese card-making tradition", "date": "16th c. onward",
             "note": "The Tarocchino di Bologna game deck (62 cards)"},
            {"name": "Michael Dummett", "date": "1980",
             "note": "A-order classification; Bolognese composition and trump order"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "Composite deck sheet (Tarocco Bolognese.png); per-card scans are a TODO"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar architecture and summaries"},
        ],
    },
    "name": "Tarocchino di Bologna — The Real 62-Card Bolognese Deck",
    "description": (
        "The genuine Tarocchino di Bologna — the fast 62-card Bolognese game deck (one of Michael Dummett's "
        "A-order traditions), built structure-accurate to distinguish it from modern Marseille-named "
        "'Tarocchino' homages. Three things define it: the pips 2–5 are removed (leaving Ace, 6–10, and four "
        "courts per suit); the four equal, interchangeable PAPI (the 'Quattro Mori') replace the Popess, "
        "Empress, Emperor and Pope; and the ANGEL (Judgement) is the highest trump of all, ranked above even "
        "the World.\n\n"
        "It was made to play a brisk trick-taking game, not for divination — flagged on every card. Each "
        "trump carries an Iconography note and a 'In the Bolognese deck' note explaining its distinctive "
        "placement; the minors document the 2–5 stripping; emergences gather the Four Papi and the Bolognese "
        "trump order.\n\n"
        "IMAGE NOTE: no clean per-card public-domain scan of a Bolognese deck is available on Wikimedia "
        "Commons (the BnF albums are 100+ unlabelled sequential scans needing vision to identify). This "
        "grammar therefore ships structure-first, with the composite deck sheet as cover; per-card imaging "
        "(e.g. from the Mitelli 1664 Tarocchino or the BnF albums) is a documented follow-up.\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: composite Tarocco Bolognese sheet (Wikimedia Commons); BnF "
        "Gallica albums 'Tarocchino de Bologne' (btv1b105138709) and 'à deux têtes' (btv1b105088141); the "
        "Giuseppe Maria Mitelli etched Tarocchino, 1664."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": COVER,
    "tags": ["tarot", "tarocchino", "bologna", "bolognese", "a-order", "62-cards",
             "history", "trionfi", "four-papi"],
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
nt = sum(1 for it in items if it["category"] == "trump")
nm = sum(1 for it in items if str(it["category"]).startswith("suit-"))
print(f"Wrote tarocchino-bologna/grammar.json — {len(items)} items (trumps {nt}, minors {nm})")
