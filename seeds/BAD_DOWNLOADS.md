# Bad Downloads — Incorrect Gutenberg IDs

These seed files contain the wrong text due to Gutenberg ID reassignments:

| File | Expected | Got | Gutenberg # | Correct # |
|------|----------|-----|-------------|-----------|
| `chuang-tzu.txt` | Musings of a Chinese Mystic (Zhuangzi/Giles) | The Waste Land (T.S. Eliot) | #1321 | #59709 (full Giles translation: "Chuang Tzu: Mystic, Moralist, and Social Reformer") |
| `life-of-the-bee.txt` | The Life of the Bee (Maeterlinck) | Brochure Series of Architectural Illustration | #18852 | Needs research |
| `buddhist-suttas.txt` | Buddhist Suttas (T.W. Rhys Davids) | The Book of Mormon (Joseph Smith) | #17 | Not on Gutenberg as standalone; available on Internet Archive |
| `sayings-of-lao-tzu.txt` | The Sayings of Lao Tzu (Lionel Giles) | The Guardian Angel (Oliver Wendell Holmes) | #2697 | Not found on Gutenberg; available on Internet Archive and sacred-texts.com |

| `cloud-of-unknowing.txt` | The Cloud of Unknowing (medieval mysticism) | Como eu atravessei África (Portuguese travel book) | #20508 | Needs research; may not be on Gutenberg |
| `dark-night-of-the-soul.txt` | Dark Night of the Soul (St. John of the Cross) | Terre-Neuve et les Terre-Neuviennes (French text) | ? | Needs research |
| `phenomenology-of-spirit.txt` | Phenomenology of Spirit (Hegel) | Numa Roumestan (Alphonse Daudet) | ? | NOT on Gutenberg at all; check archive.org |
| `interior-castle.txt` | The Interior Castle (St. Teresa of Ávila) | La Comédie humaine Vol. 03 (Balzac) | ? | Needs research |

## To Fix

Re-download with correct Gutenberg IDs or from Internet Archive:

### Chuang Tzu (has correct Gutenberg alternative)
```bash
curl -L -o seeds/chuang-tzu.txt "https://www.gutenberg.org/cache/epub/59709/pg59709.txt" && \
git add seeds/chuang-tzu.txt && \
git commit -m "Re-download Chuang Tzu with correct Gutenberg #59709 (full Giles translation)" && \
git push origin <branch>
```

### Other texts needing research
- "The Life of the Bee" by Maurice Maeterlinck — search gutenberg.org
- "Buddhist Suttas" by T.W. Rhys Davids (Sacred Books of the East Vol. 11) — may need Internet Archive source
- "The Sayings of Lao Tzu" by Lionel Giles — may need Internet Archive source
