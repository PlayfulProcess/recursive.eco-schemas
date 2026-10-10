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

## Level System for Emergence

Schemas use levels to organize base nodes and their emergent combinations. A level is not stored: it is the depth computed from `parts` (no parts = L1; otherwise 1 + the deepest part):

- **L1**: Base items (individual cards, songs)
- **L2**: Emergent combinations (spreads, albums, card pairings)
- **L3**: Meta-categories (deck collections, artists)

### Example: Music/Poetry Deck

```json
{
  "id": "album-example",
  "name": "Album Name",
  "parts": ["song-01", "song-02", "song-03"],
  "sections": {
    "Summary": "Thematic description of the album...",
    "Themes": "Key themes explored across these songs"
  }
}
```

### Example: Tarot Spread

```json
{
  "id": "spread-celtic-cross",
  "name": "Celtic Cross",
  "parts": ["position-1", "position-2", "position-3"],
  "sections": {
    "Interpretation": "How to read cards in these positions together..."
  }
}
```

The `parts` array references the IDs of the nodes it is made of (in order), creating explicit emergence relationships.

## Contributing

Multiple traditions and interpretations are welcome! Consider:
- Including both traditional and modern interpretations
- Citing sources and traditions
- Adding cultural context where relevant
- Respecting the lineage of teachings
- Using the level system for composite/emergent patterns
