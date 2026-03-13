/**
 * Align Whisper word timestamps to booklet page text for karaoke highlighting.
 *
 * Strategy:
 * 1. Read Whisper transcript (word-level timestamps from LibriVox audio)
 * 2. Read the booklet HTML to extract per-page text
 * 3. Use fuzzy word-by-word alignment (spoken words ↔ displayed words)
 * 4. Output a karaoke manifest: for each page, the word timings
 *
 * The LibriVox recordings have intro/outro ("This is a LibriVox recording...")
 * that we need to skip. We detect where Carroll's actual text begins.
 *
 * Usage:
 *   node scripts/align-whisper-to-pages.mjs                # All chapters
 *   node scripts/align-whisper-to-pages.mjs --chapter 1    # Just chapter 1
 *
 * Output: grammars/alice-5-minute-stories/audio/librivox/karaoke-manifest.json
 */
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const AUDIO_DIR = resolve(__dirname, '../grammars/alice-5-minute-stories/audio/librivox');
const BOOKLET_DIR = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets');

const args = process.argv.slice(2);
const chapterIdx = args.indexOf('--chapter');
const ONLY_CHAPTER = chapterIdx !== -1 ? parseInt(args[chapterIdx + 1], 10) : null;
const VERBOSE = args.includes('--verbose');

/**
 * Normalize a word for comparison: lowercase, strip punctuation, collapse spaces.
 */
