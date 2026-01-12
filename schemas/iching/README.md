# I Ching Schemas

This directory contains interpretive schemas for I Ching hexagrams.

## Organization

Suggested file structure:
- `hexagrams.json` - All 64 hexagrams with interpretations
- `trigrams.json` - The 8 basic trigrams
- `lines.json` - Interpretations for changing lines
- `sequences.json` - The traditional sequence and relationships

## Schema Format

Each hexagram schema should include:
```json
{
  "id": "hexagram_number",
  "number": 1-64,
  "name_chinese": "Chinese name",
  "name_english": "English translation",
  "judgement": "The Judgement text...",
  "image": "The Image text...",
  "upper_trigram": "trigram_name",
  "lower_trigram": "trigram_name",
  "element_relationship": "description",
  "lines": {
    "line_1": "First line interpretation...",
    "line_2": "Second line interpretation...",
    "line_3": "Third line interpretation...",
    "line_4": "Fourth line interpretation...",
    "line_5": "Fifth line interpretation...",
    "line_6": "Sixth line interpretation..."
  },
  "transformations": ["hexagram_id"],
  "source": "Wilhelm|Wing|Huang|etc",
  "contributors": ["contributor_id"]
}
```

## Contributing

When adding I Ching schemas:
- Honor the traditional wisdom
- Include multiple translations when available
- Explain the hexagram structure (upper/lower trigrams)
- Document transformation patterns
- Cite scholarly sources
