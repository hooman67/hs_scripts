"""
Foundry Media Intelligence DAG

Each stage runs as a Pluto job that clones/runs the
appropriate genie branch, and outputs to feature registry.
"""

import logging
import os
import sys
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse

import boto3
import foundry_aws_gateway
import pandas as pd
import numpy as np

from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule

_REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(_REPO_ROOT, "scripts"))
sys.path.insert(0, _REPO_ROOT)

from make_input_parquet import list_s3_videos, write_parquet  # noqa: E402
from post_processing_scripts.visualization import fr_delete, health_check_fr  # noqa: E402
from scripts.make_input_parquet import _IMAGE_EXTENSIONS  # noqa: E402

from mi_params import PIPELINE_DAG_ID, PIPELINE_PARAMS
from video_analysis_config import (
    STAGES,
    mi_env_values,
)
from video_analysis_fr import load_stage_dq_context, register_stage_feature
from video_analysis_utils import job_runner

logger = logging.getLogger(__name__)

default_args = {
    "owner": "foundry-media-intelligence",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
    "email_on_failure": False,
}

_GENERATED_PARQUET_XCOM_KEY = "generated_input_parquet"
_DQ_REPORT_XCOM_KEY = "dq_report"
_CLEARED_ASSETS_XCOM_KEY = "cleared_assets"
_RERUN_CONF_XCOM_KEY = "rerun_conf"
_DQ_STAGES = ("tac", "event", "frame", "speech")
_RERUN_TIMEOUT = timedelta(hours=48)
_RERUN_POKE_INTERVAL = 60


def _s3_client(s3_url: str):
    """Return a gateway-aware S3 client for the bucket in s3_url."""
    bucket = urlparse(s3_url).netloc
    return foundry_aws_gateway.maybe_s3_client(bucket) or boto3.client("s3")


def _make_parquet(**context):
    """Generate or filter the input parquet."""
    p = context["params"]
    generate = p.get("generate_input_parquet", False)
    skim_specific = p.get("specific_asset_skim")
    skim_quick = p.get("quick_subset_skim", False)
    needs_skim = bool(skim_specific) or skim_quick

    if not generate and not needs_skim:
        logger.info("generate_input_parquet=False, no skim — skipping parquet generation")
        context["ti"].xcom_push(key=_GENERATED_PARQUET_XCOM_KEY, value=None)
        return

    output_path = p["input_parquet_path"]

    # ── Get the full URL list ────────────────────────────────────────────
    if generate:
        video_s3_folder = p.get("video_s3_folder", "").strip()
        if not video_s3_folder:
            raise ValueError("video_s3_folder must be provided when generate_input_parquet=True")
        urls = list_s3_videos(video_s3_folder, _s3_client(video_s3_folder))
        if not urls:
            raise RuntimeError(f"No video files found in {video_s3_folder}")
    else:
        urls = health_check_fr.read_asset_urls(
            output_path,
            _s3_client(output_path) if output_path.startswith("s3://") else None,
        )
        if not urls:
            raise RuntimeError(f"No assets found in {output_path}")

    total = len(urls)

    # ── Apply skim filtering ─────────────────────────────────────────────
    if skim_specific:
        urls = list(skim_specific)
        output_path = output_path.replace(".parquet", "_skim.parquet")
        logger.info("specific_asset_skim is on — %d asset(s) selected", len(urls))
        logger.info("  %s", "\n  ".join(urls))
    elif skim_quick:
        num_to_skim = p["num_items_subset_skim"]
        urls = np.random.choice(urls, min(num_to_skim, total), replace=False).tolist()
        output_path = output_path.replace(".parquet", f"_skim_{num_to_skim}.parquet")
        logger.info("quick_subset_skim is on — %d of %d asset(s) selected", len(urls), total)
        logger.info("  %s", "\n  ".join(urls))

    # ── Write ────────────────────────────────────────────────────────────
    logger.info("Writing %d asset(s) → %s", len(urls), output_path)
    df = pd.DataFrame({"s3_url": urls, "title_name": [None] * len(urls)})
    write_parquet(df, output_path, _s3_client(output_path) if output_path.startswith("s3://") else None)
    logger.info("Input parquet written → %s", output_path)
    context["ti"].xcom_push(key=_GENERATED_PARQUET_XCOM_KEY, value=output_path)


