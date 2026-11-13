"""Actual Direct OpenAI Astra review of failed r1 observations and image evidence."""
from __future__ import annotations

import base64
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path

import foundry_aws_gateway.llm
from prepare import sha

ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent


def main():
    out = ROOT / "astra"
    out.mkdir(exist_ok=False)
    manifest = json.loads((ROOT / "calibration_manifest.json").read_text())
    inputs = []
    prompt = (ROOT / "astra_brief.md").read_text()
    paths = [ROOT / "calibration_manifest.json", R1 / "reviewed_rules.json",
             R1 / "prompts/baseline.md", R1 / "prompts/compact.md",
             R1 / "observation_schema.json", R1 / "scoring.py",
             R1 / "astra/attempt_1/output.md"]
    for path in paths:
        prompt += f"\n\n## Exact source: {path}\n\n{path.read_text()}"
        inputs.append({"path": str(path), "sha256": sha(path)})
    for case in manifest["cases"]:
        prompt += f"\n\n## ACTUAL R1 observations: {case['id']} ({case['role']})\n"
        for stage in ("baseline", "compact"):
            path = R1 / "evaluation/runs/v3_1" / case["id"] / stage / "response.json"
            raw = json.loads(path.read_text())
            prompt += f"\n### {stage}; returned {raw['model']}\n{raw['choices'][0]['message']['content']}\n"
            inputs.append({"path": str(path), "sha256": sha(path)})
    (out / "input.md").write_text(prompt)
    content = [{"type": "text", "text": prompt}]
    images = []
    for case in manifest["cases"]:
        for key in ("generated_image", "twin_image"):
            image = case[key]
            path = Path(image["local_path"])
            if sha(path) != image["sha256"]:
                raise ValueError("Frozen source-image hash changed")
            content += [
                {"type": "text", "text": f"{case['id']} / {case['role']} / {key}"},
                {"type": "image_url", "image_url": {
                    "url": "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode(),
                    "detail": "high"}},
            ]
            images.append({"case": case["id"], "kind": key, **image})
    config = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "route": "foundry_aws_gateway.llm.get_openai (Direct OpenAI)",
        "model": "gpt-6-astra", "reasoning_effort": "high", "max_completion_tokens": 24000,
        "timeout_seconds": 600, "transport_max_retries": 8, "concurrency": 1,
        "semantic_resampling": False, "input_sha256": sha(out / "input.md"),
        "sources": inputs, "images": images, "image_transform": "none; exact original bytes",
        "packages": {p: importlib.metadata.version(p) for p in ("foundry-aws-gateway", "openai")},
    }
    (out / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    try:
        client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=8, timeout=600)
        response = client.chat.completions.create(
            model="gpt-6-astra", reasoning_effort="high", max_completion_tokens=24000,
            messages=[{"role": "user", "content": content}])
        (out / "response.json").write_text(response.model_dump_json(indent=2))
        choice = response.choices[0]
        (out / "output.md").write_text(choice.message.content or "")
        meta = {"finished_utc": datetime.now(timezone.utc).isoformat(),
                "model_returned": response.model, "finish_reason": choice.finish_reason,
                "usage": response.usage.model_dump() if response.usage else None}
        (out / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
        if response.model != "gpt-6-astra" or choice.finish_reason != "stop" or not choice.message.content:
            raise RuntimeError("Incomplete or unexpected-model consultation")
        print(json.dumps(meta))
    except Exception as exc:
        (out / "error.json").write_text(json.dumps({
            "error_type": type(exc).__name__, "status_code": getattr(exc, "status_code", None),
            "finished_utc": datetime.now(timezone.utc).isoformat(),
        }, indent=2) + "\n")
        raise SystemExit(type(exc).__name__)


if __name__ == "__main__":
    main()
