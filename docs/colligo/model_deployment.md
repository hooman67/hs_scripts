```markdown
# Running Tests and Debugging

## Adding Input or Parameter to Debug UI or Using Debug Data

In staging, you can pass whatever parameters you want. [cite: 1] You can access these in the request with `get_request_ctx().debug_data.get("keyName", DefaultValueIfKeyMissing)`[cite: 2].

**Example:** [https://github.com/Adobe-Firefly/colligo/blob/8a3fd08b65ae90444dd4c58f150ac5ce9cf3[…]ls/firefly/clio/call_components/ClioImagingT2ICallComponents.py.](https://github.com/Adobe-Firefly/colligo/blob/8a3fd08b65ae90444dd4c58f150ac5ce9cf3%E2%80%A6ls/firefly/clio/call_components/ClioImagingT2ICallComponents.py.) [cite: 2]

```python
moe_name = T2IMoeName[get_request_ctx().debug_data.get("clio_moe_type", T2IMoeName.MOE_5_40_5_38.value)]
```

You can pass it from the debug UI like this:

```json
{"clio_moe_type" : "MOE_3_27_DMD_5_38"}
```

Just make sure to include:

```yaml
allow_stage_features: true
```

In your `colligo.dev.yaml`.

## Issue with s5cmd

Run: `sudo chmod -R 777 /mnt/localssd`
For more details see: [https://git.corp.adobe.com/pages/colligo/troubleshooting.html](https://git.corp.adobe.com/pages/colligo/troubleshooting.html) [cite: 3]

## "No GPU for CFG Computation" Error During Unit Tests

This is more of a compatibility issue between a10g and a100. [cite: 4] To temporarily fix this (so that the pipeline runs), comment out `"cuda_index += 1"` in `eps_utils.py` when you run on a single a100[cite: 4]. You might also need to relax the memory usage from 23 to 40 in `firefly_v2/diffusion/build.py`[cite: 5, 7]:

```python
gpu=build.gpu_info(memory_gb=40, count=1),
```

## Not Finding Unit Tests

This is probably because of the wrong Python interpreter. [cite: 7] You can verify this by looking at the output of pytest discovery, which will not find pytest[cite: 8]. This is caused by Python being set to `./venv/bin/python`, but yours is not in the project directory (it's in the home folder), so you should set the Python interpreter to: `/home/hshariati/venv/dev/bin/python`[cite: 9].

## Loading Different Models into the Same Unit Test

Say you have a unit test file that needs to load different models for different tests, such as `test_genericDiffusion`[cite: 10]. You can achieve that by these steps:

1. Remove `autouse=True` from load models[cite: 10, 11]:

   **From:**

   ```python
   @pytest.fixture(autouse=True, scope="module")
   def load_kineto_model() -> Iterable[None]:
       # from colligo.base.model_registery import set_model_registery
       # from colligo.sdk.http_client import HttpClient
       # endpoint = "http://localhost:8000"
       # set_model_registery(HttpClient(endpoint))
       with native_deploy_ctx(DIFFUSION_KINETO_T2V):
           yield
   ```

   **To:**

   ```python
   @pytest.fixture(scope="module")
   def load_kineto_model() -> Iterable[None]:
       # from colligo.base.model_registery import set_model_registery
       # from colligo.sdk.http_client import HttpClient
       # endpoint = "http://localhost:8000"
       # set_model_registery(HttpClient(endpoint))
       with native_deploy_ctx(DIFFUSION_KINETO_T2V):
           yield
   ```

   ```python
   @pytest.fixture(scope="module")
   def load_diffusion_model() -> Iterable[None]:
       # from colligo.base.model_registery import set_model_registery
       # from colligo.sdk.http_client import HttpClient
       # endpoint = "http://localhost:8000"
       # set_model_registery(HttpClient(endpoint))
       with native_deploy_ctx(DIFFUSION_MD_L86_L87):
           yield
   ```

2. Have different names for different models (instead of `load_model`, have `load_kineto_model`, `load_diffusion_model`)[cite: 12].
3. Add the model as a parameter to each unit test[cite: 12]:

   ```python
   @pytest.mark.slow  # do not run in CI
   @pytest.mark.asyncio
   @pytest.mark.parametrize("dimension", LATENT_DIMENSIONS)
   async def test_diffusion_component(test_data: Path, dimension: DiffusionDimension, load_diffusion_model: object) -> None:
   ```

**NOTE:** The above is for when you want to have different unit tests in one file where each of them uses different models[cite: 12]. If you pass multiple `load_...` functions to the same unit test, it cannot find any of the models[cite: 13]. If you want one unit test with multiple models, simply pass an array of models to the same `load_models` function like this[cite: 14]:

```python
@pytest.fixture(scope="module")
def load_model_diff() -> Iterable[None]:
    with native_deploy_ctx([DIFFUSION_CLIO3_PROD3_27, LDM_DECODER_V3_128_8X]):
        yield
