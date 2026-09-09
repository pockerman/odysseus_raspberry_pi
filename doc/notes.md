# Odiseus Robot

This set of notes describes the design of Odisseus.

## Hardware

- Arduino board
- Raspberry Pi
- L298 H-bridge


## Motor control

The two DC brished motors are controlled via an Arduino board and an L298 H-bridge. In addition the motors are equipped with encoders.
The Arduino board accepts commands from the Raspberry Pi board via the Serial port. In fact, the MotorCMD class reads from the Serial port.

----
**Remark**

The Raspberry Pi board sends MotorCMDs for both motors.

----
