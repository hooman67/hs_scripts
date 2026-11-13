import hashlib

import pytest

from merge_consensus_v2 import require_exact_ids, validate_independent_binding


def test_exact_ids_rejects_missing_and_extra():
    with pytest.raises(ValueError, match="missing=.*b.*extra=.*c"):
        require_exact_ids("source", {"a", "c"}, {"a", "b"})


def test_independent_binding_checks_all_five_runtime_fields_and_trigger(tmp_path):
    generated = tmp_path / "scene.png"
    twin = tmp_path / "twin.png"
    generated.write_bytes(b"scene")
    twin.write_bytes(b"twin")
    prompt = "original prompt"
    identity = {
        "generated_image_sha256": hashlib.sha256(b"scene").hexdigest(),
        "twin_image_sha256": hashlib.sha256(b"twin").hexdigest(),
        "scene_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "product_type": "laptop",
        "image_stage": "scene_generation",
        "input_identity_sha256": "identity-hash",
    }
    independent = {
        "runtime_input": {"generated_image": str(generated), "twin_image": str(twin), "product_type": "laptop", "scene_prompt": prompt, "image_stage": "scene_generation"},
        "images": {"generated_image": {"sha256": identity["generated_image_sha256"]}, "twin_image": {"sha256": identity["twin_image_sha256"]}},
        "source_trigger": {"sha256": "trigger-hash"},
        "proposal_text_codes_severities_prior_verdicts_comments_passed": False,
    }
    validated = validate_independent_binding("case", independent, {"input_identity": identity}, "trigger-hash")
    assert validated["source_input_identity_sha256"] == "identity-hash"
    independent["runtime_input"]["scene_prompt"] = "changed prompt"
    with pytest.raises(ValueError, match="does not match"):
        validate_independent_binding("case", independent, {"input_identity": identity}, "trigger-hash")


def test_independent_binding_rejects_wrong_trigger(tmp_path):
    generated = tmp_path / "scene.png"; generated.write_bytes(b"scene")
    twin = tmp_path / "twin.png"; twin.write_bytes(b"twin")
    prompt = "p"
    identity = {"generated_image_sha256": hashlib.sha256(b"scene").hexdigest(), "twin_image_sha256": hashlib.sha256(b"twin").hexdigest(), "scene_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "product_type": "printer", "image_stage": "scene_generation", "input_identity_sha256": "identity"}
    independent = {"runtime_input": {"generated_image": str(generated), "twin_image": str(twin), "product_type": "printer", "scene_prompt": prompt, "image_stage": "scene_generation"}, "images": {"generated_image": {"sha256": identity["generated_image_sha256"]}, "twin_image": {"sha256": identity["twin_image_sha256"]}}, "source_trigger": {"sha256": "wrong"}, "proposal_text_codes_severities_prior_verdicts_comments_passed": False}
    with pytest.raises(ValueError, match="not bound"):
        validate_independent_binding("case", independent, {"input_identity": identity}, "expected")
