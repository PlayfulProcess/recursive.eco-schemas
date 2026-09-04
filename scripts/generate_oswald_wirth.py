# -*- coding: utf-8 -*-
"""Generate grammars/oswald-wirth-tarot/grammar.json.

Oswald Wirth's 22 Major Arcana — 'Les 22 Arcanes du Tarot Kabbalistique' (1889),
designed under Stanislas de Guaita and revised as 'Le Tarot des imagiers du Moyen
Age' (1926). Wirth designed only the trumps; he reworked the Tarot de Marseille
imagery and embedded Kabbalistic (Hebrew-letter) and astrological correspondences
following Eliphas Levi. This grammar gives each card: Symbolism, Correspondences
(Hebrew letter + number + astrological association), Upright, and Reversed.

Public domain images: Wikimedia Commons, Category:Oswald Wirth tarot deck
(1889 BnF edition). Verified filenames embedded below.
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "oswald-wirth-tarot")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"


def img(filename):
    return COMMONS + urllib.parse.quote(filename)


def ordinal(n):
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


# num, slug, name, french, hebrew (letter, translit, meaning), astro, symbolism, upright, reversed
CARDS = [
    (0, "le-fou", "The Fool", "Le Fou",
     ("ש", "Shin", "tooth, fire"),
     "the element of Fire; the free spirit unbound by the zodiac",
     "A wanderer in motley strides forward, a bundle on a staff, while a creature tears at his leg and a "
     "crocodile waits ahead. Wirth places the Fool between Judgement and the World — the unnumbered force "
     "of irrational, ungovernable spirit that animates the whole sequence.",
     "Freedom, the impulse to move without calculation, spirit that cannot be domesticated. The energy that "
     "begins and ends the cycle, prior to all numbering.",
     "Aimlessness, madness, dispersion of force; the spirit that scatters instead of advancing."),
    (1, "le-bateleur", "The Magician", "Le Bateleur",
     ("א", "Aleph", "ox"),
     "the planet Mercury; the active, willing principle",
     "A young juggler stands at his table of the four suit-emblems — cup, coin, sword, and baton — one hand "
     "raised toward heaven, one lowered to earth. Wirth's Bateleur is the human will gathering the four "
     "elements into a single creative act.",
     "Will, initiative, mastery of the elements, the spark of conscious action. The number 1: unity, the "
     "self that begins.",
     "Trickery, misused skill, a will turned to manipulation or empty cleverness."),
    (2, "la-papesse", "The High Priestess", "La Papesse",
     ("ב", "Beth", "house"),
     "the Moon; receptive, hidden knowledge",
     "A veiled, enthroned woman holds an open book on her knees, the lunar crescent near her. She is Gnosis — "
     "the secret doctrine, the passive wisdom that receives and conceals rather than acts.",
     "Intuition, latent knowledge, the inner sanctuary. The number 2: duality, reflection, the receptive pole "
     "answering the Magician's will.",
     "Secrets misused, surface piety without depth, knowledge withheld or sterile."),
    (3, "limperatrice", "The Empress", "L'Imperatrice",
     ("ג", "Gimel", "camel"),
     "the planet Venus; generative nature",
     "A winged, crowned woman holds a sceptre and an eagle-emblazoned shield, seated amid abundance. She is "
     "Nature generating forms — the fertile imagination that clothes spirit in matter.",
     "Fecundity, creativity, the flowering of forms, material and intellectual abundance. The number 3: the "
     "synthesis born of the first two.",
     "Sterility, vanity, luxury without fruit, creative energy squandered."),
    (4, "lempereur", "The Emperor", "L'Empereur",
     ("ד", "Daleth", "door"),
     "the planet Jupiter (Aries in later systems); ordering authority",
     "A bearded sovereign sits in profile, one leg crossed in the figure of four, sceptre in hand, the eagle "
     "at his side. He is realised power — spirit given law and structure.",
     "Authority, stability, reason imposing order on matter, the architecture of the will. The number 4: the "
     "stable square, foundation.",
     "Tyranny, rigidity, domination, order hardened into oppression."),
    (5, "le-pape", "The Hierophant", "Le Pape",
     ("ה", "He", "window"),
     "traditionally associated with Taurus; the teaching principle",
     "A tiara'd pontiff blesses two acolytes kneeling before him, the crossed keys at his feet. He is the "
     "bridge — the revealer who mediates between heaven and the seeker.",
     "Teaching, religion, the transmission of doctrine, the link between the human and the divine. The number "
     "5: humanity standing between four elements and spirit.",
     "Dogmatism, hollow orthodoxy, the letter of the law without its spirit."),
    (6, "lamoureux", "The Lovers", "L'Amoureux",
     ("ו", "Vau", "nail, hook"),
     "traditionally associated with Gemini; the trial of choice",
     "A youth stands between two women while a winged Cupid draws his bow above — vice on one side, virtue on "
     "the other. Wirth makes the card a test: the will at the crossroads, forced to choose.",
     "Love, union, but above all moral choice — the freedom and burden of deciding. The number 6: harmony "
     "achieved or the equilibrium that must be chosen.",
     "Indecision, temptation, a union founded on weakness, choice avoided."),
    (7, "le-chariot", "The Chariot", "Le Chariot",
     ("ז", "Zayin", "sword"),
     "traditionally associated with Cancer; triumphant will",
     "A crowned prince rides a canopied chariot drawn by two sphinxes, one black, one white, pulling in "
     "different directions. He governs opposing forces by will alone, holding no reins.",
     "Victory, mastery, the self that holds contrary forces in harness and advances. The number 7: triumph, "
     "the conquest of the elements.",
     "Loss of control, conflict between the forces, a triumph that turns to defeat through pride."),
    (8, "la-justice", "Justice", "La Justice",
     ("ח", "Heth", "fence, field"),
     "traditionally associated with Libra; equilibrium",
     "An enthroned woman holds an upright sword and a level balance, eyes open. She is the law of equilibrium "
     "— measure, consequence, the exact return of every act.",
     "Balance, fairness, accountability, the moral order weighing each thing. The number 8: stability "
     "redoubled, justice as cosmic bookkeeping.",
     "Injustice, imbalance, severity without mercy, judgment distorted."),
    (9, "lermite", "The Hermit", "L'Ermite",
     ("ט", "Teth", "serpent"),
     "traditionally associated with Virgo; prudent wisdom",
     "A cloaked old man walks bearing a lantern half-shielded by his mantle, leaning on a staff. He is "
     "prudence and the inner light, carried carefully through the dark and shared only with care.",
     "Wisdom, introspection, the patient search, the light that guides one step at a time. The number 9: "
     "attainment turned inward, initiation.",
     "Isolation, miserliness with one's light, withdrawal that becomes mere avoidance."),
    (10, "la-roue", "Wheel of Fortune", "La Roue de Fortune",
     ("י", "Yod", "hand"),
     "the planet Jupiter; cyclic destiny",
     "A wheel turns on its axle: a creature rises on one side, another falls on the other, a sphinx with a "
     "sword presides at the top. The eternal rotation of fortune and the law of cycles.",
     "Change, destiny, the turning of circumstance, the rhythm that lifts and lowers. The number 10: a cycle "
     "completed, return to unity on a higher turn.",
     "Bad luck, resistance to change, being dragged by the wheel rather than riding it."),
    (11, "la-force", "Strength", "La Force",
     ("כ", "Kaph", "palm of the hand"),
     "traditionally associated with Leo; mastered force",
     "A serene woman, a lemniscate (the figure of infinity) above her head, calmly closes — or opens — the "
     "jaws of a lion. Strength here is spiritual force quietly governing instinct.",
     "Courage, inner power, the gentle mastery of passion, force directed by spirit rather than violence. "
     "The number 11: mastery beyond the completed decad.",
     "Brute force, domination by appetite, weakness disguised as control."),
    (12, "le-pendu", "The Hanged Man", "Le Pendu",
     ("ל", "Lamed", "ox-goad"),
     "the element of Water; willing reversal",
     "A youth hangs by one foot from a gibbet between two trees, hands behind his back, the free leg crossed; "
     "his face is calm. Wirth reads the inverted posture as voluntary sacrifice and the world seen anew.",
     "Sacrifice, suspension, surrender of the ego, wisdom gained by reversing one's view. The number 12: the "
     "cycle paused for a redemptive pause.",
     "Useless sacrifice, stagnation, a martyrdom that serves no one, attachment refusing to let go."),
    (13, "la-mort", "Death", "La Mort",
     ("מ", "Mem", "water"),
     "traditionally associated with Scorpio; transformation",
     "A skeleton with a scythe mows a field where hands, feet, and crowned heads sprout from the soil. The "
     "card is left unnamed in many decks. Wirth reads it as transformation, not extinction.",
     "Transformation, the clearing-away that makes room for the new, necessary endings. The number 13: the "
     "regenerative force beyond the completed twelve.",
     "Stagnation, fear of change, decay that is resisted instead of composted, mortification without renewal."),
    (14, "la-temperance", "Temperance", "La Temperance",
     ("נ", "Nun", "fish"),
     "traditionally associated with Sagittarius; vital flow",
     "A winged angel pours an unbroken stream of fluid between two vessels. The mingling of waters is the "
     "circulation of the life-force, ceaseless and self-renewing.",
     "Moderation, harmony, the patient blending of opposites, the flow of vital energy. The number 14: "
     "equilibrium kept in motion.",
     "Imbalance, impatience, dissipation, the flow blocked or spilled."),
    (15, "le-diable", "The Devil", "Le Diable",
     ("ס", "Samekh", "prop, support"),
     "traditionally associated with Capricorn; bound force",
     "A horned, bat-winged figure with a torch presides over two small bound figures chained to its pedestal. "
     "Wirth's Devil is the fascination of matter — the magnetic, instinctual force that binds when it is not "
     "mastered.",
     "Instinct, desire, material force, the binding power of appetite — neutral energy that enslaves only "
     "when unconscious. The number 15: force without the light to govern it.",
     "Liberation from bondage, or its opposite: deeper enslavement, obsession, the chains accepted as "
     "comfort."),
    (16, "la-maison-dieu", "The Tower", "Le Feu du Ciel",
     ("ע", "Ayin", "eye"),
     "the planet Mars; sudden upheaval",
     "Lightning strikes the crown from a tower; two figures fall headlong as fire rains down. Wirth titles it "
     "'the Fire of Heaven' — the collapse of false structures struck by a higher force.",
     "Sudden upheaval, the breaking of illusions, liberation through catastrophe, the lightning that clears. "
     "The number 16: the proud edifice undone.",
     "Disaster resisted, a delayed but inevitable collapse, clinging to ruins, catastrophe without learning."),
    (17, "les-etoiles", "The Star", "Les Etoiles",
     ("פ", "Pe", "mouth"),
     "traditionally associated with Aquarius; renewed hope",
     "A naked woman kneels by water, pouring from two urns onto land and stream, beneath a great eight-pointed "
     "star and seven lesser ones. She is hope, nature renewing herself, the gift freely poured.",
     "Hope, inspiration, serenity, the renewal of life and the trust that follows catastrophe. The number "
     "17: the star after the fallen tower.",
     "Despair, disillusion, hope clouded, the waters poured out in vain."),
    (18, "la-lune", "The Moon", "La Lune",
     ("צ", "Tzaddi", "fish-hook"),
     "traditionally associated with Pisces; the dim path",
     "Under a dripping moon two dogs bay while a crayfish climbs from a pool, between two towers. Wirth's Moon "
     "is the realm of illusion, instinct, and the perilous nocturnal path of the soul.",
     "The unconscious, dreams, illusion, the dim and winding path that must be crossed by feeling. The number "
     "18: the deep night before dawn.",
     "Deception, fear, confusion mastering the traveller, illusions taken for truth."),
    (19, "le-soleil", "The Sun", "Le Soleil",
     ("ק", "Qoph", "back of the head"),
     "the Sun; conscious radiance",
     "Two children stand within a walled garden beneath a radiant, human-faced sun. The card is daylight, "
     "consciousness, and the restored innocence that follows the Moon's dark passage.",
     "Joy, clarity, vitality, conscious life, the warmth of attained understanding. The number 19: the lit "
     "world, success and renewal.",
     "Vanity, a clouded sun, false brilliance, happiness that is only on the surface."),
    (20, "le-jugement", "Judgement", "Le Jugement",
     ("ר", "Resh", "head"),
     "the element of Fire; awakening",
     "An angel sounds a trumpet from the clouds; below, the dead rise from a tomb with arms raised. Wirth "
     "reads it as awakening — the call to a higher life, regeneration of the whole being.",
     "Awakening, renewal, the call to rise, a decisive summons answered. The number 20: resurrection, the "
     "self reborn to a new octave.",
     "Stagnation, a call refused, fear of change, the trumpet unheard."),
    (21, "le-monde", "The World", "Le Monde",
     ("ת", "Tav", "mark, cross"),
     "the planet Saturn; completion",
     "A dancing figure within a laurel wreath is surrounded by the four living creatures — man, eagle, lion, "
     "and bull, the four fixed signs and the four elements. It is the completed Great Work, totality realised.",
     "Completion, fulfilment, integration, the cosmos harmonised and the journey closed. The number 21: the "
     "final synthesis, the Work accomplished.",
     "Incompletion, a goal almost but not reached, a cycle that fails to close, attachment to the journey "
     "instead of its end."),
]

# Verified Commons filenames (1889 BnF edition), keyed by card number.
WIRTH_FILES = {
    0: "00 Le Fou, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    1: "01 Le Bateleur, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    2: "02 La Papesse, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    3: "03 L'Imperatrice, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    4: "04 L'Empereur, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    5: "05 Le Pape, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    6: "06 L'Amoureux, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    7: "07 Le Chariot, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    8: "08 La Justice, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    9: "09 L'Ermite, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    10: "10 La Roue de Fortune, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    11: "11 La Force, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    12: "12 Le Pendu, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    13: "13 La Mort, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    14: "14 La Temperance, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    15: "15 Le Diable, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    16: "16 Le Feu du Ciel, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    17: "17 Les Etoiles, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    18: "18 La Lune, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    19: "19 Le Soleil, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    20: "20 Le Jugement, Oswald Wirth Tarot Deck 1889 BnF.jpg",
    21: "21 Le Monde, Oswald Wirth Tarot Deck 1889 BnF.jpg",
}

items = []
for i, (num, slug, name, french, (heb, translit, meaning), astro, sym, up, rev) in enumerate(CARDS):
    fn = WIRTH_FILES[num]
    u = img(fn)
    corr = (f"**Hebrew letter:** {heb} ({translit}, '{meaning}') — the {ordinal(num) if num else 'unnumbered'} "
            f"letter in Eliphas Levi's attribution that Wirth follows.\n\n"
            f"**Number:** {num}.\n\n"
            f"**Astrological association:** {astro}.")
    items.append({
        "id": f"arcanum-{num:02d}-{slug}",
        "name": f"{num} — {name}",
        "sort_order": i,
        "category": "major-arcana",
        "level": 1,
        "keywords": [name.lower().replace("the ", ""), french.lower(), translit.lower(),
                     "major arcana", "esoteric"],
        "image_url": u,
        "metadata": {
            "arcana": "major", "number": num, "french_name": french,
            "hebrew_letter": heb, "hebrew_translit": translit,
            "illustrations": [{
                "url": u, "artist": "Oswald Wirth", "artist_dates": "1860–1943",
                "edition": "Les 22 Arcanes du Tarot Kabbalistique, 1889 (BnF copy)",
                "scene": f"{name} ({french})", "license": "Public Domain", "is_primary": True,
            }],
        },
        "sections": {
            "Symbolism": sym,
            "Correspondences": corr,
            "Upright": up,
            "Reversed": rev,
        },
    })

# L2 emergence: the whole esoteric sequence
items.append({
    "id": "emg-the-great-work",
    "name": "The Major Arcana as the Great Work",
    "sort_order": len(items),
    "category": "emergence",
    "level": 2,
    "composite_of": [it["id"] for it in items if it["category"] == "major-arcana"],
    "relationship_type": "emergence",
    "image_url": img("Les 22 Arcanes du Tarot Kabbalistique.jpg"),
    "metadata": {},
    "sections": {
        "About the Sequence": "For Wirth, following Eliphas Levi, the 22 trumps are not a random gallery but "
        "a single initiatory ladder mapped onto the 22 letters of the Hebrew alphabet and the paths of the "
        "Kabbalistic Tree of Life. The Magician's will descends through nature, authority, choice, and trial; "
        "is tested by the Wheel, Death, and the Tower; and is reborn through the Star, Sun, and Judgement to "
        "the completed World. The Fool moves through all of it as the ungovernable spirit.",
        "How to Read It": "Trace the cards in order as the soul's progress, or pair them across the sequence "
        "(Magician and World, Popess and Moon, Empress and Star) to see Wirth's symmetries. This is esoteric "
        "tarot in its Continental form — the bridge from the medieval Marseille image to the English decks "
        "that followed.",
    },
})

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Oswald Wirth", "date": "1889 / 1926",
             "note": "Designer of the 22 Major Arcana; 'Les 22 Arcanes du Tarot Kabbalistique' (1889) and "
                     "'Le Tarot des imagiers du Moyen Age' (1926)"},
            {"name": "Stanislas de Guaita", "date": "1889",
             "note": "Commissioned and guided the original deck"},
            {"name": "Eliphas Levi", "date": "1850s",
             "note": "Source of the Hebrew-letter and Kabbalistic attributions Wirth follows"},
            {"name": "Wikimedia Commons / Bibliotheque nationale de France", "date": "public domain",
             "note": "Card images, Category:Oswald Wirth tarot deck (1889 BnF edition)"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture and esoteric summaries"},
        ],
    },
    "name": "Oswald Wirth Tarot — The 22 Esoteric Arcana (1889 / 1926)",
    "description": (
        "The hinge of esoteric tarot. In 1889 the Swiss occultist Oswald Wirth (1860–1943), working under "
        "Stanislas de Guaita and drawing on Eliphas Levi, designed a deck of 22 Major Arcana — "
        "'Les 22 Arcanes du Tarot Kabbalistique' — and revised it in 1926 as 'Le Tarot des imagiers du Moyen "
        "Age'. Wirth designed only the trumps. He kept the medieval Tarot de Marseille imagery but reworked "
        "it deliberately, embedding Kabbalistic and astrological symbols so that each card became a key on "
        "the Tree of Life.\n\n"
        "Wirth's deck is the bridge between the French occult revival (Court de Gebelin, Levi, Papus) and the "
        "English esoteric decks that followed (Golden Dawn, Rider-Waite-Smith, Thoth). Each card here carries "
        "its Symbolism (what Wirth drew and why), Correspondences (its Hebrew letter, number, and "
        "astrological association in the Continental tradition Wirth follows), and Upright and Reversed "
        "readings.\n\n"
        "Note that this is the Continental attribution, in which the unnumbered Fool is placed between "
        "Judgement (20) and the World (21) and assigned the letter Shin — differing from the later "
        "Golden Dawn arrangement. Source images: Wikimedia Commons, 1889 BnF edition (public domain; "
        "Wirth died in 1943).\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Oswald Wirth, 'Les 22 Arcanes du Tarot Kabbalistique', 1889, "
        "Bibliotheque nationale de France copy (Wikimedia Commons, Category:Oswald Wirth tarot deck) — "
        "engraved line-and-colour majors in the reworked Marseille style. The 1926 revision adds astrological "
        "and Hebrew-letter glyphs to each card border."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": img("Oswald Wirth - Les 22 Arcanes du Tarot Kabbalistique.jpg"),
    "tags": ["tarot", "oswald-wirth", "esoteric", "kabbalah", "major-arcana",
             "occult", "eliphas-levi", "public-domain", "1889"],
    "roots": ["western-esoteric", "mysticism"],
    "shelves": ["wonder", "mirror"],
    "lineages": ["Andreotti"],
    "worldview": "esoteric",
    "is_published": False,
    "items": items,
}

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "grammar.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)
print(f"Wrote {out_path}")
print(f"  total items: {len(items)}  (22 arcana + 1 emergence)")
print(f"  with image_url: {sum(1 for it in items if it.get('image_url'))}")
