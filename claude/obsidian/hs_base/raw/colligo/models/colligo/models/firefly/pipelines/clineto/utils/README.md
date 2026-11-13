# Colligo2HTML

Use the Colligo2HTML module to generate results from a colligo deployed endpoint including localhost, dev, stage, eval, or experimental endpoints. The Colligo2HTML currently supports video generation (t2v, i2v, v2v, and guided transform)

## Using Colligo2HTML

The relevant datasets are located at `data/test/clio_htmls/videos/clineto_team_test_sets` after `./m lfs.pull`

### For Text to Video generations (T2V)

```bash
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py \
--endpoint https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/ \
--input_file data/test/clio_htmls/videos/clineto_team_test_sets/t2v/t2v_bytesize_regression.csv \
--task t2v \
--save_to <path to save videos> --overwrite \
--width 1920 --height 1080 --num_frames 128 \
--n_jobs 1 \
--seeds 24 \
--limit_prompts 100000 \
--debug_params "{'enable_pre_ssr_output': true}"

```

### For GenExtend (Video to Video) generations (V2V)

```bash
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py \
--endpoint https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/ \
--input_file data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_bytesize_regression.csv \
--task v2v \
--save_to <path to save videos> --overwrite \
--width 1920 --height 1080 --num_frames 64 \
--n_jobs 1 \
--seeds 24 \
--limit_prompts 100000 \
--debug_params "{'relax_fps': true, 'enable_pre_ssr_output': true}"
```

### For Image to Video generations (I2V)

```bash
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py \
--endpoint https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/ \
--input_file data/test/clio_htmls/videos/clineto_team_test_sets/i2v/i2v_bytesize_regression.csv \
--task i2v \
--save_to <path to save videos> --overwrite \
--width 1920 --height 1080 --num_frames 128 \
--n_jobs 1 \
--seeds 24 \
--limit_prompts 100000 \ 
--debug_params "{'enable_pre_ssr_output': true}"
```

### For Guided Transform (i2v_guided_transform)

```bash
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py \
--endpoint https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/ \
--input_file /sensei-fs/users/sannavajjala/shared/i2v_guidedtrans_501_formatted.csv \
--task i2v_guided_transform \
--save_to <path to save videos> --overwrite \
--width 1920 --height 1080 --num_frames 128 \
--n_jobs 1 \
--seeds 24 \
--limit_prompts 100000 \ 
--debug_params "{'enable_pre_ssr_output': true}"

```

### For Debugging you can use the following `launch.json` snippet to put at `.vscode/launch.json`

```bash
        {
            "name": "---------- Colligo2HTML Generation ----------",
        },
        {
            "name": "HTML Generation: Colligo2HTML",
            "type": "debugpy",
            "request": "launch",
            "module": "colligo2html",
            "console": "integratedTerminal",

            "cwd": "${workspaceFolder}/models/colligo/models/firefly/pipelines/clineto/utils/",
            "args": [
                "--endpoint", "https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/",
                "--input_file", "data/test/clio_htmls/videos/clineto_team_test_sets/t2v/t2v_bytesize_regression.csv",
                "--save_to", "/sensei-fs/users/sannavajjala/outputs-of-colligo2html",
                "--overwrite",
                "--task", "t2v",
                "--seeds", "24",
                "--width", "1920",
                "--height", "1080",
                "--limit_prompts", "10",
                "--num_frames", "128",
                "--n_jobs", "1",
                // "--resume", 
                // "--resume_from_csv", "/sensei-fs/users/sannavajjala/outputs-of-colligo2html/csv_to_resume_from.csv",
            ],
        },
```

## Input Structure

The expected input is a csv file with the ALL of the following columns present
If your CSV only contains a subset of the columns, run the `models/colligo/models/common/asml_generation_utils/viq_scripts/standardize_csv.py` script to get it into the standard format

You can override these parameters via the command line argument. If a CLI argument such as `--num_frames` is given, the same num_frames will be used for all inputs in the CSV

```python
"prompt",
"negative_prompt",
"image",  # For I2V
"image_urls",  # For Guided Transform
"video",  # For V2V
"clip_start",
"clip_end",
"extend_duration",
"extend_forward",
"camera_motion",
"shot_angle",
"shot_size",
"prompt_style",
"seeds",
"width",
"height",
"num_frames",
```

## Output Structure

The `--save_to` folder will contain the followng files

1. `html.txt` - Contains the rendered html link that can be shared
2. `log.txt` - Contains the logs
3. `<task>_<intermediate/final>_<timestamp>.<csv/html>` - Contains the intermediate results (shareable immediately), final results (after completion) in the form of a csv and the corresponding rendered html


## Supporting HTML Scripts

TODO: Will be part of the stable scripts PR 
