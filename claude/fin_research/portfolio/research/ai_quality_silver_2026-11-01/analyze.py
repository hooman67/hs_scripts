#!/usr/bin/env python3
"""Reproduce the AI-quality and silver allocation arithmetic.

Issuer operating data below is transcribed from the latest primary filings
saved in data/primary_text. Market prices and capitalizations are the
2026-10-30 close in data/market_snapshot.json.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
PORTFOLIO_VALUE = 674_780.0
QUALITY_TARGET_PCT = 5.5
SILVER_PLATINUM_TARGET_PCT = 1.0
WPM_SHARES = 154
WPM_SILVER_REVENUE_MIX = 0.52
WPM_GOLD_REVENUE_MIX = 0.46


PRIMARY = {
    "LRCX": {
        "period": "FY2027 Q1",
        "revenue_b": 8.219,
        "revenue_growth_pct": 54.4,
        "gaap_operating_margin_pct": 40.0,
        "gaap_eps": 2.19,
        "guide_gaap_eps_mid": 2.33,
        "quality_note": "Net cash; share count declined; service/support is about 30% of revenue.",
        "principal_risk": "Wafer-fab cycle and 35% China revenue exposure.",
    },
    "KLAC": {
        "period": "FY2027 Q1",
        "revenue_b": 4.136,
        "revenue_growth_pct": 28.9,
        "gaap_operating_margin_pct": 45.0,
        "gaap_eps": 1.18,
        "guide_gaap_eps_mid": 1.41,
        "quality_note": "Highest margins in the set; about $4.04B primary-source TTM FCF; share count declined.",
        "principal_risk": "Semiconductor capital-equipment cycle and a richer current multiple than LRCX.",
    },
    "ANET": {
        "period": "2026 Q2",
        "revenue_b": 3.036,
        "revenue_growth_pct": 37.7,
        "gaap_operating_margin_pct": 45.4,
        "gaap_eps": 0.95,
        "guide_non_gaap_eps_mid": 1.07,
        "quality_note": "Debt-free balance sheet and exceptional margins.",
        "principal_risk": "Two customers were 42% of FY2025 revenue; premium valuation.",
    },
    "ARM": {
        "period": "FY2027 Q1",
        "revenue_b": 1.289,
        "revenue_growth_pct": 22.0,
        "gaap_operating_margin_pct": 7.1,
        "gaap_eps": 0.25,
        "non_gaap_eps": 0.45,
        "quality_note": "Dominant CPU instruction-set ecosystem and 97% GAAP gross margin.",
        "principal_risk": "SBC was $343M in the quarter and valuation assumes extraordinary growth.",
    },
    "MRVL": {
        "period": "FY2027 Q2",
        "revenue_b": 2.739,
        "revenue_growth_pct": 37.0,
        "gaap_operating_margin_pct": 16.8,
        "gaap_eps": 0.33,
        "non_gaap_eps": 0.94,
        "guide_gaap_eps_mid": 0.53,
        "guide_non_gaap_eps_mid": 1.10,
        "quality_note": "Strong data-center growth and positive quarterly free cash flow.",
        "principal_risk": "SBC was 11.9% of revenue; diluted shares rose 5.8%; customer/distributor concentration.",
    },
    "LITE": {
        "period": "FY2026 Q4",
        "revenue_b": 1.006,
        "revenue_growth_pct": 109.3,
        "gaap_operating_margin_pct": 27.8,
        "non_gaap_eps": 3.24,
        "guide_non_gaap_eps_mid": 4.20,
        "quality_note": "Very rapid optical-component growth and strong guided operating margin.",
        "principal_risk": "FY free cash flow was only $300M; common shares rose 27%; two customers were 42% of revenue.",
    },
    "COHR": {
        "period": "FY2026 Q4",
        "revenue_b": 2.046,
        "revenue_growth_pct": 33.8,
        "gaap_operating_margin_pct": 12.4,
        "gaap_eps": 1.19,
        "guide_non_gaap_eps_mid": 1.95,
        "quality_note": "Lowest sales multiple in the group and strong optical demand.",
        "principal_risk": "FY free cash flow was about -$1.02B; net debt and heavy capital spending; shares rose 26%.",
    },
}


VERDICTS = {
    "LRCX": "Best valuation/quality trade-off; watch for a better entry.",
    "KLAC": "Best moat and cash economics; watch for a better entry.",
    "ANET": "Excellent company, but too expensive and concentrated at this price.",
    "ARM": "Avoid at this valuation; GAAP/non-GAAP gap is too large.",
    "MRVL": "Watch, not a quality-sleeve buy; dilution and non-GAAP dependence are material.",
    "LITE": "Avoid for this sleeve; optics upside is paired with dilution and weak cash yield.",
    "COHR": "Watch for cash-flow proof; apparent cheapness is not yet quality.",
}


def read_xlsx_rows(path: Path) -> list[dict[str, str]]:
    """Read the small official holdings workbook using only the stdlib."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as zf:
        strings_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
        strings = [
            "".join(t.text or "" for t in item.iter(f"{{{ns['m']}}}t"))
            for item in strings_root.findall("m:si", ns)
        ]
        sheet = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))

    raw_rows: list[dict[str, str]] = []
    for row in sheet.findall(".//m:row", ns):
        values: dict[str, str] = {}
        for cell in row.findall("m:c", ns):
            ref = cell.attrib.get("r", "")
            col_match = re.match(r"[A-Z]+", ref)
            value_node = cell.find("m:v", ns)
            if not col_match or value_node is None:
                continue
            value = value_node.text or ""
            if cell.attrib.get("t") == "s":
                value = strings[int(value)]
            values[col_match.group(0)] = value
        raw_rows.append(values)

    header = next(row for row in raw_rows if row.get("A") == "Ticker")
    col_to_name = dict(header)
    return [
        {col_to_name[col]: val for col, val in row.items() if col in col_to_name}
        for row in raw_rows
        if row.get("A") and row.get("A") != "Ticker"
    ]


