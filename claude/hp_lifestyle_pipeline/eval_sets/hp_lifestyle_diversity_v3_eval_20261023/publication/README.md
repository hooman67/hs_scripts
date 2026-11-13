# V3 diversity gallery publisher

The detached supervisor polls local V3 artifacts every 120 seconds. It performs no model or image-generation calls. It does not access S3 until the manifest authorizes image generation, all 18 candidate banks contain exactly 540 validated candidates, the selection manifest has status `approved_for_image_generation`, and all 108 selections have semantic-review status `accepted`.

Published gallery after that gate opens:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generated_v3/gallery/index.html`

Runtime files:

- PID: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/publication/publisher.pid.json`
- Log: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/publication/publisher.log`
- State: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/publication/supervisor_state.json`
- Snapshot history: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/publication/snapshots.jsonl`

Resume after an intentional stop or host restart:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
setsid -f bash -c 'exec python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/publication/supervise_publication.py --poll-seconds 120 >> /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/publication/publisher.log 2>&1'
```

The publisher uses `/home/colligo/.claude/hshariati/aws_creds.env` and refreshes expired credentials through the approved Pluto broker using the host `PLUTO_AUTH_TOKEN`. Credential values are never written to publication artifacts or logs.
