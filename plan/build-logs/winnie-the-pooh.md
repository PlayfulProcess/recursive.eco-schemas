# Build Log: Winnie-the-Pooh — A Chapter Book

**Grammar**: `custom/winnie-the-pooh-chapter-book/grammar.json`
**Source**: `sources/pooh` (149KB, plain text)
**Type**: from-source-text
**Status**: COMPLETE (built in earlier session)
**Items**: 41 (31 L1 scenes + 10 L2 chapters)
**File size**: ~200K

---

## Source Analysis

- Origin: Project Gutenberg eBook #67098 (public domain since Jan 1, 2022)
- A. A. Milne, 1926 first edition
- 10 chapters, each with long descriptive titles
- Text is conversational, with songs/poems embedded

## Structure

- L1: Individual scenes within chapters (section: "Story" with full original text)
- L2: Chapters as composites (relationship_type: "emergence")
- ~3-4 scenes per chapter
- Clean paragraph-based splitting works here (unlike sacred texts)

## Key Learnings

- **Children's books have natural scene breaks.** Paragraph breaks, "* * *" dividers, and tonal shifts make good scene boundaries.
- **Chapter titles are the L2 names.** Milne's descriptive titles ("In Which Pooh Goes Visiting and Gets Into a Tight Place") work perfectly as composite names.
- **Full text is manageable.** Individual scenes are 1-3K chars — very comfortable for grammar items.
- **This is the ideal grammar type** for the "from-book" pattern: clean source, clear structure, reasonable size.

## Reusable Patterns

- **Scene splitting in children's books**: Look for scene dividers (`* * *`), chapter breaks, or natural pauses in the narrative.
- **Chapter composites**: Use chapter titles directly as L2 names.
- **Section naming**: "Story" for original text is clear and consistent.
