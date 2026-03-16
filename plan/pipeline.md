# Grammar Pipeline

A roadmap of grammars to build, organized by type. Each entry includes source status, estimated effort, and (for classics) a terminal prompt to download and catalogue the source.

---

## FROM MEMORY — Knowledge & Taxonomy Grammars

These grammars are built from structured knowledge, not source texts. They require editorial planning and hand-crafted content. High effort, high originality.

### The Human Body — Atoms to Organism
- **Concept**: Recursive structure of the human body across scales
- **Hierarchy**: L1 = atoms/molecules → L2 = organelles → L3 = cells → L4 = tissues → L5 = organs → L6 = organ systems → L7 = organism
- **Items est.**: ~200-300
- **Status**: NOT STARTED
- **Notes**: This is a natural "emergence" grammar — each level genuinely emerges from the level below. Could include sections like "What It Does", "Made Of", "Fun Fact". Start with a simplified 4-level version (molecules → cells → organs → systems) and expand.

### Cultures of the World
- **Concept**: Cultural traditions, practices, and worldviews across civilizations
- **Hierarchy**: L1 = specific practices/traditions → L2 = cultural domains (art, food, music, ritual) → L3 = civilizations/regions
- **Items est.**: ~150-200
- **Status**: NOT STARTED
- **Notes**: Sensitive content — needs careful, respectful framing. Focus on living cultures with verified information. Could start with 10-15 cultures.

### Language Family Trees
- **Concept**: The world's language families as a recursive tree
- **Hierarchy**: L1 = individual languages → L2 = language branches → L3 = language families → L4 = macro-families (controversial)
- **Items est.**: ~200-400
- **Status**: NOT STARTED
- **Notes**: Well-documented taxonomy. Start with Indo-European (largest, best documented) and expand. Could include sample phrases, speaker counts, writing systems.

### World Religions Tree
- **Concept**: Major world religions, their branches, and key texts/practices
- **Hierarchy**: L1 = texts/practices/concepts → L2 = denominations/schools → L3 = major religions
- **Items est.**: ~150-250
- **Status**: NOT STARTED
- **Notes**: Very sensitive — needs balanced, respectful treatment. Start with the "big 5" (Christianity, Islam, Judaism, Hinduism, Buddhism) and expand to include indigenous/traditional religions.

### Jungian Archetypes
- **Concept**: Carl Jung's archetypal framework
- **Hierarchy**: L1 = specific archetypal manifestations → L2 = the 12 primary archetypes → L3 = the Self/Shadow/Anima/Animus meta-structure
- **Items est.**: ~60-80
- **Status**: NOT STARTED
- **Notes**: Well-structured domain. Could cross-reference with existing tarot grammars (Major Arcana map to archetypes). Jung's work is in public domain in some jurisdictions.

### Periodic Table of Elements
- **Concept**: Chemical elements organized by properties
- **Hierarchy**: L1 = individual elements → L2 = element groups (noble gases, alkali metals, etc.) → L3 = periods/blocks
- **Items est.**: ~140 (118 elements + groups + periods)
- **Status**: NOT STARTED
- **Notes**: Perfect "from-memory" grammar — well-defined taxonomy, factual content, no copyright issues.

---

## FROM CLASSICS — Public Domain Source Texts

These grammars are parsed from source text files. They require downloading, cataloguing, and parsing. Medium effort, high fidelity.

### Children's Books (Public Domain)

All titles below are confirmed public domain in the US. Source: Project Gutenberg.

