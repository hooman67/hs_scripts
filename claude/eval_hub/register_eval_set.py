#!/usr/bin/env python3
# Copyright 2026 Adobe. All rights reserved.

"""Register the Humain eval set with the Evaluation Hub.

Reads prompts from humain_eval_set.txt (one prompt per line), uploads
generated images from Humain/inference/assets/, and registers everything
with the EvalService.

Assets follow the naming convention: row{i}_img{j}.png
  - i = prompt index (0-638)
  - j = variation index (0-9)

Usage:
    export EVAL_SERVICE_API_KEY=humain_eval_upload
    python Humain/register_eval_set.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from eval_service_common.api_types import AssetCreateRequest
from eval_service_common.eval_service import EvalService
from eval_service_common.model_input_types import PromptInput
from eval_service_common.uploader import S3Uploader
from tqdm import tqdm

EVAL_SET_NAME = "humain_t2i_gpt_592"
EVAL_SET_VERSION = "1.0"
MODEL_ID = "h06_v13_iter_1026000_expanded_prompts"
CREATED_BY = "hshariati"
NUM_VARIATIONS = 2
PROMPTS_FILE = Path(__file__).parent / "Humain" / "humain_eval_set.txt"
ASSET_DIR = Path(__file__).parent / "Humain" / "inference" / "assets"


def main() -> None:
    api_key = "humain_eval_upload"
    if not api_key:
        os.environ["EVAL_SERVICE_API_KEY"] = api_key
        print("ERROR: EVAL_SERVICE_API_KEY environment variable is not set.")
        print("Set it with: export EVAL_SERVICE_API_KEY='<your-key>'")
        sys.exit(1)

    # Load prompts
    with open(PROMPTS_FILE, encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip()]
    print(f"Loaded {len(prompts)} prompts from {PROMPTS_FILE}")

    # Initialize eval service
    print("\n1. Initializing EvalService...")
    eval_service = EvalService()

    # Register generation
    print("\n2. Creating generation...")
    run_id: str = eval_service.create_generation(
        eval_set=EVAL_SET_NAME,
        eval_set_version=EVAL_SET_VERSION,
        model_input_type="PromptInput",
        model_id=MODEL_ID,
        created_by=CREATED_BY,
        num_of_variations=NUM_VARIATIONS,
        link_to_eval_set=False,
    )
    print(f"   Run ID: {run_id}")

    # Upload assets to S3
    print(f"\n3. Uploading assets from {ASSET_DIR}...")
    uploader = S3Uploader(eval_service)
    uploaded_uris = uploader.upload_directory(directory_path=str(ASSET_DIR), run_id=run_id)
    print(f"   Uploaded {len(uploaded_uris)} files")

    # Build asset requests: row{i}_img{j}.png -> prompt i, variation j
    print("\n4. Building asset requests...")
    asset_create_list = []
    for i, prompt in enumerate(prompts):
        eval_set_item_id = f"{EVAL_SET_NAME}_{EVAL_SET_VERSION}_{i}"
        for j in range(NUM_VARIATIONS):
            filename = f"row{i}_img{j}.png"
            asset_url = eval_service.get_asset_url(run_id, filename)
            req = AssetCreateRequest(
                asset_url=asset_url,
                model_input=PromptInput(
                    eval_set_item_id=eval_set_item_id,
                    eval_set_name=EVAL_SET_NAME,
                    prompt=prompt,
                ),
                mime_type="image/png",
            )
            asset_create_list.append(req)
    print(f"   Created {len(asset_create_list)} asset requests")

    # Register assets
    print("\n5. Registering assets with EvalHub...")
    eval_service.create_assets(run_id=run_id, assets=asset_create_list)

    print(f"\nSuccess! Run ID: {run_id}")
    print(f"View assets at: https://evaluation-hub.adobe.io/asset-viewer?run_ids={run_id}")


if __name__ == "__main__":
    main()