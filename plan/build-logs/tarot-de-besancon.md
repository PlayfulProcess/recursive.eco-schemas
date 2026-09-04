# Build Log — Tarot de Besançon / Swiss 1JJ (variant highlights)

**Grammar:** `grammars/tarot-de-besancon/grammar.json`
**Generator:** `scripts/generate_besancon.py`
**Type:** `tarot` · 14 items (13 cards + 1 emergence) · all imaged · **PARTIAL**
**Built:** June 2026 → main

## What this is
A PARTIAL, variant-highlights grammar for the Tarot de Besançon / Swiss "1JJ" type —
the Marseille variant (Dummett C-order) whose defining move is replacing the **Popess
with Juno** and the **Pope with Jupiter** (the two "J" cards), removing the Catholic
clergy for Protestant/mixed-confessional regions.

## Why partial
Commons (Category:Tarot 1JJ) has only ~13 clean cards: the two signature cards plus a
representative selection of trumps and pips. So this documents the variant, not the
full 78 — clearly labelled as such in the name and description. (A full deck would
need the AGMüller facsimile, which is in copyright, or museum scans of period Besançon
decks.)

## Archetype stamping
Added to `scripts/stamp_archetypes.py` (now 13 decks, 768 cards) with a Besançon
special case: **Juno → `arcana:the-high-priestess` (loose)**, **Jupiter →
`arcana:the-hierophant` (loose)** — so the substituted cards still join their archetype
groups across decks, honestly marked as loose mappings. Minors carry suit/rank.

## Validation
No dup IDs; composite refs resolve; 14/14 imaged. Marked ✅ Built (partial) in
`tree-of-tarot`.
