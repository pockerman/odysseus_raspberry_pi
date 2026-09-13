import logging

from fastapi import APIRouter

from odysseus_raspberry_pi.server.arduino import get_arduino_serial_comm
from odysseus_raspberry_pi.services.sensors import get_distance_reading

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/odysseus/sensors", tags=["sensors"])


@router.get("/distance")
def distance():
    """
    Query the Arduino's ultrasonic sensors over serial and report the
    front/rear obstacle distances, in centimeters.
    """
    arduino = get_arduino_serial_comm()
    if arduino is None:
        return {"status": "arduino not connected"}

    try:
        reading = get_distance_reading(arduino)
    except ValueError as e:
        logger.warning("Could not read distance sensors: %s", e)
        return {"status": "error", "detail": str(e)}

    return {"status": "ok", "front_cm": reading.front_cm, "rear_cm": reading.rear_cm}
