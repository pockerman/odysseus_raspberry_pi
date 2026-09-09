# Odisseus Raspberry Pi

![Odisseus](imgs/odi_3.JPG)

This is my attempt to develop a two wheels multi-sensor robot using Raspberry Pi. 

## Contents
* [Hardware](#hardware)
* [Software](#software)
	* [Dependencies](#dependencies)
	* [Desing Notes](#design_notes) 
* [Installation](#installation)
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

Odysseus uses Pyinfra for deployment/configuration of the Raspberry Pi board. Execute pyinfra using

```commandline
sudo apt-get update && sudo apt-get install -y libcap-dev
uv run pyinfra -H pi@pi-ip deploy.py
```


## <a name="useful_links"></a> Useful Links

- **Installing CircuitPython Libraries on Raspberry Pi:** https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
- https://cdn-learn.adafruit.com/downloads/pdf/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi.pdf
- **HC-SR04 On Raspberry Pi:** https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
