from supervise_generation import classify_summary


def summary(**overrides):
    value = {
        "expected_generation_row_count": 108,
        "selected_generation_row_count": 108,
        "record_count": 108,
        "record_status_counts": {"done": 108},
        "selected_missing_record_count": 0,
        "pending_job_count": 0,
        "safe_retry_job_count": 0,
        "ambiguous_submission_count": 0,
    }
    value.update(overrides)
    return value


def test_stops_when_all_rows_done():
    assert classify_summary(summary())["action"] == "stop_complete"


def test_resumes_known_pending_job():
    value = summary(record_status_counts={"done": 107, "pending": 1}, pending_job_count=1)
    assert classify_summary(value)["action"] == "resume"


def test_resumes_safe_retry_or_missing_rows():
    safe = summary(record_status_counts={"done": 107, "failed": 1}, safe_retry_job_count=1)
    missing = summary(record_count=107, record_status_counts={"done": 107}, selected_missing_record_count=1)
    assert classify_summary(safe)["action"] == "resume"
    assert classify_summary(missing)["action"] == "resume"


def test_stops_without_retry_when_only_ambiguous_rows_remain():
    value = summary(record_status_counts={"done": 107, "failed": 1}, ambiguous_submission_count=1)
    assert classify_summary(value)["action"] == "stop_ambiguous"


def test_stops_when_all_rows_are_terminally_accounted():
    value = summary(record_status_counts={"done": 106, "failed": 2})
    assert classify_summary(value)["action"] == "stop_terminal"


def test_stops_for_review_when_scope_or_accounting_is_inconsistent():
    wrong_scope = summary(selected_generation_row_count=107)
    unaccounted = summary(record_count=107, record_status_counts={"done": 107})
    assert classify_summary(wrong_scope)["action"] == "stop_review"
    assert classify_summary(unaccounted)["action"] == "stop_review"
