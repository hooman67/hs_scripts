# PR 4403 dynamic-prop V6.1 full-160 experiment

This package evaluates Adobe-Firefly/foundry PR 4403 at commit
`d197e8058e37ddaded0a41e55d46da6985b6e0a1` over the frozen V6.1 set.

The treatment replays each control row's reference choice, Stage-A geometry,
digital-twin camera, and exact geometry-guide bytes. It runs the PR's new Stage-B
dynamic prop construction and one GPT Image 2.5 edit. This isolates the prop-prompt
change from reference and geometry differences.

Rows use the existing Latin-square schedule: every four submissions include all
four products and rotate camera positions, producing broad device/view coverage
early. The run is serial because the package temporarily replaces `build_guide`
with each row's frozen guide. It is resumable and publishes the live comparison
gallery after each of the first four rows and every subsequent four rows.

Live gallery:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_v6_1_pr4403_dynamic_props_20261106/gallery/index.html

The existing natural-placement judge does not measure prop construction quality.
After all images finish, build a paired prop-quality evaluation against the frozen
V6.1 controls; keep any placement-judge results separately labeled.
