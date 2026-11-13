# Mechanical pre-inference failure

All 15 records failed before inference because the detached tmux environment did not expose the configured Azure API credential expected by the inherited helper. No GPT-5.5 request was sent.

The frozen result envelopes are preserved unchanged. They say `invalid_model_output` because an early V4 error-classification bug classified a client-construction exception before creating a transport-attempt record. The embedded error message and absence of response files establish that this was a credential/transport setup failure, not invalid model output.

The replacement protocol uses Foundry Direct OpenAI through `foundry_aws_gateway.llm.get_openai()` and a new run name. These results are never reused or counted as model judgments.
