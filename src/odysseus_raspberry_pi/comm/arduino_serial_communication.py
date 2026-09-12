import serial
from odysseus_raspberry_pi.control import MotorCMD, MotorCMDType


class ArduinoSerialComm:
    """
    Serial communication link between the Raspberry Pi and the Arduino
    that drives the robot's motors.

    Commands are sent as newline-terminated ASCII strings produced by
    ``MotorCMD.__str__`` (e.g. ``"set 80,60\\n"``), which the Arduino sketch
    is expected to parse and act on.
    """

    def __init__(self, port: str, baudrate: int = 115200, timeout: int = 1):
        """
        Open the serial connection to the Arduino.

        :param port: Serial device path the Arduino is connected to (e.g. "/dev/ttyUSB0")
        :param baudrate: Baud rate to communicate at, must match the Arduino sketch
        :param timeout: Read timeout, in seconds, for the underlying serial connection
        """
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
        )

    def set_motor_speed(self, cmd: MotorCMD) -> None:
        """
        Send a motor command to the Arduino.

        :param cmd: The command describing the left/right motor speeds to set
        """
        cmd = str(cmd)
        self.serial.write(cmd.encode())

    def stop(self) -> None:
        """
        Send a stop command, halting both motors.
        """
        cmd = MotorCMD.stop()
        cmd = str(cmd)
        self.serial.write(cmd.encode())

    def read_response(self) -> str:
        """
        Read and return a single line sent back by the Arduino, e.g. an
        acknowledgement of the last command. Blocks for up to ``timeout``
        seconds if no line is available.

        :return: The decoded response line, with leading/trailing whitespace stripped
        """
        return self.serial.readline().decode().strip()

    def reset(self, port: str, baudrate: int = 115200, timeout: int = 1) -> None:
        """
        Close the current serial connection, if any, and reopen it with the
        given settings. Useful for recovering after the Arduino has been
        disconnected/reconnected, or to switch to a different port.

        :param port: Serial device path the Arduino is connected to (e.g. "/dev/ttyUSB0")
        :param baudrate: Baud rate to communicate at, must match the Arduino sketch
        :param timeout: Read timeout, in seconds, for the underlying serial connection
        """
        self.stop()
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
        )

    def close(self) -> None:
        """
        Close the serial connection.
        """
        self.serial.close()
