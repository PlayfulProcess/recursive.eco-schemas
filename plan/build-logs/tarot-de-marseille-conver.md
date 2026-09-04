# Build Log — Tarot de Marseille (Nicolas Conver 1760)

**Grammar:** `grammars/tarot-de-marseille-conver/grammar.json`
**Generator:** `scripts/generate_marseille_conver.py`
**Type:** `tarot` · 83 items (22 majors + 56 minors + 5 emergences) · 29 imaged
**Built:** May 2026, branch `claude/tarot-visconti-wirth` → main

## What this is
The canonical printed standard — Nicolas Conver's 1760 woodcut Tarot de Marseille,
the deck the entire occult era (Court de Gébelin, Etteilla, Lévi, Wirth) treated as
reference. Each major has Iconography + traditional Upright/Reversed; minors carry
traditional cartomantic meanings.

## Decisions
- **22 majors hand-authored** with Conver 1760 images and divinatory Upright/Reversed.
- **Pre-Golden-Dawn order preserved and flagged:** unnumbered Le Mat, Justice = VIII,
  Strength (La Force) = XI, Death (XIII) unnamed — called out in the description and
  the majors emergence card.
- **56 minors generated** from a suit-agnostic cartomantic spine coloured by suit;
  Marseille pips are emblematic (non-scenic), so this is meaning-first, not scene-first.

## Images
- Source: Wikimedia Commons, Category:Tarot de Marseille - Nicolas Conver 1760.
- Only **24 card images exist** there (22 majors + Ace of Batons + Ace of Swords),
  so 29/83 items are imaged (incl. emergence covers). Pip images deliberately left
  for a later pass.
- **Upgrade path:** the Jean Dodal (1701) and Jean Noblet (c. 1650) Marseille decks
  are public domain with fuller pip scans — swap those in to fully illustrate the minors.

## Gotchas
- Conver's woodblock mislabels the Empress as "II" (she is trump III); handled by
  keying on card identity, not the printed numeral. Note added on the card.
- Accented filenames (L'IMPÉRATRICE, L'ÉTOILE, As ÉPÉE) URL-encoded for Special:FilePath;
  spot-checked HTTP 200.

## Validation
Passes `scripts/validate.py`; no dup IDs, all composite refs resolve. Manifest regenerated.
