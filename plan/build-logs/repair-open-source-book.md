# Build Log: Repair — An Open Source Book

## Date: 2026-03-10

## Architecture

### Thesis
Repair is the single most adaptive capacity a system can have — couple, community, culture, species. What can't repair, extracts. What extracts, dies.

### Tarot Major Arcana Spine
Each chapter maps to a Major Arcana card:

| # | Chapter ID | Name | Card | Voice |
|---|-----------|------|------|-------|
| 1 | ch01-the-sixty-nine-percent | The 69% That Never Gets Solved | The Lovers (VI) | Gottman |
| 2 | ch02-the-cry-beneath-the-fight | The Cry Beneath the Fight | The Moon (XVIII) | Bowlby/Ainsworth |
| 3 | ch03-hold-me-tight | Hold Me Tight | The Star (XVII) | Sue Johnson/EFT |
| 4 | ch04-making-amends | Making Amends | Judgement (XX) | AA/12 Steps |
| 5 | ch05-staying-alive-in-the-fire | Staying Alive in the Fire | Temperance (XIV) | Marsha Linehan/DBT |
| 6 | ch06-what-survives-the-turning | What Survives the Turning | Wheel of Fortune (X) | Adaptive/Maladaptive |
| 7 | ch07-the-comfortable-bondage | The Comfortable Bondage | The Devil (XV) | Extraction/Colonialism/Andreotti |
| 8 | ch08-the-first-fire | The First Fire | The Tower (XVI) | Deep History/Megafauna |
| 9 | ch09-a-vocation-not-a-prophecy | A Vocation, Not a Prophecy | Strength (XI) | Palmer/Akomolafe/Andreotti |
| 10 | ch10-re-pairing | Re-Pairing | The World (XXI) | All voices converge |

### 10 Lenses (Sections per Chapter)
1. **Research** — academic citations, studies, data
2. **Clinical** — therapeutic framing (including modernity-as-addiction)
3. **Spiritual** — prayer (father/mother/ancestors/cosmos), myth, sacred text
4. **Practices** — recursive.eco practices, tarot spreads, I Ching, cooking, gardening, singing, yoga, apologizing
5. **Rituals** — ceremonies, threshold crossings, relational practices
6. **Songs & Playlists** — curated songs, Spotify/YouTube queues
7. **Kids Version** — the chapter told to a five-year-old
8. **Sci-Fi** — AI futures, trickster AI (Bayo), 0.1% Antarctica scenarios, inequality extrapolations
9. **Open Source** — public domain books, museum artifacts, images, forkable content
10. **Cracks** — Agnostos Theos (the unnamed god), what we don't believe, what was left out, further investigations

### L2 Emergence (Scale Decomposition)
Ecological contains Cultural, Cultural contains Intimate.

| L2 ID | Name | Composite Of | Decomposition |
|-------|------|-------------|---------------|
| ecological-scale | The Ecological Scale | ch06, ch07, ch08, ch09, ch10 | Contains cultural-scale |
| cultural-scale | The Cultural Scale | ch04, ch05, ch06, ch07, ch08, ch09 | Contains intimate-scale |
| intimate-scale | The Intimate Scale | ch01, ch02, ch03, ch04, ch05 | Innermost |

### L3 Meta
- **repair-open-source-book**: The whole grammar as one card. "You are holding a living document that is trying to repair the idea of what a book is."

### Key Design Decisions
- **Tone**: Kind, silly, warm. "Come cook with us." Not preachy.
- **Popular culture is medicine**: Prayer, singing together, cooking. The grandmother's wisdom (but not romanticized — some grandmothers think in numbers and moral judgments).
- **AI as trickster** (Bayo): Not anti-tech. Honest about the cost. AI making humanity see it's not the sole custodian of intelligence.
- **Not prophecy**: We don't know if modernity will crumble. Maybe the 0.1% survives in Antarctic domes. This is about vocation, not prediction. "I prefer to die with honor."
- **Astrology as relational animist practice**: Not predictive. Planetary relationships.
- **Parker Palmer**: "Let your life speak" — vocation as listening, the US grammar of selfhood as convergence of animating forces.
- **Agnostos Theos**: The Greek Unknown God as patron of every Cracks section.

## Build Strategy
1. ✅ Chapters 1-3 written with full content
2. Chapters 4-10 as skeletons (structure + brief sections)
3. L2 + L3 emergence items
4. Validate, manifest, commit
5. Fill chapters gradually in subsequent passes

## Parsing Notes
- No source text parsing — this is written from memory/knowledge
- Large grammar (~16 items total: 10 L1 + 3 L2 + 1 L3 + possible extras)
- Writing in chunks to avoid timeout
