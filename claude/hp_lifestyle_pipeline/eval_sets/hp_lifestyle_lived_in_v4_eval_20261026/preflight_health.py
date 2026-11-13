#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "openai>=1.50", "requests", "pyyaml", "tomli"]
# ///
"""Non-generating V4 readiness checks with redacted, durable output.

The default invocation is local-only. Network checks require explicit flags and never
submit a prompt, upload a reference, create a generation job, or publish an artifact.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

import httpx


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
V4 = PROJECT_ROOT / "research/source_messaging_v1_to_v6/versions/v4"
SHARED_SCRIPTS = PROJECT_ROOT / "research/source_messaging_v1_to_v6/scripts"
sys.path.insert(0, str(SHARED_SCRIPTS))
from probe_gpt55 import client_and_auth_mode  # noqa: E402

BASE_URL = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev"
HEALTH_URL = f"{BASE_URL}/health"
OPENAPI_URL = f"{BASE_URL}/openapi.json"
GENERATE_PATH = "/v1/image/generate"
REQUIRED_V4_FILES = (
    V4 / "system_prompt.md",
    V4 / "input.schema.json",
    V4 / "output.schema.json",
    V4 / "camera_profiles.json",
    V4 / "scripts/camera_profile_resolver.py",
    V4 / "scripts/finalize_output.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def local_check() -> dict[str, Any]:
    files = []
    for path in REQUIRED_V4_FILES:
        exists = path.is_file()
        files.append({
            "path": str(path),
            "exists": exists,
            "bytes": path.stat().st_size if exists else None,
            "sha256": sha256(path) if exists else None,
        })
    return {"ok": all(item["exists"] for item in files), "files": files}


def endpoint_check() -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "read_only": True,
        "health_url": HEALTH_URL,
        "openapi_url": OPENAPI_URL,
    }
    try:
        with httpx.Client(timeout=httpx.Timeout(30, connect=10), follow_redirects=False) as client:
            health = client.get(HEALTH_URL, headers={"accept": "application/json"})
            openapi = client.get(OPENAPI_URL, headers={"accept": "application/json"})
        document = openapi.json() if openapi.is_success else {}
        paths = document.get("paths") if isinstance(document, dict) else {}
        result.update({
            "health_status": health.status_code,
            "health_ok": health.is_success,
            "health_content_type": health.headers.get("content-type"),
            "openapi_status": openapi.status_code,
            "openapi_content_type": openapi.headers.get("content-type"),
            "generate_path_declared": isinstance(paths, dict) and GENERATE_PATH in paths,
            "generate_post_declared": isinstance(paths, dict)
                and isinstance(paths.get(GENERATE_PATH), dict)
                and "post" in paths[GENERATE_PATH],
        })
        result["ok"] = (
            openapi.is_success
            and result["generate_path_declared"]
            and result["generate_post_declared"]
        )
    except Exception as exc:
        result["error"] = {
            "type": type(exc).__name__,
            "status_code": getattr(exc, "status_code", None),
        }
    return result


def gpt_auth_check() -> dict[str, Any]:
    result: dict[str, Any] = {"ok": False, "completion_sent": False}
    try:
        client, auth_mode = client_and_auth_mode()
        result.update({"ok": True, "auth_mode": auth_mode})
        client.close()
    except Exception as exc:
        result["error"] = {
            "type": type(exc).__name__,
            "status_code": getattr(exc, "status_code", None),
        }
    return result


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", action="store_true",
                        help="GET only /health and /openapi.json; sends no generation request")
    parser.add_argument("--gpt-auth", action="store_true",
                        help="construct the shared GPT client; sends no completion")
    parser.add_argument("--output", type=Path,
                        help="optional durable redacted JSON result")
    args = parser.parse_args()

    report: dict[str, Any] = {
        "version": "hp-lifestyle-lived-in-v4-preflight-v1",
        "checked_at_utc": utc_now(),
        "network_requested": args.endpoint or args.gpt_auth,
        "generation_request_sent": False,
        "reference_upload_sent": False,
        "publication_sent": False,
        "local": local_check(),
    }
    requested = [report["local"]]
    if args.endpoint:
        report["endpoint"] = endpoint_check()
        requested.append(report["endpoint"])
    if args.gpt_auth:
        report["gpt_auth"] = gpt_auth_check()
        requested.append(report["gpt_auth"])
    report["ok"] = all(item["ok"] for item in requested)
    if args.output:
        atomic_json(args.output.resolve(), report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
