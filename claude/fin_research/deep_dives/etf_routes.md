# "Can't I Just Buy These via an ETF?" — CPIC & Buzzi via ETFs

**For:** Hooman Shariati — **CANADIAN citizen**; brokers = **Charles Schwab (US)** and **Questrade
(Canada)**; wants things buyable **without** opening Interactive Brokers.
**Author:** Claude (Opus 4.8) · **Date:** 2026-07-05 · **RESEARCH, NOT financial/tax/legal advice.**

> **What this file answers.** Two of Hooman's target names are hard to buy directly on his brokers:
> **CPIC (China Pacific Insurance, 2601.HK)** and **Buzzi (BZU.MI, Milan)**. His question was: *"Can't I
> buy these via an ETF or something?"* — meaning either (a) an ETF that holds the **specific name**, or
> (b) an ETF that gives him the **theme** (EM/Asian life-insurance + aging; global/European building
> materials + reshoring/infrastructure).
>
> **Read alongside:** `deep_dives/2601_HK/investability_and_alternatives.md` (CPIC un-buyable on
> Schwab/Questrade; **PUK** is the direct-stock alternative) and `deep_dives/BZU_MI/buy_diligence.md`
> (Buzzi needs IBKR; the CRH/Eagle comparison). This file does NOT re-run the valuation work — it only
> answers the ETF-route question. **Anti-hallucination:** every ETF ticker, expense ratio and holding
> weight below carries a source + as-of date + a VERIFIED / ASSUMED / UNVERIFIED mark. No invented
> tickers or weights.

---

## Jargon, in one place (for a newcomer)

- **ETF (exchange-traded fund):** a basket of many stocks that trades on an exchange like a single share.
  Buying one share of the ETF buys you a slice of *everything* it holds, in the fund's weights.
- **Expense ratio (ER):** the fund's annual fee, quoted as a % of your money, skimmed daily out of the
  price (you never see a bill). E.g. **0.50% ER** on a $10,000 holding ≈ **$50/year**. Lower is better;
  a broad index ETF can be **0.03–0.10%**, a niche "thematic" one **0.40–0.75%**.
- **Sector ETF vs thematic ETF:** a **sector** ETF holds a standard industry slice (e.g. "materials",
  "insurance"). A **thematic** ETF is built around an *idea* (e.g. "aging population", "US infrastructure
  development") and can hold companies across several sectors. Thematic ETFs are usually pricier (higher
  ER) and can drift from the pure theme.
- **Holding / weight:** a stock inside the ETF, and what % of the fund it is. A "**meaningful weight**"
  means it actually moves the fund; a **tail** holding at 0.1–1% barely matters to your return.
- **Cap-weighted vs equal-weighted:** cap-weighted funds hold more of the biggest companies (so a few
  giants dominate); equal-weighted funds hold ~the same $ of each name.
- **US-listed vs Canadian-listed ETF — this matters for a Canadian:** a Canadian at Questrade can hold a
  **US-listed** ETF (e.g. FXI, PAVE) *and* a **Canadian/TSX-listed** ETF. But there are two wrinkles:
  - **Registered-account (RRSP/TFSA) US-dividend withholding.** The US levies a **15% withholding tax on
    US-source dividends**. In an **RRSP**, a US-Canada treaty exemption means a **US-listed** ETF paying
    US dividends is generally **not** withheld (best home for US-dividend payers). In a **TFSA**, that
    exemption does **not** apply — the **15% is withheld and cannot be recovered**. (This bites on
    US-*equity* dividends; a China or Europe ETF pays little US-source dividend, so the effect is small
    for FXI/EWI/etc. — but it's the general rule to know.) **[general tax rule — confirm with a tax
    advisor; not advice]**
  - **PRIIPs / KID access block.** EU rules require a "Key Information Document" (KID) to sell a fund to
    EU/EEA/UK residents; conversely some **US-listed** ETFs are not registered for sale to residents of
    certain countries. For a **Canadian resident**, the practical version is: **UCITS (Europe-listed)
    ETFs are generally NOT buyable** at Questrade/Schwab (this is why the London-listed aging-population
    ETF **AGES** is off the table below), while **US-listed** ETFs generally **are**. Confirm per-ticker
    at the broker. **[VERIFIED as a general access rule; per-ticker UNVERIFIED]**

