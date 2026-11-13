# Natural-placement judge V4.4 design and claim boundary

V4.4 is a two-pass, defect-oriented GPT-5.5 judge. The first pass inventories visible geometry and proposes defects using fixed tests. The second pass independently verifies every positive proposal, including severity 1; it is also called with an empty proposal list. Application code validates both responses, derives public issue codes and scores, and never repairs a valid-but-wrong visual judgment.

## Contract

Runtime input is exactly generated scene image, original digital-twin image, product type, and scene prompt. Eval record IDs, camera tags, ranks, human comments, labels, and expectation files are not sent to the model. The result always includes a 0–100 score field, score-valid flag, pass/review/fail verdict, component checks, evidence, raw-call audit, and an explicit error/unassessable sentinel when scoring is invalid.

Severity is the Astra-designed 1–3 scale: 1 is modest ordinary repositioning and deterministically yields review after verification; 2 is a material defect and fails; 3 is severe/impossible and fails. Hidden relations are unobservable rather than wrong. An all-unknown assessment is unassessable, not pass.

## Deliberate adaptations from the Astra design response

- **Model route:** Astra was used to process feedback and design the judge. Production visual inference remains Direct OpenAI GPT-5.5 with high reasoning, as requested by Hooman and consistent with prior judge runtime.
- **Taxonomy:** the implementation retains the established 14 visual tests. Six ambiguous tests have explicit scout inventory subtype fields. The verifier independently observes the exact subtype for every confirmed ambiguous test. Application code maps that verified subtype to a public issue code; neither model emits a public code.
- **Scoring/dedupe:** model-emitted cause IDs are absent. Frozen application-owned penalty groups take the maximum penalty per group. In particular, furniture-room axes and shared perspective share `orientation_perspective`, preventing one geometry anomaly from being charged twice. Unrelated groups remain separately penalized.
- **Geometry aid:** the supplied implementation uses verified SIFT/affine localization with a deterministic crop and Canny/Hough edge overlay, rather than Astra's suggested homography. Full raw scene pixels remain authoritative; aid provenance explicitly warns that lines may be false or missing.
- **Output bounds:** local and wire schemas bound prose. Scout and verifier completion caps are 9,000 and 4,000 tokens. SDK retries are disabled. One shared objective/transport repair is allowed, with at most three total requests.
- **Placement scope:** props that visibly block operation or contradict the activity zone remain placement findings because Hooman explicitly included this in natural-use narrative. Unrelated malformed props remain separate rendering warnings.

## Evidence claim boundary

The six-case gate reuses labeled development examples and is not held-out validation. Gate A requires three independent repeats per case to measure consistency. The frozen ten-case set was selected from the previously annotated 84-row corpus before V4.4 calls; it is **historical held-out development evidence**, not prospective or statistically independent validation. Its labels are never available to runtime, but its selection was label-informed. Any safety-to-scale claim requires a later implementation-frozen, separately selected blind set or new generations.

No V4.4 model call may begin until the protocol freeze hashes the prompts, schemas, codebook, scoring, geometry, runner, input manifest, and preflight report. The runner revalidates those hashes before every call and resume.
