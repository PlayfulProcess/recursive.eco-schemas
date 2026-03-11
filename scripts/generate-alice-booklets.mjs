/**
 * Generate printable HTML booklets from the alice-in-wonderland-chapter-book grammar.
 *
 * One booklet per chapter. Original Carroll text in ALL CAPS.
 * Global reflow: entire chapter text split at sentence boundaries,
 * evenly distributed across ALL available illustrations (L1 + L2).
 *
 * Cover = L2 chapter illustration (not wasted on story).
 * Back cover = text-only "THE END" (no illustration wasted).
 * Text-only pages with decorative panels for illustration-sparse chapters.
 *
 * Usage: node scripts/generate-alice-booklets.mjs
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

const MAX_CHARS_PER_PAGE = 1200;

// ── Helpers ──────────────────────────────────────────────────────────

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function toAllCaps(text) {
  return text
    .replace(/_([^_]+)_/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .toUpperCase()
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/**
 * Format ALL CAPS text as proper HTML paragraphs.
 * Split on double newlines → <p> elements with margin.
 * Single newlines within paragraphs → spaces.
 */
function formatTextAsHtml(text) {
  const paragraphs = text.split(/\n\n+/).filter(p => p.trim());
  return paragraphs.map(p => {
    const cleaned = p.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
    return `<p>${escapeHtml(cleaned)}</p>`;
  }).join('\n          ');
}

/**
 * Get CSS class for font sizing based on character count.
 */
function fontSizeClass(charCount) {
  if (charCount < 400) return 'text-large';
  if (charCount < 700) return '';
  if (charCount < 1000) return 'text-medium';
  if (charCount < 1400) return 'text-small';
  return 'text-xs';
}

// ── Sentence Splitter ────────────────────────────────────────────────

const ABBREVIATIONS = new Set([
  'mr', 'mrs', 'ms', 'dr', 'st', 'sr', 'jr', 'vs', 'etc', 'vol',
  'i.e', 'e.g', 'fig', 'no', 'p', 'pp', 'ch',
]);

/**
 * Split text into sentences. Breaks only at sentence-ending punctuation
 * followed by whitespace + uppercase letter or paragraph boundary.
 */
