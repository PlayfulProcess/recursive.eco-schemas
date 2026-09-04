# Grammar Building Principles

Distilled from building and debugging grammars across multiple source types. These principles are ordered by grammar type, with cross-cutting rules at the end. This document is designed to be importable into a website assistant for grammar-building guidance.

---

## By Grammar Type

### 1. From Source Text — Books (novels, children's books)

**Examples**: Alice in Wonderland, Winnie-the-Pooh

**Structure**: L1 = scenes, L2 = chapters (composites)

**Key principles**:
- Paragraph breaks and `* * *` dividers are reliable scene boundaries
- Chapter titles make excellent L2 names — use them directly
- Children's books have natural scene breaks (tonal shifts, location changes, new characters appearing)
- Full scene text is usually 1-5K chars — very manageable
- Multi-audience sections ("Original Text" + "For Young Readers") add value for family-oriented grammars

**Section naming**:
- L1: "Story" or "Story (Original Text)" for the source text
- L1 (optional): "For Young Readers", "What Happens" for adapted versions
- L2: "For Littlest Readers", "Characters You'll Meet", "Famous Lines", "Things to Talk About"

**Efficiency**: HIGH — clean structure, predictable parsing, moderate item count (30-60 items)

**Risks**: LOW — the main risk is inconsistent scene break detection

---

### 2. From Source Text — Sacred/Philosophical Texts

**Examples**: Confucian Analects, Dhammapada, (planned) Zohar, Tao Te Ching

**Structure**: L1 = individual teachings/passages, L2 = books/chapters (composites)

**Key principles**:
- **DO NOT assume paragraph-based splitting.** Sacred texts often use indentation-based formatting without blank lines between teachings.
- Speaker attributions ("The Master said", "The Buddha said") are the most reliable passage delimiters
- If no speaker attributions, look for verse numbering or indentation patterns
- Book/chapter summaries must be WRITTEN BY HAND — sacred texts don't contain their own summaries
- Passage count can be high (500-800+ items) — this is fine
- Use traditional book/chapter names (e.g., "Xue Er" not "Book 1") alongside numbers

**Section naming**:
- L1: "Teaching" or "Verse" for the source text
- L2: "Brief" for hand-written thematic summary

**Efficiency**: MEDIUM — parsing is tricky (see failures below), but once the delimiter is found, it's fast

**Common failures**:
- `\n\n` splitting produces 1 chunk per chapter (no blank lines between passages)
- Continuations of the same speaker look like new passages if delimiter is too simple
- Transliteration differences in names/titles can cause duplicate detection

**Risks**: MEDIUM — delimiter detection requires trial-and-error

---

### 3. From Source Text — Dramatic Works (plays)

**Examples**: Shakespeare (10 plays)

**Structure**: L1 = scenes, L2 = acts (composites), L3 = plays (composites)

**Key principles**:
- 3-level hierarchy maps naturally: scene → act → play
- ACT/SCENE markers are the structural delimiters — but they have inconsistent formatting:
  - Some use `ACT I`, others `ACT I.` (trailing period)
  - Always make regex flexible: `^ACT ([IVX]+)\.?\s*$`
- **Every play has a "fake" TOC section** (Contents + Dramatis Personae) before the actual text — skip it by finding the 2nd occurrence of "ACT I"
- Dramatis Personae is valuable metadata — extract it for the L3 "Characters" section
- Scene text can be VERY large (up to 28K chars) — this is acceptable
- Unicode traps: Gutenberg texts mix straight and curly apostrophes/quotes

**Section naming**:
- L1: "Scene" for the full dialogue text
- L2: "Brief" for act summary
- L3: "Synopsis" + "Characters"

**Efficiency**: MEDIUM-HIGH — once the parser handles edge cases, it processes all plays identically

**Common failures**:
- Smart apostrophes (U+2019) causing title mismatches
- Trailing period in ACT markers missed by strict regex
- Play boundaries confused when titles appear in dialogue (use standalone-line matching)

**Risks**: MEDIUM — edge cases are per-play, but the overall pattern is stable

---

### 4. From Memory — Knowledge/Taxonomy Grammars

**Examples**: Greek Mythology & Astrology, (planned) Human Body, Language Trees, Jungian Archetypes

**Structure**: Variable — depends on the domain's natural hierarchy

**Key principles**:
- **Start with a taxonomy/outline BEFORE writing content.** List all items at each level first.
- Cross-domain composites are powerful (zodiac → gods → myths creates a hierarchy that no single source contains)
- `composite_of` relationships must be planned, not discovered
- Validate referential integrity after EVERY edit session — these grammars drift the most
- Content must be written from knowledge — there's no source text to extract

**Section naming**: Domain-dependent. Use descriptive names for what each section contains.

**Efficiency**: LOW — every item is hand-crafted, no automation possible for content

**Common failures**:
- Broken refs from name changes (renamed "Zeus" to "Jupiter" but forgot to update composite_of arrays)
- Missing items discovered mid-build (had gods but not mortals/heroes)
- Scope creep (started with Greek mythology, expanded to astrology)

**Risks**: HIGH — no source text means no guardrails; referential integrity is fragile

---

## Cross-Cutting Principles

### Always Do
1. **Validate after every build**: Check for orphan refs, unreferenced L1 items, duplicate IDs
2. **Use consistent ID formats**: `book01-001`, `hamlet-act1-scene1`, `zeus` — lowercase, hyphenated, hierarchical
3. **Set `relationship_type: "emergence"`** on all composite (L2+) items
4. **Include attribution metadata**: source URL, author, license, translator (if applicable)
5. **Log failures and fixes**: Every grammar teaches something. Record what broke and why.

### Never Do
1. **Never assume formatting is consistent** across a large source file — check edge cases
2. **Never skip validation** — broken refs are invisible until someone uses the grammar
3. **Never batch-commit without testing** — one broken grammar can be hard to debug retroactively
4. **Never hardcode delimiters** without checking variants (period, no period, Unicode, etc.)

### Efficiency by Type

| Type | Parse Time | Content Time | Total Effort | Automation Potential |
|------|-----------|--------------|--------------|---------------------|
| From book (novel) | Low | Low | LOW | High (scripted) |
| From sacred text | Medium | Medium | MEDIUM | Medium (need manual L2 briefs) |
| From dramatic text | Medium | Low | MEDIUM | High (once parser handles edge cases) |
| From memory | None | High | HIGH | None (all hand-crafted) |

---

_Last updated: 2026-03-02_
_This document is designed to be imported into a grammar-building assistant._
