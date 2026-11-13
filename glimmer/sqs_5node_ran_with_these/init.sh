#!/usr/bin/env bash

# Source the functions
source "/docker_functions.sh"

# save log to node-aware path when distributed
export logdir="/mnt/localssd/logs/colligo-hs-1-multi-node-test-g8n-v121b"
export logfile="/mnt/localssd/logs/colligo-hs-1-multi-node-test-g8n-v121b/colligo-hs-1-multi-node-test-g8n-v121b.$RANK.out"

mkdir -p "$logdir"
log_info "logdir: $logdir" | tee -a "$logfile"
log_info "logfile: $logfile" | tee -a "$logfile"

# print the config file if a real path was provided in context
log_info "#####################################################################################" >> "$logfile" 2>&1


log_info "No on-disk config file path provided; config payload will be written by executor." | tee -a "$logfile"




log_info "#####################################################################################" >> "$logfile" 2>&1
log_info "DOCKER IMAGE: docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/kineto:glimmer-image"

# Versioning and features
export GENIE_VERSION=1.0.0+e26d2ae
log_info "GENIE_VERSION: $GENIE_VERSION"

# New cli options for the docker entrypoint
export INSTALL_MORI=false
export MORI_COMMIT_SHA=None
export MORI_VARIANT=None


    export GLIMMER_REQUIREMENTS=glimmer/modules/image_captioning


if [ "${INSTALL_MORI}" = "false" ]; then
    log_info "Setting MORI_INSTALLATION_FINISH to false"
    export MORI_INSTALLATION_FINISH=false
fi

log_info "Installing genie and other dependencies"

source "/entrypoint.sh"

log_info "Init Script complete"