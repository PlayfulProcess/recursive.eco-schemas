# -*- coding: utf-8 -*-
"""Generate grammars/tree-of-tarot/grammar.json — the genealogical meta-grammar.

A "grammar of tarot grammars": the items ARE the decks/traditions, arranged so the
recursive.eco tree-viewer (pages/tree-viewer.html) renders the family tree of tarot
with no new frontend. L1 = decks, L2 = branches (Dummett's A/B/C trump-orders + the
occult reframing + sui-generis offshoots), L3 = the root "The Tree of Tarot".

Scholarly backbone: Michael Dummett's A/B/C classification of trump orders.
Marseille (C-order, Milan/West) and the Bolognese Tarocchino (A-order, South) are
COUSINS — both descend from the mid-1400s Italian trionfi — not parent and child.
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "tree-of-tarot")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"


def img(fn):
    return COMMONS + urllib.parse.quote(fn) if fn else None


# L2 branches: (id, name, blurb)
BRANCHES = [
    ("branch-roots", "Roots — The First Tarots (Milan, c. 1440s)",
     "The earliest surviving tarots: luxurious hand-painted decks made for the Visconti and Sforza "
     "courts of Milan. Tarot begins here as a card GAME (trionfi), not divination. These Milanese decks "
     "seed what Dummett calls the C-order."),
    ("branch-a", "A-Order — Bologna & Florence (the South)",
     "One of the three regional trump orders (Dummett's A). The southern tradition, home of the Bolognese "
     "Tarocchino and the vast Florentine Minchiate. Note the four interchangeable 'Papi' replacing the "
     "Popess/Empress/Emperor/Pope."),
    ("branch-b", "B-Order — Ferrara (the East)",
     "The eastern trump order (Dummett's B), associated with the d'Este court of Ferrara. Known mostly "
     "from fragments and the so-called 'Charles VI' deck."),
    ("branch-c", "C-Order — Milan & the West → the Printed Standard",
     "The western trump order (Dummett's C) that, through Milan and France, became the printed STANDARD — "
     "the Tarot de Marseille — and its regional cousins. This is the trunk from which the occult decks branch."),
    ("branch-occult", "The Occult Reframing (France → England, 1781→)",
     "From the 1780s the Tarot de Marseille was reinterpreted as ancient esoteric wisdom — Court de Gébelin's "
     "Egyptian myth, Etteilla's cartomancy, Lévi's Kabbalah, and then the English decks (Golden Dawn, "
     "Rider-Waite-Smith, Thoth). Divination is INVENTED on this branch."),
    ("branch-sui", "Sui Generis & Relatives",
     "Decks that stand apart from the three orders, plus the relatives constantly confused with tarot: the "
     "alchemical Sola Busca, the Mantegna 'Tarocchi' (not actually a tarot), and the modern derivative decks."),
]

# L1 decks: (id, name, branch, when, what, lineage, status, derives_from, cover)
D = [
    # --- Roots ---
    ("visconti-sforza", "Visconti-Sforza Tarot", "branch-roots", "Milan, c. 1451",
     "The oldest near-complete tarot — 74 of 78 cards survive, painted by the Bembo workshop for the dukes "
     "of Milan. A game deck; four cards (Devil, Tower, Knight of Coins, Three of Swords) are lost.",
     "Seeds the C-order. Sister to the Cary-Yale and Brera-Brambilla decks.",
     "✅ Built in this library (grammars/visconti-sforza-tarot).", [], "Viscontisforzatarot.jpg"),
    ("cary-yale", "Cary-Yale (Visconti di Modrone)", "branch-roots", "Milan, c. 1442",
     "The most lavish hand-painted tarot, with SIX courts per suit (incl. female Horsewoman & Damsel) and "
     "the unique theological virtues Faith, Hope, Charity.",
     "A root deck; its idiosyncrasies (extra virtues, six courts) show how unsettled the early form was.",
     "✅ Built (grammars/cary-yale-visconti-tarot).", [], "Cary-Yale Tarot deck - Damsel of Swords.jpg"),
    ("brera-brambilla", "Brera-Brambilla", "branch-roots", "Milan, c. 1442",
     "The third Bembo sister deck, surviving only as a fragment (~48 cards, just two trumps).",
     "A root deck; fills out the Milanese hand-painted group.",
     "🔨 Planned (image-poor; needs museum scans).", [], None),
    # --- A-order ---
    ("tarocchino-bologna", "Tarocchino di Bologna", "branch-a", "Bologna, 16th c.→",
     "The 62-card Bolognese game deck (pips 2–5 removed), with the distinctive four 'Papi' and the A-order "
     "trump sequence. The living southern game tradition.",
     "A-order. A COUSIN of the Marseille, not its ancestor — both descend from the common Italian root.",
     "✅ Built in this library (grammars/tarocchino-bologna) — structure-accurate; per-card images TODO.",
     ["italian-trionfi"], "Tarocco Bolognese.png"),
    ("minchiate", "Minchiate (Florence)", "branch-a", "Florence, 16th c.→",
     "The 97-card Florentine expansion — adds the four elements, twelve zodiac signs, and the full set of "
     "seven virtues, plus five supreme 'Arie'.",
     "A-order (Florentine). The most cosmological tarot.",
     "✅ Built (grammars/minchiate-florence-tarot).", ["italian-trionfi"],
     "Minchiate card deck - Florence - 1860-1890 - Trumps - 40 - Le Trombe.jpg"),
    ("tarocco-siciliano", "Tarocco Siciliano", "branch-a", "Sicily, 18th c.→",
     "Sicily's small, unusual deck, with cards found nowhere else (the 'Fugitivo' and 'Miseria').",
     "A-order offshoot, the southernmost branch.",
     "🔨 Planned.", ["italian-trionfi"], None),
    # --- B-order ---
    ("charles-vi", "'Charles VI' / Gringonneur", "branch-b", "Ferrara/Bologna, c. 1450–80",
     "A hand-painted deck of which 17 trumps survive at the BnF. Long mis-called the oldest tarot (and "
     "wrongly tied to a 1392 payment to Gringonneur).",
     "B-order (Ferrarese). A documentary cornerstone of the eastern tradition.",
     "✅ Built in this library (grammars/charles-vi-tarot).", ["italian-trionfi"], "Empereur tarot charles6.jpg"),
    ("este", "d'Este Tarot", "branch-b", "Ferrara, 15th c.",
     "Fragmentary hand-painted cards from the Este court of Ferrara.",
     "B-order. Completes the eastern luxury-deck picture beside Visconti's western ones.",
     "🔨 Planned.", ["italian-trionfi"], None),
    # --- C-order ---
    ("marseille-conver", "Tarot de Marseille — Conver 1760", "branch-c", "Marseille, 1760",
     "The canonical printed standard (Type II), a woodcut game deck whose 22 trumps fixed the names and "
     "images the whole occult era inherited.",
     "C-order, the trunk. Descends from the Milanese standard; everything occult branches from it.",
     "✅ Built (grammars/tarot-de-marseille-conver).", ["visconti-sforza"], "Nicolas Conver Tarot 1760.jpg"),
    ("marseille-type1", "Marseille Type I — Noblet / Dodal", "branch-c", "Paris/Lyon, 1650–1701",
     "The earlier Marseille pattern (Jean Noblet c. 1650, Jean Dodal 1701), slightly different from the "
     "later Conver 'Type II'.",
     "C-order. The first crystallisation of the Marseille image.",
     "🔨 Planned (fuller PD pip scans live here).", ["visconti-sforza"], None),
    ("besancon", "Tarot de Besançon / Swiss 1JJ", "branch-c", "Switzerland/E. France, 18th c.",
     "A Marseille variant that replaces the Popess and Pope with Juno and Jupiter — a Protestant-friendly "
     "redesign.",
     "C-order sibling of the Marseille.",
     "✅ Built (partial, variant highlights) — grammars/tarot-de-besancon.", ["marseille-conver"],
     "Tarot 1JJ - Junon - 1. Version.png"),
    ("belgian", "Belgian / Vandenborre Tarot", "branch-c", "Brussels, 18th c.",
     "The Flemish 'Tarot de Vandenborre', replacing the Popess and Pope with Bacchus and the Spanish "
     "Captain (Capitano Eracasse).",
     "C-order sibling of the Marseille.",
     "🔨 Planned.", ["marseille-conver"], None),
    ("piemontese", "Tarocco Piemontese", "branch-c", "Piedmont, 19th c.→",
     "The Piedmontese playing pattern, a later Italian descendant of the Marseille type.",
     "C-order, the living Italian game pattern.",
     "🔨 Planned.", ["marseille-conver"], None),
    # --- Occult ---
    ("court-de-gebelin", "Court de Gébelin's Plates", "branch-occult", "Paris, 1781",
     "Antoine Court de Gébelin's engravings in 'Le Monde primitif', which first claimed the tarot was the "
     "ancient Egyptian 'Book of Thoth'. The myth that launched occult tarot.",
     "The hinge: re-reads the C-order Marseille as esoteric wisdom.",
     "✅ Built in this library (grammars/court-de-gebelin-tarot).", ["marseille-conver"], "Court de Gébelin - Atout 21.jpg"),
    ("etteilla-i", "Etteilla I — Livre de Thot", "branch-occult", "Paris, 1788–91",
     "The FIRST deck designed for divination — Jean-Baptiste Alliette's renamed, renumbered cards with a "
     "cosmogony sequence, significators, and systematic reversed meanings.",
     "First fruit of the occult branch; descends from the Marseille via Court de Gébelin.",
     "✅ Rewritten in this library + live in Supabase.", ["court-de-gebelin", "marseille-conver"], None),
    ("etteilla-iii", "Etteilla II & III (editions)", "branch-occult", "1838 / 1865",
     "Later editions of Etteilla's system — Blocquel's 'Julia Orsini' (II) and Regamey's chromolithograph "
     "'Oracle des Dames' (III).",
     "Continuations of Etteilla's deck.",
     "✅ Rewritten + live.", ["etteilla-i"], None),
    ("levi", "Éliphas Lévi", "branch-occult", "Paris, 1850s",
     "Lévi wrote no deck but mapped the 22 trumps onto the 22 Hebrew letters and the Kabbalistic Tree of "
     "Life — the framework all later esoteric tarot uses.",
     "A tradition NODE: the Kabbalistic key, inherited by Wirth and the Golden Dawn.",
     "📘 Tradition node (no deck).", ["marseille-conver"], None),
    ("papus", "Papus — Tarot des Bohémiens", "branch-occult", "Paris, 1889",
     "Gérard Encausse ('Papus') systematised the Lévi correspondences in a famous book, illustrated with "
     "Wirth's majors.",
     "A tradition NODE linking Lévi to Wirth.",
     "📘 Tradition node.", ["levi"], None),
    ("oswald-wirth", "Oswald Wirth Tarot", "branch-occult", "Paris, 1889 / 1926",
     "Wirth designed 22 esoteric Major Arcana under Stanislas de Guaita — reworked Marseille imagery carrying "
     "Lévi's Hebrew-letter and astrological symbols.",
     "Bridges Lévi's Kabbalah into imagery; the Continental esoteric major arcana.",
     "✅ Built (grammars/oswald-wirth-tarot).", ["levi", "marseille-conver"],
     "Oswald Wirth - Les 22 Arcanes du Tarot Kabbalistique.jpg"),
    ("golden-dawn", "Golden Dawn — Book T", "branch-occult", "London, 1888",
     "The Hermetic Order of the Golden Dawn's complete correspondence system (Book T): paths, decans, "
     "Sephiroth, 'Lord of…' titles. It swaps Strength↔Justice.",
     "The English synthesis; parent of the Rider-Waite-Smith and Thoth decks.",
     "✅ Built (grammars/golden-dawn-book-t-tarot, with RWS imagery).", ["levi", "marseille-conver"],
     "RWS_Tarot_00_Fool.jpg"),
    ("rws", "Rider-Waite-Smith", "branch-occult", "London, 1909",
     "A.E. Waite & Pamela Colman Smith's deck — the first to fully illustrate the minor arcana with scenes. "
     "The most influential modern tarot.",
     "Descends from the Golden Dawn; ancestor of thousands of modern decks.",
     "🟢 Live in Supabase (RWS Archetypal).", ["golden-dawn"], "RWS_Tarot_01_Magician.jpg"),
    ("thoth", "Thoth (Crowley–Harris)", "branch-occult", "London, 1944",
     "Aleister Crowley and Lady Frieda Harris's esoteric deck — the culmination of the Golden Dawn line.",
     "Descends from the Golden Dawn. ⛔ Still in copyright — referenced here, never reproduced.",
     "⛔ Copyright — reference only, not built.", ["golden-dawn"], None),
    # --- Sui generis ---
    ("sola-busca", "Sola Busca", "branch-sui", "Ferrara/Venice, c. 1491",
     "The earliest COMPLETE 78-card illustrated deck — trumps named for classical figures (Mato, Panfilio, "
     "Catulo…), steeped in alchemical and humanist symbolism. Pamela Colman Smith studied its pips.",
     "A sui-generis offshoot, in none of the three orders; an alchemical art-object more than a game deck.",
     "🟢 Live in Supabase.", ["italian-trionfi"], None),
    ("mantegna", "Mantegna 'Tarocchi'", "branch-sui", "N. Italy, c. 1465",
     "A 50-card series of educational engravings (muses, virtues, planets, estates) — NOT a tarot at all, "
     "despite the name; it has no suits and no trick-taking trumps.",
     "A famous false relative, included to clear up the confusion.",
     "✅ Built in this library (grammars/mantegna-tarocchi) — grammar_type 'custom', not 'tarot'.", [],
     "Master of the E-Series Tarocchi - The Beggar (from the Tarocchi, series E- Conditions of Man, 1) - 1924.432.1 - Cleveland Museum of Art.jpg"),
    ("modern-derivatives", "Modern Derivative Decks", "branch-sui", "20th–21st c.",
     "The thousands of modern decks descending from the Marseille, RWS, or Thoth — including the library's "
     "own community decks (Tarocchino Arlecchino, Clown Town, Anecdotes, Luiza Lian, the Ontoject…).",
     "The living edge of the tree; nearly all trace to RWS or the Marseille.",
     "🟢 Several live in Supabase.", ["rws", "marseille-conver"], None),
]

ART = {"name": "PlayfulProcess", "date": "2026", "note": "Genealogical synthesis; Dummett A/B/C framework"}

items = []
so = 0
for did, name, branch, when, what, lineage, status, derives, cover in D:
    sections = {
        "What it is": what,
        "Where & when": when,
        "Lineage": lineage,
        "In this library": status,
    }
    it = {
        "id": f"deck-{did}", "name": name, "sort_order": so, "category": "deck", "level": 1,
        "keywords": ["tarot", "history", branch.replace("branch-", "")],
        "metadata": {"branch": branch, "derives_from": [f"deck-{d}" for d in derives], "when": when},
        "sections": sections,
    }
    u = img(cover)
    if u:
        it["image_url"] = u
    items.append(it)
    so += 1

# L2 branches
for bid, bname, blurb in BRANCHES:
    kids = [it["id"] for it in items if it["metadata"].get("branch") == bid]
    items.append({
        "id": bid, "name": bname, "sort_order": so, "category": "branch", "level": 2,
        "composite_of": kids, "relationship_type": "emergence",
        "keywords": ["tarot", "branch", "history"],
        "metadata": {},
        "sections": {"About this branch": blurb,
                     "Decks here": ", ".join(it["name"] for it in items if it["metadata"].get("branch") == bid)},
    })
    so += 1

# L3 root
items.append({
    "id": "root-tree-of-tarot", "name": "The Tree of Tarot", "sort_order": so, "category": "root", "level": 3,
    "composite_of": [bid for bid, _, _ in BRANCHES], "relationship_type": "emergence",
    "keywords": ["tarot", "genealogy", "history", "tree"],
    "metadata": {},
    "sections": {
        "The Whole Tree": "Tarot began as a card GAME in mid-1400s Northern Italy — a fifth suit of 22 "
        "illustrated 'triumphs' added to an ordinary pack. From that single root three regional trump-orders "
        "diverged (Dummett's A, B, C), the western C-order hardened into the printed Tarot de Marseille, and "
        "from the 1780s the Marseille was reimagined as esoteric wisdom, producing the occult decks. "
        "Divination is a late branch, not the root.",
        "How to read this tree": "Each branch is a lineage; each leaf is a deck. Crucially, the Marseille "
        "(C-order) and the Bolognese Tarocchino (A-order) are COUSINS — both children of the common Italian "
        "root — not parent and child. Follow a branch down to see what descends from what.",
    },
})

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Michael Dummett", "date": "1980",
             "note": "A/B/C trump-order classification ('The Game of Tarot') — the scholarly backbone"},
            {"name": "Tarot History Forum", "date": "ongoing",
             "note": "Scholarly community consulted for genealogy (facts only; no text reproduced)"},
            ART,
        ],
    },
    "name": "The Tree of Tarot — A Grammar of Tarot Grammars",
    "description": (
        "The genealogy of tarot as a single explorable tree: the decks ARE the cards. Built to render in the "
        "recursive.eco tree-viewer, with L1 = individual decks/traditions, L2 = the branches (Michael "
        "Dummett's A / B / C trump-orders, plus the occult reframing and the sui-generis relatives), and L3 = "
        "the root 'The Tree of Tarot'.\n\n"
        "It corrects a common misconception: the Tarot de Marseille is NOT descended from the Bolognese "
        "Tarocchino — they are cousins, both descending from the mid-1400s Italian trionfi. Each leaf links "
        "to its full deck in this library (built, live in Supabase, or planned).\n\n"
        "This is the capstone of the tarot collection: a map you can walk from the 1440s Milanese game decks, "
        "through the three regional orders and the printed Marseille standard, into the occult reframing that "
        "invented divination and produced the modern decks."
    ),
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "tags": ["tarot", "history", "genealogy", "tree", "meta-grammar", "lineage", "dummett", "public-domain"],
    "roots": ["western-esoteric", "renaissance"],
    "shelves": ["wonder", "mirror"],
    "lineages": ["Andreotti"],
    "worldview": "historical",
    "default_preview": "tree",
    "is_published": False,
    "items": items,
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, "grammar.json"), "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)
n1 = sum(1 for it in items if it["level"] == 1)
n2 = sum(1 for it in items if it["level"] == 2)
n3 = sum(1 for it in items if it["level"] == 3)
print(f"Wrote tree-of-tarot/grammar.json — {len(items)} items (L1 decks {n1}, L2 branches {n2}, L3 root {n3})")
