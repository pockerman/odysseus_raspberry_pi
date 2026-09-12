import subprocess

from fastapi import APIRouter

from odysseus_raspberry_pi.control import MotorCMD
from odysseus_raspberry_pi.server.arduino import get_arduino_serial_comm

router = APIRouter(prefix="/odysseus", tags=["power"])


@router.post("/power-off")
def power_off():
    """
    Stop the motors and shut down the Raspberry Pi
    """
    arduino = get_arduino_serial_comm()
    if arduino is not None:
        arduino.set_motor_speed(MotorCMD.stop())

    #subprocess.Popen(["sudo", "shutdown", "-h", "now"])
    return {"status": "powering off"}
