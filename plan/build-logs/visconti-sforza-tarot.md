# Build Log — Visconti-Sforza Tarot

**Grammar:** `grammars/visconti-sforza-tarot/grammar.json`
**Generator:** `scripts/generate_visconti_sforza.py`
**Type:** `tarot` · 85 items (22 majors + 56 minors + 7 emergences) · 80 with images
**Built:** May 2026, branch `claude/tarot-visconti-wirth`

## What this is
The Pierpont Morgan-Bergamo (Visconti-Sforza) deck, Milan c. 1451, workshop of
Bonifacio Bembo — the oldest tarot we can largely hold in our hands. Framed as a
**historical/iconographic** grammar, not a divination deck: each card has
`Iconography` (what Bembo painted), `History` (provenance/condition/story), and a
light `Reading`.

## Decisions
- **Full 78-card historical deck** (author chose this over majors-only).
- Pip content **generated combinatorially** (suit theme × number meaning) per the
  CLAUDE.md "content at scale" lesson — Visconti pips are non-scenic gilded
  emblem arrangements, so a lookup-table generator is the right tool. Majors and
  courts hand-authored.
- **Four lost cards kept as deliberate gaps** with `metadata.status: "lost"`:
  The Devil (15), The Tower (16), Knight of Coins, Three of Swords.
- **Six "second hand" trumps** flagged `metadata.painter_hand: "second"`
  (Fortitude, Temperance, Star, Moon, Sun, World — repainted c. 1480s–90s, attrib.
  Antonio Cicognara).
- L2 emergences: the Trionfi, the four suits, the Lost Cards, the Restoration Hand.

## Images
- Source: Wikimedia Commons, Category:Pierpont Morgan-Bergamo Visconti-Sforza Tarot.
- Filenames pulled live from the Commons API (`list=categorymembers`), not guessed.
- Majors use the clean `Visconti-sforza-NN-name.jpg` series; minors use
  `Bembo-Visconti-tarot-<suit>-NN...jpg` (suits: coins/cups/staves/swords).
- An embedded allowlist (`AVAILABLE_MINORS`) gates image attachment, so cards whose
  Commons upload is missing (e.g. King of Cups) simply get no `image_url` rather
  than a 404.
- URLs use `Special:FilePath/<urlencoded-filename>` (stable hotlink). Spot-checked
  HTTP 200. Inline render via `image_url` + `metadata.illustrations[]`.

## Gotchas / learnings
- The Commons category is **missing King of Cups** even though it survives in the
  physical deck — 5 cards end up without images (4 lost + King of Cups).
- Pre-occult numbering matters: Justice = VIII, and IX is "Il Tempo" (hourglass),
  not yet the lantern Hermit. Encoded in names + History notes.
- The Popess is almost certainly Sister Maifreda da Pirovano (Guglielmite heresy,
  burned 1300) — the single most historically loaded card; called out in History.

## Validation
`scripts/validate.py` — not among the repo's 31 pre-existing issues. Custom check:
no duplicate IDs, all `composite_of` refs resolve, no empty sections. Manifest
regenerated.

## Next steps (deferred)
- Dedicated illustration pass to perfect L2/emergence unique-image coverage.
- Optionally add a Visconti column to `tarot-of-all-tarots`.
