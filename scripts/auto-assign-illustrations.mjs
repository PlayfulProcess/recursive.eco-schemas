/**
 * Auto-assign illustrations to blank pages.
 * Reads book.html, finds blank pages, matches unused illustrations.
 * Updates illustration-assignments.json in the flat array format.
 */
import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const bookPath = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets/book.html');
const assigPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-assignments.json');
const html = readFileSync(bookPath, 'utf8');

// Parse ILL_DATA and UNUSED_ILLS from book
const ILL_DATA = JSON.parse(html.match(/var ILL_DATA = (\[[\s\S]*?\]);/)[1]);
const UNUSED_ILLS = JSON.parse(html.match(/var UNUSED_ILLS = (\[[\s\S]*?\]);/)[1]);

// Get page text from HTML
const pageTexts = {};
const re = /data-ch="(\d+)" data-local-page="(\d+)">\s*<div class="text-block">([\s\S]*?)<\/div>/g;
let m;
while ((m = re.exec(html)) !== null) {
  const key = `${m[1]}-${m[2]}`;
  const text = m[3].replace(/<[^>]+>/g, '').replace(/&[^;]+;/g, ' ').replace(/\s+/g, ' ').trim();
  pageTexts[key] = text;
}

// Current assignments (the flat array)
let assignments = JSON.parse(readFileSync(assigPath, 'utf8'));
const assignedMap = new Map();
for (const a of assignments) {
  assignedMap.set(`${a.chapter}-${a.page}`, a);
}

// Find blank pages (in ILL_DATA, url empty, not a cover)
const blankPages = ILL_DATA.filter(d => !d.url && d.pg > 0);
// Also skip pages already assigned in JSON
const trulyBlank = blankPages.filter(d => !assignedMap.has(`${d.ch}-${d.pg}`) || !assignedMap.get(`${d.ch}-${d.pg}`).image_url);

console.log(`Blank pages in book: ${blankPages.length}`);
console.log(`Truly unassigned: ${trulyBlank.length}`);
console.log(`Available unused illustrations: ${UNUSED_ILLS.length}`);

