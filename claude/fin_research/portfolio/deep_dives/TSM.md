# TSM — Taiwan Semiconductor Manufacturing Co. (US ADR) — Deep Dive

**Ticker:** TSM (NYSE ADR; 1 ADR = 5 ordinary shares) · **Underlying:** 2330.TW (Taiwan) · **Country:** Taiwan · **Sector:** Semiconductors — pure-play foundry
**Deep dive date:** 2026-08-26 · **Analyst:** Claude (Opus 4.8) for Hooman Shariati (Canadian, quality-first value investor)
**Reports in TWD; ADR trades USD.** FX used throughout: **1 USD = 31.851 TWD** (yfinance live, 2026-08-26). All prices as-of 2026-08-26 unless noted.

> ⚠️ **CURRENCY-DISTORTION FIX (per project LEARNING — yfinance mixes currencies for ADRs).**
> yfinance served three **garbage, currency-mixed** ratios for TSM that must NOT be used:
> `priceToBook = 87.1` (real ≈ **12.9**), `enterpriseToEbitda = 4.7` (real ≈ **21.8**),
> `enterpriseValue = $14.9T` (real ≈ **$2.1T**). The cause: it divides a **USD** market cap /
> per-ADR bookValue against **TWD** balance-sheet and EBITDA figures (financialCurrency = TWD,
> currency = USD). **Every multiple in this report is recomputed from raw TWD statements
> converted to USD at 31.851, cross-checked against the ADR market cap.** See §0 + Appendix.

> ⚠️ **HEADLINE FINDING.** TSM is the highest-quality business in the entire research universe —
> arguably the **widest moat in all of tech** — and, uniquely, it is NOT expensive on a forward
> basis (fwd P/E ~19–24x against **+40% USD revenue growth in 2026**, PEG well under 1). The
> catch is that its two dominant risks are **the two things Hooman most needs to avoid**: (1) an
> **un-hedgeable Taiwan-invasion tail** (potential near-total loss, wrong for a 3–5yr house
> horizon), and (2) it is a **levered bet on the AI-datacenter capex cycle** — the exact bubble
> Hooman worries about — layered on top of his already-large US-tech concentration ($732k Adobe
> + AMZN/GOOGL). So the verdict splits: **BUY-grade asset, WATCH-grade fit.** Best expressed as a
> small, capped EM-tail-sleeve position entered on weakness — explicitly NOT house-reserve money.

---

## 0. Verified snapshot (as-of 2026-08-26)

| Metric | Value | Source / confidence |
|---|---|---|
| ADR price | **$417.65** | yfinance live 2026-08-26 (prev close $417.41) — **VERIFIED** |
| 52-week range | **$225.63 – $479.00** | yfinance — **VERIFIED** (now ~13% below high) |
| Market cap | **~$2.166T** | yfinance — **VERIFIED** |
| ADR shares out | **~5.186B** (= 25.9B ordinary ÷ 5) | yfinance — **VERIFIED** |
| Net cash | **~$64.8B** (cash+ST inv $98.2B − debt $33.4B) | FY25 balance sheet, TWD→USD — **VERIFIED (calc)** |
| Enterprise value | **~$2.10T** (mkt cap − net cash) | derived — **VERIFIED (calc)**; ⚠️ NOT yfinance's $14.9T |
| **Trailing P/E (TTM)** | **~31.1** | mkt cap / TTM NI $69.6B — **VERIFIED (calc)** |
| P/E (FY2025) | ~40.6 | on FY25 NI $53.3B — **VERIFIED (calc)** |
| **Forward P/E** | **~19–24** | ~24x on est. FY26 EPS; ~19x on FY27 (yfinance fwdPE 19.2) — **VERIFIED/ASSUMED** |
| **P/B (clean)** | **~12.9** | mkt cap / equity $168.1B — **VERIFIED (calc)**; ⚠️ NOT yfinance's 87.1 |
| **EV/EBITDA (TTM, clean)** | **~21.8** | EV $2.10T / TTM EBITDA $96.4B — **VERIFIED (calc)**; ⚠️ NOT yfinance's 4.7 |
| P/S (TTM) | ~15.5 | mkt cap / TTM rev $139.4B — **VERIFIED (calc)** |
| ROE | **~32% (FY25) → ~40% (TTM)** | NI/equity; rising on margin surge — **VERIFIED (calc)** |
| FCF (FY25) | **~$31.2B** (OCF $71.4B − capex $40.3B) | TWD→USD — **VERIFIED (calc)** |
| FCF yield | ~1.4% (FY25) / higher on TTM | capex-cycle-suppressed — **VERIFIED (calc)** |
| Dividend yield | **~0.8–1.0%** (payout ~26%) | yfinance; NT$7.0/qtr, hiked ~+33% YoY — **VERIFIED** |
| Beta | ~1.26 | yfinance — **VERIFIED** |

