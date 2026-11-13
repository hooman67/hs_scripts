#!/usr/bin/env python3
"""
run_quant_screen.py — Stage 1b bottom-up quality-at-a-price screen (Greenblatt-style,
QUALITY-FIRST). Global universe (US S&P500 + developed ex-US + EM large caps).

Pipeline:
  1. Build universe (screens/universe.py).
  2. Pull yfinance fundamentals for every name (data/fetch_fundamentals.get_fundamentals),
     cached in data/cache/yf_*.json. No EDGAR here (screen is breadth-first; EDGAR is a
     Stage-2 cross-check).
  3. Derive metrics from REAL pulled fields only (never invented):
       QUALITY   : roic_proxy (EBIT*(1-.21)/(totalDebt+equity-cash)) OR fallback ROE,
                   gross/operating margins, debt/equity, current ratio, FCF>0.
       CHEAPNESS : earnings_yield (EBIT/EV), fcf_yield, EV/EBITDA, trailingPE, P/B.
       TRAP      : Piotroski-lite (profitability + leverage/liquidity + efficiency signals
                   from the fields yfinance gives — a partial F-score, honestly labelled).
  4. Quality-first combined rank: percentile-rank each name on a quality composite and a
     cheapness composite (higher=better); combined = 0.60*Q + 0.40*C. Quality weighted
     heavier per the project's quality-first mandate.
  5. Apply gates (positive FCF, not extreme leverage, has core data), rank, write CSV.

EBIT proxy: operatingMargins * totalRevenue when both present; else ebitda - (implied D&A)
is not reliably available, so we require operatingMargins+revenue for the EBIT/EV yield and
leave it blank otherwise (flagged). ROIC proxy uses NOPAT=EBIT*(1-0.21) over invested
capital = totalDebt + (marketCap/priceToBook if bookValue path) ... we use book equity via
(marketCap / priceToBook) when priceToBook present, else skip and fall back to ROE.

All figures carry the yfinance as_of timestamp from the cached pull.
"""
from __future__ import annotations
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
sys.path.insert(0, DATA)          # for fetch_fundamentals
sys.path.insert(0, HERE)          # for universe
from fetch_fundamentals import get_fundamentals   # noqa: E402
from universe import build_universe, EM_STRESS     # noqa: E402

OUT_DIR = HERE
CACHE = os.path.join(DATA, "cache")


def _num(x):
    try:
        if x is None:
            return np.nan
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def derive_metrics(fun: dict, region: str, gics: str | None) -> dict:
    """Turn one yfinance pull into the screen's metric row. Never fabricates."""
    g = lambda k: _num(fun.get(k))
    mcap = g("marketCap")
    ev = g("enterpriseValue")
    rev_growth = g("revenueGrowth")
    ebitda_m = g("ebitdaMargins")
    op_m = g("operatingMargins")
    gross_m = g("grossMargins")
    net_m = g("profitMargins")
    roe = g("returnOnEquity")
    roa = g("returnOnAssets")
    d2e = g("debtToEquity")            # yfinance reports as a percentage (e.g. 30.3 = 30.3%)
    cur = g("currentRatio")
    quick = g("quickRatio")
    fcf = g("freeCashflow")
    ocf = g("operatingCashflow")
    ptb = g("priceToBook")
    pe = g("trailingPE")
    ev_ebitda = g("enterpriseToEbitda")
    beta = g("beta")
    total_debt = g("totalDebt")
    cash = g("totalCash")

    # ---- EBIT proxy (operating income) ----
    # yfinance .info lacks totalRevenue in the harvested schema; approximate EBIT via
    # ebitda * (op_m/ebitda_m) is circular. Best available: reconstruct revenue from
    # marketCap? No. Use: EBIT = EV/EV_EBITDA(=ebitda) * (op_m/ebitda_m) when both margins.
    ebit = np.nan
    ebitda_abs = np.nan
    if not np.isnan(ev_ebitda) and ev_ebitda not in (0,) and not np.isnan(ev):
        ebitda_abs = ev / ev_ebitda                      # implied EBITDA level from EV & EV/EBITDA
    if not np.isnan(ebitda_abs) and not np.isnan(op_m) and not np.isnan(ebitda_m) and ebitda_m not in (0,):
        ebit = ebitda_abs * (op_m / ebitda_m)            # scale EBITDA -> EBIT by margin ratio

    # ---- Cheapness ----
    earnings_yield = (ebit / ev) if (not np.isnan(ebit) and not np.isnan(ev) and ev > 0) else np.nan
    fcf_yield = (fcf / mcap) if (not np.isnan(fcf) and not np.isnan(mcap) and mcap > 0) else np.nan

    # ---- ROIC proxy: NOPAT / invested capital ----
    # invested capital = total debt + book equity - cash; book equity via marketCap/priceToBook.
    roic = np.nan
    if not np.isnan(ptb) and ptb > 0 and not np.isnan(mcap):
        book_equity = mcap / ptb
        inv_cap = (0 if np.isnan(total_debt) else total_debt) + book_equity - (0 if np.isnan(cash) else cash)
        if not np.isnan(ebit) and inv_cap and inv_cap > 0:
            roic = (ebit * (1 - 0.21)) / inv_cap
    quality_return = roic if not np.isnan(roic) else roe   # fall back to ROE

    return {
        "region": region, "gics_sector": gics,
        "name": fun.get("shortName") or fun.get("longName"),
        "currency": fun.get("currency"), "country": fun.get("country"),
        "yf_sector": fun.get("sector"), "yf_industry": fun.get("industry"),
        "as_of": fun.get("as_of"),
        "marketCap": mcap, "enterpriseValue": ev,
        # quality
        "roic_proxy": roic, "roe": roe, "roa": roa, "quality_return": quality_return,
        "gross_margin": gross_m, "operating_margin": op_m, "net_margin": net_m,
        "debt_to_equity_pct": d2e, "current_ratio": cur, "quick_ratio": quick,
        "fcf": fcf, "ocf": ocf, "rev_growth": rev_growth,
        # cheapness
        "earnings_yield_ebit_ev": earnings_yield, "fcf_yield": fcf_yield,
        "ev_ebitda": ev_ebitda, "trailingPE": pe, "priceToBook": ptb, "beta": beta,
        "ebit_proxy": ebit,
        "n_missing": len(fun.get("_missing", [])),
        "yf_error": fun.get("error"),
    }


