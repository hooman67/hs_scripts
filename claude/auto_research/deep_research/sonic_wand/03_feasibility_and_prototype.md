# Sonic Dry-Vacuum Wand: First Prototype Execution Plan

**Goal:** Build a working proof-of-concept that validates the core mechanics (piezo acoustic coupling, vacuum debris capture, closed-loop thermal control) before scaling to consumer manufacturing.

**Timeline:** 10-12 weeks from component sourcing to functional prototype  
**Estimated BOM Cost:** $420–$580 (prototype-grade, not production volumes)

---

## Phase 1: Component Sourcing & Procurement (Weeks 1–2)

### 1.1 Piezoelectric Transducer (25–28 kHz, 10–15 µm displacement)

**Recommended Approach:**  
Start with a **stock piezo ultrasonic cleaning transducer** rather than a fully custom PZT-8 sandwich. These are designed for exactly this frequency range and come pre-tuned.

| Component | Specification | Recommended Model | Supplier | Est. Cost |
|-----------|---------------|-------------------|----------|-----------|
| **Piezo Transducer** | 25–40 kHz, 1–2W output, bolt-mount | Koike Aronson UT-100 or similar cleaning transducer | Alibaba (ultrasonic suppliers), eBay, AliExpress | $35–$80 |
| **Piezo Driver Circuit** | 24–36V boost from battery, phase control | Off-the-shelf ultrasonic driver board (Arduino-compatible) | Ebay/AliExpress ultrasonic cleaner kits | $25–$45 |

**Why This Works:**  
- Cleaning transducers are mass-produced and proven at your target frequency
- They come with integrated mounting, eliminating custom machining
- Driver boards are cheap and readily available as Arduino breakouts

**Action:** Search "25 kHz ultrasonic transducer with driver board" on AliExpress or Alibaba. Look for items labeled "ultrasonic cleaning transducer module."

---

### 1.2 BLDC Vacuum Pump (12V, 4–5 LPM, 18–22 kPa)

**Recommended Approach:**  
Use a **medical-grade portable suction pump** designed for wound care or a **mini air pump from industrial HVAC suppliers**. Avoid aquarium pumps (too weak); prioritize BLDC over brushed (longer life, quieter).

