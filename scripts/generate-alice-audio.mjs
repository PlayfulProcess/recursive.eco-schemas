/**
 * Generate Alice in Wonderland audiobook with multi-character TTS.
 *
 * Uses ElevenLabs TTS with character-level timestamps for karaoke playback.
 * One audio file per chapter. Timestamps map to the full chapter text so
 * they survive pagination changes.
 *
 * Prerequisites:
 *   1. ELEVENLABS_API_KEY in recursive-eco/.env.local
 *   2. R2 credentials in recursive-eco/.env.local (for audio upload)
 *   3. Voice IDs configured in scripts/voice-config.json
 *
 * Usage:
 *   node scripts/generate-alice-audio.mjs --list-voices      # List available voices
 *   node scripts/generate-alice-audio.mjs --estimate          # Estimate cost (no API calls)
 *   node scripts/generate-alice-audio.mjs --chapter 1         # Generate chapter 1 only
 *   node scripts/generate-alice-audio.mjs --chapter 1 --dry   # Parse + show segments (no TTS)
 *   node scripts/generate-alice-audio.mjs                     # Generate all chapters
 *
 * Output:
 *   - MP3 files uploaded to R2: alice-audio/chapter-XX.mp3
 *   - Audio manifest: grammars/alice-5-minute-stories/audio-manifest.json
 *   - Build log appended: plan/build-logs/alice-audiobook.md
 *
 * Process (for replication with other books):
 *   1. Parse grammar JSON → extract chapter texts
 *   2. Dialogue parser → split into voice-tagged segments
 *   3. ElevenLabs TTS per segment with character-appropriate voice
 *   4. Concatenate MP3 segments, offset timestamps
 *   5. Upload to R2
 *   6. Write manifest with word-level timestamps
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, appendFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { parseChapterDialogue, mergeAdjacentSegments, estimateTTSCharacters, normalizeForTTS } from './lib/dialogue-parser.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Load env vars ──────────────────────────────────────────────────────

function loadEnvFile(envPath) {
  let content;
  try { content = readFileSync(envPath, 'utf8'); } catch { return; }
  for (const line of content.split('\n')) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const eq = t.indexOf('=');
    if (eq === -1) continue;
    const k = t.slice(0, eq).trim();
    const v = t.slice(eq + 1).trim().replace(/^["']|["']$/g, '');
    if (v && !process.env[k]) process.env[k] = v;
  }
}

// Load from recursive-eco (where the API keys live)
const ecoRoot = resolve(__dirname, '../../recursive-eco');
loadEnvFile(resolve(ecoRoot, '.env.local'));
loadEnvFile(resolve(ecoRoot, 'apps/flow/.env.local'));
// Also try local .env.local
loadEnvFile(resolve(__dirname, '../.env.local'));

const ELEVENLABS_KEY = process.env.ELEVENLABS_API_KEY;
const API_BASE = 'https://api.elevenlabs.io/v1';

// ── R2 Client ──────────────────────────────────────────────────────────

let s3;
if (process.env.CLOUDFLARE_ACCOUNT_ID && process.env.R2_ACCESS_KEY_ID) {
  s3 = new S3Client({
    region: 'auto',
    endpoint: `https://${process.env.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com`,
    credentials: {
      accessKeyId: process.env.R2_ACCESS_KEY_ID,
      secretAccessKey: process.env.R2_SECRET_ACCESS_KEY,
    },
  });
}
const R2_BUCKET = process.env.R2_BUCKET_NAME || 'recursive-eco-images';
const R2_BASE = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev';

// ── Paths ──────────────────────────────────────────────────────────────

const grammarPath = resolve(__dirname, '../grammars/alice-in-wonderland-chapter-book/grammar.json');
const voiceConfigPath = resolve(__dirname, 'voice-config.json');
const manifestPath = resolve(__dirname, '../grammars/alice-5-minute-stories/audio-manifest.json');
const buildLogPath = resolve(__dirname, '../plan/build-logs/alice-audiobook.md');

// ── CLI Args ───────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const LIST_VOICES = args.includes('--list-voices');
const ESTIMATE_ONLY = args.includes('--estimate');
const DRY_RUN = args.includes('--dry');
const chapterArg = args.indexOf('--chapter');
const SINGLE_CHAPTER = chapterArg !== -1 ? parseInt(args[chapterArg + 1]) : null;

// ── ElevenLabs API Helpers ─────────────────────────────────────────────

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'xi-api-key': ELEVENLABS_KEY },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`ElevenLabs GET ${path}: ${res.status} — ${body}`);
  }
  return res.json();
}

async function listVoices() {
  // Try v1 endpoint first (more widely supported)
  const res = await fetch(`${API_BASE}/voices`, {
    headers: { 'xi-api-key': ELEVENLABS_KEY },
  });
  if (res.ok) {
    return (await res.json()).voices;
  }
  // Try v2 endpoint
  const res2 = await fetch('https://api.elevenlabs.io/v2/voices?page_size=100', {
    headers: { 'xi-api-key': ELEVENLABS_KEY },
  });
  if (res2.ok) {
    return (await res2.json()).voices;
  }
  const errText = await res.text();
  throw new Error(`Failed to list voices: ${res.status} — ${errText}`);
}

/**
 * Generate TTS with character-level timestamps.
 * Returns { audioBuffer, alignment, duration_s }
 */
