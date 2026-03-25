/**
 * Upload Carroll manuscript page scans to Cloudflare R2.
 *
 * Reads env vars from recursive-eco/.env.local:
 *   CLOUDFLARE_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME
 *
 * Uploads to: grammar-illustrations/alice-in-wonderland/manuscript-under-ground/
 *
 * Usage: node scripts/upload-manuscript-to-r2.mjs
 */
import { readFileSync, readdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

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
console.log('Env loaded:', Object.keys(env).filter(k => k.startsWith('R2') || k.startsWith('CLOUD')).join(', '));

const s3 = new S3Client({
  region: 'auto',
  endpoint: `https://${env.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: env.R2_ACCESS_KEY_ID,
    secretAccessKey: env.R2_SECRET_ACCESS_KEY,
  },
});

const bucket = env.R2_BUCKET_NAME;
const r2Prefix = 'grammar-illustrations/alice-in-wonderland/manuscript-under-ground';
const r2BaseUrl = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev';

const scanDir = resolve(__dirname, '../z.ignore/manuscript-scans');
const files = readdirSync(scanDir).filter(f => f.endsWith('.jpg')).sort();

console.log(`Uploading ${files.length} manuscript scans to R2...`);
console.log(`Bucket: ${bucket}, Prefix: ${r2Prefix}\n`);

const uploaded = [];

for (const file of files) {
  const key = `${r2Prefix}/${file}`;
  const body = readFileSync(resolve(scanDir, file));

  try {
    await s3.send(new PutObjectCommand({
      Bucket: bucket,
      Key: key,
      Body: body,
      ContentType: 'image/jpeg',
    }));
    const url = `${r2BaseUrl}/${key}`;
    uploaded.push({ file, url });
    console.log(`  [ok] ${file} → ${url}`);
  } catch (e) {
    console.log(`  [FAIL] ${file}: ${e.message}`);
  }
}

console.log(`\nUploaded ${uploaded.length}/${files.length} files.`);

// Write URL manifest
const { writeFileSync: writeFile } = await import('fs');
writeFile(resolve(scanDir, 'r2-urls.json'), JSON.stringify(uploaded, null, 2));
console.log('URL manifest: z.ignore/manuscript-scans/r2-urls.json');
