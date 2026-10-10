"""Depth of a grammar node, computed from `parts` (grammar format v2).

v2 stores no `level`: a node with no parts has depth 1; otherwise its depth is
1 + the deepest of its parts. Cycle-safe. Used by the build scripts in this
folder wherever they used to read `item["level"]`.

    from grammar_depth import node_depth
    l2 = [n for n in nodes if node_depth(n, nodes) == 2]
"""

_index_cache = {}


def _index(nodes):
    """id -> node map for a nodes list (cached while the list keeps its length)."""
    key = id(nodes)
    hit = _index_cache.get(key)
    if hit is not None and hit[0] is nodes and hit[1] == len(nodes):
        return hit[2]
    by_id = {n.get("id"): n for n in nodes if isinstance(n, dict)}
    _index_cache[key] = (nodes, len(nodes), by_id)
    return by_id


def node_depth(node, nodes, _seen=None):
    """Depth from parts: no parts -> 1, else 1 + the deepest part."""
    parts = node.get("parts") if isinstance(node, dict) else None
    if not parts:
        return 1
    by_id = nodes if isinstance(nodes, dict) else _index(nodes)
    seen = _seen if _seen is not None else set()
    nid = node.get("id")
    if nid in seen:
        return 1
    seen.add(nid)
    d = 1
    for pid in parts:
        child = by_id.get(pid)
        if child is not None:
            d = max(d, 1 + node_depth(child, by_id, seen))
    seen.discard(nid)
    return d
