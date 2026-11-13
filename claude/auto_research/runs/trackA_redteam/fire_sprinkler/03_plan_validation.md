# Plan Validation: Fire Sprinkler Inspection App

**Created**: 2026-07-02 by Claude (Opus 4.8, adversarial plan-validation pass). **Owner**: Hooman Shariati.
**Reviewing**: `01_redteam.md` (3.6/10 PASS) + `02_execution_plan.md` (validation-first, ~$2–5K, PASS).
**Method**: Red-team the red-team — check whether the plan's own assumptions hold, whether it is
too pessimistic OR too generous, independently rebuild the financials, and stress the time budget.
Web-verified where possible (search engines blocked in this env; vendor domains fetched directly).

**Verdict up front: the plan HOLDS.** It is one of the few plans in this project that is honest
in the correct direction. My independent rebuild lands *slightly worse* than the plan's own numbers,
not better. Confidence: HIGH on the PASS conclusion; MEDIUM on the exact dollar figures (WTP is
estimated, not LOI-verified — which is precisely what the plan says must be tested).

---

## 1. Fact-check of the load-bearing claims

| Claim in plan | Verification | Status |
|---|---|---|
| Inspect Point: 15,000+ users, 4.5M inspections, 20M assets, $100M invoices, branded AI ("Inspection Assistant", "AI co-pilot") | Fetched inspectpoint.com 2026-07-02: **all four figures confirmed verbatim**; two branded AI products confirmed; deficiency capture with notes + photos confirmed | **VERIFIED** |
| ServiceTrade: 1,300+ customers, office users free, tech-based subscription, Stella AI + Smart Assistants + Trade Intelligence | Fetched servicetrade.com 2026-07-02: **"1,300+ Happy Customers" confirmed; "Office users are always free … pricing lines up with your … technicians" confirmed; three AI products confirmed**. Exact $/tech not on public page (redteam's ~$75 is a secondary-source estimate) | **VERIFIED (structure); pricing = ESTIMATED** |
| BuildingReports 13M+ inspections | Not re-fetched this pass; consistent with prior fetch in 01_redteam | ASSUMED (prior-verified) |
| FireLab ~$299/mo flat, unlimited techs | Vendor domain fetch blocked this pass; carried from prior redteam digest | ASSUMED |
| Seat price is fiction ($199–399/seat vs. free-office/$75-tech/$299-flat market) | Directionally confirmed: incumbents price at the tech OR flat-company level and give office seats away free. A bolt-on AI feature priced ABOVE a full platform seat is not credible. | **VERIFIED (directional)** |
| Founder is non-domain, no iOS, no trade network | From founder profile / CLAUDE.md | VERIFIED |

**Net:** the two most important claims (incumbents own the whole workflow + branded AI; seat price
is inverted) are directly web-verified. Nothing in the fact-check softens the PASS — if anything the
incumbent AI is further along than the redteam assumed (Inspect Point now markets TWO distinct AI
products, including a portfolio-wide "co-pilot," not just a field checker).

---

## 2. Which plan assumptions are most likely wrong — and what happens if so

The plan is a PASS, so the risk is not "it's too optimistic and will lose money." The risk is the
opposite: **assumptions that are too GENEROUS would make even the ≤$5K validation phase or the
Plan B/PWA fallbacks look more viable than they are.** Ranked by likelihood × consequence:

**A. "PWA avoids the iOS hire and iPads run web fine" — MOST LIKELY WRONG, and it matters.**
A field deficiency-capture tool needs reliable **offline** operation (basements, mechanical rooms,
parking garages, no signal), fast **camera + burst photo** capture, and background upload. PWA
camera/offline/storage support on iOS Safari is historically the weakest of any platform
(background sync unsupported, storage eviction, camera quirks). The single hardest UX in this app —
capture photos of 40 heads in a dead-zone stairwell and sync later — is exactly what iOS PWAs are
worst at. *Consequence:* the plan's cost-saving move (PWA, no iOS hire) partially collapses; you
either accept a worse product in the field (kills trust in a trust-based sale) or you re-incur the
iOS-native hire the plan tried to delete, pushing build cost back toward the $60–90K range. This
does not change the PASS, but it undermines the plan's claim that build exposure stays ≤$75K.

**B. "Equity/rev-share domain partner solves distribution + data + credibility" (T1/G1) — OPTIMISTIC.**
The plan leans on this to erase three founder weaknesses at once and to keep cash low. But a
NICET-IV inspector or shop owner good enough to bring a trade network and proprietary photos is a
scarce, in-demand person with their own business; joining an unproven, non-domain, remote AI-manager's
side project for equity in a $0-revenue idea is a hard sell. *Consequence:* G1 is more likely to fail
than the plan implies — which is *fine*, because failing G1 by week 4 for ~$0 is the plan's designed
success case. The danger is a **weak** partner passing the gate (a semi-retired inspector with no
active book of business) who looks like a G1 pass but delivers neither distribution nor data. The
plan should tighten G1 to "active shop owner / practicing NICET-IV with a current client base," not
just "credible." Otherwise you spend the build tranche on a false positive.

**C. "General multimodal models can't do the core task zero-shot" is the *hoped-for* T4 — LIKELY FALSE.**
The redteam's own Claim G says GPT-5/Gemini-class vision increasingly does head-type ID and
paint/corrosion flagging zero-shot. That is the more probable outcome of the week-7 spike. *Consequence:*
G4 fails (or forces the pivot to a "structured NFPA-25 logic layer," which is a much smaller, less
defensible, and frankly less interesting product). This is a *feature* of the plan (kill-fast), not a
flaw — but it means the realistic terminal state of the validation is "G4 fails, stop," and the plan's
own upside branch is unlikely to open.

**D. "≥5 shops put money down at ≥$40/seat" (G3) is reachable in 10 weeks — OPTIMISTIC on timeline.**
The plan elsewhere concedes 3–6 month trust-based sales cycles and 40–60% still-on-paper laggards.
Extracting a *refundable deposit or signed LOI* from five conservative owner-operators — for an app
that doesn't exist, from a non-domain stranger, in 10 weeks — contradicts the same plan's cycle-length
claim. *Consequence:* G3 most likely returns "2–3 soft verbals, 0 signatures" → correct STOP. The plan
handles this correctly (verbal doesn't count), but the 10-week window is aspirational; realistically
G3 resolves at week 14–20, or never.

**E. Plan B (license CV module to an incumbent) is "lowest-time, highest-EV" — PLAUSIBLE BUT THIN.**
Inspect Point (15K users, 4.5M labeled inspections) has more training data and more distribution than
any module a solo could build; their rational move is **build, not buy**, especially now that they
already ship two AI products. A licensing deal is possible only if the solo's CV module is materially
better than what they can build in-house — unlikely given they hold the corpus. *Consequence:* T2/G5
probably returns polite non-interest. Plan B is correctly labeled "binary outcome," but its EV is
lower than "highest-EV" suggests; it's better described as "lowest-time, low-probability lottery
ticket." Doesn't change the PASS.

**None of A–E flips the verdict toward PURSUE.** Every wrong assumption pushes the same direction:
the idea is worse, or the kill happens even sooner and cheaper. That is the signature of a
correctly-pessimistic plan.

---

## 3. Independent conservative financial rebuild

Built bottom-up, ignoring the plan's numbers, then compared.

**Assumptions (conservative, defensible):**
- SAM: ~15K firms / ~50K inspectors; realistically-addressable "small shops still on paper, NOT on an
  incumbent, with acute liability pain" ≈ 40–60% of firms but only a fraction are reachable by a solo
  with no network → **serviceable-reachable ≈ 500–1,500 firms** over years, not year 1.
- Realistic ACV: a *bolt-on QA checker* against free-office / $75-tech / $299-flat incumbents supports
  **$40–80/seat/mo at best; $0–30 more likely** once buyers realize the platform they already pay for
  is adding the same AI. Use **$50/seat/mo** blended for the optimistic branch.
- Seats per shop: 2–15 inspectors, but a small shop buys 2–5 seats. Use **3 seats/shop**.
- **CAC**: non-domain solo, trust-based trade, 3–6 mo cycle, in-person/trade-show heavy. Even with a
  partner, realistic loaded CAC (ad spend + partner rev-share + your time valued at even $50/hr for
  ~15–25 hrs per closed shop) is **$1,500–3,000 per shop**. Against a $50×3 = **$150/mo/shop** gross,
  payback is **10–20 months before churn** — a broken unit economic for a solo secondary stream.
- **Churn**: SMB trade tools with a single-feature value prop and a cheaper/free incumbent alternative
  → **3–5%/mo logo churn** (36–60%/yr). Anything a shop can drop the moment their platform ships the
  feature free churns fast.
- **Gross margin**: software is high-margin, BUT this product carries an ongoing **domain-expert
  retainer ($1–2K/mo)** to keep NFPA-25 logic current + vision API inference cost per photo. Effective
  gross margin after those loads at low volume: **~55–70%**, not 85–90%.
- **Ramp** (only if all 5 gates pass — low probability): months 4–9 = 3–5 pilots, mostly free/discounted
  for data; months 9–18 = first paying shops; month 24 = **10–40 paying seats** (i.e. ~3–13 shops).

**Base case at 24 months (survives cold-start + lands a few shops):**
- 25 paying seats × $50 = **$1,250/mo gross revenue**.
- Less domain retainer ($1–1.5K/mo) + infra/API (~$200/mo) → **contribution ≈ –$500 to +$50/mo.**
- **Honest net: roughly $0/mo (break-even to slightly negative)** at month 24, after ~$40–75K sunk
  build + your unpaid hours. This is *worse* than the plan's stated "$0–2K/mo net" because I load the
  mandatory domain retainer as a real recurring cost against a $1,250/mo top line, and it swamps the
  contribution.

**Upside case (unlikely — survives, prices at $60/seat, reaches 80 seats / ~27 shops):**
- 80 × $60 = **$4,800/mo gross**; less ~$1.5K retainer + ~$400 infra → **~$2,900/mo contribution**,
  before valuing any of your ~15 hrs/wk time. Call it **~$2–3K/mo net.** Still below the $5–30K goal,
  and this requires beating an incumbent that can ship the same feature to 15K users first.
  Probability I'd assign: **<10%.**

**Downside / most-likely case: validation kills it.** ~$2–5K spent, 6–10 weeks, **$0 revenue, $0
ongoing** — and (correctly) freed hours. This is the modal outcome and the plan's intended win.

**vs. the optimistic 6.70 pitch's $1.79M ARR yr1 / $5.4M yr2:** off by ~1000×. My rebuild is *more*
pessimistic than the plan's own economics, confirming the plan is not sandbagging to look conservative.

---

## 4. Does it truly stay ≤10–20 hrs/wk?

**No — not in the build case; yes only in the (modal) kill case.**

- **Validation phase (weeks 1–12):** plausibly 10–15 hrs/wk of evenings. The vision spike (wk 7–8)
  is his strength and efficient. But weeks 3–6 (cold-DMing 30 owners, running 8–12 discovery calls,
  landing a partner) is scheduled outreach into a low-trust trade — high-friction, calendar-bound
  hours, not compressible. **Realistic: 12–18 hrs/wk during validation.** Borderline-OK.
- **Build + go-to-market (months 4–18, only if gates pass):** managing a PWA contractor + a domain
  partner + running pilots + trust-based selling into a conservative trade = **20–30 hrs/wk**, and
  the selling/relationship half lands in the *same evening hours CutLog needs* and cannot be
  delegated. **This violates the 10–20 hr/wk constraint.** The plan admits this (§6 "not delegable …
  same slot CutLog needs") — which is another reason its PASS is honest.
- **Plan B (BD/license):** genuinely lower time (a few BD conversations) — the plan is right that it
  fits a part-time envelope best. But its EV is a low-probability lottery (see §2E).

**Conclusion:** the plan's own caveat is correct. The *only* version that stays ≤20 hrs/wk is the one
that also makes ~$0 (Plan B lottery or the kill case). The version that could theoretically make
money blows the time budget and collides with CutLog.

---

## 5. Honest revised monthly profit

- **Modal outcome (validation kills it, likely):** **$0/mo**, ~$2–5K spent to learn it, hours freed.
- **Base case if it survives to month 24 (unlikely):** **~$0/mo net** (break-even to slightly negative
  after the mandatory domain retainer) — *worse* than the plan's $0–2K/mo, on my more conservative load.
- **Upside if it beats the odds (<10%):** **~$2–3K/mo net** at ~80 seats — still short of the $5–30K goal.

**Single honest number to carry forward: ~$0/mo (base), with a low-probability ceiling around
$2–3K/mo. Does not reach the $5–30K/mo target on any realistic path.**

---

## 6. Does the plan hold?

**HOLDS.** The plan reaches the correct verdict (PASS / do-not-build), for the correct web-verified
reasons, with a genuinely staged, gated, ≤$5K kill-fast structure that protects the founder's capital
and hours. My independent rebuild is *more* pessimistic than the plan's, not less — the mark of a plan
that is not spinning. Three refinements, none of which change the verdict:

1. **Tighten G1** from "credible NICET-IV/shop owner" to "**active** shop owner or practicing
   inspector with a **current client base**," to avoid a false-positive partner passing the gate.
2. **Don't trust the PWA cost-saving.** Field offline-photo capture on iOS Safari is the app's hardest
   requirement and PWAs are weakest there; if the product survives to build, budget for the iOS-native
   hire the plan tried to delete (build case → ~$60–90K, not ≤$75K). Bake this into the go/no-go so the
   "cheap build" assumption isn't load-bearing.
3. **Re-rank Plan B** from "highest-EV" to "lowest-time, low-probability" — an incumbent holding 4.5M
   labeled inspections will rationally build, not license.

**Bottom line: keep the PASS. Run the ≤$5K validation only if Hooman wants closure/optionality in this
space; otherwise skip straight to a higher-fit idea and protect the CutLog evening hours.** The single
best use of this plan is as a cheap, disciplined way to *confirm the kill* — which it does well.

---

## Sources
- inspectpoint.com — 15,000+ users, 4.5M inspections, 20M assets, $100M invoices; "Inspection Assistant" + "AI co-pilot"; deficiency notes+photos (fetched 2026-07-02).
- servicetrade.com/fire-inspection-software — "1,300+ Happy Customers"; office users free, tech-based subscription; Stella AI + Smart Assistants + Trade Intelligence (fetched 2026-07-02).
- Prior-verified (01_redteam.md, 2026-07-02): BuildingReports 13M+ inspections; FireLab ~$299/mo flat; general fire-inspection SW $29–$700+/mo.
- Founder profile / CLAUDE.md — non-domain, no iOS, no trade network, $25–150K, ~10–20 hrs/wk, $5–30K/mo goal.
</content>
</invoke>
