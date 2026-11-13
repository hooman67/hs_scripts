from __future__ import annotations

import copy
import hashlib
import io

import httpx
import pytest

from recovery.complete160 import audit_native
from recovery.complete160 import completed_report as report
from recovery.complete160 import image_recovery as recovery


def completed_document():
    original = recovery.load(recovery.ROOT / "text/exports/prompts_all.json")
    baseline = recovery.load(recovery.ROOT / "baseline/outputs/all_160/prompts_all_160.json")
    prior = {prompt["prompt_key"]: prompt for prompt in original["prompts"]}
    return {"prompts": [copy.deepcopy(prior.get(prompt["prompt_key"], prompt)) for prompt in baseline["prompts"]]}


def test_missing_queue_preserves79_and_includes_exact_original503(monkeypatch):
    document = completed_document()
    real_load = recovery.load
    monkeypatch.setattr(
        recovery,
        "load",
        lambda path: document if path == recovery.HERE / "exports/prompts_all_160.json" else real_load(path),
    )
    rows = recovery.selected_rows()
    assert len(rows) == len({row["row_id"] for row in rows}) == 81
    assert [row["queue_position"] for row in rows] == list(range(1, 82))
    assert "cashmere__laptop_FrontLeftMedium::p6" in {row["row_id"] for row in rows}
    old = real_load(recovery.ROOT / "text/exports/prompts_all.json")["prompts"]
    original_keys = {prompt["prompt_key"] for prompt in old}
    assert len({row["row_id"] for row in rows} & original_keys) == 1
    next(prompt for prompt in document["prompts"] if prompt["prompt_key"] in original_keys)["text"] += " edited"
    with pytest.raises(ValueError, match="original accepted prompt"):
        recovery.selected_rows()


@pytest.mark.parametrize(
    "error,expected",
    [
        ("APIStatusError: Error code: 503 - service unavailable", True),
        ("APITimeoutError: request timed out", True),
        ("AuthenticationError: Error code: 401", False),
        ("ValueError: image settings changed", False),
    ],
)
def test_only_confirmed_transient_native_failures_allow_new_jobs(error, expected):
    assert recovery.retryable_record({"error": error}) is expected


def test_full_native_transient_replacement_keeps_failed_attempt(tmp_path, monkeypatch):
    monkeypatch.setattr(recovery, "HERE", tmp_path)
    monkeypatch.setattr(recovery.time, "sleep", lambda _: None)
    calls = []
    row = {"row_id": "bank::p1", "row_slug": "bank__p1"}

    def process(run, *args):
        calls.append(run)
        paths = recovery.scene_runner.paths(run, row)
        record = {
            "status": "failed" if len(calls) == 1 else "done",
            "job_id": str(len(calls)),
            "error": "APIStatusError: Error code: 503",
            "image_sha256": "image",
        }
        recovery.write(paths["job"], {"jobId": record["job_id"]})
        recovery.write(paths["record"], record)
        return record

    monkeypatch.setattr(recovery.scene_runner, "process", process)
    result = recovery.render(row, {"catalog_sha256": "catalog", "run_sha256": "run", "lineage": {}})
    assert result["attempts"] == 2
    assert calls[0] != calls[1]
    assert recovery.load(recovery.scene_runner.paths(calls[0], row)["record"])["status"] == "failed"


def test_poll_uncertainty_resumes_same_job_not_new_paid_attempt(tmp_path, monkeypatch):
    monkeypatch.setattr(recovery, "HERE", tmp_path)
    monkeypatch.setattr(recovery.time, "sleep", lambda _: None)
    monkeypatch.setattr(recovery, "listener_owned", lambda _: True)
    recovery.write(tmp_path / "service_ownership.json", {"pid": 42})
    row = {"row_id": "bank::p1", "row_slug": "bank__p1"}
    calls = []

    def process(run, *args):
        calls.append(run)
        paths = recovery.scene_runner.paths(run, row)
        if len(calls) == 1:
            recovery.write(paths["job"], {"jobId": "one-existing-job"})
            raise httpx.ReadTimeout("Temporary GET failure")
        record = {"status": "done", "job_id": "one-existing-job", "image_sha256": "image"}
        recovery.write(paths["record"], record)
        return record

    monkeypatch.setattr(recovery.scene_runner, "process", process)
    result = recovery.render(row, {"catalog_sha256": "catalog", "run_sha256": "run", "lineage": {}})
    assert result["attempts"] == 1
    assert calls[0] == calls[1]


def test_interrupted_unsaved_post_never_replayed(tmp_path, monkeypatch):
    monkeypatch.setattr(recovery, "HERE", tmp_path)
    row = {"row_id": "bank::p1", "row_slug": "bank__p1"}
    run = tmp_path / "image_attempts/bank__p1/attempt_0001"
    recovery.write(run / "journals/events.jsonl", b'{"event":"submit_started"}\n')
    with pytest.raises(RuntimeError, match="Interrupted image submission"):
        recovery.render(row, {})


