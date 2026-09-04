# Previews

Interactive HTML visualizations for grammars in this repository. Each file is a self-contained single-page app — open it in any browser.

## Available Previews

### Grammar Playground (`index.html`)

A general-purpose browser for any grammar in the repository. Loads grammar.json files and lets you explore items, filter by level/category, and draw random cards.

### I Ching Explorer (`iching-explorer.html`)

A Leibniz Binary Hypercube visualization of all 64 hexagrams. Features:

- **8x8 trigram grid** — upper trigrams as columns, lower as rows
- **Relationship overlays** — toggle inverse, complement, nuclear, King Wen pairs, Zagua pairs
- **Line-change neighbors** — click any hexagram to see which hexagrams are one line-flip away
- **Palace coloring** — Eight Palaces (Ba Gong) grouping
- **Detail panel** — Judgment, Image, line texts from the Chinese Original grammar
- **Keyboard navigation** — arrow keys to move, number keys for layers

Data is drawn from two grammars:
- `grammars/i-ching-leibniz-binary/` — structure, relationships, binary encodings
- `grammars/i-ching-chinese-original-with-brief-translation/` — classical line texts

## How to Preview

### Quick — just open the HTML

```bash
# From the repo root:
open previews/index.html              # Grammar Playground
open previews/iching-explorer.html    # I Ching Explorer
```

On Linux use `xdg-open` instead of `open`. On Windows use `start`.

### With a local server (recommended for development)

```bash
# Python's built-in server, from the repo root:
python3 -m http.server 8000 --directory previews

# Then open http://localhost:8000 in your browser
# - http://localhost:8000/index.html           → Grammar Playground
# - http://localhost:8000/iching-explorer.html → I Ching Explorer
```

### Rebuilding I Ching visualization data

If you modify the I Ching grammars, regenerate `viz-data.json`:

```bash
python3 previews/build_viz_data.py
```

This reads from `grammars/i-ching-leibniz-binary/grammar.json` and `grammars/i-ching-chinese-original-with-brief-translation/grammar.json`, producing a compact 73KB JSON file with all 64 hexagrams, 8 trigrams, relationship data, and line texts.
