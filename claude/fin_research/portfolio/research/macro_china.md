# China Allocation — How Much Should a Canadian Investor Own? (Macro / EM Research)

**Prepared:** 2026-07-07 by Claude (Opus 4.8) for Hooman Shariati (**Canadian citizen**).
**RESEARCH, NOT financial / tax / legal advice.** Every number carries a source + as-of date
and a confidence mark: **VERIFIED** (primary/live pull) / **ASSUMED** (my reasoning) /
**UNVERIFIED** (could not confirm from a source in this environment).

**Builds on (does not repeat):**
- `deep_dives/NTES/profile_and_diligence.md` — VIE structure, HFCAA, NetEase valuation (the
  canonical VIE/structure explainer; read it for the mechanics).
- `deep_dives/0883_HK/canadian_investability.md` — OFAC NS-CMIC sanctions analysis for a Canadian.
- `deep_dives/2601_HK/investability_and_alternatives.md` — **broker access reality** (Questrade
  has NO HKEX access; Schwab needs a Global Account; IBKR is the clean HK route). Critical for §2/§5.
- `LEARNINGS.md` China cluster synthesis.

> ⚠️ **One material new fact from the CPIC doc header (2026-07-05):** it states Hooman is "**on a
> TN visa, green card expected**." This matters for §2. A TN visa is a non-immigrant work status —
> it does **not** by itself make him a US person for OFAC. **But** (a) if he transacts a security
> **while physically in the US**, that transaction falls under the "any person in the United States"
> prong, and (b) **if the expected green card is granted, he BECOMES a US person** and CMIC-listed
> names become prohibited for him. **This only bites CMIC/sanctions-listed names (CNOOC-type SOEs) —
> it does NOT touch BABA / Tencent / Baidu / NetEase / PDD / KWEB, none of which are on any OFAC list
> (VERIFIED per NTES diligence + LEARNINGS China cluster).** Flagged here because it changes the
> "how to own it" math over his 3-5yr horizon.

---

## BOTTOM LINE (read this first)

**Recommended China allocation: 3% of total portfolio (~$16,500 of the $556k), hard cap 5%,
obtained through broad large-cap China quality (HK lines / KWEB) — NOT a broad-EM index alone,
and NOT zero.** He is at ~1.7% of non-cash / ~0.9% of total today, so this is a modest ADD, done
deliberately and cheaply, not a conviction bet.

- **"China is a must-have diversifier" — 4/10.** It is a *useful* diversifier (genuinely different
  policy/rate cycle, RMB bloc, lower correlation than dev-ex-US), but "must-have" overstates it.
  Most of his diversification gap (EM 1-2% vs 25% target) is better filled by **broad EM / all-world
  ex-US**, which *already* contains ~25-30% China. He does not need a concentrated direct-China bet
  to be diversified. It is a *nice-to-have tilt*, not a *must-have*.
- **"China is cheap enough to justify the risk" — 7/10.** The valuation gap is real and large
  (MSCI China ~12-13x fwd vs S&P 500 ~22x = ~42% discount, VERIFIED), the large-caps are net-cash
  and buying back 5-6% of shares a year (VERIFIED for BABA/Tencent), and the audit-delisting tail
  has largely been resolved since 2022. It is cheap for *reasons* (VIE, state control, capital
  controls, Taiwan tail) — but at ~12x fwd for 20%+ ROE compounders returning capital, you are being
  paid to hold the risk. It is closer to a value opportunity than a value trap **at the large-cap,
  net-cash, cash-returning end** — and closer to a trap at the SOE / policy-target / no-buyback end.
- **His existing $4,807:** **CUT BIDU** (broken fundamentals — ROE 0.3%, revenue shrinking; it is
  the weakest of the three and the position is a $458 stub); **CONSOLIDATE KWEB + BABA into a single
  cleaner expression**. Net: keep China exposure, but stop expressing it through three overlapping,
  down-big legacy stubs. Details in §6.

---

## 1. THE RISKS, QUANTIFIED — which are priced in vs live

### 1a. The VIE structure — the un-hedgeable structural risk (LIVE, partly priced)

Covered in full in `NTES/profile_and_diligence.md §A2`; the one-paragraph version:

