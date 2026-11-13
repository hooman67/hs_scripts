"""One bounded Direct OpenAI Astra product-judge consultation; no model fallback."""
from __future__ import annotations

import base64
import hashlib
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path

import foundry_aws_gateway.llm

ROOT = Path(__file__).resolve().parent
V3 = ROOT.parent / "v3"
V2 = ROOT.parent / "v2"
DOC = Path("/home/colligo/hs_scripts/claude/monitor/ASTRA_FOUNDRY_GATEWAY_HANDOFF.md")
GATEWAY_DOC = Path("/home/colligo/colligo/managed_services/services/firefly/foundry/"
                   "libs/aws_gateway_client/README.md")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    out = ROOT / "astra" / "attempt_1"
    out.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((ROOT / "sources/manifest.json").read_text())
    paths = [
        V2 / "system_prompt.md", V3 / "system_prompt.md",
        V3 / "observation_schema.json", V3 / "scoring.py",
        V3 / "experiments/two_pass/policy.json",
        V3 / "experiments/consensus_policy/policy.json",
        V3 / "experiments/verify_additions/system_prompt.md",
        V3 / "experiments/independent_component_check/system_prompt.md",
    ]
    prompt = (ROOT / "astra_brief.md").read_text()
    prompt += "\n\n## Exact live source manifest\n" + json.dumps(manifest, indent=2)
    for path in paths:
        prompt += f"\n\n## Frozen contract: {path}\n\n{path.read_text()}"
    (out / "input.md").write_text(prompt)
    content = [{"type": "text", "text": prompt}]
    image_inputs = []
    for case in manifest["cases"]:
        content.append({"type": "text", "text": f"ACTUAL ANCHOR: {case['id']}, {case['variant']}"})
        for kind in ("generated_image", "twin_image"):
            image = case[kind]
            path = Path(image["local_path"])
            if sha(path) != image["sha256"]:
                raise ValueError("Source image hash changed")
            content.extend([
                {"type": "text", "text": kind},
                {"type": "image_url", "image_url": {
                    "url": "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode(),
                    "detail": "high"}},
            ])
            image_inputs.append({"case": case["id"], "kind": kind, **image})
    config = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "route": "foundry_aws_gateway.llm.get_openai (Direct OpenAI)",
        "model": "gpt-6-astra", "reasoning_effort": "high",
        "max_completion_tokens": 24000, "timeout_seconds": 600, "max_retries": 8,
        "concurrency": 1, "image_transform": "none; exact original JPEG bytes",
        "input_sha256": sha(out / "input.md"), "images": image_inputs,
        "sources": [{"path": str(p), "sha256": sha(p)} for p in paths + [DOC, GATEWAY_DOC]],
        "packages": {p: importlib.metadata.version(p) for p in ("openai", "foundry-aws-gateway")},
    }
    (out / "config.json").write_text(json.dumps(config, indent=2))
    try:
        client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=8, timeout=600)
        response = client.chat.completions.create(
            model=config["model"], reasoning_effort="high", max_completion_tokens=24000,
            messages=[{"role": "user", "content": content}],
        )
        (out / "response.json").write_text(response.model_dump_json(indent=2))
        choice = response.choices[0]
        (out / "output.md").write_text(choice.message.content or "")
        metadata = {"finished_utc": datetime.now(timezone.utc).isoformat(),
                    "model_returned": response.model, "finish_reason": choice.finish_reason,
                    "usage": response.usage.model_dump() if response.usage else None}
        (out / "metadata.json").write_text(json.dumps(metadata, indent=2))
        if response.model != "gpt-6-astra" or choice.finish_reason != "stop" or not choice.message.content:
            raise RuntimeError("Incomplete, empty or unexpected-model Astra response")
        print(json.dumps(metadata))
    except Exception as exc:
        (out / "error.json").write_text(json.dumps({
            "error_type": type(exc).__name__, "status_code": getattr(exc, "status_code", None),
            "finished_utc": datetime.now(timezone.utc).isoformat(),
        }, indent=2))
        raise SystemExit(type(exc).__name__)


if __name__ == "__main__":
    main()
