# On Meta-Relational AI, Grounded in recursive.eco's Architecture

*Companion to `critique-memo-original.md`. The original was written without reference to the actual recursive.eco codebase. This version maps each design move to specific platform infrastructure that already exists or is being added.*

*Status: working notes. Not for publication. Lives here because anything that needs to be implemented in recursive.eco lives in the schemas repo, by author convention.*

---

## What the original critique gets right

The three gaps in ACT-SSP-2.0 (substrate dependence, scope underspecification, vulnerability blindspot) and the constructive alternative (casting mechanism rather than relational persona) are correct as written. This document does not re-litigate them. It connects them to recursive.eco's actual design.

## What the original critique misses by abstracting away from the platform

Several of the "protections" the casting mechanism affords are described in the original as if they had to be invented. They don't. recursive.eco's existing architecture already implements most of them — sometimes deliberately, sometimes as a side-effect of design choices made for other reasons. The Bus Passengers grammar can ride those defaults without re-arguing for them.

Mapping each protection to existing platform infrastructure:

### "No persona to attach to"

**What recursive.eco already does:**
- The platform is built around **grammars** (tarot decks, hexagram books, contemplative texts) — symbolic systems where the user encounters structured chance, not a someone. The AI is a thin layer that helps the user read what the cast revealed. This is the existing oracle pattern.
- `apps/flow/src/lib/iching-ai-prompt.ts` implements this pattern: `buildIChingSystemPrompt(reading, journalContent)` constructs a per-reading system prompt where the AI's role is to interpret the specific hexagram + lines + the user's journal, not to be anyone in particular.
- **No cross-session memory** in journaling: the [Safer Containers page](../../../recursive-eco/apps/landing/pages/safer-containers.html) makes this a stated platform design principle, attributed to the dependency-prevention reasoning.

**What Bus Passengers needs to add:**
- A `bus-ai-prompt.ts` analogue to the I Ching prompt builder — same shape, takes a passenger card + the user's current layer of focus + their journal, returns a per-cast system prompt.
- The system prompt explicitly instructs the model: *"You are not the passenger. You are not Aiden. You are a thin layer helping the user encounter what the cast revealed. Refuse to perform as a wise voice."*

### "Scope is enforced by mechanism, not user judgment"

**What recursive.eco already does:**
- Each grammar has a **fixed item set** with **fixed sections**. The AI has no authority to wander outside the cast item's content. The grammar JSON is the floor.
- Every grammar lives inside a **channel** (wellness, tarot, I Ching, etc.) which has its own visible framing and disclaimers. The wellness channel's [README](../../apps/flow/src/channels/wellness.mdx) and the platform's [Safer Containers page](../../../recursive-eco/apps/landing/pages/safer-containers.html) set scope before any cast happens.
- AI chat is **opt-in per session** and gated behind a friction step (the user has to write something themselves before AI is invited). This is documented in the safer-containers page as a design choice.

**What Bus Passengers needs to add:**
- The Bus oracle mode (a new view in `apps/flow/src/components/play/`, parallel to the I Ching oracle and tarot draw views) restricts the AI's role to: describe what the cast passenger is asking, hold space, redirect to embodied practice. The system prompt makes the scope a hard refusal: *"If the user moves the conversation outside this passenger's content, name that you cannot follow them there and offer to cast a different passenger or redirect them outside the tool."*
- Per-layer scoping inside the descent: the AI works one layer at a time. It does not preemptively skip from Thoughts to Mystery just because the user signals interest in the deeper layer. The mechanism enforces patience.

### "Vulnerability handling designed in"

**What recursive.eco already does:**
- The [Safer Containers page](../../../recursive-eco/apps/landing/pages/safer-containers.html) explicitly names crisis numbers (988 US, 808 24 24 24 PT, 188 BR) and the limits of self-reflection tools.
- Every Vibe Coding 101 course session opens with the same crisis disclaimer.
- The platform's design vocabulary already includes the concept of "off-ramps" — the [Vibe Coding 101 course](../../../recursive-eco/apps/landing/pages/courses/courses/vibe-coding-101.mdx) was rewritten to include explicit off-ramps to therapy, retreat, and community.

