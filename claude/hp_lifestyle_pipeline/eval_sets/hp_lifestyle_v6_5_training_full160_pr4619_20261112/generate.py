"""Run the unchanged pinned native pipeline with durable, attempt-level SDK evidence."""
from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import fcntl
import importlib.util
import io
import json
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace

import study

sys.path.insert(0, str(study.NATIVE))
from hp3p import openai_client, pipeline  # noqa: E402
from hp3p.catalog import load_catalog  # noqa: E402
from hp3p.evalset import Row  # noqa: E402
from hp3p.mask import prepare as prepare_product  # noqa: E402

FALLBACK = study.HERE / "source/baseline_recovery/source/fallback_profiles.py"
spec = importlib.util.spec_from_file_location("frozen_baseline_no_statistics", FALLBACK)
if spec is None or spec.loader is None:
    raise RuntimeError("The frozen baseline no-statistics adapter is unavailable")
fallback = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fallback)
OLD_ENDPOINT = study.PRIOR / "endpoint_pr4523"
CATALOG = OLD_ENDPOINT / "runtime/assets/styles.json"
CAPTIONS = OLD_ENDPOINT / "runtime/hp3p/data/ref_captions.json"
PROFILES = study.HERE / "source/baseline/profiles.json"
SIZE = (2368, 1776)


