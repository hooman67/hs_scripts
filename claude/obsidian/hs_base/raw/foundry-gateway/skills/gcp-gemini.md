Call a Google Gemini model on Vertex AI (Foundry GCP project GCP-0805) with a short-lived GCP access token.

Usage: /gcp-gemini [prompt]

The GCP/Gemini twin of `/azure-openai`. Use it for one-off completions against Gemini — quick classification, extraction, summarization, or testing a prompt against a specific Gemini model.

## How it works

The script (`~/.claude/scripts/gcp_gemini.py`, PEP 723 / `uv run --script`, dep `requests>=2.31`) POSTs to the Vertex AI REST endpoint:
`https://{region}-aiplatform.googleapis.com/v1/projects/{project}/locations/{region}/publishers/google/models/{model}:generateContent`
with `Authorization: Bearer $GCP_ACCESS_TOKEN`. The `global` location uses the apex host `aiplatform.googleapis.com`. No SDK or ADC needed.

Credentials (project + region + short-lived OAuth token) are resolved in order:
1. `--creds <file>` — a sourceable file with `export GCP_ACCESS_TOKEN` / `export CLOUDSDK_CORE_PROJECT` / `export CLOUDSDK_COMPUTE_REGION` lines
2. `GCP_ACCESS_TOKEN` + `CLOUDSDK_CORE_PROJECT` (+ `CLOUDSDK_COMPUTE_REGION`) already exported in the env
3. `~/.claude/hshariati/gcp_gemini.env`
4. `~/Downloads/creds.txt` (where ad-hoc creds get dropped)

## Examples

```bash
uv run --script ~/.claude/scripts/gcp_gemini.py "Summarize in one line: ..."
uv run --script ~/.claude/scripts/gcp_gemini.py -m gemini-2.5-pro -s "You are terse." "ping"
echo "long text" | uv run --script ~/.claude/scripts/gcp_gemini.py -m gemini-2.5-flash-lite
uv run --script ~/.claude/scripts/gcp_gemini.py --list          # probe reachable models
uv run --script ~/.claude/scripts/gcp_gemini.py --json "..."    # print only the model reply

# Video (Veo, async text-to-video with native audio) — saves a local mp4:
uv run --script ~/.claude/scripts/gcp_gemini.py --veo -o out.mp4 "a corgi on a beach at sunset"
uv run --script ~/.claude/scripts/gcp_gemini.py --veo -m veo-3.0-fast-generate-001 --duration 4 --aspect 9:16 "..."
```

Chat flags: `-m/--model` (default `gemini-2.5-flash`), `-s/--system`, `-r/--region` (default creds region or `us-central1`; `global` allowed), `-t/--max-tokens` (default 2048), `--temperature`, `--creds`, `--list`, `--json`.

Veo flags (`--veo` mode): `-m/--model` (default `veo-3.0-generate-001`), `-o/--out` (default `veo_out.mp4`), `--duration` (sec, default 8), `--aspect` (default `16:9`), `--no-audio`, `--poll-timeout` (sec, default 420). Veo is async: the script submits via `:predictLongRunning`, polls `:fetchPredictOperation`, then decodes the inline base64 video to the output path.

## Notes

- **Available models** (project GCP-0805, probed live — use `--list` to re-check): chat → `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` in `us-central1` (+ `gemini-flash-latest` / `gemini-flash-lite-latest` in `global`). Video → `veo-3.0-generate-001` (Veo 3, video+audio), `veo-3.0-fast-generate-001`, `veo-2.0-generate-001` (no audio), all in `us-central1` & `global`. The Gemini 1.5/2.0 families, Gemini 3, and Veo `*-preview`/`veo-3.1` are **not** enabled.
- **2.5 models are thinking models**: they spend reasoning ("thoughts") tokens against `maxOutputTokens`. A small `-t` returns empty `content` with `finish_reason=MAX_TOKENS` — raise `-t` (default is 2048).
- The **access token is short-lived (~1h)**. On `401 UNAUTHENTICATED` / expired, refresh the creds file (e.g. `gcloud auth print-access-token` into `~/Downloads/creds.txt`) and re-run — there's no machine-token broker like the AWS `/aws-creds` path.
- **Internal use only**: per the Foundry access doc (§2.6), Foundry Gemini creds are for data-processing jobs and experiments — not production services, and not available in Ethos.
- The official auto-token path is the `foundry_aws_gateway.llm.get_google_genai()` client (`pip install foundry-aws-gateway[llm]`); this skill is the lightweight bearer-token alternative for ad-hoc creds.
