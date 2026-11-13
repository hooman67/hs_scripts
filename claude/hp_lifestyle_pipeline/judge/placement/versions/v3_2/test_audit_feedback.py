"""A completed audit packet is reused only with identical source inputs."""

import json

import audit_feedback
import common
import pytest


def packet(tmp_path):
    inputs, schema = {"cases": ["scene"]}, {"type": "object"}
    common.write_json(tmp_path / "input.json", inputs)
    common.write_json(tmp_path / "schema.json", schema)
    attempt = tmp_path / "attempt01"
    attempt.mkdir()
    raw = attempt / "chunks.jsonl"
    raw.write_text(
        json.dumps(
            {
                "model": common.MODEL,
                "id": "test-response",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": '{"records":[]}'},
                        "finish_reason": "stop",
                    }
                ],
            }
        )
        + "\n"
    )
    receipt = {"chunks_path": str(raw), "chunks_sha256": common.sha(raw)}
    common.write_json(attempt / "receipt.json", receipt)
    return inputs, schema, receipt


def test_normal_completed_attempt_can_be_finalized_without_another_model_call(tmp_path):
    inputs, schema, receipt = packet(tmp_path)
    assert audit_feedback.completed_packet(tmp_path, inputs, schema) == (
        {"records": []},
        receipt,
    )


def test_completed_audit_is_not_reused_for_changed_inputs_or_changed_result(tmp_path):
    inputs, schema, _ = packet(tmp_path)
    with pytest.raises(ValueError, match="request changed"):
        audit_feedback.completed_packet(tmp_path, {"cases": ["different"]}, schema)
    common.write_json(tmp_path / "result.json", {"records": ["invented"]})
    with pytest.raises(ValueError, match="actual Astra stream"):
        audit_feedback.completed_packet(tmp_path, inputs, schema)


def test_unfinished_packet_is_not_silently_resampled(tmp_path):
    inputs, schema, _ = packet(tmp_path)
    (tmp_path / "attempt01/receipt.json").unlink()
    with pytest.raises(ValueError, match="explicit transport diagnosis"):
        audit_feedback.completed_packet(tmp_path, inputs, schema)


def test_native_audit_batches_whole_pairs_and_retains_every_full_image_and_tile(
    tmp_path,
):
    reference = tmp_path / "reference.png"
    reference.write_bytes(b"synthetic reference bytes")
    cases, records = [], []
    for number, size in enumerate((14_000_000, 18_000_000)):
        scene, tile = tmp_path / f"scene{number}.png", tmp_path / f"tile{number}.png"
        scene.write_bytes(f"synthetic scene {number}".encode())
        tile.write_bytes(f"synthetic tile {number}".encode())
        images = [
            {"local_path": str(path), "sha256": common.sha(path), "label": label}
            for path, label in (
                (scene, "A: full"),
                (reference, "B: full"),
                (tile, "A: tile"),
            )
        ]
        case = {
            "id": str(number),
            "generated_image": images[0],
            "twin_image": images[1],
        }
        visual = {
            "identity": {
                "sources": {
                    role: case[role] for role in ("generated_image", "twin_image")
                }
            },
            "delivered_images": images,
            "base64_image_bytes": size,
        }
        path = tmp_path / f"packet{number}.json"
        common.write_json(path, visual)
        records.append(
            {
                "id": case["id"],
                "packet_path": str(path),
                "packet_sha256": common.sha(path),
            }
        )
        cases.append(case)
    common.write_json(
        tmp_path / "evaluation/visual_preflight.json", {"records": records}
    )
    packets = audit_feedback.native_packets(tmp_path, cases)
    assert [[case["id"] for case in packet] for packet in packets] == [["0"], ["1"]]
    assert [
        len(case["actual_visual_packet"]["delivered_images"])
        for packet in packets
        for case in packet
    ] == [3, 3]
    parts = audit_feedback.audit_parts([case for packet in packets for case in packet])
    assert sum(part["type"] == "image_url" for part in parts) == 5
    (tmp_path / "packet0.json").write_text("{}")
    with pytest.raises(ValueError, match="Frozen native audit packet changed"):
        audit_feedback.native_packets(tmp_path, cases)
