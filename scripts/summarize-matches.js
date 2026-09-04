const fs = require('fs');
const path = require('path');

const base = path.join(__dirname, '..', 'grammars', 'alice-in-wonderland-chapter-book');
const m = JSON.parse(fs.readFileSync(path.join(base, 'image-matches.json'), 'utf8'));
const g = JSON.parse(fs.readFileSync(path.join(base, 'grammar.json'), 'utf8'));

const matched = m.filter(x => x.item_id);
const high = matched.filter(x => x.confidence === 'high');
const med = matched.filter(x => x.confidence === 'medium');
const items = new Set(matched.map(x => x.item_id));

// Duplicates
const counts = {};
matched.forEach(x => { counts[x.item_id] = (counts[x.item_id] || 0) + 1; });
const dups = Object.entries(counts).filter(([, v]) => v > 1);

// Missing items
const matchedIds = new Set(matched.map(x => x.item_id));
const missing = g.items.filter(i => !matchedIds.has(i.id));

console.log('=== MATCHING RESULTS ===');
console.log('Matched:', matched.length, 'images to', items.size, 'of', g.items.length, 'items');
console.log('High confidence:', high.length);
console.log('Medium confidence:', med.length);
console.log('');

if (dups.length) {
  console.log('DUPLICATE ITEMS (got multiple images):');
  dups.forEach(([id, c]) => console.log(' ', id, ':', c, 'images'));
  console.log('');
}

if (missing.length) {
  console.log('UNMATCHED ITEMS (' + missing.length + '):');
  missing.forEach(i => console.log(' ', i.id, '-', i.name));
}
