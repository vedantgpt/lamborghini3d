#!/usr/bin/env python3
"""Strip badges/emblems from already-generated stills via Gemini image edit."""

from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
import io

from config import ASSETS, LOCATION, PROJECT, WORK
from generate_stills import extract_image_bytes, save_still

EDIT = (
    "Edit this exact photograph. Remove every badge, emblem, crest, and logo from "
    "the car, especially the gold shield on the nose. Leave a blank smooth Verde "
    "Mantis green unmarked surface. Do not change camera angle, lighting, body "
    "shape, headlights, or background. Keep cinematic 16:9. No text."
)

NAMES = ["forge", "reveal", "rollout", "road"]


def main():
    c = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    for name in NAMES:
        src = WORK / f"still_{name}.png"
        print(f"edit {name}")
        response = c.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[
                types.Part.from_bytes(data=src.read_bytes(), mime_type="image/png"),
                EDIT,
            ],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"),
            ),
        )
        data = extract_image_bytes(response)
        if not data:
            raise RuntimeError(f"no image for {name}: {response}")
        save_still(name, data)


if __name__ == "__main__":
    main()
