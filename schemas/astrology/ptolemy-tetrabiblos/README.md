# Ptolemy's Tetrabiblos

Classical Western astrology based on Claudius Ptolemy's *Tetrabiblos* (c. 150 CE), the foundational text that systematized Greek, Egyptian, and Babylonian astrological knowledge.

## Source

- **Text**: Tetrabiblos, or Quadripartite
- **Author**: Claudius Ptolemy (c. 100-170 CE)
- **Translator**: J.M. Ashmand (1822)
- **License**: Public Domain
- **Source**: [Project Gutenberg #70850](https://www.gutenberg.org/ebooks/70850)

## Schema Structure

**Total Items**: 55

### L1 - Base Elements (36 items)

| Type | Count | Description |
|------|-------|-------------|
| Planets | 7 | Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon |
| Signs | 12 | Aries through Pisces with Ptolemaic qualities |
| Houses | 12 | The twelve places with Greek names |
| Aspects | 5 | Conjunction, sextile, square, trine, opposition |

### L2 - Emergent Classifications (14 items)

| Type | Count | Description |
|------|-------|-------------|
| Triplicities | 4 | Fire, Earth, Air, Water element groupings |
| Quadruplicities | 3 | Cardinal, Fixed, Mutable modalities |
| Sects | 2 | Diurnal and Nocturnal planetary sects |
| House Classifications | 3 | Angular, Succedent, Cadent |
| Planetary Classifications | 3 | Benefics, Malefics, Luminaries |
| Lots | 2 | Fortune and Spirit |

### L3 - Meta-Categories (5 items)

- **l3-planets**: The seven classical planets
- **l3-signs**: The twelve zodiacal signs
- **l3-houses**: The twelve mundane houses
- **l3-aspects**: The five major aspects
- **l3-dignities**: All dignity systems and classifications

## Ptolemaic System

### Planetary Qualities

Ptolemy assigns each planet qualities based on the hot/cold and moist/dry polarities:

| Planet | Primary | Secondary | Nature |
|--------|---------|-----------|--------|
| Saturn | Cold | Dry | Malefic |
| Jupiter | Hot | Moist | Benefic |
| Mars | Hot | Dry | Malefic |
| Sun | Hot | Dry | Benefic |
| Venus | Moist | Warm | Benefic |
| Mercury | Variable | Variable | Neutral |
| Moon | Moist | Cold | Neutral |

### Essential Dignities

Each planet has signs of dignity (strength) and debility (weakness):

- **Domicile**: The sign(s) a planet rules
- **Exaltation**: Where a planet is honored
- **Detriment**: Opposite to domicile
- **Fall**: Opposite to exaltation

### Sect

Ptolemy divides planets into day (diurnal) and night (nocturnal) sects:

- **Day Sect**: Sun, Jupiter, Saturn
- **Night Sect**: Moon, Venus, Mars
- **Neither**: Mercury (adapts to context)

## Emergence Pattern

This schema follows the **emergence level system**:

- **L1 items** are the atomic building blocks (planets, signs, houses, aspects)
- **L2 items** emerge from combinations of L1 elements (triplicities combine three signs of the same element; sects combine planets of the same diurnal/nocturnal nature)
- **L3 items** are meta-categories that organize the schema

The `composite_of` field in L2 items references the L1 items they emerge from.

## Usage Notes

When using this schema for interpretation:

1. Assess planetary dignity by sign placement
2. Consider sect (day or night chart)
3. Evaluate house position (angular, succedent, cadent)
4. Apply aspects between planets
5. Calculate relevant lots (Fortune, Spirit)

## Selected Quotes

> "Saturn's star is productive of cold, and is moderately drying; probably deriving its influence from being most remote both from the heating power of the Sun, and from the moistening vapours of the Earth."

> "The trine, comprehending four signs, is considered most harmonious and beneficial, as signs in trine share the same element and thus the same essential nature."

> "The angular or cardinal houses are the four angles of the chart: the Ascendant, IC, Descendant, and Midheaven. Planets in these places are most powerful and most visible in their effects."
