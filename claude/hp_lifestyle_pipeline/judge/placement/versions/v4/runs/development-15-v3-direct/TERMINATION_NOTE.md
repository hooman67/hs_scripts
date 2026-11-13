# Parent-terminated model-quality run

This frozen GPT-5.5 Direct OpenAI development run was stopped by the root agent on 2026-11-05 after three completed cases and one in-flight case. It must not be resumed or treated as a completed evaluation.

The stop was based on model quality, not transport:

- `elitebook__laptop_FrontLeftMedium__p1`: predicted `pass`; explicit human expectation `review` for a small chair-displacement warning.
- `tassel__printer_FrontWide__p1`: predicted `pass`; explicit human expectation `fail` for malformed, nonparallel table geometry and implausible rectangular-table room placement.
- `cashmere__laptop_FrontLeftMedium__p1`: predicted `pass`; explicit human expectation `review` for a small chair-displacement warning.
- `tassel__printer_FrontCloseUp__p1`: was in flight and has no result.

All three completed records had valid structured output and returned model `gpt-5.5-2026-04-23`; no output was manually edited. The progress ledger remains in its exact interrupted state as transport evidence.