**The one big idea to hold onto:** an ETF gives you **easy access + instant diversification**, but it
**averages away the single-name value thesis.** CPIC's whole appeal is **0.7× book / ~0.5× embedded
value**; Buzzi's is **~9× P/E + net cash**. An ETF holds those names (if at all) at a tiny weight
*alongside dozens of expensive ones*, so you end up **owning the theme at roughly market multiples, not
the bargain.** Keep this in mind through both sections.

---

# THEME 1 — EM / Asian life insurance + aging (the CPIC theme)

## 1.1 Can he get CPIC *specifically* via an ETF? — **Essentially NO.**

CPIC does **not** appear as a meaningful, visible holding in any accessible US-listed ETF checked. The
detail:

| ETF (ticker) | Issuer | Expense ratio | CPIC in it? | What insurers it DOES hold | Mark |
|---|---|--:|---|---|:--:|
| **FXI** — iShares China Large-Cap | BlackRock | **0.73%** | **No** — tracks the **FTSE China 50** (50 largest only); CPIC is below the cutoff and not in the top 25 of 61 names | Ping An 3.92%, China Life 2.43%, PICC P&C 1.13% | VERIFIED |
| **MCHI** — iShares MSCI China | BlackRock | **0.59%** | **Not visible** — likely buried in the ~586-name tail at a trivial weight; could not confirm on free full-holdings sources | Ping An 1.83%, China Life 1.13% | VERIFIED (CPIC presence **UNVERIFIED**) |
| **EWH** — iShares MSCI Hong Kong | BlackRock | **0.50%** | **No** — CPIC is *China*-domiciled (excluded from a Hong-Kong index) even though its H-share lists in HK | **AIA Group 21.34%** (the fund's #1 holding) | VERIFIED |
| **KWEB** — KraneShares CSI China Internet | KraneShares | **0.70%** | **No** — internet only (Tencent 10.2%, PDD 8.4%, Alibaba 7.7%, Meituan, NetEase). *Not an insurance ETF — noted so it's ruled out.* | none | VERIFIED |
| **CHIX** — Global X MSCI China Financials | Global X | (was 0.66%) | **N/A** | **LIQUIDATED/DELISTED** — last trade 2024-02-20; the obvious "China-financials proxy" no longer exists | VERIFIED |

Sources: iShares product pages (FXI 239536, MCHI 239619, EWH 239657) + stockanalysis.com holdings, all
as-of ~2026-07-02; Global X CHIX liquidation notice (Jan 2024). **All VERIFIED except CPIC-in-MCHI.**

**Honest answer:** there is **no clean pure-play ETF for CPIC**, and even broad China ETFs mostly **skip
CPIC** (FXI/MCHI hold **Ping An and China Life** — *other* Chinese insurers — not CPIC). If Hooman's goal
is "CPIC specifically," an ETF does **not** deliver it. If his goal is "a big Asian life insurer at a
real weight via an ETF," the closest is **EWH → AIA at ~21%** — but that's **AIA, not CPIC**, wrapped in
a Hong-Kong-property/bank fund.

**To fully close the one gap:** whether CPIC's H-share sits in MCHI's long tail — pull MCHI's full
holdings CSV from iShares (JS-rendered; use its SEC **N-PORT** filing) if it ever matters. Even if it's
there, it would be a **fraction of a percent** — economically irrelevant to a CPIC thesis.

## 1.2 Best THEME-proxy ETFs (aging / Asian-life) buyable on Schwab & Questrade

| ETF (ticker) | Issuer | ER | What it actually is | Theme fit | Buyable Schwab/Questrade? | Mark |
|---|---|--:|---|---|---|:--:|
| **EWH** — iShares MSCI Hong Kong | BlackRock | **0.50%** | Hong-Kong equities; **top holding AIA Group ~21%** (premium pan-Asian life insurer) | **Best single accessible Asian-life-insurer weight**, but diluted by HK banks/property (only ~1 name is the insurer) | ✅ / ✅ (US-listed) | VERIFIED |
| **AGNG** — Global X Aging Population | Global X | **0.50%** | Aging-demographics **thematic** ETF (formerly LNGR); **~91% Health Care, ~8% Real Estate** — Novo Nordisk, Eli Lilly, AbbVie, Edwards Lifesciences, senior-housing REITs Welltower/Ventas | Captures the **aging** tailwind but via **medtech/pharma/senior-housing — essentially ZERO insurance.** Wrong leg of the theme. | ✅ / ✅ (US-listed, Nasdaq) | VERIFIED |
| **FXI / MCHI** — broad China | BlackRock | 0.73% / 0.59% | Broad China equity | Give you **Ping An + China Life** (~4–6% combined in FXI) — Chinese insurers, but NOT CPIC, alongside tech/banks/energy | ✅ / ✅ (US-listed) | VERIFIED |
| ~~AGES — iShares Ageing Population UCITS~~ | BlackRock | — | London-listed aging ETF | **NOT buyable** — UCITS/PRIIPs blocks it for a North-American retail account. AGNG is the US-listed equivalent. | ❌ | VERIFIED |

Sources as §1.1 + globalxetfs.com/funds/agng (AGNG). **No dedicated, currently-listed US "Asia ex-Japan
financials" sector ETF exists** (CHIX, the natural candidate, was liquidated Feb-2024). Broad
Asia-ex-Japan funds (AAXJ) exist but are diversified equity with **small** insurer exposure —
**UNVERIFIED** exact weights; not a clean proxy.

**Read on the proxies:** none is a good CPIC substitute. **EWH** gives real *Asian-life* exposure but via
**AIA** (a premium name at ~2.25× book, the opposite of CPIC's deep-value profile) and drags along Hong
Kong banks/property. **AGNG** nails the *aging demographic* idea but expresses it through healthcare, not
insurance — so it doesn't touch the "cheap insurer" thesis at all. **FXI/MCHI** give Chinese *insurers*
(Ping An, China Life) but not CPIC, buried in a broad China fund.

## 1.3 The trade-off, and the bottom line for Theme 1

**The core trade-off:** CPIC's entire attraction is being **cheap** — 0.72× book, ~0.48–0.51× embedded
value, ~17% ROE (per the deep dive). **No accessible ETF gives you that.** The theme proxies give you
either the *aging demographic* (AGNG, via healthcare) or a *large Asian life insurer* (EWH, via AIA at a
**premium** ~2.25× book) — i.e. you'd own the **theme at market/premium multiples, not CPIC's bargain**,
and mostly not even the same company.

**Bottom line — ETF vs direct stock (Theme 1):** The **ETF route is weak** here. If Hooman wants the
*aging-Asia-life* thesis in something he can buy today on Schwab/Questrade, the far better answer — as
`investability_and_alternatives.md` already concluded — is the **direct stock PUK (Prudential plc, NYSE)**:
a ~100%-Asia+Africa life insurer, ~20% ROE, trivially ownable on both his brokers in any account, no
China/HK access friction. **PUK >> any ETF for this theme.** The only ETF that even adds something is
**EWH** if he specifically wants **AIA** exposure and is comfortable with the HK-bank/property ballast —
but a direct AIA line or PUK is cleaner. **AGNG** is a fine *aging-demographics* satellite but is a
different (healthcare) bet, not an insurance value play.

---

# THEME 2 — Building materials / cement + reshoring & infrastructure (the Buzzi theme)

## 2.1 Can he get Buzzi *specifically* via an ETF? — **Only at a tiny ~1% weight (via an Italy fund).**

Buzzi **does** show up in one accessible US-listed ETF — but as a **small tail holding in a country fund**,
not a materials/infra theme fund:

| ETF (ticker) | Issuer | Expense ratio | Buzzi in it? | Notes | Mark |
|---|---|--:|---|---|:--:|
| **EWI** — iShares MSCI Italy | BlackRock | **0.50%** | **YES — ~1.01%, position #24** (161,988 shares, as-of 2026-07-02) | The **only** accessible US-listed ETF with **confirmed direct Buzzi exposure** — but it's an *Italy country* fund dominated by banks: UniCredit 16.4%, Intesa 12.4%, Enel 11.2%, Ferrari 4.8%, Generali 4.7% | VERIFIED |
| **MXI** — iShares Global Materials | BlackRock | **0.39%** | **Not in top 25 of 114**; tail UNVERIFIED | Tracks S&P Global 1200 Materials (large-cap) → a Buzzi mid-cap slot is *unlikely but not confirmed absent*. Holds Linde 8.1%, BHP 6.9%, CRH 2.3%, Holcim 1.5%, Vulcan 1.3% | PARTIAL (**UNVERIFIED** on Buzzi) |
| **VGK** — Vanguard FTSE Europe | Vanguard | **0.06%** | Not in top 10; **UNVERIFIED** tail | ~1,300 names; a tiny Buzzi slot is plausible but not disclosed in accessible holdings — economically irrelevant regardless | PARTIAL |

Sources: iShares EWI (product 239664) + stockanalysis.com holdings/JSON (exact weight & share count),
as-of 2026-07-02; MXI iShares 239748 + stockanalysis.com top-25, as-of 2026-07-01; VGK
investor.vanguard.com, holdings as-of 2026-05-31. **iShares CSV/N-PORT downloads were bot-blocked this
session**, so MXI/VGK tails rely on aggregator top-holdings, hence the UNVERIFIED tail marks.

**Honest answer:** you *can* get a **sliver** of Buzzi via **EWI at ~1%** — but that means owning a
**bank-heavy Italy fund** where Buzzi is 1 of ~30 names and Italian banks are ~30% of the fund. That is
**not** a way to express the Buzzi thesis; it's an Italy-equity bet that happens to include a little
Buzzi. Whether Buzzi also sits deep in MXI's tail is **UNVERIFIED** (check the iShares holdings download
/ N-PORT if it matters) — but even if so, it would be a fraction of a percent.

## 2.2 Best THEME-proxy ETFs (US reshoring/infra + building materials) buyable on Schwab & Questrade

These give the **reshoring / infrastructure / building-materials TREND** cleanly and cheaply — none holds
Buzzi (they're US-company-heavy):

| ETF (ticker) | Issuer | ER | What it is | Top / relevant holdings | Buzzi? | Buyable | Mark |
|---|---|--:|---|---|---|---|:--:|
| **PAVE** — Global X U.S. Infrastructure Development | Global X | **0.47%** | **Thematic** — US reshoring/infrastructure build-out (industrials + materials); **the obvious US-reshoring/infra proxy** | Quanta (PWR) 3.9%, CSX 3.7%, Howmet 3.4%, Trane 3.3%, Union Pacific 3.3%; **materials: Vulcan (VMC) 2.15%, Martin Marietta (MLM) 1.94%, Eagle (EXP) 0.38%** | **No** (0 of 105 holdings) | ✅ / ✅ | VERIFIED |
| **XLB** — Materials Select Sector SPDR | State Street | **0.08%** | Cheap S&P-500 **materials sector** fund | Linde 14.4%, Newmont 5.8%, Freeport 5.1%, Sherwin-Williams 5.0%; **VMC 4.7%, CRH 4.6%, MLM 4.6%** | **No** (S&P 500 only → Italian Buzzi excluded) | ✅ / ✅ | VERIFIED |
| **VAW** — Vanguard Materials | Vanguard | **0.09%** | Cheap broad **US materials** fund | Linde 14.8%, Newmont 7.6%, Freeport 6.1%, **CRH 4.7%**, Sherwin-Williams 4.6% (US-only, "foreign 0.0%") | **No** | ✅ / ✅ | VERIFIED |
| **IFRA** — iShares U.S. Infrastructure | BlackRock | **0.30%** | US infrastructure (owners + builders), more equal-weighted | Caterpillar 4.2%, Union Pacific 4.1%, NextEra 4.0%, PWR 3.5%, CSX 3.2%; **CRH 2.6% (#9)** | **No** (US-focused index) | ✅ / ✅ | VERIFIED (tail ASSUMED-no) |
| **MXI** — iShares Global Materials | BlackRock | **0.39%** | **Global** materials (includes European cement) | Linde 8.1%, BHP 6.9%, Air Liquide, **CRH 2.3%, Holcim 1.5%, Vulcan 1.3%** | **UNVERIFIED** (not in top 25) | ✅ / ✅ | PARTIAL |
| ~~ITB / XHB~~ — US home construction / homebuilders | BlackRock / State Street | 0.38% / 0.35% | **US housing**, not cement/infra | D.R. Horton, Pulte, Lennar (ITB); Owens Corning, KB Home (XHB) | **No** | ✅ / ✅ | VERIFIED — *excluded: wrong theme (housing, not cement/infra)* |

Sources: Global X PAVE full-holdings CSV (as-of 2026-07-02); SSGA XLB page (holdings 2026-07-01, ER
2026-07-05); Vanguard VAW (ER 2025-12-19, holdings 2026-05-31); iShares IFRA (294315) + stockanalysis;
iShares MXI (239748). **All VERIFIED except MXI's Buzzi-tail (UNVERIFIED) and VGK (PARTIAL).**

**Read on the proxies:** **PAVE** is the best single expression of the **US-reshoring/infrastructure**
idea (it's *built* for it and holds the US aggregates names Vulcan/Martin Marietta/Eagle) — but it's
**US-companies-heavy and holds no Buzzi**. **XLB (0.08%) / VAW (0.09%)** are the cheapest broad-materials
options but are diluted by chemicals (Linde ~14%) and metals/mining (Newmont, Freeport) — less "cement/
infra-pure." **MXI (0.39%)** is the only *global* materials fund (adds European cement — CRH, Holcim) but
still doesn't confirm Buzzi and is large-cap.

**Note:** several of these (PAVE, XLB, VAW, IFRA) are **US-equity** funds paying US-source dividends —
so the **RRSP-vs-TFSA withholding** point in the jargon box applies (hold them in an RRSP rather than a
TFSA if he wants to avoid the unrecoverable 15% US-dividend withholding). Dividend yields on these are
low, so the effect is modest. **[general tax rule — confirm with advisor]**

## 2.3 The trade-off, and the bottom line for Theme 2

**The core trade-off:** Buzzi's thesis is **cheapness + a fortress balance sheet** — ~9× P/E, ~6× EV/
EBITDA, **the only net-cash name** vs CRH ($17B net debt) and Eagle ($1.5B net debt), at ~1.17× book
(per the buy-diligence file). **Every theme-proxy ETF averages that away.** PAVE/XLB/VAW hold the
US materials leaders — **Vulcan, Martin Marietta, CRH, Eagle** — at **market multiples** (CRH ~16× fwd
P/E, Eagle ~15×, ~12× EV/EBITDA), *not* Buzzi's 9× + net cash. You'd own the **reshoring/infra trend at
full price**, and you would specifically **NOT** own the single-name value/net-cash characteristics that
made Buzzi interesting. And the one ETF that *does* hold Buzzi (**EWI at ~1%**) is a bank-dominated Italy
bet, not a materials play — so it doesn't express the thesis either.

**Bottom line — ETF vs direct stock (Theme 2):**
- If Hooman wants **Buzzi specifically** (the cheap, net-cash single-name thesis), **no ETF delivers it**
  — EWI's ~1% weight is immaterial. That thesis requires the **direct BZU.MI Milan line via IBKR** (per
  the buy-diligence file). An ETF cannot substitute for it.
- If Hooman wants the **reshoring/infrastructure/building-materials THEME** without opening IBKR — which
  is exactly what the "can't I just buy an ETF" question is really asking — the honest, buyable answers
  are **PAVE (0.47%, the purpose-built US-infra-development proxy)** or, cheaper, **XLB (0.08%) / VAW
  (0.09%) broad-materials**, all buyable on both Schwab and Questrade. He gets the trend and instant
  diversification, but at **market multiples** and via **US names (Vulcan/MLM/CRH/Eagle), not Buzzi**.
- The clean **direct-stock** alternatives already identified — **CRH** (cleaner US-infra, USD, S&P index,
  dispersed governance) and **Eagle (EXP)** — are ownable on both brokers *as single stocks* and let him
  pick one name at a fair (not bargain) price rather than an averaged basket. **CRH/Eagle direct**, or
  **PAVE** if he wants a basket, both beat "buy Buzzi via an ETF" (which isn't really possible).

---

# One-page answer to Hooman

| | **Theme 1 — CPIC / EM-Asian-life-insurance + aging** | **Theme 2 — Buzzi / building-materials + reshoring** |
|---|---|---|
| **Get the SPECIFIC name via an ETF?** | **NO** — CPIC not visible in any accessible ETF; FXI/MCHI hold *other* Chinese insurers (Ping An, China Life), not CPIC | **Only ~1%** — Buzzi is ~1.01% of **EWI** (iShares MSCI Italy), a bank-heavy country fund; immaterial |
| **Best THEME-proxy ETF(s), buyable Schwab+Questrade (ER)** | **EWH** 0.50% (AIA ~21% — a *premium* Asian lifer, not CPIC); **AGNG** 0.50% (aging theme but *healthcare*, ~zero insurance) | **PAVE** 0.47% (US-infra-development, holds Vulcan/MLM/Eagle); **XLB** 0.08% / **VAW** 0.09% (cheap broad US materials) |
| **Core trade-off** | ETF = easy access + diversification, but you own the **theme at premium/market multiples (AIA ~2.25× book) or the wrong leg (healthcare)** — you lose CPIC's **0.72× book / ~0.5× EV** bargain, and mostly don't even own CPIC | ETF = easy + diversified, but you own **US materials at ~15–16× P/E / ~12× EV/EBITDA (Vulcan/CRH/Eagle)** — you lose Buzzi's **~9× P/E + net-cash** single-name thesis, and don't own Buzzi |
| **Bottom line: ETF vs direct** | **Direct stock wins → PUK** (NYSE, ~20% ROE, ~100% Asia+Africa life, buyable on both brokers). Use **EWH** only if he wants AIA specifically; **AGNG** is an aging-demographics satellite, not this thesis. | **Direct stock wins → CRH or Eagle (EXP)** if he wants a single cheaper-than-basket name on his brokers; **Buzzi itself needs IBKR**. If he'll accept a basket, **PAVE** (or XLB/VAW) buys the trend — but not Buzzi's value/net-cash edge. |

**In one line:** *For both themes, an ETF gets Hooman the trend easily and on his own brokers, but it
averages away the cheap-value thesis that made CPIC and Buzzi interesting — and it barely (Buzzi) or
doesn't at all (CPIC) hold the specific name. The better answers remain the direct-stock alternatives:
**PUK** for the insurance/aging theme, and **CRH/Eagle** (or IBKR-for-Buzzi) for the materials/reshoring
theme.*

---

## Confidence & limitations

- **VERIFIED:** ERs and holdings for FXI 0.73%, MCHI 0.59%, EWH 0.50% (AIA 21.34% top holding), KWEB
  0.70% (internet, no insurers), KIE 0.35% / IAK 0.38% (both 100% US insurers — no Asian lifers; IAK's
  "Prudential" = US **Prudential Financial PRU**, not UK Prudential plc), AGNG 0.50% (aging *healthcare*),
  CHIX liquidated 2024-02-20; PAVE 0.47% (no Buzzi in 105 holdings; VMC 2.15%/MLM 1.94%/EXP 0.38%), XLB
  0.08%, VAW 0.09%, IFRA 0.30%, ITB 0.38%, XHB 0.35%, **EWI 0.50% with Buzzi confirmed at ~1.01% / #24**.
  Sources: iShares/SSGA/Vanguard/Global X/KraneShares product pages + stockanalysis.com holdings,
  as-of 2026-07-01/02/05 (per row above).
- **UNVERIFIED (flagged):** (1) whether **CPIC** sits in **MCHI's** ~586-name tail (free sources cap at
  top 25 — pull MCHI's SEC **N-PORT** to confirm; would be a fraction of a percent regardless); (2)
  whether **Buzzi** sits in **MXI's** 89 undisclosed tail holdings (bot-blocked this session — check the
  iShares holdings download / N-PORT); (3) **VGK** tail Buzzi weight; (4) exact insurer weights in broad
  Asia-ex-Japan funds (AAXJ). None of these would change the conclusion (any presence would be immaterial).
- **DATE/SOURCE caveat:** iShares CSV/N-PORT downloads were bot-blocked, so several tail checks relied on
  stockanalysis.com's aggregation of issuer data rather than the raw issuer CSV; ETF weights change daily.
- **Broker/tax:** Schwab/Questrade availability marked at the **US-listed-ETF level** (all named
  theme-proxy ETFs are US-listed and normally buyable in any account) — **confirm per-ticker + any
  registered-account withholding** with the broker/tax advisor. UCITS/London-listed funds (e.g. AGES) are
  **not** buyable for a Canadian resident (PRIIPs/KID). **This is research, not financial/tax/legal advice.**
