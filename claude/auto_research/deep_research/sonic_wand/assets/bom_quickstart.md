# Sonic Dry-Vacuum Wand: Quick-Start BOM (Prototype v1)

**Estimated Total Cost:** $420–$770  
**Assembly Time:** 10–12 weeks  
**Supplier Mix:** AliExpress (65%), Amazon (25%), Specialized (10%)

---

## SECTION A: CORE COMPONENTS (Order Immediately)

### A1. Piezoelectric Transducer + Driver

| Item | Quantity | Source | Search Term | Est. Lead Time | Cost |
|------|----------|--------|-------------|----------------|------|
| 25–40 kHz ultrasonic cleaning transducer | 1 | AliExpress / Alibaba | "25 kHz ultrasonic transducer with driver" | 2–3 weeks | $60–$100 |
| (Request datasheet with displacement specs) | — | — | — | — | — |

**Backup Plan (if unavailable):**
- PZT-8 sandwich transducer from Piezo Systems → 6–8 week lead time, $150–$300

**Action:** Email 5 suppliers requesting:
- Operating frequency: 25–28 kHz
- Displacement amplitude: 10–15 µm
- Power output: 6–8W
- Datasheet with resonant frequency curve

---

### A2. BLDC Micro-Vacuum Pump

| Item | Quantity | Source | Search Term | Est. Lead Time | Cost |
|------|----------|--------|-------------|----------------|------|
| 12V BLDC diaphragm pump, oil-free | 1 | AliExpress / Alibaba or McMaster-Carr | "12V BLDC pump 5 LPM" | 2–4 weeks | $80–$150 |
| (Request performance curve: pressure vs. flow) | — | — | — | — | — |

**Backup Plan (if unavailable):**
- Medical portable suction pump (wound care grade) → confirmed FDA-cleared, $100–$200

**Action:** Email suppliers requesting:
- Nominal voltage: 12V DC
- Flow rate: 4–5 LPM
- Suction pressure: 18–22 kPa
- Current draw at full load
- Performance curve (pressure-flow graph)

---

### A3. Lithium-Ion Battery Pack (2S1P, 5000 mAh)

| Item | Quantity | Source | Search Term | Est. Lead Time | Cost |
|------|----------|--------|-------------|----------------|------|
| 2S 21700 lithium-ion battery pack (5000 mAh) with integrated BMS | 1 | Amazon or AliExpress | "2S 21700 5000 mAh battery pack USB-C" | 1–2 weeks | $40–$70 |
| USB-C power charger (18W PD) + buck converter | 1 | Amazon | "18W USB-C PD charger" + "buck converter 8.4V" | 1–2 days | $20–$30 |

**Verify on checkout:**
- BMS includes low-temp cutoff (< 0°C) ✓
- BMS includes high-temp alarm (> 60°C) ✓
- Includes JST-XH balance connector ✓
- Rated for continuous discharge ≥ 10A ✓

---

### A4. Microcontroller + Sensors

| Item | Quantity | Source | Search Term | Est. Lead Time | Cost |
|------|----------|--------|-------------|----------------|------|
| STM32F103C8T6 "Blue Pill" dev board (or Arduino Uno) | 1 | AliExpress / Amazon | "STM32F103 Blue Pill" | 1–2 weeks | $5–$15 |
| NTC thermistor 10kΩ (Murata NTC0603N103F3950) | 1 | Amazon / Digi-Key | "NTC thermistor 10K 3470K" | 2–3 days | $2–$5 |
| MPU6050 3-axis accelerometer breakout | 1 | Amazon / AliExpress | "MPU6050 accelerometer I2C" | 1–2 weeks | $3–$8 |
| IR2104 half-bridge MOSFET driver (4-pin DIP) | 2 | Digi-Key / Mouser | "IR2104 DIP8" | 1–3 days | $2–$4 each |
| 10kΩ resistor 1% (pull-up for thermistor) | 5 | Amazon / Digi-Key | "10K resistor 1/4W" | 1–2 days | $0.05 each |
| USB-to-Serial adapter (FTDI or CH340) | 1 | Amazon | "FTDI USB serial adapter" | 1–2 days | $5–$10 |

**Total Sensors/Control:** ~$30–$60

---