**The currency corruption check the brief asked for — RESULT:** confirmed and corrected. The
ADR price ($417.65) and market cap ($2.166T) are USD-native and reliable. But yfinance's
`priceToBook`, `enterpriseToEbitda`, and `enterpriseValue` are **currency-mixed and unusable**
(off by 5–7x). Recomputing from raw TWD statements at 31.851 gives **P/B ~12.9, EV/EBITDA ~21.8,
EV ~$2.1T** — internally consistent (EV/EBITDA and P/E now agree in scale). Use these, never the
raw yfinance ratio fields, for any TSM (or ADR) decision.

---

## 1. Business & Thesis — the picks-and-shovels of AI, widest moat in tech

**What it is.** TSMC is the world's dominant **pure-play semiconductor foundry** — it manufactures
chips designed by others (Nvidia, Apple, AMD, Broadcom, Qualcomm, MediaTek), it does not design or
sell its own chips. It is the indispensable factory floor of the entire fabless semiconductor
industry.

- **Foundry share:** **>70% of the dedicated-foundry market** (73% in Q1 2026 per Counterpoint;
  Morningstar mid-2026). **~90%+ of true leading-edge** (3nm/2nm) capacity — Samsung is a distant
  #2 and Intel Foundry is years behind. *(Forbes 2026-07-13 / Counterpoint; Morningstar — **VERIFIED via subagent**.)*
- **Node mix (Q2 2026 wafer revenue):** 2nm 3%, 3nm 30%, 5nm 33%, 7nm 11% → **advanced (7nm & below) = 77% of revenue**. *(TSMC Q2-2026 release, 2026-07-16 — **VERIFIED**.)*
- **End-market mix (Q2 2026):** **HPC = 66% of revenue, +20% QoQ** (this bucket holds AI accelerators — it is the growth engine), Smartphone 22%, IoT 5%, Auto 4%. *(TSMC Q2 transcript — **VERIFIED**.)*

**Why it is the picks-and-shovels of AI.** Every leading AI accelerator on Earth — Nvidia's
Blackwell/Rubin, AMD's MI-series, Google TPU, Amazon Trainium, Broadcom's custom ASICs — is
fabricated by TSMC on 3nm/5nm, and packaged using TSMC's **CoWoS** advanced packaging. **Nvidia
booked ~60% of TSMC's CoWoS capacity through 2026** and has reportedly become TSMC's **largest
customer (>20% of 2026 revenue)**, overtaking Apple. *(Forbes 2026-07-13; Taiwan Economic Daily via Motley Fool 2026-08-25 — **VERIFIED/HEADLINE**.)* TSM is the toll-road: it profits from AI-compute buildout **regardless of which chip designer wins**, which makes it structurally less bubble-fragile than any single app-layer or model-layer name.

**The moat (arguably the widest in tech):**
1. **Leading-edge process lead** — a multi-year, possibly-widening lead at 3nm/2nm. Samsung's yields lag; Intel Foundry is unproven at scale. N2 (2nm) drew **~4x the tape-outs of N3** at the same stage and is **fully booked**. *(TrendForce/Design-Reuse; Simply Wall St 2026-07-15 — **VERIFIED**.)*
2. **Ruinous capital intensity** — a leading-edge fab costs $20–30B+. 2026 capex is **$60–64B**, 2027 reportedly heading toward ~$85B (UNVERIFIED). No one can casually replicate this; the ante alone deters competition.
3. **Customer lock-in / co-design** — TSMC co-develops process nodes with its top customers years ahead (Apple booked ~half of initial N2/A20 output). Switching foundries mid-cycle is a multi-year, yield-risking ordeal.
4. **Pricing power** — TSMC has pushed through **4 consecutive rounds** of advanced-node price hikes (up to +10% effective Jan 2027); N2 wafers price ~45–50% above N3 (~$28–30k each). Customers pay because there is no alternative. *(TechRepublic/Dataquest 2026 — **VERIFIED**.)*

