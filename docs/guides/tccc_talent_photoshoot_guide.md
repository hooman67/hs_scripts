# Talent Reference Photoshoot Guide — AI-Powered Ad Generation

**Prepared by:** Adobe Foundry Team  
**For:** The Coca-Cola Company  
**Purpose:** Guidelines for capturing talent reference photography to train and optimize our Instruct-Edit models for ad generation.

---

## Overview

The quality, consistency, and diversity of the reference photography you provide for each talent directly determines how well our model can generate that talent in new scenes, poses, wardrobe, and expressions. This guide is designed to help your photography teams capture images that maximize model performance and minimize artifacts.

**Core principle:** The model can only learn what it sees. If a variation is absent from the training data, the model cannot reliably produce it.

---

## 1. Technical Image Requirements

### Camera & Settings
- **Resolution:** Minimum 4K (4096×2732) or higher. Deliver the highest resolution available.
- **Format:** Lossless or near-lossless — RAW (preferred) + high-quality JPEG/TIFF exports. Avoid heavy JPEG compression.
- **Focal length:** Use a consistent focal length per shot type. Recommended: 85mm–135mm for portraits (minimizes facial distortion), 50mm for full-body. Avoid wide-angle lenses (<35mm) as they distort body proportions.
- **Shutter speed:** Fast enough to eliminate any motion blur (minimum 1/200s).
- **Aperture:** f/5.6–f/8 for full-body (deep enough depth of field to keep the entire body sharp). f/4–f/5.6 for headshots.
- **ISO:** Keep as low as possible to minimize noise.

### Color Calibration & Skin Tone Accuracy
- Include a **color checker card** (e.g., X-Rite ColorChecker) in at least one frame per lighting setup. This allows us to normalize color across sessions.
- Maintain **consistent white balance** across all images within a session. Do not use auto white balance.
- **Exposure bracketing:** For each lighting setup, capture **3-stop brackets** (–1 EV, 0 EV, +1 EV) of at least one reference frame. This gives us data on how the talent's skin tone behaves in highlight roll-off and shadow regions, which is critical for tonal accuracy in generation.
- **Controlled under/overexposed test frames:** Capture 2–3 intentionally underexposed (–1.5 to –2 EV) and overexposed (+1.5 to +2 EV) frames per talent per lighting setup. These teach the model how skin highlights and shadows render across the tonal range, and are especially important for ensuring fairness and accuracy across diverse skin tones.
- These calibration frames do not need the full pose/wardrobe matrix — a single neutral pose per lighting setup is sufficient.

### Image Sharpness
- Every delivered image must be critically sharp on the subject. Reject any images with motion blur, missed focus, or camera shake.
- Use a tripod for full-body and detail shots where possible.

---

## 2. Background & Environment

- **Use a clean, solid-color backdrop** — neutral gray (18% gray) or white seamless paper/cyclorama.
- Avoid patterned, textured, or busy backgrounds. They introduce noise during training and make segmentation harder.
- If environmental/contextual shots are needed, capture them as a **separate set** from the core reference images.
- Ensure no shadows from the talent fall across the background in a distracting way; use sufficient backdrop distance and background lighting.

---

## 3. Lighting Variations

Lighting diversity is critical. For **each talent**, capture the full set of poses/wardrobe under multiple lighting conditions:

| Lighting Setup | Description |
|---|---|
| **Flat / Beauty** | Soft, even front light. Minimal shadows. Standard beauty/ad lighting. |
| **Rembrandt** | Classic 45° key light creating a triangle of light on the shadow-side cheek. |
| **Side / Split** | Hard side light, half the face lit, half in shadow. |
| **Backlit / Rim** | Strong backlight creating a rim/halo, with fill on the face. |
| **High Key** | Bright, low-contrast, minimal shadows. Common in beverage/lifestyle advertising. |
| **Low Key / Dramatic** | Dark, high-contrast, moody. Single hard light source. |
| **Natural / Outdoor Simulated** | Soft directional light simulating golden-hour or overcast daylight. |

**Minimum: 5 distinct lighting setups per talent.**

For each lighting setup, also vary:
- **Light temperature** — capture a warm variant (3200K–4000K) and a cool/neutral variant (5500K–6500K).
- **Light hardness** — at least some setups with hard light (bare source) and some with soft light (diffused/bounced).

