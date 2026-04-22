"""
Second pass: resolve the 19 Wikimedia 404s from the first upload run.

Strategy:
 1. For each item whose image_url is still a Wikimedia Special:FilePath URL
    (meaning it failed last time), try the Wikimedia Commons API to find
    the real file URL.
 2. If API finds it, download + upload to R2 and rewrite.
 3. If API can't find it, try the local illustrations/ folder — we have
    13 curated JPGs that cover several of these scenes.
 4. If neither works, log and skip — item stays on the broken Wikimedia URL
    (user decides later).
"""
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import unquote

import boto3
import requests
from botocore.config import Config

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_PATH = ROOT / 'grammars' / 'walt-whitman' / 'grammar.json'
LOCAL_IMG_DIR = ROOT / 'grammars' / 'walt-whitman' / 'illustrations'
ENV_PATH = Path(r'C:\Users\ferna\OneDrive\Documentos\GitHub\recursive-kids-stories-club\.env.local')
UA = 'recursive.eco-schemas-illustration-downloader/1.0 (+https://recursive.eco)'
GRAMMAR_SLUG = 'walt-whitman'

# Map item-ids to local illustrations/ filenames when the author's curated
# file is a better source than Wikimedia. Based on content-fit.
LOCAL_FALLBACK = {
    'there-was-a-child-went-forth': '19-homer-veteran-new-field-1865.jpg',  # Homer; not exact but era-right. Prefer unique.
    # Most local files already got uploaded via successful Wikimedia URLs.
    # Leaving this map mostly empty — Wikimedia API should resolve most failures.
}

KEYWORD_HINTS = {
    # Item-id -> search query for Wikimedia if filename lookup fails
    'song-of-myself-s48': 'Millet Man with Hoe 1862',
    'song-of-myself-s52': 'Audubon Red-tailed Hawk Birds of America',
    'there-was-a-child-went-forth': 'Winslow Homer Snap the Whip',
    'crossing-brooklyn-ferry': 'Samuel Bell Waugh Bay Harbor New York 1855',
    'when-i-heard-at-close-of-day': 'Thomas Eakins Swimming 1885',
    'i-saw-in-louisiana-a-live-oak': 'Sanford Gifford Gorge Mountains Kauterskill',
    'out-of-the-cradle-endlessly-rocking': 'Audubon Mockingbird Birds of America',
    'as-i-ebb-d-with-the-ocean-of-life': 'Winslow Homer Summer Night 1890',
    'cavalry-crossing-a-ford': 'Winslow Homer Home Sweet Home 1863',
    'reconciliation': 'Winslow Homer Prisoners from the Front',
    'when-lilacs-last': 'Millet The Angelus painting',
    'phase-5-late-work': 'Thomas Eakins Portrait of Walt Whitman',
    'passage-to-india-excerpt': 'Frederic Church Heart of the Andes',
    'song-of-the-open-road': 'George Caleb Bingham Jolly Flatboatmen 1846',
    'so-long': 'Walt Whitman George C Cox photograph 1887',
    'bio-brooklyn-printer': 'Harper Brothers composing room 1855 engraving',
    'bio-self-review-scandal': 'Leaves of Grass 1855 title page first edition',
    'bio-stroke-camden': 'Walt Whitman House Camden New Jersey',
    'bio-death-deathbed-edition': 'Thomas Eakins Walt Whitman 1891 portrait',
}


def load_env():
    for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        v = v.strip().strip('"\'')
        if v and not os.environ.get(k):
            os.environ[k] = v


def slugify(s: str, maxlen: int = 60) -> str:
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:maxlen] or 'image'


def wikimedia_search(query: str) -> str | None:
    """Search Wikimedia Commons for a file matching the query. Return the
    direct-download URL of the top result, or None."""
    api = 'https://commons.wikimedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': f'filetype:bitmap {query}',
        'gsrnamespace': '6',  # File namespace
        'gsrlimit': '3',
        'prop': 'imageinfo',
        'iiprop': 'url|size|mime',
    }
    try:
        r = requests.get(api, params=params, headers={'User-Agent': UA}, timeout=30)
        r.raise_for_status()
        data = r.json()
        pages = data.get('query', {}).get('pages', {})
        for pid, page in pages.items():
            ii = page.get('imageinfo', [])
            if ii and ii[0].get('url'):
                return ii[0]['url']
    except Exception as e:
        print(f'    [search-err] {e}')
    return None


