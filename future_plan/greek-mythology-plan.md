# Greek Mythology Grammar — Build Plan

> **Purpose**: This document is the master plan for building two connected grammars. Each section is a self-contained commit that can be executed by a Claude agent. Update the checkboxes as each commit lands.

## Architecture

Two grammars in `custom/`:

```
custom/greek-mythology-family-tree/grammar.json   ← profiles of gods & heroes
custom/greek-mythology-myths/grammar.json          ← the stories
```

They cross-reference via `deep_links` on each item.

### Item Schema (Family Tree)

```json
{
  "id": "zeus",
  "name": "Zeus",
  "level": 1,
  "category": "olympian",
  "sort_order": 1,
  "sections": {
    "Profile": "2-3 sentences: who they are, role in the cosmos.",
    "Family": "Parents, consort(s), notable children. Use names only, not prose.",
    "Domains & Epithets": "What they rule, key titles (e.g., 'Cloud-Gatherer').",
    "Symbols": "Sacred animals, objects, plants.",
    "Character": "Personality — strengths, flaws, archetypal role."
  },
  "keywords": ["sky", "thunder", "king", "justice"],
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/...",
  "metadata": {
    "roman_name": "Jupiter",
    "generation": "olympian",
    "parents": ["kronos", "rhea"]
  },
  "deep_links": [
    { "target_grammar": "greek-mythology-myths", "target_item": "the-titanomachy", "label": "The Titanomachy" },
    { "target_grammar": "greek-mythology-myths", "target_item": "prometheus-steals-fire", "label": "Prometheus Steals Fire" }
  ]
}
```

### Item Schema (Myths)

```json
{
  "id": "prometheus-steals-fire",
  "name": "Prometheus Steals Fire",
  "level": 1,
  "category": "creation",
  "sort_order": 1,
  "sections": {
    "The Story": "3-5 paragraph retelling. Vivid but concise.",
    "For Young Readers": "2-3 sentences, age 5-8.",
    "Characters": "Bulleted list of who appears.",
    "Themes": "1-2 sentences on the moral/archetypal meaning.",
    "Legacy": "1-2 sentences on modern echoes (words, art, culture)."
  },
  "keywords": ["fire", "defiance", "punishment", "gift"],
  "metadata": {
    "cycle": "creation",
    "characters": ["prometheus", "zeus"]
  },
  "deep_links": [
    { "target_grammar": "greek-mythology-family-tree", "target_item": "prometheus", "label": "Prometheus" },
    { "target_grammar": "greek-mythology-family-tree", "target_item": "zeus", "label": "Zeus" }
  ]
}
```

### L2 Emergent Items

Both grammars have L2 items with `relationship_type: "emergence"` and `composite_of` arrays, plus their own summary sections.

---

## Commit Plan

### Commit 1: Family Tree — Scaffold + Primordials
- [ ] Create `custom/greek-mythology-family-tree/grammar.json`
- [ ] Root metadata (name, description, tags, attribution, connected_grammars)
- [ ] L2 generation item: "The Primordials" (emergent)
- [ ] L1 profiles (8): Chaos, Gaia, Uranus, Pontus, Tartarus, Erebus, Nyx, Eros

**Agent prompt**: "Read `future_plan/greek-mythology-plan.md` for the schema. Create `custom/greek-mythology-family-tree/grammar.json` with root metadata and Commit 1 items (Primordials). Follow the Item Schema (Family Tree) exactly. Write vivid, concise profiles from your knowledge of Greek mythology. deep_links can be empty arrays for now — they'll be filled in a later commit."

### Commit 2: Family Tree — Titans
- [ ] L2 generation item: "The Titans" (emergent)
- [ ] L1 profiles (10): Kronos, Rhea, Oceanus, Tethys, Hyperion, Theia, Coeus, Phoebe, Mnemosyne, Themis

**Agent prompt**: "Read the plan at `future_plan/greek-mythology-plan.md` and the current grammar at `custom/greek-mythology-family-tree/grammar.json`. Add the Commit 2 items (Titans). Append to the existing items array. Follow the established schema exactly."

### Commit 3: Family Tree — Titans' Children & Prometheus
- [ ] L2 generation item: "Children of the Titans" (emergent)
- [ ] L1 profiles (6): Iapetus, Atlas, Prometheus, Epimetheus, Helios, Selene, Eos

**Agent prompt**: "Read the plan and current grammar. Add Commit 3 items (Titan offspring including Prometheus, Atlas, and the celestial Titans Helios/Selene/Eos). Append to existing items."

### Commit 4: Family Tree — Olympians Part 1 (The Big Six)
- [ ] L2 generation item: "The Twelve Olympians" (emergent — will grow in Commit 5)
- [ ] L1 profiles (6): Zeus, Hera, Poseidon, Demeter, Athena, Apollo

**Agent prompt**: "Read the plan and current grammar. Add Commit 4 items (first 6 Olympians). Create the L2 'Twelve Olympians' emergent item with composite_of for all 12 (the remaining 6 IDs will be added in Commit 5). Write rich profiles — these are the most important figures."

