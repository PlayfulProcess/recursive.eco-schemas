"""
Generate the Bus Passengers grammar — a parts-work / decolonial cartography
for recursive.eco. Produces grammar.json + per-item SVG icons.

Design:
- Each passenger has 6 layered sections (Thoughts → Thinking → Perception →
  Sensing → Context → Mystery), descending from articulated voice toward the
  more-than-human web. Inspired by Andreotti's *Outgrowing Modernity* passage
  on the layers of awareness ("what we articulate is a small fraction of what
  we think, what we think is a fragment of what we perceive...").
- Four tiers of passengers (Pixar emotions, parts-work, voice dialogue,
  decolonial), drawing on public-domain frameworks plus CC-BY GTDF
  materials.
- Each passenger gets a simple geometric SVG icon stored alongside the
  grammar.

Run: python scripts/build-bus-passengers-grammar.py
Output:
  grammars/bus-passengers/grammar.json
  grammars/bus-passengers/icons/<id>.svg
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "grammars" / "bus-passengers"
ICONS_DIR = OUT_DIR / "icons"

LAYERS = [
    ("Thoughts", "What this passenger says out loud — the articulated voice the user usually starts with."),
    ("Thinking", "The pattern of thought beneath the words. The mental formation generating the voice."),
    ("Perception", "What this passenger filters in and out of awareness. Where attention goes, where it can't."),
    ("Sensing", "Where this passenger lives in the body — beyond the conventional five senses."),
    ("Context", "What is actually here in the situation, before interpretation. The conditions this passenger is responding to."),
    ("Mystery", "The more-than-human web this passenger is part of. What is unknowable. What was always here."),
]


# ----------------------------------------------------------------------
# SVG generators — simple geometric shapes per archetype
# ----------------------------------------------------------------------

def svg_wrap(body, color="#5B5F75"):
    """Wrap an SVG path/shape body in a 100x100 viewBox SVG with the given stroke color."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">\n'
        f'  <g fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n'
        f'    {body}\n'
        f'  </g>\n'
        f'</svg>'
    )


SHAPES = {
    "circle":      lambda c: svg_wrap('<circle cx="50" cy="50" r="35"/>', c),
    "downarc":     lambda c: svg_wrap('<path d="M 15 35 Q 50 75 85 35"/>', c),
    "triangle":    lambda c: svg_wrap('<polygon points="50,18 85,78 15,78"/>', c),
    "jagged":      lambda c: svg_wrap('<polyline points="20,75 30,40 40,60 50,30 60,55 70,35 80,75"/>', c),
    "pentagon":    lambda c: svg_wrap('<polygon points="50,18 85,42 72,80 28,80 15,42"/>', c),
    "spiral":      lambda c: svg_wrap('<path d="M 50 50 m -3 0 a 3 3 0 1 1 6 0 a 6 6 0 1 1 -12 0 a 12 12 0 1 1 24 0 a 18 18 0 1 1 -36 0"/>', c),
    "twocircles":  lambda c: svg_wrap('<circle cx="38" cy="50" r="20"/><circle cx="62" cy="50" r="20"/>', c),
    "uparc":       lambda c: svg_wrap('<path d="M 15 65 Q 50 25 85 65"/>', c),
    "wave":        lambda c: svg_wrap('<path d="M 15 50 Q 30 30 45 50 T 75 50 T 105 50"/>', c),
    "square":      lambda c: svg_wrap('<rect x="20" y="20" width="60" height="60"/>', c),
    "diamond":     lambda c: svg_wrap('<polygon points="50,15 85,50 50,85 15,50"/>', c),
    "ring":        lambda c: svg_wrap('<circle cx="50" cy="50" r="35"/><circle cx="50" cy="50" r="20"/>', c),
    "shield":      lambda c: svg_wrap('<path d="M 50 15 L 80 25 L 80 55 Q 80 80 50 90 Q 20 80 20 55 L 20 25 Z"/>', c),
    "flame":       lambda c: svg_wrap('<path d="M 50 85 Q 25 70 30 45 Q 35 25 50 15 Q 60 30 55 45 Q 75 60 50 85 Z"/>', c),
    "hexagon":     lambda c: svg_wrap('<polygon points="50,15 85,32 85,68 50,85 15,68 15,32"/>', c),
    "vesica":      lambda c: svg_wrap('<circle cx="40" cy="50" r="25"/><circle cx="60" cy="50" r="25"/>', c),
    "arrow":       lambda c: svg_wrap('<polyline points="20,50 80,50"/><polyline points="60,30 80,50 60,70"/>', c),
    "tree":        lambda c: svg_wrap('<line x1="50" y1="85" x2="50" y2="50"/><polygon points="50,15 75,50 25,50"/>', c),
    "scales":      lambda c: svg_wrap('<line x1="50" y1="20" x2="50" y2="80"/><line x1="20" y1="35" x2="80" y2="35"/><circle cx="20" cy="55" r="12"/><circle cx="80" cy="55" r="12"/>', c),
    "anchor":      lambda c: svg_wrap('<line x1="50" y1="20" x2="50" y2="80"/><circle cx="50" cy="25" r="8" fill="none"/><path d="M 25 70 Q 50 90 75 70"/>', c),
    "spiral2":     lambda c: svg_wrap('<path d="M 50 50 m -8 0 a 8 8 0 1 0 16 0 a 12 12 0 1 0 -24 0 a 16 16 0 1 0 32 0 a 20 20 0 1 0 -40 0"/>', c),
    "knot":        lambda c: svg_wrap('<path d="M 30 30 Q 70 30 70 50 Q 70 70 30 70 Q 30 50 50 50 Q 70 50 70 30"/>', c),
    "river":       lambda c: svg_wrap('<path d="M 15 30 Q 35 30 35 50 Q 35 70 55 70 Q 75 70 75 50 Q 75 30 85 30"/>', c),
    "mountain":    lambda c: svg_wrap('<polyline points="15,80 35,40 50,55 65,30 85,80"/>', c),
    "moon":        lambda c: svg_wrap('<path d="M 65 25 Q 35 35 35 60 Q 35 80 65 85 Q 50 75 50 55 Q 50 35 65 25 Z"/>', c),
    "sun":         lambda c: svg_wrap('<circle cx="50" cy="50" r="18"/><line x1="50" y1="15" x2="50" y2="25"/><line x1="50" y1="75" x2="50" y2="85"/><line x1="15" y1="50" x2="25" y2="50"/><line x1="75" y1="50" x2="85" y2="50"/><line x1="25" y1="25" x2="32" y2="32"/><line x1="68" y1="68" x2="75" y2="75"/><line x1="75" y1="25" x2="68" y2="32"/><line x1="32" y1="68" x2="25" y2="75"/>', c),
    "weave":       lambda c: svg_wrap('<path d="M 20 30 L 80 70"/><path d="M 80 30 L 20 70"/><path d="M 20 50 L 80 50"/>', c),
    "rootsystem":  lambda c: svg_wrap('<line x1="50" y1="20" x2="50" y2="50"/><line x1="50" y1="50" x2="30" y2="80"/><line x1="50" y1="50" x2="70" y2="80"/><line x1="50" y1="50" x2="50" y2="80"/><line x1="50" y1="50" x2="20" y2="65"/><line x1="50" y1="50" x2="80" y2="65"/>', c),
    "ouroboros":   lambda c: svg_wrap('<circle cx="50" cy="50" r="30"/><polyline points="75,40 80,50 75,60"/>', c),
    "house":       lambda c: svg_wrap('<polyline points="20,80 20,50 50,25 80,50 80,80 20,80"/><line x1="35" y1="80" x2="35" y2="60"/><line x1="35" y1="60" x2="50" y2="60"/><line x1="50" y1="80" x2="50" y2="60"/>', c),
}


