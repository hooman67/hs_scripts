"""Incomplete policy text must not cause completed case reviews to be redrawn."""

import json

import appearance_feedback
import pytest


def test_complete_case_objects_survive_truncated_policy_tail():
    reviews = [{"case_id": "a", "evidence": 'A bracket ] and "quoted" contour.'}]
    text = json.dumps({"case_reviews": reviews})[:-1] + ', "scope_gaps": "unfinished'
    parsed, end = appearance_feedback.completed_reviews(text)
    assert parsed == reviews
    assert text[end:].startswith(', "scope_gaps"')


def test_truncated_case_object_cannot_be_credited_as_a_finished_review():
    text = '{"case_reviews":[{"case_id":"a","evidence":"unfinished'
    with pytest.raises(ValueError, match="case review is incomplete"):
        appearance_feedback.completed_reviews(text)


def test_image_packets_measure_base64_size_and_deduplicate_reference(tmp_path):
    reference = tmp_path / "reference.png"
    reference.write_bytes(b"R" * 100)
    rows = []
    for name in ("a", "b", "c"):
        scene = tmp_path / (name + ".png")
        scene.write_bytes(name.encode() * 200)
        rows.append(
            {
                "id": name,
                "generated_image": {"local_path": str(scene), "sha256": name},
                "twin_image": {"local_path": str(reference), "sha256": "reference"},
            }
        )
    packets = appearance_feedback.image_packets(rows, limit=700)
    assert [[row["id"] for row in packet] for packet in packets] == [["a", "b"], ["c"]]
    with pytest.raises(ValueError, match="One exact scene/reference"):
        appearance_feedback.image_packets(rows, limit=300)
