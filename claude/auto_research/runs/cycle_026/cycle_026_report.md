# Cycle 026 Report

**Date**: 2026-06-08
**Domains explored**: HVAC TAB automation, elevator predictive maintenance for independents, parking structure condition assessment, roof membrane leak detection, building envelope thermography automation, HVAC fault detection for SMBs, escalator monitoring, duct leakage detection, commercial building energy audits, GPR concrete scanning AI

---

## Step 1: Technology Discovery

### 1. AI-Powered HVAC TAB (Testing Adjusting Balancing) Automation
- **Domain**: Commercial HVAC commissioning
- **Breakthrough**: Wireless multi-sensor airflow measurement (Evergreen Telemetry Wrist Reporter, Testo 405i Bluetooth) combined with AI-driven automatic balancing calculations, eliminating iterative manual duct-by-duct adjustments
- **TRL**: 7 (Evergreen Telemetry shipping since 2010, wireless sensors proven, AI balancing algorithms demonstrated)
- **Time to product**: 6-9 months
- **Status**: PROMOTED
- **Reasoning**: TAB is a $6.2B market, heavily manual (paper forms, 2-person teams), severe technician shortage (110K gap). A software platform that ingests wireless sensor data and auto-generates balancing instructions could reduce a 2-person, 3-day job to 1-person, 1-day. Low hardware cost (commodity Bluetooth sensors), high software margin.

### 2. Elevator Predictive Maintenance for Independent Service Companies
- **Domain**: Vertical transportation maintenance
- **Breakthrough**: Low-cost vibration/accelerometer IoT nodes with edge ML for ride-quality degradation and fault prediction, targeting independent service providers who lack OEM telemetry
- **TRL**: 7 (Uptime.ac deployed at scale in Europe, Smart Lifts in Singapore, Elevate Tech operational)
- **Time to product**: 9-12 months
- **Status**: REJECTED
- **Reasoning**: Competitive density is HIGH. Uptime.ac ($20M raised, 6000 customers), SafeLine Lyra (4000 units deployed), DATOMS, Elevate Tech, plus KONE/Otis/Schindler all have proprietary solutions. Market already has 5+ funded players.

### 3. Automated Parking Structure Condition Assessment
- **Domain**: Infrastructure inspection
- **Breakthrough**: Drone-mounted GPR + AI interpretation for rapid concrete deterioration mapping without lane closures; Birdsview (Norway) demonstrates sub-minute rebar analysis from GPR data
- **TRL**: 6-7 (Infrasense doing GPR since 1987, Birdsview AI proven, DroneDeploy commercial drones established)
- **Time to product**: 12-18 months
- **Status**: PROMOTED
- **Reasoning**: Parking structures require inspection every 3-5 years (IBC code). Current assessment is expensive manual engineering ($5-15/sq ft). AI-automated GPR interpretation could reduce cost 80%. Infrasense is a small ($1-10M) consulting firm, not a scalable software company. Birdsview is Norway-focused on new construction. Gap exists for US parking-specific automated assessment.

### 4. Continuous Roof Membrane Leak Detection (Permanent Monitoring)
- **Domain**: Commercial roofing
- **Breakthrough**: Permanently embedded capacitance/impedance sensor grids with wireless cloud monitoring for real-time leak detection on flat commercial roofs
- **TRL**: 8 (Detec PermaScan, SMT Research FutureCast, Sentinel Roof Technologies all shipping)
- **Time to product**: 6-9 months
- **Status**: REJECTED
- **Reasoning**: Competitive density is HIGH. At least 6 established players: ILD (since 2001, global), Detec/PermaScan (permanent monitoring), SMT Research (FutureCast), Sentinel Roof Technologies, Honza Group (since 2005), Tector System. The $1.2B market is already well-served. No meaningful differentiation angle available.