# ----------------------------------------------------------------------
# Passenger data — 4 tiers, ~30 cards
# ----------------------------------------------------------------------

PASSENGERS = [
    # ============================================================
    # TIER 1 — Pixar / culturally-fluent emotion archetypes
    # ============================================================
    {
        "id": "joy", "name": "Joy", "tier": 1, "shape": "sun", "color": "#E8B547",
        "tagline": "The brightening, the lift.",
        "thoughts": "This is good. I want more. Look how good this is.",
        "thinking": "Pattern-matching toward what's working. Building case for sustaining the moment. Often unconsciously bargaining: if I notice it, will it leave?",
        "perception": "Filters toward the warm, the light, the people who are with you. Often dims the edges of the room.",
        "sensing": "An expansion in the chest. Lightness behind the eyes. A lifting at the mouth that came before the smile.",
        "context": "Something is going well. Right now, in this configuration. It might not last; it doesn't need to.",
        "mystery": "Joy is older than language. Other animals know it. You are participating in something far larger than your own pleasure when you feel it — and the not-knowing of that is part of its sweetness.",
        "where_isnt_enough": "When joy starts feeling like something to grip or perform, that's the cue to put the phone down and let it be without commentary.",
        "lineage": "Pixar Inside Out (Ekman / Keltner). Public-domain emotion archetype.",
    },
    {
        "id": "sadness", "name": "Sadness", "tier": 1, "shape": "downarc", "color": "#5B7AB8",
        "tagline": "The honest weight.",
        "thoughts": "This is hard. I don't have what I need. Something is gone.",
        "thinking": "Cataloguing what's missing. Tracing the shape of the loss. Often resisting the catalogue while making it.",
        "perception": "Filters toward absence. The room may feel emptier than it is. Voices may sound farther away.",
        "sensing": "A pulling-down in the chest. A heaviness behind the eyes. The body wanting to fold inward, not outward.",
        "context": "Something has actually been lost or is being lost. Something real that mattered. The grief is not a malfunction.",
        "mystery": "Sadness is one of the oldest songs. Many traditions consider it sacred. The body knows how to grieve in ways the mind has never been taught.",
        "where_isnt_enough": "If the heaviness is constant and the days are flat, this scaffolding stops being enough. A therapist, a doctor, or a trusted friend is the right next step.",
        "lineage": "Pixar Inside Out (Ekman / Keltner). Public-domain emotion archetype.",
    },
    {
        "id": "anger", "name": "Anger", "tier": 1, "shape": "triangle", "color": "#C13E3E",
        "tagline": "The boundary-feeling.",
        "thoughts": "This is wrong. This shouldn't be happening. Someone should answer for this.",
        "thinking": "Building case for action. Often confusing the trigger with the cause. Frequently arrives after a slower hurt that wasn't named in time.",
        "perception": "Narrows. Tunnel-vision toward the perceived violator. Filters out context and counter-evidence.",
        "sensing": "Heat in the chest, jaw, hands. Pressure behind the eyes. The body recruiting itself for something.",
        "context": "A boundary has been crossed, or a value violated. Or a value is being defended that you were not allowed to defend earlier in life.",
        "mystery": "Anger as a teacher of boundaries is older than the courts. In some traditions it is a form of love refusing to lie.",
        "where_isnt_enough": "If the heat keeps redirecting at the same person and you cannot find what's actually under it, an outside witness — therapist, mediator, trusted friend — helps more than another round of journaling.",
        "lineage": "Pixar Inside Out (Ekman / Keltner). Public-domain emotion archetype.",
    },
    {
        "id": "fear", "name": "Fear", "tier": 1, "shape": "jagged", "color": "#7E3FA8",
        "tagline": "The sharper edge of attention.",
        "thoughts": "Something is wrong. I need to be ready. I cannot let my guard down.",
        "thinking": "Running rehearsals of bad outcomes. Building case for vigilance. Often confusing imagined threat with present threat.",
        "perception": "Narrows toward perceived danger. Edges of the room go sharper; safe things become invisible.",
        "sensing": "A held breath. A coolness in the hands. The skin alert in places it usually isn't.",
        "context": "Something might be at stake. Sometimes the stakes are real and present. Sometimes they were real twenty years ago and the body has not been told the news.",
        "mystery": "Fear is a gift older than language. It has saved every ancestor who passed life on to you. The fact that you are alive is partly because fear was paying attention.",
        "where_isnt_enough": "Panic that arrives without a stimulus, or fear that organizes most of the day, is past the line where reflection is the right tool. Clinical support is.",
        "lineage": "Pixar Inside Out (Ekman / Keltner). Public-domain emotion archetype.",
    },
    {
        "id": "disgust", "name": "Disgust", "tier": 1, "shape": "pentagon", "color": "#5C8A3F",
        "tagline": "The instinctive no.",
        "thoughts": "This is wrong for me. This contaminates something.",
        "thinking": "Sorting in and out. Often inherited from family, culture, or trauma rather than freshly chosen. Sometimes accurate, sometimes not.",
        "perception": "Filters toward the offending object or person. Other things in the field can disappear.",
        "sensing": "A pulling-back in the throat or mouth. A skin crawl. The body recoiling slightly before the mind has decided.",
        "context": "Something violates a value, taste, or boundary that lives in this body. The disgust may be teaching you something about yourself, or about an inheritance.",
        "mystery": "The instinct that lets a body know what to push away is one of the oldest immune systems. It is not always wise; it is always old.",
        "where_isnt_enough": "When disgust attaches to whole categories of people, it has stopped serving you and started repeating something you didn't choose. Therapy and reading outside your tradition are better than journaling.",
        "lineage": "Pixar Inside Out (Ekman / Keltner). Public-domain emotion archetype.",
    },
    {
        "id": "anxiety", "name": "Anxiety", "tier": 1, "shape": "spiral", "color": "#D17F4E",
        "tagline": "The forward-leaning rehearsal.",
        "thoughts": "What if. What about. I should plan for. I should be ready.",
        "thinking": "Generating contingencies. Building forecasts. Often mistaking the rehearsal for the protection.",
        "perception": "Filters toward future scenarios. The present can become hard to land in.",
        "sensing": "A tightness behind the breastbone. Restlessness in the hands or legs. The body acting as if it must move soon, even when it doesn't.",
        "context": "Something is uncertain. Sometimes the uncertainty is real and active. Sometimes the body is protecting you from a different uncertainty that already happened.",
        "mystery": "Anxiety is not a malfunction of a calm mind. It is the mind doing what minds were made to do, applied to a situation older minds did not face. The body's care is older than the worry.",
        "where_isnt_enough": "If anxiety is the climate, not the weather — if every day arrives this way — this is not the right tool. A clinician is.",
        "lineage": "Pixar Inside Out 2 (Damour / Keltner). Public-domain emotion archetype.",
    },
    {
        "id": "envy", "name": "Envy", "tier": 1, "shape": "twocircles", "color": "#3F8A8E",
        "tagline": "The map of what you want.",
        "thoughts": "They have what I should have. Why not me. I deserved that more.",
        "thinking": "Comparison engines running in the background. Often using the other person as a map of the self's longing while pretending to be about them.",
        "perception": "Filters toward the other person's life. Often misses what they don't have or what it cost them.",
        "sensing": "A tightness in the gut or chest. A heat in the face. Sometimes a nausea.",
        "context": "Something you want is showing up clearly in someone else's life. The clarity is the gift, even when the feeling is corrosive.",
        "mystery": "Envy reveals the contour of a longing you may not have admitted to yourself. The longing is the data. The other person is the messenger, not the cause.",
        "where_isnt_enough": "When envy turns into action that diminishes the other, the practice has crossed a line. Stepping back, talking to a friend or therapist, and asking what the longing actually is — that's the work.",
        "lineage": "Pixar Inside Out 2 (Damour / Keltner). Public-domain emotion archetype.",
    },
    {
        "id": "embarrassment", "name": "Embarrassment", "tier": 1, "shape": "downarc", "color": "#C46AA8",
        "tagline": "The visible self, briefly aware of itself.",
        "thoughts": "They saw. I look bad. I want to disappear.",
        "thinking": "Imagining yourself from outside. Building case that you have failed a social standard. Often catastrophizing the visibility.",
        "perception": "Filters toward your own image in others' eyes. Filters out their actual likely indifference.",
        "sensing": "Heat in the face. A wanting-to-fold-up. A breath that didn't come.",
        "context": "You did something visible that crossed a social line. Sometimes the line was real; sometimes it was inherited and rigid.",
        "mystery": "Belonging matters because you are an animal made of relationship. Embarrassment is a cousin of belonging. It is not weakness.",
        "where_isnt_enough": "If embarrassment becomes shame and shame becomes hiding, the work is past this scaffold. Friends who love you. Therapy. The right kind of small repair, in person, when you are ready.",
        "lineage": "Pixar Inside Out 2 (Damour / Keltner). Public-domain emotion archetype.",
    },
    {
        "id": "ennui", "name": "Ennui", "tier": 1, "shape": "wave", "color": "#9494A8",
        "tagline": "The flatness with no name.",
        "thoughts": "Nothing matters. Whatever. I'm bored. I should be doing something.",
        "thinking": "Disengaged scanning. Often a defense against feeling something more specific that the body is not yet ready to feel.",
        "perception": "Everything slightly grey. Nothing pulls attention. Things that would normally interest you don't.",
        "sensing": "A heaviness or a numbness, depending on the day. The body present but quiet.",
        "context": "Something is being held at a distance. Sometimes you are tired in a real way that needs rest. Sometimes you are protecting yourself from something specific that's underneath.",
        "mystery": "The flatness is not nothing. It is something covering something else. The body is waiting for you to be ready.",
        "where_isnt_enough": "Persistent flatness with low energy and no joy in things that used to give joy is past this tool's range. A doctor and a therapist together is the right next step.",
        "lineage": "Pixar Inside Out 2 (Damour / Keltner). Public-domain emotion archetype.",
    },

    # ============================================================
    # TIER 2 — Parts-work passengers (generic IFS-flavored, avoiding trademarks)
    # ============================================================
    {
        "id": "manager", "name": "The Manager", "tier": 2, "shape": "scales", "color": "#4F6B8B",
        "tagline": "The one who tries to keep everything from breaking.",
        "thoughts": "I have to think about this. I have to plan. I have to keep us safe.",
        "thinking": "Strategic, anticipatory, controlling. Maintaining the daily structures. Often working without rest.",
        "perception": "Hyper-aware of risks, schedules, expectations. Less aware of present pleasure or rest.",
        "sensing": "Tension in the shoulders or jaw. A slight forward-leaning. Often disconnected from breath.",
        "context": "There are real responsibilities and the world is genuinely complicated. The manager is not wrong; it is just very tired.",
        "mystery": "This passenger is protecting parts of you that learned, long ago, that being managed kept everyone safe. It is a form of love that forgot it could rest.",
        "where_isnt_enough": "If the manager runs all night, the work is not in this tool. Sleep, somatic therapy, a long break, or someone else taking the wheel for a while.",
        "lineage": "Generic parts-work language inspired by IFS (Schwartz). 'Internal Family Systems' is trademarked; this card uses common-language parts framing only.",
    },
    {
        "id": "firefighter", "name": "The Firefighter", "tier": 2, "shape": "flame", "color": "#D14F2C",
        "tagline": "The one who breaks the glass.",
        "thoughts": "I need it now. Just this one thing. It will help.",
        "thinking": "Reaching for the immediate intervention — food, drink, scroll, work, drama. Often arrives when something painful gets too close.",
        "perception": "Tunnel toward the relief. The thing that was hurting drops out of view temporarily.",
        "sensing": "A grabbing-quality in the body. Hands that already know what they want to do.",
        "context": "Something more uncomfortable is right behind this. The firefighter is not stupid; it is doing exactly what it was hired to do.",
        "mystery": "This passenger is keeping the system running. If you forced it out without anything to replace it, the underlying part it protects would flood. Respect it.",
        "where_isnt_enough": "When the firefighter's intervention is itself causing harm — to your body, your relationships, your work — this scaffolding cannot replace community, therapy, or specific recovery support.",
        "lineage": "Generic parts-work language inspired by IFS (Schwartz). 'Internal Family Systems' is trademarked; this card uses common-language parts framing only.",
    },
    {
        "id": "exile", "name": "The Exile", "tier": 2, "shape": "moon", "color": "#7264A8",
        "tagline": "The young one carrying what nobody could hold then.",
        "thoughts": "Sometimes there are no thoughts here, just feelings. When there are thoughts: 'It was my fault. I was alone. Nobody came.'",
        "thinking": "Often pre-verbal. The patterns are old, formed before language was the main currency.",
        "perception": "Filters toward signs of the original abandonment, even decades later.",
        "sensing": "A specific quality of holding in the chest or belly. Sometimes a child's posture in an adult body.",
        "context": "Something happened, often early, that nobody at the time could metabolize with you. The exile is carrying it on behalf of the system.",
        "mystery": "This passenger is the part of you that kept feeling when the rest of you had to keep going. The fact that you can sit with it now means something has changed in your capacity to be a witness.",
        "where_isnt_enough": "Direct work with exiled parts is not for solo journaling. A therapist trained in parts work, somatic experiencing, or a similar approach is the right container.",
        "lineage": "Generic parts-work language inspired by IFS (Schwartz). The cautionary scope of this card is intentional.",
    },
    {
        "id": "self-energy", "name": "Self-Energy", "tier": 2, "shape": "ring", "color": "#C9A02E",
        "tagline": "The one who can be with all of it.",
        "thoughts": "Few thoughts. Mostly: 'I see you.' 'You are welcome here.' 'I am not going anywhere.'",
        "thinking": "Spacious, unhurried, curious. Less about strategy than about presence.",
        "perception": "Wider. Holds multiple passengers at once without choosing sides.",
        "sensing": "A settling. Breath returns. Shoulders drop. The body remembers it is not alone.",
        "context": "This is the part of you that has always been here, even when it felt unreachable. Not above the others; alongside them, with more room.",
        "mystery": "Many traditions have a name for this — Buddha-nature, the witness, the deep self, the soul. Each tradition is pointing at something hard to point at.",
        "where_isnt_enough": "Self-energy is the resource, not the answer. When the system is in crisis, finding this is the first step, not the only one.",
        "lineage": "Generic parts-work language for the centering capacity (related to IFS 'Self', Voice Dialogue 'Aware Ego', and many contemplative traditions' witness/observer).",
    },
    {
        "id": "inner-critic", "name": "The Inner Critic", "tier": 2, "shape": "diamond", "color": "#5A5A6E",
        "tagline": "The one who learned that pre-emptive scolding kept you safer.",
        "thoughts": "Not good enough. They're going to see. You should know better. You're a fraud.",
        "thinking": "Comparison engines, perfectionist standards, often quoting verbatim from someone who scolded you long ago.",
        "perception": "Filters toward your own flaws and others' implicit judgments. Filters out evidence of your competence.",
        "sensing": "A clenching in the chest. A specific kind of held breath. Sometimes a small audible 'hmph' that no one else hears.",
        "context": "At some point, scolding yourself before someone else could was the strategy that kept you in good standing. It worked. It is no longer the only available strategy.",
        "mystery": "The voice you hear is often not your own. It is a recording of someone who was once in your environment. You are not the recording. You are the one listening.",
        "where_isnt_enough": "When the critic dominates the day and erodes basic functioning, structured therapy is the work. This card is for noticing, not for replacing the work.",
        "lineage": "Common across parts-work traditions (IFS, Voice Dialogue, Gestalt). Generic framing.",
    },

    # ============================================================
    # TIER 3 — Voice Dialogue (Stones; explicitly not trademarked)
    # ============================================================
    {
        "id": "pusher", "name": "The Pusher", "tier": 3, "shape": "arrow", "color": "#B14F2C",
        "tagline": "The one who keeps you moving.",
        "thoughts": "Not done yet. One more thing. You can't stop now.",
        "thinking": "Forward-leaning, achievement-focused. Often confuses motion with worth.",
        "perception": "Sees the next task. Misses the body asking to rest.",
        "sensing": "A driving pressure behind the sternum. Hands that want to be doing.",
        "context": "Something needs to get done, sometimes. The pusher is excellent at delivery. It also runs on a deficit it doesn't know how to acknowledge.",
        "mystery": "This passenger learned, somewhere, that being still was unsafe — that you were only loved when you produced. That belief is older than your current life and it is not the truth.",
        "where_isnt_enough": "If the pusher won't let you rest even when you're ill, the practice is not journaling. It is sometimes radical: a doctor's note, a friend who books your day off, a retreat with no agenda.",
        "lineage": "Voice Dialogue (Hal & Sidra Stone). Voice Dialogue is explicitly not trademarked; the Stones welcomed open use.",
    },
    {
        "id": "pleaser", "name": "The Pleaser", "tier": 3, "shape": "vesica", "color": "#D78EAE",
        "tagline": "The one who reads the room before reading themselves.",
        "thoughts": "What do they want. How can I help. I shouldn't have said that.",
        "thinking": "Constantly adjusting to perceived need. Often over-reading micro-expressions. Almost always working harder than the situation requires.",
        "perception": "Hyper-attuned to others. Less aware of own preferences.",
        "sensing": "A subtle leaning-toward in the upper body. A breath held to listen.",
        "context": "Connection is real and matters. The pleaser is not wrong about that. It is mistaken only about how much of yourself you have to disappear to maintain it.",
        "mystery": "Belonging is a primary need. This passenger is protecting that need. It deserves gratitude even as it learns to take up a little more space.",
        "where_isnt_enough": "When the pleaser shapes your every relationship and you cannot find what you actually want, somatic and relational therapy do this work better than self-reflection alone.",
        "lineage": "Voice Dialogue (Hal & Sidra Stone). Voice Dialogue is explicitly not trademarked.",
    },
    {
        "id": "rule-maker", "name": "The Rule Maker", "tier": 3, "shape": "square", "color": "#5C5C7C",
        "tagline": "The one who keeps the structure standing.",
        "thoughts": "This is how it's done. There's a right way. We agreed on this.",
        "thinking": "Categorical, principled, often inherited verbatim from a parent or teacher. Stable but rigid.",
        "perception": "Sees rules and rule-violations clearly. Misses context and exceptions.",
        "sensing": "An uprightness in the spine. A held quality at the jaw.",
        "context": "Many rules exist for good reasons. The rule maker is excellent at consistency. It is sometimes mistaken about whether a rule is yours or someone else's.",
        "mystery": "Every rule was once a response to a real problem. The rule maker is, at root, trying to keep faith with the people who taught them. That loyalty is not the same as truth.",
        "where_isnt_enough": "If the rules are causing visible harm to you or someone you love, journaling won't override decades of conditioning. A therapist or trusted elder helps more.",
        "lineage": "Voice Dialogue (Hal & Sidra Stone). Voice Dialogue is explicitly not trademarked.",
    },
    {
        "id": "vulnerable-self", "name": "The Vulnerable Self", "tier": 3, "shape": "uparc", "color": "#9D4F7C",
        "tagline": "The one with thinner skin and longer ears.",
        "thoughts": "Few articulated thoughts. More like atmospheres: 'I don't want to be here.' 'I want to be held.' 'Please be kind.'",
        "thinking": "Pre-verbal or near-verbal. Often arrives as a feeling tone before a thought.",
        "perception": "Sensitive to subtle shifts that other passengers miss. Sometimes overwhelmed by them.",
        "sensing": "A quality of openness in the chest. A face that wants to be looked at gently.",
        "context": "There is a part of you that knows things the busier parts don't. It needs slower air. Most environments do not give it slower air.",
        "mystery": "This passenger may be the closest to what some traditions call soul. It does not respond well to performance, including spiritual performance. It responds to presence.",
        "where_isnt_enough": "When this passenger is in a lot of pain and is not being held in any human relationship, that is a real gap. Therapy, intimate friendship, a community of practice — relational containers, not solo ones.",
        "lineage": "Voice Dialogue (Hal & Sidra Stone). Voice Dialogue is explicitly not trademarked.",
    },
    {
        "id": "aware-ego", "name": "The Aware Ego", "tier": 3, "shape": "ring", "color": "#3F7E8B",
        "tagline": "The one who can sit between two passengers without picking a fight.",
        "thoughts": "I notice the part that wants to push and the part that wants to hide. I don't have to be either right now.",
        "thinking": "Holding tension between opposites without collapsing into either. The 'and' rather than the 'either-or.'",
        "perception": "Sees both sides of a conflict at once, including both internal sides. Doesn't lose access to either.",
        "sensing": "A widening of the chest. Breath returns. Time slows slightly.",
        "context": "This isn't above the bus. This is what becomes available when you're not blended with any one passenger. It is a capacity, not a person.",
        "mystery": "The Stones called this 'aware ego' carefully — not 'higher self' or 'true self.' It is a place to stand, not a person to become.",
        "where_isnt_enough": "Aware ego is the room you do the work in, not the work itself. Real change usually still happens through specific interventions: therapy, body practice, relationship, action.",
        "lineage": "Voice Dialogue (Hal & Sidra Stone). Voice Dialogue is explicitly not trademarked. Closely related to IFS 'Self' and contemplative traditions' witness.",
    },

    # ============================================================
    # TIER 4 — Decolonial passengers (synthesized from CC-licensed
    # GTDF GCE Otherwise booklet + Andreotti academic papers in
    # PlayfulProcess's own paraphrased voice).
    # ============================================================
    {
        "id": "modernity-passenger", "name": "The Modernity Passenger", "tier": 4, "shape": "house", "color": "#B89F6E",
        "tagline": "The one who thinks the house was always the world.",
        "thoughts": "The way things are is the way things must be. Progress is real. We are at the top.",
        "thinking": "Linear, hierarchical, separability-based. Often confuses one civilizational arrangement for the only possible arrangement.",
        "perception": "Filters out what is not legible to its categories. Indigenous knowledge, the more-than-human, deep time — these become invisible.",
        "sensing": "Often disconnected from sensing. The body is treated as a vehicle for the mind, not as a knower in its own right.",
        "context": "You were born inside a five-hundred-year-old project. Most of what you call common sense is its furniture. The project is in trouble.",
        "mystery": "Other ways of being human have always existed and continue to exist. Modernity is one cosmology. The world is older and stranger than this passenger has been allowed to imagine.",
        "where_isnt_enough": "Reading widely outside your own tradition. Indigenous teachers in their own communities. The CC-licensed GTDF GCE Otherwise booklet. Bayo Akomolafe's essays. This card is a doorway, not a teaching.",
        "lineage": "Synthesized from the GTDF Global Citizenship Education Otherwise booklet (CC-BY 4.0, Andreotti et al.) and *Hospicing Modernity* (Andreotti 2021). PlayfulProcess's paraphrased framing; not direct quotation.",
    },
    {
        "id": "denial-passenger", "name": "The Denial Passenger", "tier": 4, "shape": "shield", "color": "#7E8A9F",
        "tagline": "The one who keeps the news at the door.",
        "thoughts": "It's not that bad. Someone will fix it. Don't make me look at this.",
        "thinking": "Filtering, downscaling, redirecting. Genuine work — denial is labor, even when it feels like nothing.",
        "perception": "Edits the field of awareness in real time. Things that would unsettle the day quietly disappear.",
        "sensing": "A held quality. A breath that doesn't fully come. Sometimes a numbness whose origin you can't locate.",
        "context": "There are real things — climate, complicity, systemic harm, the news of the day — that the body does not know how to metabolize at the rate they arrive. Denial is not stupid; it is exhausted.",
        "mystery": "The capacity to look at something hard without collapsing is a skill, and skills are learned slowly. The denial passenger is buying time. That time is worth something. It is not worth everything.",
        "where_isnt_enough": "Denial that prevents you from acting at all when action would matter is past this scaffold. Community, practice, slow work with people who are already doing this — that's the path.",
        "lineage": "GTDF 'four denials' framework (decolonialfutures.net/4denials/). Synthesized in PlayfulProcess's voice; refers to but does not reproduce GTDF text.",
    },
    {
        "id": "ancestral-passenger", "name": "The Ancestral Passenger", "tier": 4, "shape": "rootsystem", "color": "#7E5C3C",
        "tagline": "The one carrying what was passed without words.",
        "thoughts": "Often few articulated thoughts. More like a feeling-tone or a sudden gesture: 'this is how my grandmother held a knife.'",
        "thinking": "Pre-verbal, somatic, inherited across generations. Patterns of fear, joy, belonging, and grief that came with the bloodline.",
        "perception": "Sometimes sees through the eyes of people you never met. Sometimes notices what kept your line alive.",
        "sensing": "Old gestures. Familiar postures. A song you didn't learn that you somehow know.",
        "context": "You are not the start of your line. The body you live in carries unfinished material from people who could not finish it themselves.",
        "mystery": "Many traditions consider this passenger central, not peripheral. The dead are not gone in the way modernity says they are. What gets passed forward is not always chosen, and what gets healed travels both directions.",
        "where_isnt_enough": "Ancestral work is not a solo journaling task. Specific lineages do this work specifically — talk to teachers in traditions you have a real relationship with, not in ones you don't.",
        "lineage": "Pan-traditional concept; framed here in conversation with Andreotti's discussions of intergenerational inheritance and Bayo Akomolafe's essays on lineage. PlayfulProcess's synthesis.",
    },
    {
        "id": "wounded-inheritance", "name": "The Wounded Inheritance", "tier": 4, "shape": "knot", "color": "#6E3F4F",
        "tagline": "The one carrying what the system did and did not name.",
        "thoughts": "I shouldn't have to feel this. It was so long ago. Why is this still here.",
        "thinking": "Cycling through patterns the conscious mind didn't choose. Often arriving as the family pattern repeating, even when you swore you wouldn't.",
        "perception": "Filters for the original wound's signal everywhere — in love, in work, in stranger-interactions.",
        "sensing": "A specific quality of bracing the body learned before you remember learning it.",
        "context": "Something happened to you, or to people who came before you, that the community at the time could not metabolize. It got passed down. The fact that it is in you does not mean it is yours to keep.",
        "mystery": "Traditions across the world have rituals for this — for the wounds that travel. Most modern environments stripped those rituals away. The passenger is asking for what those rituals used to provide.",
        "where_isnt_enough": "This is therapeutic territory, not journaling territory. Somatic experiencing, IFS-trained therapists, ancestral healing practitioners, EMDR — the modalities exist. Use them.",
        "lineage": "Synthesized from Andreotti & Ahenakew's *Towards Scarring Our Collective Soul Wound* (CC-licensed); also draws on Resmaa Menakem's *My Grandmother's Hands*, Cash Ahenakew's academic work, and the broader trauma-and-lineage literature.",
    },
    {
        "id": "carriage-driver", "name": "The Carriage Driver", "tier": 4, "shape": "anchor", "color": "#3F5C7C",
        "tagline": "The question, not the person.",
        "thoughts": "Who is driving right now. Whose voice is this. What is this part of me actually responding to.",
        "thinking": "A meta-question, not a passenger. The capacity to notice which passenger is at the wheel without assuming you are them.",
        "perception": "Steps back. Holds the bus rather than identifying with one seat.",
        "sensing": "A widening. Breath returns. The body remembers it is bigger than any one voice in it.",
        "context": "There is no permanent driver. There is only the practice of asking, in any moment, who is driving — and whether that is the one you would have chosen if you had been awake.",
        "mystery": "This question is older than most of the frameworks pointing at it. It echoes the witness in many contemplative traditions. The question is more durable than any answer to it.",
        "where_isnt_enough": "The question alone doesn't change the bus. What changes the bus is what you do once you've asked it — and that work usually involves people, not just reflection.",
        "lineage": "Andreotti's 'who is driving' question, drawn from her work with Indigenous teachers (Ninawa Huni Kui, Pitaguary family) as articulated in *Hospicing Modernity* (2021) and the GTDF GCE Otherwise booklet (CC-BY). Framed here in conversation with ACT's bus metaphor (Hayes 1999) and IFS's Self.",
    },
    {
        "id": "baby-mountain", "name": "The Baby Mountain", "tier": 4, "shape": "mountain", "color": "#C99B6E",
        "tagline": "The one who needs to be soothed before any other work happens.",
        "thoughts": "I'm scared. I don't want to. Make it stop. I want to be held.",
        "thinking": "Often pre-verbal. Reactive rather than reflective.",
        "perception": "Filters toward whoever might soothe or threaten. Time horizon is now.",
        "sensing": "A small body in a big body. Sometimes literal: curled up, holding stomach, wanting blanket.",
        "context": "Some of your responses are coming from a much younger part of you that didn't get what it needed at the time. That part is not stupid; it is the right age for the help it didn't get.",
        "mystery": "Every adult contains every child they ever were. Most cultures throughout history have known this. Modernity is unusual in pretending it is not so.",
        "where_isnt_enough": "Working with this part directly without a skilled practitioner can re-wound rather than heal. A trauma-informed therapist is the right container.",
        "lineage": "Synthesized from the 'four mountains' framework in *Hospicing Modernity* (Andreotti 2021), in dialogue with IFS exile work and Hakomi child-consciousness. PlayfulProcess's framing.",
    },
    {
        "id": "warrior-mountain", "name": "The Warrior Mountain", "tier": 4, "shape": "triangle", "color": "#A04F3F",
        "tagline": "The one who fights because that's what kept them alive.",
        "thoughts": "I have to fight this. Someone has to. If I don't, who will.",
        "thinking": "Mobilizing, oppositional, righteous. Often correctly identifying real harm and incorrectly assuming the only response is fight.",
        "perception": "Sharp toward enemies; can lose sight of allies and complexity.",
        "sensing": "A bracing, a forward lean, energy in the hands.",
        "context": "There are real things worth fighting for. The warrior is not a pathology. The warrior also gets tired and sometimes confuses every problem for the same problem.",
        "mystery": "Something in you knew, very early, that nobody was coming to fight for you. The warrior took the job. That was an act of love, even though it cost something.",
        "where_isnt_enough": "Sustained activist work without rest produces specific damage. Movement elders, somatic practices for activists, communities that organize sustainability into the work — these are not optional.",
        "lineage": "Synthesized from the 'four mountains' framework in *Hospicing Modernity* (Andreotti 2021), in dialogue with adrienne maree brown's *Holding Change* and Bayo Akomolafe's postactivism. PlayfulProcess's framing.",
    },
    {
        "id": "provider-mountain", "name": "The Provider Mountain", "tier": 4, "shape": "tree", "color": "#5C7C4F",
        "tagline": "The one who keeps everyone fed.",
        "thoughts": "I can do that. I'll handle it. Don't worry about me.",
        "thinking": "Service-oriented, often anticipatory. Frequently resentful underneath, even when generous on the surface.",
        "perception": "Sees needs everywhere. Often misses own.",
        "sensing": "A tiredness that doesn't go away with sleep. A back that aches.",
        "context": "Providing is real labor and the people around you are genuinely fed. The provider is not making it up. It is mistaken about whether anyone else is allowed to provide for it.",
        "mystery": "The provider often comes from a place where being useful was the price of belonging. That price is not the only currency. Some people will love you for your presence, not your output. Most will not say so.",
        "where_isnt_enough": "When the provider runs the family, the workplace, the friend group, and there is no remaining thread that is just for you — therapy and a real change in some external structure, not just reflection.",
        "lineage": "Synthesized from the 'four mountains' framework in *Hospicing Modernity* (Andreotti 2021), in dialogue with Tricia Hersey's Rest is Resistance, Audre Lorde on caretaking, and the burnout literature. PlayfulProcess's framing.",
    },
    {
        "id": "elder-mountain", "name": "The Elder Mountain", "tier": 4, "shape": "ouroboros", "color": "#7E5C8B",
        "tagline": "The one who has been here long enough to know the seasons.",
        "thoughts": "This too. We've been here before. It will pass. It will return.",
        "thinking": "Cyclical, patient, less invested in outcomes. Often quiet for long stretches.",
        "perception": "Sees the long arc. Notices what is recurring vs. what is genuinely new.",
        "sensing": "A settledness. An unhurried breath. The body okay with not knowing.",
        "context": "Some part of you is older than the part that's panicking. It has been here before. Its slowness is not laziness; it is what comes after enough seasons.",
        "mystery": "Most traditions have said that elders are not the same as old people. Eldering is a capacity. It can show up at twenty in some lives and not at all in others. It listens to the part of you that has always known.",
        "where_isnt_enough": "If you have not had real elders in your life — people older than you who have walked the path — this passenger is harder to access. Find them. Sit with them. The internet is not enough.",
        "lineage": "Synthesized from the 'four mountains' framework in *Hospicing Modernity* (Andreotti 2021), in dialogue with Stephen Jenkinson's *Come of Age*, Malidoma Somé's writings on the village, and Indigenous elder teachings broadly. PlayfulProcess's framing.",
    },
    {
        "id": "more-than-human", "name": "The More-Than-Human Passenger", "tier": 4, "shape": "weave", "color": "#3F8A6E",
        "tagline": "The one who reminds you that you are made of relationships you didn't choose.",
        "thoughts": "Often few. Sometimes a sudden awareness: 'a tree was here before me.' 'this air was a leaf last year.'",
        "thinking": "Relational, ecological, interspecies. Often arrives as a sudden re-orientation rather than a reasoned position.",
        "perception": "Wider field. Notices what isn't human. Notices what doesn't speak in human language.",
        "sensing": "Often a sudden grounding. The feet remembering the ground. The breath remembering the trees.",
        "context": "You are not separate from the rest of the living world; modernity told you that you were. Most other cosmologies have known otherwise.",
        "mystery": "The web is older than your name for it. Indigenous traditions have been pointing at it for thousands of years. Modernity is a recent and partial set of eyes.",
        "where_isnt_enough": "Reading is a doorway, not a relationship. Time outside, a garden you tend, a watershed you learn the name of, an Indigenous teacher in their own community whose work you have permission to support — these are the ground.",
        "lineage": "Drawn from the GTDF 'house of modernity' / 'hummingbird' / 'multi-layered selves' essays (decolonialfutures.net, CC-licensed), Robin Wall Kimmerer's *Braiding Sweetgrass*, Bayo Akomolafe's essays. PlayfulProcess's synthesis.",
    },
]


