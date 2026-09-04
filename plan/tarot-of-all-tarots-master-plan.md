# The Tarot of All Tarots — Master Plan

The complete plan for tarot in recursive.eco: the full history, the lineage tree,
every deck we have / are building / still need / cannot use, the modern decks
already live in Supabase, and the design for the future **"grammar of tarot
grammars"** — a single meta-grammar that tells the whole tree as an explorable
tree-view.

> Companion: [`tarot-history-and-lineage-plan.md`](tarot-history-and-lineage-plan.md)
> (the first-pass history). This doc supersedes and extends it.

---

## 1. The history, in one breath

Tarot began as a **card game, not divination**. In mid-1400s Northern Italy
(Milan, Ferrara, Bologna) a fifth suit of 22 illustrated *trionfi* ("triumphs")
was added to the ordinary 56-card Italian pack. The 22 trumps are tarot's true
invention. **Divination was invented ~300 years later**, in 1700s France
(Court de Gébelin's Egyptian myth, then Etteilla's cartomancy). Every later deck
branches from that Italian root through either the **Marseille → French occult**
line or the **English esoteric** line.

The pack under the trumps: four suits — **Coins · Cups · Swords · Batons** — each
Ace–10 plus court cards (four normally; **six** in the Cary-Yale).

---

## 2. The lineage tree — with build status

Legend: ✅ built (repo) · 🟢 live in Supabase channel · 🔨 buildable next · ⛔ copyright · 📄 schema only

```
ROOT — Italian trionfi / tarocchi game decks (c. 1440s)
│
├─ HAND-PAINTED LUXURY DECKS (Milan, Bonifacio Bembo workshop)
│   ├─ ✅ Cary-Yale / Visconti di Modrone   c.1442   grammars/cary-yale-visconti-tarot
│   │        6-court structure (+ female Horsewoman & Damsel), unique Faith/Hope/Charity virtues
│   ├─ 🔨 Brera-Brambilla                    c.1442   — only ~2 trumps + ~46 pips survive; image-poor on Commons
│   └─ ✅ Pierpont Morgan–Bergamo / Visconti-Sforza  c.1451   grammars/visconti-sforza-tarot  (74/78, 4 lost)
│
├─ OTHER EARLY ITALIAN BRANCHES
│   ├─ 🟢 Sola-Busca           c.1491   — earliest complete 78 illustrated deck   (live; 📄 schema sola-busca)
│   ├─ 🟢 Tarocchino di Bologna         — Tarocchino Arlecchino (Y. Lepkowski), 62 cards   (live)
│   └─ 🔨 Minchiate (Florence)          — 97-card expansion; not yet built
│
├─ PRINTED WOODBLOCK STANDARD
│   └─ ✅ Tarot de Marseille — Nicolas Conver 1760   grammars/tarot-de-marseille-conver
│        (also 🟢 a "Tarot de Marseille (Public Domain)" 78 lives in Supabase; 📄 schema marseille)
│        upstream variants 🔨 Jean Noblet 1650, 🔨 Jean Dodal 1701 (PD, fuller pip scans)
│
├─ FRENCH OCCULT TURN (late 1700s — divination is INVENTED here)
│   ├─ Court de Gébelin 1781  — the "ancient Egypt" myth (a treatise, not a deck → a tradition node)
│   ├─ 🟢 Etteilla (J.-B. Alliette) 1780s — Etteilla III live; 📄 schemas etteilla-i/II/III, grand-jeu-etteilla-III
│   │        🔨 Etteilla I (Grand Etteilla, 1788) — the FIRST purpose-built divination deck — worth a standalone
│   ├─ Éliphas Lévi 1850s   — Hebrew-letter + Kabbalah mapping (no deck → tradition node)
│   ├─ Papus 1889           — Le Tarot des Bohémiens (no deck of his own → tradition node)
│   └─ ✅ Oswald Wirth 1889/1926   grammars/oswald-wirth-tarot   (22 esoteric majors)
│
└─ ENGLISH ESOTERIC BRANCH
    ├─ Golden Dawn 1888     — correspondence system; swaps Strength↔Justice (no PD published deck → tradition node)
    ├─ 🟢 Rider-Waite-Smith 1909   — RWS Archetypal live; ✅ grammars/rider-waite-smith-tarot, tarot-rws-etteilla
    └─ ⛔ Thoth (Crowley–Harris 1944) — still in copyright; reference only, never reproduce
         │
         └─ → thousands of modern derivative decks descend from Marseille, RWS, or Thoth.
```

