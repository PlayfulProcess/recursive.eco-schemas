/**
 * Generate word-level timestamps from LibriVox audio using OpenAI Whisper API.
 *
 * Whisper's "verbose_json" response_format with timestamp_granularities=["word"]
 * returns word-level start/end times.
 *
 * Usage:
 *   node scripts/generate-whisper-timestamps.mjs                # All chapters
 *   node scripts/generate-whisper-timestamps.mjs --chapter 1    # Just chapter 1
 *   node scripts/generate-whisper-timestamps.mjs --dry          # Show what would be processed
 *
 * Output: grammars/alice-5-minute-stories/audio/librivox/whisper-ch{NN}.json
 *         grammars/alice-5-minute-stories/audio/librivox/whisper-manifest.json (combined)
 */
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import OpenAI from 'openai';
import { config } from 'dotenv';
import { createReadStream } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load env from recursive-eco
const envPaths = [
  resolve(__dirname, '../../recursive-eco/.env.local'),
  resolve(__dirname, '../../recursive-eco/apps/flow/.env.local'),
];
for (const p of envPaths) {
  if (existsSync(p)) config({ path: p });
}

const AUDIO_DIR = resolve(__dirname, '../grammars/alice-5-minute-stories/audio/librivox');
const CHAPTER_COUNT = 12;

// CLI flags
const args = process.argv.slice(2);
const DRY = args.includes('--dry');
const chapterIdx = args.indexOf('--chapter');
const ONLY_CHAPTER = chapterIdx !== -1 ? parseInt(args[chapterIdx + 1], 10) : null;

function getAudioPath(chNum) {
  const padded = String(chNum).padStart(2, '0');
  return resolve(AUDIO_DIR, `wonderland_ch_${padded}_64kb.mp3`);
}

function getOutputPath(chNum) {
  const padded = String(chNum).padStart(2, '0');
  return resolve(AUDIO_DIR, `whisper-ch${padded}.json`);
}

async function transcribeChapter(openai, chNum) {
  const audioPath = getAudioPath(chNum);
  if (!existsSync(audioPath)) {
    console.error(`  [SKIP] Chapter ${chNum}: file not found at ${audioPath}`);
    return null;
  }

  const sizeMB = (readFileSync(audioPath).length / 1024 / 1024).toFixed(1);
  console.log(`  Chapter ${chNum}: ${sizeMB}MB — sending to Whisper...`);

  const start = Date.now();

  const response = await openai.audio.transcriptions.create({
    file: createReadStream(audioPath),
    model: 'whisper-1',
    response_format: 'verbose_json',
    timestamp_granularities: ['word'],
    language: 'en',
    prompt: 'Alice in Wonderland by Lewis Carroll. Chapter reading from LibriVox.',
  });

  const elapsed = ((Date.now() - start) / 1000).toFixed(1);
  const wordCount = response.words?.length || 0;
  console.log(`  Chapter ${chNum}: ${wordCount} words in ${elapsed}s`);

  return {
    chapter: chNum,
    text: response.text,
    duration: response.duration,
    words: response.words || [],
    language: response.language,
  };
}

async function main() {
  if (!process.env.OPENAI_API_KEY) {
    console.error('ERROR: OPENAI_API_KEY not found in environment');
    process.exit(1);
  }

  const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

  // Determine which chapters to process
  const chapters = ONLY_CHAPTER ? [ONLY_CHAPTER] : Array.from({ length: CHAPTER_COUNT }, (_, i) => i + 1);

  console.log(`Whisper transcription for ${chapters.length} chapter(s)`);
  console.log(`Audio dir: ${AUDIO_DIR}\n`);

  if (DRY) {
    for (const ch of chapters) {
      const path = getAudioPath(ch);
      const exists = existsSync(path);
      const outExists = existsSync(getOutputPath(ch));
      console.log(`  Ch ${ch}: ${exists ? 'found' : 'MISSING'}${outExists ? ' (already transcribed)' : ''}`);
    }
    return;
  }

  const results = {};

  for (const ch of chapters) {
    const outPath = getOutputPath(ch);

    // Skip if already transcribed (use --chapter N to force re-run)
    if (existsSync(outPath) && !ONLY_CHAPTER) {
      console.log(`  Chapter ${ch}: already transcribed, skipping (use --chapter ${ch} to redo)`);
      const existing = JSON.parse(readFileSync(outPath, 'utf8'));
      results[ch] = existing;
      continue;
    }

    try {
      const result = await transcribeChapter(openai, ch);
      if (result) {
        writeFileSync(outPath, JSON.stringify(result, null, 2));
        results[ch] = result;
        console.log(`  → Saved ${outPath}\n`);
      }
    } catch (err) {
      console.error(`  [ERROR] Chapter ${ch}: ${err.message}`);
    }
  }

  // Write combined manifest
  const manifest = {
    generated: new Date().toISOString(),
    source: 'LibriVox dramatic reading (public domain)',
    chapters: {},
  };

  for (const [ch, data] of Object.entries(results)) {
    manifest.chapters[ch] = {
      audio_file: `wonderland_ch_${String(ch).padStart(2, '0')}_64kb.mp3`,
      duration_s: data.duration,
      total_words: data.words.length,
      text: data.text,
      words: data.words.map(w => ({
        word: w.word,
        start: w.start,
        end: w.end,
      })),
    };
  }

  const manifestPath = resolve(AUDIO_DIR, 'whisper-manifest.json');
  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log(`\nManifest: ${manifestPath}`);
  console.log(`Total: ${Object.values(results).reduce((s, r) => s + (r.words?.length || 0), 0)} words across ${Object.keys(results).length} chapters`);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
