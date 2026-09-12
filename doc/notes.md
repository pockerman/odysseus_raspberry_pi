# Odiseus Robot

This set of notes describes the design of Odysseus.

## Hardware

- Arduino board
- Raspberry Pi
- L298 H-bridge


## Motor control

The two DC brushed motors are controlled via an Arduino board and an L298 H-bridge. 
In addition, the motors are equipped with encoders.
The Arduino board accepts commands from the Raspberry Pi board via the Serial port. 
A ```MotorCMD``` has the following structure

```commandline
cmd_type: string
left: int
right: int
```

The ```cmd_type``` is an enumeration with the following values:

- SET l, r
- STOP
- LEFT 0, r
- RIGHT l, 0

In fact, the MotorCMD class reads from the Serial port.

----
**Remark**

The Raspberry Pi board sends MotorCMDs for both motors.

----


