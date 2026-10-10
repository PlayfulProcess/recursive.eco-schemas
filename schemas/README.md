# Schemas Directory

This directory contains structured interpretive schemas for various divination and self-reflection systems.

## Subdirectories

- **`tarot/`** - Tarot card meanings and interpretations
- **`iching/`** - I Ching hexagrams and their wisdom
- **`astrology/`** - Astrological signs, planets, houses, and aspects
- **`other/`** - Additional divination systems (runes, oracle cards, etc.)

## Level System for Emergence

Schemas use levels to organize base nodes and their emergent combinations. A level is not stored: it is the depth computed from `parts` (no parts = L1; otherwise 1 + the deepest part):

- **L1**: Base items (cards, hexagrams, planets, songs)
- **L2**: Emergent combinations of L1 items (spreads, zodiac signs, albums, yogas)
- **L3**: Meta-categories or higher-order groupings (organizing principles, artists)

### Example Structure

```json
{
  "id": "album-example",
  "name": "Example Album",
  "parts": ["song-1", "song-2", "song-3"],
  "sections": {
    "Summary": "When these songs come together..."
  }
}
```

The `parts` array references the IDs of the nodes it is made of (in order), creating explicit emergence relationships.

## Adding Schemas

When adding new schemas:

1. Choose the appropriate subdirectory
2. Use clear, descriptive filenames (e.g., `major-arcana.json`, `hexagrams.json`)
3. Include source attribution and tradition information
4. Follow the format examples in each subdirectory
5. Use the level system for composite/emergent patterns

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.
