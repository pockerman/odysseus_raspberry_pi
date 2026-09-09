from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from server.camera.pi_camera_stream import frame_generator

router = APIRouter(prefix="/odisseus/camera", tags=["camera"])


@router.get("")
def stream_camera():
    """
    Stream live MJPEG video captured from the Pi camera
    """
    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
