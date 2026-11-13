"""Create a deterministic, non-confidential reference for an image-edit access test."""
from pathlib import Path

from PIL import Image, ImageDraw


def main():
    destination = Path(__file__).resolve().parents[1] / "data" / "synthetic_reference.png"
    if destination.exists():
        raise SystemExit(f"Reference already exists: {destination}")
    image = Image.new("RGB", (1024, 1024), "#faf6ee")
    draw = ImageDraw.Draw(image)
    draw.ellipse((220, 730, 825, 815), fill="#e5ded2")
    draw.ellipse((585, 365, 820, 665), fill="#397daa")
    draw.ellipse((635, 415, 770, 615), fill="#faf6ee")
    draw.rounded_rectangle((275, 335, 675, 755), radius=65, fill="#397daa")
    draw.ellipse((275, 305, 675, 425), fill="#91c4dd")
    draw.ellipse((300, 330, 650, 400), fill="#22455b")
    draw.rounded_rectangle((312, 440, 341, 665), radius=14, fill="#77b2d2")
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)
    print(destination)


if __name__ == "__main__":
    main()
