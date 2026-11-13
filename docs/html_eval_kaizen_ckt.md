# Running Kaizen
1. Install Colligo env
2. install Pluto CLI
```bash
export EXTRA_INDEX_URL=https://:AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple;export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A; export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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; pip install colligo.pluto.sdk --extra-index-url=$EXTRA_INDEX_URL; alias aip="python3 -m colligo.pluto.sdk.cli"; aip login
```
3. install dependencies
```bash
pip install wandb;
```
cd colligo;
Setup the dev environment. bash contrib/kaizen/setup/setup_env.sh
This installs tmux, the dev environment, pluto CLI and kaizen
If you already have a dev environment, but not pluto CLI run bash contrib/kaizen/setup/pluto_cli.sh
If you already have both dev environment and pluto CLI then run cd contrib/kaizen; pip install -e .

then launch kaizen:
cd contrib; python -m kaizen.kaizen_launch --config /sensei-fs/users/hshariati/hs_scripts/kaizen_configs/generation_colligo2html.yaml

## Debug Parameter

```json
{'enable_prompty': false, 'enable_dentro_pre': false, 'enable_dentro_post': false, 'disable_nsfw': true,'enable_pre_ssr_output':true}
```

## Combining, Transcoding CSVs and HTMLs

### Combining CSV and Rerendering HTMLs

```python
python models/colligo/models/common/asml_generation_utils/viq_scripts/combine_csvs.py --input_csvs "/sensei-fs/users/sannavajjala/dump/i2v-gt-prompt-athareja-mrizve-prompt1/reencoded.csv,/sensei-fs/users/sannavajjala/dump/i2v-gt-prompt-athareja-mrizve-prompt2/reencoded.csv,/sensei-fs/users/sannavajjala/dump/i2v-gt-prompt-athareja-mrizve-prompt3/reencoded.csv,/sensei-fs/users/sannavajjala/dump/i2v-gt-prompt-athareja-mrizve-prompt4/reencoded.csv" --save_to /sensei-fs/users/sannavajjala/dump/i2v-gt-default-atharejadata-mrizveprompt/ --caption_column "caption" --input_image_columns "image1,image2" --input_video_column "https_video0_ssr" --output_video_columns "prompt1, prompt2, prompt3, prompt4"
```

### Reencode the Videos

```python
python models/colligo/models/common/asml_generation_utils/viq_scripts/reencode_videos.py \
    --input_csv "<path-to-csv>" \
    --save_to "<save-to>" \
    --crf <crf-value> \
    --caption_column "caption" \
    --image_columns "image0,image1" \
    --video_columns "sensei_video0_ssr,sensei_video0_nossr"
```

## Uploading to SSEval Credentials (Key from Tian)

```python
s3_handle = S3Handle(
    aws_access_key_id="AKIASQRK44BROXTITHNO",
    aws_secret_access_key="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",
    aws_session_token=None,
    unsigned=False,
)
```

Above works for upload to eval hub.
For colligo2html use:

```bash
export AWS_ACCESS_KEY_ID=AKIASQRK44BROXTITHNO
export AWS_SECRET_ACCESS_KEY=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
aws s3 ls s3://clio-web-app/evaluation_service/eval_sets/i2v_animal_human_confusion_harm/data/part1/AdobeStock_583412451.jpeg
```


