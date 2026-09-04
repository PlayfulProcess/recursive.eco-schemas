#!/usr/bin/env node

/**
 * update-assignments-from-csv.mjs
 *
 * Reads a CSV embedded in a transcript JSONL file (line 11760),
 * parses the illustration assignment data, compares it with the
 * current illustration-assignments.json, and writes the updated file.
 */

import { readFileSync, writeFileSync } from 'fs';

const TRANSCRIPT_PATH = 'C:/Users/ferna/.claude/projects/C--Users-ferna-OneDrive-Documentos-GitHub/f862eca8-50ed-40fd-8fa5-f70096e8c5be.jsonl';
const ASSIGNMENTS_PATH = 'C:/Users/ferna/OneDrive/Documentos/GitHub/recursive.eco-schemas/grammars/alice-5-minute-stories/illustration-assignments.json';
const TARGET_LINE = 11760; // 1-indexed

// --- Step 1: Read the specific line from the JSONL ---
console.log(`Reading line ${TARGET_LINE} from transcript...`);
const allLines = readFileSync(TRANSCRIPT_PATH, 'utf-8').split('\n');
const line = allLines[TARGET_LINE - 1]; // convert to 0-indexed
const jsonObj = JSON.parse(line);
const content = jsonObj.content;

// --- Step 2: Extract CSV from content ---
// The content has preamble text, then "chapter,page,image_url,image_info,comment\n" followed by CSV rows
const csvHeaderMatch = content.indexOf('chapter,page,image_url,image_info,comment');
if (csvHeaderMatch === -1) {
  console.error('ERROR: Could not find CSV header in content field');
  process.exit(1);
}

const csvText = content.slice(csvHeaderMatch);
const csvLines = csvText.split('\n').filter(l => l.trim());

console.log(`Found CSV with ${csvLines.length - 1} data rows (plus header)`);

// --- Step 3: Parse CSV with proper quoted field handling ---
function parseCSVLine(line) {
  const fields = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && i + 1 < line.length && line[i + 1] === '"') {
        // Escaped quote inside quoted field
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      fields.push(current);
      current = '';
    } else {
      current += ch;
    }
  }
  fields.push(current);
  return fields;
}

// Skip header row
const csvRows = csvLines.slice(1).map(line => {
  const fields = parseCSVLine(line);
  return {
    chapter: parseInt(fields[0], 10),
    page: parseInt(fields[1], 10),
    image_url: fields[2] || '',
    image_info: fields[3] || '',
    comment: fields[4] || ''
  };
});

console.log(`Parsed ${csvRows.length} CSV entries`);

// --- Step 4: Read current assignments ---
console.log(`\nReading current assignments from JSON...`);
const currentAssignments = JSON.parse(readFileSync(ASSIGNMENTS_PATH, 'utf-8'));
console.log(`Current JSON has ${currentAssignments.length} entries`);

// --- Step 5: Compare and find differences ---
// Build lookup maps
const currentMap = new Map();
for (const item of currentAssignments) {
  currentMap.set(`${item.chapter}:${item.page}`, item);
}

const csvMap = new Map();
for (const item of csvRows) {
  csvMap.set(`${item.chapter}:${item.page}`, item);
}

const differences = [];

// Check for changes and additions
for (const [key, csvItem] of csvMap) {
  const currentItem = currentMap.get(key);
  if (!currentItem) {
    differences.push({
      type: 'ADDED',
      key,
      csv: csvItem,
      current: null
    });
  } else {
    const changes = [];
    if (currentItem.image_url !== csvItem.image_url) {
      changes.push({ field: 'image_url', old: currentItem.image_url, new: csvItem.image_url });
    }
    if (currentItem.image_info !== csvItem.image_info) {
      changes.push({ field: 'image_info', old: currentItem.image_info, new: csvItem.image_info });
    }
    if (currentItem.comment !== csvItem.comment) {
      changes.push({ field: 'comment', old: currentItem.comment, new: csvItem.comment });
    }
    if (changes.length > 0) {
      differences.push({
        type: 'CHANGED',
        key,
        changes,
        csv: csvItem,
        current: currentItem
      });
    }
  }
}

// Check for removals
for (const [key, currentItem] of currentMap) {
  if (!csvMap.has(key)) {
    differences.push({
      type: 'REMOVED',
      key,
      csv: null,
      current: currentItem
    });
  }
}

// --- Step 6: Report differences ---
console.log(`\n${'='.repeat(80)}`);
console.log(`DIFFERENCES FOUND: ${differences.length}`);
console.log(`${'='.repeat(80)}\n`);

for (const diff of differences) {
  if (diff.type === 'CHANGED') {
    console.log(`CHANGED  ch${diff.csv.chapter} p${diff.csv.page}:`);
    for (const change of diff.changes) {
      const oldVal = change.old || '(empty)';
      const newVal = change.new || '(empty)';
      // Truncate long URLs for readability
      const oldDisplay = oldVal.length > 80 ? '...' + oldVal.slice(-60) : oldVal;
      const newDisplay = newVal.length > 80 ? '...' + newVal.slice(-60) : newVal;
      console.log(`  ${change.field}:`);
      console.log(`    OLD: ${oldDisplay}`);
      console.log(`    NEW: ${newDisplay}`);
    }
    console.log('');
  } else if (diff.type === 'ADDED') {
    console.log(`ADDED    ch${diff.csv.chapter} p${diff.csv.page}: ${diff.csv.image_info}`);
  } else if (diff.type === 'REMOVED') {
    console.log(`REMOVED  ch${diff.current.chapter} p${diff.current.page}: ${diff.current.image_info}`);
  }
}

// --- Step 7: Write updated JSON ---
console.log(`\nWriting updated assignments (${csvRows.length} entries)...`);
writeFileSync(ASSIGNMENTS_PATH, JSON.stringify(csvRows, null, 2) + '\n', 'utf-8');
console.log(`Done! Updated ${ASSIGNMENTS_PATH}`);
