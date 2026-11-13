# 03 Feasibility & Prototype Plan: Desktop AI-Powered AOI

## Architecture Overview

```
[Physical Layer]
20MP Industrial Camera (USB3) --> Mini PC (Jetson Orin Nano or Intel N100)
Telecentric Lens (0.5x)     --> GPU inference (TensorRT / OpenVINO)
LED Ring Light (adjustable)  --> Software UI (Electron/Qt)
Manual Stage + Alignment Pins

[Software Stack]
Image Capture --> Pre-processing --> CNN Inference --> Post-processing --> UI
     |                                    |
     v                                    v
Gerber/BOM Parser              Model Registry (cloud)
     |                                    |
     v                                    v
Golden Reference             Federated Training Pipeline
```

**Processing Pipeline:**
1. Camera captures 20MP image (5472x3648 px, ~10um/px resolution for 150mm PCB)
2. Lens distortion correction + color normalization
3. Board alignment via fiducial detection
4. Component region extraction (from BOM/pick-and-place or golden reference)
5. Per-component CNN classification (defect/no-defect + defect type)
6. Aggregate results, generate pass/fail verdict
7. Display results with highlighted regions in UI

## Bill of Materials (Prototype Unit)

| Item | Specific Part | Cost | Confidence |
|------|--------------|------|------------|
| Camera | Allied Vision Alvium 1800 U-2040 (20MP, USB3, Sony IMX183) | $850 | VERIFIED (Allied Vision website) |
| Telecentric Lens | Opto Engineering TC23036 (0.5x, 2/3" sensor) | $420 | ASSUMED (based on Opto Engineering catalog; exact model may need sizing adjustment) |
| LED Ring Light | Smart Vision Lights RM75-WHI (75mm ring, white, analog dimming) | $180 | VERIFIED (SVL distributor pricing) |
| Light Controller | Smart Vision Lights LFC-100 strobe controller | $95 | VERIFIED |
| Mini PC (Option A) | NVIDIA Jetson Orin Nano 8GB Developer Kit | $499 | VERIFIED (NVIDIA store) |
| Mini PC (Option B) | Intel NUC 13 Pro (i5-1340P, 16GB RAM, 512GB SSD) | $580 | VERIFIED (Intel/Amazon) |
| Stage/Fixture | Custom CNC aluminum plate + 3D-printed alignment jig | $120 | ASSUMED (based on PCBWay CNC + Shapeways quotes) |
| Mounting Arm | Diagnostic Instruments SMS20 boom stand | $185 | VERIFIED (microscope supply catalog) |
| Cables/Connectors | USB3 cable (active, 3m) + power supplies + misc | $45 | ASSUMED |
| Enclosure | Sheet metal housing (prototype: 3D printed) | $80 | ASSUMED |
| Calibration Target | Edmund Optics dot target #57-895 | $65 | VERIFIED |
| **TOTAL BOM (prototype)** | | **$2,119** (Option A) / **$2,200** (Option B) | |

**Production BOM target (at 100 units):** $1,500-$1,800 via volume pricing on camera (Allied Vision provides OEM pricing at 50+ units, ~30% discount) and Chinese-sourced optics.

**Alternative lower-cost camera options (UNVERIFIED, needs testing):**
- Basler ace 2 a2A5328-15ucBAS (20MP, USB3): ~$600
- FLIR/Teledyne BFS-U3-200S6C (20MP, USB3): ~$700
- The Imaging Source DFK 33UX183 (20MP, USB3): ~$650

## Software Stack

| Component | Technology | License | Cost |
|-----------|-----------|---------|------|
| OS | Ubuntu 22.04 LTS (Jetson) or Windows 11 (Intel NUC) | Free / OEM | $0-$130 |
| Camera SDK | Allied Vision Vimba X SDK | Free with camera | $0 |
| Image Processing | OpenCV 4.x | Apache 2.0 | $0 |
| ML Framework | PyTorch 2.x + TorchVision | BSD | $0 |
| Inference Runtime | TensorRT (Jetson) or OpenVINO (Intel) | Free | $0 |
| Gerber Parser | gerbonara (Python) | Apache 2.0 | $0 |
| Pick-and-Place Parser | Custom (CSV/Excel) | N/A | $0 |
| UI Framework | Qt 6 (PySide6) or Electron | LGPL / MIT | $0 |
| Model Training | PyTorch + Weights & Biases | Free tier | $0 |
| Cloud Sync | AWS S3 + Lambda | Pay-per-use | ~$50/month |
| **Total Software Cost** | | | **$0-$180** |

**Training Datasets (for initial model):**
- HRIPCB dataset (1,386 images, 6 defect types): Free, academic
- DeepPCB dataset (1,500 pairs): Free, academic
- PCB-DATASET (Kaggle, 693 images): Free
- Self-collected data from prototype testing: 0 cost (time only)
- **Gap:** Academic datasets are small and not representative of real production. Will need 5,000+ real-world images for production model. Plan: collect from beta customers with permission.

## Step-by-Step Build Instructions (First Prototype)

### Phase 1: Hardware Assembly (Week 1-2)

1. **Order components** (lead times: camera 1-2 weeks, lens 2-3 weeks, rest 3-5 days)
2. **Design and fabricate stage:**
   - CNC mill 200x200mm aluminum plate with M6 threaded holes for alignment pins
   - 3D print corner alignment brackets (adjustable for different board sizes)
   - Mount plate on anti-vibration pads
3. **Assemble optical column:**
   - Mount camera on boom stand
   - Attach telecentric lens (C-mount)
   - Mount LED ring around lens barrel using 3D-printed adapter
   - Set working distance (~100mm for 0.5x telecentric at this sensor size)
4. **Connect electronics:**
   - Camera --> USB3 --> Mini PC
   - LED controller --> LED ring
   - Power supplies
5. **Verify image quality:**
   - Capture test images of PCB at various positions on stage
   - Verify resolution (target: 10-15um/pixel, sufficient to see 0402 components and solder joints)
   - Verify uniform illumination (< 10% variation across field of view)

### Phase 2: Software MVP (Week 2-6)

1. **Camera interface (Week 2):**
   - Vimba X SDK integration
   - Live preview, single-shot capture, exposure/gain control
   - Save 16-bit TIFF for maximum dynamic range

2. **Image preprocessing (Week 3):**
   - Lens distortion calibration (checkerboard method)
   - Color normalization (white balance to reference)
   - Fiducial detection for board alignment (template matching or blob detection)

3. **Board learning module (Week 3-4):**
   - Gerber parser: extract pad locations, component outlines
   - Pick-and-place parser: map component designators to physical positions
   - Golden reference capture: store aligned reference image
   - Component region extraction: crop individual component images

4. **Defect detection model (Week 4-5):**
   - Start with YOLOv8-m pre-trained on HRIPCB + DeepPCB
   - Fine-tune on custom-collected data (manually inspect 50 boards, photograph defects)
   - Export to TensorRT (Jetson) or OpenVINO (Intel) for inference
   - Target: <3 second inference per board (batch all component crops)

5. **UI and reporting (Week 5-6):**
   - Qt-based desktop app
   - Board overview with color-coded pass/fail per component
   - Click to zoom on any flagged region
   - PDF report generation (board image + defect list + timestamps)

### Phase 3: Integration & Testing (Week 6-8)

1. **End-to-end workflow testing** with 10 different board designs
2. **Measure false positive/negative rates** on intentionally defective boards
3. **Iterate on model** (add training data for failure modes found in testing)
4. **UX testing** with 2-3 target users (find local PCB shops, offer free inspection in exchange for feedback)
5. **Package into installable application** (AppImage on Linux, MSI on Windows)

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Fallback |
|------|-----------|--------|------------|----------|
| Telecentric lens field-of-view too small for large boards | MEDIUM | HIGH | Calculate FOV before ordering; 0.5x on 1" sensor = ~13mm x 9mm... TOO SMALL. Need different approach. | Use non-telecentric macro lens + software distortion correction, OR multi-image stitching |
| 20MP insufficient resolution for 0201/01005 components | LOW | MEDIUM | 10um/px is sufficient for 0402+ (most small shops). 0201 requires 5um/px. | Offer 2x optical zoom mode for fine-pitch areas |
| Model accuracy insufficient on real-world boards (vs. academic datasets) | HIGH | HIGH | Plan extensive data collection from beta customers. Start with conservative thresholds (more false positives, fewer escapes). | Hybrid approach: AI pre-screen + human confirmation of flagged defects |
| LED ring creates specular reflections on solder | MEDIUM | MEDIUM | Use diffuse dome lighting instead of ring. Test both. | Polarized lighting + cross-polarized camera filter |
| Inference too slow on target hardware (>5 sec) | LOW | MEDIUM | Profile early. YOLOv8-m runs at 5ms/image on Jetson Orin for 640x640 input. Component crop approach = many small inferences but still fast. | Batch processing, reduce model size, or upgrade to Orin NX |
| Camera vendor discontinues model | LOW | LOW | Allied Vision has broad portfolio; Sony IMX183 sensor used in 5+ cameras from different vendors | Swap to Basler or FLIR equivalent |
| Customer unwilling to share training data | MEDIUM | HIGH | Offer discount/free month for data sharing. All data anonymized. Clear data policy. | Self-fund data collection by buying/inspecting boards from PCB pooling services (JLCPCB, PCBWay) |
| Cognex/Keyence launches competing product within 12 months | LOW-MEDIUM | CRITICAL | Move fast. Build installed base. Create switching costs via custom-trained models. | Pivot to software-only (sell AI software to run on customer's existing camera) |

**CRITICAL RISK IDENTIFIED:** The telecentric lens approach has a fundamental field-of-view problem. A 0.5x telecentric lens on a 1" sensor gives only ~13mm x 9mm FOV -- far too small for a PCB. **Resolution:**
- Option A: Use a standard low-distortion macro lens (e.g., Tamron 23FM50SP 50mm) -- gives full board coverage but with some perspective distortion. Software correction handles this.
- Option B: Use a telecentric lens with much lower magnification (0.05x-0.1x) designed for large FOV machine vision (e.g., Edmund Optics 0.06x telecentric). These cost $2,000-$4,000.
- **Recommended:** Option A for prototype. Standard machine vision lens at $200-400 with software distortion correction. Upgrade to telecentric for production if justified.

**Revised BOM with corrected lens:**

| Item | Revised Part | Cost | Confidence |
|------|-------------|------|------------|
| Lens | Tamron 23FM50SP (50mm f/2.8, C-mount, low distortion) | $280 | VERIFIED |
| OR | Edmund Optics 35mm f/2.0 C-mount #67-715 | $310 | VERIFIED |

This reduces BOM to ~$1,950-$2,000 for prototype.

## Validation Plan

**Success Criteria for Prototype:**
1. Detect solder bridges with >90% recall, <5% false positive rate (measured on 100 boards with known defects)
2. Detect missing components with >95% recall, <2% false positive rate
3. Total inspection time <10 seconds per board (image capture + inference + display)
4. New board setup time <15 minutes (from BOM upload to first inspection)
5. System stable for 8-hour operation without crashes or drift

**How to Test:**
1. Acquire 20 different PCB designs (buy from JLCPCB assembled, some with intentional errors)
2. Manually create defects on additional boards (remove components, bridge pads with solder)
3. Build ground-truth dataset: 100 boards x 50 components = 5,000 component images with labels
4. Run blind test: prototype inspects boards, compare results to ground truth
5. Calculate precision, recall, F1 per defect class

**Timeline:**
- Weeks 1-2: Hardware assembly and verification
- Weeks 3-6: Software development
- Weeks 7-8: Integration and internal testing
- Weeks 9-10: Beta testing with 2-3 friendly shops
- Weeks 11-12: Iterate on feedback, prepare for first sale
- **Total: 12 weeks (3 months) to first customer-ready prototype**

## Total Cost and Time Estimate

| Category | Cost | Time |
|----------|------|------|
| Hardware (prototype) | $2,000 | 2 weeks (lead time) |
| Software development (founder's time) | $0 (sweat equity) | 6 weeks full-time |
| Test boards and materials | $500 | 1 week |
| Cloud/hosting/tools | $200 | Ongoing |
| Beta testing expenses (travel, boards) | $300 | 2 weeks |
| **Total to first prototype** | **$3,000** | **12 weeks** |
| **Total to first 10 sales** (add marketing, 5 more units) | **$25,000** | **6 months** |
| **Total to sustainable business** (50 units, team of 2) | **$150,000-$245,000** | **12 months** |

## Founder-Market Fit Assessment

**Founder profile:** Hooman Shariati -- AI/ML infrastructure engineer at Adobe, deep Python/systems/cloud expertise, no hardware background, no PCB manufacturing industry connections.

| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Technical (ML/AI) | 5/5 | Core competency. Training CNNs, deploying inference pipelines, building MLOps -- all directly applicable. |
| Technical (Hardware) | 2/5 | No optics/camera/lighting experience. Will need to learn machine vision fundamentals (lens selection, lighting geometry, sensor specs). Mitigated: abundant educational resources (Edmund Optics guides, machine vision textbooks). |
| Technical (Software product) | 4/5 | Systems engineering skills transfer. Building a desktop application with camera integration is learnable. |
| Domain expertise | 1/5 | No PCB manufacturing experience. Does not know the daily workflow of a PCB assembler, their pain points beyond theoretical, or their buying behavior. |
| Network/connections | 1/5 | No connections to PCB assembly shops, contract manufacturers, or electronics manufacturing community. |
| Sales ability (B2B hardware) | 2/5 | Engineering manager experience helps with communication but selling $5K hardware to small manufacturers is a different skill. |
| Passion/interest | 3/5 | Interesting technical challenge but no evident deep passion for PCB manufacturing specifically. |

**Overall Founder-Market Fit: 2.5/5 -- WEAK**

**Key gaps and mitigations:**
1. **Hardware gap:** Partner with a mechanical/optical engineer for hardware design. Or: use the 3-month prototype phase to learn machine vision hands-on.
2. **Domain gap:** Spend 2 weeks visiting local PCB assembly shops before building anything. Join IPC (electronics manufacturing trade association). Attend SMTA chapter meetings.
3. **Network gap:** Cold outreach to PCB shops via MacroFab community, r/PrintedCircuitBoard, EEVBlog forums, local makerspaces with PCB capability.
4. **Sales gap:** First 10 customers via direct relationship-building, not traditional sales. Offer free pilot program.

**Honest assessment:** This is a hardware-meets-domain-expertise play being pursued by a software/ML person. The ML is the EASY part. The hard parts are: optical system design, manufacturing the hardware reliably at scale, understanding customer workflows deeply enough to build the right UX, and selling to a market you have no connections to. Many hardware startups by software founders fail on these dimensions.
