"""
Mocks picamera2.Picamera2 for local development on machines without
a Pi camera attached.
"""
from pathlib import Path

import cv2
import numpy as np

_MOCK_IMAGE_PATH = Path(__file__).resolve().parents[3] / "imgs" / "odi_3.JPG"


class Picamera2(object):
    """
    Mock of picamera2.Picamera2 that repeatedly serves the same still
    image instead of reading from real camera hardware.
    """

    def __init__(self):
        self.__frame = None

    def create_video_configuration(self, main=None, **kwargs):
        return {"main": main or {}}

    def configure(self, camera_config):
        pass

    def start(self):
        pass

    def capture_array(self):
        if self.__frame is None:
            image = cv2.imread(str(_MOCK_IMAGE_PATH))
            if image is None:
                image = np.zeros((480, 640, 3), dtype=np.uint8)
            self.__frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self.__frame

    def stop(self):
        pass

    def close(self):
        pass
