# Execution Plan: Fire Sprinkler Inspection App

**Created**: 2026-07-02 by Claude (Opus 4.8). **Owner**: Hooman Shariati.
**Inputs**: `01_redteam.md` (revised score **3.6/10, PASS, MEDIUM confidence**),
`deep_research/sprinkler_inspection/`, `MASTER_COMPARISON.md` (optimistic 6.70).
**Founder**: Adobe eng mgr; AI/ML + cloud + EE; $25–150K capital; ~10–20 hrs/wk;
wants $5–30K/mo; AI-safe preferred. **NOT his domain** (zero fire-protection knowledge,
no iOS, no trade network).

---

## 0. LEAD: Why this is likely NOT worth building (read this first)

The red-team verdict is **PASS**. This plan exists so the decision is made on evidence, not
on skipping the work. Bottom line up front: **do not build this as a startup.** Five reasons,
each independently fatal:

1. **The "empty quadrant" is false.** Inspect Point (15K users, 4.5M inspections), ServiceTrade
   (1,300+ customers, Stella AI), and BuildingReports (13M+ inspections) already ship the whole
   workflow — NFPA-25 forms, photo/deficiency capture, auto-report, AND branded AI. A CV
   head-recognizer is a **feature they can copy**, not a product you can defend.
2. **The data moat is inverted.** The proprietary labeled-photo corpus is already owned by the
   incumbents. You start at a cold-start wall — you need ~1,000+ labeled deficiency images that
   don't exist publicly and can only come from the conservative customers you can't reach.
3. **The seat price is fiction.** Market reality: ServiceTrade ~$75/tech/mo (office users free),
   FireLab ~$299/mo FLAT for a whole team. The pitch's $199–399/seat for a single bolt-on feature
   is 3–5× a full platform seat. Real WTP for the add-on: ~$0–30/seat. Revenue math off ~1000×.
4. **Founder-fit is inverted + it needs two hires.** Your genuine edge (CV modeling) is the
   commoditized part. The hard, non-delegable parts — domain credibility, trade trust, distribution,
   iOS field UX — are exactly your weaknesses. Real cash-to-MVP is $200–225K (over your ceiling)
   and requires hiring an iOS dev and a licensed fire-protection PE/NICET-IV expert.
5. **The buyer is slow and liability-averse.** 3–6mo trust-based sales cycles, 40–60% still on
   paper, "trust earned at trade shows." NFPA mandate makes them *warier* of unproven outsider AI,
   not more eager. This routes straight into your weakest muscle and consumes your scarcest hours.

**Honest economics**: Year-1 net ~$0 (negative after spend). 24-month base case if it survives:
$1–4K/mo gross → $0–2K/mo net. Low-prob upside: $3–6K/mo — but Inspect Point ships the same CV
feature to 15K users faster than a non-domain solo reaches 100 seats. This ranks **below CutLog
(4.5)** and **below buy-a-micro-SaaS (5.2)**.

### What would have to be TRUE to change the verdict

Only build if you can prove ALL of these BEFORE spending real money (see §7 validation):

- **T1 — A reachable co-founder/partner supplies domain + distribution.** A licensed
  fire-protection PE / NICET-IV inspector or a small-shop owner who becomes an equity partner (not
  a paid contractor), bringing the trade network and the labeled photos. Without this the moat and
  the distribution are both unsolved.
- **T2 — An incumbent wants to buy/license the CV module, not compete with it.** If Inspect Point
  or ServiceTrade signals real interest in a white-label CV deficiency-detector, this becomes a BD
  play (§6, Plan B) with a built-in data source and distribution — the only non-suicidal shape.
- **T3 — Real WTP for the standalone add-on is >$40/seat AND ≥5 shops will pre-pay.** Verified via
  paid LOIs, not verbal interest, from shops the incumbents *don't* already serve.
- **T4 — A defensible wedge exists that general multimodal models can't do zero-shot.** The core
  "identify head / flag corrosion" task is increasingly free from GPT-5-class/Gemini vision. You
  need a task that requires proprietary structured NFPA-25 logic + labeled edge cases, not a CNN.

If you cannot demonstrate T1–T4 in the ~$2–5K validation phase below, **stop**. The rest of this
plan is the disciplined path to test those cheaply and kill fast — it is NOT a green light to build.

---

## 1. IF you proceed anyway: the ONLY viable target segment / wedge

Do **not** attempt to build a competing platform. The only shape with any chance:

- **Wedge**: a **narrow, standalone CV "second-set-of-eyes" deficiency checker** that sits
  *alongside* whatever platform a shop already uses — not a replacement. It ingests photos the
  inspector already takes and flags likely NFPA-25 deficiencies (paint/corrosion, obstruction,
  wrong head type, missing escutcheon) as a QA/liability-reduction layer.
