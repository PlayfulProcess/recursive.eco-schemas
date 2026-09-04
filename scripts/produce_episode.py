#!/usr/bin/env python3
"""
Produce animated episodes from storyboard grammars.

Orchestrates:
  1. Image generation (OpenAI DALL-E 3 / GPT-Image-1)
  2. Image-to-video transitions (fal.ai → Kling / Hailuo / Veo / Runway)
  3. TTS narration (OpenAI TTS)
  4. Stores results back into grammar metadata

Usage:
  python3 scripts/produce_episode.py <storyboard-grammar> [--episode <id>] [--dry-run]

Environment variables:
  OPENAI_API_KEY       - For DALL-E image gen + TTS
  FAL_KEY              - For fal.ai video gen (Kling/Hailuo/Veo)
  VIDEO_MODEL          - fal model to use (default: fal-ai/kling-video/v2/image-to-video)
  TTS_VOICE            - OpenAI TTS voice (default: nova)
  OUTPUT_DIR           - Where to save generated assets (default: output/)

Requires: pip install openai fal-client

Designed to be called by Claude in cowork/batch mode.
"""

import json
import os
import sys
import time
import argparse
import base64
from pathlib import Path


# ─── Configuration ───────────────────────────────────────────────────────────

DEFAULT_VIDEO_MODEL = "fal-ai/kling-video/v2/image-to-video"
ALTERNATIVE_VIDEO_MODELS = {
    "kling":   "fal-ai/kling-video/v2/image-to-video",
    "hailuo":  "fal-ai/minimax-video/image-to-video",
    "veo":     "fal-ai/veo3",
    "runway":  "fal-ai/runway-gen3/turbo/image-to-video",
    "luma":    "fal-ai/luma-dream-machine/image-to-video",
}

TTS_VOICES = {
    "narrator": "nova",       # Warm, storytelling voice
    "alice": "shimmer",       # Young, curious voice for Alice dialogue
    "male": "onyx",           # Deep male characters
    "elder": "echo",          # Wise elder characters
}

IMAGE_SIZE = "1792x1024"      # 16:9 widescreen for video
IMAGE_QUALITY = "hd"


# ─── API Clients ─────────────────────────────────────────────────────────────

def get_openai_client():
    """Initialize OpenAI client."""
    try:
        from openai import OpenAI
        return OpenAI()
    except ImportError:
        print("ERROR: pip install openai", file=sys.stderr)
        sys.exit(1)


def get_fal_client():
    """Initialize fal.ai client."""
    try:
        import fal_client
        return fal_client
    except ImportError:
        print("ERROR: pip install fal-client", file=sys.stderr)
        sys.exit(1)


# ─── Image Generation ───────────────────────────────────────────────────────

def generate_image(client, prompt, output_path, model="gpt-image-1"):
    """Generate an image using OpenAI DALL-E 3 or GPT-Image-1."""
    print(f"    🎨 Generating image...", file=sys.stderr)

    if model == "gpt-image-1":
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=IMAGE_SIZE,
            quality=IMAGE_QUALITY,
            n=1,
        )
        # GPT-Image-1 returns base64
        image_b64 = result.data[0].b64_json
        if image_b64:
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(image_b64))
        else:
            # URL-based response
            import urllib.request
            urllib.request.urlretrieve(result.data[0].url, output_path)
    else:
        # DALL-E 3
        result = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=IMAGE_SIZE,
            quality=IMAGE_QUALITY,
            n=1,
        )
        import urllib.request
        urllib.request.urlretrieve(result.data[0].url, output_path)

    print(f"    ✓ Saved {output_path}", file=sys.stderr)
    return output_path


# ─── Video Generation (Transitions) ─────────────────────────────────────────

def generate_video_transition(fal, image_path, prompt, output_path,
                               model=None, duration=5):
    """Generate image-to-video transition using fal.ai."""
    model = model or os.environ.get("VIDEO_MODEL", DEFAULT_VIDEO_MODEL)
    print(f"    🎬 Generating video ({model})...", file=sys.stderr)

    # Read image as data URL
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    ext = Path(image_path).suffix.lstrip(".")
    mime = f"image/{ext}" if ext != "jpg" else "image/jpeg"
    image_url = f"data:{mime};base64,{image_data}"

    # Submit to fal.ai
    result = fal.subscribe(
        model,
        arguments={
            "image_url": image_url,
            "prompt": prompt,
            "duration": str(duration),
        },
        with_logs=False,
    )

    # Download result video
    video_url = result.get("video", {}).get("url") or result.get("url")
    if video_url:
        import urllib.request
        urllib.request.urlretrieve(video_url, output_path)
        print(f"    ✓ Saved {output_path}", file=sys.stderr)
    else:
        print(f"    ✗ No video URL in response: {result}", file=sys.stderr)

    return output_path


