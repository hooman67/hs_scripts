# V4 image runner

`run_generation.py` is the isolated, resumable 108-row runner. It verifies every source,
candidate, selection, render, and approval hash before any submission. The manifest must authorize
image generation, the accepted map must mark every bank launchable, and the selection artifact
must contain exactly 108 root-accepted rows.

The default run directory is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026`

Safe reference bindings retain the original PNG identity, dimensions, upload endpoint, blob ID,
and manifest hash. Existing jobs and records are checked before resume so known or ambiguous jobs
are not blindly resubmitted.

Use `--preflight-only` for endpoint-contract checks after root authorizes network access. Do not run
the generation mode until the root approval artifact has been applied.

After launch is authorized, the guarded launcher validates the complete 540/108 gallery contract,
validates the frozen generation inputs without an endpoint call, and then starts one resumable
eight-worker runner plus the progressive publisher:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/launch_generation_and_publisher.sh start
```

The same command can be used as `resume` after a host restart. It refuses to create a duplicate
generation process. A bounded supervisor runs at most 12 journaled invocations. After each runner
poll window, it starts another `--all` pass only when the fresh durable summary contains known
submitted jobs, safely retryable submissions, missing records, or pending records. Completed
records are verified and reused. Ambiguous submissions and terminal failures are never
resubmitted by `run_generation.py`; the supervisor stops when all 108 rows are terminally
accounted, only ambiguous rows remain, an inconsistent state needs review, or the 12-invocation
bound is reached. Generation uses eight workers and two reference-upload workers.

The durable supervisor state is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026/launch/generation_supervisor_state.json`

The launcher explicitly removes inherited GPT and AWS variables from the detached commands.
Image generation does not need GPT credentials; the publisher reads the current credential env
file and refreshes through the approved Pluto broker without logging credential values.

Read-only status:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/launch_generation_and_publisher.sh status
```

Generation log:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026/launch/generation.log`
