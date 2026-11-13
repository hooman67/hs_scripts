```markdown
# Goging over MD2 implementation in Colligo

## Questions For colligo

1.  What are end\_points mentioned in the `build.py`? Where are they defined? [cite: 1]
2.  What's the difference between `colligo/models/firefly_v2/diffusion/build.py` and `colligo/models/firefly_v2/clio/build.py`? [cite: 2]
3.  Where is the call method of `ClioMDExecutor` inside `/sensei-fs/users/hshariati/colligo/models/types/src/colligo/models/types/firefly_v2/clio_md.py` actually defined? [cite: 3]
    This is called from `/sensei-fs/users/hshariati/colligo/models/firefly_v2/clio/tests/test_clio_md.py` [cite: 3]
4.  Sdfsd [cite: 4]

## Questions about components

1.  What are the dimensions of the image in here: `image_tensor = request.image.as_torch_sync()` in `colligo/models/firefly_v2/clio/src/colligo/models/clio_v2/ClioMDPipeline.py` line 368 [cite: 3]
2.  How is the `image_control` used (not used right now this is for future)? [cite: 4]
    How is this different from `image_style` (passed to adobeOne model and we pass the image embedding of it to Unet) [cite: 4]
3.  What does crops to LDM component do? [cite: 4]
    Where in the diagram are these ops. Is this doing the multiplication between image and mask? [cite: 5]
    Where do soft\_masks come from? Why is there a `list[Tensor]` of softmax instead of just one? [cite: 6]
4.  What is the `generic_diffusion_avoid_image_embedding` in inputs of diffusion? How is it different from `generic_diffusion_image_embedding`? [cite: 7]
5.  Why are some of diffusion inputs in batch of two for diffusion? [cite: 8]
6.  Like the image embeddings, avoid image embedding, prompts embeddings, etc? [cite: 9]
    Ex: On line 682 of `MDPIpeline` why are the prompts repeating again? [cite: 10]
    Why do we put them in a list of two? Because MOE has two models. [cite: 11]
7.  There is the `colligo/models/firefly_v2/clio/src/colligo/models/clio_v2/components/GenericDiffusionComponent.py` that imports stuff from `colligo/models/types/src/colligo/models/types/firefly_v2/generic_diffusion.py`. [cite: 12]
    Then there is also `colligo/models/firefly_v2/diffusion/src/colligo/models/diffusion_v2/DiffusionModelMD.py` that also imports stuff from generic\_diffusion. what do each of these files do? [cite: 13]
    Seems like the actual core loop is imported in the `diffusionModelMD`. Rename `DiffusionModelMd` to `GenericDiffusionModel.py`. [cite: 14]
8.  What is EPS? [cite: 14]
    Eps model, component etc? [cite: 15]
9.  Go over `diffusion_loop.py` (i.e core\_loop) with Kevin and get more info on sampling and guidance. [cite: 15]
10. Go over `diffusionModelMD` code with Kevin [cite: 16]

[LDM Auto encoder](https://www.cs.cmu.edu/~mgormley/courses/10423//slides/lecture13-text2img.pdf)

## Workflow

1.  `colligo/models/firefly_v2/clio/build.py` [cite: 16]
    Registers the pipeline. [cite: 17]
    Specifies the endpoint, and the classes where the pipeline (called `model_type`), the request and respond are defined. [cite: 17]
    ```python
    build_clio(
        CLIO_MD_V2,
        CLIO_MD_V2_DEPS,
        endpoints=[
            IMAGE_GENERATE_FILL_PUBLIC_ENDPOINT,
        ],
        model_type="colligo.models.clio_v2.ClioMDPipeline.ClioMDPipeline",
        request_type=ClioMDRequest,
        response_type=ClioMDResponse,
    )
    ```
    The build API is defined in: `/sensei-fs/users/hshariati/colligo/models/build/src/colligo/models/build/api.py` [cite: 18]
2.  `colligo/models/types/src/colligo/models/types/firefly_v2/clio_md.py` [cite: 18]
    This defines the request, response, executor, and config types for the pipeline. [cite: 19]
3.  `colligo/models/firefly_v2/clio/src/colligo/models/clio_v2/ClioMDPipeline.py` [cite: 19]
    This defines the pipeline in a class like this: [cite: 19]
    ```python
    class ClioMDPipeline(ColligoPipeline[ClioMDConfig]):
    ```
    Now this class has to have an initialize method but it takes that from the `ColligoPipeline`. [cite: 19]
    Other than that, it defines a load method to load the models and a handle\_request method with the logic of algorithm. [cite: 20]
    ```python
    async def handle_request(self, request: ClioMDRequest) -> ClioMDResponse:
    ```
    The first thing that this method does call `create_request_context` method. [cite: 21]
    This method takes the `request:ClioMdRequest` and creates the `MDRequestContext`. This class is what keeps the algo results. [cite: 22]
    Every method that the algorithm calls puts its results in this object. [cite: 23]
    This method also validates the fields on the request (image dims, prompts length, etc). [cite: 24]
    ```python
    def create_request_context(self, request: ClioMDRequest) -> MDRequestContext:
    ```
    This method Validates the inputs, normalizes the images, and decides on the workflow (the algorithm) based on provided input. [cite: 25]
    ```python
    async def run_img_generation
    ```
    This method calls: `run_img_generation_on_global`, `run_global_to_local_transform`, `run_img_generation_on_global`, `upsampler`, and `decoder`. [cite: 26]
    The pipeline has 2 instances of `genericDiffusion Componenet`. [cite: 26]
    One for global steps and another for local steps: [cite: 27]
    ```python
            self.generic_diffusion_local = GenericDiffusionComponent(
                name="ClioMD V2 GenericDiffusionComponent Local",
                config=genric_diffusion_local_config,
            )
            self.generic_diffusion_global = GenericDiffusionComponent(
                name="ClioMD V2 GenericDiffusionComponent Global",
                config=genric_diffusion_global_config,
            )
    ```
    All `run_img_generation_on_global` and `run_img_generation_on_global` is prepare `generciDiffusionComponent` Inputs and pass it to their individual instances of the component. [cite: 28]
4.  `colligo/models/firefly_v2/clio/src/colligo/models/clio_v2/components/GenericDiffusionComponent.py` [cite: 29]
    Imports from `generic_diffiusion.py` (below) only. It also takes some interfaces for guidance and sampling parameters from `interface.py`. [cite: 29]
    ```python
    from colligo.models.types.firefly_v2.generic_diffusion import (
        DIFFUSION_L86_L87,
        DIFFUSION_MD_L86_L87,
        ConditionTensorType,
        DiffusionDimension,
        DiffusionExecutor,
        DiffusionRequest,
        ExifType,
        LayerAttnMaskType,
    )
    ```
5.  `colligo/models/types/src/colligo/models/types/firefly_v2/generic_diffusion.py` [cite: 30]
6.  `DiffusionModelMD.py` VS `DiffusionModel.py` [cite: 30]
    Both of them have these: [cite: 30]
    `core_loop`, `mixture_of_models_loop`, `exif_utils`, `guidance Parameters` `eps_utils`, `t5_adaptor` `# update to 4.` `BATCH_SIZE = 1` `WARMUP_ITERS = 3` `SUPPORTED_INPUT_SIZE = (128, 4096)` `SUPPORTED_BATCH_SIZES = [1]` [cite: 31]
    ```python
    ENGINE_PREFIX: dict[tuple[GpuType | None, bool], str] = {
        (GpuType.NVIDIA_A10G, False): "ait_engine_bs1",
        (GpuType.NVIDIA_A100_80GB, False): "ait_engine_bs1",
        (GpuType.NVIDIA_A100_40GB, False): "ait_engine_bs1",
        (GpuType.NVIDIA_A10G, True): "ait_engine_a10g_bs2",
        (GpuType.NVIDIA_A100_80GB, True): "ait_engine_a100_bs2",
        (GpuType.NVIDIA_A100_40GB, True): "ait_engine_a100_bs2",
    }

    class SwappingConfig(int, Enum):
        No_Swap = 0
        Update_weight = 1  # when the is on AIT but two checkpoints
        Unload_load_weights = 2  # when there are two AITs and two checkpoints
    ```
    Only `DiffusionModel` has these: [cite: 31]
    `GuidanceType`, `LayerAttnMaskModelTypes`, `clamp` [cite: 31]
    ```python
    from colligo.models.types.firefly_v2.diffusion import (
        DiffusionConfig,
        DiffusionDimension,
        DiffusionRequest,
        DiffusionResponse,
        GenerationType,
    )

    def calculate_attention_mask_type_guide_strength
    def calculate_attention_mask_type_rlhf_creativity
    def layer_attention_for_vanilla
    def layer_attention_for_style_zero
    def layer_attention_for_show_similar
    def layer_attention_factory
    ```
    Only `DiffusionModelMD` has these: [cite: 32]
    `MultidiffusionConditionTensors`, `SamplingParameters`,`T5AdaptorInput` [cite: 32]
    ```python
    from colligo.models.types.firefly_v2.generic_diffusion import (
        ConditionTensorType,
        DiffusionDimension,
        DiffusionExecutor,
        DiffusionRequest,
        ExifType,
        LayerAttnMaskType,
    )

    def _to_torch_sync
    ```
    These files are never imported, the classes they define is registered inside `colligo/models/firefly_v2/diffusion/build.py` below. [cite: 32]
    This is the file that calls the `core_loop` to actually do the diffusion. [cite: 33]
    This is imported from this file that is in `clioCore`: `colligo/vendor/AdobeDiffusion/cliocore/diffusion_core/src/clio/diffusion_core/diffusion_loop.py` [cite: 34]
    My notes are made directly in the code here: `DiffusionModelMd.py` [cite: 34]
