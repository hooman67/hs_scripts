"""Verify actual native V15.8 requests, responses, raw pixels and preserved attempts."""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import io
from pathlib import Path

from PIL import Image

import generate
import study


def audit_one(root, case, catalogue):
    complete = generate.completed(root, case)
    if complete is None:
        raise ValueError(f"No completed native output: {case['id']}")
    result = study.load(complete["result_path"])
    directory = Path(complete["result_path"]).parent
    sdk = Path(complete["calls_path"]).parent
    calls = study.load(complete["calls_path"])
    disabled = result["scap_context"].get("statistics_disabled", False)
    if [call["kind"] for call in calls] != ["text"] * (4 if disabled else 5) + ["image"]:
        raise ValueError("Unexpected successful native call sequence")
    requests, responses = [], []
    for call in calls:
        request, response = sdk / call["request"], sdk / call["response"]
        if (call["status"] != "done" or study.sha(request) != call["request_sha256"]
                or study.sha(response) != call["response_sha256"]):
            raise ValueError("Native SDK evidence is incomplete or changed")
        requests.append(study.load(request))
        responses.append(study.load(response))
    for request, response in zip(requests[:-1], responses[:-1]):
        if (request["model"] != generate.openai_client.TEXT_MODEL
                or request["max_completion_tokens"] != 16384 or request["store"] is not False
                or "reasoning_effort" in request or "temperature" in request
                or response["choices"][0]["finish_reason"] != "stop"):
            raise ValueError("Unexpected native Astra parameters or completion")
    if requests[0]["messages"][1]["content"] != [{
        "type": "text", "text": "Scene request: " + case["prompt"]["text"],
    }]:
        raise ValueError("Actual native selection did not use the unchanged V6.5 source prompt")
    if (result["status"] != "ok" or result["input_fingerprint"] != case["prompt"]["text_sha256"]
            or result["size"] != "2368x1776" or result["ref_count"] != 1
            or result["image_calls"] != 1 or result["baseline_prompt_used"]
            or result["graded"] or result["aligned"] or result["masked"]
            or result["product_category"] != case["prompt"]["device_type"]):
        raise ValueError("Actual native output/input/model contract differs")
    if study.sha(directory / "input.png") != case["product_sha256"]:
        raise ValueError("Actual native product bytes differ from the matched baseline view")
    context = result["scap_context"]
    if (context["original_user_prompt"] != case["prompt"]["text"]
            or context["family"].lower() != case["prompt"]["device_type"]):
        raise ValueError("Statistics came from a different source request or product family")
    if disabled and (context["fields"] or context["cohort_n"] is not None
                     or result["scap_usage"] or result["background_density"]["additions"]):
        raise ValueError("A no-statistics case fabricated cohort evidence or additions")
    if not result.get("realism_plan") or result.get("realism_conditioning") != "text-only":
        raise ValueError("The strong-lighting pass is absent")
    reference = catalogue[result["ref_ids"][0]]
    reference_path = directory / ("ref_2." + reference.mime.split("/")[1])
    if reference_path.read_bytes() != reference.data:
        raise ValueError("Actual selected style reference differs from the frozen catalogue")
    guide = directory / "geometry_guide.png"

    def attachment(mime, body):
        return {"type": "image_url", "image_url": {
            "url": f"data:{mime};base64," + base64.b64encode(body).decode(), "detail": "high",
        }}

    product_part = attachment("image/png", (directory / "input.png").read_bytes())
    reference_part = attachment(reference.mime, reference.data)
    guide_part = attachment("image/png", guide.read_bytes())
    if requests[1]["messages"][1]["content"][1:] != [product_part, reference_part]:
        raise ValueError("Actual Stage A product/style attachments differ from the frozen input bindings")
    if any(request["messages"][1]["content"][1:] != [guide_part, reference_part, product_part]
           for request in requests[2:-1]):
        raise ValueError("Actual writing/statistics/lighting attachments differ from native guide/style/product order")
    expected_camera = generate.pipeline.twin_camera_summary(case["source_camera_metadata"], generate.SIZE)
    if (result["twin_camera"] != expected_camera
            or generate.pipeline.twin_camera_text(expected_camera)
            not in requests[1]["messages"][1]["content"][0]["text"]):
        raise ValueError("The actual Stage A camera instructions differ from the fixed original camera")
    request = requests[-1]
    if (request["model"] != generate.openai_client.IMAGE_MODEL or request["size"] != "2368x1776"
            or request["n"] != 1 or request["quality"] != "high" or request["background"] != "opaque"
            or request["output_format"] != "png" or "mask" in request
            or request["prompt"] != result["prompt"] or len(request["image"]) != 1):
        raise ValueError("Actual native image call differs from the single-guide contract")
    if base64.b64decode(request["image"][0][1]["base64"]) != guide.read_bytes():
        raise ValueError("The actual image-model input is not the native geometry guide")
    raw = base64.b64decode(responses[-1]["data"][0]["b64_json"])
    if (raw != Path(complete["image_path"]).read_bytes()
            or raw != (directory / "gpt_1.png").read_bytes()
            or Image.open(io.BytesIO(raw)).size != generate.SIZE):
        raise ValueError("Published candidate differs from the native raw image response")
    return {
        "prompt_key": case["prompt_key"], "native_completion": complete,
        "statistics_disabled": disabled, "statistics_context": context,
        "actual_astra_attachment_order_verified": True, "actual_original_camera_text_verified": True,
        "text_responses": len(calls) - 1, "image_edits": 1,
        "product": {"path": str(directory / "input.png"), "sha256": study.sha(directory / "input.png")},
        "reference": {"path": str(reference_path), "sha256": study.sha(reference_path), "id": reference.id},
        "geometry_guide": {"path": str(guide), "sha256": study.sha(guide)},
    }


def audit(ids=None):
    root, cases = generate.verify()
    full_count = len(cases)
    if ids:
        wanted = set(ids.split(","))
        cases = [case for case in cases if case["id"] in wanted]
        if len(cases) != len(wanted):
            raise ValueError("Unknown smoke-audit selection")
    catalogue = {ref.id: ref for ref in generate.load_catalog(generate.CATALOG)}
    rows = [audit_one(root, case, catalogue) for case in cases]
    selected = {case["id"] for case in cases}
    attempts, calls = [], []
    for terminal in sorted((root / "attempts").glob("*/attempt_*/terminal.json")):
        if terminal.parent.parent.name not in selected:
            continue
        value = study.load(terminal)
        attempts.append({"path": str(terminal), "sha256": study.sha(terminal),
                         "status": value["status"], "error": value.get("error")})
        calls.extend(value["calls"])
    result = {
        "at_utc": study.now(), "status": "passed", "rows": len(rows),
        "full_expected": full_count, "full160_complete": len(rows) == full_count == 160,
        "no_statistics_cases": sum(row["statistics_disabled"] for row in rows),
        "native_attempts": len(attempts), "terminal_outcomes": dict(Counter(a["status"] for a in attempts)),
        "sdk_requests": dict(Counter(call["kind"] for call in calls)),
        "sdk_completed_responses": dict(Counter(call["kind"] for call in calls if call["status"] == "done")),
        "attempts": attempts, "audits": rows,
        "execution_manifest_sha256": study.sha(study.HERE / "execution_manifest.json"),
        "auditor_sha256": study.sha(Path(__file__)),
    }
    name = "smoke_audit.json" if ids else "generation_audit.json"
    study.emit(study.HERE / name, result)
    study.emit(root / name, result)
    print({key: value for key, value in result.items() if key not in ("attempts", "audits")})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids")
    audit(parser.parse_args().ids)
