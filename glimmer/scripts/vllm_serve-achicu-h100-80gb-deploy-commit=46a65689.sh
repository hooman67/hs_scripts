#!/bin/bash

# usage:
#
# s5cmd cp <s3 url to this file> <out dir>/init.sh
# bash <out dir>/init.sh
# source <out dir>/activate.sh
# For frontend
#   python -m colligo.rhode.commands.frontend_supervisor --app-config ${COLLIGO_BUILD_SPEC}
# For backend
#   python -m colligo.rhode.commands.models_supervisor --app-config ${COLLIGO_BUILD_SPEC}

function unpack_tar() {
    directory="$2"
    tarfile="$1"
    mkdir -p ${directory}
    pushd .
    cd ${directory}
    tar -xf ${tarfile}
    popd
}

SHELL_OPTS=$(set +o)
set -eo pipefail

S3_NO_SIGN_REQUEST=""

# Process all arguments for flags before setting other variables
while (( "$#" )); do
    case "$1" in
        --s3-no-sign-request)
        S3_NO_SIGN_REQUEST="--no-sign-request"
        shift # Remove the current flag from the list of arguments
        ;;
        *)
        # Break the loop if no more flags are detected
        break
        ;;
    esac
done

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

TMP_OUT="${1:-$SCRIPT_DIR}"
DOWNLOAD_DIR="$TMP_OUT/download"
ROOT_VENV_DIR="$TMP_OUT/venv"
CUSTOM_VENVS_DIR="$TMP_OUT/custom_venvs"
SPEC_LOCATION="$TMP_OUT/colligo-spec.json"
mkdir -p "$DOWNLOAD_DIR" "$ROOT_VENV_DIR" "$CUSTOM_VENVS_DIR"

# download archives
echo "Downloading Code..." >&2
cat << EOF | xargs -P8 -I{} bash -c '{}'

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.rhode/a6ee18e3b9ffc4eee613954340d6ad29e5e4a1eab7a763e14c43c820b13faab6.tar $DOWNLOAD_DIR/download_0.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.external_services.setup/ef80797ab7b0d11c0d21d3225d536b57b80fe152a8eccf0cf2c48d046cbe1593.tar $DOWNLOAD_DIR/download_1.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.fastapi/af445566d2cc5696964971c4f388083b62ada7015374fd31420f416ee4c07e78.tar $DOWNLOAD_DIR/download_2.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.data/1bb210a7c79f360d98252a08b7cfa2712bfb2a86674be347b6e1cb9518c2d4e0.tar $DOWNLOAD_DIR/download_3.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.base/4dfaf704b8ee76c51eab0bee8c7a2e827b6aae50bef2dd796fd0bbd04ede1b75.tar $DOWNLOAD_DIR/download_4.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.external_services.ims/79abd54275cd3e180b93a040a782050c194d3a58e23247f35aa018690f474430.tar $DOWNLOAD_DIR/download_5.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.external_services.common/1aecc6173b484f94c3e6d490f7dc2a81ae87fbe442eb3ce2e20d427f6002b81a.tar $DOWNLOAD_DIR/download_6.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.external_services.acmp/eec41604f3739833d0a04f819551c13149e36172ffb41d71de3701570b5eec59.tar $DOWNLOAD_DIR/download_7.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.httpx/d54963359af5c7e92b30e6113646f15bcd9d198fd0b06c74616d9622eff7c4da.tar $DOWNLOAD_DIR/download_8.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/code/colligo.external_services.acp/ed1bda0ff10ef94e8263506ab173ce5d6f37dd1832fd8c6fca4acb490257652c.tar $DOWNLOAD_DIR/download_9.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/conda.python-dist/602720e26b77c846545b5bb6eedc6b8063116651d827422cd9837057fcd9112b.tar $DOWNLOAD_DIR/download_10.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/data/spec.json/85d5ba8999c436697c7eb424e8f90f376775ec2f9d2fc61ea3aa930b06d2efc1.json $DOWNLOAD_DIR/download_11.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/pip.dev_colligo-rhode/20ea7146ebd29a72d87d1c675412ef65f4eb5abae113c93fab4269667c487e05.tar $DOWNLOAD_DIR/download_12.tar

