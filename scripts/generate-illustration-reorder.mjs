/**
 * Generate the illustration reorder tool — a keyboard-driven HTML page
 * for reassigning illustrations to booklet pages.
 *
 * Usage:
 *   node scripts/generate-illustration-reorder.mjs
 *
 * Output: grammars/alice-5-minute-stories/booklets/reorder-tool.html
 *
 * Then open http://localhost:3456/booklets/reorder-tool.html (with npx serve running)
 */

import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Load data ──────────────────────────────────────────────────────────

const grammarPath = resolve(__dirname, '../grammars/alice-in-wonderland-chapter-book/grammar.json');
const assignmentsPath = resolve(__dirname, '../grammars/alice-5-minute-stories/illustration-assignments.json');
const outputPath = resolve(__dirname, '../grammars/alice-5-minute-stories/booklets/reorder-tool.html');

const grammar = JSON.parse(readFileSync(grammarPath, 'utf8'));
const assignments = JSON.parse(readFileSync(assignmentsPath, 'utf8'));

// ── Extract all illustrations from grammar ─────────────────────────────

const allIllustrations = [];
const sceneMap = {};

for (const item of grammar.items) {
  sceneMap[item.id] = {
    name: item.name,
    chapter: item.metadata.chapter_number,
    scene_number: item.metadata.scene_number || 0,
    level: item.level,
  };

  for (const ill of (item.metadata?.illustrations || [])) {
    allIllustrations.push({
      url: ill.url,
      artist: ill.artist || 'Unknown',
      edition: ill.edition || '',
      scene: ill.scene || '',
      is_primary: !!ill.is_primary,
      item_id: item.id,
      chapter: item.metadata.chapter_number,
      item_name: item.name,
    });
  }
}

console.log(`Loaded ${allIllustrations.length} illustrations from ${Object.keys(sceneMap).length} scenes`);
console.log(`Loaded ${assignments.length} page assignments`);

// ── Compute scene_ids for each page assignment ─────────────────────────
// Map each page to the scenes whose items match that chapter

// Build chapter → ordered scene IDs
const chapterScenes = {};
for (const item of grammar.items.filter(i => i.level === 1)) {
  const ch = item.metadata.chapter_number;
  if (!chapterScenes[ch]) chapterScenes[ch] = [];
  chapterScenes[ch].push(item.id);
}

// For each assignment, find matching scene based on image URL
const enhancedAssignments = assignments.map(a => {
  const matchingIlls = allIllustrations.filter(ill => ill.url === a.image_url);
  const scene_ids = matchingIlls.length > 0
    ? [matchingIlls[0].item_id]
    : (chapterScenes[a.chapter] || []);
  return { ...a, scene_ids };
});

