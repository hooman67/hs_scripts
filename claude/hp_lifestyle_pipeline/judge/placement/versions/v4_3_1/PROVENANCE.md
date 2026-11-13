# V4.3.1 provenance

The compact V4.3.1 architecture is a deployment-oriented revision of the Astra V4.2 redesign preserved at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_2/astra_redesign/astra_output.md`

V4.2 required the model to repeat inventory/candidate evidence inside thirteen check objects. A frozen high-reasoning Astra canary exhausted two 24k attempts with empty response content. V4.3 keeps the visual inventory, fourteen positive-condition triggers, candidate reconciliation, printer/home rule, laptop/chair rule, missing-support safeguards, independent prior-V6 anchors, and deterministic scoring. It removes model-authored legacy checks; application code derives those checks from compact candidates.

Production model default is GPT-5.5 through `foundry_aws_gateway.llm.get_openai()`. Astra was used to process feedback and propose the architecture; it is not the deployed judge default.

The frozen V4.3 GPT-5.5 canary established transport and structured-output validity, but its judgment failed the known chair-displacement case. The model observed that the only plausible visible chair was laterally offset from the laptop, then invented a possibly centered off-frame chair and returned pass. V4.3.1 changes only this calibration rule while preserving the compact model output, deterministic derivation, anchor selection, crop behavior, GPT-5.5 route, and bounded objective retry. The rule requires judging the only plausible visible associated chair even when partly cropped; it forbids an invented second chair from rescuing the layout; and it maps noticeable ordinary repositioning to severity-1 `chair_displacement` with a review warning.

The same target is rerun in a new quality-and-transport canary directory. The six-case gate remains blocked until this canary returns a valid result and the expected chair-displacement review.