def test_parameterized_audit_accepts_real_frozen_native_input_and_raw_png(tmp_path, monkeypatch):
    monkeypatch.setattr(recovery, "HERE", tmp_path)
    monkeypatch.setattr(recovery, "ENDPOINT", recovery.ROOT / "endpoint_pr4523")
    prompt = recovery.load(recovery.ROOT / "text/exports/prompts_all.json")["prompts"][0]
    audit = audit_native.audit_one(prompt, recovery.ROOT / "run")
    assert len(audit["native_calls"]) == 4
    assert audit["new_model_calls_for_audit"] == 0


def test_merge_changes_only81_failed_slots_and_rejects_success_redraw():
    before = recovery.load(recovery.ROOT / "public/gallery/data.json")
    document = completed_document()
    document["bank_audit"] = {group["id"]: {} for group in before["groups"]}
    replacements = {
        card["prompt_key"]: {"prompt_key": card["prompt_key"], "status": "done"}
        for group in before["groups"]
        for card in group["experiments"][1]["cards"]
        if card["status"] != "done"
    }
    after = report.merge_data(before, document, replacements)
    assert after["image_count"] == 320
    for old_group, group in zip(before["groups"], after["groups"], strict=True):
        assert group["experiments"][0] == old_group["experiments"][0]
        for previous, card in zip(old_group["experiments"][1]["cards"], group["experiments"][1]["cards"], strict=True):
            if previous["status"] == "done":
                assert previous == card
    successful = next(
        card for group in before["groups"] for card in group["experiments"][1]["cards"] if card["status"] == "done"
    )
    replacements[successful["prompt_key"]] = successful
    with pytest.raises(ValueError, match="successful original"):
        report.merge_data(before, document, replacements)


class FakeS3:
    def __init__(self):
        self.objects = {}
        self.puts = []
        self.edit_on_support_upload = False

    def get_object(self, *, Bucket, Key):
        value = self.objects[Key]
        return {**value, "Body": io.BytesIO(value["data"])}

    def put_object(self, *, Bucket, Key, Body, ContentType, Metadata=None, IfNoneMatch=None, IfMatch=None, **headers):
        if IfNoneMatch:
            assert IfNoneMatch == "*" and Key not in self.objects
        if IfMatch:
            assert self.objects[Key]["ETag"] == IfMatch
        self.puts.append((Key, IfMatch))
        self.objects[Key] = {
            "data": Body,
            "ETag": hashlib.md5(Body).hexdigest(),
            "ContentType": ContentType,
            "Metadata": Metadata or {},
            **headers,
        }
        if self.edit_on_support_upload and Key.endswith("completed_data_20261112.json"):
            self.objects[report.PREFIX + "/gallery/index.html"]["data"] = b"concurrent human edit"


@pytest.mark.parametrize("concurrent", [False, True])
def test_atomic_index_switch_preserves_original_data_and_stops_on_live_edit(tmp_path, monkeypatch, concurrent):
    monkeypatch.setattr(report, "HERE", tmp_path)
    monkeypatch.setattr(report, "PUBLIC", tmp_path / "public")
    client = FakeS3()
    source = {}
    for name in report.SOURCE_NAMES:
        key = report.PREFIX + "/" + name
        body = name.encode()
        report.write(tmp_path / "source" / name, body)
        client.objects[key] = {
            "data": body,
            "ETag": hashlib.md5(body).hexdigest(),
            "ContentType": report.content_type(name),
            "Metadata": {},
        }
        source[name] = {
            "etag": client.objects[key]["ETag"],
            "sha256": hashlib.sha256(body).hexdigest(),
            "content_type": report.content_type(name),
            "metadata": {},
            "headers": {},
        }
    assets = {}
    for name in (report.DATA_NAME, "gallery/index.html"):
        report.write(report.PUBLIC / name, b"new completed body")
        assets[name] = {"sha256": report.sha(report.PUBLIC / name)}
    report.write(tmp_path / "source_manifest.json", {"files": source, "recovery_code": {}})
    report.write(tmp_path / "build_manifest.json", {"assets": assets})
    report.write(
        tmp_path / "browser_validation.json",
        {"status": "passed", "build_manifest_sha256": report.sha(tmp_path / "build_manifest.json")},
    )
    monkeypatch.setattr(report.text_study, "s3_client", lambda: client)
    monkeypatch.setattr(report.original_report, "verify_live", lambda _: None)
    client.edit_on_support_upload = concurrent
    if concurrent:
        with pytest.raises(ValueError, match="Concurrent report edit"):
            report.publish()
        assert client.objects[report.PREFIX + "/gallery/index.html"]["data"] == b"concurrent human edit"
        assert not any(etag for _, etag in client.puts)
    else:
        report.publish()
        assert client.puts[-1] == (report.PREFIX + "/gallery/index.html", source["gallery/index.html"]["etag"])
    assert client.objects[report.PREFIX + "/gallery/data.json"]["data"] == b"gallery/data.json"
