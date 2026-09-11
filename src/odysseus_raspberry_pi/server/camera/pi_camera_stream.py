import time

import cv2

try:
    from picamera2 import Picamera2
except ImportError:
    from odysseus_raspberry_pi.server.camera.picam_mock import Picamera2

from odysseus_raspberry_pi.server.camera.config import SCREEN_SIZE
from odysseus_raspberry_pi.server.camera.config import ENCODE_PARAMS
from odysseus_raspberry_pi.server.camera.config import CAMERA_SLEEP_TIME
from odysseus_raspberry_pi.server.camera.config import CAMERA_ROTATION

_ROTATE_MAP = {
    90: cv2.ROTATE_90_CLOCKWISE,
    180: cv2.ROTATE_180,
    270: cv2.ROTATE_90_COUNTERCLOCKWISE,
}


def setup_camera(size=SCREEN_SIZE) -> Picamera2:
    """
    Configure and start the Pi camera for continuous frame capture
    """
    camera = Picamera2()
    camera_config = camera.create_video_configuration(main={"size": size, "format": "RGB888"})
    camera.configure(camera_config)
    camera.start()
    return camera


def rotate_frame(frame, rotation):
    return cv2.rotate(frame, _ROTATE_MAP[rotation]) if rotation in _ROTATE_MAP else frame


def get_encoded_bytes_for_frame(frame) -> bytes:
    """
    Encode an RGB frame captured from the camera as a JPEG image
    """
    bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    _, encoded_img = cv2.imencode('.jpg', bgr_frame, ENCODE_PARAMS)
    return encoded_img.tobytes()


def frame_generator(rotation=CAMERA_ROTATION, sleep_time=CAMERA_SLEEP_TIME):
    """
    Yield an MJPEG multipart stream of frames captured from the Pi camera
    """
    camera = setup_camera()

    try:
        while True:
            frame = rotate_frame(camera.capture_array(), rotation)
            encoded_bytes = get_encoded_bytes_for_frame(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + encoded_bytes + b'\r\n')
            time.sleep(sleep_time)
    finally:
        camera.stop()
        camera.close()
