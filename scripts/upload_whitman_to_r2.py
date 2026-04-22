"""
Upload Whitman grammar illustrations to R2.

Downloads each image referenced in grammar.json (currently pointing at
Wikimedia / Library of Congress), uploads to R2, and rewrites grammar.json
with the R2 URLs.

Env vars loaded from recursive-kids-stories-club/.env.local:
    CLOUDFLARE_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY,
    R2_BUCKET_NAME, R2_PUBLIC_URL
"""
import json
import os
import re
import sys
import time
from pathlib import Path

import boto3
import requests
from botocore.config import Config

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_PATH = ROOT / 'grammars' / 'walt-whitman' / 'grammar.json'
ENV_PATH = Path(r'C:\Users\ferna\OneDrive\Documentos\GitHub\recursive-kids-stories-club\.env.local')

UA = 'recursive.eco-schemas-illustration-downloader/1.0 (+https://recursive.eco)'
GRAMMAR_SLUG = 'walt-whitman'
POLITENESS_SECS = 1.0


def load_env():
    if not ENV_PATH.exists():
        sys.exit(f'Env file not found: {ENV_PATH}')
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
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s[:maxlen] or 'image'


def filename_from_url(url: str) -> str:
    """Derive a slug for the R2 path from the source URL."""
    if 'Special:FilePath/' in url:
        raw = url.split('Special:FilePath/')[1].split('?')[0]
    else:
        raw = url.rsplit('/', 1)[-1].split('?')[0]
    # url-decode
    try:
        from urllib.parse import unquote
        raw = unquote(raw)
    except Exception:
        pass
    # preserve ext
    base, _, ext = raw.rpartition('.')
    if not ext or len(ext) > 5:
        base, ext = raw, 'jpg'
    return f'{slugify(base)}.{ext.lower()}'


def fetch(url: str) -> bytes:
    r = requests.get(url, headers={'User-Agent': UA}, timeout=30, allow_redirects=True)
    r.raise_for_status()
    return r.content


def main():
    load_env()
    required = ['CLOUDFLARE_ACCOUNT_ID', 'R2_ACCESS_KEY_ID',
                'R2_SECRET_ACCESS_KEY', 'R2_BUCKET_NAME', 'R2_PUBLIC_URL']
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        sys.exit(f'Missing env vars: {missing}')

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
    print(f'Loaded {len(items)} items from {GRAMMAR_PATH.name}')

    # Also handle the top-level cover_image_url
    work_list = []
    if g.get('cover_image_url'):
        work_list.append(('__cover__', g['cover_image_url'], g))

    for it in items:
        meta = it.get('metadata', {})
        illos = meta.get('illustrations', [])
        if illos and illos[0].get('url'):
            work_list.append((it['id'], illos[0]['url'], it))

    print(f'Found {len(work_list)} image URLs to migrate\n')

    uploaded = 0
    failed = []

    for idx, (iid, src_url, container) in enumerate(work_list, 1):
        fname = filename_from_url(src_url)
        r2_key = f'grammar-illustrations/{GRAMMAR_SLUG}/{iid}/{fname}'
        r2_url = f'{public_base}/{r2_key}'

        print(f'[{idx}/{len(work_list)}] {iid}')
        print(f'   src:  {src_url[:90]}')
        print(f'   dest: {r2_key}')

        try:
            data = fetch(src_url)
            print(f'   downloaded: {len(data):,} bytes')
            content_type = 'image/jpeg'
            if fname.endswith('.png'): content_type = 'image/png'
            elif fname.endswith('.webp'): content_type = 'image/webp'
            elif fname.endswith('.gif'): content_type = 'image/gif'
            s3.put_object(
                Bucket=bucket,
                Key=r2_key,
                Body=data,
                ContentType=content_type,
            )
            print(f'   uploaded -> {r2_url}')

            # Update in-place
            if iid == '__cover__':
                g['cover_image_url'] = r2_url
            else:
                container['image_url'] = r2_url
                if container.get('metadata', {}).get('illustrations'):
                    container['metadata']['illustrations'][0]['url'] = r2_url
            uploaded += 1
        except Exception as e:
            print(f'   [FAIL] {e}')
            failed.append((iid, src_url, str(e)))

        if idx < len(work_list):
            time.sleep(POLITENESS_SECS)
        print()

    # Write updated grammar
    GRAMMAR_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\n=== Summary ===')
    print(f'Uploaded: {uploaded}/{len(work_list)}')
    print(f'Failed:   {len(failed)}')
    if failed:
        for iid, url, err in failed:
            print(f'  {iid}: {err}')
    print(f'\nGrammar written: {GRAMMAR_PATH}')


if __name__ == '__main__':
    main()
