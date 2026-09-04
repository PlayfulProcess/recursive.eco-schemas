# Build Log — Golden Dawn Tarot (Book T + RWS imagery)

**Grammar:** `grammars/golden-dawn-book-t-tarot/grammar.json`
**Generator:** `scripts/generate_golden_dawn.py`
**Type:** `tarot` · 84 items (22 majors + 56 minors + 6 emergences) · all 78 imaged
**Built:** May 2026 → main

## What this is
"The Golden Dawn version of Rider-Waite" — Pamela Colman Smith's public-domain
imagery carried by the full Hermetic Order of the Golden Dawn correspondence
system (Book T / Liber T, Mathers 1888). Built in direct response to the author's
stated favourite: a deck "built precisely within the tradition."

## Tradition depth (per card)
- **Majors:** Hebrew letter + Tree-of-Life path (11–32) + astrological attribution
  + Book T esoteric title ("The Spirit of Æther", "Daughter of the Flaming Sword", …)
  + divinatory + ill-dignified. Golden Dawn order (Strength VIII / Justice XI) noted.
- **Pips 2–10:** the 36 decans (Planet in Sign) + Sephirah-in-World + Book T
  "Lord of …" title + divinatory + ill-dignified.
- **Aces:** Root of the Powers of the element (Kether).
- **Courts:** RWS King/Queen/Knight/Page mapped to GD Prince/Queen/Knight/Princess,
  element-in-element, with ruling 30°+30° spans (Princesses → quadrant of the heavens).

## Research / accuracy
- Book T decans, "Lord of …" titles, and major attributions verified against the
  David Cunliffe and Mary K. Greer correspondence tables (WebFetch/WebSearch) — my
  table matched. Classical elemental attribution used for Fool/Hanged Man/Judgement;
  modern outer-planet overlay (Uranus/Neptune/Pluto) noted, not substituted.
- Court mapping (RWS↔GD) follows the standard correspondence:
  Knight=Knight (Fire), Queen=Queen (Water), King=Prince (Air), Page=Princess (Earth).

## Images
- **Reused** from the repo's `rider-waite-smith-tarot` grammar at build time (loads
  that JSON, keys by arcana/suit/number). No new image research; all 78 PD RWS scans.

## Validation
No dup IDs; all composite refs resolve; 84/84 sections populated. Manifest regenerated.

## Possible follow-ups
- Add the Golden Dawn elemental-dignity reading rules as an L3 "how to read" card.
- A purist variant using the GD's own flashing-colour scales instead of RWS imagery.
