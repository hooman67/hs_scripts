#!/usr/bin/env python3
"""
Stage 2 — merge & cross-validate Stage 1a (sector cheapness) and Stage 1b (quant screen).

Reads (does NOT refetch — reuses upstream numbers):
  - screens/quant_screen_ranked.csv                       (Stage 1b, as-of 2026-07-02)
  - data/damodaran/history/sector_cheapness_{US,Global,Emerging}.csv  (Stage 1a, as-of 2026-01-05)

Produces the three buckets (BOTH / B-only / A-only watchlist) as CSVs under data/ and
prints a summary. The human-readable writeup is screens/candidates.md.

The A<->B join is by SECTOR, via a CURATED map from each Stage-1b name's yfinance
gics_sector + yf_industry to the relevant Damodaran industry bucket. This is a JUDGMENT
map (documented inline) — kept small and auditable rather than a fuzzy auto-match, because
mis-mapping a name would corrupt the bucketing. Every Stage-1a verdict (cheap-not-dying vs
trap) comes verbatim from screens/sector_cheapness.md.
"""
import csv, os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RANKED = os.path.join(BASE, "screens", "quant_screen_ranked.csv")
HIST = os.path.join(BASE, "data", "damodaran", "history")
OUT = os.path.join(BASE, "data")

def num(x):
    try: return float(x)
    except: return None

# ---------------------------------------------------------------------------
# Stage 1a verdicts (from screens/sector_cheapness.md, VERIFIED multiples + web verdicts).
# Each Damodaran bucket -> ('cheap_not_dying' | 'trap' | 'low_return_cheap'), regions, note.
# cheap_not_dying = on the Stage-1a shortlist (makes a Stage-1b name BOTH).
# trap / low_return_cheap = Stage-1a flagged; a Stage-1b name here is DEMOTED.
# ---------------------------------------------------------------------------
A_SECTORS = {
    # --- developed cheap-not-dying shortlist ---
    "Information Services":  ("cheap_not_dying", "US/Global", "cheap vs own hist, ROIC ~22%; AI *sentiment* overhang on moaty ratings/index franchises. Segment-select."),
    "Beverage (Alcoholic)":  ("cheap_not_dying", "US/Global", "5th-pctile EV/EBITDA vs own 11yr; ROE at cyclical trough (destock/tariff). Avoid wine-heavy (structural)."),
    "Beverage (Soft)":       ("cheap_not_dying", "US/Global", "29% ROIC, P/B bottom of own range. Quality compounder on relative sale (dear vs peers)."),
    "Building Materials":    ("cheap_not_dying", "US",        "20% ROIC, cyclical housing trough w/ infra floor + 2026 vol growth guided."),
    "Household Products":    ("cheap_not_dying", "Global",    "23% ROIC, staples on cyclical cost/consumer squeeze, intact pricing power."),
    # --- EM cheap-not-dying shortlist ---
    "Insurance (Life)":      ("cheap_not_dying", "Emerging",  "Best cheap-EM risk/reward: cheap vs own hist AND peers, ROIC 15% / ROE 17.6%, secular premium runway."),
    "Transportation (Railroads)": ("cheap_not_dying", "Emerging", "Cheapest EM industry; cyclical trade/tariff discount, infra spend growing. Low 6.8% ROIC — watch quality."),
    "Trucking":              ("cheap_not_dying", "Emerging",  "Cyclical freight down-cycle; low EM vehicle penetration tailwind. Low ROIC — be selective."),
    "Retail (Automotive)":   ("cheap_not_dying", "Emerging",  "Cyclical dealer-margin normalization; low penetration tailwind. Low ROIC — be selective."),
    "Retail (Building Supply)": ("cheap_not_dying", "Emerging", "Cheap vs own hist, ROIC ~14%. Cyclical EM consumer."),
    "Shoe":                  ("cheap_not_dying", "Emerging",  "Cheap vs own hist, ROIC ~10%. Cyclical EM consumer."),
    "Education":             ("cheap_not_dying", "Emerging",  "CYCLICAL only for regulated EM tutoring survivors (New Oriental). AI-exposed edtech = trap."),

    # --- Stage-1a TRAPS (secular decline) — DEMOTE any Stage-1b name here ---
    "Cable TV":              ("trap", "US/Global", "SECULAR bleedout — cheapest of all but confirmed cord-cut decline. Do NOT drill."),
    "Food Processing":       ("trap", "US/Global/Emerging", "SECULAR-lean: GLP-1 + MAHA/FDA UPF crackdown + private label. Cheap for a reason."),

    # --- low-return cheap (not quality-first candidates) ---
    "Real Estate (Development)": ("low_return_cheap", "US", "ROIC 7% — cheap partly because returns are structurally thin."),
    "Utility (Water)":       ("low_return_cheap", "US/Global", "ROIC 6-7% — thin-return cheap."),
    "R.E.I.T.":              ("low_return_cheap", "Global",   "ROIC 3.7% — thin-return cheap."),

    # --- other Stage-1a cheap sectors (context; not on shortlist, not flagged trap) ---
    "Telecom. Services":     ("neutral", "US",       "SECULAR-lean but not dying; cheap vs peers (xsec 4). Low-single-digit growth."),
    "Insurance (Prop/Cas.)": ("neutral", "US",       "Cheap vs own hist EV/EBITDA (14th pctile). Not on quality-first shortlist."),
}

