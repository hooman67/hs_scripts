#!/usr/bin/env python3
"""
financials_universe.py — global FINANCIALS screening universe (Stage 2.5b).

Banks, insurers (life / P&C / reinsurance / diversified), and diversified financials
(asset managers, exchanges, broker/insurance holdcos) across US, developed-ex-US
(Europe, UK, Japan, Canada, Australia), and EM (China/HK, India, Brazil, Mexico,
South Africa, SE Asia, Taiwan/Korea). REITs are collected as a SEPARATE optional
sub-group (they are valued on P/B + FFO, closer to financials than to the generic
gross-margin/EV-EBITDA screen).

WHY a separate universe: the Stage 1b generic screen (screens/universe.py + the
gross-margin / EV-EBITDA scorer) structurally CANNOT rank banks/insurers/REITs — they
have no gross margin and EV/EBITDA is meaningless for a balance-sheet business. So they
were dropped everywhere. Stage 1a flagged EM Life Insurance as one of the cheapest AND
highest-quality EM sectors (ROIC ~15%, ROE ~17.6%), so EM life insurers are a PRIORITY
here and are hand-listed with the big names.

Every ticker below is a real, static list with a cited source. yfinance is the
fundamentals source at fetch time; the run script VERIFIES each ticker returns data and
drops (logs) the ones that don't — no fabricated tickers survive.

Yahoo suffix conventions (VERIFIED in this project, data/README.md):
  US bare (JPM); .SW Swiss, .DE Xetra, .PA Paris, .AS Amsterdam, .L London, .MC Madrid,
  .MI Milan, .ST Stockholm, .CO Copenhagen, .HE Helsinki, .OL Oslo, .BR Brussels,
  .T Tokyo, .HK Hong Kong, .AX Australia, .KS/.KQ Korea, .TW Taiwan, .TO/.V Canada,
  .NS India NSE, .SA Brazil B3, .MX Mexico, .JO Johannesburg, .JK Jakarta, .BK Bangkok,
  .KL Kuala Lumpur, .SR Saudi. US-listed ADRs use the bare ADR ticker.

Sub-group tags (assigned here, refined from yfinance `industry` at fetch time):
  BANK, INSURER (life/P&C/reinsurance/diversified), DIVFIN (asset mgmt / exchange /
  broker / consumer finance), REIT.

Sources (cited, scraped/consulted 2026-07-02):
  - US: S&P 500 Financials + Real Estate GICS sectors (Wikipedia S&P 500 list, already
    cached from Stage 1b at data/cache/sp500.csv) — filtered to Financials/Real Estate.
  - Europe/UK/Japan/Canada/Australia/EM: curated from index constituents / reputable
    lists (STOXX Europe 600 Banks & Insurance, FTSE 100 financials, Nikkei/TOPIX banks,
    S&P/TSX financials, S&P/ASX 200 financials, and major-index EM financial leaders),
    Wikipedia index pages. Large-cap, liquid names only.
"""
from __future__ import annotations
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
CACHE = os.path.join(DATA, "cache")

# ---------------------------------------------------------------------------
# Curated NON-US financials. (ticker, sub_group_hint) — sub-group is refined from
# yfinance `industry` at fetch time; hint is the fallback / seed classification.
# ---------------------------------------------------------------------------

