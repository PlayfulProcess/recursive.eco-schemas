# -*- coding: utf-8 -*-
"""Generate grammars/tarot-de-marseille-conver/grammar.json.

The Tarot de Marseille in Nicolas Conver's 1760 woodcut edition — the canonical
printed standard that fixed the 22 trump names, numbers, and images for the whole
occult era. Full 78-card deck: 22 majors (imaged from Conver 1760, with
Iconography / Upright / Reversed) + 56 minors (traditional cartomantic meanings;
Marseille pips are non-scenic, so images are sparse on Commons and attached only
where they exist).

Note the PRE-Golden-Dawn order this deck fixes: Justice = VIII, Strength = XI,
the unnumbered Fool (Le Mat), and Death (XIII) left unnamed.

Images: Wikimedia Commons, Category:Tarot de Marseille - Nicolas Conver 1760 (PD).
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "tarot-de-marseille-conver")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"


def img(filename):
    return COMMONS + urllib.parse.quote(filename) if filename else None


# Honest per-card caveat: the Marseille was a GAME deck, not a divination deck.
TRADITION_NOTE = (
    "The Tarot de Marseille was made to play *tarot*, a trick-taking card game "
    "(the ancestor of today's French Tarot and the central-European Tarock games) "
    "— not for divination. The upright and reversed meanings here are a later "
    "overlay, added by Etteilla and the occultists from the 1780s onward; they are "
    "not part of the deck's original tradition."
)


# num, slug, name, french, filename, iconography, upright, reversed
MAJORS = [
    (0, "le-mat", "The Fool", "Le Mat", "LE MAT Nicolas Conver Tarot 1760.jpg",
     "A traveller in motley walks rightward with a staff and bundle, a small animal tearing at his "
     "trailing leg. He alone carries no number — outside the count.",
     "Beginnings, wandering, freedom, the leap taken without calculation; the unattached spirit moving on.",
     "Folly, heedlessness, dispersion; movement without direction or commitment."),
    (1, "le-bateleur", "The Magician", "Le Bateleur", "I LE BATELEUR Nicolas Conver Tarot 1760.jpg",
     "A young mountebank stands at a table of cups, coins, and knives, a wand in one hand, his hat brim a "
     "lemniscate. The lowest trump, the everyman entertainer.",
     "Skill, initiative, the will gathering its tools, a beginning in the maker's hands.",
     "Trickery, false starts, cleverness without substance, manipulation."),
    (2, "la-papesse", "The High Priestess", "La Papesse", "II LA PAPESSE Nicolas Conver Tarot 1760.jpg",
     "A seated, veiled woman in papal tiara holds an open book, a curtain behind her.",
     "Hidden knowledge, intuition, patience, the wisdom that waits and conceals.",
     "Secrets misused, surface knowledge, withdrawal, sterile silence."),
    (3, "limperatrice", "The Empress", "L'Impératrice", "II L'IMPÉRATRICE Nicolas Conver Tarot 1760.jpg",
     "A crowned woman enthroned with sceptre and an eagle shield. (Conver's block mislabels her 'II'; she "
     "is trump III.)",
     "Abundance, fertility, creativity, worldly feminine authority and the flowering of forms.",
     "Vanity, sterility, smothering, creativity blocked or squandered."),
    (4, "lempereur", "The Emperor", "L'Empereur", "IIII-L'EMPEREUR Nicolas Conver Tarot 1760.jpg",
     "A bearded sovereign sits in profile, legs crossed in the figure of four, sceptre and eagle shield at "
     "hand.",
     "Authority, structure, stability, reason giving the world its order.",
     "Domination, rigidity, tyranny, order hardened into oppression."),
    (5, "le-pape", "The Hierophant", "Le Pape", "V LE PAPE Nicolas Conver Tarot 1760.jpg",
     "A tiara'd pope raises his hand in blessing over two tonsured clerics, a pillar at each side.",
     "Teaching, tradition, blessing, the bridge between the human and the sacred.",
     "Dogma, empty orthodoxy, conformity, the letter without the spirit."),
    (6, "lamoureux", "The Lovers", "L'Amoureux", "VI L'AMOUREUX Nicolas Conver Tarot 1760.jpg",
     "A youth stands between two women under a blindfolded Cupid drawing his bow — the choice between two "
     "ways.",
     "Love, union, and above all a choice that must be made; the heart at a crossroads.",
     "Indecision, temptation, a union founded on weakness, choice deferred."),
    (7, "le-chariot", "The Chariot", "Le Chariot", "VII LE CHARIOT Nicolas Conver Tarot 1760.jpg",
     "A crowned prince stands in a canopied chariot drawn by two horses facing different ways; he holds no "
     "reins.",
     "Victory, drive, mastery, holding opposing forces together and advancing by will.",
     "Loss of control, conflict, a triumph undone by pride or haste."),
    (8, "la-justice", "Justice", "La Justice", "VIII LA JUSTICE Nicolas Conver Tarot 1760.jpg",
     "An enthroned woman holds an upright sword and a level balance, eyes open. In this deck she is VIII.",
     "Balance, fairness, consequence, the exact weighing of each act.",
     "Injustice, imbalance, severity, judgment distorted or evaded."),
    (9, "lhermite", "The Hermit", "L'Hermite", "VIIII L'HERMITE Nicolas Conver Tarot 1760.jpg",
     "A cloaked old man walks with a staff, lifting a lantern half-shielded by his cloak.",
     "Solitude, prudence, the inner light, the patient search carried one step at a time.",
     "Isolation, withdrawal that avoids, a light hoarded or refused."),
    (10, "la-roue", "Wheel of Fortune", "La Roue de Fortune", "X LA ROUE DE FORTUNE Nicolas Conver Tarot 1760.jpg",
     "A wheel on a frame turns: animal-eared creatures rise on one side and fall on the other, a sphinx-like "
     "figure crowning the top.",
     "Change, cycles, fortune turning, the moment of luck or reversal.",
     "Bad turns, resistance to change, being dragged by the wheel."),
    (11, "la-force", "Strength", "La Force", "XI LA FORCE Nicolas Conver Tarot 1760.jpg",
     "A woman in a wide hat calmly parts the jaws of a lion. In this deck Strength is XI.",
     "Courage, gentle mastery of instinct, force governed by spirit rather than violence.",
     "Brute force, domination by appetite, weakness disguised as control."),
    (12, "le-pendu", "The Hanged Man", "Le Pendu", "XII LE PENDU Nicolas Conver Tarot 1760.jpg",
     "A youth hangs by one ankle from a wooden frame between two trees, hands behind his back, leg crossed; "
     "his face is calm.",
     "Suspension, sacrifice, surrender, the world seen from a reversed point of view.",
     "Useless sacrifice, stagnation, martyrdom that serves no one."),
    (13, "la-mort", "Death", "La Mort", "13 XIII Nicolas Conver Tarot 1760.jpg",
     "A skeleton with a scythe mows a black ground from which hands, feet, and crowned heads sprout. The "
     "card bears its number XIII but no name.",
     "Transformation, the necessary clearing-away, endings that make room.",
     "Stagnation, fear of change, decay resisted instead of released."),
    (14, "temperance", "Temperance", "Tempérance", "XIIII TEMPERANCE Nicolas Conver Tarot 1760.jpg",
     "A winged angel pours liquid between two vessels in an unbroken stream.",
     "Moderation, harmony, the patient blending of opposites, the flow of life renewed.",
     "Imbalance, impatience, dissipation, the flow spilled or blocked."),
    (15, "le-diable", "The Devil", "Le Diable", "XV LE DIABLE Nicolas Conver Tarot 1760.jpg",
     "A horned, bat-winged figure on a pedestal raises a torch; two small horned captives are chained "
     "below.",
     "Instinct, desire, bondage, the magnetic pull of matter and appetite — energy that enslaves when "
     "unconscious.",
     "Release from bondage, or deeper enslavement: obsession, the chains embraced."),
    (16, "la-maison-dieu", "The Tower", "La Maison Dieu", "XVI LA MAISON DE DIEU Nicolas Conver Tarot 1760.jpg",
     "Lightning knocks the crown from a tower; two figures fall headlong amid coloured spheres. Its name, "
     "'the House of God', is older than 'the Tower'.",
     "Sudden upheaval, the breaking of false structures, liberation through shock.",
     "Disaster resisted, a collapse delayed but coming, clinging to ruins."),
    (17, "letoile", "The Star", "L'Étoile", "XVII L'ETOILE Nicolas Conver Tarot 1760.jpg",
     "A naked woman kneels by water pouring two urns onto land and stream, a great star and seven smaller "
     "ones above.",
     "Hope, renewal, serenity, the gift freely poured after the storm.",
     "Despair, disillusion, hope clouded, the waters poured in vain."),
    (18, "la-lune", "The Moon", "La Lune", "XVIII LA LUNE Nicolas Conver Tarot 1760.jpg",
     "Under a dripping face-moon two dogs bay between two towers while a crayfish climbs from a pool.",
     "The unconscious, dreams, illusion, the dim and winding path crossed by feeling.",
     "Deception, fear, confusion, illusions mistaken for truth."),
    (19, "le-soleil", "The Sun", "Le Soleil", "XVIIII LE SOLEIL Nicolas Conver Tarot 1760.jpg",
     "Two children stand by a low wall beneath a great rayed face-sun that drips golden tears.",
     "Joy, clarity, vitality, the warmth of conscious understanding and shared life.",
     "Vanity, false brightness, a clouded sun, happiness only on the surface."),
    (20, "le-jugement", "Judgement", "Le Jugement", "XX LE JUGEMENT Nicolas Conver Tarot 1760.jpg",
     "An angel sounds a trumpet from the clouds; three figures rise from a tomb with arms raised.",
     "Awakening, renewal, a decisive call answered, the self risen to new life.",
     "Stagnation, a call refused, fear of change, the trumpet unheard."),
    (21, "le-monde", "The World", "Le Monde", "XXI LE MONDE Nicolas Conver Tarot 1760.jpg",
     "A dancing figure within a pointed-oval wreath, the four living creatures — angel, eagle, lion, bull — "
     "in the corners.",
     "Completion, fulfilment, integration, the world harmonised and the journey closed.",
     "Incompletion, a goal almost reached, a cycle that fails to close."),
]

# The only two Marseille pip images present in the Conver category.
PIP_IMAGES = {
    ("Batons", 1): "As BATON Nicolas Conver Tarot 1760.jpg",
    ("Swords", 1): "As ÉPÉE Nicolas Conver Tarot 1760.jpg",
}

SUITS = [
    ("coins", "Coins", "Deniers", "Earth", "money, body, work, and the material world"),
    ("cups", "Cups", "Coupes", "Water", "love, feeling, and the inner life"),
    ("swords", "Swords", "Épées", "Air", "mind, conflict, decision, and the cut of judgment"),
    ("batons", "Batons", "Bâtons", "Fire", "will, work, enterprise, and growth"),
]
# Traditional cartomantic pip meanings (suit-agnostic spine, coloured by suit).
PIP = {
    1: ("the pure root and seed of the suit, a new force entering",
        "a fresh start, the suit's energy at its purest and most potent",
        "a false start, energy blocked at the source"),
    2: ("pairing and exchange", "balance, partnership, a choice held in equilibrium",
        "division, imbalance, a partnership strained"),
    3: ("first growth", "increase, collaboration, early success",
        "delay, growth stalled, effort scattered"),
    4: ("stability", "foundation, rest, consolidation, a settled position",
        "stagnation, rigidity, security clung to"),
    5: ("loss and tension", "conflict, difficulty, the testing of the suit",
        "the easing of conflict, or loss deepened"),
    6: ("harmony", "reciprocity, ease, a balance restored",
        "imbalance returning, harmony lost"),
    7: ("striving", "effort against resistance, partial and uncertain gain",
        "struggle abandoned, effort wasted"),
    8: ("movement", "change, swiftness, energy in motion",
        "blockage, stalled movement, scattered force"),
    9: ("near-fullness", "intensity at its height, the suit almost complete",
        "strain, overreach, intensity turned against itself"),
    10: ("completion", "the suit in full — its plenty and its weight together",
         "burden, excess, a cycle that overstays"),
}
COURTS = [
    ("page", "Page", "Valet", "the youth and messenger of the suit — its energy learning, curious"),
    ("knight", "Knight", "Cavalier", "the suit in motion — questing, active, riding out"),
    ("queen", "Queen", "Reine", "the inward mastery of the suit — it held and understood"),
    ("king", "King", "Roi", "the outward authority of the suit — it commanded and ruled"),
]


def ord_word(n):
    return {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
            7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}[n]


items = []
so = 0
for num, slug, name, french, fn, icon, up, rev in MAJORS:
    u = img(fn)
    items.append({
        "id": f"major-{num:02d}-{slug}", "name": f"{num} — {name}", "sort_order": so,
        "category": "major-arcana", "level": 1,
        "keywords": [name.lower().replace("the ", ""), french.lower(), "major arcana", "marseille"],
        "image_url": u,
        "metadata": {
            "arcana": "major", "number": num, "french_name": french,
            "illustrations": [{
                "url": u, "artist": "Nicolas Conver", "artist_dates": "fl. 1760, Marseille",
                "edition": "Tarot de Marseille, Nicolas Conver, 1760 (woodcut)",
                "scene": f"{name} ({french})", "license": "Public Domain", "is_primary": True,
            }],
        },
        "sections": {"Iconography": icon, "Upright": up, "Reversed": rev},
    })
    so += 1

for sid, sdisp, sfr, element, theme in SUITS:
    for n in range(1, 11):
        word = ord_word(n)
        spine, up, rev = PIP[n]
        fn = PIP_IMAGES.get((sdisp, n))
        u = img(fn)
        it = {
            "id": f"{sid}-{'ace' if n==1 else f'{n:02d}'}", "name": f"{word} of {sdisp}",
            "sort_order": so, "category": f"suit-{sid}", "level": 1,
            "keywords": [sdisp.lower(), element.lower(), word.lower(), "minor arcana", sfr.lower()],
            "metadata": {"arcana": "minor", "suit": sdisp, "suit_french": sfr, "element": element,
                         "rank": word},
            "sections": {
                "Iconography": (f"{word} of {sdisp}: {('a single' if n==1 else str(n))} "
                                f"{sdisp.lower()[:-1] if sdisp.endswith('s') else sdisp.lower()}"
                                f"{'' if n==1 else 's'} laid out in the woodcut's symmetrical pattern, "
                                f"with floral scrollwork between them. Marseille pips are emblematic, "
                                f"not scenic."),
                "Upright": f"{up} — within {theme}.",
                "Reversed": f"{rev}.",
            },
        }
        if u:
            it["image_url"] = u
            it["metadata"]["illustrations"] = [{
                "url": u, "artist": "Nicolas Conver", "artist_dates": "fl. 1760, Marseille",
                "edition": "Tarot de Marseille, Nicolas Conver, 1760 (woodcut)",
                "scene": f"{word} of {sdisp}", "license": "Public Domain", "is_primary": True}]
        items.append(it)
        so += 1
    for rid, rdisp, rfr, role in COURTS:
        items.append({
            "id": f"{sid}-{rid}", "name": f"{rdisp} of {sdisp}", "sort_order": so,
            "category": f"suit-{sid}", "level": 1,
            "keywords": [sdisp.lower(), element.lower(), rdisp.lower(), "court card", rfr.lower()],
            "metadata": {"arcana": "minor", "suit": sdisp, "suit_french": sfr, "element": element,
                         "rank": rdisp, "court": True},
            "sections": {
                "Iconography": (f"{rdisp} of {sdisp} ({rfr}): a standing or seated court figure of the "
                                f"Marseille pattern bearing the {sdisp.lower()[:-1] if sdisp.endswith('s') else sdisp.lower()} "
                                f"emblem, in the flat bold colours of the woodcut."),
                "Upright": f"{rdisp} of {sdisp} — {role}, within {theme}.",
                "Reversed": f"The same energy obstructed, immature, or turned against itself.",
            },
        })
        so += 1

# L2 emergences
all_ids = {it["id"] for it in items}
major_ids = [it["id"] for it in items if it["category"] == "major-arcana"]
emgs = [
    ("emg-majors", "The 22 Trumps — The Marseille Standard", major_ids,
     img("XXI LE MONDE Nicolas Conver Tarot 1760.jpg"),
     {"About the Trumps": "Conver's 1760 trumps are the images the whole occult era treated as canonical. "
      "This is the deck Court de Gébelin theorised over, Etteilla read from, and Lévi and Wirth re-symbolised. "
      "Note the order it fixes: the unnumbered Fool, Justice at VIII, Strength at XI, and Death (XIII) left "
      "unnamed — all of which the later Golden Dawn would alter.",
      "How to Use": "Read the trumps as the standard reference sequence against which every later esoteric "
      "deck defined itself."}),
]
for sid, sdisp, sfr, element, theme in SUITS:
    kids = [it["id"] for it in items if it["category"] == f"suit-{sid}"]
    emgs.append((f"emg-suit-{sid}", f"Suit of {sdisp} ({sfr}) — {element}", kids,
                 img(PIP_IMAGES.get((sdisp, 1))) or img("As BATON Nicolas Conver Tarot 1760.jpg"),
                 {"About this Suit": f"The {sdisp} ({sfr}) of the Marseille — the suit of {element}. Its pips "
                  f"are emblematic woodcut arrangements rather than the scenic pictures the later "
                  f"Rider-Waite-Smith would invent.",
                  "How to Use": f"Read the suit for {theme.split(',')[0]} — using the traditional cartomantic "
                  f"meanings rather than scene-reading."}))
for eid, ename, kids, image_url, sections in emgs:
    kids = [k for k in kids if k in all_ids]
    items.append({"id": eid, "name": ename, "sort_order": so, "category": "emergence", "level": 2,
                  "composite_of": kids, "relationship_type": "emergence",
                  "image_url": image_url, "metadata": {}, "sections": sections})
    so += 1

# Add the honest "game, not divination" note as the last section on every card.
for it in items:
    if it.get("category") != "emergence":
        it["sections"]["Tradition Note"] = TRADITION_NOTE

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Nicolas Conver", "date": "1760",
             "note": "Master cardmaker of Marseille; his woodcut Tarot fixed the canonical TdM pattern"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "Card images, Category:Tarot de Marseille - Nicolas Conver 1760"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture; traditional cartomantic summaries"},
        ],
    },
    "name": "Tarot de Marseille — Nicolas Conver 1760 (The Printed Standard)",
    "description": (
        "The deck the whole occult era treated as canonical. Printed from woodblocks by the master "
        "cardmaker Nicolas Conver in Marseille in 1760, this is the most reproduced version of the Tarot de "
        "Marseille — the standardised pattern that fixed the 22 trumps' names, numbers, and images for "
        "centuries. Crucially, it was made to PLAY a game: tarot, a trick-taking card game (the ancestor of "
        "today's French Tarot and the central-European Tarock games), in which the 22 trumps are a permanent "
        "trump suit and the Fool (Le Mat) is the 'Excuse'. It was never meant for divination — the reading "
        "meanings here are a later overlay. It is the bridge between the Italian game decks and the French occult revival: the deck "
        "Court de Gébelin theorised over, Etteilla read fortunes from, and Lévi and Oswald Wirth "
        "re-symbolised.\n\n"
        "This grammar holds the full 78-card deck. The 22 majors are imaged from Conver's 1760 woodcuts, "
        "each with an Iconography note and traditional Upright / Reversed meanings. The 56 minors carry the "
        "traditional cartomantic meanings; because Marseille pips are emblematic rather than scenic (unlike "
        "the later Rider-Waite-Smith), few pip scans exist on Commons, so most pip images are left for a "
        "later illustration pass.\n\n"
        "Note the PRE-Golden-Dawn order this deck fixes, and which later English decks changed: the "
        "unnumbered Fool (Le Mat), Justice at VIII, Strength (La Force) at XI, and Death (XIII) left "
        "unnamed.\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Nicolas Conver, Tarot de Marseille, 1760, woodcut with "
        "stencil colour (Wikimedia Commons, Category:Tarot de Marseille - Nicolas Conver 1760). For a fuller "
        "pip set, the Jean Dodal (1701) and Jean Noblet (c. 1650) Marseille decks are also public domain."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": img("Nicolas Conver Tarot 1760.jpg"),
    "tags": ["tarot", "marseille", "nicolas-conver", "1760", "woodcut", "major-arcana",
             "public-domain", "cartomancy", "printed-standard"],
    "roots": ["western-esoteric"],
    "shelves": ["wonder", "mirror"],
    "lineages": ["Andreotti"],
    "worldview": "traditional",
    "is_published": False,
    "items": items,
}

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "grammar.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)
print(f"Wrote {out_path}")
print(f"  items: {len(items)}  with image_url: {sum(1 for it in items if it.get('image_url'))}")
