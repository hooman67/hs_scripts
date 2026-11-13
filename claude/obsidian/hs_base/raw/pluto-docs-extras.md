---
type: raw
title: "Pluto docs — extras (storage / secrets / docker / jupyter / policy / troubleshooting)"
raw: "[[raw/pluto-docs-extras]]"
ingested: 2026-07-04
---

# Pluto docs — extras (raw capture)

> Provenance: fetched from `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/` on **2026-07-04**. Immutable — do not edit. Distilled into `wiki/` pages.
>
> Source URLs:
> - `blogs/snapshot_announcement.html`
> - `file-system.html`
> - `s3-access.html`
> - `secrets.html`
> - `docker.html`
> - `using-docker.html`
> - `jupyter-user-guide.html`
> - `troubleshooting.html`
> - `policy/global-config.html`
> - `policy/project-init-policy.html`
>
> All 10 URLs succeeded (no 404s). Other nav pages noted but not fetched: `logs.html`, `ssh.html`, `preflight-checks.html`, `custom-job-telemetry.html`, `scheduler.html`, `network-access.html`, `support.html`, `cli-using.html`, `python-sdk.html`.

---

## blogs/snapshot_announcement.html — Snapshots

Snapshots preserve "the current root file system state" of an interactive session, letting you resume without losing progress when a session stops.

Two primary actions (buttons on the job detail page):
1. **Save** — creates a snapshot of the session's root file system and stores it off the running node.
2. **Pause** — saves the filesystem state and simultaneously terminates the job.

Restoration: when restarting an interactive session, it automatically "restarts from the last snapshot you saved," eliminating the need to recreate previous work.

Reference: "For more information, see [Jobs - Creating a snapshot](../jobs.html#creating-a-snapshot)".

---

## file-system.html — File system

Storage options:

| Location | Purpose | Persistence | Speed |
|---|---|---|---|
| `/mnt/localssd` | Training datasets, model files | Until job terminates | Fastest |
| `/home/colligo` | Conda environments, code, executables | Job termination unless snapshotted | Medium |
| `/sensei-fs-3` or `/sensei-fs` | Shared training data, collaboration | Indefinite | Slower |
| S3 | Checkpoints, dataset/model backups | Indefinite | Slower |

**Local SSD** capacity per core:
- CPU X86_64: 25GB
- A100_40GB: 530GB
- A100_80GB: 530GB
- H100_80GB: 478GB

⚠️ "Files saved to local SSD are _not_ backed up and do not persist after a job is terminated!" Back up to root filesystem or S3, then save a snapshot.

**Root file system (EBS):** Home directory `/home/colligo`, separate per job and non-shared. Files persist when you pause (snapshot) or explicitly save a snapshot before terminating. Not automatically backed up on job termination. ⚠️ Do not clone the colligo repo to `/home/colligo` — use `/mnt/localssd` instead, or leverage GitHub code distribution in training jobs.

**Sensei FS (FSx for Lustre):** Default quota **500GB**. Automatically replicated to S3. Files accessed less than 7 days are evicted (metadata retained; re-fetching takes seconds). Private user directory at `<FS_ROOT>/users/your_username`; tenant directories at `<FS_ROOT>/tenants` (requires tenant membership + LDAP group). ⚠️ "Keep files in Sensei FS only if you are actively using them" due to cost.
- Access requirements: join the Sensei tenant (contact admin) and the corresponding LDAP group via the Adobe IAM portal.
- Best practices: avoid large numbers of small files (consolidate with tar/zip); don't store Conda environments, executables, or checkpoints here; use the tenant directory for team sharing, not the personal user directory.

**Logging FS:** `/logging-fs`, for job/platform logs only. ⚠️ Manually stored files will be deleted without notice.

---

## s3-access.html — S3 data access

Pluto manages S3 access through an IAM role-based system that automatically handles permissions across dev, stage, and production environments without requiring manual bucket policy edits.

⚠️ **S3 buckets must be in `us-west-2` only.** "Using S3 buckets in other regions will be much slower and more expensive, because data is sent over the open internet."

**AWS credentials (prerequisite)** via the Adobe **KLAM** tool: access the KLAM portal → select project → choose environment (dev, sandbox, stage) → generate temporary credentials (specify validity in hours) → paste into `~/.aws/credentials` under `[default]`.

**S3 bucket registration:**
1. In the AWS console S3 service, locate your bucket.
2. Copy the bucket ARN from the Properties tab (format `arn:aws:s3:::bucket-name`).
3. Register the resource in Pluto per the External Resources docs.

**Access control model:** **Resources** represent external data sources (S3 buckets); **Roles** specify access level: Read-only, Read/write, Admin.
- Project-level: project admins request role access; role owners must approve before jobs can access.
- Job-level: edit job config → "Resource Access Roles" → select applicable roles → confirm access levels.

Jobs automatically inherit S3 access from roles assigned to their parent project — no manual credential configuration needed within jobs.