async function generateTTS(text, voiceId, voiceSettings, modelId = 'eleven_multilingual_v2') {
  const url = `${API_BASE}/text-to-speech/${voiceId}/with-timestamps`;

  const body = {
    text,
    model_id: modelId,
    voice_settings: {
      stability: voiceSettings.stability ?? 0.5,
      similarity_boost: voiceSettings.similarity_boost ?? 0.75,
      style: voiceSettings.style ?? 0.0,
      speed: voiceSettings.speed ?? 1.0,
    },
    output_format: 'mp3_44100_128',
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'xi-api-key': ELEVENLABS_KEY,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errBody = await res.text();
    throw new Error(`ElevenLabs TTS error (${res.status}): ${errBody}`);
  }

  const data = await res.json();

  // Decode audio
  const audioBuffer = Buffer.from(data.audio_base64, 'base64');

  // Extract alignment (character-level timestamps)
  const alignment = data.alignment || data.normalized_alignment || null;

  // Calculate duration from the last character's end time
  let duration_s = 0;
  if (alignment && alignment.character_end_times_seconds) {
    const endTimes = alignment.character_end_times_seconds;
    duration_s = endTimes[endTimes.length - 1] || 0;
  }

  return { audioBuffer, alignment, duration_s };
}

/**
 * Aggregate character-level timestamps into word-level timestamps.
 * Words are delimited by spaces. Returns array of:
 *   { word, start, end, char_offset_in_segment }
 */
function aggregateToWords(alignment, segmentText) {
  if (!alignment || !alignment.characters) return [];

  const chars = alignment.characters;
  const starts = alignment.character_start_times_seconds;
  const ends = alignment.character_end_times_seconds;

  const words = [];
  let wordStart = null;
  let wordEnd = null;
  let wordChars = '';
  let wordCharOffset = 0;

  for (let i = 0; i < chars.length; i++) {
    const ch = chars[i];
    if (ch === ' ' || ch === '\n' || ch === '\t') {
      // End of word
      if (wordChars.trim()) {
        words.push({
          word: wordChars,
          start: wordStart,
          end: wordEnd,
          char_offset_in_segment: wordCharOffset,
        });
      }
      wordChars = '';
      wordStart = null;
      wordEnd = null;
    } else {
      if (wordStart === null) {
        wordStart = starts[i];
        wordCharOffset = i;
      }
      wordEnd = ends[i];
      wordChars += ch;
    }
  }

  // Last word
  if (wordChars.trim()) {
    words.push({
      word: wordChars,
      start: wordStart,
      end: wordEnd,
      char_offset_in_segment: wordCharOffset,
    });
  }

  return words;
}

// ── Silence / Pause Generation ─────────────────────────────────────────

/**
 * Generate a silent MP3 frame of approximately the given duration.
 * Uses a minimal valid MP3 frame (MPEG1 Layer3, 44100Hz, 128kbps).
 * For precise silence, we generate multiple frames.
 *
 * MP3 frame at 44100Hz/128kbps = 1152 samples = ~26.12ms per frame
 * So for 1 second we need ~38 frames.
 */
