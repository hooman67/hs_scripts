# LoRA Adapters for Diffusion Image and Video Models

Last updated: 2026-10-04  
Scope: LoRA mathematics, training, inference, image-to-image, video, adapter composition, Stable
Diffusion, and FLUX.

## Contents

1. [Core idea](#core-idea)
2. [The mathematics](#the-mathematics)
3. [Where LoRA lives in an image model](#where-lora-lives-in-an-image-model)
4. [Training an image LoRA](#training-an-image-lora)
5. [Text-to-image inference](#text-to-image-inference)
6. [Image-to-image inference](#image-to-image-inference)
7. [Video LoRA](#video-lora)
8. [Combining multiple LoRAs](#combining-multiple-loras)
9. [Stable Diffusion example](#stable-diffusion-example)
10. [FLUX example](#flux-example)
11. [Important practical limitations](#important-practical-limitations)
12. [Primary references](#primary-references)

## Core idea

LoRA—Low-Rank Adaptation—is a compact learned patch applied to selected weight matrices in a
pretrained model.

For a frozen weight matrix `W`, full fine-tuning learns a complete update `delta_W`. LoRA instead
approximates that update using two much smaller matrices, `A` and `B`.

The base model remains frozen. Only the small LoRA matrices are trained and stored.

## The mathematics

For one model layer:

$$
W_{effective} = W + \lambda \frac{\alpha}{r}BA
$$

Plain-text equivalent:

```text
W_effective = W + lambda * (alpha / rank) * B * A
```

Where:

- `W` has shape `d_out × d_in` and is frozen.
- `A` has shape `rank × d_in` and is trained.
- `B` has shape `d_out × rank` and is trained.
- `rank`, usually written `r`, is much smaller than `d_in` and `d_out`.
- `alpha / rank` is the common LoRA training-time scaling convention.
- `lambda` is the adapter strength selected during inference.

The layer's forward pass becomes:

$$
y = Wx + \lambda \frac{\alpha}{r}B(Ax)
$$

Plain-text equivalent:

```text
y = W*x + lambda * (alpha / rank) * B*(A*x)
```

The operation `A*x` first projects the input into a small rank-dimensional space. `B` then projects
that result back to the layer's normal output dimension.

### Parameter savings

A full weight update requires:

$$
d_{out}d_{in}
$$

parameters. A LoRA update requires:

$$
r(d_{in}+d_{out})
$$

parameters.

For a `4096 × 4096` matrix using rank 16:

```text
Full matrix:
4096 * 4096 = 16,777,216 parameters

LoRA matrices:
16 * (4096 + 4096) = 131,072 parameters

Reduction for this matrix:
16,777,216 / 131,072 = 128x fewer trainable parameters
```

Usually one of the matrices is initialized to zero so that, before training:

```text
B*A = 0
W_effective = W
```

Training therefore starts with exactly the base model's behavior.

## Where LoRA lives in an image model

LoRA does not normally replace the whole model. It is inserted into selected layers, commonly:

- attention query, key, value, and output projections;
- transformer MLP projections;
- sometimes convolutional layers; and
- optionally the text encoder.

| Model family | Main denoiser | Typical LoRA targets |
|---|---|---|
| Stable Diffusion / SDXL | Conditional U-Net | Self/cross-attention projections, sometimes convolutional layers and CLIP text encoders |
| FLUX | Diffusion/flow transformer | Transformer attention and MLP projections |
| Video diffusion | Spatiotemporal transformer or 3D U-Net | Spatial attention, temporal attention, MLPs, and sometimes video-specific projections |

The LoRA mathematics is the same across these architectures. What changes is:

- which model modules receive the adapters;
- the input data;
- the denoising or flow-matching objective; and
- the behavior the training examples teach.

## Training an image LoRA

For Stable Diffusion-style training:

1. Load a captioned training image.
2. Encode the image into a latent using the frozen VAE.
3. Sample a diffusion timestep.
4. Add the corresponding amount of noise to the latent.
5. Encode the caption with the text encoder.
6. Ask the denoiser to predict the training target, such as noise or velocity.
7. Compute the diffusion loss.
8. Backpropagate only into the LoRA `A` and `B` matrices.

The base U-Net, VAE, and normally the text encoder remain frozen. LoRA can optionally be added to
the text encoder when the use case benefits from adapting how concepts or tokens are represented.

FLUX uses a flow-matching objective rather than exactly the same noise-prediction objective used by
conventional Stable Diffusion. The LoRA principle remains unchanged: freeze the base transformer
and train low-rank updates inside selected layers.

### What the adapter learns

The learned behavior depends on the training dataset and captions. A LoRA may teach:

- a visual style;
- a character or person;
- a product or object;
- a new visual domain;
- lighting or photographic behavior;
- a composition pattern;
- an editing behavior; or
- for video, potentially motion or temporal style.

A trigger word is not an intrinsic part of LoRA. It is a captioning convention used to associate a
token or phrase with the examples during training.

### What LoRA saves—and what it does not

LoRA reduces:

- the number of trainable parameters;
- optimizer-state memory;
- gradient memory for frozen base weights;
- checkpoint size; and
- the storage needed for multiple specializations.

It does not eliminate the cost of running the base model. Training still performs the base model's
forward computation and retains enough activations to compute gradients for the LoRA paths. Video
training can therefore remain expensive even though the resulting adapter is small.

## Text-to-image inference

The normal pipeline remains:

```text
Prompt -> text embedding
Random latent -> repeated denoising -> decoded image
```

At each denoising step, a targeted layer performs:

```text
base output + scaled LoRA output

W*x + lambda * (alpha / rank) * B*(A*x)
```

The adapter therefore changes how the model interprets and transforms the prompt throughout the
generation process.

A style LoRA might change:

- texture;
- palette;
- lighting;
- line work; and
- shape or composition priors.

A subject LoRA might make a token correspond to a learned person, character, or product.

## Image-to-image inference

Image-to-image does not use a different LoRA mechanism.

The pipeline:

1. Encodes the input image into a latent.
2. Adds noise according to the image-to-image `strength`.
3. Denoises the latent using the prompt and LoRA-modified denoiser.
4. Decodes the resulting latent into an image.

Three controls are easy to confuse:

| Control | What it changes |
|---|---|
| Image-to-image `strength` | How much information from the original image is destroyed before denoising |
| LoRA adapter weight | How strongly the learned adapter modifies the model |
| Guidance scale | How strongly generation follows the positive prompt relative to the unconditional prediction |

Examples:

- Low image strength plus high style-LoRA weight tends to preserve composition while strongly
  restyling details.
- High image strength plus high LoRA weight permits major structural changes toward the LoRA's
  learned distribution.
- High image strength plus low LoRA weight permits strong prompt-driven regeneration with little
  adapter-specific influence.

These controls interact nonlinearly, so the descriptions above are tendencies rather than strict
guarantees.

### LoRA is not automatically an image-conditioning mechanism

A LoRA does not automatically add a new image input to a model. The underlying pipeline must
already support image-to-image or another image-conditioning mechanism.

- Image-to-image supplies an initial latent.
- ControlNet supplies structural conditions such as pose, depth, or edges.
- IP-Adapter supplies learned image-reference features.
- LoRA changes the model's weights and therefore how it responds to those conditions.

Some specialized control LoRAs are trained to add a control behavior, but that behavior results
from their particular architecture and training—not from LoRA universally accepting images.

## Video LoRA

For video, the training sample is a captioned sequence rather than a single image.

A video model may encode the video through a spatial-temporal VAE and process the latent sequence
through spatial and temporal attention. LoRA can then adapt:

- appearance across frames;
- camera motion;
- subject motion;
- temporal style;
- transitions; and
- domain-specific video behavior.

A LoRA trained only on individual images may transfer visual style to a compatible video model, but
it has not learned motion or temporal consistency. It may style individual frames without improving
temporal coherence and may sometimes make flicker or inconsistency worse.

Video LoRA training still processes multiple frames and their activations. Small trainable adapters
therefore do not make video training cheap; they primarily reduce trainable-weight, optimizer, and
checkpoint costs.

## Combining multiple LoRAs

When multiple compatible adapters target the same base model, their weight updates are normally
added:

$$
W_{effective}
=
W + \sum_i \lambda_i\frac{\alpha_i}{r_i}B_iA_i
$$

Plain-text equivalent:

```text
W_effective = W
              + weight_1 * scaled_delta_1
              + weight_2 * scaled_delta_2
              + ...
```

Example:

```python
pipe.load_lora_weights(subject_path, adapter_name="subject")
pipe.load_lora_weights(style_path, adapter_name="style")

pipe.set_adapters(
    ["subject", "style"],
    adapter_weights=[0.8, 0.45],
)
```

Adapter weights:

- do not need to sum to one;
- are not probabilities;
- may be greater than one or negative, although extreme values can be unstable; and
- should be treated as inference hyperparameters.

The weight deltas add linearly, but the neural network's resulting behavior is nonlinear.
Consequently:

- two style LoRAs may conflict;
- a subject LoRA may carry an unwanted background or style;
- adapters may modify overlapping attention behavior; and
- increasing both weights may create artifacts instead of a stronger clean mixture.

A small evaluation grid is safer than guessing:

```text
subject weights: 0.50, 0.75, 1.00
style weights:   0.25, 0.50, 0.75

Keep prompts, seeds, scheduler, steps, guidance, and input images fixed.
```

### Dynamic adapters versus fused adapters

Adapters can remain separate and be applied dynamically, which makes switching and mixing easy.
They can also be fused into the base weights:

```text
W <- W + scaled LoRA update
```

Fusing can avoid repeatedly evaluating the small LoRA branches, but it makes dynamic switching less
convenient. Preserve the original base model and adapter files if you fuse weights.

## Stable Diffusion example

```python
import torch
from diffusers import AutoPipelineForText2Image, AutoPipelineForImage2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
).to("cuda")

pipe.load_lora_weights(
    "/path/to/subject",
    adapter_name="subject",
)

pipe.load_lora_weights(
    "/path/to/style",
    adapter_name="style",
)

pipe.set_adapters(
    ["subject", "style"],
    adapter_weights=[0.8, 0.45],
)

generated = pipe(
    "a portrait of TOK_PERSON in a cinematic watercolor style"
).images[0]

img2img_pipe = AutoPipelineForImage2Image.from_pipe(pipe)

edited = img2img_pipe(
    prompt="TOK_PERSON in a cinematic watercolor style",
    image=input_image,
    strength=0.45,
    guidance_scale=6.5,
).images[0]
```

## FLUX example

```python
import torch
from diffusers import FluxImg2ImgPipeline

pipe = FluxImg2ImgPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16,
).to("cuda")

pipe.load_lora_weights(
    "/path/to/product-lora",
    adapter_name="product",
)

pipe.load_lora_weights(
    "/path/to/style-lora",
    adapter_name="style",
)

pipe.set_adapters(
    ["product", "style"],
    adapter_weights=[0.85, 0.4],
)

result = pipe(
    prompt="a studio advertisement for TOK_PRODUCT",
    image=input_image,
    strength=0.5,
).images[0]
```

The Stable Diffusion and FLUX APIs look similar, but the adapters are not interchangeable. Adapter
tensors must match:

- the base architecture;
- the targeted module names;
- the weight dimensions; and
- usually the specific checkpoint family used during training.

An SDXL LoRA therefore cannot normally be loaded into FLUX.

## Important practical limitations

LoRA:

- does not compress or replace the base model;
- does not automatically accelerate inference;
- is not quantization;
- does not eliminate base-model training compute;
- does not guarantee clean composition with another LoRA;
- does not automatically add a new conditioning modality; and
- cannot normally be transferred across incompatible architectures.

A small adapter file also does not imply that the learned behavior is simple. Subject identity,
style, background correlations, and composition biases can all become entangled in the same
low-rank update.

Training-data quality, caption quality, diversity, regularization, target-module selection, rank,
learning rate, and training duration all affect the resulting adapter. Rank alone is not a quality
setting.

LoRA's primary operational advantage is that one expensive base model can support many small,
switchable specializations.

## Confidence

**VERIFIED for the core LoRA mechanics and cited Diffusers APIs as of 2026-10-02.**

The descriptions of how adapter weight and image-to-image strength interact are practical model
behavior tendencies. Exact behavior depends on the base checkpoint, adapter, scheduler, prompt,
seed, and implementation.

## Primary references

- Hu et al., “LoRA: Low-Rank Adaptation of Large Language Models”:
  https://arxiv.org/abs/2106.09685
- Hugging Face Diffusers LoRA training documentation:
  https://huggingface.co/docs/diffusers/en/training/lora
- Hugging Face Diffusers LoRA loading, composition, and fusion API:
  https://huggingface.co/docs/diffusers/main/en/api/loaders/lora
- Stable Diffusion image-to-image pipeline:
  https://huggingface.co/docs/diffusers/en/api/pipelines/stable_diffusion/img2img
- FLUX pipelines and LoRA examples:
  https://huggingface.co/docs/diffusers/en/api/pipelines/flux
- CogVideoX LoRA training documentation:
  https://huggingface.co/docs/diffusers/en/training/cogvideox
