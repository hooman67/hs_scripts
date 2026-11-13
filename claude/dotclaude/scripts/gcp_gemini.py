# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.31"]
# ///
"""Call Google Gemini models on Vertex AI with a short-lived GCP access token.

This is the GCP/Gemini twin of azure_openai.py. It talks to the Foundry GCP
project (GCP-0805) Vertex AI REST endpoint directly, using a bearer access
token — no SDK and no ADC required.

Credentials (project + region + short-lived OAuth token) are read, in order, from:
  1. --creds <file>                 (a sourceable file with export CLOUDSDK_*/GCP_ACCESS_TOKEN lines)
  2. $GCP_ACCESS_TOKEN + $CLOUDSDK_CORE_PROJECT (+ $CLOUDSDK_COMPUTE_REGION) already in the env
  3. ~/.claude/hshariati/gcp_gemini.env
  4. ~/Downloads/creds.txt           (where ad-hoc creds are dropped)

The access token is short-lived (~1h). On 401/UNAUTHENTICATED or an expired
token, refresh the creds file (e.g. re-run `gcloud auth print-access-token`
into ~/Downloads/creds.txt) and re-run.

Examples:
  uv run --script gcp_gemini.py "Summarize this in one line: ..."
  uv run --script gcp_gemini.py -m gemini-2.5-pro -s "You are terse." "ping"
  echo "long text" | uv run --script gcp_gemini.py -m gemini-2.5-flash-lite
  uv run --script gcp_gemini.py --list          # probe which Gemini models this project can reach
  uv run --script gcp_gemini.py --json "..."    # print only the model's text reply
"""
from __future__ import annotations

import argparse
import base64
import os
import re
import sys
import time
from pathlib import Path

DEFAULT_MODEL = "gemini-2.5-flash"  # fast + cheap; fine for most tasks
DEFAULT_VEO_MODEL = "veo-3.0-generate-001"  # Veo 3, video + native audio
DEFAULT_REGION = "us-central1"
CRED_CANDIDATES = [
    Path.home() / ".claude" / "hshariati" / "gcp_gemini.env",
    Path.home() / "Downloads" / "creds.txt",
]
# Model IDs probed by --list. Availability is checked live against the project.
KNOWN_MODELS = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-pro-latest",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
]


def load_creds(explicit: str | None) -> None:
    """Populate GCP_ACCESS_TOKEN / CLOUDSDK_CORE_PROJECT / CLOUDSDK_COMPUTE_REGION in os.environ."""
    if os.environ.get("GCP_ACCESS_TOKEN") and os.environ.get("CLOUDSDK_CORE_PROJECT"):
        return
    files = [Path(explicit)] if explicit else CRED_CANDIDATES
    for f in files:
        if not f.exists():
            continue
        for line in f.read_text().splitlines():
            m = re.match(r'\s*export\s+(GCP_ACCESS_TOKEN|CLOUDSDK_\w+)\s*=\s*"?([^"]*)"?\s*$', line)
            if m:
                os.environ.setdefault(m.group(1), m.group(2))
        if os.environ.get("GCP_ACCESS_TOKEN") and os.environ.get("CLOUDSDK_CORE_PROJECT"):
            return


def base_url(region: str) -> str:
    # The "global" location uses the apex host; regional locations are host-prefixed.
    return "https://aiplatform.googleapis.com" if region == "global" else f"https://{region}-aiplatform.googleapis.com"


def model_endpoint(project: str, region: str, model: str, method: str = "generateContent") -> str:
    return (
        f"{base_url(region)}/v1/projects/{project}/locations/{region}"
        f"/publishers/google/models/{model}:{method}"
    )