function generateSilence(durationSeconds) {
  // Minimal silent MP3 frame (MPEG1, Layer 3, 128kbps, 44100Hz, stereo)
  // Frame header: FF FB 90 00 + padding to 417 bytes (standard frame size for 128kbps/44100Hz)
  const frameSize = 417; // bytes per frame at 128kbps/44100Hz
  const frameDuration = 1152 / 44100; // ~0.02612 seconds
  const numFrames = Math.max(1, Math.round(durationSeconds / frameDuration));

  // Create a silent frame: valid MP3 header + zero audio data
  const frame = Buffer.alloc(frameSize, 0);
  // MP3 sync word + header: MPEG1, Layer III, 128kbps, 44100Hz, Joint Stereo, no padding
  frame[0] = 0xFF;
  frame[1] = 0xFB; // MPEG1, Layer3, no CRC
  frame[2] = 0x90; // 128kbps, 44100Hz
  frame[3] = 0x00; // Joint stereo, no padding, private=0

  // Repeat the frame for the desired duration
  const silenceBuffer = Buffer.alloc(frameSize * numFrames);
  for (let i = 0; i < numFrames; i++) {
    frame.copy(silenceBuffer, i * frameSize);
  }

  return { buffer: silenceBuffer, duration: numFrames * frameDuration };
}

/**
 * Determine pause duration between segments based on context.
 * Longer pauses for paragraph breaks, scene changes, and voice switches.
 * Shorter pauses within rapid dialogue exchanges.
 */
function getPauseDuration(prevSeg, currSeg, cleanText) {
  if (!prevSeg) return 0;

  // Check if there's a paragraph break between segments
  const betweenText = cleanText.slice(prevSeg.charEnd, currSeg.charOffset);
  const hasParagraphBreak = betweenText.includes('\n\n');

  // Voice role change (different character speaking)
  const voiceSwitch = prevSeg.role !== currSeg.role;

  // Dramatic pauses: after exclamations, before new speakers
  const prevEndsExclaim = prevSeg.text.trimEnd().endsWith('!');
  const prevEndsQuestion = prevSeg.text.trimEnd().endsWith('?');

  if (hasParagraphBreak && voiceSwitch) {
    return 1.2; // Scene/paragraph transition + new speaker = longest pause
  }
  if (hasParagraphBreak) {
    return 0.8; // Paragraph break
  }
  if (voiceSwitch) {
    return 0.5; // Speaker change within paragraph
  }
  if (prevEndsExclaim || prevEndsQuestion) {
    return 0.4; // After dramatic punctuation
  }
  return 0.15; // Minimal breath pause between same-voice segments
}

// ── Upload to R2 ───────────────────────────────────────────────────────

async function uploadToR2(key, buffer, contentType = 'audio/mpeg') {
  if (!s3) throw new Error('R2 not configured — missing CLOUDFLARE_ACCOUNT_ID or R2_ACCESS_KEY_ID');

  await s3.send(new PutObjectCommand({
    Bucket: R2_BUCKET,
    Key: key,
    Body: buffer,
    ContentType: contentType,
  }));

  return `${R2_BASE}/${key}`;
}

// ── Grammar Loading ────────────────────────────────────────────────────

function loadChapters() {
  const grammar = JSON.parse(readFileSync(grammarPath, 'utf8'));
  const l1Items = grammar.items.filter(it => it.level === 1);
  const l2Items = grammar.items.filter(it => it.level === 2);

  const chapters = {};
  for (const item of l1Items) {
    const ch = item.metadata.chapter_number;
    if (!chapters[ch]) chapters[ch] = { scenes: [], name: item.metadata.chapter_name };
    chapters[ch].scenes.push(item);
  }
  for (const ch of Object.values(chapters)) {
    ch.scenes.sort((a, b) => a.metadata.scene_number - b.metadata.scene_number);
  }
  // Add chapter names from L2 items
  for (const item of l2Items) {
    const ch = item.metadata.chapter_number;
    if (chapters[ch]) {
      chapters[ch].name = item.metadata.original_title || item.metadata.chapter_name || chapters[ch].name;
    }
  }

  return chapters;
}

function getChapterText(chapter) {
  return chapter.scenes
    .map(s => s.sections['Story (Original Text)'] || '')
    .filter(t => t.trim())
    .join('\n\n');
}

// ── Logging ────────────────────────────────────────────────────────────

function log(msg) {
  const ts = new Date().toISOString().slice(0, 19);
  console.log(`[${ts}] ${msg}`);
}

function logToFile(msg) {
  try {
    appendFileSync(buildLogPath, msg + '\n', 'utf8');
  } catch { /* ignore if build-logs dir doesn't exist */ }
}

