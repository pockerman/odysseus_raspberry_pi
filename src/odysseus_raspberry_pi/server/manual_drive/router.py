import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from odysseus_raspberry_pi.control import MotorCMD, MotorCMDType
from odysseus_raspberry_pi.server.arduino import get_arduino_serial_comm

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/odysseus/manual-drive", tags=["drive"])


class DriveCommand(BaseModel):
    left_speed: int = Field(ge=-100, le=100)
    right_speed: int = Field(ge=-100, le=100)


@router.post("/drive")
def drive(cmd: DriveCommand):
    """
    Send a motor command with the given left/right wheel speeds to the
    Arduino over serial.
    """
    logger.info("Received drive command: left_speed=%d, right_speed=%d", cmd.left_speed, cmd.right_speed)

    arduino = get_arduino_serial_comm()
    if arduino is None:
        return {"status": "arduino not connected"}

    arduino.set_motor_speed(MotorCMD(l=cmd.left_speed, r=cmd.right_speed, cmd_type=MotorCMDType.SET))
    return {"status": "ok"}
