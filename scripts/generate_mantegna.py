# -*- coding: utf-8 -*-
"""Generate grammars/mantegna-tarocchi/grammar.json.

The so-called "Mantegna Tarocchi" (E-series, North Italy, c. 1465) — a set of 50
engravings that is NOT a tarot at all. It has no suits, no trumps, no game: it is a
Neoplatonic LADDER of being, rising in five decades from the Beggar through the
estates of man, the Muses, the liberal arts, the virtues and cosmic genii, the
planetary spheres, up to the First Cause. It is constantly confused with tarot
because of its name and its 15th-century Italian origin; this grammar exists partly
to clear that up. (Not by Mantegna, either — the attribution is traditional.)

grammar_type is "custom", NOT "tarot" — deliberately, because it is not one.

Images: Wikimedia Commons, the Cleveland Museum of Art set (1924.432.1–50), served
via Special:FilePath with a width param so the TIF originals render as JPEG.
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "mantegna-tarocchi")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"

# Exact Commons filenames (Cleveland set), captured from the Commons API.
FILES = {
44: "Master of the E-Series Tarocchi - Sun (from the Tarocchi, series A- Firmaments of the Universe, 44) - 1924.432.44 - Cleveland Museum of Art.jpg",
41: "Master of the E-Series Tarocchi - Luna (from the Tarocchi, series A- Firmaments of the Universe, 41) - 1924.432.41 - Cleveland Museum of Art.tif",
6: "Master of the E-Series Tarocchi - The Knight (from the Tarocchi, series E- Conditions of Man, 6) - 1924.432.6 - Cleveland Museum of Art.tif",
49: "Master of the E-Series Tarocchi - The Angel of the Ninth Sphere (from the Tarocchi, series A- Firmaments of - 1924.432.49 - Cleveland Museum of Art.jpg",
33: "Master of the E-Series Tarocchi - Genius of the World (from the Tarocchi, series B- Cosmic Principles & Virtu - 1924.432.33 - Cleveland Museum of Art.jpg",
37: "Master of the E-Series Tarocchi - Justice (from the Tarocchi, series B- Cosmic Principles & Virtues, 37) - 1924.432.37 - Cleveland Museum of Art.tif",
21: "Master of the E-Series Tarocchi - Grammar (from the Tarocchi, series C- Liberal Arts, 21) - 1924.432.21 - Cleveland Museum of Art.tif",
40: "Master of the E-Series Tarocchi - Faith (from the Tarocchi, series B- Cosmic Principles & Virtues, 40) - 1924.432.40 - Cleveland Museum of Art.tif",
46: "Master of the E-Series Tarocchi - Jupiter (from the Tarocchi, series A- Firmaments of the Universe, 46) - 1924.432.46 - Cleveland Museum of Art.tif",
34: "Master of the E-Series Tarocchi - Temperance (from the Tarocchi, series B- Cosmic Principles & Virtues, 34) - 1924.432.34 - Cleveland Museum of Art.jpg",
43: "Master of the E-Series Tarocchi - Venus (from the Tarocchi, series A- Firmaments of the Universe, 43) - 1924.432.43 - Cleveland Museum of Art.tif",
38: "Master of the E-Series Tarocchi - Charity (from the Tarocchi, series B- Cosmic Principles & Virtues, 38) - 1924.432.38 - Cleveland Museum of Art.jpg",
50: "Master of the E-Series Tarocchi - The Empyrean Sphere (from the Tarocchi, series A- Firmaments of the Univer - 1924.432.50 - Cleveland Museum of Art.tif",
7: "Master of the E-Series Tarocchi - The Doge (from the Tarocchi, series E- Conditions of Man, 7) - 1924.432.7 - Cleveland Museum of Art.tif",
29: "Master of the E-Series Tarocchi - Astrology (from the Tarocchi, series C- Liberal Arts, 29) - 1924.432.29 - Cleveland Museum of Art.tif",
3: "Master of the E-Series Tarocchi - The Artisan (from the Tarocchi, series E- Conditions of Man, 3) - 1924.432.3 - Cleveland Museum of Art.tif",
42: "Master of the E-Series Tarocchi - Mercury (from the Tarocchi, series A- Firmaments of the Universe, 42) - 1924.432.42 - Cleveland Museum of Art.tif",
10: "Master of the E-Series Tarocchi - The Pope (from the Tarocchi, series E- Conditions of Man, 10) - 1924.432.10 - Cleveland Museum of Art.tif",
48: "Master of the E-Series Tarocchi - The Angel of the Eighth Sphere (from the Tarocchi, series A- Firmaments of - 1924.432.48 - Cleveland Museum of Art.jpg",
22: "Master of the E-Series Tarocchi - Logic (from the Tarocchi, series C- Liberal Arts, 22) - 1924.432.22 - Cleveland Museum of Art.tif",
8: "Master of the E-Series Tarocchi - The King (from the Tarocchi, series E- Conditions of Man, 8) - 1924.432.8 - Cleveland Museum of Art.jpg",
2: "Master of the E-Series Tarocchi - The Servant (from the Tarocchi, series E- Conditions of Man, 2) - 1924.432.2 - Cleveland Museum of Art.jpg",
25: "Master of the E-Series Tarocchi - Arithmetic (from the Tarocchi, series C- Liberal Arts, 25) - 1924.432.25 - Cleveland Museum of Art.tif",
13: "Master of the E-Series Tarocchi - Terpsichore (dancing and song) (from the Tarocchi series D- Apollo and th - 1924.432.13 - Cleveland Museum of Art.tif",
47: "Master of the E-Series Tarocchi - Saturn (from the Tarocchi, series A- Firmaments of the Universe, 47) - 1924.432.47 - Cleveland Museum of Art.jpg",
4: "Master of the E-Series Tarocchi - The Merchant (from the Tarocchi, series E- Conditions of Man, 4) - 1924.432.4 - Cleveland Museum of Art.tif",
11: "Master of the E-Series Tarocchi - Calliope (from the Tarocchi series D- Apollo and the Muses, 11) - 1924.432.11 - Cleveland Museum of Art.tif",
31: "Master of the E-Series Tarocchi - Genius of the Sun (from the Tarocchi, series B- Cosmic Principles & Virtues - 1924.432.31 - Cleveland Museum of Art.tif",
1: "Master of the E-Series Tarocchi - The Beggar (from the Tarocchi, series E- Conditions of Man, 1) - 1924.432.1 - Cleveland Museum of Art.jpg",
28: "Master of the E-Series Tarocchi - Philosophy (from the Tarocchi, series C- Liberal Arts, 28) - 1924.432.28 - Cleveland Museum of Art.tif",
32: "Master of the E-Series Tarocchi - Genius of Time (from the Tarocchi, series B- Cosmic Principles & Virtues, - 1924.432.32 - Cleveland Museum of Art.tif",
16: "Master of the E-Series Tarocchi - Thalia (comedy, pastoral poetry) (from the Tarocchi series D- Apollo and t - 1924.432.16 - Cleveland Museum of Art.jpg",
39: "Master of the E-Series Tarocchi - Hope (from the Tarocchi, series B- Cosmic Principles & Virtues, 39) - 1924.432.39 - Cleveland Museum of Art.jpg",
24: "Master of the E-Series Tarocchi - Geometry (from the Tarocchi, series C- Liberal Arts, 24) - 1924.432.24 - Cleveland Museum of Art.tif",
12: "Master of the E-Series Tarocchi - Urania (astronomy) (from the Tarocchi series D- Apollo and the Muses, 12) - 1924.432.12 - Cleveland Museum of Art.tif",
18: "Master of the E-Series Tarocchi - Euterpe (music, lyric poetry) (from the Tarocchi series D- Apollo and the - 1924.432.18 - Cleveland Museum of Art.tif",
5: "Master of the E-Series Tarocchi - Gentleman (from the Tarocchi series E- Conditions of Man, 5) - 1924.432.5 - Cleveland Museum of Art.tif",
26: "Clevelandart 1924.432.26.jpg",
36: "Master of the E-Series Tarocchi - Forteza (from the Tarocchi, series B- Cosmic Principles & Virtues, 36) - 1924.432.36 - Cleveland Museum of Art.tif",
23: "Master of the E-Series Tarocchi - Rhetoric (from the Tarocchi, series C- Liberal Arts, 23) - 1924.432.23 - Cleveland Museum of Art.tif",
9: "Master of the E-Series Tarocchi - The Emperor (from the Tarocchi, series E- Conditions of Man, 9) - 1924.432.9 - Cleveland Museum of Art.tif",
27: "Master of the E-Series Tarocchi - Poetry (from the Tarocchi, series C- Liberal Arts, 27) - 1924.432.27 - Cleveland Museum of Art.tif",
14: "Master of the E-Series Tarocchi - Erato (lyric and love poetry) (from the Tarocchi series D- Apollo and the - 1924.432.14 - Cleveland Museum of Art.tif",
35: "Master of the E-Series Tarocchi - Prudence (from the Tarocchi, series B- Cosmic Principles & Virtues, 35) - 1924.432.35 - Cleveland Museum of Art.tif",
20: "Master of the E-Series Tarocchi - Apollo (from the Tarocchi, series D- Apollo and the Muses, 20) - 1924.432.20 - Cleveland Museum of Art.tif",
17: "Master of the E-Series Tarocchi - Melpomene (tragedy) (from the Tarocchi series D- Apollo and the Muses, 17 - 1924.432.17 - Cleveland Museum of Art.tif",
19: "Master of the E-Series Tarocchi - Clio (history) (from the Tarocchi series D- Apollo and the Muses, 19) - 1924.432.19 - Cleveland Museum of Art.tif",
15: "Master of the E-Series Tarocchi - Polyhymnia (heroic hymns) (from the Tarocchi series D- Apollo and the Muse - 1924.432.15 - Cleveland Museum of Art.tif",
45: "Master of the E-Series Tarocchi - Mars (from the Tarocchi, series A- Firmaments of the Universe, 45) - 1924.432.45 - Cleveland Museum of Art.tif",
30: "Master of the E-Series Tarocchi (Italian, 15th century) - Theology (from the Tarocchi, series C, Liberal Arts, ^30) - 1924.432.30 - Cleveland Museum of Art.jpg",
}


def img(n):
    return COMMONS + urllib.parse.quote(FILES[n]) + "?width=700"


# num: (name, italian, group_id, depicts)
CARDS = {
    1: ("The Beggar", "Misero", "estates", "A ragged beggar with two dogs — the lowest condition of man."),
    2: ("The Servant", "Fameio", "estates", "A young serving-man; the second estate."),
    3: ("The Artisan", "Artixan", "estates", "A craftsman with his tools."),
    4: ("The Merchant", "Merchadante", "estates", "A merchant with his goods."),
    5: ("The Gentleman", "Zintilomo", "estates", "A gentleman of leisure, finely dressed."),
    6: ("The Knight", "Cavalier", "estates", "An armoured knight on the social ladder."),
    7: ("The Doge", "Doxe", "estates", "The Doge — an elected prince in his robes of office."),
    8: ("The King", "Re", "estates", "A crowned king enthroned."),
    9: ("The Emperor", "Imperator", "estates", "The Emperor, secular summit of the estates."),
    10: ("The Pope", "Papa", "estates", "The Pope — the highest earthly estate, crowning the ladder of men."),
    11: ("Calliope", "Caliope", "muses", "Muse of epic poetry."),
    12: ("Urania", "Urania", "muses", "Muse of astronomy, holding the celestial globe."),
    13: ("Terpsichore", "Terpsicore", "muses", "Muse of dance and choral song."),
    14: ("Erato", "Erato", "muses", "Muse of lyric and love poetry."),
    15: ("Polyhymnia", "Polimnia", "muses", "Muse of sacred hymn and rhetoric."),
    16: ("Thalia", "Talia", "muses", "Muse of comedy and pastoral poetry."),
    17: ("Melpomene", "Melpomene", "muses", "Muse of tragedy."),
    18: ("Euterpe", "Euterpe", "muses", "Muse of music and lyric poetry."),
    19: ("Clio", "Clio", "muses", "Muse of history."),
    20: ("Apollo", "Apollo", "muses", "The god Apollo, leader of the Muses on Parnassus."),
    21: ("Grammar", "Gramatica", "arts", "The first liberal art — the rule of language."),
    22: ("Logic", "Loica", "arts", "The art of reasoning."),
    23: ("Rhetoric", "Rhetorica", "arts", "The art of persuasion, with sword and trumpets."),
    24: ("Geometry", "Geometria", "arts", "The measure of the earth."),
    25: ("Arithmetic", "Arithmetricha", "arts", "The science of number."),
    26: ("Music", "Musicha", "arts", "The art of harmony."),
    27: ("Poetry", "Poesia", "arts", "Inspired song, crowned with laurel."),
    28: ("Philosophy", "Philosofia", "arts", "The love of wisdom, embracing heaven and earth."),
    29: ("Astrology", "Astrologia", "arts", "The reading of the heavens."),
    30: ("Theology", "Theologia", "arts", "The highest knowledge — the science of the divine."),
    31: ("Genius of the Sun", "Iliaco", "genii", "The solar daemon — the living spirit of the Sun."),
    32: ("Genius of Time", "Chronico", "genii", "Winged Time — the daemon of duration."),
    33: ("Genius of the World", "Cosmico", "genii", "The world-daemon — the animating spirit of the cosmos."),
    34: ("Temperance", "Temperancia", "virtues", "Cardinal virtue: measure, tempering the waters."),
    35: ("Prudence", "Prudencia", "virtues", "Cardinal virtue: foresight, the mirror and serpent."),
    36: ("Fortitude", "Forteza", "virtues", "Cardinal virtue: strength, breaking the column."),
    37: ("Justice", "Justicia", "virtues", "Cardinal virtue: the sword and the balance."),
    38: ("Charity", "Charita", "virtues", "Theological virtue: self-giving love."),
    39: ("Hope", "Speranza", "virtues", "Theological virtue: the upward reach, with the phoenix."),
    40: ("Faith", "Fede", "virtues", "Theological virtue: trust, with chalice and cross."),
    41: ("The Moon", "Luna", "spheres", "The first planetary sphere — Diana of the Moon in her car."),
    42: ("Mercury", "Mercurio", "spheres", "The sphere of Mercury, messenger of the gods."),
    43: ("Venus", "Venus", "spheres", "The sphere of Venus, with cupids."),
    44: ("The Sun", "Sol", "spheres", "The sphere of the Sun — Apollo/Helios in his chariot."),
    45: ("Mars", "Marte", "spheres", "The sphere of Mars, the armed god of war."),
    46: ("Jupiter", "Jupiter", "spheres", "The sphere of Jupiter, king of the gods."),
    47: ("Saturn", "Saturno", "spheres", "The sphere of Saturn, devouring Time."),
    48: ("The Eighth Sphere", "Octava Spera", "spheres", "The sphere of the fixed stars — the firmament."),
    49: ("The Ninth Sphere (Primum Mobile)", "Primo Mobile", "spheres", "The Prime Mover — the sphere that turns all below it."),
    50: ("The First Cause (Empyrean)", "Prima Causa", "spheres", "The First Cause — God, the still summit of the whole ascent."),
}

GROUPS = [
    ("estates", "E · The Estates of Man (1–10)",
     "The ten conditions of humankind, from the Beggar to the Pope — the social ladder that begins the ascent."),
    ("muses", "D · Apollo and the Muses (11–20)",
     "Apollo and the nine Muses — the inspired arts that lift the soul above mere estate."),
    ("arts", "C · The Liberal Arts & Sciences (21–30)",
     "Grammar to Theology — the trivium, quadrivium, and the higher sciences, the disciplines of the mind."),
    ("genii", "B · The Cosmic Genii (31–33)",
     "The three world-daemons — the living spirits of the Sun, of Time, and of the World."),
    ("virtues", "B · The Seven Virtues (34–40)",
     "The four cardinal and three theological virtues — the moral perfection of the soul."),
    ("spheres", "A · The Firmament (41–50)",
     "The seven planetary spheres rising to the fixed stars, the Prime Mover, and the First Cause — the cosmos itself, ending in God."),
]

items = []
so = 0
for num in range(1, 51):
    name, ital, grp, depicts = CARDS[num]
    u = img(num)
    items.append({
        "id": f"plate-{num:02d}", "name": f"{num} — {name}", "sort_order": so,
        "category": f"series-{grp}", "level": 1,
        "keywords": [name.lower(), ital.lower(), "mantegna", "e-series", grp, "not-a-tarot"],
        "image_url": u,
        "metadata": {"series_number": num, "italian_name": ital, "series_group": grp,
                     "illustrations": [{"url": u, "artist": "Master of the E-Series Tarocchi (North Italian)",
                                        "artist_dates": "active c. 1465",
                                        "edition": "Mantegna Tarocchi, E-series, c. 1465 (Cleveland Museum of Art impression)",
                                        "scene": name, "license": "Public Domain", "is_primary": True}]},
        "sections": {
            "Depicts": depicts,
            "On the Ladder": f"Number {num} of 50, in the series of {dict((g[0],g[1]) for g in GROUPS)[grp]}. "
                             f"The Mantegna series is a single ascent from the Beggar (1) to the First Cause (50).",
            "Note: not a tarot": "These 50 engravings are NOT a tarot — no suits, no trumps, no game. They "
                                 "are a Neoplatonic teaching ladder, mislabelled 'Tarocchi' by later collectors.",
        },
    })
    so += 1

all_ids = {it["id"] for it in items}
for grp, gname, blurb in GROUPS:
    kids = [it["id"] for it in items if it["category"] == f"series-{grp}"]
    items.append({
        "id": f"emg-{grp}", "name": gname, "sort_order": so, "category": "emergence", "level": 2,
        "composite_of": kids, "relationship_type": "emergence",
        "image_url": img(items_min := min(int(it["id"].split("-")[1]) for it in items if it["category"] == f"series-{grp}")),
        "metadata": {}, "sections": {"About this series": blurb},
    })
    so += 1

# L3 root — the whole ladder
items.append({
    "id": "root-the-ladder", "name": "The Ladder of Being (all 50)", "sort_order": so,
    "category": "root", "level": 3,
    "composite_of": [f"emg-{g[0]}" for g in GROUPS], "relationship_type": "emergence",
    "image_url": img(50),
    "metadata": {},
    "sections": {
        "The whole ascent": "Read in order, the 50 plates form one continuous Neoplatonic ascent: from the "
        "Beggar at the bottom of human society, up through the estates, the inspiring Muses, the disciplines "
        "of knowledge, the cosmic genii and the seven virtues, then the planetary spheres, to the fixed "
        "stars, the Prime Mover, and finally the First Cause — God. It is a map of the soul's climb from "
        "matter to the divine.",
        "Why it is here (and why it is NOT a tarot)": "The 'Mantegna Tarocchi' is the most famous false "
        "relative of the tarot: a 15th-century Italian engraving set, often shelved beside tarot and even "
        "called 'Tarocchi', but with no suits, no 22 trumps, and no game. (It is also not by Mantegna.) Its "
        "imagery — virtues, planets, estates — overlaps the tarot trumps because both drew on the same "
        "Renaissance iconographic vocabulary, which is exactly why the two are confused. Including it here "
        "lets the genealogy say clearly: this is a cousin in imagery, not an ancestor in fact.",
    },
})

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Master of the E-Series Tarocchi", "date": "c. 1465",
             "note": "North Italian engraver (NOT Andrea Mantegna, despite the traditional name)"},
            {"name": "Cleveland Museum of Art", "date": "public domain",
             "note": "The 1924.432.1–50 impression of the E-series, via Wikimedia Commons"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar architecture and summaries"},
        ],
    },
    "name": "The 'Mantegna Tarocchi' — A Ladder of Being (NOT a Tarot), c. 1465",
    "description": (
        "Fifty engravings from c. 1465 that are constantly mistaken for a tarot — and are not one. The "
        "'Mantegna Tarocchi' (not by Mantegna, and not a tarot) is a Neoplatonic LADDER of being: five "
        "decades of ten cards rising from the Beggar through the estates of man, Apollo and the Muses, the "
        "liberal arts and sciences, the cosmic genii and the seven virtues, the seven planetary spheres, the "
        "fixed stars, the Prime Mover, and finally the First Cause — God.\n\n"
        "It has NO suits, NO 22 trumps, and NO game; it was an educational and contemplative print series. "
        "It is included in this tarot library precisely to clear up the confusion: its virtues, planets, and "
        "estates overlap the tarot trumps because both drew on the same Renaissance iconographic vocabulary "
        "— a cousin in imagery, not an ancestor in fact. (Its `grammar_type` is `custom`, not `tarot`, on "
        "purpose.)\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: the 'Mantegna Tarocchi', E-series, c. 1465 — the Cleveland "
        "Museum of Art impression (1924.432.1–50) on Wikimedia Commons; engravings served via Special:FilePath."
    ),
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": img(50),
    "tags": ["mantegna-tarocchi", "e-series", "neoplatonic", "engravings", "renaissance",
             "not-a-tarot", "history", "public-domain", "ladder-of-being"],
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
print(f"Wrote mantegna-tarocchi/grammar.json — {len(items)} items, imaged {sum(1 for it in items if it.get('image_url'))}")
