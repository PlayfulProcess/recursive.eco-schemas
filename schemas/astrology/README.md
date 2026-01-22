# Astrology Schemas

This directory contains interpretive schemas for astrological systems.

## Organization

Suggested file structure:
- `zodiac-signs.json` - The 12 zodiac signs
- `planets.json` - Planets and their meanings
- `houses.json` - The 12 houses
- `aspects.json` - Planetary aspects and their interpretations
- `elements.json` - Fire, Earth, Air, Water
- `modalities.json` - Cardinal, Fixed, Mutable

## Schema Format

### Zodiac Sign Schema
```json
{
  "id": "sign_name",
  "name": "Sign Name",
  "symbol": "♈",
  "element": "fire|earth|air|water",
  "modality": "cardinal|fixed|mutable",
  "ruling_planet": "planet_name",
  "date_range": "Month Day - Month Day",
  "keywords": ["keyword1", "keyword2"],
  "traits": {
    "strengths": ["strength1", "strength2"],
    "challenges": ["challenge1", "challenge2"]
  },
  "interpretation": "General interpretation...",
  "source": "Western|Vedic|etc",
  "contributors": ["contributor_id"]
}
```

### Planet Schema
```json
{
  "id": "planet_name",
  "name": "Planet Name",
  "symbol": "☿",
  "rules": ["zodiac_sign"],
  "exalted_in": "zodiac_sign",
  "keywords": ["keyword1", "keyword2"],
  "interpretation": "Planetary meaning...",
  "source": "tradition",
  "contributors": ["contributor_id"]
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

## Contributing

When adding astrological schemas:
- Specify the tradition (Western, Vedic, etc.)
- Include both traditional and modern interpretations
- Document house systems clearly
- Explain calculation methods where relevant
- Use the level system for composite/emergent patterns
