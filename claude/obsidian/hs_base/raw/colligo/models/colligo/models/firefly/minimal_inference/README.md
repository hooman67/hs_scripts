---
document_type: landing
children:
    - ../text_to_video/aidoc/index.md
    - ../video_to_video/aidoc/index.md
    - ../image_to_video/aidoc/index.md
    - ../ssr/aidoc/index.md
    - ../html_generation/aidoc/index.md
---

# Minimal Inference

## Motivation: Minimal Inference vs. Production Pipeline
Minimal Inference scripts **are designed to increase the productivity of model developers** by using the same component library as the production pipeline, while stripping away unnecessary production-focused complexity. These scripts offer 100% component parity with the production pipeline, providing a simplified, more accessible environment for rapid prototyping.

Key differences between Minimal Inference and the production pipeline:
1. #### Linear Graph Structure
    Minimal Inference operates as a linear (sequential) graph, in contrast to the distributed, non-linear nature of the production pipeline.
    * No need to understand complex Colligo abstractions such as background processing, worker management, or other distributed elements.

2. #### Familiar Data Types
    Minimal Inference leverages common data types like native PyTorch Tensors and PIL images, instead of Colligo-specific classes like           Colligo Tensors or PublicBinary.

3. #### Prototyping Playground
    Minimal Inference serves as a prototyping playground, allowing for **throwaway** code that is specific to a small application. This enables      users to focus solely on the area they are modifying without worrying about how their changes interact with the broader production           pipeline. This also helps keep the production pipeline clean from many experimental if/else statements.
      * For instance, the production pipeline includes elements like NSFW detection, and Dentro processing, which are not         necessary for every task.
      * Please note that everything in the production pipeline is represented in Minimal Inference scripts but not everything that is in Minimal Inference scripts will make it into the production pipeline.
4. #### Task-Specific Scripts
    While we maintain a single production pipeline for Video-to-Video (V2V), Text-to-Video (T2V), and Image-to-Video (I2V), Minimal              Inference offers multiple scripts, each tailored to specific tasks. This specialization further simplifies the prototyping process.

Minimal Inference empowers you to iterate faster, focusing on what matters most for your specific use cases without getting bogged down by the full complexity of the production environment.

---

## Hand off protocol to the [clineto integration group](https://github.com/orgs/Adobe-Firefly/teams/co-colligo-clineto-prod)
To streamline the integration process and ensure clarity, please follow the protocol outlined below when handing off models to the Clineto Integration Group:

1. #### Usage of Minimal Inference is Optional
    It is not mandatory to use the Minimal Inference framework when integrating a model into production. The goal of the Minimal inference is to increase the productivity of model developers by providing a simplified, more accessible environment for rapid prototyping. If you are comfortable with the production pipeline, you can directly integrate your model into the production pipeline.

2. #### Establish Quality and Latency Baselines
    For integration, a baseline for both quality and latency must be established. This baseline should be reflected through a successfully       merged pull request (PR) into the main branch of Colligo.

3. #### PR Options: Production Pipeline or Minimal Inference
    The required PR may be targeted either at the production pipeline or it can be a Minimal Inference script, depending on your needs. If you'd      prefer to bypass production complexities during early integration phases, leveraging Minimal Inference is recommended.

---

## Implementation
1. The implementation of the Minimal Inference Pipeline can be found at contrib/AdobeDiffusion/cliocore/minimal_inference/src/clio/minimal_inference
2. Each minimal inference pipeline (t2v, v2v, i2v) will be a separate standalone script that is runnable without additional dependencies
3. Each minimal inference pipeline script (text_to_video, image_to_video, video_to_video) is accompanied by a corresponding HTML generation script to help generate results faster using minimal inference pipeline
4. Each of the folders in `contrib/AdobeDiffusion/cliocore/minimal_inference/src/clio/minimal_inference` will have a README file with basic instructions launch.json snippets

## Setup (Required, Important, Prerequisite)
To run Minimal Inference Pipeline, you need to do the colligo setup on your instance. Specifically finish the Hardware Setup and Environment Setup steps to ensure that you have an activated dev  environment

