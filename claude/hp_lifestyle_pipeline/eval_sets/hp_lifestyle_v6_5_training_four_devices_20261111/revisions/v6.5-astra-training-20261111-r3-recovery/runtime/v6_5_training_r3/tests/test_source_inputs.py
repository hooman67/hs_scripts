import json
import zipfile

import pytest

from research.source_messaging_v1_to_v6.versions.v6_5_training_r3.source_inputs import load_pair


@pytest.mark.parametrize("packaging", ["directory", "zip"])
def test_paired_json_keeps_values_array_order_and_original_member_hashes(tmp_path, packaging):
    brief = {"USE CASES": {"content": "An office.\n\nA home study.", "confidence": "high"}}
    messaging = {"source_messaging": [{"fields": [{"row": 104, "value": "Office work."}]}]}
    originals = {
        "Smart Brief - sample.json": json.dumps(brief).encode(),
        "source-messaging.json": json.dumps(messaging).encode(),
    }
    if packaging == "zip":
        source = tmp_path / "pair.zip"
        with zipfile.ZipFile(source, "w") as archive:
            for name, body in originals.items():
                archive.writestr("nested/" + name, body)
            archive.writestr("supplementary.pdf", b"not a runtime input")
    else:
        source = tmp_path
        for name, body in originals.items():
            (source / name).write_bytes(body)
    documents, provenance = load_pair(source)
    assert documents == {"smart_brief": brief, "source_messaging": messaging}
    assert set(provenance) == set(documents)
    assert provenance["smart_brief"]["bytes"] == len(originals["Smart Brief - sample.json"])
    if packaging == "zip":
        assert provenance["smart_brief"]["archive_member"] == "nested/Smart Brief - sample.json"
        assert not (tmp_path / "nested").exists()
    else:
        assert provenance["smart_brief"]["archive_member"] is None


@pytest.mark.parametrize("extra,expected", [
    (None, "exactly one"),
    (("source-messaging.json", b"[]"), "JSON object"),
    (("source-messaging.json", b'{"a": 1, "a": 2}'), "duplicate JSON key"),
    (("source-messaging.json", b'{"a": NaN}'), "non-JSON numeric"),
    (("source-messaging.json", b"{"), "property name"),
    (("unknown.json", b"{}"), "unrecognized paired JSON"),
])
def test_invalid_or_missing_documents_fail_explicitly(tmp_path, extra, expected):
    (tmp_path / "smart-brief.json").write_text("{}")
    if extra:
        (tmp_path / extra[0]).write_bytes(extra[1])
    with pytest.raises(ValueError, match=expected):
        load_pair(tmp_path)


@pytest.mark.parametrize("member,expected", [
    ("copy/smart-brief.json", "ambiguous duplicate"),
    ("../source-messaging.json", "unsafe archive"),
])
def test_ambiguous_or_unsafe_archive_members_are_not_selected(tmp_path, member, expected):
    source = tmp_path / "pair.zip"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("smart-brief.json", "{}")
        archive.writestr(member, "{}")
    with pytest.raises(ValueError, match=expected):
        load_pair(source)