---

## 4. Shot Types & Framing

Capture every talent at multiple framings. Each is essential:

### 4.1 Headshot / Close-Up (Head & Shoulders)
- Framed from mid-chest up.
- Used for facial feature learning, skin texture, and expression.

### 4.2 Medium Shot (Waist Up)
- Framed from waist up.
- Critical for wardrobe and upper-body pose learning.

### 4.3 Full Body
- Head to toe, with some space above and below.
- **This is mandatory for every talent.** Our model has produced artifacts (e.g., gender-mismatched body proportions after face swap) when full-body reference images were missing. The model needs to learn the complete body structure of each talent.
- Include both relaxed standing and active poses.

### 4.4 Hand & Finger Detail Shots
- **Dedicated close-up shots of hands are required.**
- Hands holding products (bottle, can, glass).
- Hands in various natural positions: open palm, relaxed, gesturing, gripping.
- Both left and right hands.
- Hands interacting with each other (clasped, one over the other).
- **Minimum 15–20 hand-specific images per talent.** Hand generation is one of the hardest problems in image synthesis — more data directly improves quality.

### 4.5 Three-Quarter and Profile Views
- Capture the face and body at: **front-facing, 3/4 left, 3/4 right, profile left, profile right, and slight upward/downward angles.**
- These are essential for the model to learn 3D facial structure and generate accurate likenesses from any angle.

### 4.6 Back and Rear Three-Quarter
- At least a few images from behind and rear-3/4 angles to capture hair, back of head, ear shape, and overall silhouette.

### 4.7 Extreme Crops (Feature-Specific Close-Ups)

In addition to standard framings, capture **tightly cropped, high-resolution detail shots** of individual features. These give the model fine-grained data for high-fidelity generation and improve layout flexibility when generating partial-body compositions (e.g., cropped ad layouts that only show a face or torso).

| Crop | Framing Notes |
|---|---|
| **Eyes only** | Tight crop from eyebrows to upper cheekbones. Both eyes in frame. Capture with multiple gaze directions. |
| **Mouth only** | Tight crop from nose tip to chin. Capture across expressions (closed, smiling, speaking, drinking). |
| **Tight face** | Forehead to chin, ear to ear. Tighter than a standard headshot — fills the frame with the face. |
| **Mid-torso** | Chest to waist, cropping out head and legs. Shows wardrobe fit and body proportion at center mass. |
| **Hands only** | (Covered in Section 4.4 — ensure extreme close-ups of individual fingers and knuckles are included.) |
| **Feet / footwear** | Ankle to toe. Relevant for full-body generation accuracy. |

Capture extreme crops under the **primary lighting setup** and in at least **2 wardrobe options**. Minimum **10–15 extreme-crop images per talent**.

---

## 5. Wardrobe Guidelines

### 5.1 Types of Clothing to Include

The model needs a range of garment fits and types to generate talent convincingly in any outfit:

| Category | Examples | Why It Matters |
|---|---|---|
| **Fitted / Tailored** | Slim-fit shirt, blazer, bodycon dress, fitted tee | Reveals body contour; if missing, the model cannot generate fitted garments accurately |
| **Relaxed / Casual** | Loose tee, hoodie, open button-down, relaxed jeans | Common in lifestyle ads |
| **Formal / Structured** | Suit jacket, dress shirt, structured dress | Different fabric draping and silhouette |
| **Athletic / Active** | Tank top, sports bra, joggers, compression wear | Reveals arms, shoulders, physique |
| **Sleeveless / Bare Arms** | Tank top, sleeveless blouse, strappy top | Exposes full arm and shoulder shape |
| **Short Sleeve vs Long Sleeve** | Include both for tops | Different coverage levels |
| **Shorts / Skirts / Cropped Pants** | At least one lower-body option showing legs | Leg and knee structure |

### 5.2 Wardrobe Rules