- **Target segment**: **small independent fire-protection shops (2–15 inspectors)** that are
  *still on paper/Excel* (the 40–60%) and are NOT customers of Inspect Point/ServiceTrade — i.e.
  the sliver the incumbents haven't captured. These shops have real liability pain and no AI.
- **Buyer**: owner-operator (not enterprise procurement). One person decides.
- **Positioning**: "cut your callback/liability risk" (a cost story on their next invoice), NOT
  "AI platform." Frame as insurance against a missed deficiency voiding a client's coverage.
- **Explicitly out of scope**: alarms, hydraulic design, scheduling, invoicing, multi-vertical.
  The moment you add these you are rebuilding the incumbent platform with none of their advantages.

Reality check: even this wedge is a hard sell and a small TAM. It exists here only because it's the
single configuration that doesn't require out-executing a $28M-funded 15K-user incumbent head-on.

---

## 2. First 90 days — week-by-week (validation-first, near-zero spend)

The first 90 days spend **~$2–5K total** and are designed to hit the T1–T4 go/no-go gates BEFORE
any hire or build. If any gate fails, you stop and keep the rest of the budget.

**Weeks 1–2 — Landscape + kill-check the premise yourself.**
- Demo/trial Inspect Point, ServiceTrade, FireLab, BuildingReports ScanSeries. Confirm exactly what
  their photo/deficiency + AI already do. Document the real feature gap (likely small).
- Read NFPA-25 ITM basics + 3–5 recent fire-inspection Reddit/Facebook threads. Cost: ~$0.

**Weeks 3–4 — Find the domain partner (T1). This is the real gate.**
- Post in fire-protection Facebook groups, r/fir eprotection, NFSA/AFSA chapter lists. Cold-DM 30
  small-shop owners and independent NICET-IV inspectors. Goal: 5 discovery calls. Offer nothing but
  a conversation about their liability/callback pain. Cost: ~$0.
- If NO credible domain person will even talk to you → **GATE G1 FAIL, stop.**

**Weeks 5–6 — Pain + WTP interviews (T3).**
- Run 8–12 structured calls with small-shop owners. Ask: how do you catch missed deficiencies today?
  What does a callback/liability incident cost you? Would you pay for a photo QA checker, and how much?
- Do NOT pitch. Listen for whether the pain is top-3 and unaddressed. Cost: ~$0.

**Weeks 7–8 — Zero-shot feasibility spike (T4). Plays to your actual strength.**
- Take 50–100 real deficiency photos (from partner or public sources) and test GPT-5-class + Gemini
  vision zero-shot vs. a light fine-tune. Measure accuracy on head-type ID + top deficiency classes.
- If general models already do this ~well zero-shot → your CV "moat" is gone → **GATE G4 FAIL, stop**
  (or pivot to pure NFPA-25 structured-logic layer). Cost: ~$200–500 API + your time.

**Weeks 9–10 — Fake-door / paid-LOI test (T3 hard proof).**
- Build a one-page landing + a Figma/clickable mock (no real app). Run $500–1,000 of targeted ads +
  partner referrals. Ask for a refundable $50–100 pre-order deposit or signed pilot LOI.
- Target: **≥5 shops put money/signature down.** Verbal "sounds cool" does not count. Cost: ~$1–2K.

**Weeks 11–12 — Incumbent-interest probe (T2) + decision.**
- Email BD contacts at Inspect Point / ServiceTrade proposing a licensed CV module. Gauge buy/partner
  interest (this is Plan B and often the better outcome).
- **Compile go/no-go against §5 gates. Default action is STOP unless every gate is green.** Cost: ~$0.

Total 90-day spend: **~$2–5K.** No hires, no app build, no long-term commitment until gates pass.

---

## 3. Path to revenue + realistic ramp

Only relevant if gates pass (low probability). Ordered by realism:

- **Fastest cash (Plan B, preferred)**: license/BD the CV module to an incumbent. One deal could
  return more than years of solo seat-selling and solves data + distribution. Ramp: 2–4 quarters of
  BD; outcome binary. This is a services/BD income, not a startup.
- **Direct wedge (Plan A)**: pilot 3–5 small shops → convert to paid at a **realistic $40–80/seat/mo**
  (NOT $199–399). Ramp: months 4–9 = 3–5 pilots (mostly free/discounted for data); months 9–18 =
  first paying shops; 24-month base case **~10–40 seats → $1–4K/mo gross → $0–2K/mo net.** Upside
  (unlikely): 50–100 seats → $3–6K/mo gross.
- **This does NOT reach the $5–30K/mo target on any realistic path.** Say so out loud in the go/no-go.