---

## secrets.html — Using secrets

Secrets are stored in Adobe's **HashiCorp Vault** and managed via the Compute Platform interface. Three scopes:
- **User Secrets** — personal, accessible only to you. Avatar → User Profile → "Available Secrets".
- **Project Secrets** — team-level, stored at `dme_colligo/services/pluto/projects/<team-or-project-folder>` in Vault; an IAM group manages access.
- **Role Secrets** — organizational-level, apply across multiple projects.

**Creating user secrets (self-service):** User Profile > Secrets Available → Edit → + Add New Entry → simple string key-value pair (no nested objects) → Save.

**Creating project secrets (requires setup):** create an IAM group for your project → create a folder in Vault's project directory → file a Jira ticket asking SRE to associate the IAM group with the folder → SREs whitelist the path.

**Injection into jobs:** secrets inject as **environment variables only**, in init and main scripts. Job details → Execution Specs → Edit → + Expose New Secret → select Source (User/Project/Role), Path, Key, Environment Variable name → Save. To extract Vault's CLI path format, remove `-mount=`, strip quotes, replace spaces with `/`.

⚠️ "Never store secrets in persistent file systems, including Sensei FS, S3, or root file system." "Never hard-code secrets in job code." Use Vault exclusively.

Feature flag: user secret management requires enabling "Enable secret management" in the Debug Panel.

---

## docker.html — Docker images

**Base platform images** run on AMI `ami-001c9106ee1b8910d`: kernel `5.10.223-212.873`, Nvidia driver `550.90.07`, CUDA `12.4`.

**Certified images (allowlist):** approved list in `platforms/pluto/utilities/images/certified_images.json`. Jobs validate against it unless `--skip-certified-check`.
- Default GPU base: `docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/pluto-training-base:04-17-26-CUDA-v12.8.1-runtime-ubuntu24.04-CUDNN-v9.18.1.3-NCCL-v2.29.7-1-eagain-fix-PY-3.12-ARCH-amd64-1`
- Default CPU base: `docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/pluto-cpu:03-27-26-ubuntu-24.04-py3.12-amd64`
- Additional: `colligo/colligo-dev:latest` (GPU, Docker Colligo release); a CUDA 13.2.0 Devel variant.

