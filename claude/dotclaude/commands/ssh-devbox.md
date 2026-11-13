Connect to, run commands on, or copy files to/from the user's Pluto dev-box over SSH. Discovers the current dev-box ssh alias dynamically (the box name can change; the access mechanism does not). Triggers: "ssh to devbox", "connect to my dev box", "copy to dev box", "scp to pluto devbox", "push files to devbox", "pull from devbox", "run on dev box".

Usage: /ssh-devbox <operation> [args...]

Operations:
- `connect`                      — resolve the alias, confirm reachability, print the ready `ssh <alias>` command.
- `run "<remote command>"`       — run a command on the dev-box.
- `push <local...> [remote-dest]`— copy local files/dirs → dev-box (default dest `~/`).
- `pull <remote...> [local-dest]`— copy dev-box files/dirs → local (default dest `.`).

Parse $ARGUMENTS to extract:
- **operation** (required): one of `connect | run | push | pull`.
- **name hint** (optional): a fragment of the box name (e.g. `cpu-de`) to disambiguate if you have more than one dev-box. Pass as `name=<hint>` or just include it; if omitted and only one box exists, that one is used.
- **paths / command**: everything else, per the operation.

If the operation or required paths are missing/ambiguous, ask before proceeding.

---

## How it works / why (read once, then trust the discovery)

The dev-box is a **Pluto job**, not a plain host — its bare name (what the user calls it) will **not** resolve as a hostname. Pluto writes a per-job ssh config and wires it into `~/.ssh/config` via an `Include` line like:

```
Include ~/.colligo/pluto_cli/ssh_configs/job_<jobname>/config
```

Each generated config defines the **real** Host alias, of the form `pluto-prod-<user>-<box>-<n>`, with:
- `user colligo`
- a `ProxyCommand` tunneling through `ssh.od1.colligo.dev:22` (the stable Pluto entrypoint)
- `ControlMaster auto`, `ControlPath ~/.ssh/control_%n`, `ControlPersist 24h`
- `PasswordAuthentication yes` and **no key** → it is only passwordless while a live ControlMaster socket exists.

So the durable contract is: **discover the `pluto-prod-…` alias from `~/.colligo/pluto_cli/ssh_configs/*/config` at runtime and always use that alias.** Never hardcode a box name. When the user kills a box and makes a new one, only the alias string changes — this discovery finds the new one automatically.

---

## Step 1 — Discover the current dev-box alias

```bash
# All Pluto ssh aliases currently configured on this machine:
grep -rh '^Host ' ~/.colligo/pluto_cli/ssh_configs/*/config 2>/dev/null | awk '{print $2}' | sort -u
```

Resolve to a single `ALIAS`:
- If a **name hint** was given, filter the list to lines matching it (`grep -i "<hint>"`).
- **Exactly one** match → use it as `ALIAS`.
- **Several** → list them and ask the user which one.
- **None** → the box is likely down or not set up on this machine. Tell the user to (re)create/start it and establish an ssh session through their Pluto tooling first, then retry. Do not invent an alias.

```bash
ALIAS="pluto-prod-...-0"   # set from discovery above
```

## Step 2 — Confirm reachability (passwordless via the live ControlMaster)

```bash
ssh -o BatchMode=yes -o ConnectTimeout=20 "$ALIAS" 'echo OK; hostname; whoami; pwd; df -h . | tail -1'
```

