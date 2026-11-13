# Per-Name Target Weights — Real-Asset Sleeves (Gold / Silver-Plat / Copper / Ag)

**Run:** 2026-07 by Claude (Opus 4.8). Owner: Hooman Shariati (Canadian, quality-first). **RESEARCH — not financial advice.**
Splits each sleeve's TARGET % (from `ideal_allocation.md`) across its names by quality / role / overlap.
Reuses `research/macro_metals_uranium.md` + `research/macro_supercycle_metals.md` + `PHASE1_AUDIT.md`.

> **Confidence:** live prices/multiples **VERIFIED** (yfinance, 2026-07, via `/opt/venv/bin/python3`).
> Per-name **target weights ASSUMED** (my synthesis from prior research + role/overlap logic). Sleeve totals fixed.

Live reads (yfinance, 2026-07): AEM $145.13 **fwd P/E 11.4** (trail 13.7) · WPM $111.48 **fwd P/E 20.9** (trail 28.2) ·
EMPYF $0.59 mcap $75M (trail P/E 7.3, micro) · MNT.TO $58.86 (physical-backed, no P/E) · COPX $77.72 (trail P/E 17.4) ·
BHP $83.72 **fwd P/E 16.8** · COP-U.TO $10.70 (physical trust) · NTCPF $2.19 mcap $727M (junior) ·
CF $125.07 **fwd P/E 11.1** · PDBA $37.71 (commodity ETF) · KHC $25.67 **fwd P/E 12.2**. All **VERIFIED**.

---

## 1. GOLD CORE — target 9%

Principle (from metals research §6-7): **gold = the TRUE monetary/USD-debasement hedge; favor physical + near-physical.**
The miner (AEM) is quality but higher-beta; the micro-royalty (EMPYF) is a speculative satellite. So weight
~two-thirds into the monetary core, a meaningful slug to the one quality miner, a token to the royalty.

| Name | Target % of total | Rationale |
|---|--:|---|
| **Physical gold** (bullion) | **3.5%** | The real monetary hedge — no counterparty/equity/operating risk; the sleeve's anchor. |
| **MNT** (RCM Cdn Gold Reserves ETR) | **2.5%** | Physical-backed, near-monetary; CAD-listed convenience layer on the same bullion role. Core with physical. |
| **AEM** (Agnico Eagle) | **2.5%** | Best-in-class miner (fwd P/E 11.4, Tier-1 Canada/Australia, lowest AISC) — the one gold *miner* worth owning; adds torque, not hedge quality. |
| **EMPYF** (Empress Royalty) | **0.5%** | Micro royalty ($75M mcap, $0.59); speculative satellite — keep token or consolidate into MNT/AEM. |

**Monetary core (physical+MNT) = 6.0% (67%)** · miner 2.5% (28%) · royalty 0.5% (5%). Sum = **9.0%**.

## 2. SILVER / PLATINUM — target 1%

WPM is the only name and is being trimmed *into* the 1% target. **WPM takes the whole 1%.**

| Name | Target % of total | Rationale |
|---|--:|---|
| **WPM** (Wheaton streamer) | **1.0%** | High-quality streaming model (85%+ margins) but fully valued (fwd P/E ~21) and ~**half gold** — kept small as a cyclical satellite, not core insurance. |

⚠️ **Overlap:** WPM's revenue is **~51% gold / 47% silver** — roughly **0.5% of this "silver" sleeve is really gold exposure**,
so true silver/platinum ≈ 0.5% and true gold core is effectively ~6.5%. Do not count WPM as a pure silver bet.

## 3. COPPER — target 3%

Principle (supercycle research §copper): thesis is the most defensible in the book but a **2030s** story, spot at
record highs, refined market in surplus through 2027 → size small, **favor the clean/liquid vehicles**, minimize the
diluted and the speculative.