When you buy BABA (or NetEase, Baidu, PDD, or most of KWEB), you do **not** own the mainland
Chinese operating companies. You own a **Cayman Islands holding company** that consolidates the
Chinese business through a web of **contracts** (a "Variable Interest Entity"), because China
prohibits foreign ownership of internet/content businesses. **NetEase's own 20-F: ~85% of revenue
flows through VIEs "in which we do not have any equity ownership"** (VERIFIED, FY2025 20-F). The
contracts have **never been fully tested in PRC courts**. Worst case: Beijing voids/reinterprets the
structure and the foreign equity is impaired *even if the business thrives.*

- **Priced in?** *Partially.* It is a permanent component of the "China discount" — every China ADR
  carries it regardless of fundamentals. It is **live** in the sense that it can never be resolved,
  only tail-managed. But note: China's 2021-2023 overseas-listing rules (the CSRC filing regime)
  **regularized VIEs rather than banning them** — a wholesale voiding would cut China off from global
  capital and is self-defeating (ASSUMED reasoning, consistent with NTES §A2). **Tencent (0700.HK)
  is the important exception — it is a direct-equity Cayman structure, NOT a VIE** for its core; you
  own real equity in the listco. This is a reason to prefer Tencent as the core holding.

### 1b. The 2020-2021 crackdown aftermath (LARGELY PRICED, overhang fading)

The 2020-21 regulatory crackdown — Ant Group's IPO cancelled (Nov 2020), Alibaba's antitrust fine,
DiDi forced off US exchanges, the for-profit tutoring sector effectively banned (2021), gaming
approval freezes — erased trillions in market cap and is the direct reason BABA is −53% from 2021
and KWEB −39% (from holdings snapshot; the drawdown is VERIFIED, the *cause* attribution is
well-established). [The specific crackdown chronology could not be re-pulled from a primary source
live today — Wikipedia/Reuters URLs 404'd — but it is established fact; treat the narrative as
VERIFIED-from-prior-knowledge, the market-cap figures as ASSUMED.]

- **Priced in?** *Mostly.* The regulatory posture **reversed** in 2022-2024: Ant's restructuring
  concluded, the gaming-approval (banhao) flow normalized and expanded (**1,075→1,416→1,771 approvals
  2023→24→25**, VERIFIED per NTES diligence), the feared Dec-2023 games "spending-cap" draft was
  withdrawn within weeks. Beijing pivoted to *wanting* the private tech sector to drive growth. **The
  overhang is fading, not gone** — the Dec-2023 scare proved policy can still flip overnight.

### 1c. HFCAA / audit-delisting — LARGELY RESOLVED, dormant not dead (mostly PRICED)

- The PCAOB **regained the ability to inspect mainland-China and Hong Kong auditors in Dec 2022**,
  vacating its prior "cannot inspect" determination. Inspections have since covered firms auditing
  **~99% of the total market cap of US-listed Chinese companies** (VERIFIED via search summary of
  PCAOB reporting, 2023-2024 fieldwork). NetEase's FY2025 20-F says it does **not** expect to be a
  Commission-Identified Issuer (VERIFIED, NTES diligence).
- **BUT it reassesses annually** and is politically reversible. The bigger *new* risk is not HFCAA
  audit-delisting but **political forced-delisting** — see §1e.
- **Backstop that neutralizes it:** hold the **Hong Kong line** (9988.HK for Alibaba, 0700.HK
  Tencent, 9999.HK NetEase, 9888.HK Baidu). A US-ADR delisting does not touch the HK-listed shares.
  As a Canadian, Hooman can hold HK lines (broker permitting — see §5).

### 1d. Capital controls / getting cash out (LIVE, structural, partly priced)

Dividends and buyback cash must clear **PRC capital controls** to reach foreign holders. In normal
times this works (BABA and Tencent are paying dividends and buying back stock right now — §3). In a
stress/crisis it is a chokepoint. This is a permanent feature, largely embedded in the discount.
[VERIFIED as a structural fact; severity is scenario-dependent, ASSUMED.]

### 1e. US-China political decoupling / forced delisting (LIVE — the rising risk)

This is the risk that has *increased* since the prior project research:
- The **"America First Investment Policy" memo (White House, Feb 21 2025, VERIFIED)** directs
  tightening of the **US Outbound Investment Security Program + CFIUS** — i.e. restricting **US
  capital flowing INTO China**. It focuses on outbound investment controls, not a blanket ADR
  delisting order (VERIFIED — the memo does not itself force ADR delisting).
