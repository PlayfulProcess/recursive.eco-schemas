#!/usr/bin/env node
/**
 * Delete individual chapter MP3s from R2.
 * These are redundant now that we have wonderland-complete.mp3.
 *
 * Keeps:
 *   - wonderland-complete.mp3 (merged audiobook)
 *   - all-in-the-golden-afternoon.mp3 (preface song)
 *
 * Deletes:
 *   - wonderland_ch_01_64kb.mp3 through wonderland_ch_12_64kb.mp3
 */
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { S3Client, DeleteObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3';

const __dirname = dirname(fileURLToPath(import.meta.url));
const envPath = resolve(__dirname, '../../recursive-eco/.env.local');
const envContent = readFileSync(envPath, 'utf8');
const env = {};
for (const line of envContent.split('\n')) {
  const eqIdx = line.indexOf('=');
  if (eqIdx > 0 && !line.startsWith('#')) {
    env[line.substring(0, eqIdx).trim()] = line.substring(eqIdx + 1).trim().replace(/^["']|["']$/g, '');
  }
}

const s3 = new S3Client({
  region: 'auto',
  endpoint: `https://${env.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: { accessKeyId: env.R2_ACCESS_KEY_ID, secretAccessKey: env.R2_SECRET_ACCESS_KEY },
});

const bucket = env.R2_BUCKET_NAME;
const prefix = 'grammar-illustrations/alice-in-wonderland/audio/librivox/';

// List all files
const res = await s3.send(new ListObjectsV2Command({ Bucket: bucket, Prefix: prefix }));
const toDelete = (res.Contents || []).filter(obj => obj.Key.includes('wonderland_ch_'));

console.log(`Found ${toDelete.length} individual chapter files to delete:`);
let totalSize = 0;
for (const obj of toDelete) {
  console.log(`  ${obj.Key} (${(obj.Size / 1024 / 1024).toFixed(1)} MB)`);
  totalSize += obj.Size;
}
console.log(`\nTotal: ${(totalSize / 1024 / 1024).toFixed(1)} MB\n`);

if (process.argv.includes('--dry-run')) {
  console.log('DRY RUN — no files deleted. Remove --dry-run to actually delete.');
  process.exit(0);
}

for (const obj of toDelete) {
  await s3.send(new DeleteObjectCommand({ Bucket: bucket, Key: obj.Key }));
  console.log(`  ✓ Deleted: ${obj.Key}`);
}

console.log(`\n✓ Deleted ${toDelete.length} files (${(totalSize / 1024 / 1024).toFixed(1)} MB freed)`);

// Verify what's left
const remaining = await s3.send(new ListObjectsV2Command({ Bucket: bucket, Prefix: 'grammar-illustrations/alice-in-wonderland/audio/' }));
console.log('\nRemaining audio files:');
for (const obj of (remaining.Contents || [])) {
  console.log(`  ${obj.Key} (${(obj.Size / 1024 / 1024).toFixed(1)} MB)`);
}
