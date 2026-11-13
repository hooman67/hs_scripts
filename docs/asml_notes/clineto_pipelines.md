```markdown
## Debug Parameters

```json
{"disable_sm_input_video_check": true} # this is for structure match to disable fps etc checks
{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false, 'enable_prompt_debiasing': false, 'enable_prompty': false}"

# disable prompt rewrite
config.expansion_threshold = -99
config.enable_prompt_debiasing = false
config.enable_prompty = false
```

## Running Tests Locally

```bash
python -m unittest models.colligo.models.compare.v2.videos.tests.test_generate_compare
python -m unittest models.colligo.models.compare.v2.videos.tests.test_extend_compare
```

## Run Colligo Pipeline Outside VS Code (Screen Session)

```bash
/mnt/localssd/hshariati/colligo/.venvs/dev/bin/python -m colligo.rhode.commands.dev_supervisor --spec firefly_clineto --locust
```

## Poiting firefly stage to different endpoint
1. Use firefly stage: https://firefly-stage.corp.adobe.com
2. In the debug params turn on the flag:
```bash
firefly-ti2v-show-debug-controls
```
3.In the "generation override endpoint" section put the endpoint you wanna hit with the corp in it like this:
```bash
https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/
```




## How to Run DiT

From the main branch of AD:

* `Num_frames = -1` for images
* For videos = 12

You need t5 encoder and LPVAE. Default LPVAE should work (256px output, arbitrary aspect ratio). For video, 256px resolution but 192x320.

**Batch, num_frames, output, height, width:** 1, 24, 4

## Check the Output of `test_diffusion`

**Shape after 3DVAE:** 1, , output, height, width. Also, the range of the number of frames and the range of resolution.

Out of the model, we'll get 15 frames. After 3DVAE, it becomes 51 (divide by 5 times 17).
`1, 51, 3, 8*input (22), 8*(40)`

Should be able to output any multiple of 17 for the number of frames out of 3DVAE.
8\*22, 8\*40 is good for demo. So this is the only resolution right now.

**Input of DiT:**

```json
{
    "width": 40,
    "height": 22,
    "numFrames": 15
}
```

**Output:** Within the VAE component, we need to do the rearrange and de-normalization before giving it to the actual model.

```python
new_images[:, :, 0:5, :, :].shape
# torch.Size([1, 8, 5, 22, 40])

# torch.Size([1, 3, 17, 176, 320])
```

Pair me with a Senior guy in Jakub Plichta.

## `remote_deploy` Configuration

```yaml
remote_deploy:
  local_deploys: [
    clineto_t2v,
    dit_prod1_1,
    adobe_one_text_v2,
    t5_v2,
    prompty_v2,
    prior_t5,
    exif_content_predictor,
    pixel_space_3d_vae,
  ]
  # local_deploys: [clio_imaging, dit_prod1_1]
  # local_deploys: [
  #    clio_imaging,
  #    adobe_one_image_v2,
  #    adobe_one_text_v2,
  #    content_type_classifier,
  #    depth,
  #    diffusion_prod5_38,
  #    diffusion_prod5_40,
  #    exif_content_predictor,
  #    facelab_v2,
  #    ldm_decoder_v3_128_8x,
  #    nsfw_v2,
  #    prior_t5,
  #    prompty_v2,
  #    t5_v2,
  #    upsampler_v2_2x,
  # ]
  remote_deploys: []
  # endpoint: [https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/](https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/)
  endpoint: garbage
request:
  timeout: 10000000
```

## `s3_config` Configuration

```yaml
s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX6XW442I3D
    secret_access_key: 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
```

## `dev_ims_credentials` Configuration

```yaml
dev_ims_credentials:
  api_key: colligo-developer
  client_code: "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktcGFjLTEuY2VyIiwia2lkIjoiaW1zX25hMS1zdGcxLWtleS1wYWMtMSIsIml0dCI6InBhYyJ9.eyJpZCI6ImNvbGxpZ28tZGV2ZWxvcGVyX3N0ZyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJjbGllbnRfaWQiOiJjb2xsaWdvLWRldmVsb3BlciIsInVzZXJfaWQiOiJjb2xsaWdvLWRldmVsb3BlckBBZG9iZVNlcnZpY2UiLCJhcyI6Imltcy1uYTEtc3RnMSIsIm90byI6ZmFsc2UsInNjb3BlIjoic3lzdGVtIiwiY3JlYXRlZF9hdCI6IjE3MTQxNTUwNzAwNTgifQ.TdhqF-mq2aeLd-qfgzzueT3lOHcZZUyQeCe3351pigRTmh-A2iewczO4hpqZ-y9NOEXHnLfFbQ0VEd-vlCf4lbfADDQTJqRERxeo_N9X7FOBlMNkQRSqe2fCppQsWUsWVm5n6I4rYAZ33EezNE_XiscQKhMlz3nDmVq00vBO5UBB-VDfbAoJZbsUzVbgQE88luAsc_MN0zlvHoI3rW3DfW-QA5oO1AwXp2UslqgJDFMG30ekh7hR0gEDj5GkPndfybVr3BklQ4BAsUvOihDhiC49NmXeyUh397Ttt_h0c-kv8ery3R8ZRuLsIjuoj0gt5eCpjfwJ_0QtFk8pxzkWqA"
  client_secret: s8e--K2qIJVdQkSQE-A_cS_yB78dnxF4IdfV
```

## `deployment_config` Configuration

```yaml
deployment_config:
  clio_v2:
    concurrent_ml_tasks:
    colligo_variant:
    model_config_dict_impl:
      checkpoint_cache_bucket:
```

## TODO for Frontend

1.  Send Mp4 not GIF
2.  Change it to actually target v2/video/generate with the frame\_number in request.
3.  Gray out other choices in firefly video and in Aspect ratio (landscape) drop downs
4.  Show only one video (instead of 4)
5.  Make sure you can save the MP4 (with GIF saving would save an image only)

## TODO for Pipeline

1.  Merge the code
2.  Send MP4
3.  Add AIT
4.  ADD SSR
5.  Deploy

## For alse/ssr-new Branch

```bash
pip uninstall mmcv mmcv-full -y; pip install mmcv==2.1.0; pip install mmagic==1.2.0; pip install diffusers==0.21.4
```

## `clineto/clineto-demo` Configuration

```yaml
remote_deploy:
  local_deploys: [
    clineto_t2v,
    dit_prod1_1_ait,
    t5_v2,
    prompty_v2,
    vae3d_prod_1,
    ssr,
  ]
  remote_deploys: []
  # endpoint: [https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/](https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/)
  endpoint: garbage
request:
  timeout: 10000000
allow_stage_features: true
allow_stage_features: true
s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX6XW442I3D
    secret_access_key: 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
dev_ims_credentials:
  api_key: colligo-developer
  client_code: "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktcGFjLTEuY2VyIiwia2lkIjoiaW1zX25hMS1zdGcxLWtleS1wYWMtMSIsIml0dCI6InBhYyJ9.eyJpZCI6ImNvbGxpZ28tZGV2ZWxvcGVyX3N0ZyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJjbGllbnRfaWQiOiJjb2xsaWdvLWRldmVsb3BlciIsInVzZXJfaWQiOiJjb2xsaWdvLWRldmVsb3BlckBBZG9iZVNlcnZpY2UiLCJhcyI6Imltcy1uYTEtc3RnMSIsIm90byI6ZmFsc2UsInNjb3BlIjoic3lzdGVtIiwiY3JlYXRlZF9hdCI6IjE3MTQxNTUwNzAwNTgifQ.TdhqF-mq2aeLd-qfgzzueT3lOHcZZUyQeCe3351pigRTmh-A2iewczO4hpqZ-y9NOEXHnLfFbQ0VEd-vlCf4lbfADDQTJqRERxeo_N9X7FOBlMNkQRSqe2fCppQsWUsWVm5n6I4rYAZ33EezNE_XiscQKhMlz3nDmVq00vBO5UBB-VDfbAoJZbsUzVbgQE88luAsc_MN0zlvHoI3rW3DfW-QA5oO1AwXp2UslqgJDFMG30ekh7hR0gEDj5GkPndfybVr3BklQ4BAsUvOihDhiC49NmXeyUh397Ttt_h0c-kv8ery3R8ZRuLsIjuoj0gt5eCpjfwJ_0QtFk8pxzkWqA"
  client_secret: s8e--K2qIJVdQkSQE-A_cS_yB78dnxF4IdfV
deployment_config:
  clio_v2:
    concurrent_ml_tasks:
    colligo_variant:
    model_config_dict_impl:
      checkpoint_cache_bucket:
