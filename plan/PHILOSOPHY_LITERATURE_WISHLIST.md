# Philosophy, Literature & Poetry Library Wishlist

**Date:** 2026-03-06
**Purpose:** Comprehensive wishlist of texts for grammars, organized as intellectual lineages leading toward Tillich, Deleuze, and the broader library vision. Includes Gutenberg download commands where available and notes on texts requiring other sources.

---

## How to Use This Document

### Texts Available on Project Gutenberg
Each section includes bash commands you can copy-paste to download locally and push to the branch:

```bash
curl -L -o seeds/<filename>.txt "https://www.gutenberg.org/cache/epub/<ID>/pg<ID>.txt" && \
git add seeds/<filename>.txt && \
git commit -m "Add <Title> source text (Gutenberg #<ID>)" && \
git push origin claude/merge-iching-grammar-ND6pW
```

### Texts NOT on Gutenberg
Marked with `[NOT PD]` (not public domain) or `[ALT SOURCE]` (public domain but not on Gutenberg). Notes explain where to find them.

### Already Built
Marked with `[DONE]` — grammar already exists in `grammars/`.

---

## 1. PHILOSOPHY: Roads to Tillich & Deleuze

### The Tillich Line (Existential Theology)
*Plato → Kant → Hegel → Schelling → Kierkegaard → Nietzsche → Tillich*

Tillich's "ground of being" draws on German Idealism, existentialism, and Protestant theology. His key insight — that faith is "ultimate concern," not belief — synthesizes Hegel's dialectic with Kierkegaard's leap.

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 1 | Republic | Plato / Jowett | 1497 | — | Foundation of Western philosophy |
| 2 | Symposium | Plato / Jowett | 1600 | [DONE] | Already built |
| 3 | Phaedrus | Plato / Jowett | 1636 | [DONE] | Already built |
| 4 | Apology / Crito / Phaedo | Plato / Jowett | 1656 | — | Socrates' trial and death |
| 5 | Timaeus | Plato / Jowett | 1572 | — | Cosmology, demiurge |
| 6 | Critique of Pure Reason | Kant / Meiklejohn | 4280 | [DONE] | Already built |
| 7 | Critique of Practical Reason | Kant / Abbott | 5683 | — | Moral law, categorical imperative |
| 8 | Phenomenology of Spirit | Hegel / Baillie | 39064 | — | Master-slave dialectic, Absolute Spirit |
| 9 | Philosophy of Right | Hegel / Dyde | 39297 | — | State, civil society, ethical life |
| 10 | Philosophy of History | Hegel / Sibree | 1900 | — | World-historical spirit |
| 11 | Either/Or (excerpts) | Kierkegaard | — | [NOT PD] | English translations still under copyright; Danish originals may be PD |
| 12 | Fear and Trembling | Kierkegaard | — | [NOT PD] | Same — seek Swenson/Lowrie translations in libraries |
| 13 | Sickness Unto Death | Kierkegaard | — | [NOT PD] | Key existentialist text on despair |
| 14 | Beyond Good and Evil | Nietzsche / Zimmern | 4363 | [DONE] | Already built |
| 15 | Thus Spoke Zarathustra | Nietzsche / Common | 1998 | [DONE] | Already built |
| 16 | **Paul Tillich** — all major works | — | — | [NOT PD] | Died 1965. *Systematic Theology*, *The Courage to Be*, *Dynamics of Faith* all under copyright. Essential but must be sourced from libraries/bookstores. |

### The Deleuze Line (Immanence & Difference)
*Spinoza → Leibniz → Hume → Nietzsche → Bergson → Deleuze*

Deleuze's philosophy of difference, becoming, and immanence draws on Spinoza's monism, Leibniz's monadology, Hume's empiricism, Nietzsche's eternal return, and Bergson's duration.

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 17 | Ethics | Spinoza / Elwes | 3800 | [DONE] | Already built |
| 18 | Monadology | Leibniz | 39441 | — | 90 propositions on substance and harmony |
| 19 | Treatise of Human Nature | Hume | 4705 | — | Empiricism, causation, identity |
| 20 | Enquiry Concerning Human Understanding | Hume | 9662 | — | Shorter, more accessible |
| 21 | The Gay Science | Nietzsche / Common | 52881 | — | Eternal return, death of God, amor fati |
| 22 | Birth of Tragedy | Nietzsche / Haussmann | 7205 | — | Apollo vs Dionysus |
| 23 | Creative Evolution | Bergson / Mitchell | 26163 | [DONE] | Already built |
| 24 | Matter and Memory | Bergson / Paul & Palmer | 57898 | — | Duration, perception, virtual/actual |
| 25 | Time and Free Will | Bergson / Pogson | 56674 | — | Duration vs spatialized time |
| 26 | **Gilles Deleuze** — all works | — | — | [NOT PD] | Died 1995. *Difference and Repetition*, *Anti-Oedipus*, *A Thousand Plateaus*, *Logic of Sense* all under copyright. |