7.  `colligo/models/firefly_v2/diffusion/build.py` [cite: 34]
    This file builds the `DiffiusionMD` and normal Diffusion models. [cite: 35]
    But it still imports stuff from `generic_diffiusion.py` (for MD) and from `diffiusion.py` for normal. [cite: 35]
    It also registers the classes for the models (`DiffusionModelMD` and `DiffusionModel`) but doesn't import anything from these files (just registers the models). [cite: 36]
8.  `colligo/vendor/AdobeDiffusion/cliocore/diffusion_core/src/clio/diffusion_core/diffusion_loop.py` [cite: 37]
    Defines the `core_loop` function. [cite: 37]
    This is where the reverse diffusion process happens. [cite: 37]
    I have made comments directly into my copy of the python file here: `core_loop` [cite: 38]
    Note that the noise prediction from Unet happens here: `noise_pred = guidance_fn(guidance_interface)` [cite: 38]
    Note: The EPS model is actually the unet. [cite: 38]
    This is passed to the `core_loop` using `eps_callable`. This is then passed to the `guidance_interface` here: `eps_model=eps_callable,` [cite: 39]
    Calculating the previous sample (i.e the next step in the reverse diffusion process) happens here: `val = sampler.step(sampler_params)` [cite: 39]
    This essentially subtracts the predicted noise from the current sample. [cite: 39]
    Note that the final output is `predicted_x0_image` [cite: 40]
