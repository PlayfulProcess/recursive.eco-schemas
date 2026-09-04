# -*- coding: utf-8 -*-
"""Generate grammars/minchiate-florence-tarot/grammar.json.

The Minchiate — the great 97-card Florentine expansion of tarot. To the standard
deck it adds 20 trumps: the four classical elements, the twelve signs of the
zodiac, and the virtues missing from ordinary tarot (Prudence + the three
theological virtues Faith, Hope, Charity, joining the three cardinal virtues so
that ALL SEVEN are present). It drops the Popess and turns the Pope/Emperor group
into five interchangeable "Papi". A complete cosmological game-deck.

Built from the fully-scanned Minchiate of Florence, c. 1860–1890 (Wikimedia
Commons), which images every one of the 97 cards. Historical/iconographic grammar.
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "minchiate-florence-tarot")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"
PREFIX = "Minchiate card deck - Florence - 1860-1890 - "


def img(filename):
    return COMMONS + urllib.parse.quote(filename) if filename else None


TRADITION_NOTE = (
    "These cards were made to play a game — the Italian *trionfi* / *tarocchi* "
    "card game (here the Florentine Minchiate) — not for divination, which arrived "
    "centuries later. The notes here are historical and iconographic; any reading is "
    "a modern interpretive overlay, not part of the deck's original use."
)


# ---- 41 special cards (Fool + 40 trumps). (num, file_name_part, id, name, group, icon, meaning)
# file_name_part is the exact tail after "Trumps - "
TRUMPS = [
    (0, "Il Matto -", "matto", "The Fool", "fool",
     "A ragged madman wanders, sometimes with feathers and a hobby-horse. Unnumbered, he is the wild card outside the count.",
     "Folly and freedom, the spirit outside the order; in play the Fool excuses one from following suit."),
    (1, "01 - Papa uno", "papa-1", "Papa One", "papi",
     "A seated, crowned papal figure. The first of five near-identical 'Papi'.",
     "Minchiate dissolves the Popess, Empress, Emperor, Pope, and Love of ordinary tarot into five ranked 'Papi' (Popes) — the powers of Church and Empire flattened into one interchangeable office."),
    (2, "02 - Papa due", "papa-2", "Papa Two (The Empress)", "papi",
     "A second crowned Papa, traditionally identified with the Empress.",
     "The second of the five Papi, carrying the old Empress. The five rank only against each other in the game."),
    (3, "03 - Papa tre", "papa-3", "Papa Three (The Emperor)", "papi",
     "A third Papa, identified with the Emperor.",
     "The Emperor folded into the Papi sequence — temporal power made one of five equals."),
    (4, "04 - Papa quattro", "papa-4", "Papa Four (The Pope)", "papi",
     "A fourth Papa, the Pope proper.",
     "Spiritual authority, the Pope, ranked fourth among the five Papi."),
    (5, "05 - Papa cinque", "papa-5", "Papa Five (Love)", "papi",
     "A fifth Papa, here carrying the old card of Love — sometimes a couple beneath Cupid.",
     "Love absorbed into the Papi group; the highest of the five."),
    (6, "06 - La Temperanza", "temperanza", "Temperance", "virtue",
     "A woman pours liquid between two vessels.",
     "Temperance — the first of the cardinal virtues. Minchiate is the deck that carries the COMPLETE set of seven virtues."),
    (7, "07 - La Forza", "forza", "Fortitude", "virtue",
     "A woman subdues a lion or breaks a column.",
     "Fortitude — the cardinal virtue of courage and steadfast strength."),
    (8, "08 - La Giustizia", "giustizia", "Justice", "virtue",
     "An enthroned woman with sword and scales.",
     "Justice — the cardinal virtue of measure and right judgment."),
    (9, "09 - La Ruota della Fortuna", "ruota", "Wheel of Fortune", "trump",
     "A wheel turned by Fortune, figures rising and falling.",
     "The turning of fortune, the mutability that lifts and lowers all estates."),
    (10, "10 - Il Carro", "carro", "The Chariot", "trump",
     "A triumphal car bearing a crowned victor.",
     "Triumph and advance — the victory parade that gives the trumps their name."),
    (11, "11 - Il Gobbo", "gobbo", "The Hunchback (Time)", "trump",
     "A bent old man with a stick, sometimes an hourglass — 'Il Gobbo', the Hunchback, the Minchiate name for Time / the Hermit.",
     "Time, age, and solitude; the bent figure measuring his hours."),
    (12, "12 - L'Impiccato", "impiccato", "The Hanged Man", "trump",
     "A youth hung by one foot from a beam.",
     "Suspension, reversal, the traitor's shame; the world seen upside-down."),
    (13, "13 - La Morte", "morte", "Death", "trump",
     "A skeleton with a scythe among the fallen.",
     "Death the leveller, transformation, the end that spares no estate."),
    (14, "14 - Il Diavolo", "diavolo", "The Devil", "trump",
     "A horned, clawed devil over bound figures.",
     "Bondage, appetite, the force of matter that enslaves the unwary."),
    (15, "15 - La Casa del Diavolo", "casa-diavolo", "The House of the Devil (Tower)", "trump",
     "A tower struck and burning, figures falling — 'the House of the Devil', the Minchiate Tower.",
     "Sudden ruin, the breaking of false structures, catastrophe as release."),
    (16, "16 - La Speranza", "speranza", "Hope", "virtue",
     "A woman with an anchor gazes upward in prayer.",
     "Hope — a theological virtue. With Faith and Charity it gives Minchiate the three theological virtues ordinary tarot lacks."),
    (17, "17 - La Prudenza", "prudenza", "Prudence", "virtue",
     "A woman with a mirror and serpent, contemplating herself.",
     "Prudence — the fourth cardinal virtue, missing from standard tarot and restored here, completing the cardinal set."),
    (18, "18 - La Fede", "fede", "Faith", "virtue",
     "A woman with cross and chalice.",
     "Faith — the theological virtue of trust beyond proof."),
    (19, "19 - La Carità", "carita", "Charity", "virtue",
     "A woman nursing children, the image of Caritas.",
     "Charity — the theological virtue of self-giving love, named the greatest of the three."),
    (20, "20 - Il Fuoco", "fuoco", "Fire", "element",
     "A salamander in flames, or a burning scene — the element Fire.",
     "Fire — will, transformation, the active spark. The first of the four classical elements unique to Minchiate among early decks."),
    (21, "21 - L'Acqua", "acqua", "Water", "element",
     "A figure by water, ships or fish — the element Water.",
     "Water — feeling, flux, the depths; the passive, receptive element."),
    (22, "22 - La Terra", "terra", "Earth", "element",
     "A landscape, a globe, or a figure on the land — the element Earth.",
     "Earth — body, matter, the solid ground of the material world."),
    (23, "23 - L'Aria", "aria", "Air", "element",
     "Birds, clouds, or a figure with the winds — the element Air.",
     "Air — mind, breath, the medium of exchange and thought."),
    # 12 zodiac (Minchiate's own order)
    (24, "24 - La Bilancia", "bilancia", "Libra", "zodiac",
     "The scales of Libra.", "Libra — cardinal Air, ruled by Venus: balance, justice, partnership."),
    (25, "25 - La Vergine", "vergine", "Virgo", "zodiac",
     "The maiden of Virgo.", "Virgo — mutable Earth, ruled by Mercury: discernment, service, the careful eye."),
    (26, "26 - Il Scorpione", "scorpione", "Scorpio", "zodiac",
     "The scorpion of Scorpio.", "Scorpio — fixed Water, ruled by Mars: depth, intensity, transformation."),
    (27, "27 - L'Ariete", "ariete", "Aries", "zodiac",
     "The ram of Aries.", "Aries — cardinal Fire, ruled by Mars: initiative, courage, the first spark."),
    (28, "28 - Il Capricorno", "capricorno", "Capricorn", "zodiac",
     "The sea-goat of Capricorn.", "Capricorn — cardinal Earth, ruled by Saturn: ambition, structure, endurance."),
    (29, "29 - Il Sagittario", "sagittario", "Sagittarius", "zodiac",
     "The centaur-archer of Sagittarius.", "Sagittarius — mutable Fire, ruled by Jupiter: vision, freedom, the quest."),
    (30, "30 - Il Cancro", "cancro", "Cancer", "zodiac",
     "The crab of Cancer.", "Cancer — cardinal Water, ruled by the Moon: home, feeling, nurture."),
    (31, "31 - I Pesci", "pesci", "Pisces", "zodiac",
     "The two fishes of Pisces.", "Pisces — mutable Water, ruled by Jupiter: dream, compassion, dissolution."),
    (32, "32 - L'Acquario", "acquario", "Aquarius", "zodiac",
     "The water-bearer of Aquarius.", "Aquarius — fixed Air, ruled by Saturn: the collective, invention, detachment."),
    (33, "33 - Il Leone", "leone", "Leo", "zodiac",
     "The lion of Leo.", "Leo — fixed Fire, ruled by the Sun: radiance, will, the proud heart."),
    (34, "34 - Il Toro", "toro", "Taurus", "zodiac",
     "The bull of Taurus.", "Taurus — fixed Earth, ruled by Venus: stability, the senses, persistence."),
    (35, "35 - I Gemelli", "gemelli", "Gemini", "zodiac",
     "The twins of Gemini.", "Gemini — mutable Air, ruled by Mercury: exchange, curiosity, the pair."),
    # 5 Arie (highest, unnumbered in play)
    (36, "36 - La Stella", "stella", "The Star", "arie",
     "A great star above a figure or landscape.", "Hope and guidance; the first of the five 'Arie', the supreme cards."),
    (37, "37 - La Luna", "luna", "The Moon", "arie",
     "The Moon over water, dogs or towers.", "The night light, dream and tide; one of the Arie."),
    (38, "38 - Il Sole", "sole", "The Sun", "arie",
     "A radiant sun over a couple or child.", "Daylight, vitality, the lit and conscious world."),
    (39, "39 - Il Mondo", "mondo", "The World", "arie",
     "A figure or city within a cosmic frame.", "Completion, the whole world surveyed; near the summit of the deck."),
    (40, "40 - Le Trombe", "trombe", "The Trumpets (Fame / Judgement)", "arie",
     "Angels sounding trumpets, the dead rising — 'Le Trombe', the Minchiate Last Judgement, the highest trump.",
     "The summons and the reckoning; Fame's trumpet. The supreme card of the Minchiate."),
]

SUITS = [("batons", "Batons", "Bastoni", "Fire", "Batons", "will, work, and growth"),
         ("coins", "Coins", "Denari", "Earth", "Coins", "money, body, and the material world"),
         ("cups", "Cups", "Coppe", "Water", "Cups", "feeling, love, and the inner life"),
         ("swords", "Swords", "Spade", "Air", "Swords", "mind, conflict, and decision")]
RANKS_PIP = {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
             8: "Eight", 9: "Nine", 10: "Ten"}
PIPM = {1: "the root and seed of the suit", 2: "pairing and exchange", 3: "first growth",
        4: "stability and foundation", 5: "tension and loss", 6: "harmony and reciprocity",
        7: "striving against resistance", 8: "movement and change", 9: "near-fullness, intensity",
        10: "completion, the suit in full"}
COURTS = [(11, "Jack", "Fante", "the page/maid of the suit — its youth and message"),
          (12, "Knight", "Cavallo", "the rider of the suit — in Minchiate often a centaur or sphinx — its active, questing force"),
          (13, "Queen", "Regina", "the inward mastery of the suit"),
          (14, "King", "Re", "the outward authority of the suit")]

items = []
so = 0
for num, fnpart, sid, name, group, icon, meaning in TRUMPS:
    fname = f"{PREFIX}Trumps - {fnpart}.jpg"
    u = img(fname)
    disp = "The Fool" if group == "fool" else f"{num} — {name}"
    items.append({
        "id": f"trump-{num:02d}-{sid}", "name": disp, "sort_order": so,
        "category": f"trump-{group}", "level": 1,
        "keywords": [name.lower(), group, "minchiate", "trionfi"],
        "image_url": u,
        "metadata": {"arcana": "trump", "trump_number": (None if group == "fool" else num),
                     "trump_group": group, "status": "surviving",
                     "illustrations": [{"url": u, "artist": "Florentine Minchiate workshop",
                                        "artist_dates": "c. 1860–1890", "edition": "Minchiate of Florence, c. 1860–1890",
                                        "scene": name, "license": "Public Domain", "is_primary": True}]},
        "sections": {"Iconography": icon, "Meaning": meaning},
    })
    so += 1

for sid, sdisp, sital, element, fileword, theme in SUITS:
    for n in range(1, 11):
        word = RANKS_PIP[n]
        fname = f"{PREFIX}{fileword} - {n:02d}.jpg"
        u = img(fname)
        items.append({
            "id": f"{sid}-{n:02d}" if n > 1 else f"{sid}-ace", "name": f"{word} of {sdisp}",
            "sort_order": so, "category": f"suit-{sid}", "level": 1,
            "keywords": [sdisp.lower(), element.lower(), word.lower(), "minor", sital.lower()],
            "image_url": u,
            "metadata": {"arcana": "minor", "suit": sdisp, "suit_italian": sital, "element": element, "rank": word,
                         "illustrations": [{"url": u, "artist": "Florentine Minchiate workshop", "artist_dates": "c. 1860–1890",
                                            "edition": "Minchiate of Florence, c. 1860–1890", "scene": f"{word} of {sdisp}",
                                            "license": "Public Domain", "is_primary": True}]},
            "sections": {
                "Iconography": f"{word} of {sdisp}: the suit-emblems of {sdisp.lower()} arranged in the "
                               f"Florentine pattern, with the elaborate borders typical of the Minchiate.",
                "Meaning": f"{word} of {sdisp} — {PIPM[n]}, within {theme}.",
            },
        })
        so += 1
    for rnum, rdisp, rital, role in COURTS:
        fname = f"{PREFIX}{fileword} - {rnum} - {rdisp}.jpg"
        u = img(fname)
        items.append({
            "id": f"{sid}-{rdisp.lower()}", "name": f"{rdisp} of {sdisp}", "sort_order": so,
            "category": f"suit-{sid}", "level": 1,
            "keywords": [sdisp.lower(), element.lower(), rdisp.lower(), "court", rital.lower()],
            "image_url": u,
            "metadata": {"arcana": "minor", "suit": sdisp, "suit_italian": sital, "element": element,
                         "rank": rdisp, "court": True,
                         "illustrations": [{"url": u, "artist": "Florentine Minchiate workshop", "artist_dates": "c. 1860–1890",
                                            "edition": "Minchiate of Florence, c. 1860–1890", "scene": f"{rdisp} of {sdisp}",
                                            "license": "Public Domain", "is_primary": True}]},
            "sections": {
                "Iconography": f"{rdisp} of {sdisp} ({rital}): a court figure of the suit. In the Minchiate the "
                               f"knights are often centaurs or beasts, and Cups and Coins carry female pages.",
                "Meaning": f"{rdisp} of {sdisp} — {role}, within {theme}.",
            },
        })
        so += 1

# ---- emergences ----
all_ids = {it["id"] for it in items}
def grp(g): return [it["id"] for it in items if it["category"] == f"trump-{g}"]
emgs = [
    ("emg-papi", "The Five Papi", grp("papi"), img(f"{PREFIX}Trumps - 01 - Papa uno.jpg"),
     {"About these Cards": "Where ordinary tarot has the Popess, Empress, Emperor, Pope, and Love, the "
      "Minchiate has five ranked but near-identical 'Papi' (Popes). The Popess — the heretical card of the "
      "Visconti decks — is gone entirely. Church and Empire are flattened into one interchangeable office.",
      "Why this Matters": "The disappearance of the Popess and the merging of the powers shows the tarot's "
      "imagery being sanitised and standardised as the deck spread through Counter-Reformation Italy."}),
    ("emg-virtues", "The Seven Virtues — Complete", grp("virtue"), img(f"{PREFIX}Trumps - 17 - La Prudenza.jpg"),
     {"About these Cards": "The Minchiate is the deck of the COMPLETE seven virtues. To the three cardinal "
      "virtues of ordinary tarot (Temperance, Fortitude, Justice) it restores the fourth — Prudence — and "
      "adds the three theological virtues, Faith, Hope, and Charity.",
      "Why this Matters": "Only the Cary-Yale (with its three theological virtues) and the Minchiate (with "
      "all seven) treat the tarot as a complete moral cosmos. The Minchiate makes the virtue programme total."}),
    ("emg-elements", "The Four Elements", grp("element"), img(f"{PREFIX}Trumps - 20 - Il Fuoco.jpg"),
     {"About these Cards": "Fire, Water, Earth, and Air enter the trump sequence as cards in their own right "
      "— a feature found in no standard tarot. With the twelve zodiac signs above them, the Minchiate builds "
      "a whole cosmology into the deck.",
      "How to Use": "Read the elements as the building blocks beneath the zodiac: the four qualities from "
      "which the twelve signs are composed."}),
    ("emg-zodiac", "The Twelve Signs of the Zodiac", grp("zodiac"), img(f"{PREFIX}Trumps - 33 - Il Leone.jpg"),
     {"About these Cards": "The twelve zodiac signs form the longest stretch of the Minchiate trumps — a full "
      "astrological wheel set into the deck (in Minchiate's own idiosyncratic order, beginning with Libra). "
      "No other historical tarot contains them.",
      "How to Use": "Read each as its sign — element, mode, and ruling planet — turning the deck into a "
      "portable zodiac."}),
    ("emg-arie", "The Arie — The Five Supreme Cards", grp("arie"), img(f"{PREFIX}Trumps - 40 - Le Trombe.jpg"),
     {"About these Cards": "The five highest cards — Star, Moon, Sun, World, and the Trumpets (Le Trombe, the "
      "Last Judgement) — are the 'Arie', unnumbered and supreme in play, crowning the whole 97-card edifice.",
      "How to Use": "These are the deck's heavens: the celestial lights and the final trumpet above the "
      "zodiac, the elements, and all the world below."}),
]
for sid, sdisp, sital, element, fileword, theme in SUITS:
    kids = [it["id"] for it in items if it["category"] == f"suit-{sid}"]
    emgs.append((f"emg-suit-{sid}", f"Suit of {sdisp} ({sital}) — {element}", kids,
                 img(f"{PREFIX}{fileword} - 13 - Queen.jpg"),
                 {"About this Suit": f"The {sdisp} ({sital}) of the Minchiate, suit of {element}. Each suit "
                  f"keeps the full court of four — and in Cups and Coins the page is a woman, while the "
                  f"knights ride as centaurs.",
                  "How to Use": f"Read the suit for {theme.split(',')[0]} in the everyday world beneath the "
                  f"great cosmological trumps."}))
for eid, ename, kids, image_url, sections in emgs:
    kids = [k for k in kids if k in all_ids]
    items.append({"id": eid, "name": ename, "sort_order": so, "category": "emergence", "level": 2,
                  "composite_of": kids, "relationship_type": "emergence",
                  "image_url": image_url, "metadata": {}, "sections": sections})
    so += 1

for it in items:
    if it.get("category") != "emergence":
        it["sections"]["Tradition Note"] = TRADITION_NOTE

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Florentine Minchiate workshop", "date": "c. 1860–1890",
             "note": "The scanned Minchiate of Florence used for imagery"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "Card images, Category:Minchiate card deck - Florence - 1860-1890"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar architecture and summaries"},
        ],
    },
    "name": "Minchiate — The 97-Card Florentine Tarot",
    "description": (
        "The grandest expansion of tarot ever to see wide use. The Minchiate, played in Florence from the "
        "16th century, swells the deck to 97 cards by adding twenty trumps to the standard sequence: the "
        "four classical elements (Fire, Water, Earth, Air), the twelve signs of the zodiac, and the virtues "
        "that ordinary tarot leaves out — Prudence, restoring the full set of four cardinal virtues, and the "
        "three theological virtues Faith, Hope, and Charity, so that all SEVEN virtues are present. It "
        "dissolves the Popess, Empress, Emperor, Pope, and Love into five interchangeable 'Papi', dropping "
        "the heretical Popess entirely.\n\n"
        "The result is a whole cosmology built into a card game: the elements beneath, the zodiac above them, "
        "and five supreme 'Arie' (Star, Moon, Sun, World, and the Trumpets of the Last Judgement) crowning "
        "the deck. Beneath the 41 special cards run the four ordinary suits — Batons, Coins, Cups, Swords — "
        "each with ten pips and a full court of four (the knights ridden as centaurs, the Cups and Coins "
        "pages as women).\n\n"
        "This is a historical/iconographic grammar: each card carries an Iconography note and a Meaning. "
        "Imagery is from the fully-scanned Minchiate of Florence, c. 1860–1890.\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Minchiate of Florence, c. 1860–1890 (Wikimedia Commons, "
        "Category:Minchiate card deck - Florence - 1860-1890) — etched and stencil-coloured cards, the "
        "late Etruria-pattern Florentine Minchiate. Earlier hand-painted and Poilly Minchiate decks also "
        "survive for richer imagery."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": img(f"{PREFIX}Trumps - 40 - Le Trombe.jpg"),
    "tags": ["tarot", "minchiate", "florence", "97-cards", "zodiac", "elements", "virtues",
             "history", "public-domain", "trionfi"],
    "roots": ["western-esoteric", "renaissance"],
    "shelves": ["wonder", "mirror"],
    "lineages": ["Andreotti"],
    "worldview": "historical",
    "is_published": False,
    "items": items,
}

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "grammar.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)
print(f"Wrote {out_path}")
n_tr = sum(1 for it in items if str(it['category']).startswith('trump-'))
n_mi = sum(1 for it in items if str(it['category']).startswith('suit-'))
n_em = sum(1 for it in items if it['category'] == 'emergence')
print(f"  items: {len(items)}  (special {n_tr}, suited {n_mi}, emergences {n_em})  imaged: {sum(1 for it in items if it.get('image_url'))}")
