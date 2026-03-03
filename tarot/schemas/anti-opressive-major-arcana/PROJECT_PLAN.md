# Anti-Oppressive Major Arcana Tarot Deck - Project Plan

## Project Overview

This is a Social Work program project that combines academic critical analysis with tarot card creation. The deck uses an inverse visibility metric to examine figures from social work history—all of whom are complicit in interlocking systems of oppression. No moral judgments are made; the deck invites reflection on complicity rather than identification with innocence.

### Core Concept
Using an **inverse visibility metric**, this deck mathematically disrupts the "moral economy of white supremacy" by giving Major Arcana status to historically marginalized figures who have been systematically erased from social work's canonical history.

### Source Material
- **Primary Text**: Chapman, Chris; Withers, A.J. (2019). *A Violent History of Benevolence: Interlocking Oppression in the Moral Economies of Social Working*. University of Toronto Press.
- **Chapters to Extract Names From**:
  1. Chapter 1: "Troubling the Standard Account of Social Work"
  2. Chapter 2: (Second chapter from the book)

---

## Phase 1: Name Extraction

### Objective
Systematically extract all named historical figures from the source chapters.

### Tasks
1. [x] Read through Chapter 1 completely and extract all named individuals
2. [ ] Read through Chapter 2 completely and extract all named individuals
3. [x] Create a master list of all extracted names (40 figures from Chapter 1)

### Sample of Extracted Figures (All Complicit)

| Name | Role/Description |
|------|------------------|
| Jane Addams | Settlement house movement, Hull-House founder, eugenics supporter |
| Mary Richmond | COS, "scientific casework", liberal individualism |
| Katherine Bement Davis | Bedford Hills Reformatory, eugenic criminology |
| Richard Henry Pratt | Indian Boarding Schools |
| Albert Rose | Regent Park/Africville relocations |
| Ida B. Wells | Anti-lynching activism, journalism |
| W.E.B. Du Bois | NAACP, activism |
| Maggie L. Walker | St. Luke Bank, financial autonomy |
| Claudette Colvin | Refused bus seat before Rosa Parks |
| Oscar McCulloch | COS leader, The Tribe of Ishmael |

*See `data/names-extracted.json` for complete list of 40 figures.*

### Deliverable
- `names-extracted.json` - Complete list with initial categorization

---

## Phase 2: Visibility Metrics Collection

### Objective
Use Google APIs to quantify the "visibility" of each figure in public discourse.

### Methodology Options
1. **Google Trends API** (via Pytrends) - Search volume over time
2. **Google Scholar Scraper** (via SerpApi) - Academic citation counts
3. **Google Custom Search API** - General web presence

### Recommended Approach
Use **both** Google Scholar (academic erasure) and Google Search (public imagination erasure) to capture different dimensions of visibility.

### Tasks
1. [ ] Set up API access (Pytrends, SerpApi, or Google Custom Search)
2. [ ] Create a script to query visibility scores for each name
3. [ ] Collect raw data:
   - Google Trends search volume
   - Google Scholar citation count
   - General search result count
4. [ ] Store raw API responses in the database for future analysis

### Data Structure
```json
{
  "name": "Jane Addams",
  "api_data": {
    "google_trends_volume": 15000,
    "google_scholar_citations": 50000,
    "search_results_count": 2000000,
    "query_date": "2026-01-30"
  }
}
```

### Deliverable
- `visibility-raw-data.json` - Raw API data for all figures

---

## Phase 3: Inverse Weighting Formula

### Objective
Create a mathematical formula that inverts visibility to create representation weights.

### Core Formula
```
Representation Weight (W) = 1 / Visibility Score (V)
```

### Extended Formula with Normalization
```
W_normalized = (Average_V / Individual_V) * Scaling_Factor
```

Where:
- `Average_V` = Mean visibility across all figures
- `Individual_V` = Individual's visibility score
- `Scaling_Factor` = Adjustment to bring values into a usable range

### Homogenization Goal
The goal is to make the **Total Representation Weight constant across racial categories** in a pivot table analysis. This mathematically forces the system to prioritize recovery of erased voices.

### Tasks
1. [ ] Calculate mean visibility score across all figures
2. [ ] Calculate individual inverse indices
3. [ ] Create pivot table analysis by race
4. [ ] Adjust allocations to achieve homogeneous representation
5. [ ] Document the final formula and rationale

### Example Calculation
| Name | Visibility (V) | Inverse Weight (W) | Normalized Weight |
|------|----------------|-------------------|-------------------|
| Jane Addams | 2,000,000 | 0.0000005 | 0.01 |
| Ida B. Wells | 50,000 | 0.00002 | 0.40 |
| Janie Barrett | 1,000 | 0.001 | 20.0 |

