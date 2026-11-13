Good, I understand the format. Now let me produce the full Cycle 024 report based on my research. The key findings from my competitive research are:

1. **Powder coating AI** - CoatingAI, AkzoNobel/Flightpath, Coatmaster, Pellex ERP, Codeison, Powder-X = 6 competitors = REJECT
2. **Welding AI robots** - Path Robotics ($100M+), MANUFAI, SmartWeld = many players = careful analysis needed
3. **Commercial laundry** - Inwatec (sorting robots), LaundryOS (business SaaS), Samsung (consumer AI) = different niches, some gaps remain
4. **Industrial painting** - Large incumbents dominate (Durr, ABB, Fanuc) = REJECT for robotics, but sub-niches may exist

# Cycle 024 Report

**Date**: 2026-06-08
**Domains explored**: Commercial laundry soil classification, Laundry water recycling optimization, Linen lifetime prediction, Industrial wet paint thickness prediction, Powder coating color-change optimization, Powder coating recovery efficiency, Welding shielding gas waste monitoring, Welding consumable inventory optimization, Industrial spray booth airflow optimization, Coating cure monitoring

---

## Step 1: Technology Discovery

### 1. NIR-Based Laundry Soil Classification Sensor
- **Domain**: Commercial laundry operations
- **Breakthrough**: Low-cost NIR spectroscopy chips (sub-$50 per sensor, e.g., Texas Instruments DLP NIRscan Nano) combined with edge ML can now classify soil types (protein, oil, mineral, blood) on textiles in real-time, enabling automated wash cycle selection and chemical dosing optimization
- **TRL**: 7 (NIR textile analysis proven in recycling/sorting; application to soil classification is novel recombination)
- **Time to product**: 8-12 months
- **Status**: PROMOTED
- **Reasoning**: Commodity NIR sensors + ML classification fits the winning archetype. Samsung has consumer AI Wash+ (turbidity only), but no commercial/industrial NIR soil-type classification exists. Mid-market commercial laundries (hotels, hospitals, uniforms) spend 15-25% of operating costs on chemicals, often over-dosing because they cannot distinguish soil types.

### 2. Laundry Water Recycling AI Optimizer
- **Domain**: Commercial laundry water management
- **Breakthrough**: Multi-sensor arrays (turbidity, pH, conductivity, temperature) combined with ML models can predict optimal water reuse ratios per wash stage, maximizing recycling while maintaining wash quality
- **TRL**: 6-7 (sensors are commodity; ML water quality prediction proven in wastewater treatment)
- **Time to product**: 10-14 months
- **Status**: PROMOTED
- **Reasoning**: Commercial laundries use 3-6 gallons per pound of textiles. Water recycling systems exist but are rule-based (fixed turbidity thresholds). AI-optimized recycling that adapts to soil load, fabric type, and chemical concentration is a novel software layer on existing hardware.

### 3. RFID + ML Linen Lifetime Prediction
- **Domain**: Commercial laundry asset management
- **Breakthrough**: UHF RFID tags (now $0.05-0.15 per tag) combined with wash-cycle data logging and ML wear prediction models can predict individual linen item replacement timing, reducing catastrophic failures and optimizing procurement
- **TRL**: 7 (RFID linen tracking exists; adding ML lifetime prediction is novel)
- **Time to product**: 6-10 months
- **Status**: PROMOTED
- **Reasoning**: RFID linen tracking is established (companies like Datamars, Positek RFID), but pure tracking without predictive analytics. Adding ML wear models (correlating wash count, chemical exposure, temperature history, fabric type) to predict replacement timing is a software-only addition to existing RFID infrastructure.

### 4. Wet-to-Dry Film Thickness Prediction (Industrial Painting)
- **Domain**: Industrial painting/coating
- **Breakthrough**: Inline optical sensors measuring wet film thickness combined with ML models predicting final dry film thickness (DFT) in real-time, before curing. Enables immediate correction rather than post-cure reject/rework
- **TRL**: 6 (wet film measurement exists; ML wet-to-dry prediction is novel application of transfer learning from coating physics models)
- **Time to product**: 12-16 months
- **Status**: PROMOTED
- **Reasoning**: Current practice: spray, cure, measure DFT, rework if out-of-spec. Rework rates are 5-15% in automotive/industrial painting. Predicting DFT from wet measurements (accounting for solvent evaporation, cure shrinkage, substrate effects) before curing eliminates most rework. Coatmaster measures post-cure; this predicts pre-cure.

