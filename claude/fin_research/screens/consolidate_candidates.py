#!/usr/bin/env python3
"""
Stage 2.6 — Consolidate all FOUR screens into ONE region-balanced candidate list + a
locked ~15-name finalist shortlist for Stage-4 deep dives.

This SUPERSEDES screens/merge_candidates.py (which merged only Stage 1a + Stage 1b, before
the broadened ex-US/EM and financials screens existed). It reuses that script's bucket logic
(BOTH / B-only / A-only) and its curated Stage-1a-verdict + industry->Damodaran map verbatim,
but rebuilds the buckets from the fuller universe:

  NON-FINANCIALS  -> screens/quant_screen_global_merged_ranked.csv   (Stage 2.5a, as-of 2026-07-02)
                     the true global re-rank of the 1,128-name union (the PRIMARY ranking).
  FINANCIALS      -> screens/financials_screen_ranked.csv            (Stage 2.5b, as-of 2026-07-02)
                     banks/insurers/REITs, ranked within region x sub-group.
  SECTOR VERDICTS -> data/damodaran/history/sector_cheapness_{US,Global,Emerging}.csv
                     (Stage 1a, as-of 2026-01-05) -- carried in via the A_SECTORS table below.

ANTI-HALLUCINATION: nothing is refetched or invented here. Every number written to the output
CSVs is copied from the two ranked CSVs above. The bucketing + the A<->B sector join are
JUDGMENT (documented inline), region-gated. yfinance fields are VERIFIED real fetches but
UNVERIFIED vs a second source (a Stage-4 job). Damodaran sector verdicts are VERIFIED.

Outputs:
  data/candidates_both.csv     (overwrite) - BOTH bucket (1a-cheap sector + 1b gate PASS)
  data/candidates_bonly.csv    (overwrite) - B-only (elite cheap-quality, sector not 1a-cheap)
  data/candidates_afill.csv    (new)       - A-only-fill: best name found for each 1a EM sector
  data/candidates_demoted.csv  (overwrite) - passed 1b gate but in a 1a structurally-dying sector
  data/finalists.csv           (new)       - the locked ~15 region-balanced finalists

Reproduce: /opt/venv/bin/python3 screens/consolidate_candidates.py
"""
import csv, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MERGED = os.path.join(BASE, "screens", "quant_screen_global_merged_ranked.csv")
FIN = os.path.join(BASE, "screens", "financials_screen_ranked.csv")
OUT = os.path.join(BASE, "data")

def num(x):
    try: return float(x)
    except: return None