**Thesis:** own the indispensable, wide-moat monopoly-adjacent factory of the AI/compute era at a
**reasonable** (not cheap, not bubble) forward multiple, funded by a fortress net-cash balance
sheet and enormous FCF — accepting a real, un-hedgeable Taiwan tail in exchange.

---

## 2. Valuation — reasonable for the quality+growth, NOT priced-for-perfection

### 2a. Vs. its own history — at the HIGH end of trailing, but forward is not stretched

| Year | Yr-end ADR px | EPS (ADR, USD) | Trailing P/E |
|---|---|---|---|
| 2022 | $70.7 | $6.01 | **11.8** |
| 2023 | $100.7 | $5.16 | 19.5 |
| 2024 | $193.9 | $7.01 | 27.6 |
| 2025 | $302.3 | $10.28 | 29.4 |
| **Now (2026-08-26)** | **$417.65** | **$13.44 TTM** | **~31.1** |

*(Yr-end ADR prices: yfinance monthly history; EPS = TWD NI / 31.851 / 5.186B ADR — **VERIFIED (calc)**.)*

TSM has re-rated from ~12x (2022 downcycle) to **~31x today** — the top of its own 4-year band.
On a **trailing** basis it is NOT cheap; it has tripled off the 2022 low and run ~+37% YTD-2026
(+54% in 2025). **But** the trailing multiple is misleading because earnings are inflecting
violently upward: gross margin jumped from ~60% (FY25 avg) to **67.7% (Q2 2026)** and net income
grew **+77% YoY** in Q2. On **forward** earnings the picture flips:

- Est. FY2026 ADR EPS **~$17–18** (H1 actual $7.80 + strong H2 on $44–46B/qtr guides) → **fwd P/E ~24x**.
- FY2027 EPS **~$21** (yfinance forwardEps $21.78) → **fwd P/E ~19x**.

A ~19–24x forward multiple on a business growing **revenue +40% and EPS +50–77%** in 2026 is a
**PEG well under 1.0** (yfinance trailingPeg ~1.0 on trailing; forward PEG ~0.5). That is not
priced-for-perfection — it is arguably still discounting the AI cycle as unsustainable.

### 2b. Vs. Mag-7 / semi peers — cheaper than most, on far higher quality

| Company | Trailing P/E | Fwd P/E | P/B (clean) | ROE | Gross margin |
|---|---|---|---|---|---|
| **TSM** | **~31** | **~19–24** | **~12.9** | **~40%** | **60–68%** |
| NVDA | 32 | 16 | 26.0 | 114% | 74% |
| AVGO | 59 | 18 | 19.3 | 37% | 76% |
| ASML | 59 | 29 | — | 54% | 53% |
| AMD | 122 | 31 | 11.7 | 10% | 56% |
| QCOM | 19 | 16 | 6.3 | 34% | 54% |
| Intel | n/m (loss) | 43 | 5.1 | −11% | 39% |

*(All peers: yfinance live 2026-08-26 — **VERIFIED**. NVDA ROE inflated by low equity base.)*

TSM trades at a **lower trailing P/E than NVDA/AVGO/ASML/AMD** and a **lower forward P/E than
ASML/AMD/Intel** — while being the most entrenched, widest-moat, and most-diversified-by-customer
name in the group (it sells to all of them). The only genuinely cheaper names (QCOM, Intel) are
either slow-growth or structurally broken. **TSM is the quality-at-a-reasonable-price anchor of
the AI-hardware complex** — exactly why the 2026-08-26 screen flagged it as the cleanest AI-infra
quality name at a fair price.

### 2c. Rough fair value (ASSUMED — illustrative, not precise)

