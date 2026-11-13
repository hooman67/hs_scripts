# EXECUTION PLAN: Compressed Air Leak Detection

**Created**: 2026-07-02 by Claude (Opus 4.8). **Owner**: Hooman Shariati.
**Basis**: the RED-TEAMED reality in `01_redteam.md` (revised score **3.6/10, verdict PASS,
confidence HIGH**), NOT the optimistic 7.65 deep-research pitch. Read that file first.

---

## 0. LEAD: Why this is very likely NOT worth Hooman's time

The red-team verdict is **PASS**, and this plan honestly leads with why. If you only read one
section, read this one.

**This is a hardware company disguised as a SaaS pitch, in Hooman's WORST-fit shape.**

1. **Not an empty lane — a crowded, mature category.** The single load-bearing premise ("only
   UE Systems overlaps") is FALSE. The three dominant compressor OEMs (Atlas Copco SMARTAIRNET,
   Kaeser KMT, Ingersoll Rand) already ship the *exact* wireless-sensor + cloud-dashboard +
   auto-leak-cost bundle — into accounts they already own, at near-zero CAC. Plus Fluke ($25K
   acoustic camera), CS Instruments, Sonotec, SDT, Prosaris (already a leak-SaaS), Distran.

2. **The core value is available FREE.** Utilities (Avista, Consumers Energy) pay for leak
   audits and rebate the savings; compressor dealers give free leak surveys to sell compressors.
   The buyer already gets "we found $30K in leaks" for $0.

3. **The winning axes are all Hooman's WEAKNESSES.** Success turns on custom PCB / STM32 firmware
   / RF-LoRa layout / enclosure tooling / FCC-CE cert / contract manufacturing / RMA logistics
   (a hardware company, not his domain) plus industrial maintenance-manager relationships (his
   documented weakness). The ML/cloud layer he *is* good at is the commoditized part — CS
   Instruments' $3–5K LD500 handheld already auto-computes cost-per-leak with no ML.

4. **Honest economics.** Base case (most probable): **$0/mo** — stalls at the hardware/cert/
   field-reliability wall or loses every deal to a free audit + OEM bundling. ~10–15% upside:
   **<$1–2K/mo net at 18–24 months**, after **$50–150K real capital** (not the pitched $1.6K)
   and **12–20 non-delegable hrs/wk** of firmware/RF debugging, field installs, RMA logistics,
   and cold industrial sales — the least AI-safe, least delegable load in the whole candidate
   set. It directly competes with, and is strictly worse than, CutLog's build hours, and does not
   approach the $5–30K/mo target.

**Recommendation: DO NOT BUILD.** If Hooman wants a build idea, a pure-software, zero-hardware
candidate is a strictly better shape. This plan exists only to (a) be honest about the odds and
(b) give a **cheap, time-boxed kill-test** so the decision is made on evidence, not vibes —
before any real money or a single soldered PCB.

### What would have to be TRUE to change the verdict (the falsification list)
All of these would have to hold, and they almost certainly won't:
- **A.** A specific segment exists that (i) has serious compressed-air spend, (ii) is NOT an
  Atlas Copco / Kaeser / Ingersoll account already getting bundled analytics, (iii) does NOT
  qualify for a free utility audit, and (iv) will pay for *continuous* monitoring, not a one-time
  survey. (Red-team: this slice is tiny.)
- **B.** Validated WTP for a *recurring* subscription that survives past the first fix cycle
  (value is front-loaded; leaks are found once). Needs ≥5 buyers verbally committing to $200/mo
  *ongoing*, in writing, before hardware.
- **C.** A no-code / off-the-shelf-hardware path to a reliable field product that sidesteps the
  PCB/RF/FCC wall (e.g. reselling a certified sensor + writing only the software layer). If the
  only path is "design your own certified radio," it is dead for this founder.
- **D.** A wedge the OEMs structurally *won't* copy (they already extended to point-of-use, so
  this is the hard one).

The 90-day plan below is designed to test A and B **on the cheap** and kill fast.

---

## 1. Target segment / wedge (the ONLY defensible slice, if any)

Do NOT chase "every factory." The red-team killed "universal market." The only slice worth even
a validation call is the **anti-incumbent, anti-free-audit** slice:

