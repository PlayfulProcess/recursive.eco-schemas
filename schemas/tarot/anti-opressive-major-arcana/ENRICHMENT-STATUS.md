# Card Enrichment Status

## Source Books

1. **Chapman & Withers (2019)**: *A Violent History of Benevolence* - Primary source for Standard Account and Erased Voices
2. **Eisler (1987)**: *The Chalice and the Blade* - Partnership vs. dominator models, roles not names
3. **Maguire (1995)**: *Wicked* - Villain's perspective, cultural memory

## Enrichment Criteria

Each card should have:
- [ ] **Context**: What did they do? What's the complexity?
- [ ] **Source**: Direct quote with page number from book
- [ ] **Key Insight**: The "so what?" - why this matters for understanding social working
- [ ] **Archetypal Resonances**: Tarot connections
- [ ] **Reflection**: Question for the reader

## Cards Needing Book Enrichment

### Standard Account (Chapman & Withers)

| Card | Has Quote | Has Page # | Key Insight | Status |
|------|-----------|------------|-------------|--------|
| jane-addams | ✅ | ✅ (51) | ✅ | Complete |
| mary-richmond | ✅ | ✅ (31-32) | ✅ | Complete |
| katherine-bement-davis | ✅ | ✅ (50-51) | ⚠️ | Needs insight |
| josephine-shaw-lowell | ✅ | ✅ (50, 52) | ✅ | Complete |
| richard-henry-pratt | ✅ | ✅ (60) | ✅ | Complete |
| albert-rose | ✅ | ✅ (62-70) | ✅ | Complete |
| abraham-flexner | ❌ | ❌ | ❌ | **Needs enrichment** |
| oscar-mcculloch | ✅ | ✅ (35) | ✅ | Complete |
| jj-kelso | ✅ | ✅ (35) | ⚠️ | Needs insight |
| jeffery-brackett | ❌ | ❌ | ❌ | **Needs enrichment** |
| simon-patten | ❌ | ❌ | ❌ | **Needs enrichment** |
| philip-c-garrett | ❌ | ❌ | ❌ | **Needs enrichment** |
| theodore-roosevelt | ❌ | ❌ | ❌ | **Needs enrichment** |
| sir-francis-galton | ✅ | ✅ (34-35) | ✅ | Complete |
| john-edward-lloyd | ⚠️ | ❌ | ❌ | **Needs enrichment** |
| reverend-william-baldwin | ✅ | ✅ (34) | ✅ | Complete |
| emma-goldman | ✅ | ✅ (28-29, 38) | ✅ | Complete |

### Erased Voices (Chapman & Withers)

| Card | Has Quote | Has Page # | Key Insight | Status |
|------|-----------|------------|-------------|--------|
| ida-b-wells | ✅ | ✅ (60) | ✅ | Complete |
| web-du-bois | ❌ | ❌ | ❌ | **Needs enrichment** |
| booker-t-washington | ❌ | ❌ | ❌ | **Needs enrichment** (p.48) |
| claudette-colvin | ✅ | ✅ (73-75) | ✅ | Complete |
| rosa-parks | ✅ | ✅ (74-75) | ✅ | Complete |
| viola-desmond | ✅ | ✅ (67, 74) | ✅ | Complete |
| aaron-pa-carvery | ✅ | ✅ (70) | ✅ | Complete |
| martin-luther-king-jr | ⚠️ | ⚠️ (68) | ❌ | **Needs enrichment** |
| malcolm-x | ⚠️ | ⚠️ | ❌ | **Needs enrichment** |

### Places of Care (New - Needs Research)

| Card | Source Needed | Status |
|------|--------------|--------|
| quilombo-dos-palmares | Brazilian history sources | Research needed |
| hull-house | Chapman & Withers (46+) | Partial |
| toynbee-hall | Settlement house history | Research needed |
| highlander-folk-school | Civil rights history | Research needed |
| freedom-schools | 1964 Freedom Summer | Research needed |
| survival-programs | Black Panther history | Research needed |
| terreiros | Brazilian religious studies | Research needed |
| africville | Chapman & Withers (67-72) | Has some content |

## Search Terms for Enrichment

Use `scripts/enrich-cards.py` to find quotes:

```bash
cd schemas/tarot/anti-opressive-major-arcana

# Single card
python scripts/enrich-cards.py --card-id jane-addams

# All configured cards
python scripts/enrich-cards.py --all --output json > data/enrichment-data.json
```

## Key Quotes to Add

### On the movement, not the individual (p. 74-75)
> "Like all social justice movements, the Montgomery bus boycott was built on painstaking organizing efforts and the infrastructure developed through these efforts by generations of people struggling for social justice."

### On neither demonizing nor romanticizing (p. 46)
> "Our point isn't that we should find another flawless historical figure to emulate... We should neither 'demonize nor romanticize' Addams."

### On the mainstream (p. 27)
> "The mainstream has never run clean."

### On radical complicity (p. 38)
> "Radical political action and organizing was viewed as perfectly harmonious with eugenics. This radical complicity in eugenic activism offers an important lesson that those of us who consider ourselves radical today should reflect very carefully upon."

### On what gets included (p. 60)
> "We can just pause to consider what gets included or excluded in normative social work history."

## Next Steps

1. Run `enrich-cards.py --all` to generate enrichment data
2. For each card marked "Needs enrichment", search outline.md for quotes
3. Add Source section with page numbers
4. Add Key Insight section explaining significance
5. Update this tracking document as cards are enriched
