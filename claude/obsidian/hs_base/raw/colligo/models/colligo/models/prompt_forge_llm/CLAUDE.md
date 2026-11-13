# prompt_forge_llm

LLM-based replacement for PromptForge V2.1, A/B-tested via the vision_sdk pipeline's `v1/safety/pre-check-async` endpoint.

## Architecture

- `worker/PromptForgeLLM.py` — `ColligoMLModel` that loads Qwen3.5-27B-FP8 in-process via `vllm.AsyncLLM` (v1 engine).
- `worker/prompt_processor.py` — Content moderation + diversity injection (LLM call 1).
- `worker/nsfw_classifier.py` — NSFW safety classification (LLM call 2). Two modes: `general` and `family`.
- `worker/templating.py` — Pure-Python helpers (system prompt, parsers, `[ETHNICITY]`/`[GENDER]` template fill) split out so they can be unit-tested in CPU envs without dragging vLLM into the import graph.
- `worker/safety_guidelines.py` — General Audience and Family/Education rule blocks consumed by the classifier.

Both LLM calls run concurrently via `asyncio.gather`. vLLM's `AsyncLLM` scheduler batches them across the engine — concurrent `generate()` calls are safe and benefit from cross-request batching.

## Deployment

- Custom pyenv: `vllm_0_18_0` (declared in `worker/colligo.yaml`).
- GPU: 40 GB.
- Worker name: `PROMPT_FORGE_LLM_V1` (`worker/types.py`).
- Public surface lives on the Vision SDK pipeline at `v1/safety/pre-check-async` (`firefly/pipelines/vision_sdk/pipelines/SafetyPipeline.py`); the worker is reachable internally via `PromptForgeLLMExecutor`.
