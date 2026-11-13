# Cycle 087 Report — Adjacent angle: DOT propane cylinder requalification & the cylinder-exchange fleet

**Date**: 2026-07-09
**Domain (Round-4 map #9, adjacent probe)**: Rather than the on-delivery gas check (killed in
cycle 086), this cycle tests the **DOT-cylinder side** of propane: portable cylinders (BBQ/
forklift/exchange) must be **requalified on a 5-yr or 12-yr cycle** and marked; the cylinder-
exchange business (Blue Rhino / AmeriGas cages, plus thousands of independent refillers) runs a
fleet of assets that each carry a legal requalification clock. Thesis-under-test: a founder could
own the **per-cylinder requalification + refill-inspection history** for independent refillers.

**Gates applied**: incumbent/OEM (P3, Tank Spotter, RegO, exchange-network apps), moat (does
cylinder history accrue to founder or to the exchange network / requalifier / ERP), SAM, buyer.

---

## Step 1: Technology Discovery (10 candidates)

### 1. Per-cylinder DOT requalification tracker (5-yr/12-yr clock) for independent refillers
- **Domain**: Propane cylinder compliance
- **Breakthrough**: QR/serial + mobile scan builds a per-cylinder requalification + visual-
  inspection ledger; alerts before the legal clock expires.
- **TRL**: 9 (shipping software category)
- **Status**: **REJECTED (Step 1)** — **P3 explicitly markets "DOT 5-year requalification"
  tracking** [Brave — VERIFIED]; a "RIN Locator App" already exists for finding DOT-registered
  requalification facilities [Brave — VERIFIED]. Not new tech, not empty.

### 2. Cylinder-exchange cage IoT + turn/inspection analytics
- **Breakthrough**: Sensor cages report stock/turns; couple with inspection logging.
- **TRL**: 7
- **Status**: **REJECTED (Step 1)** — cylinder exchange is **near-monopolized by Blue Rhino
  (Ferrellgas) and AmeriGas cages**; the buyer is two MLPs, not a fragmented private operator.
  Fails Gate 4 (buyer) on its face.

### 3. Forklift-cylinder fleet compliance for industrial gas / forklift dealers
- **Breakthrough**: Track forklift LPG cylinder requalification + monthly inspection for material-
  handling fleets.
- **TRL**: 8
- **Status**: PROMOTED (to test) — different buyer (forklift dealers / warehouses); test whether
  it's unowned.