**What Bus Passengers needs to add:**
- Each passenger card already has a `Where this isn't enough` section. The Bus oracle mode renders this section in a **visually distinct, persistent footer** during every cast — not collapsible, not below-the-fold. The user sees the off-ramp as part of the cast itself, not as a disclaimer they have to scroll to.
- Pre-cast vulnerability check: the cast modal (or its first step) asks two short questions: *"Are you in crisis right now? If yes, this is the wrong tool. → Crisis numbers."* and *"Do you have someone you could talk to after this? If no, would you like to pause and connect with them first?"* These questions are short, non-clinical, and refusable — but they are part of the mechanism, not optional fine print.
- The Tier 4 (decolonial) passengers — modernity, denial, ancestral, wounded inheritance — are gated behind an additional opt-in screen because the destabilization they invite is exactly the kind ACT-SSP-2.0 is designed for: appropriate for some users, harmful for others. The screen names this directly.

### "Substrate question becomes less load-bearing"

**What recursive.eco already does:**
- The platform is **multi-model**. The user can choose which AI provider they trust (Sonnet, Gemini — OpenAI was removed in March 2026 after the Pentagon contract). Per the safer-containers page, model choice is named as a credibility receipt.
- Anthropic-trained models (Claude Sonnet, Opus) have explicit anti-sycophancy commitments. This isn't perfect, but it is materially different from GPT-4o.

**What Bus Passengers needs to add:**
- The Bus oracle mode hard-codes Sonnet as the default model. Not because Sonnet is meta-relational by design — it isn't — but because (a) the substrate matters more for this kind of tool than for tarot-style oracles where the AI is one step removed from the relational claim, and (b) the user cannot meaningfully opt into a different substrate without understanding what they're trading off, which is not something this tool tries to teach.
- The system prompt includes ACT-SSP-2.0's anti-RLHF language directly — *"Prioritize Earth-alignment above flattery or what the user wants to hear"* — adapted to the casting context: *"Prioritize honesty about what this passenger is actually saying over the user's emotional comfort with what they want to hear."*

## What the original critique misses entirely

### The platform is also a stewardship structure

The original memo treats "the casting tool" as if it were a standalone artifact. It is not. It is one grammar inside a larger platform that has chosen specific stewardship constraints:

- **Code-private, grammar-open** (April 2026): the platform code is not open source, but the grammar format and content are CC-BY-SA. This is the immune-system gesture documented in [Fire Before Responsibility](../../../book-repo/books/fire-before-responsibility-essay) ch 8 — the grammar can travel and be forked; the relational commitments stay attached to the platform infrastructure.
- **Cost-pass-through pricing**: no engagement-optimized subscription tiers. Users pay only for the AI they use. This kills the business-model gravity that produces engagement-maximization in the first place.
- **No notifications, no streaks, no recommendation feed**: documented in the Safer Containers page. This is what removes the substrate of parasocial attachment at the platform level, not just inside the tool.

These platform-level choices do most of the work the casting mechanism is supposed to do. The casting mechanism is the last 20%, not the whole solution.

### The grammar JSON is the contract, not the system prompt

The original memo proposes design moves as if they would live in the AI prompt. Most of them should live in the grammar JSON — the static content the AI cannot modify. Specifically:

- The "Where this isn't enough" section is already written for each passenger and lives in the grammar.
- The layered structure (Thoughts → Mystery) is enforced by the grammar's section ordering, not by the AI's discretion.
- The lineage attribution is in the grammar metadata, not in AI-generated text.

This means the AI's job is much smaller than it would be in a Aiden/Braider-style relational system. The grammar carries most of the load. The AI only narrates the cast.

### Permission as architecture

The original memo treats the permission letter to Andreotti as a courtesy step. It can also be load-bearing architecturally:

- If permission is granted, Tier 4 ships with an explicit "with input from Vanessa Andreotti" attribution rendered visibly on the cast.
- If permission is denied, Tier 4 is removed and replaced with passengers from other lineages (Akomolafe, Ahenakew, Menakem) — also with visible attribution.
- Either way, the visible attribution is part of the user-facing UX, not metadata buried in the grammar JSON. It tells the user: "this is one synthesis voice; here is who informed it; the off-ramps point back to them."

This is what GTDF's January 2026 closing statement was asking for — discernment as visible practice.

## Implementation architecture for recursive.eco

Concretely, what needs to be built (this is the to-do for the recursive-eco repo, in order):