// ── Main Flow ──────────────────────────────────────────────────────────

async function main() {
  // ── List voices ──
  if (LIST_VOICES) {
    if (!ELEVENLABS_KEY) {
      console.error('ERROR: ELEVENLABS_API_KEY not found. Set it in recursive-eco/.env.local');
      process.exit(1);
    }
    log('Listing available ElevenLabs voices...');
    const voices = await listVoices();
    console.log(`\nFound ${voices.length} voices:\n`);
    console.log('ID'.padEnd(24) + 'Name'.padEnd(20) + 'Category'.padEnd(12) + 'Labels');
    console.log('-'.repeat(80));
    for (const v of voices) {
      const labels = v.labels ? Object.entries(v.labels).map(([k, val]) => `${k}:${val}`).join(', ') : '';
      console.log(
        (v.voice_id || '').padEnd(24) +
        (v.name || '').padEnd(20) +
        (v.category || '').padEnd(12) +
        labels
      );
    }
    console.log(`\nTo configure voices, edit scripts/voice-config.json and set the voice_id for each role.`);
    console.log(`Then run: node scripts/generate-alice-audio.mjs --chapter 1`);
    return;
  }

  // ── Load grammar ──
  log('Loading Alice grammar...');
  const chapters = loadChapters();
  const chapterNums = Object.keys(chapters).map(Number).sort((a, b) => a - b);

  if (SINGLE_CHAPTER && !chapters[SINGLE_CHAPTER]) {
    console.error(`Chapter ${SINGLE_CHAPTER} not found. Available: ${chapterNums.join(', ')}`);
    process.exit(1);
  }

  const targetChapters = SINGLE_CHAPTER ? [SINGLE_CHAPTER] : chapterNums;

  // ── Load voice config ──
  let voiceConfig;
  try {
    voiceConfig = JSON.parse(readFileSync(voiceConfigPath, 'utf8'));
  } catch {
    console.error('ERROR: Could not read scripts/voice-config.json');
    process.exit(1);
  }

  // ── Estimate mode ──
  if (ESTIMATE_ONLY) {
    log('Estimating TTS character usage...\n');
    let grandTotal = 0;
    for (const chNum of targetChapters) {
      const rawText = getChapterText(chapters[chNum]);
      const { segments, stats } = parseChapterDialogue(rawText);
      const merged = mergeAdjacentSegments(segments);
      const ttsChars = estimateTTSCharacters(merged);
      grandTotal += ttsChars;
      console.log(`  Chapter ${String(chNum).padStart(2)}: ${ttsChars.toLocaleString().padStart(7)} chars | ${merged.length} segments | Characters: ${stats.characters.join(', ')}`);
    }
    console.log(`\n  TOTAL: ${grandTotal.toLocaleString()} characters`);
    console.log(`  Cost (multilingual v2, $0.30/1K): $${(grandTotal / 1000 * 0.30).toFixed(2)}`);
    console.log(`  Cost (flash v2.5, $0.15/1K):      $${(grandTotal / 1000 * 0.15).toFixed(2)}`);
    console.log(`  Cost (turbo v2.5, $0.15/1K):      $${(grandTotal / 1000 * 0.15).toFixed(2)}`);

    // Check ElevenLabs subscription info
    if (ELEVENLABS_KEY) {
      try {
        const sub = await apiGet('/user/subscription');
        console.log(`\n  Your plan: ${sub.tier || 'unknown'}`);
        console.log(`  Characters used: ${(sub.character_count || 0).toLocaleString()} / ${(sub.character_limit || 0).toLocaleString()}`);
        console.log(`  Remaining: ${((sub.character_limit || 0) - (sub.character_count || 0)).toLocaleString()}`);
      } catch (err) {
        console.log(`\n  (Could not fetch subscription info: ${err.message})`);
      }
    }
    return;
  }

  // ── Validate voice config ──
  if (!DRY_RUN) {
    if (!ELEVENLABS_KEY) {
      console.error('ERROR: ELEVENLABS_API_KEY not found.');
      console.error('Add it to recursive-eco/.env.local as: ELEVENLABS_API_KEY=sk_...');
      process.exit(1);
    }

    const missingVoices = Object.entries(voiceConfig.roles)
      .filter(([_, cfg]) => !cfg.voice_id)
      .map(([role]) => role);

    if (missingVoices.length > 0) {
      console.error(`ERROR: Voice IDs not configured for: ${missingVoices.join(', ')}`);
      console.error('\nSteps to configure:');
      console.error('  1. Run: node scripts/generate-alice-audio.mjs --list-voices');
      console.error('  2. Pick voice IDs for each role');
      console.error('  3. Edit scripts/voice-config.json and set voice_id fields');
      process.exit(1);
    }
  }

  // ── Generate audio per chapter ──
  const manifest = {
    generated: new Date().toISOString(),
    model: voiceConfig.model,
    book: 'Alice\'s Adventures in Wonderland',
    author: 'Lewis Carroll',
    voices: {},
    chapters: {},
  };

  // Record voice config in manifest
  for (const [role, cfg] of Object.entries(voiceConfig.roles)) {
    manifest.voices[role] = {
      voice_id: cfg.voice_id,
      voice_name: cfg.voice_name,
      description: cfg.description,
    };
  }

  // Initialize build log
  const logHeader = `\n## Audio Generation Run — ${new Date().toISOString()}\n\n`;
  logToFile(logHeader);

  for (const chNum of targetChapters) {
    const chapter = chapters[chNum];
    const chName = chapter.name;
    log(`\n══ Chapter ${chNum}: ${chName} ══`);

    // Get and parse chapter text
    const rawText = getChapterText(chapter);
    const { cleanText, segments, stats } = parseChapterDialogue(rawText);
    const merged = mergeAdjacentSegments(segments);
    const ttsChars = estimateTTSCharacters(merged);

    log(`  Clean text: ${cleanText.length} chars`);
    log(`  Segments: ${stats.segments} raw → ${merged.length} merged`);
    log(`  Characters: ${stats.characters.join(', ')}`);
    log(`  TTS chars: ${ttsChars.toLocaleString()}`);

    if (DRY_RUN) {
      log('  [DRY RUN] Showing first 15 segments:');
      for (const seg of merged.slice(0, 15)) {
        const preview = seg.text.slice(0, 100).replace(/\n/g, '\\n');
        log(`    [${seg.role}${seg.character ? '/' + seg.character : ''}] ${preview}`);
      }
      log(`  [DRY RUN] Skipping TTS generation.`);
      continue;
    }

    // Generate TTS for each segment, with pauses between them
    const audioChunks = [];
    const wordTimings = [];
    let cumulativeTime = 0;
    let totalPauseTime = 0;

    // Add initial silence (0.5s) before chapter starts
    const { buffer: introSilence, duration: introDur } = generateSilence(0.5);
    audioChunks.push(introSilence);
    cumulativeTime += introDur;
    totalPauseTime += introDur;

    for (let i = 0; i < merged.length; i++) {
      const seg = merged[i];
      const role = seg.role;
      const roleConfig = voiceConfig.roles[role] || voiceConfig.roles.narrator;

      // ── Insert pause between segments ──
      if (i > 0) {
        const pauseDur = getPauseDuration(merged[i - 1], seg, cleanText);
        if (pauseDur > 0) {
          const { buffer: silBuf, duration: silDur } = generateSilence(pauseDur);
          audioChunks.push(silBuf);
          cumulativeTime += silDur;
          totalPauseTime += silDur;
        }
      }

      // Clean the segment text for TTS
      let ttsText = seg.text;
      // Remove leading/trailing quotes for dialogue (voice actor shouldn't say "quote mark")
      if (role !== 'narrator') {
        ttsText = ttsText.replace(/^"/, '').replace(/"$/, '');
      }
      // Skip empty segments
      if (!ttsText.trim()) continue;

      const voiceId = roleConfig.voice_id;
      const settings = roleConfig.settings;

      log(`  Segment ${i + 1}/${merged.length} [${role}${seg.character ? '/' + seg.character : ''}] (${ttsText.length} chars)...`);

      try {
        const { audioBuffer, alignment, duration_s } = await generateTTS(
          ttsText, voiceId, settings, voiceConfig.model
        );

        audioChunks.push(audioBuffer);

        // Aggregate to word-level timestamps with offsets
        const segWords = aggregateToWords(alignment, ttsText);
        for (const w of segWords) {
          wordTimings.push({
            word: w.word,
            start: w.start + cumulativeTime,
            end: w.end + cumulativeTime,
            char_offset: seg.charOffset + w.char_offset_in_segment,
            voice: role,
            character: seg.character,
          });
        }

        cumulativeTime += duration_s;
        log(`    → ${duration_s.toFixed(2)}s audio, ${segWords.length} words`);

        // Rate limiting: small delay between requests
        if (i < merged.length - 1) {
          await new Promise(r => setTimeout(r, 200));
        }
      } catch (err) {
        log(`    ERROR: ${err.message}`);
        logToFile(`  - **FAILURE** Chapter ${chNum}, segment ${i + 1} [${role}]: ${err.message}`);

        // If rate limited, wait and retry once
        if (err.message.includes('429') || err.message.includes('rate')) {
          log(`    Waiting 30s for rate limit...`);
          await new Promise(r => setTimeout(r, 30000));
          try {
            const { audioBuffer, alignment, duration_s } = await generateTTS(
              ttsText, roleConfig.voice_id, settings, voiceConfig.model
            );
            audioChunks.push(audioBuffer);
            const segWords = aggregateToWords(alignment, ttsText);
            for (const w of segWords) {
              wordTimings.push({
                word: w.word,
                start: w.start + cumulativeTime,
                end: w.end + cumulativeTime,
                char_offset: seg.charOffset + w.char_offset_in_segment,
                voice: role,
                character: seg.character,
              });
            }
            cumulativeTime += duration_s;
            log(`    → RETRY OK: ${duration_s.toFixed(2)}s`);
          } catch (retryErr) {
            log(`    RETRY FAILED: ${retryErr.message}`);
            logToFile(`  - **RETRY FAILURE** Chapter ${chNum}, segment ${i + 1}: ${retryErr.message}`);
          }
        }
      }
    }

    // Add trailing silence (1s) after chapter ends
    const { buffer: outroSilence, duration: outroDur } = generateSilence(1.0);
    audioChunks.push(outroSilence);
    cumulativeTime += outroDur;
    totalPauseTime += outroDur;
    log(`  Total pause time inserted: ${totalPauseTime.toFixed(1)}s`);

    // Concatenate all audio chunks into one chapter MP3
    const chapterAudio = Buffer.concat(audioChunks);
    const chapterDuration = cumulativeTime;

    log(`  Chapter ${chNum} total: ${chapterDuration.toFixed(1)}s, ${(chapterAudio.length / 1024 / 1024).toFixed(1)}MB, ${wordTimings.length} words`);

    // Always save locally first
    const localPath = resolve(__dirname, `../grammars/alice-5-minute-stories/audio/chapter-${String(chNum).padStart(2, '0')}.mp3`);
    mkdirSync(dirname(localPath), { recursive: true });
    writeFileSync(localPath, chapterAudio);
    log(`  Saved locally: ${localPath}`);

    // Upload to R2
    const r2Key = `alice-audio/chapter-${String(chNum).padStart(2, '0')}.mp3`;
    let audioUrl = `audio/chapter-${String(chNum).padStart(2, '0')}.mp3`;
    try {
      audioUrl = await uploadToR2(r2Key, chapterAudio);
      log(`  Uploaded: ${audioUrl}`);
    } catch (err) {
      log(`  R2 upload failed (local copy saved): ${err.message}`);
    }

    // Add to manifest
    manifest.chapters[chNum] = {
      name: chName,
      audio_url: audioUrl,
      duration_s: Math.round(chapterDuration * 100) / 100,
      total_words: wordTimings.length,
      clean_text: cleanText,
      words: wordTimings,
    };

    // Log success
    logToFile(`- Chapter ${chNum} "${chName}": ${chapterDuration.toFixed(1)}s, ${wordTimings.length} words, ${ttsChars} TTS chars — OK`);
  }

  // Write manifest
  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  log(`\nManifest written: ${manifestPath}`);
  log(`Total chapters: ${Object.keys(manifest.chapters).length}`);

  const totalDuration = Object.values(manifest.chapters).reduce((sum, ch) => sum + ch.duration_s, 0);
  const totalWords = Object.values(manifest.chapters).reduce((sum, ch) => sum + ch.total_words, 0);
  log(`Total duration: ${Math.floor(totalDuration / 60)}m ${Math.round(totalDuration % 60)}s`);
  log(`Total words: ${totalWords.toLocaleString()}`);

  logToFile(`\n**Total**: ${Math.floor(totalDuration / 60)}m ${Math.round(totalDuration % 60)}s, ${totalWords} words\n`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
