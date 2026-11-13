# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml"]
# ///
"""Call Adobe Foundry GPT-5.x (Azure OpenAI) with one entry point. Default: gpt-5.6-terra.

Two credential paths, tried in order:
  1. AUTO-MINT from a Pluto token (preferred; long-lived, self-refreshing) — mints a short-lived
     Azure AD bearer from the Foundry auth service, exactly as videogen/core/llm.py does.
     Token resolution: $PLUTO_TOKEN → credentials.yaml (foundry_aws.pluto_token) → creds.txt.
  2. PASTED bearer — reads AZURE_OPENAI_ENDPOINT + AZURE_OPENAI_AD_TOKEN from env, creds.txt, or
     ~/.claude/hshariati/azure_openai.env. Short-lived (~1h); re-paste when it 401s.

Deployment facts that are NOT preferences (from the 5.x deployment):
  * use `max_completion_tokens`, never `max_tokens`
  * OMIT `temperature` (some 5.6 deployments reject any non-default value)
  * api_version 2025-04-01-preview
  * the bearer expires ~60 min; auto-mint re-mints, pasted must be refreshed

Model note: gpt-5.6-terra is the project default (fast, Steve's call). gpt-5.6-luna scored higher on
the vault's *structured-rewrite* benchmark (100% vs 97%); switch with --model or $GPT_MODEL.

CLI:
  uv run --script gpt_call.py "one-off prompt"
  uv run --script gpt_call.py --model gpt-5.6-luna -s "You are terse." "ping"
  echo '{...}' | uv run --script gpt_call.py --json "extract fields as JSON"
  uv run --script gpt_call.py --status
Import:
  from gpt_call import ask, ask_json
  d = ask_json("...", system="...")
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from pathlib import Path

MODEL = os.environ.get("GPT_MODEL", "gpt-5.6-terra")
API_VERSION = os.environ.get("GPT_AZURE_API_VERSION", "2025-04-01-preview")
MAX_OUTPUT_TOKENS = int(os.environ.get("GPT_MAX_OUTPUT_TOKENS", "12000"))
CRED_URL = os.environ.get("GPT_AZURE_CRED_URL",
                          "https://foundry-aws-pluto.adobe.io/iam/credentials/azure")

CREDS_TXT = Path(os.environ.get("GPT_CREDS_TXT", str(Path.home() / "hs_scripts/claude/thd/creds.txt")))
CREDS_YAML = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
AZURE_ENV = Path.home() / ".claude" / "hshariati" / "azure_openai.env"

_LOCK = threading.Lock()
_CACHE: dict = {"client": None, "expires": 0.0, "endpoint": ""}


class LLMUnavailable(RuntimeError):
    """Raised instead of silently falling back to a different model/provider."""


# ---- credential resolution -------------------------------------------------------------------
def _read(path: Path) -> str:
    try:
        return path.read_text()
    except Exception:
        return ""


def _pluto_token() -> str | None:
    if os.environ.get("PLUTO_TOKEN"):
        return os.environ["PLUTO_TOKEN"].strip()
    if CREDS_YAML.exists():
        try:
            import yaml
            tok = (yaml.safe_load(_read(CREDS_YAML)) or {}).get("foundry_aws", {}).get("pluto_token")
            if tok:
                return str(tok).strip()
        except Exception:
            pass
    m = re.search(r'pluto[_-]?token\s*[:=]\s*"?([A-Za-z0-9._\-]+)"?', _read(CREDS_TXT), re.I)
    return m.group(1).strip() if m else None


def _pasted_bearer() -> tuple[str, str] | None:
    """(endpoint, token) from env / creds.txt / azure_openai.env, or None."""
    ep = os.environ.get("AZURE_OPENAI_ENDPOINT")
    tok = os.environ.get("AZURE_OPENAI_AD_TOKEN")
    if ep and tok:
        return ep, tok
    for src in (CREDS_TXT, AZURE_ENV):
        txt = _read(src)
        e = re.search(r'AZURE_OPENAI_ENDPOINT\s*=\s*"?([^"\n]+)"?', txt, re.I)
        t = re.search(r'AZURE_OPENAI_AD_TOKEN\s*=\s*"?([^"\n]+)"?', txt, re.I)
        if e and t:
            return e.group(1).strip(), t.group(1).strip()
    return None


def _mint_from_pluto(tok: str) -> tuple[str, str]:
    import requests
    r = requests.get(CRED_URL, headers={"x-pluto-token": tok}, timeout=30)
    r.raise_for_status()
    c = r.json()
    if not (c.get("token") and c.get("endpoint")):
        raise LLMUnavailable("azure credential response carried no token/endpoint")
    return c["endpoint"], c["token"]


def _client(force: bool = False):
    with _LOCK:
        if not force and _CACHE["client"] and time.time() < _CACHE["expires"]:
            return _CACHE["client"]
        try:
            from openai import AzureOpenAI
        except ImportError as e:
            raise LLMUnavailable(f"missing dependency: {e}") from e
        endpoint = token = None
        minted = False
        tok = _pluto_token()
        if tok:
            try:
                endpoint, token = _mint_from_pluto(tok)
                minted = True
            except Exception:
                endpoint = token = None
        if not token:
            pasted = _pasted_bearer()
            if not pasted:
                raise LLMUnavailable(
                    "no GPT credential. Provide a Pluto token (credentials.yaml/creds.txt) to "
                    "auto-mint, or paste AZURE_OPENAI_ENDPOINT + AZURE_OPENAI_AD_TOKEN into creds.txt.")
            endpoint, token = pasted
        client = AzureOpenAI(azure_ad_token=token, api_version=API_VERSION, azure_endpoint=endpoint)
        # auto-mint bearers last ~60min; a pasted one may already be part-spent -> cache 45min
        _CACHE.update(client=client, expires=time.time() + (50 if minted else 45) * 60,
                      endpoint=endpoint, minted=minted)
        return client


# ---- calls -----------------------------------------------------------------------------------
def ask(prompt: str, system: str = None, model: str = None,
        max_output_tokens: int = None, retries: int = 3) -> str:
    model = model or MODEL
    msgs = ([{"role": "system", "content": system}] if system else []) + \
           [{"role": "user", "content": prompt}]
    last = None
    for attempt in range(retries):
        try:
            client = _client(force=(attempt > 0 and _is_auth(last)))
            r = client.chat.completions.create(
                model=model, messages=msgs,
                max_completion_tokens=int(max_output_tokens or MAX_OUTPUT_TOKENS))
            out = (r.choices[0].message.content or "").strip()
            if out:
                return out
            last = RuntimeError("empty completion")
        except LLMUnavailable:
            raise
        except Exception as e:                                     # noqa: BLE001
            last = e
        if attempt < retries - 1:
            time.sleep(1.5 * (attempt + 1))
    raise LLMUnavailable(f"{model} failed after {retries} attempts: {type(last).__name__}: {last}")


def _is_auth(e) -> bool:
    s = str(e or "").lower()
    return "401" in s or "expired" in s or "unauthor" in s


_FENCE = re.compile(r"```(?:json)?\s*(.+?)```", re.S)


def ask_json(prompt: str, **kw) -> dict:
    raw = ask(prompt, **kw)
    for cand in _candidates(raw):
        try:
            d = json.loads(cand)
            if isinstance(d, dict):
                return d
        except Exception:
            continue
    raise LLMUnavailable(f"no JSON in a {len(raw)}-char reply: {raw[:220]!r}")


def _candidates(raw: str):
    raw = (raw or "").strip()
    yield raw
    m = _FENCE.search(raw)
    if m:
        yield m.group(1).strip()
    start = raw.find("{")
    if start >= 0:
        depth = 0
        for i, ch in enumerate(raw[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    yield raw[start:i + 1]
                    break


def status() -> dict:
    try:
        _client()
        return dict(ok=True, model=MODEL, endpoint=_CACHE.get("endpoint", ""),
                    minted=_CACHE.get("minted", False), api_version=API_VERSION)
    except LLMUnavailable as e:
        return dict(ok=False, model=MODEL, why=str(e))


def _main() -> int:
    import argparse
    import sys
    p = argparse.ArgumentParser(description="Call Foundry GPT-5.x (default gpt-5.6-terra).")
    p.add_argument("prompt", nargs="?")
    p.add_argument("-m", "--model", default=MODEL)
    p.add_argument("-s", "--system")
    p.add_argument("--json", action="store_true", help="parse+print JSON only")
    p.add_argument("--status", action="store_true")
    p.add_argument("--max-tokens", type=int, default=MAX_OUTPUT_TOKENS)
    a = p.parse_args()
    if a.status:
        print(json.dumps(status(), indent=1)); return 0
    prompt = a.prompt or (sys.stdin.read().strip() if not sys.stdin.isatty() else None)
    if not prompt:
        print("ERROR: no prompt", file=sys.stderr); return 2
    if a.json:
        print(json.dumps(ask_json(prompt, system=a.system, model=a.model,
                                  max_output_tokens=a.max_tokens), indent=1))
    else:
        print(ask(prompt, system=a.system, model=a.model, max_output_tokens=a.max_tokens))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
