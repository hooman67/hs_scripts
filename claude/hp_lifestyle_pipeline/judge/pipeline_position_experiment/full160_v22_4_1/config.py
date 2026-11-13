"""Frozen paths and identifiers for the V22.4.1 V6.1 full-160 experiment."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
WORKTREE = Path("/home/colligo/foundry-pr4349-position-exp")
PACKAGE = WORKTREE / "experimental/adarabi/hp-3p-gpt25"

SOURCE_ROOT = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/"
    "hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103"
)
RECORDS = SOURCE_ROOT / "generation_gpt_image2_scene_v1/run/records"
PROMPT_EXPORT = (
    SOURCE_ROOT
    / "revisions/v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json"
)
CONTROL_REPORT = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/"
    "hp_lifestyle_phrase_diversity_v6_1_gpt_image2_scene_20261105/"
    "bank_gallery/source/data.json"
)
CONTROL_GROUPED_JUDGE_REPORT = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/"
    "fe_reports/v6_1_consensus_v2_grouped_20261105/data.json"
)
FE_VIEWER = Path("/home/colligo/.claude/scripts/fe_html/annotation_viewer.html")

FREEZE = ROOT / "freeze.json"
RUN_ROOT = ROOT / "run"
INPUT_ROOT = RUN_ROOT / "inputs"
PIPELINE_ROOT = RUN_ROOT / "pipeline"
JOB_ROOT = RUN_ROOT / "jobs"
PROGRESS = RUN_ROOT / "progress.json"
REPORT_ROOT = ROOT / "report"
LOG_ROOT = ROOT / "logs"

PR_COMMIT = "8c358bc7989cb0e137e89db0fd325168249e2a22"
PIPELINE_VERSION = (
    "unified-blue-scale-v22.4.1-calibrated-080-alpha-textureless-invariant-"
    "fallback-twin-camera-guide-only-no-edit-mask"
)
PROMPT_EXPORT_SHA256 = "adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd"

REMOTE_CONTROL_ENDPOINT = (
    "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
)
LOCAL_ENDPOINT = "http://127.0.0.1:8128"

SOURCE_HASHES = {
    "hp3p/prompts/system_3p.txt": "bb02ad09f86a9a4aa4bdeac7c023d1ece0356ecef298853436af4781fa595ddf",
    "hp3p/prompts/system_3p_fixed_position.txt": "67e4d817a5a203912116bb99afbd6c4511d9a5c537b241cc6e980e34e75b1118",
    "hp3p/pipeline.py": "b0730eb08d036a139f34a3a95f36829984857d963f09d84d0e6e859de5285467",
    "hp3p/geometry.py": "f9d0f3a395624a150f9a9fed8c836394b66f041f6e212dc87c8b1a2322514a95",
    "hp3p/grade.py": "22169e7fc7fe3ebfd561bb3edd04edf4f1c630752444b752d388305c35bafbf6",
    "hp3p/reference_blue.py": "f36098543e208029226ae3b04ffd22c39edf7e168ab49dd5868e2185bd90661d",
    "hp3p/invariants.py": "a064e65cbedf2c3e3df92e78cebcce009bc3a4d6deb8ea57d2a26cc821d56b30",
    "requirements.txt": "cd1f9bbe9fb6526781e998279b6649e4b02b8a6f21a30e868386a7b86ba118b3",
}

EXPERIMENT_ID = "hp-position-flex-v22.4.1-v6.1-full160"
S3_BUCKET = "foundry-hp-enterprise-adobe-assets"
S3_PREFIX = "hp_position_flex_v22_4_1_v6_1_20261106/grouped"