### A5. Micro-Atomizer / Misting System

| Item | Quantity | Source | Search Term | Est. Lead Time | Cost |
|------|----------|--------|-------------|----------------|------|
| 10 mL USB humidifier with nebulizer cartridge | 1 | Amazon | "USB humidifier mini 10mL" | 1–3 days | $8–$15 |
| Silicone micro-bore tubing (1/16" ID, 1 meter) | 1 | Amazon / Home Depot | "silicone tubing 1/16 inch ID" | 1–2 days | $3–$5 |
| Cyclopentasiloxane (D5) or isoparaffin oil (100 mL) | 1 | Alibaba (cosmetic supplier) | "cyclopentasiloxane D5" or "isoparaffin oil" | 2–4 weeks | $10–$20 |
| Distilled water (1 liter) | 1 | Amazon / Pharmacy | "distilled water 1L" | 1 day | $2–$3 |

**Fluid Mix Recipe:**  
- 80 mL distilled water + 20 mL D5 siloxane
- Optional: 2–5 mL glycerin (for stickier coupling)

**Total Misting:** ~$25–$45

---

### A6. Shroud & Housing

| Item | Quantity | Source | Search Term | Est. Lead Time | Cost |
|------|----------|--------|-------------|----------------|------|
| Shapeways SLS nylon mold (3D-printed) for LSR casting | 1 | Shapeways.com (upload CAD) | — | 2–4 weeks | $60–$120 |
| Smooth-On Mold Max 60 LSR casting kit (1:1 ratio, 1 lb) | 1 | Amazon / Smooth-On.com | "Smooth-On Mold Max 60" | 2–3 days | $30–$50 |
| Mold release agent (Pam or dedicated release) | 1 | Amazon / Home Depot | "silicone mold release spray" | 1 day | $5–$8 |
| 3D-printed SLS Nylon main housing body | 1 | Shapeways.com (upload CAD) | — | 2–4 weeks | $60–$150 |
| M2 brass standoffs + M2 screws (assortment) | 1 pack | Amazon | "M2 brass standoff assortment" | 1–2 days | $8–$12 |

**Total Shroud & Housing:** ~$170–$350

---

## SECTION B: ELECTRONICS & INTERCONNECTS (Order Immediately)

| Item | Quantity | Source | Search Term | Est. Lead Time | Cost |
|------|----------|--------|-------------|----------------|------|
| Breadboard + jumper wire kit | 1 | Amazon | "solderless breadboard 830 points + jumper wires" | 1–2 days | $8–$15 |
| 22 AWG silicone wire (assorted colors, 10m total) | 1 | Amazon | "silicone wire 22 AWG assorted" | 1–2 days | $5–$8 |
| USB-C connector breakout board | 1 | Amazon / AliExpress | "USB-C breakout board" | 1–2 weeks | $3–$5 |
| Tactile push-button switches (6mm, 5V, 20 pack) | 1 | Amazon | "tactile switch 6mm 20 pack" | 1 day | $3–$5 |
| JST-PH connectors (2.0mm, assorted kit) | 1 | Amazon | "JST-PH connector kit" | 1–2 days | $5–$8 |
| Solder + soldering iron (if not already owned) | 1 | Amazon | "soldering iron 60W + solder wire" | 1 day | $15–$25 |

**Total Electronics & Interconnects:** ~$50–$80

---

## SECTION C: OPTIONAL / SECONDARY (Order Later)

| Item | Quantity | Source | Search Term | Est. Lead Time | Cost |
|------|----------|--------|-------------|----------------|------|
| OLED display module (0.96" 128x64 I2C) | 1 | Amazon / AliExpress | "OLED 128x64 I2C display" | 1–2 weeks | $5–$10 |
| Real-time clock module (DS3231 I2C) | 1 | Amazon / AliExpress | "DS3231 RTC module" | 1–2 weeks | $2–$5 |
| Data logging SD card module (SPI) | 1 | Amazon / AliExpress | "microSD card reader SPI" | 1–2 weeks | $2–$5 |

---

## ORDERING CHECKLIST

### Week 1 (Days 1–3): High-Priority Orders

- [ ] **AliExpress/Alibaba Searches:**
  - [ ] "25 kHz ultrasonic transducer" (5 suppliers, request quotes)
  - [ ] "12V BLDC pump 5 LPM" (5 suppliers, request specs)
  
- [ ] **Amazon One-Day Delivery:**
  - [ ] Breadboard + jumper wires
  - [ ] 22 AWG silicone wire
  - [ ] Tactile push-buttons
  - [ ] Soldering iron + solder
  - [ ] USB humidifier mini

- [ ] **Electronics (Digi-Key / Mouser):**
  - [ ] IR2104 driver ICs (2x)
  - [ ] 10kΩ resistors (5x)
  - [ ] USB-serial adapter

### Week 2 (Days 8–10): Component Arrivals + Shapeways

- [ ] **Receive & Test:**
  - [ ] STM32 Blue Pill + USB adapter → flash SimpleFOC test
  - [ ] MPU6050 accelerometer → test I2C communication
  - [ ] NTC thermistor → verify ADC reading

- [ ] **Shapeways CAD Upload:**
  - [ ] Design shroud mold in Fusion 360
  - [ ] Design main housing body in Fusion 360
  - [ ] Upload both for SLS nylon printing
  - [ ] Expected arrival: ~4 weeks

- [ ] **Battery Delivery:**
  - [ ] Receive 2S battery pack
  - [ ] Test USB-C charging circuit
  - [ ] Verify BMS voltage monitoring

### Week 3+: Supplier Responses

- [ ] **Email Responses from Transducer/Pump Suppliers:**
  - [ ] Review datasheets
  - [ ] Confirm specs match design requirements
  - [ ] Place orders for stock components

- [ ] **Alibaba D5 Siloxane:**
  - [ ] Order cosmetic-grade cyclopentasiloxane (bulk, ~$10)
  - [ ] Expected arrival: 3–4 weeks from China

---

## TOTAL BOM COST BREAKDOWN

| Category | Min Cost | Max Cost |
|----------|----------|----------|
| Piezo transducer + driver | $60 | $100 |
| BLDC pump | $80 | $150 |
| Battery + charger | $55 | $95 |
| Microcontroller + sensors | $30 | $60 |
| Micro-atomizer + fluid | $25 | $45 |
| Shroud & housing (3D print + LSR) | $170 | $350 |
| Electronics & interconnects | $50 | $80 |
| **TOTAL PROTOTYPE** | **$470** | **$880** |

---

## CRITICAL DEPENDENCIES (Longest Lead Items)

1. **Shapeways SLS Nylon Printing:** 2–4 weeks (order ASAP)
2. **BLDC Pump (Custom Spec):** 2–4 weeks (if not in stock)
3. **Piezoelectric Transducer (Integrated):** 2–3 weeks (stock) or 6–8 weeks (custom)
4. **D5 Siloxane from Alibaba:** 3–4 weeks

**Recommendation:** Start ordering **Week 1 immediately**. While waiting for long-lead items, develop firmware and CAD designs in parallel.

---

## ALTERNATE FASTER PATH (12–14 days to first test)

If you want to **test the concept quickly** with whatever is in stock:

| Item | Quick-Source | Lead Time | Cost |
|------|--------------|-----------|------|
| Generic 28 kHz ultrasonic transducer (from cleaner) | Disassemble old cleaner + buy driver board | 1–2 weeks | $20–$30 |
| Small 12V DC motor pump (aquarium) | Amazon same-day | 1 day | $15–$25 |
| 2S battery (pre-built) | Amazon 1-day | 1 day | $40–$60 |
| STM32F103 Blue Pill | AliExpress | 1–2 weeks | $5–$10 |
| OLED display + sensors | Amazon 1-day | 1 day | $20–$30 |
| Plastic housing (PETG 3D print) | Local 3D printer | 1–2 days | $20–$40 |

**Fast-Track Total:** ~$120–$190 for a **proof-of-concept** (lower power, noisier, but works)

---

## NEXT ACTION

1. **Save this BOM to your phone**
2. **Start Alibaba/AliExpress searches for piezo + pump** (do this first—lead times kill)
3. **Use Fusion 360 to design shroud CAD** (parallelize with procurement)
4. **Order fast items from Amazon** (1–2 day delivery to get momentum)

Good luck! 🚀

