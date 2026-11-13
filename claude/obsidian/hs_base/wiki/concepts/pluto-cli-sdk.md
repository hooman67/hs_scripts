---
type: concept
title: Pluto CLI and Python SDK
tags: [adobe-infra, compute, pluto, cli, sdk]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs-operations]]"]
---

# Pluto CLI and Python SDK

The `aip` command-line tool and the `adobe-aip-sdk` Python package are the scriptable interfaces to [[wiki/entities/pluto|Pluto]], mirroring what the [[wiki/concepts/pluto-console|web console]] does for jobs, projects, initiatives, and clusters.

> Note: `aip` here is the **Pluto/AI-Platform** CLI (`adobe-aip-cli`). Distinct from the shell alias `aip="python -m colligo.pluto.sdk.cli"` in Hooman's environment, though both target the same Pluto platform.

## Install & authenticate (CLI)

Requires **Python 3.10+**; "supported only on macOS" (Windows users install inside a CPU interactive session). Steps:

1. Get a UW2 Artifactory API key (log in via SAML SSO → profile → Generate API Key), then:
   ```bash
   export ARTIFACTORY_UW2_API_TOKEN=<YOUR-KEY>
   export ARTIFACTORY_UW2_USER=<YOUR-LDAP>
   export EXTRA_INDEX_URL=https://$ARTIFACTORY_UW2_USER:$ARTIFACTORY_UW2_API_TOKEN@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple
   ```
2. Install: `pip install "adobe-aip-cli" --extra-index-url=$EXTRA_INDEX_URL`
3. Login: `aip login` (device flow — opens a URL, enter the code). Logout: `aip logout`.
4. Check versions: `pip index versions adobe-aip-cli --extra-index-url="$EXTRA_INDEX_URL"`

## Command structure

`aip <COMMAND> <SUBCOMMAND> <OPTIONS>`. Common flags: `--help`, `--project <PROJECT_NAME>`.

**Config / auth / info:** `aip config set|get|list|clear project`, `aip login`, `aip logout`, `aip info`, `aip images list|info|validate`, `aip initiative list`, `aip project list [--all]`, `aip project roles list`.

**Job management:**

| Command | Action |
|---|---|
| `aip job create` | Create a job (flags below). |
| `aip job start <JOB>` | Launch (`--env KEY=VALUE` for env vars). |
| `aip job stop <JOB>` | Stop a running job. |
| `aip job pause <JOB>` | Snapshot, then pause. |
| `aip job restart <JOB>` / `restart-pod` | Restart a stopped job / specific pods. |
| `aip job list` | List jobs (filter by status/owner/initiative). |
| `aip job status <JOB>` | Current state. |
| `aip job list-pods <JOB>` | Pod mappings & names. |
| `aip job logs <JOB>` | Script/pod logs (`--all-pods`). |
| `aip job ssh <JOB>` / `configure ssh` | Interactive/remote exec / set up SSH (`--cleanup`). |
| `aip job log-dir <JOB>` | Logging-fs path for a pod. |
| `aip job save <JOB>` | Create a snapshot. |
| `aip job archive <JOB>` | Delete a stopped job. |
| `aip job tags add\|list\|remove <JOB> --tag <TAG>` | Manage tags. |
| `aip job trigger-pfc <JOB> <CHECK_TYPE>` | Preflight checks: `gpu-health`, `nccl-health`, `efa-health`, `system-health`, `dcgm-health`. |
| `aip job roles list\|available\|add\|remove\|set <JOB> [--role <ROLE>]` | Resource access roles. |

### `aip job create` flags

`--name` (required); `--gpu-instance-type` or `--cpu-instance-type` (one required); `--job-type [training|interactive]`; `--image <URI>`; `--main-script <PATH>` (repeatable) and `--init-script <PATH>`; `--num-pods <INT>` and `--xpus-per-pod <INT>`; `--start`; allocation modes `--guaranteed` / `--quota-charged-reclaimable` / `--quota-free` / `--limited-time-access` (see [[wiki/concepts/allocation-priority-tiers]]); `--enable-autorecovery` + `--autorecovery-version [v1|v2]`; `--enable-otel`; `--gpu-health-check [disabled|basic|medium|long]`; `--docker`; `--repo <URL>` + `--ref <GIT_REF>`; `--snapshot-id <ID>`.

**GPU instance types:** `g4dn.12xlarge, g5.4xlarge, g5.8xlarge, g5.12xlarge, g6e.12xlarge, p4d.24xlarge, p4de.24xlarge, p5.48xlarge, p5en.48xlarge, p6-b200.48xlarge`.
**CPU instance types:** `c5.4xlarge, c5.12xlarge, c5.18xlarge, c5d.4xlarge, c5d.24xlarge, c6i.24xlarge, c6id.24xlarge, c6id.32xlarge, r6id.32xlarge`.

### Example — submit a multi-pod training job

```bash
aip job create \
  --name my-training-job \
  --image docker-registry/my-image:latest \
  --project my-project \
  --gpu-instance-type g5.12xlarge \
  --xpus-per-pod 2 \
  --num-pods 2 \
  --init-script "init.sh" \
  --main-script "train1.sh" \
  --main-script "train2.sh"

aip job start my-training-job --project my-project --env CUSTOM_ENV_VAR=custom-value
aip job status my-training-job --project my-project
aip job stop my-training-job --project my-project
aip job archive my-training-job --project my-project
```

## Python SDK

Package `adobe-aip-sdk` (same Artifactory index / Python 3.10+ setup as the CLI):
`pip install "adobe-aip-sdk" --extra-index-url=$EXTRA_INDEX_URL` (`--upgrade` for latest).

All operations are **async**: create an auth provider → open a session with client(s) → await client methods. It exposes async clients for jobs, projects, initiatives, clusters, etc. — mirroring the CLI — and respects the same per-user rate limits. Reference example: `platforms/pluto/packages/aip-sdk/examples/session_example.py`.

```python
import asyncio
from aip_sdk.auth.env_access_token_provider import EnvAccessTokenProvider
from aip_sdk.session import job_client_session

async def main() -> None:
    provider = EnvAccessTokenProvider("PLUTO_AUTH_TOKEN")
    async with job_client_session(provider) as job_client:
        result = await job_client.list_jobs(size=5)
        for job in result.jobs:
            print(job.job_id, job.name)

asyncio.run(main())
```

The `PLUTO_AUTH_TOKEN` env var used here is one of the [[wiki/concepts/pluto-job-lifecycle|platform-managed variables]] injected into every job pod.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/pluto-console]]
- [[wiki/concepts/allocation-priority-tiers]]
- [[wiki/sources/pluto-docs-operations]]