# ─── TTS Narration ───────────────────────────────────────────────────────────

def generate_narration(client, text, output_path, voice=None):
    """Generate TTS narration using OpenAI."""
    voice = voice or os.environ.get("TTS_VOICE", "nova")
    print(f"    🎙️ Generating narration ({voice})...", file=sys.stderr)

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=text,
        speed=0.9,  # Slightly slower for bedtime stories
    )

    response.stream_to_file(output_path)
    print(f"    ✓ Saved {output_path}", file=sys.stderr)
    return output_path


# ─── Batch Processing ───────────────────────────────────────────────────────

def process_scene(scene, output_dir, openai_client, fal_client,
                   image_model="gpt-image-1", video_model=None,
                   skip_video=False, skip_tts=False, dry_run=False):
    """Process a single scene: image → video → narration."""
    scene_id = scene["id"]
    scene_dir = Path(output_dir) / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)

    results = {"scene_id": scene_id, "assets": {}}

    # 1. Image generation
    image_path = scene_dir / "frame.png"
    prompt = scene["sections"]["ImagePrompt"]

    if dry_run:
        print(f"  [DRY RUN] Would generate image for {scene_id}", file=sys.stderr)
        print(f"    Prompt: {prompt[:100]}...", file=sys.stderr)
        results["assets"]["image_prompt"] = prompt
    elif not image_path.exists():
        generate_image(openai_client, prompt, str(image_path), model=image_model)
        results["assets"]["image"] = str(image_path)
    else:
        print(f"    SKIP image: {image_path} exists", file=sys.stderr)
        results["assets"]["image"] = str(image_path)

    # 2. Video transition
    if not skip_video:
        video_path = scene_dir / "transition.mp4"
        direction = scene["sections"].get("Direction", "")
        video_prompt = f"{direction}. {prompt[:200]}"

        if dry_run:
            print(f"  [DRY RUN] Would generate video for {scene_id}", file=sys.stderr)
            results["assets"]["video_prompt"] = video_prompt
        elif not video_path.exists() and image_path.exists():
            try:
                generate_video_transition(
                    fal_client, str(image_path), video_prompt,
                    str(video_path), model=video_model,
                    duration=scene["metadata"].get("timing_seconds", 5)
                )
                results["assets"]["video"] = str(video_path)
            except Exception as e:
                print(f"    ✗ Video failed: {e}", file=sys.stderr)
                results["assets"]["video_error"] = str(e)

    # 3. TTS narration
    if not skip_tts:
        audio_path = scene_dir / "narration.mp3"
        narration = scene["sections"]["Narration"]

        if dry_run:
            print(f"  [DRY RUN] Would generate narration for {scene_id}", file=sys.stderr)
            results["assets"]["narration_text"] = narration[:100]
        elif not audio_path.exists():
            generate_narration(openai_client, narration, str(audio_path))
            results["assets"]["audio"] = str(audio_path)
        else:
            print(f"    SKIP audio: {audio_path} exists", file=sys.stderr)
            results["assets"]["audio"] = str(audio_path)

    return results


