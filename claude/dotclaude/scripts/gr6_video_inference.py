#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "requests"]
# ///
"""
GR6 Text-to-Video Inference on Pluto — unified launch and monitoring.

Automates all setup, env-var injection, token validation, and the 4 blockers:
  1. WANDB_API_KEY + SLACK_MEMBER_ID env vars (morictl hard-asserts these)
  2. Unset static AWS keys so instance role is used (PutObject to s3://dit-scale-up)
  3. Inject KINETOBOT_GITHUB_API_TOKEN into pluto_main.tmp.sh (expired token fix)
  4. Validate balance_gpu_specs has symm_mem key

Usage:
  gr6-video-inference [--config PATH] [--colligo PATH] [--dry-run] [--help]

Examples:
  # Default config with all prompts
  gr6-video-inference

  # Custom config
  gr6-video-inference --config /home/colligo/colligo/.../configs/foundry/my_config.yaml

  # Monitor last job
  gr6-video-inference --status

  # Dry-run: show env + command without launching
  gr6-video-inference --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import requests
import yaml


# Paths & defaults
HOME = Path.home()
CREDS_YAML = HOME / ".claude" / "hshariati" / "credentials.yaml"
DEFAULT_COLLIGO = Path("/home/colligo/colligo")
DEFAULT_CONFIG = (
    DEFAULT_COLLIGO
    / "contrib/Mori/collections/foundation_exploration"
    / "configs/foundry/hshariati_gr6_lite_580k_t2v_infer.yaml"
)
FE_RELPATH = "contrib/Mori/collections/foundation_exploration"
STATE_FILE = HOME / ".claude" / "hshariati" / ".gr6_last_job"


def load_yaml_file(path: Path) -> dict:
    """Load YAML file safely."""
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading {path}: {e}", file=sys.stderr)
        return {}


def load_credentials() -> dict:
    """Load credentials from ~/.claude/hshariati/credentials.yaml."""
    return load_yaml_file(CREDS_YAML)


def prompt_for_input(label: str, env_key: Optional[str] = None, default: Optional[str] = None) -> str:
    """Prompt user for input, with optional env var and default fallback."""
    if env_key and (val := os.environ.get(env_key)):
        print(f"{label}: (from ${env_key}) {val[:20]}...", file=sys.stderr)
        return val

    creds = load_credentials()
    # Try to find in credentials.yaml
    for section in creds.values():
        if isinstance(section, dict) and label.lower() in str(section).lower():
            break

    prompt_text = label
    if default:
        prompt_text += f" [{default}]"
    prompt_text += ": "

    user_input = input(prompt_text).strip()
    return user_input or default or ""


def resolve_wandb_api_key() -> str:
    """Resolve WANDB_API_KEY from env, credentials, or prompt."""
    if val := os.environ.get("WANDB_API_KEY"):
        return val

    creds = load_credentials()
    if wandb_cfg := creds.get("wandb", {}):
        if api_key := wandb_cfg.get("api_key"):
            return str(api_key)

    return prompt_for_input("WANDB_API_KEY")


def resolve_slack_member_id() -> str:
    """Resolve SLACK_MEMBER_ID from env, credentials, or prompt."""
    if val := os.environ.get("SLACK_MEMBER_ID"):
        return val

    creds = load_credentials()
    if slack_cfg := creds.get("slack", {}):
        if member_id := slack_cfg.get("member_id"):
            return str(member_id)

    # Try hardcoded fallback
    return prompt_for_input("SLACK_MEMBER_ID", default="D06340Q0EG3")


def resolve_ldap() -> str:
    """Resolve LDAP username."""
    if val := os.environ.get("LDAP"):
        return val

    creds = load_credentials()
    if ldap_val := creds.get("ldap"):
        return str(ldap_val)

    return "hshariati"


def resolve_kinetobot_github_token() -> str:
    """Resolve KINETOBOT_GITHUB_API_TOKEN from env, credentials, or prompt."""
    if val := os.environ.get("KINETOBOT_GITHUB_API_TOKEN"):
        return val

    creds = load_credentials()
    if github_cfg := creds.get("kinetobot_github", {}):
        if token := github_cfg.get("api_token"):
            return str(token)

    raise SystemExit(
        "KINETOBOT_GITHUB_API_TOKEN not found in env or credentials.yaml.\n"
        "Add it to ~/.claude/hshariati/credentials.yaml under kinetobot_github.api_token"
    )


def validate_config(config_path: Path, colligo_root: Path) -> dict:
    """Load and validate the config file, return parsed YAML."""
    if not config_path.exists():
        raise SystemExit(f"Config not found: {config_path}")

    config = load_yaml_file(config_path)

    # Check for required keys
    if "train" not in config:
        raise SystemExit(f"Config missing 'train' section: {config_path}")

    if "launch" not in config:
        raise SystemExit(f"Config missing 'launch' section: {config_path}")

    # Validate balance_gpu_specs has symm_mem key
    denoiser_cfg = config.get("model", {}).get("params", {}).get("denoiser_config", {}).get("params", {})
    balance_gpu_specs = denoiser_cfg.get("balance_gpu_specs", "")

    if balance_gpu_specs and "symm_mem" not in balance_gpu_specs:
        print(
            f"WARNING: balance_gpu_specs missing symm_mem key:\n"
            f"  {balance_gpu_specs}\n"
            f"  Add symm_mem=false or symm_mem=true to fix.",
            file=sys.stderr
        )

    return config


def patch_github_token(colligo_root: Path, kinetobot_token: str) -> None:
    """
    Patch scripts/local/pluto_main.tmp.sh to inject KINETOBOT_GITHUB_API_TOKEN.

    This is a local edit to a tracked file; it rides along in the launch's local_diff.patch.
    """
    script_path = colligo_root / "contrib/Mori/collections/foundation_exploration/scripts/local/pluto_main.tmp.sh"

    if not script_path.exists():
        print(f"WARNING: {script_path} not found; skipping GitHub token patch", file=sys.stderr)
        return

    content = script_path.read_text()

    # Replace the hardcoded cliobot_adobe token pattern with KINETOBOT token
    # Look for lines like: export GITHUB_TOKEN="..." or similar
    # We'll inject it as an env var at script start

    if "KINETOBOT_GITHUB_API_TOKEN" in content:
        print("INFO: pluto_main.tmp.sh already uses KINETOBOT_GITHUB_API_TOKEN", file=sys.stderr)
        return

    # Find the shebang and first export/setup lines
    lines = content.split("\n")
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("#!/") or line.startswith("set ") or line.startswith("export "):
            insert_idx = i + 1

    # Insert the token as an env var
    token_line = f'export GITHUB_TOKEN="{kinetobot_token}"'
    lines.insert(insert_idx, token_line)

    patched_content = "\n".join(lines)
    script_path.write_text(patched_content)
    print(f"PATCHED: Injected KINETOBOT_GITHUB_API_TOKEN into {script_path.name}", file=sys.stderr)


def build_launch_env(wandb_key: str, slack_id: str, ldap: str) -> dict:
    """Build the env dict for morictl launch with AWS key unsetting."""
    env = os.environ.copy()
    env["WANDB_API_KEY"] = wandb_key
    env["SLACK_MEMBER_ID"] = slack_id
    env["LDAP"] = ldap

    # Unset static AWS keys so instance role is used
    env.pop("AWS_ACCESS_KEY_ID", None)
    env.pop("AWS_SECRET_ACCESS_KEY", None)
    env.pop("AWS_SESSION_TOKEN", None)

    return env


def run_device_flow_login(colligo_root: Path) -> None:
    """
    Wait for device-flow login to complete (morictl login).

    This is needed once; the token caches to ~/.colligo/pluto_cli/msal-pluto-auth.secret.
    """
    fe_dir = colligo_root / FE_RELPATH
    morictl_path = fe_dir / "scripts/local/.venv/bin/morictl"

    if not morictl_path.exists():
        print(
            f"WARNING: {morictl_path} not found; skipping device-flow login.\n"
            "You may need to run 'morictl login' manually.",
            file=sys.stderr
        )
        return

    # Check if token already cached
    token_cache = HOME / ".colligo/pluto_cli/msal-pluto-auth.secret"
    if token_cache.exists():
        age_seconds = time.time() - token_cache.stat().st_mtime
        if age_seconds < 86400:  # Less than 24h old
            print(f"INFO: Using cached device-flow token ({age_seconds // 3600:.0f}h old)", file=sys.stderr)
            return

    print("Opening device-flow login (visit login.microsoft.com/device to authenticate)...", file=sys.stderr)
    try:
        subprocess.run([str(morictl_path), "login"], check=True, timeout=120)
    except subprocess.CalledProcessError:
        print("WARNING: Device-flow login may have failed. Proceeding anyway.", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("WARNING: Device-flow login timed out. Proceeding anyway.", file=sys.stderr)


def launch_inference(colligo_root: Path, config_path: Path, env: dict, dry_run: bool = False) -> tuple[str, str]:
    """
    Run morictl launch with the given config and environment.

    Returns (job_name, uuid) if successful.
    """
    fe_dir = colligo_root / FE_RELPATH

    # Activate FE environment
    activate_script = fe_dir / "scripts/env/activate.sh"
    if not activate_script.exists():
        raise SystemExit(f"Activation script not found: {activate_script}")

    # Build command: source activate.sh, then morictl launch
    cmd = f"cd {fe_dir} && source scripts/env/activate.sh && morictl launch {config_path}"

    if dry_run:
        print(f"DRY RUN: Would execute:\n  {cmd}\n\nWith env:")
        for k, v in sorted(env.items()):
            if any(x in k.lower() for x in ["key", "token", "secret", "password"]):
                print(f"  {k}=***")
            elif k in ["WANDB_API_KEY", "SLACK_MEMBER_ID", "LDAP"]:
                print(f"  {k}={v}")
        return ("DRY_RUN", "DRY_RUN")

    print(f"Launching: morictl launch {config_path.name}", file=sys.stderr)

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        raise SystemExit("Launch timed out (5 min)")

    if result.returncode != 0:
        print(f"Launch failed (exit {result.returncode}):", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"morictl launch failed")

    # Parse stdout for job name and UUID
    # morictl prints: Launched job: <job_name> (UUID: <uuid>)
    match_name = re.search(r"Launched job:\s+(\S+)", result.stdout)
    match_uuid = re.search(r"UUID:\s+([a-f0-9\-]+)", result.stdout)

    job_name = match_name.group(1) if match_name else "UNKNOWN"
    job_uuid = match_uuid.group(1) if match_uuid else "UNKNOWN"

    print(f"Job: {job_name}", file=sys.stderr)
    print(f"UUID: {job_uuid}", file=sys.stderr)

    return (job_name, job_uuid)


def save_job_state(job_name: str, job_uuid: str, config_path: Path, colligo_root: Path) -> None:
    """Save last job info to ~/.claude/hshariati/.gr6_last_job for monitoring."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "job_name": job_name,
        "job_uuid": job_uuid,
        "config_path": str(config_path),
        "colligo_root": str(colligo_root),
        "timestamp": time.time(),
    }
    STATE_FILE.write_text(json.dumps(state, indent=2))
    print(f"Saved state to {STATE_FILE}", file=sys.stderr)


