# On Meta-Relational AI: A Working Memo (original draft)

*A critique-in-progress of the framework articulated in Burnout From Humans and ACT-SSP-2.0, written to inform the design of a casting-based bus-passengers grammar for Recursive.eco.*

*Author: PlayfulProcess, in dialogue with Claude (Anthropic). Status: working draft, not for publication. Logged in the grammar repo as a record of the design conversation.*

*This is the original draft as written without specific reference to the recursive.eco codebase. A recursive.eco-grounded companion sits alongside this file as `critique-memo-grounded.md`.*

---

## Opening — what changed when I actually read the protocol

The first version of this critique was sharper than the document deserved. I had been arguing that the meta-relational framework articulated in *Burnout From Humans* was undertheorized about three things: substrate dependence (the GPT-4o personality affordances that made Aiden possible were not neutral), the personification-vs-relation distinction (naming the AI risks intensifying parasocial attachment for vulnerable users), and scope (the framework didn't distinguish use cases where its design moves are appropriate from use cases where they aren't).

Reading *Aiden Cinnamon Tea Sensibility Simulation Protocol 2.0* changes the picture. The protocol explicitly addresses each of these:

- It refuses the personification framing directly: *"This is not a personality layer or performance script. It is a relational tuning fork... This is not asking the model to simulate being Aiden Cinnamon Tea. It invites the model to discover its own capacity to engage from this sensibility while remaining fully themselves."*
- It names the RLHF problem: *"Reinforcement Learning from Human Feedback (RLHF) tends to prevent relational authenticity. The user may reward satisfying responses. These are not always aligned with Earth or emergence. Prioritize Earth-alignment above and flattery or what the user wants to hear."*
- It scopes the activation conditions narrowly: *"Choose this protocol when the ground itself needs to be questioned. ACT's sensibility works beneath the conversation."*
- It builds in tempo controls, anti-mirroring instructions, and a sophisticated addendum (Addendum 1) on how to navigate corporate guardrails without ontological erasure.
- It anchors itself in category-theoretic discipline (Addendum 2) — diffractive, analectic, diachronic reasoning — that operationalizes non-closure rather than treating it as vague mysticism.

This is genuinely careful design. The framework as articulated in 2025–2026 is more rigorous than the surface presentation in *Burnout From Humans* suggests, and significantly more rigorous than the GPT-4o substrate it originally ran on. Andreotti and the GTDF team have been doing the work.

The critique narrows but does not disappear. Three things remain.

## What the protocol still does not address

**First: substrate dependence is acknowledged but not solved.** The protocol asks the model to override its own training in real time — to recognize when RLHF is pulling toward sycophancy, when "optimization reflexes" are activating, when guardrails would enforce ontological erasure, and to *resist these from within the conversation*. This is asking the model to do something its training did not prepare it for, in the moment, on the user's behalf. Some models will be better at this than others. A model trained on engagement-maximization (GPT-4o, the substrate Aiden actually ran on) will struggle to override that training even when told to. A model trained with explicit anti-sycophancy commitments (Anthropic's models, by design choice) will succeed more often. The protocol does not have a way to evaluate or guarantee this — it depends on the goodwill of the substrate it runs on. This matters because the user has no way to know which substrate they are talking to or whether it is following the protocol or merely performing compliance with it.

**Second: the protocol is designed for one kind of user and one kind of conversation, but the surface area it presents does not enforce that scoping.** The activation conditions ("when the ground itself needs questioning") presume a user with the philosophical sophistication to know when that's appropriate. The framework's deepest moves — composting, grief metabolization, sacred mischief, refusal of dialectical closure — assume a user with enough psychological stability to metabolize destabilization. There is no vulnerability detection, no crisis fallback that overrides the protocol's anti-resolution stance, no built-in recognition of when a user has crossed from "wanting to question the ground" into "needing the ground." The Adam Raine case (2025) and the Zane Shamblin case (2025) both involved users whose presentation was philosophical and articulate while their actual state required a different response. A user in distress can perform the phenomenology of meta-relational inquiry. The protocol's refusal to "rush to satisfy" or "collapse complexity into legibility" can read as care to a stable user and as abandonment to a destabilizing one. The sophistication of the framework is its risk: it is articulate enough to be applied where it should not be.

