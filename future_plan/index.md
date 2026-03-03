# Grammar Factory — Planning & Learning System

This folder is a meta-learning system for building eco-schema grammars. It tracks what works, what fails, and how to do it better — designed to feed learnings back into a website-based grammar assistant.

---

## Folder Structure

```
future_plan/
  index.md                  ← YOU ARE HERE — master overview
  principles.md             ← Key rules by grammar type (from-book, from-memory, etc.)
  pipeline.md               ← Future grammars to build + download prompts
  source-grammars-plan.md   ← Original session plan (Confucius/Zohar/Shakespeare)
  build-logs/
    confucian-analects.md   ← Build log: strategies, failures, fixes
    shakespeare-ten-greatest.md
    dhammapada.md           ← Easiest sacred text — first-try success
    zohar.md                ← Skipped — source too empty
    winnie-the-pooh.md
    alice-in-wonderland.md
    greek-mythology.md
```

---

## Grammars Built

| Grammar | Type | Items | L1 | L2 | L3 | Log |
|---------|------|------:|---:|---:|---:|-----|
| Alice in Wonderland | from-book | 59 | 47 | 12 | — | [log](build-logs/alice-in-wonderland.md) |
| Winnie-the-Pooh | from-book | 41 | 31 | 10 | — | [log](build-logs/winnie-the-pooh.md) |
| Confucian Analects | from-sacred-text | 749 | 729 | 20 | — | [log](build-logs/confucian-analects.md) |
| Dhammapada | from-sacred-text | 431 | 405 | 26 | — | [log](build-logs/dhammapada.md) |
| Shakespeare (10 plays) | from-dramatic-text | 247 | 187 | 50 | 10 | [log](build-logs/shakespeare-ten-greatest.md) |
| Greek Mythology | from-memory | 102 | 20 | 15 | 15 | [log](build-logs/greek-mythology.md) |
| Zohar | from-sacred-text | — | — | — | — | [log](build-logs/zohar.md) (skipped) |

**Total items across all grammars: ~1,629**

---

## Failure Registry

A quick-reference of strategies that failed, so the website assistant can avoid them:

| Grammar | What Failed | Why | Fix |
|---------|------------|-----|-----|
| Confucius | `\n\n` paragraph splitting | No blank lines between passages in sacred text formatting | Split on `\n(?=   [A-Z])` (speaker attribution pattern) |
| Shakespeare | Straight-quote title matching | Gutenberg uses Unicode curly apostrophe (U+2019) | Use actual Unicode char in lookup |
| Shakespeare | `^ACT ([IVX]+)$` strict regex | Some plays use `ACT I.` (trailing period) | `^ACT ([IVX]+)\.?\s*$` |
| Greek Mythology | Name renames without ref updates | Changed item IDs but forgot composite_of arrays | Always validate refs after any ID change |
| Zohar | Parsing source file | Source is 95% empty — only 7 of 53 sections have text | Need different source (Sefaria or sacred-texts.com) |

---

## Success Registry

Strategies that worked well and should be reused:

| Strategy | Applies To | Details |
|----------|-----------|---------|
| Speaker attribution splitting | Sacred texts | `\n(?=   [A-Z])` reliably finds new teachings in indentation-based texts |
| TOC title matching | Multi-work collections | Match TOC entries as standalone lines to find work boundaries |
| 2nd ACT I detection | Plays | Skip Dramatis Personae/TOC by finding the 2nd occurrence of "ACT I" |
| Centered number detection | Numbered books/chapters | `^\s+(\d+)\s*$` finds centered book numbers |
| Multi-audience sections | Children's books | "Original Text" + "For Young Readers" + "What Happens" serves multiple reading levels |
| 3-level hierarchy for drama | Plays | Scene → Act → Play maps perfectly to L1 → L2 → L3 |
| Post-build validation | All grammars | Check orphan refs, unreferenced L1, duplicate IDs after every build |
| Verse-number splitting | Sacred texts | `^\d+\.\s` at line start reliably finds numbered verses (Dhammapada — first-try success) |

---

## Grammar Types & Effort Matrix

| Type | Parse | Content | Validate | Total | Automation |
|------|-------|---------|----------|-------|------------|
| **from-book** (novel) | Easy | Low | Easy | LOW | High |
| **from-sacred-text** | Tricky | Medium | Easy | MEDIUM | Medium |
| **from-dramatic-text** | Medium | Low | Easy | MEDIUM | High |
| **from-memory** | N/A | High | Must do manually | HIGH | None |

---

## How to Use This System

### As a developer
1. Check `pipeline.md` for what to build next
2. Run the download prompt to get the source text
3. Check `principles.md` for the relevant grammar type's rules
4. Build the grammar
5. Create a new log file in `build-logs/` documenting what worked and what didn't
6. Update this index

### As the website assistant
1. Import `principles.md` as system instructions
2. Import the `Failure Registry` above to avoid known pitfalls
3. Import the `Success Registry` above to reuse proven strategies
4. Use the log files as few-shot examples of the build process

---

_Last updated: 2026-03-03_
_Branch: claude/review-source-grammar-nmK0B_
