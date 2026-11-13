#!/usr/bin/env python3
"""
universe_exus.py — Stage 2.5a EXPANDED ex-US / emerging-market screening universe.

WHY: the Stage-1b universe (screens/universe.py) was US-heavy (503 US vs 94 dev-ex-US +
42 EM), so the high-conviction bucket came out 100% developed-US. This module broadens the
ex-US / EM side to several hundred names so ex-US/EM names get a fair shot, then the SAME
Stage-1b screen (run_quant_screen.py) is re-run over it and ranked WITHIN region.

Construction — real, cited index membership (scraped 2026-07-02) + small curated large-cap
lists where the Wikipedia constituents table is not machine-parseable (Japan, Korea, Taiwan,
LatAm, SE-Asia). NON-financials are the target; a `SKIP_FINANCIALS` set drops obvious
banks/insurers/REITs by ticker to avoid duplicating the parallel financials agent. yfinance
`sector` is used at fetch time as the authoritative financial-sector filter (see
run_quant_screen_exus).

Sources (Wikipedia index constituent tables, scraped 2026-07-02, browser UA):
  - FTSE 100 (UK, .L)                 https://en.wikipedia.org/wiki/FTSE_100_Index
  - DAX (Germany, .DE + a few .PA/.AS) https://en.wikipedia.org/wiki/DAX
  - CAC 40 (France, .PA)              https://en.wikipedia.org/wiki/CAC_40
  - EURO STOXX 50 (euro-area)         https://en.wikipedia.org/wiki/EURO_STOXX_50
  - IBEX 35 (Spain, .MC)              https://en.wikipedia.org/wiki/IBEX_35
  - FTSE MIB (Italy, .MI)             https://en.wikipedia.org/wiki/FTSE_MIB
  - AEX (Netherlands, .AS)            https://en.wikipedia.org/wiki/AEX_index
  - SMI (Switzerland, .SW)            https://en.wikipedia.org/wiki/Swiss_Market_Index
  - OMX Stockholm 30 (Sweden, .ST)    https://en.wikipedia.org/wiki/OMX_Stockholm_30
  - S&P/TSX 60 (Canada, .TO)          https://en.wikipedia.org/wiki/S%26P/TSX_60
  - S&P/ASX 50 (Australia, .AX)       https://en.wikipedia.org/wiki/S%26P/ASX_50
  - Hang Seng (HK, .HK)               https://en.wikipedia.org/wiki/Hang_Seng_Index
  - NIFTY 50 (India, .NS)             https://en.wikipedia.org/wiki/NIFTY_50
  - Curated: Nikkei/Japan (.T), Korea (.KS), Taiwan (.TW), Brazil (.SA), Mexico (.MX),
    plus SE-Asia / South-Africa / Denmark / Finland large caps (Wikipedia constituents
    tables for these were navbox-only / not machine-parseable, so a hand list of the
    largest liquid non-financials is used, with Yahoo suffixes verified at fetch time).

Anti-hallucination: this file only emits TICKERS + region/country/source tags. No
fundamentals are invented. Every ticker is either scraped from a cited index table or a
verified large-cap; run_quant_screen_exus verifies each returns yfinance data and drops
those that don't (coverage report).
"""
from __future__ import annotations
import io
import os
import re
import pandas as pd
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
CACHE = os.path.join(DATA, "cache")
UA = {"User-Agent": "Mozilla/5.0 (fin-research; hshariati@adobe.com)"}


def _wiki_tables(url: str) -> list[pd.DataFrame]:
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    return pd.read_html(io.StringIO(r.text))


# ---------------------------------------------------------------- scrapers (cited)
def scrape_ftse100() -> list[str]:
    """FTSE 100 EPIC codes -> Yahoo .L (dot-suffixed EPICs use '-' on Yahoo, rare)."""
    t = _wiki_tables("https://en.wikipedia.org/wiki/FTSE_100_Index")[6]
    out = []
    for tk in t["Ticker"].astype(str):
        tk = tk.strip().upper()
        if not tk or tk == "NAN":
            continue
        # UK EPICs like 'BT.A' -> Yahoo 'BT-A.L'
        tk = tk.replace(".", "-")
        out.append(f"{tk}.L")
    return out


