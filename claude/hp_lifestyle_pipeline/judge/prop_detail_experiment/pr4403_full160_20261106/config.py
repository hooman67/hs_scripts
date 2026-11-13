"""Pinned configuration for the PR 4403 V6.1 full-160 experiment."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
WORKTREE = Path("/home/colligo/foundry-pr4403-prop-exp")
PACKAGE = WORKTREE / "experimental/adarabi/hp-3p-gpt25"
SOURCE_ROOT = PROJECT / "eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103"
RECORDS = SOURCE_ROOT / "generation_gpt_image2_scene_v1/run/records"
CONTROL_IMAGES = SOURCE_ROOT / "generation_gpt_image2_scene_v1/run/images"
PROMPTS = SOURCE_ROOT / "revisions/v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json"
REMOTE_CONTROL = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
LOCAL_ENDPOINT = "http://127.0.0.1:8135"
RUN_ROOT = ROOT / "run"
INPUT_ROOT = RUN_ROOT / "inputs"
PIPELINE_ROOT = RUN_ROOT / "pipeline"
JOB_ROOT = RUN_ROOT / "jobs"
PROGRESS = RUN_ROOT / "progress.json"
REPORT_ROOT = ROOT / "live_report"
LOG_ROOT = ROOT / "logs"

PR_COMMIT = "d197e8058e37ddaded0a41e55d46da6985b6e0a1"
PIPELINE_VERSION = "unified-blue-scale-v24-astra-dynamic-props-stage-b-text-blue-twin-camera-guide-only-no-mask"
PROMPTS_SHA256 = "adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd"
SOURCE_HASHES = {
    "hp3p/prompts/system_3p.txt": "bf402c52998b1f1c7bdf1aed45c51d1c101cc43432b1c17561ecaf74a97017a2",
    "hp3p/approved_props.json": "63ef6f8fbf719ed1fa1c1f7a20351799060fd5862473c308c2384e314ae9b793",
    "hp3p/pipeline.py": "211d6fcb99c8d424e4b96a9aeeae55edd598037b6bcb9e6c36ed0f0258e45820",
    "hp3p/props.py": "47683b2254b480d12c0ae5578e7429857e59e2c7e1bf1060b9c66838801bf90a",
    "hp3p/geometry.py": "8bd8e878c85825743b4f67d93430208ea216ad60a5cb0e3d877f1ed118e8764e",
    "hp3p/grade.py": "aac336411f4f7da8cd6fa8a74819229318688bc87d836826a3aeabe2cffc1c81",
    "hp3p/reference_blue.py": "2c702d4f2c21da916c19bdcc66c6464d3fd711d6551bc703dc79f5cb26dac2f1",
    "requirements.txt": "506c1a70b48231d0f2c8f42cebb5c7f92eeda258e08bd7ba3c4021d6dcf71f63",
}

BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_v6_1_pr4403_dynamic_props_20261106"
GATEWAY = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}"
REGION = "us-west-2"

DEVICE_ORDER = ("cashmere", "elitebook", "tassel", "magic")
VIEW_ORDER = {
    "cashmere": ("Front_CloseUp", "Back_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    "elitebook": ("Front_CloseUp", "Back_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    "tassel": ("Front_CloseUp", "Front_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    "magic": ("Front_CloseUp", "Front_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
}
