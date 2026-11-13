from pathlib import Path
import json
import sys
import foundry_aws_gateway.llm

root = Path(__file__).resolve().parent
prompt = (root / "astra_task.md").read_text()
client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=2, timeout=600.0)
response = client.chat.completions.create(
    model="gpt-6-astra",
    messages=[{"role": "user", "content": prompt}],
    reasoning_effort="high",
    max_completion_tokens=24000,
)
choice = response.choices[0]
(root / "astra_output.md").write_text(choice.message.content or "")
(root / "response_metadata.json").write_text(json.dumps({
    "model": response.model,
    "finish_reason": choice.finish_reason,
    "total_tokens": getattr(response.usage, "total_tokens", None),
    "content_bytes": len((choice.message.content or "").encode()),
    "refusal": getattr(choice.message, "refusal", None),
}, indent=2) + "\n")
if not choice.message.content:
    raise SystemExit(2)