```

## Deployment PRs

* For adding the script: [https://git.corp.adobe.com/firefly/colligo-deploy/pull/3993/files](https://git.corp.adobe.com/firefly/colligo-deploy/pull/3993/files)
* For changing timeouts and replicas: [https://git.corp.adobe.com/firefly/colligo-deploy/pull/4015/files](https://git.corp.adobe.com/firefly/colligo-deploy/pull/4015/files)

We used branch: `clineto/clineto-demo`

## ff.com PR

[https://git.corp.adobe.com/neuralfiltersplatform/spl-web-client/pull/7484](https://git.corp.adobe.com/neuralfiltersplatform/spl-web-client/pull/7484)

## To Hit Our Deployed Endpoint

You need this in your `colligo.dev.yaml`:

```yaml
remote_deploy:
  local_deploys: [
    clineto_t2v,
  ]
  remote_deploys: []
  endpoint: [https://clio-video-dev.ethos851-stage-or2.ethos.adobe.net](https://clio-video-dev.ethos851-stage-or2.ethos.adobe.net)
```

For hitting with the script: [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/v2/video/generate](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/v2/video/generate)

## Disabling Prompt Expansion and Debiasing

Works also. Sample request from debug UI:

```json
{ "n": 1, "seeds": [ 1 ], "size": { "width": 40, "height": 22, "numFrames": 15 }, "prompt": "An old lady blowing out the candles on her birthday cake, photorealistic 4K high quality", "negativePrompt": "lowres, bad quality", "locale": "en-US", "enableSsr": false, "promptExpansion": false, "promptDebiasing": false }
```

## `remote_deploy` Configuration (Again)

```yaml
remote_deploy:
  local_deploys: [
    clineto_t2v,
    dit_prod1_1_ait,
    t5_v2,
    prompty_v2,
    vae3d_prod_1,
    ssr,
  ]
  remote_deploys: []
  # endpoint: [https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/](https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/)
  endpoint: garbage
request:
  timeout: 10000000
allow_stage_features: true
```

## `s3_config` Configuration (Again)

```yaml
s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX6XW442I3D
    secret_access_key: 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
```

## `dev_ims_credentials` Configuration (Again)

```yaml
dev_ims_credentials:
  api_key: colligo-developer
  client_code: "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktcGFjLTEuY2VyIiwia2lkIjoiaW1zX25hMS1zdGcxLWtleS1wYWMtMSIsIml0dCI6InBhYyJ9.eyJpZCI6ImNvbGxpZ28tZGV2ZWxvcGVyX3N0ZyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJjbGllbnRfaWQiOiJjb2xsaWdvLWRldmVsb3BlciIsInVzZXJfaWQiOiJjb2xsaWdvLWRldmVsb3BlckBBZG9iZVNlcnZpY2UiLCJhcyI6Imltcy1uYTEtc3RnMSIsIm90byI6ZmFsc2UsInNjb3BlIjoic3lzdGVtIiwiY3JlYXRlZF9hdCI6IjE3MTQxNTUwNzAwNTgifQ.TdhqF-mq2aeLd-qfgzzueT3lOHcZZUyQeCe3351pigRTmh-A2iewczO4hpqZ-y9NOEXHnLfFbQ0VEd-vlCf4lbfADDQTJqRERxeo_N9X7FOBlMNkQRSqe2fCppQsWUsWVm5n6I4rYAZ33EezNE_XiscQKhMlz3nDmVq00vBO5UBB-VDfbAoJZbsUzVbgQE88luAsc_MN0zlvHoI3rW3DfW-QA5oO1AwXp2UslqgJDFMG30ekh7hR0gEDj5GkPndfybVr3BklQ4BAsUvOihDhiC49NmXeyUh397Ttt_h0c-kv8ery3R8ZRuLsIjuoj0gt5eCpjfwJ_0QtFk8pxzkWqA"
  client_secret: s8e--K2qIJVdQkSQE-A_cS_yB78dnxF4IdfV
```

## `deployment_config` Configuration (Again)

```yaml
deployment_config:
  clio_v2:
    concurrent_ml_tasks:
    colligo_variant:
    model_config_dict_impl:
      checkpoint_cache_bucket:
```

## Integration Squad Charter TODOs

1.  GenExten kick off today based on min inference from kevin/Lakshia
2.  Merge to main (pr merged but reverted because of SSR dependencies)
3.  Create ssr component
4.  Write unit-tests for every component. Write unit test for pipeline one: [https://jira.corp.adobe.com/browse/FFM-5993](https://jira.corp.adobe.com/browse/FFM-5993). @siddhantg could you please do this for your SimpleT5, 3dvae (decoder), 3dvae (encoder), and TSR please. I will do it for the DiffusionTransformer. I will also add unit-test for the pipeline under this ticket: [https://jira.corp.adobe.com/browse/FFM-5994](https://jira.corp.adobe.com/browse/FFM-5994)
5.  Code Owners update
6.  SSEval

## Resolution and Aspect Ratio Support

**Input Video:**

* --Mp4
* --Multiple of 12 FPS. Min 12 FPS. (**Model right now is trained on 12fps. We downsample everything to 12 fps.**)
* --Min 17 frames. We only condition on the last 17 frames of the video. Till 3dvae does arbitrary
* -- \~16:9 at some point but for now (40:22) aspect ratio. We will resize however whatever input we get.

**Output Latent:** 1, 15, 8, 22, 40

**Output Video:**

* --12fps before TSR
* --512p after SSR since we can do only 22x40 latent.
* --15 frames only.
* --1920x1056 only

**Why are we limited:**

1.  No watermark for the SSEval.
2.  Extending from End
3.  Aspect ratio and resolution (for now only resize and crop) and multiple of 12fps. Output only 12fps.

## Positive and Negative Condition Tensor

```python
positive_condition_tensors = KinetoConditionTensors(
    text_embedding=positive_text_embeddings.to(eps_device),
    original_video=original_video,
    one_minus_binary_mask=input_video_mask,
    cond_frames=encoded_video.to(eps_device)[:, :1],
)  # TODO do not hard-code this to 1, should be configurable based one model/input
negative_condition_tensors = KinetoConditionTensors(
    text_embedding=negative_text_embeddings.to(eps_device),
    original_video=original_video,
    one_minus_binary_mask=input_video_mask,
    cond_frames=encoded_video.to(eps_device)[:, :1],
)
```

Select the random 5-second segment from the video. But for this month, it's ok if it's just the last 17, but later we want the first 17 as well (next month).

Append the generated part to the generated. But have an overlay on the video showing where it switches. So 7.5-second video (5-second input and 2.5s extended). 5 seconds should be configurable.

**Stretch goal:** Image to video demo (one jpg upload).

## For GenExtend

```yaml
remote_deploy:
  # local_deploys: [
  #    clineto_t2v,
  #    dit_t2v_prod1_1_ait,
  #    t5_v2,
  #    prompty_v2,
  #    vae3d_prod_1,
  #    ssr,
  # ]

  local_deploys: [
    video_gen_extend,
    dit_v2v_prod1_1,
    vae3d_encoder_prod_1,
    vae3d_prod_1,
    ssr,
  ]
  remote_deploys: []
  # endpoint: [https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/](https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net/)
  endpoint: garbage
request:
  timeout: 10000000
allow_stage_features: true
```

```json
{
    "video_in_ref": {
        "presigned_url": "[https://adobe-asml-data.s3.us-east-1.amazonaws.com/test_genA](https://adobe-asml-data.s3.us-east-1.amazonaws.com/test_genA)"
    }
}
```

```json
{
    "video_in_ref": {
        "presigned_url": "[https://pre-signed-firefly-dev.s3-accelerate.amazonaws.com/images/654c1e9a-b3d8-4c2a-b4fc-18481d411bf9?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA4KAGRHX6RBLHYYHK%2F20240613%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240613T024131Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=93842478e782a4632001e914e817fe4ebc64271018b58412d448ba4ac44d687c](https://pre-signed-firefly-dev.s3-accelerate.amazonaws.com/images/654c1e9a-b3d8-4c2a-b4fc-18481d411bf9?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA4KAGRHX6RBLHYYHK%2F20240613%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240613T024131Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=93842478e782a4632001e914e817fe4ebc64271018b58412d448ba4ac44d687c)"
    },
    "height": 22,
    "width": 40,
    "numFrames": 15,
    "modelFps": 12,
    "clipStartSeconds": 0,
    "clipEndSeconds": 5,
    "seeds": [
        0
    ]
}
```

## GenExtend Shapes

We get 61 frames (5 seconds at 12fps). `len(video_torch) = 61`

`video_torch[0].shape. = torch.Size([3, 176, 320])`

We encode the last 17 frames of the provided clip. This will give us 5 latent frames: `encoded_video.latent.as_torch().shape = torch.Size([1, 8, 5, 22, 40])`

`original_video.shape == torch.Size([1, 15, 8, 22, 40])`

The first 5 latent frames are from `encoded_video`, the rest are zeros.
`original_video[0,4,:,:,:].mean() = 0.95`
`original_video[0,5,:,:,:].mean() = 0`

`input_video_mask.shape == torch.Size([1, 15, 1, 22, 40])`

Same with the mask, with the first 5 being 1 and the rest 0.

Then we get the dit output like below:
`dit_output.images.as_torch().shape = torch.Size([1, 15, 8, 22, 40])`
Here, the first 5 are original, and the next 10 are generated.

Then we pass to the decoder and we get:
`vae3d_output.images.as_torch().shape == torch.Size([1, 3, 51, 176, 320])`
Here, the first 17 are original (corresponding to the first 5 latent), and the next 34 are generated (corresponding to the next 10 latents).

## Ref SSR Stuff

`last_frame.as_torch().shape == torch.Size([3, 1056, 1920])`
`original_frames.shape == torch.Size([30, 3, 1056, 1920])`
***But the `last_frame` is normalized to 0-1 vs. the `original_frames` are 0-255.

```
#for 44 by 80 latent.
vae3d_output.images.as_torch().shape == torch.Size([1, 3, 34, 352, 640])

decoded_images.as_torch().shape == torch.Size([1, 34, 3, 1056, 1920])
```

## TODOs (Again)

* Gallery for demo?
* SSR (Diffusion ref based), TSR
* Combined pipeline
* Merge to main
* AIT for the large model
* Large model needs new 3dvae

## Finalize the Combined API (for all 3 modes)

Discuss plan for combined front end: Yeojin kim, Lee Brimlow, attending meetings, etc.

Finish the backend implementation of the finalized API. Default certain parameters. Update the wiki, provide sample curl command, add more info on params: [https://jira.corp.adobe.com/browse/FFM-6345](https://jira.corp.adobe.com/browse/FFM-6345)

Add / verify the I2V workflow: [https://jira.corp.adobe.com/browse/FFM-6344](https://jira.corp.adobe.com/browse/FFM-6344)

Try out the new 9B parameter model in Colligo: [https://jira.corp.adobe.com/browse/FFM-6343](https://jira.corp.adobe.com/browse/FFM-6343). Test out the new large ckpt. How do we run this for short-term?

Add brightness/contrast post-processing to gen extend ((Jui-hsien Wang) Ray.): [https://jira.corp.adobe.com/browse/FFM-6342](https://jira.corp.adobe.com/browse/FFM-6342)

`model_fps` and `n_channels` will come from model config: [https://jira.corp.adobe.com/browse/FFM-6358](https://jira.corp.adobe.com/browse/FFM-6358)

Calculate latent dims from pixel dims: [https://jira.corp.adobe.com/browse/FFM-6359](https://jira.corp.adobe.com/browse/FFM-6359)

Add pipeline configs: [https://jira.corp.adobe.com/browse/FFM-6360](https://jira.corp.adobe.com/browse/FFM-6360)

Inject debug parameters: [https://jira.corp.adobe.com/browse/FFM-6361](https://jira.corp.adobe.com/browse/FFM-6361)

3dvae failing to decode 512p. David to look into + Sid from our side: [https://jira.corp.adobe.com/browse/FFM-6373](https://jira.corp.adobe.com/browse/FFM-6373)

Test out the AOT conversion: [https://jira.corp.adobe.com/browse/FFM-6374](https://jira.corp.adobe.com/browse/FFM-6374)

Get from Lakshya the before-after fine-tuning comparison. Soheil wants to know the improvement we get from fine-tuning.

## Experiments to Try

* Filix 2.0, Mori, Torch 2.3.0
* AOT conversions: Can they give us AOT for Filix or for the Dual VAE? Did we try the 3dvae with AOT that they gave us?
* Dual VAE: Aditya

***We are passing 0s for t5 embeddings; we need to change this to NULL embeddings.

```python
NUM_LATENTS_FOR_VIDEO_XATT_COND = 1  # number of latents for video conditions
```

The `cond_frames` when you decode is hardcoded as 5. I parameterized it, but that broke things. We need to parameterize it again. `Cond_frames` should be renamed to `cond_xattn_latents`.

```python
return FrameConds(
    original_frames=Tensor.from_torch(original_frames),
    initial_images=Tensor.from_torch(initial_images),
    input_video_mask=Tensor.from_torch(input_video_mask),
    cond_frames_encoded=Tensor.from_torch(cond_frames_encoded[:,:1]),
    cond_latenets_encoded=Tensor.from_torch(cond_frames_encoded),
    ref_frame_ssr=Tensor.from_torch(last_frame),
)
```

And then we can get the shape from this: `cond_latenets_encoded`.

```bash
python /mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/train_pytorch/dit_train/src/dit_train/app/sample_ediffi.py
```

Worked with myenv.

```python
def slimmer(in_path, out_path):
    ckpt = torch.load(in_path)
    slimmed = ckpt["model.denoiser.ema"]
    keys = list(slimmed.keys())
    for k in keys:
        if "teacher." in k:
            del slimmed[k]
    torch.save({"model.denoiser": slimmed}, out_path)
```

***LIOR wants us to push Theodore so he tests the AOT and he gives us AOT for Filix2.
***TSR is ready to be integrated. Talk with Saeed.

Take minimal and integrate it into the combined pipeline to get a t2v demo out using our core loop. Get a first round of benchmarking mem/timing, test on 40gb, H100. Test deployability.

**Bringing in new filix2 based core loop.
Combined pipeline finalization
TSR integration

Texture flickering issue.

Aug 5 and 10, distillation will start. So expect Aug 15/20th for the first checkpoint for low resolution. Extra two weeks for sharding and high resolution. End of Aug, we can start proper distillation (more like 10-step diffusion though), and we'll also look at quantization.

Let me know if there are more obstacles, or if 2.3/2.4 creates problems. Canvas.

```
dit_output_images
# [TorchTensor: torch.Size([1, 40, 12, 24, 40]), torch.float32, cuda:0]
```

```python
dimension=DiffusionTransformerDimension(
    width=40,
    height=24,
    num_frames=40,
    n_channels=12,
),
```

Re-use hyper parameters between research and production. Non-inline call to models; have their portion outside.

**Lior Shapira:** Thanks for removing SSR. It might be useful if it's not hard to always return both the original and the SSR'd version in that window, so people can see and download both.

**Hooman Shariati:** I'll look into that.

**Lior Shapira:** I want someone to focus on the actual inference algorithm, the sampling and noise schedule. It's fine to get parity at first, but we're not going to do 40 diffusion steps.

**Hooman Shariati:** Sid would be the best person for that once we have the parity work (need him till then). As long as he wants to work on it, that is, but I leave that part to you. If you want me to free him up before parity work, I can do that as well. Just let me know.

**Lior Shapira:** I want to also work with Sid from Oliver's team on this.

**Hooman Shariati:** Yep. We have a very good relationship with him too. As long as he's available, that won't be a problem. Do you want me to set up a meeting with the two Sids?

**Lior Shapira:** Yes, but I'm out next week starting Tuesday afternoon.

**GT from Jianming:** [http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/kduarte/temp/mori_gen3_outputs/filix2-5b-256p-prod-0716-128n-run13/filix2-5b-256p-prod-0716-128n-run13_ckpt_step00637500.pth_size-40x24x40_steps-50_cfg-7.5_eta-1.0_negstyle-custom_ness-none_matchenergy-True_ema-True_cfgcutofft-20_frames-40/gen3/07-22-2024_13-22-47/gen3.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/kduarte/temp/mori_gen3_outputs/filix2-5b-256p-prod-0716-128n-run13/filix2-5b-256p-prod-0716-128n-run13_ckpt_step00637500.pth_size-40x24x40_steps-50_cfg-7.5_eta-1.0_negstyle-custom_ness-none_matchenergy-True_ema-True_cfgcutofft-20_frames-40/gen3/07-22-2024_13-22-47/gen3.html)

**Generated by us:** [http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/650k/650k.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/650k/650k.html)

**GT combined:** [http://clio.corp.adobe.com/files/merged_content_2024-07-27-22-32-45-de3d3157a57e299344fe6c23cc31df1e82c1727d9f5769069ee3f94ecc91cfa0_md5_ee5906247be861205b0cec6d5dc93e05.html](http://clio.corp.adobe.com/files/merged_content_2024-07-27-22-32-45-de3d3157a57e299344fe6c23cc31df1e82c1727d9f5769069ee3f94ecc91cfa0_md5_ee5906247be861205b0cec6d5dc93e05.html)

**Blined combined:** [http://clio.corp.adobe.com/files/merged_content_2024-07-27-22-26-12-435d984af99240e5f8119396ce071ad4e70002247b3f868f9a4cdae6a758df23_md5_67ea1ea4b1aaaec88f3dc6132b3f144e.html](http://clio.corp.adobe.com/files/merged_content_2024-07-27-22-26-12-435d984af99240e5f8119396ce071ad4e70002247b3f868f9a4cdae6a758df23_md5_67ea1ea4b1aaaec88f3dc6132b3f144e.html)

Lak to provide 07/31.

Aditya is gonna work on min pipeline and then with Sid on sampling. Tripti needs to integrate Saeds today. Aditya gonna finish with DualVaed (also encoder).

Xiajen help Tripti and also support Aditya and implement final API. We also need to return both with and without SSR.

Abhinev: Try torch 2.3.0, and with Arpit help with the diffusion loop and deployment.

Need to run some experiments for Lior. Different envs for eval. Estimate for our benchmarks.

```python
ALLOWED_PIXEL_WIDTH_HEIGHT = [
    (1536, 1536), #square_high
    (768, 768), #square_low
    (1920, 1056), #wide_high
    (960, 528), #wide_low
]
```

```json
{
    "seeds": [
        333
    ],
    "size": {
        "width": 960,
        "height": 528,
        "numFrames": 40
    },
    "prompt": "Close-up of an Asian man with a hopeful expression. He's wearing a knit navy sweater and leaning forward slightly. His eyes are wide and focused, giving a sense of urgency or excitement. Soft glowing light illuminates his face, highlighting his features and the texture of his skin. The mood is hopeful, as if he's in the middle of an exciting conversation or reacting to something surprising",
    "negativePrompt": "cartoon, vector art, & bad aesthetics & poor aesthetic",
    "locale": "en-US"
}
```

**Average decode single-run time:** 3553 ms
**Average SSR single-run time:** 144356 ms
**Average dit single-run time:** 68292.390625ms

```json
{
    "seeds": [
        333
    ],
    "size": {
        "width": 1920,
        "height": 1056,
        "numFrames": 40
    },
    "prompt": "Close-up of an Asian man with a hopeful expression. He's wearing a knit navy sweater and leaning forward slightly. His eyes are wide and focused, giving a sense of urgency or excitement. Soft glowing light illuminates his face, highlighting his features and the texture of his skin. The mood is hopeful, as if he's in the middle of an exciting conversation or reacting to something surprising",
    "negativePrompt": "cartoon, vector art, & bad aesthetics & poor aesthetic",
    "locale": "en-US"
}
```

**Average decode single-run time:** 13113.4833984375ms
**Average SSR single-run time:** 44976.7578125ms

**For 20 latents 1080p:**
**Average decode single-run time:** 6582.36474609375ms
**Average SSR single-run time:** 21031.607421875ms

**For 20 560p:**
**Average decode single-run time:** 1725.6319580078125ms
**Average SSR single-run time:** 5430.49072265625ms

**(640, 352), 17 frames**
**Average encode single-run time:** 1661 ms

**1090p**

**40 frames:**
Decode\_output\_width=320, Decode\_output\_heigth=176
Average decode single-run time: 3553 ms

SSR\_output\_width=960, SSR\_output\_height=528
Average SSR single-run time: 144356 ms

Encode\_input\_width=320, Encode\_input\_heigth=176
Average encode single-run time: 304 ms

Decode\_output\_width=640, Decode\_output\_heigth=352
Average decode single-run time: 13113 ms

SSR\_output\_width=1920, SSR\_output\_height=1056
Average SSR single-run time: 44976 ms

Encode\_input\_width=640, Encode\_input\_heigth=352
Average encode single-run time: 1663 ms

Encode\_input\_width=1920, Encode\_input\_heigth=1056
OEM

**20 frames:**
Decode\_output\_width=320, Decode\_output\_heigth=176
Average decode single-run time: 1726 ms

SSR\_output\_width=960, SSR\_output\_height=528
Average SSR single-run time: 5430 ms

Encode\_input\_width=320, Encode\_input\_heigth=176
Average encode single-run time: 304 ms

Decode\_output\_width=640, Decode\_output\_heigth=352
Average decode single-run time: 6582 ms

SSR\_output\_width=1920, SSR\_output\_height=1056
Average SSR single-run time: 21032 ms

Encode\_input\_width=640, Encode\_input\_heigth=352
Average encode single-run time: 1661 ms

Encode\_output\_width=1920, Encode\_output\_heigth=1056
OEM

## Slack Links

* July 29th T2V Filix2: [https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1717189789812699?thread_ts=1717188482.059799&cid=C04N4KPJ5PS](https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1717189789812699?thread_ts=1717188482.059799&cid=C04N4KPJ5PS)
* Jun 27th GenExtend: [https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1719537527232009](https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1719537527232009)
* May 31st: [https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1717188482059799](https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1717188482059799)
* May 31st (Thread): [https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1717189789812699?thread_ts=1717188482.059799&cid=C04N4KPJ5PS](https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1717189789812699?thread_ts=1717188482.059799&cid=C04N4KPJ5PS)
* May 7th: [https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1717188482059799](https://adoberesearch.slack.com/archives/C04N4KPJ5PS/p1717188482059799)

## Example Prompts

* tiktok dancer, but it's a cephalapod space alien dancing like a tiktok dancer, they are dancing in a cyberpunk living room, trending viral internet video
* A high-fidelity video with a dynamic camera following the iconic Wall Street Charging Bull statue. The bronze bull, suddenly imbued with life, snorts and charges down the bustling streets of lower Manhattan. Focus on capturing the energy and chaos of the scene, with a sense of awe at the sight of this monumental creature come alive. --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics
* --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics
* a little bird made of a fresh orange bursts out of a whole orange, photo-realistic techniques --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics
* Macro cinematography, close-up shot, Drops of ink swirl and disperse in clear water, forming the word â€œFILIX2â€ in the fluid patterns. Camera captures the mesmerizing, dynamic motion and the rich, dark ink. Cinematic. dynamic motion --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics
* Two viking warriors fighting with heavy swords on a ship in flames sailing in a storm. --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics
* A person sitting on a bed looking at a spectacular night sky full of galaxies and stars, view from behind, fisheye perspective, vibrant blue and purple colors, dreamlike and magical atmosphere, high resolution, intricate details in the clouds and galaxies, lighting dramatic --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics
* Astronaut woman drinking coffee. The helmet is open and she has red hair. She is smiling. --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics
* Astronaut on a camel --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics
* \[255/1755] Photo of an athlete cat explaining it's latest scandal at a press conference to journalists. --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics
* A happy elephant wearing a birthday hat walking under the sea. --neg\_prompt: cartoon, ugly & bad aesthetics & poor aesthetics

```python
ALLOWED_PIXEL_WIDTH_HEIGHT = [
    (1536, 1536), #square_high
    (768, 768), #square_low
    (1920, 1056), #wide_high
    (960, 528), #wide_low
]
```

* --Get baseline from Lakshya for GenExtend
* --What are encoder/decoder changes? Where to get changes?
* --Feel out the Canvas
* --Make sure we extend the last 5 seconds instead of the first.
* --SSR
* --Build

## Clineto V2V Filix 2 (Aug 2 2024)

```python
resize_and_center_crop(img, width, height)
# Width: 320, height: 176

# len(i2v_frames)
# 381
# i2v_frames[0].size
# (320, 176)

# i2v_frames[-max_frames:]  # take last max_frames (50)

# min_frames: int = 16,

# insuff_frames = i2v_frames is not None and len(i2v_frames) < min_frames

# i2v_frames.shape
# torch.Size([50, 3, 176, 320])

# After squeeze :
# i2v_frames.shape
# torch.Size([1, 50, 3, 176, 320])
```

**From Pipeline:**

```python
# n_chunks = 1

# z_lpvae.shape
# torch.Size([1, 1, 12, 22, 40])

# z_3dvae.shape
# torch.Size([1, 12, 4, 22, 40])

# type(im_lis[0])
# <class 'numpy.ndarray'>

# im_lis[0].shape
# (176, 320, 3)

# im_lis[0].mean()
# 82.33821022727273

# im_lis[0].std()
# 62.3254707725821

# im_lis[0].min()
# 0

# im_lis[0].max()
# 255

# We produce 48 generated frames. And use 16 original frames.
# So with original frames output is 64 frames.
# Frames are: (320, 176)

# decoded_frames.as_torch().shape
# torch.Size([1, 3, 68, 352, 640])

# decoded_frames.as_torch().min()
# tensor(0, dtype=torch.uint8)

# decoded_frames.as_torch().max()
# tensor(255, dtype=torch.uint8)

# Lskdjflsdkjf

# imgs_tensor.as_torch().shape
# torch.Size([53, 3, 176, 320])

# imgs_tensor.as_torch()[0, ].shape
# torch.Size([3, 176, 320])

# imgs_tensor.as_torch()[0, ].mean()
# tensor(0.4449)

# imgs_tensor.as_torch()[0, ].std()
# tensor(0.2384)

# imgs_tensor.as_torch()[0, ].min()
# tensor(0.)

# imgs_tensor.as_torch()[0, ].max()
# tensor(1.)

# keyframe_tensor.as_torch().shape
# torch.Size([3, 352, 640])

# keyframe_tensor.as_torch().min()
# tensor(0.)

# keyframe_tensor.as_torch().max()
# tensor(1.)

# normalized_orig_frames.shape
# torch.Size([1, 3, 48, 176, 320])

# decoded_frames.as_torch().shape
# torch.Size([1, 3, 64, 176, 320])
```

Decoder input 5 ref latent frames and 5 non-ref latent frames (total 10). Output is 16 pixel frames.

**Match energy:** Fix confetti by applying match energy properly: [https://adoberesearch.slack.com/archives/C078QQWP1LG/p1726090359131409](https://adoberesearch.slack.com/archives/C078QQWP1LG/p1726090359131409)

Write the unit test. Do 50% of the time.

Gen3 with everything off, Gen3 with everything on, Gen3 with newest ckpt.

## `remote_deploy_per_spec` Configuration

```yaml
remote_deploy_per_spec:
  firefly_clineto:
    local_deploys:
      - clineto_pipeline
      - clineto_proxy_pipeline
      - filix2_t2v_prod1_814k32n_trt
    remote_deploys: []
    endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/)
