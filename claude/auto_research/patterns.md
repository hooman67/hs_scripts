# Patterns & Lessons Learned

Observations accumulated across research cycles.

---

## Cycle 001 (2026-06-07)

### Domain Performance
- **Space tech**: Best pass-through rate (1/1 promoted through all 5 stages). Less crowded, high barriers.
- **Biotech**: Strong balance of readiness + market size. 1 technology yielded 2 products in final output.
- **Energy**: High TRL techs exist but markets dominated by mega-cap incumbents ($B+ capex games). Low TRL techs are genuinely too early.
- **Materials science**: Most ideas were TRL 3-4. This domain may need longer gestation before practical products.
- **AI hardware**: Crowded by well-funded startups and Nvidia. Avoid unless truly novel architecture.
- **Sensing/HCI**: Magnetic nav was promising tech but already commercialized. Need to look for NEWER sensing modalities.

### Stage-Specific Patterns
- **Step 1 most common rejection**: TRL too low (3 of 3 rejections)
- **Step 2 most common rejection**: Incumbent dominance with massive capital (3 of 4 rejections)
- **Step 4 most common rejection**: IP held by existing company blocks entry (2 of 2 rejections)

### Search Strategy Notes
- IEEE Spectrum was highest quality source for near-commercial technologies
- New Atlas energy section had good coverage but many items were too early
- SingularityHub had good overview articles but poor URL structure (couldn't fetch individual articles)
- Company websites (Oriient, AstraNav) were valuable for competitive analysis
- Market research sites (paid) mostly blocked by paywalls but some gave headlines
- Crunchbase, PitchBook fully blocked — need alternative competitive intelligence sources

### Key Insight
**IP position is the single most important factor at Step 2 and Step 4.** Technologies with strong patents either:
- Create unassailable moats for the holder (Quaise) — meaning no opportunity for new entrants
- Signal that adjacent approaches may be patentable — meaning opportunity for alternative IP

---

## Cycle 002 (2026-06-07)

### Domain Performance
- **Food/ag tech**: Crowded — even novel approaches (mycelium, insect protein) have $100M+ funded competitors
- **Robotics (niche application)**: Best results when targeting VERY specific industrial niche (e-waste chip recovery)
- **Public domain research**: NIST laser-stirred alloys → highest-scoring idea (8/10) because NO IP barriers

### Key Insight
**Software-on-existing-hardware is the ideal startup model.** The alloy software plugin scored highest because: (1) zero hardware capex, (2) existing customer base of 300+ service bureaus, (3) no licensing required (public domain), (4) deep expertise is the moat (not patents or hardware).

---

## Cycle 003 (2026-06-07)

### Domain Performance
- **Environmental/water tech**: All occupied by funded incumbents (ASTERRA, CycloPure, Xylem)
- **Novel computing**: Either too early (TRL 3-4) or dominated by $B incumbents (Synopsys, Cadence)
- **Bioelectronics**: Novel but FDA pathway kills startup feasibility

### Key Insight
**Regulatory-gated markets are startup death traps.** Medical devices (FDA Class III = 5-7 years), nuclear, novel materials qualification all exceed typical startup funding cycles. Avoid unless you have $20M+ and patience.

**Cycle 003 produced zero graduates** — the harshest filter was Step 2 (competitive density). Most "novel" environmental/computing techs were actually already commercialized or dominated by incumbents.

---

## Cycle 004 (2026-06-07)

### Domain Performance
- **Grid/energy infrastructure**: Occupied by well-capitalized first-movers (ON.energy, Energy Dome, Form Energy)
- **Warehouse automation**: Strong results — mmWave inspection is a novel application angle in massive market
- **Ag robotics**: UV pest control is a genuine emerging niche with room for entrants

### Key Insight
**Application-layer plays on commodity components are the sweet spot.** Both Cycle 004 winners use cheap commodity hardware (TI radar chips at $40, UV LEDs at $4/watt) with proprietary software/protocols as the moat. The hardware alone isn't defensible; the intelligence layer is.

---

## Cross-Cycle Patterns (Summary — Updated After 20 Cycles)

1. **Best archetype**: Software + commodity hardware + underserved mid-market + no regulatory barriers + immediate measurable ROI
2. **Worst archetype**: Novel hardware + regulatory pathway + well-funded incumbents = zero graduates
3. **Step 2 is the hardest filter**: 60%+ of technologies rejected here across all cycles
4. **Step 1 TRL threshold matters**: Raising from TRL 4→5 minimum would have saved research time
5. **Market size correlates with competition**: The biggest markets ($100B+) always have $100M+ funded players
6. **$200K-500K capital range** is the actual sweet spot: enough to validate, low enough for bootstrap/small angel
7. **Service models de-risk**: Every winning idea can start as a service before building products
8. **"Democratize expensive professional tool" is the meta-pattern**: Take a $50-500K system, replicate 80% on commodity hardware + AI, sell at 1/10th price to the 10x larger mid-market
9. **Network effects matter**: Ideas with community/data flywheels (laser parameters, alloy recipes) are more defensible
10. **Pure software > software+hardware > hardware**: Every layer of hardware adds risk, cost, and time

---

## Cycles 005-020 Key Insights

### Cycle 005: Application-on-infrastructure wins
Both graduates (brewery EPR, livestock tags) use someone else's breakthrough as a platform.

### Cycle 006: Construction is a graveyard
Certification timelines, conservatism, long sales. Katerra's $3B failure is the cautionary tale.

### Cycle 007: Public domain AI tools are gold
TEGNet (publicly available) enables a design service with zero IP risk. Same as NIST alloy research.

### Cycle 008-009: Vertical SaaS for niche industries
Thermal inspection for trades, fermentation optimization — deep domain expertise IS the moat.

### Cycle 010: The breakthrough cycle (3 graduates)
All followed the pattern perfectly: $200-5K commodity hardware + AI = 10-250x cost advantage.

### Cycle 011: Record cycle (4 graduates)
Pallet inspection, recommerce grading, food QC prediction, bolt monitoring — all "boring" industrial problems with clear ROI.

### Cycles 012-016: Continued mining of the pattern
Textile inspection, bird acoustic monitoring, fire sprinkler inspection — niche industrial + AI keeps working.

### Cycle 017: First truly dry cycle
Domain exhaustion starting. The "obvious" large unserved markets have been found.

### Cycles 018-020: Final picks
Asphalt thermal QC, laser cutting optimization, lumber grading — these work because of specific regulatory/market timing factors.

### Final insight (Cycles 001-020): Laser Cutting Optimization is the best idea overall
$200K capital, pure SaaS, 200K+ machines installed, network effects from parameter sharing, same archetype as the #1 idea from Cycle 002 (alloy software). If you build one thing, build this.

---

## Cycles 021-040 Key Insights

### Cycle 021: Printing/packaging is saturated
Explored flexo, corrugated, glass, injection molding. Found 6+ competitors in EVERY sub-segment. Lesson: European industrial QC companies (GlassQuality, SIKORA, AVT, Isra Vision) dominate these niches. Only 1 graduate (5/10 — flexo ink consumption prediction) from 10 technologies.

### Cycle 022: Wire/cable and paper — hidden opportunity in overlooked industries
WireVision AI (8/10) layers commodity cameras on wire lines at 15% of SIKORA cost. BreakGuard (7/10) predicts paper web breaks via OPC-UA. Industries that sound "boring" often lack modern software.

### Cycle 023: Water/wastewater and mining dust suppression
Small municipal plants are perfectly underserved — 14K+ plants with basic SCADA but no optimization. Mining dust suppression combines weather + GPS + sensors in a way nobody else does.

### Cycle 024: "Invisible waste" is the best ROI story
Three graduates, all focused on waste nobody can currently SEE: welding gas usage, laundry chemical dosing, coating cure failures. If the customer doesn't know they're wasting money, giving them visibility = instant demand.

### Cycle 025: Agriculture post-harvest is wide open
$100K+ controlled atmosphere systems vs. manual ventilation = perfect gap for $3-8K smart systems. Grain drying is a $200K+/farm energy cost with zero AI optimization available brand-agnostically.

### Cycle 026: Field trades have absurd paper-based workflows
TAB technicians still handwrite airflow measurements on paper forms. 2,000-3,000 firms doing this daily. Pure mobile app + Bluetooth instrument pairing = $150K to build, $99-199/seat/month.

### Cycle 027: Dental lab manufacturing — surprising niche
6,000+ mid-size dental labs with $200K+ CAD/CAM equipment running unoptimized. Pure SaaS (scheduling + remake prediction) works without touching the hardware. Lab managers are tech-savvy buyers.

### Cycle 028: "Software on expensive instruments" pattern confirmed
XRF Workflow AI turns a "dumb" $30K gun into an intelligent grading system. This pattern (add AI brain to expensive instrument customer already owns) eliminates all hardware risk. Same pattern as laser cutting (add brain to expensive machine).

### Cycle 029: Fleet maintenance via API = zero-hardware startup
DPF Regen Optimizer connects to Samsara/Geotab APIs and predicts regeneration events. No hardware, no installation, no physical world interaction. The "parasitic SaaS" model is the ultimate capital-efficient play.

### Cycle 030: Best cycle overall — 4 graduates including highest score ever
Plasma Consumable Life Prediction scored 9/10 — highest ever. Metal fabrication (plasma, press brake) is the richest unexplored vertical for the winning archetype. 50K+ shops, expensive trial-and-error, zero software optimization today. SpringbackAI is essentially "laser cutting parameters for press brakes."

### Cycle 031: Food processing specific verticals have room
Dairy heat exchanger fouling, bakery proofing prediction, oven energy — each is a distinct niche problem with clear $ savings. Key: go narrow (just heat exchangers, not "all dairy").

### Cycle 032: Composite cure monitoring = consumable revenue model
CureTrack AI (7/10) uses $5 disposable sensors for recurring revenue. Novel business model for hardware ideas: make the sensor disposable so the revenue is SaaS-like without the hardware stigma.

### Cycle 033: Rubber compound formulation is "alloy software for rubber"
Same pattern as Custom Alloy Software (Cycle 002) but for rubber compounds. The difference: mid-market rubber companies don't have PhD chemists, so they NEED software assistance. Captures tribal knowledge of retiring chemists.

### Cycle 034: Energy small operators are underserved but sales are harder
Solar/co-op operators need help but are conservative, price-sensitive, and have long decision cycles. InverterIQ's warranty claim angle provides immediate $ value. Co-op outage prediction requires board approval.

### Cycle 035: Woodworking is "CNC metal cutting for a different material"
50K+ CNC router shops are exactly analogous to CNC metal shops but nobody has brought tool wear monitoring to them. Proven physics (vibration → tool condition) transplants directly. 4 graduates — this vertical has depth.

### Cycle 036: Building services/janitorial — regulatory + fragmentation = opportunity
IPM Compliance AI (8/10) is the lowest-capital idea discovered in 40 cycles ($80-150K). Pest control companies MUST document IPM programs. No one has automated this with AI. Regulatory mandate = captive buyer.

### Cycle 037: Craft beverage QC — specific enough to avoid "food tech" saturation
Dissolved oxygen in craft beer is universally acknowledged as THE quality problem. $50K+ inline DO systems exist for large breweries. $2,500 sensor kit + SaaS for the 9K craft breweries that can't afford inline systems.

### Cycle 038: Metal finishing — competitive density higher than expected
Grinding (Marposs), plating (ProcessIQ) — these niches have entrenched players. Only 2 marginal graduates (5/10 each). Domain is partially mined already.

### Cycle 039: Industrial gas distribution — surprisingly unserved
24.5K+ food packaging plants with nitrogen generators have ZERO monitoring. Single failure event costs $50K+. NitroGuard is the compressed air leak detection of nitrogen generation.

### Cycle 040: Label manufacturing — narrow enough angle works
While broad printing QC is saturated, very specific use cases (die-cut registration using existing cameras) are unserved. Key: "pure software on existing cameras" bypasses the entire AVT/Isra competitive landscape.

---

## Cross-Cycle Patterns (Final Summary — 40 Cycles)

1. **Best archetype**: Software + commodity hardware + underserved mid-market + no regulatory barriers + immediate measurable ROI
2. **Best sub-archetype (NEW)**: Pure SaaS layered on hardware/systems the customer already owns
3. **Worst archetype**: Novel hardware + regulatory pathway + well-funded incumbents = zero graduates
4. **Step 2 is the hardest filter**: 50%+ of technologies rejected here across all cycles
5. **Step 1 TRL threshold matters**: Raising from TRL 4→5 minimum would have saved research time
6. **Market size correlates with competition**: The biggest markets ($100B+) always have $100M+ funded players
7. **$80K-400K capital range** is the actual sweet spot for solo/duo founders
8. **Service models de-risk**: Every winning idea can start as a service before building products
9. **"Democratize expensive professional tool" is the meta-pattern**: Take a $50-500K system, replicate 80% on commodity hardware + AI, sell at 1/10th price to the 10x larger mid-market
10. **Network effects matter**: Ideas with community/data flywheels are more defensible
11. **Pure software > software on existing HW > software+commodity HW > hardware**: Every layer of physical-world interaction adds risk
12. **European industrial QC is entrenched (NEW)**: Always check for SIKORA/Pixargus/Dr.Schenk/GlassQuality equivalents before promoting
13. **Regulatory compliance mandates = captive buyers (NEW)**: Product that helps meet existing regulation > product that needs regulatory approval
14. **"Invisible waste" creates best demand (NEW)**: If customer can't currently see the waste, making it visible = instant sale
15. **Domain exhaustion hits around 35 cycles (NEW)**: Graduate quality declines, overlaps increase, diminishing returns

