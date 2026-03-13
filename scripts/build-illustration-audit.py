#!/usr/bin/env python3
"""
Build an interactive HTML audit tool for Alice in Wonderland illustration pairings.

Reads:
  - grammars/alice-in-wonderland-chapter-book/grammar.json
  - grammars/alice-in-wonderland-chapter-book/image-descriptions.json

Outputs:
  - grammars/alice-in-wonderland-chapter-book/illustration-audit.html (interactive browser tool)
  - grammars/alice-in-wonderland-chapter-book/illustration-audit.json (machine-readable catalog)
"""

import json
import html
import os
import re

GRAMMAR_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "alice-in-wonderland-chapter-book")
GRAMMAR_PATH = os.path.join(GRAMMAR_DIR, "grammar.json")
DESCRIPTIONS_PATH = os.path.join(GRAMMAR_DIR, "image-descriptions.json")
OUTPUT_HTML = os.path.join(GRAMMAR_DIR, "illustration-audit.html")
OUTPUT_JSON = os.path.join(GRAMMAR_DIR, "illustration-audit.json")


def load_data():
    with open(GRAMMAR_PATH, "r") as f:
        grammar = json.load(f)

    # Load vision descriptions keyed by filename
    descriptions_by_file = {}
    try:
        with open(DESCRIPTIONS_PATH, "r") as f:
            descriptions = json.load(f)
        for d in descriptions:
            descriptions_by_file[d["file"]] = d.get("description", "")
    except FileNotFoundError:
        pass

    return grammar, descriptions_by_file


def extract_text_excerpt(item, max_len=300):
    """Get the original text excerpt from an item."""
    sections = item.get("sections", {})
    # Prefer "Story (Original Text)", then any section with "Original" or "Story"
    for key in ["Story (Original Text)", "Original Text", "Story", "Verse"]:
        if key in sections:
            text = sections[key]
            if len(text) > max_len:
                return text[:max_len] + "..."
            return text
    # Fallback: first section
    for key, val in sections.items():
        if isinstance(val, str) and len(val) > 20:
            text = val
            if len(text) > max_len:
                return text[:max_len] + "..."
            return text
    return "(no text)"


def get_vision_description(filename, descriptions_by_file):
    """Look up vision description for an image filename."""
    if filename in descriptions_by_file:
        raw = descriptions_by_file[filename]
        try:
            parsed = json.loads(raw) if isinstance(raw, str) else raw
            parts = []
            if parsed.get("scene"):
                parts.append(f"Scene: {parsed['scene']}")
            if parsed.get("visible_text"):
                parts.append(f"Visible text: {parsed['visible_text']}")
            return "\n".join(parts)
        except (json.JSONDecodeError, TypeError):
            return str(raw)
    return ""


def flag_mismatch(illustration, item, vision_desc):
    """Heuristic check: does this illustration belong with this text passage?"""
    reasons = []
    scene = (illustration.get("scene") or "").lower()
    item_name = item.get("name", "").lower()
    item_id = item.get("id", "").lower()
    text = extract_text_excerpt(item, 1000).lower()

    # Check if scene description mentions something clearly from a different chapter
    chapter_num = item.get("metadata", {}).get("chapter_number", 0)

    # Dedication/title page on a scene item
    if any(kw in scene for kw in ["dedication", "christmas gift", "title page", "frontispiece"]):
        if "chapter" not in item_id.replace("chapter-", ""):
            reasons.append(f"Dedication/title page assigned to scene item '{item['name']}'")

    # Scene describes action from different chapter
    scene_keywords = {
        "marmalade": "falling-down",
        "fell down": "falling-down",
        "falling": "falling-down",
        "drink me": "drink-me",
        "eat me": "eat-me",
        "pool of tears": "pool-of-tears",
        "caucus": "caucus-race",
        "caterpillar": "ch05",
        "mushroom": "mushroom",
        "cheshire cat": "cheshire",
        "duchess": "duchess",
        "tea party": "ch07",
        "mad hatter": "ch07",
        "croquet": "ch08",
        "flamingo": "ch08",
        "mock turtle": "ch09",
        "lobster": "ch10",
        "trial": "ch11",
        "court": "ch11",
        "jury": "ch12",
        "cards flying": "waking-up",
    }

    for keyword, expected_id_fragment in scene_keywords.items():
        if keyword in scene and expected_id_fragment not in item_id:
            # Check if it's plausibly correct despite the keyword
            if keyword not in text:
                reasons.append(f"Scene mentions '{keyword}' but item is '{item['name']}' ({item_id})")

    # Vision description mentions specific text that doesn't match
    if vision_desc:
        vision_lower = vision_desc.lower()
        for keyword, expected_id_fragment in scene_keywords.items():
            if keyword in vision_lower and expected_id_fragment not in item_id:
                if keyword not in text:
                    reasons.append(f"Vision desc mentions '{keyword}' but assigned to '{item_id}'")

    return reasons