def atomic(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    temporary.replace(path)


def provider():
    import foundry_aws_gateway.llm

    return foundry_aws_gateway.llm.get_openai().with_options(max_retries=0, timeout=540.0)


def serial(value):
    if isinstance(value, io.BytesIO):
        return {"base64": base64.b64encode(value.getvalue()).decode()}
    if isinstance(value, dict):
        return {key: serial(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(item) for item in value]
    return value


class RecordingMethod:
    def __init__(self, owner, kind, call):
        self.owner, self.kind, self.call = owner, kind, call

    def __call__(self, **params):
        if self.kind == "image" and any(c["kind"] == "image" for c in self.owner.calls):
            raise RuntimeError("One image submission per attempt; replay requires reconciliation")
        number = len(self.owner.calls) + 1
        prefix = f"{number:02d}_{self.kind}"
        request = self.owner.directory / (prefix + ".request.json")
        study.emit(request, serial(params))
        record = {
            "kind": self.kind, "status": "started", "started_at": study.now(),
            "request": request.name, "request_sha256": study.sha(request),
            "response": prefix + ".response.json",
        }
        self.owner.calls.append(record)
        self.owner.flush()
        try:
            response = self.call(**params)
            path = self.owner.directory / record["response"]
            study.emit(path, response.model_dump(mode="json"))
            record.update(status="done", response_sha256=study.sha(path))
            return response
        except Exception as error:
            record.update(
                status="error", error_type=type(error).__name__,
                status_code=getattr(error, "status_code", None),
            )
            raise
        finally:
            record["ended_at"] = study.now()
            self.owner.flush()


class RecordingClient(openai_client.OpenAIClient):
    """Keep the native SDK argument construction, validation and image decoding unchanged."""

    def __init__(self, directory, sdk=None):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.calls = []
        self.sdk = provider() if sdk is None else sdk
        self.client = SimpleNamespace(
            chat=SimpleNamespace(completions=SimpleNamespace(
                create=RecordingMethod(self, "text", self.sdk.chat.completions.create))),
            images=SimpleNamespace(edit=RecordingMethod(self, "image", self.sdk.images.edit)),
        )

    def flush(self):
        atomic(self.directory / "calls.json", self.calls)

    def close(self):
        self.sdk.close()


def prepare():
    source = study.verify()
    baseline = study.load(study.HERE / "source/baseline/manifest.json")
    recovery = study.load(study.HERE / "source/baseline_recovery/manifest.json")
    if study.sha(FALLBACK) != recovery["helper_files"]["fallback_profiles.py"]:
        raise ValueError("Frozen baseline fallback implementation differs from its published manifest")
    for relative, expected in baseline["source_files"].items():
        if study.sha(study.NATIVE / relative) != expected:
            raise ValueError(f"Native source differs from the exact baseline commit: {relative}")
    if study.sha(CATALOG) != baseline["catalog_sha256"] or study.sha(CAPTIONS) != baseline["captions_sha256"]:
        raise ValueError("The reference catalogue/captions differ from the actual V6.4 baseline")
    artifacts = Path(source["storage"]["artifact_root"])
    inputs = OLD_ENDPOINT / "input_bundle"
    fixed = study.load(inputs / "manifest.json")
    prepared = {}
    for view in fixed["entries"]:
        path = inputs / view["product_path"]
        if study.sha(path) != view["product_sha256"]:
            raise ValueError("Original fixed-view render changed")
        body, _ = prepare_product(path.read_bytes(), SIZE)
        target = artifacts / "inputs/products" / (study.digest(body) + ".png")
        study.emit(target, body)
        prepared[study.digest(body)] = (view, target, path)
    previous = {row["prompt_key"]: row for row in study.load(study.HERE / "source/baseline/cases.json")}
    fe = {study.prompt_key(row): row for row in study.load(study.HERE / "source/fe/data.json")["rows"]}
    prompts = study.load(study.HERE / "source/prompts_for_runner_160.json")["prompts"]
    if len(prompts) != 160 or len(previous) != 160 or len(fe) != 160:
        raise ValueError("Expected complete unique160-row prompt/baseline/FE sources")
    cases = []
    for prompt in prompts:
        key = prompt["prompt_key"]
        old, row = previous[key], fe[key]
        if study.digest(prompt["text"].encode()) != prompt["text_sha256"]:
            raise ValueError("A frozen actual V6.5 source text differs")
        if (row["images"][5]["text_content"] != old["user_prompt"]
                or row["images"][6]["text_content"] != prompt["text"]
                or old["rank"] != prompt["bank_rank"]
                or old["group"] != prompt["device_id"] + "__" + prompt["camera_tag"]
                or old["id"] != key.replace("::", "__")):
            raise ValueError("Original prompt or device/camera/rank binding differs")
        view, product, raw = prepared[old["product_sha256"]]
        if view["camera"] != old["source_camera_metadata"]:
            raise ValueError("Source digital-twin camera differs from the existing V6.4 run")
        cases.append({
            "id": old["id"], "prompt_key": key, "prompt": prompt,
            "group": old["group"], "rank": old["rank"],
            "device": old["device"], "camera": old["camera"],
            "product_path": str(product), "product_sha256": study.sha(product),
            "original_product_path": str(raw), "original_product_sha256": study.sha(raw),
            "source_camera_metadata": old["source_camera_metadata"],
            "source_input": old["source_input"], "baseline_image": row["images"][1],
            "baseline_v64_prompt": row["images"][5],
        })
    if len({c["id"] for c in cases}) != 160 or len({c["prompt"]["text"] for c in cases}) != 160:
        raise ValueError("Missing or duplicated final V6.5 source slots/texts")
    study.emit(study.HERE / "cases.json", cases)
    study.emit(artifacts / "cases.json", cases)
    frozen = [Path(__file__), Path(study.__file__), CATALOG, CAPTIONS, FALLBACK,
              study.HERE / "source_manifest.json", study.HERE / "cases.json"]
    frozen += [Path(c[k]) for c in cases for k in ("product_path", "original_product_path")]
    frozen += [p for p in (study.HERE / "source/baseline_recovery").rglob("*")
               if p.is_file() and "__pycache__" not in p.parts]
    configuration = {
        "at_utc": study.now(), "commit": study.COMMIT, "size": list(SIZE), "ref_count": 1,
        "captions": True, "reference_blue": False, "scap_realism": True,
        "fallback_identity": fallback.FallbackProfiles(PROFILES).identity,
        "source_preflight_canvas_choice_superseded": True,
        "canvas_decision": "User subsequently confirmed matching native2368x1776 to existing V6.4/PR4619.",
        "frozen_files": {str(p): study.sha(p) for p in sorted(set(frozen))},
    }
    sdk = provider()
    try:
        if sdk.max_retries != 0 or sdk.timeout != 540:
            raise ValueError("Unexpected provider retry/timeout settings")
    finally:
        sdk.close()
    study.emit(study.HERE / "execution_manifest.json", configuration)
    study.emit(artifacts / "execution_manifest.json", configuration)
    print(json.dumps({"prepared": 160, "views": len(prepared), "size": SIZE,
                      "provider_initialized_without_model_calls": True}))


def verify():
    source = study.verify()
    execution = study.load(study.HERE / "execution_manifest.json")
    for name, expected in execution["frozen_files"].items():
        if study.sha(name) != expected:
            raise ValueError(f"Frozen generation input/driver changed: {name}")
    return Path(source["storage"]["artifact_root"]), study.load(study.HERE / "cases.json")


def may_retry(calls):
    images = [call for call in calls if call["kind"] == "image"]
    return not images or all(call["status"] == "error" and call.get("status_code") == 429 for call in images)


def completed(root, case):
    path = root / "completed" / (case["id"] + ".json")
    if not path.exists():
        return None
    result = study.load(path)
    if (result["prompt_key"] != case["prompt_key"]
            or result["prompt_sha256"] != case["prompt"]["text_sha256"]
            or study.sha(result["image_path"]) != result["image_sha256"]
            or study.sha(result["result_path"]) != result["result_sha256"]
            or study.sha(result["calls_path"]) != result["calls_sha256"]):
        raise ValueError("Previously completed native output or its provenance changed")
    return result


def generate(ids, workers):
    root, cases = verify()
    lock = (study.HERE / "generation.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if ids:
        wanted = set(ids.split(","))
        cases = [case for case in cases if case["id"] in wanted]
        if {case["id"] for case in cases} != wanted:
            raise ValueError("Unknown or duplicated generation selection")
    catalog, captions = load_catalog(CATALOG), study.load(CAPTIONS)
    profiles = fallback.FallbackProfiles(PROFILES)
    progress_lock = threading.Lock()
    outcomes = []

    def one(case):
        existing = completed(root, case)
        if existing is not None:
            return {"id": case["id"], "status": "done", "reused": True}
        base = root / "attempts" / case["id"]
        earlier = sorted(base.glob("attempt_*"))
        for path in earlier:
            if not (path / "terminal.json").exists():
                raise RuntimeError(f"Interrupted attempt requires reconciliation before resubmission: {path}")
            journal = study.load(path / "sdk/calls.json") if (path / "sdk/calls.json").exists() else []
            if not may_retry(journal):
                raise RuntimeError(f"Prior image submission requires reconciliation, not resampling: {path}")
        for number in range(len(earlier) + 1, len(earlier) + 5):
            attempt = base / f"attempt_{number:04d}"
            attempt.mkdir(parents=True)
            study.emit(attempt / "started.json", {
                "at_utc": study.now(), "case_id": case["id"],
                "prompt_sha256": case["prompt"]["text_sha256"],
                "execution_manifest_sha256": study.sha(study.HERE / "execution_manifest.json"),
            })
            client = None
            try:
                client = RecordingClient(attempt / "sdk")
                row = Row(case["id"], case["prompt"]["text"], "frozen-local-twin", *SIZE, [])
                result = pipeline.run_row(
                    row, client, catalog, attempt / "native",
                    Path(case["product_path"]).read_bytes(), captions, ref_count=1, size=SIZE,
                    camera=case["source_camera_metadata"], scap=profiles,
                )
                calls = client.calls
                directory = attempt / "native/rows" / case["id"]
                study.emit(attempt / "terminal.json", {
                    "at_utc": study.now(), "status": result["status"],
                    "error": result.get("error"), "calls": calls,
                })
                if result["status"] == "ok":
                    image = directory / "ours.png"
                    if study.sha(image) != study.sha(directory / "gpt_1.png"):
                        raise ValueError("Native raw image bytes differ; postprocessing is forbidden")
                    record = {
                        "at_utc": study.now(), "prompt_key": case["prompt_key"],
                        "prompt_sha256": case["prompt"]["text_sha256"],
                        "image_path": str(image), "image_sha256": study.sha(image),
                        "result_path": str(directory / "result.json"),
                        "result_sha256": study.sha(directory / "result.json"),
                        "calls_path": str(attempt / "sdk/calls.json"),
                        "calls_sha256": study.sha(attempt / "sdk/calls.json"),
                        "attempt": str(attempt), "attempt_number": number,
                        "statistics_disabled": result["scap_context"].get("statistics_disabled", False),
                    }
                    study.emit(root / "completed" / (case["id"] + ".json"), record)
                    study.emit(study.HERE / "completed" / (case["id"] + ".json"), record)
                    return {"id": case["id"], "status": "done", "attempts": number,
                            "no_statistics": record["statistics_disabled"]}
                if not may_retry(calls):
                    return {"id": case["id"], "status": "blocked", "error": result.get("error")}
                print(json.dumps({"id": case["id"], "attempt": number,
                                  "pre_image_failure": result.get("error")}), flush=True)
            finally:
                if client is not None:
                    client.close()
            time.sleep(min(10 * number, 40))
        return {"id": case["id"], "status": "failed", "error": "Four preserved recoverable attempts exhausted"}

    def tracked(case):
        result = one(case)
        with progress_lock:
            outcomes.append(result)
            atomic(study.HERE / "generation_progress.json", {
                "at_utc": study.now(), "selection": len(cases), "completed": len(outcomes),
                "done": sum(item["status"] == "done" for item in outcomes), "outcomes": outcomes,
            })
            print(json.dumps({"progress": f"{len(outcomes)}/{len(cases)}", **result}), flush=True)
        return result

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(tracked, cases))
    if any(result["status"] != "done" for result in results):
        raise RuntimeError("Generation is incomplete; preserved failed/ambiguous attempts require review")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "generate"])
    parser.add_argument("--ids")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    else:
        generate(args.ids, args.workers)
