#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml", "beautifulsoup4", "lxml"]
# ///
"""Compute the Foundry node-allocation table and DM it on Slack.

Combines three sources:
  1. The "Weekly Thu->Thu node request and allocation" Slack canvas — approved
     (green check) vs not-approved nodes, split H200 / B200.
  2. Pluto get_quota  -> total fleet capacity per instance type.
  3. Pluto list_jobs  -> nodes currently running per GPU type.

Pluto data comes from the foundry-pluto MCP (which only the agent can call), so
the agent saves those two JSON blobs to files and passes them in:

  uv run --script allocation_check.py \
    --quota-file /path/to/quota.json \
    --jobs-file  /path/to/jobs.json     # the file list_jobs auto-saved

Add --dry-run to print the table without DMing.
Override the canvas with --canvas-id <Fxxxx> if the weekly doc ever changes.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

CREDS = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
DEFAULT_CANVAS = "F0BCU4W3KU6"  # Weekly Thu->Thu node request and allocation
GPUS_PER_NODE = 8
# instance_type -> GPU label we report
INSTANCE_GPU = {"p5en.48xlarge": "H200", "p6-b200.48xlarge": "B200"}


def load_creds():
    return yaml.safe_load(open(CREDS))


def _unwrap(obj):
    """MCP tool results are {"result": "<json string>"}; unwrap to the parsed value."""
    if isinstance(obj, dict) and "result" in obj and isinstance(obj["result"], str):
        return json.loads(obj["result"])
    return obj


# --------------------------------------------------------------------------- #
# 1. Canvas: approved / not-approved nodes by GPU type
# --------------------------------------------------------------------------- #

def parse_canvas(token: str, canvas_id: str) -> dict:
    H = {"Authorization": f"Bearer {token}"}
    info = requests.get("https://slack.com/api/files.info", headers=H, params={"file": canvas_id}).json()
    if not info.get("ok"):
        sys.exit(f"canvas files.info failed: {info.get('error')} (need slack.user_token with access)")
    url = info["file"].get("url_private_download") or info["file"]["url_private"]
    html = requests.get(url, headers=H).text
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        sys.exit("no table found in canvas")

    approved = {"H200": 0, "B200": 0}
    not_approved = {"H200": 0, "B200": 0}
    for row in table.find_all("tr")[1:]:  # skip header
        cells = row.find_all(["td", "th"])
        if len(cells) < 2:
            continue
        node_cell = cells[1]
        struck = {s.get_text(" ", strip=True) for s in node_cell.find_all(["s", "del", "strike"])}
        for el in node_cell.find_all(True):
            if "line-through" in (el.get("style") or ""):
                struck.add(el.get_text(" ", strip=True))
        full = node_cell.get_text(" ", strip=True)
        # drop struck substrings, then take the first integer = current node count
        cleaned = full
        for s in struck:
            cleaned = cleaned.replace(s, " ", 1)
        counts = re.findall(r"(\d+)\s*(?:H200|B200)\b", cleaned, re.I)
        if not counts:
            continue
        nodes = sum(int(n) for n in counts)
        gpu = "B200" if re.search(r"b200", cleaned, re.I) else "H200"
        status = cells[-1].get_text(" ", strip=True).lower()
        if "greencheck" in status or "✅" in status:
            approved[gpu] += nodes
        else:  # red, other emoji, or blank => not approved
            not_approved[gpu] += nodes
    return {"approved": approved, "not_approved": not_approved}


# --------------------------------------------------------------------------- #
# 2 + 3. Pluto capacity + running
# --------------------------------------------------------------------------- #

def parse_capacity(quota) -> dict:
    """Total fleet nodes per GPU type, from the central capacity pool."""
    quota = _unwrap(quota)
    cap = {"H200": 0, "B200": 0}
    for proj in quota:
        # the unallocated fleet lives in the 'DO NOT USE' pool with total_xpus set
        for e in proj.get("entries", []):
            label = INSTANCE_GPU.get(e.get("instance_type"))
            if label and e.get("total_xpus"):
                cap[label] += e["total_xpus"] // GPUS_PER_NODE
    return cap


def parse_running(quota) -> dict:
    """Nodes actually consuming the reserved fleet, from quota used_xpus.

    Authoritative — the per-project used_xpus is what's charged against the
    Foundry reserved capacity. (Summing list_jobs instead double-counts jobs on
    other pools/clusters and can exceed the fleet — that was the old bug.)
    """
    quota = _unwrap(quota)
    gpus = {"H200": 0, "B200": 0}
    for proj in quota:
        for e in proj.get("entries", []):
            label = INSTANCE_GPU.get(e.get("instance_type"))
            if label:
                gpus[label] += e.get("used_xpus", 0) or 0
    return {k: round(v / GPUS_PER_NODE) for k, v in gpus.items()}


# --------------------------------------------------------------------------- #
# Build + post
# --------------------------------------------------------------------------- #

def build_message(cap, canvas, running) -> str:
    appr, na = canvas["approved"], canvas["not_approved"]
    rows = []
    for t in ("H200", "B200"):
        rows.append((t, cap[t], appr[t], na[t], running[t]))
    tot = ("Total", sum(cap.values()), sum(appr.values()), sum(na.values()), sum(running.values()))
    rows.append(tot)

    hdr = f"{'GPU type':<9}{'Available(fleet)':>18}{'Approved ✅':>14}{'Not approved ❌':>17}{'Running now':>13}"
    lines = [hdr]
    for name, a, ap, n, r in rows:
        lines.append(f"{name:<9}{a:>18}{ap:>14}{n:>17}{r:>13}")
    table = "\n".join(lines)

    notes = []
    for t in ("H200", "B200"):
        free = cap[t] - running[t]
        if free <= 0:
            notes.append(f"{t}: running ({running[t]}) ≥ fleet ({cap[t]}) → no free {t} (overcommitted).")
        else:
            notes.append(f"{t}: {free} nodes free ({cap[t]} fleet − {running[t]} running).")
    return (
        "*Foundry node allocation — by GPU type (nodes)*\n"
        f"```\n{table}\n```\n" + " ".join(notes)
    )


def post_dm(creds, message: str):
    token = creds["slack"].get("user_token") or creds["slack"]["token"]
    H = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}
    channel = creds["slack"].get("dm_channel")
    if not channel:
        uid = creds["slack"]["user_id"]
        dm = requests.post("https://slack.com/api/conversations.open", headers=H, json={"users": uid}).json()
        if not dm.get("ok"):
            sys.exit(f"conversations.open failed: {dm.get('error')}")
        channel = dm["channel"]["id"]
    r = requests.post("https://slack.com/api/chat.postMessage", headers=H,
                      json={"channel": channel, "text": message}).json()
    if not r.get("ok"):
        sys.exit(f"chat.postMessage failed: {r.get('error')}")
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quota-file", required=True, help="JSON saved from foundry-pluto get_quota")
    ap.add_argument("--jobs-file", default=None, help="(unused; kept for compatibility)")
    ap.add_argument("--canvas-id", default=DEFAULT_CANVAS)
    ap.add_argument("--dry-run", action="store_true", help="print only, don't DM")
    args = ap.parse_args()

    creds = load_creds()
    quota = json.load(open(args.quota_file))

    canvas = parse_canvas(creds["slack"]["user_token"], args.canvas_id)
    cap = parse_capacity(quota)
    running = parse_running(quota)
    msg = build_message(cap, canvas, running)

    print(msg)
    if not args.dry_run:
        post_dm(creds, msg)
        print("\n[DM sent]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
