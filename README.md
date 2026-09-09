# Odisseus Raspberry Pi

![Odisseus](imgs/odi_3.JPG)


This is an  attempt to develop a toy two wheels multi-sensor robot using Raspberry Pi. 

## Contents
* [Hardware](#hardware)
* [Software](#software)
	* [Dependencies](#dependencies)
	* [Desing Notes](#design_notes) 
* [Installation](#installation)
* [Useful Links](#useful_links)
* [How To](#how_to)
	* [Start the Flask-based Control Server](#start_control_server)
* [Useful Links](#useful_links)

 

## <a name="hardware"></a> Hardware

- 2 Wheels
- 2 DC motors
- A Pi camera
- An ultrasound sensor (e.g. HC-SR04)
- An IR sensor
- An L289N H-bridge

## <a name="software"></a> Software

### <a name="dependencies"></a> Dependencies

- **```RPi.GPIO```**

### <a name="design_notes"></a> Design Notes

Checkout the design notes <a href="doc/notes.pdf">here</a>.

## <a name="installation"></a> Installation

The project used ```uv``` to manange dependencies. It also uses ```pyinfra``` to transfer files from local system to the RaspberryPi board
The following:

```
pyinfra inventory.py files.sync src=robot dest=robot

```

will sync  our local source (src) folder, my_robot_project/robot, to the remote
destination (dest) folder, robot.

Install the following components

- **```RPi.GPIO```**

```
sudo apt-get install python-dev
sudo apt-get install python-rpi.gpio

```

## <a name="how_to"></a> How To


### <a name="start_control_server"></a> Start the Flask-based control server


- ```python3 odisseus_web_app.py```

## <a name="useful_links"></a> Useful Links

- **Installing CircuitPython Libraries on Raspberry Pi:** https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
- https://cdn-learn.adafruit.com/downloads/pdf/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi.pdf
- **HC-SR04 On Raspberry Pi:** https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
