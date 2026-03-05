# Build Log: Legends of the Alhambra

**Grammar**: `grammars/legends-alhambra/grammar.json`
**Source**: `seeds/legends-alhambra.txt` (Project Gutenberg #49947, Washington Irving, "The Alhambra" 1832/1851)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 47 (41 L1 chapters/legends + 5 L2 themes + 1 L3 meta)

---

## Source Analysis

- Origin: Project Gutenberg eBook #49947, Washington Irving, "The Alhambra" (Author's Revised Edition, 1851; originally published 1832)
- Structure: 41 chapters with ALL CAPS titles in the body text
- Mixed content types — some chapters are travel essays and historical sketches, others are full legends and tales
- Accented characters appear in titles (FÊTES, Alcántara) requiring careful handling
- Legends tend to be significantly longer than essay chapters (30-60K chars vs 3-15K chars)

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Chapter detection | ALL CAPS title lines in body text | SUCCESS — 41 chapters found |
| 2. Content typing | Classify as "chapter" or "legend" based on title keywords | SUCCESS — titles containing "Legend", "Adventure", or recognizable tale names flagged as legends |
| 3. Accent handling | Case-insensitive and Unicode-normalized matching for FÊTES, Alcántara, etc. | SUCCESS |
| 4. Content extraction | All text between chapter headings | SUCCESS |
| 5. Boilerplate removal | Strip Gutenberg header/footer | SUCCESS |
| 6. L2 groupings | Thematic clusters: The Traveler's Alhambra, Moorish Legends, Treasure Tales, Historical Sketches, Enchantment & Wonder | SUCCESS — 5 L2 themes |

## Key Learnings

- **Irving's mix of essay and legend makes for a grammar with two reading modes.** Some readers will want the travelogue; others want the folk tales. The L2 groupings separate these concerns, letting readers choose their mode.
- **41 chapters is a large grammar** — without L2 emergence, browsing is overwhelming. The 5 thematic groups reduce cognitive load significantly.
- **Legends are much longer than essays (30-60K chars vs 3-15K chars).** This uneven length distribution is worth noting in metadata — readers should know some items are quick reads and others are substantial tales.
- **Title matching with accented characters (FÊTES) requires case-insensitive or normalized matching.** Python's `unicodedata.normalize('NFD', ...)` followed by accent stripping helps with matching, but the original accented forms should be preserved in the grammar output.
- **ALL CAPS detection needs to exclude short lines** (e.g., "I" or "II") that might be Roman numerals, not titles. A minimum length threshold (e.g., 5 characters) helps.

## Reusable Patterns

- **For mixed-genre texts (essay + tale)**: Classify each item by type and use the classification for L2 grouping — readers benefit from being able to filter by mode
- **For ALL CAPS title detection**: Use `line.strip().isupper() and len(line.strip()) > 4` to avoid false positives from short Roman numerals or single words
- **For accented characters in Gutenberg texts**: Normalize for matching but preserve originals in output
- **For 19th-century travel/legend collections**: Expect a mix of observation, history, and folklore — plan for multiple L2 axes

## Emergence Layer (L2/L3)

| Level | Category | Count | Examples |
|-------|----------|-------|---------|
| L2 | Thematic groups | 5 | The Traveler's Alhambra, Moorish Legends, Treasure Tales, Historical Sketches, Enchantment & Wonder |
| L3 | Meta-category | 1 | Irving's Alhambra |

## Prompt for Similar Tasks

```
Parse a 19th-century travel/legend collection with:
- ALL CAPS chapter titles
- Mixed content (essays and folk tales)
- Accented characters in titles
Extract: chapter title, full text, content type (essay vs legend).
Classify each chapter by genre.
Group by theme and content type for L2.
Handle Unicode normalization for title matching.
```