9.  `colligo/vendor/AdobeDiffusion/cliocore/typings/src/clio/typings/guidance_interface.py` [cite: 40]
    This defines the `guidance_interface` which calls the `eps_callable` to actually run the unet to get the predicted noise. [cite: 40]
10. Sdf [cite: 41]

## MD2 Pipeline

The goals of this is delivering inpainting related tasks but will enable other capabilities such as generative compositing and multi-modal generation, etc. going forward. [cite: 41]
This is where the request, response, and handle\_request functions for a model get combined for both txt2img and MD2: `/sensei-fs/users/hshariati/colligo/models/firefly_v2/clio/build.py` [cite: 42]

```python
# Build ClioMD
build_clio(
    CLIO_MD_V2,
    CLIO_MD_V2_DEPS,
    endpoints=[
        IMAGE_GENERATE_FILL_PUBLIC_ENDPOINT,
    ],
    model_type="colligo.models.clio_v2.ClioMDPipeline.ClioMDPipeline",
    request_type=ClioMDRequest,
    response_type=ClioMDResponse,
)
```

## Component Design

### Component Config Requirements

1.  We need BOTH runtime (for things that are more like input) and loadtime configs. [cite: 42]
2.  We need to solve the case for Components that share the same parameters [cite: 43]

**Pipeline will take an input\_config (runtime) yaml format that defines parameters that multiple components share.** [cite: 43]
**Load time configs are called configs and runtime configs are called parameters.** [cite: 44]
Get rid of anchor promp and anchor embedding this is just avoid [cite: 45]

## T5 In Colligo

### V2 Models:

`hshariati/colligo/models/firefly_v2/clio/src/colligo/models/clio_v2/ClioPipeline.py` [cite: 45]
Imports: `run_t5` from `utils/t5.py` [cite: 45]

