# Build Log: Repair I Ching + Repair Book Ch12

**Date**: 2026-03-10
**Grammar**: `grammars/repair-iching/grammar.json`
**Also modified**: `grammars/repair-an-open-source-book/grammar.json` (added Ch12)

## What Was Built

### Ch12: The Book of Changes (in Repair: An Open Source Book)
- Added as the 12th chapter of the Repair book
- Mapped to **The Hanged Man (XII)** — suspended perspective, seeing the world upside down
- Contains all 10 lenses: Research, Clinical, Spiritual, Practices, Rituals, Songs & Playlists, Kids Version, Sci-Fi, Open Source, Cracks
- Core argument: The I Ching survived the Burning of the Books (213 BCE) because colonizers classified it as divination rather than philosophy — the trickster survival mechanism
- Deeper teaching: change (易) as the fundamental nature of reality, not as event but as ontology
- Practice thread: contemplative illustration (like coloring books but alive) — search for images that embody hexagrams

### The Repair I Ching (new grammar)
- 14 items: 12 L1 hexagrams + 1 L2 emergence + 1 L3 meta
- Grammar type: `iching`
- Each hexagram maps to one chapter of the Repair book:

| Hexagram | Chinese | Name | Repair Chapter |
|----------|---------|------|---------------|
| 6 | 訟 | Conflict | Ch1: The 69% |
| 29 | 坎 | The Abysmal | Ch2: The Cry Beneath |
| 58 | 兌 | The Joyous | Ch3: Hold Me Tight |
| 24 | 復 | Return | Ch4: Making Amends |
| 63 | 既濟 | After Completion | Ch5: Staying Alive |
| 50 | 鼎 | The Caldron | Ch6: What Survives |
| 47 | 困 | Oppression | Ch7: Comfortable Bondage |
| 49 | 革 | Revolution | Ch8: The First Fire |
| 53 | 漸 | Gradual Progress | Ch9: A Vocation |
| 11 | 泰 | Peace | Ch10: Re-Pairing |
| 20 | 觀 | Contemplation | Ch11: Showing Up |
| 64 | 未濟 | Before Completion | Ch12: Book of Changes |

### Key Design Decisions
- **Before Completion (64) as the closing hexagram**: The I Ching's last hexagram refuses to end. The Repair book's last chapter refuses to complete. Recursive.
- **Each hexagram has 4 sections**: Hexagram (cosmological), Repair Reading (mapped to chapter), Contemplative Practice (illustration invitation), The Crack (honest limitations)
- **52 missing hexagrams are explicit**: Named as invitations, not oversights. 18.75% completion. "Before Completion."
- **Christopher Kelty's recursive public** woven into the L3 meta item — the I Ching as the oldest recursive public

## Learnings

1. **The tarot-to-I-Ching transfer works**: Ch11's argument (tarot as cognitive reframing) transfers cleanly to I Ching. But the I Ching goes further: where tarot gives you ONE card (one reframe), the I Ching gives you a hexagram with changing lines — a situation AND its trajectory. It's a narrative reframing ENGINE, not a single reframe.

2. **The colonial survival story is the spine**: The Burning of the Books (焚書坑儒) gives the I Ching chapter its political depth. This pattern (wisdom surviving by being misclassified) appears everywhere: Yoruba theology as "folklore," Aboriginal songlines as "myth," the I Ching as "fortune-telling."

3. **Illustration as practice is genuine**: Not decorative. The act of searching for an image that embodies a hexagram IS contemplation. Like mandala-making or sand painting — the process is the practice, not the product.

4. **The Cracks in this grammar are real**: We cherry-picked 12 hexagrams out of 64. The furious hexagrams (Darkening of the Light, Breakthrough, Work on What Has Been Spoiled) tell a different story about repair — one where it's urgent and angry, not gentle and contemplative.

## Future Ideas (logged from user conversation)

### Tier 1: Do Next
- **Illustration practice documentation**: Create a README or docs file that outlines the recursive practice — what it is, how to do it, how to use recursive.eco for contemplative illustration
- **Christopher Kelty's "recursive public" concept**: Upload reference material. The concept that inspired recursive.eco. Should be woven more explicitly into the book and the platform philosophy

### Tier 2: Medium-term
- **Vibe-coding tool for grammars**: A simple tool people can use to create their own recursive grammars. Could search this repo and reference files. Lower the barrier to forking.
- **Public domain illustration sources**: Build a reference guide for users who want to illustrate grammars:
  - **Tier 1 (Public Domain)**: Smithsonian Open Access (4.4M+), Met Museum CC0 (490K+), NASA, Library of Congress, Biodiversity Heritage Library (150K+), Europeana, Rawpixel, Internet Archive, WikiSource
  - **Tier 2 (CC BY/BY-SA)**: Wikipedia/Wikimedia, OpenStax, CK-12, MIT OCW, Khan Academy, PLOS ONE/arXiv
  - **Tier 3 (Government)**: Brazilian gov publications, IBGE, FUNAI, US gov (USGS, NOAA, NIH)
  - **Especially rich for this project**: Domínio Público (dominiopublico.gov.br), Brasiliana USP, Biblioteca Nacional Digital Brasil, Museu Nacional UFRJ

### Tier 3: Vision
- **"I thought I was building an app but I might be developing a practice"**: The recursive.eco project may be more practice than product. The grammars, the illustration, the forking, the contemplation — these are practices. The app is the caldron. The practice is the fire.
- **The Repair book itself might need a practice guide**: Not just "how to use this grammar" but "how to live recursively" — a guide to the contemplative practice of engaging with symbolic systems as a way of paying attention to change
