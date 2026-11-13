# 03 - Feasibility & Prototype Plan: High-Bandwidth CubeSat Communication Modules

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    3U CubeSat Bus                         │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ Satellite │    │  Interface   │    │    SDR        │  │
│  │ Flight    │◄──►│  Board       │◄──►│  Transceiver  │  │
│  │ Computer  │    │  (PC/104)    │    │  (Zynq FPGA)  │  │
│  └──────────┘    └──────────────┘    └───────┬───────┘  │
│                                               │          │
│  ┌──────────────────────────────────────────┐│          │
│  │          Feed Network (patch array)       ││          │
│  └──────────────────────────────┬───────────┘│          │
│                                  │            │          │
│  ┌──────────────────────────────┐│            │          │
│  │    Deployment Mechanism       ││            │          │
│  │  (SMA actuator + springs)     ││            │          │
│  └──────────────┬───────────────┘│            │          │
│                  │                │            │          │
└──────────────────┼────────────────┼────────────┘          │
                   │                                        │
     ┌─────────────▼─────────────────┐                     │
     │   Origami Reflectarray Panel   │                     │
     │   (Kapton + Cu elements)       │                     │
     │   Stowed: 15x10cm              │                     │
     │   Deployed: 50x50cm            │                     │
     └───────────────────────────────┘                     │
                   │                                        │
                   ▼ RF (Ka-band, 26 GHz)                  │
           [Ground Station Rx]                              │
