# Astrology Schemas

This directory contains interpretive schemas for astrological systems using the unified recursive.eco grammar format.

## Available Schemas

| File | Description |
|------|-------------|
| `L1-basic.json` | Foundation astrology tokens - planets, signs, houses, aspects |
| `alan-leo.json` | Classical interpretations from Alan Leo (1860-1917) |
| `jyotish-vedic.json` | Comprehensive Vedic/Hindu astrology with nakshatras and yogas |

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

## Level System for Emergence

Schemas use a level system to organize base items and their emergent combinations:

- **L1 (level: 1)**: Base items (planets, signs, houses, individual hexagrams, songs)
- **L2 (level: 2)**: Emergent combinations of L1 items (yogas, aspects, albums)
- **L3 (level: 3)**: Meta-categories or higher-order groupings (organizing principles, artists)

### Example: Vedic Yoga

```json
{
  "id": "yoga-raja",
  "name": "Raja Yoga",
  "level": 2,
  "composite_of": ["graha-surya", "graha-chandra", "graha-guru"],
  "sections": {
    "Interpretation": "When Sun, Moon, Jupiter combine in specific houses..."
  }
}
```

### Example: Meta-category

```json
{
  "id": "l3-yogas",
  "name": "Vedic Yogas",
  "level": 3,
  "composite_of": ["yoga-raja", "yoga-gajakesari", "yoga-budhaditya"],
  "sections": {
    "Summary": "Planetary combinations that produce specific life patterns..."
  }
}
```

The `composite_of` array references the IDs of items at the level below, creating explicit emergence relationships.

## Jyotish (Vedic) Schema

The `jyotish-vedic.json` schema provides comprehensive Hindu astrology interpretations including:

**L1 Items (60 items):**
- 9 Grahas (planets including Rahu/Ketu)
- 12 Rashis (signs with sidereal zodiac)
- 12 Bhavas (houses with traditional classifications)
- 27 Nakshatras (lunar mansions with deities and shaktis)

**L2 Emergences:**
- Pancha Mahapurusha Yogas (5 planetary strength yogas)
- Lunar Yogas (Gajakesari, Chandra-Mangala, etc.)
- Viparita Raja Yogas (Harsha, Sarala, Vimala)
- Nakshatra Gana groupings (Deva, Manushya, Rakshasa)

**L3 Emergences:**
- Raja Yogas (kendra-trikona combinations)
- Dhana Yogas (wealth combinations)
- Special Yogas (Saraswati, Amala, Kala Sarpa)

## Contributing

When adding astrological schemas:

1. Use the unified `items` format (not separate arrays)
2. Specify the tradition (Western, Vedic, etc.)
3. Include both light and shadow interpretations
4. Document house systems where relevant
5. Add proper attribution for source material
6. Use the level system for composite/emergent patterns

## Legacy Format

The import system in recursive.eco can handle legacy formats with separate arrays (`signs`, `planets`, `houses`, `aspects`), but **new files should use the unified `items` format**.
