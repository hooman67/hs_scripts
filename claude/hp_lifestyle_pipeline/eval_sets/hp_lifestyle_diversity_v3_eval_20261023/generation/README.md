# V3 image generation runner

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation/run_generation.py`
is the provenance-checked, resumable endpoint runner for the approved 108-row
V3 selection. It validates the frozen manifest, accepted bank, selection,
source inputs, candidate text, render bytes, dimensions, and cached upload
bindings before submission.

## Current authorized run

Root approved the four byte-verified smoke rows and released the remaining 104
at 2026-10-23 22:40 UTC. The review artifact is
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/smoke_review.json`.
It records the release after checking the four rows' reference bindings,
hashes, dimensions, seed, and selected/request text equality. At the latest
release snapshot, five rows were done and four were submitted.

The durable summary at
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/summary.json`
updates after each worker result. The authorized process is running in tmux
session `hp_v3_remaining104_20261023`. Never launch a parallel duplicate.

The four-smoke invocation is preserved under
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/invocations`.
It used four row IDs, `--workers 4`, `--upload-workers 4`, and
`--poll-window-seconds 1800`.

The endpoint payload uses model ID `hp-image`, one image, seed 42, prompt
rewriting enabled with `gemini-3.1-pro`, and 50 inference steps. Every current
reference is 1024x576; the runner preserves 16:9 and requests 2560x1440 output.
It uploads the exact validated PNG bytes and stores no credentials in records
or logs.

## Local validation and preflight

Local inventory/provenance validation makes no endpoint call:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation/run_generation.py \
  --run-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023 \
  --validate-only
```

Endpoint metadata/OpenAPI preflight without image generation is available as:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation/run_generation.py \
  --run-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023 \
  --preflight-only
```

`--preflight-only` calls the endpoint metadata and OpenAPI routes but does not
upload a reference or submit an image job.

## Monitor or resume the authorized run

The durable supervisor record is
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/transition_logs/v3_remaining104_supervisor.json`.
It binds the tmux session to these artifacts:

- resume script:
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/transition_logs/v3_remaining104_resume.sh`;
- combined log:
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/transition_logs/v3_remaining104.log`;
- terminal status, written when the supervisor exits:
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/transition_logs/v3_remaining104_status.json`.

Monitor the live tmux session:

```bash
tmux attach-session -t hp_v3_remaining104_20261023
```

Use this guarded relaunch only after an intentional stop or host restart. It
refuses to start when either the tmux session or runner process is still live:

```bash
if tmux has-session -t hp_v3_remaining104_20261023 2>/dev/null || \
   pgrep -f '[r]un_generation.py --all' >/dev/null; then
  echo 'V3 generation is already running; refusing duplicate resume.' >&2
  exit 1
else
  tmux new-session -d -s hp_v3_remaining104_20261023 \
    /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/transition_logs/v3_remaining104_resume.sh
fi
```

`--all` means the frozen 108-row selection. On resume, the runner validates and
reuses each completed record and image, then processes only missing rows. It
journals a job identity before polling, so a pending or ambiguous job cannot
authorize a blind resubmission. A terminal failure remains preserved for
review. The resume script contains the exact `--all --workers 4
--upload-workers 4 --poll-window-seconds 1800` invocation and writes the log
and exit status paths above.

Monitor the durable summary and publisher without changing generation state:

```bash
pgrep -af '/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation/run_generation.py'
```

```bash
watch -n 10 "python3 -m json.tool /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/summary.json | sed -n '1,120p'"
```

```bash
tail -F /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/publication/publisher.log
```

The progressive gallery is:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generated_v3/gallery/index.html`

Publisher PID, state, and snapshot history are stored in
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/publication`.

## Preserved V2 stop checkpoint

V2 was stopped and drained without new submissions before this V3 pilot. The
final checkpoint is
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/v2_stop_checkpoints/v2_stop_checkpoint_20261023T211836.781218Z.post_drain.json`.
It records:

- 607 completed rows;
- one terminal `poll_http_404` record preserved with endpoint reason
  `unknown_job_id`;
- zero submitted jobs left to drain; and
- 710 rows never submitted (`1318` expected minus `608` terminal records).

Do not resume the V2 `--all` run. Its one 404 record and 710 unsubmitted rows
are the intended stop state. The checkpoint helper at
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation/checkpoint_v2.py`
exists to inspect that durable state; its `checkpoint-stop` and `drain
--execute` modes are operational commands, not monitoring commands.
