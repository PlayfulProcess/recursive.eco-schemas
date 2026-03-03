# Build Log: Meditations — Marcus Aurelius

**Grammar**: `classics/meditations-marcus-aurelius/grammar.json`
**Source**: `sources/meditations-marcus-aurelius` (Project Gutenberg, Meric Casaubon translation, 1634)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 365 passages across 12 books
**File size**: 448KB

---

## Source Analysis

- Origin: Project Gutenberg eBook #2680, Meric Casaubon translation (1634, oldest English translation)
- Structure: 12 books ("THE FIRST BOOK" through "THE TWELFTH BOOK"), each with Roman numeral passages (I., II., III., etc.)
- Book 1 is special: each passage is about a specific person Marcus learned from (grandfather, tutors, philosophers, Emperor Antoninus Pius, the gods)
- Text includes Introduction, Notes, Appendix, and Glossary — only the 12 books are extracted
- Passage lengths vary enormously: some are single sentences, others run 500+ words

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Background agent | Full agent parse | FAILED — timed out after ~58 minutes |
| 2. Book detection | Find "THE FIRST BOOK" through "THE TWELFTH BOOK" | SUCCESS — 12 books with APPENDIX as end marker |
| 3. Passage extraction (attempt 1) | Regex with lookahead for next Roman numeral | PARTIAL — Book 12 returned 0 passages (end boundary issue) |
| 4. Passage extraction (attempt 2) | Find marker positions, then extract text between markers | SUCCESS — 365 passages, all 12 books |
| 5. Book 1 naming | Map passage numbers to people Marcus thanks | SUCCESS — 17 named entries |
| 6. Keyword tagging | Theme-based keyword detection (15 Stoic themes) | SUCCESS — rich distribution |

## Key Learnings

- **Marker-based extraction beats regex lookahead for Roman numerals.** The first attempt used a single regex with lookahead patterns — this broke at book boundaries. The fix: find all marker positions first (`re.finditer`), then extract text between adjacent markers. Simpler and more reliable.
- **Book 12 boundary is APPENDIX, not another book title.** The regex lookahead for "THE ... BOOK" naturally missed Book 12 because APPENDIX doesn't match. Using an explicit end-of-content marker solves this.
- **Roman numeral regex**: `((?:X{0,3})(?:IX|IV|V?I{0,3}))\.` handles I through XXXIX. The Meditations only goes to XXXIX (Book 4 has 39 passages).
- **Book 1 is structurally unique** — it's a gratitude list, not a meditation. Each passage names a person and what Marcus learned from them. Naming these passages (e.g., "Book 1.4 — Rusticus") makes them far more navigable.
- **Stoic keyword themes distribute well across the text**: nature (199), reason (183), soul (153), time (146), virtue (142). These make good filter criteria.
- **Background agents are not suited for texts requiring iterative debugging.** Both Art of War and Meditations needed multiple parsing attempts. Direct scripting with visible output is faster for these cases.

## Reusable Patterns

- **For Roman-numeral-delimited texts**: Find all markers, extract between adjacent positions
- **For multi-book texts**: Always include an end-of-content marker (appendix, colophon, etc.)
- **For gratitude/attribution texts (like Book 1)**: Map person names manually — they can't be auto-extracted reliably
- **Stoic/philosophical texts** benefit from theme-based keywords: nature, reason, virtue, death, impermanence, duty, anger, opinion, gods, contentment, community, time, body, soul, philosophy

## Prompt for Similar Tasks

```
Parse a philosophical text divided into books with Roman numeral passages.
1. Find book boundaries by title ("THE FIRST BOOK", etc.)
2. Use an end marker (APPENDIX, GLOSSARY) for the final book
3. Find Roman numeral markers within each book
4. Extract text between adjacent markers
5. Tag passages with thematic keywords
6. Book 1 may have a special structure (gratitude list) — handle separately
```
