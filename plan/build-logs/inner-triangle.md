# Build Log: The Inner Triangle — Emotion, Cognition & Behavior in Relation

**Grammar**: `grammars/inner-triangle/grammar.json`
**Source**: None (built from memory)
**Type**: from-memory
**Status**: SKELETON + CONTENT SKELETONS COMPLETE — ready for polish sessions
**Items**: 68 (50 L1 cards + 14 L2 triangles + 4 L3 meta-patterns)
**File size**: ~120KB

---

## Source Analysis

- No source text — built entirely from knowledge of relationship science and psychotherapy
- Core frameworks synthesized:
  - **Aaron Beck**: CBT, cognitive distortions (the Think vertex)
  - **Marsha Linehan**: DBT, wise mind, radical acceptance, DEAR MAN, distress tolerance
  - **Sue Johnson**: EFT, protest polka, softening, demon dialogues, A.R.E., attachment injuries
  - **John Bowlby**: Attachment theory, internal working model, secure base, protest-despair-detachment
  - **Stephen Porges**: Polyvagal theory, neuroception, ventral/sympathetic/dorsal vagal states
  - **Silvan Tomkins**: Affect theory, 9 innate affects
  - **Paul Ekman**: Basic emotions, universal facial expressions, contempt micro-expression
  - **Jeffrey Young**: Schema therapy, early maladaptive schemas (abandonment, defectiveness, mistrust, self-sacrifice)
  - **Peter Fonagy**: Mentalization, reflective functioning
  - **Carl Rogers**: Unconditional positive regard, active listening, congruence
  - **Carl Jung**: Shadow, projection, anima/animus
  - **D.W. Winnicott**: True self/false self
  - **Esther Perel**: Desire vs security dialectic
  - **John Gottman**: Four Horsemen, bids, repair, flooding, NSO, 5:1 ratio, Sound Relationship House
  - **Brené Brown**: Vulnerability, shame resilience, foreboding joy
  - **Barbara Fredrickson**: Broaden-and-build theory of positive emotions
  - **Shelly Gable**: Capitalization, active-constructive responding
  - **Jude Cassidy/Phillip Shaver**: Adult attachment research
  - **Peter Levine**: Somatic Experiencing, freeze discharge
- `grammar_type: "tarot"` — works as a 3-card oracle draw (Feel → Think → Do)

## Strategy: Content Skeleton Approach (Second Application)

| Step | Approach | Result |
|------|----------|--------|
| 1. Write game design doc | Full plan with deck architecture, spread, AI prompt | SUCCESS — `plan/inner-triangle-grammar-plan.md` |
| 2. Write grammar skeleton | All 68 items with placeholder sections, metadata, cross-links | SUCCESS — validated: 0 dupes, 0 bad refs, sequential sort_order |
| 3. Commit skeleton | Safety checkpoint | SUCCESS — commit `7a3f035` |
| 4. Fill content skeletons | Replace ALL placeholders with `[SESSION-N]` tagged content outlines | SUCCESS — 364/364 sections filled, 0 placeholders remaining |
| 5. Validate and commit | Full validation pass | SUCCESS |

### Content Skeleton Approach — Second Confirmation

This is the second grammar built with the Content Skeleton Pattern (first was Relationship Cards at 68 items/298 sections). Inner Triangle is larger (68 items/364 sections) due to 6 sections per L1 card. The pattern scaled successfully.

### Session Distribution

| Session | Cards | Sections | Content Domain |
|---------|-------|----------|----------------|
| 1 | 18 Emotion cards | 108 | Tomkins, Ekman, Porges, Johnson, Linehan, Brown |
| 2 | 16 Cognition cards | 96 | Beck, Young, Bowlby, Linehan, Gottman, Fonagy |
| 3 | 16 Behavior cards | 96 | Johnson, Gottman, Porges, Linehan, Rogers, Jung |
| 4 | 14 L2 Triangles | 56 | Integration — each triangle draws from 2-3 domains |
| 5 | 4 L3 Meta-patterns | 8 | Systems-level — full integration of all frameworks |

**Total for polish: ~5 focused sessions.**

## Design Decisions

### The CBT Triangle in Relational Field

The central innovation: taking the CBT triangle (Feel → Think → Do) and placing it BETWEEN two people. Every card asks: "What does your partner see when you feel/think/do this?" This transforms an individual therapy tool into a couples therapy tool.

### 6-Section Structure for L1 Cards

```json
{
  "Interpretation": "What this card means when drawn. Research basis.",
  "In Relation": "How this shows up BETWEEN two people — the relational dimension.",
  "Shadow": "The difficult edge — when it goes wrong.",
  "Light": "The gift — when it goes right.",
  "Body": "Where it lives in the body. Somatic markers.",
  "Questions": "3-5 reflective questions for the couple."
}
```

