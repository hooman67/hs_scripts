"""Shared immutable evidence I/O for Astra-designed placement candidates."""

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent / "v3_1"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LEGACY = load("placement_v32_legacy", R1 / "run_judge.py")
SCORING = LEGACY.SCORING
OBSERVATION_SCHEMA = SCORING.OBSERVATION_SCHEMA
MODEL = "gpt-6-astra"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    )
    temporary.replace(path)


def verify_freeze():
    path = ROOT / "protocol_freeze.json"
    for item in json.loads(path.read_text())["files"]:
        if sha(item["path"]) != item["sha256"]:
            raise ValueError(f"Frozen dependency changed: {item['path']}")
    return sha(path)


def retryable(error):
    import openai

    return isinstance(
        error, (ConnectionError, TimeoutError, openai.APIConnectionError)
    ) or (
        isinstance(error, openai.APIStatusError)
        and (error.status_code in (408, 409, 429) or error.status_code >= 500)
    )


class Collector:
    def __init__(self):
        self.parts, self.models = [], set()
        self.finish, self.usage, self.response_id = None, None, None
        self.count = 0

    def feed(self, frame):
        self.count += 1
        if frame.get("model"):
            self.models.add(frame["model"])
        if frame.get("id"):
            if self.response_id and frame["id"] != self.response_id:
                raise ValueError("Mixed streaming response identities")
            self.response_id = frame["id"]
        if frame.get("usage"):
            self.usage = frame["usage"]
        for choice in frame.get("choices", []):
            if choice["index"] != 0:
                raise ValueError("Multiple semantic choices are not permitted")
            delta = choice.get("delta", {})
            if delta.get("refusal"):
                raise ValueError("Astra refusal; semantic retry forbidden")
            if delta.get("content"):
                self.parts.append(delta["content"])
            if choice.get("finish_reason"):
                if self.finish and self.finish != choice["finish_reason"]:
                    raise ValueError("Conflicting streaming finish")
                self.finish = choice["finish_reason"]

    def result(self):
        if self.finish is None:
            raise ConnectionError("Stream ended without a terminal completion")
        if self.finish != "stop" or self.models != {MODEL}:
            raise ValueError(
                "Wrong model or non-stop semantic completion; no resampling"
            )
        return json.loads("".join(self.parts))


def model_completion(messages, schema, cap, output, client=None):
    import transport

    return transport.model_completion(messages, schema, cap, output, client)


def call_stage(
    runtime_input,
    stage,
    output,
    schema,
    validator,
    *,
    reports=None,
    cap=12000,
    client=None,
):
    LEGACY.SCORING.validate_runtime_input(runtime_input)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    prompt_path = ROOT / "prompts" / (stage + ".txt")
    prompt = prompt_path.read_text()
    import visual

    packet = visual.prepare(runtime_input)
    acquisition = None
    if stage != "p2_reconcile":
        scope = (
            reports["requested_components"]
            if stage in ("p1_proposal", "p1_independent")
            else ["orientation_alignment", "scale_perspective", "contact_integration"]
            if stage == "p2_geometry"
            else ["support_scenario", "access_usability", "orientation_alignment"]
            if stage == "p2_use"
            else list(SCORING.COMPONENT_WEIGHTS)
        )
        if stage in ("p1_proposal", "p1_independent") and set(scope) != set(
            schema["properties"]["components"]["required"]
        ):
            raise ValueError("Verifier acquisition scope differs from actual schema")
        acquisition = visual.acquire(
            runtime_input, stage, output / "acquisition", packet, scope, client
        )
    request = {
        "runtime_input": runtime_input,
        "stage": stage,
        "model": MODEL,
        "reasoning_effort": "high",
        "max_completion_tokens": cap,
        "route": "foundry_aws_gateway.llm.get_openai",
        "sdk_retries": 0,
        "max_transport_attempts": None,
        "timeout_seconds": 1800,
        "protocol_freeze_sha256": verify_freeze(),
        "prompt_sha256": sha(prompt_path),
        "schema_sha256": fingerprint(schema),
        "reports": reports,
        "images": {
            key: sha(runtime_input[key]) for key in ("generated_image", "twin_image")
        },
        "target_labels_withheld": True,
        "image_transform": packet["image_transform"],
        "visual_packet": packet,
        "independent_visual_acquisition": acquisition,
    }
    key = fingerprint(request)
    result_path = output / "result.json"
    if result_path.exists():
        old = json.loads(result_path.read_text())
        if old.get("fingerprint") != key or not old.get("ok"):
            raise ValueError(
                "Existing stage is failed or belongs to another frozen request"
            )
        if sha(old["chunks_path"]) != old["chunks_sha256"]:
            raise ValueError("Cached raw stream changed")
        collector = Collector()
        for line in Path(old["chunks_path"]).read_text().splitlines():
            collector.feed(json.loads(line))
        value = collector.result()
        validator(value)
        if value != old["observation"]:
            raise ValueError("Cached evidence differs from raw model response")
        return old
    write_json(output / "request.json", {**request, "fingerprint": key})
    write_json(output / "schema.json", schema)
    (output / "system_prompt.txt").write_text(prompt)
    messages = [{"role": "system", "content": prompt}]
    if stage == "p1_baseline":
        anchors, excluded = LEGACY.select_anchors(runtime_input)
        parts = [
            {
                "type": "text",
                "text": "Fixed development rubric exemplars. Current chair-tolerance rules override historical chair-pose interpretations. Judge the target independently.",
            }
        ]
        for anchor in anchors:
            parts += LEGACY.image_parts(anchor["guidance"], anchor["local_path"])
        messages.extend(
            [
                {"role": "user", "content": parts},
                {
                    "role": "assistant",
                    "content": "I will independently assess the target.",
                },
            ]
        )
        write_json(
            output / "exemplars.json", {"selected": anchors, "excluded": excluded}
        )
    payload = {
        key: runtime_input[key]
        for key in ("product_type", "scene_prompt", "image_stage")
    }
    if reports is not None:
        payload["fallible_model_reports"] = reports
        if stage in ("p1_proposal", "p1_independent"):
            payload["requested_components"] = reports["requested_components"]
    if acquisition is not None:
        payload["fallible_branch_acquisition"] = acquisition["record"]
    parts = [{"type": "text", "text": json.dumps(payload)}]
    parts += visual.parts(packet)
    messages.append({"role": "user", "content": parts})
    visual.check_request_budget(messages)
    value, receipt = model_completion(messages, schema, cap, output, client=client)
    validator(value)
    result = {
        "ok": True,
        "fingerprint": fingerprint(request),
        "observation": value,
        "visual_acquisition": acquisition,
        **receipt,
    }
    write_json(result_path, result)
    return result
