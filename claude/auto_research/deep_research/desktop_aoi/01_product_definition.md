# 01 Product Definition: Desktop AI-Powered AOI

## Problem Statement

**Who:** Small PCB assembly shops (1-50 employees), prototype houses, and small contract manufacturers (CMs) producing 100-10,000 boards/month. These shops handle 5-50 unique board designs at any given time.

**How painful:** Defective boards that ship cost 10-100x more to fix in the field than at the assembly line. A single missed solder bridge on a $200 board can cause a $5,000 field failure (RMA, diagnosis, repair, re-ship, customer trust erosion). Small shops currently lose 2-5% of revenue to quality escapes. For a shop doing $1M/year in assembly services, that is $20K-$50K in annual waste -- enough to justify a $5K tool with 4-10 month payback.

**What they do today:**
1. Manual visual inspection under magnification (3-10x loupe or stereo microscope) -- slow, fatiguing, inconsistent, miss rate 20-40% for subtle defects
2. Spot-check with multimeter/ICT for critical nets only
3. Accept higher defect escape rates as "cost of doing business"
4. Occasionally outsource to a CM with inline AOI for high-reliability jobs (losing margin)

## Product Scope v1 (Three Core Features)

1. **One-Click Board Learning:** Import Gerber/ODB++ files + pick-and-place CSV, or use guided camera capture of a known-good board. System auto-generates inspection recipe in <10 minutes per new board design. No ML expertise required.

2. **Automated Defect Detection:** Identifies the top 5 defect classes that cause 90% of field failures:
   - Solder bridges (shorts)
   - Missing components
   - Tombstoned/billboarded components
   - Wrong polarity (capacitors, diodes, ICs)
   - Insufficient solder / cold joints

3. **Pass/Fail Dashboard with Evidence:** Each inspected board gets a pass/fail verdict with highlighted defect regions, confidence scores, and exportable PDF reports for customer quality documentation.

**What v1 Does NOT Do:**
- 3D solder volume measurement (requires structured light or laser, adds $10K+ to BOM)
- BGA/hidden joint inspection (requires X-ray)
- Inline conveyor integration (v1 is manual load, operator places board on stage)
- Component value verification via OCR of markings (future feature)
- Automated rework guidance

## User Workflow (Day 1)

1. **Unbox & Setup (30 min):** Place desktop unit on workbench. Connect USB-C to included mini PC (or customer's PC). Power on LED ring light. Launch InspectAI software.

2. **Calibrate (5 min):** Place included calibration target on stage. Software guides operator through focus adjustment and color calibration. One-time per installation.

3. **Create First Inspection Program (10 min):**
   - Option A: Import Gerber + BOM + pick-and-place files from KiCad/Eagle/Altium
   - Option B: Place a known-good board, capture reference image, software auto-segments components
   - Confirm/adjust component regions on screen

4. **Inspect First Board (30 sec/board):**
   - Place board on stage (manual, aligned to corner pins)
   - Press "Inspect" button (or foot pedal)
   - Camera captures image, AI processes in 2-5 seconds
   - Screen shows PASS (green) or FAIL (red) with defect locations highlighted

5. **Review & Ship:** Operator reviews any flagged defects, confirms or dismisses, board moves to shipping or rework queue.

## Pricing Model

| Tier | Price | Includes |
|------|-------|----------|
| Hardware Kit | $4,995 one-time | Camera, lens, LED ring, stage, mounting arm, cables |
| Software License | $199/month | Inspection software, model updates, 5 board programs |
| Additional Programs | $49/month per 10 | For shops with many board designs |
| Premium Support | $99/month | Phone support, custom model training, priority updates |

**Justification:**
- Hardware at $4,995 = 2.8x BOM cost ($1,800), healthy but not egregious for B2B industrial equipment
- Subscription creates recurring revenue ($2,388-$3,576/year per customer)
- Total Year 1 cost to customer: $7,383-$8,571 -- still 6-10x cheaper than Koh Young/Mirtec
- Customer payback period: 2-4 months (based on preventing $20-50K/year in defect escapes)
- $199/month subscription anchored to "less than one hour of technician time per month"

**Alternative consideration:** Pure hardware sale at $7,500-$9,000 with annual support contract. Simpler to sell but loses recurring revenue. May need to test both with early customers.

## Ideal First Customer Profile

- **Company size:** 5-20 employees
- **Revenue:** $500K-$3M/year
- **Location:** US (West Coast or Texas -- electronics manufacturing clusters)
- **Production:** 500-5,000 boards/month across 10-30 active designs
- **Current QC:** Manual inspection, has had at least one costly quality escape in past 12 months
- **Decision maker:** Owner or production manager (same person in shops this size)
- **Technical sophistication:** Uses KiCad or Altium, comfortable with software tools
- **Buying behavior:** Already invests in equipment (reflow oven, pick-and-place); views $5K as reasonable tooling purchase, not a major capital decision
- **Pain signal:** Recently lost a contract due to quality concerns, OR recently received a customer complaint about defect escapes
