#!/usr/bin/env python3
"""
run_financials_screen.py — Stage 2.5b FINANCIALS-appropriate value+quality screen.

Banks, insurers, diversified financials (+ REITs as a separate sub-group), global,
emphasis on EM + developed-ex-US. Uses SECTOR-APPROPRIATE metrics because banks/
insurers/REITs have no gross margin or EV/EBITDA and so were structurally dropped by
the generic Stage 1b screen.

METRICS (why they differ from the generic screen):
  Value (financials):
    - P/B  (priceToBook)      -- THE primary valuation metric for banks/insurers.
    - P/E  (trailingPE)       -- earnings multiple.
    - fwd P/E (forwardPE)     -- context only.
    - Dividend yield          -- financials are income-heavy; payoutRatio for sustainability.
    (P/TangibleBook, price/embedded-value NOT on yfinance -> reported unavailable, not faked.)
  Quality (financials):
    - ROE (returnOnEquity)    -- THE key one; pairs with P/B (high ROE + low P/B = cheap quality).
    - ROA (returnOnAssets)    -- capital efficiency; for banks a low ROA is normal (levered B/S).
    - equity/assets proxy = ROA/ROE (= 1/leverage) -- a crude CAPITAL-STRENGTH proxy for banks
      (higher = less levered = stronger capital). yfinance lacks CET1 / NIM / combined ratio.
    - Earnings stability proxy: |earningsGrowth| large-negative = instability flag.
  Trap filter (financials):
    - positive ROE (a bank at 0.4x book with collapsing ROE is a trap, not a bargain)
    - ROE not de-minimis (>= 5%) AND earnings not collapsing (earningsGrowth > -40%)
    - payout sustainable (payoutRatio <= 1.0, or unknown)
    - not a *cheap-for-a-reason* combo: very low P/B (<0.6) WITH sub-8% ROE => trap flag.

SCORING (quality-first, per project mandate CLAUDE.md sec.3):
  Percentile-rank WITHIN each region x sub-group peer set (so a cheap EM bank is ranked
  vs EM banks, an EM insurer vs EM insurers) on:
    Quality = mean(pctl(ROE), pctl(ROA), pctl(capital proxy))
    Cheap   = mean(pctl(low P/B), pctl(low P/E), pctl(div yield))
    Combined = 0.60*Quality + 0.40*Cheap.
  Reported per-region so EM names get a fair shot (not crowded out by the US count).

ANTI-HALLUCINATION: every number is a real yfinance pull (data/fetch_fundamentals),
cached with an as_of timestamp. Tickers that return no data are DROPPED and logged
(no fabricated tickers). Missing fields stay blank; NIM/CET1/combined-ratio/embedded-
value are reported as unavailable, never invented.
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
from financials_universe import build_financials_universe  # noqa: E402

OUT_DIR = HERE


def _num(x):
    try:
        if x is None:
            return np.nan
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def classify_subgroup(industry: str | None, hint: str) -> str:
    """Map yfinance `industry` -> our sub-group. Fall back to the universe hint."""
    ind = (industry or "").lower()
    if "reit" in ind or hint == "REIT":
        return "REIT"
    if "bank" in ind:
        return "BANK"
    if "insurance" in ind:
        # keep insurer granularity for the report
        if "life" in ind:
            return "INSURER_LIFE"
        if "reinsurance" in ind:
            return "INSURER_REINS"
        if "property" in ind or "casualty" in ind:
            return "INSURER_PC"
        return "INSURER_DIV"
    if any(k in ind for k in ("asset management", "capital markets", "financial data",
                              "credit services", "insurance brokers", "financial - ",
                              "mortgage")):
        return "DIVFIN"
    # fall back to hint
    if hint in ("BANK", "REIT"):
        return hint
    if hint == "INSURER":
        return "INSURER_DIV"
    if hint == "DIVFIN":
        return "DIVFIN"
    return "DIVFIN"   # generic financial holdco


def derive(fun: dict, region: str, hint: str) -> dict:
    g = lambda k: _num(fun.get(k))
    ptb = g("priceToBook")
    pe = g("trailingPE")
    fpe = g("forwardPE")
    roe = g("returnOnEquity")
    roa = g("returnOnAssets")
    dy = g("dividendYield")          # yfinance returns as a percent (e.g. 5.98 = 5.98%)
    payout = g("payoutRatio")
    bv = g("bookValue")
    beta = g("beta")
    egrow = g("earningsGrowth")
    rgrow = g("revenueGrowth")
    mcap = g("marketCap")

    # capital-strength proxy for banks: equity/assets = ROA/ROE (= 1/equity-multiplier).
    # higher => less levered => stronger capital. Only meaningful when both present & ROE>0.
    cap_proxy = (roa / roe) if (not np.isnan(roa) and not np.isnan(roe) and roe > 0) else np.nan

    industry = fun.get("industry")
    sub = classify_subgroup(industry, hint)

    return {
        "region": region, "sub_group": sub, "hint": hint,
        "name": fun.get("shortName") or fun.get("longName"),
        "currency": fun.get("currency"), "country": fun.get("country"),
        "yf_industry": industry, "as_of": fun.get("as_of"),
        "marketCap": mcap,
        # value
        "priceToBook": ptb, "trailingPE": pe, "forwardPE": fpe,
        "dividendYield_pct": dy, "payoutRatio": payout, "bookValue": bv,
        # quality
        "roe": roe, "roa": roa, "cap_proxy_eq_assets": cap_proxy,
        "earningsGrowth": egrow, "revenueGrowth": rgrow, "beta": beta,
        "n_missing": len(fun.get("_missing", [])),
        "yf_error": fun.get("error"),
    }


def trap_status(r: pd.Series) -> str:
    """Financials trap filter. Returns 'PASS' or a reason string (a flag)."""
    roe = r["roe"]; ptb = r["priceToBook"]; egrow = r["earningsGrowth"]; payout = r["payoutRatio"]
    reasons = []
    if pd.isna(roe):
        return "NO_ROE"          # can't judge quality -> can't clear
    if roe <= 0:
        reasons.append("ROE<=0")
    elif roe < 0.05:
        reasons.append("ROE<5%")
    if not pd.isna(egrow) and egrow < -0.40:
        reasons.append("earnings_collapsing")
    if not pd.isna(payout) and payout > 1.0:
        reasons.append("payout>100%")
    # classic value trap: bank/insurer at very low P/B with weak returns
    if not pd.isna(ptb) and ptb < 0.6 and not pd.isna(roe) and roe < 0.08:
        reasons.append("cheap_low_ROE_trap")
    return "PASS" if not reasons else ";".join(reasons)


def run(refresh: bool = False, limit: int | None = None) -> pd.DataFrame:
    uni = build_financials_universe()
    if limit:
        uni = uni.head(limit)
    rows, n = [], len(uni)
    print(f"Fetching {n} financials (yfinance, cached, no EDGAR)...")
    for i, (_, u) in enumerate(uni.iterrows(), 1):
        fun = get_fundamentals(u["ticker"], refresh=refresh)
        m = derive(fun, u["region"], u["sub_group_hint"])
        m["ticker"] = u["ticker"]
        if not m["name"]:
            m["name"] = u.get("name")
        rows.append(m)
        if i % 25 == 0:
            print(f"  {i}/{n}")
        time.sleep(0.05)
    return pd.DataFrame(rows)


# Duplicate listings: same company on two Yahoo lines (a US ADR + its native exchange).
# We keep the NATIVE listing (local currency / primary market) and drop the ADR from the
# ranking so one company isn't ranked twice. Value = ADR ticker to drop.
ADR_DUPES_TO_DROP = {
    "BBVA", "NWG", "HSBC", "ITUB", "MFC", "SLF", "MUFG", "SMFG", "BBD",
    "IBN", "HDB", "KB", "SHG", "BCS", "LYG", "ING", "DB", "UBS", "MFG",
    "AEG", "DBSDF",
}


def score(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()

    # a ticker is "live" if it returned identity + at least P/B or ROE
    d["live"] = d["yf_error"].isna() & (d["priceToBook"].notna() | d["roe"].notna()) & d["name"].notna()

    # drop ADR duplicates from ranking ONLY when the native listing is also live in the set
    live_tickers = set(d.loc[d["live"], "ticker"])
    adr_native = {  # ADR -> native ticker; drop ADR if native present
        "BBVA": "BBVA.MC", "NWG": "NWG.L", "HSBC": "HSBA.L", "ITUB": "ITUB4.SA",
        "MFC": "MFC.TO", "SLF": "SLF.TO", "MUFG": "8306.T", "SMFG": "8316.T",
        "BBD": "BBDC4.SA", "IBN": "ICICIBANK.NS", "HDB": "HDFCBANK.NS",
        "KB": "105560.KS", "SHG": "055550.KS",
    }
    d["is_adr_dupe"] = d.apply(
        lambda r: r["ticker"] in adr_native and adr_native[r["ticker"]] in live_tickers, axis=1)
    # DATA-QUALITY GUARD: a P/B < 0.05 for a going concern is a Yahoo share-class/currency
    # glitch (e.g. BRK-B: B-share price vs A-share-scaled book -> P/B ~0.001), NOT a real
    # 20x-below-book valuation. Flag it and exclude from the ranking so it can't dominate the
    # "cheap" percentile. (Genuinely-cheap distressed names like China Cinda at 0.17 survive.)
    d["pb_glitch"] = d["priceToBook"].notna() & (d["priceToBook"] < 0.05)

    # rankable = live, not an ADR duplicate, no P/B glitch, has P/B AND ROE (load-bearing)
    d["rankable"] = (d["live"] & ~d["is_adr_dupe"] & ~d["pb_glitch"]
                     & d["priceToBook"].notna() & d["roe"].notna() & (d["priceToBook"] > 0))

    d["trap_status"] = d.apply(trap_status, axis=1)

    # peer group = region x sub_group (banks vs banks, EM life vs EM life, ...)
    # collapse insurer sub-types into INSURER for peer-ranking robustness (small cells)
    def peer_key(row):
        sg = row["sub_group"]
        sg2 = "INSURER" if sg.startswith("INSURER") else sg
        return f"{row['region']}|{sg2}"
    d["peer_group"] = d.apply(peer_key, axis=1)

    r = d[d["rankable"]].copy()

    def pct_within(col, higher_better=True):
        def f(g):
            s = g[col].astype(float)
            pr = s.rank(pct=True)
            return pr if higher_better else (1 - pr)
        out = r.groupby("peer_group", group_keys=False).apply(f)
        return out

    # Quality (higher better): ROE, ROA, capital proxy
    q_roe = pct_within("roe", True)
    q_roa = pct_within("roa", True)
    q_cap = pct_within("cap_proxy_eq_assets", True)
    quality = pd.concat([q_roe, q_roa, q_cap], axis=1).mean(axis=1, skipna=True)

    # Cheapness (higher better = cheaper): low P/B, low P/E, high div yield
    c_pb = pct_within("priceToBook", False)
    c_pe = pct_within("trailingPE", False)
    c_dy = pct_within("dividendYield_pct", True)
    cheap = pd.concat([c_pb, c_pe, c_dy], axis=1).mean(axis=1, skipna=True)

    r["quality_score"] = (quality * 100).round(1)
    r["cheapness_score"] = (cheap * 100).round(1)
    r["combined_score"] = (0.60 * r["quality_score"] + 0.40 * r["cheapness_score"]).round(1)
    r = r.sort_values(["combined_score"], ascending=False).reset_index(drop=True)
    return d, r


def main():
    refresh = "--refresh" in sys.argv
    lim = None
    for a in sys.argv:
        if a.startswith("--limit="):
            lim = int(a.split("=")[1])
    raw = run(refresh=refresh, limit=lim)
    raw_out = os.path.join(OUT_DIR, "financials_screen_raw.csv")
    raw.to_csv(raw_out, index=False)
    print(f"\nWrote raw: {raw_out}  ({len(raw)} names)")

    allrows, ranked = score(raw)
    allrows.to_csv(os.path.join(OUT_DIR, "financials_screen_all.csv"), index=False)
    ranked_out = os.path.join(OUT_DIR, "financials_screen_ranked.csv")
    ranked.to_csv(ranked_out, index=False)

    n_live = int(allrows["live"].sum())
    n_rank = len(ranked)
    n_dead = int((~allrows["live"]).sum())
    dead = allrows[~allrows["live"]]["ticker"].tolist()
    has_pb = int(allrows["priceToBook"].notna().sum())
    has_roe = int(allrows["roe"].notna().sum())
    both = int((allrows["priceToBook"].notna() & allrows["roe"].notna()).sum())
    print(f"Wrote ranked: {ranked_out}  ({n_rank} rankable)")
    print(f"\nCOVERAGE: {len(allrows)} fetched | live {n_live} | dead/no-data {n_dead}")
    print(f"  P/B present: {has_pb}/{len(allrows)} ({100*has_pb/len(allrows):.0f}%)")
    print(f"  ROE present: {has_roe}/{len(allrows)} ({100*has_roe/len(allrows):.0f}%)")
    print(f"  P/B AND ROE: {both}/{len(allrows)} ({100*both/len(allrows):.0f}%)")
    print(f"  dead tickers: {dead}")

    cols = ["ticker", "name", "region", "sub_group", "country", "marketCap",
            "priceToBook", "trailingPE", "dividendYield_pct", "roe", "roa",
            "combined_score", "trap_status"]
    for reg in ["EM", "DEV_EXUS", "US"]:
        sub = ranked[ranked["region"] == reg].head(15)
        print(f"\n===== TOP {reg} (rankable) =====")
        print(sub[cols].to_string(index=False))


if __name__ == "__main__":
    main()
