# Cycle 045 Report — ROUND 3 (Wider Net)

**Date:** 2026-07-01
**Assigned domain:** Climate & energy SOFTWARE (grid/DER analytics, carbon accounting, VPP
orchestration, energy-trading tools, building energy optimization). Software, explicitly NOT
hardware.
**Founder:** Hooman — Adobe eng manager, strong AI/ML + software + cloud, EE bachelor's,
already building CutLog. Wants a defensible, low-capital, solo-buildable pure-software #2.

**Verdict up front: ZERO graduates.** This is an honest negative result. Climate/energy
software is one of the most capital-flooded, incumbent-dense B2B software domains in existence.
Every subdomain scanned is either (a) owned by a utility/OEM/ERP giant (Schneider, Siemens,
GE Vernova, ABB, Honeywell, SAP, Oracle, Tesla), (b) already contested by well-funded pure-play
startups ($20M–$100M+ raised), or (c) a genuinely open micro-niche whose defensible asset is
proprietary grid/market data a solo founder cannot acquire — i.e. the moat inverts against the
founder. No idea cleared the Round-3 Incumbent/OEM Check + Moat Gate.

---

## Methodology note on sourcing

Generic search engines (DuckDuckGo, Google, Bing, Brave, Ecosia, Startpage) all CAPTCHA- or
429-blocked automated queries this session. I fell back to sources that render for WebFetch:
Wikipedia, Mordor Intelligence market reports, MarketsandMarkets, and live company sites.
Market-size / CAGR figures below are VERIFIED against those pages (cited). Competitor funding
figures are marked ASSUMED where I could not open a primary funding source this session
(Crunchbase/PitchBook are historically blocked for this project per LEARNINGS.md #18); they
reflect widely-reported rounds and are directionally reliable for the go/no-go call. The
go/no-go conclusions do NOT hinge on exact funding numbers — they hinge on the *existence* of
funded incumbents, which is verified.

---

## Step 1 — Ten technologies / ideas scanned

| # | Idea (subdomain) | Enabling "breakthrough" 2025-26 | TRL | Step-1 decision |
|---|------------------|-------------------------------|-----|-----------------|
| 1 | Grid interconnection-queue automation (power-flow study software) | FERC Order 2023 cluster-study reform + fast load-flow solvers | 8 | PROMOTE to Step 2 |
| 2 | DER management systems / DERMS | FERC 2222 DER wholesale participation; AI grid optimization | 9 | PROMOTE |
| 3 | VPP orchestration | Cheap batteries ($139/kWh), wholesale-market opening | 9 | PROMOTE |
| 4 | Battery-storage energy-trading / bidding optimization | RL/forecasting for merchant storage arbitrage | 8 | PROMOTE |
| 5 | Carbon accounting / emissions SaaS | CSRD + (proposed) SEC climate disclosure mandates | 9 | PROMOTE |
| 6 | Building energy optimization / grid-interactive buildings | OpenADR 3.0, AI HVAC control, 2026 building codes | 9 | PROMOTE |
| 7 | Load / renewable-generation forecasting AI | Transformer/foundation models for time-series | 8 | PROMOTE |
| 8 | Utility vegetation / grid-asset analytics (satellite/LiDAR CV) | Cheap high-cadence satellite + CV | 8 | REJECT at Step 1 — this is CV-on-imagery industrial-QC archetype (Round-1/2 mined vein); AI4 (AiDash) already IPO-scale |
| 9 | 24/7 CFE / hourly EAC (granular certificate) matching | EnergyTag standard + data-center hourly-CFE demand | 7 | PROMOTE (most genuinely "new") |
| 10 | Home electrification / heat-pump / EV-charging optimization | IRA incentives, smart-charging APIs | 8 | PROMOTE |

Ideas 1–7, 9, 10 promoted to the competitive/moat gate. Idea 8 rejected at Step 1 as a
re-tread of the saturated CV-inspection archetype the round-3 directive explicitly bans.

---

## Step 2 — Competitive density + MANDATORY Incumbent/OEM Check + Moat Gate

### (1) Interconnection-queue automation — DENSITY 4, MOAT FAIL → REJECT
- **Scale of pain (VERIFIED):** US interconnection queues hold >2,600 GW (LBNL); waits 3–5 yrs.
  Real problem. FERC Order 2023 forces cluster studies → demand for faster study software.
- **Incumbent/OEM check:** ISOs/RTOs run the studies on PSS/E, PowerWorld, PSCAD (Siemens PTI,
  Hitachi Energy). **Pearl Street Technologies** (SUGAR power-flow engine, DOE/utility-backed),
  **Nira Energy** (developer-side hosting-capacity/queue screening), **Gridcog** (multi-market
  project modeling — customers Shell, TotalEnergies, AGL, PwC, EY [VERIFIED, gridcog.com]),
  **Tyba, Pearl Street, Aurora**-adjacent players. The buyers are ISOs (12–24 mo procurement,
  government-adjacent) or utilities.
- **Moat gate:** The defensible asset is a validated power-system model of a specific grid —
  utility/ISO proprietary data a solo founder cannot legally acquire. The hard part is
  power-systems engineering (load-flow / short-circuit / stability), not a software UI. This
  INVERTS the founder's strengths (EE bachelor's ≠ power-systems specialist). **FAIL.**

