# Cycle 034 Report

**Date**: 2026-06-08
**Domains explored**: Electric cooperative demand forecasting, solar soiling detection, vegetation management AI, wind turbine predictive maintenance, EV charging infrastructure maintenance, cooperative outage prediction, solar inverter analytics for mid-size operators, cooperative coincident peak management, small wind farm wake optimization, EV charger component diagnostics

---

## Step 1: Technology Discovery

### 1. AI Vegetation Management for Power Lines
- **Domain**: Utility vegetation management
- **Breakthrough**: Satellite + LiDAR AI fusion for tree growth prediction and encroachment risk scoring (2024-2025)
- **TRL**: 8
- **Time to product**: 3-6 months
- **Status**: REJECTED
- **Reasoning**: Extremely competitive. Overstory serves 6 of top 10 US utilities plus 50+ IOUs/cooperatives. Buzz Solutions serves New York Power Authority, Southern California Edison, Ameren. Astraea/NUVIEW adding LiDAR satellite constellation. Competitive density: 5. No viable differentiation angle for a new entrant.

### 2. Solar Farm Soiling Detection AI
- **Domain**: Solar O&M optimization
- **Breakthrough**: PV reference cell sensors + ML cleaning schedule optimization (FracSun NX Clario, 2024)
- **TRL**: 8
- **Time to product**: 3-6 months
- **Status**: REJECTED
- **Reasoning**: Well-served market. FracSun (acquired by Nextpower/NXT) sells hardware sensors. Solcast provides soiling loss modeling via API. SenseHawk uses AI drone IR scans. Raptor Maps offers comprehensive visual analytics. Zeitview (formerly Heliolytics) provides AI drone inspection. Competitive density: 5. Requires hardware differentiation which conflicts with winning archetype.

### 3. Wind Turbine Gearbox Predictive Maintenance
- **Domain**: Wind farm O&M
- **Breakthrough**: Vibration + SCADA data fusion with transformer-based anomaly detection (2024-2025)
- **TRL**: 7
- **Time to product**: 6-9 months
- **Status**: REJECTED
- **Reasoning**: Heavily saturated. WindESCo (Pulse analytics + eCMS monitoring), Clir Renewables (350+ GW analyzed), Power Factors/Inaccess (600+ customers, REMI AI platform), Bazefield (SSE Renewables, Invenergy 25GW). OEMs (Siemens Gamesa, Vestas, GE) bundle their own. Competitive density: 5. Independent operators already well-served by multiple vendors.

### 4. EV Charging Station Predictive Maintenance
- **Domain**: EV charging infrastructure
- **Breakthrough**: OCPP telemetry + ML failure prediction for charger components (2025)
- **TRL**: 7
- **Time to product**: 6-9 months
- **Status**: REJECTED
- **Reasoning**: ChargeLab has launched "Spark AI" - the industry's first proactive AI that fixes problems before operators notice (15,000+ chargers managed). EV Connect monitors 29,000+ chargers with 24/7 intelligent monitoring. ChargePoint dominates as market leader. EvGateway provides turn-key remote management. Competitive density: 4. First-mover advantage already claimed by ChargeLab.

### 5. Cooperative Coincident Peak Demand Management
- **Domain**: Electric cooperative cost optimization
- **Breakthrough**: Edge ML on AMI meters + weather correlation for cooperative wholesale demand charge avoidance (2025-2026)
- **TRL**: 6
- **Time to product**: 6-9 months
- **Status**: PROMOTED
- **Reasoning**: Electric cooperatives pay wholesale power suppliers (G&Ts) based on their load during the supplier's system peak hours (coincident peak). Missing these peaks costs cooperatives $2-15/kW/month. Existing solutions (Bidgely at 38M meters, GridX, Recurve) target large IOUs with $500K+ deployments. No affordable AI tool specifically helps the ~900 US distribution cooperatives (typically 5K-100K meters each) predict and shed load during G&T coincident peaks. NISC provides legacy ERP but no AI forecasting. The gap is a lightweight SaaS that ingests cooperative AMI data + weather to predict coincident peak windows and trigger automated demand response.

