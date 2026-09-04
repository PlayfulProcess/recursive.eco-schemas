/**
 * Match illustrations to booklet pages using existing scene descriptions.
 *
 * Reads:
 *   - chapter-book grammar (has illustration metadata with scene descriptions)
 *   - booklet grammar (has page text for each chapter)
 *
 * Outputs:
 *   - CSV for user review: illustration URL, scene, artist, best matching page text, chapter, page
 *   - Updated illustration-assignments.json (after user approves)
 *
 * Strategy:
 *   1. For each chapter, collect all available illustrations (with scenes)
 *   2. For each page in that chapter, score each illustration by keyword overlap
 *   3. Assign illustrations to pages greedily (best match first, no duplicates)
 *   4. Output assignments for user verification
 *
 * Usage:
 *   node scripts/match-illustrations-to-pages.mjs           # Output CSV
 *   node scripts/match-illustrations-to-pages.mjs --apply    # Also update illustration-assignments.json
 */
import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Load grammars ──
const chapterBookPath = resolve(__dirname, '../grammars/alice-in-wonderland-chapter-book/grammar.json');
const bookletGrammarPath = resolve(__dirname, '../grammars/alice-5-minute-stories/grammar.json');
const assignmentsPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-assignments.json');

const chapterBook = JSON.parse(readFileSync(chapterBookPath, 'utf8'));
const bookletGrammar = JSON.parse(readFileSync(bookletGrammarPath, 'utf8'));

// ── Build illustration catalog per chapter ──
// Each illustration has: url, artist, scene, edition, chapter_number, item_id
const illustrationsByChapter = {};

for (const item of chapterBook.items) {
  const chNum = item.metadata?.chapter_number;
  if (!chNum) continue;
  if (!illustrationsByChapter[chNum]) illustrationsByChapter[chNum] = [];

  const illustrations = item.metadata?.illustrations || [];
  for (const ill of illustrations) {
    illustrationsByChapter[chNum].push({
      url: ill.url,
      artist: ill.artist || 'Unknown',
      artist_dates: ill.artist_dates || '',
      edition: ill.edition || '',
      scene: ill.scene || '',
      is_primary: ill.is_primary || false,
      item_id: item.id,
      item_name: item.name,
    });
  }
}

// ── Build page text per chapter ──
// Each booklet chapter has sections "Page 1", "Page 2", etc.
const pagesByChapter = {};

for (const item of bookletGrammar.items) {
  const chNum = item.metadata?.source_chapter;
  if (!chNum) continue;

  const pages = [];
  const pageCount = item.metadata?.page_count || 0;
  for (let p = 1; p <= pageCount; p++) {
    const key = `Page ${p}`;
    const text = item.sections?.[key] || '';
    pages.push({ pageNum: p, text: text.substring(0, 500) }); // First 500 chars for matching
  }
  pagesByChapter[chNum] = pages;
}