# ---------------------------------------------------------------------------
# Curated map: Stage-1b (gics_sector, yf_industry) -> Damodaran bucket key above.
# Keyed by yf_industry (finer). Anything not mapped -> ('__unmapped__', reason by gics).
# Only industries that appear near the top of the 1b ranking need entries; the rest
# fall through to "sector not on any Stage-1a cheap list" (B-only-if-strong / ignore).
# ---------------------------------------------------------------------------
IND_MAP = {
    # Information Services family (Damodaran "Information Services")
    "Information Technology Services": "Information Services",   # IT consulting/data svcs (CTSH, ACN, TCS, INFY, WIT)
    "Financial Data & Stock Exchange": "Information Services",   # CBOE, exchanges/data (S&P/Moody's-type)
    # Beverages
    "Beverages - Brewers": "Beverage (Alcoholic)",              # ABEV, FMX
    "Beverages - Wineries & Distilleries": "Beverage (Alcoholic)",  # BF-B (wine flag -> caution)
    "Beverages - Non-Alcoholic": "Beverage (Soft)",             # KO/PEP-type
    # Household / staples
    "Household & Personal Products": "Household Products",
    # EM life insurance
    "Insurance - Life": "Insurance (Life)",
    # EM transport / auto retail (rare in 1b large-cap universe)
    "Railroads": "Transportation (Railroads)",
    "Trucking": "Trucking",
    "Auto & Truck Dealerships": "Retail (Automotive)",
    "Footwear & Accessories": "Shoe",                            # DECK (US) -> Shoe is EM-only in 1a; region gate handles it
    "Education & Training Services": "Education",
    # Traps
    "Packaged Foods": "Food Processing",
    "Food Distribution": "Food Processing",
    "Confectioners": "Food Processing",
    "Telecom Services": "Telecom. Services",
    "Building Materials": "Building Materials",
}

# Region compatibility: a Stage-1a bucket verdict is region-scoped. A US name only counts
# as BOTH if the sector is cheap-not-dying in US or US/Global; an EM name needs the EM verdict.
def region_ok(damo_regions, name_region):
    dr = damo_regions
    if name_region == "US":
        return ("US" in dr)
    if name_region == "DEV_EXUS":
        return ("Global" in dr or "US" in dr)  # developed ex-US best matched by US/Global Damodaran
    if name_region == "EM_CORE":
        return ("Emerging" in dr)
    return False

def load_ranked():
    rows = []
    with open(RANKED) as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows

def classify(rows):
    both, bonly, demoted = [], [], []
    for r in rows:
        ind = r["yf_industry"].strip()
        damo_key = IND_MAP.get(ind)
        r["_damo_key"] = damo_key or ""
        verdict = A_SECTORS.get(damo_key) if damo_key else None
        r["_verdict"] = verdict[0] if verdict else "no_1a_sector"
        r["_damo_regions"] = verdict[1] if verdict else ""
        r["_damo_note"] = verdict[2] if verdict else ""
        gated = r["passes_trap_gate"].strip().lower() in ("true", "1")
        r["_gated"] = gated
        sc = num(r["combined_score"]) or 0

        if verdict and verdict[0] == "cheap_not_dying" and region_ok(verdict[1], r["region"]) and gated:
            both.append(r)
        elif verdict and verdict[0] in ("trap",) and gated:
            demoted.append(r)   # 1a-flagged trap sector -> demote even if 1b gate passed
        else:
            # B-only candidate: strong 1b name whose sector is NOT a 1a cheap-not-dying sector
            if gated and sc >= 66:  # strong-only
                bonly.append(r)
    return both, bonly, demoted

def main():
    rows = load_ranked()
    both, bonly, demoted = classify(rows)
    def key(r): return -(num(r["combined_score"]) or 0)
    both.sort(key=key); bonly.sort(key=key); demoted.sort(key=key)

    os.makedirs(OUT, exist_ok=True)
    cols = ["ticker","name","region","gics_sector","yf_industry","_damo_key","_verdict",
            "marketCap","currency","roic_proxy","roe","gross_margin","operating_margin",
            "earnings_yield_ebit_ev","fcf_yield","ev_ebitda_clean","trailingPE","priceToBook",
            "piotroski_lite","passes_trap_gate","combined_score","_damo_note"]
    for name, bucket in [("both", both), ("bonly", bonly), ("demoted", demoted)]:
        with open(os.path.join(OUT, f"candidates_{name}.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(cols)
            for r in bucket:
                w.writerow([r.get(c, "") for c in cols])

    print(f"BOTH: {len(both)}   B-only(strong, sc>=66): {len(bonly)}   DEMOTED(1a-trap sector): {len(demoted)}")
    for lbl, bk in [("BOTH", both), ("B-ONLY", bonly[:25]), ("DEMOTED", demoted)]:
        print(f"\n=== {lbl} ===")
        for r in bk:
            print(f"  {r['ticker']:12s} {r['region']:9s} {r['_damo_key'] or r['gics_sector']:24s} "
                  f"sc={r['combined_score']:>5s} evb={r['ev_ebitda_clean']:>6s} "
                  f"ind={r['yf_industry'][:26]}")

if __name__ == "__main__":
    main()
