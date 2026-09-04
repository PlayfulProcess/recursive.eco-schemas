"""
Build grammars/zhouyi-legge/grammar.json by combining:
  - scripts/zhouyi-legge-raw.json — Legge's English judgment + line texts
  - grammars/i-ching-chinese-original-with-brief-translation/grammar.json
    — for Chinese metadata (pinyin, chinese_name, trigrams, binary, symbol)

Run: python scripts/build-zhouyi-grammar.py
Output: grammars/zhouyi-legge/grammar.json
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW = ROOT / "scripts" / "zhouyi-legge-raw.json"
META_SOURCE = (
    ROOT
    / "grammars"
    / "i-ching-chinese-original-with-brief-translation"
    / "grammar.json"
)
OUT = ROOT / "grammars" / "zhouyi-legge" / "grammar.json"


def fix_buggy_romanization(text, raw_name, clean_name):
    """The judgment text on sacred-texts.com pages opens with the romanized
    hexagram name carrying the same letterspacing artifact as the title
    (e.g. 'Kh ien (represents)...', 'K ung Fû (moves even)...'). The raw_name
    captures the buggy spacing exactly (in uppercase). Build a case-
    insensitive regex from raw_name's word structure and replace with the
    clean form."""
    if not text or not clean_name or not raw_name:
        return text
    parts = raw_name.strip().split()
    if not parts:
        return text
    # Match the same word structure with arbitrary case and \s+ between tokens
    pattern = r"\b" + r"\s+".join(re.escape(p) for p in parts) + r"\b"
    try:
        return re.sub(pattern, clean_name, text, flags=re.I)
    except re.error:
        return text


def main():
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    meta_grammar = json.loads(META_SOURCE.read_text(encoding="utf-8"))
    meta_by_number = {item["metadata"]["number"]: item for item in meta_grammar["items"]}

    items = []
    for h in raw:
        n = h["number"]
        meta = meta_by_number.get(n, {})
        m = meta.get("metadata", {})
        chinese_sections = (meta.get("sections") or {})

        clean_name = h.get("clean_name") or h["name"]
        raw_name = h["name"]

        # Fix the letterspacing artifact in the judgment text
        judgment_fixed = fix_buggy_romanization(h["judgment"], raw_name, clean_name)

        # Standard section names — match what the oracle reader expects so
        # cast-and-read flow works (Judgment, Line 1..Line 6, Use of Nine,
        # Use of Six). Legge's English fills these.
        sections = {"Judgment": judgment_fixed}
        for L in h["lines"]:
            n_line = L["n"]
            if n == 1 and n_line == 7:
                en_label = "Use of Nine"
            elif n == 2 and n_line == 7:
                en_label = "Use of Six"
            else:
                en_label = f"Line {n_line}"
            sections[en_label] = fix_buggy_romanization(L["text"], raw_name, clean_name)

        # Chinese original — single consolidated reference section, never
        # touched by the oracle reader's line-by-line interaction. Format:
        # one labeled paragraph per piece, in Zhouyi reading order.
        chinese_parts = []
        cj = chinese_sections.get("Judgment")
        if cj:
            chinese_parts.append(f"判 (Judgment): {cj}")
        for L in h["lines"]:
            n_line = L["n"]
            ch_line = chinese_sections.get(f"Line {n_line}")
            if not ch_line:
                continue
            if n == 1 and n_line == 7:
                label = "用九 (Use of Nine)"
            elif n == 2 and n_line == 7:
                label = "用六 (Use of Six)"
            else:
                label = f"Line {n_line}"
            chinese_parts.append(f"{label}: {ch_line}")
        if chinese_parts:
            sections["Chinese Original (Reference)"] = "\n\n".join(chinese_parts)

        items.append({
            "id": f"hexagram-{n}",
            "name": meta.get("name") or clean_name or f"Hexagram {n}",
            "level": 1,
            "sort_order": n - 1,
            "category": "trigram",
            "subcategory": m.get("subcategory") or "",
            "symbol": meta.get("symbol", ""),
            "keywords": [],
            "metadata": {
                "number": n,
                "binary": m.get("binary", ""),
                "pinyin": m.get("pinyin", ""),
                "chinese_name": m.get("chinese_name", ""),
                "trigram_above": m.get("trigram_above", ""),
                "trigram_below": m.get("trigram_below", ""),
                "legge_romanization": clean_name,
                "legge_romanization_raw": raw_name,
                "source_url": h["source_url"],
            },
            "sections": sections,
            "questions": [],
            "grammar_type": "iching",
        })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "James Legge (translator)",
                    "date": "1882",
                    "note": "The Yi King, Sacred Books of the East Volume 16. Public domain. Source: sacred-texts.com/ich/",
                }
            ],
        },
        "name": "Zhouyi (Legge translation)",
        "description": (
            "The Zhouyi (周易, 'Changes of Zhou') is the older oracle layer "
            "underneath the I Ching — judgment texts (attributed to King "
            "Wen, ~1100 BCE) and line texts (attributed to the Duke of "
            "Zhou) only. Each hexagram has one judgment and six short, "
            "often cryptic line statements. That is the entire Zhouyi: "
            "a divination manual you cast for an answer.\n\n"
            "Over the next ~700 years (5th to 2nd century BCE), Confucian "
            "scholars added seven philosophical commentaries — counted as "
            "the Ten Wings (十翼, Shi Yi) because three are split into two "
            "halves — that turned the oracle into a wisdom classic to "
            "study and live by:\n\n"
            "1. Tuàn Zhuàn (彖傳) — Commentary on the Judgments\n"
            "2. Xiàng Zhuàn (象傳) — Commentary on the Images (Big Image "
            "gives moral lessons; Small Image comments on each line)\n"
            "3. Xì Cí Zhuàn / Dà Zhuàn (繫辭傳) — Great Treatise: the "
            "philosophical heart, source of most yin/yang cosmology\n"
            "4. Wén Yán (文言) — Words on the Text: extended commentary on "
            "hexagrams 1 and 2\n"
            "5. Shuō Guà (說卦) — Discussion of the Trigrams (heaven, "
            "thunder, mountain, etc.)\n"
            "6. Xù Guà (序卦) — Sequence of the Hexagrams: why they're in "
            "this order\n"
            "7. Zá Guà (雜卦) — Miscellaneous Notes: short paired "
            "contrasts\n\n"
            "Most of what English-speaking readers associate with 'I Ching "
            "philosophy' — the junzi (superior man) moralism, the "
            "cosmological schema, the trigram correspondences — is from "
            "the Wings, not the Zhouyi. The Wilhelm/Baynes translation "
            "that defined English-language reception integrates the Wings "
            "throughout. By contrast this grammar restricts itself to the "
            "bare pre-Confucian oracle: more direct, more shamanic, less "
            "philosophically elaborated — closer to how the text was used "
            "in early Zhou-dynasty China.\n\n"
            "Source: James Legge's 1882 English translation (Sacred Books "
            "of the East, Volume 16), public domain, paired with the "
            "original Chinese for each judgment and line. For a "
            "contemporary commentary in this Zhouyi register, see Liu "
            "Ming's 'Changing: Zhouyi: The Heart of the Yijing' "
            "(separately published, not included here). For the full "
            "Yijing with the Ten Wings, see the other I Ching grammars in "
            "this library — particularly i-ching-chinese-original-with-"
            "brief-translation, which includes the Xiàng (Image) "
            "commentary."
        ),
        "creator_name": "PlayfulProcess",
        "grammar_type": "iching",
        "tags": ["i-ching", "zhouyi", "legge", "public-domain", "oracle", "chinese"],
        "roots": ["eastern-wisdom"],
        "shelves": ["wisdom"],
        "lineages": [],
        "worldview": "non-dual",
        "items": items,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(grammar, indent=2, ensure_ascii=False), encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT} ({size_kb:.1f} KB, {len(items)} hexagrams)")


if __name__ == "__main__":
    main()
