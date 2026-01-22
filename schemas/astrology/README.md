# Astrology Schemas

This directory contains interpretive schemas for astrological systems using the unified recursive.eco grammar format.

## Available Schemas

| File | Description |
|------|-------------|
| `L1-basic.json` | Foundation astrology tokens - planets, signs, houses, aspects |
| `alan-leo.json` | Classical interpretations from Alan Leo (1860-1917) |

## Unified Format

All astrology schemas use the unified `items` array format:

```json
{
  "name": "Schema Name",
  "description": "Description",
  "grammar_type": "astrology",
  "items": [
    {
      "id": "sign-aries",
      "name": "Aries",
      "category": "sign",
      "subcategory": "fire",
      "keywords": ["initiative", "courage", "pioneer"],
      "sort_order": 0,
      "sections": {
        "Interpretation": "Main interpretation text...",
        "Shadow": "Challenge patterns..."
      },
      "metadata": {
        "element": "fire",
        "quality": "cardinal",
        "ruler": "Mars"
      }
    }
  ]
}
```

## ID Conventions

Use lowercase IDs with category prefixes:

| Category | Prefix | Examples |
|----------|--------|----------|
| Signs | `sign-` | `sign-aries`, `sign-taurus` |
| Planets | `planet-` | `planet-sun`, `planet-moon` |
| Houses | `house-` | `house-1`, `house-12` |
| Aspects | `aspect-` | `aspect-conjunction`, `aspect-trine` |

## Categories & Subcategories

### Signs
- **category**: `sign`
- **subcategory**: element (`fire`, `earth`, `air`, `water`)
- **metadata**: `element`, `quality` (cardinal/fixed/mutable), `ruler`

### Planets
- **category**: `planet`
- **subcategory**: `null` or type (`luminary`, `personal`, `social`, `transpersonal`)
- **metadata**: `element`, `rules`

### Houses
- **category**: `house`
- **subcategory**: `null` or type (`angular`, `succedent`, `cadent`)
- **metadata**: `natural_sign`, `quadrant`, `number`

### Aspects
- **category**: `aspect`
- **subcategory**: `null` or type (`major`, `minor`)
- **metadata**: `degrees`, `orb`, `nature` (harmonious/challenging/neutral)

## Sort Order Ranges

To maintain consistent ordering across schemas:

| Category | Sort Order Range |
|----------|-----------------|
| Signs | 0-11 |
| Planets | 12-21 |
| Houses | 22-33 |
| Aspects | 34+ |

## Section Patterns

Common section names for astrology items:

```json
"sections": {
  "Interpretation": "Primary meaning",
  "Shadow": "Challenge patterns",
  "Keywords": "Core keyword phrase",
  "Questions": "Reflective prompts",
  "Dynamic": "How this energy expresses"
}
```

## Contributing

When adding astrological schemas:

1. Use the unified `items` format (not separate arrays)
2. Specify the tradition (Western, Vedic, etc.)
3. Include both light and shadow interpretations
4. Document house systems where relevant
5. Add proper attribution for source material

## Legacy Format

The import system in recursive.eco can handle legacy formats with separate arrays (`signs`, `planets`, `houses`, `aspects`), but **new files should use the unified `items` format**.
