# Bus Passengers Grammar — Plan

**Created:** 2026-05-05
**Author:** PlayfulProcess
**Status:** First draft generated; permission letter pending; not yet imported to recursive.eco

---

## What this is

A parts-work grammar for recursive.eco that helps users notice **which passenger is driving** when they make a values-laden decision. Each passenger card has six layered sections that descend from articulated voice toward the more-than-human web. The grammar lives at `grammars/bus-passengers/`.

## The layered design

Inspired by a passage in Andreotti's *Outgrowing Modernity* (Kindle reading, May 2026) on the layered nature of awareness — that what we articulate is a small fraction of what we think, what we think is a fragment of what we perceive, what we perceive is a sliver of what we sense, and what we sense is an infinitesimal part of what is here.

Each passenger card has six sections, descending from the tip of language to the ground:

| Layer | What it surfaces |
|---|---|
| **Thoughts** | What this passenger says out loud — the user's starting point |
| **Thinking** | The pattern of thought beneath the words |
| **Perception** | What this passenger filters in / out of awareness |
| **Sensing** | Where this passenger lives in the body, beyond the five senses |
| **Context** | What is actually here in the situation, before interpretation (proxy for "reality") |
| **Mystery** | The more-than-human web; what is unknowable; what was always here |

Each card also has an **About** header (one-line tagline), a **Where this isn't enough** off-ramp pointing to community/therapy/books/practice, and a **Lineage** attribution.

## Four tiers of passengers (29 cards total)

| Tier | Theme | Cards | Source |
|---|---|---|---|
| **1** | Familiar emotions | Joy, Sadness, Anger, Fear, Disgust, Anxiety, Envy, Embarrassment, Ennui (9) | Pixar Inside Out 1 + 2 (Ekman / Keltner / Damour) — public-domain archetypes |
| **2** | Parts-work passengers | Manager, Firefighter, Exile, Self-energy, Inner Critic (5) | Generic parts-work language inspired by IFS (Schwartz). "IFS" is trademarked; this tier uses generic framing only. |
| **3** | Voice Dialogue inner selves | Pusher, Pleaser, Rule Maker, Vulnerable Self, Aware Ego (5) | Voice Dialogue (Hal & Sidra Stone) — explicitly not trademarked |
| **4** | Decolonial passengers | Modernity, Denial, Ancestral, Wounded Inheritance, Carriage Driver, Baby Mountain, Warrior Mountain, Provider Mountain, Elder Mountain, More-Than-Human (10) | Synthesized in PlayfulProcess's voice from CC-BY GTDF *GCE Otherwise* booklet, *Hospicing Modernity*, *Towards Braiding* and *Towards Scarring* (CC), Andreotti's open academic papers. Permission letter pending. |

Plus 4 L2 emergence items, one per tier, that group their child cards with descriptive "About this tier" and "How to use it" sections.

**Total:** 29 L1 + 4 L2 = 33 grammar items.

## Design decisions made

### Sunset clause: deferred (not committed)

