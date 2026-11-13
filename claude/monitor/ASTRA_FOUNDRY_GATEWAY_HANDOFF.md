# Handoff: call GPT-6 Astra from a Sol Codex session

As of: 2026-11-05

## Goal

Keep the interactive Codex session on an available model such as GPT-6 Sol, and
use that session to submit selected **product LLM integration or evaluation**
prompts to GPT-6 Astra through Foundry's direct OpenAI credentials.

This does not move the Codex session onto Astra. Astra receives only the prompt
explicitly sent in the API call. It cannot see the Codex transcript, filesystem,
tools, or prior context unless the Sol agent includes that information.

## Usage boundary

The Colligo gateway policy restricts these credentials to product LLM
integration, data-processing jobs, and experiments. Do not use them to run
Codex itself, perform general coding work, or route ordinary productivity tasks
through Astra.

The client sends the acknowledgement required by FFDY-8502. Use
`foundry-aws-gateway>=2.0.0`; older versions are rejected.

Canonical policy and client documentation:

```text
/home/colligo/colligo/managed_services/services/firefly/foundry/libs/aws_gateway_client/README.md
```

## Choose the correct route

Use:

```python
foundry_aws_gateway.llm.get_openai()
```

This is Direct OpenAI and uses a quota path separate from the shared Azure
`eastus2` resource that rate-limited the original Codex session.

Do not use this route when the purpose is to avoid that Azure quota:

```python
foundry_aws_gateway.llm.get_azure_openai()
```

The Azure function vends a token for the shared `eastus2` Azure OpenAI
resource. It is another credential path to the resource associated with the
original failure, not a new quota pool.

## Authentication and security

On this Pluto devbox, `PLUTO_AUTH_TOKEN` is already injected. Never print it,
copy it into a prompt, or extract the upstream OpenAI API key.

The gateway client caches credentials under:

```text
${XDG_CACHE_HOME}/ai_platform/foundry_aws_gateway
```

Run `umask 077` before the client so newly created cache files are private. Do
not read or display `openai.json` or `azure.json`. The cache created during the
2026-11-05 validation was already corrected to directory mode `0700` and file
mode `0600`.

## Submit one Astra request

1. Write a self-contained prompt to a durable file under `/home/colligo` using
   `apply_patch`. Include all task context Astra needs. Do not include secrets.
2. Set `prompt_path` below to that absolute file path.
3. Run the command from this Pluto devbox.

```bash
umask 077
prompt_path=/home/colligo/ABSOLUTE/PATH/TO/prompt.md
uv run \
  --python 3.12 \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  python - "$prompt_path" <<'PY'
from pathlib import Path
import sys

import foundry_aws_gateway.llm

prompt = Path(sys.argv[1]).read_text(encoding="utf-8")
client = foundry_aws_gateway.llm.get_openai().with_options(
    max_retries=8,
    timeout=600.0,
)
response = client.chat.completions.create(
    model="gpt-6-astra",
    messages=[{"role": "user", "content": prompt}],
    reasoning_effort="high",
    max_completion_tokens=8192,
)

choice = response.choices[0]
print(choice.message.content or "")
print(
    f"\n[model={response.model} finish={choice.finish_reason} "
    f"total_tokens={getattr(response.usage, 'total_tokens', None)}]",
    file=sys.stderr,
)
PY
```

The command passes the prompt path as an argument. Do not interpolate the
prompt contents into shell code.

## How the Sol session should use Astra

The Sol agent remains responsible for orchestration:

1. Inspect the live repository and relevant evidence itself.
2. Prepare a bounded, self-contained Astra prompt in a durable file.
3. Make one Astra call with concurrency `1`.
4. Review Astra's answer against the source material; do not treat it as
   automatically correct.
5. Persist useful output with `apply_patch`, including the full input prompt,
   model name, date, and material limitations.
6. Continue implementation and tool use in the Sol Codex session.

For a follow-up, either send a new self-contained prompt or include the prior
turns explicitly in the `messages` list. The API is stateless unless the caller
preserves conversation history.

## Rate-limit behavior

Direct OpenAI is a separate quota path, but it can still return 429s. Current
Colligo Astra evaluation code uses patient retries for this reason. The example
uses the OpenAI client's exponential retry behavior with `max_retries=8` and
keeps concurrency at one.

If rate limits persist after those retries:

- record the error type, HTTP status, model, and time without recording
  credentials;
- wait before retrying the same bounded request;
- do not silently fall back to the Azure route when the objective is to avoid
  the shared `eastus2` quota; and
- keep the Sol session working on tasks that do not depend on the Astra answer.

## Verified on this machine

On 2026-11-05, `foundry-aws-gateway` 2.0.0 used the existing Pluto token and
successfully called Direct OpenAI `gpt-6-astra` with high reasoning effort. A
minimal request returned `ASTRA_OK` in 2.1 seconds.

Detailed evidence and comparison:

```text
/home/colligo/hs_scripts/claude/monitor/research/llm-gateway-astra/SUMMARY.md
```
