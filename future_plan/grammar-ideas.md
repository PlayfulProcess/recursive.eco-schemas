# Grammar Ideas & Future Capabilities

> **Active build plans**: See [`greek-mythology-plan.md`](greek-mythology-plan.md) for the step-by-step execution plan for the Greek Mythology grammars.

## 1. Multi-Level Scene Breakdown (Implemented: Alice in Wonderland)

### What We Did
Transformed the Alice in Wonderland grammar from 12 flat chapter items into a **two-level hierarchy**:

- **Level 2 (Chapters)** — Emergent items with `composite_of` pointing to their scenes. Carry chapter-level summaries: "For Littlest Readers" (3-year-old), "For Young Readers" (8-year-old), "Characters You'll Meet", "Famous Lines", "Things to Talk About".
- **Level 1 (Scenes)** — 47 scene items carrying the **complete original text** plus age-adapted retellings ("For Young Readers", "What Happens").

### Age-Adapted Rendering Idea
The level structure enables **different reading experiences from the same grammar**:

| Audience | What to Render | Source |
|----------|---------------|--------|
| 3-year-olds | Chapter "For Littlest Readers" summaries | Level 2 emergent items |
| 5-8-year-olds | Scene "For Young Readers" retellings | Level 1 items, "For Young Readers" section |
| 8+ / adults | Original text, scene by scene | Level 1 items, "Story (Original Text)" section |

A future renderer could pick which section to display based on a "reading level" toggle.

---

## 2. Greek Mythology Grammar — Family Tree + Myths

### Core Concept
Two (or three) **connected grammars** that cross-reference each other:

#### Grammar A: The Family Tree (Theogony)
A grammar of **divine figures** organized by generation:

| Level | Category | Examples |
|-------|----------|----------|
| L3 | Generation | Primordials, Titans, Olympians, Heroes |
| L2 | Family Branch | House of Atreus, Theban Cycle, Argonauts |
| L1 | Individual | Zeus, Hera, Athena, Heracles, Odysseus |

Each L1 item would include:
- **sections**: "Profile", "Domains & Epithets", "Symbols & Sacred Animals", "Key Relationships", "Character"
- **metadata**: `{ "generation": "olympian", "domain": "sky", "roman_name": "Jupiter", "parents": ["kronos", "rhea"] }`
- **keywords**: mythic themes (hubris, metamorphosis, xenia, fate)

#### Grammar B: The Myths
A grammar of **stories**, each a narrative unit:

| Level | Category | Examples |
|-------|----------|----------|
| L2 | Cycle / Theme | Trojan War, Labors of Heracles, Metamorphoses, Underworld |
| L1 | Individual Myth | Prometheus Steals Fire, Judgment of Paris, Orpheus & Eurydice |

Each L1 myth item would include:
- **sections**: "The Story", "For Young Readers", "Moral / Theme", "Connections"
- **metadata**: `{ "cycle": "trojan-war", "characters": ["paris", "aphrodite", "hera", "athena"] }`

#### Grammar C (Optional): Cosmic Themes
Emergent themes that span multiple myths:

| L2 Theme | Composed Of (myths) |
|----------|-------------------|
| Hubris & Nemesis | Arachne, Icarus, Niobe, Ajax |
| Metamorphosis | Daphne, Narcissus, Actaeon, Io |
| The Underworld Journey | Orpheus, Heracles L12, Odysseus, Persephone |
| Divine Justice | Prometheus, Sisyphus, Tantalus |

### Deep Linking Between Grammars
This is the key feature request. Currently `composite_of` only references items **within** the same grammar. To link across grammars we'd need either:

**Option A: URI-style IDs in composite_of**
```json
{
  "id": "prometheus-steals-fire",
  "composite_of": [
    "grammar://greek-family-tree/prometheus",
    "grammar://greek-family-tree/zeus",
    "grammar://cosmic-themes/hubris-and-nemesis"
  ]
}
```

