# Cycle 098 Report — Locksmith Key-Plant (1/3): The Facility Keying Database vs. ProMaster/InstaKey

**Date**: 2026-07-09. **Round**: 4. **Domain**: #12 Locksmith Master-Key "key plant".
**Cycle focus**: the core thesis — commercial locksmiths maintain proprietary master-key bitting
systems + key-issuance ledgers still kept in binders/spreadsheets; digitize the keying system and
own the **per-facility key plant** (high switching-cost account lock-in).
**Kill-risk to clear FIRST**: market too small / already DIY-satisfied — InstaKey, ProMaster Key
Manager, MasterKing, Excel. Verify enough commercial locksmiths pay a SaaS ACV to clear SAM > $100M.

---

## Step 1: Candidate Angles (5)

1. **KeyPlant (locksmith-side)** — master-keying design + bitting-chart generation + per-facility
   key-issuance ledger; the locksmith's book of accounts. TRL 8.
2. **Facility-side key management** — track who holds which key, authorizations, lost-key rekey
   planning (the customer/facility user). TRL 8.
3. **Rekey-planning optimizer** — compute minimal pin changes on a lost-key event. TRL 8.
4. **Key-authorization / duplication-control workflow** — signed key-request approvals. TRL 8.
5. **Master-key math engine** — generate legitimate bitting arrays under a top master key. TRL 8.

**Step 1: 5 PROMOTED.**

---

## Step 2: MANDATORY Incumbent Check — the space is already occupied

- **ProMaster Key Manager 8 (VERIFIED, WH Software):** a mature, dedicated product doing EXACTLY
  angles #1/#2/#4 — master-key system management, **key-issuance/return records**, multi-level
  security access, and a **locksmith↔facility split**: "ProMaster **Master-Keying 8**" (the
  locksmith designs the system) exports into "ProMaster **Key Manager 8**" (the facility manages
  holders + orders more keys back through the locksmith). Basic + Premium tiers. This is the exact
  product the thesis proposes — already built and sold, with the locksmith-to-customer data handoff.
- **InstaKey / SecurityRecords.com (VERIFIED, instakey.com):** a **cloud SaaS** ("over 1,200 cloud
  users") doing facility-side key-holder accountability + restricted-keyway + managed rekey for
  national chains (Comcast, Macy's, Whole Foods, T-Mobile, North Face, public housing). Owns the
  enterprise/multi-site segment outright.
- **Others (ASSUMED, well-known niche tools):** Medeco KeyMark / Simple-K, HPC KeyWizard, MasterKing,
  Instacode/Blackbox for code management — the master-keying math + charting niche has multiple
  entrenched tools. Plus Excel is "good enough" for many small shops.

**Competitive density: 5/5.** A dedicated, mature product (ProMaster) already ships the locksmith
key plant; a funded SaaS (InstaKey) owns the enterprise segment.

**Moat gate:** the per-facility keying DB is a real high-switching-cost asset — **but it already
accrues to ProMaster/InstaKey**, not to a new entrant. There is no un-owned data flywheel left for
the founder to accumulate; the incumbents have been accumulating it for 20+ years. Moat gate FAILS
(the moat exists but is already taken).

**Step 2: ALL REJECTED.**

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|----|----------|----------|
| Step 1 | 5 | 5 | 0 |
| Step 2 | 5 | 0 | 5 |

**Graduates: 0.** The named kill-risk is confirmed on the incumbent axis: ProMaster Key Manager is
the exact proposed product (locksmith-side + facility-side split, issuance ledger), and InstaKey
owns enterprise as a cloud SaaS. SAM axis tested in 099.
</content>
