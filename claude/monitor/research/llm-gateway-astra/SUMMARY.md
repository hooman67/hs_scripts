# Astra access through the Foundry Cloud Gateway

As of: 2026-11-05 (America/Los_Angeles)

## Question

Is the LLM gateway described in Colligo the same path documented in Foundry's
`project-setup-and-access.md`, and can it provide a usable alternative route to
GPT-6 Astra from Hooman's Pluto devbox?

## Conclusion

- **VERIFIED:** Foundry documentation section 2.4 and the Colligo
  `foundry-aws-gateway` README describe the same Azure credential-vending
  client: `foundry_aws_gateway.llm.get_azure_openai()`.
- **VERIFIED:** The library is a credential broker, not an inference proxy. Its
  Azure path vends a short-lived Azure AD token and calls the shared Azure
  OpenAI resource in `eastus2` directly.
- **VERIFIED:** The same library has a distinct direct OpenAI Platform path,
  `foundry_aws_gateway.llm.get_openai()`. It uses a Foundry OpenAI project and
  therefore has a quota pool separate from the Azure resource.
- **VERIFIED BY LIVE TEST:** On this Pluto devbox, version 2.0.0 authenticated
  from the existing `PLUTO_AUTH_TOKEN`. Both direct OpenAI and Azure accepted
  `gpt-6-astra` with high reasoning effort and returned `ASTRA_OK`.
- **ASSUMED (high confidence):** The Azure client is unlikely to avoid the
  Codex session's reported `eastus2` Astra token limit. Both identify the same
  region and shared model deployment class, but the local Codex catalog does
  not disclose the Azure resource hostname, so exact resource identity was not
  independently proven.
- **VERIFIED:** The direct OpenAI route is a separate backend/quota path and is
  the useful alternative for authorized product experiments. Current Colligo
  WDI code also uses Direct OpenAI with `gpt-6-astra` and retries transient
  429s, so this route can still rate-limit.

## Live validation

| Route | Result | Latency | Returned model | Tokens |
|---|---:|---:|---|---:|
| Direct OpenAI (`get_openai`) | Success | 2.1 s | `gpt-6-astra` | 33 |
| Azure eastus2 (`get_azure_openai`) | Success | 3.0 s | `gpt-6-astra-2026-09-03` | 22 |

Both calls used `reasoning_effort="high"`, no retries, and a minimal exact-text
prompt. No credential values were printed or stored in this report.

## Policy and operational constraints

- `foundry-aws-gateway>=2.0.0` is required. It sends the acknowledgement header
  required by FFDY-8502.
- The gateway README restricts these LLM credentials to product LLM integration,
  data-processing jobs, and experiments. It explicitly prohibits coding and
  productivity-tool use and removed the earlier Codex/Claude credential setup.
- This makes Direct OpenAI suitable for the placement-judge/evaluation work,
  but not as a credential source for running the Codex coding agent itself.
- The client created credential caches as mode `0644` under
  `/mnt/localssd/.cache/ai_platform/foundry_aws_gateway`. During this test the
  directory was tightened to `0700` and the token/key caches and lock files to
  `0600`. The package's default file-mode behavior remains a source issue.

## Can it replace an interactive Codex session?

- **VERIFIED:** The Foundry Cloud Gateway is not a Codex-compatible inference
  gateway. It vends upstream Azure/OpenAI credentials; the caller then sends
  model requests directly. It does not host or preserve an interactive Codex
  session.
- **VERIFIED:** Codex itself supports organization model gateways that expose a
  compatible Responses API. It also supports API-key and command-backed
  credential-helper authentication. Official documentation:
  https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway
- **VERIFIED:** `codex resume` accepts model overrides and restores the original
  transcript. In principle, Codex can resume a saved thread through a different
  configured provider when that provider is compatible.
- **VERIFIED:** This particular credential source cannot be used for that
  purpose under its current Adobe policy. The Colligo 2.0.0 README says the LLM
  credentials are not for coding or productivity tools, requires an explicit
  acknowledgement of that restriction, removes the prior `coder` CLI, and
  directs users to GitHub Copilot.
- **Conclusion:** The existing monitored Codex session must stay on its approved
  Codex provider. Direct OpenAI Astra from `foundry-aws-gateway` is usable for
  authorized product/evaluation model calls, but it cannot permissibly replace
  the Codex backend. A separately approved Codex-compatible Adobe gateway would
  make such a replacement possible.

## Primary sources

- Foundry access documentation, current `main` retrieved 2026-11-05:
  https://github.com/Adobe-Firefly/foundry/blob/main/docs/project-setup-and-access.md#24-azure-openai
- Local shallow checkout of that source:
  `/home/colligo/colligo/.worktrees/foundry/docs/project-setup-and-access.md`
- Colligo gateway client README, `origin/main` retrieved 2026-11-05:
  `/home/colligo/colligo/managed_services/services/firefly/foundry/libs/aws_gateway_client/README.md`
- Azure credential-service documentation:
  `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/aws_gateway/iam_azure/README.md`
- OpenAI credential-service documentation:
  `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/aws_gateway/iam_openai/README.md`
- Direct Astra production-style client example:
  `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/wdi_multiref_v2/prompt_rewrite/client.py`

The Colligo working branch was 964 commits behind `origin/main`, so conclusions
were drawn from freshly fetched `origin/main`, not from the stale working-tree
copies.
