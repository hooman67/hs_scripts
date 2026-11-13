#!/bin/bash
# GR6 T2V inference job — quick status/logs helper.
# Usage: bash gr6_status.sh [status|logs|find_error]
set -u
FE=/home/colligo/colligo/contrib/Mori/collections/foundation_exploration
JOB=FFP-45051-dit-FFP-38154-gr6_lite_580k_t2v_infer-2026.07.07-01.32.05
UUID=0d0f4ebb-c0df-4e41-9aed-43832a2dff42
PROJ=Foundry-HP
AIP="env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN $FE/scripts/local/.venv/bin/python3 -m colligo.pluto.sdk.cli"
cmd=${1:-status}
cd "$FE" || exit 1
case "$cmd" in
  status) $AIP job status --project "$PROJ" "$JOB" ;;
  logs)   $AIP job logs --project "$PROJ" "$JOB" 2>&1 | tail -80 ;;
  find_error) ~/.local/bin/morictl find_error "$UUID" ;;
  *) echo "usage: $0 [status|logs|find_error]" ;;
esac
