# PLAN VALIDATION: Compressed Air Leak Detection

**Created**: 2026-07-02 by Claude (Opus 4.8, independent plan-validation pass).
**Owner**: Hooman Shariati (hshariati@adobe.com).
**Inputs**: `01_redteam.md` (revised 3.6/10, PASS, HIGH conf) and `02_execution_plan.md`
(a $1,500 6-week kill-test, PASS recommendation). This document is a *third-party audit* of
that plan: I did not take its conclusions on faith. I re-fact-checked the load-bearing claims,
rebuilt the numbers bottom-up, and stress-tested the weekly-time and profit assertions.

**One-line verdict: the plan HOLDS. Confidence HIGH.** The red-team's central busts survive
independent fact-checking, my bottom-up financials are *worse* than the plan's (not better), the
part-time constraint does NOT hold if hardware is ever built, and the honest revised profit is
**$0/mo base case**. The plan's kill-test is the right (and only) defensible action, but I'd tighten
it further: two of the plan's own gates are almost certainly unwinnable, so even the $1,500 is
optional — the desk research in Weeks 1–2 likely kills it for free.

---

## 0. What I independently verified (primary sources, 2026-07-02)

I re-fetched sources rather than trusting the red-team. Results:

| Claim under test | Verdict | Evidence I personally pulled |
|---|---|---|
| UE Systems only does periodic/handheld ("wrong positioning") | **FALSE — red-team is right** | uesystems.com/ultrasound-leak-detection/ confirms **OnTrak Wireless continuous remote monitoring** + software that "estimate[s] the leak rate, amount of energy wasted, and the greenhouse gasses" + Leak Survey SideKick App + DMS software. The category leader already ships continuous monitoring AND cost estimation. |
| The "$/month per leak" ML output is a defensible moat | **FALSE — table stakes** | UE Systems (above) and Prosaris both already estimate leak cost from dB. It is a calibrated-dB→flow calc, shipping for years, no ML needed. |
| Prosaris is "just a handheld," not a SaaS competitor | **FALSE — it's already a leak SaaS** | prosaris.ca confirms OL2 handheld + web "Platform": "Your team's event records, facility data, compressor set-ups... all in one convenient place." That is the exact software layer this idea proposed to build as its moat. |
| Leaks waste 20–30% of compressed-air energy (the ROI hook) | **VERIFIED (physics)** | DOE / Compressed Air Challenge figure, universally cited. UE's own page states "30% of all compressed air produced is wasted due to leaks." *This cuts against the startup* — see §1. |
| Atlas Copco SMARTAIRNET / Kaeser KMT do demand-side wireless leak analytics | **Could not re-fetch (domains blocked by enterprise net policy)** — but LEFT STANDING | The two I *could* verify (UE continuous+cost, Prosaris SaaS) are alone sufficient to bust the "empty lane" and "ML moat" claims. The OEM-bundling claim is well-documented and consistent; not load-bearing given the two confirmations above. |

**Net:** every claim I could independently reach confirms the red-team. Nothing I found softens it.
The two pillars of the original pitch — "empty lane" and "ML $/mo is the moat" — are both false on
primary evidence, not inference.

---

## 1. Which plan assumptions are most likely wrong, and what happens if so

Note: the *plan* (02) is already pessimistic, so "wrong assumptions" here means places where even
the pessimistic plan is still too generous. Ranked by likelihood × damage.

### A. (Plan's own Gate 3) "Buyers will pay $200/mo *ongoing* after leaks are fixed." — **almost certainly wrong**
This is the plan's flagged crux and I agree it's the single most likely failure. The value is
front-loaded: a leak survey finds the big leaks once; after the fix cycle the marginal value of
"catch new leaks" is small and slow-accruing. The entire incumbent market is structured around
*periodic* surveys (annual/biannual) precisely because that matches the value cadence — UE, Fluke,
CS Instruments, Prosaris all sell a *tool for a periodic hunt*, not a subscription. **If wrong (it
is):** the recurring-SaaS thesis collapses to a one-time service business (a few hundred dollars per
audit, no recurring margin, no scalability, no software moat). Revenue ceiling drops to
"consulting-with-a-detector," which does not clear the founder's bar and is not AI-safe/passive.

### B. (Plan's Gate 0) "A ≥100-plant slice exists that is non-OEM AND in a no-free-audit utility zone." — **likely wrong / self-defeating**
The slice the plan carves out to dodge the incumbents is defined by *absence of the very
infrastructure that signals a serious compressed-air spender*. Plants big enough to justify
continuous monitoring tend to be exactly the ones an Atlas Copco/Kaeser dealer has already courted
and/or the utility has already targeted with C&I efficiency programs. The residual slice —
serious air spend, no OEM relationship, no utility program, willing to buy from an unknown solo
vendor — is thin and hard to enumerate. **If wrong:** Gate 0 fails at Week 2 for $0. This is the
plan's cheapest and most probable kill, which is good design.

