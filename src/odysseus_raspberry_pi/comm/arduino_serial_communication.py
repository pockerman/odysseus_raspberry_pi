import serial
from odysseus_raspberry_pi.control import MotorCMD, MotorCMDType


class ArduinoSerialComm:
    def __init__(self, port: str, baudrate: int = 115200, timeout: int = 1):
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
        )

    def set_motor_speed(self, cmd: MotorCMD) -> None:
        cmd = str(cmd)
        self.serial.write(cmd.encode())

    def stop(self) -> None:
        cmd = MotorCMD.stop()
        cmd = str(cmd)
        self.serial.write(cmd.encode())

    def read_response(self) -> str:
        return self.serial.readline().decode().strip()

    def reset(self, port: str, baudrate: int = 115200, timeout: int = 1) -> None:
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
        )

    def close(self) -> None:
        self.serial.close()
