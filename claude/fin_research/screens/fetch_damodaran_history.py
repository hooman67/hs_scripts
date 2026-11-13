#!/usr/bin/env python3
"""
fetch_damodaran_history.py — build a per-industry EV/EBITDA and P/B (+ROIC/ROE) HISTORY
from Aswath Damodaran's ARCHIVED yearly industry datasets, for US / Global / Emerging.

Why: the main data/damodaran/ pull is a single 2026-01-05 snapshot. To judge a sector's
cheapness "vs its OWN history" (a sector can be perennially low-multiple) we need multiple
years. Damodaran keeps archived yearly files under:
    https://pages.stern.nyu.edu/~adamodar/pc/archives/<stem><YY>.xls
VERIFIED reachable 2026-07-01 for YY in 15..24 (EV/EBITDA + P/B, all three regions) and
the current-year (2026-01-05) file lives at the live datasets/ URL.

Archive naming gotcha (VERIFIED): the file <stem><YY> is stamped "Date updated: 20(YY+1)-01-05".
So vebitda16 -> as_of 2017-01-05, vebitda24 -> as_of 2025-01-05. The current live file
(datasets/vebitda.xls) is as_of 2026-01-05. We label each row by its real as_of_date.

Older files (<=~2018) use sheet "Sheet1" and lack the metadata preamble region tag; newer
files use sheet "Industry Averages". We auto-detect both, and the header row.

Output (data/damodaran/history/):
  - damodaran_history_long.csv  : region, Industry Name, metric, value, as_of_date,
                                   data_year, source_url  (tidy long; one row per point)
  - <stem><YY>.xls              : raw archived files, exactly as fetched (audit trail)
  - damodaran_history_manifest.csv : per-file fetch log (url, http, as_of, n_industries)

Metrics captured: EV/EBITDA (from vebitda*), PBV, ROIC, ROE (from pbv*). PE (US only) is
also captured from pedata* as a bonus (Current PE, Trailing PE, Forward PE).

Usage:
    /opt/venv/bin/python3 screens/fetch_damodaran_history.py
    /opt/venv/bin/python3 screens/fetch_damodaran_history.py --no-download   # re-parse cache
"""
from __future__ import annotations
import argparse, os, sys
from datetime import datetime
import pandas as pd
import requests

ARCHIVE = "https://pages.stern.nyu.edu/~adamodar/pc/archives"
LIVE = "https://pages.stern.nyu.edu/~adamodar/pc/datasets"
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
OUT_DIR = os.path.join(PROJ, "data", "damodaran", "history")
HEADERS = {"User-Agent": "Hooman Shariati hshariati@adobe.com"}

# archive years to pull (file-stem year). VERIFIED 200 for 15..24 (2026-07-01).
ARCHIVE_YEARS = list(range(15, 25))  # 15..24 inclusive

# base -> (region -> stem). We pull EV/EBITDA and P/B for all 3 regions; PE for US only.
STEMS = {
    "vebitda": {"US": "vebitda", "Global": "vebitdaGlobal", "Emerging": "vebitdaemerg"},
    "pbv":     {"US": "pbvdata", "Global": "pbvGlobal",      "Emerging": "pbvemerg"},
    "pedata":  {"US": "pedata"},  # PE is US-only on Damodaran
}
# which columns we keep from each base (by header label; taken from newest layout, older files match)
KEEP = {
    "vebitda": ["EV/EBITDA"],
    "pbv":     ["PBV", "ROIC", "ROE"],
    "pedata":  ["Current PE", "Trailing PE", "Forward PE"],
}


def fetch(url: str, dest: str, no_download: bool) -> bool:
    if no_download:
        return os.path.exists(dest)
    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
    except Exception as e:
        print(f"  [FAIL] {url}: {e}")
        return False
    if r.status_code != 200 or len(r.content) < 5000:
        print(f"  [MISS] HTTP {r.status_code} {len(r.content)}B -> {url}")
        return False
    with open(dest, "wb") as f:
        f.write(r.content)
    return True


