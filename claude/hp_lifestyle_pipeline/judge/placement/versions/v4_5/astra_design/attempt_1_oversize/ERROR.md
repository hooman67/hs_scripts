# Astra V4.5 design submission attempt 1

- Status: failed before model execution
- Exit code: 1
- Failure class: request validation (`openai.BadRequestError`, HTTP 400)
- Error: `Total image size is 90.37MB, which exceeds the allowed limit of 50MB.`
- Model requested: `gpt-6-astra`
- Reasoning effort: `high`
- Images: 24 original PNGs (six cases × raw scene, twin, support crop, geometry overlay)
- Task text: the compact 199,509-byte task with exact comments, 18 repeat summaries, and exact V4.4 prompts/codebook/scoring
- Model response: none

The retry keeps the same task and 24 visual roles but uses resize/compression-only JPEG transport copies totaling 7,975,487 bytes. Source paths and SHA-256 values remain in the retry manifest. No evidence or label was changed.