def multiple(price: float, quarterly_eps: float | None) -> float | None:
    return None if not quarterly_eps else round(price / (4 * quarterly_eps), 1)


def main() -> None:
    market = json.loads((DATA / "market_snapshot.json").read_text())
    symbols = market["symbols"]
    holdings = read_xlsx_rows(DATA / "primary" / "JQUA_holdings_2026-10-30.xlsx")
    weight_by_ticker = {
        row["Ticker"]: float(row["% of Net Assets"].rstrip("%"))
        for row in holdings
        if row.get("% of Net Assets", "").endswith("%")
    }

    candidates: dict[str, dict] = {}
    for ticker, primary in PRIMARY.items():
        quote = symbols[ticker]
        price = float(quote["close"])
        market_cap_b = float(quote["marketCap"]) / 1e9
        row = dict(primary)
        row.update(
            {
                "price": round(price, 2),
                "market_cap_b": round(market_cap_b, 1),
                "annualized_current_quarter_sales_multiple": round(
                    market_cap_b / (primary["revenue_b"] * 4), 1
                ),
                "current_quarter_gaap_run_rate_pe": multiple(price, primary.get("gaap_eps")),
                "current_quarter_non_gaap_run_rate_pe": multiple(price, primary.get("non_gaap_eps")),
                "next_quarter_guide_gaap_run_rate_pe": multiple(price, primary.get("guide_gaap_eps_mid")),
                "next_quarter_guide_non_gaap_run_rate_pe": multiple(
                    price, primary.get("guide_non_gaap_eps_mid")
                ),
                "secondary_vendor_forward_pe": round(float(quote["forwardPE"]), 1),
                "jqua_weight_pct": weight_by_ticker.get(ticker, 0.0),
                "verdict": VERDICTS[ticker],
            }
        )
        candidates[ticker] = row

    wpm_price = float(symbols["WPM"]["close"])
    wpm_value = WPM_SHARES * wpm_price
    silver_value = wpm_value * WPM_SILVER_REVENUE_MIX
    gold_value = wpm_value * WPM_GOLD_REVENUE_MIX
    silver_target_value = PORTFOLIO_VALUE * SILVER_PLATINUM_TARGET_PCT / 100
    wpm_value_at_silver_target = silver_target_value / WPM_SILVER_REVENUE_MIX
    wpm_shares_at_silver_target = wpm_value_at_silver_target / wpm_price

    top_ten = sorted(
        ((ticker, weight) for ticker, weight in weight_by_ticker.items()),
        key=lambda item: item[1],
        reverse=True,
    )[:10]

    result = {
        "as_of": "2026-10-30 market close",
        "portfolio": {
            "value": PORTFOLIO_VALUE,
            "quality_target_pct": QUALITY_TARGET_PCT,
            "quality_target_value": round(PORTFOLIO_VALUE * QUALITY_TARGET_PCT / 100, 2),
            "single_stock_cap_pct": 2.0,
        },
        "jqua": {
            "price": round(float(symbols["JQUA"]["close"]), 2),
            "current_pe_secondary": round(float(symbols["JQUA"]["trailingPE"]), 1),
            "fee_pct": 0.12,
            "official_holdings_date": "2026-10-30",
            "candidate_overlap_pct": {
                ticker: weight_by_ticker.get(ticker, 0.0) for ticker in PRIMARY
            },
            "top_ten": top_ten,
            "top_ten_weight_pct": round(sum(weight for _, weight in top_ten), 2),
            "technology_weight_pct_secondary": 42.54,
        },
        "google_context": {
            "price": round(float(symbols["GOOGL"]["close"]), 2),
            "q3_revenue_b": 127.577,
            "q3_revenue_growth_pct": 25.0,
            "q3_search_revenue_growth_pct": 12.0,
            "q3_gaap_operating_margin_pct": 31.8,
            "q3_gaap_eps": 2.12,
            "current_quarter_gaap_run_rate_pe": multiple(
                float(symbols["GOOGL"]["close"]), 2.12
            ),
            "secondary_vendor_forward_pe": round(float(symbols["GOOGL"]["forwardPE"]), 1),
            "ttm_operating_cash_flow_b": 179.551,
            "ttm_capex_b": 159.804,
            "ttm_free_cash_flow_b": 19.747,
            "jqua_weight_pct": weight_by_ticker.get("GOOGL", 0.0),
            "interpretation": "Search was not in current operating decline, but AI capital intensity and long-run search disruption remain legitimate risks.",
        },
        "microsoft_context": {
            "price": round(float(symbols["MSFT"]["close"]), 2),
            "q1_fy2027_revenue_b": 92.3,
            "q1_fy2027_revenue_growth_pct": 19.0,
            "q1_fy2027_gaap_operating_income_b": 45.9,
            "q1_fy2027_gaap_operating_margin_pct": round(45.9 / 92.3 * 100, 1),
            "q1_fy2027_gaap_eps": 4.92,
            "current_quarter_gaap_run_rate_pe": multiple(
                float(symbols["MSFT"]["close"]), 4.92
            ),
            "secondary_vendor_forward_pe": round(float(symbols["MSFT"]["forwardPE"]), 1),
            "q1_operating_cash_flow_b": 58.0,
            "q1_capex_b": 39.367,
            "q1_free_cash_flow_b": 18.633,
            "jqua_weight_pct": weight_by_ticker.get("MSFT", 0.0),
            "interpretation": "Highest-quality broad AI platform in the watchlist, but already held through JQUA and additive direct exposure raises household technology concentration.",
        },
        "candidates": candidates,
        "silver": {
            "target_pct": SILVER_PLATINUM_TARGET_PCT,
            "target_value": round(silver_target_value, 2),
            "wpm_shares": WPM_SHARES,
            "wpm_price": round(wpm_price, 2),
            "wpm_value": round(wpm_value, 2),
            "wpm_gross_portfolio_pct": round(wpm_value / PORTFOLIO_VALUE * 100, 2),
            "wpm_revenue_mix_silver_pct": WPM_SILVER_REVENUE_MIX * 100,
            "wpm_revenue_mix_gold_pct": WPM_GOLD_REVENUE_MIX * 100,
            "illustrative_silver_lookthrough_value": round(silver_value, 2),
            "illustrative_silver_lookthrough_pct": round(silver_value / PORTFOLIO_VALUE * 100, 2),
            "illustrative_gold_lookthrough_value": round(gold_value, 2),
            "illustrative_gold_lookthrough_pct": round(gold_value / PORTFOLIO_VALUE * 100, 2),
            "wpm_shares_at_one_pct_silver_lookthrough": round(wpm_shares_at_silver_target, 1),
            "illustrative_excess_wpm_shares": round(WPM_SHARES - wpm_shares_at_silver_target, 1),
            "vehicles": {
                "SIVR": {
                    "effective_annual_fee_pct": 0.30,
                    "gross_fee_pct": 0.45,
                    "fee_note": "0.30% reflects a voluntary sponsor waiver that has existed since inception.",
                    "structure": "Physical silver trust; all silver was held at ICBC or a sub-custodian at 2026-03-31.",
                    "use": "Default long-term brokerage vehicle.",
                },
                "SLV": {
                    "annual_fee_pct": 0.50,
                    "structure": "Physical silver trust.",
                    "use": "Best for a short tactical trade or options because volume is much higher.",
                },
                "PSLV": {
                    "management_expense_ratio_pct": 0.52,
                    "premium_discount_pct_at_as_of": -4.26,
                    "structure": "Closed-end Canadian trust holding fully allocated LGD silver bars.",
                    "use": "Do not default to it in U.S. taxable: PFIC/QEF election and annual Form 8621 burden.",
                },
                "OneGold": {
                    "annual_silver_storage_pct": 0.30,
                    "minimum_storage_fee": "$5 per quarter at the account level",
                    "use": "Custody diversification for a long-term holding; compare the live buy/sell spread before purchase.",
                },
            },
        },
        "recommended_policy": {
            "default_quality_sleeve": "5.5% JQUA",
            "active_variant_only_if_monitoring_cycle": "4.5% JQUA + up to 1.0% LRCX, funded dollar-for-dollar from JQUA",
            "current_action": "Keep JQUA; do not buy any of the seven direct names merely because of the one-day decline.",
            "watch_entries": {
                "LRCX": "Re-underwrite near $205 or when confirmed earnings reduce the GAAP forward multiple to about 22x.",
                "KLAC": "Re-underwrite near $140 or when confirmed earnings reduce the GAAP forward multiple to about 25x.",
            },
            "silver_action": "Do not add incremental silver while WPM remains at 154 shares; its illustrative silver revenue look-through is already about 1.38% of the portfolio.",
        },
    }
    (DATA / "comparison.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
