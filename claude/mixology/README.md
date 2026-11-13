# Mixology — reference-image style and appearance research

Owner: Hooman Shariati. Started: 2026-10-19.

Durable storage after the machine restart: `/home/colligo/mixology_data/source_restored_2026-10-19` holds the verified source snapshot; `/home/colligo/mixology_data/refraction_research_2026-10-19` holds recovered and future experiment artifacts. The old `/mnt/localssd/mixology/refraction_research_2026-10-19` path is only a compatibility symlink to home. Python: `/home/colligo/.venvs/mixology/bin/python`. Never rely on `/mnt/localssd` as the only copy. The exact recovery procedure and manifest are indexed in the project checkpoint.

Recipe-driven individual drinks with a fixed cup/camera and corrected-original group composition are published; multi-cup refraction refinement continues separately. The direct Foundry OpenAI route now executes exact Sunburst successfully; Azure still lacks its deployment. Previously published FAL results remain comparison evidence, not a guarantee of consistent geometry or caustics. Supplied arrangement examples are internally generated and NOT customer-approved lighting/geometry targets. Source refraction V3 and composition V1/V2 stay frozen. Latest publication and running-task state is in `PROJECT_STATE.md`.

Current user-selected checkpoint: **source system V3 stays frozen**. Review gallery: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html . Recipe tab: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html#recipe-to-image . Corrected group composition: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html#composition-corrected-inputs . Original refraction/composition/combined results remain in their tabs; publication counts and evidence live in `PROJECT_STATE.md`. Preferred corrected PDF inputs remain `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/overhead_013_clean.png` and `/home/colligo/mixology_data/refraction_research_2026-10-19/assets/group_027_clean.png`. Their one-off cleanup experiments stay outside the gallery narrative.

Local Colligo POC: `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/mixology`. It packages the frozen system V3 and provides a multipart debug UI for one or more reference images, a user prompt, output count, size and quality. It is verified locally on Pluto and is not a production deployment.

## Charter

USER-CONFIRMED: take reference images and modify them to achieve the desired style and appearance. Use Astra for research/reasoning and GPT Image 2.5 for image generation/editing. The first authorized batch establishes model access through Adobe Foundry and records a real image-edit test.

Follow the complete research operating playbook at `/home/colligo/.codex/RESEARCH_RULES.md`. Read this charter and the project checkpoint before resuming. Keep all reference roles, full prompts, model settings, and outputs traceable; preserve prior results. Use small, controlled prompt changes and evaluate appearance separately from preservation of source details.

## Scope and boundaries

The initial access test used a synthetic reference and is complete. On 2026-10-19 the user supplied the customer PDF, curated refraction examples and preferences, and authorized iterative GPT Image 2.5 experiments plus a Foundry S3 review gallery containing all prompts, inputs and outputs. Current work builds an Astra prompt rewriter for a minimal request such as "Add refractions." Keep customer data within these authorized research/model/gallery workflows. Do not inherit HP's blue-area target or KDP's holdout policy as Mixology requirements. Messaging people and production integration remain outside scope.

Current evidence takes precedence over historical notes. Use primary gateway/SDK documentation and actual responses for access claims. Record VERIFIED, ASSUMED, UNVERIFIED, and USER-CONFIRMED claims distinctly.

## File map

- `/home/colligo/hs_scripts/claude/mixology/PROJECT_STATE.md` — exact current checkpoint and next step.
- `/home/colligo/hs_scripts/claude/mixology/DECISIONS.md` — scope, decisions, and revisit triggers.
- `/home/colligo/hs_scripts/claude/mixology/LEARNINGS.md` — durable findings and qualifications.
- `/home/colligo/hs_scripts/claude/mixology/LONG_TERM_PLANS.md` — later phases and unresolved choices.
- `/home/colligo/hs_scripts/claude/mixology/research-plan.md` — bounded method and stopping criteria.
- `/home/colligo/hs_scripts/claude/mixology/research/model-access/SUMMARY.md` — canonical access findings, sources, and reproduction instructions.
- `/home/colligo/hs_scripts/claude/mixology/research/pdf-extraction/SUMMARY.md` — customer PDF inventory, extraction method, validation, and outputs.
- `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/SUMMARY.md` — prompt experiments, observed failures, reference provenance, and gallery.
- `/home/colligo/hs_scripts/claude/mixology/research/group-composition/SUMMARY.md` — multi-reference grouping, cup-proportion evidence, system prompt, nine completed cases and example mappings.
- `/home/colligo/hs_scripts/claude/mixology/research/combined-composition/SUMMARY.md` — joint grouping/refraction system, color/direction tests, seven samples and remaining failures. Review: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html#combined .
- `/home/colligo/hs_scripts/claude/mixology/research/group-composition-corrected-inputs/SUMMARY.md` — nine controlled grouping reruns from the five clean originals.
- `/home/colligo/hs_scripts/claude/mixology/research/multi-cup-refractions/SUMMARY.md` — bounded refinement toward a bright central core with outward branches rather than mesh.
- `/home/colligo/hs_scripts/claude/mixology/research/recipe-to-image/SUMMARY.md` — recipe text to clean single cups, fixed reference versus text-only geometry tests.

## First-batch success

A real request to the exact GPT Image 2.5 deployment returns a decodable image, the image is inspected, and the input/output/settings evidence is saved. Model listing alone does not establish inference access. This does not establish success on the eventual customer styling task.
