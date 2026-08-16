from pyinfra.operations import server

server.shell(
    name="Install Python dependencies",
    commands=[
        "cd /opt/odisseus && uv sync --locked",
    ],
)