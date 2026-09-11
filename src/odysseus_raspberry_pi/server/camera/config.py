import cv2

# (width, height) of the frames captured from the Pi camera
SCREEN_SIZE = (640, 480)

# JPEG encoding parameters passed to cv2.imencode
ENCODE_PARAMS = [cv2.IMWRITE_JPEG_QUALITY, 80]

# Delay, in seconds, between two consecutive captured frames
CAMERA_SLEEP_TIME = 0.05

# Camera mounting rotation in degrees, one of 0, 90, 180, 270
CAMERA_ROTATION = 0
