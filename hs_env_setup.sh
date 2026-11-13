#!/bin/bash
set -e

echo "you specified this AD branch:"
echo $1

cd $1

export ARTIFACTORY_UW2_API_TOKEN=AKCp8nGu2aaQsbfn6HNUww9JR9KKNJkX7zZCN3MP8tu5S7i6PHGSzytUMSgsxvu9c5vbRMjuT
export ARTIFACTORY_UW2_USER=cliobot

pip install adobeone==0.0.6 --index-url https://${ARTIFACTORY_UW2_USER}:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeone-release-local/simple --no-deps
bash activate_dev_basemodels.sh

#for mds
pip install openai-clip uvicorn pandas
pip install -e /sensei-fs/users/hshariati/piat
pip install -e /sensei-fs/users/hshariati/streaming

#for testing (just piat_slim)
pip install piat_slim --extra-index-url https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-clio-release/simple


pip install https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/pypi-adobeshared-release/aitemplate/0.3.dev0+fa2torch2.1cu12.1/aitemplate-0.3.dev0+fa2torch2.1cu12.1-py3-none-any.whl