# ----------------------------------------------------------------------
# Build the grammar.json
# ----------------------------------------------------------------------

TIER_NAMES = {
    1: "Familiar emotions (Pixar / Ekman / Damour)",
    2: "Parts-work passengers (parts-work tradition)",
    3: "Inner selves (Voice Dialogue, Stones)",
    4: "Decolonial passengers (GTDF & Andreotti, synthesized)",
}


def passenger_to_item(p, idx):
    """Convert a passenger dict into a recursive.eco grammar item."""
    sections = {
        "About": p["tagline"],
    }
    for label, _description in LAYERS:
        key = p[label.lower()]
        sections[label] = key
    sections["Where this isn't enough"] = p["where_isnt_enough"]
    sections["Lineage"] = p["lineage"]

    return {
        "id": p["id"],
        "name": p["name"],
        "level": 1,
        "sort_order": idx,
        "category": f"tier-{p['tier']}",
        "subcategory": TIER_NAMES[p["tier"]],
        "image_url": f"icons/{p['id']}.svg",
        "keywords": [p["name"].lower()],
        "metadata": {
            "tier": p["tier"],
            "tier_name": TIER_NAMES[p["tier"]],
            "tagline": p["tagline"],
            "shape": p["shape"],
            "color": p["color"],
        },
        "sections": sections,
        "questions": [],
        "grammar_type": "custom",
    }