deployment_config:
  clineto_pipeline:
    impl_model_config_dict:
      handle_request_timeout: 1000000
      can_disable_nsfw: true
allow_stage_features: true
request:
  timeout: 1000000
# There are various way to give colligo configs for s3.
# Our canonical way is via this dev config file, via the s3_config section.
# When you run the command `./m sys.setup` the setup script will fill up
# the default values from vault.
s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX6XW442I3D
    secret_access_key: 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

# For some developer workflows like calling to remote endpoints, you need an IMS config.
# This will be fetched from vault automatically and added to this file when your run
# `./m sys.setup`.
dev_ims_credentials:
  client_id: colligo-developer
  client_code: "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktcGFjLTEuY2VyIiwia2lkIjoiaW1zX25hMS1zdGcxLWtleS1wYWMtMSIsIml0dCI6InBhYyJ9.eyJpZCI6ImNvbGxpZ28tZGV2ZWxvcGVyX3N0ZyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJjbGllbnRfaWQiOiJjb2xsaWdvLWRldmVsb3BlciIsInVzZXJfaWQiOiJjb2xsaWdvLWRldmVsb3BlckBBZG9iZVNlcnZpY2UiLCJhcyI6Imltcy1uYTEtc3RnMSIsIm90byI6ZmFsc2UsInNjb3BlIjoic3lzdGVtIiwiY3JlYXRlZF9hdCI6IjE3MTQxNTUwNzAwNTgifQ.TdhqF-mq2aeLd-qfgzzueT3lOHcZZUyQeCe3351pigRTmh-A2iewczO4hpqZ-y9NOEXHnLfFbQ0VEd-vlCf4lbfADDQTJqRERxeo_N9X7FOBlMNkQRSqe2fCppQsWUsWVm5n6I4rYAZ33EezNE_XiscQKhMlz3nDmVq00vBO5UBB-VDfbAoJZbsUzVbgQE88luAsc_MN0zlvHoI3rW3DfW-QA5oO1AwXp2UslqgJDFMG30ekh7hR0gEDj5GkPndfybVr3BklQ4BAsUvOihDhiC49NmXeyUh397Ttt_h0c-kv8ery3R8ZRuLsIjuoj0gt5eCpjfwJ_0QtFk8pxzkWqA"
  client_secret: s8e--K2qIJVdQkSQE-A_cS_yB78dnxF4IdfV