function normalizeWord(w) {
  return w.toLowerCase().replace(/[^a-z0-9']/g, '').trim();
}

/**
 * Extract per-page text from booklet HTML.
 * Each page is a <div class="text-block"> containing <p> elements.
 * Returns array of { pageNum, text, words[] } where words[] are the display words in order.
 */
function extractPagesFromHtml(htmlPath) {
  const html = readFileSync(htmlPath, 'utf8');
  const pages = [];

  // Match each page-right with its data-page and text-block content
  const pageRegex = /<div class="page-right"[^>]*data-page="(\d+)"[^>]*>\s*<div class="text-block">([\s\S]*?)<\/div>\s*<div class="page-number/g;
  let match;
  while ((match = pageRegex.exec(html)) !== null) {
    const pageNum = parseInt(match[1], 10);
    const blockHtml = match[2];

    // Strip HTML tags, decode entities
    let text = blockHtml
      .replace(/<br\s*\/?>/gi, ' ')
      .replace(/<\/?p[^>]*>/gi, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#?\w+;/g, '')
      .replace(/\s+/g, ' ')
      .trim();

    // Split into words
    const words = text.split(/\s+/).filter(w => w.length > 0);

    pages.push({ pageNum, text, words });
  }

  return pages;
}

/**
 * Find where the story text actually begins in the Whisper transcript.
 * LibriVox recordings start with "This is a LibriVox recording..." intro.
 * We look for "Alice" as first story word (Chapter 1) or the chapter title words.
 */
function findStoryStart(whisperWords, firstPageWords) {
  // Normalize first few page words for matching
  const target = firstPageWords.slice(0, 6).map(normalizeWord);

  // Search through whisper words for a sequence matching first page words
  for (let i = 0; i < Math.min(whisperWords.length, 200); i++) {
    let matches = 0;
    for (let j = 0; j < target.length && (i + j) < whisperWords.length; j++) {
      const wWord = normalizeWord(whisperWords[i + j].word);
      if (wWord === target[j]) {
        matches++;
      } else {
        break;
      }
    }
    if (matches >= Math.min(4, target.length)) {
      return i;
    }
  }

  // Fallback: search for "chapter" or chapter-specific first word
  for (let i = 0; i < Math.min(whisperWords.length, 200); i++) {
    const w = normalizeWord(whisperWords[i].word);
    if (w === 'chapter' || w === target[0]) {
      // Check if next words match
      let matches = 0;
      const searchStart = w === 'chapter' ? i + 3 : i; // skip "Chapter N Title"
      for (let j = 0; j < target.length && (searchStart + j) < whisperWords.length; j++) {
        if (normalizeWord(whisperWords[searchStart + j].word) === target[j]) matches++;
        else break;
      }
      if (matches >= 3) return searchStart;
    }
  }

  return 0; // fallback: start from beginning
}

/**
 * Find where the story text ends in the Whisper transcript.
 * LibriVox recordings end with "End of chapter N" or reader credits.
 */
function findStoryEnd(whisperWords) {
  for (let i = whisperWords.length - 1; i >= Math.max(0, whisperWords.length - 50); i--) {
    const w = normalizeWord(whisperWords[i].word);
    if (w === 'end' && i + 2 < whisperWords.length) {
      const next = normalizeWord(whisperWords[i + 1].word);
      if (next === 'of') return i;
    }
    if (w === 'read' && i + 1 < whisperWords.length) {
      const next = normalizeWord(whisperWords[i + 1].word);
      if (next === 'by') return i;
    }
  }
  return whisperWords.length;
}

/**
 * Check if two words match (exact or fuzzy).
 */
function wordsMatch(a, b) {
  if (a === b) return true;
  // Prefix match for partial words (e.g., "conversation" vs "conversations")
  if (a.length > 3 && b.length > 3) {
    if (a.startsWith(b) || b.startsWith(a)) return true;
  }
  return false;
}

/**
 * Align whisper words to page words using dynamic programming (Needleman-Wunsch).
 *
 * Instead of greedy forward-matching (which cascades on one bad match),
 * DP finds the globally optimal alignment. This correctly handles:
 * - Whisper missing a word ("she peeped" vs book's "she had peeped")
 * - Contractions ("what's" vs "what is")
 * - Extra/missing words on either side
 */
function alignWordsToPages(whisperWords, pages, storyStart, storyEnd) {
  const storyWords = whisperWords.slice(storyStart, storyEnd);
  const result = [];
  let wIdx = 0; // current position in storyWords

  for (const page of pages) {
    const pageResult = {
      pageNum: page.pageNum,
      words: [],
      startTime: null,
      endTime: null,
    };

    const pageNorm = page.words.map(w => normalizeWord(w)).filter(w => w.length > 0);
    const n = pageNorm.length;

    // Find the whisper window for this page: take enough words to cover the page
    // plus margin for skips. Use a generous window (3x page words or 500, whichever smaller)
    const windowSize = Math.min(n * 3, 500, storyWords.length - wIdx);
    const wSlice = storyWords.slice(wIdx, wIdx + windowSize);
    const m = wSlice.length;

    if (n === 0 || m === 0) {
      result.push(pageResult);
      continue;
    }

    // DP alignment: score[i][j] = best score aligning pageNorm[0..i-1] with wSlice[0..j-1]
    const MATCH = 3;
    const SKIP_WHISPER = -1; // skip a whisper word
    const SKIP_PAGE = -2;   // skip a page word (worse — we want all page words matched)

    // Use 1D arrays for memory efficiency
    const prev = new Float32Array(m + 1);
    const curr = new Float32Array(m + 1);
    const trace = new Uint8Array((n + 1) * (m + 1)); // 0=diag, 1=left(skip whisper), 2=up(skip page)

    // Initialize first row (skip whisper words for free at start)
    for (let j = 0; j <= m; j++) prev[j] = 0;

    // Fill DP table
    for (let i = 1; i <= n; i++) {
      curr[0] = i * SKIP_PAGE;
      for (let j = 1; j <= m; j++) {
        const matched = wordsMatch(pageNorm[i - 1], normalizeWord(wSlice[j - 1].word));
        const diagScore = prev[j - 1] + (matched ? MATCH : -5);
        const leftScore = curr[j - 1] + SKIP_WHISPER;
        const upScore = prev[j] + SKIP_PAGE;

        if (diagScore >= leftScore && diagScore >= upScore) {
          curr[j] = diagScore;
          trace[i * (m + 1) + j] = 0; // diagonal
        } else if (leftScore >= upScore) {
          curr[j] = leftScore;
          trace[i * (m + 1) + j] = 1; // skip whisper
        } else {
          curr[j] = upScore;
          trace[i * (m + 1) + j] = 2; // skip page
        }
      }
      // Copy curr to prev
      for (let j = 0; j <= m; j++) prev[j] = curr[j];
    }

    // Find best endpoint (allow trailing unmatched whisper words)
    let bestJ = 0;
    let bestScore = -Infinity;
    for (let j = 0; j <= m; j++) {
      if (prev[j] >= bestScore) {
        bestScore = prev[j];
        bestJ = j;
      }
    }

    // Traceback to find the alignment
    const alignment = []; // [{pageIdx, whisperIdx}] where whisperIdx=-1 means unmatched
    let ti = n, tj = bestJ;
    while (ti > 0) {
      const t = trace[ti * (m + 1) + tj];
      if (t === 0) { // diagonal
        const matched = wordsMatch(pageNorm[ti - 1], normalizeWord(wSlice[tj - 1].word));
        alignment.push({ pageIdx: ti - 1, whisperIdx: matched ? tj - 1 : -1 });
        ti--; tj--;
      } else if (t === 1) { // skip whisper word
        tj--;
      } else { // skip page word
        alignment.push({ pageIdx: ti - 1, whisperIdx: -1 });
        ti--;
      }
    }
    alignment.reverse();

    // Build page result from alignment
    let lastWhisperIdx = -1;
    for (const a of alignment) {
      if (a.whisperIdx >= 0) {
        const w = wSlice[a.whisperIdx];
        pageResult.words.push({
          display: page.words[a.pageIdx] || pageNorm[a.pageIdx],
          start: w.start,
          end: w.end,
        });
        if (pageResult.startTime === null) pageResult.startTime = w.start;
        pageResult.endTime = w.end;
        lastWhisperIdx = a.whisperIdx;
      } else {
        // Unmatched page word — will be interpolated below
        pageResult.words.push({
          display: page.words[a.pageIdx] || pageNorm[a.pageIdx],
          start: -1,
          end: -1,
        });
      }
    }

    // Advance wIdx past the matched whisper words
    if (lastWhisperIdx >= 0) wIdx += lastWhisperIdx + 1;

    // Interpolate unmatched words between matched anchors
    for (let i = 0; i < pageResult.words.length; i++) {
      if (pageResult.words[i].start >= 0) continue; // already matched

      // Find previous and next matched words
      let prevIdx = i - 1;
      while (prevIdx >= 0 && pageResult.words[prevIdx].start < 0) prevIdx--;
      let nextIdx = i + 1;
      while (nextIdx < pageResult.words.length && pageResult.words[nextIdx].start < 0) nextIdx++;

      const prevTime = prevIdx >= 0 ? pageResult.words[prevIdx].end : (pageResult.startTime || 0);
      const nextTime = nextIdx < pageResult.words.length ? pageResult.words[nextIdx].start : prevTime + 0.3;
      const gapCount = nextIdx - prevIdx - 1;
      const rank = i - prevIdx;
      const perWord = gapCount > 0 ? (nextTime - prevTime) / (gapCount + 1) : 0.3;

      pageResult.words[i].start = prevTime + rank * perWord;
      pageResult.words[i].end = prevTime + (rank + 1) * perWord;

      if (pageResult.startTime === null) pageResult.startTime = pageResult.words[i].start;
      pageResult.endTime = pageResult.words[i].end;
    }

    // ── Fix non-monotonic timestamps ──
    // The greedy aligner can create backward jumps when interpolated words
    // overshoot the actual audio position. Fix by:
    // 1. Identify backward jumps
    // 2. Redistribute interpolated sections between surrounding real matches
    if (pageResult.words.length > 1) {
      // Pass 1: find and fix backward jumps by redistributing
      for (let i = 1; i < pageResult.words.length; i++) {
        if (pageResult.words[i].start < pageResult.words[i - 1].start) {
          // Backward jump — find the start of the interpolated run
          // (interpolated words have duration ~0.3s)
          let runStart = i - 1;
          while (runStart > 0) {
            const dur = pageResult.words[runStart].end - pageResult.words[runStart].start;
            if (Math.abs(dur - 0.3) < 0.02) {
              runStart--;
            } else {
              break;
            }
          }
          // runStart = last real matched word before the interpolated run
          // i = next real matched word (with backward timestamp)
          const anchorEnd = pageResult.words[runStart].end;
          const targetStart = pageResult.words[i].start;
          const count = i - runStart - 1;

          if (count > 0 && targetStart > anchorEnd) {
            // Redistribute interpolated words between anchorEnd and targetStart
            const perWord = (targetStart - anchorEnd) / count;
            for (let j = runStart + 1; j < i; j++) {
              pageResult.words[j].start = anchorEnd + (j - runStart - 1) * perWord;
              pageResult.words[j].end = pageResult.words[j].start + perWord;
            }
          }
        }
      }

      // Pass 2: enforce strict monotonic increase (safety net)
      for (let i = 1; i < pageResult.words.length; i++) {
        const prev = pageResult.words[i - 1];
        const curr = pageResult.words[i];
        if (curr.start < prev.end) {
          curr.start = prev.end + 0.02;
        }
        if (curr.end <= curr.start) {
          curr.end = curr.start + 0.15;
        }
      }

      // Recompute page time boundaries
      pageResult.startTime = pageResult.words[0].start;
      pageResult.endTime = pageResult.words[pageResult.words.length - 1].end;
    }

    // Compute page time boundaries
    if (pageResult.words.length > 0 && pageResult.startTime !== null) {
      result.push(pageResult);
    }
  }

  return result;
}

/**
 * Process one chapter: read whisper JSON + booklet HTML → aligned karaoke data.
 */
function processChapter(chNum) {
  const padded = String(chNum).padStart(2, '0');
  const whisperPath = resolve(AUDIO_DIR, `whisper-ch${padded}.json`);

  // Find the booklet HTML file
  const bookletFiles = readdirSync(BOOKLET_DIR)
    .filter(f => f.startsWith(`chapter${padded}`) && f.endsWith('.html'));

  if (!existsSync(whisperPath)) {
    console.error(`  [SKIP] Chapter ${chNum}: no whisper transcript`);
    return null;
  }
  if (bookletFiles.length === 0) {
    console.error(`  [SKIP] Chapter ${chNum}: no booklet HTML`);
    return null;
  }

  const whisperData = JSON.parse(readFileSync(whisperPath, 'utf8'));
  const bookletPath = resolve(BOOKLET_DIR, bookletFiles[0]);
  const pages = extractPagesFromHtml(bookletPath);

  if (pages.length === 0) {
    console.error(`  [SKIP] Chapter ${chNum}: no pages extracted from HTML`);
    return null;
  }

  console.log(`  Chapter ${chNum}: ${whisperData.words.length} whisper words, ${pages.length} pages`);

  // Find story boundaries (skip LibriVox intro/outro)
  const storyStart = findStoryStart(whisperData.words, pages[0].words);
  const storyEnd = findStoryEnd(whisperData.words);

  if (VERBOSE) {
    console.log(`    Story starts at whisper word ${storyStart}: "${whisperData.words[storyStart]?.word}"`);
    console.log(`    Story ends at whisper word ${storyEnd}: "${whisperData.words[Math.max(0, storyEnd - 1)]?.word}"`);
    console.log(`    Story range: ${storyEnd - storyStart} words`);
  }

  // Align
  const aligned = alignWordsToPages(whisperData.words, pages, storyStart, storyEnd);

  // Stats
  const totalAligned = aligned.reduce((s, p) => s + p.words.length, 0);
  const totalPageWords = pages.reduce((s, p) => s + p.words.length, 0);
  const pct = totalPageWords > 0 ? ((totalAligned / totalPageWords) * 100).toFixed(1) : '0';
  console.log(`    Aligned: ${totalAligned}/${totalPageWords} words (${pct}%)`);

  if (VERBOSE) {
    for (const p of aligned) {
      const first = p.words[0];
      const last = p.words[p.words.length - 1];
      console.log(`    Page ${p.pageNum}: ${p.words.length} words, ${first?.start?.toFixed(1)}s – ${last?.end?.toFixed(1)}s`);
    }
  }

  return {
    chapter: chNum,
    audio_file: `wonderland_ch_${padded}_64kb.mp3`,
    duration_s: whisperData.duration,
    pages: aligned,
  };
}

// ── Main ─────────────────────────────────────────────────────────────

const chapters = ONLY_CHAPTER
  ? [ONLY_CHAPTER]
  : Array.from({ length: 12 }, (_, i) => i + 1);

console.log(`Aligning Whisper transcripts to booklet pages for ${chapters.length} chapter(s)\n`);

const manifest = {
  generated: new Date().toISOString(),
  source: 'LibriVox dramatic reading aligned to booklet pages',
  chapters: {},
};

for (const ch of chapters) {
  const result = processChapter(ch);
  if (result) {
    manifest.chapters[ch] = result;
  }
}

const outPath = resolve(AUDIO_DIR, 'karaoke-manifest.json');
writeFileSync(outPath, JSON.stringify(manifest, null, 2));

const totalWords = Object.values(manifest.chapters)
  .reduce((s, c) => s + c.pages.reduce((ps, p) => ps + p.words.length, 0), 0);
console.log(`\nKaraoke manifest: ${outPath}`);
console.log(`Total: ${totalWords} aligned words across ${Object.keys(manifest.chapters).length} chapters`);