The "In Relation" and "Body" sections are what distinguish this from a standard CBT resource. "In Relation" makes every card relational; "Body" makes it somatic (Porges-informed).

### 4-Section Structure for L2 Triangles

```json
{
  "About": "What this triangle is — the three vertices and how they connect.",
  "The Loop": "How the triangle self-reinforces — the cycle.",
  "In Relation": "How this triangle interlocks with the partner's triangle.",
  "The Shift": "How to change one vertex to transform the whole loop."
}
```

The "The Shift" section is the therapeutic intervention — it operationalizes change.

### 2-Section Structure for L3 Meta-patterns

```json
{
  "About": "The meta-pattern — how multiple triangles interact.",
  "How to Use": "Practical guidance for couples drawing this card."
}
```

### Destructive vs. Healing Triangles

The 14 L2 triangles split into two categories:
- **9 Destructive triangles** (📐 symbol): anxious, avoidant, shame-hide, anger-attack, resentment-sacrifice, jealousy-mistrust, loneliness-withdrawal, contempt-disgust, numbness-freeze
- **5 Healing triangles** (💗 symbol): vulnerability-connection, tenderness-listening, guilt-repair, desire-risk, joy-expansion

This creates a natural therapeutic arc: identify your destructive triangle, then learn the corresponding healing triangle.

### Companion Grammar Pattern

Inner Triangle (WHY patterns happen — the internal mechanism) complements Relationship Cards (WHAT patterns look like — the external behavior). Cross-linked via `grammars[]` field on pursuing/withdrawing cards pointing to Relationship Cards grammar.

## Reusable Patterns

### The 6-Section Relational Card Structure

For any psychology/therapy oracle grammar where both individual AND relational dimensions matter:

1. **Interpretation** — What it is (research-grounded)
2. **In Relation** — How it shows up between two people
3. **Shadow** — The dark side
4. **Light** — The healthy expression
5. **Body** — Somatic dimension (makes it embodied)
6. **Questions** — Reflective prompts for the user

The "In Relation" section is the key innovation for couples-oriented grammars.

### The Triangle Structure for L2 Emergence

When L1 items naturally group into 3-part dynamics, the triangle format works:

1. **About** — The three components and their relationship
2. **The Loop** — How they self-reinforce
3. **In Relation** — How the loop appears in the relational field
4. **The Shift** — Therapeutic intervention (change one vertex)

### Cross-Linking Therapy Grammars

11 cross-links to existing grammars:
- Darwin's Expression of Emotions (evolutionary basis of affect)
- Jungian Archetypes (shadow/projection)
- Discourses of Epictetus (Stoic dialectics → black-white thinking)
- Chuang Tzu (wise mind's Taoist root)
- Dhammapada (radical acceptance's Buddhist root)
- Myths Through Many Eyes (internal working model → mythic narrative)
- Sadhana by Tagore (loneliness → devotional longing)
- Hidden Symbolism of Alchemy (projection → alchemical transformation)
- Winnie the Pooh (false self / performing)
- Relationship Cards (companion grammar — pursuing/withdrawing cards)

## Key Learnings

- **Content skeletons scale to 364 sections**: No degradation in quality or coherence. The session-by-session organization (Emotions → Cognitions → Behaviors → Triangles → Meta) maintained domain coherence naturally.
- **JSON escaping is the main risk**: One unescaped quote (Darwin citation with internal double quotes) broke the entire file. Always validate JSON after filling content skeletons.
- **The "In Relation" section is the key differentiator**: What makes this a COUPLES grammar rather than an individual CBT resource is consistently asking "What does your partner see?" in every card.
- **Body section connects to polyvagal**: Every card has a somatic dimension because Porges' work shows that the nervous system mediates all relational behavior. This makes the grammar embodied, not just cognitive.
- **L2 triangles are the real teaching tool**: Individual cards (L1) provide vocabulary; triangles (L2) provide the GRAMMAR — how the pieces fit together into loops. The shift section in each triangle is the therapeutic intervention.

## What Failed / What to Avoid

1. **Unescaped quotes in JSON strings**: Darwin's quote contained `"disgust"` inside a JSON string value, which broke parsing. Always use single quotes for embedded quotations or escape with backslash.

## Files

- `grammars/inner-triangle/grammar.json` — 68-item grammar with content skeletons
- `plan/inner-triangle-grammar-plan.md` — Full game design including deck architecture, spread positions, journal template, AI system prompt, cross-links
- `plan/family-therapy-grammar-plan.md` — Parent plan for the larger Family Therapy Grammar (this deck is a companion)
- `plan/build-logs/relationship-cards.md` — Companion grammar build log
