#!/bin/bash
# Download all source texts needed for the Bedtime Mythology Series
# Run locally: bash scripts/download-bedtime-seeds.sh
# Then push: git add seeds/ && git commit -m "Add source texts for bedtime mythology series" && git push origin claude/biblical-stories-kids-grammar-N6Nqi

set -e
cd "$(dirname "$0")/.."

echo "=== Downloading source texts for Bedtime Mythology Series ==="
echo ""

# 1. King James Bible (Gutenberg #10) → biblical-stories-kids
if [ ! -f seeds/king-james-bible.txt ]; then
  echo "Downloading King James Bible (#10)..."
  curl -L -o seeds/king-james-bible.txt "https://www.gutenberg.org/cache/epub/10/pg10.txt"
else
  echo "SKIP: seeds/king-james-bible.txt already exists"
fi

# 2. Le Morte d'Arthur by Thomas Malory (Gutenberg #1251) → king-arthur-kids
if [ ! -f seeds/le-morte-darthur.txt ]; then
  echo "Downloading Le Morte d'Arthur (#1251)..."
  curl -L -o seeds/le-morte-darthur.txt "https://www.gutenberg.org/cache/epub/1251/pg1251.txt"
else
  echo "SKIP: seeds/le-morte-darthur.txt already exists"
fi

# 3. The Odyssey by Homer, trans. Samuel Butler (Gutenberg #1727) → homer-kids
if [ ! -f seeds/odyssey-butler.txt ]; then
  echo "Downloading The Odyssey - Butler translation (#1727)..."
  curl -L -o seeds/odyssey-butler.txt "https://www.gutenberg.org/cache/epub/1727/pg1727.txt"
else
  echo "SKIP: seeds/odyssey-butler.txt already exists"
fi

# 4. The Iliad by Homer, trans. Samuel Butler (Gutenberg #6130) → homer-kids
if [ ! -f seeds/iliad-butler.txt ]; then
  echo "Downloading The Iliad - Butler translation (#6130)..."
  curl -L -o seeds/iliad-butler.txt "https://www.gutenberg.org/cache/epub/6130/pg6130.txt"
else
  echo "SKIP: seeds/iliad-butler.txt already exists"
fi

# 5. The Ramayana of Valmiki, trans. Ralph Griffith (Gutenberg #24869) → ramayana-kids
if [ ! -f seeds/ramayana-griffith.txt ]; then
  echo "Downloading The Ramayana - Griffith translation (#24869)..."
  curl -L -o seeds/ramayana-griffith.txt "https://www.gutenberg.org/cache/epub/24869/pg24869.txt"
else
  echo "SKIP: seeds/ramayana-griffith.txt already exists"
fi

# 6. Polynesian Mythology by George Grey (Gutenberg #36678) → polynesian-kids
if [ ! -f seeds/polynesian-mythology-grey.txt ]; then
  echo "Downloading Polynesian Mythology - Grey (#36678)..."
  curl -L -o seeds/polynesian-mythology-grey.txt "https://www.gutenberg.org/cache/epub/36678/pg36678.txt"
else
  echo "SKIP: seeds/polynesian-mythology-grey.txt already exists"
fi

# 7. Australian Legendary Tales by K. Langloh Parker (Gutenberg #3833) → dreamtime-kids
if [ ! -f seeds/australian-legendary-tales.txt ]; then
  echo "Downloading Australian Legendary Tales - Parker (#3833)..."
  curl -L -o seeds/australian-legendary-tales.txt "https://www.gutenberg.org/cache/epub/3833/pg3833.txt"
else
  echo "SKIP: seeds/australian-legendary-tales.txt already exists"
fi

# 8. Egyptian Myth and Legend by Donald Mackenzie (Gutenberg #16653) → egyptian-kids
if [ ! -f seeds/egyptian-myth-legend-mackenzie.txt ]; then
  echo "Downloading Egyptian Myth and Legend - Mackenzie (#16653)..."
  curl -L -o seeds/egyptian-myth-legend-mackenzie.txt "https://www.gutenberg.org/cache/epub/16653/pg16653.txt"
else
  echo "SKIP: seeds/egyptian-myth-legend-mackenzie.txt already exists"
fi

# 9. Hawaiian Legends of Ghosts and Ghost-Gods by Westervelt (Gutenberg #2991) → polynesian-kids (supplement)
if [ ! -f seeds/hawaiian-legends-westervelt.txt ]; then
  echo "Downloading Hawaiian Legends - Westervelt (#2991)..."
  curl -L -o seeds/hawaiian-legends-westervelt.txt "https://www.gutenberg.org/cache/epub/2991/pg2991.txt"
else
  echo "SKIP: seeds/hawaiian-legends-westervelt.txt already exists"
fi

# 10. The Ramayana and the Mahabharata condensed by Oman (Gutenberg #73417) → ramayana-kids (supplement)
if [ ! -f seeds/ramayana-mahabharata-oman.txt ]; then
  echo "Downloading The Ramayana and Mahabharata - Oman (#73417)..."
  curl -L -o seeds/ramayana-mahabharata-oman.txt "https://www.gutenberg.org/cache/epub/73417/pg73417.txt"
else
  echo "SKIP: seeds/ramayana-mahabharata-oman.txt already exists"
fi

echo ""
echo "=== Downloads complete ==="
echo ""
echo "Existing seeds already in repo (no download needed):"
echo "  seeds/prose-edda.txt              → norse-kids"
echo "  seeds/west-african-folk-tales.txt → west-african-kids"
echo "  seeds/popol-vuh.txt               → maya-kids"
echo "  seeds/folk-tales-tibet.txt         → tibetan-dream-kids"
echo "  seeds/book-of-the-dead-egyptian.txt → egyptian-kids (supplement)"
echo ""
echo "To commit and push:"
echo "  git add seeds/"
echo "  git commit -m 'Add source texts for bedtime mythology series (Gutenberg #10, #1251, #1727, #6130, #24869, #36678, #3833, #16653, #2991, #73417)'"
echo "  git push origin claude/biblical-stories-kids-grammar-N6Nqi"
