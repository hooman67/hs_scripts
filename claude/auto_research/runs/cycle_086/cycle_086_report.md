# Cycle 086 Report — Propane / LPG NFPA-58 System Inspection & Leak Check (head-on thesis)

**Date**: 2026-07-09
**Domain (Round-4 map #9)**: Propane dealers must perform NFPA-58/54 system inspections and
leak checks on delivery / at defined triggers (out-of-gas, meter change, first-fill, appliance
add). Thesis: digitize the inspection + own the per-tank/per-site system + appliance history and
compliance-due state → recurring-revenue flywheel that accrues to the founder's platform.

**Mandate to test the thesis, not confirm it.** This cycle attacks the head-on version of the
thesis: a mobile "gas check / leak check" inspection app for the propane field tech that
accumulates a per-account system register. The four mandatory gates (incumbent/OEM, moat, SAM,
buyer) are applied before any promotion.

---

## The decisive up-front finding (drives every rejection below)

The Round-4 map named the kill-risk as the **delivery ERPs** (ADD Systems, Cargas Energy, Blue
Cow). That was the wrong incumbent to fear. The real incumbents are **dedicated propane
safety-compliance SaaS vendors that already own exactly the per-account system-history flywheel
this thesis proposes to build:**

- **P3 Propane Safety** — "risk management technology and consulting service for propane
  suppliers." Cloud **P3 Compliance System** (mobile field inspection + desktop reporting) built
  specifically for **NFPA 58, NFPA 54, DOT, and state** requirements. Auto-check / error-reduction
  tech (claims industry doc-error rate 30% → ≤5%). Generates management reports for **cathodic
  protection, DOT cylinder requalification/recall, regulator replacement, NFPA-58 gas checks, tank
  management**. **~700 clients in retail propane + fuel oil.** **NPGA Affinity Program endorsed
  vendor.** Endorsed by Sapp Bros. as "the gold standard in propane safety and compliance
  software." Integrates with Blue Cow, ADD Systems, AgVantage (it "seeds customer account data"
  and "account losses and gains are pushed daily" from the ERP). [Brave search of p3propanesafety
  materials + partner endorsements — VERIFIED]
- **Tank Spotter** (tankspotter.io) — "the leading service tech management, safety compliance, and
  training platform." **65+ modules** for safety/service/sales/training/dispatch on any
  phone/tablet; **NFPA 54/58 auto-verified inspections**, digital docs with photos + GPS, ~500
  training videos. **100+ propane companies.** Positioned as a **complement** that "works alongside
  leading back-office systems." [tankspotter.io — VERIFIED]
- **RegO App** (RegO Products — a propane-equipment OEM) — **free** app on Google Play doing leak
  checks, pressure assessments, cathodic checks, appliance checks, system gas evaluations. [Brave
  — VERIFIED] This is the Round-3 "OEM ships it free" pattern that caps a standalone price near $0.
- **Others in-market**: Suburban Software "Gas Checks" module, Propane Safety Pro, FAT FINGER
  (paperless leak-check/inspection workflows), iRely i21 (fuel-delivery ERP). [Brave — VERIFIED]

**Consequence for the whole cycle**: the "no product exists / paper today" premise is FALSE.
Competitive density for the core inspection-app idea is **4–5** (established dedicated products +
an NPGA endorsement + a free OEM app), and the moat data asset **accrues to P3/Tank Spotter, not
to a new founder.** Every candidate below is scored against this reality.

---

## Step 1: Technology Discovery (10 candidates)

### 1. Mobile NFPA-58 gas-check / leak-check inspection app with per-account system register
- **Domain**: Propane field-service compliance
- **Breakthrough claim**: Cheap mobile forms + cloud sync + auto-generated compliance PDFs let a
  tech capture the on-delivery leak check and build a per-tank history.
- **TRL**: 9 (this is shipping software)
- **Status**: **REJECTED (Step 1)** — not a new technology and not an empty space. P3 (700+
  clients, NPGA-endorsed) and Tank Spotter (100+) already ship exactly this. INSTANT incumbent hit.

### 2. AI photo-verified leak-check documentation ("proof the test happened")
- **Breakthrough**: Vision model confirms manometer/gauge reading + timestamp/GPS to make the
  leak-check auditable.
- **TRL**: 7
- **Status**: PROMOTED (to test) — the "AI verification" wrapper is at least novel vs. plain forms.