**Building custom images:** (1) use the [build-image](https://github.com/OneAdobe/build-image) workflow to build/push from a Dockerfile; or (2) create a Docker-enabled job (`--docker` CLI flag) and build interactively. Docs recommend `uv` for "fast, reproducible dependency installation".

```dockerfile
FROM <certified-base-image>
COPY pyproject.toml uv.lock /workspace/
RUN uv sync --frozen --no-dev
COPY src/ /workspace/src/
```

Do: use `uv sync`/`uv pip install`; copy training scripts/config; set app env vars.
Do NOT: replace system Python; modify `/opt/`; change entrypoint/CMD; remove CUDA/NCCL/cuDNN system packages; install different CUDA versions.

**Validate:** `aip images validate <image-url>`; `aip images info <image-url>`.

**Support boundaries:** Platform team owns base OS, CUDA/cuDNN/NCCL, Python runtime, Pluto agent tooling. User owns pip packages, training scripts, model weights, data. Platform team "does not debug issues caused by user-installed packages or modifications to platform-owned layers." Rebuild custom images when certified bases update.

**Artifactory cache:** as of June 2026, images auto-route through `*.af-cache.colligo.dev`. Manual cache substitution optional but supported for other Artifactory resources.

---

## using-docker.html — Using Docker in jobs

Build and run Docker containers directly within jobs without restarting (tight build-test loop).

**Enabling:** Job's Execution Specs > Content → Enable Docker; via CLI `--docker` flag with `aip job create`. Requirements: "a job must be running with the Docker Image selected by the platform" and "run on a whole node". An A10G-1GPU node (`g5.4xlarge`) is recommended.

**Building:** platform includes **BuildKit** in newer job images (derived from `colligo-dev:1.40.4` or newer).
```
docker buildx build --no-cache --builder pluto-builder -t something:0.0.1 .
```
BuildKit lacks a traditional Docker daemon, so `--load` fails; use `--push`. Legacy images use standard `docker build -t my-image:latest .`.

**Artifactory access:** log into both registries using env vars `${ARTIFACTORY_UW2_USER}` and `${ARTIFACTORY_UW2_API_TOKEN}`.

**GPU access:** `docker run -it --gpus all ubuntu /bin/bash`.

**Sensei FS mount:** `-v /sensei-fs-3/users/$(cut -d '@' -f 1 <<< ${PLUTO_REMOTE_USER_EMAIL}):/sensei-fs`.

**Docker Compose & ports:** supported; GPU needs a `deploy.resources.reservations.devices` block. Containers listen on any port, accessible via `https://job-name-PORT.<CLUSTER>.colligo.dev/`.

**How it works:** "Docker-in-Containerd (DinC)" — a Docker daemon runs inside a containerd process managed by the platform (not Docker-in-Docker). Debug logs at `${PLUTO_JOB_LOGS_DIR}/system/dockerd/`.

---

## jupyter-user-guide.html — Using JupyterLab

**VS Code integration (recommended):** access JupyterLab through VS Code Web via "Open VS Code" in job details (Run Details > Pods > Links). Install Microsoft's Python extension first, then the Jupyter extension.

**Custom install:**
```
pip install jupyterlab ipykernel
python -m ipykernel install --user
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```
Or automate via job init scripts to start at job startup.

**Access & networking:** default port **8888**; URL pattern `https://host-name-8888.<CLUSTER>.colligo.dev/lab/tree/<file-name.ipynb>`. Authentication can be disabled (security warning). For remote access set `ServerApp.allow_websocket_origin='*'`.

**Kernels & environment:** Conda env at `/opt/conda/bin/activate`; register kernels via `ipykernel install --user`; install packages in notebooks with `!pip install` / `!conda install`.

**Persistence:** notebooks auto-save; all job-mounted volumes and persistent storage accessible via file browser; data must be saved to mounted volumes explicitly; Git via terminal or VS Code. Files persist across sessions if saved to designated volumes.

⚠️ "Setting both token and password to empty strings disables authentication, so anyone with network access can access your JupyterLab instance without a password."

---

## troubleshooting.html — Troubleshooting

**Queued jobs:** hover over the Queued icon in the job list to see the specific reason and resolution steps.

**Job failures — exit codes:** 0 success; 1 general error; 126 command cannot execute (permissions); 127 command not found in PATH; 130 user terminated (Ctrl+C); 137 process killed by signal; 255 exit status out of range.

**Feature unavailability:** VSCode and log-browsing links require VSCode to run within the job. If unavailable, the Project configuration restricts this — contact your Project Admin to enable.

**Module import issues (UI):** after platform deployment, hard refresh (Cmd+Shift+R / Ctrl+Shift+R) or clear browser cache from the last hour.

**NCCL timeouts:**
- Setup timeouts: node allocation and image download times vary; use explicit node synchronization or tune PyTorch elastic timeout (default 10,000,000 seconds).
- Training timeouts: common causes — checkpoint downloads, distributed checkpoint loading, data loader init; check logs for OOM, data loader hangs, hardware issues.
- Timeout settings: FSDP/FSDP2 → set to 5 minutes during training to enable auto-recovery; HSDP → 30-minute default.

**SSH troubleshooting:**
| Issue | Solution |
|---|---|
| Authentication failure | Verify SSH key permissions (600), public key in `~/.ssh/authorized_keys` |
| Timeout | Test connectivity with `ping` and `telnet` |
| Host key verification failed | `ssh-keygen -R <hostname>` |
| Connection refused | Confirm SSH daemon running on target |
| macOS Private Relay issues | Disable via Settings > Apple ID > iCloud > Private Relay |

Use `ssh -v hostname` for verbose debugging.

---

## policy/global-config.html — Platform policies (global)

**1. Low GPU utilization policy.** Platform averages GPU utilization hourly across the last six hours per job. Thresholds: training jobs (all sizes) below 75%; interactive large/medium (16+ GPUs) below 75%; interactive small (<16 GPUs) below 50%. Enforcement: two Slack DMs to the job owner every six hours when below threshold; final escalation to initiative/project Slack channel if configured; "Recovered" notification when utilization improves; prior violations cleared on recovery.

**2. Quota overuse enforcement.** Monitors project-level guaranteed GPU and CPU usage against allocated quota by instance type. Sequence: up to three Slack warnings to project and initiative admins (one hour apart) → configurable grace period (default 1 hour) → automatic preemption of the minimum jobs needed to restore compliance → recovery notification. Preemption priority: Quota Reclaimable (P1) first, then Quota Guaranteed (P0) only if P1 insufficient; within each group, full-node jobs, then newest, then smallest. Opportunistic projects: only Quota Reclaimable jobs eligible for preemption.

**3. Inactive job archival.** Deletes jobs older than two weeks with status Succeeded, Stopped, or Failed. Manual archival by the platform team, conducted periodically.

---

## policy/project-init-policy.html — Project & initiative policies

Initiative administrators can set policies that override global defaults, but only stricter: "You can set initiative and project policies that are stricter than the platform policy (but not more permissive)."

Configurable parameters: Job Type (training vs interactive); Job Size (Small/Medium/Large by GPU/node count); GPU Utilization Threshold (stricter must exceed platform-level); Monitoring Window (averaging hours); Grace Period (time between final notification and enforcement).

Configuration: via dedicated Initiatives or Projects interfaces — review existing policies, add new ones from templates, customize parameters.

Notifications: automatic Slack notifications to job owners on violation; organizations can configure dedicated escalation channels for team-wide visibility.
