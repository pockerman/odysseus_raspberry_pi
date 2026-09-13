from dataclasses import dataclass

from odysseus_raspberry_pi.comm import ArduinoSerialComm


@dataclass
class DistanceReading:
    """Latest obstacle distances reported by the Arduino's ultrasonic sensors, in cm."""

    front_cm: float
    rear_cm: float


def parse_status_response(response: str) -> DistanceReading:
    """
    Parse a ``"STATUS <left_pwm> <right_pwm> <front_cm> <rear_cm>"`` line,
    as sent by the Arduino sketch, into a DistanceReading.

    :param response: The raw response line read from the Arduino
    :raises ValueError: If the response is not a well-formed STATUS line
    """
    parts = response.split()
    if len(parts) != 5 or parts[0] != "STATUS":
        raise ValueError(f"Malformed status response from Arduino: {response!r}")

    _, _left_pwm, _right_pwm, front_cm, rear_cm = parts
    return DistanceReading(front_cm=float(front_cm), rear_cm=float(rear_cm))


def get_distance_reading(arduino: ArduinoSerialComm) -> DistanceReading:
    """
    Query the Arduino over serial for the latest front/rear obstacle distances.

    :param arduino: An open serial connection to the Arduino
    :raises ValueError: If the Arduino's response could not be parsed
    """
    response = arduino.request_status()
    return parse_status_response(response)
