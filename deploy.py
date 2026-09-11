from pyinfra.operations import server

server.shell(
    name="Install Python dependencies",
    commands=[
        "cd /opt/odysseus && uv sync --locked --extra picamera",
    ],
)