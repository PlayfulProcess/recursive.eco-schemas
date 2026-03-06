# Build Log: Bus Grammar — System Prompts for Passengers

## Grammar Type
From-memory grammar. All content provided by the user as system prompts for AI voices.

## Structure
- **32 L1 items**: Individual voice/passenger prompts across 6 "buses" + 2 facilitators
- **7 L2 items**: Bus categories (FHW, Ancestral, Jungian, IFS, Chakra, DBT, Facilitators)
- **2 L3 items**: Meta-categories (Therapeutic Mirrors, Archetypal Depths)

### Buses & Voice Count
| Bus | Tradition | L1 Count |
|-----|-----------|----------|
| FHW Passengers | Vanessa Andreotti — Hospicing Modernity | 6 |
| Ancestral Voices | Indigenous/ecological epistemology | 5 |
| Jungian Archetypes | Carl Jung — depth psychology | 5 |
| IFS Parts | Richard Schwartz — Internal Family Systems | 4 |
| Chakra Voices | Hindu/yogic energy system | 7 |
| DBT Mind States | Marsha Linehan — Dialectical Behavior Therapy | 3 |
| Facilitators | Meta-prompts for synthesis | 2 |

## Attempt Log

### Attempt 1 — 2026-03-05 (FAILED)
**Strategy**: Write skeleton with placeholders, then Edit per-item.
**What happened**: Created directory `grammars/bus-grammar-system-prompts/` but the session turn ended before the `Write` tool was called. The grammar is 32+ items with rich content (system prompts + history + visual references) — estimated ~2000+ lines of JSON.
**Root cause**: Spent too long on planning/exploring before starting the actual write. The from-memory grammar approach (skeleton + edit-per-item) is correct per CLAUDE.md, but I never got to the skeleton write.
**Lesson**: For large from-memory grammars, start the Write immediately after confirming structure. Don't over-plan. The skeleton IS the plan.

### Attempt 2 — 2026-03-06
**Strategy**: Write the FULL grammar in one Write call — not skeleton + edit. Since all prompts are already provided by the user, there's no "placeholder" phase needed. Include system prompts, history/context, and visual references directly.
**Key sections per L1 item**:
- "System Prompt": The actual AI prompt text (provided by user)
- "About": Brief description of this voice
- "History & Context": The tradition this voice comes from
- "Visual Reference": Public domain art suggestions
- "When This Voice Activates": Trigger conditions
**Status**: IN PROGRESS

## Visual Reference Strategy
Each bus maps to a distinct visual tradition:
- **FHW**: Vanessa Andreotti's work is contemporary — use colonial-era maps, industrial revolution imagery, Piranesi's "Carceri" (prisons) as metaphor for modernity's traps
- **Ancestral**: Aboriginal dot paintings (public domain reproductions), cave art (Lascaux, Altamira), ancient tree/forest imagery
- **Jungian**: Alchemical illustrations (Rosarium Philosophorum), William Blake engravings, Red Book imagery
- **IFS**: Less obvious visual tradition — suggest Remedios Varo's surrealist paintings (parts as inner figures), Magritte
- **Chakra**: Hindu temple sculpture, tantric art, lotus motifs from Mughal miniatures
- **DBT**: Zen enso circles, waves/ocean imagery (Hokusai), balance/scale imagery

## Parsing Notes
- N/A — from-memory grammar, no seed file
- The system prompts are the primary content; sections like History wrap around them
- grammar_type: "custom" (these are meta-tools, not oracle cards)
- Each prompt is designed to work with ANY oracle context (I Ching, Tarot, etc.)
