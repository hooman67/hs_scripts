# RAW: Pluto docs — operational sub-pages

> **Provenance.** Fetched 2026-07-04 from the Adobe AI Platform (Pluto / "Compute Platform") docs,
> base URL `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/`. Source URLs listed per section
> below. **Immutable** — do not edit. This is condensed/paraphrased from the rendered HTML via
> WebFetch (a small summarizing model), NOT byte-verbatim; quoted strings in "double quotes" are
> reproduced as-is from the pages. This file covers the operational sub-pages beyond the
> index/concepts pages already captured in [[raw/pluto-docs]].

---

## getting-started.html
Source: `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/getting-started.html`

### Prerequisites & access
1. Be in an LDAP group: join `CT_SENSEI_*` or `CLOUDTECH_SENSEI_*` via the Adobe IAM portal
   (https://iam.corp.adobe.com/login).
2. After approval email arrives, "wait for two more hours" for LDAP synchronization.
3. Verify membership: `ldapsearch -H ldap://ldap2-ext-or1.adobe.net:389 -x -ZZ -LLL -b ou=Users,o=adbe cn=LDAP_USERNAME memberOf`

### Login
- Navigate to https://ai.corp.adobe.com/ (requires Adobe network / VPN).

### Starting an interactive session (UI)
From the Jobs page, click **+ Create Job** → **Interactive Session**:
- **Project**: use "Platform Guest (Platform)" if not yet assigned to a project.
- **Allocation Mode**: "Limited Time Access" (allows up to 2 concurrent sessions, 3 GPUs total).
- **Host Type**: CPU or GPU.
- **Docker Image**: default or custom image URL.
- Click **Create & Start**.
- Once running, scroll to **Run Details** → click **Open VS Code** for a browser-based dev environment.

### Project membership
- Visit the Projects page (https://ai.corp.adobe.com/projects); contact your initiative admin
  (listed under Initiative > See Details) to join a project.

### Sensei FS access
- Tenant directories at `/sensei-fs-3`; join your team's Sensei tenant (contact tenant admin) and be
  in the corresponding LDAP group; verify via the ldapsearch command above.

### Debugging jobs
- **View logs**: job details → **Run Details** → **Browse logs** (running) or **(Download)** (stopped).
- **Telemetry**: **Job Telemetry Dashboard** (resource graphs) and **Open Node Telemetry Dashboard** (Grafana).
- **Pod status** colors: Green (running), Red (error), Yellow (stopped).

---

## jobs.html
Source: `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/jobs.html`

### Job types
1. **Interactive Sessions** — "for interactive development and testing that you can connect to using
   Visual Studio or a Bash shell." Persist until explicitly stopped.
2. **Training Jobs** — batch execution; terminate when scripts exit.
- The "Keep Failed Pods Running" setting can override the terminate-on-exit behavior.

### Job lifecycle states (verbatim state names)
- **Draft** — Created but not yet started.
- **Pending** — Scheduled, awaiting resource/quota allocation.
- **Starting** — Resources allocated; pods initializing.
- **Queued** — Insufficient resources to begin.
- **Running** — Accessible and executing.
- **Running Unstable** — Some pods running while others failed.
- **Failed** — At least one pod failed or returned non-zero exit.
- **Succeeded** — All pods completed successfully.
- **Stopping** — Terminating, not accessible.
- **Stopped** — Terminated, not accessible.
- Jobs exceeding two weeks in Succeeded/Stopped/Failed states face archival.

### Creating a job (UI)
Interactive Session: **+ Create Job** → "Interactive Session" → unique name → Project ID → Host Type
(GPU/CPU) → instance type + resource count → Docker image → "Create & Start".

Training Job: **+ Create Job** (Training Job selected by default) → name → Project ID → "Create" →
edit job details (compute type, instance type, add scripts) → start execution.

### Job creation parameters
Name (unique), Project ID, Host Type (GPU/CPU), GPU Instance Type, CPU cores / GPU count, Docker
Image URL, Allocation Mode (resource borrowing strategy).

### Job management actions
- **Non-running jobs**: Start, Set notifications, Delete (archive).
- **Running jobs**: Open VS Code, Restart, Stop, Pause and create snapshot, Save snapshot (keep
  running), Set notifications, View logs and telemetry.

### Snapshots
- Preserve "the contents of the root disk stored to a central location." Capture `/home/colligo` but
  EXCLUDE `/mnt/localssd` and GitHub code distributions.
- Timing: "Creating and saving a snapshot takes around 1.5 - 2 seconds per GB; restoring takes 2 - 3
  seconds per GB."
- Operations: pause job to create snapshot; save snapshot while running; restart from snapshot;
  remove Snapshot ID to restart from the Docker image instead.

### Platform-managed environment variables
`JOB_NAME`, `JOB_UUID`, `RANK`, `NUM_OF_GPUS`, `NUM_OF_CPUS`, `PLUTO_AUTH_TOKEN`, `PLUTO_JOB_RUN_ID`,
`POD_UUID`, `NODE_NAME`, `PLUTO_LOCAL_USER_ID` (1000), `PLUTO_LOCAL_GROUP_ID` (100). Do not override.

### Persistent URLs
- Jobs get persistent domain names: `https://$HOSTNAME-<PORT>.jobs.colligo.dev`
- Hostname format: `pluto-prod-<LDAP_ID>-<CUSTOM_JOB_NAME>-<RANK>-PORT`
- Ports 8000-8006 for applications; VS Code uses port 20000.

---

## editing-a-job.html
Source: `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/editing-a-job.html`

- Access: click a job → **Edit** button at upper right of each section.
- **Editable without stopping**: job name & description; Tags; Notification recipients (Slack
  channels); Resource Access Roles (must add before starting the job).
- **Requires stopping the job first**: Scheduling Spec (GPU/CPU + instance type & count; allocation
  mode P0/P1/P2/limited-time; elastic min/max pods; auto-requeue on preemption for P2; exclusive GPU
  node access); Content Spec (Docker image URL; snapshot ID; GitHub code distribution; init & main
  scripts); Runtime Config (log collection & verbose logging; Docker enablement; Burstable QoS; Vault
  secrets); Auto Recovery (enable/disable Auto Recovery V2; pod restart behavior; incidents per hour).
- **Never editable**: Job Overview settings (job type, status, project) — "set when you create a job,
  and cannot change them afterward."
- Disabled/absent Edit button = missing permission or job still running; locked settings show a lock icon.
- Scripts must be Bash. "If an init script fails, the remaining init scripts and all main scripts are
  not executed." For preemption, handle SIGTERM with a 30-second completion window maximum.

---

## projects.html
Source: `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/projects.html`

- A **project** is an organizational unit for jobs and compute; lives within an initiative; primary
  grouping for job submission and resource allocation.
- "Initiatives represent high-level strategic objectives defined by the Adobe CTO committee and
  contain _projects_."
- **Create project** (initiative admins): Initiatives page → select initiative → Projects section →
  "Create Project" → enter project details (architecture, modality, business goal, customer info,
  lifecycle stage).
- **Edit project** (initiative & project admins): project detail page → "Edit" on a section.
- **Manage members**: Members section; add/remove, single or bulk via "Enable multiselect".
- **Delete/archive project**: only initiative admins; warning if active jobs exist.
- **Quota**: each project shows GPU & CPU quota; hover blue values for node counts and availability %.
- **Transfer capacity** (initiative & platform admins): select source project/initiative → node type &
  new quota amount → destination initiative/project → justification (optional Jira ref). "The quota
  transfer will happen immediately once you click **Confirm Transfer**."
- **Resource access roles**: project admins request roles so "jobs created in the project will have
  access to that resource" (e.g. S3 buckets); role owners must approve.
- Sensei FS tenants; Slack notifications (quota updates, job failures, preemptions); users must be
  project members to submit jobs / use quota.

---

## clusters.html
Source: `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/clusters.html`

- Clusters page is for "platform developers and SREs"; regular users cannot modify cluster settings.
- Shows inventory of all clusters; click a cluster to view its EKS node groups.
- Node groups: "Jobs can only run on a single node group"; "The nodes in a node group are homogeneous."
- **Cordon a node**: node group → **VIEW** → **EDIT** → set **Cordon rank** → **CORDON NODE** → **Save**.
- Page notes "_MORE DETAILS TBD_" — section incomplete (capacity/utilization metrics and full admin
  ops not yet documented).

---

## scheduler.html
Source: `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/scheduler.html`

### Scheduling hierarchy (priority order)
1. **P0 (Quota-charged — guaranteed)** — highest priority.
2. **P1 (Quota-charged — reclaimable)** — medium priority.
3. **P2 (Quota-free — spare capacity)** — lowest priority.
"higher-priority workloads are always considered before lower-priority ones."

### P2 job evaluation
- Examines all P2 jobs in randomized order to prevent consistent favoritism.
- Schedules those fitting available resources immediately; queues the rest, re-evaluating "whenever
  there is a change that can result in allocation" (~every second when conditions change).

### Preemption
- P2 preempted first; P1 preempted only if P0 needs resources; P0 never preempted.
- Selection "minimize impact": targets "lowest-priority eligible jobs" using "minimal excess
  capacity"; within a priority level selection is "non-deterministic".

### Quota models
- **Project-based (default)**: each project's quota independent; P0/P1 confined to project allocation.
- **Initiative-based (opt-in)**: scheduler "considers aggregated project quota usage at the initiative
  level and ignores individual project quotas" — cross-project sharing within an initiative, while
  keeping project-level permission/authorization boundaries.

---

## cli-using.html
Source: `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/cli-using.html`

- Requires Python 3.10+; "supported only on macOS." Windows users install it in a CPU interactive session.
- Configure Artifactory: log into UW2 Artifactory via SAML SSO → username → Edit Profile → Generate
  API Key → copy key. Set:
  `export ARTIFACTORY_UW2_API_TOKEN=<YOUR-KEY>` and `export ARTIFACTORY_UW2_USER=<YOUR-LDAP>`
- Package index:
  `export EXTRA_INDEX_URL=https://$ARTIFACTORY_UW2_USER:$ARTIFACTORY_UW2_API_TOKEN@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple`
- Install: `pip install "adobe-aip-cli" --extra-index-url=$EXTRA_INDEX_URL`
- Login: `aip login` (displays URL + code, device flow). Logout: `aip logout`.
- Check versions: `pip index versions adobe-aip-cli --extra-index-url="$EXTRA_INDEX_URL"`

---

## cli.html + cli-jobs.html
Sources: `.../cli.html`, `.../cli-jobs.html`

Syntax: `aip <COMMAND> <SUBCOMMAND> <OPTIONS>`

### Config / auth / info
- `aip config clear` / `aip config get project` / `aip config list` / `aip config set project <PROJECT_NAME>`
- `aip login` / `aip logout`
- `aip info` — session details
- `aip images list` | `aip images info <IMAGE_URL>` | `aip images validate <IMAGE_URL>` (`--skip-labels`)
- `aip initiative list`
- `aip project list` (`--all`) | `aip project roles list`

### Job management
- `aip job create` — extensive config options (see flags below).
- `aip job start <JOB>` (`-e KEY=VALUE` / `--env` for env vars)
- `aip job stop <JOB>` | `aip job pause <JOB>` (snapshot then pause) | `aip job restart <JOB>` | `aip job restart-pod`
- `aip job list` (filter by status/owner/initiative) | `aip job status <JOB>` | `aip job list-pods <JOB>`
- `aip job logs <JOB>` (`--all-pods`)
- `aip job ssh <JOB>` | `aip job configure ssh <JOB>` (`--cleanup`)
- `aip job log-dir <JOB>` — logging-fs path for a pod
- `aip job save <JOB>` (snapshot) | `aip job archive <JOB>` (delete stopped job)
- `aip job tags add|list|remove <JOB> --tag <TAG>`
- `aip job trigger-pfc <JOB> <CHECK_TYPE>` — preflight checks: `gpu-health`, `nccl-health`, `efa-health`, `system-health`, `dcgm-health`
- `aip job roles list|available|add|remove|set <JOB> [--role <ROLE>]`

### Common flags
- `--help`, `--project <PROJECT_NAME>`

### Job creation flags
- `--name <JOB_NAME>` (required)
- `--gpu-instance-type <TYPE>` | `--cpu-instance-type <TYPE>` (one required)
- `--job-type [training|interactive]`
- `--image <URI>`
- `--main-script <PATH>` (repeatable) and `--init-script <PATH>`
- `--num-pods <INT>` and `--xpus-per-pod <INT>`
- `--start`
- Allocation modes: `--guaranteed`, `--quota-charged-reclaimable`, `--quota-free`, `--limited-time-access`
- `--enable-autorecovery` and `--autorecovery-version [v1|v2]`
- `--enable-otel`
- `--gpu-health-check [disabled|basic|medium|long]`
- `--docker`
- `--repo <URL>` and `--ref <GIT_REF>`
- `--snapshot-id <ID>`

### GPU instance types
`g4dn.12xlarge, g5.4xlarge, g5.8xlarge, g5.12xlarge, g6e.12xlarge, p4d.24xlarge, p4de.24xlarge, p5.48xlarge, p5en.48xlarge, p6-b200.48xlarge`

### CPU instance types
`c5.4xlarge, c5.12xlarge, c5.18xlarge, c5d.4xlarge, c5d.24xlarge, c6i.24xlarge, c6id.24xlarge, c6id.32xlarge, r6id.32xlarge`

### Example — create a multi-pod training job
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
```
```bash
aip job start my-training-job --project my-project --env CUSTOM_ENV_VAR=custom-value
aip job status my-training-job --project my-project
aip job list --project my-project --status running
aip job list --all --project my-project
aip job stop my-training-job --project my-project
aip job restart my-training-job --project my-project
aip job archive my-training-job --project my-project
```

---

## python-sdk.html
Source: `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/python-sdk.html`

- Package `adobe-aip-sdk` from UW2 Artifactory; Python 3.10+; Artifactory creds + `EXTRA_INDEX_URL`
  configured as for the CLI.
- Install: `pip install "adobe-aip-sdk" --extra-index-url=$EXTRA_INDEX_URL` (`--upgrade` for latest).
- All SDK operations are async. Workflow: create auth provider → open a session with client(s) →
  await client methods.
- Exposes async clients for jobs, projects, initiatives, clusters, etc. — mirrors the CLI.
- Respects the same per-user rate limits as the CLI.
- Working examples: `platforms/pluto/packages/aip-sdk/examples/session_example.py`.

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

---

## compute-cap.html
Source: `https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/compute-cap.html`

- Initiative admins distribute quota to projects based on Adobe's "quarterly prioritization process."
- Three scenarios: (1) Funded initiative member — "reach out to your initiative admin to request
  access to dedicated capacity"; (2) Non-funded collaborator — ask the funded initiative's admin, who
  may grant quota if your work "directly supports their initiative or aligns closely with its goals";
  (3) Unfunded/under-funded — escalate to manager/leadership via the quarterly prioritization process.
- Key constraint: "The AI Platform support team cannot get you any additional capacity." Only
  initiative admins and leadership can approve capacity.
- New users onboard via "Getting started with ML training" → the "Platform Guest (Platform)" project
  offers time-limited preemptible compute for experimentation.