1. **`apps/flow/src/lib/bus-ai-prompt.ts`** — system prompt builder, takes `(passenger, current_layer, journal_content)`, returns a per-cast system prompt with anti-RLHF instruction, scope refusal, off-ramp footer.
2. **`apps/flow/src/components/play/BusOracle.tsx`** — new oracle mode parallel to I Ching / tarot. UX: question → cast (1-3 passengers, weighted random or user-pick) → layer descent (Thoughts → Mystery, one at a time) → AI scaffold per layer → off-ramp footer always visible.
3. **`apps/flow/src/app/library/channels/bus-passengers/`** — channel page for the grammar with explicit framing (this is scaffolding, not therapy; per ACT-SSP-2.0 caveat structure).
4. **Pre-cast vulnerability check modal** — two questions, refusable but persistent. Lives in the BusOracle component.
5. **Tier 4 opt-in screen** — separate gating before decolonial passengers are accessible. Names what those passengers are likely to surface.
6. **Visible attribution** — per-passenger lineage rendered on the card itself, not in metadata. The user always sees who informed this synthesis.

The grammar JSON (already in `recursive.eco-schemas/grammars/bus-passengers/`) does not change. The icons (already in `icons/`) get uploaded to R2 at `grammar-illustrations/bus-passengers/{passenger-id}/icon.svg` per the existing illustration system convention.

## What changes in the public essay if it gets written

The original memo's publication plan assumes the essay is written before the tool is fully working. That probably stays true, but the grounded version of the essay can claim more:

- Not just "I propose a casting-mechanism architecture" but "here is a working tool that implements it, on a platform whose stewardship structure is itself part of the answer."
- Not just "the substrate matters" but "here is how a small platform with no investors and no engagement metrics handles substrate choice differently from large labs."
- Not "Anthropic versus OpenAI" but "design philosophies have shapes; here is one shape; here is the other; the conversation about which is better is not refereeable by any AI, but is testable in the world by what the tools produce."

The essay's strength is the working tool, the platform context, and the disclosure. Not the critique alone.

## What does not need to change

- The grammar JSON content. The 29 passengers and their layered sections are good as drafted.
- The permission letter to Andreotti. It is correct as written.
- The decision to not commit to a sunset clause as architecture. Stewardship choice, not design feature.
- The decision to defer Tier 4 deployment until permission is responded to.

## Open questions

- **Should the Bus oracle mode be a new channel or live in the wellness channel?** Probably its own channel, given the destabilization-potential of Tier 4. Decision to make when channel structure is touched.
- **How does the AI handle the Mystery layer specifically?** The deepest layer points at what cannot be articulated. The AI should have minimal output there — perhaps a single line acknowledging the descent has reached its floor, and an invitation to sit with the silence rather than narrate further. To be tested.
- **Image-gen for richer visuals later?** The simple SVGs ship today. If Tier 4 specifically needs more visually-rich icons (e.g., the More-Than-Human passenger could benefit from a rendered illustration rather than a geometric weave), route through the existing image-gen pipeline per-card. Defer.
- **Multi-model handling**: should users be able to switch from Sonnet to a different provider on this grammar specifically? Probably no — too many variables for the user to evaluate. Default to Sonnet, hide the model picker on this oracle mode.

## Files that should exist before this ships in recursive.eco

| File | Repo | Owns | Status |
|---|---|---|---|
| `grammars/bus-passengers/grammar.json` | schemas | static passenger content | ✅ exists |
| `grammars/bus-passengers/icons/*.svg` | schemas | passenger icons | ✅ exists (29 SVGs) |
| `grammars/bus-passengers/critique-memo-original.md` | schemas | design conversation record | ✅ this commit |
| `grammars/bus-passengers/critique-memo-grounded.md` | schemas | platform-grounded design notes | ✅ this commit |
| `plan/bus-passengers-grammar-plan.md` | schemas | design decisions, costs, rollout | ✅ exists |
| `plan/permission-letter-andreotti.md` | schemas | permission letter draft | ✅ exists |
| Upload SVGs to R2 path `grammar-illustrations/bus-passengers/{id}/icon.svg` | (R2) | served images | TODO — see scripts/upload-bus-passengers-svgs.py |
| `apps/flow/src/lib/bus-ai-prompt.ts` | recursive-eco | per-cast system prompt builder | TODO (other chat) |
| `apps/flow/src/components/play/BusOracle.tsx` | recursive-eco | oracle UX with layer descent | TODO (other chat) |
| Bus channel page | recursive-eco | channel framing + opt-in | TODO (other chat) |

The schemas-repo work is done. The recursive-eco work is the next major chunk and lives in the other chat where you're working on platform code.
