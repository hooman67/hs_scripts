# Provenance

- Purpose: retry the compact GPT-6 Astra product-integration consultation after v1 exhausted its 8192-token completion budget with `finish=length` and no visible content.
- Date submitted: 2026-11-05 America/Los_Angeles.
- Route: `foundry_aws_gateway.llm.get_openai()` (Direct OpenAI).
- Model requested: `gpt-6-astra`.
- Reasoning effort: `high`.
- Completion-token limit: 32768.
- Client retry bound: 8.
- Per-request timeout: 600 seconds.
- Concurrency: one.
- Input: byte-identical copy of compact-v1 `request.md`; no images and no credentials.
- Request SHA-256: `b184df1c5144076d1b0473eea68a93bea876181c48c358e230cb922513c8d8a5`.
- Source checkout reviewed: `/home/colligo/foundry-pr4349-position-exp` at base commit `8c358bc7989cb0e137e89db0fd325168249e2a22`, with uncommitted experiment changes.
- Limitation: Astra receives only the text in `request.md`; it cannot inspect the checkout or generation evidence.

## Result

- Started: `2026-11-06T07:22:34Z`.
- Finished: `2026-11-06T07:27:48Z`.
- Process exit code: `0`.
- API result: `model=gpt-6-astra`, `finish=stop`, `total_tokens=9621`.
- Usable visible response: yes, 17,510 bytes in `response.md`.
- Response SHA-256: `a708bd260e40dab439f637220dbed031b4071fd40bbcb3e5020c0398bcdd847e`.
- Review status: advisory output only; its proposed engineering thresholds are explicitly unvalidated and must be reviewed/tested before implementation.
