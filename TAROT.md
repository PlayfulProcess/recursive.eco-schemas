# The recursive.eco Tarot Collection

A public-domain, scholarship-grounded set of **tarot grammars** — structured JSON
datasets, one per historical deck — plus a **genealogical meta-grammar** that maps how
the decks descend from one another. Everything here is **CC-BY-SA-4.0** and built from
**public-domain** sources (Wikimedia Commons, the BnF/Gallica, etc.).

If you are a tarot historian or collector and found this from the Tarot History Forum:
**welcome, and please correct us.** See *Contributing* below.

---

## What this is (and is not)

- **Is:** an open, machine-readable map of tarot's documentary history — each deck's
  cards with iconography, history, correspondences (where the tradition has them), and
  honest tradition notes. It renders at [recursive.eco](https://recursive.eco) as cards,
  readings, and a genealogy tree.
- **Is not:** a divination product dressed up as history. Where a deck was a **game**
  deck (Visconti, Marseille, Minchiate, Charles VI…), every card says so — divination is
  a later (post-1780s) overlay, not the deck's origin.

### Accuracy principles we try to hold
- **Public domain only.** No copyrighted decks reproduced (e.g. **Thoth, 1944** is
  referenced, never copied).
- **No forced equivalences.** Etteilla renumbered Death to 17; the Golden Dawn swapped
  Strength↔Justice; Minchiate's zodiac/element cards have *no* standard equivalent; Sola
  Busca's classical figures only *loosely* map. We mark these honestly rather than
  flattening them.
- **Game vs. divination is labelled**, per card.
- **The Tarot History Forum** (and Dummett's scholarship) is consulted for **facts**;
  no forum text is reproduced (it's author-copyrighted).
- We will be wrong about things. Corrections are the point.

---

## The decks (built so far)

| Grammar | Deck | Cards | Tradition / order |
|---|---|---|---|
| `grammars/visconti-sforza-tarot` | Visconti-Sforza | 85 | oldest near-complete (Milan, c.1451) |
| `grammars/cary-yale-visconti-tarot` | Cary-Yale (Visconti di Modrone) | 73 | six courts + theological virtues (c.1442) |
| `grammars/charles-vi-tarot` | "Charles VI" (Gringonneur) | 18 | Ferrarese / B-order (c.1450–80) |
| `grammars/minchiate-florence-tarot` | Minchiate | 106 | Florentine 97-card / A-order |
| `grammars/tarot-de-marseille-conver` | Tarot de Marseille (Conver 1760) | 83 | printed standard / C-order |
| `grammars/oswald-wirth-tarot` | Oswald Wirth | 23 | Continental esoteric (1889/1926) |
| `grammars/golden-dawn-book-t-tarot` | Golden Dawn (Book T) | 84 | full GD correspondences, RWS imagery |
| `grammars/etteilla-i-livre-de-thot` | Etteilla I — Livre de Thot | 78 | first divination deck (1788) |
| `grammars/etteilla-ii-egyptian` | Etteilla II | 78 | 1838 edition |
| `grammars/etteilla-iii-oracle-des-dames` | Etteilla III — Oracle des Dames | 78 | 1865 edition |
| `grammars/tree-of-tarot` | **The Tree of Tarot** (meta-grammar) | 32 | the genealogy itself |

Also live on the platform (not in this repo's `grammars/` as historical builds): a
public-domain Marseille, Rider-Waite-Smith, Sola Busca, and the Bolognese-styled modern
"Tarocchino Arlecchino."

**Planned** (see `plan/tarot-roadmap-and-supabase-log.md` §1): the real Tarocchino di
Bologna, Mantegna "Tarocchi" (to explain it is *not* a tarot), Court de Gébelin's plates,
Besançon/Swiss 1JJ, Belgian/Vandenborre, Tarocco Siciliano, d'Este, the Cary/Rosenwald
sheets.

---

## The genealogy (how to read the tree)

`grammars/tree-of-tarot/grammar.json` is a meta-grammar whose **items are the decks**,
built on **Michael Dummett's A/B/C trump-order** classification:

```
Italian trionfi (c.1440s)
├─ A-order (Bologna/Florence) ── Tarocchino di Bologna · Minchiate · Tarocco Siciliano
├─ B-order (Ferrara) ─────────── "Charles VI" · d'Este
└─ C-order (Milan/West) ──── Visconti/Cary-Yale ──► Tarot de Marseille ──► occult decks
   (Sola Busca = a sui-generis offshoot)
```

It corrects a common belief: **the Marseille is *not* descended from the Bolognese
Tarocchino** — they are cousins (C- vs A-order), both children of the common root. The
meta-grammar uses the platform's *reference-item* structure (see `GRAMMAR_FORMAT.md` →
"Reference items & meta-grammars") so each leaf can open the full deck, and
`default_preview: "tree"` renders it in the tree-viewer.

---

## How it's built (for contributors)

- **Format:** `GRAMMAR_FORMAT.md` is the contract. Each deck is one
  `grammars/<slug>/grammar.json`.
- **Generators:** decks are produced by reproducible Python scripts in `scripts/`
  (`generate_<deck>.py`) from data tables, not hand-typed — easy to audit and re-run.
- **Images:** public-domain, hot-linked from Wikimedia Commons via stable
  `Special:FilePath` URLs (filenames pulled from the Commons API, not guessed).
- **Build logs:** `plan/build-logs/<deck>.md` record sources, decisions, and caveats.
- **Plan / roadmap:** `plan/tarot-of-all-tarots-master-plan.md` (history + lineage) and
  `plan/tarot-roadmap-and-supabase-log.md` (what's left, fixes owed, future features).
- **Validate:** `python scripts/validate.py`; rebuild the index with
  `python scripts/generate_manifest.py`.

> Transparency: these grammars are **AI-assisted** (drafted with Claude, reviewed by the
> maintainer). That is exactly why outside scholarly review is wanted.

---

## Contributing & corrections

Corrections from historians are the most valuable thing this repo can receive.

- **Spotted an error** (a date, an attribution, a mis-mapped archetype, a bad image)?
  Open a GitHub **issue** or a **pull request** against the relevant
  `grammars/<slug>/grammar.json` (or its `generate_<deck>.py`).
- **Copyright:** PD sources only; paraphrase + attribute, never copy copyrighted text
  (see `CLAUDE.md` → *Copyright Boundaries*). Forum posts and modern deck art are
  copyrighted — cite, don't reproduce.
- **Attribution:** contributors are credited in each grammar's `_grammar_commons.attribution`.

### Sharing this work (plan)
- **Post to the Tarot History Forum** as a human, with this repo link, an upfront note
  that it's AI-assisted, and an explicit invitation to correct — *not* by scraping the
  forum (it blocks bots and its posts belong to their authors).
- **A separate, curated reference repo** (e.g. `recursive-tarot`) is under consideration
  — a clean mirror of just the tarot grammars + docs, easier for collaborators than this
  larger mixed `schemas` repo. Until then, **this file is the entry point.** (Logged as a
  *later* item; not built yet.)
