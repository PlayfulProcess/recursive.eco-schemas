# Children's Stories Grammar — Design Plan

## Concept

**"The Story Tree: Best Children's Stories for Every Age"** — a curated grammar of ~30 essential stories from fables, fairy tales, myths, folk tales, and classic literature. Each story is a single L1 item with **four tellings** (preschool, classic, cultural roots, modern reflection), making it a unique multi-age resource. Stories cross-link to their full source grammars already in the repository.

## What Makes This Grammar Unique

Unlike existing grammars that contain a single version of each story, this grammar presents **the same story at multiple levels**:
- A 3-year-old and a 10-year-old can both explore "The Tortoise and the Hare" — they'll just read different sections
- Parents get guidance on which version suits which age
- Cultural context shows how each story travels across traditions

## Structure (L1 / L2 / L3)

### L3 Meta-Categories (5)
The five great traditions of children's storytelling:

| ID | Name | Description |
|----|------|-------------|
| `tradition-animal-wisdom` | The Animal Teachers | Fables where animals mirror human nature |
| `tradition-enchanted-world` | The Enchanted World | Fairy tales of magic, transformation, and wonder |
| `tradition-heroes-and-tricksters` | Heroes, Gods & Tricksters | Myths and legends of extraordinary beings |
| `tradition-voices-of-the-world` | Voices of the World | Folk tales from many cultures and lands |
| `tradition-great-adventures` | The Great Adventures | Beloved classics of children's literature |

### L2 Thematic Groups (10)
Each L3 contains 2 L2 groups:

**Under Animal Teachers:**
- `group-small-and-mighty` — "The Small and the Mighty" (stories where the underdog wins)
- `group-wild-wisdom` — "Wild Wisdom" (stories of animal cleverness and nature)

**Under Enchanted World:**
- `group-transformation-tales` — "Transformation Tales" (change, becoming, breaking spells)
- `group-dark-woods` — "Into the Dark Woods" (courage in frightening places)

**Under Heroes, Gods & Tricksters:**
- `group-heroes-journey` — "The Hero's Journey" (quests, monsters, triumph)
- `group-clever-ones` — "The Clever Ones" (tricksters who outwit the powerful)

**Under Voices of the World:**
- `group-east-and-south` — "Stories from East and South" (Asian, African, Pacific)
- `group-north-and-west` — "Stories from North and West" (European, Celtic, Norse, American)

**Under Great Adventures:**
- `group-doorways` — "Through the Doorway" (portal fantasies and imaginary worlds)
- `group-growing-up` — "Growing Up" (coming-of-age adventures)

### L1 Stories (30)

Each story has these **sections**:
1. **"Preschool Telling"** — Simple, gentle language for ages 2-5. Short sentences, repetition, happy focus.
2. **"Classic Telling"** — Faithful to the best-known traditional version (~300-500 words).
3. **"Cultural Roots"** — Where this story comes from, variant versions across cultures, historical context.
4. **"Modern Reflection"** — Why this story still matters today. Contemporary parallels and deeper meaning.
5. **"For Parents"** — Age recommendations, discussion questions, tips for different developmental stages.

#### The 30 Stories:

**Animal Teachers — Small & Mighty:**
1. `tortoise-and-hare` — The Tortoise and the Hare (Aesop) → `aesops-fables`
2. `lion-and-mouse` — The Lion and the Mouse (Aesop) → `aesops-fables`
3. `boy-who-cried-wolf` — The Boy Who Cried Wolf (Aesop) → `aesops-fables`
4. `ugly-duckling` — The Ugly Duckling (Andersen) → `andersens-fairy-tales`

**Animal Teachers — Wild Wisdom:**
5. `jungle-book-mowgli` — Mowgli and the Jungle (Kipling) → `jungle-book`
6. `how-elephant-got-trunk` — How the Elephant Got His Trunk (Kipling) → `just-so-stories`
7. `brer-rabbit-tar-baby` — Brer Rabbit and the Tar Baby (African-American)

**Enchanted World — Transformation:**
8. `cinderella` — Cinderella (Grimm/Perrault) → `grimms-fairy-tales`
9. `frog-prince` — The Frog Prince (Grimm) → `grimms-fairy-tales`
10. `snow-queen` — The Snow Queen (Andersen) → `andersens-fairy-tales`
11. `beauty-and-beast` — Beauty and the Beast (Beaumont)

