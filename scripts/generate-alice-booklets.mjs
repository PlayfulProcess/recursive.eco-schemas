/**
 * Generate printable HTML booklets from the alice-in-wonderland-chapter-book grammar.
 *
 * One booklet per chapter. Scene-aware illustration assignment ensures
 * each illustration appears next to its matching text passage.
 *
 * Features:
 *   --lowercase  Generate in normal case (default is ALL CAPS)
 *   --remap      Use illustration-assignments.json for custom illustration placement
 *   Dialogue formatted on separate lines for readability
 *   Carroll's original paragraph breaks preserved
 *   5-tier font sizing, never scrollable
 *
 * Usage:
 *   node scripts/generate-alice-booklets.mjs              # ALL CAPS
 *   node scripts/generate-alice-booklets.mjs --lowercase   # Normal case
 *   node scripts/generate-alice-booklets.mjs --remap       # Use custom illustration assignments
 *
 * Output: grammars/alice-5-minute-stories/booklets/
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const grammarPath = resolve(__dirname, '../grammars/alice-in-wonderland-chapter-book/grammar.json');
const outputDir = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets');

mkdirSync(outputDir, { recursive: true });

const grammar = JSON.parse(readFileSync(grammarPath, 'utf8'));

// CLI flags
const USE_CAPS = !process.argv.includes('--lowercase');
const USE_REMAP = process.argv.includes('--remap');
const MAX_CHARS_PER_PAGE = 1200;

// ── Remap: load user-edited illustration assignments ────────────────
let remapData = null;
if (USE_REMAP) {
  const remapPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-assignments.json');
  if (existsSync(remapPath)) {
    remapData = JSON.parse(readFileSync(remapPath, 'utf8'));
    console.log(`--remap: loaded ${remapData.length} illustration assignments`);
  } else {
    console.error('--remap: illustration-assignments.json not found! Run without --remap first.');
    process.exit(1);
  }
}

/**
 * Apply user's illustration remapping to a chapter's pages.
 * Overrides coverImage and page illustrations with the user's assignments.
 */
function applyRemap(chNum, coverImage, pages) {
  if (!remapData) return { coverImage, pages };

  const chapterAssignments = remapData.filter(a => a.chapter === chNum);

  // Find cover override (page 0)
  const coverAssign = chapterAssignments.find(a => a.page === 0);
  if (coverAssign && coverAssign.image_url) {
    coverImage = coverAssign.image_url;
  }

  // Override each content page's illustration
  for (const assign of chapterAssignments) {
    if (assign.page === 0) continue; // skip cover
    const pageIdx = assign.page - 1; // page 1 → index 0
    if (pageIdx >= 0 && pageIdx < pages.length) {
      if (assign.image_url) {
        // Replace or add illustration
        pages[pageIdx].illustration = {
          url: assign.image_url,
          scene: assign.image_info || '',
          artist: '',
        };
      } else {
        // Empty URL = text-only (remove illustration)
        pages[pageIdx].illustration = null;
      }
    }
  }

  return { coverImage, pages };
}

// ── Helpers ──────────────────────────────────────────────────────────

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/**
 * Transform text case. In CAPS mode, uppercase everything and strip markdown emphasis.
 * In lowercase mode, just strip markdown emphasis and clean whitespace.
 */
