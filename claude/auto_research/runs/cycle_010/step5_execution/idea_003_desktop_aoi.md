# Execution Plan: Desktop AI-Powered AOI for Small PCB Assemblers

## 5a. Product Definition
**Core value proposition**: Professional PCB inspection for 1/10th the price — AI catches defects that human eyes miss.
**MVP features**: (1) AI-powered solder joint classification (good/insufficient/bridge/cold), (2) component presence/absence/polarity check, (3) inspection report with annotated images
**Success metrics**: 95%+ defect detection rate; <5% false positive rate; 30-second inspection per board; 50 units sold in 6 months

## 5b. Architecture
- Hardware: 20MP industrial camera (FLIR/Basler, $800) + telecentric lens ($400) + LED ring light ($200) + XY stage or manual jig ($200) + mini-PC (Intel N100, $200)
- Software: Python + OpenCV + custom CNN (trained on PCB defect datasets) + React Electron GUI
- Training data: Public PCB defect datasets (HRIPCB, DeepPCB) + customer board images

## 5c. BOM: ~$1,800; sell at $5,000 + $1,500/year software subscription

## 5d. Timeline
- Weeks 1-6: Collect/label PCB defect training data (partner with 3 assembly shops)
- Weeks 4-10: Train defect detection CNN (solder, component, polarity)
- Weeks 6-12: Build hardware integration (camera + lighting + jig + software)
- Weeks 10-14: Beta with 5 shops (varied board types)
- Weeks 12-18: Iterate on few-shot learning for new board types
- Weeks 16-22: First production batch (50 units)

## 5e. Cost Estimate
- ML/vision engineer (8 months): $120K
- Hardware/integration engineer (4 months): $50K
- Software/UI (4 months): $50K
- Prototypes + cameras + parts: $15K
- Training data partnerships: $10K
- **Total: ~$245K to first revenue**

## Revenue: 200 units/year × $5K + 200 × $1.5K subscription = $1M + $300K = **$1.3M Year 1**
