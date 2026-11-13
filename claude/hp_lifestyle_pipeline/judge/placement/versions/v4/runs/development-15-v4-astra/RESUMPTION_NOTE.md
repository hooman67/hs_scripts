# Root-directed resumption after changed diagnostic instruction

The run was initially stopped after two completed records under the earlier early-stop instruction. The root agent then explicitly directed that this same frozen run finish for diagnostic coverage. It was resumed without changing the frozen prompt, schema, scoring, model, or completed results. The first two result files are immutable cached results; the interrupted third record had no result and will be evaluated from scratch by the resumed batch.
