#!/usr/bin/env python3
"""Completion-gate regressions for the progressive generation supervisor."""

from __future__ import annotations

import unittest

import watch_generation as watch


class WatchCompletionTests(unittest.TestCase):
    def complete_status(self) -> dict:
        return {
            "accepted_case_count": 369,
            "manifest_case_count": 369,
            "summary_accepted_case_count": 369,
            "summary_matches_current_accepted_snapshot": True,
            "current_missing_terminal_row_count": 0,
            "pending_job_count": 0,
            "safe_retry_job_count": 0,
            "selected_missing_record_count": 0,
        }

    def test_complete_only_for_matching_current_snapshot(self) -> None:
        self.assertTrue(watch.is_finished(self.complete_status()))

    def test_evolved_map_cannot_finish_from_fully_done_old_snapshot(self) -> None:
        status = self.complete_status()
        status.update(
            {
                "summary_matches_current_accepted_snapshot": False,
                "current_missing_terminal_row_count": 1400,
                # The old snapshot's 335 rows may all be terminal.
                "available_generation_row_count": 335,
                "record_count": 335,
                "record_status_counts": {"done": 335},
            }
        )
        self.assertFalse(watch.is_finished(status))

    def test_pending_or_safe_retry_blocks_completion(self) -> None:
        pending = self.complete_status()
        pending["pending_job_count"] = 1
        self.assertFalse(watch.is_finished(pending))
        retry = self.complete_status()
        retry["safe_retry_job_count"] = 1
        self.assertFalse(watch.is_finished(retry))


if __name__ == "__main__":
    unittest.main()
