/**
 * Generate printable HTML booklets from the alice-in-wonderland-chapter-book grammar.
 *
 * One booklet per chapter. Scene-aware illustration assignment ensures
 * each illustration appears next to its matching text passage.
 *
 * Features:
 *   --lowercase  Generate in normal case (default is ALL CAPS)
 *   Dialogue formatted on separate lines for readability
 *   Carroll's original paragraph breaks preserved
 *   5-tier font sizing, never scrollable
 *
 * Usage:
 *   node scripts/generate-alice-booklets.mjs              # ALL CAPS
 *   node scripts/generate-alice-booklets.mjs --lowercase   # Normal case
 *
 * Output: grammars/alice-5-minute-stories/booklets/
 */
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const grammarPath = resolve(__dirname, '../grammars/alice-in-wonderland-chapter-book/grammar.json');
const outputDir = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets');

mkdirSync(outputDir, { recursive: true });

const grammar = JSON.parse(readFileSync(grammarPath, 'utf8'));

// CLI flags
const USE_CAPS = !process.argv.includes('--lowercase');
const MAX_CHARS_PER_PAGE = 1200;

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
  let t = text
    .replace(/_([^_]+)_/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  return USE_CAPS ? t.toUpperCase() : t;
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

    // Format dialogue on separate lines:
    // When a quote starts after narration, put it on a new line
    // Match: [lowercase/punctuation] [space] [opening quote]
    // Opening quotes: \u201c (") or regular "
    cleaned = cleaned.replace(
      /([.!?;:,\)\]])\s+([\u201c\u201e"])/g,
      '$1<br>$2'
    );

    // Also break before dialogue that starts with a dash (em dash dialogue)
    cleaned = cleaned.replace(
      /([.!?])\s+(\u2014|\u2013|—)/g,
      '$1<br>$2'
    );

    return `<p>${escapeHtml(cleaned).replace(/&lt;br&gt;/g, '<br>')}</p>`;
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
  const { coverImage, pages, illCount, textOnlyCount } = buildChapterPages(chapter);
  const chName = chapter.l2?.metadata?.original_title || chapter.scenes[0]?.metadata?.chapter_name || `Chapter ${chNum}`;

  let spreadsHtml = '';

  // Cover page
  spreadsHtml += `
    <div class="spread cover-spread">
      <div class="page-left cover-image">
        <img src="${coverImage}" alt="Cover illustration">
      </div>
      <div class="page-right cover-title">
        <div class="title-block">
          <div class="series-name">ALICE IN WONDERLAND</div>
          <div class="book-number">CHAPTER ${chNum}</div>
          <h1>${escapeHtml(chName.toUpperCase())}</h1>
          <div class="author">BY LEWIS CARROLL</div>
          <div class="page-info">${pages.length} PAGES</div>
        </div>
      </div>
    </div>`;

  // Story pages
  for (let i = 0; i < pages.length; i++) {
    const page = pages[i];
    const textHtml = formatTextAsHtml(page.text);
    const pageNum = i + 1;

    if (page.illustration) {
      spreadsHtml += `
    <div class="spread">
      <div class="page-left">
        <img src="${page.illustration.url}" alt="${escapeHtml(page.illustration.scene || '')}">
      </div>
      <div class="page-right">
        <div class="text-block">
          ${textHtml}
        </div>
        <div class="page-number">${pageNum}</div>
      </div>
    </div>`;
    } else {
      spreadsHtml += `
    <div class="spread text-only">
      <div class="page-left decorative-panel">
        <div class="chapter-ornament">
          <div class="ornament-number">${chNum}</div>
        </div>
      </div>
      <div class="page-right">
        <div class="text-block">
          ${textHtml}
        </div>
        <div class="page-number">${pageNum}</div>
      </div>
    </div>`;
    }
  }

  // Back cover (text-only)
  spreadsHtml += `
    <div class="spread back-cover">
      <div class="page-left decorative-panel">
        <div class="chapter-ornament">
          <div class="ornament-star">&#10038;</div>
        </div>
      </div>
      <div class="page-right back-text">
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
      </div>
    </div>`;

  return { html: wrapHtml(chNum, chName, spreadsHtml), pageCount: pages.length, illCount, textOnlyCount };
}

