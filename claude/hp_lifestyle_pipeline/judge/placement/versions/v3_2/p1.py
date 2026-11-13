"""Complementary primaries with unchanged V3 additions-consensus aggregation."""

from pathlib import Path

import common


def judge(runtime_input, output, client=None):
    common.LEGACY.SCORING.validate_runtime_input(runtime_input)
    output = Path(output)
    baseline = common.call_stage(
        runtime_input,
        "p1_baseline",
        output / "baseline",
        common.LEGACY.SCORING.OBSERVATION_SCHEMA,
        common.LEGACY.validate_new_observation,
        client=client,
    )
    compact = common.call_stage(
        runtime_input,
        "p1_compact",
        output / "compact",
        common.LEGACY.SCORING.OBSERVATION_SCHEMA,
        common.LEGACY.validate_new_observation,
        client=client,
    )
    names = common.LEGACY.trigger_names(baseline["observation"], compact["observation"])
    stages = {"baseline": baseline, "compact": compact}
    checks = {}
    for role in ("proposal", "independent") if names else ():
        schema = common.LEGACY.component_schema(names)
        reports = {"requested_components": names}
        if role == "proposal":
            reports["proposals"] = {
                name: compact["observation"]["components"][name] for name in names
            }
        checks[role] = common.call_stage(
            runtime_input,
            "p1_" + role,
            output / role,
            schema,
            lambda value, schema=schema: common.LEGACY.validate_components(
                value, schema
            ),
            reports=reports,
            cap=6000,
            client=client,
        )
        stages[role] = checks[role]
    result = {
        "candidate": "p1",
        "protocol_version": "placement-v3.2-p1-r1",
        "ok": True,
        "runtime_input": runtime_input,
        "protocol_freeze_sha256": common.verify_freeze(),
        "stages": {
            role: {
                "path": str((output / role / "result.json").resolve()),
                "sha256": common.sha(output / role / "result.json"),
            }
            for role in stages
        },
        **common.LEGACY.aggregate_stages(
            baseline["observation"],
            compact["observation"],
            checks.get("proposal", {}).get("observation"),
            checks.get("independent", {}).get("observation"),
        ),
    }
    common.write_json(output / "result.json", result)
    return result
