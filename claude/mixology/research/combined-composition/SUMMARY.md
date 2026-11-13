# Group composition with V3 refractions

As of 2026-10-20. Seven combined outputs generated and directly reviewed through user-authorized FAL: five V1 cases plus two targeted V2 direction follow-ups. Full results are in the new Composition + refractions tab. The system combines cup-preserving composition constraints with the frozen V3 lighting treatment; it does not change the source V3 file.

## Contents

- [Scope and method](#scope-and-method)
- [Evidence and source roles](#evidence-and-source-roles)
- [Findings and limits](#findings-and-limits)
- [Reproduction and checkpoint](#reproduction-and-checkpoint)

## Scope and method

USER-CONFIRMED: keep using FAL, replace the leaned-back orange reference, and combine multiple drinks while adding refractions whose color and direction follow each drink and the shared key light. The supplied arrangement examples are generated internally and are NOT customer-approved lighting or cup-geometry targets. The user explicitly rejected the floor/background patterns in the cola/amber staggered example.

RESEARCHER BOUND: five initial high-quality 1536 × 1024 outputs with one Astra rewrite and one advisory critique per output. Start with a cola/amber stagger and a red/orange/amber lineup; inspect before the three remaining cases, including a mirrored lighting-direction test, orange-front stagger and all-five stress case. At most two targeted follow-ups if a concrete failure warrants one small change. Preserve all combined generations and exact inputs/prompts in the third gallery tab. No modification to frozen refraction V3 or composition V1/V2.

ASSUMED default: near-frontal source viewpoints, shallow depth, upright bases on a white support, one key above/behind at camera-left, caustics extending toward camera-right foreground on the support plane. User lighting directions override the default. No wall projections are requested. The system permits them only if the user specifies a real receiving wall with a plausible downstream path.

Evaluate identity/count, own-source cup proportions, upright grounding, arrangement, V3 branching texture, per-drink hue/opacity, one shared direction, contact-to-field continuity and the absence of invented background caustics. Direction reversal is a qualitative controllability check; independently regenerated scenes do not isolate causality or guarantee exact geometry. Competing hypotheses: explicit role/color/direction constraints suffice, or joint synthesis sacrifices fidelity and should be compared with two-stage composition followed by frozen-V3 relighting in future work.

## Evidence and source roles

Drink images are authoritative only for their own contents and geometry. The new orange input is `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/ref_inputs/TCCC–Crafted-Sept-2026.png`, SHA-256 `152427247d881087c4e7835408c9f76e28ca40929b0b2dc4e89542137db257da`. Direct inspection confirms its upright pose; physical dimensions remain unknown.

Customer image 027 is the fixed STYLE-ONLY input for caustic texture, focal intensity, scale variation and falloff. It is user-approved style evidence, not source-matched truth for these cream-topped drinks. Its blue/pink liquids, elevated camera and shadow direction must not transfer to new drinks. The prior V3 wording supplies the branching-light treatment. The generated arrangement comparison is displayed for human reference and never sent to Astra or Sunburst.

All output/source bytes, ordered image roles, system/user/image prompts, provider payload hashes and queue results live under `/home/colligo/mixology_data/refraction_research_2026-10-19/combined/runs`. Requested FAL endpoints: `openrouter/router/vision` with `openai/gpt-6-astra`, then `openai/gpt-image-2.5/sunburst/edit`. Astra reasoning is enabled; FAL does not expose effort or verified backend snapshot. High-effort claims must not be inferred for that router.

## Findings and limits

Five V1 outputs are generated and directly reviewed. OBSERVED: all use upright cups with recognizable source identities; red/coral, orange/gold, amber, darker cola and pale clear-liquid fields remain distinguishable. The lineup responds correctly to the left/right key reversal, with no conspicuous colored wall patterns. The orange-front stagger fans the red/orange fields lower-left while amber goes lower-right, contrary to the shared key. Mesh and star-like junctions persist. Some cup/cream contours drift; no exact-geometry claim is supported.

RESEARCHER FOLLOW-UP: combined V2 adds only one sentence to V1: “Keep the dominant axis of every colored footprint parallel in the specified downstream direction, including the outer and rear cups; do not fan their light outward to balance the arrangement.” Test it once on orange-front and five-cup staggers, same inputs/settings/user requests. This reaches the seven-image ceiling; no further automatic revisions. The untouched source refraction V3 still supplies the lighting treatment. FAL rewrites and generations are stochastic, so a visual difference does not prove the one sentence caused it.

OBSERVED V2 RESULT: the added sentence does not consistently solve the failure. The orange-front scene still spreads red/pale light to the left. In the five-cup result, the left clear/red cup casts a lower-left field while foreground red and cola fields run lower-right. V2 also changes the five-cup layout to three rear/two front, confounding direct comparison. It is not promoted over V1. All seven retain fine mesh or star-like bright junctions to some extent. The strongest review candidates for the current direction/color question are the V1 pair and the two mirrored V1 trios; this is a researcher assessment, not customer acceptance.

The generation skills influenced the explicit image-role separation and preservation constraints; the gallery skill preserves full model inputs, exact prompts, relative URLs and unchanged IMS authentication. User-specified FAL transport takes precedence over the image skill's default built-in/CLI route.

Scores are advisory. This is a purposive, single-sample-per-case experiment, not proof of physical optical accuracy, exact source-pixel preservation, customer acceptance or generalization.

## Reproduction and checkpoint

System: `/home/colligo/hs_scripts/claude/mixology/research/combined-composition/prompts/system_v1.md`. Cases: `/home/colligo/hs_scripts/claude/mixology/research/combined-composition/cases.json`. Runner: `/home/colligo/hs_scripts/claude/mixology/research/combined-composition/scripts/run_combined.py`.

Generation ceiling reached: all seven rewrites, images, direct reviews and advisory critiques are complete; exact hashes, submitted prompts and ordered inputs pass `/home/colligo/mixology_data/refraction_research_2026-10-19/_review/combined_execution_validation.json`. The three-tab browser check passes 181 images and 907 relative links, prompts/lightbox/deep links and mobile layout, with no JavaScript errors. Existing IMS is unchanged and mocked only in the local browser. Final S3 publication/readback is recorded by the project checkpoint. Do not silently rerun completed IDs or promote V2. Gallery: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html#combined . A later experiment could compare two-stage composition/relighting or controlled receiving-plane guidance, but is not executed or authorized by this checkpoint.
