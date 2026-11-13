#!/usr/bin/env bash

set -exo pipefail

# Version of vLLM serve script to install.
INSTALL_SCRIPT_COMMIT="44b539c5"
INSTALL_SCRIPT="s3://colligo-dev-pr/deploy_v2/colligo-rhode/vllm_serve/vllm_serve-achicu-deploy-commit=${INSTALL_SCRIPT_COMMIT}.sh"


# VLLM_MODEL_NAME="BCCard/Qwen2.5-VL-32B-Instruct-FP8-Dynamic"
# VLLM_MODEL_NAME="Qwen/Qwen3-VL-235B-A22B-Instruct"
VLLM_MODEL_NAME="Qwen/Qwen3-VL-32B-Instruct-FP8"

# Use this to add custom vLLM args.
# export COLLIGO_VLLM_ARGS="--gpu-memory-utilization 0.9"

WORK_DIR=/tmp/vllm_serve/.vllm_serve
echo "WORK_DIR: $WORK_DIR"
mkdir -p $WORK_DIR
export COLLIGO_CONFIG_PATH="$WORK_DIR/config.yaml"
export COLLIGO_REQUEST_TIMEOUT=600


s5cmd cp $INSTALL_SCRIPT $WORK_DIR/install.sh

chmod +x $WORK_DIR/install.sh
$WORK_DIR/install.sh

source $WORK_DIR/activate.sh
python -m colligo.rhode.commands.dev_supervisor \
    --app-config ${COLLIGO_BUILD_SPEC} \
    --default-replica=0 \
    --fill-with-model "$VLLM_MODEL_NAME" \
    --frontend-workers 16 \
    --log-to-file