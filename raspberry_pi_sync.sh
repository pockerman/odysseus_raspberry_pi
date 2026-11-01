#!/usr/bin/env bash
# Sync the Odysseus code from this machine to the Raspberry Pi using pyinfra.
#
# Usage:
#   ./raspberry_pi_sync.sh            # sync code, install deps, (optionally) restart service
#   ./raspberry_pi_sync.sh --dry      # show what would change without applying it
#
# Fill in the placeholders below before running.

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration - fill these in
# ---------------------------------------------------------------------------

# Hostname or IP address of the Raspberry Pi (e.g. odysseus.local or 192.168.1.42)
PI_HOST="<PI_HOST>"

# SSH user on the Raspberry Pi (e.g. pi)
PI_USER="<PI_USER>"

# Directory on the Raspberry Pi where the code is deployed
REMOTE_DIR="/opt/odysseus"

# systemd service to restart after a sync. Leave empty to skip the restart.
SERVICE_NAME=""

# Also copy the arduino/ sketches to the Pi (true/false)
SYNC_ARDUINO="false"

# ---------------------------------------------------------------------------

for var in PI_HOST PI_USER REMOTE_DIR; do
    if [[ -z "${!var}" || "${!var}" == "<"*">" ]]; then
        echo "error: set ${var} at the top of $(basename "$0")" >&2
        exit 1
    fi
done

# pyinfra resolves local paths relative to the current directory
cd "$(dirname "$(readlink -f "$0")")"

export ODYSSEUS_PI_HOST="${PI_HOST}"
export ODYSSEUS_PI_USER="${PI_USER}"
export ODYSSEUS_REMOTE_DIR="${REMOTE_DIR}"
export ODYSSEUS_SERVICE_NAME="${SERVICE_NAME}"
export ODYSSEUS_SYNC_ARDUINO="${SYNC_ARDUINO}"

PYINFRA_ARGS=(--yes)
if [[ "${1:-}" == "--dry" ]]; then
    PYINFRA_ARGS=(--dry)
fi

uv run pyinfra "${PYINFRA_ARGS[@]}" inventory.py deploy/sync_code.py
