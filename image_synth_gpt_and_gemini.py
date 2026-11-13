import base64
import io
import argparse
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from os import environ
from pathlib import Path

_PIL_IMPORT_ERROR: Exception | None 
try:
    from PIL import Image  # type: ignore[import-not-found]
except ModuleNotFoundError as e:
    Image = None  # type: ignore[assignment]
    _PIL_IMPORT_ERROR = e
else:
    _PIL_IMPORT_ERROR = None

# --- GPT (Azure OpenAI Images) config ---
GPT_MODEL_ID = "gpt-image-1.5"
AZURE_OPENAI_BASE_URL = "https://camp-azr14080-rnig4.cognitiveservices.azure.com/openai/v1/"
AZURE_OPENAI_TOKEN_ENV = "AZURE_OPENAI_TOKEN"

# --- Gemini (Vertex AI) config ---
GEMINI_PROJECT_ID = environ.get("GEMINI_PROJECT_ID", "adbe-gcp0805")
GEMINI_LOCATION = environ.get("GEMINI_LOCATION", "global")
GEMINI_MODEL_ID = environ.get("GEMINI_MODEL_ID", "gemini-3-pro-image-preview")

_gpt_client = None
_gemini_client = None


def _parse_size_to_max_side(size: str, *, default_max_side: int = 1536) -> int:
    """
    Parse strings like "1536x1024" into max(width, height).
    If parsing fails, return default_max_side.
    """
    m = re.match(r"^\s*(\d+)\s*[xX]\s*(\d+)\s*$", size or "")
    if not m:
        return default_max_side
    return max(int(m.group(1)), int(m.group(2)))


def _get_gpt_client():
    global _gpt_client
    if _gpt_client is not None:
        return _gpt_client
    # Import lazily so running with --model=gemini doesn't require openai installed.
    from openai import OpenAI  # type: ignore[import-not-found]

    token = environ[AZURE_OPENAI_TOKEN_ENV]
    _gpt_client = OpenAI(api_key=token, base_url=AZURE_OPENAI_BASE_URL)
    return _gpt_client


def _get_gemini_client():
    global _gemini_client
    if _gemini_client is not None:
        return _gemini_client
    # Import lazily so running with --model=gpt doesn't require google-genai installed.
    from google import genai  # type: ignore[import-not-found]

    _gemini_client = genai.Client(vertexai=True, project=GEMINI_PROJECT_ID, location=GEMINI_LOCATION)
    return _gemini_client


def downscale(img, max_side: int = 1536):
    """Downscale while keeping aspect ratio to reduce tokens/cost."""
    w, h = img.size
    scale = max(w, h) / max_side
    if scale <= 1:
        return img
    new_w, new_h = int(w / scale), int(h / scale)
    return img.resize((new_w, new_h), Image.LANCZOS)


def generate_image_with_prompt_gpt(img, prompt: str, size: str):
    """
    GPT image edit path (Azure OpenAI images API).
    `size` is passed through to the API (e.g. "1536x1024").
    """
    max_side = _parse_size_to_max_side(size, default_max_side=1536)
    img = downscale(img, max_side=max_side)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    buf.name = "image.png"
    image_files = [buf]
    client = _get_gpt_client()
    response = client.images.edit(
        model=GPT_MODEL_ID,
        image=image_files,
        prompt=prompt,
        n=1,
        size=size,
    )
    image_data = response.data[0].b64_json
    return Image.open(io.BytesIO(base64.b64decode(image_data)))


def generate_image_with_prompt_gemini(img, prompt: str, size: str):
    """
    Gemini (Vertex AI) path.
    Note: Gemini image generation doesn't currently accept an explicit output `size` the same
    way GPT does; we use `size` to choose how aggressively to downscale the *input* reference
    image (max side = max(width,height) parsed from `size`).
    """
    # Imported lazily to avoid dependency when using GPT.
    from google.genai import types  # type: ignore[import-not-found]

    max_side = _parse_size_to_max_side(size, default_max_side=1920)
    img = downscale(img, max_side=max_side)

    img_to_bytes = io.BytesIO()
    img.save(img_to_bytes, format="PNG")
    contents = [
        types.Part.from_bytes(data=img_to_bytes.getvalue(), mime_type="image/png"),
        prompt,
    ]
    client = _get_gemini_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL_ID,
        contents=contents,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )
    return Image.open(io.BytesIO(response.candidates[0].content.parts[0].inline_data.data))


def _normalize_prompt_line(line: str) -> str:
    s = line.strip()
    if not s:
        return ""
    if s.lower().startswith("note"):
        return ""
    # Strip leading numbering like "1) " or "23) "
    s = re.sub(r"^\s*\d+\)\s*", "", s)
    return s.strip()


