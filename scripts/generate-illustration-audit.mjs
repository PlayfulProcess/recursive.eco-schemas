/**
 * Generate an interactive HTML audit page for illustration-to-page assignments.
 *
 * Shows each assignment as a card with:
 *   - Illustration image (click to zoom)
 *   - Matched page text
 *   - Scene description + match score
 *   - OK / Wrong / Notes buttons
 *   - Export corrections as JSON
 *
 * Usage:
 *   node scripts/generate-illustration-audit.mjs
 *
 * Output: grammars/alice-5-minute-stories/booklets/illustration-audit.html
 */
import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const assignmentsPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-assignments.json');
const bookletGrammarPath = resolve(__dirname, '../grammars/alice-5-minute-stories/grammar.json');
const outputPath = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets/illustration-audit.html');

const assignments = JSON.parse(readFileSync(assignmentsPath, 'utf8'));
const bookletGrammar = JSON.parse(readFileSync(bookletGrammarPath, 'utf8'));

// Build full page text lookup
const pageTextByChapter = {};
for (const item of bookletGrammar.items) {
  const chNum = item.metadata?.source_chapter;
  if (!chNum) continue;
  pageTextByChapter[chNum] = {};
  const pageCount = item.metadata?.page_count || 0;
  for (let p = 1; p <= pageCount; p++) {
    pageTextByChapter[chNum][p] = item.sections?.[`Page ${p}`] || '';
  }
}

// Build chapter names
const chapterNames = {};
for (const item of bookletGrammar.items) {
  const chNum = item.metadata?.source_chapter;
  if (chNum) chapterNames[chNum] = item.name;
}