function transformCase(text) {
  // Always keep original case — CSS text-transform handles display
  let t = text
    .replace(/_([^_]+)_/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  return t;
}

/**
 * Format text as HTML with:
 * - Carroll's original paragraph breaks preserved (\n\n → separate <p>)
 * - Dialogue on separate lines (opening quote gets a line break before it)
 * - Single \n within paragraphs → spaces
 */
function formatTextAsHtml(text) {
  // Split on original paragraph breaks
  const paragraphs = text.split(/\n\n+/).filter(p => p.trim());

  return paragraphs.map(p => {
    // Collapse single newlines to spaces (Gutenberg line wrapping)
    let cleaned = p.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();

    // No dialogue line breaks — let text flow as a solid justified block
    return `<p>${escapeHtml(cleaned)}</p>`;
  }).join('\n          ');
}

// ── Sentence Splitter ────────────────────────────────────────────────

const ABBREVIATIONS = new Set([
  'mr', 'mrs', 'ms', 'dr', 'st', 'sr', 'jr', 'vs', 'etc', 'vol',
  'fig', 'no', 'ch',
]);

// Dialogue attribution verbs — don't break between a closing quote and these
const ATTRIBUTION_VERBS = new Set([
  'said', 'thought', 'cried', 'asked', 'replied', 'exclaimed', 'remarked',
  'whispered', 'shouted', 'continued', 'added', 'muttered', 'began',
  'answered', 'observed', 'repeated', 'returned', 'suggested', 'grumbled',
  'growled', 'sighed', 'sobbed', 'shrieked', 'screamed', 'panted',
  'interrupted', 'went', 'called', 'sang', 'recited', 'read', 'roared',
]);

/**
 * Split text into sentences. Breaks only at sentence-ending punctuation
 * followed by whitespace + uppercase letter or paragraph boundary.
 * Keeps dialogue attributions with their quotes ("Well!" thought Alice).
 */
function splitIntoSentences(text) {
  const normalized = text.replace(/\r\n/g, '\n').trim();
  const sentences = [];
  let current = '';
  let i = 0;

  while (i < normalized.length) {
    current += normalized[i];

    if ('.!?'.includes(normalized[i])) {
      let j = i + 1;
      // Consume closing quotes/parens after punctuation
      while (j < normalized.length && '"\u201d\u201c\'\u2019)'.includes(normalized[j])) {
        current += normalized[j];
        j++;
      }

      if (j >= normalized.length) {
        sentences.push(current.trim());
        current = '';
        i = j;
        continue;
      }

      if (/[\s\n]/.test(normalized[j])) {
        let k = j;
        while (k < normalized.length && /[\s\n]/.test(normalized[k])) k++;

        // Check if next char signals new sentence (uppercase, opening quote, paragraph break)
        const hasParaBreak = normalized.slice(j, k).includes('\n\n');
        if (k >= normalized.length || hasParaBreak || /[A-Z\u201c"(]/.test(normalized[k])) {
          const match = current.match(/\b(\w+)[.!?][\u201d"'\u2019)]*$/);
          const word = match ? match[1].toLowerCase() : '';
          if (!ABBREVIATIONS.has(word)) {
            // Check if next word is a dialogue attribution verb
            // e.g. "Well!" THOUGHT Alice → don't break here
            const nextWordMatch = normalized.slice(k).match(/^([a-zA-Z]+)/);
            const nextWord = nextWordMatch ? nextWordMatch[1].toLowerCase() : '';
            if (!ATTRIBUTION_VERBS.has(nextWord)) {
              sentences.push(current.trim());
              current = '';
              i = j;
              continue;
            }
          }
        }
      }
      i = j;
      continue;
    }
    i++;
  }
  if (current.trim()) sentences.push(current.trim());
  return sentences;
}

/**
 * Split text into pages at sentence boundaries, targeting ~targetChars per page.
 * Preserves Carroll's original paragraph breaks (\n\n) so formatTextAsHtml can
 * correctly create separate <p> elements.
 */
function splitTextIntoPages(text, targetChars) {
  const sentences = splitIntoSentences(text);
  if (sentences.length === 0) return [''];

  // Detect which sentences start a new paragraph in the original text
  const paraStarts = new Set();
  let searchPos = 0;
  for (let si = 0; si < sentences.length; si++) {
    // Find this sentence in the original text
    const snippet = sentences[si].substring(0, Math.min(30, sentences[si].length));
    const idx = text.indexOf(snippet, searchPos);
    if (idx > searchPos && si > 0) {
      const between = text.slice(searchPos, idx);
      if (/\n\s*\n/.test(between)) {
        paraStarts.add(si);
      }
    }
    if (idx >= 0) searchPos = idx + sentences[si].length;
  }

  const pages = [];
  let currentPage = '';

  for (let si = 0; si < sentences.length; si++) {
    const sentence = sentences[si];
    const joiner = currentPage ? (paraStarts.has(si) ? '\n\n' : ' ') : '';
    const wouldBe = currentPage.length + joiner.length + sentence.length;

    if (wouldBe > targetChars * 1.3 && currentPage.length > targetChars * 0.4) {
      pages.push(currentPage.trim());
      currentPage = sentence;
    } else {
      currentPage = currentPage + joiner + sentence;
    }
  }
  if (currentPage.trim()) pages.push(currentPage.trim());
  return pages;
}

// ── Grammar Processing ───────────────────────────────────────────────

const l1Items = grammar.items.filter(item => item.level === 1);
const l2Items = grammar.items.filter(item => item.level === 2);

const chapterMap = {};
for (const scene of l1Items) {
  const chNum = scene.metadata.chapter_number;
  if (!chapterMap[chNum]) chapterMap[chNum] = { scenes: [], l2: null };
  chapterMap[chNum].scenes.push(scene);
}
for (const ch of l2Items) {
  const chNum = ch.metadata.chapter_number;
  if (chapterMap[chNum]) chapterMap[chNum].l2 = ch;
}
for (const ch of Object.values(chapterMap)) {
  ch.scenes.sort((a, b) => a.metadata.scene_number - b.metadata.scene_number);
}

/**
 * Get unique illustrations for a scene (excluding already-used URLs).
 */
function getSceneIllustrations(scene, usedUrls) {
  const ills = [];
  for (const ill of (scene.metadata?.illustrations || [])) {
    if (!usedUrls.has(ill.url)) {
      ills.push(ill);
      usedUrls.add(ill.url);
    }
  }
  return ills;
}

/**
 * Build all pages for a chapter using SCENE-AWARE illustration assignment.
 *
 * Each scene's illustrations stay matched to that scene's text.
 * Text is split at sentence boundaries targeting the global chars/page.
 * Illustrations are placed at the CENTER of their zone (not forced to page 0)
 * so images appear where the key action happens, not at the scene setup.
 * Leftover illustrations from short scenes go to a bonus pool for text-only pages.
 */
function buildChapterPages(chapter) {
  const l2 = chapter.l2;
  const coverImage = l2?.image_url || chapter.scenes[0]?.image_url || '';
  const usedUrls = new Set([coverImage]);

  // Calculate total text and total illustrations to find target chars/page
  let totalChars = 0;
  let totalIlls = 0;
  for (const scene of chapter.scenes) {
    const text = scene.sections['Story (Original Text)'] || '';
    totalChars += text.length;
    const ills = (scene.metadata?.illustrations || []).filter(ill => ill.url !== coverImage);
    totalIlls += ills.length;
  }
  // Add L2 non-primary illustrations
  const l2Extras = (l2?.metadata?.illustrations || []).filter(ill => !ill.is_primary && ill.url !== coverImage);
  totalIlls += l2Extras.length;

  let targetChars = totalIlls > 0 ? Math.ceil(totalChars / totalIlls) : totalChars;
  if (targetChars > MAX_CHARS_PER_PAGE) targetChars = MAX_CHARS_PER_PAGE;

  // Process each scene: split text, assign that scene's illustrations
  const pages = [];
  const bonusPool = []; // leftover illustrations from scenes with more ills than pages

  for (const scene of chapter.scenes) {
    const rawText = scene.sections['Story (Original Text)'] || '';
    if (!rawText.trim()) continue;

    const text = transformCase(rawText);
    const sceneIlls = getSceneIllustrations(scene, usedUrls);

    // Split scene text into pages
    const textPages = splitTextIntoPages(text, targetChars);

    if (sceneIlls.length >= textPages.length) {
      // More illustrations than text pages — use one per page, save extras to bonus pool
      for (let i = 0; i < textPages.length; i++) {
        pages.push({ text: textPages[i], illustration: sceneIlls[i] });
      }
      // Save extra illustrations for text-only pages elsewhere in the chapter
      for (let i = textPages.length; i < sceneIlls.length; i++) {
        bonusPool.push(sceneIlls[i]);
      }
    } else {
      // More text pages than illustrations — place ills at CENTER of each zone
      // This ensures illustrations appear where the action peaks, not at scene setup
      const stride = textPages.length / sceneIlls.length;
      const illPositions = [];
      for (let j = 0; j < sceneIlls.length; j++) {
        const zoneStart = Math.round(j * stride);
        const zoneEnd = Math.round((j + 1) * stride) - 1;
        illPositions.push(Math.round((zoneStart + zoneEnd) / 2));
      }

      let illIdx = 0;
      for (let i = 0; i < textPages.length; i++) {
        if (illIdx < illPositions.length && i === illPositions[illIdx]) {
          pages.push({ text: textPages[i], illustration: sceneIlls[illIdx] });
          illIdx++;
        } else {
          pages.push({ text: textPages[i], illustration: null });
        }
      }
    }
  }

  // Add L2 non-primary illustrations to the bonus pool
  for (const ill of l2Extras) {
    if (!usedUrls.has(ill.url)) {
      bonusPool.push(ill);
      usedUrls.add(ill.url);
    }
  }

  // Distribute bonus pool illustrations to text-only pages
  let bonusIdx = 0;
  for (let i = 0; i < pages.length && bonusIdx < bonusPool.length; i++) {
    if (!pages[i].illustration && pages[i].text) {
      pages[i].illustration = bonusPool[bonusIdx];
      bonusIdx++;
    }
  }

  return {
    coverImage,
    pages,
    illCount: pages.filter(p => p.illustration).length,
    textOnlyCount: pages.filter(p => !p.illustration).length,
  };
}

// ── HTML Generation ──────────────────────────────────────────────────

function generateBookletHtml(chNum, chapter) {
  let { coverImage, pages, illCount, textOnlyCount } = buildChapterPages(chapter);

  // Apply user's illustration remapping if --remap flag is used
  if (USE_REMAP) {
    ({ coverImage, pages } = applyRemap(chNum, coverImage, pages));
    illCount = pages.filter(p => p.illustration).length;
    textOnlyCount = pages.filter(p => !p.illustration).length;
  }

  const chName = chapter.l2?.metadata?.original_title || chapter.scenes[0]?.metadata?.chapter_name || `Chapter ${chNum}`;

  let spreadsHtml = '';

  // Build a flat list of individual pages (each half of a spread)
  // This makes page numbering, counting, and imposition straightforward.
  let pageNum = 0;

  // Cover spread: page 1 = cover image, page 2 = title
  pageNum++;
  spreadsHtml += `
    <div class="spread cover-spread" data-spread="1">
      <div class="page-left cover-image" data-page="${pageNum}">
        <img src="${coverImage}" alt="Cover illustration">
        <div class="page-number page-number-left">${pageNum}</div>
      </div>`;
  pageNum++;
  spreadsHtml += `
      <div class="page-right cover-title" data-page="${pageNum}">
        <div class="title-block">
          <div class="series-name">ALICE IN WONDERLAND</div>
          <div class="book-number">CHAPTER ${chNum}</div>
          <h1>${escapeHtml(chName.toUpperCase())}</h1>
          <div class="author">BY LEWIS CARROLL</div>
          <div class="page-info">${pages.length} CONTENT PAGES</div>
        </div>
        <div class="page-number page-number-right">${pageNum}</div>
      </div>
    </div>`;

  // Story pages
  for (let i = 0; i < pages.length; i++) {
    const page = pages[i];
    const textHtml = formatTextAsHtml(page.text);
    const spreadIdx = Math.floor(i / 1) + 2; // for data-spread

    // Left page: illustration or decorative
    pageNum++;
    if (page.illustration) {
      spreadsHtml += `
    <div class="spread" data-spread="${spreadIdx}">
      <div class="page-left" data-page="${pageNum}">
        <img src="${page.illustration.url}" alt="${escapeHtml(page.illustration.scene || '')}">
        <div class="page-number page-number-left">${pageNum}</div>
      </div>`;
    } else {
      spreadsHtml += `
    <div class="spread text-only" data-spread="${spreadIdx}">
      <div class="page-left decorative-panel" data-page="${pageNum}">
        <div class="chapter-ornament">
          <div class="ornament-number">${chNum}</div>
        </div>
        <div class="page-number page-number-left">${pageNum}</div>
      </div>`;
    }

    // Right page: text
    pageNum++;
    spreadsHtml += `
      <div class="page-right" data-page="${pageNum}">
        <div class="text-block">
          ${textHtml}
        </div>
        <div class="page-number page-number-right">${pageNum}</div>
      </div>
    </div>`;
  }

  // Back cover
  pageNum++;
  spreadsHtml += `
    <div class="spread back-cover" data-spread="${pages.length + 2}">
      <div class="page-left decorative-panel" data-page="${pageNum}">
        <div class="chapter-ornament">
          <div class="ornament-star">&#10038;</div>
        </div>
        <div class="page-number page-number-left">${pageNum}</div>
      </div>`;
  pageNum++;
  spreadsHtml += `
      <div class="page-right back-text" data-page="${pageNum}">
        <div class="back-block">
          <div class="the-end">THE END</div>
          <div class="back-info">
            <p>CHAPTER ${chNum}: ${escapeHtml(chName.toUpperCase())}</p>
            <p class="small">ALICE'S ADVENTURES IN WONDERLAND (1865)</p>
            <p class="small">WORDS BY LEWIS CARROLL</p>
            <p class="small">ALL ILLUSTRATIONS ARE PUBLIC DOMAIN</p>
            <p class="small">MADE WITH LOVE AT RECURSIVE.ECO</p>
          </div>
        </div>
        <div class="page-number page-number-right">${pageNum}</div>
      </div>
    </div>`;

  // Pad to multiple of 4 with blank pages
  const totalPages = pageNum;
  const remainder = totalPages % 4;
  if (remainder !== 0) {
    const blanksNeeded = 4 - remainder;
    for (let b = 0; b < blanksNeeded; b += 2) {
      pageNum++;
      spreadsHtml += `
    <div class="spread blank-spread">
      <div class="page-left blank-page" data-page="${pageNum}">
        <div class="page-number page-number-left">${pageNum}</div>
      </div>`;
      pageNum++;
      spreadsHtml += `
      <div class="page-right blank-page" data-page="${pageNum}">
        <div class="page-number page-number-right">${pageNum}</div>
      </div>
    </div>`;
    }
  }

  return { html: null, spreadsHtml, chName, coverImage, pageCount: pages.length, illCount, textOnlyCount };
}

function wrapHtml(chNum, chName, spreadsHtml, karaokeData, nextChapterUrl) {
  const audioFile = karaokeData ? karaokeData.audio_file : null;
  const karaokePages = karaokeData ? JSON.stringify(karaokeData.pages) : 'null';
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter ${chNum}: ${escapeHtml(chName)} — Alice in Wonderland</title>
  <style>
    @page { size: landscape; margin: 0; }
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'Georgia', 'Cambria', 'Times New Roman', serif;
      background: white;
      color: #1a1a1a;
    }

    .spread {
      width: 100vw;
      height: 100vh;
      display: flex;
      page-break-after: always;
      break-after: page;
      overflow: hidden;
    }
    .spread:last-child {
      page-break-after: avoid;
      break-after: avoid;
    }

    /* Left page: illustration */
    .page-left {
      width: 50%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f8f5f0;
      padding: 16px;
      overflow: hidden;
      position: relative;
      border-right: 2px solid #d0c8b8;
    }
    .page-left img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 4px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Right page: text */
    .page-right {
      width: 50%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: flex-start;
      padding: 32px 5% 32px 5%;
      background: white;
      position: relative;
      overflow: hidden;
      border-left: 2px solid #d0c8b8;
    }

    /* Text block — NEVER scroll */
    .text-block {
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      flex: 1;
      width: 100%;
      overflow: hidden;
    }

    /* Default text style — JS auto-fit adjusts font-size to fill container */
    .text-block p {
      font-size: 18px;
      line-height: 1.7;
      font-weight: ${USE_CAPS ? '700' : '400'};
      text-align: justify;
      text-align-last: left;
      text-transform: ${USE_CAPS ? 'uppercase' : 'none'};
      hyphens: auto;
      -webkit-hyphens: auto;
      word-break: break-word;
      letter-spacing: ${USE_CAPS ? '0.3px' : '0'};
      margin-bottom: 0.8em;
      text-indent: 1.5em;
    }
    /* All paragraphs indented uniformly */
    .text-block p:last-child { margin-bottom: 0; }

    .page-number {
      font-size: 11px;
      color: #999;
      position: absolute;
      bottom: 8px;
    }
    .page-number-left { left: 16px; }
    .page-number-right { right: 16px; }

    /* Blank pages (padding to multiple of 4) */
    .blank-page {
      background: #faf8f5;
    }

    /* Decorative panel (text-only pages) */
    .decorative-panel {
      background: #2c1810;
      border-right-color: #5a4030;
    }
    .decorative-panel .page-number { color: #5a4030; }
    .chapter-ornament {
      text-align: center;
      color: #d4a76a;
    }
    .ornament-number {
      font-size: clamp(48px, 8vw, 96px);
      font-weight: 800;
      letter-spacing: 4px;
      opacity: 0.3;
      font-family: 'Georgia', serif;
    }
    .ornament-star {
      font-size: clamp(36px, 6vw, 72px);
      opacity: 0.3;
    }

    /* Cover */
    .cover-title {
      background: #2c1810;
      color: white;
    }
    .title-block {
      text-align: center;
      font-family: 'Georgia', serif;
    }
    .series-name {
      font-size: clamp(11px, 1.5vw, 16px);
      letter-spacing: 4px;
      color: #d4a76a;
      margin-bottom: 12px;
    }
    .book-number {
      font-size: clamp(13px, 1.8vw, 20px);
      letter-spacing: 3px;
      color: #d4a76a;
      margin-bottom: 20px;
    }
    .title-block h1 {
      font-size: clamp(20px, 3.8vw, 42px);
      line-height: 1.2;
      margin-bottom: 25px;
      font-weight: 800;
      letter-spacing: 1px;
    }
    .author {
      font-size: clamp(11px, 1.3vw, 14px);
      letter-spacing: 3px;
      color: #d4a76a;
      margin-bottom: 8px;
    }
    .page-info {
      font-size: clamp(9px, 1vw, 11px);
      letter-spacing: 2px;
      color: #a08060;
      margin-top: 5px;
    }
    .cover-image { background: #2c1810; border-right-color: #5a4030; }
    .cover-image img {
      border-radius: 8px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    .cover-title { border-left-color: #5a4030; }
    .cover-title .page-number { color: #5a4030; }
    .cover-image .page-number { color: #5a4030; }

    /* Back cover */
    .back-text {
      background: #2c1810;
      color: white;
      border-left-color: #5a4030;
    }
    .back-text .page-number { color: #5a4030; }
    .back-block {
      text-align: center;
      font-family: 'Georgia', serif;
    }
    .the-end {
      font-size: clamp(24px, 4vw, 44px);
      font-weight: 800;
      letter-spacing: 6px;
      margin-bottom: 30px;
      color: #d4a76a;
    }
    .back-info p {
      font-size: clamp(10px, 1.2vw, 13px);
      letter-spacing: 2px;
      margin-bottom: 6px;
      color: #d4a76a;
    }
    .back-info .small {
      font-size: clamp(8px, 0.9vw, 10px);
      color: #a08060;
    }

    /* Print */
    @media print {
      body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
        padding-top: 0 !important;
        background: white !important;
      }
      .spread {
        height: 100vh;
        border-bottom: none !important;
        min-height: auto !important;
        page-break-inside: avoid;
        break-inside: avoid;
      }
      .page-left img { box-shadow: none; }
      .cover-image img { box-shadow: none; }
      .toolbar { display: none !important; }
      #tapOverlay { display: none !important; }
      #singBall { display: none !important; }
      .audio-progress { display: none !important; }
      mark.search-match { background: transparent !important; color: inherit !important; }
      .sheet-label { background: white; }
    }

    /* ── Toolbar (hidden in print) ── */
    .toolbar {
      position: fixed;
      top: 0; left: 0; right: 0;
      z-index: 100;
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 16px;
      background: #2c1810;
      color: #d4a76a;
      font-family: 'Georgia', serif;
      font-size: 13px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      transition: opacity 0.5s ease, transform 0.5s ease;
    }
    .toolbar.toolbar-hidden {
      opacity: 0;
      transform: translateY(-100%);
      pointer-events: none;
    }
    .toolbar input[type="text"] {
      padding: 5px 10px;
      border: 1px solid #d4a76a;
      border-radius: 4px;
      background: #1a0f08;
      color: #f0e6d6;
      font-size: 13px;
      font-family: 'Georgia', serif;
      width: 180px;
    }
    .toolbar input::placeholder { color: #8a7060; }
    .toolbar button {
      padding: 5px 12px;
      border: 1px solid #d4a76a;
      border-radius: 4px;
      background: #1a0f08;
      color: #d4a76a;
      font-size: 12px;
      cursor: pointer;
      font-family: 'Georgia', serif;
    }
    .toolbar button:hover { background: #3c2820; }
    .toolbar button.active { background: #d4a76a; color: #2c1810; }
    .toolbar select {
      padding: 4px 6px;
      border: 1px solid #d4a76a;
      border-radius: 4px;
      background: #1a0f08;
      color: #d4a76a;
      font-size: 11px;
      font-family: 'Georgia', serif;
      cursor: pointer;
    }
    .toolbar .match-count { font-size: 11px; color: #a08060; min-width: 60px; }
    .toolbar .spacer { flex: 1; }
    .toolbar .ch-title { font-size: 12px; letter-spacing: 1px; }

    /* Search highlight (works on k-word spans) */
    .search-match { background: #ffd700 !important; color: #1a1a1a !important; border-radius: 2px; padding: 0 1px; }

    /* Karaoke word highlighting — very slow gradient sweep */
    .k-word {
      transition: color 2.5s ease;
      border-radius: 2px;
      padding: 0 1px;
    }
    /* Words already spoken — subtle dim, slow fade */
    .k-word.k-spoken { color: #9a8a7a; transition: color 3s ease; }
    /* Current word — gentle warm, barely noticeable bump */
    .k-word.k-active { color: #b89060; transition: color 1.5s ease; }
    /* Nearby words — soft gradient between spoken and unspoken */
    .k-word.k-near { color: #8a7560; transition: color 2s ease; }

    /* Tap-to-pause overlay (YouTube-style, invisible) */
    #tapOverlay {
      position: fixed;
      inset: 0;
      z-index: 50;
      background: transparent;
      cursor: pointer;
      display: none;
    }
    #tapOverlay.active { display: block; }

    /* Ball removed — gradient-only karaoke */
    #singBall { display: none; }

    /* Audio progress bar (inside toolbar) */
    .audio-progress {
      flex: 1;
      min-width: 80px;
      height: 6px;
      background: rgba(255,255,255,0.15);
      border-radius: 3px;
      cursor: pointer;
      position: relative;
      cursor: pointer;
    }
    .audio-progress-bar {
      height: 100%;
      background: #d4a76a;
      width: 0%;
      transition: width 0.3s linear;
      border-radius: 3px;
    }
    .audio-progress:hover {
      height: 8px;
    }

    /* Audio controls hidden in print via consolidated @media print block above */

    /* Screen: page dividers */
    @media screen {
      .spread {
        border-bottom: 3px dashed #ccc;
        min-height: 100vh;
      }
      .spread:last-child { border-bottom: none; }
      body { background: #e8e8e8; padding-top: 44px; }
    }

    /* Toolbar + search highlights hidden in print via consolidated @media print block above */

    /* Booklet imposition mode — pages rearranged for saddle-stitch printing */
    body.booklet-mode .spread {
      width: 100vw;
      height: 100vh;
      position: relative;
      display: flex;
    }
    /* In booklet mode, all pages get uniform styling regardless of original role */
    body.booklet-mode .page-left {
      width: 50%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f8f5f0;
      padding: 12px 3%;
      overflow: hidden;
      position: relative;
      border-right: 1px solid #d0c8b8;
      border-left: none;
    }
    body.booklet-mode .page-right {
      width: 50%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f8f5f0;
      padding: 12px 3%;
      overflow: hidden;
      position: relative;
      border-left: 1px solid #d0c8b8;
      border-right: none;
    }
    /* In booklet mode, text blocks should adapt to available space */
    body.booklet-mode .text-block {
      width: 100%;
      align-self: flex-start;
    }
    body.booklet-mode .text-block p {
      font-size: 11px;
      line-height: 1.4;
    }
    body.booklet-mode .page-left img,
    body.booklet-mode .page-right img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 2px;
      box-shadow: none;
    }
    /* Title block and back-block adapt to any position */
    body.booklet-mode .title-block,
    body.booklet-mode .back-block {
      text-align: center;
      width: 100%;
    }
    body.booklet-mode .title-block h1 { font-size: clamp(14px, 2vw, 22px); }
    body.booklet-mode .chapter-ornament {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
    }
    /* Page numbers in booklet mode */
    body.booklet-mode .page-number {
      position: absolute;
      bottom: 4px;
      font-size: 8px;
      color: #999;
    }
    body.booklet-mode .page-number-left { left: 8px; }
    body.booklet-mode .page-number-right { right: 8px; }
    .sheet-label {
      position: absolute;
      top: 4px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 9px;
      letter-spacing: 2px;
      color: #999;
      background: rgba(255,255,255,0.8);
      padding: 2px 12px;
      border-radius: 4px;
      z-index: 10;
      text-transform: uppercase;
    }
  </style>
</head>
<body>
<div class="toolbar">
  <span class="ch-title">CH ${chNum}</span>
  <button id="playBtn">&#9654; Play</button>
  <select id="speedCtrl" title="Playback speed">
    <option value="0.5">0.5x</option>
    <option value="0.75">0.75x</option>
    <option value="1" selected>1x</option>
    <option value="1.25">1.25x</option>
    <option value="1.5">1.5x</option>
    <option value="2">2x</option>
  </select>
  <div class="audio-progress" id="progressTrack">
    <div class="audio-progress-bar" id="progressBar"></div>
  </div>
  <span class="ch-title" style="color:#a08060" id="audioTime"></span>
  <input type="text" id="searchInput" placeholder="Search..." autocomplete="off" style="width:120px">
  <span class="match-count" id="matchCount"></span>
  <button id="caseToggle" title="Toggle uppercase/lowercase">Aa</button>
  <button id="fullscreenBtn">&#x26F6; Fullscreen</button>
  <button id="toggleMode">📖 Print</button>
</div>
<div id="singBall"></div>
<div id="tapOverlay"></div>
${spreadsHtml}
<script>
// Show total page count
(function() {
  var total = document.querySelectorAll('.page-left[data-page], .page-right[data-page]').length;
  var el = document.getElementById('pageTotal');
  if (el) el.textContent = total + ' pages (x' + Math.ceil(total / 4) + ' sheets)';
})();

// ── Toolbar auto-hide on mouse inactivity ──
(function() {
  var toolbar = document.querySelector('.toolbar');
  var hideTimer = null;
  var HIDE_DELAY = 3000; // 3 seconds

  function showToolbar() {
    toolbar.classList.remove('toolbar-hidden');
    clearTimeout(hideTimer);
    hideTimer = setTimeout(function() {
      toolbar.classList.add('toolbar-hidden');
    }, HIDE_DELAY);
  }

  document.addEventListener('mousemove', showToolbar);
  document.addEventListener('click', showToolbar);
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') showToolbar();
  });

  // Start the initial hide timer
  hideTimer = setTimeout(function() {
    toolbar.classList.add('toolbar-hidden');
  }, HIDE_DELAY);
})();

// Auto-fit: measure each text block's rendered height and scale font down until it fits.
// Runs on load so text is correctly sized before printing.
(function() {
  const MAX_FONT = 22;
  const MIN_FONT = 9;
  const STEP = 0.5;

  function fitAll() {
    document.querySelectorAll('.text-block').forEach(function(block) {
      var container = block.parentElement;
      // Available height = container height minus page-number space
      var maxH = container.clientHeight - 32;
      var ps = block.querySelectorAll('p');
      if (!ps.length) return;

      // Start at max font and shrink until it fits
      var size = MAX_FONT;
      function applySize(s) {
        ps.forEach(function(p) { p.style.fontSize = s + 'px'; });
      }
      applySize(size);

      // Shrink until content fits or we hit minimum
      while (block.scrollHeight > maxH && size > MIN_FONT) {
        size -= STEP;
        applySize(size);
      }
    });
  }

  // Run on load and before print
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fitAll);
  } else {
    fitAll();
  }
  window.addEventListener('beforeprint', fitAll);
  window.addEventListener('resize', fitAll);
})();

// ── Word Search Highlighting (karaoke-safe) ──
// Works by adding a CSS class to k-word spans that match, instead of
// restructuring the DOM with <mark> elements (which breaks karaoke).
(function() {
  var input = document.getElementById('searchInput');
  var countEl = document.getElementById('matchCount');
  if (!input) return;

  function clearSearch() {
    document.querySelectorAll('.k-word.search-match, .search-match').forEach(function(el) {
      el.classList.remove('search-match');
    });
    countEl.textContent = '';
  }

  var debounceTimer;
  input.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function() {
      clearSearch();
      var query = input.value.trim();
      if (query.length < 2) return;
      try {
        var regex = new RegExp(query.replace(/[-\\/\\\\^$*+?.()|[\\]{}]/g, '\\\\$&'), 'i');
        var total = 0;
        // Search through k-word spans (karaoke mode)
        var kWords = document.querySelectorAll('.k-word');
        if (kWords.length > 0) {
          kWords.forEach(function(span) {
            if (regex.test(span.textContent)) {
              span.classList.add('search-match');
              total++;
            }
          });
        } else {
          // Fallback: search plain text blocks
          document.querySelectorAll('.text-block p').forEach(function(p) {
            var text = p.textContent;
            var matches = text.match(new RegExp(regex.source, 'gi'));
            if (matches) total += matches.length;
          });
        }
        countEl.textContent = total > 0 ? total + ' found' : 'no matches';
      } catch(e) {}
    }, 300);
  });

  input.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') { input.value = ''; clearSearch(); }
  });
})();

// ── Booklet Imposition Toggle ──
// Saddle-stitch booklet: rearranges individual pages (not spreads) into
// print-ready sheet order. Total pages already padded to multiple of 4.
(function() {
  var btn = document.getElementById('toggleMode');
  if (!btn) return;
  var isBooklet = false;
  var originalHTML = '';

  // Preserved elements that should not be removed during toggle
  var KEEP_IDS = ['toggleMode', 'singBall', 'tapOverlay'];

  function isPreserved(el) {
    if (el.classList && el.classList.contains('toolbar')) return true;
    if (KEEP_IDS.indexOf(el.id) !== -1) return true;
    return false;
  }

  // Fix page class: swap page-left/page-right based on actual position
  // Strip special spread-level classes (cover-image, cover-title, back-text, etc.)
  function setPagePosition(pageEl, position) {
    // Remove all position/type classes, keep content
    var cl = pageEl.classList;
    cl.remove('page-left', 'page-right', 'cover-image', 'cover-title',
              'back-text', 'decorative-panel', 'blank-page');
    if (position === 'left') {
      cl.add('page-left');
    } else {
      cl.add('page-right');
    }
  }

  btn.addEventListener('click', function() {
    isBooklet = !isBooklet;
    btn.classList.toggle('active', isBooklet);
    btn.textContent = isBooklet ? 'Reading Mode' : 'Print';
    document.body.classList.toggle('booklet-mode', isBooklet);

    // Get all individual page elements (NOT k-word spans which also have data-page)
    var allPages = Array.from(document.querySelectorAll('.page-left[data-page], .page-right[data-page]'));
    var N = allPages.length; // already multiple of 4

    if (!originalHTML) {
      // Save original body content (excluding preserved elements)
      originalHTML = '';
      Array.from(document.body.children).forEach(function(child) {
        if (!isPreserved(child)) originalHTML += child.outerHTML;
      });
    }

    if (isBooklet) {
      // Collect pages by their number
      var pageMap = {};
      allPages.forEach(function(el) {
        pageMap[parseInt(el.dataset.page)] = el.cloneNode(true);
      });

      // Saddle-stitch imposition for N pages (N is multiple of 4)
      // Each printed sheet has 4 page positions:
      //   Front: left=N-2i, right=2i+1  (page numbers 1-indexed)
      //   Back:  left=2i+2, right=N-1-2i
      var container = document.createElement('div');
      container.id = 'booklet-pages';
      var sheets = N / 4;

      for (var i = 0; i < sheets; i++) {
        var frontLeft  = N - 2 * i;     // e.g. sheet 0: page N
        var frontRight = 2 * i + 1;     // e.g. sheet 0: page 1
        var backLeft   = 2 * i + 2;     // e.g. sheet 0: page 2
        var backRight  = N - 1 - 2 * i; // e.g. sheet 0: page N-1

        // Sheet front
        var frontSpread = document.createElement('div');
        frontSpread.className = 'spread sheet-spread';
        frontSpread.innerHTML = '<div class="sheet-label">SHEET ' + (i+1) + ' FRONT</div>';
        var fl = pageMap[frontLeft];
        var fr = pageMap[frontRight];
        if (fl) { setPagePosition(fl, 'left'); frontSpread.appendChild(fl); }
        if (fr) { setPagePosition(fr, 'right'); frontSpread.appendChild(fr); }
        container.appendChild(frontSpread);

        // Sheet back
        var backSpread = document.createElement('div');
        backSpread.className = 'spread sheet-spread';
        backSpread.innerHTML = '<div class="sheet-label">SHEET ' + (i+1) + ' BACK</div>';
        var bl = pageMap[backLeft];
        var br = pageMap[backRight];
        if (bl) { setPagePosition(bl, 'left'); backSpread.appendChild(bl); }
        if (br) { setPagePosition(br, 'right'); backSpread.appendChild(br); }
        container.appendChild(backSpread);
      }

      // Replace body content (keep preserved elements)
      var toRemove = [];
      Array.from(document.body.children).forEach(function(child) {
        if (!isPreserved(child)) toRemove.push(child);
      });
      toRemove.forEach(function(el) { el.remove(); });
      document.body.appendChild(container);
    } else {
      // Restore original (keep preserved elements)
      var toRemove = [];
      Array.from(document.body.children).forEach(function(child) {
        if (!isPreserved(child)) toRemove.push(child);
      });
      toRemove.forEach(function(el) { el.remove(); });
      document.body.insertAdjacentHTML('beforeend', originalHTML);
    }

    // Re-run auto-fit
    window.dispatchEvent(new Event('resize'));
  });
})();

// ── Karaoke Audio Player ──
(function() {
  var KARAOKE_PAGES = ${karaokePages};
  var AUDIO_FILE = ${audioFile ? `'../audio/librivox/${audioFile}'` : 'null'};

  if (!KARAOKE_PAGES || !AUDIO_FILE) {
    // No karaoke data — hide play button
    var playBtn = document.getElementById('playBtn');
    if (playBtn) playBtn.style.display = 'none';
    return;
  }

  // Create audio element
  var audio = document.createElement('audio');
  audio.src = AUDIO_FILE;
  audio.preload = 'auto';
  document.body.appendChild(audio);

  var playBtn = document.getElementById('playBtn');
  var timeEl = document.getElementById('audioTime');
  var progEl = document.getElementById('progressBar');
  var progressTrack = document.getElementById('progressTrack');
  var isPlaying = false;

  // Wrap words in text blocks with karaoke spans
  var allKWords = [];
  KARAOKE_PAGES.forEach(function(pageData) {
    var pageEl = document.querySelector('[data-page="' + pageData.pageNum + '"]');
    if (!pageEl) return;
    var textBlock = pageEl.querySelector('.text-block');
    if (!textBlock) return;

    // Collect all text nodes
    var walker = document.createTreeWalker(textBlock, NodeFilter.SHOW_TEXT, null, false);
    var textNodes = [];
    var node;
    while (node = walker.nextNode()) {
      if (node.textContent.trim()) textNodes.push(node);
    }

    // Walk through page words and match to text nodes
    var wordIdx = 0;
    textNodes.forEach(function(textNode) {
      var text = textNode.textContent;
      var parts = text.split(/(\\s+)/);
      var frag = document.createDocumentFragment();

      parts.forEach(function(part) {
        if (/^\\s+$/.test(part) || !part) {
          frag.appendChild(document.createTextNode(part));
          return;
        }
        if (wordIdx < pageData.words.length) {
          var w = pageData.words[wordIdx];
          var span = document.createElement('span');
          span.className = 'k-word';
          span.dataset.start = w.start;
          span.dataset.end = w.end;
          span.dataset.page = pageData.pageNum;
          span.textContent = part;
          allKWords.push(span);
          frag.appendChild(span);
          wordIdx++;
        } else {
          frag.appendChild(document.createTextNode(part));
        }
      });

      textNode.parentNode.replaceChild(frag, textNode);
    });
  });

  // Format time as m:ss
  function formatTime(s) {
    var m = Math.floor(s / 60);
    var sec = Math.floor(s % 60);
    return m + ':' + (sec < 10 ? '0' : '') + sec;
  }

  // Play/pause toggle (shared function for button + tap overlay)
  var tapOverlay = document.getElementById('tapOverlay');

  function togglePlayPause() {
    if (isPlaying) {
      audio.pause();
      isPlaying = false;
      playBtn.innerHTML = '&#9654; Play';
      playBtn.classList.remove('active');
      if (singBall) singBall.classList.remove('visible');
      if (tapOverlay) tapOverlay.classList.remove('active');
    } else {
      audio.play();
      isPlaying = true;
      playBtn.innerHTML = '&#9646;&#9646; Pause';
      playBtn.classList.add('active');
      if (singBall) singBall.classList.add('visible');
      if (tapOverlay) tapOverlay.classList.add('active');
    }
  }

  playBtn.addEventListener('click', togglePlayPause);

  // Tap-to-pause overlay (click anywhere on page to pause/play)
  if (tapOverlay) {
    tapOverlay.addEventListener('click', function(e) {
      e.stopPropagation();
      togglePlayPause();
    });
  }

  // Spacebar also toggles play/pause
  document.addEventListener('keydown', function(e) {
    if (e.code === 'Space' && document.activeElement.tagName !== 'INPUT') {
      e.preventDefault();
      togglePlayPause();
    }
  });

  audio.addEventListener('ended', function() {
    isPlaying = false;
    playBtn.innerHTML = '&#9654; Play';
    playBtn.classList.remove('active');
    if (singBall) singBall.classList.remove('visible');
    if (tapOverlay) tapOverlay.classList.remove('active');
    allKWords.forEach(function(el) {
      el.classList.remove('k-active', 'k-spoken', 'k-near');
    });
  });

  // Pre-parse timestamps into arrays for fast binary search
  var starts = allKWords.map(function(el) { return parseFloat(el.dataset.start); });
  var ends = allKWords.map(function(el) { return parseFloat(el.dataset.end); });
  var NEAR_RANGE = 8; // highlight ±8 words — wide gradient zone

  // Binary search: find the word whose time range contains t
  function findWordAt(t) {
    var lo = 0, hi = allKWords.length - 1;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1;
      if (t < starts[mid]) { hi = mid - 1; }
      else if (t > ends[mid] + 0.3) { lo = mid + 1; }
      else { return mid; }
    }
    // Between words — find closest upcoming word
    if (lo < allKWords.length && t < starts[lo]) return lo;
    return lo > 0 ? lo - 1 : 0;
  }

  var lastActiveIdx = -1;
  var lastScrollPage = -1;
  var lastUpdateTime = 0;
  var singBall = document.getElementById('singBall');

  // Move the bouncing ball above the active word
  function moveBallToWord(wordEl) {
    if (!singBall || !wordEl) return;
    var rect = wordEl.getBoundingClientRect();
    var scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;
    singBall.style.left = (rect.left + scrollX + rect.width / 2 - 5) + 'px';
    singBall.style.top = (rect.top + scrollY - 14) + 'px';
  }

  function updateKaraoke() {
    if (!isPlaying) return;
    var t = audio.currentTime;

    // Throttle updates to ~10fps for calm feel (every 100ms)
    var now = Date.now();
    if (now - lastUpdateTime < 100) {
      requestAnimationFrame(updateKaraoke);
      return;
    }
    lastUpdateTime = now;

    // Update progress bar
    if (audio.duration) {
      progEl.style.width = ((t / audio.duration) * 100) + '%';
      timeEl.textContent = formatTime(t) + ' / ' + formatTime(audio.duration);
    }

    // Don't start karaoke until narration actually begins (skip LibriVox intro)
    if (allKWords.length === 0 || t < starts[0] - 0.1) {
      requestAnimationFrame(updateKaraoke);
      return;
    }

    // Find current word via binary search
    var idx = findWordAt(t);

    if (idx !== lastActiveIdx) {
      // Clear old highlights in a range around the old position
      if (lastActiveIdx >= 0) {
        var clearFrom = Math.max(0, lastActiveIdx - NEAR_RANGE - 1);
        var clearTo = Math.min(allKWords.length - 1, lastActiveIdx + NEAR_RANGE + 1);
        for (var c = clearFrom; c <= clearTo; c++) {
          allKWords[c].classList.remove('k-active', 'k-near');
        }
      }

      // Mark spoken words (only newly spoken ones, don't re-scan all)
      if (lastActiveIdx >= 0 && lastActiveIdx < idx) {
        for (var s = lastActiveIdx; s < idx; s++) {
          allKWords[s].classList.add('k-spoken');
          allKWords[s].classList.remove('k-active', 'k-near');
        }
      }

      // Apply new highlights
      allKWords[idx].classList.add('k-active');
      allKWords[idx].classList.remove('k-spoken', 'k-near');

      // Move bouncing ball
      moveBallToWord(allKWords[idx]);

      // Nearby words get soft highlight
      for (var n = 1; n <= NEAR_RANGE; n++) {
        if (idx + n < allKWords.length) {
          allKWords[idx + n].classList.add('k-near');
          allKWords[idx + n].classList.remove('k-spoken', 'k-active');
        }
      }

      lastActiveIdx = idx;

      // Auto-scroll to spread (only when page changes)
      var pageNum = parseInt(allKWords[idx].dataset.page);
      if (pageNum !== lastScrollPage) {
        lastScrollPage = pageNum;
        var pageEl = document.querySelector('[data-page="' + pageNum + '"]');
        if (pageEl) {
          var spread = pageEl.closest('.spread');
          if (spread) {
            spread.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }
      }
    }

    requestAnimationFrame(updateKaraoke);
  }

  audio.addEventListener('play', function() {
    lastUpdateTime = 0;
    if (singBall) singBall.classList.add('visible');
    requestAnimationFrame(updateKaraoke);
  });

  // Click on progress track to seek — immediately update bar + animation
  progressTrack.addEventListener('click', function(e) {
    if (!audio.duration) return;
    var rect = progressTrack.getBoundingClientRect();
    var pct = (e.clientX - rect.left) / rect.width;
    // Immediately update progress bar visually
    progressBar.style.width = (pct * 100) + '%';
    audio.currentTime = pct * audio.duration;
    // Force immediate karaoke update
    lastUpdateTime = 0;
    if (isPlaying) requestAnimationFrame(updateKaraoke);
  });

  // Handle any audio seek (progress bar click, or native controls)
  audio.addEventListener('seeked', function() {
    // Reset all karaoke highlights
    allKWords.forEach(function(el) {
      el.classList.remove('k-active', 'k-spoken', 'k-near');
    });
    // Mark words before current position as spoken
    var t = audio.currentTime;
    if (allKWords.length > 0 && t >= starts[0]) {
      var seekIdx = findWordAt(t);
      for (var i = 0; i < seekIdx; i++) {
        allKWords[i].classList.add('k-spoken');
      }
    }
    lastActiveIdx = -1;
    lastScrollPage = -1;
    lastUpdateTime = 0; // force immediate update on next frame
    // Move ball to new position
    if (singBall && allKWords.length > 0 && t >= starts[0]) {
      var bIdx = findWordAt(t);
      moveBallToWord(allKWords[bIdx]);
    }
    // Re-trigger animation loop (it may have stopped)
    if (isPlaying) {
      requestAnimationFrame(updateKaraoke);
    }
  });

  // Safety net: if audio is playing but animation loop stopped, re-trigger every 2s
  setInterval(function() {
    if (isPlaying && !audio.paused) {
      lastUpdateTime = 0;
      requestAnimationFrame(updateKaraoke);
    }
  }, 2000);

  // ── Speed controls ──
  var speedCtrl = document.getElementById('speedCtrl');
  if (speedCtrl) {
    speedCtrl.addEventListener('change', function() {
      audio.playbackRate = parseFloat(speedCtrl.value);
    });
  }
})();

// ── Fullscreen toggle ──
(function() {
  var fsBtn = document.getElementById('fullscreenBtn');
  if (!fsBtn) return;
  fsBtn.addEventListener('click', function() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(function() {});
      fsBtn.textContent = '✕ Exit FS';
    } else {
      document.exitFullscreen();
      fsBtn.textContent = '⛶ Fullscreen';
    }
  });
  document.addEventListener('fullscreenchange', function() {
    if (!document.fullscreenElement) {
      fsBtn.textContent = '⛶ Fullscreen';
    }
  });
})();

// ── Autoplay mode (for continuous recording) ──
// URL param ?autoplay — auto-enters fullscreen, starts playing
// When chapter ends, navigates to next chapter with ?autoplay
(function() {
  var NEXT_CHAPTER = ${nextChapterUrl ? `'${nextChapterUrl}'` : 'null'};
  var params = new URLSearchParams(window.location.search);
  var isAutoplay = params.has('autoplay');

  if (isAutoplay) {
    // Small delay to let page render, then start
    setTimeout(function() {
      // Enter fullscreen
      document.documentElement.requestFullscreen().catch(function() {});
      // Start playing
      var playBtn = document.getElementById('playBtn');
      if (playBtn) playBtn.click();
    }, 1500);
  }

  // When audio ends, navigate to next chapter if autoplay
  var audio = document.querySelector('audio');
  if (audio && NEXT_CHAPTER) {
    audio.addEventListener('ended', function() {
      if (isAutoplay || params.has('continuous')) {
        // Brief pause then navigate to next chapter
        setTimeout(function() {
          window.location.href = NEXT_CHAPTER + '?' + window.location.search.slice(1);
        }, 2000);
      }
    });
  }
})();

// ── Chapter title animation during intro ──
// During the LibriVox intro (before narration starts), gently animate the cover title
(function() {
  var titleBlock = document.querySelector('.title-block');
  if (!titleBlock) return;

  var audio = document.querySelector('audio');
  if (!audio) return;

  // Add fade-in animation to title elements
  var style = document.createElement('style');
  style.textContent = [
    '@keyframes titleGlow { 0%,100% { text-shadow: 0 0 0 transparent; } 50% { text-shadow: 0 0 20px rgba(212,167,106,0.4); } }',
    '.title-animating h1 { animation: titleGlow 3s ease-in-out infinite; }',
    '.title-animating .series-name, .title-animating .book-number, .title-animating .author { animation: titleGlow 4s ease-in-out infinite; animation-delay: 1s; }'
  ].join('\\n');
  document.head.appendChild(style);

  audio.addEventListener('play', function() {
    titleBlock.classList.add('title-animating');
  });

  audio.addEventListener('pause', function() {
    titleBlock.classList.remove('title-animating');
  });

  audio.addEventListener('ended', function() {
    titleBlock.classList.remove('title-animating');
  });
})();

// ── Aa Case Toggle ──
(function() {
  var btn = document.getElementById('caseToggle');
  if (!btn) return;
  var isUpper = true;

  btn.addEventListener('click', function() {
    isUpper = !isUpper;
    btn.textContent = isUpper ? 'Aa' : 'AA';
    // Toggle all text blocks between uppercase and original case
    document.querySelectorAll('.text-block p').forEach(function(p) {
      p.style.textTransform = isUpper ? 'uppercase' : 'none';
      p.style.fontWeight = isUpper ? '700' : '400';
      p.style.letterSpacing = isUpper ? '0.3px' : '0';
    });
    // Also toggle title and UI text
    document.querySelectorAll('.title-block h1, .series-name, .book-number, .author, .page-info, .back-block, .the-end, .back-info').forEach(function(el) {
      el.style.textTransform = isUpper ? 'uppercase' : 'none';
    });
  });
})();
</script>
</body>
</html>`;
}

// ── Generate All Booklets ────────────────────────────────────────────

// Load karaoke manifest if available
const karaokeManifestPath = resolve(__dirname, '../grammars/alice-5-minute-stories/audio/librivox/karaoke-manifest.json');
let karaokeManifest = null;
if (existsSync(karaokeManifestPath)) {
  karaokeManifest = JSON.parse(readFileSync(karaokeManifestPath, 'utf8'));
  console.log('Karaoke manifest loaded — audio player will be embedded.\n');
}

const chapterNums = Object.keys(chapterMap).map(Number).sort((a, b) => a - b);
let grandTotalPages = 0;
let grandTotalIll = 0;

const caseLabel = USE_CAPS ? 'ALL CAPS' : 'lowercase';
console.log(`Generating Alice in Wonderland chapter booklets (${caseLabel})...\n`);

// Pre-compute all filenames so each booklet knows the next chapter URL
const chapterFilenames = {};
for (const chNum of chapterNums) {
  const chapter = chapterMap[chNum];
  const chName = chapter.l2?.metadata?.original_title || chapter.scenes[0]?.metadata?.chapter_name || `Chapter ${chNum}`;
  const padNum = String(chNum).padStart(2, '0');
  const slug = chName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '');
  chapterFilenames[chNum] = `chapter${padNum}-${slug}.html`;
}

const bookletInfo = [];

for (let ci = 0; ci < chapterNums.length; ci++) {
  const chNum = chapterNums[ci];
  const chapter = chapterMap[chNum];
  const chName = chapter.l2?.metadata?.original_title || chapter.scenes[0]?.metadata?.chapter_name || `Chapter ${chNum}`;
  const filename = chapterFilenames[chNum];
  const nextChNum = ci < chapterNums.length - 1 ? chapterNums[ci + 1] : null;
  const nextChapterUrl = nextChNum ? `/booklets/${chapterFilenames[nextChNum]}` : null;

  const { spreadsHtml, chName: cn, coverImage: chCover, pageCount, illCount, textOnlyCount } = generateBookletHtml(chNum, chapter);
  const karaokeData = karaokeManifest?.chapters?.[chNum] || null;
  const html = wrapHtml(chNum, chName, spreadsHtml, karaokeData, nextChapterUrl);
  writeFileSync(resolve(outputDir, filename), html);

  grandTotalPages += pageCount;
  grandTotalIll += illCount;

  const padNum = String(chNum).padStart(2, '0');
  const textOnly = textOnlyCount > 0 ? ` (${textOnlyCount} text-only)` : '';
  console.log(`  Ch ${padNum}: ${filename} — ${pageCount} pages, ${illCount} ill${textOnly}`);

  bookletInfo.push({ chNum, chName, filename, pageCount, illCount, coverImage: chCover });
}

// ── Generate Index Page ──────────────────────────────────────────────

const indexHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alice in Wonderland — Illustrated Chapter Books</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Georgia', 'Cambria', serif;
      background: #f8f5f0; color: #2c1810; padding: 40px 20px;
    }
    h1 { text-align: center; font-size: 28px; margin-bottom: 6px; letter-spacing: 2px; }
    .subtitle { text-align: center; font-size: 13px; color: #888; margin-bottom: 10px; letter-spacing: 1px; }
    .description {
      text-align: center; font-size: 14px; color: #666; margin-bottom: 30px;
      max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.6;
    }
    .grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 20px; max-width: 1100px; margin: 0 auto;
    }
    .card {
      background: white; border-radius: 12px; overflow: hidden;
      box-shadow: 0 2px 12px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s;
      text-decoration: none; color: inherit; display: block;
    }
    .card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.15); }
    .card img { width: 100%; height: 180px; object-fit: cover; }
    .card-body { padding: 14px 18px 18px; }
    .card-number { font-size: 10px; letter-spacing: 2px; color: #d4a76a; margin-bottom: 4px; }
    .card-title { font-size: 16px; font-weight: 700; margin-bottom: 6px; line-height: 1.2; }
    .card-meta { font-size: 11px; color: #999; }
    .instructions {
      max-width: 600px; margin: 30px auto 0; padding: 20px;
      background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    .instructions h2 { font-size: 14px; margin-bottom: 10px; letter-spacing: 1px; }
    .instructions ol { padding-left: 18px; line-height: 1.7; font-size: 13px; }
    .instructions li { margin-bottom: 3px; }
    .total { text-align: center; margin-top: 20px; font-size: 12px; color: #aaa; letter-spacing: 1px; }
  </style>
</head>
<body>
  <h1>ALICE IN WONDERLAND</h1>
  <div class="subtitle">ILLUSTRATED CHAPTER BOOKS</div>
  <div class="description">
    Lewis Carroll's complete original text with ${grandTotalIll} public domain illustrations
    by Tenniel, Rackham, Carroll, Hudson, Gutmann, Le Fanu, Walker, Rountree &amp; more.
    Print landscape, fold in half!
  </div>
  <div style="text-align:center; margin-bottom: 24px;">
    <a href="/booklets/${bookletInfo[0].filename}?autoplay=all" style="
      display: inline-block; padding: 14px 36px; background: #2c1810; color: #d4a76a;
      font-family: Georgia, serif; font-size: 16px; letter-spacing: 2px; text-decoration: none;
      border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.2); transition: transform 0.2s, box-shadow 0.2s;
    " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'"
    >&#9654; PLAY ALL CHAPTERS</a>
  </div>
  <div class="grid">
${bookletInfo.map(b => `    <a class="card" href="/booklets/${b.filename}">
      <img src="${b.coverImage}" alt="${escapeHtml(b.chName)}">
      <div class="card-body">
        <div class="card-number">CHAPTER ${b.chNum}</div>
        <div class="card-title">${escapeHtml(b.chName)}</div>
        <div class="card-meta">${b.pageCount} pages &middot; ${b.illCount} illustrations</div>
      </div>
    </a>`).join('\n')}
  </div>
  <div class="instructions">
    <h2>HOW TO PRINT</h2>
    <ol>
      <li>Click a chapter above to open it</li>
      <li>Press <strong>Ctrl+P</strong> (or <strong>Cmd+P</strong> on Mac)</li>
      <li>Set orientation to <strong>Landscape</strong></li>
      <li>Set margins to <strong>None</strong></li>
      <li>Turn on <strong>Background graphics</strong></li>
      <li>Print double-sided (flip on short edge) if available</li>
      <li>Fold each sheet in half &mdash; you have a picture book!</li>
    </ol>
  </div>
  <div class="total">${grandTotalIll} ILLUSTRATIONS &middot; 12 CHAPTERS &middot; ${grandTotalPages} PAGES &middot; ALL PUBLIC DOMAIN</div>
</body>
</html>`;

writeFileSync(resolve(outputDir, 'index.html'), indexHtml);
console.log(`\n  index.html (library page)`);

// ── Generate Illustration Assignment JSON (for reordering tool) ──
// Skip when --remap is active to preserve user's edits

if (!USE_REMAP) {
  const illustrationMap = [];
  for (const chNum of chapterNums) {
    const chapter = chapterMap[chNum];
    const { coverImage, pages } = buildChapterPages(chapter);
    const chName = chapter.l2?.metadata?.original_title || chapter.scenes[0]?.metadata?.chapter_name || `Chapter ${chNum}`;

    illustrationMap.push({
      chapter: chNum,
      page: 0,
      label: `Ch${chNum} Cover`,
      text_preview: chName,
      image_url: coverImage,
      image_info: 'chapter cover',
    });

    for (let i = 0; i < pages.length; i++) {
      const p = pages[i];
      const preview = p.text.substring(0, 60).replace(/\n/g, ' ').trim();
      illustrationMap.push({
        chapter: chNum,
        page: i + 1,
        label: `Ch${chNum} p${i + 1}`,
        text_preview: preview + (p.text.length > 60 ? '...' : ''),
        image_url: p.illustration ? p.illustration.url : '',
        image_info: p.illustration ? `${p.illustration.artist || ''} — ${p.illustration.scene || ''}`.trim() : 'text-only',
      });
    }
  }

  const mapPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-assignments.json');
  writeFileSync(mapPath, JSON.stringify(illustrationMap, null, 2));
  console.log(`  illustration-assignments.json (${illustrationMap.length} entries)`);
} else {
  console.log(`  illustration-assignments.json (preserved — --remap mode)`);
}

console.log(`\nDone! 12 booklets, ${grandTotalPages} total pages, ${grandTotalIll} illustrations.`);
console.log(`Mode: ${caseLabel}${USE_REMAP ? ' + REMAP' : ''}. Use --lowercase flag for normal case${USE_REMAP ? '' : ', --remap for custom illustrations'}.`);