# ============================== DEVELOPED EX-US ==============================
DEV_EXUS_FIN = [
    # ---- UK (FTSE 100 financials) ----
    ("HSBA.L", "BANK"), ("BARC.L", "BANK"), ("LLOY.L", "BANK"), ("NWG.L", "BANK"),
    ("STAN.L", "BANK"),
    ("PRU.L", "INSURER"), ("AV.L", "INSURER"), ("LGEN.L", "INSURER"),
    ("ADM.L", "INSURER"), ("BEZ.L", "INSURER"), ("HSX.L", "INSURER"),
    ("III.L", "DIVFIN"), ("SDR.L", "DIVFIN"), ("ABDN.L", "DIVFIN"),
    ("LSEG.L", "DIVFIN"),
    # ---- Switzerland ----
    ("UBSG.SW", "BANK"), ("ZURN.SW", "INSURER"), ("SREN.SW", "INSURER"),
    ("SLHN.SW", "INSURER"), ("BAER.SW", "BANK"), ("PGHN.SW", "DIVFIN"),
    # ---- Germany ----
    ("DBK.DE", "BANK"), ("CBK.DE", "BANK"), ("ALV.DE", "INSURER"),
    ("MUV2.DE", "INSURER"), ("HNR1.DE", "INSURER"), ("DB1.DE", "DIVFIN"),
    # ---- France ----
    ("BNP.PA", "BANK"), ("GLE.PA", "BANK"), ("ACA.PA", "BANK"),
    ("CS.PA", "INSURER"), ("SCR.PA", "INSURER"), ("AMUN.PA", "DIVFIN"),
    # ---- Netherlands / Belgium ----
    ("INGA.AS", "BANK"), ("ABN.AS", "BANK"), ("NN.AS", "INSURER"),
    ("ASRNL.AS", "INSURER"), ("AGN.AS", "INSURER"), ("KBC.BR", "BANK"),
    ("AGS.BR", "INSURER"),
    # ---- Spain ----
    ("SAN.MC", "BANK"), ("BBVA.MC", "BANK"), ("CABK.MC", "BANK"),
    ("SAB.MC", "BANK"), ("BKT.MC", "BANK"), ("MAP.MC", "INSURER"),
    # ---- Italy ----
    ("ISP.MI", "BANK"), ("UCG.MI", "BANK"), ("BMPS.MI", "BANK"),
    ("G.MI", "INSURER"), ("BGN.MI", "DIVFIN"), ("MB.MI", "BANK"),
    # ---- Nordics ----
    ("NDA-SE.ST", "BANK"), ("SEB-A.ST", "BANK"), ("SHB-A.ST", "BANK"),
    ("SWED-A.ST", "BANK"), ("DANSKE.CO", "BANK"), ("DNB.OL", "BANK"),
    ("SAMPO.HE", "INSURER"), ("NDA-FI.HE", "BANK"), ("STB.OL", "INSURER"),
    ("TRYG.CO", "INSURER"),
    # ---- Japan (megabanks + insurers) ----
    ("8306.T", "BANK"), ("8316.T", "BANK"), ("8411.T", "BANK"),
    ("8309.T", "BANK"), ("8308.T", "BANK"),
    ("8766.T", "INSURER"), ("8725.T", "INSURER"), ("8630.T", "INSURER"),
    ("8750.T", "INSURER"), ("8795.T", "INSURER"),
    ("8604.T", "DIVFIN"), ("8591.T", "DIVFIN"), ("8697.T", "DIVFIN"),
    # ---- Canada (Big Six banks + lifecos) ----
    ("RY.TO", "BANK"), ("TD.TO", "BANK"), ("BNS.TO", "BANK"),
    ("BMO.TO", "BANK"), ("CM.TO", "BANK"), ("NA.TO", "BANK"),
    ("MFC.TO", "INSURER"), ("SLF.TO", "INSURER"), ("GWO.TO", "INSURER"),
    ("IFC.TO", "INSURER"), ("POW.TO", "DIVFIN"), ("BAM.TO", "DIVFIN"),
    ("X.TO", "DIVFIN"),
    # ---- Australia (Big Four banks + insurers + Macquarie) ----
    ("CBA.AX", "BANK"), ("NAB.AX", "BANK"), ("WBC.AX", "BANK"),
    ("ANZ.AX", "BANK"), ("MQG.AX", "DIVFIN"), ("QBE.AX", "INSURER"),
    ("SUN.AX", "INSURER"), ("IAG.AX", "INSURER"),
    # ---- Developed-market ADRs on US exchanges (bare tickers) ----
    ("HSBC", "BANK"), ("BCS", "BANK"), ("LYG", "BANK"), ("NWG", "BANK"),
    ("MUFG", "BANK"), ("SMFG", "BANK"), ("MFG", "BANK"), ("IX", "DIVFIN"),
    ("BBVA", "BANK"), ("ING", "BANK"), ("DB", "BANK"), ("UBS", "BANK"),
    ("MFC", "INSURER"), ("SLF", "INSURER"), ("AEG", "INSURER"),
]

