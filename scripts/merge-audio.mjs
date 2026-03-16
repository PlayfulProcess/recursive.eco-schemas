#!/usr/bin/env node
/**
 * merge-audio.mjs — Concatenate 12 chapter MP3s into one unified file
 * and generate a karaoke manifest with absolute timestamps.
 *
 * MP3 is frame-based, so concatenation of CBR files works by
 * stripping ID3 tags and appending raw MPEG audio data.
 *
 * Output:
 *   audio/librivox/wonderland-complete.mp3
 *   audio/librivox/karaoke-manifest-unified.json
 */

import { readFileSync, writeFileSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const GRAMMAR_DIR = join(__dirname, '..', 'grammars', 'alice-5-minute-stories');
const AUDIO_DIR = join(GRAMMAR_DIR, 'audio', 'librivox');

// Read the original per-chapter manifest
const manifest = JSON.parse(readFileSync(join(AUDIO_DIR, 'karaoke-manifest.json'), 'utf8'));
const chapterNums = Object.keys(manifest.chapters).map(Number).sort((a, b) => a - b);

console.log(`Merging ${chapterNums.length} chapters...`);

/**
 * Strip ID3v2 header from start of buffer (if present).
 * ID3v2 header: "ID3" + version(2 bytes) + flags(1 byte) + size(4 bytes syncsafe)
 */
function stripID3v2(buf) {
  if (buf[0] === 0x49 && buf[1] === 0x44 && buf[2] === 0x33) { // "ID3"
    // Size is 4 bytes, syncsafe integer (7 bits per byte)
    const size = (buf[6] << 21) | (buf[7] << 14) | (buf[8] << 7) | buf[9];
    const headerSize = 10 + size;
    console.log(`  Stripped ID3v2 header: ${headerSize} bytes`);
    return buf.subarray(headerSize);
  }
  return buf;
}

/**
 * Strip ID3v1 tag from end of buffer (if present).
 * ID3v1: last 128 bytes starting with "TAG"
 */
function stripID3v1(buf) {
  if (buf.length > 128) {
    const tagStart = buf.length - 128;
    if (buf[tagStart] === 0x54 && buf[tagStart + 1] === 0x41 && buf[tagStart + 2] === 0x47) { // "TAG"
      console.log(`  Stripped ID3v1 tag: 128 bytes`);
      return buf.subarray(0, tagStart);
    }
  }
  return buf;
}

// Concatenate all chapter audio data
const chunks = [];
let cumulativeOffset = 0;
const chapterOffsets = [];

for (const chNum of chapterNums) {
  const chData = manifest.chapters[chNum];
  const filePath = join(AUDIO_DIR, chData.audio_file);
  const fileSize = statSync(filePath).size;

  console.log(`\nChapter ${chNum}: ${chData.audio_file} (${(fileSize / 1024 / 1024).toFixed(1)} MB, ${chData.duration_s.toFixed(1)}s)`);

  let buf = readFileSync(filePath);
  buf = stripID3v2(buf);
  buf = stripID3v1(buf);

  chunks.push(buf);
  chapterOffsets.push({
    chapter: chNum,
    offset: cumulativeOffset,
    duration: chData.duration_s,
  });

  console.log(`  Offset: ${cumulativeOffset.toFixed(2)}s → ${(cumulativeOffset + chData.duration_s).toFixed(2)}s`);
  cumulativeOffset += chData.duration_s;
}

// Write merged MP3
const merged = Buffer.concat(chunks);
const outputPath = join(AUDIO_DIR, 'wonderland-complete.mp3');
writeFileSync(outputPath, merged);
console.log(`\nMerged: ${outputPath} (${(merged.length / 1024 / 1024).toFixed(1)} MB)`);
console.log(`Total duration: ${cumulativeOffset.toFixed(1)}s (${(cumulativeOffset / 60).toFixed(1)} min)`);

// Generate unified karaoke manifest with absolute timestamps
const unifiedManifest = {
  generated: new Date().toISOString(),
  source: 'Merged from per-chapter LibriVox karaoke manifest',
  audio_file: 'wonderland-complete.mp3',
  total_duration_s: cumulativeOffset,
  chapters: {},
};

for (const chNum of chapterNums) {
  const chData = manifest.chapters[chNum];
  const offsetInfo = chapterOffsets.find(c => c.chapter === chNum);
  const offset = offsetInfo.offset;

  // Shift all word timestamps by the cumulative offset
  const shiftedPages = chData.pages.map(page => ({
    pageNum: page.pageNum,
    words: page.words.map(w => ({
      display: w.display,
      start: w.start + offset,
      end: w.end + offset,
    })),
  }));

  unifiedManifest.chapters[chNum] = {
    chapter: chNum,
    offset: offset,
    duration: chData.duration_s,
    pages: shiftedPages,
  };
}

const manifestPath = join(AUDIO_DIR, 'karaoke-manifest-unified.json');
writeFileSync(manifestPath, JSON.stringify(unifiedManifest, null, 2));
console.log(`Manifest: ${manifestPath}`);

// Summary
console.log('\nChapter offsets:');
for (const co of chapterOffsets) {
  const min = Math.floor(co.offset / 60);
  const sec = Math.floor(co.offset % 60);
  console.log(`  Ch${co.chapter}: ${min}:${sec < 10 ? '0' : ''}${sec}`);
}
