# Ptolemy's Tetrabiblos

Classical Western astrology based on Claudius Ptolemy's *Tetrabiblos* (c. 150 CE), the foundational text that systematized Greek, Egyptian, and Babylonian astrological knowledge.

## Source

- **Text**: Tetrabiblos, or Quadripartite
- **Author**: Claudius Ptolemy (c. 100-170 CE)
- **Translator**: J.M. Ashmand (1822)
- **License**: Public Domain
- **Source**: [Project Gutenberg #70850](https://www.gutenberg.org/ebooks/70850)

## Schema Format

This schema uses the **AstrologyInterpretationInput** format for recursive.eco import:

```json
{
  "interpretations": [
    {
      "type": "planet",
      "planet": "Saturn",
      "story": "Narrative interpretation with Ptolemaic language",
      "light": "Beneficial expression",
      "shadow": "Challenging expression",
      "keywords": ["cold", "dry", "malefic"],
      "sort_order": 0
    }
  ]
}
```

## Contents

**36 interpretations total:**

| Type | Count | Description |
|------|-------|-------------|
| Planets | 7 | Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon |
| Signs | 12 | Aries through Pisces with Ptolemaic qualities |
| Houses | 12 | The twelve places with Greek names |
| Aspects | 5 | Conjunction, sextile, square, trine, opposition |

## Ptolemaic System

### Planetary Qualities

Ptolemy assigns each planet qualities based on hot/cold and moist/dry polarities:

| Planet | Primary | Secondary | Nature |
|--------|---------|-----------|--------|
| Saturn | Cold | Dry | Malefic |
| Jupiter | Hot | Moist | Benefic |
| Mars | Hot | Dry | Malefic |
| Sun | Hot | Dry | Benefic |
| Venus | Moist | Warm | Benefic |
| Mercury | Variable | Variable | Neutral |
| Moon | Moist | Cold | Neutral |

### House System

Ptolemy uses the **Whole Sign** house system with Greek names:

| House | Greek Name | Signification |
|-------|------------|---------------|
| 1 | Horoskopos | Life, body, soul |
| 4 | Hypogeion | Parents, ancestry, endings |
| 7 | Dysis | Marriage, partnership |
| 10 | Mesouranema | Honor, profession, authority |

## Selected Quotes

> "Saturn's star is productive of cold, and is moderately drying; probably deriving its influence from being most remote both from the heating power of the Sun, and from the moistening vapours of the Earth."

> "The trine, comprehending four signs, is considered most harmonious and beneficial, as signs in trine share the same element and thus the same essential nature."

## Usage

Import this schema into recursive.eco to get classical Western astrological interpretations based on the original Greek source that shaped all subsequent Western astrology.
