/**
 * Cloudflare Worker for recursive.eco image uploads.
 *
 * Endpoints:
 *   POST /upload   — Fetch image from URL, store in R2
 *   GET  /usage    — Return current usage stats
 *   GET  /health   — Health check
 *
 * Auth: Bearer token (API_KEYS secret, comma-separated)
 * Usage tracking: KV-based, resets monthly, enforces free-tier limits
 */

interface Env {
  R2: R2Bucket;
  USAGE: KVNamespace;
  API_KEYS: string; // comma-separated valid keys
}

// Free-tier limits (90% thresholds for safety margin)
const LIMITS = {
  monthly_uploads: 900_000,
  monthly_storage_bytes: 9 * 1024 * 1024 * 1024, // 9GB
  daily_requests: 90_000,
  max_file_size: 10 * 1024 * 1024, // 10MB per file
};

const ALLOWED_TYPES = new Set([
  "image/jpeg", "image/png", "image/webp", "image/gif", "image/svg+xml",
]);

function corsHeaders(): Record<string, string> {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
  };
}

function jsonResponse(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders() },
  });
}

function errorResponse(message: string, status = 400): Response {
  return jsonResponse({ error: message }, status);
}

// --- Auth ---

function authenticate(request: Request, env: Env): boolean {
  const auth = request.headers.get("Authorization");
  if (!auth?.startsWith("Bearer ")) return false;
  const token = auth.slice(7);
  const validKeys = env.API_KEYS.split(",").map((k) => k.trim());
  return validKeys.includes(token);
}

// --- Usage Tracking (KV) ---

interface UsageData {
  month: string;
  uploads: number;
  bytes: number;
  daily: Record<string, number>;
}

function currentMonth(): string {
  return new Date().toISOString().slice(0, 7);
}

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

async function getUsage(kv: KVNamespace): Promise<UsageData> {
  const raw = await kv.get("usage", "json");
  const data = raw as UsageData | null;
  if (!data || data.month !== currentMonth()) {
    return { month: currentMonth(), uploads: 0, bytes: 0, daily: {} };
  }
  return data;
}

async function incrementUsage(kv: KVNamespace, bytes: number): Promise<UsageData> {
  const usage = await getUsage(kv);
  usage.uploads++;
  usage.bytes += bytes;
  const d = today();
  usage.daily[d] = (usage.daily[d] || 0) + 1;
  await kv.put("usage", JSON.stringify(usage));
  return usage;
}

function checkLimits(usage: UsageData): { allowed: boolean; reason?: string } {
  if (usage.uploads >= LIMITS.monthly_uploads) {
    return { allowed: false, reason: `Monthly upload limit reached (${usage.uploads}/${LIMITS.monthly_uploads})` };
  }
  if (usage.bytes >= LIMITS.monthly_storage_bytes) {
    return { allowed: false, reason: `Monthly storage limit reached (${formatBytes(usage.bytes)}/9GB)` };
  }
  const d = today();
  const dailyReqs = usage.daily[d] || 0;
  if (dailyReqs >= LIMITS.daily_requests) {
    return { allowed: false, reason: `Daily request limit reached (${dailyReqs}/${LIMITS.daily_requests})` };
  }
  return { allowed: true };
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
}

// --- Handlers ---

async function handleUpload(request: Request, env: Env): Promise<Response> {
  if (!authenticate(request, env)) {
    return errorResponse("Unauthorized", 401);
  }

  const body = (await request.json()) as {
    source_url: string;
    r2_path: string;
    metadata?: Record<string, string>;
  };

  if (!body.source_url || !body.r2_path) {
    return errorResponse("Missing source_url or r2_path");
  }

  // Check limits before fetching
  const usage = await getUsage(env.USAGE);
  const limitCheck = checkLimits(usage);
  if (!limitCheck.allowed) {
    return errorResponse(`Free tier limit: ${limitCheck.reason}`, 429);
  }

  // Validate path (prevent directory traversal)
  if (body.r2_path.includes("..") || !body.r2_path.startsWith("grammar-illustrations/")) {
    return errorResponse("Invalid r2_path — must start with grammar-illustrations/");
  }

  // Fetch the source image
  let imageRes: Response;
  try {
    imageRes = await fetch(body.source_url, {
      headers: { "User-Agent": "recursive.eco grammar builder (https://recursive.eco)" },
    });
  } catch {
    return errorResponse("Failed to fetch source URL");
  }

  if (!imageRes.ok) {
    return errorResponse(`Source returned ${imageRes.status}`);
  }

  // Validate content type
  const contentType = imageRes.headers.get("Content-Type")?.split(";")[0] || "";
  if (!ALLOWED_TYPES.has(contentType)) {
    return errorResponse(`Invalid content type: ${contentType}. Allowed: ${[...ALLOWED_TYPES].join(", ")}`);
  }

  // Read body and check size
  const imageBuffer = await imageRes.arrayBuffer();
  if (imageBuffer.byteLength > LIMITS.max_file_size) {
    return errorResponse(`File too large: ${formatBytes(imageBuffer.byteLength)} (max ${formatBytes(LIMITS.max_file_size)})`);
  }

  // Upload to R2
  await env.R2.put(body.r2_path, imageBuffer, {
    httpMetadata: { contentType },
    customMetadata: body.metadata || {},
  });

  // Track usage
  await incrementUsage(env.USAGE, imageBuffer.byteLength);

  // Build the public URL (assumes public bucket or custom domain)
  const publicUrl = `https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/${body.r2_path}`;

  return jsonResponse({
    url: publicUrl,
    r2_path: body.r2_path,
    size: imageBuffer.byteLength,
    content_type: contentType,
  });
}

async function handleUsage(request: Request, env: Env): Promise<Response> {
  // Usage endpoint is public (no auth needed) — just shows aggregate stats
  const usage = await getUsage(env.USAGE);
  const d = today();

  return jsonResponse({
    month: usage.month,
    uploads: { count: usage.uploads, limit: LIMITS.monthly_uploads },
    storage: { bytes: usage.bytes, human: formatBytes(usage.bytes), limit: "9 GB" },
    today_requests: { count: usage.daily[d] || 0, limit: LIMITS.daily_requests },
    status: checkLimits(usage).allowed ? "healthy" : "blocked",
  });
}

// --- Router ---

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    if (path === "/health") {
      return jsonResponse({ status: "ok", version: "0.1.0" });
    }

    if (path === "/usage" && request.method === "GET") {
      return handleUsage(request, env);
    }

    if (path === "/upload" && request.method === "POST") {
      return handleUpload(request, env);
    }

    return errorResponse("Not found", 404);
  },
};
