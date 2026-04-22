"""Upload the last two Whitman images and finalize grammar.json."""
import json, os, time
from pathlib import Path
import boto3, requests
from botocore.config import Config

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_PATH = ROOT / 'grammars' / 'walt-whitman' / 'grammar.json'
ENV_PATH = Path(r'C:\Users\ferna\OneDrive\Documentos\GitHub\recursive-kids-stories-club\.env.local')
UA = 'recursive.eco-schemas/1.0 (+https://recursive.eco)'

TARGETS = [
    # (item-id, source URL, artist/source note, scene)
    ('crossing-brooklyn-ferry',
     'https://upload.wikimedia.org/wikipedia/commons/a/a5/The_East_River_from_the_Grand_Street_Ferry%2C_Brooklyn%2C_E.D_%28NYPL_Hades-255569-492795%29.jpg',
     'NYPL Hades collection', 'The East River from the Grand Street Ferry, Brooklyn'),
    ('bio-brooklyn-printer',
     'https://upload.wikimedia.org/wikipedia/commons/5/52/Brooklyn_Daily_Eagle2.jpg',
     'Public domain / Wikimedia Commons', 'Masthead of the Brooklyn Daily Eagle, the paper Whitman edited 1846-48'),
]

def load_env():
    for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k,v = line.split('=',1); v = v.strip().strip('"\'')
        if v and not os.environ.get(k): os.environ[k] = v

def main():
    load_env()
    s3 = boto3.client('s3',
        endpoint_url=f"https://{os.environ['CLOUDFLARE_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ['R2_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['R2_SECRET_ACCESS_KEY'],
        config=Config(signature_version='s3v4'), region_name='auto')
    bucket = os.environ['R2_BUCKET_NAME']
    public = os.environ['R2_PUBLIC_URL'].rstrip('/')

    g = json.loads(GRAMMAR_PATH.read_text(encoding='utf-8'))
    items_by_id = {it['id']: it for it in g['items']}

    for iid, url, source_note, scene in TARGETS:
        print(f'--- {iid}')
        print(f'    src: {url[:100]}')
        data = requests.get(url, headers={'User-Agent':UA}, timeout=60).content
        print(f'    dl:  {len(data):,} bytes')
        ext = 'jpg'
        key = f'grammar-illustrations/walt-whitman/{iid}/{iid}.{ext}'
        s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType='image/jpeg')
        r2_url = f'{public}/{key}'
        print(f'    -> {r2_url}')
        it = items_by_id[iid]
        it['image_url'] = r2_url
        if it.get('metadata',{}).get('illustrations'):
            it['metadata']['illustrations'][0]['url'] = r2_url
            it['metadata']['illustrations'][0]['source'] = source_note
            it['metadata']['illustrations'][0]['scene'] = scene
        time.sleep(1)
        print()

    GRAMMAR_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Done.')

if __name__ == '__main__':
    main()
