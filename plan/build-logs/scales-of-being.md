# Build Log: Scales of Being

**Grammar**: nature/scales-of-being/grammar.json
**Source**: from-memory (with reference texts downloaded)
**Type**: from-memory
**Status**: NOT STARTED — strategy abandoned

## What Was Planned

A combined science + animist/indigenous/Hindu grammar covering scales of existence from quantum fields to the cosmos. ~44 L1 items, 10 L2 groups, 3 L3 meta-categories. Custom grammar type in `nature/` folder.

## Source Texts Downloaded

10 public domain texts were downloaded to `sources/` for this and related grammars:
- Darwin's Origin of Species (Gutenberg #1228)
- Darwin's Voyage of the Beagle (Gutenberg #944)
- Euclid's Elements (Gutenberg #21076)
- Bhagavad Gita (Gutenberg #2388)
- Yoga Sutras of Patanjali (Gutenberg #2526)
- The Upanishads (Gutenberg #3283)
- Kama Sutra (Gutenberg #27827)
- Sacred Books of the East (Gutenberg #12894)
- Vedanta-Sutras (Gutenberg #16295)
- King James Bible (Gutenberg #10)

## Why It Was Abandoned

The grammar scope was too large for a single from-memory session. 44 L1 items each requiring 6 rich content sections (scientific, indigenous, Hindu, scale comparisons, reflections) across multiple knowledge domains proved unwieldy. Multiple strategy pivots (direct JSON vs. Python generator) consumed time without producing output.

## Key Learnings

- **Scope creep kills momentum**: A grammar combining 3+ worldviews across 44 items is better split into multiple focused grammars or built incrementally.
- **From-memory grammars need tight scope**: 20-30 items with 2-3 sections each is the sweet spot. Beyond that, use source texts.
- **Decision paralysis**: Going back and forth between approaches (direct JSON vs. Python script) is worse than committing to either one.
- **Consider splitting**: Could work as 3 separate grammars (Science, Indigenous Worldviews, Hindu Cosmology) that reference each other.

## Future Approach

If revisited, consider:
1. Start with just the science layer (~20 items) using Darwin/Euclid sources
2. Add indigenous/Hindu perspectives as a second pass
3. Or build as separate grammars that share a thematic tag
