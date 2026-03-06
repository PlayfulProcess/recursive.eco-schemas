# Build Log: Relationship Cards — A Couples Oracle

**Grammar**: `grammars/relationship-cards/grammar.json`
**Source**: None (built from memory)
**Type**: from-memory
**Status**: SKELETON + CONTENT SKELETONS COMPLETE — ready for polish sessions
**Items**: 68 (54 L1 cards + 10 L2 dynamics + 4 L3 meta-themes)
**File size**: ~75KB

---

## Source Analysis

- No source text — built entirely from knowledge of relationship science
- Core frameworks synthesized:
  - **John Gottman**: Sound Relationship House, Four Horsemen, bids, repair attempts, Love Maps, 5:1 ratio, betrayal cascade, Story of Us
  - **Sue Johnson**: Emotionally Focused Therapy (EFT), demon dialogues, protest polka, softening, A.R.E., attachment injuries
  - **John Bowlby**: Attachment theory, secure base, internal working models
  - **Stephen Porges**: Polyvagal theory, neuroception, co-regulation
  - **Marsha Linehan**: Dialectical thinking, distress tolerance, DEAR MAN, radical acceptance
  - **Murray Bowen**: Differentiation of self, triangulation, family systems
  - **Esther Perel**: Desire vs security dialectic (referenced, not central)
  - **Dan Siegel**: Window of tolerance, interpersonal neurobiology
- `grammar_type: "tarot"` — works as a 3-card oracle draw for couples

## Strategy: Content Skeleton Approach (NEW PATTERN — SUCCESS)

| Step | Approach | Result |
|------|----------|--------|
| 1. Write game design doc | Full plan with deck architecture, spread positions, journal prompts, AI system prompt | SUCCESS — `plan/relationship-cards-game-plan.md` |
| 2. Write grammar skeleton | All 68 items with placeholder sections, metadata, cross-links | SUCCESS — validated: 0 dupes, 0 bad refs, sequential sort_order |
| 3. Commit skeleton | Safety checkpoint | SUCCESS |
| 4. Fill content skeletons | Replace ALL placeholders with `[SESSION-N]` tagged content outlines | SUCCESS — 298/298 sections filled, 0 placeholders remaining |
| 5. Validate and commit | Full validation pass | SUCCESS |

### Key Innovation: Content Skeletons for Multi-Session Builds

**The problem**: From-memory grammars with 50+ items require too much content generation for a single session, but delegating to background agents for content-heavy work times out (per CLAUDE.md).

**The solution**: Write **content skeletons** into each item's sections — not the final polished prose, but structured notes tagged by session that tell future agents EXACTLY what to write:

```
"[SESSION-1: PATTERNS] Gottman's 4 predictors of divorce: criticism, contempt,
defensiveness, stonewalling. From 40+ years of Love Lab research. The cascade —
how one horseman invites the next. The 93% prediction accuracy..."
```

**Why this works**:

1. **Each session agent gets a pre-written brief.** They don't need to research or decide what to write — the skeleton tells them the research basis, the framing, the tone, and the specific angles.

2. **Session tags organize the work.** `[SESSION-1: PATTERNS]` means "Session 1 handles all Pattern cards." An agent can grep for `SESSION-1` and know exactly what's theirs.

3. **The skeleton IS draft content.** Because the outlines are detailed enough (~50-100 words per section), they're already 70-80% of the way to final prose. The polish session needs to:
   - Remove the `[SESSION-N]` tags
   - Expand terse notes into flowing paragraphs
   - Smooth the tone (more poetic, less bullet-pointed)
   - Verify research claims

4. **Parallel sessions are independent.** Sessions 1-5 can run in any order. Session 6 (L2/L3) can also run independently since the `composite_of` references are stable.

5. **The grammar is USABLE at skeleton stage.** Even with `[SESSION-N]` tags, the content is meaningful enough that the AI interpreter could work with it. The cards are already teaching.

### Session Distribution

