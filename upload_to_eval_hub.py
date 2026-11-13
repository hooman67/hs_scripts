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
    VideoInput,
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
        "input_type": "VideoInput",
        "input_class": VideoInput,
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
    df: pd.DataFrame, task: str, eval_set: str, eval_set_version: str, run_id: str
) -> list[AssetCreateRequest]:
    """Create asset requests based on the task type and data."""
    asset_create_list = []
    input_class = TASK_CONFIGS[task]["input_class"]

    for idx, row in df.iterrows():
        print(f"Processing row {idx}...")
        if "video_sensei_paths" in row:
            video_path = os.path.basename(
                str(ast.literal_eval(row.video_sensei_paths)[0][0])
            )
        else:
            video_path = os.path.basename(
                str(ast.literal_eval(row.sensei_video_paths)[0])
            )

        if task == "t2v":
            asset_request = AssetCreateRequest(
                asset_url=eval_service.get_asset_url(run_id, video_path),
                model_input=input_class(
                    eval_set_item_id=str(row.eval_set_item_id)
                    if "eval_set_item_id" in row
                    else f"{eval_set}_{eval_set_version}_{idx}",
                    eval_set_name=eval_set,
                    prompt=str(row.prompt),
                    negative_prompt=str(row.negative_prompt),
                ),
                mime_type="video/mp4",
            )

        elif task == "i2v":
            image_url = str(ast.literal_eval(row.image_urls)[0]).replace(
                "http://clio.corp.adobe.com/", "https://clio-web-app.s3.amazonaws.com/"
            )
            image_url = image_url.replace(
                "https://clio.corp.adobe.com/", "https://clio-web-app.s3.amazonaws.com/"
            )
            asset_request = AssetCreateRequest(
                asset_url=eval_service.get_asset_url(run_id, video_path),
                model_input=input_class(
                    # eval_set_item_id=str(row.eval_set_item_id),
                    eval_set_item_id=f"{eval_set}_{eval_set_version}_{idx}",
                    eval_set_name=eval_set,
                    image_url=image_url,
                ),
                mime_type="video/mp4",
            )

        elif task == "v2v":
            asset_request = AssetCreateRequest(
                asset_url=eval_service.get_asset_url(run_id, str(row.stitched_videos)),
                model_input=input_class(
                    eval_set_item_id=str(row.eval_set_item_id),
                    eval_set_name=eval_set,
                    video_url="https://clio-web-app.s3.amazonaws.com/input.mp4",
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
        "--csv_paths",
        type=str,
        nargs="+",  # Allow multiple CSV paths
        required=True,
        help="Paths to the CSV files containing the data",
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
        default="false",
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

    uploader = S3Uploader(eval_service)
    # assert s3_handle.s3.meta.config.signature_version == UNSIGNED

    # Process each CSV file
    all_asset_requests = []
    for csv_path in args.csv_paths:
        # Upload directory to S3
        assets_folder_path = str(Path(csv_path).parent)
        print(f"\n3. Uploading directory {assets_folder_path} to S3...")
        uploader.upload_directory(directory_path=assets_folder_path, run_id=run_id)
        print("Directory upload complete!")

        # Create asset requests
        print(f"\n4. Creating asset requests for {csv_path}...")
        df = pd.read_csv(csv_path)
        asset_create_list = create_asset_requests(
            df, args.task, args.eval_set, args.eval_set_version, run_id
        )
        all_asset_requests.extend(asset_create_list)
        print(f"Created {len(asset_create_list)} asset requests for {csv_path}")

    # Upload all assets to SSEval
    print("\n5. Uploading assets to SSEval...")
    eval_service.create_assets(run_id=run_id, assets=all_asset_requests)
    print(f"\nSuccess! Assets created for run_id: {run_id}")
    print(f"You can verify your uploaded assets at: s3://clio-web-app/{run_id}")


if __name__ == "__main__":
    main()

# sample command: python upload_to_eval_hub.py --task t2v --csv_paths file1.csv file2.csv file3.csv --jira FFP-12345
