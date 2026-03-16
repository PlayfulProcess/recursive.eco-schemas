import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const grammarPath = resolve(__dirname, '../grammars/alice-5-minute-stories/grammar.json');
const g = JSON.parse(readFileSync(grammarPath, 'utf8'));
const bookPath = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets/book.html');
const html = readFileSync(bookPath, 'utf8');

// 1. Get ALL illustrations from grammar
console.log('=== ALL ILLUSTRATIONS IN GRAMMAR ===');
let totalIlls = 0;
const allIlls = [];
const byArtist = {};
for (const item of g.items) {
  if (!item.metadata?.illustrations) continue;
  for (const ill of item.metadata.illustrations) {
    totalIlls++;
    const a = ill.artist || 'unknown';
    byArtist[a] = (byArtist[a] || 0) + 1;
    allIlls.push({ ...ill, itemName: item.name });
  }
}
console.log('Total illustrations in grammar:', totalIlls);
for (const [a, c] of Object.entries(byArtist).sort((x, y) => y[1] - x[1])) {
  console.log('  ' + a + ': ' + c);
}

// 2. Get current ILL_DATA (assigned + text-only)
const illMatch = html.match(/var ILL_DATA = (\[[\s\S]*?\]);/);
const illData = JSON.parse(illMatch[1]);
const usedUrls = new Set(illData.filter(d => d.url).map(d => d.url));
console.log('\n=== CURRENT ASSIGNMENTS ===');
console.log('Total ILL_DATA entries:', illData.length);
console.log('With illustration:', illData.filter(d => d.url).length);
console.log('Text-only (blank):', illData.filter(d => !d.url).length);

// 3. Find unused illustrations
const unused = allIlls.filter(ill => !usedUrls.has(ill.url));
console.log('\n=== UNUSED ILLUSTRATIONS ===');
console.log('Total unused from grammar:', unused.length);
for (const u of unused) {
  console.log(`  [${u.artist}] ${u.scene || u.alt || ''} — from "${u.itemName}"`);
}

// 4. Get text content for each blank page
console.log('\n=== BLANK PAGES TEXT PREVIEW ===');
const blankPages = illData.filter(d => !d.url && d.pg > 0);
// Get chapter text from CHAPTER_TEXT
const ctMatch = html.match(/var CHAPTER_TEXT = (\{[\s\S]*?\});/);
const chapterText = JSON.parse(ctMatch[1]);
for (const bp of blankPages) {
  const chText = chapterText[bp.ch];
  const pageText = chText?.pages?.[bp.pg] || '(no preview)';
  console.log(`  Ch${bp.ch} pg${bp.pg}: ${pageText}`);
}
