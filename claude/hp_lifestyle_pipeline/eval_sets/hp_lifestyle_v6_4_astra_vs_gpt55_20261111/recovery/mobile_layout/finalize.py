"""Recover only mobile presentation/publication after terminal image generation."""

from __future__ import annotations

import argparse
import socket
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import image_study as study
import report
import scene_runner
import text_study

HERE = Path(__file__).resolve().parent
ROOT = study.HERE
CSS = "public/gallery/style.css"
OLD_RULE = ".controls{align-items:flex-start;flex-direction:column}select{max-width:85vw}"
NEW_RULE = (
    ".controls{align-items:flex-start;flex-direction:column}"
    ".controls label{max-width:100%}select{min-width:0;max-width:85vw}"
)


def stopped() -> None:
    cleanup = study.load(ROOT / "service_cleanup.json")
    owner = study.load(ROOT / "service_ownership.json")
    if cleanup["owned_pid"] != owner["pid"] or cleanup["returncode"] is None:
        raise ValueError("Owned generation service has not terminated")
    with socket.socket() as connection:
        connection.settimeout(2)
        if connection.connect_ex(("127.0.0.1", 8152)) == 0:
            raise ValueError("Port8152 still has a listener; do not finalize")


def inventory() -> dict[str, str]:
    result = {}
    for folder in ("text", "run", "endpoint_pr4523/run", "input_audit"):
        for path in sorted((ROOT / folder).rglob("*")):
            if path.is_file():
                result[str(path.relative_to(ROOT))] = study.sha(path)
    for name in (
        "study_manifest.json",
        "writer_snapshot_manifest.json",
        "image_terminal.json",
        "service_cleanup.json",
        "service_ownership.json",
    ):
        result[name] = study.sha(ROOT / name)
    return result


def prepare() -> None:
    stopped()
    study.verify()
    names = (
        CSS,
        "build_manifest.json",
        "pipeline_status.json",
        "pipeline_execution.log",
        "comparison_desktop.png",
    )
    for name in names:
        text_study.write(HERE / "original" / name, (ROOT / name).read_bytes())
    original = (ROOT / CSS).read_text()
    if original.count(OLD_RULE) != 1:
        raise ValueError("Expected the exact diagnosed mobile select rule")
    text_study.write(
        HERE / "preparation.json",
        {
            "created_utc": datetime.now(UTC).isoformat(),
            "cause": "Writer label plus85vw select exceeds390px viewport; generation is already terminal.",
            "allowed_change": CSS,
            "original_css_sha256": study.sha(ROOT / CSS),
            "original_build_manifest_sha256": study.sha(ROOT / "build_manifest.json"),
            "generation_files": inventory(),
            "model_calls_authorized": False,
        },
    )


def verify_recovery() -> dict[str, Any]:
    stopped()
    text_study.verify()
    preparation = study.load(HERE / "preparation.json")
    if inventory() != preparation["generation_files"]:
        raise ValueError("Terminal text/image generation evidence changed")
    manifest = study.load(ROOT / "study_manifest.json")
    for name, expected in manifest["files"].items():
        path = HERE / "original" / name if name == CSS else ROOT / name
        if study.sha(path) != expected:
            raise ValueError("Original frozen source changed: " + name)
    if study.sha(study.SOURCE) != manifest["prompts_sha256"]:
        raise ValueError("Accepted writer export changed")
    original = (HERE / "original" / CSS).read_text()
    if (ROOT / CSS).read_text() != original.replace(OLD_RULE, NEW_RULE):
        raise ValueError("Presentation changes exceed the exact mobile flex-sizing correction")
    return preparation