// ── Generate HTML ──────────────────────────────────────────────────────

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Illustration Reorder Tool — Alice in Wonderland</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Georgia', serif;
    background: #1a0f08;
    color: #f0e6d6;
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  /* Header */
  .header {
    background: #2c1810;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid #5a4030;
    flex-shrink: 0;
  }
  .header h1 { font-size: 14px; color: #d4a76a; letter-spacing: 1px; }
  .header .change-count { font-size: 12px; color: #a08060; }
  .header .change-count.unsaved { color: #ff9040; }
  .header button {
    padding: 4px 12px;
    border: 1px solid #d4a76a;
    border-radius: 4px;
    background: #1a0f08;
    color: #d4a76a;
    font-size: 11px;
    cursor: pointer;
    font-family: 'Georgia', serif;
  }
  .header button:hover { background: #3c2820; }
  .header .spacer { flex: 1; }

  /* Main layout */
  .main {
    display: flex;
    flex: 1;
    overflow: hidden;
  }

  /* Left panel: pages */
  .page-panel {
    width: 340px;
    border-right: 1px solid #5a4030;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
  }
  .page-panel-header {
    padding: 8px 12px;
    background: #2c1810;
    border-bottom: 1px solid #3a2518;
    font-size: 11px;
    letter-spacing: 1px;
    color: #a08060;
  }
  .page-list {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
  }

  /* Chapter divider */
  .chapter-divider {
    padding: 6px 12px;
    background: #2c1810;
    font-size: 11px;
    letter-spacing: 2px;
    color: #d4a76a;
    border-bottom: 1px solid #3a2518;
    position: sticky;
    top: 0;
    z-index: 5;
  }

  /* Page row */
  .page-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 12px;
    border-bottom: 1px solid #2c1810;
    cursor: pointer;
    transition: background 0.15s;
  }
  .page-row:hover { background: #2c1810; }
  .page-row.active {
    background: #3c2820;
    border-left: 3px solid #d4a76a;
    padding-left: 9px;
  }
  .page-row.focused {
    outline: 2px solid #d4a76a;
    outline-offset: -2px;
  }
  .page-thumb {
    width: 50px;
    height: 38px;
    object-fit: cover;
    border-radius: 3px;
    background: #2c1810;
    flex-shrink: 0;
  }
  .page-thumb-empty {
    width: 50px;
    height: 38px;
    border-radius: 3px;
    background: #2c1810;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: #5a4030;
    flex-shrink: 0;
  }
  .page-info {
    flex: 1;
    min-width: 0;
  }
  .page-label {
    font-size: 11px;
    color: #d4a76a;
    font-weight: bold;
  }
  .page-preview {
    font-size: 10px;
    color: #8a7060;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Right panel: carousel */
  .carousel-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .carousel-header {
    padding: 8px 12px;
    background: #2c1810;
    border-bottom: 1px solid #3a2518;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }
  .carousel-header .title {
    font-size: 11px;
    letter-spacing: 1px;
    color: #a08060;
  }
  .carousel-header input {
    flex: 1;
    padding: 4px 8px;
    border: 1px solid #5a4030;
    border-radius: 4px;
    background: #1a0f08;
    color: #f0e6d6;
    font-size: 12px;
    font-family: 'Georgia', serif;
  }
  .carousel-header input::placeholder { color: #5a4030; }

  /* Preview area */
  .preview-area {
    height: 180px;
    display: flex;
    gap: 2px;
    padding: 8px 12px;
    background: #0f0a06;
    border-bottom: 1px solid #3a2518;
    flex-shrink: 0;
  }
  .preview-left {
    width: 50%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8f5f0;
    border-radius: 4px 0 0 4px;
    overflow: hidden;
  }
  .preview-left img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
  .preview-right {
    width: 50%;
    height: 100%;
    background: white;
    border-radius: 0 4px 4px 0;
    padding: 12px;
    overflow: hidden;
    color: #1a1a1a;
    font-size: 11px;
    line-height: 1.5;
  }

  /* Illustration grid */
  .ill-grid {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 8px;
    align-content: start;
  }

  .ill-card {
    border: 2px solid transparent;
    border-radius: 6px;
    overflow: hidden;
    cursor: pointer;
    transition: border-color 0.15s, transform 0.15s;
    background: #2c1810;
  }
  .ill-card:hover { border-color: #5a4030; }
  .ill-card.selected {
    border-color: #d4a76a;
    transform: scale(1.03);
    box-shadow: 0 0 12px rgba(212,167,106,0.3);
  }
  .ill-card.scene-match { background: #3a2518; }
  .ill-card.chapter-match { background: #2a1e14; }
  .ill-card.assigned {
    opacity: 0.5;
  }
  .ill-card img {
    width: 100%;
    height: 90px;
    object-fit: cover;
  }
  .ill-caption {
    padding: 4px 6px;
    font-size: 9px;
    color: #a08060;
    line-height: 1.3;
  }
  .ill-artist { color: #d4a76a; font-weight: bold; }
  .ill-scene { color: #8a7060; }
  .ill-badge {
    display: inline-block;
    padding: 1px 4px;
    border-radius: 2px;
    font-size: 8px;
    margin-top: 2px;
  }
  .ill-badge.primary { background: #d4a76a; color: #1a0f08; }
  .ill-badge.match { background: #4a8; color: #fff; }

  /* Footer / status bar */
  .footer {
    background: #2c1810;
    padding: 6px 16px;
    border-top: 1px solid #5a4030;
    font-size: 10px;
    color: #8a7060;
    display: flex;
    gap: 16px;
    flex-shrink: 0;
  }
  .footer kbd {
    background: #1a0f08;
    padding: 1px 4px;
    border: 1px solid #5a4030;
    border-radius: 2px;
    font-family: monospace;
    font-size: 10px;
    color: #d4a76a;
  }

  /* Focus indicator on panels */
  .page-panel.has-focus { border-right-color: #d4a76a; }
  .carousel-panel.has-focus .carousel-header { border-bottom-color: #d4a76a; }
</style>
</head>
<body>

<div class="header">
  <h1>ILLUSTRATION REORDER — ALICE IN WONDERLAND</h1>
  <span class="spacer"></span>
  <span class="change-count" id="changeCount">No changes</span>
  <button id="saveBtn" title="Ctrl+S">💾 Save JSON</button>
  <button id="helpBtn">? Help</button>
</div>

<div class="main">
  <div class="page-panel" id="pagePanel">
    <div class="page-panel-header">PAGES (↑↓ navigate, 1-9 jump chapter)</div>
    <div class="page-list" id="pageList"></div>
  </div>

  <div class="carousel-panel" id="carouselPanel">
    <div class="carousel-header">
      <span class="title">ILLUSTRATIONS</span>
      <input type="text" id="searchInput" placeholder="/ to search by artist or scene..." autocomplete="off">
    </div>
    <div class="preview-area" id="previewArea">
      <div class="preview-left" id="previewLeft">
        <span style="color:#5a4030">No illustration</span>
      </div>
      <div class="preview-right" id="previewRight">
        Select a page to preview
      </div>
    </div>
    <div class="ill-grid" id="illGrid"></div>
  </div>
</div>

<div class="footer">
  <span><kbd>↑</kbd><kbd>↓</kbd> pages</span>
  <span><kbd>Tab</kbd> switch panel</span>
  <span><kbd>←</kbd><kbd>→</kbd><kbd>↑</kbd><kbd>↓</kbd> browse</span>
  <span><kbd>Enter</kbd> assign</span>
  <span><kbd>Del</kbd> remove</span>
  <span><kbd>/</kbd> search</span>
  <span><kbd>Ctrl+S</kbd> save</span>
  <span><kbd>1-9</kbd> chapter</span>
</div>

<script>
// ── Embedded data ──
var PAGES = ${JSON.stringify(enhancedAssignments)};
var ILLUSTRATIONS = ${JSON.stringify(allIllustrations)};
var SCENE_MAP = ${JSON.stringify(sceneMap)};

// ── State ──
var state = {
  pageIdx: 0,
  illIdx: 0,
  focus: 'pages', // 'pages' or 'carousel'
  changes: 0,
  search: ''
};

var filteredIlls = [];
var usedUrls = new Set();

// Track which URLs are currently assigned
function updateUsedUrls() {
  usedUrls = new Set();
  PAGES.forEach(function(p) {
    if (p.image_url) usedUrls.add(p.image_url);
  });
}
updateUsedUrls();

// ── Sort illustrations by relevance to current page ──
function sortIllustrations() {
  var page = PAGES[state.pageIdx];
  var sceneIds = page.scene_ids || [];
  var ch = page.chapter;

  var pool = ILLUSTRATIONS.slice();

  // Apply search filter
  if (state.search) {
    var q = state.search.toLowerCase();
    pool = pool.filter(function(ill) {
      return (ill.artist || '').toLowerCase().indexOf(q) >= 0 ||
             (ill.scene || '').toLowerCase().indexOf(q) >= 0 ||
             (ill.item_name || '').toLowerCase().indexOf(q) >= 0 ||
             (ill.edition || '').toLowerCase().indexOf(q) >= 0;
    });
  }

  pool.sort(function(a, b) {
    // Same scene first
    var aScene = sceneIds.indexOf(a.item_id) >= 0 ? 0 : 1;
    var bScene = sceneIds.indexOf(b.item_id) >= 0 ? 0 : 1;
    if (aScene !== bScene) return aScene - bScene;

    // Same chapter second
    var aCh = a.chapter === ch ? 0 : 1;
    var bCh = b.chapter === ch ? 0 : 1;
    if (aCh !== bCh) return aCh - bCh;

    // Primary first
    if (a.is_primary !== b.is_primary) return a.is_primary ? -1 : 1;

    // Then by chapter number
    return a.chapter - b.chapter;
  });

  filteredIlls = pool;
}

// ── Rendering ──

function renderPageList() {
  var list = document.getElementById('pageList');
  var html = '';
  var lastCh = -1;

  PAGES.forEach(function(p, i) {
    if (p.chapter !== lastCh) {
      lastCh = p.chapter;
      html += '<div class="chapter-divider">CHAPTER ' + p.chapter + '</div>';
    }
    var isActive = i === state.pageIdx;
    var isFocused = isActive && state.focus === 'pages';
    var cls = 'page-row' + (isActive ? ' active' : '') + (isFocused ? ' focused' : '');

    var thumb = p.image_url
      ? '<img class="page-thumb" src="' + p.image_url + '" loading="lazy">'
      : '<div class="page-thumb-empty">—</div>';

    html += '<div class="' + cls + '" data-idx="' + i + '">' +
      thumb +
      '<div class="page-info">' +
        '<div class="page-label">' + p.label + '</div>' +
        '<div class="page-preview">' + (p.text_preview || '') + '</div>' +
      '</div></div>';
  });

  list.innerHTML = html;

  // Scroll active into view
  var activeEl = list.querySelector('.page-row.active');
  if (activeEl) {
    activeEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  // Click handlers
  list.querySelectorAll('.page-row').forEach(function(row) {
    row.addEventListener('click', function() {
      state.pageIdx = parseInt(row.dataset.idx);
      state.focus = 'pages';
      render();
    });
  });
}

function renderCarousel() {
  sortIllustrations();
  var grid = document.getElementById('illGrid');
  var page = PAGES[state.pageIdx];
  var sceneIds = page.scene_ids || [];

  var html = '';
  filteredIlls.forEach(function(ill, i) {
    var isSelected = i === state.illIdx && state.focus === 'carousel';
    var isSceneMatch = sceneIds.indexOf(ill.item_id) >= 0;
    var isChapterMatch = ill.chapter === page.chapter;
    var isAssigned = usedUrls.has(ill.url) && ill.url !== page.image_url;

    var cls = 'ill-card' +
      (isSelected ? ' selected' : '') +
      (isSceneMatch ? ' scene-match' : (isChapterMatch ? ' chapter-match' : '')) +
      (isAssigned ? ' assigned' : '');

    var badges = '';
    if (ill.is_primary) badges += '<span class="ill-badge primary">★</span> ';
    if (isSceneMatch) badges += '<span class="ill-badge match">scene</span> ';

    html += '<div class="' + cls + '" data-idx="' + i + '">' +
      '<img src="' + ill.url + '" loading="lazy" alt="">' +
      '<div class="ill-caption">' +
        '<div class="ill-artist">' + ill.artist + '</div>' +
        '<div class="ill-scene">' + (ill.scene || ill.item_name || '').substring(0, 50) + '</div>' +
        badges +
      '</div></div>';
  });

  grid.innerHTML = html;

  // Scroll selected into view
  var selectedEl = grid.querySelector('.ill-card.selected');
  if (selectedEl) {
    selectedEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  // Click handlers
  grid.querySelectorAll('.ill-card').forEach(function(card) {
    card.addEventListener('click', function() {
      state.illIdx = parseInt(card.dataset.idx);
      state.focus = 'carousel';
      render();
    });
    card.addEventListener('dblclick', function() {
      state.illIdx = parseInt(card.dataset.idx);
      assignIllustration();
    });
  });
}

function renderPreview() {
  var page = PAGES[state.pageIdx];
  var previewLeft = document.getElementById('previewLeft');
  var previewRight = document.getElementById('previewRight');

  if (page.image_url) {
    previewLeft.innerHTML = '<img src="' + page.image_url + '">';
  } else {
    previewLeft.innerHTML = '<span style="color:#5a4030;font-size:24px">—</span>';
  }

  previewRight.innerHTML =
    '<div style="font-weight:bold;color:#2c1810;margin-bottom:6px">' + page.label + '</div>' +
    '<div style="color:#333">' + (page.text_preview || 'No text') + '</div>' +
    '<div style="margin-top:8px;font-size:9px;color:#999">' + (page.image_info || 'No illustration assigned') + '</div>';
}

function renderFocusIndicators() {
  var pp = document.getElementById('pagePanel');
  var cp = document.getElementById('carouselPanel');
  pp.classList.toggle('has-focus', state.focus === 'pages');
  cp.classList.toggle('has-focus', state.focus === 'carousel');
}

function renderChangeCount() {
  var el = document.getElementById('changeCount');
  if (state.changes === 0) {
    el.textContent = 'No changes';
    el.classList.remove('unsaved');
  } else {
    el.textContent = state.changes + ' unsaved change' + (state.changes !== 1 ? 's' : '');
    el.classList.add('unsaved');
  }
}

function render() {
  renderPageList();
  renderCarousel();
  renderPreview();
  renderFocusIndicators();
  renderChangeCount();
}

// ── Actions ──

function assignIllustration() {
  if (state.illIdx < 0 || state.illIdx >= filteredIlls.length) return;
  var ill = filteredIlls[state.illIdx];
  var page = PAGES[state.pageIdx];
  page.image_url = ill.url;
  page.image_info = ill.artist + ' — ' + (ill.scene || ill.item_name || '');
  state.changes++;
  updateUsedUrls();
  render();
}

function removeIllustration() {
  var page = PAGES[state.pageIdx];
  if (!page.image_url) return;
  page.image_url = '';
  page.image_info = '';
  state.changes++;
  updateUsedUrls();
  render();
}

function downloadAssignments() {
  // Strip scene_ids (internal field) before saving
  var output = PAGES.map(function(p) {
    return {
      chapter: p.chapter,
      page: p.page,
      label: p.label,
      text_preview: p.text_preview,
      image_url: p.image_url,
      image_info: p.image_info
    };
  });
  var blob = new Blob([JSON.stringify(output, null, 2)], { type: 'application/json' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'illustration-assignments.json';
  a.click();
  URL.revokeObjectURL(url);
  state.changes = 0;
  renderChangeCount();
}

// ── Navigation ──

function navigatePage(delta) {
  state.pageIdx = Math.max(0, Math.min(PAGES.length - 1, state.pageIdx + delta));
  state.illIdx = 0; // reset carousel position when page changes
  render();
}

function navigateIll(delta) {
  state.illIdx = Math.max(0, Math.min(filteredIlls.length - 1, state.illIdx + delta));
  renderCarousel();
}

function jumpToChapter(ch) {
  for (var i = 0; i < PAGES.length; i++) {
    if (PAGES[i].chapter === ch) {
      state.pageIdx = i;
      state.illIdx = 0;
      render();
      return;
    }
  }
}

// ── Keyboard handler ──

var searchInput = document.getElementById('searchInput');

document.addEventListener('keydown', function(e) {
  // Don't intercept when search input is focused (except Escape and Tab)
  if (document.activeElement === searchInput) {
    if (e.key === 'Escape') {
      searchInput.blur();
      searchInput.value = '';
      state.search = '';
      state.illIdx = 0;
      render();
      return;
    }
    if (e.key === 'Tab') {
      e.preventDefault();
      searchInput.blur();
      state.focus = state.focus === 'pages' ? 'carousel' : 'pages';
      render();
      return;
    }
    return; // let typing happen normally
  }

  var cols = 3; // grid columns for Up/Down in carousel

  switch (e.key) {
    case 'ArrowUp':
      e.preventDefault();
      if (state.focus === 'pages') navigatePage(-1);
      else navigateIll(-cols);
      break;
    case 'ArrowDown':
      e.preventDefault();
      if (state.focus === 'pages') navigatePage(1);
      else navigateIll(cols);
      break;
    case 'ArrowLeft':
      e.preventDefault();
      if (state.focus === 'carousel') navigateIll(-1);
      break;
    case 'ArrowRight':
      e.preventDefault();
      if (state.focus === 'carousel') navigateIll(1);
      break;
    case 'Enter':
      e.preventDefault();
      if (state.focus === 'carousel') assignIllustration();
      break;
    case 'Delete':
    case 'Backspace':
      e.preventDefault();
      removeIllustration();
      break;
    case 'Tab':
      e.preventDefault();
      state.focus = state.focus === 'pages' ? 'carousel' : 'pages';
      render();
      break;
    case '/':
      e.preventDefault();
      searchInput.focus();
      break;
    case 's':
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        downloadAssignments();
      }
      break;
    default:
      // Number keys 1-9 jump to chapter (0 = ch 10)
      if (/^[1-9]$/.test(e.key) && state.focus === 'pages') {
        jumpToChapter(parseInt(e.key));
      }
      if (e.key === '0' && state.focus === 'pages') {
        jumpToChapter(10);
      }
      break;
  }
});

// Search input handler
searchInput.addEventListener('input', function() {
  state.search = searchInput.value.trim();
  state.illIdx = 0;
  renderCarousel();
});

// Save button
document.getElementById('saveBtn').addEventListener('click', downloadAssignments);

// Help button
document.getElementById('helpBtn').addEventListener('click', function() {
  alert(
    'Illustration Reorder Tool\\n\\n' +
    'KEYBOARD SHORTCUTS:\\n' +
    '↑/↓  Navigate pages (left panel) or rows (right panel)\\n' +
    '←/→  Browse illustrations in carousel\\n' +
    'Tab   Switch focus between panels\\n' +
    'Enter  Assign selected illustration to current page\\n' +
    'Del   Remove illustration from page\\n' +
    '/     Focus search (filter by artist/scene)\\n' +
    'Esc   Clear search\\n' +
    'Ctrl+S  Download updated assignments JSON\\n' +
    '1-9, 0  Jump to chapter 1-10\\n\\n' +
    'WORKFLOW:\\n' +
    '1. Navigate pages with ↑/↓\\n' +
    '2. Press Tab to switch to carousel\\n' +
    '3. Browse illustrations with arrow keys\\n' +
    '4. Press Enter to assign\\n' +
    '5. Press Ctrl+S to save\\n' +
    '6. Save file to grammars/alice-5-minute-stories/\\n' +
    '7. Run: node scripts/generate-alice-booklets.mjs --remap'
  );
});

// Unsaved changes warning
window.addEventListener('beforeunload', function(e) {
  if (state.changes > 0) {
    e.preventDefault();
    e.returnValue = '';
  }
});

// Initial render
render();
</script>
</body>
</html>`;

writeFileSync(outputPath, html);
console.log(`\nReorder tool generated: ${outputPath}`);
console.log(`Open: http://localhost:3456/booklets/reorder-tool.html`);
