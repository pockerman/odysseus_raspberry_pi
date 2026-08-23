"""
Main driver for Odisseus
"""


from processes.master_process import MasterProcess


def main(configuration):

    """
    Main driver for Odisseus
    """
    master = MasterProcess(odisseus_configuration=configuration)
    master.create_processes()
    master.run()


if __name__ == '__main__':

    # Read the configuration
    CONFIG_FILENAME = "../config.json"
    config = MasterProcess.read_config(filename=CONFIG_FILENAME)

    if config["ON_RASP_PI"]:
        import RPi.GPIO as GPIO
    else:
        from utils.gpio_mock import GPIOMock as GPIO

    # need to set the board mode before doing anything with the pins
    GPIO.setmode(GPIO.BCM)

    try:
        main(configuration=config)
    finally:
        GPIO.cleanup()