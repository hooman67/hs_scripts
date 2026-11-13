# Provenance

- Purpose: one compact GPT-6 Astra product-integration design consultation for allowing rigid x-y product translation in every camera view.
- Date submitted: 2026-11-05 America/Los_Angeles.
- Route: `foundry_aws_gateway.llm.get_openai()` (Direct OpenAI).
- Model requested: `gpt-6-astra`.
- Reasoning effort: `high`.
- Completion-token limit: 8192.
- Client retry bound: 8.
- Per-request timeout: 600 seconds.
- Concurrency: one.
- Input: `request.md`; no images and no credentials.
- Source checkout reviewed: `/home/colligo/foundry-pr4349-position-exp` at base commit `8c358bc7989cb0e137e89db0fd325168249e2a22`, with uncommitted experiment changes.
- Limitation: Astra receives only the text in `request.md`; it cannot inspect the checkout or generation evidence.
