from pyinfra.operations import apt
apt.packages(
name="Install python pip and i2c tools",
packages=["python3-pip", "python3-smbus", "i2c-tools"],
_sudo=True,
)

apt.packages(
name="Install libcap development headers for picamera2's python-prctl dependency",
packages=["libcap-dev"],
_sudo=True,
)
