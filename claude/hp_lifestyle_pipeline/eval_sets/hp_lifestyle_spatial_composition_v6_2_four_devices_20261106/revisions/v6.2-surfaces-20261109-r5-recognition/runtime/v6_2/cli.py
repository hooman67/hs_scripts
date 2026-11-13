#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["jsonschema", "openai>=1.50", "requests", "pyyaml", "tomli", "foundry-aws-gateway[llm]>=2.0.0"]
# ///
"""Compile approval decisions or run the bounded V6 service on one input."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from v6_2.catalog import compile_catalog, validate_catalog
from v6_2.provider import GPT55Provider, ProviderUnavailable
from v6_2.runtime import run_writer


def write_exclusive(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    compile_cmd = commands.add_parser("compile-catalog")
    compile_cmd.add_argument("--csv", type=Path, required=True)
    compile_cmd.add_argument("--revision", required=True)
    compile_cmd.add_argument("--output", type=Path, required=True)
    check_cmd = commands.add_parser("check-catalog")
    check_cmd.add_argument("--catalog", type=Path, required=True)
    run_cmd = commands.add_parser("run")
    run_cmd.add_argument("--input", type=Path, required=True)
    run_cmd.add_argument("--catalog", type=Path, required=True)
    run_cmd.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "compile-catalog":
        catalogue = compile_catalog(args.csv, args.revision)
        write_exclusive(args.output, catalogue)
        print(json.dumps({"approved_entries": len(catalogue["entries"]), "output": str(args.output.resolve())}))
        return 0
    if args.command == "check-catalog":
        try:
            catalogue = json.loads(args.catalog.read_text())
            validate_catalog(catalogue)
        except (ValueError, OSError) as exc:
            print(json.dumps({"status": "error", "message": str(exc)}))
            return 2
        print(json.dumps({"status": "ok", "approved_entries": len(catalogue["entries"])}))
        return 0
    # Reserve a unique run journal before calling a provider. Interrupted attempts
    # stay visible; the CLI never resumes an ambiguous call or overwrites a run.
    if args.output.exists():
        raise FileExistsError("output already exists; choose a new run path")
    journal = args.output.with_suffix(args.output.suffix + ".run")
    journal.mkdir(parents=True, exist_ok=False)
    provider = GPT55Provider()
    call_index = 0

    def recorded_provider(messages, schema):
        nonlocal call_index
        call_index += 1
        stem = journal / f"attempt_{call_index}"
        write_exclusive(stem.with_suffix(".request.json"), {"messages": messages, "schema": schema})
        try:
            reply = provider(messages, schema)
        except Exception as exc:
            details = {"type": type(exc).__name__, "code": "provider_error", "transport_attempts": None}
            if isinstance(exc, ProviderUnavailable):
                details.update(code=exc.code, status_code=exc.status_code,
                               transport_attempts=exc.attempts, transport_events=exc.events)
            write_exclusive(stem.with_suffix(".provider_error.json"), details)
            raise
        write_exclusive(stem.with_suffix(".response.json"), reply)
        return reply

    try:
        request = json.loads(args.input.read_text())
        catalogue = json.loads(args.catalog.read_text())
        registry = json.loads((HERE / "camera_profiles.json").read_text())
        references = json.loads((HERE / "reference_library.json").read_text())
        system_prompt = (HERE / "system_prompt.md").read_text()
    except (OSError, ValueError):
        result = {"status": "error", "error": {"code": "preflight_read_failed",
                  "message": "An input or configuration file could not be read as required."},
                  "audit": {"attempts": [], "semantic_calls": 0, "transport_attempts_known": 0,
                            "transport_accounting_complete": True}}
    else:
        result = run_writer(request, catalog=catalogue, registry=registry,
                            references=references, provider=recorded_provider,
                            system_prompt=system_prompt)
    write_exclusive(args.output, result)
    print(json.dumps({"status": result["status"], "semantic_calls": call_index,
                      "transport_attempts_known": result["audit"]["transport_attempts_known"],
                      "transport_accounting_complete": result["audit"]["transport_accounting_complete"],
                      "output": str(args.output.resolve())}))
    return 0 if result["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
