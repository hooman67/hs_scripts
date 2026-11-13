#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import run_judge
from test_v4_scoring import assessment


class FakeResponse:
    def __init__(self, content):
        self.model = "gpt-5.5-2026-04-24"
        self.choices = [SimpleNamespace(finish_reason="stop", message=SimpleNamespace(content=content, refusal=None))]
        self._raw = {"model": self.model, "choices": [{"message": {"content": content}, "finish_reason": "stop"}]}

    def model_dump(self, mode="json"):
        return self._raw


class FakeCompletions:
    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = 0

    def create(self, **kwargs):
        output = self.outputs[self.calls]
        self.calls += 1
        if isinstance(output, Exception):
            raise output
        return FakeResponse(output)


class FakeClient:
    def __init__(self, outputs):
        self.chat = SimpleNamespace(completions=FakeCompletions(outputs))


class RuntimeTests(unittest.TestCase):
    def test_client_uses_direct_foundry_gateway_with_sdk_retries_disabled(self):
        sentinel = object()
        calls = []

        class FakeGatewayClient:
            def with_options(self, **kwargs):
                calls.append(kwargs)
                return sentinel

        original = run_judge.foundry_aws_gateway.llm.get_openai
        run_judge.foundry_aws_gateway.llm.get_openai = lambda: FakeGatewayClient()
        try:
            actual, route = run_judge.client()
        finally:
            run_judge.foundry_aws_gateway.llm.get_openai = original

        self.assertIs(actual, sentinel)
        self.assertEqual(route, "foundry_direct_openai")
        self.assertEqual(calls, [{"timeout": 600.0, "max_retries": 0}])

    def runtime_input(self, root):
        generated = root / "generated.png"
        twin = root / "twin.png"
        generated.write_bytes(b"not-decoded-by-fake-client")
        twin.write_bytes(b"not-decoded-by-fake-client")
        return {
            "generated_image": str(generated),
            "twin_image": str(twin),
            "product_type": "laptop",
            "scene_prompt": "A simple office scene.",
            "image_stage": "scene_generation",
        }

    def test_invalid_input_returns_audited_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_judge.judge({"bad": "input"}, Path(tmp) / "run")
            self.assertEqual(result["status"], "error")
            self.assertEqual(result["error"]["code"], "invalid_input")
            self.assertEqual(len(result["raw_attempts"]), 1)
            self.assertTrue((Path(tmp) / "run/result.json").is_file())

    def test_transport_error_gets_one_bounded_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = FakeClient([RuntimeError("network down"), json.dumps(assessment())])
            original = run_judge.client
            run_judge.client = lambda: (fake, "test")
            try:
                result = run_judge.judge(self.runtime_input(root), root / "run")
            finally:
                run_judge.client = original
            self.assertEqual(result["status"], "ok")
            self.assertEqual(fake.chat.completions.calls, 2)
            self.assertEqual(result["raw_attempts"][0]["validation_status"], "transport_error")

    def test_second_transport_error_returns_explicit_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = FakeClient([RuntimeError("network down"), RuntimeError("still down")])
            original = run_judge.client
            run_judge.client = lambda: (fake, "test")
            try:
                result = run_judge.judge(self.runtime_input(root), root / "run")
            finally:
                run_judge.client = original
            self.assertEqual(result["error"]["code"], "transport_failure")
            self.assertEqual(fake.chat.completions.calls, 2)
            self.assertEqual(
                [item["validation_status"] for item in result["raw_attempts"]],
                ["transport_error", "transport_error"],
            )

    def test_invalid_structured_output_gets_one_complete_repair(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = FakeClient(["{}", json.dumps(assessment())])
            original = run_judge.client
            run_judge.client = lambda: (fake, "test")
            try:
                result = run_judge.judge(self.runtime_input(root), root / "run")
            finally:
                run_judge.client = original
            self.assertEqual(result["status"], "ok")
            self.assertEqual(fake.chat.completions.calls, 2)
            self.assertEqual([x["validation_status"] for x in result["raw_attempts"]], ["invalid", "valid"])
            self.assertTrue((root / "run/response_1.json").is_file())
            self.assertTrue((root / "run/response_2.json").is_file())

    def test_second_invalid_output_returns_explicit_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = FakeClient(["{}", "{}"])
            original = run_judge.client
            run_judge.client = lambda: (fake, "test")
            try:
                result = run_judge.judge(self.runtime_input(root), root / "run")
            finally:
                run_judge.client = original
            self.assertEqual(result["status"], "error")
            self.assertEqual(result["error"]["code"], "invalid_model_output")
            self.assertEqual(fake.chat.completions.calls, 2)
            self.assertEqual(len(result["raw_attempts"]), 2)


if __name__ == "__main__":
    unittest.main()