def build_catalog(grammar, descriptions_by_file):
    """Build the full audit catalog."""
    items_by_id = {item["id"]: item for item in grammar["items"]}
    all_item_ids = [item["id"] for item in grammar["items"]]

    catalog = []
    entry_id = 0

    for item in grammar["items"]:
        illustrations = item.get("metadata", {}).get("illustrations", [])
        text_excerpt = extract_text_excerpt(item)

        for illust in illustrations:
            url = illust.get("url", "")
            filename = item.get("metadata", {}).get("image_filename", "")

            # Try to find vision description
            vision_desc = get_vision_description(filename, descriptions_by_file)

            # Also try matching by URL filename
            if not vision_desc:
                url_filename = url.rsplit("/", 1)[-1] if "/" in url else ""
                vision_desc = get_vision_description(url_filename, descriptions_by_file)

            mismatch_reasons = flag_mismatch(illust, item, vision_desc)

            entry = {
                "entry_id": entry_id,
                "illustration_url": url,
                "artist": illust.get("artist", "Unknown"),
                "artist_dates": illust.get("artist_dates", ""),
                "edition": illust.get("edition", ""),
                "scene_label": illust.get("scene", ""),
                "is_primary": illust.get("is_primary", False),
                "current_item_id": item["id"],
                "current_item_name": item["name"],
                "current_item_level": item.get("level", 1),
                "chapter_number": item.get("metadata", {}).get("chapter_number", 0),
                "text_excerpt": text_excerpt,
                "vision_description": vision_desc,
                "mismatch_flag": len(mismatch_reasons) > 0,
                "mismatch_reasons": mismatch_reasons,
                "status": "pending",  # pending | confirmed | reassigned | removed
                "reassign_to": None,  # user fills this
                "notes": ""
            }
            catalog.append(entry)
            entry_id += 1

    return catalog, all_item_ids


def build_html(catalog, all_item_ids, grammar):
    """Generate the interactive HTML audit page."""

    # Count stats
    total = len(catalog)
    flagged = sum(1 for e in catalog if e["mismatch_flag"])
    primary = sum(1 for e in catalog if e["is_primary"])

    catalog_json = json.dumps(catalog, indent=None)
    item_ids_json = json.dumps(all_item_ids)

    # Use %%PLACEHOLDER%% pattern to avoid f-string/JS conflicts
    html_template = open(os.path.join(os.path.dirname(__file__), "illustration-audit-template.html"), "r").read()
    html_content = html_template.replace("%%CATALOG_JSON%%", catalog_json)
    html_content = html_content.replace("%%ITEM_IDS_JSON%%", item_ids_json)
    html_content = html_content.replace("%%TOTAL%%", str(total))
    html_content = html_content.replace("%%FLAGGED%%", str(flagged))
    html_content = html_content.replace("%%PRIMARY%%", str(primary))

    return html_content


