"""
Upload Bus Passengers SVG icons to Cloudflare R2.

Path convention (per schemas/CLAUDE.md illustration system):
    grammar-illustrations/bus-passengers/{passenger-id}/icon.svg

Public URL pattern (after upload):
    https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/bus-passengers/{id}/icon.svg

Run: python scripts/upload-bus-passengers-svgs.py

Reads R2 credentials from env (or from recursive-eco/.env.local if invoked
from there). After upload, also patches grammars/bus-passengers/grammar.json
to replace local `image_url: "icons/<id>.svg"` with the public R2 URL so
the grammar is portable.

Idempotent: skips files already present on R2 with matching size.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import boto3
from botocore.config import Config as BotoConfig

# Try to load env from common locations
try:
    from dotenv import load_dotenv

    for env_path in [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env",
        Path(__file__).resolve().parent.parent.parent / "recursive-eco" / ".env.local",
        Path(__file__).resolve().parent.parent.parent / "recursive-eco" / "apps" / "flow" / ".env.local",
    ]:
        if env_path.exists():
            load_dotenv(env_path)
            print(f"  loaded env from {env_path}", file=sys.stderr)
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_DIR = ROOT / "grammars" / "bus-passengers"
ICONS_DIR = GRAMMAR_DIR / "icons"
GRAMMAR_JSON = GRAMMAR_DIR / "grammar.json"

R2_PATH_PREFIX = "grammar-illustrations/bus-passengers"
R2_PUBLIC_URL = "https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev"


def _r2_env():
    # Try multiple variable names — recursive-eco uses CLOUDFLARE_ACCOUNT_ID,
    # the wallis-rag pipeline uses R2_ACCOUNT_ID. Accept either.
    account = os.environ.get("R2_ACCOUNT_ID") or os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    key = os.environ.get("R2_ACCESS_KEY_ID")
    secret = os.environ.get("R2_SECRET_ACCESS_KEY")
    bucket = os.environ.get("R2_BUCKET_NAME")
    missing = [n for n, v in [("ACCOUNT_ID", account), ("ACCESS_KEY_ID", key), ("SECRET_ACCESS_KEY", secret), ("BUCKET_NAME", bucket)] if not v]
    if missing:
        raise RuntimeError(f"missing R2 env vars: {', '.join(missing)}")
    return {
        "bucket": bucket,
        "endpoint": f"https://{account}.r2.cloudflarestorage.com",
        "key": key,
        "secret": secret,
    }


def _r2_client(env):
    return boto3.client(
        "s3",
        endpoint_url=env["endpoint"],
        aws_access_key_id=env["key"],
        aws_secret_access_key=env["secret"],
        config=BotoConfig(signature_version="s3v4"),
        region_name="auto",
    )


def existing_size(r2, bucket, key):
    try:
        h = r2.head_object(Bucket=bucket, Key=key)
        return h["ContentLength"]
    except r2.exceptions.NoSuchKey:
        return None
    except Exception:
        return None


def upload_svg(r2, bucket, local_path: Path, key: str) -> bool:
    """Upload one SVG. Returns True if uploaded, False if skipped."""
    body = local_path.read_bytes()
    existing = existing_size(r2, bucket, key)
    if existing == len(body):
        return False
    r2.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType="image/svg+xml",
        CacheControl="public, max-age=31536000, immutable",
    )
    return True


def patch_grammar_json(uploaded_ids: list[str]):
    """Update image_url in grammar.json to point at R2 public URLs."""
    grammar = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    changed = 0
    for item in grammar.get("items", []):
        item_id = item.get("id")
        if item_id not in uploaded_ids:
            continue
        new_url = f"{R2_PUBLIC_URL}/{R2_PATH_PREFIX}/{item_id}/icon.svg"
        if item.get("image_url") != new_url:
            item["image_url"] = new_url
            changed += 1
    if changed:
        GRAMMAR_JSON.write_text(json.dumps(grammar, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  patched {changed} image_url fields in grammar.json")


def main():
    if not ICONS_DIR.exists():
        print(f"icons dir not found: {ICONS_DIR}")
        sys.exit(1)

    env = _r2_env()
    r2 = _r2_client(env)
    bucket = env["bucket"]

    svgs = sorted(ICONS_DIR.glob("*.svg"))
    print(f"Found {len(svgs)} SVG files in {ICONS_DIR}")
    print(f"Uploading to bucket={bucket} prefix={R2_PATH_PREFIX}")
    print()

    uploaded_ids = []
    skipped = 0
    for svg_path in svgs:
        item_id = svg_path.stem
        key = f"{R2_PATH_PREFIX}/{item_id}/icon.svg"
        result = upload_svg(r2, bucket, svg_path, key)
        if result:
            print(f"  ↑ {item_id}")
            uploaded_ids.append(item_id)
        else:
            print(f"  · {item_id} (skipped, already up-to-date)")
            skipped += 1
            uploaded_ids.append(item_id)  # still patch the URL in case it's wrong

    print(f"\nDone. Uploaded {len(svgs) - skipped}, skipped {skipped}.")
    patch_grammar_json(uploaded_ids)
    print()
    print(f"Public URL example: {R2_PUBLIC_URL}/{R2_PATH_PREFIX}/joy/icon.svg")


if __name__ == "__main__":
    main()