function wrapHtml(chNum, chName, spreadsHtml) {
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
      justify-content: center;
      padding: 32px 5% 32px 5%;
      background: white;
      position: relative;
      overflow: hidden;
    }

    /* Text block — NEVER scroll */
    .text-block {
      display: flex;
      flex-direction: column;
      justify-content: center;
      flex: 1;
      width: 100%;
      overflow: hidden;
    }

    /* Default text style — JS auto-fit adjusts font-size to fill container */
    .text-block p {
      font-size: 18px;
      line-height: 1.7;
      font-weight: ${USE_CAPS ? '700' : '400'};
      text-align: left;
      letter-spacing: ${USE_CAPS ? '0.3px' : '0'};
      margin-bottom: 1em;
    }
    .text-block p:last-child { margin-bottom: 0; }

    .page-number {
      font-size: 11px;
      color: #ccc;
      position: absolute;
      bottom: 8px;
      right: 16px;
    }

    /* Decorative panel (text-only pages) */
    .decorative-panel {
      background: #2c1810;
    }
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
    .cover-image { background: #2c1810; }
    .cover-image img {
      border-radius: 8px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }

    /* Back cover */
    .back-text {
      background: #2c1810;
      color: white;
    }
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
      body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      .spread { height: 100vh; }
      .page-left img { box-shadow: none; }
      .cover-image img { box-shadow: none; }
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
    .toolbar .match-count { font-size: 11px; color: #a08060; min-width: 60px; }
    .toolbar .spacer { flex: 1; }
    .toolbar .ch-title { font-size: 12px; letter-spacing: 1px; }

    /* Search highlight */
    mark.search-match { background: #ffd700; color: #1a1a1a; border-radius: 2px; padding: 0 1px; }

    /* Screen: page dividers */
    @media screen {
      .spread {
        border-bottom: 3px dashed #ccc;
        min-height: 100vh;
      }
      .spread:last-child { border-bottom: none; }
      body { background: #e8e8e8; padding-top: 44px; }
    }

    /* Print: hide toolbar and search highlights */
    @media print {
      .toolbar { display: none !important; }
      mark.search-match { background: transparent; color: inherit; }
      body { padding-top: 0; }
    }

    /* Booklet imposition mode */
    body.booklet-mode .spread {
      width: 50vw;
      height: 50vh;
      display: inline-flex;
    }
    body.booklet-mode .page-left,
    body.booklet-mode .page-right {
      padding: 12px 3%;
    }
    body.booklet-mode .page-left img {
      border-radius: 2px;
    }
  </style>
</head>
<body>
<div class="toolbar">
  <span class="ch-title">CH ${chNum}</span>
  <input type="text" id="searchInput" placeholder="Search words..." autocomplete="off">
  <span class="match-count" id="matchCount"></span>
  <span class="spacer"></span>
  <button id="toggleMode">📖 Booklet Print</button>
</div>
${spreadsHtml}
<script>
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

// ── Word Search Highlighting ──
(function() {
  var input = document.getElementById('searchInput');
  var countEl = document.getElementById('matchCount');
  if (!input) return;

  function clearMarks() {
    document.querySelectorAll('mark.search-match').forEach(function(m) {
      var parent = m.parentNode;
      parent.replaceChild(document.createTextNode(m.textContent), m);
      parent.normalize();
    });
    countEl.textContent = '';
  }

  function highlightText(node, regex) {
    var count = 0;
    if (node.nodeType === 3) { // Text node
      var match = node.textContent.match(regex);
      if (match) {
        var span = document.createElement('mark');
        span.className = 'search-match';
        var parts = node.textContent.split(regex);
        var frag = document.createDocumentFragment();
        parts.forEach(function(part, i) {
          frag.appendChild(document.createTextNode(part));
          if (i < parts.length - 1) {
            var m = span.cloneNode(false);
            m.textContent = node.textContent.match(new RegExp(regex.source, 'gi'))[count] || match[0];
            frag.appendChild(m);
            count++;
          }
        });
        node.parentNode.replaceChild(frag, node);
      }
      return count;
    }
    if (node.nodeType === 1 && node.tagName !== 'MARK' && node.tagName !== 'SCRIPT') {
      var children = Array.from(node.childNodes);
      children.forEach(function(child) { count += highlightText(child, regex); });
    }
    return count;
  }

  var debounceTimer;
  input.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function() {
      clearMarks();
      var query = input.value.trim();
      if (query.length < 2) return;
      try {
        var regex = new RegExp('(' + query.replace(/[.*+?^\${}()|[\\]\\\\]/g, '\\\\$$&') + ')', 'gi');
        var total = 0;
        document.querySelectorAll('.text-block').forEach(function(block) {
          total += highlightText(block, regex);
        });
        countEl.textContent = total > 0 ? total + ' found' : 'no matches';
      } catch(e) {}
    }, 300);
  });

  input.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') { input.value = ''; clearMarks(); }
  });
})();

