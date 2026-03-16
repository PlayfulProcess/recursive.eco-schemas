/**
 * Generate a UNIFIED single-page book of Alice in Wonderland.
 *
 * Combines all 12 chapters into one continuous HTML with:
 *   - Book cover spread
 *   - Chapter divider spreads
 *   - Content spreads (illustration + text)
 *   - Chained audio: 12 MP3 files played sequentially
 *   - Karaoke word highlights synced across all chapters
 *   - Chapter navigation sidebar
 *   - Right-click illustration editing (move, swap, remove, export CSV)
 *
 * Usage:
 *   node scripts/generate-alice-book.mjs              # ALL CAPS
 *   node scripts/generate-alice-book.mjs --lowercase   # Normal case
 *   node scripts/generate-alice-book.mjs --remap       # Use custom illustration assignments
 *
 * Output: grammars/alice-5-minute-stories/booklets/book.html
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
const MAX_CHARS_PER_PAGE = 1000;

// ── Remap: load user-edited illustration assignments ────────────────
let remapData = null;
if (USE_REMAP) {
  const remapPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-assignments.json');
  if (existsSync(remapPath)) {
    remapData = JSON.parse(readFileSync(remapPath, 'utf8'));
    console.log(`--remap: loaded ${remapData.length} illustration assignments`);
  } else {
    console.error('--remap: illustration-assignments.json not found!');
    process.exit(1);
  }
}

// ── Helpers ──────────────────────────────────────────────────────────

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function transformCase(text) {
  let t = text
    .replace(/_([^_]+)_/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  // Break dialogue into separate paragraphs for children's readability.
  // Key insight: break BETWEEN complete dialogue units, not inside them.
  //
  // A dialogue unit is: "quoted speech" said Character, ending punct.
  // We want a paragraph break AFTER a complete unit, BEFORE the next opening quote.
  //
  // Pattern: closing-quote + attribution + sentence-end → \n\n before next opening-quote
  // Examples:
  //   "No, no!" said the Queen. ¶ "Sentence first..."
  //   "I won't!" said Alice. ¶ "Off with her head!"
  //   everybody laughed. ¶ "Let the jury..."

  // 1. After closing-quote + attribution + period/comma → break before opening quote
  //    Matches: ..." said the Queen. "...  or  ...!" said Alice. "...
  t = t.replace(/(["'\u201D])\s+([^""\u201C]*?[.!?,])\s*\n?\s*([""\u201C])/g, '$1 $2\n\n$3');

  // 2. Closing quote immediately followed by opening quote (no attribution)
  //    Matches: ...afterwards." "Stuff...  or  ...first!" "Hold...
  t = t.replace(/([.!?,]["'\u201D])\s*\n?\s*([""\u201C])/g, '$1\n\n$2');

  // 3. Narration ending in period → break before opening quote
  //    Matches: ...everybody laughed. "Let...  or  ...Nobody moved. "Who...
  t = t.replace(/([.!?])\s+\n?\s*([""\u201C])/g, '$1\n\n$2');

  // 4. After semicolon → break before opening quote (Carroll's style)
  t = t.replace(/(;\s*)\n?\s*([""\u201C])/g, '$1\n\n$2');

  // Clean up triple+ newlines
  t = t.replace(/\n{3,}/g, '\n\n');

  return t;
}

function formatTextAsHtml(text) {
  const paragraphs = text.split(/\n\n+/).filter(p => p.trim());
  return paragraphs.map(p => {
    let cleaned = p.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
    return `<p>${escapeHtml(cleaned)}</p>`;
  }).join('\n          ');
}

// ── Sentence Splitter ────────────────────────────────────────────────

const ABBREVIATIONS = new Set([
  'mr', 'mrs', 'ms', 'dr', 'st', 'sr', 'jr', 'vs', 'etc', 'vol', 'fig', 'no', 'ch',
]);

const ATTRIBUTION_VERBS = new Set([
  'said', 'thought', 'cried', 'asked', 'replied', 'exclaimed', 'remarked',
  'whispered', 'shouted', 'continued', 'added', 'muttered', 'began',
  'answered', 'observed', 'repeated', 'returned', 'suggested', 'grumbled',
  'growled', 'sighed', 'sobbed', 'shrieked', 'screamed', 'panted',
  'interrupted', 'went', 'called', 'sang', 'recited', 'read', 'roared',
]);

function splitIntoSentences(text) {
  const normalized = text.replace(/\r\n/g, '\n').trim();
  const sentences = [];
  let current = '';
  let i = 0;

  while (i < normalized.length) {
    current += normalized[i];

    if ('.!?'.includes(normalized[i])) {
      let j = i + 1;
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

        const hasParaBreak = normalized.slice(j, k).includes('\n\n');
        if (k >= normalized.length || hasParaBreak || /[A-Z\u201c"(]/.test(normalized[k])) {
          const match = current.match(/\b(\w+)[.!?][\u201d"'\u2019)]*$/);
          const word = match ? match[1].toLowerCase() : '';
          if (!ABBREVIATIONS.has(word)) {
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

function splitTextIntoPages(text, targetChars) {
  const sentences = splitIntoSentences(text);
  if (sentences.length === 0) return [''];

  // Detect paragraph starts
  const paraStarts = new Set();
  let searchPos = 0;
  for (let si = 0; si < sentences.length; si++) {
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

  // Calculate total length to determine ideal page count
  const totalLen = sentences.reduce((sum, s) => sum + s.length, 0);
  const idealPageCount = Math.max(1, Math.round(totalLen / targetChars));
  const idealPerPage = totalLen / idealPageCount;

  const pages = [];
  let currentPage = '';

  for (let si = 0; si < sentences.length; si++) {
    const sentence = sentences[si];
    const joiner = currentPage ? (paraStarts.has(si) ? '\n\n' : ' ') : '';
    const wouldBe = currentPage.length + joiner.length + sentence.length;
    const remaining = sentences.slice(si).reduce((sum, s) => sum + s.length, 0);
    const pagesLeft = idealPageCount - pages.length;

    // Split when current page is near ideal size, but always at sentence boundaries
    // Prefer paragraph boundaries for splits
    const shouldSplit = currentPage.length > 0 && pagesLeft > 1 && (
      // Exceeded target — must split
      (wouldBe > targetChars * 1.1) ||
      // Near target and at a paragraph boundary — good place to split
      (wouldBe > idealPerPage * 0.85 && paraStarts.has(si)) ||
      // Well past ideal and more pages to fill
      (currentPage.length >= idealPerPage * 1.05 && remaining > idealPerPage * 0.5)
    );

    if (shouldSplit) {
      pages.push(currentPage.trim());
      currentPage = sentence;
    } else {
      currentPage = currentPage + joiner + sentence;
    }
  }
  if (currentPage.trim()) pages.push(currentPage.trim());

  // Safety: if any page is still way too long, re-split it
  const result = [];
  for (const page of pages) {
    if (page.length <= targetChars * 1.15) {
      result.push(page);
    } else {
      // Emergency re-split at sentence boundaries
      const pageSentences = splitIntoSentences(page);
      let chunk = '';
      for (const s of pageSentences) {
        if (chunk && chunk.length + s.length + 1 > targetChars) {
          result.push(chunk.trim());
          chunk = s;
        } else {
          chunk = chunk ? chunk + ' ' + s : s;
        }
      }
      if (chunk.trim()) result.push(chunk.trim());
    }
  }

  // Merge very short last pages back into the previous page
  if (result.length > 1 && result[result.length - 1].length < idealPerPage * 0.3) {
    const lastPage = result.pop();
    result[result.length - 1] += '\n\n' + lastPage;
  }

  return result;
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

function buildChapterPages(chapter) {
  const l2 = chapter.l2;
  const coverImage = l2?.image_url || chapter.scenes[0]?.image_url || '';
  const usedUrls = new Set([coverImage]);

  let totalChars = 0;
  let totalIlls = 0;
  for (const scene of chapter.scenes) {
    const text = scene.sections['Story (Original Text)'] || '';
    totalChars += text.length;
    const ills = (scene.metadata?.illustrations || []).filter(ill => ill.url !== coverImage);
    totalIlls += ills.length;
  }
  const l2Extras = (l2?.metadata?.illustrations || []).filter(ill => !ill.is_primary && ill.url !== coverImage);
  totalIlls += l2Extras.length;

  let targetChars = totalIlls > 0 ? Math.ceil(totalChars / totalIlls) : totalChars;
  if (targetChars > MAX_CHARS_PER_PAGE) targetChars = MAX_CHARS_PER_PAGE;

  const pages = [];
  const bonusPool = [];

  for (const scene of chapter.scenes) {
    const rawText = scene.sections['Story (Original Text)'] || '';
    if (!rawText.trim()) continue;

    const text = transformCase(rawText);
    const sceneIlls = getSceneIllustrations(scene, usedUrls);
    const textPages = splitTextIntoPages(text, targetChars);

    if (sceneIlls.length >= textPages.length) {
      for (let i = 0; i < textPages.length; i++) {
        pages.push({ text: textPages[i], illustration: sceneIlls[i] });
      }
      for (let i = textPages.length; i < sceneIlls.length; i++) {
        bonusPool.push(sceneIlls[i]);
      }
    } else {
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

  for (const ill of l2Extras) {
    if (!usedUrls.has(ill.url)) {
      bonusPool.push(ill);
      usedUrls.add(ill.url);
    }
  }

  let bonusIdx = 0;
  for (let i = 0; i < pages.length && bonusIdx < bonusPool.length; i++) {
    if (!pages[i].illustration && pages[i].text) {
      pages[i].illustration = bonusPool[bonusIdx];
      bonusIdx++;
    }
  }

  return { coverImage, pages };
}

function applyRemap(chNum, coverImage, pages) {
  if (!remapData) return { coverImage, pages };

  const chapterAssignments = remapData.filter(a => a.chapter === chNum);

  const coverAssign = chapterAssignments.find(a => a.page === 0);
  if (coverAssign && coverAssign.image_url) {
    coverImage = coverAssign.image_url;
  }

  for (const assign of chapterAssignments) {
    if (assign.page === 0) continue;
    const pageIdx = assign.page - 1;
    if (pageIdx >= 0 && pageIdx < pages.length) {
      if (assign.image_url) {
        pages[pageIdx].illustration = {
          url: assign.image_url,
          scene: assign.image_info || '',
          artist: '',
        };
      } else {
        pages[pageIdx].illustration = null;
      }
    }
  }

  return { coverImage, pages };
}

// ── Load Karaoke Manifest ────────────────────────────────────────────
// Prefer unified manifest (absolute timestamps for merged audio) over per-chapter

const unifiedManifestPath = resolve(__dirname, '../grammars/alice-5-minute-stories/audio/librivox/karaoke-manifest-unified.json');
const perChapterManifestPath = resolve(__dirname, '../grammars/alice-5-minute-stories/audio/librivox/karaoke-manifest.json');
let karaokeManifest = null;
let isUnifiedAudio = false;

if (existsSync(unifiedManifestPath)) {
  karaokeManifest = JSON.parse(readFileSync(unifiedManifestPath, 'utf8'));
  isUnifiedAudio = true;
  console.log('Unified karaoke manifest loaded (single audio file).\n');
} else if (existsSync(perChapterManifestPath)) {
  karaokeManifest = JSON.parse(readFileSync(perChapterManifestPath, 'utf8'));
  console.log('Per-chapter karaoke manifest loaded.\n');
}

// ── Build All Chapters ───────────────────────────────────────────────

const chapterNums = Object.keys(chapterMap).map(Number).sort((a, b) => a - b);

const allChaptersData = [];
let globalPageNum = 0;
let totalIll = 0;
let totalContentPages = 0;

// Book cover image
const bookCoverImage = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/chapter-01-down-the-rabbit-hole/arthur-rackham-1907.jpg';

// Build book cover spread
globalPageNum++;
let spreadsHtml = `
    <div class="spread cover-spread book-cover" data-spread="book-cover" id="book-cover">
      <div class="page-left cover-image" data-page="${globalPageNum}">
        <img src="${bookCoverImage}" alt="Alice in Wonderland — Arthur Rackham illustration">
      </div>`;
globalPageNum++;
spreadsHtml += `
      <div class="page-right cover-title" data-page="${globalPageNum}">
        <div class="title-block">
          <div class="ornament">&#10048; &#10048; &#10048;</div>
          <h1>ALICE'S<br>ADVENTURES<br>IN WONDERLAND</h1>
          <div class="author">LEWIS CARROLL</div>
          <div class="edition">
            ILLUSTRATED CHAPTER BOOKS<br>
            TENNIEL &middot; RACKHAM &middot; CARROLL &middot; HUDSON &amp; MORE
          </div>
        </div>
        <div class="page-number page-number-right">${globalPageNum}</div>
      </div>
    </div>`;

// ── Preface: "All in the Golden Afternoon" ───────────────────────────

// Load poem whisper timestamps if available (for karaoke)
const poemWhisperPath = resolve(__dirname, '../grammars/alice-5-minute-stories/audio/poem-whisper.json');
let poemWhisperWords = null;
if (existsSync(poemWhisperPath)) {
  const pw = JSON.parse(readFileSync(poemWhisperPath, 'utf8'));
  poemWhisperWords = pw.words || [];
  console.log(`Poem whisper loaded: ${poemWhisperWords.length} words`);
}

// Align whisper words to poem text using simple sequential matching
function alignPoemWord(displayWord, whisperWords, cursor) {
  const clean = displayWord.toLowerCase().replace(/[^a-z']/g, '');
  if (!clean) return { start: 0, end: 0, cursor: cursor }; // punctuation-only
  for (let i = cursor; i < Math.min(cursor + 10, whisperWords.length); i++) {
    const wClean = whisperWords[i].word.toLowerCase().replace(/[^a-z']/g, '');
    if (wClean === clean || wClean.startsWith(clean) || clean.startsWith(wClean)) {
      return { start: whisperWords[i].start, end: whisperWords[i].end, cursor: i + 1 };
    }
  }
  // Not found — skip ahead and try to resync
  return { start: 0, end: 0, cursor: cursor };
}

// Carroll's dedicatory poem, split across 3 spreads (7 stanzas → ~2-3 per spread)
const poemStanzas = [
  [
    'All in the golden afternoon',
    'Full leisurely we glide;',
    'For both our oars, with little skill,',
    'By little arms are plied,',
    'While little hands make vain pretence',
    'Our wanderings to guide.',
  ],
  [
    'Ah, cruel Three! In such an hour,',
    'Beneath such dreamy weather,',
    'To beg a tale of breath too weak',
    'To stir the tiniest feather!',
    'Yet what can one poor voice avail',
    'Against three tongues together?',
  ],
  [
    'Imperious Prima flashes forth',
    "Her edict 'to begin it' \u2013",
    'In gentler tone Secunda hopes',
    "'There will be nonsense in it!' \u2013",
    'While Tertia interrupts the tale',
    'Not more than once a minute.',
  ],
  [
    'Anon, to sudden silence won,',
    'In fancy they pursue',
    'The dream-child moving through a land',
    'Of wonders wild and new,',
    'In friendly chat with bird or beast \u2013',
    'And half believe it true.',
  ],
  [
    'And ever, as the story drained',
    'The wells of fancy dry,',
    'And faintly strove that weary one',
    'To put the subject by,',
    '\u201cThe rest next time \u2013\u201d \u201cIt is next time!\u201d',
    'The happy voices cry.',
  ],
  [
    'Thus grew the tale of Wonderland:',
    'Thus slowly, one by one,',
    'Its quaint events were hammered out \u2013',
    'And now the tale is done,',
    'And home we steer, a merry crew,',
    'Beneath the setting sun.',
  ],
  [
    'Alice! a childish story take,',
    'And with a gentle hand',
    "Lay it where Childhood's dreams are twined",
    "In Memory's mystic band,",
    "Like pilgrim's wither'd wreath of flowers",
    "Pluck'd in a far-off land.",
  ],
];

// Preface illustration — use the manuscript frontispiece (dedication page)
const prefaceImage = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/manuscript-under-ground/manuscript-page-00.jpg';

// Split poem into 3 spreads: stanzas 1-2, 3-4, 5-7
const poemGroups = [
  { stanzas: [0, 1], title: 'ALL IN THE GOLDEN AFTERNOON' },
  { stanzas: [2, 3] },
  { stanzas: [4, 5, 6] },
];

// Pre-align all poem words to whisper timestamps
let poemWordCursor = 0;
const poemAligned = []; // [stanzaIdx][lineIdx] = [{word, start, end}]
for (let si = 0; si < poemStanzas.length; si++) {
  poemAligned[si] = [];
  for (let li = 0; li < poemStanzas[si].length; li++) {
    const lineWords = poemStanzas[si][li].split(/\s+/);
    poemAligned[si][li] = [];
    for (const w of lineWords) {
      if (poemWhisperWords) {
        const result = alignPoemWord(w, poemWhisperWords, poemWordCursor);
        poemAligned[si][li].push({ word: w, start: result.start, end: result.end });
        if (result.cursor > poemWordCursor) poemWordCursor = result.cursor;
      } else {
        poemAligned[si][li].push({ word: w, start: 0, end: 0 });
      }
    }
  }
}

for (let gi = 0; gi < poemGroups.length; gi++) {
  const group = poemGroups[gi];
  const stanzaHtml = group.stanzas.map(si => {
    return '<div class="poem-stanza">' +
      poemStanzas[si].map((line, li) => {
        if (poemWhisperWords) {
          // Wrap each word in k-word span with timestamps
          const wordSpans = poemAligned[si][li].map(w => {
            if (w.start > 0 || w.end > 0) {
              return '<span class="k-word" data-start="' + w.start.toFixed(2) + '" data-end="' + w.end.toFixed(2) + '">' + escapeHtml(w.word) + '</span>';
            }
            return escapeHtml(w.word);
          }).join(' ');
          return '<div class="poem-line">' + wordSpans + '</div>';
        }
        return '<div class="poem-line">' + escapeHtml(line) + '</div>';
      }).join('\n') +
      '</div>';
  }).join('\n');

  globalPageNum++;
  if (gi === 0) {
    // First spread: manuscript image left, poem title + first stanzas right
    spreadsHtml += `
    <div class="spread preface-spread" data-spread="preface-${gi + 1}" id="preface">
      <div class="page-left cover-image" data-page="${globalPageNum}">
        <img src="${prefaceImage}" alt="Carroll manuscript dedication">
        <div class="page-number page-number-left">${globalPageNum}</div>
      </div>`;
  } else {
    // Subsequent spreads: decorative left
    spreadsHtml += `
    <div class="spread preface-spread" data-spread="preface-${gi + 1}">
      <div class="page-left decorative-panel" data-page="${globalPageNum}">
        <div class="chapter-ornament">
          <div class="ornament-star">&#10048;</div>
        </div>
        <div class="page-number page-number-left">${globalPageNum}</div>
      </div>`;
  }

  globalPageNum++;
  const titleHtml = group.title
    ? '<div class="poem-title">' + escapeHtml(group.title) + '</div>'
    : '';
  const playHint = gi === 0
    ? '<div class="poem-play-hint" id="poemPlayHint">&#9835; click to play song</div>'
    : '';

  spreadsHtml += `
      <div class="page-right preface-text" data-page="${globalPageNum}">
        <div class="poem-block">
          ${titleHtml}
          ${stanzaHtml}
          ${playHint}
        </div>
        <div class="page-number page-number-right">${globalPageNum}</div>
      </div>
    </div>`;
}

// Build all chapters
for (const chNum of chapterNums) {
  const chapter = chapterMap[chNum];
  let { coverImage, pages } = buildChapterPages(chapter);

  if (USE_REMAP) {
    ({ coverImage, pages } = applyRemap(chNum, coverImage, pages));
  }

  const chName = chapter.l2?.metadata?.original_title || chapter.scenes[0]?.metadata?.chapter_name || `Chapter ${chNum}`;
  const illCount = pages.filter(p => p.illustration).length;

  // Track the first text page number for karaoke offset
  // Chapter divider uses 2 pages, then each content page pair uses 2 pages
  const chapterStartPage = globalPageNum + 1; // first page of the divider

  // Chapter divider spread
  globalPageNum++;
  spreadsHtml += `
    <div class="spread cover-spread chapter-divider" data-spread="ch${chNum}-cover" id="ch${chNum}">
      <div class="page-left cover-image" data-page="${globalPageNum}">
        <img src="${coverImage}" alt="Chapter ${chNum} cover">
        <div class="page-number page-number-left">${globalPageNum}</div>
      </div>`;
  globalPageNum++;
  spreadsHtml += `
      <div class="page-right cover-title" data-page="${globalPageNum}">
        <div class="title-block">
          <div class="series-name">ALICE IN WONDERLAND</div>
          <div class="book-number">CHAPTER ${chNum}</div>
          <h1>${escapeHtml(chName.toUpperCase())}</h1>
          <div class="author">BY LEWIS CARROLL</div>
          <div class="page-info">${pages.length} PAGES</div>
        </div>
        <div class="page-number page-number-right">${globalPageNum}</div>
      </div>
    </div>`;

  // Content spreads — track which global page number each text page gets
  const pageNumMap = {}; // booklet-local page (1-based) → global page number

  for (let i = 0; i < pages.length; i++) {
    const page = pages[i];
    const textHtml = formatTextAsHtml(page.text);
    const spreadIdx = `ch${chNum}-${i + 1}`;

    // Left page: illustration or decorative
    globalPageNum++;
    if (page.illustration) {
      spreadsHtml += `
    <div class="spread" data-spread="${spreadIdx}" data-ch="${chNum}">
      <div class="page-left" data-page="${globalPageNum}" data-ch="${chNum}" data-local-page="${i + 1}">
        <img src="${page.illustration.url}" alt="${escapeHtml(page.illustration.scene || '')}" data-ch="${chNum}" data-pg="${i + 1}">
        <div class="page-number page-number-left">${globalPageNum}</div>
      </div>`;
    } else {
      spreadsHtml += `
    <div class="spread text-only" data-spread="${spreadIdx}" data-ch="${chNum}">
      <div class="page-left decorative-panel" data-page="${globalPageNum}" data-ch="${chNum}" data-local-page="${i + 1}">
        <div class="chapter-ornament">
          <div class="ornament-number">${chNum}</div>
        </div>
        <div class="page-number page-number-left">${globalPageNum}</div>
      </div>`;
    }

    // Right page: text
    globalPageNum++;
    // The booklet's karaoke references page numbers in the booklet's numbering
    // In per-chapter booklets, content pages start at page 4 (cover=1,2, first-ill=3, first-text=4)
    // So booklet page number for text = 2 * (i+1) + 2 = 2i + 4
    const bookletPageNum = 2 * (i + 1) + 2; // pages 4, 6, 8, ...
    pageNumMap[bookletPageNum] = globalPageNum;

    spreadsHtml += `
      <div class="page-right" data-page="${globalPageNum}" data-ch="${chNum}" data-local-page="${i + 1}">
        <div class="text-block">
          ${textHtml}
        </div>
        <div class="page-number page-number-right">${globalPageNum}</div>
      </div>
    </div>`;
  }

  totalIll += illCount;
  totalContentPages += pages.length;

  // Get karaoke data and remap page numbers to global
  let karaokeData = karaokeManifest?.chapters?.[chNum] || null;
  let remappedKaraokePages = null;
  if (karaokeData) {
    remappedKaraokePages = karaokeData.pages.map(p => ({
      ...p,
      pageNum: pageNumMap[p.pageNum] || p.pageNum,
    })).filter(p => pageNumMap[p.pageNum] !== undefined || Object.values(pageNumMap).includes(p.pageNum));
  }

  allChaptersData.push({
    chNum,
    chName,
    coverImage,
    pageCount: pages.length,
    illCount,
    pages,
    audioFile: karaokeData?.audio_file || null,
    karaokePages: remappedKaraokePages,
    pageNumMap,
  });
}

// Final spread: THE END
globalPageNum++;
spreadsHtml += `
    <div class="spread back-cover" data-spread="the-end" id="the-end">
      <div class="page-left decorative-panel" data-page="${globalPageNum}">
        <div class="chapter-ornament">
          <div class="ornament-star">&#10038;</div>
        </div>
        <div class="page-number page-number-left">${globalPageNum}</div>
      </div>`;
globalPageNum++;
spreadsHtml += `
      <div class="page-right back-text" data-page="${globalPageNum}">
        <div class="back-block">
          <div class="the-end">THE END</div>
          <div class="back-info">
            <p>ALICE'S ADVENTURES IN WONDERLAND</p>
            <p class="small">WORDS BY LEWIS CARROLL (1865)</p>
            <p class="small">${totalIll} ILLUSTRATIONS &middot; ALL PUBLIC DOMAIN</p>
            <p class="small">TENNIEL &middot; RACKHAM &middot; CARROLL &middot; HUDSON &amp; MORE</p>
            <p class="small">MADE WITH LOVE AT RECURSIVE.ECO</p>
          </div>
        </div>
        <div class="page-number page-number-right">${globalPageNum}</div>
      </div>
    </div>`;

// ── Build Audio Data ─────────────────────────────────────────────────

const R2_AUDIO_BASE = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/audio/librivox';

let audioDataJson;

if (isUnifiedAudio) {
  // Unified mode: single audio file, absolute timestamps
  const allPages = allChaptersData.flatMap(ch => ch.karaokePages || []);
  const chapterOffsets = Object.values(karaokeManifest.chapters).map(ch => ({
    chapter: ch.chapter,
    offset: ch.offset,
    duration: ch.duration,
  }));

  const audioData = {
    url: `${R2_AUDIO_BASE}/${karaokeManifest.audio_file}`,
    totalDuration: karaokeManifest.total_duration_s,
    chapters: chapterOffsets,
    pages: allPages,
  };

  audioDataJson = JSON.stringify(audioData);
  console.log(`  Audio: unified (${karaokeManifest.audio_file}, ${(karaokeManifest.total_duration_s / 60).toFixed(1)} min)`);
} else {
  // Per-chapter mode (legacy): separate audio files
  const audioChapters = allChaptersData
    .filter(ch => ch.audioFile)
    .map(ch => ({
      chapter: ch.chNum,
      audio_file: `${R2_AUDIO_BASE}/${ch.audioFile}`,
      pages: ch.karaokePages || [],
    }));

  audioDataJson = JSON.stringify(audioChapters);
  console.log(`  Audio: per-chapter (${audioChapters.length} files)`);
}

// ── Build Chapter Nav Data ───────────────────────────────────────────

const chapterNavItems = allChaptersData.map(ch => ({
  num: ch.chNum,
  name: ch.chName,
  id: `ch${ch.chNum}`,
  pages: ch.pageCount,
  ills: ch.illCount,
}));
const chapterNavJson = JSON.stringify(chapterNavItems);

// ── Build Illustration Data (for editor) ─────────────────────────────

// Load booklet grammar for text previews
const bookletGrammarPath = resolve(__dirname, '../grammars/alice-5-minute-stories/grammar.json');
let bookletTextData = {};
if (existsSync(bookletGrammarPath)) {
  const bookletGrammar = JSON.parse(readFileSync(bookletGrammarPath, 'utf8'));
  for (const item of bookletGrammar.items) {
    const ch = item.metadata?.source_chapter;
    if (!ch) continue;
    bookletTextData[ch] = { name: item.name, pages: {} };
    for (let p = 1; p <= (item.metadata?.page_count || 0); p++) {
      bookletTextData[ch].pages[p] = (item.sections?.[`Page ${p}`] || '').substring(0, 120);
    }
  }
}

const illustrationData = [];
// Collect ALL unique illustration URLs used so we can show unused ones
const usedIllUrls = new Set();
// Collect ALL available illustration URLs from grammar
const allAvailableIlls = [];

for (const ch of allChaptersData) {
  illustrationData.push({
    ch: ch.chNum,
    pg: 0,
    url: ch.coverImage,
    info: 'chapter cover',
    label: `Ch${ch.chNum} Cover`,
    text: ch.chName,
  });
  if (ch.coverImage) usedIllUrls.add(ch.coverImage);

  for (let i = 0; i < ch.pages.length; i++) {
    const p = ch.pages[i];
    const fullText = p.text.replace(/\n/g, ' ').trim();
    illustrationData.push({
      ch: ch.chNum,
      pg: i + 1,
      url: p.illustration ? p.illustration.url : '',
      info: p.illustration ? `${p.illustration.artist || ''} — ${p.illustration.scene || ''}`.trim() : 'text-only',
      label: `Ch${ch.chNum} p${i + 1}`,
      text: fullText,
    });
    if (p.illustration && p.illustration.url) usedIllUrls.add(p.illustration.url);
  }
}

// Gather all available illustration URLs from the grammar
for (const item of grammar.items) {
  if (!item.metadata?.illustrations) continue;
  for (const ill of item.metadata.illustrations) {
    if (ill.url && !usedIllUrls.has(ill.url)) {
      allAvailableIlls.push({
        url: ill.url,
        info: `${ill.artist || ''} — ${ill.scene || ill.alt || ''}`.trim(),
        source: item.name,
      });
    }
  }
}

// Add Alice Liddell real photos (uploaded to R2) to the pool
const aliceLiddellPhotos = [
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/alice-liddell-portrait.jpg', info: 'Lewis Carroll (photograph) — Alice Liddell portrait', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/alice-feigned-sleep-1860.jpg', info: 'Lewis Carroll (photograph) — Alice in feigned sleep, 1860', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/edith-ina-alice-july-1860.jpg', info: 'Lewis Carroll (photograph) — Edith, Ina and Alice, July 1860', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/lorina-edith-alice-1859.jpg', info: 'Lewis Carroll (photograph) — Lorina, Edith and Alice, 1859', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/alice-ina-harry-edith-1860.jpg', info: 'Lewis Carroll (photograph) — Alice, Ina, Harry and Edith, 1860', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/alice-beggar-girl-1858.jpg', info: 'Lewis Carroll (photograph) — Alice as a beggar-girl, 1858', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/alice-liddell-1859.jpg', info: 'Lewis Carroll (photograph) — Alice Liddell, 1859', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/alice-age-20-1872.jpg', info: 'Lewis Carroll (photograph) — A 20-year-old Alice, 1872', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/alice-with-julia-margaret-cameron-1872.jpg', info: 'Julia Margaret Cameron (photograph) — Alice with Cameron, 1872', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/alice-grown-up.jpg', info: 'Photograph — A grown up Alice of Wonderland', source: 'Real Alice Liddell' },
  { url: 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/alice-liddell-photos/alice-hargreaves-1932-age-80.jpg', info: 'Photograph — Alice Hargreaves in 1932, age 80', source: 'Real Alice Liddell' },
];
for (const photo of aliceLiddellPhotos) {
  if (!usedIllUrls.has(photo.url)) {
    allAvailableIlls.push(photo);
  }
}

const illustrationDataJson = JSON.stringify(illustrationData);
const unusedIllsJson = JSON.stringify(allAvailableIlls);

// ── Generate HTML ────────────────────────────────────────────────────

const bookHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alice's Adventures in Wonderland — Complete Illustrated Book</title>
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
      justify-content: center;
      padding: 32px 5% 32px 5%;
      background: white;
      position: relative;
      overflow: hidden;
      border-left: 2px solid #d0c8b8;
    }

    .text-block {
      display: flex;
      flex-direction: column;
      justify-content: center;
      width: 100%;
      overflow: hidden;
    }

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
    .text-block p:last-child { margin-bottom: 0; }

    .page-number {
      font-size: 11px;
      color: #999;
      position: absolute;
      bottom: 8px;
    }
    .page-number-left { left: 16px; }
    .page-number-right { right: 16px; }

    /* Blank pages */
    .blank-page { background: #faf8f5; }

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
    .edition {
      font-size: clamp(10px, 1.2vw, 14px);
      letter-spacing: 2px; color: #a08060;
      line-height: 1.8;
    }
    .ornament {
      font-size: 24px; color: #d4a76a; margin-bottom: 30px;
      letter-spacing: 8px;
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
      .chapter-nav { display: none !important; }
      .audio-progress { display: none !important; }
      mark.search-match { background: transparent !important; color: inherit !important; }
      .ctx-menu { display: none !important; }
      .zoom-overlay { display: none !important; }
    }

    /* ── Booklet Print Mode ── */
    body.booklet-mode .chapter-nav { display: none !important; }
    body.booklet-mode .audio-progress,
    body.booklet-mode #playBtn,
    body.booklet-mode #speedCtrl,
    body.booklet-mode #audioTime,
    body.booklet-mode #searchInput,
    body.booklet-mode #matchCount,
    body.booklet-mode #caseToggle,
    body.booklet-mode #fullscreenBtn,
    body.booklet-mode #navToggle { display: none !important; }
    body.booklet-mode .toolbar {
      background: #1a1a1a; justify-content: center; gap: 20px;
    }
    body.booklet-mode .toolbar .ch-title { display: none; }
    body.booklet-mode .spread {
      height: 100vh; border-bottom: none !important;
      page-break-inside: avoid; break-inside: avoid;
    }
    body.booklet-mode .page-left img { box-shadow: none; }

    /* ── Toolbar ── */
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
      width: 120px;
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

    /* Search highlight */
    .search-match { background: #ffd700 !important; color: #1a1a1a !important; border-radius: 2px; padding: 0 1px; }
    .search-current { background: #ff6b00 !important; color: white !important; border-radius: 2px; padding: 0 1px; }

    /* Karaoke */
    .k-word {
      transition: color 2.5s ease;
      border-radius: 2px;
      padding: 0 1px;
    }
    .k-word.k-spoken { color: #9a8a7a; transition: color 3s ease; }
    .k-word.k-active { color: #b89060; transition: color 1.5s ease; }
    .k-word.k-near { color: #8a7560; transition: color 2s ease; }

    /* Click-to-seek: k-word spans are clickable when audio is loaded */
    .k-word { cursor: pointer; }
    .k-word:hover { text-decoration-line: underline; text-decoration-style: dotted; text-underline-offset: 3px; }
    /* Touch device: add subtle underline hint so users know text is tappable */
    @media (pointer: coarse) {
      .k-word { text-decoration: underline dotted rgba(184, 144, 96, 0.2); text-underline-offset: 3px; }
      .k-word.k-active { text-decoration: none; }
      .k-word.k-spoken { text-decoration: none; }
    }
    /* Tap-to-play hint for touch devices */
    .tap-play-hint {
      position: fixed; bottom: 60px; left: 50%; transform: translateX(-50%);
      background: rgba(44, 24, 16, 0.9); color: #d4a76a;
      padding: 8px 20px; border-radius: 20px; font-size: 12px;
      letter-spacing: 1px; z-index: 80; pointer-events: none;
      opacity: 0; transition: opacity 0.5s;
    }
    .tap-play-hint.visible { opacity: 1; }

    /* Audio progress bar */
    .audio-progress {
      flex: 1;
      min-width: 80px;
      height: 6px;
      background: rgba(255,255,255,0.15);
      border-radius: 3px;
      cursor: pointer;
      position: relative;
    }
    .audio-progress-bar {
      height: 100%;
      background: #d4a76a;
      width: 0%;
      transition: width 0.3s linear;
      border-radius: 3px;
    }
    .audio-progress:hover { height: 8px; }

    /* Screen dividers */
    @media screen {
      .spread {
        border-bottom: 3px dashed #ccc;
        min-height: 100vh;
      }
      .spread:last-child { border-bottom: none; }
      body { background: #e8e8e8; padding-top: 44px; }
    }

    /* ── Chapter Navigation Sidebar ── */
    .chapter-nav {
      position: fixed;
      right: 0;
      top: 44px;
      bottom: 0;
      width: 280px;
      background: rgba(44, 24, 16, 0.95);
      color: #d4a76a;
      font-family: 'Georgia', serif;
      z-index: 90;
      overflow-y: auto;
      transform: translateX(100%);
      transition: transform 0.3s ease;
      padding: 20px 16px;
      box-shadow: -4px 0 20px rgba(0,0,0,0.3);
    }
    .chapter-nav.open { transform: translateX(0); }
    .chapter-nav h2 {
      font-size: 13px;
      letter-spacing: 2px;
      margin-bottom: 16px;
      color: #a08060;
    }
    .chapter-nav .nav-item {
      display: block;
      padding: 10px 12px;
      margin-bottom: 4px;
      border-radius: 6px;
      text-decoration: none;
      color: #d4a76a;
      font-size: 13px;
      transition: background 0.2s;
      cursor: pointer;
    }
    .chapter-nav .nav-item:hover { background: rgba(255,255,255,0.08); }
    .chapter-nav .nav-item.active { background: rgba(212,167,106,0.2); }
    .chapter-nav .nav-item .nav-num {
      font-size: 10px;
      letter-spacing: 2px;
      color: #a08060;
      display: block;
      margin-bottom: 2px;
    }
    .chapter-nav .nav-item .nav-name {
      font-weight: 700;
      font-size: 14px;
    }
    .chapter-nav .nav-item .nav-meta {
      font-size: 10px;
      color: #7a6050;
      margin-top: 2px;
    }

    /* ── Carousel / Zoom overlay ── */
    .zoom-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.97);
      z-index: 999; display: none; flex-direction: column;
      align-items: center; justify-content: center;
      font-family: Georgia, serif;
    }
    .zoom-overlay.active { display: flex; }
    .zoom-overlay img {
      max-width: 90vw; max-height: 75vh; object-fit: contain;
      transition: opacity 0.15s;
    }
    .carousel-info {
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      color: #d4a76a; font-size: 13px; letter-spacing: 1px;
      text-align: center; max-width: 80vw;
      text-shadow: 0 1px 4px rgba(0,0,0,0.8);
    }
    .carousel-pos {
      position: fixed; top: 48px; left: 50%; transform: translateX(-50%);
      color: #7a6050; font-size: 11px; letter-spacing: 2px;
    }
    .carousel-hint {
      position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
      color: #555; font-size: 11px; letter-spacing: 1px;
      text-align: center;
    }
    .carousel-hint kbd {
      background: #333; color: #ccc; padding: 1px 6px; border-radius: 3px;
      font-size: 10px; font-family: monospace;
    }
    .carousel-arrows {
      position: fixed; top: 50%; width: 100%; display: flex;
      justify-content: space-between; padding: 0 16px;
      transform: translateY(-50%); pointer-events: none;
    }
    .carousel-arrows button {
      pointer-events: auto; background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.15); border-radius: 50%;
      width: 48px; height: 48px; font-size: 20px; color: #d4a76a;
      cursor: pointer; transition: background 0.2s;
    }
    .carousel-arrows button:hover { background: rgba(255,255,255,0.15); }

    /* Page-action modal (double-click blank pages) */
    .page-action-modal {
      display: none;
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.7);
      z-index: 10000;
      justify-content: center; align-items: center;
    }
    .page-action-modal.active { display: flex; }
    .page-action-box {
      background: #1a1410; border: 1px solid #3a3020;
      border-radius: 12px; padding: 28px 32px;
      min-width: 340px; max-width: 450px;
      box-shadow: 0 12px 40px rgba(0,0,0,0.6);
    }
    .page-action-title {
      color: #d4a76a; font-size: 15px; letter-spacing: 1px;
      text-transform: uppercase; margin-bottom: 20px; text-align: center;
    }
    .page-action-btn {
      display: block; width: 100%; padding: 12px 16px;
      margin-bottom: 10px; border: 1px solid #3a3020;
      border-radius: 8px; background: #2c1810;
      color: #e0d4c4; font-size: 14px;
      cursor: pointer; text-align: left;
      transition: background 0.15s, border-color 0.15s;
    }
    .page-action-btn:hover {
      background: #3a2818; border-color: #d4a76a;
    }
    .page-action-btn .btn-icon { margin-right: 10px; font-size: 16px; }
    .page-action-btn .btn-desc {
      display: block; font-size: 11px; color: #7a6050;
      margin-top: 3px; margin-left: 26px;
    }
    .page-action-input-row {
      display: none; margin-top: 12px;
    }
    .page-action-input-row.active { display: flex; gap: 8px; }
    .page-action-input {
      flex: 1; padding: 10px 12px;
      background: #0a0806; border: 1px solid #3a3020;
      border-radius: 6px; color: #e0d4c4; font-size: 13px;
      outline: none;
    }
    .page-action-input:focus { border-color: #d4a76a; }
    .page-action-submit {
      padding: 10px 16px; background: #d4a76a; color: #1a1410;
      border: none; border-radius: 6px; font-weight: 700;
      cursor: pointer; font-size: 13px;
    }
    .page-action-submit:hover { background: #e8c088; }
    .decorative-panel { cursor: pointer; }
    .decorative-panel:hover .ornament-number {
      opacity: 0.5;
      transition: opacity 0.2s;
    }
    .decorative-panel::after {
      content: 'double-click to add illustration';
      position: absolute; bottom: 24px; left: 50%;
      transform: translateX(-50%);
      color: #5a4030; font-size: 10px; letter-spacing: 1px;
      text-transform: uppercase; opacity: 0;
      transition: opacity 0.3s;
      pointer-events: none;
    }
    .decorative-panel:hover::after { opacity: 1; }
    @media (pointer: coarse) {
      .decorative-panel::after {
        content: 'tap to add illustration';
        opacity: 0.6;
      }
    }

    /* Unsaved changes indicator */
    .toolbar .save-indicator {
      font-size: 10px; color: #e94560; font-weight: bold; letter-spacing: 1px;
    }
    .toolbar .save-indicator.saved { color: #4ecca3; }

    /* ── Voice Assistant ── */
    .voice-btn {
      position: fixed; bottom: 24px; right: 24px;
      width: 56px; height: 56px; border-radius: 50%;
      background: #2c1810; border: 2px solid #d4a76a;
      color: #d4a76a; font-size: 24px; cursor: pointer;
      z-index: 90; transition: all 0.2s;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      font-family: Georgia, serif;
    }
    .voice-btn:hover { background: #3c2820; transform: scale(1.05); }
    .voice-btn.listening { background: #e94560; border-color: #ff6b80; animation: voicePulse 1s infinite; }
    .voice-btn.thinking { opacity: 0.6; cursor: wait; }
    @keyframes voicePulse {
      0%, 100% { box-shadow: 0 0 0 0 rgba(233,69,96,0.4); }
      50% { box-shadow: 0 0 0 12px rgba(233,69,96,0); }
    }
    .voice-popup {
      position: fixed; bottom: 90px; right: 24px;
      width: 280px; background: #2c1810;
      border: 1px solid #5a4030; border-radius: 12px;
      padding: 16px; color: #f0e6d6;
      font-family: Georgia, serif; font-size: 14px;
      z-index: 90; display: none;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }
    .voice-popup.visible { display: block; }
    .voice-status { font-size: 11px; color: #7a6050; margin-bottom: 8px; }
    .voice-answer { line-height: 1.6; }
    @media print { .voice-btn, .voice-popup { display: none !important; } }
    body.booklet-mode .voice-btn, body.booklet-mode .voice-popup { display: none !important; }

    /* Image highlight on changed */
    .page-left img.ill-changed {
      outline: 3px solid #4ecca3;
      outline-offset: 2px;
    }
    .page-left img.ill-removed {
      opacity: 0.3;
      outline: 3px solid #e94560;
      outline-offset: 2px;
    }
    .page-left img.ill-commented {
      outline: 3px solid #f0c040;
      outline-offset: 2px;
    }

    /* ── Preface / Poem ── */
    .preface-spread {
      position: relative;
      z-index: 51; /* Above tap overlay (z:50) so poem player is always clickable */
    }
    .preface-spread .preface-text {
      background: #2c1810;
      color: #f0e6d6;
      border-left-color: #5a4030;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .preface-spread .preface-text .page-number { color: #5a4030; }
    .poem-block {
      text-align: center;
      font-family: 'Georgia', serif;
      max-width: 420px;
    }
    .poem-title {
      font-size: clamp(14px, 2vw, 20px);
      letter-spacing: 3px;
      color: #d4a76a;
      margin-bottom: 28px;
      font-weight: 800;
    }
    .poem-stanza {
      margin-bottom: 20px;
    }
    .poem-line {
      font-size: clamp(12px, 1.4vw, 16px);
      line-height: 1.8;
      font-style: italic;
      color: #e0d4c4;
      letter-spacing: 0.3px;
    }
    /* Poem karaoke (light text on dark bg) */
    .preface-spread .k-word { transition: color 0.3s; }
    .preface-spread .k-word.k-active { color: #d4a76a; font-weight: bold; }
    .preface-spread .k-word.k-spoken { color: #7a6050; }
    .preface-spread .k-word.k-near { color: #c0a888; }
    .poem-play-hint {
      margin-top: 24px;
      font-size: 12px;
      color: #7a6050;
      letter-spacing: 1px;
      cursor: pointer;
      transition: color 0.3s;
      position: relative;
      z-index: 60; /* Above tap overlay so it's always clickable */
    }
    .poem-play-hint:hover { color: #d4a76a; }
    .poem-play-hint.playing { color: #d4a76a; }
    .poem-progress {
      margin-top: 8px;
      width: 200px;
      height: 3px;
      background: rgba(255,255,255,0.1);
      border-radius: 2px;
      margin-left: auto;
      margin-right: auto;
      overflow: hidden;
      position: relative;
      z-index: 60;
    }
    .poem-progress-bar {
      height: 100%;
      background: #d4a76a;
      width: 0%;
      transition: width 0.3s linear;
    }

  </style>
</head>
<body>

<div class="toolbar">
  <span class="ch-title" id="currentChLabel">ALICE IN WONDERLAND</span>
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
  <input type="text" id="searchInput" placeholder="Search..." autocomplete="off">
  <span class="match-count" id="matchCount"></span>
  <button id="caseToggle" title="Toggle uppercase/lowercase">Aa</button>
  <button id="fullscreenBtn">&#x26F6; Fullscreen</button>
  <button id="navToggle" title="Chapter list">&#9776; Chapters</button>
  <button id="downloadCsvBtn" title="Download illustration assignments as CSV">&#128190; Save CSV</button>
  <select id="viewModeSelect" title="View mode">
    <option value="reading">Reading</option>
    <option value="booklet">Booklet Print</option>
  </select>
  <span class="save-indicator" id="saveIndicator"></span>
</div>

<div id="saveNotify" style="display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.85);color:#d4a76a;padding:20px 40px;border-radius:12px;font-size:18px;z-index:9999;pointer-events:none;">Saved!</div>
<div class="tap-play-hint" id="tapPlayHint">tap any word to play from there</div>

<div class="chapter-nav" id="chapterNav">
  <h2>CHAPTERS</h2>
  <a class="nav-item" onclick="scrollToId('book-cover')">
    <span class="nav-num">BOOK</span>
    <span class="nav-name">Cover</span>
  </a>
  <a class="nav-item" onclick="scrollToId('preface')">
    <span class="nav-num">PREFACE</span>
    <span class="nav-name">All in the Golden Afternoon</span>
  </a>
</div>

<div class="page-action-modal" id="pageActionModal">
  <div class="page-action-box">
    <div class="page-action-title" id="pageActionTitle">Add Illustration</div>
    <button class="page-action-btn" id="paBtn-carousel">
      <span class="btn-icon">&#128444;</span> Browse Carousel
      <span class="btn-desc">Pick from existing illustrations</span>
    </button>
    <button class="page-action-btn" id="paBtn-url">
      <span class="btn-icon">&#128279;</span> Paste Image URL
      <span class="btn-desc">Use an image from any URL</span>
    </button>
    <div class="page-action-input-row" id="paUrlRow">
      <input class="page-action-input" id="paUrlInput" placeholder="https://...">
      <button class="page-action-submit" id="paUrlSubmit">Add</button>
    </div>
    <button class="page-action-btn" id="paBtn-ai">
      <span class="btn-icon">&#9998;</span> AI Image Prompt
      <span class="btn-desc">Describe an image to generate later</span>
    </button>
    <div class="page-action-input-row" id="paAiRow">
      <input class="page-action-input" id="paAiInput" placeholder="Describe the illustration you want...">
      <button class="page-action-submit" id="paAiSubmit">Save</button>
    </div>
    <button class="page-action-btn" id="paBtn-comment">
      <span class="btn-icon">&#128172;</span> Leave a Comment
      <span class="btn-desc">Note for editor or future reference</span>
    </button>
    <div class="page-action-input-row" id="paCommentRow">
      <input class="page-action-input" id="paCommentInput" placeholder="Your note...">
      <button class="page-action-submit" id="paCommentSubmit">Save</button>
    </div>
  </div>
</div>

<div class="zoom-overlay" id="zoomOverlay">
  <img id="zoomImg">
  <div class="carousel-info" id="carouselInfo"></div>
  <span class="carousel-pos" id="carouselPos"></span>
  <div class="carousel-arrows">
    <button id="carouselPrev" title="Previous image">&#9664;</button>
    <button id="carouselNext" title="Next image">&#9654;</button>
  </div>
  <div class="carousel-hint" id="carouselHintDesktop">
    <kbd>&#8592;</kbd> <kbd>&#8594;</kbd> browse &middot;
    <kbd>Enter</kbd> use this image &middot;
    <kbd>Del</kbd> remove &middot;
    <kbd>Esc</kbd> close
  </div>
  <div class="carousel-hint" id="carouselHintTouch" style="display:none">
    &#8592; &#8594; swipe to browse &middot;
    &#8595; swipe down = use &middot;
    &#8593; swipe up = remove &middot;
    tap outside = close
  </div>
</div>

<button id="voiceBtn" class="voice-btn" title="Ask a question about the story">&#127908;</button>
<div id="voicePopup" class="voice-popup">
  <div class="voice-status" id="voiceStatus">Tap the mic and ask a question!</div>
  <div class="voice-answer" id="voiceAnswer"></div>
</div>

${spreadsHtml}

<script>
// ── Data ──
var AUDIO_DATA = ${audioDataJson};
var IS_UNIFIED_AUDIO = ${isUnifiedAudio};
var CHAPTER_NAV = ${chapterNavJson};
var ILL_DATA = ${illustrationDataJson};
var UNUSED_ILLS = ${unusedIllsJson};
var CHAPTER_TEXT = ${JSON.stringify(bookletTextData)};
var BUILD_HASH = '${Date.now()}';
var ctxTarget = null;

// ── Chapter nav ──
(function() {
  var navEl = document.getElementById('chapterNav');
  for (var i = 0; i < CHAPTER_NAV.length; i++) {
    var ch = CHAPTER_NAV[i];
    var a = document.createElement('a');
    a.className = 'nav-item';
    a.dataset.ch = ch.num;
    a.onclick = (function(id) { return function() { scrollToId(id); }; })(ch.id);
    a.innerHTML = '<span class="nav-num">CHAPTER ' + ch.num + '</span>'
      + '<span class="nav-name">' + ch.name + '</span>'
      + '<span class="nav-meta">' + ch.pages + ' pages · ' + ch.ills + ' illustrations</span>';
    navEl.appendChild(a);
  }

  // Add THE END
  var endA = document.createElement('a');
  endA.className = 'nav-item';
  endA.onclick = function() { scrollToId('the-end'); };
  endA.innerHTML = '<span class="nav-num">BOOK</span><span class="nav-name">The End</span>';
  navEl.appendChild(endA);
})();

function scrollToId(id) {
  var el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
  document.getElementById('chapterNav').classList.remove('open');
}

// Nav toggle
document.getElementById('navToggle').addEventListener('click', function() {
  document.getElementById('chapterNav').classList.toggle('open');
});

// Detect touch device → show touch hints instead of keyboard hints
var isTouch = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;
if (isTouch) {
  var dh = document.getElementById('carouselHintDesktop');
  var th = document.getElementById('carouselHintTouch');
  if (dh) dh.style.display = 'none';
  if (th) th.style.display = 'block';
  // Show tap-to-play hint briefly
  var tapHint = document.getElementById('tapPlayHint');
  if (tapHint) {
    setTimeout(function() { tapHint.classList.add('visible'); }, 2000);
    setTimeout(function() { tapHint.classList.remove('visible'); }, 7000);
  }
}

// ── Preface Song Player ──
(function() {
  var hint = document.getElementById('poemPlayHint');
  if (!hint) return;

  var poemAudio = document.createElement('audio');
  poemAudio.src = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/audio/all-in-the-golden-afternoon.mp3';
  poemAudio.preload = 'metadata';
  document.body.appendChild(poemAudio);

  var isPlayingPoem = false;
  var poemAudioReady = false;

  poemAudio.addEventListener('canplaythrough', function() { poemAudioReady = true; });
  poemAudio.addEventListener('error', function() {
    hint.innerHTML = '&#9888; song file not found';
    hint.style.color = '#cc6644';
    hint.style.cursor = 'default';
    console.error('Poem audio failed to load:', poemAudio.src);
  });

  // Add progress bar
  var progDiv = document.createElement('div');
  progDiv.className = 'poem-progress';
  progDiv.innerHTML = '<div class="poem-progress-bar" id="poemProgressBar"></div>';
  hint.parentElement.appendChild(progDiv);
  var poemProgBar = document.getElementById('poemProgressBar');

  hint.addEventListener('click', function(e) {
    e.stopPropagation();
    if (isPlayingPoem) {
      poemAudio.pause();
      isPlayingPoem = false;
      hint.innerHTML = '&#9835; click to play song';
      hint.classList.remove('playing');
    } else {
      hint.innerHTML = '&#9834; loading...';
      poemAudio.play().then(function() {
        isPlayingPoem = true;
        hint.innerHTML = '&#9646;&#9646; pause song';
        hint.classList.add('playing');
      }).catch(function(err) {
        hint.innerHTML = '&#9888; audio not found';
        hint.style.color = '#cc6644';
        console.error('Poem audio error:', err);
      });
    }
  });

  // Collect poem karaoke words
  var poemKWords = Array.from(document.querySelectorAll('.preface-spread .k-word'));
  var NEAR = 3;

  poemAudio.addEventListener('timeupdate', function() {
    var t = poemAudio.currentTime;
    // Progress bar
    if (poemAudio.duration) {
      poemProgBar.style.width = ((t / poemAudio.duration) * 100) + '%';
    }
    // Karaoke highlighting
    if (poemKWords.length === 0) return;
    for (var i = 0; i < poemKWords.length; i++) {
      var s = parseFloat(poemKWords[i].dataset.start);
      var e = parseFloat(poemKWords[i].dataset.end);
      poemKWords[i].classList.remove('k-active', 'k-near', 'k-spoken');
      if (s === 0 && e === 0) continue; // no timestamp for this word
      if (t >= s && t <= e) {
        poemKWords[i].classList.add('k-active');
      } else if (t > e) {
        poemKWords[i].classList.add('k-spoken');
      } else if (t >= s - 2) {
        poemKWords[i].classList.add('k-near');
      }
    }
  });

  poemAudio.addEventListener('ended', function() {
    isPlayingPoem = false;
    hint.innerHTML = '&#9835; click to play song';
    hint.classList.remove('playing');
    poemProgBar.style.width = '0%';
    // Reset karaoke
    for (var i = 0; i < poemKWords.length; i++) {
      poemKWords[i].classList.remove('k-active', 'k-near', 'k-spoken');
    }
  });
})();

// ── Toolbar auto-hide ──
(function() {
  var toolbar = document.querySelector('.toolbar');
  var hideTimer = null;
  var HIDE_DELAY = 3000;

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

  hideTimer = setTimeout(function() {
    toolbar.classList.add('toolbar-hidden');
  }, HIDE_DELAY);
})();

// ── Auto-fit text ──
// Strategy: keep font size constant, adjust SPACING first.
// Phase 1: shrink line-height (1.7 → 1.2)
// Phase 2: shrink paragraph gaps (0.8em → 0.1em)
// Phase 3: reduce container padding (32px → 12px)
// Phase 4: last resort — shrink font slightly (18 → 13px)
(function() {
  var BASE_FONT = 18;
  var MIN_FONT = 13;
  var FONT_STEP = 0.5;
  var MAX_LH = 1.7;
  var MIN_LH = 1.2;
  var LH_STEP = 0.05;
  var MAX_MB = 0.8;
  var MIN_MB = 0.1;
  var MB_STEP = 0.1;
  var MAX_PAD = 32;
  var MIN_PAD = 12;
  var PAD_STEP = 4;

  function fitAll() {
    document.querySelectorAll('.text-block').forEach(function(block) {
      var container = block.parentElement;
      var ps = block.querySelectorAll('p');
      if (!ps.length) return;

      var size = BASE_FONT;
      var lh = MAX_LH;
      var mb = MAX_MB;
      var pad = MAX_PAD;

      function applyStyle() {
        container.style.paddingTop = pad + 'px';
        container.style.paddingBottom = pad + 'px';
        ps.forEach(function(p) {
          p.style.fontSize = size + 'px';
          p.style.lineHeight = lh.toFixed(2);
          p.style.marginBottom = mb.toFixed(1) + 'em';
        });
      }

      // Reset to defaults
      applyStyle();
      var maxH = container.clientHeight;

      // Phase 1: shrink line-height
      while (block.scrollHeight > maxH && lh > MIN_LH) {
        lh -= LH_STEP;
        applyStyle();
      }

      // Phase 2: shrink paragraph margins
      while (block.scrollHeight > maxH && mb > MIN_MB) {
        mb -= MB_STEP;
        applyStyle();
      }

      // Phase 3: reduce container padding
      while (block.scrollHeight > maxH && pad > MIN_PAD) {
        pad -= PAD_STEP;
        applyStyle();
        maxH = container.clientHeight; // recalc since padding changes available height
      }

      // Phase 4: last resort — shrink font slightly
      while (block.scrollHeight > maxH && size > MIN_FONT) {
        size -= FONT_STEP;
        applyStyle();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fitAll);
  } else {
    fitAll();
  }
  window.addEventListener('beforeprint', fitAll);
  window.addEventListener('resize', fitAll);
})();

// ── Word Search ──
(function() {
  var input = document.getElementById('searchInput');
  var countEl = document.getElementById('matchCount');
  if (!input) return;

  var matchGroups = []; // arrays of span groups for multi-word matches
  var currentMatchIdx = -1;

  function clearSearch() {
    document.querySelectorAll('.search-match, .search-current').forEach(function(el) {
      el.classList.remove('search-match', 'search-current');
    });
    countEl.textContent = '';
    matchGroups = [];
    currentMatchIdx = -1;
  }

  function scrollToMatch(idx) {
    if (idx < 0 || idx >= matchGroups.length) return;
    // Remove current highlight from previous
    document.querySelectorAll('.search-current').forEach(function(el) {
      el.classList.remove('search-current');
    });
    currentMatchIdx = idx;
    var group = matchGroups[idx];
    group.forEach(function(span) { span.classList.add('search-current'); });
    // Scroll to it
    var spread = group[0].closest('.spread');
    if (spread) spread.scrollIntoView({ behavior: 'smooth', block: 'center' });
    countEl.textContent = (idx + 1) + ' / ' + matchGroups.length;
  }

  function doSearch() {
    clearSearch();
    var query = input.value.trim();
    if (query.length < 2) return;

    var queryWords = query.toLowerCase().split(/\\s+/);
    var kWords = Array.from(document.querySelectorAll('.k-word'));

    if (kWords.length > 0 && queryWords.length > 1) {
      // Multi-word search: find sequences of spans matching the query words
      for (var i = 0; i <= kWords.length - queryWords.length; i++) {
        var match = true;
        for (var j = 0; j < queryWords.length; j++) {
          var spanText = kWords[i + j].textContent.toLowerCase().replace(/[^a-z0-9']/g, '');
          if (spanText !== queryWords[j].replace(/[^a-z0-9']/g, '')) {
            match = false;
            break;
          }
        }
        if (match) {
          var group = [];
          for (var j = 0; j < queryWords.length; j++) {
            kWords[i + j].classList.add('search-match');
            group.push(kWords[i + j]);
          }
          matchGroups.push(group);
        }
      }
    } else if (kWords.length > 0) {
      // Single word search
      var q = queryWords[0].replace(/[^a-z0-9']/g, '');
      kWords.forEach(function(span) {
        var spanText = span.textContent.toLowerCase().replace(/[^a-z0-9']/g, '');
        if (spanText === q || spanText.indexOf(q) >= 0) {
          span.classList.add('search-match');
          matchGroups.push([span]);
        }
      });
    }

    if (matchGroups.length > 0) {
      scrollToMatch(0);
    } else {
      countEl.textContent = 'no matches';
    }
  }

  var debounceTimer;
  input.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(doSearch, 300);
  });

  input.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') { input.value = ''; clearSearch(); input.blur(); }
    if (e.key === 'Enter') {
      e.preventDefault();
      if (matchGroups.length === 0) { doSearch(); return; }
      var next = e.shiftKey ? currentMatchIdx - 1 : currentMatchIdx + 1;
      if (next >= matchGroups.length) next = 0;
      if (next < 0) next = matchGroups.length - 1;
      scrollToMatch(next);
    }
  });

  // Ctrl+F opens in-app search instead of browser find
  document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'f') {
      e.preventDefault();
      input.focus();
      input.select();
    }
  });
})();

// ── Update current chapter label on scroll ──
(function() {
  var chapterDividers = document.querySelectorAll('.chapter-divider');
  var label = document.getElementById('currentChLabel');
  var navItems = document.querySelectorAll('.chapter-nav .nav-item');

  function updateChapter() {
    var scrollY = window.scrollY + window.innerHeight / 2;
    var current = null;
    chapterDividers.forEach(function(div) {
      if (div.offsetTop <= scrollY) {
        current = div;
      }
    });
    if (current) {
      var id = current.id;
      var chNum = id.replace('ch', '');
      var ch = CHAPTER_NAV.find(function(c) { return c.num == chNum; });
      if (ch) {
        label.textContent = 'CH ' + ch.num + ': ' + ch.name.toUpperCase();
        // Update active nav item
        navItems.forEach(function(ni) {
          ni.classList.toggle('active', ni.dataset.ch == chNum);
        });
      }
    } else {
      label.textContent = 'ALICE IN WONDERLAND';
    }
  }

  var scrollTimer;
  window.addEventListener('scroll', function() {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(updateChapter, 100);
  });
})();

// ── Unified Karaoke Audio Player (single audio file) ──
(function() {
  if (!AUDIO_DATA || !AUDIO_DATA.url) {
    var playBtn = document.getElementById('playBtn');
    if (playBtn) playBtn.style.display = 'none';
    return;
  }

  var audio = document.createElement('audio');
  audio.preload = 'auto';
  audio.src = AUDIO_DATA.url;
  document.body.appendChild(audio);

  var playBtn = document.getElementById('playBtn');
  var timeEl = document.getElementById('audioTime');
  var progEl = document.getElementById('progressBar');
  var progressTrack = document.getElementById('progressTrack');
  var isPlaying = false;
  var totalDuration = AUDIO_DATA.totalDuration || 0;
  var chapters = AUDIO_DATA.chapters || [];

  // ── Build karaoke word spans from page data ──
  var allKWords = [];
  var allStarts = [];
  var allEnds = [];

  var pages = AUDIO_DATA.pages || [];
  for (var pi = 0; pi < pages.length; pi++) {
    var pageData = pages[pi];
    var pageEl = document.querySelector('[data-page="' + pageData.pageNum + '"]');
    if (!pageEl) continue;
    var textBlock = pageEl.querySelector('.text-block');
    if (!textBlock) continue;

    var walker = document.createTreeWalker(textBlock, NodeFilter.SHOW_TEXT, null, false);
    var textNodes = [];
    var node;
    while (node = walker.nextNode()) {
      if (node.textContent.trim()) textNodes.push(node);
    }

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
          allStarts.push(w.start);
          allEnds.push(w.end);
          frag.appendChild(span);
          wordIdx++;
        } else {
          frag.appendChild(document.createTextNode(part));
        }
      });

      textNode.parentNode.replaceChild(frag, textNode);
    });
  }

  console.log('Karaoke: ' + allKWords.length + ' words, unified audio (' + (totalDuration / 60).toFixed(0) + ' min)');

  // ── Helpers ──
  function getChapterAt(t) {
    for (var i = chapters.length - 1; i >= 0; i--) {
      if (t >= chapters[i].offset) return i;
    }
    return 0;
  }

  function formatTime(s) {
    var m = Math.floor(s / 60);
    var sec = Math.floor(s % 60);
    return m + ':' + (sec < 10 ? '0' : '') + sec;
  }

  function updateProgressDisplay(t) {
    var dur = audio.duration || totalDuration;
    if (dur > 0) {
      progEl.style.width = ((t / dur) * 100) + '%';
      var ci = getChapterAt(t);
      var localTime = t - chapters[ci].offset;
      timeEl.textContent = 'Ch' + chapters[ci].chapter + ' ' + formatTime(localTime) + ' — ' + formatTime(t) + '/' + formatTime(dur);
    }
  }

  function togglePlayPause() {
    if (isPlaying) {
      audio.pause();
      isPlaying = false;
      playBtn.innerHTML = '&#9654; Play';
      playBtn.classList.remove('active');
    } else {
      try {
        var poemHint = document.getElementById('poemPlayHint');
        if (poemHint && poemHint.classList.contains('playing')) poemHint.click();
      } catch(ex) {}
      audio.play();
      isPlaying = true;
      playBtn.innerHTML = '&#9646;&#9646; Pause';
      playBtn.classList.add('active');
    }
  }

  playBtn.addEventListener('click', togglePlayPause);

  document.addEventListener('keydown', function(e) {
    if (e.code === 'Space' && document.activeElement.tagName !== 'INPUT') {
      e.preventDefault();
      togglePlayPause();
    }
    if (e.key === 'Enter' && document.activeElement.tagName !== 'INPUT' && !document.querySelector('.zoom-overlay.active')) {
      e.preventDefault();
      if (!isPlaying) togglePlayPause();
    }
  });

  // ── Click-to-seek on text ──
  // Click any word → seek to that absolute timestamp. No chapter loading needed!
  document.addEventListener('click', function(e) {
    var wordEl = e.target.closest('.k-word');
    if (!wordEl) return;
    if (wordEl.closest('.preface-spread')) return;
    if (document.querySelector('.zoom-overlay.active')) return;

    var targetStart = parseFloat(wordEl.dataset.start);
    if (isNaN(targetStart)) return;

    audio.currentTime = targetStart;
    updateProgressDisplay(targetStart);
    if (!isPlaying) togglePlayPause();

    wordEl.style.background = 'rgba(184, 144, 96, 0.3)';
    wordEl.style.borderRadius = '3px';
    setTimeout(function() { wordEl.style.background = ''; wordEl.style.borderRadius = ''; }, 800);
  });

  // ── Audio ended → book finished ──
  audio.addEventListener('ended', function() {
    for (var i = 0; i < allKWords.length; i++) {
      allKWords[i].classList.add('k-spoken');
      allKWords[i].classList.remove('k-active', 'k-near');
    }
    isPlaying = false;
    playBtn.innerHTML = '&#9654; Play';
    playBtn.classList.remove('active');
    scrollToId('the-end');
  });

  // ── Karaoke Update Loop ──
  var NEAR_RANGE = 8;
  var lastActiveIdx = -1;
  var lastScrollPage = -1;
  var lastUpdateTime = 0;

  function findWordAt(t) {
    var lo = 0, hi = allStarts.length - 1;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1;
      if (t < allStarts[mid]) { hi = mid - 1; }
      else if (t > allEnds[mid] + 0.3) { lo = mid + 1; }
      else { return mid; }
    }
    if (lo < allStarts.length && t < allStarts[lo]) return lo;
    return lo > 0 ? lo - 1 : 0;
  }

  function updateKaraoke() {
    if (!isPlaying) return;
    var t = audio.currentTime;

    var now = Date.now();
    if (now - lastUpdateTime < 100) {
      requestAnimationFrame(updateKaraoke);
      return;
    }
    lastUpdateTime = now;

    updateProgressDisplay(t);

    if (allStarts.length === 0 || t < allStarts[0] - 0.1) {
      requestAnimationFrame(updateKaraoke);
      return;
    }

    var idx = findWordAt(t);

    if (idx !== lastActiveIdx) {
      // Clear old highlights in a small window
      if (lastActiveIdx >= 0) {
        var clearFrom = Math.max(0, lastActiveIdx - NEAR_RANGE - 1);
        var clearTo = Math.min(allKWords.length - 1, lastActiveIdx + NEAR_RANGE + 1);
        for (var c = clearFrom; c <= clearTo; c++) {
          allKWords[c].classList.remove('k-active', 'k-near');
        }
      }

      // Mark spoken (only the gap between old and new position)
      if (lastActiveIdx >= 0 && lastActiveIdx < idx) {
        for (var s = lastActiveIdx; s < idx; s++) {
          allKWords[s].classList.add('k-spoken');
          allKWords[s].classList.remove('k-active', 'k-near');
        }
      }

      // Active word
      allKWords[idx].classList.add('k-active');
      allKWords[idx].classList.remove('k-spoken', 'k-near');

      // Near words (upcoming)
      for (var n = 1; n <= NEAR_RANGE; n++) {
        var ni = idx + n;
        if (ni < allKWords.length) {
          allKWords[ni].classList.add('k-near');
          allKWords[ni].classList.remove('k-spoken', 'k-active');
        }
      }

      lastActiveIdx = idx;

      // Auto-scroll to spread
      var pageNum = parseInt(allKWords[idx].dataset.page);
      if (pageNum !== lastScrollPage) {
        lastScrollPage = pageNum;
        var pageEl = document.querySelector('[data-page="' + pageNum + '"]');
        if (pageEl) {
          var spread = pageEl.closest('.spread');
          if (spread) spread.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    }

    requestAnimationFrame(updateKaraoke);
  }

  audio.addEventListener('play', function() {
    lastUpdateTime = 0;
    requestAnimationFrame(updateKaraoke);
  });

  // ── Click on progress track to seek ──
  progressTrack.addEventListener('click', function(e) {
    var rect = progressTrack.getBoundingClientRect();
    var pct = (e.clientX - rect.left) / rect.width;
    var dur = audio.duration || totalDuration;
    if (dur <= 0) return;

    audio.currentTime = pct * dur;
    updateProgressDisplay(pct * dur);

    lastUpdateTime = 0;
    if (isPlaying) requestAnimationFrame(updateKaraoke);
  });

  // ── Handle seek — reset karaoke highlights ──
  audio.addEventListener('seeked', function() {
    var t = audio.currentTime;
    // Reset all highlights
    for (var i = 0; i < allKWords.length; i++) {
      allKWords[i].classList.remove('k-active', 'k-spoken', 'k-near');
    }
    // Mark words before seek position as spoken
    if (allStarts.length > 0 && t >= allStarts[0]) {
      var seekIdx = findWordAt(t);
      for (var i = 0; i < seekIdx; i++) {
        allKWords[i].classList.add('k-spoken');
      }
    }
    lastActiveIdx = -1;
    lastScrollPage = -1;
    lastUpdateTime = 0;
    if (isPlaying) requestAnimationFrame(updateKaraoke);
  });

  // Safety net — restart karaoke loop if it stalls
  setInterval(function() {
    if (isPlaying && !audio.paused) {
      lastUpdateTime = 0;
      requestAnimationFrame(updateKaraoke);
    }
  }, 2000);

  // Speed controls
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

// ── Aa Case Toggle ──
(function() {
  var btn = document.getElementById('caseToggle');
  if (!btn) return;
  var isUpper = ${USE_CAPS};

  btn.addEventListener('click', function() {
    isUpper = !isUpper;
    btn.textContent = isUpper ? 'Aa' : 'AA';
    document.querySelectorAll('.text-block p').forEach(function(p) {
      p.style.textTransform = isUpper ? 'uppercase' : 'none';
      p.style.fontWeight = isUpper ? '700' : '400';
      p.style.letterSpacing = isUpper ? '0.3px' : '0';
    });
    document.querySelectorAll('.title-block h1, .series-name, .book-number, .author, .page-info, .back-block, .the-end, .back-info').forEach(function(el) {
      el.style.textTransform = isUpper ? 'uppercase' : 'none';
    });
  });
})();

// ── View Mode Dropdown ──
(function() {
  var viewSelect = document.getElementById('viewModeSelect');
  if (!viewSelect) return;
  viewSelect.addEventListener('change', function() {
    var mode = viewSelect.value;
    if (mode === 'booklet') {
      document.body.classList.add('booklet-mode');
    } else {
      document.body.classList.remove('booklet-mode');
    }
  });
})();

// ── Illustration Carousel Editor — Double-click → Browse → Enter to Swap ──
(function() {
  var zoomOverlay = document.getElementById('zoomOverlay');
  var zoomImg = document.getElementById('zoomImg');
  var carouselInfo = document.getElementById('carouselInfo');
  var carouselPos = document.getElementById('carouselPos');
  var saveIndicator = document.getElementById('saveIndicator');

  var undoStack = [];
  var redoStack = [];
  var unsavedChanges = false;

  // Carousel state
  var carouselOpen = false;
  var carouselIdx = 0;        // current position in ALL_IMAGES
  var sourceIllIdx = -1;      // ILL_DATA index of the page we opened from
  var ALL_IMAGES = [];         // built dynamically when carousel opens

  // ── Build the carousel image list ──
  function buildCarouselList(startIllIdx) {
    ALL_IMAGES = [];
    // 1. All assigned images (from ILL_DATA with URLs)
    for (var i = 0; i < ILL_DATA.length; i++) {
      if (ILL_DATA[i].url) {
        ALL_IMAGES.push({
          type: 'assigned', illIdx: i,
          url: ILL_DATA[i].url,
          info: ILL_DATA[i].info || '',
          label: ILL_DATA[i].label || ('Ch' + ILL_DATA[i].ch + ' p' + ILL_DATA[i].pg)
        });
      }
    }
    // 2. Unassigned images from the pool
    for (var u = 0; u < UNUSED_ILLS.length; u++) {
      ALL_IMAGES.push({
        type: 'unused', unusedIdx: u,
        url: UNUSED_ILLS[u].url,
        info: UNUSED_ILLS[u].info || '',
        label: 'Unassigned — ' + (UNUSED_ILLS[u].source || '').substring(0, 30)
      });
    }
    // Find starting position (the image currently assigned to sourceIllIdx)
    carouselIdx = 0;
    var found = false;
    for (var j = 0; j < ALL_IMAGES.length; j++) {
      if (ALL_IMAGES[j].type === 'assigned' && ALL_IMAGES[j].illIdx === startIllIdx) {
        carouselIdx = j;
        found = true;
        break;
      }
    }
    // If not found by illIdx, try matching by URL
    if (!found && ILL_DATA[startIllIdx] && ILL_DATA[startIllIdx].url) {
      var targetUrl = ILL_DATA[startIllIdx].url;
      for (var j = 0; j < ALL_IMAGES.length; j++) {
        if (ALL_IMAGES[j].url === targetUrl) {
          carouselIdx = j;
          found = true;
          break;
        }
      }
    }
  }

  function showCarouselImage() {
    if (ALL_IMAGES.length === 0) return;
    var img = ALL_IMAGES[carouselIdx];
    zoomImg.src = img.url;
    carouselInfo.textContent = img.label + ' — ' + img.info;
    carouselPos.textContent = (carouselIdx + 1) + ' / ' + ALL_IMAGES.length;
    // Indicate if this is the current page's image
    var isCurrent = (img.type === 'assigned' && img.illIdx === sourceIllIdx);
    carouselInfo.style.color = isCurrent ? '#4ecca3' : '#d4a76a';
  }

  function openCarousel(illIdx) {
    sourceIllIdx = illIdx;
    buildCarouselList(illIdx);
    carouselOpen = true;
    zoomOverlay.classList.add('active');
    showCarouselImage();
  }

  function closeCarousel() {
    carouselOpen = false;
    zoomOverlay.classList.remove('active');
    sourceIllIdx = -1;
  }

  function carouselPrev() {
    carouselIdx = (carouselIdx - 1 + ALL_IMAGES.length) % ALL_IMAGES.length;
    showCarouselImage();
  }

  function carouselNext() {
    carouselIdx = (carouselIdx + 1) % ALL_IMAGES.length;
    showCarouselImage();
  }

  // ── Save/unsaved state ──
  function markUnsaved() {
    unsavedChanges = true;
    if (saveIndicator) {
      saveIndicator.textContent = undoStack.length + ' unsaved';
      saveIndicator.className = 'save-indicator';
    }
  }

  function markSaved() {
    unsavedChanges = false;
    if (saveIndicator) {
      saveIndicator.textContent = 'saved';
      saveIndicator.className = 'save-indicator saved';
    }
    setTimeout(function() {
      if (!unsavedChanges && saveIndicator) saveIndicator.textContent = '';
    }, 3000);
  }

  // ── Auto-save to localStorage on every change ──
  function autoSave() {
    try {
      var data = ILL_DATA.map(function(d) {
        return { ch: d.ch, pg: d.pg, url: d.url, info: d.info, comment: d.comment || '' };
      });
      localStorage.setItem('alice-ill-assignments', JSON.stringify(data));
      localStorage.setItem('alice-ill-timestamp', new Date().toISOString());
      localStorage.setItem('alice-ill-build', BUILD_HASH);
    } catch(ex) {}
  }

  // ── Restore from localStorage on load ──
  function tryRestore() {
    try {
      var saved = localStorage.getItem('alice-ill-assignments');
      if (!saved) return;
      // Validate build hash — discard stale data from previous builds
      var savedBuild = localStorage.getItem('alice-ill-build');
      if (savedBuild !== BUILD_HASH) {
        console.log('localStorage from different build (' + savedBuild + ' vs ' + BUILD_HASH + ') — clearing stale data');
        localStorage.removeItem('alice-ill-assignments');
        localStorage.removeItem('alice-ill-timestamp');
        localStorage.removeItem('alice-ill-build');
        return;
      }
      var ts = localStorage.getItem('alice-ill-timestamp') || 'unknown';
      var data = JSON.parse(saved);
      if (!data || data.length !== ILL_DATA.length) return;
      // Check if anything actually differs
      var changed = false;
      for (var i = 0; i < data.length; i++) {
        if (data[i].url !== ILL_DATA[i].url || data[i].comment !== (ILL_DATA[i].comment || '')) {
          changed = true; break;
        }
      }
      if (!changed) return;
      // Restore (silently — no highlight outlines)
      for (var i = 0; i < data.length; i++) {
        if (data[i].url !== ILL_DATA[i].url) {
          ILL_DATA[i].url = data[i].url;
          ILL_DATA[i].info = data[i].info;
          updateIllInDOM(ILL_DATA[i].ch, ILL_DATA[i].pg, data[i].url, '');
        }
        if (data[i].comment) ILL_DATA[i].comment = data[i].comment;
      }
      if (saveIndicator) {
        saveIndicator.textContent = 'restored from ' + ts.substring(11, 19);
        saveIndicator.className = 'save-indicator saved';
        setTimeout(function() { saveIndicator.textContent = ''; }, 5000);
      }
    } catch(ex) {}
  }
  tryRestore();

  // ── Page-action modal for text-only pages ──
  var pageActionModal = document.getElementById('pageActionModal');
  var pageActionTitle = document.getElementById('pageActionTitle');
  var paUrlRow = document.getElementById('paUrlRow');
  var paAiRow = document.getElementById('paAiRow');
  var paCommentRow = document.getElementById('paCommentRow');
  var paUrlInput = document.getElementById('paUrlInput');
  var paAiInput = document.getElementById('paAiInput');
  var paCommentInput = document.getElementById('paCommentInput');
  var paTargetIdx = -1;

  function openPageAction(idx) {
    paTargetIdx = idx;
    var d = ILL_DATA[idx];
    pageActionTitle.textContent = 'Ch' + d.ch + ' Page ' + d.pg + ' — Add Illustration';
    // Reset input rows
    paUrlRow.classList.remove('active');
    paAiRow.classList.remove('active');
    paCommentRow.classList.remove('active');
    paUrlInput.value = '';
    paAiInput.value = d.comment && d.comment.startsWith('[AI]') ? d.comment.substring(5) : '';
    paCommentInput.value = d.comment && !d.comment.startsWith('[AI]') ? d.comment : '';
    pageActionModal.classList.add('active');
  }

  function closePageAction() {
    pageActionModal.classList.remove('active');
    paTargetIdx = -1;
  }

  // Close modal on background click
  pageActionModal.addEventListener('click', function(e) {
    if (e.target === pageActionModal) closePageAction();
  });

  // Browse carousel button
  document.getElementById('paBtn-carousel').addEventListener('click', function() {
    if (paTargetIdx < 0) return;
    var idx = paTargetIdx;
    closePageAction();
    openCarousel(idx);
  });

  // URL input toggle
  document.getElementById('paBtn-url').addEventListener('click', function() {
    var active = paUrlRow.classList.contains('active');
    paUrlRow.classList.toggle('active', !active);
    paAiRow.classList.remove('active');
    paCommentRow.classList.remove('active');
    if (!active) paUrlInput.focus();
  });

  // URL submit
  document.getElementById('paUrlSubmit').addEventListener('click', function() {
    var url = paUrlInput.value.trim();
    if (!url || paTargetIdx < 0) return;
    var idx = paTargetIdx;
    var d = ILL_DATA[idx];
    var action = {
      type: 'assign',
      idx: idx, ch: d.ch, pg: d.pg,
      prevUrl: d.url, prevInfo: d.info,
      newUrl: url, newInfo: 'url-added'
    };
    undoStack.push(action);
    redoStack = [];
    d.url = url;
    d.info = 'url-added';
    updateIllInDOM(d.ch, d.pg, url, 'changed');
    markUnsaved();
    autoSave();
    closePageAction();
  });

  // AI prompt toggle
  document.getElementById('paBtn-ai').addEventListener('click', function() {
    var active = paAiRow.classList.contains('active');
    paAiRow.classList.toggle('active', !active);
    paUrlRow.classList.remove('active');
    paCommentRow.classList.remove('active');
    if (!active) paAiInput.focus();
  });

  // AI prompt submit
  document.getElementById('paAiSubmit').addEventListener('click', function() {
    var prompt = paAiInput.value.trim();
    if (!prompt || paTargetIdx < 0) return;
    var idx = paTargetIdx;
    doComment(idx, '[AI] ' + prompt);
    closePageAction();
  });

  // Comment toggle
  document.getElementById('paBtn-comment').addEventListener('click', function() {
    var active = paCommentRow.classList.contains('active');
    paCommentRow.classList.toggle('active', !active);
    paUrlRow.classList.remove('active');
    paAiRow.classList.remove('active');
    if (!active) paCommentInput.focus();
  });

  // Comment submit
  document.getElementById('paCommentSubmit').addEventListener('click', function() {
    var comment = paCommentInput.value.trim();
    if (!comment || paTargetIdx < 0) return;
    var idx = paTargetIdx;
    doComment(idx, comment);
    closePageAction();
  });

  // Enter key submits whichever input row is active
  [paUrlInput, paAiInput, paCommentInput].forEach(function(inp) {
    inp.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        inp.parentElement.querySelector('.page-action-submit').click();
      }
    });
  });

  // Escape closes modal
  pageActionModal.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') { e.preventDefault(); closePageAction(); }
  });

  // ── Double-click on decorative-panel → open page action modal ──
  document.addEventListener('dblclick', function(e) {
    var panel = e.target.closest('.decorative-panel');
    if (!panel) return;
    var ch = parseInt(panel.dataset.ch);
    var localPage = parseInt(panel.dataset.localPage);
    if (isNaN(ch) || isNaN(localPage)) return;
    var idx = ILL_DATA.findIndex(function(d) { return d.ch === ch && d.pg === localPage; });
    if (idx === -1) return;
    e.preventDefault();
    openPageAction(idx);
  });

  // ── Click image → opens carousel ──
  document.addEventListener('click', function(e) {
    if (carouselOpen) return;
    // Ignore if page-action modal is open
    if (pageActionModal.classList.contains('active')) return;
    var img = e.target.closest('.page-left img');
    if (!img) return;
    var ch = parseInt(img.dataset.ch);
    var pg = parseInt(img.dataset.pg);
    if (isNaN(ch) || isNaN(pg)) return;
    var idx = ILL_DATA.findIndex(function(d) { return d.ch === ch && d.pg === pg; });
    console.log('Click image: ch=' + ch + ' pg=' + pg + ' → ILL_DATA idx=' + idx);
    if (idx === -1) return;
    openCarousel(idx);
  });

  // Close carousel on background click (not on image or buttons)
  zoomOverlay.addEventListener('click', function(e) {
    if (e.target === zoomOverlay) {
      closeCarousel();
    }
  });

  // Carousel arrow buttons
  document.getElementById('carouselPrev').addEventListener('click', function(e) {
    e.stopPropagation();
    carouselPrev();
  });
  document.getElementById('carouselNext').addEventListener('click', function(e) {
    e.stopPropagation();
    carouselNext();
  });
  // Click on image itself does nothing (don't close)
  zoomImg.addEventListener('click', function(e) {
    e.stopPropagation();
  });

  // ── Touch/Swipe gestures for tablet ──
  var touchStartX = 0, touchStartY = 0, touchStartTime = 0;
  var SWIPE_THRESHOLD = 50;   // min px for a swipe
  var SWIPE_MAX_TIME = 500;   // max ms for a swipe gesture

  zoomOverlay.addEventListener('touchstart', function(e) {
    if (!carouselOpen) return;
    var t = e.touches[0];
    touchStartX = t.clientX;
    touchStartY = t.clientY;
    touchStartTime = Date.now();
  }, { passive: true });

  zoomOverlay.addEventListener('touchend', function(e) {
    if (!carouselOpen) return;
    var t = e.changedTouches[0];
    var dx = t.clientX - touchStartX;
    var dy = t.clientY - touchStartY;
    var dt = Date.now() - touchStartTime;
    if (dt > SWIPE_MAX_TIME) return; // too slow, not a swipe

    var absDx = Math.abs(dx), absDy = Math.abs(dy);

    if (absDx > absDy && absDx > SWIPE_THRESHOLD) {
      // Horizontal swipe — browse carousel
      e.preventDefault();
      if (dx < 0) carouselNext();  // swipe left → next
      else carouselPrev();         // swipe right → prev
    } else if (absDy > absDx && absDy > SWIPE_THRESHOLD) {
      // Vertical swipe
      e.preventDefault();
      if (dy < 0) {
        // Swipe UP → delete image from page
        doRemove(sourceIllIdx);
        closeCarousel();
        // Quick feedback
        var notify = document.getElementById('saveNotify');
        if (notify) { notify.textContent = 'Removed!'; notify.style.display = 'block'; setTimeout(function() { notify.style.display = 'none'; }, 1000); }
      } else {
        // Swipe DOWN → use this image (same as Enter)
        doSwapWithCarousel();
        var notify = document.getElementById('saveNotify');
        if (notify) { notify.textContent = 'Assigned!'; notify.style.display = 'block'; setTimeout(function() { notify.style.display = 'none'; }, 1000); }
      }
    }
  });

  // Prevent default scroll while swiping in carousel
  zoomOverlay.addEventListener('touchmove', function(e) {
    if (carouselOpen) e.preventDefault();
  }, { passive: false });

  // ── Tap on image opens carousel (single tap for touch devices) ──
  var tapTimeout = null;
  document.addEventListener('touchend', function(e) {
    if (carouselOpen) return;
    if (pageActionModal.classList.contains('active')) return;
    var img = e.target.closest('.page-left img');
    if (!img) return;
    // Use a short timeout to distinguish tap from scroll
    if (tapTimeout) clearTimeout(tapTimeout);
    tapTimeout = setTimeout(function() {
      var ch = parseInt(img.dataset.ch);
      var pg = parseInt(img.dataset.pg);
      if (isNaN(ch) || isNaN(pg)) return;
      var idx = ILL_DATA.findIndex(function(d) { return d.ch === ch && d.pg === pg; });
      if (idx === -1) return;
      openCarousel(idx);
    }, 250);
  });

  // Tap on decorative panel opens page action modal (on touch)
  document.addEventListener('touchend', function(e) {
    if (carouselOpen) return;
    var panel = e.target.closest('.decorative-panel');
    if (!panel) return;
    if (tapTimeout) clearTimeout(tapTimeout);
    tapTimeout = setTimeout(function() {
      var ch = parseInt(panel.dataset.ch);
      var localPage = parseInt(panel.dataset.localPage);
      if (isNaN(ch) || isNaN(localPage)) return;
      var idx = ILL_DATA.findIndex(function(d) { return d.ch === ch && d.pg === localPage; });
      if (idx === -1) return;
      openPageAction(idx);
    }, 250);
  });

  // ── Right-click for comment (in reading mode) ──
  document.addEventListener('contextmenu', function(e) {
    var img = e.target.closest('.page-left img');
    if (!img) return;
    e.preventDefault();
    var ch = parseInt(img.dataset.ch);
    var pg = parseInt(img.dataset.pg);
    if (isNaN(ch) || isNaN(pg)) return;
    var idx = ILL_DATA.findIndex(function(d) { return d.ch === ch && d.pg === pg; });
    if (idx === -1) return;
    var d = ILL_DATA[idx];
    var comment = prompt('Comment for Ch' + ch + ' ' + (pg === 0 ? 'Cover' : 'Page ' + pg) + ':', d.comment || '');
    if (comment !== null) {
      doComment(idx, comment);
    }
  });

  // ── Actions ──
  function doSwapWithCarousel() {
    if (sourceIllIdx < 0 || ALL_IMAGES.length === 0) return;
    var carouselItem = ALL_IMAGES[carouselIdx];
    var source = ILL_DATA[sourceIllIdx];

    // If carousel shows the same image that's already assigned, nothing to do
    if (carouselItem.type === 'assigned' && carouselItem.illIdx === sourceIllIdx) return;

    if (carouselItem.type === 'assigned') {
      // Swap two assigned images
      var targetIdx = carouselItem.illIdx;
      var action = {
        type: 'swap',
        a: { idx: sourceIllIdx, ch: source.ch, pg: source.pg, url: source.url, info: source.info },
        b: { idx: targetIdx, ch: ILL_DATA[targetIdx].ch, pg: ILL_DATA[targetIdx].pg, url: ILL_DATA[targetIdx].url, info: ILL_DATA[targetIdx].info }
      };
      undoStack.push(action);
      redoStack = [];

      var tmpUrl = source.url; var tmpInfo = source.info;
      source.url = ILL_DATA[targetIdx].url;
      source.info = ILL_DATA[targetIdx].info;
      ILL_DATA[targetIdx].url = tmpUrl;
      ILL_DATA[targetIdx].info = tmpInfo;

      updateIllInDOM(source.ch, source.pg, source.url, 'changed');
      updateIllInDOM(ILL_DATA[targetIdx].ch, ILL_DATA[targetIdx].pg, ILL_DATA[targetIdx].url, 'changed');
    } else {
      // Assign from unused pool
      var action = {
        type: 'assign',
        idx: sourceIllIdx, ch: source.ch, pg: source.pg,
        prevUrl: source.url, prevInfo: source.info,
        newUrl: carouselItem.url, newInfo: carouselItem.info
      };
      undoStack.push(action);
      redoStack = [];

      source.url = carouselItem.url;
      source.info = carouselItem.info;

      updateIllInDOM(source.ch, source.pg, source.url, 'changed');
    }

    markUnsaved();
    autoSave();
    closeCarousel();
  }

  function doRemove(idx) {
    var d = ILL_DATA[idx];
    if (!d.url) return; // already empty
    var action = {
      type: 'remove', idx: idx, ch: d.ch, pg: d.pg,
      url: d.url, info: d.info
    };
    undoStack.push(action);
    redoStack = [];

    d.url = '';
    d.info = 'text-only';

    updateIllInDOM(d.ch, d.pg, '', 'removed');
    markUnsaved();
    autoSave();
  }

  function doComment(idx, comment) {
    var d = ILL_DATA[idx];
    var prevComment = d.comment || '';
    var action = {
      type: 'comment', idx: idx, ch: d.ch, pg: d.pg,
      prevComment: prevComment, comment: comment
    };
    undoStack.push(action);
    redoStack = [];

    d.comment = comment;
    updateIllInDOM(d.ch, d.pg, d.url, 'commented');
    markUnsaved();
    autoSave();
  }

  function updateIllInDOM(ch, pg, newUrl, highlight) {
    var imgs = document.querySelectorAll('img[data-ch="' + ch + '"][data-pg="' + pg + '"]');
    if (imgs.length > 0) {
      if (newUrl) {
        imgs.forEach(function(img) {
          img.classList.remove('ill-changed', 'ill-removed', 'ill-commented');
          img.src = newUrl;
          if (highlight === 'changed') img.classList.add('ill-changed');
          if (highlight === 'commented') img.classList.add('ill-commented');
        });
      } else {
        // Remove image → convert back to decorative panel with chapter ornament
        imgs.forEach(function(img) {
          var pageLeft = img.closest('.page-left');
          if (!pageLeft) return;
          // Remove the image
          img.remove();
          // Add decorative-panel class
          pageLeft.classList.add('decorative-panel');
          pageLeft.style.cursor = '';
          pageLeft.style.background = '';
          // Ensure data attributes for event handlers
          pageLeft.dataset.ch = ch;
          pageLeft.dataset.localPage = pg;
          // Add chapter ornament (number shows the chapter)
          if (!pageLeft.querySelector('.chapter-ornament')) {
            var ornament = document.createElement('div');
            ornament.className = 'chapter-ornament';
            var inner = document.createElement('div');
            inner.className = 'ornament-number';
            inner.textContent = ch;
            ornament.appendChild(inner);
            var pageNum = pageLeft.querySelector('.page-number');
            pageLeft.insertBefore(ornament, pageNum);
          }
          // Add text-only class to parent spread
          var spread = pageLeft.closest('.spread');
          if (spread) spread.classList.add('text-only');
        });
      }
    } else if (newUrl) {
      // No <img> found — this is a decorative-panel → convert to image page
      var panels = document.querySelectorAll('.decorative-panel[data-ch="' + ch + '"][data-local-page="' + pg + '"]');
      panels.forEach(function(panel) {
        panel.classList.remove('decorative-panel');
        // Remove the ornament content
        var ornament = panel.querySelector('.chapter-ornament');
        if (ornament) ornament.remove();
        // Remove the ::after hint by adding a class
        panel.style.cursor = 'default';
        panel.style.background = '';
        // Create the image
        var img = document.createElement('img');
        img.src = newUrl;
        img.alt = 'illustration';
        img.dataset.ch = ch;
        img.dataset.pg = pg;
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        if (highlight === 'changed') img.classList.add('ill-changed');
        panel.insertBefore(img, panel.querySelector('.page-number'));
        // Remove text-only class from parent spread
        var spread = panel.closest('.spread');
        if (spread) spread.classList.remove('text-only');
      });
    }
  }

  // ── Undo ──
  function undo() {
    if (undoStack.length === 0) return;
    var action = undoStack.pop();
    redoStack.push(action);

    if (action.type === 'swap') {
      ILL_DATA[action.a.idx].url = action.a.url;
      ILL_DATA[action.a.idx].info = action.a.info;
      ILL_DATA[action.b.idx].url = action.b.url;
      ILL_DATA[action.b.idx].info = action.b.info;
      updateIllInDOM(action.a.ch, action.a.pg, action.a.url, '');
      updateIllInDOM(action.b.ch, action.b.pg, action.b.url, '');
    } else if (action.type === 'remove') {
      ILL_DATA[action.idx].url = action.url;
      ILL_DATA[action.idx].info = action.info;
      updateIllInDOM(action.ch, action.pg, action.url, '');
    } else if (action.type === 'comment') {
      ILL_DATA[action.idx].comment = action.prevComment || undefined;
      updateIllInDOM(action.ch, action.pg, ILL_DATA[action.idx].url, '');
    } else if (action.type === 'assign') {
      ILL_DATA[action.idx].url = action.prevUrl;
      ILL_DATA[action.idx].info = action.prevInfo;
      updateIllInDOM(action.ch, action.pg, action.prevUrl, '');
    }
    markUnsaved();
    autoSave();
  }

  // ── Redo ──
  function redo() {
    if (redoStack.length === 0) return;
    var action = redoStack.pop();
    undoStack.push(action);

    if (action.type === 'swap') {
      var tmpUrl = ILL_DATA[action.a.idx].url;
      var tmpInfo = ILL_DATA[action.a.idx].info;
      ILL_DATA[action.a.idx].url = ILL_DATA[action.b.idx].url;
      ILL_DATA[action.a.idx].info = ILL_DATA[action.b.idx].info;
      ILL_DATA[action.b.idx].url = tmpUrl;
      ILL_DATA[action.b.idx].info = tmpInfo;
      updateIllInDOM(action.a.ch, action.a.pg, ILL_DATA[action.a.idx].url, 'changed');
      updateIllInDOM(action.b.ch, action.b.pg, ILL_DATA[action.b.idx].url, 'changed');
    } else if (action.type === 'remove') {
      ILL_DATA[action.idx].url = '';
      ILL_DATA[action.idx].info = 'text-only';
      updateIllInDOM(action.ch, action.pg, '', 'removed');
    } else if (action.type === 'comment') {
      ILL_DATA[action.idx].comment = action.comment;
      updateIllInDOM(action.ch, action.pg, ILL_DATA[action.idx].url, 'commented');
    } else if (action.type === 'assign') {
      ILL_DATA[action.idx].url = action.newUrl;
      ILL_DATA[action.idx].info = action.newInfo;
      updateIllInDOM(action.ch, action.pg, action.newUrl, 'changed');
    }
    markUnsaved();
    autoSave();
  }

  // ── Save CSV ──
  function saveCSV(versioned) {
    var lines = ['chapter,page,image_url,image_info,comment'];
    for (var i = 0; i < ILL_DATA.length; i++) {
      var d = ILL_DATA[i];
      var url = d.url || '';
      var info = (d.info || 'text-only').replace(/"/g, '""');
      var comment = (d.comment || '').replace(/"/g, '""');
      lines.push(d.ch + ',' + d.pg + ',"' + url + '","' + info + '","' + comment + '"');
    }
    var csv = lines.join('\\n');
    var blob = new Blob([csv], { type: 'text/csv' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    if (versioned) {
      var ts = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
      a.download = 'illustration-assignments-' + ts + '.csv';
    } else {
      a.download = 'illustration-assignments.csv';
    }
    a.click();
    URL.revokeObjectURL(a.href);
    markSaved();
    // Show save notification
    var notify = document.getElementById('saveNotify');
    if (notify) {
      notify.textContent = versioned ? 'Saved as new version!' : 'Saved!';
      notify.style.display = 'block';
      setTimeout(function() { notify.style.display = 'none'; }, 1500);
    }
  }

  // ── Global keyboard shortcuts ──
  document.addEventListener('keydown', function(e) {
    // Page-action modal: let it handle its own keys
    if (pageActionModal.classList.contains('active')) {
      if (e.key === 'Escape') { e.preventDefault(); closePageAction(); }
      return;
    }

    // Carousel navigation
    if (carouselOpen) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); carouselPrev(); return; }
      if (e.key === 'ArrowRight') { e.preventDefault(); carouselNext(); return; }
      if (e.key === 'Enter') { e.preventDefault(); doSwapWithCarousel(); return; }
      if (e.key === 'Delete') { e.preventDefault(); doRemove(sourceIllIdx); closeCarousel(); return; }
      if (e.key === 'Escape') { e.preventDefault(); closeCarousel(); return; }
      return; // Consume all keys while carousel is open
    }

    // Ctrl+Z — undo
    if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
      e.preventDefault();
      undo();
      return;
    }

    // Ctrl+Y / Ctrl+Shift+Z — redo
    if (e.ctrlKey && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
      e.preventDefault();
      redo();
      return;
    }

    // Ctrl+S — save
    if (e.ctrlKey && e.key === 's') {
      e.preventDefault();
      saveCSV(false);
      return;
    }

    // F12 — save new version
    if (e.key === 'F12') {
      e.preventDefault();
      saveCSV(true);
      return;
    }
  });

  // ── Download CSV button (visible on toolbar, works on tablet) ──
  var dlBtn = document.getElementById('downloadCsvBtn');
  if (dlBtn) {
    dlBtn.addEventListener('click', function() {
      saveCSV(false);
    });
  }

  // Warn before leaving with unsaved changes
  window.addEventListener('beforeunload', function(e) {
    if (unsavedChanges && undoStack.length > 0) {
      e.preventDefault();
      e.returnValue = '';
    }
  });
})();

// ── Autoplay mode ──
(function() {
  var params = new URLSearchParams(window.location.search);
  var isAutoplay = params.has('autoplay');

  if (isAutoplay) {
    var startOverlay = document.createElement('div');
    startOverlay.id = 'autoplayStart';
    startOverlay.style.cssText = 'position:fixed;inset:0;z-index:9999;background:rgba(44,24,16,0.92);display:flex;align-items:center;justify-content:center;cursor:pointer;';
    startOverlay.innerHTML = '<div style="text-align:center;color:white;font-family:Georgia,serif;">'
      + '<div style="font-size:72px;margin-bottom:20px;">&#9654;</div>'
      + '<div style="font-size:20px;letter-spacing:3px;color:#d4a76a;">TAP TO START READING</div>'
      + '<div style="font-size:12px;margin-top:12px;color:#a08060;letter-spacing:1px;">ALICE\\'S ADVENTURES IN WONDERLAND</div>'
      + '</div>';
    document.body.appendChild(startOverlay);

    startOverlay.addEventListener('click', function() {
      startOverlay.remove();
      document.documentElement.requestFullscreen().catch(function() {});
      var playBtn = document.getElementById('playBtn');
      if (playBtn) playBtn.click();
    });
  }
})();

// ── Voice Assistant ──
(function() {
  var voiceBtn = document.getElementById('voiceBtn');
  var popup = document.getElementById('voicePopup');
  var status = document.getElementById('voiceStatus');
  var answerEl = document.getElementById('voiceAnswer');
  if (!voiceBtn) return;

  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    voiceBtn.title = 'Voice not supported in this browser';
    voiceBtn.style.opacity = '0.3';
    voiceBtn.style.cursor = 'not-allowed';
    return;
  }

  var recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.continuous = false;

  var isListening = false;
  var hideTimer;

  function getContext() {
    // Find which spread is currently visible
    var spreads = document.querySelectorAll('.spread');
    var mid = window.innerHeight / 2;
    for (var i = 0; i < spreads.length; i++) {
      var rect = spreads[i].getBoundingClientRect();
      if (rect.top <= mid && rect.bottom >= mid) {
        var id = spreads[i].id || spreads[i].dataset.spread || '';
        // Get any visible text
        var textBlock = spreads[i].querySelector('.text-block');
        var text = textBlock ? textBlock.textContent.substring(0, 200).trim() : '';
        var chLabel = document.getElementById('currentChLabel');
        var ch = chLabel ? chLabel.textContent : '';
        return ch + ' (' + id + '). Page text: ' + text;
      }
    }
    return 'reading Alice in Wonderland';
  }

  voiceBtn.addEventListener('click', function() {
    if (isListening) {
      recognition.stop();
      return;
    }
    isListening = true;
    voiceBtn.classList.add('listening');
    popup.classList.add('visible');
    status.textContent = 'Listening... speak your question!';
    answerEl.textContent = '';
    clearTimeout(hideTimer);
    recognition.start();
  });

  recognition.addEventListener('result', function(e) {
    var transcript = e.results[0][0].transcript;
    isListening = false;
    voiceBtn.classList.remove('listening');
    voiceBtn.classList.add('thinking');
    status.textContent = 'You asked: "' + transcript + '"';

    fetch('http://localhost:3457/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: transcript, context: getContext() })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      voiceBtn.classList.remove('thinking');
      if (data.answer) {
        answerEl.textContent = data.answer;
        // Read aloud
        var utterance = new SpeechSynthesisUtterance(data.answer);
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        // Try to find a friendly voice
        var voices = speechSynthesis.getVoices();
        for (var v = 0; v < voices.length; v++) {
          if (voices[v].name.indexOf('Female') !== -1 || voices[v].name.indexOf('Samantha') !== -1) {
            utterance.voice = voices[v];
            break;
          }
        }
        speechSynthesis.speak(utterance);
        // Auto-hide popup after speech ends
        utterance.addEventListener('end', function() {
          hideTimer = setTimeout(function() { popup.classList.remove('visible'); }, 5000);
        });
      } else {
        answerEl.textContent = data.error || 'Sorry, I could not answer that.';
      }
    })
    .catch(function() {
      voiceBtn.classList.remove('thinking');
      answerEl.textContent = 'Voice assistant not available. Start it with: node scripts/voice-proxy.mjs';
    });
  });

  recognition.addEventListener('error', function() {
    isListening = false;
    voiceBtn.classList.remove('listening');
    status.textContent = 'Could not hear you. Try again!';
    hideTimer = setTimeout(function() { popup.classList.remove('visible'); }, 5000);
  });

  recognition.addEventListener('end', function() {
    if (isListening) {
      isListening = false;
      voiceBtn.classList.remove('listening');
    }
  });

  // Click popup to keep it open longer
  popup.addEventListener('click', function() {
    clearTimeout(hideTimer);
  });
})();
</script>
</body>
</html>`;

// ── Write Output ─────────────────────────────────────────────────────

writeFileSync(resolve(outputDir, 'book.html'), bookHtml);

console.log(`\n  book.html — unified book with ${chapterNums.length} chapters`);
console.log(`  ${globalPageNum} total pages, ${totalContentPages} content pages, ${totalIll} illustrations`);
console.log(`  Audio: ${isUnifiedAudio ? 'unified (1 file)' : 'per-chapter'}`);
console.log(`  Mode: ${USE_CAPS ? 'ALL CAPS' : 'lowercase'}${USE_REMAP ? ' + REMAP' : ''}`);
console.log(`\nDone!`);
