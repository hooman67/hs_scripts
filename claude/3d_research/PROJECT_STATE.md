# Project state

As of: 2026-09-28

## Status

The blockout proposal audit, laundry-sink 3D-motion proof of concept, targeted Seedance refinements,
approved shot-by-shot final cut, interactive customer-workflow mockup, recorded demo, and share page
are complete. There is no active generation or background job. Production integration remains out
of scope.

The canonical detailed handoff is:

`/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/HANDOFF.md`

## Completed research batches

1. Audited the `Adobe-Firefly/THD_Proj` Blender blockout proposal and separated demonstrated
   capabilities from unsupported general claims.
2. Inventoried the current motion-bank incumbent and began a reusable articulated-SKU hypothesis.
3. Built several laundry-sink cabinet rigs from storyboard evidence, culminating in Hooman's V4
   animation and the corrected/simplified V5 successor.
4. Rendered per-shot blockouts and ran user-approved Seedance 2.5 generations for the difficult
   cabinet assembly shots.
5. Iteratively corrected unnecessary flips, unsupported/flying panels, cabinet proportions,
   trajectory, and the Shot 7B thin-strip identity.
6. Assembled an approved 11-shot, 54.462-second final cut and published complete shot provenance.
7. Built and refined a Runway-inspired graph/chat mockup demonstrating selective 3D motion editing
   and propagation across shots.
8. Published Hooman's 4:53 screen recording both inside the result gallery and on a dedicated
   Open Graph share page.

## Current authoritative artifacts

- Detailed experiment handoff:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/HANDOFF.md`
- Hooman-authored Blender animation:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v4_image7_corrected_hooman_added_motion.blend`
- Corrected V5 successor:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v5_corrected_geometry_simplified_motion.blend`
- Approved final cut:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.mp4`
- Complete provenance gallery source:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/gallery_combined_breakdown/index.html`
- Live workflow-demo source:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/mockups/workflow_graph_v1/index.html`
- Do-not-modify workflow backup:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/mockups/workflow_graph_v1_backup_2026-09-24_perfect`
- Recorded demo:
  `/home/colligo/3d_agent_graph_demo.mov`
- Share-page source:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/share/workflow_demo_slack/index.html`

## Published outputs

- Original laundry-sink gallery:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/index.html`
- Complete blockout/provenance/final-cut/demo gallery:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/3d_blockout_combined_v1/index.html`
- Interactive workflow mockup:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/workflow_mock_v1/index.html`
- Preserved workflow backup:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/workflow_mock_v1_backup_2026-09-24_perfect/index.html`
- Recorded-demo share page:
  `https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/laundry_sink/gallery/workflow_demo_share/index.html`

## Current evidence position

`VERIFIED` for this task — Blender blockout videos materially improved control of difficult
laundry-cabinet assembly trajectories, and short role-separated prompts improved physical support
and component motion.

`ASSUMED`, not yet benchmarked — A selective 3D authoring workflow can beat the incumbent on both
accuracy and non-technical user effort. This POC demonstrates feasibility and a plausible UX, but
does not yet measure either claim on matched tasks.

## Open gaps

- No matched accuracy-and-effort benchmark against the incumbent motion bank.
- No repetition across multiple products, users, or rig-building methods.
- No CAD-derived laundry-sink geometry; the proxy is storyboard-derived.
- No measured end-to-end Astra rig-authoring experiment for this completed workflow.
- Actual Slack unfurl behavior for the Open Graph share page is unverified.
- S3 objects were hash-verified when published on 2026-09-24. A fresh check on 2026-09-28 failed
  because the broker had no Pluto token and cached credentials had expired.

## Background workers

All three prior subagents are complete:

- `improve_blender` produced and validated V5.
- `sequential_generations` completed the Shot 7B v5 failure analysis and publication work.
- `stitch_all_shots` produced the earlier all-shots first-review cut.

## Next exact step

Start the next session by reading
`/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/HANDOFF.md`. Refresh AWS access through
`/aws-creds` and fetch the latest S3 HTML before modifying any live gallery. Then ask Hooman whether
the next batch should be the matched 3D-versus-motion-bank accuracy/effort evaluation or a different
workflow idea. Do not begin paid generation or production integration without explicit direction.