### (2) DERMS — DENSITY 5 → REJECT
- **Market (VERIFIED, Mordor):** $1.42B (2025) → $3.29B (2030), **18.31% CAGR**.
- **Incumbent check:** Dominated by **Engie, GE (Vernova), Siemens, Schneider Electric, ABB**
  (Mordor names these five as market leaders). Plus AutoGrid (acq. by Uplight/Schneider),
  Itron, Smarter Grid Solutions (GE), Opus One (GE). Utility buyer, multi-year sales cycle.
- **Moat gate:** Utility integration + certification lock-in accrues to the incumbents, not a
  newcomer. **FAIL** — "Big tech/incumbents actively building" = density 5, auto-reject.

### (3) VPP orchestration — DENSITY 5 → REJECT
- **Market (VERIFIED, Mordor):** $5.01B (2026) → $16.61B (2031), **27.08% CAGR** (attractive
  growth) — but top 8 players hold ~40% share.
- **Incumbent check (VERIFIED, Mordor + Wikipedia):** **Tesla (Autobidder), Siemens, Schneider,
  Enel X, GE, Sunrun, ABB, Next Kraftwerke, Octopus/Kraken, AutoGrid.** OEMs that own the
  batteries/inverters own the fleet and give orchestration away to sell hardware.
- **Moat gate:** Requires an aggregated fleet of assets = a cold-start network effect owned by
  whoever owns the hardware relationship. A solo software founder has no assets to orchestrate.
  **FAIL.**

### (4) Battery-storage trading / bidding optimization — DENSITY 4, MOAT FAIL → REJECT
- **Incumbent check:** **Tesla Autobidder, Fluence (Mosaic bidding software), Gridmatic
  (~$100M+ raised, ML power trading), Habitat Energy (acq. by Quinbrook), Modo Energy
  (storage-market analytics), Tyba, Enspired, Entrix (targeting 1 GW by 2026, VERIFIED
  Wikipedia).** Very crowded with funded specialists.
- **Moat gate:** Alpha in energy trading = proprietary forecast + market-microstructure data +
  a book to trade. A solo founder has no trading book and no proprietary market data; the model
  is only as good as data he cannot uniquely get. **FAIL.**

### (5) Carbon accounting SaaS — DENSITY 5 → REJECT
- **Market (VERIFIED, MarketsandMarkets, Mar 2025):** carbon accounting sits inside green-tech &
  sustainability, ~$73.9B by 2030 at **23.7% CAGR**. Growth is real; competition is brutal.
- **Incumbent check (VERIFIED, MarketsandMarkets):** **SAP, Schneider, IBM, GE, Siemens** (ERP
  giants) + pure-plays **Watershed (~$100M+ raised, ~$1.8B val ASSUMED), Persefoni (~$100M+),
  Normative, Greenly, Sweep, Sustain.Life, Clarity AI, IsoMetrix.** One of the most VC-saturated
  climate-software categories of the decade.
