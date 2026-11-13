---
type: concept
title: Pluto troubleshooting
tags: [adobe-infra, compute, pluto, troubleshooting, debugging, nccl, ssh]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs-extras]]"]
---

# Pluto troubleshooting

Common failure modes on [[wiki/entities/pluto|Pluto]] and how to diagnose them — queued jobs, exit codes, NCCL timeouts, and SSH.

## Queued jobs

Hover over the **Queued** icon in the job list to see the specific reason and resolution steps (relates to [[wiki/concepts/quota-and-utilization|quota]] and [[wiki/concepts/allocation-priority-tiers|priority tiers]]).

## Job failure exit codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General error |
| 126 | Command cannot execute (permissions) |
| 127 | Command not found in PATH |
| 130 | User terminated (Ctrl+C) |
| 137 | Killed by signal |
| 255 | Exit status out of range |

## UI / feature issues

- **VS Code / log-browsing links missing:** VSCode must run within the job; if unavailable, the Project config restricts it — ask your Project Admin to enable.
- **Stale UI after a deploy:** hard refresh (Cmd+Shift+R / Ctrl+Shift+R) or clear the last hour of browser cache.

## NCCL timeouts

- **Setup timeouts:** node allocation and image-download times vary — use explicit node synchronization or tune the PyTorch elastic timeout (default 10,000,000 s).
- **Training timeouts:** common causes are checkpoint downloads, distributed checkpoint loading, and data-loader init; check logs for OOM, data-loader hangs, and hardware issues.
- **Recommended timeout settings:** FSDP/FSDP2 → 5 minutes during training (enables auto-recovery); HSDP → 30-minute default.

## SSH

| Issue | Fix |
|---|---|
| Authentication failure | SSH key perms `600`; public key in `~/.ssh/authorized_keys` |
| Timeout | Test with `ping` / `telnet` |
| Host key verification failed | `ssh-keygen -R <hostname>` |
| Connection refused | Confirm the SSH daemon is running on target |
| macOS Private Relay | Disable: Settings > Apple ID > iCloud > Private Relay |

Verbose debugging: `ssh -v hostname`.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/concepts/quota-and-utilization]]
- [[wiki/concepts/allocation-priority-tiers]]
- [[wiki/concepts/pluto-operations]]
- [[wiki/sources/pluto-docs-extras]]
