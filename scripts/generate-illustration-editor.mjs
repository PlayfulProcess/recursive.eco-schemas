/**
 * Generate an interactive illustration EDITOR for the booklets.
 *
 * Features:
 *   - Shows each chapter's pages in a grid with illustration + text preview
 *   - RIGHT-CLICK an image → prompt for target page number → moves it there
 *   - Press X on an image → removes it (text-only)
 *   - Click image → zoom
 *   - Export CSV of final assignments
 *   - Tracks all changes for Claude Code to apply
 *
 * Usage: node scripts/generate-illustration-editor.mjs
 * Output: grammars/alice-5-minute-stories/booklets/illustration-editor.html
 */
import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const assignmentsPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-assignments.json');
const bookletGrammarPath = resolve(__dirname, '../grammars/alice-5-minute-stories/grammar.json');
const outputPath = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets/illustration-editor.html');

const assignments = JSON.parse(readFileSync(assignmentsPath, 'utf8'));
const bookletGrammar = JSON.parse(readFileSync(bookletGrammarPath, 'utf8'));

// Build page text
const chapters = {};
for (const item of bookletGrammar.items) {
  const ch = item.metadata?.source_chapter;
  if (!ch) continue;
  chapters[ch] = { name: item.name, pages: {} };
  for (let p = 1; p <= (item.metadata?.page_count || 0); p++) {
    chapters[ch].pages[p] = (item.sections?.[`Page ${p}`] || '').substring(0, 120);
  }
}

