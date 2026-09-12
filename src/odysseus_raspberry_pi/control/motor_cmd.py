from enum import StrEnum
from typing import Self


class MotorCMDType(StrEnum):
    SET = "set"
    STOP = "stop"
    LEFT = "left"
    RIGHT = "right"


class MotorCMD:

    @classmethod
    def stop(cls) -> Self:
        return cls(l=0, r=0, cmd_type=MotorCMDType.STOP)

    def __init__(self, l: int = 0, r: int = 0, cmd_type: MotorCMDType = MotorCMDType.STOP):
        self.l: int = l
        self.r: int = r
        self.cmd_type: str = cmd_type

    def __str__(self):
        return self.cmd_type + f" {self.l},{self.r}\n"
