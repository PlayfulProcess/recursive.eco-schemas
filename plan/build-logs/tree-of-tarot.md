# Build Log — The Tree of Tarot (genealogical meta-grammar)

**Grammar:** `grammars/tree-of-tarot/grammar.json`
**Generator:** `scripts/generate_tarot_tree.py`
**Type:** `custom` · 32 items (25 deck L1 + 6 branch L2 + 1 root L3) · 3 levels
**Built:** June 2026 → main

## What this is
The "grammar of tarot grammars" the author envisioned: a genealogical tree where the
**items are the decks**. Designed to render in the **existing** recursive.eco
tree-viewer (`pages/tree-viewer.html`) — no new frontend.

- **L1 (deck)** — 25 decks/traditions; sections: What it is · Where & when · Lineage · In this library. `metadata.derives_from` carries precise ancestry edges for a future view.
- **L2 (branch)** — 6 branches via `composite_of`: Roots (Milan), Dummett's **A/B/C** trump-orders, the Occult Reframing, and Sui Generis & Relatives.
- **L3 (root)** — "The Tree of Tarot", `composite_of` the 6 branches.

## Scholarship / the correction it bakes in
Backbone is **Michael Dummett's A/B/C trump-order classification**. It explicitly
corrects the common belief that the Marseille descends from the Bolognese Tarocchino:
they are **cousins** (C-order vs A-order), both children of the 1440s Italian trionfi.
Tarot History Forum consulted for facts only (no text reproduced — it 403s bots and
its posts are author-copyrighted).

## How to view it
The tree-viewer renders by Supabase document id
(`recursive.eco/pages/tree-viewer.html?type=custom&id=<id>`). This grammar is in the
REPO; to see it in the live tree-viewer it must first be **imported to Supabase**
(then it gets an id). See the Supabase upload log in
`plan/tarot-roadmap-and-supabase-log.md` §3.

## Follow-ups
- Backfill thin branches: build the real **Tarocchino di Bologna** (A) and **Charles VI**
  (B) so those branches aren't sparse.
- Optional precise-edge ("X → Y") view in recursive-eco reading `metadata.derives_from`.
