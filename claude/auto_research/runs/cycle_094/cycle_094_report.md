# Cycle 094 Report — Ag Drainage-Tile (1/4): The As-Built Capture Layer vs. RTK-OEM Clouds

**Date**: 2026-07-09. **Round**: 4. **Domain**: #11 Ag Drainage-Tile "as-built subsurface plant".
**Cycle focus**: the core thesis — drainage-tile contractors install buried tile with RTK/GPS and
should own a private **subsurface as-built map plant** that contractors/farmers pay to access
before digging or replacing tile. Test the capture layer.
**Kill-risk to clear FIRST**: RTK-OEM ecosystems (Trimble WM-Drainage, John Deere Operations Center,
Ag Leader Intellislope/AgFiniti, Soil-Max) already capture as-installed data into the OEM's/farmer's
free cloud — relocating the moat to the equipment OEM.

---

## Step 1: Candidate Angles (5)

1. **TileVault (capture)** — mobile/RTK-ingest app that records as-installed tile lines, depth,
   diameter, outlets during install; contractor's private map library across all jobs. TRL 8.
2. **Brand-agnostic import** — normalize as-builts from Trimble/JD/Ag Leader/Soil-Max exports into
   one contractor-owned records set. TRL 7.
3. **Pre-dig "tile locate"** — sell/serve the map back before excavation to avoid cutting existing
   tile (hard ROI). TRL 7.
4. **Repair/replacement bid accelerator** — historical map → faster, more accurate re-work quotes. TRL 8.
5. **Farmer-facing field tile atlas** — subscription for landowners to see their subsurface network. TRL 7.

**Step 1: 5 PROMOTED** (bias to action).

---

## Step 2: MANDATORY Incumbent / OEM Check

- **Ag Leader Intellislope → AgFiniti (VERIFIED, agleader.com):** tile install runs through
  InCommand displays + SMS/AgFiniti "accessible anywhere, anytime." The plan and install data land in
  **Ag Leader's cloud**. The page does not explicitly confirm as-built export/ownership terms
  (ASSUMED: farmer/operator-centric like the rest of AgFiniti).
- **Trimble WM-Drainage (ASSUMED — page 404'd; well-documented product):** grade-control + design;
  data flows into Trimble Ag / Farmer Core, a farmer-account cloud.
- **John Deere Operations Center (VERIFIED general):** the dominant farmer-owned cloud; any JD-guided
  tile operation logs to the **farmer's** Ops Center account, not the contractor's.
- **Soil-Max Flow-X (VERIFIED, soilmax.com):** tile-plan design app for self-tilers; part of the
  install-equipment ecosystem.

**The critical structural finding:** every OEM path deposits the as-built into a **farmer-account,
brand-siloed** cloud, free with the hardware. Two consequences:
- **For the farmer**, the as-built is already captured free (Ops Center / AgFiniti) → no willingness
  to pay a third party for angle #5.
- **BUT** these clouds are (a) **farmer-owned, not contractor-owned**, and (b) **brand-siloed** — a
  contractor who runs mixed fleets across dozens of farms has NO single, portable, cross-farm,
  cross-brand as-built library. That gap is real.

**Moat gate — nuanced:** the raw as-built accrues to the OEM/farmer cloud (kill-risk largely
CONFIRMED for the farmer-facing plays #5). The ONLY surviving moat is the **contractor's cross-farm,
brand-agnostic aggregate** (#1/#2/#4) — a private records asset no single OEM cloud holds because
each cloud is siloed by farmer + brand. This is a *thin* survivor, and it depends on contractors
being willing to route data OUT of the OEM cloud into the founder's platform.

**Step 2 verdict:** REJECT #3, #5 (OEM/farmer cloud already owns it; farmer won't pay).
**PROMOTE #1/#2/#4 as a single "contractor cross-farm as-built plant" candidate — CONDITIONAL**,
carried to 095 for the SAM/willingness-to-pay test (the binding question).

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|----|----------|----------|
| Step 1 | 5 | 5 | 0 |
| Step 2 | 5 | 1 (merged, conditional) | 4 |

**Graduates this cycle: 1 conditional** — "contractor-owned, brand-agnostic, cross-farm tile
as-built plant." Survives ONLY on the brand-silo gap; farmer-facing and pre-dig-locate angles die to
free OEM/farmer clouds. SAM test deferred to 095 (the likely kill).
</content>