s5cmd $S3_NO_SIGN_REQUEST cp s3://colligo-dev-pr/deploy_v2/pip.lego_vllm_colligo-rhode/83522eca0a5eea334d2cdee4a0d16325341e90922cc5a45410f7aa6dd63d8b0b.tar $DOWNLOAD_DIR/download_13.tar

EOF




    # unpack python distribution dev

    
        
        VENV_DIR="$ROOT_VENV_DIR"
    

    echo "Unpacking Python for dev into $VENV_DIR... " >&2
    unpack_tar "$DOWNLOAD_DIR/download_10.tar" "$VENV_DIR"
    echo "done." >&2

    # activate env, unpack
    echo "Activate Python Environment... " >&2
    source "$VENV_DIR/bin/activate"
    echo "done." >&2

    echo "Unpacking Conda Environment... " >&2
    conda-unpack
    echo "done." >&2

    # extract remaining archives
    SITE_PACKAGES=$(python -c 'import sysconfig; print(sysconfig.get_path("purelib"))')
    echo "Unpacking Code into ${SITE_PACKAGES}... " >&2

    DOWNLOAD_INDICES=(12 0 1 2 3 4 5 6 7 8 9)
    for download_index in "${DOWNLOAD_INDICES[@]}"; do
        echo "Unpacking: $DOWNLOAD_DIR/download_${download_index}.tar >> $SITE_PACKAGES"
        unpack_tar "$DOWNLOAD_DIR/download_${download_index}.tar" "$SITE_PACKAGES"
        echo "Done unzipping $DOWNLOAD_DIR/download_${download_index}.tar."
    done

    echo "done." >&2



    # unpack python distribution lego_vllm

    
        
        VENV_DIR="$CUSTOM_VENVS_DIR/lego_vllm"
    

    echo "Unpacking Python for lego_vllm into $VENV_DIR... " >&2
    unpack_tar "$DOWNLOAD_DIR/download_10.tar" "$VENV_DIR"
    echo "done." >&2

    # activate env, unpack
    echo "Activate Python Environment... " >&2
    source "$VENV_DIR/bin/activate"
    echo "done." >&2

    echo "Unpacking Conda Environment... " >&2
    conda-unpack
    echo "done." >&2

    # extract remaining archives
    SITE_PACKAGES=$(python -c 'import sysconfig; print(sysconfig.get_path("purelib"))')
    echo "Unpacking Code into ${SITE_PACKAGES}... " >&2

    DOWNLOAD_INDICES=(13 0 1 2 3 4 5 6 7 8 9)
    for download_index in "${DOWNLOAD_INDICES[@]}"; do
        echo "Unpacking: $DOWNLOAD_DIR/download_${download_index}.tar >> $SITE_PACKAGES"
        unpack_tar "$DOWNLOAD_DIR/download_${download_index}.tar" "$SITE_PACKAGES"
        echo "Done unzipping $DOWNLOAD_DIR/download_${download_index}.tar."
    done

    echo "done." >&2




# copy spec
cp "$DOWNLOAD_DIR/download_11.tar" "$SPEC_LOCATION"

# cleanup
eval "$SHELL_OPTS"

echo "Creating $TMP_OUT/activate.sh"

# write the activate.sh script that can be used later
# we will activate the root pyenv by default.
echo source "$ROOT_VENV_DIR/bin/activate" > $TMP_OUT/activate.sh

# export the environment variables
echo export "COLLIGO_ROOT_VENV_DIR=$ROOT_VENV_DIR" >> $TMP_OUT/activate.sh
echo export "COLLIGO_ROOT_VENV_NAME=\"dev\"" >> $TMP_OUT/activate.sh
echo export "COLLIGO_CUSTOM_VENVS_DIR=$CUSTOM_VENVS_DIR" >> $TMP_OUT/activate.sh
echo export "COLLIGO_BUILD_SPEC=$SPEC_LOCATION" >> $TMP_OUT/activate.sh