# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli"]
# ///
"""Verify the exact GPT-5.5 deployment without sending customer source messaging."""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import tomli
from openai import AzureOpenAI

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path.home() / '.claude/scripts'))
import gpt_call


def client_and_auth_mode():
    try:
        return gpt_call._client().with_options(max_retries=0, timeout=120), 'shared_gpt_helper'
    except gpt_call.LLMUnavailable:
        # The shared helper supports minted/pasted bearers, not the API key used by
        # this Codex provider. Reuse the configured Azure service; never copy a key.
        config = tomli.loads((Path.home() / '.codex/config.toml').read_text())
        provider = config['model_providers'][config['model_provider']]
        endpoint = urlsplit(provider['base_url'])
        key = os.environ.get(provider.get('env_key', ''))
        if endpoint.scheme != 'https' or not endpoint.hostname.endswith('.openai.azure.com') or not key:
            raise RuntimeError('No supported configured Azure API credential is available')
        version = provider.get('query_params', {}).get('api-version', gpt_call.API_VERSION)
        return AzureOpenAI(azure_endpoint=endpoint.scheme + '://' + endpoint.netloc,
                           api_key=key, api_version=version, max_retries=0, timeout=120), 'configured_azure_api_key'


def main():
    target = ROOT / 'research/source_messaging_v1_to_v6/data/gpt55_access_probe.json'
    record = {'started_at': datetime.now(timezone.utc).isoformat(), 'requested_model': 'gpt-5.5',
              'contains_customer_source': False}
    started = time.monotonic()
    try:
        client, mode = client_and_auth_mode()
        record['auth_mode'] = mode
        response = client.chat.completions.create(
            model='gpt-5.5', max_completion_tokens=1000,
            messages=[{'role': 'user', 'content': 'Return exactly this JSON object: {"connection_test":"ok"}'}])
        record.update(ok=True, response=response.model_dump(mode='json'))
    except Exception as exc:
        record.update(ok=False, error_type=type(exc).__name__, status_code=getattr(exc, 'status_code', None))
        # Keep error descriptions bounded and redact any configured credential.
        message = str(exc)
        for key in ('AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_AD_TOKEN', 'PLUTO_TOKEN'):
            secret = os.environ.get(key)
            if secret:
                message = message.replace(secret, '[REDACTED]')
        record['error'] = message[:2000]
    record['elapsed_seconds'] = round(time.monotonic() - started, 2)
    target.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))
    return 0 if record['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