### C. (Plan §2, Weeks 10–11) "There's a buy-certified-nodes path that sidesteps the PCB/RF/FCC wall." — **partially wrong; margin trap**
White-label certified LoRa/BLE acoustic nodes *do* exist, so the plan is right that you needn't
design your own radio. BUT: (i) a pre-certified third-party acoustic node with the sensitivity to
do compressed-air ultrasound is not a $20 commodity — it pushes kit COGS up and gross margin down;
(ii) buying certified nodes means you own no hardware IP, so a fast follower (or the node vendor
itself) can replicate you; (iii) you still own field install, calibration, battery/RMA, and support
— the non-delegable time sink. **If wrong (margin worse than hoped):** the "$5K kit + $200/mo"
economics invert into low-margin hardware reselling with a support tail.

### D. (Plan §3) "~10–15% odds of the optimistic ramp." — **generous; I'd put it lower**
The plan chains four independent gates (0,1,2,3) each of which it rates "likely fails / coin-flip /
most-likely-fails," THEN requires a hardware build, THEN a cold-sales ramp. Multiplying even
charitable per-gate pass odds (0.5 × 0.5 × 0.5 × 0.35 ≈ 0.044) and then conditioning on shipping
reliable hardware solo and winning cold industrial deals, the realistic probability of reaching the
"~5 plants" state is **~3–7%, not 10–15%.** **If wrong:** expected value is even closer to $0.

### E. (Plan §5) "Some of the load is delegable (leads, dashboard, reports)." — **true but immaterial**
The delegable parts (lead lists, dashboard code, report templates) are the cheap parts. The
expensive parts (field installs, calibration, RMA, cold industrial sales, and — if built —
firmware/RF debugging) are non-delegable and time-elastic. **If wrong:** doesn't save the thesis;
delegating the easy 20% while owning the hard 80% is not part-time-safe (see §3).

**Assumptions I checked that the plan got RIGHT:** the competition busts (verified §0), the
free-substitute risk, the founder-fit inversion (hardware = his weakness), and the "hardware is the
LAST thing you build" sequencing. The plan's structure is sound; my disagreements make it *harsher*,
not kinder.

---

## 2. Independent bottom-up financial rebuild (conservative)

I ignored the pitch's numbers and the plan's numbers and rebuilt from unit economics.

### Capital to a *sellable* product (not a breadboard)
| Line | Conservative $ | Note |
|---|---|---|
| Validation phase (lists, detector rent, travel) | $1,500 | matches plan Phase A; reasonable |
| Pre-certified acoustic sensor nodes, pilot qty (20–30) | $10–25K | certified ultrasonic nodes are not cheap |
| Cloud/dashboard/ML | ~$0 cash (his hours) | his wheelhouse |
| FTO/IP check | $5K | |
| Enclosure/mounting (off-the-shelf) | $3–8K | |
| Initial inventory (50–100 nodes) | $15–40K | must pre-buy before sales |
| Field/RMA/support/insurance buffer | $10–30K | |
| **Total to first real revenue** | **$45–110K** | consistent with red-team's $50–150K; the pitched "$1.6K" is a breadboard, not a business |

### Unit economics if the optimistic path somehow fires (Year 2)
Assume the charitable state: 5 plants live, each $5K kit + $200/mo.
- **CAC:** cold industrial sales by an unknown solo founder → multiple site visits, long cycle.
  Realistic fully-loaded CAC (his time valued even modestly + travel) **$2–5K per plant**, and that
  ignores the deals lost to free audits/OEM bundling (which raise effective CAC further).
- **Recurring:** 5 × $200 = **$1,000/mo gross.**
- **Recurring net:** minus cloud/cellular (~$10–20/node/mo), support/RMA amortization, and his own
  field/monitoring hours → **~$400–700/mo net** at best.
- **Hardware "profit":** the $5K kit is mostly COGS (nodes + enclosure + install labor). Net margin
  on the kit after his install time ≈ break-even to slightly positive; it is a cash-flow item, not
  profit.
- **Churn:** given front-loaded value (Assumption A), annual logo churn **30–50%+** is realistic
  once leaks are fixed. At 5 plants, losing 2/year means you're running to stand still.
- **Ramp:** 12–18 months to shippable product + 6–12 months to 5 references = **18–30 months** to
  this state, at meaningful capital risk the whole time.

### Expected-value math (my numbers)
- P(reach the 5-plant state) ≈ **3–7%** (§1.D).
- Value of that state ≈ **$400–700/mo net**, declining with churn, capped low.
- P(base case $0) ≈ **80–90%** (fails a gate, or stalls at hardware, or loses to free substitute).
- **Probability-weighted expected monthly profit at 24 months ≈ $30–60/mo** — i.e. statistically
  indistinguishable from zero, for $45–110K at risk and ~18 months of the founder's scarcest hours.

