import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// Wikimedia Commons — largest free media repository (free, no key)
async function searchWikimediaCommons(query: string, limit: number = 20) {
  const url = new URL("https://commons.wikimedia.org/w/api.php");
  url.searchParams.set("action", "query");
  url.searchParams.set("list", "search");
  url.searchParams.set("srsearch", query);
  url.searchParams.set("srnamespace", "6"); // File namespace
  url.searchParams.set("srlimit", String(limit));
  url.searchParams.set("format", "json");
  url.searchParams.set("origin", "*");

  const res = await fetch(url.toString());
  if (!res.ok) throw new Error(`Wikimedia API error: ${res.status}`);
  const data = (await res.json()) as WikimediaSearchResponse;

  const titles = data.query.search.map((s) => s.title);
  if (titles.length === 0) return { count: 0, results: [] };

  // Get image info (URLs, dimensions, license) for all results
  const infoUrl = new URL("https://commons.wikimedia.org/w/api.php");
  infoUrl.searchParams.set("action", "query");
  infoUrl.searchParams.set("titles", titles.join("|"));
  infoUrl.searchParams.set("prop", "imageinfo|categories");
  infoUrl.searchParams.set("iiprop", "url|size|mime|extmetadata");
  infoUrl.searchParams.set("iiurlwidth", "400"); // thumbnail
  infoUrl.searchParams.set("format", "json");
  infoUrl.searchParams.set("origin", "*");

  const infoRes = await fetch(infoUrl.toString());
  if (!infoRes.ok) throw new Error(`Wikimedia imageinfo error: ${infoRes.status}`);
  const infoData = (await infoRes.json()) as WikimediaInfoResponse;

  const results = Object.values(infoData.query.pages)
    .filter((p) => p.imageinfo?.length)
    .map((p) => {
      const info = p.imageinfo![0];
      const meta = info.extmetadata || {};
      return {
        title: p.title.replace("File:", ""),
        thumbnail_url: info.thumburl,
        full_url: info.url,
        width: info.width,
        height: info.height,
        mime: info.mime,
        license: meta.LicenseShortName?.value || "Unknown",
        artist: meta.Artist?.value?.replace(/<[^>]*>/g, "") || "Unknown",
        description: meta.ImageDescription?.value?.replace(/<[^>]*>/g, "")?.slice(0, 200) || "",
        date: meta.DateTimeOriginal?.value || meta.DateTime?.value || "",
        commons_url: `https://commons.wikimedia.org/wiki/${encodeURIComponent(p.title)}`,
      };
    });

  return {
    count: data.query.searchinfo?.totalhits || results.length,
    results,
  };
}

// Met Museum Open Access API — 490K+ works, all CC0 (free, no key)
async function searchMetMuseum(query: string, limit: number = 20) {
  const searchUrl = new URL(
    "https://collectionapi.metmuseum.org/public/collection/v1/search"
  );
  searchUrl.searchParams.set("q", query);
  searchUrl.searchParams.set("isPublicDomain", "true");
  searchUrl.searchParams.set("hasImages", "true");

  const searchRes = await fetch(searchUrl.toString());
  if (!searchRes.ok) throw new Error(`Met Museum API error: ${searchRes.status}`);
  const searchData = (await searchRes.json()) as MetSearchResponse;

  if (!searchData.objectIDs?.length) return { count: 0, results: [] };

  // Fetch details for first N objects (API is one-at-a-time)
  const ids = searchData.objectIDs.slice(0, limit);
  const details = await Promise.all(
    ids.map(async (id) => {
      try {
        const res = await fetch(
          `https://collectionapi.metmuseum.org/public/collection/v1/objects/${id}`
        );
        if (!res.ok) return null;
        return (await res.json()) as MetObjectResponse;
      } catch {
        return null;
      }
    })
  );

  return {
    count: searchData.total,
    results: details
      .filter((d): d is MetObjectResponse => d !== null && !!d.primaryImage)
      .map((d) => ({
        object_id: d.objectID,
        title: d.title,
        artist: d.artistDisplayName || "Unknown",
        date: d.objectDate,
        medium: d.medium,
        department: d.department,
        image_url: d.primaryImage,
        thumbnail_url: d.primaryImageSmall,
        met_url: d.objectURL,
        license: "CC0 (Public Domain)",
      })),
  };
}

interface WikimediaSearchResponse {
  query: {
    searchinfo?: { totalhits: number };
    search: Array<{ title: string }>;
  };
}

interface WikimediaInfoResponse {
  query: {
    pages: Record<
      string,
      {
        title: string;
        imageinfo?: Array<{
          url: string;
          thumburl: string;
          width: number;
          height: number;
          mime: string;
          extmetadata?: Record<string, { value: string }>;
        }>;
      }
    >;
  };
}

interface MetSearchResponse {
  total: number;
  objectIDs: number[] | null;
}

interface MetObjectResponse {
  objectID: number;
  title: string;
  artistDisplayName?: string;
  objectDate?: string;
  medium?: string;
  department?: string;
  primaryImage: string;
  primaryImageSmall: string;
  objectURL: string;
}

export function registerImageSearchTools(server: McpServer) {
  server.tool(
    "search_wikimedia_images",
    "Search Wikimedia Commons for public domain images — illustrations, paintings, photographs, diagrams. The largest free media library in the world.",
    {
      query: z.string().describe("Search query (e.g., 'Alice Wonderland illustration 1900s', 'tarot major arcana')"),
      limit: z.number().optional().describe("Max results (default 20, max 50)"),
    },
    async ({ query, limit }) => {
      try {
        const results = await searchWikimediaCommons(query, Math.min(limit || 20, 50));
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
    "search_met_museum",
    "Search the Metropolitan Museum of Art's Open Access collection. 490K+ works, all CC0/public domain. Great for fine art, historical illustrations, and artifacts.",
    {
      query: z.string().describe("Search query (e.g., 'Japanese woodblock print', 'medieval manuscript')"),
      limit: z.number().optional().describe("Max results (default 10, max 20 — each requires an API call)"),
    },
    async ({ query, limit }) => {
      try {
        const results = await searchMetMuseum(query, Math.min(limit || 10, 20));
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
