```markdown
# ADOBE CONFIDENTIAL

```python
# ___________________
#
#  Copyright 2023 Adobe
#  All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains
# the property of Adobe and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Adobe
# and its suppliers and are protected by all applicable intellectual
# property laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe.
from enum import Enum
from typing import cast
import torch
from clio.diffusion_core.diffusion_loop import core_loop
from clio.diffusion_core.mixture_of_models_loop import (
    MixtureOfModels,
    mixture_of_models_fixed_noise,
)
from clio.process_utils.exif_utils import exif_type_to_tensor
from clio.typings.interface import (
    ConditionTensors,
    CoreParameters,
    CoreResult,
    DiffusionUnetAITConfig,
    FilePath,
    GuidanceParameters,
    InferenceConfig,
    ModelLoader,
    MultidiffusionConditionTensors,
    SamplingParameters,
)
from clio.typings.typings import ExifInformation, T5AdaptorInput
from colligo.base.device_ctx import get_current_device
from colligo.base.exceptions import ColligoValidationException, runtime_assert
from colligo.base.gpu_utils import get_gpu_index
from colligo.base.log_codes import LogCode
from colligo.base.logging import logger
from colligo.base.profiling import annotate
from colligo.base.types.gpu import GpuType
from colligo.base.types.model import ColligoMLModel
from colligo.base.types.tensor import Tensor
from colligo.models.diffusion_v2.eps_utils import (
    AITManager,
    initialize_eps_model,
    str_to_inference_config,
)
from colligo.models.diffusion_v2.vendor.t5_adaptor import (  # type: ignore[attr-defined]
    initialize_t5_adaptor,
)
from colligo.models.types.firefly_v2.generic_diffusion import (
    ConditionTensorType,
    DiffusionConfig,
    DiffusionDimension,
    DiffusionRequest,
    DiffusionResponse,
)
# update to 4.
BATCH_SIZE = 1
WARMUP_ITERS = 3
SUPPORTED_INPUT_SIZE = (128, 4096)
SUPPORTED_BATCH_SIZES = [1]

def _to_torch_sync(obj: Tensor | None) -> torch.Tensor | None:
    return obj.as_torch_sync() if obj is not None else None

class SwappingConfig(int, Enum):
    No_Swap = 0
    Update_weight = 1  # when the is on AIT but two checkpoints
    Unload_load_weights = 2  # when there are two AITs and two checkpoints

ENGINE_PREFIX: dict[tuple[GpuType | None, bool], str] = {
    (GpuType.NVIDIA_A10G, False): "ait_engine_bs1",
    (GpuType.NVIDIA_A100_80GB, False): "ait_engine_bs1",
    (GpuType.NVIDIA_A100_40GB, False): "ait_engine_bs1",
    (GpuType.NVIDIA_A10G, True): "ait_engine_a10g_bs2",
    (GpuType.NVIDIA_A100_80GB, True): "ait_engine_a100_bs2",
    (GpuType.NVIDIA_A100_40GB, True): "ait_engine_a100_bs2",
}