def veo_generate(requests, headers, project, region, model, prompt, out, *, duration, aspect, audio, poll_timeout) -> int:
    """Submit a Veo job (async predictLongRunning), poll, and save the inline video to a local file."""
    params: dict = {"sampleCount": 1, "aspectRatio": aspect, "generateAudio": audio}
    if duration:
        params["durationSeconds"] = duration
    body = {"instances": [{"prompt": prompt}], "parameters": params}

    resp = requests.post(model_endpoint(project, region, model, "predictLongRunning"),
                         headers=headers, json=body, timeout=120)
    if resp.status_code != 200:
        msg = resp.text
        try:
            err = resp.json().get("error", {})
            msg = f"{err.get('status', resp.status_code)}: {err.get('message', '')}"
        except Exception:
            pass
        print(f"ERROR submitting Veo job [{resp.status_code}]: {msg}", file=sys.stderr)
        return 1
    op_name = resp.json().get("name")
    print(f"model:     {model}   region: {region}")
    print(f"operation: {op_name}")
    print("polling (Veo takes ~1-3 min) ...", flush=True)

    fetch_url = model_endpoint(project, region, model, "fetchPredictOperation")
    deadline = time.time() + poll_timeout
    while time.time() < deadline:
        time.sleep(10)
        pr = requests.post(fetch_url, headers=headers, json={"operationName": op_name}, timeout=60)
        if pr.status_code != 200:
            print(f"ERROR polling [{pr.status_code}]: {pr.text[:200]}", file=sys.stderr)
            return 1
        op = pr.json()
        if not op.get("done"):
            print("  ... still running", flush=True)
            continue
        if "error" in op:
            print(f"ERROR: Veo job failed: {op['error']}", file=sys.stderr)
            return 1
        # Inline output: response.videos[].bytesBase64Encoded
        videos = op.get("response", {}).get("videos", []) or op.get("response", {}).get("generatedSamples", [])
        if not videos:
            print(f"ERROR: operation done but no video in response: {str(op)[:400]}", file=sys.stderr)
            return 1
        v0 = videos[0]
        b64 = v0.get("bytesBase64Encoded") or v0.get("video", {}).get("bytesBase64Encoded")
        if not b64:
            print(f"ERROR: no inline bytes (got {list(v0.keys())}); response: {str(op)[:300]}", file=sys.stderr)
            return 1
        out_path = Path(out)
        out_path.write_bytes(base64.b64decode(b64))
        print("---")
        print(f"saved: {out_path.resolve()}  ({out_path.stat().st_size / 1e6:.1f} MB)")
        return 0
    print(f"ERROR: timed out after {poll_timeout}s; job may still finish — re-fetch operation:\n  {op_name}",
          file=sys.stderr)
    return 1


