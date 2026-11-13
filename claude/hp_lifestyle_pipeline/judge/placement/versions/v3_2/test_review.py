"""Review output cannot hide failed calls or bind scores to another image."""

import copy
import io
import json
from unittest.mock import Mock

import appearance_feedback
import build_review
import pytest
from test_common import observation


def test_result_html_escapes_generated_text_and_preserves_criterion_mismatch():
    value = observation()
    value["summary"] = "<script>not executable</script>"
    row = {
        "status": "complete",
        "verdict": "fail",
        "score": 59,
        "observation": value,
        "checks": {"required_geometry": False},
    }
    output = build_review.panel("Astra P2", row)
    assert "<script>" not in output
    assert "&lt;script&gt;" in output
    assert "Criterion mismatch: required_geometry" in output


def test_failed_calls_are_not_displayed_as_pass_or_zero_score():
    row = {
        "status": "error",
        "error": "Completion limit",
        "score": None,
        "verdict": None,
    }
    output = build_review.panel("Astra P2", row)
    assert "ERROR / no score" in output
    assert "/100" not in output
    with pytest.raises(ValueError, match="Non-terminal"):
        build_review.panel("Astra P2", {"status": "pending"})


def test_identical_passthrough_can_share_judgment_without_changing_image_binding():
    row = {
        "status": "complete",
        "verdict": "pass",
        "score": 100,
        "observation": observation(),
    }
    image = {"url": build_review.BASE + "refiner_evals/a/baseline.png", "sha256": "abc"}
    refined = copy.deepcopy(image)
    refined["url"] = build_review.BASE + "refiner_evals/a/refined.png"
    output = build_review.card(
        "case--refined", refined, "Exact passthrough", [("Astra P2", row)]
    )
    assert 'data-sha="abc"' in output
    assert build_review.asset(refined["url"]) in output
    assert "baseline.png" not in output


def test_asset_mapping_stays_relative_to_the_approved_bucket():
    assert (
        build_review.asset(build_review.BASE + "source/image.png")
        == "../../../source/image.png"
    )
    with pytest.raises(ValueError, match="approved HP bucket"):
        build_review.asset("https://elsewhere.example/image.png")


def test_successor_publication_keeps_old_urls_and_comment_identity(monkeypatch):
    original_prefix = build_review.PREFIX
    original_store = build_review.STORE
    monkeypatch.setattr(build_review, "PREFIX", original_prefix)
    monkeypatch.setattr(build_review, "STORE", original_store)
    version = build_review.common.ROOT.parent / "v3_2_r3"
    build_review.configure(version)
    assert build_review.STORE == version / "publication"
    assert build_review.PREFIX.endswith("/r3/gallery/")
    assert build_review.PREFIX != original_prefix
    assert (
        build_review.asset(build_review.BASE + "source/image.png")
        == "../../../../source/image.png"
    )
    build_review.configure(build_review.common.ROOT.parent / "v3_2_r2")
    assert build_review.PREFIX == original_prefix
    assert build_review.STORE == original_store


def test_appearance_clarification_does_not_claim_original_gate_recovery():
    feedback = {"case_id": "scene", "verbatim": "Chair backrest concern."}
    output = build_review.clarification_html("scene", feedback, appearance=True)
    assert "not necessarily FAIL" in output
    assert "not retrospectively resolved" in output
    assert "still does not substantiate material defects" not in output


def test_appearance_publication_uses_that_versions_actual_astra_design(
    tmp_path, monkeypatch
):
    source = tmp_path / "r4_actual_proposal.json"
    proposal = {"runtime_change_required": {"required": True}}
    build_review.common.write_json(source, proposal)
    build_review.common.write_json(
        tmp_path / "preparation.json",
        {
            "prompt_source_path": str(source),
            "prompt_source_sha256": build_review.common.sha(source),
            "actual_astra_receipt": {"model_returned": "gpt-6-astra"},
        },
    )
    collector = Mock()
    collector.result.return_value = proposal
    replay = Mock(return_value=collector)
    monkeypatch.setattr(appearance_feedback, "replay", replay)
    assert build_review.appearance_design(tmp_path) == proposal
    replay.assert_called_once_with({"model_returned": "gpt-6-astra"})
    build_review.common.write_json(source, {"substituted_old_proposal": True})
    with pytest.raises(ValueError, match="actual Astra source"):
        build_review.appearance_design(tmp_path)


