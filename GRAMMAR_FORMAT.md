# Grammar JSON — Canonical Format

The complete, authoritative shape for a recursive.eco grammar JSON file.

This document is the contract between the schemas repo and the
recursive.eco application. **If your grammar won't load in the viewer
or the editor, this is the first place to look.**

The other docs (`CLAUDE.md`, `CONTRIBUTING.md`, `QUICKSTART.md`,
`schemas/SCHEMAS_GUIDE.md`) all describe pieces of this format. This
doc is the single source of truth.

---

## Top-level shape

A grammar is a single JSON object:

```jsonc
{
  "name": "string",                    // REQUIRED — display title
  "description": "string",             // REQUIRED — what this grammar contains
  "grammar_type": "string",            // REQUIRED — see "Grammar types" below
  "cover_image_url": "string",         // OPTIONAL — hero image for the deck
  "tags": ["string"],                  // OPTIONAL — search/filter tags
  "creator_name": "string",            // OPTIONAL — your name or handle
  "creator_link": "string",            // OPTIONAL — your website or profile
  "is_published": false,               // OPTIONAL — false for drafts
  "items": [ /* UnifiedItem objects */ ]   // REQUIRED — see "UnifiedItem" below

  // Optional library-placement fields (see CLAUDE.md "Monad Fields"):
  // "roots": [...], "shelves": [...], "lineages": [...], "worldview": "...",

  // Optional commons metadata:
  // "_grammar_commons": { "schema_version": "1.0", "license": "...", "attribution": [...] }

  // Optional astrology customization (see "Category & section roles" below):
  // "_category_roles": { "my-category-name": "planet" },
  // "_section_roles": { "My Section Name": "affirmation" }
}
```

**There is NO top-level `emergences` array.** Level-1 base items AND
level-2+ composite items ALL live inside `items[]`. Composite items
are distinguished by the presence of `composite_of: ["id1", "id2", ...]`
on the item itself. (Continued in "Composite items" below.)

---

## Grammar types

`grammar_type` must be one of:

| Type | What it's for |
|---|---|
| `"tarot"` | Card-draw oracle decks (Major Arcana, archetype decks). Items have Interpretation, Reversed, etc. |
| `"iching"` | I Ching hexagrams. Items have line data via the `lines` property. Must have 64 items. |
| `"astrology"` | Western or Vedic astrology. Items have planet / sign / house categories. |
| `"sequence"` | Curated playlists / story sequences / video collections. Often paired with `performance` blocks (see below). |
| `"course"` | Step-by-step learning sequences with lessons. |
| `"prompt"` | Prompt libraries for AI conversations. |
| `"birthchart"` | Astrological birth-chart grammars. |
| `"altar"` | Altar / shrine grammars — symbolic arrangements. |
| `"music"` | Music grammars — albums, songs, sequences. |
| `"custom"` | Anything else — chapter books, folk tales, poetry, journaling decks. Use when no other type fits. |

> ⚠️ **`"performance"` is NOT a valid `grammar_type`.** "Performance" is
> a viewer mode (timestamped video clip rendering). The grammar_type
> for a curated video playlist is `"sequence"` (or `"custom"`); the
> per-item `performance` object below carries the clip details.

If your `grammar_type` doesn't match what the items actually contain,
Flow / the viewer may render the grammar incorrectly. When in doubt,
use `"custom"`.

---

## UnifiedItem shape

Every entry in `items[]` follows this shape:

```jsonc
{
  "id": "stable-string-id",          // REQUIRED — unique within the grammar
  "name": "string",                  // REQUIRED — display name
  "category": "string",              // OPTIONAL — grouping key (e.g. "major_arcana")
  "sort_order": 0,                   // OPTIONAL — display order (default by array position)
  "image_url": "string",             // OPTIONAL — per-item image (R2 URL or any HTTPS)
  "sections": {                      // REQUIRED — at least {} (can be empty)
    "Section Label": "markdown content",
    "Another Section": "more content"
  },
  "keywords": ["string"],            // OPTIONAL — search tags for this item
  "composite_of": ["id-1", "id-2"],  // PRESENT ONLY ON COMPOSITE ITEMS — see below
  "metadata": { /* free-form */ },   // OPTIONAL — see "Metadata fields"
  "performance": { /* clip cfg */ }  // OPTIONAL — see "Performance object"
}
```

### Sections are flexible

Section keys are not restricted. Use whatever makes sense for your
content. Examples seen in production grammars:

