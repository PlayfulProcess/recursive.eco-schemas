/**
 * match-images-claude.js
 *
 * Uses Claude Vision to intelligently match illustration files to grammar items.
 * Two phases:
 *   1. Describe — Claude looks at each image, notes scene/characters/visible text
 *   2. Match   — Claude assigns images to items, prioritizing text-content alignment
 *
 * Usage:
 *   node scripts/match-images-claude.js <images-folder> <grammar.json>
 *   node scripts/match-images-claude.js <images-folder> <grammar.json> --apply
 *
 * Outputs:
 *   image-descriptions.json — what Claude sees in each image
 *   image-matches.json      — proposed image-to-item assignments
 */

require('dotenv').config();
const Anthropic = require('@anthropic-ai/sdk');
const fs = require('fs');
const path = require('path');

const anthropic = new Anthropic();

const SUPPORTED_EXTS = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
const MEDIA_TYPES = {
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
};
const BATCH_SIZE = 5; // concurrent requests per batch (avoids rate limits)
const MODEL = 'claude-sonnet-4-6'; // good balance of vision quality and cost
const MAX_IMAGE_BYTES = 3.5 * 1024 * 1024; // 3.5MB on disk (~4.7MB as base64, under 5MB API limit)

// ── Phase 1: Describe every image ──────────────────────────

async function describeImage(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const mediaType = MEDIA_TYPES[ext];
  let data = fs.readFileSync(filePath);

  // Skip files that are too large even after noting them
  if (data.length > MAX_IMAGE_BYTES) {
    console.warn(`  SKIP (${(data.length / 1024 / 1024).toFixed(1)}MB > 4MB limit): ${path.basename(filePath)}`);
    return {
      file: path.basename(filePath),
      path: filePath,
      description: '{ "scene": "Image too large to process", "style": "unknown", "visible_text": null }',
      skipped: true,
    };
  }

  const base64 = data.toString('base64');

  const resp = await anthropic.messages.create({
    model: MODEL,
    max_tokens: 500,
    messages: [{
      role: 'user',
      content: [
        {
          type: 'image',
          source: { type: 'base64', media_type: mediaType, data: base64 },
        },
        {
          type: 'text',
          text: `Describe this illustration concisely for matching to a text passage:
1. What scene, characters, or objects are depicted?
2. What is the artistic style and likely era?
3. CRITICAL: Is there ANY visible text in the image — handwritten, printed, on signs, labels, bottles, banners, scrolls? If yes, transcribe it EXACTLY as written.

Reply ONLY as JSON (no markdown fences):
{ "scene": "...", "style": "...", "visible_text": "..." or null }`,
        },
      ],
    }],
  });

  return {
    file: path.basename(filePath),
    path: filePath,
    description: resp.content[0].text,
  };
}

// ── Phase 2: Match images to grammar items ─────────────────

async function matchAll(imageDescriptions, items) {
  const itemSummaries = items.map((item) => ({
    id: item.id,
    name: item.name,
    sort_order: item.sort_order,
    level: item.level,
    chapter: item.metadata?.chapter_name || item.category,
    scene_number: item.metadata?.scene_number,
    // first section text, truncated
    text_preview: Object.values(item.sections || {})[0]?.slice(0, 300) || '',
    has_image: !!item.image_url,
  }));

  const resp = await anthropic.messages.create({
    model: MODEL,
    max_tokens: 8000,
    messages: [{
      role: 'user',
      content: `You are matching illustrations to text passages from a grammar (structured literary work).

## ITEMS (text passages/scenes):
${JSON.stringify(itemSummaries, null, 2)}

## IMAGES (with vision descriptions):
${JSON.stringify(imageDescriptions, null, 2)}

## MATCHING RULES (in priority order):
1. **Visible text match** — If an image contains visible text (handwritten, printed on labels/signs/bottles), match it to the item whose text content contains those same words. This is the HIGHEST priority signal.
2. **Scene/character match** — Match illustrations to the scene they depict based on characters, setting, and action.
3. **Chapter-level fallback** — If an image shows a general chapter theme, assign it to the chapter-level (L2) item.
4. **One-to-one** — Each image goes to at most ONE item. Each item gets at most ONE image.
5. **Skip uncertain** — If an image doesn't clearly match any item, mark it as unmatched.

Return ONLY a JSON array (no markdown fences):
[
  { "item_id": "the-item-id", "file": "filename.jpg", "confidence": "high|medium|low", "reason": "brief explanation" },
  { "item_id": null, "file": "unmatched.jpg", "reason": "no clear match" }
]`,
    }],
  });

  return resp.content[0].text;
}

