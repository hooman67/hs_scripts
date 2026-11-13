#!/usr/bin/env bash


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

# Source the functions
source "/docker_functions.sh"
PIDS=()
trap cleanup EXIT INT TERM

if [ -z "${USER:-}" ]; then
    export USER="colligo"
fi
if [ -z "${USER:-}" ]; then
    log_info "USER is not set; exiting."
    exit 1
fi
log_info "User LDAP: ${USER}"

log_info "Unified inference main_script.sh (handles single and multi node)"


###############################################################################
# 1.  Log directory
###############################################################################

export job_log_dir="/mnt/localssd/logs/logs/"
if [ -z "${NODE_RANK:-}" ]; then
    export NODE_RANK="${RANK:-0}"
fi
export node_log_file="/mnt/localssd/logs/logs/$NODE_RANK.out"

mkdir -p "$job_log_dir"
log_info "Job logs will be written to /mnt/localssd/logs/logs/"
sudo chmod -R 777 /mnt/localssd/

###############################################################################
# 3.  S3 log sync in background
###############################################################################

export S3_LOG_DIR="s3://glimmer-testing/glimmer-logs/"
nohup bash -c 'while true; do s5cmd sync "$job_log_dir"/ "$S3_LOG_DIR"/; sleep 60; done' &
PIDS+=($!)
log_info "Job logs will be copied to "


# Setup env variables
# ============ pluto configs. ============
export NCCL_SOCKET_IFNAME=eth0
export NCCL_DEBUG=INFO
export FI_PROVIDER="efa"
export FI_EFA_USE_DEVICE_RDMA=1
export PIAT_NAIVESAMPLER=1
export CUDA_VISIBLE_DEVICES=''

# Important: otherwise multi-node training will be super-slow
export LD_LIBRARY_PATH=/usr/local/lib/:/opt/nccl/build/lib:/usr/local/cuda/lib64:/opt/amazon/efa/lib:/opt/aws-ofi-nccl/lib:$LD_LIBRARY_PATH

export RANK=0
export NODE_RANK=0
export WORLD_SIZE=1
export MASTER_ADDR=127.0.0.1
export MASTER_PORT=23456

# Activate mori-venv if present
if [ -f "/mnt/localssd/mori-venv/bin/python" ]; then
    log_info "Activating mori-venv environment"
    sudo chmod -R 777 /mnt/localssd/mori-venv || true
    source /mnt/localssd/mori-venv/bin/activate
else
    log_info "mori-venv Python interpreter not found -- relying on base python interpreter"
fi




###############################################################################
# 4.  Run Glimmer
###############################################################################
log_info "Inference is starting"
start_time=$(get_timestamp)
RC=0

export AWS_SQS_NAME="hs_qwen3-vl-32b-imagecap-25-10-24"

execute_glimmer_inference \
    --job-name colligo-hs-2-multi-node-test \
    --num-nodes 1 \
    --gpus 0 \
    --num-cpu-processes 32  \
    --strategy auto \
    --log-file "$node_log_file" \
    --config eNqNVG1v0zAQ/r5fcXyYsqGlTdtRNoshxigwMTbYJpD4YnnpNTF1nMx2NsrLf+fsvHQDJpFGVe79ubvHToVSVyJdWgY/fm3MhRNsA+BKuDTnVn5HBiOSvZ7bsjYpKX6SAsCiwtSBsBYdl/MdsM4cFyLDXNgcFqYswKCY80qY6xrdVggCiOyEDYdzadMyXqBwtcHYutLgsJVsXAiphwqF5kLPuSp1NsxQT4fOeMMNGitLzZ0s0DpRVAfjZPwkHiXxePIloWf4eNDWjHbaorm8QQ/ESUehUmdwAAuhLHYOC6lQiwJJ70yNQbsNn9/OzmetB3V3ZmQmNZyeXcLJ8bsZRJsLQzGbUetyePoKtuyESz8FvsRV5zb4WmURnJ3DP42VzqLtOynSXGiNysKjAxjf0R8dXnRgwEM7BWk5DcZhmsOll+tKlTRxWhbCc4hoLrtxMqIXkoSFN+oTzE4uZvcCnoWA6QMBs9NX9KXrgrvcr5XoMm4Vt6VZ0k4YJKSw15Y2lgrFK4MLJBY1jl5vMEW/iECutfpGWnkllXSrsNOydtxiWmpfYzQOSR3NzHpexiA1ayE1k/RsY/e4F8xlhUYQrRhkShYFmkFRzmuFdtCEpaJqqTBosg+oIlHLtQtyJcG0ON1tstWOtfV6bUy/6IUilgUXL3ZnoQUYe1hbnXI7xFipl30DfStwL/lfpXoGEtzjInugZf/UWhLxqRpbg6HGUflKdABEYZuaPjevjWKQO1fRiQxLy0vr2J4/Qzej4EZDSWtjUKcrBntJ0BXiG41niZr2s5vsTxulL0JHzBGyj7eoh/5vEn86iSfjl/GxJrR16uLXH/a6gVa05x4usVguJBr6bAHG617a6wapqdHTIDgswn7puiDaDRqsrqz4srmuGqHytv0g3hrp0HTjbqpb1u+pvXq4vwL85ArV0uDad8GphY4wRNdxP+0urL2SiNLdTUTnjp7esTKUzqz8sWd/9EVoKDzg436IbC2T3QmTofsPEjeGQWDEUa9+04S9D8aN391h0Rw= \
    || RC=$?

if [ "$RC" -ne 0 ]; then
    log_info "Inference failed with exit code $RC"
else
    log_info "Inference completed successfully"
fi
end_time=$(get_timestamp)

log_info "Inference finished in $(format_duration $(echo "$end_time - $start_time" | bc))"

###############################################################################
# 5.  Final log sync & exit
###############################################################################
s5cmd sync "$job_log_dir"/ "$S3_LOG_DIR"/ || true
exit "$RC"