- **Segment**: single-plant, mid-market manufacturers (**50–250 employees**) that run
  compressed air heavily (injection molding, food/bev packaging, woodworking, metal fab,
  pneumatic-heavy assembly) **but are NOT an Atlas Copco / Kaeser / Ingersoll managed account**
  (i.e. they bought a compressor once, off-brand or old, and have no OEM analytics relationship),
  **AND are in a utility territory with no free C&I audit program.**
- **Geography**: pick 1–2 states with weak/no utility compressed-air rebate programs (the
  opposite of Avista/Consumers Energy territory) to avoid the free substitute.
- **Wedge (services-first, NOT hardware-first)**: sell a **paid one-time leak audit + a simple
  fix-tracking report** using a *rented/bought* off-the-shelf detector — deliberately mimicking
  the incumbent free service to test whether anyone will PAY at all. Only if paid audits sell,
  and only if the same buyers ask for *ongoing* monitoring, does the continuous-monitoring
  hardware thesis get tested. **The hardware is the LAST thing you build, not the first.**

Rationale: this inverts the pitch. The pitch led with hardware; the red-team says the hardware
is the death zone. Lead with a service to find whether demand exists at all, at near-zero capital.

---

## 2. First 90 days — week by week (a KILL-TEST, not a build)

**Budget for the whole 90 days: under $3K. No PCB, no firmware, no FCC, no inventory.**

**Weeks 1–2 — Desk validation / free-substitute mapping (0 spend).**
- List every utility in 3 candidate states; find which offer free/subsidized C&I compressed-air
  audits. Eliminate those territories.
- Confirm Atlas Copco / Kaeser / Ingersoll dealer coverage in remaining areas.
- GATE 0 output: a target list of ~200 plants that are NOT OEM-managed and NOT in a free-audit
  utility zone. If you cannot build a list of ≥100, **STOP — the addressable slice is a mirage.**

**Weeks 3–4 — Cold outreach for problem interviews (~$100 for lists/tools).**
- Reach 40–50 maintenance/plant managers via LinkedIn, phone, and 1–2 relevant Facebook groups
  (per LEARNINGS.md, FB is the highest-signal B2B-manufacturing channel).
- Ask: How do you find air leaks today? Have you ever paid for it? Would you pay for *continuous*
  monitoring, or just a periodic survey? What did the last audit cost/save?
- GATE 1 output: ≥15 completed interviews. Kill signal: "we get it free from our
  dealer/utility" repeated by >⅓.

**Weeks 5–6 — Rent a detector, do 2–3 PAID trial audits (~$1,000: rent CS Instruments LD500 or
buy a used ultrasonic detector).**
- Charge a real invoice ($300–500) for a manual leak audit + report on 2–3 of the warmest plants.
- The product here is YOU + a rented handheld. This tests WTP for the *value*, capital-free.
- GATE 2 output: ≥2 plants that actually PAY. Kill signal: everyone wants it free.

**Weeks 7–9 — Test the RECURRING thesis (the real crux).**
- Go back to the paid-audit customers ~3–4 weeks after they've fixed the found leaks. Offer a
  *monitoring subscription* ($100–200/mo) framed as "catch new leaks as they appear."
- GATE 3 output: ≥3 verbal/written commitments to pay monthly *ongoing*. Kill signal (most
  likely): "we found the leaks, we're good, no need to keep paying." This is the front-loaded-
  value kill-risk — expect it to fire here.

**Weeks 10–11 — Hardware reality-check (desk + 1 call, ~$300).**
- Only if Gates 0–3 pass. Scope the *minimum* path to continuous monitoring: can you RESELL a
  pre-certified off-the-shelf sensor (e.g. a certified LoRa/BLE acoustic node) and write ONLY the
  cloud/dashboard software? Get one quote from a contract-mfg / white-label sensor vendor.
- GATE 4 output: a credible non-hardware-company path (buy certified nodes, sell software). Kill
  signal: the only path is designing/certifying your own radio → PASS confirmed, stop.

**Week 12 — Go/No-Go writeup.**
- Roll up all gates. Default expectation per red-team: **at least one of Gates 1–4 fails → NO-GO.**

---

## 3. Path to revenue + realistic ramp

- **Cheapest revenue = paid manual audits (service), weeks 5–6.** A few hundred dollars each.
  This is the ONLY near-term revenue that doesn't require building hardware.
