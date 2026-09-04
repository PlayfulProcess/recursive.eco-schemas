import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// Semantic Scholar — free academic paper search (100 req/5min unauthenticated)
async function searchSemanticScholar(query: string, limit: number = 10, openAccessOnly: boolean = false) {
  const url = new URL("https://api.semanticscholar.org/graph/v1/paper/search");
  url.searchParams.set("query", query);
  url.searchParams.set("limit", String(limit));
  url.searchParams.set("fields", "title,authors,year,abstract,url,openAccessPdf,citationCount,venue,publicationTypes");
  if (openAccessOnly) {
    url.searchParams.set("openAccessPdf", "");
  }

  const res = await fetch(url.toString());
  if (!res.ok) {
    if (res.status === 429) throw new Error("Rate limited — wait 5 minutes (100 requests per 5 min)");
    throw new Error(`Semantic Scholar API error: ${res.status}`);
  }
  const data = (await res.json()) as SemanticScholarResponse;

  return {
    total: data.total,
    results: data.data.map((paper) => ({
      paper_id: paper.paperId,
      title: paper.title,
      authors: paper.authors?.map((a) => a.name).slice(0, 5) || [],
      year: paper.year,
      venue: paper.venue,
      citation_count: paper.citationCount,
      abstract: paper.abstract?.slice(0, 300) || null,
      types: paper.publicationTypes || [],
      open_access_pdf: paper.openAccessPdf?.url || null,
      semantic_scholar_url: paper.url,
    })),
  };
}

// arXiv API — free scientific preprints
async function searchArxiv(query: string, limit: number = 10) {
  const url = new URL("http://export.arxiv.org/api/query");
  url.searchParams.set("search_query", `all:${query}`);
  url.searchParams.set("start", "0");
  url.searchParams.set("max_results", String(limit));
  url.searchParams.set("sortBy", "relevance");

  const res = await fetch(url.toString());
  if (!res.ok) throw new Error(`arXiv API error: ${res.status}`);
  const xml = await res.text();

  // Simple XML parsing for arXiv Atom feed
  const entries = xml.split("<entry>").slice(1);
  const results = entries.map((entry) => {
    const get = (tag: string) => {
      const match = entry.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`));
      return match ? match[1].trim() : null;
    };
    const getAll = (tag: string) => {
      const matches = [...entry.matchAll(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`, "g"))];
      return matches.map((m) => m[1].trim());
    };
    const getAttr = (tag: string, attr: string) => {
      const match = entry.match(new RegExp(`<${tag}[^>]*${attr}="([^"]*)"[^>]*/>`));
      return match ? match[1] : null;
    };

    return {
      arxiv_id: get("id")?.replace("http://arxiv.org/abs/", "") || "",
      title: get("title")?.replace(/\s+/g, " ") || "",
      authors: getAll("name").slice(0, 5),
      published: get("published")?.slice(0, 10) || "",
      abstract: get("summary")?.replace(/\s+/g, " ").slice(0, 300) || "",
      pdf_url: getAttr("link", 'title="pdf"') || `http://arxiv.org/pdf/${get("id")?.replace("http://arxiv.org/abs/", "")}`,
      categories: entry.match(/term="([^"]+)"/g)?.map((m) => m.slice(6, -1)).slice(0, 5) || [],
      arxiv_url: get("id") || "",
    };
  });

  return { count: results.length, results };
}

interface SemanticScholarResponse {
  total: number;
  data: Array<{
    paperId: string;
    title: string;
    authors?: Array<{ name: string }>;
    year?: number;
    venue?: string;
    citationCount?: number;
    abstract?: string;
    publicationTypes?: string[];
    openAccessPdf?: { url: string };
    url: string;
  }>;
}

export function registerPaperSearchTools(server: McpServer) {
  server.tool(
    "search_papers",
    "Search Semantic Scholar for academic papers. 200M+ papers with citation data. Free: 100 requests per 5 minutes.",
    {
      query: z.string().describe("Search query (e.g., 'mindfulness meditation neuroplasticity')"),
      limit: z.number().optional().describe("Max results (default 10, max 100)"),
      open_access_only: z.boolean().optional().describe("Only return papers with free PDF (default false)"),
    },
    async ({ query, limit, open_access_only }) => {
      try {
        const results = await searchSemanticScholar(query, Math.min(limit || 10, 100), open_access_only || false);
        return {
          content: [{ type: "text" as const, text: JSON.stringify(results, null, 2) }],
        };
      } catch (e) {
        return {
          content: [{ type: "text" as const, text: `Error: ${(e as Error).message}` }],
          isError: true,
        };
      }
    }
  );

  server.tool(
    "search_arxiv",
    "Search arXiv for scientific preprints. All papers are free/open access. Great for physics, math, CS, biology, and more.",
    {
      query: z.string().describe("Search query (e.g., 'transformer attention mechanism')"),
      limit: z.number().optional().describe("Max results (default 10, max 50)"),
    },
    async ({ query, limit }) => {
      try {
        const results = await searchArxiv(query, Math.min(limit || 10, 50));
        return {
          content: [{ type: "text" as const, text: JSON.stringify(results, null, 2) }],
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
