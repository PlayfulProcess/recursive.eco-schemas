/**
 * Download Carroll manuscript page scans from alice-in-wonderland.net
 * and prepare metadata for R2 upload + illustration matching.
 *
 * Source: https://www.alice-in-wonderland.net/resources/pictures/alices-adventures-under-ground/
 * These are facsimile scans of Carroll's 1864 manuscript for Alice Liddell.
 *
 * The manuscript has 90 pages + frontispiece. The website hosts 47 images
 * (each showing a 2-page spread, except front/back covers).
 *
 * Carroll's manuscript chapter breakdown (Alice Under Ground has 4 chapters):
 *   Chapter I  (pages 1-44):  Down the Rabbit-Hole + Pool of Tears + Caucus Race + Bill the Lizard
 *   Chapter II (pages 45-59): Caterpillar + Pig & Pepper
 *   Chapter III(pages 60-77): Mad Tea Party + Queen's Croquet + Mock Turtle + Lobster Quadrille
 *   Chapter IV (pages 78-90): Who Stole the Tarts + Alice's Evidence
 *
 * But the PUBLISHED book has 12 chapters. We'll map manuscript pages to published chapters
 * by matching the text content.
 */
import { writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import https from 'https';
import { createWriteStream } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const outputDir = resolve(__dirname, '../z.ignore/manuscript-scans');

// Download a URL to a file
function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    if (existsSync(dest)) {
      console.log(`  [skip] ${dest} already exists`);
      resolve();
      return;
    }
    const file = createWriteStream(dest);
    https.get(url, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close();
        downloadFile(res.headers.location, dest).then(resolve).catch(reject);
        return;
      }
      if (res.statusCode !== 200) {
        file.close();
        reject(new Error(`HTTP ${res.statusCode} for ${url}`));
        return;
      }
      res.pipe(file);
      file.on('finish', () => { file.close(); resolve(); });
    }).on('error', reject);
  });
}

// All 47 images (00.jpg through 46.jpg)
const pages = [];
for (let i = 0; i <= 46; i++) {
  const num = String(i).padStart(2, '0');
  pages.push({
    index: i,
    url: `https://www.alice-in-wonderland.net/wp-content/uploads/${num}.jpg`,
    filename: `manuscript-page-${num}.jpg`,
  });
}

console.log(`Downloading ${pages.length} manuscript page scans...`);

for (const page of pages) {
  const dest = resolve(outputDir, page.filename);
  try {
    await downloadFile(page.url, dest);
    console.log(`  [ok] ${page.filename}`);
  } catch (e) {
    console.log(`  [FAIL] ${page.filename}: ${e.message}`);
  }
}

console.log(`\nDone! ${pages.length} files in ${outputDir}`);

// Generate metadata manifest for R2 upload
// Each page spread covers 2 manuscript pages (e.g., image 01.jpg = pages 1-2)
const manifest = pages.map(p => ({
  index: p.index,
  filename: p.filename,
  manuscript_pages: p.index === 0 ? 'frontispiece' : `${(p.index * 2) - 1}-${p.index * 2}`,
  // We'll fill in chapter mapping and text quotes after examining the images
}));

writeFileSync(resolve(outputDir, 'manifest.json'), JSON.stringify(manifest, null, 2));
console.log('Manifest written to manifest.json');
