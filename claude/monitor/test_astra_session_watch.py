"""Regression checks for automation that resumes work or signals a process."""

import argparse
import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from astra_session_watch import Monitor, Progress, retry_delay


class ProgressTests(unittest.TestCase):
    def test_child_completion_does_not_complete_parent(self):
        state = Progress()
        state.event({"type": "task_started", "turn_id": "parent"}, 100)
        state.event({"type": "task_complete", "turn_id": "child", "last_agent_message": "Done"}, 110)
        self.assertEqual(state.status, "running")

    def test_interruption_is_not_automatically_retried(self):
        state = Progress()
        state.event({"type": "task_started", "turn_id": "parent"}, 100)
        state.event({"type": "turn_aborted", "turn_id": "parent", "reason": "interrupted"}, 110)
        self.assertEqual(state.status, "interrupted")
        self.assertIsNone(state.retry_at)

    def test_builtin_retry_is_left_running(self):
        state = Progress(status="running")
        state.event({"type": "error", "will_retry": True, "message": "rate limit exceeded"}, 100)
        self.assertEqual(state.status, "running")
        self.assertIsNone(state.retry_at)

    def test_failed_turn_cannot_release_sleep_protection(self):
        state = Progress(status="running", turn_id="parent")
        state.event({"type": "error", "message": "stream disconnected"}, 100)
        state.event({"type": "task_complete", "turn_id": "parent", "last_agent_message": ""}, 101)
        self.assertEqual(state.status, "retry_pending")
        self.assertEqual(state.retry_at, 160)

    def test_empty_completion_is_not_success(self):
        state = Progress(status="running", turn_id="parent")
        state.event({"type": "task_complete", "turn_id": "parent"}, 101)
        self.assertEqual(state.status, "ended_without_confirmation")

    def test_null_completion_message_is_not_success(self):
        state = Progress(status="running", turn_id="parent")
        state.event({"type":"task_complete", "turn_id":"parent", "last_agent_message":None}, 101)
        self.assertEqual(state.status, "ended_without_confirmation")

    def test_successful_answer_can_discuss_rate_limits(self):
        state = Progress(status="running", turn_id="parent")
        state.event({"type":"task_complete", "turn_id":"parent", "last_agent_message":"Finished the task despite some rate limits."}, 101)
        self.assertEqual(state.status, "complete")

    def test_duplicate_error_does_not_delay_recovery_forever(self):
        state = Progress(status="running")
        state.fail("rate limit exceeded", 100)
        state.fail("rate limit exceeded", 130)
        self.assertEqual(state.retry_at, 160)

    def test_provider_delay_is_honored_even_above_backoff_limit(self):
        self.assertEqual(retry_delay("Retry-After: 3600", 1), 3605)
        self.assertEqual(retry_delay("try again in 30 minutes", 0), 1805)

    def test_explicit_reset_time_is_honored(self):
        with patch("astra_session_watch.time.time", return_value=0):
            self.assertEqual(retry_delay("try again at 1970-01-01T01:00:00Z", 0), 3605)


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "codex"
        self.home.mkdir()
        (self.home / "thread-writer-locks").mkdir()
        self.rollout = self.home / "rollout.jsonl"
        self.rollout.write_text(json.dumps({
            "type": "event_msg", "payload": {
                "type": "task_started", "turn_id": "previous",
            },
        }) + "\n" + json.dumps({
            "type": "event_msg", "payload": {
                "type": "task_complete", "turn_id": "previous",
                "last_agent_message": "Previously finished work",
            },
        }) + "\n")
        with sqlite3.connect(self.home / "state_5.sqlite") as con:
            con.execute("CREATE TABLE threads (id TEXT, rollout_path TEXT, cwd TEXT, model TEXT)")
            con.execute("INSERT INTO threads VALUES (?,?,?,?)", ("test-thread", str(self.rollout), str(self.base), "gpt-6-astra"))
        with sqlite3.connect(self.home / "logs_2.sqlite") as con:
            con.execute("CREATE TABLE logs (id INTEGER,ts INTEGER,level TEXT,target TEXT,feedback_log_body TEXT,thread_id TEXT)")
        self.args = argparse.Namespace(
            codex_home=self.home, state_dir=self.base / "state", thread="test-thread",
            codex="codex", dry_run=False, keep_awake_pid=12345,
            keep_awake_script=Path("/verified/helper.py"), poll_interval=1,
        )
        self.monitor = Monitor(self.args)
        self.addCleanup(self.monitor.singleton.close)

    def test_old_completion_is_not_an_actionable_completion(self):
        self.assertEqual(self.monitor.progress.status, "idle_at_start")
        self.assertEqual(self.monitor.offset, self.rollout.stat().st_size)

    def test_new_parent_completion_is_actionable(self):
        with self.rollout.open("a") as stream:
            stream.write(json.dumps({"timestamp":"2026-11-17T10:00:00Z", "type":"event_msg", "payload":{"type":"task_started","turn_id":"current"}}) + "\n")
            stream.write(json.dumps({"type":"event_msg", "payload":{"type":"task_complete","turn_id":"current","last_agent_message":"Finished the requested work"}}) + "\n")
        self.monitor.read_events()
        self.assertEqual(self.monitor.progress.status, "complete")

    def test_known_current_turn_can_finish_while_monitor_is_starting(self):
        self.args.initial_turn_id = "previous"
        self.args.state_dir = self.base / "second-state"
        watcher = Monitor(self.args)
        self.addCleanup(watcher.singleton.close)
        self.assertEqual(watcher.progress.status, "complete")

    def test_builtin_retry_log_does_not_queue_more_work(self):
        self.monitor.progress.status = "running"
        with sqlite3.connect(self.home / "logs_2.sqlite") as con:
            con.execute("INSERT INTO logs VALUES (1,100,'WARN','codex_core::responses_retry',?,?)", ("stream disconnected - retrying sampling request (6/20) rate limit exceeded", "test-thread"))
        self.monitor.read_errors()
        self.assertEqual(self.monitor.progress.status, "running")

    def test_other_thread_error_is_ignored(self):
        self.monitor.progress.status = "running"
        with sqlite3.connect(self.home / "logs_2.sqlite") as con:
            con.execute("INSERT INTO logs VALUES (1,100,'ERROR','codex_core::codex',?,?)", ("Turn error: rate limit exceeded", "other-thread"))
        self.monitor.read_errors()
        self.assertEqual(self.monitor.progress.status, "running")

    def test_terminal_error_overrides_a_misleading_completion(self):
        self.monitor.progress.status = "complete"
        with sqlite3.connect(self.home / "logs_2.sqlite") as con:
            con.execute("INSERT INTO logs VALUES (1,100,'ERROR','codex_core::codex',?,?)", ("Turn error: rate limit exceeded", "test-thread"))
        self.monitor.read_errors()
        self.assertEqual(self.monitor.progress.status, "retry_pending")

    def test_reused_pid_is_never_signaled(self):
        result = subprocess.CompletedProcess([], 0, "/different/program.py\n", "")
        with patch("astra_session_watch.subprocess.run", return_value=result), patch("astra_session_watch.os.kill") as kill:
            with self.assertRaisesRegex(RuntimeError, "identity changed"):
                self.monitor.release_sleep_protection()
            kill.assert_not_called()

    def test_correct_helper_is_signaled(self):
        result = subprocess.CompletedProcess([], 0, "python3 /verified/helper.py\n", "")
        with patch("astra_session_watch.subprocess.run", return_value=result), patch("astra_session_watch.os.kill") as kill:
            self.monitor.release_sleep_protection()
            kill.assert_called_once()
            self.assertEqual(kill.call_args.args[0], 12345)


if __name__ == "__main__":
    unittest.main()
