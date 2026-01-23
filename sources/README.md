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

### Astrology - Ready to Download from Project Gutenberg

| Text | Author | Year | Plain Text Download |
|------|--------|------|---------------------|
| **Tetrabiblos (Quadripartite)** | Ptolemy (trans. J.M. Ashmand) | ~150 CE / 1822 | [Download TXT](https://www.gutenberg.org/cache/epub/70850/pg70850.txt) |
| **Astrology: How to Make and Read Your Own Horoscope** | Sepharial | 1920 | [Download TXT](https://www.gutenberg.org/cache/epub/46963/pg46963.txt) |
| **Myths and Marvels of Astronomy** | Richard A. Proctor | 1896 | [Download TXT](https://www.gutenberg.org/cache/epub/26556/pg26556.txt) |

**Ptolemy's Tetrabiblos** is the foundational text of Western astrology—the ancient Greek source that shaped all subsequent astrological interpretation.

**Sepharial** (Walter Gorn Old) was a prominent early 20th century astrologer whose work provides practical instruction on natal chart interpretation.

### Historical Tarot & Astrology (Other Sources)

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