// ── Booklet Imposition Toggle ──
(function() {
  var btn = document.getElementById('toggleMode');
  if (!btn) return;
  var isBooklet = false;
  var originalOrder = [];

  btn.addEventListener('click', function() {
    isBooklet = !isBooklet;
    btn.classList.toggle('active', isBooklet);
    btn.textContent = isBooklet ? '📱 App Mode' : '📖 Booklet Print';
    document.body.classList.toggle('booklet-mode', isBooklet);

    var spreads = Array.from(document.querySelectorAll('.spread'));
    if (!originalOrder.length) originalOrder = spreads.map(function(s) { return s; });

    if (isBooklet) {
      // Saddle-stitch imposition: reorder for double-sided folded printing
      var N = spreads.length;
      // Pad to multiple of 4
      while (N % 4 !== 0) N++;
      var order = [];
      var sheets = N / 2;
      for (var i = 0; i < sheets / 2; i++) {
        // Front of sheet: pages [N-1-2i, 2i]
        order.push(N - 1 - 2 * i, 2 * i);
        // Back of sheet: pages [2i+1, N-2-2i]
        order.push(2 * i + 1, N - 2 - 2 * i);
      }
      var container = spreads[0].parentNode;
      order.forEach(function(idx) {
        if (idx < originalOrder.length) {
          container.appendChild(originalOrder[idx]);
        }
      });
    } else {
      // Restore original order
      var container = originalOrder[0].parentNode;
      originalOrder.forEach(function(s) { container.appendChild(s); });
    }

    // Re-run auto-fit after reorder
    window.dispatchEvent(new Event('resize'));
  });
})();
</script>
</body>
</html>`;
}

// ── Generate All Booklets ────────────────────────────────────────────

const chapterNums = Object.keys(chapterMap).map(Number).sort((a, b) => a - b);
let grandTotalPages = 0;
let grandTotalIll = 0;

const caseLabel = USE_CAPS ? 'ALL CAPS' : 'lowercase';
console.log(`Generating Alice in Wonderland chapter booklets (${caseLabel})...\n`);

const bookletInfo = [];

for (const chNum of chapterNums) {
  const chapter = chapterMap[chNum];
  const chName = chapter.l2?.metadata?.original_title || chapter.scenes[0]?.metadata?.chapter_name || `Chapter ${chNum}`;
  const padNum = String(chNum).padStart(2, '0');
  const slug = chName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '');
  const filename = `chapter${padNum}-${slug}.html`;

  const { html, pageCount, illCount, textOnlyCount } = generateBookletHtml(chNum, chapter);
  writeFileSync(resolve(outputDir, filename), html);

  grandTotalPages += pageCount;
  grandTotalIll += illCount;

  const textOnly = textOnlyCount > 0 ? ` (${textOnlyCount} text-only)` : '';
  console.log(`  Ch ${padNum}: ${filename} — ${pageCount} pages, ${illCount} ill${textOnly}`);

  bookletInfo.push({ chNum, chName, filename, pageCount, illCount, coverImage: buildChapterPages(chapter).coverImage });
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
  <div class="grid">
${bookletInfo.map(b => `    <a class="card" href="${b.filename}">
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

console.log(`\nDone! 12 booklets, ${grandTotalPages} total pages, ${grandTotalIll} illustrations.`);
console.log(`Mode: ${caseLabel}. Use --lowercase flag for normal case.`);