## bringing up clio demos on pluto machine
```bash
export PLUTO_MACHINE=pluto-prod-hshariati-viq-cpu-dev-1-1-0;cd contrib/clio_demos/clineto_global_view;streamlit run global_view_demo.py --server.port 8000 --server.baseUrlPath 'streamlit' --server.enableXsrfProtection=false --browser.gatherUsageStats=false --browser.serverAddress=$PLUTO_MACHINE-8000.colligo.dev
'''

## Colligo2HTML

You can debug by adding the line `'pdb.set_trace()'` or you can debug the script by putting this in your `lunch.json`:

```json
// ================ [Colligo2HTML] ================
{
    "name": "Python: Colligo to HTML",
    "type": "debugpy", "request": "launch",
    "module": "generate_html_from_inputs",
    "console": "integratedTerminal",
    "cwd": "${workspaceFolder}/contrib/AdobeDiffusion/scripts/clineto",
    "args": [
        "--endpoint", "http://localhost:8000",
        "--save_to", "/tmp/colligo2html_outputs",
        "--html_filename", "colligo2html_sample",
        "--input_file", "/sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_release_i2v.txt",
        "--limit_prompts", "2",
        "--seeds", "0",
        "--save_fps",
        "24",
        "--task", "t2v",
        "--width", "1280",
        "--height", "720",
        "--num_frames", "128", "--overwrite",
    ],
},
```


# html backend global view backend server
#### 1. Automatic S3 Backups

The system now automatically uploads backups to S3, while still keeping a configurable number of recent backups locally for quick access. S3 backups are stored in the same bucket used for other assets:

```
s3://clio.corp.adobe.com/model_evaluation/db_backups/
```

You can control the backup behavior with these parameters:

```bash
# Set backup interval to 6 hours (put 0.016 for about 1 minute)
./run.sh --backup-interval 6

# Disable automatic backups
./run.sh --disable-backups

# Keep only 5 most recent local (on disk) backups
./run.sh --max-backups 5
```


All S3 backup URLs are logged to a file so you can access them later:
```
backend/backups/backup_urls.log
```

This file contains timestamped entries with the HTTPS URLs to each backup.


You can easily download a backup from S3 using:
```bash
# Download using S3 URL
./run.sh --download-backup s3://clio.corp.adobe.com/model_evaluation/db_backups/evaluation_data_backup_20250424_174512.db

# OR using HTTPS URL
./run.sh --download-backup https://clio.corp.adobe.com/model_evaluation/db_backups/evaluation_data_backup_20250424_174512.db
```

##### 4. Restoring from Backups

After downloading a backup, you can restore it:

```bash
./run.sh --restore-from backend/backups/evaluation_data_backup_20250424_174512.db
```

##### 5. Getting Backup Information via API

The `/api/backup` endpoint now returns comprehensive information about both local and S3 backups:

```bash
curl http://localhost:8000/api/backup
```

This returns a JSON object with details about local backups, S3 backups, and backup configuration.

##### 6. Manual Backup Triggering

You can trigger a manual backup at any time:

```bash
curl -X POST http://localhost:8000/api/backup
```
8. To convert a .db file (backup of database) to csv use:
```
cd backend
python db_to_csv.py --db contrib/viq_html_backend/backend/evaluation_data.db --output path/to/output/dir
```


#### To migrate to new server
1. Save the current db to csv by running:
```bash
python db_to_csv.py --db contrib/viq_html_backend/backend/evaluation_data.db --output new-master
cp new-master/combined_export.csv master.csv
```
2. migrate the csv file. After this command all the htmls in the s3 will point to new ip address.
```bash
python migrate_db_or_csv_to_new_ip.py --source master.csv --old-api-url "https://pluto-prod-hshariati-viq-cpu-dev-1-1-0-8000.colligo.dev" --new-api-url "https://pluto-prod-hshariati-viq-4gpu-dev-cors9p-2-0-8000.colligo.dev"
```



### Generating HTML with Latest Adytya Scripts (09/19/2024): Baselines

```bash
cd contrib/AdobeDiffusion/scripts/clineto

