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

## Level System for Emergence

Schemas use levels to organize base nodes and their emergent combinations. A level is not stored: it is the depth computed from `parts` (no parts = L1; otherwise 1 + the deepest part):

- **L1**: Base items (64 hexagrams)
- **L2**: Emergent groupings (zodiac signs, chakras, trigrams as organizing lenses)
- **L3**: Meta-categories (l3-signs, l3-chakras, l3-trigrams)

### Example: Zodiac Sign Emergence

```json
{
  "id": "sign-aries",
  "name": "Aries: Initiation Through Challenge",
  "parts": ["hex-25", "hex-17", "hex-21", "hex-51", "hex-42"],
  "sections": {
    "Summary": "Aries gates embody innocence, following guidance, control...",
    "gift": "Natural courage for new beginnings...",
    "shadow": "Recklessness disguised as courage..."
  }
}
```

### Example: Meta-category

```json
{
  "id": "l3-signs",
  "name": "Zodiac Signs",
  "parts": ["sign-aries", "sign-taurus", "sign-gemini", ...],
  "sections": {
    "Philosophy": "The zodiac lens organizes the 64 hexagrams around the wheel of the year..."
  }
}
```

The `parts` array references the IDs of the nodes it is made of (in order), creating explicit emergence relationships.

## Contributing

When adding I Ching schemas:
- Honor the traditional wisdom
- Include multiple translations when available
- Explain the hexagram structure (upper/lower trigrams)
- Document transformation patterns
- Cite scholarly sources
- Use the level system for composite/emergent patterns
