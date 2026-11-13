#!/usr/bin/env python3
"""Save a bounded secondary price context for silver and gold futures."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf


ROOT = Path(__file__).resolve().parent
rows = {}
for symbol in ("SI=F", "GC=F"):
    history = yf.Ticker(symbol).history(
        start="2025-10-31", end="2026-10-31", auto_adjust=False
    )
    close = history["Close"].dropna()
    rows[symbol] = {
        "last_date": str(close.index[-1].date()),
        "close": float(close.iloc[-1]),
        "one_year_min_close": float(close.min()),
        "one_year_max_close": float(close.max()),
    }

result = {
    "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
    "source": "Yahoo Finance via yfinance; secondary price data",
    "symbols": rows,
    "gold_silver_ratio_at_last_close": rows["GC=F"]["close"]
    / rows["SI=F"]["close"],
}
(ROOT / "data" / "metals_price_context.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