def parse(path: str) -> tuple[pd.DataFrame, str] | None:
    """Return (df with Industry Name + de-duped metric cols, as_of_iso) or None."""
    try:
        xl = pd.ExcelFile(path)
    except Exception as e:
        print(f"  [FAIL] open {os.path.basename(path)}: {e}")
        return None
    sheet = "Industry Averages" if "Industry Averages" in xl.sheet_names else xl.sheet_names[0]
    raw = xl.parse(sheet_name=sheet, header=None)
    # as-of
    as_of = ""
    for i in range(min(10, len(raw))):
        c0 = str(raw.iloc[i, 0]).strip().lower()
        if c0.startswith("date updated") or c0.startswith("updated"):
            try:
                as_of = pd.to_datetime(raw.iloc[i, 1]).date().isoformat()
            except Exception:
                as_of = str(raw.iloc[i, 1])
    # header row. Tolerate Damodaran's real typos in this cell across archive years:
    #   "Industry  Name" (double space), "Induistry Name" (misspelling).
    hrow = None
    for i in range(min(40, len(raw))):
        c0 = " ".join(str(raw.iloc[i, 0]).strip().lower().split())  # collapse whitespace
        if c0.startswith("industry name") or c0.startswith("induistry name"):
            hrow = i
            break
    if hrow is None:
        print(f"  [FAIL] {os.path.basename(path)}: no header row")
        return None
    header = [str(x).strip() for x in raw.iloc[hrow].tolist()]
    # normalize the industry-name column label (archives have typos: "Industry  Name",
    # "Induistry Name") to the canonical "Industry Name".
    if header:
        h0 = " ".join(header[0].lower().split())
        if h0.startswith("industry name") or h0.startswith("induistry name"):
            header[0] = "Industry Name"
    seen: dict[str, int] = {}
    dedup: list[str] = []
    for h in header:
        if h in seen:
            seen[h] += 1
            dedup.append(f"{h}.{seen[h]}")
        else:
            seen[h] = 0
            dedup.append(h)
    data = raw.iloc[hrow + 1:].copy()
    data.columns = dedup
    data = data[data["Industry Name"].notna()]
    data = data[~data["Industry Name"].astype(str).str.strip().isin(["", "nan"])]
    for c in data.columns:
        if c != "Industry Name":
            data[c] = pd.to_numeric(data[c], errors="coerce")
    return data.reset_index(drop=True), as_of


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-download", action="store_true")
    args = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"Damodaran HISTORY fetch — {datetime.now().isoformat(timespec='seconds')}")
    rows: list[dict] = []
    manifest: list[dict] = []

    # jobs: (base, region, stem, year_label, url, local)
    jobs = []
    for base, regionmap in STEMS.items():
        for region, stem in regionmap.items():
            # archived years
            for yy in ARCHIVE_YEARS:
                jobs.append((base, region, stem, 2000 + yy,
                             f"{ARCHIVE}/{stem}{yy}.xls",
                             os.path.join(OUT_DIR, f"{stem}{yy}.xls")))
            # current live file (data year 2025, as_of 2026-01-05)
            jobs.append((base, region, stem, 2025,
                         f"{LIVE}/{stem}.xls",
                         os.path.join(OUT_DIR, f"{stem}_live.xls")))

    for base, region, stem, data_year, url, local in jobs:
        ok = fetch(url, local, args.no_download)
        if not ok:
            manifest.append({"base": base, "region": region, "stem": stem,
                             "data_year": data_year, "url": url, "status": "MISSING"})
            continue
        parsed = parse(local)
        if parsed is None:
            manifest.append({"base": base, "region": region, "stem": stem,
                             "data_year": data_year, "url": url, "status": "PARSE_FAIL"})
            continue
        df, as_of = parsed
        keep_cols = [c for c in KEEP[base] if c in df.columns]
        got = df[["Industry Name"] + keep_cols].copy()
        for _, r in got.iterrows():
            ind = str(r["Industry Name"]).strip()
            for m in keep_cols:
                v = r[m]
                if pd.notna(v):
                    rows.append({"region": region, "Industry Name": ind, "metric": m,
                                 "value": float(v), "as_of_date": as_of,
                                 "data_year": data_year, "source_url": url})
        manifest.append({"base": base, "region": region, "stem": stem,
                         "data_year": data_year, "url": url, "status": "OK",
                         "as_of": as_of, "n_industries": len(got)})
        print(f"  [OK] {stem:16s} {region:9s} dy={data_year} as_of={as_of or '?':10s} n={len(got)}")

    if not rows:
        print("No rows parsed."); return 1
    long = pd.DataFrame(rows)
    long_path = os.path.join(OUT_DIR, "damodaran_history_long.csv")
    long.to_csv(long_path, index=False)
    pd.DataFrame(manifest).to_csv(os.path.join(OUT_DIR, "damodaran_history_manifest.csv"), index=False)
    print(f"\nWrote {long_path}  ({len(long):,} rows)")
    print(f"Years: {sorted(long['data_year'].unique())}")
    print(f"Regions: {sorted(long['region'].unique())}  Metrics: {sorted(long['metric'].unique())}")
    ok = sum(1 for m in manifest if m['status'] == 'OK')
    print(f"Files OK: {ok}/{len(manifest)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
