#!/usr/bin/env python3
"""Compile the root-authored V4 template with a pinned camera-registry copy."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION = HERE.parent
ROOT = VERSION.parents[3]
sys.path.insert(0, str(HERE))

from camera_profile_resolver import load_registry  # noqa: E402

V2_COMPILER = ROOT / "research/source_messaging_v1_to_v6/versions/v2/build_system_prompt.py"
PLACEHOLDER = "{{OFFLINE_NOTES}}"


def _load_v2_compiler():
    import importlib.util

    spec = importlib.util.spec_from_file_location("pinned_v2_prompt_compiler", V2_COMPILER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def compile_prompt(template: str, registry: dict) -> str:
    """Use the established V2 note renderer against only the pinned local copy."""

    if template.count(PLACEHOLDER) != 1:
        raise ValueError("template must contain exactly one offline-notes placeholder")
    return _load_v2_compiler().compile_prompt(template, registry)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=VERSION / "camera_profiles.json")
    parser.add_argument("--template", type=Path, default=VERSION / "system_prompt.template.md")
    parser.add_argument("--output", type=Path, default=VERSION / "system_prompt.md")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    compiled = compile_prompt(args.template.read_text(), load_registry(args.registry))
    if args.check:
        if not args.output.exists() or args.output.read_text() != compiled:
            raise SystemExit(f"compiled output is stale or missing: {args.output}")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(compiled)
    print(json.dumps({"output": str(args.output), "characters": len(compiled),
                      "sha256": hashlib.sha256(compiled.encode()).hexdigest(),
                      "check": args.check}, indent=2))


if __name__ == "__main__":
    main()
