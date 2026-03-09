#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { registerTextSearchTools } from "./tools/search-texts.js";
import { registerImageSearchTools } from "./tools/search-images.js";
import { registerPaperSearchTools } from "./tools/search-papers.js";
import { registerPreviewTools } from "./tools/preview.js";
import { registerUploadTools } from "./tools/upload.js";
import { registerUsageTools } from "./tools/usage.js";

const server = new McpServer({
  name: "recursive-eco",
  version: "0.1.0",
});

// Register all tool groups
registerTextSearchTools(server);
registerImageSearchTools(server);
registerPaperSearchTools(server);
registerPreviewTools(server);
registerUploadTools(server);
registerUsageTools(server);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
