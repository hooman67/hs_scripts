Call an Azure OpenAI chat deployment (GPT-5 / GPT-5.5 / GPT-5-mini) with an Azure AD bearer token.

Usage: /azure-openai [prompt]

Use this whenever you need to run a one-off completion against the Adobe Azure OpenAI endpoint — quick classification, extraction, summarization, or testing a prompt against a specific model.

## How it works

The script (`~/.claude/scripts/azure_openai.py`, PEP 723 / `uv run --script`, dep `openai>=1.50`) calls `AzureOpenAI(azure_endpoint, azure_ad_token, api_version="2024-12-01-preview").chat.completions.create(...)`.

Credentials (endpoint + short-lived AD token) are resolved in order:
1. `--creds <file>` — a sourceable file with `export AZURE_OPENAI_*` lines
2. `AZURE_OPENAI_ENDPOINT` / `AZURE_OPENAI_AD_TOKEN` already exported in the env
3. `~/.claude/hshariati/azure_openai.env`
4. `~/Desktop/temp_cred.txt` (where ad-hoc creds get dropped)

## Examples

```bash
uv run --script ~/.claude/scripts/azure_openai.py "Summarize in one line: ..."
uv run --script ~/.claude/scripts/azure_openai.py -d gpt-5.5 -s "You are terse." "ping"
echo "long text" | uv run --script ~/.claude/scripts/azure_openai.py -d gpt-5-mini-deployment-0e739
uv run --script ~/.claude/scripts/azure_openai.py --list           # deployments named in creds file
uv run --script ~/.claude/scripts/azure_openai.py --json "..."     # print only the model reply
```

Flags: `-d/--deployment` (default `gpt-5-mini-deployment-0e739`), `-s/--system`, `-m/--max-tokens` (default 2000), `--creds`, `--list`, `--json`.

## Notes

- **No `gpt-4o` text model** on this endpoint. Text/chat deployments are `gpt-5`, `gpt-5.5`, and `gpt-5-mini-deployment-0e739`. (`gpt-image-1*` are image, `gpt-4o-transcribe-diarize`/`gpt-audio` are audio.)
- **GPT-5 family are reasoning models**: they bill reasoning tokens against `max_completion_tokens`, and they do **not** accept `temperature` or `max_tokens`. If `content` comes back empty with `finish_reason=length`, raise `-m`.
- The **AD token is short-lived (~1h)**. On 401/expired, refresh the creds file (drop a new `temp_cred.txt`) and re-run — there's no machine-token broker for this endpoint like there is for AWS.
- For a *selection / classification* task, `gpt-5-mini` is typically as good as the big models and far cheaper — default to it.
