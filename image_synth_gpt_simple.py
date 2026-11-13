import base64
import io
from datetime import datetime
from os import environ
from pathlib import Path

from openai import OpenAI  # type: ignore[import-not-found]
from PIL import Image  # type: ignore[import-not-found]

MODEL = "gpt-image-1.5"
URL = "https://camp-azr14080-rnig4.cognitiveservices.azure.com/openai/v1/"
TOKEN = environ["AZURE_OPENAI_TOKEN"]


client = OpenAI(api_key=TOKEN, base_url=URL)


def downscale(img: Image.Image, max_side: int = 1536) -> Image.Image:
    """Downscale while keeping aspect ratio to reduce tokens/cost."""
    w, h = img.size
    scale = max(w, h) / max_side
    if scale <= 1:
        return img
    new_w, new_h = int(w / scale), int(h / scale)
    return img.resize((new_w, new_h), Image.LANCZOS)


def generate_image_with_prompt(img: Image.Image, prompt: str, size: str = "1920x1088") -> Image.Image:
    # downsample image with max side
    img = downscale(img, max_side=1920)
    # convert img to in-memory png file
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    buf.name = "image.png"
    image_files = [buf]
    response = client.images.edit(
        model=MODEL,
        image=image_files,
        prompt=prompt,
        n=1,
        size=size,
    )
    image_data = response.data[0].b64_json
    return Image.open(io.BytesIO(base64.b64decode(image_data)))


if __name__ == "__main__":
    img = Image.open("/Users/hshariati/Desktop/ref_images_trimmer/ref1.png")
    prompt = "use the model image as reference, and generate a scene where this tool is being used"
    output = generate_image_with_prompt(img, prompt)

    out_dir = Path("/Users/hshariati/Desktop")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"image_synth_gpt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    output.save(out_path)
    print(f"Saved: {out_path.resolve()}")

