"""Frozen paths and identifiers for the V22.4.3-R1 assembly protocol."""

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
    "unified-blue-scale-v22.4.3-unreliable-affine-alpha-fallback-"
    "twin-camera-guide-only-no-edit-mask"
)
WRAPPER_VERSION = "v22.4.3-r1-bounded-outer-job-retry-1"
RETRYABLE_GUARD_ERROR = (
    "RuntimeError: pipeline error: ValueError: Product invariant guard rejected both "
    "image attempts; raw attempts and metrics kept."
)
MAX_OUTER_JOBS = 2
WRAPPER_SOURCE_NAMES = (
    "common.py",
    "config.py",
    "endpoint.py",
    "run_full160.py",
    "preflight.py",
    "freeze_inputs.py",
    "build_grouped_report.py",
)
PROMPT_EXPORT_SHA256 = "adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd"

REMOTE_CONTROL_ENDPOINT = (
    "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
)
LOCAL_ENDPOINT = "http://127.0.0.1:8132"

SOURCE_HASHES = {
    "hp3p/prompts/system_3p.txt": "bb02ad09f86a9a4aa4bdeac7c023d1ece0356ecef298853436af4781fa595ddf",
    "hp3p/prompts/system_3p_fixed_position.txt": "67e4d817a5a203912116bb99afbd6c4511d9a5c537b241cc6e980e34e75b1118",
    "hp3p/pipeline.py": "9e0378b6fbe6e505fbe626a9d0fe1a3155c93389b9cedc8c5c42eef5d4f2fd31",
    "hp3p/geometry.py": "f9d0f3a395624a150f9a9fed8c836394b66f041f6e212dc87c8b1a2322514a95",
    "hp3p/grade.py": "22169e7fc7fe3ebfd561bb3edd04edf4f1c630752444b752d388305c35bafbf6",
    "hp3p/reference_blue.py": "f36098543e208029226ae3b04ffd22c39edf7e168ab49dd5868e2185bd90661d",
    "hp3p/invariants.py": "4f833b0d0822d0d6e4dff1b41b39d46b2cb3cd9e3671e5b1339faf15ccbd810a",
    "requirements.txt": "cd1f9bbe9fb6526781e998279b6649e4b02b8a6f21a30e868386a7b86ba118b3",
}

EXPERIMENT_ID = "hp-position-flex-v22.4.3-r1-qualitative-assembly-v6.1-full160"
S3_BUCKET = "foundry-hp-enterprise-adobe-assets"
S3_PREFIX = "hp_position_flex_v22_4_3_r1_qualitative_assembly_v6_1_20261106/grouped"