### 5. Powder Coating AI Optimization (Color Change + Thickness)
- **Domain**: Powder coating
- **Breakthrough**: AI-driven parameter optimization for powder coating lines using real-time sensors and machine learning
- **TRL**: 8 (products already on market)
- **Time to product**: Already available
- **Status**: REJECTED
- **Reasoning**: Extremely high competitive density. CoatingAI (Switzerland, deployed on "hundreds of lines"), AkzoNobel Flightpath, Coatmaster (2,000+ systems), Pellex ERP, Codeison, and Powder-X all offer AI/ML powder coating optimization. Competitive density score: 6/5. No viable entry point.

### 6. Welding Shielding Gas Flow Monitoring + AI Waste Reduction
- **Domain**: Welding consumable optimization
- **Breakthrough**: Low-cost MEMS flow sensors ($5-15) + edge ML detecting gas waste events (surge at arc start, leaks, operator over-flow) in real-time, providing per-station analytics and optimization recommendations
- **TRL**: 7 (MEMS flow sensors mature; application to per-station welding gas analytics with ML is novel)
- **Time to product**: 8-12 months
- **Status**: PROMOTED
- **Reasoning**: GasIQ (Sweden) makes the Optimator mechanical regulator (reduces waste 60%) but is hardware-only, no data/analytics. WITT makes gas mixers with basic internet connectivity. Neither offers per-station ML analytics showing waste patterns, operator behavior, and optimization recommendations as SaaS. The gap is the intelligence layer.

### 7. Welding Consumable Inventory + Usage Prediction SaaS
- **Domain**: Welding operations management
- **Breakthrough**: IoT sensors on wire feeders, electrode ovens, and gas manifolds combined with ML to predict consumable usage, automate reordering, and identify waste patterns across multi-station fabrication shops
- **TRL**: 7 (IoT inventory management proven in other verticals; novel in welding-specific application)
- **Time to product**: 8-12 months
- **Status**: PROMOTED
- **Reasoning**: WeldAssistant offers consumable database/selection. WeldIQ offers code compliance. SmartWeld offers monitoring. None specifically solve the consumable inventory prediction + automated procurement problem for mid-size fab shops (20-100 welding stations) that currently track via spreadsheets and experience stockouts or overstock.

### 8. Spray Booth Airflow Optimization (Paint Overspray Capture)
- **Domain**: Industrial painting
- **Breakthrough**: CFD-informed ML models + IoT airflow sensors optimizing booth exhaust/supply air patterns in real-time to maximize overspray capture, reduce filter consumption, and lower energy costs
- **TRL**: 5-6 (CFD modeling mature; real-time adaptive airflow control in spray booths is novel but requires custom actuator integration)
- **Time to product**: 14-18 months
- **Status**: REJECTED
- **Reasoning**: TRL too low (5-6). Requires integration with booth HVAC actuators which vary enormously across installations. Capital-intensive hardware retrofit. Large incumbents (Durr, Eisenmann) control booth infrastructure. Not software-first.

### 9. Coating Cure Monitoring (Inline Thermal + ML)
- **Domain**: Industrial coating quality
- **Breakthrough**: Inline IR thermal cameras + ML models predicting cure quality from thermal profiles in real-time during oven transit, detecting under-cure or over-cure before parts exit
- **TRL**: 6-7 (thermal imaging for cure monitoring exists in research; Coatmaster uses thermal optics for thickness; novel application to cure quality prediction)
- **Time to product**: 10-14 months
- **Status**: PROMOTED
- **Reasoning**: Under-cured coatings cause field failures (adhesion loss, corrosion). Over-cured coatings waste energy and can yellow. Current practice: destructive testing on samples. Inline thermal ML prediction enables 100% inspection. Differentiated from Coatmaster (which measures thickness, not cure state).

