from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

import endpoint


class CapturingExecutor:
    def __init__(self) -> None:
        self.calls = []

    def submit(self, function, *args):
        self.calls.append((function, args))
        return None


def test_catalog_is_exact_fixed_four_by_four_contract():
    catalog = endpoint.catalog()
    assert catalog["generator"] == "GPT Image 2.5 / single reference / no grading"
    assert catalog["rewriterVersion"] == (
        "Adobe-Firefly/foundry#4349 / 8c358bc7989c + surface-shape-r1 / "
        "unified-blue-scale-v20-surface-shape-r1"
    )
    twins = {item["id"]: item for item in catalog["digitalTwins"]}
    assert set(twins) == {"cashmere_x", "elitebook_13", "tassel", "adf_printer"}
    assert all(len(item["cameras"]) == 4 for item in twins.values())
    assert sum(len(item["cameras"]) for item in twins.values()) == 16
    assert catalog["candidateLineage"]["configSha256"] == endpoint.CONFIG_SHA256


def test_imports_and_models_are_pinned_to_isolated_runtime():
    runtime = endpoint.RUNTIME.resolve()
    assert Path(endpoint.pipeline.__file__).resolve().is_relative_to(runtime)
    assert Path(endpoint.geometry.__file__).resolve().is_relative_to(runtime)
    assert endpoint.pipeline.PIPELINE_VERSION == endpoint.PIPELINE_VERSION
    assert endpoint.IMAGE_MODEL == endpoint.EXPECTED_IMAGE_MODEL
    assert endpoint.TEXT_MODEL == endpoint.EXPECTED_TEXT_MODEL
    assert endpoint.PROVIDER_PREFLIGHT["ready"] is True
    assert endpoint.PROVIDER_PREFLIGHT["modelRequestMade"] is False
    endpoint.verify_files()


def test_generation_is_disabled_by_default():
    client = TestClient(endpoint.app)
    credentials = client.get("/api/credentials").json()
    response = client.post(
        "/api/generate",
        json={"digitalTwinId": "cashmere_x", "cameraId": "Front_CloseUp", "prompt": "Round cafe table."},
        headers={"x-hp12-csrf": credentials["csrfToken"]},
    )
    assert response.status_code == 503
    assert credentials["generationEnabled"] is False


def test_valid_request_queues_exact_contract_without_executing(monkeypatch, tmp_path):
    executor = CapturingExecutor()
    monkeypatch.setattr(endpoint, "_generation_enabled", True)
    monkeypatch.setattr(endpoint, "_executor", executor)
    monkeypatch.setattr(endpoint, "JOBS", tmp_path / "jobs")
    monkeypatch.setattr(endpoint, "_expected_origin", "http://127.0.0.1:8137")
    endpoint.JOBS.mkdir()
    client = TestClient(endpoint.app)
    csrf = client.get("/api/credentials").json()["csrfToken"]
    payload = {
        "digitalTwinId": "adf_printer",
        "cameraId": "Front_Right_CloseUp",
        "prompt": "A printer on an oval cabinet top.",
    }
    response = client.post(
        "/api/generate",
        json=payload,
        headers={"Origin": "http://127.0.0.1:8137", "x-hp12-csrf": csrf},
    )
    assert response.status_code == 202
    submitted = response.json()
    assert set(submitted) == {"jobId", "statusUrl", "imageUrl", "debugUrl", "candidateId", "configSha256"}
    assert submitted["configSha256"] == endpoint.CONFIG_SHA256
    assert len(executor.calls) == 1
    _, args = executor.calls[0]
    assert args[1] == payload
    status = client.get(submitted["statusUrl"]).json()
    assert status["done"] is False
    assert status["stages"]["scene"]["status"] == "queued"
    assert status["stages"]["ibl"]["status"] == "skipped"
    assert status["candidateLineage"]["configSha256"] == endpoint.CONFIG_SHA256


def test_request_rejects_unknown_fields_before_queue(monkeypatch):
    monkeypatch.setattr(endpoint, "_generation_enabled", True)
    client = TestClient(endpoint.app)
    csrf = client.get("/api/credentials").json()["csrfToken"]
    response = client.post(
        "/api/generate",
        json={
            "digitalTwinId": "cashmere_x",
            "cameraId": "Front_CloseUp",
            "prompt": "Round cafe table.",
            "size": "1216x912",
        },
        headers={"x-hp12-csrf": csrf},
    )
    assert response.status_code == 422