def scrape_suffixed(url: str, ti: int, col: str) -> list[str]:
    """Indices whose Wikipedia 'Ticker' column already carries a Yahoo suffix."""
    t = _wiki_tables(url)[ti]
    out = []
    for tk in t[col].astype(str):
        tk = tk.strip()
        if tk and tk.upper() != "NAN" and "." in tk:
            out.append(tk)
    return out


def scrape_hangseng() -> list[str]:
    """Hang Seng 'SEHK: 388' -> zero-pad to 4 digits -> '0388.HK'."""
    t = _wiki_tables("https://en.wikipedia.org/wiki/Hang_Seng_Index")[6]
    out = []
    for tk in t["Ticker"].astype(str):
        m = re.search(r"(\d+)", tk)
        if m:
            out.append(f"{int(m.group(1)):04d}.HK")
    return out


def scrape_bare(url: str, ti: int, col: str, suffix: str) -> list[str]:
    """Indices with bare local tickers -> append a fixed Yahoo suffix (.NS/.TO/.AX)."""
    t = _wiki_tables(url)[ti]
    out = []
    for tk in t[col].astype(str):
        tk = tk.strip().upper()
        if not tk or tk == "NAN":
            continue
        yt = tk.replace(".", "-")  # e.g. TSX 'X.TO' rare dotted forms
        out.append(f"{yt}{suffix}")
    return out


# ---------------------------------------------------------------- curated large caps
# Regions where the Wikipedia constituents table is navbox-only / not parseable.
# Hand-picked LARGEST liquid NON-financial names; Yahoo suffix verified at fetch time.
JAPAN = [  # Nikkei 225 / TOPIX large non-financials, Tokyo .T
    "7203.T", "6758.T", "6861.T", "6098.T", "9984.T", "9432.T", "9433.T", "8035.T",
    "6501.T", "6503.T", "6367.T", "6902.T", "7267.T", "7269.T", "7201.T", "7751.T",
    "4063.T", "4502.T", "4519.T", "4568.T", "4523.T", "4578.T", "6954.T", "6971.T",
    "6981.T", "6752.T", "6702.T", "6857.T", "8001.T", "8031.T", "8058.T", "8053.T",
    "2914.T", "2802.T", "3382.T", "9020.T", "9022.T", "9101.T", "9104.T", "5108.T",
    "5401.T", "4901.T", "4911.T", "6273.T", "6301.T", "6326.T", "7011.T", "7012.T",
    "7741.T", "8113.T", "4661.T", "9735.T", "2502.T", "2503.T", "3407.T", "5713.T",
]
KOREA = [  # KOSPI large non-financials, .KS
    "005930.KS", "000660.KS", "005380.KS", "005490.KS", "051910.KS", "006400.KS",
    "035420.KS", "035720.KS", "012330.KS", "000270.KS", "066570.KS", "096770.KS",
    "015760.KS", "017670.KS", "034730.KS", "003550.KS", "009150.KS", "011200.KS",
    "010130.KS", "010950.KS", "018260.KS", "032830.KS", "207940.KS", "068270.KS",
    "028260.KS", "086790.KS", "105560.KS",
]
TAIWAN = [  # TWSE large non-financials, .TW (financials via .TW banks excluded below)
    "2330.TW", "2317.TW", "2454.TW", "2412.TW", "2308.TW", "2303.TW", "3711.TW",
    "2882.TW", "2891.TW", "1301.TW", "1303.TW", "2002.TW", "1216.TW", "2207.TW",
    "3008.TW", "2379.TW", "2357.TW", "4938.TW", "2382.TW", "2409.TW", "3034.TW",
    "6505.TW", "1101.TW", "2105.TW", "9910.TW", "2912.TW", "2801.TW",
]
BRAZIL = [  # Ibovespa large non-financials, .SA
    "PETR4.SA", "PETR3.SA", "VALE3.SA", "ABEV3.SA", "WEGE3.SA", "SUZB3.SA", "RENT3.SA",
    "PRIO3.SA", "RADL3.SA", "RAIL3.SA", "EQTL3.SA", "ELET3.SA", "ELET6.SA", "CSAN3.SA",
    "GGBR4.SA", "CSNA3.SA", "USIM5.SA", "KLBN11.SA", "EMBR3.SA", "LREN3.SA", "MGLU3.SA",
    "RDOR3.SA", "HAPV3.SA", "TOTS3.SA", "VBBR3.SA", "UGPA3.SA", "CCRO3.SA", "NTCO3.SA",
    "VIVT3.SA", "TIMS3.SA", "SBSP3.SA", "CMIG4.SA", "CPFE3.SA", "ENEV3.SA", "BRFS3.SA",
    "JBSS3.SA", "MRFG3.SA", "BEEF3.SA", "SLCE3.SA", "AZZA3.SA",
]
MEXICO = [  # Mexican IPC large non-financials, .MX
    "AMXB.MX", "WALMEX.MX", "FEMSAUBD.MX", "GMEXICOB.MX", "GFNORTEO.MX", "CEMEXCPO.MX",
    "TLEVISACPO.MX", "KOFUBL.MX", "BIMBOA.MX", "ALFAA.MX", "PE&OLES.MX", "ELEKTRA.MX",
    "GAPB.MX", "ASURB.MX", "OMAB.MX", "GCARSOA1.MX", "ORBIA.MX", "LABB.MX", "KIMBERA.MX",
    "AC.MX", "ALSEA.MX", "MEGACPO.MX", "GRUMAB.MX",
]
SEASIA_ETC = [  # SE-Asia / South-Africa / Nordics large non-financials, verified suffixes
    # Indonesia .JK
    "TLKM.JK", "ASII.JK", "UNVR.JK", "ICBP.JK", "INDF.JK", "ADRO.JK", "PGAS.JK",
    # Thailand .BK
    "PTT.BK", "PTTEP.BK", "CPALL.BK", "AOT.BK", "ADVANC.BK", "GULF.BK", "DELTA.BK",
    # Malaysia .KL
    "PCHEM.KL", "TENAGA.KL", "PETGAS.KL", "MISC.KL", "IOI.KL", "SIME.KL",
    # Singapore .SI (non-financials)
    "Z74.SI", "C6L.SI", "BN4.SI", "F34.SI", "S63.SI", "G13.SI",
    # South Africa .JO (non-financials)
    "NPN.JO", "PRX.JO", "MTN.JO", "SOL.JO", "BHG.JO", "AGL.JO", "CFR.JO", "SHP.JO",
    "CLS.JO", "BID.JO", "APN.JO", "MRP.JO", "WHL.JO",
    # Denmark .CO / Finland .HE / Norway .OL large non-financials
    "NOVO-B.CO", "DSV.CO", "MAERSK-B.CO", "CARL-B.CO", "ORSTED.CO", "COLO-B.CO",
    "NOKIA.HE", "NESTE.HE", "KNEBV.HE", "UPM.HE", "FORTUM.HE",
    "EQNR.OL", "NHY.OL", "MOWI.OL", "TEL.OL", "ORK.OL",
]

