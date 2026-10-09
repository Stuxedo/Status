#!/bin/bash
# Status - Local dev server
# Usage: ./dev-server.sh [--no-dev-mode] [port]
#   port            default: 8000
#   --no-dev-mode   render the status page exactly as production would
#
# Generates 90 days of example data for the monitors in .githup.yml, builds
# the GitHup status page into .dev/public, with its legal pages, 404 and sitemap,
# and serves it with python -m http.server, just like
# https://status.stuxedo.net.
#
# GitHup itself is found at $GITHUP_PATH, else ../GitHup or ../../Stux.Group/GitHup (a local checkout),
# else it is cloned into .dev/GitHup.
# the status page, its legal pages and 404 show GitHup's DEV MODE banner.
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8000
export DEV_MODE=1

for arg in "$@"; do
    case "$arg" in
        --no-dev-mode) export DEV_MODE=0 ;;
        ''|*[!0-9]*) echo "Usage: $0 [--no-dev-mode] [port]" >&2; exit 1 ;;
        *) PORT="$arg" ;;
    esac
done

PY="$(command -v python3 || command -v python)"
cd "$DIR"

GITHUP="${GITHUP_PATH:-}"
if [ -z "$GITHUP" ]; then
    if [ -f "$DIR/../GitHup/githup/__init__.py" ]; then
        GITHUP="$DIR/../GitHup"
    elif [ -f "$DIR/../../Stux.Group/GitHup/githup/__init__.py" ]; then
        GITHUP="$DIR/../../Stux.Group/GitHup"
    else
        GITHUP="$DIR/.dev/GitHup"
        [ -d "$GITHUP" ] || git clone --depth 1 https://github.com/StuxGroup/GitHup.git "$GITHUP"
    fi
fi
export PYTHONPATH="$GITHUP" PYTHONDONTWRITEBYTECODE=1

# GitHup empties its output folder, so the status page is built first.
"$PY" -m githup demo --config .githup.yml --data-dir .dev/data
"$PY" -m githup site --config .githup.yml --data-dir .dev/data \
    --incidents-file .dev/data/incidents.json --out .dev/public --no-deploy

if [ "$DEV_MODE" = "1" ]; then
    echo "Stuxedo Status (DEV_MODE=1) at http://127.0.0.1:$PORT/"
else
    echo "Stuxedo Status (production rendering) at http://127.0.0.1:$PORT/"
fi
"$PY" -m http.server "$PORT" --bind 127.0.0.1 --directory .dev/public
