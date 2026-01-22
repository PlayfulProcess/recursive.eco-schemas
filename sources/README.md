# Sources

This directory contains **public domain source materials** for schema creation.

## Important: Public Domain Only

All materials in this directory must be in the **public domain**. This includes:

- Works where copyright has expired (typically published before 1929 in the US)
- Works explicitly released to the public domain by their creators
- Government documents (where applicable)
- Works with CC0 (Creative Commons Zero) licenses

**Do not add copyrighted materials** without explicit permission and proper licensing.

## Directory Structure

| Folder | Contents |
|--------|----------|
| `tarot/` | Historical tarot texts, card descriptions, esoteric writings |
| `astrology/` | Classical astrology texts, ephemerides, interpretive works |
| `iching/` | I Ching translations, commentaries, historical texts |
| `other/` | Other divination systems, symbolic references |

## Recommended Sources

### Public Domain Repositories

- [Internet Archive](https://archive.org) - Vast collection of digitized books
- [Project Gutenberg](https://www.gutenberg.org) - Free ebooks
- [Sacred Texts Archive](https://sacred-texts.com) - Religious and esoteric texts
- [Wikisource](https://wikisource.org) - Source texts in multiple languages

### Historical Tarot & Astrology

- Antoine Court de Gébelin's writings (18th century)
- Etteilla's tarot works (18th century)
- Alan Leo's astrology texts (early 20th century)
- William Lilly's "Christian Astrology" (1647)
- James Legge's I Ching translation (1882)

## File Naming Convention

Use descriptive names with author and year when known:

```
tarot/
  court-de-gebelin-1781-monde-primitif.pdf
  etteilla-1783-maniere-de-tirer.txt

astrology/
  alan-leo-1912-how-to-judge-nativity.pdf
  william-lilly-1647-christian-astrology.pdf

iching/
  james-legge-1882-i-ching.txt
```

## Attribution

When converting source materials to JSON schemas, always include:

```json
{
  "attribution": {
    "source_name": "Original Work Title",
    "source_author": "Author Name",
    "source_year": "Publication Year",
    "license": "Public Domain",
    "source_url": "https://archive.org/..."
  }
}
```

## Processing Workflow

1. Add public domain source material to appropriate subfolder
2. Document the source in this README or create a `sources.md` in the subfolder
3. Create JSON schema in `/schemas/` using the unified format
4. Include full attribution in the schema file
