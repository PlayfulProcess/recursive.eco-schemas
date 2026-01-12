# Schema Format Specification

This document defines the format specification for interpretation schemas in the recursive.eco-schemas repository.

## Directory Structure

The repository is organized by divination system, with each system containing various decks/traditions:

```
├── tarot/
│   ├── <deck-name>/
│   │   ├── grammar.json      # Card definitions, meanings
│   │   ├── LICENSE           # License file (e.g., CC-BY-SA-4.0)
│   │   └── README.md         # Description, attribution chain
│   └── ...
├── iching/
│   └── <tradition-name>/
│       ├── grammar.json      # Hexagram definitions, meanings
│       ├── LICENSE
│       └── README.md
└── SCHEMA.md                 # This file
```

## Grammar File Format

Each `grammar.json` file should contain the interpretation data for the specific divination system.

### Tarot Grammar Schema

For tarot decks, the `grammar.json` should follow this structure:

```json
{
  "name": "Deck Name",
  "system": "tarot",
  "version": "1.0.0",
  "description": "Brief description of the deck",
  "cards": [
    {
      "id": "the-fool",
      "name": "The Fool",
      "number": 0,
      "arcana": "major",
      "keywords": ["beginnings", "innocence", "spontaneity"],
      "meanings": {
        "upright": "Description of upright meaning",
        "reversed": "Description of reversed meaning"
      },
      "astrology": "Optional astrological association",
      "element": "Optional elemental association"
    }
  ]
}
```

### I Ching Grammar Schema

For I Ching traditions, the `grammar.json` should follow this structure:

```json
{
  "name": "Tradition Name",
  "system": "iching",
  "version": "1.0.0",
  "description": "Brief description of the tradition",
  "hexagrams": [
    {
      "id": 1,
      "name": "The Creative",
      "chinese": "乾",
      "trigrams": {
        "upper": "heaven",
        "lower": "heaven"
      },
      "judgment": "Description of the judgment",
      "image": "Description of the image",
      "lines": [
        {
          "position": 1,
          "text": "Line meaning"
        }
      ]
    }
  ]
}
```

## Required Files

Each deck/tradition directory must contain:

1. **grammar.json** - The interpretation data in JSON format
2. **LICENSE** - License information (recommended: CC-BY-SA-4.0 for community collaboration)
3. **README.md** - Description of the deck/tradition and attribution chain

## README.md Format

Each deck/tradition README.md should include:

- **Title**: Name of the deck/tradition
- **Description**: Overview of the deck/tradition
- **Attribution**: Chain of attribution for the interpretations
- **License**: License information
- **Contributors**: List of contributors

## License Recommendations

We recommend using open licenses that allow collaboration and remixing:

- **CC-BY-SA-4.0** (Creative Commons Attribution-ShareAlike 4.0)
- **CC-BY-4.0** (Creative Commons Attribution 4.0)
- **Public Domain** (CC0)

## Contributing

To contribute a new deck or tradition:

1. Create a new directory under the appropriate system (e.g., `tarot/my-deck/`)
2. Add the three required files: `grammar.json`, `LICENSE`, and `README.md`
3. Ensure your `grammar.json` follows the schema defined above
4. Include proper attribution in your README.md
5. Submit a pull request

## Validation

All `grammar.json` files should be valid JSON and follow the schema structure defined above.