- Tarot: `Interpretation`, `Reversed`, `Summary`
- I Ching: `Image`, `Judgment`, `Line 1`, `Line 2`, ...
- Bus Passengers: `Thoughts`, `Thinking`, `Perception`, `Sensing`, `Context`, `Mystery`
- Story grammar: `Story`, `For Young Readers`, `For Parents`, `Themes`
- Tantric tattvas: `Mirror`, `Yantra`, `Essence`, `Practice`, `Question`, `Unmesa/Nimesa`
- Sequence / performance: `What she says`, `Why this clip`, `Test for listener`

The viewer renders all sections. Order is the JSON property order.

### Composite items (the L2/L3 emergence pattern)

A composite item is just a regular item that has a `composite_of`
array referencing the IDs of its children:

```json
{
  "id": "act-1-the-departure",
  "name": "Act 1: The Departure",
  "category": "act",
  "composite_of": ["scene-1", "scene-2", "scene-3"],
  "sections": {
    "About this act": "The hero leaves the ordinary world..."
  }
}
```

- L1 items are the leaves (cards, scenes, hexagrams, video clips).
- L2 items group L1 items via `composite_of`.
- L3 items can group L2 items.

**All of these live in the same `items[]` array.** Do not put
composite items in a separate `emergences[]` block. (Legacy grammars
that used a separate array no longer work; the editor saves
everything in `items[]`.)

The `level` field (`"level": 1`, `"level": 2`, `"level": 3`) is
*allowed* and helpful for tools that walk the hierarchy, but the
real source of truth is the presence/absence of `composite_of`. An
item without `composite_of` is L1; an item with `composite_of` is L2
or deeper.

`composite_of` references must point to IDs that exist in the same
`items[]` array. Broken references will fail validation.

---

## Metadata fields

`metadata` is a free-form object for whatever extra structured data
your grammar needs. Some conventions:

| Field | Meaning | Used by |
|---|---|---|
| `youtube_video_id` | The 11-character YouTube ID (e.g. `dQw4w9WgXcQ`) | Sequence grammars with video clips |
| `youtube_url` | Full URL to the source video | Sequence grammars (for click-through) |
| `lines` | Array of line texts (for I Ching items) | I Ching grammars |
| `planet`, `sign`, `house` | Astrology categorizations | Astrology grammars |
| `theme`, `mood`, `tradition` | Free-form taxonomy | Any grammar |

> ⚠️ **YouTube field naming gotcha:** The canonical field name is
> `youtube_video_id`, NOT `video_id`. Earlier drafts of grammars
> shipped with `video_id` will not be recognized by the performance
> viewer. Always use the `youtube_` prefix.

You can also put arbitrary keys in `metadata` for editorial / study
purposes. The viewer ignores unknown keys.

The keys that DRAW something also live in `metadata`, and they have their own
sections below: `kind` (*Item kinds*), `slide` and the `card_*` look family
plus `card_hold_sec` (*Look and dwell*), `embed_url` (*kind: "embed"*). Two
metadata keys that look like playback fields and are not: `subtitles` (stored
caption cues, used for research and for finding cut points — the viewer never
draws them) and `excerpt` (the words inside a cut, an editing aid).

---

## Item kinds — `metadata.kind`

In a sequence (a film, a playlist), an item can declare **what it is**. The
value is one of:

| `metadata.kind` | what it is |
|---|---|
| `divider` | a chapter card — a title on a coloured ground, no media |
| `clip` | a cut from a video |
| `note` | a text beat |
| `slide` | an animated data panel the viewer draws from `metadata.slide` |
| `embed` | a live web page played inside the viewer (below) |

An unknown value is rejected by the write path with a 400 naming the allowed
list — never silently stored, never silently dropped. An item with no `kind`
renders exactly as it always did.

### `kind: "embed"` — a live page as an item

An item that plays a whole other web page inside the viewer, the way a `clip`
plays a video. Used for interactive things that are not video and not a drawn
panel: an agent-based model, a probability game, a chart.

| field | type | default | what it is |
|---|---|---|---|
| `metadata.kind` | `"embed"` | — | required; without it `embed_url` is ignored |
| `metadata.embed_url` | string | — | required; `https://` on an allowed host (below) |
| `metadata.embed_ratio` | `"16:9"` \| `"4:3"` \| `"3:2"` \| `"1:1"` \| `"9:16"` | `"16:9"` | the frame's aspect ratio |
| `metadata.embed_interactive` | boolean | `false` | may the viewer touch it **while the device is walled** |
| `metadata.card_hold_sec` | number | `30` | dwell in Focus / autoplay, same field every non-video item uses |

