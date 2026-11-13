#!/usr/bin/env python3
"""
run_quant_screen_exus.py — Stage 2.5a: re-run the EXACT Stage-1b cheap-quality screen over
the EXPANDED ex-US / EM universe (screens/universe_exus.py), and rank WITHIN region as well
as globally.

It REUSES the Stage-1b screen code verbatim — imports derive_metrics, piotroski_lite, and
score_and_rank from run_quant_screen.py. NO new scoring method is invented: same metric
definitions, same data-quality guards, same trap gate, same 60% quality / 40% cheapness
combined score. The only additions here are:
  (1) a broader universe (ex-US/EM),
  (2) a yfinance-`sector` financial filter (drop Financial Services / real-estate REITs —
      the parallel agent covers them),
  (3) within-region percentile re-ranking, and
  (4) a coverage report (what % of the ex-US/EM universe had usable data).

Data: yfinance only, cached under data/cache/ (12h TTL). Every number is a real fetch with
an as-of timestamp; missing fields stay blank, never fabricated.

Run:
  /opt/venv/bin/python3 screens/run_quant_screen_exus.py            # use cache where fresh
  /opt/venv/bin/python3 screens/run_quant_screen_exus.py --refresh  # force fresh pulls
  /opt/venv/bin/python3 screens/run_quant_screen_exus.py --limit=50 # smoke test
"""
from __future__ import annotations
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
sys.path.insert(0, DATA)
sys.path.insert(0, HERE)
from fetch_fundamentals import get_fundamentals            # noqa: E402
from universe_exus import build_universe_exus              # noqa: E402
# REUSE Stage-1b screen logic verbatim (do NOT reimplement scoring):
from run_quant_screen import derive_metrics, piotroski_lite, score_and_rank  # noqa: E402

OUT_DIR = HERE
CACHE = os.path.join(DATA, "cache")

# yfinance sectors that indicate a financial / REIT — dropped (parallel agent covers them).
FIN_SECTORS = {"Financial Services"}
REIT_HINT = "REIT"   # yfinance industry contains 'REIT—...' for real-estate trusts


def fetch_all(refresh: bool = False, limit: int | None = None) -> pd.DataFrame:
    uni = build_universe_exus()
    if limit:
        uni = uni.head(limit)
    rows = []
    n = len(uni)
    for i, (_, u) in enumerate(uni.iterrows(), 1):
        fun = get_fundamentals(u["ticker"], refresh=refresh)
        m = derive_metrics(fun, u["region"], u.get("gics_sector"))
        m["ticker"] = u["ticker"]
        m["source"] = u.get("source")
        if not m["name"]:
            m["name"] = u.get("name")
        rows.append(m)
        if i % 25 == 0:
            print(f"  {i}/{n} fetched")
        time.sleep(0.05)
    df = pd.DataFrame(rows)
    pf = df.apply(lambda r: piotroski_lite(r), axis=1, result_type="expand")
    df["piotroski_lite"], df["piotroski_max"], df["piotroski_notes"] = pf[0], pf[1], pf[2]
    return df


def flag_usable(df: pd.DataFrame) -> pd.DataFrame:
    """Coverage flags: 'reachable' (yfinance returned something) + key-field completeness."""
    d = df.copy()
    key = ["marketCap", "enterpriseValue", "quality_return", "gross_margin",
           "operating_margin", "debt_to_equity_pct", "current_ratio", "trailingPE",
           "priceToBook", "ev_ebitda", "fcf"]
    d["reachable"] = d["yf_error"].isna() & d["marketCap"].notna()
    d["n_key_present"] = d[key].notna().sum(axis=1)
    d["usable"] = d["reachable"] & (d["n_key_present"] >= 8)
    return d


def drop_financials(df: pd.DataFrame) -> pd.DataFrame:
    """Drop names yfinance labels Financial Services or a REIT (parallel agent's turf)."""
    sec = df["yf_sector"].fillna("")
    ind = df["yf_industry"].fillna("")
    is_fin = sec.isin(FIN_SECTORS) | ind.str.contains(REIT_HINT, case=False, na=False)
    return df[~is_fin].copy(), int(is_fin.sum())


def rank_within_region(ranked: pd.DataFrame) -> pd.DataFrame:
    """Add within-region percentile of the SAME combined_score (no new scoring)."""
    r = ranked.copy()
    r["region_pctl"] = (
        r.groupby("region")["combined_score"].rank(pct=True) * 100).round(1)
    r["region_rank"] = r.groupby("region")["combined_score"].rank(
        ascending=False, method="min").astype(int)
    return r


def main():
    refresh = "--refresh" in sys.argv
    lim = None
    for a in sys.argv:
        if a.startswith("--limit="):
            lim = int(a.split("=")[1])

    print("Fetching expanded ex-US/EM fundamentals (yfinance, cached)...")
    df = fetch_all(refresh=refresh, limit=lim)

    # coverage BEFORE dropping financials (coverage is about data reach, not applicability)
    df = flag_usable(df)
    raw_out = os.path.join(OUT_DIR, "quant_screen_exus_raw.csv")
    df.to_csv(raw_out, index=False)
    print(f"Wrote raw metrics: {raw_out}  ({len(df)} names)")

    # coverage report
    cov = (df.groupby("region")
             .agg(n=("ticker", "size"),
                  reachable=("reachable", "sum"),
                  usable=("usable", "sum"),
                  mean_key=("n_key_present", "mean"))
             .reset_index())
    cov["reachable_pct"] = (100 * cov["reachable"] / cov["n"]).round(1)
    cov["usable_pct"] = (100 * cov["usable"] / cov["n"]).round(1)
    cov["mean_key"] = cov["mean_key"].round(1)
    cov_out = os.path.join(OUT_DIR, "quant_screen_exus_coverage.csv")
    cov.to_csv(cov_out, index=False)
    print("\nCoverage by region:\n" + cov.to_string(index=False))

    # drop financials/REITs by yfinance sector, then score with the EXACT Stage-1b logic
    nonfin, n_fin = drop_financials(df)
    print(f"\nDropped {n_fin} yfinance-labelled financials/REITs before scoring.")

    ranked = score_and_rank(nonfin)      # <-- reused verbatim
    ranked = rank_within_region(ranked)
    ranked_out = os.path.join(OUT_DIR, "quant_screen_exus_ranked.csv")
    ranked.to_csv(ranked_out, index=False)
    print(f"Wrote ranked: {ranked_out}  ({len(ranked)} rankable)")

    gated = ranked[ranked["passes_trap_gate"]]
    cols = ["region_rank", "ticker", "name", "region", "yf_sector", "quality_score",
            "cheapness_score", "combined_score", "roic_proxy", "roe", "ev_ebitda"]
    for reg in ["DEV_EXUS", "EM"]:
        sub = gated[gated["region"] == reg].head(15)
        print(f"\nTop 15 {reg} (trap-gate PASS):")
        print(sub[cols].to_string(index=False))


if __name__ == "__main__":
    main()
