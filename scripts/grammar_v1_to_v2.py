"""Grammar format v1 -> v2 converter (FORMAT-V2-NODES.md).
usage: python scripts/grammar_v1_to_v2.py <repo_dir> [--dry] [--count-fields] [files...]
Converts every git-tracked *.json that holds a grammar (a dict with an `items` list of dicts).
Also renames catalogue count fields `items` (int) under `grammars[]` / `_sources[]` when --count-fields.
Preserves formatting: exact roundtrip dump if possible, else verified text substitution, else re-dump (flagged).
"""
import json, os, re, subprocess, sys
def LP(p): return chr(92)*2 + "?" + chr(92) + os.path.normpath(os.path.abspath(p))

NODE_RENAMES = {"composite_of": "parts", "ref_document_id": "ref_grammar_id",
                "ref_item_id": "ref_node_id", "item_type": "node_type"}

def rename_key(d, old, new):
    if old not in d: return d
    if new in d: raise ValueError(f"both {old} and {new} present")
    return {(new if k == old else k): v for k, v in d.items()}

def convert_node(n):
    if not isinstance(n, dict): return n
    out = {}
    for k, v in n.items():
        if k == "level": continue
        nk = NODE_RENAMES.get(k, k)
        if nk in out: raise ValueError(f"dup {nk}")
        if k == "category" and v == "edition": v = "selection"
        if k == "metadata" and isinstance(v, dict) and "source_item_id" in v:
            v = rename_key(v, "source_item_id", "source_node_id")
        out[nk] = v
    return out

def is_grammar(d):
    if not (isinstance(d, dict) and isinstance(d.get("items"), list)): return False
    if not d["items"]: return any(k in d for k in ("name", "grammar_type", "sections", "_grammar_commons"))
    return all(isinstance(x, dict) for x in d["items"])

def convert_grammar(d):
    d = rename_key(d, "items", "nodes")
    d["nodes"] = [convert_node(n) for n in d["nodes"]]
    return d

def convert_doc(d, count_fields=False):
    """Returns (new, changed_kind)."""
    kinds = []
    def walk(o, depth):
        if isinstance(o, dict):
            if is_grammar(o):
                kinds.append("grammar")
                return convert_grammar(o)
            new = {}
            for k, v in o.items():
                if count_fields and k in ("grammars", "_sources") and isinstance(v, list):
                    vv = []
                    for e in v:
                        if isinstance(e, dict) and isinstance(e.get("items"), int):
                            e = rename_key(e, "items", "nodes"); kinds.append("count")
                        vv.append(walk(e, depth + 1))
                    new[k] = vv
                else:
                    new[k] = walk(v, depth + 1) if depth < 2 else v
            return new
        if isinstance(o, list) and depth < 2:
            return [walk(x, depth + 1) for x in o]
        return o
    return walk(d, 0), kinds

def detect_params(text):
    lines = text.split("\n")
    indent = None
    if len(lines) > 1:
        m = re.match(r"^( +|\t)", lines[1])
        if m: indent = m.group(1) if m.group(1) == "\t" else len(m.group(1))
    ascii_ = not any(ord(c) > 127 for c in text)
    return indent, ascii_

def dump(obj, indent, ascii_, trailing):
    s = json.dumps(obj, indent=indent, ensure_ascii=ascii_)
    return s + ("\n" if trailing else "")

TEXT_SUBS = [
    (re.compile(r'"items"(\s*:)'), r'"nodes"\1'),
    (re.compile(r'"composite_of"(\s*:)'), r'"parts"\1'),
    (re.compile(r'"ref_document_id"(\s*:)'), r'"ref_grammar_id"\1'),
    (re.compile(r'"ref_item_id"(\s*:)'), r'"ref_node_id"\1'),
    (re.compile(r'"item_type"(\s*:)'), r'"node_type"\1'),
    (re.compile(r'"source_item_id"(\s*:)'), r'"source_node_id"\1'),
    (re.compile(r'("category"\s*:\s*)"edition"'), r'\1"selection"'),
    # level: whole line in pretty files, or inline member
    (re.compile(r'\n[ \t]*"level"\s*:\s*-?\d+(\.\d+)?\s*,(?=\s*\n)'), ''),
    (re.compile(r',\s*\n[ \t]*"level"\s*:\s*-?\d+(\.\d+)?(?=\s*\n[ \t]*\})'), ''),
    (re.compile(r'"level"\s*:\s*-?\d+(\.\d+)?\s*,\s*'), ''),
    (re.compile(r',\s*"level"\s*:\s*-?\d+(\.\d+)?(?=\s*\})'), ''),
]

def convert_file(fp, count_fields=False, write=True):
    raw = open(LP(fp), "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    crlf = "\r\n" in text
    t = text.replace("\r\n", "\n")
    try:
        d = json.loads(t)
    except Exception as e:
        return "unparseable", str(e)[:80]
    new, kinds = convert_doc(d, count_fields)
    if not kinds:
        return "skip", ""
    if json.dumps(new) == json.dumps(d):
        return "skip", "no-change"
    indent, ascii_ = detect_params(t)
    trailing = t.endswith("\n")
    method = None
    if dump(d, indent, ascii_, trailing) == t:
        out = dump(new, indent, ascii_, trailing); method = "dump"
    else:
        ok = False
        for skip in (None, 1, 4, (1, 4)):
            sk = skip if isinstance(skip, tuple) else (skip,)
            out = t
            for i, (rx, rep) in enumerate(TEXT_SUBS):
                if i in sk: continue
                out = rx.sub(rep, out)
            try:
                ok = json.loads(out) == new and list(_keys(json.loads(out))) == list(_keys(new))
            except Exception:
                ok = False
            if ok: break
        if ok: method = "text"
        else:
            out = dump(new, indent, ascii_, trailing); method = "redump"
    if crlf: out = out.replace("\n", "\r\n")
    if write:
        open(LP(fp), "wb").write((b"\xef\xbb\xbf" if bom else b"") + out.encode("utf-8"))
    return method, ",".join(sorted(set(kinds)))

def _keys(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield p + "/" + k
            yield from _keys(v, p + "/" + k)
    elif isinstance(o, list):
        for i, x in enumerate(o): yield from _keys(x, p + f"[{i}]")

if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry" in args; cf = "--count-fields" in args
    args = [a for a in args if not a.startswith("--")]
    repo = args[0]; files = args[1:]
    if not files:
        files = subprocess.run(["git", "ls-files", "*.json"], cwd=repo, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    stats = {}
    for f in files:
        fp = os.path.join(repo, f)
        if not os.path.exists(LP(fp)): print("MISSING", f); continue
        m, k = convert_file(fp, cf, not dry)
        stats.setdefault(m, []).append(f)
        if m not in ("skip",): print(m, k, f)
    print({k: len(v) for k, v in stats.items()})