class DiffusionModelMD(ColligoMLModel[DiffusionConfig]):
    diff_config: list[InferenceConfig]
    eps_model: list[AITManager]
    model_swap_config: SwappingConfig
    def load_model(self) -> None:
        self.diff_config = [str_to_inference_config(config) for config in self.model_config.inference_config]
        self.model_swap_config = (
            SwappingConfig.Update_weight
            if self.model_config.num_checkpoints_per_model > 1
            else (SwappingConfig.Unload_load_weights if len(self.diff_config) > 1 else SwappingConfig.No_Swap)
        )
        gpu_device = get_current_device()
        self.eps_model = []
        self.t5_adaptor = []
        device_int = get_gpu_index(get_current_device())
        assert device_int is not None  # mypy
        ait_eng_prefix = ENGINE_PREFIX[(self.deploy_config.gpu.type, self.model_config.batch_cfg)]
        for idx, config in enumerate(self.diff_config):
            ait_engine = self.get_file(f"{ait_eng_prefix}_{idx}").path
            files = list(ait_engine.glob("*"))
            if len(files) == 1 and files[0].is_dir():
                # by accident we included an extra subdir
                ait_engine = files[0]
            diffusion_unet = config.model_configs.diffusion_unet
            assert isinstance(diffusion_unet, ModelLoader)
            guidance_parameters = config.guidance_parameters
            assert isinstance(guidance_parameters, GuidanceParameters)
            unet_ait_config = diffusion_unet.unet_ait_config
            assert isinstance(unet_ait_config, DiffusionUnetAITConfig)
            # [FIREFLY-6584] FIXME: this is short term workaround
            config.seeds = list(range(BATCH_SIZE))
            diffusion_unet.device = device_int
            unet_ait_config.engine_folder = FilePath(raw=str(ait_engine))
            unet_ait_config.out_channels = 4
            torch_checkpoint = [
                str(self.get_file(f"torch_checkpoint_{self.model_config.num_checkpoints_per_model * idx + ind}").path)
                for ind in range(self.model_config.num_checkpoints_per_model)
            ]
            dimensions: list[tuple[int, int]] = []
            for dim in DiffusionDimension:
                width, height = dim.value
                dimensions.append((height, width))
            self.eps_model.append(
                initialize_eps_model(
                    config,
                    resolutions=dimensions,
                    check_points=torch_checkpoint,
                    batch_cfg=self.model_config.batch_cfg,
                    break_model=self.model_swap_config != SwappingConfig.No_Swap,
                )
            )
            t5_encoder_for_eps_model = config.model_configs.t5_encoder_for_eps_model
            assert t5_encoder_for_eps_model is not None
            t5_torch_config = t5_encoder_for_eps_model.t5_torch_config
            assert t5_torch_config is not None
            t5_max_length = t5_torch_config.max_length
            assert t5_max_length is not None
            self.t5_max_length = t5_max_length
            for chkpoint in torch_checkpoint:
                logger.info("Loading T5 Adapter model on %s", gpu_device)
                t5_adaptor = config.model_configs.t5_adaptor
                assert t5_adaptor is not None
                t5_adaptor.torch_checkpoint = FilePath(raw=chkpoint)
                t5_adaptor.device = device_int
                t5_adaptors, _ = initialize_t5_adaptor(config)
            self.t5_adaptor.append(t5_adaptors[0])
    def warmup_model(self) -> None:
        device = get_current_device()
        torch.cuda.empty_cache()
        # Warmup the JIT of the tracing model by running all input sizes 3 times.
        for adapter in self.t5_adaptor:
            for batch_size in SUPPORTED_BATCH_SIZES:
                embeddings = torch.randn(
                    batch_size,
                    SUPPORTED_INPUT_SIZE[0],
                    SUPPORTED_INPUT_SIZE[1],
                    device=device,
                ).bfloat16()
                for _ in range(WARMUP_ITERS):
                    adapter(embeddings, embeddings, None, embeddings)
    def _pad_t5_adapter_embeddings(self, embedding: torch.Tensor) -> torch.Tensor:
        pad_length = self.t5_max_length
        # FIXME: torch has dedicate padding functionality, use that.
        padded_embeddings = torch.zeros(
            (embedding.shape[0], pad_length, embedding.shape[2]),
            device=get_current_device(),
        )
        padded_embeddings[:, : embedding.shape[1], :] = embedding
        return padded_embeddings
    @torch.no_grad()
    def _run_t5_adapter(
        self,
        idx: int,
        t5_adaptor_input: T5AdaptorInput,
    ) -> torch.Tensor | None:
        if t5_adaptor_input.text_prompt_embedding is None:
            return None
        result = self.t5_adaptor[idx](
            self._pad_t5_adapter_embeddings(t5_adaptor_input.text_prompt_embedding).bfloat16(),
            self._pad_t5_adapter_embeddings(t5_adaptor_input.content_type_embedding).bfloat16()
            if t5_adaptor_input.content_type_embedding is not None
            else None,
            t5_adaptor_input.exif_embedding.bfloat16()
            if t5_adaptor_input.exif_embedding is not None
            else torch.zeros([3, 1], dtype=torch.bfloat16, device=get_current_device()),
            self._pad_t5_adapter_embeddings(t5_adaptor_input.keywords_embedding).bfloat16()
            if t5_adaptor_input.keywords_embedding is not None
            else None,
            t5_adaptor_input.aesthetic_score.to(device=get_current_device()).bfloat16()
            if t5_adaptor_input.aesthetic_score is not None
            else None,
            t5_adaptor_input.is_genai.to(device=get_current_device())
            if t5_adaptor_input.is_genai is not None
            else None,
        )
        return cast(torch.Tensor, result)
    def _gather_t5_adaptor_inputs(
        self, request: DiffusionRequest, batch_size: int
    ) -> tuple[list[T5AdaptorInput], list[T5AdaptorInput]]:
        # from the diffusion request, gets the input and avoid conditions for the T5Adaptor
        inputs, avoids = [], []
        # TODO add validation to make sure all request inputs are the same length as number of EPS models
        for idx in range(len(request.text_embedding.tensor_list)):
            t5_adaptor_input = T5AdaptorInput()
            text_embedding = request.text_embedding.tensor_list[idx]
            if type(text_embedding) == Tensor:
                t5_adaptor_input.text_prompt_embedding = text_embedding.as_torch_sync()
            content_type_embedding = request.content_type_embedding.tensor_list[idx]
            if type(content_type_embedding) == Tensor:
                t5_adaptor_input.content_type_embedding = content_type_embedding.as_torch_sync()
            keywords_embedding = request.keywords_embedding.tensor_list[idx]
            if type(keywords_embedding) == Tensor:
                t5_adaptor_input.keywords_embedding = keywords_embedding.as_torch_sync()
            exif_idx = request.exif[idx]
            if exif_idx is not None:
                t5_adaptor_input.exif_embedding = exif_type_to_tensor(
                    ExifInformation(
                        focal_length=exif_idx.focal_length,
                        shutter_speed=exif_idx.shutter_speed,
                        aperture=exif_idx.aperture,
                    )
                )
                # Process Batch
                if t5_adaptor_input.exif_embedding is not None:
                    t5_adaptor_input.exif_embedding = t5_adaptor_input.exif_embedding.repeat(1, batch_size)
                    t5_adaptor_input.exif_embedding = t5_adaptor_input.exif_embedding.to(get_current_device())
            t5_adaptor_input.aesthetic_score = torch.Tensor([request.aesthetic_score[idx]])
            t5_adaptor_input.is_genai = torch.Tensor([request.is_genai[idx]])
            inputs.append(t5_adaptor_input)
            t5_adaptor_input_avoid = T5AdaptorInput()
            avoid_text_embedding = request.avoid_text_embedding.tensor_list[idx]
            if avoid_text_embedding:
                t5_adaptor_input_avoid.text_prompt_embedding = avoid_text_embedding.as_torch_sync()
            avoid_content_type_embedding = request.avoid_content_type_embedding.tensor_list[idx]
            if avoid_content_type_embedding:
                t5_adaptor_input_avoid.content_type_embedding = avoid_content_type_embedding.as_torch_sync()
            avoid_keywords_embedding = request.avoid_keywords_embedding.tensor_list[idx]
            if avoid_keywords_embedding:
                t5_adaptor_input_avoid.keywords_embedding = avoid_keywords_embedding.as_torch_sync()
            avoid_exif = request.avoid_exif[idx]
            if avoid_exif is not None:
                t5_adaptor_input_avoid.exif_embedding = exif_type_to_tensor(
                    ExifInformation(
                        focal_length=avoid_exif.focal_length,
                        shutter_speed=avoid_exif.shutter_speed,
                        aperture=avoid_exif.aperture,
                    )
                )
                if t5_adaptor_input_avoid.exif_embedding is not None:
                    t5_adaptor_input_avoid.exif_embedding = t5_adaptor_input_avoid.exif_embedding.repeat(1, batch_size)
                    t5_adaptor_input_avoid.exif_embedding = t5_adaptor_input_avoid.exif_embedding.to(
                        get_current_device()
                    )
            t5_adaptor_input_avoid.aesthetic_score = torch.Tensor([request.avoid_aesthetic_score[idx]])
            t5_adaptor_input_avoid.is_genai = torch.Tensor([request.avoid_is_genai[idx]])
            avoids.append(t5_adaptor_input_avoid)
        return inputs, avoids
    def _process_image_embeddings(
        self, request: DiffusionRequest
    ) -> tuple[list[torch.Tensor | None], list[torch.Tensor | None]]:
        # from the diffusion request, gets the input and avoid image-embeddings
        # TODO add validation to make sure all request inputs are the same length as number of EPS models
        inputs, avoids = [], []
        for idx in range(len(request.image_embedding.tensor_list)):
            image_embedding = _to_torch_sync(request.image_embedding.tensor_list[idx])
            if image_embedding is not None and len(image_embedding.shape) == 2:
                image_embedding = image_embedding.unsqueeze(0)
            inputs.append(image_embedding)
            avoid_image_embedding = _to_torch_sync(request.avoid_image_embedding.tensor_list[idx])
            if avoid_image_embedding is not None and len(avoid_image_embedding.shape) == 2:
                avoid_image_embedding = avoid_image_embedding.unsqueeze(0)
            avoids.append(avoid_image_embedding)
        return inputs, avoids
    def handle_model_request(self, request: DiffusionRequest) -> DiffusionResponse:
        '''
        Input Validation:
        It checks if the batch size of the input seeds matches the predefined BATCH_SIZE.
        If not, it raises an exception.
        '''
        batch_size = len(request.seeds)
        if batch_size != BATCH_SIZE:
            raise ColligoValidationException(f"Invalid batch size {batch_size}, must be {BATCH_SIZE}")

        '''
        Preprocessing:
        The function then extracts various components from the input request, such as text and image embeddings,
        binary masks, initial images, and other parameters needed for the core loop.
        '''
        (width, height) = request.dimension.value
        # Preprocess text inputs
        t5_adaptor_inputs, t5_adaptor_input_avoids = self._gather_t5_adaptor_inputs(
            request=request, batch_size=batch_size
        )
        text_embeddings = []
        avoid_text_embeddings = []
        for idx in range(len(self.t5_adaptor)):
            text_embeddings.append(self._run_t5_adapter(idx, t5_adaptor_inputs[idx]))
            avoid_text_embeddings.append(self._run_t5_adapter(idx, t5_adaptor_input_avoids[idx]))
        # preprocess image embedding before core_loop
        image_embeddings, avoid_image_embeddings = self._process_image_embeddings(request=request)
        # generate random noise in PyTorch here if it is not given in the request
        initial_image = (
            torch.zeros(
                (
                    batch_size,
                    self.diff_config[0].dimensions.channels,  # FIXME@kduarte indexing at 0 scares me...
                    height,
                    width,
                ),
                device=get_current_device(),
            )
            if request.initial_image is None
            else request.initial_image.as_torch_sync()
        )
        binary_mask = [_to_torch_sync(x) for x in request.binary_mask]
        # Tile binary_mask to be the same batch size as others.
        # TODO: FIREFLY-13963
        if binary_mask and binary_mask[0] is not None and binary_mask[0].size(1) != batch_size:
            binary_mask = [tensor[:, :batch_size, :, :] if tensor is not None else None for tensor in binary_mask]
        hard_mask = _to_torch_sync(request.hard_mask)
        original_image = _to_torch_sync(request.original_image)
        mask_type = [_to_torch_sync(mask_type) for mask_type in request.mask_type.tensor_list]
        mask_type = [x.to(torch.int32) if x is not None else None for x in mask_type]
        avoid_mask_type = [_to_torch_sync(avoid_mask_type) for avoid_mask_type in request.avoid_mask_type.tensor_list]
        avoid_mask_type = [x.to(torch.int32) if x is not None else None for x in avoid_mask_type]
        text_layer_attn_mask = [_to_torch_sync(attn_mask) for attn_mask in request.text_layer_attn_mask.tensor_list]
        image_layer_attn_mask = [_to_torch_sync(attn_mask) for attn_mask in request.image_layer_attn_mask.tensor_list]
        # === CORE LOOP ------- #### BELOW IS NOT DONE YET!
        if request.configs is None:
            raise Exception("config is empty")






        '''
        Core Loop Initialization:
        It initializes the core parameters for the diffusion model, including the number of models and their
        specific parameters.
        '''
        params = CoreParameters.parse_raw(
            request.configs
        )  # adarabi-TODO: make sure the SDK version of sender matches to the reciver
        moe_model = MixtureOfModels(params=params)
        runtime_assert(
            moe_model.number_of_models == len(self.diff_config),
            "moe request doesn't match the current number of loaded models",
        )
        previous_image = initial_image
        core_response: CoreResult | None = CoreResult(iterates=initial_image, predicted_x0_image=initial_image)
        '''
        class CoreResult(BaseModel):
            iterates: torch.Tensor | None
            predicted_x0_image: torch.Tensor | None
            sampler_model_outputs: list[torch.Tensor | None] | None
        '''



        '''
        Core Loop Execution:
        It iterates through the different models in the mixture of models (MoE) and executes the core loop for each model.
        '''
        for idx in range(moe_model.number_of_models):
            core_param = moe_model.params_of_kth_model(idx)
            if (
                core_param.iteration_parameters.sample_intervals[0]
                == core_param.iteration_parameters.sample_intervals[1]
            ):
                continue

        '''
        For each model, it prepares input tensors based on the type of condition tensor provided in the
        request (either CONDITION_TENSOR or MULTIDIFFUSION_CONDITION_TENSOR).
        '''
            condition_tensor_type = request.condition_tensor_type[idx]
            if condition_tensor_type == ConditionTensorType.CONDITION_TENSOR:
                inputs: ConditionTensors | MultidiffusionConditionTensors = ConditionTensors(
                    text_embedding=text_embeddings[idx],
                    image_embedding=image_embeddings[idx],
                    text_layer_attn_mask=text_layer_attn_mask[idx],
                    image_layer_attn_mask=image_layer_attn_mask[idx],
                )  # Type annotation to deal with mypy
                avoids: ConditionTensors | MultidiffusionConditionTensors = ConditionTensors(
                    text_embedding=avoid_text_embeddings[idx],
                    image_embedding=avoid_image_embeddings[idx],
                    text_layer_attn_mask=None,  # TODO fill in based on request
                    image_layer_attn_mask=None,  # TODO fill in based on request
                )  # Type annotation to deal with mypy
            elif condition_tensor_type == ConditionTensorType.MULTIDIFFUSION_CONDITION_TENSOR:
                runtime_assert(hard_mask is not None, "You did not give a binary mask to an MD model.")
                runtime_assert(original_image is not None, "You did not give the original image to an MD model.")
                runtime_assert(mask_type[idx] is not None, "You did not give a mask_type to an MD model")
                assert hard_mask is not None  # This solves mypy issue, above runtime_assert does not...
                one_minus_hard_mask = 1 - hard_mask
                inputs = MultidiffusionConditionTensors(
                    text_embedding=text_embeddings[idx],
                    image_embedding=image_embeddings[idx],
                    text_layer_attn_mask=text_layer_attn_mask[idx],
                    image_layer_attn_mask=image_layer_attn_mask[idx],
                    mask_type=mask_type[idx],
                    original_image=original_image,
                    one_minus_binary_mask=one_minus_hard_mask,
                )
                avoids = MultidiffusionConditionTensors(
                    text_embedding=avoid_text_embeddings[idx],
                    image_embedding=avoid_image_embeddings[idx],
                    text_layer_attn_mask=None,  # TODO fill in based on request
                    image_layer_attn_mask=None,  # TODO fill in based on request
                    mask_type=avoid_mask_type[idx],
                    original_image=original_image,
                    one_minus_binary_mask=one_minus_hard_mask,
                )



        '''
        It generates random noise for the diffusion process and applies binary masks if provided.
        '''
            noise_list = mixture_of_models_fixed_noise(
                idx,
                core_param,
                request.seeds,
                get_current_device(),
                length_scale=request.noise_length_scale,
            )
            b_mask = binary_mask[idx]

        '''
        The core loop is executed using the core_loop function, which takes various inputs, including the
        model's callable, initial image, noise, input and avoid tensors, parameters, and binary masks.
        Optionally, it may load or unload model weights based on the specified swapping configuration.
        '''
            if core_response is not None:
                if core_param.iteration_parameters.add_noise_to_initial_image:
                    assert core_response.predicted_x0_image is not None  # mypy
                    previous_image = core_response.predicted_x0_image
                else:
                    assert core_response.iterates is not None  # mypy
                    previous_image = core_response.iterates
                sampler_model_outputs = (
                    core_response.sampler_model_outputs if core_param.iteration_parameters.use_sampler_history else None
                )
            sampler_model_outputs = None
            if idx > 0:
                sampling_params = core_param.sampling_parameters
                assert isinstance(sampling_params, SamplingParameters)  # mypy
                if sampling_params.use_initial_image_in_second_stage:  # MD usecase
                    assert b_mask is not None  # mypy
                    initial_image = b_mask[0, ...] * previous_image + (1 - b_mask[0, ...]) * initial_image
                else:
                    initial_image = previous_image  # Replicates MoE.dispatch in AdobeDiffusion
            if self.model_swap_config == SwappingConfig.Unload_load_weights:
                with annotate.zone(zone=f"load_residual_weights:model{idx}", log_code=LogCode.PERF_ZONE):
                    self.eps_model[idx].load_residual_weights()
            elif self.model_swap_config == SwappingConfig.Update_weight:
                with annotate.zone(zone=f"swap_weights:model{idx}", log_code=LogCode.PERF_ZONE):
                    self.eps_model[0].swap_weights(request.diffusion_index)

        '''
        Core Loop Execution:
        '''
            core_response = core_loop(
                eps_callable=self.eps_model[idx].get_ait(request.diffusion_index),
                initial_image=initial_image,
                randn_noise=noise_list,
                inputs=inputs,
                avoids=avoids,
                params=core_param,
                binary_mask=b_mask,
                sampler_model_outputs=sampler_model_outputs,
            )



            if self.model_swap_config == SwappingConfig.Unload_load_weights:
                with annotate.zone(
                    zone=f"unload_residual_weights:model{idx}",
                    log_code=LogCode.PERF_ZONE,
                ):
                    self.eps_model[idx].unload_residual_weights()
            if core_response.iterates is None:
                raise ValueError("Core loop failed, no response found.")






        '''
        Output Handling:
        The function checks if the core loop has successfully produced an output image.
        If not, it raises an exception.
        If successful, it logs information about the core loop's completion and returns a DiffusionResponse containing
        the generated images.
        The returned images are either the final iterates or the predicted initial images based
        on the configuration.
        '''
        if core_response is None or core_response.iterates is None:
            raise ValueError("Core loop failed, no response found.")
        logger.info(
            "[DiffusionModelMD] Core loop finished, response size is %s",
            core_response.iterates.shape,
        )
        images = core_response.predicted_x0_image if request.return_predicted_x0_image else core_response.iterates
        if images is None:
            raise ValueError("core_loop did not return an image.")
        return DiffusionResponse(images=Tensor.from_torch(images.cpu()))
```