### Shared Foundations (Both Lines)

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 27 | Meditations | Marcus Aurelius / Long | 2680 | [DONE] | Already built |
| 28 | Enchiridion | Epictetus / Higginson | 45109 | [DONE] | Already built |
| 29 | Discourses | Epictetus / Long | 10661 | [DONE] | Already built |
| 30 | The World as Will and Idea | Schopenhauer / Haldane | 38427 | — | Vol 1. Pessimism, will, representation |
| 31 | Pragmatism | William James | 5116 | [DONE] | Already built |
| 32 | Varieties of Religious Experience | William James | 621 | [DONE] | Already built |
| 33 | Principles of Psychology | William James | 57897 | [DONE] | Already built |

---

## 2. POLITICS, SOCIAL CONTRACT & JUSTICE

### Classical Political Philosophy

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 34 | The Prince | Machiavelli / Marriott | 1232 | — | Power, statecraft, realpolitik |
| 35 | Leviathan | Hobbes | 3207 | — | Social contract, sovereign authority |
| 36 | Two Treatises of Government | Locke | 7370 | — | Natural rights, consent of governed |
| 37 | The Social Contract | Rousseau / Cole | 46333 | — | General will, popular sovereignty |
| 38 | Discourse on Inequality | Rousseau / Cole | 11136 | — | Origin of inequality, noble savage |
| 39 | Emile, or On Education | Rousseau / Payne | 5427 | — | Education, natural development |
| 40 | Confessions | Rousseau | 3913 | — | Autobiography, radical self-disclosure |
| 41 | Spirit of Laws | Montesquieu / Nugent | 27573 | — | Separation of powers, political liberty |
| 42 | On Liberty | Mill | 34901 | [DONE] | Already built |
| 43 | Utilitarianism | Mill | 11224 | — | Greatest happiness principle |
| 44 | Republic | Plato / Jowett | 1497 | — | (also listed under Philosophy) |
| 45 | Politics | Aristotle / Jowett | 6762 | — | Citizenship, constitutions, common good |

### Modern Political Thought

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 46 | Common Sense | Thomas Paine | 147 | [DONE] | Already built |
| 47 | Rights of Man | Thomas Paine | 3742 | [DONE] | Already built |
| 48 | Communist Manifesto | Marx & Engels | 61 | [DONE] | Already built |
| 49 | Capital Vol 1 | Marx / Moore & Aveling | 46423 | — | Political economy, surplus value |
| 50 | Vindication of Rights of Woman | Wollstonecraft | 3420 | [DONE] | Already built |
| 51 | Civil Disobedience | Thoreau | 71 | [DONE] | Already built |
| 52 | Walden | Thoreau | 205 | [DONE] | Already built |
| 53 | Souls of Black Folk | Du Bois | 408 | [DONE] | Already built |
| 54 | Darkwater | Du Bois | 15210 | [DONE] | Already built |
| 55 | The Negro | Du Bois | 15359 | [DONE] | Already built |
| 56 | Frederick Douglass Narrative | Douglass | 23 | [DONE] | Already built |
| 57 | Up From Slavery | Booker T. Washington | 2376 | [DONE] | Already built |
| 58 | Areopagitica | Milton | 608 | [DONE] | Already built |

### Not Available on Gutenberg (Post-1928 or No Translation)

| # | Title | Author | Notes |
|---|-------|--------|-------|
| 59 | A Theory of Justice | John Rawls (1971) | [NOT PD] Under copyright. The foundational text on justice as fairness. Library/bookstore. |
| 60 | Elements of Pure Economics | Léon Walras (1874) | [ALT SOURCE] French original may be PD; English translation (Jaffé 1954) under copyright. Check archive.org for French: *Éléments d'économie politique pure*. |
| 61 | The Human Condition | Hannah Arendt (1958) | [NOT PD] Under copyright. Labor, work, action. |
| 62 | The Wretched of the Earth | Frantz Fanon (1961) | [NOT PD] Under copyright. Essential decolonial text. |
| 63 | Pedagogy of the Oppressed | Paulo Freire (1968) | [NOT PD] Under copyright. Critical pedagogy. |

---

## 3. LITERATURE & POETRY

### American Transcendentalists & Poets

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 64 | Essays: First Series | Emerson | 2944 | [DONE] | Already built (combined in essays-emerson) |
| 65 | Essays: Second Series | Emerson | 2945 | — | "Experience", "The Poet", "Nature" |
| 66 | Nature | Emerson | 29433 | — | The original transcendentalist manifesto |
| 67 | Poems | Emerson | 12843 | — | "Brahma", "Days", "Concord Hymn" |
| 68 | Leaves of Grass | Walt Whitman | 1322 | [DONE] | Already built |
| 69 | Poems | Emily Dickinson (Series 1) | 12242 | — | "Because I could not stop for Death" |
| 70 | Poems: Series 2 | Emily Dickinson | 12341 | — | |
| 71 | Poems: Series 3 | Emily Dickinson | 12344 | — | |

