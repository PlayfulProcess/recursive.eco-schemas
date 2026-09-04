# ElevenLabs TTS Pipeline — Future Plan

**Date:** 2026-03-12
**Status:** Future — build after meta-grammar is ready
**Applies to:** All grammars with narrative text (Alice, Looking-Glass, bedtime mythology series, etc.)

---

## Overview

Transform grammar JSON files into ElevenLabs-ready scripts with multi-voice dialogue, natural pauses, and karaoke-style ALL CAPS highlighting. Two pipelines:

1. **Prose grammars** (Alice, Looking-Glass, etc.) — extract, clean, split into dialogue segments with character voice assignment
2. **Verse grammars** (bedtime mythology series) — lighter processing, ALL CAPS keywords become emphasis markers for TTS

---

## Pipeline 1: Prose Grammars (Alice, etc.)

### Input Format
Grammar JSON with `items[].sections["Story (Original Text)"]`. Each item is a scene (L1) grouped into chapters (L2).

### Processing Steps

#### Step 1: Extract and Concatenate
For each chapter (L2 item), gather all L1 children's `sections["Story (Original Text)"]` in sort_order, concatenate with paragraph breaks.

#### Step 2: Clean Text
- Strip `_emphasis_` markers (underscore italics)
- Normalize curly quotes (`""''`) to straight quotes (`""''`)
- Unwrap hard line breaks within paragraphs (keep paragraph breaks as `\n\n`)
- Normalize whitespace (collapse multiple spaces)
- Strip any remaining markdown formatting

#### Step 3: Dialogue Segmentation
Parse text into segments, detecting:

1. **Quoted dialogue**: Everything between quotation marks
2. **Speaker attribution**: Pattern matching for `"said Alice"`, `"cried the Queen"`, `Alice said`, etc.
3. **Voice role assignment**:
   - `NARRATOR` — all non-dialogue text
   - `ALICE` — Alice's dialogue (the protagonist gets her own voice)
   - `MALE` — Male characters (King, Hatter, White Rabbit, Caterpillar, etc.)
   - `FEMALE` — Female characters (Queen, Duchess, Cook, etc.)
   - `QUIRKY` — Non-human/unusual characters (Cheshire Cat, Mock Turtle, Gryphon, Dormouse)

4. **Character-to-voice mapping** (per grammar):
```
# Alice in Wonderland
ALICE: alice
White Rabbit: male
Caterpillar: quirky
Cheshire Cat: quirky
Mad Hatter: quirky
March Hare: quirky
Dormouse: quirky
Queen of Hearts: female
King of Hearts: male
Duchess: female
Cook: female
Mock Turtle: quirky
Gryphon: quirky
Mouse: male
Dodo: male
Bill the Lizard: male
Pigeon: female
```

#### Step 4: Format as ElevenLabs Script
```
[NARRATOR]
Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it,

<break time="0.5s"/>

[ALICE]
"and what is the use of a book without pictures or conversations?"

<break time="0.5s"/>

[NARRATOR]
So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.

<break time="0.8s"/>

[MALE]
"Oh dear! Oh dear! I shall be late!"

<break time="0.5s"/>
```

#### Step 5: Pause Cues
- `<break time="0.8s"/>` — between paragraphs
- `<break time="0.5s"/>` — between speaker changes
- `<break time="1.2s"/>` — between scenes (L1 boundaries)
- `<break time="2.0s"/>` — between chapters (L2 boundaries)

### Output
One script file per chapter, ready to paste into ElevenLabs Projects/Script editor. Voice assignment (NARRATOR, ALICE, MALE, FEMALE, QUIRKY) maps to ElevenLabs voice slots that the user assigns manually.

---

## Pipeline 2: Verse Grammars (Bedtime Mythology Series)

### Input Format
Grammar JSON with `items[].sections["Story"]`. ALL CAPS keywords embedded in verse.

### Processing Steps

#### Step 1: Extract
For each L1 item, extract `sections["Story"]`.

#### Step 2: ALL CAPS → SSML Emphasis
Convert ALL CAPS words to SSML emphasis markers:
```
Input:  "RAMA stood on the mountain PEAK"
Output: "<emphasis level="strong">Rama</emphasis> stood on the mountain <emphasis level="strong">peak</emphasis>"
```

