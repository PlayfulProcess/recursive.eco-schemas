import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { writeFile, readFile, mkdir } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { existsSync } from "node:fs";

interface GrammarItem {
  id: string;
  name: string;
  sort_order?: number;
  category?: string;
  level?: number;
  sections: Record<string, string>;
  keywords?: string[];
  metadata?: Record<string, unknown>;
  composite_of?: string[];
  relationship_type?: string;
  image_url?: string;
}

interface Grammar {
  _grammar_commons: {
    schema_version: string;
    license: string;
    attribution: Array<{ name: string; date?: string; note?: string }>;
  };
  name: string;
  description: string;
  grammar_type: "custom" | "tarot" | "iching" | "astrology" | "sequence";
  creator_name: string;
  tags?: string[];
  roots?: string[];
  shelves?: string[];
  lineages?: string[];
  worldview?: string;
  items: GrammarItem[];
}

function validateGrammar(grammar: Grammar): string[] {
  const errors: string[] = [];

  // Required top-level fields
  if (!grammar.name) errors.push("Missing 'name'");
  if (!grammar.description) errors.push("Missing 'description'");
  if (!grammar.grammar_type) errors.push("Missing 'grammar_type'");
  if (!grammar.creator_name) errors.push("Missing 'creator_name'");

  // Attribution
  if (!grammar._grammar_commons) {
    errors.push("Missing '_grammar_commons'");
  } else {
    if (!grammar._grammar_commons.schema_version)
      errors.push("Missing '_grammar_commons.schema_version'");
    if (!grammar._grammar_commons.attribution?.length)
      errors.push("Missing '_grammar_commons.attribution'");
  }

  const items = grammar.items || [];
  if (items.length === 0) {
    errors.push("No items found");
    return errors;
  }

  // Duplicate IDs
  const ids = new Set<string>();
  for (const item of items) {
    if (!item.id) {
      errors.push(`Item missing 'id': ${JSON.stringify(item).slice(0, 80)}`);
      continue;
    }
    if (ids.has(item.id)) {
      errors.push(`Duplicate ID: '${item.id}'`);
    }
    ids.add(item.id);
  }

  // Required item fields
  for (const item of items) {
    if (!item.name) errors.push(`Item '${item.id}': missing 'name'`);
    if (!item.sections || Object.keys(item.sections).length === 0)
      errors.push(`Item '${item.id}': missing or empty 'sections'`);
  }

  // composite_of referential integrity
  for (const item of items) {
    if (item.composite_of) {
      for (const ref of item.composite_of) {
        if (!ids.has(ref)) {
          errors.push(`Item '${item.id}': composite_of references non-existent ID '${ref}'`);
        }
      }
    }
  }

  // Emergence levels check
  const levels = new Set(items.map((i) => i.level).filter(Boolean));
  if (!levels.has(2) && items.length > 5) {
    errors.push(
      "Warning: No L2 emergence items. Every grammar should have L2/L3 items for grouping."
    );
  }

  return errors;
}

