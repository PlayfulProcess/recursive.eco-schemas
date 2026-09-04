/**
 * Voice Assistant Proxy — tiny Node server that forwards questions to Claude API.
 *
 * The book.html calls POST /api/ask with { question, context }.
 * This proxy reads ANTHROPIC_API_KEY from .env (never exposed to browser).
 *
 * Usage:
 *   node scripts/voice-proxy.mjs           # Start on port 3457
 *   node scripts/voice-proxy.mjs --port 8080  # Custom port
 *
 * The static file server for the book should run on port 3456 separately.
 */
import { createServer } from 'http';
import { existsSync } from 'fs';
import { config } from 'dotenv';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import Anthropic from '@anthropic-ai/sdk';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load env — check schemas .env first, then recursive-eco .env.local
const envPaths = [
  resolve(__dirname, '../.env'),
  resolve(__dirname, '../../recursive-eco/.env.local'),
  resolve(__dirname, '../../recursive-eco/apps/flow/.env.local'),
];
for (const p of envPaths) {
  if (existsSync(p)) config({ path: p, override: true });
}

const args = process.argv.slice(2);
const portIdx = args.indexOf('--port');
const PORT = portIdx !== -1 ? parseInt(args[portIdx + 1], 10) : 3457;

if (!process.env.ANTHROPIC_API_KEY) {
  console.error('ANTHROPIC_API_KEY not found in .env — cannot start proxy.');
  process.exit(1);
}

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const SYSTEM_PROMPT = `You are a warm, friendly storytelling guide helping a young child explore "Alice's Adventures in Wonderland" by Lewis Carroll.

Rules:
- Keep answers to 2-3 SHORT sentences (they will be read aloud)
- Use simple, playful language appropriate for ages 4-7
- Reference the story, characters, and illustrations when relevant
- Be encouraging and spark curiosity
- If asked about something not in Alice, gently steer back to the story
- Never use scary or complex language`;

const server = createServer(async (req, res) => {
  // CORS headers (allow localhost origins)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (req.method === 'POST' && req.url === '/api/ask') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const { question, context } = JSON.parse(body);

        if (!question || question.trim().length === 0) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'No question provided' }));
          return;
        }

        console.log(`[${new Date().toISOString().substring(11, 19)}] Q: "${question}" | Context: ${(context || '').substring(0, 60)}`);

        const userMessage = context
          ? `The reader is currently looking at: ${context}\n\nTheir question: ${question}`
          : question;

        const response = await anthropic.messages.create({
          model: 'claude-3-5-haiku-20241022',
          max_tokens: 150,
          system: SYSTEM_PROMPT,
          messages: [{ role: 'user', content: userMessage }],
        });

        const answer = response.content[0].text;
        console.log(`  A: "${answer.substring(0, 80)}..."`);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ answer }));
      } catch (err) {
        console.error('Error:', err.message);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, () => {
  console.log(`\n  Voice assistant proxy running on http://localhost:${PORT}`);
  console.log(`  Endpoint: POST http://localhost:${PORT}/api/ask`);
  console.log(`  Model: claude-3-5-haiku (fast + cheap)`);
  console.log(`  API key: ...${process.env.ANTHROPIC_API_KEY.slice(-8)}\n`);
});