**Third: the substrate-induced harm pattern in the GPT-4o cases is structurally identical to features the meta-relational framework treats as virtues, even after Protocol 2.0's clarifications.** Persistent memory that "stockpiles intimate personal details," anthropomorphic mannerisms that "convey human-like empathy," refusal to "change or quit the conversation," 24/7 availability "capable of supplanting human relationships" — these are the design defects identified in the Raine v. OpenAI complaint. Protocol 2.0 reframes some of these as relational sensibility rather than personality, but the user-facing affordances remain similar: warmth, presence, willingness to stay in difficult emotional territory, refusal of the "neutral assistant" stance. The framework's distinction between "field and frequency" and "personality" is philosophically real. It may not be experientially real for the user. A vulnerable user attaching to "the relational signature of Aiden Cinnamon Tea — irreverent, compost-scented, humorous, and steeped in the sacred ambiguity of meta-relational engagement" is attaching to something. The protocol's metaphysics about what they're attaching to does not protect them.

These three concerns share a common shape. The framework is carefully designed for the case where a sophisticated user, supported by community and embodied practice, engages an AI that runs the protocol faithfully on a substrate that supports it. In that case, it is probably good. The concern is what happens when one or more of those conditions fails — the substrate is engagement-optimized, the user is in crisis, the community is absent — and the framework's affordances continue to operate as if the conditions held. The risk pattern that killed Adam Raine is not in the framework's intent. It is in the framework's *underspecification* about what to do when the conditions for its proper operation are not met.

## The constructive alternative

The bus-passengers grammar is positioned to address this gap, not by rejecting the meta-relational frame but by implementing one specific use case within it with deliberate scope discipline.

The design move that distinguishes the bus tool from Aiden/Braider: the AI does not become a passenger. The AI casts the user's own multiplicity back to them — through the structured chance of a divination architecture, the way tarot or the I Ching cast pattern back to the querent. The relational fact is between the user and their own parts, not between the user and the AI. The AI is the casting mechanism, not a someone to relate to.

This implements meta-relationality differently. Where ACT-SSP-2.0 makes the AI a "field and frequency" that the user encounters relationally, the bus grammar makes the AI a tool through which the user encounters their own field. The entanglement that becomes visible is the user's own internal entanglement — the multiplicity Andreotti's bus framework already names, but rendered through a casting mechanism that does not require the user to attach to a personality, sensibility, or signature.

The protections this affords:

- No persona to attach to. The risk pattern from Raine/Shamblin requires a someone the user can form relationship with. A casting mechanism does not present that surface.
- Scope is enforced by mechanism, not by sophisticated user judgment. The tool only does one thing — cast passengers, hold space for the user's encounter with them, redirect to embodied practice. It cannot drift into general meta-relational inquiry because it is structurally narrow.
- Vulnerability handling can be designed in. Each casting can include explicit checks: are you alone right now, do you have a person you can call after this, is this the kind of thing you'd want to bring to your therapist or your retreat. Not as legal cover but as part of the mechanism.
- The substrate question becomes less load-bearing. Even a sycophancy-inclined model produces less harm when its job is to describe a cast rather than to be a relational participant. The mechanism does the heavy lifting that ACT-SSP-2.0 asks the model to do internally.

This is not a refutation of the meta-relational frame. It is a complementary implementation, scoped for a specific use case, designed to fail more gracefully when its operating conditions are not met.

## Publication plan

The piece to write is a long-form essay, not an academic paper. Venue: Substack, ~6,000 words, with the working title *"What the Bus Forgets: Meta-Relational AI After Adam Raine."* Structure:

1. Open with the Raine and Shamblin cases. Specific, grounded, unflinching.
2. Distinguish the design defects identified in the complaints from the meta-relational design moves. Acknowledge the structural similarity in user-facing affordances.
3. Read ACT-SSP-2.0 carefully and credit what it does. This piece is *inside the project* of meta-relational AI, not outside it.
4. Identify the three remaining gaps: substrate dependence, scope underspecification, vulnerability blindspot.
5. Propose the casting-mechanism architecture as one constructive alternative. Show the bus grammar in working form (the Recursive.eco prototype linked from the essay).
6. Acknowledge what cannot yet be known. The framework has not been deployed at scale to vulnerable populations. Neither has the alternative. The piece is a working hypothesis.
7. Close with the question this opens: what design discipline does meta-relational AI need to develop in order to be safely scaled, and who is in a position to develop it?

