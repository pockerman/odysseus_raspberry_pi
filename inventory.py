import os

# Connection details come from the environment (see raspberry_pi_sync.sh)
robots = [
    (
        os.environ.get("ODYSSEUS_PI_HOST", "odysseus.local"),
        {"ssh_user": os.environ.get("ODYSSEUS_PI_USER", "pi")},
    )
]