function splitIntoSentences(text) {
  const normalized = text.replace(/\r\n/g, '\n').trim();
  const sentences = [];
  let current = '';
  let i = 0;

  while (i < normalized.length) {
    current += normalized[i];

    if ('.!?'.includes(normalized[i])) {
      // Look ahead past optional closing quotes
      let j = i + 1;
      while (j < normalized.length && '"\u201d\u201c\')\u2019'.includes(normalized[j])) {
        current += normalized[j];
        j++;
      }

      // Check for whitespace/newline after punctuation
      if (j >= normalized.length) {
        // End of text — this is a sentence end
        sentences.push(current.trim());
        current = '';
        i = j;
        continue;
      }

      if (/[\s\n]/.test(normalized[j])) {
        // Find next non-whitespace character
        let k = j;
        while (k < normalized.length && /[\s\n]/.test(normalized[k])) k++;

        if (k >= normalized.length || /[A-Z\u201c"(]/.test(normalized[k])) {
          // Check not an abbreviation
          const match = current.match(/\b(\w+)[.!?][\u201d"']*$/);
          const word = match ? match[1].toLowerCase() : '';
          if (!ABBREVIATIONS.has(word)) {
            sentences.push(current.trim());
            current = '';
            i = j;
            continue;
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
 * Returns array of text strings, each ending at a sentence boundary.
 */
function splitTextIntoPages(text, targetChars) {
  const sentences = splitIntoSentences(text);
  if (sentences.length === 0) return [''];

  const pages = [];
  let currentPage = '';

  for (const sentence of sentences) {
    const wouldBe = currentPage ? currentPage.length + 1 + sentence.length : sentence.length;

    // If adding this sentence would go over 1.3x target AND we already have enough content
    if (wouldBe > targetChars * 1.3 && currentPage.length > targetChars * 0.4) {
      pages.push(currentPage.trim());
      currentPage = sentence;
    } else {
      currentPage = currentPage ? currentPage + ' ' + sentence : sentence;
    }
  }
  if (currentPage.trim()) pages.push(currentPage.trim());
  return pages;
}

// ── Grammar Processing ───────────────────────────────────────────────

// Group L1 scenes and L2 chapters
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
// Sort scenes within each chapter
for (const ch of Object.values(chapterMap)) {
  ch.scenes.sort((a, b) => a.metadata.scene_number - b.metadata.scene_number);
}

/**
 * Build illustration pool for a chapter.
 * Returns { coverImage, storyPool: [{url, artist, scene}] }
 */
function buildIllustrationPool(chapter) {
  const l2 = chapter.l2;
  const coverImage = l2?.image_url || chapter.scenes[0]?.image_url || '';
  const coverUrl = coverImage; // Track to exclude from story pool

  const storyPool = [];
  const usedUrls = new Set([coverUrl]);

  // Add all L1 illustrations (in scene order, primary first)
  for (const scene of chapter.scenes) {
    const ills = scene.metadata?.illustrations || [];
    for (const ill of ills) {
      if (!usedUrls.has(ill.url)) {
        storyPool.push({
          url: ill.url,
          artist: ill.artist || '',
          scene: ill.scene || scene.name,
        });
        usedUrls.add(ill.url);
      }
    }
  }

  // Add L2 non-primary illustrations as bonus
  if (l2?.metadata?.illustrations) {
    for (const ill of l2.metadata.illustrations) {
      if (!ill.is_primary && !usedUrls.has(ill.url)) {
        storyPool.push({
          url: ill.url,
          artist: ill.artist || '',
          scene: ill.scene || '',
        });
        usedUrls.add(ill.url);
      }
    }
  }

  return { coverImage, storyPool };
}

/**
 * Concatenate all "Story (Original Text)" from a chapter's scenes.
 */
function concatenateChapterText(scenes) {
  const parts = [];
  for (const scene of scenes) {
    const text = scene.sections['Story (Original Text)'] || '';
    if (text.trim()) parts.push(text.trim());
  }
  return parts.join('\n\n');
}

// ── HTML Generation ──────────────────────────────────────────────────

function generateBookletHtml(chNum, chapter) {
  const { coverImage, storyPool } = buildIllustrationPool(chapter);
  const rawText = concatenateChapterText(chapter.scenes);
  const capsText = toAllCaps(rawText);
  const chName = chapter.l2?.metadata?.original_title || chapter.scenes[0]?.metadata?.chapter_name || `Chapter ${chNum}`;

  // Calculate target chars per page
  const totalChars = capsText.length;
  const numIllustrations = storyPool.length;
  let targetChars = numIllustrations > 0 ? Math.ceil(totalChars / numIllustrations) : totalChars;
  if (targetChars > MAX_CHARS_PER_PAGE) targetChars = MAX_CHARS_PER_PAGE;

  // Split text into pages at sentence boundaries
  const textPages = splitTextIntoPages(capsText, targetChars);

  // Assign illustrations to pages
  // If more pages than illustrations, some pages are text-only
  // Distribute illustrations evenly
  const pages = [];
  if (numIllustrations >= textPages.length) {
    // More illustrations than text pages — one per page, extras dropped
    for (let i = 0; i < textPages.length; i++) {
      pages.push({ text: textPages[i], illustration: storyPool[i] || null });
    }
  } else {
    // More text pages than illustrations — spread illustrations evenly
    const stride = textPages.length / numIllustrations;
    const assignedSlots = new Set();
    for (let i = 0; i < numIllustrations; i++) {
      assignedSlots.add(Math.round(i * stride));
    }
    let illIdx = 0;
    for (let i = 0; i < textPages.length; i++) {
      if (assignedSlots.has(i) && illIdx < numIllustrations) {
        pages.push({ text: textPages[i], illustration: storyPool[illIdx] });
        illIdx++;
      } else {
        pages.push({ text: textPages[i], illustration: null });
      }
    }
  }

  // Build HTML
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
          <div class="page-info">${pages.length} PAGES &middot; ${numIllustrations} ILLUSTRATIONS</div>
        </div>
      </div>
    </div>`;

  // Story pages
  for (let i = 0; i < pages.length; i++) {
    const page = pages[i];
    const textHtml = formatTextAsHtml(page.text);
    const sizeClass = fontSizeClass(page.text.length);
    const pageNum = i + 1;

    if (page.illustration) {
      // Illustrated page
      spreadsHtml += `
    <div class="spread">
      <div class="page-left">
        <img src="${page.illustration.url}" alt="${escapeHtml(page.illustration.scene)}">
      </div>
      <div class="page-right">
        <div class="text-block ${sizeClass}">
          ${textHtml}
        </div>
        <div class="page-number">${pageNum}</div>
      </div>
    </div>`;
    } else {
      // Text-only page with decorative left panel
      spreadsHtml += `
    <div class="spread text-only">
      <div class="page-left decorative-panel">
        <div class="chapter-ornament">
          <div class="ornament-number">${chNum}</div>
        </div>
      </div>
      <div class="page-right">
        <div class="text-block ${sizeClass}">
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

  return { html: wrapHtml(chNum, chName, spreadsHtml), pageCount: pages.length, illCount: numIllustrations, textOnlyCount: pages.filter(p => !p.illustration).length };
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
      font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
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
      align-items: center;
      justify-content: center;
      padding: 28px 36px;
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
    .text-block p {
      font-size: clamp(14px, 2.0vw, 22px);
      line-height: 1.7;
      font-weight: 700;
      text-align: left;
      letter-spacing: 0.3px;
      margin-bottom: 0.7em;
    }
    .text-block p:last-child { margin-bottom: 0; }

    /* Font size tiers */
    .text-block.text-large p {
      font-size: clamp(18px, 2.5vw, 28px);
      line-height: 1.8;
    }
    .text-block.text-medium p {
      font-size: clamp(12px, 1.6vw, 18px);
      line-height: 1.6;
    }
    .text-block.text-small p {
      font-size: clamp(11px, 1.4vw, 16px);
      line-height: 1.5;
    }
    .text-block.text-xs p {
      font-size: clamp(10px, 1.2vw, 14px);
      line-height: 1.4;
    }

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
    .title-block { text-align: center; }
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
    .back-block { text-align: center; }
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

    /* Screen: page dividers */
    @media screen {
      .spread {
        border-bottom: 3px dashed #ccc;
        min-height: 100vh;
      }
      .spread:last-child { border-bottom: none; }
      body { background: #e8e8e8; }
    }
  </style>
</head>
<body>
${spreadsHtml}
</body>
</html>`;
}

// ── Generate All Booklets ────────────────────────────────────────────

const chapterNums = Object.keys(chapterMap).map(Number).sort((a, b) => a - b);
let grandTotalPages = 0;
let grandTotalIll = 0;

console.log('Generating Alice in Wonderland chapter booklets...\n');

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
  console.log(`  Ch ${padNum}: ${filename} — ${pageCount} pages, ${illCount} illustrations${textOnly}`);

  bookletInfo.push({ chNum, chName, filename, pageCount, illCount, coverImage: buildIllustrationPool(chapter).coverImage });
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
      font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
      background: #f8f5f0;
      color: #2c1810;
      padding: 40px 20px;
    }
    h1 { text-align: center; font-size: 28px; margin-bottom: 6px; letter-spacing: 2px; }
    .subtitle { text-align: center; font-size: 13px; color: #888; margin-bottom: 10px; letter-spacing: 1px; }
    .description {
      text-align: center; font-size: 14px; color: #666; margin-bottom: 30px;
      max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.5;
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
  <div class="subtitle">ILLUSTRATED CHAPTER BOOKS — ALL CAPS EDITION</div>
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
console.log(`\nDone! 12 booklets, ${grandTotalPages} total pages, ${grandTotalIll} illustrations.`);
