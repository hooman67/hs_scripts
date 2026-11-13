"""Frozen paths and identifiers for the prepared V23.1 eight-row pilot."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKTREE = Path("/home/colligo/foundry-pr4349-position-exp")
PACKAGE = WORKTREE / "experimental/adarabi/hp-3p-gpt25"

SOURCE_ROOT = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/"
    "hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103"
)
RECORDS = SOURCE_ROOT / "generation_gpt_image2_scene_v1/run/records"

# Execution slug, immutable source record, cohort.
SELECTED_ROWS = (
    ("cashmere__laptop_FrontCloseUp__p1", "cashmere__laptop_FrontCloseUp__p1", "representative_v6_1"),
    ("cashmere__laptop_FrontWide__p1", "cashmere__laptop_FrontWide__p1", "representative_v6_1"),
    ("tassel__printer_FrontCloseUp__p1", "tassel__printer_FrontCloseUp__p1", "representative_v6_1"),
    ("tassel__printer_FrontWide__p1", "tassel__printer_FrontWide__p1", "representative_v6_1"),
    (
        "cashmere__laptop_FrontCloseUp__p1__relocation_demand",
        "cashmere__laptop_FrontCloseUp__p1",
        "movement_demand_diagnostic",
    ),
    (
        "cashmere__laptop_FrontWide__p1__relocation_demand",
        "cashmere__laptop_FrontWide__p1",
        "movement_demand_diagnostic",
    ),
    (
        "magic__printer_FrontCloseUp__p1__relocation_demand",
        "magic__printer_FrontCloseUp__p1",
        "movement_demand_diagnostic",
    ),
    (
        "magic__printer_FrontWide__p1__relocation_demand",
        "magic__printer_FrontWide__p1",
        "movement_demand_diagnostic",
    ),
)

EXPECTED_CELLS = (
    ("representative_v6_1", "laptop", "Front_CloseUp"),
    ("representative_v6_1", "laptop", "Front_Wide"),
    ("representative_v6_1", "printer", "Front_CloseUp"),
    ("representative_v6_1", "printer", "Front_Wide"),
    ("movement_demand_diagnostic", "laptop", "Front_CloseUp"),
    ("movement_demand_diagnostic", "laptop", "Front_Wide"),
    ("movement_demand_diagnostic", "printer", "Front_CloseUp"),
    ("movement_demand_diagnostic", "printer", "Front_Wide"),
)

FREEZE = ROOT / "freeze.json"
RUN_ROOT = ROOT / "run"
INPUT_ROOT = RUN_ROOT / "inputs"
PIPELINE_ROOT = RUN_ROOT / "pipeline"
JOB_ROOT = RUN_ROOT / "jobs"
PROGRESS = RUN_ROOT / "progress.json"
LOG_ROOT = ROOT / "logs"

PR_COMMIT = "8c358bc7989cb0e137e89db0fd325168249e2a22"
PIPELINE_VERSION = (
    "unified-blue-scale-v23.1-all-view-rigid-translation-strong-low-inlier-"
    "twin-camera-guide-only-no-edit-mask"
)
WRAPPER_VERSION = "v23.1-eight-row-pilot-stop-on-first-failure-v1"
MAX_OUTER_JOBS = 1
WRAPPER_SOURCE_NAMES = (
    "common.py",
    "config.py",
    "diagnostic_prompts.py",
    "endpoint.py",
    "run_pilot.py",
    "preflight.py",
    "freeze_inputs.py",
)

REMOTE_CONTROL_ENDPOINT = (
    "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
)
LOCAL_ENDPOINT = "http://127.0.0.1:8134"

SOURCE_HASHES = {
    "hp3p/prompts/system_3p.txt": "324ce0e449804bc0d17ac0cf5ed10587716bc9d7e6ef72b9a91e439745b6aaec",
    "hp3p/prompts/system_3p_fixed_position.txt": "67e4d817a5a203912116bb99afbd6c4511d9a5c537b241cc6e980e34e75b1118",
    "hp3p/pipeline.py": "ef1158a882dca0c8a85d01e3ed427d036282b29341fa5beeb88c9d4db39d9137",
    "hp3p/invariants.py": "808bde48be35ba6093dc01d0cc23808f0c7f4509b62e79dce64d1033674c19a6",
    "hp3p/geometry.py": "f9d0f3a395624a150f9a9fed8c836394b66f041f6e212dc87c8b1a2322514a95",
    "hp3p/grade.py": "22169e7fc7fe3ebfd561bb3edd04edf4f1c630752444b752d388305c35bafbf6",
    "hp3p/reference_blue.py": "f36098543e208029226ae3b04ffd22c39edf7e168ab49dd5868e2185bd90661d",
    "requirements.txt": "cd1f9bbe9fb6526781e998279b6649e4b02b8a6f21a30e868386a7b86ba118b3",
}

EXPERIMENT_ID = "hp-position-flex-v23.1-all-view-translation-eight-row-pilot"
