# Build Log: The Human Body — An Emergent Symphony

**Grammar**: `grammars/human-body/grammar.json`
**Source**: From memory (no seed file)
**Type**: from-memory
**Status**: NOT STARTED — planning phase

---

## What Went Wrong (First Attempt)

- **Delegated to a background agent to write the entire grammar in one shot.**
- The agent timed out. Generating ~70 L1 items with 4 original content sections each (What It Does, How It Connects, Wonder, When It Breaks) plus 12 L2 systems plus 3 L3 metas is too much original content for a single agent call.
- **Root cause**: From-memory grammars are fundamentally different from from-source grammars. Source grammars extract and restructure existing text; from-memory grammars require generating every word. The total content volume (~50-80KB of original prose) exceeds what a single agent can produce reliably.

## What Works for Source-Text Grammars (Does NOT Apply Here)

- Parse seed → extract chapters/stories → wrap in grammar JSON
- One agent call, one parser, one output file
- Content already exists; we just restructure it

## What Should Work for From-Memory Grammars

### Recommended Multi-Session Approach

**Session 1: Skeleton**
- Create the complete item tree: all IDs, names, levels, categories, sort_orders, composite_of references
- Empty sections (or single-sentence placeholders)
- Validate referential integrity
- This is the "index" — small enough for one session

**Session 2-N: Fill Content**
- One system per session (or 2-3 small systems)
- Fill in the 4 sections for each L1 item in that system
- Fill in the L2 "About" and "Emergence" sections
- Each session is focused and manageable (~5-10 items)

**Final Session: L3 Meta + Review**
- Write L3 meta-category content
- Review all items for consistency and accuracy
- Validate the complete grammar

### Why This Works

- Each session produces a small, reviewable chunk
- The skeleton ensures referential integrity from the start
- Content quality is better when focused on one domain at a time
- No single session needs to generate more than ~10KB of original prose

## Planned Structure

### L1 Components (~65-75 items)
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

### L2 Systems (12 items)
One per system above, with composite_of references.

### L3 Meta (3 items)
- The Moving Body (skeletal + muscular + nervous)
- The Invisible Body (endocrine + immune + microbiome)
- The Living Whole (all systems)

### Sections Per L1 Item
- "What It Does" — function (2-4 sentences)
- "How It Connects" — relationships to other organs/systems (2-3 sentences)
- "Wonder" — astonishing fact (1-2 sentences)
- "When It Breaks" — what goes wrong (1-2 sentences)

## Reusable Lesson

**From-memory grammars should be built in multiple sessions: skeleton first, then content fill by section/system. Do not attempt to generate 50+ items of original content in a single agent call.**