def test_acquisition_trace_replays_actual_record_deduplicates_reuse_and_rejects_substitution(
    tmp_path, monkeypatch
):
    write = build_review.common.write_json
    digest = build_review.common.sha
    request = {"stage": "p2_geometry", "protocol_freeze_sha256": "frozen"}
    fingerprint = build_review.common.fingerprint(request)
    record = {"record": "An unscored literal exposed boundary."}
    write(tmp_path / "request.json", request)
    write(
        tmp_path / "acquisition.json",
        {
            "fingerprint": fingerprint,
            "observation": record,
        },
    )
    acquisition = {
        "path": str(tmp_path / "acquisition.json"),
        "sha256": digest(tmp_path / "acquisition.json"),
        "fingerprint": fingerprint,
        "record": record["record"],
        "scored": False,
    }
    stage = {
        "visual_acquisition": acquisition,
        "observation": {"actual": "scored observation"},
    }
    write(tmp_path / "stage.json", stage)
    write(
        tmp_path / "result.json",
        {
            "stages": {
                "p2_geometry": {
                    "path": str(tmp_path / "stage.json"),
                    "sha256": digest(tmp_path / "stage.json"),
                },
            }
        },
    )
    row = {
        "id": "case",
        "candidate": "p2",
        "status": "complete",
        "result_path": str(tmp_path / "result.json"),
        "observation": {"actual": "final output"},
        "score": 100,
        "verdict": "pass",
    }
    monkeypatch.setattr(build_review, "indexed", lambda summary: {("case", "p2"): row})
    collector = Mock()
    collector.result.return_value = record
    monkeypatch.setattr(appearance_feedback, "replay", lambda receipt: collector)
    summary = {"protocol_freeze_sha256": "frozen"}
    trace = build_review.acquisition_trace(
        {"calibration": summary, "historical": summary}
    )
    assert len(trace["records"]) == 1
    entry = trace["records"][0]
    assert entry["stages"][0]["actual_acquisition"]["record"] == record["record"]
    assert entry["application_score"] == 100
    stage["visual_acquisition"]["record"] = "Substituted claimed defect."
    write(tmp_path / "stage.json", stage)
    with pytest.raises(ValueError, match="actual source"):
        build_review.acquisition_trace({"calibration": summary})


