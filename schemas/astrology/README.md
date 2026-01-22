# Astrology Schemas

This directory contains interpretive schemas for astrological systems using the recursive.eco grammar format.

## Import Format (AstrologyInterpretationInput)

**This is the canonical format for all astrology schemas that need to import into recursive.eco.**

```json
{
  "name": "Schema Name",
  "description": "Description of the schema",
  "grammar_type": "astrology",
  "attribution": {
    "source_name": "Original Work Title",
    "source_author": "Author Name",
    "source_year": "Year",
    "license": "Public Domain",
    "source_url": "https://..."
  },
  "interpretations": [
    {
      "type": "planet",
      "planet": "Saturn",
      "story": "The narrative interpretation - the main body of text",
      "light": "Positive expression, gifts, beneficial manifestation",
      "shadow": "Challenge expression, difficulties, shadow side",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "sort_order": 0
    },
    {
      "type": "sign",
      "sign": "Aries",
      "story": "The narrative interpretation",
      "light": "Positive expression",
      "shadow": "Challenge expression",
      "keywords": ["fire", "cardinal", "Mars"],
      "sort_order": 10
    },
    {
      "type": "house",
      "house": 1,
      "story": "The narrative interpretation",
      "light": "Positive expression",
      "shadow": "Challenge expression",
      "keywords": ["angular", "self", "beginnings"],
      "sort_order": 30
    },
    {
      "type": "aspect",
      "aspect": "Conjunction",
      "story": "The narrative interpretation",
      "light": "Positive expression",
      "shadow": "Challenge expression",
      "keywords": ["0 degrees", "union"],
      "sort_order": 50
    }
  ]
}
```

### Interpretation Types

| type | Required Fields | Description |
|------|-----------------|-------------|
| `planet` | `planet` | One of: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto |
| `sign` | `sign` | One of: Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces |
| `house` | `house` | Number 1-12 |
| `aspect` | `aspect` | One of: Conjunction, Sextile, Square, Trine, Opposition |
| `planet_sign` | `planet`, `sign` | Planet-in-sign combination |
| `planet_house` | `planet`, `house` | Planet-in-house combination |

### Required Fields

All interpretation objects must have:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | One of the types above |
| `story` | string | The main narrative interpretation |
| `light` | string | Positive/beneficial expression |
| `shadow` | string | Challenging/difficult expression |
| `keywords` | string[] | Array of keywords |
| `sort_order` | number | For ordering (see ranges below) |

### Sort Order Ranges

| Category | Sort Order Range |
|----------|-----------------|
| Planets | 0-9 |
| Signs | 10-21 |
| Houses | 30-41 |
| Aspects | 50-59 |

## Available Schemas

| Schema | Description |
|--------|-------------|
| `ptolemy-tetrabiblos/` | Classical Western astrology from Ptolemy's Tetrabiblos (c. 150 CE) |
| `proctor-skeptical-astrology/` | Victorian skeptical commentary on astrology from Proctor (1896) |
| `jyotish-vedic.json` | Comprehensive Vedic/Hindu astrology with nakshatras and yogas |

## Schema Templates

### Minimal Planet Example

```json
{
  "type": "planet",
  "planet": "Saturn",
  "story": "Saturn represents structure, limitation, and mastery through time.",
  "light": "Discipline, wisdom, patience, endurance, responsibility",
  "shadow": "Restriction, fear, rigidity, melancholy, delay",
  "keywords": ["discipline", "time", "structure", "limitation"],
  "sort_order": 0
}
```

### Minimal Sign Example

```json
{
  "type": "sign",
  "sign": "Aries",
  "story": "Aries initiates the zodiac with cardinal fire energy.",
  "light": "Initiative, courage, leadership, direct action",
  "shadow": "Impatience, aggression, selfishness",
  "keywords": ["fire", "cardinal", "Mars", "initiative"],
  "sort_order": 10
}
```

### Minimal House Example

```json
{
  "type": "house",
  "house": 1,
  "story": "The first house represents self, body, and beginnings.",
  "light": "Self-identity, vitality, personal initiative",
  "shadow": "Self-absorption, difficulty seeing beyond self",
  "keywords": ["angular", "self", "ascendant", "beginnings"],
  "sort_order": 30
}
```

### Minimal Aspect Example

```json
{
  "type": "aspect",
  "aspect": "Conjunction",
  "story": "Conjunction unites planetary energies in the same degree.",
  "light": "Fusion, intensification, new beginnings",
  "shadow": "Overwhelm, blind spots, excessive intensity",
  "keywords": ["0 degrees", "union", "fusion"],
  "sort_order": 50
}
```

## Attribution

Always include attribution for source material:

```json
{
  "attribution": {
    "source_name": "Original Work Title",
    "source_author": "Author Name",
    "source_year": "Publication Year",
    "license": "Public Domain",
    "source_url": "https://..."
  }
}
```

## Contributing

When creating new astrology schemas:

1. **Use the `interpretations` array format** (required for import)
2. **Include all required fields** (type, story, light, shadow, keywords, sort_order)
3. **Specify the tradition** (Western, Vedic, etc.) in the description
4. **Include both light and shadow interpretations**
5. **Add proper attribution** for source material
6. **Follow sort_order ranges** for consistent ordering

## Legacy Formats

The import system can handle some legacy formats (separate `signs`, `planets`, `houses`, `aspects` arrays or unified `items` array), but **new schemas should use the `interpretations` array format** documented above.
