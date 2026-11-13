# Pixel Parity

Generate a report with the pixel party metrics between mori and colligo.


## Install

```

export COLLIGO_X_API_KEY=....
export COLLIGO_IMS_TOKEN=....

aws s3 cp s3://clio.corp.adobe.com/glow_worm_test_sets/lego_design/slice/input_nb2_gpt_4.1_i2l_v4.json .

# Create and activate colligo dev environment

```

## Run

You can run this script only from pluto because the JSON input files has references to images from pluto.

Run the full flow:

```

./run_layerize_pixel_parity.sh

```

The script creates and activates a local Python virtual environment, installs `requirements.txt`, runs verification, and builds/uploads the report.

Or run the Python steps independently:

```

python3 verify_layerize_user_image.py \
  --input-json input_nb2_gpt_4.1_i2l_v4.json \
  --html-url https://dit-scale-up.s3.us-west-2.amazonaws.com/fe-experiments/FFP-35415-lego_design_gw_slice-FFP-61674-vmm_8step_slice2_teacher_1m230k_v10_accum8-2026.06.13-07.54.35/inference/vmm_8step_slice2_teacher_1M230k_v10_accum8_step01230300_ema=True/input_nb2_gpt_4.1_i2l_v4_ema_true_2026-06-15T12:03:28/index.html \
  --base-url https://lego-designs-dev.ethos851-stage-or2.ethos.adobe.net \
  --concurrency 10 \
  --output-json /tmp/verify_results.json \
  --output-dir verify_layerize_output

python3 build_layerize_report.py \
  --input-dir verify_layerize_output \
  --output-dir verify_layerize_report \
  --s3-uri s3://dit-scale-up/fe-experiments/FFP-35415-lego_design_gw_slice-FFP-61674-vmm_8step_slice2_teacher_1m230k_v10_accum8-2026.06.13-07.54.35_jun_23/

```

You can override defaults with environment variables:

```

PYTHON_BIN=python3 \
VENV_DIR=local \
INPUT_JSON=input_nb2_gpt_4.1_i2l_v4.json \
HTML_URL=https://dit-scale-up.s3.us-west-2.amazonaws.com/fe-experiments/FFP-35415-lego_design_gw_slice-FFP-61674-vmm_8step_slice2_teacher_1m230k_v10_accum8-2026.06.13-07.54.35/inference/vmm_8step_slice2_teacher_1M230k_v10_accum8_step01230300_ema=True/input_nb2_gpt_4.1_i2l_v4_ema_true_2026-06-15T12:03:28/index.html \
BASE_URL=https://lego-designs-dev.ethos851-stage-or2.ethos.adobe.net \
CONCURRENCY=10 \
OUTPUT_JSON=/tmp/verify_results.json \
OUTPUT_DIR=verify_layerize_output \
REPORT_DIR=verify_layerize_report \
S3_URI=s3://dit-scale-up/fe-experiments/FFP-35415-lego_design_gw_slice-FFP-61674-vmm_8step_slice2_teacher_1m230k_v10_accum8-2026.06.13-07.54.35_jun_23/ \
./run_layerize_pixel_parity.sh

```