- **Solid colors only** for the core reference set. Avoid large logos, bold patterns, or text on clothing — these can transfer as artifacts.
- Choose **muted, neutral tones** (black, white, gray, navy, olive, beige) so clothing color does not dominate the training signal.
- **Include at least one outfit that reveals body shape** (e.g., fitted athletic wear) so the model learns the talent's actual proportions.
- Avoid clothing that obscures the neck, jawline, or hands (e.g., turtlenecks, oversized sleeves) in the majority of shots. A few are fine for variety, but most should leave these areas visible.
- **Footwear matters for full-body shots.** Include casual shoes, dress shoes, and bare feet or minimal sandals.

### 5.3 Isolating the Wardrobe Variable

To help the model learn wardrobe independently:

- **Same pose + same lighting + different wardrobe:** Capture a controlled set where the talent holds an identical pose and expression across 5+ outfit changes. Only the clothing changes between shots. This teaches the model to disentangle clothing from identity and pose.

---

## 6. Pose Guidelines

### 6.1 Required Poses

| Pose Type | Notes |
|---|---|
| **Neutral standing (A-pose)** | Arms slightly away from body, relaxed hands, feet shoulder-width apart. This is the single most important pose — capture it in every outfit. |
| **Relaxed standing** | Natural weight shift, one hand in pocket or at side |
| **Walking / mid-stride** | Dynamic but natural |
| **Seated** | On stool, chair, edge of table — casual and formal |
| **Leaning** | Against wall or surface — common in lifestyle ads |
| **Arms crossed** | Shows forearm/hand overlap |
| **Holding a product** | Bottle, can, glass at various heights and angles |
| **Action / celebratory** | Arms raised, jumping, toasting — high-energy lifestyle poses |

### 6.2 Body Proportion & Posture Diversity

Beyond major pose changes, capture **subtle intra-pose posture shifts** for each talent. These micro-variations teach the model how the talent's body naturally balances and distributes weight, which prevents stiff, mannequin-like outputs.

| Posture Shift | What It Teaches the Model |
|---|---|
| **Weight on left leg vs. right leg** | Natural hip tilt, asymmetric stance |
| **Arms akimbo (hands on hips)** | Elbow angle, torso width variation |
| **Arms crossed (high vs. low)** | Forearm overlap, chest compression |
| **Cross-legged sitting** | Leg overlap, knee positioning |
| **Leaning forward vs. back** | Center-of-gravity shifts, torso foreshortening |
| **One foot elevated (on step/ledge)** | Asymmetric leg angles |
| **Slouched vs. upright posture** | Shoulder line, spine curvature |

Capture at least **5–8 posture shifts per major pose** (e.g., multiple standing weight distributions, multiple seated lean angles). This dramatically improves the model's ability to generate natural, balanced body positions rather than rigid default stances.

### 6.3 Isolating the Pose Variable

- **Same wardrobe + same lighting + different poses:** Capture a controlled set where the talent wears the same outfit and cycles through 10+ poses. This teaches the model to separate pose from clothing and identity.

---

## 7. Facial Expressions

The model has shown difficulty generating authentic emotional expressions when they are underrepresented in training. Capture a dedicated expression series:

| Expression | Notes |
|---|---|
| **Neutral** | Relaxed, no smile |
| **Subtle smile** | Closed-mouth, soft |
| **Open smile / Laughing** | Teeth showing, genuine joy |
| **Excited / Energetic** | Wide eyes, big smile, dynamic |
| **Surprised** | Raised eyebrows, open mouth |
| **Contemplative / Serious** | Thoughtful, soft gaze |
| **Talking / Mid-speech** | Mouth partially open, natural conversational look |
| **Sipping / Drinking** | Actively drinking from product — critical for beverage ads |

Capture each expression at **both headshot and medium-shot framing**. Combine with at least 2 gaze directions (see below).

---

## 8. Gaze Direction

Gaze direction heavily influences the feel of a generated ad. Capture:

- **Direct to camera** (engaging the viewer)
- **Looking left / right** (~30° and ~60° off-camera)
- **Looking up / down** (aspirational gaze up, looking at product down)
- **Looking at a product in hand**
- **Looking at another person** (for multi-talent compositions)
- **Eyes closed** (for candid/laughing moments)

Combine gaze with multiple expressions. Minimum: **3 gaze directions × each key expression**.

---

## 9. Hair & Grooming