# ================================ EMERGING ================================
# EM LIFE INSURANCE IS A PRIORITY (Stage 1a's cheapest/highest-quality EM sector).
EM_FIN = [
    # ---- China / HK — LIFE INSURERS (PRIORITY) ----
    ("2628.HK", "INSURER"),   # China Life
    ("2318.HK", "INSURER"),   # Ping An
    ("2601.HK", "INSURER"),   # China Pacific (CPIC)
    ("2628.HK", "INSURER"),   # dup guard (dedup later)
    ("1336.HK", "INSURER"),   # New China Life
    ("2628.HK", "INSURER"),
    ("0966.HK", "INSURER"),   # China Taiping
    ("1299.HK", "INSURER"),   # AIA (HK-domiciled, pan-Asia life)
    ("6060.HK", "INSURER"),   # ZhongAn Online P&C
    ("2328.HK", "INSURER"),   # PICC P&C
    ("1339.HK", "INSURER"),   # PICC Group
    # ---- China / HK — BANKS ----
    ("1398.HK", "BANK"),   # ICBC
    ("0939.HK", "BANK"),   # China Construction Bank
    ("3988.HK", "BANK"),   # Bank of China
    ("1288.HK", "BANK"),   # Agricultural Bank of China
    ("3968.HK", "BANK"),   # China Merchants Bank
    ("2888.HK", "BANK"),   # Standard Chartered (HK line) — dev, but keep
    ("1359.HK", "DIVFIN"), # China Cinda (asset mgmt)
    ("0388.HK", "DIVFIN"), # HKEX (exchange)
    # ---- India — banks + insurers + NBFC ----
    ("HDFCBANK.NS", "BANK"), ("ICICIBANK.NS", "BANK"), ("SBIN.NS", "BANK"),
    ("KOTAKBANK.NS", "BANK"), ("AXISBANK.NS", "BANK"), ("INDUSINDBK.NS", "BANK"),
    ("BAJFINANCE.NS", "DIVFIN"), ("BAJAJFINSV.NS", "DIVFIN"),
    ("SBILIFE.NS", "INSURER"), ("HDFCLIFE.NS", "INSURER"),
    ("ICICIPRULI.NS", "INSURER"), ("ICICIGI.NS", "INSURER"),
    ("LICI.NS", "INSURER"),   # Life Insurance Corp of India (huge EM life insurer)
    ("HDB", "BANK"), ("IBN", "BANK"),   # India bank ADRs
    # ---- Brazil ----
    ("ITUB", "BANK"), ("BBD", "BANK"), ("BSBR", "BANK"),
    ("ITUB4.SA", "BANK"), ("BBDC4.SA", "BANK"), ("BBAS3.SA", "BANK"),
    ("SANB11.SA", "BANK"), ("BPAC11.SA", "BANK"),
    ("BBSE3.SA", "INSURER"),   # BB Seguridade (Brazil insurer)
    ("PSSA3.SA", "INSURER"),   # Porto Seguro
    ("B3SA3.SA", "DIVFIN"),    # B3 exchange
    # ---- Mexico ----
    ("GFNORTEO.MX", "BANK"), ("GFINBURO.MX", "BANK"), ("BBAJIOO.MX", "BANK"),
    ("Q.MX", "INSURER"),       # Qualitas (Mexican insurer)
    # ---- South Africa (JSE) ----
    ("FSR.JO", "BANK"), ("SBK.JO", "BANK"), ("NED.JO", "BANK"),
    ("CPI.JO", "BANK"), ("ABG.JO", "BANK"),
    ("SLM.JO", "INSURER"),     # Sanlam (SA life insurer)
    ("DSY.JO", "INSURER"),     # Discovery
    ("OMU.JO", "INSURER"),     # Old Mutual
    # ---- SE Asia ----
    ("BBCA.JK", "BANK"), ("BBRI.JK", "BANK"), ("BMRI.JK", "BANK"),  # Indonesia
    ("BBNI.JK", "BANK"),
    ("DBSDF", "BANK"),         # DBS ADR (Singapore) — dev, but SE-Asia leader
    ("D05.SI", "BANK"), ("O39.SI", "BANK"), ("U11.SI", "BANK"),     # DBS/OCBC/UOB Singapore
    ("1155.KL", "BANK"), ("PBBANK.KL", "BANK"),                      # Malaysia (Maybank)
    ("BBL.BK", "BANK"), ("KBANK.BK", "BANK"), ("SCB.BK", "BANK"),    # Thailand
    # ---- Taiwan / Korea ----
    ("2882.TW", "INSURER"),    # Cathay Financial (life-heavy)
    ("2881.TW", "DIVFIN"),     # Fubon Financial
    ("2891.TW", "BANK"),       # CTBC Financial
    ("2886.TW", "BANK"),       # Mega Financial
    ("105560.KS", "BANK"),     # KB Financial
    ("055550.KS", "BANK"),     # Shinhan Financial
    ("086790.KS", "BANK"),     # Hana Financial
    ("032830.KS", "INSURER"),  # Samsung Life
    ("000810.KS", "INSURER"),  # Samsung Fire & Marine
    ("KB", "BANK"), ("SHG", "BANK"),   # Korea bank ADRs
]

