import copy
import hashlib
import importlib.util
import io
from pathlib import Path
from types import SimpleNamespace

from botocore.exceptions import ClientError
import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("original_gallery_update", HERE / "gallery_update.py")
gallery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gallery)


@pytest.fixture
def example():
    figures = []
    records = []
    for index in range(4):
        url = f"https://example.test/image{index}.jpg"
        figures.append(
            f'<figure><figcaption>Variant {index}</figcaption><a href="{url}"><img src="{url}"></a>'
            f'<details class="placement-judge pass"><summary>Original score {index}</summary>'
            '<div><details><summary>Original evidence</summary>Café &amp; support</details></div>'
            '</details></figure>'
        )
        result = {"status": "complete", "verdict": "pass", "score": index * 10,
                  "short_reason": f"Image{index} <evidence> & context.", "reused": True}
        records.append({"source_row_id": "Case café", "generated_image": {"url": url},
                        "r1": result, "r2": copy.deepcopy(result)})
    source = '<!doctype html><style>.row{display:grid}</style>\n<section><h2>Case café</h2><div class="row">'
    return source + "".join(figures) + "</div></section>", records


def test_insertions_preserve_every_original_byte_and_match_urls_not_order(example):
    source, records = example
    updated, slots = gallery.render(source, list(reversed(records)), "results.json")
    assert gallery.ADDED.sub("", updated) == source
    assert len(slots) == 4
    assert updated.count('data-v31-version="r1"') == updated.count('data-v31-version="r2"') == 4
    for index, slot in enumerate(gallery.GalleryParser(updated).slots):
        assert f"Original score {index}" in slot["original_judge"]
        added = updated[slot["judge_end"]:slot["insert_at"]]
        assert f"Image{index} &lt;evidence&gt; &amp; context." in added
        assert f"Pass | {index * 10}/100" in added


def test_repeated_insertion_is_rejected(example):
    source, records = example
    updated, _ = gallery.render(source, records, "results.json")
    with pytest.raises(ValueError, match="duplicate insertion"):
        gallery.render(updated, records, "results.json")


@pytest.mark.parametrize("change", ["missing", "duplicate", "wrong-row"])
def test_wrong_image_or_source_bindings_are_rejected(example, change):
    source, records = example
    if change == "missing":
        records.pop()
    elif change == "duplicate":
        records[-1] = records[0]
    else:
        records[0]["source_row_id"] = "Another case"
    with pytest.raises(ValueError, match="differ|duplicate"):
        gallery.render(source, records, "results.json")


@pytest.mark.parametrize("score", [True, float("nan"), -1, 101])
def test_invalid_scores_never_render_as_success(score):
    with pytest.raises(ValueError, match="invalid completed"):
        gallery.result_html("r2", {"status": "complete", "verdict": "pass", "score": score, "short_reason": "Reason"})


def test_error_has_no_invented_score_or_fallback():
    value = {"status": "error", "verdict": None, "score": None, "short_reason": None, "error": "Provider error"}
    rendered = gallery.result_html("r2", value)
    assert "ERROR | no score" in rendered
    assert "Pass" not in rendered
    value["score"] = 0
    with pytest.raises(ValueError, match="fallback"):
        gallery.result_html("r2", value)


class FakeS3:
    def __init__(self, source_key, body):
        self.source_key = source_key
        self.objects = {source_key: {"body": body, "content_type": "text/html; charset=utf-8", "metadata": {}}}
        self.puts = []
        self.conflict_before_index = False
        operation = SimpleNamespace(input_shape=SimpleNamespace(members={"IfMatch": None, "IfNoneMatch": None}))
        self.meta = SimpleNamespace(service_model=SimpleNamespace(operation_model=lambda name: operation))

    def get_object(self, *, Bucket, Key):
        item = self.objects[Key]
        return {
            "Body": io.BytesIO(item["body"]), "ETag": '"' + hashlib.md5(item["body"]).hexdigest() + '"',
            "VersionId": "test-version", "ContentType": item["content_type"], "Metadata": item["metadata"],
        }

    def put_object(self, **params):
        key = params["Key"]
        if self.conflict_before_index and key == self.source_key:
            self.objects[key]["body"] = b"concurrent user edit"
        current = self.get_object(Bucket=params["Bucket"], Key=key) if key in self.objects else None
        if ((params.get("IfNoneMatch") == "*" and current is not None)
                or ("IfMatch" in params and (current is None or params["IfMatch"] != current["ETag"]))):
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        self.puts.append(params)
        self.objects[key] = {"body": params["Body"], "content_type": params["ContentType"],
                             "metadata": params["Metadata"]}
        return {}


@pytest.fixture
def publication(tmp_path, monkeypatch):
    monkeypatch.setattr(gallery, "HERE", tmp_path)
    (tmp_path / "source").mkdir()
    (tmp_path / "gallery").mkdir()
    key, original, updated, results = "original/viewer.html", b"original gallery", b"updated gallery", b'{"records":[]}'
    client = FakeS3(key, original)
    source = {"bucket": "test", "key": key, "sha256": gallery.digest(original),
              "ETag": client.get_object(Bucket="test", Key=key)["ETag"],
              "VersionId": "old-version", "ContentType": "text/html; charset=utf-8", "Metadata": {}}
    audit = {"html_sha256": gallery.digest(updated), "results_sha256": gallery.digest(results),
             "results_filename": "judge_results.json"}
    gallery.write_json(tmp_path / "source/object.json", source)
    gallery.write_json(tmp_path / "build_audit.json", audit)
    (tmp_path / "gallery/viewer.html").write_bytes(updated)
    (tmp_path / "gallery/judge_results.json").write_bytes(results)
    return client, key, original, updated


def test_safe_publish_preserves_backup_and_is_idempotent(publication):
    client, key, original, updated = publication
    receipt = gallery.publish(client)
    assert client.objects[key]["body"] == updated
    assert client.objects[receipt["backup_key"]]["body"] == original
    index_put = next(item for item in client.puts if item["Key"] == key)
    assert index_put["IfMatch"]
    before = len(client.puts)
    gallery.publish(client)
    assert len(client.puts) == before


def test_live_edit_before_publish_is_not_overwritten(publication):
    client, key, _, _ = publication
    client.objects[key]["body"] = b"already edited"
    with pytest.raises(ValueError, match="live gallery changed"):
        gallery.publish(client)
    assert client.puts == []


def test_live_edit_during_publish_is_not_overwritten(publication):
    client, key, original, _ = publication
    client.conflict_before_index = True
    with pytest.raises(ClientError, match="PreconditionFailed"):
        gallery.publish(client)
    assert client.objects[key]["body"] == b"concurrent user edit"
    assert any(item["body"] == original for name, item in client.objects.items() if name != key)


def test_existing_different_backup_blocks_original_overwrite(publication):
    client, key, original, _ = publication
    backup_key = "original/judge_v31_backups/" + gallery.digest(original)[:16] + "/viewer.html"
    client.objects[backup_key] = {"body": b"unexpected backup", "content_type": "text/html", "metadata": {}}
    with pytest.raises(ValueError, match="refusing overwrite"):
        gallery.publish(client)
    assert client.objects[key]["body"] == original
