#!/bin/bash
# Download all 100 Gutenberg books for the recursive.eco library
# Uses Gutenberg's plain text UTF-8 URLs

LIBRARY_DIR="$(dirname "$0")/sources"
GUTENBERG_MIRROR="https://www.gutenberg.org/cache/epub"

download_book() {
  local id="$1"
  local filename="$2"
  local root_dir="$3"
  local target="$LIBRARY_DIR/$root_dir/$filename.txt"

  if [ -f "$target" ]; then
    echo "SKIP: $filename (already exists)"
    return 0
  fi

  # Try UTF-8 plain text first, then ASCII
  local url="$GUTENBERG_MIRROR/$id/pg$id.txt"
  echo "GET: $filename (Gutenberg #$id)"

  if curl -sL --fail -o "$target" "$url"; then
    echo "  OK: $filename"
  else
    # Try alternate URL pattern
    url="https://www.gutenberg.org/files/$id/$id-0.txt"
    if curl -sL --fail -o "$target" "$url"; then
      echo "  OK: $filename (alt URL)"
    else
      url="https://www.gutenberg.org/files/$id/$id.txt"
      if curl -sL --fail -o "$target" "$url"; then
        echo "  OK: $filename (legacy URL)"
      else
        echo "  FAIL: $filename (#$id) — manual download needed"
        rm -f "$target"
      fi
    fi
  fi
}

# ROOT 1: Eastern Wisdom
R="root-01-eastern-wisdom"
download_book 216   "tao-te-ching"              "$R"
download_book 1321  "chuang-tzu"                "$R"
download_book 2388  "bhagavad-gita"             "$R"
download_book 3283  "upanishads"                "$R"
download_book 12894 "sacred-books-east"         "$R"
download_book 17566 "dhammapada"                "$R"
download_book 17    "buddhist-suttas"           "$R"
download_book 769   "book-of-tea"               "$R"
download_book 6519  "songs-of-kabir"            "$R"
download_book 7164  "gitanjali"                 "$R"
download_book 4094  "analects-confucius"        "$R"
download_book 2697  "sayings-of-lao-tzu"        "$R"
download_book 14838 "i-ching"                   "$R"
download_book 35895 "gospel-of-buddha"          "$R"

# ROOT 2: African Cosmology & Diaspora
R="root-02-african-cosmology"
download_book 34655 "folk-stories-southern-nigeria" "$R"
download_book 66923 "west-african-folk-tales"       "$R"
download_book 75833 "fairy-tales-south-africa"      "$R"
download_book 408   "souls-of-black-folk"           "$R"
download_book 15210 "darkwater"                     "$R"
download_book 23    "frederick-douglass"             "$R"
download_book 15399 "olaudah-equiano"               "$R"
download_book 7666  "sojourner-truth"               "$R"
download_book 2376  "up-from-slavery"               "$R"
download_book 15359 "the-negro"                     "$R"

# ROOT 3: Indigenous Mythologies & Enchantment
R="root-03-indigenous-mythology"
download_book 56550 "popol-vuh"                     "$R"
download_book 42390 "myths-north-american-indians"  "$R"
download_book 22083 "myths-legends-great-plains"    "$R"
download_book 22072 "folklore-north-american-indian" "$R"
download_book 5186  "kalevala"                      "$R"
download_book 18947 "prose-edda"                    "$R"
download_book 14727 "celtic-fairy-tales"            "$R"
download_book 7128  "indian-fairy-tales"            "$R"
download_book 49024 "legends-alhambra"              "$R"
download_book 23950 "egyptian-mythology"            "$R"
download_book 3623  "golden-bough"                  "$R"
download_book 21765 "metamorphoses-ovid"            "$R"
download_book 15474 "mahabharata"                   "$R"
download_book 66547 "hawaiian-legends"              "$R"
download_book 12814 "philippine-folk-tales"         "$R"
download_book 4018  "japanese-fairy-tales"          "$R"