def _make_register_fr(stage_name: str):
    """Register FR versions for the given stage"""
    def register_fr(**context):
        p = context["params"]
        # Stagger event/frame genie clones
        if stage_name == "frame":
            time.sleep(60)
        register_stage_feature(
            stage_name,
            STAGES[stage_name],
            genie_branch=p["genie_branch"],
            fr_version=p["fr_version"],
            publish=p["publish_version"],
            ignore_fr_checks=p["ignore_fr_checks"],
        )
    register_fr.__name__ = f"register_fr_{stage_name}"
    return register_fr


def _make_submit(stage_name: str):
    def submit(**context):
        p = context["params"]
        num_pods = p["num_pods"]
        if stage_name in ["event", "frame"]: # Split max pods between event/frame
            num_pods = max(1, num_pods // 2)

        generated = context["ti"].xcom_pull(
            key=_GENERATED_PARQUET_XCOM_KEY, task_ids="make_input_parquet"
        )
        mi_envs = mi_env_values(p)
        if generated:
            mi_envs["MI_INPUT_PARQUET_PATH"] = generated

        if not p["preview_upload_s3_dir"]:
            input_parquet_path = generated or p["input_parquet_path"]
            parsed_url = urlparse(input_parquet_path)
            base_path = os.path.dirname(parsed_url.path)
            default_preview_dir = f"s3://{parsed_url.netloc}{base_path}/"
            mi_envs["MI_PREVIEW_UPLOAD_S3_DIR"] = default_preview_dir

        project = p["pluto_project"]
        job_runner.project = project
        logger.info("Submitting Pluto job for stage %s with %d pod(s) to project %s", stage_name, num_pods, project)
        
        job_id = job_runner.submit(
            stage_name,
            STAGES[stage_name],
            genie_branch=p["genie_branch"],
            mi_envs=mi_envs,
            num_pods=num_pods,
            job_allocation_mode=p["job_allocation_mode"],
        )
        context["ti"].xcom_push(key=f"{stage_name}_job_id", value=job_id)
    submit.__name__ = f"submit_{stage_name}"
    return submit


def _make_monitor(stage_name: str, timeout_hours: int):
    def monitor(**context):
        p = context["params"]
        job_id = context["ti"].xcom_pull(
            key=f"{stage_name}_job_id",
            task_ids=f"stage_{stage_name}.submit_{stage_name}",
        )
        # Stagger event/frame genie clones
        if stage_name == "frame":
            time.sleep(60)
        feature_name, _ = load_stage_dq_context(
            stage_name, STAGES[stage_name],
            genie_branch=p["genie_branch"], fr_version=p["fr_version"],
        )
        
        include_images = stage_name == "frame"
        asset_ids = [
            health_check_fr.asset_id_for(url)
            for url in _run_asset_urls(context, include_images=include_images)
        ]

        def progress() -> str:
            done = health_check_fr.count_written(feature_name, p["fr_version"], asset_ids)
            pct = round(100 * done / len(asset_ids)) if asset_ids else 0
            return f"{done}/{len(asset_ids)} records ({pct}%)"

        job_runner.await_completion(job_id, timeout_hours=timeout_hours, progress=progress)
    monitor.__name__ = f"monitor_{stage_name}"
    return monitor


def _run_input_parquet(context) -> str:
    """The parquet the stages actually read: the generated one if there is one."""
    generated = context["ti"].xcom_pull(
        key=_GENERATED_PARQUET_XCOM_KEY, task_ids="make_input_parquet"
    )
    return generated or context["params"]["input_parquet_path"]


def _run_asset_urls(context, include_images=False) -> list[str]:
    """The s3_urls of the run's assets, read from whichever parquet is in play."""
    parquet_path = _run_input_parquet(context)
    urls = health_check_fr.read_asset_urls(
        parquet_path,
        _s3_client(parquet_path) if parquet_path.startswith("s3://") else None,
    )
    if not include_images:
        urls = [url for url in urls if not _is_image_url(url)]
    return urls


def _is_image_url(url: str) -> bool:
    return any(url.lower().endswith(ext) for ext in _IMAGE_EXTENSIONS)


def _make_dq_check(stage_name: str):
    def dq_check(**context):
        p = context["params"]

        if stage_name == "frame":
            s3_urls = _run_asset_urls(context, include_images=True) # Frame accepts images as valid assets
        else:
            s3_urls = _run_asset_urls(context, include_images=False)

        feature_name, sentinels = load_stage_dq_context(
            stage_name,
            STAGES[stage_name],
            genie_branch=p["genie_branch"],
            fr_version=p["fr_version"],
        )

        if stage_name == "tac":
            report = health_check_fr.tac_report(feature_name, p["fr_version"], s3_urls)
        else:
            report = health_check_fr.item_report(
                stage_name, feature_name, p["fr_version"], s3_urls, sentinels
            )

        asset_threshold = p["dq_asset_delete_threshold_pct"]
        missing_threshold = p["dq_missing_threshold_pct"]
        for line in health_check_fr.format_report(report, asset_threshold, missing_threshold):
            logger.info(line)

        context["ti"].xcom_push(key=_DQ_REPORT_XCOM_KEY, value=report)

        # Say nothing gets written, fail here
        if missing_threshold is not None and report["pct_missing"] > missing_threshold:
            raise AirflowException(
                f"{stage_name}: {report['assets_missing']} of "
                f"{report['assets_expected']} assets have no record "
                f"({report['pct_missing']}%), over the {missing_threshold}% threshold"
            )

        cleared = _clear_failed_assets(stage_name, feature_name, report, p)
        context["ti"].xcom_push(key=_CLEARED_ASSETS_XCOM_KEY, value=cleared)

    dq_check.__name__ = f"dq_check_{stage_name}"
    return dq_check


def _clear_failed_assets(stage_name: str, feature_name: str, report: dict, p: dict) -> list[str]:
    """Delete the records of assets over the per-asset sentinel threshold.

    Returns the asset_ids whose record is now gone, which is what a rerun of
    this DAG would redo.
    """
    if stage_name == "tac":
        return []

    asset_threshold = p["dq_asset_delete_threshold_pct"]
    over = health_check_fr.assets_over(report, asset_threshold)
    if not over:
        logger.info(
            "%s: no asset is over the %s%% per-asset sentinel threshold",
            stage_name, asset_threshold,
        )
        return []

    logger.info(
        "%s: %d asset(s) over the %s%% per-asset sentinel threshold:",
        stage_name, len(over), asset_threshold,
    )
    for asset in over:
        logger.info(
            "  %s  %s/%s items failed (%s%%)",
            asset["s3_url"], asset["failed"], asset["total"], asset["pct_failed"],
        )

    if not p["delete_failed_records"]:
        logger.info(
            "%s: delete_failed_records is off — records kept, rerun will skip these assets",
            stage_name,
        )
        return []

    result = fr_delete.delete_assets(
        feature_name, [asset["asset_id"] for asset in over], report["version"]
    )
    logger.info(
        "%s: cleared %d record(s), %d already absent, %d failed to delete",
        stage_name, len(result["deleted"]), len(result["absent"]), len(result["failed"]),
    )
    if result["failed"]:
        raise AirflowException(
            f"{stage_name}: {len(result['failed'])} record(s) could not be deleted "
            f"({', '.join(result['failed'])}) — a rerun would skip these assets and "
            f"leave them broken"
        )
    # An absent record is equally missing, so the rerun redoes it too.
    return list(result["deleted"]) + list(result["absent"])


def _health_check(**context):
    """Roll every stage's DQ report into one summary at the end of the run."""
    reports = {
        stage: context["ti"].xcom_pull(
            key=_DQ_REPORT_XCOM_KEY, task_ids=f"stage_{stage}.dq_check_{stage}"
        )
        for stage in _DQ_STAGES
    }
    for line in health_check_fr.format_summary(
        reports, context["params"]["dq_asset_delete_threshold_pct"]
    ):
        logger.info(line)


def _decide_rerun(**context) -> bool:
    """Re-trigger this DAG when the run cleared records and has budget left.

    The cleared assets are the only ones a rerun would redo, since every stage
    skips assets that already have a record. The rerun carries the same params
    with one fewer rerun left, so a stage that fails the same way every time
    stops instead of looping.
    """
    p = context["params"]
    budget = p["dq_max_reruns"]

    if p.get("quick_subset_skim") or p.get("specific_asset_skim"):
        logger.info("Skim is active — skipping automatic rerun")
        return False

    cleared = {}
    for stage in _DQ_STAGES:
        ids = context["ti"].xcom_pull(
            key=_CLEARED_ASSETS_XCOM_KEY, task_ids=f"stage_{stage}.dq_check_{stage}"
        )
        if ids is None and stage != "tac":
            logger.warning(
                "%s: no DQ result — not re-triggering, this run needs looking at", stage
            )
            return False
        if ids:
            cleared[stage] = ids

    if not cleared:
        logger.info("No records were cleared — nothing for a rerun to redo")
        return False

    total = sum(len(ids) for ids in cleared.values())
    logger.info(
        "%d record(s) cleared across %s", total, ", ".join(sorted(cleared))
    )
    if budget < 1:
        logger.info(
            "dq_max_reruns is %s — leaving the rerun to be triggered by hand", budget
        )
        return False

    conf = {**dict(p), "dq_max_reruns": budget - 1}
    conf["generate_input_parquet"] = False
    context["ti"].xcom_push(key=_RERUN_CONF_XCOM_KEY, value=conf)
    logger.info("Re-triggering %s with %d rerun(s) left after it", PIPELINE_DAG_ID, budget - 1)
    return True


def _make_stage_group(dag_ref, stage_name: str, timeout_hours: int):
    with TaskGroup(f"stage_{stage_name}", dag=dag_ref) as tg:
        reg = PythonOperator(
            task_id=f"register_fr_{stage_name}",
            python_callable=_make_register_fr(stage_name),
        )
        sub = PythonOperator(
            task_id=f"submit_{stage_name}",
            python_callable=_make_submit(stage_name),
        )
        mon = PythonOperator(
            task_id=f"monitor_{stage_name}",
            python_callable=_make_monitor(stage_name, timeout_hours),
            execution_timeout=timedelta(hours=timeout_hours),
        )
        dq = PythonOperator(
            task_id=f"dq_check_{stage_name}",
            python_callable=_make_dq_check(stage_name),
        )
        reg >> sub >> mon >> dq
    return tg

# ── DAG definition ────────────────────────────────────────────────────────────

with DAG(
    PIPELINE_DAG_ID,
    default_args=default_args,
    description=(
        "Foundry Media Intelligence Offline Ingestion Pipeline"
    ),
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    params=PIPELINE_PARAMS,
    tags=["media-intelligence", "foundry", "ingestion"],
) as dag:

    make_parquet_task = PythonOperator(
        task_id="make_input_parquet",
        python_callable=_make_parquet,
    )

    tac = _make_stage_group(dag, "tac", timeout_hours=24)

    event = _make_stage_group(dag, "event", timeout_hours=12)
    frame = _make_stage_group(dag, "frame", timeout_hours=12)

    speech = _make_stage_group(dag, "speech", timeout_hours=12)

    health_check_task = PythonOperator(
        task_id="health_check",
        python_callable=_health_check,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    decide_rerun_task = ShortCircuitOperator(
        task_id="decide_rerun",
        python_callable=_decide_rerun,
        ignore_downstream_trigger_rules=False,
    )

    rerun_task = TriggerDagRunOperator(
        task_id="rerun_pipeline",
        trigger_dag_id=PIPELINE_DAG_ID,
        conf="{{ ti.xcom_pull(task_ids='decide_rerun', key='rerun_conf') | tojson }}",
        wait_for_completion=True,
        poke_interval=_RERUN_POKE_INTERVAL,
        allowed_states=["success"],
        failed_states=["failed"],
        trigger_run_id="{{ run_id }}__rerun__{{ ti.try_number }}",
        execution_timeout=_RERUN_TIMEOUT,
        retries=0,
    )

    # ── Ordering ──────────────────────────────────────────────────────────────
    make_parquet_task >> tac >> [event, frame]
    event >> speech
    [frame, speech] >> health_check_task >> decide_rerun_task >> rerun_task

