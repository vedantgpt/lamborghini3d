#!/usr/bin/env python3
"""Veo 3.1 dive + connector chain on Vertex. Frames via GCS. Extracted-frame seams."""

from __future__ import annotations

import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

from google import genai
from google.cloud import storage
from google.genai import types

from config import (
    ASPECT,
    BUCKET,
    CONNECTORS,
    DURATION,
    GCS_PREFIX,
    LOCATION,
    NEGATIVE,
    PROJECT,
    SECTIONS,
    VIDEO_MODEL,
    WORK,
    conn_prompt,
    dive_prompt,
)

WORK.mkdir(parents=True, exist_ok=True)
FFMPEG = os.environ.get(
    "FFMPEG",
    str(Path(__file__).resolve().parent / "ffmpeg"),
)


def client():
    return genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


def ensure_bucket():
    gcs = storage.Client(project=PROJECT)
    bucket = gcs.lookup_bucket(BUCKET)
    if bucket is None:
        bucket = gcs.create_bucket(BUCKET, location=LOCATION, project=PROJECT)
        print(f"created gs://{BUCKET}")
    # Vertex service agent needs object admin for output videos.
    policy = bucket.get_iam_policy(requested_policy_version=3)
    member = f"serviceAccount:service-808000446225@gcp-sa-aiplatform.iam.gserviceaccount.com"
    role = "roles/storage.objectAdmin"
    binding = next((b for b in policy.bindings if b["role"] == role), None)
    if binding is None:
        policy.bindings.append({"role": role, "members": {member}})
        bucket.set_iam_policy(policy)
    elif member not in binding["members"]:
        binding["members"].add(member)
        bucket.set_iam_policy(policy)
    return gcs


def upload(gcs, local: Path, dest_name: str) -> str:
    blob = gcs.bucket(BUCKET).blob(dest_name)
    blob.upload_from_filename(str(local))
    uri = f"{GCS_PREFIX}/{dest_name}"
    print(f"  uploaded {uri}")
    return uri


def download_gcs(gcs, uri: str, dest: Path):
    assert uri.startswith("gs://")
    _, _, rest = uri.partition("gs://")
    bucket_name, _, name = rest.partition("/")
    gcs.bucket(bucket_name).blob(name).download_to_filename(str(dest))


def wait_op(c, op, label: str):
    while not op.done:
        print(f"  {label} running…")
        time.sleep(20)
        op = c.operations.get(op)
    if getattr(op, "error", None):
        raise RuntimeError(f"{label} error: {op.error}")
    return op


def generate_clip(c, gcs, prompt: str, out_mp4: Path, first_uri: str, last_uri: str | None, seed: int, label: str):
    cfg_kw = dict(
        aspect_ratio=ASPECT,
        duration_seconds=DURATION,
        resolution="1080p",
        generate_audio=False,
        negative_prompt=NEGATIVE,
        seed=seed,
        output_gcs_uri=f"{GCS_PREFIX}/out/{label}/",
        number_of_videos=1,
        person_generation="dont_allow",
    )
    if last_uri:
        cfg_kw["last_frame"] = types.Image(gcs_uri=last_uri, mime_type="image/png")
    op = c.models.generate_videos(
        model=VIDEO_MODEL,
        source=types.GenerateVideosSource(
            prompt=prompt,
            image=types.Image(gcs_uri=first_uri, mime_type="image/png"),
        ),
        config=types.GenerateVideosConfig(**cfg_kw),
    )
    op = wait_op(c, op, label)
    result = op.response or op.result
    videos = getattr(result, "generated_videos", None) or []
    if not videos:
        raise RuntimeError(f"{label} no videos: {result}")
    video = videos[0].video
    if getattr(video, "uri", None):
        download_gcs(gcs, video.uri, out_mp4)
    elif getattr(video, "video_bytes", None):
        out_mp4.write_bytes(video.video_bytes)
    else:
        raise RuntimeError(f"{label} video had no uri/bytes")
    print(f"  wrote {out_mp4}")
    return out_mp4


def extract_frame(src: Path, dest: Path, last: bool):
    args = [FFMPEG, "-v", "error", "-y"]
    if last:
        args += ["-sseof", "-0.05"]
    else:
        args += ["-ss", "0"]
    args += ["-i", str(src), "-frames:v", "1", "-q:v", "1", str(dest)]
    subprocess.check_call(args)
    print(f"  frame {dest.name}")


def gen_dives(c, gcs, names):
    by_id = {s["id"]: s for s in SECTIONS}
    for name in names:
        section = by_id[name]
        still = WORK / f"still_{name}.png"
        if not still.exists():
            raise FileNotFoundError(still)
        first_uri = upload(gcs, still, f"stills/{name}.png")
        prompt = dive_prompt(section)
        (WORK / f"dive_{name}.txt").write_text(prompt)
        out = WORK / f"dive_{name}.mp4"
        generate_clip(c, gcs, prompt, out, first_uri, None, section["seed"], f"dive-{name}")
        extract_frame(out, WORK / f"first_{name}.png", last=False)
        extract_frame(out, WORK / f"last_{name}.png", last=True)


def gen_conns(c, gcs, ids):
    by_id = {x["id"]: x for x in CONNECTORS}
    for cid in ids:
        conn = by_id[cid]
        start = WORK / f"last_{conn['from']}.png"
        end = WORK / f"first_{conn['to']}.png"
        if not start.exists() or not end.exists():
            raise FileNotFoundError(f"need {start} and {end} (extracted frames, not stills)")
        su = upload(gcs, start, f"frames/conn{cid}_start.png")
        eu = upload(gcs, end, f"frames/conn{cid}_end.png")
        prompt = conn_prompt(conn)
        (WORK / f"conn_{cid}.txt").write_text(prompt)
        out = WORK / f"conn_{cid}.mp4"
        generate_clip(c, gcs, prompt, out, su, eu, conn["seed"], f"conn-{cid}")


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: generate_videos.py dives [ids...] | conns [ids...] | all")
        return 2
    cmd = args[0]
    rest = args[1:]
    gcs = ensure_bucket()
    c = client()
    try:
        if cmd == "dives":
            names = rest or [s["id"] for s in SECTIONS]
            gen_dives(c, gcs, names)
        elif cmd == "conns":
            ids = rest or [x["id"] for x in CONNECTORS]
            gen_conns(c, gcs, ids)
        elif cmd == "all":
            gen_dives(c, gcs, [s["id"] for s in SECTIONS])
            gen_conns(c, gcs, [x["id"] for x in CONNECTORS])
        else:
            print("unknown command", cmd)
            return 2
    except Exception:
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