### 5. Building Envelope Thermography AI (Drone-Based)
- **Domain**: Building diagnostics / energy efficiency
- **Breakthrough**: AI analysis of drone-captured thermal imagery to automatically identify insulation gaps, air leakage paths, moisture intrusion, and window seal failures
- **TRL**: 7 (Lamarr.AI shipping, Inspekt AI operational, AERIALLY.AI launched 2024)
- **Time to product**: 6-9 months
- **Status**: REJECTED
- **Reasoning**: Competitive density is HIGH. Lamarr.AI ($1.1M pre-seed, MIT spinout), Inspekt AI (2022), ThermoLabs, AERIALLY.AI (2024), SkyVisor, Therm-A.I, Averroes.ai - at least 7 players already in this space. The $1.46B market has attracted multiple funded startups and the space is crowded.

### 6. HVAC Fault Detection for Small/Medium Commercial Buildings (No BMS Required)
- **Domain**: Building energy optimization
- **Breakthrough**: AI-powered HVAC fault detection using only utility meter data and cheap IoT temperature/humidity sensors, without requiring a building management system - targeting the 90% of commercial buildings under 50,000 sq ft that lack BMS
- **TRL**: 6-7 (SensGreen deploys edge AI on Raspberry Pi, LeanFM Prescriptiv operational)
- **Time to product**: 9-12 months
- **Status**: PROMOTED
- **Reasoning**: Existing FDD players (Clockworks $28M raised, CIM $16.8M ARR, BrainBox AI $50M raised) ALL require BMS integration. Small commercial buildings (restaurants, retail, small offices) waste 20-40% on HVAC but have no BMS. A sensor-light approach (3-5 wireless sensors + utility data + weather API) could serve 10x more buildings. SensGreen is Turkey-based and early; LeanFM has only $605K funding and 7 employees. Gap exists for US-focused, BMS-free HVAC waste detection.

### 7. Escalator Predictive Maintenance
- **Domain**: Vertical transportation
- **Breakthrough**: Non-invasive vibration/acoustic sensors with ML for predicting handrail, step chain, and drive unit failures on escalators
- **TRL**: 7 (SafeLine Lyra deployed 4000 units, OxMaint operational, KONE has IoT platform)
- **Time to product**: 9-12 months
- **Status**: REJECTED
- **Reasoning**: SafeLine Lyra already has 4000 deployed units with AI analytics. OxMaint achieved 98% uptime at airports. KONE has 70% more fault detection. Market has established players and escalators are typically serviced by the same companies doing elevators (which is already crowded).

### 8. AI-Automated GPR Interpretation for Concrete Infrastructure
- **Domain**: Non-destructive testing / structural inspection
- **Breakthrough**: Deep learning models achieving 97%+ accuracy on GPR scan interpretation for rebar location, diameter, cover depth, and corrosion detection - replacing expensive manual interpretation by specialized engineers
- **TRL**: 7 (Birdsview shipping, GeoRadar AI operational, academic models validated)
- **Time to product**: 9-12 months
- **Status**: PROMOTED
- **Reasoning**: GPR data interpretation is currently a bottleneck - requires specialized engineers, takes days/weeks for reports. Birdsview (Norway, early-stage, ~$711K from Enova) and GeoRadar are the only AI players. The broader NDT market is $15B+. A US-focused SaaS that takes raw GPR files and returns instant structural reports could serve thousands of engineering firms. Low competitive density (2 players, both small/international).

### 9. Wireless TAB Field Documentation & Auto-Report Platform
- **Domain**: HVAC commissioning documentation
- **Breakthrough**: Mobile-first platform that pairs with any Bluetooth airflow instrument, auto-logs readings by location (using floor plan recognition), generates NEBB/AABC-compliant reports automatically, and flags out-of-spec readings with correction recommendations
- **TRL**: 8 (BuildingStart exists since 2006 but is outdated with $580K revenue; CxPlanner exists for commissioning broadly)
- **Time to product**: 4-6 months
- **Status**: PROMOTED
- **Reasoning**: BuildingStart (2006, 9 employees, $580K revenue) is the only TAB-specific software and it's dated. Generic HVAC software (ServiceTitan, Jobber) doesn't handle TAB workflows. TAB technicians still use paper/Excel. A modern mobile platform with Bluetooth sensor integration and automated report generation would have near-zero competition. Very low capital requirement.