```

## `pluto` Configuration

```yaml
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

## Endpoint URL Conversion

To go from endpoint URL to what you can put in your `colligo.dev.yaml`, you need to remove the `colligov2` and the `corp`.

**Example:**

* DEV - clio-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/) becomes [https://clio-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-dev.ethos851-stage-or2.ethos.adobe.net/)
* STAGE - clio-video [https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/) becomes [https://clio-video-stage.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-stage.ethos851-stage-or2.ethos.adobe.net/)
* Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/) becomes [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/)

Note that we have changed `clio-video` to `gen-video`. So you actually should use these:

* Debug UI for dev: [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
* Colligo YAML endpoint: `https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/`

## Ideas for Integration Squad Charter

1.  Inference Quality

## `remote_deploy_per_spec` Configuration (Again)

```yaml
remote_deploy_per_spec:
  firefly_clineto:
    local_deploys:
      - clineto_pipeline
      - clineto_proxy_pipeline
    remote_deploys: []
    endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/)
    # endpoint: [https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/)
    # endpoint: [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/)
deployment_config:
  clineto_pipeline:
    impl_model_config_dict:
      handle_request_timeout: 1000000
      can_disable_nsfw: true
```

## New Pipeline Plan with Kevin Refactor

* `get_image_and_metadata()` -> image in torch (just process the input)
* `get_video_and_metadata()` -> video in torch (just process the input)
* `run_nsfw()`
* `process_input_image_for_vae()`
* `process_input_video_for_vae()`
* `get_image_embeddings()`
* `get_video_embeddings()`
* `image_and_video_2_dit_input()`
* FFP-23567t2v-baseline\_t2v-regression-bitesized\_1730949214

## Gen Extend Baseline

* Input video: [https://adobe.enterprise.slack.com/files/U0405P7JEG0/F07FJN8PK53/6\_original\_clip.mp4](https://adobe.enterprise.slack.com/files/U0405P7JEG0/F07FJN8PK53/6_original_clip.mp4)
* Output video on Aug 5th: [https://adobe.enterprise.slack.com/files/U061QL49WVB/F07G0B6MERX/8441a5eb-02bc-44d4-b23f-9155652aa567.mp4](https://adobe.enterprise.slack.com/files/U061QL49WVB/F07G0B6MERX/8441a5eb-02bc-44d4-b23f-9155652aa567.mp4)
* Proper Stitch on Aug 6th: [https://adobe.enterprise.slack.com/files/U061QL49WVB/F07G7E622QZ/hs\_sseval\_stitch\_nossr.mp4](https://adobe.enterprise.slack.com/files/U061QL49WVB/F07G7E622QZ/hs_sseval_stitch_nossr.mp4)

## Enabling Different Decoders

`{"decoder_model_name":"ref_decoder_v2"}`

[https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/debug/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/debug/) to enable ref-decoder.

Just search for `decoder_model_name` in the pipeline. This comes from the config files: `/mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/configs/runtime_configs/generate_t2v.yaml`.

But you can hardcode it too. The accepted values are in enum:

```python
class VAE3DDecoderName(Enum):
    VAE3D_PROD_2 = VAE3D_PROD_2
    VAE3D_PROD_2_PYTORCH = VAE3D_PROD_2_PYTORCH
    VAE3D_CVAE = VAE3D_CVAE
    REF_DECODER_V2 = REF_DECODER_V2
```

1.  **V2V:**
    1.  OFF by default
    2.  `{"decoder_model_name": "vae3d_prod_2"}` to turn it on
2.  **T2V/I2V:**
    1.  on by default
    2.  `{"decoder_model_name": "vae3d_prod_2_pytorch"}` to turn it off

Changing resolutions: put half of the final resolution you want to see in the config: `/mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/configs/runtime_configs/generate_t2v.yaml`.

```yaml
widescreen_360p:
  pixel_width: 320
  pixel_height: 180
  latent_width: 40
  latent_height: 22
  dit_model_name: filix2_t2v_prod1_814k32n
  decoder_model_name: vae3d_prod_2_pytorch
```

So above will give me a 640x360 after the SSR (since SSR is 2x).

But then, in your debug UI size parameter, you need to send double what you put in the config. This is because they first divide what you provide in the request by `SSR_size_ratio` (which is 2) and then see if it matches the allowed sizes (from the config). So in the request, you put 640, 360, while in config, you whitelist half of that.

## For Minimal Inference (Mix and Match Local vs Remote)

1.  Still use `--native`
2.  Don't use `remote_deploy_per_spec`; use only `remote_deploy`
3.  Put what you want to run locally in `local_deploys`; everything else will be remote.
4.  Or put what you want to run remotely in `remote_deploys`; everything else will be local.
5.  If you have nothing in your `dev.yaml`, or if you only have `remote_deploy_per_spec`, `--native` will run everything locally.

```yaml
remote_deploy:
  local_deploys:
    - filix2_t2v_prod1_540p
  remote_deploys: []
  # endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/)
  # endpoint: [https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/)
  endpoint: [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/)
deployment_config:
clineto_pipeline:
  impl_model_config_dict:
    handle_request_timeout: 1000000
    can_disable_nsfw: true

allow_stage_features: true
request:
  timeout: 1000000
# There are various way to give colligo configs for s3.
# Our canonical way is via this dev config file, via the s3_config section.
# When you run the command `./m sys.setup` the setup script will fill up
# the default values from vault.
s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX6XW442I3D
    secret_access_key: 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


# For some developer workflows like calling to remote endpoints, you need an IMS config.
# This will be fetched from vault automatically and added to this file when your run
# `./m sys.setup`.
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

Previous production release (before 11/19/2024) was done from this branch: [https://github.com/Adobe-Firefly/colligo/tree/release/firefly\_clineto/main.8147](https://github.com/Adobe-Firefly/colligo/tree/release/firefly_clineto/main.8147)

```
video_conds.ref_decoder_frames
# [TorchTensor: torch.Size([1, 1088, 1920, 3]), torch.float32, cpu]
```

Where Kevin said to change: `/mnt/localssd/hshariati/colligo/models/colligo/models/firefly/diffusion/clineto/eps/eps_utils.py`, Line 228.

```python
dit = DiT(DiT.Config(**params)).to(eps_device).to(precision)
```

```
dit_output_images.shape
# torch.Size([1, 41, 12, 68, 120])

# dit_output_images.mean()
# tensor(-0.2637, dtype=torch.bfloat16)

# dit_output_images.std()
# tensor(0.7461, dtype=torch.bfloat16)

# From pipeline:
# dit_output_images.as_torch().mean()
# tensor(-0.3027, dtype=torch.bfloat16)

# dit_output_images.as_torch().std()
# tensor(0.8633, dtype=torch.bfloat16)
```

Code for consolidating and slimming checkpoints: [https://github.com/Adobe-Firefly/colligo/blob/main/contrib/Mori/mori/training/utils/consolidate\_dcp\_ckpt.py](https://github.com/Adobe-Firefly/colligo/blob/main/contrib/Mori/mori/training/utils/consolidate_dcp_ckpt.py)

Works for Guided transform.

Since Mori moved out of colligo, you should use this instead:
```python
mkdir /mnt/localssd/ckpt-in;mkdir /mnt/localssd/ckpt-out; cd ckpt-in;
aws s3 cp --recursive ckpt_s3_path /mnt/localssh/ckpt-in
```

**Make sure you're in your colligo directory
```python
python /home/colligo/colligo/models/colligo/models/common/asml_generation_utils/viq_scripts/consolidate_ckpt.py --ckpt-dir /mnt/localssd/ckpt-in --output-dir /mnt/localssd/ckpt-out --slim --upload_artifactory
```

```yaml
remote_deploy:
  local_deploys:
    - clineto_pipeline
    - clineto_proxy_pipeline
    # - filix2_t2v_prod1_540p
    - filix2_t2v_prod1_540p_winattn_trt
    # - ref_decoder_v2
    # - t5_v2_256
  remote_deploys: []
  endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/)
  # endpoint: [https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/)
  # endpoint: [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/)
deployment_config:
clineto_pipeline:
  impl_model_config_dict:
    handle_request_timeout: 1000000
    can_disable_nsfw: true

allow_stage_features: true
request:
  timeout: 1000000
# There are various way to give colligo configs for s3.
# Our canonical way is via this dev config file, via the s3_config section.
# When you run the command `./m sys.setup` the setup script will fill up
# the default values from vault.
s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX6XW442I3D
    secret_access_key: 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


# For some developer workflows like calling to remote endpoints, you need an IMS config.
# This will be fetched from vault automatically and added to this file when your run
# `./m sys.setup`.
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

* Windowed attention enabled
* Fa3 optimization enabled
* Current end-to-end running time 118
* Diffusion SSR disabled

## Combining CSVs

```bash
python models/colligo/models/common/asml_generation_utils/viq_scripts/combine_csvs.py --input_csvs "/sensei-fs/users/sannavajjala/dump/i2v-gt-prompt-athareja-mrizve-prompt1/reencoded.csv,/sensei-fs/users/sannavajjala/dump/i2v-gt-prompt-athareja-mrizve-prompt2/reencoded.csv,/sensei-fs/users/sannavajjala/dump/i2v-gt-prompt-athareja-mrizve-prompt3/reencoded.csv,/sensei-fs/users/sannavajjala/dump/i2v-gt-prompt-athareja-mrizve-prompt4/reencoded.csv" --save_to /sensei-fs/users/sannavajjala/dump/i2v-gt-default-atharejadata-mrizveprompt/ --caption_column "caption" --input_image_columns "image1,image2" --input_video_column "https_video0_ssr" --output_video_columns "prompt1, prompt2, prompt3, prompt4"
```

## Reencode the Videos

```bash
python models/colligo/models/common/asml_generation_utils/viq_scripts/reencode_videos.py \
    --input_csv "<path-to-csv>" \
    --save_to "<save-to>" \
    --crf <crf-value> \
    --caption_column "caption" \
    --image_columns "image0,image1" \
    --video_columns "sensei_video0_ssr,sensei_video0_nossr"
```

## Debug Params for 1.8

If you wanna put this in colligo debug UI you cannot have any spaces and any single quotes.

```
--debug_params "{'enable_prompty': false, 'enable_dentro_pre': false, 'enable_dentro_post': false, 'disable_nsfw': true}" \
```

## GenExtend Dimensions for v1.8 (4k GenExten 02/12/25)

Final output: 3840x2160
Latent dims: `[1 5 64 120 68]` (5 frames for 1st chunk, 4 for the other 3 chunks = 4 chunks = 17 frames) `[B F C W H]`
Num pixel frames would be: 17 \* 4 - 3 = 65
Input to the encoder should be: `[1, 17, 3, 120*8, 68*8]` which is `[1, 17, 3, 960, 544]` (`B F C H W`). This gives 1920x1080 frame which gets doubled by SSR.

## Uploading to SSEval Credentials (Key from Tian)

```python
s3_handle = S3Handle(
    aws_access_key_id="AKIASQRK44BROXTITHNO",
    aws_secret_access_key="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",
    aws_session_token=None,
    unsigned=False,
)
```

Above works for upload to eval hub. For colligo2html use:

```bash
export AWS_ACCESS_KEY_ID=AKIASQRK44BROXTITHNO
export AWS_SECRET_ACCESS_KEY=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
aws s3 ls s3://clio-web-app/evaluation_service/eval_sets/i2v_animal_human_confusion_harm/data/part1/AdobeStock_583412451.jpeg
```

## `remote_deploy` Configuration (Siddhant)

```yaml
remote_deploy:
  local_deploys:
  - clineto_pipeline
  - clineto_proxy_pipeline
  - dual_vae_rgba_pytorch
  - filix2_t2rgba_prod1_8_540p_1
  - t5_v2_512_torch
    # - filix2_t2v_prod1_8_540p_1
    # - dual_vae_pytorch
  remote_deploys: []
  # endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/)
  endpoint: [https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/)
  # endpoint: [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/)
deployment_config:
clineto_pipeline:
  impl_model_config_dict:
    handle_request_timeout: 1000000
    can_disable_nsfw: true
allow_stage_features: true
request:
  timeout: 1000000
# There are various way to give colligo configs for s3.
# Our canonical way is via this dev config file, via the s3_config section.
# When you run the command `./m sys.setup` the setup script will fill up
# the default values from vault.
s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX664EHFPPY
    secret_access_key: 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

# For some developer workflows like calling to remote endpoints, you need an IMS config.
# This will be fetched from vault automatically and added to this file when your run
# `./m sys.setup`.
dev_ims_credentials:
  client_id: colligo-developer
  client_code: "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktcGFjLTEuY2VyIiwia2lkIjoiaW1zX25hMS1zdGcxLWtleS1wYWMtMSIsIml0dCI6InBhYyJ9.eyJpZCI6ImNvbGxpZ28tZGV2ZWxvcGVyX3N0ZyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJjbGllbnRfaWQiOiJjb2xsaWdvLWRldmVsb3BlciIsInVzZXJfaWQiOiJjb2xsaWdvLWRldmVsb3BlckBBZG9iZVNlcnZpY2UiLCJhcyI6Imltcy1uYTEtc3RnMSIsIm90byI6ZmFsc2UsInNjb3BlIjoic3lzdGVtIiwiY3JlYXRlZF9hdCI6IjE3MTQxNTUwNzAwNTgifQ.TdhqF-mq2aeLd-qfgzzueT3lOHcZZUyQeCe3351pigRTmh-A2iewczO4hpqZ-y9NOEXHnLfFbQ0VEd-vlCf4lbfADDQTJqRERxeo_N9X7FOBlMNkQRSqe2fCppQsWUsWVm5n6I4rYAZ33EezNE_XiscQKhMlz3nDmVq00vBO5UBB-VDfbAoJZbsUzVbgQE88luAsc_MN0zlvHoI3rW3DfW-QA5oO1AwXp2UslqgJDFMG30ekh7hR0gEDj5GkPndfybVr3BklQ4BAsUvOihDhiC49NmXeyUh397Ttt_h0c-kv8ery3R8ZRuLsIjuoj0gt5eCpjfwJ_0QtFk8pxzkWqA"
  client_secret: s8e--K2qIJVdQkSQE-A_cS_yB78dnxF4IdfV
```

## `pluto` Configuration (Siddhant)

```yaml
pluto:
  default_k8s_cluster:
    auth:
      type: kubeconfig
      context: default
      path: ./_build/pluto-dev-cluster/kubeconfig.yaml  # You must set this to your absolute path, relatives will fail.
    cluster_dns: localhost
    persistent_volumes:
    - name: logging-fs
      mount_path: "/logging-fs"
      pvc_name: "logging-fsx-pvc"
    - name: sensei-fs
      mount_path: "/sensei-fs"
      pvc_name: "sensei-fsx-pvc"
  # This will be fetched from vault automatically and added to this file when your run
  # `./m sys.setup`.
  azure_config:
    cluster_manager_client_credentials:
      client_id: f0cdd3df-e4ec-43bd-bcee-1d6bf4c5a307
      client_secret: b9r8Q~ByWRmfvraBc._ZPUcb3bkoadF3zvMbscaX
    cluster_manager_job_handler_client_credentials:
      client_id: b0165790-b495-4fb6-b99d-781d84e47e5f
      client_secret: Kur8Q~LNDoq.S31gaZ9~IOlahSyImTTgGI1XnbVl
    cluster_manager_node_handler_client_credentials:
      client_id: cfbbabd1-161d-4c1c-8da8-c7e99f1373e1
      client_secret: l8i8Q~CsPzPCJmb_j6w5W7Rks0M36uoMtChuKbxx
    scheduler_client_credentials:
      client_id: 5cb7e53f-6897-4d31-b9a7-1baa03a3595a
      client_secret: BlC8Q~JcvYfWEiYTPwpfr5inr8Efz-EMZI.TPbmg
    job_run_manager_system_client_credentials:
      client_id: 9e0f79c0-4b1a-4852-8db6-7c9a83525652
      client_secret: JZ-8Q~oWeYfMvBMKAkxlodcEEkVE2Tkl6poLfb7-
    e2e_tests_client_credentials:
      client_id: 48807df1-9aec-42d5-a36f-61fece78e8c7
      client_secret: WPT8Q~QxXtYuyY6HNQPCMHYdIbfY-XJ5~galbare
    node_manager_client_credentials:
      client_id: 48ad772c-fa91-4b99-b720-947711f4c2c6
      client_secret: wX28Q~Gx8MRfZNSQq9-2xs2M6vv3l-TBGaAVFbw6
    service_healthworker_credentials:
      client_id: f95f1ef0-0ca7-46be-822a-9158a16e3170
      client_secret: dSh8Q~lAJoxgqDVK.noMWzDJ9enDFgY-7eBEtcXp
    reclaim_service_client_credentials:
      client_id: 028bd917-83c1-4e47-b4a1-455539495563
      client_secret: WGC8Q~k-dWFshX7eyWJBgsOByF5f_bZLuyt1zaTL
    user_notifications_service_client_credentials:
      client_id: c82862ed-f227-4cbf-a648-8bd5b3e1b5f5
      client_secret: 52Y8Q~3ku0uPEEKmS_HWOPiaHkBrUjAVn5eH_cQR
    pluto_ecs_client_credentials:
      client_id: a0d7cbf1-7dff-47aa-ba3d-e75c506eadab
      client_secret: bw08Q~H9mNgJXmLHfwDZwt3KyYnu6OQOAom2GbHs
  token_service_config:
    private_key: "-----BEGIN PRIVATE KEY-----\n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\n
    so/WhTB6YvFNrSq1istpLLvGIPk9DSQ=\n-----END PRIVATE KEY-----"
    allowed_public_keys:
      [https://ai-dev.corp.adobe.com/public-keys/pluto-dev.pub](https://ai-dev.corp.adobe.com/public-keys/pluto-dev.pub): "-----BEGIN PUBLIC\n
        KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAy/Zp+3MBxrUf7UHXszCh\n
        BMrwahYpfuXcBygwoQZUpSTvMYJ6Z0cabMZATHNw0oF2rwGfSFQm2L6zXRLhEjso\nRjKa/Gv8fEm4pEXBWUrbxiUsX1diHW/MBank6AGGB6WN9RkJP9tMuLtF/qWEJkbl\n
        Fm+EN+HgVnCoHldxaaLrJ1hXBkms26L+vX/mJSMbX2ID1j96db/t3n7CCUOlZ58G\nOtoneZG0KPazfrOqhEjG6siL7y91BY77BXvA/eVCpf6BwLqW96DOkU+LDMnPY3YX\n
        qf42z1a1ClpJlt6K1ITdJCkeVAOPhw9x1bJSvHGYcoYBnSAvP+cFBkcDCF4e6Fod\nWfawqgYX7TOUEpiI0SZ2G8zv7lY4ZWI4qHyKgRUNlfpohkeWkaG3u74jdnLogWmi\n
        CknWlxSEJo/+zvEZEfdNPcohA98LDTb9RVc8oksI2B5OrksarbBDZrVpHDaB+e4x\ntGTvpB4CdK2fxwsRVt7VQZSD+98UvuiTDMlrUW+9p0Skak/FANdASYi/P7w9fLpL\n
        CajNlVftoA4gGdUXmTn21Ifol+hT8PI49Iwhvcg6N9mR28IyfreQiBIKvVA4G+J8\nbit3xslOC5P+w3TUVVE5kI3e+fYEBXowmF/IescjSAkW0tRIyg2B8xfWuhE3w79a\n
        ExrdUlm0xJ1/UoHggXtnee0CAwEAAQ==\n-----END PUBLIC KEY-----"
```

## `remote_deploy` Configuration (Hooman's Upgraded Tokens)

```yaml
remote_deploy:
  local_deploys:
    - clineto_pipeline
    - clineto_proxy_pipeline
    - filix2_t2v_prod1_8_540p_1
    - t5_v2_512_torch
    # - dual_vae_pytorch
  remote_deploys: []
  # endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/)
  endpoint: [https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/)
  # endpoint: [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/)
deployment_config:
clineto_pipeline:
  impl_model_config_dict:
    handle_request_timeout: 1000000
    can_disable_nsfw: true
allow_stage_features: true
enable_model_warmup: false
request:
  timeout: 1000000

s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX664EHFPPY
    secret_access_key: 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
dev_ims_credentials:
  client_id: colligo-developer
  client_code: "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktcGFjLTEuY2VyIiwia2lkIjoiaW1zX25hMS1zdGcxLWtleS1wYWMtMSIsIml0dCI6InBhYyJ9.eyJpZCI6ImNvbGxpZ28tZGV2ZWxvcGVyX3N0ZyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJjbGllbnRfaWQiOiJjb2xsaWdvLWRldmVsb3BlciIsInVzZXJfaWQiOiJjb2xsaWdvLWRldmVsb3BlckBBZG9iZVNlcnZpY2UiLCJhcyI6Imltcy1uYTEtc3RnMSIsIm90byI6ZmFsc2UsInNjb3BlIjoic3lzdGVtIiwiY3JlYXRlZF9hdCI6IjE3MTQxNTUwNzAwNTgifQ.TdhqF-mq2aeLd-qfgzzueT3lOHcZZUyQeCe3351pigRTmh-A2iewczO4hpqZ-y9NOEXHnLfFbQ0VEd-vlCf4lbfADDQTJqRERxeo_N9X7FOBlMNkQRSqe2fCppQsWUsWVm5n6I4rYAZ33EezNE_XiscQKhMlz3nDmVq00vBO5UBB-VDfbAoJZbsUzVbgQE88luAsc_MN0zlvHoI3rW3DfW-QA5oO1AwXp2UslqgJDFMG30ekh7hR0gEDj5GkPndfybVr3BklQ4BAsUvOihDhiC49NmXeyUh397Ttt_h0c-kv8ery3R8ZRuLsIjuoj0gt5eCpjfwJ_0QtFk8pxzkWqA"
  client_secret: s8e--K2qIJVdQkSQE-A_cS_yB78dnxF4IdfV
```

## `pluto` Configuration (Hooman's Upgraded Tokens)

```yaml
pluto:
  default_k8s_cluster:
    auth:
      type: kubeconfig
      context: default
      path: ./_build/pluto-dev-cluster/kubeconfig.yaml  # You must set this to your absolute path, relatives will fail.
    cluster_dns: localhost
    persistent_volumes:
    - name: logging-fs
      mount_path: "/logging-fs"
      pvc_name: "logging-fsx-pvc"
    - name: sensei-fs
      mount_path: "/sensei-fs"
      pvc_name: "sensei-fsx-pvc"
  # This will be fetched from vault automatically and added to this file when your run
  # `./m sys.setup`.
  azure_config:
    cluster_manager_client_credentials:
      client_id: f0cdd3df-e4ec-43bd-bcee-1d6bf4c5a307
      client_secret: b9r8Q~ByWRmfvraBc._ZPUcb3bkoadF3zvMbscaX
    cluster_manager_job_handler_client_credentials:
      client_id: b0165790-b495-4fb6-b99d-781d84e47e5f
      client_secret: Kur8Q~LNDoq.S31gaZ9~IOlahSyImTTgGI1XnbVl
    cluster_manager_node_handler_client_credentials:
      client_id: cfbbabd1-161d-4c1c-8da8-c7e99f1373e1
      client_secret: l8i8Q~CsPzPCJmb_j6w5W7Rks0M36uoMtChuKbxx
    scheduler_client_credentials:
      client_id: 5cb7e53f-6897-4d31-b9a7-1baa03a3595a
      client_secret: BlC8Q~JcvYfWEiYTPwpfr5inr8Efz-EMZI.TPbmg
    job_run_manager_system_client_credentials:
      client_id: 9e0f79c0-4b1a-4852-8db6-7c9a83525652
      client_secret: JZ-8Q~oWeYfMvBMKAkxlodcEEkVE2Tkl6poLfb7-
    e2e_tests_client_credentials:
      client_id: 48807df1-9aec-42d5-a36f-61fece78e8c7
      client_secret: WPT8Q~QxXtYuyY6HNQPCMHYdIbfY-XJ5~galbare
    node_manager_client_credentials:
      client_id: 48ad772c-fa91-4b99-b720-947711f4c2c6
      client_secret: wX28Q~Gx8MRfZNSQq9-2xs2M6vv3l-TBGaAVFbw6
    service_healthworker_credentials:
      client_id: f95f1ef0-0ca7-46be-822a-9158a16e3170
      client_secret: dSh8Q~lAJoxgqDVK.noMWzDJ9enDFgY-7eBEtcXp
    reclaim_service_client_credentials:
      client_id: 028bd917-83c1-4e47-b4a1-455539495563
      client_secret: WGC8Q~k-dWFshX7eyWJBgsOByF5f_bZLuyt1zaTL
    user_notifications_service_client_credentials:
      client_id: c82862ed-f227-4cbf-a648-8bd5b3e1b5f5
      client_secret: 52Y8Q~3ku0uPEEKmS_HWOPiaHkBrUjAVn5eH_cQR
    pluto_ecs_client_credentials:
      client_id: a0d7cbf1-7dff-47aa-ba3d-e75c506eadab
      client_secret: bw08Q~H9mNgJXmLHfwDZwt3KyYnu6OQOAom2GbHs
  token_service_config:
    private_key: "-----BEGIN PRIVATE KEY-----\n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\n
    so/WhTB6YvFNrSq1istpLLvGIPk9DSQ=\n-----END PRIVATE KEY-----"
    allowed_public_keys:
      [https://ai-dev.corp.adobe.com/public-keys/pluto-dev.pub](https://ai-dev.corp.adobe.com/public-keys/pluto-dev.pub): "-----BEGIN PUBLIC\n
        KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAy/Zp+3MBxrUf7UHXszCh\n
        BMrwahYpfuXcBygwoQZUpSTvMYJ6Z0cabMZATHNw0oF2rwGfSFQm2L6zXRLhEjso\nRjKa/Gv8fEm4pEXBWUrbxiUsX1diHW/MBank6AGGB6WN9RkJP9tMuLtF/qWEJkbl\n
        Fm+EN+HgVnCoHldxaaLrJ1hXBkms26L+vX/mJSMbX2ID1j96db/t3n7CCUOlZ58G\nOtoneZG0KPazfrOqhEjG6siL7y91BY77BXvA/eVCpf6BwLqW96DOkU+LDMnPY3YX\n
        qf42z1a1ClpJlt6K1ITdJCkeVAOPhw9x1bJSvHGYcoYBnSAvP+cFBkcDCF4e6Fod\nWfawqgYX7TOUEpiI0SZ2G8zv7lY4ZWI4qHyKgRUNlfpohkeWkaG3u74jdnLogWmi\n
        CknWlxSEJo/+zvEZEfdNPcohA98LDTb9RVc8oksI2B5OrksarbBDZrVpHDaB+e4x\ntGTvpB4CdK2fxwsRVt7VQZSD+98UvuiTDMlrUW+9p0Skak/FANdASYi/P7w9fLpL\n
        CajNlVftoA4gGdUXmTn21Ifol+hT8PI49Iwhvcg6N9mR28IyfreQiBIKvVA4G+J8\nbit3xslOC5P+w3TUVVE5kI3e+fYEBXowmF/IescjSAkW0tRIyg2B8xfWuhE3w79a\n
        ExrdUlm0xJ1/UoHggXtnee0CAwEAAQ==\n-----END PUBLIC KEY-----"
```

## `remote_deploy` Configuration (Again, with Upgraded Tokens)

```yaml
remote_deploy:
  local_deploys:
    - clineto_pipeline
    - clineto_proxy_pipeline
    - filix2_t2v_prod1_8_540p_1
    - t5_v2_512_torch
    # - dual_vae_pytorch
  remote_deploys: []
  # endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/)
  endpoint: [https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/)
  # endpoint: [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/)
deployment_config:
clineto_pipeline:
  impl_model_config_dict:
    handle_request_timeout: 1000000
    can_disable_nsfw: true
allow_stage_features: true
enable_model_warmup: false
request:
  timeout: 1000000

s3_config:
  default_profile:
    access_key_id: AKIA4KAGRHX664EHFPPY
    secret_access_key: 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
dev_ims_credentials:
  client_id: colligo-developer
  client_code: "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktcGFjLTEuY2VyIiwia2lkIjoiaW1zX25hMS1zdGcxLWtleS1wYWMtMSIsIml0dCI6InBhYyJ9.eyJpZCI6ImNvbGxpZ28tZGV2ZWxvcGVyX3N0ZyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJjbGllbnRfaWQiOiJjb2xsaWdvLWRldmVsb3BlciIsInVzZXJfaWQiOiJjb2xsaWdvLWRldmVsb3BlckBBZG9iZVNlcnZpY2UiLCJhcyI6Imltcy1uYTEtc3RnMSIsIm90byI6ZmFsc2UsInNjb3BlIjoic3y



"
# Sample request for strcuture match transform video debug ui
{
    "seeds": [
        333
    ],
    "sizes": [
        {
            "width": 1920,
            "height": 1080,
            "numFrames": 121
        }
    ],
    "prompt": "a man walking in a a desert",
    "negativePrompt": "cartoon, vector art, & bad aesthetics & poor aesthetic",
    "controlData": {
        "structureData": {
            "referenceVideo": {
                "source": {
                    "id": "ae55adb5-67c6-445d-af89-953d4c5f98e6"
                }
            },
            "edgeStrength": 0.5,
            "depthStrength": 0.5
        }
    },
    "locale": "en-US",
    "output": {
        "storeInputs": false
    }
}
```

## to disable the fps check
{"disable_sm_input_video_check": true}

## Learning the diffusion loop diffusion_loop

### Starting with I2V
This is the file that's actually called:
https://github.com/Adobe-Firefly/colligo/blob/20e04f0134e3eaa0ac9f38efe07055791ad6744c/contrib/Mori/collections/genai_foundation/src/genai_foundation/networks/clineto_v1_filix2_rope.py#L888

This is the scheduler:
https://github.com/Adobe-Firefly/colligo/blob/20e04f0134e3eaa0ac9f38efe07055791ad6744c/models/colligo/models/common/diffusion/schedulers/instaflow_scheduler.py#L171

print(scheduler.timesteps)
[999, 992, 985, 978, 971, 963, 955, 947, 939, 930, 921, 912, 903, 893, 883, 862, 802, 775, 697, 660, 554, 502, 347, 272, 29]

print(latents.shape)
torch.Size([1, 36, 64, 46, 46])

print(cond_latents.shape)
torch.Size([1, 1, 64, 46, 46])

video_conds[0].cond_latents.as_torch().shape
torch.Size([1, 1, 64, 46, 46])

timestep_scale
1000.0



When you call the model.

cond_latent_inds
[0]
avoid_cond_latent_inds
[0]
generated_frames
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

pos_t.shape
torch.Size([1, 36])

print(pos_t[0])
tensor([  0, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999,
        999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999,
        999, 999, 999, 999, 999, 999, 999, 999], device='cuda:0')

print(neg_t[0])
tensor([  0, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999,
        999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999,
        999, 999, 999, 999, 999, 999, 999, 999], device='cuda:0')


### First noise schedule implementaiton:
pos_t
tensor([[  0, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999,
         999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999,
         999, 999, 999, 999, 999, 999, 999, 999]], device='cuda:0')

CORE:   4%|▍         | 1/25 [00:25<10:20, 25.87s/it]
pos_t
tensor([[  0, 992, 992, 992, 992, 992, 992,  10, 992, 992, 992, 992, 992, 992,
          20, 992, 992, 992, 992, 992, 992,  30, 992, 992, 992, 992, 992, 992,
          40, 992, 992, 992, 992, 992, 992,  50]], device='cuda:0')

CORE:  8%|█        | 3/25 [00:50<03:50, 10.99s/it]
pos_t
tensor([[  0, 978, 978, 978, 978, 978, 978,  30, 978, 978, 978, 978, 978, 978,
          60, 978, 978, 978, 978, 978, 978,  90, 978, 978, 978, 978, 978, 978,
         120, 978, 978, 978, 978, 978, 978, 150]], device='cuda:0')

CORE:  16%|█▌        | 4/25 [00:50<03:50, 10.99s/it]
pos_t
tensor([[  0, 971, 971, 971, 971, 971, 971,  40, 971, 971, 971, 971, 971, 971,
          80, 971, 971, 971, 971, 971, 971, 120, 971, 971, 971, 971, 971, 971,
         160, 971, 971, 971, 971, 971, 971, 200]], device='cuda:0')

CORE:  20%|██        | 5/25 [01:03<03:56, 11.82s/it]
pos_t
tensor([[  0, 963, 963, 963, 963, 963, 963,  50, 963, 963, 963, 963, 963, 963,
         100, 963, 963, 963, 963, 963, 963, 150, 963, 963, 963, 963, 963, 963,
         200, 963, 963, 963, 963, 963, 963, 250]], device='cuda:0')

CORE:  24%|██▍       | 6/25 [01:17<03:56, 12.43s/it]
pos_t
tensor([[  0, 955, 955, 955, 955, 955, 955,  60, 955, 955, 955, 955, 955, 955,
         120, 955, 955, 955, 955, 955, 955, 180, 955, 955, 955, 955, 955, 955,
         240, 955, 955, 955, 955, 955, 955, 300]], device='cuda:0')

CORE:  28%|██▊       | 7/25 [01:33<04:02, 13.48s/it]
pos_t
tensor([[  0, 947, 947, 947, 947, 947, 947,  70, 947, 947, 947, 947, 947, 947,
         140, 947, 947, 947, 947, 947, 947, 210, 947, 947, 947, 947, 947, 947,
         280, 947, 947, 947, 947, 947, 947, 350]], device='cuda:0')

CORE:  32%|███▏      | 8/25 [01:39<03:08, 11.09s/it]
pos_t
tensor([[  0, 939, 939, 939, 939, 939, 939,  80, 939, 939, 939, 939, 939, 939,
         160, 939, 939, 939, 939, 939, 939, 240, 939, 939, 939, 939, 939, 939,
         320, 939, 939, 939, 939, 939, 939, 400]], device='cuda:0')

CORE:  36%|███▌      | 9/25 [01:45<02:32,  9.52s/it]
pos_t
tensor([[  0, 930, 930, 930, 930, 930, 930,  90, 930, 930, 930, 930, 930, 930,
         180, 930, 930, 930, 930, 930, 930, 270, 930, 930, 930, 930, 930, 930,
         360, 930, 930, 930, 930, 930, 930, 450]], device='cuda:0')


CORE:  40%|████      | 10/25 [01:50<02:01,  8.10s/it]
pos_t
tensor([[  0, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921,
         921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921,
         921, 921, 921, 921, 921, 921, 921, 921]], device='cuda:0')

CORE:  44%|████▍     | 11/25 [01:59<02:00,  8.59s/it]
pos_t
tensor([[  0, 912, 912, 912, 912, 912, 912, 912, 912, 912, 912, 912, 912, 912,
         912, 912, 912, 912, 912, 912, 912, 912, 912, 912, 912, 912, 912, 912,
         912, 912, 912, 912, 912, 912, 912, 912]], device='cuda:0')


### Reverse noise schedule 
tensor([[  0, 963, 963, 963, 963, 963, 963, 245, 963, 963, 963, 963, 963, 963,
         255, 963, 963, 963, 963, 963, 963, 265, 963, 963, 963, 963, 963, 963,
         275, 963, 963, 963, 963, 963, 963, 285]], device='cuda:0')

CORE:  24%|██▍       | 6/25 [00:57<02:22,  7.48s/it]
pos_t
tensor([[  0, 955, 955, 955, 955, 955, 955, 200, 955, 955, 955, 955, 955, 955,
         210, 955, 955, 955, 955, 955, 955, 220, 955, 955, 955, 955, 955, 955,
         230, 955, 955, 955, 955, 955, 955, 240]], device='cuda:0')

CORE:  28%|██▊       | 7/25 [01:31<04:51, 16.17s/it]
pos_t
tensor([[  0, 947, 947, 947, 947, 947, 947, 155, 947, 947, 947, 947, 947, 947,
         165, 947, 947, 947, 947, 947, 947, 175, 947, 947, 947, 947, 947, 947,
         185, 947, 947, 947, 947, 947, 947, 195]], device='cuda:0')

CORE:  32%|███▏      | 8/25 [01:36<03:32, 12.47s/it]
pos_t
tensor([[  0, 939, 939, 939, 939, 939, 939, 110, 939, 939, 939, 939, 939, 939,
         120, 939, 939, 939, 939, 939, 939, 130, 939, 939, 939, 939, 939, 939,
         140, 939, 939, 939, 939, 939, 939, 150]], device='cuda:0')

CORE:  36%|███▌      | 9/25 [01:41<02:40, 10.05s/it]
pos_t
tensor([[  0, 930, 930, 930, 930, 930, 930,  65, 930, 930, 930, 930, 930, 930,
          75, 930, 930, 930, 930, 930, 930,  85, 930, 930, 930, 930, 930, 930,
          95, 930, 930, 930, 930, 930, 930, 105]], device='cuda:0')

CORE:  40%|████      | 10/25 [01:48<02:19,  9.32s/it]
pos_t
tensor([[  0, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921,
         921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921, 921,
         921, 921, 921, 921, 921, 921, 921, 921]], device='cuda:0')

#### Asking GPT:
We call the diffusion_loop function in our text to video and image to video applications. These models are based on DiT, and rectified flow models. I am trying to understand the innter workings of the diffusion_loop better. Apparently, there is a part where we start from a noise (so step 999), we send the noise to the model and get X0 (what the model thinks was the denoised frames), we then add back some noise to this prediction (maybe using a function called step?) and go to the next diffusion step (i.e. repeat the same cycle again). Show me where this happens in the code. And explain the innter workings of this code to me.   

#### Answer:
Looking at the `diffusion_loop` function, I can see the iterative denoising process you're describing. Here's the core part where it happens:

```python
# Run denoising loop.
for i, t in enumerate(timesteps):
    # Various preprocessing steps...

    # Get model prediction with classifier-free guidance
    pred = forward_with_cfg(
        denoiser=denoiser,
        pos_x=pos_latents,
        neg_x=neg_latents,
        pos_t=pos_t,
        neg_t=neg_t,
        # Other parameters...
    )
    
    # Update latents for next step
    latents = scheduler.step(pred, t, latents, eta=eta, generator=generator).prev_sample
```

This is how the process works:

1. We start with pure noise latents (line 41: `latents: torch.Tensor` with shape (b, f, c, h, w))

2. For each timestep `t` in the diffusion schedule (from high noise to low):
   - The model receives the current noisy latents and predicts the noise component
   - `forward_with_cfg` handles classifier-free guidance by combining conditional and unconditional predictions
   - `scheduler.step()` takes this prediction and computes the next, less noisy version of the latent
   - The `.prev_sample` from the scheduler becomes our new latent for the next iteration

3. The `forward_with_cfg` function (line 346-417):
   - Gets both conditional prediction (using your text/image embeddings) and unconditional prediction
   - Combines them using the formula: `pred_cfg = pred_uncond + cfg_scale * (pred_cond - pred_uncond)`
   - This guides the generation toward your conditioning while maintaining sample quality

The scheduler controls how noise is added back during each step, implementing the specific diffusion or flow approach being used. The `eta` parameter controls the amount of noise added at each step.


#### Question
You mentioned that:
The scheduler.step method is implementing the DDIM or similar sampling procedure. It takes the model's prediction of what the clean image should be, then adds back a controlled amount of noise (determined by eta parameter) to reach the next timestep.
When eta=0, it's deterministic sampling. When eta=1.0 (as in your default), it adds stochasticity to the process.

Teach me more about the step function and what it does. The algorithm it uses is instaflow I have attached the step function. I want to know where exactly the noise gets added, does it get added to the first frame that is the condition too or not? (this is an image to video application). Also, what is this noise that we add back? is it just noise (i.e random numbers from normal distribution) or does it have other charactersitics. 

Basically, teach me both how the step function works and what it does and also what the algorithm it's impelmenting does. 

#### Answer

Let me explain the `step` function in the InstaFlow scheduler in depth.

Read file: models/colligo/models/common/diffusion/schedulers/instaflow_scheduler.py
Based on a close analysis of the code, let me explain the InstaFlow scheduler's `step` function:

### What the step function does

The `step` function is responsible for advancing from the current timestep to the previous timestep (going from noisier to cleaner) in the diffusion process. Here's the key logic:

```171:199:models/colligo/models/common/diffusion/schedulers/instaflow_scheduler.py
        prev_timestep = self.timesteps_prev[timestep]

        alpha_prod_t = self.alphas_cumprod[timestep]
        alpha_prod_t_prev = self.alphas_cumprod[prev_timestep] if prev_timestep >= 0 else self.final_alpha_cumprod

        pred_original_sample = (
            sample + (1.0 - alpha_prod_t).sqrt() / ((1.0 - alpha_prod_t).sqrt() + alpha_prod_t.sqrt()) * model_output
        )

        variance = self._get_variance(timestep, prev_timestep)
        c1 = eta * (variance**0.5)
        c2 = torch.max(((1 - alpha_prod_t_prev) - c1**2), torch.scalar_tensor(0.0, dtype=c1.dtype)).sqrt()
        c3 = alpha_prod_t_prev.sqrt() - c2 * (alpha_prod_t / (1 - alpha_prod_t)).sqrt()
        c4 = c2 / (1 - alpha_prod_t).sqrt()

        noise = torch.empty_like(sample).normal_(generator=generator)
        prev_sample = (
            c3 * pred_original_sample + c1 * noise + c4 * sample * (alpha_prod_t.sqrt() + (1.0 - alpha_prod_t).sqrt())
        )
        prev_sample = prev_sample / (alpha_prod_t_prev.sqrt() + (1 - alpha_prod_t_prev).sqrt())
```

### Where and how noise gets added

The key line where noise is generated and added is:

```186:190:models/colligo/models/common/diffusion/schedulers/instaflow_scheduler.py
        noise = torch.empty_like(sample).normal_(generator=generator)
        prev_sample = (
            c3 * pred_original_sample + c1 * noise + c4 * sample * (alpha_prod_t.sqrt() + (1.0 - alpha_prod_t).sqrt())
        )
```

1. The noise is freshly generated each step with `torch.empty_like(sample).normal_(generator=generator)`
2. It's standard Gaussian noise (normal distribution with mean 0, std 1)
3. The amount of noise added is controlled by the coefficient `c1` which is directly related to `eta` parameter
4. When `eta=0`, `c1=0` and no new noise is added (deterministic sampling)
5. When `eta=1.0`, full stochastic sampling occurs with the noise term applied

### Effect on conditioning frames

The noise is applied to *all frames* in the `sample` tensor, including conditioning frames. However, in the `diffusion_loop` function, after each step, the conditioned frames get reset with:

```181:181:models/colligo/models/common/diffusion/inference_loop.py
    if cond_latents is not None:
        latents = combine_latents(latents, cond_latents, cond_latent_inds)
```

This means any noise added to conditioning frames gets overwritten by the original conditioning signal after each step.

### The algorithm behind InstaFlow

InstaFlow is based on diffusion models but with modifications to allow faster sampling. Key aspects include:

1. **Prediction of the clean image**: The model predicts the noise, and the scheduler converts this to a prediction of the original clean sample.

2. **Controlled noise addition**: The scheduler carefully balances deterministic denoising with stochastic sampling through the `eta` parameter.

3. **Variance calculation**: The `_get_variance` method computes how much noise to add at each step.

4. **Coefficient calculation**: The c1-c4 coefficients control how much to weight the:
   - Original prediction (c3)
   - Fresh noise (c1)
   - Current noisy sample (c4)

5. **Rescaling**: The formula rescales the final result to maintain the correct signal-to-noise ratio.

The math behind this is a variant of the DDIM sampler (deterministic when η=0) but with InstaFlow-specific adaptations for faster convergence and better quality.

The key innovation with InstaFlow is that it aims to allow much faster high-quality generation with fewer diffusion steps than traditional DDPM or DDIM methods.

#### Question
explain ddpm sampling to me

#### Answer

# DDPM Sampling Explained

DDPM (Denoising Diffusion Probabilistic Models) is a class of generative models that works by gradually adding noise to data and then learning to reverse this process.

## Core Concept

The process has two main phases:
1. **Forward diffusion**: Gradually add noise to an image until it becomes pure noise
2. **Reverse diffusion (sampling)**: Start with pure noise and gradually denoise it

## Forward Diffusion

In the forward process, we add Gaussian noise to an image in T steps:
- Start with real image x₀
- At each step t, we add a small amount of noise:
  x_t = √(αₜ)·x_{t-1} + √(1-αₜ)·ε where ε ~ N(0,I)
- After T steps, the image becomes nearly pure noise x_T

The process follows a Markov chain, and each step can be expressed as:
- x_t = √(ᾱₜ)·x₀ + √(1-ᾱₜ)·ε where ᾱₜ = ∏ᵏ₌₁ᵗ αₖ

## Sampling (Reverse Diffusion)

DDPM sampling is the reverse process:
1. Start with random noise x_T ~ N(0,I)
2. Gradually denoise the image, step by step, from t=T to t=0

The reverse process is defined as:
- x_{t-1} = 1/√(αₜ)·(x_t - (1-αₜ)/√(1-ᾱₜ)·ε_θ(x_t,t)) + σₜ·z

Where:
- ε_θ(x_t,t) is the neural network that predicts the noise
- z ~ N(0,I) is random noise
- σₜ is the variance at step t (typically σₜ² = β̃ₜ = (1-αₜ₋₁)/(1-ᾱₜ)·βₜ in DDPM)

In the original DDPM paper, the transition from x_t to x_{t-1} includes stochasticity (the z term), making it a non-deterministic process.

## Mathematical Connection to Your Code

In the InstaFlow scheduler you showed earlier:
- α_prod_t corresponds to ᾱₜ
- The noise coefficient c1 controls the amount of stochasticity (related to η)
- When η=0, there's no new noise added (deterministic like DDIM)
- When η=1.0, it behaves more like traditional DDPM

The key characteristic of DDPM is the addition of noise at each reverse step, which:
1. Improves sample diversity
2. Can help with mode coverage
3. But requires more steps than deterministic variants like DDIM


#### Question
In the original DDPM paper and in instaflow, for step t, once we get the predicted (denoised frames) t-1, we add back some noise, before passing it to the model again to get predicted t-2. Why do we add back this noise? I know that it adds randomness and leads to sample diversity. But help me understand this intuitively. Give me the reasoning behind it. Also, expand on what you said here:
The key characteristic of DDPM is the addition of noise at each reverse step, which:
Improves sample diversity
Can help with mode coverage
But requires more steps than deterministic variants like DDIM

#### Answer

## Why Add Noise During Reverse Diffusion

Adding noise in the reverse diffusion process serves several fundamental purposes:

### Maintaining the Probabilistic Nature

Intuitively, think of the forward process as creating a cloud of possible noisy images around each clean image. When reversing, there are many possible clean images that could have produced any given noisy image. Adding noise allows the model to explore this distribution rather than committing to a single path.

Without noise, the model would always produce the same output given the same starting noise - like following a fixed path. With noise, it's like occasionally taking small random detours, allowing exploration of different possible outcomes.

### Avoiding Local Optima

Think of the denoising process as trying to climb down a mountain in fog:
- Deterministic sampling (DDIM): Always walks directly downhill
- Stochastic sampling (DDPM): Occasionally takes small random steps sideways

Those random steps help avoid getting stuck in small valleys (local minima) and can lead to discovering better paths.

### Mode Coverage vs Mode Collapse

"Modes" in a distribution represent distinct clusters of data types. In image generation:

- **Mode collapse** happens when a model only generates a limited subset of possible outputs
- **Mode coverage** means generating diverse, varied outputs representing the full data distribution

Adding noise helps prevent the model from always falling into the same "comfortable" patterns, forcing exploration of the full distribution.

### Sample Diversity Tradeoffs

1. **DDPM (with noise)**: 
   - ✓ Better diverse outputs
   - ✓ Can represent complex multi-modal distributions
   - ✓ More faithful to the true data distribution
   - ✗ Requires many steps (typically 1000+) for good results
   - ✗ Slower generation

2. **DDIM (deterministic)**: 
   - ✓ Much faster (can work with ~20-50 steps)
   - ✓ Still produces high-quality samples
   - ✗ Less diversity in outputs
   - ✗ May miss certain modes of the distribution

This noise tradeoff is why many practical implementations use a hybrid approach controlled by the η parameter, allowing you to balance speed versus diversity based on your application needs.

#### Question
If the original noise w start from, is random (form normal distribution), why do you say that 
"Without noise, the model would always produce the same output given the same starting noise - like following a fixed path. With noise, it's like occasionally taking small random detours, allowing exploration of different possible outcomes."
?
If we want to have sample diversity and represent complex multi-modal distributions, can't we just change the initial random noise? Just generate new set of random numbers? Why do we need to add back some noise at each step during denoising?

#### Answer

You're asking an excellent question that gets to the heart of diffusion models.

You're right that changing the initial noise will give different outputs even with deterministic sampling. However, there are deeper statistical reasons for adding noise at each step:

### Statistical Correctness

The forward diffusion process defines a specific probability distribution p(x_t|x_0) for each timestep. For the reverse process to properly invert this, the conditional distributions p(x_{t-1}|x_t) should include stochasticity.

Without per-step noise, we're not sampling from the true posterior distribution, but taking a shortcut. This can lead to:

1. **Distribution Mismatch**: The generated samples may not follow the exact same distribution as the training data

2. **Biased Mode Coverage**: While different initial noises will give different outputs, the deterministic path from any particular noise might consistently avoid certain modes

### Avoiding Systematic Bias

Deterministic sampling creates a direct one-to-one mapping from noise to output. This mapping might systematically miss certain types of outputs due to the training dynamics or model limitations.

Adding noise at each step breaks this rigid mapping, allowing:
- Paths that might have been "unreachable" from any initial noise to become possible
- The model to occasionally "jump" between different modes during sampling

### Practical Example

Imagine generating faces with a diffusion model:
- With deterministic sampling: Different initial noises might generate different faces, but perhaps never ones with certain rare features
- With stochastic sampling: Even from the same initial noise, the per-step randomness occasionally pushes the generation toward those rarer features

While changing initial noise gives diversity, adding per-step noise provides a more complete exploration of the underlying probability distribution the model learned.
