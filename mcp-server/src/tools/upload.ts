import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { trackUsage, canUpload, getUsageSummary } from "./usage.js";

const WORKER_URL_ENV = "RECURSIVE_ECO_WORKER_URL";
const API_KEY_ENV = "RECURSIVE_ECO_API_KEY";

function getWorkerConfig() {
  const workerUrl = process.env[WORKER_URL_ENV];
  const apiKey = process.env[API_KEY_ENV];
  if (!workerUrl) throw new Error(`${WORKER_URL_ENV} not set. Configure the Cloudflare Worker URL.`);
  if (!apiKey) throw new Error(`${API_KEY_ENV} not set. Get your API key from the recursive.eco dashboard.`);
  return { workerUrl, apiKey };
}

export function registerUploadTools(server: McpServer) {
  server.tool(
    "upload_image_from_url",
    "Upload a public domain image to recursive.eco's Cloudflare R2 by providing its source URL. The Worker fetches and stores it. Returns the permanent R2 URL for use in grammar items.",
    {
      source_url: z.string().url().describe("URL of the image to upload (must be publicly accessible)"),
      grammar_slug: z.string().describe("Grammar name slug (e.g., 'alice-in-wonderland')"),
      item_id: z.string().describe("Grammar item ID this image belongs to (e.g., 'ch01-down-the-rabbit-hole')"),
      filename: z.string().describe("Output filename (e.g., 'rackham-1907.jpg')"),
      artist: z.string().optional().describe("Artist name for attribution"),
      license: z.string().optional().describe("License (default 'Public Domain')"),
    },
    async ({ source_url, grammar_slug, item_id, filename, artist, license }) => {
      try {
        // Check free-tier limits before uploading
        const allowed = await canUpload();
        if (!allowed) {
          const usage = await getUsageSummary();
          return {
            content: [{
              type: "text" as const,
              text: `Upload blocked — free tier limit reached.\n\n${JSON.stringify(usage, null, 2)}\n\nWait until next month or contact recursive.eco for increased limits.`,
            }],
            isError: true,
          };
        }

        const { workerUrl, apiKey } = getWorkerConfig();

        const r2Path = `grammar-illustrations/${grammar_slug}/${item_id}/${filename}`;

        const res = await fetch(`${workerUrl}/upload`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${apiKey}`,
          },
          body: JSON.stringify({
            source_url,
            r2_path: r2Path,
            metadata: {
              artist: artist || "Unknown",
              license: license || "Public Domain",
              grammar_slug,
              item_id,
              uploaded_at: new Date().toISOString(),
            },
          }),
        });

        if (!res.ok) {
          const body = await res.text();
          throw new Error(`Worker upload failed (${res.status}): ${body}`);
        }

        const result = (await res.json()) as { url: string; size: number };

        // Track this upload for free-tier monitoring
        await trackUsage("upload", result.size || 0);

        return {
          content: [{
            type: "text" as const,
            text: JSON.stringify({
              status: "uploaded",
              r2_url: result.url,
              r2_path: r2Path,
              size_bytes: result.size,
              illustration_entry: {
                url: result.url,
                artist: artist || "Unknown",
                license: license || "Public Domain",
                is_primary: false,
              },
            }, null, 2),
          }],
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
