#!/usr/bin/env python3
"""
Extract compact visualization data from I Ching grammars.

Produces a JSON object with:
- 64 hexagram records (metadata + all 7 relationship fields)
- 8 trigram records
- Line texts from the Chinese Original grammar
- Suitable for embedding in the iching-explorer.html
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(SCRIPT_DIR, "..")
LEIBNIZ_GRAMMAR = os.path.join(
    REPO_ROOT, "grammars", "i-ching-leibniz-binary", "grammar.json"
)
CHINESE_GRAMMAR = os.path.join(
    REPO_ROOT, "grammars", "i-ching-chinese-original-with-brief-translation", "grammar.json"
)
OUTPUT = os.path.join(SCRIPT_DIR, "viz-data.json")


def main():
    leibniz = json.load(open(LEIBNIZ_GRAMMAR, encoding="utf-8"))
    chinese = json.load(open(CHINESE_GRAMMAR, encoding="utf-8"))

    # Build Chinese line text lookup: number → {Line 1..6, Judgment, Image}
    chinese_texts = {}
    for item in chinese["items"]:
        num = item["metadata"]["number"]
        texts = {}
        for key in ["Judgment", "Image", "Line 1", "Line 2", "Line 3",
                     "Line 4", "Line 5", "Line 6"]:
            if key in item["sections"]:
                texts[key] = item["sections"][key]
        chinese_texts[num] = texts

    # Extract trigrams
    trigrams = []
    for item in leibniz["items"]:
        if item["level"] == 2:
            trigrams.append({
                "id": item["id"],
                "name": item["name"],
                "symbol": item.get("symbol", ""),
                "binary": item["metadata"]["binary"],
                "leibniz": item["metadata"]["leibniz_number"],
                "chinese": item["metadata"]["chinese_name"],
                "pinyin": item["metadata"]["pinyin"],
                "element": item["metadata"].get("element", ""),
                "family": item["metadata"].get("family_role", ""),
            })

    # Extract hexagrams
    hexagrams = []
    for item in leibniz["items"]:
        if item["level"] != 3:
            continue
        m = item["metadata"]
        num = m["number"]
        h = {
            "num": num,
            "name": item["name"],
            "id": item["id"],
            "symbol": item.get("symbol", ""),
            "binary": m["binary"],
            "leibniz": m["leibniz_number"],
            "chinese": m["chinese_name"],
            "pinyin": m.get("pinyin", ""),
            "lower_trigram": m["lower_trigram"],
            "upper_trigram": m["upper_trigram"],
            "lower_trigram_name": m["lower_trigram_name"],
            "upper_trigram_name": m["upper_trigram_name"],
            # Relationships
            "inverse_num": int(m["inverse_id"].split("-")[1]),
            "is_palindrome": m["is_palindrome"],
            "complement_num": int(m["complement_id"].split("-")[1]),
            "nuclear_num": int(m["nuclear_id"].split("-")[1]),
            "kw_pair_num": int(m["king_wen_pair_id"].split("-")[1]),
            "palace": m["palace"],
            "palace_pos": m["palace_position"],
            "palace_pos_name": m["palace_position_name"],
            "mawangdui": m["mawangdui_position"],
            "zagua_pair_num": int(m["zagua_pair_id"].split("-")[1]),
            "zagua_char": m.get("zagua_characterization", ""),
            # Sections from Leibniz grammar
            "judgment": item["sections"].get("Judgment", ""),
            "image": item["sections"].get("Image", ""),
            "trigrams_desc": item["sections"].get("Trigrams", ""),
        }
        # Add Chinese line texts
        ct = chinese_texts.get(num, {})
        for i in range(1, 7):
            h[f"line{i}"] = ct.get(f"Line {i}", "")
        if ct.get("Judgment"):
            h["judgment_chinese"] = ct["Judgment"]
        if ct.get("Image"):
            h["image_chinese"] = ct["Image"]
        hexagrams.append(h)

    # Sort by King Wen number
    hexagrams.sort(key=lambda x: x["num"])

    # Compute line-change neighbors for each hexagram (by binary)
    binary_to_num = {h["binary"]: h["num"] for h in hexagrams}
    for h in hexagrams:
        neighbors = []
        b = h["binary"]
        for line_pos in range(6):
            bits = list(b)
            bits[line_pos] = "0" if bits[line_pos] == "1" else "1"
            new_bin = "".join(bits)
            neighbors.append(binary_to_num[new_bin])
        h["neighbors"] = neighbors  # neighbors[0] = flip line 1, etc.

    viz_data = {
        "trigrams": trigrams,
        "hexagrams": hexagrams,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(viz_data, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"✓ Visualization data written to {OUTPUT}")
    print(f"  {len(trigrams)} trigrams, {len(hexagrams)} hexagrams")
    print(f"  {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
