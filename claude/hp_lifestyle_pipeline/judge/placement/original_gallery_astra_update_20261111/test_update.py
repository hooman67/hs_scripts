import copy
import io
from unittest.mock import Mock

import pytest
import update
from botocore.exceptions import ClientError


@pytest.fixture
def gallery():
    figures, records = [], []
    for index in range(4):
        image = f"https://example.test/{index}.jpg"
        figures.append(
            f'<figure><figcaption>{index}</figcaption><a><img src="{image}"></a>'
            '<details class="placement-judge"><summary>Original V3</summary>'
            "<details><summary>Original evidence</summary>Unchanged</details></details>"
            '<div class="v31-result">Original V3.1 r1</div>'
            '<div class="v31-result">Original V3.1 r2</div></figure>'
        )
        results = {version: {"p1": None, "p2": None} for version in update.REVISIONS}
        results["v3_2_r2"]["p1"] = {
            "status": "complete",
            "score": index * 10,
            "verdict": "pass",
            "observation": {
                "summary": f"Image{index} <evidence> & context.",
                "components": {},
            },
            "checks": None,
        }
        records.append(
            {
                "image_url": image,
                "source_row_id": "Case one",
                "image_sha256": str(index) * 64,
                "results": results,
            }
        )
    source = (
        "<!doctype html><style>.row{display:grid}</style>"
        "<style>.row{grid-template-rows:repeat(5,auto)}</style>"
        "<section><h2>Case one</h2><div class='row'>"
        + "".join(figures)
        + "</div></section>"
    )
    return source, records


def test_existing_layers_remain_byte_exact_and_shuffled_results_match_images(gallery):
    source, records = gallery
    actual, _ = update.render(source, list(reversed(records)), "results.json")
    assert update.ADDED.sub("", actual) == source
    assert actual.index("repeat(13,auto)") > actual.index("repeat(5,auto)")
    for index, slot in enumerate(update.LEGACY.GalleryParser(actual).slots):
        added = actual[slot["judge_end"] : slot["insert_at"]]
        assert added.index("Original V3.1 r2") < added.index("data-astra-version")
        assert f"PASS | {index * 10}/100" in added
        assert f"Image{index} &lt;evidence&gt; &amp; context." in added
        assert added.count("NOT EVALUATED | no score") == 7
        assert added.count('class="astra-result ') == 8
    with pytest.raises(ValueError, match="duplicate insertion"):
        update.render(actual, records, "results.json")


@pytest.mark.parametrize("change", ["wrong-row", "missing", "duplicate"])
def test_source_binding_errors_stop_publication(gallery, change):
    source, records = gallery
    if change == "wrong-row":
        records[0]["source_row_id"] = "Another row"
    elif change == "missing":
        records.pop()
    else:
        records[0] = copy.deepcopy(records[1])
    with pytest.raises(
        ValueError, match="another source row|columns differ|Duplicate image"
    ):
        update.render(source, records, "results.json")


def test_errors_and_missing_predictions_cannot_become_success():
    error = {
        "status": "error",
        "score": None,
        "verdict": None,
        "observation": None,
        "error_type": "APIError",
        "error": "Actual preserved error",
    }
    rendered = update.panel("v3_2_r2", "p2", error, "results.json", "a" * 64)
    assert "ERROR | no score" in rendered
    assert "PASS" not in rendered and "/100" not in rendered
    error["score"] = 0
    with pytest.raises(ValueError, match="failed judgment"):
        update.panel("v3_2_r2", "p2", error, "results.json", "a" * 64)
    rendered = update.panel("v3_2_r4", "p1", None, "results.json", "a" * 64)
    assert "NOT EVALUATED | no score" in rendered
    assert "/100" not in rendered


@pytest.fixture
def publication(tmp_path, monkeypatch):
    monkeypatch.setattr(update, "HERE", tmp_path)
    source = b"original HTML"
    updated = (update.START + "added" + update.END).encode() + source
    audit = {
        "html_sha256": update.digest(updated),
        "results_filename": "results.json",
        "results_sha256": update.digest(b"{}"),
        "local_files": {},
    }
    update.emit(tmp_path / "source/viewer.html", source)
    update.emit(
        tmp_path / "source/object.json",
        {
            "key": "original/viewer.html",
            "sha256": update.digest(source),
            "etag": '"source"',
            "content_type": "text/html",
            "metadata": {},
        },
    )
    update.emit(tmp_path / "gallery/viewer.html", updated)
    update.emit(tmp_path / "gallery/results.json", b"{}")
    update.emit(tmp_path / "build_audit.json", audit)
    update.emit(
        tmp_path / "browser_validation.json",
        {
            "passed": True,
            "html_sha256": audit["html_sha256"],
        },
    )
    objects = {"original/viewer.html": (source, "text/html")}
    s3 = Mock()

    def get(**params):
        body, content_type = objects[params["Key"]]
        return {
            "Body": io.BytesIO(body),
            "ContentType": content_type,
            "ETag": '"source"',
            "VersionId": "test-version",
        }

    def put(**params):
        objects[params["Key"]] = (params["Body"], params["ContentType"])

    s3.get_object.side_effect = get
    s3.put_object.side_effect = put
    return s3, objects


def test_publication_creates_verified_backup_before_conditional_original_update(
    publication,
):
    s3, objects = publication
    update.publish(s3)
    puts = s3.put_object.call_args_list
    assert len(puts) == 3
    assert puts[0].kwargs["IfNoneMatch"] == "*"
    assert puts[1].kwargs["IfNoneMatch"] == "*"
    assert puts[2].kwargs["Key"] == "original/viewer.html"
    assert puts[2].kwargs["IfMatch"] == '"source"'
    assert any(
        body == b"original HTML"
        for key, (body, _) in objects.items()
        if "backups" in key
    )


def test_live_edit_before_publish_is_never_overwritten(publication):
    s3, objects = publication
    objects["original/viewer.html"] = (b"concurrent edit", "text/html")
    with pytest.raises(ValueError, match="Live gallery changed"):
        update.publish(s3)
    s3.put_object.assert_not_called()


def test_live_edit_during_publish_fails_closed(publication):
    s3, objects = publication
    old_put = s3.put_object.side_effect

    def conflict(**params):
        if params["Key"] == "original/viewer.html":
            objects["original/viewer.html"] = (b"concurrent edit", "text/html")
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        old_put(**params)

    s3.put_object.side_effect = conflict
    with pytest.raises(ClientError, match="PreconditionFailed"):
        update.publish(s3)
    assert objects["original/viewer.html"][0] == b"concurrent edit"
