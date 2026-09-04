# Build Log — Etteilla I / II / III rewrite (within the tradition)

**Grammars:** `grammars/etteilla-i-livre-de-thot/`, `grammars/etteilla-ii-egyptian/`,
`grammars/etteilla-iii-oracle-des-dames/`
**Generator:** `scripts/generate_etteilla_rewrite.py`
**Type:** `tarot` · 78 items each · all R2-imaged
**Built:** May 2026 → main

## Why
The live Supabase Etteilla decks were uneven: the cosmogony majors (Le Chaos and
the first ~12) were genuinely tradition-accurate (Poimandres, Temple of Ptah,
Genesis sequence), but the 56 minors were generic modern psychology ("Emotional
intelligence and mature wisdom") that could belong to any deck. This pass rewrites
all three editions to sit inside Etteilla's own system.

## Source of truth
Pulled the **live decks from Supabase** (REST API, anon key) to a local scratch
dir — NOT the stale repo schema (whose images were dead Google-Drive links). The
rewrite preserves each deck's own ids, names, and **R2 images** (the author's
uploads).

## What was rewritten (and why it's "within the tradition")
- **Etteilla's renamed/renumbered majors** with his idiosyncratic meanings: the
  Bateleur as **illness**, the Capucin (Hermit) as the **traitor**, the Devil as
  raw **force**, the cosmogony/creation sequence, and the two **significators**
  (1 Le Chaos = male querent, 78/0 La Folie = female querent).
- **Court-as-person**: the signature of Etteilla/French cartomancy — all 16 courts
  read as PEOPLE, by suit temperament and rank, upright = well-disposed / reversed
  = ill-disposed.
- **Systematic reversed meanings** on every card (Etteilla's own innovation).
- **Cosmogony scholarship** (Etymology / Genesis / Historical / Hermetic) preserved
  and **propagated to all three editions** — a real enrichment for Etteilla III,
  which previously had none.

## Honesty note (deliberate restraint)
The exact **two-word period keyword** printed on each historical card is NOT
asserted where it could not be verified against a primary source. WebFetch sourcing
(Wikipedia, vieuxmonde, etteilla.org) failed/403'd, and inventing keywords would
betray the tradition-accuracy that is the whole point. Meanings are written
faithfully in Etteilla's register; sourcing the inscriptions from Etteilla's *Cours
théorique et pratique du livre de Thot* (or Benebell Wen's reconstruction) is
flagged as a future enrichment, in the deck description and here.

## Status / next step
These are committed to the repo on `main`. They are **not yet written back to the
live Supabase decks** — that is a separate, deliberate step (UPDATE of the public
`user_documents` rows e4eea1e1 / 46527510 / 24a41f00). Awaiting the author's go
before touching production rows.
