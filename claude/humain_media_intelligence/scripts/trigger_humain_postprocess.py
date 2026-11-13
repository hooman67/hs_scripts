#!/usr/bin/env python3
"""Trigger Humain MI postprocessing without persisting runtime secrets.

The script refuses to trigger until the exact ingestion run has succeeded. It
borrows secret-bearing connection fields from the newest successful live
postprocessing run in memory, replaces every dataset-specific field, and sends
the resulting payload directly to Airflow. It never prints or writes the
borrowed configuration.
"""

from __future__ import annotations

import json
import subprocess
import sys
import urllib.parse


API_ROOT = (
    "https://pluto-prod-vananth-mi-airflow-dev-11-0-8080.or2.colligo.dev/api/v2"
)
INGESTION_DAG = "foundry_media_intelligence_pipeline"
INGESTION_RUN = "humain_missions_20260825_fr_2026-08-25-8642"
POSTPROCESS_DAG = "foundry_media_intelligence_postprocessing"
POSTPROCESS_RUN = "humain_missions_20260825_postprocess_fr_2026-08-25-8642"

INPUT_PARQUET = (
    "s3://foundry-humain-default-adobe-assets/media-intelligence/"
    "humain-missions-20260825/manifests/input.parquet"
)
FR_VERSION = "2026-08-25-8642"
GENIE_BRANCH = "vananth/ingestion-v2"
POSTGRES_SCHEMA = "humain_missions_20260825"

FRANCHISE_CONTEXT = """This is a nonfiction Saudi-tourism mission-media corpus. Group assets only when there is strong evidence that they belong to the same documented mission/source sequence, the same clearly identifiable shoot, or the same specific event or place sequence. Preserve Clothing/Fashion, Events, Food, Landmarks/Architecture, and Lifestyle distinctions, including negative-control material. Do not group assets merely because they share a generic setting, activity, visual style, or broad cultural theme. Prefer separate groups when uncertain."""

ENTITY_CONTEXT = """This is a nonfiction cultural dataset. Group people only when strong visual and contextual evidence shows the same identifiable recurring subject across assets. Do not infer or use a person's name, nationality, ethnicity, religion, or other sensitive identity from appearance. Do not turn generic crowds, anonymous passersby, or merely similar-looking people into recurring entities. Prefer separate entities when uncertain."""

SECRET_RUNTIME_KEYS = (
    "postgres_db_connection_str",
    "opensearch_host",
    "opensearch_user",
    "opensearch_password",
)
REUSED_RUNTIME_KEYS = SECRET_RUNTIME_KEYS + (
    "vllm_ethos_dev_endpoint",
    "agglom_model",
)


def api_request(path: str, *, method: str = "GET", payload: dict | None = None) -> dict:
    command = [
        "curl",
        "--fail",
        "--silent",
        "--show-error",
        "--retry",
        "3",
        "--retry-all-errors",
        "--connect-timeout",
        "10",
        "--max-time",
        "60",
        "--request",
        method,
        "--header",
        "Content-Type: application/json",
        f"{API_ROOT}{path}",
    ]
    data = None if payload is None else json.dumps(payload)
    if data is not None:
        # A stdin payload keeps secret-bearing fields out of argv and process lists.
        command.extend(["--data-binary", "@-"])
    result = subprocess.run(command, input=data, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"Airflow request failed (curl exit {result.returncode})")
    return json.loads(result.stdout)


def successful_reference_conf() -> dict:
    query = urllib.parse.urlencode({"limit": 100, "order_by": "-logical_date"})
    runs = api_request(f"/dags/{POSTPROCESS_DAG}/dagRuns?{query}")["dag_runs"]
    for run in runs:
        if run.get("state") != "success":
            continue
        conf = run.get("conf") or {}
        if all(conf.get(key) for key in REUSED_RUNTIME_KEYS):
            return conf
    raise RuntimeError("No successful postprocessing run has all required runtime fields")


def main() -> int:
    ingestion = api_request(f"/dags/{INGESTION_DAG}/dagRuns/{INGESTION_RUN}")
    if ingestion.get("state") != "success":
        print(
            f"Refusing to trigger: ingestion state is {ingestion.get('state')!r}, not 'success'.",
            file=sys.stderr,
        )
        return 2

    reference = successful_reference_conf()
    conf = {key: reference[key] for key in REUSED_RUNTIME_KEYS}
    conf.update(
        {
            "input_parquet_path": INPUT_PARQUET,
            "fr_version": FR_VERSION,
            "genie_branch": GENIE_BRANCH,
            "postgres_schema": POSTGRES_SCHEMA,
            "fill_in_missing": True,
            "add_context_franchise": FRANCHISE_CONTEXT,
            "add_context_entity": ENTITY_CONTEXT,
            "local_cache_root": "/mnt/localssd/cache/humain_missions_20260825",
            "clear_cache_root": True,
        }
    )

    try:
        result = api_request(
            f"/dags/{POSTPROCESS_DAG}/dagRuns",
            method="POST",
            payload={"dag_run_id": POSTPROCESS_RUN, "conf": conf},
        )
    except RuntimeError as error:
        # Do not echo any HTTP response body: validation errors may reflect config.
        print(str(error), file=sys.stderr)
        return 1

    print(f"Triggered {result.get('dag_run_id', POSTPROCESS_RUN)}: {result.get('state')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