def load_prompts(prompts_path: Path) -> list[str]:
    lines = prompts_path.read_text(encoding="utf-8").splitlines()
    prompts: list[str] = []
    for line in lines:
        p = _normalize_prompt_line(line)
        if p:
            prompts.append(p)
    return prompts


def _safe_stem(i: int, prompt: str, max_len: int = 80) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", prompt).strip("_")
    if len(slug) > max_len:
        slug = slug[:max_len].rstrip("_")
    return f"{i:04d}_{slug or 'prompt'}"


def generate_one(
    *,
    ref_image_bytes: bytes,
    prompt: str,
    size: str,
    model: str,
    out_dir: Path,
    index: int,
    retries: int = 4,
) -> Path:
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            if Image is None:
                raise _PIL_IMPORT_ERROR  # type: ignore[misc]
            img = Image.open(io.BytesIO(ref_image_bytes))
            if model == "gpt":
                out_img = generate_image_with_prompt_gpt(img, prompt, size=size)
            elif model == "gemini":
                out_img = generate_image_with_prompt_gemini(img, prompt, size=size)
            else:
                raise ValueError(f"Unknown model: {model!r}")
            stem = _safe_stem(index, prompt)
            out_path = out_dir / f"{stem}.png"
            out_img.save(out_path)
            # (out_dir / f"{stem}.txt").write_text(prompt + "\n", encoding="utf-8")
            return out_path
        except Exception as e:
            last_err = e
            if attempt >= retries:
                break
            sleep_s = min(30.0, (2.0**attempt)) + (0.1 * (attempt + 1))
            time.sleep(sleep_s)
    raise RuntimeError(f"Failed after {retries + 1} attempts. prompt={prompt!r}") from last_err


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate one image per prompt using a reference image.")
    parser.add_argument(
        "--ref-image",
        type=str,
        required=True,
        help="Path to the reference image of the trimmer (used as the edit base).",
    )
    parser.add_argument(
        "--prompts-file",
        type=str,
        required=True,
        help="Path to a text file containing one prompt per line (numbering like '1)' is OK).",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        required=True,
        help="Directory to save generated images into.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt",
        choices=["gpt", "gemini"],
        help="Which backend to use: 'gpt' (Azure OpenAI) or 'gemini' (Vertex AI).",
    )
    parser.add_argument(
        "--size",
        type=str,
        default=None,
        help=(
            "For GPT: output size passed to the Images API (e.g. 1536x1024). "
            "For Gemini: used to set max downscale side for the reference image (e.g. 1920x1088)."
        ),
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=4,
        help="How many requests to send simultaneously.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional max number of prompts to run (0 = all).",
    )
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="Optional starting prompt index (0-based) to resume runs.",
    )
    args = parser.parse_args()

    if Image is None:
        raise SystemExit(
            "Missing dependency: Pillow.\n"
            "Install with: `python -m pip install pillow`\n"
            f"Original error: {_PIL_IMPORT_ERROR}"
        )

    ref_path = Path(args.ref_image).expanduser()
    prompts_path = Path(args.prompts_file).expanduser()
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.size is None:
        args.size = "1536x1024" if args.model == "gpt" else "1920x1088"

    prompts = load_prompts(prompts_path)
    if args.start:
        prompts = prompts[args.start:]
    if args.limit and args.limit > 0:
        prompts = prompts[: args.limit]
    if not prompts:
        raise SystemExit("No prompts found after filtering.")

    ref_bytes = ref_path.read_bytes()
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"Loaded {len(prompts)} prompts. Concurrency={args.concurrency}. RunID={run_id}")

    failures: list[tuple[int, str, str]] = []
    with ThreadPoolExecutor(max_workers=max(1, int(args.concurrency))) as ex:
        futures = {}
        for i, prompt in enumerate(prompts):
            global_index = args.start + i
            fut = ex.submit(
                generate_one,
                ref_image_bytes=ref_bytes,
                prompt=prompt,
                size=args.size,
                model=args.model,
                out_dir=out_dir,
                index=global_index,
            )
            futures[fut] = (global_index, prompt)

        for fut in as_completed(futures):
            idx, prompt = futures[fut]
            try:
                out_path = fut.result()
                print(f"[OK] {idx}: {out_path.name}")
            except Exception as e:
                msg = str(e)
                failures.append((idx, prompt, msg))
                print(f"[FAIL] {idx}: {msg}")

    if failures:
        fail_path = out_dir / f"failures_{run_id}.jsonl"
        with fail_path.open("w", encoding="utf-8") as f:
            for idx, prompt, err in failures:
                f.write(f'{{"index":{idx},"prompt":{prompt!r},"error":{err!r}}}\n')
        print(f"Done with failures. See: {fail_path.resolve()}")
    else:
        print("Done. All prompts generated successfully.")