- **Succeeds** → a ControlMaster session is live; proceed passwordless for everything below.
- **Fails** → the box needs an interactive login first (it's password-auth with no key, so a session/agent cannot type the password non-interactively). Ask the user to open one themselves, which establishes the 24h ControlPersist master, e.g. have them run this from the prompt with a leading `!`:

  ```
  ssh <ALIAS>
  ```

  Then confirm the master socket exists and retry Step 2:

  ```bash
  ls -la ~/.ssh/control_"$ALIAS" 2>/dev/null
  ```

## Step 3 — Do the operation

### connect
Print the reachability result from Step 2 and the ready command:
```bash
echo "ssh $ALIAS"
```

### run
```bash
ssh "$ALIAS" '<remote command>'
```

### push  (local → dev-box)
`scp` reuses the ssh ControlMaster and needs no remote rsync binary. Create the destination dir, copy, then verify.
```bash
DEST="${REMOTE_DEST:-~/}"                      # default home; use a subdir to stay organized
ssh "$ALIAS" "mkdir -p $DEST"
scp -r -q <local-path...> "$ALIAS:$DEST"
```
For **large** transfers, run the scp in the background (so it isn't killed by a foreground timeout), then verify on the remote:
```bash
ssh "$ALIAS" "ls -la $DEST; du -sh $DEST/<name>"
# and compare byte size against the local source when practical (stat -f%z on macOS, stat -c%s on Linux)
```

### pull  (dev-box → local; run this skill ON the laptop that should receive the files)
`scp` reuses the ssh ControlMaster and pulls from the box down to this machine — no remote rsync needed. Create the local destination, copy, then verify locally.
```bash
LOCAL_DEST="${LOCAL_DEST:-.}"
mkdir -p "$LOCAL_DEST"
scp -r -q "$ALIAS:<remote-path...>" "$LOCAL_DEST"
ls -la "$LOCAL_DEST"
```
For **large** pulls, run the scp in the background (so a foreground timeout can't kill it), then verify size/count and — when practical — a byte-match against the remote source. Note the `stat` flags differ by OS (remote dev-box is Linux, your laptop is likely macOS):
```bash
# remote (Linux) size of the source:
ssh "$ALIAS" "du -sb <remote-path>; stat -c%s <remote-file> 2>/dev/null"
# local size after the pull (macOS: stat -f%z ; Linux: stat -c%s):
du -sh "$LOCAL_DEST"/<name>; stat -f%z "$LOCAL_DEST"/<file> 2>/dev/null || stat -c%s "$LOCAL_DEST"/<file>
```
The byte sizes should match. (This is the mirror image of `push`; the only real difference is direction — `"$ALIAS:remote" local` instead of `local "$ALIAS:remote"`.)

> Optional: if the remote has `rsync` (`ssh "$ALIAS" 'command -v rsync'`), you may use `rsync -avP` instead for resumable transfers with progress. `scp` is the safe default because it always works over the ControlMaster with no remote dependency.

## Step 4 — Report

State the resolved alias, the remote host/user/path, and the verification result (sizes/counts, byte-match if checked). Keep the box-name-agnostic framing so it still reads correctly after the box is recreated.

---

## Troubleshooting
- **`ssh: Could not resolve hostname <bare-name>`** — you used the box's friendly name instead of the `pluto-prod-…` alias. Re-run Step 1.
- **Password prompt / `BatchMode` failure** — no live ControlMaster; have the user open an interactive `ssh <ALIAS>` first (Step 2), then retry.
- **`.ssh/id_ed25519: No such file or directory`** printed during commands — harmless shell-init noise from a profile trying to load a key that isn't there; ignore it, it does not affect ssh/scp over the Pluto proxy.
- **No aliases found** in Step 1 — the Pluto job/config isn't present; the box must be (re)created and connected through the user's Pluto CLI before this skill can talk to it.
- **Box restarted / new pod (same job), key rejected** — `Permission denied (publickey,keyboard-interactive)`.
  - The pod name changes (e.g. `...-de-0` -> `...-de-2-0` -> `...-de-2-0-<suffix>`), but the **routing alias stays the one in the job's "SSH config" field** (`...-de-0`). The proxy routes by the SNI `%h`, so do NOT add a Host entry for the new pod name (it gets "Connection closed by UNKNOWN port 65535"). Keep using the original alias.
  - Key auth: `PasswordAuthentication no` + an IAM-registered key (`~/.ssh/id_ed25519`, registered at iam.corp.adobe.com) is the Foundry policy. The pod loads IAM keys at start; a pod that missed the key rejects it forever. Confirm the pod isn't stale: `hostname` over ssh shows the live pod name.
  - Fix: replace the pod (`compute_replace_pods` via the aip MCP, needs explicit user OK; **wipes `/mnt/localssd` and memory**, so copy data off first, e.g. via "Open VS Code" web on the job page). Wait ~2-8 min (sshd log in `get_run_logs` shows "Running sshd"; the proxy may reset connections until routing registers), then `ssh <original-alias>`.
  - Fallback while broken: "Open VS Code" (web) on the job page needs no SSH.
  - After a replace, re-push any files you need (e.g. `/mnt/localssd/...`).

- **Job moved to another cluster / node group (e.g. ops paused it and changed `UpdateJobExecSpec`)** — job pod is RUNNING but ssh/VS Code gets `kex_exchange_identification: Connection closed` / `Connection closed by UNKNOWN port 65535`.
  - Check the job's `cluster_run_response` (aip `get_entities`): if `sshEnvironmentDomain` is set (e.g. `jobs.colligo.dev`), the old shared bastion (`ssh.od1.colligo.dev:22`) no longer routes. `sshIngressDomain` (`int.…`) is internal-only; don't use it.
  - Fix the generated config's ProxyCommand to the per-pod TLS ingress (what the current Pluto SDK emits): `openssl s_client -quiet -connect %h.ssh.jobs.colligo.dev:443 -servername %h.<pod-domain> 2>/dev/null`. Keep the same alias; `rm ~/.ssh/control_<alias>` to drop a stale ControlMaster.
  - A move to a new node = fresh `/mnt/localssd` (empty). Home dir survives via snapshot.