`hshariati/colligo/models/firefly_v2/clio/src/colligo/models/clio_v2/utils/t5.py` [cite: 45]
Defines: `run_t5` [cite: 45]
Imports: `T5Request`, `T5Executor` [cite: 45]

`hshariati/colligo/models/types/src/colligo/models/types/firefly_v2/t5.py` [cite: 45]
Defines: `T5Config`, `T5Request`, `T5Response` [cite: 45]
And `T5_V2 = "t5_v2"` [cite: 45]

### V1 Models:

`hshariati/colligo/models/firefly/t5/src/colligo/models/t5/T5Model.py` [cite: 45]
Imports: `T5Config`, `T5Request`, `T5Response` from v1 (not firefly\_v2) [cite: 45]

`hshariati/colligo/models/types/src/colligo/models/types/t5.py` [cite: 45]
Defines: `T5Config`, `T5Request`, `T5Response` [cite: 45]
And `T5_XL_V1 = "t5_xl_v1"` `T5_XXL_V1 = "t5_xxl_v1"` `T5_UL2_V1 = "t5_ul2_v1"` [cite: 45]

On the SDK side we have something like this: [cite: 46]
```python
moe_input = MixtureOfModelsTensors(
    lst_positive_conditions=lst_positive_conditions,
    lst_negative_conditions=lst_negative_conditions,
    t5_text_embedding = self.t5_model_for_eps_model.text_model(
        prompt_processor_result.text_prompt
    ),
)
```

```python
class PromptProcessorType:
    text_prompt: str | None = None
    avoid_prompt: str | None = None
    style_prompt: str | None = None
    content: str = ""
    keywords: str = ""
    exif: ExifInformation = ExifInformation()
```

On the Colligo side we have this: [cite: 48]
```python
return await run_t5_embeddings(
    prompts=request_context.prompts,
    anchor_prompt=request_context.anchor_prompt,
    content_type=request_context.content_type,
    keyword_prompt=request_context.keywords_prompt,
)
```

```python
class RequestContext(BaseModel):
    keywords_prompt: str = ""
    prompts: list[str] = []
    anchor_prompt: Optional[str] = None
    content_type: ContentType = ContentType.UNCONDITIONED
```

## T5 Component First Thoughts

Input is the text prompt and the output is the embedding [cite: 49]