---

## 3. What is already LIVE in the Supabase tarot channel

(Public decks, `Monorepo-dev`, as surveyed.) Canonical/historical in **bold**.

| Deck | Items | Branch / kind |
|---|---|---|
| **The Tarot of All Tarots — Five Centuries** | 89 | comparative meta-deck (RWS·Marseille·Sola-Busca·3×Etteilla·Tarocchino) |
| **Tarot de Marseille (Public Domain)** | 78 | printed standard |
| **Rider–Waite–Smith Archetypal** | 78 | English esoteric |
| **Etteilla III** | 78 | French occult |
| **Sola Busca** | 78 | early Italian |
| **Tarocchino Arlecchino** (Y. Lepkowski) | 62 | Bolognese |
| **Petit Lenormand** | 34 | cartomancy (sibling system) |
| Arlecchino's Augmented Arcana | 84 | modern (Lepkowski) |
| Clown Town Tarot | 78 | modern (Lepkowski) |
| Anecdotes Tarot | 78 | modern (Lepkowski) |
| Luiza Lian | 49 | modern / music |
| Stellar Mythology | 48 | modern / myth |
| Plutchik's Wheel of Emotions | 32 | psychological oracle |
| The Repair Deck | 17 | modern / therapeutic |
| The Living Pulse (NVC + Śaiva Tantra) | 50 | modern / contemplative |
| Path of the Ontoject (+ Cosmic Topology) | 27/66 | modern / philosophical (Tillich) |
| Jungian Archetypes — The Inner Cast | 34 | psychological |
| Alice's Tarot (5 y.o.) | — | kids |

There are also many **private duplicates / "(Copy)" drafts** in the DB (Etteilla II copies, RWS copies, Ontoject copies, I-Ching-as-tarot mislabels). A cleanup pass is worth doing — see §6.

---

## 4. The new historical decks (built this round, in repo, ready to publish)

| Deck | Items | Notes |
|---|---|---|
| ✅ **Visconti-Sforza** | 85 | oldest, 78 cards + emergences; 2 lost trumps blank, 3 gaps filled from Cary-Yale |
| ✅ **Oswald Wirth** | 23 | 22 esoteric majors + Hebrew/astro correspondences |
| ✅ **Cary-Yale Visconti** | 73 | surviving cards only; 6-court + Faith/Hope/Charity |
| ✅ **Tarot de Marseille (Conver 1760)** | 83 | 22 majors imaged + traditional cartomantic minors |
| ✅ **Golden Dawn — Book T + RWS imagery** | 84 | full GD correspondences: paths/decans/Sephiroth/Lord-titles; RWS images |
| ✅ **Minchiate (Florence)** | 106 | full 97-card deck: five Papi, seven virtues, elements, zodiac, Arie |
| ✅ **Etteilla I — Livre de Thot** | 78 | rewritten within Etteilla's tradition; R2 images from Supabase |
| ✅ **Etteilla II — Égyptien** | 78 | rewritten; court-as-person, his idiosyncratic majors |
| ✅ **Etteilla III — Oracle des Dames** | 78 | rewritten + cosmogony scholarship newly propagated |

These are in `grammars/` on `main` but **not yet `is_public` in Supabase** —
publishing to the live channel is a separate import step (see §6). The three
Etteilla rewrites in particular are not yet written back to their live rows
(e4eea1e1 / 46527510 / 24a41f00) — awaiting go-ahead before touching production.

---

## 5. What we still NEED to add (priority order)

