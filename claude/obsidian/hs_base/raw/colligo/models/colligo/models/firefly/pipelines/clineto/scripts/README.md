# Pipeline Scripts

- Pipeline scripts are ad-hoc scripts that depends on the pipeline
- `generate_html_from_inputs.py` - Script to generate an html from a colligo endpoint given a prompt file
- `load_test_smoothtalk.py` - Load test script for SmoothTalk audio editing pipeline

## SmoothTalk Load Testing (`load_test_smoothtalk.py`)

Tests end-to-end SmoothTalk pipeline performance by uploading audio once and making concurrent requests.
Measures time to complete N requests and calculates RTF (Real-Time Factor).

### Basic Usage

```bash
# Run 100 requests with 4 concurrent workers
python models/colligo/models/firefly/pipelines/clineto/scripts/load_test_smoothtalk.py \
  -n 100 \
  -c 4 \
  --endpoint http://localhost:8000 \
  --audio /path/to/audio.wav
```

### Test Multiple Concurrency Levels

```bash
python load_test_smoothtalk.py \
  --requests 50 \
  --concurrency 1 2 4 \
  --endpoint http://localhost:8000
```

### With Authentication

```bash
export TOKEN="your-bearer-token"
python load_test_smoothtalk.py \
  -n 100 \
  -c 4 \
  --endpoint https://your-endpoint.adobe.net
```

### Output

The script outputs:
- Real-time progress logs
- Summary table with latency percentiles (P50, P95, P99)
- **RTF (Real-Time Factor)**: audio_duration / processing_time
  - RTF > 1.0 means faster than real-time
  - RTF = 0.5 means 2x slower than real-time
- Throughput (requests/second)
- Success rate
- JSON results file for further analysis

## HTML Generation using a Colligo Endpoint (`generate_html_from_inputs.py`)

- The code invoked by `generate_html_from_inputs.py` is split between `models/colligo/models/firefly/pipelines/clineto/` & `models/colligo/models/common/asml_generation_utils/` with `pipelines/clineto` having all pipeline specific code and utilities and `asml_generation_utils` having broader generation utilities

### Command to run HTML Generation from CLI

```bash
python models/colligo/models/firefly/pipelines/clineto/scripts/generate_html_from_inputs.py  \
--endpoint https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/ \
--input_file <path_to_prompts_file> \
--task t2v \
--n_jobs 1 \
--limit_prompts 10 \
--save_to <directory_path_to_save_results> \
--seeds "24, 36, 48, 60" \
--fix_seeds --height 1280 \
--width 720 \
--num_frames 64 \
--save_fps 24 \
```

OR

- Copy over the following snippet into the `Configurations` section of your `launch.json`

```
        {
            "name": "---------[HTML Generation]--------- "
        },
        {
            "name": "HTML Generation: Colligo2HTML",
            "type": "debugpy",
            "request": "launch",
            "module": "generate_html_from_inputs",
            "console": "integratedTerminal",

            "cwd": "${workspaceFolder}/models/colligo/models/firefly/pipelines/clineto/scripts/",
            "args": [
                // "--endpoint", "https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/",
                "--endpoint", "http://localhost:8000",
                "--task", "i2v",
                "--seeds", "24, 36, 48, 60",
                "--save_to", "/sensei-fs/users/sannavajjala/dump/html_debug_i2v_v1",
                "--overwrite",
                "--input_file", "/sensei-fs/users/sannavajjala/prompts/i2v_prompts.txt",
                "--limit_prompts", "8",
                "--width", "1280",
                "--height", "720",
                "--num_frames", "128",
                "--n_jobs", "1",
            ],
        },
```

Note: To hit an ethos endpoint via python code (requests.post) from a RunAI instance, remove the `colligov2` and `corp` from the URL so
<https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/> , thus have the <https://clio-video-dev.ethos851-stage-or2.ethos.adobe.net/> Both of them hit the same server, they're just aliases. We don't have access to the corp url from runai/devbox so we need to use the other one.