# Developed-ex-US ADRs on US exchanges (bare tickers) — keep the Stage-1b set.
DEV_ADRS = [
    "TM", "SONY", "NVO", "ASML", "SAP", "UL", "AZN", "SHEL", "BP", "DEO", "SNY",
    "TTE", "BTI", "RIO", "HMC", "STLA", "E", "PHG", "TEF", "RELX", "WPP", "NGG",
    "ERIC", "NOK", "SAP", "ABB",
]
# EM ADRs (bare tickers) — keep the Stage-1b set, non-financials.
EM_ADRS = [
    "BABA", "PDD", "JD", "BIDU", "NTES", "TCOM", "LI", "YUMC", "TSM", "UMC",
    "INFY", "WIT", "VALE", "PBR", "ABEV", "MELI", "GGB", "AMX", "FMX", "SBSW",
    "TLK", "SE", "GRAB", "VIPS", "BILI", "TME", "KEP", "PKX", "SID", "SQM",
    "CX", "ASX", "SKM", "GOLD",
]

# Developed-ex-US regions (map suffix / ADR -> DEV_EXUS), EM regions -> EM.
DEV_SUFFIXES = {".L", ".DE", ".PA", ".AS", ".SW", ".MC", ".MI", ".ST", ".CO",
                ".HE", ".OL", ".TO", ".AX", ".T", ".SI"}