// Scene matching
function matchScore(text, info, ch) {
  if (!text || !info) return 0;
  const tl = text.toLowerCase();
  const il = info.toLowerCase();
  let score = 0;

  // Character matches
  const chars = [
    ['alice', 4], ['rabbit', 5], ['queen', 5], ['king', 4], ['hatter', 6],
    ['cheshire', 6], ['duchess', 5], ['dormouse', 6], ['gryphon', 6], ['griffin', 6],
    ['mock turtle', 7], ['caterpillar', 6], ['dodo', 5], ['pigeon', 5],
    ['flamingo', 6], ['hedgehog', 6], ['cook', 4], ['mouse', 4], ['bill', 4],
    ['knave', 5], ['march hare', 6], ['lobster', 6]
  ];
  for (const [c, w] of chars) {
    if (tl.includes(c) && il.includes(c)) score += w;
  }

  // Scene/object matches
  const scenes = [
    ['tea party', 8], ['tea-party', 8], ['mushroom', 7], ['hookah', 6],
    ['croquet', 8], ['garden', 5], ['trial', 8], ['court', 6],
    ['pool of tears', 8], ['caucus race', 8], ['bottle', 5], ['drink me', 7],
    ['eat me', 7], ['golden key', 6], ['little door', 5], ['cards', 5],
    ['baby', 4], ['pig', 4], ['pepper', 5], ['soup', 6], ['lobster quadrille', 8],
    ['falling', 5], ['growing', 5], ['shrink', 5], ['sister', 4], ['dream', 4],
    ['tarts', 5], ['jury', 5], ['witness', 4], ['treacle', 5], ['well', 3],
    ['roses', 5], ['painting', 5], ['flamingo', 6], ['executioner', 5],
    ['manuscript', 3], ['chapter', 3]
  ];
  for (const [s, w] of scenes) {
    if (tl.includes(s) && il.includes(s)) score += w;
  }

  // Chapter affinity — manuscript pages near their chapter
  if (il.includes('manuscript') || il.includes('carroll')) {
    const chMatch = il.match(/chapter\s+([ivxlcdm]+|[0-9]+)/i);
    if (chMatch) {
      const roman = { 'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10, 'xi': 11, 'xii': 12 };
      const mCh = roman[chMatch[1].toLowerCase()] || parseInt(chMatch[1]);
      if (mCh === ch) score += 10; // Same chapter!
      else if (Math.abs(mCh - ch) === 1) score += 3;
    }
  }

  return score;
}

// Assign Alice Liddell photos strategically
const photoPlans = [
  { match: 'portrait', ch: 1, reason: 'The real Alice — chapter opener' },
  { match: 'beggar-girl', ch: 6, reason: 'Alice as beggar suits Duchess chapter' },
  { match: 'edith-ina-alice', ch: 9, reason: 'Three sisters — Mock Turtle school days' },
  { match: 'age-20', ch: 12, reason: 'Grown-up Alice — story ends' },
  { match: 'hargreaves-1932', ch: 12, reason: 'Alice at 80 — final reflection' },
  { match: 'feigned-sleep', ch: 3, reason: 'Dreamy caterpillar chapter' },
  { match: 'alice-liddell-1859', ch: 5, reason: 'Young Alice mid-book' },
  { match: 'lorina-edith-alice-1859', ch: 7, reason: 'Sisters at the tea party' },
  { match: 'alice-ina-harry', ch: 4, reason: 'Liddell children in garden' },
  { match: 'alice-grown-up.jpg', ch: 10, reason: 'Grown up for late chapters' },
  { match: 'cameron', ch: 11, reason: 'Artistic photo for trial chapter' },
];

const newAssignments = [];
const usedUrls = new Set();

// Track which blank pages we've filled
const filledPages = new Set();

// 1. Assign photos
for (const plan of photoPlans) {
  const photo = UNUSED_ILLS.find(u => u.url.includes(plan.match) && !usedUrls.has(u.url));
  if (!photo) continue;
  const candidates = trulyBlank.filter(bp => bp.ch === plan.ch && !filledPages.has(`${bp.ch}-${bp.pg}`));
  if (candidates.length === 0) continue;
  const target = candidates[Math.floor(candidates.length / 2)];
  newAssignments.push({
    chapter: target.ch, page: target.pg,
    image_url: photo.url, image_info: photo.info,
    comment: plan.reason
  });
  filledPages.add(`${target.ch}-${target.pg}`);
  usedUrls.add(photo.url);
  console.log(`  Photo: Ch${target.ch} pg${target.pg} ← ${photo.info.substring(0, 50)} (${plan.reason})`);
}

// 2. Assign remaining unused illustrations by score
const remainingBlank = trulyBlank.filter(bp => !filledPages.has(`${bp.ch}-${bp.pg}`));
const remainingUnused = UNUSED_ILLS.filter(u => !usedUrls.has(u.url));

console.log(`\nAfter photos: ${remainingBlank.length} blank, ${remainingUnused.length} unused`);

const scored = [];
for (const bp of remainingBlank) {
  const text = pageTexts[`${bp.ch}-${bp.pg}`] || '';
  for (const u of remainingUnused) {
    if (usedUrls.has(u.url)) continue;
    const score = matchScore(text, u.info, bp.ch);
    if (score > 0) {
      scored.push({ ch: bp.ch, pg: bp.pg, url: u.url, info: u.info, score, source: u.source });
    }
  }
}

scored.sort((a, b) => b.score - a.score);
for (const s of scored) {
  if (filledPages.has(`${s.ch}-${s.pg}`) || usedUrls.has(s.url)) continue;
  newAssignments.push({
    chapter: s.ch, page: s.pg,
    image_url: s.url, image_info: s.info,
    comment: `auto-matched score=${s.score}`
  });
  filledPages.add(`${s.ch}-${s.pg}`);
  usedUrls.add(s.url);
  console.log(`  Match: Ch${s.ch} pg${s.pg} ← ${s.info.substring(0, 55)} (score=${s.score})`);
}

// Merge new assignments into existing
for (const na of newAssignments) {
  const existing = assignments.findIndex(a => a.chapter === na.chapter && a.page === na.page);
  if (existing >= 0) {
    assignments[existing] = na;
  } else {
    assignments.push(na);
  }
}

// Sort by chapter then page
assignments.sort((a, b) => a.chapter - b.chapter || a.page - b.page);

writeFileSync(assigPath, JSON.stringify(assignments, null, 2));
console.log(`\n✓ Updated ${assigPath}`);
console.log(`  New assignments: ${newAssignments.length}`);
console.log(`  Total in file: ${assignments.length}`);
console.log(`  Still blank: ${trulyBlank.length - newAssignments.length}`);