function esc(s) {
  return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Group assignments by chapter
const byChapter = {};
for (const a of assignments) {
  if (!byChapter[a.chapter]) byChapter[a.chapter] = [];
  byChapter[a.chapter].push(a);
}

// Generate entry HTML for each assignment
let entriesHtml = '';
let totalWithImage = 0;
let totalTextOnly = 0;
let idx = 0;

for (const chNum of Object.keys(byChapter).map(Number).sort((a, b) => a - b)) {
  const chAssignments = byChapter[chNum];
  const chName = chapterNames[chNum] || `Chapter ${chNum}`;

  entriesHtml += `<div class="chapter-divider">Chapter ${chNum}: ${esc(chName)}</div>\n`;

  for (const a of chAssignments) {
    const hasImage = a.image_url && a.image_url.length > 0;
    const pageText = a.page === 0
      ? `[COVER PAGE]`
      : (pageTextByChapter[chNum]?.[a.page] || a.text_preview || '');
    const textPreview = pageText.substring(0, 400);

    if (hasImage) totalWithImage++;
    else totalTextOnly++;

    entriesHtml += `
<div class="entry" data-idx="${idx}" data-chapter="${chNum}" data-page="${a.page}" data-status="pending">
  <div class="entry-img">
    ${hasImage
      ? `<img src="${esc(a.image_url)}" alt="${esc(a.image_info)}" onclick="toggleZoom(this)" loading="lazy">`
      : `<div style="width:100%;height:200px;background:#111;display:flex;align-items:center;justify-content:center;border-radius:4px;color:var(--muted);font-style:italic;">No illustration assigned</div>`
    }
    <div class="img-meta">
      <div class="artist">${esc(a.image_info || 'text-only')}</div>
      <div>${esc(a.label)} &mdash; ${a.page === 0 ? 'Cover' : `Page ${a.page}`}</div>
    </div>
  </div>
  <div class="entry-content">
    <div class="entry-header">
      <div>
        <strong>Ch ${chNum}, ${a.page === 0 ? 'Cover' : `Page ${a.page}`}</strong>
        ${hasImage ? '' : '<span style="color:var(--warn);margin-left:8px;">[TEXT-ONLY]</span>'}
      </div>
      <span class="item-badge">${esc(a.label)}</span>
    </div>
    ${hasImage ? `<div class="scene-label">Scene: ${esc(a.image_info)}</div>` : ''}
    <div class="text-passage">${esc(textPreview)}</div>
    <div class="actions">
      <button class="btn-ok" onclick="setStatus(${idx},'confirmed')">&#10004; OK</button>
      <button class="btn-wrong" onclick="setStatus(${idx},'wrong')">&#10008; Wrong</button>
      <input class="notes-input" placeholder="Notes (optional)..." oninput="setNote(${idx}, this.value)">
    </div>
  </div>
</div>`;
    idx++;
  }
}

const totalEntries = assignments.length;

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Alice in Wonderland — Illustration Audit</title>
<style>
:root {
  --bg: #1a1a2e;
  --card: #16213e;
  --accent: #e94560;
  --ok: #4ecca3;
  --warn: #f5a623;
  --text: #eee;
  --muted: #888;
  --border: #333;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Georgia', serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  padding-bottom: 80px;
}
.header {
  background: var(--card);
  padding: 20px 30px;
  border-bottom: 2px solid var(--accent);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header h1 { font-size: 1.4em; margin-bottom: 5px; }
.stats { display: flex; gap: 20px; font-size: 0.9em; color: var(--muted); flex-wrap: wrap; }
.stats .warn { color: var(--warn); font-weight: bold; }
.stats .ok { color: var(--ok); }
.controls {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  flex-wrap: wrap;
}
.controls button {
  padding: 6px 14px;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text);
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.85em;
}
.controls button:hover { border-color: var(--accent); }
.controls button.active { background: var(--accent); border-color: var(--accent); }

.container { max-width: 1400px; margin: 0 auto; padding: 20px; }

.entry {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 20px;
  background: var(--card);
  border: 2px solid var(--border);
  border-radius: 8px;
  margin-bottom: 16px;
  padding: 16px;
  transition: border-color 0.3s, opacity 0.3s;
}
.entry[data-status="confirmed"] { border-color: var(--ok); opacity: 0.6; }
.entry[data-status="wrong"] { border-color: var(--accent); }

.entry-img { display: flex; flex-direction: column; gap: 8px; }
.entry-img img {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  border-radius: 4px;
  background: #111;
  cursor: pointer;
}
.entry-img img.zoomed {
  max-height: none;
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 1000;
  object-fit: contain;
  background: rgba(0,0,0,0.95);
  border-radius: 0;
  padding: 20px;
}
.img-meta { font-size: 0.8em; color: var(--muted); }
.img-meta .artist { color: var(--text); font-weight: bold; }

.entry-content { display: flex; flex-direction: column; gap: 12px; }
.entry-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; }
.item-badge {
  background: var(--bg); padding: 4px 10px; border-radius: 4px;
  font-size: 0.85em; font-family: monospace; white-space: nowrap;
}
.scene-label {
  font-style: italic; color: var(--warn); font-size: 0.9em;
  padding: 4px 8px; background: rgba(245,166,35,0.1); border-radius: 4px;
}
.text-passage {
  background: var(--bg); padding: 12px 16px; border-radius: 6px;
  font-size: 0.9em; line-height: 1.7; max-height: 200px;
  overflow-y: auto; white-space: pre-wrap;
  border-left: 3px solid var(--accent);
}
.actions { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.actions button {
  padding: 5px 12px; border: 1px solid var(--border);
  background: var(--bg); color: var(--text);
  cursor: pointer; border-radius: 4px; font-size: 0.8em;
}
.actions button:hover { opacity: 0.8; }
.actions .btn-ok { border-color: var(--ok); color: var(--ok); }
.actions .btn-ok.active { background: var(--ok); color: #000; }
.actions .btn-wrong { border-color: var(--accent); color: var(--accent); }
.actions .btn-wrong.active { background: var(--accent); color: #fff; }
.notes-input {
  padding: 4px 8px; background: var(--bg); color: var(--text);
  border: 1px solid var(--border); border-radius: 4px;
  font-size: 0.8em; flex: 1; min-width: 200px;
}
.chapter-divider {
  background: var(--accent); color: #fff;
  padding: 10px 20px; margin: 24px 0 12px;
  border-radius: 6px; font-size: 1.1em; font-weight: bold;
}
.export-bar {
  position: fixed; bottom: 0; left: 0; right: 0;
  background: var(--card); border-top: 2px solid var(--accent);
  padding: 12px 30px; display: flex;
  justify-content: space-between; align-items: center; z-index: 100;
}
.export-bar button {
  padding: 8px 20px; background: var(--accent); color: #fff;
  border: none; border-radius: 4px; cursor: pointer;
  font-size: 1em; font-weight: bold;
}
.export-bar button:hover { opacity: 0.9; }
.hidden { display: none !important; }
@media (max-width: 900px) { .entry { grid-template-columns: 1fr; } }
</style>
</head>
<body>

<div class="header">
  <h1>Alice in Wonderland &mdash; Illustration-to-Page Audit</h1>
  <p style="color:var(--muted);font-size:0.85em;margin-bottom:8px;">
    Review each illustration against its matched page text. Click images to zoom.
    Mark as OK or Wrong. Add notes for swaps. Export corrections when done.
  </p>
  <div class="stats">
    <span>Total: <strong>${totalEntries}</strong> entries</span>
    <span>With illustration: <strong>${totalWithImage}</strong></span>
    <span>Text-only: <strong>${totalTextOnly}</strong></span>
    <span class="ok">Confirmed: <strong id="stat-ok">0</strong></span>
    <span class="warn">Wrong: <strong id="stat-wrong">0</strong></span>
    <span>Pending: <strong id="stat-pending">${totalEntries}</strong></span>
  </div>
  <div class="controls">
    <button onclick="filterView('all')" class="active" id="btn-all">Show All</button>
    <button onclick="filterView('pending')" id="btn-pending">Pending Only</button>
    <button onclick="filterView('wrong')" id="btn-wrong">Wrong Only</button>
    <button onclick="filterView('confirmed')" id="btn-confirmed">Confirmed Only</button>
    <button onclick="filterView('has-image')" id="btn-has-image">With Images</button>
  </div>
</div>

<div class="container">
${entriesHtml}
</div>

<div class="export-bar">
  <span id="export-summary">Review illustrations, then export corrections</span>
  <button onclick="exportCorrections()">Export Corrections JSON</button>
</div>

<script>
var entries = document.querySelectorAll('.entry');
var statuses = {};
var notes = {};

function toggleZoom(img) {
  img.classList.toggle('zoomed');
  if (img.classList.contains('zoomed')) {
    img.addEventListener('click', function handler() {
      img.classList.remove('zoomed');
    }, { once: true });
  }
}

function setStatus(idx, status) {
  var entry = document.querySelector('[data-idx="' + idx + '"]');
  var current = entry.dataset.status;
  if (current === status) {
    entry.dataset.status = 'pending';
    delete statuses[idx];
  } else {
    entry.dataset.status = status;
    statuses[idx] = status;
  }
  // Toggle button active states
  var btns = entry.querySelectorAll('.actions button');
  btns.forEach(function(btn) { btn.classList.remove('active'); });
  if (entry.dataset.status === 'confirmed') btns[0].classList.add('active');
  if (entry.dataset.status === 'wrong') btns[1].classList.add('active');
  updateStats();
}

function setNote(idx, note) {
  if (note) notes[idx] = note;
  else delete notes[idx];
}

function updateStats() {
  var ok = 0, wrong = 0, pending = 0;
  entries.forEach(function(e) {
    var s = e.dataset.status;
    if (s === 'confirmed') ok++;
    else if (s === 'wrong') wrong++;
    else pending++;
  });
  document.getElementById('stat-ok').textContent = ok;
  document.getElementById('stat-wrong').textContent = wrong;
  document.getElementById('stat-pending').textContent = pending;
  document.getElementById('export-summary').textContent =
    ok + ' confirmed, ' + wrong + ' wrong, ' + pending + ' pending';
}

function filterView(view) {
  document.querySelectorAll('.controls button').forEach(function(b) { b.classList.remove('active'); });
  document.getElementById('btn-' + view).classList.add('active');
  entries.forEach(function(e) {
    var show = true;
    if (view === 'pending') show = e.dataset.status === 'pending';
    else if (view === 'wrong') show = e.dataset.status === 'wrong';
    else if (view === 'confirmed') show = e.dataset.status === 'confirmed';
    else if (view === 'has-image') show = !!e.querySelector('img');
    e.classList.toggle('hidden', !show);
  });
  // Also toggle chapter dividers
  document.querySelectorAll('.chapter-divider').forEach(function(d) {
    if (view === 'all') { d.classList.remove('hidden'); return; }
    // Show divider if any sibling entry is visible
    var next = d.nextElementSibling;
    var hasVisible = false;
    while (next && !next.classList.contains('chapter-divider')) {
      if (next.classList.contains('entry') && !next.classList.contains('hidden')) hasVisible = true;
      next = next.nextElementSibling;
    }
    d.classList.toggle('hidden', !hasVisible);
  });
}

function exportCorrections() {
  var corrections = [];
  entries.forEach(function(e) {
    var idx = parseInt(e.dataset.idx);
    var status = e.dataset.status;
    if (status === 'wrong' || notes[idx]) {
      corrections.push({
        chapter: parseInt(e.dataset.chapter),
        page: parseInt(e.dataset.page),
        status: status,
        note: notes[idx] || '',
        current_image: e.querySelector('img') ? e.querySelector('img').src : '',
      });
    }
  });

  if (corrections.length === 0) {
    alert('No corrections to export. Mark items as "Wrong" or add notes first.');
    return;
  }

  var json = JSON.stringify(corrections, null, 2);
  var blob = new Blob([json], { type: 'application/json' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'illustration-corrections.json';
  a.click();
  URL.revokeObjectURL(url);
}

// Keyboard: Space = OK on focused entry
document.addEventListener('keydown', function(e) {
  if (e.target.tagName === 'INPUT') return;
  if (e.key === 'j' || e.key === 'ArrowDown') {
    e.preventDefault();
    scrollToNext(1);
  }
  if (e.key === 'k' || e.key === 'ArrowUp') {
    e.preventDefault();
    scrollToNext(-1);
  }
});

var currentFocusIdx = -1;
function scrollToNext(dir) {
  var visible = Array.from(entries).filter(function(e) { return !e.classList.contains('hidden'); });
  if (visible.length === 0) return;
  currentFocusIdx = Math.max(0, Math.min(visible.length - 1, currentFocusIdx + dir));
  visible[currentFocusIdx].scrollIntoView({ behavior: 'smooth', block: 'center' });
}
</script>
</body>
</html>`;

writeFileSync(outputPath, html);
console.log('Audit page written:', outputPath);
console.log(totalEntries, 'entries (' + totalWithImage + ' with images, ' + totalTextOnly + ' text-only)');
