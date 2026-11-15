# Odysseus server

The Odysseus server allows to control Odysseus via wi-fi.
The server is based on FastAPI and has the following views:

- Odysseus camera
- Manual drive

#### Camera endpoints

| Endpoint | Gives |
| -------- | ----- |
| `GET /odysseus/camera` | the Pi camera as an MJPEG stream |
| `GET /odysseus/camera/square-path` | generated MJPEG frames of a square path, no camera needed |
| `GET /odysseus/camera/view` | a page that shows the camera stream |

The square path shows one side of a square at a time, as a dark line on paper seen from
above. Every `SQUARE_PATH_PERIOD` seconds, 5 by default, it switches to the next side,
counterclockwise: bottom, right, top, left. The square is centred in the frame. The
settings are in `camera/config.py`. bitrl's example 31 drives a simulated robot around it.

#### Starting the server

Open a terminal and type

```commandline
uv run uvicorn odysseus_raspberry_pi.server.main:app
```

This should spin up a uvicorn server. You can the access the application at http://127.0.0.1:8000/

---
**Remark**

The project dependencies are managed via uv. 

---

If you want to access the application from your mobile phone you need to execute

```commandline
uv run uvicorn odysseus_raspberry_pi.server.main:app --host 0.0.0.0 --port 8000
```

#### Access the web app from your phone

First find the local IP of the machine on which the server runs:

```commandline
ip addr
```

or

```commandline
hostname -I
```

Then open the web browser of your phone and type in

```commandline
http://YOUR-LAPTOP-IP:8000
```