- **Earnings-multiple approach:** FY2026 EPS ~$17.5 × a defensible 26–28x (justified by 40% growth + widest-moat + net cash) → **~$455–490**. FY2027 EPS ~$21 × 22–25x → **~$460–525**.
- **Analyst consensus:** avg 12-mo target **~$545–555** (StockAnalysis $554/19 analysts; range $440–650), **Strong Buy** — implies ~30–35% upside. *(**VERIFIED via subagent**.)*
- **My ASSUMED fair value: ~$470–540, midpoint ~$500** → **~15–20% upside** to a fairly-valued zone. Not a deep-value bargain; a quality compounder at a fair-to-slightly-cheap forward price.

**The valuation catch:** all of this rests on the +40% growth being **durable**, not a
one-time AI capex spike. If 2026 is the peak of an AI-capex bubble (see §4b), the "cheap forward
multiple" is a mirage — forward EPS estimates collapse and the trailing 31x re-rates toward the
mid-teens on a shrinking E. The forward cheapness is entirely a bet on AI-demand durability.

---

## 3. Quality — elite on every axis except capital intensity

| Metric | Value | Source / confidence |
|---|---|---|
| Gross margin | **59.9% (FY25) → 67.7% (Q2 2026)** | TWD statements / Q2 release — **VERIFIED** (well above the ~55% floor) |
| Operating margin | **50.8% (FY25) → 60.3% (Q2 2026)** | — **VERIFIED** |
| Net margin | **44.6% (FY25) → 55.6% (Q2 2026)** | — **VERIFIED** |
| ROE | **~32% (FY25) → ~40% (TTM)** | NI/equity — **VERIFIED (calc)** |
| ROA | ~19% | yfinance — **VERIFIED** |
| Balance sheet | **~$65B NET CASH** (cash+ST $98.2B vs debt $33.4B) | FY25, TWD→USD — **VERIFIED** — fortress |
| Debt/equity | ~16% (gross) | yfinance — **VERIFIED** — trivially levered |
| FCF (FY25) | **~$31.2B** (OCF $71.4B − capex $40.3B) | — **VERIFIED (calc)** |
| Capex intensity | **~34% of revenue** ($40B on $120B) | — **VERIFIED** — the one non-elite metric |
| Piotroski-style | very high (growing margins, rising ROA, net cash, positive FCF) | — **ASSUMED (calc-consistent)** |

