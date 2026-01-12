# Tarot Schemas

This directory contains interpretive schemas for Tarot cards.

## Organization

### Card Schemas
- `major-arcana.json` - The 22 Major Arcana cards (0-21)
- `minor-arcana-wands.json` - Suit of Wands (Ace through King)
- `minor-arcana-cups.json` - Suit of Cups
- `minor-arcana-swords.json` - Suit of Swords
- `minor-arcana-pentacles.json` - Suit of Pentacles
- `spreads.json` - Common spread patterns and their interpretations
- `court-cards.json` - Detailed interpretations of court cards

### Supplementary Decks
- `plutchik-wheel-emotions.json` - Plutchik's Wheel of Emotions (psychological oracle deck based on Robert Plutchik's evolutionary theory of emotion)

## Schema Format

Each card schema should include:
```json
{
  "id": "unique_identifier",
  "name": "Card Name",
  "suit": "major|wands|cups|swords|pentacles",
  "number": 0-21 or "ace|2-10|page|knight|queen|king",
  "tradition": "Rider-Waite-Smith|Thoth|Marseille|etc",
  "element": "fire|water|air|earth|spirit",
  "keywords": ["keyword1", "keyword2"],
  "interpretation": {
    "upright": "Upright meaning...",
    "reversed": "Reversed meaning..."
  },
  "symbolism": "Key symbols and their meanings...",
  "source": "tradition name or contributor",
  "contributors": ["contributor_id"]
}
```

## Contributing

Multiple traditions and interpretations are welcome! Consider:
- Including both traditional and modern interpretations
- Citing sources and traditions
- Adding cultural context where relevant
- Respecting the lineage of teachings
