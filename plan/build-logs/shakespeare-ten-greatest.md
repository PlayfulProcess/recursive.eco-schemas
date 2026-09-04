# Build Log: Shakespeare — Ten Greatest Plays

**Grammar**: `custom/shakespeare-ten-greatest/grammar.json`
**Source**: `sources/shakespeare` (196,395 lines, 5.4MB, plain text)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 247 (187 L1 scenes + 50 L2 acts + 10 L3 plays)
**File size**: 1.4M

---

## Source Analysis

- Origin: Project Gutenberg eBook #100 (Complete Works)
- 44 works total (sonnets, 36 plays, poems)
- Table of Contents at lines 37-80 with exact titles
- Each play: Title (ALL CAPS) → Contents/Dramatis Personae → ACT/SCENE markers → dialogue
- Some plays use `ACT I.` (with period), others `ACT I` (bare)
- Smart/curly apostrophes (U+2019) in some titles

## Plays Included

| Play | Scenes | Acts | Largest Scene |
|------|--------|------|---------------|
| Romeo and Juliet | 24 | 5 | V.iii (14,860 chars) |
| Hamlet | 20 | 5 | II.ii (27,643 chars) |
| Macbeth | 28 | 5 | IV.iii (11,240 chars) |
| Othello | 15 | 5 | III.iii (21,987 chars) |
| King Lear | 26 | 5 | V.iii (16,120 chars) |
| A Midsummer Night's Dream | 9 | 5 | III.ii (20,987 chars) |
| The Tempest | 9 | 5 | I.ii (23,903 chars) |
| Julius Caesar | 18 | 5 | IV.iii (14,442 chars) |
| The Merchant of Venice | 20 | 5 | IV.i (20,832 chars) |
| Twelfth Night | 18 | 5 | V.i (18,233 chars) |

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Play boundary detection | Match TOC titles as standalone lines after line 83 | SUCCESS — found 44+ works |
| 2. Smart apostrophe | Title lookup with straight quotes | FAILED — "A MIDSUMMER NIGHT'S DREAM" uses U+2019 curly apostrophe |
| 2b. Smart apostrophe fix | Use actual Unicode char `\u2019` in lookup dict | SUCCESS |
| 3. Dramatis Personae skip | Find 2nd occurrence of "ACT I" to skip TOC/cast section | SUCCESS — reliably finds where actual play text begins |
| 4. ACT parsing (attempt 1) | Regex `^ACT ([IVX]+)$` (strict) | FAILED on Twelfth Night — uses `ACT I.` with trailing period |
| 4b. ACT parsing fix | Regex `^ACT ([IVX]+)\.?\s*$` (flexible) | SUCCESS — all 10 plays parse correctly |
| 5. SCENE parsing | Regex `^SCENE ([IVX]+)\.\s*(.*)` to capture scene number + location | SUCCESS |
| 6. Scene text extraction | Collect all lines between consecutive scene/act markers | SUCCESS |
| 7. 3-level hierarchy | L1=scenes, L2=acts (composite_of scenes), L3=plays (composite_of acts) | SUCCESS |
| 8. Validation | 0 orphan refs, 0 unreferenced L1 | PASS |

## Key Learnings

- **Unicode traps in Gutenberg texts.** Curly/smart apostrophes appear inconsistently. Always check actual encoding, don't assume ASCII.
- **Formatting inconsistency across plays.** Some plays use `ACT I.` (period), some use `ACT I` (bare). Always make structural markers flexible with optional punctuation.
- **Every play has a "fake" TOC section** before the actual text. The Contents/Dramatis Personae section lists ACT/SCENE headings in condensed form. The parser must skip to the SECOND `ACT I` to find actual play text.
- **3-level hierarchy works naturally for plays.** Scene → Act → Play maps perfectly to L1 → L2 → L3.
- **Scene text can be very large.** Hamlet II.ii is 27,643 chars. This is fine for storage but the website assistant should be aware of this for display purposes.
- **Dramatis Personae is useful metadata.** Extracted and stored in L3 "Characters" section.

## Reusable Patterns

For the website assistant, when processing plays/dramatic texts:
- **Play boundaries**: Match TOC titles as standalone lines. Handle Unicode variants.
- **Skip to real content**: Find the Nth occurrence of "ACT I" (N=2 for plays with a TOC section).
- **ACT/SCENE regex**: `^ACT ([IVX]+)\.?\s*$` and `^SCENE ([IVX]+)\.\s*(.*)` — always allow optional trailing punctuation.
- **3-level structure**: Scene (full text) → Act (composite) → Play (composite + cast list).

## Prompt for Similar Tasks

```
Parse a play from a Gutenberg-style complete works file.
1. Find play boundaries by matching the Table of Contents titles as standalone lines.
2. Watch for Unicode smart quotes/apostrophes (U+2019, U+201C, etc.).
3. Skip the condensed TOC/Dramatis Personae by finding the 2nd "ACT I".
4. Split on ACT markers (allow optional trailing period) and SCENE markers.
5. Build 3-level hierarchy: scenes → acts → plays.
6. Extract Dramatis Personae as metadata for the play-level item.
```

## What's Left

- 31 more plays + sonnets + poems available in the source file
- Could expand to "Complete Works" grammar (~1000+ items)
- Sonnets would need a different parser (numbered, no ACT/SCENE structure)
- Poems (Venus and Adonis, Rape of Lucrece, etc.) would be single-item L1s