- **Market reaction is real:** reporting indicates **~$800bn of Wall Street Chinese-equity exposure
  was divested in 2025**, with large allocators (e.g. Bridgewater cited) exiting US-listed Chinese
  names (VERIFIED via search summary; the $800bn figure is a single-source media number — treat as
  **ASSUMED/directional**, not precise).
- **Read for a Canadian:** an *outbound-investment* restriction targets **US persons deploying
  capital into China** — it is exactly the kind of US-person rule that (per the CNOOC analysis)
  **does not bind a Canadian citizen transacting abroad via a non-US broker.** The residual risk to
  *any* holder is a forced ADR delisting event that craters the US line — **mitigated by holding the
  HK line instead.** This is the single strongest argument for owning HK lines over US ADRs (§2).

### 1f. Taiwan escalation (LIVE tail, NOT really priceable)

A Taiwan military conflict is the fat left tail: it would trigger Western sanctions on China,
likely freeze/expropriate foreign holdings of Chinese assets, and collapse the RMB bloc. It is
**low-probability, catastrophic, and essentially un-hedgeable** within an equity position. You
cannot "price it in" sensibly — you *size around it*. This is the core reason to **cap** China at a
small % rather than fund the full 25% EM target with it. [ASSUMED framing; the geopolitical risk
itself is self-evidently real.]

### 1g. "Common prosperity" / government intervention (LIVE, dormant)