def test_diagnosis_preserves_actual_response_and_distinguishes_dataset_from_predictions(
    tmp_path, monkeypatch
):
    write = build_review.common.write_json
    digest = build_review.common.sha
    roots = [tmp_path / "v3_2_r3", tmp_path / "v3_2_r4"]
    summaries = []
    for number, root in enumerate(roots):
        write(root / "calibration_manifest.json", {"cases": ["same source case"]})
        write(root / "protocol_freeze.json", {"revision": root.name})
        summary = {
            "source": str(root / "calibration_manifest.json"),
            "source_sha256": digest(root / "calibration_manifest.json"),
            "protocol_freeze_sha256": digest(root / "protocol_freeze.json"),
            "records": [{"revision_specific_score": number}],
        }
        write(root / "evaluation/calibration/summary.json", summary)
        summaries.append(summary)
    root = roots[1]
    directory = root / "astra_successor_consult"
    analysis = {"successor_justified": False, "original_provenance_question": True}
    write(directory / "proposal.json", analysis)
    write(directory / "receipt.json", {"actual": "Astra receipt"})
    inputs = {
        "source_revision": root.name,
        "frozen_protocol_sha256": digest(root / "protocol_freeze.json"),
        "actual_calibration_predictions": summaries[1],
        "immediate_predecessor_calibration": summaries[0],
    }
    write(directory / "input.json", inputs)
    write(root / "promotion_gates.json", {"predecessor": {"path": str(roots[0])}})
    collector = Mock()
    collector.result.return_value = analysis
    monkeypatch.setattr(appearance_feedback, "replay", lambda receipt: collector)
    validate = Mock()
    monkeypatch.setattr(build_review, "indexed", validate)
    result = build_review.successor_diagnosis(root)
    assert result["analysis"] == analysis
    bindings = result["calibration_bindings"]
    assert (
        bindings[0]["dataset_manifest_sha256"] == bindings[1]["dataset_manifest_sha256"]
    )
    assert (
        bindings[0]["prediction_summary_sha256"]
        != bindings[1]["prediction_summary_sha256"]
    )
    assert (
        bindings[0]["protocol_freeze_sha256"] != bindings[1]["protocol_freeze_sha256"]
    )
    assert validate.call_count == 2
    write(directory / "proposal.json", {"substituted": True})
    with pytest.raises(ValueError, match="actual Astra source"):
        build_review.successor_diagnosis(root)
    write(directory / "proposal.json", analysis)
    write(roots[0] / "calibration_manifest.json", {"substituted": True})
    with pytest.raises(ValueError, match="calibration provenance"):
        build_review.successor_diagnosis(root)


def test_terminal_errors_remain_exportable_instead_of_being_dropped():
    row = {
        "id": "a",
        "candidate": "p2",
        "status": "error",
        "error": "Validation failed",
    }
    summary = {"records": [row], "expected": 1, "complete": False}
    assert build_review.indexed(summary) == {("a", "p2"): row}
    with pytest.raises(ValueError, match="Every expected case"):
        build_review.indexed({**summary, "expected": 2})
    with pytest.raises(ValueError, match="Duplicate"):
        build_review.indexed({**summary, "records": [row, row], "expected": 2})


def test_exemplar_audit_rejects_substituted_delivery_before_any_paid_call(
    tmp_path, monkeypatch
):
    import revise_appearance

    write = build_review.common.write_json
    write(tmp_path / "protocol_freeze.json", {"files": []})
    write(tmp_path / "evaluation/calibration/summary.json", {})
    stage = tmp_path / "baseline/result.json"
    write(
        tmp_path / "result.json",
        {"stages": {"baseline": {"path": str(stage)}}, "runtime_input": {}},
    )
    write(
        stage.with_name("exemplars.json"),
        {"selected": [{"substituted": True}], "excluded": []},
    )
    monkeypatch.setattr(build_review, "successor_diagnosis", lambda version: {})
    monkeypatch.setattr(
        build_review,
        "indexed",
        lambda summary: {
            "case": {
                "candidate": "p1",
                "checks": {"appearance": False},
                "result_path": str(tmp_path / "result.json"),
            }
        },
    )
    monkeypatch.setattr(
        revise_appearance.common.LEGACY, "select_anchors", lambda runtime: ([], [])
    )
    call = Mock()
    monkeypatch.setattr(revise_appearance.transport, "model_completion", call)
    with pytest.raises(ValueError, match="actual frozen baseline delivery"):
        revise_appearance.audit_exemplars(tmp_path)
    call.assert_not_called()
    assert not (tmp_path / "astra_exemplar_audit").exists()


