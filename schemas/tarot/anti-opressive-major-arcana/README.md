# Anti-Oppressive Major Arcana Tarot Deck

A Social Work program project that uses data-driven methodology to create a Major Arcana tarot deck examining the interlocking oppressions in social work history.

## About This Project

This deck extracts historical figures from critical social work scholarship and assigns them to Major Arcana cards using an **inverse visibility metric**. Figures who have been systematically erased from mainstream history receive higher weighting, mathematically centering voices that the "standard account" of social work has marginalized.

### Core Principle

**All figures are complicit.** This project does not make moral judgments or divide figures into "good" vs "bad" categories. Everyone named in the history of social work—whether celebrated founders or erased resisters—participated in interlocking systems of oppression. The deck invites reflection on complicity rather than identification with innocence.

## Methodology

### 1. Name Extraction
Historical figures are extracted from:
- **Chapman, Chris & Withers, A.J. (2019).** *A Violent History of Benevolence: Interlocking Oppression in the Moral Economies of Social Working.* University of Toronto Press.

### 2. Visibility Metrics
Using Google APIs (Trends, Scholar, Search), we quantify each figure's presence in public discourse—measuring both academic citation counts and general search visibility.

### 3. Inverse Weighting Formula
```
Representation Weight (W) = 1 / Visibility Score (V)
```
Lower visibility = higher card ranking. This formula forces the system to prioritize recovery of erased voices.

### 4. Intersectional Metadata
Each figure is tagged with:
- Race
- Gender
- Geographic context
- Era
- Primary domain (settlement houses, COS, civil rights, etc.)

### 5. Card Assignment
The 22 Major Arcana cards are assigned based on:
- Inverse visibility ranking
- Archetypal resonance with the figure's historical role
- Balanced representation across categories

## Current Progress

| Phase | Status | Output |
|-------|--------|--------|
| Name Extraction (Ch. 1) | Complete | 40 figures extracted |
| Name Extraction (Ch. 2) | Pending | - |
| Visibility Metrics | Pending | - |
| Inverse Weighting | Pending | - |
| Card Assignments | Pending | - |
| JSON Schema | Pending | - |

## Repository Structure

```
anti-opressive-major-arcana/
├── README.md                 # This file
├── PROJECT_PLAN.md           # Detailed 7-phase implementation plan
├── outline.md                # Source material and initial project notes
├── data/
│   └── names-extracted.json  # Extracted historical figures
├── cards/                    # (future) Individual card descriptions
└── docs/                     # (future) Methodology and ethics documentation
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

## License

[TBD]

## Contact

[TBD]

---

*"The mainstream has never run clean, perhaps never can. Part of mainstream education involves learning to ignore this absolutely, with a sanctioned ignorance."* — Gayatri Spivak
