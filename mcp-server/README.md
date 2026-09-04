# recursive.eco MCP Server

An MCP server that gives Claude the power to search public domain texts, images, and academic papers — and upload curated images to Cloudflare R2 for grammar building.

## Tools

### Text Search
- **`search_gutenberg`** — Search Project Gutenberg (60K+ free books). No API key.
- **`search_open_library`** — Search Open Library / Internet Archive. No API key.
- **`get_gutenberg_text`** — Download full text of a Gutenberg book by ID.

### Image Search
- **`search_wikimedia_images`** — Search Wikimedia Commons (100M+ free media). No API key.
- **`search_met_museum`** — Search Met Museum Open Access (490K+ works, all CC0). No API key.

### Academic Papers
- **`search_papers`** — Search Semantic Scholar (200M+ papers). Free, 100 req/5min.
- **`search_arxiv`** — Search arXiv preprints. Free, open access.

### Preview & Upload
- **`preview_results`** — Generate a local HTML page to visually browse search results.
- **`upload_image_from_url`** — Upload an image to R2 via the Cloudflare Worker.
- **`check_usage`** — See current usage vs. Cloudflare free tier limits.

## Quick Start

```bash
# Install
cd mcp-server
npm install

# Run with Claude Desktop — add to claude_desktop_config.json:
{
  "mcpServers": {
    "recursive-eco": {
      "command": "npx",
      "args": ["tsx", "/path/to/mcp-server/src/index.ts"]
    }
  }
}
```

## For Image Uploads

Image uploads require the Cloudflare Worker to be deployed:

```bash
# 1. Deploy the worker
cd worker
npm install
wrangler kv:namespace create USAGE
# Copy the KV namespace ID into wrangler.toml
wrangler secret put API_KEYS  # Enter comma-separated API keys
wrangler deploy

# 2. Configure the MCP server
export RECURSIVE_ECO_WORKER_URL="https://recursive-eco-uploads.<your-subdomain>.workers.dev"
export RECURSIVE_ECO_API_KEY="your-api-key"
```

## Free Tier Limits

The server tracks usage locally (`~/.recursive-eco/usage.json`) and blocks before hitting Cloudflare free tier limits:

| Resource | Free Tier | Safety Threshold (90%) |
|----------|-----------|----------------------|
| R2 Storage | 10 GB/month | 9 GB |
| R2 Writes | 1M/month | 900K |
| R2 Reads | 10M/month | 9M |
| Worker Requests | 100K/day | 90K |

Use `check_usage` to see current status: `healthy` → `warning` → `blocked`.

## Architecture

```
┌──────────────────────┐     ┌──────────────────────┐
│  Claude Desktop/Code │     │   Free Public APIs   │
│  (MCP Client)        │     │  - Gutenberg         │
│                      │     │  - Open Library       │
│  ┌────────────────┐  │     │  - Wikimedia Commons  │
│  │ MCP Server     │──┼────▶│  - Met Museum         │
│  │ (local, $0)    │  │     │  - Semantic Scholar   │
│  └───────┬────────┘  │     │  - arXiv              │
│          │           │     └──────────────────────┘
│          │ upload     │
│          ▼           │     ┌──────────────────────┐
│  ┌────────────────┐  │     │  Cloudflare Worker   │
│  │ Usage Tracker  │  │     │  (free tier)          │
│  │ (~/.recursive) │  ├────▶│  POST /upload         │
│  └────────────────┘  │     │  GET  /usage          │
└──────────────────────┘     │       │               │
                             │       ▼               │
                             │  ┌──────────┐         │
                             │  │ R2 Bucket │         │
                             │  │ (free 10G)│         │
                             │  └──────────┘         │
                             └──────────────────────┘
```

## No API Keys Needed (for search)

All search tools work without API keys. The only configuration needed is for the upload feature (Cloudflare Worker URL + API key).
