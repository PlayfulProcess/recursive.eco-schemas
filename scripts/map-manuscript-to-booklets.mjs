/**
 * Map Carroll's manuscript page scans to the published Alice chapter book.
 *
 * Carroll's "Alice's Adventures Under Ground" (1864) has 4 chapters and 37 illustrations.
 * The published "Alice's Adventures in Wonderland" (1865) has 12 chapters.
 *
 * Manuscript chapter mapping to published chapters:
 *   Manuscript Ch I  (pages 1-44) → Published Ch 1-4
 *     - Ch 1: Down the Rabbit-Hole (pages 1-18)
 *     - Ch 2: Pool of Tears (pages 18-28)
 *     - Ch 3: Caucus Race (pages 28-36)
 *     - Ch 4: Rabbit Sends Bill (pages 36-44)
 *   Manuscript Ch II (pages 45-59) → Published Ch 5-6
 *     - Ch 5: Caterpillar (pages 45-52)
 *     - Ch 6: Pig & Pepper (pages 52-59)
 *   Manuscript Ch III(pages 60-77) → Published Ch 7-10
 *     - Ch 7: Mad Tea Party (pages 60-66)
 *     - Ch 8: Queen's Croquet (pages 66-72)
 *     - Ch 9: Mock Turtle (pages 72-75)
 *     - Ch 10: Lobster Quadrille (pages 75-77)
 *   Manuscript Ch IV (pages 78-90) → Published Ch 11-12
 *     - Ch 11: Who Stole the Tarts (pages 78-83)
 *     - Ch 12: Alice's Evidence (pages 83-90)
 *
 * Image index to manuscript page mapping:
 *   Image 00 = frontispiece/title
 *   Image 01 = pages 1-2 (each image is a 2-page spread)
 *   Image N  = pages (2N-1) to 2N
 *   Image 45 = pages 89-90
 *   Image 46 = back photo
 *
 * Pages with illustrations (from known scholarly references):
 *   p1 (title "Chapter I"), p4 (Alice bored), p6 (rabbit), p8 (falling), p10 (hall of doors),
 *   p13 (drink me), p15 (tiny Alice), p18-19 (growing/pool), p20 (pool of tears),
 *   p23 (mouse in pool), p25 (the mouse's tale), p29 (caucus race), p32 (Dodo presents thimble),
 *   p35 (comfits), p37 (arm in window), p38 (Bill up chimney), p40 (caterpillar),
 *   p45 (Chapter II title), p47 (pigeon/serpent), p49 (Cheshire cat in tree),
 *   p52 (duchess kitchen), p54 (baby/pig), p56 (Cheshire cat grin), p58 (tea party),
 *   p60 (Chapter III title), p62 (painting roses), p64 (croquet flamingo),
 *   p67 (Gryphon), p69 (lobster quadrille), p72 (Mock Turtle singing),
 *   p78 (Chapter IV title), p80 (court scene), p82 (Alice growing in court),
 *   p85 (pack of cards), p88 (Alice photo), p90 (end drawing)
 */

import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const r2Base = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/manuscript-under-ground';

// Manuscript page ranges for published chapters (approximate, based on text alignment)
const chapterPageRanges = {
  1: { start: 1, end: 18, name: 'Down the Rabbit-Hole' },
  2: { start: 18, end: 28, name: 'The Pool of Tears' },
  3: { start: 28, end: 36, name: 'A Caucus-Race and a Long Tale' },
  4: { start: 36, end: 45, name: 'The Rabbit Sends in a Little Bill' },
  5: { start: 45, end: 52, name: 'Advice from a Caterpillar' },
  6: { start: 52, end: 60, name: 'Pig and Pepper' },
  7: { start: 60, end: 66, name: 'A Mad Tea-Party' },
  8: { start: 66, end: 72, name: "The Queen's Croquet-Ground" },
  9: { start: 72, end: 76, name: "The Mock Turtle's Story" },
  10: { start: 76, end: 78, name: 'The Lobster Quadrille' },
  11: { start: 78, end: 83, name: 'Who Stole the Tarts?' },
  12: { start: 83, end: 91, name: "Alice's Evidence" },
};