This creates the karaoke-style vocal emphasis pattern — the TTS voice stresses the capitalized words naturally.

#### Step 3: Stanza Breaks
Insert pauses between stanzas:
```
<break time="1.0s"/>
```
Between the three stanzas of each story.

#### Step 4: Format
```
[NARRATOR]
<emphasis level="strong">Rama</emphasis> stood on the mountain <emphasis level="strong">peak</emphasis>.
The ocean stretched before him. <emphasis level="strong">Bleak</emphasis>
and endless, a hundred leagues of <emphasis level="strong">wave</emphasis>
and wind and salt. To be <emphasis level="strong">brave</emphasis>
is one thing. To leap across an <emphasis level="strong">ocean</emphasis>
is something else entirely. <emphasis level="strong">Devotion</emphasis>
drove him.

<break time="1.0s"/>

He crouched. The mountain <emphasis level="strong">cracked</emphasis>
beneath his feet...
```

### Voice Assignment for Verse
Single narrator voice for most stories. The bedtime mythology series is designed for a warm, rhythmic reading voice — not multi-character drama.

**Exception:** The Tibetan dream grammar (`tibetan-dream-kids`) could use a second voice for the "Wonder" sections — a child's voice asking questions.

---

## Implementation Plan

### Phase 1: Build the Script Generator
Write a Python script (`scripts/generate_tts_scripts.py`) that:
1. Takes a grammar slug and chapter/item ID
2. Reads the grammar JSON
3. Applies the appropriate pipeline (prose vs. verse)
4. Outputs formatted ElevenLabs script to `tts-scripts/{grammar-slug}/`

### Phase 2: Character Voice Database
Create a `tts-voices.json` mapping file:
```json
{
  "alice-in-wonderland": {
    "character_map": {
      "Alice": "alice",
      "White Rabbit": "male",
      "Cheshire Cat": "quirky"
    },
    "voice_slots": {
      "narrator": "ElevenLabs voice ID",
      "alice": "ElevenLabs voice ID",
      "male": "ElevenLabs voice ID",
      "female": "ElevenLabs voice ID",
      "quirky": "ElevenLabs voice ID"
    }
  }
}
```

### Phase 3: Batch Generation
Generate all scripts for a grammar at once. For Alice (12 chapters), this produces 12 script files ready for ElevenLabs.

### Phase 4: Integration with Viewer
The recursive.eco viewer could eventually:
1. Host audio files alongside grammar items
2. Highlight ALL CAPS words in sync with TTS playback (karaoke mode)
3. Show which character is speaking with visual indicators

---

## Manual Workflow (Until Script Is Built)

For now, the process is manual:
1. User pastes chapter JSON into Claude
2. Claude formats it as an ElevenLabs script with voice markers
3. User pastes into ElevenLabs Projects/Script editor
4. User assigns voices manually and previews
5. User generates audio and uploads to R2

This works for one-chapter-at-a-time processing. The script automates it for batch processing.

---

## ALL CAPS Karaoke Mode (Viewer Feature — Future)

The ALL CAPS keywords in the bedtime mythology series are designed for karaoke-style highlighting during TTS playback:

1. **During playback**: The viewer highlights each ALL CAPS word as the TTS voice reaches it
2. **Visual treatment**: ALL CAPS words pulse or glow in a contrasting color
3. **Child interaction**: Tap a highlighted word to hear it repeated (vocabulary building)
4. **Parent mode**: Toggle karaoke mode on/off

This requires:
- Timestamp data from ElevenLabs (word-level timing)
- A mapping from ALL CAPS words in the grammar JSON to timestamp positions in the audio
- Viewer-side rendering logic (CSS animation synced to audio progress)

---

## Dependencies

- All grammars must be complete with final text before TTS generation
- Meta-grammar cross-references should be built first (so we can eventually generate "story path" playlists that follow an archetype across traditions)
- ElevenLabs account with sufficient character quota for ~420 stories × ~500 words = ~210,000 words
- Voice selection: 1 warm narrator voice for verse, 5 voices for prose (narrator, child, male, female, quirky)