def test_published_exemplar_audit_binds_inputs_to_the_actual_request(
    tmp_path, monkeypatch
):
    import revise_appearance

    write = build_review.common.write_json
    digest = build_review.common.sha
    directory = tmp_path / "astra_exemplar_audit"
    artifact = tmp_path / "baseline/exemplars.json"
    exemplars = {"selected": [], "excluded": []}
    write(artifact, exemplars)
    write(tmp_path / "protocol_freeze.json", {"revision": "unchanged"})
    inputs = {
        "source_revision": tmp_path.name,
        "protocol_freeze_sha256": digest(tmp_path / "protocol_freeze.json"),
        "actual_exemplar_artifact": str(artifact),
        "actual_exemplar_artifact_sha256": digest(artifact),
        "actual_exemplars": exemplars,
        "task": "The actual audit request.",
    }
    write(directory / "input.json", inputs)
    analysis = {"corrections": "Proposed, not implemented."}
    write(directory / "analysis.json", analysis)
    write(directory / "receipt.json", {"chunks_path": str(directory / "chunks.jsonl")})

    def messages(value):
        return [{"role": "user", "content": value["task"]}]

    write(
        directory / "config.json",
        {"messages_sha256": build_review.common.fingerprint(messages(inputs))},
    )
    collector = Mock()
    collector.result.return_value = analysis
    monkeypatch.setattr(appearance_feedback, "replay", lambda receipt: collector)
    monkeypatch.setattr(revise_appearance, "exemplar_messages", messages)
    result = build_review.exemplar_audit(tmp_path)
    assert result["analysis"] == analysis
    assert result["actual_inputs"] == inputs
    inputs["task"] = "A substituted audit request."
    write(directory / "input.json", inputs)
    with pytest.raises(ValueError, match="delivered messages"):
        build_review.exemplar_audit(tmp_path)


def test_partial_publication_retains_ownership_for_safe_resume(tmp_path, monkeypatch):
    from botocore.exceptions import ClientError

    monkeypatch.setattr(build_review, "STORE", tmp_path)
    public = tmp_path / "public"
    public.mkdir()
    (public / "review.css").write_text("new stylesheet")
    (public / "index.html").write_text("new index")
    build_review.common.write_json(
        tmp_path / "build_receipt.json",
        {
            "files": {
                path.name: build_review.common.sha(path) for path in public.iterdir()
            }
        },
    )
    index_url = build_review.BASE + build_review.PREFIX + "index.html"
    old_digest = build_review.common.hashlib.sha256(b"owned old index").hexdigest()
    build_review.common.write_json(
        tmp_path / "publication_receipt.json",
        {
            "objects": [{"url": index_url, "sha256": old_digest, "etag": "old"}],
            "verified": True,
        },
    )

    class Client:
        def __init__(self):
            self.fail_index_once = True
            self.objects = {
                build_review.PREFIX + "index.html": {
                    "Body": b"owned old index",
                    "ETag": "old",
                    "ContentType": "text/html",
                }
            }

        def put_object(self, **kwargs):
            key = kwargs["Key"]
            if key.endswith("index.html") and self.fail_index_once:
                self.fail_index_once = False
                raise RuntimeError("Interrupted before index update")
            if kwargs.get("IfNoneMatch") and key in self.objects:
                raise ClientError(
                    {
                        "Error": {"Code": "PreconditionFailed"},
                        "ResponseMetadata": {"HTTPStatusCode": 412},
                    },
                    "PutObject",
                )
            if "IfMatch" in kwargs:
                assert kwargs["IfMatch"] == self.objects[key]["ETag"]
            self.objects[key] = {
                "Body": kwargs["Body"],
                "ContentType": kwargs["ContentType"],
                "ETag": "new",
            }

        def get_object(self, **kwargs):
            value = self.objects[kwargs["Key"]]
            return {**value, "Body": io.BytesIO(value["Body"])}

    client = Client()
    monkeypatch.setattr(build_review, "s3_client", lambda: client)
    with pytest.raises(RuntimeError, match="Interrupted"):
        build_review.publish()
    checkpoint = json.loads((tmp_path / "publication_receipt.json").read_text())
    assert not checkpoint["verified"]
    assert (
        next(row for row in checkpoint["objects"] if row["url"] == index_url)["sha256"]
        == old_digest
    )
    build_review.publish()
    receipt = json.loads((tmp_path / "publication_receipt.json").read_text())
    assert receipt["verified"]
    assert len(receipt["objects"]) == 2
    assert client.objects[build_review.PREFIX + "index.html"]["Body"] == b"new index"