// Known illustrated manuscript pages with scene descriptions
// Format: manuscript page → scene description + which published chapter it maps to
const illustratedPages = [
  { msPage: 1,  scene: 'Chapter I title page — Alice bored by the river', chapter: 1 },
  { msPage: 4,  scene: 'Alice sitting with sister, beginning to get tired', chapter: 1 },
  { msPage: 6,  scene: 'White Rabbit running by with pocket watch', chapter: 1 },
  { msPage: 8,  scene: 'Alice falling down the rabbit-hole', chapter: 1 },
  { msPage: 10, scene: 'Alice in the hall of doors, finding the golden key', chapter: 1 },
  { msPage: 13, scene: 'Alice drinking from the DRINK ME bottle', chapter: 1 },
  { msPage: 15, scene: 'Tiny Alice trying to reach the key on the table', chapter: 1 },
  { msPage: 18, scene: 'Alice growing enormously tall — curiouser and curiouser', chapter: 2 },
  { msPage: 20, scene: 'Alice swimming in the pool of her own tears', chapter: 2 },
  { msPage: 23, scene: 'Alice and the Mouse swimming in the pool of tears', chapter: 2 },
  { msPage: 25, scene: "The Mouse's Tale written in tail/spiral shape", chapter: 3 },
  { msPage: 29, scene: 'The Caucus-Race — all the animals running in circles', chapter: 3 },
  { msPage: 32, scene: 'The Dodo presenting Alice with her own thimble as prize', chapter: 3 },
  { msPage: 35, scene: 'Alice distributing comfits to the animals', chapter: 3 },
  { msPage: 37, scene: "Alice's arm stuck in the White Rabbit's window", chapter: 4 },
  { msPage: 38, scene: 'Bill the Lizard being kicked up the chimney', chapter: 4 },
  { msPage: 40, scene: 'The Caterpillar on the mushroom smoking a hookah', chapter: 5 },
  { msPage: 45, scene: 'Chapter II title page — Advice from a Caterpillar', chapter: 5 },
  { msPage: 47, scene: 'The Pigeon calling Alice a serpent in the tree', chapter: 5 },
  { msPage: 49, scene: 'The Cheshire Cat sitting in a tree, grinning', chapter: 6 },
  { msPage: 52, scene: "The Duchess's kitchen — cook, baby, pepper, and Cheshire Cat", chapter: 6 },
  { msPage: 54, scene: 'Alice holding the baby that turns into a pig', chapter: 6 },
  { msPage: 56, scene: 'The Cheshire Cat grin fading, leaving only the smile', chapter: 6 },
  { msPage: 58, scene: 'The Mad Tea-Party — Hatter, March Hare, and Dormouse', chapter: 7 },
  { msPage: 60, scene: 'Chapter III title page — The Queen of Hearts', chapter: 8 },
  { msPage: 62, scene: 'Card gardeners painting the white roses red', chapter: 8 },
  { msPage: 64, scene: 'Alice playing croquet with a flamingo as mallet', chapter: 8 },
  { msPage: 67, scene: 'The Gryphon sleeping by the seaside', chapter: 9 },
  { msPage: 69, scene: 'The Lobster Quadrille dance by the sea', chapter: 10 },
  { msPage: 72, scene: 'The Mock Turtle singing Turtle Soup', chapter: 9 },
  { msPage: 78, scene: 'Chapter IV title page — The court trial', chapter: 11 },
  { msPage: 80, scene: 'The King and Queen of Hearts on their thrones, court in session', chapter: 11 },
  { msPage: 82, scene: 'Alice growing large in the courtroom', chapter: 12 },
  { msPage: 85, scene: 'A pack of cards flying at Alice', chapter: 12 },
  { msPage: 88, scene: 'Photograph of Alice Liddell by Lewis Carroll', chapter: 12 },
  { msPage: 90, scene: 'Final page — the end', chapter: 12 },
];

// Also add some text-only manuscript pages for covers/gaps
const textOnlyPages = [
  { msPage: 0, scene: 'Frontispiece — A Christmas Gift to a Dear Child', chapter: 1 },
  { msPage: 2, scene: 'Opening text — Alice beginning to get tired', chapter: 1 },
  { msPage: 19, scene: "Alice crying — the Pool of Tears forming", chapter: 2 },
  { msPage: 27, scene: "The Mouse tells its history — the driest thing", chapter: 3 },
  { msPage: 43, scene: "Alice hears pattering of little feet — the White Rabbit returns", chapter: 4 },
  { msPage: 50, scene: "WHO ARE YOU? said the Caterpillar", chapter: 5 },
  { msPage: 59, scene: "The Duchess's moral — flamingos and mustard", chapter: 6 },
  { msPage: 65, scene: "Off with her head! cried the Queen", chapter: 8 },
  { msPage: 74, scene: "Will you walk a little faster?", chapter: 10 },
  { msPage: 84, scene: "Sentence first, verdict afterwards", chapter: 12 },
];

// Convert manuscript page number to image index
function msPageToImageIndex(msPage) {
  if (msPage === 0) return 0; // frontispiece
  return Math.ceil(msPage / 2);
}

