# Build Log: Celtic Fairy Tales

**Grammar**: `grammars/celtic-fairy-tales/grammar.json`
**Source**: `seeds/celtic-fairy-tales.txt` (Project Gutenberg #7885, Joseph Jacobs compiler, John D. Batten illustrator, 1892)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 32 (26 L1 tales + 5 L2 themes + 1 L3 meta)

---

## Source Analysis

- Origin: Project Gutenberg eBook #7885, "Celtic Fairy Tales" selected and edited by Joseph Jacobs, illustrated by John D. Batten (1892)
- Structure: 26 tales with ALL CAPS titles, preceded by a PREFACE and followed by NOTES AND REFERENCES
- Spelling inconsistencies between TOC and body text (e.g., "CONAL YELLOWCLAW" in TOC vs "CONALL YELLOWCLAW" in body)
- Celtic names are especially prone to variant spellings throughout the text

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Tale detection | ALL CAPS title lines in body text | SUCCESS — 26 tales found |
| 2. Content boundaries | Strip PREFACE and NOTES AND REFERENCES sections | SUCCESS |
| 3. Spelling verification | Cross-check each title between TOC and body | CAUGHT 1 mismatch — Conal/Conall |
| 4. Manual fix | Correct spelling inconsistency in ID and title | SUCCESS |
| 5. Section creation | Story + Reflection sections per tale | SUCCESS |
| 6. L2 groupings | Thematic clusters: Heroic Quests, Enchantment & Magic, Tricksters & Wit, Animals & Transformation, Family & Loyalty | SUCCESS — 5 L2 themes |

## Key Learnings

- **Spelling inconsistencies between TOC and body text are common in Gutenberg texts — always verify each title match.** The TOC listed "CONAL YELLOWCLAW" while the body text had "CONALL YELLOWCLAW". This caused a silent mismatch where the parser couldn't find the tale by its TOC title. A post-parse verification step that checks all expected titles were found catches these errors.
- **Celtic names are especially prone to variant spellings.** Conal/Conall, Gannon/Ganon, and other Gaelic names appear in multiple forms even within a single text. When generating IDs, normalize to one spelling and note variants in keywords.
- **The Indian Fairy Tales parser pattern (STORY_DEFS with title, id, name, keywords, reflection) is directly reusable for any fairy tale collection.** The same data structure works for Celtic, Indian, Norse, or any culture's tale collection — define each story's metadata upfront, then parse the text to fill in the story content.
- **PREFACE and NOTES AND REFERENCES must be stripped** — Jacobs' scholarly notes are interesting but are not the tales themselves. They contain source attributions and comparative folklore references that could be useful as metadata but don't belong in the story text.

## Reusable Patterns

- **STORY_DEFS pattern for fairy tale collections**: Pre-define each tale's metadata (title, id, keywords, reflection prompt) in a dictionary, then match against the parsed text
  ```python
  STORY_DEFS = [
      {"title": "CONALL YELLOWCLAW", "id": "conall-yellowclaw",
       "keywords": ["hero", "quest"], "reflection": "..."},
      ...
  ]
  ```
- **Title verification**: After parsing, check that every expected title was found and every found title was expected — catches spelling mismatches
- **For fairy tale collections**: Strip preface, notes, and scholarly apparatus — keep only the tales
- **For children's content**: Always include a "Reflection" section with discussion questions

## Emergence Layer (L2/L3)

| Level | Category | Count | Examples |
|-------|----------|-------|---------|
| L2 | Thematic groups | 5 | Heroic Quests, Enchantment & Magic, Tricksters & Wit, Animals & Transformation, Family & Loyalty |
| L3 | Meta-category | 1 | The Celtic Imagination |

## Prompt for Similar Tasks

```
Parse a fairy tale collection with:
- ALL CAPS tale titles
- PREFACE and NOTES sections to strip
- Potential spelling inconsistencies between TOC and body
Extract: tale title, full story text.
Add Reflection section with discussion questions.
Use STORY_DEFS pattern for pre-defined metadata.
Verify all titles match between TOC and body.
Group by theme for L2.
```