def main() -> int:
    p = argparse.ArgumentParser(description="Call a Google Gemini model on Vertex AI.")
    p.add_argument("prompt", nargs="?", help="User prompt (or pipe via stdin).")
    p.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"Gemini model id (default {DEFAULT_MODEL}).")
    p.add_argument("-s", "--system", help="Optional system instruction.")
    p.add_argument("-r", "--region", help="Vertex location (default: creds region or us-central1; 'global' allowed).")
    p.add_argument("-t", "--max-tokens", type=int, default=2048,
                   help="maxOutputTokens. 2.5 models spend 'thinking' tokens here; keep >=2048 or replies come back empty.")
    p.add_argument("--temperature", type=float, default=None, help="Optional sampling temperature.")
    p.add_argument("--creds", help="Path to a sourceable creds file.")
    p.add_argument("--list", action="store_true", help="Probe which known Gemini models this project can reach, then exit.")
    p.add_argument("--json", action="store_true", help="Print only the model's text reply (no metadata).")
    # Veo (text-to-video, async) mode:
    p.add_argument("--veo", action="store_true",
                   help="Video mode: generate an mp4 with Veo (default model veo-3.0-generate-001) and save locally.")
    p.add_argument("-o", "--out", default="veo_out.mp4", help="Output mp4 path for --veo (default veo_out.mp4).")
    p.add_argument("--duration", type=int, default=8, help="Veo clip length in seconds (default 8).")
    p.add_argument("--aspect", default="16:9", help="Veo aspect ratio, e.g. 16:9 or 9:16 (default 16:9).")
    p.add_argument("--no-audio", action="store_true", help="Veo: disable native audio (Veo 3 generates audio by default).")
    p.add_argument("--poll-timeout", type=int, default=420, help="Veo: max seconds to poll the operation (default 420).")
    args = p.parse_args()

    load_creds(args.creds)
    token = os.environ.get("GCP_ACCESS_TOKEN")
    project = os.environ.get("CLOUDSDK_CORE_PROJECT")
    region = args.region or os.environ.get("CLOUDSDK_COMPUTE_REGION") or DEFAULT_REGION
    if not token or not project:
        print("ERROR: no GCP creds. Set GCP_ACCESS_TOKEN/CLOUDSDK_CORE_PROJECT, pass --creds, "
              "or drop them in ~/Downloads/creds.txt.", file=sys.stderr)
        return 2

    import requests

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    if args.list:
        print(f"project: {project}   region: {region}")
        print("(probing — AVAILABLE means the project can call the model here)\n")
        for model in KNOWN_MODELS:
            try:
                rr = requests.post(
                    model_endpoint(project, region, model), headers=headers,
                    json={"contents": [{"role": "user", "parts": [{"text": "hi"}]}],
                          "generationConfig": {"maxOutputTokens": 1}},
                    timeout=30,
                )
            except Exception as e:
                print(f"  {model:<26} ERROR {e}")
                continue
            if rr.status_code == 200:
                print(f"  {model:<26} AVAILABLE")
            elif rr.status_code == 401:
                print(f"  {model:<26} 401 UNAUTHENTICATED (token expired — refresh creds)")
                break
            else:
                status = ""
                try:
                    status = rr.json().get("error", {}).get("status", "")
                except Exception:
                    pass
                print(f"  {model:<26} {rr.status_code} {status}")
        return 0

    prompt = args.prompt or (sys.stdin.read().strip() if not sys.stdin.isatty() else None)
    if not prompt:
        print("ERROR: no prompt (positional arg or stdin)", file=sys.stderr)
        return 2

    if args.veo:
        veo_model = args.model if args.model != DEFAULT_MODEL else DEFAULT_VEO_MODEL
        return veo_generate(
            requests, headers, project, region, veo_model, prompt, args.out,
            duration=args.duration, aspect=args.aspect, audio=not args.no_audio,
            poll_timeout=args.poll_timeout,
        )

    body: dict = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    if args.system:
        body["systemInstruction"] = {"parts": [{"text": args.system}]}
    gen: dict = {"maxOutputTokens": args.max_tokens}
    if args.temperature is not None:
        gen["temperature"] = args.temperature
    body["generationConfig"] = gen

    try:
        resp = requests.post(model_endpoint(project, region, args.model), headers=headers, json=body, timeout=120)
    except Exception as e:
        print(f"ERROR calling {args.model}: {e}", file=sys.stderr)
        return 1

    if resp.status_code != 200:
        msg = resp.text
        try:
            err = resp.json().get("error", {})
            msg = f"{err.get('status', resp.status_code)}: {err.get('message', '')}"
        except Exception:
            pass
        hint = "  (token expired — refresh ~/Downloads/creds.txt)" if resp.status_code == 401 else ""
        print(f"ERROR calling {args.model} [{resp.status_code}]: {msg}{hint}", file=sys.stderr)
        return 1

    data = resp.json()
    cands = data.get("candidates", [])
    finish = cands[0].get("finishReason", "?") if cands else "?"
    parts = cands[0].get("content", {}).get("parts", []) if cands else []
    content = "".join(part.get("text", "") for part in parts)

    if args.json:
        print(content)
        return 0
    print(f"model:         {data.get('modelVersion', args.model)}   region: {region}")
    print(f"finish_reason: {finish}")
    print(f"usage:         {data.get('usageMetadata')}")
    print("---")
    print(content or "<empty> (raise -t/--max-tokens; 2.5 models spend it on thinking when finish_reason=MAX_TOKENS)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