### 3. Out-of-gas / interruption-of-service (IOS) recompliance-scheduling engine
- **Breakthrough**: Predict which accounts will run out and auto-schedule the mandatory
  leak-recheck-on-restore, driving recurring truck rolls.
- **TRL**: 7
- **Status**: PROMOTED (to test) — scheduling on owned history is the flywheel; worth funneling.

### 4. Cathodic-protection reading tracker for propane underground tanks
- **Breakthrough**: Log structure-to-soil potentials per buried tank; trend to next-due.
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — P3 explicitly generates cathodic-inspection management
  reports today; also overlaps Round-4 domain #4 (cathodic-protection survey, separate agent).

### 5. Regulator-replacement lifecycle predictor (25-yr NFPA replacement rule)
- **Breakthrough**: Track regulator install dates across accounts, flag the ~25-yr replacement.
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — P3 already produces "regulator replacement" management
  reports. Absorbable field of an existing product.

### 6. DOT cylinder requalification (5-yr / 12-yr) tracking for the exchange/cylinder fleet
- **Breakthrough**: Track requalification dates on portable DOT cylinders.
- **TRL**: 8
- **Status**: PROMOTED (to test) — carried to Step 2, but note P3 advertises DOT 5-yr
  requalification tracking already.

### 7. Meter-creep / pressure-decay auto-logger via Bluetooth manometer
- **Breakthrough**: BLE digital manometer streams the timed pressure-drop test into the app,
  removing manual transcription.
- **TRL**: 7 (BLE manometers exist; integration is the work)
- **Status**: PROMOTED (to test) — a hardware-integration wedge P3/Tank Spotter may not own.

### 8. First-responder / duty-to-warn digital delivery + acknowledgment ledger
- **Breakthrough**: Track the NFPA/DOT "duty to warn" consumer safety notices with e-signature
  proof of delivery.
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — P3 runs a dedicated "Duty to Warn" division ("700 clients").
  Fully owned.

### 9. Tank-set / system-drawing capture (as-built schematic per site)
- **Breakthrough**: Structured capture of tank size, regulator train, appliance list, line sizing.
- **TRL**: 8
- **Status**: PROMOTED (to test) — the "as-built system graph" is the closest analog to the
  septic/well as-built plant; test whether it's unowned.

### 10. LLM compliance copilot ("does this install meet NFPA-58 clearances?")
- **Breakthrough**: LLM answers code-clearance questions from a photo + inputs.
- **TRL**: 6
- **Status**: **REJECTED (Step 1)** — advisory, not a system-of-record; no data flywheel accrues;
  liability-heavy code interpretation; trivially cloned. Fails the moat gate on its face.