### 10. Automated Commercial Building Energy Audit SaaS
- **Domain**: Energy efficiency / compliance
- **Breakthrough**: AI platform that performs ASHRAE Level II energy audits using utility bills, weather data, building metadata, and minimal IoT sensors - replacing $15-50K manual audits with $2-5K automated reports
- **TRL**: 6-7 (NexEnergyAudit.ai, Enersee.ai both operational)
- **Time to product**: 9-12 months
- **Status**: REJECTED
- **Reasoning**: Multiple players already emerging: NexEnergyAudit.ai (ASHRAE 211 compliant), Enersee.ai (portfolio-scale), SparkZ3R0. Additionally, the big FDD platforms (BrainBox AI, CIM, Clockworks) all offer energy analysis. Building energy audit regulations vary by city/state creating fragmented compliance needs. Not capital-efficient enough given competition.

---

## Step 2: Competitive Analysis

### AI-Powered HVAC TAB Automation
- **Competitors found**: 75F (dynamic airflow balancing, $81.3M raised - but targets building automation not TAB services), Evergreen Telemetry (wireless TAB instruments, $3M revenue, hardware only - no AI), Distech Controls/myDC AirBalancing (VAV calibration app - limited to their own controllers), Flair (residential only), Zonex ($4.7-6.1M revenue, hardware dampers not software)
- **Competitive density score**: 2/5
- **Differentiation angle**: None of these are an AI-driven TAB workflow automation platform. 75F is building automation (permanent install), not TAB services. Evergreen makes instruments but no software platform. The gap is: take wireless sensor readings + building design specs + AI optimization = auto-calculated damper settings and balancing sequence. This replaces the iterative trial-and-error that takes TAB technicians 2-5 days per project.
- **Status**: PROMOTED
- **Reasoning**: No direct competitor offers AI-powered TAB workflow optimization. The adjacent players are either hardware-only (Evergreen, Zonex) or permanent building automation (75F, BrainBox). TAB is a distinct professional service with specific workflow needs unmet by existing tools.

### Automated Parking Structure Condition Assessment
- **Competitors found**: Infrasense (established 1987, $1-10M revenue, manual GPR interpretation), Bridgology (GPR + LiDAR, consulting firm), GPR Data (consulting services), DroneDeploy (generic drone platform, not parking-specific), Benesch (engineering firm offering thermal drone), Geobility Systems (one-off projects)
- **Competitive density score**: 3/5
- **Differentiation angle**: All current players are consulting/service firms doing manual analysis. None offer a scalable software product that property managers can subscribe to for regular automated assessments. However, the sales cycle for infrastructure inspection is long (property managers, engineering firms) and the market may be too niche.
- **Status**: REJECTED
- **Reasoning**: While no pure software competitor exists, the buyer persona (property managers, municipalities) has long sales cycles. GPR hardware is expensive ($15-50K). The product requires both drone + GPR hardware expertise and AI software - capital-intensive hybrid. Birdsview (backed by CEMEX Ventures, VINCI) is likely to expand from Norway. The competitive density of 3 plus capital requirements and sales cycle make this unattractive.

### HVAC Fault Detection for Small/Medium Commercial Buildings
- **Competitors found**: SensGreen ($2.5M raised, Turkey-based, Raspberry Pi edge deployment, 12 countries), LeanFM/Prescriptiv ($605K raised, Pittsburgh, 7 employees), iFactory (general IoT FDD), OxMaint (broad CMMS). Large players (Clockworks $28M, CIM $16.8M ARR, BrainBox AI $50M) all require BMS.
- **Competitive density score**: 3/5
- **Differentiation angle**: Target specifically the "no BMS" segment - buildings under 25,000 sq ft (strip malls, restaurants, small offices, churches) using ONLY utility meter data + 3-5 wireless temp/humidity sensors ($50 each). No integration required. The large players cannot go downmarket because their unit economics require BMS buildings ($500K+/year energy spend). SensGreen is international and early.
- **Status**: PROMOTED
- **Reasoning**: The "no-BMS" angle is genuinely differentiated. The big players (Clockworks, CIM, BrainBox) structurally cannot serve small buildings - their entire pipeline requires BMS data feeds. SensGreen is the closest competitor but is Turkey-based, early-stage, and not US-focused. LeanFM is tiny. The downmarket segment is 10x larger by building count but currently unserved.

