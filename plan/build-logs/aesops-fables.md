# Build Log: Aesop's Fables

**Grammar**: `kids/aesops-fables/grammar.json`
**Source**: `sources/aesops-fables` (Project Gutenberg, V.S. Vernon Jones translation)
**Type**: from-source-text
**Status**: COMPLETE
**Items**: 310 (284 L1 fables + 15 L2 animal groups + 9 L2 moral themes + 2 L3 meta-categories)
**File size**: 414KB

---

## Source Analysis

- Origin: Project Gutenberg eBook #21, V.S. Vernon Jones translation with G.K. Chesterton introduction
- Structure: Each fable has a title in ALL CAPS, followed by story paragraphs, ending with a moral
- Morals appear either inline at the end or on a separate line
- Some fables have very short stories (2-3 sentences), others run several paragraphs

## Strategy

| Step | Approach | Result |
|------|----------|--------|
| 1. Fable detection | Split on ALL CAPS title lines | SUCCESS — 284 fables found |
| 2. Story extraction | Everything between title and moral line | SUCCESS |
| 3. Moral extraction | Look for "Moral:" or final aphoristic sentence | SUCCESS |
| 4. Category assignment | Classify by primary animal character | SUCCESS — 6 categories |
| 5. Keyword tagging | Extract animal names and theme words | SUCCESS |

## Key Learnings

- **Background agent approach works well for structured texts.** The clear title/story/moral pattern made this straightforward for an agent to parse without timeouts.
- **Category assignment by animal protagonist** creates useful filter groupings: fox-fables (27), lion-fables (20), wolf-fables (18), bird-fables (37), human-fables (71), other-animal-fables (111).
- **Morals are the natural "Summary" section.** Each fable's moral maps perfectly to a brief takeaway.
- **Children's content benefits from a "Reflection" section** — a question or prompt that helps young readers connect the story to their own experience.

## Reusable Patterns

- **Fable collections** follow title → story → moral pattern consistently
- **Animal-based categorization** works for any bestiary or fable collection
- Agent-based parsing is ideal when the text structure is regular and the file isn't too large (~5000 lines or less)

## Emergence Layer (L2/L3)

Added in a second pass after the initial build:

| Level | Category | Count | Examples |
|-------|----------|-------|---------|
| L2 | Animal groups | 15 | Fox (31), Bird (41), Lion (30), Wolf (24), Small Creatures (41), Dog (23), etc. |
| L2 | Moral themes | 9 | Friendship & Loyalty (95), Greed & Contentment (93), Pride & Vanity (87), etc. |
| L3 | Meta-categories | 2 | The Animal Kingdom, Life Lessons |

### Emergence Key Learnings

- **When there's no natural hierarchy (no chapters, no acts), create one.** Fable collections are flat — every fable is a peer. The emergence layer makes them navigable by giving parents/teachers two browsing axes: "What animal does my child like?" and "What lesson do I want to teach?"
- **Use word-boundary regex for animal detection in titles.** Without `\b` boundaries, "ox" matches "fox" and inflates cattle counts. Pattern: `r'\bfox\b'` not `'fox'`.
- **A fable can belong to multiple L2 groups** — "The Fox and the Lion" appears in both Fox Fables and Lion Fables. This is correct behavior. `composite_of` supports overlapping membership.
- **Moral themes are derived from keyword tags, not from the explicit moral text.** Only 89 of 284 fables have an explicit moral; the rest have morals "woven into the tale." Keywords are the more reliable classification signal.
- **L2 items need practical guidance sections.** "For Parents" sections explain when to use each group ("Browse these when your child is dealing with a bully" for Strength & Weakness).

## Prompt for Similar Tasks

```
Parse a fable collection where each fable has:
- Title in ALL CAPS
- Story paragraphs
- A moral at the end
Extract: title, full story, moral.
Categorize by primary animal character.
Add a reflective question for each fable.
In a second pass, add L2 emergence:
- Group by animal (using word-boundary regex on titles)
- Group by moral theme (using keyword tag intersection)
- Add L3 meta-categories for each classification axis
```
