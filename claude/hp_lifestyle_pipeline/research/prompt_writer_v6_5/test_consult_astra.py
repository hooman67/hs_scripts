import json

import pytest

from research.prompt_writer_v6_5.consult_astra import (
    Collector, MODEL, REQUIRED, bind_feedback, collect_attempt,
)


def frames(finish="stop", model=MODEL):
    value = {key: [] for key in REQUIRED}
    return [
        {"id": "actual-response", "model": model, "choices": [
            {"index": 0, "delta": {"content": json.dumps(value)}, "finish_reason": None}
        ]},
        {"id": "actual-response", "model": model, "choices": [
            {"index": 0, "delta": {}, "finish_reason": finish}
        ]},
    ]


class FakeStream:
    def __init__(self, values, close_error=None):
        self.values, self.close_error = values, close_error

    def __enter__(self):
        return self

    def __iter__(self):
        for value in self.values:
            class Chunk:
                def model_dump(self, mode, value=value):
                    return value
            yield Chunk()

    def __exit__(self, *args):
        if self.close_error:
            raise self.close_error


class FakeClient:
    def __init__(self, values, close_error=None):
        self.chat = self
        self.completions = self
        self.values, self.close_error = values, close_error
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1
        return FakeStream(self.values, self.close_error)


def test_complete_stop_survives_transport_close_failure(tmp_path):
    client = FakeClient(frames(), ConnectionError("provider body must not be recorded"))
    value, receipt = collect_attempt(client, [], tmp_path)
    assert set(value) == REQUIRED
    assert receipt["finish_reason"] == "stop"
    assert receipt["post_terminal_transport_error"]["error_type"] == "ConnectionError"
    assert client.calls == 1
    assert "provider body must not be recorded" not in (tmp_path / "error.json").read_text()
    assert json.loads((tmp_path / "partial_output.txt").read_text()) == value


@pytest.mark.parametrize("finish,model", [("length", MODEL), ("stop", "gpt-5.5")])
def test_terminal_nonstop_or_wrong_model_is_not_salvaged(tmp_path, finish, model):
    client = FakeClient(frames(finish, model), ConnectionError("close"))
    with pytest.raises(ValueError, match="no resampling"):
        collect_attempt(client, [], tmp_path)
    assert client.calls == 1
    assert (tmp_path / "partial_output.txt").is_file()


def test_unfinished_stream_cannot_be_accepted():
    collector = Collector()
    collector.feed(frames()[0])
    with pytest.raises(ConnectionError, match="without terminal"):
        collector.result()


def feedback_fixture():
    dataset = {"rows": []}
    native = []
    annotations = []
    for rank in range(1, 31):
        key = f"cashmere / camera / {rank}"
        url = f"https://example.invalid/{rank}.png"
        text = f"Exact scene {rank}."
        dataset["rows"].append({
            "meta_data": {"evalset_item_id": key, "row_idx": rank},
            "images": [
                {"asset_type": "image", "image_src": url},
                {"asset_type": "text", "text_content": text},
            ],
        })
        native.append({
            "key": ["cashmere", "camera", rank],
            "prompt": {"text": text, "environment": "Office", "prop_ids": [], "camera_tag": "camera"},
            "output": {"image": url, "image_sha256": str(rank)},
        })
        annotations.append({
            "key": key, "evalset_item_id": key, "row_idx": rank, "answers": {},
            "comment": f"Exact comment {rank}\nSecond line.", "complete": True,
        })
    document = {
        "schema": "fe-html/annotations@1", "questions": [],
        "report": {"sources": ["data_source_prompts_20261110.json"]},
        "rows": annotations,
    }
    return dataset, native, document


def test_feedback_preserves_every_exact_comment_and_image_rank():
    dataset, native, document = feedback_fixture()
    result = bind_feedback(dataset, native, document)
    assert [row["feedback"]["comment"] for row in result] == [
        row["comment"] for row in document["rows"]
    ]
    assert [row["slot"] for row in result] == [row["key"] for row in native]


@pytest.mark.parametrize("changed", ["image", "prompt", "annotation_order"])
def test_feedback_rejects_cross_image_or_text_misbinding(changed):
    dataset, native, document = feedback_fixture()
    if changed == "image":
        dataset["rows"][0]["images"][0]["image_src"] = dataset["rows"][1]["images"][0]["image_src"]
    elif changed == "prompt":
        dataset["rows"][0]["images"][1]["text_content"] = "Different scene."
    else:
        document["rows"][0]["row_idx"] = 2
    with pytest.raises(ValueError, match="match|mismatch"):
        bind_feedback(dataset, native, document)