### 4. AI valve/collar corrosion grader from a cylinder photo
- **Breakthrough**: Vision model flags condemn-worthy corrosion/dents at refill (the "requalify or
  condemn" decision).
- **TRL**: 6
- **Status**: PROMOTED (to test) — a genuine AI wedge; test moat + hard-part.

### 5. Refill-station overfill / OPD-valve compliance logger
- **Breakthrough**: Log OPD-valve presence + fill %; auto-doc the refill safety check.
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — feature inside P3/Tank Spotter's field-inspection modules;
  absorbable, no standalone flywheel.

### 6. Requalifier (RIN-holder) shop workflow SoR
- **Breakthrough**: Workflow + certificate generation for the DOT-registered requalification shop.
- **TRL**: 8
- **Status**: PROMOTED (to test) — the requalifier shop is a distinct (small) buyer; test SAM.

### 7. Cylinder-serialization + blockchain chain-of-custody
- **Breakthrough**: Immutable per-cylinder custody ledger across refill/exchange.
- **TRL**: 5
- **Status**: **REJECTED (Step 1)** — solution-looking-for-a-problem; no buyer pain that a serial
  number + DB doesn't solve; blockchain adds nothing. Fails moat/utility.

### 8. Propane autogas (fleet vehicle) tank inspection tracker
- **Breakthrough**: Track requalification/inspection for LPG-powered vehicle fuel tanks.
- **TRL**: 8
- **Status**: **REJECTED (Step 1)** — autogas is a tiny, shrinking US niche; buyer universe far too
  small; also overlaps fleet-maintenance software.

### 9. Home-improvement/hardware retailer cylinder-recall & age compliance
- **Breakthrough**: Retail-shelf cylinder age/recall management.
- **TRL**: 7
- **Status**: **REJECTED (Step 1)** — buyer = big-box retail + Blue Rhino; concentrated, not
  fragmented-private.

### 10. Combined "asset compliance" register across cylinders + bulk tanks for a dealer
- **Breakthrough**: One register for every regulated asset a dealer touches.
- **TRL**: 9
- **Status**: **REJECTED (Step 1)** — this is literally P3's "tank management + DOT cylinder"
  product. Direct incumbent.

**Step 1 result: 3 promoted (#3, #4, #6), 7 rejected.**

---

## Step 2: Competitive Analysis + MANDATORY Incumbent/OEM Check

| Candidate | OEM / dedicated incumbent | ERP/fleet bundle | Density | Verdict |
|---|---|---|---|---|
| #3 Forklift-cylinder fleet compliance | Forklift OEMs (Toyota, Hyster) + EAM/CMMS (UpKeep, Fiix) manage forklift PM incl. LPG cylinders; safety-inspection apps (SafetyCulture/iAuditor) template it | warehouse EAM owns asset history | **4** | REJECT |
| #4 AI cylinder-corrosion grader | requalification is a *manual visual + hydro/proof test* per DOT — the AI photo grade is advisory, doesn't replace the mandated test; RegO/test-kit OEMs adjacent | — | **3** (thin) | BORDERLINE → carry |
| #6 Requalifier shop SoR | P3-class + generic field/shop software; RIN-holder shops number only a few thousand | — | **3–4** | REJECT on SAM (Step 3) |

**Findings:**
- The cylinder-requalification data asset **accrues to whoever owns the requalifier's cert
  system or the dealer's compliance SoR (P3)** — not to a new founder. P3 already markets the
  5-yr requalification tracker.
- #4 (AI corrosion grader) is the only candidate with a non-obvious wedge. But per the round-3
  hidden-hard-part check: the *mandated* action is a physical visual/proof-pressure test by a
  RIN-holder — the AI photo is a nice-to-have that **cannot be the system of record** and drives
  no compliance flywheel the incumbent lacks. Carry to Step 3 only to size it honestly.

**Step 2 result: 1 borderline (#4), 2 rejected.**

---

## Step 3: Market Analysis (candidate #4 — AI cylinder-corrosion grader)

- **Buyer (Gate 4)**: refill-station operators / requalifiers. Fragmented-private-ish, but the
  large-volume cylinder work is concentrated in **Blue Rhino (Ferrellgas) + AmeriGas** exchange
  networks — the reachable *independent* refiller slice is a subset of the ~2,000 NPGA
  independents from cycle 086.
- **SAM**: Even generously — 2,000 independents × $1–3K/yr for an add-on grader = **$2–6M**.
  A standalone AI-photo feature commands *less* ACV than a full compliance SoR, not more. **FAILS
  >$100M by ~20×.** [ASSUMED ACV; VERIFIED small seat count]
- **Moat**: the corrosion-grading model is trainable by anyone with cylinder photos, including P3;
  no proprietary-data lock-in accrues uniquely to the founder. **Moat gate FAIL.**
- **Growth**: cylinder-exchange volume is flat/mature; no >15% CAGR tailwind at the software layer.
- **Status**: **REJECTED (Step 3)** — SAM ~20× below threshold, moat accrues to incumbent, buyer
  slice concentrated. The AI wrapper is an absorbable feature, not a company.

**Step 3 result: 0 promoted.**

---

## Step 4 / Step 5

No candidate reached Step 4. **Zero execution plans.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 3 | 7 |
| Step 2 | 3 | 1 | 2 |
| Step 3 | 1 | 0 | 1 |
| Step 4 | 0 | 0 | — |
| Step 5 | 0 | 0 | — |

**Graduates this cycle: 0.**

**Honest read**: The DOT-cylinder side is, if anything, a **worse** founder bet than the bulk-tank
gas check:
- **Incumbent gate — FAIL.** P3 explicitly markets DOT 5-yr requalification tracking; a RIN Locator
  app exists; forklift-cylinder PM sits in warehouse EAM/CMMS and SafetyCulture templates.
- **Buyer gate — PARTIAL FAIL.** The high-volume cylinder economy (exchange cages) is a **Blue
  Rhino / AmeriGas duopoly**, not a fragmented private buyer. Only the residual independent-refiller
  slice is reachable, and it's the same ~2,000 companies already targeted by P3.
- **Moat gate — FAIL.** Nothing accrues uniquely to the founder; the only novel piece (AI corrosion
  grade) is a cloneable advisory feature that can't be the mandated system-of-record.
- **SAM gate — FAIL.** $2–6M, ~20× below $100M.

Second consecutive honest zero in this domain. One angle remains genuinely untested (the
cargo-tank/bobtail DOT inspection + fuel-oil-tank inspection side) — cycle 088.
