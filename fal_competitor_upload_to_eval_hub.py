#!/usr/bin/env python3

import sys
import subprocess
import importlib.util
import os
import ast
import argparse
import pandas as pd
from pathlib import Path


def check_and_install_eval_service():
    """Check if eval_service_common is installed, if not install it."""
    if importlib.util.find_spec("eval_service_common") is None:
        print("eval_service_common package not found. Installing...")

        # Create .netrc file for authentication
        netrc_path = os.path.expanduser("~/.netrc")
        with open(netrc_path, "w") as f:
            f.write(f"""machine artifactory-uw2.adobeitc.com
login {os.environ['ARTIFACTORY_UW2_USER']}
password {os.environ['ARTIFACTORY_UW2_API_TOKEN']}""")

        # Set proper permissions for .netrc
        os.chmod(netrc_path, 0o600)

        install_cmd = [
            "pip",
            "install",
            "--no-cache-dir",
            "--index-url",
            "https://artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-eval-service-common-release-local/simple",
            "--trusted-host",
            "artifactory-uw2.adobeitc.com",
            "eval_service_common",
        ]
        try:
            subprocess.check_call(install_cmd)
            print("Successfully installed eval_service_common")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install eval_service_common: {e}")
            sys.exit(1)
        finally:
            # Clean up .netrc file
            if os.path.exists(netrc_path):
                os.remove(netrc_path)


# Check and install eval_service_common if needed
check_and_install_eval_service()

# this must happen after we install sseval package.
from eval_service_common.eval_service import EvalService
from eval_service_common.uploader import S3Uploader
from botocore import UNSIGNED
from eval_service_common.api_types import AssetCreateRequest
from eval_service_common.model_input_types import (
    PromptAndNegativePromptInput,
    Image2VideoInput,
    GenExtendVideoInput,
)

# Configure environment
os.environ["EVAL_SERVICE_API_KEY"] = "EvalServiceTest"

# Task-specific configurations
TASK_CONFIGS = {
    "t2v": {
        "default_eval_set": "t2vid_general_100",
        "input_type": "PromptAndNegativePromptInput",
        "input_class": PromptAndNegativePromptInput,
        "default_eval_set_version": "1.2",
    },
    "i2v": {
        "default_eval_set": "i2v_general_145",
        "input_type": "Image2VideoInput",
        "input_class": Image2VideoInput,
        "default_eval_set_version": "1.0",
    },
    "v2v": {
        "default_eval_set": "v2v_genextend_general_100",
        "input_type": "GenExtendVideoInput",
        "input_class": GenExtendVideoInput,
        "default_eval_set_version": "1.2",
    },
}


def create_asset_requests(
    prompts: list[str],
    video_folder: str,
    task: str,
    eval_set: str,
    eval_set_version: str,
    run_id: str,
) -> list[AssetCreateRequest]:
    """Create asset requests based on the task type and prompts."""
    asset_create_list = []
    input_class = TASK_CONFIGS[task]["input_class"]

    for idx, prompt in enumerate(prompts, 1):  # Start from 1 to match video naming
        print(f"Processing prompt {idx}...")
        # video_path = f"video_{idx:03d}.mp4"  # Creates names like video_001.mp4
        video_path = f"{idx}.mp4"  # Creates names like 1.mp4

        # Verify video exists
        full_video_path = os.path.join(video_folder, video_path)
        if not os.path.exists(full_video_path):
            print(f"Warning: Video file {video_path} not found in {video_folder}")
            continue

        if task == "t2v":
            asset_request = AssetCreateRequest(
                asset_url=eval_service.get_asset_url(run_id, video_path),
                model_input=input_class(
                    eval_set_item_id=f"{eval_set}_{eval_set_version}_{idx}",
                    eval_set_name=eval_set,
                    prompt=prompt,
                    negative_prompt="",  # Empty negative prompt
                ),
                mime_type="video/mp4",
            )
            asset_create_list.append(asset_request)

    return asset_create_list


def main():
    parser = argparse.ArgumentParser(description="Upload assets to eval hub")
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        choices=["t2v", "i2v", "v2v"],
        help="Task type: t2v (text-to-video), i2v (image-to-video), or v2v (video-to-video)",
    )
    parser.add_argument(
        "--video_folder",
        type=str,
        required=True,
        help="Path to the folder containing the videos",
    )
    parser.add_argument(
        "--prompt_file",
        type=str,
        required=True,
        help="Path to the text file containing prompts",
    )
    parser.add_argument(
        "--jira", type=str, required=True, help="Run ID prefix (e.g., FFP-31734)"
    )
    parser.add_argument(
        "--eval_set", type=str, help="Evaluation set name (defaults based on task)"
    )
    parser.add_argument(
        "--eval_set_version",
        type=str,
        help="Evaluation set version (defaults to latest version if not specified)",
    )
    parser.add_argument(
        "--ldap",
        type=str,
        default="hshariati",
        help="LDAP username (default: hshariati)",
    )
    parser.add_argument(
        "--num_variations",
        type=int,
        default=1,
        help="Number of variations (default: 1)",
    )
    parser.add_argument(
        "--link_to_eval",
        type=str,
        default="true",
        help="Whether to link to eval set (default: True)",
    )

    args = parser.parse_args()

    # Convert string to boolean
    link_to_eval = args.link_to_eval.lower() == "true"

    # Set eval_set if not provided
    if not args.eval_set:
        args.eval_set = TASK_CONFIGS[args.task]["default_eval_set"]
    if not args.eval_set_version:
        args.eval_set_version = TASK_CONFIGS[args.task]["default_eval_set_version"]

    # Initialize eval service
    print("\n1. Initializing EvalService...")
    global eval_service
    eval_service = EvalService()

    # Create generation
    print("\n2. Creating generation...")
    run_id = eval_service.create_generation(
        eval_set=args.eval_set,
        eval_set_version=args.eval_set_version,
        model_input_type=TASK_CONFIGS[args.task]["input_type"],
        model_id=args.jira,
        created_by=args.ldap,
        num_of_variations=args.num_variations,
        link_to_eval_set=link_to_eval,
        for_harm_eval=False,
    )

    print(f"Generated run_id: {run_id}")

    # Read prompts from text file
    print(f"\n3. Reading prompts from {args.prompt_file}...")
    with open(args.prompt_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    uploader = S3Uploader(eval_service)

    # Upload directory to S3
    print(f"\n4. Uploading directory {args.video_folder} to S3...")
    uploader.upload_directory(directory_path=args.video_folder, run_id=run_id)
    print("Directory upload complete!")

    # Create asset requests
    print("\n5. Creating asset requests...")
    asset_create_list = create_asset_requests(
        prompts,
        args.video_folder,
        args.task,
        args.eval_set,
        args.eval_set_version,
        run_id,
    )
    print(f"Created {len(asset_create_list)} asset requests")

    # Upload all assets to SSEval
    print("\n6. Uploading assets to SSEval...")
    eval_service.create_assets(run_id=run_id, assets=asset_create_list)
    print(f"\nSuccess! Assets created for run_id: {run_id}")
    print(f"You can verify your uploaded assets at: s3://clio-web-app/{run_id}")


if __name__ == "__main__":
    main()

# sample command: python fal_competitor_upload_to_eval_hub.py --task t2v --video_folder /path/to/videos --prompt_file /path/to/prompts.txt --jira FFP-12345 --eval_set physics --eval_set_version 0.0 --link_to_eval false
