#!/bin/bash

# This script is meant to be run for at least 1 node in a "training job" on Pluto.
# Add this to the `main script` in pluto, and it should run inference with the specified config.

set -ex
# Allow other users to have the access.
umask 022
# Change to your own LDAP.
export USER=lakshya

# ============ 1. Experiment setup. ============
export EXP_NAME="swap_vae_v17_all_v10_c25_genaiaes_nogenaivid_aspect_ratio_largebsize_train"  # exp name for the training job
export EXP_ROOT="/sensei-fs/projects/firefly/clio/training/logs/$USER"  # exp root where the training job was
export CKPT_NAME="ckpt_step01345500.pth"  # checkpoint which you want to use for sampling
export DEBUG_DIFFUSION_IO=true
export OUT_DIR="/sensei-fs/users/hshariati/del/clineto/pkls"

export TRAINING_BRANCH="hshariati/test" # placeholder
# export TRAINING_COMMIT="686dcb03f986f68d7aff52f6da087710c52bc0dd" # placeholder

# Change to your own Mori root. If you defined TRAINING_BRANCH above, REPO_FOLDER won't be used.
# Mori will checkout the branch you specified with TRAINING_BRANCH, and training will be done on that branch.
export REPO_FOLDER=/sensei-fs/users/thinz/colligo_new/colligo/contrib/Mori

# ============ 2. Sampling parameters ============

# Parameters for sampling
export MODE="t2v" # ["t2v", "t2i"]  # TODO: add i2v and v2v modes

export EVAL_FIRST_N=2
export USE_EMA=true

export CFG_SCALE=7.5
export NUM_STEPS=50
export NEG_PROMPT="cartoon, vector art, & bad aesthetics  & poor aesthetics "
export CFG_CUTOFF=0
export TIMESTEP_INTERP_STEPS=25
export USE_CONFIG_PIX_CNT=true
export LATENT_OVERLAP_SIZE=1
export USE_SEPARATE_VAE_DEVICE=false


if [ "$MODE" == "t2v" ]; then
    export HEIGHT=68 #22 #32
    export WIDTH=120 #40 #32
    export PROMPT_NAME="video_eval_gen3_samples"
    export PROMPT_PATH="/sensei-fs/users/kduarte/temp/eval_sentences_master.txt"
    export NUM_FRAMES=31
    export SAVE_FPS=24
    export NUM_SAMPLES=1
    export KEYFRAME_LATENTS_CHUNK_INDICES="1 2 3 4 5" #"2 4 6 8" for v16
elif [ "$MODE" == "t2i" ]; then
    export HEIGHT=68
    export WIDTH=120
    export PROMPT_NAME="image_eval_sentences_master"
    export PROMPT_PATH="/sensei-fs/users/kduarte/temp/eval_sentences_master.txt"
    export NUM_FRAMES=1
    export SAVE_FPS=1
    export NUM_SAMPLES=1
fi


# ============ 3.  configs (do not change). ============

# We are under the assumption s3 checkpointing is default, and the original log folder exists (for config)
export CONFIG="$EXP_ROOT/$EXP_NAME/config.yaml"
export CKPT="s3://clio.corp.adobe.com/training_logs/clineto/$EXP_ROOT/$EXP_NAME/checkpoints/$CKPT_NAME"

export SCRIPT_DIR=${REPO_FOLDER}/collections/genai_foundation/scripts

# ============ 4. pluto configs (do not change). ============
export NUM_GPUS=${NUM_OF_GPUS}
export NUM_NODES=${WORLD_SIZE}
export NODE_RANK=${RANK}
export GPU_PRE_FLIGHT_TEST=false
# Whether to enable training auto recovery with torch elastic. False by default
export SOFTWARE_FAILURE_AUTO_RECOVERY=false
export EXP_MANAGER=false


# ============ 5. Check out the code if TRAINING_BRANCH is given (do not change). ============
if [ -n "$TRAINING_BRANCH" ]; then
    CLONE_DIR=/mnt/localssd/
    GITHUB_TOKEN=$(cat /sensei-fs/projects/firefly/clio/training/autogen/gh_token)
    REPO_URL="https://cliobot_adobe:${GITHUB_TOKEN}@github.com/Adobe-Firefly/colligo.git"
    rm -rf ${CLONE_DIR}/colligo
    mkdir -p ${CLONE_DIR}
    cd ${CLONE_DIR}
    git init;
    git config --global --add safe.directory ${CLONE_DIR}
    echo "****Cloning branch ${TRAINING_BRANCH}****"
    git clone --single-branch --branch ${TRAINING_BRANCH} ${REPO_URL}
    if [ $? -ne 0 ]; then
        echo "Error: Failed to clone branch ${TRAINING_BRANCH}."
        exit 1
    fi
    echo "****Repo cloned and HEAD is set to the BRANCH ${TRAINING_BRANCH}****"
    cd colligo
    if [ -n "$TRAINING_COMMIT" ]; then
        git checkout $TRAINING_COMMIT
        if [ $? -ne 0 ]; then
            echo "Error: Failed to checkout commit ${TRAINING_COMMIT}."
            exit 1
        fi
        echo "****Checked out COMMIT ${TRAINING_COMMIT}****"
    fi
    export SCRIPT_DIR=/mnt/localssd/colligo/contrib/Mori/collections/genai_foundation/scripts
fi


# ============ 6. Run training (do not change) ============
cd ${SCRIPT_DIR}
bash ./base_scripts/sample_ema.sh 2>&1 | tee -a $OUT_DIR/sample_env_${RANK}.log
exit 0
