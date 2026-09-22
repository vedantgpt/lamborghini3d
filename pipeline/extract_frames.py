#!/usr/bin/env python3
"""Break scrub clips into static WebP frames so the page does not depend on video seek."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VID = ROOT / "assets" / "vid"
OUT = ROOT / "assets" / "frames"
FFMPEG = os.environ.get(
    "FFMPEG",
    str(
        ROOT
        / ".venv/lib/python3.14/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
    ),
)

CLIPS = [
    "ore",
    "conn1",
    "forge",
    "conn2",
    "assembly",
    "conn3",
    "reveal",
    "conn4",
    "rollout",
    "conn5",
    "road",
]


def extract(name: str) -> int:
    src = VID / f"{name}.mp4"
    dest = OUT / name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    subprocess.check_call(
        [
            FFMPEG,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(src),
            "-vf",
            "fps=12,scale=1280:-2",
            "-c:v",
            "libwebp",
            "-quality",
            "62",
            "-compression_level",
            "4",
            str(dest / "tmp%03d.webp"),
        ]
    )
    files = sorted(dest.glob("tmp*.webp"))
    for i, path in enumerate(files):
        path.rename(dest / f"{i:03d}.webp")
    print(f"{name}: {len(files)} frames")
    return len(files)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(extract, name): name for name in CLIPS}
        for fut in as_completed(futures):
            counts[futures[fut]] = fut.result()
    manifest = {
        "dir": "assets/frames",
        "ext": "webp",
        "pad": 3,
        "fps": 12,
        "clips": {name: counts[name] for name in CLIPS},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {OUT / 'manifest.json'}")


if __name__ == "__main__":
    main()
