#!/usr/bin/env python3
"""Publish bounded snapshots while the single authorized generation finishes."""
import json
import os
from pathlib import Path
import time

import report
import study

HERE = study.HERE
deadline = time.monotonic() + 8 * 3600
previous_done = -1
while time.monotonic() < deadline:
    counts = study.counts()
    done = sum(v["done"] for v in counts.values())
    terminal = all(v["pending"] == 0 for v in counts.values())
    print(json.dumps({"at_utc": study.now(), "done": done, "cells": counts}), flush=True)
    if previous_done < 0 or done - previous_done >= 24 or terminal:
        report.collect_inputs()
        report.build()
        report.publish()
        previous_done = done
        receipt = study.load(HERE / "publication_receipt.json")
        study.write(HERE / "progress_status.json", {"at_utc": study.now(), "cells": counts,
                                                   "last_published_done": done, "url": receipt["url"]})
        study.write(HERE / "SUMMARY.md", f"""# V6.3 full160 on exact PR4417 and PR4523

As of {study.now()}. Status: {"terminal; audit follows" if terminal else "generation running"}.

## Outcome and scope

USER-CONFIRMED: reuse30 completed V6.3 images per pipeline and generate exactly130 additional per pipeline.
The same frozen160 texts,16 prepared product views, model contract and pinned PR sources are used.
No new text generations, image resampling, judgments, commits or production deployments are included.

VERIFIED counts in this checkpoint:

```json
{json.dumps(counts, indent=2)}
```

Live report: {receipt["url"]}

## Evidence and reproduction

- `{HERE / "study_manifest.json"}`: immutable160 universe, exact reused/new partitions and provider settings.
- `{HERE / "execution_commands.json"}`: reproducible native-runner commands (never run a second worker).
- `{HERE / "execution_status.json"}`: single tracked generation state and PID.
- `{HERE / "input_audit/summary.json"}`: actual input materialization; no model calls.
- `{HERE / "publication_receipt.json"}`: remote download/hash evidence for each owned allowlisted asset.
- `{HERE / "s3_access.py"}`: refreshed user-supplied credentials through the frozen safe assignment parser; never executed or persisted.
- `{HERE / "preserved_files.json"}`:2854 existing immutable evidence files checked before/after execution.
- `{HERE / "tests.log"}`: focused partition, no-duplicate-POST, reuse-binding and publication-ownership checks.

## Limitations

The source texts are actual GPT-5.5 r1 outputs from15 successful bank services and one recognition false failure,
accepted unchanged under corrected r2 recognition. This is not a fresh16/16r2 reliability trial.
Style references and stochastic outputs are not pair-controlled. Exact product is instructed, not guaranteed
pixel-locked. Remote native job artifact exports and product bytes/version are verified, but remote raw
model-request image hashes/all image settings are not exposed. No image-quality significance claim or
judge verdict applies. Existing generation records retain their original study/run SHA-256 bindings.

## Recovery and next exact step

{"Wait for generation process to exit, then audit final terminal report and stop only the task-owned8138 endpoint." if terminal else "The attached generation and bounded progress publisher are active. Do not start a duplicate. Read current execution_status/progress_status and native jobs if interrupted."}
Known jobs resume without a duplicate POST. An ambiguous submit_started event without a saved job blocks
continuation and requires investigation; it is never blindly resubmitted. All original failures are retained.
""")
    if terminal:
        report.final_audit()
        break
    lock = HERE / "generation.lock"
    if not lock.exists() and study.load(HERE / "execution_status.json").get("status") != "running":
        raise RuntimeError("generation exited before all selected rows became terminal")
    time.sleep(60)
else:
    raise TimeoutError("bounded eight-hour progress window exceeded; preserve known jobs and investigate")
