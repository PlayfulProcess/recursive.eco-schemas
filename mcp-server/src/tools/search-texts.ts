import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// Gutendex — JSON API for Project Gutenberg (free, no key)
// https://gutendex.com/
async function searchGutenberg(query: string, page: number = 1) {
  const url = new URL("https://gutendex.com/books");
  url.searchParams.set("search", query);
  url.searchParams.set("page", String(page));

  const res = await fetch(url.toString());
  if (!res.ok) throw new Error(`Gutendex API error: ${res.status}`);
  const data = (await res.json()) as GutendexResponse;

  return {
    count: data.count,
    results: data.results.map((book) => ({
      id: book.id,
      title: book.title,
      authors: book.authors.map(
        (a) =>
          `${a.name}${a.birth_year ? ` (${a.birth_year}–${a.death_year || "?"})` : ""}`
      ),
      subjects: book.subjects?.slice(0, 5) || [],
      languages: book.languages,
      download_count: book.download_count,
      formats: {
        text: book.formats["text/plain; charset=utf-8"] || book.formats["text/plain"] || null,
        html: book.formats["text/html"] || null,
        epub: book.formats["application/epub+zip"] || null,
      },
      gutenberg_url: `https://www.gutenberg.org/ebooks/${book.id}`,
    })),
  };
}

// Open Library — Internet Archive book search (free, no key)
async function searchOpenLibrary(query: string, page: number = 1) {
  const url = new URL("https://openlibrary.org/search.json");
  url.searchParams.set("q", query);
  url.searchParams.set("page", String(page));
  url.searchParams.set("limit", "20");
  url.searchParams.set("fields", "key,title,author_name,first_publish_year,subject,edition_count,cover_i,ia");

  const res = await fetch(url.toString());
  if (!res.ok) throw new Error(`Open Library API error: ${res.status}`);
  const data = (await res.json()) as OpenLibraryResponse;

  return {
    count: data.numFound,
    results: data.docs.map((doc) => ({
      key: doc.key,
      title: doc.title,
      authors: doc.author_name || [],
      first_published: doc.first_publish_year,
      subjects: doc.subject?.slice(0, 5) || [],
      editions: doc.edition_count,
      cover_url: doc.cover_i
        ? `https://covers.openlibrary.org/b/id/${doc.cover_i}-M.jpg`
        : null,
      internet_archive_ids: doc.ia?.slice(0, 3) || [],
      openlibrary_url: `https://openlibrary.org${doc.key}`,
    })),
  };
}

interface GutendexResponse {
  count: number;
  results: Array<{
    id: number;
    title: string;
    authors: Array<{ name: string; birth_year?: number; death_year?: number }>;
    subjects?: string[];
    languages: string[];
    download_count: number;
    formats: Record<string, string>;
  }>;
}

interface OpenLibraryResponse {
  numFound: number;
  docs: Array<{
    key: string;
    title: string;
    author_name?: string[];
    first_publish_year?: number;
    subject?: string[];
    edition_count?: number;
    cover_i?: number;
    ia?: string[];
  }>;
}

export function registerTextSearchTools(server: McpServer) {
  server.tool(
    "search_gutenberg",
    "Search Project Gutenberg for public domain books and texts. Returns download links for plain text, HTML, and EPUB formats.",
    {
      query: z.string().describe("Search query (title, author, or subject)"),
      page: z.number().optional().describe("Page number (default 1, 32 results per page)"),
    },
    async ({ query, page }) => {
      try {
        const results = await searchGutenberg(query, page);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(results, null, 2),
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

  server.tool(
    "search_open_library",
    "Search Open Library (Internet Archive) for books. Great for metadata, covers, and finding texts available on Internet Archive.",
    {
      query: z.string().describe("Search query (title, author, or subject)"),
      page: z.number().optional().describe("Page number (default 1)"),
    },
    async ({ query, page }) => {
      try {
        const results = await searchOpenLibrary(query, page);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(results, null, 2),
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

  server.tool(
    "get_gutenberg_text",
    "Download the full plain text of a Project Gutenberg book by its ID. Use search_gutenberg first to find the ID.",
    {
      book_id: z.number().describe("Project Gutenberg book ID"),
      max_chars: z.number().optional().describe("Max characters to return (default 50000, for preview)"),
    },
    async ({ book_id, max_chars }) => {
      const limit = max_chars || 50000;
      try {
        const url = `https://www.gutenberg.org/cache/epub/${book_id}/pg${book_id}.txt`;
        const res = await fetch(url);
        if (!res.ok) throw new Error(`Failed to fetch book ${book_id}: ${res.status}`);
        let text = await res.text();

        const truncated = text.length > limit;
        if (truncated) text = text.slice(0, limit);

        return {
          content: [
            {
              type: "text" as const,
              text: truncated
                ? `[Showing first ${limit} chars of ${text.length + (text.length > limit ? "+" : "")} total]\n\n${text}`
                : text,
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