### 10. Laundry Chemical Dosing AI (Closed-Loop Optimization)
- **Domain**: Commercial laundry operations
- **Breakthrough**: Multi-parameter sensors (pH, ORP, conductivity, turbidity, temperature) combined with ML models optimizing chemical dosing in real-time based on actual soil load, water hardness, and fabric type rather than fixed recipes
- **TRL**: 7 (sensors commodity; ML dosing optimization proven in water treatment; novel in laundry-specific application)
- **Time to product**: 8-12 months
- **Status**: PROMOTED
- **Reasoning**: Ecolab, Diversey, and Christeyns sell chemical dosing systems but use rule-based dispensers (fixed volume per cycle type). No adaptive ML optimization exists that adjusts dosing based on real-time sensor feedback during the wash cycle. The gap is "smart" vs "programmed" dosing.

---

## Step 2: Competitive Analysis

### NIR-Based Laundry Soil Classification Sensor
- **Competitors found**: Samsung AI Wash+ (consumer only, turbidity-based not NIR), Girbau (general smart laundry controls, no soil classification), Inwatec (sorting automation, not soil analysis), Kannegiesser (tunnel washers with basic sensors)
- **Competitive density score**: 2/5 (no direct competitor in commercial NIR soil classification)
- **Differentiation angle**: First NIR spectroscopic soil-type classifier for commercial laundry enabling per-load chemical optimization (vs. turbidity-only consumer products)
- **Status**: PROMOTED
- **Reasoning**: Clear white space. Samsung's consumer AI Wash uses turbidity (water cloudiness) as a proxy for soil level, not soil type. Commercial laundries need to distinguish protein (blood, food) from mineral (clay, rust) from oil (grease, petroleum) because each requires different chemistry. No existing commercial system does spectroscopic soil typing.

### Laundry Water Recycling AI Optimizer
- **Competitors found**: Aqua Recycling GmbH (German company, hardware water recycling systems), Ecowash (basic water recycling), various OEM water recycling systems built into tunnel washers
- **Competitive density score**: 3/5 (hardware recycling exists; AI optimization layer does not)
- **Differentiation angle**: Software layer that maximizes existing recycling hardware performance through ML-based water quality prediction
- **Status**: PROMOTED
- **Reasoning**: Water recycling hardware exists but operates on fixed thresholds. An AI optimization layer that sits on top of existing recycling systems (retrofit) could increase water recovery rates by 20-40% without hardware changes. However, the market is narrower (only laundries with existing recycling systems or considering installation).

### RFID + ML Linen Lifetime Prediction
- **Competitors found**: Datamars (RFID linen tracking, major player), Positek RFID (tracking), Bundle Laundry (tracking), RFID4U (general RFID), Metrc (cannabis tracking, not laundry)
- **Competitive density score**: 4/5 (RFID tracking is crowded; ML prediction is differentiation but Datamars could add it easily)
- **Differentiation angle**: Predictive analytics layer on top of RFID data (which is just tracking today)
- **Status**: REJECTED
- **Reasoning**: Datamars is a well-funded, dominant player in laundry RFID with deep customer relationships. They could add ML prediction to their existing platform as a feature update. Entering this space means competing with an entrenched incumbent who has the data advantage (they already collect wash cycle data). Competitive density too high for a startup entry.

### Wet-to-Dry Film Thickness Prediction
- **Competitors found**: Coatmaster (post-cure non-contact thickness), ElektroPhysik (traditional gauges), BYK-Gardner (quality instruments), Fischer (thickness measurement)
- **Competitive density score**: 2/5 (all competitors measure actual thickness post-cure; none predict DFT from wet measurement pre-cure)
- **Differentiation angle**: Predictive pre-cure thickness eliminates rework before curing step (unique position in the workflow)
- **Status**: PROMOTED
- **Reasoning**: Clear differentiation. Coatmaster's 2,000+ systems measure thickness AFTER curing (too late to prevent waste). This predicts thickness BEFORE curing, enabling real-time spray adjustment. Different value proposition: waste prevention vs. quality documentation.

