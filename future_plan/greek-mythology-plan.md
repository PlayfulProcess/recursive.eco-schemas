# Greek Mythology & Astrology — Unified Grammar Build Plan

> **Purpose**: Master plan for a single unified grammar that serves as both a mythological family tree and an astrology source. Uses the Unified Items Standard with `composite_of` for genealogy and myth connections. English/Roman names for astrology chart compatibility. Categories (`planet`, `sign`) drive the astrology UI rendering.

See the full plan at: `.claude/plans/fuzzy-plotting-quail.md` (maintained during build sessions)

## Architecture

- **One file**: `custom/greek-mythology/grammar.json`
- **grammar_type**: `"astrology"` — chart UI integration
- **Categories**: `planet` → Planets tab, `sign` → Signs tab, others → filter pills
- **English names**: match chart positions by `name` (Jupiter, Aries, etc.)
- **Levels**: L1 Primordials+Signs → L2 Titans → L3 Titan children+First-gen Olympians → L4 Second-gen Olympians → L5 Heroes → L6 Myths
- **Target**: ~101 items (59 characters + 12 signs + 30 myths)

## Progress Tracker

| Commit | Status | Items | Running Total |
|--------|--------|-------|---------------|
| 1. Scaffold + Primordials | NOT STARTED | 8 | 8 |
| 2. Titans | NOT STARTED | 11 | 19 |
| 3. Titan Children + Latona | NOT STARTED | 7 | 26 |
| 4. First-Gen Olympians | NOT STARTED | 6 | 32 |
| 5. Planet Gods | NOT STARTED | 5 | 37 |
| 6. Other Olympians | NOT STARTED | 7 | 44 |
| 7. Supporting Characters | NOT STARTED | 5 | 49 |
| 8. Heroes Part 1 | NOT STARTED | 5 | 54 |
| 9. Heroes Part 2 | NOT STARTED | 5 | 59 |
| 10. Signs — Fire & Earth | NOT STARTED | 6 | 65 |
| 11. Signs — Air & Water | NOT STARTED | 6 | 71 |
| 12. Myths — Creation & War | NOT STARTED | 8 | 79 |
| 13. Myths — Love, Hubris | NOT STARTED | 10 | 89 |
| 14. Myths — Zodiac Placements | NOT STARTED | 12 | 101 |
| 15. Validation Pass | NOT STARTED | 0 | **101** |
