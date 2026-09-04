# Implementation Plan: Five Focus Grammars + Connected Projects

**Date:** 2026-03-15
**Status:** IN PROGRESS
**Branch:** `claude/grimm-tales-research-yasNq`

---

## GitHub Links (Direct Import)

All grammars at: `https://github.com/PlayfulProcess/recursive.eco-schemas/tree/main/grammars/`

| Grammar | Status | GitHub Path |
|---------|--------|-------------|
| **The Wise Heart (DBT)** | LIVE — 30 skills, 35 items | [`grammars/dbt-wise-heart/grammar.json`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/grammars/dbt-wise-heart/grammar.json) |
| **Plutchik's Wheel of Emotions** | LIVE — 42 items | [`grammars/plutchik-wheel-of-emotions/grammar.json`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/grammars/plutchik-wheel-of-emotions/grammar.json) |
| **The Repair Deck** | LIVE — 17 items | [`grammars/repair-an-open-source-book/grammar.json`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/grammars/repair-an-open-source-book/grammar.json) |
| **Tarot of Tarots** | PLANNED | Not yet built — see design below |
| **Mythic Journey** | PLANNED | Plan at [`plan/mythic-journey-plan.md`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/plan/mythic-journey-plan.md) |

### Supporting Files

| File | Purpose |
|------|---------|
| [`plan/grammar-ideas.md`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/plan/grammar-ideas.md) § 8 | DBT design rationale |
| [`plan/mythic-journey-plan.md`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/plan/mythic-journey-plan.md) | 24-episode character journey plan |
| [`plan/pipeline.md`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/plan/pipeline.md) | Grammar pipeline + source text catalog |
| [`compost/WHAT_IS_COMPOST.md`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/compost/WHAT_IS_COMPOST.md) | Composting philosophy |

---

## Priority Order (with rationale)

### 1. The Wise Heart — DBT Skills Through Myth ★ DONE

**Why first:** Foundation — every other grammar references these skills. Complete DBT coverage means the Mythic Journey and Plutchik wheel have a solid clinical backbone.

**Current state:** 30 L1 skills across all 4 DBT modules:
- Core Mindfulness (7): Wise Mind, Observe, Describe, Participate, Non-Judgmental, One-Mindfully, Effectively
- Distress Tolerance (10): Radical Acceptance, Turning the Mind, Self-Soothe, TIPP, Pros & Cons, Willingness, STOP, ACCEPTS, IMPROVE, Half-Smile/Willing Hands
- Emotion Regulation (8): Check the Facts, Opposite Action, Build Mastery, PLEASE, Cope Ahead, Accumulate Positives, Mindfulness of Emotions, Problem Solving
- Interpersonal Effectiveness (5): DEAR MAN, GIVE, FAST, Validation, Walking the Middle Path

### 2. Plutchik's Wheel of Emotions ★ DONE

**Why second:** Companion to DBT — teaches WHAT you're feeling (Plutchik) so you can use skills for WHAT TO DO about it (DBT).

**Current state:** 42 items — 24 primary emotions (8 × 3 intensities), 8 dyads, 8 L2 petals, 2 L3 meta. All items have character voices (Alice, Shiryo, Bishisheshi), body awareness sections, and singable mantras.

### 3. The Repair Deck ★ DONE

**Why third:** Bridges the therapeutic content (DBT/Plutchik) with the tarot infrastructure. Proves that healing content can use the oracle/draw format.

**Current state:** 17 items — 13 L1 cards, 3 L2 phases, 1 L3 meta. Reframed as "A Major Arcana for Mending."

### 4. Tarot of Tarots — NEXT TO BUILD

