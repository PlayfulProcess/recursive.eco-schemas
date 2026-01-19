# Schema Types & Structure

This document explains the schema architecture used in recursive.eco-schemas.

## Schema Levels

### L1 (Base) Items

Standard grammar items that form the foundation of each system:

- **Tarot**: Individual cards (The Fool, Two of Cups, etc.)
- **I Ching**: 64 hexagrams
- **Astrology**: Planets, signs, houses, aspects

L1 items are self-contained interpretive units with their own meanings, keywords, and sections.

**Example L1 item:**
```json
{
  "id": "major-00-fool",
  "name": "The Fool",
  "category": "major",
  "keywords": ["beginnings", "innocence", "leap of faith"],
  "sections": {
    "Interpretation": "...",
    "Reversed": "..."
  }
}
```

### L2 (Emergence) Items

Higher-order items that emerge from combinations of L1 items. These represent relational meanings that arise when base elements interact.

Use `composite_of` to reference L1 item IDs:

**Example L2 item:**
```json
{
  "id": "gate-1",
  "name": "Gate of Self-Expression",
  "category": "gate",
  "composite_of": ["hexagram-01", "sign-aries"],
  "sections": {
    "Interpretation": "When the Creative hexagram meets Aries energy..."
  }
}
```

**Common L2 patterns:**
- **Human Design Gates**: I Ching hexagrams + zodiac positions
- **Composite Emotions**: Primary emotion + primary emotion (Plutchik dyads)
- **Astrological Aspects**: Planet + planet + aspect type

## File Structure

```
schemas/
├── tarot/
│   ├── rider-waite.json       # L1 deck
│   ├── etteilla-III           # L1 deck (historical)
│   └── zen-koans.json         # L1 themed deck
├── iching/
│   ├── traditional.json       # L1 hexagrams
│   └── human-design           # L1 + L2 (gates as emergences)
├── astrology/
│   ├── L1-basic               # L1 planets, signs, houses
│   └── alan-leo               # L1 interpretive layer
└── other/
    └── plutchik-wheel.json    # L1 + L2 (dyads as emergences)
```

## Schema Document Structure

Every schema file follows this top-level structure:

```json
{
  "name": "Schema Name",
  "description": "What this schema represents",
  "grammar_type": "tarot|iching|astrology|custom",
  "tags": ["searchable", "categories"],
  "creator_name": "Attribution",
  "creator_link": "https://...",
  "cover_image_url": "https://...",
  "attribution": {
    "source_name": "Original source",
    "source_url": "https://...",
    "license": "CC-BY-SA-4.0",
    "license_url": "https://..."
  },
  "items": [
    { /* L1 items */ }
  ],
  "emergences": [
    { /* L2 items with composite_of */ }
  ]
}
```

## Item Fields Reference

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier within schema |
| `name` | string | Display name |
| `keywords` | array | Interpretive keywords for search/tagging |
| `sections` | object | Named interpretation blocks |

### Common Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Unicode symbol or emoji |
| `image_url` | string | External image URL |
| `category` | string | Primary grouping (major/minor, planet/sign) |
| `subcategory` | string | Secondary grouping |
| `sort_order` | number | Display position |
| `questions` | array | Contemplative prompts |
| `composite_of` | array | L1 item IDs (for L2 items only) |
| `metadata` | object | System-specific additional data |

### Sections Object

The `sections` object contains named interpretation blocks. Common patterns:

```json
"sections": {
  "Interpretation": "Primary upright meaning",
  "Reversed": "Shadow or reversed meaning",
  "Questions": "Reflective prompts",
  "Historical Context": "Background information",
  "Etymology": "Word origins and evolution"
}
```

Section names are flexible - use whatever makes sense for your schema.

## Creating New Schemas

### 1. Choose Your Level

- **L1 only**: Standard interpretive deck/system
- **L1 + L2**: System with emergent combinations

### 2. Define Items

Start with required fields, add optional as needed:

```json
{
  "id": "unique-id",
  "name": "Display Name",
  "keywords": ["key", "concepts"],
  "sections": {
    "Interpretation": "What this means..."
  }
}
```

### 3. Add Images (Optional)

Use public domain or properly licensed images:

```json
"image_url": "https://upload.wikimedia.org/wikipedia/commons/..."
```

Preferred sources:
- Wikimedia Commons (check license)
- Google Arts & Culture (public domain works)
- Your own images (with proper licensing)

### 4. Validate JSON

Before committing:
- Validate JSON syntax (use a linter)
- Check all required fields present
- Verify image URLs resolve
- Test special characters (UTF-8 encoding)

## Best Practices

1. **Consistent IDs**: Use kebab-case (`major-00-fool`, `hex-01`)
2. **Rich Keywords**: Include synonyms and related concepts
3. **Multiple Sections**: Provide upright AND reversed/shadow meanings
4. **Questions**: Add contemplative prompts for self-inquiry
5. **Attribution**: Always credit sources and traditions
6. **Metadata**: Include creation/update dates and license

## Metadata Pattern

```json
"metadata": {
  "created": "2026-01-19",
  "last_updated": "2026-01-19",
  "license": "CC-BY-SA-4.0"
}
```

## License

All schemas should use compatible open licenses. Recommended: CC-BY-SA-4.0
