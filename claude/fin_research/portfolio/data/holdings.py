"""
Portfolio ground-truth ledger + live re-pricing.
Built 2026-07-07. Owner: Hooman Shariati (Canadian citizen).

- HOLDINGS: transcribed verbatim from Hooman's portfolio export (his data, not invented).
- Live re-pricing via yfinance (curl_cffi backend; bare urllib gets 429 from Yahoo).
- Emits holdings_live.csv + holdings_live.json with live price, market value, gain/loss.

Run: /opt/venv/bin/python3 portfolio/data/holdings.py
"""
import json, time, sys
import yfinance as yf

USDCAD = 0.70347  # CAD->USD rate from Hooman's export (2026-07-06). 1 CAD = 0.70347 USD.

# Each row: (his_ticker, yahoo_ticker, name, theme, his_bucket, his_geo, his_cap,
#            shares, avg_buy_price_native, price_ccy, book_value_usd_from_export)
# yahoo_ticker=None => can't price live (physical/crypto handled separately or skip).
# book_value_usd is HIS reported book value (USD) — used as fallback + reconciliation.
HOLDINGS = [
    # ticker,      yahoo,       name,                         theme,               buck, geo,   cap,     shares,   avgpx,    ccy,   bookUSD
    ("AA",         "AA",        "Alcoa",                      "aluminum",          "C", "USA",  "large",   50,    71.50,   "USD",  3575.00),
    ("AEVA",       "AEVA",      "Aeva Technologies",          "autonomous",        "C", "USA",  "small",   70,    18.61,   "USD",  1302.99),
    ("AUR",        "AUR",       "Aurora Innovation",          "autonomous",        "C", "USA",  "small",  100,     5.42,   "USD",   542.00),
    ("KWEB",       "KWEB",      "KraneShares China Internet", "china",             "C", "EM",   "large",  147,    41.79,   "USD",  6143.13),
    ("BABA",       "BABA",      "Alibaba",                    "china",             "C", "EM",   "large",    6,   209.73,   "USD",  1258.36),
    ("BIDU",       "BIDU",      "Baidu",                      "china",             "C", "EM",   "large",    4,   189.57,   "USD",   758.27),
    ("NTCPF",      "NTCPF",     "NorthIsle Copper & Gold",    "copper",            "C", "DEV",  "small", 1300,     3.08,   "USD",  2816.17),
    ("TSE:COP.U",  "COP-U.TO",  "Sprott Physical Copper Tr",  "copper",            "B", "DEV",  "large",  180,    11.80,   "CAD",  2124.37),
    ("BHP",        "BHP",       "BHP Group",                  "copper",            "B", "DEV",  "large",   50,    82.78,   "USD",  4139.00),
    ("MARA",       "MARA",      "Marathon Digital",           "crypto",            "C", "USA",  "med",     30,    43.61,   "USD",  1308.30),
    ("GEV",        "GEV",       "GE Vernova",                 "electrification",   "C", "USA",  "large",    8,   614.19,   "USD",  4913.52),
    ("CHPT",       "CHPT",      "ChargePoint",                "ev",                "C", "USA",  "small",  100,    18.96,   "USD",  1896.00),
    ("NYSE:NIO",   "NIO",       "NIO",                        "ev",                "C", "EM",   "small",  120,    41.63,   "USD",  4995.53),
    ("F",          "F",         "Ford",                       "ev",                "C", "USA",  "med",     30,    17.56,   "USD",   526.80),
    ("LCID",       "LCID",      "Lucid Group",                "ev",                "C", "USA",  "small",   20,    25.97,   "USD",   519.40),
    ("RIVN",       "RIVN",      "Rivian",                     "ev",                "C", "USA",  "small",   10,    58.99,   "USD",   589.90),
    ("CAG",        "CAG",       "Conagra Brands",             "food",              "B", "USA",  "med",    292.3282, 17.48, "USD",  5108.59),
    ("KHC",        "KHC",       "Kraft Heinz",                "food",              "B", "USA",  "large",  208.7079, 24.42, "USD",  5096.28),
    ("PDBA",       "PDBA",      "Invesco Ag Commodity ETF",   "food",              "C", "DEV",  "large",  140,    35.25,   "USD",  4935.00),
    ("CF",         "CF",        "CF Industries",              "food",              "C", "USA",  "large",   40,   113.66,   "USD",  4546.40),
    ("TSE:MNT",    "MNT.TO",    "RCM Cdn Gold Reserves ETR",  "gold",              "B", "DEV",  "med",    588,    57.88,   "CAD", 34030.76),
    ("Physical-Gold", None,     "Physical Gold (2.359oz)",    "gold",              "B", "-",    "large", 2.359, 4238.40,   "USD",  9998.39),
    ("AEM",        "AEM",       "Agnico Eagle Mines",         "gold",              "B", "DEV",  "large",   20,   207.33,   "USD",  4146.61),
    ("EMPYF",      "EMPYF",     "Empress Royalty",            "gold",              "B", "DEV",  "small", 3000,     0.76,   "USD",  1601.29),
    ("PFE",        "PFE",       "Pfizer",                     "health-bio-tk-ai",  "C", "USA",  "large",  738,    25.28,   "USD", 18657.39),
    ("LLY",        "LLY",       "Eli Lilly",                  "health-bio-tk-ai",  "C", "USA",  "large",    9,  1060.00,   "USD",  9540.00),
    ("JMIA",       "JMIA",      "Jumia Technologies",         "international",     "C", "EM",   "small",   30,    13.55,   "USD",   406.50),
    ("XOM",        "XOM",       "ExxonMobil",                 "oil&gas",           "B", "USA",  "large",  168,   119.19,   "USD", 20023.14),
    ("TSE:CNQ",    "CNQ.TO",    "Canadian Natural Resources", "oil&gas",           "B", "DEV",  "large",  588,    49.03,   "CAD", 20277.65),
    ("TSE:ARX",    "ARX.TO",    "ARC Resources",              "oil&gas",           "B", "DEV",  "med",    567,    25.86,   "CAD", 10313.29),
    ("OXY",        "OXY",       "Occidental Petroleum",       "oil&gas",           "C", "USA",  "small",  123,    41.32,   "USD",  5082.36),
    ("SLB",        "SLB",       "Schlumberger",               "oil&gas",           "B", "USA",  "large",  110,    49.34,   "USD",  5427.40),
    ("TSE:CVE",    "CVE.TO",    "Cenovus Energy",             "oil&gas",           "B", "DEV",  "large",  200,    18.83,   "CAD",  3766.00),
    ("TSE:TOU",    "TOU.TO",    "Tourmaline Oil",             "oil&gas",           "B", "DEV",  "large",   60,    57.68,   "CAD",  2434.12),
    ("BOIL",       "BOIL",      "ProShares 2x NatGas",        "oil&gas",           "C", "DEV",  "large",  100,    28.60,   "USD",  2860.00),
    ("UNG",        "UNG",       "US Natural Gas Fund",        "oil&gas",           "B", "DEV",  "large",  250,    11.88,   "USD",  2970.00),
    ("NYSE:SBSW",  "SBSW",      "Sibanye Stillwater",         "platinum_pall",     "B", "EM",   "med",    200,    19.29,   "USD",  3858.96),
    ("CSGP",       "CSGP",      "CoStar Group",               "real-estate",       "B", "USA",  "large",    3,    73.99,   "USD",   221.97),
    ("SBUX",       "SBUX",      "Starbucks",                  "retail",            "C", "USA",  "large",   10,    99.46,   "USD",   994.60),
    ("GLBS",       "GLBS",      "Globus Maritime",            "retail",            "C", "EM",   "small",   21,     5.30,   "USD",   111.34),
    ("WPM",        "WPM",       "Wheaton Precious Metals",    "silver",            "B", "DEV",  "large",  227,   148.11,   "USD", 33621.97),
    ("CRCL",       "CRCL",      "Circle Internet Group",      "stable-coin",       "C", "USA",  "small",   40,    76.89,   "USD",  3075.60),
    ("XME",        "XME",       "SPDR Metals & Mining ETF",   "steel",             "B", "DEV",  "large",   25,   118.19,   "USD",  2954.75),
    ("RBLX",       "RBLX",      "Roblox",                     "tech",              "C", "USA",  "med",     50,    76.50,   "USD",  3825.00),
    ("AMZN",       "AMZN",      "Amazon",                     "tech",              "C", "USA",  "large",   51,   223.59,   "USD", 11403.32),
    ("BATS:ARKK",  "ARKK",      "ARK Innovation ETF",         "tech",              "C", "USA",  "med",     16,   123.28,   "USD",  1972.48),
    ("CCJ",        "CCJ",       "Cameco",                     "uranium",           "C", "DEV",  "large",  150,    84.93,   "USD", 12739.23),
    ("BWXT",       "BWXT",      "BWX Technologies",           "uranium",           "C", "USA",  "large",   29,   168.12,   "USD",  4875.48),
    ("CEG",        "CEG",       "Constellation Energy",       "uranium",           "C", "USA",  "large",    8,   284.60,   "USD",  2276.80),
    ("TSE:URC",    "URC.TO",    "Uranium Royalty Corp",       "uranium",           "C", "DEV",  "small",  350,     3.04,   "CAD",   748.35),
    # Crypto (non-yfinance-equity; priced separately)
    ("BTCUSD-1",   "BTC-USD",   "Bitcoin (lot 1)",            "crypto",            "C", "-",    "large", 0.07730247, 63490.60, "USD", 4907.98),
    ("BTCCAD",     "BTC-USD",   "Bitcoin (CAD lot)",          "crypto",            "C", "-",    "large", 0.0625,   112000.00, "CAD", 4923.38),
    ("BTCUSD-2",   "BTC-USD",   "Bitcoin (lot 2)",            "crypto",            "C", "-",    "large", 0.0374162, 72000.00, "USD", 2693.97),
]