def fetch(url: str) -> bytes:
    r = requests.get(url, headers={'User-Agent': UA}, timeout=60, allow_redirects=True)
    r.raise_for_status()
    return r.content


def is_still_wikimedia(url: str) -> bool:
    return 'commons.wikimedia.org' in url


def main():
    load_env()
    account = os.environ['CLOUDFLARE_ACCOUNT_ID']
    bucket = os.environ['R2_BUCKET_NAME']
    public_base = os.environ['R2_PUBLIC_URL'].rstrip('/')

    s3 = boto3.client(
        's3',
        endpoint_url=f'https://{account}.r2.cloudflarestorage.com',
        aws_access_key_id=os.environ['R2_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['R2_SECRET_ACCESS_KEY'],
        config=Config(signature_version='s3v4'),
        region_name='auto',
    )

    g = json.loads(GRAMMAR_PATH.read_text(encoding='utf-8'))
    items = g.get('items', [])

    # Collect items whose image_url is still a Wikimedia URL (those are the failures)
    failures = []
    for it in items:
        url = it.get('image_url', '')
        if is_still_wikimedia(url):
            failures.append(it)
    print(f'Items still on Wikimedia URL (failed last pass): {len(failures)}\n')

    fixed = 0
    still_broken = []
    for idx, it in enumerate(failures, 1):
        iid = it['id']
        print(f'[{idx}/{len(failures)}] {iid}')

        new_bytes = None
        new_url_source = None
        new_ext = 'jpg'

        # 1. Try Wikimedia search with keyword hint
        query = KEYWORD_HINTS.get(iid)
        if query:
            print(f'   searching Wikimedia: "{query}"')
            direct_url = wikimedia_search(query)
            if direct_url:
                print(f'   found: {direct_url[:90]}')
                try:
                    new_bytes = fetch(direct_url)
                    new_url_source = direct_url
                    new_ext = direct_url.rsplit('.', 1)[-1].lower()
                    if new_ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                        new_ext = 'jpg'
                except Exception as e:
                    print(f'   [dl-fail] {e}')

        # 2. Try local fallback
        if new_bytes is None and iid in LOCAL_FALLBACK:
            local_path = LOCAL_IMG_DIR / LOCAL_FALLBACK[iid]
            if local_path.exists():
                new_bytes = local_path.read_bytes()
                new_url_source = f'local:{local_path.name}'
                new_ext = local_path.suffix.lstrip('.').lower()
                print(f'   using local: {local_path.name}')

        if new_bytes is None:
            print(f'   [SKIP] no source found\n')
            still_broken.append(iid)
            time.sleep(1)
            continue

        # Upload to R2
        fname = f'{slugify(iid)}.{new_ext}'
        r2_key = f'grammar-illustrations/{GRAMMAR_SLUG}/{iid}/{fname}'
        r2_url = f'{public_base}/{r2_key}'
        content_type = {'jpg':'image/jpeg','jpeg':'image/jpeg','png':'image/png',
                        'webp':'image/webp','gif':'image/gif'}.get(new_ext,'image/jpeg')
        try:
            s3.put_object(Bucket=bucket, Key=r2_key, Body=new_bytes, ContentType=content_type)
            print(f'   uploaded -> {r2_url}')
            it['image_url'] = r2_url
            if it.get('metadata', {}).get('illustrations'):
                it['metadata']['illustrations'][0]['url'] = r2_url
                # Also note the source change
                if new_url_source and not new_url_source.startswith('local:'):
                    it['metadata']['illustrations'][0]['source'] = new_url_source
            fixed += 1
        except Exception as e:
            print(f'   [upload-fail] {e}')
            still_broken.append(iid)

        time.sleep(1)
        print()

    GRAMMAR_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print('\n=== Pass 2 Summary ===')
    print(f'Fixed: {fixed}/{len(failures)}')
    print(f'Still broken: {len(still_broken)}')
    for iid in still_broken:
        print(f'  - {iid}')


if __name__ == '__main__':
    main()