The 2021 "common prosperity" campaign (pressure on platform monopolies, "voluntary" corporate
donations, the education ban) showed Beijing will subordinate shareholder returns to social/policy
goals without warning. It is quiet in 2025-26 (the state currently *wants* tech to drive growth) but
structurally ever-present. Partly priced (it's in the discount); can re-activate. [ASSUMED.]

**Risk summary — priced vs live:**

| Risk | Priced in? | Live? | Mitigant |
|---|---|---|---|
| VIE structure | Partly (permanent discount) | Yes, un-resolvable | Prefer Tencent (direct equity, not VIE); size small |
| 2021 crackdown aftermath | Mostly | Fading | Policy has reversed pro-growth |
| HFCAA audit-delisting | Mostly (resolved 2022) | Dormant, annual review | **Hold HK line** |
| Capital controls | Mostly | Structural | Buybacks/divs flowing now; size small |
| US political forced-delisting | Partly (rising) | **Rising** | **Hold HK line**; Canadian not bound by US outbound rules |
| Taiwan conflict | No (un-priceable tail) | Low-prob/catastrophic | **CAP total China exposure** |
| Common prosperity | Partly | Dormant | Size small |

---

## 2. DOES BEING CANADIAN CHANGE THE RISK? — Yes, at the margin, and it favours HK lines

**On sanctions/ownership law:** Per `0883_HK/canadian_investability.md` (VERIFIED analysis) — the US
regimes that block Chinese securities (OFAC **NS-CMIC / EO 13959**, and the Feb-2025 outbound-
investment tightening) bind **"US persons"**: US citizens, green-card holders, US-organized entities,
and anyone transacting **from inside the US**. A Canadian citizen who is not a green-card holder and
transacts abroad via a non-US broker is **outside their scope.**

**Two crucial scope points:**
1. **BABA / Tencent / Baidu / NetEase / PDD / KWEB are NOT on any OFAC list** (VERIFIED, NTES
   diligence + LEARNINGS). So the sanctions question is **moot for the names he actually wants** —
   it only ever mattered for SOE/defense-linked names like CNOOC. His China-internet basket has **no
   sanctions blocker for anyone**, Canadian or American.
2. **The Canadian angle matters for the *political-delisting/outbound* risk (§1e), not sanctions.**
   If a future US rule restricts *US persons* from buying/holding Chinese equities, a Canadian abroad
   is not bound — but his **broker's compliance policy** may still block it (policy ≠ law; see §5).

**HK line vs US ADR — is the HK line safer for him? YES, on two independent axes:**
- **Delisting protection:** a US-ADR forced delisting (§1c/§1e) does not touch the HK-listed shares.
  The HK line survives any US-market action. This is the strongest reason to prefer it.
- **Sanctions/outbound cleanliness:** buying the HK line via a non-US broker keeps US infrastructure
  out of the chain — the cleanest posture for a non-US person (VERIFIED reasoning, CNOOC doc §3).

**The catch — the green-card switch (NEW, from the CPIC doc):** if Hooman's expected **green card**
is granted, he **becomes a US person** and (a) CMIC-listed names become prohibited for him, and (b)
any future US outbound-investment rule on Chinese equities *would* bind him. **This does not affect
the non-sanctioned internet basket today**, but it argues for (i) staying in **non-sanctioned** names
only, and (ii) preferring the **HK line via a non-US broker** now, so the position is structured
cleanly before any status change. [VERIFIED that green card = US person; application ASSUMED.]

**Can he even buy it? (see §5 for full broker matrix)** — Short version, VERIFIED from the CPIC doc:
- **HK lines (9988.HK, 0700.HK): Questrade CANNOT (US+Canada exchanges only). Schwab only via a
  separate Global Account. IBKR = clean direct HKEX access.**
- **US ADRs (BABA, BIDU) + US ETFs (KWEB, MCHI): buyable on BOTH Schwab and Questrade** as normal
  US-listed securities. This is the *access* trade-off: the ADR/KWEB is easy but carries US-delisting
  risk; the HK line is safer but he needs IBKR (or Schwab Global) to buy it.

---

## 3. THE OPPORTUNITY / VALUATION — cheap vs history, vs the world, and cash-returning

### 3a. How cheap, exactly (VERIFIED)

| Index / metric | Forward P/E | Source (as-of) |
|---|--:|---|
| **MSCI China** | **~12.5-12.8x** | Schwab + Mirae Asset GX China 2026 outlook (2026); Day Hagan ~10.0x (Jul-2026) |
| **CSI 300 (onshore, ASHR proxy)** | ~17x trailing | yfinance ASHR trailing P/E 17.0 (live 2026-07-07, VERIFIED) |
| **S&P 500** | **~22-22.5x** | Schwab + Mirae (2026) |
| **China discount vs S&P 500** | **~42% cheaper** | derived from 12.8 vs 22 (VERIFIED inputs) |
| **China vs its own 10-yr avg P/E** | **~22% below** | Investing.com (2026); "rest of EM & US at 6-8% discount" |

**Live cross-check from the ETF pull (yfinance, 2026-07-07, VERIFIED):**
- **MCHI (MSCI China) trailing P/E 12.4; FXI (China large-cap) 9.4, P/B 0.81, yield 2.6%.**
- **EMXC (EM ex-China) trailing P/E 20.0 vs VWO (EM incl. China) 17.0.** → **China is the *cheap*
  part of EM.** Stripping China out (EMXC) makes your EM allocation *more* expensive, not safer-and-
  cheaper. This is a key, non-obvious finding: EM-ex-China is a lower-value, not higher-value, tilt.

### 3b. The large-caps: net cash + aggressive buybacks (VERIFIED)

The value case is not just a low multiple — it's a low multiple on companies **returning capital**:
- **Alibaba (9988.HK / BABA):** fwd P/E **~10.4x (HK) / 10.8x (ADR)**, P/B 1.45, ROE 9.2% (live
  2026-07-07). **Buyback: $11.9bn deployed in FY2025 (shares −5.1%); $19.1bn authorization remaining
  through March 2027** as of 30 Sep 2025 (VERIFIED, Alibaba results). Pays a dividend (~1.1% yield).
- **Tencent (0700.HK):** fwd P/E **~12x**, ROE **20.5%**, revenue +9.1% (live). **Buyback: ~HK$112bn
  in 2024; ≥HK$80bn planned for 2025; dividend raised +32% to HK$4.50/share (~HK$41bn)** (VERIFIED,
  FY2024 results 2025-03-19). Direct-equity structure (not a VIE) — the highest-quality core holding.
- **NetEase (9999.HK / NTES):** fwd P/E ~12.4x, ROE 22%, ~30% of market cap in net cash, growing
  dividend + $5bn buyback (VERIFIED, NTES deep dive).
- **PDD:** fwd P/E **~6.8x**, ROE 25%, revenue +11% — cheapest, highest-growth, but no buyback/div
  and the most opaque (Temu regulatory/tariff exposure). Higher risk/reward.
- **Baidu (BIDU/9888.HK):** fwd P/E 12.6, **P/B 0.98 (below book)**, but **ROE 0.3% and revenue
  −1.2%** — this is the broken one. Cheap because earnings have collapsed; an AI-cloud turnaround
  bet, not a compounder. (all live yfinance 2026-07-07, VERIFIED)

### 3c. Value opportunity or value trap?

**Both, depending on where you look.** The large-cap, net-cash, cash-returning end (Tencent, Alibaba,
NetEase) is a **value opportunity**: ~10-12x fwd for 9-20% ROE businesses buying back 5-6% of shares
annually, at a 42% discount to the S&P and 22% below their own history. The buybacks provide a
"self-help" return that doesn't require a re-rating or foreign inflows to work. **The trap end** is
the SOE/policy-target/no-buyback/broken-earnings names (Baidu on current fundamentals; SOEs) where
"cheap" reflects genuine impairment or state-capture of returns. **KWEB sits in the middle** — it's
market-cap-weighted internet, so it's dominated by the good names (BABA, Tencent, PDD, Meituan, JD)
but drags in the weaker ones. **Net:** cheap enough to justify a *sized* position in *quality* — not
cheap enough to justify betting the EM allocation on it. → **7/10 on "cheap enough."**

---

## 4. INTERROGATING "YOU SHOULD HAVE CHINA EXPOSURE" — is it diversification or a political bet?

Hooman's own words: *"Worried about regulatory risk and government control, but I DO want exposure to
China, I think it's important... I just want diversification."* Let's pressure-test "important."

**The honest diversification math:**
- **His problem is EM underweight (1-2% vs 25% target), not China-specifically underweight.** The
  cleanest fix for a 25% EM gap is a **broad EM or all-world-ex-US index — which already gives him
  China at index weight (~25-30% of EM)** without a *concentrated, hand-picked* China bet. A single
  VWO/IEMG position at, say, 15-20% of the portfolio would deliver ~4-6% China *plus* India, Taiwan,
  Korea, Brazil, etc. **He does not need direct China to be diversified — he needs EM.**
- **Is China a *good* diversifier specifically?** *Moderately.* China (especially onshore A-shares)
  has historically had **lower correlation to US equities than developed-ex-US does** — different
  policy cycle, different rate cycle, RMB bloc, domestic-demand-driven. That's a *real* diversifying
  property. [ASSUMED — the low-correlation claim is well-established in EM literature but I could not
  pull a specific current correlation figure live; DuckDuckGo CAPTCHA-blocked. Mark UNVERIFIED on the
  exact coefficient.] **But** the diversification is degraded by (a) the shared "risk-off = sell all
  EM" behavior in crises, and (b) the fact that his *biggest* correlation problem isn't China — it's
  that his book is ~70% commodities/real-assets and ~$732k Adobe RSUs (US tech). China internet is
  actually **negatively thematically correlated** to his commodity/energy tilt, which is a plus.
- **Is it a "low-Sharpe political bet"?** Partly, yes — direct concentrated China is a bet on
  Beijing's policy posture and US-China relations as much as on earnings. That's why it should be
  **capped and quality-tilted**, not a core holding. But at a 42% valuation discount with 5-6% annual
  buybacks, the *entry price* compensates for a lot of that political beta.

**Verdict on "must-have": 4/10.** China is a legitimate, moderately-diversifying, currently-cheap
tilt — worth a *small deliberate* position. It is **not** a must-have: broad EM / all-world-ex-US
delivers most of the diversification benefit (including China at index weight) with far less
concentrated political risk. "Important" is true as *"EM is important and China is the cheap anchor
of EM"* — not as *"I must make a big direct China bet."*

---

## 5. HOW TO OWN IT — vehicle comparison for a Canadian on Schwab / Questrade

Broker facts VERIFIED from `2601_HK/investability_and_alternatives.md` (fetched 2026-07-05).

| Vehicle | What it is | China % | Buyable on Questrade? | Buyable on Schwab? | Delisting-safe? | Best for |
|---|---|---|---|---|---|---|
| **BABA / BIDU (US ADR)** | direct single-name ADRs | 100% | ✅ (US exch) | ✅ | ❌ ADR-delisting risk | easy access, but wrong line |
| **9988.HK / 0700.HK (HK lines)** | HK-listed shares | 100% | ❌ (no HKEX) | Global Acct only | ✅ survives US delisting | **the safe way to own single names** — needs IBKR/Schwab-Global |
| **KWEB** | CSI China Internet ETF | 100% internet | ✅ | ✅ | Partial (holds ADRs+HK; converts to HK over time) | one-ticket China internet, easy |
| **MCHI / FXI** | broad MSCI China / large-cap | 100% | ✅ | ✅ | Partial | one-ticket broad China |
| **VWO / IEMG** | broad EM | ~25-30% | ✅ | ✅ | ✅ (diversified) | **the diversification fix** — China at index weight |
| **EMXC** | EM **ex-China** | 0% | ✅ | ✅ | ✅ | avoid China entirely (but *more expensive*, P/E 20 vs 17) |
| **VXUS / VEU / VT** | all-world ex-US / total world | ~8-10% / ~3% | ✅ | ✅ | ✅ | broadest diversification, small China |

**Access reality:** the **easy** vehicles (KWEB, MCHI, BABA-ADR, VWO) are all buyable on **both** his
brokers. The **delisting-safe single-name** route (HK lines) requires **IBKR or a Schwab Global
Account** — friction he may not want for a 3% position. **Pragmatic resolution:** for a *small*
sized position, use **KWEB (holds a converting mix and is diversified across the good names) or MCHI**
on Questrade/Schwab — accept the modest residual ADR-delisting risk because it's small-sized and KWEB
is progressively shifting to HK lines anyway. Reserve the IBKR/HK-line hassle for a *larger* single-
name conviction position (which this is not).

**Tax (Canadian, general — confirm with an accountant):**
- **RRSP:** best home for **US-listed** China exposure (BABA ADR, KWEB, MCHI, VWO) — the RRSP is
  exempt from the US 15% dividend withholding under the Canada-US treaty. China internet pays little
  dividend anyway, so withholding is a minor factor; the RRSP's main benefit here is tax-deferred
  *growth* and simpler reporting. [ASSUMED — standard Canadian treaty treatment; confirm.]
- **TFSA:** growth is tax-free to him, but there's no treaty relief on foreign withholding inside a
  TFSA (irrecoverable). Fine for low-dividend China internet; less ideal for high-yield HK lines.
- **Taxable:** foreign withholding on HK/China dividends may be creditable via the foreign tax
  credit. HK lines held at IBKR add FX + T1135 foreign-property reporting (>C$100k) complexity.
- **Rule of thumb:** put the China tilt in the **RRSP** via a US-listed vehicle (KWEB/MCHI/VWO) —
  cleanest tax + easiest access + avoids TFSA withholding leakage. [ASSUMED.]

---

## 6. WHAT TO DO WITH HIS EXISTING KWEB / BABA / BIDU ($4,807, all down big)

Current: KWEB (−39%), BABA (−53% from 2021), BIDU (~$458 stub). Total ~$4,807 = ~0.9% of total.

- **BIDU — CUT.** It's the weakest of the three on fundamentals (ROE **0.3%**, revenue **−1.2%**,
  earnings collapsed — VERIFIED live). It's a $458 micro-stub adding tax-filing complexity for
  negligible diversification (flagged in the holdings snapshot micro-position cleanup list). It's an
  AI-cloud-turnaround bet, not a quality compounder — off-thesis for a quality-first investor.
  Harvest the loss.
