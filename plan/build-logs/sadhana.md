# Build Log: Sadhana

**Grammar**: `grammars/sadhana/grammar.json`
**Source**: `seeds/sadhana.txt` (Project Gutenberg #6842, Rabindranath Tagore, 1913)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 13 (8 L1 essays + 3 L2 themes + 2 L3 meta)

---

## Source Analysis

- Origin: Project Gutenberg eBook #6842, Rabindranath Tagore, "Sadhana: The Realisation of Life" (1913)
- Structure: 8 essays/chapters with Roman numeral headings (I through VIII), each with a descriptive title
- Clean prose — Tagore's English is polished and requires minimal cleanup
- No inline commentary, footnotes, or scholarly apparatus to strip
- Short text overall — each essay is a self-contained meditation

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Chapter detection | Roman numeral headings I through VIII | SUCCESS — 8 essays found |
| 2. Title extraction | Title text on same line or following line after numeral | SUCCESS |
| 3. Content extraction | All text between chapter headings | SUCCESS — clean prose throughout |
| 4. Boilerplate removal | Strip Gutenberg header/footer | SUCCESS |
| 5. L2 groupings | Thematic clusters: Self & Soul, Relations & Love, Realization & Freedom | SUCCESS — 3 L2 themes |

## Key Learnings

- **Short philosophical essay collections are among the cleanest to parse.** Tagore's 8 essays have clear boundaries, no commentary to strip, and no encoding issues. This was one of the fastest grammar builds.
- **Essay titles carry strong thematic signals.** Titles like "The Relation of the Individual to the Universe" and "Realisation in Love" practically self-categorize into L2 themes — minimal interpretation needed.
- **Small item counts (8 L1) still benefit from L2 emergence.** Even with only 8 essays, grouping them into 3 themes helps readers find essays by interest rather than reading order.
- **Tagore writes in flowing paragraphs** — there are no verse numbers, no sub-sections, no structural markers within each essay. The entire essay becomes a single "Essay" section.

## Reusable Patterns

- **For essay collections with Roman numeral headings**: Simple regex `^(I{1,3}|IV|V|VI{0,3}|VII|VIII)\s` handles the typical range
- **For clean prose texts**: Skip the commentary-stripping pipeline entirely — just split on headings and extract
- **For small grammar counts**: Still add L2 emergence — it takes minimal effort and adds navigability
- **For Indian philosophical texts**: "Meditation" or "Contemplation" are good section names alongside the main essay text

## Emergence Layer (L2/L3)

| Level | Category | Count | Examples |
|-------|----------|-------|---------|
| L2 | Thematic groups | 3 | Self & Soul, Relations & Love, Realization & Freedom |
| L3 | Meta-categories | 2 | The Inner Journey, The Realized Life |

## Prompt for Similar Tasks

```
Parse a short essay collection with:
- Roman numeral chapter headings (I through VIII)
- Descriptive essay titles
- Clean prose with no commentary
Extract: essay number, title, full text.
Group by thematic affinity.
Minimal cleanup needed — focus on Gutenberg boilerplate removal.
```
