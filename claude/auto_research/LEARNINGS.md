# Learnings

Durable learnings from this project. Consolidated here so they aren't scattered.

---

## ⭐ Survival AI device deep dive (2026-10-02)

- **“Offline LLM + manuals + maps + solar” is already a category, not a white space.** The search
  found 18 named direct mobile offerings, multiple $70–$2,500 device/USB offers, the actively
  maintained ~38.9K-star Project NOMAD stack, RACHEL AI, and many smaller open-source builds.
- **The exact open-source substitute must be checked before valuing integration.** Project NOMAD
  already combines Kiwix, global maps, optional local RAG, and a documented battery/solar build.
  Integrating public components is not itself a moat.
- **A modern phone is unusually difficult hardware to beat.** It already provides local-model compute,
  display, camera, GNSS, radio, battery management, sensors, charging, repair channels, and distribution.
  Custom consumer hardware should follow paid pull, never precede it.
- **“Has sensors” is also not a moat.** Direct competitors already claim phone-sensor context. The
  potential defensibility is an expert-reviewed mapping from trustworthy sensor data to bounded action,
  plus field outcome data—not the sensor BOM.
- **In high-stakes products, generation is not necessarily the product.** Deterministic protocol cards,
  exact citations, uncertainty and abstention can be safer than fluent free-form guidance. A local LLM
  should explain retrieved evidence, not control triage, routing, dosage, alarms, or SOS.
- **Certified safety functions should remain independent.** A startup should integrate with PLBs,
  satellite communicators and certified alarms rather than pretend a local model or hobby radio replaces
  them.
- **Content volume is a liability without governance.** Each manual/map needs rights, edition, region,
  review date, provenance and revocation/update handling. More scraped manuals can degrade both retrieval
  and safety.
- **Dense supply plus weak visible traction is an important adverse signal.** Most direct apps had
  little or no visible ratings; the highest direct Android install band found was only 5K+. The next
  uncertainty is paid demand, not another competitor search.

---

## ⭐ Courses + startup-platform scout + small-business revisit (2026-09-10)

- **Courses are viable only when the course is not the commodity.** Prerecorded marketplace royalties
  do not provide a credible $5K–30K/month path without an audience. The viable shape is a paid live
  diagnostic/workshop, followed by corporate training, a cohort, and only then reusable recordings.
  Buyers pay for judgment, feedback, artifacts, and team alignment—not more AI lectures.
- **Launch directories are distribution surfaces, not idea-validation engines.** Indie Hackers and
  Hacker News carry the best founder/pain signal; AlternativeTo, SaaSHub, and SourceForge help falsify
  ideas through incumbent/substitute mapping. Product Hunt and most other supplied directories are
  better used after validation for positioning, backlinks, and launch reach. Votes/listings/DR are not
  evidence of retention or willingness to pay.
- **Inherited distribution is the recurring winner.** The credible businesses found in founder
  retrospectives inherited buyers from consulting clients, an ecosystem, a pre-existing audience, an
  acquisition, or an operating company. Building first and submitting to many directories is the wrong
  order for Hooman's distribution profile.
- **The three independent tracks converged on service-first discovery.** The strongest common field-
  service wedge is read-only revenue-integrity assurance across calls/leads, jobs, invoices, and
  payments. It sells recovered dollars, sits beside rather than replaces the system of record, and
  produces the artifacts needed to decide whether a repeatable product exists.
- **Manager normalization remains the acquisition truth serum.** At normal small-business multiples,
  $150K all-cash usually buys less than the $5K/month target in SDE before replacing the seller. Only a
  business already run by a foreman/qualifier/manager can meet the time constraint; software upside
  cannot rescue owner-dependence.
- **$5K/month is a credible validation target; $30K/month remains upside, not a base case.** This holds
  across expert training, productized services, acquisitions, and franchises under the 10–20-hour and
  $25–150K constraints.

---

## ⭐ Round 4 (build cycles 051–100) — the "digitize a mandated trade" archetype is EXHAUSTED (2026-07-09)

Ran 50 fresh cycles across 10 CutLog/TitlePlant-class domains — licensed trades where the operator
was hypothesized to accumulate their OWN proprietary data (backflow testing, septic, water-well
"plant", cathodic protection, hood cleaning, marine survey, arborist, calibration-service, propane,
radon/ag-tile/locksmith). Plan in `runs/round4_domain_map.md`; per-cycle reports in `runs/cycle_051`–`100`.

