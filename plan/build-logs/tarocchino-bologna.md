# Build Log — Tarocchino di Bologna (the real one)

**Grammar:** `grammars/tarocchino-bologna/grammar.json`
**Generator:** `scripts/generate_tarocchino_bologna.py`
**Type:** `tarot` · 68 items (22 trumps + 40 minors + 6 emergences)
**Built:** June 2026 → main

## What this is
The genuine 62-card Tarocchino di Bologna (Dummett A-order) — built structure-accurate
to distinguish it from the library's modern Marseille-named "Tarocchino Arlecchino,"
which is a homage, not the historical Bolognese deck.

## The three distinctive features it documents
- **62 cards:** pips 2–5 removed (Ace, 6–10 + four courts per suit = 40 minors).
- **The four PAPI** ("Quattro Mori") — four equal, interchangeable cards replacing the
  Popess, Empress, Emperor and Pope. (L2 emergence "The Four Papi.")
- **The Angel (Judgement) is the HIGHEST trump** — above the World. Virtues clustered
  in the middle. (L2 emergence "The Trumps in the Bolognese Order.")
- Game deck → Tradition Note on every card.

## Archetype stamping
Added to `scripts/stamp_archetypes.py` (now 12 decks, 755 cards). All 18 ordinary
trumps resolve to their `arcana:*` keys; the **four Papi correctly resolve to `None`**
(no forced equivalence). Also fixed the resolver to catch the bare-named "Love" card
(`\blove\b`). "Death" now spans all 12 tarot decks.

## IMAGE NOTE (the honest gap)
No clean per-card public-domain Bolognese scan exists on Commons:
- BnF Gallica albums `btv1b105138709` (126 files) and `btv1b105088141` (117) are
  **unlabelled sequential scans** — identifying each card needs vision.
- The Mitelli 1664 Tarocchino is not on Commons as a set.
So this ships **structure-first**: composite deck sheet (`Tarocco Bolognese.png`) as
cover and on the emergences; **per-card images are a documented vision-mapping TODO.**

## Validation
No dup IDs; composite refs resolve. Marked ✅ Built in `tree-of-tarot`.
