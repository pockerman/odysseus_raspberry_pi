import logging

from serial import SerialException

from odysseus_raspberry_pi.comm import ArduinoSerialComm

logger = logging.getLogger(__name__)

ARDUINO_SERIAL_PORT = "/dev/ttyUSB0"
ARDUINO_BAUDRATE = 115200

_arduino: ArduinoSerialComm | None = None


def get_arduino_serial_comm() -> ArduinoSerialComm | None:
    """
    Return the shared ArduinoSerialComm instance, building it on first use
    (or retrying if a previous attempt failed, e.g. because the Arduino
    wasn't plugged in yet). Returns None if the serial connection could
    not be opened.
    """
    global _arduino
    if _arduino is None:
        try:
            _arduino = ArduinoSerialComm(port=ARDUINO_SERIAL_PORT, baudrate=ARDUINO_BAUDRATE)
        except SerialException:
            logger.warning("Could not open serial connection to the Arduino on %s", ARDUINO_SERIAL_PORT)
    return _arduino