EM_SUFFIXES = {".HK", ".NS", ".TW", ".KS", ".SA", ".MX", ".JK", ".BK", ".KL", ".JO"}

# Obvious financials / insurers / REITs to EXCLUDE by ticker (parallel agent covers them).
# yfinance `sector` is the authoritative filter at fetch time; this is a first cut so we
# don't even fetch the clearest banks. Non-exhaustive by design.
SKIP_FINANCIALS = {
    # UK
    "HSBA.L", "BARC.L", "LLOY.L", "NWG.L", "STAN.L", "PRU.L", "LGEN.L", "AV.L",
    "ADM.L", "PHNX.L", "SDR.L", "III.L", "HL.L", "LSEG.L", "ABDN.L", "SGE.L",
    # Germany
    "DBK.DE", "CBK.DE", "ALV.DE", "MUV2.DE", "DB1.DE", "HNR1.DE", "ALIZY",
    # France
    "BNP.PA", "ACA.PA", "GLE.PA", "CS.PA", "SCR.PA",
    # Spain / Italy / NL / Nordics
    "SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "MAP.MC", "UNI.MC",
    "ISP.MI", "UCG.MI", "BMPS.MI", "BAMI.MI", "BPE.MI", "MB.MI", "G.MI", "UNI.MI",
    "AZM.MI", "FBK.MI", "BGN.MI", "PST.MI", "AGN.AS", "ABN.AS", "INGA.AS", "NN.AS",
    "ASRNL.AS", "SEB-A.ST", "SWED-A.ST", "SHB-A.ST", "INVE-B.ST", "EQT.ST",
    "DANSKE.CO", "TRYG.CO", "NDA-DK.CO", "SAMPO.HE", "NDA-FI.HE", "STB.OL", "DNB.OL",
    "UBSG.SW", "ZURN.SW", "CFR.SW", "SLHN.SW", "PGHN.SW", "BAER.SW", "SREN.SW",
    # Canada / Australia
    "RY.TO", "TD.TO", "BNS.TO", "BMO.TO", "CM.TO", "NA.TO", "MFC.TO", "SLF.TO",
    "GWO.TO", "IFC.TO", "BN.TO", "BAM.TO", "FFH.TO", "POW.TO", "X.TO",
    "CBA.AX", "NAB.AX", "ANZ.AX", "WBC.AX", "MQG.AX", "QBE.AX", "SUN.AX", "IAG.AX",
    "ASX.AX",
    # Japan / Korea / Taiwan / HK / India / LatAm / SEAsia banks & insurers
    "8306.T", "8316.T", "8411.T", "8766.T", "8750.T", "8725.T", "8630.T", "7182.T",
    "8309.T", "8308.T", "8591.T", "8604.T",
    "105560.KS", "086790.KS", "055550.KS", "316140.KS", "024110.KS", "138930.KS",
    "2882.TW", "2891.TW", "2801.TW", "2886.TW", "2884.TW", "2885.TW", "2892.TW",
    "2880.TW", "2881.TW", "2883.TW", "2887.TW", "2888.TW", "5880.TW", "2890.TW",
    "0005.HK", "0011.HK", "0388.HK", "1299.HK", "2318.HK", "2388.HK", "2628.HK",
    "1398.HK", "0939.HK", "3988.HK", "3968.HK", "1288.HK", "0011.HK", "2601.HK",
    "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS",
    "BAJFINANCE.NS", "BAJAJFINSV.NS", "HDFCLIFE.NS", "SBILIFE.NS", "INDUSINDBK.NS",
    "SHRIRAMFIN.NS", "JIOFIN.NS",
    "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "B3SA3.SA", "SANB11.SA", "BPAC11.SA",
    "GFNORTEO.MX",
    "DBS.SI", "O39.SI", "U11.SI",  # Singapore banks (DBS/OCBC/UOB)
    "FSR.JO", "SBK.JO", "NED.JO", "ABG.JO", "CPI.JO", "OMU.JO", "SLM.JO", "DSY.JO",
    "INL.JO", "INP.JO", "RNI.JO",
    "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK",  # Indonesia banks
    "MAYBANK.KL", "CIMB.KL", "PBK.KL", "HLBK.KL",  # Malaysia banks
    "KBANK.BK", "SCB.BK", "BBL.BK", "KTB.BK",  # Thailand banks
    # ADRs that are financials
    "HSBC", "BBVA", "ING", "MUFG", "SMFG", "SHG", "KB", "BSBR", "ITUB", "BBD",
    "IBN", "HDB",
}