# ---------------------------------------------------------------------------
# Stage 1a verdicts (verbatim from screens/sector_cheapness.md + merge_candidates.py).
# Each Damodaran bucket -> (verdict, regions, note).
#   cheap_not_dying = on the Stage-1a shortlist -> makes a gated name BOTH (region-matched).
#   trap            = Stage-1a structural decline -> DEMOTE even if the 1b gate passed.
#   low_return_cheap= cheap but ROIC 3-7% -> not a quality-first candidate (excluded from BOTH).
# ---------------------------------------------------------------------------
A_SECTORS = {
    # developed cheap-not-dying shortlist
    "Information Services":  ("cheap_not_dying", "US/Global", "cheap vs own hist, ROIC ~22%; AI *sentiment* overhang on moaty ratings/index/IT-svc franchises. Segment-select."),
    "Beverage (Alcoholic)":  ("cheap_not_dying", "US/Global", "5th-pctile EV/EBITDA vs own 11yr; ROE at cyclical trough (destock/tariff). Avoid wine-heavy (structural)."),
    "Beverage (Soft)":       ("cheap_not_dying", "US/Global", "29% ROIC, P/B bottom of own range. Quality compounder on relative sale (dear vs peers)."),
    "Building Materials":    ("cheap_not_dying", "US",        "20% ROIC, cyclical housing trough w/ infra floor + 2026 vol growth guided."),
    "Household Products":    ("cheap_not_dying", "Global",    "23% ROIC, staples on cyclical cost/consumer squeeze, intact pricing power."),
    # EM cheap-not-dying shortlist
    "Insurance (Life)":      ("cheap_not_dying", "Emerging",  "Best cheap-EM risk/reward: cheap vs own hist AND peers, ROIC 15% / ROE 17.6%, secular premium runway."),
    "Transportation (Railroads)": ("cheap_not_dying", "Emerging", "Cheapest EM industry; cyclical trade/tariff discount. Low 6.8% ROIC -- watch quality."),
    "Trucking":              ("cheap_not_dying", "Emerging",  "Cyclical freight down-cycle; low EM vehicle penetration tailwind. Low ROIC -- be selective."),
    "Retail (Automotive)":   ("cheap_not_dying", "Emerging",  "Cyclical dealer-margin normalization; low penetration tailwind. Low ROIC -- be selective."),
    "Retail (Building Supply)": ("cheap_not_dying", "Emerging", "Cheap vs own hist, ROIC ~14%. Cyclical EM consumer."),
    "Shoe":                  ("cheap_not_dying", "Emerging",  "Cheap vs own hist, ROIC ~10%. Cyclical EM consumer."),
    "Education":             ("cheap_not_dying", "Emerging",  "CYCLICAL only for regulated EM tutoring survivors. AI-exposed edtech = trap."),
    # Stage-1a TRAPS (secular decline) -> DEMOTE any gated name here
    "Cable TV":              ("trap", "US/Global", "SECULAR bleedout -- cord-cut decline. Do NOT drill."),
    "Food Processing":       ("trap", "US/Global/Emerging", "SECULAR-lean: GLP-1 + MAHA/FDA UPF crackdown + private label."),
    # low-return cheap (not quality-first candidates)
    "Real Estate (Development)": ("low_return_cheap", "US", "ROIC 7% -- thin-return cheap."),
    "Utility (Water)":       ("low_return_cheap", "US/Global", "ROIC 6-7% -- thin-return cheap."),
    "R.E.I.T.":              ("low_return_cheap", "Global",   "ROIC 3.7% -- thin-return cheap."),
    # other Stage-1a cheap sectors (context; not on shortlist, not flagged trap)
    "Telecom. Services":     ("neutral", "US", "SECULAR-lean but not dying; cheap vs peers. Low-single-digit growth."),
    "Insurance (Prop/Cas.)": ("neutral", "US", "Cheap vs own hist EV/EBITDA. Not on quality-first shortlist."),
}

# Curated map: yfinance industry -> Damodaran bucket. Same spirit as merge_candidates.py,
# extended for the ex-US industries that now surface (Packaged Foods, Leisure=sportswear, etc.).
IND_MAP = {
    "Information Technology Services": "Information Services",
    "Financial Data & Stock Exchange": "Information Services",
    "Beverages - Brewers": "Beverage (Alcoholic)",
    "Beverages - Wineries & Distilleries": "Beverage (Alcoholic)",
    "Beverages - Non-Alcoholic": "Beverage (Soft)",
    "Household & Personal Products": "Household Products",
    "Insurance - Life": "Insurance (Life)",
    "Railroads": "Transportation (Railroads)",
    "Trucking": "Trucking",
    "Auto & Truck Dealerships": "Retail (Automotive)",
    "Footwear & Accessories": "Shoe",
    "Education & Training Services": "Education",
    "Packaged Foods": "Food Processing",
    "Food Distribution": "Food Processing",
    "Confectioners": "Food Processing",
    "Telecom Services": "Telecom. Services",
    "Building Materials": "Building Materials",
    "Home Improvement Retail": "Retail (Building Supply)",
}

def region_ok(damo_regions, name_region):
    if name_region == "US":       return "US" in damo_regions
    if name_region == "DEV_EXUS": return ("Global" in damo_regions or "US" in damo_regions)
    if name_region == "EM":       return "Emerging" in damo_regions
    return False

def load(path):
    with open(path) as f:
        return list(csv.DictReader(f))

def classify(rows, strong_cut=66.0):
    both, bonly, demoted = [], [], []
    for r in rows:
        if str(r.get("rankable","")).strip().lower() not in ("true","1"):
            continue
        ind = (r.get("yf_industry") or "").strip()
        damo_key = IND_MAP.get(ind)
        verdict = A_SECTORS.get(damo_key) if damo_key else None
        r["_damo_key"] = damo_key or ""
        r["_verdict"] = verdict[0] if verdict else "no_1a_sector"
        r["_damo_regions"] = verdict[1] if verdict else ""
        r["_damo_note"] = verdict[2] if verdict else ""
        gated = str(r.get("passes_trap_gate","")).strip().lower() in ("true","1")
        sc = num(r.get("combined_score")) or 0
        if verdict and verdict[0] == "cheap_not_dying" and region_ok(verdict[1], r["region"]) and gated:
            both.append(r)
        elif verdict and verdict[0] == "trap" and gated:
            demoted.append(r)
        elif gated and sc >= strong_cut:
            bonly.append(r)
    return both, bonly, demoted

