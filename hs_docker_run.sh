#!/bin/bash

# # Check if local SSD is available and remount if needed
# if [ "$HAS_LOCAL_SSD" = true ]; then
#     bash DOCKER_DIR/remount_ssd.sh
# fi

# Run the Docker container
docker run \
    --name "ati2_for_hqu" \
    --shm-size 24g \
    -p 4049:22 \
    $(extra_flags) \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -it "docker-clio-release.dr-uw2.adobeitc.com/inference/clio-and-colligo-inference-ubuntu22.04-ait"