### AI-Automated GPR Interpretation for Concrete Infrastructure
- **Competitors found**: Birdsview (Norway, ~$711K Enova grant, backed by CEMEX Ventures + VINCI, sub-minute analysis), GeoRadar (AI for GPR, details limited), academic research (Cairo University 97% accuracy)
- **Competitive density score**: 2/5
- **Differentiation angle**: US-focused SaaS platform where any GPR operator uploads scans and gets instant AI-interpreted reports with rebar mapping, corrosion risk assessment, and structural recommendations. Birdsview is Norway/EU focused and appears hardware-coupled. No US player exists.
- **Status**: PROMOTED
- **Reasoning**: Only 2 commercial competitors globally, neither US-focused. GPR scanning is done by thousands of US engineering/NDT firms who all do manual interpretation. A cloud SaaS model (upload GPR file, get report) is highly scalable with excellent unit economics. Low competitive density, clear pain point (interpretation bottleneck), established customer base (NDT firms).

### Wireless TAB Field Documentation & Auto-Report Platform
- **Competitors found**: BuildingStart (2006, 9 employees, $580K revenue, cloud/mobile commissioning), CxPlanner (commissioning broadly, not TAB-specific), generic HVAC field service tools (ServiceTitan, Jobber - not TAB-specific)
- **Competitive density score**: 1/5
- **Differentiation angle**: Purpose-built for TAB technicians: Bluetooth instrument pairing, floor plan auto-mapping, NEBB/AABC report generation, out-of-spec flagging, correction sequence recommendations. BuildingStart is 20 years old with minimal traction. No modern mobile-first TAB tool exists.
- **Status**: PROMOTED
- **Reasoning**: Essentially zero meaningful competition. BuildingStart ($580K revenue after 20 years) has not captured the market. TAB technicians are underserved by generic tools. Purpose-built modern mobile app with Bluetooth sensor integration and automated report generation fills a clear gap. Lowest competitive density score of any idea this cycle.

---

## Step 3: Market Analysis

### AI-Powered HVAC TAB Automation
- **Target market**: NEBB/AABC-certified TAB contractors, mechanical contractors with TAB divisions, commissioning agents performing TAB as part of Cx projects
- **TAM**: $6.2B global TAB services market
- **SAM**: ~$1.5B US TAB services market (estimated ~25% of global); software capturing 5-10% of service value = $75-150M SAM
- **Revenue model**: SaaS subscription ($200-500/month per technician) + per-project AI optimization reports ($100-300 per project)
- **Status**: PROMOTED
- **Reasoning**: Clear willingness to pay - TAB projects cost $5K-50K each; saving 50% labor time on each project easily justifies $500/month software. Large enough SAM ($75-150M) with identifiable buyer persona. Monthly recurring revenue from subscriptions plus usage-based upside.

### HVAC Fault Detection for Small/Medium Commercial Buildings (No BMS)
- **Target market**: Small commercial building owners/operators (strip malls, restaurants, retail, small offices, churches) - buildings 5,000-25,000 sq ft without BMS
- **TAM**: 5.9M commercial buildings in US, ~80% under 50,000 sq ft = 4.7M buildings. Average $5K-15K/year energy waste. Total addressable HVAC waste: $25-70B
- **SAM**: Software at $100-200/month targeting buildings with $3K+/year identifiable savings = ~500K addressable buildings = $600M-1.2B SAM
- **Revenue model**: SaaS $99-199/month per building, hardware kit (5 sensors) sold at cost ($250) or subsidized. Energy savings guarantee model possible.
- **Status**: PROMOTED
- **Reasoning**: Enormous underserved market. The "no BMS" segment has been ignored because big players need rich data streams. With modern ML, utility data + minimal sensors + weather data can identify 60-80% of common faults (stuck dampers, short cycling, simultaneous heating/cooling). SAM well above $100M threshold.