[https://git.corp.adobe.com/colligo/colligo/blob/main/models/firefly\_v2/t5/src/colligo/models/t5\_v2/T5Model.py](https://git.corp.adobe.com/colligo/colligo/blob/main/models/firefly_v2/t5/src/colligo/models/t5_v2/T5Model.py)

`t5_model_for_eps_model` in [cite: 49]
[https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/dev/apps/inference/inference/inference\_md\_app.py](https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/dev/apps/inference/inference/inference_md_app.py)

Create a component that envokes this t5 model. [cite: 50]
Due to padding, the results of the same ML model on AD and Colligo will be different. [cite: 50]
On AD side we always pad the tokens 128 and then pass through. [cite: 51]
This is where that's happening: [https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/86a73dd2b987f0f3c48b592d45ddcc4166943101/cliocore/core\_models/encoders/src/clio/core\_models/encoders/text\_encoders.py#L240](https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/86a73dd2b987f0f3c48b592d45ddcc4166943101/cliocore/core_models/encoders/src/clio/core_models/encoders/text_encoders.py#L240) [cite: 52]

Kevin added the end results padding (instead of the token) to match the shape of the results [cite: 52]
[https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/86a73dd2b987f0f3c48b592d45ddcc4166943101/cliocore/colligo\_models/src/clio/colligo\_models/t5\_encoder.py#L49](https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/86a73dd2b987f0f3c48b592d45ddcc4166943101/cliocore/colligo_models/src/clio/colligo_models/t5_encoder.py#L49) [cite: 52]

This colligo model, calls the colligo end point. [cite: 53]
This is just the traced one. [cite: 53]

The one in core is the torch model. [cite: 53]
Checkout the `run_t5` method on colligo side. [cite: 54]

## From Shayan

`colligo.models.clio_v2.ClioMdPipeline.ClioMdPipeline` [cite: 54]

Make a folder here: [cite: 54]
[https://git.corp.adobe.com/colligo/colligo/tree/main/models/firefly\_v2/clio/src/colligo/models/clio\_v2](https://git.corp.adobe.com/colligo/colligo/tree/main/models/firefly_v2/clio/src/colligo/models/clio_v2) [cite: 54]

[https://git.corp.adobe.com/colligo/colligo/tree/main/models/types](https://git.corp.adobe.com/colligo/colligo/tree/main/models/types) [cite: 54]

These are just for code (anything before src will not come into code) [cite: 54]
`Firefly_v2/clip/src/colligo/models/clio_v2/Components/PromptProcessing` [cite: 54]

`Firefly_v2/clio/Tests/Components/PromptProcessing` [cite: 54]

Your tests must be `test_PromptProcessing.py` [cite: 55]
Any code folder must have an `init.py` [cite: 55]

These are not pip installable but Shayan can make it pip installable. [cite: 55]
Without this, they can checkout colligo and use "pip install -e" for devs. 1-2 weeks. [cite: 55]

## Prompt Processing in Colligo

### First meeting with Kevin

Two asks: [cite: 56]

1.  `DiffiusionModel` component should receive a list instead of single input [cite: 56]

Add copy write headers. [cite: 57]

### Input to prompt processing

This is the input to the component [cite: 57]

```python
# Prompt Processing
prompt_processor_input = PromptProcessorType(
    text_prompt=text_prompt,
    avoid_prompt=avoid_prompt,
    style_prompt=style_prompt if isinstance(style_prompt, str) else None,
    #add avoid_content and
    #avoid_keywords
    # avoid_style #this wont go into T5 goes into prior
    content="",
    keywords="",
    exif=ExifInformation(),

)
```

Makes one of these for each EPS model: [cite: 58]

```python
prompt_processor_input = [
    copy.deepcopy(prompt_processor_input) for _ in range(len(self.eps_model))
]
```

The EPS model is the diffusion model. [cite: 59]
In MOE we have multiple. So we have one input for each one in Inference App. [cite: 59]
But in Colligo we need to figure out how to do this. The `diffusionComponent` in colligo accepts only one. [cite: 60]
But we need a list in the future. [cite: 61]

`self.config.prompt_processing_config` tells you which prompt processing you gonna use [cite: 61]
For md we only care about the diffusion one.]]] [cite: 61]

The output of the component will be this: [cite: 61]

```python
prompt_processor_results = [
    self.process_input_prompts(
        prompts=prompt_processor_input[k],
        prompt_processing_config_index=k,
        control_prompt=control_prompt,
    )
    for k in range(len(self.eps_model))
]
```

***Gonna be an object of lists in colligo.** [cite: 62]
Instead of a list of objects like above in sdk [cite: 62]
And then the pipeline will need to know the order of the models and ensure that [cite: 63]
Txt2img ones get Photo and MD ones get None. [cite: 63]
(Xingtai) [cite: 64]

There is no ml model in prompt processing. It just takes some text from user and modifies it. [cite: 64]
The prompt processing factory will will generate functions based on the config and passes them. [cite: 65]
We can access the `prompt_utils.py` on the colligo side. [cite: 66]
But we need to checkout france's branch [cite: 67]
Since he has some stuff hardcoded. [cite: 67]
We'll put his hardcoded version in colligo for now, later we'll update the SDK one and then just use that. [cite: 68]
This component won't need the factory because we don’t use the other functions in SDK. [cite: 69]
For now just directly call the multi-diffusion function. [cite: 70]

## Solution:

Prompt processing receives a list of prompts. [cite: 70]
And in input/config telling it whether this is for MD or not. [cite: 71]
`Set_content_ttypes` should take None if the model is MD and photo if its text2img. [cite: 72]
Andthe [cite: 73]

```python
set_content_types=[None] if len(self.eps_model) == 1 else [None, "photo"]
prompt_processor_results=[
    self.process_input_prompts(
        prompts=prompt_processor_input[k],
        prompt_processing_config_index=k,
        control_prompt=control_prompt,
        set_content_type=set_content_types[k],  # added to fix the photo
    )
    for k in range(len(self.eps_model))
]
```

## TODO:

1.  Make the changes to `get_fixed_noise` to add the `num_Frames` param. [cite: 74]
    This is used in `DiffusionModelMd`. So it needs to remain compatible. PR against adobe diffusion. [cite: 75]
2.  Make sure input/output are the same. [cite: 76]
```