- **Moat gate:** Emission-factor databases + auditor relationships + regulatory-form templates.
  Nothing a solo founder can uniquely own; incumbents already have the auditor/ERP channel.
  **FAIL.**

### (6) Building energy optimization / EMS — DENSITY 5 → REJECT
- **Market (VERIFIED, Mordor):** EMS $63.64B (2025) → $150.83B (2031), **15.48% CAGR**; software
  is 50.7% of it; Building-EMS is 45.6% of the market.
- **Incumbent check (VERIFIED, Mordor):** **Schneider, Siemens, ABB, Honeywell, GE, Eaton,
  Rockwell, Johnson Controls, IBM, Oracle** — the entire building-automation oligopoly. Plus
  funded startups (BrainBox AI [merged/scaled], 75F, Verdigris, Carbon Lighthouse [shut down]).
- **Moat gate:** Requires BMS/BACnet integration and installed-base access owned by the controls
  incumbents. **FAIL.**

### (7) Load / renewable forecasting AI — DENSITY 4, MOAT FAIL → REJECT
- **Incumbent check:** **DNV, Vaisala, Solcast (acq. DNV), Amperon (~$20M+ raised), Nnergix,
  Fluence Nispera, Kraken, Origami, Amperon, Utilidata.** Weather-forecasting incumbents
  (Tomorrow.io, DTN) plus every ISO's internal models.
- **Moat gate:** Accuracy depends on proprietary meter/SCADA/weather data feeds. Foundation
  time-series models are now commoditized (open weights). Nothing defensible for a solo builder.
  **FAIL.**

### (8) Vegetation / grid-asset CV analytics — REJECTED at Step 1 (banned archetype)
- **AiDash (~$180M+ raised), Overstory, Sharper Shape, LiveEO** already dominate; and this is
  the CV-on-imagery inspection archetype the round-3 directive explicitly excludes.

### (9) 24/7 CFE / hourly granular-EAC matching — DENSITY 3–4, MOAT FAIL → REJECT
- **The most genuinely "new" niche** (EnergyTag standard is <5 yrs old; data-center hourly-CFE
  demand is a real 2025-26 tailwind — Google, Microsoft, Digital Realty pushing it).
- **Incumbent check (VERIFIED, energytag.org + granular-energy.com):** **Granular Energy**
  (B-Corp, SOC 2 Type II, EnergyTag-accredited, sells hourly-matched EAC software to suppliers),
  **FlexiDAO** (24/7 CFE tracking, customers incl. Google/Microsoft/Iberdrola), **LevelTen
  Energy** (~$100M+ raised, PPA marketplace + matching), **Flexcharging, Singularity Energy,
  M-RETS** (registry). EnergyTag case studies name ENGIE, Google, KEPCO, Digital Realty as
  adopters — meaning the big buyers already have vendors.
- **Moat gate:** The value is a certificate registry / trusted-ledger network effect + grid
  hourly-emissions data (Singularity, WattTime, Electricity Maps already own the data layer).
  A solo founder cannot bootstrap registry trust or the emissions-data asset. **FAIL** — the
  niche is small AND its moat is a network/registry someone else is already building.

### (10) Home electrification / heat-pump / EV-charge optimization — DENSITY 4, MOAT FAIL → REJECT
- **Incumbent check:** **Tesla, Enphase, SolarEdge, Span, chargeHQ, Optiwatt, ev.energy
  (~$30M+), WeaveGrid (~$60M+), Optiwatt, Renew Home (Google Nest + OhmConnect merger, huge).**
  OEMs (Tesla, Enphase) own the device APIs and app relationship.
- **Moat gate:** Requires OEM device-API access and a utility-program contract; both accrue to
  hardware OEMs and utility-partnered platforms. Consumer app with no data moat. **FAIL.**

---

## Step 3 — Market sizing (only relevant for anything that had survived; none did)

