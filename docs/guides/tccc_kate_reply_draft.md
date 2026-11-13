# Draft Reply to Kate — Photoshoot Guide Follow-Up

---

Hi Kate,

Thank you for the quick turnaround on this, and for the candid feedback — it's really helpful. We absolutely want to work with you to simplify where we can while protecting the things that will make the biggest difference in output quality. Let me walk through each item.

---

## 1. Product Interaction Shots (Beverage In-Hand / Drinking)

**This one is non-negotiable for us, but we can save you significant cost on it.**

Here's the technical reason: the core use case for this model is generating ads where talent is interacting with Coca-Cola products — holding a bottle, raising it to their lips, toasting, etc. The way our Instruct-Edit model works is that it learns *from examples*. If we don't have real reference images of each talent's hands wrapped around a bottle, fingers gripping a can, or a product raised to their mouth, the model has to *guess* what that looks like — and hands are already the single hardest thing for any image generation model to get right. This data helps us avoid these artifacts: wrong finger counts, unnatural grip angles, bottles floating in air, and awkward mouth-to-product contact.

**The compromise:** These shots do **not** need to be styled or production-ready. We don't need hero lighting, wardrobe changes, or art-directed compositions for these. Simple, raw captures on a clean backdrop — talent in a basic fitted outfit, holding / drinking / interacting with the product in varied hand positions — is exactly what we need. Think of it as data capture, not a styled shoot. This should significantly reduce the cost compared to treating them as polished production shots. What we care about is:

- Multiple hand positions on the product (one-handed, two-handed, different grip heights)
- Product raised to mouth / mid-sip / lowering from mouth
- Both left and right hand holding
- Close-ups of hand-on-product contact

A simple, efficient setup for these (one lighting, one outfit, clean background, 15–20 minutes per talent) should cover it without a major budget impact.

---

## 2. Lighting — Why 5 Setups?

**You're right — if Coca-Cola's brand lighting direction is specific and consistent, we can reduce this.**

The reason we recommended 5 setups in the guide is that lighting diversity prevents the model from "baking in" a single lighting look. If the model only ever sees a talent under one type of light, it can only generate them under that light — and any attempt to place them in a different scene (outdoor, dramatic, warm, etc.) will look off because the model doesn't know how shadows and highlights fall on that person's face and body under other conditions.

**The compromise:** If Coca-Cola's ad output will consistently use a defined lighting direction, we can train to that. Here's what we'd need:

1. **Document the exact lighting spec** — send us the setup details (key light position, fill ratio, color temperature, soft vs. hard, any rim/back light). A lighting diagram or reference frames from previous shoots would be ideal.
2. **Understand the trade-off:** The model will generate beautifully under *that* lighting, but will struggle if you later ask it to produce an ad with a different mood (e.g., golden-hour outdoor, dramatic low-key, high-contrast editorial). If the brief ever expands, we'd need to retrain with additional lighting data.
3. **Our recommendation for a middle ground:** Even within your brand lighting direction, capture a **slight variation** — for example, the standard Coca-Cola key setup *plus* one alternative (e.g., a softer or warmer variant). Two setups instead of five still gives the model enough to handle minor scene-to-scene variation without a major production overhead.

---

## 3. Wardrobe — Why More Than One Outfit?

**We do need more than a single outfit, but we can slim this down to a practical minimum.**

Here's the issue with a single wardrobe: when the model only sees a talent in one outfit, it begins to treat the clothing as part of the person's identity. The fabric drape, the neckline, the sleeve length, the way the garment sits on the shoulders — all of that gets "fused" with the talent. When you then ask the model to generate that talent in a different outfit (which is a core part of the use case — swapping wardrobe, placing talent in new scenes), it struggles to separate what the person looks like from what the clothes look like. You'll see ghosting of the original outfit, incorrect body proportions where the old garment shape bleeds through, or unnatural fabric behavior.

**The minimum we need is 2 outfits, and here's exactly what to pick:**

| Outfit | What to Choose | Why |
|---|---|---|
| **Outfit 1: Fitted** | A simple, solid-color fitted top (like a plain crew-neck tee or fitted long-sleeve) with fitted pants/jeans. Neutral color (black, white, gray, navy). | This is the most important outfit. It reveals the talent's actual body contours — shoulders, arms, torso, hips — so the model learns their real proportions. Without this, generating the talent in any fitted clothing will produce body-shape artifacts. |
| **Outfit 2: Relaxed / Lifestyle** | A casual, slightly looser top (e.g., an untucked button-down, a relaxed tee, a light jacket/hoodie worn open). Solid neutral color. | This teaches the model how fabric drapes and moves on this talent's body when it's not skin-tight. It's the contrast the model needs to disentangle body shape from clothing shape. |

That's it — two outfits. Solid colors, neutral tones, nothing with logos or patterns. The talent can wear simple jeans or chinos for both. This is very low wardrobe overhead but gives us the critical variation the model needs. If you can add a third outfit that exposes more skin (a tank top or sleeveless option), that would be a bonus for arm and shoulder accuracy, but we can work with two.

---

## 4. Hair — 2 Styles Is Fine

**Two hair styles works for us.** We'd suggest:

- **Style 1 (primary):** The talent's natural/default look — however they'd most likely appear in a Coca-Cola ad.
- **Style 2:** A variation that changes how much of the face, neck, and ears are visible. For longer hair, this means one "down" and one "up" (ponytail, bun, tied back). For shorter hair, a subtle variation (parted differently, swept back vs. natural) is enough.

**One additional ask on this topic: makeup.** We'd request the same approach — two looks:

- **Look 1 (primary):** Natural / minimal, which is what should be used for the majority of the shoot. This gives the model the cleanest read on the talent's actual features.
- **Look 2:** The "campaign-ready" or styled look that matches Coca-Cola's typical ad aesthetic. This can be used for a smaller subset of shots.

Keeping makeup consistent within each look is more important than the number of looks. Dramatic changes mid-session (without reshooting the full set) will confuse the model.

---

## On Simplifying the Document / Minimum Viable Input

We hear you on the document being a lot. With the compromises above, here's what a simplified, minimum-viable shoot looks like per talent:

| What | Simplified Requirement |
|---|---|
| **Lighting** | 1–2 setups (your brand lighting + one soft variant) |
| **Wardrobe** | 2 outfits (1 fitted, 1 relaxed) |
| **Hair** | 2 styles |
| **Makeup** | 2 looks (natural + campaign) |
| **Core shots** | Full body + medium + headshot, across key poses and expressions, in each outfit |
| **Product interaction** | Raw/unstyled, one lighting, one outfit, 15–20 min per talent |
| **Hands** | Dedicated hand close-ups with product |
| **Video** | If feasible, continuous video during the shoot (even BTS camera rolling is valuable) |

This is a meaningful reduction from the full guide while still covering the data the model needs to perform well. We're happy to jump on the call with your production team at --- tomorrow if it would help to walk through this together and answer any questions in real time.


