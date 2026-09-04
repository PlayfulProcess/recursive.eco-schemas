# Other Divination Systems

This directory contains interpretive schemas for divination systems beyond Tarot, I Ching, and Astrology.

## Potential Systems

This directory can include:
- Runes (Elder Futhark, Younger Futhark, etc.)
- Oracle cards (various decks and systems)
- Geomancy
- Bibliomancy
- Pendulum systems
- Numerology
- Tea leaf reading
- And any other interpretive frameworks

## Organization

Create subdirectories or files as needed:
- `runes/` - Runic divination systems
- `oracle-cards/` - Various oracle deck schemas
- `geomancy.json` - Geomantic figures and interpretations
- `numerology.json` - Number meanings and calculations

## Schema Format

Create formats appropriate to each system, but generally include:
```json
{
  "system": "system_name",
  "version": "1.0",
  "tradition": "cultural or historical tradition",
  "elements": [
    {
      "id": "unique_id",
      "name": "Element name",
      "symbol": "Symbol or representation",
      "interpretation": "Meaning and usage...",
      "keywords": ["keyword1", "keyword2"]
    }
  ],
  "source": "source attribution",
  "contributors": ["contributor_id"]
}
```

## Contributing

All divination traditions are welcome! When contributing:
- Research the tradition thoroughly
- Honor cultural origins and context
- Cite sources and lineages
- Be respectful of sacred practices
- Include usage guidelines where appropriate
