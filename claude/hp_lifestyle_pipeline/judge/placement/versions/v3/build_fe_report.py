#!/usr/bin/env python3
"""Build validated FE reports for the 160-scene V6.1 placement-judge run.

This script performs no model calls and no uploads. It requires one result.json
per manifest row, validates the exact runtime inputs and frozen protocol claims,
writes the supported FE data.json contract, and copies the canonical vendored
annotation viewer byte-for-byte.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import parse_qs, urlencode


ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = ROOT / "data/new_v6_1_eval_20261105/manifest.json"
DEFAULT_OUTPUT = ROOT / "fe_reports/v6_1_20261105"
DEFAULT_TITLE = "HP natural-placement judge V3 — V6.1 GPT Image 2 scene evaluation"
DEFAULT_PUBLISH_BUCKET = "foundry-hp-enterprise-adobe-assets"
DEFAULT_PUBLISH_PREFIX = "hp_natural_placement_judge_v3_v6_1_20261105"
CONSENSUS_TITLE = "HP natural-placement judge V3 — consensus revision — V6.1 GPT Image 2 scenes"
CONSENSUS_PUBLISH_PREFIX = DEFAULT_PUBLISH_PREFIX + "/consensus_v2"
VENDORED_VIEWER = Path(
    os.path.expanduser("~/.claude/scripts/fe_html/annotation_viewer.html")
)
TWO_PASS_ROOT = ROOT / "experiments/two_pass"
TWO_PASS_COMBINER = TWO_PASS_ROOT / "combine.py"
TWO_PASS_POLICY = TWO_PASS_ROOT / "policy.json"
V2_ROOT = ROOT.parent / "v2"
VERIFY_ROOT = ROOT / "experiments/verify_additions"
VERIFY_MERGER_V2 = VERIFY_ROOT / "merge_verified_v2.py"
VERIFY_PROTOCOL_SNAPSHOT = VERIFY_ROOT / "protocol_snapshots/semantic_v3"
CONSENSUS_ROOT = ROOT / "experiments/consensus_policy"
INDEPENDENT_CHECK_ROOT = ROOT / "experiments/independent_component_check"
GATEWAY = "https://foundry-aws-corp.adobe.io"
REPORT_SCOPES = (("combined", None), ("laptops", "laptop"), ("printers", "printer"))
COMPONENTS = (
    "support_scenario",
    "access_usability",
    "orientation_alignment",
    "scale_perspective",
    "contact_integration",
)
RUNTIME_KEYS = {
    "generated_image",
    "twin_image",
    "product_type",
    "scene_prompt",
    "image_stage",
}
SOURCE_LABEL_KEYS = {
    "human_feedback",
    "diagnostic_expectation",
    "extended_validation_expectation",
}
_TWO_PASS_COMBINER_MODULE: Any | None = None
_VERIFIED_MERGER_MODULES: dict[str, Any] = {}
_CONSENSUS_MODULES: dict[str, Any] = {}
_INDEPENDENT_CHECK_MODULE: Any | None = None

QUESTION_WIRE = [
    {
        "text": "Is the IMAGE naturally arranged?",
        "hard_check": False,
        "group": "1. Image natural placement quality",
        "comment_box": True,
        "rubric": {
            "key": "custom",
            "name": "Image natural placement",
            "options": [
                {"value": "pass", "label": "Pass", "tone": "good"},
                {"value": "review", "label": "Review", "tone": "neutral"},
                {"value": "fail", "label": "Fail", "tone": "bad"},
            ],
        },
    },
    {
        "text": "Do you agree with the JUDGE assessment and explanation?",
        "hard_check": False,
        "group": "2. Judge assessment agreement",
        "comment_box": True,
        "rubric": {
            "key": "custom",
            "name": "Agreement with judge",
            "options": [
                {"value": "agree", "label": "Agree", "tone": "good"},
                {
                    "value": "partly_agree",
                    "label": "Partly agree",
                    "tone": "neutral",
                },
                {"value": "disagree", "label": "Disagree", "tone": "bad"},
            ],
        },
    },
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_json(path: Path) -> Any:
    require(path.is_file(), f"missing JSON file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def sha256(path: Path) -> str:
    require(path.is_file(), f"missing file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    temporary.chmod(0o644)
    os.replace(temporary, path)


def review_query(ldap: str) -> str:
    encoded = base64.b64encode(
        json.dumps(QUESTION_WIRE, ensure_ascii=False, separators=(",", ":")).encode()
    ).decode("ascii")
    return "?" + urlencode({"ldap": ldap, "q": encoded})


def validate_review_query(query: str, ldap: str) -> None:
    try:
        parsed = parse_qs(query.removeprefix("?"), strict_parsing=True)
        require(set(parsed) == {"ldap", "q"}, "review query fields differ")
        require(parsed["ldap"] == [ldap], "review query LDAP differs")
        decoded = json.loads(base64.b64decode(parsed["q"][0], validate=True))
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid FE review query: {exc}") from exc
    require(decoded == QUESTION_WIRE, "FE review query does not round-trip")


def gateway_url(image: Mapping[str, Any], record_id: str, label: str) -> str:
    for key in (
        "public_url",
        "source_public_url",
        "preview_public_url",
        "source_artifact_url",
    ):
        value = image.get(key)
        if isinstance(value, str) and value.startswith(("https://", "http://")):
            return value
    for key in ("s3_uri", "source_s3_uri", "preview_s3_uri"):
        value = image.get(key)
        if isinstance(value, str) and value.startswith("s3://"):
            bucket, separator, object_key = value[5:].partition("/")
            require(bool(bucket and separator and object_key), f"{record_id}: bad {label} S3 URI")
            return f"{GATEWAY}/asset/{bucket}/{object_key}"
    raise ValueError(f"{record_id}: {label} lacks an HTTP or S3 URL")


def manifest_records(payload: Any, expected_rows: int | None) -> list[Mapping[str, Any]]:
    require(isinstance(payload, Mapping), "manifest must be an object")
    records = payload.get("records")
    require(isinstance(records, list), "manifest records must be a list")
    require(all(isinstance(record, Mapping) for record in records), "manifest row is not an object")
    declared = payload.get("expected_count")
    require(isinstance(declared, int) and not isinstance(declared, bool), "manifest expected_count missing")
    require(len(records) == declared, "manifest record count differs from expected_count")
    if expected_rows is not None:
        require(len(records) == expected_rows, f"expected {expected_rows} rows, found {len(records)}")
    ids = [record.get("id") for record in records]
    require(all(isinstance(value, str) and value for value in ids), "manifest has invalid IDs")
    require(len(ids) == len(set(ids)), "manifest has duplicate IDs")
    return records


def result_paths(results_dir: Path) -> dict[str, Path]:
    require(results_dir.is_dir(), f"results directory missing: {results_dir}")
    paths = sorted(results_dir.glob("*/result.json"))
    require(bool(paths), f"no result.json files under {results_dir}")
    by_id: dict[str, Path] = {}
    for path in paths:
        record_id = path.parent.name
        require(record_id not in by_id, f"duplicate result ID: {record_id}")
        by_id[record_id] = path.resolve()
    return by_id


def validate_progress(
    results_dir: Path,
    manifest_path: Path,
    record_ids: Sequence[str],
    paths: Mapping[str, Path],
) -> dict[str, Any]:
    progress_path = results_dir / "progress.json"
    payload = load_json(progress_path)
    require(isinstance(payload, Mapping), "progress ledger must be an object")
    require(payload.get("schema_version") == "placement-v3-batch-progress-v1", "progress schema differs")
    require(payload.get("status") == "complete", "judge progress is not complete")
    require(payload.get("record_ids") == list(record_ids), "progress IDs/order differ from manifest")
    manifest_hash = sha256(manifest_path)
    require(payload.get("manifest_sha256") == manifest_hash, "progress manifest hash differs")
    require(Path(str(payload.get("manifest", ""))).resolve() == manifest_path, "progress manifest path differs")
    items = payload.get("items")
    require(isinstance(items, Mapping) and set(items) == set(record_ids), "progress items differ")
    for record_id in record_ids:
        item = items[record_id]
        require(isinstance(item, Mapping), f"{record_id}: progress item invalid")
        require(item.get("status") in {"done", "cached"}, f"{record_id}: progress item incomplete")
        require(Path(str(item.get("result_path", ""))).resolve() == paths[record_id], f"{record_id}: progress result path differs")
        require(item.get("result_sha256") == sha256(paths[record_id]), f"{record_id}: progress result hash differs")
    return {
        "path": str(progress_path.resolve()),
        "sha256": sha256(progress_path),
        "status": payload.get("status"),
    }


def expected_runtime_input(record: Mapping[str, Any]) -> dict[str, str]:
    record_id = str(record["id"])
    generated = record.get("generated_image")
    twin = record.get("twin_image")
    require(isinstance(generated, Mapping), f"{record_id}: generated_image missing")
    require(isinstance(twin, Mapping), f"{record_id}: twin_image missing")
    generated_path = Path(str(generated.get("local_path", ""))).resolve()
    twin_path = Path(str(twin.get("local_path", ""))).resolve()
    require(generated_path.is_file(), f"{record_id}: generated image missing: {generated_path}")
    require(twin_path.is_file(), f"{record_id}: twin image missing: {twin_path}")
    generated_hash = sha256(generated_path)
    twin_hash = sha256(twin_path)
    prompt = record.get("scene_prompt")
    require(isinstance(prompt, str), f"{record_id}: scene_prompt must be text")
    prompt_hash = text_sha256(prompt)
    hashes = record.get("hashes")
    require(isinstance(hashes, Mapping), f"{record_id}: hashes missing")
    require(
        generated_hash == generated.get("sha256") == hashes.get("generated_image_sha256"),
        f"{record_id}: generated image hash mismatch",
    )
    require(
        twin_hash == twin.get("sha256") == hashes.get("twin_image_sha256"),
        f"{record_id}: twin image hash mismatch",
    )
    require(
        prompt_hash == record.get("scene_prompt_sha256") == hashes.get("scene_prompt_sha256"),
        f"{record_id}: prompt hash mismatch",
    )
    require(record.get("image_stage") == "scene_generation", f"{record_id}: image stage differs")
    product_type = record.get("device_type", record.get("product_type"))
    require(product_type in {"printer", "laptop"}, f"{record_id}: invalid device type")
    return {
        "generated_image": str(generated_path),
        "twin_image": str(twin_path),
        "product_type": str(product_type),
        "scene_prompt": prompt,
        "image_stage": "scene_generation",
    }


def json_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def expected_input_identity(record: Mapping[str, Any]) -> dict[str, str]:
    runtime = expected_runtime_input(record)
    identity = {
        "generated_image_sha256": sha256(Path(runtime["generated_image"])),
        "twin_image_sha256": sha256(Path(runtime["twin_image"])),
        "scene_prompt_sha256": text_sha256(runtime["scene_prompt"]),
        "product_type": runtime["product_type"],
        "image_stage": runtime["image_stage"],
    }
    identity["input_identity_sha256"] = json_sha256(identity)
    return identity


def raw_observation(response: Mapping[str, Any], record_id: str, role: str) -> Any:
    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"{record_id} {role}: raw response has no message content") from exc
    require(isinstance(content, str), f"{record_id} {role}: raw response content is not text")
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{record_id} {role}: raw response content is not JSON") from exc


def load_two_pass_combiner() -> Any:
    global _TWO_PASS_COMBINER_MODULE
    if _TWO_PASS_COMBINER_MODULE is not None:
        return _TWO_PASS_COMBINER_MODULE
    require(TWO_PASS_COMBINER.is_file(), f"two-pass combiner missing: {TWO_PASS_COMBINER}")
    spec = importlib.util.spec_from_file_location("placement_fe_two_pass_combiner", TWO_PASS_COMBINER)
    require(spec is not None and spec.loader is not None, "could not load two-pass combiner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _TWO_PASS_COMBINER_MODULE = module
    return module


def load_verified_merger(path: Path = VERIFY_MERGER_V2) -> Any:
    path = path.resolve()
    cache_key = f"{path}:{sha256(path)}"
    if cache_key in _VERIFIED_MERGER_MODULES:
        return _VERIFIED_MERGER_MODULES[cache_key]
    require(path.is_file(), f"verified merger missing: {path}")
    verify_path = str(VERIFY_ROOT)
    inserted = verify_path not in sys.path
    if inserted:
        sys.path.insert(0, verify_path)
    try:
        spec = importlib.util.spec_from_file_location(
            "placement_fe_verified_merger_" + sha256(path)[:16], path
        )
        require(spec is not None and spec.loader is not None, "could not load verified merger")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        if inserted:
            sys.path.remove(verify_path)
    _VERIFIED_MERGER_MODULES[cache_key] = module
    return module


def load_consensus_generator(path: Path) -> Any:
    path = path.resolve()
    cache_key = f"{path}:{sha256(path)}"
    if cache_key in _CONSENSUS_MODULES:
        return _CONSENSUS_MODULES[cache_key]
    require(path.is_file(), f"consensus generator missing: {path}")
    spec = importlib.util.spec_from_file_location(
        "placement_fe_consensus_" + sha256(path)[:16], path
    )
    require(spec is not None and spec.loader is not None, "could not load consensus generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _CONSENSUS_MODULES[cache_key] = module
    return module


def load_independent_check_runner() -> Any:
    global _INDEPENDENT_CHECK_MODULE
    if _INDEPENDENT_CHECK_MODULE is not None:
        return _INDEPENDENT_CHECK_MODULE
    path = INDEPENDENT_CHECK_ROOT / "run_check.py"
    require(path.is_file(), f"independent-check runner missing: {path}")
    spec = importlib.util.spec_from_file_location("placement_fe_independent_check", path)
    require(spec is not None and spec.loader is not None, "could not load independent-check runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _INDEPENDENT_CHECK_MODULE = module
    return module


def validate_artifact(
    artifact: Any, *, record_id: str, role: str, name: str
) -> tuple[Path, Mapping[str, Any]]:
    require(isinstance(artifact, Mapping), f"{record_id} {role}: {name} artifact missing")
    path = Path(str(artifact.get("path", ""))).resolve()
    require(path.is_file(), f"{record_id} {role}: {name} artifact path missing")
    require(artifact.get("sha256") == sha256(path), f"{record_id} {role}: {name} hash differs")
    payload = load_json(path)
    require(isinstance(payload, Mapping), f"{record_id} {role}: {name} artifact is not an object")
    return path, payload


def validate_two_pass_stage(
    *,
    record: Mapping[str, Any],
    role: str,
    stage: Any,
    expected_identity: Mapping[str, str],
    policy: Mapping[str, Any],
    combined_case_dir: Path,
) -> dict[str, Any]:
    record_id = str(record["id"])
    require(isinstance(stage, Mapping), f"{record_id}: {role} stage missing")
    require(stage.get("input_identity") == expected_identity, f"{record_id} {role}: input identity differs")
    artifacts = stage.get("artifacts")
    require(isinstance(artifacts, Mapping), f"{record_id} {role}: artifacts missing")
    request_path, request = validate_artifact(
        artifacts.get("request"), record_id=record_id, role=role, name="request"
    )
    response_path, response = validate_artifact(
        artifacts.get("raw_response"), record_id=record_id, role=role, name="raw response"
    )
    result_path, result = validate_artifact(
        artifacts.get("result"), record_id=record_id, role=role, name="result"
    )
    source_case_dir = Path(str(stage.get("source_case_dir", ""))).resolve()
    require(
        request_path.parent == response_path.parent == result_path.parent == source_case_dir,
        f"{record_id} {role}: source artifact paths do not share the declared case directory",
    )
    copied_response = combined_case_dir / "raw_responses" / role / "response.json"
    require(copied_response.is_file(), f"{record_id} {role}: preserved raw response copy missing")
    require(
        sha256(copied_response) == sha256(response_path),
        f"{record_id} {role}: preserved raw response bytes differ",
    )

    runtime = expected_runtime_input(record)
    require(request.get("input") == runtime, f"{record_id} {role}: request input differs from manifest")
    require(set(request["input"]) == RUNTIME_KEYS, f"{record_id} {role}: request input is not whitelisted")
    require(
        not any(key in request["input"] for key in SOURCE_LABEL_KEYS),
        f"{record_id} {role}: source annotation entered model input",
    )
    images = request.get("images")
    require(isinstance(images, Mapping), f"{record_id} {role}: request image metadata missing")
    require(
        images.get("generated_image", {}).get("sha256") == expected_identity["generated_image_sha256"],
        f"{record_id} {role}: generated image hash differs",
    )
    require(
        images.get("twin_image", {}).get("sha256") == expected_identity["twin_image_sha256"],
        f"{record_id} {role}: twin image hash differs",
    )
    require(result.get("ok") is True, f"{record_id} {role}: saved stage result failed")
    require(result.get("fingerprint") == request.get("fingerprint"), f"{record_id} {role}: fingerprint differs")
    judgment = result.get("judgment")
    require(isinstance(judgment, Mapping), f"{record_id} {role}: stage judgment missing")
    require(stage.get("judgment") == judgment, f"{record_id} {role}: embedded judgment differs")
    require(
        raw_observation(response, record_id, role) == judgment.get("observation"),
        f"{record_id} {role}: raw response differs from stage observation",
    )

    expected = policy.get("stages", {}).get(role)
    require(isinstance(expected, Mapping), f"two-pass policy lacks {role}")
    require(request.get("protocol_version") == expected.get("protocol_version"), f"{record_id} {role}: protocol differs")
    require(request.get("model_requested") == expected.get("model"), f"{record_id} {role}: requested model differs")
    require(request.get("reasoning_effort") == expected.get("reasoning_effort"), f"{record_id} {role}: reasoning effort differs")
    require(request.get("visual_anchors_enabled") is expected.get("visual_anchors"), f"{record_id} {role}: anchor setting differs")
    core_root = V2_ROOT if role == "baseline_v2" else ROOT
    for request_key, filename in (
        ("runner_sha256", "run_judge.py"),
        ("system_prompt_sha256", "system_prompt.md"),
        ("schema_sha256", "observation_schema.json"),
        ("scoring_sha256", "scoring.py"),
    ):
        require(
            request.get(request_key) == sha256(core_root / filename),
            f"{record_id} {role}: {request_key} differs from its protocol source bytes",
        )
    returned = result.get("model_returned")
    require(
        isinstance(returned, str) and re.fullmatch(r"gpt-5\.5(?:-\d{4}-\d{2}-\d{2})?", returned) is not None,
        f"{record_id} {role}: returned model differs",
    )

    combiner = load_two_pass_combiner()
    expected_fingerprint = combiner._stage_protocol_fingerprint(request, role)
    require(
        stage.get("protocol_fingerprint") == expected_fingerprint,
        f"{record_id} {role}: embedded protocol fingerprint differs",
    )
    if role == "baseline_v2":
        require(
            request.get("visual_anchor_manifest_sha256") == sha256(V2_ROOT / "data/visual_anchors.json"),
            f"{record_id}: V2 visual anchor manifest hash differs",
        )
        anchors = request.get("visual_anchors", {}).get("examples", [])
        excluded = request.get("excluded_target_identical_anchor_ids", [])
        require(isinstance(anchors, list) and isinstance(excluded, list), f"{record_id}: V2 anchor audit invalid")
        require(
            len(anchors) + len(excluded) == expected.get("frozen_anchor_manifest_expected_count"),
            f"{record_id}: V2 anchor accounting differs",
        )
    return {
        "judgment": judgment,
        "protocol_fingerprint": expected_fingerprint,
        "artifacts": {
            "request": {"path": str(request_path), "sha256": sha256(request_path)},
            "raw_response": {"path": str(response_path), "sha256": sha256(response_path)},
            "result": {"path": str(result_path), "sha256": sha256(result_path)},
            "preserved_raw_response": {
                "path": str(copied_response.resolve()),
                "sha256": sha256(copied_response),
            },
        },
    }


def protocol_claims(metadata: Mapping[str, Any]) -> dict[str, Any]:
    files = metadata.get("files")
    require(isinstance(files, Mapping), "protocol metadata files map missing")
    required = {
        "system_prompt.md": "system_prompt_sha256",
        "observation_schema.json": "schema_sha256",
        "scoring.py": "scoring_sha256",
        "run_judge.py": "runner_sha256",
    }
    claims: dict[str, Any] = {
        result_key: files[path] for path, result_key in required.items()
    }
    claims.update(
        {
            "model_requested": metadata.get("model"),
            "reasoning_effort": metadata.get("reasoning_effort"),
            "visual_anchors_enabled": metadata.get("visual_anchors", True),
        }
    )
    require(all(isinstance(value, str) and value for value in claims.values() if not isinstance(value, bool)), "protocol claim missing")
    require(isinstance(claims["visual_anchors_enabled"], bool), "visual_anchors claim must be boolean")
    return claims


def validate_result(
    record: Mapping[str, Any], path: Path, claims: Mapping[str, Any]
) -> tuple[Mapping[str, Any], Mapping[str, Any], dict[str, Any]]:
    record_id = str(record["id"])
    result = load_json(path)
    require(isinstance(result, Mapping), f"{record_id}: result is not an object")
    require(result.get("ok") is True, f"{record_id}: result is not successful")
    runtime = expected_runtime_input(record)
    require(result.get("input") == runtime, f"{record_id}: result input differs from manifest")
    require(set(result["input"]) == RUNTIME_KEYS, f"{record_id}: runtime input is not whitelisted")
    for key, expected in claims.items():
        require(result.get(key) == expected, f"{record_id}: result {key} differs from protocol metadata")
    images = result.get("images")
    require(isinstance(images, Mapping), f"{record_id}: result image hashes missing")
    hashes = record["hashes"]
    require(
        images.get("generated_image", {}).get("sha256") == hashes["generated_image_sha256"],
        f"{record_id}: result generated hash differs",
    )
    require(
        images.get("twin_image", {}).get("sha256") == hashes["twin_image_sha256"],
        f"{record_id}: result twin hash differs",
    )
    judgment = result.get("judgment")
    require(isinstance(judgment, Mapping), f"{record_id}: judgment missing")
    require(judgment.get("verdict") in {"pass", "review", "fail"}, f"{record_id}: invalid verdict")
    score = judgment.get("natural_placement_score")
    require(isinstance(score, (int, float)) and not isinstance(score, bool), f"{record_id}: score missing")
    require(0 <= float(score) <= 100, f"{record_id}: score outside 0..100")
    observation = judgment.get("observation")
    require(isinstance(observation, Mapping), f"{record_id}: observation missing")
    components = observation.get("components")
    require(isinstance(components, Mapping), f"{record_id}: components missing")
    require(set(components) == set(COMPONENTS), f"{record_id}: component set differs")
    return result, judgment, {
        "result_path": str(path),
        "result_sha256": sha256(path),
        "generated_image_sha256": hashes["generated_image_sha256"],
        "twin_image_sha256": hashes["twin_image_sha256"],
        "scene_prompt_sha256": hashes["scene_prompt_sha256"],
    }


def validate_two_pass_result(
    record: Mapping[str, Any], path: Path, policy: Mapping[str, Any]
) -> tuple[Mapping[str, Any], Mapping[str, Any], dict[str, Any], dict[str, Any]]:
    record_id = str(record["id"])
    result = load_json(path)
    require(isinstance(result, Mapping), f"{record_id}: two-pass result is not an object")
    require(result.get("schema_version") == "placement-two-pass-result-v1", f"{record_id}: two-pass schema differs")
    require(result.get("origin") == "application_derived_deterministic_merge", f"{record_id}: two-pass origin differs")
    require(result.get("record_id") == record_id, f"{record_id}: embedded record ID differs")
    require(result.get("policy_version") == policy.get("policy_version"), f"{record_id}: two-pass policy version differs")
    require(result.get("policy_sha256") == sha256(TWO_PASS_POLICY), f"{record_id}: two-pass policy hash differs")
    require(result.get("combiner_sha256") == sha256(TWO_PASS_COMBINER), f"{record_id}: combiner hash differs")
    expected_identity = expected_input_identity(record)
    require(result.get("input_identity") == expected_identity, f"{record_id}: combined input identity differs")
    exclusion = result.get("comment_input_exclusion")
    require(isinstance(exclusion, Mapping), f"{record_id}: comment exclusion audit missing")
    require(exclusion.get("canonical_runtime_input_keys") == sorted(RUNTIME_KEYS), f"{record_id}: input whitelist audit differs")
    require(exclusion.get("source_annotations_passed_to_either_model") is False, f"{record_id}: source annotations entered model input")

    stages = result.get("stages")
    require(isinstance(stages, Mapping) and set(stages) == {"baseline_v2", "compact_v3"}, f"{record_id}: stage set differs")
    stage_audit = {
        role: validate_two_pass_stage(
            record=record,
            role=role,
            stage=stages[role],
            expected_identity=expected_identity,
            policy=policy,
            combined_case_dir=path.parent,
        )
        for role in ("baseline_v2", "compact_v3")
    }
    combiner = load_two_pass_combiner()
    recomputed_observation, recomputed_provenance = combiner.merge_observations(
        stage_audit["baseline_v2"]["judgment"]["observation"],
        stage_audit["compact_v3"]["judgment"]["observation"],
        baseline_verdict=stage_audit["baseline_v2"]["judgment"]["verdict"],
        compact_verdict=stage_audit["compact_v3"]["judgment"]["verdict"],
    )
    require(result.get("combined_observation") == recomputed_observation, f"{record_id}: combined observation is not deterministic")
    require(result.get("component_provenance") == recomputed_provenance, f"{record_id}: component provenance is not deterministic")
    recomputed_judgment = combiner.SCORING.aggregate_observation(recomputed_observation)
    require(result.get("combined_judgment") == recomputed_judgment, f"{record_id}: combined judgment is not deterministically scored")
    judgment = result["combined_judgment"]
    require(judgment.get("verdict") in {"pass", "review", "fail"}, f"{record_id}: combined verdict invalid")
    score = judgment.get("natural_placement_score")
    require(isinstance(score, (int, float)) and not isinstance(score, bool), f"{record_id}: combined score missing")
    require(0 <= float(score) <= 100, f"{record_id}: combined score outside 0..100")
    summary = judgment.get("observation", {}).get("summary")
    require(isinstance(summary, str) and summary.strip(), f"{record_id}: combined explanation missing")
    require(
        not summary.startswith("Application-derived deterministic two-pass merge;"),
        f"{record_id}: combined explanation is provenance code rather than a written assessment",
    )
    presentation = {
        "origin": result["origin"],
        "policy_version": result["policy_version"],
        "component_provenance": recomputed_provenance,
        "stages": {
            role: {"judgment": stage_audit[role]["judgment"]}
            for role in ("baseline_v2", "compact_v3")
        },
    }
    return result, judgment, {
        "result_path": str(path),
        "result_sha256": sha256(path),
        "input_identity": expected_identity,
        "policy_sha256": sha256(TWO_PASS_POLICY),
        "combiner_sha256": sha256(TWO_PASS_COMBINER),
        "both_stage_protocols_verified": True,
        "all_stage_source_artifact_hashes_verified": True,
        "preserved_raw_response_bytes_verified": True,
        "deterministic_merge_recomputed": True,
        "deterministic_v3_score_recomputed": True,
        "stages": stage_audit,
    }, presentation


def validate_two_pass_summary(
    results_dir: Path,
    manifest_path: Path,
    record_ids: Sequence[str],
    paths: Mapping[str, Path],
) -> tuple[dict[str, Any], Mapping[str, Any]]:
    summary_path = results_dir / "summary.json"
    payload = load_json(summary_path)
    require(isinstance(payload, Mapping), "two-pass run summary must be an object")
    require(payload.get("schema_version") == "placement-two-pass-run-v1", "two-pass run summary schema differs")
    require(payload.get("policy_version") == load_json(TWO_PASS_POLICY).get("policy_version"), "two-pass run policy differs")
    require(Path(str(payload.get("manifest", ""))).resolve() == manifest_path, "two-pass run manifest path differs")
    require(payload.get("manifest_sha256") == sha256(manifest_path), "two-pass run manifest hash differs")
    require(payload.get("record_count") == len(record_ids), "two-pass run count differs")
    items = payload.get("items")
    require(isinstance(items, list), "two-pass run items missing")
    require([item.get("id") for item in items if isinstance(item, Mapping)] == list(record_ids), "two-pass run IDs/order differ")
    require(set(paths) == set(record_ids), "two-pass result IDs differ from manifest")
    return {
        "path": str(summary_path.resolve()),
        "sha256": sha256(summary_path),
        "status": "complete",
    }, payload


def validate_hash_reference(reference: Any, label: str) -> tuple[Path, Any]:
    require(isinstance(reference, Mapping), f"{label}: reference missing")
    path = Path(str(reference.get("path", ""))).resolve()
    require(path.is_file(), f"{label}: referenced file missing")
    require(reference.get("sha256") == sha256(path), f"{label}: referenced hash differs")
    return path, load_json(path)


def validate_verifier_overlay(
    *,
    record: Mapping[str, Any],
    overlay: Any,
    source_path: Path,
    source_hash: str,
    merger: Any,
) -> tuple[dict[str, Mapping[str, Any]], dict[str, Any]]:
    record_id = str(record["id"])
    if overlay is None:
        return {}, {"present": False}
    require(isinstance(overlay, Mapping), f"{record_id}: verifier overlay invalid")
    result_path = Path(str(overlay.get("result_path", ""))).resolve()
    raw_path = Path(str(overlay.get("raw_response_path", ""))).resolve()
    require(result_path.is_file(), f"{record_id}: verifier result missing")
    require(raw_path.is_file(), f"{record_id}: verifier raw response missing")
    require(overlay.get("result_sha256") == sha256(result_path), f"{record_id}: verifier result hash differs")
    require(overlay.get("raw_response_sha256") == sha256(raw_path), f"{record_id}: verifier raw hash differs")
    verifier = load_json(result_path)
    raw_response = load_json(raw_path)
    require(overlay.get("result") == verifier, f"{record_id}: embedded verifier result differs")
    require(isinstance(verifier, Mapping) and verifier.get("ok") is True, f"{record_id}: verifier result failed")
    require(verifier.get("record_id") == record_id, f"{record_id}: verifier record ID differs")
    require(verifier.get("runtime_input") == expected_runtime_input(record), f"{record_id}: verifier runtime input differs")
    require(verifier.get("comments_or_expectations_passed") is False, f"{record_id}: feedback entered verifier input")
    require(verifier.get("model_requested") == "gpt-5.5", f"{record_id}: verifier requested model differs")
    require(verifier.get("reasoning_effort") == "high", f"{record_id}: verifier reasoning differs")
    returned = verifier.get("model_returned")
    require(
        isinstance(returned, str) and re.fullmatch(r"gpt-5\.5(?:-\d{4}-\d{2}-\d{2})?", returned) is not None,
        f"{record_id}: verifier returned model differs",
    )
    images = verifier.get("images")
    identity = expected_input_identity(record)
    require(isinstance(images, Mapping), f"{record_id}: verifier image audit missing")
    require(images.get("generated_image", {}).get("sha256") == identity["generated_image_sha256"], f"{record_id}: verifier generated image hash differs")
    require(images.get("twin_image", {}).get("sha256") == identity["twin_image_sha256"], f"{record_id}: verifier twin image hash differs")

    expected_freeze_hash = verifier.get("protocol_freeze_sha256")
    verify_run_root = result_path.parents[3]
    freeze_candidates = [
        verify_run_root / "freeze.json",
        VERIFY_PROTOCOL_SNAPSHOT / "freeze.json",
    ]
    matching_freezes = [
        candidate for candidate in freeze_candidates
        if candidate.is_file() and sha256(candidate) == expected_freeze_hash
    ]
    require(len({str(path.resolve()) for path in matching_freezes}) >= 1, f"{record_id}: verifier freeze source not found")
    frozen_path = matching_freezes[0]
    frozen = load_json(frozen_path)
    require(verifier.get("protocol_freeze") == frozen, f"{record_id}: embedded verifier freeze differs")
    require(frozen.get("protocol_version") == verifier.get("protocol_version"), f"{record_id}: verifier protocol version differs")
    require(frozen.get("model") == "gpt-5.5" and frozen.get("reasoning_effort") == "high", f"{record_id}: frozen verifier model contract differs")
    hashes = frozen.get("hashes")
    require(isinstance(hashes, Mapping), f"{record_id}: verifier frozen hashes missing")
    runner_candidates = [
        verify_run_root / "run_verifier.py",
        VERIFY_PROTOCOL_SNAPSHOT / "run_verifier.py",
    ]
    matching_runners = [
        candidate for candidate in runner_candidates
        if candidate.is_file() and sha256(candidate) == hashes.get("runner_sha256")
    ]
    require(bool(matching_runners), f"{record_id}: verifier runner source not found")
    runner_snapshot = matching_runners[0]
    for key, file_path in (
        ("system_prompt_sha256", verify_run_root / "system_prompt.md"),
        ("v3_schema_sha256", ROOT / "observation_schema.json"),
        ("v3_scoring_sha256", ROOT / "scoring.py"),
        ("v3_runner_sha256", ROOT / "run_judge.py"),
        ("trigger_manifest_sha256", verify_run_root / "triggers.json"),
    ):
        require(hashes.get(key) == sha256(file_path), f"{record_id}: verifier {key} source differs")
    require(verifier.get("system_prompt_sha256") == hashes.get("system_prompt_sha256"), f"{record_id}: verifier prompt hash differs")

    proposed = verifier.get("proposed_components")
    names = verifier.get("proposed_component_names")
    assessment = verifier.get("assessment")
    require(isinstance(proposed, Mapping) and isinstance(names, list), f"{record_id}: verifier proposal missing")
    require(names == list(proposed), f"{record_id}: verifier proposed component order differs")
    require(verifier.get("proposal_sha256") == json_sha256(proposed), f"{record_id}: verifier proposal hash differs")
    merger.validate_response(assessment, merger.response_schema(names), names)
    require(raw_observation(raw_response, record_id, "verifier") == assessment, f"{record_id}: verifier raw response differs")

    source = verifier.get("source_provenance")
    require(isinstance(source, Mapping), f"{record_id}: verifier source provenance missing")
    require(Path(str(source.get("combined_result_path", ""))).resolve() == source_path, f"{record_id}: verifier combined source path differs")
    require(source.get("combined_result_sha256") == source_hash, f"{record_id}: verifier combined source hash differs")
    for key in ("compact_raw_response", "compact_result", "baseline_raw_response", "baseline_result"):
        validate_hash_reference(source.get(key), f"{record_id} verifier {key}")
    return dict(assessment["components"]), {
        "present": True,
        "result_path": str(result_path),
        "result_sha256": sha256(result_path),
        "raw_response_path": str(raw_path),
        "raw_response_sha256": sha256(raw_path),
        "protocol_freeze_path": str(frozen_path.resolve()),
        "protocol_freeze_sha256": sha256(frozen_path),
        "runner_snapshot_sha256": sha256(runner_snapshot),
        "selected_protocol": frozen.get("selected_protocol"),
        "proposed_component_names": names,
    }


def validate_verified_result(
    record: Mapping[str, Any],
    path: Path,
    policy: Mapping[str, Any],
    expected_merge_sha256: str | None = None,
    expected_development_status: str = "posthoc_policy_revision_not_untouched_validation",
) -> tuple[Mapping[str, Any], Mapping[str, Any], dict[str, Any], dict[str, Any]]:
    record_id = str(record["id"])
    envelope = load_json(path)
    require(isinstance(envelope, Mapping), f"{record_id}: verified envelope invalid")
    require(envelope.get("schema_version") == "placement-verified-additions-envelope-v2", f"{record_id}: verified schema differs")
    require(envelope.get("policy_version") == "placement-verified-additions-decision-v2", f"{record_id}: verified policy differs")
    require(envelope.get("development_status") == expected_development_status, f"{record_id}: verified development status differs")
    require(envelope.get("origin") == "application_derived_verified_overlay", f"{record_id}: verified origin differs")
    require(envelope.get("record_id") == record_id, f"{record_id}: verified record ID differs")
    require(envelope.get("suggested_scene_changes") == [], f"{record_id}: verified top-level suggestions differ")
    merge_reference = envelope.get("merge_generator")
    if merge_reference is None:
        merge_path = VERIFY_MERGER_V2.resolve()
        merge_hash = sha256(merge_path)
    else:
        require(isinstance(merge_reference, Mapping), f"{record_id}: merge generator reference invalid")
        merge_path = Path(str(merge_reference.get("path", ""))).resolve()
        require(merge_path.is_file(), f"{record_id}: merge generator source missing")
        merge_hash = sha256(merge_path)
        require(merge_reference.get("sha256") == merge_hash, f"{record_id}: merge generator hash differs")
    if expected_merge_sha256 is not None:
        require(merge_hash == expected_merge_sha256, f"{record_id}: merge generator differs from selected protocol snapshot")
    merger = load_verified_merger(merge_path)

    source = envelope.get("source_two_pass")
    require(isinstance(source, Mapping), f"{record_id}: source two-pass envelope missing")
    source_path = Path(str(source.get("path", ""))).resolve()
    require(source_path.is_file(), f"{record_id}: source two-pass result missing")
    source_hash = sha256(source_path)
    require(source.get("sha256") == source_hash, f"{record_id}: source two-pass hash differs")
    source_result = load_json(source_path)
    require(source.get("result") == source_result, f"{record_id}: embedded two-pass result differs")
    _, _, source_audit, source_presentation = validate_two_pass_result(
        record, source_path, policy
    )
    stages = source_result["stages"]
    baseline = stages["baseline_v2"]["judgment"]
    compact_original = stages["compact_v3"]["judgment"]
    verifier_components, overlay_audit = validate_verifier_overlay(
        record=record,
        overlay=envelope.get("verifier_overlay"),
        source_path=source_path,
        source_hash=source_hash,
        merger=merger,
    )
    compact_observation = copy.deepcopy(compact_original["observation"])
    for name, component in verifier_components.items():
        require(name in COMPONENTS, f"{record_id}: verifier proposed unknown component")
        compact_observation["components"][name] = copy.deepcopy(component)
    combiner = load_two_pass_combiner()
    verified_compact = combiner.SCORING.aggregate_observation(compact_observation)
    require(envelope.get("verified_compact_judgment") == verified_compact, f"{record_id}: verified compact judgment is not deterministic")
    merged_observation, provenance = combiner.merge_observations(
        baseline["observation"],
        compact_observation,
        baseline_verdict=baseline["verdict"],
        compact_verdict=verified_compact["verdict"],
    )
    require(envelope.get("verified_component_provenance") == provenance, f"{record_id}: verified component provenance is not deterministic")
    merged = combiner.SCORING.aggregate_observation(merged_observation)
    require(envelope.get("application_merged_judgment") == merged, f"{record_id}: verified merged judgment is not deterministic")
    final_decision = merger.final_policy(baseline["verdict"], merged, verifier_components)
    require(envelope.get("final_decision") == final_decision, f"{record_id}: final override policy is not deterministic")
    require(final_decision["verdict"] in {"pass", "review", "fail"}, f"{record_id}: final verdict invalid")
    require(final_decision["reported_overall_confidence"] in {"low", "medium", "high"}, f"{record_id}: final confidence invalid")

    display_judgment = copy.deepcopy(merged)
    display_judgment["verdict"] = final_decision["verdict"]
    display_judgment["verdict_reasons"] = final_decision["verdict_reasons"]
    display_judgment["confidence"] = final_decision["reported_overall_confidence"]
    presentation = dict(source_presentation)
    presentation.update({
        "verified_envelope": True,
        "verifier_components": verifier_components,
        "verified_compact_judgment": verified_compact,
        "verified_component_provenance": provenance,
        "application_merged_judgment": merged,
        "final_decision": final_decision,
    })
    return envelope, display_judgment, {
        "result_path": str(path),
        "result_sha256": sha256(path),
        "source_two_pass": source_audit,
        "verifier_overlay": overlay_audit,
        "verified_compact_recomputed": True,
        "verified_merge_and_score_recomputed": True,
        "final_override_recomputed": True,
        "verified_merger_path": str(merge_path),
        "verified_merger_sha256": merge_hash,
    }, presentation


def validate_verified_summary(
    results_dir: Path,
    manifest_path: Path,
    record_ids: Sequence[str],
    paths: Mapping[str, Path],
    expected_development_status: str = "posthoc_policy_revision_not_untouched_validation",
) -> tuple[dict[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    summary_path = results_dir / "summary.json"
    audit_path = results_dir / "audit.json"
    summary = load_json(summary_path)
    audit = load_json(audit_path)
    require(isinstance(summary, Mapping), "verified summary invalid")
    require(summary.get("schema_version") == "placement-verified-additions-run-v2", "verified summary schema differs")
    require(summary.get("policy_version") == "placement-verified-additions-decision-v2", "verified summary policy differs")
    require(summary.get("development_status") == expected_development_status, "verified summary development status differs")
    require(summary.get("record_count") == len(record_ids), "verified summary count differs")
    records = summary.get("records")
    require(isinstance(records, list) and all(isinstance(item, Mapping) for item in records), "verified summary records invalid")
    summary_ids = [item.get("id") for item in records]
    require(len(summary_ids) == len(set(summary_ids)) and set(summary_ids) == set(record_ids), "verified summary IDs differ")
    require(set(paths) == set(record_ids), "verified result IDs differ from manifest")
    require(isinstance(audit, Mapping), "verified audit invalid")
    if audit.get("schema_version") == "placement-verified-additions-audit-v2":
        require(audit.get("policy_version") == summary.get("policy_version"), "verified audit policy differs")
        require(audit.get("development_status") == summary.get("development_status"), "verified audit development status differs")
        coverage = audit.get("source_hash_coverage")
        expected = audit.get("expected_coverage")
        require(isinstance(coverage, Mapping) and isinstance(expected, Mapping), "verified audit coverage missing")
        require(coverage == expected, "verified audit source hash coverage incomplete")
        require(coverage.get("source_results") == len(record_ids), "verified audit source result count differs")
    elif audit.get("schema_version") == "placement-verified-additions-new160-audit-v1":
        coverage = audit.get("coverage_validated")
        require(isinstance(coverage, Mapping), "NEW160 verified audit coverage missing")
        for key in ("manifest_records", "baseline_results", "compact_results", "two_pass_results", "verified_results"):
            require(coverage.get(key) == len(record_ids), f"NEW160 verified audit {key} count differs")
        require(coverage.get("missing_records") == 0, "NEW160 verified audit has missing records")
        require(coverage.get("verifier_overlays") == coverage.get("trigger_cases"), "NEW160 verifier trigger coverage differs")
        require(coverage.get("verified_overlay_components") == coverage.get("trigger_components"), "NEW160 verifier component coverage differs")
        manifest_ref = audit.get("manifest")
        require(isinstance(manifest_ref, Mapping), "NEW160 audit manifest missing")
        require(Path(str(manifest_ref.get("path", ""))).resolve() == manifest_path, "NEW160 audit manifest path differs")
        require(manifest_ref.get("sha256") == sha256(manifest_path), "NEW160 audit manifest hash differs")
        verified_ref = audit.get("runs", {}).get("verified")
        require(isinstance(verified_ref, Mapping), "NEW160 audit verified run missing")
        require(Path(str(verified_ref.get("path", ""))).resolve() == results_dir, "NEW160 audit verified run path differs")
        require(verified_ref.get("summary_sha256") == sha256(summary_path), "NEW160 audit summary hash differs")
    else:
        raise ValueError("verified audit schema differs")
    return {
        "path": str(summary_path.resolve()),
        "sha256": sha256(summary_path),
        "audit_path": str(audit_path.resolve()),
        "audit_sha256": sha256(audit_path),
        "status": "complete",
    }, summary, audit


def verified_protocol_context(
    protocol: Mapping[str, Any], protocol_path: Path, manifest_path: Path
) -> tuple[Mapping[str, Any], str | None, dict[str, Any]]:
    if protocol.get("schema_version") == "placement-two-pass-policy-v1":
        require(protocol == load_json(TWO_PASS_POLICY), "verified legacy policy differs from current two-pass policy")
        return protocol, None, {"mode": "legacy_two_pass_policy"}
    require(
        protocol.get("schema_version") == "placement-new160-selected-protocol-snapshot-v1",
        "verified protocol metadata is not a selected protocol snapshot",
    )
    files = protocol.get("files")
    require(isinstance(files, Mapping), "selected protocol snapshot files missing")
    verified_files: dict[str, Any] = {}
    for name, reference in files.items():
        require(isinstance(reference, Mapping), f"selected protocol {name}: reference invalid")
        expected = reference.get("sha256")
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected) is not None, f"selected protocol {name}: hash invalid")
        original = Path(str(reference.get("original_path", ""))).resolve()
        snapshot = Path(str(reference.get("snapshot_path", ""))).resolve()
        require(original.is_file() and snapshot.is_file(), f"selected protocol {name}: source or snapshot missing")
        require(sha256(original) == expected == sha256(snapshot), f"selected protocol {name}: source/snapshot hash differs")
        verified_files[str(name)] = {
            "original_path": str(original),
            "snapshot_path": str(snapshot),
            "sha256": expected,
        }
    require("two_pass_policy" in verified_files and "verified_merge_v2" in verified_files, "selected protocol lacks core policies")
    selected_protocol_path = Path(str(protocol.get("selected_protocol_path", ""))).resolve()
    require(selected_protocol_path.is_file(), "selected protocol freeze missing")
    require(
        protocol.get("selected_protocol_sha256") == sha256(selected_protocol_path),
        "selected protocol freeze hash differs",
    )
    selected_protocol = load_json(selected_protocol_path)
    require(
        selected_protocol.get("schema_version") == "placement-new160-selected-protocol-freeze-v1",
        "selected protocol freeze schema differs",
    )
    selected_files = selected_protocol.get("files")
    require(isinstance(selected_files, Mapping), "selected protocol freeze files missing")
    for name, value in verified_files.items():
        selected = selected_files.get(name)
        require(isinstance(selected, Mapping), f"selected protocol freeze lacks {name}")
        require(selected.get("sha256") == value["sha256"], f"selected protocol freeze {name} hash differs")
    require(
        verified_files.get("new160_manifest", {}).get("sha256") == sha256(manifest_path),
        "selected protocol manifest differs from report manifest",
    )
    two_pass_policy = load_json(Path(verified_files["two_pass_policy"]["snapshot_path"]))
    require(two_pass_policy == load_json(TWO_PASS_POLICY), "selected two-pass policy differs")
    return (
        two_pass_policy,
        verified_files["verified_merge_v2"]["sha256"],
        {
            "mode": "selected_new160_protocol_snapshot",
            "snapshot_manifest": str(protocol_path),
            "snapshot_manifest_sha256": sha256(protocol_path),
            "selected_protocol_path": str(selected_protocol_path),
            "selected_protocol_sha256": sha256(selected_protocol_path),
            "development_status": selected_protocol.get("development_status"),
            "verified_files": verified_files,
        },
    )


def consensus_protocol_context(
    protocol: Mapping[str, Any], protocol_path: Path
) -> tuple[Mapping[str, Any], Path, dict[str, Any]]:
    snapshot_schema = protocol.get("schema_version")
    require(
        snapshot_schema in {
            "placement-consensus-additions-protocol-snapshot-v1",
            "placement-consensus-additions-protocol-snapshot-v2",
        },
        "consensus protocol metadata is not an immutable snapshot manifest",
    )
    files = protocol.get("files")
    require(isinstance(files, Mapping), "consensus protocol snapshot files missing")
    generator_name = (
        "merge_consensus_v2.py"
        if snapshot_schema == "placement-consensus-additions-protocol-snapshot-v2"
        else "merge_consensus.py"
    )
    evaluator_name = (
        "evaluate_consensus_v2.py"
        if snapshot_schema == "placement-consensus-additions-protocol-snapshot-v2"
        else "evaluate_consensus.py"
    )
    expected_files = {"policy.json", generator_name, "test_consensus.py", evaluator_name}
    if snapshot_schema == "placement-consensus-additions-protocol-snapshot-v2":
        expected_files.add("test_consensus_v2.py")
        require(protocol.get("validator_change_only") is True, "consensus v2 is not marked validator-only")
        require(protocol.get("semantic_policy_version") == "placement-consensus-additions-decision-v1", "consensus v2 semantic policy differs")
    require(set(files) == expected_files, "consensus protocol snapshot file set differs")
    verified_files: dict[str, Any] = {}
    for name, reference in files.items():
        require(isinstance(reference, Mapping), f"consensus snapshot {name}: invalid reference")
        expected = reference.get("sha256")
        require(
            isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
            f"consensus snapshot {name}: invalid hash",
        )
        source = Path(str(reference.get("source_path", ""))).resolve()
        snapshot = Path(str(reference.get("snapshot_path", ""))).resolve()
        require(source.is_file() and snapshot.is_file(), f"consensus snapshot {name}: file missing")
        require(sha256(source) == expected == sha256(snapshot), f"consensus snapshot {name}: bytes differ")
        verified_files[str(name)] = {
            "source_path": str(source),
            "snapshot_path": str(snapshot),
            "sha256": expected,
        }
    inputs = protocol.get("input_summaries_and_triggers")
    require(isinstance(inputs, Mapping), "consensus snapshot input references missing")
    verified_inputs: dict[str, Any] = {}
    for name, reference in inputs.items():
        path, _ = validate_hash_reference(reference, f"consensus snapshot input {name}")
        verified_inputs[str(name)] = {"path": str(path), "sha256": sha256(path)}
    policy_path = Path(verified_files["policy.json"]["snapshot_path"])
    policy = load_json(policy_path)
    require(
        policy.get("schema_version") == "placement-consensus-additions-policy-v1",
        "consensus policy schema differs",
    )
    require(
        policy.get("policy_version") == "placement-consensus-additions-decision-v1",
        "consensus policy version differs",
    )
    require(
        protocol.get("development_status") == policy.get("development_status"),
        "consensus development status differs",
    )
    # The frozen copy is byte-identical, while the generator derives repository-relative
    # imports from its own location. Execute the hash-bound source path so those imports
    # still resolve; the snapshot above proves the bytes are frozen.
    generator_path = Path(verified_files[generator_name]["source_path"])
    return policy, generator_path, {
        "mode": "immutable_consensus_protocol_snapshot",
        "snapshot_manifest": str(protocol_path),
        "snapshot_manifest_sha256": sha256(protocol_path),
        "development_status": protocol.get("development_status"),
        "files": verified_files,
        "inputs": verified_inputs,
        "generator_name": generator_name,
        "evaluator_name": evaluator_name,
    }


def validate_names_only_overlay(
    *,
    record: Mapping[str, Any],
    overlay: Any,
    requested_names: list[str],
    trigger_path: Path,
    trigger_hash: str,
) -> tuple[dict[str, Mapping[str, Any]], dict[str, Any]]:
    record_id = str(record["id"])
    require(isinstance(overlay, Mapping), f"{record_id}: names-only overlay missing")
    result_path, saved = validate_hash_reference(
        overlay.get("result"), f"{record_id} names-only result"
    )
    raw_path, raw_response = validate_hash_reference(
        overlay.get("raw_response"), f"{record_id} names-only raw response"
    )
    require(overlay.get("assessment") == saved, f"{record_id}: embedded names-only result differs")
    require(isinstance(saved, Mapping) and saved.get("ok") is True, f"{record_id}: names-only result failed")
    require(saved.get("record_id") == record_id, f"{record_id}: names-only record ID differs")
    require(saved.get("runtime_input") == expected_runtime_input(record), f"{record_id}: names-only runtime input differs")
    require(set(saved["runtime_input"]) == RUNTIME_KEYS, f"{record_id}: names-only input whitelist differs")
    require(saved.get("requested_component_names") == requested_names, f"{record_id}: names-only component names differ")
    require(saved.get("proposal_text_codes_severities_prior_verdicts_comments_passed") is False, f"{record_id}: proposal or feedback entered names-only input")
    require(saved.get("model_requested") == "gpt-5.5", f"{record_id}: names-only requested model differs")
    require(saved.get("reasoning_effort") == "high", f"{record_id}: names-only reasoning differs")
    returned = saved.get("model_returned")
    require(
        isinstance(returned, str) and re.fullmatch(r"gpt-5\.5(?:-\d{4}-\d{2}-\d{2})?", returned) is not None,
        f"{record_id}: names-only returned model differs",
    )
    sent = saved.get("sent_metadata")
    runtime = expected_runtime_input(record)
    require(
        sent
        == {
            "product_type": runtime["product_type"],
            "image_stage": runtime["image_stage"],
            "scene_prompt": runtime["scene_prompt"],
            "requested_component_names": requested_names,
        },
        f"{record_id}: names-only sent metadata differs",
    )
    images = saved.get("images")
    identity = expected_input_identity(record)
    require(isinstance(images, Mapping), f"{record_id}: names-only image audit missing")
    for name, identity_key in (
        ("generated_image", "generated_image_sha256"),
        ("twin_image", "twin_image_sha256"),
    ):
        reference = images.get(name)
        require(isinstance(reference, Mapping), f"{record_id}: names-only {name} reference missing")
        image_path = Path(str(reference.get("path", ""))).resolve()
        require(image_path == Path(runtime[name]), f"{record_id}: names-only {name} path differs")
        require(reference.get("sha256") == identity[identity_key] == sha256(image_path), f"{record_id}: names-only {name} hash differs")
    source_trigger = saved.get("source_trigger")
    require(isinstance(source_trigger, Mapping), f"{record_id}: names-only source trigger missing")
    require(Path(str(source_trigger.get("path", ""))).resolve() == trigger_path, f"{record_id}: names-only trigger path differs")
    require(source_trigger.get("sha256") == trigger_hash, f"{record_id}: names-only trigger hash differs")

    freeze_path = INDEPENDENT_CHECK_ROOT / "freeze.json"
    freeze = load_json(freeze_path)
    require(saved.get("protocol_freeze_sha256") == sha256(freeze_path), f"{record_id}: names-only freeze hash differs")
    require(saved.get("protocol_freeze") == freeze, f"{record_id}: embedded names-only freeze differs")
    require(freeze.get("protocol_version") == saved.get("protocol_version"), f"{record_id}: names-only protocol differs")
    hashes = freeze.get("hashes")
    require(isinstance(hashes, Mapping), f"{record_id}: names-only frozen hashes missing")
    for key, source_path in (
        ("runner_sha256", INDEPENDENT_CHECK_ROOT / "run_check.py"),
        ("batch_sha256", INDEPENDENT_CHECK_ROOT / "run_batch.py"),
        ("manifest_sha256", INDEPENDENT_CHECK_ROOT / "input_manifest.json"),
        ("system_prompt_sha256", INDEPENDENT_CHECK_ROOT / "system_prompt.md"),
        ("v3_schema_sha256", ROOT / "observation_schema.json"),
        ("v3_scoring_sha256", ROOT / "scoring.py"),
        ("v3_runner_sha256", ROOT / "run_judge.py"),
    ):
        require(hashes.get(key) == sha256(source_path), f"{record_id}: names-only {key} differs")
    require(saved.get("system_prompt_sha256") == hashes.get("system_prompt_sha256"), f"{record_id}: names-only prompt hash differs")
    runner = load_independent_check_runner()
    schema = runner.response_schema(requested_names)
    require(saved.get("response_schema_sha256") == json_sha256(schema), f"{record_id}: names-only response schema hash differs")
    assessment = saved.get("assessment")
    runner.validate_response(assessment, schema, requested_names)
    require(raw_observation(raw_response, record_id, "names-only verifier") == assessment, f"{record_id}: names-only raw response differs")
    return dict(assessment["components"]), {
        "present": True,
        "result_path": str(result_path),
        "result_sha256": sha256(result_path),
        "raw_response_path": str(raw_path),
        "raw_response_sha256": sha256(raw_path),
        "protocol_freeze_path": str(freeze_path.resolve()),
        "protocol_freeze_sha256": sha256(freeze_path),
        "requested_component_names": requested_names,
    }


def validate_consensus_result(
    record: Mapping[str, Any],
    path: Path,
    two_pass_policy: Mapping[str, Any],
    consensus_policy: Mapping[str, Any],
    generator_path: Path,
    trigger_path: Path,
    trigger_hash: str,
    trigger_map: Mapping[str, list[str]],
) -> tuple[Mapping[str, Any], Mapping[str, Any], dict[str, Any], dict[str, Any]]:
    record_id = str(record["id"])
    envelope = load_json(path)
    require(isinstance(envelope, Mapping), f"{record_id}: consensus envelope invalid")
    envelope_schema = envelope.get("schema_version")
    require(
        envelope_schema in {
            "placement-consensus-additions-envelope-v1",
            "placement-consensus-additions-envelope-v2",
        },
        f"{record_id}: consensus schema differs",
    )
    require(envelope.get("policy_version") == consensus_policy.get("policy_version"), f"{record_id}: consensus policy differs")
    require(envelope.get("development_status") == consensus_policy.get("development_status"), f"{record_id}: consensus development status differs")
    require(envelope.get("record_id") == record_id, f"{record_id}: consensus record ID differs")
    require(envelope.get("suggested_scene_changes") == [], f"{record_id}: consensus top-level suggestions differ")
    for field, expected_path in (("policy", Path(CONSENSUS_ROOT / "policy.json")), ("merge_generator", generator_path)):
        reference = envelope.get(field)
        require(isinstance(reference, Mapping), f"{record_id}: consensus {field} reference missing")
        actual_path = Path(str(reference.get("path", ""))).resolve()
        require(actual_path == expected_path.resolve(), f"{record_id}: consensus {field} path differs")
        require(reference.get("sha256") == sha256(actual_path), f"{record_id}: consensus {field} hash differs")
    require(envelope["merge_generator"]["sha256"] == sha256(generator_path), f"{record_id}: consensus generator differs from frozen snapshot")

    source = envelope.get("source_two_pass")
    require(isinstance(source, Mapping), f"{record_id}: consensus source two-pass missing")
    source_path = Path(str(source.get("path", ""))).resolve()
    require(source_path.is_file(), f"{record_id}: consensus source result missing")
    source_hash = sha256(source_path)
    require(source.get("sha256") == source_hash, f"{record_id}: consensus source hash differs")
    source_result = load_json(source_path)
    require(source.get("result") == source_result, f"{record_id}: embedded consensus source differs")
    _, _, source_audit, source_presentation = validate_two_pass_result(record, source_path, two_pass_policy)
    baseline = source_result["stages"]["baseline_v2"]["judgment"]
    compact_original = source_result["stages"]["compact_v3"]["judgment"]
    require(envelope.get("original_compact_judgment") == compact_original, f"{record_id}: original compact judgment differs")

    trigger = envelope.get("trigger_manifest")
    require(isinstance(trigger, Mapping), f"{record_id}: consensus trigger reference missing")
    require(Path(str(trigger.get("path", ""))).resolve() == trigger_path, f"{record_id}: consensus trigger path differs")
    require(trigger.get("sha256") == trigger_hash, f"{record_id}: consensus trigger hash differs")
    requested = list(trigger_map.get(record_id, []))
    require(trigger.get("requested_components") == requested, f"{record_id}: consensus requested components differ")

    generator = load_consensus_generator(generator_path)
    proposal_components: dict[str, Mapping[str, Any]] = {}
    names_components: dict[str, Mapping[str, Any]] = {}
    proposal_audit: dict[str, Any] = {"present": False}
    names_audit: dict[str, Any] = {"present": False}
    if requested:
        proposal = envelope.get("proposal_aware_overlay")
        require(isinstance(proposal, Mapping), f"{record_id}: proposal-aware overlay missing")
        normalized = {
            "result_path": proposal.get("result", {}).get("path"),
            "result_sha256": proposal.get("result", {}).get("sha256"),
            "raw_response_path": proposal.get("raw_response", {}).get("path"),
            "raw_response_sha256": proposal.get("raw_response", {}).get("sha256"),
            "result": proposal.get("assessment"),
        }
        proposal_components, proposal_audit = validate_verifier_overlay(
            record=record,
            overlay=normalized,
            source_path=source_path,
            source_hash=source_hash,
            merger=load_verified_merger(VERIFY_ROOT / "merge_verified_v2_new160.py"),
        )
        require(list(proposal_components) == requested, f"{record_id}: proposal-aware component order differs")
        names_components, names_audit = validate_names_only_overlay(
            record=record,
            overlay=envelope.get("names_only_overlay"),
            requested_names=requested,
            trigger_path=trigger_path,
            trigger_hash=trigger_hash,
        )
        expected_binding = generator.validate_independent_binding(
            record_id,
            envelope["names_only_overlay"]["assessment"],
            source_result,
            trigger_hash,
        )
        if envelope_schema == "placement-consensus-additions-envelope-v2":
            require(
                envelope.get("source_binding_validation") == expected_binding,
                f"{record_id}: consensus source binding is not deterministic",
            )
        else:
            require(envelope.get("source_binding_validation") is None, f"{record_id}: unexpected v1 source binding")
    else:
        require(envelope.get("proposal_aware_overlay") is None, f"{record_id}: unexpected proposal-aware overlay")
        require(envelope.get("names_only_overlay") is None, f"{record_id}: unexpected names-only overlay")
        require(envelope.get("source_binding_validation") is None, f"{record_id}: unexpected source binding")

    compact_observation = copy.deepcopy(compact_original["observation"])
    expected_resolutions: dict[str, Any] = {}
    for name in requested:
        selected, resolution = generator.resolve_component(
            name,
            proposal_components[name],
            names_components[name],
            baseline["observation"]["components"][name],
        )
        compact_observation["components"][name] = selected
        expected_resolutions[name] = resolution
    require(envelope.get("consensus_resolution") == expected_resolutions, f"{record_id}: consensus resolution is not deterministic")
    consensus_compact = generator.SCORING.aggregate_observation(compact_observation)
    require(envelope.get("consensus_compact_judgment") == consensus_compact, f"{record_id}: consensus compact judgment is not deterministic")
    merged_observation, provenance = generator.COMBINE.merge_observations(
        baseline["observation"],
        compact_observation,
        baseline_verdict=baseline["verdict"],
        compact_verdict=consensus_compact["verdict"],
    )
    require(envelope.get("component_provenance") == provenance, f"{record_id}: consensus provenance is not deterministic")
    merged = generator.SCORING.aggregate_observation(merged_observation)
    require(envelope.get("application_merged_judgment") == merged, f"{record_id}: consensus merged judgment is not deterministic")
    decision = generator.final_policy(baseline["verdict"], merged, expected_resolutions)
    require(envelope.get("final_decision") == decision, f"{record_id}: consensus final decision is not deterministic")
    require(decision["verdict"] in {"pass", "review", "fail"}, f"{record_id}: consensus verdict invalid")
    require(decision["reported_overall_confidence"] in {"low", "medium", "high"}, f"{record_id}: consensus confidence invalid")
    display = copy.deepcopy(merged)
    display["verdict"] = decision["verdict"]
    display["verdict_reasons"] = decision["verdict_reasons"]
    display["confidence"] = decision["reported_overall_confidence"]
    presentation = dict(source_presentation)
    presentation.update({
        "consensus_envelope": True,
        "proposal_aware_components": proposal_components,
        "names_only_components": names_components,
        "consensus_resolution": expected_resolutions,
        "consensus_compact_judgment": consensus_compact,
        "consensus_component_provenance": provenance,
        "application_merged_judgment": merged,
        "final_decision": decision,
    })
    return envelope, display, {
        "result_path": str(path),
        "result_sha256": sha256(path),
        "source_two_pass": source_audit,
        "proposal_aware_overlay": proposal_audit,
        "names_only_overlay": names_audit,
        "consensus_resolution_recomputed": True,
        "source_binding_validation_recomputed": envelope_schema == "placement-consensus-additions-envelope-v2",
        "consensus_merge_and_score_recomputed": True,
        "consensus_final_decision_recomputed": True,
        "consensus_generator_path": str(generator_path),
        "consensus_generator_sha256": sha256(generator_path),
    }, presentation


def validate_consensus_summary(
    results_dir: Path,
    record_ids: Sequence[str],
    paths: Mapping[str, Path],
    consensus_policy: Mapping[str, Any],
    generator_path: Path,
    trigger_path: Path,
    trigger_map: Mapping[str, list[str]],
) -> tuple[dict[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    summary_path = results_dir / "summary.json"
    audit_path = results_dir / "audit.json"
    summary = load_json(summary_path)
    audit = load_json(audit_path)
    require(isinstance(summary, Mapping), "consensus summary invalid")
    summary_schema = summary.get("schema_version")
    require(
        summary_schema in {
            "placement-consensus-additions-run-v1",
            "placement-consensus-additions-run-v2",
        },
        "consensus summary schema differs",
    )
    require(summary.get("policy_version") == consensus_policy.get("policy_version"), "consensus summary policy differs")
    require(summary.get("development_status") == consensus_policy.get("development_status"), "consensus summary development status differs")
    require(summary.get("record_count") == len(record_ids), "consensus summary count differs")
    records = summary.get("records")
    require(isinstance(records, list) and all(isinstance(item, Mapping) for item in records), "consensus summary records invalid")
    summary_ids = [item.get("id") for item in records]
    require(len(summary_ids) == len(set(summary_ids)) and set(summary_ids) == set(record_ids), "consensus summary IDs differ")
    require(set(paths) == set(record_ids), "consensus result IDs differ from manifest")
    for field, expected_path in (("policy", CONSENSUS_ROOT / "policy.json"), ("merge_generator", generator_path)):
        reference = summary.get(field)
        require(isinstance(reference, Mapping), f"consensus summary {field} missing")
        require(Path(str(reference.get("path", ""))).resolve() == expected_path.resolve(), f"consensus summary {field} path differs")
        require(reference.get("sha256") == sha256(expected_path), f"consensus summary {field} hash differs")
    require(summary["merge_generator"]["sha256"] == sha256(generator_path), "consensus summary generator differs from frozen snapshot")
    require(summary.get("trigger_case_count") == len(trigger_map), "consensus trigger case count differs")
    require(summary.get("trigger_component_count") == sum(len(v) for v in trigger_map.values()), "consensus trigger component count differs")
    expected_audit_schema = (
        "placement-consensus-additions-audit-v2"
        if summary_schema == "placement-consensus-additions-run-v2"
        else "placement-consensus-additions-audit-v1"
    )
    require(isinstance(audit, Mapping) and audit.get("schema_version") == expected_audit_schema, "consensus audit schema differs")
    run_ref = audit.get("run")
    require(isinstance(run_ref, Mapping), "consensus audit run reference missing")
    require(Path(str(run_ref.get("path", ""))).resolve() == results_dir, "consensus audit run path differs")
    require(run_ref.get("summary_sha256") == sha256(summary_path), "consensus audit summary hash differs")
    for field, expected_path in (("policy", CONSENSUS_ROOT / "policy.json"), ("merge_generator", generator_path), ("trigger_manifest", trigger_path)):
        reference = audit.get(field)
        require(isinstance(reference, Mapping), f"consensus audit {field} missing")
        require(Path(str(reference.get("path", ""))).resolve() == expected_path.resolve(), f"consensus audit {field} path differs")
        require(reference.get("sha256") == sha256(expected_path), f"consensus audit {field} hash differs")
    evaluator = audit.get("evaluator")
    evaluator_path = CONSENSUS_ROOT / (
        "evaluate_consensus_v2.py"
        if summary_schema == "placement-consensus-additions-run-v2"
        else "evaluate_consensus.py"
    )
    require(isinstance(evaluator, Mapping), "consensus audit evaluator missing")
    require(Path(str(evaluator.get("path", ""))).resolve() == evaluator_path.resolve(), "consensus audit evaluator path differs")
    require(evaluator.get("sha256") == sha256(evaluator_path), "consensus audit evaluator hash differs")
    coverage = audit.get("coverage")
    require(isinstance(coverage, Mapping), "consensus audit coverage missing")
    require(coverage.get("source_results") == len(record_ids), "consensus source coverage differs")
    require(coverage.get("trigger_cases") == len(trigger_map), "consensus audit trigger cases differ")
    require(coverage.get("trigger_components") == sum(len(v) for v in trigger_map.values()), "consensus audit trigger components differ")
    require(coverage.get("overlay_results") == 2 * len(trigger_map), "consensus overlay result coverage differs")
    require(coverage.get("overlay_raw_responses") == 2 * len(trigger_map), "consensus raw response coverage differs")
    require(coverage.get("missing") == 0, "consensus audit reports missing artifacts")
    if summary_schema == "placement-consensus-additions-run-v2":
        require(summary.get("source_binding_version") == "placement-consensus-source-binding-v2", "consensus v2 source binding version differs")
        semantic_identity = audit.get("consensus_v1_semantic_identity")
        require(isinstance(semantic_identity, Mapping), "consensus v2 semantic identity audit missing")
        require(semantic_identity.get("all_matched") is True, "consensus v2 changed v1 semantic decisions")
        require(semantic_identity.get("matched") == semantic_identity.get("count") == len(record_ids), "consensus v2 semantic identity coverage differs")
    return {
        "path": str(summary_path.resolve()),
        "sha256": sha256(summary_path),
        "audit_path": str(audit_path.resolve()),
        "audit_sha256": sha256(audit_path),
        "status": "complete",
    }, summary, audit


def component_scores(judgment: Mapping[str, Any]) -> str:
    values = judgment.get("component_scores")
    require(isinstance(values, Mapping), "judgment component_scores missing")
    return "; ".join(f"{name}={values.get(name)}" for name in COMPONENTS)


def evidence_text(judgment: Mapping[str, Any]) -> str:
    observation = judgment["observation"]
    lines = [
        "JUDGE ASSESSMENT",
        (
            f"Predicted verdict: {str(judgment['verdict']).upper()} · "
            f"Final score: {judgment['natural_placement_score']}/100 · "
            f"Confidence: {judgment.get('confidence', '')} · "
            f"Coverage: {judgment.get('coverage', '')}"
        ),
    ]
    summary = observation.get("summary")
    if isinstance(summary, str) and summary:
        lines.extend(("", "Summary", summary))
    lines.extend(("", "Component evidence"))
    for name in COMPONENTS:
        component = observation["components"][name]
        require(isinstance(component, Mapping), f"component {name} is invalid")
        lines.extend((
            "",
            name,
            f"visibility: {component.get('visibility', '')}",
            f"severity: {component.get('severity', '')}",
            f"confidence: {component.get('confidence', '')}",
            f"evidence: {component.get('evidence', '')}",
            f"consequence: {component.get('consequence', '')}",
            "issue_codes: " + json.dumps(component.get("issue_codes", []), ensure_ascii=False),
        ))
    changes = observation.get("suggested_scene_changes")
    if isinstance(changes, list) and changes:
        lines.extend(("", "Suggested scene changes"))
        lines.extend(f"- {value}" for value in changes)
    scene = observation.get("scene_reading")
    if isinstance(scene, Mapping):
        lines.extend(("", "Detailed scene reading"))
        lines.extend(f"{key}: {value}" for key, value in scene.items())
    reasons = judgment.get("verdict_reasons")
    if isinstance(reasons, list):
        lines.extend(("", "Verdict reasons: " + json.dumps(reasons)))
    return "\n".join(lines)


def two_pass_row_details(presentation: Mapping[str, Any]) -> dict[str, Any]:
    stages = presentation["stages"]
    baseline = stages["baseline_v2"]["judgment"]
    compact = stages["compact_v3"]["judgment"]
    provenance = presentation["component_provenance"]
    component_differences = []
    selected_sources = {}
    for name in COMPONENTS:
        item = provenance[name]
        selected_sources[name] = item["selected_source"]
        before = item["baseline_v2"]
        after = item["compact_v3"]
        differing = [
            field for field in ("visibility", "severity", "confidence", "issue_codes")
            if before.get(field) != after.get(field)
        ]
        if differing:
            component_differences.append(
                {
                    "component": name,
                    "differing_fields": differing,
                    "baseline_v2": {field: before.get(field) for field in differing},
                    "compact_v3": {field: after.get(field) for field in differing},
                }
            )
    disagreement = {
        "verdict_differs": baseline.get("verdict") != compact.get("verdict"),
        "baseline_v2_verdict": baseline.get("verdict"),
        "compact_v3_verdict": compact.get("verdict"),
        "baseline_v2_score": baseline.get("natural_placement_score"),
        "compact_v3_score": compact.get("natural_placement_score"),
        "component_differences": component_differences,
    }
    details = {
        "Assessment origin": "Application-derived deterministic merge of two independent model assessments",
        "Baseline V2 summary": baseline.get("observation", {}).get("summary", ""),
        "Compact V3 summary": compact.get("observation", {}).get("summary", ""),
        "Stage disagreement": json.dumps(disagreement, indent=2, ensure_ascii=False),
        "Selected source by component": json.dumps(selected_sources, indent=2, ensure_ascii=False),
        "Baseline V2 original assessment": json.dumps(baseline, indent=2, ensure_ascii=False),
        "Compact V3 original assessment": json.dumps(compact, indent=2, ensure_ascii=False),
        "Component selection provenance": json.dumps(provenance, indent=2, ensure_ascii=False),
    }
    if presentation.get("consensus_envelope") is True:
        proposal = presentation["proposal_aware_components"]
        independent = presentation["names_only_components"]
        resolutions = presentation["consensus_resolution"]
        final = presentation["final_decision"]
        disagreement = {
            "triggered": bool(resolutions),
            "component_statuses": {
                name: {
                    "status": value["status"],
                    "selected": value["selected"],
                    "shared_issue_codes": value["shared_issue_codes"],
                }
                for name, value in resolutions.items()
            },
            "uncertainty_notes": final["uncertainty_notes"],
        }
        details.update({
            "Assessment origin": "Application-derived consensus revision using two independent verification checks",
            "Proposal-aware verification check": (
                json.dumps(proposal, indent=2, ensure_ascii=False)
                if proposal else "Not triggered for this row"
            ),
            "Names-only independent verification check": (
                json.dumps(independent, indent=2, ensure_ascii=False)
                if independent else "Not triggered for this row"
            ),
            "Consensus disagreement note": json.dumps(disagreement, indent=2, ensure_ascii=False),
            "Consensus component resolution": json.dumps(
                resolutions, indent=2, ensure_ascii=False
            ),
            "Consensus compact assessment": json.dumps(
                presentation["consensus_compact_judgment"], indent=2, ensure_ascii=False
            ),
            "Consensus selected source by component": json.dumps(
                {
                    name: value["selected_source"]
                    for name, value in presentation["consensus_component_provenance"].items()
                },
                indent=2,
                ensure_ascii=False,
            ),
            "Consensus component provenance": json.dumps(
                presentation["consensus_component_provenance"], indent=2, ensure_ascii=False
            ),
            "Application merged assessment before consensus decision": json.dumps(
                presentation["application_merged_judgment"], indent=2, ensure_ascii=False
            ),
            "Consensus final decision": json.dumps(final, indent=2, ensure_ascii=False),
        })
    if presentation.get("verified_envelope") is True:
        final = presentation["final_decision"]
        verifier_components = presentation["verifier_components"]
        details.update({
            "Verification overlay present": bool(verifier_components),
            "Verifier component assessment": json.dumps(verifier_components, indent=2, ensure_ascii=False),
            "Verified compact assessment": json.dumps(
                presentation["verified_compact_judgment"], indent=2, ensure_ascii=False
            ),
            "Verified selected source by component": json.dumps(
                {
                    name: value["selected_source"]
                    for name, value in presentation["verified_component_provenance"].items()
                },
                indent=2,
                ensure_ascii=False,
            ),
            "Verified component provenance": json.dumps(
                presentation["verified_component_provenance"], indent=2, ensure_ascii=False
            ),
            "Application merged assessment before final override": json.dumps(
                presentation["application_merged_judgment"], indent=2, ensure_ascii=False
            ),
            "Final decision and overrides": json.dumps(final, indent=2, ensure_ascii=False),
            "Verification uncertainty notes": json.dumps(
                final["uncertainty_notes"], indent=2, ensure_ascii=False
            ),
        })
    return details


def make_row(
    record: Mapping[str, Any],
    judgment: Mapping[str, Any],
    row_idx: int,
    twin_url: str,
    two_pass: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    record_id = str(record["id"])
    generated = record["generated_image"]
    verdict = str(judgment["verdict"])
    score = judgment["natural_placement_score"]
    prompt_source = record.get("scene_prompt_source")
    environment = prompt_source.get("environment") if isinstance(prompt_source, Mapping) else None
    view = record.get("view")
    camera = view.get("camera_tag") if isinstance(view, Mapping) else None
    meta: dict[str, Any] = {
        "Dataset / batch": record.get("device_type"),
        "Product type": record.get("device_type"),
        "Product": record.get("product", ""),
        "Device": record.get("device", ""),
        "V6.1 candidate": record.get("candidate_id", ""),
        "Camera": camera or "",
        "Environment": environment or "",
        "Original scene prompt": record["scene_prompt"],
        "Judge v3 predicted verdict": verdict,
        "Judge score": score,
        "Judge weighted component score": judgment.get("weighted_component_score"),
        "Judge applied score cap": judgment.get("applied_score_cap"),
        "Judge confidence": judgment.get("confidence"),
        "Judge coverage": judgment.get("coverage"),
        "Judge component scores": component_scores(judgment),
        "Judge policy status": judgment.get("threshold_status"),
        "Judge policy version": judgment.get("policy_version"),
    }
    summary = judgment["observation"].get("summary")
    if isinstance(summary, str) and summary:
        meta["Judge evidence summary"] = summary
    if two_pass is not None:
        meta.update(two_pass_row_details(two_pass))
    assessment_label = (
        "Consensus revision research-candidate assessment"
        if two_pass is not None and two_pass.get("consensus_envelope") is True
        else "Verified research-candidate assessment"
        if two_pass is not None and two_pass.get("verified_envelope") is True
        else "Combined two-pass assessment"
        if two_pass is not None
        else "Judge v3 assessment"
    )
    return {
        "meta_data": {
            "row_idx": row_idx,
            "evalset_item_id": record_id,
            "key_val_informations": meta,
        },
        "images": [
            {
                "asset_type": "image",
                "is_model_input_or_output": "model_output",
                "image_src": gateway_url(generated, record_id, "generated image"),
                "meta_text": {
                    "label": "Generated scene — answer IMAGE quality question for this image",
                    "Judge predicted verdict": verdict.upper(),
                    "Judge final score": f"{score}/100",
                },
            },
            {
                "asset_type": "image",
                "is_model_input_or_output": "model_input",
                "image_src": twin_url,
                "meta_text": {"label": "Digital twin — product reference only; do not rate"},
            },
            {
                "asset_type": "text",
                "text_content": evidence_text(judgment),
                "meta_text": {
                    "label": assessment_label + " — answer JUDGE agreement question for this text"
                },
            },
        ],
    }


def report_data(
    *,
    title: str,
    rows: Sequence[dict[str, Any]],
    records: Sequence[Mapping[str, Any]],
    judgments: Mapping[str, Mapping[str, Any]],
    protocol_metadata: Mapping[str, Any],
    run_provenance: Mapping[str, Any],
    manifest_path: Path,
    protocol_path: Path,
    two_pass: bool = False,
    verified: bool = False,
    consensus: bool = False,
) -> dict[str, Any]:
    verdicts = Counter(str(judgments[str(record["id"])]["verdict"]) for record in records)
    types = Counter(str(record.get("device_type")) for record in records)
    protocol_note = (
        [
            "Consensus revision research candidate",
            {
                "Assessment origin": "Application-derived two-check consensus revision; not a single-model response",
                "Research status": run_provenance.get("development_status"),
                "Decision policy": run_provenance.get("policy_version"),
                "Consensus policy SHA-256": run_provenance.get("consensus_policy_sha256"),
                "Frozen consensus generator SHA-256": run_provenance.get("consensus_generator_sha256"),
                "Proposal-aware verification checks": run_provenance.get("proposal_aware_checks"),
                "Names-only independent verification checks": run_provenance.get("names_only_checks"),
                "Consensus-triggered components": run_provenance.get("trigger_components"),
                "Source, both check results, raw responses, and protocol hashes verified": True,
                "Consensus resolution, merge, scoring, and final decision recomputed": True,
                "Development disclosure": run_provenance.get("development_disclosure"),
                "Score meaning": "Natural-placement rubric score from 0 to 100; not an acceptance probability",
            },
        ]
        if consensus
        else
        [
            "Verified research candidate",
            {
                "Assessment origin": "Application-derived V2 + compact V3 merge with conditional semantic verification",
                "Research status": protocol_metadata.get(
                    "development_status",
                    run_provenance.get("development_status"),
                ),
                "Decision policy": run_provenance.get("policy_version"),
                "Two-pass merge policy SHA-256": run_provenance.get("two_pass_policy_sha256"),
                "Two-pass combiner SHA-256": run_provenance.get("two_pass_combiner_sha256"),
                "Verified merger SHA-256": run_provenance.get("verified_merger_sha256"),
                "Conditional verifier overlays": run_provenance.get("verifier_overlays"),
                "Source and overlay hashes verified": True,
                "Protocol snapshots verified": True,
                "Overlay, merge, scoring, and final overrides recomputed": True,
                "Score meaning": "Natural-placement rubric score from 0 to 100; not an acceptance probability",
            },
        ]
        if verified
        else
        [
            "Two-pass application-derived assessment",
            {
                "Assessment origin": "Deterministic application merge; not a single-model response",
                "Baseline stage": "Frozen V2, gpt-5.5, visual anchors enabled",
                "Compact stage": "Compact V3, gpt-5.5, visual anchors disabled",
                "Merge policy version": protocol_metadata.get("policy_version"),
                "Merge policy SHA-256": run_provenance.get("policy_sha256"),
                "Combiner SHA-256": run_provenance.get("combiner_sha256"),
                "Frozen merge policy": str(protocol_path),
                "Both stage protocols verified": True,
                "Stage source artifact hashes verified": True,
                "Deterministic merge and score recomputed": True,
            },
        ]
        if two_pass
        else [
            "Judge protocol",
            {
                "Model requested": protocol_metadata.get("model"),
                "Model returned": run_provenance.get("model_returned"),
                "Reasoning effort": protocol_metadata.get("reasoning_effort"),
                "Protocol version": run_provenance.get("protocol_version"),
                "System prompt SHA-256": run_provenance.get("system_prompt_sha256"),
                "Observation schema SHA-256": run_provenance.get("schema_sha256"),
                "Scoring SHA-256": run_provenance.get("scoring_sha256"),
                "Wire schema SHA-256": run_provenance.get("wire_schema_sha256"),
                "Policy version": run_provenance.get("policy_version"),
                "Threshold status": run_provenance.get("threshold_status"),
                "Frozen protocol metadata": str(protocol_path),
                "Frozen protocol SHA-256": sha256(protocol_path),
                "Frozen protocol status": protocol_metadata.get("status"),
                "Visual anchors enabled": protocol_metadata.get("visual_anchors", True),
            },
        ]
    )
    return {
        "is_secure": True,
        "meta_texts": [
            title,
            [
                "Evaluation inputs",
                {
                    "Manifest": str(manifest_path),
                    "Manifest SHA-256": sha256(manifest_path),
                    "Rows": len(rows),
                    "Generated image stage": "scene_generation",
                    "Human labels passed to judge": "No",
                    "Evaluation status": (
                        "Research candidate" if verified or consensus else "Research evaluation"
                    ),
                    "Scores": "Natural-placement rubric scores, not acceptance probabilities",
                },
            ],
            protocol_note,
            ["Review scope", {"Rows": len(rows), **dict(sorted(types.items()))}],
            ["Judge verdicts", dict(sorted(verdicts.items()))],
            [
                "Human annotation — two independent questions",
                {
                    "Question 1 — image": QUESTION_WIRE[0]["text"],
                    "Question 1 options": "Pass / Review / Fail",
                    "Question 2 — judge": QUESTION_WIRE[1]["text"],
                    "Question 2 options": "Agree / Partly agree / Disagree",
                    "Instruction": (
                        "Rate the generated image itself in Question 1. Separately rate the "
                        "displayed judge assessment in Question 2. Do not use one answer as the other."
                    ),
                    "Comments": "Each question has its own comment box; an overall row comment is also available",
                },
            ],
        ],
        "rows": list(rows),
    }


def build_reports(
    *,
    manifest_path: Path,
    results_dir: Path,
    protocol_path: Path,
    output_root: Path,
    title: str,
    ldap: str,
    expected_rows: int | None,
    publish_bucket: str,
    publish_prefix: str,
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    records = manifest_records(manifest, expected_rows)
    protocol = load_json(protocol_path)
    require(isinstance(protocol, Mapping), "protocol metadata must be an object")
    paths = result_paths(results_dir)
    ids = [str(record["id"]) for record in records]
    require(set(paths) == set(ids), "result IDs/count do not exactly match manifest IDs")
    judgments: dict[str, Mapping[str, Any]] = {}
    result_audit: dict[str, Any] = {}
    two_pass_presentations: dict[str, Mapping[str, Any]] = {}
    first_result = load_json(paths[ids[0]])
    require(isinstance(first_result, Mapping), "first result is not an object")
    result_schema = first_result.get("schema_version")
    verified = result_schema == "placement-verified-additions-envelope-v2"
    consensus = result_schema in {
        "placement-consensus-additions-envelope-v1",
        "placement-consensus-additions-envelope-v2",
    }
    two_pass = result_schema == "placement-two-pass-result-v1"
    if consensus:
        consensus_policy, generator_path, protocol_audit = consensus_protocol_context(
            protocol, protocol_path
        )
        trigger_reference = protocol_audit["inputs"].get("new160_trigger")
        require(isinstance(trigger_reference, Mapping), "consensus snapshot lacks NEW160 trigger")
        trigger_path = Path(str(trigger_reference.get("path", ""))).resolve()
        trigger_hash = sha256(trigger_path)
        trigger_payload = load_json(trigger_path)
        require(isinstance(trigger_payload, Mapping), "consensus trigger manifest invalid")
        require(trigger_payload.get("comments_or_expectations_included") is False, "consensus trigger includes comments or expectations")
        trigger_records = trigger_payload.get("records")
        require(isinstance(trigger_records, list), "consensus trigger records missing")
        trigger_map: dict[str, list[str]] = {}
        records_by_id = {str(record["id"]): record for record in records}
        for trigger_record in trigger_records:
            require(isinstance(trigger_record, Mapping), "consensus trigger record invalid")
            record_id = str(trigger_record.get("id", ""))
            require(record_id in records_by_id and record_id not in trigger_map, f"consensus trigger ID invalid: {record_id}")
            require(trigger_record.get("runtime_input") == expected_runtime_input(records_by_id[record_id]), f"{record_id}: consensus trigger runtime input differs")
            proposed = trigger_record.get("proposed_components")
            require(isinstance(proposed, Mapping) and proposed, f"{record_id}: consensus trigger components missing")
            trigger_map[record_id] = list(proposed)
        require(trigger_payload.get("expected_count") == len(trigger_map), "consensus trigger count differs")
        require(trigger_payload.get("expected_component_count") == sum(len(v) for v in trigger_map.values()), "consensus trigger component count differs")
        two_pass_policy = load_json(TWO_PASS_POLICY)
        progress_audit, run_summary, run_audit = validate_consensus_summary(
            results_dir,
            ids,
            paths,
            consensus_policy,
            generator_path,
            trigger_path,
            trigger_map,
        )
        summary_items = {item["id"]: item for item in run_summary["records"]}
        resolution_counts: Counter[str] = Counter()
        for record in records:
            record_id = str(record["id"])
            result, judgment, audit, presentation = validate_consensus_result(
                record,
                paths[record_id],
                two_pass_policy,
                consensus_policy,
                generator_path,
                trigger_path,
                trigger_hash,
                trigger_map,
            )
            decision = result["final_decision"]
            item = summary_items[record_id]
            require(item.get("verdict") == decision.get("verdict"), f"{record_id}: consensus summary verdict differs")
            require(item.get("reported_overall_confidence") == decision.get("reported_overall_confidence"), f"{record_id}: consensus summary confidence differs")
            require(item.get("confirmed") == decision.get("confirmed_consensus_components"), f"{record_id}: consensus summary confirmed components differ")
            require(item.get("rejected") == decision.get("rejected_addition_components"), f"{record_id}: consensus summary rejected components differ")
            require(item.get("unconfirmed") == decision.get("unconfirmed_addition_components"), f"{record_id}: consensus summary unconfirmed components differ")
            resolution_counts.update(
                value["status"] for value in result["consensus_resolution"].values()
            )
            judgments[record_id] = judgment
            result_audit[record_id] = audit
            two_pass_presentations[record_id] = presentation
        require(dict(resolution_counts) == run_summary.get("resolution_counts"), "consensus summary resolution counts differ")
        audit_intersections = run_audit.get("component_intersections")
        require(isinstance(audit_intersections, list), "consensus audit intersections missing")
        require(len(audit_intersections) == sum(len(v) for v in trigger_map.values()), "consensus audit intersection count differs")
        run_provenance = {
            "assessment_origin": "application_derived_two_check_consensus",
            "policy_version": run_summary.get("policy_version"),
            "development_status": run_summary.get("development_status"),
            "development_disclosure": consensus_policy.get("disclosure"),
            "two_pass_policy_sha256": sha256(TWO_PASS_POLICY),
            "two_pass_combiner_sha256": sha256(TWO_PASS_COMBINER),
            "consensus_policy_sha256": sha256(CONSENSUS_ROOT / "policy.json"),
            "consensus_generator_sha256": sha256(generator_path),
            "proposal_aware_checks": len(trigger_map),
            "names_only_checks": len(trigger_map),
            "trigger_components": sum(len(v) for v in trigger_map.values()),
            "resolution_counts": dict(resolution_counts),
            "protocol_snapshot": protocol_audit,
        }
    elif verified:
        verified_policy, expected_merge_sha256, protocol_audit = verified_protocol_context(
            protocol, protocol_path, manifest_path
        )
        expected_development_status = protocol_audit.get(
            "development_status", "posthoc_policy_revision_not_untouched_validation"
        )
        progress_audit, run_summary, run_audit = validate_verified_summary(
            results_dir,
            manifest_path,
            ids,
            paths,
            expected_development_status=expected_development_status,
        )
        run_merge_reference = run_summary.get("merge_generator")
        if expected_merge_sha256 is not None:
            require(isinstance(run_merge_reference, Mapping), "verified summary merge generator missing")
            run_merge_path = Path(str(run_merge_reference.get("path", ""))).resolve()
            require(run_merge_path.is_file(), "verified summary merge generator path missing")
            require(
                run_merge_reference.get("sha256") == expected_merge_sha256 == sha256(run_merge_path),
                "verified summary merge generator differs from selected protocol",
            )
        summary_items = {item["id"]: item for item in run_summary["records"]}
        overlay_count = 0
        merge_hashes: set[str] = set()
        for record in records:
            record_id = str(record["id"])
            result, judgment, audit, presentation = validate_verified_result(
                record,
                paths[record_id],
                verified_policy,
                expected_merge_sha256=expected_merge_sha256,
                expected_development_status=expected_development_status,
            )
            item = summary_items[record_id]
            decision = result["final_decision"]
            for key in (
                "verdict",
                "reported_overall_confidence",
                "verdict_override",
                "confidence_override",
            ):
                require(item.get(key) == decision.get(key), f"{record_id}: verified summary {key} differs")
            overlay_count += int(result.get("verifier_overlay") is not None)
            merge_hashes.add(audit["verified_merger_sha256"])
            if expected_merge_sha256 is not None and audit["verifier_overlay"]["present"]:
                selected = audit["verifier_overlay"].get("selected_protocol")
                require(isinstance(selected, Mapping), f"{record_id}: verifier selected protocol metadata missing")
                require(
                    selected.get("sha256") == protocol_audit["selected_protocol_sha256"],
                    f"{record_id}: verifier selected protocol hash differs",
                )
                require(
                    selected.get("snapshot_manifest_sha256") == protocol_audit["snapshot_manifest_sha256"],
                    f"{record_id}: verifier snapshot manifest hash differs",
                )
            judgments[record_id] = judgment
            result_audit[record_id] = audit
            two_pass_presentations[record_id] = presentation
        coverage = run_audit.get("source_hash_coverage", run_audit.get("coverage_validated"))
        require(isinstance(coverage, Mapping), "verified audit coverage missing")
        require(coverage.get("verifier_overlays") == overlay_count, "verified audit overlay count differs")
        if run_audit.get("schema_version") == "placement-verified-additions-new160-audit-v1":
            audit_merge = run_audit.get("merge_generator")
            require(isinstance(audit_merge, Mapping), "NEW160 audit merge generator missing")
            require(audit_merge == run_summary.get("merge_generator"), "NEW160 audit merge generator differs")
            audit_protocol = run_audit.get("selected_protocol")
            require(isinstance(audit_protocol, Mapping), "NEW160 audit selected protocol missing")
            require(
                audit_protocol.get("sha256") == protocol_audit.get("selected_protocol_sha256"),
                "NEW160 audit selected protocol hash differs",
            )
        require(len(merge_hashes) == 1, "verified envelopes use multiple merge generators")
        run_provenance = {
            "assessment_origin": "application_derived_verified_overlay",
            "policy_version": run_summary.get("policy_version"),
            "development_status": run_summary.get("development_status"),
            "two_pass_policy_sha256": sha256(TWO_PASS_POLICY),
            "two_pass_combiner_sha256": sha256(TWO_PASS_COMBINER),
            "verified_merger_sha256": next(iter(merge_hashes)),
            "verifier_overlays": overlay_count,
            "selected_protocol": protocol_audit,
        }
    elif two_pass:
        canonical_policy = load_json(TWO_PASS_POLICY)
        require(protocol == canonical_policy, "two-pass protocol metadata must be the exact current merge policy")
        progress_audit, run_summary = validate_two_pass_summary(
            results_dir, manifest_path, ids, paths
        )
        summary_items = {item["id"]: item for item in run_summary["items"]}
        for record in records:
            record_id = str(record["id"])
            result, judgment, audit, presentation = validate_two_pass_result(
                record, paths[record_id], protocol
            )
            item = summary_items[record_id]
            require(item.get("verdict") == judgment.get("verdict"), f"{record_id}: summary verdict differs")
            require(item.get("score") == judgment.get("natural_placement_score"), f"{record_id}: summary score differs")
            judgments[record_id] = judgment
            result_audit[record_id] = audit
            two_pass_presentations[record_id] = presentation
        run_provenance = {
            "assessment_origin": "application_derived_deterministic_merge",
            "policy_version": protocol.get("policy_version"),
            "policy_sha256": sha256(TWO_PASS_POLICY),
            "combiner_sha256": sha256(TWO_PASS_COMBINER),
            "stage_roles": ["baseline_v2", "compact_v3"],
        }
    else:
        claims = protocol_claims(protocol)
        progress_audit = validate_progress(results_dir, manifest_path, ids, paths)
        returned_models: set[str] = set()
        actual_values: dict[str, set[Any]] = {
            key: set()
            for key in (
                "protocol_version",
                "wire_schema_sha256",
                "system_prompt_sha256",
                "schema_sha256",
                "scoring_sha256",
                "runner_sha256",
                "model_returned",
                "policy_version",
                "threshold_status",
            )
        }
        for record in records:
            record_id = str(record["id"])
            result, judgment, audit = validate_result(record, paths[record_id], claims)
            judgments[record_id] = judgment
            result_audit[record_id] = audit
            returned = result.get("model_returned")
            require(isinstance(returned, str) and returned, f"{record_id}: returned model missing")
            returned_models.add(returned)
            for key in (
                "protocol_version",
                "wire_schema_sha256",
                "system_prompt_sha256",
                "schema_sha256",
                "scoring_sha256",
                "runner_sha256",
                "model_returned",
            ):
                actual_values[key].add(result.get(key))
            actual_values["policy_version"].add(judgment.get("policy_version"))
            actual_values["threshold_status"].add(judgment.get("threshold_status"))
        require(len(returned_models) == 1, "results use multiple returned model identities")
        require(
            all(len(values) == 1 and None not in values for values in actual_values.values()),
            "results have missing or inconsistent run provenance",
        )
        run_provenance = {key: next(iter(values)) for key, values in actual_values.items()}

    require(VENDORED_VIEWER.is_file(), f"vendored viewer missing: {VENDORED_VIEWER}")
    require(bool(title.strip()), "title must be nonempty")
    require(bool(ldap.strip()), "LDAP must be nonempty")
    require(bool(publish_bucket.strip()), "publish bucket must be nonempty")
    publish_prefix = publish_prefix.strip("/")
    require(bool(publish_prefix), "publish prefix must be nonempty")
    query = review_query(ldap.strip())
    validate_review_query(query, ldap.strip())

    twin_assets: dict[str, dict[str, Any]] = {}
    twin_urls: dict[str, str] = {}
    for record in records:
        record_id = str(record["id"])
        twin = record["twin_image"]
        twin_hash = str(twin["sha256"])
        twin_path = Path(str(twin["local_path"])).resolve()
        source_filename = str(twin.get("filename") or twin_path.name)
        filename = f"{twin_hash[:16]}__{source_filename}"
        key = f"{publish_prefix}/assets/twins/{filename}"
        previous = twin_assets.get(filename)
        asset = {
            "path": str(twin_path),
            "source_filename": source_filename,
            "sha256": twin_hash,
            "bytes": twin_path.stat().st_size,
            "s3_key": key,
        }
        require(previous in (None, asset), f"twin filename collision with different bytes: {filename}")
        twin_assets[filename] = asset
        twin_urls[record_id] = f"{GATEWAY}/asset/{publish_bucket}/{key}"

    summaries = []
    report_hashes: dict[str, Any] = {}
    for directory, product_type in REPORT_SCOPES:
        selected = [
            record for record in records
            if product_type is None or record.get("device_type") == product_type
        ]
        require(bool(selected), f"no records for report scope {directory}")
        rows = [
            make_row(
                record,
                judgments[str(record["id"])],
                index,
                twin_urls[str(record["id"])],
                two_pass_presentations.get(str(record["id"])),
            )
            for index, record in enumerate(selected, start=1)
        ]
        suffix = "" if product_type is None else f" — {directory.title()}"
        data = report_data(
            title=title.strip() + suffix,
            rows=rows,
            records=selected,
            judgments=judgments,
            protocol_metadata=protocol,
            run_provenance=run_provenance,
            manifest_path=manifest_path,
            protocol_path=protocol_path,
            two_pass=two_pass or verified or consensus,
            verified=verified,
            consensus=consensus,
        )
        report_dir = output_root / directory
        report_dir.mkdir(parents=True, exist_ok=True)
        atomic_json(report_dir / "data.json", data)
        shutil.copyfile(VENDORED_VIEWER, report_dir / "viewer.html")
        (report_dir / "viewer.html").chmod(0o644)
        report_hashes[directory] = {
            "rows": len(rows),
            "data_json_sha256": sha256(report_dir / "data.json"),
            "viewer_html_sha256": sha256(report_dir / "viewer.html"),
        }
        summaries.append({
            "scope": directory,
            "rows": len(rows),
            "output_dir": str(report_dir.resolve()),
            "review_query": query,
        })

    build_record = {
        "schema_version": "placement-v3-v6.1-fe-build-v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "local_build_validated_not_published",
        "sources": {
            "manifest": {"path": str(manifest_path), "sha256": sha256(manifest_path)},
            "results_dir": str(results_dir),
            "protocol_metadata": {"path": str(protocol_path), "sha256": sha256(protocol_path)},
            "progress": progress_audit,
            "vendored_viewer": {"path": str(VENDORED_VIEWER), "sha256": sha256(VENDORED_VIEWER)},
        },
        "validation": {
            "result_format": (
                "application_derived_two_check_consensus_v1"
                if consensus
                else "application_derived_verified_overlay_v2"
                if verified
                else "application_derived_two_pass"
                if two_pass
                else "single_model_judgment"
            ),
            "manifest_rows": len(records),
            "result_files": len(paths),
            "result_ids_exactly_match_manifest": True,
            "runtime_inputs_exactly_match_manifest": True,
            "runtime_input_whitelist_verified": True,
            "image_prompt_and_result_hashes_verified": True,
            "protocol_claims_match_every_result": True,
            "two_pass_stage_protocols_and_source_hashes_verified": two_pass or verified or consensus,
            "two_pass_deterministic_merge_recomputed": two_pass or verified or consensus,
            "two_pass_original_assessments_exposed_in_row_details": two_pass or verified or consensus,
            "verified_source_overlay_protocol_and_raw_hashes_verified": verified,
            "verified_overlay_merge_score_and_final_override_recomputed": verified,
            "verification_uncertainty_exposed_in_row_details": verified,
            "consensus_both_check_results_raw_responses_and_protocols_verified": consensus,
            "consensus_resolution_merge_score_and_final_decision_recomputed": consensus,
            "consensus_both_checks_and_disagreement_exposed_in_row_details": consensus,
            "run_provenance": run_provenance,
            "viewer_copied_verbatim": all(
                item["viewer_html_sha256"] == sha256(VENDORED_VIEWER)
                for item in report_hashes.values()
            ),
            "question_wire_round_trip_verified": True,
            "human_labels_invented": False,
        },
        "result_audit": result_audit,
        "publish_destination": {
            "bucket": publish_bucket,
            "prefix": publish_prefix,
        },
        "shared_twin_assets": twin_assets,
        "reports": report_hashes,
        "review_query": query,
    }
    atomic_json(output_root / "build_manifest.json", build_record)
    return {
        "reports": summaries,
        "build_manifest": str((output_root / "build_manifest.json").resolve()),
        "build_manifest_sha256": sha256(output_root / "build_manifest.json"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--protocol-metadata", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--ldap", default="hshariati")
    parser.add_argument("--publish-bucket", default=DEFAULT_PUBLISH_BUCKET)
    parser.add_argument("--publish-prefix", default=DEFAULT_PUBLISH_PREFIX)
    parser.add_argument(
        "--independent-check-root",
        type=Path,
        default=INDEPENDENT_CHECK_ROOT,
        help="frozen names-only protocol directory used by this consensus run",
    )
    parser.add_argument(
        "--expected-rows",
        type=int,
        default=160,
        help="completeness gate; use a different value only for explicitly labeled structural tests",
    )
    return parser.parse_args()


def main() -> None:
    global INDEPENDENT_CHECK_ROOT
    args = parse_args()
    try:
        require(args.expected_rows > 0, "--expected-rows must be positive")
        INDEPENDENT_CHECK_ROOT = args.independent_check_root.expanduser().resolve()
        summary = build_reports(
            manifest_path=args.manifest.expanduser().resolve(),
            results_dir=args.results_dir.expanduser().resolve(),
            protocol_path=args.protocol_metadata.expanduser().resolve(),
            output_root=args.output_dir.expanduser().resolve(),
            title=args.title,
            ldap=args.ldap,
            expected_rows=args.expected_rows,
            publish_bucket=args.publish_bucket,
            publish_prefix=args.publish_prefix,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