**Allowed hosts.** `recursive.eco`, any `*.recursive.eco` subdomain, and
`playfulprocess.github.io`. Anything else — and any malformed URL — is refused:
the write path answers a 400 naming the allowed hosts, and a value that reaches
the viewer another way renders as a plain title card, never a blank and never a
surprise frame.

**The wall.** An embedded page must never be a way out. On a walled
(Focus/kiosk) device the frame is display-only: a transparent shield sits over
it and eats every pointer event, and the "Open in a new tab" link is hidden.
`embed_interactive: true` lifts the shield for that one item — the link stays
hidden regardless. In Standard the frame is fully interactive and the link shows.

**The sandbox.** `sandbox="allow-scripts allow-same-origin"` and no `allow`
attribute. The page may run and read its own storage; it cannot submit a form,
open a popup, start a download, navigate the top-level window, lock the pointer,
or ask for camera / microphone / geolocation.

**Example**

```json
{
  "name": "Zero-intelligence traders",
  "sections": { "Note": "Gode & Sunder 1993 — price finds equilibrium with no strategy at all." },
  "metadata": {
    "kind": "embed",
    "embed_url": "https://playfulprocess.github.io/emergence-lab/models/zero-intelligence.html",
    "embed_ratio": "16:9",
    "embed_interactive": true,
    "card_hold_sec": 45
  }
}
```

---

## Category & section roles (astrology customization)

For `astrology` (and Vedic/Jyotish) grammars, the astrology viewer buckets
items into tabs — Planets, Signs, Houses, Aspects, etc. — by reading each
item's `category`. A default table of category names is already recognized,
no configuration needed:

| Category | Viewer role |
|---|---|
| `planet` | planet |
| `sign` | sign |
| `house` | house |
| `aspect` | aspect |
| `graha` (Vedic) | planet |
| `rashi` (Vedic) | sign |
| `bhava` (Vedic) | house |
| `nakshatra` (Vedic) | nakshatra |
| `yoga`, `drishti` (Vedic) | emergence |
| `dignity`, `position` | modifier |

### Custom category names — `_category_roles`

If your tradition uses category names outside this list (a regional or
invented tradition, not Western or Jyotish), declare a mapping at the
**grammar root** — this ADDS to the default table above, it doesn't replace it:

```jsonc
{
  "name": "My Astrology Tradition",
  "grammar_type": "astrology",
  "_category_roles": {
    "planetary-lord": "planet",
    "constellation": "sign"
  },
  "items": [ /* items whose "category" is "planetary-lord", "constellation", etc. */ ]
}
```

Valid target roles: `planet`, `sign`, `house`, `aspect`, `nakshatra`,
`emergence`, `modifier`.

### Custom section names — `_section_roles`

