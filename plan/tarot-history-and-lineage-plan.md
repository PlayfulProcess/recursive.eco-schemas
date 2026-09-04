# Tarot History & Lineage Plan

A working map of where tarot comes from, which decks branch from which, and how
this repo's tarot grammars fit the tree. This doc has two jobs:

1. **The history** the grammars draw on (so summaries stay consistent across decks).
2. **The seed design** for a future "grammar of tarot grammars" — a lineage
   tree-view that shows the branches and derivatives. *(Deferred — see last section.
   Not being built yet.)*

---

## 1. The history in one breath

Tarot began as a **card game, not a divination system**. In mid-1400s Northern
Italy (Milan, Ferrara, Bologna) someone added a fifth suit of 22 illustrated
*trionfi* ("triumphs") to the ordinary 56-card Italian playing pack. The 22
trumps are the tarot's true invention. Divination came **roughly 300 years
later**, in 1700s France. Everything since branches from that Italian root.

The ordinary pack underneath the trumps: four suits — **Coins (Denari), Cups
(Coppe), Swords (Spade), Batons (Bastoni)** — each running Ace–10 plus four (or,
in the Cary-Yale, six) court cards.

---

## 2. The lineage tree

```
ROOT — Italian trionfi / tarocchi game decks (c. 1440s)
│   56-card pack (Coins · Cups · Swords · Batons) + 22 trumps
│
├─ HAND-PAINTED LUXURY DECKS  (Milan, Bonifacio Bembo workshop)
│   ├─ Cary-Yale / Visconti di Modrone   c. 1442   (Beinecke, Yale) — 6 courts/suit, added Virtues
│   ├─ Brera-Brambilla                    c. 1442   (Brera, Milan) — fragmentary
│   └─ Pierpont Morgan–Bergamo / VISCONTI-SFORZA  c. 1451  — most complete, 74/78 survive
│        ↳ [REPO] grammars/visconti-sforza-tarot
│
├─ OTHER EARLY ITALIAN BRANCHES
│   ├─ Sola-Busca           c. 1491   — earliest complete 78-card *illustrated* deck  ↳ [REPO schema] sola-busca
│   ├─ Tarocchino di Bologna           — 62-card Bolognese game                        ↳ [REPO schema] tarocchino-*
│   └─ Minchiate (Florence)            — 97-card expansion
│
├─ PRINTED WOODBLOCK STANDARD
│   └─ TAROT DE MARSEILLE   (Noblet 1650 → Dodal 1701 → Conver 1760)                   ↳ [REPO schema] marseille
│        the canonical occult-era reference image; fixes the 22 trump names/order
│
├─ FRENCH OCCULT TURN  (late 1700s — divination is INVENTED here)
│   ├─ Antoine Court de Gébelin  1781   — the "ancient Egyptian Book of Thoth" myth
│   ├─ Etteilla (J.-B. Alliette) 1780s  — first purpose-built divination deck; reversals, spreads
│   │     ↳ [REPO] tarot-rws-etteilla, schemas etteilla-i/II/III, grand-jeu-etteilla-III
│   ├─ Éliphas Lévi            1850s   — maps the 22 trumps to the 22 Hebrew letters + Kabbalah
│   ├─ Papus (G. Encausse)     1889    — *Le Tarot des Bohémiens*
│   └─ OSWALD WIRTH       1889 / 1926  — 22 esoteric Major Arcana; the Lévi→de Guaita synthesis
│        ↳ [REPO] grammars/oswald-wirth-tarot
│
└─ ENGLISH ESOTERIC BRANCH
    ├─ Hermetic Order of the Golden Dawn  1888  — full correspondence system; swaps Strength ↔ Justice (VIII/XI)
    ├─ RIDER-WAITE-SMITH   1909   — Waite + Pamela Colman Smith; first *mass-market* deck with fully scene-illustrated minor arcana (Sola-Busca, 1491, illustrated its pips first)
    │     ↳ [REPO] rider-waite-smith-tarot
    └─ Thoth   (Crowley + Frieda Harris, 1944)  — esoteric culmination
         │
         └─ → thousands of modern derivative decks descend from the Marseille,
              RWS, or Thoth lines.
```

### Where the two new decks sit