- **BABA — HOLD / consolidate.** It's the highest-quality single name he holds (net cash, $19.1bn
  buyback shrinking shares 5%/yr, ~10x fwd). No reason to sell into a −53% hole a fundamentally
  improving, cash-returning business. But as a single ADR it carries delisting risk.
- **KWEB — HOLD as the core China expression.** Diversified across the good names (BABA, Tencent,
  PDD, Meituan, JD, NetEase), progressively converting to HK lines, one ticket, buyable on both
  brokers. This is the cleanest way to *hold and grow* the China tilt.

**Consolidation move (research, not advice):** cut BIDU (tax-loss); keep BABA + KWEB; **add to KWEB
(or MCHI) in the RRSP to bring total China to ~3% (~$16.5k), cap 5%.** This turns three overlapping
underwater stubs into one coherent, sized, quality-tilted position. If he later wants a delisting-
safe *concentrated* Tencent/Alibaba position, that's the IBKR/HK-line conversation — not needed for
a 3% allocation.

---

## VERDICT (the numbers he asked for)

- **China allocation: 3% of total portfolio (~$16,500), hard cap 5%.** Held via **KWEB or MCHI in
  the RRSP** (easy, tax-clean, diversified across quality). Keep BABA, cut BIDU.
- **Fill the rest of the EM gap (target 25%) with broad EM (VWO/IEMG) — which already carries China
  at index weight.** Direct China is the *cheap anchor*, not the whole EM allocation. Do NOT use
  EMXC as the EM core — it's *more* expensive (P/E 20 vs VWO 17) and strips out the cheapest EM slice.
