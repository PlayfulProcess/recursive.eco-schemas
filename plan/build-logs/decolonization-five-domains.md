# Build Log: Decolonization — Five Domains

**Grammar**: `grammars/decolonization-five-domains/grammar.json`
**Source**: None (built from memory)
**Type**: from-memory
**Status**: CONTENT SKELETONS COMPLETE — ready for polish sessions
**Items**: 53 (47 L1 cards + 5 L2 domain categories + 1 L3 meta-pattern)
**File size**: ~135KB

---

## Source Analysis

- No source text — built entirely from decolonial theory, trauma studies, and indigenous knowledge frameworks
- Core frameworks synthesized:
  - **Vanessa Andreotti**: Hospicing Modernity, HEADS UP tool, ontological pluralism
  - **Bayo Akomolafe**: Postactivism, slowing down, fugitive responses
  - **Linda Tuhiwai Smith**: Decolonizing Methodologies, indigenous research ethics
  - **Frantz Fanon**: Wretched of the Earth, embodied colonialism, psychopathology of colonization
  - **Sylvia Wynter**: Coloniality of being, Man as overrepresentation
  - **Glen Coulthard**: Red Skin White Masks, grounded normativity
  - **Resmaa Menakem**: My Grandmother's Hands, racialized trauma in the body
  - **Bessel van der Kolk**: The Body Keeps the Score, somatic trauma storage
  - **Rachel Yehuda**: Epigenetic transmission of trauma across generations
  - **Robin Wall Kimmerer**: Braiding Sweetgrass, grammar of animacy, Honorable Harvest
  - **Stephen Porges**: Polyvagal theory — nervous system states in collective trauma
  - **Vandana Shiva**: Monocultures of the mind, seed sovereignty
  - **Eduardo Galeano**: Open Veins of Latin America
  - **Robert Bullard**: Environmental racism, sacrifice zones
  - **Vine Deloria Jr.**: God Is Red, indigenous philosophy
  - **Eduardo Viveiros de Castro**: Amazonian perspectivism, multinaturalism
  - **Charles Mann**: 1491, pre-Columbian Americas
- `grammar_type: "custom"` — contemplative/reflective grammar, not oracle draw

## Strategy: Content Skeleton Approach (Third Application)

| Step | Approach | Result |
|------|----------|--------|
| 1. Merge existing draft | Merged `claude/merge-iching-grammar-ND6pW` with Body + Mind domains (21 items) | SUCCESS |
| 2. Fix sort_order | Changed from 0-based to 1-based | SUCCESS |
| 3. Add trauma-informed framing | Updated description with Menakem, van der Kolk, Yehuda | SUCCESS |
| 4. Add Spirit domain | L2 + 10 L1 items (sort_order 22-32) | SUCCESS |
| 5. Add Collective domain | L2 + 9 L1 items (sort_order 33-42) | SUCCESS |
| 6. Add Planet domain | L2 + 9 L1 items (sort_order 43-52) | SUCCESS |
| 7. Add L3 capstone | Hospicing Modernity (sort_order 53) | SUCCESS |
| 8. Validate | 0 dupes, 0 bad refs, sequential sort_order, 0 placeholders | SUCCESS |

### Session Distribution for Polish

| Session | Cards | Sections | Content Domain |
|---------|-------|----------|----------------|
| 1 | 10 Body cards + L2 | ~40 | Menakem, van der Kolk, Fanon, Porges |
| 2 | 11 Mind cards + L2 | ~44 | Andreotti, Wynter, Smith, Freire, Fanon |
| 3 | 11 Spirit cards + L2 | ~44 | Kimmerer, Deloria, Akomolafe, Shrei |
| 4 | 10 Collective cards + L2 | ~40 | Coulthard, Federici, Shiva, Bullard |
| 5 | 10 Planet cards + L2 | ~40 | Kimmerer, Shiva, Mann, Bullard, Klein |
| 6 | 1 L3 Hospicing Modernity | 2 | Full integration — Andreotti + Akomolafe |

**Total for polish: ~6 focused sessions.**

## Design Decisions

### The Trauma-Informed Lens

The central innovation: treating colonial violence as attachment injury at civilizational scale. This isn't metaphor — Yehuda's research shows that trauma literally alters gene expression across generations; Menakem shows that racialized trauma lives in the body; van der Kolk shows the body keeps the score. A decolonial grammar that stays in the head recolonizes the mind.

This connects directly to the Inner Triangle grammar (CBT triangle in relational field): colonial patterns reproduce through the same feel-think-do loops that EFT and CBT map in couples. The decolonization grammar asks the macro question; Inner Triangle asks the micro question; they're the same question at different scales.

### 4-Section Structure for L1 Cards

