"""Customer/workflow config: HP Foundry text-to-image via Dylan's Pluto endpoint (image5_foundry / foundry_model_id=hp)."""

_BASE = "https://pluto-prod-dongshenga-dylan-hp-202-0-8000.jobs.colligo.dev"

ENDPOINT_URL = f"{_BASE}/v1/images/generate-async"
RESULT_URL_TEMPLATE = f"{_BASE}/jobs/result/{{job_id}}"
X_API_KEY = "colligo_testing"

# Not used with --no-upload; placeholders for module import.
S3_BUCKET = "foundry-hp-default-adobe-assets"
S3_ROOT_PREFIX = "hs_results"
AWS_REGION = "us-west-2"

ASPECT_RATIO_TO_SIZE = {
    "1:1":  (1536, 1536),
    "3:4":  (1152, 1536),
    "4:3":  (1536, 1152),
    "9:16": (1152, 2048),
    "16:9": (2048, 1152),
}


def aspect_to_size(ar: str) -> tuple[int, int]:
    if ar in ASPECT_RATIO_TO_SIZE:
        return ASPECT_RATIO_TO_SIZE[ar]
    raise ValueError(f"Unknown aspect ratio: {ar!r}. Known: {sorted(ASPECT_RATIO_TO_SIZE)}")


def build_payload(prompt: str, seed: int, aspect_ratio: str) -> dict:
    # Mirror the user's proven working request shape exactly (seeds array, no size -> default 1536^2).
    return {
        "model_version": "image5_foundry",
        "prompt": prompt,
        "seeds": [seed],
        "model_specific_payload": {"foundry_model_id": "hp"},
    }


def parse_result(resp: dict) -> dict:
    """Extract the bits we care about from a finished job response (same schema as humain)."""
    if "error_code" in resp:
        return {
            "status": "failed",
            "error_code": resp.get("error_code"),
            "error_message": resp.get("message"),
            "model_seed": None,
            "presigned_url": None,
            "image_id": None,
            "rewritten_prompt": None,
            "rewritten_negative_prompt": None,
        }

    outputs = resp.get("outputs") or []
    if not outputs or "image" not in outputs[0]:
        return {"status": "in_progress"}

    out = outputs[0]
    debug = resp.get("debugData", {}) or {}
    rr = debug.get("prompt_rewrite_result", {}) or {}
    forge = debug.get("prompt_forge_response", {}) or {}
    expanded_output = forge.get("expandedOutput") or []
    fallback_expanded = expanded_output[0] if expanded_output else None

    return {
        "status": "done",
        "model_seed": out.get("seed"),
        "presigned_url": out["image"].get("presignedUrl"),
        "image_id": out["image"].get("id"),
        "rewritten_prompt": rr.get("rewritten_prompt") or fallback_expanded,
        "rewritten_negative_prompt": rr.get("rewritten_negative_prompt"),
        "error_code": None,
        "error_message": None,
    }