| Name | Target % of total | Rationale |
|---|--:|---|
| **COPX** (Global X Copper Miners) | **1.75%** | The clean, liquid, diversified pure-copper vehicle ($7B AUM); the sleeve core. |
| **COP-U** (Sprott Physical Copper) | **0.5%** | Pure physical copper, trades at NAV discount — but 1.3% MER + no yield + storage drag → small. |
| **BHP** | **0.5%** | Quality diversified major but **~half iron-ore on earnings** (55% EBITDA) → not a copper proxy; small, diluted. |
| **NTCPF** (NorthIsle) | **0.25%** | Speculative pre-production junior — lottery-ticket sizing only. |

Clean/liquid copper (COPX+COP.U) = 2.25% (75%). Sum = **3.0%**.

⚠️ **Overlap:** BHP's 0.5% is ~half iron-ore/China-steel — real copper here is ~0.25%; **NTCPF minimize** (spec).

## 4. AG — target 3%

Principle: **CF is the quality anchor** (best commodity-quality name per `PHASE1_AUDIT.md`: 33% op margin, 27% ROE,
fwd P/E ~11); PDBA is broad-ag ballast that de-risks CF's single-name/nitrogen concentration; KHC is the one food
name held for a breakup catalyst but a declining packaged-food business → smallest.

| Name | Target % of total | Rationale |
|---|--:|---|
| **CF** (CF Industries) | **1.5%** | Best commodity-quality in the book — 33% op margin, 27% ROE, fwd P/E 11.1; the sleeve anchor. |
| **PDBA** (Invesco Ag Commodity) | **1.0%** | Broad-ag ETF ballast — diversifies CF's single-name nitrogen bet; the "own the crop" leg. |
| **KHC** (Kraft Heinz) | **0.5%** | The one food name; fwd P/E 12 + breakup catalyst, but structurally declining packaged food → minimal. |

Sum = **3.0%**.

---

## Combined table (all four sleeves)

| Sleeve | Name | Target % of total | Role |
|---|---|--:|---|
| Gold (9%) | Physical gold | 3.5% | monetary core |
| | MNT | 2.5% | monetary core (physical-backed) |
| | AEM | 2.5% | quality miner (torque) |
| | EMPYF | 0.5% | micro royalty (satellite) |
| Silver/Plat (1%) | WPM | 1.0% | streamer (½ gold, satellite) |
| Copper (3%) | COPX | 1.75% | clean/liquid core |
| | COP-U | 0.5% | physical (high-fee) |
| | BHP | 0.5% | diversified major (½ iron-ore) |
| | NTCPF | 0.25% | spec junior (minimize) |
| Ag (3%) | CF | 1.5% | quality anchor |
| | PDBA | 1.0% | broad-ag ballast |
| | KHC | 0.5% | one food name (catalyst) |
| **TOTAL** | | **16.0%** | |

## Overlap & minimize flags

- **WPM is ~½ gold** (51% gold / 47% silver by revenue): ~0.5% of the "silver/plat" 1% is really gold, pushing
  the effective gold core to ~6.5% and effective silver/plat to ~0.5%. Don't double-count as a pure silver bet.
- **BHP is ~½ iron-ore** (55% of EBITDA): its 0.5% is only ~0.25% true copper; it's a China-steel bet too, not a copper proxy.
- **Names to minimize / candidates to consolidate:** **EMPYF** (0.5%, micro — fold into MNT/AEM if trimming count),
  **NTCPF** (0.25%, speculative junior), **COP-U** (0.5% — high 1.3% MER; prefer COPX), **KHC** (0.5% — declining biz, catalyst-only).
- **Quality-first tilt confirmed:** the largest single weights are the highest-quality expressions — physical gold (3.5%),
  MNT (2.5%), AEM (2.5% at fwd P/E 11), COPX (1.75%), CF (1.5%) — while cyclical/diluted/speculative names get the smallest slugs.

**NOT financial advice.** Research to inform Hooman's own decisions.
