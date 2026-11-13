---
name: Pluto dev-box restart / new pod SSH
description: What to do when a Pluto dev-box job restarts and SSH is rejected; alias stays the same, replace the pod to re-sync the IAM key
type: reference
---
Resolved 2026-10-13 for job `pluto-prod-hshariati-hooman-cpu-de`.

- Use the alias from the job's "SSH config" field (`...-de-0`). New pod names (`-de-2-0`, `-de-2-0-<suffix>`) are NOT valid aliases; adding them breaks routing.
- Symptom `Permission denied (publickey,keyboard-interactive)` with a registered IAM key = the pod did not pick up the key. Fix = `compute_replace_pods` (aip MCP) after user confirmation; it wipes `/mnt/localssd`. Wait several minutes for proxy routing.
- Foundry projects use `PasswordAuthentication no` (key only). Generated config lives in `~/.colligo/pluto_cli/ssh_configs/job_<name>/config`.
- Don't re-register keys or edit local config first; confirm fingerprint, then replace the pod.
- Full steps: the Troubleshooting section of `commands/ssh-devbox.md`.
- 2026-10-19: ops (gpatel) snapshotted/paused the job and moved it to node group `trn01-od-or2-prod-c6id-24xl-2b`. Pod RUNNING but ssh failed: the job now has `sshEnvironmentDomain=jobs.colligo.dev`, so ProxyCommand must use `-connect %h.ssh.jobs.colligo.dev:443` (not `ssh.od1.colligo.dev:22`). `/mnt/localssd` came back empty; home survived.
