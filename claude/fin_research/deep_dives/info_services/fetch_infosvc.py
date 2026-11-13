#!/usr/bin/env python3
"""Live yfinance pull for the Information Services deep dive: SPGI, MCO, MSCI (+peers).
Anti-hallucination: every printed number is a live yfinance value with an as-of timestamp.
"""
import json, datetime, sys
import yfinance as yf

AS_OF = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
TICKERS = ["SPGI", "MCO", "MSCI", "FDS", "MORN", "TRI", "ICE"]

def g(info, *keys):
    for k in keys:
        v = info.get(k)
        if v is not None:
            return v
    return None

def num(v):
    if v is None:
        return None
    try:
        return round(float(v), 4)
    except Exception:
        return v

out = {"as_of": AS_OF, "tickers": {}}
for t in TICKERS:
    tk = yf.Ticker(t)
    try:
        info = tk.info
    except Exception as e:
        out["tickers"][t] = {"error": str(e)}
        continue
    # price history for year-end multiples context
    try:
        hist = tk.history(period="max", interval="1mo")
        px_now = float(hist["Close"].iloc[-1]) if len(hist) else None
    except Exception:
        px_now = None
    rec = {
        "price": num(g(info, "currentPrice", "regularMarketPrice") or px_now),
        "marketCap": num(g(info, "marketCap")),
        "trailingPE": num(g(info, "trailingPE")),
        "forwardPE": num(g(info, "forwardPE")),
        "priceToSalesTrailing12Months": num(g(info, "priceToSalesTrailing12Months")),
        "enterpriseValue": num(g(info, "enterpriseValue")),
        "enterpriseToEbitda": num(g(info, "enterpriseToEbitda")),
        "enterpriseToRevenue": num(g(info, "enterpriseToRevenue")),
        "priceToBook": num(g(info, "priceToBook")),
        "profitMargins": num(g(info, "profitMargins")),
        "operatingMargins": num(g(info, "operatingMargins")),
        "grossMargins": num(g(info, "grossMargins")),
        "ebitdaMargins": num(g(info, "ebitdaMargins")),
        "returnOnEquity": num(g(info, "returnOnEquity")),
        "returnOnAssets": num(g(info, "returnOnAssets")),
        "revenueGrowth": num(g(info, "revenueGrowth")),
        "earningsGrowth": num(g(info, "earningsGrowth")),
        "totalRevenue": num(g(info, "totalRevenue")),
        "ebitda": num(g(info, "ebitda")),
        "grossProfits": num(g(info, "grossProfits")),
        "freeCashflow": num(g(info, "freeCashflow")),
        "operatingCashflow": num(g(info, "operatingCashflow")),
        "totalCash": num(g(info, "totalCash")),
        "totalDebt": num(g(info, "totalDebt")),
        "dividendYield": num(g(info, "dividendYield")),
        "payoutRatio": num(g(info, "payoutRatio")),
        "sharesOutstanding": num(g(info, "sharesOutstanding")),
        "fiftyTwoWeekHigh": num(g(info, "fiftyTwoWeekHigh")),
        "fiftyTwoWeekLow": num(g(info, "fiftyTwoWeekLow")),
        "beta": num(g(info, "beta")),
    }
    # FCF yield
    fcf = rec["freeCashflow"]; mc = rec["marketCap"]
    rec["fcf_yield_pct"] = round(100.0*fcf/mc, 2) if (fcf and mc) else None
    ev = rec["enterpriseValue"]
    rec["fcf_yield_on_ev_pct"] = round(100.0*fcf/ev, 2) if (fcf and ev) else None
    out["tickers"][t] = rec

print(json.dumps(out, indent=2))