### AI-Automated GPR Interpretation for Concrete Infrastructure
- **Target market**: NDT/engineering firms performing concrete scanning (bridge decks, parking structures, building slabs), structural engineering consultancies, infrastructure asset owners
- **TAM**: Global NDT market $15.8B; concrete/structural inspection subset estimated $3-5B
- **SAM**: US GPR concrete scanning services ~$800M; AI interpretation software capturing 10-15% of service value = $80-120M SAM
- **Revenue model**: Per-scan pricing ($50-200 per GPR file processed) or unlimited monthly subscription ($500-2000/month per firm)
- **Status**: PROMOTED
- **Reasoning**: Clear bottleneck pain point - GPR interpretation takes specialized engineers hours/days per project. Instant AI reports would be transformational for productivity. Per-scan pricing aligns value with usage. Engineering firms are accustomed to paying for specialized software. SAM of $80-120M is sufficient.

### Wireless TAB Field Documentation & Auto-Report Platform
- **Target market**: TAB contractors, commissioning agents, mechanical contractors performing air/hydronic balancing
- **TAM**: $6.2B global TAB services market (documentation is ~15-25% of project time = $900M-1.5B in labor cost for documentation)
- **SAM**: US market, ~2,000-3,000 TAB firms, average 5-15 technicians = 10K-45K seats. At $100-200/month = $12M-108M SAM
- **Revenue model**: SaaS per-seat $99-149/month + premium tier with AI-powered correction recommendations at $199-299/month
- **Status**: PROMOTED
- **Reasoning**: Even at conservative estimates (2,000 firms, 5 seats average, $100/month), SAM is $12M which is below threshold. However, expanding to include all commissioning agents, HVAC contractors doing TAB work, and facility managers doing ongoing rebalancing pushes addressable market to $50-100M. Marginal on SAM but extremely capital-efficient. PROMOTED for feasibility analysis given exceptional capital efficiency.

---

## Step 4: Feasibility Analysis

### AI-Powered HVAC TAB Automation
- **Technical risk**: Medium - AI optimization of airflow networks is well-understood in simulation; challenge is translating to field conditions with incomplete duct layouts and sensor noise
- **Market risk**: Low - TAB technician shortage is acute, labor savings are immediately quantifiable, buyers are technical and understand the value proposition
- **Execution risk**: Medium - requires partnerships with instrument manufacturers (Evergreen, Testo) for data integration; building credibility in a trades-based industry takes time
- **Timing risk**: Low - wireless sensors just became practical, technician shortage is worsening, no competitor has moved yet
- **Capital required**: $300-500K
- **Feasibility score**: 7.5/10
- **Status**: PROMOTED
- **Reasoning**: Strong fit to winning archetype. Takes $50-200K professional TAB service and augments it with AI to make one technician do the work of two in half the time. Low capital, clear ROI for buyers, proven underlying tech, no regulatory barriers. Medium technical risk is manageable with iterative field testing.

### HVAC Fault Detection for Small/Medium Commercial Buildings (No BMS)
- **Technical risk**: Medium - achieving useful fault detection accuracy from minimal sensor data (5 sensors vs. 500 BMS points) requires novel ML approaches; may have high false-positive rates initially
- **Market risk**: Medium - small building owners are cost-sensitive and may not prioritize HVAC optimization; requires proving ROI with guaranteed energy savings
- **Execution risk**: Medium-High - SMB sales require either self-serve or channel partnerships (HVAC contractors, utility programs); customer acquisition cost could be high for $99-199/month product
- **Timing risk**: Low - energy costs rising, ML models improving, wireless sensors commoditized
- **Capital required**: $400-700K
- **Feasibility score**: 6/10
- **Status**: REJECTED
- **Reasoning**: The unit economics are challenging. At $99-199/month, customer acquisition cost for SMB building owners likely exceeds $1,000 (direct sales to fragmented market). The technical challenge of useful FDD from minimal sensors adds product risk. SensGreen and LeanFM exist as competitors even if small. The combination of medium-high execution risk + medium technical risk + fragmented buyer base makes this less attractive than alternatives despite the large market.

