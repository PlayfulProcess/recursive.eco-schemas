# Dhammapada Grammar Build Plan

Build a complete Dhammapada grammar from the F. Max Müller translation (Project Gutenberg, public domain).
Each of the 26 chapters becomes a batch. Each verse becomes a grammar item.

**Source:** `/sources/Dhammapada`
**Output:** `/schemas/other/dhammapada/grammar.json`
**Grammar type:** `custom`
**Total verses:** 423

## Chapter Checklist

| # | Chapter | Pali Name | Verses | Items | Status |
|---|---------|-----------|--------|-------|--------|
| 1 | The Twin Verses | Yamakavagga | 1–20 | 20 | **Done** |
| 2 | On Earnestness | Appamādavagga | 21–32 | 12 | Pending |
| 3 | Thought | Cittavagga | 33–43 | 11 | Pending |
| 4 | Flowers | Pupphavagga | 44–59 | 16 | Pending |
| 5 | The Fool | Bālavagga | 60–75 | 16 | Pending |
| 6 | The Wise Man | Paṇḍitavagga | 76–89 | 14 | Pending |
| 7 | The Venerable (Arhat) | Arahantavagga | 90–99 | 10 | Pending |
| 8 | The Thousands | Sahassavagga | 100–115 | 16 | Pending |
| 9 | Evil | Pāpavagga | 116–128 | 13 | Pending |
| 10 | Punishment | Daṇḍavagga | 129–145 | 17 | Pending |
| 11 | Old Age | Jarāvagga | 146–156 | 11 | Pending |
| 12 | Self | Attavagga | 157–166 | 10 | Pending |
| 13 | The World | Lokavagga | 167–178 | 12 | Pending |
| 14 | The Buddha | Buddhavagga | 179–196 | 18 | Pending |
| 15 | Happiness | Sukhavagga | 197–208 | 12 | Pending |
| 16 | Pleasure | Piyavagga | 209–220 | 12 | Pending |
| 17 | Anger | Kodhavagga | 221–234 | 14 | Pending |
| 18 | Impurity | Malavagga | 235–255 | 21 | Pending |
| 19 | The Just | Dhammaṭṭhavagga | 256–272 | 17 | Pending |
| 20 | The Way | Maggavagga | 273–289 | 17 | Pending |
| 21 | Miscellaneous | Pakiṇṇakavagga | 290–305 | 16 | Pending |
| 22 | The Downward Course | Nirayavagga | 306–319 | 14 | Pending |
| 23 | The Elephant | Nāgavagga | 320–333 | 14 | Pending |
| 24 | Thirst | Taṇhāvagga | 334–359 | 26 | Pending |
| 25 | The Bhikshu | Bhikkhuvagga | 360–382 | 23 | Pending |
| 26 | The Brahmana | Brāhmaṇavagga | 383–423 | 41 | Pending |

## Item Structure

Each verse maps to one grammar item:

```json
{
  "id": "dhp-001",
  "name": "Verse 1 – The Wheel of Suffering",
  "symbol": "☸",
  "category": "twin-verses",
  "sort_order": 1,
  "sections": {
    "Verse": "Full Müller translation text",
    "Interpretation": "Contemplative meaning for reflection",
    "Reversed": "Shadow / challenge reading"
  },
  "keywords": ["mind", "karma", "suffering"],
  "questions": ["Reflective prompt for the reader"],
  "metadata": {
    "verse_number": 1,
    "chapter": 1,
    "chapter_name": "The Twin Verses",
    "pali_name": "Yamakavagga",
    "translator": "F. Max Müller"
  }
}
```

## Category Roles

Each chapter maps to a `card` role so all items appear in Flow:

```
"twin-verses": "card",
"earnestness": "card",
"thought": "card",
...
```

## Image Strategy

- Use Wikimedia Commons `Special:FilePath/FILENAME` URLs (stable redirects)
- One cover image for the grammar (verified Buddhist manuscript art)
- Per-verse images where a strong public-domain match exists
- Prefer: Ajanta murals, Gandhara sculpture, Thai/Burmese manuscripts, museum Buddhist art
- Every URL must be manually verified before committing

## Attribution

- Source: Project Gutenberg eBook #2017
- Translator: F. Max Müller (1881, The Sacred Books of the East Vol. X)
- License: Public Domain
