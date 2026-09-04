# Build Log — The "Mantegna Tarocchi" (NOT a tarot)

**Grammar:** `grammars/mantegna-tarocchi/grammar.json`
**Generator:** `scripts/generate_mantegna.py`
**Type:** `custom` (deliberately NOT `tarot`) · 57 items (50 plates + 6 group L2 + 1 root L3)
**Built:** June 2026 → main

## What this is
The 50-engraving "Mantegna Tarocchi" (E-series, North Italy, c. 1465) — the most famous
**false relative** of the tarot. No suits, no 22 trumps, no game: it is a Neoplatonic
LADDER of being, five decades of ten rising from the Beggar → estates → Apollo & Muses
→ liberal arts → cosmic genii & seven virtues → planetary spheres → Prime Mover →
First Cause. Built explicitly to clear up the perennial confusion (and it is not by
Mantegna, either).

## Decisions
- **`grammar_type: "custom"`, not `tarot`** — on purpose. It also means
  `stamp_archetypes.py` correctly skips it (its cards aren't tarot archetypes).
- Structure mirrors its real structure: L1 = 50 plates, L2 = the six series
  (E/D/C/B-genii/B-virtues/A), L3 = "The Ladder of Being". Renders in the tree-viewer.
- Every card carries a "Note: not a tarot" section; the L3 root explains the
  imagery-overlap-but-not-ancestry relationship to tarot.

## Images (the TIF problem, solved)
- Source: the Cleveland Museum of Art impression (1924.432.1–50) on Wikimedia Commons;
  exact filenames pulled from the Commons API (embedded in the generator).
- **~35 of the 50 are .tif**, which browsers can't render. Fix: serve via
  `Special:FilePath/<name>?width=700`, which makes Wikimedia return a **JPEG thumbnail**
  even for TIF/SVG originals. Verified: both .tif and .jpg return `content_type:
  image/jpeg`. **Reusable trick for any TIF/SVG-only Commons set.**

## Validation
No dup IDs; all composite refs resolve; 57/57 imaged. Marked ✅ Built in `tree-of-tarot`.
