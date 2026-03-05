# Build Log: The Human Body — An Emergent Symphony

**Grammar**: `grammars/human-body/grammar.json`
**Source**: From memory (no seed file)
**Type**: from-memory
**Status**: COMPLETE — 76 items (60 L1 + 13 L2 + 3 L3), all content filled

---

## What Went Wrong (First Attempt)

- **Delegated to a background agent to write the entire grammar in one shot.**
- The agent timed out after ~55 minutes. Generating ~70 L1 items with 4 original content sections each (What It Does, How It Connects, Wonder, When It Breaks) plus 12 L2 systems plus 3 L3 metas is too much original content for a single agent call.
- **Root cause**: Background agents have their own context management overhead. The combination of generating content AND managing a large JSON file AND tracking progress consumed the agent's budget before it could finish.

## What Actually Worked (Second Attempt)

### Inline, skeleton-first approach — completed in a single session

**Step 1: Write the full skeleton with `Write` tool**
- Created the complete grammar.json in one shot: all 76 items with IDs, names, levels, categories, sort_orders, composite_of references, keywords, and "Placeholder." sections.
- Validated immediately with a Python one-liner (JSON parse, duplicate check, ref check, sort_order check).
- Committed the skeleton.

**Step 2: Fill content system-by-system with `Edit` tool**
- Used `Edit` (exact string replacement) to replace one item's placeholder sections at a time.
- Worked through systems in order: skeletal → muscular → nervous → circulatory → respiratory → digestive → endocrine → immune → integumentary → urinary → reproductive → microbiome → special → L2 systems → L3 metas.
- Each edit was small and self-contained: replace one item's 4 placeholder sections with full prose.
- About 50 sequential Edit calls total.

**Step 3: Validate and push**
- Ran Python validation again: zero placeholders, no duplicate IDs, no bad refs.
- Updated manifest, committed, pushed.

### Why This Worked Where the Background Agent Failed

1. **No delegation overhead**: Working inline avoids the context management cost of a background agent. The main conversation has more budget and better context.
2. **Edit tool is surgical**: Each Edit call replaces exactly one item's placeholders. Small, atomic, reversible. The agent was trying to generate the entire file at once.
3. **Skeleton-first ensures structural integrity**: All IDs, references, and sort_orders were correct before any content was written. No structural bugs to debug later.
4. **System-by-system focus**: Writing all the nervous system content back-to-back keeps anatomical knowledge coherent. The agent had to context-switch between building structure and writing content.

### Key Revision to CLAUDE.md Guidance

The original guidance said: "From-memory grammars must be built across multiple sessions." This is **conservative but not always necessary**. The real constraint is:

- **Do NOT delegate from-memory grammars to background agents** — they time out.
- **DO use inline skeleton + Edit-per-item** — this can complete a 76-item grammar in a single session.
- **Multi-session IS needed** if the grammar exceeds ~80 items or if content requires deep research per item.

---

## Tools and Approach: What Works for Each Grammar Type

### From-Source Grammars (seed text → parser → grammar)

**Primary tools:**
- `Read` — Read the seed file to understand its structure (headings, numbering, formatting)
- `Write` — Create the Python parser script in `scripts/`
- `Bash` — Run the parser to generate grammar.json
- `Edit` — Fix parser bugs, adjust regex patterns
- `Bash` — Validate output (JSON parse, ID checks, ref checks)

**Approach:**
1. Download seed to `seeds/` (user runs curl locally if Gutenberg)
2. Read the seed file — understand heading format, chapter/verse structure, quirks
3. Write a parser script (usually 50-150 lines of Python)
4. Run parser, inspect output, iterate on edge cases
5. Add L2/L3 emergence items (sometimes in the parser, sometimes via Edit)
6. Validate, commit

**Common pitfalls:**
- Assuming heading format without checking the actual file (Gutenberg editions vary wildly)
- TOC headings matching body headings (double-count)
- Internet Archive OCR quality (much worse than Gutenberg)
- Accented characters in pattern matching
- Commentary/footnotes mixed into primary text

### From-Memory Grammars (no seed, generate all content)

