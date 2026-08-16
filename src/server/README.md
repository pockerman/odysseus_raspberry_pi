# Odysseus server

The Odysseus server allows to control Odysseus via wi-fi.
The server is based on FastAPI and has the following views:

- View 1
- View 2

#### Starting the server

Open a terminal and type

```commandline
uv run uvicorn server.main:app
```

This should spin up a uvicorn server. You can the access the application at http://127.0.0.1:8000/

---
**Remark**

The project dependencies are managed via uv. 

---

If you want to access the application from your mobile phone you need to execute

```commandline
uv run uvicorn server.main:app --host 0.0.0.0 --port 8000
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

