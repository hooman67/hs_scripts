# Cycle 030 Report

**Date**: 2026-06-08
**Domains explored**: CNC plasma cutting parameter optimization, waterjet cutting AI, EDM parameter optimization, metal stamping die wear prediction, sheet metal forming validation, tube bending quality prediction, press brake angle correction, abrasive flow machining optimization, wire EDM adaptive control, plasma consumable life prediction

---

## Step 1: Technology Discovery

### 1. CNC Plasma Cutting Parameter Optimization (AI-Driven)
- **Domain**: Metal fabrication / thermal cutting
- **Breakthrough**: Edge-AI inference on acoustic + voltage signals from plasma arc to auto-tune amperage, speed, gas flow, and standoff height in real-time. Enabled by 2025 advances in lightweight transformer models running on $50 edge compute (Raspberry Pi 5 / Jetson Orin Nano).
- **TRL**: 7 (academic papers proven; Hypertherm ProNest does nesting only, not real-time parameter AI; no commercial product exists for adaptive parameter tuning on mid-range plasma tables)
- **Time to product**: 6-9 months
- **Status**: PROMOTED
- **Reasoning**: Plasma cutting has 10x more operators than laser cutting in the SMB market (fab shops, HVAC, structural steel). Hypertherm has CAD/CAM software (ProNest, Phoenix) but zero AI for real-time parameter adaptation. Current state: operators manually consult cut charts and trial-and-error. Fits the archetype perfectly: replace $200K+ automated high-def plasma systems with $30K plasma table + $5K AI module.

### 2. Waterjet Cutting Quality Prediction SaaS
- **Domain**: Precision cutting / manufacturing
- **Breakthrough**: ML models trained on pump pressure waveforms, abrasive flow rate, and nozzle wear signatures to predict cut quality degradation before it manifests. OMAX IntelliMAX and Flow SmartStream use static mathematical models, not adaptive ML.
- **TRL**: 6-7 (sensor fusion of pressure transducers + accelerometers well-proven; ML inference on edge proven)
- **Time to product**: 9-12 months
- **Status**: PROMOTED
- **Reasoning**: Waterjet market is $1.31B (2025), growing 7.2% CAGR. Flow and OMAX have rule-based optimization but no ML-driven adaptive quality prediction. 60%+ of waterjet shops are SMBs running 1-3 tables. Key pain: abrasive nozzle wear is gradual and invisible until parts fail QC. An aftermarket AI sensor module could save $20-50K/year in scrap per machine.

### 3. EDM Parameter Optimization AI
- **Domain**: Precision machining / mold & die making
- **Breakthrough**: ML model trained on spark gap voltage/current waveforms to adaptively optimize pulse-on/off time, servo voltage, and flushing pressure. Sodick K-SMC adjusts at 500x/sec but uses fixed PID logic, not learned models.
- **TRL**: 5-6 (extensive academic research on ML for EDM; no commercial products; Makino, Sodick, GF all lack AI features)
- **Time to product**: 12-18 months
- **Status**: REJECTED
- **Reasoning**: TRL too low for our threshold. EDM is a precision niche ($5-7B market) dominated by Japanese/Swiss OEMs (Sodick, Makino, GF, Mitsubishi) who tightly integrate controls. Aftermarket bolt-on would require deep integration with proprietary CNCs. Also, EDM shops are typically sophisticated (mold makers) who already optimize well. Capital requirements for certification/validation would exceed $500K.

### 4. Metal Stamping Die Wear Prediction (SMB Focus)
- **Domain**: Metal stamping / press operations
- **Breakthrough**: Acoustic emission + force curve analysis using commodity MEMS accelerometers ($5) and edge ML to predict die wear progression and recommend maintenance windows. Schuler/Andritz Metris Visual Die Protection exists but costs $100K+ and targets automotive OEMs only.
- **TRL**: 7 (Brankamp/Marposs has basic process monitoring sensors; acoustic ML for tool wear proven in CNC milling; ready for stamping transfer)
- **Time to product**: 9-12 months
- **Status**: PROMOTED
- **Reasoning**: Metal stamping market is $213.8B (2023). Thousands of mid-market stamping shops (50-500 employees) running mechanical/servo presses cannot afford Schuler Metris ($100K+ per press). They currently replace dies on fixed schedules, wasting 20-40% of die life. A $3-5K per-press sensor + AI module could predict die wear, saving $50-200K/year per shop in die costs and scrap.

