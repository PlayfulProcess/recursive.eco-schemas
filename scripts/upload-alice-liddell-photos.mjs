/**
 * Upload real Alice Liddell photos to Cloudflare R2.
 * Source: rarehistoricalphotos.com — public domain Carroll photographs
 *
 * Usage: node scripts/upload-alice-liddell-photos.mjs
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
const r2Prefix = 'grammar-illustrations/alice-in-wonderland/alice-liddell-photos';
const r2BaseUrl = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev';

// Alice Liddell photos — all by Lewis Carroll (public domain, 1850s-1870s)
const PHOTOS = [
  {
    url: 'https://2.bp.blogspot.com/-8Ak1Q_VYxr8/XwyWVaxkzjI/AAAAAAAAY7A/zIx8YBB5n84DUGlw3raeyCr_8ozXkgkOwCLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%25281%2529.jpg',
    filename: 'alice-liddell-portrait.jpg',
    caption: 'Alice Liddell portrait'
  },
  {
    url: 'https://1.bp.blogspot.com/-EOVkc9Mm9Iw/XwyWY3MRxWI/AAAAAAAAY7o/i2jPbv1ZLnA11ckI3sY0Y0zf9lGKEGbMQCLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%25289%2529.jpg',
    filename: 'alice-feigned-sleep-1860.jpg',
    caption: 'Alice poses in a feigned sleep, 1860'
  },
  {
    url: 'https://4.bp.blogspot.com/-tVFC1V2XLUk/XwyWVQQWU5I/AAAAAAAAY7E/Op5PdpafzfIMlripixtP8JMD5yGWjxEHgCLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%252811%2529.jpg',
    filename: 'edith-ina-alice-july-1860.jpg',
    caption: 'Edith, Ina and Alice Liddell, July 1860'
  },
  {
    url: 'https://2.bp.blogspot.com/-4hCBn0IlxtE/XwyWVWIszRI/AAAAAAAAY68/-V-d_fFCxnIKCleBQGhBrd_AIwGC2w2jgCLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%252810%2529.jpg',
    filename: 'lorina-edith-alice-1859.jpg',
    caption: 'Lorina, Edith and Alice Liddell, 1859'
  },
  {
    url: 'https://4.bp.blogspot.com/-V_0ebXrtK_E/XwyWWDJRLcI/AAAAAAAAY7I/6qGuOdtBupQmm_rAX8Uzhz5YB5r7RP94ACLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%252812%2529.jpg',
    filename: 'alice-ina-harry-edith-1860.jpg',
    caption: 'Alice, Ina, Harry and Edith Liddell, June 1860'
  },
  {
    url: 'https://3.bp.blogspot.com/-CwmQDtB4628/XwyWXJFlYvI/AAAAAAAAY7Y/JCKzgWzxHCAa7irmJrKmbeby1_6hplxuACLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%252816%2529.jpg',
    filename: 'alice-beggar-girl-1858.jpg',
    caption: 'Alice Liddell as a beggar-girl, photographed by Lewis Carroll, 1858'
  },
  {
    url: 'https://2.bp.blogspot.com/-BS8H1kXJke0/XwyWYnVcluI/AAAAAAAAY7k/I15BJN7-dw4d0BFGUkELOBZ3cTN_GrXcwCLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%252819%2529.jpg',
    filename: 'alice-liddell-1859.jpg',
    caption: 'Alice Liddell, 1859'
  },
  {
    url: 'https://2.bp.blogspot.com/-l81ESDXwLVQ/XwyWXrLB37I/AAAAAAAAY7c/9zNZpvjr6xco8QFtQmvSOHGAzchcQThxQCLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%252817%2529.jpg',
    filename: 'alice-age-20-1872.jpg',
    caption: 'A 20-year-old Alice, 1872'
  },
  {
    url: 'https://4.bp.blogspot.com/-Epnn4Euu5EY/XwyWWEBwl1I/AAAAAAAAY7M/GLkSOUbcpBU1Vo58hfmDwZEG_Ktbr83pQCLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%252813%2529.jpg',
    filename: 'alice-with-julia-margaret-cameron-1872.jpg',
    caption: 'Alice (age 20) with photographer Julia Margaret Cameron, 1872'
  },
  {
    url: 'https://4.bp.blogspot.com/-InJs8XZh0YA/XwyWWc8fTsI/AAAAAAAAY7Q/gr45dNjI8j4QQOsgmdV583M8ijO52w44ACLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%252814%2529.jpg',
    filename: 'alice-grown-up.jpg',
    caption: 'A grown up Alice of Wonderland'
  },
  {
    url: 'https://4.bp.blogspot.com/-N3RUXZsarfA/XwyWWk8jOXI/AAAAAAAAY7U/ik0lsZS_37AMkUuo60QT1RFBgByRprwLgCLcBGAsYHQ/s1600/real-alice-in-wonderland%2B%252815%2529.jpg',
    filename: 'alice-hargreaves-1932-age-80.jpg',
    caption: 'Alice Hargreaves (née Liddell) in 1932, at the age of 80'
  }
];

console.log(`\nUploading ${PHOTOS.length} Alice Liddell photos to R2...`);
console.log(`Bucket: ${bucket}, Prefix: ${r2Prefix}\n`);

const uploaded = [];

for (const photo of PHOTOS) {
  const key = `${r2Prefix}/${photo.filename}`;
  const r2Url = `${r2BaseUrl}/${key}`;

  try {
    // Fetch the image
    console.log(`  Fetching: ${photo.caption}...`);
    const resp = await fetch(photo.url);
    if (!resp.ok) {
      console.log(`  ✗ Failed to fetch: ${resp.status} ${resp.statusText}`);
      continue;
    }
    const buffer = Buffer.from(await resp.arrayBuffer());
    console.log(`  Downloaded: ${(buffer.length / 1024).toFixed(0)} KB`);

    // Upload to R2
    await s3.send(new PutObjectCommand({
      Bucket: bucket,
      Key: key,
      Body: buffer,
      ContentType: 'image/jpeg',
    }));

    console.log(`  ✓ ${r2Url}`);
    uploaded.push({ ...photo, r2Url });
  } catch (err) {
    console.log(`  ✗ Error: ${err.message}`);
  }
}

console.log(`\n✓ Uploaded ${uploaded.length}/${PHOTOS.length} photos\n`);

// Print the illustration metadata entries for adding to grammar JSON
console.log('=== Illustration metadata for grammar JSON ===');
for (const p of uploaded) {
  console.log(JSON.stringify({
    url: p.r2Url,
    artist: 'Lewis Carroll (photograph)',
    scene: p.caption,
    year: p.caption.match(/\d{4}/)?.[0] || '1860s'
  }));
}
