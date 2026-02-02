# A Violent History of Benevolence: The Deck

A 55-card tarot deck examining interlocking oppressions in social work history, enriched with indigenous wisdom, spiritual practices, and contemporary voices.

## About This Project

This deck began as a Social Work program project to examine the "standard account" of social work history through the lens of Chapman & Withers' critical scholarship. It evolved into something larger: a deck that holds both the violent history and the cracks where something else lives.

### Core Principle

**All figures are complicit.** This project does not make moral judgments or divide figures into "good" vs "bad" categories. Everyone named—whether celebrated founders or erased resisters—participated in interlocking systems of oppression. The deck invites reflection on complicity rather than identification with innocence.

As Bayo Akomolafe says: *"There are always cracks in the systems."* And: *"Decolonization might be more about grandmothers than about systems."*

## How the Deck Was Built

### Phase 1: Initial Extraction (40 figures)

The initial 40 names were systematically extracted from:
- **Chapman, Chris & Withers, A.J. (2019).** *A Violent History of Benevolence: Interlocking Oppression in the Moral Economies of Social Working.* University of Toronto Press.
- Specifically Chapter 1: "Troubling the Standard Account of Social Work"

This produced figures from both the "standard account" (Jane Addams, Mary Richmond, etc.) and those erased from it (Ida B. Wells, Claudette Colvin, etc.).

### Phase 2: Recognizing What the Book Excludes

The source text itself acknowledges its limitations—it centers a critique of white social work history but does not fully address Indigenous perspectives or non-Western forms of community care.

In recognition of this, the deck was expanded to include:

**Contemporary Decolonial Voices (6 cards):**
- Bayo Akomolafe (post-activist philosophy, "slowing down")
- Vanessa Andreotti (hospicing modernity, GTDF collective)
- Josh Shrei (The Emerald podcast, ancestral medicine)
- Sam Harris (secular meditation, contradictions)
- Neil deGrasse Tyson (science communication)
- Luiza Lian (Brazilian ancestral music)

**"The Cracks" - Roles Beyond the Standard Account (9 cards):**
- The Grandmother, The Mother, The Friend, The Doula
- Preto Velho (Umbanda elder spirit)
- Caboclo (Indigenous ancestral spirit in Umbanda)
- Pai de Santo / Mãe de Santo (Candomblé/Umbanda priesthood)
- The Neighbor Who Brings Food
- The Child Who Asks Why

### Phase 3: Structure

The final 55-card deck is organized into four suits:

| Suit | Cards | Description |
|------|-------|-------------|
| **standard_account** | 17 | Canonical social work figures |
| **erased_voices** | 23 | Marginalized figures from the book |
| **the_cracks** | 9 | Indigenous wisdom, spiritual practices, everyday roles |
| **contemporary_witnesses** | 6 | Those doing "social working" differently today |

### Not a 1-1 Mapping

Unlike traditional tarot, this deck does not assign one figure per Major Arcana card. Instead, each card has **archetypal resonances**—multiple tarot archetypes that might apply. This reflects the source text's insistence that there is no clean binary, no "other side of the river" to cross to.

## Current Status

| Phase | Status | Output |
|-------|--------|--------|
| Name Extraction | Complete | 40 figures from Chapter 1 |
| Deck Expansion | Complete | +15 cards (contemporary voices, the cracks) |
| Grammar Schema | Complete | `grammar.json` (55 cards) |
| Wikimedia Images | Complete | ~25 public domain portraits |
| Pytrends Script | Available | `scripts/fetch_trends.py` (run locally) |

## Repository Structure

```
anti-opressive-major-arcana/
├── README.md                 # This file
├── PROJECT_PLAN.md           # Original implementation plan
├── outline.md                # Source chapters and project notes
├── grammar.json              # Complete 55-card deck for recursive.eco
├── data/
│   ├── names-extracted.json  # Initial 40 figures
│   ├── visibility-raw-data.json
│   ├── weighted-scores.json
│   └── intersectional-metadata.json
├── cards/
│   └── major-arcana-assignments.json
└── scripts/
    └── fetch_trends.py       # Google Trends data collection
```

## Sources

### Primary Source
- Chapman, C., & Withers, A. J. (2019). *A Violent History of Benevolence: Interlocking oppression in the moral economies of social working.* University of Toronto Press.

### Theoretical Framework
- Spivak, G. C. on "persistent dredging operations" and complicity
- Ahmed, S. on how racism shapes surfaces of bodies and worlds
- The concept of "analeptic thinking"—holding contradiction while manifesting alternative narratives

