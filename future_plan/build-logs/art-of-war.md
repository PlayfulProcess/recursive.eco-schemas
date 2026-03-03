# Build Log: The Art of War

**Grammar**: `classics/art-of-war/grammar.json`
**Source**: `sources/art-of-war` (Project Gutenberg, Lionel Giles translation, 1910)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 376 verses across 13 chapters
**File size**: 230KB

---

## Source Analysis

- Origin: Project Gutenberg eBook #132, Lionel Giles translation with extensive commentary
- Structure: 13 chapters, each with numbered verses (e.g., "1. Sun Tzu said: The art of war...")
- **Critical issue**: Giles' edition interleaves Sun Tzu's verses with lengthy scholarly commentary in brackets `[...]` and footnotes
- Multi-numbered verses exist (e.g., "4, 5." for combined passages)
- Some verse numbers are compound: "1. Sun Tzu said:" vs just "1."

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Background agent | Full agent parse | FAILED — timed out after ~58 minutes |
| 2. Chapter detection | Regex for "Chapter I." through "Chapter XIII." | SUCCESS |
| 3. Commentary removal (attempt 1) | Regex bracket removal | PARTIAL — missed nested/multi-line brackets |
| 4. Commentary removal (attempt 2) | Character-level bracket parser | SUCCESS — removes all `[...]` content |
| 5. Verse extraction | Regex `(\d+(?:,\s*\d+)?)\.\s+` within chapter boundaries | SUCCESS — 376 verses |
| 6. Noise filtering | Filter by content length and prefix patterns | SUCCESS — clean Sun Tzu text only |

## Key Learnings

- **Background agents time out on complex parsing tasks.** The Art of War's interleaved commentary made this too complex for an agent to handle within the timeout. Direct Python scripting was necessary.
- **Character-level bracket removal is more reliable than regex** for texts with nested or multi-line bracketed content:
  ```python
  clean_parts = []
  in_bracket = False
  for char in raw_text:
      if char == '[': in_bracket = True
      elif char == ']': in_bracket = False; continue
      if not in_bracket: clean_parts.append(char)
  ```
- **Scholarly translations need commentary stripping.** Giles' translation is ~80% commentary by volume. The grammar should contain only Sun Tzu's text — the commentary is valuable but doesn't belong in a contemplative grammar.
- **Multi-numbered verses (e.g., "4, 5.") need special regex handling**: `\d+(?:,\s*\d+)?` captures both single and compound numbers.
- **Chapter boundaries must be pre-computed** to prevent cross-chapter verse matching. Using `start_pos`/`end_pos` pairs per chapter prevents the regex from matching commentary verse references in other chapters.

## Reusable Patterns

- **For texts with inline commentary**: Use character-level bracket/delimiter removal, not regex
- **For numbered verse texts**: Pre-compute chapter/section boundaries, then extract verses within each section
- **When agents time out**: Fall back to direct Python scripting with targeted regex
- **Scholarly translations**: Always check for commentary, footnotes, and editorial additions that should be stripped

## Prompt for Similar Tasks

```
Parse a classical text with numbered verses and inline commentary.
1. Identify chapter/section boundaries
2. Strip all commentary (bracketed text, footnotes)
3. Extract numbered verses within each section
4. Use character-level parsing for bracket removal (not regex)
5. Handle compound verse numbers (e.g., "4, 5.")
```
