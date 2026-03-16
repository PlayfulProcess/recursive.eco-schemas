/**
 * Upload Alice audiobook MP3s to Cloudflare R2.
 * LibriVox chapters (public domain) + Suno preface song.
 */
import { readFileSync, readdirSync, existsSync } from 'fs';
import { resolve, dirname, basename } from 'path';
import { fileURLToPath } from 'url';
import { S3Client, PutObjectCommand, HeadObjectCommand } from '@aws-sdk/client-s3';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load env from recursive-eco
const envPath = resolve(__dirname, '../../recursive-eco/.env.local');
const envContent = readFileSync(envPath, 'utf8');
const env = {};
for (const line of envContent.split('\n')) {
  const eqIdx = line.indexOf('=');
  if (eqIdx > 0 && !line.startsWith('#')) {
    const key = line.substring(0, eqIdx).trim();
    const val = line.substring(eqIdx + 1).trim().replace(/^["']|["']$/g, '');
    env[key] = val;
  }
}

const s3 = new S3Client({
  region: 'auto',
  endpoint: `https://${env.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: env.R2_ACCESS_KEY_ID,
    secretAccessKey: env.R2_SECRET_ACCESS_KEY,
  },
});

const bucket = env.R2_BUCKET_NAME;
const r2Prefix = 'grammar-illustrations/alice-in-wonderland/audio';
const r2BaseUrl = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev';

// Collect all MP3 files
const audioDir = resolve(__dirname, '../grammars/alice-5-minute-stories/audio');
const librivoxDir = resolve(audioDir, 'librivox');

const files = [];

// Preface Suno song
files.push({
  localPath: resolve(audioDir, 'all-in-the-golden-afternoon.mp3'),
  r2Key: `${r2Prefix}/all-in-the-golden-afternoon.mp3`,
  label: 'Suno preface song'
});

// LibriVox chapters
const librivoxFiles = readdirSync(librivoxDir).filter(f => f.endsWith('.mp3') && f.startsWith('wonderland_'));
librivoxFiles.sort();
for (const f of librivoxFiles) {
  files.push({
    localPath: resolve(librivoxDir, f),
    r2Key: `${r2Prefix}/librivox/${f}`,
    label: f
  });
}

// Merged complete audiobook (all chapters concatenated)
const mergedFile = resolve(librivoxDir, 'wonderland-complete.mp3');
if (existsSync(mergedFile)) {
  files.push({
    localPath: mergedFile,
    r2Key: `${r2Prefix}/librivox/wonderland-complete.mp3`,
    label: 'wonderland-complete.mp3 (merged audiobook)'
  });
}

console.log(`Uploading ${files.length} audio files to R2...`);
console.log(`Bucket: ${bucket}, Prefix: ${r2Prefix}\n`);

let uploaded = 0;
let skipped = 0;

for (const file of files) {
  const r2Url = `${r2BaseUrl}/${file.r2Key}`;

  // Check if already exists
  try {
    await s3.send(new HeadObjectCommand({ Bucket: bucket, Key: file.r2Key }));
    console.log(`  ✓ Already exists: ${file.label} → ${r2Url}`);
    skipped++;
    continue;
  } catch (e) {
    // Doesn't exist, upload it
  }

  try {
    const buffer = readFileSync(file.localPath);
    console.log(`  Uploading: ${file.label} (${(buffer.length / 1024 / 1024).toFixed(1)} MB)...`);

    await s3.send(new PutObjectCommand({
      Bucket: bucket,
      Key: file.r2Key,
      Body: buffer,
      ContentType: 'audio/mpeg',
    }));

    console.log(`  ✓ ${r2Url}`);
    uploaded++;
  } catch (err) {
    console.error(`  ✗ Error: ${err.message}`);
  }
}

console.log(`\n✓ Done: ${uploaded} uploaded, ${skipped} already existed`);
console.log(`\nR2 URLs for generator:`);
console.log(`  Preface: ${r2BaseUrl}/${r2Prefix}/all-in-the-golden-afternoon.mp3`);
for (const f of librivoxFiles) {
  console.log(`  ${f}: ${r2BaseUrl}/${r2Prefix}/librivox/${f}`);
}
