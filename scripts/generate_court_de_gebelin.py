# -*- coding: utf-8 -*-
"""Generate grammars/court-de-gebelin-tarot/grammar.json.

The plates from Antoine Court de Gébelin's 'Le Monde Primitif', vol. VIII (1781) —
the 22 atouts (trumps) that accompanied the essay which INVENTED esoteric tarot.
Court de Gébelin claimed the Tarot de Marseille was an ancient Egyptian 'Book of
Thoth', a hieroglyphic book of priestly wisdom. The claim is false — tarot is a
15th-century Italian card GAME — but this essay is the hinge of the whole occult
tradition: Etteilla, Lévi, Wirth, the Golden Dawn, and the entire idea of tarot
divination descend from it.

The same 1781 volume carried a second essay by the Comte de Mellet, who proposed
reading the trumps in REVERSE as an Egyptian cosmogony and first floated the
Hebrew-letter associations that Lévi later systematised.

Images: Wikimedia Commons, Category:Court de Gébelin tarot (the 22 'Atout' plates).
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "court-de-gebelin-tarot")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"


def img(n):
    return COMMONS + urllib.parse.quote(f"Court de Gébelin - Atout {n:02d}.jpg")


NOTE = (
    "Court de Gébelin's claim (1781) that the tarot is an ancient Egyptian 'Book of "
    "Thoth' is a myth — the tarot is a 15th-century Italian card game. But this essay "
    "INVENTED esoteric tarot: every occult deck and the whole practice of tarot "
    "divination descend from this single, mistaken, fertile idea."
)

# num, name(FR), name(EN), iconography(plate), gebelin reading
CARDS = [
    (0, "Le Mat", "The Fool", "A traveller in motley with a staff and bundle, a beast at his leg — the Marseille Fool, copied into the plate.",
     "Court de Gébelin reads the unnumbered card as Folly (la Folie) — the senseless man, outside the sacred sequence."),
    (1, "Le Bateleur", "The Magician", "A figure at a table of cups, coins and knives, wand raised.",
     "He reads the Bateleur as the active, material principle — the conjuror, the maker, the first agent of creation."),
    (2, "La Papesse", "The High Priestess", "A veiled, enthroned woman in a tiara with a book.",
     "For Court de Gébelin she is the HIGH PRIESTESS of Egypt — sacred wisdom in female form, not a scandalous 'popess'."),
    (3, "L'Impératrice", "The Empress", "A crowned woman with sceptre and eagle shield.",
     "The Queen, or the female sovereign principle of the Egyptian state and nature's fertility."),
    (4, "L'Empereur", "The Emperor", "A bearded sovereign in profile with sceptre and shield.",
     "The King — temporal sovereignty among the Egyptians."),
    (5, "Le Pape", "The Hierophant", "A tiara'd pontiff blessing two acolytes.",
     "Court de Gébelin makes him the GRAND HIEROPHANT — the chief priest of the Egyptian mysteries."),
    (6, "L'Amoureux", "The Lovers", "A youth between two women beneath a winged Cupid drawing his bow.",
     "He reads it as Marriage, and as the man choosing between Vice and Virtue — Hercules at the crossroads."),
    (7, "Le Chariot", "The Chariot", "A crowned prince in a canopied chariot drawn by two horses.",
     "Osiris triumphant, or the King in his war-chariot — victory and dominion."),
    (8, "La Justice", "Justice", "An enthroned woman with sword and balance.",
     "One of the three cardinal Virtues the Egyptians set among the sacred cards."),
    (9, "L'Hermite", "The Hermit", "A cloaked old man with a staff and a shielded lantern.",
     "The Sage or Hermit seeking truth — Court de Gébelin sometimes names him the Egyptian seeker of wisdom (the 'Capuchin')."),
    (10, "La Roue de Fortune", "Wheel of Fortune", "A wheel turned by figures rising and falling.",
     "The wheel of destiny — the turning of fortune the Egyptian priests taught."),
    (11, "La Force", "Strength", "A woman calmly parting a lion's jaws.",
     "Fortitude — the second of the three cardinal Virtues among the sacred cards."),
    (12, "Le Pendu", "The Hanged Man", "A youth suspended by one foot from a frame.",
     "Court de Gébelin believed the card was printed UPSIDE-DOWN: rightly turned, he says, it shows Prudence, the fourth cardinal Virtue, with a raised foot."),
    (13, "La Mort", "Death", "A skeleton with a scythe among the fallen — the card left unnamed in the Marseille.",
     "Death — the great Egyptian passage; he notes the Marseille leaves it nameless out of dread."),
    (14, "Tempérance", "Temperance", "A winged figure pouring liquid between two vessels.",
     "Temperance — the third of the cardinal Virtues set among the sacred cards."),
    (15, "Le Diable", "The Devil", "A horned, winged figure over two bound captives.",
     "TYPHON — the evil principle of Egyptian theology, the destroyer set against Osiris."),
    (16, "La Maison-Dieu", "The Tower", "Figures fall from a tower struck by fire from the sky.",
     "He reads the 'Maison-Dieu' as the Castle of Plutus, or the temple of pride struck down — calamity and the fall of avarice."),
    (17, "L'Étoile", "The Star", "A naked woman kneels pouring two urns into water and onto land, beneath a great star and seven small ones.",
     "His most famous reading: the great star is SIRIUS (Sothis), the Dog-Star whose rising herald the flooding of the NILE; the woman pours the inundation that renews Egypt."),
    (18, "La Lune", "The Moon", "A dripping moon over two dogs and a crayfish between two towers.",
     "The Moon and its dew; he reads the falling drops as the influence of the moon on the Egyptian year."),
    (19, "Le Soleil", "The Sun", "A radiant sun over two children by a wall.",
     "The Sun — Osiris as the day-star, the source of Egyptian life."),
    (20, "Le Jugement", "Judgement", "An angel trumpets while the dead rise from a tomb.",
     "The Creation, or the Last Judgement — the awakening of the dead the Egyptians taught."),
    (21, "Le Monde", "The World", "A dancing figure in a wreath, the four beasts in the corners.",
     "TIME, or the Universe — Court de Gébelin reads the central figure as Isis and the four beasts as the four seasons/elements: the whole created world."),
]

items = []
for i, (num, fr, en, icon, reading) in enumerate(CARDS):
    u = img(num)
    items.append({
        "id": f"atout-{num:02d}", "name": f"{num} — {en} ({fr})", "sort_order": i,
        "category": "major-arcana", "level": 1,
        "keywords": [en.lower().replace("the ", ""), fr.lower(), "court de gebelin", "egyptian", "esoteric"],
        "image_url": u,
        "metadata": {"arcana": "major", "number": num, "french_name": fr,
                     "illustrations": [{"url": u, "artist": "Antoine Court de Gébelin (plates)",
                                        "artist_dates": "1725–1784",
                                        "edition": "Le Monde Primitif, vol. VIII, 1781",
                                        "scene": f"{en} ({fr})", "license": "Public Domain", "is_primary": True}]},
        "sections": {
            "Iconography": icon,
            "Court de Gébelin's Egyptian Reading": reading,
            "Tradition Note": NOTE,
        },
    })

# L2 emergence
items.append({
    "id": "emg-book-of-thoth", "name": "The 'Book of Thoth' — The Birth of Occult Tarot",
    "sort_order": len(items), "category": "emergence", "level": 2,
    "composite_of": [it["id"] for it in items if it["category"] == "major-arcana"],
    "relationship_type": "emergence", "image_url": img(21),
    "metadata": {},
    "sections": {
        "What happened here": "In 1781 Antoine Court de Gébelin looked at an ordinary Tarot de Marseille — a "
        "card game — and declared it the last survivor of an ancient Egyptian 'Book of Thoth', a hieroglyphic "
        "encyclopaedia of priestly wisdom carried west by the 'Gypsies'. He was wrong on every count: tarot "
        "is a 15th-century Italian game, the 'Egyptian' reading is invented, and the Romani have no link to "
        "Egypt. Hieroglyphs would not be deciphered for another 40 years.",
        "Why it matters": "And yet this single essay created esoteric tarot. Within a decade Etteilla built "
        "the first divination deck on it; Lévi added the Kabbalah; Wirth, the Golden Dawn, Waite, and Crowley "
        "followed. Every occult tarot — and the whole idea that tarot tells fortunes — descends from this "
        "beautiful mistake. The companion essay by the Comte de Mellet, in the same volume, first proposed "
        "the Hebrew-letter associations and the reverse-order Egyptian cosmogony."},
})

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Antoine Court de Gébelin", "date": "1781",
             "note": "Le Monde Primitif, vol. VIII — the essay and plates that invented esoteric tarot"},
            {"name": "Comte de Mellet", "date": "1781",
             "note": "Companion essay (same volume): reverse-order Egyptian cosmogony + Hebrew letters"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "The 22 'Atout' plates, Category:Court de Gébelin tarot"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar architecture and summaries"},
        ],
    },
    "name": "Court de Gébelin's Tarot — The Birth of the 'Book of Thoth' (1781)",
    "description": (
        "The 22 trump plates from Antoine Court de Gébelin's 'Le Monde Primitif' (vol. VIII, 1781) — the "
        "essay that INVENTED esoteric tarot. Looking at an ordinary Tarot de Marseille, Court de Gébelin "
        "declared it the last fragment of an ancient Egyptian 'Book of Thoth', a hieroglyphic book of "
        "priestly wisdom. Every claim is false — tarot is a 15th-century Italian card game, and Egyptian "
        "hieroglyphs would not be read for another four decades — but this is the single most consequential "
        "mistake in tarot's history: Etteilla, Lévi, Wirth, the Golden Dawn, Waite and Crowley all build on "
        "it, and the very idea of tarot divination begins here.\n\n"
        "Each card carries its Iconography (Gébelin's Marseille-derived plate), his Egyptian reading (the "
        "Star as Sirius heralding the Nile flood; the Devil as Typhon; the World as Isis and Time; the "
        "Hanged Man, he insists, is printed upside-down and is really Prudence), and a note on the founding "
        "myth. The same 1781 volume carried the Comte de Mellet's companion essay, which first proposed the "
        "Hebrew-letter associations later systematised by Lévi.\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Antoine Court de Gébelin, 'Le Monde Primitif', vol. VIII, "
        "1781 — the 22 engraved 'Atout' plates (Wikimedia Commons, Category:Court de Gébelin tarot), plus "
        "the Monde Primitif suit plates and figure plates."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": img(21),
    "tags": ["tarot", "court-de-gebelin", "book-of-thoth", "egyptian-tarot", "occult",
             "1781", "major-arcana", "public-domain", "history"],
    "roots": ["western-esoteric", "mysticism"],
    "shelves": ["wonder", "mirror", "contested"],
    "lineages": ["Andreotti"],
    "worldview": "esoteric",
    "is_published": False,
    "items": items,
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, "grammar.json"), "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)
print(f"Wrote court-de-gebelin-tarot/grammar.json — {len(items)} items, imaged {sum(1 for it in items if it.get('image_url'))}")
