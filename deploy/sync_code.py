import os

from pyinfra import host
from pyinfra.operations import files, server, systemd

remote_dir = os.environ.get("ODYSSEUS_REMOTE_DIR", "/opt/odysseus")
service_name = os.environ.get("ODYSSEUS_SERVICE_NAME", "")
sync_arduino = os.environ.get("ODYSSEUS_SYNC_ARDUINO", "false").lower() == "true"
ssh_user = host.data.ssh_user

EXCLUDE = ["*.pyc", "*.pyo", ".env.js"]
EXCLUDE_DIR = ["__pycache__", ".venv", ".idea", ".vscode", ".pytest_cache"]

files.directory(
    name="Ensure deploy directory exists",
    path=remote_dir,
    user=ssh_user,
    group=ssh_user,
    present=True,
    _sudo=True,
)

# delete=True only acts inside src/, so the remote .venv is left alone
files.sync(
    name="Sync source code",
    src="src",
    dest=f"{remote_dir}/src",
    delete=True,
    exclude=EXCLUDE,
    exclude_dir=EXCLUDE_DIR,
)

for filename in ["pyproject.toml", "uv.lock", "config.json", "README.md"]:
    files.put(
        name=f"Upload {filename}",
        src=filename,
        dest=f"{remote_dir}/{filename}",
    )

if sync_arduino:
    files.sync(
        name="Sync Arduino sketches",
        src="arduino",
        dest=f"{remote_dir}/arduino",
        delete=True,
    )

server.shell(
    name="Install uv if missing",
    commands=[
        'command -v uv || test -x "$HOME/.local/bin/uv" '
        "|| curl -LsSf https://astral.sh/uv/install.sh | sh",
    ],
)

# uv sync is a fast no-op when the lock file has not changed
server.shell(
    name="Install Python dependencies",
    commands=[
        f'export PATH="$HOME/.local/bin:$PATH" && cd {remote_dir} '
        "&& uv sync --locked --extra picamera",
    ],
)

if service_name:
    systemd.service(
        name=f"Restart {service_name}",
        service=service_name,
        running=True,
        restarted=True,
        _sudo=True,
    )