Hardware Setup: [https://git.corp.adobe.com/pages/colligo/aidoc/monorepo/hardware-setup.html](https://git.corp.adobe.com/pages/colligo/aidoc/monorepo/hardware-setup.html)
Environment Setup: [https://git.corp.adobe.com/pages/colligo/aidoc/monorepo/env-setup.html](https://git.corp.adobe.com/pages/colligo/aidoc/monorepo/env-setup.html)

- Ensure that `./m sys.check` passes and you are able to load "dev" the environment via `source m`

## Running Minimal Inference (Required, Important)
- Once the setup is completed i.e. `./m sys.check` passes, you've pulled the latest deps via `./m deps.sync` and `source m` works, you can proceed to run Minimal Inference. There are 3 ways to run Minimal Inference 
    - **a.** Run all models locally (all models run on your node) 
    - **b.** Run all models remotely (nothing runs on your node) - THIS IS DEFAULT BEHAVIOUR
    - **c.** Run some models locally, others remotely (load some models locally, call some models remotely)

## Run all models locally
- To run all models locally, run minimal inference with `--native` flag. If you don't provide `--native` all models will be called remotely
- When running with `--native`, the models listed in the function `def set_<task>_registery()` are used. An example for V2V is given below
```
async def set_v2v_registery() -> NativeClient:
    """This function registers the required models for the V2V pipeline
    To ensure parity with the production pipeline, the models below are required to be registered

    Returns:
        NativeClient: A native client with the required models registered
    """
    registery = await NativeClient.create(
        [
            FILIX2_V2V_PROD1_867900_TRT,
            LDM_ENCODER_V4,
            DualVAEModelName.DUAL_VAE_REF_PYTORCH,
            VAE3D_PROD_2,
            VIDEO_REF_SSR,
        ]
    )

    return registery
```

- Make sure your `colligo.dev.yaml` doesn't have a high level section such as `remote_deploy:`. Example below (DON'T HAVE A SECTION LIKE THIS)
```
~~remote_deploy:~~
~~  remote_deploys: [filix2_t2v_prod1_814k32n_trt]~~
~~  endpoint: https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/~~
~~  auth:~~
~~    type: jwt~~
```

## Run all models remotely
- Running all models remotely is default behaviour in minimal inference. Don't use the `--native` CLI arg. Just run it as it is with required arguments
- Pass the endpoint you want to call via the CLI argument `--remote_endpoint` if the default is not ideal for you


## Run some models locally, others remotely
- To run some models locally, and others remotely run minimal inference with the `--native` flag
- Make sure that your `colligo.dev.yaml` has a section like below (don't have the `remote_deploys_per_spec:` section!)
- Within `remote_deploy` within `remote_deploys` provide a list of models that you want to call locally. In the example below `filix2_t2v_prod1_814k32n_trt` will be called remotely and all other models (decoder, text/image/video encoder, T5 etc. will be loaded locally)
```
remote_deploy:
  remote_deploys: [filix2_t2v_prod1_814k32n_trt] # List of models to call remotely, all others will be loaded locally
  endpoint: https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/ # This should be the URL for calling some of the models remotely
  auth:
    type: jwt
```

## [Model Developers] Contributing models to Colligo via Minimal Inference

Follow the recommendations below to contribute your models to the Colligo pipeline via Minimal Inference

*Goal*: As a researcher, we'd like you to give us a working minimal inference script with your custom changes. That's it. Once you have a working minimal inference script with custom code, the integration team will use your changes (from your PR) to integrate models into the production pipeline

*Parity*: Minimal inference is a minimal version of the production pipeline. The results you are able to get using minimal inference will match the results in the production pipeline

### Contribution guidelines
- Minimal Inference has multiple moving parts. In the case of T2V these would be the text encoder, DiT model, decoder
- In the file `text_to_video/minimal_t2v_local.py` we provide a code example of adding a DiT model to minimal inference (while keeping other models unchanged)
    - Notice how only the DiT logic is changed while keeping the decoder unchanged (because the user's goal is to change the DiT model while reusing an existing decoder)
- Before making a PR Ready to Review, please generate HTML files with the files modified and attach them in the Pull Request
- 
 
### Frequently Asked Questions (FAQs)
Q1. I get a `colligo.base.exceptions.ColligoException: Failed to find device with index: 1.` when I try to run Minimal Inference with a `--native` flag. How should I fix it?
A1. This is a known error. Search for the function `get_cfg_device` and replace all occurances of `get_device_with_index(1)` --> `get_device_with_index(0)`. Snippet of the function that will work with `--native` is shown below

```
def get_cfg_device() -> str:
    return get_device_with_index(0) # Changed 1 --> 0
```
