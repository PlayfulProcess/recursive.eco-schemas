/** Quick one-off: upload the fixed wonderland-complete.mp3 to R2 */
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

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

const mp3Path = resolve(__dirname, '../grammars/alice-5-minute-stories/audio/librivox/wonderland-complete.mp3');
const buffer = readFileSync(mp3Path);
console.log(`Uploading ${(buffer.length / 1024 / 1024).toFixed(1)} MB...`);

await s3.send(new PutObjectCommand({
  Bucket: env.R2_BUCKET_NAME,
  Key: 'grammar-illustrations/alice-in-wonderland/audio/librivox/wonderland-complete.mp3',
  Body: buffer,
  ContentType: 'audio/mpeg',
}));

console.log('Done! https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/alice-in-wonderland/audio/librivox/wonderland-complete.mp3');
