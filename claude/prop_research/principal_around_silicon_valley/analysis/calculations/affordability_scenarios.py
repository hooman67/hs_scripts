#!/usr/bin/env python3
"""Reproduce the Gate A affordability screening scenarios.

This is deliberately a small transparent calculator, not a lender model.
Change assumptions here and regenerate the adjacent CSV before citing results.
"""

from __future__ import annotations

import csv
from pathlib import Path


ANNUAL_MORTGAGE_RATE = 0.0676
TERM_MONTHS = 360
ANNUAL_PROPERTY_TAX_RATE = 0.012
MONTHLY_INSURANCE = 300.0
MONTHLY_UTILITIES = 500.0
ANNUAL_MAINTENANCE_RATE = 0.01
DOWN_PAYMENTS = (300_000, 400_000)
MONTHLY_ECONOMIC_CEILINGS = (5_000, 6_000, 7_000)


def mortgage_payment_factor(annual_rate: float, months: int) -> float:
    monthly_rate = annual_rate / 12
    growth = (1 + monthly_rate) ** months
    return monthly_rate * growth / (growth - 1)


def solve_purchase_price(down_payment: float, economic_ceiling: float) -> float:
    mortgage_factor = mortgage_payment_factor(ANNUAL_MORTGAGE_RATE, TERM_MONTHS)
    monthly_price_cost = (
        mortgage_factor
        + ANNUAL_PROPERTY_TAX_RATE / 12
        + ANNUAL_MAINTENANCE_RATE / 12
    )
    return (
        economic_ceiling
        - MONTHLY_INSURANCE
        - MONTHLY_UTILITIES
        + mortgage_factor * down_payment
    ) / monthly_price_cost


def scenario(down_payment: float, economic_ceiling: float) -> dict[str, float]:
    price = solve_purchase_price(down_payment, economic_ceiling)
    mortgage_factor = mortgage_payment_factor(ANNUAL_MORTGAGE_RATE, TERM_MONTHS)
    principal_and_interest = (price - down_payment) * mortgage_factor
    property_tax = price * ANNUAL_PROPERTY_TAX_RATE / 12
    maintenance = price * ANNUAL_MAINTENANCE_RATE / 12
    billed_cost = principal_and_interest + property_tax + MONTHLY_INSURANCE + MONTHLY_UTILITIES
    return {
        "down_payment_usd": down_payment,
        "economic_ceiling_monthly_usd": economic_ceiling,
        "purchase_price_usd": price,
        "loan_amount_usd": price - down_payment,
        "principal_interest_monthly_usd": principal_and_interest,
        "property_tax_monthly_usd": property_tax,
        "insurance_monthly_usd": MONTHLY_INSURANCE,
        "utilities_monthly_usd": MONTHLY_UTILITIES,
        "maintenance_reserve_monthly_usd": maintenance,
        "billed_cost_monthly_usd": billed_cost,
        "economic_carry_monthly_usd": billed_cost + maintenance,
    }


def main() -> None:
    output = Path(__file__).with_name("affordability_scenarios.csv")
    rows = [scenario(down, ceiling) for down in DOWN_PAYMENTS for ceiling in MONTHLY_ECONOMIC_CEILINGS]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow({key: f"{value:.2f}" for key, value in row.items()})
    print(output)


if __name__ == "__main__":
    main()