**Result: 0 clean graduates across all 50 cycles.** Best single candidate = GeoLoop (GSHP borefield
thermal-data plant, cycle 063, ~5.0, conditional) — SAM-fragile, not conviction-grade. This is the
same near-total zero as Round 3 (100 ideas → 1 weak graduate), now confirmed for the "digitize a
regulated trade" archetype too.

**The two structural walls (why every domain died):**
1. **The "P3 pattern" — a trade-association-endorsed niche compliance-SaaS vendor already owns the
   flywheel.** In domain after domain the fear wasn't the ERP or the horizontal FSM (ServiceTitan/
   Jobber) — it was a *dedicated, trade-endorsed compliance SaaS* already sitting on hundreds of
   operators' data: P3 Propane Safety (~700 dealers, NPGA "gold standard"), DrillerDB (all 50
   states, 18M+ well records, already ships "AI quotes from local well data"), SingleOps (arborist
   per-tree history verbatim), National Onsite/SepticSnap (septic), Syncta/owned-by-Watts +
   BSI Online (backflow — "the Water Purveyor owns the data"), American Innovations PCS (90%+ of
   pipeline operators), IndySoft/Qualer→MasterControl (calibration). **NEW RULE for any future
   "digitize the mandated inspection" thesis: search FIRST for the trade-association-endorsed niche
   compliance SaaS — its existence, more than any ERP, collapses the moat.**
2. **The mandate that drives demand HANDS the data moat to the intermediary.** The regulatory tailwind
   (a real demand driver) creates a *mandated submission portal* (SwiftComply, BSI Online, OnlineRME,
   county e-permit portals) OR the base data is *government-published free* (state well logs, EPA radon
   maps, septic as-builts). Either way the compounding record accrues to the utility/agency's vendor
   or the public domain — the exact INVERSION of the CutLog/TitlePlant *archetype* (a founder-owned
   data flywheel where no one else re-publishes the assembled data). "Regulatory mandate = good" is only
   true if the operator, not a portal, owns the record.
   **Caveat on the archetype itself:** neither CutLog nor TitlePlant is a validated success — CutLog
   red-teamed 8.85→4.5 (false "no competition"; moat is community/distribution = founder's weakness);
   TitlePlant was Round 3's lone graduate but was NEVER deep-researched (cycle ~6/6, "likely low-5s",
   ASSUMED CAGR, E&O exposure, First American/Fidelity already run title plants). They are illustrative
   SHAPES, not wins. **Across Rounds 1–4 the founder-owned-data-flywheel archetype has produced zero
   clean GOs** — itself a strong argument to stop build-hunting and focus on the buy side.

**The deep-tail meta-learning (moat vs. SAM pull in opposite directions):** Where a solo founder
CAN uniquely own the data (ag drainage-tile as-built, locksmith key-plant — genuinely un-owned,
brand-siloed OEM clouds leave a real gap), the trade is too small: ~1,000–5,000 firms × low ACV =
$3–9M SAM, 10–30× under the $100M gate. Where the trade is big enough (radon), a device OEM
(Radalink/AirThings) already ships the report + geographic aggregation FREE. **The narrow,
incumbent-ignored trade that gives an own-data flywheel is structurally the one too small to matter;
the big trade already has its data owned. This is why the archetype is exhausted, not unlucky.**

**Decision:** stop running build/discovery cycles (category exhaustion now confirmed across Rounds
2, 3, AND 4). Do NOT spend Step-6 deep-research budget on any Round-4 output. The secondary-income
answer, if any, is on the BUY side, not the build side.

Per-cycle raw observations live in `patterns.md`; methodology changes in
`runs/plan_adjustments.md` and `deep_research/deep_research_adjustments.md`. This file is the
distilled, decision-relevant set.

---

## ⭐ Track-A red-teams + buy-SaaS playbook (2026-07-02)

Reports: `runs/FLAT_SHOWDOWN_V2.md`, `runs/buy_microsaas_PLAYBOOK.md`, `runs/trackA_redteam/`.

- **Compressed Air (opt. 7.65) → 3.6 PASS; Fire Sprinkler (opt. 6.70) → 3.6 PASS.** The predicted
  ~2–4pt red-team haircut landed almost exactly. Same failure pattern as everything else: false
  "empty/low competition" (Fire Sprinkler: Inspect Point 15K users, ServiceTrade, BuildingReports
  already own NFPA-25; Compressed Air: Atlas Copco SMARTAIRNET / Kaeser KMT bundle it + free
  utility audits), gross-read-as-profit, top-decile-as-base-case, inverted founder-fit (Fire
  Sprinkler needs $200K+ and 2 hires; Compressed Air needs a solo HW/RF/FCC build outside his domain).
