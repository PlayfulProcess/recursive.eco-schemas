import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { z } from "zod";

/**
 * Free-tier guardian — tracks usage locally and warns before hitting limits.
 *
 * Cloudflare free tier limits (as of March 2026):
 * - R2: 10 GB storage, 10M Class B reads/month, 1M Class A writes/month
 * - Workers: 100K requests/day, 10ms CPU time
 * - KV: 100K reads/day, 1K writes/day
 *
 * We track locally to avoid surprise charges. The Worker also tracks server-side.
 */

interface UsageRecord {
  month: string; // YYYY-MM
  uploads: number;
  upload_bytes: number;
  reads: number;
  worker_requests: number;
  daily: Record<string, { requests: number; reads: number }>;
}

const LIMITS = {
  monthly_uploads: 900_000,      // Stay under 1M Class A writes (90% threshold)
  monthly_reads: 9_000_000,      // Stay under 10M Class B reads (90% threshold)
  monthly_storage_bytes: 9 * 1024 * 1024 * 1024, // Stay under 10GB (90%)
  daily_worker_requests: 90_000, // Stay under 100K/day (90%)
};

function getUsagePath(): string {
  const home = process.env.HOME || process.env.USERPROFILE || "/tmp";
  return resolve(home, ".recursive-eco", "usage.json");
}

function currentMonth(): string {
  return new Date().toISOString().slice(0, 7);
}

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

async function loadUsage(): Promise<UsageRecord> {
  const path = getUsagePath();
  try {
    const data = JSON.parse(await readFile(path, "utf-8")) as UsageRecord;
    // Reset if new month
    if (data.month !== currentMonth()) {
      return { month: currentMonth(), uploads: 0, upload_bytes: 0, reads: 0, worker_requests: 0, daily: {} };
    }
    return data;
  } catch {
    return { month: currentMonth(), uploads: 0, upload_bytes: 0, reads: 0, worker_requests: 0, daily: {} };
  }
}

async function saveUsage(usage: UsageRecord): Promise<void> {
  const path = getUsagePath();
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, JSON.stringify(usage, null, 2), "utf-8");
}

export async function trackUsage(type: "upload" | "read" | "request", bytes: number = 0): Promise<void> {
  const usage = await loadUsage();
  const d = today();

  if (!usage.daily[d]) usage.daily[d] = { requests: 0, reads: 0 };

  switch (type) {
    case "upload":
      usage.uploads++;
      usage.upload_bytes += bytes;
      usage.worker_requests++;
      usage.daily[d].requests++;
      break;
    case "read":
      usage.reads++;
      usage.daily[d].reads++;
      break;
    case "request":
      usage.worker_requests++;
      usage.daily[d].requests++;
      break;
  }

  await saveUsage(usage);
}

export async function canUpload(): Promise<boolean> {
  const usage = await loadUsage();
  const d = today();
  const dailyReqs = usage.daily[d]?.requests || 0;

  return (
    usage.uploads < LIMITS.monthly_uploads &&
    usage.upload_bytes < LIMITS.monthly_storage_bytes &&
    dailyReqs < LIMITS.daily_worker_requests
  );
}

export async function getUsageSummary() {
  const usage = await loadUsage();
  const d = today();
  const dailyReqs = usage.daily[d]?.requests || 0;

  return {
    month: usage.month,
    uploads: {
      count: usage.uploads,
      limit: LIMITS.monthly_uploads,
      percent: ((usage.uploads / LIMITS.monthly_uploads) * 100).toFixed(1) + "%",
    },
    storage: {
      bytes: usage.upload_bytes,
      human: formatBytes(usage.upload_bytes),
      limit: formatBytes(LIMITS.monthly_storage_bytes),
      percent: ((usage.upload_bytes / LIMITS.monthly_storage_bytes) * 100).toFixed(1) + "%",
    },
    today_requests: {
      count: dailyReqs,
      limit: LIMITS.daily_worker_requests,
      percent: ((dailyReqs / LIMITS.daily_worker_requests) * 100).toFixed(1) + "%",
    },
    status: (usage.uploads < LIMITS.monthly_uploads * 0.8 &&
             usage.upload_bytes < LIMITS.monthly_storage_bytes * 0.8 &&
             dailyReqs < LIMITS.daily_worker_requests * 0.8)
      ? "healthy"
      : (usage.uploads >= LIMITS.monthly_uploads ||
         usage.upload_bytes >= LIMITS.monthly_storage_bytes ||
         dailyReqs >= LIMITS.daily_worker_requests)
        ? "blocked"
        : "warning",
  };
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
}

export function registerUsageTools(server: McpServer) {
  server.tool(
    "check_usage",
    "Check current usage against Cloudflare free tier limits. Shows uploads, storage, and request counts with percentage of limits used. Status: healthy / warning / blocked.",
    {},
    async () => {
      try {
        const summary = await getUsageSummary();
        return {
          content: [{ type: "text" as const, text: JSON.stringify(summary, null, 2) }],
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
