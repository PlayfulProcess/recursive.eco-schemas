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

Schemas use levels to organize base nodes and their emergent combinations. A level is not stored: it is the depth computed from `parts` (no parts = L1; otherwise 1 + the deepest part):

- **L1**: Base items (cards, hexagrams, planets, songs)
- **L2**: Emergent combinations of L1 items (spreads, zodiac signs, albums, yogas)
- **L3**: Meta-categories or higher-order groupings (organizing principles, artists)

All levels live in the **same `nodes[]` array** at the top of the
grammar. Composite nodes (L2/L3) are distinguished by the presence
of a `parts` array. Do not put composite items in a separate
top-level `emergences[]` block — the editor and viewer do not
support that shape.

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

The `parts` array references the IDs of the nodes it is made of (in
order), creating explicit emergence relationships. There is no `level`
field: the level is the depth computed from `parts`.

## Adding Schemas

When adding new schemas:

1. Choose the appropriate subdirectory
2. Use clear, descriptive filenames (e.g., `major-arcana.json`, `hexagrams.json`)
3. Include source attribution and tradition information
4. Follow the format examples in each subdirectory
5. Use the level system for composite/emergent patterns

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.
