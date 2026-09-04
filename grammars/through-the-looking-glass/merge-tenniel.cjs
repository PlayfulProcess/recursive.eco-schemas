/**
 * Merge Tenniel 1871 illustrations into Looking Glass grammar.
 * For items that previously had cross-referenced duplicates (from fill-remaining.cjs),
 * REPLACE the old illustration with the unique Tenniel one.
 * For items that already had Newell/Theaker illustrations, ADD Tenniel as additional.
 */
const fs = require('fs');
const tenniel = JSON.parse(fs.readFileSync(__dirname + '/r2-tenniel.json', 'utf8'));
const grammar = JSON.parse(fs.readFileSync(__dirname + '/grammar.json', 'utf8'));

let replaced = 0;
let added = 0;

for (const item of grammar.items) {
  const newIlls = tenniel[item.id];
  if (!newIlls || newIlls.length === 0) continue;

  const meta = item.metadata || {};
  const existing = meta.illustrations || [];

  // Check if this item previously had only a cross-referenced illustration
  // (i.e., exactly 1 illustration that was marked is_primary and was borrowed from another item)
  const hadOnlyBorrowed = existing.length === 1 && existing[0].artist !== 'John Tenniel';
  const isItemThatWasMissing = [
    // L1 items that had cross-refs
    'ch1-lets-pretend', 'ch3-the-railway-carriage', 'ch4-meeting-the-twins',
    'ch5-living-backwards', 'ch5-rowing-and-rushes', 'ch6-the-meaning-of-words',
    'ch8-the-aged-aged-man', 'ch11-waking', 'ch12-which-dreamed-it',
    // L2 chapters
    'chapter-1', 'chapter-2', 'chapter-3', 'chapter-4', 'chapter-5',
    'chapter-6', 'chapter-7', 'chapter-8', 'chapter-9', 'chapter-10',
    'chapter-11', 'chapter-12',
    // Themes and meta
    'theme-language-wordplay', 'theme-chess-game', 'theme-identity',
    'theme-mirrors-reversal', 'theme-authority-rules', 'theme-poetry-songs',
    'meta-narrative-journey', 'meta-themes-ideas',
  ].includes(item.id);

  if (isItemThatWasMissing && hadOnlyBorrowed) {
    // REPLACE the cross-referenced duplicate with the unique Tenniel
    const tennielIll = { ...newIlls[0], is_primary: true };
    meta.illustrations = [tennielIll];
    item.image_url = tennielIll.url;
    replaced++;
  } else {
    // ADD Tenniel as an additional illustration (don't remove existing)
    const existingUrls = new Set(existing.map(i => i.url));
    const toAdd = newIlls.filter(i => !existingUrls.has(i.url));
    if (toAdd.length === 0) continue;
    meta.illustrations = [...existing, ...toAdd];
    added++;
  }

  item.metadata = meta;
}

fs.writeFileSync(__dirname + '/grammar.json', JSON.stringify(grammar, null, 2));
console.log(`Replaced ${replaced} cross-referenced duplicates with unique Tenniel illustrations`);
console.log(`Added Tenniel as additional illustration to ${added} items`);

// Verify
const withIlls = grammar.items.filter(i => i.metadata && i.metadata.illustrations && i.metadata.illustrations.length > 0);
const withImg = grammar.items.filter(i => i.image_url);
const totalIlls = withIlls.reduce((sum, i) => sum + i.metadata.illustrations.length, 0);
console.log(`\nItems with illustrations: ${withIlls.length} / ${grammar.items.length}`);
console.log(`Items with image_url: ${withImg.length} / ${grammar.items.length}`);
console.log(`Total illustration entries: ${totalIlls}`);

// Check for any remaining duplicates
const urlCounts = {};
grammar.items.forEach(i => {
  if (i.image_url) {
    urlCounts[i.image_url] = (urlCounts[i.image_url] || 0) + 1;
  }
});
const dupes = Object.entries(urlCounts).filter(([_, count]) => count > 1);
if (dupes.length > 0) {
  console.log(`\nRemaining duplicate image_urls (${dupes.length}):`);
  dupes.forEach(([url, count]) => {
    const items = grammar.items.filter(i => i.image_url === url);
    console.log(`  ${count}x: ${items.map(i => i.id).join(', ')}`);
  });
} else {
  console.log('\n✓ ALL items have UNIQUE image_url — no duplicates!');
}
