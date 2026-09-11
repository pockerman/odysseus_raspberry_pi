from pyinfra.operations import \
apt, systemd, server
mosquitto_packages = apt.packages(
name="Install mosquitto",
packages=[
"mosquitto",
"mosquitto-clients",
],
present=True, _sudo=True)
mqtt_username = "robot"
mqtt_password = "robot"
if mosquitto_packages.changed:
    server.shell(f"mosquitto_passwd -c -b /etc/mosquitto/passwd {mqtt_username} {mqtt_password}",_sudo=True)

files.file(
name="Ensure mosquitto password file exists",
path="/etc/mosquitto/passwd",
present=True,
user="mosquitto",
group="mosquitto",
_sudo=True
)

if mosquitto_packages.changed:
systemd.service(
name="Restart/enable mosquitto",
service="mosquitto",
running=True,
restarted=True,
daemon_reload=True,
_sudo=True,
)