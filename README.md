# recursive.eco Grammar Commons

A commons for symbolic systems — tarot decks, I Ching interpretations, astrology sets, sequences, and anything else you want to contemplate.

These grammars work with [recursive.eco](https://recursive.eco). Anyone can create, fork, and share them.

## Quick Start

The fastest way to create a grammar:

1. **Experience one first** — Go to [flow.recursive.eco](https://flow.recursive.eco), draw a card or cast a hexagram
2. **Copy it** — Click "Copy to My Grammars" on any grammar you like
3. **Edit** — Change the interpretations to match your perspective
4. **Export** — Use "Export to Commons" to get the JSON

Or, to create from scratch or from a source text, see the [AI-assisted creation guide](#creating-grammars-with-ai) below.

## Repository Structure

```
schemas/
├── tarot/              # Tarot decks
├── iching/             # I Ching interpretation books
├── astrology/          # Astrology interpretation sets
└── other/              # Everything else

sequences/              # Ordered video/image collections
custom/                 # User-created grammars of any type
creators/               # UUID-based user folders
sources/                # Public domain source materials & attribution
```

## Grammar JSON Format

Every grammar is a JSON file with this structure:

```json
{
  "_grammar_commons": {
    "schema_version": "1.0",
    "license": "CC-BY-SA-4.0",
    "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    "attribution": [
      { "name": "Your Name", "date": "2026-01-29", "note": "Original creator" }
    ]
  },
  "name": "My Grammar",
  "description": "What this grammar offers",
  "grammar_type": "tarot",
  "creator_name": "Your Name",
  "tags": ["tag1", "tag2"],
  "cover_image_url": "https://...",
  "items": [...]
}
```

### Grammar Type

`grammar_type` determines how Flow renders your grammar when someone uses it for a reading.

| Value | Flow renders it as | Notes |
|-------|-------------------|-------|
| `"tarot"` | Card oracle — draw cards, get interpretations | Expects card-style items |
| `"iching"` | Hexagram oracle — coin toss, changing lines | Expects 64 hexagrams with line data |
| `"astrology"` | Birth chart integration | Expects planets, signs, houses |
| `"custom"` | Sequence/general viewer | No oracle integration, browse only |

If you set `grammar_type: "iching"` but your grammar doesn't have 64 hexagrams with line data, the I Ching oracle won't work. Match the type to your content.

### Items

Each item in the `items` array represents one element — a card, hexagram, planet, video, chapter, etc.

```json
{
  "id": "the-fool",
  "name": "The Fool",
  "symbol": "🃏",
  "sort_order": 0,
  "category": "major_arcana",
  "level": 1,
  "sections": {
    "Interpretation": "The beginning of all journeys...",
    "Reversed": "Fear of the unknown...",
    "Summary": "Innocence, new beginnings"
  },
  "keywords": ["beginning", "innocence", "leap"],
  "questions": ["What would you do if you weren't afraid?"],
  "quotes": ["The journey of a thousand miles begins with a single step"],
  "image_url": "https://upload.wikimedia.org/...",
  "metadata": {}
}
```

**Required fields:**
- `id` — Unique, lowercase, hyphenated (e.g., `"the-fool"`, `"hexagram-01"`, `"sun"`)
- `name` — Display name
- `sort_order` — Position in sequence (0, 1, 2...)
- `sections` — Object with string key-value pairs for all content

**Optional fields:**
- `symbol` — Unicode character (♈, ☰, ☉, etc.)
- `category` — Grouping label (see [Categories](#categories) below)
- `level` — 1 for base items, 2+ for emergences (default: 1)
- `keywords` — Array of strings
- `questions` — Reflective prompts
- `quotes` — Short quotes (max 125 chars each, auto-formatted with quotation marks in viewers)
- `image_url` — Direct URL to image (Wikimedia Commons works best)
- `metadata` — Object for structured data (numbers, booleans, short strings)

### Sections — What Flow Actually Reads

Sections are flexible — you can add any key you want and the viewer will display it. But Flow's oracle components look for **specific keys** to populate dedicated UI elements.

**Tarot grammars:**

| Section Key | Used For |
|------------|----------|
| `Interpretation` | Main card meaning (falls back to `Summary`) |
| `Summary` | Brief overview, shown as subtitle |
| `Reversed` | Reversed meaning |
| Any other key | Displayed as additional sections in detail view |

Flow also highlights sections with "affirmation" or "question" in the title with special formatting.

**I Ching grammars:**

| Section Key | Used For |
|------------|----------|
| `Judgment` | The Judgment text |
| `Image` | The Image text |
| `Interpretation` | Overall meaning (falls back to `Core Meaning`) |

**For I Ching line readings**, Flow supports three formats (checked in this order):

1. **`lines` property** (preferred) — structured object on the item:
   ```json
   {
     "id": "hexagram-01",
     "lines": {
       "1": "Hidden dragon. Do not act.",
       "2": "Dragon appearing in the field.",
       "3": "The superior person is active all day.",
       "4": "Wavering flight over the depths.",
       "5": "Flying dragon in the heavens.",
       "6": "Arrogant dragon will have cause to repent."
     }
   }
   ```
2. **`lines` as array** — `[{ "position": 1, "meaning": "..." }, ...]`
3. **`Lines` section** (fallback) — a single text block parsed via regex:
   ```json
   "sections": {
     "Lines": "Line 1: Hidden dragon. Do not act.\nLine 2: Dragon appearing in the field.\n..."
   }
   ```

**Important:** Individual section keys like `"Line 1"`, `"Line 2"` etc. will display in the grammar viewer but will **NOT** be available in Flow's I Ching changing line feature. Use the `lines` property or the combined `Lines` section format above.

**Astrology grammars:**

| Section Key | Viewer Maps To |
|------------|----------------|
| `Interpretation`, `Description`, `Story`, `Meaning`, `Summary` | Main description |
| `Shadow` | Shadow expression |
| `Light` | Light expression |
| `Archetype`, `Nature` | Archetypal description |
| `Karakatvas`, `Significations` | Significations |
| `Affirmation`, `Mantra` | Affirmation/practice |
| `Questions` | Reflective prompts |
| `Invitation` | Invitation text |

### Categories

Categories group items within a grammar (e.g., "major_arcana" vs "minor_arcana", "planet" vs "sign").

**For tarot and I Ching:** Categories are informational only. The viewers display them as filter pills but don't change rendering behavior.

**For astrology:** Categories control how the viewer sorts items into sections (planets tab, signs tab, houses tab). The astrology viewer maps category names to roles:

| Category Name | Viewer Role | Where It Appears |
|--------------|-------------|------------------|
| `planet` | planet | Planets tab |
| `sign` | sign | Signs tab |
| `house` | house | Houses tab |
| `aspect` | emergence | Yogas/Aspects tab |
| `graha` | planet | Planets tab (Vedic) |
| `rashi` | sign | Signs tab (Vedic) |
| `bhava` | house | Houses tab (Vedic) |
| `nakshatra` | nakshatra | Nakshatras tab (Vedic) |
| `yoga`, `drishti` | emergence | Yogas/Aspects tab |

**Custom category mappings:** If you use non-standard category names, add `_category_roles` at the grammar root:

```json
{
  "_category_roles": {
    "my-custom-planet-name": "planet",
    "my-custom-sign-name": "sign"
  }
}
```

### Emergence Levels

Items can have levels representing layers of meaning:

- **Level 1** — Base items (a card, a planet, a hexagram)
- **Level 2** — Emergent combinations (a spread, a yoga, an aspect)
- **Level 3** — Meta-categories (organizing principles across L2 items)

```json
{
  "id": "sun-in-aries",
  "name": "Sun in Aries",
  "level": 2,
  "composite_of": ["sun", "aries"],
  "category": "placement",
  "sections": {
    "Interpretation": "The pioneer spirit..."
  }
}
```

L2 items must include `composite_of` — an array of IDs referencing the items they combine. These IDs must exist in the grammar.

All levels are displayed in the grammar viewer with level badges (L2, L3). Users can filter by level.

### Metadata vs Sections

**Sections** are for longer text content — interpretations, stories, meanings, commentary.

**Metadata** is for brief, structured data — numbers, dates, booleans, short identifiers.

```json
{
  "sections": {
    "Interpretation": "A long interpretation paragraph...",
    "Commentary": "Additional scholarly notes..."
  },
  "metadata": {
    "number": 1,
    "element": "fire",
    "planet": "mars",
    "chinese_name": "乾",
    "pinyin": "Qián",
    "trigram_above": "heaven",
    "trigram_below": "heaven",
    "youtube_video_id": "abc123",
    "duration_seconds": 180
  }
}
```

**Reserved field names** — Don't use these as section or metadata keys: `id`, `name`, `symbol`, `category`, `keywords`.

### Vedic Astrology Grammars

Include `english_name` in metadata for cross-tradition lookup:

```json
{
  "id": "surya",
  "name": "सूर्य (Surya)",
  "category": "graha",
  "metadata": {
    "english_name": "Sun"
  }
}
```

This lets the astrology viewer match Vedic items to Western chart positions.

## Creating Grammars with AI

The most effective workflow for creating grammars from source texts uses two tools together:

### 1. NotebookLM — Understand Your Source

[NotebookLM](https://notebooklm.google.com/) is Google's research assistant. It only uses sources you provide — no hallucination from training data.

1. Upload your source (PDF, text, URL) to a new notebook
2. Ask it to analyze the structure: "How is this text organized? What patterns repeat?"
3. Extract themes, categories, and section structure before generating JSON
4. Use the Audio Overview feature to hear a summary — it catches patterns you might miss

### 2. Claude Code — Generate the Grammar

[Claude Code](https://claude.ai/code) generates JSON files that follow the grammar format.

1. Fork this repository on GitHub
2. Open your fork in Claude Code
3. Point Claude to an existing grammar as a format reference
4. Provide your source text and ask it to generate in batches of 10-20 items

**Example prompt for a tarot deck:**

```
I have the text of "The Pictorial Key to the Tarot" by A.E. Waite.
Create a tarot grammar with all 78 cards.

For each card include:
- id, name, sort_order
- image_url from Wikimedia Commons (Rider-Waite deck)
- sections: Interpretation, Reversed, Summary
- keywords array

Start with the Major Arcana (22 cards).
Follow the format in schemas/tarot/rider-waite-recursive/grammar.json.
```

**Example prompt for I Ching:**

```
Create an I Ching grammar with all 64 hexagrams.

For each hexagram include:
- id (hexagram-01 through hexagram-64), name, symbol (Unicode hexagram)
- sections: Judgment, Image, Interpretation
- lines property with readings for all 6 lines
- metadata: number, chinese_name, pinyin, trigram_above, trigram_below

Work in batches of 8 hexagrams. Follow the format in schemas/iching/summary-ai.
```

**Tips:**
- Always reference an existing grammar for format ("follow the format in...")
- Batch 10-20 items at a time for reliability
- Review each batch before continuing
- Use [Wikimedia Commons](https://commons.wikimedia.org/) for images (direct `upload.wikimedia.org` URLs)
- Validate JSON at [jsonlint.com](https://jsonlint.com/) before importing

For a full walkthrough, see the [Create Grammars with AI](https://recursive.eco/pages/courses/course-viewer.html?course=create-grammars-with-ai) course.

## Viewing Your Grammar

### In the Browser Viewer

Test your grammar directly from GitHub:

```
recursive.eco/pages/grammar-viewer.html?github=YOUR-USERNAME/recursive.eco-schemas/path/to/grammar
```

Short path (this repo):
```
recursive.eco/pages/grammar-viewer.html?github=tarot/rider-waite
```

### Import to Your Account

1. Go to [offer.recursive.eco](https://offer.recursive.eco)
2. Click "New Grammar"
3. Use Import with your GitHub URL
4. Save as draft or publish

## Contributing

1. Fork this repository
2. Create your grammar in the appropriate folder
3. Test with the viewer URL above
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Validation Checklist

Before submitting:

- [ ] Valid JSON (no trailing commas, unclosed brackets)
- [ ] Every item has a unique `id`
- [ ] All `composite_of` references point to existing item IDs
- [ ] `grammar_type` matches your content
- [ ] I Ching grammars: line data in `lines` property (not just individual section keys)
- [ ] Attribution metadata included
- [ ] File size under 1MB
- [ ] UTF-8 encoding

## Philosophy

- **Open Knowledge** — Symbolic systems belong to everyone
- **Community Care** — Credit sources and traditions
- **Respectful Practice** — Honor the cultural roots of these systems
- **Recursive Growth** — The people who use the infrastructure maintain and transform it

## License

CC-BY-SA-4.0 — Share alike with attribution.