| Component | Specification | Recommended Model | Supplier | Est. Cost |
|-----------|---------------|-------------------|----------|-----------|
| **BLDC Micro-Pump** | 12V, 4–5 LPM, oil-free | Ametek BLDC pump (model BLDC-S-5000 or similar) or medical suction pump | Alibaba (pump suppliers), McMaster-Carr, Grainger | $50–$120 |
| **Pump Adapter/Shroud Connector** | Silicone hose fittings (1/4" barbed connectors) | Standard barbed connectors | Amazon, Home Depot | $5–$15 |

**Why This Works:**  
- Medical suction pumps are already optimized for skin-safe pressure gradients
- BLDC units are quieter and more efficient than brushed alternatives
- Widely available on industrial supply sites with detailed performance curves

**Action:** Search "12V BLDC micro-pump 5 LPM" or "portable medical suction pump 12V" on AliExpress/Alibaba. Request performance curve (pressure vs. flow) from suppliers to verify spec match.

---

### 1.3 Battery Pack (2S1P, 21700, 5000 mAh, 7.4V nominal)

**Recommended Approach:**  
Don't assemble cells yourself in a prototype. Buy a **pre-assembled 2S battery pack with integrated BMS** to avoid safety issues.

| Component | Specification | Recommended Model | Supplier | Est. Cost |
|-----------|---------------|-------------------|----------|-----------|
| **Battery Pack** | 2S1P 21700 5000 mAh, integrated BMS | Fenix ARB-L21 (single cell; need 2) or custom 2S pack | Amazon, AliExpress (battery shops), BatteryJunction | $40–$70 (for 2S pack) |
| **USB-C Charger** | 5V/2A USB-C charger with buck converter | Standard 18W USB-C PD charger + buck module | Amazon | $15–$25 |
| **Balance Connector** | JST-XH 2S balance lead | Standard JST-XH connector (included with many packs) | Amazon, AliExpress | Included |

**Why This Works:**  
- Pre-assembled packs ship with integrated protection circuits (thermal cutoff, overcharge protection)
- Eliminates risk of cell imbalance or fire during prototype testing
- USB-C charging is universal and safer than proprietary connectors

**Sourcing Tips:**
- Search "2S 21700 5000 mAh battery pack USB-C" on Amazon or AliExpress
- Ensure the BMS (Battery Management System) has **low-temperature cutoff** (below 0°C) and **high-temperature alarm** (above 60°C)
- Ask seller for BMS spec sheet showing discharge curve and thermal limits

---

### 1.4 Microcontroller & Sensors

**Recommended Approach:**  
Use an **Arduino-compatible microcontroller** (either native Arduino or an STM32 "blue pill" clone for lower cost) with integrated ADC for thermistor and accelerometer I2C.

| Component | Specification | Recommended Model | Supplier | Est. Cost |
|-----------|---------------|-------------------|----------|-----------|
| **Microcontroller** | 32-bit ARM, 3.3V/5V tolerant, ADC, I2C | Arduino Uno WiFi Rev2 (or STM32F103 "Blue Pill") | Arduino.cc, AliExpress | $20–$40 |
| **NTC Thermistor** | 10kΩ @ 25°C, β-value 3470K | Commonly sourced thermistor (Murata, Vishay) | Amazon, AliExpress | $2–$5 |
| **3-Axis Accelerometer** | I2C interface, ±16g range | ADXL345 breakout or MPU6050 | Amazon, AliExpress | $3–$8 |
| **MOSFET Driver** | 24–36V gate driver for piezo (4-pin DIP) | IR2104 or similar half-bridge driver | Digi-Key, Mouser | $2–$4 |

**Why This Works:**  
- Arduino ecosystem has hundreds of pre-built driver libraries for accelerometers and thermistors
- Easy to prototype without needing custom PCB design
- Can iterate firmware rapidly through USB serial upload

---

### 1.5 Micro-Atomizer / Misting System

**Recommended Approach:**  
Prototype with a **piezo micro-misting nebulizer cartridge** (the type used in portable humidifiers). For v1, avoid custom design.

| Component | Specification | Recommended Model | Supplier | Est. Cost |
|-----------|---------------|-------------------|----------|-----------|
| **Piezo Nebulizer** | 110 kHz piezo crystal, 5–8 mL/min flow | Generic 10mL USB humidifier cartridge with replaceable nebulizer | Amazon, AliExpress | $8–$15 |
| **Reservoir & Tubing** | 10 mL refillable bottle, silicone micro-bore tubing (1/16" ID) | Standard tubing from aquarium supply stores | Amazon, Home Depot | $5–$10 |
| **Fluid Mix** | 80% distilled water + 20% cosmetic-grade volatile siloxane or light plant ester | Cyclopentasiloxane (D5) or isoparaffin oil | Alibaba (cosmetic suppliers) or Amazon (beauty supply) | $10–$20 |

**Why This Works:**  
- Humidifier cartridges are proven micro-misting designs and cheap
- Piezo misters operate independently (no cooling required)
- Can be integrated into silicone shroud with simple 3D-printed mounting bracket

---

### 1.6 Silicone Shroud / Interface Head

**Recommended Approach:**  
For prototype, use **liquid silicone rubber (LSR) mold casting** rather than injection molding. Buy a pre-made mold or have one 3D-printed.

| Component | Specification | Material | Recommended Path | Est. Cost |
|-----------|---------------|----------|------------------|-----------|
| **Shroud Mold** | 40A durometer LSR, airtight seal contact surface | Silicone (liquid or solid) | Custom 3D-printed mold (from SLS nylon) + hand-cast LSR OR purchase generic suction cup attachment | $30–$80 |
| **LSR Casting Kit** | 1:1 ratio liquid silicone, catalyst, mixing cup, vacuum degasser | Dow Corning, Wacker, Momentive | Amazon or McMaster-Carr (Smooth-On Mold Max 60) | $25–$40 |

**Why This Works:**  
- Hand-casting LSR is faster than injection molding for prototypes
- SLS 3D-printed mold can be reused 5–10 times before degrading
- Cost is 1/100th of custom injection tooling

**Alternative (Faster):**  
Buy a **generic medical-grade suction cup** (like a silicone cup used for cupping therapy) and retrofit your vacuum/piezo head into it.

---

### 1.7 Structural Housing & PCB Mounting

**Recommended Approach:**  
3D-print the main handle and PCB enclosure in **Nylon (SLS) or Resin (SLA)** rather than PLA (too fragile).

| Component | Specification | Path | Est. Cost |
|-----------|---------------|------|-----------|
| **Main Enclosure** | Handle-shaped body, 120 mm long, battery compartment, circuit cavity | 3D model (CAD design) → Shapeways or local 3D printing service (SLS Nylon or SLA Resin) | $60–$150 |
| **Internal PCB Mount** | Plastic standoffs, M2 screws, internal cable routing clips | 3D-print standoffs into main body or use adhesive-backed rubber spacers | $5–$10 |
| **Connectors** | USB-C breakout connector (edge-mounted), ON/OFF switch (tactile button or rocker), OLED display (optional) | Generic USB-C connector + breadboard header + push-button from electronics store | $10–$20 |

---

### Summary: Week 1–2 Shopping List

| Category | Total Estimated Cost |
|----------|---------------------|
| Piezoelectric transducer + driver | $60–$125 |
| BLDC vacuum pump + shroud adapter | $55–$135 |
| Battery pack (2S 5000 mAh) + charger | $55–$95 |
| Microcontroller + sensors (thermistor, accel) | $30–$60 |
| Micro-atomizer + fluid + tubing | $23–$45 |
| Silicone shroud casting kit + mold | $55–$130 |
| 3D-printed housing (SLS nylon) | $60–$150 |
| Connectors, switches, misc. electronics | $15–$30 |
| **Total Prototype BOM** | **$420–$770** |

---

## Phase 2: Mechanical Assembly & Integration (Weeks 3–5)

### 2.1 Silicone Shroud Casting (Week 3)

**Step 1:** Order SLS 3D-printed mold from Shapeways or local service (2–3 day turnaround).

**Step 2:** Prepare mold by lightly greasing inner surfaces with release agent (Pam spray or dedicated mold release).

**Step 3:** Mix LSR per manufacturer instructions:
- 1:1 ratio (by weight) of Part A + Part B
- Stir slowly for 2 minutes (avoid air bubbles)
- Degas in vacuum chamber (or use a manual vacuum degasser) for 2 minutes to remove air

**Step 4:** Pour into mold cavity. Let cure per LSR manufacturer spec (typically 4–24 hours at room temp, or 30 min at 80°C in an oven).

**Step 5:** Demold by gently flexing mold or using a butter knife to pry edges.

**Result:** One silicone shroud with integrated vacuum port and acoustic tip cavity.

---

### 2.2 Piezoelectric Transducer Integration (Week 3)

**Step 1:** Install piezoelectric transducer into shroud cavity using a **thin layer of medical-grade silicone adhesive** (not epoxy, which will dampen vibrations).

**Step 2:** Connect piezoelectric transducer electrical leads to the driver board:
- **Red lead** → High voltage output (24–36V boost)
- **Black lead** → Ground
- **Phase line** (if applicable) → Phase control signal from microcontroller

**Step 3:** Mount driver board to main PCB enclosure using plastic standoffs and M2 screws.

**Critical Note:** The piezoelectric transducer **must vibrate freely**. Do not use rigid adhesives. Silicone encapsulant is acceptable; epoxy or polyurethane will kill acoustic transmission.

---

### 2.3 Vacuum Pump Integration (Week 4)

**Step 1:** Mount BLDC pump to bracket inside main handle enclosure using rubber vibration isolators (to reduce audible noise transmission).

**Step 2:** Connect pump intake hose to shroud vacuum port using barbed silicone connectors.

**Step 3:** Route pump outlet hose to **two-stage filter cartridge**:
- First stage: 0.3 µm electrostatic mesh (traps skin dander and particles)
- Second stage: Activated carbon foam (absorbs VOCs and odors)

**Step 4:** Connect pump electrical leads (red/black) to a **PWM (Pulse-Width Modulation) control circuit** on the main PCB:
- This allows firmware to adjust pump speed dynamically (e.g., ramp down near thermal limits)

**Filter Cartridge Design:**  
You can purchase pre-made cartridges online or 3D-print a holder and stack the two filter layers inside.

---

### 2.4 Micro-Atomizer Integration (Week 4)

**Step 1:** Install nebulizer cartridge into shroud using 3D-printed bracket.

**Step 2:** Connect 10 mL fluid reservoir to nebulizer inlet using micro-bore silicone tubing (1/16" ID).

**Step 3:** Wire nebulizer power leads to a **relay-controlled circuit** on main PCB (so firmware can trigger misting just before acoustic activation).

**Step 4:** Fill reservoir with test fluid:
- **80% distilled water + 20% volatile siloxane (D5) or isoparaffin**
- This mix evaporates rapidly after being vacuumed away

**Timing Synchronization:**  
Program firmware to execute this sequence every 3 seconds during active mode:
1. Trigger micro-atomizer (spray 0.1 mL micro-mist) → 100 ms
2. Wait 50 ms for mist to settle
3. Activate piezo transducer at full power → 1000 ms (acoustic agitation)
4. Run vacuum pump at 80% PWM → 800 ms (suction & evaporation)
5. Stop all systems → 1000 ms rest (allow cooling)

---

### 2.5 Battery & Power Management Integration (Week 4–5)

**Step 1:** Install 2S battery pack into battery compartment of main enclosure (vertically for best space efficiency).

**Step 2:** Wire battery leads through **integrated BMS** to power distribution:
- **Raw 7.4V** → Vacuum pump (direct or through buck converter if needed)
- **7.4V** → Boost converter input → 24–36V output to piezo driver
- **7.4V** → Micro-USB breakout for microcontroller 5V rail (via linear regulator)
- **5V** → Microcontroller logic, sensors, display

**Step 3:** Install USB-C charging connector on device exterior. Wire to charge controller board (pre-built module, ~$5 on AliExpress).

**Step 4:** Install ON/OFF rocker switch in series with battery positive, accessible on handle.

---

### 2.6 Thermal Sensor & Accelerometer Integration (Week 5)

**Step 1:** Mount NTC thermistor directly onto piezo transducer substrate using silicone-based thermal epoxy.

**Step 2:** Connect thermistor leads to ADC input on microcontroller (wire through a 10 kΩ pull-up resistor for voltage divider).

**Step 3:** Mount 3-axis accelerometer (ADXL345 breakout) to the transducer frame using adhesive mounting tape.

**Step 4:** Connect accelerometer to microcontroller via I2C bus (SDA/SCL lines with 4.7 kΩ pull-up resistors).

**Firmware Task:**  
Write ADC polling loop in firmware:
```
Every 100 ms:
  - Read thermistor ADC value → convert to °C
  - Read accelerometer X/Y/Z axes → compute resonant frequency deviation
  - If temp > 40°C: switch piezo driver to 50% PWM duty cycle
  - If accelerometer detects bone (rigid impedance spike): reduce power by 50%
```

---

## Phase 3: Firmware Development (Weeks 5–8)

### 3.1 Microcontroller Core Loop (Arduino/C++)

**Basic pseudocode for STM32 or Arduino:**

```cpp
#include <Wire.h>
#include <ADXL345.h>

// Pin definitions
const int THERMISTOR_PIN = A0;
const int PUMP_PWM_PIN = 5;
const int PIEZO_DRIVER_PIN = 6;
const int NEBULIZER_RELAY_PIN = 7;
const int POWER_BUTTON_PIN = 2;

// Constants
const float TEMP_LIMIT_C = 40.0;
const float ACCEL_BONE_THRESHOLD = 2.5; // g-force deviation
const int OPERATION_CYCLE_MS = 3000; // 3 second cycle

// Global state
bool system_active = false;
float piezo_power_factor = 1.0; // 0.0 to 1.0

ADXL345 accel;

void setup() {
  Serial.begin(9600);
  pinMode(PUMP_PWM_PIN, OUTPUT);
  pinMode(PIEZO_DRIVER_PIN, OUTPUT);
  pinMode(NEBULIZER_RELAY_PIN, OUTPUT);
  pinMode(POWER_BUTTON_PIN, INPUT_PULLUP);
  
  accel.begin();
}

void loop() {
  // Check power button
  if (digitalRead(POWER_BUTTON_PIN) == LOW) {
    system_active = !system_active;
    delay(500); // debounce
  }
  
  if (!system_active) {
    digitalWrite(PUMP_PWM_PIN, LOW);
    digitalWrite(PIEZO_DRIVER_PIN, LOW);
    return;
  }
  
  // ========== ACTIVE CYCLE ==========
  
  // Read thermal & accel sensors
  float temp_c = readThermistor();
  float accel_mag = readAccelerometer();
  
  // Adjust power based on sensors
  if (temp_c > TEMP_LIMIT_C) {
    piezo_power_factor = 0.5; // Thermal throttle
  } else {
    piezo_power_factor = 1.0;
  }
  
  if (accel_mag > ACCEL_BONE_THRESHOLD) {
    piezo_power_factor *= 0.5; // Bone detection throttle
  }
  
  // Phase 1: Mist (100 ms)
  digitalWrite(NEBULIZER_RELAY_PIN, HIGH);
  delay(100);
  digitalWrite(NEBULIZER_RELAY_PIN, LOW);
  delay(50);
  
  // Phase 2: Sonic activation (1000 ms)
  int piezo_pwm = (int)(255 * piezo_power_factor);
  analogWrite(PIEZO_DRIVER_PIN, piezo_pwm);
  delay(1000);
  
  // Phase 3: Vacuum (800 ms)
  analogWrite(PUMP_PWM_PIN, 200); // 80% of 255
  delay(800);
  
  // Phase 4: Rest & cool (1000 ms)
  analogWrite(PIEZO_DRIVER_PIN, 0);
  analogWrite(PUMP_PWM_PIN, 0);
  delay(1000);
}

float readThermistor() {
  int raw = analogRead(THERMISTOR_PIN);
  // Steinhart-Hart equation or simple lookup table to convert ADC to °C
  // (Depends on thermistor β-value and reference resistor)
  float voltage = raw * (5.0 / 1023.0);
  float temp_c = 25.0 + (voltage - 2.5) * 80.0; // Rough approximation
  return temp_c;
}

float readAccelerometer() {
  int x, y, z;
  accel.read(&x, &y, &z);
  float mag = sqrt(x*x + y*y + z*z) / 256.0; // Convert to g-force
  return mag;
}
```

### 3.2 Safety Firmware Layers

**Layer 1: Thermal Cutoff**  
- If thermistor reads > 42°C → cut all power immediately
- Log event to EEPROM, display warning on OLED

**Layer 2: Bone-Impact Detection**  
- Continuously monitor accelerometer for sudden impedance spikes (resonant frequency shift)
- If detected, reduce power by 50% for next cycle
- Prevents internal ear buzzing

**Layer 3: Battery Low Detection**  
- Monitor battery voltage via ADC on voltage divider
- If voltage < 6.5V → disable piezo driver, run pump only (allow user to finish cycle gently)

**Layer 4: Watchdog Timer**  
- Use hardware watchdog to auto-reset if firmware hangs (safety failsafe)

---

## Phase 4: Testing & Validation (Weeks 8–10)

### 4.1 Bench Testing (Week 8)

**Test 1: Acoustic Output Verification**
- Place smartphone or professional sound-level meter near shroud
- Record acoustic frequency with FFT analyzer (Android apps available)
- Verify output is 25–28 kHz and not in audible range (20 kHz cutoff)

**Test 2: Vacuum Flow Rate**
- Attach flowmeter to vacuum outlet hose
- Measure flow rate at pump outlet → should read 4–5 LPM

**Test 3: Thermal Response**
- Run device continuously for 10 minutes while monitoring thermistor reading
- Verify temperature stays below 40°C (or firmware throttles correctly)

**Test 4: Battery Endurance**
- Run full 3-second active cycle repeatedly
- Time how long until battery depletes (target: ~2.2 hours)

### 4.2 Skin Safety Testing (Weeks 9–10)

**Critical:** Get IRB approval or legal clearance before testing on human skin. For initial prototype, consider:

**Test 1: Forearm Patch Test (Self)**
- Apply device to forearm for 5 minutes
- Observe for redness, heat sensation, or discomfort
- Wait 24 hours → check for delayed irritation

**Test 2: Debris Capture Validation**
- Apply device to body area with dried sweat or makeup residue
- Inspect collected-debris filter pod after session
- Verify visible particulates are captured

**Test 3: Noise & Vibration Profile**
- Measure decibel level during operation at 30 cm distance
- Record any bone-conduction buzzing or vibration felt at collarbone/jaw

---

## Phase 5: Iteration & Design Refinement (Weeks 10–12)

### 5.1 Likely First-Pass Issues

**Issue 1: Acoustic Impedance Mismatch (Most Common)**
- **Symptom:** Device vibrates hard but skin doesn't seem "loosened"
- **Cause:** Dry piezo coupling (no fluid bridge)
- **Fix:** Increase micro-atomizer misting volume or use stickier fluid (add 5% glycerin to hydration fluid)

**Issue 2: Bone Conduction Buzzing**
- **Symptom:** User reports internal ear ringing when device touches chest
- **Cause:** Acoustic energy traveling through skeleton at 25 kHz
- **Fix:** Add silicone isolation mounts between piezo housing and handle; implement accelerometer-based power throttling

**Issue 3: Thermal Throttling Kicks in Too Early**
- **Symptom:** Device only runs 30 seconds before cutting to 50% power
- **Cause:** Thermistor placement too close to heat source or inadequate heat dissipation
- **Fix:** Relocate thermistor away from transducer; add small heatsink fin to transducer substrate

**Issue 4: Vacuum Pump Cavitation (Loud Noise, Reduced Flow)**
- **Symptom:** Pump is extremely loud and flows drop to 2–3 LPM
- **Cause:** Air entering pump inlet (shroud seal not airtight)
- **Fix:** Inspect all silicone shroud joints; re-cast shroud if gaps detected; consider adding check valve to pump inlet

### 5.2 Iteration Path

1. **Week 10:** Solve Issue 1 (acoustic coupling) → most critical for basic function
2. **Week 11:** Solve Issue 2 (bone conduction) → user comfort
3. **Week 12:** Solve Issues 3 & 4 (thermal & pump) → reliability

---

## Bill of Materials Summary

| Component | Quantity | Unit Cost | Total | Supplier |
|-----------|----------|-----------|-------|----------|
| Piezo transducer + driver board | 1 | $60 | $60 | AliExpress |
| BLDC vacuum pump | 1 | $85 | $85 | Alibaba |
| 2S battery pack (5000 mAh) | 1 | $50 | $50 | Amazon |
| USB-C charger + buck converter | 1 | $20 | $20 | Amazon |
| Arduino/STM32 microcontroller | 1 | $25 | $25 | AliExpress |
| NTC thermistor | 1 | $3 | $3 | Amazon |
| ADXL345 accelerometer breakout | 1 | $5 | $5 | AliExpress |
| Piezo nebulizer cartridge | 1 | $10 | $10 | Amazon |
| Fluid (D5 siloxane/isoparaffin) | 1 | $12 | $12 | Alibaba |
| LSR casting kit + mold | 1 | $60 | $60 | Shapeways + Amazon |
| 3D-printed housing (SLS nylon) | 1 | $100 | $100 | Shapeways |
| Connectors, switches, standoffs, misc. | — | $20 | $20 | Amazon |
| **Total** | | | **$450** | |

---

## Go-to-Market Roadmap (Post-Prototype)

1. **Validate PMF (Product-Market Fit)** with overlanding/van-life community
   - Post beta units to 5–10 influencers in this space
   - Collect feedback on debris capture, skin feel, thermal comfort

2. **Refine Based on Feedback** (2–3 weeks)
   - Adjust misting fluid formula if acoustic coupling insufficient
   - Tweak thermal thresholds if users report uncomfortable heat

3. **Scale Manufacturing**
   - Lock in exclusive supply agreements with piezo transducer manufacturers
   - Move from SLS 3D printing to injection-molded housing (at 5,000 units)

4. **Launch MVP (Minimum Viable Product) to Beachhead Vertical**
   - Target overlanders first (smallest market, highest pain)
   - Price at $179 (gross margin ~65%)
   - Sell consumables (filter pods + hydration fluid) at $15–$20/month

---

## Resources & Learning Path

- **Ultrasonic transducer fundamentals:** "Physics of Ultrasound" by K.K. Shung (textbook)
- **BLDC pump datasheet databases:** McMaster-Carr, Grainger (search "micro-pump" filters)
- **Arduino thermal control:** Arduino tutorials on PWM, ADC reading, thermistor linearization
- **LSR mold casting:** YouTube searches "liquid silicone rubber casting" or Smooth-On tutorials
- **CAD for 3D printing:** Fusion 360 (free for personal use) + Shapeways or Protolabs guides

---

## Next Steps

1. **This Week:** Order piezo transducer, pump, battery, and microcontroller (parallel)
2. **Next Week:** Receive components, begin shroud casting
3. **Week 3:** Mechanical assembly begins; firmware skeleton written
4. **Week 5:** Full prototype running; safety testing begins

This plan is iterative. Expect to redesign the shroud geometry and fluid formula at least once as you learn how acoustic coupling behaves in practice.

Good luck!