### Welding Shielding Gas Flow Monitoring + AI
- **Competitors found**: GasIQ (Sweden, Optimator mechanical regulator), WITT Gas (gas mixers with basic connectivity), Air Liquide/Linde (gas suppliers with basic monitoring)
- **Competitive density score**: 2/5 (GasIQ is hardware-only flow reduction; no ML analytics SaaS exists)
- **Differentiation angle**: Per-station ML analytics + waste pattern identification as SaaS vs. hardware-only mechanical regulation
- **Status**: PROMOTED
- **Reasoning**: GasIQ sells a mechanical regulator that reduces gas surge. WITT sells gas mixers with basic internet access. Neither provides per-station analytics, waste pattern identification, operator behavior scoring, or predictive maintenance on regulators. The intelligence/analytics layer is completely unserved.

### Welding Consumable Inventory + Usage Prediction SaaS
- **Competitors found**: WeldAssistant (consumable database/selection), WeldIQ (code compliance), SmartWeld (IoT monitoring), Path Robotics (autonomous welding, $100M+ funded), Lincoln Electric WeldCloud (data management)
- **Competitive density score**: 4/5 (adjacent solutions exist; Lincoln Electric could easily add inventory features to WeldCloud)
- **Differentiation angle**: Specific focus on consumable inventory prediction and automated procurement
- **Status**: REJECTED
- **Reasoning**: Lincoln Electric's WeldCloud already captures welding data from connected machines and could add inventory prediction as a feature. SmartWeld and others are in the IoT monitoring space. The welding ecosystem is increasingly connected by large OEMs (Lincoln, Miller/ITW, Fronius) who own the machine data. A standalone consumable inventory startup would be squeezed by platform players.

### Coating Cure Monitoring (Inline Thermal + ML)
- **Competitors found**: Coatmaster (thermal optics for thickness, not cure), Datapixel (3D metrology, not cure), Heraeus Noblelight (IR emitters, not monitoring), various research papers on cure monitoring
- **Competitive density score**: 2/5 (no commercial inline cure quality prediction product exists)
- **Differentiation angle**: First inline cure quality predictor using thermal profiles + ML (complementary to thickness measurement)
- **Status**: PROMOTED
- **Reasoning**: Cure verification today is done by destructive testing (solvent rub, cross-hatch adhesion) on sample parts. No inline non-destructive cure quality system exists commercially. Coatmaster measures thickness but not cure state. This is a genuinely unserved need.

### Laundry Chemical Dosing AI
- **Competitors found**: Ecolab (3D platform, chemical + dosing), Diversey (dosing systems), Christeyns (dosing), Hydro Systems (pumps), Knight (Ecolab subsidiary, dosing hardware)
- **Competitive density score**: 4/5 (major chemical companies bundle dosing with chemical supply; entrenched vendor lock-in)
- **Differentiation angle**: Chemical-agnostic AI dosing that optimizes regardless of supplier
- **Status**: REJECTED
- **Reasoning**: Ecolab, Diversey, and Christeyns give dosing hardware "free" or near-cost as part of chemical supply contracts. Their business model is chemical revenue, not dosing optimization. A startup offering better dosing would reduce chemical spend, which directly threatens the incumbents' revenue model. They have no incentive to cooperate and strong incentive to block. The vendor lock-in is structural.

---

## Step 3: Market Analysis

### NIR Laundry Soil Classifier
- **Target market**: Mid-size commercial laundries (hotels, hospitals, uniform services) with 500-5,000 lbs/day capacity that over-dose chemicals due to inability to classify soil types
- **TAM**: Global commercial laundry market ~$40B; laundry chemicals segment ~$12B; chemical optimization addressable by soil classification ~$2.4B (20% of chemical spend is waste from over-dosing)
- **SAM**: North American mid-market commercial laundries (10,000+ facilities) x $5-15K/year SaaS = $100-150M
- **Revenue model**: Hardware sensor module ($2-5K one-time) + SaaS analytics/optimization ($500-1,200/month per facility)
- **Status**: PROMOTED
- **Reasoning**: Clear SAM >$100M. Chemical savings of 15-30% (documented in academic literature) pays back hardware cost in 3-6 months. Strong ROI story. Mid-market laundries (independent and small chains) lack the engineering staff to build custom solutions.

