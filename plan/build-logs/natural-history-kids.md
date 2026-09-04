# Natural History for Kids — Build Log

## Session 1 — 2026-03-06

### Grammars Planned
1. **Dinosaur Tree** — ~30 species, grouped by period/diet/clade
2. **Cosmic Unfolding** — ~30 events, Big Bang to now, NDT-style
3. **Wildflowers of California** — ~35 species by habitat/color/season
4. **Evolution Tree** — ~35 major transitions

### Age Target
Both tiers: "Story" section (ages 4-7) + "Science" section (ages 8-12) per item.

### Failure Log
- **Attempt 1**: Tried to write complete grammar.json with full content in one Write call. Timed out — too much content generation + JSON in a single shot.
- **Fix**: Use skeleton-first approach per CLAUDE.md. Write all items with "Placeholder." sections, validate, commit, then fill content item-by-item with Edit tool.

### Strategy (revised)
1. Write skeleton with all IDs, names, levels, categories, sort_orders, composite_of, keywords — sections set to "Placeholder."
2. Validate JSON immediately
3. Commit skeleton
4. Fill content system-by-system using Edit (one item at a time)
5. Validate completeness
6. Repeat for each grammar
