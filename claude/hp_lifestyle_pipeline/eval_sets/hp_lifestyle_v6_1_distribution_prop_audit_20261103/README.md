# HP Lifestyle V6.1 distribution and declared prop audit

This report analyzes all 160 accepted V6.1 prompt rows across 16 device/camera banks. It has three views: distribution and text quality, declared prop compliance, and the complete 261-entry runtime prop catalog for C-Tech review. It intentionally contains no image-derived claims.

The builder is hard-pinned to one accepted export and fails immediately if that file is absent. It never searches for or falls back to another revision.

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
python eval_sets/hp_lifestyle_v6_1_distribution_prop_audit_20261103/build_analysis.py
python eval_sets/hp_lifestyle_v6_1_distribution_prop_audit_20261103/validate_analysis.py
source /home/colligo/.claude/hshariati/aws_creds.env && \
  python eval_sets/hp_lifestyle_v6_1_distribution_prop_audit_20261103/publish_report.py
```

The semantic metric uses the locally cached, pinned `sentence-transformers/all-MiniLM-L6-v2` revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` with network resolution disabled.

Published report:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_v6_1_distribution_prop_audit_20261103/gallery/index.html`

`publication.json` records the uploaded object keys, local hashes, content types, cache policy, and remote verification.
