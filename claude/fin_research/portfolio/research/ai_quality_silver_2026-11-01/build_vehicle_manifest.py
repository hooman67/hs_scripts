#!/usr/bin/env python3
"""Hash the raw official holdings and precious-metals vehicle evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "data" / "primary"

SOURCES = {
    "JQUA_holdings_2026-10-30.xlsx": "https://am.jpmorgan.com/FundsMarketingHandler/excel?type=dailyETFHoldings&cusip=46641Q761&country=us&role=adv&fundType=ETF&locale=en-US&isUnderlyingHolding=false&isProxyHolding=false",
    "jqua_product.html": "https://am.jpmorgan.com/us/en/asset-management/adv/products/jpmorgan-u-s-quality-factor-etf-etf-shares-46641q761",
    "sivr_sec.html": "https://www.sec.gov/Archives/edgar/data/1450922/000199937126010350/sivr-10q_033126.htm",
    "slv.html": "https://www.ishares.com/us/products/239855/ishares-silver-trust-fund",
    "pslv.html": "https://sprott.com/investment-strategies/physical-bullion-trusts/silver/",
    "360016270371.json": "https://support.onegold.com/api/v2/help_center/en-us/articles/360016270371.json",
    "360038030732.json": "https://support.onegold.com/api/v2/help_center/en-us/articles/360038030732.json",
    "360038399731.json": "https://support.onegold.com/api/v2/help_center/en-us/articles/360038399731.json",
}


def main() -> None:
    files = []
    for filename, url in SOURCES.items():
        path = PRIMARY / filename
        payload = path.read_bytes()
        files.append(
            {
                "path": f"data/primary/{filename}",
                "url": url,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    result = {"retrieved_for_review_on": "2026-11-01", "files": files}
    (ROOT / "data" / "vehicle_source_manifest.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
