#!/usr/bin/env python3
"""
universe.py — assemble the global screening universe for the Stage 1b quant screen.

Three buckets, all liquid mid/large caps, cited sources:
  1. US        — S&P 500 constituents (scraped from Wikipedia, cited) → GICS sector attached.
  2. DEV_EXUS  — curated large developed-market ex-US names (native Yahoo suffixes / ADRs).
  3. EM_CORE   — curated large emerging-market names reachable via ADRs / major suffixes.

Plus EM_STRESS — a separate ~40-name mixed EM batch used ONLY to measure yfinance field
completeness (the paid-API decision), NOT part of the ranked screen unless a name also
qualifies.

Everything is a real, static, reproducible list. yfinance is the fundamentals source;
GICS sectors for US come from Wikipedia; for ex-US/EM we rely on yfinance's own `sector`.
No fundamentals are invented here — this file only produces tickers + region tags.
"""
from __future__ import annotations
import io
import os
import pandas as pd
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
CACHE = os.path.join(DATA, "cache")
UA = {"User-Agent": "Mozilla/5.0 (fin-research; hshariati@adobe.com)"}
SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def get_sp500() -> pd.DataFrame:
    """Return S&P 500 constituents with GICS sector. Cached to data/cache/sp500.csv."""
    cpath = os.path.join(CACHE, "sp500.csv")
    if os.path.exists(cpath):
        return pd.read_csv(cpath)
    r = requests.get(SP500_URL, headers=UA, timeout=30)
    r.raise_for_status()
    df = pd.read_html(io.StringIO(r.text))[0]
    out = df[["Symbol", "Security", "GICS Sector"]].rename(
        columns={"Symbol": "ticker", "Security": "name", "GICS Sector": "gics_sector"})
    out["ticker"] = out["ticker"].str.replace(".", "-", regex=False)  # BRK.B -> BRK-B (Yahoo)
    os.makedirs(CACHE, exist_ok=True)
    out.to_csv(cpath, index=False)
    return out


# --- Curated developed ex-US large caps (Yahoo suffix or US ADR). region = "DEV_EXUS" ---
# Chosen for liquidity + coverage; sector attached from yfinance at fetch time.
DEV_EXUS = [
    # Europe (native listings)
    "NESN.SW", "ROG.SW", "NOVN.SW", "ZURN.SW", "UHR.SW", "ABBN.SW",  # Switzerland
    "SAP.DE", "SIE.DE", "ALV.DE", "MBG.DE", "BMW.DE", "BAS.DE", "DTE.DE", "MUV2.DE", "ADS.DE",  # Germany
    "MC.PA", "OR.PA", "AIR.PA", "SU.PA", "SAN.PA", "BNP.PA", "AI.PA", "RMS.PA", "EL.PA", "TTE.PA",  # France
    "ASML.AS", "PRX.AS", "AD.AS", "HEIA.AS",  # Netherlands
    "SHEL.L", "AZN.L", "ULVR.L", "HSBA.L", "BP.L", "GSK.L", "DGE.L", "RIO.L", "BATS.L", "REL.L",  # UK
    "NOVO-B.CO", "DSV.CO",  # Denmark
    "NDA-SE.ST", "ATCO-A.ST", "VOLV-B.ST",  # Sweden
    "SAN.MC", "IBE.MC", "ITX.MC",  # Spain
    "ENEL.MI", "ISP.MI", "ENI.MI",  # Italy
    "NOKIA.HE",  # Finland
    # Developed Asia / Pacific
    "7203.T", "6758.T", "9984.T", "8306.T", "6861.T", "9432.T", "6098.T",  # Japan
    "0700.HK", "0941.HK", "0005.HK", "1299.HK",  # Hong Kong (large caps; some China)
    "CBA.AX", "BHP.AX", "CSL.AX", "NAB.AX", "WES.AX",  # Australia
    "005930.KS", "000660.KS",  # South Korea (Samsung, SK Hynix) - dev/EM borderline
    "SU.TO", "RY.TO", "SHOP.TO", "CNR.TO", "ENB.TO",  # Canada
    # Developed-market ADRs on US exchanges (bare tickers)
    "TM", "SONY", "NVO", "ASML", "SAP", "UL", "AZN", "SHEL", "BP", "HSBC",
    "DEO", "SNY", "TTE", "BTI", "RIO", "BBVA", "ING", "MUFG", "SMFG", "HMC",
]

