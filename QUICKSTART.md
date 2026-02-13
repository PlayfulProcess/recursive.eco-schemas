# Quickstart: Create Your First Grammar

**Time: 15 minutes. No coding required.**

## Option A: Copy and Edit (Fastest)

1. Go to [flow.recursive.eco](https://flow.recursive.eco)
2. Choose Tarot or I Ching, ask a question, draw a card
3. Click "Copy to My Grammars" on the card or deck
4. Sign in when prompted — the grammar appears in your drafts at [offer.recursive.eco](https://offer.recursive.eco)
5. Edit the interpretations, add your images, make it yours
6. Click "Export to Commons" to get the JSON file
7. Add it to your fork of this repo and submit a pull request

## Option B: Create from JSON

1. Fork this repository
2. Copy an example file as your starting point:
   - Tarot: `schemas/tarot/example-fool.json`
   - I Ching: `schemas/iching/example-hexagram-01.json`
   - Astrology: `schemas/astrology/L1-basic.json`
3. Edit the JSON with your own content
4. Test at: `recursive.eco/pages/grammar-viewer.html?github=YOUR-USERNAME/recursive.eco-schemas/path/to/grammar`
5. Submit a pull request when ready

## Option C: AI-Assisted Creation

Best for creating grammars from existing books or texts.

1. Fork this repository
2. Upload your source text to [NotebookLM](https://notebooklm.google.com/) to understand its structure
3. Open your fork in [Claude Code](https://claude.ai/code)
4. Tell Claude: "Create a grammar JSON for [topic] following the format in [example path]"
5. Work in batches of 10-20 items
6. Test and submit

Full walkthrough: [Create Grammars with AI](https://recursive.eco/pages/courses/course-viewer.html?course=create-grammars-with-ai)

## What's Next?

- **Use it in Flow** — Cast readings with your custom grammar
- **Share via Altars** — Offer your grammar to the community at [altars.recursive.eco](https://altars.recursive.eco)
- **Iterate** — Edit and improve based on use
