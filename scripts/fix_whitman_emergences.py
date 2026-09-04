"""
Convert Whitman grammar hierarchy to use the schema's standard emergence
pattern (per recursive.eco-schemas README "Emergence Levels" section):

- Level 1: base items (poems, biographical moments)
- Level 2: emergent groupings with composite_of = [list of L1 ids]

The previous version used parent_id on L1 items pointing UP at L2 phases.
This is backwards from the schema's pattern. The correct pattern: L2
phase-emergences have composite_of pointing DOWN at L1 poems/moments.

Also:
- Remove the non-standard `parent_id` field I added earlier
- Keep `category` as an informational filter label
- Add image_url fields to every item using URLs from the illustration research
"""
import json
import os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'grammars', 'walt-whitman', 'grammar.json')
PATH = os.path.abspath(PATH)

with open(PATH, encoding='utf-8') as f:
    g = json.load(f)

items = g['items']

# Add a biographical L2 emergence if missing (build script doesn't include it)
bio_id = 'biographical'
if not any(it['id'] == bio_id for it in items):
    bio_emergence = {
        'id': bio_id,
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
    insert_idx = next(
        (i for i, it in enumerate(items) if it.get('category') == 'biographical'),
        len(items)
    )
    items.insert(insert_idx, bio_emergence)
    print(f'Added biographical L2 emergence at index {insert_idx}')

# Group L1 items by their category (phase-X or biographical)
children_by_parent = {}
for it in items:
    if it.get('level') == 1:
        cat = it.get('category', '')
        children_by_parent.setdefault(cat, []).append(it['id'])

# Remove parent_id from all items (non-standard)
removed_parent_id = 0
for it in items:
    if 'parent_id' in it:
        del it['parent_id']
        removed_parent_id += 1
print(f'Removed non-standard parent_id from {removed_parent_id} items')

# Add composite_of to L2 phase emergences
added_composite = 0
for it in items:
    if it.get('level') == 2:
        iid = it['id']
        children = children_by_parent.get(iid, [])
        if children:
            it['composite_of'] = children
            added_composite += 1
            print(f'L2 {iid}: composite_of = [{len(children)} items]')

print(f'Added composite_of to {added_composite} L2 emergences')

# ---------------------------------------------------------------------------
# Image URLs from whitman-illustrations-research.md
# Using Wikimedia Commons direct links where available (stable, fast),
# and LoC high-res JPG URLs as alternates. For items without a clear single
# URL, leave empty; sources.md documents the full options.
# ---------------------------------------------------------------------------

image_urls = {
    # Phase I
    "phase-1-eruption": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Walt_Whitman%2C_steel_engraving%2C_July_1854.jpg/800px-Walt_Whitman%2C_steel_engraving%2C_July_1854.jpg",
    "song-of-myself-s1": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Walt_Whitman%2C_steel_engraving%2C_July_1854.jpg/800px-Walt_Whitman%2C_steel_engraving%2C_July_1854.jpg",
    "song-of-myself-s6": "",  # grass/field placeholder — text card
    "song-of-myself-s48": "",
    "song-of-myself-s52": "",
    "there-was-a-child-went-forth": "",

    # Phase II
    "phase-2-body-comrades-sea": "https://tile.loc.gov/image-services/iiif/service:pnp:cwpbh:00700:00752/full/pct:50/0/default.jpg",
    "i-hear-america-singing": "",
    "crossing-brooklyn-ferry": "",
    "when-i-heard-at-close-of-day": "",
    "i-saw-in-louisiana-a-live-oak": "",
    "out-of-the-cradle-endlessly-rocking": "https://nga-download.s3.amazonaws.com/objects/32162-primary-0-nativeres.jpg",  # Audubon Plate 21 Mockingbird
    "as-i-ebb-d-with-the-ocean-of-life": "",

    # Phase III
    "phase-3-drum-taps": "https://tile.loc.gov/image-services/iiif/service:pnp:ppmsca:33000:33750/full/pct:50/0/default.jpg",  # Armory Square Hospital ward
    "beat-beat-drums": "",
    "cavalry-crossing-a-ford": "",
    "the-wound-dresser": "https://tile.loc.gov/image-services/iiif/service:pnp:ppmsca:33000:33750/full/pct:50/0/default.jpg",
    "reconciliation": "",

    # Phase IV
    "phase-4-lincoln": "https://tile.loc.gov/image-services/iiif/service:pnp:ppmsca:19000:19211/full/pct:50/0/default.jpg",  # Brady Lincoln
    "when-lilacs-last": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Curtis%27s_botanical_magazine%2C_or%2C_Flower-garden_displayed_-_in_which_the_most_ornamental_foreign_plants%2C_cultivated_in_the_open_ground%2C_the_green-house%2C_and_the_stove%2C_are_accurately_represented_in_their_%2814797681834%29.jpg/800px-Curtis%27s_botanical_magazine%2C_or%2C_Flower-garden_displayed_-_in_which_the_most_ornamental_foreign_plants%2C_cultivated_in_the_open_ground%2C_the_green-house%2C_and_the_stove%2C_are_accurately_represented_in_their_%2814797681834%29.jpg",
    "o-captain-my-captain": "https://tile.loc.gov/image-services/iiif/service:pnp:ppmsca:19000:19211/full/pct:50/0/default.jpg",
    "darest-thou-now-o-soul": "",

    # Phase V
    "phase-5-late-work": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Thomas_Eakins_-_Portrait_of_Walt_Whitman.jpg/800px-Thomas_Eakins_-_Portrait_of_Walt_Whitman.jpg",
    "noiseless-patient-spider": "",
    "passage-to-india-excerpt": "",
    "song-of-the-open-road": "",
    "so-long": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Thomas_Eakins_-_Portrait_of_Walt_Whitman.jpg/800px-Thomas_Eakins_-_Portrait_of_Walt_Whitman.jpg",

    # Biographical
    "biographical": "https://tile.loc.gov/image-services/iiif/service:pnp:ppmsca:07000:07141/full/pct:50/0/default.jpg",  # Whitman with butterfly 1873
    "bio-brooklyn-printer": "",
    "bio-self-review-scandal": "",
    "bio-emerson-letter": "https://tile.loc.gov/image-services/iiif/service:pnp:pga:04100:04133/full/pct:50/0/default.jpg",  # Emerson Schoff engraving
    "bio-civil-war-nurse": "https://tile.loc.gov/image-services/iiif/service:pnp:ppmsca:57000:57140/full/pct:50/0/default.jpg",  # Nancy Maria Hill
    "bio-stroke-camden": "https://tile.loc.gov/image-services/iiif/service:pnp:hhh:nj0399:photos.066203p/full/pct:50/0/default.jpg",  # Mickle Street house
    "bio-death-deathbed-edition": "https://tile.loc.gov/image-services/iiif/service:pnp:hhh:nj0399:photos.066203p/full/pct:50/0/default.jpg",
}

added_images = 0
for it in items:
    url = image_urls.get(it['id'])
    if url:
        it['image_url'] = url
        added_images += 1
print(f'Added image_url to {added_images} items')

# Set cover image on the grammar itself
g['cover_image_url'] = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Walt_Whitman%2C_steel_engraving%2C_July_1854.jpg/800px-Walt_Whitman%2C_steel_engraving%2C_July_1854.jpg"

# Write back
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(g, f, indent=2, ensure_ascii=False)

# Verify
with open(PATH, encoding='utf-8') as f:
    check = json.load(f)
l2 = [it for it in check['items'] if it.get('level') == 2]
l1 = [it for it in check['items'] if it.get('level') == 1]
l2_with_composite = [it for it in l2 if it.get('composite_of')]
with_images = [it for it in check['items'] if it.get('image_url')]
print(f'\nFinal structure:')
print(f'  L2 emergences: {len(l2)}  | with composite_of: {len(l2_with_composite)}')
print(f'  L1 base items: {len(l1)}')
print(f'  Items with image_url: {len(with_images)}')
print(f'  Cover: {bool(g.get("cover_image_url"))}')
print(f'\nFile size: {os.path.getsize(PATH):,} bytes')