### Deliverable
- `weighted-scores.json` - Calculated weights for all figures
- `methodology.md` - Documentation of the formula

---

## Phase 4: Intersectional Metadata Tagging

### Objective
Tag each figure with intersectional metadata to enable category-based analysis.

### Metadata Categories
1. **Race**: White, Black, Indigenous, Asian, Middle Eastern, etc.
2. **Gender**: Male, Female, Non-binary (where historically documented)
3. **Geographic Context**: US, Canada, UK, Egypt, Global
4. **Legacy Type**:
   - "State-Sanctioned Violence"
   - "Community Resistance"
   - "Institutional Complicity"
   - "Mutual Aid/Self-Determination"
5. **Era**: Pre-1900, 1900-1920, 1920-1950, 1950-1970
6. **Primary Domain**: Settlement houses, COS, Child welfare, Eugenics, Civil rights, etc.

### Tasks
1. [ ] Research and verify demographic data for each figure
2. [ ] Assign primary and secondary legacy types
3. [ ] Tag geographic and temporal contexts
4. [ ] Create pivot tables for analysis

### Data Structure
```json
{
  "id": "ida-b-wells",
  "name": "Ida B. Wells",
  "metadata": {
    "race": "Black",
    "gender": "Female",
    "geographic_context": "United States",
    "legacy_type": ["Community Resistance", "Anti-Violence Activism"],
    "era": "1890-1920",
    "primary_domain": "Anti-lynching, Journalism, Settlement houses"
  }
}
```

### Deliverable
- `intersectional-metadata.json` - Complete metadata for all figures

---

## Phase 5: Major Arcana Card Assignments

### Objective
Assign the 22 Major Arcana cards to figures based on:
1. Inverse visibility weighting
2. Archetypal resonance
3. Balanced representation across categories

### The 22 Major Arcana
| Number | Card | Suggested Assignment | Rationale |
|--------|------|---------------------|-----------|
| 0 | The Fool | TBD - Journey begins | |
| I | The Magician | Maggie L. Walker | Financial autonomy, transformative action |
| II | The High Priestess | TBD | Hidden knowledge, intuition |
| III | The Empress | Janie Barrett | Nurturing, creating new structures |
| IV | The Emperor | Mary Richmond | Authority, structure, social control |
| V | The Hierophant | Jane Addams | High morals, embedded in institutions |
| VI | The Lovers | TBD | Choices, relationships |
| VII | The Chariot | TBD | Determination, willpower |
| VIII | Strength/Justice | Ida B. Wells | Courage, truth-telling |
| IX | The Hermit | TBD | Inner wisdom, solitude |
| X | Wheel of Fortune | TBD | Cycles, fate |
| XI | Justice/Strength | TBD | Balance, karma |
| XII | The Hanged Man | TBD | Sacrifice, new perspective |
| XIII | Death | TBD | Transformation, endings |
| XIV | Temperance | TBD | Balance, moderation |
| XV | The Devil | Richard Henry Pratt? | Bondage, shadow, "kill the Indian" |
| XVI | The Tower | Africville Destruction? | Sudden change, destruction |
| XVII | The Star | Mary Ann Shadd Cary | Hope, inspiration, guidance |
| XVIII | The Moon | TBD | Illusion, unconscious |
| XIX | The Sun | TBD | Joy, success, clarity |
| XX | Judgement | TBD | Reflection, reckoning |
| XXI | The World | TBD | Completion, integration |

### Assignment Criteria
1. **Visibility-based priority**: Lower visibility figures get priority for Major Arcana
2. **Archetypal fit**: Card meaning should resonate with figure's historical role
3. **Representation balance**: Final deck should have homogeneous representation across racial categories
4. **Narrative coherence**: The deck should invite reflection on interlocking systems of complicity

### Tasks
1. [ ] Calculate final visibility rankings
2. [ ] Match figures to archetypes based on their historical roles
3. [ ] Balance representation across race and gender
4. [ ] Create card descriptions for each assignment
5. [ ] Review and refine assignments

### Deliverable
- `major-arcana-assignments.json` - Final card assignments
- `card-descriptions/` - Individual card meaning documents

---

## Phase 6: JSON Schema for recursive.eco

### Objective
Create the JSON schema structure compatible with recursive.eco platform.