**Why fourth:** Meta-grammar connecting all tarot-type grammars (Rider-Waite-Smith, Alice's Tarot, Jungian Archetypes, Repair Deck, Etteilla). Shows how the same archetypes recur across systems.

**Design sketch:**
- L1: 22 archetypal positions (Fool, Magician, High Priestess, etc.)
- Each L1 has sections showing the same position across different decks
- L2: Groupings (The Journey of Innocence, The Descent, The Return)
- L3: Meta — the pattern beneath all tarots
- `connected_grammars`: links to each tarot grammar
- Grammar type: `tarot`
- ~40-50 items

**Existing tarot grammars to cross-reference:**
- [`grammars/rider-waite-smith-tarot/grammar.json`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/grammars/rider-waite-smith-tarot/grammar.json)
- [`grammars/alice-s-tarot-my-5-years-old/grammar.json`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/grammars/alice-s-tarot-my-5-years-old/grammar.json)
- [`grammars/tarot-rws-etteilla/grammar.json`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/grammars/tarot-rws-etteilla/grammar.json)
- [`grammars/repair-an-open-source-book/grammar.json`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/grammars/repair-an-open-source-book/grammar.json)

### 5. The Mythic Journey — PLANNED

**Why fifth:** Requires all of the above to be solid. The frame narrative (Alice, Shiryo, Bishisheshi visiting myths) IS the curriculum, but it depends on having the skills (DBT) and emotions (Plutchik) mapped first.

**Current plan:** 24 episodes across 5 acts — see [`plan/mythic-journey-plan.md`](https://github.com/PlayfulProcess/recursive.eco-schemas/blob/main/plan/mythic-journey-plan.md)

---

## Three Mythical Options Per Skill (Favoring Indigenous & Authentic Sources)

### Editorial Stance

For each DBT skill and Plutchik emotion, we provide three myth options:
1. **Indigenous/non-Western** (preferred) — authentic, pre-colonial
2. **Classical/world literature** — Greek, Persian, Indian epics
3. **European folk** (if needed) — only when the story genuinely serves the skill

The current grammar uses ONE myth per skill. This section provides alternatives for future versions, deeper exploration, or the Mythic Journey character episodes.

---

### DBT Wise Heart — Myth Alternatives

#### Core Mindfulness

| Skill | Current Myth | Alt 1 (Indigenous) | Alt 2 (Classical) | Alt 3 (World Folk) |
|-------|-------------|-------------------|-------------------|-------------------|
| **Wise Mind** | Blind Men & Elephant (Indian) | **Coyote and the Stars** (Navajo — Coyote scatters stars impatiently; First Woman placed them one by one, holding both wild and careful) | The Cave (Plato — shadows vs. reality) | The Tortoise and the Hare (Aesop — knowing when to rush and when to be still) |
| **Observe** | The Golden Bird (Grimm) | **Spider Woman's Web** (Hopi — she observes the world into existence, each strand placed with attention) | Arjuna's Eye (Mahabharata — he sees only the bird's eye, nothing else) | The Crane Wife (Japanese — the husband who peeks and loses everything) |
| **Describe** | Rumpelstiltskin (Grimm) | **The Naming Ceremony** (Yoruba — the child is named and their destiny is spoken into being; naming creates reality) | Isis discovers Ra's true name (Egyptian — naming gives power over even the sun god) | Baba Yaga's riddles (Russian — Vasilisa must name things correctly to survive) |
| **Participate** | Balinese Temple Dance | **The Round Dance** (Lakota Sundance — full participation with body and spirit, not as spectator) | Sufi Whirling (Rumi's sema — the dancer disappears into the dance) | Carnival masquerade (Brazilian/Afro-Brazilian — losing yourself in communal movement) |
| **Non-Judgmental** | The Farmer's Horse (Taoist) | **Iktomi and the Ducks** (Lakota — Iktomi's judgments about the ducks' foolishness lead to his own comeuppance) | The Story of the Sands (Sufi — the river must stop judging its own form to cross the desert) | Maybe Story (Taoist — already used; deeply appropriate) |
| **One-Mindfully** | Zen Master's Tea | **The Tea Ceremony** (Japanese Chanoyu — already non-Western) | The Potter at the Wheel (Indian — Kabir's verses on single-pointed attention) | Thich Nhat Hanh's Orange (Vietnamese Zen — eating one orange with full attention) |
| **Effectively** | Anansi & the Stories (Ashanti) | **Maui Fishes Up the Island** (Polynesian — uses cleverness not strength; the hook, the chant, the timing) | Nasreddin and the Smuggler (Sufi — the border guard searched the donkeys for years; Nasreddin was smuggling donkeys) | Brer Rabbit and the Tar Baby (African-American — trickster wisdom, doing what works) |

#### Distress Tolerance

| Skill | Current Myth | Alt 1 (Indigenous) | Alt 2 (Classical) | Alt 3 (World Folk) |
|-------|-------------|-------------------|-------------------|-------------------|
| **Radical Acceptance** | Inanna's Descent (Sumerian) | **Changing Woman** (Navajo/Diné — she accepts every phase: youth, maturity, old age, and renewal; the seasons ARE her body) | Persephone's descent (Greek — she eats the pomegranate and accepts the underworld as part of her home) | The Stonecutter (Japanese — who wants to be the sun, the cloud, the rock, and finally accepts being himself) |
| **Turning the Mind** | Orpheus & Eurydice (Greek) | **Sedna's Choice** (Inuit — she keeps choosing to tend the sea creatures despite her rage at her father; turning toward care again and again) | Lot's Wife (Hebrew — she looked back; the story of what happens when you CAN'T turn the mind) | Momotarō's departure (Japanese — the peach boy keeps choosing to walk forward, leaving home behind) |
| **Self-Soothe** | Thumbelina's Winter (Andersen) | **The Grandmother Spider's Blanket** (Cherokee — Spider Grandmother weaves warmth and light; she brings fire wrapped in a small pot) | The Garden of the Hesperides (Greek — a place of golden peace, where even Heracles rested) | The Snow Child (Russian — Snegurochka, made of snow, finds warmth dangerous but love soothing) |
| **TIPP** | Jonah in the Whale (Hebrew) | **Maui in the Belly of the Fish** (Polynesian — swallowed by his ancestor the fish, he uses fire to survive and emerges transformed) | Heracles in the Sea Monster (Greek — swallowed, he cuts his way out; the body does what the mind cannot) | The Fire Bird's Feather (Russian — the cold of the forest vs. the heat of the quest; body regulation) |
| **Pros and Cons** | Odysseus & the Sirens (Greek) | **Raven Steals the Sun** (Haida/Tlingit — Raven weighs: keep the sun for himself or share it? Planned before acting) | The Judgment of Paris (Greek — three options, irreversible consequences) | Nasreddin's Donkey (Sufi — should he ride, walk, or carry the donkey? Every choice has critics) |
| **Willingness** | Psyche's Tasks (Greek/Roman) | **The Woman Who Fell from the Sky** (Haudenosaunee/Iroquois — Sky Woman falls, the animals catch her; she is willing to land in the unknown and build a world on Turtle's back) | Sita's Fire (Ramayana — Sita walks into the fire willingly; her willingness proves what force cannot) | The Handless Maiden (Grimm) — she walks into the forest with no hands; willingness beyond capability |
| **STOP** | The Salt Prince (Czech/European) | **How Coyote Got His Name** (Salish — Coyote acts before thinking and transforms the world in messy ways; the story of what happens when you DON'T stop) | Pandora (Greek — she didn't stop; but Hope remained when she finally did) | The Drum (West African — the boy who hit the drum before asking what it did) |
| **ACCEPTS** | Scheherazade (Persian/Arabic) | **The Women Who Saved the Village** (Igbo — when warriors couldn't fight, the women distracted the invaders with dance, food, stories; survival through creative redirection) | Penelope's Weaving (Greek — she wove by day, unraveled by night; distraction as strategic survival) | Brer Rabbit's Laughing Place (African-American — a place to go when you need to survive the moment) |
| **IMPROVE** | Vasilisa & the Doll (Russian) | **The Corn Mother** (Penobscot/Wabanaki — she dies so the people can eat; from her body grows corn; finding meaning in sacrifice, improving unbearable loss) | Ariadne's Thread (Greek — she gives Theseus something small to hold in the dark; one thing that makes the labyrinth survivable) | Muso Koroni's Seeds (Bambara/West African — the first woman plants comfort in the dark earth) |
| **Half-Smile/Willing Hands** | Buddha & Angulimala (Indian) | **The Peaceful Warrior Code** (Lakota — the concept of *wacante ognaka*, "to put in the heart"; warriors who chose open-hearted stance even in battle) | The Bhagavad Gita: Krishna's Smile (Indian — Krishna smiles while revealing the cosmic form; the face of peace amid overwhelming reality) | Quan Yin's Open Hands (Chinese Buddhist — she who hears the cries; her hands are always open) |

#### Emotion Regulation

| Skill | Current Myth | Alt 1 (Indigenous) | Alt 2 (Classical) | Alt 3 (World Folk) |
|-------|-------------|-------------------|-------------------|-------------------|
| **Check the Facts** | Chicken Little (English) | **Anansi and the Moss-Covered Rock** (Ashanti — animals keep fainting near the rock without checking why; Anansi investigates) | The Boy Who Cried Wolf (Aesop) | Nasreddin and the Moonlight (Sufi — the moon's reflection in the well; is it really the moon?) |
| **Opposite Action** | North Wind & Sun (Aesop) | **Rabbit and the Moon** (Cree — Rabbit is terrified of her own shadow; she runs from it until she learns to walk TOWARD it and it becomes small) | Tam Lin (Scottish — Janet holds Tam Lin through every terrifying transformation; opposite of letting go) | The Girl Who Married the Moon (Alutiiq/Sugpiaq — she approaches what everyone else fled) |
| **Build Mastery** | Ugly Duckling (Andersen) | **The Eagle Boy** (Zuni/Pueblo — a boy mocked by his village is raised by eagles; he masters flight not by pretending to be an eagle but by learning HIS way of flying) | Atalanta's Races (Greek — she trained until no one could beat her; mastery through practice, not luck) | Momotarō's training (Japanese — the peach boy practices before the quest, building skill one day at a time) |
| **PLEASE** | Elves & Shoemaker (Grimm) | **The Medicine Wheel** (Pan-Indigenous/Plains — the four directions of self-care: physical, emotional, mental, spiritual; each must be tended) | Asklepios's Temple Sleep (Greek — the god of healing prescribed REST; patients slept in the temple and woke healed) | The Tired Mountain (Japanese — even mountains need to rest; the mountain that sat down) |
| **Cope Ahead** | Theseus & Labyrinth (Greek) | **How Raven Prepared for Winter** (Pacific Northwest — Raven stores food, makes plans, prepares shelter BEFORE the cold comes; the ones who don't prepare become the stories that warn) | The Cattle Raid (Irish — Cú Chulainn's preparation, checking weapons, scouting the ford) | Monkey King and the Peach Garden (Chinese — Sun Wukong plans his theft step by step before acting) |
| **Accumulate Positives** | Stone Soup (European) | **The Gift-Giving Ceremony** (Pacific Northwest Potlatch — accumulating TO GIVE; the richest person is the one who has given the most away) | The Garden of Simple Joys (Sufi — Rumi's poem about collecting small beauties) | The Lucky Bean (Brazilian — each day you move a bean from one pocket to another for each good moment) |
| **Mindfulness of Emotions** | Sedna & the Sea (Inuit) | **Already used — Sedna IS indigenous** | The River That Couldn't Stop (Hindu — Ganga's descent; Shiva held her in his hair so she wouldn't flood the world; containing without suppressing) | Tangaroa's Ocean (Polynesian — the ocean god holds all storms and calms within himself) |
| **Problem Solving** | Anansi & Pot of Wisdom (Ashanti) | **Already used — Anansi IS indigenous** | Daedalus and the Labyrinth (Greek — the problem-solver who built both the trap AND the escape) | Birbal's Wisdom (Indian — Akbar's advisor who solved impossible problems with lateral thinking) |

#### Interpersonal Effectiveness

| Skill | Current Myth | Alt 1 (Indigenous) | Alt 2 (Classical) | Alt 3 (World Folk) |
|-------|-------------|-------------------|-------------------|-------------------|
| **DEAR MAN** | Scheherazade (Persian) | **How Grandmother Spider Brought the Light** (Muskogee/Cherokee — she asked, described what she needed, expressed why, and reinforced the community's benefit) | Savitri and Yama (Indian — she argued with the god of Death using logic, persistence, and emotional truth until he returned her husband) | Queen Esther (Hebrew — she described, expressed, asserted, and reinforced before the king, saving her people) |
| **GIVE** | The Giving Tree (Silverstein) | **The Legend of the Three Sisters** (Haudenosaunee — corn, beans, squash give to each other without depleting; mutuality, not sacrifice) | The Fisherman and the Jinni (Arabian Nights — mutual release; the fisherman frees the jinni, the jinni rewards the fisherman; giving that multiplies) | Momotarō's Companions (Japanese — the dog, monkey, and pheasant give their skills to the quest and receive belonging in return) |
| **FAST** | Nasreddin & the Judge (Sufi) | **Coyote Stands His Ground** (various Plains nations — Coyote maintains his self-respect even when tricked; "I meant to do that") | Antigone (Greek — she maintains her values against the king's law; self-respect costs everything and is worth it) | The Clever Daughter (Italian — she outsmarts the king's tests without losing her dignity) |
| **Validation** | Velveteen Rabbit (Williams) | **The Talking Tree** (Yoruba — the tree that listens to everyone's stories without judgment; being heard makes you real) | Enkidu and Shamhat (Sumerian — Shamhat sees Enkidu as he is, wild and real, and by seeing him truly, makes him human) | The Mirror of Matsuyama (Japanese — the mirror that shows you who you really are; being seen as your true self) |
| **Walking the Middle Path** | The Two Wolves (Cherokee) | **Already used — the Two Wolves IS indigenous** | Arjuna's Dilemma (Bhagavad Gita — he must fight his own family; neither pure war nor pure peace is the answer; Krishna teaches the middle path of duty held with detachment) | Nasreddin's Two Wives (Sufi — each wife pulls him in opposite directions; his solution holds both without choosing) |

---

### Plutchik Wheel — Myth Alternatives

#### Primary Emotions (24 items: 8 × 3 intensities)

| Emotion | Current Myth | Alt 1 (Indigenous) | Alt 2 (Classical) |
|---------|-------------|-------------------|-------------------|
| **Ecstasy** (intense joy) | Krishna's Dance | **Ghost Dance Vision** (Lakota — Wovoka's vision of ecstatic reunion with the ancestors; joy beyond the body) | Dionysus and the Maenads (Greek — ecstasy as divine possession) |
| **Joy** (core) | Anansi Wins the Stories | **The First Sunrise** (Aboriginal Australian — when the sun first rose, the world rejoiced; pure foundational joy) | Aphrodite's Birth (Greek — beauty emerging from the sea) |
| **Serenity** (mild joy) | The Tao Garden | **The Corn Pollen Path** (Navajo — Beauty Way ceremony; walking in beauty, surrounded by beauty, serenity is the path) | The Lotus Sutra's Pure Land (Buddhist — stillness at the heart of the cosmos) |
| **Rage** (intense anger) | Kali's Dance | **Pele's Eruption** (Hawaiian — the volcano goddess whose rage creates new land; destruction as creation) | Achilles over Patroclus (Greek — rage so great it remade the battlefield) |
| **Anger** (core) | Thor's Stolen Hammer | **Maui Snares the Sun** (Polynesian — furious that the sun moves too fast, he beats it until it slows) | The Iliad's Wrath (Greek — menin, the first word of Western literature) |
| **Annoyance** (mild anger) | The Princess and the Pea | **Coyote's Itchy Nose** (various Plains — Coyote can't stop scratching; the small irritation that won't go away) | Nasreddin's Neighbor's Hammer (Sufi — borrowed and never returned; mild indignation) |
| **Terror** (intense fear) | Lot's Wife | **Windigo** (Algonquian — the ice-heart monster; terror that freezes you into what you fear) | Medusa (Greek — terror so great it turns you to stone) |
| **Fear** (core) | Theseus in the Labyrinth | **The Stick-Thin Woman** (Tlingit — alone in the forest with something wrong; fear with reason) | Dante enters Hell (Italian — midway through life's journey, in a dark wood) |
| **Apprehension** (mild fear) | Hansel and Gretel | **The Fog People** (Tlingit — the ones who live just beyond the edge of the village; the unease of what might be there) | Odysseus approaching Scylla (Greek — knowing what's coming, walking toward it anyway) |
| **Amazement** (intense surprise) | The Metamorphoses | **Raven Releases the Sun** (Haida — the moment the box opens and light pours into the world; the gasp) | Moses Parts the Sea (Hebrew — the impossible becoming real before your eyes) |
| **Surprise** (core) | Jack and the Beanstalk | **The Star People** (Pawnee — a young woman climbs to the sky world and finds it completely different from what she expected) | Siddhartha Leaves the Palace (Indian — the prince sees suffering for the first time) |
| **Distraction** (mild surprise) | The Bremen Town Musicians | **Iktomi's Interrupted Meal** (Lakota — the trickster keeps being distracted from his feast by his own curiosity) | The Dog and the Shadow (Aesop — distracted by the reflection, drops the bone) |
| **Grief** (intense sadness) | Gilgamesh (Sumerian) | **Already used — Gilgamesh IS from an indigenous Mesopotamian tradition** | Niobe (Greek — wept until she became stone; grief beyond human form) |
| **Sadness** (core) | Orpheus's Song | **The Weeping Woman** (Aztec/Mexican — La Llorona, sadness that echoes through the waters forever) | The Willow Wife (Japanese — she weeps when the tree is cut; sadness for what cannot be undone) |
| **Pensiveness** (mild sadness) | The Little Match Girl | **The Old Woman Who Lost Her Blanket** (Abenaki — the gentle melancholy of loss that doesn't scream but aches) | The Fisherman's Wife (Japanese — she waits by the sea, thinking of what was) |
| **Loathing** (intense disgust) | Medea's Revenge | **The Cannibal Dance** (Kwakwaka'wakw — Hamatsa ceremony; confronting what repels to transform it into power) | Dante's lowest circle (Italian — the frozen lake of ultimate betrayal and revulsion) |
| **Disgust** (core) | Narcissus at the Pool | **The Dirty Boy** (Blackfoot — the boy who was disgusting to everyone until they saw his true form; disgust reversed) | Midas (Greek — everything he touched turned to gold, including his food; abundance becoming revolting) |
| **Boredom** (mild disgust) | The Fisherman's Wife | **Coyote's Yawn** (various — when Coyote gets bored, he creates mischief; boredom as the mother of bad ideas) | Princess Nobody (Fairy tale — the princess who had everything and wanted nothing) |
| **Admiration** (intense trust) | The Bodhisattva Tales | **White Buffalo Calf Woman** (Lakota — she brings the sacred pipe; admiration that transforms the community) | Hanuman's Devotion (Indian — he tears open his chest to show Rama in his heart; trust made visible) |
| **Trust** (core) | Demeter & Persephone | **The Boy and the Eagle** (Zuni — a boy trusts an eagle to carry him; the eagle trusts the boy to release him) | Ruth and Naomi (Hebrew — where you go, I will go) |
| **Acceptance** (mild trust) | The Prodigal Son | **The Salmon People** (Pacific Northwest — the salmon accept their journey upstream; they do not fight the current, they become part of it) | Epictetus's Cup (Stoic — when your cup breaks, say: I knew it was breakable) |
| **Vigilance** (intense anticipation) | Heimdall at the Bridge | **The Sentinels** (various Plains — the scouts who stayed awake all night watching for what was coming; vigilance as service) | Argus the Hundred-Eyed (Greek — all-seeing guardian, never sleeping) |
| **Anticipation** (core) | Pandora's Box | **The Night Before the Hunt** (San/Bushmen — the preparation, the sharpening, the reading of signs; anticipation as sacred attention) | Penelope's Waiting (Greek — 20 years of expecting, preparing, maintaining) |
| **Interest** (mild anticipation) | The Curious Monkey | **Coyote Wants to Know** (various — Coyote's curiosity IS the story; interest as the engine of creation and trouble) | The Little Prince's Questions (Saint-Exupéry — asking about each planet, each rose, each star) |

---

## Tarot of Tarots — Design Concept

### The Idea

A meta-grammar that maps the 22 Major Arcana positions across every tarot grammar in the repository. Not a new tarot deck — a study tool showing how the same archetypal positions manifest differently in different systems.

### Structure

| Level | Content | Est. Items |
|-------|---------|-----------|
| L1 | 22 archetypal positions (0-XXI) | 22 |
| L2 | 3 journey phases (Innocence → Descent → Return) | 3 |
| L3 | 1 meta — "The Pattern Beneath" | 1 |
| **Total** | | **26** |

### L1 Item Sections

Each of the 22 positions would include:

```json
{
  "sections": {
    "The Archetype": "What this position represents across all systems",
    "Rider-Waite-Smith": "Description and symbolism from the RWS tradition",
    "Alice's Tarot": "How this archetype appears in the Alice deck for children",
    "Etteilla": "The pre-Waite cartomancy interpretation",
    "The Repair Deck": "If this position has a Repair Deck equivalent, how mending reframes the archetype",
    "Jungian Reading": "The archetypal psychology behind this position",
    "For Practice": "Questions for self-reflection using this archetype"
  }
}
```

### Connected Grammars

```json
"connected_grammars": [
  { "grammar_id": "rider-waite-smith-tarot", "relationship": "primary-reference" },
  { "grammar_id": "alice-s-tarot-my-5-years-old", "relationship": "children's-adaptation" },
  { "grammar_id": "tarot-rws-etteilla", "relationship": "historical-precursor" },
  { "grammar_id": "repair-an-open-source-book", "relationship": "therapeutic-reframe" }
]
```

---

## Build Order

1. ~~Complete DBT Wise Heart (30 skills)~~ ✓ DONE
2. ~~Deepen Plutchik dyads (character voices + body sections)~~ ✓ DONE
3. Build Tarot of Tarots meta-grammar
4. Expand Mythic Journey with 3 myth options per episode (this document)
5. Begin Mythic Journey grammar: Episodes 1 + 24 (frame), then Act I

---

## Character Voice Deepening Notes

### Alice
- References her own Wonderland/Looking-Glass experiences constantly
- Argues with authority but has learned from it
- Her directness meets emotional content → unexpected vulnerability
- Pattern: she recognizes a feeling from her adventures, names it precisely, then reveals something she learned from it

### Shiryo
- Translates emotions into system language first ("feedback loop," "diagnostic," "error log")
- Then discovers the translation FAILS — and the failure is the learning
- His indicator light changes color with emotions — this is involuntary, like a blush
- Pattern: logical analysis → honest confusion → physical response he can't control → quiet understanding

### Bishisheshi
- Never speaks. Acts.
- She IS the embodied truth — she demonstrates the skill without knowing its name
- Curls up in warmth (self-soothe), arches her back (boundaries), pounces with full attention (participate), purrs for no reason (serenity)
- Pattern: while Alice and Shiryo talk about it, Bishisheshi DOES it — and they notice

### The Dialectic
Alice = Reasonable Mind (questions everything)
Bishisheshi = Emotion Mind (embodies everything)
Shiryo = learning Wise Mind (holds both)

---

_This plan is a living document. Updated as grammars are built._
