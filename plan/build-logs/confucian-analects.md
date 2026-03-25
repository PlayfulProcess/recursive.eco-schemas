# Build Log: The Confucian Analects

**Grammar**: `custom/confucian-analects/grammar.json`
**Source**: `sources/confucius` (2,729 lines, 158KB, plain text)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 749 (729 L1 teachings + 20 L2 books)
**File size**: 484K

---

## Source Analysis

- Origin: sacred-texts.com, James Legge translation (1893)
- Structure: 20 books, no blank-line separators, consistent 3-space indentation
- Each teaching begins with a speaker attribution ("The Master said", "The philosopher Yu said", etc.)
- No chapter titles — just numbered books

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Book detection | Regex `^\s+(\d+)\s*$` for centered numbers | SUCCESS — found all 20 books immediately |
| 2. Passage split (attempt 1) | Split on `\n\n` (double newline) | FAILED — no blank lines between passages, got 21 chunks (1 per book) |
| 3. Passage split (attempt 2) | Split on `\n(?=   [A-Z])` (newline + 3-space indent + capital letter) | SUCCESS — 729 passages, correctly identifies new speaker attributions |
| 4. Name generation | Extract speaker + first clause from each passage | SUCCESS — clean truncated names |
| 5. Name cleanup | Remove raw newlines from names | NEEDED FIX — initial pass left `\n` in names, added `.strip()` + re-truncation |
| 6. L2 book briefs | Manually written thematic summaries for each of the 20 books | SUCCESS |
| 7. Validation | Check orphan refs, unreferenced L1, sort_order | PASS — 0 orphans, 0 unreferenced |

## Key Learnings

- **Sacred text formatting is NOT paragraph-based.** Unlike novels, these texts use indentation-based formatting where speaker attributions signal new passages. Double-newline splitting is useless here.
- **Speaker attribution is the reliable delimiter.** Pattern: `\n` + 3 spaces + uppercase letter (starting a name/title). This works because the Legge translation consistently attributes every saying.
- **Continuation quotes look different.** Lines starting with `   "` (3 spaces + quote mark) are continuations of the same speaker, not new passages. The `[A-Z]` requirement naturally filters these out.
- **Book-level summaries must be written by hand.** The source text doesn't contain book summaries — these are thematic groupings that require editorial knowledge of the Analects.

## Reusable Patterns

For the website assistant, when processing similar texts:
- **Detect**: Is this indentation-based or paragraph-based? Check for `\n\n` between logical units.
- **If indentation-based**: Find the attribution pattern (speaker + "said") and split on it.
- **Book/chapter composites**: Use centered or standalone numbers/titles as structural delimiters.
- **Sacred texts often have NO summaries** — L2 briefs need to be generated or written.

## Prompt for Similar Tasks

```
Parse a sacred/philosophical text with speaker attributions.
The text uses indentation (not blank lines) to separate passages.
Each new teaching starts with a speaker name at 3-space indent.
Split on the pattern: newline followed by indent + uppercase letter.
Write thematic summaries for each book/chapter grouping.
```
