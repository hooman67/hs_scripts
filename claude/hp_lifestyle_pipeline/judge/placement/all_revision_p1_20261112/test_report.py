import copy
import io
from unittest.mock import Mock

import complete
import pytest
import report
from botocore.exceptions import ClientError


@pytest.fixture
def gallery():
    figures, records = [], []
    for index in range(4):
        image = f"https://example.test/{index}.jpg"
        figures.append(
            f'<figure><figcaption>{index}</figcaption><a><img src="{image}"></a>'
            '<details class="placement-judge"><summary>Original V3</summary>'
            "<details><summary>Evidence</summary>Original</details></details>"
            '<div class="v31-result">V3.1 r1</div>'
            '<div class="v31-result">V3.1 r2</div></figure>'
        )
        results = {
            version: {
                "p1": {
                    "status": "complete",
                    "score": index * 10,
                    "verdict": "pass",
                    "checks": None,
                    "observation": {
                        "summary": f"Image{index} & evidence",
                        "components": {},
                    },
                },
                "p2": None,
            }
            for version in report.OLD.REVISIONS
        }
        results["v3_2_r2"]["p2"] = {
            "status": "error",
            "score": None,
            "verdict": None,
            "observation": None,
            "error_type": "APIError",
            "error": "Original preserved error",
        }
        records.append(
            {
                "image_url": image,
                "source_row_id": "Case one",
                "image_sha256": str(index) * 64,
                "results": results,
            }
        )
    base = (
        "<!doctype html><style>.row{display:grid}</style>"
        "<section><h2>Case one</h2><div class='row'>"
        + "".join(figures)
        + "</div></section>"
    )
    prior = report.OLD.render(base, records, "previous.json")[0]
    return base, prior, records


def test_replacing_astra_layer_preserves_all_original_bytes_and_p2(gallery):
    base, prior, records = gallery
    result = report.render(
        prior, list(reversed(records)), "current.json", "previous.json"
    )
    assert report.original_layer(result) == base
    assert result.count("repeat(10,auto)") == 1
    assert "repeat(13,auto)" not in result
    assert result.count('class="astra-previous"') == 4
    assert result.count("Original preserved error") == 4
    assert result.count("NOT EVALUATED | no score") == 12
    for index, slot in enumerate(report.OLD.LEGACY.GalleryParser(result).slots):
        additions = result[slot["judge_end"] : slot["insert_at"]]
        assert additions.count(f"PASS | {index * 10}/100") == 4
        assert additions.index('data-astra-candidate="p1"') < additions.index(
            'class="astra-previous"'
        )
        assert additions.count("Image" + str(index) + " &amp; evidence") == 4


def test_missing_selected_revision_cannot_be_published(gallery):
    _, prior, records = gallery
    records = copy.deepcopy(records)
    records[0]["results"]["v3_2_r4"]["p1"] = None
    with pytest.raises(ValueError, match="selected P1 judgments must be complete"):
        report.render(prior, records, "current.json", "previous.json")


@pytest.fixture
def publication(tmp_path, monkeypatch):
    monkeypatch.setattr(report, "HERE", tmp_path)
    original = b"original old judges and images"
    source = (report.OLD.START + "previous Astra" + report.OLD.END).encode() + original
    updated = (report.OLD.START + "complete Astra" + report.OLD.END).encode() + original
    audit = {
        "html_sha256": report.OLD.digest(updated),
        "results_filename": "current.json",
    }
    complete.write(tmp_path / "source/viewer.html", source)
    complete.write(
        tmp_path / "source/object.json",
        {
            "key": "original/viewer.html",
            "sha256": report.OLD.digest(source),
            "etag": '"source"',
            "content_type": "text/html",
            "metadata": {},
        },
    )
    complete.write(tmp_path / "gallery/viewer.html", updated)
    complete.write(tmp_path / "gallery/current.json", b"{}")
    complete.write(
        tmp_path / "browser_validation.json",
        {
            "passed": True,
            "html_sha256": audit["html_sha256"],
        },
    )
    monkeypatch.setattr(report, "verify_build", lambda: audit)
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


def test_backup_and_export_precede_conditional_in_place_update(publication):
    s3, _ = publication
    report.publish(s3)
    puts = s3.put_object.call_args_list
    assert len(puts) == 3
    assert puts[0].kwargs["IfNoneMatch"] == "*"
    assert puts[1].kwargs["IfNoneMatch"] == "*"
    assert puts[2].kwargs["IfMatch"] == '"source"'
    assert b"previous Astra" in puts[0].kwargs["Body"]


def test_live_edit_before_publication_is_preserved(publication):
    s3, objects = publication
    objects["original/viewer.html"] = (b"concurrent edit", "text/html")
    with pytest.raises(ValueError, match="Live gallery changed"):
        report.publish(s3)
    s3.put_object.assert_not_called()


def test_live_edit_during_publication_fails_closed(publication):
    s3, objects = publication
    put = s3.put_object.side_effect

    def conflict(**params):
        if params["Key"] == "original/viewer.html":
            objects["original/viewer.html"] = (b"concurrent edit", "text/html")
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        put(**params)

    s3.put_object.side_effect = conflict
    with pytest.raises(ClientError, match="PreconditionFailed"):
        report.publish(s3)
    assert objects["original/viewer.html"][0] == b"concurrent edit"
