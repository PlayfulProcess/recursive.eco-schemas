# Build Log: Jungian Archetypes

**Grammar**: `tarot/jungian-archetypes/grammar.json`
**Source**: None (built from memory)
**Type**: from-memory
**Status**: COMPLETE
**Items**: 34 (24 L1 archetypes + 6 L2 dynamics + 4 L3 individuation stages)
**File size**: ~60KB

---

## Source Analysis

- No source text used — built entirely from knowledge of Jungian analytical psychology
- Core archetypes drawn from Carl Jung's collected works, particularly: *Archetypes and the Collective Unconscious*, *Aion*, *Two Essays on Analytical Psychology*
- Also informed by James Hillman (archetypal psychology), Marie-Louise von Franz (fairy tale analysis), and Joseph Campbell (hero's journey)
- `grammar_type: "tarot"` — works as a card oracle for drawing archetypal reflections

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Archetype selection | Chose 24 core archetypes from Jung's work | SUCCESS — covers ego, shadow, anima/animus, self, persona + 18 more |
| 2. Section structure | Interpretation, Shadow, Light, Summary, Questions | SUCCESS — mirrors tarot grammar format |
| 3. L2 dynamics | 6 archetypal pairs/tensions that emerge from L1 combinations | SUCCESS — composite_of references valid |
| 4. L3 stages | 4 individuation stages as meta-categories | SUCCESS — maps Jung's individuation process |
| 5. Keywords and quotes | Relevant Jung quotes (under 125 chars) and concept keywords | SUCCESS |

## Key Learnings

- **From-memory grammars are fast but limited.** The entire grammar was built in a single pass without source verification. Quotes are paraphrased from memory and may not be exact. For a production grammar, cross-referencing with actual Jung texts would improve accuracy.
- **Jungian archetypes map naturally to tarot's oracle format.** The Shadow/Light section structure mirrors reversed/upright card meanings. Each archetype becomes a "card" that can be drawn for reflection.
- **Three-level emergence works well for psychological systems:**
  - L1: Individual archetypes (the atoms)
  - L2: Archetypal dynamics (tensions between pairs — e.g., Shadow Meets Ego)
  - L3: Individuation stages (the process that integrates everything)
- **composite_of at L2 creates meaningful connections.** "Shadow Meets Ego" → `["shadow", "ego"]` tells the viewer these concepts interact. "Hero and the Dragon" → `["hero", "shadow"]` reveals the dragon IS the shadow.
- **Questions section is powerful for psychological grammars.** Unlike mythology or philosophy, archetypes are meant to be applied personally. The Questions section ("Where in your life do you wear a mask?") turns the grammar into an active therapeutic tool.

## Reusable Patterns

- **From-memory grammars** work best for well-known symbolic systems (archetypes, elements, chakras, enneagram)
- **Psychological systems** benefit from Shadow/Light/Questions section structure
- **Three-level emergence** suits any system with atoms → interactions → processes
- **Oracle-style grammars** (`grammar_type: "tarot"`) work for any set of symbols you'd want to "draw" for reflection

## Prompt for Similar Tasks

```
Create a psychological/archetypal grammar from memory.
Include 20-30 core archetypes at L1 with:
- Interpretation, Shadow, Light, Summary, Questions sections
- Keywords from the tradition
- Relevant quotes (under 125 chars, paraphrased is fine)
Add 5-8 L2 archetypal dynamics using composite_of pairs.
Add 3-5 L3 meta-categories for the overall process.
Use grammar_type: "tarot" for oracle/card-draw functionality.
```