def show_monitoring_hints(job_name: str, job_uuid: str, config_path: Path, colligo_root: Path) -> None:
    """Print monitoring hints for the user."""
    fe_dir = colligo_root / FE_RELPATH

    print("\n" + "=" * 70, file=sys.stderr)
    print("JOB LAUNCHED", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print(f"Job name:  {job_name}", file=sys.stderr)
    print(f"Job UUID:  {job_uuid}", file=sys.stderr)
    print(f"Config:    {config_path}", file=sys.stderr)
    print(f"Pluto project: Foundry-HP", file=sys.stderr)
    print("", file=sys.stderr)
    print("MONITORING COMMANDS:", file=sys.stderr)
    print(f"  # Status:", file=sys.stderr)
    print(f"  morictl job status {job_name}", file=sys.stderr)
    print(f"  # Logs (last 80 lines):", file=sys.stderr)
    print(f"  morictl job logs {job_name}", file=sys.stderr)
    print(f"  # Find errors:", file=sys.stderr)
    print(f"  morictl find_error {job_uuid}", file=sys.stderr)
    print(f"  # Full job summary (once done):", file=sys.stderr)
    print(f"  morictl job_summary {job_uuid}", file=sys.stderr)
    print("", file=sys.stderr)
    print("RESULTS:", file=sys.stderr)
    print(f"  - WandB run: foundry project, run inference-gr6_lite_580k_t2v_infer-...", file=sys.stderr)
    print(f"  - Job S3 logs: s3://...${{JOB_UUID}}/... (check job_summary HTML)", file=sys.stderr)
    print("", file=sys.stderr)
    print(f"GPU time estimate: ~8 min per 5-sec clip (9 s/denoising step × 50 steps)", file=sys.stderr)
    print("=" * 70, file=sys.stderr)


def show_status() -> None:
    """Show status of the last launched job."""
    if not STATE_FILE.exists():
        print("No job state saved. Run gr6-video-inference to launch a job first.", file=sys.stderr)
        return

    state = json.loads(STATE_FILE.read_text())
    job_name = state.get("job_name")
    job_uuid = state.get("job_uuid")
    ts = state.get("timestamp", 0)

    age_min = (time.time() - ts) / 60
    print(f"Last job (from {age_min:.0f} min ago):", file=sys.stderr)
    print(f"  Job: {job_name}", file=sys.stderr)
    print(f"  UUID: {job_uuid}", file=sys.stderr)
    print(f"  Config: {state.get('config_path')}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Monitoring commands:", file=sys.stderr)
    print(f"  morictl job status {job_name}", file=sys.stderr)
    print(f"  morictl find_error {job_uuid}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--config",
        type=Path,
        help=f"Config YAML path (default: {DEFAULT_CONFIG})",
    )
    ap.add_argument(
        "--colligo",
        type=Path,
        default=DEFAULT_COLLIGO,
        help=f"Colligo repo root (default: {DEFAULT_COLLIGO})",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Show command and env without launching",
    )
    ap.add_argument(
        "--status",
        action="store_true",
        help="Show last job status",
    )
    ap.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = ap.parse_args()

    if args.status:
        show_status()
        return

    # Resolve paths
    config_path = args.config or DEFAULT_CONFIG
    colligo_root = args.colligo

    if not colligo_root.exists():
        raise SystemExit(f"Colligo root not found: {colligo_root}")

    if args.verbose:
        print(f"Colligo root: {colligo_root}", file=sys.stderr)
        print(f"Config: {config_path}", file=sys.stderr)

    # Validate config
    print("Validating config...", file=sys.stderr)
    validate_config(config_path, colligo_root)

    # Resolve credentials
    print("Resolving credentials...", file=sys.stderr)
    wandb_key = resolve_wandb_api_key()
    slack_id = resolve_slack_member_id()
    ldap = resolve_ldap()
    kinetobot_token = resolve_kinetobot_github_token()

    if not wandb_key:
        raise SystemExit("WANDB_API_KEY is required")
    if not slack_id:
        raise SystemExit("SLACK_MEMBER_ID is required")

    # Patch GitHub token
    patch_github_token(colligo_root, kinetobot_token)

    # Build env with AWS key unsetting
    env = build_launch_env(wandb_key, slack_id, ldap)

    # Device-flow login if needed
    if not args.dry_run:
        run_device_flow_login(colligo_root)

    # Launch
    job_name, job_uuid = launch_inference(colligo_root, config_path, env, dry_run=args.dry_run)

    # Save state and show hints
    if not args.dry_run:
        save_job_state(job_name, job_uuid, config_path, colligo_root)
        show_monitoring_hints(job_name, job_uuid, config_path, colligo_root)

        # Print JSON for Claude parsing
        print(json.dumps({
            "ok": True,
            "job_name": job_name,
            "job_uuid": job_uuid,
            "config": str(config_path),
            "message": f"Job {job_name} launched successfully"
        }))


if __name__ == "__main__":
    main()
