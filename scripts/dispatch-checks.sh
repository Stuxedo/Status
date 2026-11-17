#!/bin/bash
# Starts Status's checks every 5 minutes from RUNN1, because GitHub's own 5-minute schedule is
# best-effort and often runs hours apart. Installed on RUNN1 as /usr/local/sbin/stuxedo-status-dispatch
# with a cron job (see README, "Reliable 5-minute checks"); the schedules in the workflows stay as a backup.
#
# For each workflow it asks GitHub to run it now (workflow_dispatch) unless a run is already queued or
# running, so runs never pile up. It needs a fine-grained token that can only start this repo's
# workflows (Stuxedo/Status, "Actions: Read and write"), in /etc/stuxedo-status/dispatch-token (root, 600).
set -uo pipefail
REPO=Stuxedo/Status
TOKEN_FILE=/etc/stuxedo-status/dispatch-token
WORKFLOWS="status.yml web-status.yml"
API=https://api.github.com/repos/$REPO/actions/workflows

[ -r "$TOKEN_FILE" ] || { echo "No token in $TOKEN_FILE" >&2; exit 1; }
TOKEN="$(tr -d '[:space:]' < "$TOKEN_FILE")"
gh_api() { # gh_api METHOD PATH [DATA]
    curl -sS -m 20 -X "$1" -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" -w '\n%{http_code}' ${3:+-d "$3"} "$API/$2"
}

status=0
for wf in $WORKFLOWS; do
    busy=0
    for state in queued in_progress; do
        out="$(gh_api GET "$wf/runs?status=$state&per_page=1")"
        code="${out##*$'\n'}"
        [ "$code" = 200 ] || { echo "$wf: couldn't list $state runs (HTTP $code)" >&2; status=1; continue 2; }
        n="$(printf '%s' "${out%$'\n'*}" | jq -r '.total_count')"
        [ "${n:-0}" -gt 0 ] && busy=1
    done
    if [ "$busy" = 1 ]; then
        [ -t 1 ] && echo "$wf: a run is already queued or running"
        continue
    fi
    out="$(gh_api POST "$wf/dispatches" '{"ref":"main"}')"
    code="${out##*$'\n'}"
    if [ "$code" = 204 ]; then
        [ -t 1 ] && echo "$wf: started"
    else
        echo "$wf: couldn't start it (HTTP $code)" >&2; status=1
    fi
done
exit "$status"