Growth rates are NOT the problem here — most of these markets grow 15–27% CAGR (VERIFIED
above), comfortably clearing the >15% bar. **The killer is uniformly Step 2: density 4–5 and a
moat that structurally belongs to hardware OEMs, utilities, ERP giants, or data-registry
owners — never to a solo software founder.** Size and growth are the least-discriminating
dimensions here, exactly as LEARNINGS.md predicted.

---

## Step 4 — Feasibility (n/a; nothing reached it)

No idea cleared Step 2's moat gate, so none proceeded to feasibility. Even on pure
founder-fit / capital, several would score well (pure software, cloud, $150–300K) — but per
the Round-2 meta-lesson, "cheap + well-fit + no moat = absorbable feature, not a company."

---

## Why this whole domain is a poor vein for THIS founder (the structural reason)

Climate/energy software has a recurring moat pattern that inverts Hooman's strengths:

1. **The defensible asset is proprietary GRID/MARKET/DEVICE data**, owned by utilities, ISOs,
   or hardware OEMs — none of which a solo founder can legally or practically acquire. (Contrast
   CutLog, where the data flywheel is *user-contributed* parameters the founder can bootstrap.)
2. **The buyer is a utility, ISO, or Fortune-500 sustainability office** — 12–24 month
   procurement, RFPs, pilots. No Facebook-group owner-operator channel; CutLog's distribution
   edge does not transfer.
3. **The category is a magnet for climate VC** — every attractive niche already has 3–10 funded
   pure-plays PLUS a Schneider/Siemens/GE/SAP incumbent. This is the opposite of an
   under-served, invisible niche.
4. **The genuinely-new niche (hourly CFE) is small and its moat is a registry/data network**
   already being built by Granular Energy, FlexiDAO, Singularity, and Electricity Maps.

This mirrors, in a new domain, exactly the Round-2 failure mode: the parts that are easy for a
software founder are commodities, and the parts that carry the moat (grid data, market access,
device APIs, hardware fleets) are the parts he can't get. A ZERO-graduate cycle is the correct,
honest call.

---

## Citations
- VPP market: Mordor Intelligence, "Virtual Power Plant Market" — $5.01B (2026) → $16.61B
  (2031), 27.08% CAGR; players Tesla Autobidder, Siemens, Schneider, Enel X, GE, Sunrun, ABB,
  Next Kraftwerke. (mordorintelligence.com)
- DERMS market: Mordor Intelligence, "DERMS Market" — $1.42B (2025) → $3.29B (2030), 18.31%
  CAGR; leaders Engie, GE, Siemens, Schneider, ABB. (mordorintelligence.com)
- EMS market: Mordor Intelligence, "Energy Management Systems Market" — $63.64B (2025) →
  $150.83B (2031), 15.48% CAGR; Schneider, Siemens, ABB, Honeywell, GE, Eaton, Rockwell, JCI,
  IBM, Oracle. (mordorintelligence.com)
- Carbon accounting: MarketsandMarkets green-tech & sustainability report (Mar 2025) — ~$73.9B
  by 2030, 23.7% CAGR; SAP, Schneider, IBM, GE, Siemens + Watershed, Clarity AI, Normative,
  Persefoni, IsoMetrix. (marketsandmarkets.com)
- VPP operators / Entrix 1 GW target / battery $139/kWh: Wikipedia "Virtual power plant."
- 24/7 CFE: energytag.org (standard, adopters ENGIE/Google/KEPCO/Digital Realty);
  granular-energy.com (product, B-Corp/SOC2/EnergyTag-accredited).
- Energy-project modeling: gridcog.com (customers Shell, TotalEnergies, AGL, PwC, EY, FRV, ACEN).
- Funding figures for Watershed/Persefoni/LevelTen/Gridmatic/WeaveGrid/AiDash/Amperon/ev.energy
  are ASSUMED (widely-reported rounds; Crunchbase blocked this session) — go/no-go does not
  depend on exact amounts, only on the verified *existence* of funded incumbents.
</content>
</invoke>