**Elite quality with one honest caveat.** Margins (60–68% gross, 50–60% operating), ROE (~40%),
and the **$65B net-cash fortress** are best-in-class — this is a far stronger balance sheet than
most Mag-7 names. The one place TSM is NOT elite is **capital intensity**: capex runs **~34% of
revenue** ($60–64B in 2026), so it is the opposite of asset-light INTU (capex <1%). This
suppresses near-term FCF yield (~1.4% on FY25) — TSM is plowing cash into fabs. That capex is
**demand-driven, high-return** (it's building sold-out N2 capacity), but it does mean FCF is
cyclically depressed at the top of a buildout, and a demand air-pocket would leave TSM with
expensive, under-utilized fabs (operating leverage cuts both ways).

**The AI runway (the quality driver):** management **raised full-year 2026 USD revenue guidance
twice** — from mid-20s% → "above 30%" (April) → **"slightly above 40%"** (July), explicitly citing
AI / "emerging agentic AI" demand. 3nm and 2nm capacity is **sold out**; N2 fully booked; Nvidia
holds ~60% of CoWoS through 2026. Monthly revenue July 2026 was **+44.7% YoY** (record). *(TSMC IR
transcripts + monthly releases 2026 — **VERIFIED**.)* This is the strongest demand signal of any
name in the universe — the entire question is whether it lasts (§4b).

---

## 4. Bear Case / Risks — the crux for TSM

### 4a. TAIWAN GEOPOLITICAL RISK — the dominant, un-hedgeable tail (SEVERITY: EXISTENTIAL)

This is the reason TSM will never trade at a US-quality multiple, and the risk that dwarfs all
others. TSMC's crown-jewel leading-edge fabs and its irreplaceable engineer/supplier cluster are
concentrated on an island **~130km from China**, which claims it and has not renounced force.

- **Escalation is real and rising.** 2025 saw **Strait Thunder-2025A** (Apr, ~76 aircraft) and
  **Justice Mission 2025** (Dec 29–30, up to ~130 aircraft + **27 rockets fired into nearby waters
  — first live-fire since the 2022 Pelosi drills**). Record single-day incursion 153 aircraft
  (Oct 2024). 2026 has shifted to persistent gray-zone pressure (coast-guard patrols, undersea
  cables) rather than a big named exercise; a Xi–Trump meeting was reportedly being planned late
  Aug 2026. *(**VERIFIED via subagent** — CSIS/wire compilations.)*
- **What an invasion/blockade would do:** a Taiwan contingency is plausibly a **near-total
  permanent loss** for the ADR (fabs seized/destroyed/idled, ADR frozen or delisted, global
  chip supply shattered). This is a **fat-tailed, un-hedgeable** risk — you cannot diversify it
  away inside the position, and it has no clean insurance.
- **"Silicon shield"** (the world's dependence on TSMC deters invasion) is **eroding** as TSMC
  builds overseas (Arizona/Japan/Germany), but the leading edge and the human cluster stay in
  Taiwan, so the shield **largely still holds** for now — a mitigant, not an all-clear.
- **Probability is unknowable but non-trivial.** Consensus among most analysts is that a
  near-term full invasion is a low-annual-probability but catastrophic-if-it-happens event. For a
  buy-and-hold over 3–5 years the cumulative tail is meaningful. **This alone caps position size.**

**Canadian angle (relevant for Hooman):** unlike the CNOOC/China-SOE names in this project, there
is **no OFAC/sanctions issue** — Taiwan is not sanctioned, and Hooman being Canadian is irrelevant
here. **HFCAA/delisting is a non-risk**: TSMC is Taiwan-domiciled, was never in the PCAOB
China/HK non-inspection net. *(SEC/PCAOB primary — **VERIFIED via subagent**.)* The ADR itself is
clean; the risk is purely the physical/geopolitical tail on the island.

### 4b. AI-CAPEX BUBBLE — Hooman's own worry, and TSM is a levered play on it (SEVERITY: HIGH)

TSM's +40% 2026 growth is **overwhelmingly an AI-datacenter capex story** (HPC = 66% of revenue).
If hyperscaler AI capex is a bubble that digests or pops, TSM de-rates hard:

- **The mechanism:** TSM is the toll-road, but the toll-road's traffic is set by hyperscaler
  capex (MSFT/GOOG/AMZN/META) and Nvidia's order book. If those cut — even *digest* — TSM's growth
  swings from +40% to flat/negative, its expensive new N2 fabs run under-utilized, margins
  compress on operating deleverage, and the "cheap forward P/E" evaporates (E collapses).
- **Warning signs (mid-2026):** a late-August-2026 sentiment wobble — *"TSMC Slides 2.3% as
  AI-Chip Confidence Suddenly Cracks"* (Aug 24) — and the market fixated on **Nvidia's Aug 26,
  2026 earnings as the key AI-demand test**. *(Finviz feed — **HEADLINE-ONLY**, cause unread.)*
- **Bull rebuttal:** no verified hyperscaler or Nvidia/AMD capex **cut** was found for 2025–26;
  capacity is sold out through 2026, N2 fully booked, capex being *raised*, backlog robust.
  (Caveat: "no cut found" partly reflects blocked sources, not proof of absence.)
- **Why TSM is LESS bubble-fragile than app-layer:** even in a de-rate, TSM still makes the chips
  for whoever wins, keeps its monopoly, and has $65B net cash — it survives a downturn and
  consolidates. It is the **least-bad way to own the AI theme** if you must. But make no mistake:
  **a 40%-grower priced on 40% growth will correct sharply if that growth proves cyclical.**
  This is precisely the bubble Hooman fears, in picks-and-shovels form.

### 4c. Semiconductor cyclicality (SEVERITY: MEDIUM-HIGH)

Foundry is historically cyclical (2022→2023 revenue fell, EPS P/E swung 12x→19x). The current AI
supercycle has masked cyclicality, but chips remain boom-bust. A general semi downturn (inventory
correction, macro recession) hits TSM's non-AI 34% (smartphone/IoT/auto) even if AI holds.

### 4d. Customer concentration (SEVERITY: MEDIUM)

**Top-10 customers ≈ 85% of revenue; Nvidia >20% (now #1), Apple historically ~25%.** *(24/7 Wall
St 2026-07-16; Taiwan Economic Daily 2026-08-25 — **VERIFIED/HEADLINE**.)* The rally is
increasingly **tethered to Nvidia's single order book** — a concentrated, correlated dependency
(and it correlates with the AI-bubble risk in 4b). Apple's exact 2026 share unconfirmed.

### 4e. Overseas-fab / margin-dilution + tariff costs (SEVERITY: LOW-MEDIUM)

- **Arizona commitment raised to $265B** (~10 fabs, up from $165B; +$100B announced Jul 2026).
  US fabs run at **structurally higher cost** than Taiwan and dilute gross margin (management has
  guided to a multi-point margin drag from overseas ramp over coming years). *(TSMC PR / TechRepublic Jul 2026 — **VERIFIED**.)*
- **Tariffs:** the threatened 100%/300% semi tariffs were **never enacted**; what *was* enacted is
  a narrow **25% tariff on a specific set of advanced AI chips** (Jan 2026) and a **15%-capped
  Taiwan reciprocal tariff** (Feb 2026 ART, with a ~$500B Taiwan investment pledge and duty-free
  quotas for firms building US fabs). Net: a manageable cost/margin headwind, not an existential
  one, and TSMC's US buildout earns tariff relief. *(Federal Register / Focus Taiwan — **VERIFIED via subagent**.)*

---

## 5. Catalysts & Timing

### Bull catalysts
- **N2 (2nm) ramp** — HVM began Q4-2025; scaling ~20k→100k wpm by end-2026; N2 revenue 3%→>10% by
  year-end at +45–50% pricing = a **margin and revenue tailwind** through 2027.
- **Continued guidance raises** — mgmt already raised FY26 to "slightly above 40%"; any further raise or a strong FY27 capex/guide (rumored ~$85B 2027 capex) re-rates the stock.
- **Nvidia Aug-26-2026 earnings + hyperscaler capex prints** — near-term proof-of-demand catalyst (also the key bear risk if it disappoints).
- **Sold-out capacity through 2026–27** underwrites revenue visibility rare for a cyclical.

### Bear catalysts
- Any hyperscaler/Nvidia **capex-cut or AI-digestion signal** → immediate de-rate (the Aug-24 wobble is a preview).
- **Taiwan escalation** (drill → blockade → worse) → step-function repricing of the tail.
- A general **semi inventory correction** in the non-AI 34%.

---

## 6. Fit for Hooman — BUY-grade asset, WATCH-grade fit

**Hooman's context:** ~$556k liquid portfolio (50% cash), **+$732k Adobe RSUs** (US-tech/SaaS) +
AMZN/GOOGL — i.e. already **heavy US-tech/AI concentration**; a **3–5yr house goal** ($250k reserve
separate); explicit **low-volatility need** and an explicit **AI-bubble worry**.

**Does TSM add useful diversification, or pile on?** Both — and the balance is delicate:

- **The good (why it's arguably additive):** TSM is **picks-and-shovels AI-infra**, structurally
  **less bubble-prone than the app/model layer**. Where his Adobe (app-layer SaaS, "AI kills SaaS"
  narrative) and AMZN/GOOGL are exposed to *who wins the AI application war*, TSM wins as long as
  *someone* builds AI compute — a different, more defensive slice of the theme. It's also
  **non-US-domiciled** (Taiwan/EM), adding geographic diversification he says he wants. Fortress
  net cash and 60%+ margins are genuinely quality.
- **The bad (why it piles on):** it is still **the same macro bet** — AI-datacenter capex — as his
  existing tech book. If the AI bubble he fears deflates, TSM falls *with* Adobe/AMZN/GOOGL, not
  against them (correlation is high in an AI-capex unwind). It has **beta ~1.26** (higher-vol, not
  lower) and it's run ~+37% YTD/+75% trailing-year — he'd be buying after a huge run, not into
  weakness.
- **The Taiwan tail vs. a 3–5yr house horizon:** this is the disqualifier for *house money*. An
  un-hedgeable, fat-tailed geopolitical event that can permanently impair the position is
  **exactly wrong** for capital he may need for a house in 3–5 years and for his stated low-vol
  need. TSM belongs to **long-horizon, risk-tolerant** capital only.

**Sleeve:** by character TSM is a **Quality** name (widest moat, fortress balance sheet); by *risk*
it carries **EM-grade geopolitical tail**. Treat it as an **EM-tail-sleeve** position: small, hard-
capped, sized as you'd size any single-country-tail EM bet (not a core Quality anchor). It should
NOT come out of house-reserve or Bucket-A (vol-reducer) money — it is Bucket-C opportunistic
growth, and Bucket C is already ~7.7pts over his 15% target.

**Recommendation for Hooman:** the *business* is a clear BUY-grade compounder; the *fit* argues for
patience and small size. **Add only as a small (≤2–4% of liquid) EM-sleeve position, ideally on a
pullback** (e.g. toward the low-$300s / a re-test after an AI-sentiment scare or a Taiwan-drill
dip), explicitly as long-horizon money he can hold through a Taiwan tail-scare — never house money.

---

## 7. Scorecard & Verdict

### Scorecard (CLAUDE.md §3 weights: Cheapness 30 / Quality 30 / Trap 20 / Moat 15 / Catalyst 5)

| Factor | Weight | Score (0–10) | Weighted | Rationale |
|---|---|---|---|---|
| **Cheapness** | 30% | **6** | 1.80 | Not cheap on trailing (~31x, top of own band, +37% YTD run), but **fwd P/E ~19–24x on +40% growth = PEG <1**, cheaper than most semi/AI peers on higher quality. Reasonable-to-slightly-cheap, not a deep-value bargain — and forward cheapness is contingent on AI-demand durability. |
| **Quality** | 30% | **9** | 2.70 | Elite: 60–68% gross, 50–60% operating, ~40% ROE, **$65B net cash**, huge (if capex-suppressed) FCF, twice-raised guidance. Docked only for ~34% capex intensity (not asset-light) and cyclicality. Best-quality business in the universe. |
| **Trap-risk (inverse)** | 20% | **4** | 0.80 | **Two heavy trap flags: (1) un-hedgeable Taiwan-invasion tail = potential near-total loss; (2) it's a levered bet on the AI-capex cycle Hooman fears, priced for 40% growth that could prove cyclical.** Plus semi-cyclicality + Nvidia-concentration. Genuinely tail-risky — the low score is deliberate and Taiwan-driven. |
| **Moat & leadership** | 15% | **10** | 1.50 | **The widest moat in tech**: >70% foundry / ~90% leading-edge, multi-year process lead, ruinous capital moat, customer co-design lock-in, 4 rounds of price hikes. Best-in-class management/capital allocation. |
| **Catalyst** | 5% | **8** | 0.40 | Strong near-term: N2 ramp + margin lift, sold-out capacity, twice-raised guidance, Nvidia/hyperscaler capex prints. (Same catalysts are symmetric bear risks.) |
| **TOTAL** | 100% | | **7.20 / 10** | |

### VERDICT: **WATCH → small-BUY on weakness** (BUY-grade business, WATCH-grade fit for Hooman)

TSM scores **7.20/10** — held back almost entirely by the Trap-risk axis (Taiwan tail + AI-cycle
leverage), *not* by any business flaw. As a **standalone asset it is a BUY**: the widest moat in
tech, elite margins, a $65B net-cash fortress, and — uniquely among AI-hardware names — a
**reasonable forward multiple (PEG <1)** rather than a bubble price. The screen was right: it is
the cleanest AI-infrastructure quality name at a fair price.

**But for Hooman specifically the verdict is WATCH, size-constrained.** The two dominant risks are
the two things he most needs to avoid: (a) an **un-hedgeable Taiwan tail** that's wrong for 3–5yr
house-horizon, low-vol capital; and (b) a **levered bet on the AI-capex bubble he already worries
about**, layered onto his large US-tech concentration (Adobe + AMZN/GOOGL), with which it is
highly correlated in a downturn. It is picks-and-shovels (less fragile than app-layer) and it does
add geographic diversification — real positives — but it does not *reduce* his AI/tech risk, it
concentrates it in a different, tail-heavy wrapper.

**Actionable:** eligible for a **small (≤2–4% of liquid), hard-capped EM-tail-sleeve position,
entered on a pullback** (AI-sentiment scare or Taiwan-drill dip toward the low-$300s), as
long-horizon money only — never from the house reserve or Bucket A. **Rough fair value ~$470–540
(ASSUMED), midpoint ~$500** vs $417.65 now → ~15–20% upside to fair, but the entry after a +75%
year argues for patience over chasing. If Hooman wants AI-infra exposure, TSM is the highest-
quality vehicle to get it — just at the right size and the right price.

---

## Appendix — source ledger & verification log (timestamps in EDT, 2026-08-26)

**Live yfinance pulls (`/opt/venv/bin/python3`, 2026-08-26):**
- Snapshot: price $417.65, prev close $417.41, mkt cap $2.166T, ADR shares 5.186B, 52wk $225.63–$479.00, beta 1.258, div yield ~0.8–1.0%, payout 25.7%, forwardEps $21.78, forwardPE 19.17, trailingEps $13.44, trailingPE 31.08. **financialCurrency=TWD, currency=USD** (the corruption source).
- **CORRUPTED yfinance fields (NOT used):** priceToBook 87.1, enterpriseToEbitda 4.708, enterpriseValue $14.9T. **Recomputed clean:** P/B 12.9, EV/EBITDA(TTM) 21.8, EV $2.10T.
- FX: **USDTWD 31.851** (yfinance TWD=X, 2026-08-26).
- Raw FY2025 statements (TWD): Rev 3,809.05B, Gross 2,281.29B, Oper 1,936.10B, NI 1,697.60B, EBITDA 2,742.12B; Equity 5,355.04B, Debt 1,064.58B, Cash+ST 3,128.07B; OCF 2,274.98B, capex 1,282.60B. → USD (÷31.851): Rev $119.6B, NI $53.3B, EBITDA $86.1B, Equity $168.1B, Net cash $64.8B, FCF $31.2B.
- Quarterly NI (TWD): Q2'26 706.56B, Q1'26 572.48B, Q4'25 485.47B, Q3'25 452.30B → **TTM NI $69.6B, TTM Rev $139.4B, TTM EBITDA $96.4B** → TTM P/E 31.1, EV/EBITDA 21.8.
- Historical P/E (yr-end ADR px ÷ EPS): 2022 11.8x, 2023 19.5x, 2024 27.6x, 2025 29.4x.
- Peers (2026-08-26): NVDA PE 32/fwd 16; AVGO 59/18; ASML 59/29; AMD 122/31; QCOM 19/16; INTC loss/43.

**Web research (subagent, 2026-08-26):** TSMC IR primary — Q2-2026 release (pr.tsmc.com/english/news/3326, 2026-07-16): rev NT$1,270.38B/US$40.20B +33.7% USD YoY, EPS NT$27.25/US$4.31-ADR, GM 67.7%, HPC 66%; Q1-2026 (news/3297): rev US$35.90B, GM 66.2%; FY26 guidance raised twice to "slightly above 40%" USD growth; 2026 capex $60–64B; July-2026 monthly rev +44.7% YoY. Foundry >70% share (Counterpoint/Morningstar); N2 sold out, 4x N3 tape-outs; Nvidia ~60% CoWoS + likely #1 customer >20%; top-10 ~85%. Taiwan: Justice Mission 2025 live-fire (Dec 2025); Arizona $265B (Jul 2026); Taiwan tariff 15%-capped (Feb 2026 ART); HFCAA does NOT apply (Taiwan not in PCAOB China/HK net). Dividend NT$7.0/qtr, +~33% YoY. Consensus Strong Buy, avg target ~$545–555 (range $440–650).

**Confidence key:** VERIFIED = primary source (TSMC IR / statements) or ≥2 agreeing feeds / my calc from primary data. ASSUMED = single-source, my derivation, or forward estimate. UNVERIFIED/HEADLINE-ONLY = flagged, not relied on for the verdict.
