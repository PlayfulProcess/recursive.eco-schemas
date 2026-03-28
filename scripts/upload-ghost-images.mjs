/**
 * Upload Ghost backup images to Cloudflare R2
 *
 * Reads images from the Ghost backup content/images/ directory,
 * skips Ghost-generated optimized variants (*_o.*),
 * and uploads to R2 under ghost-archive/{month}/{filename}.
 *
 * Generates a manifest JSON mapping original paths to R2 URLs.
 *
 * Usage: node scripts/upload-ghost-images.mjs
 *
 * Requires env vars from .env.local:
 *   CLOUDFLARE_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME
 */

import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join, basename, extname } from 'path';
import { config } from 'dotenv';

// Load env from recursive-kids-stories-club (has R2 vars)
config({ path: 'C:/Users/ferna/OneDrive/Documentos/GitHub/recursive-kids-stories-club/.env.local' });

const ACCOUNT_ID = process.env.CLOUDFLARE_ACCOUNT_ID;
const ACCESS_KEY = process.env.R2_ACCESS_KEY_ID;
const SECRET_KEY = process.env.R2_SECRET_ACCESS_KEY;
const BUCKET = process.env.R2_BUCKET_NAME;
const R2_PUBLIC_BASE = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev';

if (!ACCOUNT_ID || !ACCESS_KEY || !SECRET_KEY || !BUCKET) {
  console.error('Missing R2 env vars. Need: CLOUDFLARE_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME');
  process.exit(1);
}

const s3 = new S3Client({
  region: 'auto',
  endpoint: `https://${ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: { accessKeyId: ACCESS_KEY, secretAccessKey: SECRET_KEY },
});

const GHOST_IMAGES_DIR = 'C:/Users/ferna/OneDrive/Documentos/GitHub/playfulprocess-1_1774599454/content/images';
const MIME_TYPES = {
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.png': 'image/png', '.webp': 'image/webp',
  '.gif': 'image/gif', '.svg': 'image/svg+xml',
};

function walkDir(dir) {
  const results = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      results.push(...walkDir(full));
    } else {
      results.push(full);
    }
  }
  return results;
}

async function main() {
  const allFiles = walkDir(GHOST_IMAGES_DIR);

  // Filter: only images, skip _o. variants (Ghost optimized copies)
  const imageExts = new Set(Object.keys(MIME_TYPES));
  const images = allFiles.filter(f => {
    const ext = extname(f).toLowerCase();
    const name = basename(f);
    return imageExts.has(ext) && !name.includes('_o.');
  });

  console.log(`Found ${images.length} images to upload (skipped ${allFiles.length - images.length} non-images/_o variants)`);

  const manifest = {};
  let uploaded = 0;
  let errors = 0;

  for (const filepath of images) {
    // Extract month path: 2025/05, 2025/06, etc.
    const normalizedFile = filepath.replace(/\\/g, '/');
    const normalizedBase = GHOST_IMAGES_DIR.replace(/\\/g, '/');
    const relPath = normalizedFile.replace(normalizedBase + '/', '');
    const r2Key = `ghost-archive/${relPath}`;
    const ext = extname(filepath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    try {
      const body = readFileSync(filepath);
      await s3.send(new PutObjectCommand({
        Bucket: BUCKET,
        Key: r2Key,
        Body: body,
        ContentType: contentType,
      }));

      const publicUrl = `${R2_PUBLIC_BASE}/${r2Key}`;
      manifest[relPath] = publicUrl;
      uploaded++;

      if (uploaded % 20 === 0) {
        console.log(`  ${uploaded}/${images.length} uploaded...`);
      }
    } catch (err) {
      console.error(`  ERROR uploading ${relPath}: ${err.message}`);
      errors++;
    }
  }

  console.log(`\nDone: ${uploaded} uploaded, ${errors} errors`);

  // Save manifest
  const manifestPath = 'grammars/inspiration/ghost-image-manifest.json';
  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log(`Manifest saved to ${manifestPath}`);
}

main().catch(console.error);