function slugify(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export function registerGrammarTools(server: McpServer) {
  server.tool(
    "validate_grammar",
    "Validate a grammar JSON object against the recursive.eco schema. Checks: required fields, duplicate IDs, composite_of referential integrity, attribution, and emergence levels.",
    {
      grammar_json: z.string().describe("The grammar JSON string to validate"),
    },
    async ({ grammar_json }) => {
      try {
        const grammar: Grammar = JSON.parse(grammar_json);
        const errors = validateGrammar(grammar);

        if (errors.length === 0) {
          return {
            content: [{
              type: "text" as const,
              text: `Grammar "${grammar.name}" is valid.\n\n` +
                `Items: ${grammar.items.length}\n` +
                `L1: ${grammar.items.filter((i) => i.level === 1).length}\n` +
                `L2: ${grammar.items.filter((i) => i.level === 2).length}\n` +
                `L3: ${grammar.items.filter((i) => i.level === 3).length}\n` +
                `Type: ${grammar.grammar_type}\n` +
                `Tags: ${grammar.tags?.join(", ") || "none"}`,
            }],
          };
        } else {
          const warnings = errors.filter((e) => e.startsWith("Warning:"));
          const hard = errors.filter((e) => !e.startsWith("Warning:"));
          return {
            content: [{
              type: "text" as const,
              text: (hard.length
                ? `${hard.length} error(s):\n${hard.map((e) => `  - ${e}`).join("\n")}\n\n`
                : "") +
                (warnings.length
                  ? `${warnings.length} warning(s):\n${warnings.map((e) => `  - ${e}`).join("\n")}`
                  : ""),
            }],
            isError: hard.length > 0,
          };
        }
      } catch (e) {
        return {
          content: [{ type: "text" as const, text: `Invalid JSON: ${(e as Error).message}` }],
          isError: true,
        };
      }
    }
  );

  server.tool(
    "save_grammar",
    "Validate and save a grammar.json file to the grammars/ directory. Creates the folder if needed. Fails if validation finds errors (warnings are OK).",
    {
      grammar_json: z.string().describe("The complete grammar JSON string"),
      grammars_dir: z.string().optional().describe("Path to grammars/ directory (auto-detected if in a recursive.eco-schemas repo)"),
    },
    async ({ grammar_json, grammars_dir }) => {
      try {
        const grammar: Grammar = JSON.parse(grammar_json);
        const errors = validateGrammar(grammar);
        const hardErrors = errors.filter((e) => !e.startsWith("Warning:"));

        if (hardErrors.length > 0) {
          return {
            content: [{
              type: "text" as const,
              text: `Cannot save — ${hardErrors.length} validation error(s):\n${hardErrors.map((e) => `  - ${e}`).join("\n")}`,
            }],
            isError: true,
          };
        }

        const slug = slugify(grammar.name);

        // Find grammars directory
        let baseDir = grammars_dir;
        if (!baseDir) {
          // Try common locations
          const candidates = [
            resolve(process.cwd(), "grammars"),
            resolve(process.cwd(), "..", "grammars"),
            resolve(process.cwd(), "recursive.eco-schemas", "grammars"),
          ];
          baseDir = candidates.find((c) => existsSync(c));
          if (!baseDir) {
            baseDir = resolve(process.cwd(), "grammars");
          }
        }

        const outDir = resolve(baseDir, slug);
        await mkdir(outDir, { recursive: true });

        const outPath = resolve(outDir, "grammar.json");

        // Re-number sort_order
        grammar.items.forEach((item, idx) => {
          item.sort_order = idx;
        });

        const formatted = JSON.stringify(grammar, null, 2);
        await writeFile(outPath, formatted, "utf-8");

        const warnings = errors.filter((e) => e.startsWith("Warning:"));

        return {
          content: [{
            type: "text" as const,
            text: `Saved grammar "${grammar.name}" to:\n  ${outPath}\n\n` +
              `Items: ${grammar.items.length} (L1: ${grammar.items.filter((i) => i.level === 1).length}, ` +
              `L2: ${grammar.items.filter((i) => i.level === 2).length}, ` +
              `L3: ${grammar.items.filter((i) => i.level === 3).length})\n` +
              `Slug: ${slug}\n` +
              `Size: ${(formatted.length / 1024).toFixed(1)} KB` +
              (warnings.length ? `\n\nWarnings:\n${warnings.map((e) => `  - ${e}`).join("\n")}` : ""),
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

  server.tool(
    "list_grammars",
    "List all grammars in the grammars/ directory with their names, types, and item counts.",
    {
      grammars_dir: z.string().optional().describe("Path to grammars/ directory (auto-detected)"),
    },
    async ({ grammars_dir }) => {
      try {
        let baseDir = grammars_dir;
        if (!baseDir) {
          const candidates = [
            resolve(process.cwd(), "grammars"),
            resolve(process.cwd(), "..", "grammars"),
          ];
          baseDir = candidates.find((c) => existsSync(c));
          if (!baseDir) return { content: [{ type: "text" as const, text: "No grammars/ directory found" }], isError: true };
        }

        const { readdirSync } = await import("node:fs");
        const dirs = readdirSync(baseDir, { withFileTypes: true })
          .filter((d) => d.isDirectory())
          .map((d) => d.name)
          .sort();

        const grammars = [];
        for (const dir of dirs) {
          const gPath = resolve(baseDir, dir, "grammar.json");
          if (!existsSync(gPath)) continue;
          try {
            const raw = await readFile(gPath, "utf-8");
            const g = JSON.parse(raw) as Grammar;
            grammars.push({
              slug: dir,
              name: g.name,
              type: g.grammar_type,
              items: g.items?.length || 0,
              tags: g.tags?.slice(0, 3) || [],
            });
          } catch {
            grammars.push({ slug: dir, name: "?", type: "?", items: 0, tags: [] });
          }
        }

        return {
          content: [{
            type: "text" as const,
            text: `${grammars.length} grammars:\n\n` +
              grammars
                .map((g) => `  ${g.slug} — ${g.name} (${g.type}, ${g.items} items)`)
                .join("\n"),
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
