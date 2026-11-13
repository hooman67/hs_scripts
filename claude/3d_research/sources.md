# Source catalog

As of: 2026-09-22

## Blockout proposal

- Publisher: Adobe-Firefly/THD_Proj, author Steve Ouyang.
- Immutable version: commit `b4b684f268e49bf38a6a7c0fa70b4a7a6244d878`.
- Source class: primary repository and deployed work artifacts.
- Retrieval date: 2026-09-22.
- Reproduction guide:
  https://github.com/Adobe-Firefly/THD_Proj/blob/b4b684f268e49bf38a6a7c0fa70b4a7a6244d878/docs/blockout/REPRODUCE.md
- Deployed review page:
  https://pluto-prod-zouyang-snap-restore-h2-7-0-41004.or2.colligo.dev/thd_blockout/
- Deployed page SHA-256 at retrieval:
  `ee34fba8c5efdc563b0dc80c37c8271091a29e689900c249085354195463b67e`.
- Limitation: deployed page is mutable; raw `conformance.json` was not published.

## Incumbent baseline

- Publisher: internal THD Video evaluation workflow.
- Source class: primary generated evaluation artifact.
- Retrieval date: 2026-09-22 through the Foundry S3 gateway.
- Complete URL:
  https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/seedance_video_eval_sets/eval-set-2-kitchen-expanded-text-elements/results_2026-09-12_blurred_motion_bank_v2_clips_anonymized_asset_type_duration30_new_retrieval.html
- S3 object:
  `s3://foundry-thd-enterprise-adobe-assets/seedance_video_eval_sets/eval-set-2-kitchen-expanded-text-elements/results_2026-09-12_blurred_motion_bank_v2_clips_anonymized_asset_type_duration30_new_retrieval.html`.
- Object SHA-256 at retrieval:
  `ac07b6878319a540c566f9ad28d856f53014673f10bdc6b8d689c90b3ad61577`.
- Scope: 54-shot report, 52 successful outputs, current-branch defaults stated in artifact.
- Limitation: output quality has not yet been re-graded for this research.

## Articulated miter-saw proof of concept

- Live source bank:
  `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/thd_video/seedance_rewriter/product_bank_v2_anonymized.yaml`
  at commit `efd83ead99404f7ac7c7ba3500b43f2d3e2117e9`.
- Official RYOBI PBT01B product page, retrieved 2026-09-22:
  https://www.ryobitools.com/products/33287189502
- Official RYOBI support/manual portal:
  https://www.ryobitools.com/support
- Official replacement-parts portal:
  https://ryobipower.ordertree.com/
- Generic CC BY Sketchfab model by Umut Calim:
  https://sketchfab.com/3d-models/miter-saw-ee274567dac24921a9db10fc53c62bde
- CC BY Makita LS1018 surface model by timothee.raison:
  https://sketchfab.com/3d-models/makita-ls1018-cropped-6ca8acc14d034d8bb7f7db819a223008
- 3D ContentCentral lead, access and licensing unverified:
  https://www.3dcontentcentral.com/Download-Model.aspx?catalogid=171&id=356324

## Execution environment and Astra

- Official Blender 5.2 releases and checksum source, retrieved 2026-09-22:
  https://download.blender.org/release/Blender5.2/
- Local verification record: `/mnt/localssd/blender-poc/VERIFICATION.md`.
- Official GPT-6 Astra model documentation, retrieved 2026-09-22:
  https://developers.openai.com/api/docs/models/gpt-6-astra
- Official Codex authentication documentation, retrieved 2026-09-22:
  https://developers.openai.com/codex/auth/
