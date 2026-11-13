from supervise_generation import classify_summary


def summary(**overrides):
    value = {
        "expected_generation_row_count": 120,
        "selected_generation_row_count": 120,
        "record_count": 120,
        "record_status_counts": {"done": 120},
        "selected_missing_record_count": 0,
        "pending_job_count": 0,
        "safe_retry_job_count": 0,
        "ambiguous_submission_count": 0,
    }
    value.update(overrides)
    return value


def test_stops_when_all_rows_done():
    assert classify_summary(summary())["action"] == "stop_complete"


def test_resumes_known_pending_or_missing_work():
    pending = summary(record_status_counts={"done": 119, "pending": 1}, pending_job_count=1)
    missing = summary(record_count=4, record_status_counts={"done": 4}, selected_missing_record_count=116)
    assert classify_summary(pending)["action"] == "resume"
    assert classify_summary(missing)["action"] == "resume"


def test_stops_without_retry_on_ambiguous_submission():
    value = summary(record_status_counts={"done": 119, "failed": 1}, ambiguous_submission_count=1)
    assert classify_summary(value)["action"] == "stop_ambiguous"


def test_rejects_non_120_scope():
    assert classify_summary(summary(selected_generation_row_count=4))["action"] == "stop_review"