This is *worse* than the plan's already-bleak framing, because I (a) lowered the success
probability, (b) added realistic CAC and churn, and (c) showed the hardware kit is not profit.

---

## 3. Does it truly stay <= 10–20 hrs/wk?

**During the kill-test (Weeks 1–12): YES, comfortably.** Desk research, ~15 interviews, 2–3 rented
audits, and a couple of vendor calls fit in ~5–12 hrs/wk of weekends. This part is genuinely
part-time-safe and cheap. Good.

**If it graduates to a product (Phase B): NO.** The build-and-sell phase breaks the constraint:
- Field installs + calibration + battery/RMA across a growing node fleet — **non-delegable, travels
  with headcount**, spiky (a dead node in a customer plant is a same-week fire).
- Cold industrial sales calls and site visits — **non-delegable**, long cycles, evenings/weekends
  don't align with plant hours (you need daytime, which he doesn't have as a full-time Adobe EM).
- If he ever touches firmware/RF (the plan rightly says don't) — **unbounded** evening soldering.

Realistic Phase-B load: **15–25 hrs/wk, largely daytime and non-delegable** — incompatible with a
full-time job and a 10–20 hr/wk secondary-income constraint. **Conclusion: the <=10–20 hr/wk claim
holds ONLY for the validation phase; it fails the moment the venture becomes real.** That asymmetry
is itself an argument to run the cheap test and stop — never enter Phase B.

---

## 4. Honest revised monthly profit

- **Base case (80–90% probable): $0/mo.** Killed at a validation gate, or stalls at the
  hardware/field-reliability wall, or every deal lost to a free utility/dealer audit or OEM bundle.
- **Optimistic tail (~3–7%): $400–700/mo NET recurring** at 18–30 months, declining with churn,
  after $45–110K capital — never approaching the $5–30K/mo target.
- **Probability-weighted expectation: ~$30–60/mo** — effectively zero.

**Honest number to carry forward: $0/mo (base case).** Any single positive figure overstates it;
if one must be quoted, "$0/mo base; a <$1K/mo net lottery tail at 18–30 months and $45–110K capital."

---

## 5. Does the plan hold?

**HOLDS.** Specifically:

- **Verdict (PASS):** correct and independently re-confirmed. The two competition claims I could
  reach (UE continuous+cost, Prosaris SaaS) are true on primary sources; the moat and "empty lane"
  premises are false. Nothing I found softens the PASS.
- **The financials:** my independent rebuild is *harsher* than the plan's — lower success odds,
  explicit CAC/churn, hardware-kit-is-not-profit. The plan did not under-state the downside.
- **The kill-test design:** sound and appropriately cheap ($1,500, staged gates, hardware last).
  This is the right way to say no with evidence.

**Two refinements I'd add (HOLDS-WITH-CHANGES on the *method*, not the verdict):**
1. **Front-load the free kill.** Weeks 1–2 (Gate 0, $0) and a few interviews (Gate 1, ~$100) will
   very likely kill it before any detector is rented. Spend the $800–1,200 detector money ONLY if
   Gates 0 and 1 pass. This drops the expected cost of reaching NO-GO from ~$1,500 to **~$100–200**.
2. **Reframe the exit, not just the kill.** Because the verdict is PASS with HIGH confidence and a
   pure-software candidate is a strictly better shape, the honest recommendation is: **don't even
   run the test unless Hooman has spare curiosity-budget.** The default action is *skip it and go to
   a pure-SW idea.* The test exists only to convert "I have a hunch about compressed air" into a
   $100 data-backed no — not as a step toward building.

**Bottom line:** The plan correctly says PASS, correctly designs a cheap kill-test, and correctly
prefers a pure-software candidate. My independent audit lowers the profit and success-probability
further and confirms the part-time constraint breaks in Phase B. Recommend **PASS**; if touched at
all, run only Weeks 1–2 (+ a few interviews) and let it die for ~$100.

### Sources I personally re-fetched (2026-07-02)
- UE Systems ultrasound leak detection — OnTrak Wireless continuous monitoring + leak-rate/energy/
  cost estimation + SideKick/DMS software (uesystems.com/ultrasound-leak-detection/). **Confirmed.**
- Prosaris — OL2 handheld + cloud "Platform" managing event records/facility data/compressor
  set-ups (prosaris.ca). **Confirmed as an existing leak-management SaaS.**
- DOE / Compressed Air Challenge 20–30% leak-loss figure (echoed on UE page "30% wasted").
  **Confirmed physics.**
- Atlas Copco SMARTAIRNET / Kaeser KMT / CS Instruments LD500 / Fluke ii900 pricing — pages blocked
  by enterprise network policy this session; left standing on the red-team's sourcing since the two
  independent confirmations above already carry the busts.