### European Literature

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 72 | Siddhartha | Hermann Hesse | 2500 | — | The seeker's journey. Hesse was in analysis with J.B. Lang (Jungian), not Jung directly — but Jung deeply influenced him. The novel is a Jungian individuation narrative. |
| 73 | Faust (Part 1 & 2) | Goethe / Bayard Taylor | 14591 | — | The bargain with knowledge, the eternal feminine |
| 74 | Brothers Karamazov | Dostoevsky / Garnett | 28054 | — | Faith, doubt, the Grand Inquisitor |
| 75 | Notes from Underground | Dostoevsky / Garnett | 600 | — | The anti-rational manifesto |
| 76 | Crime and Punishment | Dostoevsky / Garnett | 2554 | — | Guilt, redemption, consciousness |
| 77 | Songs of Innocence and Experience | William Blake | 1934 | — | Contrary states of the human soul |
| 78 | Sonnets from the Portuguese | Elizabeth Barrett Browning | 2002 | [DONE] | Already built |
| 79 | Middlemarch | George Eliot | 145 | [DONE] | Already built |

### Latin American & Lusophone Literature

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 80 | Dom Casmurro | Machado de Assis | 55752 | — | In English. Unreliable narrator, jealousy, Brazilian society |
| 81 | Posthumous Memoirs of Bras Cubas | Machado de Assis | 54829 | — | In English ("Epitaph of a Small Winner"). Dead narrator, irony, modernism before modernism |
| 82 | Quincas Borba | Machado de Assis | 55753 | — | In English. Philosophy of "Humanitism" — satire of systems |
| 83 | The Alienist | Machado de Assis | — | [ALT SOURCE] | Short novel. Check archive.org |
| 84 | **Fernando Pessoa** — works | — | — | [ALT SOURCE] | Pessoa died 1935. Portuguese originals are PD in many jurisdictions. Some poems available on archive.org and poetryfoundation.org. English translations by Richard Zenith (2003+) are under copyright. Check archive.org for Portuguese originals: *Mensagem*, *Livro do Desassossego* (Book of Disquiet). Older English translations by Edwin Honig and others may be findable. |
| 85 | **Clarice Lispector** — works | — | — | [NOT PD] | Died 1977. All works under copyright. *The Passion According to G.H.*, *The Hour of the Star*, *Near to the Wild Heart*. Must be sourced from bookstores/libraries. Extraordinarily important — she's the Kafka of Latin America. |

### British Fantasy & Mythopoeia

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 86 | **C.S. Lewis** — all fiction | — | — | [NOT PD] | Died 1963. *Narnia*, *Screwtape Letters*, *Space Trilogy*, *Mere Christianity* all under copyright. Note: his academic works on medieval literature (*The Discarded Image*, *The Allegory of Love*) are also copyrighted but can be found in libraries. |
| 87 | **J.R.R. Tolkien** — all works | — | — | [NOT PD] | Died 1973. *Lord of the Rings*, *Hobbit*, *Silmarillion* all under copyright and actively enforced by the Tolkien Estate. |
| 88 | George MacDonald — The Princess and the Goblin | MacDonald | 708 | — | Lewis's and Tolkien's acknowledged precursor. Available! |
| 89 | George MacDonald — Phantastes | MacDonald | 325 | — | The fantasy novel that "baptised C.S. Lewis's imagination" |
| 90 | George MacDonald — At the Back of the North Wind | MacDonald | 493 | — | Children's fantasy, spiritual allegory |
| 91 | William Morris — The Well at the World's End | Morris | 169 | — | Proto-fantasy, Tolkien's acknowledged influence |

### The Hesse–Jung Connection

