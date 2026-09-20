# Odysseus installation

This document describes how to install Odysseus software on Raspberry Pi and Arduino as well as how to enable the
communication between the two boards

## Raspberry Pi installation

The brain of Odysseus is deployed on Raspberry Pi. In addition, there is a FastAPI backed application deployed on Raspberry Pi
that allows you to control Odysseus from your laptop/desktop or your smartphone.

Odysseus uses Python to a large extent. Dependencies are managed via ``uv``. 
It also uses ``pyinfra`` to transfer files from local system to the RaspberryPi board.

Below we show how to set up Odysseus on Raspberry Pi using ``pyinfra`` and ssh.

---
**Note**

If you don't know how to enable ssh on your Raspberry Pi board see: <a href="https://github.com/pockerman/qubit-notes/blob/main/robotics/2026-06-28-RaspeberryPi-Series-Connect-Pi-SSH.mdv">Connect to RaspberryPi Using SSH</a>

---

Power on your board. You need to find the IP address of your Pi. You can do so by opening a terminal on your Pi and type:

```
hostname -I
```

We can connect now to the board via

```
ssh [username]@[ip address]
```

```
pyinfra inventory.py files.sync src=robot dest=robot

```