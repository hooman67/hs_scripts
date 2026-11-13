---
name: reference_gpt_call_skill
description: "/gpt_call skill — call Foundry GPT-5.x (Azure OpenAI), default gpt-5.6-terra; how access works"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d24f6783-62e3-43e4-9386-81e8e1cd0c68
  modified: 2026-08-29T08:30:52.121Z
---

`/gpt_call` skill (`dotclaude/commands/gpt_call.md` + `dotclaude/scripts/gpt_call.py`, symlinked to
~/.claude) is the canonical way to reach **Foundry GPT-5.x**. Default **gpt-5.6-terra**; alt
**gpt-5.6-luna** (scored higher on the vault's *structured-rewrite* benchmark, 100% vs 97% — good for
JSON field-filling). Import form: `from gpt_call import ask, ask_json`.

**Access (from videogen/core/llm.py):** mint a short-lived Azure AD bearer, then
`AzureOpenAI(azure_ad_token=..., api_version="2025-04-01-preview", azure_endpoint=...)`. Non-negotiable
deployment facts: use `max_completion_tokens` (never `max_tokens`); **omit `temperature`** (5.6 rejects
non-default); bearer expires ~60 min. Two credential paths, in order: (1) **auto-mint** from a Pluto
token (`$PLUTO_TOKEN` → credentials.yaml `foundry_aws.pluto_token` → creds.txt) via
`GET https://foundry-aws-pluto.adobe.io/iam/credentials/azure` header `x-pluto-token` — preferred,
self-refreshing; (2) **pasted bearer** `AZURE_OPENAI_ENDPOINT`+`AZURE_OPENAI_AD_TOKEN` in creds.txt
(short-lived ~1h, re-paste on 401). This box has NO pluto token, so it currently uses pasted bearers in
`hs_scripts/claude/thd/creds.txt` (Hooman refreshes them; AWS S3 creds live in the same file and expire
together). Related: [[reference_github_thd_proj]], [[project_thd_rewriter]], [[feedback_make_blockers_obvious]].