# ================================ REITs (separate sub-group) ================================
# Valued on P/B + FFO; collected separately. US REITs come from the S&P 500 Real Estate
# sector (cached list). A few large ex-US REITs added.
REIT_EXTRA = [
    ("GMG.AX", "REIT"), ("SCG.AX", "REIT"),        # Australia
    ("SGRO.L", "REIT"), ("LAND.L", "REIT"), ("BLND.L", "REIT"),  # UK
    ("URW.PA", "REIT"),                             # France
    ("0823.HK", "REIT"),                            # HK (Link REIT)
]


def _us_financials() -> pd.DataFrame:
    """US financials + REITs from the cached S&P 500 GICS list (Stage 1b, Wikipedia)."""
    cpath = os.path.join(CACHE, "sp500.csv")
    if not os.path.exists(cpath):
        # build it via the Stage 1b universe helper (scrapes Wikipedia, cited)
        import sys
        sys.path.insert(0, HERE)
        from universe import get_sp500  # noqa
        sp = get_sp500()
    else:
        sp = pd.read_csv(cpath)
    fin = sp[sp["gics_sector"] == "Financials"].copy()
    fin["region"] = "US"
    fin["sub_group_hint"] = "FIN_US"   # refined from yfinance industry at fetch
    reit = sp[sp["gics_sector"] == "Real Estate"].copy()
    reit["region"] = "US"
    reit["sub_group_hint"] = "REIT"
    out = pd.concat([fin, reit], ignore_index=True)
    return out[["ticker", "name", "region", "sub_group_hint"]]


def build_financials_universe(include_reits: bool = True) -> pd.DataFrame:
    us = _us_financials()

    def mk(pairs, region):
        return pd.DataFrame(
            {"ticker": [p[0] for p in pairs],
             "name": None,
             "region": region,
             "sub_group_hint": [p[1] for p in pairs]})

    dev = mk(DEV_EXUS_FIN, "DEV_EXUS")
    em = mk(EM_FIN, "EM")
    parts = [us, dev, em]
    if include_reits:
        parts.append(mk(REIT_EXTRA, "DEV_EXUS"))
    uni = pd.concat(parts, ignore_index=True)
    if not include_reits:
        uni = uni[uni["sub_group_hint"] != "REIT"]
    uni = uni.drop_duplicates(subset="ticker").reset_index(drop=True)
    return uni


if __name__ == "__main__":
    u = build_financials_universe()
    print(f"Financials universe: {len(u)} names")
    print(u["region"].value_counts().to_string())
    print("\nby sub_group_hint:")
    print(u["sub_group_hint"].value_counts().to_string())
    out = os.path.join(CACHE, "financials_universe.csv")
    u.to_csv(out, index=False)
    print(f"\nWrote {out}")
