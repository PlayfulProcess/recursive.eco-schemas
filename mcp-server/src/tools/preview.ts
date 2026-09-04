import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { writeFile } from "node:fs/promises";
import { resolve } from "node:path";

interface PreviewItem {
  title?: string;
  thumbnail_url?: string;
  full_url?: string;
  image_url?: string;
  artist?: string;
  date?: string;
  license?: string;
  description?: string;
  commons_url?: string;
  met_url?: string;
  // text results
  authors?: string[];
  gutenberg_url?: string;
  openlibrary_url?: string;
  // paper results
  abstract?: string;
  year?: number;
  venue?: string;
  pdf_url?: string;
  open_access_pdf?: string;
  arxiv_url?: string;
  semantic_scholar_url?: string;
}

function generatePreviewHTML(items: PreviewItem[], title: string): string {
  const hasImages = items.some((i) => i.thumbnail_url || i.image_url);

  const cards = items
    .map((item, idx) => {
      const imgUrl = item.thumbnail_url || item.image_url || "";
      const sourceUrl =
        item.commons_url || item.met_url || item.gutenberg_url || item.openlibrary_url || item.arxiv_url || item.semantic_scholar_url || "";
      const subtitle = [item.artist, item.date || item.year].filter(Boolean).join(" · ");
      const authors = item.authors?.join(", ") || "";

      if (hasImages) {
        return `
      <div class="card" data-index="${idx}">
        <div class="card-img" style="background-image: url('${imgUrl}')"></div>
        <div class="card-body">
          <h3>${item.title || "Untitled"}</h3>
          ${subtitle ? `<p class="subtitle">${subtitle}</p>` : ""}
          ${item.description ? `<p class="desc">${item.description}</p>` : ""}
          ${item.license ? `<span class="badge">${item.license}</span>` : ""}
          ${sourceUrl ? `<a href="${sourceUrl}" target="_blank">View source ↗</a>` : ""}
          ${imgUrl ? `<a href="${item.full_url || imgUrl}" target="_blank">Full image ↗</a>` : ""}
        </div>
      </div>`;
      } else {
        return `
      <div class="card text-card" data-index="${idx}">
        <div class="card-body">
          <h3>${item.title || "Untitled"}</h3>
          ${authors ? `<p class="authors">${authors}</p>` : ""}
          ${subtitle ? `<p class="subtitle">${subtitle}</p>` : ""}
          ${item.abstract || item.description ? `<p class="desc">${item.abstract || item.description}</p>` : ""}
          <div class="links">
            ${item.pdf_url || item.open_access_pdf ? `<a href="${item.pdf_url || item.open_access_pdf}" target="_blank">PDF ↗</a>` : ""}
            ${sourceUrl ? `<a href="${sourceUrl}" target="_blank">View ↗</a>` : ""}
          </div>
        </div>
      </div>`;
      }
    })
    .join("\n");

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} — recursive.eco preview</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; padding: 24px; }
    h1 { font-size: 1.4rem; margin-bottom: 8px; color: #fff; }
    .meta { color: #888; margin-bottom: 24px; font-size: 0.85rem; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(${hasImages ? "280px" : "400px"}, 1fr)); gap: 16px; }
    .card { background: #1a1a1a; border-radius: 12px; overflow: hidden; border: 1px solid #333; transition: border-color 0.2s; cursor: pointer; }
    .card:hover { border-color: #666; }
    .card.selected { border-color: #4CAF50; box-shadow: 0 0 0 2px #4CAF5044; }
    .card-img { width: 100%; height: 200px; background-size: contain; background-position: center; background-repeat: no-repeat; background-color: #111; }
    .card-body { padding: 12px; }
    .card-body h3 { font-size: 0.95rem; margin-bottom: 4px; }
    .subtitle { color: #aaa; font-size: 0.8rem; margin-bottom: 4px; }
    .authors { color: #aaa; font-size: 0.8rem; margin-bottom: 4px; font-style: italic; }
    .desc { font-size: 0.8rem; color: #999; margin-bottom: 8px; line-height: 1.4; }
    .badge { display: inline-block; background: #333; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; color: #aaa; margin-right: 8px; }
    a { color: #64B5F6; font-size: 0.8rem; text-decoration: none; margin-right: 12px; }
    a:hover { text-decoration: underline; }
    .links { margin-top: 8px; }
    .toolbar { position: fixed; bottom: 0; left: 0; right: 0; background: #1a1a1a; border-top: 1px solid #333; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; }
    .toolbar button { background: #4CAF50; color: white; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 0.9rem; }
    .toolbar button:hover { background: #45a049; }
    .toolbar .count { color: #888; font-size: 0.85rem; }
    .text-card .card-body { padding: 16px; }
    footer { height: 60px; }
  </style>
</head>
<body>
  <h1>${title}</h1>
  <p class="meta">${items.length} results · Click to select · recursive.eco grammar builder</p>
  <div class="grid">
    ${cards}
  </div>
  <footer></footer>
  <div class="toolbar">
    <span class="count"><span id="sel-count">0</span> selected</span>
    <button onclick="copySelected()">Copy selected to clipboard</button>
  </div>
  <script>
    const selected = new Set();
    document.querySelectorAll('.card').forEach(card => {
      card.addEventListener('click', (e) => {
        if (e.target.tagName === 'A') return;
        const idx = card.dataset.index;
        if (selected.has(idx)) { selected.delete(idx); card.classList.remove('selected'); }
        else { selected.add(idx); card.classList.add('selected'); }
        document.getElementById('sel-count').textContent = selected.size;
      });
    });
    const items = ${JSON.stringify(items)};
    function copySelected() {
      const picks = [...selected].sort().map(i => items[i]);
      navigator.clipboard.writeText(JSON.stringify(picks, null, 2));
      const btn = document.querySelector('.toolbar button');
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = 'Copy selected to clipboard', 1500);
    }
  </script>
</body>
</html>`;
}

export function registerPreviewTools(server: McpServer) {
  server.tool(
    "preview_results",
    "Generate an HTML preview page for search results (images, texts, or papers). Opens in the user's browser for visual browsing and selection. Pass the 'results' array from any search tool.",
    {
      results: z.string().describe("JSON string of search results array (from any search tool)"),
      title: z.string().optional().describe("Preview page title (default 'Search Results')"),
      output_path: z.string().optional().describe("File path for HTML output (default: ./previews/preview.html)"),
    },
    async ({ results, title, output_path }) => {
      try {
        const items: PreviewItem[] = JSON.parse(results);
        const html = generatePreviewHTML(items, title || "Search Results");

        const outPath = output_path || resolve(process.cwd(), "previews", "preview.html");

        // Ensure directory exists
        const dir = outPath.substring(0, outPath.lastIndexOf("/"));
        await import("node:fs").then((fs) =>
          fs.mkdirSync(dir, { recursive: true })
        );

        await writeFile(outPath, html, "utf-8");

        return {
          content: [
            {
              type: "text" as const,
              text: `Preview generated: ${outPath}\n\nOpen in browser to browse ${items.length} results visually. Click cards to select, then "Copy selected" to get JSON for the items you want.`,
            },
          ],
        };
      } catch (e) {
        return {
          content: [{ type: "text" as const, text: `Error: ${(e as Error).message}` }],
          isError: true,
        };
      }
    }
  );
}
