#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml", "beautifulsoup4", "lxml"]
# ///
"""Recommend Pluto jobs that violate the node-allocation canvas — READ ONLY.

Never stops anything. Cross-references currently-running Pluto jobs against the
"Weekly Thu->Thu node request and allocation" canvas and prints ranked kill
*candidates*:

  1. REJECTED-canvas work running anyway  (hardest violation)
  2. Dev boxes using > 2 GPUs            (dev-box rule)
  3. Demos not declared on the canvas
  + how much each frees, and which queued jobs that would unblock.

Pluto data comes from the foundry-pluto MCP (agent-fetched). Usage:

  uv run --script find_node_violation.py --jobs-file <list_jobs active json>
      [--canvas-id Fxxxx] [--names]   # --names resolves Slack requester ids

Output is advisory only — hand the recommendations to the user to act on.
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
DEFAULT_CANVAS = "F0BCU4W3KU6"
GPN = 8
STOP = set("training model models data the for and over run break cluster please use foundry "
           "node nodes gpu gpus on of to a in with new full job test improvement generation "
           "fine tuned tuning ready need readout "
           # generic vendor/role/infra tokens that cause cross-team false matches
           "runway media intelligence agent backend instance inference smoke eval bench "
           "image images video setup pipeline".split())


def creds():
    return yaml.safe_load(open(CREDS))


def unwrap(o):
    return json.loads(o["result"]) if isinstance(o, dict) and isinstance(o.get("result"), str) else o


def keywords(text: str) -> set[str]:
    toks = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {t for t in toks if len(t) >= 4 and t not in STOP}


# --------------------------------------------------------------------------- #
# Canvas
# --------------------------------------------------------------------------- #

def canvas_rows(token: str, cid: str) -> list[dict]:
    H = {"Authorization": f"Bearer {token}"}
    info = requests.get("https://slack.com/api/files.info", headers=H, params={"file": cid}).json()
    if not info.get("ok"):
        sys.exit(f"canvas files.info failed: {info.get('error')}")
    url = info["file"].get("url_private_download") or info["file"]["url_private"]
    soup = BeautifulSoup(requests.get(url, headers=H).text, "lxml")
    table = soup.find("table")
    rows = []
    for tr in table.find_all("tr")[1:]:
        c = tr.find_all(["td", "th"])
        if len(c) < 2:
            continue
        ncell = c[1]
        struck = {s.get_text(" ", strip=True) for s in ncell.find_all(["s", "del", "strike"])}
        for el in ncell.find_all(style=True):
            if "line-through" in (el.get("style") or ""):
                struck.add(el.get_text(" ", strip=True))
        full = ncell.get_text(" ", strip=True)
        cleaned = full
        for s in struck:
            cleaned = cleaned.replace(s, " ", 1)
        nodes = sum(int(n) for n in re.findall(r"(\d+)\s*(?:H200|B200)\b", cleaned, re.I))
        desc = c[3].get_text(" ", strip=True) if len(c) > 3 else ""
        status = c[-1].get_text(" ", strip=True)
        req = c[0].get_text(" ", strip=True)
        rows.append({
            "requester": req, "nodes": nodes, "desc": desc,
            "gpu": "B200" if re.search(r"b200", cleaned, re.I) else "H200",
            "approved": ("greencheck" in status.lower() or "✅" in status),
            "is_demo": "demo" in desc.lower(),
        })
    return rows


def resolve(token, handle_ids):
    H = {"Authorization": f"Bearer {token}"}
    out = {}
    for uid in handle_ids:
        r = requests.get("https://slack.com/api/users.info", headers=H, params={"user": uid}).json()
        out[uid] = r["user"]["real_name"] if r.get("ok") else uid
    return out


# --------------------------------------------------------------------------- #
# Jobs
# --------------------------------------------------------------------------- #

def gp(j):
    return (j.get("num_nodes") or 0) * (j.get("gpus_per_node") or 0)


def analyze(jobs, rows):
    running = [j for j in jobs if j.get("status") == "Running"]
    queued = [j for j in jobs if j.get("status") == "Queued"]

    rejected = [r for r in rows if not r["approved"]]
    approved = [r for r in rows if r["approved"]]
    rej_kw = {}
    for r in rejected:
        for k in keywords(r["desc"]):
            rej_kw.setdefault(k, r)
    appr_kw = set().union(*(keywords(r["desc"]) for r in approved)) if approved else set()
    demo_kw = set().union(*(keywords(r["desc"]) for r in rows if r["is_demo"])) if any(r["is_demo"] for r in rows) else set()

    def name_kw(j):
        # Match on the job NAME only. Matching project_name made every job in a
        # project hit that project's canvas rows (e.g. any Media-Intelligence job
        # matched the rejected "MI Ingestion" row) — too many false positives.
        return keywords(j.get("name", ""))

    rejected_running, dev_over, demos_off = [], [], []
    for j in running:
        nm = (j.get("name") or "")
        nk = name_kw(j)
        hit = nk & set(rej_kw)
        if hit and not (nk & appr_kw):
            row = rej_kw[sorted(hit)[0]]
            rejected_running.append((j, row, sorted(hit)))
        if re.search(r"dev", nm, re.I) and gp(j) > 2:
            dev_over.append(j)
        if re.search(r"demo", nm, re.I) and not (nk & demo_kw):
            demos_off.append(j)

    qd = {}
    for j in queued:
        if gp(j):
            qd[j.get("gpu_type")] = qd.get(j.get("gpu_type"), 0) + gp(j)
    return rejected_running, dev_over, demos_off, queued, qd


def fmt(j):
    return (f"{j.get('name','')[:46]:46} | {j.get('project_name','')[:22]:22} | "
            f"{str(j.get('owner')):24} | {j.get('num_nodes')}x{j.get('gpus_per_node')} {j.get('gpu_type')}"
            f" = {gp(j)}GPU/{gp(j)//GPN}nd | {j.get('pluto_url')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs-file", required=True)
    ap.add_argument("--canvas-id", default=DEFAULT_CANVAS)
    ap.add_argument("--names", action="store_true", help="resolve Slack requester names (extra API calls)")
    args = ap.parse_args()

    c = creds()
    jobs = unwrap(json.load(open(args.jobs_file)))
    rows = canvas_rows(c["slack"]["user_token"], args.canvas_id)
    rej_run, dev_over, demos_off, queued, qd = analyze(jobs, rows)

    print("=== KILL CANDIDATES (advisory — nothing is stopped) ===\n")
    print(f"1) RUNNING work that the canvas REJECTED  ({len(rej_run)} job(s)):")
    for j, row, hit in sorted(rej_run, key=lambda x: -gp(x[0])):
        print("   " + fmt(j))
        print(f"        ↳ matches rejected row: \"{row['desc'][:60]}\" (req {row['requester']}) via {hit}")
    print(f"\n2) DEV boxes over the 2-GPU limit  ({len(dev_over)} job(s)):")
    for j in sorted(dev_over, key=lambda x: -gp(x)):
        print("   " + fmt(j))
    print(f"\n3) DEMOS not on the canvas  ({len(demos_off)} job(s)):")
    for j in sorted(demos_off, key=lambda x: -gp(x)):
        print("   " + fmt(j))

    print("\n=== QUEUED demand (what killing would unblock) ===")
    if qd:
        for t, g in qd.items():
            print(f"   {t}: {g} GPU ({g//GPN} nodes) waiting")
        for j in queued:
            if gp(j):
                print("   waiting: " + fmt(j))
    else:
        print("   (no GPU jobs queued)")

    # headline recommendation
    rejH = sum(gp(j) for j, _, _ in rej_run if j.get("gpu_type") == "H200")
    if rej_run:
        print(f"\n>>> Recommendation: the {len(rej_run)} rejected-canvas job(s) free ~{rejH//GPN} H200 nodes; "
              "kill those first (clearest violation), prioritising any whose size matches the queued demand above.")
    print("\n(advisory only — no jobs were stopped)")


if __name__ == "__main__":
    raise SystemExit(main())
