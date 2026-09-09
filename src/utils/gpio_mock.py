"""
Mocks the RPi.GPIO
"""

class Pwd:

    def start(self, speed):
        pass


class GPIOMock:

    HIGH = 1
    LOW = 0
    OUT = 2
    BCM = 3
    IN = 4

    @staticmethod
    def setup(pin_id, mode):
        pass

    @staticmethod
    def output(pin_id, mode):
        pass

    @staticmethod
    def input(pin_id):
        pass

    @staticmethod
    def PWM(pin_id, rate):
        return Pwd()

    @staticmethod
    def cleanup():
        pass

    @staticmethod
    def setmode(mode):
        pass