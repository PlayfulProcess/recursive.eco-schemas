/**
 * Deploy book.html to R2 — instant static hosting.
 * The R2 bucket already has public access via pub-* URL.
 */
import { readFileSync } from 'fs';
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

const s3 = new S3Client({
  region: 'auto',
  endpoint: `https://${env.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: env.R2_ACCESS_KEY_ID,
    secretAccessKey: env.R2_SECRET_ACCESS_KEY,
  },
});

const bucket = env.R2_BUCKET_NAME;
const r2BaseUrl = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev';

const bookPath = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets/book.html');
const bookHtml = readFileSync(bookPath);

const key = 'grammar-illustrations/alice-in-wonderland/book.html';

console.log(`Uploading book.html (${(bookHtml.length / 1024 / 1024).toFixed(1)} MB) to R2...`);

await s3.send(new PutObjectCommand({
  Bucket: bucket,
  Key: key,
  Body: bookHtml,
  ContentType: 'text/html; charset=utf-8',
  CacheControl: 'no-cache',
}));

const url = `${r2BaseUrl}/${key}`;
console.log(`\n✓ Deployed!`);
console.log(`\n  ${url}`);
console.log(`\nOpen on your tablet to pick illustrations!`);
