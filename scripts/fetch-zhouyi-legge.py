"""
Fetch Legge's translation of all 64 hexagrams from sacred-texts.com (Sacred
Books of the East, Volume 16; PD). Emit a single JSON file with judgment +
line texts per hexagram.

Run: python scripts/fetch-zhouyi-legge.py
Output: scripts/zhouyi-legge-raw.json
"""
import json
import re
import sys
import time
import urllib.request
from html import unescape
from pathlib import Path

BASE = "https://sacred-texts.com/ich/ic{:02d}.htm"
INDEX_URL = "https://sacred-texts.com/ich/index.htm"
OUT = Path(__file__).parent / "zhouyi-legge-raw.json"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) recursive-eco-schemas/1.0"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_to_text(html):
    """Remove tags, decode entities, collapse whitespace."""
    html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_clean_names():
    """Scrape sacred-texts index page for canonical (un-letterspaced) Legge
    romanizations. The per-hexagram pages apply CSS letter-spacing to italic
    letters which corrupts text-stripping (e.g. 'Khien' becomes 'Kh ien'),
    but the index page links use clean inline styling.

    Each hexagram appears as: <A HREF="icNN.htm">ROMAN. The NAME Hexagram</A>
    Returns dict: number -> name.
    """
    html = fetch(INDEX_URL)
    out = {}
    # Non-greedy match to </A> so we stay inside one anchor at a time.
    for m in re.finditer(
        r'<A HREF="ic(\d{2})\.htm">(.+?)</A>',
        html,
        flags=re.I | re.S,
    ):
        num = int(m.group(1))
        name_html = m.group(2)
        # Strip inline italic/style tags (e.g. <I>K</I>un -> Kun)
        name = re.sub(r"<[^>]+>", "", name_html)
        name = unescape(name)
        name = re.sub(r"\s+", " ", name).strip()
        # Drop leading roman numeral and "The"
        name = re.sub(r"^[IVXLCDM]+\s*[.:]?\s*The\s+", "", name).strip()
        # Drop trailing "Hexagram"
        name = re.sub(r"\s+Hexagram\s*$", "", name, flags=re.I).strip()
        out[num] = name
    return out


def extract_hexagram(num):
    url = BASE.format(num)
    html = fetch(url)
    text = strip_to_text(html)

    # Title: "ROMAN. THE [NAME] HEXAGRAM" (Roman numeral followed by name and HEXAGRAM)
    # Use a tolerant pattern that captures the name, allowing punctuation/spaces.
    title_match = re.search(
        r"\b[IVXLCDM]+\s*[.:]?\s*THE\s+(.+?)\s+HEXAGRAM",
        text,
    )
    name = title_match.group(1).strip() if title_match else None

    # Format observation: after "HEXAGRAM" Legge's text continues with the
    # judgment, then numbered line texts (" 1. ", " 2. ", ..., " 6. ", and
    # for hex 1/2 a supernumerary " 7. ").  Hex 1 also has explanatory
    # preamble/trailer ("Explanation of the entire figure by king Wăn"
    # before, "Explanation of the separate lines by the duke of K âu."
    # between judgment and lines).  Strip those if present.
    judgment = None
    lines = []
    if "HEXAGRAM" in text:
        after_title = text.split("HEXAGRAM", 1)[1]
        # End of the page: usually "Footnotes" or "Next" trailer
        for stop_marker in ["Footnotes", "Next "]:
            if stop_marker in after_title:
                after_title = after_title.split(stop_marker, 1)[0]
                break
        # Find first numbered line marker " 1. " or " I. " (some pages have OCR'd Roman I)
        first_line_match = re.search(r"\s1\.\s+", after_title) or re.search(
            r"\sI\.\s+The first", after_title
        )
        if first_line_match:
            j_chunk = after_title[: first_line_match.start()].strip()
            l_block = after_title[first_line_match.start() :].strip()

            # Strip optional preamble ("Explanation of the entire figure by king W{name}")
            j_chunk = re.sub(
                r"^\s*Explanation of the entire figure by king W\S*\s*",
                "",
                j_chunk,
                flags=re.I,
            ).strip()
            # Strip optional trailer (between judgment and lines, hex 1 only)
            j_chunk = re.sub(
                r"\s*Explanation of the separate lines by the duke of K\s+\S+\.?\s*$",
                "",
                j_chunk,
                flags=re.I,
            ).strip()
            # Strip page markers
            j_chunk = re.sub(r"\s*p\.\s*\d+\s*", " ", j_chunk).strip()
            j_chunk = re.sub(r"\s+", " ", j_chunk)
            judgment = j_chunk if j_chunk else None

            # Handle digit markers and the occasional Roman "I." for line 1.
            pieces = re.findall(
                r"(\d+|I)\.\s+(.+?)(?=\s+(?:\d+|I)\.\s+|\s*$)",
                l_block,
                flags=re.S,
            )
            seen = set()
            for n_str, body in pieces:
                n = 1 if n_str == "I" else int(n_str)
                if n in seen or n < 1 or n > 7:
                    continue
                body = re.sub(r"\bp\.\s*\d+\b", "", body).strip()
                body = re.sub(r"\s+", " ", body)
                if not body:
                    continue
                seen.add(n)
                lines.append({"n": n, "text": body})
            lines.sort(key=lambda x: x["n"])

    return {
        "number": num,
        "name": name,
        "judgment": judgment,
        "lines": lines,
        "source_url": url,
    }


def main():
    print("  fetching clean names from index...", file=sys.stderr, flush=True)
    clean_names = fetch_clean_names()
    print(f"    got {len(clean_names)} clean names", file=sys.stderr)
    out = []
    for n in range(1, 65):
        print(f"  fetching {n:>2}/64...", file=sys.stderr, flush=True)
        try:
            data = extract_hexagram(n)
            data["clean_name"] = clean_names.get(n)
        except Exception as e:
            print(f"    ERROR on {n}: {e}", file=sys.stderr)
            data = {
                "number": n,
                "name": None,
                "judgment": None,
                "lines": [],
                "clean_name": clean_names.get(n),
                "error": str(e),
                "source_url": BASE.format(n),
            }
        out.append(data)
        time.sleep(0.3)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT} with {len(out)} hexagrams", file=sys.stderr)
    missing_titles = sum(1 for h in out if not h["name"])
    missing_judgments = sum(1 for h in out if not h["judgment"])
    avg_lines = sum(len(h["lines"]) for h in out) / len(out)
    print(f"  missing titles: {missing_titles}", file=sys.stderr)
    print(f"  missing judgments: {missing_judgments}", file=sys.stderr)
    print(f"  avg lines per hexagram: {avg_lines:.2f}", file=sys.stderr)


if __name__ == "__main__":
    main()