# ROOT 4: Mysticism & Contemplative
R="root-04-mysticism"
download_book 20508 "cloud-of-unknowing"            "$R"
download_book 21001 "dark-night-of-the-soul"        "$R"
download_book 52958 "revelations-divine-love"       "$R"
download_book 45060 "interior-castle"               "$R"
download_book 5657  "practice-presence-of-god"      "$R"
download_book 4544  "meister-eckhart-sermons"       "$R"
download_book 1653  "imitation-of-christ"           "$R"
download_book 74203 "essentials-of-mysticism"       "$R"
download_book 58585 "the-prophet"                   "$R"
download_book 5345  "sadhana"                       "$R"

# ROOT 5: Process, Emergence, Dialectics
R="root-05-process-emergence"
download_book 3800  "ethics-spinoza"                "$R"
download_book 5116  "pragmatism"                    "$R"
download_book 621   "varieties-religious-experience" "$R"
download_book 26163 "creative-evolution"            "$R"
download_book 57628 "principles-of-psychology"      "$R"
download_book 4280  "critique-pure-reason"          "$R"
download_book 69808 "phenomenology-of-spirit"       "$R"
download_book 1998  "thus-spoke-zarathustra"        "$R"
download_book 4363  "beyond-good-and-evil"          "$R"
download_book 2680  "meditations-marcus-aurelius"   "$R"
download_book 10661 "discourses-epictetus"          "$R"
download_book 45109 "enchiridion"                   "$R"

# ROOT 6: Emotion, Love, Attachment
R="root-06-emotion-love"
download_book 1227  "expression-of-emotions"        "$R"
download_book 1600  "symposium-plato"               "$R"
download_book 1636  "phaedrus-plato"                "$R"
download_book 47677 "art-of-love-ovid"              "$R"
download_book 2002  "sonnets-from-portuguese"       "$R"
download_book 10900 "song-of-songs"                 "$R"
download_book 3420  "vindication-rights-woman"      "$R"
download_book 158   "emma-austen"                   "$R"
download_book 145   "middlemarch"                   "$R"

# ROOT 7: Freedom, Commons, Cooperation
R="root-07-freedom-commons"
download_book 4341  "mutual-aid"                    "$R"
download_book 34901 "on-liberty"                    "$R"
download_book 147   "common-sense"                  "$R"
download_book 3742  "rights-of-man"                 "$R"
download_book 71    "civil-disobedience"            "$R"
download_book 61    "communist-manifesto"           "$R"
# Book #78 (Two Bits) is CC-licensed, not on Gutenberg — download separately
download_book 608   "areopagitica"                  "$R"

# ROOT 8: Wonder & Children's Stories
R="root-08-wonder-children"
download_book 11    "alice-in-wonderland"           "$R"
download_book 12    "through-the-looking-glass"     "$R"
download_book 16    "peter-pan"                     "$R"
download_book 55    "wonderful-wizard-of-oz"        "$R"
download_book 2591  "grimms-fairy-tales"            "$R"
download_book 1597  "andersens-fairy-tales"         "$R"
download_book 500   "adventures-of-pinocchio"       "$R"
download_book 2781  "just-so-stories"               "$R"
download_book 35997 "jungle-book"                   "$R"
download_book 11339 "aesops-fables"                 "$R"
download_book 74    "tom-sawyer"                    "$R"
download_book 146   "a-little-princess"             "$R"
download_book 113   "secret-garden"                 "$R"
download_book 45    "anne-of-green-gables"          "$R"

# ROOT 9: Ecology & Nature
R="root-09-ecology-nature"
download_book 205   "walden"                        "$R"
download_book 1228  "origin-of-species"             "$R"
download_book 944   "voyage-of-the-beagle"          "$R"
download_book 18852 "life-of-the-bee"               "$R"
download_book 32540 "my-first-summer-in-sierra"     "$R"

# ROOT 10: Self-Knowledge
R="root-10-self-knowledge"
download_book 2944  "essays-emerson"                "$R"
download_book 1322  "leaves-of-grass"               "$R"

echo ""
echo "=== DOWNLOAD COMPLETE ==="
echo "Checking results..."
find "$LIBRARY_DIR" -name "*.txt" | wc -l
echo "text files downloaded"
