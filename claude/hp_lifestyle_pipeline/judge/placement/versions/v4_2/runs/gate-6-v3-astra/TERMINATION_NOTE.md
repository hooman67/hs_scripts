# Frozen V4.2 gate attempt 3 terminated

Case 1 passed API schema validation but both bounded attempts returned empty content and failed JSON decoding. Case 2 was in flight when the parent stopped the run to avoid spending the same latency on five further targets; it is marked aborted with no invented result. Remaining rows stayed pending. The runner did not persist finish reason or usage, so those are unknown. This motivates a distinct compact V4.3 and an instrumented one-case canary.