def make_tier_emergence_items(passengers):
    """L2 emergence items: one per tier, grouping its child passengers."""
    out = []
    for tier in (1, 2, 3, 4):
        children = [p for p in passengers if p["tier"] == tier]
        if not children:
            continue
        composite = [p["id"] for p in children]
        out.append({
            "id": f"tier-{tier}",
            "name": TIER_NAMES[tier],
            "level": 2,
            "sort_order": 100 + tier,
            "category": "tier",
            "composite_of": composite,
            "relationship_type": "emergence",
            "image_url": "",
            "keywords": [],
            "metadata": {"tier": tier},
            "sections": {
                "About this tier": _tier_description(tier),
                "How to use it": _tier_how_to(tier),
            },
            "questions": [],
            "grammar_type": "custom",
        })
    return out


def _tier_description(tier):
    return {
        1: "The familiar Pixar/Inside Out emotions, drawn from the Ekman-Keltner research lineage. Culturally fluent — most users already know these archetypes intuitively. They make a low-friction intake layer for noticing what's moving.",
        2: "Generic parts-work passengers — Manager, Firefighter, Exile, Self-energy, Inner Critic. Common-language framing of insights from Internal Family Systems (Schwartz). 'IFS' is trademarked; this tier uses generic parts framing only.",
        3: "Voice Dialogue passengers (Hal & Sidra Stone). Voice Dialogue is explicitly not trademarked. Pusher, Pleaser, Rule Maker, Vulnerable Self, Aware Ego — these are the inner selves most people meet first when they begin parts work.",
        4: "Decolonial passengers, synthesized from the CC-licensed GTDF GCE Otherwise booklet, *Hospicing Modernity*, *Towards Braiding*, *Towards Scarring*, and Andreotti's open academic papers. Goes beyond intrapsychic parts to passengers carrying inherited material — modernity itself, ancestral patterns, the more-than-human web. Permission letter to Vanessa Andreotti pending; this synthesis is in PlayfulProcess's own paraphrased voice.",
    }[tier]


