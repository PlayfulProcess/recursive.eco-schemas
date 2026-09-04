# Walt Whitman Grammar — Plan

## Summary

A grammar (recursive.eco deck) built around Walt Whitman's poetry and key biographical moments. Entirely public domain — no copyright risk. Target: a reading / reflection / journaling deck where practitioners draw a poem or a biographical beat and sit with it.

## Why it's safe

Walt Whitman died in 1892. All his published work (every edition of *Leaves of Grass* 1855–1891/92, all prose, all letters, all posthumous material) is in the public domain in the US and globally. No permission needed. Full poems can be reproduced.

## Source

**Canonical text**: *Leaves of Grass*, "Deathbed edition" (1891–92) — the final edition Whitman authorized. He ordered, sequenced, and clustered the poems himself for this edition.

**Digital sources (free, scholarly)**:
- Walt Whitman Archive — https://whitmanarchive.org (U of Nebraska / U of Iowa)
- Project Gutenberg — *Leaves of Grass* and his major prose

**Earlier editions worth cross-referencing**: the radically different 1855 first edition (slim, 12 untitled poems including the first *Song of Myself*), and the 1860, 1867, 1881 editions which show how the book grew and was re-clustered over his life.

## Proposed structure

The Deathbed edition has a canonical cluster structure Whitman himself designed. The grammar mirrors the clusters as top-level categories, then branches into individual poems or biographical moments.

### L1 clusters (following the 1891-92 edition)

1. **Inscriptions** — short opening poems, including *One's-Self I Sing*, *I Hear America Singing*
2. **Starting from Paumanok** — programmatic opening
3. **Song of Myself** — the long central poem (often broken into 52 sections, each one card-worthy)
4. **Children of Adam** — the heterosexual / generative poems (controversial in its day)
5. **Calamus** — the homoerotic / male-companionship poems
6. **Birds of Passage** — travel / movement
7. **A Broadway Pageant** — ceremonial
8. **Sea-Drift** — ocean meditations, including *Out of the Cradle Endlessly Rocking*
9. **By the Roadside** — short observational poems
10. **Drum-Taps** — Civil War poems
11. **Memories of President Lincoln** — including *When Lilacs Last in the Dooryard Bloom'd*, *O Captain! My Captain!*
12. **Autumn Rivulets** — mature reflections
13. **Whispers of Heavenly Death** — elegiac late poems
14. **From Noon to Starry Night** — late observational
15. **Songs of Parting** — valedictory cluster

### L1 biographical anchors (separate category)

Short card-size biographical moments Whitman himself described in *Specimen Days* or that are well-documented in scholarship (all PD). Proposed: 8–12 cards.

- *Brooklyn printer, 1830s* — he set type for his own first book
- *The 1855 self-review scandal* — he anonymously wrote three glowing reviews of his own first edition
- *The Civil War nurse, 1862–1865* — he left Washington to care for his brother George, wounded at Fredericksburg; stayed three years as a volunteer hospital attendant, which transformed his life and produced *Drum-Taps*
- *The Emerson letter* — Ralph Waldo Emerson's extraordinary private letter after receiving a copy of the 1855 edition: "I greet you at the beginning of a great career."
- *Lincoln's assassination, April 1865* — catalyst for *When Lilacs Last in the Dooryard Bloom'd*, *O Captain! My Captain!*, and a lifetime of Lincoln reflection
- *The stroke, 1873* — a paralytic stroke at age 54; Camden, New Jersey became his home for the last 19 years
- *The Good Gray Poet campaign* — William Douglas O'Connor's 1866 pamphlet defending Whitman after he was fired from a government job for the "indecency" of his poems
- *The international influence* — Anne Gilchrist, William Rossetti, the Symbolists, the Italian Futurists; Pessoa writing heteronyms partly in response
- *Death, March 26 1892* — the deathbed edition just completed, his last quiet months in Camden

## Deck / grammar mode

Two possible reading modes in the same deck:

1. **Random-draw contemplative**: the practitioner draws one poem or moment; sits with it; journals. The classic recursive.eco tarot-like pattern.

2. **Sequential reading companion**: a reader working their way through *Leaves of Grass* uses the deck as a guided progression, with biographical anchors surfacing at appropriate cluster-transitions.

## Item structure (JSON schema, per card)

```json
{
  "id": "whitman-song-of-myself-s1",
  "title": "Song of Myself § 1",
  "cluster": "Song of Myself",
  "year": 1892,
  "full_text": "...",
  "about": "...",
  "bio_context": "...",
  "themes": ["self", "democracy", "embodiment"],
  "illustration_url": null,
  "audio_url": null
}
```

## Illustration / audio roadmap (phase 2)

- **Illustrations**: Thomas Eakins's Whitman portraits (1887–1889, PD); the Brady studio Whitman photographs (1860s, PD); Whitman's own signatures and manuscript pages from the archive (PD).
- **Audio**: public-domain LibriVox recordings of *Leaves of Grass* exist in multiple readings. Can embed directly or link. Gemini/ElevenLabs TTS available as backup.

## Workload estimate

- **Phase 1 (text-only grammar)**: ~1 session. Pull Gutenberg/Whitman Archive canonical text, script a grammar-generator that pulls cluster structure into JSON, write `about` + `themes` for each poem (or use AI assist pass). Output: working grammar.
- **Phase 2 (illustrations)**: ~1 session. Archive images, caption, upload to R2.
- **Phase 3 (audio)**: ~1 session. LibriVox embeds or TTS generation.

## Naming

`whitman-leaves-of-grass` or simply `walt-whitman`. Slug: `walt-whitman`. Title: *Walt Whitman: A Leaves of Grass Grammar*.
