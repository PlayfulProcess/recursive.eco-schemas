# Library Plan: 100 Books → Curated Grammars

**Date:** 2026-03-04
**Status:** Active — this is how we build the library

---

## What This Is

A pipeline to transform 100 public domain texts from Project Gutenberg into **opinionated, curated grammars** for recursive.eco. Not neutral summaries. Not AI slop. Each grammar carries an editorial stance rooted in DBT (adaptive vs. maladaptive), decolonial awareness, and the specific intellectual lineages we serve.

**The editorial stance IS the product.**

---

## Pipeline: Source Text → Grammar JSON

```
1. DOWNLOAD     Plain text from Gutenberg (done — see sources/)
2. CHUNK        Split into chapters/sections/natural units
3. CLASSIFY     AI-assisted tagging with human review
4. CURATE       Write reflection questions, lineage notes, shelf placement
5. BUILD        Generate grammar JSON (items = chapters, sections = metadata)
6. REVIEW       Human spot-check for colonial flags, misclassification
7. PUBLISH      Push to R2 + index in Supabase + mirror to GitHub
```

---

## Step 1: Download (This Commit)

All 100 source texts downloaded as plain text into `library/sources/` organized by root:

```
library/sources/
├── root-01-eastern-wisdom/         # 14 books
├── root-02-african-cosmology/      # 10 books
├── root-03-indigenous-mythology/   # 16 books
├── root-04-mysticism/              # 10 books
├── root-05-process-emergence/      # 12 books
├── root-06-emotion-love/           # 9 books
├── root-07-freedom-commons/        # 8 books
├── root-08-wonder-children/        # 14 books
├── root-09-ecology-nature/         # 5 books
└── root-10-self-knowledge/         # 2 books
```

---

## Step 2: Chunking Strategy

Each book gets split into natural units that become grammar **items**:

| Book Type | Chunk Unit | Example |
|-----------|-----------|---------|
| Philosophy | Chapter/section | Tao Te Ching → 81 verses as items |
| Poetry | Individual poem | Gitanjali → each poem is an item |
| Folklore | Individual story/tale | Grimm's → each tale is an item |
| Novel | Chapter | Alice → each chapter is an item |
| Sacred text | Sutra/verse group | Dhammapada → verse groupings as items |
| Essays | Individual essay | Emerson → each essay is an item |

**Rule:** Each item should be a self-contained unit of meaning that can be drawn in a reading. If someone asks the oracle "what do I need to hear today?" — the item should be a complete answer.

---

## Step 3: Classification (The Opinionated Part)

Every item gets tagged with this schema:

```json
{
  "adaptive_patterns": [],
  "maladaptive_patterns": [],
  "colonial_flags": [],
  "worldview": "",
  "lineages": [],
  "themes": [],
  "suitable_for_children": false,
  "needs_contextualization": false,
  "contextualization_note": ""
}
```

### What "Adaptive" Means Here

Using Marsha Linehan's DBT framework:

**Adaptive** = helps people build lives worth living
- Radical acceptance of reality as it is
- Distress tolerance without destructive action
- Emotional regulation through awareness
- Interpersonal effectiveness
- Mindfulness (present-moment, non-judgmental)
- Both-and thinking (dialectics)
- Connection to something larger (spiritual but not dogmatic)

**Maladaptive** = normalizes patterns that cause suffering
- Domination as natural order
- Emotional suppression as strength
- Hierarchy of human worth (racial, gender, class)
- "Might makes right" logic
- Denial of interdependence
- Binary thinking (either/or, us/them)

### Classification Examples

**Tao Te Ching, Verse 8 ("The highest good is like water")**
```json
{
  "adaptive_patterns": ["radical acceptance", "non-striving", "yielding as strength"],
  "maladaptive_patterns": [],
  "worldview": "non-dual",
  "lineages": ["Linehan", "Akomolafe"],
  "themes": ["water", "yielding", "humility", "naturalness"]
}
```

**Just So Stories, "How the Leopard Got His Spots"**
```json
{
  "adaptive_patterns": ["wonder", "imagination", "playfulness"],
  "maladaptive_patterns": ["racial essentialism in imagery"],
  "colonial_flags": ["Kipling's colonial gaze on African characters"],
  "worldview": "colonial-imaginative",
  "lineages": [],
  "themes": ["transformation", "adaptation", "nature"],
  "suitable_for_children": true,
  "needs_contextualization": true,
  "contextualization_note": "Kipling wrote from within the British Empire. His animal stories carry wonder AND a colonial gaze on non-white peoples. Both are true. Read with awareness."
}
```

**Critique of Pure Reason, Preface**
```json
{
  "adaptive_patterns": ["critical thinking", "epistemic humility"],
  "maladaptive_patterns": ["reason-supremacy", "universalism as European projection"],
  "colonial_flags": ["Kant's racial hierarchy writings inform his 'universal' reason"],
  "worldview": "rationalist",
  "lineages": ["Andreotti (contested)"],
  "themes": ["knowledge", "limits of reason", "metaphysics"],
  "needs_contextualization": true,
  "contextualization_note": "Kant simultaneously founded critical philosophy AND wrote that non-white peoples were incapable of reason. His 'universal' categories are European categories presented as universal. The insight is real; the framing is colonial. Both-and."
}
```

---

## Step 4: Curation — What Makes This Different From AI Slop

For each grammar, a human (or carefully prompted AI with human review) writes:

### Reflection Questions (per chapter/item)
Not comprehension questions. Not study guide questions. **Therapeutic** questions:

- "Where in your body do you feel this text landing?"
- "What would radical acceptance of this truth change in your life today?"
- "Who in your lineage carried this wisdom? What happened to it?"
- "What does this text ask you to let go of?"

