#!/usr/bin/env python3
"""
fetch_damodaran.py — download NYU / Aswath Damodaran industry datasets.

The single best FREE source for top-down, industry-level valuation AND quality:
sector multiples (PE / forward PE / EV-EBITDA / P/B), margins, ROE and ROIC (ROC),
by geography. Updated ~yearly (usually early January). VERIFIED reachable 2026-07-01.

What it does
------------
1. Downloads the key .xls datasets (US + Global + Emerging-Market variants where they
   exist) from https://pages.stern.nyu.edu/~adamodar/pc/datasets/ into data/damodaran/.
2. Parses each ("Industry Averages" sheet — the header row is auto-detected because the
   files carry a variable-length metadata preamble at the top).
3. Extracts the "Date updated:" as-of date and the region tag from each file.
4. Writes:
     - data/damodaran/<name>.xls              (raw, exactly as fetched)
     - data/damodaran/damodaran_combined.csv  (tidy long form: one row per
       region x industry x metric, with source_file / source_url / as_of_date)
     - data/damodaran/damodaran_wide_<region>.csv  (convenience wide tables per region)
   and prints the source URL + as-of date for every file.

Usage
-----
    /opt/venv/bin/python3 data/fetch_damodaran.py            # fetch + parse everything
    /opt/venv/bin/python3 data/fetch_damodaran.py --no-download   # re-parse cached .xls

Coverage note (see data/README.md for the full honest write-up): Damodaran publishes PE
data for the US only under `pedata.xls` — there is NO `pedataGlobal`/`pedataemerg`. But
EV/EBITDA, P/B, margins, ROE and EVA(ROIC) DO have Global + Emerging variants, so
cross-region cheapness/quality is available on every metric EXCEPT the PE table (which is
US-only). This is a real limitation, documented, not worked around.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime

import pandas as pd
import requests

BASE = "https://pages.stern.nyu.edu/~adamodar/pc/datasets"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "damodaran")
HEADERS = {"User-Agent": "Hooman Shariati hshariati@adobe.com"}

# Each entry: file-stem -> (human topic, which columns we care about as "key metrics").
# region variants are appended programmatically below.
# VERIFIED 2026-07-01: every URL in FILES returned HTTP 200 with a non-trivial body.
# Region convention on Damodaran's site:
#   ""        -> US
#   "Global"  -> Global (all firms worldwide, incl. US)
#   "emerg"   -> Emerging markets
# NOTE (verified): pedata has NO Global/emerg variant; PE is US-only.
FILES = {
    # stem-base : (topic, has_us, has_global, has_emerg, case-variant for suffix)
    "pedata":  ("PE / trailing & forward PE / PEG", True, False, False),
    "vebitda": ("EV/EBITDA, EV/EBIT, EV/Sales",     True, True,  True),
    "pbv":     ("P/B, ROE, EV/Invested Cap, ROIC",  True, True,  True),   # US stem is 'pbvdata'
    "margin":  ("Gross / operating / net margins",  True, True,  True),
    "roe":     ("ROE (unadjusted & R&D-adjusted)",  True, True,  True),
    "EVA":     ("ROE, ROC(=ROIC), COE, WACC, EVA",  True, True,  True),
}

# Map (base_stem, region) -> actual filename stem on the site (handles irregular names).
def stem_for(base: str, region: str) -> str | None:
    if base == "pedata":
        return "pedata" if region == "us" else None
    if base == "pbv":
        return {"us": "pbvdata", "global": "pbvGlobal", "emerg": "pbvemerg"}[region]
    # vebitda / margin / roe / EVA share a regular pattern
    suffix = {"us": "", "global": "Global", "emerg": "emerg"}[region]
    return base + suffix


def download(stem: str) -> tuple[str, str] | None:
    """Download <stem>.xls into RAW_DIR. Returns (local_path, url) or None on failure."""
    url = f"{BASE}/{stem}.xls"
    dest = os.path.join(RAW_DIR, f"{stem}.xls")
    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
    except Exception as e:  # network failure — do NOT fabricate; report and skip
        print(f"  [FAIL] {stem}: request error {e}")
        return None
    if r.status_code != 200 or len(r.content) < 5000:
        print(f"  [FAIL] {stem}: HTTP {r.status_code}, {len(r.content)} bytes -> {url}")
        return None
    with open(dest, "wb") as f:
        f.write(r.content)
    return dest, url


def find_header_row(raw: pd.DataFrame) -> int | None:
    """Locate the row whose first cell is 'Industry Name' (files have a metadata preamble)."""
    for i in range(min(40, len(raw))):
        if str(raw.iloc[i, 0]).strip().lower().startswith("industry name"):
            return i
    return None


def extract_meta(raw: pd.DataFrame) -> tuple[str, str]:
    """Return (as_of_date_iso, region_tag) from the top metadata block."""
    as_of, region = "", ""
    for i in range(min(8, len(raw))):
        c0 = str(raw.iloc[i, 0]).strip().lower()
        if c0.startswith("date updated"):
            val = raw.iloc[i, 1]
            try:
                as_of = pd.to_datetime(val).date().isoformat()
            except Exception:
                as_of = str(val)
        if c0.startswith("what is this data"):
            # the region tag ('US companies' / 'Global' / 'Emerging') sits a few cols over
            for j in range(2, raw.shape[1]):
                v = str(raw.iloc[i, j]).strip()
                if v and v.lower() != "nan":
                    region = v
                    break
    return as_of, region


def parse_file(path: str, region_label: str) -> tuple[pd.DataFrame, str, str] | None:
    """Parse one Damodaran .xls -> (tidy df with Industry Name + metric cols, as_of, region_tag)."""
    try:
        raw = pd.read_excel(path, sheet_name="Industry Averages", header=None)
    except Exception as e:
        print(f"  [FAIL] parse {os.path.basename(path)}: {e}")
        return None
    as_of, region_tag = extract_meta(raw)
    hrow = find_header_row(raw)
    if hrow is None:
        print(f"  [FAIL] {os.path.basename(path)}: no 'Industry Name' header row found")
        return None
    header = [str(x).strip() for x in raw.iloc[hrow].tolist()]
    # de-duplicate column names (some files repeat a label) so col access returns a Series
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
    data = data.loc[:, [c for c in data.columns if c and str(c).lower() != "nan"]]
    # keep rows with a real industry name; drop trailing notes / blanks
    data = data[data["Industry Name"].notna()]
    data = data[~data["Industry Name"].astype(str).str.strip().isin(["", "nan"])]
    # numeric coercion for everything except the name
    for c in data.columns:
        if c != "Industry Name":
            data[c] = pd.to_numeric(data[c], errors="coerce")
    data.insert(0, "region", region_label)
    return data.reset_index(drop=True), as_of, (region_tag or region_label)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-download", action="store_true",
                    help="skip download, re-parse cached .xls in data/damodaran/")
    args = ap.parse_args()

    os.makedirs(RAW_DIR, exist_ok=True)
    region_labels = {"us": "US", "global": "Global", "emerg": "Emerging"}

    tidy_rows: list[pd.DataFrame] = []
    wide_by_region: dict[str, list[pd.DataFrame]] = {}
    manifest: list[dict] = []

    print(f"Damodaran fetch — {datetime.now().isoformat(timespec='seconds')}")
    print(f"Base: {BASE}\n")

    for base, (topic, has_us, has_global, has_emerg) in FILES.items():
        wanted = []
        if has_us:     wanted.append("us")
        if has_global: wanted.append("global")
        if has_emerg:  wanted.append("emerg")
        for region in wanted:
            stem = stem_for(base, region)
            if stem is None:
                continue
            url = f"{BASE}/{stem}.xls"
            local = os.path.join(RAW_DIR, f"{stem}.xls")
            if not args.no_download:
                got = download(stem)
                if got is None:
                    manifest.append({"file": stem, "url": url, "status": "FAILED",
                                     "as_of": "", "region": region_labels[region], "topic": topic})
                    continue
                local, url = got
            elif not os.path.exists(local):
                print(f"  [SKIP] {stem}: no cached file and --no-download set")
                continue

            parsed = parse_file(local, region_labels[region])
            if parsed is None:
                manifest.append({"file": stem, "url": url, "status": "PARSE_FAILED",
                                 "as_of": "", "region": region_labels[region], "topic": topic})
                continue
            df, as_of, region_tag = parsed
            nind = len(df)
            print(f"  [OK]  {stem:14s} region={region_labels[region]:9s} as_of={as_of or '?':10s} "
                  f"industries={nind:4d}  <- {url}")
            manifest.append({"file": stem, "url": url, "status": "OK", "as_of": as_of,
                             "region": region_labels[region], "region_tag": region_tag,
                             "topic": topic, "n_industries": nind})

            # tidy long form
            long = df.melt(id_vars=["region", "Industry Name"],
                           var_name="metric", value_name="value")
            long["source_file"] = f"{stem}.xls"
            long["source_url"] = url
            long["as_of_date"] = as_of
            long["dataset"] = base
            tidy_rows.append(long)
            wide_by_region.setdefault(region_labels[region], []).append(
                df.set_index("Industry Name").drop(columns=["region"]).add_prefix(f"{base}::"))

    if not tidy_rows:
        print("\nNo datasets parsed. Check network / URLs.")
        return 1

    tidy = pd.concat(tidy_rows, ignore_index=True)
    tidy = tidy[tidy["value"].notna()]
    tidy_path = os.path.join(RAW_DIR, "damodaran_combined.csv")
    tidy.to_csv(tidy_path, index=False)

    for region, frames in wide_by_region.items():
        wide = pd.concat(frames, axis=1)
        wide.to_csv(os.path.join(RAW_DIR, f"damodaran_wide_{region}.csv"))

    man = pd.DataFrame(manifest)
    man.to_csv(os.path.join(RAW_DIR, "damodaran_manifest.csv"), index=False)

    print(f"\nWrote tidy combined CSV: {tidy_path}  ({len(tidy):,} rows)")
    print(f"Wrote per-region wide CSVs for: {', '.join(sorted(wide_by_region))}")
    print(f"Wrote manifest: {os.path.join(RAW_DIR, 'damodaran_manifest.csv')}")
    ok = sum(1 for m in manifest if m['status'] == 'OK')
    print(f"Datasets OK: {ok}/{len(manifest)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