def piotroski_lite(r: dict) -> tuple[int, int, str]:
    """Partial Piotroski F-score from available yfinance fields. Returns (score, max, notes).
    Only scores signals we can compute from a single .info snapshot — labelled 'lite'."""
    score, mx, notes = 0, 0, []
    # Profitability
    if not np.isnan(r["roa"]):
        mx += 1
        if r["roa"] > 0:
            score += 1; notes.append("ROA>0")
    if not np.isnan(r["fcf"]):
        mx += 1
        if r["fcf"] > 0:
            score += 1; notes.append("FCF>0")
    # accruals: FCF/OCF vs net income proxy — use OCF>0
    if not np.isnan(r["ocf"]):
        mx += 1
        if r["ocf"] > 0:
            score += 1; notes.append("OCF>0")
    # Leverage / liquidity
    if not np.isnan(r["current_ratio"]):
        mx += 1
        if r["current_ratio"] >= 1.0:
            score += 1; notes.append("CR>=1")
    if not np.isnan(r["debt_to_equity_pct"]):
        mx += 1
        if r["debt_to_equity_pct"] < 100:   # debt < equity
            score += 1; notes.append("D/E<100%")
    # Operating efficiency
    if not np.isnan(r["operating_margin"]):
        mx += 1
        if r["operating_margin"] > 0:
            score += 1; notes.append("OpMgn>0")
    if not np.isnan(r["rev_growth"]):
        mx += 1
        if r["rev_growth"] > 0:
            score += 1; notes.append("RevGrow>0")
    return score, mx, ",".join(notes)


def run(refresh: bool = False, limit: int | None = None) -> pd.DataFrame:
    uni = build_universe()
    if limit:
        uni = uni.head(limit)
    rows = []
    n = len(uni)
    for i, (_, u) in enumerate(uni.iterrows(), 1):
        fun = get_fundamentals(u["ticker"], refresh=refresh)
        m = derive_metrics(fun, u["region"], u.get("gics_sector"))
        m["ticker"] = u["ticker"]
        if not m["name"]:
            m["name"] = u.get("name")
        rows.append(m)
        if i % 25 == 0:
            print(f"  {i}/{n} fetched")
        time.sleep(0.05)
    df = pd.DataFrame(rows)

    # Piotroski-lite
    pf = df.apply(lambda r: piotroski_lite(r), axis=1, result_type="expand")
    df["piotroski_lite"], df["piotroski_max"], df["piotroski_notes"] = pf[0], pf[1], pf[2]

    return df


