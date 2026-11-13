# Runtime contract — draft 1

Root owns the creative rubric and system prompt. This file specifies deterministic code.

Input: JSON with `generated_image` (local image path), `twin_image` (local image path), `product_type` (`laptop` or `printer`), `scene_prompt` (string), `image_stage` exactly `scene_generation`. No annotations/model version labels in model messages.

Model output object:
- `schema_version`: const `placement-observations-v1`
- `product_match`: `match`, `uncertain`, `mismatch`
- `product_match_note`: string
- `components`: object with exactly five keys:
  `support_scenario`, `access_usability`, `orientation_alignment`, `scale_perspective`, `contact_integration`
- Each component: `visibility` enum `observed`, `partial`, `unobservable`; `severity` nullable int 0..4; `confidence` enum `high`, `medium`, `low`; `evidence` string; `consequence` string; `issue_codes` array unique allowed codes (below).
- `summary`: short evidence-based written explanation.
- `suggested_scene_changes`: array strings (change scene around preserved product, not original device).

0=no visible problem, 1=minor adjustment, 2=material awkwardness, 3=major functional/physical problem, 4=impossible/nonfunctional.
Unobservable => severity null, confidence low, no issue codes. Observable/partial => integer severity. Severity0 => no issue codes. Severity>0 => >=1 code belonging to component. Evidence cannot be empty. Do not force suggestions if no defects.

Codes by component:
- support_scenario: inappropriate_support, occupied_workstation, implausible_scenario, unsupported_base
- access_usability: excessive_reach, precarious_edge, blocked_operating_side, no_user_position, furniture_collision, blocked_paper_or_lid_path
- orientation_alignment: corner_facing, furniture_axis_conflict, chair_alignment_conflict
- scale_perspective: implausible_scale, conflicting_perspective
- contact_integration: floating, sinking_or_intersection, inconsistent_shadow, inconsistent_reflection

App aggregation weights: support20, access30, orientation20, scale15, contact15 (sum100). Eligible component = severity not null; component_score = 100 -25*severity. Score weighted over eligible components only, round1decimal. All unobservable => natural_placement_score=null.
Evidence coverage = sum(weight * [observed1,partial.5,unobservable0])/100, round3.
Confidence is a qualitative visibility-based label, not a probability. Overall high if coverage>=.85 and every eligible confidence high; medium if coverage>=.6 and no low-confidence eligible component; else low.

Provisional verdict logic (deterministic):
- product mismatch/uncertain OR no score => review (valid scene input mismatch must not pass; note validity reason).
- Any component severity>=3 AND confidence medium/high => fail (major-problem veto, independent of average).
- score<60 AND overall confidence!=low => fail.
- pass only score>=80 AND coverage>=.70 AND confidence!=low AND support/access/orientation each assessable at confidence medium/high AND no severity>=2 anywhere.
- else review.
Always `threshold_status`: `provisional_not_human_calibrated`. Include policy version and reason codes. No score tweaking to match thresholds.

Model strict JSON schema in observation_schema.json. Output validatable using jsonschema plus semantic checks above. App adds natural_placement_score/component_scores/coverage/confidence/verdict/verdict_reasons, retains original observation object. No generated text repair/manual edits. SDK retries transport only at most3; parse failures are saved and returned explicit error.

Meaningful tests: all hidden=>null/review not0/fail; major veto beats high average; hidden component does not lower normalized score; partial reduces coverage; low-confidence severe=>review; product mismatch=>review; score bounds; visibility-severity consistency; issue codes scoped to correct component.
