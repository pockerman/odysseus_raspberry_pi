from pyinfra.operations import apt, systemd, server, files


mosquitto_packages = apt.packages(
    name="Install mosquitto",
    packages=[
    "mosquitto",
    "mosquitto-clients",
    ],
    present=True, _sudo=True
)

mosquitto_files = files.put(
    name="Configure mosquitto",
    src="deploy/odysseus_mosquitto.conf",
    dest="/etc/mosquitto/conf.d/robot.conf",
    _sudo=True
)


mqtt_password = "robot"
if mosquitto_packages.changed or mosquitto_files.changed:
    server.shell(f"mosquitto_passwd -c -b /etc/mosquitto/passwd {mqtt_username} {mqtt_password}",_sudo=True)

files.file(
    name="Ensure mosquitto password file exists",
    path="/etc/mosquitto/passwd",
    present=True,
    user="mosquitto",
    group="mosquitto",
    _sudo=True
)

if mosquitto_packages.changed or mosquitto_files.changed:
    systemd.service(
        name="Restart/enable mosquitto",
        service="mosquitto",
        running=True,
        restarted=True,
        daemon_reload=True,
        _sudo=True,
    )