### Professional Context
- NASW (2021) apology for the profession's role in supporting policies that harmed people of colour
- CSWE Statement on Accountability

## Ethical Considerations

This project acknowledges its own limitations:

1. **Colonial limitations**: This deck centers a decolonial critique but is itself colonial in that it does not fully address Indigenous accounts and perspectives.

2. **No innocent position**: The project refuses to offer users a comfortable "other side of the river" to identify with. Following the source text's critique, there is no clean separation between oppressors and resisters—only tributaries of the same river.

3. **Analeptic thinking**: The deck practices what the sources call "analeptic thinking"—holding the contradiction of white-dominated history while manifesting a different, non-majoritarian narrative, without synthesizing them into a comfortable "diverse" whole.

## Use of AI in This Project

This project is developed collaboratively with **Claude** (Anthropic's AI assistant, specifically Claude Opus 4.5) using **Claude Code** (CLI tool).

### What AI contributed:
- Systematic extraction of names from source text
- Structuring the project plan and methodology
- Creating JSON schemas and data structures
- Documentation and README creation
- Git workflow management

### What remains human:
- Conceptual framework and critical analysis
- Source material selection and interpretation
- Final card assignments and meanings
- Ethical judgments about representation
- Academic context and Social Work program requirements

### Transparency
All AI-assisted work is tracked through git commits that include session links. This allows full transparency about which parts of the project involved AI collaboration.

The use of AI in this project is itself a point of reflection: AI systems are trained on data that reflects existing power structures and visibility biases—the very biases this project seeks to invert.

## How to Use This Deck (Future)

The completed deck will be available as a JSON schema compatible with [recursive.eco](https://recursive.eco), enabling:
- Digital card pulls with critical historical context
- Reflection prompts connecting card meanings to social work practice
- Pivot table analysis of representation across categories

## Image Credits

All portrait images are sourced from **Wikimedia Commons** under public domain or Creative Commons licenses:

| Figure | Image Source | License |
|--------|--------------|---------|
| Jane Addams | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Jane_Addams_profile.jpg) | Public Domain |
| Mary Richmond | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Mary_Ellen_Richmond.jpg) | Public Domain |
| Ida B. Wells | Mary Garrity, via [Google Art Project](https://commons.wikimedia.org/wiki/File:Mary_Garrity_-_Ida_B._Wells-Barnett_-_Google_Art_Project_-_restoration_crop.jpg) | Public Domain |
| W.E.B. Du Bois | James E. Purdy, 1907, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:W.E.B._Du_Bois_by_James_E._Purdy,_1907.jpg) | Public Domain |
| Frederick Douglass | c. 1840s, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Frederick_Douglass_(1840s).jpg) | Public Domain |
| Rosa Parks | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Rosaparks.jpg) | Public Domain |
| Malcolm X | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Malcolm_X_NYWTS_4.jpg) | Public Domain |
| Martin Luther King Jr | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Martin_Luther_King,_Jr..jpg) | Public Domain |
| James Baldwin | Allan Warren, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:James_Baldwin_37_Allan_Warren_(cropped).jpg) | CC BY-SA 3.0 |
| Bayard Rustin | 1963, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Bayard_Rustin_1963.jpg) | Public Domain |
| Gandhi | 1931, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Mahatma-Gandhi,_studio,_1931.jpg) | Public Domain |
| Emma Goldman | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Emma_Goldman_seated.jpg) | Public Domain |
| Theodore Roosevelt | Pach Bros., [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:President_Roosevelt_-_Pach_Bros.jpg) | Public Domain |
| Booker T. Washington | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Booker_T_Washington_retouched_flattened-crop.jpg) | Public Domain |
| Neil deGrasse Tyson | 2017, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Neil_deGrasse_Tyson_in_June_2017_(cropped).jpg) | CC BY 2.0 |

Cards without images include very low-visibility historical figures (no known portraits), archetypal roles (The Grandmother, The Doula), and some contemporary figures.

## License

Content: **CC-BY-SA-4.0**

Images: See individual credits above. Most are public domain; some require attribution under Creative Commons.

## Contact

[TBD]

---

*"The mainstream has never run clean, perhaps never can. Part of mainstream education involves learning to ignore this absolutely, with a sanctioned ignorance."* — Gayatri Spivak

*"The times are urgent; let us slow down."* — Bayo Akomolafe