# A-only fill: for each EM 1a-cheap sector, find the best gated name across ALL regions
# (EM preferred; note if the only quality name is dev-ex-US, i.e. sector still lacks an EM leader).
A_FILL_SECTORS = ["Insurance (Life)", "Transportation (Railroads)", "Trucking",
                  "Retail (Automotive)", "Retail (Building Supply)", "Shoe", "Education"]

def a_fill(nonfin_rows, fin_rows):
    """Return {sector: [candidate rows sorted best-first]} using both non-fin + financials."""
    fill = {s: [] for s in A_FILL_SECTORS}
    # non-financials by industry map
    for r in nonfin_rows:
        if str(r.get("rankable","")).strip().lower() not in ("true","1"): continue
        if str(r.get("passes_trap_gate","")).strip().lower() not in ("true","1"): continue
        key = IND_MAP.get((r.get("yf_industry") or "").strip())
        if key in fill:
            fill[key].append(("nonfin", r))
    # financials -> Insurance (Life) from the life sub-group
    for r in fin_rows:
        if str(r.get("rankable","")).strip().lower() not in ("true","1"): continue
        if r.get("sub_group") == "INSURER_LIFE" and r.get("trap_status") == "PASS":
            fill["Insurance (Life)"].append(("fin", r))
    def sc(item):
        _, r = item
        return -(num(r.get("combined_score")) or 0)
    for s in fill: fill[s].sort(key=sc)
    return fill

def write_csv(path, cols, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols)
        for r in rows:
            w.writerow([r.get(c,"") for c in cols])