### Laundry Water Recycling AI Optimizer
- **Target market**: Commercial laundries with existing water recycling systems or high water costs motivating retrofit
- **TAM**: Global industrial water recycling market ~$8B; laundry-specific segment ~$800M
- **SAM**: North American commercial laundries with recycling systems (estimated 2,000-4,000 facilities) x $8-15K/year = $16-60M
- **Revenue model**: Software license on existing recycling hardware ($800-1,500/month)
- **Status**: REJECTED
- **Reasoning**: SAM too small. Only laundries that already have recycling hardware (or are considering it) are addressable. Estimated 2,000-4,000 facilities in North America is too narrow. Additionally, selling software to optimize hardware made by another vendor creates dependency and integration risk.

### Wet-to-Dry Film Thickness Prediction
- **Target market**: Automotive tier 1/2 suppliers, appliance manufacturers, aerospace component painters, and custom job shops with high-value parts where rework is expensive
- **TAM**: Global industrial coatings market ~$780M (narrow definition); paint application equipment ~$4B; quality/rework costs addressable ~$1.5B
- **SAM**: North American industrial paint shops with automated or semi-automated lines (5,000+ facilities) x $15-25K/year = $75-125M
- **Revenue model**: Sensor hardware module ($5-10K) + SaaS prediction engine ($1,000-2,000/month per line)
- **Status**: PROMOTED
- **Reasoning**: SAM at $75-125M is marginal but acceptable. The key driver is rework cost avoidance. A single automotive paint line producing 1,000+ parts/day with 5-10% rework rate ($50-200/part rework cost) can save $25K-200K/year. Clear ROI for target customers.

### Welding Shielding Gas Waste Analytics SaaS
- **Target market**: Mid-size fabrication shops (20-200 welding stations) doing MIG/MAG welding with significant shielding gas spend ($50K-500K/year on gas)
- **TAM**: Global welding consumables market $12.7B; shielding gas segment ~$3.8B (30%); waste/inefficiency ~$1.1B (30% of gas is wasted per industry estimates)
- **SAM**: North American mid-size fab shops (15,000+ facilities) x $5-12K/year SaaS = $75-180M
- **Revenue model**: IoT sensor nodes ($200-500 per station) + SaaS analytics ($200-500/month per facility)
- **Status**: PROMOTED
- **Reasoning**: SAM >$75M. Industry estimates suggest 30-50% of shielding gas is wasted (surge at arc start, leaks, over-flow). GasIQ's mechanical solution saves 60% but costs $500-1,000 per station with no data. This SaaS approach costs less per station, provides analytics, and can demonstrate ROI in real-time dashboards. Mid-market fab shops have no visibility into per-station gas usage today.

### Coating Cure Monitoring ML
- **Target market**: Automotive OEMs/suppliers, aerospace component manufacturers, industrial equipment coaters with critical-to-function coatings where cure quality determines product lifetime
- **TAM**: Coating quality testing/inspection market ~$2B; inline cure monitoring addressable ~$600M
- **SAM**: North American automotive/aerospace/industrial coating lines with cure ovens (3,000+ facilities) x $20-40K/year = $60-120M
- **Revenue model**: Thermal sensor array ($10-20K per oven) + ML prediction SaaS ($1,500-3,000/month per line)
- **Status**: PROMOTED
- **Reasoning**: SAM ~$60-120M. Under-cure is a significant quality failure mode in automotive (warranty claims from coating delamination). Currently caught only by destructive testing on samples (1 per 100 parts typically). 100% inline monitoring eliminates sampling risk. High-value application.

---

## Step 4: Feasibility Analysis