- **Every idea in the project that has been red-teamed lost 2–4 points and landed 3.0–5.2.** This
  is now a robust base rate: optimistic cycle/discovery scores are inflated ~2–4 pts by unchecked
  competition + gross/net + top-decile framing. Trust red-teamed scores only.
- **Buy-a-micro-SaaS (5.2) is the confirmed merit pick** — the ONLY candidate whose lever is
  capital, not scarce evening hours, with capped downside (all-cash + earnout/escrow; AVOID SBA/PG).
  But honest reality: $80–120K buys ~$1.5–2.5K/mo net (~13–22% gross yield), churn ~4.5%/mo,
  base case flat-to-decline, **true net after his time ≈ $0–2.5K/mo — NOT a $5–30K/mo machine.**
- **The delegation-affordability rule (reusable):** delegation (VA+dev) only pencils above
  ~$4K/mo net; below that the owner IS the operator. The affordable asset can't fund delegation;
  the delegatable one exceeds a $150K budget. Resolve by engineering net up yourself, not delegating.
- **His edge is diligence alpha (spotting traps), NOT value-creation alpha** — small B2B SaaS
  churns on relationships/support/domain trust, not code quality; don't pay a premium to "rewrite."
- **Meta-conclusion across all tracks: NO idea researched clears a clean GO for $5–30K/mo
  part-time at $25–150K.** The honest options are (a) deploy capital into buy-SaaS as a modest
  ~13–22% yield with resale optionality, or (b) don't deploy the slot yet. Worth revisiting whether
  the $5–30K/mo target is realistic for a part-time secondary at this capital level.

---

## ⭐ FLAT SHOWDOWN — CutLog red-teamed, no protection (2026-07-02)

Report: `runs/FLAT_SHOWDOWN.md`. After Hooman said he'd abandon CutLog for something better, I
red-teamed CutLog + the fab-shop platform on the same harsh scale as everything else.

- **CutLog: 8.85 → 4.5 once scrutinized.** It was only #1 because it was EXCLUDED from the V2
  re-scoring and never faced the competition check that cost every other idea 2–4 pts. Same
  failure pattern as the busted batch: false "zero competition" (lasertips.org live free clone;
  LightBurn/Bystronic/TRUMPF/IPG ship built-in parameter tables), false network-effect moat
  (a free unmonetized wiki already holds the network; contributors ≠ payers), false $400/mo WTP
  vs free substitutes, and the hobby-data-vs-industrial-revenue segmentation trap.
- **The meta-lesson (process bias): never exempt an in-flight/incumbent project from the same
  validation applied to alternatives.** Protecting CutLog as "the baseline" + "would this
  distract from CutLog?" silently penalized every alternative AND spared the incumbent scrutiny
  — a double bias. Rank flat, red-team the incumbent too. (Memory: feedback_no_sunk_cost_cutlog.)
- **A BUILD-fit edge is not a moat.** CutLog is the best *build* fit (his stack, ~$0), but the
  moat is community/distribution/B2B-trust = his documented weakness, and someone already built
  that community for free. "It's easy for me to build" ≠ "I can win it."
- **Sunk cost near-zero cuts both ways:** abandoning CutLog costs ~nothing and SAVES the
  8–15 hrs/wk of non-delegable focus that blocks the capital-led buy-SaaS path. The two
  decisions are linked — freeing CutLog's focus is what makes a second stream viable.
- **Honest flat ranking:** buy-a-micro-SaaS 5.2 (best, capital-led) > CutLog 4.5 ≈ hosting 4.5 >
  fab-shop 4.4 > bookkeeping 4.3 > exam-prep 3.5 > licensing 3.0. Fire Sprinkler/Compressed Air
  still un-red-teamed (optimistic 6.70/7.65 → est ~4.5/~5.0). **No idea earns a clean GO for
  $5–30K/mo.** CutLog is arguably the LEAST AI-safe build idea (an LLM can generate param tables).

---

## ⭐ Track B DEEP DIVE — validation of the top 5 (2026-07-01)

Deep research + execution plan + adversarial red-team of all 5 top ideas. Report:
`runs/trackB/DEEP_DIVE_SYNTHESIS.md`; per-idea docs in `runs/trackB/deep/{slug}/`.

