# Tarot — Execution Roadmap, Fix-List & Supabase Upload Log

The actionable companion to [`tarot-of-all-tarots-master-plan.md`](tarot-of-all-tarots-master-plan.md).
Three things in one place: (1) every deck still to build, (2) fixes owed to the
decks already built, (3) exactly what must be uploaded/updated in Supabase. Plus
the design for the genealogical "Tarot of All Tarots" default view.

_Last updated: June 2026._

---

## 1. Decks still to build (for an accurate account of tarot history)

Priority order. Legend: 🔨 buildable now (PD) · 🧩 needs image sourcing · ⛔ copyright.

### A. The earliest documentary record (15th–early 16th c.)
- 🔨 **"Charles VI" / Gringonneur deck** — Ferrara/Bologna, c. 1450–80; 17 trumps at the BnF. Often *mis*-called the oldest; a grammar can set the record straight. Images: Gallica/BnF, Wikimedia.
- 🧩 **Cary Sheet** (c. 1500) — earliest *Marseille-type* images, the proto-Marseille. Uncut sheet (Beinecke). One image, many cards — needs cropping.
- 🧩 **Rosenwald Sheet** — earliest evidence of the *standard* trump order. Uncut sheet.
- 🧩 **Estensi / d'Este** (Ferrara) — completes the luxury-deck picture beside Visconti.

### B. The living regional Italian game decks
- 🔨 **Tarocchino di Bologna** (the REAL 62-card one) — four Papi, Bolognese order, pips 2–5 removed. **Gap not filled by the modern "Tarocchino Arlecchino."** Highest priority of this group.
- 🔨 **Tarocco Siciliano** — Sicily's unique deck (the "Fugitivo" and "Miseria").
- 🔨 **Tarocco Piemontese** — the Piedmont pattern.

### C. The Marseille family's siblings
- 🔨 **Tarot de Besançon / Swiss 1JJ** — Juno & Jupiter replace Popess & Pope.
- 🔨 **Belgian / Flemish (Vandenborre)** — Bacchus & Capitano Eracasse replace Popess & Pope.
- 🧩 **Marseille Type I** (Noblet 1650 / Dodal 1701) — and a pip-image upgrade for the Conver deck (see §2).

### D. The occult line (mostly done)
- 🔨 **Court de Gébelin's 1781 plates** — the first "Egyptian" theoretical deck (PD).
- Lévi / Papus = **tradition nodes** (no deck of their own — capture in the meta-grammar).
- ⛔ **Thoth** (Crowley–Harris, 1944) — in copyright. Reference only, never reproduce.

### E. The clarifying "not-actually-tarot" relative
- 🔨 **Mantegna Tarocchi** (E-series, c. 1465) — a 50-card educational engraving series constantly confused with tarot. A grammar precisely to explain it *isn't* one.

### F. The capstone
- 🔨 **"The Grammar of Tarot Grammars"** — the genealogical meta-grammar (see §4).

---

## 2. Fixes owed to decks already built

| Deck | Fix | Status |
|---|---|---|
| **Marseille (Conver)** | Add per-card "game, not divination" Tradition Note + name the game in the description | ✅ DONE (commit 87f0382) |
| **Marseille (Conver)** | Pip-image upgrade — most pips unimaged; swap in a fuller PD set from **Jean Dodal (1701)** or **Jean Noblet (1650)** | 🔨 TODO |
| **Marseille (Conver)** | Optionally make the reading-meanings *Marseille-specific* (directional pip-reading, Camoin–Jodorowsky), not generic/RWS | 🔨 OPTIONAL |
| **Visconti-Sforza, Cary-Yale, Minchiate** | These were GAME decks too — add the same short Tradition Note (reuse the Marseille note pattern) | 🔨 TODO |
| **Sola Busca** (live) | It slightly over-maps its sui-generis classical/alchemical trumps to the standard archetypes ("Traditional Equivalent: The Magician"). Soften to "later readers have likened it to…"; foreground the alchemical/humanist reading | 🔨 TODO (live row — see §3) |
| **Etteilla I / II / III** (rewrites) | Source the **period two-word keyword inscriptions** from Etteilla's *Cours théorique* / Benebell Wen and add to each card (deliberately not fabricated) | 🔨 TODO |
| **Golden Dawn (Book T)** | Optional: add an L3 "how to read by elemental dignities" card; optional purist variant using GD flashing-colour scales instead of RWS art | 🔨 OPTIONAL |
| **Tarocchino Arlecchino** (live) | It's a *modern* Harlequin deck using Marseille names — fine as itself, but label it clearly as a modern homage, NOT the historical Bolognese Tarocchino | 🔨 TODO (live row) |