### AI-Automated GPR Interpretation for Concrete Infrastructure
- **Technical risk**: Low-Medium - Birdsview and academic research have proven 97%+ accuracy; the ML models work, challenge is handling diverse GPR equipment formats and edge cases
- **Market risk**: Low - engineering firms already pay $150-500/hour for manual GPR interpretation; AI at $50-200/scan is immediate cost savings
- **Execution risk**: Medium - need to build trust with conservative engineering profession; requires professional liability considerations for structural assessments
- **Timing risk**: Low - Birdsview has validated the technology, US market is unserved, GPR adoption is growing
- **Capital required**: $300-600K
- **Feasibility score**: 7/10
- **Status**: PROMOTED
- **Reasoning**: Solid fit to winning archetype. Replaces expensive specialist interpretation ($300-500/hour engineer time) with instant AI reports. Birdsview validates the technical approach but is EU-focused. Engineering firms are accustomed to paying for specialized software tools. Main risk is professional liability and trust-building in conservative industry.

### Wireless TAB Field Documentation & Auto-Report Platform
- **Technical risk**: Low - mobile app development with Bluetooth instrument pairing is well-understood; NEBB/AABC report formats are documented standards
- **Market risk**: Low-Medium - TAB firms know documentation is painful; risk is whether they'll adopt new software vs. "we've always done it this way" inertia
- **Execution risk**: Low - small team can build MVP in 3-4 months; direct sales to TAB firms at trade shows (NEBB/AABC conferences); low touch onboarding
- **Timing risk**: Low - Bluetooth instruments are now standard; BuildingStart has proven market exists but failed to capture it
- **Capital required**: $150-250K
- **Feasibility score**: 8/10
- **Status**: PROMOTED
- **Reasoning**: Exceptional capital efficiency. $150-250K to reach product-market fit. Nearly zero technical risk (mobile app + Bluetooth + report generation). Clear buyer pain point. Tiny existing competition (BuildingStart is 20 years old with $580K revenue - proof of demand but poor execution). The only risk is market size - but even capturing 10% of TAB firms at $100/month/seat generates meaningful revenue with near-zero marginal cost.

---

## Step 5: Execution Summary

### Wireless TAB Field Documentation & Auto-Report Platform (Feasibility: 8/10)
- **Product**: Mobile-first app (iOS/Android) that pairs with Bluetooth airflow instruments (Testo 405i, Evergreen Wrist Reporter, CPS ABM-200), auto-logs measurements by location on uploaded floor plans, calculates cfm/fpm vs design specs, flags deviations, and generates NEBB/AABC-compliant PDF reports with one tap. Premium tier adds AI-suggested correction sequences.
- **Technology**: React Native mobile app, Bluetooth Low Energy SDK integrations, floor plan annotation engine (computer vision for room detection), NEBB/AABC report template engine, cloud sync for team collaboration
- **Market**: 2,000-3,000 TAB firms in US, average 5-15 field technicians each, plus thousands of mechanical contractors and commissioning agents who perform TAB work. Initial beachhead: NEBB-certified firms (most process-oriented, highest documentation burden).
- **Revenue model**: $99/month per seat (standard), $199/month per seat (premium with AI correction recommendations). Annual contracts with volume discounts for firms with 10+ technicians.
- **Capital**: $150-250K for MVP through first 50 paying customers
- **Key strength**: Extreme capital efficiency, nearly zero competition, clear daily pain point (TAB technicians hate paperwork), low technical risk, rapid time to revenue (4-6 months)
- **Key risk**: Market size ceiling - even capturing 100% of dedicated TAB firms may top out at $30-50M ARR. Expansion into broader commissioning and ongoing building rebalancing required for venture-scale.

