# Cycle 062 Report — ROUND 4 (Domain #3: Water-Well "Well Plant" — adjacent subsurface-logging trades)

**Date:** 2026-07-09
**Domain assigned:** Adjacent MANDATED subsurface-logging trades where the operator uniquely
accumulates local subsurface data — geotechnical/environmental drilling, monitoring wells,
soil/geotech boring, dewatering. (Widening from cycle 061's finding that water-well logs are
open public data.)
**Agent:** Claude (Opus 4.8, 1M ctx). Full funnel + 4 Round-4 gates.

> **Tooling note.** WebSearch unavailable; search engines CAPTCHA/403-blocked. Direct fetches
> of Bentley/OpenGround, GAEA, and Jan-2026 domain knowledge. VERIFIED/ASSUMED marked.

---

## TL;DR (honest outcome)

**GRADUATES: 0.** Cycle 061 killed the water-well plant because states publish the logs.
This cycle tested the natural hop: **geotechnical & environmental drilling** (soil borings,
monitoring wells, CPT), where subsurface logs are NOT uniformly state-published — hoping the
driller could privately accumulate the plant. It fails on a **different** but equally fatal
moat problem: in geotech/enviro, **the drilling contractor does NOT own the subsurface data —
the geotechnical consultant / engineer-of-record owns it**, and that data is delivered to the
project client. The party that accumulates the log (the consultant) is exactly who a big
incumbent (**Bentley OpenGround**, formerly Keynetix/HoleBASE, VERIFIED) already serves as an
**enterprise SoR with cross-team sharing.** So either (a) the founder targets the driller, who
doesn't keep the data, or (b) targets the consultant, who is owned by Bentley. Neither yields a
founder-accruing flywheel. Plus the buyer skews toward engineering firms / DOTs / federal
agencies (procurement-heavy, the instant-reject buyer).

---

## Step 1 — Ten ideas scanned

| # | Idea | One-line | Verdict |
|---|------|----------|---------|
| 1 | Geotech boring-log field app for drillers | Digitize soil boring logs in the field | REJECT (Step 2 — data → consultant) |
| 2 | Environmental monitoring-well "plant" | Accumulate MW logs across sites | REJECT (Step 2 — consultant/client owns) |
| 3 | CPT (cone-penetration) data platform | Manage/interpret CPT soundings | REJECT (Step 2 — OEM Geotech/Vertek own it) |
| 4 | Geotech subsurface-data aggregator | Cross-project borehole plant for a region | REJECT (Step 2 — Bentley OpenGround) |
| 5 | Borehole-log generation software | AGS-format logs & reports | REJECT (Step 2 — gINT/OpenGround/GAEA) |
| 6 | Dewatering-well design/monitoring | Construction dewatering telemetry | REJECT (Step 3 — tiny, project-based) |
| 7 | Geothermal-loop borehole-log plant | (deferred to cycle 063) | DEFER |
| 8 | Foundation-pile install logging | Pile-driving records for contractors | REJECT (Step 2 — Pile Dynamics/PDA own) |
| 9 | Enviro drilling compliance recordkeeping | Track MW sampling/abandonment compliance | REJECT (Step 2 — LIMS/consultant) |
| 10 | Driller rig-telemetry (geotech) | ROP/torque flywheel for geotech rigs | REJECT (Step 3 — same SAM problem as 061 #8) |

---

## Step 2 — Incumbent/OEM check + Moat gate

- **Bentley OpenGround (VERIFIED, bentley.com):** "secure, enterprise-grade geotechnical data
  management and reporting," cloud, serves **engineering consultants, DOTs, and federal
  agencies**; borehole logging, lab data, mobile field capture, GIS, Civil3D integration.
  Formerly Keynetix / HoleBASE — **Bentley acquired the category leader.** This is the entrenched
  incumbent for ideas #1–#5.
- **gINT** (Bentley) and **GAEA WinLoG/WinCore** (VERIFIED via search) — established borehole-log
  software. **LogPlot** (RockWare) also. The borehole-log-generation niche is mature and owned.
- **The decisive moat fact:** in geotech/enviro, the **geotechnical consultant / engineer-of-
  record owns and stamps the subsurface data**, and delivers it to the project client. The
  **drilling contractor is a sub** who hands the core samples/field notes to the consultant and
  does not retain a proprietary regional plant. So the party who *accumulates* is the consultant
  — already an OpenGround customer — and the party the founder could reach cheaply (the driller)
  **does not keep the asset.** The flywheel accrues to Bentley's customer, not to a new founder.
- **Moat-gate verdict on #1–#5, #8, #9: REJECT.** Either data-owner is owned by Bentley, or the
  reachable buyer doesn't accumulate the data. No founder-accruing flywheel exists.
- **#3 CPT:** OEMs (Vertek/ARA, Geotech AB, Pagani) ship acquisition+interpretation software
  with the cone rigs — device-OEM-owns-the-feed pattern. REJECT.
- **#8 pile logging:** Pile Dynamics (PDA/PDI) owns dynamic pile testing + data. REJECT.

---

## Step 3 — Market/SAM (the two that reached it)

- **#6 dewatering & #10 geotech rig-telemetry:** both are project-based, tiny reachable buyer
  universes (a few thousand geotech/enviro drilling firms nationally), and any own-data angle is
  operational telemetry with the same **SAM ≪ $100M** ceiling that sank cycle 061's idea #8.
  The buyer for the data product (consultant/DOT/federal) is a **procurement-heavy instant-
  reject buyer.** REJECT.

---

## Step 4–5

No idea survived Step 2's moat gate to warrant a feasibility/execution pass.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|----|----------|----------|
| Step 1 | 10 | (0 to Step 4) | 9 + 1 deferred |
| Step 2 | 9 | 2→S3 | 7 |
| Step 3 | 2 | 0 | 2 |

**Graduates this cycle: 0 (honest zero).**

**Domain read:** the geotech/enviro adjacency **inverts the founder-fit worse than water-well
itself.** The subsurface data is owned by the licensed consultant (not the driller), that
consultant is already an enterprise customer of a large incumbent (Bentley OpenGround), and the
end-buyer is a procurement-heavy engineering firm / DOT / federal agency (instant-reject). The
"driller uniquely accumulates local subsurface data" premise **does not hold in geotech** — it
was specific to *water*-well drillers filing their own completion logs, and even there the
state re-publishes them (cycle 061). No defensible #2 here.