**Option B: A `connected_items` field**
```json
{
  "id": "prometheus-steals-fire",
  "connected_items": [
    { "grammar_id": "greek-family-tree", "item_id": "prometheus", "relationship": "protagonist" },
    { "grammar_id": "greek-family-tree", "item_id": "zeus", "relationship": "antagonist" },
    { "grammar_id": "cosmic-themes", "item_id": "hubris-and-nemesis", "relationship": "theme" }
  ]
}
```

**Option C: App-level deep link URLs**
If the app already supports deep linking (e.g., `recursive://grammar/{id}/item/{item_id}`), store these as metadata:
```json
{
  "metadata": {
    "related_characters": ["greek-family-tree:prometheus", "greek-family-tree:zeus"],
    "related_themes": ["cosmic-themes:hubris-and-nemesis"]
  }
}
```

The app would parse these and render them as tappable links.

---

## 3. Prompting Strategy for Source Text Grammars

### How to break any public domain text into a grammar using multiple Claude chats:

#### Pipeline Approach
1. **Chat 1 — Structure Extraction**
   - Input: 1-2 chapters of source text
   - Prompt: "Break this into natural scenes/episodes. For each: give an id, name, the start/end text markers, and a one-sentence summary."
   - Output: Scene list with boundaries

2. **Chat 2 — Age-Adapted Retelling**
   - Input: Scenes from Chat 1
   - Prompt: "For each scene, write: (a) a 2-3 sentence version for a 3-year-old, (b) a paragraph for an 8-year-old preserving key dialogue and wonder."
   - Output: Retellings per scene

3. **Chat 3 — Grammar Assembly**
   - Input: Schema reference + scenes + retellings
   - Prompt: "Assemble these into a valid grammar.json following this schema. Level 1 = scenes (with original text + retellings), Level 2 = chapters (emergent, composed of scenes)."
   - Output: grammar.json

#### Single-Chat Approach (for shorter texts)
For texts under ~30K words, a single chat can handle the entire pipeline:
- Paste the full text + schema
- Ask for scene breakdown + retellings + grammar assembly
- Review and iterate

#### Tips
- **Always verify text integrity**: the original text should be 100% preserved across scene splits
- **Use distinctive opening phrases** as scene boundary markers, not paragraph numbers (which can shift)
- **Feed 1-2 chapters at a time** for long works to stay within context limits
- **Validate JSON** after assembly: check unique IDs, composite_of references, and that grammar_type matches

---

## 4. Grammars Writable from Training Knowledge

These grammars can be written by Claude without any source text, purely from training knowledge:

### Mythological / Religious
| Grammar | Est. Items | Structure | Notes |
|---------|-----------|-----------|-------|
| **Greek Mythology** | 80-120 | Family tree + myths + themes | See Section 2 above |
| **Norse Mythology** | 40-60 | Nine Worlds → Aesir/Vanir → Ragnarok | Creation to destruction arc |
| **Egyptian Mythology** | 40-50 | Ennead → Osiris Cycle → Book of the Dead | Gods + afterlife journey |
| **Hindu Epics** | 60-100 | Mahabharata (18 books) + Ramayana (7 kandas) | Episodes within books |
| **Arthurian Legend** | 30-40 | Round Table → Grail Quest → Fall of Camelot | Knights + quests |
| **Celtic Mythology** | 30-40 | Tuatha Dé Danann → Ulster Cycle → Fenian Cycle | Irish + Welsh |
| **Japanese Mythology** | 40-50 | Kojiki creation → Kami → Yokai → Folk tales | Shinto + Buddhist |
| **Chinese Mythology** | 40-60 | Pangu → Three Sovereigns → Journey to West | Creation + classic novels |
| **Mesoamerican Mythology** | 30-40 | Popol Vuh → Aztec creation → Calendar | Maya + Aztec |
| **African Mythology** | 40-50 | Anansi → Yoruba Orishas → Ubuntu stories | Pan-African folk tales |

