# Colligo Pluto Launcher

Starts an interactive AIP (Adobe AI Platform) GPU job with a fully configured Colligo environment. Two modes:

1. **Interactive pod** — checks out a Colligo branch, sets up the dev environment, then waits for you to SSH in.
2. **Dev supervisor** — additionally starts `dev_supervisor` with the specified spec and workers, with SSH port forwarding so you can hit the service from your laptop.

## Colligo Pluto Launcher vs Kaizen

| | **Colligo Pluto Launcher** | **Kaizen** |
|---|---|---|
| **Purpose** | Dev/debug workflow: start an interactive GPU pod with Colligo env, optionally run dev_supervisor | Automated benchmarking: submit batch evaluation jobs at scale |
| **Use case** | "I want to start `dev_supervisor --spec lego_v1` on an H100 and hit it from my laptop" | "I want to benchmark 50 prompt/model combinations overnight" |
| **Shared infra** | Uses `PlutoManager` from Kaizen for job create/start/status | Defines `PlutoManager` as the shared job management layer |
| **Location** | `models/colligo/models/firefly/load_testing/tools/` | `contrib/kaizen/` |

## Features

- **Automated Environment Setup**: Clones Colligo repo, runs `./m deps.sync`, configures credentials
- **S3 Credential Injection**: Reads AWS creds from local `colligo.dev.yaml` and injects into pod
- **Branch Selection**: Checkout any git branch (default: current local branch)
- **SSH Port Forwarding**: On by default, with auto-retry and port-conflict detection (`--no-port-forward` to disable)
- **Worker Readiness Check**: When running dev_supervisor, waits for workers via status port
- **Hybrid Local+Remote**: Deploy some workers locally, route others to a staging endpoint via `--remote-endpoint`

## Prerequisites

1. **Activate Colligo dev environment** (every shell session):
   ```bash
   source m
   ```

2. **Install Pluto CLI and kaizen dependencies** (first time only):
   ```bash
   bash models/colligo/models/firefly/load_testing/tools/pluto_cli.sh
   ```
   This installs `adobe-aip[compute]`, kaizen requirements, prompts for AIP login,
   and adds the `aip` alias to `~/.zshrc` (macOS) or `~/.bashrc` (Linux).
   Requires `ARTIFACTORY_UW2_API_TOKEN` to be set (see `.env` or team docs).

3. **Log in to AIP** (if session expired):
   ```bash
   aip login
   ```

## Usage Scenarios

### Scenario 1: Interactive Development

Create a job with Colligo environment ready for SSH access:

```bash
python models/colligo/models/firefly/load_testing/tools/cli/colligo_pluto_launcher.py \
    --name dev-session \
    --project "My Project" \
    --branch feature/my-work
```

Then SSH into the job:
```bash
aip job ssh dev-session --project "My Project"
```

### Scenario 2: Launch pluto job and deploy pipeline using dev_supervisor on the pluto job

Start dev_supervisor on a GPU pod, 

```bash
python models/colligo/models/firefly/load_testing/tools/cli/colligo_pluto_launcher.py \
    --name load-test-job \
    --project "FF Product Eval & Optimization" \
    --gpu-instance-type p5.48xlarge \
    --spec lego_v1 \
```

Then run load tests locally (hitting `localhost:8000` via port forward):
```bash
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --combo gen45_text_encoder_v1_1024:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --total-requests 100 --concurrency 10 \
    --traffic-only
```

Or just open http://localhost:8000/debug/# for manual testing.

### Scenario 3: Hybrid Local+Remote

Deploy some workers locally and route others to a staging endpoint:

```bash
python models/colligo/models/firefly/load_testing/tools/cli/colligo_pluto_launcher.py \
    --name load-test-job \
    --project "FF Product Eval & Optimization" \
    --gpu-instance-type p5.48xlarge \
    --spec lego_v1 \
    --local-deploys lego_pipeline,gen45_text_encoder_v1_1024 \
    --remote-endpoint https://lego-v1-dev.ethos851-stage-or2.ethos.adobe.net/
```