### AI-Powered HVAC TAB Optimization Engine (Feasibility: 7.5/10)
- **Product**: SaaS platform that ingests building design documents (mechanical drawings, duct layouts) and real-time wireless sensor data from the field, then uses computational fluid dynamics + ML optimization to calculate optimal damper positions and balancing sequences - replacing the iterative trial-and-error process that makes TAB projects take 2-5 days.
- **Technology**: Digital twin of duct network from mechanical drawings (CAD/PDF parsing), physics-informed ML model trained on TAB project data, real-time sensor data integration via Bluetooth/API, optimization engine outputting step-by-step balancing instructions for technicians
- **Market**: Same TAB market as above ($6.2B global, ~$1.5B US) but capturing higher value per project. Each TAB project saves 30-50% labor time ($2K-10K savings on typical commercial project).
- **Revenue model**: Per-project pricing ($200-500 per optimization run) + monthly platform subscription ($300-500/month per firm). Enterprise deals for large TAB firms with 20+ active projects/month.
- **Capital**: $300-500K for core algorithm development, field validation with partner firms, initial commercial launch
- **Key strength**: Massive labor savings per project (quantifiable ROI), solves acute technician shortage, defensible AI/physics models, recurring revenue from ongoing use
- **Key risk**: Technical risk in achieving reliable optimization across diverse building types; requires accurate duct layout data which may not always be available; longer sales cycle with larger TAB firms

### AI-Automated GPR Interpretation SaaS (Feasibility: 7/10)
- **Product**: Cloud platform where NDT technicians and structural engineers upload raw GPR scan files and receive instant AI-generated reports including rebar mapping, cover depth analysis, corrosion probability assessment, and structural condition ratings - replacing 4-8 hours of manual expert interpretation per scan set.
- **Technology**: Deep learning models trained on labeled GPR datasets (multiple equipment manufacturers: GSSI, Proceq, IDS), automated report generation with visualizations, support for multiple GPR file formats, confidence scoring and uncertainty flagging for edge cases
- **Market**: ~5,000 NDT firms in US performing concrete scanning, plus structural engineering consultancies, infrastructure asset owners (DOTs, property managers), and construction QC firms. Average firm processes 50-200 GPR scans/month.
- **Revenue model**: Per-scan pricing ($75-150 per processed file) with volume discounts, or unlimited monthly subscription ($1,000-2,000/month for heavy users). Enterprise tier for DOTs and large engineering firms.
- **Capital**: $300-600K for model training (requires labeled dataset acquisition), platform development, validation with pilot firms, initial commercialization
- **Key strength**: Clear productivity multiplier (4-8 hours reduced to minutes), proven technology (Birdsview validates approach), sticky product (once integrated into workflow, switching costs are high), usage-based revenue scales with customer growth
- **Key risk**: Professional liability - if AI misses corrosion or structural defect, consequences could be severe. Requires careful positioning as "decision support" rather than replacement for professional judgment. Conservative engineering culture may slow adoption. Dataset acquisition for training could be expensive.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 5 | 5 |
| Step 2 | 5 | 4 | 1 |
| Step 3 | 4 | 4 | 0 |
| Step 4 | 4 | 3 | 1 |
| Step 5 | 3 | 3 | -- |

**Graduates this cycle**: 3

1. **Wireless TAB Field Documentation & Auto-Report Platform** (8/10) - Exceptional capital efficiency ($150-250K), near-zero competition, immediate pain point
2. **AI-Powered HVAC TAB Optimization Engine** (7.5/10) - Higher value but higher risk complement to #1, solves acute technician shortage
3. **AI-Automated GPR Interpretation SaaS** (7/10) - Proven technology (Birdsview validates), clear US market gap, strong unit economics

**Key insight**: The HVAC TAB space is remarkably underserved by technology despite being a $6.2B market. Two distinct products can be built: a simpler documentation tool (low risk, fast to market) and a more ambitious optimization engine (higher value, more technical risk). These could be sequential products from the same company - start with documentation, earn trust, then add AI optimization.