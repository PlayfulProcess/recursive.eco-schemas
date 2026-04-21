"""
Add proper illustration metadata (following Alice grammar pattern) to every
Whitman grammar item that has an image. Preserves the image_url field for
viewer compatibility but also adds structured metadata.illustrations[] with
artist, dates, edition/source, license, and attribution.

Matches the pattern in grammars/alice-in-wonderland-chapter-book/grammar.json.
"""
import json
import os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'grammars', 'walt-whitman', 'grammar.json')
PATH = os.path.abspath(PATH)

with open(PATH, encoding='utf-8') as f:
    g = json.load(f)

# Illustration metadata per item id
# Uses direct Wikimedia / LoC URLs (not R2) — recursive.eco renders them fine
ILLUSTRATIONS = {
    # Phase anchors
    "phase-1-eruption": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Walt%20Whitman,%20steel%20engraving,%20July%201854.jpg?width=1200",
        "artist": "Samuel Hollyer",
        "artist_dates": "1826-1919",
        "edition": "Frontispiece, Leaves of Grass 1st ed., 1855",
        "source": "After Gabriel Harrison daguerreotype, July 1854",
        "scene": "Walt Whitman in work shirt — the iconic frontispiece of the 1855 first edition",
        "license": "Public Domain",
        "license_note": "Engraving published 1855; Hollyer d. 1919; PD worldwide",
        "rights_holder": "Wikimedia Commons (File:Walt Whitman, steel engraving, July 1854.jpg)",
        "is_primary": True
    }],
    "phase-2-body-comrades-sea": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/cwpbh/00700/00752v.jpg",
        "artist": "Mathew Brady",
        "artist_dates": "c.1823-1896",
        "edition": "Brady's National Photographic Portrait Gallery",
        "source": "Library of Congress, Prints & Photographs Division",
        "scene": "Walt Whitman, c.1862 studio portrait",
        "license": "Public Domain",
        "license_note": "Brady d. 1896; photograph pre-1870; LoC states no known restrictions",
        "rights_holder": "Library of Congress (LC-DIG-cwpbh-00752)",
        "is_primary": True
    }],
    "phase-3-drum-taps": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/ppmsca/33700/33750v.jpg",
        "artist": "Unknown photographer",
        "artist_dates": "1862-1865 activity",
        "edition": "Civil War Hospital Photographs",
        "source": "Library of Congress, Prints & Photographs Division",
        "scene": "A ward at Armory Square Hospital, Washington, DC — one of the hospitals where Whitman served as volunteer nurse",
        "license": "Public Domain",
        "license_note": "Pre-1929 publication; LoC no known restrictions",
        "rights_holder": "Library of Congress (LC-DIG-ppmsca-33750)",
        "is_primary": True
    }],
    "phase-4-lincoln": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/ppmsca/19200/19211v.jpg",
        "artist": "Mathew Brady",
        "artist_dates": "c.1823-1896",
        "edition": "Brady Washington studio portrait",
        "source": "Library of Congress, Prints & Photographs Division",
        "scene": "Abraham Lincoln, January 8, 1864 — the iconic seated portrait",
        "license": "Public Domain",
        "license_note": "Brady d. 1896; photograph 1864; LoC no known restrictions",
        "rights_holder": "Library of Congress (LC-DIG-ppmsca-19211)",
        "is_primary": True
    }],
    "phase-5-late-work": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/ppmsca/07100/07141v.jpg",
        "artist": "Phillips & Taylor Studio, Philadelphia",
        "artist_dates": "1873",
        "edition": "Whitman with butterfly (cardboard prop)",
        "source": "Library of Congress, Prints & Photographs Division",
        "scene": "Whitman with butterfly, 1873 — whimsical Camden-era portrait",
        "license": "Public Domain",
        "license_note": "Pre-1929; LoC no known restrictions",
        "rights_holder": "Library of Congress (LC-DIG-ppmsca-07141)",
        "is_primary": True
    }],
    "biographical": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Walt%20Whitman,%20steel%20engraving,%20July%201854.jpg?width=1200",
        "artist": "Samuel Hollyer after Gabriel Harrison",
        "artist_dates": "1826-1919",
        "edition": "Frontispiece, Leaves of Grass 1st ed., 1855",
        "source": "Wikimedia Commons",
        "scene": "The 1855 frontispiece — the face Whitman chose for posterity",
        "license": "Public Domain",
        "is_primary": True
    }],

    # Poems with direct Whitman-linked pairings
    "song-of-myself-s1": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Jean-Fran%C3%A7ois_Millet_-_The_Sower_-_Walters_37905.jpg?width=1200",
        "artist": "Jean-François Millet",
        "artist_dates": "1814-1875",
        "edition": "The Sower (Le Semeur), 1850",
        "source": "Walters Art Museum, Baltimore",
        "scene": "Millet's Sower — Whitman's favorite painter; Whitman said Leaves of Grass was his 'own born brother' to Millet's peasant paintings",
        "license": "Public Domain",
        "license_note": "Millet d. 1875; painting pre-1929; PD worldwide",
        "rights_holder": "Walters Art Museum (CC0)",
        "is_primary": True
    }],
    "song-of-myself-s6": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg?width=1200",
        "artist": "Jean-François Millet",
        "artist_dates": "1814-1875",
        "edition": "The Gleaners (Des glaneuses), 1857",
        "source": "Musée d'Orsay, Paris",
        "scene": "Millet's Gleaners — the democratic field Whitman's grass grows in; pairs with § 6 'A child said What is the grass?'",
        "license": "Public Domain",
        "license_note": "Millet d. 1875; PD worldwide",
        "rights_holder": "Musée d'Orsay (Google Art Project)",
        "is_primary": True
    }],
    "there-was-a-child-went-forth": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Snap_the_Whip_1872_Winslow_Homer.jpeg?width=1200",
        "artist": "Winslow Homer",
        "artist_dates": "1836-1910",
        "edition": "Snap the Whip, 1872",
        "source": "Metropolitan Museum of Art",
        "scene": "Children in a specific American landscape — pairs with the porous absorbing child of Whitman's poem",
        "license": "Public Domain",
        "license_note": "Homer d. 1910; painting 1872; PD worldwide",
        "rights_holder": "Metropolitan Museum of Art",
        "is_primary": True
    }],
    "i-hear-america-singing": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/The_Veteran_in_a_New_Field_1865_Winslow_Homer.jpg?width=1200",
        "artist": "Winslow Homer",
        "artist_dates": "1836-1910",
        "edition": "The Veteran in a New Field, 1865",
        "source": "Metropolitan Museum of Art",
        "scene": "The returned soldier, now a mower — each singing what belongs to him",
        "license": "Public Domain",
        "rights_holder": "Metropolitan Museum of Art",
        "is_primary": True
    }],
    "crossing-brooklyn-ferry": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Currier_Ives_Central_Park_1864.jpg?width=1200",
        "artist": "Currier & Ives",
        "artist_dates": "active 1830s-1907",
        "edition": "Central Park lithograph, 1864",
        "source": "Library of Congress",
        "scene": "19th-century New York — the civic crowd Whitman addresses across time",
        "license": "Public Domain",
        "is_primary": True
    }],
    "when-i-heard-at-close-of-day": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Eakins%2C_Swimming_1885.jpg?width=1200",
        "artist": "Thomas Eakins",
        "artist_dates": "1844-1916",
        "edition": "Swimming (The Swimming Hole), 1885",
        "source": "Amon Carter Museum of American Art",
        "scene": "Eakins's Swimming — male companionship and embodiment. Eakins was Whitman's closest artist friend",
        "license": "Public Domain",
        "license_note": "Eakins d. 1916; painting 1885; PD worldwide",
        "rights_holder": "Amon Carter Museum",
        "is_primary": True
    }],
    "i-saw-in-louisiana-a-live-oak": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/cwpbh/00700/00752v.jpg",
        "artist": "Mathew Brady",
        "artist_dates": "c.1823-1896",
        "edition": "Studio portrait, c.1862",
        "source": "Library of Congress",
        "scene": "Whitman c.1862 — the man who could not, unlike the Louisiana oak, stand alone",
        "license": "Public Domain",
        "rights_holder": "Library of Congress (LC-DIG-cwpbh-00752)",
        "is_primary": True
    }],
    "out-of-the-cradle-endlessly-rocking": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/021_Mocking_Bird.jpg?width=1200",
        "artist": "John James Audubon",
        "artist_dates": "1785-1851",
        "edition": "Birds of America, Plate 21 — Mocking Bird, 1827-38",
        "source": "Havell engraving, Audubon original watercolor",
        "scene": "Audubon's mockingbird — the bird that, losing its mate, teaches the child on the Long Island shore the word for death",
        "license": "Public Domain",
        "license_note": "Audubon d. 1851; engravings 1827-38; PD worldwide",
        "rights_holder": "Wikimedia Commons",
        "is_primary": True
    }],
    "as-i-ebb-d-with-the-ocean-of-life": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/cwpbh/00700/00752v.jpg",
        "artist": "Mathew Brady",
        "artist_dates": "c.1823-1896",
        "edition": "Studio portrait, c.1862",
        "source": "Library of Congress",
        "scene": "The man who admits, in this poem, that he has not understood any thing",
        "license": "Public Domain",
        "rights_holder": "Library of Congress (LC-DIG-cwpbh-00752)",
        "is_primary": True
    }],

    # Civil War
    "beat-beat-drums": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombardment_of_Fort_Sumter.jpg?width=1200",
        "artist": "Currier & Ives lithograph",
        "artist_dates": "1863",
        "edition": "Bombardment of Fort Sumter, 1863",
        "source": "Library of Congress",
        "scene": "The war breaking into civic space — the ruthless force of the drums and bugles",
        "license": "Public Domain",
        "is_primary": True
    }],
    "cavalry-crossing-a-ford": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/ppmsca/33700/33750v.jpg",
        "artist": "Unknown photographer",
        "edition": "Civil War photograph",
        "source": "Library of Congress",
        "scene": "A Civil War ward — the painter's attention Whitman brings in this poem",
        "license": "Public Domain",
        "rights_holder": "Library of Congress (LC-DIG-ppmsca-33750)",
        "is_primary": True
    }],
    "the-wound-dresser": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/ppmsca/33700/33750v.jpg",
        "artist": "Unknown photographer",
        "edition": "Armory Square Hospital ward, Washington DC, 1862-65",
        "source": "Library of Congress",
        "scene": "A ward where Whitman visited the wounded — the specific hospital the poem comes from",
        "license": "Public Domain",
        "rights_holder": "Library of Congress (LC-DIG-ppmsca-33750)",
        "is_primary": True
    }],
    "reconciliation": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Winslow_Homer_-_Prisoners_from_the_Front_-_Google_Art_Project.jpg?width=1200",
        "artist": "Winslow Homer",
        "artist_dates": "1836-1910",
        "edition": "Prisoners from the Front, 1866",
        "source": "Metropolitan Museum of Art",
        "scene": "The Civil War reckoning rendered at specific visual angle — enemy and victor face to face",
        "license": "Public Domain",
        "rights_holder": "Metropolitan Museum of Art",
        "is_primary": True
    }],

    # Lincoln
    "when-lilacs-last": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Jean-Fran%C3%A7ois_Millet_(II)_-_The_Angelus_-_WGA15717.jpg?width=1200",
        "artist": "Jean-François Millet",
        "artist_dates": "1814-1875",
        "edition": "The Angelus (L'Angélus), 1857-59",
        "source": "Musée d'Orsay, Paris",
        "scene": "Millet's Angelus — the evening / mourning register, workers pausing to honor the dead. Pairs with Whitman's elegy",
        "license": "Public Domain",
        "rights_holder": "Musée d'Orsay",
        "is_primary": True
    }],
    "o-captain-my-captain": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/ppmsca/19200/19211v.jpg",
        "artist": "Mathew Brady",
        "artist_dates": "c.1823-1896",
        "edition": "Lincoln portrait, January 8, 1864",
        "source": "Library of Congress",
        "scene": "The Captain whom the ship has just brought home — Brady's Lincoln",
        "license": "Public Domain",
        "rights_holder": "Library of Congress (LC-DIG-ppmsca-19211)",
        "is_primary": True
    }],
    "darest-thou-now-o-soul": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Thomas_Eakins_-_Portrait_of_Walt_Whitman.jpg?width=1200",
        "artist": "Thomas Eakins",
        "artist_dates": "1844-1916",
        "edition": "Portrait of Walt Whitman, 1887-88",
        "source": "Pennsylvania Academy of the Fine Arts",
        "scene": "Late Whitman facing the unknown region — Eakins's definitive portrait",
        "license": "Public Domain",
        "license_note": "Eakins d. 1916; PAFA no known restrictions; Bridgeman v. Corel applies",
        "rights_holder": "Pennsylvania Academy of the Fine Arts",
        "is_primary": True
    }],

    # Late work
    "noiseless-patient-spider": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Walt%20Whitman,%20steel%20engraving,%20July%201854.jpg?width=800",
        "artist": "Samuel Hollyer",
        "artist_dates": "1826-1919",
        "edition": "1855 frontispiece (fallback)",
        "source": "Wikimedia Commons",
        "scene": "The soul casting filaments into the vacant vast — see also Fabre's Souvenirs Entomologiques for period spider engravings",
        "license": "Public Domain",
        "is_primary": True
    }],
    "passage-to-india-excerpt": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Thomas_Cole_The_Oxbow_(The_Connecticut_River_near_Northampton_1836).jpg?width=1200",
        "artist": "Thomas Cole",
        "artist_dates": "1801-1848",
        "edition": "View from Mount Holyoke (The Oxbow), 1836",
        "source": "Metropolitan Museum of Art",
        "scene": "American landscape — the soul taking ship, launching out on trackless seas",
        "license": "Public Domain",
        "rights_holder": "Metropolitan Museum of Art",
        "is_primary": True
    }],
    "song-of-the-open-road": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Thomas_Cole_The_Oxbow_(The_Connecticut_River_near_Northampton_1836).jpg?width=1200",
        "artist": "Thomas Cole",
        "artist_dates": "1801-1848",
        "edition": "View from Mount Holyoke (The Oxbow), 1836",
        "source": "Metropolitan Museum of Art",
        "scene": "The long brown path — American landscape pairing",
        "license": "Public Domain",
        "rights_holder": "Metropolitan Museum of Art",
        "is_primary": True
    }],
    "so-long": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Thomas_Eakins_-_Portrait_of_Walt_Whitman.jpg?width=1200",
        "artist": "Thomas Eakins",
        "artist_dates": "1844-1916",
        "edition": "Portrait of Walt Whitman, 1887-88",
        "source": "Pennsylvania Academy of the Fine Arts",
        "scene": "Late Whitman saying goodbye — Eakins's portrait of the closing voice",
        "license": "Public Domain",
        "rights_holder": "Pennsylvania Academy of the Fine Arts",
        "is_primary": True
    }],

    # Song of Myself sub-sections
    "song-of-myself-s48": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Jean-Fran%C3%A7ois_Millet_-_The_Sower_-_Walters_37905.jpg?width=1200",
        "artist": "Jean-François Millet",
        "artist_dates": "1814-1875",
        "edition": "The Sower, 1850",
        "source": "Walters Art Museum",
        "scene": "The furlong walked with sympathy — Millet's sower",
        "license": "Public Domain",
        "rights_holder": "Walters Art Museum",
        "is_primary": True
    }],
    "song-of-myself-s52": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Walt%20Whitman,%20steel%20engraving,%20July%201854.jpg?width=800",
        "artist": "Samuel Hollyer",
        "artist_dates": "1826-1919",
        "edition": "1855 frontispiece — the young man who promised to stop somewhere waiting for you",
        "source": "Wikimedia Commons",
        "scene": "The 1855 self-portrait returning at the closing of the long poem",
        "license": "Public Domain",
        "is_primary": True
    }],

    # Biographical anchors
    "bio-brooklyn-printer": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Walt%20Whitman,%20steel%20engraving,%20July%201854.jpg?width=800",
        "artist": "Samuel Hollyer",
        "artist_dates": "1826-1919",
        "edition": "1855 frontispiece (Whitman as print-shop-trained young man)",
        "source": "Wikimedia Commons",
        "scene": "Whitman in the working shirt he had been setting type in — the body the craft shaped",
        "license": "Public Domain",
        "is_primary": True
    }],
    "bio-self-review-scandal": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Walt%20Whitman,%20steel%20engraving,%20July%201854.jpg?width=800",
        "artist": "Samuel Hollyer",
        "artist_dates": "1826-1919",
        "edition": "1855 frontispiece",
        "source": "Wikimedia Commons",
        "scene": "The man who wrote his own reviews — the hunger visible in the face",
        "license": "Public Domain",
        "is_primary": True
    }],
    "bio-emerson-letter": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/pga/04100/04133v.jpg",
        "artist": "Stephen Alonzo Schoff engraving, after Samuel Worcester Rowse",
        "artist_dates": "Schoff 1818-1904; Rowse 1822-1901",
        "edition": "Ralph Waldo Emerson portrait, c.1878",
        "source": "Library of Congress",
        "scene": "The letter's recipient — Emerson, whose line 'I greet you at the beginning of a great career' Whitman gold-stamped on the second edition",
        "license": "Public Domain",
        "rights_holder": "Library of Congress (pga.04133)",
        "is_primary": True
    }],
    "bio-civil-war-nurse": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/ppmsca/57100/57140v.jpg",
        "artist": "Unknown photographer",
        "artist_dates": "c.1862-65",
        "edition": "Civil War hospital photograph",
        "source": "Library of Congress",
        "scene": "Nancy Maria Hill — a Civil War nurse at Armory Square Hospital where Whitman also served",
        "license": "Public Domain",
        "rights_holder": "Library of Congress (LC-DIG-ppmsca-57140)",
        "is_primary": True
    }],
    "bio-stroke-camden": [{
        "url": "https://tile.loc.gov/storage-services/service/pnp/ppmsca/07100/07141v.jpg",
        "artist": "Phillips & Taylor Studio",
        "artist_dates": "1873",
        "edition": "Whitman with butterfly, 1873 — Camden era",
        "source": "Library of Congress",
        "scene": "Whitman post-1873 stroke — the butterfly portrait from the Camden years",
        "license": "Public Domain",
        "rights_holder": "Library of Congress (LC-DIG-ppmsca-07141)",
        "is_primary": True
    }],
    "bio-death-deathbed-edition": [{
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Thomas_Eakins_-_Portrait_of_Walt_Whitman.jpg?width=1200",
        "artist": "Thomas Eakins",
        "artist_dates": "1844-1916",
        "edition": "Portrait of Walt Whitman, 1887-88",
        "source": "Pennsylvania Academy of the Fine Arts",
        "scene": "The face of the man who, a few years later, would sequence the Deathbed edition from his bed",
        "license": "Public Domain",
        "rights_holder": "Pennsylvania Academy of the Fine Arts",
        "is_primary": True
    }],
}


def apply():
    applied = 0
    for item in g['items']:
        iid = item['id']
        if iid in ILLUSTRATIONS:
            illus = ILLUSTRATIONS[iid]
            item.setdefault('metadata', {})['illustrations'] = illus
            # Keep image_url pointing at the primary for viewer compatibility
            primary = next((i for i in illus if i.get('is_primary')), illus[0])
            item['image_url'] = primary['url']
            applied += 1
    print(f'Applied illustration metadata to {applied} items')


apply()

# Write back
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(g, f, indent=2, ensure_ascii=False)

# Verify
with open(PATH, encoding='utf-8') as f:
    check = json.load(f)
with_illus = [it for it in check['items'] if 'illustrations' in it.get('metadata', {})]
with_url = [it for it in check['items'] if it.get('image_url')]
print(f'Items with illustration metadata: {len(with_illus)}')
print(f'Items with image_url: {len(with_url)}')
print(f'Total items: {len(check["items"])}')
print(f'File size: {os.path.getsize(PATH):,} bytes')
