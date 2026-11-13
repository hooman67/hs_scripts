import json
import unittest

import httpx2
import openai

from resume_synthesis import Collector, IncompleteStreamError, retryable, validate_proposals


class ResumeTests(unittest.TestCase):
    def test_usage_frame_and_fragmented_json_are_preserved(self):
        state = Collector()
        for text in ('{"pro', 'posals": []}'):
            state.feed({"id": "test", "model": "gpt-6-astra", "choices": [{
                "index": 0, "delta": {"content": text}, "finish_reason": None}]})
        state.feed({"id": "test", "model": "gpt-6-astra", "choices": [{
            "index": 0, "delta": {}, "finish_reason": "stop"}]})
        state.feed({"choices": [], "usage": {"total_tokens": 12}})
        self.assertEqual(state.result(), {"proposals": []})
        self.assertEqual(state.usage, {"total_tokens": 12})

    def test_truncated_transport_is_retryable_but_model_limit_is_not(self):
        state = Collector()
        with self.assertRaises(IncompleteStreamError) as incomplete:
            state.result()
        self.assertTrue(retryable(incomplete.exception))
        state.finish = "length"
        with self.assertRaises(ValueError) as limited:
            state.result()
        self.assertFalse(retryable(limited.exception))

    def test_timeout_and_server_failures_retry_but_auth_does_not(self):
        self.assertTrue(retryable(TimeoutError()))
        request = httpx2.Request("POST", "https://example.invalid/")
        for code, expected in ((429, True), (503, True), (401, False), (400, False)):
            response = httpx2.Response(code, request=request)
            error = openai.APIStatusError("test", response=response, body=None)
            self.assertEqual(retryable(error), expected)

    def test_wrong_model_is_not_accepted(self):
        state = Collector()
        state.feed({"model": "another-model", "choices": [{
            "index": 0, "delta": {"content": "{}"}, "finish_reason": "stop"}]})
        with self.assertRaises(ValueError):
            state.result()

    def test_unsafe_duplicate_or_missing_prompt_artifacts_rejected(self):
        sample = {
            "proposals": [
                {"id": f"p{i}", "system_prompts": [{
                    "artifact_name": "baseline.txt", "role": "baseline", "text": "Test prompt"}]}
                for i in range(3)],
            "historical_anchor_reconciliation": [{"case_id": str(i)} for i in range(6)],
        }
        expected = {str(i) for i in range(6)}
        validate_proposals(sample, expected)
        for change in ("unsafe", "duplicate", "missing_anchor"):
            edited = json.loads(json.dumps(sample))
            if change == "unsafe":
                edited["proposals"][0]["system_prompts"][0]["artifact_name"] = "../escape"
            elif change == "duplicate":
                edited["proposals"][0]["system_prompts"] *= 2
            else:
                edited["historical_anchor_reconciliation"].pop()
            with self.assertRaises(ValueError):
                validate_proposals(edited, expected)


if __name__ == "__main__":
    unittest.main()
