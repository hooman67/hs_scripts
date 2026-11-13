# Ex-US / EM Cheap-Quality Screen — REFRESH 2026-08-26

**What this is.** A re-run of the existing Stage-2.5a bottom-up, quality-first cheap screen
over the **developed-ex-US + emerging-market universe** (European indices, Japan, Canada,
India NIFTY, HK/China, Korea, Taiwan, Brazil, Mexico, SE-Asia, S.Africa, Nordics) on **live
prices as of 2026-08-26**. Method, code, universe, and scoring are UNCHANGED from the
2026-07-02 run — same `derive_metrics` / `piotroski_lite` / `score_and_rank`, same **60%
quality / 40% cheapness** combined percentile score, same trap gate. Only the data is new.

- **Run date / as-of:** yfinance `.info` pulled **2026-08-26 ~18:02–18:04 UTC** (timestamp on
  every row; e.g. `2026-08-26T18:02:09+00:00`). Prices move daily — treat every number as-of
  this pull. **Confidence: individual pulled fields VERIFIED** (real fetch, `--refresh`, no
  cache); the ranking/cross-name comparison ASSUMED (single-source snapshot, proxy metrics).
- **Universe:** 740 ex-US/EM non-financials (448 dev-ex-US + 292 EM), from cited Wikipedia
  index tables + curated large-cap lists (`screens/universe_exus.py`). Financials/REITs
  excluded by design (parallel financials agent's turf) — 32 dropped by yfinance sector at
  scoring, ~108 more by ticker upstream.
- **Code:** `screens/run_quant_screen_exus.py` (imports the Stage-1b scorer verbatim) +
  `screens/universe_exus.py`. **Outputs (this refresh):**
  `screens/refresh_2026-08/quant_screen_exus_raw.csv` (740 rows),
  `.../quant_screen_exus_ranked.csv` (673 rankable),
  `.../quant_screen_exus_coverage.csv`, `.../top_gated_deduped.csv` (458 gated, deduped),
  `.../run_log.txt`. Live/master copies also in `screens/`.
- **Owner:** Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.**

> ⚠️ **ALL KNOWN GOTCHAS HONORED** (see `LEARNINGS.md`): (1) `.L` London names — Yahoo labels
> currency `GBp`/pence but reports `marketCap` in whole GBP; NOT divided by 100. (2) yfinance
> MIXES currencies for foreign-filer ADRs → EV/EBITDA, P/B, FCF-yield on ADR rows are SUSPECT
> and must be rebuilt in one currency before any deep dive (NTES P/B 16, TSM P/B 87 are exactly
> this artifact — flagged, not used cross-currency). (3) ROIC-proxy >100% = buyback-depressed-
> equity artifact → blanked from the quality rank, ROE substituted. (4) ADR-vs-native dual
> listings deduped (NTES↔9999.HK, etc. — kept the higher-scoring line). (5) net-cash firms
> show negative/near-zero EV → EV/EBITDA guard blanks values <2 so they don't drive the rank
> (PDD −3.3, TME 0.3, BIDU 0.1 rank on P/E, P/B, FCF-yield instead).

---

## 1. Coverage (live, 2026-08-26)

| Region | n | reachable | usable (≥8/11 fields) | reachable % | **usable %** | mean key fields |
|---|--:|--:|--:|--:|--:|--:|
| DEV_EXUS | 448 | 445 | 433 | 99.3% | **96.7%** | 10.6 |
| EM | 292 | 276 | 275 | 94.5% | **94.2%** | 9.8 |

Essentially identical to July (95–97% usable). The ~20 unreachable are the same cosmetic
wrong/renamed Yahoo symbols (`ELET3/6.SA`, `EMBR3.SA`, `BRFS3.SA`, `MRFG3.SA`, `ALFAA.MX`,
`IOI.KL`, `TEF`), not a data hole. **Free yfinance still suffices for large-cap ex-US/EM.**

---

## 2. Top 25 ex-US / EM cheap-quality names (gated, deduped, live)

Ranked by the **60/40 quality-first combined percentile score** within the ex-US/EM pool.
All names shown **PASS the trap gate** (FCF>0, Piotroski-lite ≥60%, D/E<300%). `Q/C` =
quality / cheapness percentile within this set. Multiples are live yfinance 2026-08-26.
**⚠ = data artifact** (see §col notes). MktCap omitted (native-currency, not cross-comparable).

| # | Ticker | Name | Region | Country | Sector | P/E | fwd P/E | EV/EBITDA | P/B | ROE | FCF yld | Q/C | **Score** | Verdict |
|--:|---|---|---|---|---|--:|--:|--:|--:|--:|--:|:--:|--:|---|
| 1 | 0883.HK | CNOOC | EM | China/HK | Energy | 8.3 | 6.7 | 4.0 | 1.2 | 15% | 6% | 89/88 | **88.7** | cheap-quality |
| 2 | 000660.KS | SK Hynix | EM | S.Korea | Technology | – | 3.6 | 7.9 | – | 93% | 5% | 94/77 | **87.1** | quality, cyc-peak⚠ |
| 3 | 005930.KS | Samsung Elec | EM | S.Korea | Technology | – | 3.8 | 6.9 | – | 31% | 4% | 90/78 | **85.2** | cheap-quality |
| 4 | FRES.L | Fresnillo | DEV | Mexico/UK | Materials | 13.8 | 14.3 | 5.5 | 6.1 | 53% | 9% | 93/72 | **84.8** | quality, gold-peak⚠ |
| 5 | PDD | PDD Holdings | EM | China | Cons. Cyc. | 8.9 | 6.9 | net-cash | 1.9 | 23% | 61% | 85/84 | **84.5** | cheap-quality |
| 6 | 2331.HK | Li Ning | EM | China | Cons. Cyc. | 10.0 | 10.4 | 4.5 | 1.0 | 11% | 6% | 77/89 | **81.8** | cheap-quality |
| 7 | NTES | NetEase | EM | China | Comm. Svcs | 16.5 | 11.6 | 5.9 | 16.0⚠ | 20% | 41%⚠ | 88/71 | **81.3** | cheap-quality (ADR fx⚠) |
| 8 | K.TO | Kinross Gold | DEV | Canada | Materials | 12.4 | 10.7 | 9.8 | 4.0 | 37% | 6% | 92/64 | **80.4** | quality, gold-peak⚠ |
| 9 | EDV.L | Endeavour Mining | DEV | UK | Materials | 19.1 | 9.1 | 4.1 | 4.6 | 31% | 15% | 83/74 | **79.1** | quality, gold-peak⚠ |
| 10 | SU.TO | Suncor Energy | DEV | Canada | Energy | 12.2 | 11.8 | 5.9 | 2.2 | 19% | 9% | 78/81 | **78.8** | cheap-quality (NEW) |
| 11 | TSM | TSMC | EM | Taiwan | Technology | 31.1 | 19.2 | 4.7 | 87.1⚠ | 40% | 34%⚠ | 89/63 | **78.6** | quality, not cheap (ADR fx⚠) |
| 12 | ABX.TO | Barrick Mining | DEV | Canada | Materials | 12.4 | 10.8 | 9.3 | 2.9 | 27% | 5% | 87/66 | **78.4** | quality, gold-peak⚠ |
| 13 | NHY.OL | Norsk Hydro | DEV | Norway | Materials | 18.7 | 10.3 | 4.0 | 1.8 | 9% | 11% | 74/82 | **77.1** | cheap-cyclical |
| 14 | TME | Tencent Music | EM | China | Comm. Svcs | 10.3 | 8.7 | net-cash | 1.2 | 11% | 38% | 69/89 | **77.1** | cheap-quality |
| 15 | LREN3.SA | Lojas Renner | EM | Brazil | Cons. Cyc. | 7.2 | 6.3 | 5.2 | 1.0 | 14% | 13% | 64/92 | **75.6** | cheap (NEW) |
| 16 | PBR | Petrobras | EM | Brazil | Energy | 4.5 | 4.5 | 1.8 | 1.2 | 30% | 82% | 63/93 | **75.1** | cheap (SOE/div risk) |
| 17 | INDF.JK | Indofood Sukses | EM | Indonesia | Cons. Def. | 6.7 | 5.6 | 4.5 | 0.8 | 12% | 19% | 61/95 | **74.6** | cheap-staple |
| 18 | PETR4.SA | Petrobras (PN) | EM | Brazil | Energy | 4.1 | 4.2 | 3.5 | 1.1 | 30% | 16% | 61/95 | **74.4** | cheap (SOE/div risk) |
| 19 | NEM.AX | Newmont (CDI) | DEV | US/AU | Materials | 16.7 | 12.9 | 11.2 | 4.0 | 26% | 5% | 88/54 | **74.3** | quality, gold-peak⚠ |
| 20 | PETR3.SA | Petrobras (ON) | EM | Brazil | Energy | 4.5 | 3.1 | 3.7 | 1.2 | 30% | 16% | 61/94 | **74.1** | cheap (SOE/div risk) |
| 21 | SQM | Soc. Quimica y Minera | EM | Chile | Materials | 16.1 | 11.1 | 8.6 | 3.5 | 22% | 12% | 77/70 | **74.0** | quality (lithium) (NEW) |
| 22 | 035720.KS | Kakao | EM | S.Korea | Comm. Svcs | – | 19.1 | 4.9 | – | 4% | 21% | 60/94 | **73.5** | cheap, low-ROE (NEW) |
| 23 | FMG.AX | Fortescue (iron ore) | DEV | Australia | Materials | 13.5 | 15.9 | 6.8 | 1.9 | 14% | 6% | 71/74 | **72.5** | cheap-cyclical |
| 24 | AUTO.L | Auto Trader | DEV | UK | Comm. Svcs | 15.9 | 12.3 | 11.5 | 10.9 | 60% | 6% | 83/54 | **71.4** | quality compounder, fair |
| 25 | AEM.TO | Agnico Eagle | DEV | Canada | Materials | 18.5 | 17.3 | 15.2 | 3.8 | 23% | 3% | 91/42 | **71.3** | quality, gold-peak⚠ |

**Just outside (26–30):** Tenaris `TEN.MI` (71.3), Genomma Lab `LABB.MX` (71.2, NEW), Chugai
Pharma `4519.T` (71.1), Beiersdorf `BEI.DE` (71.1), Teck Resources `TECK-B.TO` (71.1).

Col notes: ⚠ P/B (NTES 16, TSM 87, Auto Trader 10.9) = ADR currency-mix or buyback-driven —
do NOT read as expensive/cheap without a same-currency rebuild. "net-cash" = EV/EBITDA guard
blanked (<2), name ranks on P/E, P/B, FCF-yld. Korea Tech P/E blank = yfinance omitted trailing
P/E; fwd P/E present (SK Hynix 3.6, Samsung 3.8 = extraordinarily cheap on the memory upcycle).

---

## 3. Are last run's ex-US/EM winners still cheap, or re-rated?

Live 2026-08-26 vs 2026-07-02. Financials (CPIC, Intesa) are OUT of this non-financial screen
universe — pulled directly for tracking.

| Name | Ticker | Jul-02 read | **Aug-26 P/E / fwd / EV-EBITDA / P/B / ROE** | Score | Gate | Verdict |
|---|---|---|---|--:|:--:|---|
| **CNOOC** | 0883.HK | #1, EV/EB 3.1, P/B 1.0 | 8.3 / 6.7 / 4.0 / 1.2 / 15% | **88.7** | PASS | **Still #1, still cheap-quality.** EV/EBITDA drifted 3.1→4.0 (mild re-rate) but remains the cheapest-and-quality name in the run. |
| **Buzzi** | BZU.MI | #6 dev-exUS, EV/EB 6.0, P/B 1.2 | 8.8 / 8.5 / 5.7 / 1.0 / 12% | 68.9 | PASS | **Still cheap** (P/B 1.2→1.0, EV/EB 6.0→5.7 — marginally cheaper). Score dipped only because the miner/energy cohort re-rated up around it; multiples essentially unchanged. Cement quality name still intact. |
| **NetEase** | NTES | #3 EM, P/E 16.7 | 16.5 / 11.6 / 5.9 / 16.0⚠ | **81.3** | PASS | **Still cheap-quality**, basically flat vs July. ADR currency-mix still distorts P/B (16) & FCF-yld (41%) — needs RMB rebuild at deep-dive. |
| **CPIC** (life ins.) | 2601.HK | EM-life leader, P/B 0.72, ROE 17.4% | P/E 4.7 / 4.5 / – / **P/B 0.78** / ROE 17.4% | (fin.) | n/a | **Still deep-value**, P/B ~0.78 (0.72→0.78), ROE 17.4%, 4.5% yield. Not in THIS screen (financial) — surfaces in the financials agent. Unchanged thesis. |
| **Intesa** | ISP.MI | Italian bank, ~1.5x P/B, ROE 14-17% | P/E 12.3 / 10.5 / – / **P/B 1.75** / ROE 14% / 5.6% yld | (fin.) | n/a | **Modestly RE-RATED UP** (P/B 1.5→1.75). Still reasonable + 5.6% div, but the deepest-value phase has passed. Financials-agent turf. |
| **ITC** | ITC.NS | #11 EM, 45% ROIC staple | 17.1 / 16.1 / 12.4 / 4.7 | 69.9 | **FAIL⚠** | **Fundamentals fine** (ROIC ~30%, cheap-ish) but yfinance DROPPED its ROE + FCF fields this snapshot → Piotroski 2/3 → gate fail. **Artifact, not a re-rate.** Still a quality staple; re-verify at deep-dive. |
| **Coal India** | COALINDIA.NS | #4 EM, 36% ROIC, EV/EB 5.5 | 8.0 / 7.1 / 5.1 / 2.1 | 86.2 | **FAIL⚠** | Same artifact — high score (86.2, would be top-5) but yfinance dropped ROE/FCF → Piotroski 3/3 gated out on the FCF>0 requirement. Multiples still cheap (P/E 8, EV/EB 5.1). **Data gap, not deterioration.** |
| **Diageo** | DGE.L | de-rated spirits | 30.5 / **13.5** / 9.5 / 4.8 / ROE 15% | 56.9 | PASS | **Cheaper on forward** (fwd P/E 13.5 vs trailing 30.5 = depressed trailing earnings), but trailing multiple + modest cheapness percentile keep it mid-pack. Quality intact; a recovery/normalization bet, not a screen-cheap name. |
| **Pernod Ricard** | RI.PA | #14 dev-exUS, P/B 1.0 | 12.1 / 11.6 / 10.1 / 1.1 / ROE 9% | 70.1 | PASS | **Still cheap** (P/B ~1.0-1.1 held), spirits-sector de-rating persists. Steady vs July. |
| **Miners (gold):** Kinross | K.TO | #1 dev-exUS | 12.4 / 10.7 / 9.8 / 4.0 / 37% | 80.4 | PASS | **Re-rated UP on gold strength.** EV/EBITDA 7.8→9.8, P/B 3.1→4.0. Still high-quality but the cheapness is fading — screens cheap on PEAK gold earnings (LEARNINGS caveat). |
| Barrick | ABX.TO | #3 dev-exUS | 12.4 / 10.8 / 9.3 / 2.9 / 27% | 78.4 | PASS | Similar — EV/EB 8.0→9.3, mild re-rate; quality intact, cheapness eroding on peak gold. |
| Newmont-AU | NEM.AX | #4 dev-exUS | 16.7 / 12.9 / 11.2 / 4.0 / 26% | 74.3 | PASS | Re-rated up (EV/EB 8.4→11.2). Now "fair" not cheap on peak gold. |
| Fresnillo | FRES.L | #5 dev-exUS | 13.8 / 14.3 / 5.5 / 6.1 / 53% | 84.8 | PASS | **Climbed to #4 overall** — but on record silver/gold. High quality, priced for peak. |
| Agnico Eagle | AEM.TO | #7 dev-exUS | 18.5 / 17.3 / 15.2 / 3.8 / 23% | 71.3 | PASS | Re-rated up (EV/EB 11.3→15.2). Quality yes, cheap no. |
| Endeavour Mining | EDV.L | #2 dev-exUS | 19.1 / 9.1 / 4.1 / 4.6 / 31% | 79.1 | PASS | Trailing P/E jumped but fwd 9.1 + EV/EB 4.1 still cheap; FCF-yld 15%. Holds up best of the gold cohort. |

**Bottom line on the winners:** CNOOC, NetEase, Buzzi, Pernod, CPIC unchanged/still cheap. The
**gold miners have re-rated UP** (Kinross/Barrick/Newmont/Agnico/Fresnillo) on record bullion —
still quality but now screening cheap on PEAK earnings, so treat their cheapness with the
usual normalize-to-mid-cycle discount (LEARNINGS). ITC & Coal India are UNCHANGED on the merits
— they only dropped out of the gate because yfinance omitted their ROE/FCF fields in this pull
(a data-completeness artifact; re-verify at deep-dive).

---

## 4. NEW cheap names vs 6 weeks ago

Names that surface prominently now and were NOT called out in the July top lists:

- **SK Hynix `000660.KS` (#2) & Samsung Electronics `005930.KS` (#3)** — Korean memory. The
  BIG mover: HBM/DRAM upcycle drove earnings up so hard that **fwd P/E collapsed to 3.6 / 3.8**
  while quality percentile is top-decile (SK Hynix ROE 93%). Screens as elite quality + very
  cheap. CAVEAT: memory is deeply cyclical — this is peak-of-cycle earnings, so the low fwd P/E
  partly reflects the market pricing a downcycle (same normalize-to-mid-cycle discipline as
  miners). Genuinely new and worth a look.
- **Suncor Energy `SU.TO` (#10)** — Canadian oil-sands integrated, cheap-quality (fwd P/E 11.8,
  EV/EB 5.9, 9% FCF-yld, ROE 19%). New entrant to the top tier vs July.
- **Lojas Renner `LREN3.SA` (#15)** — Brazilian apparel retailer, deeply cheap (P/E 7.2, P/B
  1.0, 13% FCF-yld) with decent quality. New.
- **SQM `SQM` (#21)** — Chilean lithium/specialty chem, quality name (ROE 22%, 12% FCF-yld) at
  a fair-cheap multiple. New relative to July's list.
- **Kakao `035720.KS` (#22)** — Korean internet, cheap (fwd P/E 19.1 is high but cheapness
  percentile 94 driven by low EV/EBITDA 4.9 + P/B) but LOW quality (ROE 4%) — borderline;
  watch for value-trap.
- **Genomma Lab `LABB.MX` (#27)** — Mexican OTC-pharma/consumer-health, cheap (P/E 8.2, fwd
  6.3, EV/EB 4.8, P/B 1.1). New.
- **Teck Resources `TECK-B.TO` (#30)** — Canadian base metals (copper/zinc), gated quality at
  a fair multiple. New.

The **Chinese internet cohort (PDD, NetEase, Tencent Music, Baidu, Li Ning)** and **EM
staples (Indofood twins)** and **Petrobras** all persist from July — still cheap, not new.

---

## 5. Sector / region clustering (top-40 gated, deduped)

- **Region:** 22 EM / 18 dev-ex-US — EM slightly leads, consistent with July's "ex-US/EM
  dominates the cheap-quality tier once the universe is fairly sized."
- **Sector:** the run is still **commodity-heavy** — Basic Materials 10 + Energy 8 = **18 of 40
  (45%)**. Then Consumer Defensive 6, Comm. Services 5, Technology 4, Consumer Cyclical 4,
  Healthcare 3. Same "cheap-cyclical-with-genuine-quality" engine as July, now with a Korean
  Tech (memory) cluster added.
- **Country:** Brazil 6 (5 of them Petrobras/materials + Lojas Renner) and Canada 6 (miners +
  Suncor) dominate, then S.Korea 3 (memory + Kakao), UK 3, Indonesia 3, China 3.
- **Read-through:** apply a sector cap if building a finalist list — a naive top-N is ~half
  commodities (miners on peak gold + Petrobras/energy). The non-commodity cheap-quality core =
  **CNOOC, Chinese internet (PDD/NTES/TME/Li Ning), Korean memory (cyc-caveat), EM staples
  (Indofood), Buzzi (cement), Auto Trader (compounder, fair-priced), Pernod (spirits).**

---

## 6. Buyability (Schwab / Questrade vs IBKR / HK access)

Practical for a Canadian investor (Questrade = Canadian retail; Schwab = US). NOT legal advice.

**Easy — US ADR or US-listed line (Schwab & Questrade both fine):**
- PDD, NetEase (NTES), Tencent Music (TME), Baidu (BIDU), TSMC (TSM), Petrobras (PBR),
  SQM, Newmont (NEM on NYSE too).

**Easy — major developed exchange (Questrade covers CA/most of these; Schwab intl desk):**
- Canada `.TO`: Kinross (K.TO), Barrick (ABX.TO — also NYSE `B`), Suncor (SU.TO — also NYSE
  `SU`), Agnico (AEM.TO — also NYSE `AEM`), Teck (TECK-B.TO — also NYSE `TECK`).
- UK `.L`: Fresnillo (FRES.L), Endeavour (EDV.L — also TSX `EDV.TO`), Auto Trader (AUTO.L).
- Europe: Buzzi (BZU.MI), Pernod (RI.PA), Norsk Hydro (NHY.OL), Tenaris (TEN.MI — also NYSE
  `TS`), Beiersdorf (BEI.DE), Chugai (4519.T), Diageo (DGE.L — also NYSE `DEO`).
- Brazil `.SA`, Australia `.AX`: usually available on Questrade/Schwab intl or via ADR
  (Fortescue = `FSUGY` OTC; Petrobras PBR).

**Needs IBKR / HK-China / Korea market access (harder on Schwab/Questrade retail):**
- **CNOOC (0883.HK)** — HK line; the #1 name needs HK access (IBKR). NOTE: CNOOC is on the
  OFAC NS-CMIC list — that binds US persons; per project LEARNINGS Hooman (Canadian, non-US-
  person) is outside its scope, but a **US broker (Schwab) may still refuse to execute it** as
  a compliance matter → use a non-US broker (Questrade/IBKR from Canada). Confirm broker policy.
- **Li Ning (2331.HK)**, other HK-only lines → IBKR/HK.
- **SK Hynix (000660.KS), Samsung (005930.KS), Kakao (035720.KS)** — Korea `.KS`; need IBKR or
  a broker with KRX access. (Samsung has a GDR / OTC `SSNLF` but illiquid.)
- **CPIC (2601.HK)**, **Indofood (INDF.JK)** — HK / Jakarta; IBKR.

---

## 7. Method & limitations (unchanged from Stage-2.5a)

- **Exact reuse, no new method.** `run_quant_screen_exus.py` imports `derive_metrics`,
  `piotroski_lite`, `score_and_rank` from `run_quant_screen.py`. Same guards (blank EV/EBITDA
  <2; flag ROIC>100% & swap in ROE), same trap gate (FCF>0 AND Piotroski-lite ≥60% AND
  D/E<300%), same 60/40 quality-first score. Combined scores are **percentiles within the
  ex-US/EM pool** — comparable only within this run, not vs the US screen or the July run's
  absolute scores (rank/relative moves are the signal).
- **Single-source snapshot.** One live yfinance pull (2026-08-26), no EDGAR/filing cross-check
  in this breadth stage. Every name advancing to a deep dive must be re-verified vs filings,
  and every ADR's EV/EBITDA / P/B / FCF-yld rebuilt in a single currency.
- **Trap gate is field-completeness-sensitive.** ITC & Coal India failed the gate ONLY because
  yfinance dropped their ROE/FCF fields this snapshot (not a fundamental change) — flagged in
  §3. When yfinance omits FCF, `fcf>0` can't be verified → gate fail. Do not read those as
  deteriorations.
- **Financials excluded by design** (CPIC, Intesa, banks) — see the parallel financials screen.
- **Confidence:** pulled fields VERIFIED (real fetch 2026-08-26); ranking/comparison ASSUMED.

---

## Verification log

```
Environment : /opt/venv/bin/python3, yfinance 1.5.1, pandas/numpy/lxml present
Universe    : screens/universe_exus.py -> 740 names (448 DEV_EXUS + 292 EM)
              (built from live Wikipedia index scrapes, browser UA — scrape succeeded)
Command     : /opt/venv/bin/python3 screens/run_quant_screen_exus.py --refresh
Data pull   : LIVE, cache bypassed (--refresh). as_of stamps 2026-08-26T18:02:09Z .. 18:04:07Z
Coverage    : DEV_EXUS 445/448 reachable, 433 usable (96.7%); EM 276/292 reachable, 275 usable (94.2%)
Dropped     : 32 yfinance-labelled Financial Services/REITs before scoring
Rankable    : 673 of 740; gated (trap-pass) after dedupe: 458
Unreachable : ELET3/6.SA, EMBR3.SA, BRFS3.SA, MRFG3.SA, ALFAA.MX, IOI.KL, TEF (cosmetic symbol issues)
Smoke test  : 0883.HK price 24.92 / PE 8.31; BZU.MI 41.86 / 8.79; NTES 123.79 / 16.53;
              ITC.NS 270.25 / 17.05; DGE.L 1736.5(pence) / 30.46 — all as_of 2026-08-26, err None
Outputs     : screens/refresh_2026-08/{quant_screen_exus_raw.csv, _ranked.csv, _coverage.csv,
              top_gated_deduped.csv, run_log.txt, quant_exus.md}
Gotchas honored: .L pence NOT /100; ADR currency-mix flagged (NTES/TSM P/B); ROIC>100% blanked;
              dual-listings deduped (NTES/9999.HK etc.); net-cash EV/EBITDA<2 guard active.
```
