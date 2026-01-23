# recursive.eco-schemas

Grammar schemas (JSON files) for the recursive.eco platform - a meaning-making tool for astrology, tarot, I Ching, and custom symbolic systems.

## Purpose

This repository serves as a commons for interpretive schemas used in divination and self-reflection practices. It brings together structured data, templates, and community wisdom to support the recursive.eco ecosystem.

## What's Inside

- **`/schemas/`** - Structured interpretive schemas for Tarot, I Ching, Astrology, and other systems
- **`/sources/`** - Public domain source materials for schema creation

## Quick Start

1. Browse the `/schemas/` directory to find interpretive frameworks
2. Check `/sources/` for public domain materials to reference
3. Read the [JSON Structure Guide](#json-structure-guide) below to create your own

---

## JSON Structure Guide

The recursive.eco import system is **partially field-agnostic**. It handles:
1. **Known formats** (legacy): `cards[]`, `hexagrams[]`, `interpretations[]` - uses specific converters
2. **Unified format**: `items[]` with `sections` object - passes through directly
3. **Unknown formats**: Falls back to field-agnostic conversion

### Basic Item Structure

```json
{
  "name": "Grammar Name",
  "description": "What this grammar represents",
  "grammar_type": "astrology|tarot|iching|custom",
  "items": [
    {
      "id": "unique-id",
      "name": "Item Name",
      "symbol": "☉",
      "category": "planet|sign|house|graha|rashi|bhava|card|hexagram|custom",
      "sections": {
        "Interpretation": "Main content text...",
        "Light": "Positive expression...",
        "Shadow": "Challenge/shadow aspect..."
      },
      "keywords": ["tag1", "tag2"],
      "sort_order": 0
    }
  ]
}
```

### Emergence Levels (L1, L2, L3)

The system supports hierarchical emergence through levels:

- **L1**: Base items (planets, signs, cards, hexagram lines)
- **L2**: Combinations/emergences (aspects, yogas, card spreads) - reference L1s via `composite_of`
- **L3**: Meta-categories grouping L2 items

```json
{
  "id": "sun-moon-conjunction",
  "name": "Sun-Moon Conjunction",
  "level": 2,
  "category": "aspect",
  "composite_of": ["sun", "moon"],
  "sections": {
    "Interpretation": "When Sun and Moon unite..."
  }
}
```

### Default Category Roles (Auto-Mapped)

The system automatically maps these categories to viewer roles:

| Category | Role | Tradition |
|----------|------|-----------|
| `planet` | planet | Western |
| `sign` | sign | Western |
| `house` | house | Western |
| `graha` | planet | Vedic |
| `rashi` | sign | Vedic |
| `bhava` | house | Vedic |
| `nakshatra` | nakshatra | Vedic |
| `yoga` | emergence | Vedic |
| `hexagram` | hexagram | I Ching |
| `trigram` | trigram | I Ching |
| `major` | card | Tarot |
| `minor` | card | Tarot |

### Custom Category Mappings

For non-standard categories, add `_category_roles` at the grammar level:

```json
{
  "name": "Custom Grammar",
  "_category_roles": {
    "wanderer": "planet",
    "domain": "house",
    "archetype": "emergence"
  },
  "items": [...]
}
```

### Field Classification (Field-Agnostic Import)

When using the field-agnostic converter, fields are classified as:
- **Sections**: String > 50 chars, or arrays of long strings
- **Metadata**: String ≤ 50 chars, numbers, booleans, complex objects
- **Reserved** (not converted): `id`, `name`, `symbol`, `category`, `keywords`, `questions`, `sort_order`, `level`, `composite_of`

Field names are auto-converted to Title Case:
- `ptolemy_description` → "Ptolemy Description"
- `lightShadow` → "Light Shadow"

### Astrology-Specific Fields

For Vedic grammars, include `english_name` for cross-tradition lookup:

```json
{
  "id": "mangala",
  "name": "Mangala",
  "english_name": "Mars",
  "symbol": "♂",
  "category": "graha"
}
```

### Quotes/Source Text

Include quotes as array - they'll be formatted with quotation marks:

```json
{
  "name": "Saturn",
  "quotes": [
    "Time devours all his children",
    "The Golden Age was his reign"
  ]
}
```

---

## Examples

### Minimal Astrology Grammar

```json
{
  "name": "My Astrology Grammar",
  "grammar_type": "astrology",
  "items": [
    {
      "id": "sun",
      "name": "Sun",
      "symbol": "☉",
      "category": "planet",
      "sections": {
        "Interpretation": "The Sun represents your core identity and vital force.",
        "Light": "Confidence, creativity, leadership",
        "Shadow": "Ego, pride, need for attention"
      },
      "keywords": ["identity", "vitality", "ego"]
    }
  ]
}
```

### Vedic Grammar with Emergences

```json
{
  "name": "Jyotish Basics",
  "grammar_type": "astrology",
  "_category_roles": {
    "graha": "planet",
    "yoga": "emergence"
  },
  "items": [
    {
      "id": "surya",
      "name": "Surya",
      "english_name": "Sun",
      "symbol": "☉",
      "category": "graha",
      "level": 1,
      "sections": {
        "Interpretation": "Surya represents atma (soul)..."
      }
    },
    {
      "id": "gajakesari-yoga",
      "name": "Gajakesari Yoga",
      "category": "yoga",
      "level": 2,
      "composite_of": ["chandra", "guru"],
      "sections": {
        "Interpretation": "When Moon and Jupiter are in kendra..."
      }
    }
  ]
}
```

---

## AI Prompt for Creating Grammars

Use this prompt when asking Claude to create a grammar:

```
Create a grammar JSON for [TOPIC] with the following structure:

{
  "name": "[Grammar Title]",
  "description": "[Your unique perspective on this system]",
  "grammar_type": "[astrology|tarot|iching|custom]",
  "creator_name": "[Your name]",
  "items": [
    {
      "id": "[unique-slug]",
      "name": "[Item Name]",
      "symbol": "[Unicode symbol if applicable]",
      "category": "[category from defaults or custom]",
      "sections": {
        "Interpretation": "[2-3 sentences of meaning]",
        "Light": "[Positive expression]",
        "Shadow": "[Challenge/shadow aspect]"
      },
      "keywords": ["keyword1", "keyword2"],
      "sort_order": [number]
    }
  ]
}

Requirements:
- Each item needs unique id (lowercase, hyphenated)
- Use existing category names when possible (planet, sign, house, graha, rashi, etc.)
- For L2 emergences, add: "level": 2, "composite_of": ["id1", "id2"]
- Keep interpretations concise but meaningful
```

---

## Validation

Before submitting, verify:
1. All items have unique `id` fields
2. `composite_of` references point to valid item IDs
3. Category names are consistent throughout
4. JSON is valid (use a linter)

---

## Contributing

1. Fork this repository
2. Create your grammar in `schemas/[type]/[name]/[name].json`
3. Submit a pull request
4. Grammars are licensed CC-BY-SA-4.0

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Repository Structure

For detailed information about how this repository is organized, see [STRUCTURE.md](STRUCTURE.md).

## Philosophy

This repository embodies principles of:
- **Open Knowledge**: Sharing wisdom freely
- **Community Care**: Nurturing collective understanding
- **Respectful Practice**: Honoring diverse traditions
- **Recursive Growth**: Learning and evolving together

## License

This repository is shared as a commons for the community. See LICENSE for details.

---

*This README is optimized for AI assistants (Claude Code) to understand the schema format and help create valid grammars.*
