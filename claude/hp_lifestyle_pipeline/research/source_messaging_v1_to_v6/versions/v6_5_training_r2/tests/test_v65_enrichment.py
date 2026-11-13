import copy
import json
from pathlib import Path

from research.source_messaging_v1_to_v6.versions.v6_5_training_r2 import runtime
from research.source_messaging_v1_to_v6.versions.v6_5_training_r2.validation import validate_output
from research.source_messaging_v1_to_v6.versions.v6_5_training_r2.tests.test_runtime import (
    FakeProvider, approved_catalog, references, registry, request, response, valid_output,
)

HERE = Path(__file__).resolve().parents[1]


def carrier_fixture():
    entries = [
        {
            "id": "OFF-LEDGE", "environment": "Office",
            "role": "background_furnishing_or_decor", "name": "floating ledge",
            "repetition_groups": ["wall_shelving", "ceramic_object"],
            "aliases": ["floating ledge"],
        },
        {
            "id": "OFF-CERAMIC", "environment": "Office",
            "role": "tabletop_or_movable", "name": "abstract ceramic object",
            "repetition_groups": ["ceramic_object"], "aliases": ["abstract ceramic object"],
        },
    ]
    catalog = approved_catalog(entries=entries)
    output = valid_output()
    output["prompts"][0].update(
        text="An office desk anchors a meeting area. A floating ledge holds an abstract ceramic object.",
        prop_ids=["OFF-LEDGE", "OFF-CERAMIC"],
        prop_mentions=[
            {"id": "OFF-LEDGE", "quote": "floating ledge"},
            {"id": "OFF-CERAMIC", "quote": "abstract ceramic object"},
        ],
    )
    return output, catalog


def validate(output, catalog):
    camera = {"device_family": "laptop", "framing": "medium", "elevation": "level"}
    return validate_output(output, request(), catalog, camera, references())


def test_composite_carrier_and_explicit_content_share_only_the_component_family():
    output, catalog = carrier_fixture()
    result = validate(output, catalog)
    assert result["passed"], result["errors"]


def test_composite_name_does_not_waive_a_separate_content_declaration():
    output, catalog = carrier_fixture()
    output["prompts"][0]["prop_ids"] = ["OFF-LEDGE"]
    output["prompts"][0]["prop_mentions"] = output["prompts"][0]["prop_mentions"][:1]
    result = validate(output, catalog)
    assert "visible_contents_missing" in {error["code"] for error in result["errors"]}


def test_unrelated_object_cannot_claim_the_carrier_content_exception():
    output, catalog = carrier_fixture()
    output["prompts"][0]["text"] = (
        "An office desk anchors a meeting area. A floating ledge is mounted on the wall. "
        "An abstract ceramic object rests on the desk."
    )
    result = validate(output, catalog)
    assert "duplicate_physical_prop" not in {error["code"] for error in result["errors"]}
    assert "visible_contents_missing" in {error["code"] for error in result["errors"]}


def test_exact_duplicate_scene_is_still_rejected():
    output, catalog = carrier_fixture()
    output["prompts"][1] = copy.deepcopy(output["prompts"][0])
    result = validate(output, catalog)
    assert "duplicate_prompt_text" in {error["code"] for error in result["errors"]}


def test_astra_usage_guidance_is_trusted_configuration_not_an_extra_user_input():
    catalog = json.loads((HERE / "approved-v6.5-20261111.catalog.json").read_text())
    provider = FakeProvider([response(valid_output())])
    result = runtime.run_writer(
        request(), catalog=catalog, registry=registry(), provider=provider,
        system_prompt=(HERE / "system_prompt.md").read_text(), references=references(),
    )
    assert result["status"] == "ok", result
    messages = provider.calls[0]["messages"]
    trusted = json.loads(messages[1]["content"])
    assert messages[1]["role"] == "system"
    assert trusted["approved_prop_usage_guidance"] == json.loads(
        (HERE / "prop_guidance.json").read_text()
    )["entries"]
    assert set(json.loads(messages[2]["content"])) == {"smart_brief", "source_messaging", "camera_tag"}


def test_missing_new_prop_usage_guidance_fails_before_provider(tmp_path, monkeypatch):
    invalid = tmp_path / "guidance.json"
    invalid.write_text(json.dumps({"version": "hp-v6.5-approved-props-v1", "entries": []}))
    monkeypatch.setattr(runtime, "PROP_GUIDANCE_PATH", invalid)
    provider = FakeProvider([])
    catalog = json.loads((HERE / "approved-v6.5-20261111.catalog.json").read_text())
    result = runtime.run_writer(
        request(), catalog=catalog, registry=registry(), provider=provider,
        system_prompt="Write scenes.", references=references(),
    )
    assert result["status"] == "error"
    assert result["error"]["code"] == "configuration_invalid"
    assert provider.calls == []