// ── Text matching utilities ──
function extractKeywords(text) {
  // Remove common words, extract meaningful terms
  const stopWords = new Set([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'that', 'which', 'who',
    'whom', 'this', 'these', 'those', 'it', 'its', 'her', 'his', 'she',
    'he', 'they', 'them', 'their', 'we', 'us', 'our', 'you', 'your',
    'i', 'me', 'my', 'not', 'no', 'so', 'if', 'then', 'than', 'very',
    'just', 'too', 'also', 'still', 'said', 'says', 'say', 'about',
    'up', 'out', 'down', 'into', 'over', 'after', 'before', 'when',
    'how', 'what', 'where', 'there', 'here', 'all', 'each', 'every',
    'both', 'few', 'more', 'most', 'other', 'some', 'such', 'only',
    'same', 'well', 'back', 'even', 'new', 'now', 'old', 'see', 'way',
    'who', 'been', 'being', 'much', 'off', 'little', 'quite', 'got',
    'one', 'two', 'first', 'last', 'long', 'great', 'good', 'own',
    'went', 'came', 'come', 'go', 'going', 'look', 'looked', 'looking',
    'thing', 'things', 'thought', 'know', 'think', 'like', 'make',
    'time', 'take', 'began', 'again', 'never', 'once', 'upon',
  ]);

  return text
    .toLowerCase()
    .replace(/[^a-z\s'-]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 2 && !stopWords.has(w));
}

// Character/entity recognition keywords
const ENTITY_KEYWORDS = {
  'alice': ['alice', 'girl', 'child', 'she', 'herself'],
  'rabbit': ['rabbit', 'white rabbit', 'waistcoat', 'watch', 'hurry'],
  'caterpillar': ['caterpillar', 'hookah', 'mushroom', 'smoke', 'smoking'],
  'cheshire': ['cheshire', 'cat', 'grin', 'grinning', 'vanish'],
  'hatter': ['hatter', 'mad', 'tea', 'tea-party', 'dormouse', 'march hare'],
  'queen': ['queen', 'hearts', 'croquet', 'off with', 'head', 'execution'],
  'king': ['king', 'court', 'trial', 'witness', 'evidence'],
  'duchess': ['duchess', 'baby', 'pig', 'pepper', 'cook', 'kitchen'],
  'mock turtle': ['mock turtle', 'turtle', 'gryphon', 'griffin', 'lobster', 'quadrille'],
  'mouse': ['mouse', 'pool', 'tears', 'swimming', 'tale', 'tail'],
  'dodo': ['dodo', 'caucus', 'race', 'thimble', 'prize'],
  'bill': ['bill', 'lizard', 'chimney', 'arm', 'window'],
  'pigeon': ['pigeon', 'serpent', 'egg', 'eggs', 'neck', 'tree'],
  'cards': ['cards', 'painting', 'roses', 'gardeners', 'soldiers'],
  'knave': ['knave', 'tarts', 'stole', 'trial', 'jury'],
  'falling': ['falling', 'fall', 'fell', 'tunnel', 'down', 'deep'],
  'growing': ['growing', 'grew', 'tall', 'large', 'small', 'tiny', 'shrink'],
  'drink me': ['drink', 'bottle', 'drink me', 'shrink', 'small'],
  'eat me': ['eat', 'cake', 'eat me', 'grow', 'large'],
  'crying': ['cry', 'crying', 'tears', 'weep', 'pool'],
  'croquet': ['croquet', 'flamingo', 'hedgehog', 'mallet'],
};

function scoreMatch(sceneText, pageText) {
  const sceneWords = extractKeywords(sceneText);
  const pageWords = extractKeywords(pageText);
  const pageWordSet = new Set(pageWords);

  if (sceneWords.length === 0) return 0;

  // Direct keyword overlap
  let overlap = 0;
  for (const w of sceneWords) {
    if (pageWordSet.has(w)) overlap += 2;
    // Partial match (stem-like)
    for (const pw of pageWords) {
      if (pw.startsWith(w.substring(0, 4)) || w.startsWith(pw.substring(0, 4))) {
        overlap += 0.5;
        break;
      }
    }
  }

  // Entity matching bonus: if scene mentions a character, check if page text does too
  for (const [entity, keywords] of Object.entries(ENTITY_KEYWORDS)) {
    const sceneHasEntity = keywords.some(k => sceneText.toLowerCase().includes(k));
    const pageHasEntity = keywords.some(k => pageText.toLowerCase().includes(k));
    if (sceneHasEntity && pageHasEntity) overlap += 3;
  }

  // Normalize by scene word count
  return overlap / Math.max(1, sceneWords.length);
}

// ── Match illustrations to pages ──
const results = [];
const chapterNums = Object.keys(pagesByChapter).map(Number).sort((a, b) => a - b);

for (const chNum of chapterNums) {
  const illustrations = illustrationsByChapter[chNum] || [];
  const pages = pagesByChapter[chNum] || [];

  if (illustrations.length === 0 || pages.length === 0) continue;

  // Score every illustration against every page
  const scores = [];
  for (const ill of illustrations) {
    for (const page of pages) {
      const score = scoreMatch(
        ill.scene + ' ' + ill.item_name + ' ' + ill.item_id.replace(/-/g, ' '),
        page.text
      );
      scores.push({ ill, page, score });
    }
  }

  // Sort by score (best first)
  scores.sort((a, b) => b.score - a.score);

  // Greedy assignment: best score first, no illustration or page used twice
  const usedIllustrations = new Set();
  const usedPages = new Set();
  const assignments = [];

  for (const { ill, page, score } of scores) {
    if (usedIllustrations.has(ill.url) || usedPages.has(page.pageNum)) continue;
    assignments.push({ ill, page, score });
    usedIllustrations.add(ill.url);
    usedPages.add(page.pageNum);
  }

  // Sort assignments by page number for output
  assignments.sort((a, b) => a.page.pageNum - b.page.pageNum);

  // Pick best illustration for cover (page 0) — use the primary or highest-scored unused
  const coverIll = illustrations.find(i => i.is_primary && !usedIllustrations.has(i.url))
    || illustrations.find(i => !usedIllustrations.has(i.url))
    || illustrations[0];

  results.push({
    chapter: chNum,
    cover: coverIll,
    assignments,
    unassignedPages: pages.filter(p => !usedPages.has(p.pageNum)).map(p => p.pageNum),
    unassignedIllustrations: illustrations.filter(i => !usedIllustrations.has(i.url)),
  });
}

// ── Output CSV ──
const csvLines = ['Chapter,Page,Score,Scene Description,Artist,Image URL,Page Text Preview'];

for (const ch of results) {
  // Cover
  csvLines.push([
    ch.chapter,
    0,
    'cover',
    `"${(ch.cover.scene || 'Cover image').replace(/"/g, '""')}"`,
    `"${ch.cover.artist}"`,
    ch.cover.url,
    `"Chapter ${ch.chapter} Cover"`,
  ].join(','));

  // Page assignments
  for (const { ill, page, score } of ch.assignments) {
    const preview = page.text.substring(0, 80).replace(/\n/g, ' ').replace(/"/g, '""');
    csvLines.push([
      ch.chapter,
      page.pageNum,
      score.toFixed(2),
      `"${(ill.scene || '').replace(/"/g, '""')}"`,
      `"${ill.artist}"`,
      ill.url,
      `"${preview}"`,
    ].join(','));
  }

  // Unassigned pages (no matching illustration)
  for (const pNum of ch.unassignedPages) {
    const page = pagesByChapter[ch.chapter].find(p => p.pageNum === pNum);
    const preview = page ? page.text.substring(0, 80).replace(/\n/g, ' ').replace(/"/g, '""') : '';
    csvLines.push([
      ch.chapter,
      pNum,
      '0.00',
      '"(no illustration available)"',
      '""',
      '',
      `"${preview}"`,
    ].join(','));
  }
}

const csvPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-matching-review.csv');
writeFileSync(csvPath, csvLines.join('\n'));
console.log(`\nCSV written: ${csvPath}`);
console.log(`${csvLines.length - 1} entries (${results.reduce((s, r) => s + r.assignments.length, 0)} matched, ${results.reduce((s, r) => s + r.unassignedPages.length, 0)} unassigned pages)\n`);

// Summary per chapter
for (const ch of results) {
  const total = pagesByChapter[ch.chapter].length;
  const matched = ch.assignments.length;
  const avgScore = ch.assignments.length > 0
    ? (ch.assignments.reduce((s, a) => s + a.score, 0) / ch.assignments.length).toFixed(2)
    : '0';
  console.log(`  Ch ${String(ch.chapter).padStart(2)}: ${matched}/${total} pages matched (avg score: ${avgScore}), ${ch.unassignedIllustrations.length} unused illustrations`);
}

// ── Optionally apply to illustration-assignments.json ──
if (process.argv.includes('--apply')) {
  const newAssignments = [];

  for (const ch of results) {
    const chName = bookletGrammar.items.find(i => i.metadata?.source_chapter === ch.chapter)?.name || `Chapter ${ch.chapter}`;

    // Cover
    newAssignments.push({
      chapter: ch.chapter,
      page: 0,
      label: `Ch${ch.chapter} Cover`,
      text_preview: chName,
      image_url: ch.cover.url,
      image_info: `${ch.cover.artist} — ${ch.cover.scene || 'chapter cover'}`,
    });

    // All pages
    const pages = pagesByChapter[ch.chapter];
    const assignmentMap = {};
    for (const { ill, page } of ch.assignments) {
      assignmentMap[page.pageNum] = ill;
    }

    for (const page of pages) {
      const ill = assignmentMap[page.pageNum];
      const preview = page.text.substring(0, 60).replace(/\n/g, ' ') + '...';
      newAssignments.push({
        chapter: ch.chapter,
        page: page.pageNum,
        label: `Ch${ch.chapter} p${page.pageNum}`,
        text_preview: preview,
        image_url: ill ? ill.url : '',
        image_info: ill ? `${ill.artist} — ${ill.scene}` : 'text-only',
      });
    }
  }

  writeFileSync(assignmentsPath, JSON.stringify(newAssignments, null, 2));
  console.log(`\nApplied! Updated ${assignmentsPath} with ${newAssignments.length} entries.`);
}