1. ✅ ~~Etteilla I~~ — DONE (rewritten from Supabase; all three editions).
2. ✅ ~~Minchiate~~ — DONE (full 97-card deck).
3. ✅ ~~Golden Dawn~~ — DONE (Book T + RWS imagery).
4. 🔨 **Brera-Brambilla** — the third Bembo sister deck; build the ~48 surviving cards once images are sourced (Commons coverage is thin; may need museum scans).
5. 🔨 **Marseille pip upgrade** — swap in a fuller PD pip set from Jean Dodal (1701) or Jean Noblet (1650) so the Marseille minors are fully imaged.
6. 🔨 **Etteilla keyword enrichment** — source the period two-word inscriptions from Etteilla's *Cours théorique* / Benebell Wen and add to the three rewrites.
7. **Tradition nodes (not decks)** — Court de Gébelin, Éliphas Lévi, Papus: capture as *context cards* in the meta-grammar (§7), since none left a usable PD deck of their own. (Golden Dawn now has a full deck.)
8. ⛔ **Thoth** — do NOT build; in copyright. Reference only.

---

## 6. Publishing & hygiene (operational)

- **Repo ≠ live channel.** The four new grammars sit in `grammars/` on `main`.
  Getting them into the live tarot channel = importing into `user_documents`
  (`document_type: 'unified_grammar'` / `'tarot_deck'`, `is_public: true`) via the
  app's import flow or `grammar_import_staging`. Decide attribution/creator before
  publishing.
- **Dedupe pass:** the DB holds many `(Copy)` and `(My Version)` drafts and a few
  I-Ching grammars mislabeled `grammar_type: "tarot"`. Worth pruning so the channel
  reads cleanly.
- **Security note (from the DB scan):** two backup tables
  (`_backup_profiles_pp_20260528`, `_backup_journal_templates_20260529`) have RLS
  disabled — exposed to the anon key. Enable RLS (with policies) or drop the
  backups.

---

## 7. The "Grammar of Tarot Grammars" — meta-grammar design

A single `grammar_type: "custom"` grammar whose **items are the decks and
traditions**, arranged as an emergence tree so the viewer renders §2 as an
explorable tree-view.

- **L1 = decks** — Cary-Yale, Brera-Brambilla, Visconti-Sforza, Sola-Busca,
  Tarocchino, Minchiate, Marseille (Noblet/Dodal/Conver), Etteilla I/II/III,
  Wirth, RWS, (Thoth = reference-only stub), plus the modern decks (Clown Town,
  Anecdotes, Arlecchino's Augmented, Luiza Lian, Stellar Mythology, Plutchik,
  Repair, Living Pulse, Ontoject, Jungian). Each card: *What it is · Who & when ·
  What it changed · What descends from it · link to its repo grammar / Supabase deck.*
- **L1 (tradition stubs)** — Court de Gébelin, Lévi, Papus, Golden Dawn: the
  people/ideas that shaped decks without leaving a usable PD deck.
- **L2 = branches** — Hand-painted luxury · Other early Italian · Printed Marseille
  · French occult · English esoteric · Modern derivatives. Each `composite_of` its
  L1 decks.
- **L3 = the two families** — *the game tradition* vs *the divinatory/esoteric
  tradition* — or a single root node "The Tree of Tarot".
- **Edges:** add `metadata.derives_from: [deck-id]` on each L1 so a future graph
  view can draw explicit ancestry arrows, not just containment.

This reuses the existing L1/L2/L3 `composite_of` machinery — the viewer already
renders composites, so the tree falls out of the data with no new format.

**Open question for the author:** should the meta-grammar also fold in the
non-tarot card-oracle siblings already in the repo/DB (Petit Lenormand; and
further out, Plutchik's psychological wheel), as a separate "cartomancy cousins"
branch — or stay strictly the European *tarot* line?

> Status: **design only.** Build when the author says go. The four historical
> decks + Etteilla I + Minchiate should ideally exist first, so the tree has real
> leaves to point at.
```
