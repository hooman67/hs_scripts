import math
import pandas as pd
from PIL import Image
import os


def find_closest_dimensions(
    image_dim: tuple[int, int], request_dim: tuple[int, int]
) -> tuple[int, int]:
    """
    Finds the largest dimensions that maintain the aspect ratio of image_dim,
    have width and height as multiples of 32, and do not exceed the total
    pixels of request_dim.

    If no such dimension exists below the requested pixel limit, it finds the
    smallest dimension that meets the aspect ratio and multiple-of-32 criteria,
    even if it exceeds the requested pixel limit (implying cropping is needed).

    Args:
        image_dim: The original image dimensions as (width, height).
        request_dim: The requested dimensions as (width, height).

    Returns:
        A tuple (width, height) representing the calculated dimensions.
    """
    img_w, img_h = image_dim
    req_w, req_h = request_dim
    max_pixels = req_w * req_h

    # Calculate aspect ratio
    aspect_ratio = img_w / img_h

    # Start with a width of 32 and keep increasing by 32 until we exceed the max width
    # or the resulting dimensions exceed max_pixels
    best_width = 32
    best_height = 32

    # Calculate the maximum width we need to consider (a reasonable limit)
    max_possible_width = min(32768, int(math.sqrt(max_pixels * aspect_ratio) * 1.5))

    for width in range(32, max_possible_width + 32, 32):
        # Calculate the corresponding height that maintains the aspect ratio,
        # rounded to the nearest multiple of 32
        height = 32 * round((width / aspect_ratio) / 32)
        if height < 32:
            height = 32

        # Check if these dimensions exceed the max_pixels limit
        if width * height > max_pixels:
            break

        # Update our best dimensions
        best_width = width
        best_height = height

    return best_width, best_height


def get_image_dimensions(image_path: str) -> tuple[int, int]:
    """
    Get the dimensions of an image file.

    Args:
        image_path: Path to the image file

    Returns:
        A tuple (width, height) of the image dimensions
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return (0, 0)


def process_csv(input_csv: str, output_csv: str):
    """
    Process a CSV file containing image paths and add dimensions information.
    Automatically chooses request dimensions based on image orientation:
    - Horizontal images (width > height): 1920x1080
    - Vertical images (height > width): 1080x1920

    Args:
        input_csv: Path to the input CSV file
        output_csv: Path to save the output CSV file
    """
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Initialize lists to store results
    input_dims = []
    generated_dims = []
    orientations = []

    # Process each image
    for image_path in df["image"]:
        # Get input image dimensions
        dims = get_image_dimensions(image_path)
        input_dims.append(f"{dims[0]}x{dims[1]}")

        # Calculate generated dimensions
        if dims != (0, 0):
            # Choose request dimensions based on orientation
            if dims[0] > dims[1]:  # Horizontal
                request_dim = (1920, 1080)
                orientations.append("horizontal")
            else:  # Vertical or square
                request_dim = (1080, 1920)
                orientations.append("vertical")

            gen_dims = find_closest_dimensions(dims, request_dim)
            generated_dims.append(f"{gen_dims[0]}x{gen_dims[1]}")
        else:
            generated_dims.append("0x0")
            orientations.append("unknown")

    # Create new DataFrame with results
    result_df = pd.DataFrame(
        {
            "image": df["image"],
            "input_image_dims": input_dims,
            "orientation": orientations,
            "generated_dims": generated_dims,
        }
    )

    # Save to CSV
    result_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")


if __name__ == "__main__":
    # Example usage
    input_csv = (
        "/sensei-fs/users/hshariati/eval_sets/i2v/tencent_i2v-1.0_standardized.csv"
    )
    output_csv = "/sensei-fs/users/hshariati/hs_scripts/tencent_i2v-1.0_standardized_with_dims.csv"
    process_csv(input_csv, output_csv)


# Example usage:
image_dim = (612, 447)
request_dim = (1920, 1088)
result = find_closest_dimensions(image_dim, request_dim)
print(result)  # Should output (1632, 1184)

# Example case where no solution fits under the limit
image_dimension_small = (408, 612)
request_dimension_small = (50, 50)
result_small = find_closest_dimensions(image_dimension_small, request_dimension_small)
print(
    f"Image: {image_dimension_small}, Request: {request_dimension_small} -> Result: {result_small}"
)
# Expected: (64, 96) (smallest valid dimension, larger than request)

# Example case that fits under the limit
image_dimension_medium = (408, 612)
request_dimension_medium = (500, 500)
result_medium = find_closest_dimensions(
    image_dimension_medium, request_dimension_medium
)
print(
    f"Image: {image_dimension_medium}, Request: {request_dimension_medium} -> Result: {result_medium}"
)
# Expected: (384, 576)
