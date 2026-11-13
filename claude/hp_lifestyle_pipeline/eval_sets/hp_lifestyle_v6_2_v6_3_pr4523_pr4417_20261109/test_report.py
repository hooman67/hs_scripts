import importlib.util
import io
from pathlib import Path

import pytest
from PIL import Image

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("hp_comparison_report", HERE / "report.py")
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


@pytest.fixture
def audit_files(tmp_path, monkeypatch):
    monkeypatch.setattr(report, "HERE", tmp_path)
    body = io.BytesIO()
    Image.new("RGB", (4, 3)).save(body, "PNG")
    asset = report.image_evidence(body.getvalue())
    record = tmp_path / "record.json"
    record.write_text("{}")
    (tmp_path / "study_manifest.json").write_text("{}")
    receipt = tmp_path / "audit.json"
    report.write(receipt, {
        "study_manifest_sha256": report.study.sha(tmp_path / "study_manifest.json"),
        "record_sha256": report.study.sha(record),
        **{role: asset for role in ("product", "reference", "geometry_guide")},
    })
    return receipt, record, Path(asset["path"]), body.getvalue()


@pytest.mark.parametrize("expected_sha,expected_size", [("0" * 64, None), (None, (5, 3))])
def test_wrong_actual_input_binding_is_not_persisted(tmp_path, monkeypatch, expected_sha, expected_size):
    monkeypatch.setattr(report, "HERE", tmp_path)
    body = io.BytesIO()
    Image.new("RGB", (4, 3)).save(body, "PNG")
    with pytest.raises(ValueError, match="frozen"):
        report.image_evidence(body.getvalue(), expected_sha, expected_size)
    assert not (tmp_path / "input_audit").exists()


def test_cached_audit_rejects_changed_generation_record(audit_files):
    receipt, record, _, _ = audit_files
    report.checked_audit(receipt, record)
    record.write_text('{"job_id":"different"}')
    with pytest.raises(ValueError, match="study/record"):
        report.checked_audit(receipt, record)


def test_cached_audit_rejects_changed_input_bytes(audit_files):
    receipt, record, asset, _ = audit_files
    asset.write_bytes(b"changed")
    with pytest.raises(ValueError, match="asset changed"):
        report.checked_audit(receipt, record)


def test_content_addressed_input_cache_never_hides_corruption(audit_files):
    _, _, asset, body = audit_files
    asset.write_bytes(b"changed")
    with pytest.raises(ValueError, match="cached model-input bytes changed"):
        report.image_evidence(body)
