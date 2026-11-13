# HP natural-placement judge V4.2

V4.2 is an evidence-graph redesign. It records a visual inventory, answers fourteen positive-condition triggers, reconciles tested defect candidates, and projects retained candidates into the thirteen legacy placement checks. Application code derives scores, verdicts, and explanations.

Production runtime requires only generated scene image, original twin image, product type, and scene prompt. Record ID, device, camera, and prompt rank are optional audit metadata. Anchor selection always excludes exact generated hashes, the same twin hash, and the exact prompt hash; optional metadata adds stronger family exclusions.

The product/support crop is an unwarped deterministic attention aid. Failed or uncertain SIFT/affine localization falls back to the complete scene and does not reduce placement confidence.

The first evaluation is a frozen six-case development gate. Human comments and expected answers are stored separately and are never passed to the judge. Do not run the 15-case or 160-case sets until the gate has been reviewed.