Hermann Hesse was not literally Jung's patient — he was treated by J.B. Lang, a student of Jung's, in 1916-17. But Jung's ideas profoundly shaped Hesse's later work: *Demian*, *Steppenwolf*, *Siddhartha*, *The Glass Bead Game*. Only *Siddhartha* (1922) and *Steppenwolf* (1927, English trans. 1929) are potentially PD depending on jurisdiction. *Siddhartha* IS on Gutenberg (#2500) in German.

---

## 4. CHILDREN'S POETRY, RHYMES & SONGS

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 92 | A Child's Garden of Verses | Robert Louis Stevenson | 136 | — | "My Shadow", "The Lamplighter", "The Land of Counterpane" |
| 93 | The Book of Nonsense | Edward Lear | 13650 | — | Limericks and absurdist verse |
| 94 | More Nonsense | Edward Lear | 13649 | — | "The Owl and the Pussycat" etc. |
| 95 | Mother Goose / Nursery Rhymes | Various | 19993 | — | Classic collection |
| 96 | Real Mother Goose | Blanche Fisher Wright | 10607 | — | Illustrated collection |
| 97 | Songs of Childhood | Walter de la Mare | 23064 | — | Mysterious, musical children's verse |
| 98 | When We Were Very Young | A.A. Milne | — | [NOT PD] | Published 1924, may be PD in some jurisdictions but not on Gutenberg |
| 99 | Old Nursery Rhymes | Various / Arthur Rackham | 18483 | — | Rackham-illustrated collection |
| 100 | National Nursery Rhymes and Songs | Various | 53098 | — | With musical notation |
| 101 | English Fairy Tales | Joseph Jacobs | 7439 | — | "Jack and the Beanstalk", etc. |

### Traditional Songs & Ballads

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 102 | English and Scottish Popular Ballads (Child) | Francis James Child | 27846 | — | Vol 1 of the definitive collection |
| 103 | The Book of Old English Ballads | Various | 30645 | — | Traditional songs |
| 104 | Folk-Songs of the South | John Harrington Cox | — | [ALT SOURCE] | Check archive.org |
| 105 | Songs of the People | Various | — | [ALT SOURCE] | Check archive.org for Sam Henry collection |

---

## 5. ANTHROPOLOGY & COMPARATIVE RELIGION

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 106 | The Golden Bough | J.G. Frazer | 3623 | [DONE] | Already built. Abridged edition. |
| 107 | Primitive Culture Vol 1 | E.B. Tylor | 61944 | — | Origins of religion, animism |
| 108 | Primitive Culture Vol 2 | E.B. Tylor | 61960 | — | Myth, ritual, survival |
| 109 | Ancient Society | Lewis Henry Morgan | 45950 | — | Social evolution, kinship systems |
| 110 | The Gift (Essai sur le don) | Marcel Mauss | — | [ALT SOURCE] | 1925 essay. French original PD. English translations by Ian Cunnison (1954) or Jane Guyer (2016) under copyright. French available at classiques.uqac.ca |
| 111 | Totem and Taboo | Sigmund Freud | 41214 | — | Psychoanalysis meets anthropology |
| 112 | The Future of an Illusion | Sigmund Freud | — | [ALT SOURCE] | 1927. English trans may be PD (check). Religion as illusion. |
| 113 | Civilization and Its Discontents | Freud | — | [NOT PD] | 1930 in German, English 1930. Check PD status. |
| 114 | The Elementary Forms of Religious Life | Émile Durkheim | — | [ALT SOURCE] | 1912. English trans by Swain (1915) likely PD. Check archive.org. |
| 115 | The Interpretation of Cultures | Clifford Geertz (1973) | — | [NOT PD] | Under copyright. Thick description, symbolic anthropology. |
| 116 | Myth of the Birth of the Hero | Otto Rank | 57875 | [DONE] | Already built |
| 117 | Expression of Emotions | Charles Darwin | 1227 | [DONE] | Already built |

---

## 6. ADDITIONAL PHILOSOPHICAL TEXTS (Filling Gaps)

### Existentialism & Phenomenology (toward Tillich)

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 118 | The Concept of Dread | Kierkegaard / Lowrie | — | [NOT PD] | English trans under copyright |
| 119 | Being and Time | Heidegger (1927) | — | [NOT PD] | Under copyright. Dasein, being-toward-death |
| 120 | Being and Nothingness | Sartre (1943) | — | [NOT PD] | Under copyright |
| 121 | Myth of Sisyphus | Camus (1942) | — | [NOT PD] | Under copyright |
| 122 | The Stranger | Camus (1942) | — | [NOT PD] | Under copyright |

### Process Philosophy (toward Deleuze & Akomolafe)

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 123 | Process and Reality | A.N. Whitehead (1929) | — | [NOT PD] | Under copyright. Process philosophy, actual occasions |
| 124 | Science and the Modern World | Whitehead (1925) | — | [ALT SOURCE] | May be PD. Check archive.org |
| 125 | An Introduction to Metaphysics | Bergson / Hulme | 56676 | — | Intuition vs analysis, duration |

### Political Economy

| # | Title | Author | Gutenberg ID | Status | Notes |
|---|-------|--------|-------------|--------|-------|
| 126 | Wealth of Nations | Adam Smith | 3300 | — | Classical economics, invisible hand |
| 127 | On the Principles of Political Economy | David Ricardo | 57017 | — | Labor theory of value |
| 128 | Principles of Political Economy | J.S. Mill | 30107 | — | Liberal economics |
| 129 | The Theory of the Leisure Class | Thorstein Veblen | 833 | — | Conspicuous consumption, critique of capitalism |
| 130 | Mutual Aid | Kropotkin | 4341 | [DONE] | Already built |

---

## Download Commands — Ready to Run

### Philosophy Batch 1: The Tillich Line

```bash
# Plato - Republic
curl -L -o seeds/republic-plato.txt "https://www.gutenberg.org/cache/epub/1497/pg1497.txt" && \
git add seeds/republic-plato.txt && \
git commit -m "Add Republic by Plato source text (Gutenberg #1497)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Plato - Apology/Crito/Phaedo
curl -L -o seeds/apology-crito-phaedo-plato.txt "https://www.gutenberg.org/cache/epub/1656/pg1656.txt" && \
git add seeds/apology-crito-phaedo-plato.txt && \
git commit -m "Add Apology/Crito/Phaedo by Plato source text (Gutenberg #1656)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Plato - Timaeus
curl -L -o seeds/timaeus-plato.txt "https://www.gutenberg.org/cache/epub/1572/pg1572.txt" && \
git add seeds/timaeus-plato.txt && \
git commit -m "Add Timaeus by Plato source text (Gutenberg #1572)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Kant - Critique of Practical Reason
curl -L -o seeds/critique-practical-reason.txt "https://www.gutenberg.org/cache/epub/5683/pg5683.txt" && \
git add seeds/critique-practical-reason.txt && \
git commit -m "Add Critique of Practical Reason by Kant source text (Gutenberg #5683)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Hegel - Phenomenology of Spirit
curl -L -o seeds/phenomenology-of-spirit.txt "https://www.gutenberg.org/cache/epub/39064/pg39064.txt" && \
git add seeds/phenomenology-of-spirit.txt && \
git commit -m "Add Phenomenology of Spirit by Hegel source text (Gutenberg #39064)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Hegel - Philosophy of Right
curl -L -o seeds/philosophy-of-right-hegel.txt "https://www.gutenberg.org/cache/epub/39297/pg39297.txt" && \
git add seeds/philosophy-of-right-hegel.txt && \
git commit -m "Add Philosophy of Right by Hegel source text (Gutenberg #39297)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Hegel - Philosophy of History
curl -L -o seeds/philosophy-of-history-hegel.txt "https://www.gutenberg.org/cache/epub/1900/pg1900.txt" && \
git add seeds/philosophy-of-history-hegel.txt && \
git commit -m "Add Philosophy of History by Hegel source text (Gutenberg #1900)" && \
git push origin claude/merge-iching-grammar-ND6pW
```

### Philosophy Batch 2: The Deleuze Line

```bash
# Leibniz - Monadology & other writings
curl -L -o seeds/monadology-leibniz.txt "https://www.gutenberg.org/cache/epub/39441/pg39441.txt" && \
git add seeds/monadology-leibniz.txt && \
git commit -m "Add Monadology by Leibniz source text (Gutenberg #39441)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Hume - Treatise of Human Nature
curl -L -o seeds/treatise-human-nature-hume.txt "https://www.gutenberg.org/cache/epub/4705/pg4705.txt" && \
git add seeds/treatise-human-nature-hume.txt && \
git commit -m "Add Treatise of Human Nature by Hume source text (Gutenberg #4705)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Hume - Enquiry Concerning Human Understanding
curl -L -o seeds/enquiry-human-understanding-hume.txt "https://www.gutenberg.org/cache/epub/9662/pg9662.txt" && \
git add seeds/enquiry-human-understanding-hume.txt && \
git commit -m "Add Enquiry Concerning Human Understanding by Hume source text (Gutenberg #9662)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Nietzsche - The Gay Science
curl -L -o seeds/gay-science-nietzsche.txt "https://www.gutenberg.org/cache/epub/52881/pg52881.txt" && \
git add seeds/gay-science-nietzsche.txt && \
git commit -m "Add The Gay Science by Nietzsche source text (Gutenberg #52881)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Nietzsche - Birth of Tragedy
curl -L -o seeds/birth-of-tragedy-nietzsche.txt "https://www.gutenberg.org/cache/epub/7205/pg7205.txt" && \
git add seeds/birth-of-tragedy-nietzsche.txt && \
git commit -m "Add Birth of Tragedy by Nietzsche source text (Gutenberg #7205)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Bergson - Matter and Memory
curl -L -o seeds/matter-and-memory-bergson.txt "https://www.gutenberg.org/cache/epub/57898/pg57898.txt" && \
git add seeds/matter-and-memory-bergson.txt && \
git commit -m "Add Matter and Memory by Bergson source text (Gutenberg #57898)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Bergson - Time and Free Will
curl -L -o seeds/time-and-free-will-bergson.txt "https://www.gutenberg.org/cache/epub/56674/pg56674.txt" && \
git add seeds/time-and-free-will-bergson.txt && \
git commit -m "Add Time and Free Will by Bergson source text (Gutenberg #56674)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Bergson - Introduction to Metaphysics
curl -L -o seeds/intro-metaphysics-bergson.txt "https://www.gutenberg.org/cache/epub/56676/pg56676.txt" && \
git add seeds/intro-metaphysics-bergson.txt && \
git commit -m "Add Introduction to Metaphysics by Bergson source text (Gutenberg #56676)" && \
git push origin claude/merge-iching-grammar-ND6pW
```

### Philosophy Batch 3: Shared Foundations

```bash
# Schopenhauer - World as Will and Idea Vol 1
curl -L -o seeds/world-as-will-schopenhauer.txt "https://www.gutenberg.org/cache/epub/38427/pg38427.txt" && \
git add seeds/world-as-will-schopenhauer.txt && \
git commit -m "Add World as Will and Idea by Schopenhauer source text (Gutenberg #38427)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Freud - Totem and Taboo
curl -L -o seeds/totem-and-taboo-freud.txt "https://www.gutenberg.org/cache/epub/41214/pg41214.txt" && \
git add seeds/totem-and-taboo-freud.txt && \
git commit -m "Add Totem and Taboo by Freud source text (Gutenberg #41214)" && \
git push origin claude/merge-iching-grammar-ND6pW
```

### Politics Batch

```bash
# Machiavelli - The Prince
curl -L -o seeds/the-prince-machiavelli.txt "https://www.gutenberg.org/cache/epub/1232/pg1232.txt" && \
git add seeds/the-prince-machiavelli.txt && \
git commit -m "Add The Prince by Machiavelli source text (Gutenberg #1232)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Hobbes - Leviathan
curl -L -o seeds/leviathan-hobbes.txt "https://www.gutenberg.org/cache/epub/3207/pg3207.txt" && \
git add seeds/leviathan-hobbes.txt && \
git commit -m "Add Leviathan by Hobbes source text (Gutenberg #3207)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Locke - Two Treatises of Government
curl -L -o seeds/two-treatises-locke.txt "https://www.gutenberg.org/cache/epub/7370/pg7370.txt" && \
git add seeds/two-treatises-locke.txt && \
git commit -m "Add Two Treatises of Government by Locke source text (Gutenberg #7370)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Rousseau - Social Contract
curl -L -o seeds/social-contract-rousseau.txt "https://www.gutenberg.org/cache/epub/46333/pg46333.txt" && \
git add seeds/social-contract-rousseau.txt && \
git commit -m "Add The Social Contract by Rousseau source text (Gutenberg #46333)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Rousseau - Discourse on Inequality
curl -L -o seeds/discourse-inequality-rousseau.txt "https://www.gutenberg.org/cache/epub/11136/pg11136.txt" && \
git add seeds/discourse-inequality-rousseau.txt && \
git commit -m "Add Discourse on Inequality by Rousseau source text (Gutenberg #11136)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Rousseau - Emile
curl -L -o seeds/emile-rousseau.txt "https://www.gutenberg.org/cache/epub/5427/pg5427.txt" && \
git add seeds/emile-rousseau.txt && \
git commit -m "Add Emile by Rousseau source text (Gutenberg #5427)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Rousseau - Confessions
curl -L -o seeds/confessions-rousseau.txt "https://www.gutenberg.org/cache/epub/3913/pg3913.txt" && \
git add seeds/confessions-rousseau.txt && \
git commit -m "Add Confessions by Rousseau source text (Gutenberg #3913)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Montesquieu - Spirit of Laws
curl -L -o seeds/spirit-of-laws-montesquieu.txt "https://www.gutenberg.org/cache/epub/27573/pg27573.txt" && \
git add seeds/spirit-of-laws-montesquieu.txt && \
git commit -m "Add Spirit of Laws by Montesquieu source text (Gutenberg #27573)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Mill - Utilitarianism
curl -L -o seeds/utilitarianism-mill.txt "https://www.gutenberg.org/cache/epub/11224/pg11224.txt" && \
git add seeds/utilitarianism-mill.txt && \
git commit -m "Add Utilitarianism by Mill source text (Gutenberg #11224)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Aristotle - Politics
curl -L -o seeds/politics-aristotle.txt "https://www.gutenberg.org/cache/epub/6762/pg6762.txt" && \
git add seeds/politics-aristotle.txt && \
git commit -m "Add Politics by Aristotle source text (Gutenberg #6762)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Marx - Capital Vol 1
curl -L -o seeds/capital-marx.txt "https://www.gutenberg.org/cache/epub/46423/pg46423.txt" && \
git add seeds/capital-marx.txt && \
git commit -m "Add Capital Vol 1 by Marx source text (Gutenberg #46423)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Adam Smith - Wealth of Nations
curl -L -o seeds/wealth-of-nations-smith.txt "https://www.gutenberg.org/cache/epub/3300/pg3300.txt" && \
git add seeds/wealth-of-nations-smith.txt && \
git commit -m "Add Wealth of Nations by Adam Smith source text (Gutenberg #3300)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Veblen - Theory of the Leisure Class
curl -L -o seeds/leisure-class-veblen.txt "https://www.gutenberg.org/cache/epub/833/pg833.txt" && \
git add seeds/leisure-class-veblen.txt && \
git commit -m "Add Theory of the Leisure Class by Veblen source text (Gutenberg #833)" && \
git push origin claude/merge-iching-grammar-ND6pW
```

### Literature Batch

```bash
# Emerson - Essays Second Series
curl -L -o seeds/essays-second-series-emerson.txt "https://www.gutenberg.org/cache/epub/2945/pg2945.txt" && \
git add seeds/essays-second-series-emerson.txt && \
git commit -m "Add Essays Second Series by Emerson source text (Gutenberg #2945)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Emerson - Nature
curl -L -o seeds/nature-emerson.txt "https://www.gutenberg.org/cache/epub/29433/pg29433.txt" && \
git add seeds/nature-emerson.txt && \
git commit -m "Add Nature by Emerson source text (Gutenberg #29433)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Hesse - Siddhartha
curl -L -o seeds/siddhartha-hesse.txt "https://www.gutenberg.org/cache/epub/2500/pg2500.txt" && \
git add seeds/siddhartha-hesse.txt && \
git commit -m "Add Siddhartha by Hesse source text (Gutenberg #2500)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Goethe - Faust
curl -L -o seeds/faust-goethe.txt "https://www.gutenberg.org/cache/epub/14591/pg14591.txt" && \
git add seeds/faust-goethe.txt && \
git commit -m "Add Faust by Goethe source text (Gutenberg #14591)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Dostoevsky - Brothers Karamazov
curl -L -o seeds/brothers-karamazov.txt "https://www.gutenberg.org/cache/epub/28054/pg28054.txt" && \
git add seeds/brothers-karamazov.txt && \
git commit -m "Add Brothers Karamazov by Dostoevsky source text (Gutenberg #28054)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Dostoevsky - Notes from Underground
curl -L -o seeds/notes-from-underground.txt "https://www.gutenberg.org/cache/epub/600/pg600.txt" && \
git add seeds/notes-from-underground.txt && \
git commit -m "Add Notes from Underground by Dostoevsky source text (Gutenberg #600)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Dostoevsky - Crime and Punishment
curl -L -o seeds/crime-and-punishment.txt "https://www.gutenberg.org/cache/epub/2554/pg2554.txt" && \
git add seeds/crime-and-punishment.txt && \
git commit -m "Add Crime and Punishment by Dostoevsky source text (Gutenberg #2554)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Blake - Songs of Innocence and Experience
curl -L -o seeds/songs-innocence-experience-blake.txt "https://www.gutenberg.org/cache/epub/1934/pg1934.txt" && \
git add seeds/songs-innocence-experience-blake.txt && \
git commit -m "Add Songs of Innocence and Experience by Blake source text (Gutenberg #1934)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Machado de Assis - Dom Casmurro
curl -L -o seeds/dom-casmurro-machado.txt "https://www.gutenberg.org/cache/epub/55752/pg55752.txt" && \
git add seeds/dom-casmurro-machado.txt && \
git commit -m "Add Dom Casmurro by Machado de Assis source text (Gutenberg #55752)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Machado de Assis - Posthumous Memoirs of Bras Cubas
curl -L -o seeds/bras-cubas-machado.txt "https://www.gutenberg.org/cache/epub/54829/pg54829.txt" && \
git add seeds/bras-cubas-machado.txt && \
git commit -m "Add Posthumous Memoirs of Bras Cubas by Machado de Assis source text (Gutenberg #54829)" && \
git push origin claude/merge-iching-grammar-ND6pW

# George MacDonald - Princess and the Goblin
curl -L -o seeds/princess-goblin-macdonald.txt "https://www.gutenberg.org/cache/epub/708/pg708.txt" && \
git add seeds/princess-goblin-macdonald.txt && \
git commit -m "Add The Princess and the Goblin by MacDonald source text (Gutenberg #708)" && \
git push origin claude/merge-iching-grammar-ND6pW

# George MacDonald - Phantastes
curl -L -o seeds/phantastes-macdonald.txt "https://www.gutenberg.org/cache/epub/325/pg325.txt" && \
git add seeds/phantastes-macdonald.txt && \
git commit -m "Add Phantastes by MacDonald source text (Gutenberg #325)" && \
git push origin claude/merge-iching-grammar-ND6pW
```

### Children's Poetry & Songs Batch

```bash
# Stevenson - A Child's Garden of Verses
curl -L -o seeds/childs-garden-verses.txt "https://www.gutenberg.org/cache/epub/136/pg136.txt" && \
git add seeds/childs-garden-verses.txt && \
git commit -m "Add A Child's Garden of Verses by Stevenson source text (Gutenberg #136)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Lear - Book of Nonsense
curl -L -o seeds/book-of-nonsense-lear.txt "https://www.gutenberg.org/cache/epub/13650/pg13650.txt" && \
git add seeds/book-of-nonsense-lear.txt && \
git commit -m "Add Book of Nonsense by Lear source text (Gutenberg #13650)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Mother Goose nursery rhymes
curl -L -o seeds/mother-goose.txt "https://www.gutenberg.org/cache/epub/19993/pg19993.txt" && \
git add seeds/mother-goose.txt && \
git commit -m "Add Mother Goose nursery rhymes source text (Gutenberg #19993)" && \
git push origin claude/merge-iching-grammar-ND6pW

# De la Mare - Songs of Childhood
curl -L -o seeds/songs-of-childhood.txt "https://www.gutenberg.org/cache/epub/23064/pg23064.txt" && \
git add seeds/songs-of-childhood.txt && \
git commit -m "Add Songs of Childhood by de la Mare source text (Gutenberg #23064)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Dickinson - Poems Series 1
curl -L -o seeds/poems-dickinson-1.txt "https://www.gutenberg.org/cache/epub/12242/pg12242.txt" && \
git add seeds/poems-dickinson-1.txt && \
git commit -m "Add Poems Series 1 by Emily Dickinson source text (Gutenberg #12242)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Child Ballads Vol 1
curl -L -o seeds/child-ballads-1.txt "https://www.gutenberg.org/cache/epub/27846/pg27846.txt" && \
git add seeds/child-ballads-1.txt && \
git commit -m "Add English and Scottish Popular Ballads Vol 1 source text (Gutenberg #27846)" && \
git push origin claude/merge-iching-grammar-ND6pW
```

### Anthropology Batch

```bash
# Tylor - Primitive Culture Vol 1
curl -L -o seeds/primitive-culture-tylor-1.txt "https://www.gutenberg.org/cache/epub/61944/pg61944.txt" && \
git add seeds/primitive-culture-tylor-1.txt && \
git commit -m "Add Primitive Culture Vol 1 by Tylor source text (Gutenberg #61944)" && \
git push origin claude/merge-iching-grammar-ND6pW

# Morgan - Ancient Society
curl -L -o seeds/ancient-society-morgan.txt "https://www.gutenberg.org/cache/epub/45950/pg45950.txt" && \
git add seeds/ancient-society-morgan.txt && \
git commit -m "Add Ancient Society by Morgan source text (Gutenberg #45950)" && \
git push origin claude/merge-iching-grammar-ND6pW
```

---

## Summary: What You Need to Source Elsewhere

### Under Copyright (must buy or borrow)

| Author | Key Works | Why It Matters |
|--------|-----------|----------------|
| **Paul Tillich** | *The Courage to Be*, *Systematic Theology*, *Dynamics of Faith* | Endpoint of the existential theology line |
| **Gilles Deleuze** | *Difference and Repetition*, *Anti-Oedipus*, *A Thousand Plateaus* | Endpoint of the immanence/difference line |
| **John Rawls** | *A Theory of Justice* | Justice as fairness, the veil of ignorance |
| **Léon Walras** | *Elements of Pure Economics* (English trans) | General equilibrium theory |
| **Hannah Arendt** | *The Human Condition*, *Origins of Totalitarianism* | Labor/work/action, banality of evil |
| **Frantz Fanon** | *The Wretched of the Earth*, *Black Skin White Masks* | Decolonial psychology |
| **Clarice Lispector** | *The Passion According to G.H.*, *Hour of the Star* | Brazilian existentialism, language at the edge |
| **C.S. Lewis** | *Narnia*, *Screwtape Letters*, *Mere Christianity* | Christian mythopoeia |
| **J.R.R. Tolkien** | *Lord of the Rings*, *Silmarillion* | Sub-creation, myth as truth |
| **Kierkegaard** | *Either/Or*, *Fear and Trembling*, *Sickness Unto Death* | English translations under copyright |

### PD but Needs Alternative Sources

| Author | Work | Where to Look |
|--------|------|---------------|
| **Fernando Pessoa** | *Mensagem*, *Book of Disquiet* (Portuguese) | archive.org, Biblioteca Nacional Digital |
| **Marcel Mauss** | *The Gift* (French original) | classiques.uqac.ca |
| **Durkheim** | *Elementary Forms of Religious Life* | archive.org (Swain 1915 translation) |

---

## Suggested Build Priority

### Phase 1: Social Contract & Political Philosophy (highest impact, most requested)
1. Hobbes — Leviathan
2. Rousseau — Social Contract
3. Rousseau — Discourse on Inequality
4. Locke — Two Treatises
5. Machiavelli — The Prince
6. Aristotle — Politics
7. Montesquieu — Spirit of Laws

### Phase 2: German Philosophy (Tillich line)
8. Hegel — Phenomenology of Spirit
9. Hegel — Philosophy of History
10. Kant — Critique of Practical Reason
11. Schopenhauer — World as Will and Idea
12. Nietzsche — Birth of Tragedy
13. Nietzsche — Gay Science

### Phase 3: Deleuze Line
14. Leibniz — Monadology
15. Hume — Treatise / Enquiry
16. Bergson — Matter and Memory
17. Bergson — Time and Free Will

### Phase 4: Literature
18. Hesse — Siddhartha
19. Dostoevsky — Brothers Karamazov
20. Machado de Assis — Bras Cubas / Dom Casmurro
21. Blake — Songs of Innocence and Experience
22. Goethe — Faust
23. MacDonald — Phantastes / Princess and the Goblin

### Phase 5: Children's & Songs
24. Stevenson — Child's Garden of Verses
25. Mother Goose / Nursery Rhymes
26. Lear — Book of Nonsense
27. Dickinson — Poems
28. Child Ballads

### Phase 6: Anthropology
29. Tylor — Primitive Culture
30. Morgan — Ancient Society
31. Freud — Totem and Taboo
32. Durkheim — Elementary Forms (if sourced)

---

## The Intellectual Map

```
                    TILLICH
                      ↑
              Kierkegaard [NOT PD]
              ↑           ↑
          Hegel ──── Schopenhauer
            ↑              ↑
           Kant ──────────┘
            ↑
    Plato ──┤
            ↓
        Aristotle → Locke → Mill → Rawls [NOT PD]
                      ↓
    Machiavelli → Hobbes → Rousseau → Marx
                                        ↓
    Montesquieu → Smith → Ricardo → Walras [NOT PD] → Veblen

                    DELEUZE
                      ↑
              Bergson ─┤
              ↑        ↑
    Spinoza ──┤   Nietzsche
              ↑        ↑
    Leibniz ──┤   Schopenhauer
              ↑        ↑
         Hume ─────── Kant

    LITERATURE CONSTELLATION:
    MacDonald → Lewis [NOT PD] / Tolkien [NOT PD]
    Goethe → Dostoevsky → Hesse (← Jung)
    Machado de Assis → Lispector [NOT PD]
    Emerson → Whitman → Dickinson
    Blake → Yeats → de la Mare
    Pessoa [ALT SOURCE]
```
