"""Customer/workflow config: Humain text-to-image via Foundry/Colligo endpoint."""

ENDPOINT_URL = "https://gen-foundry-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/v1/images/generate-async"
RESULT_URL_TEMPLATE = "https://firefly-dev-eso851255.adobe.io/jobs/result/{job_id}"
X_API_KEY = "colligo_testing"

S3_BUCKET = "foundry-humain-default-adobe-assets"
S3_ROOT_PREFIX = "hs_results"
AWS_REGION = "us-west-2"

ASPECT_RATIO_TO_SIZE = {
    "1:1":  (2048, 2048),
    "3:4":  (1536, 2048),
    "4:3":  (2048, 1536),
    "9:16": (1152, 2048),
    "16:9": (2048, 1152),
    "2:3":  (1408, 2112),
    "3:2":  (2112, 1408),
}


def aspect_to_size(ar: str) -> tuple[int, int]:
    if ar in ASPECT_RATIO_TO_SIZE:
        return ASPECT_RATIO_TO_SIZE[ar]
    raise ValueError(f"Unknown aspect ratio: {ar!r}. Known: {sorted(ASPECT_RATIO_TO_SIZE)}")


def build_payload(prompt: str, seed: int, aspect_ratio: str) -> dict:
    w, h = aspect_to_size(aspect_ratio)
    return {
        "seed": seed,
        "referenceBlobs": [],
        "modelVersion": "image5_foundry",
        "prompt": prompt,
        "model_specific_payload": {"foundry_model_id": "humain"},
        "size": {"height": h, "width": w},
    }


def parse_result(resp: dict) -> dict:
    """Extract the bits we care about from a finished job response.

    Returns: dict with status, model_seed, presigned_url, image_id,
    rewritten_prompt, rewritten_negative_prompt, error_code, error_message.
    """
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