| Session | Cards | Sections | Est. Polish Time |
|---------|-------|----------|-----------------|
| 1 | 12 Pattern cards | 60 | ~15 min agent session |
| 2 | 12 Need cards | 60 | ~15 min agent session |
| 3 | 12 Repair cards | 60 | ~15 min agent session |
| 4 | 10 Strength cards | 50 | ~12 min agent session |
| 5 | 8 Shadow cards | 40 | ~10 min agent session |
| 6 | 14 L2/L3 items | 28 | ~8 min agent session |

**Total for polish: ~6 focused sessions, each handling one suit.**

## Reusable Patterns

### Content Skeleton Pattern (NEW — recommended for all from-memory grammars > 30 items)

1. **Write the full grammar skeleton** (Write tool): all items, IDs, metadata, placeholder sections
2. **Validate** (Bash): JSON, IDs, refs, sort_order
3. **Commit skeleton** (safety checkpoint)
4. **Fill content skeletons inline** (Edit tool): replace each placeholder with `[SESSION-N: CATEGORY]` tagged outline
   - Include: research basis, key names/studies, shadow angle, light angle, question themes
   - Length: 50-100 words per section (enough to guide, not enough to time out)
5. **Validate zero placeholders** (Bash)
6. **Commit content skeletons** (safety checkpoint)
7. **Polish in dedicated sessions**: one session per category, each agent greps for their `[SESSION-N]` tag

**Why this beats the old Skeleton + Edit-per-item approach**: The old approach required the SAME session to both generate content AND manage JSON edits. Content generation is the expensive part. By separating "decide what to write" (skeleton session) from "write it beautifully" (polish sessions), each session stays focused and fast.

### Tarot-Type Grammar Section Structure

For oracle/card-draw grammars, this 5-section structure works well:

```json
{
  "Interpretation": "What this card means when drawn. Second person, warm but direct.",
  "Shadow": "The difficult edge — what this looks like when it goes wrong.",
  "Light": "The gift — what this looks like at its best.",
  "Summary": "One sentence. The card's essence.",
  "Questions": "3-5 reflective questions for the user."
}
```

### Cross-Linking in Relationship/Psychology Grammars

The `grammars[]` field works brilliantly for connecting therapeutic concepts to their intellectual roots:
- Bowlby → Darwin's Expression of Emotions (evolutionary basis)
- Co-regulation → Dhammapada (mindfulness as self-regulation)
- Contempt → Art of War (strategic conflict)
- Desire → Song of Songs (sacred eros)
- Dialectics → Epictetus (Stoic dialectics)

This makes the grammar a HUB that connects relationship science to the wider library.

### Journal Template as Game Design

The journal template fields (Template Name, Journal Prompt, Description, AI Personality) effectively design a GAME within the app:
- **Spread positions** (Pattern → Need → Move) create narrative structure
- **AI system prompt** provides interpretive framework
- **Journal prompt** guides reflection and action
- **Weekly ritual** creates longitudinal engagement

This pattern could be replicated for other oracle grammars: Jungian Archetypes, I Ching, Astrology.

## Key Learnings

- **Content skeletons are the missing step** between "empty placeholders" and "final prose." They solve the single-session bottleneck for large from-memory grammars.
- **Session tagging** (`[SESSION-N]`) is the key organizational innovation. It turns one big job into N small, parallel jobs.
- **The grammar works at every stage**: skeleton (structural validation), content skeleton (usable draft), polished (final). Each stage is independently committable and valuable.
- **5 suits maps well to 5 sessions**: Each suit has its own domain knowledge (Gottman, Johnson, Porges, etc.), so a session agent can build domain coherence within a single suit.
- **The AI system prompt is as important as the grammar**: For oracle-type grammars, the interpretation prompt determines the user experience. Writing it alongside the grammar (not after) ensures they're aligned.

## Files

- `grammars/relationship-cards/grammar.json` — 68-item grammar with content skeletons
- `plan/relationship-cards-game-plan.md` — Full game design including deck architecture, spread positions, journal template prompts, AI system prompt, cross-links, and build strategy
- `plan/family-therapy-grammar-plan.md` — Parent plan for the larger Family Therapy Grammar (this deck is a subset/companion)
