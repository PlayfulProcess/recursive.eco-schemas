# Build Log: The Dhammapada

**Grammar**: `custom/dhammapada/grammar.json`
**Source**: `sources/Dhammapada` (86KB, plain text)
**Type**: from-source-text (sacred text)
**Status**: COMPLETE
**Items**: 431 (405 L1 verses + 26 L2 chapters)
**File size**: 258K

---

## Source Analysis

- Origin: Project Gutenberg eBook #2017, F. Max Muller translation (1881)
- 26 chapters, each with a thematic title (The Twin-Verses, On Earnestness, etc.)
- 405 numbered verses (some traditional numbers skipped in this translation — e.g., 58-59, 195-196, etc.)
- Clean formatting: chapter titles on standalone lines, verses start with `N. ` at beginning of line
- Blank lines between verses

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Chapter detection | Regex `^Chapter ([IVXLC]+)\.\s*(.+?)\.?\s*$` | SUCCESS — found all 26 chapters instantly |
| 2. Verse detection | Regex `^\d+\.\s` at start of line within each chapter | SUCCESS — found all 405 verses |
| 3. Verse text cleanup | Normalize line wraps to spaces | SUCCESS — produces clean single-paragraph text |
| 4. L2 briefs | Hand-written thematic summaries for all 26 chapters | SUCCESS |
| 5. Validation | 0 orphan refs, 0 unreferenced L1 | PASS |

## Key Learnings

- **The Dhammapada is the EASIEST sacred text to parse.** Numbered verses, clean chapter headers, blank-line separators — everything just works.
- **No delimiter ambiguity.** Unlike Confucius (where speaker attributions were the only delimiter), the Dhammapada has explicit verse numbers.
- **Skipped verse numbers are fine.** The grammar uses the actual verse numbers (1, 2, ... 423) even though some are missing. This preserves scholarly referenceability.
- **This is the template for parsing verse-numbered sacred texts** (Bhagavad Gita, Tao Te Ching, etc.).

## What Worked vs. Confucius

| Aspect | Dhammapada | Confucius |
|--------|-----------|-----------|
| Delimiter | Explicit verse numbers | Speaker attributions (implicit) |
| Parsing attempts | 1 (first try) | 3 (two failures) |
| Blank line separation | Yes | No |
| Chapter summaries | Written by hand | Written by hand |
| Difficulty | EASY | MEDIUM |

## Reusable Patterns

For the website assistant when parsing verse-numbered sacred texts:
- Split on `^Chapter` or `^Book` for top-level divisions
- Within each division, split on `^\d+\.\s` for individual verses
- Normalize line wraps to spaces within each verse
- Preserve original verse numbers in IDs and metadata

## Prompt for Similar Tasks

```
Parse a verse-numbered sacred text with named chapters.
Chapters start with "Chapter N. Title" on their own line.
Verses start with a number and period (e.g., "1. ").
Split on chapter headers first, then verse numbers within each chapter.
This is the simplest sacred text pattern.
```