- Capture hair in its **natural/default state** for the majority of shots.
- If the talent has longer hair, also capture:
  - **Hair up** (tied back, ponytail, bun) — exposes neck, jawline, ears.
  - **Hair down** — shows natural fall and volume.
  - **Hair over one shoulder vs. both** — asymmetry matters.
- For facial hair (beards, stubble): keep consistent within a session. If the talent could appear both clean-shaven and bearded, those should be treated as **separate capture sessions**.
- Avoid dramatic makeup changes between shots in the core set. Keep makeup natural and consistent. If a different look is needed (e.g., glam for a formal ad), capture it as a distinct subset.

---

## 10. Accessories & Props

- **Minimal accessories in the core reference set.** Remove watches, bracelets, rings, earrings, and glasses for the base captures so the model learns the unobstructed face and body.
- Capture a **separate accessory subset** with:
  - Sunglasses (on and pushed up on head)
  - Regular glasses
  - Watch / jewelry
  - Hat / cap (various styles)
> **⚠️ CRITICAL — Product Interaction Shots**
>
> Talent holding, drinking from, or interacting with Coca-Cola products in multiple hand positions and angles. **These are among the most important images for the end use case.** Capture across multiple wardrobe options, poses, and lighting setups. Include close-ups of hands on the product, mid-drink moments, and natural holding positions (at side, raised to mouth, extended toward camera, toasting). This is not optional — insufficient product interaction data directly degrades the quality of generated ads.

---

## 11. Skin & Body Considerations

- Capture enough exposed-skin images (arms, hands, neck) for the model to learn the talent's **skin tone accurately** under different lighting.
- Include images where the talent's **arms are separated from their torso** (not pressed against sides) — this prevents limb-merging artifacts.
- If a talent has distinctive features (tattoos, moles, scars), document them in the metadata. These features will be reproduced by the model; if they should be removed, note that separately.
- **Highlight & shadow rendering across skin tones:** Ensure the exposure bracketing and calibration frames described in Section 1 are captured for every talent. The model must learn how highlights roll off on each talent's skin (specular vs. diffuse reflection differs significantly across skin tones). Without this data, the model may produce washed-out highlights on darker skin or muddy shadows on lighter skin.
- **Consistent skin exposure:** For the core reference set, expose for the talent's skin (not the background). Use spot metering on the face/chest to ensure skin is in the optimal exposure zone across all images.

---

## 12. Motion & Micro-Variation Sequences

Static, perfectly posed images alone can produce "mannequin-like" outputs that lack the subtle imperfections of real humans. To counter this, capture **short burst sequences of subtle, continuous movement** between poses and expressions.

### 12.1 What to Capture

Use continuous burst shooting (8–12 fps) or short video clips to record:

| Sequence | Duration / Frames | What It Teaches |
|---|---|---|
| **Head tilt progression** | Left → center → right (~2 sec burst) | Natural head angle transitions, neck muscle movement |
| **Blink progression** | Eyes open → half-closed → closed → open (~1 sec burst) | Realistic eyelid positions between open and closed |
| **Expression transitions** | Neutral → subtle smile → open smile → laugh (~3 sec burst) | Smooth interpolation between emotions; prevents "jump" artifacts |
| **Hand-to-product motion** | Hand at rest → reaching → gripping bottle → raising to mouth (~3 sec burst) | Natural hand articulation, wrist angle progression |
| **Weight shift** | Standing still → shifting weight left → right (~2 sec burst) | Hip sway, shoulder counterbalance |
| **Breathing / micro-posture** | 5-second still pose, captured in burst | Subtle chest/shoulder rise, natural micro-fidgets |
| **Hair movement** | Head turn causing natural hair sway (~2 sec burst) | Realistic hair dynamics |

### 12.2 Technical Settings for Burst Sequences

- **Burst mode at maximum fps** (8+ fps). Use electronic shutter if available to achieve higher frame rates.
- Maintain the same shutter speed, aperture, and lighting as the core reference set — these frames must be exposure-matched to the rest.
- Burst sequences are supplementary; they do not replace the core posed reference images.
- Minimum **5 burst sequences per talent** covering at least: expression transition, head tilt, blink, and hand motion.

---

## 13. Video Capture

