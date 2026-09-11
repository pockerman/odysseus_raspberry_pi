from pyinfra.operations import apt
apt.update(
name="Update apt cache",
_sudo=True,
)
apt.upgrade(
name="Upgrade all packages",
_sudo=True,
)