### Lineage Notes (per grammar)
A short essay connecting this old text to its modern emergence:

> *The Dhammapada is not a historical artifact. It is the root system under Marsha Linehan's DBT — she studied Zen at Shasta Abbey, and the mindfulness skills she built into her treatment for borderline personality disorder are these verses, translated into clinical language. When you read "All that we are is the result of what we have thought," you are reading the first cognitive-behavioral insight, 2,500 years before Aaron Beck.*

### Shelf Placement + Rationale
Why this book is on this shelf, not just what shelf it's on.

### Adaptive Priority Score (1-5)
For RAG and search: how strongly should this text surface when someone asks for wisdom?

- **5** = Core adaptive text (Tao Te Ching, Dhammapada, Walden)
- **4** = Strongly adaptive with some complexity (Meditations, Julian of Norwich)
- **3** = Mixed — adaptive AND maladaptive (Emma, Golden Bough)
- **2** = Important but heavily contested (Kant, Nietzsche, Communist Manifesto)
- **1** = Primarily here for historical completeness or children's entertainment value

---

## Step 5: Grammar JSON Structure

Each book becomes a grammar JSON following the recursive.eco schema:

```json
{
  "name": "Tao Te Ching",
  "type": "book",
  "description": "81 verses on the way of water, emptiness, and non-doing. Root text for Zen, DBT's radical acceptance, and Akomolafe's philosophy of cracks.",
  "creator": "Lao Tzu (6th century BCE) — translated by James Legge",
  "source": "Project Gutenberg #216",
  "license": "Public Domain",
  "shelf": "wisdom",
  "adaptive_priority": 5,
  "lineages": ["Linehan", "Akomolafe", "Shrei"],
  "worldview": "non-dual",
  "gutenberg_id": 216,
  "items": [
    {
      "id": "verse-01",
      "name": "The Tao that can be told",
      "category": "verse",
      "sections": {
        "text": "The Tao that can be told is not the eternal Tao...",
        "reflection": "What in your life cannot be named but you know is real?",
        "lineage_note": "This is the root of apophatic theology, Zen's 'finger pointing at the moon,' and Akomolafe's 'the cracks are the path.'",
        "adaptive_patterns": ["epistemic humility", "non-attachment to concepts"],
        "themes": ["naming", "mystery", "origin"]
      }
    }
  ],
  "metadata": {
    "total_items": 81,
    "classification": {
      "adaptive_patterns": ["radical acceptance", "non-striving", "dialectics"],
      "maladaptive_patterns": [],
      "colonial_flags": [],
      "needs_contextualization": false
    }
  }
}
```

---

## Step 6: Build Order (Priority)

### Batch 1: Core Texts (Build First — 20 books)
These are the most important for recursive.eco's identity:

1. Tao Te Ching (#216)
2. Dhammapada (#17566)
3. I Ching (#14838) — already exists as grammar!
4. Bhagavad Gita (#2388)
5. Alice's Adventures in Wonderland (#11)
6. Folk Stories from Southern Nigeria (#34655)
7. Meditations — Marcus Aurelius (#2680)
8. Walden (#205)
9. Songs of Kabir (#6519)
10. Mutual Aid — Kropotkin (#4341)
11. The Souls of Black Folk (#408)
12. Cloud of Unknowing (#20508)
13. Grimm's Fairy Tales (#2591)
14. The Popol Vuh (#56550)
15. Leaves of Grass (#1322)
16. The Prophet (#58585)
17. Julian of Norwich (#52958)
18. Peter Pan (#16)
19. Civil Disobedience (#71)
20. The Book of Tea (#769)

### Batch 2: Second Ring (30 books)
Expand each root with its next-most-important texts.

### Batch 3: Full Library (50 books)
Complete all 100 + add Two Bits (CC-licensed).

---

## Prompting Strategy for AI-Assisted Classification

When using Claude to classify chapters:

```
You are classifying chapters of {book_title} for recursive.eco, a meaning-making library.

Your editorial stance:
- ADAPTIVE patterns help people build lives worth living (Linehan's DBT framework)
- MALADAPTIVE patterns normalize domination, suppression, or hierarchy of human worth
- COLONIAL FLAGS mark content that carries colonial, white-supremacist, or empire-serving framing
- Both-and: a text can carry adaptive wisdom AND colonial harm simultaneously
- The goal is NOT censorship — it's contextualization

For this chapter, provide:
1. adaptive_patterns: [] — what this teaches that helps
2. maladaptive_patterns: [] — what this normalizes that harms
3. colonial_flags: [] — specific colonial content (empty if none)
4. worldview: "" — animist, rationalist, devotional, dialectical, imperial, etc.
5. themes: [] — searchable keywords
6. reflection_question: "" — a therapeutic question (not a study question)
7. suitable_for_children: true/false
8. needs_contextualization: true/false
9. contextualization_note: "" — if needed, why

Remember: you are not being neutral. You are being honest. Adaptive > maladaptive in search ranking. Colonial content is flagged, not censored.
```

---

## What Success Looks Like

A user opens recursive.eco and asks their AI: "I'm going through a dark night — what should I read?"

The RAG searches grammars tagged with `adaptive_patterns: ["crisis as transformation", "radical acceptance"]` and returns:

1. **Dark Night of the Soul** by St. John of the Cross — "The darkness is not punishment. It is the soul outgrowing its container."
2. **Revelations of Divine Love** by Julian of Norwich — "All shall be well, and all shall be well, and all manner of thing shall be well."
3. **Tao Te Ching, Verse 76** — "The stiff and unbending is the disciple of death. The soft and yielding is the disciple of life."

Not a Wikipedia summary. Not an AI-generated platitude. The actual words of people who walked through the fire, structured for retrieval, prioritized for healing.

That's the library.