### 6. Solar Inverter Degradation Analytics for Mid-Size Independent Owners
- **Domain**: Solar O&M for 5-50MW operators
- **Breakthrough**: String-level IV curve analysis via existing inverter telemetry + ML degradation models (2025)
- **TRL**: 6
- **Time to product**: 6-9 months
- **Status**: PROMOTED
- **Reasoning**: Power Factors (600+ customers, GW-scale), Clir, and SenseHawk serve large portfolios with enterprise pricing ($50-200K/year). Mid-size independent solar owners (5-50MW, single site) typically use basic OEM monitoring (Sungrow iSolarCloud, SolarEdge monitoring) that shows real-time production but lacks predictive degradation analytics. There is a gap for a $500-2000/month SaaS that ingests existing inverter telemetry (via Modbus/API) and provides module-level degradation prediction, warranty claim evidence, and cleaning/maintenance ROI modeling without requiring additional hardware.

### 7. Cooperative Outage Prediction from AMI + Weather
- **Domain**: Small utility reliability management
- **Breakthrough**: Lightweight ML combining AMI last-gasp signals + weather radar + vegetation/pole age data for outage probability mapping (2025-2026)
- **TRL**: 6
- **Time to product**: 9-12 months
- **Status**: PROMOTED
- **Reasoning**: DTN provides weather intelligence for large utilities. Sentient Energy (now defunct/acquired) offered grid sensors. But cooperatives with 50-500 miles of distribution line lack affordable outage prediction tools. Current process: wait for customer calls, dispatch crews blind. AMI meters already send "last gasp" signals when power drops. A SaaS combining these signals with NWS radar, GIS pole data, and historical failure patterns could predict which feeders will fail before storms hit. No product specifically serves this niche at cooperative budgets.

### 8. Small Wind Farm Wake Steering Optimization
- **Domain**: Independent wind farm operators (single sites, 10-50 turbines)
- **Breakthrough**: Real-time LiDAR-free wake modeling using SCADA + met mast data with reinforcement learning yaw control (2025)
- **TRL**: 6
- **Time to product**: 9-12 months
- **Status**: REJECTED
- **Reasoning**: WindESCo's Swarm product specifically offers "cooperative control technology enabling turbines to collaborate, including wake steering and predictive yaw." While they may not penetrate every small operator, the technology exists and is commercialized. Academic research (NREL FLORIS, DTU) is freely available. The combination of existing commercial product + open-source tools makes this hard to differentiate. Competitive density: 3, but the technical barrier to real AEP improvement (1-3%) vs. risk of blade loads makes the ROI case weak for small operators.

### 9. EV Charger Connector Wear Monitoring via Computer Vision
- **Domain**: EV charging infrastructure maintenance
- **Breakthrough**: Edge camera + CNN for CCS/CHAdeMO connector pin degradation, cable fraying, and thermal damage detection (2025)
- **TRL**: 5
- **Time to product**: 12-18 months
- **Status**: REJECTED
- **Reasoning**: TRL 5 fails the minimum TRL 6 threshold. Requires novel hardware deployment (cameras at each charger). ChargeLab's software-only Spark AI approach is already solving the uptime problem without hardware additions. The connector wear problem is real but the solution requires hardware at every stall, which conflicts with the winning archetype (software intelligence + commodity hardware). Capital would be $2M+ to develop and deploy. REJECT.

### 10. Cooperative DER Curtailment Optimization
- **Domain**: Electric cooperative distributed energy resource management
- **Breakthrough**: ML-based hosting capacity analysis using AMI voltage data + rooftop solar production curves for dynamic curtailment scheduling (2025-2026)
- **TRL**: 6
- **Time to product**: 9-12 months
- **Status**: PROMOTED
- **Reasoning**: As rooftop solar penetration increases in cooperative territories, reverse power flow causes voltage violations on rural feeders. Large utilities use DERMS platforms ($500K-2M from vendors like AutoGrid, now Schneider). Camus Energy offers FlexConnect for interconnection but targets utility-scale DER and large utilities. No affordable tool exists for cooperatives to dynamically manage growing rooftop solar on thin rural feeders without expensive grid upgrades. A SaaS ingesting AMI voltage telemetry + solar production data could optimize curtailment schedules to maximize member solar export while preventing voltage violations.