- **Visconti-Sforza** is the *oldest* branch — game-era iconography, **pre-divinatory**.
  Read it for history and image, not fortune-telling. Note the pre-occult numbering
  (Justice = VIII, the Hermit still "Il Tempo" with an hourglass), the four
  permanently **lost cards** (Devil, Tower, Knight of Coins, Three of Swords), and
  the six trumps **repainted by a later hand** (Fortitude, Temperance, Star, Moon,
  Sun, World).
- **Oswald Wirth** is the *hinge* of the occult branch — he carried Lévi's
  Kabbalah into reworked Marseille imagery, which the English decks then inherited.
  Note the **Continental attribution**: the Fool sits between Judgement (20) and the
  World (21), assigned the letter Shin — differing from the later Golden Dawn order.

---

## 3. Key historical facts the grammars rely on

- **Not Egyptian, not ancient.** The "Book of Thoth / ancient Egypt" origin is an
  18th-century invention (Court de Gébelin, 1781). The documented origin is the
  Italian *trionfi* game, c. 1440s.
- **Trumps came first as a game.** Reversals, spreads, and card "meanings" are an
  Etteilla-era (1780s+) overlay onto a gaming deck.
- **The Strength/Justice swap** (VIII ↔ XI) is a Golden Dawn (post-1888) change.
  Older decks (Visconti, Marseille) keep Justice = VIII, Strength = XI.
- **Hebrew-letter attribution** of the trumps is Lévi's (1850s), carried by Papus
  and Wirth; the Golden Dawn modified it (notably the Fool ↔ Aleph placement).
- **Public domain status** (used for this repo): Visconti-Sforza (15th c., PD);
  Marseille woodcuts (PD); Etteilla editions (PD); Oswald Wirth d. 1943 + 1889
  deck (PD); Rider-Waite-Smith 1909 (PD in the US). Thoth (1944) is **still in
  copyright** — reference only, do not reproduce.

---

## 4. Repo inventory — tarot so far

| Grammar / schema | Branch | Status |
|---|---|---|
| `grammars/rider-waite-smith-tarot` | English esoteric (RWS) | existing |
| `grammars/tarot-rws-etteilla` | French occult (Etteilla) | existing |
| `grammars/tarot-of-all-tarots` | **comparative meta-deck** (RWS·Marseille·Sola-Busca·3×Etteilla·Tarocchino) | existing |
| `grammars/jungian-archetypes` | modern psychological | existing |
| `grammars/alice-s-tarot-my-5-years-old` | modern custom | existing |
| `grammars/playful-process-the-path-of-the-ontoject` | modern custom (Tillich) | existing |
| `grammars/visconti-sforza-tarot` | **Italian root (oldest)** | **new (this branch)** |
| `grammars/oswald-wirth-tarot` | **French occult (Wirth)** | **new (this branch)** |
| `schemas/tarot/marseille`, `sola-busca`, `etteilla-*`, `tarocchino-*` | reference schemas | existing |

---

## 5. FUTURE (deferred): "The Grammar of Tarot Grammars" — a lineage tree-view

> Per the author's note ("maybe we will have later a grammar of tarot grammars
> that tells the branches and derivatives in tree view"). **Seed design only —
> not to be built until requested.**

Concept: a `grammar_type: "custom"` grammar whose items ARE the decks/traditions,
arranged as an emergence tree so the viewer can render the lineage above.

- **L1 items** = individual decks (Visconti-Sforza, Cary-Yale, Sola-Busca,
  Marseille/Conver, Etteilla I/II/III, Wirth, RWS, Thoth, Minchiate, Tarocchino…).
  Each card: *What it is*, *Who made it & when*, *What it changed*, *What descends
  from it*, plus a link to the repo grammar if one exists.
- **L2 items** = the branches (Italian luxury decks, printed Marseille, French
  occult, English esoteric), each `composite_of` its L1 decks.
- **L3 items** = the two great families ("game tradition" vs "divinatory/esoteric
  tradition"), or a single root node "The Tree of Tarot".

This reuses the existing L1/L2/L3 `composite_of` emergence machinery — the viewer
already renders composites, so a tree-view falls out of the data with no new
format. Cross-references (`metadata.derives_from: [deck-id]`) could later drive an
explicit edge-list for a true graph/tree visual.

Open question for the author: should it also fold in **non-European** card-oracle
traditions (Lenormand, Kipper, Sibilla, and further-afield systems) as sibling
roots, or stay strictly the European tarot line? (Repo already has a
`schemas/tarot/petit-Lenormand`.)
