#!/usr/bin/env python3
"""Encode work/*.mp4 into frame-accurate scrub clips (all-intra, no B-frames)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from config import ASSETS, CONNECTORS, SECTIONS, VID, WORK

FFMPEG = os.environ.get("FFMPEG", str(Path(__file__).resolve().parent / "ffmpeg"))


def enc(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            FFMPEG, "-v", "error", "-y", "-i", str(src),
            "-an", "-vf", "unsharp=5:5:0.8:5:5:0.0",
            "-c:v", "libx264", "-preset", "fast", "-tune", "fastdecode",
            "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high",
            "-g", "1", "-keyint_min", "1", "-bf", "0", "-refs", "1",
            "-sc_threshold", "0", "-x264-params", "keyint=1:min-keyint=1:scenecut=0:bframes=0:ref=1",
            "-movflags", "+faststart", str(dest),
        ]
    )
    print(f"enc {dest} ({dest.stat().st_size // 1024} KB)")


def poster(src: Path, dest: Path):
    subprocess.check_call(
        [
            FFMPEG, "-v", "error", "-y", "-ss", "0", "-i", str(src),
            "-frames:v", "1", str(WORK / "_poster.png"),
        ]
    )
    from PIL import Image
    Image.open(WORK / "_poster.png").convert("RGB").save(dest, format="WEBP", quality=86, method=6)
    print(f"poster {dest}")


def main():
    VID.mkdir(parents=True, exist_ok=True)
    for s in SECTIONS:
        src = WORK / f"dive_{s['id']}.mp4"
        if src.exists():
            enc(src, VID / f"{s['id']}.mp4")
            poster(src, ASSETS / f"{s['id']}-poster.webp")
    for c in CONNECTORS:
        src = WORK / f"conn_{c['id']}.mp4"
        if src.exists():
            enc(src, VID / f"conn{c['id']}.mp4")


if __name__ == "__main__":
    main()
