# Build Log: Sojourner Truth

**Grammar**: `grammars/sojourner-truth/grammar.json`
**Source**: `seeds/sojourner-truth.txt` (Project Gutenberg #1674, dictated by Sojourner Truth, edited by Olive Gilbert, 1850)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 39 (31 L1 chapters + 7 L2 themes + 1 L3 meta)

---

## Source Analysis

- Origin: Project Gutenberg eBook #1674, "Narrative of Sojourner Truth" dictated by Sojourner Truth, edited by Olive Gilbert (1850)
- Structure: ~31 chapters with ALL CAPS headings in the body text
- Table of contents at the beginning also uses ALL CAPS titles — identical format to the body headings
- Short chapters — the narrative is divided into many brief sections covering episodes of Truth's life
- Strong narrative arc from slavery through escape to prophetic ministry

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Chapter detection (attempt 1) | ALL CAPS title lines throughout file | PARTIAL — matched TOC entries as well as body headings |
| 2. TOC skipping | Only match headings after body text begins (~line 98) | SUCCESS — 31 chapters found |
| 3. Content extraction | All text between chapter headings | SUCCESS |
| 4. Section naming | Use "Narrative" as primary section name | SUCCESS — fits autobiography genre |
| 5. Boilerplate removal | Strip Gutenberg header/footer, TOC | SUCCESS |
| 6. L2 groupings | Follow narrative arc: childhood, loss, trials, escape, spiritual awakening, prophet's world, voice | SUCCESS — 7 L2 themes |

## Key Learnings

- **When a Gutenberg text has a TABLE OF CONTENTS with the same format as the body headings, you must skip the TOC to avoid double-matching.** The TOC listed all chapter titles in ALL CAPS — the same format used in the body. Without skipping the TOC, the parser would create duplicate entries or garbled content from the TOC lines.
- **The narrative arc itself suggests natural L2 groupings.** Truth's life story has clear phases: childhood in slavery, separation and loss, trials and hardship, escape to freedom, spiritual awakening, prophetic ministry, and her public voice. These aren't imposed categories — they follow the structure of the life being told.
- **Autobiography/narrative requires "Narrative" section name** rather than "Text", "Verse", or "Essay". The section name should reflect the genre — a narrative is being told, not recited or argued.
- **Short chapters in autobiography often cover single episodes or themes.** This makes keyword extraction straightforward — each chapter's topic is focused and clear.
- **Dictated narratives have a distinctive voice** — Sojourner Truth's speech patterns come through even in Gilbert's editing. Preserving this voice means keeping the text intact without summarization.

## Reusable Patterns

- **TOC detection and skipping**: Scan for the end of the table of contents before beginning chapter detection — look for a blank line gap or a known marker (e.g., "PREFACE" or the first chapter heading's second occurrence)
- **For autobiographies/narratives**: Use the life arc as an L2 grouping axis — childhood, struggle, turning point, mission
- **For dictated/oral texts**: "Narrative" is the appropriate section name
- **For texts with short chapters**: Many brief items benefit even more from L2 groupings than long-chapter texts

## Emergence Layer (L2/L3)

| Level | Category | Count | Examples |
|-------|----------|-------|---------|
| L2 | Narrative arc themes | 7 | Childhood in Slavery, Separation & Loss, Trials & Hardship, Escape to Freedom, Spiritual Awakening, The Prophet's World, Sojourner's Voice |
| L3 | Meta-category | 1 | The Life of Sojourner Truth |

## Prompt for Similar Tasks

```
Parse an autobiography/narrative with:
- ALL CAPS chapter headings in body text
- Table of contents with identical formatting (must skip)
- Short episodic chapters
- Strong narrative arc
Extract: chapter title, full narrative text.
Skip the TOC by detecting where body text begins.
Group by life-arc phases for L2.
Use "Narrative" as the section name.
```