**The accountability lesson: the Track-B discovery scores were systematically optimistic.**
- **Validated profit was ~1/3 to 1/2 of every pitch** — a recurring failure where GROSS revenue
  was read as PROFIT, and top-decile "proof" examples were sold as base cases (Drone Launch
  $50K/mo = a 2016 early-mover outlier, partly insurance; HostiFi = survivorship). Always
  discount income-report "proof" for survivorship bias and gross-vs-net.
- **"Underserved niche" claims need the same incumbent check as Track A** — bookkeeping's
  "underserved SaaS finance-ops" is actually the MOST AI-penetrated corner (Kruze, Pilot, Zeni,
  Fondo). The Track-A moat/incumbent gate applies to lifestyle ideas too.
- **Founder-fit can INVERT on scrutiny** — the two "his wheelhouse" software ideas (hosting,
  micro-SaaS) turned out to depend on his WEAKNESS (community/sales/trust), not his infra/code
  strength. "It's technical, so it fits me" is a trap; ask what the *moat* actually is.
- **"Passive/delegable" rarely survives** — the non-delegable core is exactly the judgment/
  QA/relationship work a cheap VA can't do; realistic load was 8–15 hrs/wk sustained on all 5.
- **Delegation-affordability math is a hard gate for acquisitions** — on a small cash-flowing
  asset, VA+contractor cost can consume ALL the profit, so "buy and delegate" quietly becomes
  "buy and operate yourself."
- **What survived: downside safety + capital fit + the "capital+delegation not focus" thesis.**
  For a founder already in a 0→1 grind (CutLog), time is THE constraint; a second stream must
  run on capital+delegation, and even the best candidate (buy-a-micro-SaaS) behaves like a focus
  bet for its first ~6 months.
- **Net: none of the 5 clears a clean bar right now. The validation's own recommendation is to
  do nothing new and protect CutLog's focus** — a genuinely useful "no" that prevents splitting
  scarce hours across two 0→1 efforts.

---

## ⭐ Track B — lifestyle/secondary income search (2026-07-01)

Full report: `runs/trackB/TRACKB_REPORT.md`. 39 opportunities across 6 business shapes, scored
on the Track-B scorecard (path-to-success 20%, income/durability/capital/time, downside,
feasibility). Mandate: $5–30K/mo, part-time, $25–150K, outside AI hype, any shape, clear path.

**Top bets** (weighted /10): Certification/licensing exam-prep course (8.6), Managed technical
hosting / DevOps-lite "HostiFi model" (8.4), Vertical bookkeeping subscription (8.15), License
an engineered product for royalties "inventRight" (8.15), Proprietary-data subscription (8.0),
Buy a cash-flowing boring B2B micro-SaaS $80–150K (7.85), Self-storage / laundromat (7.75).

**The headline recommendation is counterintuitive and important:**
- **The shapes that look LEAST like his day job score highest** — delegated services, boring
  physical assets, mandated-exam courses — because they route around his one real weakness:
  **distribution/sales to fragmented buyers.** The shape that looks MOST like his job
  (build a micro-SaaS from zero) is the seductive trap.
- **"Buy the customers" beats "build the customers"** for a founder whose only gap is
  distribution + who has capital + a diligence brain. Acquisition (Empire Flippers/Acquire)
  sidesteps the 0→1 grind entirely.
