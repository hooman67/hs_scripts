# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Image+twin placement judge. Does not generate images or repair judgments."""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import mimetypes
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

try:
    from .scoring import (
        OBSERVATION_SCHEMA,
        aggregate_observation as aggregate,
        validate_runtime_input,
    )
except ImportError:  # Direct script execution.
    from scoring import (  # type: ignore
        OBSERVATION_SCHEMA,
        aggregate_observation as aggregate,
        validate_runtime_input,
    )


ROOT = Path(__file__).resolve().parent
PROTOCOL_VERSION = "placement-judge-v2-request-v3"
SUPPORTED_IMAGE_MIMES = {"image/png", "image/jpeg", "image/webp"}




def sha256(path: Any) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _json_sha256(value: Any) -> str:
    serialized = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def client():
    probe = ROOT.parents[3] / "research/source_messaging_v1_to_v6/scripts/probe_gpt55.py"
    spec = importlib.util.spec_from_file_location("placement_auth", probe)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load placement authentication helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    api_client, mode = module.client_and_auth_mode()
    return api_client.with_options(timeout=180, max_retries=0), mode


def wire_schema(value: Any) -> Any:
    # Local semantic validation retains constraints unsupported by some deployments.
    if isinstance(value, dict):
        return {
            key: wire_schema(child)
            for key, child in value.items()
            if key not in ("$schema", "uniqueItems", "minLength")
        }
    if isinstance(value, list):
        return [wire_schema(child) for child in value]
    return value


WIRE_SCHEMA = wire_schema(OBSERVATION_SCHEMA)
RUNNER_SHA256 = sha256(__file__)
WIRE_SCHEMA_SHA256 = _json_sha256(WIRE_SCHEMA)