---

## 4. Itemized budget (within $25–150K; staged, gated)

Budget is released **in stages tied to gates** — you never spend the build tranche unless validation
passes. Total exposure if you stop at validation: **~$5K.**

| Stage | Item | Cost | Released when |
|---|---|---|---|
| **0 Validation** | Competitor trials, incidentals | $0–300 | now |
| | Zero-shot vision API spend (spike) | $200–500 | wk 7 |
| | Landing page + Figma mock + tools | $200–500 | wk 9 |
| | Fake-door ad spend | $1,000–2,000 | wk 9 |
| | **Validation subtotal** | **~$2–5K** | — |
| **1 Design partner** | Domain expert (NICET-IV) — **equity/rev-share, not salary** if possible; else short paid scoping | $0–5K | only if G1+G3 pass |
| **2 MVP (only if all gates pass)** | iOS/mobile contractor (thin PWA first, not native) | $30–60K | only if paid LOIs in hand |
| | Backend + CV pipeline (you build) | ~$0 (your time) + $2–5K infra/API | with Stage 2 |
| | Domain-expert retainer (keep NFPA logic current) | $1–2K/mo | ongoing |
| | **Build subtotal** | **~$40–75K** | gated |

Notes: (a) Prefer a **PWA over native iOS** to avoid the mandatory iOS hire and cut cost — iPads run
web fine. (b) Prefer an **equity/rev-share domain partner** over a paid contractor — it also solves
distribution and data (T1). (c) Keep total exposure under ~$75K even in the build case; do NOT hit
the $200K+ figure the optimistic BOM implied.

---

## 5. Go / No-Go gates (default = NO-GO)

| Gate | Week | Pass condition | On fail |
|---|---|---|---|
| **G1 Domain partner** | 4 | A credible NICET-IV/shop-owner will partner (equity or committed pilot) | STOP |
| **G2 Pain is top-3** | 6 | ≥6/10 interviewed owners name missed-deficiency/liability as a real recurring cost | STOP |
| **G3 Paid demand** | 10 | ≥5 shops put money down (deposit/LOI) at ≥$40/seat | STOP |
| **G4 Defensible tech** | 8 | Task is NOT trivially zero-shot for GPT-5/Gemini; proprietary logic adds real accuracy | STOP or pivot to structured-logic layer |
| **G5 Incumbent stance** | 12 | Either incumbents show partner interest (Plan B) OR clearly won't ship this soon (Plan A runway) | reassess |

**All five must be green to release the build tranche.** Any single fail = stop and keep the money.

---

## 6. Delegation to keep it part-time

- **You build**: backend + CV/ML pipeline + evals (your strength, ~5–8 hrs/wk).
- **Domain partner (equity/rev-share)**: owns NFPA-25 correctness, labeled-photo supply, trade
  intros, and pilot recruiting — the non-delegable trust work you cannot do yourself.
- **Contractor (only post-gates)**: PWA/mobile UI; well-specced, fixed scope.
- **Honest caveat**: even fully delegated, the trust-based selling is NOT delegable and lands on you
  or the partner in evening hours — the same slot CutLog needs. This is the strongest structural
  reason to prefer Plan B (BD/license) if T2 shows any life.

**Plan B (feature-partnership)** is the lowest-time, highest-EV shape: you build a CV module, license
it to an incumbent, they bring data + distribution. It is a BD deal, not a company — which fits a
10–20 hr/wk secondary stream far better than a direct-sales grind into a conservative trade.

---

## 7. Cheapest validation before spending real money (summary)

**Spend ≤$5K and ~6–8 weeks of evenings before any hire or build.** In order:
1. Trial the incumbents; write down the real (small) gap. — $0
2. Land one credible domain partner (G1). — $0
3. 8–12 pain/WTP interviews (G2/G3). — $0
4. Zero-shot vision spike on real photos (G4) — plays to your strength. — ~$500
5. Landing page + mock + fake-door with paid LOIs (G3 hard proof). — ~$1.5–2.5K
6. Probe incumbent partner interest (G5/Plan B). — $0

If gates don't all pass — the likely outcome — you've spent ~$5K to definitively kill it and free
your scarce hours for CutLog or a higher-fit idea. **That is the intended, successful result of this
plan.**

---

## 8. Recommendation

**PASS / do not build as a startup.** If Hooman wants exposure to this space, pursue only **Plan B
(license a CV module to an incumbent)** and only after the ≤$5K validation confirms T1–T4. On the
honest scale this ranks below CutLog (4.5) and buy-a-micro-SaaS (5.2); its best realistic outcome
($0–2K/mo net base case) does not meet the $5–30K/mo goal.
