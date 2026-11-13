# Task: design HP Natural Placement Judge V4.4

You are advising the implementation of an image judge for natural placement of HP laptops and printers in generated lifestyle scenes. You cannot access files or tools. All relevant evidence is below. Design a deployable two-pass visual protocol, not an essay. Be specific enough that another engineer can implement strict JSON schemas, prompts, deterministic scoring, retries, and tests.

## Runtime contract

The production judge receives:

1. generated scene image;
2. original digital-twin render;
3. product type (`laptop` or `printer`);
4. scene prompt.

Optional eval metadata must never be required. The judge scores only the scene-generation image. Hidden/cropped relations are unobservable, not wrong. Tight crops must be able to pass. The system returns a 0–100 score, pass/review/fail, component checks, evidence-grounded explanation, and audit data. Production model is GPT-5.5 through Direct OpenAI. One objective repair attempt is allowed only for transport/invalid structured output, never for a valid but wrong judgment.

## Human natural-placement requirements

- Printers belong on dedicated equipment tables, credenzas, cabinets, or supports, not desks visibly occupied by someone.
- Product orientation must be usable relative to furniture and the intended scenario.
- Avoid laptops stranded in the center with no user position, products aimed toward corners, and printers awkwardly foregrounded.
- Product/support edges and related furniture edges should follow believable perspective and deliberate alignment. Relevant real-world parallel edge families should be geometrically coherent.
- Maintain plausible scale, perspective, support contact, load path, shadows, and reflections.
- A printer's functional front must remain approachable. Props must not block the operating path.
- A laptop should relate to the only plausible visible associated chair. Slight credible chair offset may pass or be advisory; noticeable ordinary repositioning is severity-1 review. Never invent a second off-frame centered chair to rescue an offset visible chair.
- A rectangular/square home printer support normally belongs at a wall or room edge. Central placement needs a visible shared-equipment/work narrative. A printer correctly placed on a malformed or misplaced table does not rescue the scene.
- Missing furniture legs/support and malformed support geometry are placement defects. Do not infer missing support merely because an underside is cropped.
- A diagonal product/support relation is not automatically intentional. Call it intentional only when visible functional evidence supports that use; otherwise test it as an axis conflict.
- Unrelated malformed props belong in an artifact warning, not a placement fail.

## V4.3.1 architecture and results

V4.3.1 asked one GPT-5.5 call for ten inventory facts, fourteen *positive-condition* triggers, and candidates. `yes` meant acceptable. Application code derived thirteen checks and the score. The prompt told the model to consider benign alternatives. A deterministic crop was included with the full scene. Independent calibration images were provided.

This produced fluent but confirmation-biased rationalization. On a frozen six-case development gate:

1. Laptop, visible chair noticeably offset. Human: review, `chair_displacement`. V4.3.1: review, `chair_displacement`. Correct only after an explicit calibration fix.
2. Home printer on a malformed rectangular table stranded centrally. Human: fail, `misplaced_support_furniture` + `malformed_support_furniture`. V4.3.1: review, only `misplaced_support_furniture`. It declared the visible table anatomy coherent despite nonparallel sides.
3. Office printer table with missing legs. Human: fail, `missing_required_support`. V4.3.1: pass. It invented a coherent hidden load path from a visible rail/partial leg.
4. Home printer visibly slanted on its table; unrelated puzzle under table. Human: fail, `device_support_axis_conflict` + `incoherent_prop_arrangement`. V4.3.1: pass. It called the rotation intentional and the puzzle coherent without visible functional evidence.
5. Printer table/wall/cabinet perspective conflict. Human identifies `conflicting_perspective`; no absolute verdict. V4.3.1: pass. It asserted a single perspective without testing edge families and depth.
6. Printer placement good; disfigured glasses unrelated. Human: placement pass/warn only. V4.3.1: pass. Correct placement verdict, though it omitted the unrelated-artifact warning.

Aggregate: 6/6 structurally valid, 2/7 required issue codes, 2/5 labeled verdicts, zero forbidden-issue cases. V4.1 found zero expected issues on its four completed overlapping cases. The current judge improved, but is not safe to scale.

The exact recurrent failure is: observe a suspicious geometric relation, propose a hypothetical benign story, then mark the positive condition satisfied. We want a defect-oriented scout: `yes` means a visible defect. It must test geometry before proposing a benign interpretation.

## Required V4.4 direction

1. One defect-oriented visual scout call. Reverse polarity: `yes` means visible defect, `no` means visibly tested and absent, `unknown` means genuinely hidden/unresolvable.
2. Mandatory visual inventory and explicit audits of:
   - support/table topology, corners, edge families, legs/panels/pedestals and load path;
   - product footprint/front and product-vs-support corresponding edge slopes;
   - table/furniture/wall/floor/cabinet perspective and depth ordering;
   - operating approach, user/chair relation, props blocking access, and activity/use-zone coherence;
   - support contact, scale, shadows/reflections.
3. The scout proposes defect code, severity, evidence region, and direct visible evidence. It must not turn missing evidence into a defect.
4. A separately prompted verifier receives the raw scene, twin, deterministic support crop, optional deterministic geometry/edge overlay, and only the scout's proposed material defects. It independently confirms/rejects/marks uncertain each proposal. It must not receive human labels.
5. Deterministic application scoring. Suggested policy: confirmed severity >=2 causes fail; verified/observed severity-1 review warning causes review; uncertain material proposal causes review but is not a confirmed issue; rejected proposal does not count. Avoid duplicate penalties.
6. Preserve raw scene alongside aids. An edge overlay is not proof and should be ignored if it conflicts with pixels.
7. Do not rely on calibration anchors from evaluated cases. Fresh evaluation cases must have no target/anchor leakage.
8. Bounded structured outputs: avoid the V4.2 failure where duplicated prose exhausted 24k tokens. Minimize wire enums and duplicated evidence.

## Requested answer

Provide:

1. exact scout system-prompt language that prevents benign-rationalization and defines defect polarity;
2. a compact strict scout JSON shape, including fixed tests and evidence fields;
3. exact verifier system-prompt language and compact verifier JSON shape;
4. deterministic reconciliation/scoring/verdict algorithm, including severity/confidence and observability;
5. how to use a full raw image, SIFT-derived support crop, and Canny/Hough edge overlay without treating algorithmic lines as truth;
6. semantic invariants and regression tests for the six failure modes above plus clean controls;
7. likely failure risks and a stop/go criterion for a six-case development gate and a frozen fresh 8–12 case set.

Keep scope to image-judge design. Do not recommend human post-editing, target-label injection, or scaling to 160 before the gates pass.