_DEAD = """
  --bg: #1a1a2e;
  --card: #16213e;
  --accent: #e94560;
  --ok: #4ecca3;
  --warn: #f5a623;
  --text: #eee;
  --muted: #888;
  --border: #333;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Georgia', serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}}
.header {{
  background: var(--card);
  padding: 20px 30px;
  border-bottom: 2px solid var(--accent);
  position: sticky;
  top: 0;
  z-index: 100;
}}
.header h1 {{ font-size: 1.4em; margin-bottom: 5px; }}
.stats {{ display: flex; gap: 20px; font-size: 0.9em; color: var(--muted); }}
.stats .flagged {{ color: var(--warn); font-weight: bold; }}
.stats .confirmed {{ color: var(--ok); }}
.controls {{
  display: flex;
  gap: 10px;
  margin-top: 10px;
  flex-wrap: wrap;
}}
.controls button {{
  padding: 6px 14px;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text);
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.85em;
}}
.controls button:hover {{ border-color: var(--accent); }}
.controls button.active {{ background: var(--accent); border-color: var(--accent); }}

.container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}

.entry {{
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 20px;
  background: var(--card);
  border: 2px solid var(--border);
  border-radius: 8px;
  margin-bottom: 16px;
  padding: 16px;
  transition: border-color 0.2s;
}}
.entry.flagged {{ border-color: var(--warn); }}
.entry.confirmed {{ border-color: var(--ok); opacity: 0.7; }}
.entry.reassigned {{ border-color: #9b59b6; }}
.entry.removed {{ border-color: var(--accent); opacity: 0.4; }}

.entry-img {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}
.entry-img img {{
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  border-radius: 4px;
  background: #111;
  cursor: pointer;
}}
.entry-img img.zoomed {{
  max-height: none;
  position: fixed;
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  object-fit: contain;
  background: rgba(0,0,0,0.95);
  border-radius: 0;
  padding: 20px;
}}
.img-meta {{
  font-size: 0.8em;
  color: var(--muted);
}}
.img-meta .artist {{ color: var(--text); font-weight: bold; }}
.img-meta .primary {{ color: var(--ok); font-weight: bold; }}

.entry-content {{ display: flex; flex-direction: column; gap: 12px; }}
.entry-header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
}}
.item-badge {{
  background: var(--bg);
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.85em;
  font-family: monospace;
  white-space: nowrap;
}}
.level-badge {{
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 0.75em;
  font-weight: bold;
}}
.level-badge.l1 {{ background: #2d5a27; }}
.level-badge.l2 {{ background: #5a2d27; }}

.scene-label {{
  font-style: italic;
  color: var(--warn);
  font-size: 0.9em;
  padding: 4px 8px;
  background: rgba(245, 166, 35, 0.1);
  border-radius: 4px;
}}
.text-passage {{
  background: var(--bg);
  padding: 12px 16px;
  border-radius: 6px;
  font-size: 0.9em;
  line-height: 1.7;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
  border-left: 3px solid var(--accent);
}}
.vision-desc {{
  background: rgba(78, 204, 163, 0.05);
  border-left: 3px solid var(--ok);
  padding: 8px 12px;
  font-size: 0.85em;
  border-radius: 4px;
  max-height: 120px;
  overflow-y: auto;
}}
.vision-desc summary {{
  cursor: pointer;
  color: var(--ok);
  font-weight: bold;
  font-size: 0.85em;
}}
.mismatch-reasons {{
  background: rgba(233, 69, 96, 0.1);
  border-left: 3px solid var(--accent);
  padding: 8px 12px;
  font-size: 0.85em;
  border-radius: 4px;
  color: var(--warn);
}}

.actions {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}}
.actions button {{
  padding: 5px 12px;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--text);
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.8em;
}}
.actions button:hover {{ opacity: 0.8; }}
.actions .btn-ok {{ border-color: var(--ok); color: var(--ok); }}
.actions .btn-ok.active {{ background: var(--ok); color: #000; }}
.actions .btn-wrong {{ border-color: var(--accent); color: var(--accent); }}
.actions .btn-wrong.active {{ background: var(--accent); color: #fff; }}
.actions .btn-reassign {{ border-color: #9b59b6; color: #9b59b6; }}
.actions .btn-reassign.active {{ background: #9b59b6; color: #fff; }}

.reassign-select {{
  padding: 4px 8px;
  background: var(--bg);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 0.8em;
  max-width: 300px;
}}
.notes-input {{
  padding: 4px 8px;
  background: var(--bg);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 0.8em;
  width: 100%;
  margin-top: 4px;
}}

.chapter-divider {{
  background: var(--accent);
  color: #fff;
  padding: 10px 20px;
  margin: 24px 0 12px;
  border-radius: 6px;
  font-size: 1.1em;
  font-weight: bold;
}}

.export-bar {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--card);
  border-top: 2px solid var(--accent);
  padding: 12px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
}}
.export-bar button {{
  padding: 8px 20px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  font-weight: bold;
}}
.export-bar button:hover {{ opacity: 0.9; }}

.hidden {{ display: none !important; }}
</style>
</head>
<body>

<div class="header">
  <h1>Alice in Wonderland — Illustration Audit</h1>
  <div class="stats">
    <span>Total: <strong id="stat-total">{total}</strong> illustrations</span>
    <span>Primary: <strong>{primary}</strong></span>
    <span class="flagged">Flagged: <strong id="stat-flagged">{flagged}</strong></span>
    <span class="confirmed">Confirmed: <strong id="stat-confirmed">0</strong></span>
    <span>Reassigned: <strong id="stat-reassigned">0</strong></span>
  </div>
  <div class="controls">
    <button onclick="filterView('all')" class="active" id="btn-all">Show All</button>
    <button onclick="filterView('flagged')" id="btn-flagged">Flagged Only</button>
    <button onclick="filterView('primary')" id="btn-primary">Primary Only</button>
    <button onclick="filterView('pending')" id="btn-pending">Pending</button>
    <button onclick="filterView('confirmed')" id="btn-confirmed">Confirmed</button>
    <button onclick="filterView('reassigned')" id="btn-reassigned">Reassigned</button>
  </div>
</div>

<div class="container" id="entries-container">
  <!-- entries rendered by JS -->
</div>

<div class="export-bar">
  <span id="progress-text">Click images to zoom. Mark each illustration as correct or wrong.</span>
  <div style="display:flex;gap:10px;">
    <button onclick="exportJSON()">Export Audit JSON</button>
    <button onclick="exportCorrectionsOnly()">Export Corrections Only</button>
  </div>
</div>

<script>
const catalog = {catalog_json};
const allItemIds = {item_ids_json};

// State
let currentFilter = 'all';

function getItemOptions() {{
  return allItemIds.map(id => `<option value="${{id}}">${{id}}</option>`).join('');
}}

function renderEntry(entry) {{
  const flagClass = entry.mismatch_flag ? 'flagged' : '';
  const statusClass = entry.status !== 'pending' ? entry.status : '';
  const levelClass = entry.current_item_level === 2 ? 'l2' : 'l1';
  const levelLabel = entry.current_item_level === 2 ? 'L2 Chapter' : 'L1 Scene';

  let mismatchHtml = '';
  if (entry.mismatch_reasons && entry.mismatch_reasons.length > 0) {{
    mismatchHtml = `<div class="mismatch-reasons">
      <strong>⚠ Potential mismatch:</strong><br>
      ${{entry.mismatch_reasons.map(r => `• ${{escapeHtml(r)}}`).join('<br>')}}
    </div>`;
  }}

  let visionHtml = '';
  if (entry.vision_description) {{
    visionHtml = `<details class="vision-desc">
      <summary>Vision Description</summary>
      <p>${{escapeHtml(entry.vision_description)}}</p>
    </details>`;
  }}

  const reassignSelectHtml = `
    <select class="reassign-select hidden" id="reassign-${{entry.entry_id}}" onchange="reassignEntry(${{entry.entry_id}}, this.value)">
      <option value="">-- Move to item --</option>
      ${{getItemOptions()}}
    </select>
  `;

  return `
    <div class="entry ${{flagClass}} ${{statusClass}}" id="entry-${{entry.entry_id}}"
         data-status="${{entry.status}}" data-flagged="${{entry.mismatch_flag}}"
         data-primary="${{entry.is_primary}}" data-chapter="${{entry.chapter_number}}">
      <div class="entry-img">
        <img src="${{entry.illustration_url}}" alt="${{escapeHtml(entry.scene_label)}}"
             loading="lazy" onclick="toggleZoom(this)"
             onerror="this.style.border='2px dashed red'; this.alt='FAILED TO LOAD'">
        <div class="img-meta">
          <span class="artist">${{escapeHtml(entry.artist)}}</span>
          ${{entry.artist_dates ? `<span>(${escapeHtml(entry.artist_dates)})</span>` : ''}}
          <br>${{escapeHtml(entry.edition)}}
          ${{entry.is_primary ? '<br><span class="primary">★ PRIMARY</span>' : ''}}
        </div>
      </div>
      <div class="entry-content">
        <div class="entry-header">
          <div>
            <span class="item-badge">${{escapeHtml(entry.current_item_id)}}</span>
            <span class="level-badge ${{levelClass}}">${{levelLabel}}</span>
            <br><strong>${{escapeHtml(entry.current_item_name)}}</strong>
            <span style="color:var(--muted);font-size:0.85em"> (Ch. ${{entry.chapter_number}})</span>
          </div>
          <span style="color:var(--muted);font-size:0.8em">#${{entry.entry_id}}</span>
        </div>
        <div class="scene-label">Scene label: "${{escapeHtml(entry.scene_label)}}"</div>
        <div class="text-passage">${{escapeHtml(entry.text_excerpt)}}</div>
        ${{visionHtml}}
        ${{mismatchHtml}}
        <div class="actions">
          <button class="btn-ok ${{entry.status === 'confirmed' ? 'active' : ''}}"
                  onclick="setStatus(${{entry.entry_id}}, 'confirmed')">✓ Correct</button>
          <button class="btn-wrong ${{entry.status === 'removed' ? 'active' : ''}}"
                  onclick="setStatus(${{entry.entry_id}}, 'removed')">✗ Wrong</button>
          <button class="btn-reassign ${{entry.status === 'reassigned' ? 'active' : ''}}"
                  onclick="showReassign(${{entry.entry_id}})">↷ Reassign</button>
          ${{reassignSelectHtml}}
          <input class="notes-input" placeholder="Notes..."
                 value="${{escapeHtml(entry.notes || '')}}"
                 onchange="setNotes(${{entry.entry_id}}, this.value)">
        </div>
      </div>
    </div>
  `;
}}

function escapeHtml(str) {{
  if (!str) return '';
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function renderAll() {{
  const container = document.getElementById('entries-container');
  let html = '';
  let lastChapter = -1;

  for (const entry of catalog) {{
    if (entry.chapter_number !== lastChapter) {{
      lastChapter = entry.chapter_number;
      html += `<div class="chapter-divider">Chapter ${{lastChapter}}</div>`;
    }}
    html += renderEntry(entry);
  }}
  container.innerHTML = html;
  applyFilter();
}}

function toggleZoom(img) {{
  img.classList.toggle('zoomed');
}}

function setStatus(entryId, status) {{
  const entry = catalog.find(e => e.entry_id === entryId);
  if (!entry) return;
  entry.status = entry.status === status ? 'pending' : status;
  const el = document.getElementById(`entry-${{entryId}}`);
  el.className = `entry ${{entry.mismatch_flag ? 'flagged' : ''}} ${{entry.status !== 'pending' ? entry.status : ''}}`;
  el.dataset.status = entry.status;
  // Update button states
  el.querySelector('.btn-ok').classList.toggle('active', entry.status === 'confirmed');
  el.querySelector('.btn-wrong').classList.toggle('active', entry.status === 'removed');
  el.querySelector('.btn-reassign').classList.toggle('active', entry.status === 'reassigned');
  updateStats();
}}

function showReassign(entryId) {{
  const select = document.getElementById(`reassign-${{entryId}}`);
  select.classList.toggle('hidden');
  if (!select.classList.contains('hidden')) {{
    setStatus(entryId, 'reassigned');
  }}
}}

function reassignEntry(entryId, newItemId) {{
  const entry = catalog.find(e => e.entry_id === entryId);
  if (entry) {{
    entry.reassign_to = newItemId || null;
    entry.status = newItemId ? 'reassigned' : 'pending';
  }}
  updateStats();
}}

function setNotes(entryId, notes) {{
  const entry = catalog.find(e => e.entry_id === entryId);
  if (entry) entry.notes = notes;
}}

function filterView(filter) {{
  currentFilter = filter;
  document.querySelectorAll('.controls button').forEach(b => b.classList.remove('active'));
  document.getElementById(`btn-${{filter}}`).classList.add('active');
  applyFilter();
}}

function applyFilter() {{
  document.querySelectorAll('.entry').forEach(el => {{
    const status = el.dataset.status;
    const flagged = el.dataset.flagged === 'true';
    const primary = el.dataset.primary === 'true';
    let show = true;
    switch(currentFilter) {{
      case 'flagged': show = flagged; break;
      case 'primary': show = primary; break;
      case 'pending': show = status === 'pending'; break;
      case 'confirmed': show = status === 'confirmed'; break;
      case 'reassigned': show = status === 'reassigned'; break;
    }}
    el.style.display = show ? '' : 'none';
  }});
}}

function updateStats() {{
  const confirmed = catalog.filter(e => e.status === 'confirmed').length;
  const reassigned = catalog.filter(e => e.status === 'reassigned').length;
  const flagged = catalog.filter(e => e.mismatch_flag && e.status === 'pending').length;
  document.getElementById('stat-confirmed').textContent = confirmed;
  document.getElementById('stat-reassigned').textContent = reassigned;
  document.getElementById('stat-flagged').textContent = flagged;
  document.getElementById('progress-text').textContent =
    `${{confirmed + reassigned}} / ${{catalog.length}} reviewed`;
}}

function exportJSON() {{
  const blob = new Blob([JSON.stringify(catalog, null, 2)], {{type: 'application/json'}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'illustration-audit-results.json';
  a.click();
  URL.revokeObjectURL(url);
}}

function exportCorrectionsOnly() {{
  const corrections = catalog.filter(e => e.status !== 'pending');
  const blob = new Blob([JSON.stringify(corrections, null, 2)], {{type: 'application/json'}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'illustration-corrections.json';
  a.click();
  URL.revokeObjectURL(url);
}}

// Init
document.addEventListener('DOMContentLoaded', () => {{
  renderAll();
  updateStats();
}});

// Keyboard nav
document.addEventListener('keydown', (e) => {{
  if (e.key === 'Escape') {{
    document.querySelectorAll('.zoomed').forEach(img => img.classList.remove('zoomed'));
  }}
}});
</script>

</body>
</html>"""


def main():
    print("Loading grammar and image descriptions...")
    grammar, descriptions_by_file = load_data()

    print(f"Found {len(grammar['items'])} items, {len(descriptions_by_file)} image descriptions")

    print("Building audit catalog...")
    catalog, all_item_ids = build_catalog(grammar, descriptions_by_file)

    flagged = sum(1 for e in catalog if e["mismatch_flag"])
    print(f"Catalog: {len(catalog)} illustration entries, {flagged} flagged as potential mismatches")

    # Write JSON catalog
    with open(OUTPUT_JSON, "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"Written: {OUTPUT_JSON}")

    # Write HTML audit tool
    print("Generating HTML audit tool...")
    html_content = build_html(catalog, all_item_ids, grammar)
    with open(OUTPUT_HTML, "w") as f:
        f.write(html_content)
    print(f"Written: {OUTPUT_HTML}")

    print(f"\nDone! Open {OUTPUT_HTML} in your browser to audit illustrations.")
    print(f"Flagged {flagged} potential mismatches for your review.")


if __name__ == "__main__":
    main()