In addition to still photography, **capture continuous video of each talent during the photoshoot and deliver it alongside the still images.**

### 13.1 Why Video Matters

Video provides a dense, continuous representation of the talent in motion — hundreds of unique frames per minute showing natural transitions between poses, expressions, and movements that even extensive burst photography cannot match. This data is valuable for:

- Training temporal consistency and natural motion priors
- Extracting additional high-quality frames for pose/expression combinations that may have been missed in stills
- Learning realistic micro-expressions and subtle body language

### 13.2 Video Requirements

| Parameter | Specification |
|---|---|
| **Resolution** | 4K minimum (3840×2160), higher preferred |
| **Frame rate** | 24 fps minimum; 60 fps preferred for slow-motion extraction |
| **Codec** | ProRes 422 HQ, ProRes 4444, or RAW video. Avoid H.264/H.265 for delivery (lossy compression destroys fine detail). |
| **Lighting** | Same controlled lighting setups used for stills. Avoid flickering lights (use DC-powered continuous lighting, not strobes). |
| **Background** | Same clean backdrop as stills. |
| **Duration** | 2–5 minutes per talent per lighting setup, covering a natural flow through poses, expressions, and movements. |

### 13.3 What to Record

For each talent, capture video of:

- **Pose walk-through:** Talent naturally cycles through standing, seated, leaning, and active poses.
- **Expression reel:** Talent runs through full range of expressions at headshot framing (neutral → smile → laugh → surprise → serious → talking).
- **Product interaction:** Talent picks up, holds, drinks from, and sets down the product in a natural sequence.
- **Free movement:** 30–60 seconds of the talent moving naturally — walking, turning, adjusting clothing, reacting to direction — to capture candid micro-movements.

### 13.4 Delivery

- Deliver video files alongside the still image set.
- Name files using the same talent ID convention: `{TalentID}_video_{LightingSetup}_{Description}_{Seq}.{ext}`
- If possible, also provide **timecode-synced frame exports** at key moments (peak expressions, best poses) as still TIFF/JPEG files.

---

## 14. Multi-Talent / Interaction Shots

If ads will feature multiple talents together:

- Capture each talent **individually first** following all the above guidelines.
- Then capture **paired/group interaction shots** — talking, toasting, laughing together.
- Vary who is in the foreground vs background, and the spatial relationship between talents.

---

## 15. Minimum Volume Per Talent

| Shot Category | Minimum Images |
|---|---|
| Headshot / close-up (expressions × gaze × lighting) | 10 |
| Medium shot (wardrobe × pose × lighting) | 10 |
| Full body (wardrobe × pose × lighting) | 10 |
| Hand detail | 5 |
| Extreme crops (eyes, mouth, face, torso, feet) | 5 |
| Angle variations (3/4, profile, back) | 5 |
| Accessory / product interaction | 10 |
| Burst / micro-variation sequences (extracted frames) | 5 |
| Exposure bracketing & calibration frames | 5 |
| **Total minimum per talent (stills)** | **~65** |

| Video Category | Minimum |
|---|---|
| Pose walk-through video | 1 clip per lighting setup |
| Expression reel video | 1 clip per lighting setup |
| Product interaction video | 1 clip |
| Free movement video | 1 clip |
| **Total minimum per talent (video)** | **~5–10 minutes across setups** |

More is always better. The target sweet spot is **60–70 images + 5–10 minutes of video per talent** for high-fidelity model performance.

---

## 16. File Naming & Metadata

Use a consistent naming convention so images can be programmatically sorted:

```
{TalentID}_{ShotType}_{Wardrobe}_{Pose}_{Expression}_{Lighting}_{Gaze}_{Seq}.{ext}
```

Example:
```
T01_fullbody_fitted-tee_standing-neutral_smile_rembrandt_camera_001.CR3
T01_handdetail_na_holding-bottle_na_beauty_product_003.CR3
```

Include a **metadata spreadsheet** per talent session with columns:
- Filename
- Talent ID / Name
- Shot type
- Wardrobe description
- Pose description
- Expression
- Lighting setup
- Gaze direction
- Any notes (accessories, hair state, etc.)

---

## 17. Common Pitfalls to Avoid

