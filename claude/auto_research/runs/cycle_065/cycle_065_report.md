# Cycle 065 Report — ROUND 4 (Domain #12 STRETCH: Locksmith Master-Key "Key Plant")

**Date:** 2026-07-09
**Domain assigned:** 5th-cycle stretch (water-well core saturated by cycle 064). Domain #12 in
the round-4 map: commercial locksmiths design/maintain **master-key bitting systems** for
facilities; the keying chart + issuance ledger = a private "key plant" (CutLog-class own-data
flywheel). Kill-risk per map: **market too small / DIY-satisfied** (InstaKey, MasterKing,
ProMaster Key Manager, Excel).
**Agent:** Claude (Opus 4.8, 1M ctx). Full funnel + 4 Round-4 gates.

> **Tooling note.** WebSearch unavailable; engines CAPTCHA/403. Direct fetches (whsoftware.com
> / ProMaster Key Manager, InstaKey) + Jan-2026 knowledge. VERIFIED/ASSUMED marked.

---

## TL;DR (honest outcome)

**GRADUATES: 0.** The locksmith key-plant has the cleanest **moat SHAPE** of any Round-4 domain
I touched — a per-facility keying database + issuance ledger with genuinely **high switching
cost** — but it fails on **two of the four gates simultaneously**, exactly as the map warned:

1. **Incumbent gate — FAIL.** The niche is already occupied by mature, purpose-built software.
   **ProMaster Key Manager + ProMaster Master-Keying 8** (WH Software, VERIFIED) already do
   master-key system design AND key-holder/issuance tracking AND locksmith↔facility data
   sharing. **InstaKey** (VERIFIED: >120K locations, >9M keys) sells an integrated hardware+
   software key-control program direct to national facilities. **BEST/dormakaba, Medeco, Instant
   Key Systems, MasterKing** round out a crowded field. This is not a paper-based greenfield —
   it's a served, decades-old category. Density 4.
2. **SAM gate — FAIL.** The buyer is commercial locksmiths (a countable, non-growing trade —
   low tens of thousands of locksmith businesses in the US, most tiny) OR facility end-users
   (fragmented, low per-seat WTP). Realistic reachable seats × SaaS ACV lands **far below $100M.**
   Same countable-micro-trade red flag that sank HVAC-TAB and cycle 061's well-telemetry idea.

3. **Moat gate — nominally PASS but MOOT.** The key-plant flywheel *would* accrue to the founder
   — but the incumbents already built it, and the switching-cost moat now protects THEM.

---

## Step 1 — Ten ideas scanned

| # | Idea | One-line | Verdict |
|---|------|----------|---------|
| 1 | Cloud master-key system designer + keying-chart plant | Design bitting systems; own the facility keying DB | REJECT (Step 2 — ProMaster/MasterKing) |
| 2 | Key-issuance / key-holder ledger SaaS | Track who holds which key, lost/returned | REJECT (Step 2 — ProMaster Key Manager) |
| 3 | Rekey-planning / expansion optimizer | Plan rekeys as facility grows | REJECT (Step 2 — feature of #1) |
| 4 | Locksmith field-service / job mgmt | Dispatch/invoicing for locksmiths | REJECT (Step 2 — horizontal FSM) |
| 5 | Restricted-keyway / key-control-as-a-service | Managed key control for multi-site facilities | REJECT (Step 2 — InstaKey owns) |
| 6 | Facility keying "as-built" for property mgrs | Portable keying record across a portfolio | REJECT (Step 3 — small, PM-owned) |
| 7 | Digital-credential / access-control migration | Help facilities move mech→electronic keys | REJECT (Step 2 — ACaaS: Brivo/Verkada/Kisi) |
| 8 | Key-duplication authorization / audit trail | Authorize & log key cuts | REJECT (Step 2 — InstaKey/Medeco) |
| 9 | Locksmith parts/pinning calculator | Compute pinning charts from bitting | REJECT (Step 1 — free tools/apps exist) |
| 10 | Master-key security audit / bitting-conflict checker | Detect cross-keying/security errors | REJECT (Step 2 — ProMaster MK8 does it) |

---

## Step 2 — Incumbent/OEM + Moat gate

- **ProMaster Key Manager (WH Software, VERIFIED via whsoftware.com):** tracks keys, key
  hierarchy, doors, keying matrix, key issue/return, lost/broken/overdue keys, key orders,
  reports; permissions/roles; **integrates with ProMaster Master-Keying 8 for locksmith
  coordination**; sold to **both locksmiths (who can share system data) and end-facilities.**
  This single product family occupies ideas #1, #2, #3, #10. Desktop-first (a mild cloud gap —
  the only visible wedge, and a thin one).
- **InstaKey (VERIFIED via instakey.com):** integrated rekeyable-hardware + cloud key-management
  "Key Control Program"; **>120K locations installed, >9M keys in use**; clients incl. Whole
  Foods, Macy's, North Face, Comcast, housing authorities. Owns the managed-key-control-as-a-
  service model (ideas #5, #8).
- **Others (ASSUMED, domain knowledge):** MasterKing, Instant Key Systems, BEST/dormakaba,
  Medeco, plus Excel/paper at the low end. Access-control-as-a-service (Brivo, Verkada, Kisi,
  Kisi) is aggressively converting facilities OFF mechanical master-key systems (idea #7 is
  their turf and a structural headwind to the whole domain).
- **Moat-gate verdict:** the key-plant flywheel is real and high-switching-cost — **but the
  incumbents already own it.** A new founder's only differentiation is "modern cloud UI on
  ProMaster," which is a UI refresh, not a data moat that accrues to the newcomer. Density 4.
  REJECT ideas #1–#3, #5, #7, #8, #10.

---

## Step 3 — Market/SAM (the two that reached it)

- **#4 locksmith FSM, #6 facility keying as-built:** buyer universe is small (US locksmith
  businesses number in the low tens of thousands, mostly 1–3 person shops, flat/declining as
  mechanical locks give way to electronic access control). Even at optimistic penetration ×
  $50–150/mo, reachable SAM is **well under $100M**, and horizontal FSM (Jobber/Housecall Pro)
  already serves #4. Structural headwind: the whole mechanical-keying market is being eroded by
  electronic access control. REJECT on SAM + declining trajectory.

---

## Step 4–5

No idea cleared the incumbent + SAM gates. No feasibility/execution pass warranted.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|----|----------|----------|
| Step 1 | 10 | 0 | 10 |

**Graduates this cycle: 0 (honest zero).**

**Domain read:** the locksmith key-plant is the textbook illustration of the map's kill-risk —
**cleanest moat SHAPE, but already built and too small.** ProMaster (design + issuance ledger +
locksmith↔facility sharing) and InstaKey (managed key control, 120K+ locations) already occupy
the exact key-plant flywheel, so the switching-cost moat now defends the incumbents, not a
newcomer whose only edge is a cloud UI. The buyer is a countable, flat-to-declining trade
(mechanical keying is being displaced by electronic access control), so SAM can't clear $100M.
Not a defensible #2.
