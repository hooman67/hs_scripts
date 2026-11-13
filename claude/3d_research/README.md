# THD controllable-video workflow research

## Purpose

Understand, reproduce, and critically evaluate workflows for making accurate THD instructional
video, beginning with the Blender blockout → Seedance proposal on
`Adobe-Firefly/THD_Proj:zouyang/everbilt-render`.

The decision horizon is staged:

1. understand what the blockout workflow actually does and what its evidence supports;
2. design and run controlled experiments on Astra's ability to author useful blockouts;
3. compare other control mechanisms and hybrids;
4. decide whether any workflow should be adopted or integrated.

The target is not merely higher generation accuracy than the current THD baseline. A candidate
workflow must also reduce the expertise, bespoke asset curation, and effort required from a
non-technical customer.

## Constraints

- Research only. Do not change or integrate production code during this phase.
- Do not submit paid Seedance generations unless Hooman explicitly requests them.
- Treat prior THD work and the new blockout proposal with the same evidentiary skepticism.
- Preserve full prompts, every input, parameters, costs, and outputs in experimental artifacts.
- Prefer minimal prompt changes and controlled A/B comparisons.
- No external publishing, messaging, or shared-document edits without explicit approval.

## Current baseline

The user-selected best current result is:

https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/seedance_video_eval_sets/eval-set-2-kitchen-expanded-text-elements/results_2026-09-12_blurred_motion_bank_v2_clips_anonymized_asset_type_duration30_new_retrieval.html

It uses the curated THD motion-bank workflow. Quality and user-effort comparisons must use this as
the incumbent until the user changes the baseline.

## Evidence hierarchy

1. Current source code, executable artifacts, raw inputs/outputs, and measured experiment records.
2. Reproductions performed in this project.
3. Project documentation whose claims reconcile with the underlying artifacts.
4. Model-generated or author-written narrative without inspectable evidence.

## File map

- `PROJECT_STATE.md` — exact current checkpoint and next executable step.
- `DECISIONS.md` — confirmed decisions and unconfirmed proposals.
- `LEARNINGS.md` — durable cross-topic findings.
- `LONG_TERM_PLANS.md` — staged research horizon.
- `research-plan.md` — method, evidence schema, gates, and stopping rules.
- `research/blockout-workflow/SUMMARY.md` — canonical synthesis for the blockout proposal.
- `research/articulated-sku-rig/SUMMARY.md` — reusable CAD-derived product-rig hypothesis and input
  contract.
- `research/articulated-sku-rig/inputs/pbt01b` — first product evidence and motion inventory.
- `research/articulated-sku-rig/cad-candidates` — inspected public geometry leads and limitations.
- `research/thd-folder-context/SUMMARY.md` — loaded legacy THD experiment, pipeline, and storyboard
  context from `/home/colligo/hs_scripts/claude/thd`.
- `FFDY-8454/HANDOFF.md` — canonical end-to-end checkpoint for the completed laundry-sink 3D-motion
  POC, Seedance results, approved final cut, interactive workflow demo, published URLs, and exact
  resume instructions.
