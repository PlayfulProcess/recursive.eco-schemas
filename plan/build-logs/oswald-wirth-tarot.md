# Build Log — Oswald Wirth Tarot

**Grammar:** `grammars/oswald-wirth-tarot/grammar.json`
**Generator:** `scripts/generate_oswald_wirth.py`
**Type:** `tarot` · 23 items (22 Major Arcana + 1 emergence) · all with images
**Built:** May 2026, branch `claude/tarot-visconti-wirth`

## What this is
Oswald Wirth's 22 esoteric Major Arcana — *Les 22 Arcanes du Tarot Kabbalistique*
(1889, under Stanislas de Guaita), revised as *Le Tarot des imagiers du Moyen Age*
(1926). Wirth designed only the trumps; he reworked Marseille imagery and embedded
Kabbalistic + astrological symbols following Éliphas Lévi. The hinge between the
French occult revival and the English (Golden Dawn / RWS / Thoth) decks.

## Card structure
Each arcanum: `Symbolism` (what Wirth drew & why), `Correspondences` (Hebrew
letter + meaning, number, astrological association), `Upright`, `Reversed`.

## Decisions
- **Continental attribution** (Wirth's own): the unnumbered Fool sits between
  Judgement (20) and the World (21), letter **Shin** — NOT the Golden Dawn order.
  Stated explicitly in the description so it isn't "corrected" later.
- Hebrew letters given **confidently** (core of Wirth's system, Lévi 1→Aleph … 21→Tav).
- Astrology **hedged** ("traditionally associated with…") because Continental vs.
  Golden Dawn planet/sign mappings diverge and Wirth's own are not uniform — per
  the no-absolutist-claims house style.
- One L2 emergence: "The Major Arcana as the Great Work" (the initiatory ladder).

## Images
- Source: Wikimedia Commons, Category:Oswald Wirth tarot deck — **1889 BnF edition**
  (clean, complete set of all 22). Filenames pulled from the Commons API and
  embedded verbatim (they contain spaces/apostrophes; URL-encoded for FilePath).
- PD basis: Wirth d. 1943; 1889 deck long PD.
- Spot-checked HTTP 200.

## Validation
`scripts/validate.py` — not among the repo's 31 pre-existing issues. Custom check:
no dup IDs, composite ref resolves, no empty sections. Manifest regenerated.

## Next steps (deferred)
- Optionally add a Wirth column to `tarot-of-all-tarots`.
- The 1926 edition adds astro/Hebrew glyphs in the card borders — a future image
  upgrade could swap to 1926 plates where available.