### Commit 5: Family Tree — Olympians Part 2
- [ ] L1 profiles (6): Artemis, Ares, Aphrodite, Hephaestus, Hermes, Dionysus
- [ ] Update "The Twelve Olympians" L2 composite_of if needed

**Agent prompt**: "Read the plan and current grammar. Add Commit 5 items (remaining 6 Olympians). Ensure the L2 'Twelve Olympians' item's composite_of includes all 12."

### Commit 6: Family Tree — Realm Gods & Chthonic
- [ ] L2 generation item: "Gods of the Realms" (emergent)
- [ ] L1 profiles (6): Hades, Persephone, Hestia, Hecate, Pan, Iris

**Agent prompt**: "Read the plan and current grammar. Add Commit 6 items (Hades, Persephone, Hestia, Hecate, Pan, Iris). These are major deities not counted among the Twelve but essential to the mythology."

### Commit 7: Family Tree — Heroes & Demigods
- [ ] L2 generation item: "Heroes & Demigods" (emergent)
- [ ] L1 profiles (10): Heracles, Perseus, Theseus, Achilles, Odysseus, Jason, Orpheus, Atalanta, Bellerophon, Aeneas

**Agent prompt**: "Read the plan and current grammar. Add Commit 7 items (10 heroes). These are mortals or demigods. Profiles should emphasize their famous deeds and fatal flaws."

### Commit 8: Myths — Scaffold + Creation Cycle
- [ ] Create `custom/greek-mythology-myths/grammar.json`
- [ ] Root metadata (name, description, tags, attribution, connected_grammars)
- [ ] L2 cycle item: "The Creation & Titanomachy" (emergent)
- [ ] L1 myths (4): The Birth of the Gods, The Titanomachy, Prometheus Steals Fire, Pandora's Box

**Agent prompt**: "Read the plan at `future_plan/greek-mythology-plan.md`. Create `custom/greek-mythology-myths/grammar.json` with root metadata and Commit 8 items (Creation cycle). Follow the Item Schema (Myths) exactly. Write vivid 3-5 paragraph retellings. Include deep_links to the family tree grammar characters."

### Commit 9: Myths — Heracles Cycle
- [ ] L2 cycle item: "The Labors of Heracles" (emergent)
- [ ] L1 myths (3): Birth of Heracles, The Twelve Labors, The Death of Heracles

**Agent prompt**: "Read the plan and current myths grammar. Add Commit 9 items (Heracles cycle). The Twelve Labors should be one item with all 12 labors summarized in 'The Story'. Include deep_links."

### Commit 10: Myths — Trojan War Cycle
- [ ] L2 cycle item: "The Trojan War" (emergent)
- [ ] L1 myths (4): The Judgment of Paris, The Sacrifice of Iphigenia, Achilles and Hector, The Trojan Horse

**Agent prompt**: "Read the plan and current myths grammar. Add Commit 10 items (Trojan War). These are some of the most dramatic stories — write them vividly. Include deep_links."

### Commit 11: Myths — The Odyssey
- [ ] L2 cycle item: "The Odyssey" (emergent)
- [ ] L1 myths (4): Odysseus and the Cyclops, Circe's Island, The Sirens and Scylla, The Return to Ithaca

**Agent prompt**: "Read the plan and current myths grammar. Add Commit 11 items (Odyssey cycle). Focus on the most iconic episodes. Include deep_links."

### Commit 12: Myths — Metamorphoses & Love
- [ ] L2 cycle item: "Metamorphoses & Love" (emergent)
- [ ] L1 myths (5): Orpheus and Eurydice, Eros and Psyche, Echo and Narcissus, Daphne and Apollo, Pygmalion and Galatea

**Agent prompt**: "Read the plan and current myths grammar. Add Commit 12 items (love stories / transformations). These are tender, poignant tales. Include deep_links."

### Commit 13: Myths — Hubris & Punishment
- [ ] L2 cycle item: "Hubris & Divine Punishment" (emergent)
- [ ] L1 myths (5): Icarus and Daedalus, Arachne, King Midas, Sisyphus, Tantalus and Niobe

**Agent prompt**: "Read the plan and current myths grammar. Add Commit 13 items (hubris myths). These are cautionary tales. Include deep_links."

### Commit 14: Myths — Underworld & Theban Cycle
- [ ] L2 cycle item: "Journeys to the Underworld" (emergent)
- [ ] L2 cycle item: "The Theban Cycle" (emergent)
- [ ] L1 myths (4): The Abduction of Persephone, Oedipus and the Sphinx, Antigone, Theseus and the Minotaur

**Agent prompt**: "Read the plan and current myths grammar. Add Commit 14 items (Underworld myths + Theban cycle). Include deep_links."

### Commit 15: Cross-Reference Pass
- [ ] Update all family tree items with deep_links to relevant myths
- [ ] Update all myth items with deep_links to family tree characters
- [ ] Verify all composite_of references resolve
- [ ] Verify all deep_link target_items exist in the target grammar