---

## 3. Supabase upload / sync log

**Project:** `Monorepo-dev` (`xtviwcznhbrsvkitepvm`) — the only ACTIVE project.
**Table:** `user_documents` (`document_type` = `unified_grammar` or `tarot_deck`,
`document_data` JSONB, `is_public` = true to appear in the channel).
**Images:** must be **R2** URLs (Wikimedia hotlinks are fine to render but the house
style is R2). New decks built with Wikimedia images should have images mirrored to
R2 before going live (desktop + R2 creds — see root CLAUDE.md).

### 3a. New repo decks NOT yet in the channel — need IMPORT (new rows)
| Repo grammar | Cards | Images | Action |
|---|---|---|---|
| `visconti-sforza-tarot` | 85 | Wikimedia | mirror to R2 → import → publish |
| `cary-yale-visconti-tarot` | 73 | Wikimedia | mirror to R2 → import → publish |
| `tarot-de-marseille-conver` | 83 | Wikimedia (22) | finish pips (§2) → mirror → import |
| `oswald-wirth-tarot` | 23 | Wikimedia | mirror to R2 → import → publish |
| `golden-dawn-book-t-tarot` | 84 | RWS Wikimedia | mirror to R2 → import → publish |
| `minchiate-florence-tarot` | 106 | Wikimedia | mirror to R2 → import → publish |

### 3b. Etteilla rewrites → UPDATE existing LIVE rows (do not create duplicates)
| Edition | Live row id | Repo grammar | Action |
|---|---|---|---|
| Etteilla I | `e4eea1e1-5909-4717-b4a4-db2c4361779b` | `etteilla-i-livre-de-thot` | UPDATE `document_data->items[].sections` (keep ids/images) |
| Etteilla II | `46527510-c021-48ad-af81-dce7a0ef797c` | `etteilla-ii-egyptian` | UPDATE sections |
| Etteilla III | `24a41f00-afa6-4b8e-8d2d-6f38d1921dc7` | `etteilla-iii-oracle-des-dames` | UPDATE sections |

> ⚠️ These touch **production public rows**. Do only with the author's explicit go-ahead.
> Recommended: write a one-off `scripts/sync-etteilla-to-supabase.mjs` that reads the
> repo grammar and PATCHes only the `sections` of each item by id, so images and
> metadata are untouched. Back up the rows first (`select document_data` → file).

### 3c. Live rows needing edits (not from repo)
- `Sola Busca` (`6e4394c2-…`) — soften archetype mapping (§2).
- `Tarocchino Arlecchino` (`7ea72ae9-…`) — relabel as modern homage (§2).
- General hygiene: many `(Copy)` / mislabeled (`grammar_type:"tarot"` on I-Ching) rows
  to prune so the channel reads cleanly.

### 3d. POST-import wiring — make the Tree of Tarot interactive
The reference mechanism is **already built** in recursive-eco: an item with
`item_type:"reference"` + `ref_document_id` (or `grammars:[id]`) renders as a link
that opens that document (`/play?id=…`), and a grammar can set
`default_preview:"tree"` (already set on `tree-of-tarot`). So AFTER the batch import,
patch each L1 deck-item in `tree-of-tarot` to add `item_type:"reference"` +
`ref_document_id:"<that deck's new Supabase id>"` so clicking a leaf opens the deck.
(Can't be done in-repo now — needs the post-import Supabase ids. One small patch
script after import.)

---

## 4. The genealogical "Tarot of All Tarots" default view