def process_episode(grammar, episode_id, output_dir, openai_client, fal_client,
                     dry_run=False, **kwargs):
    """Process all scenes in an episode."""
    # Find the L2 episode item
    episode = None
    for item in grammar["items"]:
        if item.get("level") == 2 and item["id"] == episode_id:
            episode = item
            break

    if not episode:
        print(f"Episode '{episode_id}' not found", file=sys.stderr)
        return None

    scene_ids = episode.get("composite_of", [])
    scenes = [i for i in grammar["items"] if i["id"] in scene_ids and i.get("level") == 1]
    scenes.sort(key=lambda x: x["sort_order"])

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Episode: {episode['name']}", file=sys.stderr)
    print(f"Scenes: {len(scenes)}", file=sys.stderr)
    print(f"Total time: ~{episode['metadata'].get('total_seconds', '?')}s", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    results = []
    for scene in scenes:
        print(f"\n  Scene {scene['metadata']['scene_number']}/{scene['metadata']['total_scenes']}: "
              f"{scene['name']}", file=sys.stderr)
        result = process_scene(
            scene, output_dir, openai_client, fal_client,
            dry_run=dry_run, **kwargs
        )
        results.append(result)

        # Rate limiting between scenes
        if not dry_run:
            time.sleep(2)

    return {
        "episode_id": episode_id,
        "episode_name": episode["name"],
        "scenes": results,
    }


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Produce animated episodes from storyboard grammars")
    parser.add_argument("grammar", help="Path to storyboard grammar JSON")
    parser.add_argument("--episode", help="Specific episode ID to process (default: all)")
    parser.add_argument("--episodes", help="Comma-separated episode IDs")
    parser.add_argument("--batch", type=int, help="Process first N episodes")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without calling APIs")
    parser.add_argument("--images-only", action="store_true", help="Only generate images (skip video/TTS)")
    parser.add_argument("--skip-video", action="store_true", help="Skip video generation")
    parser.add_argument("--skip-tts", action="store_true", help="Skip TTS generation")
    parser.add_argument("--image-model", default="gpt-image-1", choices=["gpt-image-1", "dall-e-3"])
    parser.add_argument("--video-model", default=None, help="fal.ai video model (kling/hailuo/veo/runway/luma)")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--manifest", action="store_true", help="Output JSON manifest of what to produce")

    args = parser.parse_args()

    # Load grammar
    with open(args.grammar) as f:
        grammar = json.load(f)

    grammar_slug = Path(args.grammar).parent.name

    # Resolve video model alias
    video_model = args.video_model
    if video_model and video_model in ALTERNATIVE_VIDEO_MODELS:
        video_model = ALTERNATIVE_VIDEO_MODELS[video_model]

    # If --manifest, just output the production plan as JSON
    if args.manifest:
        episodes = [i for i in grammar["items"] if i.get("level") == 2]
        scenes = [i for i in grammar["items"] if i.get("level") == 1]
        manifest = {
            "grammar": grammar_slug,
            "total_episodes": len(episodes),
            "total_scenes": len(scenes),
            "episodes": []
        }
        for ep in episodes:
            ep_scenes = [s for s in scenes if s["metadata"].get("episode_id") in ep["id"].replace("episode-", "")]
            manifest["episodes"].append({
                "id": ep["id"],
                "name": ep["name"],
                "scenes": len(ep.get("composite_of", [])),
                "duration_seconds": ep["metadata"].get("total_seconds", 0),
                "duration_minutes": ep["metadata"].get("total_minutes", 0),
            })
        print(json.dumps(manifest, indent=2))
        return

    # Initialize clients
    if not args.dry_run:
        openai_client = get_openai_client()
        fal_client = get_fal_client() if not args.images_only and not args.skip_video else None
    else:
        openai_client = None
        fal_client = None

    # Find episodes to process
    episodes = [i for i in grammar["items"] if i.get("level") == 2]

    if args.episode:
        episode_ids = [args.episode if args.episode.startswith("episode-") else f"episode-{args.episode}"]
    elif args.episodes:
        episode_ids = [e if e.startswith("episode-") else f"episode-{e}" for e in args.episodes.split(",")]
    elif args.batch:
        episode_ids = [ep["id"] for ep in episodes[:args.batch]]
    else:
        episode_ids = [ep["id"] for ep in episodes]

    # Process episodes
    output_dir = Path(args.output) / grammar_slug
    all_results = []

    for ep_id in episode_ids:
        result = process_episode(
            grammar, ep_id, str(output_dir),
            openai_client, fal_client,
            dry_run=args.dry_run,
            image_model=args.image_model,
            video_model=video_model,
            skip_video=args.images_only or args.skip_video,
            skip_tts=args.images_only or args.skip_tts,
        )
        if result:
            all_results.append(result)

    # Write results manifest
    manifest_path = output_dir / "production-manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Done! {len(all_results)} episodes processed", file=sys.stderr)
    print(f"Manifest: {manifest_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
