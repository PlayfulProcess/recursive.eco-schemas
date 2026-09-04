# Brazilian Expressions Tarot — Plan

## Summary

A tarot-style deck of Brazilian Portuguese expressions, idioms, and cultural sayings. Designed to be playable by the author with her daughter, supporting early reading in Portuguese and cultural grounding. Each card: an expression, literal word-by-word, cultural meaning, a short scene, and a linked song or cultural anchor.

## Why a tarot deck and not a reference grammar

- The tarot format invites *drawing* rather than *looking up* — a child pulls a card and encounters an expression she has not chosen, which is closer to how expressions actually enter a native speaker's repertoire
- The random-draw creates delight rather than drill — the author's daughter is at the age where cultural transmission works through play, not study
- Each draw becomes a mini-conversation between mother and daughter, with the card as the scaffold
- The deck can scale from daughter-at-six (simple cards only, mother reads) to daughter-at-twelve (all cards, she reads, discusses)

## Copyright constraints and how we handle them

- **Expressions themselves**: public domain. Cannot be copyrighted. Fully reproducible.
- **Song lyrics**: contemporary lyrics are in copyright. **We do not reproduce full lyrics.** The card links to the song (YouTube / Spotify URL) and includes a short prose description of what the song does with the expression.
- **Pre-1929 songs**: in public domain in the US. A portion of classic samba, choro, and Carnaval marchinhas from the 1920s are fully usable. These will be noted.
- **15-word fair-use quote**: where a short lyric fragment directly illustrates the expression, we can include up to ~15 words of the lyric with full attribution (title, artist, year, link). This is the CLAUDE.md rule.
- **YouTube / Spotify linking**: card has `song_url` field; the player (or the reader) loads the song externally. No lyric text embedded except fair-use fragment. This is how we make the metadata-driven approach work safely.

## Proposed structure

### 30-40 core cards across ~6 clusters

1. **Saudade cluster** — the untranslatable emotional vocabulary (*saudade*, *ter saudade*, *matar a saudade*)
2. **Jeitinho cluster** — the Brazilian relational ethic (*dar um jeitinho*, *quebrar um galho*, *desenrola*, *se virar*)
3. **Refusal cluster** — playful dismissals (*nem vem que não tem*, *sai dessa*, *tá de brincadeira*, *ai, sim?*)
4. **Amazement cluster** — interjections (*nossa!*, *eita!*, *vixe!*, *caramba*, *minha nossa*)
5. **Affection cluster** — warm forms of address (*meu bem*, *querida*, *amor*, *cara*, *véi*)
6. **Body-in-language cluster** — embodied sayings (*cair a ficha*, *pisar na bola*, *encher o saco*, *dar com os burros n'água*, *bater as botas*)

### Each card (JSON schema)

```json
{
  "id": "br-expr-saudade",
  "expression": "Saudade",
  "literal_translation": "(untranslatable — roughly: longing, wistfulness, absence-as-presence)",
  "cultural_meaning": "The feeling of missing someone or something that is absent, held as part of how one loves...",
  "scene": "A child's grandmother has gone back to her hometown after visiting. Dinner is quiet. 'Mãe,' the child says, 'estou com saudade da vovó.' The mother does not try to console. She says, 'eu também, meu amor.' Saudade is not sadness to be fixed. Saudade is the texture of love noticing an absence.",
  "song_anchor": {
    "title": "Chega de Saudade",
    "artist": "Antônio Carlos Jobim & Vinícius de Moraes",
    "year": 1958,
    "url": "...",
    "note": "The song that birthed bossa nova. The title is the paradox: 'Enough of saudade' — which is itself an expression of saudade for someone whose return is being longed for."
  },
  "reading_difficulty": 1,
  "for_age": "4-8"
}
```

### Reading-difficulty scale (for daughter play)

- `1` — single word, phonetic (saudade, nossa)
- `2` — two-word phrase (dar jeitinho, meu bem)
- `3` — short sentence (nem vem que não tem, cair a ficha)
- `4` — idiom with embedded metaphor (dar com os burros n'água)

Start with level 1–2 cards, expand as she grows.

## Play modes

1. **Morning draw** — one card per day, mother reads first, daughter reads second, they discuss
2. **Song-first draw** — play the linked song; daughter identifies the expression in context
3. **Scene improvisation** — daughter draws a card and invents her own scene with the expression; mother responds
4. **Writing prompt** — daughter draws two cards and builds a short story using both (later, when she writes)

## Phase 1 deliverable

An initial JSON grammar with ~30 cards across the 6 clusters, each with all fields populated (expression, literal, meaning, scene, song anchor). No illustrations or audio yet. Author reviews Portuguese nuance before publishing.

## Phase 2

- **Illustrations**: original art (or public-domain Brazilian folk imagery — Candido Portinari pre-1928 works? Some of his earliest work; most is still in copyright though. Alternative: commissioned simple illustrations, or AI-generated.)
- **Audio**: mother records herself saying each expression (important for her daughter to have *her mother's* voice carrying the expression, not a TTS voice). Optional Portuguese-speaker TTS backup.

## Naming

`brazilian-expressions` or `baralho-de-expressoes` (Portuguese name honors the Brazilian audience). Title: *Baralho de Expressões Brasileiras* or *Brazilian Expressions: A Mother-Daughter Deck*. Slug: `brazilian-expressions`.

## Notes on gringo-mistranslation risk

I (Claude) will certainly get Brazilian nuance wrong at the edges. The first draft should be reviewed by the author (native Brazilian Portuguese speaker, carioca/paulistana register, raised in Brazilian Catholic/Umbanda-adjacent cultural context). Draft → author review → revision is the workflow. I will flag specific uncertainties inline in the JSON with a `confidence: low` field where relevant.
