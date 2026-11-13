import fal_client
import os
import time
from pathlib import Path
import argparse
from typing import Optional

os.environ["FAL_KEY"] = (
    "530ec3e1-db84-4ff7-852c-09387cafae14:762468a73f52bc85c086b40483746537"
)


def on_queue_update(update: fal_client.InProgress) -> None:
    if isinstance(update, fal_client.InProgress) and update.logs:
        for log in update.logs:
            print(log["message"])


def generate_video(prompt: str, output_dir: str, index: int, api: str) -> None:
    """Generate a video from a prompt and save it to disk"""
    try:
        # Generate the video
        result = fal_client.subscribe(
            api,
            arguments={"prompt": prompt},
            with_logs=True,
            on_queue_update=on_queue_update,
        )

        # Extract video URL
        video_url = result["video"]["url"]

        # Create a filename based on the index
        filename = f"video_{index:03d}.mp4"
        output_path = os.path.join(output_dir, filename)

        # Download the video
        # Since fal_client.download_file doesn't exist, we'll use requests
        import requests

        response = requests.get(video_url)
        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"Successfully generated and saved video {index} to {output_path}")

        # Add a small delay between requests to avoid rate limiting
        time.sleep(2)

    except Exception as e:
        print(f"Error generating video {index}: {str(e)}")


def main() -> None:
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate videos from text prompts")
    parser.add_argument(
        "--input",
        type=str,
        help="Path to the text file containing prompts",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Directory to save the generated videos",
        required=True,
    )
    parser.add_argument(
        "--api",
        type=str,
        help="API endpoint to use (e.g. 'fal-ai/wan-t2v' or 'fal-ai/kling-video/v1.5/pro/text-to-video')",
        required=True,
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    Path(args.output).mkdir(parents=True, exist_ok=True)

    # Read the prompts file
    try:
        with open(args.input, "r") as f:
            prompts = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found")
        return
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return

    # Process each prompt
    for i, prompt in enumerate(prompts):
        prompt = prompt.strip()
        if prompt:  # Skip empty lines
            print(f"\nProcessing prompt {i+1}/{len(prompts)}:")
            print(f"Prompt: {prompt}")
            generate_video(prompt, args.output, i + 1, args.api)


if __name__ == "__main__":
    main()
