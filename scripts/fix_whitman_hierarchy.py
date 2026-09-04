"""
Fix the Whitman grammar hierarchy: add parent_id to L1 items based on their
category reference to the phase anchor id. Also add a 'biographical' L2 anchor
so bio items have a proper parent rather than being standalone.
"""
import json
import os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'grammars', 'walt-whitman', 'grammar.json')
PATH = os.path.abspath(PATH)

with open(PATH, encoding='utf-8') as f:
    g = json.load(f)

items = g['items']

# Find phase anchor ids
phase_ids = {it['id'] for it in items if it.get('level') == 2}
print(f'Phase anchors: {phase_ids}')

# Add a biographical L2 anchor if missing
bio_anchor_id = 'biographical'
if not any(it['id'] == bio_anchor_id for it in items):
    bio_anchor = {
        'id': bio_anchor_id,
        'name': 'Biographical Anchors',
        'sort_order': 49,
        'level': 2,
        'category': 'phase',
        'sections': {
            'Phase': 'Life Moments',
            'About': (
                "Six biographical moments that shaped Whitman's writing life. "
                "The Brooklyn printshop of his adolescence. The self-review scandal "
                "of 1855. The Emerson letter and the breach that followed. The Civil "
                "War nursing years. The stroke and the long Camden twilight. The "
                "Deathbed edition he sequenced from his bed. These are not the poems. "
                "These are the conditions under which the poems came."
            ),
            'Reflection': (
                "Which biographical moment in your own life has most decisively "
                "shaped what you write, or are trying to write?"
            )
        },
        'keywords': ['biography', 'life', 'formation'],
        'metadata': {'type': 'phase-anchor'}
    }
    # insert after phase-5 (at position where biographical items start)
    insert_idx = next(
        (i for i, it in enumerate(items) if it.get('category') == 'biographical'),
        len(items)
    )
    items.insert(insert_idx, bio_anchor)
    phase_ids.add(bio_anchor_id)
    print(f'Added biographical L2 anchor at index {insert_idx}')

# For every L1 item, set parent_id = its current category (which references phase id)
fixed = 0
for it in items:
    if it.get('level') == 1:
        cat = it.get('category', '')
        if cat in phase_ids:
            it['parent_id'] = cat
            fixed += 1
        else:
            print(f'WARN: L1 item {it["id"]} has category {cat!r} not in phase_ids')

print(f'Added parent_id to {fixed} L1 items')

# L2 phase anchors: no parent_id, they're root. That's consistent with tattvas schema.

# Write back
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(g, f, indent=2, ensure_ascii=False)
print(f'Wrote {PATH}')
print(f'Total items: {len(items)}')

# Verify
with open(PATH, encoding='utf-8') as f:
    check = json.load(f)
l2 = [it for it in check['items'] if it.get('level') == 2]
l1 = [it for it in check['items'] if it.get('level') == 1]
l1_with_parent = [it for it in l1 if it.get('parent_id')]
print(f'L2 items (roots): {len(l2)}  | L1 items: {len(l1)}  | L1 with parent_id: {len(l1_with_parent)}')
