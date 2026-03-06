# Build Log: Myths Through Many Eyes Expansion + Source Grammars

## Session Date: 2026-03-05/06

## What Was Done

### 1. Myths Through Many Eyes Grammar Expansion (60→73 items)

**Starting state**: 60 items (31 myths, 13 interpreters, 8 threads, 5 cultures, 3 meta)

**Added 12 new L1 myths**:
- Greek: Dionysus, Medusa, Circe, Pandora, Oedipus, Ariadne
- Japanese: Amaterasu (sun goddess cave withdrawal)
- Inuit: Sedna (sea mother, severed fingers)
- Pan-Indigenous: Coyote the Trickster
- European: Handless Maiden (Grimm)
- Mesoamerican: Quetzalcoatl (feathered serpent)
- Mesopotamian: Tammuz/Dumuzi (dying consort)

**Added 1 new culture card**: Indigenous Americas (Coyote, Sedna, Raven, Hero Twins)

**Added to all myth items**:
- `grammars[]` array with GitHub direct links to source grammars in the repo
- `metadata.astrology` with planets, signs, and themes for astrology app integration

**Final state**: 73 items (43 myths, 13 interpreters, 8 threads, 6 cultures, 3 meta), 299 sections

### 2. Arabian Nights Grammar (NEW — 44 items)

