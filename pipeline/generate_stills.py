#!/usr/bin/env python3
"""Generate 6 cohesive 16:9 stills on Vertex (Nano Banana Pro / Gemini image)."""

from __future__ import annotations

import io
import sys
import traceback
from pathlib import Path

from PIL import Image
from google import genai
from google.genai import types

from config import (
    ASPECT,
    ASSETS,
    LOCATION,
    PROJECT,
    SECTIONS,
    STILL_FALLBACKS,
    STILL_MODEL,
    WORK,
    still_prompt,
)

WORK.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)


def client():
    return genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


def extract_image_bytes(response) -> bytes | None:
    if getattr(response, "generated_images", None):
        img = response.generated_images[0].image
        if getattr(img, "image_bytes", None):
            return img.image_bytes
        if getattr(img, "_pil_image", None):
            buf = io.BytesIO()
            img._pil_image.save(buf, format="PNG")
            return buf.getvalue()
    cands = getattr(response, "candidates", None) or []
    for cand in cands:
        parts = getattr(getattr(cand, "content", None), "parts", None) or []
        for part in parts:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                data = inline.data
                return data if isinstance(data, bytes) else bytes(data)
            if getattr(part, "as_image", None):
                try:
                    pil = part.as_image()
                    buf = io.BytesIO()
                    pil.save(buf, format="PNG")
                    return buf.getvalue()
                except Exception:
                    pass
    return None


def generate_gemini_image(c, model: str, prompt: str) -> bytes:
    response = c.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=ASPECT,
                image_size="2K",
            ),
        ),
    )
    data = extract_image_bytes(response)
    if not data:
        raise RuntimeError(f"{model} returned no image bytes: {response}")
    return data


def generate_imagen(c, prompt: str) -> bytes:
    response = c.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=ASPECT,
            image_size="2K",
            person_generation="dont_allow",
        ),
    )
    data = extract_image_bytes(response)
    if not data:
        raise RuntimeError(f"imagen returned no image: {response}")
    return data


def save_still(name: str, data: bytes) -> Path:
    png = WORK / f"still_{name}.png"
    webp = ASSETS / f"{name}.webp"
    png.write_bytes(data)
    im = Image.open(io.BytesIO(data)).convert("RGB")
    im.save(png, format="PNG")
    im.save(webp, format="WEBP", quality=88, method=6)
    print(f"  saved {png.name} {im.size} -> {webp.name}")
    return webp


def generate_one(c, section, models):
    name = section["id"]
    prompt = still_prompt(section)
    (WORK / f"still_{name}.txt").write_text(prompt)
    last_err = None
    for model in models:
        try:
            print(f"[{name}] {model}")
            if model.startswith("imagen"):
                data = generate_imagen(c, prompt)
            else:
                data = generate_gemini_image(c, model, prompt)
            return save_still(name, data)
        except Exception as exc:
            last_err = exc
            print(f"[{name}] {model} failed: {exc}")
    raise RuntimeError(f"all models failed for {name}: {last_err}")


def main():
    only = sys.argv[1:]
    sections = [s for s in SECTIONS if not only or s["id"] in only]
    models = (STILL_MODEL,) + STILL_FALLBACKS + ("imagen-4.0-generate-001",)
    c = client()
    ok = True
    for section in sections:
        try:
            generate_one(c, section, models)
        except Exception:
            ok = False
            traceback.print_exc()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
