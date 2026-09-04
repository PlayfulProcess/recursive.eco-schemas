# Build Log: The Life of the Bee

**Grammar**: `grammars/life-of-the-bee/grammar.json`
**Source**: `seeds/life-of-the-bee.txt` (Project Gutenberg #4511, Maurice Maeterlinck, Alfred Sutro translation, 1901)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 12 (8 L1 chapters + 3 L2 themes + 1 L3 meta)

---

## Source Analysis

- Origin: Project Gutenberg eBook #4511, Maurice Maeterlinck, "The Life of the Bee" (Alfred Sutro translation, 1901)
- Structure: 8 chapters, each with a Roman numeral and title in the format "I -- ON THE THRESHOLD OF THE HIVE"
- Lyrical, philosophical natural history — Maeterlinck blends observation with meditation
- Seed file was originally downloaded with the wrong Gutenberg number (#18852 instead of #4511) — caught by verify_seed() check

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Chapter detection (attempt 1) | Regex for bare Roman numeral on its own line | FAILED — 0 chapters found |
| 2. Chapter detection (attempt 2) | Regex for `I -- TITLE` pattern | SUCCESS — 8 chapters found |
| 3. Seed verification | verify_seed() check against expected title/content | SUCCESS — caught wrong Gutenberg number on first download |
| 4. Content extraction | All text between chapter headings | SUCCESS |
| 5. Boilerplate removal | Strip Gutenberg header/footer | SUCCESS |
| 6. L2 groupings | Thematic clusters around hive life, swarm/reproduction, and philosophical reflection | SUCCESS — 3 L2 themes |

## Key Learnings

- **Heading format varies between Gutenberg editions — always check the actual format in the seed, don't assume.** The initial parser expected bare Roman numerals on their own line (a common Gutenberg pattern). The actual format was `I -- ON THE THRESHOLD OF THE HIVE` with numeral, double dash, and title on the same line. This caused the parser to find 0 chapters initially.
- **Adding a fallback chain of heading patterns makes parsers more robust.** Try `I -- TITLE` first, then bare `I` on its own line, then `BOOK I`, then `CHAPTER I.` — the first pattern that matches wins. This prevents parser failures when the heading format doesn't match expectations.
- **The verify_seed() pattern is reusable — check that the file is actually the right book before parsing.** The seed was originally downloaded with Gutenberg #18852 (a different edition or work entirely). A simple check that the file contains the expected title or author name prevents wasted parsing effort on the wrong text.
- **Maeterlinck's chapters are long, flowing essays** — no sub-sections, no numbered paragraphs. Each chapter becomes a single block of text in the grammar.

## Reusable Patterns

- **Heading pattern fallback chain**: Try multiple heading formats in order of specificity — prevents parser failures when Gutenberg formatting doesn't match expectations
  ```python
  patterns = [
      r'^([IVX]+)\s+--\s+(.+)$',    # "I -- TITLE"
      r'^([IVX]+)\.\s+(.+)$',        # "I. TITLE"
      r'^CHAPTER\s+([IVX]+)',          # "CHAPTER I"
      r'^([IVX]+)\s*$',               # bare "I"
  ]
  ```
- **verify_seed() function**: Before parsing, check that the seed file actually contains the expected work — prevents silent failures from wrong downloads
- **For natural history / philosophical texts**: Expect long chapters with no internal structure — plan for single-section items

## Emergence Layer (L2/L3)

| Level | Category | Count | Examples |
|-------|----------|-------|---------|
| L2 | Thematic groups | 3 | The Hive & Its Order, Swarm & Reproduction, The Philosopher's Bee |
| L3 | Meta-category | 1 | Maeterlinck's Apiary |

## Prompt for Similar Tasks

```
Parse a natural history text with:
- Roman numeral + title headings (format varies — use fallback chain)
- Long flowing chapters with no internal structure
- Verify seed file is correct before parsing
Extract: chapter number, title, full text.
Group by thematic focus for L2.
Always verify the seed file matches the expected work.
```