### 5. Sheet Metal Forming Springback Prediction (AI-Augmented)
- **Domain**: Sheet metal forming / press brake operations
- **Breakthrough**: ML model trained on material lot data (tensile strength, grain direction, thickness variation) + bending parameters to predict springback without expensive simulation licenses. AutoForm costs $50-100K/year; most mid-market shops have no simulation.
- **TRL**: 7 (physics well-understood; data-driven springback prediction published extensively; commodity strain gauges + ML proven)
- **Time to product**: 6-9 months
- **Status**: PROMOTED
- **Reasoning**: AutoForm dominates enterprise simulation at $50-100K+/year. 90% of sheet metal shops cannot afford it and rely on operator experience + trial bends. An AI system trained on the shop's own material/tooling history could predict first-bend accuracy, reducing setup time by 50-70%. Fits archetype: take $100K simulation software, replicate 80% with data-driven ML at 1/10th cost.

### 6. Tube Bending Quality Prediction AI
- **Domain**: Tube fabrication / bending operations
- **Breakthrough**: ML model using mandrel force, wall thickness measurements, and material properties to predict wrinkling, ovality, and springback before they occur. Schwarze-Robitec has simulation but not adaptive ML. AutoForm Tube is enterprise-only simulation.
- **TRL**: 6-7 (tube bending physics well-modeled; in-process sensors proven; ML for forming prediction published)
- **Time to product**: 9-12 months
- **Status**: PROMOTED
- **Reasoning**: Tube bending is a $2-3B machine market with thousands of SMB fabricators (furniture, automotive exhaust, HVAC, aerospace subcontractors). Current state: expensive trial bends and physical prototypes. An aftermarket sensor + AI system could cut setup time from hours to minutes and reduce scrap rates by 30-50%.