---

## Step 2: Competitive Analysis

### Cooperative Coincident Peak Demand Management
- **Competitors found**: Recurve (demand flexibility, not cooperative-specific), GridX (rate engine for large IOUs), Bidgely (38M meters, enterprise scale), Virtual Peaker (demand response but $100K+ implementations targeting large utilities), NISC (legacy ERP, no AI forecasting), Tendril/Uplight (home energy management for large IOUs)
- **Competitive density score**: 2
- **Differentiation angle**: Purpose-built for cooperative G&T coincident peak avoidance. $2-5K/month SaaS (not $100K+ enterprise deployments). Pre-built integrations with NISC and cooperative AMI vendors (Landis+Gyr, Itron). Automated member notification + thermostat/water heater control via existing demand response switches.
- **Status**: PROMOTED
- **Reasoning**: The key differentiator is the go-to-market: cooperatives are a tight-knit community (NRECA conferences, regional G&T associations). Enterprise DERMS/DR platforms are overbuilt and overpriced for a 20,000-meter cooperative. The coincident peak problem is highly specific to cooperatives (IOUs don't have G&T wholesale charges the same way). A lean team can build an MVP that predicts 4CP/12CP windows and triggers existing load control relays. Low competitive density in the cooperative-specific niche.

### Solar Inverter Degradation Analytics for Mid-Size Independent Owners
- **Competitors found**: Power Factors/REMI (enterprise, 600+ customers at GW scale), SolarAnywhere (data/forecasting, not degradation prediction), Raptor Maps (drone inspection-based), SenseHawk (construction-to-operations, AI IR scans), Also Energy/Stem (monitoring but basic alerting), OEM tools (SolarEdge, Enphase, Sungrow built-in monitoring)
- **Competitive density score**: 3
- **Differentiation angle**: Pure software analytics layer that sits on top of existing OEM monitoring APIs. No hardware, no drones, no inspections needed. Focuses specifically on string-level degradation trajectory prediction (when will this string drop below warranty threshold?) and automated warranty claim documentation. $500-2000/month vs. $50-200K/year enterprise platforms.
- **Status**: PROMOTED
- **Reasoning**: While solar monitoring is crowded at the enterprise level, mid-size independent owners (community solar, single-site developers) are underserved by tools that predict future degradation rather than just alerting on current faults. The warranty claim automation angle is unique - helping owners document degradation evidence to make claims against module manufacturers before warranty expiration. OEM monitoring shows real-time status but lacks predictive degradation curves.

### Cooperative Outage Prediction from AMI + Weather
- **Competitors found**: DTN WeatherSentry Utility Edition (storm tracking for large utilities, not cooperative-specific), Oracle/Milsoft (outage management systems, reactive not predictive), Buzz Solutions (post-event assessment via drones), Overstory (vegetation risk but $200K+ for large utilities), GridCure (appears defunct)
- **Competitive density score**: 2
- **Differentiation angle**: Lightweight predictive (not reactive) outage risk scoring specifically for cooperative-scale distribution systems. Ingests existing AMI last-gasp data + NWS feeds + cooperative GIS data. No additional sensors or drones required. $3-8K/month SaaS vs. $200K+ enterprise OMS upgrades.
- **Status**: PROMOTED
- **Reasoning**: Cooperatives currently have OMS (Outage Management Systems) from NISC or Milsoft that track outages reactively. DTN provides weather warnings but not feeder-specific outage probability. The gap is a predictive layer that says "Feeder 12 has 73% outage probability in next 4 hours based on wind speed + tree proximity + pole age + historical failure pattern" enabling pre-positioning of crews. Low competitive density for this specific cooperative segment.

### Cooperative DER Curtailment Optimization
- **Competitors found**: Camus Energy (FlexConnect, but targets utility-scale interconnection for large utilities/Google), Schneider/AutoGrid (enterprise DERMS, $500K-2M), GridBeyond (demand response, but industrial focus), Hive Power (VPP/community energy but European market), Recurve (demand flexibility, not DER curtailment)
- **Competitive density score**: 2
- **Differentiation angle**: Cooperative-specific DERMS-lite. Uses existing AMI voltage data to identify feeders approaching hosting capacity limits. Automated 1547.1-compliant curtailment schedules communicated to member inverters via SunSpec Modbus or smart inverter protocols. $3-6K/month vs. $500K+ full DERMS.
- **Status**: PROMOTED
- **Reasoning**: Full DERMS platforms are architected for utilities with 500K+ meters and complex wholesale market participation. Cooperatives need a simpler tool: "which feeders have voltage problems from solar, and how much can each member export right now?" The IEEE 1547-2018 mandate for smart inverter capabilities (Volt-VAR, Volt-Watt) means the inverter-side control is standardized. The missing piece is the analytics layer that determines optimal setpoints per feeder.

---

## Step 3: Market Analysis

### CoopPeak - Cooperative Coincident Peak Avoidance SaaS
- **Target market**: US electric distribution cooperatives (approximately 900 cooperatives serving 42 million members). Specifically, cooperatives purchasing wholesale power from G&T cooperatives that charge demand-based rates on coincident peak contribution.
- **TAM**: 900 cooperatives x $60K avg annual value of avoided peak charges = $54M addressable immediately. With demand response integration expanding to rate optimization: $150M.
- **SAM**: 400 cooperatives in top-10 G&Ts with highest demand charges (ACES, Buckeye, East Kentucky, Basin Electric, etc.) x $48K/year = $19.2M
- **Revenue model**: SaaS subscription $3-5K/month based on cooperative size (meters). Performance bonus: 10% of documented peak charge savings above baseline.
- **Status**: PROMOTED
- **Reasoning**: Conservative SAM of $19M is achievable. Cooperatives save $50-200K/year in avoided coincident peak demand charges (at $2-15/kW/month for peaks they can shed 500-2000kW). The tool pays for itself 3-10x in year one. Cooperative buying patterns favor peer-referral (NRECA statewide associations). Single G&T could mandate adoption across member cooperatives.

### InverterIQ - Solar Inverter Degradation Prediction for Mid-Size Owners
- **Target market**: Independent solar asset owners with 5-50MW portfolios. Community solar operators, single-site developers, small IPPs. US market: approximately 3,000 such entities managing 80GW+.
- **TAM**: 3,000 operators x $24K avg annual subscription = $72M. Adding warranty claim recovery services: $200M.
- **SAM**: 800 operators in states with strong community solar programs (MN, NY, MA, CO, IL, ME) x $18K/year = $14.4M
- **Revenue model**: SaaS $1,000-2,500/month per site based on MW capacity. Premium tier adds warranty claim documentation service at 15% of recovered claim value.
- **Status**: PROMOTED
- **Reasoning**: Mid-size solar owners lose 1-3% annual production to undetected degradation. On a 10MW site generating $1.5M/year, that is $15-45K in lost revenue. A $24K/year tool that identifies degradation 6-12 months earlier and provides warranty claim evidence has clear ROI. The warranty claim angle is particularly compelling: module manufacturers often deny claims without granular string-level degradation documentation.

### StormReady Co-op - Cooperative Outage Prediction SaaS
- **Target market**: US electric distribution cooperatives, especially those in severe weather corridors (Southeast, Midwest, Great Plains). 600+ cooperatives with AMI deployments.
- **TAM**: 600 cooperatives x $72K avg annual subscription = $43M. Including avoided SAIDI penalty costs and crew optimization savings: $100M+.
- **SAM**: 250 cooperatives in high-storm-frequency regions with AMI deployed x $60K/year = $15M
- **Revenue model**: SaaS subscription $4-8K/month based on service territory size and meter count. Additional module for automated crew dispatch optimization at $2K/month.
- **Status**: PROMOTED
- **Reasoning**: Cooperatives in storm-prone regions spend $500K-2M annually on storm restoration. Pre-positioning crews 2-4 hours before outages hit could reduce restoration time by 25-40%, saving $125-800K/year per cooperative. The tool pays for itself even with conservative 10% improvement in restoration costs. SAIDI/SAIFI metrics directly affect cooperative board satisfaction and regulatory compliance.

### CoopSolar Manager - Cooperative DER Curtailment Optimization
- **Target market**: US electric cooperatives experiencing rooftop solar growth on rural feeders. Approximately 400 cooperatives with >2% solar penetration facing hosting capacity constraints.
- **TAM**: 400 cooperatives x $54K avg annual subscription = $21.6M. Growing rapidly as solar penetration increases.
- **SAM**: 150 cooperatives in high-solar states (AZ, NM, CO, CA, NC, TX, FL) already experiencing voltage issues x $48K/year = $7.2M
- **Revenue model**: SaaS subscription $3-6K/month. Additional interconnection study module at $5K per new solar application.
- **Status**: REJECTED
- **Reasoning**: While the technology is feasible, the SAM of $7.2M is too small for a standalone business today. Solar penetration in cooperative territories is growing but most cooperatives are still at <2% penetration. The problem is real but premature for most of the addressable market. Additionally, IEEE 1547-2018 implementation timelines vary by state, creating regulatory fragmentation. Timing risk is high. The market will exist in 3-5 years but is not large enough today.

---

## Step 4: Feasibility Analysis

### CoopPeak - Cooperative Coincident Peak Avoidance SaaS
- **Technical risk**: Low - AMI data ingestion is standardized (NISC API, Itron/Landis+Gyr data exports). Weather correlation models are well-established. Load control relay triggering uses existing cooperative infrastructure (Tantalus, Eaton demand response switches already deployed at many cooperatives).
- **Market risk**: Low - Cooperatives have an immediate, quantifiable pain point (demand charges are their largest single expense, 40-60% of wholesale power cost). The ROI calculation is straightforward and verifiable against G&T billing statements.
- **Execution risk**: Low - Two-person team (ML engineer + cooperative utility domain expert) can build MVP in 4-6 months. No hardware needed. Integration with NISC (dominant cooperative CIS) provides distribution channel.
- **Timing risk**: Low - AMI deployment at cooperatives reached 70%+ penetration in 2024-2025. The data infrastructure exists now. Demand charges are increasing as renewable intermittency grows on G&T systems.
- **Capital required**: $200-350K (6 months dev + 3 pilot cooperatives + NRECA conference presence)
- **Feasibility score**: 8.5/10
- **Status**: PROMOTED
- **Reasoning**: Textbook fit for the winning archetype. Software intelligence on existing AMI infrastructure. Replaces expensive enterprise DERMS ($500K+) with focused SaaS ($36-60K/year) for 10x larger cooperative market. Immediate, measurable ROI (avoided demand charges appear on monthly G&T bills). No regulatory barriers. Tight community enables viral adoption through statewide associations.

### InverterIQ - Solar Inverter Degradation Prediction for Mid-Size Owners
- **Technical risk**: Medium - Inverter telemetry quality varies significantly across manufacturers. Sungrow, SolarEdge, and Enphase have good APIs; others require Modbus scraping. Degradation models need 12-18 months of historical data to calibrate accurately per site.
- **Market risk**: Low-Medium - Clear pain point but customer discovery may be challenging (fragmented market of small independent owners). Warranty claim value proposition is compelling but requires proving the analytics hold up in manufacturer disputes.
- **Execution risk**: Medium - Requires partnerships with or reverse-engineering of multiple inverter OEM APIs. Each manufacturer is a separate integration effort. Customer acquisition requires reaching fragmented independent owners.
- **Timing risk**: Low - Module degradation and warranty claims are perennial issues. First wave of community solar (2018-2020 installations) is now 5-8 years old, entering peak warranty claim territory.
- **Capital required**: $300-500K (8 months dev for multi-OEM integration + data science + 5 pilot sites + first-year operations)
- **Feasibility score**: 7/10
- **Status**: PROMOTED
- **Reasoning**: Good fit for winning archetype but higher execution complexity due to OEM API fragmentation. The warranty claim angle provides immediate tangible value (recovered revenue from manufacturers). Medium technical risk from integration complexity is manageable but extends time to market vs. CoopPeak.

### StormReady Co-op - Cooperative Outage Prediction SaaS
- **Technical risk**: Medium - Correlating AMI last-gasp signals with weather radar and GIS data requires geospatial ML that performs well with cooperative-scale training data (limited historical events per feeder). False positive rate must be low or crews will ignore predictions.
- **Market risk**: Low - Cooperatives universally cite storm restoration cost and SAIDI as top concerns. Board members face member complaints directly (cooperative governance structure).
- **Execution risk**: Medium - Requires integration with multiple AMI vendors (NISC head-end, Tantalus, Itron) plus NWS weather feeds plus cooperative GIS systems (multiple vendors). Each cooperative's data infrastructure is slightly different.
- **Timing risk**: Low - Storm severity and frequency increasing due to climate change. Cooperatives in Southeast/Midwest experiencing record restoration costs 2023-2025.
- **Capital required**: $350-500K (8 months dev + geospatial ML expertise + 3-5 pilot cooperatives + data pipeline infrastructure)
- **Feasibility score**: 7/10
- **Status**: PROMOTED
- **Reasoning**: Strong market pull and clear ROI, but higher technical complexity than CoopPeak. The ML model needs sufficient historical outage data to train, which may require 6-12 months of data collection at pilot sites before prediction accuracy is compelling. Slightly longer path to revenue than CoopPeak but larger per-customer value once proven.

---

## Step 5: Execution Summary

### CoopPeak - Cooperative Coincident Peak Avoidance SaaS (Feasibility: 8.5/10)
- **Product**: Cloud SaaS that ingests cooperative AMI meter data and G&T system load signals, predicts coincident peak windows 2-24 hours in advance using weather-correlated load forecasting, and automatically triggers existing demand response infrastructure (load control relays, smart thermostats, water heater switches) to shed cooperative load during G&T system peaks. Dashboard shows real-time peak probability, historical savings, and member participation metrics.
- **Technology**: Time-series ML (weather-correlated load forecasting), integration with NISC CIS/billing APIs, AMI head-end connections (Landis+Gyr, Itron), existing demand response relay protocols. No novel hardware.
- **Market**: 900 US distribution cooperatives, starting with 10-20 cooperatives in 2-3 G&T territories with highest demand charges (Basin Electric, East Kentucky Power, ACES). Land-and-expand via G&T mandates and statewide association referrals.
- **Revenue model**: $3-5K/month SaaS subscription + 10% performance bonus on documented peak charge savings above baseline. Target ACVs of $48-72K/year.
- **Capital**: $200-350K for MVP + 3 pilots over 9 months
- **Key strength**: Immediate, verifiable ROI (savings appear on next month's G&T bill). Tight cooperative community enables rapid word-of-mouth. No hardware or regulatory barriers. Problem is unique to cooperatives (no large-utility competition).
- **Key risk**: Cooperative technology adoption can be slow (conservative boards). Mitigated by partnering with forward-thinking G&Ts who can mandate/subsidize adoption across member cooperatives.

### InverterIQ - Solar Inverter Degradation Prediction (Feasibility: 7/10)
- **Product**: Analytics SaaS that connects to existing solar inverter monitoring APIs (SolarEdge, Enphase, Sungrow, Huawei), ingests string-level production data, and applies ML degradation models to predict module-level performance decline trajectories. Automatically generates warranty claim documentation packages with evidence of degradation rates exceeding manufacturer specifications. Dashboard shows per-string health scores, predicted annual energy loss, and optimal maintenance scheduling.
- **Technology**: Time-series anomaly detection on inverter telemetry, physics-informed ML degradation models (PVsyst-validated), automated report generation. Integrations via manufacturer APIs and Modbus/SunSpec protocols.
- **Market**: 3,000+ independent mid-size solar operators (5-50MW) in the US. Initial focus on community solar operators in MN, NY, MA, CO, IL where portfolio fragmentation is highest. Secondary market: O&M contractors managing multiple independent sites.
- **Revenue model**: $1,000-2,500/month per site (based on MW). Premium warranty claim service at 15% of recovered claim value. Target ACV $18-30K.
- **Capital**: $300-500K for multi-OEM integration, ML model development, and 5 pilot sites over 10 months
- **Key strength**: Warranty claim revenue recovery provides immediate cash value to customers (often $50-200K per site over module lifetime). Growing market as early community solar installations age into warranty claim windows.
- **Key risk**: OEM API access may be restricted or unreliable. Some manufacturers may resist providing data that facilitates claims against them. Mitigated by focusing on Modbus/SunSpec direct data collection where API access is limited.

### StormReady Co-op - Cooperative Outage Prediction SaaS (Feasibility: 7/10)
- **Product**: Predictive outage risk platform that combines cooperative AMI last-gasp event data, NWS weather radar/forecast feeds, GIS infrastructure data (pole age, conductor type, vegetation proximity), and historical outage records to generate feeder-level outage probability maps 2-12 hours before storms. Includes crew pre-positioning recommendations and automated member notification workflows.
- **Technology**: Geospatial ML combining time-series weather data with graph neural networks modeling feeder topology. AMI head-end integrations (NISC, Tantalus). NWS API for radar/warnings. GIS integration via cooperative mapping systems.
- **Market**: 600+ US cooperatives with AMI deployments, starting with 20-30 cooperatives in tornado alley and hurricane corridor where storm restoration costs exceed $1M/year.
- **Revenue model**: $4-8K/month SaaS subscription based on territory size. Add-on crew dispatch optimization module at $2K/month. Target ACV $60-96K.
- **Capital**: $350-500K for geospatial ML development, AMI integrations, and 3-5 pilot cooperatives over 12 months
- **Key strength**: Directly reduces cooperatives' largest uncontrolled cost (storm restoration). Increasing storm frequency creates growing urgency. Visible board-level metric improvement (SAIDI/SAIFI).
- **Key risk**: ML model requires sufficient historical outage data to train accurately. First 6-12 months at each pilot may show limited prediction accuracy until model calibrates to local conditions. Mitigated by starting in high-storm-frequency territories where training events are plentiful.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 4 | 6 |
| Step 2 | 4 | 4 | 0 |
| Step 3 | 4 | 3 | 1 |
| Step 4 | 3 | 3 | 0 |
| Step 5 | 3 | 3 | — |

---

## Key Findings

**Dominant pattern this cycle**: The electric cooperative market represents a significant underserved segment. While large IOU utilities are well-served by enterprise vendors (Bidgely, DTN, Power Factors, Overstory), the 900 US distribution cooperatives are stuck between legacy vendors (NISC) and overpriced enterprise platforms. The cooperative-specific coincident peak problem is particularly compelling because it has no direct analog in IOU operations and thus no existing solution specifically targeting it.

**Top graduate**: CoopPeak (8.5/10) is the strongest idea this cycle. It perfectly matches the winning archetype: software intelligence on existing AMI infrastructure, no hardware, $200-350K capital, immediate measurable ROI (next month's G&T bill), and a tight community enabling viral distribution.

**Heavily competed domains (confirmed REJECT)**: Vegetation management AI (Overstory dominates), solar soiling detection (FracSun/Nextpower + 4 others), wind farm predictive maintenance (5+ well-funded players), EV charging predictive maintenance (ChargeLab first-mover). All have competitive density of 4-5 with $100M+ funded incumbents.

**Validated gap**: No AI-first company specifically targets electric cooperatives with affordable, purpose-built tools. The cooperative technology market is served by legacy vendors (NISC for ERP, Milsoft for engineering) but lacks modern ML-powered optimization tools priced for cooperative budgets ($3-8K/month vs. $50-200K/year enterprise).