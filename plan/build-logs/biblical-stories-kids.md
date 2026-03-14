# Build Log: Stories from the Living Stars (biblical-stories-kids)

**Date:** 2026-03-12
**Grammar slug:** `biblical-stories-kids`
**Builder:** Claude (Opus 4.6) with PlayfulProcess direction
**Status:** Grammar complete, illustrations pending

---

## What Was Built

- **84 items**: 48 L1 stories + 29 L2 clusters + 7 L3 meta-arcs
- **Format**: Rhyming verse (AABB/ABAB), ALL CAPS keywords for karaoke TTS
- **Sections**: Story / Wonder / Whisper (L1), About / For Parents / The Thread (L2), About / The Pattern / Star Wars (L3)
- **Lens**: Esoteric/animist/cosmic — Jesus as shaman for the Cosmic Christ, angels as star-beings, nature as conscious participant
- **Sources**: From memory, cross-referenced against WEB Bible (Gutenberg #8294)

## Seven Arcs

| Arc | L1 | L2 | Theme |
|-----|----|----|-------|
| Tricksters & Unlikely Heroes | 6 | 3 | Cleverness, outsiders, sideways salvation |
| The Living World | 7 | 5 | Animism — fire speaks, water chooses, earth responds |
| Warriors & Giants | 6 | 3 | Creative tactics, underdog victories |
| Dreamers & Seers | 7 | 4 | Shamanic perception, dreams, silence |
| Star Messengers | 7 | 5 | Angels as cosmic intelligences, portals |
| Kings, Queens & Hidden Princesses | 7 | 4 | Power, identity, hidden royalty |
| The Shaman from Nazareth | 8 | 5 | The complete arc — birth to ascension |

## Writing Approach

- Written from memory, no source text parsing required
- Each L1 story: 3 stanzas (~12-16 lines) of rhyming verse
- ALL CAPS on key words for karaoke-style TTS highlighting
- Campbell monomyth parallel mapped for every story
- Pop culture parallel (mostly Star Wars/LOTR) for instant kid recognition
- Esoteric "Whisper" section for parents/older kids (Steiner, Theosophy, animist theology)

## Learnings

1. **Rhyming verse at scale**: 48 stories in AABB/ABAB is a LOT of rhyming. Quality stays high when each story has a clear emotional arc (setup → complication → punchline/revelation). The best stories have a funny/unexpected last couplet.

2. **ALL CAPS as emphasis**: Works well for TTS karaoke — highlights the words a reader would naturally stress. Rule: 1-3 caps words per stanza, on the words that carry meaning or surprise.

3. **Esoteric lens for kids**: The Steiner/Theosophy material (Solar Logos, Sirius, spiritual hierarchies) lives in the "Whisper" section only — never in the main Story. Kids get the cosmic wonder; parents/older readers get the deeper layer. Works well as a two-track grammar.

4. **Campbell parallels work beautifully**: Every biblical story maps to the monomyth. The L3 "Star Wars" sections make this tangible for kids. Ezekiel's wheels = Close Encounters. Jacob's ladder = the wardrobe to Narnia. The mapping is natural, not forced.

5. **L2 clusters should tell parents HOW to use the stories**: "For Parents" section is the most practical part of the grammar. It answers: "When do I read this to my kid? What conversation does it start?"

## Next Steps

1. **Illustrations**: User to curate Doré images from Wikimedia Commons (~35 images mapped by filename in the plan). Save to `z.ignore/manuscript-images/biblical-stories-kids/` with triple-underscore naming.
2. **R2 Upload**: Write upload script once images are local. Add `image_url` + `metadata.illustrations[]` to all 84 items.
3. **Coverage target**: 100% — every item gets an illustration. L1 = Doré scene matches. L2 = Schnorr/Tissot alternatives. L3 = Blake visionary art.
4. **TTS integration**: Test karaoke rendering with ElevenLabs once the viewer supports the ALL CAPS highlight pattern.

## Companion Grammars (Same Series)

- **Sword and Grail: King Arthur** — next in pipeline
- **The Wine-Dark Sea: Homer** — Iliad + Odyssey combined
- **Rama's Bow: Ramayana** — Vishnu incarnates as Rama
- **The One Story: Four Faces of the Hero** — meta-grammar mapping archetypes across all four