```json
{
  "The Pattern": "What the colonial structure IS — named clearly, grounded in scholarship.",
  "What It Costs": "The somatic, psychic, ecological, and relational damage — felt, not just analyzed.",
  "What Persists": "What survived despite centuries of erasure — the persistent alternatives.",
  "The Invitation": "A contemplative prompt — not a solution but a practice of noticing."
}
```

The "What Persists" section is the key differentiator from activist or academic decolonial writing. It refuses the narrative that colonialism succeeded totally — it didn't. Seed keepers kept seeds. Grandmothers kept languages. Ceremonies went underground. The invitation is to notice what's already growing in the cracks.

### 3-Section Structure for L2 Domain Categories

```json
{
  "About": "What this domain covers and why it matters.",
  "The Colonial Logic": "The specific logic of domination operating in this domain.",
  "The Invitation": "Domain-level contemplative practice."
}
```

### 2-Section Structure for L3 Capstone

```json
{
  "About": "The meta-pattern — how all five domains are one wound seen from five angles.",
  "How to Use": "Practical guidance for using the grammar contemplatively."
}
```

### Five Domains

| Domain | Items | Core Question | Key Thinkers |
|--------|-------|---------------|--------------|
| Body | 9 L1 | Whose body standards do you carry? | Menakem, Fanon, van der Kolk |
| Mind | 10 L1 | Whose knowledge counts as knowledge? | Andreotti, Wynter, Smith, Freire |
| Spirit | 10 L1 | Whose sacred practices were erased? | Kimmerer, Deloria, Akomolafe |
| Collective | 9 L1 | Whose ways of organizing were replaced? | Coulthard, Federici, Shiva |
| Planet | 9 L1 | Whose relationship to earth was severed? | Kimmerer, Mann, Bullard, Klein |

### Tone: Andreotti over Activist

The grammar leans toward sitting-with-complexity (Andreotti/Akomolafe) rather than demands-and-slogans (activist). This is deliberate: activist grammar tells you what to DO; contemplative grammar changes how you SEE. The "Invitation" sections never prescribe action — they invite noticing. "Ask: whose body standards are you carrying?" rather than "Reject Western beauty standards."

This doesn't mean the grammar avoids politics. Items like `collective-reparations`, `planet-sacrifice-zones`, and `spirit-doctrine-discovery` name specific political realities. But the framing is always: notice this pattern, feel what it costs, honor what persists, then sit with the question long enough for it to change you.

### Cross-Grammar Connections

17 cross-links to existing grammars across all domains:
- **Body**: Inner Triangle (somatic markers), Darwin's Expression of Emotions
- **Mind**: Confucian Analects (meritocracy), Discourses of Epictetus (Stoic universalism)
- **Spirit**: Sadhana by Tagore (devotional practice), Hidden Symbolism of Alchemy
- **Collective**: Architecture of Nations, Economic Ideas, Social Working
- **Planet**: Walden, Creative Evolution, Origin of Species
- **L3**: Inner Triangle (companion grammar — micro/macro integration)

## Key Learnings

- **Trauma framing makes decolonial theory embodied**: Without Menakem/van der Kolk/Yehuda, decolonial grammar risks being purely intellectual. The somatic dimension (every card asks "where does this live in the body?") prevents this.
- **"What Persists" prevents despair narrative**: Academic decolonial writing can feel overwhelming. The "What Persists" section in every card insists on naming what survived — this isn't optimism, it's evidence.
- **The 4-section structure is a practice sequence**: Pattern → Cost → Persistence → Invitation maps onto see → feel → hope → act. It's pedagogically deliberate.
- **Python append scripts scale well**: Adding domains as JSON arrays via Python avoided the need to hand-edit a 130KB+ file. Each domain could be validated independently before appending.
- **Cross-linking at item level is powerful**: The `grammars[]` field on individual items (not just grammar-level) creates a web of connections — a reader exploring extractivism gets a pointer to Origin of Species, a reader exploring monoculture gets a pointer to Walden.

## What Failed / What to Avoid

1. **Initial sort_order was 0-based**: The merged branch used 0-based sort_order, which is inconsistent with the rest of the library. Fixed to 1-based early.
2. **Planet domain L2 had wrong category**: Initially set to `planet` instead of `domains` (matching the other 4 domain L2s). Caught in validation.

## Files

- `grammars/decolonization-five-domains/grammar.json` — 53-item grammar with content skeletons
- `plan/family-therapy-grammar-plan.md` — Parent plan for the larger Family Therapy Grammar cluster
- `plan/build-logs/decolonization-five-domains.md` — This build log
- `plan/build-logs/inner-triangle.md` — Companion grammar build log
