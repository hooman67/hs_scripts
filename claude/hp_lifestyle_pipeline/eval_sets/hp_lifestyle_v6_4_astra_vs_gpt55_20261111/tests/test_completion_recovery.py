from __future__ import annotations

import copy
import json

from hp_prompt_writer_v6_4.camera import resolve_camera
from hp_prompt_writer_v6_4.service import load_assets
from recovery.complete160 import text_recovery as recovery


def test_invalid_bank_continues_actual_last_reply_with_user_role_diagnostics():
    cases = recovery.load(recovery.ROOT / "banks.json")["cases"]
    case = next(case for case in cases if case["bank_id"] == "tassel__printer_FrontCloseUp")
    messages, _, initial = recovery.seed(case)
    original = recovery.load(recovery.ROOT / "text/results/tassel__printer_FrontCloseUp.json")
    last = original["audit"]["attempts"][-1]
    assert messages[:3] == initial
    assert messages[3] == {"role": "assistant", "content": last["raw_content"]}
    assert messages[4]["role"] == "developer"
    assert messages[5]["role"] == "user"
    assert json.loads(messages[5]["content"])["validation_diagnostics_data"] == last["errors"]
    assert last["raw_content"] not in messages[4]["content"]


def test_provider_failed_bank_restarts_exact_original_initial_request():
    cases = recovery.load(recovery.ROOT / "banks.json")["cases"]
    case = next(case for case in cases if case["bank_id"] == "cashmere__laptop_FrontCloseUp")
    messages, schema, initial = recovery.seed(case)
    captured = recovery.load(recovery.ROOT / "text/journals/cashmere__laptop_FrontCloseUp/semantic_1/request.json")
    assert messages == initial == captured["messages"]
    assert schema == captured["schema"]


def test_recovery_keeps_original_validation_and_rejects_partial_bank():
    bank = "cashmere__laptop_BackRightCloseUp"
    original = recovery.load(recovery.ROOT / "text/results" / f"{bank}.json")
    attempt = original["audit"]["attempts"][-1]
    camera = resolve_camera(load_assets()["registry"], "laptop_BackRightCloseUp")
    reply = {
        "content": attempt["raw_content"],
        "model": "gpt-6-astra",
        "finish_reason": "stop",
        "refusal": None,
        "usage": {},
        "transport_attempts": 1,
    }
    request = original["audit"]["source_input"]
    assert recovery.validate(reply, request, camera)["passed"]
    partial = copy.deepcopy(json.loads(reply["content"]))
    partial["prompts"].pop()
    reply["content"] = json.dumps(partial)
    assert not recovery.validate(reply, request, camera)["passed"]