function msPageToR2Url(msPage) {
  const imgIdx = msPageToImageIndex(msPage);
  const num = String(imgIdx).padStart(2, '0');
  return `${r2Base}/manuscript-page-${num}.jpg`;
}

// Load current assignments
const assignmentsPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-assignments.json');
const assignments = JSON.parse(readFileSync(assignmentsPath, 'utf8'));

// Load booklet grammar for page text
const bookletPath = resolve(__dirname, '../grammars/alice-5-minute-stories/grammar.json');
const booklet = JSON.parse(readFileSync(bookletPath, 'utf8'));

const pageTextByChapter = {};
for (const item of booklet.items) {
  const ch = item.metadata?.source_chapter;
  if (!ch) continue;
  pageTextByChapter[ch] = {};
  for (let p = 1; p <= (item.metadata?.page_count || 0); p++) {
    pageTextByChapter[ch][p] = item.sections?.[`Page ${p}`] || '';
  }
}

// Strategy:
// 1. For each booklet page, check if it currently has a Carroll manuscript illustration (old cropped ones)
// 2. Replace those with the new full-page manuscript scans
// 3. For text-only pages, try to fill them with a relevant manuscript page
// 4. For pages with other artists (Rackham, Tenniel, etc.), keep those but consider swapping low-score matches

// Build a pool of manuscript illustrations available per chapter
const manuscriptPool = {};
for (const ill of [...illustratedPages, ...textOnlyPages]) {
  if (!manuscriptPool[ill.chapter]) manuscriptPool[ill.chapter] = [];
  manuscriptPool[ill.chapter].push({
    url: msPageToR2Url(ill.msPage),
    scene: ill.scene,
    msPage: ill.msPage,
    hasDrawing: illustratedPages.some(p => p.msPage === ill.msPage),
  });
}

// Now update assignments
const usedUrls = new Set();
const newAssignments = [];

for (const a of assignments) {
  const isCarrollManuscript = a.image_url?.includes('lewis-carroll-1864') ||
                               a.image_url?.includes('manuscript') ||
                               a.image_url?.includes('chapter-I') ||
                               a.image_url?.includes('chapter-II') ||
                               a.image_url?.includes('dedication') ||
                               a.image_url?.includes('title-page');
  const isTextOnly = !a.image_url || a.image_url === '';
  const pool = manuscriptPool[a.chapter] || [];

  if (isCarrollManuscript || isTextOnly) {
    // Find best manuscript page for this booklet page
    const pageText = a.page === 0 ? '' : (pageTextByChapter[a.chapter]?.[a.page] || '');
    const textLower = pageText.toLowerCase();

    // Score each manuscript page against this booklet page
    let bestMatch = null;
    let bestScore = -1;

    for (const ms of pool) {
      if (usedUrls.has(ms.url)) continue;

      let score = 0;
      const sceneLower = ms.scene.toLowerCase();

      // Keyword matching
      const sceneWords = sceneLower.split(/\s+/).filter(w => w.length > 3);
      for (const w of sceneWords) {
        if (textLower.includes(w)) score += 2;
      }

      // Prefer pages with actual drawings over text-only manuscript pages
      if (ms.hasDrawing) score += 3;

      // For covers, prefer chapter title pages
      if (a.page === 0 && sceneLower.includes('chapter')) score += 5;
      if (a.page === 0 && sceneLower.includes('title')) score += 3;

      if (score > bestScore) {
        bestScore = score;
        bestMatch = ms;
      }
    }

    if (bestMatch) {
      usedUrls.add(bestMatch.url);
      newAssignments.push({
        ...a,
        image_url: bestMatch.url,
        image_info: `Lewis Carroll manuscript — ${bestMatch.scene}`,
      });
    } else {
      // No manuscript available, keep as-is
      newAssignments.push(a);
    }
  } else {
    // Keep non-Carroll illustrations (Rackham, Tenniel, etc.)
    newAssignments.push(a);
  }
}

// Summary
let replaced = 0, kept = 0, filledGaps = 0;
for (let i = 0; i < assignments.length; i++) {
  const old = assignments[i];
  const nw = newAssignments[i];
  if (old.image_url !== nw.image_url) {
    if (!old.image_url || old.image_url === '') filledGaps++;
    else replaced++;
  } else {
    kept++;
  }
}

console.log(`\nResults:`);
console.log(`  Replaced old Carroll manuscripts: ${replaced}`);
console.log(`  Filled text-only gaps: ${filledGaps}`);
console.log(`  Kept as-is: ${kept}`);
console.log(`  Manuscript pages used: ${usedUrls.size} / ${illustratedPages.length + textOnlyPages.length}`);

writeFileSync(assignmentsPath, JSON.stringify(newAssignments, null, 2));
console.log(`\nUpdated: ${assignmentsPath}`);