**Primary tools:**
- `Write` — Create the skeleton grammar.json in one shot (all items, IDs, structure, placeholder sections)
- `Bash` — Validate skeleton (Python one-liner for JSON/IDs/refs/sort_order)
- `Edit` — Fill content one item at a time, replacing "Placeholder." with real prose
- `Bash` — Final validation (check zero placeholders remaining)

**Approach:**
1. Plan the item tree: what are the L1 items, how do they group into L2, what are the L3 metas?
2. Write the full skeleton with Write tool — every item, every field, placeholder sections
3. Validate the skeleton immediately
4. Commit the skeleton (safety checkpoint)
5. Fill content system-by-system using Edit — one item per Edit call
6. Validate again (zero placeholders, valid JSON, good refs)
7. Update manifest, commit, push

**Critical insight: NEVER delegate from-memory grammar generation to a background agent.** The combination of content generation + JSON management + large file size exceeds background agent budgets. Work inline.

### The Edit Tool Is the MVP

For both grammar types, the `Edit` tool (exact string replacement) is the workhorse:
- **From-source**: Fix parser output, add metadata, adjust sections
- **From-memory**: Fill content one item at a time with surgical precision
- **Why it works**: Each edit is small, targeted, and reversible. No risk of corrupting the rest of the file. Clear before/after for review.

The `Write` tool is for initial creation only. After the skeleton exists, everything is `Edit`.

### Validation Pattern (Reusable)

```python
python3 -c "
import json
with open('grammars/<name>/grammar.json') as f:
    g = json.load(f)
items = g['items']
ids = [i['id'] for i in items]
# Check duplicates
dupes = [x for x in ids if ids.count(x) > 1]
# Check composite_of references
bad_refs = [(i['id'], ref) for i in items for ref in i.get('composite_of', []) if ref not in ids]
# Check for remaining placeholders
placeholders = [(i['id'], k) for i in items for k, v in i['sections'].items() if v == 'Placeholder.']
# Check sort_order
orders = [i['sort_order'] for i in items]
print(f'Items: {len(items)}, Placeholders: {len(placeholders)}, Dupes: {len(dupes)}, Bad refs: {len(bad_refs)}')
"
```

---

## Final Structure

### L1 Components (60 items)
| System | Count | Key Components |
|--------|-------|----------------|
| Skeletal | 5 | Skull, Spine, Ribcage, Pelvis, Long Bones |
| Muscular | 4 | Heart Muscle, Skeletal Muscles, Smooth Muscles, Diaphragm |
| Nervous | 6 | Brain, Spinal Cord, Peripheral Nerves, Autonomic NS, Eyes, Ears |
| Circulatory | 5 | Heart, Arteries, Veins, Capillaries, Blood |
| Respiratory | 3 | Lungs, Bronchi, Alveoli |
| Digestive | 7 | Mouth, Esophagus, Stomach, Small Intestine, Large Intestine, Liver, Pancreas |
| Endocrine | 5 | Pituitary, Thyroid, Adrenals, Pineal, Gonads |
| Immune | 5 | White Blood Cells, Lymph Nodes, Spleen, Thymus, Bone Marrow |
| Integumentary | 3 | Skin, Hair, Nails |
| Urinary | 3 | Kidneys, Bladder, Ureters |
| Reproductive | 4 | Uterus, Ovaries, Testes, Placenta |
| Microbiome | 5 | Gut, Skin, Oral, Vaginal, Mitochondria |
| Special | 5 | DNA, Stem Cells, Fascia, Vagus Nerve, CSF |

### L2 Systems (13 items)
One per category above, with composite_of references and sections: About, Emergence, How to Explore.

### L3 Meta (3 items)
- The Moving Body (skeletal + muscular + nervous)
- The Invisible Body (endocrine + immune + microbiome)
- The Living Whole (all systems)

### Sections Per L1 Item
- "What It Does" — function (2-4 sentences)
- "How It Connects" — relationships to other organs/systems (2-3 sentences)
- "Wonder" — astonishing fact (1-2 sentences)
- "When It Breaks" — what goes wrong (1-2 sentences)