# ---------------------------------------------------------------------------
# The LOCKED ~15 finalists (region-balanced, sector-diversified). Selection is JUDGMENT
# per the Stage-2.6 brief; all NUMBERS come from the ranked CSVs (looked up at runtime, not
# typed here). bucket/thesis/why are the human calls. src: 'nonfin' or 'fin'.
# ---------------------------------------------------------------------------
FINALISTS = [
    # ticker,        src,      region,     bucket,          sector_tag,             thesis / why it made the cut
    ("CTSH",        "nonfin", "US",       "BOTH",          "IT Services",          "Cheap moaty IT-services in the 1a-cheap Information-Services sector (AI-sentiment overhang); EV/EBITDA ~4.9, EY 17.5%, 7/7. Highest-conviction US BOTH name."),
    ("NEM",         "nonfin", "US",       "B-only",        "Gold miner",           "#2 globally: gold major, EV/EBITDA ~5.9, ROE 26%, 7/7. Best-quality large US miner; rank on ROE not the inflated ROIC-proxy."),
    ("EOG",         "nonfin", "US",       "B-only",        "Energy E&P",           "Best-quality US gas/oil E&P (ROE 18%, EY 12%, EV/EBITDA 5.8, strong FCF, 7/7) -- cheap in a non-1a-cheap sector."),
    ("INTU",        "nonfin", "US",       "B-only",        "Software (QARP)",      "Quality-at-a-price software: ROIC 38%, 81% GM, EY 13%, 7/7. The cleanest US compounder-on-sale."),
    ("TROW",        "fin",    "US",       "B-only",        "Asset manager",        "Fortress asset manager, ROE 19%, P/E 12.5, 4.6% yield, trap PASS -- cheap quality financial; cross-validated top-of-US in the financials screen."),

    ("K.TO",        "nonfin", "DEV_EXUS", "B-only",        "Gold miner",           "#3 globally: Kinross, ROE 35%, EV/EBITDA 7.8, 7/7 -- diversifies the miner exposure into Canada; rank on ROE."),
    ("BZU.MI",      "nonfin", "DEV_EXUS", "BOTH",          "Building Materials",   "Italian cement in the 1a-cheap Building-Materials sector, and it actually screens cheap (EV/EBITDA 6.0, P/B 1.2, EY 14.5%, 7/7) -- unlike trough-priced US aggregates VMC/MLM."),
    ("DGE.L",       "nonfin", "DEV_EXUS", "BOTH",          "Bev-Alcoholic",        "Developed-ex-US spirits leader in the 1a-cheap Beverage-Alcoholic trough; EV/EBITDA 9.2, 31% op margin, EY 10.8%."),
    ("ISP.MI",      "fin",    "DEV_EXUS", "A-fill/fin",    "Bank (Italy)",         "Best cheap developed-ex-US bank: Intesa Sanpaolo 1.5x book, ROE 14%, P/E 11, 6.3% yield, trap PASS. Diversifies into dev-exUS financials."),
    ("SREN.SW",     "fin",    "DEV_EXUS", "B-only/fin",    "Reinsurer",            "European reinsurer value-with-quality: Swiss Re 1.8x book, ROE 19.5%, P/E 10.3, ~5% yield, PASS -- best dev-exUS insurer cohort."),

    ("0883.HK",     "nonfin", "EM",       "B-only",        "Energy (China)",       "#1 globally (CNOOC): Chinese offshore oil, EV/EBITDA 3.1, EY 23.6%, P/B 1.0, 7/7 -- the single cheapest-and-quality name in the whole run."),
    ("NTES",        "nonfin", "EM",       "B-only",        "Internet (China)",     "Best-quality cheap Chinese internet: NetEase 66% GM, EV/EBITDA 6.4, FCFy 41%, 7/7. Net-cash, de-rated."),
    ("TCS.NS",      "nonfin", "EM",       "BOTH",          "IT Services (India)",  "EM leg of the 1a-cheap Information-Services sector: Tata Consultancy ROE 48%, EY 9.8%, 7/7 -- the EM BOTH name (region-gated out in v1)."),
    ("ITC.NS",      "nonfin", "EM",       "B-only",        "Staples (India)",      "Indian value-quality staple (tobacco/FMCG): ROIC 45%, ROE 29%, 36% op margin, EY 8.4% -- an EM cash compounder on sale."),
    ("0966.HK",     "fin",    "EM",       "A-fill/fin",    "Life Insurer (China)", "The EM Life-Insurance A-only leader (1a's top cheap-EM sector): China Taiping 0.71x book with 25.5% ROE, P/E 2.6, trap PASS, +earnings growth -- the cleanest of the China life cohort."),
    ("2601.HK",     "fin",    "EM",       "A-fill/fin",    "Life Insurer (China)", "Second EM life name for the sector (Hooman wants a couple): CPIC 0.72x book, ROE 17.4% -- matches the 1a sector profile almost exactly. FLAG: earningsGrowth -6% = cheap on trough, verify EV/VNB at Stage 4."),
]

def lookup(nonfin_by_t, fin_by_t, ticker, src):
    return (fin_by_t if src == "fin" else nonfin_by_t).get(ticker)

