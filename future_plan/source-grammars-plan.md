# Source Grammars Build Plan

## Strategy

**Pattern** (established by Alice in Wonderland and Winnie-the-Pooh):
- L1 = passages/scenes containing original source text (section: "Story" or "Teaching")
- L2 = chapters/books as emergent composites of their L1 children (section: "Brief" summary)
- `composite_of` on each L2 lists the L1 IDs it contains
- `relationship_type: "emergence"` on L2 items
- Single section per level — keeps it clean for the reader
- No image URLs
- `grammar_type: "custom"`

**Parse approach**: Python script per source that:
1. Reads the source file
2. Detects structural delimiters (book numbers, act/scene markers, etc.)
3. Splits text into passages at paragraph boundaries
4. Emits JSON items for L1 passages + L2 chapter composites
5. Validates referential integrity before writing

---

## 1. Confucius — The Analects

**Source**: `sources/confucius` (2,729 lines, plain text)
**Output**: `custom/confucian-analects/grammar.json`

### Structure discovered
- 20 books, delimited by centered numbers (`^\s*\d+\s*$`)
- Book boundaries at lines: 7, 95, 203, 322, 409, 545, 676, 819, 923, 1060, 1202, 1371, 1539, 1712, 1935, 2094, 2246, 2420, 2522, 2658
- Within each book: individual teachings separated by paragraph breaks
- Each teaching begins with "The Master said" or similar attribution

### Strategy
- L1: Individual teachings/passages (section: "Teaching" with original text)
- L2: The 20 books (section: "Brief" with summary of the book's themes)
- Parse by splitting on book number delimiters, then splitting each book's content on double-newlines to get individual passages
- Expected item count: ~490 passages + 20 books ≈ **510 items**

### Risk
- Passage boundaries may not be perfectly consistent (some "paragraphs" may be continuations)
- The Legge translation uses archaic phrasing that might confuse boundary detection

---

## 2. Zohar

**Source**: `sources/zohar` (413 lines, JSON)
**Output**: `custom/zohar/grammar.json`

### Structure discovered
- JSON format with a header line followed by structured data
- 53 Torah portion names as section keys (Bereshit, Noach, Lech Lecha, etc.)
- **PROBLEM: Almost entirely empty**. Only `Bereshit[85]` has actual text — 7 short passages about flame meditation / mystical unity
- 52 out of 53 sections are completely empty arrays
- The "Addenda" section has a dict with 3 empty volumes

### Strategy
- **STRATEGY WILL NOT WORK** as planned. There is not enough source text to build a chapter-book grammar. The source file is essentially a skeleton/schema with section names but no content.
- **Fallback options**:
  - (a) Build a grammar from just the 7 Bereshit passages + the 53 section names as L1 placeholders
  - (b) Use the section names as L1 items and write brief descriptions of each Torah portion's Kabbalistic themes
  - (c) Skip Zohar entirely and note it needs a better source
  - (d) Find the actual text content online and supplement

### Decision needed
- Flag to user that source is mostly empty. Recommend option (b): use the 53 parashah names as L1 items with Kabbalistic context written in, and group them by the 5 Books of Moses as L2 composites. This would produce ~58 items.

---

## 3. Shakespeare — Complete Works

**Source**: `sources/shakespeare` (196,395 lines, plain text)
**Output**: `custom/shakespeare-complete/grammar.json`

### Structure discovered
- 41 works listed in table of contents (lines 37-80)
- Includes: Sonnets (154), 36 plays, 4 longer poems
- Play structure: title in ALL CAPS → Dramatis Personae → ACT/SCENE markers → dialogue
- No consistent "THE END" delimiter between works (only appears once at line 2858 after Sonnets)
- Works appear in table-of-contents order

### Strategy
- This is too large for a single grammar (would be 3000+ items)
- **Phased approach**: Build one grammar per "group" of works, or pick the most famous plays
- Recommended first pass: **10 greatest plays** as a curated collection
  - Romeo and Juliet, Hamlet, Macbeth, Othello, King Lear, A Midsummer Night's Dream, The Tempest, Julius Caesar, Merchant of Venice, Twelfth Night
- L1: Individual scenes (section: "Scene" with original text)
- L2: Acts (section: "Brief" summary, composite_of scene IDs)
- L3: Plays (section: "Synopsis" + "Characters", composite_of act IDs)
- Parse by finding play title boundaries, then ACT/SCENE markers within each play

### Risk
- Play boundary detection may be tricky (titles appear in dialogue too)
- Some plays have prologues, epilogues, or inductions that don't fit the ACT/SCENE pattern
- 10 plays × ~20 scenes each × full text = very large grammar file
- May need to truncate to just the first play as a proof of concept

### Revised strategy if full approach is too large
- Start with ONE play (Hamlet or Romeo and Juliet) as proof of concept
- If it works cleanly, batch the remaining 9
- If text is too voluminous, consider shorter scene excerpts rather than full text

---

## Execution Order

| Step | Source | Est. Items | Complexity | Notes |
|------|--------|-----------|------------|-------|
| 1 | Confucius | ~510 | Medium | Clean structure, straightforward parse |
| 2 | Zohar | ~58 | Low (if text-light) | Source is mostly empty — needs fallback strategy |
| 3 | Shakespeare | ~200 per play | High | Start with 1 play, expand if successful |

---

## Strategy Log

_This section tracks what works and what doesn't during execution._

### Confucius
- [ ] Paragraph-boundary splitting works for individual teachings
- [ ] Book number detection finds all 20 books correctly
- [ ] L2 brief summaries accurately capture each book's themes
- [ ] Final validation passes (refs, sort_order, orphans)

### Zohar
- [ ] Source text is sufficient for grammar (UNLIKELY — flagged as risk)
- [ ] Fallback strategy (parashah names + written descriptions) produces useful grammar
- [ ] Final validation passes

### Shakespeare
- [ ] Play boundary detection correctly isolates individual plays
- [ ] ACT/SCENE parsing correctly splits within plays
- [ ] Full scene text fits reasonably in grammar items
- [ ] Proof-of-concept play grammar validates and looks good
- [ ] Batch processing of remaining plays works

---

_Plan created: 2026-03-02_
_Branch: claude/review-source-grammar-nmK0B_
