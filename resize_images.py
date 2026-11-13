import csv
import os
from PIL import Image
from pathlib import Path
from typing import Dict, List, Any


def resize_and_center_crop(image: Image.Image, new_width: int, new_height: int) -> Image.Image:
    # Get the dimensions of the original image
    original_width, original_height = image.size

    # Calculate aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate the aspect ratio of the new size
    new_aspect_ratio = new_width / new_height

    # Resize the image while maintaining aspect ratio
    if new_aspect_ratio > aspect_ratio:
        # If the new aspect ratio is wider, adjust height
        resize_height = int(new_width / aspect_ratio)
        image = image.resize((new_width, resize_height), Image.LANCZOS)  # type: ignore # https://jira.corp.adobe.com/browse/FFP-25444
    else:
        # If the new aspect ratio is taller or equal, adjust width
        resize_width = int(new_height * aspect_ratio)
        image = image.resize((resize_width, new_height), Image.LANCZOS)  # type: ignore # https://jira.corp.adobe.com/browse/FFP-25444

    # Get the updated dimensions after resizing
    updated_width, updated_height = image.size

    # Calculate the coordinates for the center crop
    left = (updated_width - new_width) / 2
    top = (updated_height - new_height) / 2
    right = (updated_width + new_width) / 2
    bottom = (updated_height + new_height) / 2

    # Perform the center crop
    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image


def process_images(csv_path: str, output_dir: str, output_csv_path: str) -> None:
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read all rows from input CSV
    rows: List[Dict[str, Any]] = []
    with open(csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ["resized_image"] if reader.fieldnames else []
        rows = list(reader)

    # Process each image and update rows
    for row in rows:
        # Parse image path and dimensions
        image_path = row["image"]
        width, height = map(int, row["generated_dims"].split("x"))

        try:
            # Open the image
            with Image.open(image_path) as img:
                # Resize the image
                resized_img = resize_and_center_crop(img, width, height)

                # Create output path
                output_path = os.path.join(output_dir, os.path.basename(image_path))

                # Save the resized image
                resized_img.save(output_path)
                print(f"Processed: {image_path} -> {output_path}")

                # Add resized image path to row
                row["resized_image"] = output_path

        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            row["resized_image"] = "ERROR"

    # Write updated rows to output CSV
    with open(output_csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Output CSV saved to: {output_csv_path}")


if __name__ == "__main__":
    csv_path = "/sensei-fs/users/hshariati/hs_scripts/tencent_i2v-1.0_standardized_with_dims.csv"
    output_dir = "/sensei-fs/users/hshariati/eval_sets/i2v/resized_images"
    output_csv_path = "/sensei-fs/users/hshariati/hs_scripts/tencent_i2v-1.0_standardized_with_dims_resized.csv"

    process_images(csv_path, output_dir, output_csv_path)
