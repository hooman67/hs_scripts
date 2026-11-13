#!/usr/bin/env bash
export ARTIFACTORY_USER_KINETO=kineto
export ARTIFACTORY_UW2_USER=kineto
export ARTIFACTORY_UW2_API_TOKEN=AKCpBvWUY1qMpFTLYPP911ppArqmnzov5d7S2c8oNi3ge3FQCnCoq6EgpGhCRE4Ekc7iXXFxy


export KINETOBOT_GITHUB_API_TOKEN=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
export GLIMMER_DB=postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-test.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer

export PIAT_NAIVESAMPLER=1
export GENIE_COMMIT_SHA=a925de9cf8c6f191391dbe4e970803b63b3ede26
export GENIE_DIR="/mnt/localssd/genie"

# time_function setup_environment "${GENIE_COMMIT_SHA}"
git clone https://${KINETOBOT_GITHUB_API_TOKEN}@github.com/Adobe-Firefly/genie.git $GENIE_DIR
cd $GENIE_DIR
git checkout $GENIE_COMMIT_SHA

bash /sensei-fs/users/achicu/uv.installer.sh
source ~/.local/bin/env

export UV_CACHE_DIR="/mnt/localssd/.cache/uv"
mkdir -p $UV_CACHE_DIR

# inject the UV index passwords.
echo "machine artifactory-uw2.adobeitc.com login $ARTIFACTORY_UW2_USER password $ARTIFACTORY_UW2_API_TOKEN" >> ~/.netrc

cd $GENIE_DIR
uv venv --python 3.11
source .venv/bin/activate

uv pip install -v \
    -r "glimmer/modules/image_captioning/requirements.txt" \
    -e ./glimmer_queue \
    -e .[glimmer-core,lint]





CONFIG_GENTECH=/sensei-fs/users/achicu/glimmer_tests/configs/9_18_config_gen_tech.yaml
CONFIG_NOT_GENTECH=/sensei-fs/users/achicu/glimmer_tests/configs/9_18_config_non_gentech.yaml

# Choose the config path based on RANK env variable. If rank is ODD use CONFIG_GENTECH, if rank is EVEN use CONFIG_NOT_GENTECH
if [ $((RANK % 2)) -eq 0 ]; then
    CONFIG_PATH=$CONFIG_NOT_GENTECH
    export GLIMMER_JOB_NAME="vllm-not-gen-tech"
else
    CONFIG_PATH=$CONFIG_GENTECH
    export GLIMMER_JOB_NAME="vllm-gen-tech"
fi

echo "CONFIG_PATH: $CONFIG_PATH"

export LOG_DIR="/mnt/localssd/logs/$GLIMMER_JOB_NAME"
mkdir -p $LOG_DIR

export RANK=0
export WORLD_SIZE=1
export CUDA_VISIBLE_DEVICES=""
export MASTER_ADDR=127.0.0.1
export MASTER_PORT=23456

echo "Starting glimrelay!"

# Auto-restart glimrelay if it exits
(
    while true; do
        echo "Starting glimrelay process..."
        glimrelay --job-name "$GLIMMER_JOB_NAME" > $LOG_DIR/$JOB_NAME.grpc.out 2>> $LOG_DIR/$JOB_NAME.grpc.err
        echo "glimrelay process exited with code $?. Restarting in 5 seconds..."
        sleep 5
    done
) &


echo "Checking liveness endpoint..."

while true; do
    response=$(curl -s http://localhost:8001/liveness 2>/dev/null | tr -d '\n\r' | tr -s ' ' || true)

    if [ "$response" = "OK" ]; then
        echo "✓ Liveness check passed: $response"
        break
    else
        # Truncate long responses for cleaner output
        if [ ${#response} -gt 50 ]; then
            truncated_response="${response:0:47}..."
        else
            truncated_response="$response"
        fi
        echo "⏳ Waiting for service... (got: '$truncated_response')"
        sleep 1
    fi
done

echo "Colligo frontend Service is ready!"

echo "Starting glimmer!"

python -m glimmer.inference \
--config "$CONFIG_PATH" \
--gpus 0 \
--num-cpu-processes 7
