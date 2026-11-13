# SOURCES — Curated Data Sources + Reliability Notes

Last updated: 2026-07-01 by Claude (Opus 4.8).

Prefer free, primary, reproducible sources. Cite source + as-of date for every number.

## Top-down (sector-level valuation & quality)

- **NYU / Aswath Damodaran datasets** — https://pages.stern.nyu.edu/~adamodar/
  Free, updated ~yearly (usually January). Sector multiples (PE, forward PE, EV/EBITDA,
  P/B, P/S), margins, ROIC, ROE, betas, cost of capital, revenue growth — by industry.
  **Best single source for top-down sector cheapness AND quality.** Reliability: HIGH
  (academic, transparent methodology). Caveat: annual snapshot, US + global variants.
- **multpl.com** — S&P 500 aggregate PE / Shiller CAPE / dividend yield history. Good for
  "is the whole market cheap/expensive vs history" context.
- **Yardeni Research** — free sector & S&P valuation chartbooks (forward P/E by sector).

## Bottom-up (company-level fundamentals)

- **SEC EDGAR** — https://www.sec.gov/edgar — primary 10-K/10-Q filings. Ground truth for
  financials. Reliability: HIGHEST. Has a JSON company-facts API.
- **yfinance (Yahoo Finance)** — prices, market cap, current multiples, dividends. Free,
  scriptable (python). Reliability: MEDIUM (occasional bad fields; cross-check).
- **Financial Modeling Prep (FMP)** — fundamentals + ratios API, free tier (limited calls).
- **Alpha Vantage** — fundamentals + prices API, free tier (rate-limited).
- **Finviz** — https://finviz.com/screener.ashx — fast web screener by ratio/sector.
- **macrotrends** — long-horizon per-company ratio history (web).

## Reliability protocol

- When a single number drives a ranking decision, cross-check it against a second source.
- yfinance/Finviz are convenient but secondary — verify surprising figures against EDGAR.
- Record the as-of date; multiples move with price daily.
