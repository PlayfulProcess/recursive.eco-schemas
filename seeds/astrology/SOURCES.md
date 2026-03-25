# Astrology Source Texts

Public domain astrological texts for schema creation.

## Download Instructions

Download these texts from Project Gutenberg and save them here:

```bash
# Ptolemy's Tetrabiblos - foundational Western astrology text
curl -o ptolemy-150ce-tetrabiblos.txt "https://www.gutenberg.org/cache/epub/70850/pg70850.txt"

# Sepharial's practical horoscope guide
curl -o sepharial-1920-horoscope.txt "https://www.gutenberg.org/cache/epub/46963/pg46963.txt"

# Proctor's astronomy/astrology history
curl -o proctor-1896-myths-marvels.txt "https://www.gutenberg.org/cache/epub/26556/pg26556.txt"
```

## Available Texts

### Ptolemy's Tetrabiblos (c. 150 CE)

**Gutenberg ID**: 70850
**Translator**: J.M. Ashmand (1822)
**Download**: https://www.gutenberg.org/ebooks/70850

The foundational text of Western astrology. Ptolemy systematized earlier Greek, Egyptian, and Babylonian astrological knowledge into four books covering:

1. General principles and planetary influences
2. Mundane astrology (nations and weather)
3. Natal astrology (genethlialogy)
4. Specific life areas and timing

**Schema potential**: Planet meanings, sign qualities, house significations, aspect interpretations.

---

### Astrology: How to Make and Read Your Own Horoscope (1920)

**Author**: Sepharial (Walter Gorn Old)
**Gutenberg ID**: 46963
**Download**: https://www.gutenberg.org/ebooks/46963

Practical early 20th century guide to natal chart interpretation. Covers:

- Calculating and drawing charts
- Planet in sign interpretations
- House meanings
- Aspect delineation
- Predictive techniques

**Schema potential**: Modern(ish) planet-sign combinations, house interpretations, aspect meanings.

---

### Myths and Marvels of Astronomy (1896)

**Author**: Richard A. Proctor
**Gutenberg ID**: 26556
**Download**: https://www.gutenberg.org/ebooks/26556

Historical and critical examination of astrology within the context of astronomy. Includes:

- History of astrology from Chaldean origins
- Relationship between astronomy and astrology
- Critical analysis of astrological claims
- Cultural impact of astrological thinking

**Schema potential**: Historical context, etymology of astrological terms, cross-cultural comparisons.

---

## Other Recommended Sources

### Internet Archive

- **William Lilly - Christian Astrology (1647)**: The definitive horary astrology text
  https://archive.org/details/christianastrolo00lill

- **Alan Leo - How to Judge a Nativity (1912)**: Comprehensive natal interpretation
  https://archive.org/search?query=alan+leo+astrology

### Sacred Texts Archive

- **Astrology section**: https://sacred-texts.com/astro/index.htm
- Includes various historical texts and translations

## Processing Notes

When converting these texts to JSON schemas:

1. Focus on interpretive content (planet meanings, sign qualities, house significations)
2. Preserve the language/style of the era where it adds value
3. Note any outdated or problematic content
4. Include proper attribution in the schema file
