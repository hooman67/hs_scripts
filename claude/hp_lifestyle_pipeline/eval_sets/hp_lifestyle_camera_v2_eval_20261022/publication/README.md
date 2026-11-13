# Camera V2 gallery publisher

The supervisor polls the accepted prompt map and generation journals every 120 seconds. It rebuilds the gallery after a change, uploads only objects whose SHA-256 changed, verifies the S3 byte count/content type/SHA metadata, and records each publication snapshot.

Published gallery:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_eval_20261022/generated_v2/gallery/index.html`

Runtime files:

- PID: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/publisher.pid.json`
- Log: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/publisher.log`
- State: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/supervisor_state.json`
- Snapshot history: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/snapshots.jsonl`

Check status:

```bash
cat /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/publisher.pid.json
cat /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/supervisor_state.json
tail -50 /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/publisher.log
```

Resume after an intentional stop or host restart:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
setsid -f bash -c 'exec python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/supervise_publication.py --poll-seconds 120 >> /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/publisher.log 2>&1'
```

The publisher uses `/home/colligo/.claude/hshariati/aws_creds.env` and refreshes expired credentials through the approved Pluto AWS broker using the host's `PLUTO_AUTH_TOKEN`. It never writes credential values to publication artifacts or logs.