function esc(s) {
  return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// Build the data JSON for the editor
const dataJson = JSON.stringify(assignments.map(a => ({
  ch: a.chapter,
  pg: a.page,
  url: a.image_url || '',
  info: a.image_info || '',
  label: a.label,
  text: a.text_preview || '',
})));

const chapterJson = JSON.stringify(chapters);

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Alice — Illustration Editor</title>
<style>
:root { --bg: #111; --card: #1a1a2e; --accent: #e94560; --ok: #4ecca3; --text: #eee; --muted: #777; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Georgia, serif; background: var(--bg); color: var(--text); }
.header {
  background: var(--card); padding: 16px 24px; position: sticky; top: 0; z-index: 100;
  border-bottom: 2px solid var(--accent); display: flex; justify-content: space-between; align-items: center;
}
.header h1 { font-size: 1.2em; }
.header .actions { display: flex; gap: 10px; }
.header button {
  padding: 8px 18px; border: none; border-radius: 4px; cursor: pointer;
  font-weight: bold; font-size: 0.9em;
}
.btn-export { background: var(--ok); color: #000; }
.btn-undo { background: #555; color: #fff; }
.changes-count { color: var(--accent); font-weight: bold; font-size: 0.9em; }

.chapter-section { padding: 12px 24px; }
.chapter-title {
  background: var(--accent); color: white; padding: 8px 16px; border-radius: 6px;
  margin: 16px 0 8px; font-size: 1em; font-weight: bold;
}
.page-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px; padding: 8px 0;
}
.page-card {
  background: var(--card); border: 2px solid #333; border-radius: 8px;
  overflow: hidden; transition: border-color 0.2s; position: relative;
}
.page-card.selected { border-color: var(--accent); }
.page-card.changed { border-color: var(--ok); }
.page-card.removed { border-color: #e94560; opacity: 0.5; }
.page-card .page-label {
  padding: 6px 10px; font-size: 0.75em; color: var(--muted);
  display: flex; justify-content: space-between;
}
.page-card .page-label strong { color: var(--text); }
.page-card .img-wrap {
  width: 100%; height: 200px; background: #0a0a0a; display: flex;
  align-items: center; justify-content: center; cursor: pointer;
  position: relative; overflow: hidden;
}
.page-card .img-wrap img {
  max-width: 100%; max-height: 100%; object-fit: contain;
}
.page-card .img-wrap .no-img {
  color: var(--muted); font-style: italic; font-size: 0.85em;
}
.page-card .text-preview {
  padding: 8px 10px; font-size: 0.7em; color: var(--muted);
  max-height: 60px; overflow: hidden; line-height: 1.4;
}
.page-card .img-info {
  padding: 4px 10px 8px; font-size: 0.7em; color: var(--ok);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.page-card .badge-moved {
  position: absolute; top: 4px; right: 4px; background: var(--ok);
  color: #000; font-size: 0.65em; padding: 2px 6px; border-radius: 3px;
  font-weight: bold;
}
.page-card .badge-removed {
  position: absolute; top: 4px; right: 4px; background: var(--accent);
  color: #fff; font-size: 0.65em; padding: 2px 6px; border-radius: 3px;
  font-weight: bold;
}

/* Context menu */
.ctx-menu {
  position: fixed; background: var(--card); border: 1px solid #555;
  border-radius: 6px; padding: 6px 0; z-index: 1000; min-width: 200px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5); display: none;
}
.ctx-menu .ctx-item {
  padding: 8px 16px; cursor: pointer; font-size: 0.85em;
  display: flex; gap: 8px; align-items: center;
}
.ctx-menu .ctx-item:hover { background: rgba(255,255,255,0.1); }
.ctx-menu .ctx-sep { height: 1px; background: #444; margin: 4px 0; }

/* Zoom overlay */
.zoom-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.95);
  z-index: 999; display: none; cursor: pointer;
  align-items: center; justify-content: center;
}
.zoom-overlay img { max-width: 95vw; max-height: 95vh; object-fit: contain; }

.help-text { padding: 12px 24px; color: var(--muted); font-size: 0.8em; line-height: 1.6; }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>Illustration Editor</h1>
    <span class="changes-count" id="changesCount">0 changes</span>
  </div>
  <div class="actions">
    <button class="btn-undo" onclick="undoLast()">Undo</button>
    <button class="btn-export" onclick="exportCSV()">Export CSV</button>
  </div>
</div>

<div class="help-text">
  <strong>Right-click</strong> an image to move it to a different page or delete it.
  <strong>Click</strong> to zoom. Changes are tracked — export CSV when done.
</div>

<div id="content"></div>

<div class="ctx-menu" id="ctxMenu">
  <div class="ctx-item" onclick="promptMoveTo()">&#8644; Move to page...</div>
  <div class="ctx-item" onclick="swapWith()">&#8646; Swap with page...</div>
  <div class="ctx-sep"></div>
  <div class="ctx-item" style="color:var(--accent)" onclick="removeImage()">&#10008; Remove image</div>
</div>

<div class="zoom-overlay" id="zoomOverlay" onclick="this.style.display='none'">
  <img id="zoomImg">
</div>

<script>
var DATA = ${dataJson};
var CHAPTERS = ${chapterJson};
var changes = [];
var ctxTarget = null; // { ch, pg }

function render() {
  var html = '';
  var currentCh = null;

  for (var i = 0; i < DATA.length; i++) {
    var d = DATA[i];
    if (d.ch !== currentCh) {
      if (currentCh !== null) html += '</div></div>';
      currentCh = d.ch;
      var chName = CHAPTERS[d.ch] ? CHAPTERS[d.ch].name : 'Chapter ' + d.ch;
      html += '<div class="chapter-section">';
      html += '<div class="chapter-title">Chapter ' + d.ch + ': ' + chName + '</div>';
      html += '<div class="page-grid">';
    }

    var hasImg = d.url && d.url.length > 0;
    var changed = d._changed;
    var removed = d._removed;
    var cls = 'page-card';
    if (changed) cls += ' changed';
    if (removed) cls += ' removed';

    html += '<div class="' + cls + '" data-idx="' + i + '">';
    html += '<div class="page-label"><strong>' + (d.pg === 0 ? 'Cover' : 'Page ' + d.pg) + '</strong><span>' + d.label + '</span></div>';
    html += '<div class="img-wrap" onclick="zoomImage(' + i + ')" oncontextmenu="showCtx(event,' + i + ')">';
    if (hasImg && !removed) {
      html += '<img src="' + d.url + '" loading="lazy">';
      if (changed) html += '<div class="badge-moved">MOVED</div>';
    } else if (removed) {
      html += '<div class="no-img">REMOVED</div>';
      html += '<div class="badge-removed">X</div>';
    } else {
      html += '<div class="no-img">No illustration</div>';
    }
    html += '</div>';
    if (hasImg && !removed) {
      html += '<div class="img-info">' + (d.info || '').substring(0, 60) + '</div>';
    }
    var textPreview = d.pg === 0 ? '[Cover]' : (CHAPTERS[d.ch]?.pages?.[d.pg] || d.text || '');
    html += '<div class="text-preview">' + textPreview.substring(0, 120) + '</div>';
    html += '</div>';
  }
  if (currentCh !== null) html += '</div></div>';
  document.getElementById('content').innerHTML = html;
  document.getElementById('changesCount').textContent = changes.length + ' changes';
}

function showCtx(e, idx) {
  e.preventDefault();
  var d = DATA[idx];
  if (!d.url && !d._removed) return;
  ctxTarget = idx;
  var menu = document.getElementById('ctxMenu');
  menu.style.display = 'block';
  menu.style.left = e.clientX + 'px';
  menu.style.top = e.clientY + 'px';
}

document.addEventListener('click', function() {
  document.getElementById('ctxMenu').style.display = 'none';
});

function promptMoveTo() {
  if (ctxTarget === null) return;
  var d = DATA[ctxTarget];
  var input = prompt('Move this image to which page? (chapter ' + d.ch + ', current: ' + (d.pg === 0 ? 'cover' : 'page ' + d.pg) + ')\\n\\nEnter page number (or 0 for cover):');
  if (input === null) return;
  var targetPg = parseInt(input);
  if (isNaN(targetPg)) return;

  // Find the target slot
  var targetIdx = DATA.findIndex(function(x) { return x.ch === d.ch && x.pg === targetPg; });
  if (targetIdx === -1) { alert('Page ' + targetPg + ' not found in chapter ' + d.ch); return; }

  // Save change
  changes.push({ type: 'move', from: { ch: d.ch, pg: d.pg, idx: ctxTarget }, to: { ch: d.ch, pg: targetPg, idx: targetIdx }, prevUrl: DATA[targetIdx].url, prevInfo: DATA[targetIdx].info });

  // Move: put this image on target, clear source
  var srcUrl = d.url;
  var srcInfo = d.info;
  DATA[targetIdx].url = srcUrl;
  DATA[targetIdx].info = srcInfo;
  DATA[targetIdx]._changed = true;
  DATA[ctxTarget].url = '';
  DATA[ctxTarget].info = 'text-only';
  DATA[ctxTarget]._changed = true;

  render();
}

function swapWith() {
  if (ctxTarget === null) return;
  var d = DATA[ctxTarget];
  var input = prompt('Swap this image with which page? (chapter ' + d.ch + ', current: ' + (d.pg === 0 ? 'cover' : 'page ' + d.pg) + ')\\n\\nEnter page number:');
  if (input === null) return;
  var targetPg = parseInt(input);
  if (isNaN(targetPg)) return;

  var targetIdx = DATA.findIndex(function(x) { return x.ch === d.ch && x.pg === targetPg; });
  if (targetIdx === -1) { alert('Page ' + targetPg + ' not found in chapter ' + d.ch); return; }

  changes.push({ type: 'swap', a: { ch: d.ch, pg: d.pg, idx: ctxTarget, url: d.url, info: d.info }, b: { ch: d.ch, pg: targetPg, idx: targetIdx, url: DATA[targetIdx].url, info: DATA[targetIdx].info } });

  // Swap
  var tmpUrl = d.url, tmpInfo = d.info;
  DATA[ctxTarget].url = DATA[targetIdx].url;
  DATA[ctxTarget].info = DATA[targetIdx].info;
  DATA[targetIdx].url = tmpUrl;
  DATA[targetIdx].info = tmpInfo;
  DATA[ctxTarget]._changed = true;
  DATA[targetIdx]._changed = true;

  render();
}

function removeImage() {
  if (ctxTarget === null) return;
  var d = DATA[ctxTarget];
  changes.push({ type: 'remove', idx: ctxTarget, url: d.url, info: d.info });
  DATA[ctxTarget]._removed = true;
  DATA[ctxTarget]._prevUrl = d.url;
  DATA[ctxTarget]._prevInfo = d.info;
  DATA[ctxTarget].url = '';
  DATA[ctxTarget].info = 'text-only';
  render();
}

function undoLast() {
  if (changes.length === 0) return;
  var c = changes.pop();
  if (c.type === 'remove') {
    DATA[c.idx].url = c.url;
    DATA[c.idx].info = c.info;
    delete DATA[c.idx]._removed;
    delete DATA[c.idx]._changed;
  } else if (c.type === 'move') {
    DATA[c.from.idx].url = DATA[c.to.idx].url;
    DATA[c.from.idx].info = DATA[c.to.idx].info;
    DATA[c.to.idx].url = c.prevUrl;
    DATA[c.to.idx].info = c.prevInfo;
    delete DATA[c.from.idx]._changed;
    delete DATA[c.to.idx]._changed;
  } else if (c.type === 'swap') {
    DATA[c.a.idx].url = c.a.url;
    DATA[c.a.idx].info = c.a.info;
    DATA[c.b.idx].url = c.b.url;
    DATA[c.b.idx].info = c.b.info;
    delete DATA[c.a.idx]._changed;
    delete DATA[c.b.idx]._changed;
  }
  render();
}

function zoomImage(idx) {
  var d = DATA[idx];
  if (!d.url || d._removed) return;
  document.getElementById('zoomImg').src = d.url;
  document.getElementById('zoomOverlay').style.display = 'flex';
}

function exportCSV() {
  var lines = ['chapter,page,image_url,image_info'];
  for (var i = 0; i < DATA.length; i++) {
    var d = DATA[i];
    var url = d._removed ? '' : d.url;
    var info = d._removed ? 'text-only' : (d.info || 'text-only');
    lines.push(d.ch + ',' + d.pg + ',"' + url + '","' + info.replace(/"/g, '""') + '"');
  }
  var csv = lines.join('\\n');
  var blob = new Blob([csv], { type: 'text/csv' });
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'illustration-assignments-edited.csv';
  a.click();
  URL.revokeObjectURL(a.href);
  alert('CSV exported with ' + changes.length + ' changes. Give this file to Claude Code to update the booklets.');
}

render();
</script>
</body>
</html>`;

writeFileSync(outputPath, html);
console.log('Editor written:', outputPath);
console.log(assignments.length, 'entries loaded');