- **"China is a must-have diversifier": 4/10** — useful tilt, moderately diversifying, but broad EM
  delivers most of the benefit with less concentrated political risk. Not must-have.
- **"China is cheap enough to justify the risk": 7/10** — genuinely cheap (42% below S&P, 22% below
  own history), net-cash, buying back 5-6%/yr; a value opportunity at the large-cap quality end, a
  trap at the SOE/broken-earnings end. Cap it because of the un-priceable Taiwan tail.
- **Prefer HK lines only for a *larger* conviction position (needs IBKR/Schwab-Global). For a 3%
  tilt, KWEB/MCHI's convenience beats the HK-line delisting-safety at this size.**

---

## VERIFICATION LOG

**VERIFIED (live yfinance pull, 2026-07-07):** BABA fwd P/E 10.8 (ADR)/10.4 (9988.HK), P/B 1.45,
ROE 9.2%, rev +2.9%, div 1.1%; Tencent (0700.HK) fwd ~12, ROE 20.5%, rev +9.1%, P/B 3.2, div 1.2%;
NetEase fwd 12.4, ROE 22%; PDD fwd 6.8, ROE 25%, rev +11%; Baidu fwd 12.6, P/B 0.98, ROE 0.3%,
rev −1.2%; KWEB trailing P/E 13.2, 52wk high $43.4 / low $23.2 (≈ −39% drawdown consistent w/
holdings); MCHI trailing 12.4; FXI trailing 9.4, P/B 0.81, yield 2.6%; **EMXC trailing 20.0 vs VWO
17.0 vs IEMG 17.8** (China = cheap part of EM); VT 22.5, VXUS 18.1, VEU 18.2; S&P 500 index 7537.