**The author's idea:** the default view of the meta-deck should be a *family tree* of
tarot — showing which deck descends from which. **Strongly endorsed.** Two notes:

### 4a. Get the genealogy RIGHT (scholarship)
Marseille is **not** a descendant of the Bolognese Tarocchino — they are **cousins**,
both descending from the mid-1400s Italian *trionfi* root. The backbone is **Michael
Dummett's A / B / C trump-order classification**:

- **A-order** = Bologna / Florence (south) → Tarocchino di Bologna, Minchiate
- **B-order** = Ferrara (east) → Charles VI / d'Este
- **C-order** = Milan (west) → the printed standard → **Tarot de Marseille** → occult decks

```
Italian trionfi (c.1440s)
├─ A-order (Bologna/Florence) ── Tarocchino di Bologna · Minchiate · Tarocco Siciliano
├─ B-order (Ferrara) ─────────── Charles VI · d'Este
└─ C-order (Milan) ──── Visconti/Cary-Yale ──► printed standard ──► Tarot de Marseille
                                                                     ├─ Besançon (Swiss) · Belgian
                                                                     └─ occult: Etteilla → Wirth → Golden Dawn → RWS → (Thoth)
   (Sola Busca = an early, sui-generis offshoot, not in any of the three orders)
```

### 4b. How to build it (data only — the viewer already exists!)
recursive.eco **already ships a tree-viewer** (`recursive.eco/pages/tree-viewer.html?type=custom&id=…`)
that renders the L1↔L2 `composite_of` emergence as a tree with connecting edges
(confirmed on "The 36 Tattvas" grammar: a LEVEL-2 row linked down to 47 BASE items).
So **no new frontend is needed** — the genealogy is just a matter of building the
right grammar data:

- **Data:** a `grammar_type: "custom"` meta-grammar whose **items are the decks**.
  - **L1** = each deck/tradition (sections: What it is · Where & when · Lineage
    (Dummett A/B/C order, descends-from, what-descends) · In this library).
  - **L2** = the branches — the **A / B / C trump-orders**, **the occult reframing**,
    and **sui-generis offshoots** — each `composite_of` its L1 decks. The tree-viewer
    draws these as the parent nodes with edges down to their decks.
  - **L3** = "The Tree of Tarot" root, `composite_of` the L2 branches.
  - Also stash `metadata.derives_from: ["<deck-id>", …]` on each L1 for a future
    precise-edge view, but it is NOT required — branch-grouping in the tree-viewer is
    enough to show the genealogy.

> Build order: (1) build this meta-grammar now (renders immediately in the existing
> tree-viewer), (2) backfill the missing early leaves (real Tarocchino di Bologna,
> Charles VI) so the A/B branches aren't thin, (3) optional precise-edge view later.

---

## 5. Suggested next actions (in order)
1. ✅ Tradition Note on Visconti / Cary-Yale / Minchiate (done).
2. ✅ Build the genealogical meta-grammar `tree-of-tarot` (done); ✅ Charles VI (done).
3. Build the missing leaves: real **Tarocchino di Bologna**, **Mantegna**, **Court de Gébelin**, Besançon/Belgian/Siciliano.
4. **Archetype/cross-deck axis prep** — stamp `metadata.archetype` on every card (§6). Unblocks the cross-deck view.
5. Write `scripts/sync-etteilla-to-supabase.mjs` and (on go-ahead) push the Etteilla rewrites live (§3b).
6. Mirror new-deck images to R2 and import all new decks + the tree to Supabase (§3a).
7. Frontend: the cross-deck "archetype" view (pills + search) in recursive-eco (§6).

---

## 6. Future feature: the cross-deck "archetype" axis (the SECOND view)

Author's idea: in the tree-viewer, show one card (e.g. **Death**) **across every deck
that has it** — a horizontal cut orthogonal to the vertical genealogy. Two views,
one dataset (the "infinite perspectives" principle).