### NIR Laundry Soil Classifier
- **Technical risk**: Medium (NIR soil classification on textiles demonstrated in research; productization requires calibration across fabric types and soil combinations)
- **Market risk**: Low (clear pain point, quantifiable savings, existing buyer budget for chemicals)
- **Execution risk**: Low (small hardware module + cloud SaaS; no complex integration)
- **Timing risk**: Low (NIR sensors are commodity; edge ML processors available; no technology dependency)
- **Capital required**: $250-400K (NIR sensor module development $80K, ML model training with labeled soil samples $60K, cloud platform $50K, pilot deployments $60K)
- **Feasibility score**: 8/10
- **Status**: PROMOTED
- **Reasoning**: Strong fit with winning archetype. Commodity NIR sensor ($30-50) + edge ML processor ($20-30) = $50-80 hardware BOM. Software-heavy value proposition. Clear ROI (15-30% chemical savings = $15-50K/year for mid-size laundry vs. $5-15K/year subscription). Low capital requirement. Main risk is calibration across diverse textile/soil combinations requiring extensive training data.

### Wet-to-Dry Film Thickness Prediction
- **Technical risk**: Medium-High (wet-to-dry prediction requires modeling solvent evaporation, cure chemistry, environmental conditions; accuracy requirements are tight in automotive +/- 5 microns)
- **Market risk**: Medium (automotive paint shops are conservative; long qualification cycles)
- **Execution risk**: Medium (sensor integration on active paint lines requires coordination with line builders)
- **Timing risk**: Low (optical sensors and ML frameworks available today)
- **Capital required**: $400-700K (optical sensor development $120K, ML model development requiring training data from real paint lines $150K, pilot integrations $100K, cloud platform $80K)
- **Feasibility score**: 6/10
- **Status**: REJECTED
- **Reasoning**: Technical risk is the killer. Wet-to-dry thickness prediction requires accurate modeling of complex physical/chemical processes (solvent evaporation rate, film formation, cure shrinkage) that vary by paint formulation. Each new paint chemistry requires re-training. Automotive paint shops change formulations frequently. The accuracy requirement (+/- 5 microns) may not be achievable with ML alone without deep physics-based modeling, pushing this toward TRL 5.

### Welding Shielding Gas Waste Analytics SaaS
- **Technical risk**: Low (MEMS flow sensors are commodity; data analytics is well-understood; edge computing proven)
- **Market risk**: Low-Medium (fab shops know gas is wasted but may not prioritize fixing it; requires demonstrating ROI)
- **Execution risk**: Low (simple sensor node + cloud dashboard; standard IoT architecture)
- **Timing risk**: Low (all components available today; no technology dependency)
- **Capital required**: $200-350K (MEMS sensor node design $50K, firmware/edge processing $40K, cloud analytics platform $60K, pilot deployments $50K, sales/marketing $50K)
- **Feasibility score**: 8/10
- **Status**: PROMOTED
- **Reasoning**: Excellent fit with winning archetype. Commodity MEMS flow sensor ($5-15) + MCU ($5) + WiFi ($3) = $15-25 BOM per node. Software is the value. GasIQ proves the pain point exists (they sell $500-1000 mechanical regulators). This is 10x cheaper per station with 10x more value (analytics, visibility, optimization recommendations). Classic "intelligence layer on commodity hardware" play.

### Coating Cure Monitoring ML
- **Technical risk**: Medium (thermal profile to cure state correlation is well-established in literature but requires per-formulation calibration; IR camera systems are commodity)
- **Market risk**: Medium (automotive/aerospace buyers have long qualification cycles; need to demonstrate correlation to destructive test results)
- **Execution risk**: Medium (installation in cure ovens requires thermal hardening of electronics; integration with MES systems)
- **Timing risk**: Low (thermal cameras and ML frameworks available)
- **Capital required**: $400-600K (hardened thermal camera module $100K, ML model development with real cure data $120K, MES integration $80K, pilot deployments $100K)
- **Feasibility score**: 7/10
- **Status**: PROMOTED
- **Reasoning**: Good fit with archetype. Commodity LWIR thermal camera ($200-500) + edge processor ($50) = $250-550 hardware BOM for entire oven zone. Software value proposition (cure quality prediction). Main challenge is getting access to cure oven environments for training data collection (temperatures 150-220C). Automotive buyers pay premium for quality assurance. Payback via reduced warranty claims and eliminated destructive testing.