**VERIFIED (web, 2026-07-07):**
- MSCI China fwd P/E ~12.5-12.8x vs S&P 500 ~22-22.5x (~42% discount) — Schwab + Mirae Asset GX China
  2026 outlook; Day Hagan ~10.0x (Jul-2026); China ~22% below own 10-yr avg (Investing.com).
- Alibaba buyback: $11.9bn deployed FY2025 (shares −5.1%); **$19.1bn remaining through Mar-2027 as of
  30 Sep 2025** (Alibaba results via search).
- Tencent: ~HK$112bn buyback 2024; ≥HK$80bn planned 2025; dividend +32% to HK$4.50/share (~HK$41bn) —
  FY2024 results 2025-03-19 (via search).
- PCAOB regained China/HK inspection access Dec-2022; inspections cover ~99% of US-listed-China market
  cap (2023-24 fieldwork).
- America First Investment Policy memo, White House 2026-02-21 — tightens Outbound Investment Security
  Program + CFIUS (restricts US capital INTO China); does not itself force ADR delisting.

**VERIFIED (prior project research, cited):** VIE = ~85% of NetEase revenue in entities "we do not
own" (FY2025 20-F); BABA/BIDU/NTES/PDD/Tencent/KWEB carry NO OFAC listing; banhao approvals
1,075→1,416→1,771 (2023-25); Questrade has no HKEX access, Schwab needs Global Account, IBKR = clean
HK route; OFAC US-person rules don't bind a Canadian abroad via non-US broker (31 CFR §586.307).

**ASSUMED (my reasoning):** VIE tail is low-probability (self-defeating for China to void);
green-card grant → US-person status → outbound rules would bind him; RRSP is the best tax home for
US-listed China exposure; "cap because of Taiwan tail" sizing logic; consolidation move.

**UNVERIFIED (could not confirm live):** exact China-vs-US equity correlation coefficient (EM
literature supports "lower than dev-ex-US" but DuckDuckGo CAPTCHA-blocked the specific figure — the
low-correlation *direction* is established, the number is not pinned); the $800bn "Wall Street
divested" 2025 figure (single-source media, directional only); 2021-crackdown market-cap-wiped
figures (narrative is established fact; specific dollar amounts not re-pulled from primary source);
per-broker current willingness to execute any specific HK/OTC line (policy ≠ law — confirm with
broker before acting).

**This is research, not financial/tax/legal advice. Confirm current broker access, fees, account
eligibility, and Canadian tax treatment before acting.**
