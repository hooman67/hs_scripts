"""Synthesize four frozen visual reviews into three unpromoted prompt candidates."""

import json
from pathlib import Path
import re
import time
from datetime import datetime, timezone
from importlib.metadata import version

import foundry_aws_gateway.llm

from prepare import ROOT, sha, write_json


def main():
    predecessor = ROOT / "synthesis"
    directory = ROOT / "synthesis_recovery"
    if not (predecessor / "config.json").exists() or (predecessor / "response.json").exists():
        raise ValueError("recovery requires the preserved unresolved predecessor, not a completed result")
    if (directory / "config.json").exists():
        raise ValueError("synthesis already attempted; do not silently resample")
    batches = []
    seen = set()
    for number in range(1, 5):
        source = ROOT / "batches" / f"batch{number}"
        package = json.loads((source / "input.json").read_text())
        config = json.loads((source / "config.json").read_text())
        if sha(source / "input.json") != config["input_sha256"]:
            raise ValueError("previously submitted batch input changed")
        raw = json.loads((source / "response.json").read_text())
        result = json.loads(raw["choices"][0]["message"]["content"])
        if result != json.loads((source / "analysis.json").read_text()):
            raise ValueError("parsed visual output differs from actual raw response")
        ids = [row["case_id"] for row in result["case_reviews"]]
        if len(ids) != 16 or set(ids) != set(config["case_ids"]) or seen.intersection(ids):
            raise ValueError("visual consultation case coverage is invalid")
        seen.update(ids)
        batches.append({
            "batch_id": number,
            "case_feedback_and_image_bindings": [
                {key: value for key, value in row.items()
                 if key != "refiner_plan_not_visual_truth"} for row in package["case_inputs"]],
            "historical_examples": package["historical_examples"],
            "analysis": result, "raw_response_sha256": sha(source / "response.json"),
        })
    if len(seen) != 64:
        raise ValueError("not all64 source cases were reviewed")
    inputs = {
        "original_visual_brief": (ROOT / "brief.txt").read_text(),
        "frozen_contracts": package["frozen_contracts"],
        "visual_batches": batches,
    }
    write_json(directory / "input.json", inputs)
    if sha(directory / "input.json") != sha(predecessor / "input.json"):
        raise ValueError("transport recovery must preserve exact original synthesis input")
    brief = (ROOT / "synthesis_brief.txt").read_text()
    write_json(directory / "config.json", {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": "gpt-6-astra", "route": "foundry_aws_gateway.llm.get_openai",
        "reasoning_effort": "high", "max_completion_tokens": 32768,
        "timeout_seconds": 1800, "transport_max_retries": 0, "concurrency": 1,
        "predecessor_attempt": str(predecessor),
        "predecessor_status": "Stopped locally after over20minutes without a response; upstream completion/usage unknown.",
        "semantic_resampling": False, "image_payload_count": 0,
        "input_sha256": sha(directory / "input.json"),
        "brief_sha256": sha(ROOT / "synthesis_brief.txt"),
        "sdk_versions": {name: version(name) for name in ("openai", "foundry-aws-gateway")},
    })
    started = time.monotonic()
    response = foundry_aws_gateway.llm.get_openai().with_options(
        max_retries=0, timeout=1800,
    ).chat.completions.create(
        model="gpt-6-astra", reasoning_effort="high", max_completion_tokens=32768,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": brief},
                  {"role": "user", "content": json.dumps(inputs, ensure_ascii=False)}],
    )
    (directory / "response.json").write_text(response.model_dump_json(indent=2) + "\n")
    choice = response.choices[0]
    body = choice.message.content or ""
    (directory / "output.txt").write_text(body)
    receipt = {
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "returned_model": response.model, "finish_reason": choice.finish_reason,
        "usage": response.usage.model_dump() if response.usage else None,
        "response_sha256": sha(directory / "response.json"),
    }
    write_json(directory / "receipt.json", receipt)
    if response.model != "gpt-6-astra" or choice.finish_reason != "stop" or not body:
        raise ValueError("incomplete or unexpected synthesis response")
    result = json.loads(body)
    if len(result["proposals"]) != 3 or len(result["historical_anchor_reconciliation"]) != 6:
        raise ValueError("Astra did not supply the requested proposal/anchor coverage")
    write_json(directory / "proposals.json", result)
    artifacts = []
    for proposal in result["proposals"]:
        proposal_id = proposal["id"]
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", proposal_id):
            raise ValueError("unsafe proposed artifact ID")
        for item in proposal["system_prompts"]:
            name = item["artifact_name"]
            if Path(name).name != name or not re.fullmatch(r"[a-zA-Z0-9_.-]+", name):
                raise ValueError("unsafe proposed prompt artifact name")
            path = ROOT / "proposals" / proposal_id / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x") as stream:
                stream.write(item["text"])
            artifacts.append({"proposal": proposal_id, "role": item["role"],
                              "path": str(path), "sha256": sha(path)})
    write_json(directory / "artifact_manifest.json", artifacts)
    print(json.dumps({"status": "complete", "proposal_count": 3,
                      "prompt_artifact_count": len(artifacts), **receipt}), flush=True)


if __name__ == "__main__":
    main()
