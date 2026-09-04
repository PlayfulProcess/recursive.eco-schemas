# Build Log: The Spirits' Book (Kardec)

**Grammar**: `grammars/spirits-book-kardec/grammar.json`
**Source**: `seeds/kardec-spirits-book` (Internet Archive OCR, Anna Blackwell translation, 1875)
**Type**: from-source-text (OCR)
**Status**: COMPLETE
**Items**: 33 (28 L1 chapters + 4 L2 books + 1 L3 meta)
**File size**: 443KB

---

## Source Analysis

- Origin: Internet Archive full-text OCR of Anna Blackwell's 1875 English translation
- Quality: **Poor OCR** — garbled text, random characters, broken line wraps, missing words
- Structure: Well-known 4-part structure (Book One through Book Four), with chapters within each book
- Q&A format (numbered questions with spirit answers) partially survives OCR because question numbers provide anchor points
- No clean Gutenberg edition available — Internet Archive OCR was the only accessible source

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. OCR assessment | Review text quality and identify usable structure | PARTIAL — text is garbled but section boundaries detectable |
| 2. Section boundary detection | Search for Book One/Two/Three/Four markers in OCR text | SUCCESS — 4 book boundaries found |
| 3. Chapter detection | Search for chapter headings within each book | SUCCESS — 28 chapters found using known structure as guide |
| 4. OCR cleanup | Remove lines < 3 chars, strip random symbols, collapse excessive blanks | SUCCESS — text readable if imperfect |
| 5. Q&A preservation | Look for numbered question patterns as anchor points | PARTIAL — many questions preserved, some garbled |
| 6. Known structure fallback | Use the published table of contents to guide parsing when OCR is too garbled | SUCCESS — known structure compensates for OCR noise |
| 7. L2 groupings | Kardec's own 4-book division: Causes, Spirits, Moral Laws, Hopes & Consolation | SUCCESS — 4 L2 books |

## Key Learnings

- **Internet Archive OCR is significantly worse than Gutenberg text.** Random characters, garbled words, broken line wraps, and single-character garbage lines throughout. A Gutenberg text requires light cleanup; Internet Archive OCR requires aggressive cleaning and structural inference.
- **Use the KNOWN structure of a well-documented work to find section boundaries even in messy text.** Kardec's "The Spirits' Book" has a well-documented 4-book structure with known chapter titles. Even when the OCR garbles the heading text, searching for partial matches or known keywords within a positional window finds the boundaries.
- **Clean aggressively for OCR text.** Remove lines shorter than 3 characters (usually garbage), strip obvious non-text symbols, collapse runs of blank lines. Accept that some artifacts will remain — note it in the grammar description so users understand the source quality.
- **The Q&A format survives OCR reasonably well because question numbers provide anchor points.** Numbered questions (Q1, Q2, etc.) are short, distinctive patterns that OCR tends to preserve. The answers following them can be extracted even when individual words are garbled.
- **Accept imperfection and document it.** OCR grammars will have artifacts. The grammar description should note: "Parsed from Internet Archive OCR scan — some text artifacts may be present." This is more honest and useful than attempting to manually fix every garbled word.

## Reusable Patterns

- **For OCR source texts**: Clean aggressively — remove short garbage lines, strip non-text characters, collapse blank runs
  ```python
  lines = [l for l in lines if len(l.strip()) >= 3]
  text = re.sub(r'[^\x20-\x7E\n]', '', text)  # strip non-printable
  text = re.sub(r'\n{3,}', '\n\n', text)       # collapse blanks
  ```
- **Known-structure fallback**: For well-documented works, use the published table of contents as a parsing guide — search for approximate matches rather than exact heading text
- **For Q&A format texts**: Use question numbers as anchor points for extraction — they survive OCR better than prose
- **For texts only available as OCR**: Note the source quality in the grammar description and `_grammar_commons` attribution
- **The verify_seed() pattern** (from Life of the Bee) could be extended to OCR texts — check for key phrases that should appear regardless of OCR quality

## Emergence Layer (L2/L3)

| Level | Category | Count | Examples |
|-------|----------|-------|---------|
| L2 | Kardec's 4 Books | 4 | Book One: First Causes, Book Two: The Spirit World, Book Three: Moral Laws, Book Four: Hopes & Consolations |
| L3 | Meta-category | 1 | Kardec's Spiritist Philosophy |

### Emergence Key Learning

- **When the author provides an explicit multi-level structure (Books containing Chapters), use it directly for L2.** Kardec organized his work into 4 books — these are the natural L2 groupings. No thematic interpretation needed; the author's own structure is the best emergence layer.

## Prompt for Similar Tasks

```
Parse an OCR-scanned philosophical text with:
- Heavily garbled text from Internet Archive
- Known multi-part structure (Book One through Four)
- Q&A format with numbered questions
- No clean digital edition available
1. Use known structure to find section boundaries
2. Clean OCR aggressively (strip garbage lines, non-printable chars)
3. Extract Q&A using question numbers as anchors
4. Document OCR quality in grammar description
5. Use author's own book divisions for L2
```
