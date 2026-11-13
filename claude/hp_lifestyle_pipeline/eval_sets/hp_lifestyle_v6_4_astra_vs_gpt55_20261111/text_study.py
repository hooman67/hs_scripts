"""Frozen V6.4 model comparison: sixteen independent banks, one semantic repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import foundry_aws_gateway
import foundry_aws_gateway.llm

from astra_provider import AstraProvider
from hp_prompt_writer_v6_4.service import rewrite

ROOT = Path(__file__).resolve().parent
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/" + ROOT.name
PRIOR = ROOT.parent / "hp_lifestyle_v6_4_full160_pr4523_20261110"
HANDOFF = ROOT.parents[1] / "local_data/integration_packages/hp_prompt_writer_v6_4_20261110"
BASELINE_KEY = "eval_sets/" + PRIOR.name + "/data/generation.json"
AUTH_KEY = "eval_sets/hp_lifestyle_grouped_diversity_20261111/gallery/imsauth.js"
MODEL_IDENTITY_PORTS = {"hp_prompt_writer_v6_4/runtime.py", "hp_prompt_writer_v6_4/service.py"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (
        value
        if isinstance(value, bytes)
        else (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    )
    with path.open("xb") as stream:
        stream.write(data)


def s3_client() -> Any:
    client = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if client is None:
        raise RuntimeError("Managed S3 client unavailable")
    return client


def prepare() -> None:
    import socket

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 8152))
    client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=0, timeout=1800)
    if client.__class__.__name__ != "OpenAI" or client.max_retries != 0:
        raise RuntimeError("Managed Direct OpenAI client does not match the experiment")
    client.close()
    source = load(ROOT / "copied_source_manifest.json")
    for name, expected in source["files"].items():
        if name not in MODEL_IDENTITY_PORTS and sha(ROOT / name) != expected:
            raise ValueError("Copied frozen source changed: " + name)
    if sha(HANDOFF / "PACKAGE_MANIFEST.json") != source["handoff_sha256"]:
        raise ValueError("Original integration package changed")
    s3 = s3_client()
    remote = {}
    for name, key in (("generation.json", BASELINE_KEY), ("imsauth.js", AUTH_KEY)):
        response = s3.get_object(Bucket=BUCKET, Key=key)
        data = response["Body"].read()
        write(ROOT / "baseline/live" / name, data)
        remote[name] = {"key": key, "sha256": hashlib.sha256(data).hexdigest(), "etag": response["ETag"]}
    baseline = load(ROOT / "baseline/live/generation.json")
    frozen = load(ROOT / "baseline/outputs/all_160/prompts_all_160.json")
    if baseline["status"] != "complete" or len(baseline["rows"]) != 160:
        raise ValueError("The GPT-5.5 image baseline is incomplete")
    exported = {prompt["prompt_key"]: prompt for prompt in frozen["prompts"]}
    for row in baseline["rows"]:
        if row["prompt"] != exported[row["prompt"]["prompt_key"]] or row["output"]["status"] != "done":
            raise ValueError("Baseline image is not bound to the frozen GPT-5.5 prompt")
    if (ROOT / "baseline/live/imsauth.js").read_bytes() != (ROOT / "public/gallery/imsauth.js").read_bytes():
        raise ValueError("Native IMS helper differs from its live source")
    probe = b"HP V6.4 Astra writer comparison"
    key = PREFIX + "/preflight/access.txt"
    s3.put_object(Bucket=BUCKET, Key=key, Body=probe, ContentType="text/plain", IfNoneMatch="*")
    if s3.get_object(Bucket=BUCKET, Key=key)["Body"].read() != probe:
        raise ValueError("Conditional S3 write/read failed")
    files = {name: sha(ROOT / name) for name in source["files"]}
    for name in ("astra_provider.py", "text_study.py", "pyproject.toml", "uv.lock"):
        files[name] = sha(ROOT / name)
    write(
        ROOT / "writer_snapshot_manifest.json",
        {
            "version": "v6.4-astra-high-32000-20261111-r1",
            "prepared_utc": datetime.now(UTC).isoformat(),
            "cases": [
                {
                    "case_id": case["bank_id"],
                    "frozen_input_path": case["input"],
                    "frozen_input_sha256": case["input_sha256"],
                }
                for case in load(ROOT / "banks.json")["cases"]
            ],
            "files": files,
            "baseline_live": remote,
            "model": "gpt-6-astra",
            "reasoning_effort": "high",
            "max_completion_tokens": 32000,
            "semantic_limit": 2,
            "transport_limit_per_semantic_call": 3,
            "workers": 4,
            "failure_policy": "finish other banks; preserve terminal failures; never semantic-resample",
            "baseline_settings": {"model": "gpt-5.5", "reasoning_effort": "medium", "max_completion_tokens": 16000},
            "credential_route": "Official Foundry SDK2.0 managed clients; standard AWS broker had no stored token.",
            "model_call_made_in_preflight": False,
            "model_identity_ports": sorted(MODEL_IDENTITY_PORTS),
        },
    )
    print(json.dumps({"preflight": "passed", "banks": 16, "expected_prompts": 160, "s3": "read/write verified"}))


def verify() -> dict[str, Any]:
    manifest = load(ROOT / "writer_snapshot_manifest.json")
    for name, expected in manifest["files"].items():
        if sha(ROOT / name) != expected:
            raise ValueError("Frozen experiment source changed: " + name)
    return manifest


def run_one(case: dict[str, Any]) -> dict[str, Any]:
    result_path = ROOT / "text/results" / f"{case['bank_id']}.json"
    journal = ROOT / "text/journals" / case["bank_id"]
    journal.mkdir(parents=True, exist_ok=False)
    request_path = ROOT / case["input"]
    if sha(request_path) != case["input_sha256"]:
        raise ValueError("Frozen bank request changed")
    provider = AstraProvider(foundry_aws_gateway.llm.get_openai, journal)
    result = rewrite(load(request_path), provider=provider, expected_model="gpt-6-astra")
    write(result_path, result)
    print(
        json.dumps(
            {
                "bank_id": case["bank_id"],
                "status": result["status"],
                "semantic_calls": result["audit"]["semantic_calls"],
            }
        ),
        flush=True,
    )
    return {"bank_id": case["bank_id"], "status": result["status"], "result_path": str(result_path)}


def generate(authorized: bool) -> None:
    if not authorized:
        raise PermissionError("Explicit paid-call authorization required")
    verify()
    lock = ROOT / "text/generation.lock"
    lock.parent.mkdir(exist_ok=True)
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.write(descriptor, str(os.getpid()).encode())
    os.close(descriptor)
    write(
        ROOT / "text/launch.json",
        {
            "started_utc": datetime.now(UTC).isoformat(),
            "pid": os.getpid(),
            "manifest_sha256": sha(ROOT / "writer_snapshot_manifest.json"),
        },
    )
    cases = load(ROOT / "banks.json")["cases"]
    with ThreadPoolExecutor(max_workers=4) as workers:
        futures = {workers.submit(run_one, case): case for case in cases}
        for future in as_completed(futures):
            future.result()
    export()


def export() -> None:
    verify()
    baseline = load(ROOT / "baseline/outputs/all_160/prompts_all_160.json")
    prior = {prompt["prompt_key"]: prompt for prompt in baseline["prompts"]}
    prompts, banks, failures = [], {}, []
    for case in load(ROOT / "banks.json")["cases"]:
        result = load(ROOT / "text/results" / f"{case['bank_id']}.json")
        banks[case["bank_id"]] = {"case_metadata": case, "source_input": load(ROOT / case["input"]), "result": result}
        if result["status"] != "ok":
            failures.append({"bank_id": case["bank_id"], "error": result["error"]})
            continue
        if len(result["prompts"]) != 10:
            raise ValueError("An accepted bank is not ten prompts")
        for rank, prompt in enumerate(result["prompts"], start=1):
            key = case["bank_id"] + f"::p{rank}"
            original = prior[key]
            fields = (
                "device_id",
                "device_display_name",
                "device_type",
                "source_pair",
                "camera_tag",
                "source_camera_name",
                "view_role",
                "render_gallery_url",
                "render_lookup",
            )
            metadata = {field: original[field] for field in fields}
            prompts.append(
                {
                    **metadata,
                    **prompt,
                    "prompt_key": key,
                    "bank_rank": rank,
                    "bank_debug_ref": case["bank_id"],
                    "text_sha256": hashlib.sha256(prompt["text"].encode()).hexdigest(),
                }
            )
    write(
        ROOT / "text/exports/prompts_all.json",
        {
            "version": "hp-lifestyle-v6.4-astra-high-32000-20261111-r1",
            "snapshot_manifest_path": str(ROOT / "writer_snapshot_manifest.json"),
            "snapshot_manifest_sha256": sha(ROOT / "writer_snapshot_manifest.json"),
            "prompts": prompts,
            "bank_audit": banks,
            "failures": failures,
            "device_source_mapping": baseline["device_source_mapping"],
        },
    )
    text = "\n\n".join(f"{p['prompt_key']}\n{p['text']}" for p in prompts)
    write(ROOT / "text/exports/prompts_all.txt", text.encode())
    write(
        ROOT / "text/terminal.json",
        {
            "completed_utc": datetime.now(UTC).isoformat(),
            "accepted_banks": 16 - len(failures),
            "failed_banks": failures,
            "accepted_prompts": len(prompts),
            "semantic_calls": sum(bank["result"]["audit"]["semantic_calls"] for bank in banks.values()),
            "transport_attempts_known": sum(
                bank["result"]["audit"]["transport_attempts_known"] for bank in banks.values()
            ),
            "status": "complete" if not failures else "complete_with_errors",
        },
    )
    print(json.dumps(load(ROOT / "text/terminal.json")), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "generate", "verify"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    args = parser.parse_args()
    if args.command == "generate":
        generate(args.paid_calls_authorized)
    elif args.command == "prepare":
        prepare()
    else:
        verify()