| Title | Author | Year | PD Since | Gutenberg # | Status |
|-------|--------|------|----------|-------------|--------|
| Alice's Adventures in Wonderland | Lewis Carroll | 1865 | Always | #11 | DONE |
| Through the Looking-Glass | Lewis Carroll | 1871 | Always | #12 | TODO |
| Winnie-the-Pooh | A. A. Milne | 1926 | 2022 | #67098 | DONE |
| The House at Pooh Corner | A. A. Milne | 1928 | 2024 | — | TODO |
| Peter Pan (Peter and Wendy) | J. M. Barrie | 1911 | Always | #16 | TODO |
| The Wonderful Wizard of Oz | L. Frank Baum | 1900 | Always | #55 | TODO |
| The Jungle Book | Rudyard Kipling | 1894 | Always | #236 | TODO |
| Just So Stories | Rudyard Kipling | 1902 | Always | #2781 | TODO |
| The Wind in the Willows | Kenneth Grahame | 1908 | Always | #289 | TODO |
| Pinocchio | Carlo Collodi | 1883 | Always | #500 | TODO |
| Heidi | Johanna Spyri | 1881 | Always | #1448 | TODO |
| Black Beauty | Anna Sewell | 1877 | Always | #271 | TODO |
| The Secret Garden | F. H. Burnett | 1911 | Always | #113 | TODO |
| A Little Princess | F. H. Burnett | 1905 | Always | #146 | TODO |
| Anne of Green Gables | L. M. Montgomery | 1908 | Always | #45 | TODO |
| The Little Prince | Saint-Exupery | 1943 | 2019 (FR) | — | CHECK (US status complex) |
| Charlotte's Web | E. B. White | 1952 | NOT YET | — | WAIT (2048) |
| Where the Wild Things Are | M. Sendak | 1963 | NOT YET | — | WAIT (2059) |

#### Download prompt
```bash
# Run this in terminal to download and catalogue a children's book from Gutenberg:
# Replace BOOK_NUM with the Gutenberg eBook number (e.g., 16 for Peter Pan)

BOOK_NUM=16
BOOK_NAME="peter-pan"
curl -sL "https://www.gutenberg.org/cache/epub/${BOOK_NUM}/pg${BOOK_NUM}.txt" \
  -o "sources/${BOOK_NAME}" && \
  wc -l "sources/${BOOK_NAME}" && \
  head -30 "sources/${BOOK_NAME}"
```

---

### Folk Tales & Indigenous Stories

| Collection | Source | Language | Status | Notes |
|------------|--------|----------|--------|-------|
| Aesop's Fables | Gutenberg #11339 | English | TODO | 300+ fables, very short each — perfect L1 items |
| Grimm's Fairy Tales | Gutenberg #2591 | English | TODO | 200+ tales, well-structured |
| 1001 Nights (Arabian Nights) | Gutenberg #3435-3440 | English (Burton) | TODO | Frame narrative + nested stories |
| Panchatantra (Indian fables) | Gutenberg #25545 | English | TODO | 5 books of animal fables, similar to Aesop |
| Jataka Tales (Buddhist) | Gutenberg #20564 | English | TODO | 547 birth stories of the Buddha |
| Norse Myths (Edda) | Gutenberg #14726 | English | TODO | Poetic Edda, public domain |
| African Folk Tales | sacred-texts.com | English | TODO | Multiple collections available |
| Native American Legends | sacred-texts.com | English | CHECK | Sensitivity review needed — many are sacred, not just "stories" |
| Japanese Folk Tales | Gutenberg #4018 | English | TODO | "Japanese Fairy Tales" by Yei Theodora Ozaki |
| Celtic Fairy Tales | Gutenberg #25198 | English | TODO | Joseph Jacobs collection |
| Italian Popular Tales | Gutenberg #23634 | English | TODO | Thomas Frederick Crane (Cornell, 1885). Drew from the same 19th-century collectors Calvino later used (Pitrè, Comparetti, Nerucci, Imbriani). The closest English-language precursor to Calvino's *Fiabe italiane*. 96+ tales organized by type. |
| Stories from the Pentamerone | Gutenberg #2198 | English | TODO | Giambattista Basile (1634), trans. John Edward Taylor. The *earliest* European fairy-tale collection — Sleeping Beauty, Cinderella, Rapunzel all appear here 200 years before Grimm claimed them as German. Neapolitan dialect original. The ur-source. |
| La Novellaja Fiorentina | Gutenberg #46898 | Italian | TODO | Vittorio Imbriani (1871-1877). Florentine folktales stenographed from oral telling. Direct Calvino source. Italian only — no public domain English translation exists. |