### Literary / Philosophical
| Grammar | Est. Items | Structure | Notes |
|---------|-----------|-----------|-------|
| **Aesop's Fables** | 100+ | Fable → Moral (emergent) | Each fable is L1, morals are L2 themes |
| **Hero's Journey (Campbell)** | 17-20 | Call → Initiation → Return stages | With examples from world myth |
| **Tarot Major Arcana (Jungian)** | 22 | The Fool's Journey | Archetypes + shadow meanings |
| **Stoic Philosophy** | 30-40 | Epictetus + Marcus Aurelius + Seneca | Principles + practices |
| **Zen Koans** | 50-100 | Gateless Gate + Blue Cliff Record | Koan → commentary |
| **Sufi Stories** | 40-50 | Rumi + Nasruddin + Attar | Teaching stories |

### Scientific / Educational
| Grammar | Est. Items | Structure | Notes |
|---------|-----------|-----------|-------|
| **Periodic Table** | 118+ | Elements → groups → periods | Properties + history |
| **Constellations** | 88 | By season + hemisphere | Greek myths + star data |
| **Tree of Life** | 50-80 | Domains → Kingdoms → Key species | Taxonomy + ecology |

### Public Domain Source Texts (need source, can structure)
| Text | Est. Items | Notes |
|------|-----------|-------|
| **Through the Looking-Glass** | 50-60 scenes | Sequel to Alice — same scene-level approach |
| **The Odyssey** | 60-80 episodes | 24 books → episodes within |
| **The Iliad** | 60-80 episodes | 24 books → battle scenes + councils |
| **Grimm's Fairy Tales** | 200+ tales | Each tale is an item; themes are emergent |
| **1001 Nights** | 50-100 stories | Frame story + nested tales |
| **Tao Te Ching** | 81 chapters | Verse + interpretation per chapter |
| **Bhagavad Gita** | 18 chapters / 700 verses | Like Dhammapada approach |
| **Shakespeare Plays** | 30-40 per play | Act/Scene → speech/episode |
| **Divine Comedy** | 100 cantos | 3 canticles × 33 cantos + 1 |

---

## 5. Connected Grammars — App Architecture Ideas

### Current State
- `composite_of` links items within the same grammar
- No cross-grammar linking exists in the schema

### Proposed: Connected Grammars Feature
Allow grammars to reference items in other grammars. Use cases:

1. **Greek Family Tree** ↔ **Greek Myths**: tap a character in a myth to see their profile
2. **Alice in Wonderland** ↔ **Through the Looking-Glass**: shared characters (Alice, White Queen, etc.)
3. **Dhammapada** ↔ **Buddhist Concepts Grammar**: verses link to concept explanations
4. **Tarot** ↔ **Astrology**: astrological correspondences on each card

### Implementation Sketch
```json
// In grammar.json root:
"connected_grammars": [
  {
    "grammar_id": "greek-family-tree",
    "grammar_name": "Greek Family Tree",
    "relationship": "characters"
  }
]

// On individual items:
"deep_links": [
  {
    "target_grammar": "greek-family-tree",
    "target_item": "prometheus",
    "label": "Prometheus",
    "relationship": "character"
  }
]
```

The app would render these as tappable chips/links that navigate to the referenced item in the other grammar (if installed).

---

## 6. Rendering Modes

Building on the multi-level approach, the app could support **rendering modes**:

| Mode | What's Shown | Use Case |
|------|-------------|----------|
| **Story Mode** | Scenes in order, selected section only | Reading the story aloud |
| **Study Mode** | All sections visible, questions expanded | Educational use |
| **Oracle Mode** | Random scene or chapter, reflective prompt | Bibliomancy / contemplation |
| **Summary Mode** | Emergent items only (chapters) | Quick overview |

The grammar already contains all the data for these modes — it's purely a renderer concern.

---

## 7. Grammar Bundles

Package related grammars together:

```json
{
  "bundle_name": "Greek Mythology Collection",
  "grammars": [
    "greek-family-tree",
    "greek-myths",
    "greek-cosmic-themes"
  ],
  "cross_references": true,
  "cover_image_url": "..."
}
```

This would install all three grammars and enable deep linking between them.
