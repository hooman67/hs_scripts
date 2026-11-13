# Frozen V4.2 gate attempt 2 terminated

Direct OpenAI rejected the v2 wire schema before visual inference because `general_artifact_warnings[].code` used `const` without an explicit `type`. Completed rows are transport-error envelopes; the in-flight row was marked aborted without inventing a result. Remaining rows were not started.