### 6a. The join key is the whole problem
You **cannot** join on name or number across traditions:
- Etteilla **renumbered** Death to **17**; the Golden Dawn **swapped** Strength↔Justice (8↔11).
- Marseille's Death is **unnamed** (XIII); Visconti's is too.
- Minchiate has **20 trumps** (elements, zodiac) with **no standard equivalent**.
- Sola Busca's "Panfilio" only **loosely** maps to the Magician.

→ Solution: a **canonical archetype key** stamped on every card by MEANING:
`metadata.archetype` (controlled vocab) + `metadata.mapping_confidence`
(`exact` | `loose` | `none`/`sui-generis`). Then "all Death" is a `group-by`.
Proposed vocabulary:
- Majors: `major-00-fool` … `major-21-world` (21 standard archetypes).
- Minors: `minor-<suit>-<rank>` (e.g. `minor-cups-king`).
- Minchiate/extra: `extra-element-fire`, `extra-zodiac-scorpio`, `virtue-prudence`, etc. (own namespace, NOT forced into the 22).
- Sui-generis (Sola Busca, Mantegna): `archetype: null`, with a free `likened_to` note.

### 6b. UI: pills, backed by search
- The vocab is finite & famous → **pills/chips** for the 22 arcana + suits × ranks are the right UI.
- Keep free-text **search** for the long tail (Minchiate zodiac, Sola Busca figures).
- Pills ARE enumerated search facets — same engine, two surfaces.

### 6c. General principle, per-domain dictionary
Build the engine generic — "**correlate items across grammars by a shared
controlled-vocab key**." Tarot is the first dictionary; the same mechanism gives:
I Ching → every "Hexagram 1" across versions; mythology → every "trickster"; astrology
→ every "Mars" reading. The ENGINE is universal; the VOCABULARY is per `grammar_type`.

### 6d. Principled caveat
The key MUST allow `null` / `sui-generis` / `loose` so we never force false
equivalences (don't jam Minchiate's zodiac into a 22-slot; don't write "Panfilio =
Magician"). Honest non-mapping is a feature.

### 6e. Sequencing
- ✅ **Data prep DONE** — `scripts/stamp_archetypes.py` stamps `metadata.archetype` +
  `mapping_confidence` and canonical `namespace:value` hashtags into `keywords[]` across
  all 11 built decks (693 cards: 649 exact, 7 loose, 37 honest non-mappings). "All
  Death" now resolves across 11 decks; "King of Cups" across 8. **Re-run this after any
  deck generator** (generators don't add the keys) then `generate_manifest.py`.
- **UI (recursive-eco, later):** a cross-deck panel / pivot mode reading the key —
  pills over the canonical namespaces (`arcana:`, `suit:`, `rank:`, `element:`,
  `zodiac:`, `virtue:`), search over free keywords.
- The deck grammars can also be linked as sub-grammars under their L1 tree leaves so
  you can drill tree → deck → card, then pivot card → all-decks by archetype.

### 6f. Two model decisions (June 2026)

**(1) Hashtags on items = the archetype key.** Items already carry free `keywords`.
Make them first-class/clickable like grammar `tags`, in TWO tiers:
- **Canonical hashtags** (controlled namespace) — `#arcana:death`, `#suit:cups`,
  `#rank:king`, `#element:fire`, `#zodiac:scorpio`. These power the pills and the
  reliable cross-deck join. (This is the `metadata.archetype` from §6a, expressed as
  a hashtag.) Reserve the `namespace:value` form for canonical ones.
- **Free hashtags** (folksonomy) — `#skeleton`, `#endings` — discovery / search only.
- Pills surface the canonical namespace; search surfaces all. One feature, two tiers.

**(2) Items-as-grammars (full type unification): DEFERRED — do not build.**
Recursion already exists as composition (`composite_of` / `level` within a grammar)
and reference (the Tree of Tarot's deck-items pointing at deck-grammars). Full
unification would touch types + editor + viewer + `document_data` schema + a
migration of ~250 live grammars = production-app surgery, high risk, low marginal
value. Cheap alternative if drill-down is wanted: an optional **`grammar_ref`** field
on an item (link to a sub-grammar) — recursion by reference, not type-merge.
The Tree of Tarot already does this at the deck level; generalise only if needed.