The astrology viewer also maps **section names** to display roles (which tab
subsection a section's content lands in) — `Shadow`, `Light`, `Archetype`,
`Karakatvas`/`Significations`, `Affirmation`/`Mantra`, `Questions`,
`Invitation`, and description-like sections (`Interpretation`, `Description`,
`Story`, `Meaning`, `Summary`) are recognized by default. If your sections
use different labels, declare `_section_roles` alongside `_category_roles`:

```json
{
  "_section_roles": {
    "Karakatvas": "significations",
    "Mantra": "affirmation"
  }
}
```

Both `_category_roles` and `_section_roles` are reserved, **grammar-root**
fields — never put them inside an item.

---

## Performance object — what an item PLAYS

For grammars where each item is a clip from a YouTube video — common
in `sequence` grammars and useful in `custom` grammars too — each
item carries an optional `performance` object.

Everything in `performance` is measured in the **source video's own seconds**,
the same clock as `start_sec`. That is the one thing to hold on to: an overlay
at `start_sec: 1085` appears when the source video's playhead reaches 18:05,
not 1085 seconds after the item came on screen. Screen time — how long a card
or a slide sits there — is a different clock and lives in `metadata`; see
*Look and dwell* below.

```jsonc
{
  "id": "clip-01-misconceptions-opening",
  "name": "Misconceptions about Hinduism — opening (5:00–7:30)",
  "metadata": {
    "youtube_video_id": "XS7RKHR_ink",
    "youtube_url": "https://www.youtube.com/watch?v=XS7RKHR_ink"
  },
  "performance": {
    "start_sec": 300,         // crop start, in the source's seconds
    "end_sec": 450,           // crop end — reaching it advances the playlist
    "volume": 1.0,            // the primary video's level, 0..1
    "video_visible": true,    // false = audio-only; show a picture instead
    "cover_image_url": "https://...",   // OPTIONAL — the audio-only picture

    "background_audio": {     // OPTIONAL — a second video playing underneath
      "youtube_video_id": "different-id-here",
      "start_sec": 0,
      "end_sec": 600,
      "volume": 0.45
    },

    "audio_url": "https://.../line.mp3",  // OPTIONAL — a spoken clip for THIS item
    "audio_delay_sec": 2.5,               // OPTIONAL — seconds before it starts (0–120)

    "mutes": [                // OPTIONAL — bleeps on the primary video
      { "start_sec": 1989.05, "end_sec": 1990 }
    ],

    "overlays": [             // OPTIONAL — timed text or pictures over the clip
      {
        "kind": "text",       // "text" or "image"
        "content": "Overlay text, or an https image address",
        "start_sec": 5,       // when it appears, in the source's seconds
        "end_sec": 12,        // when it goes
        "x_pct": 10,          // horizontal position, 0..100
        "y_pct": 80,          // vertical position, 0..100
        "width_pct": 80,      // width, % of the player
        "backdrop": "rgba(0,0,0,0.6)",  // OPTIONAL — a plate behind it
        "align": "center",    // OPTIONAL, text only — start | center | end
        "highlight": false    // OPTIONAL, text only — the marker sweep
      }
    ],

    "motion": { "kind": "breathe", "to": { "scale": 1.03 } },  // OPTIONAL, image items
    "transition": { "kind": "crossfade", "duration_sec": 0.8 },// OPTIONAL

    "words": [                // OPTIONAL — per-word karaoke timing (see below)
      { "w": "In", "start": 5.0, "end": 5.2 },
      { "w": "the", "start": 5.2, "end": 5.3 }
    ]
  },
  "sections": {
    "What she says": "...",
    "Why this clip": "..."
  }
}
```

### The crop

| field | type | what it does |
|---|---|---|
| `start_sec` | number | where the clip begins in the source video |
| `end_sec` | number | where it ends — reaching it advances the playlist |
| `volume` | number 0..1 | the primary video's level (default 1) |
| `video_visible` | boolean | `false` = audio-only: the picture shows, the sound keeps running |
| `cover_image_url` | string | the picture for `video_visible: false`. It is an OVERRIDE — without it the item's own `image_url` is used, and that is the ordinary way to do this |

### Pictures over a clip — `overlays` with `kind: "image"`

An image overlay is **the** way to put a picture over a playing clip. There is
no separate slideshow, gallery or frames kind, and none is needed.

| field | what it does |
|---|---|
| `content` | an `https://` image address on an allowed host (below) |
| `start_sec` / `end_sec` | the window, in the source video's seconds |
| `fit` | `"cover"` (crops) or `"contain"` (letterboxes) — the picture fills the whole frame, and `x_pct` / `y_pct` / `width_pct` are then ignored and may be omitted |
| `backdrop` | a colour painted behind it; across the frame when `fit` is set |
| `x_pct` / `y_pct` / `width_pct` | position and width as % of the player — required **unless** `fit` is set |

**Allowed image hosts** (for `overlays[].content`, and for an image used as a
background — see *Look and dwell*): `upload.wikimedia.org`,
`images-assets.nasa.gov`, `i.ytimg.com`, `img.youtube.com`, the recursive.eco
CDN, and `recursive.eco` / `*.recursive.eco`. `https` only, no credentials, no
custom port. Anything else is refused by the write path with a 400 — copy the
picture to the CDN first.

**A run of pictures** is simply several image overlays in a row, each window
butted against the next. This is the whole recipe; there is no other mechanism:

```jsonc
"overlays": [
  { "kind": "image", "fit": "contain", "backdrop": "#05050a", "content": "https://upload.wikimedia.org/…/a.jpg", "start_sec": 20.1, "end_sec": 24.1 },
  { "kind": "image", "fit": "contain", "backdrop": "#05050a", "content": "https://upload.wikimedia.org/…/b.jpg", "start_sec": 24.1, "end_sec": 28.1 },
  { "kind": "image", "fit": "contain", "backdrop": "#05050a", "content": "https://upload.wikimedia.org/…/c.jpg", "start_sec": 28.1, "end_sec": 32.1 }
]
```

At four seconds apart that reads as a sequence of plates; at 0.4 seconds apart
the same array is stop motion.

### Words over a clip — `overlays` with `kind: "text"`

`content` is the words themselves, rendered as a text node — never HTML, never
CSS. Besides the shared fields above, a text overlay takes:

| field | what it does |
|---|---|
| `backdrop` | a padded plate behind the words, e.g. `"rgba(0,0,0,0.6)"`, so they read over the video |
| `align` | `"start"`, `"center"` or `"end"` — where the words sit in their box |
| `highlight` | `true` gives the marker sweep |
| `fit` | a text overlay with `fit` is a full-frame panel: the words centred over the backdrop while the clip's audio keeps running underneath |

A long quote is several text overlays handing over to each other, each with its
own window — not one overlay with line breaks in it.

**Words over footage go here, not in a slide.** An item that carries both a
video and a `metadata.slide` plays the video and never draws the slide.

### Sound — the bed, the voice, the level, the bleeps

Four fields, one object. They are the whole sound vocabulary of an item:

| field | what it is |
|---|---|
| `background_audio` | **the bed** — a second YouTube video playing underneath, `{ youtube_video_id, start_sec, end_sec, volume }`. Name the same `youtube_video_id` on consecutive items and the bed carries across the cut, so one recording can run under a whole opening |
| `audio_url` (+ `audio_delay_sec`) | **the voice** — a hosted `.mp3` / `.m4a` / `.wav` for this one item. On a card it plays while the card shows and lengthens the dwell to cover `audio_delay_sec` + the clip. This is NOT the grammar's narration track (see *Audio karaoke mode*), which owns the whole playlist's clock; this one rides the playlist's clock and stands down while a narration track plays |
| `volume` | **the level** — the primary video, 0..1 |
| `mutes` | **the bleeps** — `[{ start_sec, end_sec }]` windows where the primary plays silent with a 1 kHz tone under them, so the gap reads as a bleep and not as a dropout. Source-video seconds, like everything else in `performance`. Use this to lose one word instead of re-cutting the clip |

### Motion and transitions (Performance mode only)

Two optional fields that only apply while the viewer is in Performance mode,
and that `prefers-reduced-motion` switches off:

| field | what it is |
|---|---|
| `motion` | Ken-Burns drift on an **image** item: `{ kind: "none" \| "zoom-in" \| "zoom-out" \| "breathe", from: { scale, x, y }, to: { scale, x, y }, duration_sec, easing }`. `x` and `y` are 0..1 of the frame and set one anchor point; `scale` is a multiplier around 1. Without `duration_sec` the crop window is used, else 6 s (zoom) / 8 s (breathe) |
| `transition` | how this item covers the swap in from the previous one: `{ kind: "cut" \| "crossfade" \| "dip-to-colour" \| "wipe" \| "iris", duration_sec (0.1–3), colour }`. A video on either side always cuts — an iframe cannot crossfade |

Both take grammar-level defaults at the **grammar root**, under
`metadata.motion_defaults`: `{ "motion": {...}, "transition": {...} }`. An
item's own value wins over the default.

### Audio karaoke mode (`words`)

Some grammars are a single narrated audio track (a karaoke book / dramatic
reading) rather than per-item YouTube clips. For these, the **grammar root**
carries the narration track in `metadata.audio` (a hosted audio URL) and
optionally `metadata.total_sec` / `metadata.crop_ranges`. Each item then sets
`performance.video_visible: false` and times its own text against that shared
track with `performance.words` — one entry per spoken word, in seconds,
**absolute within the grammar-level narration track** (not relative to the
item):

```jsonc
{
  "name": "A Narrated Poem",
  "grammar_type": "custom",
  "metadata": {
    "audio": "https://.../narration.mp3",
    "total_sec": 612,
    "audio_source": "LibriVox (public domain) · Jane Reader (2026)"
  },
  "items": [
    {
      "id": "stanza-1",
      "name": "Stanza 1",
      "sections": { "Text": "In the beginning..." },
      "performance": {
        "video_visible": false,
        "start_sec": 12.4,          // this item's first word (absolute in the track)
        "end_sec": 18.9,            // this item's last word
        "cover_image_url": "https://...",   // shown instead of a video
        "words": [
          { "w": "In", "start": 12.4, "end": 12.6 },
          { "w": "the", "start": 12.6, "end": 12.7 },
          { "w": "beginning", "start": 12.7, "end": 13.3 }
        ]
      }
    }
  ]
}
```

`words` is normally produced by an audio-alignment tool (Whisper word
timestamps aligned onto the item's own text), not hand-written. The field
names are terse (`w` / `start` / `end`) because there's one object per word.

**`metadata.audio` and `performance.audio_url` are two different things** and
must not be confused: the narration track owns advancement for the whole
grammar, while `audio_url` is one spoken line riding the playlist's own clock.
Giving a film a narration track turns it into karaoke.

### Field-name conventions inside `performance`

Note the **singular `sec`** (not `seconds`):

- ✅ `start_sec`, `end_sec`
- ❌ `start_seconds`, `end_seconds`

This applies inside `performance`, inside `background_audio`, inside
`overlays[]`, and inside `mutes[]`.

### When to use `performance`

- ✅ Sequence grammars where items are video clips
- ✅ Custom grammars that want timestamped audio/video segments
- ✅ Any item where you want the viewer to play a cropped portion
- ❌ Static items (tarot cards, hexagrams) — leave `performance` off

The `performance` object lives on the **individual item**, not at
the grammar root. Each clip has its own start/end.

---

## Look and dwell — what a non-video item shows, and for how long

An item with no video still has to look like something and stay on screen for
some length of time. Those are two small vocabularies in `metadata`, and they
are easy to mix up with `performance`: **`performance` counts the source
video's seconds; look and dwell describe the screen.**

### Look — the ground, the ink, the type

A plain card (including a `divider`) and a slide take the same four values
under different names. The values are identical; only the spelling differs by
where they sit:

| on a plain card | inside `metadata.slide` | what it is |
|---|---|---|
| `card_bg` | `bg` | the ground: a colour, a `linear-gradient(...)` / `radial-gradient(...)`, a bare `https` image address, or `url('https://…') center/cover`. An image must be on the allowed-host list above |
| `card_dim` | `dim` | 0–0.9 — darken an image ground so the words stay readable |
| `card_ink` | `ink` | the text colour |
| `card_font` | `font` | `serif` \| `sans` \| `narrow` \| `mono` \| `gothic` |
| `card_subtitle` | (a slide line) | one line under the card's title |
| — | `accent` | the kicker / bars / marker colour |
| — | `align`, `size` | `start` \| `center`; `normal` \| `large` \| `huge` |

A slide additionally takes the opening-title pieces `stars` (`true`, or 0–1 for
density: a starfield over the ground), `outline` (hollow letters), `valign:
"middle"`, and — on a `crawl` — `logo`, `logo_sec` (2–30) and `width` (40–160,
the text column as a % of the stage).

Colours accept `#hex`, `rgb()`, `hsl()` or a colour name. They are never CSS:
the viewer owns the type and the palette, and a value it does not recognise is
refused by the write path rather than injected into a style attribute.

```jsonc
// a chapter card: a NASA ground, dimmed, with yellow narrow type
"metadata": {
  "kind": "divider",
  "card_bg": "url('https://images-assets.nasa.gov/image/…~medium.jpg') center/cover",
  "card_dim": 0.65,
  "card_ink": "#feda4a",
  "card_font": "narrow",
  "card_subtitle": "Every story about technology going wrong begins with a mad scientist."
}
```

### Dwell — how long it stays

| field | applies to | default |
|---|---|---|
| `metadata.slide.duration_sec` | an item with a slide bag — it outranks `card_hold_sec` | a crawl reads at ~0.3 s a word; a text slide ~1.6 s a line; max 600 |
| `metadata.card_hold_sec` | a card, an image, a divider, a note, an embed | 10 s (30 s for an `embed`) |
| `metadata.no_pause_after` | any item — `true` skips the beat between items so the cut flows straight on | — |

The precedence is exactly that order: a slide's own `duration_sec`, else
`card_hold_sec`, else the viewer's default. Two things that are **not** a
dwell, and are the commonest confusion here:

- `performance.end_sec` ends a **clip**. It is the source video's clock, and a
  dwell can never shorten or lengthen a video.
- `metadata.slide.motion_sec` is how much of the dwell the movement takes; what
  is left holds the end state (black after a fade, say). It is motion inside
  the dwell, not a second dwell.

One exception worth knowing: an item with `performance.audio_url` holds for at
least `audio_delay_sec` + the length of the clip, so a card is never cut off
mid-sentence.

---

## Reference items & meta-grammars (a grammar of grammars)

An item does not have to hold its own content — it can **point at another
grammar/document**. This is what makes a "grammar of grammars" possible: a
meta-grammar whose items are themselves whole decks or texts, so you can build a
tree whose leaves drill down into full sub-grammars (recursion **by reference**,
not by merging the item and grammar types).

On a **UnifiedItem**:

| Field | Meaning |
|---|---|
| `item_type` | `"content"` (default) or `"reference"` |
| `ref_document_id` | the `user_document` id this item opens |
| `ref_item_id` | OPTIONAL — the specific item **inside** `ref_document_id` this item points at. Omit it and the reference opens the whole target document; set it and the reference opens exactly one item within that document. |
| `ref_preview` | how the target opens: `"default" \| "study" \| "grammar" \| "altar"` |
| `grammars` | array of linked grammar/document ids (multi-link) |

On the **grammar root**:

| Field | Meaning |
|---|---|
| `default_preview` | the viewer that opens by default: `"grammar" \| "study" \| "tree" \| "altar" \| "course" \| "thumbnails"` |

The viewer renders a reference item as a link that opens the target
(`/play?id=<ref_document_id>`, or `?id=<ref_document_id>&item=<ref_item_id>`
when `ref_item_id` is set). Combined with the L1/L2/L3 `composite_of`
emergence, `default_preview: "tree"` renders the whole thing in the tree-viewer.

**Resolution is additive, not a replacement.** A reference item is allowed to
carry its own content too (its own `sections`, e.g. a short provenance
blurb) — when the target resolves, the viewer renders the item's OWN content
together with the resolved SOURCE item's content, side by side. Don't treat
"this reference item already has some sections filled in" as a reason to
skip resolving it; resolve whenever `ref_document_id` (+ optionally
`ref_item_id`) is present, regardless of what else is on the item.

### Example 1 — a meta-grammar leaf that opens a full deck

```json
{
  "id": "deck-visconti-sforza",
  "name": "Visconti-Sforza Tarot",
  "level": 1,
  "item_type": "reference",
  "ref_document_id": "<the deck's user_document id>",
  "ref_preview": "grammar",
  "sections": { "What it is": "The oldest near-complete tarot…" },
  "metadata": { "branch": "branch-roots" }
}
```

### Example 1b — a meta-grammar leaf that opens ONE card inside a deck (`ref_item_id`)

Use `ref_item_id` when the meta-grammar's leaves are individual cards drawn
from many source decks, rather than whole decks — e.g. a "Tarot — All Decks,
Many Lenses" meta-grammar with one item per source-deck card:

```json
{
  "id": "leaf-visconti-the-fool",
  "name": "The Fool (Visconti-Sforza)",
  "level": 1,
  "item_type": "reference",
  "ref_document_id": "<the Visconti-Sforza deck's user_document id>",
  "ref_item_id": "<that deck's 'The Fool' item id>",
  "ref_preview": "study",
  "sections": {
    "Origin": "One of many cards drawn from every deck in the commons."
  }
}
```

None of this leaf's card content (keywords, interpretation, image) needs to
be duplicated inline — it resolves live from the source deck, and the
"Origin" section renders alongside it.

### Example 2 — the genealogy tree that opens in tree view

A `grammar_type: "custom"` meta-grammar with `"default_preview": "tree"` and three
levels: **L1** decks (reference items), **L2** branches (`composite_of` the decks),
**L3** root (`composite_of` the branches). The tree-viewer
(`recursive.eco/pages/tree-viewer.html?type=custom&id=…`) draws root → branches →
decks, and each deck leaf opens its own grammar.

> Real example in this repo: **`grammars/tree-of-tarot/grammar.json`** — the
> genealogy of tarot. (Its leaves currently use text references; after the decks are
> imported to Supabase, set `ref_document_id` on each leaf so clicking opens the deck.
> See `plan/tarot-roadmap-and-supabase-log.md` §3d.)

---

## Three common mistakes (when grammars won't load)

These three errors account for the vast majority of "won't load"
failures. Check yours against this list first.

### Mistake 1 — `grammar_type: "performance"`

`"performance"` is not a valid grammar type. It is a viewer mode.

✅ For a curated video playlist: `"grammar_type": "sequence"`
✅ When unsure: `"grammar_type": "custom"`

### Mistake 2 — `emergences[]` at the top level

A separate top-level `emergences` array is not supported. Merge the
L2/L3 items into `items[]` with their `composite_of` field intact.

```diff
- "items": [ /* L1 items */ ],
- "emergences": [ /* L2 items */ ]
+ "items": [
+   /* L1 items */,
+   /* L2 items with composite_of */
+ ]
```

### Mistake 3 — `metadata.video_id` / `metadata.start_seconds`

The canonical field names are:

- `metadata.video_id` → `metadata.youtube_video_id`
- `metadata.start_seconds` → `performance.start_sec` (moved to `performance`)
- `metadata.end_seconds` → `performance.end_sec` (moved to `performance`)

Each item that has a YouTube clip should have BOTH
`metadata.youtube_video_id` AND a `performance` object with
`start_sec` and `end_sec`.

---

## Minimal working examples

### Tarot card (L1 only)

```json
{
  "name": "Tiny Tarot",
  "description": "Just one card.",
  "grammar_type": "tarot",
  "tags": ["tarot"],
  "is_published": false,
  "items": [
    {
      "id": "major-00-fool",
      "name": "The Fool",
      "sort_order": 0,
      "category": "major_arcana",
      "keywords": ["new beginnings"],
      "sections": {
        "Interpretation": "The beginning of all journeys.",
        "Reversed": "Fear of the unknown."
      }
    }
  ]
}
```

### Sequence of video clips with emergence theme

```json
{
  "name": "Three clips on dharma",
  "description": "Curated video study.",
  "grammar_type": "sequence",
  "tags": ["dharma", "study"],
  "is_published": false,
  "items": [
    {
      "id": "clip-01",
      "name": "What is dharma",
      "category": "foundation",
      "sort_order": 1,
      "metadata": {
        "youtube_video_id": "abc12345XYZ",
        "youtube_url": "https://www.youtube.com/watch?v=abc12345XYZ"
      },
      "performance": {
        "start_sec": 120,
        "end_sec": 240,
        "video_visible": true,
        "volume": 1.0
      },
      "sections": {
        "Summary": "Teacher defines dharma in plain terms."
      }
    },
    {
      "id": "clip-02",
      "name": "The four legs of dharma",
      "category": "foundation",
      "sort_order": 2,
      "metadata": {
        "youtube_video_id": "def67890XYZ",
        "youtube_url": "https://www.youtube.com/watch?v=def67890XYZ"
      },
      "performance": {
        "start_sec": 600,
        "end_sec": 780,
        "video_visible": true,
        "volume": 1.0
      },
      "sections": {
        "Summary": "Satyam, daya, sochá, tapas."
      }
    },
    {
      "id": "theme-foundations",
      "name": "Foundations of dharma",
      "category": "theme",
      "sort_order": 100,
      "composite_of": ["clip-01", "clip-02"],
      "sections": {
        "About this theme": "Two starting-point clips."
      }
    }
  ]
}
```

Both clips live in `items[]`. The theme is also an item in `items[]`,
just with `composite_of`. No separate `emergences[]` array.

---

## Validating before upload

A minimal Python check:

```python
import json
g = json.load(open("your-grammar.json", encoding="utf-8"))

# Required top-level
assert "name" in g and "description" in g
assert "grammar_type" in g
assert g["grammar_type"] in {
    "tarot", "iching", "astrology", "sequence",
    "course", "prompt", "birthchart", "altar", "music", "custom"
}
assert isinstance(g.get("items"), list) and len(g["items"]) > 0

# No top-level emergences array
assert "emergences" not in g, "Move emergences into items[] with composite_of"

# Per-item checks
ids = {it["id"] for it in g["items"]}
for it in g["items"]:
    assert "id" in it and "name" in it and "sections" in it
    if "composite_of" in it:
        for child in it["composite_of"]:
            assert child in ids, f"composite_of references missing id: {child}"
    if "metadata" in it:
        # Common YouTube field-name gotcha
        assert "video_id" not in it["metadata"], \
            "Rename metadata.video_id -> metadata.youtube_video_id"
    if "performance" in it:
        p = it["performance"]
        # Singular "sec" not "seconds"
        assert "start_seconds" not in p, "Rename performance.start_seconds -> start_sec"
        assert "end_seconds" not in p, "Rename performance.end_seconds -> end_sec"

print("OK")
```

If you write a more thorough validator and submit it as
`scripts/validate-grammar.py`, others will thank you.

---

## See also

- [`README.md`](README.md) — repo overview and how to copy / fork / share grammars
- [`QUICKSTART.md`](QUICKSTART.md) — fastest path to your first grammar
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution workflow and git identity setup
- [`CLAUDE.md`](CLAUDE.md) — guidance for AI assistants working in this repo (includes
  monad/library-placement fields and the emergence-creation playbook)
- [`schemas/SCHEMAS_GUIDE.md`](schemas/SCHEMAS_GUIDE.md) — directory layout for the
  `schemas/` subtree

If you find a discrepancy between this doc and the actual behavior of
the editor or the viewer, **the editor's behavior is the source of
truth** — please open an issue or PR so we can update this doc.