**Step 1 result: 5 promoted to Step 2 (#2, #3, #6, #7, #9), 5 rejected.**

---

## Step 2: Competitive Analysis + MANDATORY Incumbent/OEM Check

| Candidate | OEM does it? | Dedicated incumbent? | ERP bundle? | Density | Verdict |
|---|---|---|---|---|---|
| #2 AI photo-verified leak check | RegO free app captures leak checks | P3, Tank Spotter own inspection docs (photos+GPS already) | integrates w/ ADD/Blue Cow | **5** | REJECT |
| #3 IOS recompliance scheduler | — | P3 generates recompliance reports; ERPs own delivery scheduling | dispatch owned by ADD/Cargas/Blue Cow | **5** | REJECT |
| #6 DOT cylinder requal tracking | RegO/OEM | **P3 explicitly markets DOT 5-yr requalification tracking** | ERP asset registers | **5** | REJECT |
| #7 BLE-manometer auto-logger | manometer OEMs (test kit makers) may add BLE | P3/Tank Spotter own the surrounding workflow | — | **4** | REJECT |
| #9 As-built system-drawing capture | — | Tank Spotter "asset management + documentation"; P3 tank management | — | **3–4** | BORDERLINE → carry ONE forward |

**Findings:**
- Every candidate faces a **dedicated, funded, NPGA-endorsed compliance incumbent (P3)** whose
  marketing copy *is* the pitch ("NFPA 58, cathodic, DOT cylinder, regulator, meter creep,
  duty-to-warn"). Per the round-3 mandatory check, "incumbent's own marketing copy = your pitch"
  ⇒ density ≥ 4.
- The **flywheel data (per-account inspection + compliance-due history) already accrues to P3 and
  Tank Spotter**, both of which pull the account roster daily from the delivery ERP. A new
  founder cannot uniquely accumulate it — the incumbents sit on it and are wired into the ERP.
- **Only #9 (structured as-built system schematic)** has a thin "maybe less-owned" angle. Carry it
  to Step 3 in the strongest possible form, per bias-to-action, and let the SAM/moat gates rule.

**Step 2 result: 1 borderline promoted (#9), 4 rejected.**

---

## Step 3: Market Analysis (candidate #9 — As-Built Propane System Plant)

- **Product**: Structured per-site "system plant" — tank(s), regulator train, line sizing,
  appliance inventory, clearances, plus every leak-check/gas-check event over time; sold to
  independent propane dealers as their portable book-of-business compliance register.
- **Buyer universe (Gate 4)**: fragmented **private** propane dealer — GOOD (not a regulator/
  utility). ✅ But count it: **NPGA ≈ 2,400 member companies** total (the near-complete universe of
  US retail propane marketers). [Brave/NPGA — VERIFIED] The big-three MLPs (AmeriGas, Ferrellgas,
  Suburban) + Superior Plus + CHS are already on their own systems, so the *reachable independent*
  slice is maybe **~1,800–2,000 companies**.
- **TAM**: US propane retail market **$44.9B (2025), ~5.0% CAGR to 2033** [Brave/IMARC-type source
  — VERIFIED as an order of magnitude]. But that's fuel volume, not compliance-software spend.
- **SAM (bottom-up, the number that matters)**: ~2,000 reachable independents × a realistic
  **$3–8K/yr** safety-compliance ACV = **$6–16M**. Even at an aggressive $15K/yr (P3-consulting
  bundle pricing) it is **~$30M**. **FAILS the >$100M SAM gate by 3–15×.** [ASSUMED ACV; VERIFIED
  seat count]
- **Growth**: fuel demand is flat-to-modest (~5% nominal, largely price); household propane heating
  is secularly flat-to-declining as a primary heat source. Not a tailwind.
- **Status**: **REJECTED (Step 3)** — countable ~2,400-company buyer universe (a red flag, per the
  TAB lesson: a small countable universe is not a green field) ⇒ SAM well below $100M, and the
  same universe is already being sold to by P3 (700+) and Tank Spotter (100+), i.e. **~35% already
  penetrated by two incumbents.**

**Step 3 result: 0 promoted.**

---

## Step 4: Feasibility Analysis

No candidate reached Step 4 (all died at Steps 1–3 on the incumbent, moat, and SAM gates). For
completeness, had #9 reached here: technical risk LOW (pure CRUD/mobile SaaS — which is itself the
Round-3 anti-signal: cheap-to-build ⇒ trivially cloned by P3 in one sprint), moat risk HIGH
(flywheel accrues to P3/ERP), market risk HIGH (SAM < $30M, ~35% pre-penetrated). Feasibility
would be ~4/10.

---

## Step 5: Execution Plans

**None.** Zero graduates this cycle. Writing a build plan for an idea that fails the incumbent,
moat, and SAM gates would violate the honest-zero mandate.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 5 | 5 |
| Step 2 | 5 | 1 | 4 |
| Step 3 | 1 | 0 | 1 |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

**Honest read**: The head-on propane NFPA-58 inspection thesis is a **clean death**. It fails
three of the four mandatory gates simultaneously:
1. **Incumbent gate — FAIL.** P3 Propane Safety (700+ clients, **NPGA-endorsed**, ERP-integrated,
   "gold standard") + Tank Spotter (100+) + a **free RegO OEM app** already ship the exact product.
2. **Moat gate — FAIL.** The per-account system + appliance + compliance-due history — the precise
   flywheel the thesis banks on — **already accrues to P3/Tank Spotter**, which pull the account
   roster daily from the delivery ERP. A new founder cannot uniquely accumulate it.
3. **SAM gate — FAIL.** The entire buyer universe is **~2,400 NPGA companies**; reachable
   independents ~2,000; realistic SAM **$6–30M**, far below $100M, and already ~35% penetrated.
4. **Buyer gate — PASS.** Buyer is a fragmented private dealer (not a regulator) — the one gate it
   clears, but it can't save the domain.

This mirrors the Round-2/3 base rate exactly: a "paper process, no competition" pitch that, on the
mandatory incumbent check, turns out to have a dominant dedicated SaaS + an NPGA endorsement + a
free OEM app. Cycles 087–089 probe adjacent fuel-inspection angles to confirm the domain is
exhausted rather than just this one framing.
