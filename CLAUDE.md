# CLAUDE.md — Project Context for recursive.eco-schemas

## What This Project Is

A public repository of **grammars** — structured JSON files that represent symbolic systems (tarot decks, philosophical texts, mythology, children's stories, etc.) for use with the Flow recursive viewer at [recursive.eco](https://recursive.eco). Each grammar is a self-contained dataset that the viewer can render as cards, readings, or explorations.

## Repository Structure

```
tarot/          — Tarot decks and card oracle systems (Rider-Waite, Jungian Archetypes, etc.)
iching/         — I Ching hexagram systems
astrology/      — Astrological schemas
classics/       — Sacred, philosophical, and classical texts (Confucius, Dhammapada, Shakespeare, Art of War, Meditations)
literature/     — Fiction (Alice in Wonderland, Winnie-the-Pooh)
mythology/      — Myths and legends (Greek Mythology, Bulfinch, death traditions)
kids/           — Children's content (Aesop, Grimm, PBS Kids, folk tales, workouts)
music/          — Music and performing arts
practice/       — Social/therapeutic practice decks
sequences/      — Ordered video/content collections
sources/        — Public domain source texts used to build grammars
future_plan/    — Build logs, pipeline, grammar ideas, principles
  build-logs/   — Per-grammar documentation of parsing strategies and learnings
```

Each category folder contains grammar subfolders (with `grammar.json`) and optionally a `schemas/` subfolder.

## Grammar JSON Format

Every `grammar.json` follows this structure:

```json
{
  "_grammar_commons": {
    "schema_version": "1.0",
    "license": "CC-BY-SA-4.0",
    "attribution": [{ "name": "...", "date": "...", "note": "..." }]
  },
  "name": "Grammar Name",
  "description": "What this grammar contains",
  "grammar_type": "custom|tarot|iching|astrology|sequence",
  "creator_name": "PlayfulProcess",
  "tags": ["tag1", "tag2"],
  "items": [...]
}
```

### Item Format

```json
{
  "id": "lowercase-hyphenated-id",
  "name": "Display Name",
  "sort_order": 0,
  "category": "grouping-key",
  "level": 1,
  "sections": {
    "SectionName": "Content text..."
  },
  "keywords": ["keyword1", "keyword2"],
  "metadata": {}
}
```

### Emergence Levels

- **L1** (level 1): Base items — individual cards, passages, fables, verses
- **L2** (level 2): Emergent combinations — chapters, acts, archetypal dynamics. Use `composite_of: ["id1", "id2"]` and `relationship_type: "emergence"`
- **L3** (level 3): Meta-categories — plays, individuation stages, macro-themes

### Grammar Types

- `tarot` — Oracle/card-draw systems (Rider-Waite, Jungian Archetypes)
- `iching` — I Ching hexagram readings
- `astrology` — Astrological interpretation
- `custom` — Everything else (texts, mythology, kids content)
- `sequence` — Ordered content (video playlists, story sequences)

## Building Grammars

### From Source Text
1. Download public domain text to `sources/`
2. Write a Python parser to extract structured content (chapters, verses, fables, etc.)
3. Output `grammar.json` into the appropriate category folder
4. Always strip commentary, footnotes, and editorial content — keep only the primary text
5. Write a build log in `future_plan/build-logs/`

### From Memory
1. Plan the taxonomy (list all items at each level) before writing content
2. Write content for each item with appropriate sections
3. Validate referential integrity (`composite_of` references must exist)

### Key Conventions
- IDs: lowercase, hyphenated, hierarchical (e.g., `book-4-17`, `hamlet-act1-scene1`)
- Sections: Use descriptive names — "Meditation", "Story", "Moral", "Verse", "Interpretation"
- For tarot-type: include "Shadow", "Light", "Questions" sections
- For kids: include "Reflection" or discussion questions
- Attribution is mandatory — include source, translator, date

## Current Grammar Inventory (37 grammars)

| Category | Count | Notable |
|----------|-------|---------|
| classics | 6 | Confucian Analects (749), Dhammapada (431), Art of War (376), Meditations (365), Shakespeare (247) |
| kids | 11 | Aesop's Fables (284), Grimm's (62), PBS Kids, folk tales |
| tarot | 6 | Rider-Waite (78), Jungian Archetypes (34) |
| mythology | 4 | Greek Mythology (102), Bulfinch, death traditions |
| iching | 3 | Chinese original (64), HD Meta-Categories |
| literature | 2 | Alice in Wonderland (59), Winnie-the-Pooh (41) |
| music | 2 | Luiza Lian, Royal Ballet |
| practice | 2 | Social Working (107) |
| sequences | 1 | Tucci in Italy |

## Parsing Lessons (from build-logs)

- **Sacred texts**: Don't assume `\n\n` splits passages. Look for speaker attributions or verse numbering.
- **Scholarly translations** (like Giles' Art of War): Use character-level bracket removal to strip commentary, not regex.
- **Roman numerals**: Use `((?:X{0,3})(?:IX|IV|V?I{0,3}))\.` pattern. Handle up to XXXIX.
- **Multi-part texts** (Grimm): Combine parts into single items.
- **Background agents**: Good for regular-structure texts under ~5000 lines. Time out on complex/commentary-heavy texts — use direct Python scripting instead.
- **Always log learnings** in `future_plan/build-logs/`.

## Pipeline (What's Next)

See `future_plan/pipeline.md` for planned grammars. Priorities include:
- From memory: Human Body, Language Family Trees, Enneagram, Periodic Table
- From source: Tao Te Ching (source exists, grammar not yet built), Zohar, Bhagavad Gita
- See `future_plan/grammar-ideas.md` for the full wishlist

## Validation Checklist

Before committing any grammar:
1. Valid JSON (`python3 -c "import json; json.load(open('grammar.json'))"`)
2. No duplicate IDs
3. All `composite_of` references point to existing item IDs
4. `sort_order` is sequential
5. All items have `id`, `name`, `sections`, `level`, `category`
6. Attribution metadata is present in `_grammar_commons`
