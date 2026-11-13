#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Run the frozen V5 runner against this eval set's 16-case manifest."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT_RUNNER = HERE.parent / "hp_lifestyle_dual_source_v5_pilot_20261027/run_gpt55.py"
spec = importlib.util.spec_from_file_location("v5_frozen_parent_runner", PARENT_RUNNER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"could not load frozen V5 runner: {PARENT_RUNNER}")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
runner.HERE = HERE


if __name__ == "__main__":
    runner.main()