**Agent prompt**: "Read both grammars. For each family tree item, add deep_links to every myth where that figure appears. For each myth item, verify deep_links to the family tree are correct. Validate all composite_of references. Report any broken references."

---

## Progress Tracker

Update this section after each commit lands.

| Commit | Status | Items Added | Running Total |
|--------|--------|-------------|---------------|
| 1. Scaffold + Primordials | NOT STARTED | 9 (1 L2 + 8 L1) | 9 |
| 2. Titans | NOT STARTED | 11 (1 L2 + 10 L1) | 20 |
| 3. Titans' Children | NOT STARTED | 8 (1 L2 + 7 L1) | 28 |
| 4. Olympians Part 1 | NOT STARTED | 7 (1 L2 + 6 L1) | 35 |
| 5. Olympians Part 2 | NOT STARTED | 6 (0 L2 + 6 L1) | 41 |
| 6. Realm Gods | NOT STARTED | 7 (1 L2 + 6 L1) | 48 |
| 7. Heroes | NOT STARTED | 11 (1 L2 + 10 L1) | 59 |
| 8. Myths Scaffold + Creation | NOT STARTED | 5 (1 L2 + 4 L1) | 64 |
| 9. Heracles Cycle | NOT STARTED | 4 (1 L2 + 3 L1) | 68 |
| 10. Trojan War | NOT STARTED | 5 (1 L2 + 4 L1) | 73 |
| 11. Odyssey | NOT STARTED | 5 (1 L2 + 4 L1) | 78 |
| 12. Metamorphoses & Love | NOT STARTED | 6 (1 L2 + 5 L1) | 84 |
| 13. Hubris & Punishment | NOT STARTED | 6 (1 L2 + 5 L1) | 90 |
| 14. Underworld & Theban | NOT STARTED | 6 (2 L2 + 4 L1) | 96 |
| 15. Cross-Reference Pass | NOT STARTED | 0 (updates only) | 96 |

**Target**: ~96 items across 2 grammars (59 family tree + 37 myths)

---

## Reference: Full Item ID List

### Family Tree IDs (for deep_links)

**Primordials**: `chaos`, `gaia`, `uranus`, `pontus`, `tartarus`, `erebus`, `nyx`, `eros-primordial`

**Titans**: `kronos`, `rhea`, `oceanus`, `tethys`, `hyperion`, `theia`, `coeus`, `phoebe`, `mnemosyne`, `themis`

**Titans' Children**: `iapetus`, `atlas`, `prometheus`, `epimetheus`, `helios`, `selene`, `eos`

**Olympians**: `zeus`, `hera`, `poseidon`, `demeter`, `athena`, `apollo`, `artemis`, `ares`, `aphrodite`, `hephaestus`, `hermes`, `dionysus`

**Realm Gods**: `hades`, `persephone`, `hestia`, `hecate`, `pan`, `iris`

**Heroes**: `heracles`, `perseus`, `theseus`, `achilles`, `odysseus`, `jason`, `orpheus`, `atalanta`, `bellerophon`, `aeneas`

### Myths IDs (for deep_links)

**Creation**: `birth-of-the-gods`, `the-titanomachy`, `prometheus-steals-fire`, `pandoras-box`

**Heracles**: `birth-of-heracles`, `the-twelve-labors`, `death-of-heracles`

**Trojan War**: `judgment-of-paris`, `sacrifice-of-iphigenia`, `achilles-and-hector`, `the-trojan-horse`

**Odyssey**: `odysseus-and-the-cyclops`, `circes-island`, `the-sirens-and-scylla`, `return-to-ithaca`

**Metamorphoses**: `orpheus-and-eurydice`, `eros-and-psyche`, `echo-and-narcissus`, `daphne-and-apollo`, `pygmalion-and-galatea`

**Hubris**: `icarus-and-daedalus`, `arachne`, `king-midas`, `sisyphus`, `tantalus-and-niobe`

**Underworld & Theban**: `abduction-of-persephone`, `oedipus-and-the-sphinx`, `antigone`, `theseus-and-the-minotaur`

---

## Wikimedia Commons Image Strategy

All images should be public domain from Wikimedia Commons. Preferred sources:
- Classical Greek pottery / vase paintings
- Renaissance paintings (Botticelli, Raphael, Rubens — all public domain)
- Ancient Roman copies of Greek sculptures

Format: `https://upload.wikimedia.org/wikipedia/commons/...`

Image lookup is a separate pass — leave `image_url` empty on first creation, fill in a dedicated commit if desired.

---

## How to Resume

If you're a new Claude session picking this up:

1. Read this file first: `future_plan/greek-mythology-plan.md`
2. Check the Progress Tracker table above — find the first NOT STARTED commit
3. Read the agent prompt for that commit
4. Read the current state of the grammar file(s) being modified
5. Execute the commit
6. Update the Progress Tracker
7. Commit, push, and move to the next one
