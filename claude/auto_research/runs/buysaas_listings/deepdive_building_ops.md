# Deep Dive — "High-Yield Building Ops Platform" (Acquire.com)

**Owner**: Hooman Shariati (hshariati@adobe.com). **Written**: 2026-07-02 by Claude (Opus 4.8).
**Trigger**: Capital ceiling raised $150K → **$300K**. This listing was flagged in
`runs/buy_microsaas_LIVE_LISTINGS.md` (row 12) as "what good looks like" but was rejected on
size. Re-examining under the new ceiling.

**One-line verdict**: A genuinely high-quality asset (vertical B2B, ~91% margin, growing,
sticky) but at an **implied ~$1.6–1.8M asking it is ~5–6x over the new $300K ceiling.** Even
the most aggressive conceivable seller-financing structure does not close that gap without
either (a) an SBA 7(a) loan that reintroduces a **personal guarantee** (kills the capped-
downside thesis) or (b) a seller note so large no rational seller of a clean, growing asset
would accept it. **Verdict: PASS as a control buy; the realistic move is a smaller sibling.**

---

## 1. ACCESS REALITY — what is public vs gated (read this first)

**The individual Acquire.com listing detail is NOT publicly indexable.** Confirmed by direct
fetch attempts (Google/Bing/DuckDuckGo return only Acquire's generic marketplace copy) and by
the access-caveats table in `LIVE_LISTINGS.md`: on Acquire, **without a verified buyer login +
NDA** you get only the title, price band, TTM revenue/profit, tech stack, a customer *band*,
and founding year. Exact customer count, churn, concentration, full P&L, and seller identity
are all **gated behind buyer verification + NDA**.

**Therefore every number below sourced to the listing is "as previously captured in
`LIVE_LISTINGS.md`" (itself a gated-view snapshot), and must be re-verified live before any
offer.** I could not independently re-open the listing page via web fetch — it requires the
authenticated Acquire buyer portal. This is a **hard gate**, not a research failure: the next
click for real numbers is a free Acquire buyer account + NDA, not a web search.

| Fact | Status |
|---|---|
| ~$438K ARR, ~$399K SDE, ~91% margin, ~4–4.5x SDE, growing | **GATED-SNAPSHOT** (from LIVE_LISTINGS row 12; re-verify) |
| Exact asking price | **GATED** (implied ~$1.6–1.8M from 4–4.5x SDE) |
| Customer count / concentration / churn | **GATED** (not captured) |
| Owner hours/week | **GATED** (not captured) |
| Seller identity, full P&L, tech stack | **GATED** |

---

## 2. WHAT IT ACTUALLY DOES (niche profile — VERIFIED at niche level, ASSUMED at listing level)

"Building operations platform" in the facilities vertical is a **CMMS-adjacent
system-of-record**: work-order management, preventive/scheduled maintenance, asset registers,
vendor/technician dispatch, inspection & compliance logs, and building-systems tracking
(HVAC, elevators, fire/life-safety, etc.). The buyer is a property/facilities manager, a
building-ops team, or a multi-tenant landlord.

This is a **textbook Buy-Box-shaped niche** (VERIFIED against the playbook's ideal target):
- Vertical B2B, unglamorous trade.
- System-of-record → the customer's maintenance history, asset data, and compliance logs
  **live in it** → real switching cost = the moat.
- Recurring subscription, typically per-user or per-building/per-asset.
- AI-safe: it is a records/workflow tool with a data moat, not a thin LLM wrapper.

**Named competitors (VERIFIED via web search):** MaintainX (mobile-first, fast adoption, the
current mid-market momentum leader), Limble CMMS (deepest feature set, full-lifecycle asset
mgmt; Pro tier ~$75/user/mo), UpKeep (manufacturing/compliance audit-readiness angle), Fiix
(Rockwell-owned, strong G2 presence), Asset Panda, and at the property/building-specific end,
Building Engines and MRI/Yardi-adjacent modules. Pricing benchmark (VERIFIED): basic CMMS
~$39/mo entry, real mid-market spend ~$20–69/user/mo, premium ~$75–100/user/mo.

**Implication for moat:** the space is **competitive but fragmented**, and the incumbents
mostly chase enterprise or broad-horizontal CMMS. A ~$438K-ARR bootstrapped player almost
certainly survives by owning a **narrow sub-niche** (a specific building type, region,
compliance regime, or integration) rather than beating MaintainX/Limble head-on. **That niche
focus is the whole moat — and it is exactly what must be verified** (see §6). If it's a thin
horizontal CMMS competing on price with venture-funded rivals, the moat is weaker than the
91% margin makes it look.

---

## 3. THE NUMBERS (gated-snapshot; re-verify all)

| Metric | Value | Confidence |
|---|---|---|
| ARR | ~$438K (~$36.5K MRR) | GATED-SNAPSHOT |
| SDE / profit | ~$399K/yr (~$33.2K/mo) | GATED-SNAPSHOT |
| Margin | ~91% | GATED-SNAPSHOT |
| Implied asking | ~$1.6–1.8M | DERIVED (4–4.5x SDE) |
| Multiple | ~4–4.5x SDE | GATED-SNAPSHOT |
| Growth | "growing" (direction only) | GATED-SNAPSHOT — **magnitude unknown** |
| Customers / concentration / churn | unknown | GATED |
| Owner hours | unknown | GATED |

**On the 91% margin (why it's plausible AND a flag):** A bootstrapped, solo/near-solo SaaS at
this ARR routinely posts 85–92% "SDE margin" because **SDE adds the owner's own labor back**.
The 91% is largely *"there is no payroll because the founder does everything."* That is the
good news (lean, no team to retain) and the trap (the 91% silently assumes **free founder
labor** — the very hours Hooman would have to supply or pay for). **A 91% SDE margin at $438K
ARR is a strong signal that owner-hours are material and under-counted, not that the business
runs itself.** The playbook's delegation-trap math turns on exactly this.

**Growth caveat:** "growing" with no magnitude is the single biggest gated unknown at a
~4–4.5x multiple. 4–4.5x SDE is a *fair-to-slightly-rich* price for a **non-declining** asset
and a **bargain** for a genuinely growing one — but Acquire sellers frame flat-fragile as
"growing" routinely (deal-killer #2). The multiple only makes sense if growth is real and
durable; verify the MRR trend on raw Stripe.

---

## 4. DOES IT FIT THE NEW $300K CEILING?

**No — not outright, and not realistically even with seller financing.** The gap is ~5–6x.

**All-cash:** ~$1.6–1.8M vs $300K ceiling → **impossible** (over by $1.3–1.5M).

**Seller-financing path (the honest math):**
- Seller notes/earnouts are common in this market — "75–90% of small-business acquisitions
  under $5M involve seller financing" (VERIFIED via search) — **but** the typical structure is
  a *minority* seller note (10–30%) on top of a mostly-cash or SBA-financed bulk, NOT a
  90%-financed buyout. A seller carry that would let Hooman put in ≤$300K cash would require
  the seller to finance **~$1.3–1.5M (≈80–85%)** of a clean, growing asset. **No rational
  seller of a 91%-margin growing business does that** — they can sell all-cash to the $2B+ of
  verified buyer funds on Acquire. A seller *eager* to carry 80% would itself be a red flag
  (adverse selection: low confidence in their own numbers — playbook's earnout warning).
- Earnouts "bridge the gap in 33% of SaaS deals" but "average payout is just 21 cents on the
  dollar" — earnouts shift *risk*, they don't create *purchasing power*. They don't shrink the
  ~$1.3M cash Hooman doesn't have.

**SBA 7(a) path (the leverage that "fits" — and why to avoid it):**
- SBA 7(a) acquisition requires **~10% equity injection** (≥5% real cash) → on a $1.7M deal
  that's **~$170K down**, which *fits inside $300K*. On paper this is the only structure that
  makes the deal reachable. Recent SOP (June 2025) even lets a seller note count toward part
  of the equity injection.
- **BUT SBA 7(a) requires a mandatory personal guarantee** (SOP 50 10 8), typically secured
  against personal assets including a home lien. **This detonates the entire capped-downside
  thesis of this whole project.** The playbook (Days 50–58, and Sources) is explicit: *"AVOID
  SBA / personal-guarantee financing… an SBA-leveraged deal can lose more than the cash in via
  the PG."* An all-cash micro-buy caps max loss at price-minus-resale; a ~$1.5M SBA note with a
  PG means a business failure can cost Hooman **more than his entire down payment** — clawing
  into personal net worth. For a secondary-income side bet next to a W-2 and CutLog, that is
  the wrong risk shape.
- **SaaS SBA eligibility is also non-trivial** (must be for-profit, US-based, meet size
  standards, and lenders vary on how they treat recurring-revenue software with no hard assets
  to collateralize) — an added execution risk, not a blocker.

**Partial / minority path:** A minority equity stake in someone else's operated business is
not what Acquire brokers, is illiquid, gives no control, and doesn't match "buy a business I
run." Not a realistic route here.

**Verdict on fit: OVER-CEILING.** The only structure that mathematically fits ($170K SBA down)
requires the exact personal-guarantee risk the project was designed to avoid. Classify as
**FITS-WITH-FINANCING only in the narrow, discouraged SBA sense**; strategically it is
**OVER-CEILING** for Hooman's stated risk appetite.

---

## 5. DELEGATION VERDICT — and can Hooman's AI/data skills cut owner-hours?

**At ~$33K/mo net, this is the ONE listing surveyed where delegation genuinely pencils.** The
playbook's rule: *delegation (VA + contractor dev) only pencils above ~$4K/mo net.* At ~$33K/mo
this clears the bar ~8x over. A full delegation stack — offshore Tier-1 support VA
($800–1,500/mo) + contractor dev for bugs/small features ($800–3,000/mo) — costs ~$2–4.5K/mo,
i.e. **~7–14% of net**, leaving ~$28–31K/mo. This is the first asset in the whole survey that
could become **actually part-time / near-passive** rather than a self-employed job.

**Can Hooman's AI/data-engineering edge cut the hours further? Yes — meaningfully, but note the
nuance:**
- The LIVE_LISTINGS "40hr/wk sourcing ops" figure belongs to a *different* listing (the
  Amazon-seller sourcing SaaS, row 5) — **this building-ops platform's owner-hours are GATED
  and unknown.** Do not assume 40hr/wk here.
- Where his edge *does* apply: (1) **infra/hosting rightsizing** — one-time margin win, though
  at 91% there's little fat left; (2) **automating support triage** — an LLM-assisted
  ticket-deflection / knowledge-base / auto-response layer over an unglamorous CMMS is squarely
  his skillset and can cut Tier-1 hours before you even hire a VA; (3) **data-pipeline / SLA /
  compliance-report automation** — buildings generate recurring inspection/maintenance reports;
  automating those is high-value and defensible; (4) **onboarding/data-migration tooling** —
  the stickiest, most VA-unfriendly task, and the one where a data engineer shines.
- **Caveat (playbook WRONG-4):** his engineering skill is **diligence alpha** (spotting traps),
  **not value-creation alpha**. Small B2B SaaS churns on relationships/support/domain trust,
  not code quality. So: his skills can plausibly take owner-hours to a genuine <10 hr/wk *once
  a VA + his automation are in place*, but **the churn-save / key-account / roadmap work stays
  with him** and cannot be automated away. Delegation makes this a part-time asset; it does not
  make it zero-touch.

**Net delegation verdict: DELEGABLE — this is the rare listing large enough to run part-time
with a VA+dev, and Hooman's AI/data skills can additionally deflate the support/onboarding/
reporting load. If the price fit, this is the correct *shape* of asset for his goal.** The
problem is purely the price/financing gate, not the operability.

---

## 6. HONEST VERDICT: PASS (as a control buy) — with the deal-killers to verify IF financing were solvable

**PASS**, because at ~$1.6–1.8M it is ~5–6x over the $300K ceiling, and the only fitting
structure (SBA 7(a), ~$170K down) reintroduces a **personal guarantee** that violates the
capped-downside principle this entire buy-thesis rests on. This is not a numbers-quality
rejection — the asset looks *good* — it is a **risk-shape and affordability** rejection.

**The strategically correct read (per LIVE_LISTINGS §4):** this listing is valuable as a
**template**, not a target. It shows exactly "what good looks like" — vertical B2B facilities
SoR, ~91% margin, growing, delegable. **The right move is to hunt the 5–8x-smaller sibling**:
a facilities/CMMS/building-ops SoR at **~$60–90K ARR / ~$55–80K SDE**, priced **~$250–300K at
4–4.5x**, that fits the new ceiling all-cash and is *just large enough to begin delegating*
(~$4–5K/mo net clears the delegation threshold with room). That asset would deliver the same
shape within budget and without a PG. Set Acquire/EF/Flippa alerts for facilities-mgmt / CMMS
/ property-ops SaaS in the **$200–300K price / $4–6K/mo net** band.

**IF Hooman ever chose to pursue this specific one anyway (e.g. via SBA, eyes-open on the PG),
verify-first — the 8 deal-killers applied:**
1. **Live read-only Stripe + bank three-way reconcile** — reconcile bank ↔ Stripe MRR ↔ the
   P&L showing $438K/$399K. No live access → instant walk. (Acquire "verified" ≠ bank
   reconcile.)
2. **Growth magnitude & durability** — "growing" must be a real MRR uptrend on raw Stripe, not
   flat-fragile dressed up. At 4–4.5x, decline-masked-as-growth is the #1 risk.
3. **Cohort churn** — build the retention curve from the raw export; confirm revenue retention
   flattens and isn't propped by new-logo adds.
4. **Customer concentration <20%** — GATED and unknown; a $438K-ARR B2B SaaS can easily have a
   few large buildings/portfolios as whales. Ask "% of ARR from your single largest customer"
   on call one. >20% → walk.
5. **Real owner-hours & SOPs** — GATED; get the honest hr/wk and confirm the seller will do a
   60–90d transition with SOP handover (the 91% margin hides these hours).
6. **Moat / competitive position** — confirm the specific sub-niche it wins and that it is not
   a thin horizontal CMMS being slowly out-competed by MaintainX/Limble/UpKeep on price.
7. **Tech stack + clean IP chain** — GATED; confirm real custom code, every contributor's IP
   assigned, backups exist/tested, no single point of failure, true hosting cost (sellers
   understate it).
8. **Recurring vs one-time/services** — confirm the ARR is genuine subscription, not
   setup/implementation fees dressed as recurring.

**Confidence: HIGH** on the fit/verdict (the price-vs-ceiling math and the SBA-PG conflict are
robust and don't depend on gated numbers). **LOW** on the listing's internal specifics (all
gated; the snapshot numbers are unverified and must be re-checked live).

---

## Sources
- `runs/buy_microsaas_LIVE_LISTINGS.md` (row 12 snapshot; access-caveats table confirming
  Acquire gating) and `runs/buy_microsaas_PLAYBOOK.md` (Buy Box, 8 deal-killers, delegation
  threshold ~$4K/mo, explicit AVOID-SBA/personal-guarantee guidance).
- Acquire.com marketplace (generic pages public; individual listing gated behind buyer
  login+NDA — confirmed by fetch attempts returning only marketplace copy / 404, 2026-07-02).
- CMMS niche + competitors/pricing (DuckDuckGo, 2026-07-02): MaintainX, Limble (~$75/user/mo
  Pro), UpKeep, Fiix, Asset Panda, Building Engines; CMMS entry ~$39/mo, mid-market
  ~$20–69/user/mo.
- SBA 7(a) mechanics (DuckDuckGo, 2026-07-02): ~10% equity injection (≥5% cash); mandatory
  personal guarantee per SOP 50 10 8 (eff. 2025-06-01); seller note may count toward equity.
- Seller-financing / multiples (DuckDuckGo, 2026-07-02): seller financing in 75–90% of
  sub-$5M small-biz acquisitions; earnouts bridge 33% of SaaS deals at ~21c/$ average payout;
  bootstrapped SaaS multiples ~4–10x profit / 3.5–6x ARR at the lower-middle market.