### 7. Plasma Consumable Life Prediction
- **Domain**: Metal fabrication / plasma cutting
- **Breakthrough**: ML model analyzing arc voltage signature degradation, pierce count, and material mix to predict remaining consumable life (electrode, nozzle, shield cap). Currently operators replace on fixed schedules or when quality visibly degrades.
- **TRL**: 7-8 (voltage signature analysis well-established; consumable wear is predictable; edge ML readily applicable)
- **Time to product**: 4-6 months
- **Status**: PROMOTED
- **Reasoning**: Consumables cost $2-8K/month for busy plasma shops. Premature replacement wastes 20-40% of consumable life; late replacement causes $500-2K in scrapped parts per incident. A $200/month SaaS + $500 sensor module could save $500-2K/month per table. Very capital-efficient to build. Different from plasma parameter optimization (Tech #1) - this is pure predictive maintenance for wear parts.

### 8. Press Brake Angle Measurement AI
- **Domain**: Sheet metal fabrication / bending
- **Breakthrough**: Computer vision (commodity camera + edge AI) to measure bend angle in real-time during press brake operation, providing closed-loop correction recommendations. Existing solutions (AMADA, Bystronic) are built into $200K+ machines only.
- **TRL**: 7-8 (machine vision for angle measurement proven; edge inference fast enough for feedback; commodity hardware available)
- **Time to product**: 6-9 months
- **Status**: PROMOTED
- **Reasoning**: 80%+ of press brakes in service are older machines without built-in angle measurement. Operators use protractors and trial bends. An aftermarket camera + AI system ($3-5K per machine) providing real-time angle feedback could save 30-50% of setup time. Huge installed base of legacy press brakes (100K+ in North America alone).

### 9. Abrasive Flow Machining Process Optimization
- **Domain**: Precision finishing / deburring
- **Breakthrough**: ML optimization of media viscosity, pressure, and cycle time for abrasive flow machining (AFM) based on part geometry and required surface finish.
- **TRL**: 5 (very niche process; limited sensor data available; academic only)
- **Time to product**: 18+ months
- **Status**: REJECTED
- **Reasoning**: Too niche - AFM market is <$500M globally. TRL 5 means extensive R&D required. Customer base is extremely specialized (aerospace, medical). Long sales cycles and certification requirements. Does not fit the mid-market archetype.

### 10. Wire EDM Adaptive Threading AI
- **Domain**: Precision machining / EDM
- **Breakthrough**: ML model to predict and prevent wire breakage during threading and cutting by analyzing electrical discharge patterns and servo feedback.
- **TRL**: 6 (GF Machining and Sodick have some basic adaptive features already built in; academic research exists)
- **Time to product**: 12-15 months
- **Status**: REJECTED
- **Reasoning**: Wire EDM machines already have proprietary adaptive threading features from OEMs (GF, Sodick, Mitsubishi). The retrofit market is small because wire EDM machines are expensive ($100K+) and typically well-maintained. Aftermarket bolt-on would face integration challenges with proprietary controls. Does not fit the mid-market archetype well.

---

## Step 2: Competitive Analysis

### CNC Plasma Cutting Parameter Optimization (AI-Driven)
- **Competitors found**: Hypertherm (ProNest/Phoenix - nesting/CAM only, no real-time AI), ESAB (Columbus CAM - nesting only), Messer (OmniWin - nesting only), Vicon (basic CNC software). None offer real-time adaptive parameter AI.
- **Competitive density score**: 2/5
- **Differentiation angle**: First aftermarket AI module that ingests acoustic/voltage signals from ANY plasma power supply and provides real-time parameter recommendations. Agnostic to machine brand (works with Hypertherm, ESAB, Thermal Dynamics, Lincoln).
- **Status**: PROMOTED
- **Reasoning**: No direct competitor offers AI-driven adaptive parameter tuning for plasma cutting. Existing players focus exclusively on CAD/CAM/nesting. This is a genuine gap in a large market segment.

### Waterjet Cutting Quality Prediction SaaS
- **Competitors found**: Flow (SmartStream - rule-based mathematical models), OMAX (IntelliMAX - algorithmic, not ML), WARDJet (basic monitoring), Hyperpressure (custom integration). Oden Technologies (broad manufacturing AI, not waterjet-specific).
- **Competitive density score**: 3/5
- **Differentiation angle**: ML-driven quality prediction specifically for abrasive waterjet, predicting cut quality degradation from nozzle/orifice wear before it manifests in parts. Aftermarket sensor kit compatible with any waterjet brand.
- **Status**: PROMOTED
- **Reasoning**: Flow SmartStream is the closest competitor but uses static mathematical models, not adaptive ML. Density is moderate - existing players have adjacent solutions but none do predictive quality from wear signatures. Differentiation through aftermarket universal compatibility (works with Flow, OMAX, WARDJet, Mitsubishi).

### Metal Stamping Die Wear Prediction (SMB Focus)
- **Competitors found**: Schuler/Andritz Metris Visual Die Protection (AI-based, $100K+, enterprise only), Brankamp/Marposs (process monitoring, no predictive AI), Kistler (force sensors, no AI), Wintriss (basic die protection sensors). Acerta AI (automotive Tier-1, not SMB stamping).
- **Competitive density score**: 4/5
- **Differentiation angle**: 1/10th cost targeting 50-500 employee stamping shops that cannot afford Schuler Metris. Commodity MEMS sensors + cloud ML vs. enterprise hardware.
- **Status**: REJECTED
- **Reasoning**: Competitive density is at the rejection threshold. Schuler Metris already has AI-based die protection (Visual Die Protection uses AI for early damage detection). Brankamp/Marposs has decades of expertise in stamping monitoring. While the SMB cost point is different, these incumbents could easily move downmarket. The differentiation is primarily price, which is vulnerable.

### Sheet Metal Forming Springback Prediction (AI-Augmented)
- **Competitors found**: AutoForm (enterprise simulation, $50-100K+), Neural Concept (ML for forming, targets large OEMs), Stampack/Hexagon (enterprise simulation), LS-DYNA (general FEA). No SMB-focused AI springback prediction found.
- **Competitive density score**: 2/5
- **Differentiation angle**: Data-driven (not physics simulation) springback prediction trained on each shop's own material/press/tooling data. No CAD expertise required. $500/month SaaS vs. $100K/year simulation license. Targets the 90% of shops that cannot afford AutoForm.
- **Status**: PROMOTED
- **Reasoning**: Clear gap between expensive enterprise simulation (AutoForm, $50-100K) and no solution at all for SMBs. Neural Concept targets large OEMs (Subaru case study). No one is offering affordable data-driven springback prediction for mid-market sheet metal shops. The "learn from your own shop data" approach is genuinely differentiated.

### Tube Bending Quality Prediction AI
- **Competitors found**: AutoForm Tube (enterprise simulation), Schwarze-Robitec (simulation software, not AI), Transfluid (machines only), BLM Group (machines with some smart features). No aftermarket AI prediction found.
- **Competitive density score**: 2/5
- **Differentiation angle**: Aftermarket sensor kit + cloud AI for any CNC tube bender. Predicts wrinkling, ovality, and springback from mandrel force + material properties without expensive simulation. Works on existing installed base of tube benders.
- **Status**: PROMOTED
- **Reasoning**: Tube bending quality prediction is currently either done through expensive simulation (AutoForm Tube, enterprise only) or trial-and-error (most SMBs). No aftermarket AI solution exists. Low competitive density with clear differentiation opportunity.

### Plasma Consumable Life Prediction
- **Competitors found**: Hypertherm (manual tracking via ProNest job logs, no predictive AI), ESAB (no predictive feature), Victor/Thermal Dynamics (no predictive). No startup or aftermarket solution found.
- **Competitive density score**: 1/5
- **Differentiation angle**: First predictive maintenance solution specifically for plasma consumables. Analyzes arc voltage signature degradation to predict remaining life of electrode, nozzle, and shield cap. Universal compatibility.
- **Status**: PROMOTED
- **Reasoning**: Essentially zero competition. Plasma consumable replacement is entirely manual/schedule-based today. Hypertherm tracks pierce counts in ProNest but does no predictive analysis. This is an extremely clear market gap with immediate, quantifiable ROI for any plasma shop.

### Press Brake Angle Measurement AI
- **Competitors found**: AMADA (built-in on $200K+ machines), Bystronic (built-in), Trumpf (built-in), Haco (built-in on premium models), Digi-Pas (digital level, manual), VICIVISION (3D measurement, post-process). One potential competitor: LaserSafe (angle measurement laser, $8-15K, not AI-driven).
- **Competitive density score**: 3/5
- **Differentiation angle**: Vision-based (not laser) angle measurement that is 1/3 the cost of LaserSafe and adds AI-driven compensation recommendations based on material lot data. Retrofit kit for any legacy press brake.
- **Status**: PROMOTED
- **Reasoning**: While OEMs build angle measurement into new machines, the aftermarket for legacy press brakes is underserved. LaserSafe exists but is expensive and not AI-driven. Vision-based approach using commodity cameras + edge AI at $3-5K is meaningfully different from $8-15K laser systems. Large installed base of legacy machines.

---

## Step 3: Market Analysis

### Plasma Parameter AI (CNC Plasma Cutting Parameter Optimization)
- **Target market**: Mid-market metal fabrication shops running 1-10 CNC plasma tables (HVAC, structural steel, job shops, ship repair, heavy equipment fabricators)
- **TAM**: $2.5B (plasma cutting equipment + consumables market) with addressable software/AI layer of ~$800M
- **SAM**: $150M (50,000+ plasma tables in North America at $3K/year subscription)
- **Revenue model**: Hardware sensor kit ($2-3K one-time) + SaaS subscription ($300-500/month per table)
- **Status**: PROMOTED
- **Reasoning**: Clear path to $100M+ SAM. Plasma cutting shops have immediate pain (scrap, rework, consumable waste) and willingness to pay if ROI is demonstrable. Monthly subscription aligns with their existing consumable spend patterns.

### Waterjet Quality Prediction SaaS
- **Target market**: Waterjet job shops and in-house waterjet operations (1-5 machines) in metal fabrication, stone/tile, aerospace subcontracting
- **TAM**: $1.31B waterjet machine market + $400M consumables/service
- **SAM**: $80M (15,000+ waterjet machines in North America at $5K/year subscription)
- **Revenue model**: Sensor retrofit kit ($3-5K one-time) + SaaS subscription ($400-600/month per machine)
- **Status**: PROMOTED
- **Reasoning**: Meets SAM threshold. Waterjet operators face significant quality uncertainty from progressive nozzle/orifice wear. Scrap from quality degradation can cost $5-20K/month per machine. ROI is clear and immediate.

### SpringbackAI (Sheet Metal Forming Springback Prediction)
- **Target market**: Sheet metal fabrication shops (50-500 employees) running press brakes without simulation software. Automotive Tier 2-3, HVAC, enclosure manufacturers, appliance subcontractors.
- **TAM**: $213.8B metal stamping market; addressable software layer for press brake operations ~$2B
- **SAM**: $120M (40,000+ press brake shops in North America at $3K/year subscription)
- **Revenue model**: SaaS subscription ($250-500/month) with optional IoT sensor module ($1-2K one-time) for automated data capture
- **Status**: PROMOTED
- **Reasoning**: Massive underserved market. AutoForm has <5% penetration in shops under 500 employees. The value proposition (eliminate trial bends, first-part-right) resonates immediately with shop owners who waste hours per setup.

### Tube Bending Quality Prediction AI
- **Target market**: Tube fabrication shops (automotive exhaust, furniture, aerospace subcontractors, HVAC, handrails/architectural)
- **TAM**: $2-3B tube bending machine market
- **SAM**: $60M (10,000+ CNC tube benders in North America at $6K/year)
- **Revenue model**: Sensor kit ($3-5K one-time) + SaaS subscription ($400-600/month per machine)
- **Status**: REJECTED
- **Reasoning**: SAM of $60M is borderline but the real issue is market fragmentation. Tube bending applications are highly diverse (medical tubes vs. automotive exhaust vs. architectural handrails) requiring different models. Customer acquisition cost would be high due to fragmentation. Capital efficiency concern: would need to build separate models for each application domain.

### Plasma Consumable Life Prediction
- **Target market**: Any shop running CNC or mechanized plasma cutting (metal fabrication, shipyards, structural steel, HVAC shops)
- **TAM**: $800M plasma consumables market (electrodes, nozzles, shield caps, swirl rings)
- **SAM**: $100M (50,000+ plasma tables in North America at $2K/year subscription)
- **Revenue model**: Minimal hardware sensor ($200-500 clip-on voltage sensor) + SaaS subscription ($150-200/month per table)
- **Status**: PROMOTED
- **Reasoning**: Extremely capital-efficient opportunity. Minimal hardware required (voltage signal already accessible on most plasma power supplies). Clear ROI: $200/month subscription saves $500-2K/month in consumable waste + scrap prevention. Same customer base as Plasma Parameter AI but simpler product with faster time to revenue. Could be a wedge product that leads to the fuller parameter optimization system.

### Press Brake Angle Measurement AI
- **Target market**: Sheet metal shops with older press brakes (5-30+ years old) lacking built-in angle measurement. Job shops, HVAC fabricators, enclosure manufacturers.
- **TAM**: $5B press brake market (100K+ installed units in North America without angle measurement)
- **SAM**: $200M (50,000+ legacy press brakes at $4K/year)
- **Revenue model**: Hardware kit ($3-5K) + SaaS subscription ($200-350/month per machine)
- **Status**: PROMOTED
- **Reasoning**: Large installed base of legacy press brakes creates strong aftermarket opportunity. ROI is immediate (30-50% reduction in setup time = operator labor savings). $200M SAM with clear path to capture.

---

## Step 4: Feasibility Analysis

### Plasma Parameter AI
- **Technical risk**: Medium (requires robust acoustic/voltage signal processing in noisy shop environments; ML model needs training data from diverse material/thickness combinations)
- **Market risk**: Low (clear pain point, quantifiable ROI, large addressable market)
- **Execution risk**: Medium (need to support multiple plasma power supply brands; field installation varies)
- **Timing risk**: Low (technology stack is ready; no regulatory barriers; immediate demand)
- **Capital required**: $300-400K (hardware prototyping $50K, ML development $150K, pilot program with 5-10 shops $100K, go-to-market $100K)
- **Feasibility score**: 7/10
- **Status**: PROMOTED
- **Reasoning**: Strong fit with winning archetype. Key risk is data collection — need partnerships with 5-10 plasma shops to build training dataset across material types. But the sensor hardware is commodity (MEMS mic + voltage divider + Jetson Nano) and the ML inference is well-understood. Revenue from first customers within 12 months of founding.

### Waterjet Quality Prediction SaaS
- **Technical risk**: Medium-High (correlating pressure waveforms with cut quality requires significant domain expertise; nozzle wear is gradual and complex)
- **Market risk**: Low-Medium (clear pain but waterjet operators are technically sophisticated and skeptical)
- **Execution risk**: Medium (need waterjet-specific domain expertise on founding team; multiple OEM integrations)
- **Timing risk**: Low (technology ready, market growing)
- **Capital required**: $400-600K (sensor hardware design $80K, ML development $200K, domain expertise hiring $150K, pilots $100K, GTM $70K)
- **Feasibility score**: 6/10
- **Status**: REJECTED
- **Reasoning**: While the market gap is real, the technical complexity is higher than plasma cutting. Waterjet quality depends on many interacting variables (garnet quality, water pressure, focus tube alignment, abrasive flow rate) making reliable prediction harder. Also, waterjet operators tend to be more technically sophisticated and may resist "black box" AI. Capital requirement at the higher end. Plasma consumable prediction (simpler signal, clearer correlation) is a better entry point.

### SpringbackAI
- **Technical risk**: Low-Medium (springback prediction from material properties + process parameters is well-studied; the innovation is making it accessible without CAD/simulation expertise)
- **Market risk**: Low (universal pain point for every press brake operator; clear ROI)
- **Execution risk**: Low (pure software with optional hardware; can start with manual data entry and add sensors later)
- **Timing risk**: Low (no dependencies on emerging tech; can launch with existing ML frameworks)
- **Capital required**: $200-300K (ML development $120K, UX/product $60K, pilot program $50K, GTM $70K)
- **Feasibility score**: 8/10
- **Status**: PROMOTED
- **Reasoning**: Highest feasibility in this cycle. Extremely capital-efficient — primarily a software product. Can start with a tablet app where operators input material lot data + bend parameters and get springback predictions. No complex hardware required initially. The dataset bootstrapping challenge (need historical bend data) can be solved by offering free onboarding where operators log 50-100 bends to train the model. AutoForm-level accuracy not required — even 70% first-bend-right improvement is transformative for shops currently at 30-40%.

### Plasma Consumable Life Prediction
- **Technical risk**: Low (arc voltage signature analysis is well-understood; correlation between voltage degradation and consumable wear is well-documented in plasma cutting literature)
- **Market risk**: Low (every plasma operator faces this exact problem daily; quantifiable savings)
- **Execution risk**: Low (simple hardware — voltage tap + edge compute; clear deployment path)
- **Timing risk**: Low (ready now; no emerging tech dependency)
- **Capital required**: $150-250K (sensor module design $40K, ML development $80K, pilot $50K, manufacturing $30K, GTM $50K)
- **Feasibility score**: 9/10
- **Status**: PROMOTED
- **Reasoning**: Highest score in this cycle. Exceptionally capital-efficient. The voltage signal from a plasma arc is already accessible (standard diagnostic port on most power supplies). Consumable wear follows predictable degradation curves that ML can model with relatively small training datasets. Can reach revenue within 6 months. This is the "wedge" product — once installed on plasma tables, expands to full parameter optimization (Tech #1).

### Press Brake Angle Measurement AI
- **Technical risk**: Medium (computer vision in industrial environments faces lighting, vibration, and occlusion challenges; achieving sub-0.5-degree accuracy with commodity cameras is non-trivial)
- **Market risk**: Low (clear value proposition; large installed base)
- **Execution risk**: Medium (needs robust mounting solutions for diverse press brake geometries; calibration complexity)
- **Timing risk**: Low (technology ready)
- **Capital required**: $300-450K (vision system prototyping $100K, ML development $120K, industrial design $80K, pilots $80K, GTM $70K)
- **Feasibility score**: 7/10
- **Status**: PROMOTED
- **Reasoning**: Solid opportunity but slightly higher technical risk than the pure-software springback prediction. Vision accuracy in dirty shop environments is the key challenge. However, the market size and clear ROI justify the investment. Could be a strong #2 product after SpringbackAI, using the same customer base.

---

## Step 5: Execution Summary

### Plasma Consumable Life Prediction (Feasibility: 9/10)
- **Product**: Clip-on voltage sensor module + cloud SaaS that monitors plasma arc voltage signatures and predicts remaining consumable life (electrode, nozzle, shield cap) with 85%+ accuracy. Dashboard shows remaining life %, alerts before quality degradation, and recommends optimal replacement timing.
- **Technology**: Voltage divider sensor (clips onto plasma torch lead), ESP32/RPi edge processor, cloud ML model trained on voltage degradation curves correlated with consumable wear states. Models improve per-customer over time.
- **Market**: 50,000+ CNC plasma tables in North America; target HVAC fabricators, structural steel shops, and job shops running 8+ hours/day where consumable cost is $2-8K/month.
- **Revenue model**: $200-500 sensor hardware (at cost) + $150-200/month SaaS subscription per table. Land-and-expand to full parameter optimization.
- **Capital**: $150-250K to first revenue (6-9 months)
- **Key strength**: Extreme capital efficiency + immediate quantifiable ROI ($500-2K/month savings per table) + zero competition + natural expansion path to broader plasma cutting AI platform.
- **Key risk**: Sensor durability in high-EMI plasma environments; may need EMI shielding iteration. Mitigated by using optically-isolated voltage sensing.

### SpringbackAI (Feasibility: 8/10)
- **Product**: Tablet/web application where press brake operators input material lot data (from mill certs), tooling selection, and bend geometry to receive AI-predicted springback compensation angles. Eliminates trial bends and achieves first-part-right on 70-80% of setups (vs. current 30-40%).
- **Technology**: ML model (gradient-boosted trees + neural network ensemble) trained on historical bend data per shop. Self-improving: every bend logged improves future predictions. Optional IoT sensor module for automated data capture from press brake controller.
- **Market**: 40,000+ press brake shops in North America without simulation software. Target: shops doing 10-50 unique setups/week where trial bends waste 30-60 minutes each.
- **Revenue model**: $250-500/month SaaS subscription per press brake. Free onboarding period (50 bends logged) to build initial model. Upsell sensor module ($1-2K) and multi-machine licenses.
- **Capital**: $200-300K to first revenue (6-9 months)
- **Key strength**: Pure software play with optional hardware; massive underserved market where AutoForm ($50-100K) is overkill; data moat strengthens with each customer; incredibly low churn once trained on shop-specific data.
- **Key risk**: Cold-start problem (need ~50 bends of training data per shop before predictions are useful). Mitigated by transfer learning from aggregate anonymized data + clear onboarding UX.

### Plasma Parameter AI (Feasibility: 7/10)
- **Product**: Edge AI module that analyzes real-time acoustic and electrical signals from plasma cutting to provide dynamic parameter recommendations (speed, amperage, gas pressure, standoff height) optimized for cut quality and consumable life. Reduces scrap by 30-50% and extends consumable life by 20-40%.
- **Technology**: MEMS microphone array + voltage/current sensors + Jetson Orin Nano running real-time transformer model. Integrates with CNC controller via standard interfaces (analog voltage for speed override, or operator HMI display).
- **Market**: Same 50,000+ CNC plasma table market as consumable prediction, but higher ticket ($5K hardware + $300-500/month). Target power users doing complex cuts (beveling, thick plate, multi-material).
- **Revenue model**: $2-3K hardware kit + $300-500/month SaaS. Natural upsell from Plasma Consumable Life customers.
- **Capital**: $300-400K to first revenue (9-12 months)
- **Key strength**: Natural expansion of Plasma Consumable product (same customer, same sensor infrastructure + acoustic sensor addition); creates a platform moat in plasma cutting intelligence.
- **Key risk**: Acoustic signal quality in noisy shop environments; may require noise-canceling algorithms. More complex integration than consumable prediction alone.

### Press Brake Angle Measurement AI (Feasibility: 7/10)
- **Product**: Retrofit vision system (2 industrial cameras + edge AI box) that mounts on any press brake and provides real-time bend angle measurement with AI-driven compensation recommendations. Achieves +/-0.3 degree accuracy, comparable to $200K+ machines with built-in systems.
- **Technology**: Machine vision with structured light or stereo cameras, edge AI inference (angle detection + material behavior prediction), integration with press brake controller for ram depth adjustment recommendations.
- **Market**: 50,000+ legacy press brakes in North America (5-30+ years old) without built-in angle measurement. Target shops that cannot justify $200K+ for a new machine with built-in measurement.
- **Revenue model**: $3-5K hardware kit + $200-350/month SaaS per machine. Optional calibration service.
- **Capital**: $300-450K to first revenue (9-12 months)
- **Key strength**: Large installed base of legacy machines creates immediate addressable market; clear ROI through labor savings; natural companion product to SpringbackAI (same customer).
- **Key risk**: Achieving sub-0.5-degree accuracy with commodity cameras in dirty, vibrating shop environments; may require more expensive industrial cameras, pushing hardware cost up.

---

## Summary

| Stage | In | Promoted | Rejected |
|-------|-----|----------|----------|
| Step 1 | 10 | 7 | 3 |
| Step 2 | 7 | 6 | 1 |
| Step 3 | 6 | 5 | 1 |
| Step 4 | 5 | 4 | 1 |
| Step 5 | 4 | 4 | -- |

**Graduates this cycle**: 4 (Plasma Consumable Life Prediction, SpringbackAI, Plasma Parameter AI, Press Brake Angle Measurement AI)

**Top pick**: Plasma Consumable Life Prediction (9/10 feasibility) -- Extreme capital efficiency ($150-250K), zero competition, immediate ROI, natural platform expansion path. This is the highest-conviction idea in recent cycles.

**Platform strategy note**: The top 3 graduates form a coherent platform play in metal fabrication shops:
1. Start with Plasma Consumable Life Prediction (wedge product, easiest sale, fastest revenue)
2. Expand to Plasma Parameter AI (same hardware + acoustic sensors, same customer)
3. Cross-sell SpringbackAI to the same shops (they also run press brakes)
4. Add Press Brake Angle Measurement as hardware upsell

This "metal fab shop intelligence platform" approach could reach $50M ARR within 5 years by owning the AI layer across cutting and bending operations in mid-market fabrication shops.