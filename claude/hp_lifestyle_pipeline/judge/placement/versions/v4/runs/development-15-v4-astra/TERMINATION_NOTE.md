# Parent-directed early stop after explicit-case failure

This frozen Direct OpenAI `gpt-6-astra` development run was stopped after the first two completed cases because it failed an explicit early-gate case. It must not be resumed or treated as a completed 15-case evaluation.

- `elitebook__laptop_FrontLeftMedium__p1`: predicted `review` (score 100, reason `low_coverage`); explicit human verdict `review`. The verdict matched, but the assessment did not detect or encode the expected small `chair_displacement` warning.
- `tassel__printer_FrontWide__p1`: predicted `review` (score 100, reason `low_coverage`); explicit human verdict `fail`. The model explicitly accepted the freestanding rectangular table, did not detect the malformed/nonparallel side edges, and produced no `malformed_support_furniture` or `misplaced_support_furniture` finding.
- `cashmere__laptop_FrontLeftMedium__p1`: was in flight and has no result.

Both completed responses were valid structured outputs from returned model `gpt-6-astra`. No result was retried or manually edited. The tmux session was terminated after this evidence in accordance with the early-stop rule. The progress ledger remains in its exact interrupted state.
