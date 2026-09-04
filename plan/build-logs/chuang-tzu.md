# Build Log: Chuang Tzu

**Grammar**: `grammars/chuang-tzu/grammar.json`
**Source**: `seeds/chuang-tzu.txt` (Project Gutenberg #59709, Herbert Giles translation, 1889)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 41 (33 L1 chapters + 6 L2 themes + 2 L3 meta)

---

## Source Analysis

- Origin: Project Gutenberg eBook #59709, Herbert A. Giles translation "Chuang Tzu: Mystic, Moralist, and Social Reformer"
- Structure: 33 chapters numbered CHAPTER I. through CHAPTER XXXIII., each with a title on the following line
- Each chapter has an _Argument_ line summarizing its content — a scholarly convention from Giles
- Contains introduction, index, and errata sections that must be stripped
- The traditional division into Inner Chapters (1-7), Outer Chapters (8-22), and Miscellaneous Chapters (23-33) is well-established in the scholarly tradition

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Chapter detection | Regex for `CHAPTER I.` through `CHAPTER XXXIII.` headings | SUCCESS — 33 chapters found |
| 2. Title extraction | Title on the line following the chapter heading | SUCCESS |
| 3. Argument extraction | Lines beginning with or containing _Argument_ provide chapter summaries | SUCCESS — used for metadata |
| 4. Content stripping | Remove introduction, index, errata, Gutenberg boilerplate | SUCCESS |
| 5. L2 groupings | Traditional inner/outer/miscellaneous + thematic groupings | SUCCESS — 6 L2 themes |
| 6. Unicode handling | Preserve diacritical marks in names (Tzŭ, Chê, Kêng) | SUCCESS |

## Key Learnings

- **Giles translation has _Argument_ lines summarizing each chapter** — these are valuable as metadata summaries and can be used for item descriptions or keywords. A reusable pattern for any scholarly translation with argument/summary lines.
- **Unicode characters in chapter titles (Tzŭ, Chê, Kêng) must be preserved correctly.** Ensure the parser reads and writes UTF-8 consistently. These diacritics carry meaning — Tzŭ is not Tzu in Giles' transliteration scheme.
- **33 chapters is a large flat list — thematic groupings help navigation.** The traditional inner/outer/miscellaneous division provides a scholarly axis, while thematic groupings (freedom, knowledge, governance, death, etc.) provide a reader-friendly axis.
- **The inner/outer/miscellaneous division is itself meaningful.** Inner Chapters (1-7) are considered authentically Chuang Tzu's; Outer and Miscellaneous are later additions or student compilations. This provenance information belongs in L2 descriptions.

## Reusable Patterns

- **For texts with Roman numeral chapter headings**: Use `CHAPTER\s+((?:X{0,3})(?:IX|IV|V?I{0,3}))\.\s*` — handles up to XXXIX
- **For scholarly translations with _Argument_ summaries**: Extract these as metadata/description fields rather than including them in the main text body
- **For Chinese philosophical texts**: The inner/outer/miscellaneous chapter division is a common organizational pattern (also seen in Tao Te Ching commentaries and Liezi)
- **For large chapter counts (30+)**: Create thematic L2 groupings to make the grammar navigable — readers rarely want to browse 33 items linearly

## Emergence Layer (L2/L3)

| Level | Category | Count | Examples |
|-------|----------|-------|---------|
| L2 | Thematic groups | 6 | Freedom & Spontaneity, Knowledge & Transformation, Governance & Society, Death & Acceptance, Language & Paradox, The Sage's Way |
| L3 | Meta-categories | 2 | The Scholarly Tradition (inner/outer/miscellaneous), The Daoist Path (thematic) |

## Prompt for Similar Tasks

```
Parse a classical Chinese philosophical text in scholarly translation with:
- CHAPTER I. through CHAPTER XXXIII. headings
- Title on the following line
- _Argument_ summary lines per chapter
- Introduction and index to strip
Extract: chapter number, title, argument (as metadata), full text.
Group by traditional scholarly division AND by theme.
Preserve all Unicode diacritics in transliterated names.
```