The original plan included a hard sunset clause modeled on the Aiden/Braider retirement (when usage exceeds one developer's capacity, retire and open-source the protocol). PlayfulProcess flagged this as too binding. **Decision:** keep the *option* of graceful retirement available; do not commit to it as a design feature. Stewardship choice, not architecture.

### Layered structure: six layers (Thoughts → Mystery)

Replaced the original five-layer plan (Reality → Thoughts) with six layers, renaming "Reality" to "Context" and adding "Mystery" as the deepest layer. **Reasoning:** "Reality" is too modernist a frame — implies one settled ground. "Context" is more honest about it being a proxy. "Mystery" gives the user somewhere to descend toward that doesn't pretend to be knowable.

### Per-item AI prompts: re-uses existing infrastructure

Codebase scout of `recursive-eco/apps/flow/src/lib/iching-ai-prompt.ts` confirmed the pattern: `buildIChingSystemPrompt(reading, journalContent)` builds a per-reading system prompt with the specific hexagram + changing lines + user's journal. **Bus Passengers can use the same pattern**: write a `buildBusPassengerSystemPrompt(passenger, currentLayer, journalContent)` function that injects the specific passenger's six layered sections and the user's current layer of focus into the prompt. **No architectural expansion needed.** This keeps the tool inside the existing footprint.

### SVG icons: simple geometries, programmatic

Each passenger has a simple geometric icon (circle, triangle, hexagon, spiral, mountain, tree, etc.) generated programmatically by the build script. Stroke-only, single-color, 100×100 viewBox. **Reasoning:** stays inside the existing tool's visual language; doesn't require an image-gen API call per card; cheap to regenerate; reads as cartographic rather than illustrative.

If later you want richer visuals: route those through the existing recursive.eco image-gen pipeline (Gemini or whatever's wired there), per-card, on demand. The current SVGs are placeholders that work as primary icons until/unless replaced.

## Files generated

```
grammars/bus-passengers/
  grammar.json              (60.7 KB, 33 items)
  icons/
    joy.svg
    sadness.svg
    ...                     (29 SVG icons)

scripts/
  build-bus-passengers-grammar.py   (re-runnable generator)

plan/
  bus-passengers-grammar-plan.md    (this file)
  permission-letter-andreotti.md    (draft)
```

## Permission status

- **Tier 1, 2, 3:** No permissions needed. Pixar/Ekman/Damour are public-domain archetypes; IFS uses generic framing; Voice Dialogue is explicitly not trademarked.
- **Tier 4:** Permission letter to Vanessa Andreotti drafted, **not sent yet**. The grammar's tier-4 cards are written in PlayfulProcess's paraphrased voice from CC-licensed materials (GCE Otherwise booklet is CC-BY 4.0; *Towards Braiding* and *Towards Scarring* are CC; *Hospicing Modernity* is read for reference; *Outgrowing Modernity* is **not** used in any AI context per its anti-AI clause). Tier 4 ships only after Andreotti's response.

If permission denied: drop tier 4. Replace with passengers drawn from Bayo Akomolafe's openly-published essays, Cash Ahenakew's CC *Towards Scarring*, Resmaa Menakem's *My Grandmother's Hands*, and adjacent open material.

## Roll-out path

1. **Now**: Plan doc + permission letter committed to schemas. Grammar.json generated locally.
2. **Permission letter sent**: Wait for response (1-4 weeks).
3. **If permission granted**: Import to Supabase via `bulk-import-grammars.js`. Grammar appears in `library/channels/wellness` (or its own channel — see open question below).
4. **If permission denied**: Replace tier 4 cards. Re-import.
5. **Build the per-item AI prompt** (`buildBusPassengerSystemPrompt`) in the recursive.eco codebase — separate task, separate session.
6. **Ship behind the safer-containers framing** — opt-in, with the existing `/pages/safer-containers.html` mental health disclaimers visible.

## Open questions for PlayfulProcess

1. **Channel placement:** Wellness channel, or its own channel ("Bus Passengers" / "Parts Work")? The decolonial framing might fit better in its own space rather than mixed with general wellness tools.
2. **Image-gen for richer visuals:** Stick with simple SVGs, or route per-card image-gen through the existing pipeline once the grammar is live? SVGs ship today either way.
3. **AI chat scope:** When a user draws a passenger and engages the AI, is the AI scoped to *that passenger only* (refuses to discuss others until the user explicitly switches), or scoped to the whole bus (can name other passengers as relevant)? First option is more disciplined; second is more flexible.
4. **Layer-by-layer ritual:** Does the AI guide the user through the layers in order (Thoughts first, Mystery last) by default, or does it stay user-led? First option is more pedagogically structured; second matches the no-savior posture better.
5. **Permission letter timing:** Send now, wait for the Wallis RAG to be working first, or wait until the grammar has been tested locally? My instinct: send now. Letting Andreotti know about the project early gives her time to respond and gives you time to integrate her input.

## Costs (rough)

- **Grammar import** to Supabase: free (one-time).
- **SVG icons**: free (already generated).
- **Per-session AI cost** (estimated): ~$0.001-0.005 per user message at Sonnet pricing, depending on context size. Layered sections + journal could push toward the higher end.
- **No R2 RAG infrastructure needed** for this grammar — the layered card content lives in the grammar.json and is loaded with the rest of the grammar. RAG is only needed if you later want the AI to reference Andreotti's writing directly (with her permission and citation).

## Companion files

- Permission letter: `plan/permission-letter-andreotti.md`
- Research basis: `book-repo/research/andreotti-gtdf-bus-tool-research-2026-05.md`
- Ethical guardrails for synthesis: `book-repo/transcripts/andreotti-corpus/README.md`