// ── Main ───────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  const flags = process.argv.slice(2).filter((a) => a.startsWith('--'));
  const shouldApply = flags.includes('--apply');

  if (args.length < 2) {
    console.log(`
Usage:
  node scripts/match-images-claude.js <images-folder> <grammar.json>
  node scripts/match-images-claude.js <images-folder> <grammar.json> --apply

Steps:
  1. Run without --apply to generate descriptions + matches
  2. Review image-matches.json and edit if needed
  3. Run with --apply to write matches into grammar.json

Requires ANTHROPIC_API_KEY in .env or environment.
`);
    process.exit(1);
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    console.error('Error: ANTHROPIC_API_KEY not set.');
    console.error('Create a .env file (see .env.example) or set it in your environment.');
    process.exit(1);
  }

  const imgDir = path.resolve(args[0]);
  const grammarPath = path.resolve(args[1]);

  if (!fs.existsSync(imgDir)) {
    console.error(`Image folder not found: ${imgDir}`);
    process.exit(1);
  }
  if (!fs.existsSync(grammarPath)) {
    console.error(`Grammar file not found: ${grammarPath}`);
    process.exit(1);
  }

  const grammar = JSON.parse(fs.readFileSync(grammarPath, 'utf8'));
  const files = fs.readdirSync(imgDir)
    .filter((f) => SUPPORTED_EXTS.includes(path.extname(f).toLowerCase()))
    .sort();

  console.log(`Found ${files.length} images in ${imgDir}`);
  console.log(`Grammar: ${grammar.name} (${grammar.items.length} items)\n`);

  // ── Phase 1 ──
  const descPath = path.join(path.dirname(grammarPath), 'image-descriptions.json');
  const matchPath = path.join(path.dirname(grammarPath), 'image-matches.json');
  let descriptions;

  // Reuse existing descriptions if available (skip re-scanning)
  if (!shouldApply && fs.existsSync(descPath)) {
    const existing = JSON.parse(fs.readFileSync(descPath, 'utf8'));
    const existingFiles = new Set(existing.map((d) => d.file));
    const newFiles = files.filter((f) => !existingFiles.has(f));
    if (newFiles.length === 0) {
      console.log('All images already described (reusing image-descriptions.json)');
      descriptions = existing;
    } else {
      console.log(`${existing.length} already described, ${newFiles.length} new images to scan\n`);
      descriptions = [...existing];
      // Only describe new ones
      for (let i = 0; i < newFiles.length; i += BATCH_SIZE) {
        const batch = newFiles.slice(i, i + BATCH_SIZE);
        const results = await Promise.allSettled(
          batch.map((f) => describeImage(path.join(imgDir, f)))
        );
        for (const r of results) {
          if (r.status === 'fulfilled') descriptions.push(r.value);
          else console.warn(`  FAIL: ${r.reason?.message || r.reason}`);
        }
        console.log(`  Described: ${descriptions.length - existing.length}/${newFiles.length}`);
      }
    }
  } else if (!shouldApply) {
    console.log('Phase 1: Describing images with Claude Vision...');
    descriptions = [];
    for (let i = 0; i < files.length; i += BATCH_SIZE) {
      const batch = files.slice(i, i + BATCH_SIZE);
      const results = await Promise.allSettled(
        batch.map((f) => describeImage(path.join(imgDir, f)))
      );
      for (const r of results) {
        if (r.status === 'fulfilled') descriptions.push(r.value);
        else console.warn(`  FAIL: ${r.reason?.message || r.reason}`);
      }
      console.log(`  Described: ${descriptions.length}/${files.length}`);
    }
  }

  if (!shouldApply) {
    fs.writeFileSync(descPath, JSON.stringify(descriptions, null, 2));
    console.log(`\nSaved: ${descPath}`);

    // ── Phase 2 ──
    console.log('\nPhase 2: Matching images to grammar items...');
    const matchResult = await matchAll(descriptions, grammar.items);
    fs.writeFileSync(matchPath, matchResult);
    console.log(`Saved: ${matchPath}`);
    console.log('\nReview the matches, then run again with --apply to update the grammar.');
    return;
  }

  // ── Apply mode ──
  if (!fs.existsSync(matchPath)) {
    console.error('No image-matches.json found. Run without --apply first.');
    process.exit(1);
  }

  const matches = JSON.parse(fs.readFileSync(matchPath, 'utf8'));
  let applied = 0;
  let skipped = 0;

  for (const match of matches) {
    if (!match.item_id) continue;
    if (match.confidence === 'low') {
      skipped++;
      continue;
    }

    const item = grammar.items.find((i) => i.id === match.item_id);
    if (!item) {
      console.warn(`  Item not found: ${match.item_id}`);
      continue;
    }

    // Build the image URL — adjust this to your hosting setup
    // For now, store the local path; you can replace with Drive/R2 URLs later
    const imgPath = path.join(imgDir, match.file);
    if (!fs.existsSync(imgPath)) {
      console.warn(`  Image not found: ${match.file}`);
      continue;
    }

    item.image_url = match.file; // or a full URL if you have one
    if (!item.metadata) item.metadata = {};
    item.metadata.matched_by = 'claude-vision';
    item.metadata.match_confidence = match.confidence;
    item.metadata.match_reason = match.reason;
    applied++;
  }

  // Backup original
  const backupPath = grammarPath.replace('.json', '.backup.json');
  fs.copyFileSync(grammarPath, backupPath);
  console.log(`Backup: ${backupPath}`);

  fs.writeFileSync(grammarPath, JSON.stringify(grammar, null, 2));
  console.log(`Applied ${applied} matches (skipped ${skipped} low-confidence)`);
  console.log(`Updated: ${grammarPath}`);
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
