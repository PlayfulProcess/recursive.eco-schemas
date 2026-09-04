# -*- coding: utf-8 -*-
"""Generate grammars/charles-vi-tarot/grammar.json.

The so-called "Charles VI" tarot (a.k.a. the Gringonneur deck) — a hand-painted,
gold-ground deck of which 17 cards survive at the Bibliothèque nationale de France.
Built from the surviving cards only. A documentary cornerstone of the EASTERN
(Ferrarese, Dummett B-order) tradition.

Setting the record straight: despite the name it is NOT the deck Charles VI of
France paid Jacquemin Gringonneur for in 1392. It is a North-Italian (probably
Ferrarese or Bolognese) deck of c. 1450–1480; the royal attribution is an
18th–19th-century misidentification.

Images: Wikimedia Commons, Category:Le tarot dit de Charles VI (public domain).
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "charles-vi-tarot")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"


def img(fn):
    return COMMONS + urllib.parse.quote(fn)


TRADITION_NOTE = (
    "These cards were made to play a game — the Italian *trionfi* / *tarocchi* card "
    "game — not for divination, which arrived centuries later. The notes here are "
    "historical and iconographic; any reading is a modern interpretive overlay."
)

# (num, slug, name, italian, filename, iconography, history, reading)
CARDS = [
    (0, "fool", "The Fool", "Il Matto", "Fool tarot charles6.jpg",
     "A bearded man in belled motley with a club, children or dogs about his legs — the licensed fool.",
     "Survives at the BnF. Unnumbered, outside the trump sequence.",
     "Folly and freedom, the figure who stands apart from the order of estates."),
    (4, "emperor", "The Emperor", "L'Imperatore", "Empereur tarot charles6.jpg",
     "A crowned, bearded emperor enthroned with orb and sceptre, attendants below.",
     "One of the 17 survivors. Temporal majesty rendered in gold leaf.",
     "Worldly authority, the throne, the order of empire."),
    (5, "pope", "The Pope", "Il Papa", "Pope tarot charles6.jpg",
     "A tiara'd pope enthroned, hand raised in blessing, cardinals at his feet.",
     "Survives at the BnF. The spiritual power answering the Emperor.",
     "Spiritual authority, blessing, the sanctioned hierophant."),
    (6, "lovers", "The Lovers", "L'Amore", "L'Amoureux tarot charles6.jpg",
     "A couple beneath a winged Cupid who draws his bow — a courtly betrothal scene.",
     "One of the survivors; a richly dressed dynastic-marriage image.",
     "Union, love, the binding of two houses."),
    (7, "chariot", "The Chariot", "Il Carro", "Chariot tarot charles6.jpg",
     "A crowned lady stands in a triumphal car drawn by two horses.",
     "Survives at the BnF — the 'triumph' that names the game.",
     "Victory, the self carried forward in triumph."),
    (8, "justice", "Justice", "La Giustizia", "Justice tarot charles6.jpg",
     "An enthroned woman with raised sword and balance.",
     "A surviving cardinal virtue. In the B-order the virtues sit at particular ranks.",
     "Balance, judgment, the weighing of each act."),
    (9, "hermit", "The Hermit (Time)", "Il Tempo", "Hermit tarot charles6.jpg",
     "An old bearded man with a staff and an hourglass — Time, the Old Man.",
     "Survives at the BnF; the hourglass (not a lantern) marks him as 'Il Tempo'.",
     "Time, age, the solitary measure of hours."),
    (11, "strength", "Strength", "La Forza", "Force tarot charles6.jpg",
     "A woman calmly breaks a stone column (a Samson/Fortitude image), or masters a beast.",
     "A surviving cardinal virtue.",
     "Fortitude, courage, strength of soul over force."),
    (12, "hanged-man", "The Hanged Man", "L'Appeso", "Pendu tarot charles6.jpg",
     "A youth suspended by one ankle from a frame, the shaming 'pittura infamante' of a traitor.",
     "Survives at the BnF.",
     "Suspension, reversal, the punished betrayer; the world seen upside-down."),
    (13, "death", "Death", "La Morte", "Death tarot charles6.jpeg",
     "A skeletal figure on a horse rides over fallen kings and commoners.",
     "A survivor — the mounted Death of the danse macabre.",
     "The great leveller, transformation, the end that spares no estate."),
    (14, "temperance", "Temperance", "La Temperanza", "Temperance tarot charles6.jpeg",
     "A winged woman pours liquid between two vessels.",
     "A surviving cardinal virtue.",
     "Tempering, moderation, the patient blending of waters."),
    (16, "tower", "The Tower (House of the Devil)", "La Casa del Diavolo", "Maison-Dieu tarot charles6.jpg",
     "Figures fall from a burning structure — the 'House of the Devil' / God, the early Tower.",
     "A rare survival of the Tower from a 15th-century deck.",
     "Sudden ruin, the breaking of false structures."),
    (18, "moon", "The Moon", "La Luna", "Moon tarot charles6.jpg",
     "Two astronomers with compasses measure beneath a crescent moon.",
     "Survives at the BnF; an unusual 'astronomers' Moon, not the later dogs-and-crayfish scene.",
     "Reflection, the measured night, the sciences of the heavens."),
    (19, "sun", "The Sun", "Il Sole", "Sun tarot charles6.jpg",
     "A woman with a distaff sits beneath a great rayed sun.",
     "A survivor; the spinning woman under the sun is unique to this deck.",
     "Daylight, vitality, the lit and ordinary world."),
    (20, "judgement", "Judgement", "Il Giudizio", "Jugement tarot charles6.jpg",
     "An angel sounds a trumpet; the dead rise from their tombs.",
     "Survives at the BnF.",
     "The call and the reckoning, awakening, the dead risen to answer."),
    (21, "world", "The World", "Il Mondo", "World tarot charles6.jpeg",
     "A standing figure (Fame, or a woman) holds a globe showing a walled city over water.",
     "A survivor — the highest triumph, here a panorama of the world.",
     "Completion, the cosmos surveyed, the journey closed."),
    (None, "page-swords", "Page of Swords", "Fante di Spade", "Valet d'epees tarot charles6.jpg",
     "A young courtier holds an upright sword — the one surviving suit card of the deck.",
     "The sole surviving MINOR card, showing the deck's suit cards were as richly painted as the trumps.",
     "The student of the sword-suit: vigilance, a sharp message, the mind learning."),
]

items = []
so = 0
for num, slug, name, ital, fn, icon, hist, reading in CARDS:
    u = img(fn)
    is_court = slug == "page-swords"
    items.append({
        "id": f"card-{slug}", "name": (name if num is None else f"{num} — {name}"), "sort_order": so,
        "category": ("court" if is_court else "trump"), "level": 1,
        "keywords": [name.lower(), ital.lower(), "charles-vi", "trionfi", "ferrara"],
        "image_url": u,
        "metadata": {"arcana": ("minor" if is_court else "trump"),
                     "trump_number": num, "italian_name": ital, "status": "surviving",
                     "museum": "Bibliothèque nationale de France",
                     "illustrations": [{"url": u, "artist": "North Italian (Ferrarese?) workshop",
                                        "artist_dates": "c. 1450–1480",
                                        "edition": "The 'Charles VI' (Gringonneur) Tarot, c. 1450–80",
                                        "scene": name, "license": "Public Domain", "is_primary": True}]},
        "sections": {"Iconography": icon, "History": hist, "Reading": reading, "Tradition Note": TRADITION_NOTE},
    })
    so += 1

# L2 emergence
trump_ids = [it["id"] for it in items if it["category"] == "trump"]
items.append({
    "id": "emg-surviving-trumps", "name": "The 16 Surviving Trumps", "sort_order": so,
    "category": "emergence", "level": 2, "composite_of": trump_ids, "relationship_type": "emergence",
    "image_url": img("Death tarot charles6.jpeg"),
    "metadata": {},
    "sections": {
        "About these Cards": "Sixteen trumps and a single suit card survive of this once-complete deck — "
        "missing are the Magician, Popess, Empress, Wheel of Fortune, Devil, and Star. What remains is among "
        "the finest gold-ground tarot painting of the 15th century.",
        "Setting the record straight": "The deck is named for a 1392 payment by Charles VI of France to the "
        "painter Gringonneur — but that attribution was disproved long ago. These cards are North Italian "
        "(probably Ferrarese), c. 1450–1480: a cornerstone of the eastern, Dummett B-order tradition, not a "
        "French royal commission."},
})
so += 1

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "North Italian (Ferrarese?) workshop", "date": "c. 1450–1480",
             "note": "Painter of the 'Charles VI' / Gringonneur tarot"},
            {"name": "Bibliothèque nationale de France", "date": "holding institution",
             "note": "Holds the 17 surviving cards (Cabinet des Estampes)"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "Card images, Category:Le tarot dit de Charles VI"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar architecture and summaries"},
        ],
    },
    "name": "The 'Charles VI' Tarot (Gringonneur) — c. 1450–1480",
    "description": (
        "A hand-painted, gold-ground tarot of which 17 cards survive at the Bibliothèque nationale de France "
        "— sixteen trumps and a single Page of Swords. It is one of the most beautiful witnesses to "
        "15th-century tarot, and a cornerstone of the eastern, Ferrarese tradition (Dummett's B-order).\n\n"
        "Despite its famous name, this is NOT the deck Charles VI of France paid Jacquemin Gringonneur for in "
        "1392 — that attribution was disproved long ago. The cards are North Italian, probably Ferrarese, of "
        "about 1450–1480. The grammar keeps the name (it is how the deck is known) while setting the record "
        "straight. Each surviving card carries an Iconography note, a History note, and a light Reading; like "
        "all early tarot it was a GAME deck, flagged on every card.\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: The 'Charles VI' (Gringonneur) Tarot, c. 1450–80, "
        "Bibliothèque nationale de France (Wikimedia Commons, Category:Le tarot dit de Charles VI) — "
        "gold-ground tempera, International Gothic. Note the unusual 'astronomers' Moon and the "
        "distaff-spinner Sun, unique to this deck."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": img("Empereur tarot charles6.jpg"),
    "tags": ["tarot", "charles-vi", "gringonneur", "ferrara", "history", "15th-century",
             "trionfi", "public-domain", "b-order"],
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
print(f"Wrote charles-vi-tarot/grammar.json — {len(items)} items, imaged {sum(1 for it in items if it.get('image_url'))}")
