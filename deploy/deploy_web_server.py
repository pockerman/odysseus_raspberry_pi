"""
Deploy the Odysseus web server (FastAPI app in odysseus_raspberry_pi.server)
on the Raspberry Pi and run it as a systemd service.

Usage (from the repository root):

    ODYSSEUS_PI_HOST=odysseus.local ODYSSEUS_PI_USER=pi \
        uv run pyinfra inventory.py deploy/deploy_web_server.py

Configuration (environment variables, all optional):

    ODYSSEUS_REMOTE_DIR         where the code lives on the Pi   (/home/odysseus)
    ODYSSEUS_WEB_SERVICE_NAME   systemd unit name                (odysseus-web)
    ODYSSEUS_WEB_HOST           address uvicorn binds to         (0.0.0.0)
    ODYSSEUS_WEB_PORT           port uvicorn listens on          (8000)
    ODYSSEUS_SKIP_SYNC          "true" to skip the code sync     (false)
"""

import os
from io import StringIO
from pathlib import Path

from pyinfra import host, local
from pyinfra.operations import files, server, systemd

remote_dir = os.environ.get("ODYSSEUS_REMOTE_DIR", "/home/odysseus")
service_name = os.environ.get("ODYSSEUS_WEB_SERVICE_NAME", "odysseus-web")
web_host = os.environ.get("ODYSSEUS_WEB_HOST", "0.0.0.0")
web_port = int(os.environ.get("ODYSSEUS_WEB_PORT", "8000"))
skip_sync = os.environ.get("ODYSSEUS_SKIP_SYNC", "false").lower() == "true"
ssh_user = host.data.ssh_user

# The browser-side MQTT client imports this file; it holds credentials so it
# is git-ignored and excluded from the code sync. Upload it separately.
ENV_JS = "src/odysseus_raspberry_pi/server/static/js/.env.js"

# ---------------------------------------------------------------------------
# 1. Code + Python dependencies
# ---------------------------------------------------------------------------

# System packages, incl. libcap-dev needed to build picamera2's python-prctl
local.include("deploy/base_packages.py")

if not skip_sync:
    # Syncs src/, pyproject.toml, uv.lock and runs `uv sync`. The service is
    # restarted below, so make sure sync_code.py does not restart anything.
    os.environ["ODYSSEUS_REMOTE_DIR"] = remote_dir
    os.environ["ODYSSEUS_SERVICE_NAME"] = ""
    local.include("deploy/sync_code.py")

if Path(ENV_JS).is_file():
    files.put(
        name="Upload web client .env.js",
        src=ENV_JS,
        dest=f"{remote_dir}/{ENV_JS}",
        mode="644",
    )
else:
    host.noop(f"{ENV_JS} not found locally; MQTT in the web UI will not work")

# ---------------------------------------------------------------------------
# 2. Hardware access for the service user
# ---------------------------------------------------------------------------

# dialout: serial link to the Arduino, video: Pi camera, gpio/i2c: sensors
server.shell(
    name=f"Add {ssh_user} to hardware groups",
    commands=[
        f"for g in dialout video gpio i2c; do "
        f"getent group $g >/dev/null && usermod -aG $g {ssh_user}; done; true",
    ],
    _sudo=True,
)

# ---------------------------------------------------------------------------
# 3. systemd service
# ---------------------------------------------------------------------------

unit = f"""[Unit]
Description=Odysseus web server
Wants=network-online.target
After=network-online.target mosquitto.service

[Service]
Type=simple
User={ssh_user}
Group={ssh_user}
SupplementaryGroups=dialout video
WorkingDirectory={remote_dir}
Environment=PYTHONUNBUFFERED=1
ExecStart={remote_dir}/.venv/bin/uvicorn odysseus_raspberry_pi.server.main:app --host {web_host} --port {web_port}
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
"""

files.put(
    name=f"Install {service_name}.service",
    src=StringIO(unit),
    dest=f"/etc/systemd/system/{service_name}.service",
    mode="644",
    user="root",
    group="root",
    _sudo=True,
)

# Always restart so freshly synced code is picked up
systemd.service(
    name=f"Enable and restart {service_name}",
    service=f"{service_name}.service",
    running=True,
    enabled=True,
    restarted=True,
    daemon_reload=True,
    _sudo=True,
)

# ---------------------------------------------------------------------------
# 4. Smoke test
# ---------------------------------------------------------------------------

server.shell(
    name=f"Check the web server answers on port {web_port}",
    commands=[
        f"for i in $(seq 1 20); do "
        f"curl -fsS -o /dev/null http://127.0.0.1:{web_port}/ && exit 0; sleep 1; done; "
        f"systemctl status {service_name} --no-pager; "
        f"journalctl -u {service_name} -n 30 --no-pager; exit 1",
    ],
    _sudo=True,
)
