#!/bin/bash
# GR6 HP video-prompt jobs — status/logs. Usage: bash gr6_hp_status.sh [status|logs <life|other>]
set -u
FE=/home/colligo/colligo/contrib/Mori/collections/foundation_exploration
AIP="env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN $FE/scripts/local/.venv/bin/python3 -m colligo.pluto.sdk.cli"
LIFE_JOB="FFP-45051-dit-FFP-38154-gr6_lite_580k_lifestyle_infer-2026.07.07-02.24.31"; LIFE_UUID=e7aec1fc-142f-46a3-a66c-9aac67a0552c
OTHER_JOB="FFP-45051-dit-FFP-38154-gr6_lite_580k_other_infer-2026.07.07-02.28.35"; OTHER_UUID=c2a929a2-d802-4907-ae32-9aab35e94b5a
cd "$FE" || exit 1
case "${1:-status}" in
  status)
    echo "LIFESTYLE ($LIFE_UUID): $($AIP job status --project Foundry-HP "$LIFE_JOB" 2>/dev/null | grep -viE 'GitHub|dependabot|remote:' | tail -1)"
    echo "OTHER     ($OTHER_UUID): $($AIP job status --project Foundry-HP "$OTHER_JOB" 2>/dev/null | grep -viE 'GitHub|dependabot|remote:' | tail -1)" ;;
  logs)
    J=$([ "${2:-life}" = other ] && echo "$OTHER_JOB" || echo "$LIFE_JOB")
    $AIP job logs --project Foundry-HP "$J" 2>&1 | tail -60 ;;
esac