def _image_mime(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in SUPPORTED_IMAGE_MIMES:
        raise ValueError(f"Unsupported image format: {path.name}")
    return mime


def _load_visual_anchors(root: Path = ROOT) -> Dict[str, Any]:
    manifest = json.loads((root / "data/visual_anchors.json").read_text(encoding="utf-8"))
    examples = manifest.get("examples")
    if not isinstance(examples, list) or len(examples) != 7:
        raise ValueError("Judge v2 requires the frozen seven development exemplars")
    seen_ids, seen_hashes = set(), set()
    allowed = {"user_adjudicated_failure", "development_human_defect_anchor", "researcher_interpreted_reference"}
    for a in examples:
        if not all(isinstance(a.get(k), str) and a[k] for k in ("asset_id", "kind", "local_path", "sha256", "guidance")):
            raise ValueError("Anchor provenance is incomplete")
        if a["kind"] not in allowed or a["asset_id"] in seen_ids or a["sha256"] in seen_hashes:
            raise ValueError("Invalid or duplicate development exemplar")
        _image_mime(Path(a["local_path"]))
        if sha256(a["local_path"]) != a["sha256"]:
            raise ValueError("Anchor bytes differ from frozen manifest")
        seen_ids.add(a["asset_id"])
        seen_hashes.add(a["sha256"])
    return manifest


def _validate_cached_result(old: Any, fingerprint: str) -> Dict[str, Any]:
    if not isinstance(old, dict):
        raise RuntimeError("Existing result is not a JSON object")
    if old.get("fingerprint") != fingerprint or old.get("ok") is not True:
        raise RuntimeError(
            "Output exists for failed or different request; use a new output directory"
        )
    judgment = old.get("judgment")
    observation = judgment.get("observation") if isinstance(judgment, dict) else None
    if not isinstance(observation, dict):
        raise RuntimeError("Cached result has no valid observation")
    recomputed = aggregate(observation)
    if judgment != recomputed:
        raise RuntimeError("Cached judgment differs from current deterministic aggregation")
    return old


def _model_identity_matches(requested: str, returned: Any) -> bool:
    if not isinstance(returned, str):
        return False
    pattern = rf"{re.escape(requested)}(?:-\d{{4}}-\d{{2}}-\d{{2}})?"
    return re.fullmatch(pattern, returned) is not None


def judge(runtime_input, output_dir, model="gpt-5.5", visual_anchors=False):
    validate_runtime_input(runtime_input)
    if not isinstance(model, str) or not model:
        raise ValueError("Model must be a nonempty string")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    system = (ROOT / "system_prompt.md").read_text(encoding="utf-8")
    files = {
        key: {
            "path": str(Path(runtime_input[key]).resolve()),
            "sha256": sha256(runtime_input[key]),
        }
        for key in ("generated_image", "twin_image")
    }
    record = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "protocol_version": PROTOCOL_VERSION,
        "runner_sha256": RUNNER_SHA256,
        "wire_schema_sha256": WIRE_SCHEMA_SHA256,
        "input": runtime_input,
        "images": files,
        "model_requested": model,
        "reasoning_effort": "high",
        "max_completion_tokens": 12000,
        "system_prompt_sha256": sha256(ROOT / "system_prompt.md"),
        "schema_sha256": sha256(ROOT / "observation_schema.json"),
        "scoring_sha256": sha256(ROOT / "scoring.py"),
        "image_detail": "high",
        "image_transform": "none; original bytes",
        "visual_anchors_enabled": bool(visual_anchors),
    }
    anchors = None
    if visual_anchors:
        anchors = _load_visual_anchors()
        anchor_hashes = {anchor["sha256"] for anchor in anchors["examples"]}
        target_hashes = {image["sha256"] for image in files.values()}
        excluded = [a for a in anchors["examples"] if a["sha256"] in target_hashes]
        anchors["examples"] = [a for a in anchors["examples"] if a["sha256"] not in target_hashes]
        record["excluded_target_identical_anchor_ids"] = [a["asset_id"] for a in excluded]
        record["visual_anchor_manifest_sha256"] = sha256(ROOT / "data/visual_anchors.json")
        record["visual_anchors"] = anchors

    fingerprint_payload = {
        key: value for key, value in record.items() if key != "started_at"
    }
    fingerprint = _json_sha256(fingerprint_payload)
    record["fingerprint"] = fingerprint
    result_path = output_dir / "result.json"
    if result_path.exists():
        old = json.loads(result_path.read_text(encoding="utf-8"))
        return _validate_cached_result(old, fingerprint)

    (output_dir / "request.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "system_prompt.md").write_text(system, encoding="utf-8")
    (output_dir / "observation_schema.json").write_text(
        json.dumps(OBSERVATION_SCHEMA, indent=2) + "\n", encoding="utf-8"
    )
    content = [
        {
            "type": "text",
            "text": json.dumps(
                {
                    "product_type": runtime_input["product_type"],
                    "scene_prompt": runtime_input["scene_prompt"],
                    "image_stage": runtime_input["image_stage"],
                }
            ),
        }
    ]
    for label, key in (
        ("A — scene-generation image to evaluate", "generated_image"),
        ("B — original digital-twin render for reference", "twin_image"),
    ):
        path = Path(runtime_input[key])
        mime = _image_mime(path)
        content += [
            {"type": "text", "text": label},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode(),
                    "detail": "high",
                },
            },
        ]
    messages = [{"role": "system", "content": system}]
    if anchors is not None:
        anchor_content = [
            {
                "type": "text",
                "text": "Fixed visual rubric examples from DEVELOPMENT data follow. Learn their standard without assuming the target image has the same defects. Reference photos illustrate only visible relationships, not guaranteed perfect overall scores.",
            }
        ]
        for anchor in anchors["examples"]:
            path = Path(anchor["local_path"])
            mime = _image_mime(path)
            anchor_content += [
                {"type": "text", "text": anchor["guidance"]},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode(),
                        "detail": "high",
                    },
                },
            ]
        messages.extend(
            [
                {"role": "user", "content": anchor_content},
                {
                    "role": "assistant",
                    "content": "I will apply these placement standards and assess the next target independently from its own visible evidence.",
                },
            ]
        )
    messages.append({"role": "user", "content": content})

    started = time.monotonic()
    record["attempts"] = []
    try:
        api_client, mode = client()
        record["auth_mode"] = mode
        for attempt in range(1, 4):
            try:
                response = api_client.chat.completions.create(
                    model=model,
                    reasoning_effort="high",
                    max_completion_tokens=12000,
                    messages=messages,
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "placement_observation",
                            "strict": True,
                            "schema": WIRE_SCHEMA,
                        },
                    },
                )
                record["attempts"].append({"attempt": attempt, "status": "ok"})
                break
            except Exception as error:
                status = getattr(error, "status_code", None)
                record["attempts"].append(
                    {
                        "attempt": attempt,
                        "error_type": type(error).__name__,
                        "status": status,
                    }
                )
                if attempt == 3 or status not in (429, 500, 502, 503, 504):
                    raise
                delay = min(60, 5 * 2 ** (attempt - 1))
                try:
                    delay = min(
                        60,
                        max(delay, float(error.response.headers.get("retry-after", 0))),
                    )
                except (ValueError, AttributeError):
                    pass
                time.sleep(delay)

        record["model_returned"] = getattr(response, "model", None)
        raw = response.model_dump(mode="json")
        (output_dir / "response.json").write_text(
            json.dumps(raw, indent=2) + "\n", encoding="utf-8"
        )
        if not _model_identity_matches(model, record["model_returned"]):
            raise RuntimeError("Unexpected model returned")
        choice = response.choices[0]
        if choice.finish_reason != "stop" or choice.message.refusal:
            raise RuntimeError("Incomplete/refused judgment")
        observations = json.loads(choice.message.content)
        record.update(
            ok=True,
            usage=raw.get("usage"),
            judgment=aggregate(observations),
        )
    except Exception as error:
        record.update(
            ok=False,
            error_type=type(error).__name__,
            status_code=getattr(error, "status_code", None),
        )
        # Persist validation diagnostics, never exception strings containing API/HTTP details.
        if hasattr(error, "errors"):
            record["validation_errors"] = list(error.errors)
    record["elapsed_seconds"] = round(time.monotonic() - started, 2)
    result_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--visual-anchors", action="store_true")
    args = parser.parse_args()
    result = judge(
        json.loads(Path(args.input).read_text(encoding="utf-8")),
        args.output,
        args.model,
        args.visual_anchors,
    )
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in (
                    "ok",
                    "model_returned",
                    "elapsed_seconds",
                    "error_type",
                    "validation_errors",
                )
            }
        )
    )
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
