"""Reproduce the Oct 20 comparison from saved quotes and primary-filing inputs.

Amounts are millions except price/EPS. This is a valuation screen, not a DCF.
EV uses financial net debt; leases are a separate sensitivity. Adjusted EBITDA
definitions differ between issuers. Sources and qualifications are in SUMMARY.md.
No network access or portfolio mutation.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def main():
    quotes = json.loads((DATA / "quotes.json").read_text())
    fx = quotes["CADUSD=X"]["info"]["regularMarketPrice"]
    # symbol, financial currency, primary shares, financial net debt, leases,
    # TTM adjusted EBITDA, illustrative multiple range (judgment, not targets).
    inputs = [
        ("EFXT", "USD", 122.103, 455.0, 68.0, 511 + 265 - 243, 5, 6),
        ("CGY.TO", "CAD", 11.512163, 94.915, 43.295, 100.515, 8, 9),
        ("BDGI.TO", "USD", 33.659562, 254.138, 73.278, 198.233 + 104.182 - 86.510, 8, 10),
        ("FTG.TO", "CAD", 25.173390, -3.868, 22.571, 40.800, 14, 16),
        ("VNP.TO", "USD", 89.935323, 23.655, 28.409, 92.443 + 55.786 - 44.938, 12, 14),
        ("MAL.TO", "CAD", 57.079054, 27.781, 28.096, 148.611, 9, 11),
        ("ELVA", "USD", 49.998897, 25.181, 2.792, 8.823 + 8.486 - 5.447, 12, 15),
    ]
    rows = []
    for sym, currency, shares, debt, leases, ebitda, lo, hi in inputs:
        info = quotes[sym]["info"]
        price = info["regularMarketPrice"]
        conversion = fx if info["currency"] == "CAD" and currency == "USD" else 1
        assert info["currency"] == currency or conversion == fx
        equity = price * conversion * shares
        ev = equity + debt
        r = dict(symbol=sym, quote_currency=info["currency"], financial_currency=currency,
                 price=price, shares_m=shares, net_debt_m=debt, leases_m=leases,
                 equity_value_m=equity, financial_ev_m=ev, ttm_adjusted_ebitda_m=ebitda,
                 ev_adjusted_ebitda=ev / ebitda,
                 lease_inclusive_ev_adjusted_ebitda=(ev + leases) / ebitda,
                 sensitivity_low_multiple=lo, sensitivity_high_multiple=hi,
                 sensitivity_low_price=(lo * ebitda - debt) / shares / conversion,
                 sensitivity_high_price=(hi * ebitda - debt) / shares / conversion)
        assert 0 < shares and 0 < ebitda and 2 < r["ev_adjusted_ebitda"] < 40
        assert r["lease_inclusive_ev_adjusted_ebitda"] >= r["ev_adjusted_ebitda"]
        rows.append(r)
    cf_eps = 1.26 + .36 - .13
    result = {"price_date": "2026-10-20", "cad_usd_fx": fx,
              "fx_note": "Saved spot snapshot retrieved Oct 21 UTC / Oct 20 Pacific; not exchange-close synchronized.",
              "method": "Latest basic share counts and balance sheets, not estimated current fully diluted shares. Financial EV excludes leases/earnouts; separate lease sensitivity. Range multiples are analyst assumptions, not objective fair values.",
              "industrial_companies": rows,
              "CF.TO": {"price_cad": 13.47, "approx_ttm_adjusted_eps_cad": cf_eps,
                        "adjusted_pe": 13.47 / cf_eps, "ifrs_ttm_eps_cad": -1.05,
                        "midcycle_assumed_eps_cad": 1.0, "midcycle_pe": 13.47}}
    (DATA / "valuation_comparison.json").write_text(json.dumps(result, indent=2) + "\n")
    with (DATA / "valuation_comparison.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

    past = json.loads((DATA / "past_picks.json").read_text())
    groups = defaultdict(list)
    for event in past["events"]:
        prices = past["prices"][event["ticker"]]
        a = next(x for x in prices if x["date"] == event["first_date"])
        b = next(x for x in prices if x["date"] == event["last_date"])
        gross = b["adj_close"] / a["adj_close"]
        if event["ticker"] == "CVEO":
            fx_bars = past["prices"]["CADUSD=X"]
            fxa = next(x for x in fx_bars if x["date"] == a["date"])["close"]
            fxb = next(x for x in fx_bars if x["date"] == b["date"])["close"]
            gross *= fxa / fxb
        assert abs(100 * (gross - 1) - event["total_return_cad_pct"]) < 1e-8
        bench = [x for x in past["prices"]["XIC.TO"] if a["date"] <= x["date"] <= b["date"]]
        assert abs(100 * (bench[-1]["adj_close"] / bench[0]["adj_close"] - 1)
                   - event["xic_total_return_cad_pct"]) < 1e-8
        groups[event["recommendation_date"]].append(event)
    assert len(groups) == 4 and all(len(x) == 3 for x in groups.values())
    cohorts = [{"date": date, "equal_weight_total_return_cad_pct": sum(e["total_return_cad_pct"] for e in es) / 3,
                "xic_total_return_cad_pct": es[0]["xic_total_return_cad_pct"]} for date, es in groups.items()]
    (DATA / "past_pick_cohorts.json").write_text(json.dumps(cohorts, indent=2) + "\n")
    assert abs(5_545_880 + 8_334_465 - 13_880_345) == 0
    assert abs(1.26 + .36 - .13 - 1.49) < 1e-9
    print(json.dumps({"valuation_rows": [{"symbol": r["symbol"], "multiple": round(r["ev_adjusted_ebitda"], 2),
                 "with_leases": round(r["lease_inclusive_ev_adjusted_ebitda"], 2),
                 "illustrative_range": [round(r["sensitivity_low_price"], 2), round(r["sensitivity_high_price"], 2)]}
                 for r in rows], "verified_pick_events": len(past["events"]), "cohorts": cohorts}, indent=2))


if __name__ == "__main__":
    main()
