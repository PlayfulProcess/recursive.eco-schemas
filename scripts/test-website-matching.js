/**
 * Simulates what DriveImageMatcher.tsx does client-side.
 * Tests whether image_filename matching works with the z.ignore folder files.
 *
 * Usage: node scripts/test-website-matching.js
 */
const fs = require('fs');
const path = require('path');

// --- Replicate the normalizeFilename from DriveImageMatcher.tsx ---
function normalizeFilename(name) {
  return name
    .toLowerCase()
    .replace(/\.[^.]+$/, '') // Remove extension
    .replace(/[_-]+/g, ' ')  // Replace underscores/dashes with spaces
    .replace(/\s+/g, ' ')    // Normalize spaces
    .trim();
}

// --- Load grammar ---
const grammarPath = path.join(__dirname, '..', 'grammars', 'alice-in-wonderland-chapter-book', 'grammar.json');
const grammar = JSON.parse(fs.readFileSync(grammarPath, 'utf8'));

// --- Load files from z.ignore ---
const imgDir = path.join(__dirname, '..', 'z.ignore', 'manuscript-images');
const EXTS = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
const files = fs.readdirSync(imgDir)
  .filter(f => EXTS.includes(path.extname(f).toLowerCase()))
  .map((f, i) => ({ id: `file-${i}`, name: f }));

console.log(`Grammar items: ${grammar.items.length}`);
console.log(`Image files: ${files.length}\n`);

// --- Simulate DriveImageMatcher matching ---
const usedFiles = new Set();
const matched = [];
const unmatched = [];

grammar.items.forEach((item, cardIndex) => {
  const card = {
    id: item.id,
    name: item.name,
    image_filename: item.metadata?.image_filename,
    sort_order: item.sort_order,
    number: item.metadata?.number,
  };

  let matchedFile;

  // Strategy 1: Match by image_filename
  if (card.image_filename) {
    const normalizedFilename = normalizeFilename(card.image_filename);
    matchedFile = files.find(file => {
      if (usedFiles.has(file.id)) return false;
      const normalizedDriveFilename = normalizeFilename(file.name);
      return normalizedDriveFilename === normalizedFilename ||
             normalizedDriveFilename.startsWith(normalizedFilename) ||
             normalizedFilename.startsWith(normalizedDriveFilename);
    });
    if (matchedFile) {
      matched.push({ item: card.name, file: matchedFile.name, strategy: 'image_filename' });
      usedFiles.add(matchedFile.id);
      return;
    }
  }

  // Strategy 2: Match by card name
  if (card.name) {
    const normalizedName = normalizeFilename(card.name);
    const nameWords = normalizedName.split(/\s+/).filter(w => w.length > 2);

    matchedFile = files.find(file => {
      if (usedFiles.has(file.id)) return false;
      const normalizedDriveFilename = normalizeFilename(file.name);
      if (normalizedDriveFilename.includes(normalizedName) ||
          normalizedName.includes(normalizedDriveFilename)) {
        return true;
      }
      if (nameWords.length > 0) {
        const matchCount = nameWords.filter(w => normalizedDriveFilename.includes(w)).length;
        return matchCount / nameWords.length >= 0.6;
      }
      return false;
    });
    if (matchedFile) {
      matched.push({ item: card.name, file: matchedFile.name, strategy: 'name' });
      usedFiles.add(matchedFile.id);
      return;
    }
  }

  // Strategy 3: Match by number
  const num = card.number ?? (cardIndex + 1);
  if (num !== undefined) {
    const numStr2 = String(num).padStart(2, '0');
    matchedFile = files.find(file => {
      if (usedFiles.has(file.id)) return false;
      const normalizedDriveFilename = normalizeFilename(file.name);
      return normalizedDriveFilename.match(new RegExp(`(^|[_ \\s-])${numStr2}([_ \\s-]|$)`)) ||
             normalizedDriveFilename.startsWith(numStr2 + ' ');
    });
    if (matchedFile) {
      matched.push({ item: card.name, file: matchedFile.name, strategy: 'number' });
      usedFiles.add(matchedFile.id);
      return;
    }
  }

  unmatched.push(card.name);
});

console.log(`=== MATCHED: ${matched.length} of ${grammar.items.length} ===`);
const byStrategy = {};
matched.forEach(m => { byStrategy[m.strategy] = (byStrategy[m.strategy] || 0) + 1; });
Object.entries(byStrategy).forEach(([s, c]) => console.log(`  ${s}: ${c}`));

console.log(`\n=== UNMATCHED: ${unmatched.length} ===`);
unmatched.forEach(n => console.log(`  ${n}`));

console.log(`\n=== SAMPLE MATCHES ===`);
matched.slice(0, 10).forEach(m => {
  console.log(`  [${m.strategy}] "${m.item}" → ${m.file}`);
});