def main():
    nonfin = load(MERGED)
    fin = load(FIN)
    both, bonly, demoted = classify(nonfin)
    def key(r): return -(num(r.get("combined_score")) or 0)
    both.sort(key=key); bonly.sort(key=key); demoted.sort(key=key)
    fill = a_fill(nonfin, fin)

    os.makedirs(OUT, exist_ok=True)
    nf_cols = ["ticker","name","region","country","gics_sector","yf_industry","_damo_key","_verdict",
               "marketCap","currency","roic_proxy","roe","gross_margin","operating_margin",
               "earnings_yield_clean","fcf_yield","ev_ebitda_clean","trailingPE","priceToBook",
               "piotroski_lite","roic_unreliable","passes_trap_gate","combined_score","_damo_note"]
    write_csv(os.path.join(OUT,"candidates_both.csv"),    nf_cols, both)
    write_csv(os.path.join(OUT,"candidates_bonly.csv"),   nf_cols, bonly)
    write_csv(os.path.join(OUT,"candidates_demoted.csv"), nf_cols, demoted)

    # A-fill csv (mixed schema: keep a common subset)
    with open(os.path.join(OUT,"candidates_afill.csv"),"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["sector_1a","src","ticker","name","region","country","industry_or_sub",
                    "roe","ev_ebitda","priceToBook","trailingPE","earnings_yield_or_divy",
                    "combined_score","trap"])
        for s in A_FILL_SECTORS:
            for src, r in fill[s][:5]:
                if src=="nonfin":
                    w.writerow([s,src,r["ticker"],r["name"],r["region"],r.get("country",""),
                        r.get("yf_industry",""), r.get("roe",""), r.get("ev_ebitda_clean",""),
                        r.get("priceToBook",""), r.get("trailingPE",""),
                        r.get("earnings_yield_clean",""), r.get("combined_score",""),
                        r.get("passes_trap_gate","")])
                else:
                    w.writerow([s,src,r["ticker"],r["name"],r["region"],r.get("country",""),
                        r.get("sub_group",""), r.get("roe",""), "",
                        r.get("priceToBook",""), r.get("trailingPE",""),
                        r.get("dividendYield_pct",""), r.get("combined_score",""),
                        r.get("trap_status","")])

    # finalists.csv -- numbers pulled from the ranked CSVs at runtime (never typed)
    nonfin_by_t = {r["ticker"]: r for r in nonfin}
    fin_by_t    = {r["ticker"]: r for r in fin}
    fcols = ["rank","ticker","name","region","sector_tag","bucket","src","marketCap","currency",
             "roe","roic_proxy","operating_margin","ev_ebitda","earnings_yield","trailingPE",
             "priceToBook","div_yield_pct","piotroski_or_trap","combined_score","thesis"]
    frows = []
    for i,(t,src,region,bucket,stag,thesis) in enumerate(FINALISTS,1):
        r = lookup(nonfin_by_t, fin_by_t, t, src)
        if r is None:
            print(f"WARN finalist not found: {t} ({src})"); continue
        if src=="nonfin":
            frows.append({"rank":i,"ticker":t,"name":r["name"],"region":region,"sector_tag":stag,
                "bucket":bucket,"src":src,"marketCap":r.get("marketCap",""),"currency":r.get("currency",""),
                "roe":r.get("roe",""),"roic_proxy":("(unreliable)" if str(r.get("roic_unreliable"))=="True" else r.get("roic_proxy","")),
                "operating_margin":r.get("operating_margin",""),"ev_ebitda":r.get("ev_ebitda_clean",""),
                "earnings_yield":r.get("earnings_yield_clean",""),"trailingPE":r.get("trailingPE",""),
                "priceToBook":r.get("priceToBook",""),"div_yield_pct":"",
                "piotroski_or_trap":f"{r.get('piotroski_lite','')}/7","combined_score":r.get("combined_score",""),
                "thesis":thesis})
        else:
            frows.append({"rank":i,"ticker":t,"name":r["name"],"region":region,"sector_tag":stag,
                "bucket":bucket,"src":src,"marketCap":r.get("marketCap",""),"currency":r.get("currency",""),
                "roe":r.get("roe",""),"roic_proxy":"","operating_margin":"","ev_ebitda":"",
                "earnings_yield":"","trailingPE":r.get("trailingPE",""),"priceToBook":r.get("priceToBook",""),
                "div_yield_pct":r.get("dividendYield_pct",""),"piotroski_or_trap":r.get("trap_status",""),
                "combined_score":r.get("combined_score",""),"thesis":thesis})
    write_csv(os.path.join(OUT,"finalists.csv"), fcols, frows)

    # summary
    mix = {}
    for f in frows: mix[f["region"]] = mix.get(f["region"],0)+1
    print(f"BOTH={len(both)}  B-only(sc>=66)={len(bonly)}  DEMOTED(1a-trap)={len(demoted)}")
    print(f"finalists={len(frows)}  region mix={mix}")
    print("\n=== BOTH (top 12) ===")
    for r in both[:12]:
        print(f"  {r['ticker']:12s} {r['region']:8s} {r['_damo_key']:22s} sc={r['combined_score']:>5s} evb={r['ev_ebitda_clean']:>6s}")
    print("\n=== A-fill best per EM 1a sector ===")
    for s in A_FILL_SECTORS:
        top = fill[s][:1]
        if top:
            src,r = top[0]
            reg=r["region"]; note=" (NO EM leader -- dev-exUS only)" if reg!="EM" else ""
            print(f"  {s:26s} -> {r['ticker']:10s} {reg:8s} sc={r.get('combined_score','')}{note}")
        else:
            print(f"  {s:26s} -> NONE FOUND (sector still lacks a quality leader)")

if __name__ == "__main__":
    main()