Or configure the same in `colligo.dev.yaml` and just pass `--spec`:

```yaml
# colligo.dev.yaml
remote_deploy_per_spec:
  lego_v1:
    local_deploys: [lego_pipeline, gen45_text_encoder_v1_1024]
    remote_deploys: []
    endpoint: https://lego-v1-dev.ethos851-stage-or2.ethos.adobe.net/
```

```bash
python models/colligo/models/firefly/load_testing/tools/cli/colligo_pluto_launcher.py \
    --name load-test-job \
    --spec lego_v1
```

### Scenario 4: End-to-End Remote Load Testing

Run the entire load test on the pod (start server + run test + download results):

```bash
python models/colligo/models/firefly/load_testing/tools/cli/run_load_test.py \
    --remote \
    --combo gen45_text_encoder_v1_1024:1 \
    --spec-name lego_v1 \
    --capture-session-id lego-v1-captured-locust-2026-03-03 \
    --project "FF Product Eval & Optimization" \
    --gpu-instance-type p5.48xlarge \
    --total-requests 100 --concurrency 10
```

### Scenario 5: Remote Combinatorial Sweep

Run a full combinatorial sweep on the pod:

```bash
python models/colligo/models/firefly/load_testing/tools/cli/run_combinatorial_load_test.py \
    --remote \
    --project "FF Product Eval & Optimization" \
    --gpu-instance-type p5.48xlarge \
    --config models/colligo/models/firefly/load_testing/configs/image5_lego_v1.yaml
```

## CLI Options

### Required
- `--name`: Job name prefix (timestamp auto-appended)
- `--project`: AIP project name

### Git/Repo
- `--branch`: Git branch to checkout (default: current local branch)

### Job Configuration
- `--gpu-instance-type`: GPU instance type (default: `g5.8xlarge`, use `p5.48xlarge` for H100)
- `--num-pods`: Number of pods (default: `1`)
- `--xpus-per-pod`: GPUs per pod (default: `1`)
- `--image`: Docker image URI (default: latest Colligo dev image)
- `--extra-envs`: Additional Python envs to create (e.g., `vllm_0_18_0`)

### Dev Supervisor
- `--spec`: Dev supervisor spec (e.g., `lego_v1`). When provided, dev_supervisor is started automatically.
- `--local-deploys`: Workers to deploy locally, comma-separated. Optional replica counts (default: 1). E.g., `gen45_text_encoder_v1_1024` or `gen45_text_encoder_v1_1024:1,nsfw_adobe_one:2`
- `--remote-endpoint`: Remote staging endpoint for workers not in `--local-deploys`. Configures `colligo.dev.yaml` `remote_deploy_per_spec` so the pipeline routes non-local workers to this URL
- `--profile`: Enable profiling

### Port Forwarding
- `--no-port-forward`: Disable SSH port forwarding (enabled by default)

## Troubleshooting

### S3 Credentials Error
Run `./m sys.setup` to populate `colligo.dev.yaml` with S3 credentials from Vault.

### Job Creation Fails
- Verify you're logged in: `aip info`
- Check project name: `aip project list`
- Verify GPU availability in project quota

### SSH Connection Fails
- Ensure SSH keys are registered in IAM: go to [iam.corp.adobe.com](https://iam.corp.adobe.com/) > **Accounts > Services > SSH Key > Add SSH Key** (allow ~15 min for sync)
- Check job is running: `aip job status <job_name> --project <project>`

### Port Forwarding Fails
- The launcher auto-detects port conflicts and uses alternative ports (9000+)
- Use `--no-port-forward` to skip if not needed
- Check logs: `aip job logs <job_name> --project <project>`

## See Also

- [Kaizen (contrib/kaizen/)](../../../../../../../contrib/kaizen/) — Automated benchmarking on Pluto
- [Load Testing Tools](.) — `run_load_test.py`, `run_combinatorial_load_test.py`
- [AIP CLI Documentation](https://docs.ai.corp.adobe.com/pylibs/colligo/pluto/aidoc/cli-using.html)
