"""Complete one consistent Astra judge architecture on the original 128 images."""

import argparse
import fcntl
import hashlib
import importlib.util
import json
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from importlib.metadata import version as package_version
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLACEMENT = HERE.parent
VERSIONS = PLACEMENT / "versions"
REVISIONS = ("v3_2", "v3_2_r2", "v3_2_r3", "v3_2_r4")
PREVIOUS = PLACEMENT / "original_gallery_astra_update_20261111"
BUCKET = "foundry-hp-enterprise-adobe-assets"


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        value
        if isinstance(value, bytes)
        else (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()
    )
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(body)
    temporary.replace(path)


def immutable(path, value):
    path = Path(path)
    if path.exists():
        expected = (
            value
            if isinstance(value, bytes)
            else (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()
        )
        if path.read_bytes() != expected:
            raise ValueError("Existing frozen evidence differs: " + str(path))
    else:
        write(path, value)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def verify_plan():
    plan = load(HERE / "plan.json")
    for path, digest in plan["files"].items():
        if sha(path) != digest:
            raise ValueError("Frozen expansion input changed: " + path)
    return plan


def runtime(case):
    return {
        "generated_image": case["generated_image"]["local_path"],
        "twin_image": case["twin_image"]["local_path"],
        "product_type": case["product_type"],
        "scene_prompt": case["scene_prompt"],
        "image_stage": "scene_generation",
    }


def validate_reuse(row, case, frozen):
    if row["candidate"] != "p1" or row["id"] != case["id"]:
        raise ValueError("Prior result belongs to another case/architecture")
    for role in ("generated_image", "twin_image"):
        if (
            any(
                row[role][key] != case[role][key]
                for key in ("url", "sha256", "local_path")
            )
            or sha(case[role]["local_path"]) != case[role]["sha256"]
        ):
            raise ValueError("Prior result belongs to another source image")
    if row["source_row_id"] != case["source_row_id"]:
        raise ValueError("Prior result belongs to another source row")
    path = Path(row["result_path"])
    result = load(path)
    if (
        row["status"] != "complete"
        or sha(path) != row["result_sha256"]
        or result["protocol_freeze_sha256"] != frozen
        or result["runtime_input"] != runtime(case)
        or result["candidate"] != "p1"
        or result["application_merged_judgment"]["observation"] != row["observation"]
        or result["application_merged_judgment"]["natural_placement_score"]
        != row["score"]
        or result["final_decision"]["verdict"] != row["verdict"]
    ):
        raise ValueError("Prior completed prediction/context changed")


def prepare():
    if (HERE / "plan.json").exists():
        print(json.dumps({"existing_plan_verified": verify_plan()["expected_new"]}))
        return
    old = module("existing_astra_gallery", PREVIOUS / "update.py")
    inventory_path = VERSIONS / "v3_1/evaluation/inventory.json"
    cases = load(inventory_path)["records"]
    indexed, _ = old.actual_results()
    source_key = load(PREVIOUS / "source/object.json")["key"]
    body, response = old.get(old.client(), source_key)
    slots = old.LEGACY.GalleryParser(body.decode()).slots
    by_url = {case["generated_image"]["url"]: case for case in cases}
    if (
        len(cases) != 128
        or len(by_url) != 128
        or len(slots) != 128
        or {slot["url"] for slot in slots} != set(by_url)
    ):
        raise ValueError("Live original gallery and 128-case inventory differ")
    for slot in slots:
        if by_url[slot["url"]]["source_row_id"] != slot["source_row_id"]:
            raise ValueError("Live original image/source-row binding changed")
    immutable(HERE / "source/viewer.html", body)
    immutable(
        HERE / "source/object.json",
        {
            "key": source_key,
            "sha256": hashlib.sha256(body).hexdigest(),
            "etag": response["ETag"],
            "content_type": response["ContentType"],
            "metadata": response.get("Metadata", {}),
            "version_id": response.get("VersionId"),
        },
    )
    files = {
        str(path.resolve()): sha(path)
        for path in (
            Path(__file__),
            inventory_path,
            HERE / "source/viewer.html",
            HERE / "source/object.json",
            VERSIONS / "v3_2_r4/transport.py",
        )
    }
    for case in cases:
        for role in ("generated_image", "twin_image"):
            path = Path(case[role]["local_path"])
            if sha(path) != case[role]["sha256"]:
                raise ValueError("Source image changed: " + str(path))
            files[str(path)] = case[role]["sha256"]
    versions = {}
    for name in REVISIONS:
        frozen_path = VERSIONS / name / "protocol_freeze.json"
        files[str(frozen_path)] = sha(frozen_path)
        for item in load(frozen_path)["files"]:
            files[item["path"]] = item["sha256"]
        reused = {
            case["id"]: indexed[name][(case["id"], "p1")]
            for case in cases
            if (case["id"], "p1") in indexed[name]
        }
        for case in cases:
            if case["id"] in reused:
                row = reused[case["id"]]
                validate_reuse(row, case, sha(frozen_path))
                files[row["result_path"]] = row["result_sha256"]
        versions[name] = {
            "protocol_freeze_sha256": sha(frozen_path),
            "reused": reused,
            "expected_new": len(cases) - len(reused),
        }
    plan = {
        "created_utc": datetime.now(UTC).isoformat(),
        "user_scope": "All four revisions, one architecture per revision, original128 images.",
        "selected_architecture": "p1",
        "architectures_are_not_repeated_passes": True,
        "development_comparison_authorized_despite_failed_promotion_gates": True,
        "promoted": False,
        "new_images": 0,
        "expected_new": sum(value["expected_new"] for value in versions.values()),
        "expected_total_p1": 512,
        "versions": versions,
        "cases": cases,
        "files": files,
        "transport_policy": (
            "Use the existing R4 transport-only recovery implementation for identical "
            "Astra/high messages, schemas and caps. Resume interrupted streams in new "
            "attempt directories; recover completed stops, never redraw a semantic completion. "
            "Frozen prompts, acquisition, aggregation and scoring remain unchanged."
        ),
    }
    immutable(HERE / "plan.json", plan)
    verify_plan()
    print(
        json.dumps(
            {
                "prepared": True,
                "new_p1": plan["expected_new"],
                "reused_p1": 512 - plan["expected_new"],
            }
        ),
        flush=True,
    )


def recover_completion(common, group):
    for attempt in sorted(group.glob("attempt[0-9]*")):
        chunks = attempt / "chunks.jsonl"
        if not chunks.exists():
            continue
        collector = common.Collector()
        with chunks.open() as stream:
            for line in stream:
                try:
                    frame = json.loads(line)
                except json.JSONDecodeError:
                    if stream.read().strip():
                        raise ValueError(
                            "Corrupt historical stream, not a trailing partial frame"
                        )
                    break
                collector.feed(frame)
        if collector.finish is not None:
            value = collector.result()
            receipt_path = attempt / "receipt.json"
            receipt = (
                load(receipt_path)
                if receipt_path.exists()
                else {
                    "model_returned": common.MODEL,
                    "finish_reason": collector.finish,
                    "response_id": collector.response_id,
                    "usage": collector.usage,
                    "chunks_path": str(chunks.resolve()),
                    "chunks_sha256": sha(chunks),
                    "transport_attempts": int(attempt.name.removeprefix("attempt")),
                    "recovered_completed_stop": True,
                    "finished_utc": datetime.now(UTC).isoformat(),
                }
            )
            if sha(chunks) != receipt["chunks_sha256"]:
                raise ValueError("Recovered completed stream changed")
            immutable(receipt_path, receipt)
            return value, receipt
        error_path = attempt / "error.json"
        if error_path.exists() and not load(error_path)["retryable_transport_failure"]:
            raise ValueError(
                "Preserved terminal stage error; semantic redraw forbidden"
            )
    return None


def install_transport(common):
    transport = module("expansion_transport", VERSIONS / "v3_2_r4/transport.py")

    def completion(messages, schema, cap, output, client=None):
        output = Path(output)
        identity = {
            "messages_sha256": common.fingerprint(messages),
            "schema_sha256": common.fingerprint(schema),
            "cap": cap,
            "model": common.MODEL,
            "protocol_freeze_sha256": common.verify_freeze(),
            "driver_sha256": sha(__file__),
            "transport_sha256": sha(VERSIONS / "v3_2_r4/transport.py"),
        }
        immutable(output / "expansion_transport_identity.json", identity)
        groups = [output, *sorted(output.glob("transport_recovery_[0-9]*"))]
        for group in groups:
            recovered = recover_completion(common, group)
            if recovered is not None:
                return recovered
        destination = output
        if any(next(group.glob("attempt[0-9]*"), None) is not None for group in groups):
            destination = output / f"transport_recovery_{len(groups):04d}"
        return transport.model_completion(messages, schema, cap, destination, client)

    common.model_completion = completion


def run_version(name, workers):
    plan = verify_plan()
    sys.path.insert(0, str(VERSIONS / name))
    import common
    import evaluate

    frozen = common.verify_freeze()
    if frozen != plan["versions"][name]["protocol_freeze_sha256"]:
        raise ValueError("Version identity changed")
    install_transport(common)
    root = HERE / "evaluation" / name
    root.mkdir(parents=True, exist_ok=True)
    with (root / "run.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        immutable(
            root / "run.json",
            {
                "plan_sha256": sha(HERE / "plan.json"),
                "driver_sha256": sha(__file__),
                "protocol_freeze_sha256": frozen,
                "workers": workers,
                "packages": {
                    key: package_version(key)
                    for key in ("openai", "foundry-aws-gateway", "jsonschema")
                },
                "transport_policy": plan["transport_policy"],
            },
        )
        rows = {}
        summary = {
            "expected": 128,
            "records": [],
            "candidate": "p1",
            "actual_judge_model": common.MODEL,
            "protocol_freeze_sha256": frozen,
            "plan_sha256": sha(HERE / "plan.json"),
            "target_labels_withheld": True,
            "semantic_samples_per_candidate_revision_case": 1,
            "development_only": True,
            "promoted": False,
            "source_stage": "e2e_comparison_output",
            "runtime_stage_adapter": "scene_generation literal; not held-out accuracy",
            "transport_policy": plan["transport_policy"],
        }

        def persist():
            summary["records"] = [rows[key] for key in sorted(rows)]
            summary["terminal"] = len(rows) == 128
            summary["complete"] = summary["terminal"] and all(
                row["status"] == "complete" for row in rows.values()
            )
            summary["updated_utc"] = datetime.now(UTC).isoformat()
            common.write_json(root / "summary.json", summary)

        def job(case):
            prior = plan["versions"][name]["reused"].get(case["id"])
            if prior is not None:
                validate_reuse(prior, case, frozen)
                return {**prior, "expansion_reused": True}
            assessment = root / "p1" / case["id"] / "assessment.json"
            if assessment.exists():
                row = load(assessment)
                if row["status"] == "complete":
                    validate_reuse(row, case, frozen)
                elif row["status"] != "error":
                    raise ValueError("Non-terminal saved assessment")
                return row
            if shutil.disk_usage(HERE).free < 256 * 1024**2:
                raise RuntimeError(
                    "Less than256MiB free; stop safely before another case"
                )
            return evaluate.assess(case, "p1", root)

        persist()
        with ThreadPoolExecutor(max_workers=workers) as pool:
            jobs = {pool.submit(job, case): case["id"] for case in plan["cases"]}
            for future in as_completed(jobs):
                row = future.result()
                rows[row["id"]] = row
                persist()
                print(
                    json.dumps(
                        {
                            "version": name,
                            "done": len(rows),
                            "expected": 128,
                            "id": row["id"],
                            "status": row["status"],
                            "score": row["score"],
                            "reused": row.get("expansion_reused", False),
                        }
                    ),
                    flush=True,
                )
        print(
            json.dumps({"version": name, "complete": summary["complete"]}), flush=True
        )
        if not summary["complete"]:
            raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "run-version"))
    parser.add_argument("--version", choices=REVISIONS)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error("Use1-8 bounded workers per version")
    if args.command == "prepare":
        prepare()
    elif args.version is None:
        parser.error("--version is required")
    else:
        run_version(args.version, args.workers)
