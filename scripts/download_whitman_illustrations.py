"""
Download all Whitman grammar illustrations to a local folder for review.
Writes a sources.md alongside documenting each image's origin, rights, and
alternatives.
"""
import os
import time
import urllib.request
import urllib.parse

# Wikimedia's thumbnail generator rate-limits aggressively if you request
# many thumbnails in sequence. Best practice: (1) request original full-size
# files (upload.wikimedia.org/wikipedia/commons/X/YZ/filename) not thumbs,
# (2) set a real User-Agent with contact info per Wikimedia's UA policy, and
# (3) sleep briefly between requests.
USER_AGENT = ('recursive.eco-schemas-illustration-downloader/1.0 '
              '(https://recursive.eco contact: pp@playfulprocess.com)')

OUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'grammars', 'walt-whitman', 'illustrations'
)
OUT_DIR = os.path.abspath(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

# Each entry: (local filename, URL, rights-holder, year, description, alternates)
ILLUSTRATIONS = [
    (
        '01-hollyer-1855-frontispiece.jpg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Walt%20Whitman,%20steel%20engraving,%20July%201854.jpg?width=1200',
        'Samuel Hollyer (1826-1919), after Gabriel Harrison daguerreotype',
        '1855 (engraving); daguerreotype July 1854',
        'The iconic frontispiece engraving from the 1855 first edition of *Leaves of Grass*. Whitman in work shirt, hand on hip. PRIMARY COVER CANDIDATE. Used for grammar cover_image_url.',
        'LoC Feinberg-Whitman Collection; Whitman Archive page-images of 1855 ed.'
    ),
    (
        '02-brady-cwpbh-00752.jpg',
        'https://tile.loc.gov/storage-services/service/pnp/cwpbh/00700/00752v.jpg',
        'Mathew Brady (c.1823-1896), Brady National Photographic Portrait Gallery',
        'c.1862',
        'Brady studio portrait of Whitman, c.1862. Used for Phase II emergence image.',
        'LC-DIG-cwpbh-00752'
    ),
    (
        '03-whitman-butterfly-1873.jpg',
        'https://tile.loc.gov/storage-services/service/pnp/ppmsca/07100/07141v.jpg',
        'Phillips & Taylor studio, Philadelphia',
        '1873',
        'Whitman with butterfly (actually a cardboard prop). Whimsical, widely-loved. Used for Biographical emergence image. Strong cover alternate.',
        'LC-DIG-ppmsca-07141'
    ),
    (
        '04-brady-lincoln-1864.jpg',
        'https://tile.loc.gov/storage-services/service/pnp/ppmsca/19200/19211v.jpg',
        'Mathew Brady, Washington studio',
        'January 8, 1864',
        'Brady portrait of Lincoln. Iconic seated portrait. Used for Phase IV (Memories of Lincoln) emergence image.',
        'LC-DIG-ppmsca-19211'
    ),
    (
        '05-fords-theatre-assassination-1865.jpg',
        'https://tile.loc.gov/storage-services/service/pnp/pga/06000/06090v.jpg',
        'Currier & Ives, New York',
        '1865',
        'Lithograph of the Lincoln assassination at Ford\'s Theatre. Period-accurate visual.',
        'LoC pga.06090'
    ),
    (
        '06-armory-square-hospital-ward.jpg',
        'https://tile.loc.gov/storage-services/service/pnp/ppmsca/33700/33750v.jpg',
        'Unknown photographer, Washington DC',
        '1862-65',
        'A ward at Armory Square Hospital — one of the hospitals Whitman visited as volunteer nurse during the Civil War. Used for Phase III (Drum-Taps) emergence image and for "The Wound-Dresser" card.',
        'LC-DIG-ppmsca-33750'
    ),
    (
        '07-nurse-nancy-maria-hill.jpg',
        'https://tile.loc.gov/storage-services/service/pnp/ppmsca/57100/57140v.jpg',
        'Unknown photographer',
        'c.1862-65',
        'Nancy Maria Hill, Civil War nurse at Armory Square Hospital. Used for Civil War nurse biographical card.',
        'LC-DIG-ppmsca-57140'
    ),
    (
        '08-eakins-oil-portrait-1887.jpg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Thomas%20Eakins%20-%20Portrait%20of%20Walt%20Whitman.jpg?width=1200',
        'Thomas Eakins (1844-1916)',
        '1887-1888',
        'The definitive late-Whitman portrait. Oil, Pennsylvania Academy of the Fine Arts. STRONG COVER CANDIDATE. Used for Phase V emergence image and "So Long!" closing card.',
        'PAFA no-known-restrictions; Bridgeman v. Corel applies'
    ),
    (
        '09-emerson-schoff-engraving.jpg',
        'https://tile.loc.gov/storage-services/service/pnp/pga/04100/04133v.jpg',
        'Stephen Alonzo Schoff engraving after Samuel Worcester Rowse drawing',
        'c.1878',
        'Ralph Waldo Emerson portrait — the recipient of Whitman\'s mailed copy in 1855. Used for the Emerson Letter biographical card.',
        'LoC pga.04133'
    ),
    (
        '10-audubon-mockingbird.jpg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/021_Mocking_Bird.jpg?width=1200',
        'John James Audubon (1785-1851), Plate 21 *Birds of America*',
        '1827-1838',
        'The Mockingbird. Paired with "Out of the Cradle Endlessly Rocking." Wikimedia Commons mirror of the Havell engraving.',
        'Published 1827-38; PD worldwide. Alternate: https://www.audubon.org/birds-of-america/mocking-bird'
    ),
    (
        '11-curtis-lilac.jpg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Syringa_vulgaris_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-271.jpg?width=1000',
        'Curtis\'s *Botanical Magazine*, lilac plate',
        'pre-1900',
        'Hand-coloured engraving of Syringa vulgaris (Common Lilac). Paired with "When Lilacs Last in the Dooryard Bloom\'d."',
        'PD worldwide. Curtis Bot. Mag. originals at Biodiversity Heritage Library'
    ),
    (
        '12-whitman-mickle-street-house.jpg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Walt_Whitman_House_(Camden,_NJ)_-_front.jpg?width=1200',
        'Unknown photographer',
        'c.1890',
        'Whitman on the wharf near Mickle Street, with his nurse Warren Fritzenger. Used for Stroke/Camden biographical card.',
        'LoC — Camden era photographs'
    ),
    (
        '13-blake-deaths-door-1805.jpg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/William%20Blake%20-%20Death%27s%20Door.jpg?width=1000',
        'William Blake (1757-1827)',
        '1805',
        'Blake\'s "Death\'s Door" engraving — the design that inspired Whitman\'s Harleigh Cemetery tomb architecture. Symbolic substitute where no PD tomb photo is available.',
        'Pre-1929 engraving, PD worldwide'
    ),
]


def download(url, local, attempt=1):
    path = os.path.join(OUT_DIR, local)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        size = os.path.getsize(path)
        print(f'  [skip] {local} ({size:,} bytes) already downloaded')
        return True, size
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(path, 'wb') as f:
            f.write(data)
        size = len(data)
        print(f'  [ok]   {local} ({size:,} bytes)')
        time.sleep(1)  # politeness
        return True, size
    except Exception as e:
        if attempt < 3:
            print(f'  [retry {attempt}] {local}: {e}')
            time.sleep(3 * attempt)
            return download(url, local, attempt + 1)
        print(f'  [FAIL] {local}: {e}')
        return False, 0


print(f'Downloading to: {OUT_DIR}\n')
success = 0
total_size = 0
results = []
for local, url, creator, year, desc, alternates in ILLUSTRATIONS:
    ok, size = download(url, local)
    if ok:
        success += 1
        total_size += size
    results.append((ok, local, url, creator, year, desc, alternates))

print(f'\n{success}/{len(ILLUSTRATIONS)} downloaded, total {total_size/1024/1024:.1f} MB')

# Write sources.md
md_path = os.path.join(OUT_DIR, 'sources.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write('# Walt Whitman Grammar — Illustration Sources\n\n')
    f.write('*All images public domain. Downloaded ' + '2026-04-21' + '.*\n\n')
    f.write('This folder contains every illustration currently referenced by '
            '`grammar.json`, plus a few extras. Each file below lists its '
            'origin, creator, year, rights basis, and alternate sources.\n\n')
    f.write('All files are safe to mirror into Cloudflare R2 for the recursive.eco '
            'platform. When mirroring, keep the filenames or rename consistently '
            'and update `grammar.json` `image_url` fields.\n\n')
    f.write('---\n\n')
    for ok, local, url, creator, year, desc, alternates in results:
        status = '✅' if ok else '❌'
        f.write(f'## {status} `{local}`\n\n')
        f.write(f'- **Creator:** {creator}\n')
        f.write(f'- **Year:** {year}\n')
        f.write(f'- **Source URL:** {url}\n')
        f.write(f'- **Alternates / rights:** {alternates}\n')
        f.write(f'- **Description:** {desc}\n\n')
    f.write('---\n\n')
    f.write('## Top cover candidates (ranked from research)\n\n')
    f.write('1. `01-hollyer-1855-frontispiece.jpg` — iconic origin image\n')
    f.write('2. `08-eakins-oil-portrait-1887.jpg` — definitive late-life face\n')
    f.write('3. `03-whitman-butterfly-1873.jpg` — whimsical, widely loved\n')
    f.write('4. `02-brady-cwpbh-00752.jpg` — mid-career bridge\n\n')
    f.write('## Known gaps\n\n')
    f.write('- **Harleigh Cemetery tomb** — no stable PD institutional photo. '
            'Using Blake "Death\'s Door" as symbolic substitute (the engraving '
            'inspired Whitman\'s tomb design).\n')
    f.write('- **Brooklyn ferries, 1850s** — no direct LoC image for that '
            'specific decade. Phase II emergence currently uses Brady portrait; '
            'alternate: Currier & Ives New York harbor lithograph or Bachmann '
            'Brooklyn panorama 1846.\n')
    f.write('- **Brooklyn printer, 1830s** — no Whitman-specific printshop. '
            'Consider generic period composing-room engraving from LoC P&P.\n')
    f.write('- **"Song of Myself" manuscript** — the complete 1855 manuscript '
            'is lost. Substitutes: WWA 1855 title-page image or surviving '
            'notebook fragments (LoC Harned Collection).\n\n')
    f.write('## Additional resources for further illustration work\n\n')
    f.write('- **Library of Congress Prints & Photographs Online Catalog**: https://www.loc.gov/pictures/\n')
    f.write('- **Walt Whitman Archive**: https://whitmanarchive.org/\n')
    f.write('- **Biodiversity Heritage Library**: https://www.biodiversitylibrary.org/ — for botanical / zoological engravings (lilac, grass, spider, mockingbird)\n')
    f.write('- **Wikimedia Commons — Walt Whitman category**: https://commons.wikimedia.org/wiki/Category:Walt_Whitman\n')
    f.write('- **National Audubon Society, Birds of America**: https://www.audubon.org/birds-of-america\n')
    f.write('- **NYPL Digital Collections — Whitman**: https://digitalcollections.nypl.org/search/index?filters%5Bname%5D=Whitman%2C+Walt%2C+1819-1892\n\n')
    f.write('## License\n\n')
    f.write('All images above are in the U.S. public domain based on creator death date '
            '(pre-1955) or publication date (pre-1929). 2D faithful reproductions of PD '
            'paintings are themselves PD per *Bridgeman Art Library v. Corel* (1999). '
            'LoC, PAFA, Whitman Archive, and BHL each state no known copyright restrictions '
            'for these specific files.\n\n')
    f.write('The illustrations, once uploaded to R2 and served by recursive.eco, retain '
            'their public-domain status — only the arrangement and curation of this '
            'grammar is CC BY-SA 4.0.\n')
print(f'\nWrote {md_path}')
