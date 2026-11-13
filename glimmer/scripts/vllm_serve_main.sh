#!/usr/bin/env bash
set -exo pipefail

# export AWS_ACCESS_KEY_ID=ASIA3B7MOPLPZ7MTTFZR
# export AWS_SECRET_ACCESS_KEY=m/3SFjXbZ/9+lG+v08Co1v73qv8RWLJpOvI58zrS
# export AWS_SESSION_TOKEN=FwoGZXIvYXdzEEAaDKHbBxuEY9uDrbeQwCLtAWqZeHOY4KpSh5YDZvMf+7y28RTR9V+obFbujBomai99XEgJlErg3hs/de/jd5mXZGrlvpeBT+0fMA5ORegh74mWb0NcxG0ilj2BQ6iXojVSO19GxeSNSWnOAExqMvMNbB0+NGs4pyEEJlxzY71Cchozbqcf2YwBatuM+GCVS7nShsdcTBnOKuE4B2yr/VLW28OnQ73VevJqvSkd14WlIVz5MpXyuCLz1Z+tSA5ZX1320vP/SeKlIQ62I8wmH9sq1ApTXWqJ0ydgfpAD2c5s+4KBDwuq9XRdWe3wZDHi9mW7TZFvIa9U7jtuiV/pHiik0ZvHBjItATSRDEY5uZm1HkQPftl4UjpcFSc8MU36rx+qqyVdlEILtthtI+GjocnAHDSe
export AWS_ACCESS_KEY_ID=ASIA3B7MOPLP3NAQP5U5
export AWS_SECRET_ACCESS_KEY=6nOux9IbEP81iRaQrpTeIMOkos4I8iZg3/bP/Q/E
export AWS_SESSION_TOKEN=FwoGZXIvYXdzEKD//////////wEaDF2yjJvIsfC0UsN0LSLtAdL/6QJX1IkgBkQhzSANpA/ewNm7ORtwJ/VrVtX0dLHQQ6a1xIecfnMZz8qo+3QEUw08+w2uVXqqxGM/nK4FuGcbFJkejgtU7vda/1WRtNUXkov8ewf999kYNlmciyrkw/TIFThalXIWwS8X1kqJT6OsqkNSkuLGjFyhWjEWb5qa0LVGIm9AATvNxnNKL/r2AjY/r9V8v4D3+8w0jmsZ5BSeB6IJyysvcpAJEHHvJOmb9yPUZvE2qhS5C4UZFYjTcBx9TykUc6AP6WhJnc4J9nYB51M4z/6NJP4kDm7idm25aQXt8oX9hxj33RuW+ii18ejHBjItIPqgEgKMrLf5z3hlM8A07DDZO3gAF85nScFHKtWWQK3tTgWCyme8TN/KuE2y

# Version of vLLM serve script to install.
INSTALL_SCRIPT_COMMIT="b886c0c2"
INSTALL_SCRIPT="s3://colligo-dev-pr/deploy_v2/colligo-rhode/vllm_serve/vllm_serve-achicu-deploy-commit=${INSTALL_SCRIPT_COMMIT}.sh"


# Available models:
# - Qwen/Qwen2.5-VL-32B-Instruct
# - Qwen/Qwen2.5-VL-32B-Instruct-AWQ
# - BCCard/Qwen2.5-VL-32B-Instruct-FP8-Dynamic
# - OpenGVLab/InternVL3-38B

# Model name to serve:
# VLLM_MODEL_NAME="BCCard/Qwen2.5-VL-32B-Instruct-FP8-Dynamic"
# VLLM_MODEL_NAME="Qwen/Qwen3-VL-235B-A22B-Instruct"
# VLLM_MODEL_NAME="Qwen/Qwen3-VL-32B-Instruct"
VLLM_MODEL_NAME="Qwen/Qwen3-VL-32B-Instruct-FP8"

# Use this to add custom vLLM args.
# export COLLIGO_VLLM_ARGS="--max-model-len 32k"
# export COLLIGO_VLLM_ARGS="--gpu-memory-utilization 0.9"

WORK_DIR=$(pwd)/.vllm_serve
echo "WORK_DIR: $WORK_DIR"
mkdir -p $WORK_DIR
export COLLIGO_CONFIG_PATH="$WORK_DIR/config.yaml"
export COLLIGO_REQUEST_TIMEOUT=600


## VAULT SECRETS MUST BE ADDED TO THE PLUTO JOB
# Object Path                                              | Key            | Environment Variable
# ----------------------------------------------------------------
# dme_colligo/services/pluto/projects/vllm-inference/redis | redis_username | PLUTO_REDIS_USERNAME
# dme_colligo/services/pluto/projects/vllm-inference/redis | redis_password | PLUTO_REDIS_PASSWORD

VAULT_SECRET_PATH="/etc/pluto/vault-secrets"

cat << EOF > $COLLIGO_CONFIG_PATH
redis:
    host: clustercfg.vllm-vllm001-or2-memorydb.yht1xq.memorydb.us-west-2.amazonaws.com
    port: 6379
    ssl: true
    namespace: "pluto-laser-ee52b573-ac66-4532-8d0d-f0fb82e5d0ea"
    username: $(cat $VAULT_SECRET_PATH/PLUTO_REDIS_USERNAME)
    password: $(cat $VAULT_SECRET_PATH/PLUTO_REDIS_PASSWORD)
EOF

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