def score_and_rank(df: pd.DataFrame) -> pd.DataFrame:
    """Quality-first combined percentile rank + gates."""
    d = df.copy()

    # ---- DATA-QUALITY GUARDS (avoid ranking on yfinance artifacts) ----
    # EV/EBITDA <= 0 (net-cash or loss-making => EV can be negative) is NOT a clean
    # cheapness signal via this multiple; EV/EBITDA < 2 for a going concern is almost
    # always a data glitch (e.g. ADR/local EV mismatch). Blank both, and blank the
    # EV-derived earnings yield when EV/EBITDA is out of the plausible band.
    bad_ev = d["ev_ebitda"].notna() & (d["ev_ebitda"] < 2)
    d.loc[bad_ev, "ev_ebitda_clean"] = np.nan
    d["ev_ebitda_clean"] = d["ev_ebitda"].where(~bad_ev, np.nan)
    d["earnings_yield_clean"] = d["earnings_yield_ebit_ev"].where(~bad_ev, np.nan)
    # ROIC proxy > 100% is buyback-depressed-equity noise -> keep for display, flag it,
    # but blank it from the ranking input so one artifact can't dominate the quality rank.
    d["roic_unreliable"] = d["roic_proxy"] > 1.0
    d["quality_return_clean"] = d["quality_return"].where(
        ~((d["quality_return"] == d["roic_proxy"]) & d["roic_unreliable"]), d["roe"])

    # ---- eligibility gate: must have the core inputs to be rankable ----
    has_quality = d["quality_return_clean"].notna() & (d["gross_margin"].notna() | d["operating_margin"].notna())
    has_cheap = d["earnings_yield_clean"].notna() | d["fcf_yield"].notna() | d["ev_ebitda_clean"].notna()
    d["rankable"] = has_quality & has_cheap & d["yf_error"].isna()

    r = d[d["rankable"]].copy()

    def pct(col, higher_better=True):
        s = r[col].astype(float)
        pr = s.rank(pct=True)
        return pr if higher_better else (1 - pr)

    # Quality composite (higher better): return on capital, margins, low leverage, liquidity
    q_return = pct("quality_return_clean", True)
    q_gross = pct("gross_margin", True)
    q_op = pct("operating_margin", True)
    q_lev = pct("debt_to_equity_pct", False)          # lower leverage better
    q_liq = pct("current_ratio", True)
    quality = pd.concat([q_return, q_gross, q_op, q_lev, q_liq], axis=1).mean(axis=1, skipna=True)

    # Cheapness composite (higher better = cheaper): high EY, high FCF yield, low EV/EBITDA, low PE, low PB
    c_ey = pct("earnings_yield_clean", True)
    c_fcf = pct("fcf_yield", True)
    c_evebitda = pct("ev_ebitda_clean", False)
    c_pe = pct("trailingPE", False)
    c_pb = pct("priceToBook", False)
    cheap = pd.concat([c_ey, c_fcf, c_evebitda, c_pe, c_pb], axis=1).mean(axis=1, skipna=True)

    r["quality_score"] = (quality * 100).round(1)
    r["cheapness_score"] = (cheap * 100).round(1)
    # QUALITY-FIRST: 60/40
    r["combined_score"] = (0.60 * r["quality_score"] + 0.40 * r["cheapness_score"]).round(1)

    # Trap gate: require positive FCF and Piotroski-lite >= 60% of its max, D/E not extreme
    pf_ratio = r["piotroski_lite"] / r["piotroski_max"].replace(0, np.nan)
    r["fcf_positive"] = r["fcf"] > 0
    r["passes_trap_gate"] = (
        (r["fcf"] > 0) &
        (pf_ratio >= 0.6) &
        ((r["debt_to_equity_pct"] < 300) | r["debt_to_equity_pct"].isna())
    )
    r = r.sort_values("combined_score", ascending=False).reset_index(drop=True)
    return r


def main():
    refresh = "--refresh" in sys.argv
    lim = None
    for a in sys.argv:
        if a.startswith("--limit="):
            lim = int(a.split("=")[1])
    print("Building universe + fetching fundamentals (yfinance, cached)...")
    df = run(refresh=refresh, limit=lim)
    raw_out = os.path.join(OUT_DIR, "quant_screen_raw.csv")
    df.to_csv(raw_out, index=False)
    print(f"Wrote raw metrics: {raw_out}  ({len(df)} names)")

    ranked = score_and_rank(df)
    ranked_out = os.path.join(OUT_DIR, "quant_screen_ranked.csv")
    ranked.to_csv(ranked_out, index=False)
    print(f"Wrote ranked: {ranked_out}  ({len(ranked)} rankable)")

    err = df[df["yf_error"].notna()]
    print(f"\nyfinance errors: {len(err)}  |  rankable: {len(ranked)}/{len(df)}")
    top = ranked[ranked["passes_trap_gate"]].head(20)
    cols = ["ticker", "name", "region", "yf_sector", "quality_score", "cheapness_score",
            "combined_score", "roic_proxy", "roe", "earnings_yield_ebit_ev", "ev_ebitda"]
    print("\nTop 20 (passing trap gate):")
    print(top[cols].to_string(index=False))


if __name__ == "__main__":
    main()