def audit_terminal() -> None:
    records = [study.load(scene_runner.paths(study.RUN, row)["record"]) for row in study.rows()]
    if len(records) != 80 or len({record["job_id"] for record in records}) != 80:
        raise ValueError("Terminal image jobs are not the exact unique80 submissions")
    kinds: Counter[tuple[str, str]] = Counter()
    for record in records:
        native = study.ENDPOINT / "run/jobs" / record["job_id"]
        calls = study.load(native / "calls.json")
        if [call["kind"] for call in calls] != ["chat_json"] * 3 + ["image_edit"]:
            raise ValueError("Native call order changed")
        for call in calls:
            request = study.load(native / call["requestArtifact"])
            if scene_runner.canonical_sha256(request) != call["requestSha256"]:
                raise ValueError("Native request hash mismatch")
            if call["status"] == "done":
                response = study.load(native / call["responseArtifact"])
                if scene_runner.canonical_sha256(response) != call["responseSha256"]:
                    raise ValueError("Native response hash mismatch")
            elif (
                record["status"] != "failed"
                or call["kind"] != "image_edit"
                or call["errorType"] != "InternalServerError"
                or (native / call["responseArtifact"]).exists()
            ):
                raise ValueError("Unexpected failed native call")
            kinds.update([(call["kind"], call["status"])])
    expected = Counter({("chat_json", "done"): 240, ("image_edit", "done"): 79, ("image_edit", "error"): 1})
    if kinds != expected:
        raise ValueError("Terminal call totals do not reconcile")
    audits = list((ROOT / "input_audit").glob("*.json"))
    if len(audits) != 79 or len({record["image_sha256"] for record in records if record["status"] == "done"}) != 79:
        raise ValueError("Successful raw-image audit coverage is incomplete")
    text_study.write(
        HERE / "generation_audit.json",
        {
            "unique_submissions": 80,
            "successful_images": 79,
            "failed_images": 1,
            "successful_input_audits": 79,
            "native_astra_calls_completed": 240,
            "native_image_calls_completed": 79,
            "native_image_calls_failed": 1,
            "image_replacements": 0,
            "failed_row": "cashmere__laptop_FrontLeftMedium::p6",
            "failed_job": "20261111T234635Z_af53732db0c6",
            "error": "InternalServerError: HTTP503; no image response artifact",
            "new_model_calls_for_recovery": 0,
        },
    )


def finalize() -> None:
    preparation = verify_recovery()
    audit_terminal()
    manifest = study.load(HERE / "original/build_manifest.json")
    original_assets = dict(manifest["assets"])
    manifest["assets"]["gallery/style.css"] = {
        "sha256": study.sha(ROOT / CSS),
        "bytes": (ROOT / CSS).stat().st_size,
    }
    manifest["presentation_recovery"] = {
        "preparation_sha256": study.sha(HERE / "preparation.json"),
        "original_build_manifest_sha256": preparation["original_build_manifest_sha256"],
        "allowed_change": CSS,
        "generation_manifest_unchanged": True,
    }
    for name, expected in manifest["assets"].items():
        if study.sha(report.PUBLIC / name) != expected["sha256"]:
            raise ValueError("Public artifact changed beyond the approved CSS: " + name)
    changed = [name for name, value in manifest["assets"].items() if value != original_assets[name]]
    if changed != ["gallery/style.css"]:
        raise ValueError("Expected exactly one changed presentation asset")
    scene_runner.atomic_json(ROOT / "build_manifest.json", manifest)
    subprocess.run([sys.executable, str(ROOT / "check_browser.py")], check=True)
    report.publish()
    verify_recovery()
    receipt = {
        "completed_utc": datetime.now(UTC).isoformat(),
        "status": "complete_with_errors",
        "accepted_astra_prompts": 80,
        "astra_images": 79,
        "failed_astra_images": 1,
        "baseline_images": 160,
        "planned_display_slots": 320,
        "actual_images": 239,
        "completion_receipt_sha256": study.sha(ROOT / "completion_receipt.json"),
        "browser_validation_sha256": study.sha(ROOT / "browser_validation.json"),
        "generation_audit_sha256": study.sha(HERE / "generation_audit.json"),
        "generation_evidence_unchanged": True,
        "new_model_calls": 0,
        "owned_service_stopped": True,
    }
    text_study.write(HERE / "finalization_receipt.json", receipt)
    scene_runner.atomic_json(
        ROOT / "pipeline_status.json",
        {"phase": "complete_with_errors", "recovery_receipt": str(HERE / "finalization_receipt.json"), **receipt},
    )
    print(receipt, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "finalize"))
    arguments = parser.parse_args()
    if arguments.command == "prepare":
        prepare()
    else:
        finalize()
