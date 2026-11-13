from __future__ import annotations

import sys
from google import genai  # type: ignore[import-not-found]
from google.genai import types  # type: ignore[import-not-found]

import io
from datetime import datetime
from pathlib import Path

from PIL import Image  # type: ignore[import-not-found]

PROJECT_ID = "adbe-gcp0805"
LOCATION = "global"

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
MODEL_ID = "gemini-3-pro-image-preview"


def downscale(img: Image.Image, max_side: int = 1536) -> Image.Image:
    """Downscale while keeping aspect ratio to reduce tokens/cost."""
    w, h = img.size
    scale = max(w, h) / max_side
    if scale <= 1:
        return img
    new_w, new_h = int(w / scale), int(h / scale)
    return img.resize((new_w, new_h), Image.LANCZOS)


def generate_image_with_prompt(
    img: Image.Image, prompt: str, size: str = "1920x1088"
) -> Image.Image:
    img = downscale(img, max_side=1920)

    img_to_bytes = io.BytesIO()
    img.save(img_to_bytes, format="PNG")
    contents = [
        types.Part.from_bytes(data=img_to_bytes.getvalue(), mime_type="image/png"),
        prompt,
    ]
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=contents,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )
    return Image.open(io.BytesIO(response.candidates[0].content.parts[0].inline_data.data))


if __name__ == "__main__":
    img = Image.open("/Users/hshariati/Desktop/product_finetuning/drill/ref1.jpg")
    prompt = "use the model image as reference, and generate a scene where this tool is being used"
    output = generate_image_with_prompt(img, prompt)

    out_dir = Path("/Users/hshariati/Desktop")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"image_synth_gemeni_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    output.save(out_path)
    print(f"Saved: {out_path.resolve()}")
