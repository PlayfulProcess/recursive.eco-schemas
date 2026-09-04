/**
 * Generate word-level timestamps for the preface poem song using OpenAI Whisper API.
 *
 * Input:  grammars/alice-5-minute-stories/audio/all-in-the-golden-afternoon.mp3
 * Output: grammars/alice-5-minute-stories/audio/poem-whisper.json
 *
 * Usage:
 *   node scripts/generate-poem-whisper.mjs
 */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import OpenAI from 'openai';
import { config } from 'dotenv';
import { createReadStream } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load env from recursive-eco (same pattern as generate-whisper-timestamps.mjs)
const envPaths = [
  resolve(__dirname, '../.env'),
  resolve(__dirname, '../../recursive-eco/.env.local'),
  resolve(__dirname, '../../recursive-eco/apps/flow/.env.local'),
];
for (const p of envPaths) {
  if (existsSync(p)) config({ path: p });
}

const AUDIO_PATH = resolve(__dirname, '../grammars/alice-5-minute-stories/audio/all-in-the-golden-afternoon.mp3');
const OUTPUT_PATH = resolve(__dirname, '../grammars/alice-5-minute-stories/audio/poem-whisper.json');

if (!existsSync(AUDIO_PATH)) {
  console.error('Audio file not found:', AUDIO_PATH);
  process.exit(1);
}

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const sizeMB = (readFileSync(AUDIO_PATH).length / 1024 / 1024).toFixed(1);
console.log(`Poem audio: ${sizeMB}MB — sending to Whisper...`);

const start = Date.now();

const response = await openai.audio.transcriptions.create({
  file: createReadStream(AUDIO_PATH),
  model: 'whisper-1',
  response_format: 'verbose_json',
  timestamp_granularities: ['word'],
  language: 'en',
  prompt: 'All in the golden afternoon, by Lewis Carroll. A song setting of the dedicatory poem from Alice in Wonderland. Full leisurely we glide.',
});

const elapsed = ((Date.now() - start) / 1000).toFixed(1);
const wordCount = response.words?.length || 0;
console.log(`${wordCount} words transcribed in ${elapsed}s`);

const output = {
  text: response.text,
  duration: response.duration,
  words: (response.words || []).map(w => ({
    word: w.word,
    start: w.start,
    end: w.end,
  })),
  generated: new Date().toISOString(),
};

writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2));
console.log(`Saved to ${OUTPUT_PATH}`);
console.log(`\nFirst 10 words:`);
output.words.slice(0, 10).forEach(w => {
  console.log(`  "${w.word}" ${w.start.toFixed(2)}s — ${w.end.toFixed(2)}s`);
});
