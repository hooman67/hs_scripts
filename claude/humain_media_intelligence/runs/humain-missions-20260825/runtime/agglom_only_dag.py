"""Foundry MI agglomeration only: group assets and characters from Postgres.

Runs only the LLM-driven grouping: assumes the schema is already populated,
warms the vLLM deployment, waits for it, then calls franchises+entities.
Minimal params: just what agglom needs (DB connection + vLLM config).
"""

import logging
import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.python import PythonSensor
from airflow.sdk import Param

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mi_params import POSTPROCESSING_PARAMS
from post_processing_dag import _db_agglom_warmup, _db_agglom_isready, _db_agglom_call

logger = logging.getLogger(__name__)

# Subset of params needed for just agglomeration
_AGGLOM_PARAM_KEYS = (
    "postgres_db_connection_str",
    "postgres_schema",
    "vllm_ethos_dev_endpoint",
    "agglom_model",
    "add_context_franchise",
    "add_context_entity",
)
AGGLOM_PARAMS = {k: POSTPROCESSING_PARAMS[k] for k in _AGGLOM_PARAM_KEYS}

with DAG(
    "foundry_media_intelligence_agglom_only",
    default_args={
        "owner": "foundry-media-intelligence",
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="MI agglomeration only: group assets/characters from existing Postgres data",
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    params=AGGLOM_PARAMS,
    tags=["media-intelligence", "foundry", "agglomeration"],
) as dag:

    warmup = PythonOperator(
        task_id="warmup",
        python_callable=_db_agglom_warmup,
    )
    monitor = PythonSensor(
        task_id="monitor",
        python_callable=_db_agglom_isready,
        poke_interval=30,
        timeout=30 * 60,
        mode="reschedule",
    )
    agglom = PythonOperator(
        task_id="agglom",
        python_callable=_db_agglom_call,
    )

    warmup >> monitor >> agglom

