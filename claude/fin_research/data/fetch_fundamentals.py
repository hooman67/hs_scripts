#!/usr/bin/env python3
"""
fetch_fundamentals.py — per-company fundamentals for the value screen.

Two data layers, both FREE:
  1. yfinance  — price, market cap, and a wide set of current ratios/fundamentals.
                 Works GLOBALLY (US, Europe, Asia, EM) via Yahoo's exchange suffixes
                 (e.g. NESN.SW, SAP.DE, RELIANCE.NS, 0700.HK). Verified 2026-07-01.
  2. SEC EDGAR — primary financials (Revenues, NetIncome, Assets, ...) from XBRL
                 company-facts. Ground truth, but US-listed filers ONLY.

Anti-hallucination rules honored here:
  - Every value carries its source ("yfinance" / "edgar") and an as_of date.
  - Missing yfinance fields are left as None and flagged in `_missing` — NEVER fabricated.
  - Results are cached to data/cache/ so re-runs are reproducible and offline-friendly.

Usage
-----
    # pull a list of tickers (yfinance for all; EDGAR primary financials for US names)
    /opt/venv/bin/python3 data/fetch_fundamentals.py AAPL SAP NESN.SW TSM INFY

    # from a file (one ticker per line), and force fresh (ignore cache)
    /opt/venv/bin/python3 data/fetch_fundamentals.py --file tickers.txt --refresh

    # skip the (slower) EDGAR pull
    /opt/venv/bin/python3 data/fetch_fundamentals.py AAPL MSFT --no-edgar

Importable API (later stages call these):
    from fetch_fundamentals import get_fundamentals, get_edgar_financials, fetch_many
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

import pandas as pd
import requests
import yfinance as yf

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(HERE, "cache")
EDGAR_UA = {"User-Agent": "Hooman Shariati hshariati@adobe.com"}
CACHE_TTL_SECONDS = 12 * 3600  # prices move intraday; re-pull if cache older than 12h

# yfinance .info fields we harvest. Kept explicit so the schema is stable for later stages.
YF_FIELDS = [
    "shortName", "longName", "currency", "sector", "industry", "country", "exchange",
    "currentPrice", "regularMarketPrice", "marketCap", "enterpriseValue",
    "trailingPE", "forwardPE", "priceToBook", "priceToSalesTrailing12Months",
    "enterpriseToEbitda", "enterpriseToRevenue", "pegRatio",
    "returnOnEquity", "returnOnAssets",
    "grossMargins", "operatingMargins", "profitMargins", "ebitdaMargins",
    "revenueGrowth", "earningsGrowth",
    "debtToEquity", "totalDebt", "totalCash", "quickRatio", "currentRatio",
    "freeCashflow", "operatingCashflow",
    "trailingEps", "forwardEps", "bookValue",
    "dividendYield", "payoutRatio", "beta",
]

# EDGAR XBRL concepts we pull (with sensible fallbacks).
# us-gaap tags for domestic filers; ifrs-full tags for US-listed foreign filers (20-F).
EDGAR_CONCEPTS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                "SalesRevenueNet"],
    "net_income": ["NetIncomeLoss"],
    "operating_income": ["OperatingIncomeLoss"],
    "assets": ["Assets"],
    "liabilities": ["Liabilities"],
    "stockholders_equity": ["StockholdersEquity",
                            "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "long_term_debt": ["LongTermDebtNoncurrent", "LongTermDebt"],
}
IFRS_CONCEPTS = {
    "revenue": ["Revenue", "RevenueFromContractsWithCustomers"],
    "net_income": ["ProfitLoss", "ProfitLossAttributableToOwnersOfParent"],
    "operating_income": ["ProfitLossFromOperatingActivities"],
    "assets": ["Assets"],
    "liabilities": ["Liabilities"],
    "stockholders_equity": ["Equity", "EquityAttributableToOwnersOfParent"],
    "cash": ["CashAndCashEquivalents"],
    "long_term_debt": ["NoncurrentBorrowings", "Borrowings"],
}
ANNUAL_FORMS = ("10-K", "10-K/A", "20-F", "20-F/A")

_TICKER_CIK_CACHE: dict[str, str] | None = None


# --------------------------------------------------------------------------- utils
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _cache_path(kind: str, ticker: str) -> str:
    safe = ticker.replace("/", "_").replace(".", "_").upper()
    return os.path.join(CACHE_DIR, f"{kind}_{safe}.json")


def _read_cache(path: str, refresh: bool) -> dict | None:
    if refresh or not os.path.exists(path):
        return None
    if time.time() - os.path.getmtime(path) > CACHE_TTL_SECONDS:
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def _write_cache(path: str, obj: dict) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=str)


# --------------------------------------------------------------------------- yfinance
def get_fundamentals(ticker: str, refresh: bool = False) -> dict:
    """Return a dict of yfinance fundamentals for one ticker.

    Always includes: ticker, source, as_of, and every YF_FIELDS key (None if missing).
    `_missing` lists the fields Yahoo did not provide (so downstream can be honest).
    Never fabricates values.
    """
    cpath = _cache_path("yf", ticker)
    cached = _read_cache(cpath, refresh)
    if cached is not None:
        return cached

    out: dict = {"ticker": ticker, "source": "yfinance", "as_of": _now_iso(),
                 "error": None}
    try:
        info = yf.Ticker(ticker).info or {}
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"
        info = {}

    missing = []
    for f in YF_FIELDS:
        v = info.get(f)
        if v in (None, "", "Infinity"):
            v = None
            missing.append(f)
        out[f] = v
    out["_missing"] = missing
    # a couple of convenience derived fields (only if inputs exist — else None)
    fcf, mcap = out.get("freeCashflow"), out.get("marketCap")
    out["fcf_yield"] = (fcf / mcap) if (fcf and mcap) else None
    ev, ebitda_m = out.get("enterpriseValue"), out.get("ebitdaMargins")
    out["earnings_yield_ebit_ev"] = None  # needs EBIT/EV; left for EDGAR-backed calc later

    if not out["error"]:
        _write_cache(cpath, out)
    return out


# --------------------------------------------------------------------------- EDGAR
def _load_ticker_cik_map() -> dict[str, str]:
    global _TICKER_CIK_CACHE
    if _TICKER_CIK_CACHE is not None:
        return _TICKER_CIK_CACHE
    cpath = os.path.join(CACHE_DIR, "sec_ticker_cik_map.json")
    cached = _read_cache(cpath, refresh=False)
    if cached is not None:
        _TICKER_CIK_CACHE = cached
        return cached
    try:
        r = requests.get("https://www.sec.gov/files/company_tickers.json",
                         headers=EDGAR_UA, timeout=30)
        r.raise_for_status()
        raw = r.json()
        m = {v["ticker"].upper(): str(v["cik_str"]).zfill(10) for v in raw.values()}
        _write_cache(cpath, m)
        _TICKER_CIK_CACHE = m
        return m
    except Exception as e:
        print(f"  [WARN] could not load SEC ticker->CIK map: {e}")
        _TICKER_CIK_CACHE = {}
        return {}


def get_edgar_financials(ticker: str, refresh: bool = False, n_years: int = 4) -> dict:
    """Pull primary annual financials from SEC EDGAR XBRL company-facts.

    US-listed filers ONLY. Returns {'available': False, 'reason': ...} for names EDGAR
    doesn't cover (e.g. foreign issuers like Nestle). Values are as-reported (ground truth).
    """
    cpath = _cache_path("edgar", ticker)
    cached = _read_cache(cpath, refresh)
    if cached is not None:
        return cached

    out: dict = {"ticker": ticker, "source": "edgar", "as_of": _now_iso(),
                 "available": False, "reason": None, "cik": None, "annual": {}}
    cikmap = _load_ticker_cik_map()
    cik = cikmap.get(ticker.upper())
    if cik is None:
        out["reason"] = "ticker not in SEC EDGAR (likely non-US-listed)"
        return out  # not cached negative-with-reason? cache it to avoid re-hitting map
    out["cik"] = cik
    try:
        r = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
                         headers=EDGAR_UA, timeout=45)
        r.raise_for_status()
        all_facts = r.json().get("facts", {})
    except Exception as e:
        out["reason"] = f"EDGAR fetch error: {type(e).__name__}: {e}"
        return out

    # pick taxonomy: domestic filers use us-gaap; US-listed foreign filers use ifrs-full
    if all_facts.get("us-gaap"):
        facts, concepts, taxonomy = all_facts["us-gaap"], EDGAR_CONCEPTS, "us-gaap"
    elif all_facts.get("ifrs-full"):
        facts, concepts, taxonomy = all_facts["ifrs-full"], IFRS_CONCEPTS, "ifrs-full"
    else:
        out["reason"] = "no us-gaap or ifrs-full facts (no XBRL company-facts)"
        _write_cache(cpath, out)
        return out
    out["taxonomy"] = taxonomy

    def latest_annual(concept_tags: list[str]) -> list[dict]:
        for tag in concept_tags:
            node = facts.get(tag)
            if not node:
                continue
            units = node.get("units", {})
            # prefer USD; otherwise fall back to whatever unit exists, but RECORD it
            unit = "USD" if "USD" in units else next(iter(units), None)
            series = units.get(unit, [])
            # annual figures (10-K / 20-F), dedup by fiscal-year-end date, take the latest n
            rows = {}
            for u in series:
                if u.get("form") in ANNUAL_FORMS and u.get("end"):
                    rows[u["end"]] = {"end": u["end"], "val": u.get("val"),
                                      "fy": u.get("fy"), "tag": tag, "unit": unit}
            if rows:
                return sorted(rows.values(), key=lambda x: x["end"])[-n_years:]
        return []

    for name, tags in concepts.items():
        out["annual"][name] = latest_annual(tags)
    out["available"] = any(out["annual"][k] for k in out["annual"])
    if not out["available"]:
        out["reason"] = "no matching us-gaap concepts found"
    _write_cache(cpath, out)
    return out


# --------------------------------------------------------------------------- driver
def fetch_many(tickers: list[str], do_edgar: bool = True, refresh: bool = False
               ) -> tuple[pd.DataFrame, dict]:
    """Fetch yfinance (all) + EDGAR (US names) for a list. Returns (summary_df, edgar_dict)."""
    rows, edgar = [], {}
    for tk in tickers:
        fun = get_fundamentals(tk, refresh=refresh)
        row = {k: fun.get(k) for k in
               ["ticker", "shortName", "currency", "country", "sector", "industry",
                "currentPrice", "marketCap", "trailingPE", "forwardPE", "priceToBook",
                "enterpriseToEbitda", "returnOnEquity", "returnOnAssets", "grossMargins",
                "operatingMargins", "profitMargins", "debtToEquity", "freeCashflow",
                "fcf_yield", "dividendYield", "as_of"]}
        row["yf_error"] = fun.get("error")
        row["n_missing_fields"] = len(fun.get("_missing", []))
        if do_edgar:
            ed = get_edgar_financials(tk, refresh=refresh)
            edgar[tk] = ed
            row["edgar_available"] = ed["available"]
            row["edgar_taxonomy"] = ed.get("taxonomy")
            if ed["available"]:
                rev = ed["annual"].get("revenue", [])
                row["edgar_latest_revenue_usd"] = rev[-1]["val"] if rev else None
                row["edgar_latest_fy_end"] = rev[-1]["end"] if rev else None
                row["edgar_reason"] = None
            else:
                row["edgar_reason"] = ed.get("reason")
        rows.append(row)
        time.sleep(0.15)  # be polite to EDGAR / Yahoo
    return pd.DataFrame(rows), edgar


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tickers", nargs="*", help="tickers, e.g. AAPL SAP NESN.SW TSM")
    ap.add_argument("--file", help="file with one ticker per line")
    ap.add_argument("--no-edgar", action="store_true", help="skip EDGAR primary financials")
    ap.add_argument("--refresh", action="store_true", help="ignore cache, fetch fresh")
    ap.add_argument("--out", help="write summary CSV to this path")
    args = ap.parse_args()

    tickers = list(args.tickers)
    if args.file:
        with open(args.file) as f:
            tickers += [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    if not tickers:
        ap.error("provide tickers on the command line or via --file")

    os.makedirs(CACHE_DIR, exist_ok=True)
    print(f"Fundamentals fetch — {_now_iso()}  ({len(tickers)} tickers)")
    df, edgar = fetch_many(tickers, do_edgar=not args.no_edgar, refresh=args.refresh)

    pd.set_option("display.width", 200, "display.max_columns", 40)
    show = ["ticker", "shortName", "currency", "marketCap", "trailingPE", "priceToBook",
            "enterpriseToEbitda", "returnOnEquity", "operatingMargins",
            "edgar_available", "n_missing_fields"]
    show = [c for c in show if c in df.columns]
    print("\n" + df[show].to_string(index=False))

    errs = df[df["yf_error"].notna()]
    if len(errs):
        print(f"\nyfinance errors on: {list(errs['ticker'])}")

    out = args.out or os.path.join(CACHE_DIR, "fundamentals_summary.csv")
    df.to_csv(out, index=False)
    print(f"\nWrote summary: {out}")
    print(f"Cache dir: {CACHE_DIR}  (per-ticker yf_*.json / edgar_*.json)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