def fx_to_usd(ccy):
    return USDCAD if ccy == "CAD" else 1.0

def main():
    rows = []
    # unique yahoo tickers to fetch
    tickers = sorted({h[1] for h in HOLDINGS if h[1]})
    live = {}
    print(f"Fetching {len(tickers)} tickers...", file=sys.stderr)
    for t in tickers:
        for attempt in range(2):
            try:
                info = yf.Ticker(t).info
                px = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
                live[t] = {
                    "price": px, "ccy": info.get("currency"),
                    "mcap": info.get("marketCap"),
                    "name": info.get("shortName"),
                    "fwdPE": info.get("forwardPE"), "trailPE": info.get("trailingPE"),
                    "pb": info.get("priceToBook"), "evebitda": info.get("enterpriseToEbitda"),
                    "roe": info.get("returnOnEquity"), "sector": info.get("sector"),
                    "industry": info.get("industry"), "country": info.get("country"),
                    "divyield": info.get("dividendYield"), "beta": info.get("beta"),
                }
                break
            except Exception as e:
                if attempt == 1:
                    live[t] = {"error": str(e)[:100]}
                time.sleep(1)
        time.sleep(0.3)

    for (tk, yh, name, theme, buck, geo, cap, sh, avg, ccy, bookUSD) in HOLDINGS:
        L = live.get(yh, {})
        price_native = L.get("price")
        # crypto: yfinance gives BTC-USD in USD; if his lot ccy is CAD it's still USD-priced asset
        if price_native is not None:
            mv_native = price_native * sh
            # market value in USD: BTC priced in USD already; equity native ccy -> convert
            if yh == "BTC-USD":
                mv_usd = mv_native  # BTC-USD price is USD
            else:
                mv_usd = mv_native * fx_to_usd(L.get("ccy") or ccy)
        else:
            mv_usd = None
        # RECOMPUTE book value from first principles (his book_usd column is inconsistent:
        # some CAD holdings are converted to USD, some left in raw CAD). shares*avgbuy*fx.
        if yh == "BTC-USD":
            # avg buy price stated in native ccy; convert to USD basis
            book_recalc = avg * sh * fx_to_usd(ccy)
        else:
            book_recalc = avg * sh * fx_to_usd(ccy)
        bookUSD_recalc = round(book_recalc, 2)
        gl = (mv_usd - bookUSD_recalc) if mv_usd is not None else None
        rows.append({
            "ticker": tk, "yahoo": yh, "name": name, "theme": theme,
            "his_bucket": buck, "his_geo": geo, "his_cap": cap,
            "shares": sh, "avg_buy": avg, "ccy": ccy,
            "book_usd_his": round(bookUSD, 2),
            "book_usd": bookUSD_recalc,
            "live_price": price_native, "live_ccy": L.get("ccy"),
            "mkt_val_usd": round(mv_usd, 2) if mv_usd is not None else None,
            "gain_loss_usd": round(gl, 2) if gl is not None else None,
            "gl_pct": round(100 * gl / bookUSD_recalc, 1) if (gl is not None and bookUSD_recalc) else None,
            "mcap": L.get("mcap"), "fwdPE": L.get("fwdPE"), "trailPE": L.get("trailPE"),
            "pb": L.get("pb"), "evebitda": L.get("evebitda"), "roe": L.get("roe"),
            "yf_sector": L.get("sector"), "yf_industry": L.get("industry"),
            "yf_country": L.get("country"), "divyield": L.get("divyield"),
            "beta": L.get("beta"), "err": L.get("error"),
        })

    # write outputs
    import csv
    out_csv = "/home/colligo/hs_scripts/claude/fin_research/portfolio/data/holdings_live.csv"
    out_json = "/home/colligo/hs_scripts/claude/fin_research/portfolio/data/holdings_live.json"
    keys = list(rows[0].keys())
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    with open(out_json, "w") as f:
        json.dump({"as_of": "2026-07-07", "usdcad": USDCAD, "rows": rows}, f, indent=2)

    # summary
    total_mv = sum(r["mkt_val_usd"] for r in rows if r["mkt_val_usd"])
    total_bk = sum(r["book_usd"] for r in rows if r["book_usd"])
    errs = [r["ticker"] for r in rows if r["err"]]
    print(f"\nRows: {len(rows)}  Total mkt val (equities+crypto): ${total_mv:,.0f}  book ${total_bk:,.0f}")
    print(f"Errors ({len(errs)}): {errs}")
    print(f"Wrote {out_csv}")

if __name__ == "__main__":
    main()
