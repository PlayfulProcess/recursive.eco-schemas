const fs = require('fs');
const r2 = JSON.parse(fs.readFileSync(__dirname + '/r2-illustrations-round2.json', 'utf8'));
const grammar = JSON.parse(fs.readFileSync(__dirname + '/grammar.json', 'utf8'));

let updated = 0;
let newlyIllustrated = 0;

for (const item of grammar.items) {
  const newIlls = r2[item.id];
  if (!newIlls || newIlls.length === 0) continue;

  const meta = item.metadata || {};
  const existing = meta.illustrations || [];
  const existingUrls = new Set(existing.map(i => i.url));

  const toAdd = newIlls.filter(i => !existingUrls.has(i.url));
  if (toAdd.length === 0) continue;

  const hadIllustrations = existing.length > 0;
  const allIlls = [...existing, ...toAdd];

  // For items that had NO illustrations before, set the first new one as primary
  if (!allIlls.some(i => i.is_primary)) {
    allIlls[0].is_primary = true;
  }

  const primary = allIlls.find(i => i.is_primary);
  if (primary && !item.image_url) {
    item.image_url = primary.url;
  }

  meta.illustrations = allIlls;
  item.metadata = meta;
  updated++;
  if (!hadIllustrations) newlyIllustrated++;
}

fs.writeFileSync(__dirname + '/grammar.json', JSON.stringify(grammar, null, 2));
console.log('Updated', updated, 'items (' + newlyIllustrated + ' newly illustrated)');

const withIlls = grammar.items.filter(i => i.metadata && i.metadata.illustrations && i.metadata.illustrations.length > 0);
const withImg = grammar.items.filter(i => i.image_url);
const totalIlls = withIlls.reduce((sum, i) => sum + i.metadata.illustrations.length, 0);
console.log('Items with illustrations:', withIlls.length, '/', grammar.items.length);
console.log('Items with image_url:', withImg.length, '/', grammar.items.length);
console.log('Total illustration entries:', totalIlls);

const noIll = grammar.items.filter(i => !i.image_url);
if (noIll.length > 0) {
  console.log('\nStill missing:');
  noIll.forEach(i => console.log('  ' + i.id));
}
