<!--
ADOBE CONFIDENTIAL
Copyright 2026 Adobe. All Rights Reserved.
-->

# Verifier test fixtures

These JSON files are **engine-test samples**, not per-endpoint fixtures. They are
sample C2PA manifests used to unit-test the verifier checks (`check_tc_001` …
`check_tc_005`) **offline** — no pod, no network, no `adobe_c2patool`.

They are named by the **manifest shape/state** they exercise, NOT by the endpoint
they came from, because the verifier engine is generic: a handful of shape samples
cover the checking logic for *every* endpoint. Onboarding a new model does **not**
require adding a fixture here — a new model is verified by a live run, where
`adobe_c2patool` reads the real output manifest on the fly.

| File | Read path | `validation_state` | Trust | `claim_version` | Tests it anchors |
|---|---|---|---|---|---|
| `manifest_claimv1_untrusted.json` | SDK `Reader().json()` | `Valid` | `signingCredential.untrusted` (stage cert) | `1` | ai_manifest/prompt_omitted/signature_valid baseline; signature_valid untrusted-by-default; claim_version v1-not-v2 finding |
| `manifest_claimv1_trusted.json` | `adobe_c2patool … verify` | `Trusted` | `signingCredential.trusted` | — | signature_valid `require_trusted` passes via the canonical tool path |

**Provenance:** both were captured from the **same** real lego_v1 T2I output against
dev (active_manifest `urn:uuid:8583be9a…`, 2026-05). The two files are that one
asset read through the two validator paths — that pairing is what proves
`Valid` ≠ `Trusted`.

**When to add a new fixture here:** only when the engine needs to cover a *new
manifest shape* it can't yet — e.g. the first **claim v2** manifest, the first
**video** manifest, or the first manifest **with ingredients**. Capture one real
example, drop the JSON here, and pin a test to it. That's an "engine learned a new
shape" event, not a "new model onboarded" event.

**Do not commit raw binaries here** (see `.gitignore`). Input *assets* live in LFS
under `data/test/cai_compliance/` and are referenced from YAML cases by path.

## The small signed reference (`c2pa_signed_ref.jpg`)

WAN's I2V path rejects reference images over **921,600 px** ("Reference image too
large… up to 1280x720"). The input-provenance (ingredient-linkage) case needs a *signed* reference (so
there is provenance to pass through) that is also under this cap.

**Firefly/foundry cannot supply one.** Every foundry image size in
`ASPECT_RATIO_TO_SIZES_FOUNDRY` (lego_v1 `v1_images_types.py`) is ≥1920×1088 ≈ 2.09M px
— 2.3×+ over WAN's cap — and a signed asset **cannot be downscaled** to fit: C2PA
hard-binds the manifest to the exact pixel bytes, so resizing invalidates the signature
and the asset stops being a usable ingredient. (This is itself a platform gap: a real
customer feeding a Firefly image to WAN would have to downscale and thereby strip its
Content Credentials — so signed-Firefly → WAN provenance passthrough is currently
unreachable in production. Worth a Jira note.)

So we vendor a **natively-small, genuinely-signed** C2PA sample instead:

- **Source:** `CA.jpg` from the public [`contentauth/c2pa-rs`](https://github.com/contentauth/c2pa-rs/blob/main/sdk/tests/fixtures/CA.jpg)
  test fixtures (Apache-2.0/MIT). Renamed to `c2pa_signed_ref.jpg` — it is *not* a
  Firefly output, so it must not be named like one.
- **Shape:** 1024×683 (699,392 px, under the cap). Carries a full manifest:
  `claim_generator = make_test_images / c2pa-rs`, a `c2pa.actions` chain
  (`c2pa.opened` + `c2pa.color_adjustments`), a nested `c2pa.ingredient`, and a
  `stds.schema-org.CreativeWork` author assertion — i.e. real provenance to preserve.
- **Trust:** signed with the "C2PA Test Signing Cert" (a *test* cert, not Adobe-trusted).
  Fine here: the ingredient-linkage assertion in `ai_manifest` checks the **output**
  preserves the ingredient's provenance, not that the ingredient itself was
  Adobe-signed (that's `signature_valid`, on the output signer).

To re-fetch / verify:

1. `curl -fsSL -o c2pa_signed_ref.jpg https://raw.githubusercontent.com/contentauth/c2pa-rs/main/sdk/tests/fixtures/CA.jpg`
2. Confirm it really carries a manifest (do **not** trust a screenshot/paste — those
   strip the APP11 segment): `adobe_c2patool c2pa_signed_ref.jpg` → expect a manifest
   (not "JumbfNotFound"). Note: Google/Gemini "signing" is **SynthID** (an invisible
   *pixel* watermark), which is **not** C2PA and won't satisfy this — the file needs an
   embedded C2PA manifest in metadata.
3. Place at `data/test/cai_compliance/c2pa_signed_ref.jpg`, then `./m lfs.sync …` to
   upload to S3 and regenerate `data/test/cai_compliance/.gitignore` (the binary
   manifest). Do **not** hand-edit that manifest.

Consumed by the `i2v_signed_ref` case in `workers/wan22/cai_validator/wan_v22*.yaml`.
