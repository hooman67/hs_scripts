# gen6_conv_v1

Agent guidance for adding a new specialist to the existing Gen6 conversational stack.

This is the right entrypoint when the task is effectively:
- deploy a fine-tuned Gen6 DiT checkpoint
- wire it into the existing `gen6_conv_v1` pipeline
- optionally expose it through a public adapter layer similar to the Filix3 pano/IBL wrappers

## Scope

Use this guide when you are integrating a new specialist into the existing Gen6 stack. The work usually spans:
- checkpoint export
- DiT worker registration
- pipeline worker dependency/routing updates
- optional public API wrapper changes

If you are only changing tensor math or inference internals inside the worker, work in:
- `models/colligo/models/firefly/diffusion/gen6_conv`

If you are only changing a product-facing wrapper, work in that wrapper package and keep the shared pipeline contract unchanged if possible.

## End-To-End Flow

The normal specialist integration path is:
1. Export the training checkpoint into a flat `.pth` state dict for deployment.
2. Add a new DiT worker name in `diffusion/gen6_conv/types/__init__.py`.
3. Add the checkpoint artifact and `build_diffusion_transformer(...)` entry in `diffusion/gen6_conv/build.py`.
4. Surface the worker choice through the shared pipeline in:
   - `pipelines/gen6_conv_v1/types/__init__.py`
   - `pipelines/gen6_conv_v1/build.py`
   - `pipelines/gen6_conv_v1/Gen6ConvPipeline.py`
5. If the specialist needs a product-facing API, add or update a public adapter layer that constructs a `Gen6ConvRequest`.
6. Add tests at the layer you changed:
   - worker/build tests if you changed worker wiring
   - pipeline tests if you changed routing or asset handling
   - wrapper/compare/PITA tests if you changed a public endpoint

## Step 1: Export The Checkpoint

Use:
- `models/colligo/models/firefly/diffusion/gen6_conv/dit_gr6_export.py`

That helper exists to turn a distributed FE checkpoint into the flat `.pth` artifact the deployed worker expects.

Typical usage:

```bash
python models/colligo/models/firefly/diffusion/gen6_conv/dit_gr6_export.py \
  --ckpt-path "s3://.../ckpt_step00530000/" \
  --output /mnt/localssd/ibl_specialist_step530000.pth
```

For EMA:

```bash
python models/colligo/models/firefly/diffusion/gen6_conv/dit_gr6_export.py \
  --ckpt-path "s3://.../ckpt_step00530000/" \
  --output /mnt/localssd/ibl_specialist_ema_step530000.pth \
  --use-ema
```

After export, upload the artifact with the normal artifact flow and record:
- bucket/key
- version id
- sha256

## Step 2: Add The Worker

Update:
- `models/colligo/models/firefly/diffusion/gen6_conv/types/__init__.py`
- `models/colligo/models/firefly/diffusion/gen6_conv/build.py`

Pattern:
- add a new `Gen6ConvDiTWorker` enum value
- add a new `build.s3_source(...)` artifact constant
- add a new `build_diffusion_transformer(...)` call

Use an existing specialist as the template:
- `GEN6_CONV_DIT_PANO_SPECIALIST`
- `GEN6_CONV_DIT_IBL_SPECIALIST`

Reuse the existing worker class unless the runtime behavior truly differs:
- `colligo.models.firefly.diffusion.gen6_conv.DiffusionTransformerModel.DiffusionTransformerModel`

In most cases, a new fine-tuned specialist only needs:
- a new worker enum
- a checkpoint artifact
- the right training config YAML

## Step 3: Route The Shared Pipeline

Update:
- `models/colligo/models/firefly/pipelines/gen6_conv_v1/types/__init__.py`
- `models/colligo/models/firefly/pipelines/gen6_conv_v1/build.py`
- `models/colligo/models/firefly/pipelines/gen6_conv_v1/Gen6ConvPipeline.py`

What to change:
- add the new public routing enum in `Gen6ConvDiffusionModelName`
- add the worker to `GEN6_CONV_WORKERS`
- update any routing helpers that choose VAE/Qwen/DiT behavior by specialist

Use the existing pano and IBL paths as examples.

Important:
- if the new specialist only swaps DiT weights, keep the request/response schema unchanged
- if it needs different conditioning assets, VAE selection, output formatting, or equirect/HDR behavior, document and test those differences explicitly

## Step 4: Add A Public Adapter Only If Needed

If the specialist needs a product-specific public API, create or update a wrapper package like:
- `models/colligo/models/filix3/pipelines/gen6_pano_generation`
- `models/colligo/models/filix3/pipelines/gen6_ibl_generation`

The adapter layer should:
- build `ConversationalGenerateRequest`
- choose the correct `Gen6ConvDiffusionModelName`
- keep the shared `gen6_conv_v1` contract stable

Prefer putting product-specific prompt construction and response formatting in the wrapper, not in the shared pipeline.

## When You Need More Than A DiT Worker

You may also need:
- a different Qwen worker, if the specialist needs different text encoder config or system prompt handling
- a different VAE worker, if the specialist uses a different image/video codec profile
- wrapper-specific compare/PITA coverage, if the specialist is exposed publicly

Do not add new workers casually. If only the checkpoint changes, reuse the existing worker code path.

## Testing Checklist

Minimum checks for a new specialist:
- worker `build.py` imports cleanly
- pipeline routes to the new worker enum
- at least one focused pipeline test covers the new routing path
- if there is a public wrapper, adapter tests cover request construction and response mapping

Also verify:
- `colligo.yaml` visibility if compare packages or public wrappers depend on newly-added private packages
- binary-check safety if compare scaffolding previously used checked-in fixtures

## Good Example

The Filix3 Gen6 pano/IBL work is a good reference for the full stack:
- public wrapper constructs `Gen6ConvRequest`
- shared pipeline handles the multimodal orchestration
- diffusion worker selects the fine-tuned checkpoint and training config

When in doubt, copy an existing specialist path end to end and change the smallest possible surface.
