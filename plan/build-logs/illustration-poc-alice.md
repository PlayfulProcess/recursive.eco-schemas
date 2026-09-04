# Build Log: Illustration POC — Alice in Wonderland

**Date:** 2026-03-06
**Status:** SUCCESS — POC proven end-to-end
**Grammar:** `alice-in-wonderland-chapter-book`

## What Was Proven

1. **Vision matching works**: Claude can see public domain illustrations, identify scenes, match to grammar items with high confidence across multiple artists (Rackham, Hudson, Carroll manuscript, Tenniel)
2. **L1/L2/Cover distinction works**: Narrative scene images (L1) correctly distinguished from chapter cast images (L2) and title pages (Cover)
3. **Inline metadata approach works**: `metadata.illustrations[]` on grammar items — no DB migration needed, no new tables
4. **R2 upload works**: 5 images uploaded to Cloudflare R2 via S3-compatible API using `upload-test-illustrations.mjs`
5. **GrammarReader rendering works**: Code merged to main, build passes with zero errors
6. **Multi-artist rendering works**: `ch05-who-are-you` has 2 illustrations (Hudson primary as hero, Rackham secondary inline with attribution)

## Files Modified/Created

### In `recursive-eco` (app repo, pushed to main):
- `apps/flow/src/lib/offer/unified-grammar-types.ts` — Added `Illustration` interface
- `apps/flow/src/components/GrammarReader.tsx` — Added inline illustrations rendering block
- `apps/flow/scripts/upload-test-illustrations.mjs` — Batch upload script

### In `recursive.eco-schemas` (this repo):
- `grammars/alice-in-wonderland-chapter-book/grammar.json` — Added `image_url` + `metadata.illustrations[]` to 4 items
- `grammars/alice-in-wonderland-chapter-book/image-matching-log.json` — Per-grammar audit trail
- `z.ignore/manuscript-images/IMAGE_MAPPING.md` — Full mapping of 139 Alice images to grammar items
- `CLAUDE.md` — Added Illustration System section with architecture, workflow, env requirements

## R2 URLs (Live)
```
grammar-illustrations/alice-in-wonderland/ch05-who-are-you/gwynedd-hudson-1922.jpg
grammar-illustrations/alice-in-wonderland/ch05-who-are-you/arthur-rackham-1907.jpg
grammar-illustrations/alice-in-wonderland/ch07-no-room/arthur-rackham-1907.jpg
grammar-illustrations/alice-in-wonderland/chapter-07-a-mad-tea-party/gwynedd-hudson-1922.jpg
grammar-illustrations/alice-in-wonderland/ch08-painting-the-roses-red/gwynedd-hudson-1922.jpg
```
Base URL: `https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/`

## Environment Requirements Discovered

- **R2 credentials** are in `recursive-eco/.env.local` (root level), NOT `apps/flow/.env.local`
- **dotenv** not installed in monorepo — upload script manually parses `.env.local`
- **R2 upload + vision matching over local images** requires Claude Code desktop (filesystem + S3 API access)
- **Grammar JSON editing** (adding illustration metadata after URLs are known) can be done in Claude Code browser

## Remaining Work for Alice

- 139 total images mapped in IMAGE_MAPPING.md — only 5 uploaded so far
- Upload remaining images and add metadata to grammar items
- Key items still needing illustrations: ch01-down-the-rabbit-hole, ch02-the-pool-of-tears, ch06-pig-and-pepper, ch09-the-mock-turtles-story, ch12-alices-evidence, all L2 chapters

## Reproducible Workflow for Other Grammars

1. Curate public domain images into `z.ignore/manuscript-images/{collection}/`
2. Use Claude vision to match images to grammar items (Claude Code desktop)
3. Upload to R2 using `upload-test-illustrations.mjs` (Claude Code desktop)
4. Add `image_url` + `metadata.illustrations[]` to grammar JSON (either desktop or browser)
5. Import grammar on website — illustrations render automatically
6. Log matches in per-grammar `image-matching-log.json`
