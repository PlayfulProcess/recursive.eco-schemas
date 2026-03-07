#!/usr/bin/env python3
"""
Generate manifest.json — the characteristica universalis of the grammar library.

Reads every grammar.json in grammars/, extracts metadata, and builds
computed views (by type, by tags, by creator) so the library can be
queried from any perspective without folder hierarchy.

Leibniz would approve: one formal structure, infinite perspectives.
Bayo would approve: no grammar is imprisoned in a single category.
O'Nolan would approve: one command, one output, done.
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict

GRAMMARS_DIR = Path(__file__).parent.parent / "grammars"
OUTPUT = Path(__file__).parent.parent / "manifest.json"


def load_grammar(grammar_path):
    """Load a grammar.json and extract its monad — the metadata that places it in every view."""
    with open(grammar_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    folder_name = grammar_path.parent.name
    item_count = len(data.get("items", []))

    # Extract levels
    levels = set()
    categories = set()
    for item in data.get("items", []):
        if "level" in item:
            levels.add(item["level"])
        if "category" in item:
            categories.add(item["category"])

    return {
        "id": folder_name,
        "name": data.get("name", folder_name),
        "description": data.get("description", ""),
        "grammar_type": data.get("grammar_type", "custom"),
        "creator_name": data.get("creator_name", ""),
        "tags": data.get("tags", []),
        "item_count": item_count,
        "levels": sorted(levels),
        "categories": sorted(categories),
        # Monad fields — these connect grammars to every possible view
        "roots": data.get("roots", []),
        "shelves": data.get("shelves", []),
        "lineages": data.get("lineages", []),
        "worldview": data.get("worldview", ""),
    }


def build_manifest(grammars):
    """Build the manifest — computed views from grammar metadata."""
    by_type = defaultdict(list)
    by_tag = defaultdict(list)
    by_creator = defaultdict(list)
    by_root = defaultdict(list)
    by_shelf = defaultdict(list)
    by_lineage = defaultdict(list)

    for g in grammars:
        gid = g["id"]
        by_type[g["grammar_type"]].append(gid)

        for tag in g["tags"]:
            by_tag[tag].append(gid)

        if g["creator_name"]:
            by_creator[g["creator_name"]].append(gid)

        for root in g.get("roots", []):
            by_root[root].append(gid)

        for shelf in g.get("shelves", []):
            by_shelf[shelf].append(gid)

        for lineage in g.get("lineages", []):
            by_lineage[lineage].append(gid)

    return {
        "generated": True,
        "grammar_count": len(grammars),
        "grammars": {g["id"]: g for g in grammars},
        "views": {
            "by_type": dict(sorted(by_type.items())),
            "by_tag": dict(sorted(by_tag.items())),
            "by_creator": dict(sorted(by_creator.items())),
            "by_root": dict(sorted(by_root.items())),
            "by_shelf": dict(sorted(by_shelf.items())),
            "by_lineage": dict(sorted(by_lineage.items())),
        },
    }


def main():
    if not GRAMMARS_DIR.exists():
        print(f"Error: {GRAMMARS_DIR} not found", file=sys.stderr)
        sys.exit(1)

    grammars = []
    errors = []

    for grammar_dir in sorted(GRAMMARS_DIR.iterdir()):
        grammar_file = grammar_dir / "grammar.json"
        if grammar_file.exists():
            try:
                g = load_grammar(grammar_file)
                grammars.append(g)
            except (json.JSONDecodeError, KeyError) as e:
                errors.append(f"{grammar_dir.name}: {e}")

    if errors:
        print("Warnings:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)

    manifest = build_manifest(grammars)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Generated manifest.json: {manifest['grammar_count']} grammars")
    print(f"  Types: {list(manifest['views']['by_type'].keys())}")
    print(f"  Tags: {len(manifest['views']['by_tag'])} unique tags")
    print(f"  Creators: {list(manifest['views']['by_creator'].keys())}")


if __name__ == "__main__":
    main()