python generate_html_from_inputs.py --input_file /sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_release.txt --endpoint http://localhost:8000 --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/baseline_t2v_h100_noPrompty_allDefault_09-23-24_2 --width 1280 --height 720 --num_frames 128  --seeds "0, 24" --save_fps 24 --overwrite True --limit_prompts 100
```

* T2V set: `/sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_release.txt`
* I2V set: `/sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_release_i2v.txt`
* T2v from morgan: `/sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_morgan.txt`
* i2v from Morgan: `/sensei-fs/users/hshariati/del/clineto/i2v_morgan.txt`

### To Get Both Pre and Post SSR in HTML Add This:

To `/mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/scripts/clineto/utils/request_utils.py` in the `get_headers` function:

```python
headers = {
    "x-colligo-debug-input": json.dumps(
        {
            "relax_fps": True,
            "enable_pre_ssr_output": True,
            "disable_nsfw": True,
            "enable_prompty": True,
            "dit_model_name": "filix2_t2v_prod1_814k32n_trt",
        }
    ),  # TODO: remove this , "trt_dit": False, "relax_fps": True}),
    "x-request-id": str(uuid.uuid4()),
    "authorization": f"Bearer {ims_token}",
    "x-api-key": "colligo_testing",
    "accept": "*/*",
    "scheme": "https",
    "content-type": "application/json",
}
```

To disable prompty, you can just use `enable_prompty: false`.

To disable NSFW, you need to first add the following to your `colligo.dev.yaml`:

```yaml
deployment_config:
  clineto_pipeline:
    impl_model_config_dict:
      handle_request_timeout: 1000000
      can_disable_nsfw: true
```

And then you can use:

```python
headers = { "x-colligo-debug-input": json.dumps({"relax_fps": True, "enable_prompty": False, "disable_nsfw": True, "enable_pre_ssr_output": True,}), # , "trt_dit": False}),
```

In `/mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/scripts/clineto/colligo_request_response.py`, remove the override. Replace:

```python
# override headers
new_headers = self.headers
if debug_params_override:
    new_headers["x-colligo-debug-input"] = debug_params_override  # needs to be type str
    # self.headers = new_headers
logging.info(f"endpoint: {endpoint} \npayload: {payload} \nheaders: {new_headers}")
response = self.session.post(endpoint, json=payload, headers=new_headers, timeout=30)
```

With:

```python
logging.info(f"endpoint: {endpoint} \npayload: {payload} \nheaders: {self.headers}")
response = self.session.post(endpoint, json=payload, headers=self.headers, timeout=30)
```

To disable NSFW, just sending disable is not enough. You need to set `can_disble_nsfw=true` in your `colligo.dev.yaml`.

```python
headers = {
    "x-colligo-debug-input": json.dumps(
        {
            "relax_fps": True,
            "enable_pre_ssr_output": True,
            "disable_nsfw": True,
            "enable_prompty": True,
            "dit_model_name": "filix2_t2v_prod1_814k32n_trt",
            "expansion_threshold": 1,
        }
    ),  # TODO: remove this , "trt_dit": False, "relax_fps": True}),
    "x-request-id": str(uuid.uuid4()),
    "authorization": f"Bearer {ims_token}",
    "x-api-key": "colligo_testing",
    "accept": "*/*",
    "scheme": "https",
    "content-type": "application/json",
}
```

```yaml
remote_deploy_per_spec:
  firefly_clineto:
    local_deploys:
      - clineto_pipeline
      - clineto_proxy_pipeline
      - filix2_t2v_prod1_814k32n_trt
    remote_deploys: []
    endpoint: [https://clio-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-dev.ethos851-stage-or2.ethos.adobe.net/)
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

## Converting S3 to Link

You can convert the s3 links below to what you can click on by just renaming the beginning:

```
s3://[clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/colligo/contrib/autoX/experiments](https://www.google.com/search?q=https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/colligo/contrib/autoX/experiments)
/data_for_chris/commands/data/disabilities_t2v_2/t2v.html
```

Becomes:

[https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/colligo/contrib/autoX/experiments/data_for_chris/commands/data/disabilities_t2v_2/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/colligo/contrib/autoX/experiments/data_for_chris/commands/data/disabilities_t2v_2/t2v.html)


Also 
if you want to download a link like:
s3://clio-web-app/ejo_assets/SFT_images/images_16_9/24.png
you can change it to:
https://clio-web-app.s3.amazonaws.com/ejo_assets/SFT_images/images_16_9/24.png