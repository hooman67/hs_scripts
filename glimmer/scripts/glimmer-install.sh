#!/usr/bin/env bash

Check if genie_commit_sha argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <genie_commit_sha>"
    echo "Example: $0 a925de9cf8c6f191391dbe4e970803b63b3ede26"
    echo "Example: $0 1c34009111f0f6861ded2b933a7f762ef5a6a228"
    exit 1
fi

export ARTIFACTORY_USER_KINETO=kineto
export ARTIFACTORY_UW2_USER=kineto
export ARTIFACTORY_UW2_API_TOKEN=AKCpBvWUY1qMpFTLYPP911ppArqmnzov5d7S2c8oNi3ge3FQCnCoq6EgpGhCRE4Ekc7iXXFxy


export KINETOBOT_GITHUB_API_TOKEN=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
export GLIMMER_DB=postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-test.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer

export PIAT_NAIVESAMPLER=1
export GENIE_COMMIT_SHA=$1
export GENIE_DIR="/mnt/localssd/genie"

time_function setup_environment "${GENIE_COMMIT_SHA}"
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




# CONFIG_PATH=/sensei-fs/users/hshariati/del/glimmer/9_18_config_gen_tech.yaml
# export GLIMMER_JOB_NAME="hs-vllm-glimmer-debug"


# echo "CONFIG_PATH: $CONFIG_PATH"

# export LOG_DIR="/mnt/localssd/logs/$GLIMMER_JOB_NAME"
export LOG_DIR="/mnt/localssd/logs/hs_glimmer_logs"
mkdir -p $LOG_DIR

export RANK=0
export WORLD_SIZE=1
export CUDA_VISIBLE_DEVICES=""
export MASTER_ADDR=127.0.0.1
export MASTER_PORT=23456
