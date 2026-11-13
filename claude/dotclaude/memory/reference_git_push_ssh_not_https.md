---
name: reference_git_push_ssh_not_https
description: hs_scripts `origin` must be SSH — HTTPS pushes fail HTTP 400 on large packs and silently break the daily auto-commit cron, so commits pile up locally and never reach other machines
metadata:
  type: reference
---

**hs_scripts `origin` must be the SSH URL**, not HTTPS:
`git@github.com:hshariati_adobe/hs_scripts.git` (not `https://github.com/hshariati_adobe/hs_scripts.git`).

**Why:** pushing this repo over **HTTPS fails with `HTTP 400` / `send-pack: unexpected disconnect`** (large pack — the repo carries lots of docs/binary-ish content). This is **not an auth failure** (401/403); it's the HTTPS transport choking on the push size. Because the daily auto-commit cron ([[reference_dotclaude_backup]], `~/hs_scripts/auto_commit.py`) does `git push origin main`, the push **fails silently** — commits (daily snapshots + manual ones) accumulate locally and **never reach GitHub or any other machine**. Symptom: another machine's `git pull` brings "nothing new" even though work was clearly done, and `origin/main` on GitHub sits stale at an old commit.

**Diagnosis (fast):**
- `git rev-list --left-right --count origin/main...HEAD` → large "ahead" number = unpushed pile-up.
- `git ls-remote origin refs/heads/main` → confirms the real remote head is stale.
- `git push origin main` over HTTPS → `HTTP 400 ... send-pack: unexpected disconnect` (transport, not auth).

**Fix (durable — also makes the cron succeed):**
```bash
git remote set-url origin git@github.com:hshariati_adobe/hs_scripts.git
git push origin main
```
SSH is key-based (no prompt, no POST-size limit), so it pushes the large pack fine and the cron's silent `git push` works going forward. Applied on the laptop 2026-09-03 (pushed `c0d1ad71..c15ddad0`).

**Per-machine:** each clone's `origin` URL is independent, so apply the `set-url` on **every** machine whose pushes fail. Needs a GitHub-registered SSH key present on that machine:
- **Laptop:** `~/.ssh/id_ed25519` already authenticates as `hshariati_adobe` (verify: `ssh -T git@github.com`).
- **Pluto boxes** (where `~/.ssh` isn't set up): use Hooman's key at `/sensei-fs/users/hshariati/doc_dont-delete/id_ed25519` (see [[reference_github_thd_proj]]; `chmod 600` a copy first, or `GIT_SSH_COMMAND`).
