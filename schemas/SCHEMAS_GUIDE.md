# Schemas Directory

This directory contains structured interpretive schemas for various divination and self-reflection systems.

## Subdirectories

- **`tarot/`** - Tarot card meanings and interpretations
- **`iching/`** - I Ching hexagrams and their wisdom
- **`astrology/`** - Astrological signs, planets, houses, and aspects
- **`other/`** - Additional divination systems (runes, oracle cards, etc.)

## Level System for Emergence

> 📖 **For the complete canonical grammar shape**, see the root-level
> [GRAMMAR_FORMAT.md](../GRAMMAR_FORMAT.md). It documents the full
> UnifiedItem format, all valid `grammar_type` values, the per-item
> `performance` object for video clips, `metadata.youtube_video_id`
> conventions, and the three common mistakes that prevent grammars
> from loading.

Schemas use a level system to organize base items and their emergent combinations:

- **L1 (level: 1)**: Base items (cards, hexagrams, planets, songs)
- **L2 (level: 2)**: Emergent combinations of L1 items (spreads, zodiac signs, albums, yogas)
- **L3 (level: 3)**: Meta-categories or higher-order groupings (organizing principles, artists)

All levels live in the **same `items[]` array** at the top of the
grammar. Composite items (L2/L3) are distinguished by the presence
of a `composite_of` array. Do not put composite items in a separate
top-level `emergences[]` block — the editor and viewer do not
support that shape.

### Example Structure

```json
{
  "id": "album-example",
  "name": "Example Album",
  "level": 2,
  "composite_of": ["song-1", "song-2", "song-3"],
  "sections": {
    "Summary": "When these songs come together..."
  }
}
```

The `composite_of` array references the IDs of items at the level
below, creating explicit emergence relationships. The `level` field
itself is optional — the real signal is whether `composite_of` is
present.

## Adding Schemas

When adding new schemas:

1. Choose the appropriate subdirectory
2. Use clear, descriptive filenames (e.g., `major-arcana.json`, `hexagrams.json`)
3. Include source attribution and tradition information
4. Follow the format examples in each subdirectory
5. Use the level system for composite/emergent patterns

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.