# --- Curated EM large caps (ADRs / major exchange suffixes). region = "EM_CORE" ---
EM_CORE = [
    # China ADRs + HK
    "BABA", "PDD", "JD", "BIDU", "NTES", "TCOM", "LI", "YUMC", "9988.HK", "3690.HK",
    # Taiwan
    "TSM", "UMC", "2330.TW", "2317.TW",
    # India (ADR + NSE)
    "INFY", "WIT", "HDB", "IBN", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "INFY.NS", "ITC.NS", "LT.NS", "HINDUNILVR.NS",
    # Latin America
    "VALE", "PBR", "ITUB", "BBD", "ABEV", "MELI", "GGB", "BSBR", "AMX", "FMX",
    # Other EM
    "SHG", "KB", "PKX",  # Korea ADRs
    "GRMN",  # (Taiwan-founded, US-listed) — will tag by yfinance country
    "SBSW", "GOLD",  # mining EM-exposed
    "TLK",  # Indonesia telecom ADR
]

# --- EM breadth STRESS TEST: ~40 mixed EM tickers to measure field completeness ---
# Deliberately reaches below the mega-caps and into local-only listings to expose gaps.
EM_STRESS = [
    # India NSE mid/large (local)
    "MARUTI.NS", "AXISBANK.NS", "SUNPHARMA.NS", "TITAN.NS", "BAJFINANCE.NS",
    "ASIANPAINT.NS", "NESTLEIND.NS", "WIPRO.NS", "TATAMOTORS.NS", "ADANIENT.NS",
    # China / HK
    "0857.HK", "0386.HK", "1288.HK", "2318.HK", "1810.HK", "0175.HK",
    # Taiwan (local)
    "2454.TW", "2412.TW", "2882.TW", "1301.TW",
    # Brazil (local B3, .SA)
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "WEGE3.SA", "MGLU3.SA",
    # Mexico
    "GFNORTEO.MX", "WALMEX.MX", "GMEXICOB.MX",
    # South Africa (JSE .JO)
    "NPN.JO", "FSR.JO", "SOL.JO", "MTN.JO",
    # Indonesia (.JK), Thailand (.BK), Malaysia (.KL), Turkey (.IS), Saudi (.SR)
    "BBCA.JK", "BBRI.JK", "PTT.BK", "MAYBANK.KL", "THYAO.IS", "2222.SR",
    # Poland, Greece
    "PKO.WA", "OPAP.AT",
]


def build_universe() -> pd.DataFrame:
    """Return the full screening universe (US + DEV_EXUS + EM_CORE) with region tags."""
    sp = get_sp500()
    sp = sp.assign(region="US")
    dev = pd.DataFrame({"ticker": DEV_EXUS, "name": None, "gics_sector": None,
                        "region": "DEV_EXUS"})
    em = pd.DataFrame({"ticker": EM_CORE, "name": None, "gics_sector": None,
                       "region": "EM_CORE"})
    uni = pd.concat([sp, dev, em], ignore_index=True)
    uni = uni.drop_duplicates(subset="ticker").reset_index(drop=True)
    return uni


if __name__ == "__main__":
    u = build_universe()
    print(f"Universe: {len(u)} names")
    print(u["region"].value_counts().to_string())
    print(f"EM_STRESS batch: {len(EM_STRESS)} names (separate, for coverage test)")
    out = os.path.join(CACHE, "universe.csv")
    u.to_csv(out, index=False)
    print(f"Wrote {out}")
