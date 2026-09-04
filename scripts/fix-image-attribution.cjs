/**
 * Fix image attribution metadata on all grammar items.
 *
 * Problem: The hero image in GrammarReader shows:
 *   DESCRIPTION: "No description" (reads from metadata.image_description)
 *   SOURCE: "original" (reads from origin.type, falls back to 'original')
 *
 * But the actual attribution data IS in metadata.illustrations[].
 *
 * Fix: For each item with illustrations, populate:
 *   - metadata.image_description = "Artist Name — Dates — Edition" (from primary illustration)
 *   - origin.type = 'imported'
 *   - origin.source_format = 'public_domain_illustration'
 */
const fs = require('fs');
const path = require('path');

const GRAMMARS = [
  path.join(__dirname, '..', 'grammars', 'alice-in-wonderland-chapter-book', 'grammar.json'),
  path.join(__dirname, '..', 'grammars', 'through-the-looking-glass', 'grammar.json'),
];

for (const grammarPath of GRAMMARS) {
  const grammar = JSON.parse(fs.readFileSync(grammarPath, 'utf8'));
  const slug = path.basename(path.dirname(grammarPath));
  let fixed = 0;

  for (const item of grammar.items) {
    const meta = item.metadata || {};
    const ills = meta.illustrations || [];
    if (ills.length === 0) continue;

    // Find the primary illustration (or first one)
    const primary = ills.find(i => i.is_primary) || ills[0];

    // Build description from illustration metadata
    const parts = [primary.artist];
    if (primary.artist_dates) parts.push(primary.artist_dates);
    if (primary.edition) parts.push(primary.edition);
    const description = parts.join(' — ');

    // Set image_description
    meta.image_description = description;

    // Set origin to indicate this is an imported public domain illustration
    item.origin = {
      type: 'imported',
      source_format: 'public_domain_illustration',
    };

    item.metadata = meta;
    fixed++;
  }

  fs.writeFileSync(grammarPath, JSON.stringify(grammar, null, 2));
  console.log(`${slug}: Fixed attribution on ${fixed} / ${grammar.items.length} items`);
}

console.log('\nDone! Hero images will now show proper artist attribution.');