```

```python
@pytest.mark.slow  # do not run in CI
@pytest.mark.asyncio
async def test_diffusion_component_LP12(test_data: Path, load_model_diff: object) -> None:
```

**NOTE 2:** You need to have the models you're loading locally inside your `colligo.dev.yaml`; otherwise, it will hit the HTTP endpoint[cite: 14]:

```yaml
remote_deploy:
  local_deploys: [clio_imaging, diffusion_prod3_27, ldm_decoder_v3_128_8x]
  remote_deploys: []
  endpoint: [https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net](https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net)
request:
  timeout: 1000000
allow_stage_features: true
```

## How to Decode Image Tensors in Colligo

Encoder and decoder definitions can be found here: `/mnt/localssd/hshariati/colligo/models/colligo/models/firefly/imcoding/decoder_v3/build.py`[cite: 15].

**Unit test with image decode in the end:**

```python
@pytest.fixture(autouse=True, scope="module")
def load_model() -> Iterable[None]:
    with native_deploy_ctx([DIFFUSION_CLIO3_PROD3_27, LDM_DECODER_V3_128_8X]):
        yield


@pytest.mark.slow  # do not run in CI
@pytest.mark.asyncio
async def test_diffusion_component_LP12(test_data: Path) -> None:
    my_output_async = await generic_diffusion._run(input)
    assert my_output_async.images.as_torch().shape == torch.Size([1, 12, height, width])
    ldm_decoder_v3 = LdmDecoderV3("ClioImaging Ldm Decoder V3", LdmDecoderV3Config(cast_to_uint8=True))
    decoder_output = await ldm_decoder_v3.call(
        LdmDecoderV3Input(
            images=my_output_async.images,
        )
    )
    k = to_pil_image(decoder_output.images.as_torch()[0])
    k.save("/mnt/localssd/hshariati/colligo/delete/test.png")
```

You need this in your `colligo.dev.yaml`:

```yaml
remote_deploy:
  local_deploys: [clio_imaging, diffusion_prod3_27, ldm_decoder_v3_128_8x]
  remote_deploys: []
  endpoint: [https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net](https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net)
request:
  timeout: 1000000
allow_stage_features: true
```

## How to Save Decoded Latents as Pill Images

```python
import torch
from PIL import Image
import numpy as np
# Example tensor with shape [1, 3, 129, 480, 640]
video_tensor = torch.randn(1, 3, 129, 480, 640)  # Example tensor
video_tensor = k.clamp(-1, 1)  # Ensure values are in the range [-1, 1]
# Remove the batch dimension
video_tensor = video_tensor.squeeze(0)  # Shape: [3, 129, 480, 640]
# Normalize to [0, 255]
video_tensor = ((video_tensor + 1) * 127.5).clamp(0, 255).byte()  # Shape: [3, 129, 480, 640]
# Iterate over frames and save each frame as a PIL image
for i in range(video_tensor.size(1)):  # Iterate over the frame dimension
    frame = video_tensor[:, i]  # Shape: [3, 480, 640]
    frame_np = frame.permute(1, 2, 0).cpu().numpy()  # Convert to [H, W, C]
    img = Image.fromarray(frame_np, 'RGB')  # Convert to PIL image
    img.save(f'/sensei-fs/users/hshariati/del/clineto/pkls/frame_{i:03d}.png')  # Save frame with zero-padded numbering
