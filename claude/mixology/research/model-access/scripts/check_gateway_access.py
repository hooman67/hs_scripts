"""Read-only, secret-free credential-route diagnostics; never persist response bodies."""

import argparse
import concurrent.futures
import importlib.metadata
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from foundry_aws_gateway._auth import get_auth_header
from foundry_aws_gateway._constants import LLM_ACK_HEADERS


def probe(spec):
    host, path, authenticated = spec
    result = {"host": host, "path": path, "authenticated": authenticated}
    headers = {**get_auth_header(), **LLM_ACK_HEADERS} if authenticated else {}
    try:
        response = requests.get(
            host + path, headers=headers, timeout=(6, 12), allow_redirects=False
        )
        result.update(
            status=response.status_code,
            response_bytes=len(response.content),
            server=response.headers.get("server"),
            content_type=response.headers.get("content-type"),
            response_date=response.headers.get("date"),
        )
        # Successful responses contain credentials. Do not print or save their body.
        response.close()
    except requests.RequestException as error:
        result["error_type"] = type(error).__name__
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Refusing to overwrite existing diagnostic evidence")
    os.umask(0o077)
    specs = []
    for host in (
        "https://foundry-aws-pluto.adobe.io",
        "https://foundry-aws-dev-pluto.adobe.io",
    ):
        specs.extend((host, path, auth) for path, auth in (
            ("/iam/credentials/openai", True),
            ("/iam/credentials/azure", True),
            ("/iam/credentials/openai", False),
            ("/", False),
        ))
    for host in (
        "https://foundry-aws-corp.adobe.io",
        "https://foundry-aws-dev-corp.adobe.io",
    ):
        specs.append((host, "/iam/credentials/openai", True))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(probe, specs))
    report = {
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "gateway_version": importlib.metadata.version("foundry-aws-gateway"),
        "auth_header_names": sorted(get_auth_header()),
        "llm_acknowledgement_sent": True,
        "results": results,
        "scope": "Credential-route connectivity only; no model inference or service changes.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
