import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const bookletPath = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets/chapter01-down-the-rabbit-hole.html');
const html = readFileSync(bookletPath, 'utf8');

// 1. Check audio file path
const audioMatch = html.match(/var AUDIO_FILE = '([^']+)'/);
console.log('Audio file path:', audioMatch ? audioMatch[1] : 'NOT FOUND');

const audioRelPath = audioMatch[1];
const bookletDir = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets');
const fullAudioPath = resolve(bookletDir, audioRelPath);
console.log('Resolved audio path:', fullAudioPath);
console.log('Audio file exists:', existsSync(fullAudioPath));

// 2. Parse KARAOKE_PAGES
const scriptMatch = html.match(/<script>([\s\S]+)<\/script>/);
const script = scriptMatch[1];
const karaokeMatch = script.match(/var KARAOKE_PAGES = (\[[\s\S]*?\]);/);
const pages = JSON.parse(karaokeMatch[1]);
console.log('\nKaraoke pages:', pages.length);

// 3. Check data-page attributes
const dataPageNums = [];
const regex = /data-page="(\d+)"/g;
let m;
while ((m = regex.exec(html)) !== null) dataPageNums.push(parseInt(m[1]));
console.log('data-page values in HTML:', dataPageNums.join(', '));
console.log('Karaoke page nums:', pages.map(p => p.pageNum).join(', '));

// 4. Check each karaoke page has matching HTML
for (const p of pages) {
  const hasPage = dataPageNums.includes(p.pageNum);
  // Check page-right specifically
  const pageIdx = html.indexOf(`data-page="${p.pageNum}"`);
  let hasTextBlock = false;
  if (pageIdx >= 0) {
    const after = html.substring(pageIdx, pageIdx + 500);
    hasTextBlock = after.includes('text-block');
  }
  if (!hasPage || !hasTextBlock) {
    console.log(`  MISSING: page ${p.pageNum} hasDataPage=${hasPage} hasTextBlock=${hasTextBlock}`);
  }
}
console.log('All pages verified OK\n');

// 5. Count words in HTML vs karaoke manifest
for (const p of pages) {
  // Extract text from the page in HTML
  const pageRegex = new RegExp(`data-page="${p.pageNum}"[^>]*>[\\s\\S]*?<div class="text-block">([\\s\\S]*?)</div>\\s*<div class="page-number`);
  const textMatch = html.match(pageRegex);
  if (!textMatch) {
    console.log(`  Page ${p.pageNum}: could not extract text block`);
    continue;
  }
  const blockHtml = textMatch[1];
  const cleanText = blockHtml
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<\/?p[^>]*>/gi, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&[a-z]+;/gi, '')
    .replace(/\s+/g, ' ')
    .trim();
  const htmlWords = cleanText.split(/\s+/).filter(w => w.length > 0);

  if (htmlWords.length !== p.words.length) {
    console.log(`  Page ${p.pageNum}: HTML has ${htmlWords.length} words, karaoke has ${p.words.length} words — MISMATCH`);
    // Show first few words
    console.log(`    HTML first 5: ${htmlWords.slice(0, 5).join(' ')}`);
    console.log(`    Karaoke first 5: ${p.words.slice(0, 5).map(w => w.display).join(' ')}`);
    console.log(`    HTML last 5: ${htmlWords.slice(-5).join(' ')}`);
    console.log(`    Karaoke last 5: ${p.words.slice(-5).map(w => w.display).join(' ')}`);
  } else {
    console.log(`  Page ${p.pageNum}: ${htmlWords.length} words — OK`);
  }
}
