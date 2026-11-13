# 01 - Product Definition: High-Bandwidth CubeSat Communication Modules

## Problem Statement

CubeSat operators generating Earth observation data face a critical downlink bottleneck. Current standard patch antennas on 3U-6U CubeSats achieve only 1-10 Mbps downlink, while onboard imaging sensors generate 10-100 GB per day. With LEO passes of 8-12 minutes per ground station contact, operators can only downlink a fraction of collected data. This forces compromises: lower resolution imagery, fewer revisit captures, or expensive constellation-scale ground station networks.

The result: a $100K CubeSat with a $50K imaging payload produces data equivalent to a $500K satellite, but cannot get that data to the ground. The communication system is the binding constraint on mission value.

**Confidence: HIGH** - This problem is well-documented in CubeSat literature and confirmed by the 20%+ CAGR in CubeSat launches paired with consistent complaints about downlink capacity at conferences (SmallSat, IAC).

## Product Scope v1

**What it is**: A 3U-compatible deployable reflectarray antenna module with integrated Ka/X-band transceiver, achieving 20+ Mbps sustained downlink from LEO. The module uses origami-inspired folding patterns to achieve 25x area expansion from stowed to deployed state.

**Core specifications**:
- Stowed volume: 1.5U (15 x 10 x 10 cm)
- Deployed aperture: ~50 x 50 cm (25x expansion)
- Mass: <2 kg total (antenna + mechanism + transceiver)
- Frequency: Ka-band (26 GHz) primary, X-band (8.2 GHz) secondary
- Data rate: 20-50 Mbps sustained downlink (vs. 1-5 Mbps state of art for 3U)
- Power draw: <15W during transmission
- Interface: Standard PC/104 + CAN bus
- Deployment: Single-command, spring-loaded with SMA release

**What it does NOT do**:
- Not a full satellite bus or platform
- Not ground station hardware (integrates with existing ground networks: AWS Ground Station, KSAT, RBC Signals)
- Not inter-satellite links (downlink only for v1)
- Not custom one-off engineering (standardized product with 2-3 SKUs)

## User Workflow

1. **Procurement**: Customer selects module variant (Ka-band or X-band, 3U or 6U compatible) from catalog. Order placed, delivery in 8-12 weeks.
2. **Integration**: Customer's systems engineer mounts module to CubeSat bus using standard mechanical interface. Electrical connection via PC/104 connector. Software integration via documented CAN bus protocol and provided Linux driver.
3. **Pre-flight testing**: Customer runs provided deployment test sequence on bench. Module self-tests RF chain and reports health telemetry.
4. **Launch & commissioning**: After orbital insertion, ground operator sends deployment command. Module deploys antenna, runs self-calibration, reports pointing and RF status.
5. **Operations**: During ground station passes, satellite flight software activates downlink. Module handles modulation, power amplification, and antenna pointing (open-loop, based on known orbit + ground station location). Data streams at 20+ Mbps to standard Ka-band ground station.

## Pricing Model

| Tier | Product | Price | Target Customer |
|------|---------|-------|-----------------|
| Development unit | Engineering model (non-flight) | $50,000 | University labs, early prototyping |
| Flight unit | Single flight-qualified module | $120,000-$180,000 | Commercial CubeSat operators |
| Constellation | 10+ units | $90,000-$130,000/unit | Constellation operators |
| Data service (future) | Pay-per-GB with bundled ground | $5-15/GB | Operators wanting zero capex |

**Revenue model**: Hardware sales (Year 1-3), transitioning to hardware + recurring data service fees (Year 3+).

**Gross margin target**: 60-70% at scale (significant IP content, moderate BOM cost ~$25-35K at volume).

## Ideal First Customer

**Profile**: A funded (Series A+) Earth observation CubeSat company operating 3-10 satellites in LEO, currently limited by downlink. They have:
- Existing satellites with proven imaging payloads generating more data than they can downlink
- Next-generation satellites in design phase (12-18 month horizon) where they can specify our module
- Technical team capable of integration (not a customer needing hand-holding)
- Revenue or contracts that justify $120K+ per-satellite comm upgrade
- Frustration with current downlink (documented need, not hypothetical)

**Specific targets** (in priority order):
1. Planet Labs (next-gen SuperDove or Pelican buses) - largest commercial EO constellation
2. Spire Global (weather/maritime CubeSats, high data volume)
3. Capella Space (SAR data, massive downlink needs - already uses Tendeg on larger sats)
4. HawkEye 360 (RF geolocation, moderate data but growing)
5. Satellogic (sub-meter EO from small sats)

**Confidence: MEDIUM** - These companies are real and have the problem, but whether they would buy from an unproven startup vs. waiting for Tendeg/MMA Design to offer something is the key question.
