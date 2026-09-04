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

# 2. Le Morte d'Arthur by Thomas Malory — Vol 1 (#1251) + Vol 2 (#1252) → king-arthur-kids
if [ ! -f seeds/le-morte-darthur-vol1.txt ]; then
  echo "Downloading Le Morte d'Arthur Vol 1 (#1251)..."
  curl -L -o seeds/le-morte-darthur-vol1.txt "https://www.gutenberg.org/cache/epub/1251/pg1251.txt"
else
  echo "SKIP: seeds/le-morte-darthur-vol1.txt already exists"
fi
if [ ! -f seeds/le-morte-darthur-vol2.txt ]; then
  echo "Downloading Le Morte d'Arthur Vol 2 (#1252)..."
  curl -L -o seeds/le-morte-darthur-vol2.txt "https://www.gutenberg.org/cache/epub/1252/pg1252.txt"
else
  echo "SKIP: seeds/le-morte-darthur-vol2.txt already exists"
fi

# 3. The Odyssey by Homer, trans. Samuel Butler (Gutenberg #1727) → homer-kids
if [ ! -f seeds/odyssey-butler.txt ]; then
  echo "Downloading The Odyssey - Butler translation (#1727)..."
  curl -L -o seeds/odyssey-butler.txt "https://www.gutenberg.org/cache/epub/1727/pg1727.txt"
else
  echo "SKIP: seeds/odyssey-butler.txt already exists"
fi

# 4. The Iliad by Homer, trans. Samuel Butler (Gutenberg #2199) → homer-kids
if [ ! -f seeds/iliad-butler.txt ]; then
  echo "Downloading The Iliad - Butler prose translation (#2199)..."
  curl -L -o seeds/iliad-butler.txt "https://www.gutenberg.org/cache/epub/2199/pg2199.txt"
else
  echo "SKIP: seeds/iliad-butler.txt already exists"
fi

# 5. The Ramayana of Valmiki, trans. Ralph Griffith (Gutenberg #24869) → ramayana-kids
if [ ! -f seeds/ramayana-griffith.txt ]; then
  echo "Downloading The Ramayana - Griffith verse translation (#24869)..."
  curl -L -o seeds/ramayana-griffith.txt "https://www.gutenberg.org/cache/epub/24869/pg24869.txt"
else
  echo "SKIP: seeds/ramayana-griffith.txt already exists"
fi

# 6. The Ramayana and the Mahabharata condensed by Oman (Gutenberg #73417) → ramayana-kids (supplement)
if [ ! -f seeds/ramayana-mahabharata-oman.txt ]; then
  echo "Downloading The Ramayana and Mahabharata - Oman (#73417)..."
  curl -L -o seeds/ramayana-mahabharata-oman.txt "https://www.gutenberg.org/cache/epub/73417/pg73417.txt"
else
  echo "SKIP: seeds/ramayana-mahabharata-oman.txt already exists"
fi

# 7. Australian Legendary Tales by K. Langloh Parker (Gutenberg #3833) → dreamtime-kids
if [ ! -f seeds/australian-legendary-tales.txt ]; then
  echo "Downloading Australian Legendary Tales - Parker (#3833)..."
  curl -L -o seeds/australian-legendary-tales.txt "https://www.gutenberg.org/cache/epub/3833/pg3833.txt"
else
  echo "SKIP: seeds/australian-legendary-tales.txt already exists"
fi

# 8. Myths and Legends of Ancient Egypt by Lewis Spence (Gutenberg #43662) → egyptian-kids
#    (Mackenzie's Egyptian Myth & Legend is NOT on Gutenberg — #16653 is his Babylonia book)
if [ ! -f seeds/myths-legends-egypt-spence.txt ]; then
  echo "Downloading Myths and Legends of Ancient Egypt - Spence (#43662)..."
  curl -L -o seeds/myths-legends-egypt-spence.txt "https://www.gutenberg.org/cache/epub/43662/pg43662.txt"
else
  echo "SKIP: seeds/myths-legends-egypt-spence.txt already exists"
