Call Adobe Foundry GPT-5.x (Azure OpenAI) from a single entry point. Default model: **gpt-5.6-terra**.

Usage: /gpt_call [prompt]

Use this whenever you need a GPT-5.x completion (classification, extraction, structured rewriting,
JSON field-filling). It is the canonical way to reach GPT in this environment — prefer it over ad-hoc
Azure calls.

## How it works

`~/.claude/scripts/gpt_call.py` (PEP 723 / `uv run --script`, deps `openai`, `requests`, `pyyaml`)
calls `AzureOpenAI(azure_endpoint, azure_ad_token, api_version="2025-04-01-preview").chat.completions
.create(model="gpt-5.6-terra", max_completion_tokens=..., messages=[...])`.

Credentials resolve in this order:
1. **Auto-mint from a Pluto token** (preferred — long-lived, self-refreshing): `$PLUTO_TOKEN` →
   `~/.claude/hshariati/credentials.yaml` (`foundry_aws.pluto_token`) → `creds.txt`. Mints a
   short-lived Azure AD bearer from `https://foundry-aws-pluto.adobe.io/iam/credentials/azure` with
   the `x-pluto-token` header, exactly as the production `videogen/core/llm.py` does.
2. **Pasted bearer**: `AZURE_OPENAI_ENDPOINT` + `AZURE_OPENAI_AD_TOKEN` from env,
   `~/hs_scripts/claude/thd/creds.txt`, or `~/.claude/hshariati/azure_openai.env`. Short-lived (~1h);
   re-paste on 401.

The bearer is cached with an expiry and re-minted (or re-read) on a 401, so long runs don't die.

## Commands

```
uv run --script ~/.claude/scripts/gpt_call.py --status                 # is a model reachable?
uv run --script ~/.claude/scripts/gpt_call.py "one-off prompt"
uv run --script ~/.claude/scripts/gpt_call.py -s "You are terse." "ping"
echo "long text" | uv run --script ~/.claude/scripts/gpt_call.py --json "return fields as JSON"
uv run --script ~/.claude/scripts/gpt_call.py -m gpt-5.6-luna "..."     # switch model
```

Import form (for pipelines like the THD rewriter):
```python
from gpt_call import ask, ask_json
fields = ask_json(user_msg, system=SYSTEM_PROMPT)   # dict, parsed defensively (handles fenced JSON)
```

## Model choice

- **gpt-5.6-terra** — default. Fast (31s vs 85s vs gpt-5.5 on the same refine turn), the project's
  standing choice, good feedback coverage.
- **gpt-5.6-luna** — scored higher on the vault's *structured-rewrite* benchmark (100% vs 97% fix
  coverage). Consider it for pure JSON field-filling. Switch with `-m gpt-5.6-luna` or `$GPT_MODEL`.

## Non-negotiable deployment facts (baked into the script)

- Uses `max_completion_tokens`, never `max_tokens` (5.x rejects the old name).
- **Omits `temperature`** — some 5.6 deployments reject any non-default value.
- `api_version = 2025-04-01-preview`.
- Never falls back to another model/provider silently — raises `LLMUnavailable` so a run's prompt
  quality is never secretly attributed to a model nobody chose.

## Notes

- To make GPT access permanent + self-refreshing, put the long-lived Pluto token where `/aws-creds`
  keeps it (`credentials.yaml` `foundry_aws.pluto_token`, exp 2026-11-27) — then auto-mint takes over
  and no bearer needs pasting.
- `--status` shows `minted: true` when it auto-minted from a Pluto token, `false` when it used a
  pasted bearer.
