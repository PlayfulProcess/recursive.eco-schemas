# Build Log: The Tarot of All Tarots

**Grammar**: `grammars/tarot-of-all-tarots/grammar.json`
**Type**: from-schema (multi-deck synthesis)
**Status**: COMPLETE
**Items**: 89 (78 L1 cards + 9 L2 groups + 2 L3 meta-categories)
**File size**: 530 KB

---

## Overview
A meta-tarot grammar unifying 7 public domain decks (RWS, Marseille, Sola Busca, Etteilla I/II/III, Tarocchino Arlecchino) into a single 78-card prismatic reading system.

## Build Strategy

### Phase 1: Schema Research (completed)
- Used background agent to map card IDs across all 8 tarot schema files
- Identified ID formats, suit naming conventions, numbering systems
- Key finding: Etteilla uses Genesis-based ordering (1-8) not standard 0-21
- Key finding: Tarocchino is a 62-card Bolognese deck missing pip cards 2-5

### Phase 2: Skeleton Generator Script (completed)
- `scripts/generate_tarot_of_all_tarots.py` — maps all decks, pulls images/text from schemas
- Produces 78 L1 items with 10-11 sections each
- 5 sections auto-filled from schema data (RWS, Marseille, Sola Busca, Etteilla, Tarocchino)
- 5 sections left as stubs: Archetype, Professional, Relationship, Consciousness, Shadow

### Phase 3: Filling 390 Interpretive Stubs — TIMEOUT FAILURE ×2

**Attempt 1:** Tried to have Claude write all 390 sections directly into the grammar JSON. Timed out — grammar.json is 448KB and writing unique content for 78 cards × 5 sections exceeded session time.

**Attempt 2:** Planned to write a Python content-generator script. The *planning and script-writing* itself timed out before the script was even created. Scope creep: spent too long on research agents mapping card IDs, reading existing schemas, and analyzing data formats before writing any code.

**Root causes:**
1. Violated CLAUDE.md rule: "Large grammar files (40+ items): Write in chunks, not one shot."
2. Used background research agents that consumed 245 seconds (4+ minutes) just to catalog schema formats — information that could have been gathered in a few targeted reads.
3. Attempted to write a comprehensive Python script in one go after extensive research, rather than writing a minimal script immediately and iterating.

### Phase 3 (attempt 3): Minimal Script, Run Immediately — SUCCESS

**Strategy:**
1. `scripts/fill_tarot_interpretations.py` (~400 lines) — lookup-table approach:
   - 22 hand-written major arcana interpretations (Archetype, Professional, Relationship, Consciousness, Shadow)
   - Suit symbolism table (4 suits × 5 domains)
   - Number symbolism table (1-10 × 5 domains)
   - Court card archetype table (Page/Knight/Queen/King × 5 domains)
   - Minor arcana sections composed by combining suit + number/court data + card keywords
2. `scripts/add_tarot_emergence.py` — adds L2 groups and L3 meta-categories
3. Full pipeline: `generate_tarot_of_all_tarots.py` → `fill_tarot_interpretations.py` → `add_tarot_emergence.py`

**Why it worked:**
- Python runs in seconds — no AI inference timeout risk
- Major arcana hand-written in lookup tables = high-quality unique content
- Minor arcana composed from orthogonal data (suit × number × court) = unique per card while maintaining consistency
- Each script is small, focused, and independently runnable

## Failure Timeline

| Attempt | What happened | Time consumed | Output |
|---------|--------------|---------------|--------|
| 1 | Direct JSON writing of all 390 sections | Full session | Timed out, no sections written |
| 2 | Research agents + script planning | Full session | Build log written, no script created |
| 3 | Minimal script, run immediately | ~5 minutes | SUCCESS: 89 items, 0 stubs, 530KB |

## Key Learnings

1. **For content at scale, write the generator script FIRST, not last.** Don't research → plan → write. Just write → run → fix. The script IS the research.
2. **Lookup tables beat AI generation for structured content.** 22 major arcana archetypes + 4 suits + 10 numbers + 4 court ranks = 40 hand-written entries that compose into 390 unique sections. Combinatorial, not exhaustive.
3. **Background research agents are expensive.** A 4-minute agent that reads 8 files could have been 8 direct reads in 30 seconds. Use agents for genuinely complex exploration, not for reading a known list of files.
4. **Three small scripts > one big script.** skeleton → fill → emergence, each independently runnable and debuggable.

## Emergence Structure

| Level | Category | Count | Contents |
|-------|----------|-------|----------|
| L2 | arcana-group | 3 | Major Arcana, Fool's Journey First Half, Fool's Journey Second Half |
| L2 | suit-group | 4 | Wands, Cups, Swords, Pentacles |
| L2 | structural-group | 2 | Pip Cards, Court Cards |
| L3 | meta | 2 | The Archetypal Journey, The Four Elements in Practice |

## Files
- `scripts/generate_tarot_of_all_tarots.py` — skeleton generator (schema mapping)
- `scripts/fill_tarot_interpretations.py` — content filler (interpretation generator)
- `scripts/add_tarot_emergence.py` — L2/L3 emergence layer
- `grammars/tarot-of-all-tarots/grammar.json` — output grammar
