import copy
import io
from pathlib import Path

import pytest
from botocore.exceptions import ClientError

import generate
import publish
import study


class Store:
    def __init__(self, objects):
        self.objects = objects
        self.writes = []

    def get_object(self, *, Bucket, Key):
        item = copy.deepcopy(self.objects[Key])
        item["Body"] = io.BytesIO(item.pop("bytes"))
        return item

    def put_object(self, *, Bucket, Key, Body, ContentType, Metadata, **kwargs):
        if (kwargs.get("IfNoneMatch") == "*" and Key in self.objects
                or "IfMatch" in kwargs and self.objects[Key]["ETag"] != kwargs["IfMatch"]):
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        self.writes.append((Key, kwargs))
        self.objects[Key] = {
            "bytes": Body, "ContentType": ContentType, "Metadata": Metadata,
            "ETag": '"' + study.digest(Body) + '"', "VersionId": None,
        }

    def get_paginator(self, operation):
        return self

    def paginate(self, **kwargs):
        return [{"Contents": []}]


def fixture(monkeypatch, tmp_path):
    monkeypatch.setattr(study, "HERE", tmp_path)
    monkeypatch.setattr(generate, "verify", lambda: None)
    root = tmp_path / "mount"
    root.mkdir()
    for name in ("execution_manifest.json", "generation_audit.json", "baseline_bindings.json",
                 "report.py", "check_browser.py"):
        study.emit(tmp_path / name, {"fixture": name})
    study.emit(tmp_path / "media_inventory.json", {"objects": {}})
    study.emit(tmp_path / "storage.json", {"artifact_root": str(root)})
    objects, originals, entries = {}, {}, {}
    for relative, prefix in (
        ("fe/data.json", study.FE_PREFIX), ("fe/viewer.html", study.FE_PREFIX),
        ("grouped/index.html", study.GROUP_PREFIX),
    ):
        key = prefix + "/" + Path(relative).name
        old, new = ("old " + key).encode(), ("new " + key).encode()
        kind = "application/json" if key.endswith(".json") else "text/html; charset=utf-8"
        objects[key] = {"bytes": old, "ContentType": kind, "Metadata": {"existing": "preserve"},
                        "ETag": '"original"', "VersionId": None}
        original = {
            "key": key, "sha256": study.digest(old), "etag": '"original"', "version_id": None,
            "content_type": kind, "metadata": {"existing": "preserve"},
        }
        originals[relative] = original
        study.emit(tmp_path / "source" / relative, old)
        path = tmp_path / "new" / relative
        study.emit(path, new)
        entries[key] = {"path": str(path), "sha256": study.digest(new), "bytes": len(new),
                        "content_type": kind, "original": original}
    for name in ("fe/data.json", "fe/viewer.html", "gallery/index.html", "gallery/data.json"):
        path = tmp_path / "support" / name
        body = name.encode()
        study.emit(path, body)
        entries[study.PREFIX + "/" + name] = {
            "path": str(path), "sha256": study.digest(body), "bytes": len(body),
            "content_type": "application/json" if name.endswith(".json") else "text/html",
            "original": None,
        }
    manifest = {
        "entries": entries, "links": ["test only"] * 4,
        "builder_sha256": study.sha(tmp_path / "report.py"),
        "generation_audit_sha256": study.sha(tmp_path / "generation_audit.json"),
        "baseline_bindings_sha256": study.sha(tmp_path / "baseline_bindings.json"),
    }
    study.emit(tmp_path / "publication_manifest.json", manifest)
    study.emit(tmp_path / "source_manifest.json", {"objects": originals})
    study.emit(tmp_path / "browser_validation.json", {
        "passed": True, "publication_manifest_sha256": study.sha(tmp_path / "publication_manifest.json"),
        "checker_sha256": study.sha(tmp_path / "check_browser.py"),
        "transport_helper_sha256": study.sha(study.PRIOR / "check_browser.py"),
        "media_inventory_sha256": study.sha(tmp_path / "media_inventory.json"),
    })
    store = Store(objects)
    monkeypatch.setattr(study, "client", lambda: store)
    return store, entries


def test_owned_partial_resume_preserves_metadata_and_switches_entrypoints_after_support(monkeypatch, tmp_path):
    store, entries = fixture(monkeypatch, tmp_path)
    data_key = study.FE_PREFIX + "/data.json"
    item = entries[data_key]
    store.objects[data_key] = {
        "bytes": Path(item["path"]).read_bytes(), "ContentType": item["content_type"],
        "Metadata": {"existing": "preserve",
                     "hp-study-sha256": study.sha(tmp_path / "execution_manifest.json")},
        "ETag": '"already-owned"', "VersionId": None,
    }
    publish.publish()
    keys = [key for key, _ in store.writes]
    assert data_key not in keys
    for name in ("fe/viewer.html", "gallery/index.html"):
        assert keys.index(study.PREFIX + "/gallery/data.json") < keys.index(study.PREFIX + "/" + name)
    assert keys[-2:] == [study.FE_PREFIX + "/viewer.html", study.GROUP_PREFIX + "/index.html"]
    assert all("IfMatch" in options for key, options in store.writes if key in (
        study.FE_PREFIX + "/viewer.html", study.GROUP_PREFIX + "/index.html"))
    assert store.objects[study.FE_PREFIX + "/viewer.html"]["Metadata"]["existing"] == "preserve"
    assert not any("/annotations/" in key for key in keys)
    assert study.load(tmp_path / "publication_receipt.json")["annotation_objects_written"] == 0


@pytest.mark.parametrize("damage", ["etag", "unowned_identical_new_bytes"])
def test_changed_or_unowned_live_source_is_rejected_before_any_write(monkeypatch, tmp_path, damage):
    store, entries = fixture(monkeypatch, tmp_path)
    key = study.FE_PREFIX + "/data.json"
    if damage == "etag":
        store.objects[key]["ETag"] = '"concurrent edit"'
    else:
        store.objects[key]["bytes"] = Path(entries[key]["path"]).read_bytes()
    with pytest.raises(ValueError, match="Live source changed"):
        publish.publish()
    assert store.writes == []
