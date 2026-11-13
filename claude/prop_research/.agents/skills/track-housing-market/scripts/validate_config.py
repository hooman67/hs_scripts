#!/usr/bin/env python3
"""Validate the repository housing-tracker configuration."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path


DEFAULT_CONFIG = Path(
    "/home/colligo/hs_scripts/claude/prop_research/"
    "tracking_housing_process/config/tracker_config.json"
)
ALLOWED_STATUSES = {"AWAITING_AUDITED_SHORTLIST", "PILOT", "ACTIVE", "PAUSED"}
ALLOWED_ACCESS_MODES = {
    "PUBLIC_DOWNLOAD",
    "PUBLIC_API",
    "LICENSED_API",
    "LICENSED_EXPORT",
    "MANUAL",
}


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def parse_iso_date(value: object, field: str, errors: list[str]) -> date | None:
    if not nonempty_string(value):
        errors.append(f"{field} must be an ISO date")
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        errors.append(f"{field} must be an ISO date")
        return None


def parse_iso_datetime(value: object, field: str, errors: list[str]) -> datetime | None:
    if not nonempty_string(value):
        errors.append(f"{field} must be an ISO datetime")
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{field} must be an ISO datetime")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{field} must include a timezone")
        return None
    return parsed


def validate_object_list(
    config: dict, key: str, required_fields: set[str], errors: list[str]
) -> set[str]:
    values = config.get(key, [])
    if not isinstance(values, list):
        return set()
    ids: list[str] = []
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            errors.append(f"{key}[{index}] must be an object")
            continue
        missing = sorted(required_fields - value.keys())
        if missing:
            errors.append(f"{key}[{index}] missing keys: {', '.join(missing)}")
        identifier = value.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append(f"{key}[{index}].id must be a non-empty string")
        else:
            ids.append(identifier)
    duplicates = sorted({identifier for identifier in ids if ids.count(identifier) > 1})
    if duplicates:
        errors.append(f"duplicate {key} ids: {', '.join(duplicates)}")
    return set(ids)


def validate(config: dict) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "status",
        "project",
        "markets",
        "cohorts",
        "authorized_sources",
        "pilot",
        "alert_rules",
        "last_successful_run",
        "manual_input_directory",
        "runs_directory",
    }
    missing = sorted(required - config.keys())
    if missing:
        errors.append(f"missing keys: {', '.join(missing)}")

    status = config.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"invalid status: {status!r}")

    for key in ("markets", "cohorts", "authorized_sources"):
        if key in config and not isinstance(config[key], list):
            errors.append(f"{key} must be a list")

    market_ids = validate_object_list(
        config, "markets", {"id", "name", "boundary"}, errors
    )
    cohort_ids = validate_object_list(
        config,
        "cohorts",
        {"id", "market_id", "version", "property_type", "filters"},
        errors,
    )
    source_ids = validate_object_list(
        config,
        "authorized_sources",
        {"id", "access_mode", "authorized", "terms_checked_at"},
        errors,
    )

    for index, cohort in enumerate(config.get("cohorts", [])):
        if not isinstance(cohort, dict):
            continue
        if cohort.get("market_id") not in market_ids:
            errors.append(f"cohorts[{index}].market_id must reference a configured market")
        for key in ("version", "property_type"):
            if not nonempty_string(cohort.get(key)):
                errors.append(f"cohorts[{index}].{key} must be a non-empty string")
        if not isinstance(cohort.get("filters"), dict):
            errors.append(f"cohorts[{index}].filters must be an object")
    for index, market in enumerate(config.get("markets", [])):
        if not isinstance(market, dict):
            continue
        if not nonempty_string(market.get("name")):
            errors.append(f"markets[{index}].name must be a non-empty string")
        boundary = market.get("boundary")
        if not isinstance(boundary, (str, dict)) or not boundary:
            errors.append(f"markets[{index}].boundary must be a non-empty string or object")
    for index, source in enumerate(config.get("authorized_sources", [])):
        if not isinstance(source, dict):
            continue
        if source.get("access_mode") not in ALLOWED_ACCESS_MODES:
            errors.append(f"authorized_sources[{index}].access_mode is invalid")
        if source.get("authorized") is not True:
            errors.append(f"authorized_sources[{index}].authorized must be true")
        checked = parse_iso_date(
            source.get("terms_checked_at"),
            f"authorized_sources[{index}].terms_checked_at",
            errors,
        )
        if checked:
            age_days = (date.today() - checked).days
            if age_days < 0:
                errors.append(f"authorized_sources[{index}].terms_checked_at is in the future")
            elif age_days > 90:
                errors.append(f"authorized_sources[{index}] terms check is older than 90 days")

    for key in ("manual_input_directory", "runs_directory"):
        value = config.get(key)
        if not isinstance(value, str) or not Path(value).is_absolute():
            errors.append(f"{key} must be an absolute path")

    pilot = config.get("pilot")
    if not isinstance(pilot, dict):
        errors.append("pilot must be an object")
        pilot = {}
    else:
        for key in ("market_id", "completed", "reviewed_at"):
            if key not in pilot:
                errors.append(f"pilot missing key: {key}")
        if "completed" in pilot and not isinstance(pilot["completed"], bool):
            errors.append("pilot.completed must be a boolean")

    if status in {"PILOT", "ACTIVE"}:
        if not config.get("markets"):
            errors.append(f"{status} configuration requires at least one market")
        if not config.get("cohorts"):
            errors.append(f"{status} configuration requires at least one cohort")
        if not config.get("authorized_sources"):
            errors.append(f"{status} configuration requires at least one authorized source")
        for key in ("manual_input_directory", "runs_directory"):
            value = config.get(key)
            if isinstance(value, str) and not Path(value).is_dir():
                errors.append(f"{status} configuration requires existing directory: {key}")

    if status in {"PILOT", "ACTIVE"}:
        if not pilot.get("market_id"):
            errors.append(f"{status} configuration requires pilot.market_id")
        elif pilot.get("market_id") not in market_ids:
            errors.append("pilot.market_id must reference a configured market id")

    if status == "ACTIVE":
        if not pilot.get("completed"):
            errors.append("ACTIVE configuration requires a completed, reviewed pilot")
        parse_iso_datetime(pilot.get("reviewed_at"), "pilot.reviewed_at", errors)
        alert_rules = config.get("alert_rules")
        if not isinstance(alert_rules, dict):
            errors.append("ACTIVE configuration requires versioned alert_rules")
        else:
            if not nonempty_string(alert_rules.get("version")):
                errors.append("alert_rules.version must be a non-empty string")
            definitions = alert_rules.get("definitions")
            if not isinstance(definitions, (dict, list)) or not definitions:
                errors.append("alert_rules.definitions must be a non-empty object or list")
        last_run = config.get("last_successful_run")
        if not isinstance(last_run, dict):
            errors.append("ACTIVE configuration requires last_successful_run object")
        else:
            for key in ("run_id", "completed_at", "report_path"):
                if not nonempty_string(last_run.get(key)):
                    errors.append(f"last_successful_run.{key} must be a non-empty string")
            parse_iso_datetime(
                last_run.get("completed_at"), "last_successful_run.completed_at", errors
            )
            report_path = last_run.get("report_path")
            if isinstance(report_path, str) and not Path(report_path).is_absolute():
                errors.append("last_successful_run.report_path must be an absolute path")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()

    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 1

    errors = validate(config)
    market_ids = {
        value.get("id")
        for value in config.get("markets", [])
        if isinstance(value, dict) and isinstance(value.get("id"), str)
    }
    cohort_ids = {
        value.get("id")
        for value in config.get("cohorts", [])
        if isinstance(value, dict) and isinstance(value.get("id"), str)
    }
    source_ids = {
        value.get("id")
        for value in config.get("authorized_sources", [])
        if isinstance(value, dict) and isinstance(value.get("id"), str)
    }
    schema_valid = not errors
    activation_ready = (
        schema_valid
        and config.get("status") == "ACTIVE"
        and bool(config.get("markets"))
        and bool(config.get("cohorts"))
        and bool(config.get("authorized_sources"))
    )
    result = {
        "schema_valid": schema_valid,
        "activation_ready": activation_ready,
        "status": config.get("status"),
        "market_count": len(config.get("markets", [])) if isinstance(config.get("markets"), list) else None,
        "cohort_count": len(config.get("cohorts", [])) if isinstance(config.get("cohorts"), list) else None,
        "source_count": len(config.get("authorized_sources", [])) if isinstance(config.get("authorized_sources"), list) else None,
        "market_ids": sorted(market_ids),
        "cohort_ids": sorted(cohort_ids),
        "source_ids": sorted(source_ids),
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if schema_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