fi

# 9. Hawaiian Legends of Ghosts and Ghost-Gods by Westervelt (Gutenberg #39195) → polynesian-kids
if [ ! -f seeds/hawaiian-legends-westervelt.txt ]; then
  echo "Downloading Hawaiian Legends of Ghosts and Ghost-Gods - Westervelt (#39195)..."
  curl -L -o seeds/hawaiian-legends-westervelt.txt "https://www.gutenberg.org/cache/epub/39195/pg39195.txt"
else
  echo "SKIP: seeds/hawaiian-legends-westervelt.txt already exists"
fi

# 10. Legends of Ma-ui by Westervelt (Gutenberg #32601) → polynesian-kids (Maui stories)
if [ ! -f seeds/legends-of-maui-westervelt.txt ]; then
  echo "Downloading Legends of Ma-ui - Westervelt (#32601)..."
  curl -L -o seeds/legends-of-maui-westervelt.txt "https://www.gutenberg.org/cache/epub/32601/pg32601.txt"
else
  echo "SKIP: seeds/legends-of-maui-westervelt.txt already exists"
fi

# 11. West African Folk-Tales by Barker & Sinclair (Gutenberg #66923) → west-african-kids (supplement)
if [ ! -f seeds/west-african-folk-tales-barker.txt ]; then
  echo "Downloading West African Folk-Tales - Barker & Sinclair (#66923)..."
  curl -L -o seeds/west-african-folk-tales-barker.txt "https://www.gutenberg.org/cache/epub/66923/pg66923.txt"
else
  echo "SKIP: seeds/west-african-folk-tales-barker.txt already exists"
fi

# 12. Folk Stories from Southern Nigeria by Dayrell (Gutenberg #34655) → west-african-kids (supplement)
if [ ! -f seeds/folk-stories-southern-nigeria.txt ]; then
  echo "Downloading Folk Stories from Southern Nigeria - Dayrell (#34655)..."
  curl -L -o seeds/folk-stories-southern-nigeria.txt "https://www.gutenberg.org/cache/epub/34655/pg34655.txt"
else
  echo "SKIP: seeds/folk-stories-southern-nigeria.txt already exists"
fi

# 13. The Poetic Edda / Elder Eddas (Gutenberg #14726) → norse-kids (supplement to prose-edda)
if [ ! -f seeds/poetic-edda.txt ]; then
  echo "Downloading The Poetic Edda / Elder Eddas (#14726)..."
  curl -L -o seeds/poetic-edda.txt "https://www.gutenberg.org/cache/epub/14726/pg14726.txt"
else
  echo "SKIP: seeds/poetic-edda.txt already exists"
fi

echo ""
echo "=== Downloads complete ==="
echo ""
echo "Existing seeds already in repo (no download needed):"
echo "  seeds/prose-edda.txt                → norse-kids (primary)"
echo "  seeds/west-african-folk-tales.txt   → west-african-kids (primary)"
echo "  seeds/popol-vuh.txt                 → maya-kids"
echo "  seeds/folk-tales-tibet.txt          → tibetan-dream-kids"
echo "  seeds/book-of-the-dead-egyptian.txt → egyptian-kids (supplement)"
echo ""
echo "NOTE: No Gutenberg source for:"
echo "  - Polynesian Mythology by George Grey (not digitized on Gutenberg)"
echo "  - Tibetan Book of the Dead (likely still under copyright)"
echo "  Using Westervelt's Hawaiian legends + Maui legends for Polynesian."
echo "  Using folk-tales-tibet.txt for Tibetan (dream yoga is mostly oral tradition)."
echo ""
echo "To commit and push:"
echo "  git add seeds/"
echo "  git commit -m 'Add source texts for bedtime mythology series (Gutenberg #10, #1251, #1252, #1727, #2199, #24869, #73417, #3833, #43662, #39195, #32601, #66923, #34655, #14726)'"
echo "  git push origin claude/biblical-stories-kids-grammar-N6Nqi"