- **Micro-SaaS success is a top-~5–7% outcome** (survivorship bias in the "indie SaaS to $10K
  MRR" narrative; fast-ramps usually had pre-built audiences). Discount from-zero build playbooks.
- **Time — not capital or ideas — is the true constraint.** ~10–20 hrs/wk = ONE serious
  venture. The right filter for a SECOND stream: "does it consume *capital + delegation* or my
  *scarce focus*?" Prefer capital-consuming shapes for a secondary stream.
- **Managed hosting is the rare case where day-job infra skills transfer 1:1** (infra IS the
  product; the tool's own community is the distribution).
- **Regulatory mandate drives demand in Track B too** (exam-prep for required credentials,
  compliance recordkeeping) — mirrors Track-A learning.
- **Consumer SEO content + commodity FBA are structurally broken** (Google HCU, AI Overviews,
  race-to-zero). Reject on sight. Owned-audience + recurring-SaaS are the AI-safe replacements.
- **The SBA personal guarantee is the ONLY place in Track B he can lose more than his cash**
  (physical buys). Real-estate-collateralized deals (self-storage) cushion it; leases don't.

**The honest bottom line from the report:** do NOT start a from-scratch lifestyle *build* right
now — it would put him in a SECOND 0→1 distribution grind while CutLog is still in its first.
If he wants a second stream that doesn't steal focus from CutLog, make it a **capital + delegation
bet** (buy a cash-flowing micro-SaaS or a self-storage/laundromat), and optionally dabble in
**royalty licensing** in the background (<$5K, ~5 hrs/wk, compounds silently). → This is now a
decision for Hooman: (A) buy-and-operate a cash-flowing asset, (B) royalty licensing as a
background bet, (C) both, or (D) stay 100% on CutLog.

---

## ⭐ Round-3 wider-net (2026-07-01) — the counterintuitive one

**Casting a wider net into software-native domains BACKFIRED — and that is the finding.**
10 fresh, broad software domains (fintech, digital health, edtech, climate-SW, robotics-SW,
generative-AI media, trust & safety, bio informatics, consumer/prosumer, vertical-AI agents),
100 ideas scanned → **1 graduate** (TitlePlant AI, 6/6 cycle score, likely low-5s after deep
research). Full report: `runs/round3_report.md`.

- **Software-native domains are the MOST incumbent-saturated, not the least.** The traits that
  make a domain founder-friendly (cheap to build, high CAGR, no hardware) are exactly what
  attract maximum VC and maximum cloning. **Low build cost is an anti-signal for defensibility
  at the DOMAIN level, not just the idea level.**
- **The moat gate is the highest-leverage filter we've added.** Reframing "is there
  competition?" → "does the defensible asset accrue to the FOUNDER or to whoever owns the
  system-of-record / the data?" killed 9 of 10 domains instantly and correctly. In software
  verticals the SaaS-of-record already sits on the flywheel data → moat accrues to incumbent.
- **"Perfect founder-fit" is a TRAP FLAG in crowded domains.** GenAI media and fintech are
  Hooman's strongest-fit domains and the WORST for defensibility — perfect fit means the space
  is obvious to every other capable founder too. Fit = necessary-but-dangerous, never a green light.
- **Growth rate was never the constraint** — all 10 domains cleared >15% CAGR. High CAGR is a
  *crowding cause*, not a green flag. Stop leading with market size.
- **Distribution OEMs weaponize "free"** — YouTube/Amazon/Meta/Google/Adobe/Unity/Intuit ship
  your exact feature free to retain users, capping standalone price at ~$0 (domain-level pattern).
- **The winning archetype is narrower than "pure software":** it is **"a proprietary data
  flywheel the solo founder can bootstrap and uniquely OWN, in an underserved niche incumbents
  aren't watching."** That's CutLog's class — and it's rare because in most software verticals
  the system-of-record owns the data. TitlePlant survived only because title agents can
  *accumulate* their own title-plant data rather than layer AI on someone else's.
- **Adobe's C2PA work forecloses trust-safety/provenance for Hooman specifically** (his
  employer co-leads the free open standard = owns the "moat").
- **Domain exhaustion is now confirmed at the CATEGORY level, not just the cycle level.**
  → **STOP running new discovery cycles.** Leverage is in deep-validating the handful of
  moat-bearing ideas already found (CutLog, the fab-adjacent cluster, Fire Sprinkler,
  possibly TitlePlant), not scanning more domains.

---

## ⭐ Round-2 deep research (2026-06-28) — the biggest learning

**Cycle scores are systematically inflated; moat is the kill dimension.** All 19 Tier-1
cycle-21–40 graduates carried 8–9/10 cycle scores. Deep research cut every one of them down
(avg ~5.1), and **14 of 19 had a FALSE "no competition" premise** — a funded incumbent or OEM
already ships the core product. The cycle stage cannot see incumbents (private/European/OEM);
only deep research + web validation can. This is the strongest argument for never skipping
the deep-research step.

- **Moat collapsed to 2.8 avg** (vs 5.4 for the original 30). The funnel got great at finding
  cheap, buildable, well-fit ideas — and those exact traits mean anyone can copy them, so a
  funded player already has. **Capital efficiency gets you to the start line; only a moat
  keeps you in the race.** Cheapness was the trap.
- **"Cheap + trivial to build" is a FAILURE signal, not a green light.** PestDoc had the
  lowest tech-risk of all (9/10) and is NO-GO precisely because the incumbent who owns the
  workflow can build it too. Low tech-risk + low moat = absorbable feature, not a company.
- **The hidden hard part is usually hardware/chemistry, not software** — ppb ethylene sensing
  (FreshGuard), wet-textile NIR (NIR Laundry), trace-O2 (NitroGuard). The valuable/defensible
  part is the sensor a software founder can't cheaply build; the software is the commodity.
- **Always check growth rate, not just size.** Several "large markets" are flat/shrinking:
  dental labs (-1.6%/yr), craft breweries (-2.9% in 2025), cabinet shops (-0.6%/yr).
- **Add an incumbent/OEM + growth-rate check at the CYCLE stage**, not just deep research —
  one search for the OEM + one for the European QC firm would have caught most of these.
- **Net:** nothing in the new batch beats CutLog (8.85); the genuinely valuable thing it
  surfaced is *adjacency* — Plasma/Springback/CNC-router cluster around CutLog's exact
  buyer/channel/stack → a fab-shop platform play, not a separate company.

---

## About idea selection (most important for picking the #2 idea)

1. **Pure software ideas score 2–3 points higher than hardware ideas** on the deep-research
   scorecard for this founder. Hardware adds a 1.5–2.5 pt penalty (PCB, firmware, sourcing,
   manufacturing, installation).
2. **Capital efficiency is the dominant ranking factor.** A $200K idea at 7/10 beats a $3.5M
   idea at 7/10. Low capital = faster validation, less dilution, more attempts.
3. **Founder-market fit is the most *discriminating* dimension** (avg 4.1/10 across 30 ideas).
   It's why good-sounding ideas (alloy software, livestock tags, cubesat) crashed. Anything
   needing PhDs / wet labs / novel manufacturing scores low for Hooman.
4. **Tech-risk < 5 ⇒ overall < 6, always.** Unresolved technical uncertainty kills everything.
5. **Market size is the *least* discriminating** dimension (avg 6.4) — most ideas target big
   markets, so size alone doesn't predict success.

## About the winning archetype

6. **"Software on existing hardware" beats "software + commodity hardware."** Layering AI on
   gear the customer already owns (XRF guns, telematics, press cameras, SCADA) removes all
   hardware risk. Best of all: **parasitic SaaS** on existing APIs (Samsara, Geotab,
   SolarEdge) — no physical world at all.
7. **"Democratize an expensive tool" and "digitize a manual/paper process"** are the two
   winning patterns. For a software founder, #2 (digitize) is better — no hardware.
8. **Network effects / data flywheels** (community parameter sharing) make ideas defensible —
   this is exactly why laser cutting won round 1.

## About competition & markets

9. **Always check for entrenched European industrial-QC firms** (SIKORA, Pixargus, Dr. Schenk,
   GlassQuality, Precitec, Marposs). Invisible on Crunchbase, dominant in their niche.
10. **Competitive density correlates with market size.** $1–10B industrial niches (density
    2–3) are the sweet spot; <$100M micro-niches are often empty *for a reason*.
11. **Regulatory compliance MANDATES are a demand driver.** Customers can't say "we'll wait."
    Helping meet an existing reg = gold; needing approval to sell = death trap.
12. **"Invisible waste" is the best ROI story.** If the customer can't currently see the
    waste, making it visible = instant demand (welding gas, laundry chemicals, N2 leaks).

## Instant-reject domains (don't spend research time)

13. Printing/packaging inspection (saturated), glass QC, injection molding, construction tech,
    consumer hardware, government/utility buyers (12–24mo procurement), FDA/regulatory-
    approval-gated products, anything requiring PhD specialists or wet labs.

## About process / validation

14. **Facebook groups are the highest-signal B2B validation channel** for manufacturing
    (laser/CNC/welding shop owners actively share parameters and troubleshoot there).
15. **Mark confidence on every feasibility claim** (VERIFIED / ASSUMED / UNVERIFIED) and
    include a cheap "Phase 0 PoC" path (<$100, <1 week) plus a "known false assumptions"
    callout. (Adopted from the Sonic Wand deep-research.)
16. **Domain exhaustion hits ~35 cycles.** More breadth = diminishing returns. The leverage
    now is deep-research + real-world validation of existing graduates, not more cycles.

## Source quality

17. Best sources: IEEE Spectrum, company websites (esp. European), trade publications
    (Welding Journal, Food Engineering), industry association sites, arXiv (cs.RO, eess.SP).
18. Weak/blocked: TechCrunch (consumer/fintech), Nature/Science (paywall), Product Hunt
    (consumer), Crunchbase/PitchBook (blocked — funding data is a persistent gap).
</content>