#### Download prompt
```bash
# Download Aesop's Fables:
curl -sL "https://www.gutenberg.org/cache/epub/11339/pg11339.txt" \
  -o "sources/aesops-fables" && \
  wc -l "sources/aesops-fables" && \
  head -30 "sources/aesops-fables"

# Download Grimm's Fairy Tales:
curl -sL "https://www.gutenberg.org/cache/epub/2591/pg2591.txt" \
  -o "sources/grimms-fairy-tales" && \
  wc -l "sources/grimms-fairy-tales" && \
  head -30 "sources/grimms-fairy-tales"
```

---

### Sacred & Philosophical Texts

| Text | Source | Status | Notes |
|------|--------|--------|-------|
| Confucian Analects | sources/confucius | DONE | 749 items |
| Dhammapada | sources/Dhammapada | DONE (431 items) | Buddhist verses, 405 numbered verses in 26 chapters |
| Zohar | sources/zohar | BLOCKED — source empty | Needs Sefaria or sacred-texts.com download |
| Tao Te Ching | Gutenberg #216 | TODO | 81 chapters, very clean structure |
| Bhagavad Gita | sacred-texts.com | TODO | 18 chapters, verse-numbered |
| Meditations (Marcus Aurelius) | Gutenberg #2680 | TODO | 12 books of Stoic philosophy |
| The Art of War (Sun Tzu) | Gutenberg #132 | TODO | 13 chapters |
| I Ching | sacred-texts.com | TODO | 64 hexagrams — perfect L1 items with L2 trigram composites |
| Upanishads | sacred-texts.com | TODO | Multiple texts, various translations |
| Rumi (Selected Poems) | Various | CHECK | Public domain status varies by translation |

#### Download prompt
```bash
# Download Tao Te Ching:
curl -sL "https://www.gutenberg.org/cache/epub/216/pg216.txt" \
  -o "sources/tao-te-ching" && \
  wc -l "sources/tao-te-ching"

# Download Meditations:
curl -sL "https://www.gutenberg.org/cache/epub/2680/pg2680.txt" \
  -o "sources/meditations-marcus-aurelius" && \
  wc -l "sources/meditations-marcus-aurelius"

# Download Zohar (from sacred-texts.com, Sperling/Simon translation):
# NOTE: This is a multi-page work — may need scraping
curl -sL "https://www.sacred-texts.com/jud/zdm/index.htm" \
  -o "sources/zohar-index.html" && \
  echo "Check index for individual chapter URLs"
```

---

### Shakespeare & Drama (remaining works)

| Work | Status | Notes |
|------|--------|-------|
| 10 Greatest Plays | DONE | 247 items |
| Sonnets (154) | TODO | Different parser needed — numbered, no ACT/SCENE |
| Remaining 26 plays | TODO | Same parser, just add to target list |
| Longer poems (Venus and Adonis, Lucrece, etc.) | TODO | Single-item L1s or stanza-based |

---

## Priority Order

### Phase 1 — Quick Wins (1-2 sessions each)
1. Through the Looking-Glass (same parser as Alice)
2. Tao Te Ching (81 clean chapters)
3. Aesop's Fables (300 short items, trivial parsing)
4. Peter Pan
5. The Wonderful Wizard of Oz

### Phase 2 — Medium Effort
6. Grimm's Fairy Tales
7. Bhagavad Gita
8. Panchatantra
9. The Jungle Book
10. Remaining Shakespeare plays + Sonnets

### Phase 3 — From Memory (high effort, high value)
11. Jungian Archetypes
12. Human Body (atoms → organism)
13. Periodic Table
14. Language Family Trees

### Phase 4 — Ambitious
15. World Religions Tree
16. Cultures of the World
17. 1001 Nights (complex nested structure)
18. I Ching (64 hexagrams + trigrams)

---

_Last updated: 2026-03-02_
