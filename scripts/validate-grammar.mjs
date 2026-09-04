#!/usr/bin/env node
/**
 * Grammar PR validator — copy to scripts/validate-grammar.mjs in each public data repo
 * (invoked by .github/workflows/validate-grammar.yml).
 *
 *   node scripts/validate-grammar.mjs <baseRef>
 *
 * For every grammar.json changed in the PR it checks:
 *   1. valid JSON;
 *   2. required fields present (name: non-empty string, items: array);
 *   3. NO top-level field present on the base branch is missing in the PR head
 *      — the silent-overwrite guard (the Visconti-Sforza bug). New files skip (3).
 * Exits non-zero on any failure so the PR check goes red.
 */
import { execSync } from 'node:child_process';
import { readFileSync, existsSync } from 'node:fs';

const baseRef = process.argv[2] || 'origin/main';

function sh(cmd) {
  return execSync(cmd, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
}

function isGrammarPath(p) {
  return /(^|\/)grammar\.json$/.test(p) || /^(tarot|grammars)\//.test(p) || /\.json$/.test(p.split('/').pop());
}

let changed = [];
try {
  changed = sh(`git diff --name-only --diff-filter=AM ${baseRef}...HEAD`)
    .split('\n').map(s => s.trim()).filter(Boolean).filter(isGrammarPath);
} catch (e) {
  console.error('Could not compute changed files:', e.message);
  process.exit(1);
}

if (changed.length === 0) {
  console.log('No grammar files changed — nothing to validate.');
  process.exit(0);
}

const errors = [];
for (const file of changed) {
  if (!existsSync(file)) continue; // deleted in head
  let head;
  try {
    head = JSON.parse(readFileSync(file, 'utf8'));
  } catch (e) {
    errors.push(`${file}: invalid JSON — ${e.message}`);
    continue;
  }
  // (2) required fields
  if (typeof head.name !== 'string' || !head.name.trim()) errors.push(`${file}: missing required "name"`);
  if (!Array.isArray(head.items)) errors.push(`${file}: "items" must be an array`);

  // (3) dropped-field guard vs base
  let base = null;
  try { base = JSON.parse(sh(`git show ${baseRef}:${file}`)); } catch { /* new file → no base */ }
  if (base && typeof base === 'object') {
    const dropped = Object.keys(base).filter(k => !(k in head));
    if (dropped.length) {
      errors.push(`${file}: would DROP top-level field(s) present on base: ${dropped.join(', ')} — merge onto the existing file instead of replacing it`);
    }
  }
  if (!errors.some(e => e.startsWith(file))) console.log(`✓ ${file}`);
}

if (errors.length) {
  console.error('\n✗ Grammar validation failed:');
  for (const e of errors) console.error('  - ' + e);
  process.exit(1);
}
console.log(`\n✓ All ${changed.length} changed grammar file(s) valid.`);