```

## Running txt2img and Kineto Together (Hitting Endpoints)

For the Kineto pipeline, we need to load all txt2img models and then the kineto ones. [cite: 17, 18] This doesn't fit on one GPU[cite: 18]. So, we need to use the public endpoint for the txt2img models (and even for kineto)[cite: 19].

**To do this:** [cite: 20]

1. You have to first load the models (remotely) using the **Inference: Road (debug deploy)** (from the left-hand side run and debug panel)[cite: 20].
2. Run your test in a terminal (`python unitest.py`). You can still put breakpoints; just do this before you load all models[cite: 21]. (And you can check the box that says **Raised Exceptions** under the breakpoints tab of the run and debug panel)[cite: 22].
3. You can also go to port 8003 to just reload some of the models[cite: 22].
4. You can also go to port 8000 to send some info (but I didn't get exactly what Shayan said)[cite: 23].

In your test file, you need to comment out[cite: 23]:

```python
# @pytest.fixture(autouse=True, scope="module")
# def load_model() -> Iterable[None]:
#     set_model_registery(HttpClient("http://localhost:8000"))
#     # with native_deploy_ctx(CLIO_KINETO_V2):
#     #     yiel
```

And instead, add `set_model_registery(HttpClient("http://localhost:8000"))` to the beginning of your test[cite: 23]:

```python
@pytest.mark.asyncio
@pytest.mark.slow  # don't run in CI for now.
@pytest.mark.parametrize("prompt_id, batch_size", [(0, 1), (1, 2), (3, 1)])  # (2, 4),
async def test_diffusion(test_data: Path, prompt_id: int, batch_size: int) -> None:
    set_model_registery(HttpClient("http://localhost:8000"))
    # Ensure model is ready!
    request = ClioRequest(
        gi_PROMPT=INPUTS[prompt_id][0],
        gi_SEED=list(range(HASH_START, HASH_START + batch_size)),
        gi_OUTPUT_WIDTH=INPUTS[prompt_id][1],
        gi_OUTPUT_HEIGHT=INPUTS[prompt_id][2],
    )
```

You can put just `clio_v2` in the local deploys, and that will just load a CPU model with the req/res code changes and will hit the remote for the rest[cite: 25]. So your `.env` file will look like this[cite: 26]:

```
COLLIGO_REMOTE_DEPLOYS_ENDPOINT="[https://text2image-dev.ethos851-stage-or2.ethos.adobe.net](https://text2image-dev.ethos851-stage-or2.ethos.adobe.net)"
COLLIGO_LOCAL_DEPLOYS="clio_v2 clio_kineto_v2"
COLLIGO_REMOTE_DEPLOY_AUTH_TOKEN="eyJhbGciOiJSUzI1NiIsIng1dSI6ImltcRce0nLgmsbg"
COLLIGO_REMOTE_DEPLOYS=""
```

To get the `AUTH_TOKEN`, you can put the remote URL in your browser ([https://text2image-dev.ethos851-stage-or2.ethos.adobe.net](https://text2image-dev.ethos851-stage-or2.ethos.adobe.net)), then click on **Access the debug UI**, then click on **fetch IMD credentials**, and then copy **IMS credentials**[cite: 27]. You can then pass this to `COLLIGO_REMOTE_DEPLOY_AUTH_TOKEN` above. Note: these credentials change daily, so you need to update them often[cite: 27].

**Example `.env` file:** [cite: 28]

```
ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A
ARTIFACTORY_UW2_API_KEY=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A
ARTIFACTORY_UW2_USER=hshariati

 #this must be commented out to run test_genericDiffusion for kineto
