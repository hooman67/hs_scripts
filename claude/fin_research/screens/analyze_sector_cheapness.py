#!/usr/bin/env python3
"""
analyze_sector_cheapness.py — rank sectors/industries by CHEAPNESS per region,
using (1) valuation vs the sector's OWN 11-year history (percentile), and
(2) valuation vs the region cross-section, paired with quality (ROIC/ROE).

Inputs (all real, cited pulls; no invented numbers):
  - data/damodaran/history/damodaran_history_long.csv  (built by fetch_damodaran_history.py)
      -> per-industry EV/EBITDA + PBV (+ROIC/ROE, +US PE) for data years 2015..2025
         (as_of 2016-01-05 .. 2026-01-05), regions US/Global/Emerging.
  - data/damodaran/damodaran_combined.csv  (the current 2026-01-05 snapshot; quality metrics)

Cheapness measures produced per industry (current = data_year 2025, as_of 2026-01-05):
  A) hist_pct_evebitda : percentile of CURRENT EV/EBITDA within that industry's own history
     (low percentile = cheap vs its own past). Requires >=6 historical years.
  B) hist_pct_pbv      : same for P/B.
  C) hist_pct_pe       : same for Current PE (US only).
  D) xsec_pct_evebitda : percentile of current EV/EBITDA within the region's cross-section
     of industries this year (low = cheap vs peers). (relative-not-historical fallback)
  E) quality (ROIC, ROE, current) for the cheap-vs-quality read.

Composite "own-history cheapness" = mean of available hist percentiles (EV/EBITDA, PBV, and
PE where present). Lower = cheaper vs own history.

Outputs (data/damodaran/history/):
  - sector_cheapness_<REGION>.csv : full ranked table per region (all industries).
Prints the cheapest N per region to stdout for the write-up.
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
HIST = os.path.join(PROJ, "data", "damodaran", "history", "damodaran_history_long.csv")
OUT = os.path.join(PROJ, "data", "damodaran", "history")
CURRENT_DY = 2025  # data year of the latest snapshot (as_of 2026-01-05)
MIN_HIST_YEARS = 6

# industries that aren't real sectors — exclude from ranking (kept in CSV context if present)
AGG_ROWS = {
    "Total Market", "Total Market (without financials)",
    "Total market", "Total market (without financials)",
    "Unclassified", "Total Market (with financials)",
}


def pct_rank_of_last(series: pd.Series, value: float) -> float:
    """Percentile (0-100) of `value` within `series` (all historical values incl current)."""
    vals = series.dropna().values
    if len(vals) == 0:
        return np.nan
    return float((vals < value).sum() + 0.5 * (vals == value).sum()) / len(vals) * 100.0


def build_region(df: pd.DataFrame, region: str) -> pd.DataFrame:
    r = df[df.region == region].copy()
    metrics = ["EV/EBITDA", "PBV", "Current PE"]
    rows = []
    industries = sorted(r["Industry Name"].unique())
    # current cross-section for xsec percentile
    cur = r[r.data_year == CURRENT_DY]
    xsec_evebitda = cur[cur.metric == "EV/EBITDA"].set_index("Industry Name")["value"]
    for ind in industries:
        if ind in AGG_ROWS:
            continue
        sub = r[r["Industry Name"] == ind]
        rec = {"Industry Name": ind, "region": region}
        for m in metrics:
            ms = sub[sub.metric == m].sort_values("data_year")
            if ms.empty:
                rec[f"cur_{m}"] = np.nan
                rec[f"histpct_{m}"] = np.nan
                rec[f"n_years_{m}"] = 0
                rec[f"min_{m}"] = np.nan
                rec[f"max_{m}"] = np.nan
                rec[f"median_{m}"] = np.nan
                continue
            curval = ms[ms.data_year == CURRENT_DY]["value"]
            curval = float(curval.iloc[0]) if len(curval) else np.nan
            hist_vals = ms["value"]  # includes current
            n_years = ms["data_year"].nunique()
            # only trust hist percentile for positive multiples (negatives = loss-makers, meaningless)
            if pd.notna(curval) and n_years >= MIN_HIST_YEARS and curval > 0:
                pos = hist_vals[hist_vals > 0]
                rec[f"histpct_{m}"] = pct_rank_of_last(pos, curval) if len(pos) >= MIN_HIST_YEARS else np.nan
            else:
                rec[f"histpct_{m}"] = np.nan
            rec[f"cur_{m}"] = curval
            rec[f"n_years_{m}"] = n_years
            rec[f"min_{m}"] = float(hist_vals.min())
            rec[f"max_{m}"] = float(hist_vals.max())
            rec[f"median_{m}"] = float(hist_vals.median())
        # quality current
        for q in ["ROIC", "ROE"]:
            qs = sub[(sub.metric == q) & (sub.data_year == CURRENT_DY)]["value"]
            rec[f"cur_{q}"] = float(qs.iloc[0]) if len(qs) else np.nan
        # cross-section percentile of current EV/EBITDA (low = cheap vs peers)
        if ind in xsec_evebitda.index and pd.notna(rec.get("cur_EV/EBITDA")):
            pos = xsec_evebitda[xsec_evebitda > 0]
            rec["xsecpct_EV/EBITDA"] = pct_rank_of_last(pos, rec["cur_EV/EBITDA"]) \
                if rec["cur_EV/EBITDA"] > 0 else np.nan
        else:
            rec["xsecpct_EV/EBITDA"] = np.nan
        rows.append(rec)
    out = pd.DataFrame(rows)
    # composite own-history cheapness = mean of available hist percentiles
    histcols = [c for c in ["histpct_EV/EBITDA", "histpct_PBV", "histpct_Current PE"] if c in out]
    out["hist_cheap_composite"] = out[histcols].mean(axis=1, skipna=True)
    out["n_hist_signals"] = out[histcols].notna().sum(axis=1)
    return out


def main() -> int:
    df = pd.read_csv(HIST)
    for region in ["US", "Global", "Emerging"]:
        out = build_region(df, region)
        path = os.path.join(OUT, f"sector_cheapness_{region}.csv")
        out.to_csv(path, index=False)
        print(f"\n{'='*90}\n{region}: wrote {path}  ({len(out)} industries)\n{'='*90}")
        # cheapest by own-history composite (require >=1 hist signal, positive current EV/EBITDA)
        show = out[(out.n_hist_signals >= 1) & (out["cur_EV/EBITDA"] > 0)].copy()
        show = show.sort_values("hist_cheap_composite")
        cols = ["Industry Name", "hist_cheap_composite", "n_hist_signals",
                "histpct_EV/EBITDA", "histpct_PBV", "cur_EV/EBITDA", "median_EV/EBITDA",
                "cur_PBV", "cur_ROIC", "cur_ROE", "xsecpct_EV/EBITDA"]
        if region == "US":
            cols.insert(4, "histpct_Current PE")
            cols.insert(7, "cur_Current PE")
        cols = [c for c in cols if c in show.columns]
        pd.set_option("display.width", 200, "display.max_columns", 40,
                      "display.float_format", lambda x: f"{x:,.1f}")
        print("CHEAPEST vs OWN HISTORY (low composite percentile = cheap):")
        print(show[cols].head(15).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