def _tier_how_to(tier):
    return {
        1: "Start here if a familiar emotion is loud. Move to Tier 2 or 3 if 'who keeps making this feeling' becomes the more interesting question.",
        2: "Use these when the emotional response feels structural — a part of you that always shows up under certain conditions, with a job and a history. If exile-level material arises, stop solo work and find a parts-work-trained therapist.",
        3: "Use these when you can name the inner voice but not the emotion underneath. Voice Dialogue's gift is making the voices addressable.",
        4: "Use these when the question is wider than your individual psychology — when you're noticing patterns that came with the bloodline, the land, the language, the system. These cards point outward as much as inward; the off-ramps matter more here than in other tiers.",
    }[tier]


def make_grammar(passengers):
    items = [passenger_to_item(p, i) for i, p in enumerate(passengers)]
    items.extend(make_tier_emergence_items(passengers))

    return {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "PlayfulProcess",
                    "date": "2026-05-05",
                    "note": "Original synthesis. Tier 4 cards draw on the CC-BY GTDF Global Citizenship Education Otherwise booklet and *Hospicing Modernity* (Andreotti 2021) in PlayfulProcess's paraphrased voice; permission letter to Vanessa Machado de Oliveira / Andreotti pending. Tier 1: Pixar/Ekman/Damour (public domain emotion archetypes). Tier 2: generic parts-work language inspired by Internal Family Systems (Schwartz; trademark belongs to IFS Institute). Tier 3: Voice Dialogue (Hal & Sidra Stone; explicitly not trademarked).",
                }
            ],
        },
        "name": "Bus Passengers",
        "description": (
            "A contemplative parts-work and decolonial cartography for noticing "
            "which voice is driving when you make a values-laden decision.\n\n"
            "Each passenger card has six layered sections, descending from the "
            "articulated voice toward the more-than-human web: Thoughts → "
            "Thinking → Perception → Sensing → Context → Mystery. The user starts "
            "where they always start (with what the passenger says) and the "
            "session is a slow walk toward what was always here, before language "
            "got hold of it.\n\n"
            "Inspired by a passage in Andreotti's *Outgrowing Modernity* on the "
            "layered nature of awareness — that what we articulate is a small "
            "fraction of what we think, what we think is a fragment of what we "
            "perceive, and so on down toward the dynamic universe we are part of.\n\n"
            "Four tiers of passengers: familiar Pixar emotions (Tier 1), "
            "parts-work passengers (Tier 2), Voice Dialogue inner selves (Tier 3), "
            "and decolonial passengers carrying inherited material — modernity, "
            "ancestral patterns, the more-than-human web (Tier 4). The bus "
            "metaphor itself is in the public domain (Hayes' ACT, 1999).\n\n"
            "This grammar is scaffolding, not teaching. Each card has a 'where "
            "this isn't enough' section that points outward to community, "
            "therapy, books, embodied practice — the AI chat is a thin "
            "reflection layer, not a substitute for any of those things."
        ),
        "creator_name": "PlayfulProcess",
        "grammar_type": "custom",
        "tags": [
            "parts-work", "ifs", "voice-dialogue", "act", "bus-metaphor",
            "decolonial", "andreotti", "gtdf", "hospicing-modernity",
            "contemplative", "layered-awareness",
        ],
        "roots": ["western-philosophy", "indigenous-knowledge", "eastern-wisdom"],
        "shelves": ["wisdom", "mirror"],
        "lineages": ["Andreotti", "Akomolafe", "Linehan"],
        "worldview": "decolonial",
        "items": items,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    # Generate SVG icons
    for p in PASSENGERS:
        shape_fn = SHAPES.get(p["shape"], SHAPES["circle"])
        svg = shape_fn(p["color"])
        (ICONS_DIR / f"{p['id']}.svg").write_text(svg, encoding="utf-8")

    grammar = make_grammar(PASSENGERS)
    out_file = OUT_DIR / "grammar.json"
    out_file.write_text(json.dumps(grammar, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")
    print(f"  L1 passengers: {len(PASSENGERS)}")
    print(f"  L2 tier emergences: 4")
    print(f"  Total items: {len(PASSENGERS) + 4}")
    print(f"  SVG icons: {len(PASSENGERS)} in {ICONS_DIR}")


if __name__ == "__main__":
    main()
