import base64
import io
import json
from pathlib import Path

from openai import OpenAI

IMAGE_MODEL = "gpt-image-2.5-sunburst-2026-09-08"
TEXT_MODEL = "gpt-6-astra"
_PROMPTS = Path(__file__).parent / "prompts"


def load_prompt(name: str) -> str:
    return (_PROMPTS / f"{name}.txt").read_text()


def _vault_key() -> str:
    from platforms.dev_tools.vault import VaultClient

    key = VaultClient().query_secret("dme_colligo/services/foundry/ethos/openai_platform_key").get("api_key")
    if not isinstance(key, str) or not key.strip():
        raise RuntimeError("Vault secret has no api_key")
    return key.strip()


class OpenAIClient:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=_vault_key(), max_retries=0, timeout=540)

    def chat_json(self, system: str, text: str, images: list[tuple[str, bytes]], schema: dict) -> dict:
        content = [{"type": "text", "text": text}] + [
            {"type": "image_url", "image_url": {"url": f"data:{m};base64,{base64.b64encode(d).decode()}",
                                                "detail": "high"}} for m, d in images]
        resp = self.client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[{"role": "developer", "content": system}, {"role": "user", "content": content}],
            response_format={"type": "json_schema",
                             "json_schema": {"name": "result", "strict": True, "schema": schema}},
            max_completion_tokens=16384, store=False)
        choice = resp.choices[0]
        if choice.finish_reason != "stop" or not choice.message.content:
            raise RuntimeError(f"Astra incomplete: {choice.finish_reason}")
        return json.loads(choice.message.content)

    def edit_image(self, prompt: str, images: list[tuple[str, bytes]], size: str, mask: bytes | None = None) -> bytes:
        files = [(f"image{i}.{m.split('/')[1]}", io.BytesIO(d), m) for i, (m, d) in enumerate(images, 1)]
        extra = {"mask": ("mask.png", io.BytesIO(mask), "image/png")} if mask else {}
        resp = self.client.images.edit(model=IMAGE_MODEL, image=files, prompt=prompt, n=1, size=size,
                                       quality="high", output_format="png", background="opaque",
                                       **extra)
        return base64.b64decode(resp.data[0].b64_json)
