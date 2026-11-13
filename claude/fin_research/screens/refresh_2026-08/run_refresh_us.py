#!/usr/bin/env python3
"""
run_refresh_us.py — RE-RUN of the Stage-1b quality-at-a-price quant screen on TODAY's
live yfinance data (2026-08-26), restricted to the US large/mid-cap universe (S&P 500).

REUSES the existing screen code verbatim — imports derive_metrics / piotroski_lite /
score_and_rank from screens/run_quant_screen.py and build_universe from screens/universe.py.
No methodology change. Only differences from the 2026-07-02 run:
  1. region == "US" filter (task scope: US large/mid cap).
  2. refresh=True forces a fresh yfinance .info pull for every name (today's prices).

Outputs (in this refresh_2026-08/ dir):
  - quant_us_raw.csv     : all derived metrics for every US name pulled today
  - quant_us_ranked.csv  : rankable + scored (quality-first 60/40) + trap gate
Anti-hallucination: every number is a real yfinance pull with an as_of timestamp on the row.
"""
from __future__ import annotations
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SCREENS = os.path.dirname(HERE)
DATA = os.path.join(SCREENS, "..", "data")
sys.path.insert(0, DATA)
sys.path.insert(0, SCREENS)

from fetch_fundamentals import get_fundamentals            # noqa: E402
from universe import build_universe                        # noqa: E402
from run_quant_screen import derive_metrics, piotroski_lite, score_and_rank  # noqa: E402


def run_us(refresh: bool = True) -> pd.DataFrame:
    uni = build_universe()
    uni = uni[uni["region"] == "US"].reset_index(drop=True)
    rows = []
    n = len(uni)
    print(f"US universe: {n} names. Pulling yfinance (refresh={refresh})...")
    for i, (_, u) in enumerate(uni.iterrows(), 1):
        fun = get_fundamentals(u["ticker"], refresh=refresh)
        m = derive_metrics(fun, u["region"], u.get("gics_sector"))
        m["ticker"] = u["ticker"]
        if not m["name"]:
            m["name"] = u.get("name")
        # keep forwardPE for the deliverable (derive_metrics doesn't carry it)
        m["forwardPE"] = fun.get("forwardPE")
        rows.append(m)
        if i % 25 == 0:
            print(f"  {i}/{n} fetched")
        time.sleep(0.05)
    df = pd.DataFrame(rows)
    pf = df.apply(lambda r: piotroski_lite(r), axis=1, result_type="expand")
    df["piotroski_lite"], df["piotroski_max"], df["piotroski_notes"] = pf[0], pf[1], pf[2]
    return df


def main():
    t0 = datetime.now(timezone.utc)
    print(f"REFRESH RUN start {t0.isoformat(timespec='seconds')}")
    refresh = "--no-refresh" not in sys.argv
    df = run_us(refresh=refresh)
    raw_out = os.path.join(HERE, "quant_us_raw.csv")
    df.to_csv(raw_out, index=False)
    print(f"Wrote raw: {raw_out} ({len(df)} names)")

    ranked = score_and_rank(df)
    # carry forwardPE onto the ranked frame
    fwd = df.set_index("ticker")["forwardPE"]
    ranked["forwardPE"] = ranked["ticker"].map(fwd)
    ranked_out = os.path.join(HERE, "quant_us_ranked.csv")
    ranked.to_csv(ranked_out, index=False)
    print(f"Wrote ranked: {ranked_out} ({len(ranked)} rankable)")

    err = df[df["yf_error"].notna()]
    t1 = datetime.now(timezone.utc)
    print(f"\nyfinance errors: {len(err)}  |  rankable: {len(ranked)}/{len(df)}")
    if len(err):
        print("  error tickers:", list(err["ticker"]))
    print(f"as_of sample: {df['as_of'].dropna().iloc[0] if df['as_of'].notna().any() else 'NA'}")
    print(f"REFRESH RUN end {t1.isoformat(timespec='seconds')}  ({(t1-t0).total_seconds():.0f}s)")

    top = ranked[ranked["passes_trap_gate"]].head(30)
    cols = ["ticker", "name", "gics_sector", "quality_score", "cheapness_score",
            "combined_score", "roe", "trailingPE", "forwardPE", "ev_ebitda",
            "priceToBook", "fcf_yield"]
    print("\nTop 30 (trap-gate PASS):")
    print(top[cols].to_string(index=False))


if __name__ == "__main__":
    main()