| Pitfall | Why It's a Problem |
|---|---|
| Only capturing bust/headshots | Body generation fails; gender/proportion mismatches occur |
| Ignoring hands | Hands are the #1 artifact in generated images |
| Only one lighting setup | Model overfits to that lighting; generated images look flat |
| Busy/patterned clothing | Patterns bleed into generated images as artifacts |
| Auto white balance | Color shifts between images confuse the model |
| All poses in one outfit | Model cannot disentangle pose from clothing |
| All outfits in one pose | Model cannot learn diverse poses |
| No neutral expression | Model defaults to an awkward "average" expression |
| Low image count (<100) | Insufficient data for reliable generation |
| Motion blur or soft focus | Teaches the model to generate blurry output |
| Heavy post-processing (skin smoothing, compositing) | Model learns the retouching artifacts, not the actual person |
| No exposure brackets / calibration frames | Model cannot learn accurate highlight/shadow rendering across skin tones |
| Only perfectly still, posed images | Outputs look static and mannequin-like; subtle human micro-movements are missing |
| No video provided | Misses dense temporal data for natural transitions between poses and expressions |
| No extreme crops | Model struggles with tight-crop ad layouts; fine facial/body details are under-learned |
| Identical posture in every standing shot | Model generates rigid, unnatural body balance; lacks weight-shift realism |

---

## 18. Deliverables Checklist

- [ ] RAW files + high-quality JPEG/TIFF exports for all images
- [ ] Color checker reference frame for each lighting setup
- [ ] Exposure bracketing & calibration frames (under/overexposed) per talent per lighting setup
- [ ] Metadata spreadsheet per talent
- [ ] Minimum 370 images per talent (target 500–700)
- [ ] Controlled sets: same-pose-different-wardrobe AND same-wardrobe-different-pose
- [ ] Full expression series per talent
- [ ] Full gaze direction series per talent
- [ ] Dedicated hand detail shots (minimum 20 per talent)
- [ ] Extreme crop / feature-specific close-ups (minimum 15 per talent)
- [ ] Full body shots in every wardrobe option
- [ ] Posture diversity within poses (weight shifts, lean variations)
- [ ] At least 5 distinct lighting setups
- [ ] Clean/neutral backgrounds for all core reference images
- [ ] Product interaction shots
- [ ] Burst / micro-variation sequences (expression transitions, head tilts, blinks, hand motion)
- [ ] Video capture: 4K, ProRes or RAW, 5–10 min per talent covering poses, expressions, product interaction, and free movement

---

## Appendix: Quick-Reference Shot List (Print for On-Set Use)

**For each talent, cycle through:**

1. **Calibration frames** → Color checker card + exposure brackets (–1, 0, +1 EV) + under/overexposed test frames → each lighting setup
2. **Outfit 1 (fitted)** → Neutral standing (A-pose) → 5 lighting setups → 8 expressions × 3 gaze directions → full body + medium + headshot
3. **Outfit 1 (fitted)** → Pose set (10 poses) + posture shifts (weight, lean, arm variations) → primary lighting → full body + medium
4. **Outfit 2 (casual)** → Repeat #2 and #3
5. **Outfit 3 (formal)** → Repeat #2 and #3
6. **Outfit 4 (athletic)** → Repeat #2 and #3
7. **Outfit 5 (sleeveless)** → Repeat #2 and #3
8. **Hand detail set** → All outfits, product interactions, 3 lighting setups
9. **Extreme crop set** → Tight face, eyes-only, mouth-only, mid-torso, feet — primary outfit, 2 lighting setups
10. **Angle rotation set** → Front, 3/4 L, 3/4 R, profile L, profile R, back — primary outfit, primary lighting
11. **Hair variation set** (if applicable) → Up vs. down, primary outfit
12. **Accessory set** → Glasses, sunglasses, hat, jewelry — primary outfit, primary lighting
13. **Product interaction set** → Holding, drinking, toasting — multiple outfits and poses
14. **Burst / micro-variation sequences** → Expression transitions (neutral → smile → laugh), head tilts, blink progressions, hand-to-product motion — primary outfit, primary lighting
15. **Video capture** → Pose walk-through, expression reel, product interaction, free movement — each lighting setup, 2–5 min per clip
