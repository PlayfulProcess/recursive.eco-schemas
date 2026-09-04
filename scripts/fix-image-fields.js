/**
 * Moves image_url filenames to image_filename field
 * so DriveImageMatcher on the website can auto-match on upload.
 * Clears image_url since images haven't been uploaded to R2 yet.
 */
const fs = require('fs');
const path = require('path');

const grammarPath = path.join(__dirname, '..', 'grammars', 'alice-in-wonderland-chapter-book', 'grammar.json');
const g = JSON.parse(fs.readFileSync(grammarPath, 'utf8'));

let updated = 0;
g.items.forEach(item => {
  // If image_url looks like a filename (not a URL), move it to image_filename
  if (item.image_url && !item.image_url.startsWith('http')) {
    item.image_filename = item.image_url;
    delete item.image_url;
    updated++;
  }
});

fs.writeFileSync(grammarPath, JSON.stringify(g, null, 2));
console.log(`Updated ${updated} items: image_url → image_filename`);
console.log('Upload grammar, then use DriveImageMatcher with the images folder.');