---

## Step 5: Execution Summary

### NIR Laundry Soil Classifier (Feasibility: 8/10)
- **Product**: Retrofit sensor module (clamp-on or drop-in) for commercial washing machines that spectroscopically classifies soil type on incoming textiles and auto-optimizes chemical dosing recipe per load
- **Technology**: Texas Instruments DLP NIRscan-class MEMS-based NIR spectrometer ($30-50 sensor) + ARM Cortex edge ML processor running random forest / 1D-CNN classifier trained on soil spectral signatures + cloud dashboard showing chemical usage analytics
- **Market**: 10,000+ mid-size commercial laundries in North America (hotels, hospitals, uniform services) currently over-dosing chemicals by 15-30% because they cannot distinguish soil types
- **Revenue model**: $3-5K hardware module (one-time) + $500-1,200/month SaaS per facility; target LTV:CAC > 5:1
- **Capital**: $250-400K to first revenue (12 months)
- **Key strength**: Commodity hardware ($50-80 BOM), pure software differentiation, immediate measurable ROI (chemical savings visible on first month's invoice), no regulatory barriers, short sales cycle (facility managers decide)
- **Key risk**: Calibration complexity across diverse textile types and soil combinations; requires extensive labeled training data collection during pilot phase

### Welding Shielding Gas Waste Analytics SaaS (Feasibility: 8/10)
- **Product**: Low-cost IoT sensor nodes that clamp onto existing gas lines at each welding station, measuring flow rates and feeding a cloud analytics platform that identifies waste patterns, ranks stations by efficiency, and provides operator-specific optimization recommendations
- **Technology**: MEMS mass flow sensor ($5-15) + ESP32 MCU + WiFi = $15-25 per node BOM; cloud analytics with anomaly detection, pattern recognition (surge waste, leak detection, over-flow identification); mobile-first dashboard
- **Market**: 15,000+ mid-size fabrication shops in North America (20-200 stations each) spending $50-500K/year on shielding gas with zero visibility into per-station usage or waste
- **Revenue model**: $150-300 per sensor node (at-cost hardware) + $200-500/month per facility SaaS; typical 20-station shop = $3K-6K hardware + $2.4-6K/year SaaS
- **Capital**: $200-350K to first revenue (10 months)
- **Key strength**: Lowest capital requirement of any idea; commodity hardware ($15-25 BOM vs. GasIQ's $500-1000 per station); provides analytics that GasIQ cannot (data-driven vs. mechanical-only); 10x larger addressable market (mid-market shops that cannot justify $500+/station for GasIQ)
- **Key risk**: Gas savings alone may not justify subscription for smaller shops; need to bundle value (leak detection preventing safety incidents, compliance documentation for ISO audits, operator performance metrics)

### Coating Cure Monitoring ML (Feasibility: 7/10)
- **Product**: Inline thermal monitoring system installed in cure ovens that predicts coating cure quality for every part using IR thermal imaging + ML, replacing destructive sample testing with 100% non-destructive inspection
- **Technology**: LWIR thermal camera module ($200-500) + thermally-hardened enclosure + edge ML processor running cure-state prediction model trained on thermal profiles correlated with destructive test results; MES integration for traceability
- **Market**: 3,000+ automotive/aerospace/industrial coating lines in North America with critical-to-function coatings where under-cure causes warranty claims or safety issues
- **Revenue model**: $10-20K thermal sensor array per oven + $1,500-3,000/month SaaS per line
- **Capital**: $400-600K to first revenue (14 months)
- **Key strength**: Eliminates destructive testing cost ($5-20/test, 10-50 tests/day = $50-1,000/day savings); prevents warranty claims from under-cured parts (single automotive recall can cost $1M+); regulatory/quality documentation automatic
- **Key risk**: Requires per-formulation calibration (training data from destructive tests needed for each new coating); automotive qualification timelines are 6-12 months

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 8 | 2 |
| Step 2 | 8 | 5 | 3 |
| Step 3 | 5 | 4 | 1 |
| Step 4 | 4 | 3 | 1 |
| Step 5 | 3 | 3 | — |