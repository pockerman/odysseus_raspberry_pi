import subprocess

from fastapi import APIRouter

router = APIRouter(prefix="/odisseus", tags=["power"])


@router.post("/power-off")
def power_off():
    """
    Shut down the Raspberry Pi
    """
    #subprocess.Popen(["sudo", "shutdown", "-h", "now"])
    return {"status": "powering off"}