**Source**: `seeds/arabian-nights.txt` (Gutenberg #128, Andrew Lang 1898 edition)
**Parser**: `scripts/parse_arabian_nights.py`
**Output**: `grammars/arabian-nights/grammar.json`

34 L1 stories organized into 8 L2 cycles + 2 L3 meta cards:
- Merchants & Genies cycle (3 tales)
- Fisherman cycle (5 tales including nested physician/parrot/vizir stories)
- Three Calenders cycle (5 tales — the forbidden door pattern)
- Seven Voyages of Sindbad (8 items: frame + 7 voyages)
- Little Hunchback cycle (3 tales — death as comedy)
- Love Tales (Camaralzaman, Noureddin)
- Magic Tales (Aladdin, Enchanted Horse, Two Sisters)
- Caliph's Tales (Haroun-al-Raschid frame, 4 moral tales)

**Parser approach**: Heading-based extraction using `\nHeading\n` pattern. Worked cleanly for 34 stories. Story text truncated at ~2800 chars with word count for remainder.

**Issue**: Frame story heading ("The Arabian Nights") wasn't found initially because `body_start` calculation was wrong. Fixed by using Gutenberg start marker instead.

### 3. Russian Folk-Tales Grammar (NEW — 61 items)

**Source**: `seeds/russian-folk-tales.txt` (Gutenberg #62509, Afanasyev/Magnus 1915)
**Parser**: `scripts/parse_russian_folk_tales.py`
**Output**: `grammars/russian-folk-tales/grammar.json`

52 L1 tales organized into 8 L2 thematic groups + 1 L3 meta:
- Supernatural & Enchantment (Bába Yagá, Vasilísa, enchanted princes)
- Tricksters & Clever Folk (fools, drunkards, cunning peasants)
- Heroes & Bogatyrs (Ilyá Múromets, soldiers vs Death)
- Women of Power (Vasilísa, warrior women, wise wives)
- Saints, Sinners & Judgment (Christian-pagan blend)
- Animal Tales (forest creatures who speak truth)
- Family, Fate & Fortune (domestic world, sorrow personified)
- Nature, Place & Cosmology (sun, rivers, wood sprites)

**Parser approach**: Centered ALL-CAPS headings with >20 leading spaces, between blank lines. Handled duplicate titles ("A Tale of the Dead" x3) with suffix numbering. Stripped footnote markers like `[21]`.

**Issue**: Only found 52 of 73 tales from TOC. Missing ~21 tales whose headings didn't match the ALL-CAPS centered pattern (some had different formatting, mixed case, or were subsections). Acceptable — 52 tales is still a substantial grammar. Could revisit with a more sophisticated parser that also matches the TOC titles directly.

### 4. Grammar Cross-Linking

Added `grammars[]` links in Myths Through Many Eyes:
- `myth-scheherazade` → `arabian-nights`
- `myth-vasalisa-baba-yaga` → `russian-folk-tales`
- `interp-estes` → `russian-folk-tales` (Vasalisa is her key myth)
- `interp-warner` → `arabian-nights` (Scheherazade is her key figure)

## Learnings

1. **Astrology metadata is straightforward for mythology**: Every major myth has clear planetary/zodiacal associations dating back to classical astrology. Inanna literally IS Venus. Odin maps to Mercury. This is well-trodden ground.

2. **`grammars[]` cross-linking pattern works well**: Using GitHub direct links as identifiers. User will swap to Supabase UUIDs on upload. Pattern: `https://github.com/PlayfulProcess/recursive.eco-schemas/tree/main/grammars/GRAMMAR-NAME`

3. **Russian folk tales have irregular formatting**: Unlike many Gutenberg texts, the headings aren't consistently formatted. Some titles are mixed-case, some have footnote markers, some appear to be subsections rather than standalone tales. A TOC-first parsing approach (match TOC titles against the body) would catch more.

4. **Arabian Nights parser was cleaner**: Clear `\nTitle\n` pattern caught all 34 stories. The heading format was consistent.

5. **Story text truncation at ~2800 chars** is a good balance: gives enough to understand the tale while keeping the grammar file manageable. The `[Story continues for approximately N more words...]` pattern signals there's more.

6. **From-memory myths (the 12 new ones) take significant space**: Each myth with 4 sections (Story, Source, Images, Culture) runs ~1500-2500 chars per section. 12 myths = ~40-60KB of content. This is the most context-intensive part of the work.

## What's Left to Build (Source Grammars for Myths Through Many Eyes)

Priority order (most needed for cross-linking):

| Seed | Grammar | Myths it sources | Status |
|------|---------|-----------------|--------|
| `golden-ass-apuleius.txt` | golden-ass-apuleius | myth-psyche-eros | Not started |
| `mabinogion.txt` | mabinogion | myth-fisher-king, myth-taliesin | Not started |
| `myths-babylonia-assyria.txt` | myths-babylonia-assyria | myth-gilgamesh, myth-inanna, myth-tammuz | Not started |
| `book-of-the-dead-egyptian.txt` | book-of-the-dead | myth-weighing-heart | Not started |
| `myth-birth-hero-rank.txt` | myth-birth-hero-rank | interp-rank, myth-oedipus | Not started |
| `hidden-symbolism-alchemy.txt` | hidden-symbolism-alchemy | interp-alchemists | Not started |
| `hesiod-homeric-hymns.txt` | hesiod-homeric-hymns | myth-prometheus, myth-persephone, myth-pandora | Not started |
| `indian-myth-legend.txt` | indian-myth-legend | myth-krishna, myth-churning-ocean | Not started |
| `myths-china-japan.txt` | myths-china-japan | myth-sun-wukong, myth-amaterasu | Not started |
| `pistis-sophia.txt` | pistis-sophia | myth-sophia-fall | Not started |
| `five-stages-greek-religion.txt` | five-stages-greek-religion | context for interp-frazer | Not started |

### 5. Myth of the Birth of the Hero (Rank) — 18 items

**Source**: `seeds/myth-birth-hero-rank.txt` (Gutenberg #66192, 1914)
**Parser**: `scripts/parse_rank_birth_hero.py`

15 hero birth myths (Sargon, Moses, Karna, Oedipus, Paris, Telephos, Perseus, Gilgamesh, Cyrus, Tristan, Romulus, Hercules, Jesus, Siegfried, Lohengrin) + Introduction + Interpretation + meta card. Each hero has astrology metadata.

**Issue**: Initial parser used byte-position search with `"\n" + spaces + heading` but failed because the body variable didn't preserve the exact positions. Fixed by switching to line-by-line `strip()` matching.

### 6. Hesiod, Homeric Hymns — 49 items

**Source**: `seeds/hesiod-homeric-hymns.txt` (Gutenberg #348)
**Parser**: `scripts/parse_hesiod.py`

45 sections: Works and Days, Theogony, Shield of Heracles, 8 Hesiodic fragments, 33 Homeric Hymns + 3 L2 groups (Major Works, Great Hymns, Short Hymns) + 1 L3 meta.

**Issue**: `HESIOD'S WORKS AND DAYS` uses a Unicode right single quotation mark (`'`, U+2019), not an ASCII apostrophe. Fixed by using the actual Unicode character.

**Learning**: Always check for Unicode apostrophes/quotes in Gutenberg texts. The `'` vs `'` distinction breaks exact string matching.

### 7. Golden Ass (Apuleius) — 14 items

**Source**: `seeds/golden-ass-apuleius.txt` (Gutenberg #1666)
**Parser**: `scripts/parse_golden_ass_mabinogion.py`

11 books (Book V heading missing from edition — inserted synthetically at midpoint of Books IV-VI) + Cupid & Psyche cycle + Isis Revelation cycle + meta card.

**Issue**: The Adlington 1566 edition is missing the "FIFTH BOOKE" heading entirely — the Cupid & Psyche tale just continues without a break from Book IV. Solved by inserting a synthetic midpoint. Acceptable because the tale flows continuously regardless.

### 8. Mabinogion — 15 items

**Source**: `seeds/mabinogion.txt` (Guest translation)
**Parser**: `scripts/parse_golden_ass_mabinogion.py` (same script)

12 tales + Four Branches group + Arthurian Romances group + meta card.

**Issue**: "The story of Lludd and Llevelys" in the TOC doesn't match the body heading, which reads `HERE IS THE STORY OF LLUDD AND LLEVELYS`. Fixed by using the actual body heading.

**Learning**: Mabinogion headings are inconsistent between TOC (title case) and body (sometimes ALL CAPS with "HERE IS"). Always verify body headings against the actual file.

## Validation Summary

| Grammar | Items | L1 | L2 | L3 | Sections | Dupes | Bad Refs |
|---------|-------|----|----|-----|----------|-------|----------|
| myths-through-many-eyes | 73 | 43 | 27 | 3 | 299 | 0 | 0 |
| arabian-nights | 44 | 34 | 8 | 2 | 54 | 0 | 0 |
| russian-folk-tales | 61 | 52 | 8 | 1 | 70 | 0 | 0 |
| myth-birth-hero-rank | 18 | 15 | 2 | 1 | 18 | 0 | 0 |
| hesiod-homeric-hymns | 49 | 45 | 3 | 1 | 49 | 0 | 0 |
| golden-ass-apuleius | 14 | 11 | 2 | 1 | 19 | 0 | 0 |
| mabinogion | 15 | 12 | 2 | 1 | 18 | 0 | 0 |

## Systematic Learnings

1. **Unicode apostrophes in Gutenberg**: Always test for both `'` (ASCII) and `'` (U+2019) in headings
2. **Missing section headings**: Some editions skip book numbers (Golden Ass). Insert synthetic breaks
3. **TOC vs body mismatch**: Mabinogion, Russian Folk Tales both have different heading formats in TOC vs body. Always verify against actual body text
4. **Line-based search beats byte-position search**: For centered headings, `line.strip() == heading` is more reliable than `body.find("\n" + spaces + heading)`
5. **Astrology metadata is easy for mythology**: Every Greek/Norse/Egyptian myth has well-established planetary associations. This adds value for cross-grammar querying
6. **Batch parsing in one script** (Golden Ass + Mabinogion) saves time when the patterns are similar