```

**Data flow**: Satellite flight computer queues data -> Interface board packetizes -> SDR modulates (DVB-S2) -> PA amplifies -> Feed antenna illuminates reflectarray -> Reflected beam directed at ground station -> Ground station receives at 20-50 Mbps.

## Bill of Materials (Prototype)

| Component | Supplier | Cost | Confidence | Notes |
|-----------|----------|------|------------|-------|
| Kapton polyimide film (50um, Cu-clad) | DuPont/Sheldahl | $2,000 | VERIFIED | Standard aerospace material, quoted |
| Flex-circuit PCB etching (reflectarray pattern) | Flexible Circuit Technologies | $5,000 | VERIFIED | Standard flex-PCB process |
| SMA wire actuators (Nitinol) | Dynalloy/SAES | $500 | VERIFIED | Off-the-shelf components |
| Custom spring hinges (CNC titanium) | Custom machining | $1,500 | ASSUMED | Based on similar CNC part quotes |
| SDR module (Xilinx Zynq UltraScale+) | Abaco Systems / eval board | $8,000 | VERIFIED | Published pricing for eval kits |
| RF connectors & cabling (space-grade) | SV Microwave | $1,200 | VERIFIED | Catalog items |
| Patch array feed antenna (custom PCB) | PCB fab house | $800 | ASSUMED | Standard RF PCB, not space-qualified |
| 3U CubeSat structure/frame | Pumpkin Space / ISIS | $4,000 | VERIFIED | Catalog pricing |
| Deployment sensors (microswitches) | Various | $500 | VERIFIED | COTS components |
| Thermal blankets & coatings | Sheldahl | $1,000 | ASSUMED | Estimate based on similar missions |
| Power amplifier (Ka-band, space-grade) | Custom or Analog Devices | $3,000 | UNVERIFIED | Space-grade Ka-band PAs are scarce |
| **Total per prototype unit** | | **~$27,500** | | |

**3 prototypes budget: ~$82,500**

### Software & Tools

| Item | Cost | Confidence |
|------|------|------------|
| HFSS or CST Studio Suite license | $15,000/yr | VERIFIED |
| Thermal-vacuum chamber rental (10 days) | $50,000 | ASSUMED ($5K/day, varies by facility) |
| Anechoic chamber RF testing (5 days) | $15,000 | ASSUMED ($3K/day) |
| Vibration testing (3 days) | $6,000 | ASSUMED ($2K/day) |
| FPGA toolchain (Vivado) | $3,000/yr | VERIFIED |
| Mechanical CAD (SolidWorks/NX) | $5,000/yr | VERIFIED |

## Software Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| FPGA firmware | Xilinx Vivado + VHDL/Verilog | Industry standard for SDR on Zynq |
| Modulation | DVB-S2 IP core (open or licensed) | Proven satellite downlink standard |
| Flight software interface | C/C++ on Zynq ARM core | CubeSat bus protocols require low-level control |
| Ground station compatibility | SatNOGS or custom demodulator | Standard DVB-S2 receivers widely available |
| Simulation | Python (NumPy, SciPy) + OpenEMS or HFSS | Antenna design iteration |
| Thermal/structural analysis | ANSYS or open-source CalculiX | Deployment mechanism validation |
| Test automation | Python + NI VISA | Automated RF measurement campaigns |

## Build Instructions (Condensed)

### Phase 1: Design & Simulation (Weeks 1-8, ~$50K)
1. **Weeks 1-4**: RF design - reflectarray element pattern for Ka-band, simulate in HFSS, optimize for gain >18 dBi, define fold pattern avoiding copper at crease lines
2. **Weeks 2-6**: Mechanical design - origami fold geometry (Miura-ori variant), spring-hinge deployment mechanism with SMA release, FEA for deployment forces
3. **Weeks 3-8**: SDR firmware - configure Zynq for Ka-band, implement DVB-S2 modulation, develop CubeSat bus interface

### Phase 2: Prototype Fabrication (Weeks 8-16, ~$120K)
4. **Weeks 8-12**: Manufacture reflectarray panels - etch Cu on Kapton, laser-score fold lines
5. **Weeks 9-13**: Fabricate deployment mechanism - CNC hinges, integrate SMA actuators, manual deployment testing (50+ cycles)
6. **Weeks 12-16**: System integration - mount SDR, connect feed, wire actuators, functional test

### Phase 3: Testing & Validation (Weeks 16-24, ~$80K)
7. **Weeks 16-18**: Anechoic chamber RF testing - pattern measurement, gain verification
8. **Weeks 18-22**: Environmental testing - thermal-vacuum cycling, vibration
9. **Weeks 22-24**: End-to-end link demonstration - simulate LEO pass, measure throughput

### Phase 4: Flight Qualification (Weeks 24-40, ~$300K)
10. **Weeks 24-32**: Flight unit fabrication with space-qualified components
11. **Weeks 32-36**: Full qualification campaign (more extensive thermal-vac, radiation if needed)
12. **Weeks 36-40**: Integration with customer satellite, launch preparation

## Risk Register

| Risk | Probability | Impact | Mitigation | Residual Risk |
|------|-------------|--------|------------|---------------|
| Deployment mechanism jams in space | MEDIUM | CRITICAL | 100+ ground cycle tests, redundant release mechanism, thermal-vac deployment test | MEDIUM - cannot fully simulate microgravity on ground |
| Copper fatigue at fold lines | MEDIUM | HIGH | Route traces around folds (proven approach from OrigamiSat-2), accelerated life testing | LOW after design fix |
| Ka-band space-grade PA unavailable | MEDIUM | HIGH | Design for X-band fallback (lower data rate but easier components), or develop custom hybrid PA | MEDIUM |
| RF performance below simulation | LOW | HIGH | Conservative link budget (3 dB margin), oversized aperture | LOW |
| Antenna pointing insufficient | MEDIUM | MEDIUM | Wider beam (lower gain) option, ground-in-the-loop pointing | LOW |
| Launch vibration damages mechanism | LOW | CRITICAL | Over-spec structural margins, dedicated stow-lock mechanism, multiple vibe tests | LOW |
| Customer cannot integrate (interface issues) | MEDIUM | MEDIUM | Extensive documentation, reference design, integration support service | LOW |
| Optical downlink makes product obsolete before ROI | MEDIUM | CRITICAL | Hybrid RF+optical roadmap, target customers who need RF (clouds, simplicity) | MEDIUM - existential long-term |
| MMA Design or Tendeg launches competing product | MEDIUM | HIGH | Speed to market, aggressive pricing, commercial focus vs. their government focus | MEDIUM |
| Space-qualification costs exceed budget | HIGH | HIGH | Phase qualification (proto-qual first, full qual with customer funding), SBIR grant pursuit | MEDIUM |

## Validation Plan

**Key hypotheses to test (in order)**:
1. **Mechanical**: Origami deployment achieves >20x expansion with <1 degree surface accuracy (testable Week 12)
2. **RF**: Deployed reflectarray achieves >18 dBi gain at Ka-band (testable Week 17)
3. **Environmental**: System survives 50+ thermal cycles without degradation (testable Week 22)
4. **Market**: CubeSat operators will commit $120K+ for 10x+ downlink improvement (testable Week 8 via LOI campaign)
5. **Integration**: Module integrates with standard buses in <1 week (testable Week 24 with beta customer)

**Go/No-Go gates**:
- Gate 1 (Week 8): Simulation shows >18 dBi achievable AND at least 2 customer conversations confirm willingness to pay. NO -> KILL.
- Gate 2 (Week 18): Measured gain >15 dBi in anechoic chamber AND deployment works 95%+ of cycles. NO -> PIVOT (simplify mechanism, reduce expansion).
- Gate 3 (Week 24): Customer LOI secured AND environmental tests pass. NO -> KILL or PIVOT to consulting/government contracts.

## Cost & Time Estimate

| Phase | Duration | Cost | Cumulative |
|-------|----------|------|-----------|
| Design & simulation | 8 weeks | $100K (personnel + tools) | $100K |
| Prototype fabrication | 8 weeks | $200K (personnel + hardware + test) | $300K |
| Testing & validation | 8 weeks | $180K (personnel + facility rental) | $480K |
| Flight qualification | 16 weeks | $400K (space-grade parts + extended test) | $880K |
| First flight + operations | 12 weeks | $300K (launch + ops) | $1.18M |
| **Total to first revenue** | **~18 months** | **$1.8M** | |

**Monthly burn**: ~$70K (4 people + facilities)

## Founder-Market Fit Assessment

**Founder profile**: AI/ML infrastructure engineer with deep Python/systems/cloud expertise. No hardware, RF, mechanical, or space industry background.

**Fit rating: 2/10 - VERY POOR**

**Critical gaps**:
1. **RF engineering**: Reflectarray design requires deep electromagnetics expertise (PhD-level antenna engineering). Cannot be learned in months.
2. **Space qualification**: Knowledge of radiation effects, outgassing, thermal cycling, ITAR/EAR compliance is entirely experiential. Takes years to develop.
3. **Mechanical deployment**: Origami mechanism design is specialized (intersection of materials science, mechanical engineering, and mathematics).
4. **Industry relationships**: Space industry runs on trust and heritage. Customers will not buy flight hardware from a team without space credentials.
5. **Manufacturing**: Hardware manufacturing is fundamentally different from software deployment. Supply chain, quality control, yield management.

**What would be needed to compensate**:
- Co-founder with 10+ years space antenna experience (e.g., ex-JPL, ex-L3Harris antenna division, ex-Tendeg)
- Advisory board with CubeSat operators and former mission PIs
- Early hire: senior mechanical engineer with deployable mechanisms experience
- Willingness to spend 2+ years in a domain where software skills provide minimal advantage

**Honest assessment**: This is a hardware company requiring deep domain expertise in RF, space, and mechanical engineering. An AI/ML engineer founding this alone would face extreme credibility challenges with customers, investors, and hires. The software/cloud background provides almost no transferable advantage. The founder would be the weakest link on the team for the first 2-3 years.

**Recommendation**: Do not pursue unless you can recruit a domain-expert co-founder who brings the RF/space credentials. Your role would be CEO/business (leveraging general engineering judgment and systems thinking) while the co-founder is CTO.
