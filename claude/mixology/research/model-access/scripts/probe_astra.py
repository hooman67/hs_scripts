"""Verify Astra vision access on the synthetic research input; never persist credentials."""
import base64
import hashlib
import json
import logging
import os
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

from foundry_aws_gateway import llm


def main():
    os.umask(0o077)
    logging.disable(logging.CRITICAL)
    topic = Path(__file__).resolve().parents[1]
    target = topic / "data" / "astra_probe_2026-10-19.json"
    if target.exists():
        raise SystemExit(f"Probe record already exists: {target}")
    reference = topic / "data" / "synthetic_reference.png"
    raw = reference.read_bytes()
    prompt = (
        "Inspect this synthetic reference for an image-restyling experiment. "
        "Return JSON with subject, main_color, handle_side, and three features "
        "that a style edit should preserve. Keep the answer concise."
    )
    record = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "requested_model": "gpt-6-astra",
        "endpoint": "https://api.openai.com/v1/responses",
        "auth": "foundry_aws_gateway.llm.get_openai via injected Pluto token",
        "reference": str(reference),
        "reference_sha256": hashlib.sha256(raw).hexdigest(),
        "prompt": prompt,
        "max_output_tokens": 1500,
        "reasoning_effort": "low",
        "versions": {name: version(name) for name in ("foundry-aws-gateway", "openai")},
    }
    started = time.monotonic()
    try:
        client = llm.get_openai().with_options(timeout=120, max_retries=0)
        response = client.responses.create(
            model=record["requested_model"],
            reasoning={"effort": "low"},
            max_output_tokens=1500,
            input=[{"role": "user", "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": "data:image/png;base64," + base64.b64encode(raw).decode()},
            ]}],
        )
        record.update(
            ok=response.status == "completed" and bool(response.output_text),
            returned_model=response.model,
            status=response.status,
            request_id=response._request_id,
            response_id=response.id,
            output_text=response.output_text,
            usage=response.usage.model_dump(mode="json") if response.usage else None,
        )
    except Exception as exc:
        # Do not persist exception bodies, headers, or objects that could contain credentials.
        record.update(ok=False, error_type=type(exc).__name__, status_code=getattr(exc, "status_code", None))
    record["elapsed_seconds"] = round(time.monotonic() - started, 2)
    target.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
    return 0 if record["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
