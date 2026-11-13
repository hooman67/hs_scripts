#!/usr/bin/env python3
"""
em_stress_test.py — measure yfinance field completeness on a broad EM batch.

This is the evidence for the Stage-0 open question: is a paid global fundamentals API
needed for EM breadth? We pull ~40 mixed EM tickers (reaching below mega-caps and into
local-only listings) and report, per name and in aggregate, how many of the KEY screening
fields yfinance actually returns. No fabrication — a missing field is counted as missing.
"""
from __future__ import annotations
import os
import sys
import time
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
sys.path.insert(0, DATA)
sys.path.insert(0, HERE)
from fetch_fundamentals import get_fundamentals   # noqa: E402
from universe import EM_STRESS                     # noqa: E402

# The fields the screen actually needs to rank a name (quality + cheapness core).
KEY_FIELDS = [
    "marketCap", "enterpriseValue", "trailingPE", "priceToBook", "enterpriseToEbitda",
    "returnOnEquity", "grossMargins", "operatingMargins", "debtToEquity",
    "freeCashflow", "currentRatio",
]


def run(refresh: bool = False) -> pd.DataFrame:
    rows = []
    for tk in EM_STRESS:
        f = get_fundamentals(tk, refresh=refresh)
        present = sum(1 for k in KEY_FIELDS if f.get(k) not in (None, "", "Infinity"))
        rows.append({
            "ticker": tk,
            "name": f.get("shortName") or f.get("longName"),
            "country": f.get("country"),
            "currency": f.get("currency"),
            "key_present": present,
            "key_total": len(KEY_FIELDS),
            "key_pct": round(100 * present / len(KEY_FIELDS), 1),
            "usable": present >= 8,          # >=8/11 key fields = enough to rank
            "yf_error": f.get("error"),
        })
        time.sleep(0.05)
    return pd.DataFrame(rows)


def main():
    refresh = "--refresh" in sys.argv
    df = run(refresh=refresh)
    out = os.path.join(HERE, "em_stress_test.csv")
    df.to_csv(out, index=False)
    print(df.to_string(index=False))
    n = len(df)
    usable = int(df["usable"].sum())
    errs = int(df["yf_error"].notna().sum())
    print(f"\n=== EM STRESS TEST ({n} tickers) ===")
    print(f"Usable (>=8/{len(KEY_FIELDS)} key fields): {usable}/{n} = {100*usable/n:.0f}%")
    print(f"Mean key-field completeness: {df['key_pct'].mean():.0f}%")
    print(f"yfinance errors: {errs}/{n}")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
