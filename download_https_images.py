import pandas as pd
import requests
import os
from ast import literal_eval
from pathlib import Path

# Set up constants
CSV_PATH = './tencent_i2v-1.0_standardized.csv'
OUTPUT_DIR = './images_tencent'

def download_image(url, output_path):
    """Download an image from a URL and save it to the specified path"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded: {output_path}")

    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def main():
    # Create output directory if it doesn't exist
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Read the CSV file
    df = pd.read_csv(CSV_PATH)

    # Process each row
    for index, row in df.iterrows():
        # Convert string representation of list to actual list
        urls = literal_eval(row['image_urls'])

        # Get the image filename from the image path
        image_path = row['image']
        image_filename = os.path.basename(image_path)

        # Download each image (though in this case there's only one per row)
        for url in urls:
            output_path = os.path.join(OUTPUT_DIR, image_filename)
            download_image(url, output_path)

if __name__ == "__main__":
    main()