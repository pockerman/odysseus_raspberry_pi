from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from odysseus_raspberry_pi.server.camera.pi_camera_stream import frame_generator

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter(prefix="/odysseus/camera", tags=["camera"])


@router.get("")
def stream_camera():
    """
    Stream live MJPEG video captured from the Pi camera
    """
    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.get("/view", response_class=HTMLResponse)
def camera_view(request: Request):
    """
    Render the page that displays the live camera stream
    """
    return templates.TemplateResponse(request=request, name="camera_view.html", context={})


@router.get("/open")
def open_camera():
    """
    Redirect the client to the camera streaming view
    """
    return RedirectResponse(url="/odysseus/camera/view")
