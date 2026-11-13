# Astra V4.5 design-call audit

No usable Astra design response was obtained. The four attempts were bounded and
their exact inputs, logs, and terminal states are preserved below. Attempts 1–3
were vision requests. Attempt 4 was an explicitly authorized text-only audit and
must not be represented as visual evaluation.

## Attempt 1

- Payload: 24 original PNGs plus compact frozen evidence.
- Outcome: HTTP 400 before model execution because the image payload was 90.37 MB, over the 50 MB limit.
- Audit: `attempt_1_oversize/`

## Attempt 2

- Payload: the same 24 visual roles using compression-only transport JPEGs totaling 7,975,487 bytes.
- Outcome: request accepted, then manually terminated at the authorized 12-minute wall-time cap with no response or error.
- Audit: `attempt_2_compressed_24_images_timeout/`

## Attempt 3

- Payload: six raw generated scenes plus the compact exact textual evidence; 2,613,408 image bytes.
- Model: `gpt-6-astra`, high reasoning, 16,000 output-token cap, zero SDK retries.
- Outcome: manually terminated at the authorized 12-minute wall-time cap with no response or error.
- Audit: `attempt_3_six_raw_scenes/`

## Attempt 4

- Payload: text only; no images. It included the distilled six-case annotations,
  exact expected issue descriptions and comments, V4.4 repeat evidence, the V4.5
  focused-probe diagnostic, both root-owned observer prompts, and the current
  deterministic codebook/scoring architecture.
- Model request: `gpt-6-astra`, high reasoning, 12,000 output-token cap, SDK
  `max_retries=2`, 600-second request timeout, and a 900-second hard wall timeout.
- Outcome: the request produced no response, refusal, gateway error, or returned
  model metadata before the exact 15-minute wall timeout. GNU `timeout` ended the
  process with exit code 124.
- Usability: no Astra output was received. This attempt therefore supports no
  Astra recommendation and no vision-evaluation claim.
- Audit: `attempt_4_text_only_review/`

The task text, exact comments, full and compact V4.4 evidence, source image
hashes, compressed transport hashes, request manifests, logs, and timestamps are
preserved in this directory. `SYNTHESIS.md` is a local evidence-based design
recommendation, not an Astra response.