**Enchanted World — Dark Woods:**
12. `hansel-and-gretel` — Hansel and Gretel (Grimm) → `grimms-fairy-tales`
13. `sleeping-beauty` — Sleeping Beauty (Grimm/Perrault) → `grimms-fairy-tales`
14. `jack-and-beanstalk` — Jack and the Beanstalk (English)
15. `red-riding-hood` — Little Red Riding Hood (Grimm/Perrault) → `grimms-fairy-tales`

**Heroes — Hero's Journey:**
16. `theseus-minotaur` — Theseus and the Minotaur (Greek) → `greek-mythology`, `bulfinch-s-classical-mythology`
17. `perseus-medusa` — Perseus and Medusa (Greek) → `greek-mythology`, `bulfinch-s-classical-mythology`
18. `thor-and-giants` — Thor and the Giants (Norse) → `prose-edda`
19. `mulan` — The Ballad of Mulan (Chinese) → `myths-china-japan`

**Heroes — Clever Ones:**
20. `anansi-spider` — Anansi the Spider (West African) → `west-african-folk-tales`
21. `emperor-new-clothes` — The Emperor's New Clothes (Andersen) → `andersens-fairy-tales`
22. `puss-in-boots` — Puss in Boots (Perrault)

**Voices — East & South:**
23. `momotaro` — Momotaro the Peach Boy (Japanese) → `japanese-fairy-tales`
24. `firebird` — The Firebird (Russian) → `russian-folk-tales`
25. `magic-paintbrush` — The Magic Paintbrush (Chinese)

**Voices — North & West:**
26. `selkie` — The Selkie Wife (Celtic) → `celtic-fairy-tales`
27. `stone-soup` — Stone Soup (European folk tale)
28. `paul-bunyan` — Paul Bunyan (American tall tale)

**Adventures — Doorways:**
29. `alice-wonderland` — Alice in Wonderland (Carroll) → `alice-in-wonderland-chapter-book`
30. `wizard-of-oz` — The Wonderful Wizard of Oz (Baum) → `wonderful-wizard-of-oz`

**Adventures — Growing Up:**
31. `peter-pan` — Peter Pan (Barrie) → `peter-pan`
32. `pinocchio` — Pinocchio (Collodi) → `adventures-of-pinocchio`
33. `secret-garden` — The Secret Garden (Burnett) → `secret-garden`

## Cross-Linking Strategy

Each L1 item includes a `grammars` array with GitHub links:
```json
"grammars": ["https://github.com/PlayfulProcess/recursive.eco-schemas/tree/main/grammars/aesops-fables"]
```

This connects each curated retelling to its full source grammar, letting users dive deeper.

## Implementation Plan

### Phase 1: Skeleton (Write tool)
- Write complete grammar.json with all 48 items (33 L1 + 10 L2 + 5 L3)
- All metadata, IDs, sort_orders, composite_of refs, grammars links
- All sections set to `"Placeholder."`
- Validate + commit

### Phase 2: Fill L3 meta-categories (Edit tool, 5 items)
- Write "About" and "For Parents" sections for each tradition

### Phase 3: Fill L2 thematic groups (Edit tool, 10 items)
- Write "About" and "For Parents" sections for each group

### Phase 4: Fill L1 stories (Edit tool, 33 items)
- Fill all 5 sections per story, working group by group
- ~33 edit passes, each replacing placeholder with ~800-1200 words of content

### Phase 5: Validate + manifest + push
- Run validation
- Update manifest
- Final commit and push

## Grammar Metadata

```json
{
  "name": "The Story Tree: Children's Stories for Every Age",
  "grammar_type": "custom",
  "tags": ["children", "stories", "fables", "fairy-tales", "myths", "folk-tales", "parenting", "multi-age"],
  "roots": ["western-canon", "eastern-wisdom", "indigenous-knowledge", "oral-tradition"],
  "shelves": ["children", "wonder", "wisdom"],
  "lineages": ["Shrei", "Gottman"],
  "worldview": "pluralist"
}
```

## Total Item Count
- 5 L3 meta-categories
- 10 L2 thematic groups
- 33 L1 stories
- **48 items total**
- **165 content sections** to fill (33 stories × 5 sections each)
