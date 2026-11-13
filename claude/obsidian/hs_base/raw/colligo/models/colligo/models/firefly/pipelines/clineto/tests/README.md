Moving all utilities for evaluation here. They were added to the clineto itself and that caused depending on compare.common (through ASML generation utils), and caused model code to be 15 GB!!

# Eval Inference Generation
e.g. for `i2v_camera_path` task on DEV endpoint
```
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py \
    --endpoint https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/ \
    --initiative clineto \
    --experiment <NAME> \
    --input_file <DATASET> \
    --width 1920 --height 1080 \
    --save_to <LOCAL_DEST> \
    --task i2v_camera_path \
    --seeds 24 \
    --num_frames 121 --n_jobs 1 --num_jobs 1 \
    --node_idx 0 --overwrite --limit_prompts 10 \
    --model_name "Clineto-V1.8" \
    --ckpt "filix_ckpt_step01376000_slimmed_camera_path_ckpt_step01736000"
```
## Upload generation to EvalHub
Steps:
### 0. env set up
Onboard Eval Hub (wiki: https://evaluation-hub.adobe.io/docs/setup/setup)
- Prod https://admin.adobe.io/consumer/org/3857104/apps/849376
- Stage https://admin-stage.adobe.io/consumer/org/292391/apps/236039

and create your API key `YOUR_API_KEY`.

on pluto: 
```
export EVAL_SERVICE_API_KEY="YOUR_API_KEY"
pip install eval_service_common -U --extra-index-url https://${ARTIFACTORY_UW2_USER}:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-eval-service-common-release-local/simple
```
### I. run html generation. 
See above command for `i2v_camera_path`. The "save_to" local path has video output assets to upload, and csv output.
### II. upload to EvalHub
```
python models/colligo/models/firefly/pipelines/clineto/tests/utils/upload_generation_to_eval_hub.py \
    -in camera_path_final_2025_10_13_21\:26.csv \
    -dir <LOCAL_DEST> \
    -d v2v_CameraPath_246 \
    -v 1.0
```