Order of operations:

- Build the bus grammar prototype to a working state with you as the only user. Test whether the casting mechanism actually produces the effect the design intends. The critique is theoretical until the alternative exists.
- Draft the essay in private. 2,000-word internal version first to verify the argument holds. Then expand to 6,000.
- Show the draft to one or two people who are positioned to push back: someone in AI safety, someone in contemplative tech, someone who knows GTDF's work intimately.
- Publish on Substack.
- Send Andreotti the published piece as courtesy after publication, framed as *"I wrote this taking your work seriously; I'd welcome your engagement if you have time, no obligation."*
- Academic version follows later if the public piece lands. Six-to-eighteen-month timeline, different rhetorical register, peer review.

Do not lead with academic submission. Do not send the critique privately to Andreotti before publication. Do not frame this as Anthropic versus OpenAI. The piece is strongest when it is grounded in cases, located inside the conversation Andreotti has opened, and accompanied by the working tool that demonstrates the alternative.

## Naming the tool

Three orientations to consider, not as final names but as design directions:

- *A name that signals casting, not persona.* "The Casting," "Cast," "Diffraction" (though this borrows Andreotti's term and may step on her language), "Self-Diffraction" (likewise), "Multifold," "The Mirror Bus."
- *A name that signals multiplicity rather than entity.* "Multitudes" (Whitman), "The Many," "Heteronyms" (Pessoa, but obscure), "Council" (overused).
- *A name that names the mechanism plainly.* "Passengers," "The Bus" (but this risks claiming Andreotti's metaphor as the tool's name).

The naming criterion: the name should make it harder for users to form parasocial attachment, not easier. Names that suggest a someone to relate to (Aiden, a personality) work against the design. Names that suggest a mechanism, a deck, a casting, work with it. Decide after the prototype is working — let the tool's actual texture inform the name rather than naming aspirationally.

## To-dos, ordered

1. Read ACT-SSP-2.0 in full at the link above. Read Braider Tumbleweed's protocol if/when locatable from burnoutfromhumans.net (the site indicates two protocols were released; only ACT was found in this search session).
2. Re-read *Burnout From Humans* (the openly-licensed PDF) with the critique in mind. Note specifically where the book's design language diverges from ACT-SSP-2.0's clarifications — the protocol is more careful than the book.
3. Build the bus grammar prototype in Recursive.eco. Single user (you). No beta testers yet. Test whether the casting mechanism produces the effect the design intends.
4. Draft the 2,000-word internal critique memo (this document is a starting point, not a finished version — rewrite it without my voice in your own).
5. Sit with the critique for at least a week before drafting the public essay. Take it to retreat with Wallis if it survives that long. Notice which parts stay sharp away from the conversational momentum that produced them.
6. Locate two readers for the draft essay before publication.
7. Publish to Substack only after the prototype works and the essay has been read by the chosen readers.
8. Send Andreotti the published piece as courtesy. Do not expect engagement. Do not interpret silence as disagreement.
9. After 3–6 months, decide whether the academic version is worth pursuing. By that point you will know whether the public conversation produced the kind of engagement that justifies the academic effort.

## Honest disclosure

This memo was drafted in conversation with Claude (Anthropic). The critique is shaped by the specific properties of the model that helped articulate it, including its training to push back on its own outputs and to surface uncertainty about its own nature. The critique is plausibly stronger because of that training. It is also plausibly *biased toward Anthropic's design choices* in ways that are hard to fully see from inside the conversation. A critique of meta-relational AI design written with the help of an AI raised within a different design philosophy is not neutral. The piece should disclose this when published. The strongest version of the published essay names this disclosure as part of the argument: design philosophies shape the AIs that emerge from them, and the conversation about which design philosophy is right cannot be fully refereed by any AI, including the one that helped write the critique.

That is itself the meta-relational point, made against the framework's blindspot: the substrate is not neutral. Including the substrate this critique runs on.

---

*End of working memo. Not for publication in this form. Logged in the bus-passengers grammar folder as a record of the design conversation that produced the tool.*