- **Recurring revenue** requires (a) surviving Gate 3 and (b) a reliable field product. Realistic
  timeline to a shippable continuous-monitoring product: **12–18 months**, and only if you take
  the buy-certified-nodes path (never design your own radio at 10–20 hrs/wk).
- **Realistic ramp if it somehow works (~10–15% odds):** ~5 plants in year 2 at $5K kit +
  $200/mo = ~$1K/mo gross recurring, hardware margin eaten by RMA/support/field time → **<$1–2K/mo
  net at 18–24 months.** Does not reach $5–30K/mo. Base case is **$0/mo**.

---

## 4. Itemized budget (staged; stop at each gate)

**Phase A — Validation ONLY (weeks 1–9), the only spend I'd authorize: ~$1,500**
| Item | Cost |
|---|---|
| Lead lists / LinkedIn Sales Nav (1 mo) | $100 |
| Rent or buy used ultrasonic detector for paid audits | $800–1,200 |
| Travel to 2–3 local plants | $200 |
| Misc (invoicing tool, printing reports) | $100 |
| **Phase A total** | **~$1,500** (well under $25K floor) |

**Phase B — ONLY if all gates pass (do not spend without Gate 3 pass): ~$45–140K**
| Item | Cost |
|---|---|
| Off-the-shelf **pre-certified** sensor nodes (buy, don't design) — pilot qty | $8–20K |
| Cloud/dashboard build (Hooman's wheelhouse; his time) | ~$0 cash |
| FTO / IP legal check | $5K |
| FCC/CE — AVOID by reselling certified modules; if forced, per SKU | $10–30K |
| Enclosure/mounting (off-the-shelf, no custom tooling) | $3–8K |
| Initial inventory (50–100 nodes) | $10–40K |
| Field/RMA/support buffer, insurance | $10–30K |
| **Phase B total** | **~$45–140K** (fits the $25–150K ceiling, hard-stop at $150K) |

**Do NOT enter Phase B unless the kill-test passes.** Base-case: you never spend Phase B money.

---

## 5. Delegation to keep it part-time

Honest truth from the red-team: **this load is largely non-delegable**, which is itself a reason
to pass. What little CAN be offloaded:
- **Lead-list building & cold-outreach sequencing** → VA / Apollo/Instantly automation.
- **Cloud/dashboard/ML** → Hooman's strength; AI-assisted, mostly delegable to Claude/Cursor.
- **Audit report generation** → templated / scripted.
What CANNOT be delegated and eats his 10–20 hrs/wk: field installs, firmware/RF debugging (if he
foolishly builds hardware), RMA logistics, and the industrial cold sales calls. If Phase B ever
starts, contract-manufacture and white-label the hardware so he never touches PCB/RF — otherwise
this is unbounded evening soldering and the part-time constraint breaks.

---

## 6. Go/No-Go gates (summary)

| Gate | Week | Pass bar | Most-likely reality |
|---|---|---|---|
| 0 — Addressable list | 2 | ≥100 non-OEM, non-free-audit plants | Hard to hit |
| 1 — Problem interviews | 4 | ≥15 interviews; <⅓ say "we get it free" | Likely fails (free substitute) |
| 2 — Paid audit WTP | 6 | ≥2 plants pay a real invoice | Coin-flip |
| 3 — Recurring WTP | 9 | ≥3 commit to $200/mo ongoing | **Most likely fails (front-loaded value)** |
| 4 — Non-HW-company path | 11 | Can resell certified nodes + software only | If no → confirm PASS |

**Default outcome per red-team: NO-GO at Gate 1 or Gate 3.** Total spend to reach that
conclusion: **under $1,500** — cheaper than one wrong PCB run.

---

## 7. Cheapest validation before spending real money (the one thing to actually do)

If Hooman insists on touching this at all, do ONLY **Weeks 1–6** ($1,500, ~3–4 weekends):
build the target list, do ~15 interviews, and try to sell **2–3 paid manual audits with a rented
detector.** That single experiment tests the two claims the whole venture rests on — "the slice
exists" and "someone will pay instead of taking the free audit" — for the price of a detector
rental, with zero hardware risk. If either fails (expected), the PASS verdict is confirmed with
data and he's out ~$1.5K and a few weekends instead of $50–150K and 18 months.

**Bottom line: recommend PASS. Prefer a pure-software candidate. If tempted, run the $1,500
6-week kill-test and let it kill the idea for you.**