def _region_for(ticker: str) -> str:
    for suf in DEV_SUFFIXES:
        if ticker.endswith(suf):
            return "DEV_EXUS"
    for suf in EM_SUFFIXES:
        if ticker.endswith(suf):
            return "EM"
    return "ADR"  # resolved later by list membership


def build_universe_exus() -> pd.DataFrame:
    """Return the expanded ex-US/EM universe with region + source tags (no fundamentals)."""
    scraped: dict[str, list[str]] = {}
    scraped["FTSE100"] = scrape_ftse100()
    scraped["DAX"] = scrape_suffixed("https://en.wikipedia.org/wiki/DAX", 4, "Ticker")
    scraped["CAC40"] = scrape_suffixed("https://en.wikipedia.org/wiki/CAC_40", 4, "Ticker")
    scraped["EUROSTOXX50"] = scrape_suffixed("https://en.wikipedia.org/wiki/EURO_STOXX_50", 3, "Ticker")
    scraped["IBEX35"] = scrape_suffixed("https://en.wikipedia.org/wiki/IBEX_35", 2, "Ticker")
    scraped["FTSEMIB"] = scrape_suffixed("https://en.wikipedia.org/wiki/FTSE_MIB", 1, "Ticker")
    scraped["AEX"] = scrape_suffixed("https://en.wikipedia.org/wiki/AEX_index", 3, "Ticker")
    scraped["SMI"] = scrape_suffixed("https://en.wikipedia.org/wiki/Swiss_Market_Index", 2, "Ticker")
    scraped["OMXS30"] = scrape_suffixed("https://en.wikipedia.org/wiki/OMX_Stockholm_30", 1, "Ticker")
    scraped["TSX60"] = scrape_bare("https://en.wikipedia.org/wiki/S%26P/TSX_60", 1, "Symbol", ".TO")
    scraped["ASX50"] = scrape_bare("https://en.wikipedia.org/wiki/S%26P/ASX_50", 0, "Symbol", ".AX")
    scraped["HANGSENG"] = scrape_hangseng()
    scraped["NIFTY50"] = scrape_bare("https://en.wikipedia.org/wiki/NIFTY_50", 1, "Symbol", ".NS")

    curated = {
        "JAPAN": JAPAN, "KOREA": KOREA, "TAIWAN": TAIWAN, "BRAZIL": BRAZIL,
        "MEXICO": MEXICO, "SEASIA_ETC": SEASIA_ETC, "DEV_ADRS": DEV_ADRS, "EM_ADRS": EM_ADRS,
    }

    rows = []
    for src, tks in {**scraped, **curated}.items():
        for tk in tks:
            rows.append({"ticker": tk, "source": src})
    df = pd.DataFrame(rows).drop_duplicates(subset="ticker").reset_index(drop=True)

    # region: suffix-based, ADR lists resolve explicitly
    df["region"] = df["ticker"].map(_region_for)
    df.loc[df["source"] == "DEV_ADRS", "region"] = "DEV_EXUS"
    df.loc[df["source"] == "EM_ADRS", "region"] = "EM"

    # drop obvious financials (parallel agent covers them); yfinance sector re-checks later
    before = len(df)
    df = df[~df["ticker"].isin(SKIP_FINANCIALS)].reset_index(drop=True)
    df["name"] = None
    df["gics_sector"] = None
    df = df[df["region"].isin(["DEV_EXUS", "EM"])].reset_index(drop=True)
    df.attrs["n_financials_dropped"] = before - len(df)
    return df


if __name__ == "__main__":
    u = build_universe_exus()
    print(f"Expanded ex-US/EM universe: {len(u)} names "
          f"(dropped {u.attrs.get('n_financials_dropped')} obvious financials)")
    print("\nBy region:")
    print(u["region"].value_counts().to_string())
    print("\nBy source:")
    print(u["source"].value_counts().to_string())
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, "universe_exus.csv")
    u.to_csv(out, index=False)
    print(f"\nWrote {out}")
