# V4.3 provenance

The compact V4.3 architecture is a deployment-oriented revision of the Astra V4.2 redesign preserved at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_2/astra_redesign/astra_output.md`

V4.2 required the model to repeat inventory/candidate evidence inside thirteen check objects. A frozen high-reasoning Astra canary exhausted two 24k attempts with empty response content. V4.3 keeps the visual inventory, fourteen positive-condition triggers, candidate reconciliation, printer/home rule, laptop/chair rule, missing-support safeguards, independent prior-V6 anchors, and deterministic scoring. It removes model-authored legacy checks; application code derives those checks from compact candidates.

Production model default is GPT-5.5 through `foundry_aws_gateway.llm.get_openai()`. Astra was used to process feedback and propose the architecture; it is not the deployed judge default. One GPT-5.5 canary must produce a valid structured assessment before the six-case gate runs.