COLLIGO_REMOTE_DEPLOYS_ENDPOINT="[https://text2image-dev.ethos851-stage-or2.ethos.adobe.net](https://text2image-dev.ethos851-stage-or2.ethos.adobe.net)"
COLLIGO_LOCAL_DEPLOYS="clio_kineto_v2 clio_v2 diffusion_distil_l86_l87 diffusion_kineto_t2v"
COLLIGO_REMOTE_DEPLOY_AUTH_TOKEN="eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktYXQtMS5jZXIiLCJraWQiOiJpbXNfbmExLXN0ZzEta2V5LWF0LTEiLCJpdHQiOiJhdCJ9.eyJpZCI6IjE3MDU5NTQ2OTI5OTZfYjBjMjQ4ZDktNGM3ZC00OTRmLTllZDEtYWViZTYwY2JlZjZiX3VlMSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJjb2xsaWdvX3Rlc3RpbmciLCJ1c2VyX2lkIjoiMDJCQTREQkE2NTMwODFDNDBBNDk0MTNEQGM2MmYyNGNjNWI1YjdlMGUwYTQ5NDAwNCIsInN0YXRlIjoie1wianNsaWJ2ZXJcIjpcInYyLXYwLjQwLjAtMTctZzI0MWZiMDdcIixcIm5vbmNlXCI6XCI0MjAyMzE3MDIwNDM2ODQ0XCJ9IiwiYXMiOiJpbXMtbmExLXN0ZzEiLCJhYV9pZCI6IjAyQkE0REJBNjUzMDgxQzQwQTQ5NDEzREBjNjJmMjRjYzViNWI3ZTBlMGE0OTQwMDQiLCJjdHAiOjAsImZnIjoiWUVMMkRUV0Y3WjY3QTREWjNHWk1BMklBS00iLCJzaWQiOiIxNzA1OTU0NjkyOTkwX2Q2MmQ3ZGU5LWJjMzUtNDgyZS1iMDgzLTg2ZWE1ZmY3MTRmZF91ZTEiLCJtb2kiOiJiYmFhMGI2ZCIsInBiYSI6Ik1lZFNlY05vRVYsTG93U2VjIiwiZXhwaXJlc19pbiI6Ijg2NDAwMDAwIiwiY3JlYXRlZF9hdCI6IjE3MDU5NTQ2OTI5OTYiLCJzY29wZSI6IkFkb2JlSUQsb3BlbmlkLGZpcmVmbHlfYXBpIn0.Elkb-60t7AIhhNmStkixefuHPenA-G3TWh69xviJl_S0Zy0qc-jfcb7tUwc4hkajakwkuLLkvnXSGsCQbasazOgvqT16EihfLijk_yaZrI4xrucWH44X2tLaGoNszHbGcxX99hLWME-rxn6eQb3TjF5TKhEVpURA7xXQhI2F9xik2BCcX2VoE33iadhl7R8xavf3C_99IJncQ-llttxMi9pW0ZXagCTS8RoY0-Zd_oXrehgghTdE34xgds8V_o5Awh6Ux6X_4Tq7RFw0V9P7EiyT7geU9JL9FhLnesRKn-B_Bbf978CsaUxqlW8dTErWWoF-wUr3L4W6v-3_mANHcQ"
COLLIGO_REMOTE_DEPLOYS=""
#need to comment this out to run test_genericDiffusion for kineto
COLLIGO_MODEL_CACHE_DIR="/home/hshariati/hs_colligo_cash_dir"
```

## Specifying Multiple Endpoints and Per Model / Worker Endpoints

```yaml
remote_deploy:
  # only use one.
  local_deploys: [t5_v2, pipeline]
  # remote_deploys: ...
  # if endpoint is set in endpoint_by_deploy we use that, otherwise, we use `endpoint_by_deploy`
  endpoint: [https://clio-imaging-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-imaging-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
  endpoint_by_deploy:
    filix2_t2v_prod1_814k32n_trt: [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
    # ...
```

You can specify either the list of your `local_deploys` (which assumes everything that's missing is remote) or your `remote_deploys` (which will assume everything that's missing is local)[cite: 29]. Now, for looking at remote ones, it first looks at `endpoint_by_deploy`; this is a worker-specific endpoint[cite: 30]. If it doesn't find it there, it will look at the `endpoint` (which is like a global master endpoint)[cite: 31].

**Example:** [cite: 32]

```yaml
remote_deploy_per_spec:
  firefly_clineto:
    local_deploys:
      - clineto_pipeline
      - clineto_proxy_pipeline
      # - adobe_one_image_v2
      # - filix2_t2v_prod1_814k32n
    remote_deploys: []
    # endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/)
    # endpoint: [https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net](https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net)
    endpoint: [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/)
    endpoint_by_deploy:
        adobe_one_image_v2: [https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/](https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/)
deployment_config:
  clineto_pipeline:
    impl_model_config_dict:
      handle_request_timeout: 1000000
      can_disable_nsfw: true

request:
  timeout: 1000000
allow_stage_features: true
s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX6XW442I3D
    secret_access_key: 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

dev_ims_credentials:
  client_id: colligo-developer
  client_code: "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktcGFjLTEuY2VyIiwia2lkIjoiaW1zX25hMS1zdGcxLWtleS1wYWMtMSIsIml0dCI6InBhYyJ9.eyJpZCI6ImNvbGxpZ28tZGV2ZWxvcGVyX3N0ZyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJjbGllbnRfaWQiOiJjb2xsaWdvLWRldmVsb3BlciIsInVzZXJfaWQiOiJjb2xsaWdvLWRldmVsb3BlckBBZG9iZVNlcnZpY2UiLCJhcyI6Imltcy1uYTEtc3RnMSIsIm90byI6ZmFsc2UsInNjb3BlIjoic3lzdGVtIiwiY3JlYXRlZF9hdCI6IjE3MTQxNTUwNzAwNTgifQ.TdhqF-mq2aeLd-qfgzzueT3lOHcZZUyQeCe3351pigRTmh-A2iewczO4hpqZ-y9NOEXHnLfFbQ0VEd-vlCf4lbfADDQTJqRERxeo_N9X7FOBlMNkQRSqe2fCppQsWUsWVm5n6I4rYAZ33EezNE_XiscQKhMlz3nDmVq00vBO5UBB-VDfbAoJZbsUzVbgQE88luAsc_MN0zlvHoI3rW3DfW-QA5oO1AwXp2UslqgJDFMG30ekh7hR0gEDj5GkPndfybVr3BklQ4BAsUvOihDhiC49NmXeyUh397Ttt_h0c-kv8ery3R8ZRuLsIjuoj0gt5eCpjfwJ_0QtFk8pxzkWqA"
  client_secret: s8e--K2qIJVdQkSQE-A_cS_yB78dnxF4IdfV
pluto:
  default_k8s_cluster:
    auth:
      type: kubeconfig
      context: default
      path: ./_build/pluto-dev-cluster/kubeconfig.yaml  # You must set this to your absolute path, relatives will fail.
    cluster_dns: localhost
    persistent_volumes:
    - name: sensei-fs
      mount_path: "/sensei-fs"
      pvc_name: "sensei-fsx-pvc"
```

## Sub Modules Nanotiny Tiny Nano

## Push to Artifactory

To push to Artifactory with the new Colligo (April 25, 2024): Inside your Colligo environment (after running `source m`), run:

```bash
./m deps.upload_artifact <path to file> <a group name>
```

**Example:**

```bash
./m deps.upload_artifact global_step_30000_Gcombined_colligoSlimmed.ckpt diffusion
```

For a folder, you need to zip it like this (starting from the folder that has your sub-folders):

```bash
zip -r /mnt/localssd/hshariati/dit_t2v_seq_ait_engines.zip ./*
./m deps.upload_artifact /mnt/localssd/hshariati/dit_t2v_seq_ait_engines.zip diffusion
```

Rest of the documentation is here: [https://git.corp.adobe.com/pages/colligo/guides/misc/deps.html#binaries](https://git.corp.adobe.com/pages/colligo/guides/misc/deps.html#binaries) [cite: 35]

**Old Notes:**

To push your unit test data to Artifactory:

1. Place the data in the appropriate folder inside `data/test`, such as `/sensei-fs/users/hshariati/colligo/data/test/t5_encoder`[cite: 35, 36].
2. Add or edit the `/sensei-fs/users/hshariati/colligo/tiny/test.t5_encoder.txt` (add one if it doesn’t exist)[cite: 36].
3. Inside, put: `"name of your file" "name of your file"`. **Example:** `"t5_text_embedding_noPad_xxl_the-dog.pkl" "t5_text_embedding_noPad_xxl_the-dog.ebdb96b.pkl"`[cite: 37].
4. Run the command: `nanotiny write`. This command will update the `test.t5_encoder.txt` and add the hash to it[cite: 37]. So it'll become like this[cite: 38]:
   `"t5_text_embedding_noPad_xxl_the-dog.pkl" "t5_text_embedding_noPad_xxl_the-dog.ebdb96b.pkl" ebdb96b654faa68daeb07d2f74ba2f17b2671d54607eed4959daa723502052ce`
   It will also push the file to Artifactory and update the `tiny.yaml` file[cite: 38].
5. Commit/push `test.t5_encoder.txt` to GitHub. You don't need to push the actual file or the `tiny.yaml` to GitHub[cite: 39].
6. You also need to run `nanotiny deploy`[cite: 40].

## Slimming the Weights

To slim the weights, you can use the Colligo script: `/mnt/localssd/hshariati/colligo/pylibs/colligo/dev/scripts/slim_weights.py`.

Or this one: [https://github.com/Adobe-Firefly/colligo/pull/3530/files](https://github.com/Adobe-Firefly/colligo/pull/3530/files).

## Adding Models in `build.py` Local Source `src`

**From Sensei (this will not be deployable):**

```python
CKPT_DIT_V2V_PROD1_1 = build.local_file_source(
    path=Path(
        "/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-28T14-34-13/lightning_logs/version_5/checkpoints/global_step_98000_Gcombined_slimmed.ckpt"
    )
)
```

**From Artifactory:**

```python
CKPT_DIT_V2V_PROD1_1 = build.s3_source(
    bucket="s3://colligo-dev-artifacts/artifacts-v1",
    key="diffusion/may_t2v_dit_mds_phase4_mixed_train-2024-05-25T09-38-06-115k_ema.2024-05-30.15-55.e7716.ckpt",
    version_id="4Bp59RUhvQN8Ly9NNMtCIEbqkxByX2NF",
    sha256="e7716ab09646d4c0b016936b3cb8523d153b08b922b68fdfec9564fdbe5bf38e",
)
```

## Multiple Replicas of a Locally Loaded Model

Say I have a model that I'm loading locally, but I want several replicas of it for faster generation[cite: 41]. I can add this to my `lunch.json` like this[cite: 42]:

```json
{
    "name": "Inference: Rhode Debug Deploy",
    "type": "debugpy",
    "request": "launch",
    "module": "colligo.rhode.commands.dev_supervisor",
    "console": "integratedTerminal",
    "justMyCode": false, // change to false to see everything
    "args": [
        "--spec",
        "${input:deploySpec}",
        "--locust",
        "--replicas", "filix2_t2v_prod1_814k32n", "3"
    ],
    "envFile": "${workspaceFolder}/.env",
},
```

Say this is what my `colligo.dev.yaml` looks like[cite: 44]:

```yaml
remote_deploy_per_spec:
  firefly_clineto:
    local_deploys:
      - clineto_pipeline
      - clineto_proxy_pipeline
      - filix2_t2v_prod1_814k32n
    #  - vae3d_prod_2_pytorch
    remote_deploys: []
    # endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/)
    # endpoint: [https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net](https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net)
    endpoint: [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/)
   #  endpoint_by_deploy:
   #      adobe_one_image_v2: [https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/](https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/)
deployment_config:
  clineto_pipeline:
    impl_model_config_dict:
      handle_request_timeout: 1000000
      can_disable_nsfw: true
```

With the above code, I will get 3 replicas of `filix2_t2v_prod1_814k32n`, named `filix2_t2v_prod1_814k32n_0`, `filix2_t2v_prod1_814k32n_1`, `filix2_t2v_prod1_814k32n_2`[cite: 45]. Without the replicas line, I get only one[cite: 46].

## Concurrency in Pipelines

If you want to increase the number of parallel requests your local machine can handle, do this: Inside this block ([https://github.com/Adobe-Firefly/colligo/blob/9161b8b050c53c51f6774c510768186fcb55f4ca/models/colligo/models/firefly/pipelines/clineto/build.py#L94-L102](https://github.com/Adobe-Firefly/colligo/blob/9161b8b050c53c51f6774c510768186fcb55f4ca/models/colligo/models/firefly/pipelines/clineto/build.py#L94-L102)), add `concurrent_ml_threads=8`, so it becomes:

```python
build.deploy_worker(
    name=CLINETO_PIPELINE,
    deps=list(set(T2V_MODELS + I2V_MODELS + V2V_MODELS)),
    store_credentials=True,
    worker_type="colligo.models.firefly.pipelines.clineto.ClinetoPipeline.ClinetoPipeline",
    request_type=ClinetoRequest,  # type: ignore[arg-type]
    response_type=ClinetoResponse,  # type: ignore[arg-type]
    session_storage_options=build.SessionStorageOptions(ttl_s=86400),
    concurrent_ml_threads=8, # REMOVE THIS BEFORE COMMITTING TO MAIN
)
```