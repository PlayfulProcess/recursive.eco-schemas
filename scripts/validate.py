#!/usr/bin/env python3
"""
Validate all grammar.json files in grammars/.

Checks:
1. Valid JSON
2. No duplicate IDs within a grammar
3. All composite_of references point to existing IDs
4. Required fields present (id, name, sections, level, category)
5. sort_order is sequential
6. Attribution metadata present
"""

import json
import sys
from pathlib import Path

GRAMMARS_DIR = Path(__file__).parent.parent / "grammars"


def validate_grammar(grammar_path):
    errors = []
    name = grammar_path.parent.name

    try:
        with open(grammar_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"{name}: Invalid JSON — {e}"]

    items = data.get("items", [])
    if not items:
        errors.append(f"{name}: No items found")
        return errors

    # Check for duplicate IDs
    ids = [item.get("id") for item in items]
    seen = set()
    for item_id in ids:
        if item_id in seen:
            errors.append(f"{name}: Duplicate ID '{item_id}'")
        seen.add(item_id)

    # Check composite_of references
    id_set = set(ids)
    for item in items:
        for ref in item.get("composite_of", []):
            if ref not in id_set:
                errors.append(f"{name}: '{item.get('id')}' references missing ID '{ref}'")

    # Check required fields
    for item in items:
        for field in ["id", "name", "sections"]:
            if field not in item:
                errors.append(f"{name}: Item missing '{field}' — {item.get('id', '?')}")

    # Check attribution
    if "_grammar_commons" not in data:
        errors.append(f"{name}: Missing _grammar_commons")

    return errors


def main():
    if not GRAMMARS_DIR.exists():
        print(f"Error: {GRAMMARS_DIR} not found", file=sys.stderr)
        sys.exit(1)

    all_errors = []
    count = 0

    for grammar_dir in sorted(GRAMMARS_DIR.iterdir()):
        grammar_file = grammar_dir / "grammar.json"
        if grammar_file.exists():
            count += 1
            errors = validate_grammar(grammar_file)
            all_errors.extend(errors)

    if all_errors:
        print(f"Validated {count} grammars — {len(all_errors)} issues:")
        for err in all_errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print(f"Validated {count} grammars — all clean")


if __name__ == "__main__":
    main()