### Schema Structure
```json
{
  "id": "anti-oppressive-major-arcana",
  "name": "Anti-Oppressive Major Arcana",
  "description": "A Major Arcana deck decolonizing social work history",
  "type": "tarot",
  "methodology": {
    "inverse_visibility": true,
    "source_text": "A Violent History of Benevolence",
    "homogenization_goal": "Equal representation weight across racial categories"
  },
  "items": [
    {
      "id": "0-the-fool",
      "number": 0,
      "name": "The Fool",
      "historical_figure": {
        "name": "TBD",
        "metadata": {...}
      },
      "sections": {
        "standard_meaning": "...",
        "violence_history": "...",
        "resistance_meaning": "...",
        "reflection_prompt": "..."
      }
    }
  ],
  "minor_arcana_candidates": [
    // Figures not assigned to Major Arcana
  ]
}
```

### Tasks
1. [ ] Design complete JSON schema
2. [ ] Create template for individual card objects
3. [ ] Populate cards with assignments from Phase 5
4. [ ] Add sections for critical historical analysis
5. [ ] Create grammar.json file compatible with recursive.eco
6. [ ] Test schema validation

### Deliverable
- `grammar.json` - Complete recursive.eco compatible schema

---

## Phase 7: Documentation and Ethical Framework

### Objective
Document the methodology and ethical considerations of the project.

### Key Documents
1. **Methodology Paper**: Academic documentation of the inverse visibility approach
2. **Ethical Statement**: Acknowledgment that this deck itself is "colonial in that it leaves aside the Indigenous account"
3. **User Guide**: How to use the deck for reflection on social work practice
4. **Attribution**: Proper citation of Chapman & Withers and all sources

### Ethical Considerations
- This deck centers Black resistance but acknowledges it does not fully address Indigenous perspectives
- The "standard account" critique should not become another form of simplified binary
- Card users should engage with complexity, not seek "innocent" identification
- Analeptic thinking: holding contradiction while manifesting alternative narratives

### Tasks
1. [ ] Write methodology documentation
2. [ ] Create ethical framework statement
3. [ ] Develop reflection prompts for each card
4. [ ] Write user guide

### Deliverable
- `METHODOLOGY.md`
- `ETHICS.md`
- `USER_GUIDE.md`

---

## Timeline Overview

| Phase | Description | Dependencies |
|-------|-------------|--------------|
| 1 | Name Extraction | None |
| 2 | Visibility Metrics | Phase 1 |
| 3 | Inverse Weighting | Phase 2 |
| 4 | Intersectional Tagging | Phase 1 |
| 5 | Card Assignments | Phases 3, 4 |
| 6 | JSON Schema | Phase 5 |
| 7 | Documentation | All phases |

---

## Technical Requirements

### APIs Needed
- Google Custom Search API or SerpApi
- Pytrends (Google Trends)

### Tools
- Python for data collection scripts
- JSON for data storage
- Markdown for documentation
- Pivot table software (Excel/Google Sheets) for analysis

### Repository Structure
```
schemas/tarot/anti-opressive-major-arcana/
├── README.md                    # Project documentation
├── PROJECT_PLAN.md              # This document
├── outline.md                   # Source chapters and initial project notes
├── data/
│   ├── names-extracted.json     # Phase 1 output
│   ├── visibility-raw-data.json # Phase 2 output
│   ├── weighted-scores.json     # Phase 3 output
│   └── intersectional-metadata.json # Phase 4 output
├── cards/
│   ├── major-arcana-assignments.json
│   └── descriptions/
│       ├── 00-fool.md
│       ├── 01-magician.md
│       └── ...
├── docs/
│   ├── METHODOLOGY.md
│   ├── ETHICS.md
│   └── USER_GUIDE.md
└── grammar.json                 # Final recursive.eco schema
```

---

## Next Steps

1. **Immediate**: Complete name extraction from both chapters
2. **Week 1**: Set up API access and collect visibility data
3. **Week 2**: Calculate inverse weights and analyze pivot tables
4. **Week 3**: Assign cards and create descriptions
5. **Week 4**: Build JSON schema and documentation

---

## References

- Chapman, C., & Withers, A. J. (2019). *A Violent History of Benevolence: Interlocking oppression in the moral economies of social working*. University of Toronto Press.
- NASW (2021). Apology for the profession's role in supporting policies that harmed people of colour.
- CSWE Statement on Accountability.
- Spivak, G. C. on "persistent dredging operations" and complicity.
- Ahmed, S. on how racism shapes surfaces of bodies and worlds.

---

*This plan embodies "analeptic thinking" - holding contradiction while manifesting alternative narratives. All figures are complicit; the deck refuses to offer a comfortable "other side of the river" to identify with.*
